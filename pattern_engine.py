import random

from color import Color
from constants import INDEX_STEP_FACTOR, ROOM_LENGTH, ROOM_WIDTH, LED_PER_M, UPDATES_PER_SECOND, MIN_SEC, MAX_SEC
from utils import random_color, is_debugger_active


class Point:
    def __init__(self, index: int, color: Color):
        self.index = index
        self.color = color
        self.target_index = index
        self.target_color = color
        self.weight = 1.0

    def __str__(self):
        return f"{self.color.to_hex()} -> {self.index}"

    def move(self, index):
        self.target_index = index

    def set_target_index(self, target_index):
        self.target_index = target_index

    def set_target_color(self, target_color):
        self.target_color = target_color

    # TODO: Fix animation, add color steps
    def step(self, factor, max_index=0):
        current_index = self.index
        target_index = self.target_index
        if max_index:
            rotated_target = target_index + max_index if target_index < current_index else target_index - max_index
            if abs(rotated_target - current_index) < abs(target_index - current_index):
                target_index = rotated_target
        step = int(((target_index - current_index) * INDEX_STEP_FACTOR) / factor)
        new_index = (current_index + step) % max_index if max_index else current_index + step
        self.index = new_index


class PatternEngine:
    def __init__(self, room_length, room_width, density, frequency):
        self.points: list[Point] = []

        self._initialize()

        print(
            f"PatternEngine initialized for room {ROOM_LENGTH}m x {ROOM_WIDTH}m with density {LED_PER_M} LEDs/m, running at {UPDATES_PER_SECOND}Hz")
        print(f"Calculated strip size: {self._get_strip_size()} LEDs, which is {self._get_strip_size_m():.2f} meters")
        print(f"Minimum points: {self._get_min_points()}, Maximum points: {self._get_max_points()}")

    def _initialize(self):
        num_points = random.randint(self._get_min_points(), self._get_max_points())
        points: list[Point] = []
        for i in range(num_points):
            point = Point(self._generate_random_index(i, num_points), random_color())
            point.move(self._generate_random_index(i, num_points))
            points.append(point)
        self.points = points

    def _get_margin(self, num_points):
        return self._get_strip_size() // num_points // 2

    def _get_current_points(self) -> dict[int, Color]:
        return {p.index: p.color for p in self.points}

    def _get_strip_size(self):
        return 2 * (ROOM_WIDTH * LED_PER_M + ROOM_LENGTH * LED_PER_M - 2)

    def _get_strip_size_m(self):
        return self._get_strip_size() / LED_PER_M

    def _get_min_points(self):
        return int(self._get_strip_size_m() // 4)

    def _get_max_points(self):
        return int(self._get_strip_size_m() // 2)

    def _generate_random_index(self, i, num_points):
        index = i * self._get_strip_size() // num_points
        margin = self._get_margin(num_points)
        return (index + random.randint(-margin, margin)) % self._get_strip_size()

    def _generate_random_step_count(self):
        return random.randint(UPDATES_PER_SECOND * MIN_SEC, UPDATES_PER_SECOND * MAX_SEC)

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
            if is_debugger_active():
                if i in current_points:
                    pattern.append(current_points[i])
                else:
                    pattern.append(Color(0, 0, 0))
            else:
                r, g, b = 0, 0, 0
                total_distance_normalization = 0
                for point in self.points:
                    distance = get_distance(i, point, self._get_strip_size())
                    if distance == 0:
                        pattern.append(point.color)
                        break
                    distance_normalization = 1 / (distance - 1) if distance > 1 else 1
                    r += point.color.r * point.weight * distance_normalization
                    g += point.color.g * point.weight * distance_normalization
                    b += point.color.b * point.weight * distance_normalization
                    total_distance_normalization += distance_normalization
                else:
                    r = int(r / total_distance_normalization)
                    g = int(g / total_distance_normalization)
                    b = int(b / total_distance_normalization)
                    pattern.append(Color(r, g, b))
        return pattern

    def _take_step(self):
        for point in self.points:
            point.step(UPDATES_PER_SECOND, max_index=self._get_strip_size())


def get_distance(index1: int | Point, index2: int | Point, max_index):
    if isinstance(index1, Point):
        index1 = index1.index
    if isinstance(index2, Point):
        index2 = index2.index
    direct_distance = abs(index1 - index2)
    wrapped_distance = max_index - direct_distance
    return min(direct_distance, wrapped_distance)
