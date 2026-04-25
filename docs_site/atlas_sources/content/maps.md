---
tag: Reference
title: Maps
lead: |
  Map metadata, coordinate helpers, and nested callout positions.
breadcrumb: "valorant-assets-api / maps"
---

`Maps` maps to the upstream `/maps` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/maps`

Map metadata, coordinate helpers, and nested callout positions.

## Client methods

### `list_maps`

List map resources.

:::method
list_maps(*, language: LanguageLike = None)
:::

**Returns:** `List[MapInfo]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_map`

Fetch one map by UUID.

:::method
get_map(map_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `MapInfo`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `map_uuid` | `str` | `-` | yes | UUID of the target map. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `find_map`

Find a map by display name.

:::method
find_map(name: str, *, language: LanguageLike = None)
:::

**Returns:** `MapInfo | None`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `name` | `str` | `-` | yes | Display name string used for wrapper-side matching. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

#### Notes

:::callout info
The helper matches exact case-insensitive names before substring matches.
:::

## Schema

### `MapInfo`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `narrative_description` | `str \| None` | `narrativeDescription` |
| `tactical_description` | `str \| None` | `tacticalDescription` |
| `coordinates` | `str \| None` | - |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `list_view_icon` | `AssetUrl` | `listViewIcon` |
| `list_view_icon_tall` | `AssetUrl` | `listViewIconTall` |
| `splash` | `AssetUrl` | - |
| `stylized_background_image` | `AssetUrl` | `stylizedBackgroundImage` |
| `premier_background_image` | `AssetUrl` | `premierBackgroundImage` |
| `asset_path` | `str \| None` | `assetPath` |
| `map_url` | `str \| None` | `mapUrl` |
| `x_multiplier` | `Numeric` | `xMultiplier` |
| `y_multiplier` | `Numeric` | `yMultiplier` |
| `x_scalar_to_add` | `Numeric` | `xScalarToAdd` |
| `y_scalar_to_add` | `Numeric` | `yScalarToAdd` |
| `callouts` | `Lazy[list[Callout] \| None] \| None` | - |
:::

### `Callout`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `region_name` | `str` | `regionName` |
| `super_region` | `str \| None` | `superRegion` |
| `super_region_name` | `str \| None` | `superRegionName` |
| `location` | `Position3D` | - |
| `scale_3d` | `Position3D \| None` | `scale3D` |
| `rotation` | `Rotation3D \| None` | - |
:::

### `Position3D`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `x` | `float \| int` | - |
| `y` | `float \| int` | - |
| `z` | `float \| int` | - |
:::

### `Rotation3D`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `pitch` | `float \| int` | - |
| `yaw` | `float \| int` | - |
| `roll` | `float \| int` | - |
:::

## Notes

- Map image fields are wrapped as `CachedMediaAsset` values when present.
