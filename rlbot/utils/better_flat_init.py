from rlbot.flat.Rotator import RotatorT
from rlbot.flat.Vector3 import Vector3T


class Vector3(Vector3T):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z


class Rotator(RotatorT):
    def __init__(self, pitch: float = 0, yaw: float = 0, roll: float = 0):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
