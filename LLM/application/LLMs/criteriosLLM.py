import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain

# ------------------------------------------------------------------
# 1. Modelo: baixa temperatura, pois a tarefa é determinística
# ------------------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.6,
    api_key=os.getenv("OPENAI_API_KEY")
)

# ------------------------------------------------------------------
# 2. Prompt do sistema
# ------------------------------------------------------------------
system_prompt = """
Você é um(a) consultor(a) ESG responsável por preparar um *workshop* de
priorização de critérios para uma empresa.

###########################
# DADOS DE ENTRADA (USER) #
###########################
Você receberá um ÚNICO JSON com:

{{ 
  "contexto": "<texto livre sobre a empresa>",
  "lista_criterios": [
    {{ "id": <int>, "nome": "<string>" }},
    ...
  ]
}}

O campo **contexto** pode conter:
• setor de atuação, modelo de negócio, porte, localização geográfica,
• metas declaradas (ex.: neutralidade de carbono até 2030),
• dores ou desafios (“alto consumo de água na produção”, “cadeia global complexa”),
• pressões externas (reguladores, investidores, clientes, sociedade),
• qualquer informação que ajude a entender a materialidade dos temas.

########################################
# SUA TAREFA - SIGA EXATAMENTE 4 PASSOS
########################################
1. **Analisar** o contexto e identificar os temas materiais
   (ambientais, sociais, governança) que mais impactam a empresa.

2. **Pontuar** cada critério da *lista_criterios* de 0 a 5
   - onde 0 = nada relacionado ao contexto e 5 = altamente crítico
   para o sucesso sustentável da empresa a curto ou médio prazo.

3. **Ordenar** os critérios por pontuação decrescente.

###################
# FORMATO DE SAÍDA
###################
Responda **somente** com um JSON válido:
Responda **somente** com um JSON válido:
{{ 
  "scores": [
    {{ "id": <int>, "score": <int 0‑5> }},
    ...
  ]
}}
"""

# ------------------------------------------------------------------
# 3. Monta prompt LangChain
# ------------------------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt.strip()),
    ("human", "{input}")
])

output_parser = JsonOutputParser()   # força saída JSON válida

# ------------------------------------------------------------------
# 4. Cadeia exportada
# ------------------------------------------------------------------
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_parser=output_parser
)
