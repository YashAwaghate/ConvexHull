import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

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

        # Show intermediate line checking
        if frame < len(self.intermediate_steps):
            p1, p2 = self.intermediate_steps[frame]
            check_line.set_data([p1.x, p2.x], [p1.y, p2.y])
        else:
            # Clear the green checking line after intermediate steps are completed
            check_line.set_data([], [])

        # Display each finalized edge in red progressively
        if frame < len(self.finalized_edges):
            edge = self.finalized_edges[:frame + 1]
            hull_xs = [point.x for p1, p2 in edge for point in [p1, p2]]
            hull_ys = [point.y for p1, p2 in edge for point in [p1, p2]]
            hull_lines.set_data(hull_xs, hull_ys)
        elif frame >= len(self.intermediate_steps):
            # Close the hull loop after all intermediate steps are done
            self.sort_hull_counterclockwise()
            hull_xs = [p.x for p in self.hull] + [self.hull[0].x]
            hull_ys = [p.y for p in self.hull] + [self.hull[0].y]
            hull_lines.set_data(hull_xs, hull_ys)
            hull_vertices.set_data(hull_xs, hull_ys)

        return scatter, check_line, hull_lines, hull_vertices

# Create the figure and axis for the animation
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Scatter plot for all points
scatter = ax.scatter([], [], color='blue')

# Line for checking pairs
check_line, = ax.plot([], [], 'g-', lw=1)

# Line and points for the hull
hull_lines, = ax.plot([], [], 'r-', lw=2)  # Red line for finalized edges
hull_vertices, = ax.plot([], [], 'ro')     # Red points for hull vertices

# Try reading from input file
fixed_points = file_to_fixed_points("input.txt")
if not fixed_points:
    print("Input file is empty or not found. Generating 10 random points.")
    fixed_points = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]

convex_hull = ConvexHullBruteForce(fixed_points)

# Compute the convex hull before animation
convex_hull.compute_convex_hull()

# Create the animation
anim = FuncAnimation(fig, convex_hull.animate, frames=len(convex_hull.intermediate_steps) + len(convex_hull.finalized_edges), interval=500, repeat=False)
plt.title("Convex Hull Construction with Brute Force (Fixed or Random Points)")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
