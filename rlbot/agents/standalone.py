from rlbot.agents import Controller
from rlbot.agents.runnable import Runnable
from rlbot.flat.GameTickPacket import GameTickPacketT
from rlbot.utils.logging import get_logger


class StandaloneBot(Runnable):
    def __init__(self, name, team, index):
        super().__init__(name)
        self.team = team
        self.index = index
        self.logger = get_logger(f"bot{index}")

    def get_output(self, game_tick_packet: GameTickPacketT) -> Controller:
        """
        Where all the logic of your bot gets its input and returns its output.
        """
        return Controller()
