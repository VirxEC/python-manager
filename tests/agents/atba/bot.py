import math

from rlbot.agents.standalone import Controller, StandaloneBot
from rlbot.flat.GameStateType import GameStateType
from rlbot.flat.GameTickPacket import GameTickPacketT
from rlbot.flat.TextHAlign import TextHAlign
from rlbot.flat.Vector3 import Vector3T
from rlbot.game_manager.rendering import RenderMessage
from rlbot.utils import state_set
from rlbot.utils.better_flat_init import Vector3


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    @staticmethod
    def from_vector3t(vec3: Vector3T):
        return Vector2(vec3.x, vec3.y)

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
    state_setting = False
    rendering = False

    def initialize_agent(self):
        self.logger.info("Initializing agent!")
        self.controller = Controller()
        num_boost_pads = len(self.get_field_info().boostPads)
        self.logger.info(f"There are {num_boost_pads} boost pads on the field.")
        self.renderer.begin_rendering("custom one-time rendering group")
        self.renderer.add_render(
            RenderMessage.PolyLine3D(
                [
                    Vector3(1000, 1000, 100),
                    Vector3(1000, -1000, 500),
                    Vector3(-1000, -1000, 1000),
                ],
                RenderMessage.yellow,
            )
        )
        self.renderer.end_rendering()

    def get_output(self, packet: GameTickPacketT) -> Controller:
        if self.rendering:
            self.test_rendering(packet)

        if packet.gameInfo.gameStateType not in {
            GameStateType.Active,
            GameStateType.Kickoff,
        }:
            return self.controller

        if self.state_setting:
            self.test_state_setting(packet.ball.physics.velocity)

        ball_location = Vector2.from_vector3t(packet.ball.physics.location)

        my_car = packet.players[self.index]
        car_location = Vector2.from_vector3t(my_car.physics.location)
        car_direction = get_car_facing_vector(my_car)
        car_to_ball = ball_location - car_location

        steer_correction_radians = car_direction.correction_to(car_to_ball)

        self.controller.steer = -steer_correction_radians
        self.controller.throttle = 1

        return self.controller

    def test_state_setting(self, ball_velocity: Vector3T):
        game_state = state_set.GameState(
            state_set.BallState(
                state_set.Physics(velocity=state_set.Vector3(z=ball_velocity.z + 10))
            )
        )
        self.set_game_state(game_state)

    def test_rendering(self, packet: GameTickPacketT):
        self.renderer.begin_rendering()
        text = "Hello world!\nI hope I'm centered!"
        self.renderer.add_render(
            RenderMessage.String3D(
                packet.players[self.index].physics.location,
                text,
                RenderMessage.yellow,
                1.5,
                horizontal_alignment=TextHAlign.Center,
            )
        )
        self.renderer.end_rendering()


if __name__ == "__main__":
    from rlbot.runners.python_bot import run_bot

    run_bot(Atba)
