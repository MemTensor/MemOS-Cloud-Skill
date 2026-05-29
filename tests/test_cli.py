import io
import json

from memos_cloud.cli import main
from memos_cloud.config import MemosConfig


class RecordingClient:
    def __init__(self, response=None):
        self.response = response or {"ok": True}
        self.calls = []
        self.config = MemosConfig("https://api.example/v1", "token")

    def post(self, endpoint, payload):
        self.calls.append((endpoint, payload))
        return self.response


def test_cli_search_prints_json_and_posts_payload(capsys):
    client = RecordingClient({"results": []})

    exit_code = main(["search", "user-1", "hello"], client=client)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == {"results": []}
    assert client.calls == [
        ("/search/memory", {"user_id": "user-1", "query": "hello"})
    ]


def test_cli_invalid_messages_prints_validation_json(capsys):
    exit_code = main(["add_message", "user-1", "conv-1", "not-json"], client=RecordingClient())

    captured = capsys.readouterr()
    assert exit_code == 1
    assert json.loads(captured.err) == {
        "error": "Validation Error",
        "message": "messages must be a valid JSON string",
    }


def test_cli_add_kb_doc_stdin_posts_file_payload(capsys):
    client = RecordingClient({"uploaded": True})

    exit_code = main(
        ["add_kb_doc", "kb-1", "--stdin", "--name", "note.txt"],
        stdin_buffer=io.BytesIO(b"hello"),
        client=client,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == {"uploaded": True}
    assert client.calls == [
        (
            "/add/knowledgebase-file",
            {
                "knowledgebase_id": "kb-1",
                "file": [
                    {
                        "type": "document",
                        "name": "note.txt",
                        "content": "data:text/plain;base64,aGVsbG8=",
                    }
                ],
            },
        )
    ]


def test_cli_add_message_cli_agent_id_overrides_env(capsys):
    client = RecordingClient()
    client.config = MemosConfig(
        "https://api.example/v1", "token", agent_id="env-agent", app_id="env-app"
    )

    exit_code = main(
        [
            "add_message",
            "user-1",
            "conv-1",
            '[{"role":"user","content":"hi"}]',
            "--agent-id",
            "cli-agent",
            "--app-id",
            "cli-app",
        ],
        client=client,
    )

    assert exit_code == 0
    endpoint, payload = client.calls[0]
    assert endpoint == "/add/message"
    assert payload["agent_id"] == "cli-agent"
    assert payload["app_id"] == "cli-app"


def test_cli_add_message_falls_back_to_env_agent_id(capsys):
    client = RecordingClient()
    client.config = MemosConfig(
        "https://api.example/v1", "token", agent_id="env-agent", app_id="env-app"
    )

    exit_code = main(
        ["add_message", "user-1", "conv-1", '[{"role":"user","content":"hi"}]'],
        client=client,
    )

    assert exit_code == 0
    _, payload = client.calls[0]
    assert payload["agent_id"] == "env-agent"
    assert payload["app_id"] == "env-app"


def test_cli_add_feedback_cli_agent_id_overrides_env(capsys):
    client = RecordingClient()
    client.config = MemosConfig(
        "https://api.example/v1", "token", agent_id="env-agent"
    )

    exit_code = main(
        [
            "add_feedback",
            "user-1",
            "conv-1",
            "looks good",
            "--agent-id",
            "cli-agent",
        ],
        client=client,
    )

    assert exit_code == 0
    endpoint, payload = client.calls[0]
    assert endpoint == "/add/feedback"
    assert payload["agent_id"] == "cli-agent"


def test_cli_add_kb_doc_requires_files_or_stdin(capsys):
    exit_code = main(["add_kb_doc", "kb-1"], client=RecordingClient())

    captured = capsys.readouterr()
    assert exit_code == 1
    assert json.loads(captured.err) == {
        "error": "Validation Error",
        "message": "Either provide files or use --stdin",
    }
