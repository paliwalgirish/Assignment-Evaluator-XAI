import re
from typing import Dict, List

def split_answers_by_qid(text: str, qids: List[str]) -> Dict[str, str]:
    """
    Supports:
    Q1, Question 1, QUESTION NO.1, 1., 1)
    """
    if not text:
        return {qid: "" for qid in qids}

    pattern = re.compile(
        r"(?im)^\s*(?:question\s*(?:no\.?)?\s*)?(?:q\s*)?(\d+)\s*[\.\)\:\-]",
        re.MULTILINE,
    )

    matches = list(pattern.finditer(text))
    out = {qid: "" for qid in qids}

    for i, m in enumerate(matches):
        qid = f"Q{m.group(1)}"
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        if qid in out:
            out[qid] = text[start:end].strip()

    return out
