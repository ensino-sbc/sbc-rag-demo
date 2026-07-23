"""
05_visualizar_embeddings.py — mapa 2D do corpus.

Projeta os embeddings dos chunks em 2D com PCA e salva uma figura. Serve para
 observar que chunks sobre o mesmo assunto ficam proximos no espaco
vetorial, caracter[istica que a busca por similaridade explora.

Usa sentence-transformers LOCAL (sem chave), para rodar em qualquer maquina.
"""

import os
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer

PASTA_CORPUS = os.path.join(os.path.dirname(__file__), "corpus")
SAIDA = os.path.join(os.path.dirname(__file__), "embeddings_2d.png")


def carregar_chunks(tamanho=90, sobreposicao=20):
    chunks = []
    for caminho in sorted(glob.glob(os.path.join(PASTA_CORPUS, "*.md"))):
        with open(caminho, encoding="utf-8") as f:
            palavras = f.read().split()
        i = 0
        while i < len(palavras):
            chunks.append({
                "texto": " ".join(palavras[i:i + tamanho]),
                "fonte": os.path.basename(caminho),
            })
            i += tamanho - sobreposicao
    return chunks


def main():
    chunks = carregar_chunks()
    modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    X = modelo.encode([c["texto"] for c in chunks])
    coords = PCA(n_components=2).fit_transform(X)

    fontes = sorted({c["fonte"] for c in chunks})
    cores = plt.cm.tab10(np.linspace(0, 1, len(fontes)))
    mapa = dict(zip(fontes, cores))

    plt.figure(figsize=(9, 6))
    for c, (x, y) in zip(chunks, coords):
        plt.scatter(x, y, color=mapa[c["fonte"]], s=60, alpha=0.8)
    for fonte, cor in mapa.items():
        plt.scatter([], [], color=cor, label=fonte)
    plt.legend(fontsize=8, loc="best")
    plt.title("Chunks do corpus projetados em 2D (PCA sobre os embeddings)")
    plt.xlabel("componente 1")
    plt.ylabel("componente 2")
    plt.tight_layout()
    plt.savefig(SAIDA, dpi=120)
    print("Figura salva em:", SAIDA)


if __name__ == "__main__":
    main()
