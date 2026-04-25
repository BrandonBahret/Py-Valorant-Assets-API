---
tag: Concepts
title: Typed models and enums
lead: |
  How payloads become typed Python objects and enum-backed fields.
breadcrumb: "valorant-assets-api / typed models and enums"
---

The wrapper hydrates API payloads into typed Python objects using `@apimodel` definitions from `valorant_assets_api.models`. That means resource pages can document the client call and the resulting schema together.

## What typed hydration changes

- You access fields as attributes instead of dictionary keys.
- Nested objects such as `Agent.role` or `Weapon.weapon_stats` are hydrated into nested models.
- Enum-backed fields are coerced into exported enums where possible.
- Timestamp fields are converted to `datetime` objects.

## Exported models vs nested helper models

The package root exports the main top-level resource models. Many resource pages also include nested helper models that are not exported from `valorant_assets_api.__init__`, but they still matter when you inspect real responses.

:::callout info
When a field type is written as `Enum | str | None`, the client tries to coerce known values into the enum while still tolerating unexpected upstream values.
:::

## Shared references

- [doc:enums] for exported enum values
- [doc:cached-media-asset] for media URL behavior
