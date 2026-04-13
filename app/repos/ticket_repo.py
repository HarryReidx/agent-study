"""工单仓储层。"""
from sqlmodel import Session, select
from app.models.ticket import Ticket, AgentTrace


class TicketRepo:
    """封装数据库读写，避免业务层直接操作ORM细节。"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def update(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def list(self) -> list[Ticket]:
        return list(self.session.exec(select(Ticket).order_by(Ticket.id.desc())).all())

    def get(self, ticket_id: int) -> Ticket | None:
        return self.session.get(Ticket, ticket_id)

    def save_trace(self, trace: AgentTrace) -> AgentTrace:
        self.session.add(trace)
        self.session.commit()
        self.session.refresh(trace)
        return trace

    def list_traces(self, ticket_id: int) -> list[AgentTrace]:
        stmt = select(AgentTrace).where(AgentTrace.ticket_id == ticket_id).order_by(AgentTrace.step_no)
        return list(self.session.exec(stmt).all())
