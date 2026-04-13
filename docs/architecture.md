# 架构设计

## 分层
- `app/agents`：Agent能力层（plan/synthesize/score/fallback）。
- `app/harness`：Harness约束层（白名单、重试、超时、状态流、prompt模板）。
- `app/tools`：独立工具层（结构化输入输出）。
- `app/api`：REST入口。
- `app/evals`：离线评测。

## 数据流
1. 前端提交工单。
2. API写入SQLite。
3. 触发分析时启动agent loop。
4. 每步调用工具并写入trace。
5. 汇总结果+置信度+风险，输出建议或转人工。

## 从demo到生产可演进方向
- 使用Redis缓存与状态存储。
- 用消息队列异步执行长任务。
- 接入统一权限与审计日志。
- 接入向量检索替代简单知识库匹配。
- 增加人工审批闭环与SLA跟踪。
