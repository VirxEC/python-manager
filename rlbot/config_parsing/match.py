import os
from pathlib import Path
from typing import Any, Optional

from flatbuffers import Builder

from rlbot.config_parsing.bots import (
    DEFAULT_LOOKS_CONFIG,
    LOOKS_CONFIG,
    NAME,
    SETTINGS_HEADER,
    write_player_loadout,
)
from rlbot.config_parsing.mutators import MUTATORS_HEADER, write_mutator_settings
from rlbot.config_parsing.util import index_or_zero, load_config_file, load_toml_config
from rlbot.flat import (
    HumanPlayer,
    MatchSettings,
    PlayerConfiguration,
    PsyonixBotPlayer,
    RLBotPlayer,
)
from rlbot.flat.PlayerClass import PlayerClass
from rlbot.game_manager.preference import (
    DEFAULT_LAUNCHER_PREFERENCE,
    GameLauncherPreference,
)
from rlbot.utils.logging import get_logger

DEFAULT_CONFIG_LOCATION = Path(os.path.realpath("./rlbot.toml"))

RLBOT_HEADER = "rlbot"
LAUNCHER_PREFERENCE = "launcher_preference"
USE_LOGIN_TRICKS = "use_login_tricks"
EXE_PATH = "rocket_league_exe_path"
MAIN_EXE_PATH = "main_executable_path"

MATCH_HEADER = "match"
NUM_PARTICIPANTS = "num_participants"
GAME_MODE = "game_mode"
GAME_MAP = "game_map"
GAME_MAP_UPK = "game_map_upk"
SKIP_REPLAYS = "skip_replays"
INSTANT_START = "start_without_countdown"
EXISTING_MATCH_BEHAVIOR = "existing_match_behavior"
ENABLE_LOCKSTEP = "enable_lockstep"
ENABLE_RENDERING = "enable_rendering"
ENABLE_STATE_SETTING = "enable_state_setting"
AUTO_SAVE_REPLAY = "auto_save_replay"

BOTS_HEADER = "bots"
CONFIG = "config"
TEAM = "team"
TYPE = "type"
SKILL = "skill"

GAME_MODE_TYPES = [
    "Soccer",
    "Hoops",
    "Dropshot",
    "Hockey",
    "Rumble",
    "Heatseeker",
    "Gridiron",
]

GAME_MAP_DICT = {
    "DFHStadium": "Stadium_P",
    "Mannfield": "EuroStadium_P",
    "ChampionsField": "cs_p",
    "UrbanCentral": "TrainStation_P",
    "BeckwithPark": "Park_P",
    "UtopiaColiseum": "UtopiaStadium_P",
    "Wasteland": "wasteland_s_p",
    "NeoTokyo": "NeoTokyo_Standard_P",
    "AquaDome": "Underwater_P",
    "StarbaseArc": "arc_standard_p",
    "Farmstead": "farm_p",
    "SaltyShores": "beach_P",
    "DFHStadium_Stormy": "Stadium_Foggy_P",
    "DFHStadium_Day": "stadium_day_p",
    "Mannfield_Stormy": "EuroStadium_Rainy_P",
    "Mannfield_Night": "EuroStadium_Night_P",
    "ChampionsField_Day": "cs_day_p",
    "BeckwithPark_Stormy": "Park_Rainy_P",
    "BeckwithPark_Midnight": "Park_Night_P",
    "UrbanCentral_Night": "TrainStation_Night_P",
    "UrbanCentral_Dawn": "TrainStation_Dawn_P",
    "UtopiaColiseum_Dusk": "UtopiaStadium_Dusk_P",
    "DFHStadium_Snowy": "Stadium_Winter_P",
    "Mannfield_Snowy": "eurostadium_snownight_p",
    "UtopiaColiseum_Snowy": "UtopiaStadium_Snow_P",
    "Badlands": "Wasteland_P",
    "Badlands_Night": "Wasteland_Night_P",
    "TokyoUnderpass": "NeoTokyo_P",
    "Arctagon": "ARC_P",
    "Pillars": "Labs_CirclePillars_P",
    "Cosmic": "Labs_Cosmic_V4_P",
    "DoubleGoal": "Labs_DoubleGoal_V2_P",
    "Octagon": "Labs_Octagon_02_P",
    "Underpass": "Labs_Underpass_P",
    "UtopiaRetro": "Labs_Utopia_P",
    "Hoops_DunkHouse": "HoopsStadium_P",
    "DropShot_Core707": "ShatterShot_P",
    "ThrowbackStadium": "ThrowbackStadium_P",
    "ForbiddenTemple": "CHN_Stadium_P",
    "RivalsArena": "cs_hw_p",
    "Farmstead_Night": "Farm_Night_P",
    "SaltyShores_Night": "beach_night_p",
    "NeonFields": "music_p",
    "DFHStadium_Circuit": "Stadium_Race_Day_P",
    "DeadeyeCanyon": "Outlaw_P",
    "StarbaseArc_Aftermath": "ARC_Darc_P",
    "Wasteland_Night": "Wasteland_Night_S_P",
    "BeckwithPark_GothamNight": "Park_Bman_P",
    "ForbiddenTemple_Day": "CHN_Stadium_Day_P",
    "UrbanCentral_Haunted": "Haunted_TrainStation_P",
    "ChampionsField_NFL": "BB_P",
    "ThrowbackStadium_Snowy": "ThrowbackHockey_p",
    "Basin": "Labs_Basin_P",
    "Corridor": "Labs_Corridor_P",
    "Loophole": "Labs_Holyfield_P",
    "Galleon": "Labs_Galleon_P",
    "GalleonRetro": "Labs_Galleon_Mast_P",
    "Hourglass": "Labs_PillarGlass_P",
    "Barricade": "Labs_PillarHeat_P",
    "Colossus": "Labs_PillarWings_P",
    "BeckwithPark_Snowy": "Park_Snowy_P",
    "NeoTokyo_Comic": "NeoTokyo_Toon_P",
    "UtopiaColiseum_Gilded": "UtopiaStadium_Lux_P",
    "SovereignHeights": "Street_P",
    "Hoops_TheBlock": "HoopsStreet_P",
    "Farmstead_Spooky": "Farm_HW_P",
    "ChampionsField_NikeFC": "swoosh_p",
    "ForbiddenTemple_FireAndIce": "fni_stadium_p",
    "DeadeyeCanyon_Oasis": "outlaw_oasis_p",
    "EstadioVida_Dusk": "ff_dusk_p",
}

EXISTING_MATCH_BEHAVIOR_TYPES = [
    "Restart If Different",
    "Restart",
    "Continue And Spawn",
]

MAP_TYPES = list(GAME_MAP_DICT.keys())


def get_launcher_preference(config: dict[str, Any]) -> GameLauncherPreference:
    launcher_preference = DEFAULT_LAUNCHER_PREFERENCE

    rlbot_config = config.get(RLBOT_HEADER, {})
    raw_launcher_string = rlbot_config.get(LAUNCHER_PREFERENCE, "")

    if raw_launcher_string == GameLauncherPreference.STEAM:
        launcher_preference = GameLauncherPreference(
            GameLauncherPreference.STEAM, False
        )
    else:
        if raw_launcher_string == GameLauncherPreference.EPIC_ONLY:
            launcher_preference.preferred_launcher = GameLauncherPreference.EPIC_ONLY
        else:
            launcher_preference.preferred_launcher = GameLauncherPreference.EPIC

        launcher_preference.use_login_tricks = rlbot_config.get(USE_LOGIN_TRICKS, True)

        launcher_preference.game_exe_path = rlbot_config.get(EXE_PATH)

    return launcher_preference


def get_main_executable_path(config: dict[str, Any]) -> Optional[Path]:
    rlbot_config = config.get(RLBOT_HEADER, {})
    path = rlbot_config.get(MAIN_EXE_PATH)
    if path is not None:
        return Path(path)


def get_match_settings(config: dict[str, Any]) -> MatchSettings.MatchSettingsT:
    builder = Builder(1000)
    match_settings_offset = write_match_settings(builder, config)
    builder.Finish(match_settings_offset)
    raw_bytes = builder.Output()
    match_settings = MatchSettings.MatchSettings.GetRootAsMatchSettings(raw_bytes, 0)
    return MatchSettings.MatchSettingsT.InitFromObj(match_settings)


def write_match_settings(builder: Builder, config: dict[str, Any]) -> int:
    match_config = config.get(MATCH_HEADER, {})

    num_participants = match_config.get(NUM_PARTICIPANTS, 0)
    bot_configs = config.get(BOTS_HEADER, [])
    num_participants = min(num_participants, len(bot_configs))

    name_dict = {}
    player_config_offsets = [
        write_player_configutation(pc, builder, name_dict)
        for pc in bot_configs[:num_participants]
    ]

    MatchSettings.MatchSettingsStartPlayerConfigurationsVector(
        builder, len(player_config_offsets)
    )
    for i in reversed(range(0, len(player_config_offsets))):
        builder.PrependUOffsetTRelative(player_config_offsets[i])
    player_list_offset = builder.EndVector(len(player_config_offsets))

    mutators = config.get(MUTATORS_HEADER, {})
    mutator_settings_offset = write_mutator_settings(mutators, builder)

    game_map_upk = match_config.get(GAME_MAP_UPK, "DFHStadium")
    if game_map_upk in GAME_MAP_DICT:
        upk = GAME_MAP_DICT[game_map_upk]
    else:
        upk = game_map_upk
    upk_offset = builder.CreateString(upk)

    MatchSettings.MatchSettingsStart(builder)
    MatchSettings.MatchSettingsAddPlayerConfigurations(builder, player_list_offset)
    MatchSettings.MatchSettingsAddGameMode(
        builder, index_or_zero(GAME_MODE_TYPES, match_config.get(GAME_MODE))
    )
    MatchSettings.MatchSettingsAddGameMapUpk(builder, upk_offset)
    MatchSettings.MatchSettingsAddSkipReplays(builder, match_config.get(SKIP_REPLAYS))
    MatchSettings.MatchSettingsAddInstantStart(builder, match_config.get(INSTANT_START))
    MatchSettings.MatchSettingsAddMutatorSettings(builder, mutator_settings_offset)
    MatchSettings.MatchSettingsAddExistingMatchBehavior(
        builder,
        index_or_zero(
            EXISTING_MATCH_BEHAVIOR_TYPES, match_config.get(EXISTING_MATCH_BEHAVIOR)
        ),
    )
    MatchSettings.MatchSettingsAddEnableLockstep(
        builder, match_config.get(ENABLE_LOCKSTEP)
    )
    MatchSettings.MatchSettingsAddEnableRendering(
        builder, match_config.get(ENABLE_RENDERING)
    )
    MatchSettings.MatchSettingsAddEnableStateSetting(
        builder, match_config.get(ENABLE_STATE_SETTING)
    )
    MatchSettings.MatchSettingsAddAutoSaveReplay(
        builder, match_config.get(AUTO_SAVE_REPLAY)
    )
    return MatchSettings.MatchSettingsEnd(builder)


def get_sanitized_bot_name(dict: dict[str, int], name: str) -> str:
    """
    Cut off at 31 characters and handle duplicates.
    :param dict: Holds the list of names for duplicates
    :param name: The name that is being sanitized
    :return: A sanitized version of the name
    """

    # This doesn't work someimtes in continue_and_spawn because it doesn't understand the names already in the match
    # which may be kept if the spawn IDs match. In that case it's the caller's responsibility to figure it out upstream.

    name = name[:31]
    base_name = name
    count = 2
    while name in dict:
        name = f"{base_name[:27]} ({count})"  # Truncate at 27 because we can have up to '(10)' appended
        count += 1
    dict[name] = 1
    return name


FLATBUFFER_MAX_INT = 2**31 - 1


def write_player_configutation(
    player_config: dict, builder: Builder, name_dict: dict
) -> int:
    bot_config_path = player_config.get(CONFIG)
    if bot_config_path is None:
        raise Exception("Player config missing 'config' key!")
    bot_config_path = Path(bot_config_path)
    bot_config = load_config_file(bot_config_path)
    settings = bot_config.get(SETTINGS_HEADER, {})

    deduped_name = get_sanitized_bot_name(name_dict, settings.get(NAME, ""))
    name = builder.CreateString(deduped_name)
    team = player_config.get(TEAM, 0)

    looks_path = settings.get(LOOKS_CONFIG)
    if looks_path is None:
        loadout_config = DEFAULT_LOOKS_CONFIG
    else:
        loadout_config = load_config_file(bot_config_path.parent / looks_path)

    loadout = write_player_loadout(loadout_config, team, builder)

    bot_type = player_config.get(TYPE, "rlbot")

    if bot_type == "rlbot":
        variety = PlayerClass.RLBotPlayer
        RLBotPlayer.RLBotPlayerStart(builder)
        player = RLBotPlayer.RLBotPlayerEnd(builder)
    elif bot_type == "psyonix":
        variety = PlayerClass.PsyonixBotPlayer
        PsyonixBotPlayer.PsyonixBotPlayerStart(builder)
        bot_skill = player_config.get(SKILL, 1.0)
        PsyonixBotPlayer.PsyonixBotPlayerAddBotSkill(builder, bot_skill)
        player = PsyonixBotPlayer.PsyonixBotPlayerEnd(builder)
    elif bot_type == "human":
        variety = PlayerClass.HumanPlayer
        HumanPlayer.HumanPlayerStart(builder)
        player = HumanPlayer.HumanPlayerEnd(builder)
    else:
        raise Exception(f"Unknown bot type: {bot_type}")

    PlayerConfiguration.PlayerConfigurationStart(builder)
    PlayerConfiguration.PlayerConfigurationAddName(builder, name)
    PlayerConfiguration.PlayerConfigurationAddLoadout(builder, loadout)
    PlayerConfiguration.PlayerConfigurationAddTeam(builder, team)
    PlayerConfiguration.PlayerConfigurationAddVariety(builder, player)
    PlayerConfiguration.PlayerConfigurationAddVarietyType(builder, variety)

    # make the spawn id a function of the deduped name
    # this allows restart_if_different to work properly
    spawn_id = hash(deduped_name) % FLATBUFFER_MAX_INT
    PlayerConfiguration.PlayerConfigurationAddSpawnId(builder, spawn_id)

    return PlayerConfiguration.PlayerConfigurationEnd(builder)
