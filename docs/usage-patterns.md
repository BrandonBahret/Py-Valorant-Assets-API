# Usage Patterns

This page covers the practical usage patterns that matter once you have a client instance and want predictable results without reading the full source.

## Localization

Many content endpoints accept a `language` parameter.

```python
from valorant_assets_api import Language, ValorantAPI

api = ValorantAPI()
agents = api.list_agents(language=Language.JA_JP, playable_only=True)
```

Use the `Language` enum when you want discoverable supported values. A plain string also works for the language-aware methods, which is helpful when the language comes from configuration or user input.

## UUID Lookups

If you already know the UUID for a resource, prefer the `get_*` methods.

```python
agent = api.get_agent("add6443a-41bd-e414-f6ad-e58d267f4e95")
weapon = api.get_weapon("63e5c1e4-4f5c-41e8-aad5-5a7c3c1f2e0f")
```

This is the most direct path when you are storing identifiers from a previous call, from a database, or from your own application state.

## Name-Based Helpers

If you are exploring interactively, `find_*` is usually faster than pulling a full list and filtering it yourself.

```python
agent = api.find_agent("Jett", playable_only=True)
map_info = api.find_map("Ascent")
weapon = api.find_weapon("Vandal")
```

These helpers compare against `display_name`, first by exact case-insensitive match and then by substring match. They are convenience methods, not a fuzzy-search system, so treat them as a shortcut for straightforward lookups.

## Cache Behavior

Caching is central to how this wrapper is meant to be used.

```python
api = ValorantAPI(cache_path="cache/valorant.db", default_expiry=60 * 60 * 6)
```

A few practical rules:

- Use the default cache if you just need a fast local setup.
- Lower `default_expiry` when you want fresher metadata during development or testing.
- Point `cache_path` at a project-specific file if you want reproducible local state instead of temp-directory cache data.
- Expect the wrapper to feel fast on repeated calls because many responses are served from cache.

## Request Logging

If you want visibility into network activity, enable request logging.

```python
api = ValorantAPI(request_log_path="logs/valorant-requests.log")
```

This is useful when you are validating which endpoints are hit, confirming cache behavior, or debugging how your own code traverses the client surface.

## Timeout And Session Customization

You can change the request timeout or provide your own `requests.Session`.

```python
import requests
from valorant_assets_api import ValorantAPI

session = requests.Session()
session.headers["X-Debug"] = "true"

api = ValorantAPI(timeout=10, session=session)
```

Use a custom session when you want shared headers, custom adapters, or other `requests`-level behavior. Use the built-in session path when you just want the wrapper defaults and do not need extra HTTP customization.

## Convenience Methods

Some methods package common workflows so you do not have to write them yourself:

- `get_active_events()` filters events against the current time.
- `get_current_season()` returns the active season when one exists.
- `list_contract_rewards()` flattens contract chapter rewards into one list.

Those methods are worth using because they encode wrapper-level behavior rather than just mirroring a raw endpoint.
