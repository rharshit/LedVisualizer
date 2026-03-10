import tkinter as tk
import random

from utils import get_clockwise_coordinates

# Static variables for the rectangle dimensions as requested
LED_PER_M = 60
WIDTH = 8*LED_PER_M
LENGTH = 4*LED_PER_M
STRIP_SIZE = 2 * (WIDTH + LENGTH - 2)
UPDATES_PER_SECOND = 10

print(f"Length: {LENGTH}, Width: {WIDTH}, Strip Size: {STRIP_SIZE}")

class Color:
    def __init__(self, r, g, b):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))

    def to_hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

def random_color():
    return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class LEDVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Rectangle Visualizer")
        self.root.configure(bg="#000000")
        self.square_size = 1
        
        self.calculate_square_size()
        
        canvas_width = WIDTH * self.square_size
        canvas_height = LENGTH * self.square_size

        frame = tk.Frame(root)
        frame.pack(padx=30, pady=30)
        
        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
        self.canvas.pack()
        
        self.square_coords = get_clockwise_coordinates(LENGTH, WIDTH)

        self.rects = []
        self.draw_grid()
        
        self.root.bind("<Escape>", self.on_escape)    # Escape to close
        
        self.update_loop()

    def calculate_square_size(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        max_w = screen_w * 0.95
        max_h = screen_h * 0.95
        padding = min(max_h, max_w) * 0.05
        
        square_w = int((max_w - padding) // WIDTH)
        square_h = int((max_h - padding) // LENGTH)
        
        self.square_size = max(1, min(square_w, square_h))

    def draw_grid(self):
        """Builds out the canvas rectangles corresponding exclusively to the perimeter"""
        for grid_x, grid_y in self.square_coords:
            x1 = grid_x * self.square_size
            y1 = grid_y * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black", width=0)
            self.rects.append(rect)

    def update_canvas(self):
        color_list: list[Color] = self.generate_pattern()
        
        for i, color in enumerate(color_list):
            if i < len(self.rects):
                hex_color = color.to_hex()
                self.canvas.itemconfig(self.rects[i], fill=hex_color)

    def update_loop(self):
        self.update_canvas()
        self.root.after(int(1000 / UPDATES_PER_SECOND), self.update_loop)

    def on_escape(self, event):
        self.root.destroy()

    def generate_pattern(self):
        """
        Placeholder function to generate a list of RGB values.
        Returns:
            List of tuples (R, G, B) starting from top-left, moving clockwise.
        """
        return [random_color() for _ in range(STRIP_SIZE)]

if __name__ == "__main__":
    app_root = tk.Tk()
    app = LEDVisualizer(app_root)
    app_root.mainloop()
