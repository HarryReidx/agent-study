"""工单分类工具。"""
from pydantic import BaseModel
from app.tools.base import BaseTool, ToolResult


class ClassifyInput(BaseModel):
    title: str
    description: str
    error_log: str = ""


class ClassifyTicketTool(BaseTool):
    """根据文本规则进行工单分类。

    这是学习项目中的可预测工具，便于与LLM结果对照。
    """

    name = "classify_ticket_tool"
    description = "根据工单内容分类"

    def run(self, payload: dict) -> ToolResult:
        data = ClassifyInput(**payload)
        text = f"{data.title} {data.description} {data.error_log}".lower()
        if "登录" in text or "login" in text:
            category = "auth"
        elif "权限" in text or "permission" in text:
            category = "permission"
        elif "超时" in text or "timeout" in text or "接口" in text:
            category = "api"
        elif "同步" in text:
            category = "sync"
        elif "部署" in text:
            category = "deploy"
        elif "配置" in text:
            category = "config"
        else:
            category = "frontend"
        return ToolResult(success=True, data={"category": category}, message="分类完成")
