---
tag: Overview
title: Quickstart
lead: |
  Construct a client and make a few real calls in under ten minutes.
breadcrumb: "valorant-assets-api / quickstart"
---

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
