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
            self.finalized_edges = []

        def on_one_side(self, p1: Point, p2: Point, points: list[Point]) -> bool:
            pos = 0
            neg = 0
            for point in points:
                val = (point.y - p1.y) * (p2.x - p1.x) - (point.x - p1.x) * (p2.y - p1.y)
                if val > 0:
                    pos += 1
                elif val < 0:
                    neg += 1
            return pos == 0 or neg == 0

        def is_collinear_with_existing(self, point: Point) -> bool:
            for edge in self.finalized_edges:
                p1, p2 = edge
                val = (point.y - p1.y) * (p2.x - p1.x) - (point.x - p1.x) * (p2.y - p1.y)
                if val == 0:  # Collinear
                    return True
            return False

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
                        if p1 not in self.hull or not self.is_collinear_with_existing(p1):
                            self.hull.append(p1)
                        if p2 not in self.hull or not self.is_collinear_with_existing(p2):
                            self.hull.append(p2)
                        self.finalized_edges.append((p1, p2))

            self.sort_hull_counterclockwise()

        def get_angle(self, p1: Point, p2: Point) -> float:
            return math.atan2(p2.y - p1.y, p2.x - p1.x)

        def sort_hull_counterclockwise(self) -> None:
            reference_point = min(self.hull, key=lambda p: (p.y, p.x))
            self.hull.sort(key=lambda p: (
                self.get_angle(reference_point, p),
                math.sqrt((reference_point.x - p.x) ** 2 + (reference_point.y - p.y) ** 2)
            ))

        def print_hull(self) -> None:
            self.sort_hull_counterclockwise()
            print(f"Number of points in the hull: {len(self.hull)}")
            for point in self.hull:
                print(f"({point.x}, {point.y})")

        def animate(self, frame):
            scatter.set_offsets([(p.x, p.y) for p in self.points])

            if frame < len(self.intermediate_steps):
                p1, p2 = self.intermediate_steps[frame]
                check_line.set_data([p1.x, p2.x], [p1.y, p2.y])
                check_line.set_linestyle('--')
                check_line.set_color('grey')
            else:
                check_line.set_data([], [])

            if frame == len(self.intermediate_steps):
                self.sort_hull_counterclockwise()
                hull_xs = [p.x for p in self.hull] + [self.hull[0].x]
                hull_ys = [p.y for p in self.hull] + [self.hull[0].y]
                hull_lines.set_data(hull_xs, hull_ys)
                hull_vertices.set_data(hull_xs, hull_ys)

            return scatter, check_line, hull_lines, hull_vertices

    points_from_file = data.get("payload", [])
    num_points = int(data.get("numPoints", 10))

    if points_from_file == [[0]]:
        print(f"Received [[0]]. Generating {num_points} random points.")
        fixed_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]
    elif points_from_file:
        fixed_points = [Point(x, y) for x, y in points_from_file]
        print(f"Using {len(fixed_points)} points from input data.")
    else:
        print(f"Input data is empty. Generating {num_points} random points.")
        fixed_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]

    fig, ax = plt.subplots()
    x_values = [p.x for p in fixed_points]
    y_values = [p.y for p in fixed_points]
    x_min, x_max = min(x_values) - 10, max(x_values) + 10
    y_min, y_max = min(y_values) - 10, max(y_values) + 10

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    scatter = ax.scatter([], [], color='blue')
    check_line, = ax.plot([], [], 'g-', lw=1)
    hull_lines, = ax.plot([], [], 'r-', lw=2)
    hull_vertices, = ax.plot([], [], 'ro')

    convex_hull = ConvexHullBruteForce(fixed_points)
    convex_hull.compute_convex_hull()

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
