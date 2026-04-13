"""工单Agent主循环。

本文件同时体现：
- Agent能力：规划、观察、汇总、决策。
- Harness机制：步骤上限、工具白名单、trace、重试超时、错误处理。
"""
from __future__ import annotations
import json
import uuid
from app.models.ticket import Ticket, AgentTrace
from app.repos.ticket_repo import TicketRepo
from app.agents.planner import TaskPlanner
from app.agents.synthesizer import ResultSynthesizer
from app.agents.confidence import ConfidenceScorer
from app.agents.fallback import HumanHandoff
from app.harness.executor import ActionExecutor
from app.harness.tool_registry import ToolRegistry
from app.harness.prompt_templates import render_prompt
from app.services.model_provider import ModelProvider


class TicketAgent:
    def __init__(
        self,
        repo: TicketRepo,
        provider: ModelProvider,
        planner: TaskPlanner,
        registry: ToolRegistry,
        executor: ActionExecutor,
        synthesizer: ResultSynthesizer,
        scorer: ConfidenceScorer,
        fallback: HumanHandoff,
        max_steps: int,
    ):
        self.repo = repo
        self.provider = provider
        self.planner = planner
        self.registry = registry
        self.executor = executor
        self.synthesizer = synthesizer
        self.scorer = scorer
        self.fallback = fallback
        self.max_steps = max_steps
        self.whitelist = {
            "classify_ticket_tool",
            "summarize_ticket_tool",
            "search_knowledge_tool",
            "generate_suggestion_tool",
            "risk_check_tool",
        }

    def run(self, ticket: Ticket) -> dict:
        trace_id = str(uuid.uuid4())
        plan = self.planner.plan(ticket)
        state: dict = {"risk": {}, "priority": ticket.priority}

        for i, step in enumerate(plan[: self.max_steps], start=1):
            tool_name = step["tool"]
            payload = self._build_payload(step, state)
            tool = self.registry.get(tool_name, whitelist=self.whitelist)
            result, duration, error = self.executor.execute(tool, payload)
            self.repo.save_trace(
                AgentTrace(
                    trace_id=trace_id,
                    ticket_id=ticket.id,
                    step_no=i,
                    phase="tool_execute",
                    tool_name=tool_name,
                    action_input=json.dumps(payload, ensure_ascii=False),
                    observation=json.dumps(result.data, ensure_ascii=False),
                    success=result.success,
                    error_message=error,
                    duration_ms=duration,
                )
            )
            if not result.success:
                break
            self._update_state(state, tool_name, result.data)

        # 额外调用模型作为信号补充（可mock）
        llm_text = self.provider.generate(
            render_prompt("ticket_classifier_system"),
            render_prompt("ticket_classifier_user", text=f"{ticket.title} {ticket.description}"),
        )
        self.repo.save_trace(AgentTrace(trace_id=trace_id, ticket_id=ticket.id, step_no=99, phase="llm_signal", observation=llm_text, success=True))

        final = self.synthesizer.synthesize(state)
        confidence = self.scorer.score(state)
        risk = state.get("risk", {})
        needs_human = self.fallback.should_handoff(confidence, risk)

        ticket.category = final.get("category")
        ticket.summary = final.get("summary")
        ticket.suggestion = final.get("suggestion")
        ticket.confidence = confidence
        ticket.needs_human = needs_human
        ticket.status = "handoff" if needs_human else "resolved_suggestion"
        self.repo.update(ticket)

        return {
            "trace_id": trace_id,
            "ticket_id": ticket.id,
            "confidence": confidence,
            "needs_human": needs_human,
            "final": final,
        }

    def _build_payload(self, step: dict, state: dict) -> dict:
        payload = dict(step.get("input", {}))
        if step["tool"] == "search_knowledge_tool":
            payload = {"category": state.get("category", "unknown")}
        elif step["tool"] == "generate_suggestion_tool":
            payload = {
                "category": state.get("category", "unknown"),
                "summary": state.get("summary", ""),
                "knowledge_hits": state.get("knowledge_hits", []),
            }
        elif step["tool"] == "risk_check_tool":
            payload = {
                "category": state.get("category", "unknown"),
                "priority": state.get("priority", "P3"),
                "confidence": state.get("confidence", 0.5),
            }
        return payload

    def _update_state(self, state: dict, tool_name: str, data: dict) -> None:
        if tool_name == "classify_ticket_tool":
            state["category"] = data.get("category")
        elif tool_name == "summarize_ticket_tool":
            state["summary"] = data.get("summary")
        elif tool_name == "search_knowledge_tool":
            state["knowledge_hits"] = data.get("hits", [])
        elif tool_name == "generate_suggestion_tool":
            state["suggestion"] = data.get("suggestion")
        elif tool_name == "risk_check_tool":
            state["risk"] = data
