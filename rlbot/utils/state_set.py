from typing import Optional

from rlbot.flat.Bool import BoolT
from rlbot.flat.ConsoleCommand import ConsoleCommandT
from rlbot.flat.DesiredBallState import DesiredBallStateT
from rlbot.flat.DesiredCarState import DesiredCarStateT
from rlbot.flat.DesiredGameInfoState import DesiredGameInfoStateT
from rlbot.flat.DesiredGameState import DesiredGameStateT
from rlbot.flat.DesiredPhysics import DesiredPhysicsT
from rlbot.flat.Float import FloatT
from rlbot.flat.RotatorPartial import RotatorPartialT
from rlbot.flat.Vector3Partial import Vector3PartialT


class Bool(BoolT):
    def __init__(self, val: bool):
        self.val = val


class Float(FloatT):
    def __init__(self, val: float):
        self.val = val


class Rotator(RotatorPartialT):
    def __init__(
        self,
        pitch: Optional[float] = None,
        yaw: Optional[float] = None,
        roll: Optional[float] = None,
    ):
        self.pitch = None if pitch is None else Float(pitch)
        self.yaw = None if yaw is None else Float(yaw)
        self.roll = None if roll is None else Float(roll)


class Vector3(Vector3PartialT):
    def __init__(
        self,
        x: Optional[float] = None,
        y: Optional[float] = None,
        z: Optional[float] = None,
    ):
        self.x = None if x is None else Float(x)
        self.y = None if y is None else Float(y)
        self.z = None if z is None else Float(z)


class Physics(DesiredPhysicsT):
    def __init__(
        self,
        location: Optional[Vector3] = None,
        rotation: Optional[Rotator] = None,
        velocity: Optional[Vector3] = None,
        angular_velocity: Optional[Vector3] = None,
    ):
        self.location = location
        self.rotation = rotation
        self.velocity = velocity
        self.angularVelocity = angular_velocity


class BallState(DesiredBallStateT):
    def __init__(self, physics: Optional[Physics] = None):
        self.physics = physics


class CarState(DesiredCarStateT):
    def __init__(
        self,
        physics: Optional[Physics] = None,
        boost_amount: Optional[float] = None,
    ):
        self.physics = physics
        self.boostAmount = None if boost_amount is None else Float(boost_amount)


class GameInfoState(DesiredGameInfoStateT):
    def __init__(
        self,
        world_gravity_z: Optional[float] = None,
        game_speed: Optional[float] = None,
        paused: Optional[bool] = None,
        end_match: Optional[bool] = None,
    ):
        self.worldGravityZ = None if world_gravity_z is None else Float(world_gravity_z)
        self.gameSpeed = None if game_speed is None else Float(game_speed)
        self.paused = None if paused is None else Bool(paused)
        self.endMatch = None if end_match is None else Bool(end_match)


class ConsoleCommand(ConsoleCommandT):
    def __init__(self, command: str):
        self.command = command


class GameState(DesiredGameStateT):
    def __init__(
        self,
        ball: Optional[BallState] = None,
        cars: list[CarState] = [],
        game_info: Optional[GameInfoState] = None,
        console_commands: list[ConsoleCommand] = [],
    ):
        self.ballState = ball
        self.carStates = cars # type: ignore
        self.gameInfoState = game_info
        self.consoleCommands = console_commands # type: ignore
