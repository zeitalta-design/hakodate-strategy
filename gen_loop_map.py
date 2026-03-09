import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 800
img = Image.new("RGB", (W, H), (240, 242, 245))
draw = ImageDraw.Draw(img)

# --- Fonts ---
try:
    font_ja = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 14)
    font_ja_sm = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 11)
    font_en = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 12)
    font_en_lg = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 18)
    font_en_md = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 14)
    font_legend = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 12)
    font_title = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 22)
    font_subtitle = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 13)
except:
    font_ja = font_ja_sm = font_en = font_en_lg = font_en_md = font_legend = font_title = font_subtitle = ImageFont.load_default()

NAVY = (30, 45, 80)
NAVY_LIGHT = (60, 80, 130)
ACCENT = (0, 140, 180)
RED = (200, 60, 60)
WHITE = (255, 255, 255)
GRAY = (180, 185, 195)
GRAY_DARK = (130, 135, 145)
BG_WATER = (205, 222, 238)

# --- Bay water area ---
water_pts = [(0, 300), (150, 250), (300, 350), (450, 400),
             (500, 500), (400, 600), (200, 650), (0, 700),
             (0, H), (0, 300)]
draw.polygon(water_pts, fill=BG_WATER)
# Coastline
coast = [(0, 300), (150, 250), (300, 350), (450, 400), (500, 500), (400, 600), (200, 650), (0, 700)]
for i in range(len(coast) - 1):
    draw.line([coast[i], coast[i+1]], fill=GRAY, width=2)

# --- Mountain silhouette ---
mt_cx, mt_base = 150, 280
mt_pts = [(mt_cx - 120, mt_base)]
for x in range(mt_cx - 120, mt_cx + 121, 3):
    dist = abs(x - mt_cx)
    h = mt_base - 90 * math.exp(-dist**2 / 3500)
    mt_pts.append((x, int(h)))
mt_pts.append((mt_cx + 120, mt_base))
draw.polygon(mt_pts, fill=(200, 210, 222))
draw.text((mt_cx - 22, mt_base - 70), "Mt.334m", fill=GRAY_DARK, font=font_ja_sm)

# --- Stops ---
stops = {
    "hakodate_st": (480, 380),
    "kanemori":    (350, 480),
    "motomachi":   (280, 400),
    "ropeway":     (200, 340),
    "goryokaku":   (820, 280),
}

# --- Route ---
route_points = [
    stops["hakodate_st"],
    (430, 420), stops["kanemori"],
    (310, 450), stops["motomachi"],
    (240, 370), stops["ropeway"],
    (250, 300), (350, 280), (430, 310),
    stops["hakodate_st"],
    (550, 320), (650, 280), (750, 270),
    stops["goryokaku"],
    (850, 330), (800, 380), (700, 400), (600, 400),
    stops["hakodate_st"],
]

# Route shadow
for i in range(len(route_points) - 1):
    draw.line([route_points[i], route_points[i+1]], fill=(180, 198, 218), width=12)
# Route main
for i in range(len(route_points) - 1):
    draw.line([route_points[i], route_points[i+1]], fill=ACCENT, width=5)

# Direction arrows
for i in range(0, len(route_points) - 1, 3):
    p1 = route_points[i]
    p2 = route_points[i + 1]
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2
    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L = 14
    tip = (mx + L * math.cos(angle), my + L * math.sin(angle))
    left = (mx + L * 0.7 * math.cos(angle + 2.5), my + L * 0.7 * math.sin(angle + 2.5))
    right = (mx + L * 0.7 * math.cos(angle - 2.5), my + L * 0.7 * math.sin(angle - 2.5))
    draw.polygon([tip, left, right], fill=ACCENT)

# --- Stop markers and labels ---
stop_info = {
    "hakodate_st": ("函館駅", "Hakodate Sta.", (15, -52)),
    "kanemori":    ("金森倉庫", "Kanemori", (15, 15)),
    "motomachi":   ("元町", "Motomachi", (-110, -20)),
    "ropeway":     ("函館山RW", "Ropeway", (-120, -50)),
    "goryokaku":   ("五稜郭", "Goryokaku", (-15, -55)),
}

for key, (cx, cy) in stops.items():
    ja, en, (ox, oy) = stop_info[key]

    # Marker
    for r in range(18, 0, -1):
        c = tuple(min(255, v + (18 - r) * 5) for v in NAVY)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
    draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill=WHITE)
    dot_color = RED if key == "hakodate_st" else NAVY
    draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=dot_color)

    # Label box
    lx, ly = cx + ox, cy + oy
    # Measure text
    ja_bbox = draw.textbbox((0, 0), ja, font=font_ja)
    en_bbox = draw.textbbox((0, 0), en, font=font_en)
    ja_w = ja_bbox[2] - ja_bbox[0]
    en_w = en_bbox[2] - en_bbox[0]
    box_w = max(ja_w, en_w) + 20
    box_h = 42

    draw.rounded_rectangle(
        [lx, ly, lx + box_w, ly + box_h],
        radius=6, fill=WHITE, outline=NAVY_LIGHT, width=1
    )
    draw.text((lx + 10, ly + 4), ja, fill=NAVY, font=font_ja)
    draw.text((lx + 10, ly + 22), en, fill=NAVY_LIGHT, font=font_en)

# --- Legend ---
lx, ly = 850, 560
draw.rounded_rectangle([lx, ly, lx + 310, ly + 190], radius=8, fill=WHITE, outline=GRAY, width=1)

draw.text((lx + 15, ly + 10), "Hakodate Loop", fill=NAVY, font=font_en_lg)

draw.line([(lx + 20, ly + 55), (lx + 60, ly + 55)], fill=ACCENT, width=4)
draw.text((lx + 70, ly + 47), "Loop Route", fill=NAVY, font=font_legend)

draw.ellipse([lx+30, ly+75, lx+50, ly+95], fill=WHITE, outline=NAVY, width=2)
draw.ellipse([lx+35, ly+80, lx+45, ly+90], fill=NAVY)
draw.text((lx + 70, ly + 77), "Bus Stop", fill=NAVY, font=font_legend)

draw.ellipse([lx+30, ly+105, lx+50, ly+125], fill=WHITE, outline=NAVY, width=2)
draw.ellipse([lx+35, ly+110, lx+45, ly+120], fill=RED)
draw.text((lx + 70, ly + 107), "Hub (Hakodate Sta.)", fill=NAVY, font=font_legend)

draw.rounded_rectangle([lx+25, ly+138, lx+55, ly+158], radius=4, fill=BG_WATER, outline=GRAY, width=1)
draw.text((lx + 70, ly + 140), "Bay Area", fill=GRAY_DARK, font=font_legend)

# --- Title box ---
draw.rounded_rectangle([30, 30, 440, 120], radius=8, fill=WHITE, outline=NAVY_LIGHT, width=1)
draw.text((50, 38), "Hakodate Loop", fill=NAVY, font=font_title)
draw.text((50, 68), "Route Map", fill=NAVY_LIGHT, font=font_en_md)
draw.text((50, 90), "15-20min interval / Free or Low-fare", fill=GRAY_DARK, font=font_subtitle)

OUT = "D:/ClaudeProjects/HakodateStrategy/hakodate_tourism_strategy/assets/img/projects/hakodate_loop_route.jpg"
img.save(OUT, "JPEG", quality=90)
print("Route map generated!")
