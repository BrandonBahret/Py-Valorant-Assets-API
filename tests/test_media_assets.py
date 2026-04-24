from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import uuid4

from valorant_assets_api import CachedMediaAsset, ValorantAPI
from valorant_assets_api.assets import asset_context
from valorant_assets_api.models import Agent


class _CacheRecord:
    def __init__(self, data: dict[str, object]) -> None:
        self.data = data


class _FakeCache:
    def __init__(self) -> None:
        self._records: dict[str, dict[str, object]] = {}

    def has(self, key: str) -> bool:
        return key in self._records

    def get(self, key: str) -> _CacheRecord:
        return _CacheRecord(self._records[key])

    def store(self, key: str, data: dict[str, object], expiry: float | int | None = None) -> None:
        self._records[key] = data


def _fresh_dir(name: str) -> Path:
    path = Path("tests") / ".artifacts" / f"{name}-{uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_client_binds_media_urls_to_cached_media_assets() -> None:
    root = _fresh_dir("binds-media")
    api = ValorantAPI(cache_path=None, download_directory=str(root / "assets"))
    api.cache = _FakeCache()
    with asset_context(api=api, endpoint_path="/agents"):
        agent = Agent.from_dict(
            {
                "uuid": "agent-uuid",
                "displayName": "Test Agent",
                "description": None,
                "developerName": None,
                "releaseDate": None,
                "characterTags": None,
                "displayIcon": "https://media.valorant-api.com/agents/agent-uuid/displayicon.png",
                "displayIconSmall": None,
                "bustPortrait": None,
                "fullPortrait": None,
                "fullPortraitV2": None,
                "killfeedPortrait": None,
                "minimapPortrait": None,
                "homeScreenPromoTileImage": None,
                "background": None,
                "backgroundGradientColors": [],
                "assetPath": None,
                "isFullPortraitRightFacing": False,
                "isPlayableCharacter": True,
                "isAvailableForTest": False,
                "isBaseContent": True,
                "role": None,
                "recruitmentData": None,
                "abilities": [],
                "voiceLine": {
                    "minDuration": 1.0,
                    "maxDuration": 2.0,
                    "mediaList": [
                        {
                            "id": 7,
                            "wwise": "https://media.valorant-api.com/agents/agent-uuid/vo/test.wwise",
                            "wave": "https://media.valorant-api.com/agents/agent-uuid/vo/test.wav",
                        }
                    ],
                },
            }
        )

    assert isinstance(agent.display_icon, CachedMediaAsset)
    assert isinstance(agent.display_icon, str)
    assert agent.display_icon.url.endswith("displayicon.png")
    assert isinstance(agent.voice_line.media_list[0].wave, CachedMediaAsset)
    assert isinstance(agent.voice_line.media_list[0].wwise, CachedMediaAsset)
    assert agent.display_icon.filepath is None


def test_fetch_from_disk_uses_cache_without_redownloading() -> None:
    root = _fresh_dir("fetch-cache")
    api = ValorantAPI(cache_path=None, download_directory=str(root / "assets"))
    api.cache = _FakeCache()
    asset = CachedMediaAsset(
        "https://media.valorant-api.com/weapons/test/displayicon.png",
        api=api,
        relative_directory=Path("weapons", "weapon-1"),
        field_name="display_icon",
    )
    calls: list[str] = []

    def fake_request(method: str, path: str, **_: object) -> bytes:
        calls.append(f"{method} {path}")
        return b"image-bytes"

    api.request = fake_request  # type: ignore[method-assign]

    first = asset.cache_to_disk()
    second = asset.cache_to_disk()
    first_path = first.filepath
    second_path = second.filepath

    assert first_path == second_path
    assert first_path.exists()
    assert first_path.read_bytes() == b"image-bytes"
    assert calls == ["GET https://media.valorant-api.com/weapons/test/displayicon.png"]


def test_fetch_from_disk_relocates_existing_cached_file() -> None:
    root = _fresh_dir("relocate-cache")
    api = ValorantAPI(cache_path=None, download_directory=str(root / "assets"))
    api.cache = _FakeCache()
    url = "https://media.valorant-api.com/weapons/test/displayicon.png"
    old_path = root / "assets" / "weapons" / "old-weapon" / "displayicon-old.png"
    old_path.parent.mkdir(parents=True, exist_ok=True)
    old_path.write_bytes(b"cached-image")
    api.cache.store(f"media:{hashlib.sha256(url.encode('utf-8')).hexdigest()}", {"path": str(old_path)})

    asset = CachedMediaAsset(
        url,
        api=api,
        relative_directory=Path("weapons", "new-weapon"),
        field_name="display_icon",
    )

    def fail_request(*_: object, **__: object) -> bytes:
        raise AssertionError("download should not occur when a cached file exists")

    api.request = fail_request  # type: ignore[method-assign]
    new_path = asset.cache_to_disk().filepath

    assert new_path.exists()
    assert new_path.read_bytes() == b"cached-image"
    assert "new-weapon" in str(new_path)
