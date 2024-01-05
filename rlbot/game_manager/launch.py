from typing import Optional

from rlbot.game_manager import epic_launch, steam_launch
from rlbot.game_manager.preference import (
    DEFAULT_LAUNCHER_PREFERENCE,
    GameLauncherPreference,
    GameProcInfo,
)
from rlbot.utils import process_configuration
from rlbot.utils.logging import DEFAULT_LOGGER


def is_rocket_league_running(port: int) -> bool:
    """
    Returns whether or not Rocket League is running with the right port.
    """

    try:
        is_rocket_league_running, proc = process_configuration.is_process_running(
            GameProcInfo.FILE_NAME,
            GameProcInfo.PROCESS_NAME,
            GameProcInfo.REQUIRED_ARGS,
        )

        if proc is not None:
            # Check for correct port.
            rocket_league_port = _read_port_from_rocket_league_args(proc.cmdline())
            if rocket_league_port is not None and rocket_league_port != port:
                raise Exception(
                    f"Rocket League is already running with port {rocket_league_port} but we wanted "
                    f"{port}! Please close Rocket League and let us start it for you instead!"
                )
    except process_configuration.WrongProcessArgs:
        raise Exception(
            f"Rocket League is not running with {GameProcInfo.REQUIRED_ARGS}!\n"
            "Please close Rocket League and let us start it for you instead!"
        )

    return is_rocket_league_running


def _read_port_from_rocket_league_args(args: list[str]) -> Optional[int]:
    for arg in args:
        # The arg will look like RLBot_ControllerURL="127.0.0.1:23233"
        if "RLBot_ControllerURL" in arg:
            rocket_league_port = int(arg.split(":")[1].replace('"', ""))
            return int(rocket_league_port)


def launch_rocket_league(
    port: int, launcher_preference: GameLauncherPreference = DEFAULT_LAUNCHER_PREFERENCE
) -> bool:
    if launcher_preference.preferred_launcher == GameLauncherPreference.EPIC_ONLY:
        return epic_launch.launch_rocket_league(port, launcher_preference)
    elif launcher_preference.preferred_launcher == GameLauncherPreference.STEAM:
        return steam_launch.launch_rocket_league(port)
    elif launcher_preference.preferred_launcher == GameLauncherPreference.EPIC:
        # Historically, the preference of EPIC has caused RLBot to try Epic first, then Steam.
        # Keeping that behavior for backwards compatibility.
        epic_worked = epic_launch.launch_rocket_league(port, launcher_preference)
        if epic_worked:
            return True

        DEFAULT_LOGGER.info("Epic launch has failed, falling back to Steam!")
        return steam_launch.launch_rocket_league(port)
    return False
