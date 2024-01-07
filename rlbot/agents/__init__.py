from rlbot.flat.ControllerState import ControllerStateT


class Controller(ControllerStateT):
    """
    Building flatbuffer objects is verbose and error prone. This class provides a friendlier
    interface to bot makers.
    """

    def __init__(
        self,
        steer: float = 0.0,
        throttle: float = 0.0,
        pitch: float = 0.0,
        yaw: float = 0.0,
        roll: float = 0.0,
        jump: bool = False,
        boost: bool = False,
        handbrake: bool = False,
        useItem: bool = False,
    ):
        """
        :param steer:    Range: -1 .. 1, negative=left, positive=right
        :param throttle: Range: -1 .. 1, negative=backward, positive=forward
        :param pitch:    Range: -1 .. 1, negative=nose-down, positive=nose-up
        :param yaw:      Range: -1 .. 1, negative=nose-left, positive=nose-right
        :param roll:     Range: -1 .. 1, negative=anticlockwise, positive=clockwise  (when looking forwards along the car)
        :param jump: Analogous to the jump button in game.
        :param boost: Analogous to the boost button in game.
        :param handbrake: Analogous to the handbrake button in game.
        :param useItem: Analogous to the use item button (from rumble) in game.
        """
        self.steer = steer
        self.throttle = throttle
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.jump = jump
        self.boost = boost
        self.handbrake = handbrake
        self.useItem = useItem
