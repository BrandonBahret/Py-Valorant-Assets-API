---
tag: Reference
title: Missions
lead: |
  Mission metadata and nested objective progress rows.
breadcrumb: "valorant-assets-api / missions"
---

`Missions` maps to the upstream `/missions` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/missions`

Mission metadata and nested objective progress rows.

## Client methods

### `list_missions`

List mission resources.

:::method
list_missions()
:::

**Returns:** `List[Mission]`

#### Parameters

This method does not take caller-supplied parameters.

#### Notes

:::callout info
The client applies a 30 minute expiry override.
:::

### `get_mission`

Fetch one mission by UUID.

:::method
get_mission(mission_uuid: str)
:::

**Returns:** `Mission`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `mission_uuid` | `str` | `-` | yes | UUID of the target mission. |
:::

#### Notes

:::callout info
The client applies a 30 minute expiry override.
:::

## Schema

### `Mission`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str | None` | `displayName` |
| `title` | `str | None` | - |
| `type` | `MissionType | str | None` | - |
| `xp_grant` | `int | None` | `xpGrant` |
| `progress_to_complete` | `int | None` | `progressToComplete` |
| `activation_date` | `datetime | None` | `activationDate` |
| `expiration_date` | `datetime | None` | `expirationDate` |
| `tags` | `list[str] | None` | - |
| `objectives` | `list[MissionObjectiveProgress] | None` | - |
| `asset_path` | `str | None` | `assetPath` |
:::

### `MissionObjectiveProgress`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `objective_uuid` | `str` | `objectiveUuid` |
| `value` | `int` | - |
:::

## Notes

- This resource does not expose `language` in the current client implementation.
