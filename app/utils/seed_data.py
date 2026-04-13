"""初始化测试数据。"""
from pathlib import Path
import json
from sqlmodel import Session, select
from app.core.db import engine
from app.models.ticket import Ticket


def seed_if_needed() -> None:
    """首次启动时加载20条模拟工单。"""
    with Session(engine) as session:
        count = len(session.exec(select(Ticket)).all())
        if count > 0:
            return
        path = Path("data/tickets_seed.jsonl")
        if not path.exists():
            return
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            session.add(Ticket(**json.loads(line)))
        session.commit()
