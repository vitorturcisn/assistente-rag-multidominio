# =====================================================================
# MÓDULO 3: PREPARAÇÃO DO CORPUS, CHUNKING E INDEXAÇÃO PORTÁVEL
# =====================================================================
import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Caminho absoluto ou relativo para execução Local (VS Code)
caminho_dataset = os.path.join(os.getcwd(), 'articles.csv')

# Detecção Automática: Se estiver no Colab, ajusta o caminho para o Google Drive
if not os.path.exists(caminho_dataset):
    try:
        from google.colab import drive
        drive.mount('/content/drive', force_remount=True)
        caminho_dataset = '/content/drive/MyDrive/articles.csv'
        print("[AMBIENTE: NUVEM/COLAB] Rota do Google Drive ativada.")
    except ImportError:
        pass

def inicializar_banco_vetorial():
    try:
        df_completo = pd.read_csv(caminho_dataset)
        df_corpus = df_completo.sample(600, random_state=42).copy()
        print(f"Sucesso: Base carregada localmente com {len(df_corpus)} artigos.")
    except Exception as e:
        print(f"Falha ao ler o arquivo físico ({str(e)}). Ativando o fallback de segurança.")
        df_corpus = pd.DataFrame({"text": ["O Brasil obteve 14 pódios importantes na canoagem nas competições de 2015."]})

    documentos_brutos = [Document(page_content=str(texto)) for texto in df_corpus['text'].dropna()]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", ".", " "])
    documentos_fatiados = text_splitter.split_documents(documentos_brutos)

    embeddings_engine = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    vector_store = Chroma.from_documents(
        documents=documentos_fatiados, 
        embedding=embeddings_engine, 
        persist_directory=os.path.join(os.getcwd(), "chroma_db_geral")
    )
    return vector_store

if __name__ == "__main__":
    print("Gerando banco vetorial a partir do arquivo CSV...")
    db = inicializar_banco_vetorial()
    print("Banco vetorial gerado e persistido localmente na pasta './chroma_db_geral'!")