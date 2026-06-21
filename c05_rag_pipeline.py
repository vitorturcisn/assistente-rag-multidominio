# =====================================================================
# MÓDULO 5: PIPELINE INTEGRAL DE RETRIEVAL-AUGMENTED GENERATION (RAG) COM INTERFACE GRÁFICA
# =====================================================================
import os
import warnings
import gradio as gr
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Importação dos módulos anteriores do projeto
from c01_modelos_llm import llm
from c03_embeddings_busca import inicializar_banco_vetorial

warnings.filterwarnings('ignore')

print("Inicializando componentes do pipeline RAG...")
vector_store = inicializar_banco_vetorial()

# Prompt de Contenção Estrita: Mitigação sistêmica de alucinações (Ponto 5 do edital)
diretriz_rag = (
    "Você é o 'Oráculo Editorial', um assistente de checagem de fatos jornalísticos.\n"
    "Responda à questão levantada baseando-se estritamente no contexto fornecido pelas notícias.\n"
    "Se o fragmento não possuir os fatos, declare obrigatoriamente:\n"
    "'Não há informações suficientes no acervo indexado para responder a esta consulta.'\n\n"
    "Contexto recuperado:\n{context}"
)

prompt_rag = PromptTemplate(
    template="SISTEMA:\n" + diretriz_rag + "\n\nPERGUNTA DO USUÁRIO:\n{input}\n\nRESPOSTA:", 
    input_variables=["context", "input"]
)

def formatar_documentos(docs):
    """Junta o conteúdo das notícias recuperadas em um único bloco de texto."""
    return "\n\n".join(doc.page_content for doc in docs)

# Configura o recuperador do ChromaDB para pegar as 3 notícias mais relevantes
recuperador = vector_store.as_retriever(search_kwargs={"k": 3})

# PIPELINE MODERNIZADO (LCEL): Constrói o fluxo de dados sem depender de 'langchain.chains'
pipeline_rag_final = (
    {
        "context": recuperador | formatar_documentos, 
        "input": RunnablePassthrough()
    }
    | prompt_rag 
    | llm 
    | StrOutputParser()
)

def processar_consulta(mensagem, historico=None):
    """Intermedeia o tráfego entre a UI de chat e a execução da cadeia RAG."""
    # Invoca o pipeline diretamente passando a pergunta do usuário
    resposta = pipeline_rag_final.invoke(mensagem) 
    return resposta

# Interface do Usuário Corporativa e Limpa (Compatível com Gradio v5/v6)
interface_usuario = gr.ChatInterface(
    fn=processar_consulta,
    title="Oráculo Editorial - Arquitetura RAG Multidomínio",
    description="Interface de busca semântica fundamentada sobre o acervo de artigos de mídia do Kaggle."
)

if __name__ == "__main__":
    print("Iniciando a aplicação web do Chatbot...")
    # Lança a interface localmente e gera link de compartilhamento externo
    interface_usuario.launch(share=True, debug=True)