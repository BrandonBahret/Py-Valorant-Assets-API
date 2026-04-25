---
tag: Reference
title: Contracts
lead: |
  Contract data, reward schedules, and flattened reward helper output.
breadcrumb: "valorant-assets-api / contracts"
---

`Contracts` maps to the upstream `/contracts` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/contracts`

Contract data, reward schedules, and flattened reward helper output.

## Client methods

### `list_contracts`

List contract resources.

:::method
list_contracts(*, language: LanguageLike = None)
:::

**Returns:** `List[Contract]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_contract`

Fetch one contract by UUID.

:::method
get_contract(contract_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Contract`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `contract_uuid` | `str` | `-` | yes | UUID of the target contract. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `list_contract_rewards`

Flatten all chapter levels from one contract.

:::method
list_contract_rewards(contract_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `List[ContractLevel]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `contract_uuid` | `str` | `-` | yes | UUID of the target contract. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

#### Notes

:::callout info
This helper returns `ContractLevel` items rather than a top-level exported model.
:::

## Schema

### `Contract`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `ship_it` | `bool \| None` | `shipIt` |
| `use_level_vp_cost_override` | `bool \| None` | `useLevelVPCostOverride` |
| `level_vp_cost_override` | `int \| None` | `levelVPCostOverride` |
| `free_reward_schedule_uuid` | `str \| None` | `freeRewardScheduleUuid` |
| `content` | `Lazy[ContractContent]` | - |
| `asset_path` | `str \| None` | `assetPath` |
:::

### `ContractContent`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `relation_type` | `str \| None` | `relationType` |
| `relation_uuid` | `str \| None` | `relationUuid` |
| `chapters` | `Lazy[list[ContractChapter]]` | - |
| `premium_reward_schedule_uuid` | `str \| None` | `premiumRewardScheduleUuid` |
| `premium_vp_cost` | `int \| None` | `premiumVPCost` |
:::

### `ContractChapter`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `is_epilogue` | `bool` | `isEpilogue` |
| `levels` | `list[ContractLevel]` | - |
| `free_rewards` | `list[Reward] \| None` | `freeRewards` |
:::

### `ContractLevel`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `reward` | `Reward \| None` | - |
| `xp` | `int` | - |
| `vp_cost` | `int \| None` | `vpCost` |
| `is_purchasable_with_vp` | `bool \| None` | `isPurchasableWithVP` |
| `dough_cost` | `int \| None` | `doughCost` |
| `is_purchasable_with_dough` | `bool \| None` | `isPurchasableWithDough` |
:::

### `Reward`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `type` | `str` | - |
| `uuid` | `str` | - |
| `amount` | `int` | - |
| `is_highlighted` | `bool` | `isHighlighted` |
:::

## Notes

- `list_contract_rewards()` is wrapper-specific and does not map to a direct endpoint.
