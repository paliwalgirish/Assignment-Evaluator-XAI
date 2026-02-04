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


Marks are NOT auto-modified based on similarity.

Semantic similarity is used only for fairness and instructor review.

Plagiarism results are advisory.

Instructor makes final decisions.

📜 Academic Disclaimer

Note : This system provides decision support using Explainable AI. It does not replace human evaluation.

👤 Author

Prof(Dr.) Girish Paliwal
Auto Assignment Evaluator with XAI



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



