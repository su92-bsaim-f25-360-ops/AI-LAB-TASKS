"""Task 3 interactive chatbot. Run: python document_chatbot.py

The splitter and retrieval mode come from selected_config.json, which
task3_retrieval.py writes after comparing configurations on the development
split. Candidates are never presented as verified answers.
"""
import json
from pathlib import Path

from lab6_search import Retriever
from task2_chunks import make_chunks

if __name__ == "__main__":
    with open("corpus.json", encoding="utf-8") as f:
        docs = json.load(f)
    cfg = {"strategy": "sentence", "mode": "embedding"}  # defaults if not evaluated yet
    if Path("selected_config.json").exists():
        cfg = json.load(open("selected_config.json"))
    engine = Retriever(make_chunks(docs, cfg["strategy"]), cfg["mode"])
    print(f"Evidence assistant ({cfg['mode']}, {cfg['strategy']} chunks). Type exit to stop.")
    while True:
        try:
            query = input("Question: ")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() == "exit":
            break
        hits = engine.search(query)
        if not hits:
            print("No candidate evidence; rephrase or contact a human.")
            continue
        print("Candidate evidence; relevance must be checked:")
        for number, (r, score) in enumerate(hits, 1):
            print(number, r["id"], f"{score:.3f}", "characters", r["start"], r["end"])
        chosen = input("Choose 1-3 to inspect; Enter if none apply: ")
        if not chosen.isdigit() or not 1 <= int(chosen) <= len(hits):
            print("No answer selected. Rephrase or contact a human.")
            continue
        r, score = hits[int(chosen) - 1]
        print("Retrieved passage:", r["text"])
        print("Source:", r["doc"], "characters", r["start"], r["end"])
