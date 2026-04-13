"""REST API路由。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.config.settings import get_settings
from app.core.db import get_session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketAnalyzeRequest, EvalRunRequest
from app.repos.ticket_repo import TicketRepo
from app.services.agent_factory import build_agent
from app.evals.runner import EvalRunner

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/system/config")
def get_system_config():
    return get_settings().masked_config()


@router.post("/tickets")
def create_ticket(payload: TicketCreate, session: Session = Depends(get_session)):
    repo = TicketRepo(session)
    ticket = Ticket(**payload.model_dump())
    return repo.create(ticket)


@router.get("/tickets")
def list_tickets(session: Session = Depends(get_session)):
    return TicketRepo(session).list()


@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, session: Session = Depends(get_session)):
    ticket = TicketRepo(session).get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket not found")
    return ticket


@router.post("/tickets/analyze")
def analyze_ticket(payload: TicketAnalyzeRequest, session: Session = Depends(get_session)):
    repo = TicketRepo(session)
    ticket = repo.get(payload.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket not found")
    agent = build_agent(repo)
    return agent.run(ticket)


@router.get("/tickets/{ticket_id}/traces")
def traces(ticket_id: int, session: Session = Depends(get_session)):
    return TicketRepo(session).list_traces(ticket_id)


@router.post("/evals/run")
def run_eval(payload: EvalRunRequest, session: Session = Depends(get_session)):
    return EvalRunner(session).run(payload.dataset_name)
