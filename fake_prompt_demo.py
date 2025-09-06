# stripped_fake_prompt_demo.py
# =========================================
# Educational demo of creating a fake login 
# window with tkinter in Python. 
# 
# ⚠️ Disclaimer: This is harmless. It does NOT 
# save or transmit passwords — it only shows 
# how GUI spoofing *could* be done.
# =========================================

from tkinter import *
from tkinter import ttk, messagebox
from getpass import getuser

# Create main window
window = Tk()
window.title("Windows Security")

# Remove title bar (no minimize/maximize/close buttons)
window.overrideredirect(True)

# Force fullscreen
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f"{width}x{height}+0+0")
window.attributes('-topmost', True)

# Get system username
username = getuser()

# Fonts
title_font = ("Segoe UI", 14, "bold")
text_font = ("Segoe UI", 10)

# Frame background (mimic Windows Security box)
frame = Frame(window, bg="#f0f0f0", bd=2, relief="groove")
frame.place(relx=0.5, rely=0.45, anchor="center", width=420, height=250)

# Title label
lbl = Label(frame, text="Windows Security", font=title_font, fg="#095BE2", bg="#f0f0f0")
lbl.pack(pady=(15, 5))

# Instruction text
lbl1 = Label(frame, text="Enter your password", font=text_font, fg="#232323", bg="#f0f0f0")
lbl1.pack()

# Username label
lbl2 = Label(frame, text=username, font=text_font, fg="#232323", bg="#f0f0f0")
lbl2.pack(pady=(8, 3))

# Password entry
txt = Entry(frame, width=24, font=("Segoe UI", 11), show="*")
txt.pack(pady=(3, 5))
txt.focus()

# Checkbox
chk1_state = IntVar(value=1)
chk1 = Checkbutton(frame, text="Remember me", variable=chk1_state, font=text_font, bg="#f0f0f0")
chk1.pack()

# Divider line
divider = Frame(frame, height=1, bg="#c0c0c0", relief="sunken")
divider.pack(fill="x", pady=(15, 10))

# Fake OK button
def ok_button():
    pw = txt.get().strip()
    if not pw:
        messagebox.showwarning("Windows Security", "Password cannot be empty.")
        return
    txt.delete(0, END)
    messagebox.showerror("Windows Security", "Access Denied (demo).")

# Exit with Cancel
def cancel_button():
    messagebox.showinfo("Windows Security", "Demo ended.")
    window.destroy()

# Button frame
btn_frame = Frame(frame, bg="#f0f0f0")
btn_frame.pack(pady=(0, 5))

btn = ttk.Button(btn_frame, text="OK", command=ok_button, width=10)
btn.grid(row=0, column=0, padx=5)

btn1 = ttk.Button(btn_frame, text="Cancel", command=cancel_button, width=10)
btn1.grid(row=0, column=1, padx=5)

# Start loop
window.mainloop()
