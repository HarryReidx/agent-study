"""应用配置模块。"""
from functools import lru_cache
from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """系统配置。

    作用：
    - 统一读取环境变量与默认值。
    - 为模型调用与harness参数提供可校验的配置入口。
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Ticket Triage Agent"
    app_env: str = "dev"

    database_url: str = "sqlite:///./data/app.db"

    model_use_mock: bool = True
    model_provider: str = "mock"  # mock / ollama / openai_compatible
    model_base_url: str = "http://localhost:11434"
    model_name: str = "llama3.1:8b"
    model_api_key: SecretStr | None = None
    model_timeout: int = 20
    model_temperature: float = 0.2
    model_max_tokens: int = 512

    harness_max_steps: int = 6
    harness_tool_timeout: int = 10
    harness_retry_count: int = 2

    @model_validator(mode="after")
    def validate_provider(self):
        allowed = {"mock", "ollama", "openai_compatible"}
        if self.model_provider not in allowed:
            raise ValueError(f"MODEL_PROVIDER必须属于{allowed}")
        if self.model_use_mock and self.model_provider != "mock":
            # 学习型项目中，mock模式强制provider=mock，避免配置歧义
            self.model_provider = "mock"
        return self

    def masked_config(self) -> dict:
        """返回脱敏后的配置给前端展示。"""
        return {
            "app_name": self.app_name,
            "app_env": self.app_env,
            "model_use_mock": self.model_use_mock,
            "model_provider": self.model_provider,
            "model_base_url": self.model_base_url,
            "model_name": self.model_name,
            "model_timeout": self.model_timeout,
            "model_temperature": self.model_temperature,
            "model_max_tokens": self.model_max_tokens,
            "harness_max_steps": self.harness_max_steps,
            "harness_tool_timeout": self.harness_tool_timeout,
            "harness_retry_count": self.harness_retry_count,
            "model_api_key": "***" if self.model_api_key else None,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
