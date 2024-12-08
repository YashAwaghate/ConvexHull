import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import namedtuple
import random
import base64
import io
from PIL import Image

def monotone_main(data):
    # Extract numPoints from data, default to 20 if not provided
    num_points = int(data.get('numPoints', 20))

    Point = namedtuple('Point', 'x y')

    def cross_z(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    def monotone_chain(points):
        points = sorted(points, key=lambda p: (p.x, p.y))

        lower = []
        steps = []

        for point in points:
            while len(lower) >= 2 and cross_z(lower[-2], lower[-1], point) <= 0:
                lower.pop()
            lower.append(point)
            steps.append(lower[:])

        upper = []
        for point in reversed(points):
            while len(upper) >= 2 and cross_z(upper[-2], upper[-1], point) <= 0:
                upper.pop()
            upper.append(point)
            steps.append(lower + upper[::-1])

        if lower:
            lower.pop()
        if upper:
            upper.pop()

        return lower + upper, steps

    payload = data.get('payload', [])

    # If no payload points are provided, generate random points
    if not payload or payload == [[0]]:
        points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]
    else:
        points = [Point(x, y) for x, y in payload]

    if not points:
        raise ValueError("No points available to process.")

    convex_hull, steps = monotone_chain(points)

    x_values = [p.x for p in points]
    y_values = [p.y for p in points]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    padding = 10
    x_min, x_max = x_min - padding, x_max + padding
    y_min, y_max = y_min - padding, y_max + padding

    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.scatter(x_values, y_values)
    tentative_line, = ax.plot([], [], 'grey', linestyle='--')  # Tentative lines (grey dashed)
    finalized_line, = ax.plot([], [], 'r-')  # Finalized hull segments (red solid)

    def update(frame):
        if frame < len(steps):
            hull_points = steps[frame]
            xs = [p.x for p in hull_points]
            ys = [p.y for p in hull_points]

            # Tentative lines
            if frame < len(steps) - 1:
                xs_tentative = xs + [hull_points[0].x]
                ys_tentative = ys + [hull_points[0].y]
                tentative_line.set_data(xs_tentative, ys_tentative)
                finalized_line.set_data([], [])
            else:
                # Finalized convex hull
                xs_final = [p.x for p in convex_hull] + [convex_hull[0].x]
                ys_final = [p.y for p in convex_hull] + [convex_hull[0].y]
                finalized_line.set_data(xs_final, ys_final)
                tentative_line.set_data([], [])

        return tentative_line, finalized_line

    ani = animation.FuncAnimation(fig, update, frames=len(steps) + 10, interval=500, repeat=False)

    buf = io.BytesIO()
    frames = []

    for i in range(ani.save_count):
        ani._draw_frame(i)
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
    return base64_image
