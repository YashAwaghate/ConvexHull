import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import namedtuple
import random

# Define a simple Point class
Point = namedtuple('Point', 'x y')


def file_to_fixed_points(filename):
    """Reads points from a file."""
    fixed_points = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 2:
                    x, y = map(int, values)
                    fixed_points.append(Point(x, y))
                else:
                    print(
                        f"Skipping line: {line.strip()} (does not contain exactly two values)")
    except FileNotFoundError:
        print(f"{filename} not found.")
    return fixed_points


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
    lower.pop()
    upper.pop()

    # Combine lower and upper hulls to form the final convex hull
    convex_hull = lower + upper
    return convex_hull, steps


# Function to generate random points
def generate_random_points(n, xlim, ylim):
    """Generates n random points within the given limits."""
    return [Point(random.randint(0, xlim), random.randint(0, ylim)) for _ in
            range(n)]


# Try to read points from input.txt
points = file_to_fixed_points("input.txt")

# If no points are found, generate 20 random points
if not points:
    print("Input file is empty or not found. Generating 20 random points.")
    points = generate_random_points(10, 100, 100)

# Compute the convex hull and animation steps
convex_hull, steps = monotone_chain(points)

# Create the animation
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
scat = ax.scatter([p.x for p in points], [p.y for p in points])

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


ani = animation.FuncAnimation(fig, update, frames=len(steps), blit=True,
                              repeat=False)

plt.title("Convex Hull Construction (Input or Random Points)")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
