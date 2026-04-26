from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from tempfile import gettempdir
from typing import Any, List, TypeVar, overload

import requests
from pypercache.api_wrapper import ApiWrapper
from pypercache.utils.typing_cast import instantiate_type

from .assets import asset_context
from .enums import Language
from .models import (
    Agent,
    Buddy,
    Bundle,
    Ceremony,
    CompetitiveTierSet,
    ContentTier,
    Contract,
    ContractLevel,
    Currency,
    Event,
    Gamemode,
    Gear,
    LevelBorder,
    MapInfo,
    Mission,
    Objective,
    PlayerCard,
    PlayerTitle,
    Season,
    Spray,
    Theme,
    ValorantVersion,
    Weapon,
)


BASE_URL = "https://valorant-api.com/v1"
DEFAULT_TIMEOUT = 20
DEFAULT_EXPIRY_SECONDS = 60 * 60 * 24
DEFAULT_CACHE_PATH = str(Path(gettempdir()) / "valorant-api-wrapper" / "valorant-api.db")
DEFAULT_REQUEST_LOG_PATH: str | None = None
DEFAULT_DOWNLOAD_DIRECTORY: str | None = None
USER_AGENT = "valorant-api-wrapper/0.1.2"

T = TypeVar("T")
LanguageLike = Language | str | None


class ValorantAPI(ApiWrapper):
    def __init__(
        self,
        *,
        cache_path: str | None = DEFAULT_CACHE_PATH,
        default_expiry: int | float = DEFAULT_EXPIRY_SECONDS,
        request_log_path: str | None = DEFAULT_REQUEST_LOG_PATH,
        download_directory: str | None = DEFAULT_DOWNLOAD_DIRECTORY,
        timeout: int | float | None = DEFAULT_TIMEOUT,
        session: requests.Session | None = None,
    ) -> None:
        resolved_cache_path = self._prepare_file_path(cache_path)
        resolved_request_log_path = self._prepare_file_path(request_log_path)
        self.download_directory = self._prepare_directory_path(download_directory)
        super().__init__(
            origins={"default": BASE_URL},
            default_origin="default",
            cache_path=resolved_cache_path,
            default_expiry=default_expiry,
            request_log_path=resolved_request_log_path,
            timeout=timeout,
            session=session,
        )

    def get_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            }
        )
        return session

    @overload
    def _request_data(
        self,
        path: str,
        *,
        cast: type[T],
        params: dict[str, Any] | None = None,
        expiry: int | float | None = None,
    ) -> T: ...

    @overload
    def _request_data(
        self,
        path: str,
        *,
        cast: object,
        params: dict[str, Any] | None = None,
        expiry: int | float | None = None,
    ) -> Any: ...

    def _request_data(
        self,
        path: str,
        *,
        cast: object,
        params: dict[str, Any] | None = None,
        expiry: int | float | None = None,
    ) -> Any:
        payload = self.request(
            "GET",
            path,
            params=params,
            expected="json",
            expiry=expiry,
            cast=dict,
        )
        with asset_context(api=self, endpoint_path=path):
            return instantiate_type(cast, payload["data"])

    @staticmethod
    def _language_params(language: LanguageLike) -> dict[str, str] | None:
        if language is None:
            return None
        return {"language": str(language)}

    @classmethod
    def _with_language(cls, params: dict[str, Any] | None, language: LanguageLike) -> dict[str, Any] | None:
        merged = dict(params or {})
        if language is not None:
            merged["language"] = str(language)
        return merged or None

    @staticmethod
    def _uuid_path(resource: str, uuid: str) -> str:
        return f"/{resource}/{ApiWrapper._path_value(uuid)}"

    @staticmethod
    def _prepare_file_path(path: str | None) -> str | None:
        if path is None:
            return None
        file_path = Path(path).expanduser()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return str(file_path)

    @staticmethod
    def _prepare_directory_path(path: str | None) -> Path | None:
        if path is None:
            return None
        directory = Path(path).expanduser()
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    @staticmethod
    def _find_by_name(items: list[T], name: str) -> T | None:
        needle = name.casefold().strip()
        for item in items:
            display_name = getattr(item, "display_name", None)
            if isinstance(display_name, str) and display_name.casefold() == needle:
                return item
        for item in items:
            display_name = getattr(item, "display_name", None)
            if isinstance(display_name, str) and needle in display_name.casefold():
                return item
        return None

    def list_agents(self, *, language: LanguageLike = None, playable_only: bool = False) -> List[Agent]:
        params = self._with_language({"isPlayableCharacter": playable_only or None}, language)
        return self._request_data("/agents", cast=List[Agent], params=params)

    def get_agent(self, agent_uuid: str, *, language: LanguageLike = None) -> Agent:
        return self._request_data(
            self._uuid_path("agents", agent_uuid),
            cast=Agent,
            params=self._language_params(language),
        )

    def find_agent(self, name: str, *, language: LanguageLike = None, playable_only: bool = False) -> Agent | None:
        return self._find_by_name(self.list_agents(language=language, playable_only=playable_only), name)

    def list_buddies(self, *, language: LanguageLike = None) -> List[Buddy]:
        return self._request_data("/buddies", cast=List[Buddy], params=self._language_params(language))

    def get_buddy(self, buddy_uuid: str, *, language: LanguageLike = None) -> Buddy:
        return self._request_data(
            self._uuid_path("buddies", buddy_uuid),
            cast=Buddy,
            params=self._language_params(language),
        )

    def list_bundles(self, *, language: LanguageLike = None) -> List[Bundle]:
        return self._request_data("/bundles", cast=List[Bundle], params=self._language_params(language))

    def get_bundle(self, bundle_uuid: str, *, language: LanguageLike = None) -> Bundle:
        return self._request_data(
            self._uuid_path("bundles", bundle_uuid),
            cast=Bundle,
            params=self._language_params(language),
        )

    def list_ceremonies(self) -> List[Ceremony]:
        return self._request_data("/ceremonies", cast=List[Ceremony])

    def get_ceremony(self, ceremony_uuid: str) -> Ceremony:
        return self._request_data(self._uuid_path("ceremonies", ceremony_uuid), cast=Ceremony)
    
    def list_competitive_tiers(self) -> List[CompetitiveTierSet]:
        return self._request_data("/competitivetiers", cast=List[CompetitiveTierSet], expiry=60 * 60 * 12)

    def get_competitive_tier_set(self, tier_set_uuid: str) -> CompetitiveTierSet:
        return self._request_data(
            self._uuid_path("competitivetiers", tier_set_uuid),
            cast=CompetitiveTierSet,
            expiry=60 * 60 * 12,
        )

    def list_content_tiers(self, *, language: LanguageLike = None) -> List[ContentTier]:
        return self._request_data("/contenttiers", cast=List[ContentTier], params=self._language_params(language))

    def get_content_tier(self, content_tier_uuid: str, *, language: LanguageLike = None) -> ContentTier:
        return self._request_data(
            self._uuid_path("contenttiers", content_tier_uuid),
            cast=ContentTier,
            params=self._language_params(language),
        )

    def list_contracts(self, *, language: LanguageLike = None) -> List[Contract]:
        return self._request_data("/contracts", cast=List[Contract], params=self._language_params(language))

    def get_contract(self, contract_uuid: str, *, language: LanguageLike = None) -> Contract:
        return self._request_data(
            self._uuid_path("contracts", contract_uuid),
            cast=Contract,
            params=self._language_params(language),
        )

    def list_contract_rewards(self, contract_uuid: str, *, language: LanguageLike = None) -> List[ContractLevel]:
        contract = self.get_contract(contract_uuid, language=language)
        rewards: list[ContractLevel] = []
        for chapter in contract.content.chapters:
            rewards.extend(chapter.levels)
        return rewards

    def list_currencies(self, *, language: LanguageLike = None) -> List[Currency]:
        return self._request_data("/currencies", cast=List[Currency], params=self._language_params(language))

    def get_currency(self, currency_uuid: str, *, language: LanguageLike = None) -> Currency:
        return self._request_data(
            self._uuid_path("currencies", currency_uuid),
            cast=Currency,
            params=self._language_params(language),
        )

    def list_events(self, *, language: LanguageLike = None) -> List[Event]:
        return self._request_data("/events", cast=List[Event], params=self._language_params(language))

    def get_event(self, event_uuid: str, *, language: LanguageLike = None) -> Event:
        return self._request_data(
            self._uuid_path("events", event_uuid),
            cast=Event,
            params=self._language_params(language),
        )

    def get_active_events(self, *, language: LanguageLike = None, now: datetime | None = None) -> List[Event]:
        current = now or datetime.now(UTC)
        results: list[Event] = []
        for event in self.list_events(language=language):
            if event.start_time and event.start_time > current:
                continue
            if event.end_time and event.end_time < current:
                continue
            results.append(event)
        return results

    def list_gamemodes(self, *, language: LanguageLike = None) -> List[Gamemode]:
        return self._request_data("/gamemodes", cast=List[Gamemode], params=self._language_params(language))

    def get_gamemode(self, gamemode_uuid: str, *, language: LanguageLike = None) -> Gamemode:
        return self._request_data(
            self._uuid_path("gamemodes", gamemode_uuid),
            cast=Gamemode,
            params=self._language_params(language),
        )

    def list_gear(self, *, language: LanguageLike = None) -> List[Gear]:
        return self._request_data("/gear", cast=List[Gear], params=self._language_params(language))

    def get_gear(self, gear_uuid: str, *, language: LanguageLike = None) -> Gear:
        return self._request_data(
            self._uuid_path("gear", gear_uuid),
            cast=Gear,
            params=self._language_params(language),
        )

    def list_level_borders(self, *, language: LanguageLike = None) -> List[LevelBorder]:
        return self._request_data("/levelborders", cast=List[LevelBorder], params=self._language_params(language))

    def get_level_border(self, level_border_uuid: str, *, language: LanguageLike = None) -> LevelBorder:
        return self._request_data(
            self._uuid_path("levelborders", level_border_uuid),
            cast=LevelBorder,
            params=self._language_params(language),
        )

    def list_maps(self, *, language: LanguageLike = None) -> List[MapInfo]:
        return self._request_data("/maps", cast=List[MapInfo], params=self._language_params(language))

    def get_map(self, map_uuid: str, *, language: LanguageLike = None) -> MapInfo:
        return self._request_data(
            self._uuid_path("maps", map_uuid),
            cast=MapInfo,
            params=self._language_params(language),
        )

    def find_map(self, name: str, *, language: LanguageLike = None) -> MapInfo | None:
        return self._find_by_name(self.list_maps(language=language), name)

    def list_missions(self) -> List[Mission]:
        return self._request_data("/missions", cast=List[Mission], expiry=60 * 30)

    def get_mission(self, mission_uuid: str) -> Mission:
        return self._request_data(self._uuid_path("missions", mission_uuid), cast=Mission, expiry=60 * 30)

    def list_objectives(self) -> List[Objective]:
        return self._request_data("/objectives", cast=List[Objective], expiry=60 * 30)

    def get_objective(self, objective_uuid: str) -> Objective:
        return self._request_data(self._uuid_path("objectives", objective_uuid), cast=Objective, expiry=60 * 30)

    def list_player_cards(self, *, language: LanguageLike = None) -> List[PlayerCard]:
        return self._request_data("/playercards", cast=List[PlayerCard], params=self._language_params(language))

    def get_player_card(self, card_uuid: str, *, language: LanguageLike = None) -> PlayerCard:
        return self._request_data(
            self._uuid_path("playercards", card_uuid),
            cast=PlayerCard,
            params=self._language_params(language),
        )

    def list_player_titles(self, *, language: LanguageLike = None) -> List[PlayerTitle]:
        return self._request_data("/playertitles", cast=List[PlayerTitle], params=self._language_params(language))

    def get_player_title(self, title_uuid: str, *, language: LanguageLike = None) -> PlayerTitle:
        return self._request_data(
            self._uuid_path("playertitles", title_uuid),
            cast=PlayerTitle,
            params=self._language_params(language),
        )

    def list_seasons(self, *, language: LanguageLike = None) -> List[Season]:
        return self._request_data("/seasons", cast=List[Season], params=self._language_params(language))

    def get_season(self, season_uuid: str, *, language: LanguageLike = None) -> Season:
        return self._request_data(
            self._uuid_path("seasons", season_uuid),
            cast=Season,
            params=self._language_params(language),
        )

    def get_current_season(self, *, language: LanguageLike = None, now: datetime | None = None) -> Season | None:
        current = now or datetime.now(UTC)
        active = [
            season
            for season in self.list_seasons(language=language)
            if (season.start_time is None or season.start_time <= current)
            and (season.end_time is None or season.end_time >= current)
        ]
        if not active:
            return None
        return max(
            active,
            key=lambda season: season.start_time or datetime.min.replace(tzinfo=UTC),
        )

    def list_sprays(self, *, language: LanguageLike = None) -> List[Spray]:
        return self._request_data("/sprays", cast=List[Spray], params=self._language_params(language))

    def get_spray(self, spray_uuid: str, *, language: LanguageLike = None) -> Spray:
        return self._request_data(
            self._uuid_path("sprays", spray_uuid),
            cast=Spray,
            params=self._language_params(language),
        )

    def list_themes(self, *, language: LanguageLike = None) -> List[Theme]:
        return self._request_data("/themes", cast=List[Theme], params=self._language_params(language))

    def get_theme(self, theme_uuid: str, *, language: LanguageLike = None) -> Theme:
        return self._request_data(
            self._uuid_path("themes", theme_uuid),
            cast=Theme,
            params=self._language_params(language),
        )

    def list_weapons(self, *, language: LanguageLike = None) -> List[Weapon]:
        return self._request_data("/weapons", cast=List[Weapon], params=self._language_params(language))

    def get_weapon(self, weapon_uuid: str, *, language: LanguageLike = None) -> Weapon:
        return self._request_data(
            self._uuid_path("weapons", weapon_uuid),
            cast=Weapon,
            params=self._language_params(language),
        )

    def find_weapon(self, name: str, *, language: LanguageLike = None) -> Weapon | None:
        return self._find_by_name(self.list_weapons(language=language), name)

    def get_version(self) -> ValorantVersion:
        return self._request_data("/version", cast=ValorantVersion, expiry=60 * 60)
