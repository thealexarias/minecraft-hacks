from minescript import player, inventory, hotbar, hold, echo, stop, key
import time

def equip_pickaxe():
    """Finds any pickaxe in inventory and equips it to hotbar."""
    for i, item in enumerate(inventory()):
        if item and "pickaxe" in item.id:
            hotbar(i)  # moves that pickaxe into hand
            echo(f"Equipped {item.id}")
            return True
    echo("No pickaxe found!")
    return False

def main():
    echo("Auto-miner started! Press 'X' to stop.")
    if not equip_pickaxe():
        echo("No pickaxes in inventory. Stopping.")
        return

    hold("attack", True)  # start mining (like holding left-click)

    try:
        while True:
            # Stop script if X is pressed
            if key("x"):
                echo("Stopping script (X pressed).")
                break

            # check tool durability
            item = player().held_item
            if not item or "pickaxe" not in item.id:
                echo("Pickaxe broke, trying to equip another...")
                if not equip_pickaxe():
                    echo("No pickaxes left! Stopping.")
                    break

            time.sleep(0.1)  # don’t spam the game
    finally:
        hold("attack", False)  # stop mining when script exits
        echo("Auto-miner stopped.")

main()
