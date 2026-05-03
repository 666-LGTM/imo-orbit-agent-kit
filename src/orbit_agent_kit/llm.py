from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol

from .config import MiMoConfig


@dataclass(frozen=True)
class LLMResult:
    content: str
    input_tokens: int
    output_tokens: int
    model: str
    latency_ms: int
    live: bool


class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> LLMResult:
        ...


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    chinese_chars = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    other_chars = len(text) - chinese_chars
    return max(1, chinese_chars + (other_chars + 3) // 4)


class MockMiMoClient:
    def __init__(self, model: str = "mock-mimo-v2.5-pro") -> None:
        self.model = model

    def complete(self, system: str, user: str) -> LLMResult:
        start = time.monotonic()
        role = system.splitlines()[0].strip().replace("#", "").strip() or "Agent"
        content = self._response_for(role, user)
        return LLMResult(
            content=content,
            input_tokens=estimate_tokens(system + "\n" + user),
            output_tokens=estimate_tokens(content),
            model=self.model,
            latency_ms=int((time.monotonic() - start) * 1000),
            live=False,
        )

    def _response_for(self, role: str, user: str) -> str:
        if "Planner" in role:
            return (
                "目标用户：需要申请 MiMo Orbit 权益的 AI Builder。\n"
                "核心任务：把项目想法转成可复现的 Agent 工作流和证明材料。\n"
                "成功指标：GitHub 可运行、生成物可截图、Token 预算可解释。"
            )
        if "Architect" in role:
            return (
                "架构：CLI 负责收集 idea，多 Agent 管线负责生成结构化成果，"
                "Report Builder 输出 markdown/json/html 三类证据。"
            )
        if "Builder" in role:
            return (
                "实现计划：1. 读取项目 idea；2. 顺序执行五个 Agent；"
                "3. 记录每步输入输出和 Token 估算；4. 生成证明包。"
            )
        if "Reviewer" in role:
            return (
                "审查结论：项目避免夸大真实用量，明确区分 mock 与 live，"
                "并提供可复现命令、CI 测试和后续接入 MiMo 的路径。"
            )
        return (
            "证明材料：本次运行展示了多 Agent 协作、Token 预算、"
            f"可复现报告和面向评审的项目叙述。输入摘要：{user[:120]}"
        )


class MiMoChatClient:
    def __init__(self, config: MiMoConfig) -> None:
        if not config.api_key:
            raise ValueError("MiMo API key is required for live mode.")
        self.config = config

    def complete(self, system: str, user: str) -> LLMResult:
        started = time.monotonic()
        body = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        request = urllib.request.Request(
            self.config.chat_completions_url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"MiMo API request failed: HTTP {exc.code} {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"MiMo API request failed: {exc.reason}") from exc

        message = payload.get("choices", [{}])[0].get("message", {})
        content = message.get("content", "")
        usage = payload.get("usage", {})
        return LLMResult(
            content=content,
            input_tokens=int(usage.get("prompt_tokens") or estimate_tokens(system + "\n" + user)),
            output_tokens=int(usage.get("completion_tokens") or estimate_tokens(content)),
            model=self.config.model,
            latency_ms=int((time.monotonic() - started) * 1000),
            live=True,
        )
