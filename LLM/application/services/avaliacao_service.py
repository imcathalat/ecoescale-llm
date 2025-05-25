import json
from application.LLMs.criteriosLLM import chain as criterios_chain
from application.LLMs.relatorioLLM import chain as relatorio_chain
from application.utils.criterios_loader import get_criterios_base

TOP_N      = 10# máximo a retornar
MIN_SCORE  = 3    # pontuação mínima

# ------------------------------------------------------------------
def _filtrar_top_scores(scores, min_score=MIN_SCORE, top_n=TOP_N):
    """Recebe lista [{'id': int, 'score': int}], devolve apenas os IDs válidos."""
    relevantes = [s for s in scores if s.get("score", 0) >= min_score]
    relevantes.sort(key=lambda s: s["score"], reverse=True)
    return [s["id"] for s in relevantes[:top_n]]

def _extrair_ids(bruto):
    """
    Tenta extrair lista de IDs:
      • se vier 'criterios_ids', usa direto;
      • se vier 'scores', processa com filtro;
    Retorna None se não encontrar.
    """
    # --- formato direto ---
    if isinstance(bruto, dict) and "criterios_ids" in bruto:
        return bruto["criterios_ids"]

    # --- formato com 'scores' ---
    if isinstance(bruto, dict) and "scores" in bruto:
        return _filtrar_top_scores(bruto["scores"])

    # --- dict {'input': ..., 'text': {...}} ---
    if isinstance(bruto, dict) and "text" in bruto:
        txt = bruto["text"]
        if isinstance(txt, dict):
            if "criterios_ids" in txt:
                return txt["criterios_ids"]
            if "scores" in txt:
                return _filtrar_top_scores(txt["scores"])
        if isinstance(txt, str):
            try:
                parsed = json.loads(txt)
                if "criterios_ids" in parsed:
                    return parsed["criterios_ids"]
                if "scores" in parsed:
                    return _filtrar_top_scores(parsed["scores"])
            except Exception:
                pass

    # --- string pura ---
    if isinstance(bruto, str):
        try:
            parsed = json.loads(bruto)
            if "criterios_ids" in parsed:
                return parsed["criterios_ids"]
            if "scores" in parsed:
                return _filtrar_top_scores(parsed["scores"])
        except Exception:
            pass

    return None
# ------------------------------------------------------------------

def avaliar_criterios(contexto: dict) -> dict:
    try:
        criterios_base = get_criterios_base()

        payload = {
            "contexto": contexto.get("contexto", ""),
            "lista_criterios": [
                {"id": c["id"], "nome": c["nome"]}
                for area in criterios_base["areas"]
                for tema in area["temas"]
                for c in tema["criterios"]
            ],
        }

        bruto   = criterios_chain.invoke({"input": json.dumps(payload, ensure_ascii=False)})
        ids     = _extrair_ids(bruto)

        if ids is None:
            print("[DEBUG] resposta inesperada da LLM:", bruto)
            return {"erro": "Resposta da LLM fora do formato esperado."}

        return {"criterios_ids": ids[:TOP_N]}   # garantia final

    except Exception as exc:
        return {"erro": str(exc)}

# ------------------------------------------------------------------
def _extrair_relatorio(bruto):
    """Devolve somente o dicionário com nota + relatorio."""
    # 1) já é o JSON final
    if isinstance(bruto, dict) and "nota_sustentabilidade" in bruto:
        return bruto

    # 2) formato {'input': ..., 'text': {...}}
    if isinstance(bruto, dict) and "text" in bruto:
        txt = bruto["text"]
        if isinstance(txt, dict) and "nota_sustentabilidade" in txt:
            return txt
        if isinstance(txt, str):
            try:
                parsed = json.loads(txt)
                if "nota_sustentabilidade" in parsed:
                    return parsed
            except Exception:
                pass

    # 3) string pura
    if isinstance(bruto, str):
        try:
            parsed = json.loads(bruto)
            if "nota_sustentabilidade" in parsed:
                return parsed
        except Exception:
            pass

    return None
# ------------------------------------------------------------------

def avaliar_empresa(respostas: dict, empresa: dict) -> dict:
    """
    respostas -> JSON com respostas da empresa
    empresa   -> dados da empresa
    """
    try:
        payload = {
            "empresa": empresa,
            "questionario": respostas
        }
        entrada = json.dumps(payload, ensure_ascii=False)
        bruto   = relatorio_chain.invoke({"input": entrada})

        relatorio = _extrair_relatorio(bruto)
        if relatorio is None:
            print("[DEBUG] resposta inesperada da LLM:", bruto)
            return {"erro": "Resposta da LLM fora do formato esperado."}

        return relatorio      # ✅ devolve só o JSON desejado

    except Exception as exc:
        return {"erro": str(exc)}
    
