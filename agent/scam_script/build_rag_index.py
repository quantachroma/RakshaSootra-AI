"""
Owner - Person 2 - Priyanshi Saini
build_rag_index.py — One-off / re-runnable script to (re)build the
ChromaDB advisory index from data/advisories/.

Run:
    python3 -m agent.scam_script.build_rag_index

Re-run any time advisory .txt files are added, edited, or removed —
build_index() clears and re-inserts chunks, so it's always safe to rerun.
"""

from agent.scam_script.rag import build_index, retrieve_advisories


def main():

    print("Building ChromaDB advisory index...")

    total_chunks = build_index(reset=True)

    if total_chunks == 0:
        print("Index is empty — check data/advisories/ contains .txt files.")
        return

    # Quick sanity check: a basic retrieval query
    print("\nSanity check — retrieval for a digital arrest style script:")

    sample_query = (
        "This is officer Sharma from CBI. You are under digital arrest, "
        "do not disconnect the video call, pay to avoid arrest."
    )

    matches = retrieve_advisories(sample_query, top_k=3)

    if not matches:
        print("No matches found — check embeddings/threshold.")
        return

    for match in matches:
        print(f"  [{match['distance']}] {match['source']} — {match['topic']}")


if __name__ == "__main__":
    main()