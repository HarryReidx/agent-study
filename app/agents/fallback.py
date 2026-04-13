"""人工兜底决策模块（Harness机制）。"""


class HumanHandoff:
    """依据置信度和风险标志决定是否转人工。"""

    def should_handoff(self, confidence: float, risk_result: dict) -> bool:
        return confidence < 0.65 or risk_result.get("needs_human", False)
