# Valorant Assets API

A typed Python wrapper for the public [Valorant API](https://dash.valorant-api.com/), built on `pypercache`.

## Features

- Typed `@apimodel` schema resources for the main `/v1` endpoints
- Built-in response caching via `pypercache`
- UUID lookups and collection methods
- Convenience helpers for playable agents, name-based lookup, active events, current season, and flattened contract rewards
- Convenience helpers for downloading assets and finding their path on disk
- Optional request logging

## Install

```bash
pip install valorant-assets-api
```

For local development:

```bash
pip install -e .[test]
```

## Usage

```python
from valorant_assets_api import ValorantAPI

api = ValorantAPI()

for agent in api.list_agents(playable_only=True):
    print(agent.display_name, "-", agent.role.display_name if agent.role else "No role")

current_season = api.get_current_season()
version = api.get_version()
```

## Documentation & Tutorial

Read the [docs](https://brandonbahret.github.io/Py-Valorant-Assets-API/docs_site/index.html) online, or start at [docs/index.md](docs/index.md) for the Markdown version.

For a step-by-step walkthrough covering setup, localization, UUID lookups, convenience helpers, and cache configuration, see the [tutorial notebook](notebooks/valorant_assets_api_tutorial.ipynb).

## Endpoint Coverage

`list_*` and `get_*` methods map directly to public `/v1` endpoints. Helper methods compose those calls into higher-level lookups.

| Endpoint | Collection | Detail | Helpers |
| --- | --- | --- | --- |
| `/agents` | `list_agents()` | `get_agent()` | `find_agent()` |
| `/buddies` | `list_buddies()` | `get_buddy()` | - |
| `/bundles` | `list_bundles()` | `get_bundle()` | - |
| `/ceremonies` | `list_ceremonies()` | `get_ceremony()` | - |
| `/competitivetiers` | `list_competitive_tiers()` | `get_competitive_tier_set()` | - |
| `/contenttiers` | `list_content_tiers()` | `get_content_tier()` | - |
| `/contracts` | `list_contracts()` | `get_contract()` | `list_contract_rewards()` |
| `/currencies` | `list_currencies()` | `get_currency()` | - |
| `/events` | `list_events()` | `get_event()` | `get_active_events()` |
| `/gamemodes` | `list_gamemodes()` | `get_gamemode()` | - |
| `/gear` | `list_gear()` | `get_gear()` | - |
| `/levelborders` | `list_level_borders()` | `get_level_border()` | - |
| `/maps` | `list_maps()` | `get_map()` | `find_map()` |
| `/missions` | `list_missions()` | `get_mission()` | - |
| `/objectives` | `list_objectives()` | `get_objective()` | - |
| `/playercards` | `list_player_cards()` | `get_player_card()` | - |
| `/playertitles` | `list_player_titles()` | `get_player_title()` | - |
| `/seasons` | `list_seasons()` | `get_season()` | `get_current_season()` |
| `/sprays` | `list_sprays()` | `get_spray()` | - |
| `/themes` | `list_themes()` | `get_theme()` | - |
| `/weapons` | `list_weapons()` | `get_weapon()` | `find_weapon()` |
| `/version` | - | `get_version()` | - |