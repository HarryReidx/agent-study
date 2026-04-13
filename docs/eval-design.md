# Eval设计

## 数据集
`data/evals_default.jsonl` 提供标注类别。

## Runner
`app/evals/runner.py` 会批量创建评测工单并执行agent，统计：
- 成功率
- 转人工率
- 平均步骤数
- 工具调用次数
- 平均耗时

## 为什么重要
没有eval就无法判断变更是否让Agent更稳定，容易“看起来能跑，实际退化”。
