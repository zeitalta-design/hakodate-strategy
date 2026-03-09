import math
import random
from PIL import Image, ImageDraw, ImageFilter

OUT = "D:/ClaudeProjects/HakodateStrategy/hakodate_tourism_strategy/assets/img/projects"

def star_points(cx, cy, r_outer, r_inner, n=5, rotation=-90):
    pts = []
    for i in range(n * 2):
        angle = math.radians(rotation + i * 360 / (n * 2))
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts

def draw_tower(draw, cx, base_y, h, color):
    w = h * 0.12
    draw.rectangle([cx - w, base_y - h, cx + w, base_y], fill=color)
    deck_y = base_y - h * 0.85
    deck_w = h * 0.22
    draw.rectangle([cx - deck_w, deck_y, cx + deck_w, deck_y + h * 0.12], fill=color)
    draw.polygon([(cx, base_y - h * 1.1), (cx - w * 0.5, base_y - h), (cx + w * 0.5, base_y - h)], fill=color)

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

def mountain_silhouette(draw, base_y, w, h_max, fill_color, seed_offset=0):
    pts = [(0, base_y)]
    for x in range(0, w + 1, 10):
        hv = base_y - h_max * math.sin(x * math.pi / (w * 0.8)) * (1 + 0.3 * math.sin(x * 0.015 + seed_offset))
        pts.append((x, int(hv)))
    pts.extend([(w, base_y + 100), (0, base_y + 100)])
    draw.polygon(pts, fill=fill_color)

COLORS_EVENT = [(255, 80, 80), (255, 200, 50), (80, 200, 255), (200, 80, 255), (80, 255, 150)]

# ========================================
# 1. VR Experience (1200x800)
# ========================================
img = gradient_bg(1200, 800, [(10, 15, 40), (20, 50, 90)])
draw = ImageDraw.Draw(img)
cx, cy = 600, 420

# Grid lines for VR feel
for i in range(0, 1200, 60):
    draw.line([(i, 0), (i, 800)], fill=(0, 60, 120), width=1)
for j in range(0, 800, 60):
    draw.line([(0, j), (1200, j)], fill=(0, 60, 120), width=1)

# Perspective lines
for angle in range(0, 360, 15):
    rad = math.radians(angle)
    ex = cx + 700 * math.cos(rad)
    ey = cy + 700 * math.sin(rad)
    draw.line([(cx, cy), (ex, ey)], fill=(0, 80, 160), width=1)

# Glow star outlines
for offset in range(8, 0, -1):
    pts = star_points(cx, cy, 250 + offset * 2, 150 + offset, 5)
    draw.polygon(pts, outline=(0, 30 + offset * 12, 200 + offset * 5), width=1)

# Main stars
draw.polygon(star_points(cx, cy, 250, 150, 5), outline=(0, 200, 255), width=3)
draw.polygon(star_points(cx, cy, 180, 100, 5), outline=(0, 255, 255), width=2)

# Tower
draw_tower(draw, 600, 600, 200, (0, 180, 220))

# Glow dots at star vertices
for pt in star_points(cx, cy, 250, 150, 5)[::2]:
    for r in range(12, 0, -1):
        draw.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], fill=(0, min(255, 100+r*12), 255))

img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
img.save(f"{OUT}/goryokaku_vr.jpg", "JPEG", quality=88)
print("1/7 goryokaku_vr.jpg")

# ========================================
# 2. Costume Experience (1200x800)
# ========================================
img = gradient_bg(1200, 800, [(60, 30, 20), (140, 80, 50)])
draw = ImageDraw.Draw(img)
cx, cy = 600, 400

pts = star_points(cx, cy, 280, 170, 5)
draw.polygon(pts, fill=(100, 60, 30))
draw.polygon(pts, outline=(200, 140, 80), width=3)
pts_inner = star_points(cx, cy, 220, 130, 5)
draw.polygon(pts_inner, outline=(180, 120, 60), width=2)

draw_tower(draw, 600, 580, 180, (180, 120, 60))

# Mon/crest circles at vertices
for i in range(5):
    angle = math.radians(-90 + i * 72)
    px = cx + 280 * math.cos(angle)
    py = cy + 280 * math.sin(angle)
    for r in [20, 15, 8]:
        draw.ellipse([px-r, py-r, px+r, py+r], outline=(220, 160, 80), width=2)

# Warm bokeh
random.seed(42)
for _ in range(80):
    x = random.randint(0, 1200)
    y = random.randint(0, 800)
    r = random.randint(3, 15)
    a = random.randint(40, 120)
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(min(255, a+80), min(255, a+30), a))

mountain_silhouette(draw, 700, 1200, 80, (80, 40, 25))
img.save(f"{OUT}/goryokaku_costume.jpg", "JPEG", quality=88)
print("2/7 goryokaku_costume.jpg")

# ========================================
# 3. Interactive Exhibition (1200x800)
# ========================================
img = gradient_bg(1200, 800, [(15, 20, 35), (35, 45, 80)])
draw = ImageDraw.Draw(img)
cx, cy = 600, 400

# Concentric star layers
for i, scale in enumerate([1.0, 0.75, 0.5, 0.25]):
    r_out = 300 * scale
    r_in = 180 * scale
    cv = 80 + i * 40
    pts = star_points(cx, cy, r_out, r_in, 5)
    draw.polygon(pts, outline=(cv, min(255, cv + 30), 200), width=2)

# Connection lines
for i in range(5):
    angle = math.radians(-90 + i * 72)
    for s1, s2 in [(1.0, 0.75), (0.75, 0.5), (0.5, 0.25)]:
        x1 = cx + 300 * s1 * math.cos(angle)
        y1 = cy + 300 * s1 * math.sin(angle)
        x2 = cx + 300 * s2 * math.cos(angle)
        y2 = cy + 300 * s2 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=(100, 140, 220), width=1)

# Touch points
for i in range(5):
    angle = math.radians(-90 + i * 72)
    for s in [1.0, 0.75, 0.5]:
        px = cx + 300 * s * math.cos(angle)
        py = cy + 300 * s * math.sin(angle)
        for r in [10, 6, 3]:
            c = min(255, 120 + (10 - r) * 15)
            draw.ellipse([px-r, py-r, px+r, py+r], fill=(c, min(255, c+20), 255))

draw_tower(draw, 600, 560, 160, (80, 100, 180))

# Data stream lines
random.seed(123)
for _ in range(40):
    x1, y1 = random.randint(0, 1200), random.randint(0, 800)
    length = random.randint(20, 80)
    a = random.uniform(0, 2 * math.pi)
    x2 = x1 + length * math.cos(a)
    y2 = y1 + length * math.sin(a)
    draw.line([(x1, y1), (x2, y2)], fill=(60, 80, 150), width=1)

img.save(f"{OUT}/goryokaku_exhibition.jpg", "JPEG", quality=88)
print("3/7 goryokaku_exhibition.jpg")

# ========================================
# 4. Night Illumination (1200x800)
# ========================================
img = Image.new("RGB", (1200, 800), (5, 5, 20))
draw = ImageDraw.Draw(img)
cx, cy = 600, 450

# Stars in sky
random.seed(77)
for _ in range(150):
    x = random.randint(0, 1200)
    y = random.randint(0, 300)
    r = random.choice([1, 1, 1, 2])
    bv = random.randint(100, 255)
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(bv, bv, bv))

# Glow layers
for glow in range(20, 0, -1):
    r_out = 260 + glow * 3
    r_in = 155 + glow * 2
    pts = star_points(cx, cy, r_out, r_in, 5)
    bv = max(0, 15 - glow)
    draw.polygon(pts, outline=(bv * 3, min(255, bv * 8), bv * 2))

# Main star
draw.polygon(star_points(cx, cy, 260, 155, 5), outline=(80, 220, 120), width=3)
draw.polygon(star_points(cx, cy, 200, 120, 5), outline=(60, 180, 100), width=2)

# Moat reflection
for y_off in range(50):
    t = y_off / 50
    av = int(80 * (1 - t))
    pts_ref = star_points(cx, cy + 150 + y_off, max(10, 260 - y_off * 3), max(5, 155 - y_off * 2), 5)
    draw.polygon(pts_ref, outline=(0, av, int(av * 0.6)))

# Tower with lights
draw_tower(draw, 600, 620, 200, (40, 120, 80))
for y in range(430, 620, 15):
    w = 3 if y < 500 else 2
    draw.rectangle([598 - w, y, 602 + w, y + 5], fill=(80, 200, 120))

mountain_silhouette(draw, 720, 1200, 60, (8, 8, 25))
img = img.filter(ImageFilter.GaussianBlur(radius=1))
img.save(f"{OUT}/goryokaku_lightup.jpg", "JPEG", quality=88)
print("4/7 goryokaku_lightup.jpg")

# ========================================
# 5. Night Event (1200x800)
# ========================================
img = gradient_bg(1200, 800, [(10, 5, 30), (30, 10, 50)])
draw = ImageDraw.Draw(img)
cx, cy = 600, 400

pts = star_points(cx, cy, 270, 165, 5)
draw.polygon(pts, fill=(20, 8, 40))
draw.polygon(pts, outline=(180, 100, 220), width=2)

# Event lights along edges
vertices = star_points(cx, cy, 270, 165, 5)
for i in range(len(vertices)):
    p1 = vertices[i]
    p2 = vertices[(i + 1) % len(vertices)]
    color = COLORS_EVENT[i % len(COLORS_EVENT)]
    for t_val in [x / 15 for x in range(16)]:
        lx = p1[0] + (p2[0] - p1[0]) * t_val
        ly = p1[1] + (p2[1] - p1[1]) * t_val
        for r in range(8, 0, -1):
            c = tuple(max(0, min(255, v - r * 15)) for v in color)
            draw.ellipse([lx-r, ly-r, lx+r, ly+r], fill=c)

draw_tower(draw, 600, 580, 190, (100, 50, 130))
for y in range(400, 580, 12):
    color = COLORS_EVENT[(y // 12) % len(COLORS_EVENT)]
    draw.rectangle([596, y, 604, y + 6], fill=color)

# Firework bursts
for bx, by, bc in [(200, 150, (255, 100, 80)), (900, 200, (80, 200, 255)), (500, 100, (255, 220, 50))]:
    for angle in range(0, 360, 8):
        rad = math.radians(angle)
        for dist in range(30, 90, 3):
            ex = bx + dist * math.cos(rad)
            ey = by + dist * math.sin(rad)
            fade = max(0, 255 - dist * 2)
            c = tuple(max(0, min(255, int(v * fade / 255))) for v in bc)
            if 0 <= ex < 1200 and 0 <= ey < 800:
                draw.point((int(ex), int(ey)), fill=c)

mountain_silhouette(draw, 700, 1200, 50, (12, 5, 25), seed_offset=1)
img.save(f"{OUT}/goryokaku_night_event.jpg", "JPEG", quality=88)
print("5/7 goryokaku_night_event.jpg")

# ========================================
# 6. Projection Mapping (1200x800)
# ========================================
img = Image.new("RGB", (1200, 800), (5, 0, 15))
draw = ImageDraw.Draw(img)
cx, cy = 600, 420

pts_outer = star_points(cx, cy, 280, 170, 5)
draw.polygon(pts_outer, fill=(15, 5, 25))

# Projection beams
beam_sources = [(100, 700), (1100, 700), (600, 750)]
for bx, by in beam_sources:
    for pt in star_points(cx, cy, 280, 170, 5)[::2]:
        for w in range(6, 0, -1):
            c = (w * 15, w * 5, w * 25)
            draw.line([(bx, by), pt], fill=c, width=w)

# Projected patterns on fort
for i in range(5):
    angle = math.radians(-90 + i * 72)
    px = cx + 220 * math.cos(angle)
    py = cy + 220 * math.sin(angle)
    color_proj = COLORS_EVENT[i]
    for r in range(25, 0, -2):
        fade = tuple(max(0, min(255, int(v * r / 25))) for v in color_proj)
        draw.ellipse([px-r, py-r, px+r, py+r], fill=fade)

draw.polygon(pts_outer, outline=(200, 100, 255), width=2)
pts_inner2 = star_points(cx, cy, 210, 130, 5)
draw.polygon(pts_inner2, outline=(150, 80, 200), width=1)

draw_tower(draw, 600, 600, 200, (80, 30, 120))
for y in range(410, 600, 8):
    idx = (y // 8) % 5
    c = tuple(max(0, min(255, v // 2)) for v in COLORS_EVENT[idx])
    draw.rectangle([594, y, 606, y + 5], fill=c)

# Upward light beams from tower
for angle in range(-60, 61, 20):
    rad = math.radians(angle - 90)
    ex = 600 + 400 * math.cos(rad)
    ey = 410 + 400 * math.sin(rad)
    for w in range(4, 0, -1):
        draw.line([(600, 410), (int(ex), int(ey))], fill=(w * 20, w * 10, w * 30), width=w)

img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
img.save(f"{OUT}/goryokaku_projection.jpg", "JPEG", quality=88)
print("6/7 goryokaku_projection.jpg")

# ========================================
# 7. Future Area Redesign (1600x900)
# ========================================
img = gradient_bg(1600, 900, [(200, 215, 235), (170, 195, 215)])
draw = ImageDraw.Draw(img)
cx, cy = 800, 480

# Sky
for y in range(0, 200):
    t = y / 200
    r = int(190 + 20 * t)
    g = int(210 + 15 * t)
    b = int(235 + 5 * t)
    draw.line([(0, y), (1600, y)], fill=(r, g, b))

# Mountain backdrop
mountain_silhouette(draw, 200, 1600, 100, (170, 185, 205), seed_offset=2)

# Moat (water ring)
pts_moat = star_points(cx, cy, 340, 210, 5)
draw.polygon(pts_moat, fill=(130, 175, 210))

# Green park area
pts_park = star_points(cx, cy, 310, 190, 5)
draw.polygon(pts_park, fill=(140, 185, 130))

# Inner paths
for i in range(5):
    angle = math.radians(-90 + i * 72)
    ix = cx + 80 * math.cos(angle)
    iy = cy + 80 * math.sin(angle)
    ox = cx + 310 * math.cos(angle)
    oy = cy + 310 * math.sin(angle)
    draw.line([(ix, iy), (ox, oy)], fill=(170, 180, 160), width=3)

# Buildings
facilities = [
    (cx - 50, cy - 35, cx + 50, cy + 35, (195, 180, 165)),
    (cx + 180, cy - 60, cx + 230, cy - 20, (185, 170, 155)),
    (cx - 220, cy + 40, cx - 170, cy + 80, (185, 170, 155)),
    (cx + 100, cy + 80, cx + 160, cy + 120, (190, 175, 160)),
]
for x1, y1, x2, y2, c in facilities:
    draw.rectangle([x1, y1, x2, y2], fill=c, outline=(140, 130, 120), width=2)

# Tower
draw_tower(draw, cx, cy + 20, 250, (110, 115, 125))

# Trees
random.seed(99)
for _ in range(300):
    tx = random.randint(200, 1400)
    ty = random.randint(250, 750)
    dist = math.sqrt((tx - cx)**2 + (ty - cy)**2)
    if 80 < dist < 380:
        r = random.randint(4, 10)
        gv = random.randint(130, 180)
        draw.ellipse([tx-r, ty-r, tx+r, ty+r], fill=(70, gv, 60))

# Surrounding roads
draw.rectangle([0, 780, 1600, 800], fill=(185, 185, 180))
draw.rectangle([0, 830, 1600, 900], fill=(155, 175, 155))

# Re-outline moat
draw.polygon(pts_moat, outline=(100, 155, 195), width=3)

img.save(f"{OUT}/goryokaku_future_area.jpg", "JPEG", quality=90)
print("7/7 goryokaku_future_area.jpg")

print("\nAll 7 images generated!")
