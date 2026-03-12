from __future__ import annotations

from speckit_for_projects.domain.ids import next_sequenced_slug, slugify


def test_next_sequenced_slug_first_value(tmp_path):
    assert next_sequenced_slug(tmp_path, "Customer Portal") == "001-customer-portal"


def test_next_sequenced_slug_skips_existing_numbers(tmp_path):
    (tmp_path / "001-first.md").write_text("", encoding="utf-8")
    (tmp_path / "004-existing-item").mkdir()

    assert next_sequenced_slug(tmp_path, "Next Item") == "005-next-item"


def test_slugify_normalizes_text():
    assert slugify("  Billing API v2!! ") == "billing-api-v2"
