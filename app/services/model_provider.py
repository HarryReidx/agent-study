"""模型Provider抽象层。

这是关键的harness基础设施：
- Agent只依赖ModelProvider接口，不关心具体供应商实现。
- 便于在mock、ollama、openai兼容服务间切换。
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import json
import httpx
from app.config.settings import Settings


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """生成文本响应。"""


class MockProvider(ModelProvider):
    """稳定可预测的Mock模型。

    设计原因：学习/调试时需要结果稳定，方便观察agent loop与eval变化。
    """

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        low = user_prompt.lower()
        if "login" in low or "登录" in low:
            return json.dumps({"category": "auth", "confidence": 0.86, "risk": "low"}, ensure_ascii=False)
        if "timeout" in low or "超时" in low:
            return json.dumps({"category": "api", "confidence": 0.74, "risk": "medium"}, ensure_ascii=False)
        if "部署" in low or "deploy" in low:
            return json.dumps({"category": "deploy", "confidence": 0.68, "risk": "high"}, ensure_ascii=False)
        return json.dumps({"category": "unknown", "confidence": 0.52, "risk": "medium"}, ensure_ascii=False)


class OllamaProvider(ModelProvider):
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.settings.model_name,
            "prompt": f"{system_prompt}\n{user_prompt}",
            "stream": False,
            "options": {
                "temperature": self.settings.model_temperature,
                "num_predict": self.settings.model_max_tokens,
            },
        }
        with httpx.Client(timeout=self.settings.model_timeout) as client:
            r = client.post(f"{self.settings.model_base_url}/api/generate", json=payload)
            r.raise_for_status()
            return r.json().get("response", "")


class OpenAICompatibleProvider(ModelProvider):
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        if self.settings.model_api_key:
            headers["Authorization"] = f"Bearer {self.settings.model_api_key.get_secret_value()}"
        payload = {
            "model": self.settings.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.settings.model_temperature,
            "max_tokens": self.settings.model_max_tokens,
        }
        with httpx.Client(timeout=self.settings.model_timeout) as client:
            r = client.post(f"{self.settings.model_base_url}/v1/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]


def build_provider(settings: Settings) -> ModelProvider:
    """根据配置构建Provider。"""
    if settings.model_use_mock or settings.model_provider == "mock":
        return MockProvider()
    if settings.model_provider == "ollama":
        return OllamaProvider(settings)
    return OpenAICompatibleProvider(settings)
