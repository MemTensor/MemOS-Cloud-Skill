import base64
import io

import pytest

from memos_cloud.errors import ValidationError
from memos_cloud.files import (
    build_file_payloads,
    build_stdin_file_payload,
    normalize_base64_content,
)


def test_normalize_base64_content_keeps_existing_base64():
    content = base64.b64encode(b"hello").decode("utf-8")

    assert normalize_base64_content(content.encode("utf-8")) == content


def test_normalize_base64_content_encodes_plain_text():
    assert normalize_base64_content(b"hello") == base64.b64encode(b"hello").decode("utf-8")


def test_normalize_base64_content_encodes_binary():
    raw = b"\xff\xfe\x00"

    assert normalize_base64_content(raw) == base64.b64encode(raw).decode("utf-8")


def test_build_stdin_file_payload_adds_name_when_provided():
    payload = build_stdin_file_payload(io.BytesIO(b"hello"), "skill", "note.txt")

    assert payload == {
        "type": "skill",
        "name": "note.txt",
        "content": "data:text/plain;base64," + base64.b64encode(b"hello").decode("utf-8"),
    }


def test_build_file_payloads_accepts_urls():
    assert build_file_payloads(["https://example.com/doc.pdf"]) == [
        {"type": "document", "content": "https://example.com/doc.pdf"}
    ]


def test_build_file_payloads_reads_local_file(tmp_path):
    doc = tmp_path / "doc.txt"
    doc.write_bytes(b"hello")

    assert build_file_payloads([str(doc)], "skill") == [
        {
            "type": "skill",
            "name": "doc.txt",
            "content": "data:text/plain;base64," + base64.b64encode(b"hello").decode("utf-8"),
            "mime_type": "text/plain",
        }
    ]


def test_build_file_payloads_rejects_invalid_file():
    with pytest.raises(ValidationError, match="Invalid file"):
        build_file_payloads(["missing.txt"])
