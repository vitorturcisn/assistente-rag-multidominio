# =====================================================================
# MÓDULO 1: CONFIGURAÇÃO DE SEGURANÇA E AUTENTICAÇÃO HÍBRIDA
# =====================================================================
import os
import warnings
warnings.filterwarnings('ignore')
from langchain_groq import ChatGroq

# Correção: A chave precisa estar entre aspas para o Python ler como texto (String)
os.environ["GROQ_API_KEY"] = "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"

print("[AMBIENTE: LOCAL/VS CODE] Chave de API configurada diretamente no script.")

# Instanciação estável do Large Language Model (Llama 3.1)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

if __name__ == "__main__":
    print("Testando inferência base do modelo...")
    teste_conectividade = llm.invoke("Confirme a conectividade respondendo apenas: Ativo.")
    print(f"Status da API Groq: {teste_conectividade.content.strip()}")