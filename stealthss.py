# stealthss.py
# =========================================
# Educational demo of using pyautogui to 
# capture screenshots in Python. 
#
# ⚠️ Disclaimer: This script is harmless — 
# it only takes a screenshot when you 
# manually click the button.
# =========================================

import pyautogui
import os
import datetime
from tkinter import Tk, Button, messagebox

# Folder where screenshots will be saved
folder_path = os.path.join(os.getcwd(), "screenshots")
os.makedirs(folder_path, exist_ok=True)

# Function to capture screenshot
def take_screenshot():
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(folder_path, f"ss_{now}.png")

    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

    messagebox.showinfo("StealthSS Demo", f"Screenshot saved:\n{filename}")

# Simple GUI with a button
root = Tk()
root.title("StealthSS Demo")

btn = Button(root, text="Take Screenshot", command=take_screenshot, width=20, height=2)
btn.pack(padx=20, pady=20)

root.mainloop()
