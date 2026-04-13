# 小型工单智能分诊与处理建议平台

一个“真实业务导向”的学习项目，用于快速理解：
1. Agent核心能力边界
2. Harness Engineering在工程中做什么
3. 如何把demo变成可控、可观测、可评估的小系统

## 建议阅读顺序
1. `docs/architecture.md`
2. `docs/agent-flow.md`
3. `app/agents/ticket_agent.py`
4. `app/harness/executor.py` + `app/harness/tool_registry.py`
5. `app/evals/runner.py`
6. 前端 `frontend/src/pages`

## 快速启动
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

前端：
```bash
cd frontend
npm install
npm run dev
```

## 这个项目里哪些是 Agent，哪些是 Harness Engineering
### Agent
- 任务规划：`app/agents/planner.py`
- 结果汇总：`app/agents/synthesizer.py`
- 置信度评估：`app/agents/confidence.py`
- 兜底决策：`app/agents/fallback.py`
- 主循环：`app/agents/ticket_agent.py`

### Harness Engineering
- 工具白名单与注册：`app/harness/tool_registry.py`
- 超时/重试/错误收敛：`app/harness/executor.py`
- Prompt模板管理：`app/harness/prompt_templates.py`
- 配置校验与脱敏：`app/config/settings.py`
- 评测运行与指标：`app/evals/runner.py`
- Trace可观测：`app/models/ticket.py` 的 `AgentTrace`

## Mock与真实模型切换
- `MODEL_USE_MOCK=true`：使用内置稳定Mock（推荐学习阶段）
- `MODEL_USE_MOCK=false` 且
  - `MODEL_PROVIDER=ollama`（调用 `/api/generate`）
  - `MODEL_PROVIDER=openai_compatible`（调用 `/v1/chat/completions`）

## 关键接口
- `POST /api/tickets`
- `GET /api/tickets`
- `GET /api/tickets/{id}`
- `POST /api/tickets/analyze`
- `GET /api/tickets/{id}/traces`
- `POST /api/evals/run`
- `GET /api/system/config`
- `GET /api/health`
