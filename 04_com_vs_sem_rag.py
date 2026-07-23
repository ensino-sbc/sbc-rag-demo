"""
04_com_vs_sem_rag.py — a bateria comparativa da aula.

Faz a MESMA pergunta ao Gemini de dois jeitos:
  (A) SEM RAG: pergunta crua ao modelo, que so tem conhecimento parametrico.
  (B) COM RAG: pergunta aumentada com os chunks recuperados do corpus.

O bloco final contem perguntas que o RAG vetorial simples ERRA de proposito
(multi-hop, agregacao, visao global do corpus)..
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma

load_dotenv()
PASTA_DB = os.path.join(os.path.dirname(__file__), "chroma_db")


def _extrair_texto(content):
    if isinstance(content, str):
        return content.strip()
    return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content).strip()


def responder_sem_rag(llm, pergunta):
    return _extrair_texto(llm.invoke(pergunta).content)


def responder_com_rag(llm, retriever, pergunta):
    docs = retriever.invoke(pergunta)
    contexto = "\n\n".join(d.page_content for d in docs)
    prompt = (
        "Responda usando SOMENTE o contexto. Se nao estiver nele, diga que nao sabe.\n\n"
        f"CONTEXTO:\n{contexto}\n\nPERGUNTA: {pergunta}\n\nRESPOSTA:"
    )
    fontes = {os.path.basename(d.metadata.get("source", "?")) for d in docs}
    return _extrair_texto(llm.invoke(prompt).content), fontes


def main():
    if not os.getenv("GEMINI_API_KEY"):
        raise SystemExit("Defina GEMINI_API_KEY (veja .env.example).")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vs = Chroma(collection_name="sbc_notas", embedding_function=embeddings,
                persist_directory=PASTA_DB)
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

    # Perguntas que o RAG resolve bem: factuais e localizadas.
    faceis = [
        "Qual o prazo de entrega do Mini-Projeto 3?",
        "Quantas triplas no minimo a ontologia do MP3 precisa ter?",
    ]

    # Perguntas onde o RAG vetorial simples tropeca: exigem juntar varios
    # trechos, agregar ou ter visao global. Ponte para GraphRAG.
    dificeis = [
        "Quantos dias separam a entrega do MP1 da entrega do MP2?",
        "Somando todos os pesos, quanto vale a avaliacao que NAO e prova nem "
        "projeto final?",
        "Quais sao os temas principais de toda a disciplina?",
    ]

    print("#" * 70)
    print("# PARTE 1 — perguntas factuais localizadas (RAG resolve bem)")
    print("#" * 70)
    for p in faceis:
        print("\nPERGUNTA:", p)
        print("  SEM RAG :", responder_sem_rag(llm, p)[:180])
        resp, fontes = responder_com_rag(llm, retriever, p)
        print("  COM RAG :", resp[:180])
        print("  fontes  :", ", ".join(sorted(fontes)))

    print("\n" + "#" * 70)
    print("# PARTE 2 — perguntas multi-hop / globais (RAG vetorial tropeca)")
    print("#          -> motivacao para a proxima aula, GraphRAG")
    print("#" * 70)
    for p in dificeis:
        print("\nPERGUNTA:", p)
        resp, fontes = responder_com_rag(llm, retriever, p)
        print("  COM RAG :", resp[:220])
        print("  fontes  :", ", ".join(sorted(fontes)))


if __name__ == "__main__":
    main()
