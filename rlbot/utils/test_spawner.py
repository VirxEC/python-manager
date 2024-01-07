import hashlib
from pathlib import Path
from typing import Optional

from rlbot.config_parsing.match import FLATBUFFER_MAX_INT
from rlbot.flat.ExistingMatchBehavior import ExistingMatchBehavior
from rlbot.flat.GameMode import GameMode
from rlbot.flat.LoadoutPaint import LoadoutPaintT
from rlbot.flat.MatchSettings import MatchSettingsT
from rlbot.flat.MutatorSettings import MutatorSettingsT
from rlbot.flat.PlayerClass import PlayerClass
from rlbot.flat.PlayerConfiguration import PlayerConfigurationT
from rlbot.flat.PlayerLoadout import PlayerLoadoutT
from rlbot.flat.RLBotPlayer import RLBotPlayerT
from rlbot.match_manager import MatchManager
from rlbot.utils import gateway
from rlbot.utils.standalone_arg_parser import StandaloneArgParser


class TestSpawner:
    def __init__(
        self,
        python_file: Path,
        standalone_bot_config: StandaloneArgParser,
    ):
        self.python_file = python_file
        self.standalone_bot_config = standalone_bot_config
        self.player_config: Optional[PlayerConfigurationT] = None
        self.match_manager: Optional[MatchManager] = None
        self.spawn_id = self.create_spawn_id()
        self.player_index = standalone_bot_config.player_index or 0
        self.team = standalone_bot_config.team or 0
        self.name = self.get_bot_name()

    def get_bot_name(self) -> str:
        if self.standalone_bot_config.name is not None:
            print(
                f"Spawning your bot with the name {self.standalone_bot_config.name} because no config path was provided!"
            )
            return self.standalone_bot_config.name
        print(
            f"Spawning your bot with the name {self.python_file.name} because no config path was provided!"
        )
        return self.python_file.name

    def create_spawn_id(self):
        """
        We want a spawn id unique to the python file which will be stable across re-runs.
        """
        hash = hashlib.sha1(str(self.python_file).encode("utf-8"))
        number_form = int(hash.hexdigest(), 16)
        return number_form % FLATBUFFER_MAX_INT

    def create_player_config(self) -> PlayerConfigurationT:
        player_config = PlayerConfigurationT()
        player_config.variety = RLBotPlayerT()
        player_config.varietyType = PlayerClass.RLBotPlayer
        player_config.name = self.name
        player_config.team = 0
        player_config.spawnId = self.spawn_id
        player_config.loadout = PlayerLoadoutT()
        player_config.loadout.loadoutPaint = LoadoutPaintT()
        return player_config

    def build_match_config(self) -> MatchSettingsT:
        if self.player_config is None:
            self.player_config = self.create_player_config()

        match_settings = MatchSettingsT()
        match_settings.playerConfigurations = [self.player_config]
        match_settings.gameMode = GameMode.Soccer
        match_settings.gameMapUpk = "Stadium_P"
        match_settings.existingMatchBehavior = ExistingMatchBehavior.Continue_And_Spawn
        match_settings.mutatorSettings = MutatorSettingsT()
        match_settings.enableStateSetting = True
        match_settings.enableRendering = True
        return match_settings

    def spawn_bot(self):
        match_settings = self.build_match_config()

        if self.match_manager is None:
            self.match_manager = MatchManager()

            rlbot_gateway_process, _ = gateway.find_existing_process()
            if rlbot_gateway_process is None:
                # RLBot.exe is not running yet, we should use the Restart behavior.
                # That avoids a situation where dead cars start piling up when
                # RLBot.exe gets killed and re-launched over and over and lacks context
                # to clean up previous cars.
                match_settings.existingMatchBehavior = ExistingMatchBehavior.Restart

            self.match_manager.main_executable_path = Path(
                self.standalone_bot_config.main_executable_path
            )
            self.match_manager.connect_to_game()

        self.match_manager.match_settings = match_settings
        self.match_manager.start_match()
