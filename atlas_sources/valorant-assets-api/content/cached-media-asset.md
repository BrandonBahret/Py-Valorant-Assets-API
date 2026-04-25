---
tag: Appendix
title: CachedMediaAsset
lead: |
  String-like media URL helper with optional disk fetching.
breadcrumb: "valorant-assets-api / cachedmediaasset"
---

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
