---
tag: Reference
title: Currencies
lead: |
  Currency metadata and reward icon fields.
breadcrumb: "valorant-assets-api / currencies"
---

`Currencies` maps to the upstream `/currencies` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/currencies`

Currency metadata and reward icon fields.

## Client methods

### `list_currencies`

List currency resources.

:::method
list_currencies(*, language: LanguageLike = None)
:::

**Returns:** `List[Currency]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_currency`

Fetch one currency by UUID.

:::method
get_currency(currency_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Currency`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `currency_uuid` | `str` | `-` | yes | UUID of the target currency. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `Currency`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_name_singular` | `str | None` | `displayNameSingular` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `large_icon` | `AssetUrl` | `largeIcon` |
| `reward_preview_icon` | `AssetUrl` | `rewardPreviewIcon` |
| `asset_path` | `str | None` | `assetPath` |
:::

## Notes

- No extra wrapper notes for this resource.
