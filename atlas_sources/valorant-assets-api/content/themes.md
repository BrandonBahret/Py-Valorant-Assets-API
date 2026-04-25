---
tag: Reference
title: Themes
lead: |
  Theme metadata and store artwork fields.
breadcrumb: "valorant-assets-api / themes"
---

`Themes` maps to the upstream `/themes` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/themes`

Theme metadata and store artwork fields.

## Client methods

### `list_themes`

List theme resources.

:::method
list_themes(*, language: LanguageLike = None)
:::

**Returns:** `List[Theme]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_theme`

Fetch one theme by UUID.

:::method
get_theme(theme_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Theme`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `theme_uuid` | `str` | `-` | yes | UUID of the target theme. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `Theme`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `store_featured_image` | `AssetUrl` | `storeFeaturedImage` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- No extra wrapper notes for this resource.
