import tkinter as tk
import random

# Static variables for the rectangle dimensions as requested
LED_PER_M = 60
WIDTH = 8*LED_PER_M
LENGTH = 4*LED_PER_M
STRIP_SIZE = 2 * (WIDTH + LENGTH - 2)

print(f"Length: {LENGTH}, Width: {WIDTH}, Strip Size: {STRIP_SIZE}")

def generate_pattern():
    """
    Placeholder function to generate a list of RGB values.
    Returns:
        List of tuples (R, G, B) starting from top-left, moving clockwise.
    """
    return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(STRIP_SIZE)]

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
        
        self.square_coords = self.get_clockwise_coordinates()

        self.rects = []
        self.draw_grid()
        
        self.root.bind("<Return>", self.on_enter)     # Main enter key
        self.root.bind("<KP_Enter>", self.on_enter)   # Numpad enter key just in case
        self.root.bind("<Escape>", self.on_escape)    # Escape to close
        
        self.is_processing = False
        
        self.update_canvas()

    def calculate_square_size(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        max_w = screen_w * 0.95
        max_h = screen_h * 0.95
        padding = min(max_h, max_w) * 0.05
        
        square_w = int((max_w - padding) // WIDTH)
        square_h = int((max_h - padding) // LENGTH)
        
        self.square_size = max(1, min(square_w, square_h))

    def get_clockwise_coordinates(self):
        coords = []
        
        for x in range(WIDTH):
            coords.append((x, 0))

        for y in range(1, LENGTH - 1):
            coords.append((WIDTH - 1, y))
            
        for x in range(WIDTH - 1, -1, -1):
            coords.append((x, LENGTH - 1))
            
        for y in range(LENGTH - 2, 0, -1):
            coords.append((0, y))
        print(f"strip length = {len(coords)} -> ")
        return coords

    def draw_grid(self):
        """Builds out the canvas rectangles corresponding exclusively to the perimeter"""
        for grid_x, grid_y in self.square_coords:
            x1 = grid_x * self.square_size
            y1 = grid_y * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black", width=0)
            self.rects.append(rect)

    def rgb_to_hex(self, rgb):
        r = max(0, min(255, rgb[0]))
        g = max(0, min(255, rgb[1]))
        b = max(0, min(255, rgb[2]))
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_canvas(self):
        rgb_list = generate_pattern()
        
        for i, rgb in enumerate(rgb_list):
            if i < len(self.rects):
                hex_color = self.rgb_to_hex(rgb)
                self.canvas.itemconfig(self.rects[i], fill=hex_color)

    def on_enter(self, event):
        """
        Triggered when Enter is pressed.
        Ensures cycle processing and blocks subsequent events until fully rendered.
        """
        if self.is_processing:
            return
            
        self.is_processing = True
        
        self.update_canvas()
        
        self.canvas.update_idletasks()
        
        self.root.after(35, self.unlock_processing)
        
    def unlock_processing(self):
        self.is_processing = False

    def on_escape(self, event):
        self.root.destroy()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = LEDVisualizer(app_root)
    app_root.mainloop()
