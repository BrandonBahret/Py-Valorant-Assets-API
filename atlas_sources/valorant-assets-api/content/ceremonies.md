---
tag: Reference
title: Ceremonies
lead: |
  Ceremony metadata with lightweight schema coverage.
breadcrumb: "valorant-assets-api / ceremonies"
---

`Ceremonies` maps to the upstream `/ceremonies` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/ceremonies`

Ceremony metadata with lightweight schema coverage.

## Client methods

### `list_ceremonies`

List ceremony resources.

:::method
list_ceremonies()
:::

**Returns:** `List[Ceremony]`

#### Parameters

This method does not take caller-supplied parameters.

### `get_ceremony`

Fetch one ceremony by UUID.

:::method
get_ceremony(ceremony_uuid: str)
:::

**Returns:** `Ceremony`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `ceremony_uuid` | `str` | `-` | yes | UUID of the target ceremony. |
:::

## Schema

### `Ceremony`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- This resource does not expose `language` in the current client implementation.
