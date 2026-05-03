from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class MiMoConfig:
    api_key: str | None
    base_url: str
    model: str
    timeout_seconds: int

    @property
    def chat_completions_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"


def load_config() -> MiMoConfig:
    api_key = os.getenv("XIAOMI_MIMO_API_KEY") or os.getenv("MIMO_API_KEY")
    return MiMoConfig(
        api_key=api_key,
        base_url=os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
        model=os.getenv("MIMO_MODEL", "mimo-v2.5-pro"),
        timeout_seconds=int(os.getenv("MIMO_TIMEOUT_SECONDS", "60")),
    )
