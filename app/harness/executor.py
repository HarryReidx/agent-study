"""动作执行器（Harness机制）。

包含：超时、重试、错误收敛。
若缺失这些机制，Agent可能因单个工具异常而整体失败。
"""
from __future__ import annotations
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from app.tools.base import BaseTool, ToolResult


class ActionExecutor:
    def __init__(self, timeout_sec: int, retry_count: int):
        self.timeout_sec = timeout_sec
        self.retry_count = retry_count

    def execute(self, tool: BaseTool, payload: dict) -> tuple[ToolResult, int, str | None]:
        last_error = None
        start = time.time()
        for _ in range(self.retry_count + 1):
            try:
                with ThreadPoolExecutor(max_workers=1) as pool:
                    future = pool.submit(tool.run, payload)
                    result = future.result(timeout=self.timeout_sec)
                duration = int((time.time() - start) * 1000)
                return result, duration, None
            except FuturesTimeout:
                last_error = f"工具超时({self.timeout_sec}s)"
            except Exception as e:  # noqa: BLE001
                last_error = str(e)
        duration = int((time.time() - start) * 1000)
        return ToolResult(success=False, data={}, message="执行失败"), duration, last_error
