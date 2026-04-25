---
tag: Reference
title: Bundles
lead: |
  Store bundle metadata and associated imagery.
breadcrumb: "valorant-assets-api / bundles"
---

`Bundles` maps to the upstream `/bundles` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/bundles`

Store bundle metadata and associated imagery.

## Client methods

### `list_bundles`

List bundle resources.

:::method
list_bundles(*, language: LanguageLike = None)
:::

**Returns:** `List[Bundle]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_bundle`

Fetch one bundle by UUID.

:::method
get_bundle(bundle_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Bundle`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `bundle_uuid` | `str` | `-` | yes | UUID of the target bundle. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `Bundle`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_name_sub_text` | `str | None` | `displayNameSubText` |
| `description` | `str | None` | - |
| `extra_description` | `str | None` | `extraDescription` |
| `promo_description` | `str | None` | `promoDescription` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `display_icon_2` | `AssetUrl` | `displayIcon2` |
| `display_icon_3` | `AssetUrl` | `displayIcon3` |
| `vertical_promo_image` | `AssetUrl` | `verticalPromoImage` |
| `use_additional_context` | `bool | None` | `useAdditionalContext` |
| `logo_icon` | `AssetUrl` | `logoIcon` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- Bundle image fields are wrapped as `CachedMediaAsset` values when present.
