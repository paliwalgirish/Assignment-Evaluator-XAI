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

