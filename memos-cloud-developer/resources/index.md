# MemOS Cloud 开发者文档导引

本文件是 `memos-cloud-developer` Skill 的统一导引首页。

处理本 Skill 相关的任何需求时，优先从这里选择对应的 API、功能特性或专题文档，再继续深入阅读具体资源。

## 使用方式

- 需要接入 API/SDK 时，从「核心 API」章节进入对应文档。
- 需要了解高级特性时，从「功能特性」章节进入。
- 需要查看集成方式时，参考「集成指南」章节。
- 遇到问题时，查看「FAQ 与限制」章节。

---

## 1. 快速入门

环境准备、鉴权配置、第一个记忆操作。

- [快速入门指南](quick-start.md)

---

## 2. 核心 API

MemOS Cloud 的核心记忆操作接口。

| API | 用途 | 文档 |
|-----|------|------|
| addMessage | 写入对话/信息，自动生产记忆 | [api-add-message.md](api-add-message.md) |
| searchMemory | 检索与查询相关的记忆 | [api-search-memory.md](api-search-memory.md) |
| Chat | 内置记忆管理的对话（自动召回+生成回复） | [api-chat.md](api-chat.md) |
| deleteMemory | 按用户或记忆 ID 删除记忆 | [api-delete-memory.md](api-delete-memory.md) |
| addFeedback | 自然语言反馈修正记忆 | [api-add-feedback.md](api-add-feedback.md) |

---

## 3. 功能特性

扩展记忆能力的高级特性。

| 特性 | 说明 | 文档 |
|------|------|------|
| Memory Filters | 按标签/时间/Agent/业务字段精确筛选记忆 | [features-filters.md](features-filters.md) |
| 多模态 | 支持图片、文档等非文本输入 | [features-multimodal.md](features-multimodal.md) |
| Tool Memory | 将工具调用决策和结果沉淀为可检索记忆 | [features-tool-memory.md](features-tool-memory.md) |
| Skill | 自动生成或上传可复用的任务处理方法 | [features-skill.md](features-skill.md) |
| 知识库 | 上传文档建立知识库，与用户记忆联合检索 | [features-knowledge-base.md](features-knowledge-base.md) |
| 异步模式 | 控制消息写入后的处理时机 | [features-async-mode.md](features-async-mode.md) |

---

## 4. 集成指南

将 MemOS Cloud 集成到你的 Agent 产品中。

- [集成指南](integration-guide.md)
  - Python SDK（推荐）
  - HTTP 直调
  - cURL
  - Agent Loop 集成架构

---

## 5. FAQ 与限制

- [常见问题 & 资源限制](faq-and-limits.md)
