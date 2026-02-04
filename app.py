import os, json, shutil, re, uuid, hashlib
import pandas as pd
import streamlit as st
import numpy as np

from pdf_utils import extract_pdf_text
from rubric_parser import parse_rubric
from evaluator import evaluate_student
from report_pdf import generate_report_pdf
from qa_splitter import split_answers_by_qid

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# ================= UI =================

st.set_page_config(layout="wide")
st.title("Auto Assignment Evaluator (Human-Near XAI)")


# ================= STATE =================

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


# ================= SAFE RESET =================

def reset_outputs():
    if os.path.exists("outputs"):
        try:
            shutil.rmtree("outputs")
        except PermissionError:
            st.warning("Close open report PDFs before reset.")
            return

    os.makedirs("outputs/uploads", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)
    os.makedirs("outputs/debug", exist_ok=True)


if st.button("🔄 Reset"):
    reset_outputs()
    st.session_state["rubric"] = ""
    st.session_state.uploader_key += 1
    st.rerun()


# ================= WIDGETS =================

rubric_text = st.text_area(
    "Paste Rubric",
    height=200,
    key="rubric"
)

files = st.file_uploader(
    "Upload Student PDFs",
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)


# ================= HASH (SAFE) =================

def text_hash(text: str):
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return hashlib.md5(text.encode()).hexdigest()


# ================= EVALUATE =================

if st.button("Evaluate"):

    if not rubric_text.strip():
        st.error("Paste rubric first.")
        st.stop()

    if not files:
        st.error("Upload PDFs first.")
        st.stop()

    rubrics = parse_rubric(rubric_text)

    if not rubrics:
        st.error("Rubric parsing failed.")
        st.stop()

    os.makedirs("outputs/uploads", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)
    os.makedirs("outputs/debug", exist_ok=True)

    rows = []
    student_texts = {}

    # -------- STUDENT LOOP --------

    for f in files:

        st.write("Processing:", f.name)

        name = os.path.splitext(f.name)[0]

        safe_name = re.sub(r'[^\w\-. ]', '_', f.name)
        unique_name = f"{uuid.uuid4().hex}_{safe_name}"
        path = os.path.join("outputs/uploads", unique_name)

        with open(path, "wb") as w:
            w.write(f.read())

        text = extract_pdf_text(path)

        # ===== IMAGE ONLY =====
        if len(text.strip()) < 200:

            result = {
                "questions": {},
                "total": 0.0,
                "error": "Image-only PDF"
            }

            json.dump(result, open(f"outputs/debug/{name}.json", "w"), indent=2)
            generate_report_pdf(name, result, f"outputs/reports/{name}.pdf")

            rows.append({
                "student": name,
                "final_score": 0.0,
                "note": "Image-only PDF"
            })

            student_texts[name] = f"IMAGE_ONLY_{name}"
            continue

        # ===== ANSWER ONLY TEXT =====
        per_q = split_answers_by_qid(text, list(rubrics.keys()))
        ans_only = " ".join(v for v in per_q.values() if v.strip())
        student_texts[name] = ans_only if len(ans_only) > 300 else text

        # ===== EVALUATE =====
        result = evaluate_student(text, rubrics)

        json.dump(result, open(f"outputs/debug/{name}.json", "w"), indent=2)
        generate_report_pdf(name, result, f"outputs/reports/{name}.pdf")

        rows.append({
            "student": name,
            "final_score": result["total"]
        })

    # ================= RESULTS TABLE =================

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    df.to_csv("outputs/marks.csv", index=False)
    st.success(f"Evaluation complete. Processed {len(rows)} files.")


    # ================= TF-IDF COPY CHECK =================

    st.subheader("TF-IDF Copy Similarity")

    names = list(student_texts.keys())
    docs = [student_texts[n] for n in names]

    pairs = []

    if len(docs) >= 2:

        vec = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1,2)
        )

        X = vec.fit_transform(docs)
        sim = cosine_similarity(X)

        for i in range(len(names)):
            for j in range(i+1, len(names)):
                if sim[i,j] >= 0.80:
                    pairs.append({
                        "student_1": names[i],
                        "student_2": names[j],
                        "similarity": round(float(sim[i,j]),3)
                    })

    plag_df = pd.DataFrame(pairs)
    st.dataframe(plag_df)
    plag_df.to_csv("outputs/plagiarism_pairs.csv", index=False)


    # ================= EXACT DUPLICATES =================

    st.subheader("Exact Duplicate Detection")

    hashes = {}
    dups = []

    for n,t in student_texts.items():
        if len(t) < 300:
            continue
        h = text_hash(t)
        if h in hashes:
            dups.append({
                "student_1": hashes[h],
                "student_2": n
            })
        else:
            hashes[h] = n

    dup_df = pd.DataFrame(dups)
    st.dataframe(dup_df)


    

    model = SentenceTransformer("all-MiniLM-L6-v2")
    emb = model.encode(docs, normalize_embeddings=True)

    sem_sim = cosine_similarity(emb)
    # ================= SEMANTIC SIMILARITY + MARKS =================

    semantic_rows = []

    names = list(student_texts.keys())

    for i, student in enumerate(names):

        best_peer = None
        best_sim = 0.0

        for j, other in enumerate(names):
            if i != j and sem_sim[i, j] > best_sim:
                best_sim = sem_sim[i, j]
                best_peer = other

        # get marks
        my_marks = df.loc[df["student"] == student, "final_score"].values[0]

        if best_peer:
            peer_marks = df.loc[df["student"] == best_peer, "final_score"].values[0]
            mark_gap = round(peer_marks - my_marks, 2)
        else:
            peer_marks = "—"
            mark_gap = 0.0

        # upscale logic (recommendation only)
        if best_sim >= 0.85 and mark_gap >= 1.0:
            flag = "✅ Strong upscale possibility"
        elif best_sim >= 0.80 and mark_gap >= 0.5:
            flag = "⚠ Review suggested"
        else:
            flag = "—"

        semantic_rows.append({
            "student": student,
            "similar_to": best_peer if best_peer else "None",
            "semantic_similarity": round(float(best_sim), 3),
            "student_marks": my_marks,
            "peer_marks": peer_marks,
            "mark_gap": mark_gap,
            "upscale_possibility": flag
        })

    semantic_marks_df = pd.DataFrame(semantic_rows)
    st.subheader("Semantic Similarity with Marks (Fair Evaluation View)")
    st.dataframe(
        semantic_marks_df.sort_values(
            ["upscale_possibility", "semantic_similarity"],
            ascending=False
        ),
        use_container_width=True
    )


    semantic_marks_df.to_csv(
        "outputs/semantic_similarity_with_marks.csv",
        index=False
    )
