# AGENTS.md（项目内协作说明）

## 项目目标
这是一个学习型项目，重点演示 Agent 与 Harness Engineering 的边界。

## 开发约定
1. 核心 Python 代码必须写中文注释与 docstring。
2. 新增工具时必须在 `app/harness/tool_registry.py` 注册，并在 Agent 白名单声明。
3. 不允许把所有逻辑塞进单一 service，需保持 planner/executor/scorer/fallback 分层。
4. 修改配置项时同步更新 `.env.example` 与 `/api/system/config` 返回。
5. Eval 指标字段保持兼容：成功率、转人工率、平均步骤数、工具调用次数、平均耗时。
