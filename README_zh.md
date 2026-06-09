# MemOS Cloud Skill

[English](README.md) | [中文](README_zh.md)

MemOS Cloud Server API 技能。该技能允许 Agent 或开发者直接调用 MemOS 云平台 API，实现记忆的检索、添加、删除、知识库管理以及反馈功能。

## 环境要求 (Prerequisites)

- **Python**: 3.x 及以上版本
- **Python 依赖**: `requests` 模块 (`pip3 install requests`)

## 安装与引入 (Install)

### 方式一：使用命令安装（推荐）

```bash
npx skills add https://github.com/MemTensor/MemOS-Cloud-Skill/memos-cloud-server
```

### 方式二：本地克隆并手动复制安装

1. 将本仓库克隆到本地：
    ```bash
    git clone https://github.com/MemTensor/MemOS-Cloud-Skill.git
    ```
2. 手动将技能文件夹复制到你对应的 agent 技能库目录或者使用命令安装：
    ```bash
    npx skills add ./MemOS-Cloud-Skill/memos-cloud-server
    ```

## 配置环境变量 (Environment Variables)

这是最重要的一步！在执行任何 API 操作前，你必须确保以下环境变量已经配置。

**环境变量配置位置**

- 你可以在系统环境变量中全局配置（例如 `~/.bashrc` 或 `~/.zshrc`）。
- 或者，你可以在特定的 AI Agent 或框架的环境设置中进行配置（例如，OpenClaw/Moltbot/Clawdbot 等框架支持读取 `.env` 文件）。

### 必填配置

- `MEMOS_API_KEY` (必填；Token 鉴权) — 在 [MemOS API 控制台](https://memos-dashboard.openmem.net/cn/apikeys/) 注册并获取。
- `MEMOS_USER_ID` (必填；确定性的用户自定义个人标识符，如邮箱哈希值或员工 ID) — **请不要使用随机值或聊天会话 ID 作为用户标识符。**

```env
MEMOS_API_KEY=你的_API_KEY
MEMOS_USER_ID=你的_USER_ID
```

### 可选配置

- `MEMOS_CLOUD_URL` — API 基础 URL（默认值: `https://memos.memtensor.cn/api/openmem/v1`）
- `MEMOS_AGENT_ID` — Agent 标识符（多 Agent 场景使用）
- `MEMOS_APP_ID` — 应用标识符（多应用场景使用）
- `MEMOS_ALLOW_PUBLIC` — 是否允许公共记忆访问，`true`/`false`（默认: `false`）
- `MEMOS_ASYNC_MODE` — 是否启用异步记忆添加，`true`/`false`（默认: `true`）

### 快速配置命令 (Shell 用户，如 Linux/macOS)

```bash
echo 'export MEMOS_API_KEY="mpg-..."' >> ~/.bashrc
echo 'export MEMOS_USER_ID="user-123"' >> ~/.bashrc
source ~/.bashrc
```

### 快速配置命令 (Windows PowerShell 用户)

```powershell
[System.Environment]::SetEnvironmentVariable("MEMOS_API_KEY", "mpg-...", "User")
[System.Environment]::SetEnvironmentVariable("MEMOS_USER_ID", "user-123", "User")
```

## 命令列表

### 1. 搜索记忆 (Search Memory)

```bash
python3 scripts/memos_cloud.py search [user_id] "<query>" [options]
```

选项: `--conversation-id`, `--conversation-first-message`, `--filter`, `--knowledgebase-ids`, `--memory-limit-number`, `--include-preference`, `--preference-limit-number`, `--include-tool-memory`, `--tool-memory-limit-number`, `--include-skill`, `--skill-limit-number`, `--relativity`

### 2. 添加记忆 (Add Message)

```bash
python3 scripts/memos_cloud.py add_message [user_id] [conversation_id] '<messages_json>' [options]
```

选项: `--conversation-first-message`, `--tags`, `--info`, `--allow-knowledgebase-ids`

### 3. 删除记忆 (Delete Memory)

```bash
python3 scripts/memos_cloud.py delete "id1,id2,id3"
```

### 4. 添加反馈 (Add Feedback)

```bash
python3 scripts/memos_cloud.py add_feedback [user_id] <conversation_id> "<feedback>" [options]
```

选项: `--allow-knowledgebase-ids`, `--feedback-time`

### 5. 上传知识库文档 (Add Knowledge Base Document)

```bash
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> <file1> [file2 ...] [--type document|skill]
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> --stdin [--name filename.ext] [--type document|skill]
```

### 6. 获取用户画像 (Get User Profile)

```bash
python3 scripts/memos_cloud.py get_user_profile [user_id] [options]
```

选项: `--page`, `--size`, `--filter`, `--include-preference`, `--include-tool-memory`

### 7. 创建知识库 (Create Knowledge Base)

```bash
python3 scripts/memos_cloud.py create_kb "<name>" [--description "<desc>"]
```

### 8. 获取知识库文件 (Get Knowledge Base Documents)

两种模式（互斥）:

```bash
python3 scripts/memos_cloud.py get_kb_docs --file-ids "id1,id2"
python3 scripts/memos_cloud.py get_kb_docs --knowledgebase-id "kb-1" [--type document|skill] [--page 1] [--page-size 20]
```

### 9. 删除知识库文件 (Delete Knowledge Base Documents)

```bash
python3 scripts/memos_cloud.py delete_kb_docs "file-id-1,file-id-2"
```

### 10. 移除知识库 (Remove Knowledge Base)

```bash
python3 scripts/memos_cloud.py remove_kb "kb-123"
```

## 交互示例

### 添加记忆

- **用户：** "请记住，我平时开发首选语言是 Python，喜欢用深色主题。"
- **Agent：** _(识别意图 -> 自动调用 `add_message` 技能)_ "好的，我已经记住了您关于 Python 和深色主题的偏好。"

### 搜索记忆

- **用户：** "根据我常用的技术栈写一段初始化的模板代码。"
- **Agent：** _(识别意图 -> 自动调用 `search` 技能)_ "没问题！根据您的偏好，这里是一份 Python 的初始化模板代码……"

### 删除记忆

- **用户：** "忘记我之前的居住地址，我已经搬家了。"
- **Agent：** _(识别意图 -> 自动调用 `delete` 技能)_ "明白，我已经从记忆中删除了您的旧地址信息。"

### 反馈纠正

- **用户：** "刚才的回答不够详细，以后请记得多加一些代码注释。"
- **Agent：** _(识别意图 -> 自动调用 `add_feedback` 技能)_ "收到，今后的代码我会提供更详细的注释说明。"
