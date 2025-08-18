from minescript import player, time, stop, inventory, hotbar, key, control

def equip_pickaxe():
    """Finds a pickaxe in inventory and equips it in the hotbar."""
    for i, item in enumerate(inventory()):
        if item and "pickaxe" in item.id:
            hotbar(i)   # put pickaxe in hand
            return True
    return False

# Equip a pickaxe before starting
if not equip_pickaxe():
    print("No pickaxes found! Exiting script.")
    stop()

# Start mining
control.hold("attack", True)

try:
    while True:
        # If X is pressed → stop script
        if key("x"):
            control.hold("attack", False)
            stop()
            break

        # If no pickaxe equipped, try to swap to another
        if not player().held_item or "pickaxe" not in player().held_item.id:
            control.hold("attack", False)
            if not equip_pickaxe():
                print("Out of pickaxes! Stopping script.")
                break
            control.hold("attack", True)

        time.sleep(0.1)

except KeyboardInterrupt:
    control.hold("attack", False)
    stop()
