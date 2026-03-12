import random

from color import Color
from constants import INDEX_STEP_FACTOR, ROOM_LENGTH, ROOM_WIDTH, LED_PER_M, UPDATES_PER_SECOND, MIN_SEC, MAX_SEC
from utils import random_color, is_debugger_active


class Point:
    def __init__(self, index: int, color: Color):
        self.index = index
        self.color = color
        self.target_index = index
        self.target_color = random_color()
        self.weight = 1.0

    def __str__(self):
        return f"{self.color.to_hex()} -> {self.index}"

    def move(self, index):
        self.target_index = index

    def set_target_index(self, target_index):
        self.target_index = target_index

    def set_target_color(self, target_color):
        self.target_color = target_color

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

        r_step = int(((self.target_color.r - self.color.r) * INDEX_STEP_FACTOR) / factor)
        g_step = int(((self.target_color.g - self.color.g) * INDEX_STEP_FACTOR) / factor)
        b_step = int(((self.target_color.b - self.color.b) * INDEX_STEP_FACTOR) / factor)
        self.color = Color(self.color.r + r_step, self.color.g + g_step, self.color.b + b_step)


class PatternEngine:
    def __init__(self):
        self.next_randomness = 0
        self.points: list[Point] = []
        self._initialize()
        print(f"PatternEngine initialized for room {ROOM_LENGTH}m x {ROOM_WIDTH}m"
              f" with density {LED_PER_M} LEDs/m, running at {UPDATES_PER_SECOND}Hz")
        print(f"Calculated strip size: {get_strip_size()} LEDs, which is {get_strip_size_m():.2f} meters")
        print(f"Minimum points: {get_min_points()}, Maximum points: {get_max_points()}")

    def _initialize(self):
        num_points = random.randint(get_min_points(), get_max_points())
        points: list[Point] = []
        for i in range(num_points):
            point = Point(generate_random_index(i, num_points), random_color())
            point.move(generate_random_index(i, num_points))
            points.append(point)
        self.points = points

    def _get_current_points(self) -> dict[int, Color]:
        return {p.index: p.color for p in self.points}

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
        current_points: dict[int, Color] = self._get_current_points() if is_debugger_active() else {}
        pattern = []
        for i in range(get_strip_size()):
            if is_debugger_active():
                if i in current_points:
                    pattern.append(current_points[i])
                else:
                    pattern.append(Color(0, 0, 0))
            else:
                color = self._get_spread_color(i)
                pattern.append(color)
        return pattern

    def _get_spread_color(self, i):
        r, g, b = 0, 0, 0
        total_distance_normalization = 0
        for point in self.points:
            distance = get_distance(i, point, get_strip_size())
            if distance == 0:
                return point.color
            distance_normalization = 1 / (distance - 1) if distance > 1 else 1
            r += point.color.r * point.weight * distance_normalization
            g += point.color.g * point.weight * distance_normalization
            b += point.color.b * point.weight * distance_normalization
            total_distance_normalization += distance_normalization
        r = int(r / total_distance_normalization)
        g = int(g / total_distance_normalization)
        b = int(b / total_distance_normalization)
        return Color(r, g, b)


    def _take_step(self):
        to_remove = [point for point in self.points if point.weight == 0]
        if to_remove:
            for point in to_remove:
                self.points.remove(point)
        if self.next_randomness <= 0:
            self._add_randomness()
        for point in self.points:
            point.step(UPDATES_PER_SECOND, max_index=get_strip_size())
        self.next_randomness -= 1

    def _get_random_event(self):
        def event_key(difference):
            if difference < 0:
                return -1
            elif difference > 0:
                return 1
            else:
                return 0

        num_points = len(self.points)
        event_probability = [event_key(possibility - num_points) for possibility in
                             range(get_min_points(), get_max_points() + 1)] + [0] * (
                                        get_max_points() - get_min_points() + 1)
        return random.choice(event_probability)

    def _add_randomness(self):
        event = self._get_random_event()
        self._process_event(event)
        self.next_randomness = random.randint(0, UPDATES_PER_SECOND * 2)

    def _process_event(self, event):
        if event == 1:
            self._add_random_point()
        elif event == -1:
            self._remove_random_point()
        else:
            self._change_random_point()

    def _add_random_point(self):
        print("  .")

    def _remove_random_point(self):
        print(".  ")

    def _change_random_point(self):
        print(" . ")


def get_distance(index1: int | Point, index2: int | Point, max_index):
    if isinstance(index1, Point):
        index1 = index1.index
    if isinstance(index2, Point):
        index2 = index2.index
    direct_distance = abs(index1 - index2)
    wrapped_distance = max_index - direct_distance
    return min(direct_distance, wrapped_distance)


def get_strip_size():
    return 2 * (ROOM_WIDTH * LED_PER_M + ROOM_LENGTH * LED_PER_M - 2)


def get_strip_size_m():
    return get_strip_size() / LED_PER_M


def get_min_points():
    return int(get_strip_size_m() // 4)


def get_max_points():
    return int(get_strip_size_m() // 3)


def get_margin(num_points):
    return get_strip_size() // num_points // 2


def generate_random_index(i, num_points):
    index = i * get_strip_size() // num_points
    margin = get_margin(num_points)
    return (index + random.randint(-margin, margin)) % get_strip_size()


def generate_random_step_count():
    return random.randint(UPDATES_PER_SECOND * MIN_SEC, UPDATES_PER_SECOND * MAX_SEC)
