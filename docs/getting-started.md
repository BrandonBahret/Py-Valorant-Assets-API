# Getting Started

`valorant_assets_api` is built for the common case where you want Valorant content data quickly, with typed objects and cache-backed requests, without hand-mapping JSON into your own structures.

## Install

```bash
pip install -e .
```

## Construct a Client

```python
from valorant_assets_api import ValorantAPI

api = ValorantAPI()
```

By default, the client uses:

- the public `https://valorant-api.com/v1` origin
- a local SQLite cache file in your system temp directory
- a 24 hour default cache expiry
- a 20 second request timeout

That default behavior is a feature, not an implementation detail. Most wrapper calls return content metadata that does not change constantly, so caching is part of the normal usage model.

## First Useful Calls

```python
from valorant_assets_api import ValorantAPI

api = ValorantAPI()

agents = api.list_agents(playable_only=True)
brimstone = api.find_agent("Brimstone")
bind_map = api.find_map("Bind")
version = api.get_version()
```

These calls show the three lookup styles you will use most often:

- `list_*` returns a collection of typed models.
- `get_*` fetches one resource when you already have a UUID.
- `find_*` is a convenience helper for display-name lookup when you do not want to do your own filtering.

## Typed Models

Collection methods return rich objects, not raw dictionaries:

```python
agent = api.list_agents(playable_only=True)[0]

print(agent.display_name)
print(agent.role.display_name if agent.role else "No role")
print(agent.abilities[0].slot)
```

Many top-level resources also contain nested models and enums. That means you can inspect fields directly in Python and still keep strong structure when a response contains deeper objects like `role`, `shop_data`, or `weapon_stats`.

## Where To Go Next

- Read [Usage Patterns](usage-patterns.md) for localization, UUID workflows, and cache customization.
- Read [Tutorials](tutorials.md) if you want a guided notebook walkthrough.
- Use the [Reference](reference/index.md) pages when you need quick signatures or field lookup.
