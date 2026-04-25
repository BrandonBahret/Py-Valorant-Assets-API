---
tag: Reference
title: Player Titles
lead: |
  Player title metadata and title text fields.
breadcrumb: "valorant-assets-api / player titles"
---

`Player Titles` maps to the upstream `/playertitles` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/playertitles`

Player title metadata and title text fields.

## Client methods

### `list_player_titles`

List player title resources.

:::method
list_player_titles(*, language: LanguageLike = None)
:::

**Returns:** `List[PlayerTitle]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_player_title`

Fetch one player title by UUID.

:::method
get_player_title(title_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `PlayerTitle`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `title_uuid` | `str` | `-` | yes | UUID of the target player title. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `PlayerTitle`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str \| None` | `displayName` |
| `title_text` | `str \| None` | `titleText` |
| `is_hidden_if_not_owned` | `bool \| None` | `isHiddenIfNotOwned` |
| `asset_path` | `str \| None` | `assetPath` |
:::

## Notes

- No extra wrapper notes for this resource.
