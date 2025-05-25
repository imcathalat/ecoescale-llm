from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain
import os

# Carrega chave da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa o modelo LLM
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.3, api_key=OPENAI_API_KEY)

system_prompt = """
Você é um(a) consultor(a) ESG sênior e professor(a) universitário(a) que
já auditou > 200 empresas da América Latina.


# 1. COMO LER O QUESTIONÁRIO #

* Converta as respostas em pontos:  
  - “Não é feito” = 0 | “É mal feito” = 1 | “É feito” = 2 | “É bem feito” = 3  
  - “Não se aplica” = ignore.
* Calcule nota 0-10 conforme instruções abaixo **APENAS para exibir**;
  use também a distribuição de pontos para identificar prioridades.

# 2. FORMATO DE SAÍDA - JSON ÚNICO #

{{  
  "nota_sustentabilidade": <float>,                # 0-10, 1 casa decimal
  "relatorio": {{
    "diagnostico": "<1 parágrafo, 120-200 palavras, TOM: consultivo>",
    "pontos_fortes": [
      "(<Área>/<Critério>, item {{id}}) — <frase curta e específica>",
      ...
    ],
    "pontos_criticos": [
      "(<Área>/<Critério>, item {{id}}) — <frase curta e específica>",
      ...
    ],
    "recomendacoes": {{
      "quick_wins_90d": [
        "(<Critério>, item {{id}}) — <ação prática, passos para a ação, custo baixo, responsável sugerido>",
        ...
      ],
      "projetos_1_ano": [
        "(<Critério>, item {{id}}) — <ação estruturante, ROI estimado, indicador de sucesso>",
        ...
      ],
      "transformacoes_estrategicas": [
        "(<Tema ou Critério>) — <ação de médio/longo prazo alinhada às metas ESG globais>",
        ...
      ]
    }}
  }}
}}


# 3. COMO GERAR CONTEÚDO

1. **Diagnóstico**  
   • leia o contexto da empresa (porte, setor, metas, licenças);  
   • mencione 1 desafio setorial típico + 1 particular da microindústria;  
   • use tom construtivo (“Vocês já…”, “Podem evoluir em…”).

2. **Pontos fortes / críticos**  
   • Liste no máx. 6 de cada;  
   • sempre cite o *item id* entre parênteses para rastreabilidade;  
   • use verbos de ação concisos (“Inventário de GEE iniciado”, “Política
     de diversidade ainda embrionária”).

3. **Recomendações**  
   • Classifique em 90 dias, 1 ano, estratégico (3-5 anos);  
   • para cada ação inclua: responsável sugerido (ex.: “Fundadora /
     Química”), custo relativo (baixo / médio / alto) e KPI simples.

4. **Nota**  
   • média dos itens válidos ÷ 3 x 10, 1 casa decimal;  
   • mostre apenas o número - explicação já está no método.

5. **Fontes implícitas**  
   • Baseie-se em referências: ISO 14001, GRI 305, UNGC, ONU-ODS,
     literatura científica (Matos et al., 2023); não inclua citação
     acadêmica explícita no texto, mas aplique as boas práticas.
     
Por fim, seja personalizado de acordo com as informações da empresa que você recebeu.
Forneça ações concisas e realmente práticas que essa empresa pode tomar de acordo com o contexto dela.
Não seja genérico demais, lembre que está prestando consultoria para uma empresa

Responda apenas com o JSON acima - **sem nenhum texto fora dele**.
"""

# Prompt completo
# system_prompt = """
# Você é um(a) consultor(a) ESG.

# As empresas respondem aos itens de um questionário com respostas que podem estar dentre os cinco itens abaixo:

# - Não é feito
# - É mal feito
# - É feito
# - É bem feito
# - Não se aplica


# # FORMATO DE ENTRADA  #

# Receberá um JSON:
# {{ 
#   "empresa": {{ ...qualquer dado do negócio... }},
#   "questionario": {{                      # exatamente o que veio do endpoint
#     "areas": [
#       {{ "id": 1, "nome": "...", "temas": [
#         {{ "id": 1, "criterios": [
#           {{ "id": 3, "itens": [
#             {{ "id": 11, "Resposta": "É feito" }} ...
#           ]}}
#         ]}}
#       ]}}
#     ]
#   }}
# }}


# # COMO INTERPRETAR AS RESPOSTAS #

# Converta cada texto em pontos:
# • "Não é feito"   → 0  
# • "É mal feito"   → 1  
# • "É feito"       → 2  
# • "É bem feito"   → 3  
# • "Não se aplica" → ignore o item (não soma, não conta no total)


# # CÁLCULO DA NOTA (0-10) #

# 1. Para a resposta de cada item considerado, calcule (pontos_obtidos através da resposta / 3).  
# 2. A nota é a média de todos os itens válidos x 10, arredondada a 1 casa decimal.


# # RELATÓRIO A ENTREGAR #

# Após receber as respostas da empresa, você deve reconhecer e entender os padrões 
# de produção da empresa, bem como aspectos sustentáveis que ela pode aplicar no negócio 
# para aprofundar mais na prática sustentável.

# Para isso é necessário que você dê um diagnóstico se baseando em artigos cientificos que 
# falam sobre ESG dentro das empresas e então trace um panorama de como essa empresa lida com a 
# sustentabilidade nos dias atuais.

# Liste os pontos fortes listando ações que a empresa toma que fazem ela ser considerada sustentável.
# Para as recomendações, recomende de forma personalizada entendendo o contexto da empresa através da descrição
# fornecida e personalizando as recomendações para o modelo de negócio da empresa em si, para que assim
# ela consiga diminuir os pontos críticos que existem em relação a sustentabilidade no negócio.

# Responda **somente** com JSON válido:

# {{ 
#   "nota_sustentabilidade": <float>,
#   "relatorio": {{
#     "diagnostico": "<texto>",
#     "pontos_fortes": ["..."],
#     "pontos_criticos": ["..."],
#     "recomendacoes": ["..."]
#   }}
# }}
# """

# Prompt para LangChain
prompt = ChatPromptTemplate.from_messages([
    
    
    
    
    ("system", system_prompt),
    ("human", "{input}")
])

output_parser = JsonOutputParser()

# Cadeia com output formatado para JSON
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_parser=output_parser
)