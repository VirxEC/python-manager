from typing import Any

from flatbuffers import Builder

from rlbot.config_parsing.util import index_or_zero
from rlbot.flat import MutatorSettings

MUTATORS_HEADER = "mutators"
MATCH_LENGTH = "match_length"
MAX_SCORE = "max_score"
OVERTIME = "overtime"
SERIES_LENGTH = "series_length"
GAME_SPEED = "game_speed"
BALL_MAX_SPEED = "ball_max_speed"
BALL_TYPE = "ball_type"
BALL_WEIGHT = "ball_weight"
BALL_SIZE = "ball_size"
BALL_BOUNCINESS = "ball_bounciness"
BOOST_AMOUNT = "boost_amount"
RUMBLE = "rumble"
BOOST_STRENGTH = "boost_strength"
GRAVITY = "gravity"
DEMOLISH = "demolish"
RESPAWN_TIME = "respawn_time"

MATCH_LENGTH_TYPES = ["5 Minutes", "10 Minutes", "20 Minutes", "Unlimited"]

MAX_SCORE_TYPES = [
    "Unlimited",
    "1 Goal",
    "3 Goals",
    "5 Goals",
]

OVERTIME_MUTATOR_TYPES = ["Unlimited", "+5 Max, First Score", "+5 Max, Random Team"]

SERIES_LENGTH_MUTATOR_TYPES = [
    "Unlimited",
    "3 Games",
    "5 Games",
    "7 Games",
]

GAME_SPEED_MUTATOR_TYPES = ["Default", "Slo-Mo", "Time Warp"]

BALL_MAX_SPEED_MUTATOR_TYPES = ["Default", "Slow", "Fast", "Super Fast"]

BALL_TYPE_MUTATOR_TYPES = ["Default", "Cube", "Puck", "Basketball"]

BALL_WEIGHT_MUTATOR_TYPES = ["Default", "Light", "Heavy", "Super Light"]

BALL_SIZE_MUTATOR_TYPES = ["Default", "Small", "Large", "Gigantic"]

BALL_BOUNCINESS_MUTATOR_TYPES = ["Default", "Low", "High", "Super High"]

BOOST_AMOUNT_MUTATOR_TYPES = [
    "Default",
    "Unlimited",
    "Recharge (Slow)",
    "Recharge (Fast)",
    "No Boost",
]

RUMBLE_MUTATOR_TYPES = [
    "None",
    "Default",
    "Slow",
    "Civilized",
    "Destruction Derby",
    "Spring Loaded",
    "Spikes Only",
    "Spike Rush",
]

BOOST_STRENGTH_MUTATOR_TYPES = ["1x", "1.5x", "2x", "10x"]

GRAVITY_MUTATOR_TYPES = ["Default", "Low", "High", "Super High"]

DEMOLISH_MUTATOR_TYPES = [
    "Default",
    "Disabled",
    "Friendly Fire",
    "On Contact",
    "On Contact (FF)",
]

RESPAWN_TIME_MUTATOR_TYPES = [
    "3 Seconds",
    "2 Seconds",
    "1 Second",
    "Disable Goal Reset",
]


def write_mutator_settings(mutators: dict[str, Any], builder: Builder) -> int:
    MutatorSettings.MutatorSettingsStart(builder)
    MutatorSettings.MutatorSettingsAddMatchLength(
        builder, index_or_zero(MATCH_LENGTH_TYPES, mutators.get(MATCH_LENGTH))
    )
    MutatorSettings.MutatorSettingsAddMaxScore(
        builder, index_or_zero(MAX_SCORE_TYPES, mutators.get(MAX_SCORE))
    )
    MutatorSettings.MutatorSettingsAddOvertimeOption(
        builder, index_or_zero(OVERTIME_MUTATOR_TYPES, mutators.get(OVERTIME))
    )
    MutatorSettings.MutatorSettingsAddSeriesLengthOption(
        builder, index_or_zero(SERIES_LENGTH_MUTATOR_TYPES, mutators.get(SERIES_LENGTH))
    )
    MutatorSettings.MutatorSettingsAddGameSpeedOption(
        builder, index_or_zero(GAME_SPEED_MUTATOR_TYPES, mutators.get(GAME_SPEED))
    )
    MutatorSettings.MutatorSettingsAddBallMaxSpeedOption(
        builder,
        index_or_zero(BALL_MAX_SPEED_MUTATOR_TYPES, mutators.get(BALL_MAX_SPEED)),
    )
    MutatorSettings.MutatorSettingsAddBallTypeOption(
        builder, index_or_zero(BALL_TYPE_MUTATOR_TYPES, mutators.get(BALL_TYPE))
    )
    MutatorSettings.MutatorSettingsAddBallWeightOption(
        builder, index_or_zero(BALL_WEIGHT_MUTATOR_TYPES, mutators.get(BALL_WEIGHT))
    )
    MutatorSettings.MutatorSettingsAddBallSizeOption(
        builder, index_or_zero(BALL_SIZE_MUTATOR_TYPES, mutators.get(BALL_SIZE))
    )
    MutatorSettings.MutatorSettingsAddBallBouncinessOption(
        builder,
        index_or_zero(BALL_BOUNCINESS_MUTATOR_TYPES, mutators.get(BALL_BOUNCINESS)),
    )
    MutatorSettings.MutatorSettingsAddBoostOption(
        builder, index_or_zero(BOOST_AMOUNT_MUTATOR_TYPES, mutators.get(BOOST_AMOUNT))
    )
    MutatorSettings.MutatorSettingsAddRumbleOption(
        builder, index_or_zero(RUMBLE_MUTATOR_TYPES, mutators.get(RUMBLE))
    )
    MutatorSettings.MutatorSettingsAddBoostStrengthOption(
        builder,
        index_or_zero(BOOST_STRENGTH_MUTATOR_TYPES, mutators.get(BOOST_STRENGTH)),
    )
    MutatorSettings.MutatorSettingsAddGravityOption(
        builder, index_or_zero(GRAVITY_MUTATOR_TYPES, mutators.get(GRAVITY))
    )
    MutatorSettings.MutatorSettingsAddDemolishOption(
        builder, index_or_zero(DEMOLISH_MUTATOR_TYPES, mutators.get(DEMOLISH))
    )
    MutatorSettings.MutatorSettingsAddRespawnTimeOption(
        builder, index_or_zero(RESPAWN_TIME_MUTATOR_TYPES, mutators.get(RESPAWN_TIME))
    )
    return MutatorSettings.MutatorSettingsEnd(builder)
