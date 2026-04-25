---
tag: Reference
title: Version
lead: |
  Current Valorant client and manifest version metadata.
breadcrumb: "valorant-assets-api / version"
---

`Version` maps to the upstream `/version` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/version`

Current Valorant client and manifest version metadata.

## Client methods

### `get_version`

Fetch the current version metadata.

:::method
get_version()
:::

**Returns:** `ValorantVersion`

#### Parameters

This method does not take caller-supplied parameters.

#### Notes

:::callout info
The client applies a 1 hour expiry override.
:::

## Schema

### `ValorantVersion`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `manifest_id` | `str \| None` | `manifestId` |
| `branch` | `str \| None` | - |
| `version` | `str \| None` | - |
| `build_version` | `str \| None` | `buildVersion` |
| `engine_version` | `str \| None` | `engineVersion` |
| `riot_client_version` | `str \| None` | `riotClientVersion` |
| `riot_client_build` | `str \| None` | `riotClientBuild` |
| `build_date` | `datetime \| None` | `buildDate` |
:::

## Notes

- This resource does not expose `language` in the current client implementation.
