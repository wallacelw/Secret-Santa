import tkinter as tk
from random import Random
import math
import time
from shuffle import generate

class SpinningWheel:
    def __init__(self, master, mapped):
        self.master = master
        master.title("Secret Santa da Huawei")

        # Define colors and names
        self.colors = ["red", "green", "white"]
        self.names = list(mapped)

        # Create canvas
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        # Create wheel
        self.radius = 200
        self.angle = 0
        self.wheel_segments = []
        self.create_wheel()

        # Start button
        self.start_btn = tk.Button(master, text="Spin", command=self.spin)
        self.start_btn.pack()

        # Result label
        self.result_label = tk.Label(master, text="", font=("Arial", 24))
        self.result_label.pack()

    def create_wheel(self):
        # Create segments of the wheel
        segment_angle = 360 / len(self.names)
        for i, name in enumerate(self.names):
            start_angle = math.radians(i * segment_angle)
            end_angle = math.radians((i + 1) * segment_angle)
            x0 = 200 + self.radius * math.cos(start_angle)
            y0 = 200 + self.radius * math.sin(start_angle)
            x1 = 200 + self.radius * math.cos(end_angle)
            y1 = 200 + self.radius * math.sin(end_angle)
            segment = self.canvas.create_polygon(200, 200, x0, y0, x1, y1,
                                                 fill=self.colors[i % len(self.colors)])
            self.wheel_segments.append(segment)
            # Place names in the center of the segments
            self.place_name(name, (start_angle, end_angle))

    def place_name(self, name, angles):
        # Calculate the position to place the name
        mid_angle = (angles[0] + angles[1]) / 2
        x = 200 + (self.radius / 2) * math.cos(mid_angle)
        y = 200 + (self.radius / 2) * math.sin(mid_angle)
        self.canvas.create_text(x, y, text=name, font=("Arial", 12), fill="black")

    def spin(self):
        # self.angle = random.randint(720, 1440)  # Random spin between 2 and 4 full rotations
        self.angle = 1440
        self.animate_spin()

    def animate_spin(self):
        for _ in range(360):  # Number of frames for the spin animation
            self.master.update()  # Refresh the Tkinter window
            self.angle -= 12  # Reduce the angle for each frame
            self.canvas.delete("all")  # Clear the canvas
            self.draw_wheel()  # Redraw the wheel at the new angle
            time.sleep(0.01)  # Delay for animation effect

        # Show the result after the spin completes
        self.show_result()

    def draw_wheel(self):
        # Draw the wheel segments with the current angle
        segment_angle = 360 / len(self.names)
        for i, name in enumerate(self.names):
            start_angle = math.radians(i * segment_angle + self.angle)
            end_angle = math.radians((i + 1) * segment_angle + self.angle)
            x0 = 200 + self.radius * math.cos(start_angle)
            y0 = 200 + self.radius * math.sin(start_angle)
            x1 = 200 + self.radius * math.cos(end_angle)
            y1 = 200 + self.radius * math.sin(end_angle)
            self.canvas.create_polygon(200, 200, x0, y0, x1, y1,
                                        fill=self.colors[i % len(self.colors)])
            # Place names in the center of the segments
            self.place_name(name, (start_angle, end_angle))

    def show_result(self):
        # Determine the result after spinning
        final_angle = self.angle % 360
        segment_angle = 360 / len(self.names)
        selected_index = int((final_angle / segment_angle) % len(self.names))
        selected_name = self.names[selected_index]
        self.result_label.config(text=selected_name)

if __name__ == "__main__":
    root = tk.Tk()
    seed, mapped = generate()
    app = SpinningWheel(master=root, mapped=mapped)
    root.mainloop()