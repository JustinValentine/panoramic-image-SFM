import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


W = []
# Define square corners
square_side_length = 2
square_corners = [
    (0, 0),
    (square_side_length, 0),
    (square_side_length, square_side_length),
    (0, square_side_length),
]

# Define circle parameters
circle_radius = 0.25

def plot_intersections(circle_center):
    plt.gca().clear()

    # Plot the square
    for i in range(4):
        plt.plot(
            *zip(square_corners[i], square_corners[(i + 1) % 4]),
            marker="o",
            markersize=5,
            linestyle="-",
        )

    # Plot the circle
    circle = plt.Circle(circle_center, circle_radius, fill=False)
    plt.gca().add_patch(circle)

    # Calculate and plot the intersections
    intersections = []
    for corner in square_corners:
        dx, dy = np.subtract(corner, circle_center)
        distance = np.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            intersection = circle_center
        else:
            ratio = circle_radius / distance
            intersection = circle_center[0] + dx * ratio, circle_center[1] + dy * ratio

        plt.plot(*zip(circle_center, intersection), marker="o", linestyle="--")
        plt.plot(*intersection, marker="x", markersize=10, color="red")
        intersections.append(intersection)

    # Convert intersections to 1D image coordinates
    reference_point = (circle_center[0] + circle_radius, circle_center[1])
    arc_lengths = []
    for intersection in intersections:
        angle = np.arctan2(intersection[1] - circle_center[1], intersection[0] - circle_center[0]) - np.arctan2(reference_point[1] - circle_center[1], reference_point[0] - circle_center[0])
        if angle < 0:
            angle += 2 * np.pi
        arc_length = angle * circle_radius
        arc_lengths.append(arc_length)

    # save to W
    W.append(arc_lengths)

    # Plot the 1D image coordinates
    for i, arc_length in enumerate(arc_lengths):
        plt.plot(arc_length, -1, marker="o", markersize=5, color="blue")
        plt.text(arc_length, -1.5, f"{arc_length:.2f}")

    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlim(-0.5, square_side_length + 0.5)
    plt.ylim(-2, square_side_length + 0.5)
    plt.grid()

# Animation update function
def update(frame):
    circle_center = (1 + 0.5 * np.cos(frame / 180*np.pi), 1 + 0.5 * np.sin(frame / 180*np.pi))
    plot_intersections(circle_center)

fig = plt.figure()
ani = FuncAnimation(fig, update, frames=range(0, 360, 10), interval=50, blit=False)
plt.show()

W = np.array(W)

print(W.shape)

np.save('W_test', W)

pass
