# addFeedback API

通过自然语言反馈修正和更新记忆，无需手动定位具体记忆条目。

## 端点

```
POST https://memos.memtensor.cn/api/openmem/v1/add/feedback
```

## 必要参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `user_id` | string | 用户唯一标识 |
| `conversation_id` | string | 提供上下文的会话标识 |
| `feedback_content` | string | 自然语言反馈内容 |

## 可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `allow_knowledgebase_ids` | array | 允许反馈写入的知识库 ID 列表 |

## 工作原理

1. **有效性分析**：结合当前对话上下文判断反馈是否有效
2. **更新类型识别**：判定是关键词替换还是语义更新
3. **记忆更新**：写入新记忆并更新/覆盖冲突的旧记忆

## 用法

### 语义修正

```python
from memos.api.client import MemOSClient

client = MemOSClient(api_key="YOUR_API_KEY")

res = client.add_feedback(
    user_id="user_001",
    conversation_id="feedback_conv",
    feedback_content="办公软件采购限额是600元，不是800元。",
    allow_knowledgebase_ids=["kb_xxx"]
)
print(res)
```

### 关键词替换

```python
res = client.add_feedback(
    user_id="user_001",
    conversation_id="feedback_conv",
    feedback_content="以后我改名了，把所有的「用户1」替换成「用户2」"
)
```

### HTTP

```python
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://memos.memtensor.cn/api/openmem/v1"

data = {
    "user_id": "user_001",
    "conversation_id": "feedback_conv",
    "feedback_content": "办公软件采购限额是600元，不是800元。",
    "allow_knowledgebase_ids": ["kb_xxx"]
}

res = requests.post(
    f"{BASE_URL}/add/feedback",
    headers={"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"},
    json=data
)
print(res.json())
```

## 适用场景

| 场景 | 示例反馈 |
|------|---------|
| 纠正错误事实 | "我的生日是3月15日，不是3月5日" |
| 更新过时信息 | "我已经从上海搬到北京了" |
| 修正知识库内容 | "报销标准已更新为新版本" |
| 全局关键词替换 | "把所有的A替换成B" |
