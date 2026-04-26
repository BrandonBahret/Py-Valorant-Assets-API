from __future__ import annotations

import ast
import shutil
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = ROOT / "valorant_assets_api"
ATLAS_DIR = ROOT / "atlas_sources" / "valorant-assets-api"
DOCS_SITE_DIR = ROOT / "docs_site"
INIT_PATH = PACKAGE_DIR / "__init__.py"
CLIENT_PATH = PACKAGE_DIR / "client.py"
MODELS_PATH = PACKAGE_DIR / "models.py"
ENUMS_PATH = PACKAGE_DIR / "enums.py"
NOTEBOOK_HTML_SOURCE = ROOT / "notebooks" / "valorant_assets_api_tutorial.html"
NOTEBOOK_HTML_PUBLISHED = DOCS_SITE_DIR / "notebooks" / NOTEBOOK_HTML_SOURCE.name


FONT_SOURCE = (
    "https://fonts.googleapis.com/css2?"
    "family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&"
    "family=Space+Grotesk:wght@400;500;600;700&"
    "family=Manrope:wght@400;500;600;700&display=swap"
)
EM_DASH = "-"


@dataclass(frozen=True)
class MethodParam:
    name: str
    annotation: str
    default: str | None
    kind: str


@dataclass(frozen=True)
class MethodDoc:
    name: str
    signature: str
    returns: str
    params: list[MethodParam]


@dataclass(frozen=True)
class FieldDoc:
    name: str
    annotation: str
    alias: str | None


@dataclass(frozen=True)
class ModelDoc:
    name: str
    fields: list[FieldDoc]


@dataclass(frozen=True)
class EnumValueDoc:
    name: str
    value: str


@dataclass(frozen=True)
class EnumDoc:
    name: str
    values: list[EnumValueDoc]


@dataclass(frozen=True)
class ResourceMethodConfig:
    name: str
    description: str
    notes: str | None = None


@dataclass(frozen=True)
class ResourceConfig:
    slug: str
    label: str
    endpoint: str
    summary: str
    methods: list[ResourceMethodConfig]
    models: list[str]
    notes: list[str]


INTRODUCTION = """
`valorant-assets-api` wraps the public Valorant content API in one Python client that returns typed objects instead of raw dictionaries. The package is built for applications, scripts, and notebooks that need stable game metadata without repeating HTTP plumbing, response mapping, and local caching.

The wrapper tracks the same major data classes that the upstream Valorant API exposes, but the experience is SDK-shaped rather than endpoint-shaped. Each resource page in this site shows the client methods you call, the models you receive, and the wrapper behaviors layered on top of the raw API.

:::cards
### Quickstart {link=quickstart}
Construct a client, make a few real calls, and inspect typed fields.

### Resource reference {link=agents}
Jump straight to the resource-oriented reference section.
:::

## What the wrapper gives you

- One `ValorantAPI` client for the main public `/v1` content endpoints.
- Typed `@apimodel` resources and nested helper models.
- Built-in caching through `pypercache`.
- Wrapper helpers for common lookup flows like display-name search, active events, current season lookup, and flattened contract rewards.
- Media URL fields wrapped as `CachedMediaAsset` for optional disk downloads.

## What these docs optimize for

These docs follow the upstream resource-per-page scanning model, but each page is adapted to the Python API surface. You can open a resource page like [doc:weapons] to see the relevant client methods and the schema you get back in the same place.
"""

INSTALLATION = """
Install the published package when you want the wrapper in an application environment:

```bash
pip install valorant-assets-api
```

Install the project in editable mode for local development and testing:

```bash
pip install -e .[test]
```

## Requirements

- Python `>=3.11`
- `requests>=2.31.0`
- `pypercache>=0.1.9`

## What installation gives you

After installation, the package exports the main client, the shared enums, the root resource models, and `CachedMediaAsset` from the package root:

```python
from valorant_assets_api import Language, ValorantAPI, Weapon
```

:::callout info
The package depends on the public Valorant content API. Calls that miss cache still require network access to `https://valorant-api.com`.
:::
"""

QUICKSTART = """
Start with a default client and a few calls that exercise the main lookup styles:

```python
from valorant_assets_api import ValorantAPI

api = ValorantAPI()

agents = api.list_agents(playable_only=True)
brimstone = api.find_agent("Brimstone", playable_only=True)
bind_map = api.find_map("Bind")
version = api.get_version()

print(agents[0].display_name)
print(brimstone.role.display_name if brimstone and brimstone.role else "No role")
print(bind_map.coordinates if bind_map else "No coordinates")
print(version.version)
```

## What to notice

- `list_*` methods return typed collections.
- `get_*` methods fetch one typed object by UUID.
- `find_*` helpers are convenience lookups for interactive or display-name-driven flows.
- Returned objects expose nested models and enums directly.

:::callout info
The default client uses a temp-directory SQLite cache with a 24 hour expiry. Repeated calls are expected to hit cache for mostly static metadata.
:::

:::quick_links
- [Common lookup patterns | doc:common-lookup-patterns]
- [Client configuration | doc:client-configuration]
- [Weapons reference | doc:weapons]
:::
"""

CACHING = """
Caching is part of the package's normal usage model, not an optional afterthought. Most endpoints expose content metadata that changes slowly, so the default client stores responses locally and reuses them across calls.

## Defaults

:::table
| Setting | Default | Meaning |
|---------|---------|---------|
| `cache_path` | temp SQLite path | Stores cached responses on disk |
| `default_expiry` | `60 * 60 * 24` | Freshness window for most endpoints |
| `timeout` | `20` | Request timeout in seconds |
| `request_log_path` | `None` | Logging disabled by default |
:::

## Resource-specific freshness

Some endpoints override the default expiry in the client implementation:

- Competitive tiers use a 12 hour expiry.
- Missions and objectives use a 30 minute expiry.
- Version metadata uses a 1 hour expiry.

## Practical guidance

- Keep the default cache for scripts and exploratory work.
- Set `cache_path` explicitly when you want a reproducible project-local cache file.
- Lower expiry values when you are validating freshness-sensitive behavior.
- Enable request logging when you need to confirm which calls miss cache.

:::callout warn
Cached media files are separate from the HTTP response cache. Resource metadata lives in the API cache, while downloaded images and audio files live under `download_directory`.
:::
"""

TYPED_MODELS = """
The wrapper hydrates API payloads into typed Python objects using `@apimodel` definitions from `valorant_assets_api.models`. That means resource pages can document the client call and the resulting schema together.

## What typed hydration changes

- You access fields as attributes instead of dictionary keys.
- Nested objects such as `Agent.role` or `Weapon.weapon_stats` are hydrated into nested models.
- Enum-backed fields are coerced into exported enums where possible.
- Timestamp fields are converted to `datetime` objects.

## Exported models vs nested helper models

The package root exports the main top-level resource models. Many resource pages also include nested helper models that are not exported from `valorant_assets_api.__init__`, but they still matter when you inspect real responses.

:::callout info
When a field type is written as `Enum | str | None`, the client tries to coerce known values into the enum while still tolerating unexpected upstream values.
:::

## Shared references

- [doc:enums] for exported enum values
- [doc:cached-media-asset] for media URL behavior
"""

MEDIA_ASSETS = """
Many response fields that look like plain media URLs are wrapped as `CachedMediaAsset` instances during model hydration. You can still treat them like strings, but the wrapper also lets you download and reuse them on disk.

## How it works

- A media field remains string-like, so `str(asset)` and normal URL usage still work.
- The wrapper attaches API and resource context during hydration.
- `cache_to_disk()` downloads or relocates the asset into `download_directory`.
- `fetch_from_disk()` ensures the file exists locally and returns a `Path`.

## Requirements

To fetch media files, construct the client with `download_directory`:

```python
from valorant_assets_api import ValorantAPI

api = ValorantAPI(download_directory="cache/media")
agent = api.get_agent("add6443a-41bd-e414-f6ad-e58d267f4e95")
local_icon = agent.display_icon.fetch_from_disk()
```

:::callout warn
Disk download methods raise `ValueError` when `download_directory` is not configured on the client.
:::

See [doc:cached-media-asset] for the helper reference and [doc:agents] or [doc:weapons] for real resource fields that use it.
"""

LOOKUP_PATTERNS = """
The client surface follows a consistent set of lookup patterns across resource types.

## Collection lookups

Use `list_*` methods when you want a full collection of a resource type:

```python
agents = api.list_agents(playable_only=True)
weapons = api.list_weapons()
```

## UUID lookups

Use `get_*` methods when you already have a resource identifier:

```python
agent = api.get_agent(agent_uuid)
weapon = api.get_weapon(weapon_uuid)
```

## Display-name helpers

Some resources expose `find_*` helpers:

- `find_agent()`
- `find_map()`
- `find_weapon()`

These helpers first try an exact case-insensitive display-name match, then a substring match.

## Wrapper helpers

The client also exposes task-shaped helpers:

- `get_active_events()` filters event windows against current or injected UTC time.
- `get_current_season()` returns the current active season or `None`.
- `list_contract_rewards()` flattens contract chapter rewards into one list.
"""

LOCALIZATION = """
Many content endpoints accept a `language` argument. The wrapper exposes the supported values through the `Language` enum while still accepting plain strings when that is more convenient.

```python
from valorant_assets_api import Language, ValorantAPI

api = ValorantAPI()
weapons = api.list_weapons(language=Language.JA_JP)
```

## Coverage

Localization support is resource-specific. The relevant resource pages document `language` only for methods that actually accept it in `client.py`.

Resources without language support in the current client implementation include:

- Ceremonies
- Competitive tiers
- Missions
- Objectives
- Version

:::callout info
Use the enum when you want discoverable supported values. Use a string when the value comes from config or user input.
:::
"""

CLIENT_CONFIGURATION = """
Construct `ValorantAPI` with defaults when you want the standard cached wrapper behavior, or override specific settings when your environment needs tighter control.

:::method
ValorantAPI(*, cache_path: str | None = DEFAULT_CACHE_PATH, default_expiry: int | float = DEFAULT_EXPIRY_SECONDS, request_log_path: str | None = DEFAULT_REQUEST_LOG_PATH, download_directory: str | None = DEFAULT_DOWNLOAD_DIRECTORY, timeout: int | float | None = DEFAULT_TIMEOUT, session: requests.Session | None = None)
:::

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `cache_path` | `str | None` | temp SQLite path | no | Location for the HTTP response cache |
| `default_expiry` | `int | float` | `86400` | no | Default freshness window in seconds |
| `request_log_path` | `str | None` | `None` | no | Optional request log file path |
| `download_directory` | `str | None` | `None` | no | Root directory for downloaded media assets |
| `timeout` | `int | float | None` | `20` | no | Request timeout in seconds |
| `session` | `requests.Session | None` | `None` | no | Optional custom session |
:::

## Session behavior

If you do not pass a session, the client creates one with:

- `Accept: application/json`
- `User-Agent: valorant-api-wrapper/0.1.2`

Use a custom session when you need shared headers, custom adapters, or request instrumentation beyond the built-in defaults.
"""

NOTEBOOK = """
The repository includes a guided notebook at [`notebooks/valorant_assets_api_tutorial.ipynb`](https://github.com/BrandonBahret/Py-Valorant-Assets-API/blob/main/notebooks/valorant_assets_api_tutorial.ipynb).

Use the notebook when you want an interactive walkthrough of:

- package installation and setup
- client construction
- localization
- UUID lookups
- helper methods
- cache configuration
- typed model inspection

Stay in the Atlas docs when you want fast lookup. Open the notebook when you want a single guided flow with executable examples.

:::callout info
The embedded export below is a read-only preview of the executed notebook. Open the full export in a separate tab when you want native width, your browser's page search, or the original notebook source.
:::

<style>
  .notebook-preview {
    margin: 28px 0 34px;
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    background:
      linear-gradient(180deg, color-mix(in srgb, var(--surface) 94%, transparent), color-mix(in srgb, var(--bg) 88%, transparent)),
      radial-gradient(circle at top left, color-mix(in srgb, var(--accent2) 12%, transparent), transparent 42%);
    box-shadow: 0 18px 46px color-mix(in srgb, var(--bg) 46%, transparent);
  }
  .notebook-preview__bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding: 16px 18px;
    border-bottom: 1px solid var(--border-subtle);
    background: linear-gradient(180deg, color-mix(in srgb, var(--surface) 92%, transparent), transparent);
  }
  .notebook-preview__title {
    font-family: var(--font-display);
    font-size: 22px;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0;
  }
  .notebook-preview__meta {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent2);
  }
  .notebook-preview__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  .notebook-preview__action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 36px;
    padding: 0 13px;
    border-radius: 999px;
    border: 1px solid color-mix(in srgb, var(--accent2) 20%, var(--border));
    background: color-mix(in srgb, var(--surface) 88%, transparent);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
    text-decoration: none;
    white-space: nowrap;
  }
  .notebook-preview__action:hover {
    text-decoration: none;
    border-color: color-mix(in srgb, var(--accent) 28%, var(--border));
    background: color-mix(in srgb, var(--accent) 8%, var(--surface));
  }
  .notebook-preview__frame-wrap {
    padding: 18px;
  }
  .notebook-preview__frame {
    display: block;
    width: 100%;
    min-height: 900px;
    border: 1px solid color-mix(in srgb, var(--accent2) 12%, var(--border));
    border-radius: 14px;
    background: #ffffff;
  }
  .notebook-preview__caption {
    padding: 0 18px 18px;
    font-size: 13px;
    color: var(--text-dimmer);
  }
  @media (max-width: 820px) {
    .notebook-preview__bar {
      flex-direction: column;
      align-items: flex-start;
    }
    .notebook-preview__frame {
      min-height: 720px;
    }
  }
</style>

<section class="notebook-preview" aria-labelledby="notebook-preview-title">
  <div class="notebook-preview__bar">
    <div>
      <div class="notebook-preview__meta">Notebook export</div>
      <p class="notebook-preview__title" id="notebook-preview-title">Executed HTML walkthrough</p>
    </div>
    <div class="notebook-preview__actions">
      <a class="notebook-preview__action" href="./notebooks/valorant_assets_api_tutorial.html" target="_blank">Open HTML export</a>
      <a class="notebook-preview__action" href="https://github.com/BrandonBahret/Py-Valorant-Assets-API/blob/main/notebooks/valorant_assets_api_tutorial.ipynb" target="_blank">Open notebook source</a>
    </div>
  </div>
  <div class="notebook-preview__frame-wrap">
    <iframe
      class="notebook-preview__frame"
      src="./notebooks/valorant_assets_api_tutorial.html"
      title="Valorant assets API tutorial notebook export"
      loading="lazy"
      referrerpolicy="no-referrer"
    ></iframe>
  </div>
  <p class="notebook-preview__caption">The iframe keeps Jupyter's CSS and layout isolated from the Atlas page, so the walkthrough renders as its own document instead of fighting the surrounding docs theme.</p>
</section>
"""

CACHED_MEDIA_ASSET_PAGE = """
`CachedMediaAsset` is the wrapper's string-like media helper. Resource pages use it for fields such as `Agent.display_icon`, `PlayerCard.large_art`, or `WeaponSkin.streamed_video`.

## Helper surface

:::method
CachedMediaAsset.url
:::

Returns the original remote URL as a string.

:::method
CachedMediaAsset.filepath
:::

Returns the cached local `Path` when the asset has already been downloaded or relocated, otherwise `None`.

:::method
CachedMediaAsset.cache_to_disk()
:::

Downloads or relocates the asset into the client's `download_directory` and returns the same `CachedMediaAsset`.

:::method
CachedMediaAsset.fetch_from_disk()
:::

Ensures the file exists locally and returns its `Path`.

## Behavior notes

- The helper subclasses `str`, so you can pass it where a URL string is expected.
- The cache key for local media files is derived from the media URL.
- Repeated downloads reuse cached files instead of re-fetching when possible.
- Missing client attachment or missing `download_directory` raises `ValueError`.

See [doc:media-assets-and-disk-downloads] for the conceptual guide.
"""


RESOURCE_CONFIGS = [
    ResourceConfig(
        slug="agents",
        label="Agents",
        endpoint="/agents",
        summary="Playable and non-playable agent data, plus role, ability, and voice metadata.",
        methods=[
            ResourceMethodConfig("list_agents", "List agent resources.", "Set `playable_only=True` to request only playable characters."),
            ResourceMethodConfig("get_agent", "Fetch one agent by UUID."),
            ResourceMethodConfig("find_agent", "Find an agent by display name.", "The helper matches exact case-insensitive names before substring matches."),
        ],
        models=["Agent", "Role", "Ability", "VoiceLine", "RecruitmentData", "MediaAsset"],
        notes=[
            "Agent media fields such as `display_icon` and `full_portrait` are wrapped as `CachedMediaAsset` values.",
            "Playable filtering is a wrapper-level convenience on top of the collection endpoint.",
        ],
    ),
    ResourceConfig(
        slug="buddies",
        label="Buddies",
        endpoint="/buddies",
        summary="Gun buddy collection and buddy level metadata.",
        methods=[
            ResourceMethodConfig("list_buddies", "List buddy resources."),
            ResourceMethodConfig("get_buddy", "Fetch one buddy by UUID."),
        ],
        models=["Buddy", "BuddyLevel"],
        notes=["`levels` is represented as a nested lazy list on the hydrated buddy model."],
    ),
    ResourceConfig(
        slug="bundles",
        label="Bundles",
        endpoint="/bundles",
        summary="Store bundle metadata and associated imagery.",
        methods=[
            ResourceMethodConfig("list_bundles", "List bundle resources."),
            ResourceMethodConfig("get_bundle", "Fetch one bundle by UUID."),
        ],
        models=["Bundle"],
        notes=["Bundle image fields are wrapped as `CachedMediaAsset` values when present."],
    ),
    ResourceConfig(
        slug="ceremonies",
        label="Ceremonies",
        endpoint="/ceremonies",
        summary="Ceremony metadata with lightweight schema coverage.",
        methods=[
            ResourceMethodConfig("list_ceremonies", "List ceremony resources."),
            ResourceMethodConfig("get_ceremony", "Fetch one ceremony by UUID."),
        ],
        models=["Ceremony"],
        notes=["This resource does not expose `language` in the current client implementation."],
    ),
    ResourceConfig(
        slug="competitive-tiers",
        label="Competitive Tiers",
        endpoint="/competitivetiers",
        summary="Competitive rank set data and nested tier definitions.",
        methods=[
            ResourceMethodConfig("list_competitive_tiers", "List competitive tier sets.", "The client applies a 12 hour expiry override."),
            ResourceMethodConfig("get_competitive_tier_set", "Fetch one competitive tier set by UUID.", "The client applies a 12 hour expiry override."),
        ],
        models=["CompetitiveTierSet", "CompetitiveTier"],
        notes=["This resource does not expose `language` in the current client implementation."],
    ),
    ResourceConfig(
        slug="content-tiers",
        label="Content Tiers",
        endpoint="/contenttiers",
        summary="Content tier metadata used across skins and rewards.",
        methods=[
            ResourceMethodConfig("list_content_tiers", "List content tier resources."),
            ResourceMethodConfig("get_content_tier", "Fetch one content tier by UUID."),
        ],
        models=["ContentTier"],
        notes=[],
    ),
    ResourceConfig(
        slug="contracts",
        label="Contracts",
        endpoint="/contracts",
        summary="Contract data, reward schedules, and flattened reward helper output.",
        methods=[
            ResourceMethodConfig("list_contracts", "List contract resources."),
            ResourceMethodConfig("get_contract", "Fetch one contract by UUID."),
            ResourceMethodConfig("list_contract_rewards", "Flatten all chapter levels from one contract.", "This helper returns `ContractLevel` items rather than a top-level exported model."),
        ],
        models=["Contract", "ContractContent", "ContractChapter", "ContractLevel", "Reward"],
        notes=["`list_contract_rewards()` is wrapper-specific and does not map to a direct endpoint."],
    ),
    ResourceConfig(
        slug="currencies",
        label="Currencies",
        endpoint="/currencies",
        summary="Currency metadata and reward icon fields.",
        methods=[
            ResourceMethodConfig("list_currencies", "List currency resources."),
            ResourceMethodConfig("get_currency", "Fetch one currency by UUID."),
        ],
        models=["Currency"],
        notes=[],
    ),
    ResourceConfig(
        slug="events",
        label="Events",
        endpoint="/events",
        summary="Event metadata plus wrapper-level active window filtering.",
        methods=[
            ResourceMethodConfig("list_events", "List event resources."),
            ResourceMethodConfig("get_event", "Fetch one event by UUID."),
            ResourceMethodConfig("get_active_events", "Return currently active events.", "The helper compares event windows against `now` or the current UTC time."),
        ],
        models=["Event"],
        notes=["`get_active_events()` is a wrapper helper layered on top of `list_events()`."],
    ),
    ResourceConfig(
        slug="gamemodes",
        label="Gamemodes",
        endpoint="/gamemodes",
        summary="Gamemode metadata and nested game rule overrides.",
        methods=[
            ResourceMethodConfig("list_gamemodes", "List gamemode resources."),
            ResourceMethodConfig("get_gamemode", "Fetch one gamemode by UUID."),
        ],
        models=["Gamemode", "GameFeatureOverride", "GameRuleBoolOverride"],
        notes=[],
    ),
    ResourceConfig(
        slug="gear",
        label="Gear",
        endpoint="/gear",
        summary="Gear metadata, nested shop data, and descriptive detail rows.",
        methods=[
            ResourceMethodConfig("list_gear", "List gear resources."),
            ResourceMethodConfig("get_gear", "Fetch one gear item by UUID."),
        ],
        models=["Gear", "GearDetail", "ShopData", "ShopGridPosition"],
        notes=[],
    ),
    ResourceConfig(
        slug="level-borders",
        label="Level Borders",
        endpoint="/levelborders",
        summary="Level border metadata and progression display fields.",
        methods=[
            ResourceMethodConfig("list_level_borders", "List level border resources."),
            ResourceMethodConfig("get_level_border", "Fetch one level border by UUID."),
        ],
        models=["LevelBorder"],
        notes=[],
    ),
    ResourceConfig(
        slug="maps",
        label="Maps",
        endpoint="/maps",
        summary="Map metadata, coordinate helpers, and nested callout positions.",
        methods=[
            ResourceMethodConfig("list_maps", "List map resources."),
            ResourceMethodConfig("get_map", "Fetch one map by UUID."),
            ResourceMethodConfig("find_map", "Find a map by display name.", "The helper matches exact case-insensitive names before substring matches."),
        ],
        models=["MapInfo", "Callout", "Position3D", "Rotation3D"],
        notes=["Map image fields are wrapped as `CachedMediaAsset` values when present."],
    ),
    ResourceConfig(
        slug="missions",
        label="Missions",
        endpoint="/missions",
        summary="Mission metadata and nested objective progress rows.",
        methods=[
            ResourceMethodConfig("list_missions", "List mission resources.", "The client applies a 30 minute expiry override."),
            ResourceMethodConfig("get_mission", "Fetch one mission by UUID.", "The client applies a 30 minute expiry override."),
        ],
        models=["Mission", "MissionObjectiveProgress"],
        notes=["This resource does not expose `language` in the current client implementation."],
    ),
    ResourceConfig(
        slug="objectives",
        label="Objectives",
        endpoint="/objectives",
        summary="Objective metadata used by mission payloads.",
        methods=[
            ResourceMethodConfig("list_objectives", "List objective resources.", "The client applies a 30 minute expiry override."),
            ResourceMethodConfig("get_objective", "Fetch one objective by UUID.", "The client applies a 30 minute expiry override."),
        ],
        models=["Objective"],
        notes=["This resource does not expose `language` in the current client implementation."],
    ),
    ResourceConfig(
        slug="player-cards",
        label="Player Cards",
        endpoint="/playercards",
        summary="Player card metadata and the associated art variants.",
        methods=[
            ResourceMethodConfig("list_player_cards", "List player card resources."),
            ResourceMethodConfig("get_player_card", "Fetch one player card by UUID."),
        ],
        models=["PlayerCard"],
        notes=["Art fields such as `small_art`, `wide_art`, and `large_art` are wrapped as `CachedMediaAsset` values."],
    ),
    ResourceConfig(
        slug="player-titles",
        label="Player Titles",
        endpoint="/playertitles",
        summary="Player title metadata and title text fields.",
        methods=[
            ResourceMethodConfig("list_player_titles", "List player title resources."),
            ResourceMethodConfig("get_player_title", "Fetch one player title by UUID."),
        ],
        models=["PlayerTitle"],
        notes=[],
    ),
    ResourceConfig(
        slug="seasons",
        label="Seasons",
        endpoint="/seasons",
        summary="Season metadata plus the helper for selecting the active season.",
        methods=[
            ResourceMethodConfig("list_seasons", "List season resources."),
            ResourceMethodConfig("get_season", "Fetch one season by UUID."),
            ResourceMethodConfig("get_current_season", "Return the active season.", "The helper compares season windows against `now` or the current UTC time and returns `None` when nothing is active."),
        ],
        models=["Season"],
        notes=["`get_current_season()` is a wrapper helper layered on top of `list_seasons()`."],
    ),
    ResourceConfig(
        slug="sprays",
        label="Sprays",
        endpoint="/sprays",
        summary="Spray metadata, art assets, and nested spray levels.",
        methods=[
            ResourceMethodConfig("list_sprays", "List spray resources."),
            ResourceMethodConfig("get_spray", "Fetch one spray by UUID."),
        ],
        models=["Spray", "SprayLevel"],
        notes=["Animation and icon fields are wrapped as `CachedMediaAsset` values when present."],
    ),
    ResourceConfig(
        slug="themes",
        label="Themes",
        endpoint="/themes",
        summary="Theme metadata and store artwork fields.",
        methods=[
            ResourceMethodConfig("list_themes", "List theme resources."),
            ResourceMethodConfig("get_theme", "Fetch one theme by UUID."),
        ],
        models=["Theme"],
        notes=[],
    ),
    ResourceConfig(
        slug="weapons",
        label="Weapons",
        endpoint="/weapons",
        summary="Weapon metadata, nested stats, shop data, skins, chromas, and damage ranges.",
        methods=[
            ResourceMethodConfig("list_weapons", "List weapon resources."),
            ResourceMethodConfig("get_weapon", "Fetch one weapon by UUID."),
            ResourceMethodConfig("find_weapon", "Find a weapon by display name.", "The helper matches exact case-insensitive names before substring matches."),
        ],
        models=["Weapon", "WeaponStats", "WeaponSkin", "WeaponSkinLevel", "WeaponChroma", "DamageRange", "AdsStats", "AltShotgunStats", "AirBurstStats", "ShopData", "ShopGridPosition"],
        notes=["Weapon and skin image or video fields are wrapped as `CachedMediaAsset` values when present."],
    ),
    ResourceConfig(
        slug="version",
        label="Version",
        endpoint="/version",
        summary="Current Valorant client and manifest version metadata.",
        methods=[
            ResourceMethodConfig("get_version", "Fetch the current version metadata.", "The client applies a 1 hour expiry override."),
        ],
        models=["ValorantVersion"],
        notes=["This resource does not expose `language` in the current client implementation."],
    ),
]


GROUPS = [
    ("Overview", [("Introduction", "introduction"), ("Installation", "installation"), ("Quickstart", "quickstart")]),
    ("Concepts", [("Caching and freshness", "caching-and-freshness"), ("Typed models and enums", "typed-models-and-enums"), ("Media assets and disk downloads", "media-assets-and-disk-downloads")]),
    ("Guides", [("Common lookup patterns", "common-lookup-patterns"), ("Localization", "localization"), ("Client configuration", "client-configuration"), ("Notebook walkthrough", "notebook-walkthrough")]),
    ("Reference", [(resource.label, resource.slug) for resource in RESOURCE_CONFIGS]),
    ("Appendix", [("Enums", "enums"), ("CachedMediaAsset", "cached-media-asset")]),
]


def parse_module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def parse_exports() -> list[str]:
    module = parse_module(INIT_PATH)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return list(ast.literal_eval(node.value))
    raise ValueError("Could not find __all__")


def format_arg(arg: ast.arg, default: ast.expr | None) -> str:
    text = arg.arg
    if arg.annotation is not None:
        text += f": {ast.unparse(arg.annotation)}"
    if default is not None:
        text += f" = {ast.unparse(default)}"
    return text


def format_signature(function: ast.FunctionDef) -> str:
    args = function.args
    parts: list[str] = []
    positional = list(args.posonlyargs) + list(args.args)
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    for arg, default in zip(positional, defaults):
        if arg.arg == "self":
            continue
        parts.append(format_arg(arg, default))
    if args.vararg:
        parts.append(f"*{args.vararg.arg}")
    if args.kwonlyargs:
        if not args.vararg:
            parts.append("*")
        for arg, default in zip(args.kwonlyargs, args.kw_defaults):
            parts.append(format_arg(arg, default))
    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")
    return f"({', '.join(parts)})"


def parse_client_methods() -> dict[str, MethodDoc]:
    module = parse_module(CLIENT_PATH)
    client_class = next(node for node in module.body if isinstance(node, ast.ClassDef) and node.name == "ValorantAPI")
    methods: dict[str, MethodDoc] = {}
    for node in client_class.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name.startswith("_"):
            continue
        params: list[MethodParam] = []
        positional = list(node.args.posonlyargs) + list(node.args.args)
        defaults = [None] * (len(positional) - len(node.args.defaults)) + list(node.args.defaults)
        for arg, default in zip(positional, defaults):
            if arg.arg == "self":
                continue
            params.append(
                MethodParam(
                    name=arg.arg,
                    annotation=ast.unparse(arg.annotation) if arg.annotation is not None else "Any",
                    default=ast.unparse(default) if default is not None else None,
                    kind="positional",
                )
            )
        for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
            params.append(
                MethodParam(
                    name=arg.arg,
                    annotation=ast.unparse(arg.annotation) if arg.annotation is not None else "Any",
                    default=ast.unparse(default) if default is not None else None,
                    kind="keyword",
                )
            )
        methods[node.name] = MethodDoc(
            name=node.name,
            signature=format_signature(node),
            returns=ast.unparse(node.returns) if node.returns is not None else "Any",
            params=params,
        )
    return methods


def parse_alias(annotation: ast.expr | None) -> str | None:
    if not isinstance(annotation, ast.Subscript):
        return None
    if not isinstance(annotation.value, ast.Name) or annotation.value.id != "Annotated":
        return None
    values = list(annotation.slice.elts) if isinstance(annotation.slice, ast.Tuple) else [annotation.slice]
    for extra in values[1:]:
        if (
            isinstance(extra, ast.Call)
            and isinstance(extra.func, ast.Name)
            and extra.func.id == "Alias"
            and extra.args
            and isinstance(extra.args[0], ast.Constant)
            and isinstance(extra.args[0].value, str)
        ):
            return extra.args[0].value
    return None


def strip_annotated(annotation: ast.expr | None) -> str:
    if annotation is None:
        return "Any"
    if not isinstance(annotation, ast.Subscript):
        return ast.unparse(annotation)
    if not isinstance(annotation.value, ast.Name) or annotation.value.id != "Annotated":
        return ast.unparse(annotation)
    if isinstance(annotation.slice, ast.Tuple) and annotation.slice.elts:
        return ast.unparse(annotation.slice.elts[0])
    return ast.unparse(annotation)


def parse_models() -> dict[str, ModelDoc]:
    module = parse_module(MODELS_PATH)
    models: dict[str, ModelDoc] = {}
    for node in module.body:
        if not isinstance(node, ast.ClassDef):
            continue
        fields: list[FieldDoc] = []
        for statement in node.body:
            if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
                fields.append(
                    FieldDoc(
                        name=statement.target.id,
                        annotation=strip_annotated(statement.annotation),
                        alias=parse_alias(statement.annotation),
                    )
                )
        models[node.name] = ModelDoc(name=node.name, fields=fields)
    return models


def parse_enums(export_names: set[str]) -> dict[str, EnumDoc]:
    module = parse_module(ENUMS_PATH)
    enums: dict[str, EnumDoc] = {}
    for node in module.body:
        if not isinstance(node, ast.ClassDef) or node.name not in export_names:
            continue
        values: list[EnumValueDoc] = []
        for statement in node.body:
            if (
                isinstance(statement, ast.Assign)
                and len(statement.targets) == 1
                and isinstance(statement.targets[0], ast.Name)
                and isinstance(statement.value, ast.Constant)
                and isinstance(statement.value.value, str)
            ):
                values.append(EnumValueDoc(name=statement.targets[0].id, value=statement.value.value))
        enums[node.name] = EnumDoc(name=node.name, values=values)
    return enums


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text).strip() + "\n", encoding="utf-8")


def yaml_block(entries: list[tuple[str, str]]) -> str:
    return "\n".join(f'  - {label} | {slug}' for label, slug in entries)


def render_metadata() -> str:
    return f"""---
name: valorant-assets-api
version: 0.1.2
tagline: Typed pypercache-based wrapper for the public Valorant API.
accent: "#ff4655"
accent_dark: "#ff4655"
accent_light: "#c63242"
color_scheme: dark
display_font: "Space Grotesk"
body_font: "Manrope"
mono_font: "IBM Plex Mono"
font_source: "{FONT_SOURCE}"
search_trigger_label: "resources, methods, schemas..."
search_placeholder: "Search Valorant wrapper docs..."
search_secondary_hint: "Search resources, guides, methods, and models."
features:
  search: true
---"""


def render_navigation() -> str:
    lines = ["---", "groups:"]
    for label, entries in GROUPS:
        lines.append(f"  - label: {label}")
        lines.append("    entries:")
        lines.extend(f"      - {entry_label} | {slug}" for entry_label, slug in entries)
    lines.extend(
        [
            "footer:",
            "  label: Project",
            "  entries:",
            "    - Valorant API Docs | https://dash.valorant-api.com/ | external",
            "    - Public API | https://valorant-api.com/ | external",
            "---",
        ]
    )
    return "\n".join(lines)


def render_assets() -> str:
    return "---\nsvgs: []\nimages: []\nremote_images: []\n---"


def render_page(slug: str, title: str, lead: str, body: str, tag: str) -> str:
    return f"""---
tag: {tag}
title: {title}
lead: |
  {lead}
breadcrumb: "valorant-assets-api / {title.lower()}"
---

{body.strip()}
"""


PARAM_DESCRIPTIONS = {
    "language": "Localization code for endpoints that expose translated content.",
    "playable_only": "When true, requests only playable agents from the collection endpoint.",
    "agent_uuid": "UUID of the target agent.",
    "buddy_uuid": "UUID of the target buddy.",
    "bundle_uuid": "UUID of the target bundle.",
    "ceremony_uuid": "UUID of the target ceremony.",
    "tier_set_uuid": "UUID of the target competitive tier set.",
    "content_tier_uuid": "UUID of the target content tier.",
    "contract_uuid": "UUID of the target contract.",
    "currency_uuid": "UUID of the target currency.",
    "event_uuid": "UUID of the target event.",
    "gamemode_uuid": "UUID of the target gamemode.",
    "gear_uuid": "UUID of the target gear item.",
    "level_border_uuid": "UUID of the target level border.",
    "map_uuid": "UUID of the target map.",
    "mission_uuid": "UUID of the target mission.",
    "objective_uuid": "UUID of the target objective.",
    "card_uuid": "UUID of the target player card.",
    "title_uuid": "UUID of the target player title.",
    "season_uuid": "UUID of the target season.",
    "spray_uuid": "UUID of the target spray.",
    "theme_uuid": "UUID of the target theme.",
    "weapon_uuid": "UUID of the target weapon.",
    "name": "Display name string used for wrapper-side matching.",
    "now": "Optional UTC timestamp used instead of the current time.",
}


def param_description(param_name: str) -> str:
    return PARAM_DESCRIPTIONS.get(param_name, f"{param_name.replace('_', ' ').capitalize()} parameter.")


def required_text(param: MethodParam) -> str:
    return "yes" if param.default is None and param.kind == "positional" else "no"


def default_text(param: MethodParam) -> str:
    return param.default or EM_DASH


def escape_table_cell(text: str) -> str:
    return text.replace("|", "\\|")


def render_method_section(method_doc: MethodDoc, config: ResourceMethodConfig) -> str:
    rows = []
    if method_doc.params:
        rows.extend(
            [
                ":::table",
                "| Parameter | Type | Default | Required | Description |",
                "|-----------|------|---------|----------|-------------|",
            ]
        )
        for param in method_doc.params:
            rows.append(
                f"| `{escape_table_cell(param.name)}` | `{escape_table_cell(param.annotation)}` | `{escape_table_cell(default_text(param))}` | {required_text(param)} | {escape_table_cell(param_description(param.name))} |"
            )
        rows.append(":::")
    else:
        rows.append("This method does not take caller-supplied parameters.")
    parts = [
        f"### `{method_doc.name}`",
        "",
        config.description,
        "",
        ":::method",
        f"{method_doc.name}{method_doc.signature}",
        ":::",
        "",
        f"**Returns:** `{method_doc.returns}`",
        "",
        "#### Parameters",
        "",
        *rows,
    ]
    if config.notes:
        parts.extend(["", "#### Notes", "", f":::callout info\n{config.notes}\n:::"])
    return "\n".join(parts)


def render_model_table(model_doc: ModelDoc) -> str:
    lines = [
        f"### `{model_doc.name}`",
        "",
        ":::table",
        "| Field | Type | API alias |",
        "|-------|------|-----------|",
    ]
    for field in model_doc.fields:
        alias = f"`{escape_table_cell(field.alias)}`" if field.alias else EM_DASH
        lines.append(
            f"| `{escape_table_cell(field.name)}` | `{escape_table_cell(field.annotation)}` | {alias} |"
        )
    lines.append(":::")
    return "\n".join(lines)


def render_resource_page(resource: ResourceConfig, methods: dict[str, MethodDoc], models: dict[str, ModelDoc]) -> str:
    method_blocks = "\n\n".join(render_method_section(methods[config.name], config) for config in resource.methods)
    schema_blocks = "\n\n".join(render_model_table(models[model_name]) for model_name in resource.models if model_name in models)
    notes = "\n".join(f"- {note}" for note in resource.notes)
    body = f"""
`{resource.label}` maps to the upstream `{resource.endpoint}` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1{resource.endpoint}`

{resource.summary}

## Client methods

{method_blocks}

## Schema

{schema_blocks}

## Notes

{notes if notes else "- No extra wrapper notes for this resource."}
"""
    return render_page(resource.slug, resource.label, f"{resource.summary}", body, "Reference")


def render_enums_page(enums: dict[str, EnumDoc]) -> str:
    sections: list[str] = []
    for enum_name in ["Language", "WeaponCategory", "WallPenetration", "AltFireType", "WeaponStatsFeature", "MissionType"]:
        enum_doc = enums.get(enum_name)
        if enum_doc is None:
            continue
        lines = [f"## `{enum_doc.name}`", ""]
        lines.extend(f"- `{value.name}` = `{value.value}`" for value in enum_doc.values)
        sections.append("\n".join(lines))
    body = """
The wrapper exports a small set of enums that appear across multiple resource pages.

""" + "\n\n".join(sections)
    return render_page("enums", "Enums", "Exported enum values used across the resource reference.", body, "Appendix")


def main() -> None:
    exports = set(parse_exports())
    methods = parse_client_methods()
    models = parse_models()
    enums = parse_enums(exports)

    write(ATLAS_DIR / "metadata.md", render_metadata())
    write(ATLAS_DIR / "navigation.md", render_navigation())
    write(ATLAS_DIR / "assets.md", render_assets())

    write(
        ATLAS_DIR / "content" / "introduction.md",
        render_page("introduction", "Introduction", "A typed, cached Python wrapper for Valorant content data.", INTRODUCTION, "Overview"),
    )
    write(
        ATLAS_DIR / "content" / "installation.md",
        render_page("installation", "Installation", "Install the package and understand the runtime baseline.", INSTALLATION, "Overview"),
    )
    write(
        ATLAS_DIR / "content" / "quickstart.md",
        render_page("quickstart", "Quickstart", "Construct a client and make a few real calls in under ten minutes.", QUICKSTART, "Overview"),
    )
    write(
        ATLAS_DIR / "content" / "caching-and-freshness.md",
        render_page("caching-and-freshness", "Caching and freshness", "How the wrapper stores and reuses HTTP responses by default.", CACHING, "Concepts"),
    )
    write(
        ATLAS_DIR / "content" / "typed-models-and-enums.md",
        render_page("typed-models-and-enums", "Typed models and enums", "How payloads become typed Python objects and enum-backed fields.", TYPED_MODELS, "Concepts"),
    )
    write(
        ATLAS_DIR / "content" / "media-assets-and-disk-downloads.md",
        render_page("media-assets-and-disk-downloads", "Media assets and disk downloads", "How string-like media URLs become disk-fetchable assets.", MEDIA_ASSETS, "Concepts"),
    )
    write(
        ATLAS_DIR / "content" / "common-lookup-patterns.md",
        render_page("common-lookup-patterns", "Common lookup patterns", "Consistent collection, UUID, and helper lookup flows across resources.", LOOKUP_PATTERNS, "Guides"),
    )
    write(
        ATLAS_DIR / "content" / "localization.md",
        render_page("localization", "Localization", "Using the `Language` enum and language-aware resource methods.", LOCALIZATION, "Guides"),
    )
    write(
        ATLAS_DIR / "content" / "client-configuration.md",
        render_page("client-configuration", "Client configuration", "Constructor options and session-level customization points.", CLIENT_CONFIGURATION, "Guides"),
    )
    write(
        ATLAS_DIR / "content" / "notebook-walkthrough.md",
        render_page("notebook-walkthrough", "Notebook walkthrough", "When to use the repository notebook instead of the static docs.", NOTEBOOK, "Guides"),
    )

    for resource in RESOURCE_CONFIGS:
        write(ATLAS_DIR / "content" / f"{resource.slug}.md", render_resource_page(resource, methods, models))

    write(ATLAS_DIR / "content" / "enums.md", render_enums_page(enums))
    write(
        ATLAS_DIR / "content" / "cached-media-asset.md",
        render_page("cached-media-asset", "CachedMediaAsset", "String-like media URL helper with optional disk fetching.", CACHED_MEDIA_ASSET_PAGE, "Appendix"),
    )

    DOCS_SITE_DIR.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_HTML_PUBLISHED.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(NOTEBOOK_HTML_SOURCE, NOTEBOOK_HTML_PUBLISHED)


if __name__ == "__main__":
    main()
