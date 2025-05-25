import psycopg2
import os
from dotenv import load_dotenv

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def connect():
    # return psycopg2.connect(
    #     host=DB_HOST,
    #     port=DB_PORT,
    #     dbname=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     client_encoding='UTF8',
    #     options='-c client_encoding=utf8'
    # )
    return psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
    )



def get_dados_empresa_formatado(company_id: int) -> dict:
    conn = None
    cur = None
    try:
        conn = connect()
        cur = conn.cursor()

        query = """
        SELECT 
            temas.nome AS tema,
            topicos.nome AS topico,
            itens.nome AS item,
            respostas.resposta,
            empresas.setor,
            empresas.contexto_adicional
        FROM respostas
        JOIN temas ON respostas.tema_id = temas.tema_id
        JOIN topicos ON respostas.topico_id = topicos.topico_id AND topicos.tema_id_pertencente = temas.tema_id
        JOIN itens ON respostas.item_id = itens.item_id AND itens.topico_id_pertencente = topicos.topico_id
        JOIN empresas ON empresas.id = respostas.empresa_id
        WHERE respostas.empresa_id = %s
        """

        cur.execute(query, (company_id,))
        rows = cur.fetchall()

        if not rows:
            return None

        estrutura = {}
        setor = None
        contexto = None

        for idx, row in enumerate(rows):
            try:
                tema, topico, item, resposta, setor, contexto = row
                estrutura.setdefault(tema, {})
                estrutura[tema].setdefault(topico, {})
                estrutura[tema][topico][item] = resposta
            except Exception as parse_err:
                raise Exception(f"Erro ao processar linha {idx + 1}: {parse_err}")

        return {
            "setor": setor,
            "contexto_adicional": contexto,
            "respostas": estrutura
        }

    except Exception as e:
        raise Exception(f"Erro ao buscar dados da empresa: {str(e)}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
