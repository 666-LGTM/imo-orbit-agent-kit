# MiMo Orbit 申请材料草稿

下面内容可以按你的真实情况微调后提交。不要填写没有发生过的真实用户数、收入、生产部署规模。

## 04 项目成果描述

我构建了一个名为 `mimo-orbit-agent-kit` 的多 Agent 证明包生成器，核心痛点是：很多 AI Builder 在申请 Token Plan 时只有零散截图，无法系统证明自己确实在用 Agent 进行持续构建，也无法说明 Token 消耗会发生在哪些真实环节。

项目使用 Planner、Architect、Builder、Reviewer、Evidence Curator 五个 Agent 组成闭环工作流。用户输入一个产品想法后，Planner 先澄清目标用户、核心痛点和成功指标；Architect 设计模块边界和数据流；Builder 生成可执行工程路线；Reviewer 检查夸大陈述、复现风险和证明缺口；Evidence Curator 最后整理成申请表可用叙述、结构化 JSON、Markdown 摘要和可截图 HTML 演示页。

这个项目的价值是把“AI 构建过程”变成可复现证据：每次运行都会记录 Agent 名称、任务、模型、输入/输出 Token 估算、延迟和生成内容。没有 API key 时可用离线 mock 模式复现完整流程；配置 Xiaomi MiMo API key 后，可切换到 MiMo-V2.5-Pro 等模型进行真实运行。后续我计划把它接入 Claude Code / OpenClaw / Cursor 工作流，用 MiMo 的长上下文能力处理更大的代码仓库分析、PR 审查和项目文档生成。

## 05 使用证明与影响力证明

建议上传或填写：

- GitHub 项目链接：仓库主页。
- 运行截图：`reports/demo/index.html` 页面。
- 终端日志截图：运行 `orbit-agent-kit run ...` 后的输出。
- 结构化证明：`reports/demo/evidence.json`。
- 如果已有 MiMo API key，再补充 live 模式运行截图，说明模型名和 Token 估算。

## 更高通过率的小提示

- 在 README 顶部放一张运行截图或 GIF。
- GitHub 仓库保持公开，至少包含 README、可运行命令、测试和 CI。
- 申请描述里写清楚“痛点、工作流、Token 消耗原因、后续计划”。
- 只写真实发生的使用情况，把未来计划标注为“计划”。
