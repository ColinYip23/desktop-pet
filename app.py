import random
import json
import tkinter as tk
from PIL import Image, ImageTk

# ================== CONFIG ==================
x = 1400
cycle = 0
check = 1

window = tk.Tk()
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "black")

idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]

event_number = random.randrange(1, 16)
SPRITE_PNG = r"C:\Users\user\Desktop\desktop-pet\Red Panda Sprite Sheet.png"
SPRITE_JSON = r"C:\Users\user\Desktop\desktop-pet\Red Panda Sprite Sheet.json"

FRAME_DELAY = 100  # ms per frame

# ================== LOAD SPRITES ==================
with open(SPRITE_JSON, "r") as f:
    sprite_data = json.load(f)

sprite_sheet = Image.open(SPRITE_PNG).convert("RGBA")

def load_animation(tag):
    frames = []
    for name, data in sprite_data["frames"].items():
        if tag in name:
            f = data["frame"]
            img = sprite_sheet.crop(
                (f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"])
            )
            frames.append(ImageTk.PhotoImage(img))
    return frames

idle = load_animation("Idle")
idle2 = load_animation("Idle2")
sleep = load_animation("Sleep")
walk = load_animation("Movement")

# ================== LOGIC ==================
def event(cycle, check, event_number, x):
    if event_number in idle_num:
        check = 0
        window.after(400, update, cycle, check, event_number, x)

    elif event_number == 5:
        check = 1
        window.after(100, update, cycle, check, event_number, x)

    elif event_number in walk_left:
        check = 4
        window.after(100, update, cycle, check, event_number, x)

    elif event_number in walk_right:
        check = 5
        window.after(100, update, cycle, check, event_number, x)

    elif event_number in sleep_num:
        check = 2
        window.after(1000, update, cycle, check, event_number, x)

    elif event_number == 14:
        check = 3
        window.after(100, update, cycle, check, event_number, x)

def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1)
    return cycle, event_number

def update(cycle, check, event_number, x):
    # Idle
    if check == 0:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)

    # Idle → Sleep
    elif check == 1:
        frame = idle2[cycle]
        cycle, event_number = gif_work(cycle, idle2, event_number, 10, 10)

    # Sleep
    elif check == 2:
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)

    # Sleep → Idle
    elif check == 3:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 1)

    # Walk Left
    elif check == 4:
        frame = walk[cycle]
        cycle, event_number = gif_work(cycle, walk, event_number, 1, 9)
        x -= 3

    # Walk Right
    elif check == 5:
        frame = walk[cycle]
        cycle, event_number = gif_work(cycle, walk, event_number, 1, 9)
        x += 3

    window.geometry(f"100x100+{x}+1050")
    label.configure(image=frame)
    window.after(FRAME_DELAY, event, cycle, check, event_number, x)

# ================== WINDOW ==================
label = tk.Label(window, bg="black", bd=0)
label.pack()

window.after(100, update, cycle, check, event_number, x)
window.mainloop()