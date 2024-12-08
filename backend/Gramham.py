import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import namedtuple
from functools import cmp_to_key
import random
import base64
import io
from PIL import Image

# Define the Graham Scan Convex Hull Algorithm
def graham_main(data):
    Point = namedtuple('Point', 'x y')

    def orientation(p, q, r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or Counterclockwise

    def dist_sq(p1, p2):
        return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

    def next_to_top(S):
        return S[-2]

    def compare(p1, p2):
        o = orientation(p0, p1, p2)
        if o == 0:
            return -1 if dist_sq(p0, p2) >= dist_sq(p0, p1) else 1
        return -1 if o == 2 else 1

    def convex_hull(points):
        n = len(points)
        if n < 3:
            return []

        ymin = points[0].y
        min_idx = 0
        for i in range(1, n):
            y = points[i].y
            if (y < ymin) or (ymin == y and points[i].x < points[min_idx].x):
                ymin = points[i].y
                min_idx = i

        points[0], points[min_idx] = points[min_idx], points[0]
        global p0
        p0 = points[0]

        points = sorted(points, key=cmp_to_key(compare))

        S = [points[0], points[1]]
        steps = [(S.copy(), False)]

        for i in range(2, len(points)):
            while len(S) > 1 and orientation(next_to_top(S), S[-1], points[i]) != 2:
                S.pop()
            S.append(points[i])
            steps.append((S.copy(), True if i == len(points) - 1 else False))

        return S, steps

    # Extract points from the data or generate random points if none provided
    points_from_file = data.get("payload", [])
    num_points = int(data.get("numPoints", 10))  # Default to 10 random points if not provided

    random_points = None
    if points_from_file == [[0]]:
        print(f"Received [[0]]. Generating {num_points} random points.")
        random_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]
    elif points_from_file:
        random_points = [Point(x, y) for x, y in points_from_file]
        print(f"Using {len(random_points)} points from input data.")
    else:
        print(f"Input data is empty. Generating {num_points} random points.")
        random_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]

    # Determine dynamic scale for plotting
    min_x = min(p.x for p in random_points)
    max_x = max(p.x for p in random_points)
    min_y = min(p.y for p in random_points)
    max_y = max(p.y for p in random_points)

    padding = 10  # Add some padding around the points for better visualization
    x_min, x_max = min_x - padding, max_x + padding
    y_min, y_max = min_y - padding, max_y + padding

    hull, steps = convex_hull(random_points)

    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    scatter = ax.scatter([], [], color='blue')
    tentative_line, = ax.plot([], [], 'grey', lw=2)
    finalized_line, = ax.plot([], [], 'r-', lw=2)
    start_marker, = ax.plot([], [], 'yo')
    point_marker, = ax.plot([], [], 'go')

    def animate(frame):
        scatter.set_offsets([(p.x, p.y) for p in random_points])
        start_marker.set_data(p0.x, p0.y)

        if frame < len(steps):
            current_hull, finalized = steps[frame]
            hull_xs = [p.x for p in current_hull]
            hull_ys = [p.y for p in current_hull]

            if finalized:
                finalized_line.set_data(hull_xs + [hull_xs[0]], hull_ys + [hull_ys[0]])
                tentative_line.set_data([], [])
            else:
                tentative_line.set_data(hull_xs, hull_ys)
                finalized_line.set_data([], [])

            point_marker.set_data(current_hull[-1].x, current_hull[-1].y)
        else:
            hull_xs = [p.x for p in hull]
            hull_ys = [p.y for p in hull]
            finalized_line.set_data(hull_xs + [hull_xs[0]], hull_ys + [hull_ys[0]])
            tentative_line.set_data([], [])
            point_marker.set_data([], [])

        return scatter, tentative_line, finalized_line, start_marker, point_marker

    anim = FuncAnimation(fig, animate, frames=len(steps) + 10, interval=500, repeat=False)
    plt.title("Convex Hull Construction with Graham Scan")
    plt.xlabel("X")
    plt.ylabel("Y")

    buf = io.BytesIO()
    frames = []

    for i in range(len(steps) + 10):
        animate(i)
        fig.canvas.draw()
        img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
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
    print("GIF Created and Encoded to Base64")
    return base64_image
