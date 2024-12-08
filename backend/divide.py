import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import namedtuple
from functools import cmp_to_key
import random
import base64
import io
from PIL import Image
import json

def divide_main(data):
    # Decode 'data' if it's a bytes object
    if isinstance(data, bytes):
        try:
            data = json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            data = {}

    Point = namedtuple('Point', 'x y')
    mid = Point(0, 0)

    def quad(p):
        if p.x >= 0 and p.y >= 0:
            return 1
        if p.x <= 0 and p.y >= 0:
            return 2
        if p.x <= 0 and p.y <= 0:
            return 3
        return 4

    def orientation(a, b, c):
        res = (b.y - a.y) * (c.x - b.x) - (c.y - b.y) * (b.x - a.x)
        if res == 0:
            return 0
        return 1 if res > 0 else -1

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

    def brute_hull(points):
        nonlocal mid
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
        if ret:
            mid = Point(sum(p.x for p in ret) / len(ret), sum(p.y for p in ret) / len(ret))
            ret = sorted(ret, key=cmp_to_key(compare))
        return ret

    def merger(a, b, frames):
        n1, n2 = len(a), len(b)
        ia, ib = 0, 0
        for i in range(1, n1):
            if a[i].x > a[ia].x:
                ia = i
        for i in range(1, n2):
            if b[i].x < b[ib].x:
                ib = i
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

        frames.append((list(a), list(b), list(ret)))
        return ret

    def divide(points, frames):
        if len(points) <= 5:
            hull = brute_hull(points)
            frames.append((list(hull), [], []))
            return hull

        mid_idx = len(points) // 2
        left = points[:mid_idx]
        right = points[mid_idx:]
        left_hull = divide(left, frames)
        right_hull = divide(right, frames)
        frames.append((list(left_hull), list(right_hull), []))
        return merger(left_hull, right_hull, frames)

    # Extract points or generate random points
    points_from_file = data.get("payload", [])
    num_points = int(data.get("numPoints", 10))  # Default to 10 if not provided

    if points_from_file == [[0]]:
        print(f"Received [[0]]. Generating {num_points} random points.")
        random_data = np.random.randint(0, 100, size=(num_points, 2))
        random_points = [Point(x, y) for x, y in random_data]
    elif points_from_file:
        points_array = np.array(points_from_file)
        random_points = [Point(x, y) for x, y in points_array]
        print(f"Using {len(random_points)} points from input data.")
    else:
        print(f"Input data is empty. Generating {num_points} random points.")
        random_data = np.random.randint(0, 100, size=(num_points, 2))
        random_points = [Point(x, y) for x, y in random_data]

    random_points.sort(key=lambda p: (p.x, p.y))
    min_x, max_x = min(p.x for p in random_points), max(p.x for p in random_points)
    min_y, max_y = min(p.y for p in random_points), max(p.y for p in random_points)

    fig, ax = plt.subplots()
    frames = []
    hull = divide(random_points, frames)

    def animate(frame_idx):
        ax.clear()
        ax.set_xlim(min_x - 10, max_x + 10)
        ax.set_ylim(min_y - 10, max_y + 10)
        ax.scatter([p.x for p in random_points], [p.y for p in random_points], color='blue')

        left_hull, right_hull, merged_hull = frames[frame_idx]

        # Plot intermediate hulls in grey dotted lines
        for h in [left_hull, right_hull]:
            if h:
                ax.plot([p.x for p in h + [h[0]]],
                        [p.y for p in h + [h[0]]], 'k--', linewidth=1, alpha=0.7)

        # Plot the final merged hull in red if it exists
        if frame_idx == len(frames) - 1 and merged_hull:
            ax.plot([p.x for p in merged_hull + [merged_hull[0]]],
                    [p.y for p in merged_hull + [merged_hull[0]]], 'r-', linewidth=2)

    anim = FuncAnimation(fig, animate, frames=len(frames), interval=1000, repeat=False)

    buf = io.BytesIO()
    img_frames = []
    for i in range(len(frames)):
        animate(i)
        fig.canvas.draw()
        img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        img_frames.append(img)

    img_frames[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=img_frames[1:],
        loop=0,
        duration=1000
    )

    buf.seek(0)
    base64_image = base64.b64encode(buf.read()).decode('ascii')
    buf.close()

    print("GIF Created and Encoded to Base64")
    return base64_image
