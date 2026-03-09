"""
Hakodate Future Map — 函館の都市マップ生成
函館の地形を俯瞰的に描き、5施策のエリアをマーキングする
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1400, 900
out_dir = os.path.join(os.path.dirname(__file__), "assets", "img", "map")
os.makedirs(out_dir, exist_ok=True)

# Fonts
try:
    font_lg = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    font_md = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 16)
    font_sm = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 13)
    font_en = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 11)
except:
    font_lg = ImageFont.load_default()
    font_md = font_lg
    font_sm = font_lg
    font_en = font_lg

# Colors
SEA = (200, 218, 232)
LAND = (235, 238, 230)
LAND_DARK = (210, 215, 200)
MOUNTAIN = (180, 195, 170)
ROAD = (200, 200, 200)
ROAD_MAIN = (170, 170, 170)
RAIL = (100, 100, 100)
NAVY = (15, 26, 46)
NAVY_600 = (45, 74, 111)
ACCENT = (196, 154, 60)
WHITE = (255, 255, 255)
RED = (192, 57, 43)
TEXT_DARK = (30, 30, 30)
TEXT_MID = (100, 100, 100)

img = Image.new("RGB", (W, H), SEA)
draw = ImageDraw.Draw(img)

# === Draw Hakodate geography (schematic) ===

# Sea background is already set
# Land mass - Hakodate peninsula shape (simplified)
# Main land area (north part)
land_north = [
    (0, 0), (W, 0), (W, H*0.35),
    (W*0.85, H*0.4), (W*0.7, H*0.42),
    (W*0.6, H*0.5), (W*0.55, H*0.55),
    (W*0.5, H*0.58), (W*0.45, H*0.55),
    (W*0.4, H*0.5), (W*0.3, H*0.42),
    (W*0.15, H*0.38), (0, H*0.35),
]
draw.polygon(land_north, fill=LAND)

# Hakodate Mountain peninsula (tombolo shape - narrow strip going south)
tombolo = [
    (W*0.45, H*0.55),
    (W*0.48, H*0.58),
    (W*0.47, H*0.65),
    (W*0.44, H*0.72),
    (W*0.40, H*0.78),
    (W*0.35, H*0.82),
    (W*0.30, H*0.85),
    (W*0.28, H*0.88),
    (W*0.30, H*0.92),
    (W*0.35, H*0.93),
    (W*0.40, H*0.90),
    (W*0.42, H*0.85),
    (W*0.38, H*0.80),
    (W*0.42, H*0.75),
    (W*0.46, H*0.70),
    (W*0.50, H*0.65),
    (W*0.52, H*0.60),
    (W*0.50, H*0.56),
]
draw.polygon(tombolo, fill=LAND)

# Hakodate Mountain (at the tip)
mt_hakodate = [
    (W*0.28, H*0.85),
    (W*0.25, H*0.88),
    (W*0.24, H*0.92),
    (W*0.26, H*0.96),
    (W*0.32, H*0.97),
    (W*0.38, H*0.95),
    (W*0.40, H*0.92),
    (W*0.38, H*0.88),
    (W*0.35, H*0.85),
]
draw.polygon(mt_hakodate, fill=MOUNTAIN)

# Goryokaku area (slightly elevated)
goryokaku_area = [
    (W*0.55, H*0.18), (W*0.72, H*0.18),
    (W*0.72, H*0.35), (W*0.55, H*0.35),
]
draw.polygon(goryokaku_area, fill=LAND_DARK, outline=None)

# === Roads (simplified grid) ===
# Main road along coast
coast_road = [
    (W*0.15, H*0.38), (W*0.25, H*0.42),
    (W*0.35, H*0.48), (W*0.42, H*0.55),
    (W*0.45, H*0.62), (W*0.44, H*0.72),
    (W*0.40, H*0.78),
]
for i in range(len(coast_road)-1):
    draw.line([coast_road[i], coast_road[i+1]], fill=ROAD_MAIN, width=2)

# Horizontal roads
for y_frac in [0.15, 0.25, 0.35]:
    y = int(H * y_frac)
    draw.line([(W*0.1, y), (W*0.9, y)], fill=ROAD, width=1)

# Vertical roads
for x_frac in [0.35, 0.5, 0.65, 0.8]:
    x = int(W * x_frac)
    draw.line([(x, H*0.05), (x, H*0.4)], fill=ROAD, width=1)

# === Railway line (JR) ===
rail_points = [
    (W*0.95, H*0.22),  # Shin-Hakodate-Hokuto (off east)
    (W*0.85, H*0.24),
    (W*0.75, H*0.26),
    (W*0.65, H*0.28),
    (W*0.55, H*0.32),
    (W*0.45, H*0.38),
    (W*0.40, H*0.45),
    (W*0.42, H*0.55),  # Hakodate Station area
]
for i in range(len(rail_points)-1):
    draw.line([rail_points[i], rail_points[i+1]], fill=RAIL, width=3)
# Dashes
for i in range(len(rail_points)-1):
    x1, y1 = rail_points[i]
    x2, y2 = rail_points[i+1]
    mx, my = (x1+x2)/2, (y1+y2)/2
    draw.line([(mx-4, my), (mx+4, my)], fill=WHITE, width=1)

# === Tram line ===
tram_points = [
    (W*0.42, H*0.55),  # Hakodate Station
    (W*0.40, H*0.60),
    (W*0.38, H*0.65),
    (W*0.36, H*0.72),
    (W*0.33, H*0.78),
]
for i in range(len(tram_points)-1):
    draw.line([tram_points[i], tram_points[i+1]], fill=(140, 80, 80), width=2)

# === Water labels ===
draw.text((W*0.08, H*0.55), "津軽海峡", fill=(150, 175, 200), font=font_md)
draw.text((W*0.65, H*0.60), "太平洋", fill=(150, 175, 200), font=font_md)
draw.text((W*0.12, H*0.70), "函館湾", fill=(150, 175, 200), font=font_sm)

# === Key locations (small dots) ===
def draw_dot(pos, color, label, sublabel=None, label_offset=(12, -8)):
    x, y = pos
    draw.ellipse([(x-4, y-4), (x+4, y+4)], fill=color, outline=WHITE)
    lx, ly = x + label_offset[0], y + label_offset[1]
    draw.text((lx, ly), label, fill=TEXT_DARK, font=font_sm)
    if sublabel:
        draw.text((lx, ly + 16), sublabel, fill=TEXT_MID, font=font_en)

# Hakodate Station
draw_dot((W*0.42, H*0.55), RAIL, "函館駅", "Hakodate Sta.")

# Hakodate Mountain
draw_dot((W*0.32, H*0.92), MOUNTAIN, "函館山", "Mt. Hakodate", label_offset=(-70, -20))

# === 5 Project markers (large, prominent) ===
def draw_marker(pos, color, number, title_en, title_ja, anchor="right"):
    x, y = pos
    # Outer ring
    draw.ellipse([(x-16, y-16), (x+16, y+16)], fill=color, outline=WHITE, width=3)
    # Number
    tw = draw.textlength(number, font=font_md)
    draw.text((x - tw/2, y - 9), number, fill=WHITE, font=font_md)
    # Label
    if anchor == "right":
        lx = x + 24
    elif anchor == "left":
        lx = x - 180
    else:
        lx = x - 80
    # Background pill
    pill_w = 170
    pill_h = 42
    ly = y - pill_h // 2
    draw.rounded_rectangle(
        [(lx - 8, ly - 2), (lx + pill_w, ly + pill_h)],
        radius=6, fill=(255, 255, 255, 230), outline=color, width=2
    )
    draw.text((lx, ly + 2), title_en, fill=color, font=font_md)
    draw.text((lx, ly + 22), title_ja, fill=TEXT_DARK, font=font_sm)

# 1. Goryokaku 2.0 - northeast area
draw_marker((W*0.63, H*0.26), NAVY_600, "01", "Goryokaku 2.0", "五稜郭エリア再設計", anchor="right")

# Draw star shape for Goryokaku
import math
cx, cy, r = W*0.63, H*0.26, 12
star_pts = []
for i in range(10):
    angle = math.radians(i * 36 - 90)
    radius = r if i % 2 == 0 else r * 0.5
    star_pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
# Don't draw star over marker, draw it nearby
sx, sy = W*0.60, H*0.20
star_pts2 = []
for i in range(10):
    angle = math.radians(i * 36 - 90)
    radius = 10 if i % 2 == 0 else 5
    star_pts2.append((sx + radius * math.cos(angle), sy + radius * math.sin(angle)))
draw.polygon(star_pts2, fill=NAVY_600, outline=WHITE)

# 2. Night Economy - port/waterfront area
draw_marker((W*0.35, H*0.55), RED, "02", "Night Economy", "夜間経済圏の創出", anchor="left")

# 3. Jomon Experience - north/outskirts (Minamikayabe direction)
draw_marker((W*0.20, H*0.22), (139, 90, 43), "03", "Jomon Experience", "縄文遺跡エリア", anchor="right")

# 4. Experience Liner - railway line (Shin-Hakodate-Hokuto)
draw_marker((W*0.88, H*0.22), RAIL, "04", "Experience Liner", "新函館北斗 → 函館", anchor="left")

# 5. Summer Capital - whole city overlay concept
draw_marker((W*0.50, H*0.08), ACCENT, "05", "Summer Capital", "避暑都市ビジョン", anchor="right")

# === Title block ===
draw.rounded_rectangle([(20, H-70), (320, H-15)], radius=6, fill=(15, 26, 46, 220))
draw.text((32, H-64), "HAKODATE FUTURE MAP", fill=WHITE, font=font_md)
draw.text((32, H-40), "函館観光の未来構造", fill=(180, 200, 220), font=font_sm)

# === Legend ===
draw.rounded_rectangle([(W-220, H-90), (W-20, H-15)], radius=6, fill=(255, 255, 255, 230), outline=(200, 200, 200))
draw.text((W-210, H-84), "JR線", fill=RAIL, font=font_sm)
draw.line([(W-170, H-76), (W-130, H-76)], fill=RAIL, width=3)
draw.text((W-210, H-62), "市電", fill=(140, 80, 80), font=font_sm)
draw.line([(W-170, H-54), (W-130, H-54)], fill=(140, 80, 80), width=2)
draw.text((W-210, H-40), "施策エリア", fill=NAVY_600, font=font_sm)
draw.ellipse([(W-170, H-36), (W-158, H-24)], fill=NAVY_600, outline=WHITE)

# Save
img.save(os.path.join(out_dir, "hakodate_future_map.jpg"), "JPEG", quality=92)
print("Generated: hakodate_future_map.jpg")
