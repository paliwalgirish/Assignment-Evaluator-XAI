from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# =====================================================
# STUDENT EVALUATION REPORT
# =====================================================

def generate_report_pdf(student, result, path):

    c = canvas.Canvas(path, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"Evaluation Report: {student}")
    y -= 30

    # -------- IMAGE-ONLY / ERROR CASE --------
    if "error" in result:
        c.setFont("Helvetica", 11)
        c.drawString(40, y, f"Status: {result['error']}")
        c.drawString(40, y-20, "Marks Awarded: 0")
        c.save()
        return

    # -------- NORMAL CASE --------
    c.setFont("Helvetica", 11)

    for q, qres in result.get("questions", {}).items():

        c.drawString(40, y, f"{q}: {qres.get('score', 0)} marks")
        y -= 20

        for item in qres.get("items", []):
            rp = item.get("rubric_point", "")[:90]
            st = item.get("status", "")
            c.drawString(60, y, f"- {rp} ({st})")
            y -= 15

            if y < 80:
                c.showPage()
                y = 800
                c.setFont("Helvetica", 11)

        y -= 10

    c.drawString(40, y, f"Final Score: {result.get('total', 0)}")
    c.save()


# =====================================================
# FACULTY PLAGIARISM REPORT
# =====================================================

def generate_plagiarism_report(
    penalty_df,
    dup_df,
    sem_df,
    path="outputs/plagiarism_report.pdf"
):

    c = canvas.Canvas(path, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Plagiarism Analysis Report")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(
        40, y,
        "Note: Similarity does not imply guilt. Instructor review required."
    )
    y -= 30

    # -------- Exact duplicates --------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Exact Duplicate Submissions")
    y -= 20
    c.setFont("Helvetica", 10)

    if dup_df.empty:
        c.drawString(60, y, "None detected.")
        y -= 15
    else:
        for _, r in dup_df.iterrows():
            c.drawString(60, y, f"{r['student_1']}  ↔  {r['student_2']}")
            y -= 15

    y -= 20

    # -------- Penalty recommendations --------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Penalty Recommendations")
    y -= 20
    c.setFont("Helvetica", 10)

    for _, r in penalty_df.iterrows():

        c.drawString(
            40, y,
            f"Cluster {r['cluster_id']} — {r['recommended_action']}"
        )
        y -= 15

        c.drawString(60, y, f"Students: {r['students']}")
        y -= 15

        c.drawString(
            60, y,
            f"Semantic: {r['avg_semantic_similarity']} | "
            f"TF-IDF: {r['avg_tfidf_similarity']}"
        )
        y -= 25

        if y < 100:
            c.showPage()
            y = 800
            c.setFont("Helvetica", 10)

    c.save()
