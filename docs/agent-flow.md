# Agent Flow

1. Planner生成步骤。
2. Executor按白名单执行工具（带超时+重试）。
3. 每一步写trace（含输入、观察、耗时、错误）。
4. Synthesizer整理结果。
5. ConfidenceScorer打分。
6. HumanHandoff决定是否转人工。

> 关键边界：Agent负责“如何思考与决策”；Harness负责“如何约束与保障可控”。
