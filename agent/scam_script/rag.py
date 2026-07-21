"""
Owner - Person 2 - Priyanshi Saini
rag.py — ChromaDB RAG Layer for Scam Script Checker
RakshaSootra AI

Workflow:
Advisory .txt files (data/advisories/)
      |
      v
Chunking (chunk_text)
      |
      v
Embedding + Storage (build_index -> ChromaDB via sentence-transformers)
      |
      v
Retrieval (retrieve_advisories) -> queried before the LLM check in
scam_script_agent.py, so the LLM/verdict can cite a matched advisory.
"""

import os
import re

from tool.chroma_client import get_advisory_collection

ADVISORY_DIR = os.path.join(os.getcwd(), "data", "rawFolder")

# A retrieved chunk is only treated as a real "match" (citable) if its
# distance is below this threshold. Cosine distance: 0 = identical,
# 2 = opposite. Empirically tuned for all-MiniLM-L6-v2 short-text search.
RELEVANCE_DISTANCE_THRESHOLD = 0.75


# ==========================================================
# Chunking
# ==========================================================

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> list:
    """
    Splits text into overlapping word-based chunks.

    A moderate chunk size keeps each embedded piece topically coherent
    (roughly one advisory "pattern" per chunk) while overlap avoids
    cutting a key sentence in half at a chunk boundary.
    """

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    words = text.split(" ")

    if len(words) <= chunk_size:
        return [text]

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


# ==========================================================
# Load Advisory Files
# ==========================================================

def _load_advisory_files() -> list:
    """
    Reads every .txt file in data/advisories/.

    Returns a list of dicts: {"filename": ..., "topic": ..., "text": ...}
    """

    documents = []

    if not os.path.isdir(ADVISORY_DIR):
        return documents

    for filename in sorted(os.listdir(ADVISORY_DIR)):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(ADVISORY_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        topic_match = re.search(r"TOPIC:\s*(.+)", text)

        topic = topic_match.group(1).strip() if topic_match else filename

        documents.append({
            "filename": filename,
            "topic": topic,
            "text": text,
        })

    return documents


# ==========================================================
# Build / Refresh Index
# ==========================================================

def build_index(reset: bool = True) -> int:
    """
    Chunks every advisory file and stores embeddings in ChromaDB.

    Args:
        reset: if True, clears any existing chunks for a file before
               re-inserting (keeps the index idempotent across reruns).

    Returns:
        Total number of chunks stored.
    """

    collection = get_advisory_collection()

    documents = _load_advisory_files()

    if not documents:
        print("No advisory files found in data/advisories/.")
        return 0

    if reset:
        existing = collection.get()
        if existing and existing.get("ids"):
            collection.delete(ids=existing["ids"])

    total_chunks = 0

    for doc in documents:

        chunks = chunk_text(doc["text"])

        ids = []
        metadatas = []

        for i, chunk in enumerate(chunks):

            chunk_id = f"{doc['filename']}::chunk_{i}"

            ids.append(chunk_id)

            metadatas.append({
                "source": doc["filename"],
                "topic": doc["topic"],
                "chunk_index": i,
            })

        if not chunks:
            continue

        collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas,
        )

        total_chunks += len(chunks)

    print(f"Indexed {len(documents)} advisory files into {total_chunks} chunks.")

    return total_chunks


# ==========================================================
# Retrieval
# ==========================================================

def retrieve_advisories(query_text: str, top_k: int = 3) -> list:
    """
    Retrieves the top_k most relevant advisory chunks for a scam script.

    Returns a list of dicts (best match first):
        {
            "text": "...",
            "source": "digital_arrest.txt",
            "topic": "Digital Arrest Scams",
            "distance": 0.31
        }

    Chunks whose distance exceeds RELEVANCE_DISTANCE_THRESHOLD are
    dropped, so a genuinely unrelated script returns an empty list
    rather than a forced, misleading citation.
    """

    if not query_text or not query_text.strip():
        return []

    collection = get_advisory_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query_text],
        n_results=min(top_k, collection.count()),
    )

    matches = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, distance in zip(documents, metadatas, distances):

        if distance > RELEVANCE_DISTANCE_THRESHOLD:
            continue

        matches.append({
            "text": doc,
            "source": meta.get("source", ""),
            "topic": meta.get("topic", ""),
            "distance": round(distance, 4),
        })

    return matches