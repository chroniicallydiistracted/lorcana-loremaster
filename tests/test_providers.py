"""Provider observations stay cached, provenance-bound and separate from official data."""

import json
from datetime import UTC, datetime, timedelta

import pytest

from loremaster.providers import inspect_snapshot, snapshot


def workspace(tmp_path):
    (tmp_path / "sources").mkdir()
    (tmp_path / "sources/providers.json").write_text(
        json.dumps(
            {
                "providers": [
                    {
                        "provider_id": "test",
                        "endpoints": [
                            {
                                "endpoint_id": "cards",
                                "url": "https://example.com/cards",
                                "shape": "results_object",
                                "cache_hours": 24,
                            }
                        ],
                    }
                ]
            }
        )
    )
    return tmp_path


def test_cache_avoids_network_and_preserves_actual_retrieval_time(tmp_path):
    root = workspace(tmp_path)
    now = datetime(2026, 10, 4, tzinfo=UTC)
    first = snapshot(root, "test", "cards", fetch=lambda url: (b'{"results":[{"id":1}]}', url), now=now)

    def forbidden(url):
        pytest.fail("Cached snapshot should not make a network request")

    cached = snapshot(root, "test", "cards", fetch=forbidden, now=now + timedelta(hours=23))
    assert cached["status"] == "cached"
    assert cached["retrieved_at"] == first["retrieved_at"]
    assert not (root / "sources/manifest.json").exists()


@pytest.mark.parametrize("bad", [b'{"error":"blocked"}', b'{"success":false,"results":[]}', b"not json"])
def test_failed_refresh_keeps_previous_source_and_index(tmp_path, bad):
    root = workspace(tmp_path)
    now = datetime(2026, 10, 4, tzinfo=UTC)
    snapshot(root, "test", "cards", fetch=lambda url: (b'{"results":[]}', url), now=now)
    original = (root / "sources/provider-snapshots.json").read_bytes()
    with pytest.raises(ValueError):
        snapshot(root, "test", "cards", fetch=lambda url: (bad, url), now=now + timedelta(days=1))
    assert (root / "sources/provider-snapshots.json").read_bytes() == original
    assert inspect_snapshot(root, "test", "cards")[1] == {"results": []}


def test_unknown_endpoint_and_corrupt_cache_are_rejected(tmp_path):
    root = workspace(tmp_path)
    with pytest.raises(ValueError, match="not approved"):
        snapshot(root, "test", "private-orders")
    first = snapshot(root, "test", "cards", fetch=lambda url: (b'{"results":[]}', url))
    (root / first["path"]).write_text('{"results":[{"id":"changed"}]}')
    with pytest.raises(ValueError, match="bytes changed"):
        snapshot(root, "test", "cards")


def test_missing_raw_cache_can_be_reacquired_without_losing_provenance(tmp_path):
    root = workspace(tmp_path)
    now = datetime(2026, 10, 4, tzinfo=UTC)
    first = snapshot(root, "test", "cards", fetch=lambda url: (b'{"results":[]}', url), now=now)
    (root / first["path"]).unlink()
    original = (root / "sources/provider-snapshots.json").read_bytes()

    def offline(url):
        raise OSError("Offline")

    with pytest.raises(OSError, match="Offline"):
        snapshot(root, "test", "cards", fetch=offline, now=now + timedelta(hours=1))
    assert (root / "sources/provider-snapshots.json").read_bytes() == original
    restored = snapshot(
        root,
        "test",
        "cards",
        fetch=lambda url: (b'{"results":[{"id":2}]}', url),
        now=now + timedelta(hours=2),
    )
    assert restored["sha256"] != first["sha256"]
    assert restored["previous_snapshots"][0]["sha256"] == first["sha256"]
    assert restored["cache_miss_reason"]
    assert inspect_snapshot(root, "test", "cards")[1] == {"results": [{"id": 2}]}
