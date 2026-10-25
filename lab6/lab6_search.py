"""Retriever used by task3_retrieval.py and document_chatbot.py.

Retriever(chunks, mode) with mode in {"bm25", "tfidf", "embedding"}.
search(query) -> list of (chunk_record, score), best first, at most top_k.
Returns [] for an empty query or when no chunk reaches the threshold, so the
caller can show a fallback instead of presenting weak evidence.
"""
import math
import re
from collections import Counter

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
STOP = set("a an the is are was were be to of in on for and or do does did i my me we you it "
           "can how what who where when which that this with as at by from should".split())
DEFAULT_THRESHOLD = {"bm25": 0.0, "tfidf": 0.05, "embedding": 0.30}


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9']+", text.lower()) if t not in STOP]


class Retriever:
    def __init__(self, chunks, mode="bm25", top_k=3, threshold=None):
        self.chunks, self.mode, self.top_k = chunks, mode, top_k
        self.threshold = DEFAULT_THRESHOLD[mode] if threshold is None else threshold
        if mode in ("bm25", "tfidf"):
            self.toks = [tokens(c["text"]) for c in chunks]
            n = len(chunks)
            df = Counter(t for ts in self.toks for t in set(ts))
            self.df, self.n = df, n
            self.avgdl = sum(len(t) for t in self.toks) / max(1, n)
            self.idf = {t: math.log((n + 1) / (d + 1)) + 1 for t, d in df.items()}
            self.tf = [Counter(ts) for ts in self.toks]
        elif mode == "embedding":
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(MODEL)
            self.emb = self.model.encode([c["text"] for c in chunks],
                                         normalize_embeddings=True)
        else:
            raise ValueError("Unknown mode: " + mode)

    def _scores(self, query):
        if self.mode == "embedding":
            q = self.model.encode([query], normalize_embeddings=True)[0]
            return list(self.emb @ q)
        qt = tokens(query)
        if self.mode == "bm25":
            k1, b, scores = 1.5, 0.75, []
            for tf, ts in zip(self.tf, self.toks):
                s = 0.0
                for t in set(qt):
                    if t in tf:
                        idf = math.log(1 + (self.n - self.df[t] + 0.5) / (self.df[t] + 0.5))
                        s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(ts) / self.avgdl))
                scores.append(s)
            return scores
        # tfidf cosine
        qv = {t: c * self.idf.get(t, 0) for t, c in Counter(qt).items()}
        qn = math.sqrt(sum(v * v for v in qv.values())) or 1.0
        scores = []
        for tf in self.tf:
            dv = {t: c * self.idf[t] for t, c in tf.items()}
            dn = math.sqrt(sum(v * v for v in dv.values())) or 1.0
            scores.append(sum(v * dv.get(t, 0) for t, v in qv.items()) / (qn * dn))
        return scores

    def search(self, query):
        if not query or not query.strip():
            return []
        scored = sorted(zip(self.chunks, self._scores(query)), key=lambda x: -x[1])
        return [(c, float(s)) for c, s in scored[:self.top_k] if s > self.threshold]
