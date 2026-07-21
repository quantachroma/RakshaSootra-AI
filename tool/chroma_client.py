"""
Owner - Person 2 - Priyanshi Saini
chroma_client.py — Shared ChromaDB client
RakshaSootra AI

Provides a single persistent ChromaDB client + collection getter so every
agent that needs RAG retrieval (currently Scam Script Checker) talks to
the same on-disk vector store.

Embeddings are generated with sentence-transformers (all-MiniLM-L6-v2),
which is small, fast, and needs no API key/network call at query time.
"""

import os

import chromadb
from chromadb.utils import embedding_functions

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

CHROMA_DB_PATH = os.path.join(os.getcwd(), "data", "chroma_store")

COLLECTION_NAME = "advisories"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

_client = None
_embedding_function = None


# ------------------------------------------------------------------
# Client / Embedding Function Singletons
# ------------------------------------------------------------------

def get_chroma_client():
    """
    Returns a persistent ChromaDB client. Data is stored on disk under
    data/chroma_store so the index survives across app restarts.
    """

    global _client

    if _client is None:
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)
        _client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    return _client


def get_embedding_function():
    """
    Returns a shared sentence-transformers embedding function so the
    model is only loaded into memory once per process.
    """

    global _embedding_function

    if _embedding_function is None:
        _embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=EMBEDDING_MODEL_NAME
            )
        )

    return _embedding_function


# ------------------------------------------------------------------
# Collection Getter
# ------------------------------------------------------------------

def get_advisory_collection():
    """
    Returns (creating if needed) the ChromaDB collection that stores
    chunked advisory/circular/case-study text.
    """

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )

    return collection