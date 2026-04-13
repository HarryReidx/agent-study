"""工单摘要工具。"""
from pydantic import BaseModel
from app.tools.base import BaseTool, ToolResult


class SummarizeInput(BaseModel):
    title: str
    description: str


class SummarizeTicketTool(BaseTool):
    """生成简短摘要，帮助后续知识检索与人工理解。"""

    name = "summarize_ticket_tool"
    description = "生成工单摘要"

    def run(self, payload: dict) -> ToolResult:
        data = SummarizeInput(**payload)
        summary = f"问题：{data.title}；现象：{data.description[:80]}"
        return ToolResult(success=True, data={"summary": summary}, message="摘要完成")
