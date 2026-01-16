import random
import json
import tkinter as tk
from PIL import Image, ImageTk

# ================== CONFIG ==================
FRAME_DELAY = 100     # ms per frame
SCALE = 4             # sprite size multiplier
MARGIN = 10           # distance from screen edge
TASKBAR_OFFSET = 40   # adjust if needed (40–60 typical)

idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]

event_number = random.randrange(1, 16)
cycle = 0
check = 0
x_offset = -40

SPRITE_PNG = r"C:\Users\user\Desktop\desktop-pet\Red Panda Sprite Sheet.png"
SPRITE_JSON = r"C:\Users\user\Desktop\desktop-pet\Red Panda Sprite Sheet.json"

# ================== WINDOW ==================
window = tk.Tk()
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "magenta")

label = tk.Label(window, bg="magenta", bd=0)
label.pack()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# ================== LOAD SPRITES ==================
with open(SPRITE_JSON, "r") as f:
    sprite_data = json.load(f)

sprite_sheet = Image.open(SPRITE_PNG).convert("RGBA")

def load_animation(tag):
    frames = []
    for name, data in sprite_data["frames"].items():
        if f"({tag})" in name:
            f = data["frame"]

            img = sprite_sheet.crop(
                (f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"])
            )

            img = img.resize(
                (f["w"] * SCALE, f["h"] * SCALE),
                Image.NEAREST
            )

            frames.append(ImageTk.PhotoImage(img))

    return frames

idle = load_animation("Idle")
idle2 = load_animation("Idle2")
sleep = load_animation("Sleep")
walk = load_animation("Movement")

# ================== STATE MACHINE ==================
def next_event(cycle, check, event_number):
    if event_number in idle_num:
        check = 0
    elif event_number == 5:
        check = 1
    elif event_number in walk_left:
        check = 4
    elif event_number in walk_right:
        check = 5
    elif event_number in sleep_num:
        check = 2
    elif event_number == 14:
        check = 3

    window.after(FRAME_DELAY, update, cycle, check, event_number)

def gif_work(cycle, frames, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        first_num, last_num = int(first_num), int(last_num)
        new_event = random.randrange(first_num, last_num + 1)
        return cycle, new_event
    return cycle, None

# ================== UPDATE LOOP ==================
def update(cycle, check, event_number):
    global x_offset

    if check == 0:
        frame = idle[cycle]
        cycle, new_event = gif_work(cycle, idle, 1, 9)

    elif check == 1:
        frame = idle2[cycle]
        cycle, new_event = gif_work(cycle, idle2, 10, 10)

    elif check == 2:
        frame = sleep[cycle]
        cycle, new_event = gif_work(cycle, sleep, 10, 15)

    elif check == 3:
        frame = idle[cycle]
        cycle, new_event = gif_work(cycle, idle, 1, 1)

    elif check == 4:
        frame = walk[cycle]
        cycle, new_event = gif_work(cycle, walk, 1, 9)
        x_offset -= 3

    elif check == 5:
        frame = walk[cycle]
        cycle, new_event = gif_work(cycle, walk, 1, 9)
        x_offset += 3

    else:
        frame = idle[0]
        new_event = None

    # Position bottom-right
    w = frame.width()
    h = frame.height()

    x_pos = screen_width - w - MARGIN + x_offset
    y_pos = screen_height - h - MARGIN - TASKBAR_OFFSET

    window.geometry(f"{w}x{h}+{x_pos}+{y_pos}")
    label.configure(image=frame)

    if new_event is not None:
        event_number = new_event

    window.after(FRAME_DELAY, next_event, cycle, check, event_number)

# ================== START ==================
window.after(100, update, cycle, check, event_number)
window.mainloop()
