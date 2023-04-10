import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

W = []

# Define square corners
square_side_length = 2

square_corners = [
    (0, 0),
    (0, square_side_length),
    (square_side_length, square_side_length),
    (square_side_length, 0)
]

# Define circle parameters
circle_radius = 0.5
num_squares = 5
horizontal_displacement = 3
vertical_displacement = 3 * square_side_length
line_width = 20


def line_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return None

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return px, py


def plot_intersections(circle_center):
    plt.gca().clear()

    # Plot the squares and calculate intersections
    intersections = []
    for row in range(2):
        for sq in range(num_squares):
            displaced_square_corners = [(x + sq * horizontal_displacement, y + row * vertical_displacement) for x, y in square_corners]
            for i in range(4):
                plt.plot(
                    *zip(displaced_square_corners[i], displaced_square_corners[(i + 1) % 4]),
                    marker="o",
                    markersize=5,
                    linestyle="-",
                )

            for corner in displaced_square_corners:
                dx, dy = np.subtract(corner, circle_center)
                distance = np.sqrt(dx ** 2 + dy ** 2)

                if distance == 0:
                    intersection = circle_center
                else:
                    ratio = circle_radius / distance
                    intersection = circle_center[0] + dx * ratio, circle_center[1] + dy * ratio

                intersections.append(intersection)
                # plt.plot(*zip(circle_center, intersection), marker="o")
                plt.plot(*intersection, marker="o", markersize=3)

                # plt.plot(*intersection, marker="x", markersize=10, color="red")

    # Plot the circle
    circle = plt.Circle(circle_center, circle_radius, fill=False)
    plt.gca().add_patch(circle)

    # Draw tangent lines
    line_1_start = (circle_center[0] - line_width / 2, circle_center[1] - circle_radius + 1.5)
    line_1_end = (circle_center[0] + line_width / 2, circle_center[1] - circle_radius + 1.5)
    plt.plot([line_1_start[0], line_1_end[0]], [line_1_start[1], line_1_end[1]], 'k-')

    line_2_start = (circle_center[0] - line_width / 2, circle_center[1] + circle_radius - 1.5)
    line_2_end = (circle_center[0] + line_width / 2, circle_center[1] + circle_radius -1.5)
    plt.plot([line_2_start[0], line_2_end[0]], [line_2_start[1], line_2_end[1]], 'k-')

    # Calculate and plot the intersection of points to the optical center with the lines
    tangent_intersections = []
    camera_points = []
    for row in range(2):
        for sq in range(num_squares):
            displaced_square_corners = [(x + sq * horizontal_displacement, y + row * vertical_displacement) for x, y in square_corners]
            for corner in displaced_square_corners:
                if corner[1] > 4:
                    line_intersection_point = line_intersection((corner, circle_center), (line_1_start, line_1_end))
                    
                else:
                    line_intersection_point = line_intersection((corner, circle_center), (line_2_start, line_2_end))
                    camera_points.append(line_intersection_point)

                if line_intersection_point:
                    # plt.plot(*zip(corner, circle_center), linestyle="--")
                    plt.plot(*zip(corner, circle_center), linestyle="--", alpha=1, linewidth=0.5)

                    # plt.plot(*zip(corner, line_intersection_point), marker="o")
                    plt.plot(*line_intersection_point, marker="o", markersize=5.5)
                    tangent_intersections.append(line_intersection_point)


    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlim(-2, 16)
    plt.ylim(-0.5, 8.5)
    plt.grid()


    return camera_points


# Animation update function
def update(frame):
    circle_center = (frame / 20, 4)
    intersections = plot_intersections(circle_center)
    W.append(intersections)

fig = plt.figure()
ani = FuncAnimation(fig, update, frames=range(-1, 320, 1), interval=320, blit=False)
plt.show()

W = np.array(W)

W = W[:, :, 0]

np.save('W_test', W)
