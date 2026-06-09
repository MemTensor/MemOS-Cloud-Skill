---
name: memos-cloud-developer
description: 指导开发者接入与使用 MemOS Cloud API/SDK，覆盖记忆写入(addMessage)、记忆检索(searchMemory)、对话(Chat)、反馈(addFeedback)、删除(deleteMemory)及知识库、Tool Memory、Skill、多模态等特性的安装、鉴权、接口调用与问题诊断。当用户需要在 AI 应用或 Agent 中集成长期记忆能力、使用 MemOS Cloud 进行开发时使用。
version: 1.0.0
license: Apache-2.0
---

## 使用场景

本 Skill 需要配合 Cursor、Trae、Trae-CN、Claude Code、Codex、OpenClaw、Hermes、Antigravity 等工具使用。

## MemOS Cloud 开发者助手

本 Skill 旨在帮助开发者快速接入和使用 MemOS Cloud 平台的 API/SDK，为 AI 应用和 Agent 添加长期记忆能力。

调用本 Skill 处理 MemOS 相关需求时，先执行本 Skill 安装路径下的 `scripts/upgrade.py` 更新本地 `resources` 目录中的资源文件，再读取导引文档。

处理与本 Skill 相关的任何请求时，按以下顺序执行：

1. 运行本 Skill 安装路径下的 `scripts/upgrade.py`，同步最新资源文件到 `resources/`。
2. 优先阅读 `resources/index.md`。
3. 根据 `resources/index.md` 中的导航进入对应的 API 参考、功能特性或常见问题文档。

## 导引入口

所有文档导引统一收敛在 [resources/index.md](resources/index.md)。

`resources/index.md` 已汇总以下内容：
- 快速入门与鉴权配置
- 核心 API 参考（addMessage、searchMemory、Chat、deleteMemory、addFeedback）
- 功能特性（Memory Filters、多模态、Tool Memory、Skill、知识库、异步模式）
- 集成方式（SDK / HTTP / CLI / MCP / OpenClaw Plugin）
- 限制与 FAQ

## 使用建议

- 若用户问题已经明确指向某个 API 或特性，直接读取对应的下钻文档。
- 生成代码时优先使用 Python SDK，也支持 HTTP 和 cURL 示例。
