# smart_auto_fish.py
import time
import minescript

def cast_line():
    minescript.press_key_bind("key.use", True)
    time.sleep(0.2)
    minescript.press_key_bind("key.use", False)
    minescript.echo("Line cast")

def reel_in():
    minescript.press_key_bind("key.use", True)
    time.sleep(0.2)
    minescript.press_key_bind("key.use", False)
    minescript.echo("Reeled in!")

def get_bobber():
    entities = minescript.entities(type="minecraft:fishing_bobber")
    for e in entities:
        if e.local:
            return e
    return None

def wait_for_bite(timeout=20, drop_threshold=0.2):
    start_time = time.time()
    last_y = None
    while time.time() - start_time < timeout:
        bobber = get_bobber()
        if not bobber:
            time.sleep(0.1)
            continue
        current_y = bobber.position.y
        if last_y is not None and last_y - current_y > drop_threshold:
            minescript.echo("Bite detected!")
            return True
        last_y = current_y
        time.sleep(0.1)
    minescript.echo("No bite detected in time.")
    return False

# Main loop
while True:
    cast_line()
    time.sleep(1)  # Let the bobber appear
    if wait_for_bite():
        reel_in()
    else:
        # Still reel in even if no bite, to reset
        reel_in()
    time.sleep(2)  # Pause before next cast
