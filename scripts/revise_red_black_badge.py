from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path('/opt/data/midwest-suppliers-site')
OUT = ROOT / 'assets' / 'profile-logos'
SRC = OUT / 'midwest-profile-logo-badge-red-black-phone-area.png'
PNG = OUT / 'midwest-profile-logo-badge-red-black-gold-text-no-repeat.png'
JPG = OUT / 'midwest-profile-logo-badge-red-black-gold-text-no-repeat.jpg'
PREVIEW = OUT / 'profile-logo-badge-gold-no-repeat-preview.jpg'

GOLD = (244, 189, 61, 255)
WHITE_THRESHOLD = 210
BLACK = (0, 0, 0, 255)

img = Image.open(SRC).convert('RGBA')
px = img.load()
w, h = img.size

# Change all white lettering (top location and phone) to gold.
# The logo itself and red border remain red; the existing gold lines/bottom text stay gold.
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a and r > WHITE_THRESHOLD and g > WHITE_THRESHOLD and b > WHITE_THRESHOLD:
            px[x, y] = GOLD

# Remove the repeated red "MEATS & SEAFOOD" from the original inner logo.
# This sits just above the lower gold divider. Cover only that curved text zone,
# leaving the main hook/knife mark intact as much as possible.
draw = ImageDraw.Draw(img)
# Main cleanup band over the repeated lettering under the blade.
draw.rounded_rectangle((860, 1320, 1495, 1494), radius=28, fill=BLACK)
# Cleanup the remaining curved "SEAFOOD" letters on the right side of the inner logo.
draw.rounded_rectangle((1245, 1020, 1498, 1415), radius=28, fill=BLACK)
# Re-draw the lower divider in case the cleanup touches its top edge.
draw.line((455, 1490, 1593, 1490), fill=GOLD, width=7)

img.save(PNG)
img.convert('RGB').save(JPG, quality=95)

# Preview before/after side by side
old = Image.open(SRC).convert('RGBA').resize((520, 520), Image.Resampling.LANCZOS)
new = img.resize((520, 520), Image.Resampling.LANCZOS)
sheet = Image.new('RGB', (1100, 620), 'white')
d = ImageDraw.Draw(sheet)
sheet.paste(old.convert('RGB'), (20, 25), old.split()[-1])
sheet.paste(new.convert('RGB'), (560, 25), new.split()[-1])
d.text((20, 560), 'Before: white text + repeated red Meats & Seafood', fill=(0,0,0))
d.text((560, 560), 'After: gold text + repeated red text removed', fill=(0,0,0))
sheet.save(PREVIEW, quality=95)

for p in [PNG, JPG, PREVIEW]:
    print(p, p.stat().st_size)
