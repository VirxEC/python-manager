import math

from rlbot.agents.standalone import Controller, StandaloneBot
from rlbot.flat.GameStateType import GameStateType
from rlbot.flat.GameTickPacket import GameTickPacketT


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Vector2(self.x - val.x, self.y - val.y)

    def correction_to(self, ideal):
        # The in-game axes are left handed, so use -x
        current_in_radians = math.atan2(self.y, -self.x)
        ideal_in_radians = math.atan2(ideal.y, -ideal.x)

        correction = ideal_in_radians - current_in_radians

        # Make sure we go the 'short way'
        if abs(correction) > math.pi:
            if correction < 0:
                correction += 2 * math.pi
            else:
                correction -= 2 * math.pi

        return correction


def get_car_facing_vector(car):
    pitch = float(car.physics.rotation.pitch)
    yaw = float(car.physics.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)


class Atba(StandaloneBot):
    def initialize_agent(self):
        self.logger.info("Initializing agent!")
        self.controller = Controller()
        num_boost_pads = len(self.get_field_info().boostPads)
        self.logger.info(f"There are {num_boost_pads} boost pads on the field.")

    def get_output(self, game_tick_packet: GameTickPacketT) -> Controller:
        if game_tick_packet.gameInfo.gameStateType not in { GameStateType.Active, GameStateType.Kickoff }:
            return self.controller

        ball_location = Vector2(
            game_tick_packet.ball.physics.location.x,
            game_tick_packet.ball.physics.location.y,
        )

        my_car = game_tick_packet.players[self.index]
        car_location = Vector2(my_car.physics.location.x, my_car.physics.location.y)
        car_direction = get_car_facing_vector(my_car)
        car_to_ball = ball_location - car_location

        steer_correction_radians = car_direction.correction_to(car_to_ball)

        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
        else:
            turn = 1.0

        self.controller.steer = turn
        self.controller.throttle = 1

        return self.controller


if __name__ == "__main__":
    from rlbot.runners.python_bot import run_bot

    run_bot(Atba)
