---
tag: Reference
title: Buddies
lead: |
  Gun buddy collection and buddy level metadata.
breadcrumb: "valorant-assets-api / buddies"
---

`Buddies` maps to the upstream `/buddies` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/buddies`

Gun buddy collection and buddy level metadata.

## Client methods

### `list_buddies`

List buddy resources.

:::method
list_buddies(*, language: LanguageLike = None)
:::

**Returns:** `List[Buddy]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_buddy`

Fetch one buddy by UUID.

:::method
get_buddy(buddy_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Buddy`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `buddy_uuid` | `str` | `-` | yes | UUID of the target buddy. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `Buddy`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `is_hidden_if_not_owned` | `bool \| None` | `isHiddenIfNotOwned` |
| `theme_uuid` | `str \| None` | `themeUuid` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `asset_path` | `str \| None` | `assetPath` |
| `levels` | `Lazy[list[BuddyLevel]]` | - |
:::

### `BuddyLevel`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `charm_level` | `int \| None` | `charmLevel` |
| `hide_if_not_owned` | `bool \| None` | `hideIfNotOwned` |
| `display_name` | `str` | `displayName` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `asset_path` | `str \| None` | `assetPath` |
:::

## Notes

- `levels` is represented as a nested lazy list on the hydrated buddy model.
