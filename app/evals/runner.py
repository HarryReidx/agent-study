"""Eval Runner：批量评测Agent行为。"""
from __future__ import annotations
import json
import time
from pathlib import Path
from statistics import mean
from sqlmodel import Session
from app.models.ticket import Ticket
from app.repos.ticket_repo import TicketRepo
from app.services.agent_factory import build_agent


class EvalRunner:
    """执行离线评测并汇总指标。"""

    def __init__(self, session: Session):
        self.session = session

    def run(self, dataset_name: str = "default") -> dict:
        path = Path(f"data/evals_{dataset_name}.jsonl")
        if not path.exists():
            raise FileNotFoundError(f"评测集不存在: {path}")
        rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        success = 0
        handoff = 0
        steps = []
        tool_calls = []
        cost = []
        repo = TicketRepo(self.session)
        agent = build_agent(repo)
        for row in rows:
            t = Ticket(title=f"[EVAL]{row['title']}", description=row['description'], error_log=row.get('error_log', ''), priority=row.get('priority', 'P3'))
            repo.create(t)
            st = time.time()
            result = agent.run(t)
            traces = repo.list_traces(t.id)
            elapsed = time.time() - st
            if result["final"].get("category") == row.get("expected_category"):
                success += 1
            if result["needs_human"]:
                handoff += 1
            steps.append(len([x for x in traces if x.phase == "tool_execute"]))
            tool_calls.append(len([x for x in traces if x.tool_name]))
            cost.append(elapsed)
        total = len(rows)
        return {
            "dataset": dataset_name,
            "total": total,
            "success_rate": round(success / total, 2) if total else 0,
            "handoff_rate": round(handoff / total, 2) if total else 0,
            "avg_steps": round(mean(steps), 2) if steps else 0,
            "tool_calls": round(mean(tool_calls), 2) if tool_calls else 0,
            "avg_duration_sec": round(mean(cost), 3) if cost else 0,
        }
