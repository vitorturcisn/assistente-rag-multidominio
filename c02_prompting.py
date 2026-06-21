# =====================================================================
# MÓDULO 2: ENGENHARIA DE PROMPTS E EXTRAÇÃO ESTRUTURADA (JSON PARSING)
# =====================================================================
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from c01_modelos_llm import llm  # Reaproveita a instância configurada do Módulo 1

parser = JsonOutputParser()

template_diretriz = """Você é um Assistente Editorial Sênior.
Sua tarefa é analisar o TRECHO DA NOTÍCIA e responder à PERGUNTA DO USUÁRIO.

Regras de formatação:
- Responda EXCLUSIVAMENTE em formato JSON válido.
- O objeto deve conter estritamente 3 chaves: "resposta", "data_do_evento" e "confianca".

TRECHO DA NOTÍCIA: {contexto}
PERGUNTA DO USUÁRIO: {pergunta}
{instrucoes_formato}"""

prompt_diretriz = PromptTemplate(
    template=template_diretriz,
    input_variables=["contexto", "pergunta"],
    partial_variables={"instrucoes_formato": parser.get_format_instructions()}
)

# Pipeline de extração estruturada via pipe syntax (LCEL)
pipeline_estruturado = prompt_diretriz | llm | parser

if __name__ == "__main__":
    print("Testando geração controlada em formato JSON...")
    resultado_json = pipeline_estruturado.invoke({
        "contexto": "A transferência de Neymar para o futebol francês quebrou recordes em 2017.",
        "pergunta": "Em qual ano ocorreu a transferência e para onde ele foi?"
    })
    print(json.dumps(resultado_json, indent=4, ensure_ascii=False))