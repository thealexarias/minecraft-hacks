import minescript
import time
import queue
from minescript import EventQueue, EventType, player_press_attack

STOP_KEY = 88  # X key

def auto_attack_with_key_stop():
    minescript.echo("🗡️ Auto-attacking started. Press X to stop.")

    with EventQueue() as events:
        events.register_key_listener()

        while True:
            # Check if X key was pressed to stop
            try:
                evt = events.get(block=False, timeout=0.01)
                if evt.type == EventType.KEY and evt.action == 1 and evt.key == STOP_KEY:
                    minescript.echo("🛑 Stopped by pressing X.")
                    return
            except queue.Empty:
                pass

            # Simulate left-click (attack)
            player_press_attack(True)
            time.sleep(0.1)
            player_press_attack(False)

            # Cooldown before next attack (adjust as needed)
            time.sleep(0.5)
