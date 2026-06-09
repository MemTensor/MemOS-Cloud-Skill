# 集成指南

MemOS Cloud 提供多种接入方式，根据你的开发场景选择最合适的集成路径。

## 集成方式对比

| 集成方式 | 最适合 | 优先级 |
|---------|--------|--------|
| OpenClaw Plugin | OpenClaw 等深度集成 MemOS 的 Agent 环境 | 自动化程度最高 |
| CLI + Skill | 任何可执行 Shell 的 Agent 框架 | 最通用，跨框架 |
| MCP | Cursor, Claude Desktop, Cline, Chatbox 等 AI 客户端 | 客户端支持 MCP 时使用 |
| API / SDK | 自建 Agent、聊天机器人、业务应用 | 控制力最强，适合生产集成 |

---

## 1. Python SDK / HTTP 直调

最灵活的方式，适合自建 Agent 和业务应用。

### 安装

```bash
pip install MemoryOS -U
```

### 使用

```python
from memos.api.client import MemOSClient

client = MemOSClient(api_key="YOUR_API_KEY")

# 写入
client.add_message(messages=[...], user_id="...", conversation_id="...")

# 检索
result = client.search_memory(query="...", user_id="...")
```

详见 [快速入门](quick-start.md) 和各 API 文档。

---

## 2. CLI + Skill

适合 Cursor、Claude Code、Codex、Hermes 等可执行 Shell 命令的 Agent。

### 安装 CLI

```bash
npm install -g @memtensor/memos-cloud-cli
```

### 初始化并安装 Skill

```bash
memos init --api-key YOUR_API_KEY --agent cursor
```

支持的 `--agent` 目标：

| Agent | Skill 安装路径 |
|-------|---------------|
| `cursor` | `~/.cursor/skills/memos/` |
| `codex` | `~/.codex/skills/memos/` |
| `claude` | `~/.claude/skills/memos/` |
| `openclaw` | `~/.openclaw/skills/memos/` |
| `hermes` | `~/.hermes/skills/memos/` |

### 安装后的行为

Agent 自动在每轮对话中：
1. **回答前**：`memos search` 检索相关记忆
2. **回答后**：`memos add` 写入新的事实/偏好

---

## 3. MCP

适合 Cursor、Claude Desktop、Cline、Chatbox 等支持 MCP 的客户端。

### 配置（以 Cursor 为例）

在 `mcp.json` 中添加：

```json
{
  "mcpServers": {
    "memos-api-mcp": {
      "timeout": 60,
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@memtensor/memos-api-mcp@latest"],
      "env": {
        "MEMOS_API_KEY": "YOUR_API_KEY",
        "MEMOS_USER_ID": "your-user-id",
        "MEMOS_CHANNEL": "MODELSCOPE"
      }
    }
  }
}
```

### 配合 Cursor Rules 使用

```text
Before answering the user's question, call MemOS search_memory to search long-term memories.
After answering, if this turn contains new user facts or preferences, call add_message to write into MemOS.
Only use memories relevant to the current task.
Do not expose internal details like "memory store" to the user.
```

---

## 4. OpenClaw Plugin

适合使用 OpenClaw 的开发者，自动化程度最高。

### 配置 API Key

```bash
mkdir -p ~/.openclaw
echo 'MEMOS_API_KEY=YOUR_API_KEY' >> ~/.openclaw/.env
```

### 安装插件

```bash
openclaw plugins install @memtensor/memos-cloud-openclaw-plugin@latest
openclaw gateway restart
```

### 确认启用

检查 `~/.openclaw/openclaw.json`：

```json
{
  "plugins": {
    "entries": {
      "memos-cloud-openclaw-plugin": {"enabled": true}
    }
  }
}
```

安装后 OpenClaw 会自动在对话中记忆和召回用户信息。
