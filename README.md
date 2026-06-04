# MemOS Cloud Skill

[English](README.md) | [中文](README_zh.md)

MemOS Cloud Server API skill. This skill allows Agents or developers to directly call the MemOS Cloud Platform API to retrieve, add, delete, upload, and feedback on memories.

## Prerequisites

- **Python**: 3.x and above
- **Python Dependencies**: `requests` module (`pip3 install requests`)

## Install

### Option A — Command Line (Recommended)

Install from GitHub:

```bash
npx skills add https://github.com/MemTensor/MemOS-Cloud-Skill/memos-cloud-server
```

### Option B — Local Path

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/MemTensor/MemOS-Cloud-Skill.git
    ```
2. Install from the local skill directory:
    ```bash
    npx skills add ./MemOS-Cloud-Skill/memos-cloud-server
    ```

## Environment Variables

This step is critical. You must configure these variables before using the skill.

**Where to configure**

- You can configure these globally in your system environment (e.g., `~/.bashrc`, `~/.zshrc`).
- Or, you can configure them within your specific AI Agent or framework's environment settings (e.g., `.env` files for OpenClaw/Moltbot/Clawdbot).

### Required

- `MEMOS_API_KEY` (required; Token auth) — get it at [MemOS API Console](https://memos-dashboard.openmem.net/cn/apikeys/)
- `MEMOS_USER_ID` (required; A deterministic user-defined personal identifier, e.g., hashed email, employee ID) — **Do not use random or session IDs.**

```env
MEMOS_API_KEY=YOUR_TOKEN
MEMOS_USER_ID=YOUR_USER_ID
```

### Optional

- `MEMOS_CLOUD_URL` — API base URL (default: `https://memos.memtensor.cn/api/openmem/v1`)
- `MEMOS_AGENT_ID` — Agent identifier for multi-agent scenarios
- `MEMOS_APP_ID` — Application identifier for multi-app scenarios
- `MEMOS_ALLOW_PUBLIC` — Allow public memory access, `true`/`false` (default: `false`)
- `MEMOS_ASYNC_MODE` — Enable async memory addition, `true`/`false` (default: `true`)

```env
MEMOS_CLOUD_URL=https://memos.memtensor.cn/api/openmem/v1
MEMOS_AGENT_ID=your-agent-id
MEMOS_APP_ID=your-app-id
MEMOS_ALLOW_PUBLIC=false
MEMOS_ASYNC_MODE=true
```

### Quick setup (shell)

```bash
echo 'export MEMOS_API_KEY="mpg-..."' >> ~/.bashrc
echo 'export MEMOS_USER_ID="user-123"' >> ~/.bashrc
source ~/.bashrc
```

### Quick setup (Windows PowerShell)

```powershell
[System.Environment]::SetEnvironmentVariable("MEMOS_API_KEY", "mpg-...", "User")
[System.Environment]::SetEnvironmentVariable("MEMOS_USER_ID", "user-123", "User")
```

## Commands

### 1. Search Memory

Search for long-term memories relevant to a query.

```bash
python3 scripts/memos_cloud.py search [user_id] "<query>" [options]
```

Options: `--conversation-id`, `--conversation-first-message`, `--filter`, `--knowledgebase-ids`, `--memory-limit-number`, `--include-preference`, `--preference-limit-number`, `--include-tool-memory`, `--tool-memory-limit-number`, `--include-skill`, `--skill-limit-number`, `--relativity`

### 2. Add Message

Store high-value content from conversations.

```bash
python3 scripts/memos_cloud.py add_message [user_id] [conversation_id] '<messages_json>' [options]
```

Options: `--conversation-first-message`, `--tags`, `--info`, `--allow-knowledgebase-ids`

### 3. Delete Memory

Delete stored memories by IDs.

```bash
python3 scripts/memos_cloud.py delete "id1,id2,id3"
```

### 4. Add Feedback

Add feedback to correct or reinforce memory.

```bash
python3 scripts/memos_cloud.py add_feedback [user_id] <conversation_id> "<feedback>" [options]
```

Options: `--allow-knowledgebase-ids`, `--feedback-time`

### 5. Add Knowledge Base Document

Upload files to a knowledge base.

```bash
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> <file1> [file2 ...] [--type document|skill]
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> --stdin [--name filename.ext] [--type document|skill]
```

### 6. Get User Profile

Retrieve the consolidated User Memory Profile.

```bash
python3 scripts/memos_cloud.py get_user_profile [user_id] [options]
```

Options: `--page`, `--size`, `--filter`, `--include-preference`, `--include-tool-memory`

### 7. Create Knowledge Base

Create a named container for structured documents.

```bash
python3 scripts/memos_cloud.py create_kb "<name>" [--description "<desc>"]
```

### 8. Get Knowledge Base Documents

Get document metadata/details. Two modes (mutually exclusive):

```bash
python3 scripts/memos_cloud.py get_kb_docs --file-ids "id1,id2"
python3 scripts/memos_cloud.py get_kb_docs --knowledgebase-id "kb-1" [--type document|skill] [--page 1] [--page-size 20]
```

### 9. Delete Knowledge Base Documents

Delete documents from a knowledge base.

```bash
python3 scripts/memos_cloud.py delete_kb_docs "file-id-1,file-id-2"
```

### 10. Remove Knowledge Base

Remove a knowledge base from the project.

```bash
python3 scripts/memos_cloud.py remove_kb "kb-123"
```

## Direct Script Usage

For repository-local testing before installation:

```bash
python3 memos-cloud-server/scripts/memos_cloud.py --help
```
