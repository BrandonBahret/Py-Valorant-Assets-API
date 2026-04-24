# Model Reference

> Generated file. Do not edit by hand. Run `python scripts/generate_reference_docs.py`.

Exported models are listed here for quick field lookup. Many nested helper models exist in source even when they are not re-exported at the package root.

## `Agent`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `description` | `str | None` | - |
| `developer_name` | `str | None` | `developerName` |
| `release_date` | `datetime | None` | `releaseDate` |
| `character_tags` | `list[str] | None` | `characterTags` |
| `display_icon` | `str | None` | `displayIcon` |
| `display_icon_small` | `str | None` | `displayIconSmall` |
| `bust_portrait` | `str | None` | `bustPortrait` |
| `full_portrait` | `str | None` | `fullPortrait` |
| `full_portrait_v2` | `str | None` | `fullPortraitV2` |
| `killfeed_portrait` | `str | None` | `killfeedPortrait` |
| `minimap_portrait` | `str | None` | `minimapPortrait` |
| `home_screen_promo_tile_image` | `str | None` | `homeScreenPromoTileImage` |
| `background` | `str | None` | - |
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

## `Buddy`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `is_hidden_if_not_owned` | `bool | None` | `isHiddenIfNotOwned` |
| `theme_uuid` | `str | None` | `themeUuid` |
| `display_icon` | `str | None` | `displayIcon` |
| `asset_path` | `str | None` | `assetPath` |
| `levels` | `Lazy[list[BuddyLevel]]` | - |

## `Bundle`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_name_sub_text` | `str | None` | `displayNameSubText` |
| `description` | `str | None` | - |
| `extra_description` | `str | None` | `extraDescription` |
| `promo_description` | `str | None` | `promoDescription` |
| `display_icon` | `str | None` | `displayIcon` |
| `display_icon_2` | `str | None` | `displayIcon2` |
| `display_icon_3` | `str | None` | `displayIcon3` |
| `vertical_promo_image` | `str | None` | `verticalPromoImage` |
| `use_additional_context` | `bool | None` | `useAdditionalContext` |
| `logo_icon` | `str | None` | `logoIcon` |
| `asset_path` | `str | None` | `assetPath` |

## `Ceremony`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `asset_path` | `str | None` | `assetPath` |

## `CompetitiveTierSet`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `asset_object_name` | `str | None` | `assetObjectName` |
| `asset_path` | `str | None` | `assetPath` |
| `tiers` | `Lazy[list[CompetitiveTier]]` | - |

## `ContentTier`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `dev_name` | `str | None` | `devName` |
| `rank` | `int | None` | - |
| `juice_value` | `int | None` | `juiceValue` |
| `juice_cost` | `int | None` | `juiceCost` |
| `highlight_color` | `str | None` | `highlightColor` |
| `display_icon` | `str | None` | `displayIcon` |
| `asset_path` | `str | None` | `assetPath` |

## `Contract`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_icon` | `str | None` | `displayIcon` |
| `ship_it` | `bool | None` | `shipIt` |
| `use_level_vp_cost_override` | `bool | None` | `useLevelVPCostOverride` |
| `level_vp_cost_override` | `int | None` | `levelVPCostOverride` |
| `free_reward_schedule_uuid` | `str | None` | `freeRewardScheduleUuid` |
| `content` | `Lazy[ContractContent]` | - |
| `asset_path` | `str | None` | `assetPath` |

## `Currency`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_name_singular` | `str | None` | `displayNameSingular` |
| `display_icon` | `str | None` | `displayIcon` |
| `large_icon` | `str | None` | `largeIcon` |
| `reward_preview_icon` | `str | None` | `rewardPreviewIcon` |
| `asset_path` | `str | None` | `assetPath` |

## `Event`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str | None` | `displayName` |
| `short_display_name` | `str | None` | `shortDisplayName` |
| `start_time` | `datetime | None` | `startTime` |
| `end_time` | `datetime | None` | `endTime` |
| `asset_path` | `str | None` | `assetPath` |

## `Gamemode`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `description` | `str | None` | - |
| `duration` | `str | None` | - |
| `display_icon` | `str | None` | `displayIcon` |
| `asset_path` | `str | None` | `assetPath` |
| `team_roles` | `list[str] | None` | `teamRoles` |
| `game_feature_overrides` | `list[GameFeatureOverride] | None` | `gameFeatureOverrides` |
| `game_rule_bool_overrides` | `list[GameRuleBoolOverride] | None` | `gameRuleBoolOverrides` |
| `allows_match_timeouts` | `bool | None` | `allowsMatchTimeouts` |
| `allows_custom_game_replays` | `bool | None` | `allowsCustomGameReplays` |
| `is_minimap_hidden` | `bool | None` | `isMinimapHidden` |
| `is_team_voice_allowed` | `bool | None` | `isTeamVoiceAllowed` |
| `orb_count` | `int | None` | `orbCount` |
| `rounds_per_half` | `int | None` | `roundsPerHalf` |
| `economy_type` | `str | None` | `economyType` |
| `list_view_icon_tall` | `str | None` | `listViewIconTall` |

## `Gear`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `description` | `str | None` | - |
| `descriptions` | `list[str] | None` | - |
| `details` | `list[GearDetail] | None` | - |
| `display_icon` | `str | None` | `displayIcon` |
| `asset_path` | `str | None` | `assetPath` |
| `shop_data` | `ShopData | None` | `shopData` |

## `MapInfo`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `narrative_description` | `str | None` | `narrativeDescription` |
| `tactical_description` | `str | None` | `tacticalDescription` |
| `coordinates` | `str | None` | - |
| `display_icon` | `str | None` | `displayIcon` |
| `list_view_icon` | `str | None` | `listViewIcon` |
| `list_view_icon_tall` | `str | None` | `listViewIconTall` |
| `splash` | `str | None` | - |
| `stylized_background_image` | `str | None` | `stylizedBackgroundImage` |
| `premier_background_image` | `str | None` | `premierBackgroundImage` |
| `asset_path` | `str | None` | `assetPath` |
| `map_url` | `str | None` | `mapUrl` |
| `x_multiplier` | `Numeric` | `xMultiplier` |
| `y_multiplier` | `Numeric` | `yMultiplier` |
| `x_scalar_to_add` | `Numeric` | `xScalarToAdd` |
| `y_scalar_to_add` | `Numeric` | `yScalarToAdd` |
| `callouts` | `Lazy[list[Callout] | None] | None` | - |

## `Mission`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str | None` | `displayName` |
| `title` | `str | None` | - |
| `type` | `MissionType | str | None` | - |
| `xp_grant` | `int | None` | `xpGrant` |
| `progress_to_complete` | `int | None` | `progressToComplete` |
| `activation_date` | `datetime | None` | `activationDate` |
| `expiration_date` | `datetime | None` | `expirationDate` |
| `tags` | `list[str] | None` | - |
| `objectives` | `list[MissionObjectiveProgress] | None` | - |
| `asset_path` | `str | None` | `assetPath` |

## `Objective`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `directive` | `str | None` | - |
| `asset_path` | `str | None` | `assetPath` |

## `PlayerCard`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `is_hidden_if_not_owned` | `bool | None` | `isHiddenIfNotOwned` |
| `theme_uuid` | `str | None` | `themeUuid` |
| `display_icon` | `str | None` | `displayIcon` |
| `small_art` | `str | None` | `smallArt` |
| `wide_art` | `str | None` | `wideArt` |
| `large_art` | `str | None` | `largeArt` |
| `asset_path` | `str | None` | `assetPath` |

## `PlayerTitle`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str | None` | `displayName` |
| `title_text` | `str | None` | `titleText` |
| `is_hidden_if_not_owned` | `bool | None` | `isHiddenIfNotOwned` |
| `asset_path` | `str | None` | `assetPath` |

## `LevelBorder`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `starting_level` | `int` | `startingLevel` |
| `level_number` | `int` | `levelNumber` |
| `level_number_appearance` | `str | None` | `levelNumberAppearance` |
| `small_player_card_appearance` | `str | None` | `smallPlayerCardAppearance` |
| `asset_path` | `str | None` | `assetPath` |

## `Season`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `title` | `str | None` | - |
| `type` | `str | None` | - |
| `parent_uuid` | `str | None` | `parentUuid` |
| `start_time` | `datetime | None` | `startTime` |
| `end_time` | `datetime | None` | `endTime` |
| `asset_path` | `str | None` | `assetPath` |

## `Spray`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `category` | `str | None` | - |
| `theme_uuid` | `str | None` | `themeUuid` |
| `display_icon` | `str | None` | `displayIcon` |
| `full_icon` | `str | None` | `fullIcon` |
| `full_transparent_icon` | `str | None` | `fullTransparentIcon` |
| `animation_gif` | `str | None` | `animationGif` |
| `animation_png` | `str | None` | `animationPng` |
| `hide_if_not_owned` | `bool | None` | `hideIfNotOwned` |
| `is_null_spray` | `bool | None` | `isNullSpray` |
| `asset_path` | `str | None` | `assetPath` |
| `levels` | `Lazy[list[SprayLevel]]` | - |

## `Theme`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `display_icon` | `str | None` | `displayIcon` |
| `store_featured_image` | `str | None` | `storeFeaturedImage` |
| `asset_path` | `str | None` | `assetPath` |

## `Weapon`

| Field | Type | API Alias |
| --- | --- | --- |
| `uuid` | `str` | - |
| `display_name` | `str` | `displayName` |
| `category` | `WeaponCategory | str | None` | - |
| `default_skin_uuid` | `str | None` | `defaultSkinUuid` |
| `display_icon` | `str | None` | `displayIcon` |
| `kill_stream_icon` | `str | None` | `killStreamIcon` |
| `asset_path` | `str | None` | `assetPath` |
| `weapon_stats` | `WeaponStats | None` | `weaponStats` |
| `shop_data` | `ShopData | None` | `shopData` |
| `skins` | `Lazy[list[WeaponSkin]]` | - |

## `ValorantVersion`

| Field | Type | API Alias |
| --- | --- | --- |
| `manifest_id` | `str | None` | `manifestId` |
| `branch` | `str | None` | - |
| `version` | `str | None` | - |
| `build_version` | `str | None` | `buildVersion` |
| `engine_version` | `str | None` | `engineVersion` |
| `riot_client_version` | `str | None` | `riotClientVersion` |
| `riot_client_build` | `str | None` | `riotClientBuild` |
| `build_date` | `datetime | None` | `buildDate` |
