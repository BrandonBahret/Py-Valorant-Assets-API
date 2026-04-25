---
tag: Reference
title: Agents
lead: |
  Playable and non-playable agent data, plus role, ability, and voice metadata.
breadcrumb: "valorant-assets-api / agents"
---

`Agents` maps to the upstream `/agents` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/agents`

Playable and non-playable agent data, plus role, ability, and voice metadata.

## Client methods

### `list_agents`

List agent resources.

:::method
list_agents(*, language: LanguageLike = None, playable_only: bool = False)
:::

**Returns:** `List[Agent]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
| `playable_only` | `bool` | `False` | no | When true, requests only playable agents from the collection endpoint. |
:::

#### Notes

:::callout info
Set `playable_only=True` to request only playable characters.
:::

### `get_agent`

Fetch one agent by UUID.

:::method
get_agent(agent_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Agent`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `agent_uuid` | `str` | `-` | yes | UUID of the target agent. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `find_agent`

Find an agent by display name.

:::method
find_agent(name: str, *, language: LanguageLike = None, playable_only: bool = False)
:::

**Returns:** `Agent | None`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `name` | `str` | `-` | yes | Display name string used for wrapper-side matching. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
| `playable_only` | `bool` | `False` | no | When true, requests only playable agents from the collection endpoint. |
:::

#### Notes

:::callout info
The helper matches exact case-insensitive names before substring matches.
:::

## Schema

### `Agent`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `description` | `str | None` | - |
| `developer_name` | `str | None` | `developerName` |
| `release_date` | `datetime | None` | `releaseDate` |
| `character_tags` | `list[str] | None` | `characterTags` |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `display_icon_small` | `AssetUrl` | `displayIconSmall` |
| `bust_portrait` | `AssetUrl` | `bustPortrait` |
| `full_portrait` | `AssetUrl` | `fullPortrait` |
| `full_portrait_v2` | `AssetUrl` | `fullPortraitV2` |
| `killfeed_portrait` | `AssetUrl` | `killfeedPortrait` |
| `minimap_portrait` | `AssetUrl` | `minimapPortrait` |
| `home_screen_promo_tile_image` | `AssetUrl` | `homeScreenPromoTileImage` |
| `background` | `AssetUrl` | - |
| `background_gradient_colors` | `list[str]` | `backgroundGradientColors` |
| `asset_path` | `str | None` | `assetPath` |
| `is_full_portrait_right_facing` | `bool` | `isFullPortraitRightFacing` |
| `is_playable_character` | `bool` | `isPlayableCharacter` |
| `is_available_for_test` | `bool` | `isAvailableForTest` |
| `is_base_content` | `bool` | `isBaseContent` |
| `role` | `Role | None` | - |
| `recruitment_data` | `RecruitmentData | None` | `recruitmentData` |
| `abilities` | `list[Ability]` | - |
| `voice_line` | `VoiceLine | None` | `voiceLine` |
:::

### `Role`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `description` | `str | None` | - |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `asset_path` | `str | None` | `assetPath` |
:::

### `Ability`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `slot` | `str` | - |
| `display_name` | `str | None` | `displayName` |
| `description` | `str | None` | - |
| `display_icon` | `AssetUrl` | `displayIcon` |
:::

### `VoiceLine`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `min_duration` | `Numeric` | `minDuration` |
| `max_duration` | `Numeric` | `maxDuration` |
| `media_list` | `list[MediaAsset]` | `mediaList` |
:::

### `RecruitmentData`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `counter_id` | `str | None` | `counterId` |
| `milestone_id` | `str | None` | `milestoneId` |
| `milestone_threshold` | `int | None` | `milestoneThreshold` |
| `use_level_vp_cost_override` | `bool | None` | `useLevelVpCostOverride` |
| `level_vp_cost_override` | `int | None` | `levelVpCostOverride` |
| `start_date` | `datetime | None` | `startDate` |
| `end_date` | `datetime | None` | `endDate` |
:::

### `MediaAsset`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `id` | `int | None` | - |
| `wwise` | `AssetUrl` | - |
| `wave` | `AssetUrl` | - |
:::

## Notes

- Agent media fields such as `display_icon` and `full_portrait` are wrapped as `CachedMediaAsset` values.
- Playable filtering is a wrapper-level convenience on top of the collection endpoint.
