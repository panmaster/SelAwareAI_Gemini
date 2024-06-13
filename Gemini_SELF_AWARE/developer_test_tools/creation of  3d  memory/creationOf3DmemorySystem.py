import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Create the main 3D memory folder
main_folder_name = "3DMemoryFolder"
os.makedirs(main_folder_name, exist_ok=True)

# Dimensions of the 3D array
x_dim = 8
y_dim = 8
z_dim = 8

# Loop through each dimension to create folders
for x in range(x_dim):
    for y in range(y_dim):
        for z in range(z_dim):
            # Create folder name with coordinates
            folder_name = f"Folder_{x}_{y}_{z}"
            folder_path = os.path.join(main_folder_name, folder_name)

            # Create the folder
            os.makedirs(folder_path, exist_ok=True)

            # Create "synaps" file in each folder
            synaps_file_path = os.path.join(folder_path, "synaps.txt")
            with open(synaps_file_path, 'w') as f:
                f.write("This file stores information about connections to other folders.")

print(f"Created {x_dim * y_dim * z_dim} folders in {main_folder_name}")

# Create a list of nodes
nodes = []
for x in range(x_dim):
    for y in range(y_dim):
        for z in range(z_dim):
            nodes.append((x, y, z))

# Create a list of edges (connect adjacent nodes)
edges = []
for x in range(x_dim):
    for y in range(y_dim):
        for z in range(z_dim):
            if x > 0:
                edges.append(((x, y, z), (x-1, y, z)))
            if x < x_dim - 1:
                edges.append(((x, y, z), (x+1, y, z)))
            if y > 0:
                edges.append(((x, y, z), (x, y-1, z)))
            if y < y_dim - 1:
                edges.append(((x, y, z), (x, y+1, z)))
            if z > 0:
                edges.append(((x, y, z), (x, y, z-1)))
            if z < z_dim - 1:
                edges.append(((x, y, z), (x, y, z+1)))

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot nodes
xs, ys, zs = zip(*nodes)
ax.scatter(xs, ys, zs, c='blue', marker='o')

# Plot edges
edge_lines = [[(edge[0][0], edge[0][1], edge[0][2]), (edge[1][0], edge[1][1], edge[1][2])] for edge in edges]
edge_collection = Line3DCollection(edge_lines, colors='gray', linewidths=1)
ax.add_collection3d(edge_collection)

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set equal aspect ratio
ax.set_box_aspect([x_dim, y_dim, z_dim])

plt.show()