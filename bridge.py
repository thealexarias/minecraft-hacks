import minescript, time, math
from minescript import EventQueue, EventType
import queue

# Setup: get starting item and slot
start_hand = minescript.player_hand_items().main_hand
start_item = start_hand.item
start_slot = start_hand.slot

minescript.echo(f"Bridging with {start_item} in slot {start_slot}")

# Begin movement
minescript.player_press_backward(True)
minescript.player_press_sneak(True)

# Movement key codes to cancel bridge
cancel_keys = {87, 65, 83, 68, 32, 340, 341}  # W A S D Space Shift Ctrl

try:
    with EventQueue() as events:
        events.register_key_listener()

        while True:
            # Cancel if movement key is pressed
            try:
                event = events.get(block=False, timeout=0.01)
                if event.type == EventType.KEY and event.action == 1:
                    if event.key in cancel_keys:
                        minescript.echo("Stopped: Movement key pressed.")
                        break
            except queue.Empty:
                pass

            # Cancel if item is changed or depleted
            hand = minescript.player_hand_items().main_hand
            if hand.slot != start_slot or hand.item != start_item or hand.count <= 0:
                minescript.echo("Stopped: Item changed or ran out.")
                break

            # Compute placement position
            x, y, z = minescript.player_position()
            yaw, _ = minescript.player_orientation()

            # Determine block position behind and below
            dx = round(-math.sin(math.radians(yaw)))
            dz = round(math.cos(math.radians(yaw)))
            px, py, pz = int(x) + dx, int(y) - 1, int(z) + dz

            # Look and place
            minescript.player_look_at(px + 0.5, py + 0.5, pz + 0.5)
            minescript.player_press_use(True)
            time.sleep(0.1)
            minescript.player_press_use(False)

            time.sleep(0.3)

finally:
    # Always release keys
    minescript.player_press_backward(False)
    minescript.player_press_sneak(False)
    minescript.player_press_use(False)
    minescript.echo("Bridge script ended.")
