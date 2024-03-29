from typing import Callable, Optional
from rlbot.flat.DesiredGameState import DesiredGameStateT
from rlbot.flat.FieldInfo import FieldInfoT
from rlbot.flat.MatchSettings import MatchSettingsT
from rlbot.game_manager.rendering import RenderingManager


class Runnable:
    def __init__(self, name: str):
        self.name = name
        self.spawn_id: Optional[int] = None

        self.match_settings = MatchSettingsT()
        self.field_info = FieldInfoT()
        self.renderer = RenderingManager()

        self._set_game_state_func: Callable[[DesiredGameStateT], None] = lambda _: None

    def _add_game_state_func(
        self, set_game_state_func: Callable[[DesiredGameStateT], None]
    ):
        self._set_game_state_func = set_game_state_func

    def _handle_match_settings(self, match_settings: MatchSettingsT):
        self.match_settings = match_settings

    def _handle_field_info(self, field_info: FieldInfoT):
        self.field_info = field_info

    def get_match_settings(self) -> MatchSettingsT:
        """
        Contains info about what map you're on, mutators, etc.
        """
        return self.match_settings

    def get_field_info(self) -> FieldInfoT:
        """
        Contains info about the map, such as the locations of boost pads and goals.
        """
        return self.field_info

    def set_game_state(self, game_state: DesiredGameStateT):
        """
        Sets the game to the given desired state.
        """
        self._set_game_state_func(game_state)

    def initialize_agent(self):
        """
        Called for all heaver initialization that needs to happen.
        Field info and match settings are fully loaded at this point, and won't return garbage data.
        """
        pass

    def retire(self):
        """Called after the game ends"""
        pass

    def _set_spawn_id(self, spawn_id: int):
        self.spawn_id = spawn_id
