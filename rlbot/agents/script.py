from rlbot.flat.DesiredGameState import DesiredGameStateT
from rlbot.flat.FieldInfo import FieldInfoT
from rlbot.flat.GameTickPacket import GameTickPacketT
from rlbot.flat.MatchSettings import MatchSettingsT
from rlbot.game_manager.interface import SocketRelay
from rlbot.game_manager.rendering import RenderingManager
from rlbot.utils.logging import get_logger


class StandaloneScript:
    """
    A convenience class for building scripts on top of.
    It is NOT required to use this when configuring a script.
    """

    def __init__(self, name):
        self.name = name
        self.logger = get_logger(name)
        self.game_interface = SocketRelay(logger=self.logger)

        self.game_interface.match_settings_handlers.append(self.handle_match_settings)
        self.game_interface.field_info_handlers.append(self.handle_field_info)
        self.game_interface.packet_handlers.append(self.handle_packet)

        self.renderer = RenderingManager()
        self.renderer._add_remove_render_group_func(
            self.game_interface.remove_render_group
        )
        self.renderer._add_render_group_func(self.game_interface.send_render_group)

    def set_game_state(self, game_state: DesiredGameStateT):
        self.game_interface.send_game_state(game_state)

    def run(self):
        self.game_interface.connect_and_run(True, True, True)
        del self.game_interface

    def handle_match_settings(self, match_settings: MatchSettingsT):
        pass

    def handle_field_info(self, field_info: FieldInfoT):
        pass

    def handle_packet(self, packet: GameTickPacketT):
        pass
