---
tag: Reference
title: Events
lead: |
  Event metadata plus wrapper-level active window filtering.
breadcrumb: "valorant-assets-api / events"
---

`Events` maps to the upstream `/events` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/events`

Event metadata plus wrapper-level active window filtering.

## Client methods

### `list_events`

List event resources.

:::method
list_events(*, language: LanguageLike = None)
:::

**Returns:** `List[Event]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_event`

Fetch one event by UUID.

:::method
get_event(event_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Event`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `event_uuid` | `str` | `-` | yes | UUID of the target event. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_active_events`

Return currently active events.

:::method
get_active_events(*, language: LanguageLike = None, now: datetime | None = None)
:::

**Returns:** `List[Event]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
| `now` | `datetime | None` | `None` | no | Optional UTC timestamp used instead of the current time. |
:::

#### Notes

:::callout info
The helper compares event windows against `now` or the current UTC time.
:::

## Schema

### `Event`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str | None` | `displayName` |
| `short_display_name` | `str | None` | `shortDisplayName` |
| `start_time` | `datetime | None` | `startTime` |
| `end_time` | `datetime | None` | `endTime` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- `get_active_events()` is a wrapper helper layered on top of `list_events()`.
