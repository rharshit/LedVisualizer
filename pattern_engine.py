from utils import random_color


class PatternEngine:
    def __init__(self, room_length, room_width, density, frequency):
        self.length = room_length * density
        self.width = room_width * density
        self.density = density
        self.frequency = frequency

        print(f"PatternEngine initialized for room {room_length}m x {room_width}m with density {density} LEDs/m, running at {frequency}Hz")
        print(f"Calculated strip size: {self._get_strip_size()} LEDs, which is {self._get_strip_size_m():.2f} meters")
        print(f"Minimum points: {self._get_min_points()}, Maximum points: {self._get_max_points()}")

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
        return [random_color() for _ in range(self._get_strip_size())]