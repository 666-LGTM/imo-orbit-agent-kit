# mimo-orbit-agent-kit

一个面向 Xiaomi MiMo Orbit 100T Token 创造者激励计划的多 Agent 项目模板。

它把一个产品想法拆成「需求澄清 -> 架构设计 -> 实现计划 -> 风险审查 -> 证明包」五步，并生成可提交的 GitHub 项目材料、运行日志、Token 预算和本地演示页。默认使用离线 mock 模式，方便任何评审者直接复现；配置 `XIAOMI_MIMO_API_KEY` 后可切换到 Xiaomi MiMo API。

在线可视化演示：https://666-lgtm.github.io/imo-orbit-agent-kit/

## 解决的核心痛点

很多 AI Builder 在申请 Token Plan 时只有截图或零散描述，很难证明：

- 项目确实由 Agent 或 AI 工作流驱动；
- 工作流是否包含长链路推理、多 Agent 协作和闭环审查；
- Token 使用场景是否真实、高频、可持续；
- GitHub 链接打开后能否快速看到成果。

本项目把这些证明材料自动化生成，让申请内容更具体、更可信、更容易复现。

## 核心能力

- 多 Agent 编排：Planner、Architect、Builder、Reviewer、Evidence Curator。
- MiMo 兼容调用：支持 OpenAI-compatible Chat Completions 接口。
- Token 预算：估算每个 Agent 的输入、输出和总消耗，形成额度申请依据。
- 证明包生成：输出 `summary.md`、`evidence.json` 和可截图的 `index.html`。
- 离线可跑：没有 API key 时使用 deterministic mock，方便 GitHub Actions 和评审复现。
- CI 验证：自带单元测试和 GitHub Actions。

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m orbit_agent_kit.cli run --idea "为独立开发者自动生成小米 MiMo Token 申请证明包" --out reports/demo
python -m orbit_agent_kit.cli serve --dir reports/demo --port 8765
```

打开：

```text
http://127.0.0.1:8765
```

## 使用 Xiaomi MiMo API

```bash
export XIAOMI_MIMO_API_KEY="你的 key"
export MIMO_BASE_URL="https://api.xiaomimimo.com/v1"
export MIMO_MODEL="mimo-v2.5-pro"
python -m orbit_agent_kit.cli run --idea "你的真实项目想法" --out reports/live --live
```

不想创建虚拟环境时，也可以直接运行：

```bash
PYTHONPATH=src python3 -m orbit_agent_kit.cli run --idea "你的真实项目想法" --out reports/demo
```

如果你的 Token Plan 提供的是 Anthropic-compatible endpoint，可以继续用 Claude Code、OpenClaw 等工具跑主项目；本仓库的 CLI 主要演示 OpenAI-compatible 调用和证明材料生成。

## 生成物

运行后会得到：

```text
reports/demo/
  evidence.json   # 结构化证明、Agent 步骤、Token 估算
  summary.md      # 可复制到申请表或 README 的成果描述
  index.html      # 可截图提交的演示页
```

## 适合提交到申请表的描述

见 [docs/APPLY.md](docs/APPLY.md)。

## 项目结构

```text
src/orbit_agent_kit/
  agents.py       # 多 Agent 工作流
  cli.py          # 命令行入口
  config.py       # MiMo 配置
  llm.py          # API client 和 mock client
  report.py       # 证明包生成
  server.py       # 本地演示服务
tests/
docs/
examples/
```

## License

MIT
