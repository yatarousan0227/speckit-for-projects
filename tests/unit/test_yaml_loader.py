from __future__ import annotations

from speckit_for_projects.io.yaml_loader import dump_yaml, load_yaml


def test_yaml_round_trip_preserves_key_order(tmp_path):
    path = tmp_path / "sample.yaml"
    data = {"first": 1, "second": 2, "third": 3}

    dump_yaml(path, data)
    loaded = load_yaml(path)

    assert list(loaded.keys()) == ["first", "second", "third"]
