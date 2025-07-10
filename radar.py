import minescript  # Import Minescript module to access game data

# Get up to 10 nearby entities
entities = minescript.entities(limit=10)

# Loop through each entity
for e in entities:
    # Extract the position (x, y, z) and convert to integers to remove decimals
    x, y, z = map(int, e.position)

    # Display the entity's name, type, and rounded position
    minescript.echo(f"{e.name} ({e.type}) at ({x}, {y}, {z})")