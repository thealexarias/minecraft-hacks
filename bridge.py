import minescript, time
from minescript import EventQueue, EventType

# Get the current item in the player's main hand
hand = minescript.player_hand_items()
item = hand.main_hand.item         # The item type (e.g. "minecraft.netherrack")
slot = hand.main_hand.slot         # The hotbar slot it's in (0–8)

# Notify the player that the bridge script is starting
minescript.echo(f"Starting bridge with {item} in slot {slot}")

# Begin moving backward and sneaking
minescript.player_press_backward(True)
minescript.player_press_sneak(True)

# Key codes for movement-related keys: W, A, S, D, Space, Shift, Ctrl
movement_keys = {87, 65, 83, 68, 32, 340, 341}

try:
    # Set up event listener to watch for key presses
    with EventQueue() as q:
        q.register_key_listener()

        while True:
            # Check the current main hand item
            hand_now = minescript.player_hand_items().main_hand

            # Stop if the player switched items or ran out of blocks
            if hand_now.slot != slot or hand_now.item != item or hand_now.count <= 0:
                minescript.echo("Stopped: Item changed or ran out.")
                break

            # Check for key presses that should stop the script
            while q.get(block=False, timeout=0.01) as event:
                if event.type == EventType.KEY and event.action == 1:  # 1 = key down
                    if event.key in movement_keys:
                        minescript.echo(f"Stopped: Movement key pressed (code {event.key})")
                        raise KeyboardInterrupt

            # Get the player's current position and orientation
            x, y, z = minescript.player_position()
            yaw, _ = minescript.player_orientation()

            # Calculate direction vector based on yaw
            dx = round(-minescript.math.sin(yaw))
            dz = round(minescript.math.cos(yaw))

            # Determine where to place the block (behind and below the player)
            place_x = int(x) + dx
            place_y = int(y) - 1
            place_z = int(z) + dz

            # Rotate the camera to look at the center of the target block
            minescript.player_look_at(place_x + 0.5, place_y + 0.5, place_z + 0.5)

            # Simulate right-click to place a block
            minescript.player_press_use(True)
            time.sleep(0.1)
            minescript.player_press_use(False)

            # Wait a short time before placing the next block
            time.sleep(0.3)

except KeyboardInterrupt:
    # Catch manual interruptions or triggered stop
    pass

finally:
    # Release all movement and use keys
    minescript.player_press_backward(False)
    minescript.player_press_sneak(False)
    minescript.player_press_use(False)
    minescript.echo("Bridge script ended.")