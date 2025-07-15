import minescript
import time
import queue
from minescript import EventQueue, EventType, player_press_use, entities

BOBBER_TYPE = "entity.minecraft.fishing_bobber"
STOP_KEY = 88  # X

def find_bobber():
    for e in entities(type=BOBBER_TYPE):
        if e.position:
            return e
    return None

def wait_for_bobber(timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        b = find_bobber()
        if b:
            return b
        time.sleep(0.1)
    return None

def wait_for_bobber_despawn(timeout=3):
    start = time.time()
    while time.time() - start < timeout:
        if not find_bobber():
            return True
        time.sleep(0.1)
    return False

def bobber_dipped(initial_y, threshold=0.1):
    b = find_bobber()
    if b and isinstance(b.position, list):
        return (initial_y - b.position[1]) > threshold
    return False

def auto_fish_with_key_stop():
    minescript.echo("🎣 Auto-fishing started. Press X to stop.")

    with EventQueue() as events:
        events.register_key_listener()

        while True:
            # Stop if X key is pressed
            try:
                evt = events.get(block=False, timeout=0.01)
                if evt.type == EventType.KEY and evt.action == 1 and evt.key == STOP_KEY:
                    minescript.echo("🛑 Stopped by pressing X.")
                    return
            except queue.Empty:
                pass

            # Cast rod
            player_press_use(True)
            time.sleep(0.1)
            player_press_use(False)
            time.sleep(2) # wait for bobber to land

            # Wait for bobber
            bobber = wait_for_bobber()
            if not bobber or not isinstance(bobber.position, list):
                minescript.echo("❌ No bobber found. Retrying...")
                time.sleep(2)
                continue

            time.sleep(0.5)
            initial_y = bobber.position[1]
            dipped = False
            start_time = time.time()

            while time.time() - start_time < 30:
                try:
                    evt = events.get(block=False, timeout=0.01)
                    if evt.type == EventType.KEY and evt.action == 1 and evt.key == STOP_KEY:
                        minescript.echo("🛑 Stopped by pressing X.")
                        return
                except queue.Empty:
                    pass

                if bobber_dipped(initial_y):
                    dipped = True
                    break

                time.sleep(0.1)

            # Reel in
            if dipped:
                minescript.echo("🐟 Bite detected! Reeling in...")
            else:
                minescript.echo("⏳ No bite. Reeling anyway...")

            player_press_use(True)
            time.sleep(0.1)
            player_press_use(False)
            wait_for_bobber_despawn()
            time.sleep(1)

auto_fish_with_key_stop()
