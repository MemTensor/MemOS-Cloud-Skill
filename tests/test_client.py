import requests
import pytest

from memos_cloud.client import MemosClient
from memos_cloud.config import MemosConfig
from memos_cloud.errors import ApiError, NetworkError


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text="", error=None):
        self.status_code = status_code
        self._payload = payload
        self.text = text
        self._error = error

    def raise_for_status(self):
        if self._error:
            self._error.response = self
            raise self._error

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


class FakeSession:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append({"url": url, **kwargs})
        if self.error:
            raise self.error
        return self.response


def test_client_posts_with_session_headers_and_timeout():
    session = FakeSession(response=FakeResponse(payload={"ok": True}))
    client = MemosClient(MemosConfig("https://api.example/v1", "token"), session=session)

    assert client.post("/search/memory", {"query": "hello"}) == {"ok": True}
    assert session.calls == [
        {
            "url": "https://api.example/v1/search/memory",
            "headers": {
                "Authorization": "Token token",
                "Content-Type": "application/json",
            },
            "json": {"query": "hello", "source": "MEMOS_CLOUD_SKILL"},
            "timeout": 30,
        }
    ]


def test_client_maps_http_error_json_message():
    session = FakeSession(
        response=FakeResponse(
            status_code=400,
            payload={"message": "bad request"},
            error=requests.exceptions.HTTPError(),
        )
    )
    client = MemosClient(MemosConfig("https://api.example/v1", "token"), session=session)

    with pytest.raises(ApiError) as exc_info:
        client.post("/search/memory", {})

    assert exc_info.value.to_payload() == {
        "error": "API Error",
        "message": "HTTP 400 - bad request",
        "status_code": 400,
    }


def test_client_maps_network_error():
    session = FakeSession(error=requests.exceptions.Timeout("timeout"))
    client = MemosClient(MemosConfig("https://api.example/v1", "token"), session=session)

    with pytest.raises(NetworkError, match="timeout"):
        client.post("/search/memory", {})
