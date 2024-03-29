import logging
from enum import IntEnum
from socket import socket, timeout
from threading import Thread
from time import sleep
from typing import Callable, Optional

from flatbuffers.builder import Builder

from rlbot.flat import ReadyMessage
from rlbot.flat.BallPrediction import BallPrediction, BallPredictionT
from rlbot.flat.ControllerState import ControllerStateT
from rlbot.flat.DesiredGameState import DesiredGameStateT
from rlbot.flat.FieldInfo import FieldInfo, FieldInfoT
from rlbot.flat.GameMessage import GameMessage
from rlbot.flat.GameTickPacket import GameTickPacket, GameTickPacketT
from rlbot.flat.MatchSettings import MatchSettings, MatchSettingsT
from rlbot.flat.MessagePacket import MessagePacket, MessagePacketT
from rlbot.flat.PlayerInput import PlayerInputT
from rlbot.flat.PlayerInputChange import PlayerInputChangeT
from rlbot.flat.PlayerSpectate import PlayerSpectateT
from rlbot.flat.PlayerStatEvent import PlayerStatEventT
from rlbot.flat.QuickChat import QuickChat, QuickChatT
from rlbot.flat.RemoveRenderGroup import RemoveRenderGroupT
from rlbot.flat.RenderGroup import RenderGroupT
from rlbot.flat.RenderType import RenderType
from rlbot.utils.logging import get_logger

# We can connect to RLBot.exe on this port.
RLBOT_SOCKETS_PORT = 23234


class SocketDataType(IntEnum):
    NONE = 0
    GAME_TICK_PACKET = 1
    FIELD_INFO = 2
    MATCH_SETTINGS = 3
    PLAYER_INPUT = 4
    DESIRED_GAME_STATE = 5
    RENDER_GROUP = 6
    REMOVE_RENDER_GROUP = 7
    QUICK_CHAT = 8
    BALL_PREDICTION = 9
    READY_MESSAGE = 10
    MESSAGE_PACKET = 11


MAX_SIZE_2_BYTES = 2**16 - 1


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
    data_type = SocketDataType(type_int)
    size = int_from_bytes(s.recv(2))
    data = s.recv(size)
    return SocketMessage(data_type, data)


class SocketRelay:
    def __init__(self, connection_timeout: float = 120, logger: Optional[logging.Logger] = None):
        self.connection_timeout = connection_timeout
        self.logger = get_logger("socket_man") if logger is None else logger
        self.socket = socket()
        self.is_connected = False
        self._should_continue = True
        self.on_connect_handlers: list[Callable[[], None]] = []
        self.packet_handlers: list[Callable[[GameTickPacketT], None]] = []
        self.field_info_handlers: list[Callable[[FieldInfoT], None]] = []
        self.match_settings_handlers: list[Callable[[MatchSettingsT], None]] = []
        self.quick_chat_handlers: list[Callable[[QuickChatT], None]] = []
        self.ball_prediction_handlers: list[Callable[[BallPredictionT], None]] = []
        self.player_input_change_handlers: list[
            Callable[[PlayerInputChangeT, float, int], None]
        ] = []
        self.player_stat_handlers: list[
            Callable[[PlayerStatEventT, float, int], None]
        ] = []
        self.player_spectate_handlers: list[
            Callable[[PlayerSpectateT, float, int], None]
        ] = []
        self.raw_handlers: list[Callable[[SocketMessage], None]] = []

    def __del__(self):
        self.socket.close()

    def send_flatbuffer(self, builder: Builder, data_type: SocketDataType):
        self.send_bytes(builder.Output(), data_type)

    def send_bytes(self, byte_array: bytearray, data_type: SocketDataType):
        size = len(byte_array)
        if size > MAX_SIZE_2_BYTES:
            self.logger.error(
                f"Couldn't send a {data_type} message because it was too big!"
            )
            return

        message = int_to_bytes(data_type) + int_to_bytes(size) + byte_array
        self.socket.sendall(message)

    def send_player_input(self, player_index: int, input: ControllerStateT):
        player_input = PlayerInputT()
        player_input.playerIndex = player_index
        player_input.controllerState = input
        builder = Builder(30)
        player_input_offset = player_input.Pack(builder)
        builder.Finish(player_input_offset)
        self.send_flatbuffer(builder, SocketDataType.PLAYER_INPUT)

    def send_game_state(self, state: DesiredGameStateT):
        builder = Builder(400)
        game_state_offset = state.Pack(builder)
        builder.Finish(game_state_offset)
        self.send_flatbuffer(builder, SocketDataType.DESIRED_GAME_STATE)

    def send_render_group(self, render_group: RenderGroupT):
        size = 0
        # calculate the size needed because
        # renders can be either kinda small or really big
        for render in render_group.renderMessages:
            if render.varietyType == RenderType.Line3D:
                size += 28
            elif render.varietyType == RenderType.PolyLine3D:
                size += 4 + 12 * len(render.variety.points)
            elif render.varietyType == RenderType.String2D:
                size += 16 + len(render.variety.text)
            elif render.varietyType == RenderType.String3D:
                size += 20 + len(render.variety.text)

        builder = Builder(size)
        builder.Finish(render_group.Pack(builder))
        self.send_flatbuffer(builder, SocketDataType.RENDER_GROUP)

    def remove_render_group(self, group_id: int):
        builder = Builder(4)
        msg = RemoveRenderGroupT()
        msg.id = group_id
        builder.Finish(msg.Pack(builder))
        self.send_flatbuffer(builder, SocketDataType.REMOVE_RENDER_GROUP)

    def start_match(self, match_settings: MatchSettingsT):
        builder = Builder(400)
        builder.Finish(match_settings.Pack(builder))
        byte_array = builder.Output()

        def connect_handler():
            self.send_bytes(byte_array, SocketDataType.MATCH_SETTINGS)

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
        try:
            while self._should_continue:
                incoming_message = read_from_socket(self.socket)
                self.handle_incoming_message(incoming_message)
        except:
            self.logger.error("Socket manager disconnected unexpectedly!")

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
        if incoming_message.type == SocketDataType.NONE:
            self._should_continue = False
        elif (
            incoming_message.type == SocketDataType.GAME_TICK_PACKET
            and len(self.packet_handlers) > 0
        ):
            packet = GameTickPacket.GetRootAsGameTickPacket(incoming_message.data, 0)
            for handler in self.packet_handlers:
                handler(GameTickPacketT.InitFromObj(packet))
        elif (
            incoming_message.type == SocketDataType.FIELD_INFO
            and len(self.field_info_handlers) > 0
        ):
            field_info = FieldInfo.GetRootAsFieldInfo(incoming_message.data, 0)
            for handler in self.field_info_handlers:
                handler(FieldInfoT.InitFromObj(field_info))
        elif (
            incoming_message.type == SocketDataType.MATCH_SETTINGS
            and len(self.match_settings_handlers) > 0
        ):
            match_settings = MatchSettings.GetRootAsMatchSettings(
                incoming_message.data, 0
            )
            for handler in self.match_settings_handlers:
                handler(MatchSettingsT.InitFromObj(match_settings))
        elif (
            incoming_message.type == SocketDataType.QUICK_CHAT
            and len(self.quick_chat_handlers) > 0
        ):
            quick_chat = QuickChat.GetRootAsQuickChat(incoming_message.data, 0)
            for handler in self.quick_chat_handlers:
                handler(QuickChatT.InitFromObj(quick_chat))
        elif (
            incoming_message.type == SocketDataType.BALL_PREDICTION
            and len(self.ball_prediction_handlers) > 0
        ):
            ball_prediction = BallPrediction.GetRootAsBallPrediction(
                incoming_message.data, 0
            )
            for handler in self.ball_prediction_handlers:
                handler(BallPredictionT.InitFromObj(ball_prediction))
        elif incoming_message.type == SocketDataType.MESSAGE_PACKET:
            if (
                len(self.player_stat_handlers) > 0
                or len(self.player_input_change_handlers) > 0
                or len(self.player_spectate_handlers) > 0
            ):
                msg_packet = MessagePacketT.InitFromObj(
                    MessagePacket.GetRootAsMessagePacket(incoming_message.data, 0)
                )

                skip_player_input_change = len(self.player_input_change_handlers) == 0
                skip_player_spectate = len(self.player_spectate_handlers) == 0
                skip_player_stat = len(self.player_stat_handlers) == 0

                for msg in msg_packet.messages:
                    msg_type = msg.messageType

                    if msg_type == GameMessage.PlayerInputChange:
                        if skip_player_input_change:
                            continue
                        handlers = self.player_input_change_handlers
                    elif msg_type == GameMessage.PlayerSpectate:
                        if skip_player_spectate:
                            continue
                        handlers = self.player_spectate_handlers
                    elif msg_type == GameMessage.PlayerStatEvent:
                        if skip_player_stat:
                            continue
                        handlers = self.player_stat_handlers
                    else:
                        continue

                    for handler in handlers:
                        handler(
                            msg.message,  # type: ignore
                            msg_packet.gameSeconds,
                            msg_packet.frameNum,
                        )

    def disconnect(self):
        self.send_bytes(bytearray([1]), SocketDataType.NONE)
