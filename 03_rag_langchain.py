"""
03_rag_langchain.py — consulta RAG com LangChain + Chroma + Gemini.

Estagio ONLINE do RAG. Carrega o indice Chroma criado pelo 02, recupera os k
chunks mais relevantes para a pergunta, monta o prompt aumentado e pede a
resposta ao Gemini. Exibe SEMPRE os chunks recuperados e suas fontes, para
tornar a recuperacao transparente (o ponto de explicabilidade da aula).

Rode 02_indexar_chroma.py antes deste script.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

PASTA_DB = os.path.join(os.path.dirname(__file__), "chroma_db")

PROMPT = ChatPromptTemplate.from_template(
    "Voce e um assistente da disciplina de Sistemas Baseados em Conhecimento.\n"
    "Responda a pergunta usando SOMENTE o contexto abaixo. Se a resposta nao\n"
    "estiver no contexto, diga que nao sabe. Cite a fonte entre parenteses.\n\n"
    "CONTEXTO:\n{contexto}\n\nPERGUNTA: {pergunta}\n\nRESPOSTA:"
)


def formatar(docs):
    return "\n\n".join(
        f"[fonte: {os.path.basename(d.metadata.get('source', '?'))}]\n{d.page_content}"
        for d in docs
    )


def main():
    if not os.getenv("GEMINI_API_KEY"):
        raise SystemExit("Defina GEMINI_API_KEY (veja .env.example).")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vs = Chroma(
        collection_name="sbc_notas",
        embedding_function=embeddings,
        persist_directory=PASTA_DB,
    )
    retriever = vs.as_retriever(search_kwargs={"k": 3})
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    perguntas = [
        "Qual o prazo de entrega do Mini-Projeto 3?",
        "Quais os requisitos minimos de triplas e classes da ontologia do MP3?",
        "O que o Mini-Projeto 1 exige em termos de regras?",
    ]

    for pergunta in perguntas:
        print("=" * 70)
        print("PERGUNTA:", pergunta)

        docs = retriever.invoke(pergunta)
        print("\nChunks recuperados:")
        for d in docs:
            fonte = os.path.basename(d.metadata.get("source", "?"))
            print(f"  [{fonte}] {d.page_content[:70].strip()}...")

        mensagem = PROMPT.format(contexto=formatar(docs), pergunta=pergunta)
        resposta = llm.invoke(mensagem)
        print("\nRESPOSTA:", resposta.content.strip(), "\n")


if __name__ == "__main__":
    main()
