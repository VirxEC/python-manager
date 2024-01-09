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
        self.player_index = standalone_bot_config.player_index or 0
        self.team = standalone_bot_config.team or 0
        self.name = self.get_bot_name()
        self.spawn_id = self.create_spawn_id()

    def get_bot_name(self) -> str:
        name = (
            self.python_file.name
            if self.standalone_bot_config.name is None
            else self.standalone_bot_config.name
        )
        print(f"Spawning your bot with the name {name} because no name was provided!")

        return name

    def create_spawn_id(self):
        """
        We want a spawn id unique to the bot which will be stable across re-runs.
        """
        return hash(self.name) % FLATBUFFER_MAX_INT

    def create_player_config(self) -> PlayerConfigurationT:
        player_config = PlayerConfigurationT()
        player_config.variety = RLBotPlayerT()
        player_config.varietyType = PlayerClass.RLBotPlayer
        player_config.name = self.name
        player_config.team = self.team
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
        match_settings.existingMatchBehavior = ExistingMatchBehavior.Restart
        match_settings.mutatorSettings = MutatorSettingsT()
        match_settings.enableStateSetting = True
        match_settings.enableRendering = True
        return match_settings

    def spawn_bot(self):
        match_settings = self.build_match_config()

        if self.match_manager is None:
            self.match_manager = MatchManager()
            self.match_manager.main_executable_path = Path(
                self.standalone_bot_config.main_executable_path
            )
            self.match_manager.connect_to_game()

        self.match_manager.match_settings = match_settings
        self.match_manager.start_match()
