"""
01_rag_artesanal.py — RAG do zero, sem framework.

Objetivo pedagogico: mostrar que RAG nao tem magica. Sao cinco passos:
  1. Ler o corpus e fatiar em chunks.
  2. Transformar cada chunk num vetor (embedding).
  3. Transformar a pergunta no mesmo espaco vetorial.
  4. Achar os chunks mais parecidos por similaridade de cosseno (numpy puro).
  5. Colar esses chunks no prompt e pedir a resposta ao LLM.

Os embeddings usam sentence-transformers LOCAL (roda em CPU, sem chave de API),
para que qualquer aluno reproduza a parte de recuperacao sem custo. So a geracao
final (passo 5) usa o Gemini; se nao houver chave, o script imprime o prompt
aumentado e encerra, o que ja demonstra o conceito.
"""

import os
import glob
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# ----------------------------------------------------------------------
# Passo 1 — Ler o corpus e fatiar em chunks
# ----------------------------------------------------------------------
def carregar_chunks(pasta_corpus, tamanho=90, sobreposicao=20):
    """Le todos os .md da pasta e fatia por palavras, com sobreposicao."""
    chunks = []
    for caminho in sorted(glob.glob(os.path.join(pasta_corpus, "*.md"))):
        with open(caminho, encoding="utf-8") as f:
            palavras = f.read().split()
        i = 0
        while i < len(palavras):
            trecho = " ".join(palavras[i:i + tamanho])
            chunks.append({"texto": trecho, "fonte": os.path.basename(caminho)})
            i += tamanho - sobreposicao
    return chunks


# ----------------------------------------------------------------------
# Passo 4 (nucleo) — similaridade de cosseno em numpy puro
# ----------------------------------------------------------------------
def cosseno(v, matriz):
    """Similaridade de cosseno entre um vetor v e cada linha de uma matriz."""
    v_norm = v / np.linalg.norm(v)
    m_norm = matriz / np.linalg.norm(matriz, axis=1, keepdims=True)
    return m_norm @ v_norm


def buscar(pergunta, chunks, embeddings, modelo, k=3):
    """Retorna os k chunks mais similares a pergunta."""
    q = modelo.encode([pergunta])[0]
    sims = cosseno(q, embeddings)
    indices = np.argsort(sims)[::-1][:k]
    return [(chunks[i], float(sims[i])) for i in indices]


# ----------------------------------------------------------------------
# Passo 5 — montar prompt aumentado e chamar o LLM
# ----------------------------------------------------------------------
def montar_prompt(pergunta, recuperados):
    contexto = "\n\n".join(
        f"[Trecho {n+1} — fonte: {c['fonte']}]\n{c['texto']}"
        for n, (c, _) in enumerate(recuperados)
    )
    return (
        "Voce e um assistente da disciplina de Sistemas Baseados em Conhecimento.\n"
        "Responda a pergunta usando SOMENTE os trechos de contexto abaixo.\n"
        "Se a resposta nao estiver nos trechos, diga que nao sabe.\n"
        "Sempre cite a fonte entre parenteses.\n\n"
        f"CONTEXTO:\n{contexto}\n\n"
        f"PERGUNTA: {pergunta}\n\nRESPOSTA:"
    )


def gerar_com_gemini(prompt):
    """Chama o Gemini se houver chave; caso contrario devolve None."""
    if not os.getenv("GEMINI_API_KEY"):
        return None
    from google import genai
    cliente = genai.Client()
    resp = cliente.models.generate_content(
        model="gemini-3.5-flash-lite", contents=prompt
    )
    return resp.text


# ----------------------------------------------------------------------
# Fluxo principal
# ----------------------------------------------------------------------
def main():
    pasta = os.path.join(os.path.dirname(__file__), "corpus")

    print("Passo 1: carregando e fatiando o corpus...")
    chunks = carregar_chunks(pasta)
    print(f"  {len(chunks)} chunks criados.\n")

    print("Passo 2: gerando embeddings (modelo local, pode baixar na 1a vez)...")
    modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = modelo.encode([c["texto"] for c in chunks])
    print(f"  matriz de embeddings: {embeddings.shape}\n")

    perguntas = [
        "Qual o prazo de entrega do Mini-Projeto 3?",
        "Quantas triplas no minimo a ontologia do MP3 precisa ter?",
        "Quantos alunos tem a turma e em que dia sao as aulas?",
    ]

    for pergunta in perguntas:
        print("=" * 70)
        print("PERGUNTA:", pergunta)
        recuperados = buscar(pergunta, chunks, embeddings, modelo, k=3)
        print("\nChunks recuperados (Passos 3 e 4):")
        for c, s in recuperados:
            print(f"  sim={s:.3f}  [{c['fonte']}]  {c['texto'][:70]}...")

        prompt = montar_prompt(pergunta, recuperados)
        resposta = gerar_com_gemini(prompt)
        print("\nRESPOSTA (Passo 5):")
        if resposta:
            print(" ", resposta.strip())
        else:
            print("  [sem GEMINI_API_KEY: exibindo o prompt aumentado]")
            print("  " + prompt[:300].replace("\n", "\n  ") + "...")
        print()


if __name__ == "__main__":
    main()
