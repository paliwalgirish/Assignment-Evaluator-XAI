import re
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class RubricItem:
    text: str
    marks: float

@dataclass
class QuestionRubric:
    qid: str
    total_marks: float
    items: List[RubricItem]

Q_HDR = re.compile(r"^\s*(Q\d+)\s*\(([\d.]+)\)", re.IGNORECASE)
ITEM = re.compile(r"^\s*(.+?)\s*\(([\d.]+)\)\s*$")

def parse_rubric(rubric_text: str) -> Dict[str, QuestionRubric]:
    lines = rubric_text.splitlines()
    rubrics = {}
    current_q = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        q_match = Q_HDR.match(line)
        if q_match:
            qid = q_match.group(1).upper()
            total = float(q_match.group(2))
            rubrics[qid] = QuestionRubric(qid, total, [])
            current_q = qid
            continue

        if current_q:
            i_match = ITEM.match(line)
            if i_match:
                rubrics[current_q].items.append(
                    RubricItem(i_match.group(1), float(i_match.group(2)))
                )
    return rubrics
