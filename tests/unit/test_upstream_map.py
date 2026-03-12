from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_upstream_map_local_paths_exist():
    expected_paths = [
        ROOT / "src/speckit_for_projects/foundations",
        ROOT / "src/speckit_for_projects/templates/commands",
        ROOT / "src/speckit_for_projects/templates/agent-files",
        ROOT / "src/speckit_for_projects/domain",
        ROOT / "src/speckit_for_projects/services",
    ]

    for path in expected_paths:
        assert path.exists(), f"missing expected path from upstream map: {path}"
