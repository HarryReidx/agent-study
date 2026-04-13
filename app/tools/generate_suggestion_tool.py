"""建议生成工具。"""
from pydantic import BaseModel
from app.tools.base import BaseTool, ToolResult


class SuggestionInput(BaseModel):
    category: str
    summary: str
    knowledge_hits: list[str] = []


class GenerateSuggestionTool(BaseTool):
    """根据分类、摘要、知识命中生成下一步建议。"""

    name = "generate_suggestion_tool"
    description = "生成处理建议"

    def run(self, payload: dict) -> ToolResult:
        data = SuggestionInput(**payload)
        base = f"建议优先排查 {data.category} 相关配置与日志。"
        if data.knowledge_hits:
            base += " 可参考知识库步骤并先在测试环境复现。"
        base += f" 摘要：{data.summary}"
        return ToolResult(success=True, data={"suggestion": base}, message="建议生成成功")
