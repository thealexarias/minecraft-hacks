import minescript, time
from minescript import EventQueue, EventType
import queue  # For handling empty event checks

# === SETUP ===

# Get the item currently held in your main hand
hand = minescript.player_hand_items().main_hand
start_item = hand.item
start_slot = hand.slot

# Lock pitch to 84 degrees (looking down at the edge of the block)
locked_pitch = 85.0

# Get current yaw and snap to nearest cardinal direction (0°, 90°, 180°, 270°)
raw_yaw, _ = minescript.player_orientation()
locked_yaw = round(raw_yaw / 90) * 90 % 360  # Normalize yaw to 0–359

minescript.echo(f"Locked yaw: {locked_yaw}°, pitch: {locked_pitch}°")


# These key codes will cancel the bridge if pressed
cancel_keys = {87, 83, 32, 340, 341}  # W, S, Space, Shift, Ctrl

# Tell the player the script has started
minescript.echo(f"Starting bridge with {start_item} (slot {start_slot})")
minescript.echo(f"Locked pitch: {locked_pitch:.1f}°")

# Press and hold crouch and backward keys
minescript.player_press_sneak(True)
minescript.player_press_backward(True)

# Walk backwards for a second
time.sleep(1)

# === MAIN LOOP ===
try:
    with EventQueue() as events:
        events.register_key_listener()

        while True:

            # Stop if the held item changed or ran out
            hand_now = minescript.player_hand_items().main_hand
            if hand_now.slot != start_slot or hand_now.item != start_item or hand_now.count <= 0:
                minescript.echo("Stopped: Item changed or ran out.")
                break

            # Stop if player presses a cancel key
            try:
                event = events.get(block=False, timeout=0.01)
                if event.type == EventType.KEY and event.action == 1:  # Key press
                    if event.key in cancel_keys:
                        minescript.echo(f"Stopped: Key {event.key} pressed.")
                        break
            except queue.Empty:
                pass  # No key press detected this cycle

            # Place the block (right-click)
            minescript.player_press_use(True)
            time.sleep(0.1)
            minescript.player_press_use(False)

            # Wait before next placement
            time.sleep(0.25)

finally:
    # === CLEANUP ===
    # Always release any held keys
    minescript.player_press_backward(False)
    minescript.player_press_use(False)
    # Wait a second before releasing crouch (to avoid falling)
    time.sleep(1)
    minescript.player_press_sneak(False)
    # Notify script finished
    minescript.echo("Bridge script finished.")

