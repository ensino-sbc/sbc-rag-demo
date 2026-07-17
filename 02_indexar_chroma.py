"""
02_indexar_chroma.py — indexacao do corpus com LangChain + Chroma.

Este script faz o estagio OFFLINE do RAG: le o corpus, fatia em chunks,
gera embeddings com o Gemini e persiste tudo num banco vetorial Chroma no
disco (pasta ./chroma_db). Roda uma vez; depois o 03 apenas consulta.

Requer GEMINI_API_KEY no ambiente (ou num arquivo .env). Veja o README para a
alternativa local com Ollama, sem custo.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

PASTA_CORPUS = os.path.join(os.path.dirname(__file__), "corpus")
PASTA_DB = os.path.join(os.path.dirname(__file__), "chroma_db")


def main():
    if not os.getenv("GEMINI_API_KEY"):
        raise SystemExit(
            "Defina GEMINI_API_KEY (veja .env.example) ou use a rota Ollama do README."
        )

    # 1. Carregar os documentos do corpus
    loader = DirectoryLoader(
        PASTA_CORPUS, glob="*.md",
        loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    print(f"Documentos carregados: {len(docs)}")

    # 2. Fatiar em chunks com sobreposicao
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"Chunks apos split: {len(chunks)}")

    # 3. Modelo de embeddings do Gemini
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # 4. Criar (ou sobrescrever) o Chroma persistente
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="sbc_notas",
        persist_directory=PASTA_DB,
    )
    print(f"Indice Chroma persistido em: {PASTA_DB}")
    print("Pronto. Agora rode: python 03_rag_langchain.py")


if __name__ == "__main__":
    main()
