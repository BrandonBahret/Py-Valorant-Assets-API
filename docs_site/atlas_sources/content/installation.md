---
tag: Overview
title: Installation
lead: |
  Install the package and understand the runtime baseline.
breadcrumb: "valorant-assets-api / installation"
---

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
