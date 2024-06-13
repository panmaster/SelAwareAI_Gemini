from ursina import *
import hashlib

def hash_category(category):
    """Hashes a category name to 3D coordinates (limited to 6x6x6 grid)."""
    hash_object = hashlib.sha256(category.encode())
    hex_digest = hash_object.hexdigest()
    x = int(hex_digest[0:2], 16) % 6  # Modulo for creation of  3d  memory-coordinate
    y = int(hex_digest[2:4], 16) % 6  # Modulo for y-coordinate
    z = int(hex_digest[4:6], 16) % 6  # Modulo for z-coordinate
    return x, y, z

def create_category_node(category):
    """Creates a 3D node for a category."""
    x, y, z = hash_category(category)
    node = Entity(model='cube', color=color.blue, scale=0.25, position=(x, y, z), name=category, collider='box')
    node.opacity = 0.5  # Make the box transparent
    return node

def create_no_category_node():
    """Creates a 3D node for categories with no assignment."""
    # Place the "Category_None" node at a unique position
    node = Entity(model='cube', color=color.gray, scale=0.25, position=(3, 3, 3), name='Category_None', collider='box')
    node.opacity = 0.5  # Make the box transparent
    return node

def create_empty_node(x, y, z):
    """Creates a 3D node for empty grid spaces."""
    node = Entity(model='cube', color=color.brown, scale=0.25, position=(x, y, z), collider='box')
    node.opacity = 0.7  # Make the box transparent
    return node

def add_connection(start_node, end_node, direction, strength):
    """Creates an arrow connection between two category nodes."""
    # Use a pre-existing model or create your own arrow model
    arrow = Entity(model='arrow', color=color.red, scale=(0.1, 0.1, 0.3)) # Use the 'arrow' model
    arrow.position = start_node.position + (end_node.position - start_node.position) * 0.5
    arrow.look_at(end_node, axis='forward')  # Align the arrow with the direction
    return arrow

# Create the main Ursina application
app = Ursina(win_size=(864, 1536), background=color.black)  # Set background to black

# Example categories
categories = [
    "Events", "Actions", "Concepts", "People", "Places",
    "Emotions", "Relationships", "Objects", "Time", "Space",
    "Science", "History", "Literature", "Art", "Music",
    "Sports", "Technology", "Nature", "Animals", "Plants",
    "Food", "Health", "Travel", "Education", "Business",
    # ... add more categories ...
]

# Create a dictionary to store category nodes
category_nodes = {}
folder_nodes = {}  # Create a dictionary to store folders

# Create 3D nodes for each category and organize into folders
for category in categories:
    node = create_category_node(category)
    category_nodes[category] = node  # Store the node for easy access
    folder_name = "Folder_" + category
    if folder_name not in folder_nodes:
        folder_nodes[folder_name] = Entity(name=folder_name)  # Create a folder entity if it doesn't exist
    node.parent = folder_nodes[folder_name]  # Set parent to the corresponding folder

# Create nodes for categories with no assignment
no_category_node = create_no_category_node()
folder_nodes['Folder_Category_None'] = Entity(name='Folder_Category_None')  # Create the folder
no_category_node.parent = folder_nodes['Folder_Category_None']  # Assign the node to the folder

# Create nodes to fill the remaining grid spaces
for x in range(6):
    for y in range(6):
        for z in range(6):
            position = (x, y, z)
            if position not in [node.position for node in category_nodes.values()]:
                empty_node = create_empty_node(x, y, z)

# Example connections (customize these)
connections = [
    ("Events", "Actions"),
    ("Actions", "Events"),
    ("Concepts", "Science"),
    ("Science", "Technology"),
]

# Create arrows for connections
for start_category, end_category in connections:
    start_node = category_nodes[start_category]
    end_node = category_nodes[end_category]
    arrow = add_connection(start_node, end_node, "Forward", 0.8)  # Assuming connections are bi-directional

# Add a camera
camera.position = (0, 0, -10)  # Move the camera back a bit

# Enable free flight
EditorCamera()

# Lighting
directional_light = DirectionalLight(color=color.white, strength=0.8)
ambient_light = AmbientLight(color=color.white, strength=0.3) # Set ambient light strength to 0.3
spotlight = SpotLight(parent=camera, color=color.white, range=20) # add a spotlight

# Run the application
app.run()