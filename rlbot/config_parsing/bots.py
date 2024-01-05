from typing import Any

from flatbuffers import Builder

from rlbot.flat import Color, LoadoutPaint, PlayerLoadout

SETTINGS_HEADER = "settings"
LOOKS_CONFIG = "looks_config"
BOT_STARTER = "bot_starter"
NAME = "name"
MAX_TICK_RATE_PREF = "max_tick_rate_preference"

DETAILS_HEADER = "details"
DESCRIPTION = "description"
FUN_FACT = "fun_fact"
GITHUB = "github"
DEVELOPER = "developer"
LANGUAGE = "language"
TAGS = "tags"

BLUE_TEAM_HEADER = "blue"
ORANGE_TEAM_HEADER = "orange"

PAINT_HEADER = "paint"
CAR_PAINT_ID = "car_paint_id"
DECAL_PAINT_ID = "decal_paint_id"
WHEELS_PAINT_ID = "wheels_paint_id"
BOOST_PAINT_ID = "boost_paint_id"
ANTENNA_PAINT_ID = "antenna_paint_id"
HAT_PAINT_ID = "hat_paint_id"
TRAILS_PAINT_ID = "trails_paint_id"
GOAL_EXPLOSION_PAINT_ID = "goal_explosion_paint_id"

LOADOUT_HEADER = "loadout"
TEAM_COLOR_ID = "team_color_id"
CUSTOM_COLOR_ID = "custom_color_id"
CAR_ID = "car_id"
DECAL_ID = "decal_id"
WHEELS_ID = "wheels_id"
BOOST_ID = "boost_id"
ANTENNA_ID = "antenna_id"
HAT_ID = "hat_id"
PAINT_FINISH_ID = "paint_finish_id"
CUSTOM_FINISH_ID = "custom_finish_id"
ENGINE_AUDIO_ID = "engine_audio_id"
TRAILS_ID = "trails_id"
GOAL_EXPLOSION_ID = "goal_explosion_id"
PRIMARY_COLOR_LOOKUP = "primary_color_lookup"
SECONDARY_COLOR_LOOKUP = "secondary_color_lookup"

DEFAULT_PAINT_CONFIG = {
    CAR_PAINT_ID: 0,
    DECAL_PAINT_ID: 0,
    WHEELS_PAINT_ID: 0,
    BOOST_PAINT_ID: 0,
    ANTENNA_PAINT_ID: 0,
    HAT_PAINT_ID: 0,
    TRAILS_PAINT_ID: 0,
    GOAL_EXPLOSION_PAINT_ID: 0,
}

DEFAULT_LOADOUT_CONFIG = {
    TEAM_COLOR_ID: 0,
    CUSTOM_COLOR_ID: 0,
    CAR_ID: 0,
    DECAL_ID: 0,
    WHEELS_ID: 0,
    BOOST_ID: 0,
    ANTENNA_ID: 0,
    HAT_ID: 0,
    PAINT_FINISH_ID: 0,
    CUSTOM_FINISH_ID: 0,
    ENGINE_AUDIO_ID: 0,
    TRAILS_ID: 0,
    GOAL_EXPLOSION_ID: 0,
    PAINT_HEADER: DEFAULT_PAINT_CONFIG,
    PRIMARY_COLOR_LOOKUP: [0, 0, 0],
    SECONDARY_COLOR_LOOKUP: [0, 0, 0],
}

DEFAULT_LOOKS_CONFIG = {
    LOADOUT_HEADER: {
        BLUE_TEAM_HEADER: DEFAULT_LOADOUT_CONFIG,
        ORANGE_TEAM_HEADER: DEFAULT_LOADOUT_CONFIG,
    },
}


def write_player_loadout(
    looks_config: dict[str, Any], team: int, builder: Builder
) -> int:
    team_name = BLUE_TEAM_HEADER if team == 0 else ORANGE_TEAM_HEADER
    loadout_config = looks_config.get(LOADOUT_HEADER, {}).get(
        team_name, DEFAULT_LOADOUT_CONFIG
    )

    paint_config = loadout_config.get(PAINT_HEADER, DEFAULT_PAINT_CONFIG)
    paint_offset = write_player_paint_loadout(paint_config, builder)

    primary_color_lookup = loadout_config.get(
        PRIMARY_COLOR_LOOKUP, DEFAULT_LOADOUT_CONFIG[PRIMARY_COLOR_LOOKUP]
    )
    primary_color_offset = write_color(primary_color_lookup, builder)

    secondary_color_lookup = loadout_config.get(
        SECONDARY_COLOR_LOOKUP, DEFAULT_LOADOUT_CONFIG[SECONDARY_COLOR_LOOKUP]
    )
    secondary_color_offset = write_color(secondary_color_lookup, builder)

    PlayerLoadout.PlayerLoadoutStart(builder)

    team_color_id = loadout_config.get(
        TEAM_COLOR_ID, DEFAULT_LOADOUT_CONFIG[TEAM_COLOR_ID]
    )
    PlayerLoadout.PlayerLoadoutAddTeamColorId(builder, team_color_id)

    custom_color_id = loadout_config.get(
        CUSTOM_COLOR_ID, DEFAULT_LOADOUT_CONFIG[CUSTOM_COLOR_ID]
    )
    PlayerLoadout.PlayerLoadoutAddCustomColorId(builder, custom_color_id)

    car_id = loadout_config.get(CAR_ID, DEFAULT_LOADOUT_CONFIG[CAR_ID])
    PlayerLoadout.PlayerLoadoutAddCarId(builder, car_id)

    decal_id = loadout_config.get(DECAL_ID, DEFAULT_LOADOUT_CONFIG[DECAL_ID])
    PlayerLoadout.PlayerLoadoutAddDecalId(builder, decal_id)

    wheels_id = loadout_config.get(WHEELS_ID, DEFAULT_LOADOUT_CONFIG[WHEELS_ID])
    PlayerLoadout.PlayerLoadoutAddWheelsId(builder, wheels_id)

    boost_id = loadout_config.get(BOOST_ID, DEFAULT_LOADOUT_CONFIG[BOOST_ID])
    PlayerLoadout.PlayerLoadoutAddBoostId(builder, boost_id)

    antenna_id = loadout_config.get(
        ANTENNA_ID, DEFAULT_LOADOUT_CONFIG[ANTENNA_ID]
    )
    PlayerLoadout.PlayerLoadoutAddAntennaId(builder, antenna_id)

    hat_id = loadout_config.get(HAT_ID, DEFAULT_LOADOUT_CONFIG[HAT_ID])
    PlayerLoadout.PlayerLoadoutAddHatId(builder, hat_id)

    paint_finish_id = loadout_config.get(
        PAINT_FINISH_ID, DEFAULT_LOADOUT_CONFIG[PAINT_FINISH_ID]
    )
    PlayerLoadout.PlayerLoadoutAddPaintFinishId(builder, paint_finish_id)

    custom_finish_id = loadout_config.get(
        CUSTOM_FINISH_ID, DEFAULT_LOADOUT_CONFIG[CUSTOM_FINISH_ID]
    )
    PlayerLoadout.PlayerLoadoutAddCustomFinishId(builder, custom_finish_id)

    engine_audio_id = loadout_config.get(
        ENGINE_AUDIO_ID, DEFAULT_LOADOUT_CONFIG[ENGINE_AUDIO_ID]
    )
    PlayerLoadout.PlayerLoadoutAddEngineAudioId(builder, engine_audio_id)

    trails_id = loadout_config.get(TRAILS_ID, DEFAULT_LOADOUT_CONFIG[TRAILS_ID])
    PlayerLoadout.PlayerLoadoutAddTrailsId(builder, trails_id)

    goal_explosion_id = loadout_config.get(
        GOAL_EXPLOSION_ID, DEFAULT_LOADOUT_CONFIG[GOAL_EXPLOSION_ID]
    )
    PlayerLoadout.PlayerLoadoutAddGoalExplosionId(builder, goal_explosion_id)

    PlayerLoadout.PlayerLoadoutAddLoadoutPaint(builder, paint_offset)
    PlayerLoadout.PlayerLoadoutAddPrimaryColorLookup(builder, primary_color_offset)
    PlayerLoadout.PlayerLoadoutAddSecondaryColorLookup(builder, secondary_color_offset)
    return PlayerLoadout.PlayerLoadoutEnd(builder)


def write_color(color: list[int], builder: Builder) -> int:
    Color.ColorStart(builder)
    Color.ColorAddR(builder, color[0])
    Color.ColorAddG(builder, color[1])
    Color.ColorAddB(builder, color[2])
    Color.ColorAddA(builder, color[3] if len(color) > 3 else 255)
    return Color.ColorEnd(builder)


def write_player_paint_loadout(paint_config: dict[str, Any], builder: Builder) -> int:
    LoadoutPaint.LoadoutPaintStart(builder)

    car_paint_id = paint_config.get(
        CAR_PAINT_ID, DEFAULT_PAINT_CONFIG[CAR_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddCarPaintId(builder, car_paint_id)

    decal_paint_id = paint_config.get(
        DECAL_PAINT_ID, DEFAULT_PAINT_CONFIG[DECAL_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddDecalPaintId(builder, decal_paint_id)

    wheels_paint_id = paint_config.get(
        WHEELS_PAINT_ID, DEFAULT_PAINT_CONFIG[WHEELS_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddWheelsPaintId(builder, wheels_paint_id)

    boost_paint_id = paint_config.get(
        BOOST_PAINT_ID, DEFAULT_PAINT_CONFIG[BOOST_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddBoostPaintId(builder, boost_paint_id)

    antenna_paint_id = paint_config.get(
        ANTENNA_PAINT_ID, DEFAULT_PAINT_CONFIG[ANTENNA_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddAntennaPaintId(builder, antenna_paint_id)

    hat_paint_id = paint_config.get(
        HAT_PAINT_ID, DEFAULT_PAINT_CONFIG[HAT_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddHatPaintId(builder, hat_paint_id)

    trails_paint_id = paint_config.get(
        TRAILS_PAINT_ID, DEFAULT_PAINT_CONFIG[TRAILS_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddTrailsPaintId(builder, trails_paint_id)

    goal_explosion_paint_id = paint_config.get(
        GOAL_EXPLOSION_PAINT_ID, DEFAULT_PAINT_CONFIG[GOAL_EXPLOSION_PAINT_ID]
    )
    LoadoutPaint.LoadoutPaintAddGoalExplosionPaintId(builder, goal_explosion_paint_id)

    return LoadoutPaint.LoadoutPaintEnd(builder)
