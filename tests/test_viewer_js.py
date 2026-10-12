"""The preview page's JavaScript (`lang/preview/viewer`): runs its node
tests (`lang/preview/viewer/tests/*.test.mjs`), skipped without node."""
import shutil
import subprocess
from pathlib import Path

import pytest

VIEWER_TESTS = Path(__file__).resolve().parents[1] / "lang" / "preview" / "viewer" / "tests"


def test_viewer_js() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not on PATH")
    files = sorted(str(path) for path in VIEWER_TESTS.glob("*.test.mjs"))
    assert files, f"no tests in {VIEWER_TESTS}"
    result = subprocess.run([node, "--test", *files], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
