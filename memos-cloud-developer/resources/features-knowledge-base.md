# 知识库

创建项目级知识库，上传文档建立知识记忆，与用户个人记忆联合检索。

## 与传统 RAG 的区别

| 维度 | 传统 RAG | MemOS 知识库 |
|------|---------|-------------|
| 准确性 | 语料越多噪声越大 | 结构化提取+生命周期管理 |
| 结果形态 | 原始文本段落 | 精炼的记忆单元 |
| 检索范围 | 全量语料扫描 | 分层调度，精准命中 |
| 理解能力 | 仅相似度匹配 | 结合用户偏好理解 |
| 进化能力 | 静态 | 通过反馈和对话动态更新 |

## 创建知识库

### 通过控制台

在 [Dashboard - 知识库](https://memos-dashboard.openmem.net/knowledgeBase/) 页面创建。

### 通过 API

```python
import requests

data = {
    "name": "企业政策知识库",
    "description": "包含公司各项政策和流程文档"
}

res = requests.post(
    f"{BASE_URL}/create/knowledgebase",
    headers={"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"},
    json=data
)
kb_id = res.json()["data"]["knowledgebase_id"]
```

## 上传文档

```python
data = {
    "knowledgebase_id": kb_id,
    "file": [
        {
            "type": "doc",
            "content": "https://example.com/policy.pdf"
        }
    ]
}

res = requests.post(
    f"{BASE_URL}/add/knowledgebase-file",
    headers={"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"},
    json=data
)
```

支持的文档类型：PDF, DOCX, DOC, TXT, JSON, MD, XML

也支持上传 Skill 文件（type 设为 `"skill"`），参见 [features-skill.md](features-skill.md)。

## 联合检索

在 searchMemory 中指定 `knowledgebase_ids`：

```python
data = {
    "user_id": "user_001",
    "query": "公司差旅报销标准是什么？",
    "knowledgebase_ids": ["kb_xxx"]
}

res = requests.post(
    f"{BASE_URL}/search/memory",
    headers={"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"},
    json=data
)
```

MemOS 会同时检索：
- 用户个人记忆（如"用户用 Intel MacBook Pro"）
- 知识库记忆（如"安装步骤"）

两者结合生成更精准的回答。

## 在 Chat API 中使用

```python
data = {
    "user_id": "user_001",
    "conversation_id": "conv_001",
    "query": "内网代理打不开了，该装哪个版本？",
    "knowledgebase_ids": ["kb_xxx"]
}

res = requests.post(
    f"{BASE_URL}/chat",
    headers={"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"},
    json=data
)
```

## 通过反馈更新知识库

使用 `addFeedback` + `allow_knowledgebase_ids` 可以通过自然语言更新知识库中的记忆：

```python
data = {
    "user_id": "user_001",
    "conversation_id": "feedback",
    "feedback_content": "报销标准已改为新版，办公软件限额600元",
    "allow_knowledgebase_ids": ["kb_xxx"]
}
```

## 文档上传限制

- 支持类型：PDF, DOCX, DOC, TXT, JSON, MD, XML
- 单文件大小：≤ 100 MB，≤ 500 页
- 单次上传：≤ 20 个文件
- Skill 文件：.md ≤ 100KB 或 .zip ≤ 20MB
