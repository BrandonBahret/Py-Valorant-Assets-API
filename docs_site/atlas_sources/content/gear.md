---
tag: Reference
title: Gear
lead: |
  Gear metadata, nested shop data, and descriptive detail rows.
breadcrumb: "valorant-assets-api / gear"
---

`Gear` maps to the upstream `/gear` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/gear`

Gear metadata, nested shop data, and descriptive detail rows.

## Client methods

### `list_gear`

List gear resources.

:::method
list_gear(*, language: LanguageLike = None)
:::

**Returns:** `List[Gear]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_gear`

Fetch one gear item by UUID.

:::method
get_gear(gear_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Gear`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `gear_uuid` | `str` | `-` | yes | UUID of the target gear item. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `Gear`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `description` | `str \| None` | - |
| `descriptions` | `list[str] \| None` | - |
| `details` | `list[GearDetail] \| None` | - |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `asset_path` | `str \| None` | `assetPath` |
| `shop_data` | `ShopData \| None` | `shopData` |
:::

### `GearDetail`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `name` | `str` | - |
| `value` | `str \| None` | - |
:::

### `ShopData`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `cost` | `int \| None` | - |
| `category` | `str \| None` | - |
| `shop_order_priority` | `int \| None` | `shopOrderPriority` |
| `category_text` | `str \| None` | `categoryText` |
| `grid_position` | `ShopGridPosition \| None` | `gridPosition` |
| `can_be_trashed` | `bool \| None` | `canBeTrashed` |
| `image` | `AssetUrl` | - |
| `new_image` | `AssetUrl` | `newImage` |
| `new_image_2` | `AssetUrl` | `newImage2` |
| `asset_path` | `str \| None` | `assetPath` |
:::

### `ShopGridPosition`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `row` | `int \| None` | - |
| `column` | `int \| None` | - |
:::

## Notes

- No extra wrapper notes for this resource.
