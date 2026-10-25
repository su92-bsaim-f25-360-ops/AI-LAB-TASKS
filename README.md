AI Lab Tasks

Course: CAI601400 Artificial Intelligence Lab
Student: Hamza Hakam
Repository: AI-LAB-TASKS

This repository contains my work for AI Labs 1 to 6. Each lab is in its own folder with its own code, outputs and report. Open the folder of a lab to see its commands and results.

Repository structure
AI-LAB-TASKS/
├── lab1/   AI timeline, rule-based scholarship eligibility, Turing-test comparison
├── lab2/   (add title)
├── lab3/   (add title)
├── lab4/   (add title)
├── lab5/   (add title)
├── lab6/   Document retrieval and evidence chatbot
└── README.md
Requirements
Python 3.10 or newer
Lab 6 needs extra packages: pip install -r lab6/requirements.txt
Do not commit virtual environments, model caches or credentials (see .gitignore).
Lab summary
Lab	Topic	Main files	Report
1	AI timeline, rule-based scholarship system, conversational (Turing) test comparison	lab1_rules.py, lab1_compare.py, README.md, captured outputs	Lab1_Report.docx
2	(add topic)	(add files)	Lab2_Report.docx
3	(add topic)	(add files)	Lab3_Report.docx
4	(add topic)	(add files)	Lab4_Report.docx
5	(add topic)	(add files)	Lab5_Report.docx
6	Tokenization, chunking and retrieval (BM25, TF-IDF, embeddings) with an evidence chatbot	task1_tokens.py, task2_chunks.py, task3_retrieval.py, lab6_search.py, document_chatbot.py, corpus.json, queries.json, retrieval_log.csv	Lab6_Report.docx
Lab 1: AI timeline, rule-based system and Turing test

What it covers

An AI timeline with 5 or more sourced entries, including an AI winter and a modern compute/data milestone.
A rule-based scholarship eligibility example, extended with two named conditions and four test cases.
A comparison of conversational (Turing-style) tests.

Run

bash
cd lab1
python lab1_rules.py
python lab1_compare.py

Files: lab1_rules.py, lab1_compare.py, README.md, captured outputs, Lab1_Report.docx

Lab 2: (add title)

What it covers: (add a short description)

Run

bash
cd lab2
python (add file name)

Files: (add files), Lab2_Report.docx

Lab 3: (add title)

What it covers: (add a short description)

Run

bash
cd lab3
python (add file name)

Files: (add files), Lab3_Report.docx

Lab 4: (add title)

What it covers: (add a short description)

Run

bash
cd lab4
python (add file name)

Files: (add files), Lab4_Report.docx

Lab 5: (add title)

What it covers: (add a short description)

Run

bash
cd lab5
python (add file name)

Files: (add files), Lab5_Report.docx

Lab 6: Document retrieval and evidence chatbot

What it covers

Task 1: compares whitespace, regex and WordPiece tokenization against the 256-token limit of the encoder.
Task 2: chunking strategies (doc, sentence, 30-word windows with 0 and 10 words of overlap) with exact character offsets.
Task 3: evaluation of BM25, TF-IDF and all-MiniLM-L6-v2 embeddings on development and test queries, written to retrieval_log.csv, and an interactive chatbot that shows candidate evidence for the user to confirm.

Setup and run

bash
cd lab6
python -m venv venv
# Windows: venv\Scripts\activate    Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python create_dataset.py
python task1_tokens.py
python task2_chunks.py
python task3_retrieval.py
python document_chatbot.py

task3_retrieval.py chooses the best configuration on the development split only and saves it in selected_config.json, which the chatbot then uses. The embedding model is downloaded from Hugging Face on first use.

Chatbot behaviour: candidates are shown with ID, score and character offsets. The passage is displayed only after the user chooses one. An empty query, an unsupported query, Enter or an invalid choice gives the fallback message. A candidate is never presented as a verified answer.

Files: create_dataset.py, task1_tokens.py, task2_chunks.py, task3_retrieval.py, lab6_search.py, document_chatbot.py, corpus.json, queries.json, retrieval_log.csv, requirements.txt, README.md, Lab6_Report.docx

Submission

The repository URL and the final commit ID are submitted to the instructor through the course submission channel.

Sources and attribution

Starter code and datasets come from the lab manuals and were adapted as described in each lab's own README and report. External references:

Sentence Transformers documentation: https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html
all-MiniLM-L6-v2 model card: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

All other code and written work are my own.
