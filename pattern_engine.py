import random

from color import Color
from utils import random_color


class Point:
    def __init__(self, index: int, color: Color):
        self.index = index
        self.color = color
        self.target_index = index
        self.target_color = color

    def __str__(self):
        return f"{self.color.to_hex()} -> {self.index}"

    def set_target_index(self, target_index):
        self.target_index = target_index

    def set_target_color(self, target_color):
        self.target_color = target_color

    # TODO: Implement this
    def step(self):
        pass

class PatternEngine:
    def __init__(self, room_length, room_width, density, frequency):
        self.length = room_length * density
        self.width = room_width * density
        self.density = density
        self.frequency = frequency
        self.points: list[Point] = []

        self._initialize()

        print(f"PatternEngine initialized for room {room_length}m x {room_width}m with density {density} LEDs/m, running at {frequency}Hz")
        print(f"Calculated strip size: {self._get_strip_size()} LEDs, which is {self._get_strip_size_m():.2f} meters")
        print(f"Minimum points: {self._get_min_points()}, Maximum points: {self._get_max_points()}")

    def _initialize(self):
        num_points = random.randint(self._get_min_points(), self._get_max_points())
        points: list[Point] = []
        for i in range(num_points):
            index = i * self._get_strip_size() // num_points
            margin = (self._get_strip_size() // num_points) // 5
            point = Point((index + random.randint(-margin, margin)) % self._get_strip_size(), random_color())
            points.append(point)
        self.points = points

    def _get_current_points(self) -> dict[int, Color]:
        return {p.index: p.color for p in self.points}

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
        self._take_step()
        pattern = self._generate_pattern()
        return pattern

    def _generate_pattern(self):
        current_points: dict[int, Color] = self._get_current_points()
        pattern = []
        for i in range(self._get_strip_size()):
            if i in current_points:
                pattern.append(current_points[i])
            else:
                pattern.append(Color(0, 0, 0))
        return pattern

    def _take_step(self):
        for point in self.points:
            point.step()
