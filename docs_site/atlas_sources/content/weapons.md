---
tag: Reference
title: Weapons
lead: |
  Weapon metadata, nested stats, shop data, skins, chromas, and damage ranges.
breadcrumb: "valorant-assets-api / weapons"
---

`Weapons` maps to the upstream `/weapons` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/weapons`

Weapon metadata, nested stats, shop data, skins, chromas, and damage ranges.

## Client methods

### `list_weapons`

List weapon resources.

:::method
list_weapons(*, language: LanguageLike = None)
:::

**Returns:** `List[Weapon]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_weapon`

Fetch one weapon by UUID.

:::method
get_weapon(weapon_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Weapon`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `weapon_uuid` | `str` | `-` | yes | UUID of the target weapon. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `find_weapon`

Find a weapon by display name.

:::method
find_weapon(name: str, *, language: LanguageLike = None)
:::

**Returns:** `Weapon | None`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `name` | `str` | `-` | yes | Display name string used for wrapper-side matching. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

#### Notes

:::callout info
The helper matches exact case-insensitive names before substring matches.
:::

## Schema

### `Weapon`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `category` | `WeaponCategory \| str \| None` | - |
| `default_skin_uuid` | `str \| None` | `defaultSkinUuid` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `kill_stream_icon` | `AssetUrl` | `killStreamIcon` |
| `asset_path` | `str \| None` | `assetPath` |
| `weapon_stats` | `WeaponStats \| None` | `weaponStats` |
| `shop_data` | `ShopData \| None` | `shopData` |
| `skins` | `Lazy[list[WeaponSkin]]` | - |
:::

### `WeaponStats`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `fire_rate` | `float \| int \| None` | `fireRate` |
| `magazine_size` | `int \| None` | `magazineSize` |
| `run_speed_multiplier` | `float \| int \| None` | `runSpeedMultiplier` |
| `equip_time_seconds` | `float \| int \| None` | `equipTimeSeconds` |
| `reload_time_seconds` | `float \| int \| None` | `reloadTimeSeconds` |
| `first_bullet_accuracy` | `float \| int \| None` | `firstBulletAccuracy` |
| `shotgun_pellet_count` | `int \| None` | `shotgunPelletCount` |
| `wall_penetration` | `WallPenetration \| str \| None` | `wallPenetration` |
| `feature` | `WeaponStatsFeature \| str \| None` | - |
| `fire_mode` | `str \| None` | `fireMode` |
| `alt_fire_type` | `AltFireType \| str \| None` | `altFireType` |
| `ads_stats` | `AdsStats \| None` | `adsStats` |
| `alt_shotgun_stats` | `AltShotgunStats \| None` | `altShotgunStats` |
| `air_burst_stats` | `AirBurstStats \| None` | `airBurstStats` |
| `damage_ranges` | `list[DamageRange] \| None` | `damageRanges` |
:::

### `WeaponSkin`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `theme_uuid` | `str \| None` | `themeUuid` |
| `content_tier_uuid` | `str \| None` | `contentTierUuid` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `wallpaper` | `AssetUrl` | - |
| `asset_path` | `str \| None` | `assetPath` |
| `chromas` | `list[WeaponChroma]` | - |
| `levels` | `list[WeaponSkinLevel]` | - |
:::

### `WeaponSkinLevel`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `level_item` | `str \| None` | `levelItem` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `streamed_video` | `AssetUrl` | `streamedVideo` |
| `asset_path` | `str \| None` | `assetPath` |
:::

### `WeaponChroma`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `full_render` | `AssetUrl` | `fullRender` |
| `swatch` | `AssetUrl` | - |
| `streamed_video` | `AssetUrl` | `streamedVideo` |
| `asset_path` | `str \| None` | `assetPath` |
:::

### `DamageRange`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `range_start_meters` | `float \| int` | `rangeStartMeters` |
| `range_end_meters` | `float \| int` | `rangeEndMeters` |
| `head_damage` | `float \| int` | `headDamage` |
| `body_damage` | `float \| int` | `bodyDamage` |
| `leg_damage` | `float \| int` | `legDamage` |
:::

### `AdsStats`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `zoom_multiplier` | `float \| int \| None` | `zoomMultiplier` |
| `fire_rate` | `float \| int \| None` | `fireRate` |
| `run_speed_multiplier` | `float \| int \| None` | `runSpeedMultiplier` |
| `burst_count` | `int \| None` | `burstCount` |
| `first_bullet_accuracy` | `float \| int \| None` | `firstBulletAccuracy` |
:::

### `AltShotgunStats`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `shotgun_pellet_count` | `int \| None` | `shotgunPelletCount` |
| `burst_rate` | `float \| int \| None` | `burstRate` |
:::

### `AirBurstStats`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `shotgun_pellet_count` | `int \| None` | `shotgunPelletCount` |
| `burst_distance` | `float \| int \| None` | `burstDistance` |
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

- Weapon and skin image or video fields are wrapped as `CachedMediaAsset` values when present.
