import time

from rlbot.flat.PlayerClass import PlayerClass
from rlbot.flat.MatchSettings import MatchSettings
from rlbot.game_manager.data_reporter import SocketDataReporter

# from rlbot.utils.game_state_util import CarState, Physics, Vector3, GameState
from rlbot.utils.logging import get_logger


class ValidPacketDetector:
    def __init__(self, expected_match_config: MatchSettings):
        self.match_config = expected_match_config
        self.expected_count = self.match_config.PlayerConfigurationsLength()
        self.socket_reporter = SocketDataReporter()
        self.logger = get_logger("vpd")

    def __del__(self):
        self.socket_reporter.disconnect()

    def wait_until_valid_packet(self):
        self.logger.info("Waiting for valid packet...")
        for _ in range(0, 300):
            packet = self.socket_reporter.latest_packet
            if packet is not None and not packet.GameInfo().IsMatchEnded():
                spawn_ids = set()
                for k in range(0, self.expected_count):
                    player_config = self.match_config.PlayerConfigurations(k)
                    if (
                        player_config.VarietyType() == PlayerClass.RLBotPlayer
                        and player_config.SpawnId() > 0
                    ):
                        spawn_ids.add(player_config.SpawnId())

                for n in range(0, packet.PlayersLength()):
                    try:
                        spawn_ids.remove(packet.Players(n).SpawnId())
                    except KeyError:
                        pass

                if (
                    len(spawn_ids) == 0
                    and self.expected_count <= packet.PlayersLength()
                ):
                    self.logger.info(
                        "Packets are looking good, all spawn ids accounted for!"
                    )
                    return
                # elif i > 4:
                #     car_states = {}
                #     for k in range(0, packet.PlayersLength()):
                #         player_info = packet.Players(k)
                #         if player_info.SpawnId() > 0:
                #             car_states[k] = CarState(physics=Physics(velocity=Vector3(z=500)))
                #     if len(car_states) > 0:
                #         self.logger.info("Scooting bots out of the way to allow more to spawn!")
                #         self.socket_reporter.socket_relay.send_game_state(GameState(cars=car_states))
            time.sleep(0.1)
        self.logger.info("Gave up waiting for valid packet :(")


def wait_until_valid_packet(match_settings: MatchSettings):
    detector = ValidPacketDetector(match_settings)
    detector.wait_until_valid_packet()
