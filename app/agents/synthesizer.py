"""结果汇总器（Agent能力）。"""


class ResultSynthesizer:
    """整合工具观察结果，形成结构化输出。"""

    def synthesize(self, state: dict) -> dict:
        return {
            "category": state.get("category"),
            "summary": state.get("summary"),
            "suggestion": state.get("suggestion"),
        }
