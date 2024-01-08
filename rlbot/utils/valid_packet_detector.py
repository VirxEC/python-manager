import time

from rlbot.flat.GameStateType import GameStateType
from rlbot.flat.MatchSettings import MatchSettingsT
from rlbot.flat.PlayerClass import PlayerClass
from rlbot.game_manager.data_reporter import SocketDataReporter
from rlbot.utils.state_set import CarState, GameState, Physics, Vector3
from rlbot.utils.logging import get_logger


class ValidPacketDetector:
    def __init__(self, expected_match_config: MatchSettingsT):
        self.match_config = expected_match_config
        self.expected_count = len(self.match_config.playerConfigurations)
        self.socket_reporter = SocketDataReporter()
        self.logger = get_logger("vpd")

    def __del__(self):
        self.socket_reporter.disconnect()

    def wait_until_valid_packet(self):
        self.logger.info("Waiting for valid packet...")
        for i in range(0, 300):
            packet = self.socket_reporter.latest_packet
            if (
                packet is not None
                and packet.gameInfo is not None
                and packet.gameInfo.gameStateType != GameStateType.Ended
            ):
                spawn_ids = set()
                for k in range(0, self.expected_count):
                    player_config = self.match_config.playerConfigurations[k]
                    if (
                        player_config.varietyType == PlayerClass.RLBotPlayer
                        and player_config.spawnId > 0
                    ):
                        spawn_ids.add(player_config.spawnId)

                for player in packet.players:
                    try:
                        spawn_ids.remove(player.spawnId)
                    except KeyError:
                        pass

                if len(spawn_ids) == 0 and self.expected_count <= len(packet.players):
                    self.logger.info(
                        "Packets are looking good, all spawn ids accounted for!"
                    )
                    return
                elif i > 4:
                    max_index = 0
                    car_states = {}

                    for k, player_info in enumerate(packet.players):
                        if player_info.spawnId > 0:
                            car_states[k] = CarState(Physics(velocity=Vector3(z=500)))
                            max_index = k

                    if len(car_states) > 0:
                        self.logger.info(
                            "Scooting bots out of the way to allow more to spawn!"
                        )

                        game_state = GameState()
                        game_state.carStates = []

                        empty_offset = CarState()
                        for i in range(0, max_index + 1):
                            if i in car_states:
                                game_state.carStates.append(car_states[i])
                            else:
                                game_state.carStates.append(empty_offset)

                        self.socket_reporter.socket_relay.send_game_state(game_state)
            time.sleep(0.1)
        self.logger.info("Gave up waiting for valid packet :(")


def wait_until_valid_packet(match_settings: MatchSettingsT):
    detector = ValidPacketDetector(match_settings)
    detector.wait_until_valid_packet()
    del detector
