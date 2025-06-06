from flask import request, jsonify
from application.services.avaliacao_service import avaliar_empresa
from application.services.avaliacao_service import avaliar_criterios
import sys

def avaliar_criterios_controller():
    try:
        data = request.get_json(force=True) or {}

        # --- obtém o contexto ---
        contexto_raw = data.get("contexto")
        if contexto_raw is None:
            return jsonify({"erro": "Campo 'contexto' obrigatório."}), 400

        # Aceita string OU objeto
        if isinstance(contexto_raw, str):
            contexto_dict = {"texto": contexto_raw}
        elif isinstance(contexto_raw, dict):
            contexto_dict = contexto_raw
        else:
            return (
                jsonify({"erro": "'contexto' deve ser string ou objeto JSON."}),
                400,
            )

        # ---- chama service ----
        resultado = avaliar_criterios(contexto_dict)
        return jsonify(resultado), 500 if "erro" in resultado else 200

    except Exception as exc:
        return jsonify({"erro": str(exc)}), 500
        

def avaliar_empresa_controller():
    try:
        data = request.get_json(force=True) or {}
        print("Raw JSON recebido:", data, file=sys.stderr)

        
        payload = data.get("questionario", data)

        areas   = payload.get("areas")
        empresa = payload.get("empresa")

        if empresa is None or not isinstance(areas , list):
            return jsonify({"erro": "JSON deve conter chaves 'empresa' e 'areas'."}), 400

        # opcional: remova dados sensíveis antes de mandar à LLM
        empresa.pop("senha", None)

        resultado = avaliar_empresa(areas, empresa)
        status = 500 if "erro" in resultado else 200
        return jsonify(resultado), status

    except Exception as exc:
        return jsonify({"erro": str(exc)}), 500
    
    
    


