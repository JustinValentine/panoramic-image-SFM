import matplotlib.pyplot as plt
import numpy as np

def calculate_intersection(vertex, optical_center, focal_length):
    t = focal_length / (optical_center[0] - vertex[0])
    intersection_x = optical_center[0] - t * (optical_center[0] - vertex[0])
    intersection_y = optical_center[1] - t * (optical_center[1] - vertex[1])
    return (intersection_x, intersection_y)


def calculate_intersection_circle(vertex, optical_center, radius):
    vertex = [vertex[0] - optical_center[0], vertex[1] - optical_center[1]]
    
    r_vertex = np.linalg.norm(vertex) ** 2
    theta_vertex = np.arctan2(vertex[1], vertex[0])

    intersection_r = radius #* (r_vertex / r_vertex)
    # intersection_theta = radius * (theta_vertex / r_vertex)
    intersection_theta = theta_vertex 


    intersection_x = intersection_r * np.cos(intersection_theta) + optical_center[0]
    intersection_y = intersection_r * np.sin(intersection_theta) + optical_center[1]

    return (intersection_x, intersection_y)


# Define the square's vertices
square_vertices = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

# Define the optical center and focal length
focal_length = 2
optical_center = (3 + focal_length, 0)

# Calculate the intersections with the image line
intersections = [calculate_intersection(vertex, optical_center, focal_length) for vertex in square_vertices]

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 12))

# Draw the square on the first subplot
square_x, square_y = zip(*(square_vertices + [square_vertices[0]]))
ax1.plot(square_x, square_y, 'r-', label='Square')

# Draw the image line on the first subplot
image_line_x = [optical_center[0] - focal_length] * 2
image_line_y = [min(square_y), max(square_y)]
ax1.plot(image_line_x, image_line_y, 'g-', label='Image Line')

# Draw the connecting lines and intersections on the first subplot
for vertex, intersection in zip(square_vertices, intersections):
    ax1.plot([optical_center[0], vertex[0], intersection[0]], [optical_center[1], vertex[1], intersection[1]], 'b-')
    ax1.plot(*intersection, 'bo')

# Draw the optical center on the first subplot
ax1.plot(*optical_center, 'ro', label='Optical Center')

# Configure first subplot settings
ax1.axis('equal')
ax1.legend()
ax1.set_title("Perspective Projection with Image Line")

# Draw the square on the second subplot
ax2.plot(square_x, square_y, 'r-', label='Square')

# Draw the image circle on the second subplot
image_circle_radius = focal_length / 2
theta = np.linspace(0, 2 * np.pi, 100)
circle_x = optical_center[0] - focal_length + image_circle_radius * np.cos(theta)
circle_y = image_circle_radius * np.sin(theta)
optical_center = [np.average(circle_x), np.average(circle_y)]
ax2.plot(circle_x, circle_y, 'g-', label='Image Circle')

# Draw the connecting lines and intersections on the second subplot

intersections = [calculate_intersection_circle(vertex, optical_center, image_circle_radius) for vertex in square_vertices]


for vertex, intersection in zip(square_vertices, intersections):
    ax2.plot([optical_center[0], vertex[0], intersection[0]], [optical_center[1], vertex[1], intersection[1]], 'b-')
    ax2.plot(*intersection, 'bo')

# Draw the optical center on the second subplot
ax2.plot(*optical_center, 'ro', label='Optical Center')

# Configure second subplot settings
ax2.axis('equal')
ax2.legend()
ax2.set_title("Perspective Projection with Image Circle")

# Show the plots
plt.tight_layout()
plt.show()
