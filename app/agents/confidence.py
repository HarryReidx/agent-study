"""置信度评估器（Agent能力+Harness约束）。"""


class ConfidenceScorer:
    """根据关键字段完整性与规则打分。"""

    def score(self, state: dict) -> float:
        score = 0.4
        if state.get("category"):
            score += 0.2
        if state.get("summary"):
            score += 0.2
        if state.get("suggestion"):
            score += 0.2
        return round(min(score, 0.95), 2)
