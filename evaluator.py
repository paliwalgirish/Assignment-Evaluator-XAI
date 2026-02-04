import re
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from qa_splitter import split_answers_by_qid

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

@st.cache_resource
def get_model(model_name):
    return SentenceTransformer(model_name)

def split_sentences(text):
    sents = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    return [s for s in sents if len(s) >= 10]

def evaluate_student(student_text, rubrics, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    model = get_model(model_name)
    qids = list(rubrics.keys())

    # -------- GENERIC QUESTION HANDLING --------
    per_q_text = split_answers_by_qid(student_text, qids)
    for qid in qids:
        if not per_q_text.get(qid, "").strip():
            per_q_text[qid] = student_text  # fallback

    results = {"questions": {}, "total": 0.0}

    for qid, qr in rubrics.items():
        text = per_q_text[qid]
        sents = split_sentences(text)[:250]
        emb_sents = model.encode(sents, normalize_embeddings=True) if sents else None

        q_score = 0.0
        details = []

        for item in qr.items:
            if not sents:
                sim = 0.0
                evidence = []
            else:
                emb_item = model.encode([item.text], normalize_embeddings=True)[0]
                sims = emb_sents @ emb_item
                idx = np.argmax(sims)
                sim = float(sims[idx])
                evidence = [{"text": sents[idx], "similarity": round(sim, 3)}]

            # ---- HUMAN-NEAR SCORING ----
            if sim >= 0.45:
                awarded = item.marks
                status = "matched"
            elif sim >= 0.30:
                awarded = round(0.75 * item.marks, 2)
                status = "partial"
            elif sim >= 0.18:
                awarded = round(0.40 * item.marks, 2)
                status = "partial"
            else:
                awarded = 0.0
                status = "missing"

            q_score += awarded
            details.append({
                "rubric_point": item.text,
                "max_marks": item.marks,
                "awarded": awarded,
                "status": status,
                "similarity": round(sim, 3),
                "evidence": evidence
            })

        q_score = min(q_score, qr.total_marks)
        # ---------- QUESTION-LEVEL SATISFACTION BONUS ----------
        matched_or_partial = sum(
            1 for d in details if d["status"] in ("matched", "partial")
        )
        coverage_ratio = matched_or_partial / max(len(details), 1)

        # If most rubric points are addressed, give small human-like bonus
        if coverage_ratio >= 0.75:
            q_score = min(qr.total_marks, q_score + 0.25)
                

       
        results["questions"][qid] = {
            "score": round(q_score, 2),
            "items": details
        }
        results["total"] += q_score

    # -------- HUMAN FAIRNESS RULES --------
    if len(student_text) > 700 and results["total"] < 4.0:
        results["total"] = 4.0

    diagram_words = ["diagram", "figure", "block", "architecture", "flow"]
    if any(w in student_text.lower() for w in diagram_words) and results["total"] < 5.0:
        results["total"] += 0.5
    # ---------- IMAGE / DIAGRAM EFFORT BONUS ----------
    diagram_keywords = [
        "diagram", "figure", "block diagram", "flowchart",
        "architecture", "model", "network structure"
    ]

    diagram_detected = any(
        k in student_text.lower() for k in diagram_keywords
    )

    if diagram_detected:
        # Human-style: reward diagram effort, but cap bonus
        results["total"] += 1.0   # or use 0.5 if you want stricter

    results["total"] = round(min(results["total"], 10.0), 2)
    return results
