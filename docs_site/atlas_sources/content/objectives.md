---
tag: Reference
title: Objectives
lead: |
  Objective metadata used by mission payloads.
breadcrumb: "valorant-assets-api / objectives"
---

`Objectives` maps to the upstream `/objectives` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/objectives`

Objective metadata used by mission payloads.

## Client methods

### `list_objectives`

List objective resources.

:::method
list_objectives()
:::

**Returns:** `List[Objective]`

#### Parameters

This method does not take caller-supplied parameters.

#### Notes

:::callout info
The client applies a 30 minute expiry override.
:::

### `get_objective`

Fetch one objective by UUID.

:::method
get_objective(objective_uuid: str)
:::

**Returns:** `Objective`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `objective_uuid` | `str` | `-` | yes | UUID of the target objective. |
:::

#### Notes

:::callout info
The client applies a 30 minute expiry override.
:::

## Schema

### `Objective`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `directive` | `str | None` | - |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- This resource does not expose `language` in the current client implementation.
