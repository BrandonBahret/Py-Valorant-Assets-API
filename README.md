# Valorant Assets API

Typed Python wrapper for the public [Valorant API](https://dash.valorant-api.com/) built on `pypercache`.

Read the [docs](https://brandonbahret.github.io/Py-Valorant-Assets-API/docs_site/index.html)

```python
from valorant_assets_api import ValorantAPI

api = ValorantAPI()

for agent in api.list_agents(playable_only=True):
    print(agent.display_name, "-", agent.role.display_name if agent.role else "No role")

current_season = api.get_current_season()
version = api.get_version()
```

## Features

- Typed `@apimodel` resources for the main `/v1` endpoints
- Built-in response caching via `pypercache`
- Optional request logging
- UUID lookups and collection methods
- Convenience helpers for playable agents, name-based lookup, active events, current season, and flattened contract rewards

## Endpoint Coverage Matrix

`list_*` and `get_*` methods map directly to public `/v1` endpoints. Helper methods compose those endpoint calls into higher-level lookups.

| Endpoint | Collection | Detail | Helpers | `language` support | Notes |
| --- | --- | --- | --- | --- | --- |
| `/agents` | `list_agents()` | `get_agent()` | `find_agent()` | Yes | `list_agents(playable_only=True)` adds `isPlayableCharacter=True` |
| `/buddies` | `list_buddies()` | `get_buddy()` | - | Yes | Direct endpoint coverage |
| `/bundles` | `list_bundles()` | `get_bundle()` | - | Yes | Direct endpoint coverage |
| `/ceremonies` | `list_ceremonies()` | `get_ceremony()` | - | No | Direct endpoint coverage |
| `/competitivetiers` | `list_competitive_tiers()` | `get_competitive_tier_set()` | - | No | Direct endpoint coverage |
| `/contenttiers` | `list_content_tiers()` | `get_content_tier()` | - | Yes | Direct endpoint coverage |
| `/contracts` | `list_contracts()` | `get_contract()` | `list_contract_rewards()` | Yes | Rewards helper flattens chapter levels from one contract |
| `/currencies` | `list_currencies()` | `get_currency()` | - | Yes | Direct endpoint coverage |
| `/events` | `list_events()` | `get_event()` | `get_active_events()` | Yes | Active-events helper filters by `start_time` and `end_time` |
| `/gamemodes` | `list_gamemodes()` | `get_gamemode()` | - | Yes | Direct endpoint coverage |
| `/gear` | `list_gear()` | `get_gear()` | - | Yes | Direct endpoint coverage |
| `/levelborders` | `list_level_borders()` | `get_level_border()` | - | Yes | Direct endpoint coverage |
| `/maps` | `list_maps()` | `get_map()` | `find_map()` | Yes | Name helper matches exact name first, then partial match |
| `/missions` | `list_missions()` | `get_mission()` | - | No | Direct endpoint coverage |
| `/objectives` | `list_objectives()` | `get_objective()` | - | No | Direct endpoint coverage |
| `/playercards` | `list_player_cards()` | `get_player_card()` | - | Yes | Direct endpoint coverage |
| `/playertitles` | `list_player_titles()` | `get_player_title()` | - | Yes | Direct endpoint coverage |
| `/seasons` | `list_seasons()` | `get_season()` | `get_current_season()` | Yes | Current-season helper selects the active season for a given time |
| `/sprays` | `list_sprays()` | `get_spray()` | - | Yes | Direct endpoint coverage |
| `/themes` | `list_themes()` | `get_theme()` | - | Yes | Direct endpoint coverage |
| `/weapons` | `list_weapons()` | `get_weapon()` | `find_weapon()` | Yes | Name helper matches exact name first, then partial match |
| `/version` | - | `get_version()` | - | No | Detail-style singleton endpoint |

The live cache hydration tests in `tests/test_live_endpoints.py` exercise every direct `list_*`/`get_*` mapping above, plus `find_agent()`, `find_map()`, `find_weapon()`, `list_contract_rewards()`, `get_active_events()`, `get_current_season()`, and `get_version()`.

## Install

```bash
pip install valorant-assets-api
```

For local development:

```bash
pip install -e .[test]
```

## Tutorial Notebook

See [notebooks/valorant_assets_api_tutorial.ipynb](notebooks/valorant_assets_api_tutorial.ipynb) for a step-by-step walkthrough of the client API, including setup, localization, UUID lookups, convenience helpers, and cache configuration.

## Documentation

For the Markdown docs reader path, start at [docs/index.md](docs/index.md).

Use the docs for onboarding, usage patterns, and generated reference pages. Use the notebook when you want a guided, interactive walkthrough instead of quick lookup.

## Release Checklist

- Add a real `LICENSE` file and declare the matching `project.license` / `project.license-files` metadata in `pyproject.toml`
- Add `authors` and/or `maintainers` metadata
- Add `[project.urls]` for homepage, repository, issues, and documentation
- Build distributions with `python -m build`
- Validate package metadata and README rendering with `python -m twine check dist/*`
