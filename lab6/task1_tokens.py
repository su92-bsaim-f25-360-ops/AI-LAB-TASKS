"""Task 1: compare tokenization choices on the corpus.

Run: python task1_tokens.py
Compares whitespace, regex-word and (if installed) the MiniLM WordPiece tokenizer,
and reports how many documents/chunks exceed the encoder input limit.
"""
import json
import re

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MAX_TOKENS = 256  # default max_seq_length of all-MiniLM-L6-v2 (see model card)


def whitespace_tokens(text):
    return text.split()


def regex_tokens(text):
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def load_wordpiece():
    try:
        from transformers import AutoTokenizer
        return AutoTokenizer.from_pretrained(MODEL)
    except Exception as err:  # offline / not installed
        print("WordPiece tokenizer unavailable:", err)
        return None


if __name__ == "__main__":
    with open("corpus.json", encoding="utf-8") as f:
        docs = json.load(f)
    wp = load_wordpiece()
    header = f"{'doc':12}{'chars':>7}{'whitespace':>12}{'regex':>8}"
    if wp:
        header += f"{'wordpiece':>11}{'>256?':>7}"
    print(header)
    for name, text in docs.items():
        row = f"{name:12}{len(text):>7}{len(whitespace_tokens(text)):>12}{len(regex_tokens(text)):>8}"
        if wp:
            n = len(wp.tokenize(text))
            row += f"{n:>11}{('yes' if n > MAX_TOKENS else 'no'):>7}"
        print(row)
    sample = "Contractors can't work remotely; e-mail HR (2026)."
    print("\nSample:", sample)
    print("whitespace:", whitespace_tokens(sample))
    print("regex     :", regex_tokens(sample))
    if wp:
        print("wordpiece :", wp.tokenize(sample))
