# 🤖 Oráculo Editorial: Arquitetura RAG Multidomínio

Este projeto consolida um pipeline corporativo completo de Geração Aumentada por Recuperação (RAG) utilizando o modelo Llama-3.1 (via Groq API), Embeddings locais do Hugging Face e banco vetorial ChromaDB, com interface de usuário assistiva em Gradio. O sistema adota uma arquitetura portável, funcionando tanto localmente (VS Code) quanto em nuvem (Google Colab).

## 🚀 Instalação e Requisitos
Certifique-se de utilizar o Python 3.10+ em sua máquina local. Instale todas as dependências do ecossistema executando o comando abaixo no terminal do VS Code:

pip install -r requirements.txt

## 🔑 Configuração de Credenciais e Segurança (Ponto 4 do Edital)
A autenticação do sistema foi simplificada para permitir a execução direta em sistemas locais, mitigando erros de leitura de variáveis de ambiente no Windows:

### Injeção Direta do Token (VS Code)
1. Abra o arquivo de código fonte `c01_modelos_llm.py`.
2. Localize a linha de definição da chave de API da Groq:
   
   os.environ["GROQ_API_KEY"] = "gsk_..."
   
3. Caso queira realizar a auditoria ou testes com uma credencial própria, basta substituir a string de texto contida entre as aspas duplas pelo seu token pessoal gerado no console da Groq.

## 🗂️ Ingestão do Dataset (Kaggle Data)
- **Local (VS Code):** Posicione o arquivo físico `articles.csv` extraído do Kaggle diretamente na pasta raiz do projeto. O script realizará a leitura dinamicamente via caminho relativo.
- **Nuvem (Colab):** Caso o arquivo local não seja detectado na raiz do diretório, o script acionará automaticamente um fallback lógico para montagem estruturada do Google Drive buscando o caminho padrão `/content/drive/MyDrive/articles.csv`.

## ⚙️ Arquitetura do Pipeline Técnico
1. **Amostragem:** Realiza um sorteio estatístico aleatório reproduzível (`random_state=42`) de 600 artigos gerais para balanceamento de memória computacional (evitando estouros de RAM por processamento em CPU).
2. **Segmentação (Chunking):** Fatiamento realizado via `RecursiveCharacterTextSplitter` com tamanho de bloco em 1000 caracteres e sobreposição (overlap) de 150 caracteres para preservar a integridade contextual.
3. **Vetorização (Embeddings):** Processamento local através do modelo multilíngue `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
4. **Contenção de Alucinações:** Injeção de uma diretriz estrita no System Prompt para que o Llama-3.1 atue com base factual restrita, emitindo uma negativa padrão caso as evidências não constem no acervo recuperado.

## 🕹️ Como Executar o Projeto Localmente
Para inicializar o pipeline RAG unificado, carregar o banco vetorial e levantar a interface gráfica de usuário do Chatbot, execute o script mestre diretamente através do terminal do VS Code utilizando o executável correto do Python instalado na máquina:

C:\Users\vitor\AppData\Local\Python\pythoncore-3.14-64\python.exe c05_rag_pipeline.py

O sistema processará o acervo e disponibilizará o link do servidor local de loopback (`http://localhost:7860`) para uso imediato no navegador, juntamente com um link público temporário gerado de forma segura pelo túnel do Gradio para fins de avaliação e homologação externa.