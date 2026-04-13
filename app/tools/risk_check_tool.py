"""风险检查工具。"""
from pydantic import BaseModel
from app.tools.base import BaseTool, ToolResult


class RiskInput(BaseModel):
    category: str
    priority: str
    confidence: float


class RiskCheckTool(BaseTool):
    """判断是否需要人工介入。

    规则：高优先级、低置信度、部署类问题会提升风险。
    """

    name = "risk_check_tool"
    description = "风险检查与人工兜底判断"

    def run(self, payload: dict) -> ToolResult:
        data = RiskInput(**payload)
        need = data.priority in {"P0", "P1"} or data.confidence < 0.65 or data.category in {"deploy", "unknown"}
        reason = "高风险，建议人工介入" if need else "风险可控"
        return ToolResult(success=True, data={"needs_human": need, "reason": reason}, message="风险评估完成")
