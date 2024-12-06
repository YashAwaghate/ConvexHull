import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import namedtuple
from functools import cmp_to_key
import random

# Define a simple Point class
Point = namedtuple('Point', 'x y')

# Function to read points from a file
def file_to_fixed_points(filename):
    fixed_points = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 2:
                    x, y = map(int, values)
                    fixed_points.append(Point(x, y))
                else:
                    print(f"Skipping line: {line.strip()} (does not contain exactly two values)")
    except FileNotFoundError:
        print(f"{filename} not found.")
    return fixed_points

# Function to find the orientation of the triplet (p, q, r)
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

# A utility function to return square of distance between p1 and p2
def dist_sq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

# A utility function to find next to top in a stack
def next_to_top(S):
    return S[-2]

# A function used by cmp_to_key function to sort an array of points with respect to the first point
def compare(p1, p2):
    o = orientation(p0, p1, p2)
    if o == 0:
        return -1 if dist_sq(p0, p2) >= dist_sq(p0, p1) else 1
    return -1 if o == 2 else 1

# Convex Hull using Graham Scan
p0 = Point(0, 0)

def convex_hull(points):
    n = len(points)
    if n < 3:
        return []

    # Find the bottom-most point
    ymin = points[0].y
    min_idx = 0
    for i in range(1, n):
        y = points[i].y
        if (y < ymin) or (ymin == y and points[i].x < points[min_idx].x):
            ymin = points[i].y
            min_idx = i

    # Place the bottom-most point at first position
    points[0], points[min_idx] = points[min_idx], points[0]
    global p0
    p0 = points[0]

    # Sort n-1 points with respect to the first point
    points = sorted(points, key=cmp_to_key(compare))

    # Initialize the stack with the first two points after sorting
    S = [points[0], points[1]]
    steps = [(S.copy(), False)]  # Record the initial two points as the first step with tentative status

    # Process remaining points
    for i in range(2, len(points)):
        while len(S) > 1 and orientation(next_to_top(S), S[-1], points[i]) != 2:
            S.pop()
        S.append(points[i])
        steps.append((S.copy(), True if i == len(points) - 1 else False))  # Mark as finalized only for last step

    return S, steps

# Check if input.txt is empty or not
num_points = 10  # Number of random points
points_from_file = file_to_fixed_points("input.txt")
if points_from_file:
    random_points = points_from_file
    print(f"Using {len(random_points)} points from input.txt.")
else:
    print("Input file is empty or not found. Generating random points.")
    random_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]

# Compute the convex hull and steps for visualization
hull, steps = convex_hull(random_points)

# Visualization setup
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
scatter = ax.scatter([], [], color='blue')
tentative_line, = ax.plot([], [], 'grey', lw=2)  # Grey line for tentative edges
finalized_line, = ax.plot([], [], 'r-', lw=2)    # Red line for finalized hull edges
start_marker, = ax.plot([], [], 'yo')             # Yellow marker for the start point
point_marker, = ax.plot([], [], 'go')             # Green marker for the current point being processed

def animate(frame):
    # Display all points
    scatter.set_offsets([(p.x, p.y) for p in random_points])

    # Highlight the starting point
    start_marker.set_data(p0.x, p0.y)

    # Retrieve current hull and finalization status
    if frame < len(steps):
        current_hull, finalized = steps[frame]
        hull_xs = [p.x for p in current_hull]
        hull_ys = [p.y for p in current_hull]

        # Display tentative line in grey if not finalized, otherwise red
        if finalized:
            finalized_line.set_data(hull_xs + [hull_xs[0]], hull_ys + [hull_ys[0]])  # Close the hull loop in red
            tentative_line.set_data([], [])  # Clear the grey line when finalizing
        else:
            tentative_line.set_data(hull_xs, hull_ys)  # Show grey line for tentative edges
            finalized_line.set_data([], [])  # Clear the red line during tentative phase

        # Highlight the current point being processed
        point_marker.set_data(current_hull[-1].x, current_hull[-1].y)
    else:
        # Final display of the full hull
        hull_xs = [p.x for p in hull]
        hull_ys = [p.y for p in hull]
        finalized_line.set_data(hull_xs + [hull_xs[0]], hull_ys + [hull_ys[0]])
        tentative_line.set_data([], [])  # Ensure no grey line remains
        point_marker.set_data([], [])  # Clear the point marker

    return scatter, tentative_line, finalized_line, start_marker, point_marker

# Create the animation
anim = FuncAnimation(fig, animate, frames=len(steps) + 10, interval=500, repeat=False)
plt.title("Convex Hull Construction with Graham Scan")
plt.xlabel("X")
plt.ylabel("Y")
anim.save("output.gif", writer="pillow")