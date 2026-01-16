import random
import json
import tkinter as tk
from PIL import Image, ImageTk

# ================== CONFIG ==================
FRAME_DELAY = 100
SCALE = 4
MARGIN = 10
TASKBAR_OFFSET = 38

# Panda states
PANDA_IDLE = 0
PANDA_IDLE2 = 1
PANDA_SLEEP = 2
PANDA_WAKE = 3
PANDA_WALK_L = 4
PANDA_WALK_R = 5

# Koala states
KOALA_IDLE = 0
KOALA_WALK = 1
KOALA_CLIMB = 2
KOALA_EAT = 3

# Initial states
panda_state = PANDA_IDLE
panda_cycle = 0
panda_x_offset = -40

koala_state = KOALA_IDLE
koala_cycle = 0

SPRITE_PNG = r"C:\Users\user\Desktop\desktop-pet\Red Panda Sprite Sheet.png"
SPRITE_JSON = r"C:\Users\user\Desktop\desktop-pet\Red Panda Sprite Sheet.json"
KOALA_PNG = r"C:\Users\user\Desktop\desktop-pet\Koala Sprite Sheet.png"
KOALA_JSON = r"C:\Users\user\Desktop\desktop-pet\Koala Sprite Sheet.json"

# ================== WINDOW ==================
window = tk.Tk()
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "magenta")

label = tk.Label(window, bg="magenta", bd=0)
label.pack()

koala_window = tk.Toplevel()
koala_window.overrideredirect(True)
koala_window.wm_attributes("-transparentcolor", "magenta")

koala_label = tk.Label(koala_window, bg="magenta", bd=0)
koala_label.pack()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# ================== LOAD DATA ==================
with open(SPRITE_JSON) as f:
    panda_data = json.load(f)

with open(KOALA_JSON) as f:
    koala_data = json.load(f)

panda_sheet = Image.open(SPRITE_PNG).convert("RGBA")
koala_sheet = Image.open(KOALA_PNG).convert("RGBA")

def load_animation(sheet, data, tag):
    frames = []
    for name, info in data["frames"].items():
        if f"({tag})" in name:
            f = info["frame"]
            img = sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
            img = img.resize((f["w"] * SCALE, f["h"] * SCALE), Image.NEAREST)
            frames.append(ImageTk.PhotoImage(img))
    return frames

# Panda animations
panda_idle = load_animation(panda_sheet, panda_data, "Idle")
panda_idle2 = load_animation(panda_sheet, panda_data, "Idle2")
panda_sleep = load_animation(panda_sheet, panda_data, "Sleep")
panda_walk = load_animation(panda_sheet, panda_data, "Movement")

# Koala animations
koala_idle = load_animation(koala_sheet, koala_data, "Idle")
koala_walk = load_animation(koala_sheet, koala_data, "Movement")
koala_climb = load_animation(koala_sheet, koala_data, "Climb")
koala_eat = load_animation(koala_sheet, koala_data, "Eat")

# ================== PANDA UPDATE LOOP ==================
def update_panda():
    global panda_cycle, panda_state, panda_x_offset

    if panda_state == PANDA_IDLE:
        frames = panda_idle
    elif panda_state == PANDA_IDLE2:
        frames = panda_idle2
    elif panda_state == PANDA_SLEEP:
        frames = panda_sleep
    elif panda_state == PANDA_WAKE:
        frames = panda_idle
    elif panda_state in (PANDA_WALK_L, PANDA_WALK_R):
        frames = panda_walk

        step = -3 if panda_state == PANDA_WALK_L else 3
        panda_x_offset += step
    else:
        frames = panda_idle

    frame = frames[panda_cycle]
    label.configure(image=frame)
    label.image = frame

    panda_cycle += 1
    if panda_cycle >= len(frames):
        panda_cycle = 0
        panda_state = random.choice([
            PANDA_IDLE, PANDA_IDLE2,
            PANDA_SLEEP, PANDA_WAKE,
            PANDA_WALK_L, PANDA_WALK_R
        ])

    w = frame.width()
    h = frame.height()

    panda_x = screen_width - w - MARGIN + panda_x_offset

    # -------- Clamp panda to screen --------
    min_x = 0
    max_x = screen_width - w

    if panda_x < min_x:
        panda_x = min_x
        panda_x_offset = panda_x - (screen_width - w - MARGIN)

    elif panda_x > max_x:
        panda_x = max_x
        panda_x_offset = panda_x - (screen_width - w - MARGIN)


    panda_y = screen_height - h - MARGIN - TASKBAR_OFFSET

    window.geometry(f"{w}x{h}+{panda_x}+{panda_y}")

    window.after(FRAME_DELAY, update_panda)

# ================== KOALA UPDATE LOOP ==================
def update_koala():
    global koala_cycle, koala_state

    if koala_state == KOALA_IDLE:
        frames = koala_idle
    elif koala_state == KOALA_WALK:
        frames = koala_walk
    elif koala_state == KOALA_CLIMB:
        frames = koala_climb
    elif koala_state == KOALA_EAT:
        frames = koala_eat
    else:
        frames = koala_idle

    frame = frames[koala_cycle]
    koala_label.configure(image=frame)
    koala_label.image = frame

    koala_cycle = (koala_cycle + 1) % len(frames)

    panda_w = panda_idle[0].width()
    panda_h = panda_idle[0].height()

    panda_x = screen_width - panda_w - MARGIN + panda_x_offset
    panda_y = screen_height - panda_h - MARGIN - TASKBAR_OFFSET

    koala_x = panda_x - frame.width() - 60
    koala_y = panda_y + 40

    koala_window.geometry(f"{frame.width()}x{frame.height()}+{koala_x}+{koala_y}")

    if random.random() < 0.01:
        koala_state = random.choice([KOALA_IDLE, KOALA_WALK, KOALA_CLIMB, KOALA_EAT])
        koala_cycle = 0

    window.after(FRAME_DELAY, update_koala)

# ================== START ==================
window.after(100, update_panda)
window.after(100, update_koala)
window.mainloop()