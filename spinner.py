import tkinter as tk
from shuffle import generate
import math, time, sys, random
from PIL import ImageTk

class SpinningWheel:
    def __init__(self, master, mapped):

        # Create TK object
        self.master = master
        self.master.title("Secret Santa")
        self.master.resizable(False, False)

        # Background color 
        self.background_color = "#f2e8cf"

        # Create canvas
        self.size = 800
        self.center = self.size/2
        self.canvas = tk.Canvas(master, width=self.size, height=self.size, bg=self.background_color)
        self.canvas.pack()

        # Save the member assignment 
        self.mapped = mapped
        
        # Define wheel colors and names of the members
        self.outline_color = "#cffcff"
        self.arrow_color = "#43291f"
        self.colors = ["#003e1f", "#d90429"]
        self.names = list(mapped)
        random.shuffle(self.names)

        # Compute polygon angle size and the rotation angle so the top aligns with the first element
        self.segment_angle = 360 / len(self.names)
        self.rotate_angle = math.radians(360/4 + self.segment_angle/2)

        # Create initial wheel
        self.radius = 3/8 * self.size
        self.angle = 0
        self.draw_wheel()

        # Result label
        self.result_label = tk.Label(master, text="", font=("Arial", 24, "bold"))
        self.result_label.pack()
        self.result_label.config(bg=self.background_color)
        self.result_label.place(x = 3/8 * self.size, y=15/16 * self.size)

        # Start button
        self.start_btn = tk.Button(master, text="Spin", command=self.spin)
        self.start_btn.pack()
        self.start_btn.place(x=3/4 * self.size, y=1/16 * self.size)

        # Create Dropdawn list
        self.sorted_names = sorted(self.names)
        self.user = tk.StringVar(self.master)
        self.user.set("Select the user:") # default value
        self.menu = tk.OptionMenu(self.master, self.user, *self.sorted_names)
        self.menu.pack()
        self.menu.place(x=1/8 * self.size, y=1/16 * self.size)

    # Create the arrow pointing downwards
    def draw_arrow(self):
        self.canvas.create_line(self.center, 0, 
                                self.center, 100, 
                                arrow=tk.LAST,
                                arrowshape=(20, 30, 30),
                                fill=self.arrow_color,
                                width=10,
                                )
    # draw wheel
    def draw_wheel(self):
        self.draw_arrow()

        for i, name in enumerate(self.names):
            start_angle = math.radians(i * self.segment_angle + self.angle) - self.rotate_angle
            end_angle = math.radians((i + 1) * self.segment_angle + self.angle) - self.rotate_angle

            x0 = self.center + self.radius * math.cos(start_angle)
            y0 = self.center + self.radius * math.sin(start_angle)
            x1 = self.center + self.radius * math.cos(end_angle)
            y1 = self.center + self.radius * math.sin(end_angle)

            self.canvas.create_polygon(
                self.center, 
                self.center, 
                x0, y0, x1, y1,
                fill=self.colors[i % len(self.colors)],
                outline=self.outline_color,
                width=4,)

            # Place names in the center of the segments
            self.place_name(name, (start_angle, end_angle))

    # place the name inside the triangle polygon
    def place_name(self, name, angles):
        # place name at the center of the polygon segment
        mid_angle = (angles[0] + angles[1]) / 2
        x = self.center + (self.radius / 2) * math.cos(mid_angle)
        y = self.center + (self.radius / 2) * math.sin(mid_angle)
        self.canvas.create_text(x, y, text=name, font=("Arial", 12, "bold"), fill="black")

    # spin the wheel and print the result
    def spin(self):
        self.result_label.config(text="")

        if (self.user.get() in self.mapped):
            self.animate_spin()
            self.result_label.config(text=mapped[self.user.get()])

        else:
            self.result_label.config(text="Error: Select an User !!")

    # create the spin animation, ending exactly where the result should be
    def animate_spin(self):
        self.angle = 0

        # find the position of the result label
        expected = mapped[ self.user.get() ]
        idx = self.names.index(expected)

        # define the spinning speed
        self.speed = 6
        
        # 6 loops (the last one is shorter)
        loops = 6
        reps = int((loops*360 - (idx * self.segment_angle))/self.speed)

        for _ in range(reps):  # Number of frames for the spin animation
            self.master.update()  # Refresh the Tkinter window
            self.angle += self.speed  # Each frame, the angle is increased
            self.canvas.delete("all")  # Clear the canvas
            self.draw_wheel()  # Redraw the wheel at the new angle
            time.sleep(0.01)  # Delay for animation effect


if __name__ == "__main__":
    root = tk.Tk()
    seed, mapped = generate( int(sys.argv[1]) )
    app = SpinningWheel(master=root, mapped=mapped)
    root.mainloop()