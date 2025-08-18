from minescript import player, hold, time, stop, inventory, hotbar, key

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
hold("attack", True)

try:
    while True:
        # If X is pressed → stop script
        if key("x"):
            hold("attack", False)
            stop()
            break

        # If no pickaxe equipped, try to swap to another
        if not player().held_item or "pickaxe" not in player().held_item.id:
            hold("attack", False)
            if not equip_pickaxe():
                print("Out of pickaxes! Stopping script.")
                break
            hold("attack", True)

        time.sleep(0.1)

except KeyboardInterrupt:
    hold("attack", False)
    stop()
