from __future__ import annotations

from enum import StrEnum


class Language(StrEnum):
    EN_US = "en-US"
    ES_ES = "es-ES"
    FR_FR = "fr-FR"
    DE_DE = "de-DE"
    IT_IT = "it-IT"
    JA_JP = "ja-JP"
    KO_KR = "ko-KR"
    PL_PL = "pl-PL"
    PT_BR = "pt-BR"
    RU_RU = "ru-RU"
    TH_TH = "th-TH"
    TR_TR = "tr-TR"
    VI_VN = "vi-VN"
    ZH_CN = "zh-CN"
    ZH_TW = "zh-TW"
    ID_ID = "id-ID"
    AR_AE = "ar-AE"


class WeaponCategory(StrEnum):
    SIDEARM = "EEquippableCategory::Sidearm"
    SMG = "EEquippableCategory::SMG"
    RIFLE = "EEquippableCategory::Rifle"
    SNIPER = "EEquippableCategory::Sniper"
    SHOTGUN = "EEquippableCategory::Shotgun"
    HEAVY = "EEquippableCategory::Heavy"
    MELEE = "EEquippableCategory::Melee"


class WallPenetration(StrEnum):
    LOW = "EWallPenetrationDisplayType::Low"
    MEDIUM = "EWallPenetrationDisplayType::Medium"
    HIGH = "EWallPenetrationDisplayType::High"


class AltFireType(StrEnum):
    ADS = "EWeaponAltFireDisplayType::ADS"
    AIR_BURST = "EWeaponAltFireDisplayType::AirBurst"
    SHOTGUN = "EWeaponAltFireDisplayType::Shotgun"


class WeaponStatsFeature(StrEnum):
    ROF_INCREASE = "EWeaponStatsFeature::ROFIncrease"
    DOUBLE_ZOOM = "EWeaponStatsFeature::DoubleZoom"
    SILENCED = "EWeaponStatsFeature::Silenced"


class MissionType(StrEnum):
    BTE = "EAresMissionType::BTE"
    DAILY = "EAresMissionType::Daily"
    WEEKLY = "EAresMissionType::Weekly"
    NPE = "EAresMissionType::NPE"
