import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import namedtuple
import random
import base64
import io
from PIL import Image

def monotone_main(data):
    # Define a simple Point class
    print(data)
    Point = namedtuple('Point', 'x y')

    # Function to find the z component of the cross product of three vectors
    def cross_z(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    # The monotone chain algorithm
    def monotone_chain(points):
        # Sort the points lexicographically
        points = sorted(points, key=lambda p: (p.x, p.y))

        lower = []
        steps = []

        # Build the lower hull
        for point in points:
            while len(lower) >= 2 and cross_z(lower[-2], lower[-1], point) <= 0:
                lower.pop()
            lower.append(point)
            steps.append(lower[:])  # Track the steps for animation

        upper = []
        for point in reversed(points):
            while len(upper) >= 2 and cross_z(upper[-2], upper[-1], point) <= 0:
                upper.pop()
            upper.append(point)
            steps.append(
                lower + upper[::-1])  # Track the combined steps for animation

        # Remove the last point of each half to avoid duplication in the final hull
        if lower:
            lower.pop()
        if upper:
            upper.pop()

        # Combine lower and upper hulls to form the final convex hull
        convex_hull = lower + upper
        return convex_hull, steps

    # Check for special case of data payload being [[0]]
    if data['payload'] == [[0]] or data['payload'] == []:
        points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(20)]
    else:
        # Convert the input data into a list of Point objects
        points = [Point(x, y) for x, y in data['payload']]

    if not points:
        raise ValueError("No points available to process.")

    # Compute the convex hull and animation steps
    convex_hull, steps = monotone_chain(points)

    # Determine the scale for the plot based on points
    x_values = [p.x for p in points]
    y_values = [p.y for p in points]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    # Adjust plot limits with some padding
    padding = 10
    x_min, x_max = x_min - padding, x_max + padding
    y_min, y_max = y_min - padding, y_max + padding

    # Create the animation
    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    scat = ax.scatter(x_values, y_values)

    line, = ax.plot([], [], 'r-')  # Line to draw the hull

    def update(frame):
        if frame < len(steps):
            hull_points = steps[frame]
            xs = [p.x for p in hull_points]
            ys = [p.y for p in hull_points]

            # If it's the final frame, close the hull with a continuous boundary
            if frame == len(steps) - 1:
                xs = [p.x for p in convex_hull] + [
                    convex_hull[0].x]  # Connect back to start
                ys = [p.y for p in convex_hull] + [convex_hull[0].y]
            else:
                # For intermediate steps, display the current state of hull construction
                xs = [p.x for p in hull_points] + [hull_points[0].x]
                ys = [p.y for p in hull_points] + [hull_points[0].y]

            line.set_data(xs, ys)

        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(steps) + 10, interval=500, repeat=False)

    plt.title("Convex Hull Construction using Monotone")
    plt.xlabel("X")
    plt.ylabel("Y")
    buf = io.BytesIO()
    frames = []

    for i in range(ani.save_count):
        ani._draw_frame(i)
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
