"""Agent装配工厂。

属于Harness工程：负责依赖注入与组件编排，避免API层拼装细节泄漏。
"""
from app.config.settings import get_settings
from app.repos.ticket_repo import TicketRepo
from app.services.model_provider import build_provider
from app.agents.ticket_agent import TicketAgent
from app.agents.planner import TaskPlanner
from app.agents.synthesizer import ResultSynthesizer
from app.agents.confidence import ConfidenceScorer
from app.agents.fallback import HumanHandoff
from app.harness.executor import ActionExecutor
from app.harness.tool_registry import ToolRegistry
from app.tools.classify_ticket_tool import ClassifyTicketTool
from app.tools.summarize_ticket_tool import SummarizeTicketTool
from app.tools.search_knowledge_tool import SearchKnowledgeTool
from app.tools.generate_suggestion_tool import GenerateSuggestionTool
from app.tools.risk_check_tool import RiskCheckTool


def build_agent(repo: TicketRepo) -> TicketAgent:
    settings = get_settings()
    registry = ToolRegistry()
    registry.register(ClassifyTicketTool())
    registry.register(SummarizeTicketTool())
    registry.register(SearchKnowledgeTool())
    registry.register(GenerateSuggestionTool())
    registry.register(RiskCheckTool())

    return TicketAgent(
        repo=repo,
        provider=build_provider(settings),
        planner=TaskPlanner(),
        registry=registry,
        executor=ActionExecutor(timeout_sec=settings.harness_tool_timeout, retry_count=settings.harness_retry_count),
        synthesizer=ResultSynthesizer(),
        scorer=ConfidenceScorer(),
        fallback=HumanHandoff(),
        max_steps=settings.harness_max_steps,
    )
