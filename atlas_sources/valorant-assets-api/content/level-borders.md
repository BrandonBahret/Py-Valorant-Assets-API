---
tag: Reference
title: Level Borders
lead: |
  Level border metadata and progression display fields.
breadcrumb: "valorant-assets-api / level borders"
---

`Level Borders` maps to the upstream `/levelborders` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/levelborders`

Level border metadata and progression display fields.

## Client methods

### `list_level_borders`

List level border resources.

:::method
list_level_borders(*, language: LanguageLike = None)
:::

**Returns:** `List[LevelBorder]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_level_border`

Fetch one level border by UUID.

:::method
get_level_border(level_border_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `LevelBorder`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `level_border_uuid` | `str` | `-` | yes | UUID of the target level border. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `LevelBorder`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `starting_level` | `int` | `startingLevel` |
| `level_number` | `int` | `levelNumber` |
| `level_number_appearance` | `str | None` | `levelNumberAppearance` |
| `small_player_card_appearance` | `str | None` | `smallPlayerCardAppearance` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- No extra wrapper notes for this resource.
