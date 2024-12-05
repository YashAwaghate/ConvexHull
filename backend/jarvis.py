import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os


def file_to_numpy_array(filename):
    """Reads points from a file and returns a NumPy array."""
    data = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 2:  # Ensure two values per line
                    data.append(list(map(float, values)))  # Convert to floats
                else:
                    print(
                        f"Skipping line: {line.strip()} (does not contain exactly two values)")
    except FileNotFoundError:
        print(f"{filename} not found.")
    return np.array(data)


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
    """Creates an animated visualization of the Gift Wrapping algorithm with retracting failed attempts."""
    n = len(points)
    if n < 3:
        print("Convex hull is not possible with less than 3 points.")
        return

    fig, ax = plt.subplots()
    ax.set_title(
        "Gift Wrapping Algorithm Animation with Retracting Failed Attempts")
    plt.scatter(*zip(*points), color='blue')  # Plot all points

    hull = []
    hull_lines = []
    retracting_line = None

    l = leftmost_point(points)
    p = l

    def update(frame):
        nonlocal p, retracting_line
        # Clear the retracting line from the previous step
        if retracting_line:
            retracting_line.remove()
            retracting_line = None

        hull.append(points[p])
        q = (p + 1) % n

        for i in range(n):
            # Show the current retracting line
            if retracting_line:
                retracting_line.remove()  # Remove previous retracting line
            retracting_line, = ax.plot([points[p][0], points[i][0]],
                                       [points[p][1], points[i][1]],
                                       'gray', linestyle='--',
                                       alpha=0.5)  # Draw the new retracting line
            plt.pause(0.2)  # Pause briefly to show the retracting line

            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        # Add the successful line to the hull and keep it
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

    anim = FuncAnimation(fig, update, frames=range(len(points)), repeat=False)
    plt.show()


# Try reading points from input.txt
points = file_to_numpy_array("input.txt")

# If no points are found, generate 10 random points
if points.size == 0:
    print("Input file is empty or not found. Generating 10 random points.")
    points = np.random.rand(10,
                            2) * 100  # Generate random points in range [0, 100)

gift_wrapping_animation(points)
