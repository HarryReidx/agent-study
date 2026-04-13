"""Pydantic请求响应模型。"""
from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str
    error_log: str = ""
    priority: str = "P3"


class TicketAnalyzeRequest(BaseModel):
    ticket_id: int


class EvalRunRequest(BaseModel):
    dataset_name: str = "default"
