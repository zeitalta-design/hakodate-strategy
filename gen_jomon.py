import math
import random
from PIL import Image, ImageDraw, ImageFilter

OUT = "D:/ClaudeProjects/HakodateStrategy/hakodate_tourism_strategy/assets/img/projects"

def gradient_bg(w, h, colors):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * t)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * t)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

def jomon_pattern_band(draw, y_start, w, band_h, color, seed=0):
    """Draw a horizontal band of Jomon rope-pattern inspired marks."""
    random.seed(seed)
    for x in range(0, w, 12):
        for y_off in range(0, band_h, 8):
            if random.random() > 0.3:
                y = y_start + y_off
                # Rope twist marks
                draw.arc([x, y, x+8, y+6], 0, 180, fill=color, width=1)
                draw.arc([x+4, y+2, x+12, y+8], 180, 360, fill=color, width=1)

def draw_pottery(draw, cx, base_y, h, w, body_color, pattern_color):
    """Draw a Jomon-style pottery vessel silhouette."""
    # Vessel body - wider at top, narrowing at base
    top_w = w
    mid_w = w * 0.85
    base_w = w * 0.4
    neck_w = w * 0.7

    # Build vessel outline
    pts = []
    # Left side from base to top
    for t in [x / 20 for x in range(21)]:
        y = base_y - h * t
        if t < 0.15:
            x_off = base_w + (mid_w - base_w) * (t / 0.15)
        elif t < 0.6:
            x_off = mid_w + (top_w - mid_w) * ((t - 0.15) / 0.45)
        elif t < 0.75:
            x_off = top_w - (top_w - neck_w) * ((t - 0.6) / 0.15)
        else:
            x_off = neck_w + (top_w * 1.1 - neck_w) * ((t - 0.75) / 0.25)
        pts.append((cx - x_off, y))

    # Right side from top to base
    for t in [x / 20 for x in range(20, -1, -1)]:
        y = base_y - h * t
        if t < 0.15:
            x_off = base_w + (mid_w - base_w) * (t / 0.15)
        elif t < 0.6:
            x_off = mid_w + (top_w - mid_w) * ((t - 0.15) / 0.45)
        elif t < 0.75:
            x_off = top_w - (top_w - neck_w) * ((t - 0.6) / 0.15)
        else:
            x_off = neck_w + (top_w * 1.1 - neck_w) * ((t - 0.75) / 0.25)
        pts.append((cx + x_off, y))

    draw.polygon(pts, fill=body_color, outline=pattern_color, width=2)

    # Jomon rope pattern bands
    for band_y in range(int(base_y - h * 0.3), int(base_y - h * 0.85), int(h * 0.12)):
        band_left = cx - mid_w * 0.7
        band_right = cx + mid_w * 0.7
        for x in range(int(band_left), int(band_right), 10):
            draw.arc([x, band_y, x+8, band_y+6], 0, 180, fill=pattern_color, width=1)

    # Flame-style rim decorations (kaen-doki inspired)
    rim_y = base_y - h
    for i in range(5):
        px = cx - top_w * 0.8 + i * (top_w * 1.6 / 4)
        flame_h = h * 0.12 * (1 + 0.5 * math.sin(i * 1.2))
        draw.polygon([
            (px - 8, rim_y),
            (px, rim_y - flame_h),
            (px + 8, rim_y),
        ], fill=body_color, outline=pattern_color, width=2)

def mountain_line(draw, base_y, w, h_max, color, seed_off=0):
    pts = [(0, base_y)]
    for x in range(0, w + 1, 8):
        hv = base_y - h_max * math.sin(x * math.pi / (w * 0.7)) * (1 + 0.25 * math.sin(x * 0.012 + seed_off))
        pts.append((x, int(hv)))
    pts.extend([(w, base_y + 200), (0, base_y + 200)])
    draw.polygon(pts, fill=color)


# ========================================
# 1. Pottery Workshop (1200x800)
# ========================================
img = gradient_bg(1200, 800, [(180, 160, 140), (220, 200, 175)])
draw = ImageDraw.Draw(img)

# Warm workshop environment - wooden table surface
draw.rectangle([0, 500, 1200, 800], fill=(160, 130, 95))
# Table wood grain
random.seed(55)
for i in range(30):
    y = 500 + random.randint(0, 290)
    draw.line([(0, y), (1200, y)], fill=(150, 120, 85), width=1)

# Central pottery being shaped - large vessel
draw_pottery(draw, 600, 480, 220, 90, (165, 120, 75), (130, 90, 55))

# Smaller finished pots on sides
draw_pottery(draw, 250, 500, 140, 55, (175, 130, 80), (140, 100, 60))
draw_pottery(draw, 950, 510, 130, 50, (170, 125, 78), (135, 95, 58))

# Clay/tools on table
for _ in range(15):
    x = random.randint(100, 1100)
    y = random.randint(520, 620)
    r = random.randint(3, 8)
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(145, 110, 75))

# Hands suggestion (abstract shapes suggesting work)
# Left hand area
draw.ellipse([520, 400, 570, 460], fill=(210, 175, 145), outline=(190, 155, 125))
draw.ellipse([540, 380, 580, 430], fill=(210, 175, 145), outline=(190, 155, 125))
# Right hand area
draw.ellipse([630, 400, 680, 460], fill=(210, 175, 145), outline=(190, 155, 125))
draw.ellipse([620, 380, 660, 430], fill=(210, 175, 145), outline=(190, 155, 125))

# Warm lighting from above
for r in range(300, 0, -5):
    alpha = max(0, min(40, int(40 * (1 - r / 300))))
    draw.ellipse([600-r, 50-r//2, 600+r, 50+r//2], fill=(220 + alpha//4, 200 + alpha//4, 170))

# Subtle background - wall
draw.rectangle([0, 0, 1200, 200], fill=(200, 185, 165))

# Shelves with pottery in background
for shelf_y in [150, 280]:
    draw.line([(50, shelf_y), (1150, shelf_y)], fill=(140, 115, 85), width=3)
    for px in range(100, 1100, 120):
        pot_h = random.randint(30, 60)
        pot_w = random.randint(15, 30)
        draw_pottery(draw, px, shelf_y - 2, pot_h, pot_w,
                     (160 + random.randint(-10, 10), 115 + random.randint(-10, 10), 70 + random.randint(-10, 10)),
                     (130, 90, 55))

img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img.save(f"{OUT}/jomon_pottery_workshop.jpg", "JPEG", quality=88)
print("1/3 jomon_pottery_workshop.jpg")


# ========================================
# 2. Jomon Food Course (1200x800)
# ========================================
img = gradient_bg(1200, 800, [(60, 50, 40), (90, 75, 55)])
draw = ImageDraw.Draw(img)

# Dark wood table
draw.rectangle([0, 200, 1200, 800], fill=(55, 40, 30))
random.seed(33)
for i in range(40):
    y = 200 + random.randint(0, 590)
    draw.line([(0, y), (1200, y)], fill=(50, 36, 26), width=1)

# Plates/bowls - ceramic earthenware style
def draw_plate(draw, cx, cy, rx, ry, plate_color, rim_color):
    draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=plate_color, outline=rim_color, width=2)
    draw.ellipse([cx-rx+8, cy-ry+4, cx+rx-8, cy+ry-4], outline=rim_color, width=1)

def draw_bowl(draw, cx, cy, w, h, color, rim):
    pts = [(cx-w, cy), (cx-w*0.8, cy+h), (cx+w*0.8, cy+h), (cx+w, cy)]
    draw.polygon(pts, fill=color, outline=rim, width=2)
    draw.arc([cx-w, cy-h*0.3, cx+w, cy+h*0.3], 0, 180, fill=rim, width=2)

# Main plate - center
draw_plate(draw, 600, 450, 160, 80, (140, 115, 80), (120, 95, 65))
# Food items on main plate - salmon fillet shapes
draw.polygon([(520, 430), (560, 410), (680, 420), (660, 450)], fill=(200, 120, 90))
# Greens / mountain vegetables
for _ in range(8):
    x = 550 + random.randint(0, 100)
    y = 440 + random.randint(0, 30)
    draw.ellipse([x-6, y-3, x+6, y+3], fill=(80, 140, 60))

# Bowl - top left - soup/stew
draw_bowl(draw, 300, 350, 80, 50, (150, 120, 85), (130, 100, 70))
# Stew/soup fill
draw.ellipse([230, 340, 370, 380], fill=(130, 90, 50))
# Steam wisps
for i in range(3):
    x = 280 + i * 20
    for y in range(310, 280, -3):
        off = 5 * math.sin((y + i * 10) * 0.2)
        draw.point((int(x + off), y), fill=(180, 170, 160))

# Small plate - top right - chestnuts/nuts
draw_plate(draw, 900, 360, 90, 50, (145, 118, 82), (125, 98, 68))
for _ in range(6):
    nx = 870 + random.randint(0, 60)
    ny = 350 + random.randint(0, 20)
    draw.ellipse([nx-8, ny-6, nx+8, ny+6], fill=(120, 80, 40))

# Small bowl - bottom left - shellfish
draw_bowl(draw, 250, 550, 70, 40, (148, 122, 85), (128, 102, 70))
for _ in range(4):
    sx = 220 + random.randint(0, 60)
    sy = 540 + random.randint(0, 20)
    draw.ellipse([sx-10, sy-5, sx+10, sy+5], fill=(180, 160, 140))
    draw.arc([sx-10, sy-5, sx+10, sy+5], 0, 180, fill=(160, 140, 120), width=1)

# Chopsticks
draw.line([(680, 500), (780, 380)], fill=(100, 70, 40), width=3)
draw.line([(690, 505), (790, 385)], fill=(100, 70, 40), width=3)

# Pottery cup - bottom right
draw_pottery(draw, 920, 580, 70, 30, (155, 118, 78), (130, 95, 60))

# Jomon-pattern placemat/cloth hints
for y in range(600, 660, 8):
    for x in range(400, 800, 12):
        draw.arc([x, y, x+8, y+6], 0, 180, fill=(70, 55, 40), width=1)

# Ambient warm lighting
for r in range(400, 0, -8):
    t = r / 400
    draw.ellipse([600 - r, 400 - r//2, 600 + r, 400 + r//2],
                 outline=(int(30 * (1-t)), int(20 * (1-t)), int(10 * (1-t))))

img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
img.save(f"{OUT}/jomon_food_course.jpg", "JPEG", quality=88)
print("2/3 jomon_food_course.jpg")


# ========================================
# 3. Night Projection (1200x800)
# ========================================
img = Image.new("RGB", (1200, 800), (5, 5, 15))
draw = ImageDraw.Draw(img)

# Starry sky
random.seed(88)
for _ in range(200):
    x = random.randint(0, 1200)
    y = random.randint(0, 350)
    bv = random.randint(80, 220)
    r = random.choice([1, 1, 1, 2])
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(bv, bv, min(255, bv+30)))

# Mountain silhouette (Hakodate-yama)
mountain_line(draw, 350, 1200, 120, (10, 10, 25), seed_off=0.5)

# Ground plane - archaeological site
draw.rectangle([0, 550, 1200, 800], fill=(15, 12, 8))
# Ground texture
for _ in range(100):
    x = random.randint(0, 1200)
    y = random.randint(560, 790)
    r = random.randint(1, 3)
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(25, 20, 15))

# Pit dwelling silhouettes
def draw_pit_dwelling(draw, cx, base_y, w, h, color):
    pts = [(cx - w, base_y), (cx - w * 0.3, base_y - h * 0.7),
           (cx, base_y - h), (cx + w * 0.3, base_y - h * 0.7),
           (cx + w, base_y)]
    draw.polygon(pts, fill=color, outline=(max(0, color[0]+20), max(0, color[1]+20), max(0, color[2]+20)), width=1)
    # Door opening
    draw.rectangle([cx - w * 0.15, base_y - h * 0.35, cx + w * 0.15, base_y], fill=(max(0, color[0]-5), max(0, color[1]-5), max(0, color[2]-5)))

# Multiple dwellings
draw_pit_dwelling(draw, 350, 570, 100, 80, (25, 20, 15))
draw_pit_dwelling(draw, 600, 560, 120, 95, (28, 22, 16))
draw_pit_dwelling(draw, 850, 575, 90, 75, (24, 19, 14))

# Projection mapping effect - glowing Jomon patterns on dwellings
projection_colors = [(200, 120, 50), (180, 80, 30), (220, 160, 60), (160, 100, 200)]

# Center dwelling - main projection
cx_proj, cy_proj = 600, 510
# Glowing spiral pattern (Jomon motif)
for t_val in [x * 0.1 for x in range(100)]:
    r = 5 + t_val * 6
    angle = t_val * 1.5
    px = cx_proj + r * math.cos(angle)
    py = cy_proj + r * math.sin(angle) * 0.5
    if 480 < py < 560 and 490 < px < 710:
        for gr in range(4, 0, -1):
            c = (min(255, 200 + gr*10), min(255, 120 + gr*10), min(255, 50 + gr*5))
            draw.ellipse([px-gr, py-gr, px+gr, py+gr], fill=c)

# Left dwelling projection - concentric circles
for ring_r in range(10, 60, 8):
    draw.ellipse([350-ring_r, 530-ring_r*0.5, 350+ring_r, 530+ring_r*0.5],
                 outline=(180, 80, min(255, 30 + ring_r*2)), width=1)

# Right dwelling projection - wave pattern
for wave_x in range(780, 920, 6):
    wave_y = 535 + 15 * math.sin(wave_x * 0.08)
    for gr in range(3, 0, -1):
        draw.ellipse([wave_x-gr, wave_y-gr, wave_x+gr, wave_y+gr],
                     fill=(220, min(255, 160 + gr*10), 60))

# Ground light beams (upward projection from ground fixtures)
for beam_x in [200, 450, 750, 1000]:
    for w in range(12, 0, -1):
        alpha_r = w * 4
        alpha_g = w * 3
        draw.line([(beam_x, 700), (beam_x - 30, 400)], fill=(alpha_r, alpha_g, alpha_r + 5), width=w)
        draw.line([(beam_x, 700), (beam_x + 30, 400)], fill=(alpha_r, alpha_g, alpha_r + 5), width=w)

# Floating Jomon pattern particles
for _ in range(60):
    px = random.randint(100, 1100)
    py = random.randint(380, 600)
    size = random.randint(2, 6)
    color = random.choice(projection_colors)
    for gr in range(size, 0, -1):
        fade = tuple(max(0, min(255, int(v * gr / size))) for v in color)
        draw.ellipse([px-gr, py-gr, px+gr, py+gr], fill=fade)

# Warm glow around dwellings
for dwelling_cx in [350, 600, 850]:
    for r in range(80, 0, -2):
        t = r / 80
        c = (int(30 * (1-t)), int(15 * (1-t)), int(5 * (1-t)))
        draw.ellipse([dwelling_cx-r, 530-r//2, dwelling_cx+r, 530+r//2], outline=c)

img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
img.save(f"{OUT}/jomon_night_projection.jpg", "JPEG", quality=88)
print("3/3 jomon_night_projection.jpg")

print("\nAll 3 Jomon images generated!")
