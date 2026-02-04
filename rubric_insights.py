from collections import Counter

def collect_rubric_insights(all_results):
    insights = {}

    for qid, qres_list in all_results.items():
        missing = Counter()
        matched_phrases = Counter()

        for qres in qres_list:
            for item in qres["items"]:
                if item["status"] == "missing":
                    missing[item["rubric_point"]] += 1
                for ev in item.get("evidence", []):
                    matched_phrases[ev["text"][:80]] += 1

        insights[qid] = {
            "frequently_missing": missing.most_common(5),
            "common_phrases": matched_phrases.most_common(5),
        }

    return insights

