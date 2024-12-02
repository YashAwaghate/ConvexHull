import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import namedtuple
from functools import cmp_to_key
import random

def file_to_fixed_points(filename):
    fixed_points = []
    with open(filename, 'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 2:
                x, y = map(int, values)
                fixed_points.append(Point(x, y))
            else:
                print(f"Skipping line: {line.strip()} (does not contain exactly two values)")        
    return fixed_points

# Define a simple Point class
Point = namedtuple('Point', 'x y')

# Global variable to store the center of the polygon
mid = Point(0, 0)

# Determines the quadrant of the point (used in compare())
def quad(p):
    if p.x >= 0 and p.y >= 0:
        return 1
    if p.x <= 0 and p.y >= 0:
        return 2
    if p.x <= 0 and p.y <= 0:
        return 3
    return 4

# Function to find the orientation of the triplet (a, b, c)
def orientation(a, b, c):
    res = (b.y - a.y) * (c.x - b.x) - (c.y - b.y) * (b.x - a.x)
    if res == 0:
        return 0  # Collinear
    return 1 if res > 0 else -1  # Clockwise or Counterclockwise

# A function used by cmp_to_key function to sort an array of points with respect to the center point 'mid'
def compare(p1, q1):
    p = Point(p1.x - mid.x, p1.y - mid.y)
    q = Point(q1.x - mid.x, q1.y - mid.y)
    one = quad(p)
    two = quad(q)
    if one != two:
        return -1 if one < two else 1
    if p.y * q.x < q.y * p.x:
        return -1
    return 1

# Function to merge two convex hulls
def merger(a, b, frames):
    n1, n2 = len(a), len(b)
    ia, ib = 0, 0

    # ia -> rightmost point of a
    for i in range(1, n1):
        if a[i].x > a[ia].x:
            ia = i

    # ib -> leftmost point of b
    for i in range(1, n2):
        if b[i].x < b[ib].x:
            ib = i

    # Finding the upper tangent
    inda, indb = ia, ib
    done = False
    while not done:
        done = True
        while orientation(b[indb], a[inda], a[(inda + 1) % n1]) >= 0:
            inda = (inda + 1) % n1
        while orientation(a[inda], b[indb], b[(n2 + indb - 1) % n2]) <= 0:
            indb = (indb - 1 + n2) % n2
            done = False
    uppera, upperb = inda, indb

    # Finding the lower tangent
    inda, indb = ia, ib
    done = False
    while not done:
        done = True
        while orientation(a[inda], b[indb], b[(indb + 1) % n2]) >= 0:
            indb = (indb + 1) % n2
        while orientation(b[indb], a[inda], a[(n1 + inda - 1) % n1]) <= 0:
            inda = (inda - 1 + n1) % n1
            done = False
    lowera, lowerb = inda, indb

    # Construct the merged hull
    ret = []
    ind = uppera
    ret.append(a[uppera])
    while ind != lowera:
        ind = (ind + 1) % n1
        ret.append(a[ind])
    ind = lowerb
    ret.append(b[lowerb])
    while ind != upperb:
        ind = (ind + 1) % n2
        ret.append(b[ind])

    # Add the merged hull to frames for visualization
    frames.append((list(a), list(b), list(ret)))
    return ret

# Brute force algorithm to find convex hull for a set of less than 6 points
def brute_hull(points):
    global mid
    s = set()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, x2 = points[i].x, points[j].x
            y1, y2 = points[i].y, points[j].y
            a1, b1, c1 = y1 - y2, x2 - x1, x1 * y2 - y1 * x2
            pos, neg = 0, 0
            for k in range(len(points)):
                if (k == i) or (k == j) or (a1 * points[k].x + b1 * points[k].y + c1 <= 0):
                    neg += 1
                if (k == i) or (k == j) or (a1 * points[k].x + b1 * points[k].y + c1 >= 0):
                    pos += 1
            if pos == len(points) or neg == len(points):
                s.add(points[i])
                s.add(points[j])
    ret = list(s)

    # Sorting the points in anti-clockwise order
    mid = Point(sum(p.x for p in ret) / len(ret), sum(p.y for p in ret) / len(ret))
    ret = sorted(ret, key=cmp_to_key(compare))
    return ret

# Recursive function to find the convex hull using divide and conquer
def divide(points, frames):
    if len(points) <= 5:
        hull = brute_hull(points)
        frames.append((list(hull), [], []))  # Record the hull
        return hull

    mid_idx = len(points) // 2
    left = points[:mid_idx]
    right = points[mid_idx:]

    # Convex hull for the left and right sets
    left_hull = divide(left, frames)
    frames.append((list(left_hull), [], []))  # Add left hull for persistent display
    right_hull = divide(right, frames)
    frames.append((list(left_hull), list(right_hull), []))  # Show both hulls before merging

    # Merging the convex hulls
    return merger(left_hull, right_hull, frames)

# Visualization setup
fig, ax = plt.subplots()
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

# Generate random points
num_points = 20
random_points = [Point(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(num_points)]
# random_points = file_to_fixed_points("input.txt")
random_points.sort(key=lambda p: (p.x, p.y))

# Compute convex hull with divide and conquer and record frames for animation
frames = []
hull = divide(random_points, frames)

# Animation function
def animate(frame_idx):
    ax.clear()
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    # Plot all points
    ax.scatter([p.x for p in random_points], [p.y for p in random_points], color='blue')

    # Get current frame data
    left_hull, right_hull, merged_hull = frames[frame_idx]

    # Plot left hull in gray (keep it on canvas while constructing right hull)
    if left_hull:
        for i in range(len(left_hull)):
            p1 = left_hull[i]
            p2 = left_hull[(i + 1) % len(left_hull)]
            ax.plot([p1.x, p2.x], [p1.y, p2.y], 'gray')

    # Plot right hull in gray once it's constructed
    if right_hull:
        for i in range(len(right_hull)):
            p1 = right_hull[i]
            p2 = right_hull[(i + 1) % len(right_hull)]
            ax.plot([p1.x, p2.x], [p1.y, p2.y], 'gray')

    # Plot merged hull in red once both hulls are ready
    if merged_hull:
        for i in range(len(merged_hull)):
            p1 = merged_hull[i]
            p2 = merged_hull[(i + 1) % len(merged_hull)]
            ax.plot([p1.x, p2.x], [p1.y, p2.y], 'r-')

# Create the animation
ani = FuncAnimation(fig, animate, frames=len(frames), interval=1000, repeat=False)
plt.title("Divide and Conquer Convex Hull (Animation)")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()