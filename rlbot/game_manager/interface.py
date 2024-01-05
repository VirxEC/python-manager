from enum import IntEnum
from socket import SHUT_WR, socket, timeout
from threading import Thread
from time import sleep
from typing import Callable

from flatbuffers.builder import Builder

from rlbot.flat import ReadyMessage
from rlbot.flat.BallPrediction import BallPrediction
from rlbot.flat.FieldInfo import FieldInfo
from rlbot.flat.GameMessage import GameMessage
from rlbot.flat.GameTickPacket import GameTickPacket
from rlbot.flat.MatchSettings import MatchSettings
from rlbot.flat.MessagePacket import MessagePacket
from rlbot.flat.PlayerInputChange import PlayerInputChange
from rlbot.flat.PlayerSpectate import PlayerSpectate
from rlbot.flat.PlayerStatEvent import PlayerStatEvent
from rlbot.flat.QuickChat import QuickChat
from rlbot.utils.logging import get_logger

# We can connect to RLBot.exe on this port.
RLBOT_SOCKETS_PORT = 23234


class SocketDataType(IntEnum):
    GAME_TICK_PACKET = 1
    FIELD_INFO = 2
    MATCH_SETTINGS = 3
    PLAYER_INPUT = 4
    ACTOR_MAPPING = 5
    COMPUTER_ID = 6
    DESIRED_GAME_STATE = 7
    RENDER_GROUP = 8
    QUICK_CHAT = 9
    BALL_PREDICTION = 10
    READY_MESSAGE = 11
    MESSAGE_PACKET = 12


def int_to_bytes(val: int) -> bytes:
    return val.to_bytes(2, byteorder="big")


def int_from_bytes(bytes: bytes) -> int:
    return int.from_bytes(bytes, "big")


class SocketMessage:
    def __init__(self, type: SocketDataType, data: bytes):
        self.type = type
        self.data = data


def read_from_socket(s: socket) -> SocketMessage:
    type_int = int_from_bytes(s.recv(2))
    if type_int == 0:
        raise EOFError()
    data_type = SocketDataType(type_int)
    size = int_from_bytes(s.recv(2))
    data = s.recv(size)
    return SocketMessage(data_type, data)


class SocketRelay:
    def __init__(self, connection_timeout: float = 120):
        self.connection_timeout = connection_timeout
        self.logger = get_logger("socket_man")
        self.socket = socket()
        self.is_connected = False
        self.got_valid_packet = False
        self._should_continue = True
        self.on_connect_handlers: list[Callable[[], None]] = []
        self.packet_handlers: list[Callable[[GameTickPacket], None]] = []
        self.field_info_handlers: list[Callable[[FieldInfo], None]] = []
        self.match_settings_handlers: list[Callable[[MatchSettings], None]] = []
        self.quick_chat_handlers: list[Callable[[QuickChat], None]] = []
        self.ball_prediction_handlers: list[Callable[[BallPrediction], None]] = []
        self.player_input_change_handlers: list[
            Callable[[PlayerInputChange, float, int], None]
        ] = []
        self.player_stat_handlers: list[
            Callable[[PlayerStatEvent, float, int], None]
        ] = []
        self.player_spectate_handlers: list[
            Callable[[PlayerSpectate, float, int], None]
        ] = []
        self.raw_handlers: list[Callable[[SocketMessage], None]] = []

    def send_flatbuffer(self, builder: Builder, data_type: SocketDataType):
        self.send_bytes(builder.Output(), data_type)

    def send_bytes(self, byte_array: bytearray, data_type: SocketDataType):
        size = len(byte_array)
        message = int_to_bytes(data_type) + int_to_bytes(size) + byte_array
        self.socket.sendall(message)

    # def send_player_input(self, player_index: int, input: SimpleControllerState):
    #     builder = input.to_flatbuffer(player_index)
    #     self.send_flatbuffer(builder, SocketDataType.PLAYER_INPUT)

    # def send_game_state(self, state: GameState):
    #     builder = Builder(400)
    #     game_state_offset = state.convert_to_flat(builder)
    #     if game_state_offset is None:
    #         return  # There are no values to be set, so just skip it
    #     builder.Finish(game_state_offset)
    #     self.send_flatbuffer(builder, SocketDataType.DESIRED_GAME_STATE)
    #     pass

    def start_match(self, match_settings: bytearray):
        def connect_handler():
            self.send_bytes(match_settings, SocketDataType.MATCH_SETTINGS)

        self.run_after_connect(connect_handler)

    def run_after_connect(self, handler: Callable[[], None]):
        if self.is_connected:
            handler()
        else:
            self.on_connect_handlers.append(handler)
            try:
                self.connect_and_run(
                    wants_quick_chat=False,
                    wants_ball_predictions=False,
                    wants_game_messages=False,
                    only_wait_for_ready=True,
                )
            except timeout:
                raise TimeoutError("Took too long to connect to the RLBot executable!")

    def connect_and_run(
        self,
        wants_quick_chat: bool,
        wants_game_messages: bool,
        wants_ball_predictions: bool,
        only_wait_for_ready: bool = False,
    ):
        """
        Connects to the socket and begins a loop that reads messages and calls any handlers
        that have been registered. Connect and run are combined into a single method because
        currently bad things happen if the buffer is allowed to fill up.
        """
        self.socket.settimeout(self.connection_timeout)
        for _ in range(int(self.connection_timeout * 10)):
            try:
                self.socket.connect(("127.0.0.1", RLBOT_SOCKETS_PORT))
                break
            except ConnectionRefusedError:
                sleep(0.1)
            except ConnectionAbortedError:
                sleep(0.1)

        self.socket.settimeout(None)
        self.is_connected = True
        self.logger.info(
            f"Socket manager connected to port {RLBOT_SOCKETS_PORT} from port {self.socket.getsockname()[1]}!"
        )
        for handler in self.on_connect_handlers:
            handler()

        builder = self.make_ready_message(
            wants_ball_predictions, wants_game_messages, wants_quick_chat
        )
        self.send_flatbuffer(builder, SocketDataType.READY_MESSAGE)

        incoming_message = read_from_socket(self.socket)
        self.handle_incoming_message(incoming_message)

        if only_wait_for_ready:
            Thread(target=self.handle_incoming_messages).start()
        else:
            self.handle_incoming_messages()

    def handle_incoming_messages(self):
        while self._should_continue:
            incoming_message = read_from_socket(self.socket)
            self.handle_incoming_message(incoming_message)

        self.socket.shutdown(SHUT_WR)

        # Now wait for the other end to send its own shutdown signal.
        try:
            while True:
                read_from_socket(self.socket)
        except EOFError:
            # We've succeeded with our graceful shutdown.
            pass

        self.socket.close()

    def make_ready_message(
        self,
        wants_ball_predictions: bool,
        wants_game_messages: bool,
        wants_quick_chat: bool,
    ):
        builder = Builder(50)
        ReadyMessage.ReadyMessageStart(builder)
        ReadyMessage.ReadyMessageAddWantsBallPredictions(
            builder, wants_ball_predictions
        )
        ReadyMessage.ReadyMessageAddWantsQuickChat(builder, wants_quick_chat)
        ReadyMessage.ReadyMessageAddWantsGameMessages(builder, wants_game_messages)
        offset = ReadyMessage.ReadyMessageEnd(builder)
        builder.Finish(offset)
        return builder

    def handle_incoming_message(self, incoming_message: SocketMessage):
        for raw_handler in self.raw_handlers:
            raw_handler(incoming_message)
        if (
            incoming_message.type == SocketDataType.GAME_TICK_PACKET
            and len(self.packet_handlers) > 0
        ):
            packet = GameTickPacket.GetRootAsGameTickPacket(incoming_message.data, 0)
            for handler in self.packet_handlers:
                handler(packet)
        elif (
            incoming_message.type == SocketDataType.FIELD_INFO
            and len(self.field_info_handlers) > 0
        ):
            field_info = FieldInfo.GetRootAsFieldInfo(incoming_message.data, 0)
            for handler in self.field_info_handlers:
                handler(field_info)
        elif (
            incoming_message.type == SocketDataType.MATCH_SETTINGS
            and len(self.match_settings_handlers) > 0
        ):
            match_settings = MatchSettings.GetRootAsMatchSettings(
                incoming_message.data, 0
            )
            for handler in self.match_settings_handlers:
                handler(match_settings)
        elif (
            incoming_message.type == SocketDataType.QUICK_CHAT
            and len(self.quick_chat_handlers) > 0
        ):
            quick_chat = QuickChat.GetRootAsQuickChat(incoming_message.data, 0)
            for handler in self.quick_chat_handlers:
                handler(quick_chat)
        elif (
            incoming_message.type == SocketDataType.BALL_PREDICTION
            and len(self.ball_prediction_handlers) > 0
        ):
            ball_prediction = BallPrediction.GetRootAsBallPrediction(
                incoming_message.data, 0
            )
            for handler in self.ball_prediction_handlers:
                handler(ball_prediction)
        elif incoming_message.type == SocketDataType.MESSAGE_PACKET:
            if (
                len(self.player_stat_handlers) > 0
                or len(self.player_input_change_handlers) > 0
                or len(self.player_spectate_handlers) > 0
            ):
                msg_packet = MessagePacket.GetRootAsMessagePacket(
                    incoming_message.data, 0
                )
                for i in range(msg_packet.MessagesLength()):
                    msg = msg_packet.Messages(i)
                    msg_type = msg.MessageType()

                    if (
                        msg_type == GameMessage.PlayerSpectate
                        and len(self.player_spectate_handlers) > 0
                    ):
                        spectate = PlayerSpectate()
                        spectate.Init(msg.Message().Bytes, msg.Message().Pos)
                        for handler in self.player_spectate_handlers:
                            handler(
                                spectate,
                                msg_packet.GameSeconds(),
                                msg_packet.FrameNum(),
                            )
                    elif (
                        msg_type == GameMessage.PlayerStatEvent
                        and len(self.player_stat_handlers) > 0
                    ):
                        stat_event = PlayerStatEvent()
                        stat_event.Init(msg.Message().Bytes, msg.Message().Pos)
                        for handler in self.player_stat_handlers:
                            handler(
                                stat_event,
                                msg_packet.GameSeconds(),
                                msg_packet.FrameNum(),
                            )
                    elif (
                        msg_type == GameMessage.PlayerInputChange
                        and len(self.player_input_change_handlers) > 0
                    ):
                        input_change = PlayerInputChange()
                        input_change.Init(msg.Message().Bytes, msg.Message().Pos)
                        for handler in self.player_input_change_handlers:
                            handler(
                                input_change,
                                msg_packet.GameSeconds(),
                                msg_packet.FrameNum(),
                            )

    def disconnect(self):
        self._should_continue = False
