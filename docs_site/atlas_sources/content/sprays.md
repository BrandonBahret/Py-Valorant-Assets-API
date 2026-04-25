---
tag: Reference
title: Sprays
lead: |
  Spray metadata, art assets, and nested spray levels.
breadcrumb: "valorant-assets-api / sprays"
---

`Sprays` maps to the upstream `/sprays` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/sprays`

Spray metadata, art assets, and nested spray levels.

## Client methods

### `list_sprays`

List spray resources.

:::method
list_sprays(*, language: LanguageLike = None)
:::

**Returns:** `List[Spray]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_spray`

Fetch one spray by UUID.

:::method
get_spray(spray_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Spray`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `spray_uuid` | `str` | `-` | yes | UUID of the target spray. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `Spray`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `category` | `str \| None` | - |
| `theme_uuid` | `str \| None` | `themeUuid` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `full_icon` | `AssetUrl` | `fullIcon` |
| `full_transparent_icon` | `AssetUrl` | `fullTransparentIcon` |
| `animation_gif` | `AssetUrl` | `animationGif` |
| `animation_png` | `AssetUrl` | `animationPng` |
| `hide_if_not_owned` | `bool \| None` | `hideIfNotOwned` |
| `is_null_spray` | `bool \| None` | `isNullSpray` |
| `asset_path` | `str \| None` | `assetPath` |
| `levels` | `Lazy[list[SprayLevel]]` | - |
:::

### `SprayLevel`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `spray_level` | `int \| None` | `sprayLevel` |
| `display_name` | `str` | `displayName` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `asset_path` | `str \| None` | `assetPath` |
:::

## Notes

- Animation and icon fields are wrapped as `CachedMediaAsset` values when present.
