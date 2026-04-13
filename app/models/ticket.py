"""工单与追踪相关数据模型。"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Ticket(SQLModel, table=True):
    """工单主表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    error_log: str = ""
    priority: str = "P3"
    status: str = "new"
    category: str | None = None
    summary: str | None = None
    suggestion: str | None = None
    confidence: float | None = None
    needs_human: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentTrace(SQLModel, table=True):
    """Agent轨迹表：记录每一步执行。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    trace_id: str
    ticket_id: int = Field(index=True)
    step_no: int
    phase: str
    tool_name: str | None = None
    action_input: str | None = None
    observation: str | None = None
    success: bool = True
    error_message: str | None = None
    duration_ms: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
