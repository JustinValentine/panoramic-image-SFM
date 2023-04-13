import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

W = []

# Define circle parameters
circle_radius = 0.6
num_circles = 2
horizontal_displacement = 8
vertical_displacement = 8 * 2 * circle_radius
line_width = 6
num_points = 10

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

    # Plot the point clouds for the circles and calculate intersections
    intersections = []
    for row in range(2):
        for circ in range(num_circles):
            displaced_circle_center = (circ * horizontal_displacement + circle_radius, row * vertical_displacement + circle_radius)

            # Generate point cloud for the circle
            angles = np.linspace(0, 2 * np.pi, num_points)
            points = [(circle_radius * np.cos(angle), circle_radius * np.sin(angle)) for angle in angles]
            displaced_points = [np.add(point, displaced_circle_center) for point in points]

            # Plot the point cloud
            for point in displaced_points:
                plt.plot(*point, marker="o", markersize=3)

            for point in displaced_points:
                dx, dy = np.subtract(point, circle_center)
                distance = np.sqrt(dx ** 2 + dy ** 2)

                if distance == 0:
                    intersection = circle_center
                else:
                    ratio = circle_radius / distance
                    intersection = circle_center[0] + dx * ratio, circle_center[1] + dy * ratio

                intersections.append(intersection)
                plt.plot(*intersection, marker="o", markersize=3)


    # Plot the central circle
    circle = plt.Circle(circle_center, circle_radius, fill=False)
    plt.gca().add_patch(circle)

    # Draw tangent lines
    line_1_start = (circle_center[0] - line_width / 2, circle_center[1] - circle_radius + 1.5)
    line_1_end = (circle_center[0] + line_width / 2, circle_center[1] - circle_radius + 1.5)
    plt.plot([line_1_start[0], line_1_end[0]], [line_1_start[1], line_1_end[1]], 'k-')

    line_2_start = (circle_center[0] - line_width / 2, circle_center[1] + circle_radius - 1.5)
    line_2_end = (circle_center[0] + line_width / 2, circle_center[1] + circle_radius - 1.5)
    plt.plot([line_2_start[0], line_2_end[0]], [line_2_start[1], line_2_end[1]], 'k-')

    # Calculate and plot the intersection of points to the optical center with the lines
    tangent_intersections = []
    camera_points = []
    for row in range(2):
        for circ in range(num_circles):
            displaced_circle_center = (circ * horizontal_displacement + circle_radius, row * vertical_displacement + circle_radius)
            angles = np.linspace(0, 2 * np.pi, num_points)
            points = [(circle_radius * np.cos(angle), circle_radius * np.sin(angle)) for angle in angles]
            displaced_points = [np.add(point, displaced_circle_center) for point in points]
            
            for point in displaced_points:
                if point[1] > 8:
                    line_intersection_point = line_intersection((point, circle_center), (line_1_start, line_1_end))
                    camera_points.append(line_intersection_point)

                else:
                    line_intersection_point = line_intersection((point, circle_center), (line_2_start, line_2_end))

                if line_intersection_point:
                    plt.plot(*zip(point, circle_center), linestyle="--", alpha=1, linewidth=0.5)
                    plt.plot(*line_intersection_point, marker="o", markersize=5.5)
                    tangent_intersections.append(line_intersection_point)


    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlim(-2, 16)
    plt.ylim(-2, 16)
    plt.grid()

    return camera_points


# Animation update function
# def update(frame):
#     circle_center = (frame / 3, 6)
#     intersections = plot_intersections(circle_center)
#     W.append(intersections)


def update(frame):
    circle_center = (frame / 3, 6 + 1 * np.sin(frame / 20))
    intersections = plot_intersections(circle_center)
    W.append(intersections)


fig = plt.figure()
ani = FuncAnimation(fig, update, frames=range(-1, 320, 1), interval=320, blit=False)
plt.show()

W = np.array(W)

W = W[:, :, 0]  # take just x axis (projection is 1-dimensional)

np.save('W_test', W)
