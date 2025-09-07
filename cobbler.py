import minescript
import time
import queue
from minescript import EventQueue, EventType, player_press_attack

STOP_KEY = 88  # X key

def auto_mine_cobblestone():
    minescript.echo("⛏️ Auto-mining started. Press X to stop.")

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

            # Hold down left-click (attack/mine)
            player_press_attack(True)
            time.sleep(0.2)   # keep holding briefly
            player_press_attack(False)
            time.sleep(0.05)  # short pause before next swing

auto_mine_cobblestone()
