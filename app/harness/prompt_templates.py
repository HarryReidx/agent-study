"""Prompt模板管理（Harness机制）。"""

PROMPTS = {
    "ticket_classifier_system": "你是企业工单分诊助手，输出JSON。",
    "ticket_classifier_user": "请判断工单类别与风险：{text}",
}


def render_prompt(name: str, **kwargs) -> str:
    tmpl = PROMPTS[name]
    return tmpl.format(**kwargs)
