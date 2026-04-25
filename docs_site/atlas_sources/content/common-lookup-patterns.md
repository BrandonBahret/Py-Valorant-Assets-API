---
tag: Guides
title: Common lookup patterns
lead: |
  Consistent collection, UUID, and helper lookup flows across resources.
breadcrumb: "valorant-assets-api / common lookup patterns"
---

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
