from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = [
    ("screen-centric", "001-screened-application-portal"),
    ("api-centric", "001-customer-api-modernization"),
    ("batch-centric", "001-nightly-reconciliation"),
]


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(("sample_name", "design_id"), SAMPLES)
def test_example_storybook_bundle_builds(tmp_path: Path, sample_name: str, design_id: str) -> None:
    source_dir = (
        ROOT
        / "examples"
        / sample_name
        / "designs"
        / "specific_design"
        / design_id
        / "ui-storybook"
    )
    target_dir = tmp_path / "ui-storybook"
    shutil.copytree(source_dir, target_dir)

    install = _run(["npm", "install"], cwd=target_dir)
    assert install.returncode == 0, install.stdout + install.stderr

    build = _run(["npm", "run", "build-storybook"], cwd=target_dir)
    assert build.returncode == 0, build.stdout + build.stderr
    assert (target_dir / "storybook-static" / "iframe.html").exists()
