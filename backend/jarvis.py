import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import base64
import io
from PIL import Image

def jarvis_main(data):
    def leftmost_point(points):
        """Returns the index of the leftmost point in the list of points."""
        return min(range(len(points)), key=lambda i: points[i][0])

    def orientation(p, q, r):
        """Returns the orientation of the ordered triplet (p, q, r).
        0 -> p, q and r are collinear
        1 -> Clockwise
        2 -> Counterclockwise
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def gift_wrapping_animation(points):
        """Creates an animated visualization of the Gift Wrapping algorithm."""
        n = len(points)
        if n < 3:
            print("Convex hull is not possible with less than 3 points.")
            return

        fig, ax = plt.subplots()
        ax.set_title("Gift Wrapping Algorithm Animation")

        # Dynamic axis limits based on points
        x_min, x_max = min(p[0] for p in points) - 10, max(p[0] for p in points) + 10
        y_min, y_max = min(p[1] for p in points) - 10, max(p[1] for p in points) + 10
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        plt.scatter(*zip(*points), color='blue')  # Plot all points

        hull = []
        hull_lines = []
        l = leftmost_point(points)
        p = l

        def update(frame):
            nonlocal p
            hull.append(points[p])
            q = (p + 1) % n

            for i in range(n):
                if orientation(points[p], points[i], points[q]) == 2:
                    q = i

            # Add the successful line to the hull
            line, = ax.plot([points[p][0], points[q][0]],
                            [points[p][1], points[q][1]], 'r-')
            hull_lines.append(line)

            p = q

            # Close the hull if we are back to the start
            if p == l:
                line, = ax.plot([hull[-1][0], hull[0][0]],
                                [hull[-1][1], hull[0][1]], 'r-')
                hull_lines.append(line)
                anim.event_source.stop()  # Stop the animation when the hull is complete

        anim = FuncAnimation(fig, update, frames=n + 10, repeat=False)
        buf = io.BytesIO()
        frames = []

        for i in range(n + 10):
            update(i)
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

    # Extract points from the data or generate random points if none provided
    points_from_file = data.get("payload", [])
    num_points = int(data.get("numPoints", 10))  # Default to 10 random points if not provided

    if points_from_file == [[0]]:
        print(f"Received [[0]]. Generating {num_points} random points.")
        points = np.random.randint(0, 100, size=(num_points, 2))
    elif points_from_file:
        points = np.array(points_from_file)
        print(f"Using {len(points)} points from input data.")
    else:
        print(f"Input data is empty. Generating {num_points} random points.")
        points = np.random.randint(0, 100, size=(num_points, 2))

    return gift_wrapping_animation(points)
