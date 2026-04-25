---
tag: Guides
title: Localization
lead: |
  Using the `Language` enum and language-aware resource methods.
breadcrumb: "valorant-assets-api / localization"
---

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
