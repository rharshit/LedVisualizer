import tkinter as tk
import random

# Static variables for the rectangle dimensions as requested
WIDTH = 50
LENGTH = 20

def generate_pattern(num_squares):
    """
    Placeholder function to generate a list of RGB values.
    Returns:
        List of tuples (R, G, B) starting from top-left, moving clockwise.
    """
    # Simply returning random RGB colors as a demonstration
    return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_squares)]

class LEDVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Rectangle Visualizer")
        self.root.configure(bg="#1b1b1b") # Dark background for the app window
        
        # 1. Determine safe square size based on the laptop's screen limits
        self.calculate_square_size()
        
        canvas_width = WIDTH * self.square_size
        canvas_height = LENGTH * self.square_size
        
        # We wrap the canvas in a frame to simulate the blue bounding box from the wireframe
        frame = tk.Frame(root, padx=2, pady=2)
        frame.pack(padx=30, pady=30)
        
        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
        self.canvas.pack()
        
        # 2. Derive coords spanning the perimeter clockwise
        self.square_coords = self.get_clockwise_coordinates()
        self.num_squares = len(self.square_coords)
        
        self.rects = []
        self.draw_grid()
        
        # 3. Bind Keyboard Events
        self.root.bind("<Return>", self.on_enter)     # Main enter key
        self.root.bind("<KP_Enter>", self.on_enter)   # Numpad enter key just in case
        self.root.bind("<Escape>", self.on_escape)    # Escape to close
        
        # Used to enforce that the key press is registered strictly after generation & render cycle
        self.is_processing = False
        
        # Generate initial pattern automatically
        self.update_canvas()

    def calculate_square_size(self):
        # Obtain user display characteristics dynamically
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        # Constrain canvas to roughly 85% of screen size to assure it won't overflow
        max_w = screen_w * 0.85
        max_h = screen_h * 0.85
        padding = min(max_h, max_w) * 0.1
        
        square_w = int((max_w - padding) // WIDTH)
        square_h = int((max_h - padding) // LENGTH)
        
        # Enforce uniform height & width for our tiny components
        self.square_size = max(1, min(square_w, square_h))

    def get_clockwise_coordinates(self):
        coords = []
        
        # 1. Top edge: moving left to right
        for x in range(WIDTH):
            coords.append((x, 0))
            
        # 2. Right edge: moving top to bottom 
        # (Skip corners, as they were handled by horizontal sweeps)
        for y in range(1, LENGTH - 1):
            coords.append((WIDTH - 1, y))
            
        # 3. Bottom edge: moving right to left
        for x in range(WIDTH - 1, -1, -1):
            coords.append((x, LENGTH - 1))
            
        # 4. Left edge: moving bottom to top
        for y in range(LENGTH - 2, 0, -1):
            coords.append((0, y))
            
        return coords

    def draw_grid(self):
        """Builds out the canvas rectangles corresponding exclusively to the perimeter"""
        for grid_x, grid_y in self.square_coords:
            x1 = grid_x * self.square_size
            y1 = grid_y * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            
            # Using an orange outline, which maps to typical wireframe layouts for LED visualizations
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="#ff6600", fill="black", width=1)
            self.rects.append(rect)

    def rgb_to_hex(self, rgb):
        # Guard clamps to prevent malformed color exceptions
        r = max(0, min(255, rgb[0]))
        g = max(0, min(255, rgb[1]))
        b = max(0, min(255, rgb[2]))
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_canvas(self):
        # Fetch the colors via the placeholder logic
        rgb_list = generate_pattern(self.num_squares)
        
        for i, rgb in enumerate(rgb_list):
            if i < len(self.rects):
                hex_color = self.rgb_to_hex(rgb)
                self.canvas.itemconfig(self.rects[i], fill=hex_color)

    def on_enter(self, event):
        """
        Triggered when Enter is pressed.
        Ensures cycle processing and blocks subsequent events until fully rendered.
        """
        # "key press should only be registered once the generate_pattern function is completed and the new canvas is rendered."
        if self.is_processing:
            return
            
        self.is_processing = True
        
        # Generate the properties and hook them onto UI components
        self.update_canvas()
        
        # Synchronously block until the UI is physically rendered on screen
        self.canvas.update_idletasks()
        
        # Free processing allowance shortly after rendering (Yields CPU when holding down Enter, 35ms bounds execution to ~30 FPS visually)
        self.root.after(35, self.unlock_processing)
        
    def unlock_processing(self):
        self.is_processing = False

    def on_escape(self, event):
        self.root.destroy()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = LEDVisualizer(app_root)
    app_root.mainloop()
