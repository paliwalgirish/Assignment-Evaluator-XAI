# Auto Assignment Evaluator with Explainable AI (XAI)

This project implements an automated assignment evaluation system using Natural Language Processing and Semantic Similarity. It supports PDF-based student submissions, rubric-driven marking, explainable scoring, and plagiarism/fairness analysis.

The system is designed for academic use and keeps a human-in-the-loop for final grading decisions.

---

## ✨ Features

- Batch PDF upload (multiple students)
- Rubric-based automatic evaluation (Q-wise + partial credit)
- Semantic similarity using Sentence-BERT
- Explainable AI (per-question scoring + rubric matching)
- Image-only PDF detection (auto 0 marks)
- TF-IDF plagiarism detection
- Semantic plagiarism detection (SBERT)
- Fairness analysis (similar answers vs marks)
- Under-scoring recommendation (not auto-applied)
- Student-wise PDF reports
- CSV export of marks and similarity tables
- Streamlit web interface

---

## 🧠 Core Technologies

- Python 3.11+
- Streamlit (UI)
- SentenceTransformers (SBERT)
- Scikit-learn (TF-IDF, cosine similarity)
- PyMuPDF (PDF text extraction)
- ReportLab (PDF report generation)
- Pandas / NumPy

---

## 📁 Project Structure
Assignment_Evaluator/
│
├── app.py # Main Streamlit app
├── evaluator.py # Rubric-based scoring logic
├── rubric_parser.py # Rubric parsing
├── pdf_utils.py # PDF text extraction
├── qa_splitter.py # Question-wise answer splitting
├── report_pdf.py # Student + plagiarism PDF reports
├── requirements.txt
├── packages.txt
└── outputs/ # Generated results (ignored in Git)


---

## 🚀 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py

☁️ Deployment (Streamlit Cloud)

Push project to GitHub

Go to https://streamlit.io/cloud

Click New App

Select repository

Main file: app.py

Deploy

⚠️ Important Notes

Marks are NOT auto-modified based on similarity.

Semantic similarity is used only for fairness and instructor review.

Plagiarism results are advisory.

Instructor makes final decisions.

📜 Academic Disclaimer

This system provides decision support using Explainable AI. It does not replace human evaluation.

👤 Author

Dr. Girish Paliwal
Auto Assignment Evaluator with XAI


Commit it:

```powershell
git add README.md
git commit -m "Add README"
git push

✅ 2. Architecture Diagram (paper + documentation)

You can paste this diagram into Word / PPT / Paper:

                ┌─────────────────────┐
                │   Streamlit UI      │
                │ (Rubric + PDFs)     │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │   PDF Extraction    │
                │     (PyMuPDF)       │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Question Splitter   │
                │   (qa_splitter)     │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Rubric Parser       │
                └─────────┬───────────┘
                          │
                          ▼
                ┌────────────────────────────┐
                │ Rubric-Based Evaluation    │
                │ + SBERT Semantic Matching │
                └─────────┬──────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
   Plagiarism Detection          Fairness Analysis
 (TF-IDF + SBERT)          (Similarity vs Marks)

            └─────────────┬─────────────┘
                          ▼
                ┌─────────────────────┐
                │ Explainable Outputs │
                │ CSV + PDF Reports  │
                └─────────────────────┘


You can redraw this in PowerPoint / draw.io if needed.

✅ 3. Paper-Ready System Description (you can paste into your research paper)
System Overview

This work presents an Explainable AI based automatic assignment evaluation framework. The system accepts PDF submissions and evaluates answers using a structured rubric combined with semantic similarity. Student responses are embedded using Sentence-BERT, enabling concept-level matching rather than keyword comparison.

Rubric items are evaluated independently, allowing partial credit and explainable scoring. In addition, TF-IDF and SBERT-based similarity modules detect potential plagiarism and conceptual overlap among submissions.

To improve fairness, semantic similarity is also used as a grading consistency check. When two answers are conceptually similar but receive significantly different marks, the system flags possible under-scoring for instructor review. Importantly, marks are never automatically modified, maintaining a human-in-the-loop evaluation paradigm.

The framework generates student-wise PDF reports, similarity analytics, and fairness recommendations. The system is deployed using Streamlit Cloud, providing a scalable web interface.

Key contributions include:

Rubric-driven explainable evaluation

Semantic similarity based fairness auditing

Automated plagiarism analysis

Human-centered grading recommendations

✅ 4. Deployment Screenshots (what to capture)

Take screenshots of:

📸 Screenshot 1 – GitHub Repository

Show:

app.py

requirements.txt

README.md

Title:

Project Repository on GitHub

📸 Screenshot 2 – Streamlit Cloud Deploy Page

Show:

Repo selected

app.py selected

Deploy button

Title:

Streamlit Cloud Deployment Configuration

📸 Screenshot 3 – Running Web App

Show:

Rubric box

File uploader

Evaluate button

Title:

Deployed Assignment Evaluator Interface

📸 Screenshot 4 – Results Dashboard

Show:

Marks table

Semantic similarity table

Title:

Explainable Evaluation and Fairness Analysis Dashboard

These four screenshots are enough for:

✅ paper
✅ thesis
✅ viva
✅ project report
