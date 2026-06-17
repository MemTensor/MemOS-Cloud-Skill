# MemOS Cloud Developer Skill

为 AI 应用接入 MemOS Cloud 长期记忆的开发者 Skill。

## 安装

```bash
npx skills add https://github.com/MemTensor/MemOS-Cloud-Skill --skill memos-cloud-developer -g -y
```

## 使用

将以下 prompt 复制到你的 AI Agent（Codex、Cursor、Claude Code、Trae、OpenClaw 等）聊天框中：

### Prompt：为项目接入 MemOS Cloud 记忆

```text
帮我为本项目接入 MemOS Cloud，为我的 Agent 产品添加长期记忆能力。

请按以下步骤操作：

1. 安装 memos-cloud-developer Skill（如已安装则跳过）：
   npx skills add https://github.com/MemTensor/MemOS-Cloud-Skill --skill memos-cloud-developer -g -y
   根据当前 Agent 环境自动填充 --agent 参数。

2. 读取该 Skill 安装路径下的 SKILL.md，严格按照其中的指令顺序执行。

3. 验证连通性：
   检查环境变量 MEMOS_API_KEY 是否已存在且以 mpg- 开头。
   如果有，用 memos CLI 或 cURL 执行一次 add + search 闭环验证；
   如果没有，引导我去 https://memos-dashboard.openmem.net/cn/quickstart 获取 Key 并配置。

4. 结合本项目的实际技术栈和架构，生成完整的 MemOS Cloud 集成代码。
```

## API Key 获取

前往 [MemOS Dashboard](https://memos-dashboard.openmem.net/cn/quickstart) 注册并获取 API Key（格式：`mpg-...`）。
