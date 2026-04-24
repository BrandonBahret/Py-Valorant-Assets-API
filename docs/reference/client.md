# Client Reference

> Generated file. Do not edit by hand. Run `python scripts/generate_reference_docs.py`.

Use this page for quick API lookup. Start with the narrative guides if you are new to the wrapper.

## `get_session`

**Signature:** `get_session(self)`

**Returns:** `requests.Session`

Create a configured HTTP session with default wrapper headers.

## `list_agents`

**Signature:** `list_agents(self, *, language: LanguageLike = None, playable_only: bool = False)`

**Returns:** `list[Agent]`

List agents.

## `get_agent`

**Signature:** `get_agent(self, agent_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Agent`

Fetch an agent by UUID.

## `find_agent`

**Signature:** `find_agent(self, name: str, *, language: LanguageLike = None, playable_only: bool = False)`

**Returns:** `Agent | None`

Find an agent by display name.

## `list_buddies`

**Signature:** `list_buddies(self, *, language: LanguageLike = None)`

**Returns:** `list[Buddy]`

List buddies.

## `get_buddy`

**Signature:** `get_buddy(self, buddy_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Buddy`

Fetch a buddy by UUID.

## `list_bundles`

**Signature:** `list_bundles(self, *, language: LanguageLike = None)`

**Returns:** `list[Bundle]`

List bundles.

## `get_bundle`

**Signature:** `get_bundle(self, bundle_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Bundle`

Fetch a bundle by UUID.

## `list_ceremonies`

**Signature:** `list_ceremonies(self)`

**Returns:** `list[Ceremony]`

List ceremonies.

## `get_ceremony`

**Signature:** `get_ceremony(self, ceremony_uuid: str)`

**Returns:** `Ceremony`

Fetch a ceremony by UUID.

## `list_competitive_tiers`

**Signature:** `list_competitive_tiers(self)`

**Returns:** `list[CompetitiveTierSet]`

List competitive tiers.

## `get_competitive_tier_set`

**Signature:** `get_competitive_tier_set(self, tier_set_uuid: str)`

**Returns:** `CompetitiveTierSet`

Fetch a competitive tier set by UUID.

## `list_content_tiers`

**Signature:** `list_content_tiers(self, *, language: LanguageLike = None)`

**Returns:** `list[ContentTier]`

List content tiers.

## `get_content_tier`

**Signature:** `get_content_tier(self, content_tier_uuid: str, *, language: LanguageLike = None)`

**Returns:** `ContentTier`

Fetch a content tier by UUID.

## `list_contracts`

**Signature:** `list_contracts(self, *, language: LanguageLike = None)`

**Returns:** `list[Contract]`

List contracts.

## `get_contract`

**Signature:** `get_contract(self, contract_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Contract`

Fetch a contract by UUID.

## `list_contract_rewards`

**Signature:** `list_contract_rewards(self, contract_uuid: str, *, language: LanguageLike = None)`

**Returns:** `list[ContractLevel]`

Flatten and return the rewards across all chapters in a contract.

## `list_currencies`

**Signature:** `list_currencies(self, *, language: LanguageLike = None)`

**Returns:** `list[Currency]`

List currencies.

## `get_currency`

**Signature:** `get_currency(self, currency_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Currency`

Fetch a currency by UUID.

## `list_events`

**Signature:** `list_events(self, *, language: LanguageLike = None)`

**Returns:** `list[Event]`

List events.

## `get_event`

**Signature:** `get_event(self, event_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Event`

Fetch an event by UUID.

## `get_active_events`

**Signature:** `get_active_events(self, *, language: LanguageLike = None, now: datetime | None = None)`

**Returns:** `list[Event]`

Return the events active at the provided time.

## `list_gamemodes`

**Signature:** `list_gamemodes(self, *, language: LanguageLike = None)`

**Returns:** `list[Gamemode]`

List gamemodes.

## `get_gamemode`

**Signature:** `get_gamemode(self, gamemode_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Gamemode`

Fetch a gamemode by UUID.

## `list_gear`

**Signature:** `list_gear(self, *, language: LanguageLike = None)`

**Returns:** `list[Gear]`

List gear.

## `get_gear`

**Signature:** `get_gear(self, gear_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Gear`

Fetch a gear by UUID.

## `list_level_borders`

**Signature:** `list_level_borders(self, *, language: LanguageLike = None)`

**Returns:** `list[LevelBorder]`

List level borders.

## `get_level_border`

**Signature:** `get_level_border(self, level_border_uuid: str, *, language: LanguageLike = None)`

**Returns:** `LevelBorder`

Fetch a level border by UUID.

## `list_maps`

**Signature:** `list_maps(self, *, language: LanguageLike = None)`

**Returns:** `list[MapInfo]`

List maps.

## `get_map`

**Signature:** `get_map(self, map_uuid: str, *, language: LanguageLike = None)`

**Returns:** `MapInfo`

Fetch a map by UUID.

## `find_map`

**Signature:** `find_map(self, name: str, *, language: LanguageLike = None)`

**Returns:** `MapInfo | None`

Find a map by display name.

## `list_missions`

**Signature:** `list_missions(self)`

**Returns:** `list[Mission]`

List missions.

## `get_mission`

**Signature:** `get_mission(self, mission_uuid: str)`

**Returns:** `Mission`

Fetch a mission by UUID.

## `list_objectives`

**Signature:** `list_objectives(self)`

**Returns:** `list[Objective]`

List objectives.

## `get_objective`

**Signature:** `get_objective(self, objective_uuid: str)`

**Returns:** `Objective`

Fetch an objective by UUID.

## `list_player_cards`

**Signature:** `list_player_cards(self, *, language: LanguageLike = None)`

**Returns:** `list[PlayerCard]`

List player cards.

## `get_player_card`

**Signature:** `get_player_card(self, card_uuid: str, *, language: LanguageLike = None)`

**Returns:** `PlayerCard`

Fetch a player card by UUID.

## `list_player_titles`

**Signature:** `list_player_titles(self, *, language: LanguageLike = None)`

**Returns:** `list[PlayerTitle]`

List player titles.

## `get_player_title`

**Signature:** `get_player_title(self, title_uuid: str, *, language: LanguageLike = None)`

**Returns:** `PlayerTitle`

Fetch a player title by UUID.

## `list_seasons`

**Signature:** `list_seasons(self, *, language: LanguageLike = None)`

**Returns:** `list[Season]`

List seasons.

## `get_season`

**Signature:** `get_season(self, season_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Season`

Fetch a season by UUID.

## `get_current_season`

**Signature:** `get_current_season(self, *, language: LanguageLike = None, now: datetime | None = None)`

**Returns:** `Season | None`

Return the season active at the provided time.

## `list_sprays`

**Signature:** `list_sprays(self, *, language: LanguageLike = None)`

**Returns:** `list[Spray]`

List sprays.

## `get_spray`

**Signature:** `get_spray(self, spray_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Spray`

Fetch a spray by UUID.

## `list_themes`

**Signature:** `list_themes(self, *, language: LanguageLike = None)`

**Returns:** `list[Theme]`

List themes.

## `get_theme`

**Signature:** `get_theme(self, theme_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Theme`

Fetch a theme by UUID.

## `list_weapons`

**Signature:** `list_weapons(self, *, language: LanguageLike = None)`

**Returns:** `list[Weapon]`

List weapons.

## `get_weapon`

**Signature:** `get_weapon(self, weapon_uuid: str, *, language: LanguageLike = None)`

**Returns:** `Weapon`

Fetch a weapon by UUID.

## `find_weapon`

**Signature:** `find_weapon(self, name: str, *, language: LanguageLike = None)`

**Returns:** `Weapon | None`

Find a weapon by display name.

## `get_version`

**Signature:** `get_version(self)`

**Returns:** `ValorantVersion`

Fetch the current Valorant version metadata.
