from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .llm import LLMClient, LLMResult


@dataclass(frozen=True)
class AgentSpec:
    name: str
    mission: str
    prompt: str


@dataclass(frozen=True)
class AgentRun:
    name: str
    mission: str
    output: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    live: bool

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass(frozen=True)
class WorkflowResult:
    idea: str
    created_at: str
    runs: list[AgentRun]

    @property
    def total_tokens(self) -> int:
        return sum(run.total_tokens for run in self.runs)

    @property
    def live(self) -> bool:
        return any(run.live for run in self.runs)


AGENTS = [
    AgentSpec(
        name="Planner",
        mission="澄清用户、痛点、成功指标和 Token 使用场景。",
        prompt="# Planner\n你是产品规划 Agent，请用中文输出项目目标、用户、痛点和成功指标。",
    ),
    AgentSpec(
        name="Architect",
        mission="设计多 Agent 逻辑流、数据结构和可复现边界。",
        prompt="# Architect\n你是系统架构 Agent，请输出简洁架构、模块边界和数据流。",
    ),
    AgentSpec(
        name="Builder",
        mission="把架构转成可执行路线图和工程任务。",
        prompt="# Builder\n你是实现 Agent，请输出工程计划、关键命令和交付物。",
    ),
    AgentSpec(
        name="Reviewer",
        mission="审查夸大风险、复现风险和评审材料缺口。",
        prompt="# Reviewer\n你是审查 Agent，请指出风险、验证方式和需要补充的证明。",
    ),
    AgentSpec(
        name="Evidence Curator",
        mission="整理申请表可用叙述、证明包和截图点。",
        prompt="# Evidence Curator\n你是证明材料 Agent，请输出适合提交申请的成果摘要。",
    ),
]


def run_workflow(idea: str, client: LLMClient) -> WorkflowResult:
    runs: list[AgentRun] = []
    context = f"项目想法：{idea}"

    for agent in AGENTS:
        user = (
            f"{context}\n\n"
            "请基于前面 Agent 的输出继续推进，不要编造真实用户数、真实收入或未发生的生产落地。"
        )
        result: LLMResult = client.complete(agent.prompt, user)
        runs.append(
            AgentRun(
                name=agent.name,
                mission=agent.mission,
                output=result.content.strip(),
                model=result.model,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                latency_ms=result.latency_ms,
                live=result.live,
            )
        )
        context += f"\n\n[{agent.name}]\n{result.content.strip()}"

    return WorkflowResult(
        idea=idea,
        created_at=datetime.now(timezone.utc).isoformat(),
        runs=runs,
    )
