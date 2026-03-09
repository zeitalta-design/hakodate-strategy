import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = "D:/ClaudeProjects/HakodateStrategy/hakodate_tourism_strategy/assets/img/projects"
LINER_DIR = OUT + "/experience-liner"

import os
os.makedirs(LINER_DIR, exist_ok=True)

try:
    font_sm = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 11)
except:
    font_sm = ImageFont.load_default()

def gradient_bg(w, h, c1, c2):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

def mountain_line(draw, base_y, w, h_max, color, seed_off=0):
    pts = [(0, base_y)]
    for x in range(0, w + 1, 8):
        hv = base_y - h_max * math.sin(x * math.pi / (w * 0.7)) * (1 + 0.25 * math.sin(x * 0.012 + seed_off))
        pts.append((x, int(hv)))
    pts.extend([(w, base_y + 200), (0, base_y + 200)])
    draw.polygon(pts, fill=color)

# ==============================================================
# HERO: High-value sightseeing train concept (exterior side view)
# ==============================================================
img = gradient_bg(1200, 800, (180, 200, 220), (220, 230, 240))
draw = ImageDraw.Draw(img)

# Mountain backdrop
mountain_line(draw, 250, 1200, 130, (170, 185, 205))

# Ground / tracks
draw.rectangle([0, 520, 1200, 800], fill=(190, 195, 185))
# Rails
draw.line([(0, 530), (1200, 530)], fill=(140, 140, 140), width=3)
draw.line([(0, 545), (1200, 545)], fill=(140, 140, 140), width=3)
# Ties
for x in range(0, 1200, 30):
    draw.rectangle([x, 528, x+15, 548], fill=(160, 155, 145))

# Train body - sleek, elegant design
train_left, train_right = 150, 1050
train_top, train_bottom = 340, 520

# Main body
draw.rounded_rectangle(
    [train_left, train_top, train_right, train_bottom],
    radius=20, fill=(50, 30, 25)  # Deep burgundy-brown
)

# Gold accent stripe
draw.rectangle([train_left, 440, train_right, 455], fill=(180, 150, 80))
draw.rectangle([train_left, 460, train_right, 465], fill=(200, 170, 90))

# Windows - panoramic style
for wx in range(train_left + 40, train_right - 40, 80):
    # Large panoramic windows
    draw.rounded_rectangle(
        [wx, train_top + 30, wx + 60, train_top + 90],
        radius=8, fill=(160, 200, 230)
    )
    # Window reflection
    draw.line([(wx + 10, train_top + 35), (wx + 25, train_top + 85)], fill=(180, 215, 240), width=2)

# Front nose (left side = front)
nose_pts = [
    (train_left, train_top),
    (train_left - 60, train_top + 60),
    (train_left - 70, 480),
    (train_left, train_bottom),
]
draw.polygon(nose_pts, fill=(50, 30, 25))
# Front window
draw.polygon([
    (train_left - 10, train_top + 25),
    (train_left - 50, train_top + 55),
    (train_left - 55, 470),
    (train_left - 5, 440),
], fill=(140, 185, 220))

# Gold stripe on nose
draw.line([(train_left - 65, 450), (train_left, 440)], fill=(180, 150, 80), width=4)

# Roof detail
draw.rounded_rectangle(
    [train_left - 30, train_top - 5, train_right + 5, train_top + 5],
    radius=5, fill=(40, 25, 20)
)

# Door outlines
for dx in [train_left + 200, train_left + 500]:
    draw.rectangle([dx, train_top + 40, dx + 35, train_bottom - 10], outline=(70, 50, 40), width=2)

# Platform hint
draw.rectangle([0, 550, 1200, 580], fill=(180, 180, 175))

# Sky elements - soft clouds
random.seed(42)
for _ in range(5):
    cx = random.randint(100, 1100)
    cy = random.randint(50, 180)
    rw = random.randint(60, 120)
    rh = random.randint(20, 40)
    draw.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(210, 220, 232))

img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
img.save(f"{OUT}/liner_hero_concept.jpg", "JPEG", quality=90)
print("1/5 liner_hero_concept.jpg")

# ==============================================================
# Interior images - 4 concept images (1200x800 each)
# ==============================================================

# --- 1. Semi-compartment ---
img = gradient_bg(1200, 800, (60, 45, 35), (85, 65, 50))
draw = ImageDraw.Draw(img)

# Warm wood-paneled walls
for y in range(0, 800, 3):
    shade = random.randint(-5, 5)
    draw.line([(0, y), (1200, y)], fill=(75 + shade, 58 + shade, 42 + shade))

# Partition walls (semi-compartment dividers)
for px in [300, 600, 900]:
    draw.rectangle([px - 5, 100, px + 5, 700], fill=(90, 70, 50))
    # Frosted glass upper
    draw.rectangle([px - 3, 100, px + 3, 350], fill=(140, 155, 160))

# Seating areas between partitions
for sx in [150, 450, 750, 1050]:
    # Plush seat
    draw.rounded_rectangle([sx - 80, 450, sx + 80, 650], radius=15, fill=(120, 40, 35))
    # Seat back
    draw.rounded_rectangle([sx - 70, 300, sx + 70, 460], radius=12, fill=(130, 45, 38))
    # Cushion highlight
    draw.rounded_rectangle([sx - 60, 320, sx + 60, 440], radius=8, fill=(140, 55, 45))
    # Small table
    draw.rounded_rectangle([sx - 40, 430, sx + 40, 450], radius=4, fill=(100, 80, 55))

# Warm ceiling lights
for lx in range(100, 1200, 200):
    for r in range(40, 0, -2):
        c = (min(255, 90 + r * 2), min(255, 75 + r), min(255, 50 + r // 2))
        draw.ellipse([lx - r, 30 - r // 3, lx + r, 30 + r // 3], fill=c)

# Window with scenery hint
for wx in [0, 1100]:
    draw.rectangle([wx, 150, wx + 100, 400], fill=(140, 180, 210))

img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img.save(f"{LINER_DIR}/experience-liner_semi_compartment.jpg", "JPEG", quality=92)
print("2/5 semi_compartment.jpg")

# --- 2. Premium seats ---
img = gradient_bg(1200, 800, (50, 50, 60), (75, 70, 80))
draw = ImageDraw.Draw(img)

# Floor
draw.rectangle([0, 550, 1200, 800], fill=(60, 55, 50))
# Carpet pattern
for x in range(0, 1200, 20):
    for y in range(560, 800, 20):
        if (x + y) % 40 == 0:
            draw.rectangle([x, y, x + 10, y + 10], fill=(65, 58, 52))

# Rows of premium seats (2+1 configuration)
for row_y in [350, 550]:
    for sx in [200, 400, 750]:
        # Seat shell
        w = 120 if sx < 700 else 140
        draw.rounded_rectangle([sx - w // 2, row_y - 150, sx + w // 2, row_y], radius=12, fill=(100, 35, 30))
        # Headrest
        draw.rounded_rectangle([sx - w // 2 + 15, row_y - 170, sx + w // 2 - 15, row_y - 130], radius=8, fill=(115, 45, 38))
        # Armrests
        draw.rectangle([sx - w // 2 - 5, row_y - 50, sx - w // 2 + 10, row_y + 5], fill=(80, 65, 50))
        draw.rectangle([sx + w // 2 - 10, row_y - 50, sx + w // 2 + 5, row_y + 5], fill=(80, 65, 50))

# Panoramic windows
draw.rectangle([0, 80, 1200, 280], fill=(130, 170, 210))
# Window frame
draw.rectangle([0, 78, 1200, 85], fill=(55, 55, 65))
draw.rectangle([0, 275, 1200, 283], fill=(55, 55, 65))
# Window dividers
for wx in range(0, 1200, 300):
    draw.rectangle([wx, 80, wx + 8, 280], fill=(55, 55, 65))

# Overhead lighting
draw.rectangle([0, 0, 1200, 60], fill=(65, 60, 70))
for lx in range(100, 1200, 150):
    draw.rounded_rectangle([lx - 30, 45, lx + 30, 60], radius=4, fill=(180, 170, 150))

img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
img.save(f"{LINER_DIR}/experience-liner_seats.jpg", "JPEG", quality=92)
print("3/5 seats.jpg")

# --- 3. Lounge + Bar + Shop ---
img = gradient_bg(1200, 800, (45, 40, 50), (65, 55, 65))
draw = ImageDraw.Draw(img)

# Bar counter (long, central)
draw.rounded_rectangle([200, 350, 1000, 500], radius=10, fill=(80, 60, 45))
# Counter top
draw.rounded_rectangle([195, 345, 1005, 365], radius=6, fill=(95, 75, 55))
# Counter front panel - wood
for y in range(370, 500, 3):
    shade = random.randint(-3, 3)
    draw.line([(205, y), (995, y)], fill=(75 + shade, 55 + shade, 40 + shade))

# Bar stools
for bx in range(280, 950, 120):
    # Stool seat
    draw.ellipse([bx - 20, 500, bx + 20, 520], fill=(100, 40, 35))
    # Stool leg
    draw.line([(bx, 520), (bx, 580)], fill=(70, 70, 70), width=3)
    draw.line([(bx - 15, 580), (bx + 15, 580)], fill=(70, 70, 70), width=3)

# Shelf behind bar (bottles/goods)
draw.rectangle([250, 150, 950, 330], fill=(55, 45, 55))
for shelf_y in [180, 250]:
    draw.line([(260, shelf_y), (940, shelf_y)], fill=(75, 60, 50), width=3)
    # Bottles / items
    for bx in range(280, 930, 40):
        h = random.randint(30, 55)
        w = random.randint(8, 16)
        colors = [(140, 100, 60), (80, 120, 80), (160, 80, 60), (100, 80, 120), (180, 160, 80)]
        c = random.choice(colors)
        draw.rounded_rectangle([bx - w, shelf_y - h, bx + w, shelf_y - 2], radius=3, fill=c)

# Display cases on sides (shop items)
for dx, dw in [(50, 130), (1020, 130)]:
    draw.rounded_rectangle([dx, 200, dx + dw, 550], radius=8, fill=(70, 60, 70))
    draw.rounded_rectangle([dx + 5, 205, dx + dw - 5, 545], radius=6, fill=(90, 85, 95))
    # Items
    for iy in range(230, 530, 50):
        draw.rounded_rectangle([dx + 15, iy, dx + dw - 15, iy + 35], radius=4, fill=(110, 95, 80))

# Warm pendant lights
for lx in [400, 600, 800]:
    # Cord
    draw.line([(lx, 0), (lx, 100)], fill=(60, 55, 50), width=2)
    # Shade
    for r in range(30, 0, -1):
        c = (min(255, 180 + r * 2), min(255, 140 + r), min(255, 80 + r // 2))
        draw.ellipse([lx - r, 90 - r // 2, lx + r, 90 + r // 2], fill=c)

# Floor
draw.rectangle([0, 600, 1200, 800], fill=(50, 45, 40))

img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img.save(f"{LINER_DIR}/experience-liner_lounge.jpg", "JPEG", quality=92)
print("4/5 lounge.jpg")

# --- 4. Observation deck ---
img = gradient_bg(1200, 800, (30, 50, 80), (80, 120, 160))
draw = ImageDraw.Draw(img)

# Huge front panoramic window
# Sky and landscape through window
draw.rectangle([100, 50, 1100, 500], fill=(140, 180, 220))
# Mountains through window
for mx in range(100, 1101, 5):
    h = 400 - 100 * math.sin((mx - 100) * math.pi / 500) * (1 + 0.3 * math.sin(mx * 0.02))
    draw.line([(mx, int(h)), (mx, 500)], fill=(100, 140, 100))

# Tracks converging to vanishing point
vx, vy = 600, 300
for offset in [-200, -150, -100, 100, 150, 200]:
    draw.line([(600 + offset * 3, 500), (vx + offset // 4, vy)], fill=(120, 120, 110), width=2)

# Window frame
draw.rounded_rectangle([95, 45, 1105, 505], radius=15, outline=(50, 50, 60), width=8)

# Interior frame / observation deck structure
draw.rectangle([0, 500, 1200, 800], fill=(40, 40, 50))

# Railing in front of window
draw.rectangle([120, 490, 1080, 510], fill=(60, 60, 70))
# Glass railing
draw.rectangle([120, 460, 1080, 490], fill=(80, 100, 130))

# Standing/seating area
for sx in [250, 500, 750]:
    draw.rounded_rectangle([sx - 40, 550, sx + 40, 650], radius=8, fill=(80, 35, 30))

# Side ambient lights
for ly in range(100, 500, 60):
    draw.line([(90, ly), (90, ly + 30)], fill=(100, 130, 170), width=3)
    draw.line([(1110, ly), (1110, ly + 30)], fill=(100, 130, 170), width=3)

# Ceiling structure
draw.rectangle([0, 0, 1200, 40], fill=(35, 35, 45))
for lx in range(200, 1100, 200):
    draw.rounded_rectangle([lx - 20, 30, lx + 20, 42], radius=3, fill=(120, 130, 150))

# Floor reflection
for y in range(650, 800, 2):
    t = (y - 650) / 150
    c = (int(40 + 10 * t), int(40 + 10 * t), int(50 + 10 * t))
    draw.line([(0, y), (1200, y)], fill=c)

img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img.save(f"{LINER_DIR}/experience-liner_observation.jpg", "JPEG", quality=92)
print("5/5 observation.jpg")

print("\nAll Experience Liner images generated!")
