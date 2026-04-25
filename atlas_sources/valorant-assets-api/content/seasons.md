---
tag: Reference
title: Seasons
lead: |
  Season metadata plus the helper for selecting the active season.
breadcrumb: "valorant-assets-api / seasons"
---

`Seasons` maps to the upstream `/seasons` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/seasons`

Season metadata plus the helper for selecting the active season.

## Client methods

### `list_seasons`

List season resources.

:::method
list_seasons(*, language: LanguageLike = None)
:::

**Returns:** `List[Season]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_season`

Fetch one season by UUID.

:::method
get_season(season_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Season`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `season_uuid` | `str` | `-` | yes | UUID of the target season. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_current_season`

Return the active season.

:::method
get_current_season(*, language: LanguageLike = None, now: datetime | None = None)
:::

**Returns:** `Season | None`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
| `now` | `datetime | None` | `None` | no | Optional UTC timestamp used instead of the current time. |
:::

#### Notes

:::callout info
The helper compares season windows against `now` or the current UTC time and returns `None` when nothing is active.
:::

## Schema

### `Season`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `title` | `str | None` | - |
| `type` | `str | None` | - |
| `parent_uuid` | `str | None` | `parentUuid` |
| `start_time` | `datetime | None` | `startTime` |
| `end_time` | `datetime | None` | `endTime` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- `get_current_season()` is a wrapper helper layered on top of `list_seasons()`.
