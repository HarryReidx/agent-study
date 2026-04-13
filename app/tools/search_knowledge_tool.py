"""知识库检索工具。"""
from pathlib import Path
from pydantic import BaseModel
from app.tools.base import BaseTool, ToolResult


class SearchInput(BaseModel):
    category: str


class SearchKnowledgeTool(BaseTool):
    """在内置知识库中按分类检索处理经验。"""

    name = "search_knowledge_tool"
    description = "查询内置知识库"

    def __init__(self, kb_path: str = "data/knowledge_base.jsonl"):
        self.kb_path = Path(kb_path)

    def run(self, payload: dict) -> ToolResult:
        data = SearchInput(**payload)
        if not self.kb_path.exists():
            return ToolResult(success=False, data={}, message="知识库不存在")
        hits = []
        for line in self.kb_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            if f'"category": "{data.category}"' in line:
                hits.append(line)
        return ToolResult(success=True, data={"hits": hits[:3]}, message=f"命中{len(hits)}条")
