import minescript  # Import Minescript module to access game data

# Get up to 10 nearby entities
entities = minescript.entities(limit=10)

# Loop through each entity
for e in entities:
    # Convert position to integers (x, y, z)
    x, y, z = map(int, e.position)

    # Display just the entity's name and position
    minescript.echo(f"{e.name} at ({x}, {y}, {z})")