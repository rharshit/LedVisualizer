import random

from color import Color
from utils import random_color


class Point:
    def __init__(self, index, color: Color):
        self.index = index
        self.color = color

    def __str__(self):
        return f"{self.color.to_hex()} -> {self.index}"


class PointState:
    def __init__(self, c_point: Point, t_point: Point = None):
        self.c_point = c_point
        self.t_point = t_point if t_point else c_point

class PatternEngine:
    def __init__(self, room_length, room_width, density, frequency):
        self.length = room_length * density
        self.width = room_width * density
        self.density = density
        self.frequency = frequency
        self.point_states: list[PointState] = []

        self._initialize()

        print(f"PatternEngine initialized for room {room_length}m x {room_width}m with density {density} LEDs/m, running at {frequency}Hz")
        print(f"Calculated strip size: {self._get_strip_size()} LEDs, which is {self._get_strip_size_m():.2f} meters")
        print(f"Minimum points: {self._get_min_points()}, Maximum points: {self._get_max_points()}")

    def _initialize(self):
        num_points = random.randint(self._get_min_points(), self._get_max_points())
        point_states = []
        for i in range(num_points):
            index = i * self._get_strip_size() // num_points
            point_states.append(PointState(Point(index, random_color()), Point(index, random_color())))
        self.point_states = point_states

    def _get_current_points(self) -> list[Point]:
        return [p.c_point for p in self.point_states]

    def _get_strip_size(self):
        return 2 * (self.width + self.length - 2)

    def _get_strip_size_m(self):
        return self._get_strip_size() / self.density

    def _get_min_points(self):
        return int(self._get_strip_size_m() // 4)

    def _get_max_points(self):
        return int(self._get_strip_size_m() // 2)

    def get_next_pattern(self):
        """
        Generates the list of values that will be used to update the canvas rectangles to show a pattern.
        Returns:
            List of tuples (R, G, B) starting from top-left, moving clockwise.
        """
        pattern = self._generate_pattern()
        return pattern

    def _generate_pattern(self):
        return [Color(0, 0, 0) if i not in [point.index for point in self._get_current_points()] else next(
            point.color for point in self._get_current_points() if point.index == i) for i in
                range(self._get_strip_size())]
