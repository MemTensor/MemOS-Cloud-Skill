# deleteMemory API

从 MemOS 删除记忆，支持按用户全部删除或按指定记忆 ID 删除。

## 端点

```
POST https://memos.memtensor.cn/api/openmem/v1/delete/memory
```

## 两种删除方式

| 方式 | 参数 | 效果 |
|------|------|------|
| 按用户删除 | `user_id` | 删除该用户所有记忆（事实、偏好、Skill、Tool 等） |
| 按 ID 删除 | `memory_ids` | 删除指定的一条或多条记忆 |

## 用法

### 删除用户所有记忆

```python
from memos.api.client import MemOSClient

client = MemOSClient(api_key="YOUR_API_KEY")

res = client.delete_memory(user_id="user_001")
print(res)
```

### 删除指定记忆

记忆 ID 来自 `search/memory` 或 `get/memory` 返回的 `id` 字段。

```python
res = client.delete_memory(
    memory_ids=["6b23b583-f4c4-4a8f-b345-58d0c48fea04"]
)
print(res)
```

### HTTP

```python
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://memos.memtensor.cn/api/openmem/v1"

# 按用户删除
data = {"user_id": "user_001"}

# 或按 ID 删除
data = {"memory_ids": ["6b23b583-f4c4-4a8f-b345-58d0c48fea04"]}

res = requests.post(
    f"{BASE_URL}/delete/memory",
    headers={"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"},
    json=data
)
print(res.json())
```

### cURL

```bash
# 按用户删除
curl "$MEMOS_BASE_URL/delete/memory" \
  -H "Authorization: Token $MEMOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001"}'

# 按 ID 删除
curl "$MEMOS_BASE_URL/delete/memory" \
  -H "Authorization: Token $MEMOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"memory_ids": ["6b23b583-f4c4-4a8f-b345-58d0c48fea04"]}'
```

## 返回

`"data.success": "true"` 表示删除成功。可再次调用 searchMemory 确认记忆已不被召回。
