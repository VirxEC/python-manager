import hashlib
from typing import Callable, Optional, Union

from rlbot.flat.Color import ColorT
from rlbot.flat.Line3D import Line3DT
from rlbot.flat.PolyLine3D import PolyLine3DT
from rlbot.flat.RenderGroup import RenderGroupT
from rlbot.flat.RenderMessage import RenderMessageT
from rlbot.flat.RenderType import RenderType
from rlbot.flat.String2D import String2DT
from rlbot.flat.String3D import String3DT
from rlbot.flat.TextHAlign import TextHAlign
from rlbot.flat.TextVAlign import TextVAlign
from rlbot.utils.better_flat_init import Vector3
from rlbot.utils.logging import get_logger


class Color(ColorT):
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @staticmethod
    def team_color(team: int, alt_color: bool = False):
        """
        Returns the team color of the bot. Team 0: blue, team 1: orange, other: white
        :param team: Specify which team's color. If None, the associated bot's team color will be returned.
        :param alt_color: If True, returns the alternate team colors instead. Team 0: cyan, team 1: red, other: gray
        :return: a team color
        """

        if team == 0:
            return RenderMessage.cyan if alt_color else RenderMessage.blue
        elif team == 1:
            return RenderMessage.red if alt_color else RenderMessage.orange
        else:
            return RenderMessage.gray if alt_color else RenderMessage.white


class Line3D(Line3DT):
    def __init__(self, start: Vector3, end: Vector3, color: ColorT):
        self.start = start
        self.end = end
        self.color = color


class PolyLine3D(PolyLine3DT):
    def __init__(self, points: list[Vector3], color: ColorT):
        self.points = points  # type: ignore
        self.color = color


class String2D(String2DT):
    def __init__(
        self,
        x: float,
        y: float,
        text: str,
        color: ColorT,
        scale: float = 1,
        background: ColorT = Color(0, 0, 0, 0),
        horizontal_alignment: int = TextHAlign.Left,
        vertical_alignment: int = TextVAlign.Top,
    ):
        self.x = x
        self.y = y
        self.text = text
        self.foreground = color
        self.scale = scale
        self.background = background
        self.hAlign = horizontal_alignment
        self.vAlign = vertical_alignment


class String3D(String3DT):
    def __init__(
        self,
        position: Vector3,
        text: str,
        color: ColorT,
        scale: float = 1,
        background: ColorT = Color(0, 0, 0, 0),
        horizontal_alignment: int = TextHAlign.Left,
        vertical_alignment: int = TextVAlign.Top,
    ):
        self.position = position
        self.text = text
        self.foreground = color
        self.scale = scale
        self.background = background
        self.hAlign = horizontal_alignment
        self.vAlign = vertical_alignment


class RenderMessage(RenderMessageT):
    transparent = Color(0, 0, 0, 0)
    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    grey = gray = Color(128, 128, 128)
    blue = Color(0, 0, 255)
    red = Color(255, 0, 0)
    green = Color(0, 128, 0)
    lime = Color(0, 255, 0)
    yellow = Color(255, 255, 0)
    orange = Color(225, 128, 0)
    cyan = Color(0, 255, 255)
    pink = Color(255, 0, 255)
    purple = Color(128, 0, 128)
    teal = Color(0, 128, 128)

    def __init__(
        self,
        variety_type: int,
        variety: Union[Line3D, PolyLine3D, String2D, String3D],
    ):
        self.varietyType = variety_type
        self.variety = variety

    @staticmethod
    def Line3D(start: Vector3, end: Vector3, color: Color):
        return RenderMessage(RenderType.Line3D, Line3D(start, end, color))

    @staticmethod
    def PolyLine3D(points: list[Vector3], color: Color):
        return RenderMessage(RenderType.PolyLine3D, PolyLine3D(points, color))

    @staticmethod
    def String2D(
        x: float,
        y: float,
        text: str,
        color: Color,
        scale: float = 1,
        background: ColorT = transparent,
        horizontal_alignment: int = TextHAlign.Left,
        vertical_alignment: int = TextVAlign.Top,
    ):
        return RenderMessage(
            RenderType.String2D,
            String2D(
                x,
                y,
                text,
                color,
                scale,
                background,
                horizontal_alignment,
                vertical_alignment,
            ),
        )

    @staticmethod
    def String3D(
        position: Vector3,
        text: str,
        color: Color,
        scale: float = 1,
        background: ColorT = transparent,
        horizontal_alignment: int = TextHAlign.Left,
        vertical_alignment: int = TextVAlign.Top,
    ):
        return RenderMessage(
            RenderType.String3D,
            String3D(
                position,
                text,
                color,
                scale,
                background,
                horizontal_alignment,
                vertical_alignment,
            ),
        )

    @staticmethod
    def create_color(red: int, green: int, blue: int, alpha: int = 255):
        return Color(red, green, blue, alpha)


class RenderGroup(RenderGroupT):
    def __init__(self, id: int, render_messages: list[RenderMessage]):
        self.id = id
        self.renderMessages = render_messages  # type: ignore


MAX_INT = 2147483647 // 2
DEFAULT_GROUP_ID = "default"


class RenderingManager:
    def __init__(self):
        self.logger = get_logger("Renderer")

        self.used_group_ids: set[int] = set()
        self.group_id: Optional[int] = None

        self.current_renders: list[RenderMessage] = []

        self._render_group: Callable[[RenderGroupT], None] = lambda _: None
        self._remove_render_group: Callable[[int], None] = lambda _: None

    def _add_remove_render_group_func(
        self, remove_render_group_func: Callable[[int], None]
    ):
        self._remove_render_group = remove_render_group_func

    def _add_render_group_func(self, render_group_func: Callable[[RenderGroupT], None]):
        self._render_group = render_group_func

    @staticmethod
    def _get_group_id(group_id: str) -> int:
        return hash(str(group_id).encode("utf-8")) % MAX_INT

    def begin_rendering(self, group_id: str = DEFAULT_GROUP_ID):
        if self.group_id is not None:
            self.logger.error("begin_rendering was called twice without end_rendering!")
            return

        self.group_id = RenderingManager._get_group_id(group_id)
        self.used_group_ids.add(self.group_id)

    def end_rendering(self):
        if self.group_id is None:
            self.logger.error("end_rendering was called without begin_rendering first!")
            return

        self._render_group(RenderGroup(self.group_id, self.current_renders))
        self.current_renders.clear()
        self.group_id = None

    def _clear_render_group(self, group_id: int):
        self._remove_render_group(group_id)

    def clear_render_group(self, group_id: str = DEFAULT_GROUP_ID):
        group_id_hash = RenderingManager._get_group_id(group_id)
        self._clear_render_group(group_id_hash)
        self.used_group_ids.discard(group_id_hash)

    def clear_all_render_groups(self):
        """
        Clears all render groups which have been drawn to using `begin_rendering(group_id)`.
        Note: This does not clear render groups created by e.g. other bots.
        """
        for group_id in self.used_group_ids:
            self._clear_render_group(group_id)
        self.used_group_ids.clear()

    def is_rendering(self):
        return self.group_id is not None

    def add_render(self, render_message: RenderMessage):
        self.current_renders.append(render_message)
