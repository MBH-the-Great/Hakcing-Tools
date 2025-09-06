# stripped_keylogger_demo.py
# =========================================
# Educational demo of using pynput to capture
# keyboard input in Python. 
# 
# ⚠️ Disclaimer: This script only prints keys
# to the console. It does NOT log, save, or 
# persist in the system.
# =========================================

from pynput.keyboard import Listener

def on_press(key):
    try:
        print(f"Key pressed: {key.char}")
    except AttributeError:
        print(f"Special key pressed: {key}")

def on_release(key):
    # Stop if ESC is pressed
    if str(key) == 'Key.esc':
        print("Exiting...")
        return False

# Start listener (press ESC to stop)
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
