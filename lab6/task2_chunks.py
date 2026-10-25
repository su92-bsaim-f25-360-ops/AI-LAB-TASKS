"""Task 2: chunking strategies with exact character offsets.

make_chunks(docs, strategy) -> list of dicts with id, doc, text, start, end
Strategies:
  "doc"       whole document as one chunk
  "sentence"  one chunk per sentence
  "0"         fixed windows of WINDOW words, overlap 0 words
  "10"        fixed windows of WINDOW words, overlap 10 words
Offsets satisfy docs[doc][start:end] == text.
"""
import re

WINDOW = 30  # words per fixed window


def _record(doc, i, text, start, end):
    return {"id": f"{doc}#{i}", "doc": doc, "text": text, "start": start, "end": end}


def sentence_chunks(doc, text):
    out = []
    for m in re.finditer(r"[^.!?]+[.!?]+|[^.!?]+$", text):
        raw = m.group()
        stripped = raw.strip()
        if not stripped:
            continue
        start = m.start() + (len(raw) - len(raw.lstrip()))
        out.append(_record(doc, len(out), stripped, start, start + len(stripped)))
    return out


def window_chunks(doc, text, size, overlap):
    words = [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
    step = max(1, size - overlap)
    out = []
    for i in range(0, len(words), step):
        part = words[i:i + size]
        start, end = part[0][0], part[-1][1]
        out.append(_record(doc, len(out), text[start:end], start, end))
        if i + size >= len(words):
            break
    return out


def make_chunks(docs, strategy="sentence"):
    chunks = []
    for doc, text in docs.items():
        if strategy == "doc":
            chunks.append(_record(doc, 0, text, 0, len(text)))
        elif strategy == "sentence":
            chunks += sentence_chunks(doc, text)
        elif strategy in ("0", "10"):
            chunks += window_chunks(doc, text, WINDOW, int(strategy))
        else:
            raise ValueError("Unknown strategy: " + str(strategy))
    return chunks


if __name__ == "__main__":
    import json
    with open("corpus.json", encoding="utf-8") as f:
        docs = json.load(f)
    for s in ["doc", "sentence", "0", "10"]:
        ch = make_chunks(docs, s)
        assert all(docs[c["doc"]][c["start"]:c["end"]] == c["text"] for c in ch)
        sizes = [len(c["text"].split()) for c in ch]
        print(f"{s:9} chunks={len(ch):3} words min/mean/max = "
              f"{min(sizes)}/{sum(sizes)/len(sizes):.1f}/{max(sizes)}  offsets OK")
