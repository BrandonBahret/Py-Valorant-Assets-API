from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any
from typing import TypeAlias

from pypercache.models.apimodel import Alias, Lazy, Shallow, Timestamp, apimodel

from .assets import CachedMediaAsset, get_asset_context
from .enums import AltFireType, MissionType, WallPenetration, WeaponCategory, WeaponStatsFeature



Numeric: TypeAlias = int | float
AssetUrl: TypeAlias = CachedMediaAsset | None


def _coerce_model(value: Any, model_type: type[Any]) -> Any:
    if value is None or isinstance(value, model_type):
        return value
    if isinstance(value, dict):
        return model_type.from_dict(value)
    return value


def _coerce_enum(value: Any, enum_type: type[Enum]) -> Any:
    if value is None or isinstance(value, enum_type):
        return value
    try:
        return enum_type(value)
    except Exception:
        return value


def _coerce_model_list(values: list[Any] | None, model_type: type[Any]) -> list[Any] | None:
    if values is None:
        return None
    return [_coerce_model(value, model_type) for value in values]


def _is_media_url(value: str) -> bool:
    return value.startswith("https://") or value.startswith("http://")


def _sanitize_path_part(value: object) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value)).strip("-._")
    return cleaned or "item"


def _context_path_parts() -> list[str]:
    context = get_asset_context() or {}
    endpoint_path = str(context.get("endpoint_path", "assets"))
    endpoint_slug = endpoint_path.strip("/").split("/", 1)[0] or "assets"
    return [_sanitize_path_part(endpoint_slug)]


def _resource_path_parts(value: Any) -> list[str]:
    for attr in ("uuid", "id"):
        identifier = getattr(value, attr, None)
        if identifier is not None:
            return [_sanitize_path_part(identifier)]
    return []


def _wrap_media_fields(value: Any, *, path_parts: list[str], seen: set[int]) -> None:
    if value is None:
        return
    if isinstance(value, list):
        for item in value:
            _wrap_media_fields(item, path_parts=path_parts, seen=seen)
        return
    if isinstance(value, tuple):
        for item in value:
            _wrap_media_fields(item, path_parts=path_parts, seen=seen)
        return
    if isinstance(value, (str, int, float, bool, datetime)):
        return

    object_id = id(value)
    if object_id in seen or not hasattr(value, "__dict__"):
        return
    seen.add(object_id)

    context = get_asset_context() or {}
    api = context.get("api")
    current_parts = path_parts + _resource_path_parts(value)
    relative_directory = Path(*current_parts)

    for attr, attr_value in vars(value).items():
        if attr.startswith("_") or attr == "asset_path":
            continue
        if isinstance(attr_value, (str, CachedMediaAsset)) and _is_media_url(str(attr_value)):
            wrapped = CachedMediaAsset(
                str(attr_value),
                api=api,
                relative_directory=relative_directory,
                field_name=attr,
            )
            if isinstance(attr_value, CachedMediaAsset) and attr_value.filepath is not None:
                wrapped._filepath = attr_value.filepath
            setattr(value, attr, wrapped)
            continue
        _wrap_media_fields(attr_value, path_parts=current_parts, seen=seen)


def _finalize_media_assets(instance: Any) -> None:
    _wrap_media_fields(instance, path_parts=_context_path_parts(), seen=set())


@apimodel(validate=True)
class Ability:
    slot: str
    display_name: Annotated[str | None, Alias("displayName")]
    description: str | None
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]


@apimodel(validate=True)
class Role:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    description: str | None
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class RecruitmentData:
    counter_id: Annotated[str | None, Alias("counterId")]
    milestone_id: Annotated[str | None, Alias("milestoneId")]
    milestone_threshold: Annotated[int | None, Alias("milestoneThreshold")]
    use_level_vp_cost_override: Annotated[bool | None, Alias("useLevelVpCostOverride")]
    level_vp_cost_override: Annotated[int | None, Alias("levelVpCostOverride")]
    start_date: Annotated[datetime | None, Alias("startDate"), Timestamp()]
    end_date: Annotated[datetime | None, Alias("endDate"), Timestamp()]


@apimodel(validate=True)
class MediaAsset:
    id: int | None
    wwise: AssetUrl
    wave: AssetUrl


@apimodel(validate=True)
class VoiceLine:
    min_duration: Annotated[Numeric, Alias("minDuration")]
    max_duration: Annotated[Numeric, Alias("maxDuration")]
    media_list: Annotated[list[MediaAsset], Alias("mediaList")]

    def __post_init__(self) -> None:
        self.media_list = _coerce_model_list(self.media_list, MediaAsset) or []


@apimodel(validate=True)
class Agent:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    description: str | None
    developer_name: Annotated[str | None, Alias("developerName")]
    release_date: Annotated[datetime | None, Alias("releaseDate"), Timestamp()]
    character_tags: Annotated[list[str] | None, Alias("characterTags")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    display_icon_small: Annotated[AssetUrl, Alias("displayIconSmall")]
    bust_portrait: Annotated[AssetUrl, Alias("bustPortrait")]
    full_portrait: Annotated[AssetUrl, Alias("fullPortrait")]
    full_portrait_v2: Annotated[AssetUrl, Alias("fullPortraitV2")]
    killfeed_portrait: Annotated[AssetUrl, Alias("killfeedPortrait")]
    minimap_portrait: Annotated[AssetUrl, Alias("minimapPortrait")]
    home_screen_promo_tile_image: Annotated[AssetUrl, Alias("homeScreenPromoTileImage")]
    background: AssetUrl
    background_gradient_colors: Annotated[list[str], Alias("backgroundGradientColors")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    is_full_portrait_right_facing: Annotated[bool, Alias("isFullPortraitRightFacing")]
    is_playable_character: Annotated[bool, Alias("isPlayableCharacter")]
    is_available_for_test: Annotated[bool, Alias("isAvailableForTest")]
    is_base_content: Annotated[bool, Alias("isBaseContent")]
    role: Role | None
    recruitment_data: Annotated[RecruitmentData | None, Alias("recruitmentData")]
    abilities: list[Ability]
    voice_line: Annotated[VoiceLine | None, Alias("voiceLine")]

    def __post_init__(self) -> None:
        self.role = _coerce_model(self.role, Role)
        self.recruitment_data = _coerce_model(self.recruitment_data, RecruitmentData)
        self.voice_line = _coerce_model(self.voice_line, VoiceLine)


@apimodel(validate=True)
class BuddyLevel:
    uuid: str
    charm_level: Annotated[int | None, Alias("charmLevel")]
    hide_if_not_owned: Annotated[bool | None, Alias("hideIfNotOwned")]
    display_name: Annotated[str, Alias("displayName")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class Buddy:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    is_hidden_if_not_owned: Annotated[bool | None, Alias("isHiddenIfNotOwned")]
    theme_uuid: Annotated[str | None, Alias("themeUuid")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    levels: Lazy[Annotated[list[BuddyLevel], Shallow()]]


@apimodel(validate=True)
class Bundle:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    display_name_sub_text: Annotated[str | None, Alias("displayNameSubText")]
    description: str | None
    extra_description: Annotated[str | None, Alias("extraDescription")]
    promo_description: Annotated[str | None, Alias("promoDescription")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    display_icon_2: Annotated[AssetUrl, Alias("displayIcon2")]
    display_icon_3: Annotated[AssetUrl, Alias("displayIcon3")]
    vertical_promo_image: Annotated[AssetUrl, Alias("verticalPromoImage")]
    use_additional_context: Annotated[bool | None, Alias("useAdditionalContext")]
    logo_icon: Annotated[AssetUrl, Alias("logoIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class Ceremony:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class CompetitiveTier:
    tier: int
    tier_name: Annotated[str, Alias("tierName")]
    division: str
    division_name: Annotated[str, Alias("divisionName")]
    color: str | None
    background_color: Annotated[str | None, Alias("backgroundColor")]
    small_icon: Annotated[AssetUrl, Alias("smallIcon")]
    large_icon: Annotated[AssetUrl, Alias("largeIcon")]
    rank_triangle_down_icon: Annotated[AssetUrl, Alias("rankTriangleDownIcon")]
    rank_triangle_up_icon: Annotated[AssetUrl, Alias("rankTriangleUpIcon")]


@apimodel(validate=True)
class CompetitiveTierSet:
    uuid: str
    asset_object_name: Annotated[str | None, Alias("assetObjectName")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    tiers: Lazy[Annotated[list[CompetitiveTier], Shallow()]]


@apimodel(validate=True)
class ContentTier:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    dev_name: Annotated[str | None, Alias("devName")]
    rank: int | None
    juice_value: Annotated[int | None, Alias("juiceValue")]
    juice_cost: Annotated[int | None, Alias("juiceCost")]
    highlight_color: Annotated[str | None, Alias("highlightColor")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class Reward:
    type: str
    uuid: str
    amount: int
    is_highlighted: Annotated[bool, Alias("isHighlighted")]


@apimodel(validate=True)
class ContractLevel:
    reward: Reward | None
    xp: int
    vp_cost: Annotated[int | None, Alias("vpCost")]
    is_purchasable_with_vp: Annotated[bool | None, Alias("isPurchasableWithVP")]
    dough_cost: Annotated[int | None, Alias("doughCost")]
    is_purchasable_with_dough: Annotated[bool | None, Alias("isPurchasableWithDough")]

    def __post_init__(self) -> None:
        self.reward = _coerce_model(self.reward, Reward)


@apimodel(validate=True)
class ContractChapter:
    is_epilogue: Annotated[bool, Alias("isEpilogue")]
    levels: list[ContractLevel]
    free_rewards: Annotated[list[Reward] | None, Alias("freeRewards")]


@apimodel(validate=True)
class ContractContent:
    relation_type: Annotated[str | None, Alias("relationType")]
    relation_uuid: Annotated[str | None, Alias("relationUuid")]
    chapters: Lazy[Annotated[list[ContractChapter], Shallow()]]
    premium_reward_schedule_uuid: Annotated[str | None, Alias("premiumRewardScheduleUuid")]
    premium_vp_cost: Annotated[int | None, Alias("premiumVPCost")]


@apimodel(validate=True)
class Contract:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    ship_it: Annotated[bool | None, Alias("shipIt")]
    use_level_vp_cost_override: Annotated[bool | None, Alias("useLevelVPCostOverride")]
    level_vp_cost_override: Annotated[int | None, Alias("levelVPCostOverride")]
    free_reward_schedule_uuid: Annotated[str | None, Alias("freeRewardScheduleUuid")]
    content: Lazy[Annotated[ContractContent, Shallow()]]
    asset_path: Annotated[str | None, Alias("assetPath")]

    def __post_init__(self) -> None:
        self.content = _coerce_model(self.content, ContractContent)


@apimodel(validate=True)
class Currency:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    display_name_singular: Annotated[str | None, Alias("displayNameSingular")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    large_icon: Annotated[AssetUrl, Alias("largeIcon")]
    reward_preview_icon: Annotated[AssetUrl, Alias("rewardPreviewIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class Event:
    uuid: str
    display_name: Annotated[str | None, Alias("displayName")]
    short_display_name: Annotated[str | None, Alias("shortDisplayName")]
    start_time: Annotated[datetime | None, Alias("startTime"), Timestamp()]
    end_time: Annotated[datetime | None, Alias("endTime"), Timestamp()]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class GameFeatureOverride:
    feature_name: Annotated[str, Alias("featureName")]
    state: bool


@apimodel(validate=True)
class GameRuleBoolOverride:
    rule_name: Annotated[str, Alias("ruleName")]
    state: bool


@apimodel(validate=True)
class Gamemode:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    description: str | None
    duration: str | None
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    team_roles: Annotated[list[str] | None, Alias("teamRoles")]
    game_feature_overrides: Annotated[list[GameFeatureOverride] | None, Alias("gameFeatureOverrides")]
    game_rule_bool_overrides: Annotated[list[GameRuleBoolOverride] | None, Alias("gameRuleBoolOverrides")]
    allows_match_timeouts: Annotated[bool | None, Alias("allowsMatchTimeouts")]
    allows_custom_game_replays: Annotated[bool | None, Alias("allowsCustomGameReplays")]
    is_minimap_hidden: Annotated[bool | None, Alias("isMinimapHidden")]
    is_team_voice_allowed: Annotated[bool | None, Alias("isTeamVoiceAllowed")]
    orb_count: Annotated[int | None, Alias("orbCount")]
    rounds_per_half: Annotated[int | None, Alias("roundsPerHalf")]
    economy_type: Annotated[str | None, Alias("economyType")]
    list_view_icon_tall: Annotated[AssetUrl, Alias("listViewIconTall")]

    def __post_init__(self) -> None:
        self.game_feature_overrides = _coerce_model_list(self.game_feature_overrides, GameFeatureOverride)
        self.game_rule_bool_overrides = _coerce_model_list(self.game_rule_bool_overrides, GameRuleBoolOverride)


@apimodel(validate=True)
class ShopGridPosition:
    row: int | None
    column: int | None


@apimodel(validate=True)
class ShopData:
    cost: int | None
    category: str | None
    shop_order_priority: Annotated[int | None, Alias("shopOrderPriority")]
    category_text: Annotated[str | None, Alias("categoryText")]
    grid_position: Annotated[ShopGridPosition | None, Alias("gridPosition")]
    can_be_trashed: Annotated[bool | None, Alias("canBeTrashed")]
    image: AssetUrl
    new_image: Annotated[AssetUrl, Alias("newImage")]
    new_image_2: Annotated[AssetUrl, Alias("newImage2")]
    asset_path: Annotated[str | None, Alias("assetPath")]

    def __post_init__(self) -> None:
        self.grid_position = _coerce_model(self.grid_position, ShopGridPosition)


@apimodel(validate=True)
class GearDetail:
    name: str
    value: str | None


@apimodel(validate=True)
class Gear:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    description: str | None
    descriptions: list[str] | None
    details: list[GearDetail] | None
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    shop_data: Annotated[ShopData | None, Alias("shopData")]

    def __post_init__(self) -> None:
        self.details = _coerce_model_list(self.details, GearDetail)
        self.shop_data = _coerce_model(self.shop_data, ShopData)


@apimodel(validate=True)
class Position3D:
    x: float | int
    y: float | int
    z: float | int


@apimodel(validate=True)
class Rotation3D:
    pitch: float | int
    yaw: float | int
    roll: float | int


@apimodel(validate=True)
class Callout:
    region_name: Annotated[str, Alias("regionName")]
    super_region: Annotated[str | None, Alias("superRegion")]
    super_region_name: Annotated[str | None, Alias("superRegionName")]
    location: Position3D
    scale_3d: Annotated[Position3D | None, Alias("scale3D")]
    rotation: Rotation3D | None

    def __post_init__(self) -> None:
        self.location = _coerce_model(self.location, Position3D)
        self.scale_3d = _coerce_model(self.scale_3d, Position3D)
        self.rotation = _coerce_model(self.rotation, Rotation3D)


@apimodel(validate=True)
class MapInfo:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    narrative_description: Annotated[str | None, Alias("narrativeDescription")]
    tactical_description: Annotated[str | None, Alias("tacticalDescription")]
    coordinates: str | None
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    list_view_icon: Annotated[AssetUrl, Alias("listViewIcon")]
    list_view_icon_tall: Annotated[AssetUrl, Alias("listViewIconTall")]
    splash: AssetUrl
    stylized_background_image: Annotated[AssetUrl, Alias("stylizedBackgroundImage")]
    premier_background_image: Annotated[AssetUrl, Alias("premierBackgroundImage")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    map_url: Annotated[str | None, Alias("mapUrl")]
    x_multiplier: Annotated[Numeric, Alias("xMultiplier")]
    y_multiplier: Annotated[Numeric, Alias("yMultiplier")]
    x_scalar_to_add: Annotated[Numeric, Alias("xScalarToAdd")]
    y_scalar_to_add: Annotated[Numeric, Alias("yScalarToAdd")]
    callouts: Lazy[Annotated[list[Callout] | None, Shallow()]] | None

    def __post_init__(self) -> None:
        self.callouts = _coerce_model_list(self.callouts, Callout)


@apimodel(validate=True)
class MissionObjectiveProgress:
    objective_uuid: Annotated[str, Alias("objectiveUuid")]
    value: int


@apimodel(validate=True)
class Mission:
    uuid: str
    display_name: Annotated[str | None, Alias("displayName")]
    title: str | None
    type: MissionType | str | None
    xp_grant: Annotated[int | None, Alias("xpGrant")]
    progress_to_complete: Annotated[int | None, Alias("progressToComplete")]
    activation_date: Annotated[datetime | None, Alias("activationDate"), Timestamp()]
    expiration_date: Annotated[datetime | None, Alias("expirationDate"), Timestamp()]
    tags: list[str] | None
    objectives: list[MissionObjectiveProgress] | None
    asset_path: Annotated[str | None, Alias("assetPath")]

    def __post_init__(self) -> None:
        self.type = _coerce_enum(self.type, MissionType)
        self.objectives = _coerce_model_list(self.objectives, MissionObjectiveProgress)


@apimodel(validate=True)
class Objective:
    uuid: str
    directive: str | None
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class PlayerCard:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    is_hidden_if_not_owned: Annotated[bool | None, Alias("isHiddenIfNotOwned")]
    theme_uuid: Annotated[str | None, Alias("themeUuid")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    small_art: Annotated[AssetUrl, Alias("smallArt")]
    wide_art: Annotated[AssetUrl, Alias("wideArt")]
    large_art: Annotated[AssetUrl, Alias("largeArt")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class PlayerTitle:
    uuid: str
    display_name: Annotated[str | None, Alias("displayName")]
    title_text: Annotated[str | None, Alias("titleText")]
    is_hidden_if_not_owned: Annotated[bool | None, Alias("isHiddenIfNotOwned")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class LevelBorder:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    starting_level: Annotated[int, Alias("startingLevel")]
    level_number: Annotated[int, Alias("levelNumber")]
    level_number_appearance: Annotated[str | None, Alias("levelNumberAppearance")]
    small_player_card_appearance: Annotated[str | None, Alias("smallPlayerCardAppearance")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class Season:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    title: str | None
    type: str | None
    parent_uuid: Annotated[str | None, Alias("parentUuid")]
    start_time: Annotated[datetime | None, Alias("startTime"), Timestamp()]
    end_time: Annotated[datetime | None, Alias("endTime"), Timestamp()]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class SprayLevel:
    uuid: str
    spray_level: Annotated[int | None, Alias("sprayLevel")]
    display_name: Annotated[str, Alias("displayName")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class Spray:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    category: str | None
    theme_uuid: Annotated[str | None, Alias("themeUuid")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    full_icon: Annotated[AssetUrl, Alias("fullIcon")]
    full_transparent_icon: Annotated[AssetUrl, Alias("fullTransparentIcon")]
    animation_gif: Annotated[AssetUrl, Alias("animationGif")]
    animation_png: Annotated[AssetUrl, Alias("animationPng")]
    hide_if_not_owned: Annotated[bool | None, Alias("hideIfNotOwned")]
    is_null_spray: Annotated[bool | None, Alias("isNullSpray")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    levels: Lazy[Annotated[list[SprayLevel], Shallow()]]


@apimodel(validate=True)
class Theme:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    store_featured_image: Annotated[AssetUrl, Alias("storeFeaturedImage")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class DamageRange:
    range_start_meters: Annotated[float | int, Alias("rangeStartMeters")]
    range_end_meters: Annotated[float | int, Alias("rangeEndMeters")]
    head_damage: Annotated[float | int, Alias("headDamage")]
    body_damage: Annotated[float | int, Alias("bodyDamage")]
    leg_damage: Annotated[float | int, Alias("legDamage")]


@apimodel(validate=True)
class AdsStats:
    zoom_multiplier: Annotated[float | int | None, Alias("zoomMultiplier")]
    fire_rate: Annotated[float | int | None, Alias("fireRate")]
    run_speed_multiplier: Annotated[float | int | None, Alias("runSpeedMultiplier")]
    burst_count: Annotated[int | None, Alias("burstCount")]
    first_bullet_accuracy: Annotated[float | int | None, Alias("firstBulletAccuracy")]


@apimodel(validate=True)
class AirBurstStats:
    shotgun_pellet_count: Annotated[int | None, Alias("shotgunPelletCount")]
    burst_distance: Annotated[float | int | None, Alias("burstDistance")]


@apimodel(validate=True)
class AltShotgunStats:
    shotgun_pellet_count: Annotated[int | None, Alias("shotgunPelletCount")]
    burst_rate: Annotated[float | int | None, Alias("burstRate")]


@apimodel(validate=True)
class WeaponStats:
    fire_rate: Annotated[float | int | None, Alias("fireRate")]
    magazine_size: Annotated[int | None, Alias("magazineSize")]
    run_speed_multiplier: Annotated[float | int | None, Alias("runSpeedMultiplier")]
    equip_time_seconds: Annotated[float | int | None, Alias("equipTimeSeconds")]
    reload_time_seconds: Annotated[float | int | None, Alias("reloadTimeSeconds")]
    first_bullet_accuracy: Annotated[float | int | None, Alias("firstBulletAccuracy")]
    shotgun_pellet_count: Annotated[int | None, Alias("shotgunPelletCount")]
    wall_penetration: Annotated[WallPenetration | str | None, Alias("wallPenetration")]
    feature: WeaponStatsFeature | str | None
    fire_mode: Annotated[str | None, Alias("fireMode")]
    alt_fire_type: Annotated[AltFireType | str | None, Alias("altFireType")]
    ads_stats: Annotated[AdsStats | None, Alias("adsStats")]
    alt_shotgun_stats: Annotated[AltShotgunStats | None, Alias("altShotgunStats")]
    air_burst_stats: Annotated[AirBurstStats | None, Alias("airBurstStats")]
    damage_ranges: Annotated[list[DamageRange] | None, Alias("damageRanges")]

    def __post_init__(self) -> None:
        self.wall_penetration = _coerce_enum(self.wall_penetration, WallPenetration)
        self.feature = _coerce_enum(self.feature, WeaponStatsFeature)
        self.alt_fire_type = _coerce_enum(self.alt_fire_type, AltFireType)
        self.ads_stats = _coerce_model(self.ads_stats, AdsStats)
        self.alt_shotgun_stats = _coerce_model(self.alt_shotgun_stats, AltShotgunStats)
        self.air_burst_stats = _coerce_model(self.air_burst_stats, AirBurstStats)
        self.damage_ranges = _coerce_model_list(self.damage_ranges, DamageRange)


@apimodel(validate=True)
class WeaponChroma:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    full_render: Annotated[AssetUrl, Alias("fullRender")]
    swatch: AssetUrl
    streamed_video: Annotated[AssetUrl, Alias("streamedVideo")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class WeaponSkinLevel:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    level_item: Annotated[str | None, Alias("levelItem")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    streamed_video: Annotated[AssetUrl, Alias("streamedVideo")]
    asset_path: Annotated[str | None, Alias("assetPath")]


@apimodel(validate=True)
class WeaponSkin:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    theme_uuid: Annotated[str | None, Alias("themeUuid")]
    content_tier_uuid: Annotated[str | None, Alias("contentTierUuid")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    wallpaper: AssetUrl
    asset_path: Annotated[str | None, Alias("assetPath")]
    chromas: list[WeaponChroma]
    levels: list[WeaponSkinLevel]

    def __post_init__(self) -> None:
        self.chromas = _coerce_model_list(self.chromas, WeaponChroma) or []
        self.levels = _coerce_model_list(self.levels, WeaponSkinLevel) or []


@apimodel(validate=True)
class Weapon:
    uuid: str
    display_name: Annotated[str, Alias("displayName")]
    category: WeaponCategory | str | None
    default_skin_uuid: Annotated[str | None, Alias("defaultSkinUuid")]
    display_icon: Annotated[AssetUrl, Alias("displayIcon")]
    kill_stream_icon: Annotated[AssetUrl, Alias("killStreamIcon")]
    asset_path: Annotated[str | None, Alias("assetPath")]
    weapon_stats: Annotated[WeaponStats | None, Alias("weaponStats")]
    shop_data: Annotated[ShopData | None, Alias("shopData")]
    skins: Lazy[Annotated[list[WeaponSkin], Shallow()]]

    def __post_init__(self) -> None:
        self.category = _coerce_enum(self.category, WeaponCategory)
        self.weapon_stats = _coerce_model(self.weapon_stats, WeaponStats)
        self.shop_data = _coerce_model(self.shop_data, ShopData)


@apimodel(validate=True)
class ValorantVersion:
    manifest_id: Annotated[str | None, Alias("manifestId")]
    branch: str | None
    version: str | None
    build_version: Annotated[str | None, Alias("buildVersion")]
    engine_version: Annotated[str | None, Alias("engineVersion")]
    riot_client_version: Annotated[str | None, Alias("riotClientVersion")]
    riot_client_build: Annotated[str | None, Alias("riotClientBuild")]
    build_date: Annotated[datetime | None, Alias("buildDate"), Timestamp()]


def _install_asset_post_init(*model_types: type[Any]) -> None:
    for model_type in model_types:
        existing_post_init = getattr(model_type, "__post_init__", None)

        def _post_init(self: Any, _existing=existing_post_init) -> None:
            if _existing is not None:
                _existing(self)
            _finalize_media_assets(self)

        model_type.__post_init__ = _post_init


_install_asset_post_init(
    Ability,
    Role,
    RecruitmentData,
    MediaAsset,
    VoiceLine,
    Agent,
    BuddyLevel,
    Buddy,
    Bundle,
    Ceremony,
    CompetitiveTier,
    CompetitiveTierSet,
    ContentTier,
    Reward,
    ContractLevel,
    ContractChapter,
    ContractContent,
    Contract,
    Currency,
    Event,
    GameFeatureOverride,
    GameRuleBoolOverride,
    Gamemode,
    ShopGridPosition,
    ShopData,
    GearDetail,
    Gear,
    Position3D,
    Rotation3D,
    Callout,
    MapInfo,
    MissionObjectiveProgress,
    Mission,
    Objective,
    PlayerCard,
    PlayerTitle,
    LevelBorder,
    Season,
    SprayLevel,
    Spray,
    Theme,
    DamageRange,
    AdsStats,
    AirBurstStats,
    AltShotgunStats,
    WeaponStats,
    WeaponChroma,
    WeaponSkinLevel,
    WeaponSkin,
    Weapon,
    ValorantVersion,
)