from __future__ import annotations

from valorant_assets_api.models import (
    Callout,
    ContractLevel,
    DamageRange,
    GameFeatureOverride,
    GameRuleBoolOverride,
    Gamemode,
    Gear,
    GearDetail,
    MapInfo,
    Mission,
    MissionObjectiveProgress,
    PlayerTitle,
    Reward,
    ShopData,
    ShopGridPosition,
)


def test_gamemode_override_lists_hydrate_to_models() -> None:
    gamemode = Gamemode.from_dict(
        {
            "uuid": "1cd8901f-47af-49cb-d758-e2afd0eb2a39",
            "displayName": "All Random One Site",
            "description": "LIMITED TIME mode.",
            "duration": "10-15 MINS",
            "displayIcon": "https://media.valorant-api.com/gamemodes/test/displayicon.png",
            "assetPath": "ShooterGame/Content/GameModes/AROS/AROS_GameMode_PrimaryAsset",
            "teamRoles": None,
            "gameFeatureOverrides": [
                {
                    "featureName": "EGameFeatureToggleName::EquippableCacheRecycling",
                    "state": True,
                }
            ],
            "gameRuleBoolOverrides": [
                {
                    "ruleName": "EGameRuleBoolName::AssignRandomAgents",
                    "state": True,
                }
            ],
            "allowsMatchTimeouts": False,
            "allowsCustomGameReplays": False,
            "isMinimapHidden": False,
            "isTeamVoiceAllowed": True,
            "orbCount": 1,
            "roundsPerHalf": -1,
            "economyType": None,
            "listViewIconTall": "https://media.valorant-api.com/gamemodes/test/listviewicontall.png",
        }
    )

    assert gamemode.game_feature_overrides is not None
    assert gamemode.game_rule_bool_overrides is not None
    assert isinstance(gamemode.game_feature_overrides[0], GameFeatureOverride)
    assert isinstance(gamemode.game_rule_bool_overrides[0], GameRuleBoolOverride)
    assert gamemode.game_feature_overrides[0].feature_name == "EGameFeatureToggleName::EquippableCacheRecycling"
    assert gamemode.game_rule_bool_overrides[0].rule_name == "EGameRuleBoolName::AssignRandomAgents"


def test_player_title_display_name_allows_null() -> None:
    title = PlayerTitle.from_dict(
        {
            "uuid": "d13e579c-435e-44d4-cec2-6eae5a3c5ed4",
            "displayName": None,
            "titleText": None,
            "isHiddenIfNotOwned": False,
            "assetPath": "ShooterGame/Content/Personalization/Titles/PlayerTitle_Default_PrimaryAsset",
        }
    )

    assert title.display_name is None


def test_map_callouts_allow_null_and_hydrate_nested_models() -> None:
    no_callouts = MapInfo.from_dict(
        {
            "uuid": "map-null",
            "displayName": "Test Map",
            "narrativeDescription": None,
            "tacticalDescription": None,
            "coordinates": None,
            "displayIcon": None,
            "listViewIcon": None,
            "listViewIconTall": None,
            "splash": None,
            "stylizedBackgroundImage": None,
            "premierBackgroundImage": None,
            "assetPath": None,
            "mapUrl": None,
            "xMultiplier": 1.0,
            "yMultiplier": 1.0,
            "xScalarToAdd": 0.0,
            "yScalarToAdd": 0.0,
            "callouts": None,
        }
    )
    with_callouts = MapInfo.from_dict(
        {
            "uuid": "map-callouts",
            "displayName": "Test Map",
            "narrativeDescription": None,
            "tacticalDescription": None,
            "coordinates": None,
            "displayIcon": None,
            "listViewIcon": None,
            "listViewIconTall": None,
            "splash": None,
            "stylizedBackgroundImage": None,
            "premierBackgroundImage": None,
            "assetPath": None,
            "mapUrl": None,
            "xMultiplier": 1.0,
            "yMultiplier": 1.0,
            "xScalarToAdd": 0.0,
            "yScalarToAdd": 0.0,
            "callouts": [
                {
                    "regionName": "Tree",
                    "superRegion": "ECalloutSuperRegion::A",
                    "superRegionName": "A",
                    "location": {"x": 1, "y": 2, "z": 3},
                    "scale3D": {"x": 4, "y": 5, "z": 6},
                    "rotation": {"pitch": 7, "yaw": 8, "roll": 9},
                }
            ],
        }
    )

    assert no_callouts.callouts is None
    assert with_callouts.callouts is not None
    assert isinstance(with_callouts.callouts[0], Callout)
    assert with_callouts.callouts[0].location.x == 1


def test_nested_helper_payloads_hydrate_to_models() -> None:
    contract_level = ContractLevel.from_dict(
        {
            "reward": {
                "type": "Spray",
                "uuid": "reward-uuid",
                "amount": 1,
                "isHighlighted": False,
            },
            "xp": 1000,
            "vpCost": 200,
            "isPurchasableWithVP": False,
            "doughCost": 100,
            "isPurchasableWithDough": True,
        }
    )
    gear = Gear.from_dict(
        {
            "uuid": "gear-uuid",
            "displayName": "Armor",
            "description": None,
            "descriptions": None,
            "details": [{"name": "DAMAGE REDUCTION", "value": "Partial"}],
            "displayIcon": None,
            "assetPath": None,
            "shopData": {
                "cost": 1000,
                "category": "armor",
                "shopOrderPriority": 1,
                "categoryText": "Armor",
                "gridPosition": {"row": 2, "column": 2},
                "canBeTrashed": False,
                "image": None,
                "newImage": None,
                "newImage2": None,
                "assetPath": None,
            },
        }
    )
    mission = Mission.from_dict(
        {
            "uuid": "mission-uuid",
            "displayName": "Mission",
            "title": None,
            "type": None,
            "xpGrant": 1000,
            "progressToComplete": 10,
            "activationDate": None,
            "expirationDate": None,
            "tags": None,
            "objectives": [{"objectiveUuid": "objective-uuid", "value": 1}],
            "assetPath": None,
        }
    )
    shop_data = ShopData.from_dict(
        {
            "cost": 1000,
            "category": "rifle",
            "shopOrderPriority": 1,
            "categoryText": "Rifle",
            "gridPosition": {"row": 1, "column": 1},
            "canBeTrashed": False,
            "image": None,
            "newImage": None,
            "newImage2": None,
            "assetPath": None,
        }
    )
    weapon_stats_payload = {
        "fireRate": 1.0,
        "magazineSize": 25,
        "runSpeedMultiplier": 1.0,
        "equipTimeSeconds": 1.0,
        "reloadTimeSeconds": 2.0,
        "firstBulletAccuracy": 0.5,
        "shotgunPelletCount": 0,
        "wallPenetration": None,
        "feature": None,
        "fireMode": None,
        "altFireType": None,
        "adsStats": None,
        "altShotgunStats": None,
        "airBurstStats": None,
        "damageRanges": [
            {
                "rangeStartMeters": 0,
                "rangeEndMeters": 50,
                "headDamage": 160,
                "bodyDamage": 40,
                "legDamage": 34,
            }
        ],
    }

    from valorant_assets_api.models import WeaponStats

    weapon_stats = WeaponStats.from_dict(weapon_stats_payload)

    assert isinstance(contract_level.reward, Reward)
    assert isinstance(gear.details[0], GearDetail)
    assert isinstance(gear.shop_data, ShopData)
    assert isinstance(gear.shop_data.grid_position, ShopGridPosition)
    assert isinstance(mission.objectives[0], MissionObjectiveProgress)
    assert isinstance(shop_data.grid_position, ShopGridPosition)
    assert isinstance(weapon_stats.damage_ranges[0], DamageRange)
