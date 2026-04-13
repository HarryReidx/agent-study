"""任务规划器（Agent能力）。"""
from app.models.ticket import Ticket


class TaskPlanner:
    """将工单转为可执行步骤。

    为什么存在：让Agent执行可解释、可追踪的计划，而非黑盒一次性输出。
    """

    def plan(self, ticket: Ticket) -> list[dict]:
        return [
            {"tool": "classify_ticket_tool", "input": {"title": ticket.title, "description": ticket.description, "error_log": ticket.error_log}},
            {"tool": "summarize_ticket_tool", "input": {"title": ticket.title, "description": ticket.description}},
            {"tool": "search_knowledge_tool", "input": {}},
            {"tool": "generate_suggestion_tool", "input": {}},
            {"tool": "risk_check_tool", "input": {}},
        ]
