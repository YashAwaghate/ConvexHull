import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import base64
import io
from PIL import Image

def brute_main(data):
    class Point:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

    class ConvexHullBruteForce:
        def __init__(self, points: list[Point]):
            self.points = points
            self.hull = []
            self.intermediate_steps = []
            self.finalized_edges = []  # To store edges of the finalized hull

        def on_one_side(self, p1: Point, p2: Point, points: list[Point]) -> bool:
            pos = 0
            neg = 0
            for point in points:
                val = (point.y - p1.y) * (p2.x - p1.x) - (point.x - p1.x) * (p2.y - p1.y)
                if val > 0:
                    pos += 1
                elif val < 0:
                    neg += 1
                if pos > 0 and neg > 0:
                    return False
            return True

        def compute_convex_hull(self) -> None:
            n = len(self.points)
            if n < 3:
                print("Not enough points to form a convex hull.")
                return

            for i in range(n):
                for j in range(i + 1, n):
                    p1 = self.points[i]
                    p2 = self.points[j]
                    self.intermediate_steps.append((p1, p2))

                    if self.on_one_side(p1, p2, [self.points[k] for k in range(n) if k != i and k != j]):
                        if p1 not in self.hull:
                            self.hull.append(p1)
                        if p2 not in self.hull:
                            self.hull.append(p2)
                        self.finalized_edges.append((p1, p2))  # Add edge to finalized edges

        def get_angle(self, p1: Point, p2: Point) -> float:
            return math.atan2(p2.y - p1.y, p2.x - p1.x)

        def sort_hull_counterclockwise(self) -> None:
            reference_point = min(self.hull, key=lambda p: (p.y, p.x))
            self.hull.sort(key=lambda p: self.get_angle(reference_point, p))

        def print_hull(self) -> None:
            self.sort_hull_counterclockwise()
            print(f"Number of points in the hull: {len(self.hull)}")
            for point in self.hull:
                print(f"({point.x}, {point.y})")

        def animate(self, frame):
            # Show all points as a scatter plot
            scatter.set_offsets([(p.x, p.y) for p in self.points])

            # Grey dotted line for intermediate steps
            if frame < len(self.intermediate_steps):
                p1, p2 = self.intermediate_steps[frame]
                check_line.set_data([p1.x, p2.x], [p1.y, p2.y])
                check_line.set_linestyle('--')  # Dotted line
                check_line.set_color('grey')  # Grey color
            else:
                # Clear the grey dotted line after intermediate steps are completed
                check_line.set_data([], [])

            # Finalized red hull: Draw once after all intermediate steps are done
            if frame == 0:  # Set up the final hull on the first frame
                self.sort_hull_counterclockwise()
                hull_xs = [p.x for p in self.hull] + [self.hull[0].x]
                hull_ys = [p.y for p in self.hull] + [self.hull[0].y]
                hull_lines.set_data(hull_xs, hull_ys)
                hull_vertices.set_data(hull_xs, hull_ys)

            return scatter, check_line, hull_lines, hull_vertices

    # Extract points or generate random points
    points_from_file = data.get("payload", [])
    num_points = int(data.get("numPoints", 10))  # Default to 10 random points if not provided

    if points_from_file == [[0]]:
        print(f"Received [[0]]. Generating {num_points} random points.")
        fixed_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]
    elif points_from_file:
        fixed_points = [Point(x, y) for x, y in points_from_file]
        print(f"Using {len(fixed_points)} points from input data.")
    else:
        print(f"Input data is empty. Generating {num_points} random points.")
        fixed_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]

    # Create the figure and axis for the animation
    fig, ax = plt.subplots()
    # Calculate dynamic limits based on the points
    x_values = [p.x for p in fixed_points]
    y_values = [p.y for p in fixed_points]
    x_min, x_max = min(x_values) - 10, max(x_values) + 10
    y_min, y_max = min(y_values) - 10, max(y_values) + 10

    # Set dynamic limits for the plot
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Scatter plot for all points
    scatter = ax.scatter([], [], color='blue')

    # Line for checking pairs
    check_line, = ax.plot([], [], 'g-', lw=1)

    # Line and points for the hull
    hull_lines, = ax.plot([], [], 'r-', lw=2)  # Red line for finalized edges
    hull_vertices, = ax.plot([], [], 'ro')     # Red points for hull vertices

    convex_hull = ConvexHullBruteForce(fixed_points)

    # Compute the convex hull before animation
    convex_hull.compute_convex_hull()

    # Create the animation
    anim = FuncAnimation(fig, convex_hull.animate, frames=len(convex_hull.intermediate_steps) + len(convex_hull.finalized_edges), interval=500, repeat=False)
    plt.title("Convex Hull Construction with Brute Force (Fixed or Random Points)")
    plt.xlabel("X")
    plt.ylabel("Y")

    buf = io.BytesIO()
    frames = []

    for i in range(anim.save_count):
        anim._draw_frame(i)
        fig.canvas.draw()
        img = Image.frombytes(
            'RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
        )
        frames.append(img)

    frames[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=200 
    )
    buf.seek(0)
    base64_image = base64.b64encode(buf.read()).decode('ascii')
    buf.close()
    print("Output File Saved")
    return base64_image
