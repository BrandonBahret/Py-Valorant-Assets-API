---
tag: Reference
title: Gamemodes
lead: |
  Gamemode metadata and nested game rule overrides.
breadcrumb: "valorant-assets-api / gamemodes"
---

`Gamemodes` maps to the upstream `/gamemodes` resource family and groups the wrapper methods with the typed models you inspect after hydration.

## Endpoint family

`https://valorant-api.com/v1/gamemodes`

Gamemode metadata and nested game rule overrides.

## Client methods

### `list_gamemodes`

List gamemode resources.

:::method
list_gamemodes(*, language: LanguageLike = None)
:::

**Returns:** `List[Gamemode]`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

### `get_gamemode`

Fetch one gamemode by UUID.

:::method
get_gamemode(gamemode_uuid: str, *, language: LanguageLike = None)
:::

**Returns:** `Gamemode`

#### Parameters

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `gamemode_uuid` | `str` | `-` | yes | UUID of the target gamemode. |
| `language` | `LanguageLike` | `None` | no | Localization code for endpoints that expose translated content. |
:::

## Schema

### `Gamemode`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `description` | `str \| None` | - |
| `duration` | `str \| None` | - |
| `display_icon` | `AssetUrl` | `displayIcon` |
| `asset_path` | `str \| None` | `assetPath` |
| `team_roles` | `list[str] \| None` | `teamRoles` |
| `game_feature_overrides` | `list[GameFeatureOverride] \| None` | `gameFeatureOverrides` |
| `game_rule_bool_overrides` | `list[GameRuleBoolOverride] \| None` | `gameRuleBoolOverrides` |
| `allows_match_timeouts` | `bool \| None` | `allowsMatchTimeouts` |
| `allows_custom_game_replays` | `bool \| None` | `allowsCustomGameReplays` |
| `is_minimap_hidden` | `bool \| None` | `isMinimapHidden` |
| `is_team_voice_allowed` | `bool \| None` | `isTeamVoiceAllowed` |
| `orb_count` | `int \| None` | `orbCount` |
| `rounds_per_half` | `int \| None` | `roundsPerHalf` |
| `economy_type` | `str \| None` | `economyType` |
| `list_view_icon_tall` | `AssetUrl` | `listViewIconTall` |
:::

### `GameFeatureOverride`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `feature_name` | `str` | `featureName` |
| `state` | `bool` | - |
:::

### `GameRuleBoolOverride`

:::table
| Field | Type | API alias |
|-------|------|-----------|
| `rule_name` | `str` | `ruleName` |
| `state` | `bool` | - |
:::

## Notes

- No extra wrapper notes for this resource.
