import minescript  # Import the Minescript module so we can use its functions

# Get a list of up to 10 nearby entities
entities = minescript.entities(limit=10)

# Loop through each entity in the list
for e in entities:
    # Display the entity's name, type (like 'minecraft:zombie'), and its position (x, y, z)
    minescript.echo(f"{e.name} ({e.type}) at {e.position}")