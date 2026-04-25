---
tag: Reference
title: Player Cards
lead: |
  Player card metadata and the associated art variants.
breadcrumb: "valorant-assets-api / player cards"
---

`Player Cards` maps to the upstream `/playercards` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/playercards`

Player card metadata and the associated art variants.

## Client methods

### `list_player_cards`

List player card resources.

:::method
list_player_cards(*, language: LanguageLike = None)
:::

**Returns:** `List[PlayerCard]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_player_card`

Fetch one player card by UUID.

:::method
get_player_card(card_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `PlayerCard`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `card_uuid` | `str` | `-` | yes | UUID of the target player card. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `PlayerCard`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `is_hidden_if_not_owned` | `bool | None` | `isHiddenIfNotOwned` |
| `theme_uuid` | `str | None` | `themeUuid` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `small_art` | `AssetUrl` | `smallArt` |
| `wide_art` | `AssetUrl` | `wideArt` |
| `large_art` | `AssetUrl` | `largeArt` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- Art fields such as `small_art`, `wide_art`, and `large_art` are wrapped as `CachedMediaAsset` values.
