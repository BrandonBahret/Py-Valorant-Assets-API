---
tag: Reference
title: Competitive Tiers
lead: |
  Competitive rank set data and nested tier definitions.
breadcrumb: "valorant-assets-api / competitive tiers"
---

`Competitive Tiers` maps to the upstream `/competitivetiers` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/competitivetiers`

Competitive rank set data and nested tier definitions.

## Client methods

### `list_competitive_tiers`

List competitive tier sets.

:::method
list_competitive_tiers()
:::

**Returns:** `List[CompetitiveTierSet]`

#### Parameters

This method does not take caller-supplied parameters.

#### Notes

:::callout info
The client applies a 12 hour expiry override.
:::

### `get_competitive_tier_set`

Fetch one competitive tier set by UUID.

:::method
get_competitive_tier_set(tier_set_uuid: str)
:::

**Returns:** `CompetitiveTierSet`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `tier_set_uuid` | `str` | `-` | yes | UUID of the target competitive tier set. |
:::

#### Notes

:::callout info
The client applies a 12 hour expiry override.
:::

## Schema

### `CompetitiveTierSet`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `asset_object_name` | `str | None` | `assetObjectName` |
| `asset_path` | `str | None` | `assetPath` |
| `tiers` | `Lazy[list[CompetitiveTier]]` | - |
:::

### `CompetitiveTier`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `tier` | `int` | - |
| `tier_name` | `str` | `tierName` |
| `division` | `str` | - |
| `division_name` | `str` | `divisionName` |
| `color` | `str | None` | - |
| `background_color` | `str | None` | `backgroundColor` |
| `small_icon` | `AssetUrl` | `smallIcon` |
| `large_icon` | `AssetUrl` | `largeIcon` |
| `rank_triangle_down_icon` | `AssetUrl` | `rankTriangleDownIcon` |
| `rank_triangle_up_icon` | `AssetUrl` | `rankTriangleUpIcon` |
:::

## Notes

- This resource does not expose `language` in the current client implementation.
