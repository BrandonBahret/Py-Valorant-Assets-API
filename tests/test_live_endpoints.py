from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest
import requests

from valorant_assets_api import (
    Agent,
    Buddy,
    Bundle,
    Ceremony,
    CompetitiveTierSet,
    ContentTier,
    Contract,
    Currency,
    Event,
    Gamemode,
    Gear,
    Language,
    LevelBorder,
    MapInfo,
    Mission,
    Objective,
    PlayerCard,
    PlayerTitle,
    Season,
    Spray,
    Theme,
    ValorantAPI,
    ValorantVersion,
    Weapon,
)
from valorant_assets_api.models import ContractLevel


pytestmark = pytest.mark.live

CACHE_ENV_VAR = "VALORANT_API_TEST_CACHE"
DEFAULT_CACHE_PATH = Path(__file__).with_name("cache.db")
DEFAULT_LANGUAGE = Language.EN_US


class OfflineSession(requests.Session):
    def request(self, *args: Any, **kwargs: Any) -> requests.Response:
        raise AssertionError("network access was used when cached hydration should satisfy the request")


@dataclass(frozen=True)
class ResourceSpec:
    list_method: str
    get_method: str
    item_type: type[Any]
    id_kwarg: str
    list_kwargs: dict[str, Any] = field(default_factory=dict)

    def get_kwargs(self, item: Any) -> dict[str, Any]:
        kwargs = {self.id_kwarg: item.uuid}
        if "language" in self.list_kwargs:
            kwargs["language"] = self.list_kwargs["language"]
        return kwargs


RESOURCE_SPECS = [
    ResourceSpec("list_agents", "get_agent", Agent, "agent_uuid", {"language": DEFAULT_LANGUAGE, "playable_only": True}),
    ResourceSpec("list_buddies", "get_buddy", Buddy, "buddy_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_bundles", "get_bundle", Bundle, "bundle_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_ceremonies", "get_ceremony", Ceremony, "ceremony_uuid"),
    ResourceSpec("list_competitive_tiers", "get_competitive_tier_set", CompetitiveTierSet, "tier_set_uuid"),
    ResourceSpec("list_content_tiers", "get_content_tier", ContentTier, "content_tier_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_contracts", "get_contract", Contract, "contract_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_currencies", "get_currency", Currency, "currency_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_events", "get_event", Event, "event_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_gamemodes", "get_gamemode", Gamemode, "gamemode_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_gear", "get_gear", Gear, "gear_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_level_borders", "get_level_border", LevelBorder, "level_border_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_maps", "get_map", MapInfo, "map_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_missions", "get_mission", Mission, "mission_uuid"),
    ResourceSpec("list_objectives", "get_objective", Objective, "objective_uuid"),
    ResourceSpec("list_player_cards", "get_player_card", PlayerCard, "card_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_player_titles", "get_player_title", PlayerTitle, "title_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_seasons", "get_season", Season, "season_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_sprays", "get_spray", Spray, "spray_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_themes", "get_theme", Theme, "theme_uuid", {"language": DEFAULT_LANGUAGE}),
    ResourceSpec("list_weapons", "get_weapon", Weapon, "weapon_uuid", {"language": DEFAULT_LANGUAGE}),
]


def _cache_path() -> Path:
    configured = os.environ.get(CACHE_ENV_VAR)
    path = Path(configured) if configured else DEFAULT_CACHE_PATH
    return path.expanduser().resolve()


def _cache_artifacts(path: Path) -> tuple[Path, ...]:
    return (
        path,
        path.with_name(f"{path.name}-shm"),
        path.with_name(f"{path.name}-wal"),
    )


def _make_client(cache_path: Path, *, session: requests.Session | None = None) -> ValorantAPI:
    return ValorantAPI(cache_path=str(cache_path), session=session)


def _call(cache_path: Path, method_name: str, **kwargs: Any) -> Any:
    client = _make_client(cache_path)
    try:
        return getattr(client, method_name)(**kwargs)
    finally:
        client.close()


def _call_from_cache(cache_path: Path, method_name: str, **kwargs: Any) -> Any:
    client = _make_client(cache_path, session=OfflineSession())
    try:
        return getattr(client, method_name)(**kwargs)
    finally:
        client.close()


def _cache_row_count(cache_path: Path) -> int:
    if not cache_path.exists():
        return 0
    connection = sqlite3.connect(str(cache_path))
    try:
        return connection.execute("SELECT COUNT(*) FROM cache_records").fetchone()[0]
    finally:
        connection.close()


def _assert_model_identity(expected: Any, actual: Any) -> None:
    assert isinstance(actual, type(expected))
    if hasattr(expected, "uuid"):
        assert actual.uuid == expected.uuid
    if hasattr(expected, "display_name"):
        assert actual.display_name == expected.display_name


@pytest.fixture(scope="session")
def shared_cache_path() -> Path:
    cache_path = _cache_path()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    for artifact in _cache_artifacts(cache_path):
        artifact.unlink(missing_ok=True)
    return cache_path


@pytest.mark.parametrize("spec", RESOURCE_SPECS, ids=lambda spec: spec.list_method)
def test_list_endpoints_hydrate_from_shared_cache(shared_cache_path: Path, spec: ResourceSpec) -> None:
    before_count = _cache_row_count(shared_cache_path)
    live_items = _call(shared_cache_path, spec.list_method, **spec.list_kwargs)

    assert live_items, f"{spec.list_method} returned no records"
    assert isinstance(live_items[0], spec.item_type)

    cached_items = _call_from_cache(shared_cache_path, spec.list_method, **spec.list_kwargs)

    assert isinstance(cached_items, list)
    assert len(cached_items) == len(live_items)
    _assert_model_identity(live_items[0], cached_items[0])
    assert _cache_row_count(shared_cache_path) > before_count


@pytest.mark.parametrize("spec", RESOURCE_SPECS, ids=lambda spec: spec.get_method)
def test_get_endpoints_hydrate_from_shared_cache(shared_cache_path: Path, spec: ResourceSpec) -> None:
    listed_items = _call(shared_cache_path, spec.list_method, **spec.list_kwargs)
    assert listed_items, f"{spec.list_method} returned no records to drive {spec.get_method}"

    target = listed_items[0]
    get_kwargs = spec.get_kwargs(target)

    live_item = _call(shared_cache_path, spec.get_method, **get_kwargs)
    cached_item = _call_from_cache(shared_cache_path, spec.get_method, **get_kwargs)

    _assert_model_identity(live_item, cached_item)


def test_find_endpoints_hydrate_from_shared_cache(shared_cache_path: Path) -> None:
    agent = _call(shared_cache_path, "find_agent", name="Jett", language=DEFAULT_LANGUAGE, playable_only=True)
    cached_agent = _call_from_cache(
        shared_cache_path,
        "find_agent",
        name="Jett",
        language=DEFAULT_LANGUAGE,
        playable_only=True,
    )
    assert isinstance(agent, Agent)
    _assert_model_identity(agent, cached_agent)

    game_map = _call(shared_cache_path, "find_map", name="Ascent", language=DEFAULT_LANGUAGE)
    cached_map = _call_from_cache(shared_cache_path, "find_map", name="Ascent", language=DEFAULT_LANGUAGE)
    assert isinstance(game_map, MapInfo)
    _assert_model_identity(game_map, cached_map)

    weapon = _call(shared_cache_path, "find_weapon", name="Vandal", language=DEFAULT_LANGUAGE)
    cached_weapon = _call_from_cache(shared_cache_path, "find_weapon", name="Vandal", language=DEFAULT_LANGUAGE)
    assert isinstance(weapon, Weapon)
    _assert_model_identity(weapon, cached_weapon)


def test_contract_rewards_hydrate_from_shared_cache(shared_cache_path: Path) -> None:
    contracts = _call(shared_cache_path, "list_contracts", language=DEFAULT_LANGUAGE)
    assert contracts, "list_contracts returned no records"

    live_rewards = _call(shared_cache_path, "list_contract_rewards", contract_uuid=contracts[0].uuid, language=DEFAULT_LANGUAGE)
    cached_rewards = _call_from_cache(
        shared_cache_path,
        "list_contract_rewards",
        contract_uuid=contracts[0].uuid,
        language=DEFAULT_LANGUAGE,
    )

    assert isinstance(live_rewards, list)
    assert len(cached_rewards) == len(live_rewards)
    if live_rewards:
        assert isinstance(live_rewards[0], ContractLevel)
        _assert_model_identity(live_rewards[0].reward, cached_rewards[0].reward)


def test_active_events_hydrate_from_shared_cache(shared_cache_path: Path) -> None:
    live_events = _call(shared_cache_path, "get_active_events", language=DEFAULT_LANGUAGE)
    cached_events = _call_from_cache(shared_cache_path, "get_active_events", language=DEFAULT_LANGUAGE)

    assert isinstance(live_events, list)
    assert len(cached_events) == len(live_events)
    if live_events:
        assert isinstance(live_events[0], Event)
        _assert_model_identity(live_events[0], cached_events[0])


def test_current_season_hydrates_from_shared_cache(shared_cache_path: Path) -> None:
    live_season = _call(shared_cache_path, "get_current_season", language=DEFAULT_LANGUAGE)
    cached_season = _call_from_cache(shared_cache_path, "get_current_season", language=DEFAULT_LANGUAGE)

    assert isinstance(live_season, Season)
    _assert_model_identity(live_season, cached_season)


def test_version_hydrates_from_shared_cache(shared_cache_path: Path) -> None:
    before_count = _cache_row_count(shared_cache_path)
    live_version = _call(shared_cache_path, "get_version")
    cached_version = _call_from_cache(shared_cache_path, "get_version")

    assert isinstance(live_version, ValorantVersion)
    assert isinstance(cached_version, ValorantVersion)
    assert cached_version.version == live_version.version
    assert cached_version.riot_client_version == live_version.riot_client_version
    assert _cache_row_count(shared_cache_path) > before_count
