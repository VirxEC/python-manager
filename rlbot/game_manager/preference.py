from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from rlbot.utils.os_detector import CURRENT_OS, OS


class GameProcInfo:
    GAMEID = 252950
    PROCESS_NAME = "RocketLeague.exe" if CURRENT_OS == OS.WINDOWS else "RocketLeague.ex"
    FILE_NAME = "RocketLeague.exe"
    REQUIRED_ARGS = {r"-rlbot", r"RLBot_ControllerURL=127.0.0.1:[0-9]+"}

    @staticmethod
    def get_ideal_args(port: int) -> list[str]:
        # We are specifying RLBot_PacketSendRate=240, which will override people's TARLBot.ini settings.
        # We believe there is no downside to 240. See https://github.com/RLBot/RLBot/wiki/Tick-Rate
        return [
            "-rlbot",
            f"RLBot_ControllerURL=127.0.0.1:{port}",
            "RLBot_PacketSendRate=240",
            "-nomovie",
        ]


@dataclass
class GameLauncherPreference:
    STEAM = "steam"
    EPIC = "epic"  # This tries epic first, then falls back to steam. Weird name is for backwards compat.
    EPIC_ONLY = "epic_only"
    preferred_launcher: str
    use_login_tricks: bool
    game_exe_path: Optional[Path] = None


# By default, we will attempt Epic with login tricks, then fall back to Steam.
DEFAULT_LAUNCHER_PREFERENCE = GameLauncherPreference(
    GameLauncherPreference.EPIC, True
)
