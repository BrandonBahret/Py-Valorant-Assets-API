---
tag: Reference
title: Content Tiers
lead: |
  Content tier metadata used across skins and rewards.
breadcrumb: "valorant-assets-api / content tiers"
---

`Content Tiers` maps to the upstream `/contenttiers` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/contenttiers`

Content tier metadata used across skins and rewards.

## Client methods

### `list_content_tiers`

List content tier resources.

:::method
list_content_tiers(*, language: LanguageLike = None)
:::

**Returns:** `List[ContentTier]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_content_tier`

Fetch one content tier by UUID.

:::method
get_content_tier(content_tier_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `ContentTier`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `content_tier_uuid` | `str` | `-` | yes | UUID of the target content tier. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `ContentTier`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `dev_name` | `str \| None` | `devName` |
| `rank` | `int \| None` | - |
| `juice_value` | `int \| None` | `juiceValue` |
| `juice_cost` | `int \| None` | `juiceCost` |
| `highlight_color` | `str \| None` | `highlightColor` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `asset_path` | `str \| None` | `assetPath` |
:::

## Notes

- No extra wrapper notes for this resource.
