"""工具基类与输入输出协议。"""
from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel


class ToolResult(BaseModel):
    """统一工具输出模型。"""

    success: bool
    data: dict
    message: str = ""


class BaseTool(ABC):
    """工具抽象基类。

    作用：定义统一执行入口，确保工具可被注册中心统一调度。
    """

    name: str
    description: str

    @abstractmethod
    def run(self, payload: dict) -> ToolResult:
        """执行工具。

        输入：payload字典。
        输出：ToolResult结构化结果。
        """
