from pathlib import Path
from time import sleep
from typing import Any, Optional

from rlbot import version
from rlbot.config_parsing.match import (
    DEFAULT_CONFIG_LOCATION,
    get_launcher_preference,
    get_main_executable_path,
    get_match_settings,
)
from rlbot.config_parsing.util import load_config_file
from rlbot.flat.MatchSettings import MatchSettings
from rlbot.game_manager import launch
from rlbot.game_manager.interface import SocketRelay
from rlbot.game_manager.preference import (
    DEFAULT_LAUNCHER_PREFERENCE,
    GameLauncherPreference,
)
from rlbot.utils import gateway, ta_settings
from rlbot.utils.logging import DEFAULT_LOGGER
from rlbot.utils.os_detector import MAIN_EXECUTABLE_NAME
from rlbot.utils.valid_packet_detector import wait_until_valid_packet


class MatchManager:
    def __init__(self):
        self.logger = DEFAULT_LOGGER
        self.launcher_preference = DEFAULT_LAUNCHER_PREFERENCE
        self.main_executable_path: Optional[Path] = None
        self.game_interface: SocketRelay = SocketRelay()
        self.match_settings: Optional[tuple[MatchSettings, bytearray]] = None
        self.has_started = False

    def load_config_from_file(self, config_location: Path = DEFAULT_CONFIG_LOCATION):
        self.logger.info(f"Reading {config_location} for match configuration")

        config = load_config_file(config_location)
        self.load_config(config)

    def load_config(self, config: dict[str, Any]):
        self.launcher_preference = get_launcher_preference(config)
        self.main_executable_path = get_main_executable_path(config)
        self.match_settings = get_match_settings(config)

    def connect_to_game(
        self,
        launcher_preference: Optional[GameLauncherPreference] = None,
        main_executable_path: Optional[Path] = None,
    ):
        """
        Connects to the game by initializing self.game_interface.
        """
        version.print_current_release_notes()

        main_executable_path = main_executable_path or self.main_executable_path
        if main_executable_path is None:
            raise Exception("No main_executable_path found. Please specify it.")
        port = self.ensure_rlbot_gateway_started(main_executable_path)
        self.logger.info(f"Connecting to game on port {port}...")

        # Prevent loading game interface twice.
        if self.has_started:
            if not launch.is_rocket_league_running(port):
                raise Exception(
                    "Rocket League is not running even though we started it once.\n"
                    "Please restart RLBot."
                )
            return

        # Launch the game if it is not running.
        if not launch.is_rocket_league_running(port):
            ta_settings.merge()
            pref = (
                launcher_preference
                or self.launcher_preference
                or DEFAULT_LAUNCHER_PREFERENCE
            )
            if not launch.launch_rocket_league(port=port, launcher_preference=pref):
                raise Exception("Failed to launch Rocket League!")  

        self.has_started = True

    def ensure_rlbot_gateway_started(self, main_executable_path: Path) -> int:
        """
        Ensures that RLBot.exe is running.

        Returns the port that it will be listening on for connections from Rocket League.
        Rocket League should be passed a command line argument so that it starts with this same port.
        """

        self.rlbot_gateway_process, port = gateway.find_existing_process()
        if self.rlbot_gateway_process is not None:
            self.logger.info(
                f"Already have {MAIN_EXECUTABLE_NAME} running! Port is {port}"
            )
            return port

        self.rlbot_gateway_process, port = gateway.launch(main_executable_path)
        self.logger.info(
            f"Python started RLBot.exe with process id {self.rlbot_gateway_process.pid} "
            f"and port {port}"
        )
        return port

    def start_match(self):
        if self.match_settings is None:
            raise Exception(
                "No match settings found. Please specify them with load_config."
            )

        self.logger.info("Python attempting to start match.")
        self.game_interface.start_match(self.match_settings[1])
        wait_until_valid_packet(self.match_settings[0])
        self.logger.info("Match has started")

        ta_settings.clean_up()

    def shut_down(self, quiet: bool = False):
        if not quiet:
            self.logger.info("Shutting down RLBot")

        self.game_interface.disconnect()

        if self.rlbot_gateway_process is not None:
            if not quiet:
                self.logger.info(f"Killing {MAIN_EXECUTABLE_NAME}...")
            self.rlbot_gateway_process.terminate()
        elif not quiet:
            self.logger.info(f"{MAIN_EXECUTABLE_NAME} is not running.")

        if not quiet:
            self.logger.info("Shut down complete!")
