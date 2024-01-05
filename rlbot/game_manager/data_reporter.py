from threading import Thread

from rlbot.flat.FieldInfo import FieldInfoT
from rlbot.flat.GameTickPacket import GameTickPacketT
from rlbot.flat.MatchSettings import MatchSettingsT
from rlbot.game_manager.interface import SocketRelay


class SocketDataReporter:
    def __init__(self):
        self.latest_packet = GameTickPacketT()
        self.latest_field_info = FieldInfoT()
        self.latest_match_settings = MatchSettingsT()

        self.socket_relay = SocketRelay()
        self.socket_relay.packet_handlers.append(self._handle_packet)
        self.socket_relay.field_info_handlers.append(self._handle_field_info)
        self.socket_relay.match_settings_handlers.append(self._handle_match_settings)

        self.thread = Thread(
            target=self.socket_relay.connect_and_run, args=(False, False, False)
        )

        self.thread.start()

    def _handle_packet(self, packet: GameTickPacketT):
        self.latest_packet = packet

    def _handle_field_info(self, field_info: FieldInfoT):
        self.latest_field_info = field_info

    def _handle_match_settings(self, match_settings: MatchSettingsT):
        self.latest_match_settings = match_settings

    def disconnect(self):
        self.socket_relay.disconnect()


def get_one_packet() -> GameTickPacketT:
    socket_relay = SocketRelay()
    packet = GameTickPacketT()

    def handle_packet(p):
        nonlocal packet
        packet = p
        socket_relay.disconnect()

    socket_relay.packet_handlers.append(handle_packet)
    socket_relay.connect_and_run(False, False, False)
    return packet
