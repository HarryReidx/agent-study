from app.tools.classify_ticket_tool import ClassifyTicketTool
from app.tools.risk_check_tool import RiskCheckTool


def test_classify_tool():
    res = ClassifyTicketTool().run({"title": "登录失败", "description": "无法登录", "error_log": ""})
    assert res.success
    assert res.data["category"] == "auth"


def test_risk_tool():
    res = RiskCheckTool().run({"category": "deploy", "priority": "P1", "confidence": 0.8})
    assert res.data["needs_human"] is True
