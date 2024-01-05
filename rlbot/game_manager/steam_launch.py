import subprocess
import webbrowser
from pathlib import Path
from typing import Optional

from rlbot.game_manager.preference import GameProcInfo
from rlbot.utils.logging import DEFAULT_LOGGER
from rlbot.utils.os_detector import CURRENT_OS, OS


def launch_rocket_league(port: int) -> bool:
    # Try launch via Steam.
    ideal_args = GameProcInfo.get_ideal_args(port)

    steam_exe_path = try_get_steam_executable_path()
    if (
        steam_exe_path
    ):  # Note: This Python 3.8 feature would be useful here https://www.python.org/dev/peps/pep-0572/#abstract
        exe_and_args = [
            str(steam_exe_path),
            "-applaunch",
            str(GameProcInfo.GAMEID),
        ] + ideal_args
        DEFAULT_LOGGER.info(f"Launching Rocket League with: {exe_and_args}")
        _ = subprocess.Popen(exe_and_args)  # This is deliberately an orphan process.
        return True

    DEFAULT_LOGGER.warning(
        f"Launching Rocket League using Steam-only fall-back launch method with args: {ideal_args}"
    )

    args_string = "%20".join(ideal_args)

    # Try launch via terminal (Linux)
    if CURRENT_OS == OS.LINUX:
        linux_args = [
            "steam",
            f"steam://rungameid/{GameProcInfo.GAMEID}//{args_string}",
        ]

        try:
            _ = subprocess.Popen(linux_args)
            return True
        except OSError:
            DEFAULT_LOGGER.warning("Could not launch Steam executable on Linux.")

    try:
        DEFAULT_LOGGER.info(
            "Launching rocket league via steam browser URL as a last resort..."
        )
        webbrowser.open(f"steam://rungameid/{GameProcInfo.GAMEID}//{args_string}")
    except webbrowser.Error:
        DEFAULT_LOGGER.warning(
            "Unable to launch Rocket League. Please launch Rocket League manually using the -rlbot option to continue."
        )
        return False
    return True


def try_get_steam_executable_path() -> Optional[Path]:
    """
    Tries to find the path of the Steam executable.
    Has platform specific code.
    """

    try:
        from winreg import (
            HKEY_CURRENT_USER,
            REG_SZ,
            ConnectRegistry,
            OpenKey,
            QueryValueEx,
        )
    except ImportError as e:
        return  # TODO: Linux support.

    try:
        key = OpenKey(ConnectRegistry(None, HKEY_CURRENT_USER), r"Software\Valve\Steam")
        val, val_type = QueryValueEx(key, "SteamExe")
    except FileNotFoundError:
        return
    if val_type != REG_SZ:
        return
    return Path(val)
