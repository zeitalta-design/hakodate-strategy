"""
Navajo clay sculpting reference image
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 600
out = os.path.join(os.path.dirname(__file__), "assets", "img", "projects", "jomon")
os.makedirs(out, exist_ok=True)

try:
    font_md = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 16)
    font_sm = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 12)
    font_en = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 14)
except:
    font_md = ImageFont.load_default()
    font_sm = font_md
    font_en = font_md

img = Image.new("RGB", (W, H), (215, 195, 170))
draw = ImageDraw.Draw(img)

# Warm earth-tone background with texture
for y in range(H):
    r = int(215 - y * 0.05)
    g = int(195 - y * 0.06)
    b = int(170 - y * 0.07)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Wooden work surface
draw.rectangle([(0, H*0.55), (W, H)], fill=(160, 130, 95))
for y in range(int(H*0.55), H, 8):
    draw.line([(0, y), (W, y)], fill=(150, 120, 85), width=1)

# Clay material - reddish brown lump
clay_cx, clay_cy = W*0.3, H*0.52
draw.ellipse([(clay_cx-80, clay_cy-30), (clay_cx+80, clay_cy+40)], fill=(165, 100, 65))
draw.ellipse([(clay_cx-60, clay_cy-50), (clay_cx+50, clay_cy+10)], fill=(175, 110, 70))

# Hands working with clay (simplified)
# Left hand
hand_x, hand_y = W*0.45, H*0.48
draw.ellipse([(hand_x-30, hand_y-15), (hand_x+30, hand_y+25)], fill=(210, 175, 145))
# Fingers
for i in range(4):
    fx = hand_x - 20 + i * 14
    draw.ellipse([(fx-5, hand_y-25), (fx+5, hand_y-10)], fill=(205, 170, 140))
# Thumb
draw.ellipse([(hand_x+25, hand_y-5), (hand_x+40, hand_y+15)], fill=(205, 170, 140))

# Right hand
hand2_x, hand2_y = W*0.55, H*0.50
draw.ellipse([(hand2_x-25, hand2_y-12), (hand2_x+30, hand2_y+22)], fill=(210, 175, 145))
for i in range(4):
    fx = hand2_x - 15 + i * 12
    draw.ellipse([(fx-5, hand2_y-22), (fx+5, hand2_y-8)], fill=(205, 170, 140))

# Clay piece being shaped - small figure/animal
fig_cx, fig_cy = W*0.50, H*0.44
# Body
draw.ellipse([(fig_cx-18, fig_cy-10), (fig_cx+18, fig_cy+15)], fill=(170, 105, 65))
# Head
draw.ellipse([(fig_cx-8, fig_cy-22), (fig_cx+8, fig_cy-5)], fill=(170, 105, 65))
# Legs
draw.rectangle([(fig_cx-15, fig_cy+12), (fig_cx-8, fig_cy+25)], fill=(165, 100, 60))
draw.rectangle([(fig_cx+8, fig_cy+12), (fig_cx+15, fig_cy+25)], fill=(165, 100, 60))

# Finished pieces on the side
# Small bowl
bowl_x = W*0.75
draw.arc([(bowl_x-30, H*0.50), (bowl_x+30, H*0.60)], 0, 180, fill=(155, 95, 55), width=3)
draw.ellipse([(bowl_x-30, H*0.48), (bowl_x+30, H*0.53)], fill=(165, 105, 65), outline=(145, 85, 50))

# Small animal figure
animal_x = W*0.82
draw.ellipse([(animal_x-12, H*0.50), (animal_x+12, H*0.56)], fill=(160, 100, 60))
draw.ellipse([(animal_x+8, H*0.47), (animal_x+18, H*0.52)], fill=(160, 100, 60))

# Background elements - Navajo blanket pattern suggestion on wall
for i in range(5):
    x = W*0.1 + i * 35
    draw.rectangle([(x, H*0.08), (x+25, H*0.25)], fill=(180, 60, 40), outline=(140, 45, 30))
    draw.rectangle([(x+5, H*0.12), (x+20, H*0.21)], fill=(220, 180, 80))
    draw.line([(x+12, H*0.08), (x+12, H*0.25)], fill=(50, 50, 50), width=1)

# Natural tools on surface
# Stick
draw.line([(W*0.62, H*0.58), (W*0.68, H*0.52)], fill=(120, 90, 60), width=3)
# Stone
draw.ellipse([(W*0.70, H*0.56), (W*0.74, H*0.60)], fill=(140, 140, 130))

# Text overlay
draw.rounded_rectangle([(20, H-60), (380, H-15)], radius=6, fill=(30, 30, 30, 200))
draw.text((32, H-54), "Navajo Clay Sculpting — Reference", fill=(255, 255, 255), font=font_en)
draw.text((32, H-34), "ナバホ族の粘土造形　参考イメージ", fill=(200, 200, 200), font=font_sm)

img.save(os.path.join(out, "navajo_clay_reference.jpg"), "JPEG", quality=90)
print("Generated: navajo_clay_reference.jpg")
