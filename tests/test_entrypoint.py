import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "memos-cloud-server" / "scripts" / "memos_cloud.py"


def test_real_entrypoint_help_runs_without_api_key():
    env = os.environ.copy()
    env.pop("MEMOS_API_KEY", None)

    result = subprocess.run(
        [sys.executable, str(ENTRYPOINT), "--help"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "add_kb_doc" in result.stdout


def test_real_entrypoint_reports_configuration_error_as_json():
    env = os.environ.copy()
    env.pop("MEMOS_API_KEY", None)

    result = subprocess.run(
        [sys.executable, str(ENTRYPOINT), "search", "user-1", "hello"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert json.loads(result.stderr) == {
        "error": "Configuration Error",
        "message": "MEMOS_API_KEY environment variable is not set.",
    }


def test_top_level_import_preserves_public_functions():
    import memos_cloud

    assert callable(memos_cloud.search_memory)
    assert callable(memos_cloud.add_message)
    assert callable(memos_cloud.delete_memory)
    assert callable(memos_cloud.add_feedback)
    assert callable(memos_cloud.add_kb_doc)
    assert callable(memos_cloud.get_user_profile)
    assert callable(memos_cloud.create_knowledge_base)
    assert callable(memos_cloud.get_kb_documents)
    assert callable(memos_cloud.delete_kb_documents)
    assert callable(memos_cloud.remove_knowledge_base)
