from __future__ import annotations

import html
import json
from pathlib import Path

from .agents import WorkflowResult


def write_report(result: WorkflowResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "evidence.json").write_text(
        json.dumps(_to_dict(result), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "summary.md").write_text(_summary_markdown(result), encoding="utf-8")
    (out_dir / "index.html").write_text(_html(result), encoding="utf-8")


def _to_dict(result: WorkflowResult) -> dict:
    return {
        "idea": result.idea,
        "created_at": result.created_at,
        "live": result.live,
        "total_tokens": result.total_tokens,
        "agents": [
            {
                "name": run.name,
                "mission": run.mission,
                "output": run.output,
                "model": run.model,
                "input_tokens": run.input_tokens,
                "output_tokens": run.output_tokens,
                "total_tokens": run.total_tokens,
                "latency_ms": run.latency_ms,
                "live": run.live,
            }
            for run in result.runs
        ],
    }


def _summary_markdown(result: WorkflowResult) -> str:
    lines = [
        "# MiMo Orbit Agent Kit 运行摘要",
        "",
        f"- 项目想法：{result.idea}",
        f"- 运行模式：{'MiMo live API' if result.live else '离线 mock，可复现演示'}",
        f"- Agent 数量：{len(result.runs)}",
        f"- 估算 Token：{result.total_tokens:,}",
        "",
        "## 多 Agent 逻辑流",
        "",
    ]
    for index, run in enumerate(result.runs, start=1):
        lines.extend(
            [
                f"### {index}. {run.name}",
                "",
                f"任务：{run.mission}",
                "",
                run.output,
                "",
                f"Token：输入 {run.input_tokens:,} / 输出 {run.output_tokens:,} / 合计 {run.total_tokens:,}",
                "",
            ]
        )
    lines.extend(
        [
            "## 可提交证明",
            "",
            "- GitHub README 展示项目目标、核心痛点和运行命令。",
            "- `evidence.json` 保留每个 Agent 的输出、模型、延迟和 Token 估算。",
            "- `index.html` 可作为申请表截图或在线演示页。",
        ]
    )
    return "\n".join(lines) + "\n"


def _html(result: WorkflowResult) -> str:
    cards = "\n".join(
        f"""
        <article class="agent">
          <div class="agent-head">
            <h2>{html.escape(run.name)}</h2>
            <span>{run.total_tokens:,} tokens</span>
          </div>
          <p class="mission">{html.escape(run.mission)}</p>
          <pre>{html.escape(run.output)}</pre>
        </article>
        """
        for run in result.runs
    )
    mode = "MiMo live API" if result.live else "Offline mock"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MiMo Orbit Agent Kit Evidence</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #171717;
      --muted: #62615d;
      --line: #ddd8cd;
      --paper: #f8f5ed;
      --panel: #ffffff;
      --accent: #ff6900;
      --teal: #0f766e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
    }}
    main {{ width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 32px 0 48px; }}
    header {{
      min-height: 340px;
      display: grid;
      align-content: center;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{ color: var(--accent); font-weight: 700; letter-spacing: 0; }}
    h1 {{ margin: 12px 0 16px; font-size: clamp(40px, 7vw, 82px); line-height: 0.95; letter-spacing: 0; max-width: 900px; }}
    .lead {{ max-width: 760px; color: var(--muted); font-size: 20px; line-height: 1.65; }}
    .stats {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 28px 0; }}
    .stat {{ border: 1px solid var(--line); background: var(--panel); padding: 18px; border-radius: 8px; }}
    .stat b {{ display: block; font-size: 28px; }}
    .stat span {{ color: var(--muted); }}
    .agent {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 20px; margin: 14px 0; }}
    .agent-head {{ display: flex; justify-content: space-between; gap: 16px; align-items: center; }}
    h2 {{ margin: 0; font-size: 22px; }}
    .agent-head span {{ color: var(--teal); font-weight: 700; white-space: nowrap; }}
    .mission {{ color: var(--muted); }}
    pre {{ white-space: pre-wrap; word-break: break-word; font: inherit; line-height: 1.65; margin: 0; }}
    footer {{ color: var(--muted); border-top: 1px solid var(--line); margin-top: 28px; padding-top: 18px; }}
    @media (max-width: 720px) {{
      main {{ width: min(100% - 24px, 1120px); padding-top: 18px; }}
      .stats {{ grid-template-columns: 1fr; }}
      .agent-head {{ align-items: flex-start; flex-direction: column; }}
      h1 {{ font-size: 42px; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">Xiaomi MiMo Orbit Evidence Pack</div>
      <h1>Multi-Agent Proof Builder</h1>
      <p class="lead">{html.escape(result.idea)}</p>
    </header>
    <section class="stats" aria-label="Run statistics">
      <div class="stat"><b>{len(result.runs)}</b><span>Agents</span></div>
      <div class="stat"><b>{result.total_tokens:,}</b><span>Estimated tokens</span></div>
      <div class="stat"><b>{html.escape(mode)}</b><span>Run mode</span></div>
    </section>
    <section>{cards}</section>
    <footer>Generated at {html.escape(result.created_at)}. Outputs are reproducible and separated from unverified production claims.</footer>
  </main>
</body>
</html>
"""
