import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 900, 675  # 4:3
OUT = "D:/ClaudeProjects/HakodateStrategy/hakodate_tourism_strategy/assets/img/projects"

try:
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 13)
except:
    font = ImageFont.load_default()

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

# ============================================
# 1. Nice - Promenade des Anglais / Coastline
# ============================================
img = gradient_bg(W, H, (100, 160, 220), (60, 130, 200))
draw = ImageDraw.Draw(img)

# Sea
for y in range(350, H):
    t = (y - 350) / (H - 350)
    c = (int(40 + 30 * t), int(110 + 40 * t), int(180 + 30 * t))
    draw.line([(0, y), (W, y)], fill=c)

# Sea waves
random.seed(10)
for _ in range(20):
    wx = random.randint(0, W)
    wy = random.randint(380, H - 30)
    wl = random.randint(30, 80)
    draw.arc([wx, wy, wx + wl, wy + 8], 0, 180, fill=(120, 180, 230), width=1)

# Promenade / beach
draw.rectangle([0, 330, W, 370], fill=(220, 200, 160))  # Beach sand
draw.rectangle([0, 310, W, 335], fill=(200, 195, 185))  # Promenade

# Palm trees along promenade
for px in range(80, W - 50, 140):
    # Trunk
    trunk_top = 180 + random.randint(-20, 20)
    draw.line([(px, 310), (px - 5, trunk_top)], fill=(120, 90, 50), width=4)
    # Fronds
    for angle in range(-60, 61, 20):
        rad = math.radians(angle)
        ex = px - 5 + int(45 * math.cos(rad - 0.3))
        ey = trunk_top - int(30 * abs(math.sin(rad))) + int(15 * math.sin(rad))
        draw.line([(px - 5, trunk_top), (ex, ey)], fill=(60, 140, 60), width=2)

# Buildings along coast (pastel colors of Nice)
colors_nice = [(230, 180, 140), (240, 210, 170), (220, 160, 130),
               (250, 220, 180), (210, 170, 150), (240, 200, 160)]
for bx in range(0, W, 55):
    bh = random.randint(100, 200)
    c = random.choice(colors_nice)
    draw.rectangle([bx, 310 - bh, bx + 48, 310], fill=c)
    # Windows
    for wy in range(310 - bh + 15, 300, 25):
        for wx_off in [10, 25, 38]:
            draw.rectangle([bx + wx_off, wy, bx + wx_off + 8, wy + 12],
                           fill=(c[0] - 30, c[1] - 30, c[2] - 20))

# Sun
for r in range(50, 0, -1):
    c = (min(255, 255), min(255, 230 + r), min(255, 150 + r * 2))
    draw.ellipse([700 - r, 60 - r, 700 + r, 60 + r], fill=c)

img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img.save(f"{OUT}/summer_nice_coast.jpg", "JPEG", quality=90)
print("1/3 nice coast")

# ============================================
# 2. Vancouver - Harbor / Mountains
# ============================================
img = gradient_bg(W, H, (140, 180, 220), (180, 210, 240))
draw = ImageDraw.Draw(img)

# Mountains in background
mt_colors = [(160, 180, 200), (140, 165, 190), (150, 175, 200)]
for i, (mx, mw, mh, mc) in enumerate([
    (150, 300, 180, mt_colors[0]),
    (400, 350, 220, mt_colors[1]),
    (700, 280, 160, mt_colors[2]),
]):
    pts = []
    for x in range(mx - mw // 2, mx + mw // 2 + 1, 4):
        dist = abs(x - mx)
        h_val = 280 - mh * math.exp(-dist**2 / (mw * 40))
        jitter = random.randint(-3, 3)
        pts.append((x, int(h_val) + jitter))
    pts.insert(0, (mx - mw // 2, 350))
    pts.append((mx + mw // 2, 350))
    draw.polygon(pts, fill=mc)
    # Snow caps
    for x, y in pts[1:-1]:
        if y < 280 - mh * 0.6:
            draw.point((x, y), fill=(230, 235, 240))
            draw.point((x, y + 1), fill=(225, 230, 238))

# Water
for y in range(350, H):
    t = (y - 350) / (H - 350)
    c = (int(80 + 40 * t), int(140 + 30 * t), int(190 + 20 * t))
    draw.line([(0, y), (W, y)], fill=c)

# Harbor / pier
draw.rectangle([100, 420, 800, 445], fill=(140, 130, 120))
# Pier posts
for px in range(120, 800, 60):
    draw.rectangle([px, 445, px + 8, 480], fill=(110, 100, 90))

# Boats
for bx, bw in [(200, 60), (450, 80), (650, 50)]:
    hull_c = random.choice([(180, 50, 40), (40, 60, 120), (200, 200, 200)])
    draw.polygon([(bx, 460), (bx + bw, 460), (bx + bw - 10, 480), (bx + 10, 480)], fill=hull_c)
    # Mast
    draw.line([(bx + bw // 2, 460), (bx + bw // 2, 410)], fill=(100, 100, 100), width=2)
    # Sail
    draw.polygon([(bx + bw // 2, 415), (bx + bw // 2 + 20, 445), (bx + bw // 2, 455)],
                 fill=(240, 240, 235))

# City skyline (glass towers)
for bx in range(50, W - 50, 70):
    bh = random.randint(60, 150)
    bw = random.randint(30, 55)
    c = random.choice([(160, 185, 210), (170, 190, 215), (150, 175, 200), (180, 200, 220)])
    draw.rectangle([bx, 350 - bh, bx + bw, 350], fill=c)
    # Glass reflection
    for gy in range(350 - bh + 8, 345, 12):
        draw.line([(bx + 3, gy), (bx + bw - 3, gy)], fill=(c[0] + 15, c[1] + 15, c[2] + 10), width=1)

# Trees on shore
for tx in range(30, W, 90):
    ty = 345 + random.randint(-5, 5)
    for r in range(18, 0, -1):
        gc = (40 + r, 100 + r * 2, 40 + r)
        draw.ellipse([tx - r, ty - 25 - r, tx + r, ty - 25 + r], fill=gc)

img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img.save(f"{OUT}/summer_vancouver_harbor.jpg", "JPEG", quality=90)
print("2/3 vancouver harbor")

# ============================================
# 3. Portland - Street scene / Urban village
# ============================================
img = gradient_bg(W, H, (180, 200, 220), (210, 215, 225))
draw = ImageDraw.Draw(img)

# Street
draw.rectangle([0, 480, W, H], fill=(160, 160, 155))  # Road
draw.rectangle([0, 460, W, 485], fill=(180, 175, 170))  # Sidewalk
# Road markings
for x in range(50, W, 80):
    draw.rectangle([x, 530, x + 40, 535], fill=(220, 220, 210))

# Buildings - Portland's eclectic low-rise
random.seed(33)
building_styles = [
    # (base_color, accent_color, has_awning)
    ((180, 80, 70), (200, 100, 80), True),    # Brick red
    ((220, 210, 190), (200, 190, 170), True),  # Cream
    ((160, 170, 180), (140, 150, 160), False), # Gray-blue
    ((190, 180, 150), (170, 160, 130), True),  # Tan
    ((200, 200, 195), (180, 180, 175), False), # Light gray
    ((170, 140, 110), (150, 120, 90), True),   # Brown
]

for bx in range(0, W, 90):
    bh = random.randint(150, 280)
    bw = 82
    style = random.choice(building_styles)
    base_c, accent_c, has_awning = style

    draw.rectangle([bx, 460 - bh, bx + bw, 460], fill=base_c)

    # Windows
    for wy in range(460 - bh + 20, 440, 35):
        for wx_off in [12, 35, 58]:
            draw.rectangle([bx + wx_off, wy, bx + wx_off + 16, wy + 22],
                           fill=(base_c[0] + 30, base_c[1] + 30, base_c[2] + 40))

    # Ground floor - shop front
    draw.rectangle([bx + 5, 420, bx + bw - 5, 460], fill=(base_c[0] + 20, base_c[1] + 20, base_c[2] + 20))
    # Shop window
    draw.rectangle([bx + 10, 425, bx + bw - 10, 455],
                   fill=(160, 190, 200))

    # Awning
    if has_awning:
        awning_c = random.choice([(180, 60, 50), (50, 100, 60), (60, 80, 140), (200, 150, 50)])
        draw.polygon([
            (bx + 5, 420), (bx + bw - 5, 420),
            (bx + bw, 408), (bx, 408)
        ], fill=awning_c)

# Street trees
for tx in range(60, W, 150):
    # Trunk
    draw.rectangle([tx - 3, 430, tx + 3, 460], fill=(100, 80, 50))
    # Canopy
    for r in range(25, 0, -1):
        gc = (50 + r, 110 + r * 2, 50 + r)
        draw.ellipse([tx - r - 5, 400 - r, tx + r + 5, 400 + r], fill=gc)

# Bicycles (Portland is bike-friendly)
for bkx in [200, 550]:
    # Wheels
    draw.ellipse([bkx, 450, bkx + 20, 470], outline=(60, 60, 60), width=2)
    draw.ellipse([bkx + 25, 450, bkx + 45, 470], outline=(60, 60, 60), width=2)
    # Frame
    draw.line([(bkx + 10, 460), (bkx + 22, 440)], fill=(180, 50, 40), width=2)
    draw.line([(bkx + 22, 440), (bkx + 35, 460)], fill=(180, 50, 40), width=2)
    draw.line([(bkx + 22, 440), (bkx + 35, 440)], fill=(180, 50, 40), width=2)

# A few clouds
for cx, cy, cw in [(150, 50, 80), (500, 70, 100), (750, 40, 70)]:
    for r_off in range(3):
        ox = r_off * 25 - 25
        draw.ellipse([cx + ox - cw // 3, cy - 15, cx + ox + cw // 3, cy + 15],
                     fill=(225, 228, 235))

img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img.save(f"{OUT}/summer_portland_street.jpg", "JPEG", quality=90)
print("3/3 portland street")

print("\nAll summer city images generated!")
