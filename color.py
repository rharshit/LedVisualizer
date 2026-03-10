class Color:
    def __init__(self, r, g, b):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))

    def to_hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"