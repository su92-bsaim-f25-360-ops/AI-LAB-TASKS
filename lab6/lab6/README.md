# AI Lab 6: Document Retrieval and Evidence Chatbot

Course: CAI601400 Artificial Intelligence Lab  
Student: Hamza Hakam

## Setup
```bash
python -m venv venv
# Windows: venv\Scripts\activate    Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```
The embedding model `sentence-transformers/all-MiniLM-L6-v2` is downloaded automatically
from Hugging Face on first use (public, no credentials needed). Model weights and the
virtual environment are not part of this repository.

## Commands
| Step | Command | What it does |
|---|---|---|
| 0 | `python create_dataset.py` | Creates `corpus.json` (5 documents of 150-250 words) and `queries.json` (4 dev, 6 test queries). Refuses to overwrite existing files. |
| 1 | `python task1_tokens.py` | Compares whitespace, regex and WordPiece tokenization and token counts against the 256-token encoder limit. |
| 2 | `python task2_chunks.py` | Builds `doc`, `sentence`, `0` (30-word windows, no overlap) and `10` (30-word windows, 10-word overlap) chunks and checks that offsets are exact. |
| 3 | `python task3_retrieval.py` | Evaluates BM25, TF-IDF and embedding retrieval over every chunking strategy, writes `retrieval_log.csv` and `selected_config.json` (chosen on the development split only). |
| 4 | `python document_chatbot.py` | Interactive chatbot using the selected configuration. Type `exit` to quit. |

Run step 3 before step 4 so the chatbot uses the configuration justified by development results.

## Files
- `lab6_search.py`: `Retriever` class (bm25 / tfidf / embedding); returns no hits for empty queries or scores below the threshold.
- `task2_chunks.py`: chunking with exact character offsets (`docs[doc][start:end] == text`).
- `task3_retrieval.py`: evaluation (Hit@1, Hit@3, abstention on unsupported queries, average top-1 passage length, ms/query).
- `document_chatbot.py`: confirmation/fallback chatbot (candidates are never presented as verified answers).
- `corpus.json`, `queries.json`, `retrieval_log.csv`: dataset and results.
- `Lab6_Report.docx`: report with results, tables and transcripts.

## Chatbot behaviour
1. The question is searched and ranked candidates are shown with IDs, scores and character offsets.
2. The user chooses 1-3 to inspect the exact passage and its source offsets.
3. Pressing Enter, an invalid choice, an empty query or an unsupported query gives the fallback message.

## Evaluation method
A hit means a top-k chunk comes from the gold document and its character span overlaps the gold evidence span.
Unsupported queries are correct only when no candidate is returned. Timing is the mean of 5 repeated passes over
the queries (model loading excluded) using `time.perf_counter`.

## Sources and attribution
- Starter dataset and the chatbot loop come from the lab manual; the evidence sentences are unchanged, and the
  distractor text around them was added by me.
- Embedding model: all-MiniLM-L6-v2 via Sentence Transformers
  (https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html,
  https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
- BM25 and TF-IDF are implemented from scratch in `lab6_search.py`; chunking and evaluation code is my own work.

## Limitations
The dataset is small (4 dev / 6 test queries), so differences between strategies are not statistically reliable.
