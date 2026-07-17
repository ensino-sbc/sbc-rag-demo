# sbc-rag-demo — RAG do zero ao framework

Demonstração da Aula 8 da disciplina de Sistemas Baseados em Conhecimento (SBC),
Bloco 4 (Era Agêntica). O corpus é o próprio material da disciplina (documentos
de mini-projeto e informações do curso), escolhido de propósito: são datas e
regras que os LLMs não conhecem, então a falha do modelo sem RAG fica evidente.

A demo tem dois estágios:

1. **RAG artesanal** (`01_rag_artesanal.py`): o pipeline inteiro em ~100 linhas,
   sem framework, com a similaridade de cosseno feita à mão em numpy. Mostra que
   não há mágica.
2. **RAG com framework** (`02` a `04`): o mesmo pipeline com LangChain + Chroma,
   com o índice persistido em disco, e uma bateria comparativa com vs sem RAG que
   termina nas perguntas que o RAG vetorial erra (a ponte para GraphRAG).

## Estrutura

```
sbc-rag-demo/
├── corpus/                      # o material da disciplina (o "conhecimento")
├── 01_rag_artesanal.py          # RAG sem framework, cosseno em numpy
├── 02_indexar_chroma.py         # indexacao: loader -> split -> embed -> Chroma
├── 03_rag_langchain.py          # consulta: retriever -> prompt -> LLM (com fontes)
├── 04_com_vs_sem_rag.py         # bateria comparativa + perguntas que o RAG erra
├── 05_visualizar_embeddings.py  # projecao PCA 2D dos chunks (gera figura)
├── requirements.txt
└── .env.example
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # opcional
pip install -r requirements.txt
cp .env.example .env        # e preencha GEMINI_API_KEY
```

A chave gratuita do Gemini sai de https://aistudio.google.com/app/apikey.

Os scripts `01` e `05` usam embeddings locais (sentence-transformers) e rodam
**sem chave**. Os scripts `02`, `03` e `04` usam o Gemini para embeddings e
geração, e precisam da chave.

## Como rodar

```bash
# Estagio 1 — artesanal (sem chave para a recuperacao; geracao usa Gemini se houver chave)
python 01_rag_artesanal.py

# Estagio 2 — framework
python 02_indexar_chroma.py     # cria o indice Chroma em ./chroma_db (roda uma vez)
python 03_rag_langchain.py      # consulta e mostra os chunks recuperados
python 04_com_vs_sem_rag.py     # comparacao com vs sem RAG + perguntas dificeis

# Visualizacao (sem chave)
python 05_visualizar_embeddings.py
```

## Rota sem custo: Ollama local (alternativa ao Gemini)

Quem não quiser usar a API do Gemini pode rodar tudo localmente com o
[Ollama](https://ollama.com). Instale o Ollama e baixe os modelos:

```bash
ollama pull nomic-embed-text     # embeddings
ollama pull llama3.1             # geracao
pip install langchain-ollama
```

Depois, troque as duas classes do Gemini pelas do Ollama nos scripts `02`, `03`
e `04`:

```python
# no lugar de GoogleGenerativeAIEmbeddings(...)
from langchain_ollama import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# no lugar de ChatGoogleGenerativeAI(...)
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3.1", temperature=0)
```

O restante do pipeline é idêntico: a separação entre corpus, recuperação e
geração não depende de qual LLM está por trás.

## A ideia central

RAG é uma reedição moderna da arquitetura clássica de SBC: uma base de
conhecimento externa e explícita (o corpus indexado) separada do motor de
inferência (o LLM), com rastreabilidade das fontes. O conhecimento volta a ser
um artefato que se edita, versiona e audita. As perguntas que o RAG vetorial
erra, no `04`, são exatamente as que exigem raciocínio relacional sobre o corpus,
e é aí que entra o grafo, na próxima aula.
