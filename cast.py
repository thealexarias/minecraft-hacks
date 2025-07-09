from minescript import player_press_use
import time

# Press right-click to cast the rod
player_press_use(True)

# Hold it briefly (simulate 0.1 seconds of use)
time.sleep(0.1)

# Release the button
player_press_use(False)
