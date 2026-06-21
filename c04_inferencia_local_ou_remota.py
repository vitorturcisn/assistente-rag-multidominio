# =====================================================================
# MÓDULO 4: ANÁLISE ARQUITETURAL E JUSTIFICATIVA DE PROCESSAMENTO HÍBRIDO
# =====================================================================

justificativa_arquitetura = """
=== ANALISE COMPARATIVA DE EXECUÇÃO (LOCAL VS REMOTA) ===

1. GERAÇÃO DE EMBEDDINGS (PROCESSAMENTO LOCAL):
- Modelo adotado: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (Hugging Face).
- Justificativa: Executar a vetorização localmente na CPU/GPU do host garante custo zero de tokens para a fase de indexação e busca. Além disso, protege a privacidade de dados sensíveis corporativos, visto que os textos brutos do acervo nunca deixam a infraestrutura para fins de busca por proximidade.

2. INFERÊNCIA DO LARGE LANGUAGE MODEL (PROCESSAMENTO REMOTO):
- Modelo adotado: Llama-3.1-8b-instant (via API remota Groq).
- Justificativa: Modelos de linguagem complexos de bilhões de parâmetros demandam alta capacidade de hardware (VRAM dedicada) indisponível na maioria das máquinas locais comuns. A API da Groq resolve esse gargalo utilizando LPUs (Language Processing Units), reduzindo a latência para milissegundos e fornecendo respostas factuais em tempo real com consumo zero de hardware local.
"""

if __name__ == "__main__":
    print(justificativa_arquitetura)