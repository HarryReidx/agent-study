"""工具注册中心（Harness机制）。

解决问题：
- 防止Agent调用未授权工具（工具白名单）。
- 统一管理工具元数据，便于审计与可观测。
"""
from app.tools.base import BaseTool


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str, whitelist: set[str] | None = None) -> BaseTool:
        if whitelist is not None and name not in whitelist:
            raise ValueError(f"工具{name}不在白名单中")
        if name not in self._tools:
            raise ValueError(f"工具{name}未注册")
        return self._tools[name]

    def list_names(self) -> list[str]:
        return list(self._tools.keys())
