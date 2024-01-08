import inspect
import sys
from pathlib import Path
from typing import Type

from rlbot.agents.standalone import StandaloneBot
from rlbot.flat.FieldInfo import FieldInfoT
from rlbot.flat.GameTickPacket import GameTickPacketT
from rlbot.flat.MatchSettings import MatchSettingsT
from rlbot.game_manager.interface import SocketRelay
from rlbot.utils.standalone_arg_parser import StandaloneArgParser
from rlbot.utils.test_spawner import TestSpawner


class PythonBotRunner:
    def __init__(
        self, bot_class: Type[StandaloneBot], name: str, team: int, index: int, spawn_id
    ):
        self.bot = bot_class(name, team, index)
        self.bot._set_spawn_id(spawn_id)

        # store these seperately so the bot can't lie about it xD
        self.index = index
        self.team = team

        self.initialized_bot = False
        self.has_match_settings = False
        self.has_field_info = False

        self.game_interface = SocketRelay()
        self.game_interface.match_settings_handlers.append(self.handle_match_settings)
        self.game_interface.field_info_handlers.append(self.handle_field_info)
        self.game_interface.packet_handlers.append(self.handle_packet)
        self.bot._add_game_state_func(self.game_interface.send_game_state)
        self.bot.renderer._add_remove_render_group_func(
            self.game_interface.remove_render_group
        )
        self.bot.renderer._add_render_group_func(self.game_interface.send_render_group)

    def run(self):
        self.game_interface.connect_and_run(True, True, True)

    def handle_packet(self, packet: GameTickPacketT):
        if not self.initialized_bot:
            return

        controller = self.bot.get_output(packet)
        self.game_interface.send_player_input(self.index, controller)

    def handle_match_settings(self, match_settings: MatchSettingsT):
        self.bot._handle_match_settings(match_settings)
        self.has_match_settings = True
        if not self.initialized_bot and self.has_field_info:
            self.bot.initialize_agent()
            self.initialized_bot = True

    def handle_field_info(self, field_info: FieldInfoT):
        self.bot._handle_field_info(field_info)
        self.has_field_info = True
        if not self.initialized_bot and self.has_match_settings:
            self.bot.initialize_agent()
            self.initialized_bot = True


def run_bot(agent_class: Type[StandaloneBot]):
    config = StandaloneArgParser(sys.argv)
    python_file = inspect.getfile(agent_class)

    spawn_id = config.spawn_id
    player_index = config.player_index
    team = config.team
    name = config.name

    if config.is_missing_args:
        # This process must not have been created by the RLBot framework, so this is probably
        # a developer doing some testing who did not pass all the params. Take it upon ourselves
        # to fire up the game if necessary.
        print(
            f"############################################################################################"
        )
        print(
            f"Args are missing, so we will assume this is a dev workflow and insert the bot into the game!"
        )
        print(
            f"############################################################################################"
        )
        test_spawner = TestSpawner(Path(python_file), config)
        test_spawner.spawn_bot()
        spawn_id = test_spawner.spawn_id
        player_index = test_spawner.player_index
        team = test_spawner.team
        name = test_spawner.name

    python_bot_runner = PythonBotRunner(agent_class, name, team, player_index, spawn_id)
    python_bot_runner.run()
