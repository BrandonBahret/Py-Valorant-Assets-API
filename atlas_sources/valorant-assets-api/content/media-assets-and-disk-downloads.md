---
tag: Concepts
title: Media assets and disk downloads
lead: |
  How string-like media URLs become disk-fetchable assets.
breadcrumb: "valorant-assets-api / media assets and disk downloads"
---

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
