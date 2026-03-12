from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from speckit_for_projects.services.consistency_checker import validate_design_bundle

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = [
    ("screen-centric", "001-screened-application-portal"),
    ("api-centric", "001-customer-api-modernization"),
    ("batch-centric", "001-nightly-reconciliation"),
]


def _run_sdd(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "--project", str(ROOT), "sdd", *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )


def test_sample_outputs_fit_initialized_repository(tmp_path: Path) -> None:
    for sample_name, design_id in SAMPLES:
        sample_tmp = tmp_path / sample_name
        sample_tmp.mkdir()
        init_result = _run_sdd(
            sample_tmp,
            "init",
            "--here",
            "--ai",
            "generic",
            "--ai-commands-dir",
            ".myagent/commands",
            "--no-git",
        )
        assert init_result.returncode == 0, init_result.stdout + init_result.stderr

        sample_root = ROOT / "examples" / sample_name
        shutil.copy2(
            sample_root / "briefs" / f"{design_id}.md",
            sample_tmp / "briefs" / f"{design_id}.md",
        )
        shutil.copytree(
            sample_root / "designs" / "common_design",
            sample_tmp / "designs" / "common_design",
            dirs_exist_ok=True,
        )
        shutil.copytree(
            sample_root / "designs" / "specific_design" / design_id,
            sample_tmp / "designs" / "specific_design" / design_id,
        )

        result = validate_design_bundle(
            bundle_dir=sample_tmp / "designs" / "specific_design" / design_id,
            brief_path=sample_tmp / "briefs" / f"{design_id}.md",
        )
        assert result.is_valid, f"{sample_name} pseudo E2E failed: {result.issues}"
