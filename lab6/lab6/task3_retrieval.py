"""Task 3: evaluate every chunking x retrieval configuration.

Run: python task3_retrieval.py [--modes bm25 tfidf embedding]
Writes retrieval_log.csv and selected_config.json (best config on DEV only).

A query counts as a hit@k when one of the top-k chunks is from the gold document
and its character span overlaps the gold evidence span. Unsupported queries
(doc = null) are correct only when the system returns no candidates.
"""
import argparse
import csv
import json
import time

from lab6_search import Retriever
from task2_chunks import make_chunks

STRATEGIES = ["doc", "sentence", "0", "10"]
REPEATS = 5


def overlaps(chunk, docs, q):
    text = docs[q["doc"]]
    s = text.find(q["evidence"])
    return chunk["doc"] == q["doc"] and chunk["start"] < s + len(q["evidence"]) and chunk["end"] > s


def evaluate(engine, docs, queries):
    sup = [q for q in queries if q["doc"]]
    uns = [q for q in queries if not q["doc"]]
    h1 = h3 = 0
    top1_chars = []
    for q in sup:
        hits = engine.search(q["query"])
        if hits and overlaps(hits[0][0], docs, q):
            h1 += 1
        if any(overlaps(c, docs, q) for c, _ in hits):
            h3 += 1
        if hits:
            top1_chars.append(len(hits[0][0]["text"]))
    abst = sum(1 for q in uns if not engine.search(q["query"]))
    t0 = time.perf_counter()
    for _ in range(REPEATS):
        for q in queries:
            engine.search(q["query"])
    ms = (time.perf_counter() - t0) * 1000 / (REPEATS * max(1, len(queries)))
    return dict(n_supported=len(sup), hit1=h1 / max(1, len(sup)), hit3=h3 / max(1, len(sup)),
                n_unsupported=len(uns), abstain=(abst / len(uns)) if uns else "",
                avg_top1_chars=round(sum(top1_chars) / len(top1_chars)) if top1_chars else "",
                ms_per_query=round(ms, 3))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--modes", nargs="+", default=["bm25", "tfidf", "embedding"])
    args = ap.parse_args()
    docs = json.load(open("corpus.json", encoding="utf-8"))
    queries = json.load(open("queries.json", encoding="utf-8"))
    rows = []
    for mode in args.modes:
        for strat in STRATEGIES:
            try:
                engine = Retriever(make_chunks(docs, strat), mode)
            except Exception as err:
                print("SKIPPED", mode, strat, "->", err)
                continue
            for split in ("dev", "test"):
                subset = [q for q in queries if q["split"] == split]
                rows.append(dict(mode=mode, strategy=strat, split=split,
                                 **evaluate(engine, docs, subset)))
    fields = ["mode", "strategy", "split", "n_supported", "hit1", "hit3", "n_unsupported",
              "abstain", "avg_top1_chars", "ms_per_query"]
    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
    dev = [r for r in rows if r["split"] == "dev"]
    # choose on DEV only: best hit@1, then hit@3, then shortest evidence passage
    best = max(dev, key=lambda r: (r["hit1"], r["hit3"], -(r["avg_top1_chars"] or 10**9)))
    json.dump({"mode": best["mode"], "strategy": best["strategy"]}, open("selected_config.json", "w"))
    print("\nSelected on development data:", best["mode"], best["strategy"])
