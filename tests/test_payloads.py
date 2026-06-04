import pytest

from memos_cloud.errors import ValidationError
from memos_cloud.payloads import (
    add_feedback_payload,
    add_message_payload,
    create_knowledge_base_payload,
    delete_kb_documents_payload,
    delete_memory_payload,
    generate_conversation_id,
    get_kb_documents_payload,
    get_user_profile_payload,
    remove_knowledge_base_payload,
    resolve_conversation_id,
    search_memory_payload,
)


def test_search_memory_payload_omits_empty_conversation_id():
    assert search_memory_payload("user-1", "query") == {
        "user_id": "user-1",
        "query": "query",
    }


def test_search_memory_payload_includes_conversation_id():
    assert search_memory_payload("user-1", "query", "conv-1") == {
        "user_id": "user-1",
        "query": "query",
        "conversation_id": "conv-1",
    }


def test_add_message_payload_parses_json_messages():
    assert add_message_payload(
        "user-1",
        "conv-1",
        '[{"role":"user","content":"hello"}]',
    ) == {
        "user_id": "user-1",
        "conversation_id": "conv-1",
        "messages": [{"role": "user", "content": "hello"}],
    }


def test_add_message_payload_rejects_invalid_json():
    with pytest.raises(ValidationError, match="messages must be a valid JSON string"):
        add_message_payload("user-1", "conv-1", "not-json")


def test_delete_memory_payload_parses_csv():
    assert delete_memory_payload(" id1, id2 ,, id3 ") == {
        "memory_ids": ["id1", "id2", "id3"],
    }


def test_delete_memory_payload_requires_ids():
    with pytest.raises(ValidationError, match="memory_ids is required"):
        delete_memory_payload("")


def test_add_feedback_payload_preserves_legacy_csv_shape():
    assert add_feedback_payload("user-1", "conv-1", "feedback", " kb1, kb2 ") == {
        "user_id": "user-1",
        "conversation_id": "conv-1",
        "feedback_content": "feedback",
        "allow_knowledgebase_ids": ["kb1", "kb2"],
    }


# conversation_id generation tests

def test_generate_conversation_id_is_deterministic():
    cid1 = generate_conversation_id("user-1", "first message")
    cid2 = generate_conversation_id("user-1", "first message")
    assert cid1 == cid2
    assert len(cid1) == 32  # MD5 hex length


def test_generate_conversation_id_differs_by_user():
    cid1 = generate_conversation_id("user-1", "first message")
    cid2 = generate_conversation_id("user-2", "first message")
    assert cid1 != cid2


def test_resolve_conversation_id_prefers_explicit():
    assert resolve_conversation_id("u", "conv-1", "first msg") == "conv-1"


def test_resolve_conversation_id_generates_from_first_message():
    cid = resolve_conversation_id("user-1", None, "first msg")
    assert cid == generate_conversation_id("user-1", "first msg")


def test_resolve_conversation_id_returns_none_when_neither():
    assert resolve_conversation_id("u", None, None) is None


# search_memory enhanced tests

def test_search_memory_payload_with_all_params():
    payload = search_memory_payload(
        "user-1", "query",
        filter_obj={"and": [{"agent_id": "a1"}]},
        knowledgebase_ids="kb1,kb2",
        memory_limit_number=10,
        include_preference=False,
        preference_limit_number=5,
        include_tool_memory=True,
        tool_memory_limit_number=3,
        include_skill=True,
        skill_limit_number=4,
        relativity=0.5,
    )
    assert payload["filter"] == {"and": [{"agent_id": "a1"}]}
    assert payload["knowledgebase_ids"] == ["kb1", "kb2"]
    assert payload["memory_limit_number"] == 10
    assert payload["include_preference"] is False
    assert payload["include_tool_memory"] is True
    assert payload["include_skill"] is True
    assert payload["relativity"] == 0.5


def test_search_memory_payload_knowledgebase_all():
    payload = search_memory_payload("u", "q", knowledgebase_ids="all")
    assert payload["knowledgebase_ids"] == ["all"]


# add_message enhanced tests

def test_add_message_payload_with_optional_fields():
    payload = add_message_payload(
        "user-1", "conv-1", '[{"role":"user","content":"hi"}]',
        agent_id="a1", app_id="app1", tags="t1,t2",
        info_json='{"key":"val"}', allow_public=True,
        allow_knowledgebase_ids="kb1", async_mode=False,
    )
    assert payload["agent_id"] == "a1"
    assert payload["app_id"] == "app1"
    assert payload["tags"] == ["t1", "t2"]
    assert payload["info"] == {"key": "val"}
    assert payload["allow_public"] is True
    assert payload["allow_knowledgebase_ids"] == ["kb1"]
    assert payload["async_mode"] is False


# add_feedback enhanced tests

def test_add_feedback_payload_with_optional_fields():
    payload = add_feedback_payload(
        "u", "c", "fb", agent_id="a1", app_id="app1",
        feedback_time="2026-01-01", allow_public=True,
    )
    assert payload["agent_id"] == "a1"
    assert payload["app_id"] == "app1"
    assert payload["feedback_time"] == "2026-01-01"
    assert payload["allow_public"] is True


# new payload function tests

def test_get_user_profile_payload_basic():
    assert get_user_profile_payload("user-1") == {"user_id": "user-1"}


def test_get_user_profile_payload_with_all_params():
    payload = get_user_profile_payload(
        "u", page=2, size=20, filter_obj={"and": [{"agent_id": "a"}]},
        include_preference=False, include_tool_memory=True,
    )
    assert payload["page"] == 2
    assert payload["size"] == 20
    assert payload["filter"] == {"and": [{"agent_id": "a"}]}
    assert payload["include_preference"] is False
    assert payload["include_tool_memory"] is True


def test_create_knowledge_base_payload():
    assert create_knowledge_base_payload("my-kb", "description") == {
        "knowledgebase_name": "my-kb",
        "knowledgebase_description": "description",
    }


def test_create_knowledge_base_payload_minimal():
    assert create_knowledge_base_payload("my-kb") == {
        "knowledgebase_name": "my-kb",
    }


def test_get_kb_documents_payload_by_file_ids():
    assert get_kb_documents_payload(file_ids="f1,f2") == {"file_ids": ["f1", "f2"]}


def test_get_kb_documents_payload_by_knowledgebase_id():
    payload = get_kb_documents_payload(
        knowledgebase_id="kb-1", doc_type="skill", page=2, page_size=10,
    )
    assert payload == {
        "knowledgebase_id": "kb-1",
        "type": "skill",
        "page": 2,
        "page_size": 10,
    }


def test_get_kb_documents_payload_requires_one():
    with pytest.raises(ValidationError, match="Either file_ids or knowledgebase_id"):
        get_kb_documents_payload()


def test_delete_kb_documents_payload():
    assert delete_kb_documents_payload("f1, f2") == {"file_ids": ["f1", "f2"]}


def test_delete_kb_documents_payload_requires_ids():
    with pytest.raises(ValidationError, match="file_ids is required"):
        delete_kb_documents_payload("")


def test_remove_knowledge_base_payload():
    assert remove_knowledge_base_payload("kb-1") == {"knowledgebase_id": "kb-1"}


def test_remove_knowledge_base_payload_requires_id():
    with pytest.raises(ValidationError, match="knowledgebase_id is required"):
        remove_knowledge_base_payload("")
