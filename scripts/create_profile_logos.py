from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFilter

ROOT = Path('/opt/data/midwest-suppliers-site')
SRC = ROOT / 'assets' / 'knife-logo.jpg'
OUT = ROOT / 'assets' / 'profile-logos'
OUT.mkdir(parents=True, exist_ok=True)

SIZE = 2048
SAFE_DIAMETER = 1650  # keeps the whole mark safely inside circular social crops
RED = (237, 20, 73, 255)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RING_RED = (237, 20, 73, 255)
RING_BLACK = (8, 8, 8, 255)

src = Image.open(SRC).convert('RGBA')
px = src.load()
w, h = src.size

# Mask the logo by selecting non-near-black pixels. This keeps the actual red lettering/mark.
mask = Image.new('L', src.size, 0)
mp = mask.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        # Original background is black; antialiasing creates dark reds on edges.
        if a and (r > 35 or g > 35 or b > 35) and r > max(g, b) + 8:
            mp[x, y] = min(255, max(0, int((r - max(g, b)) * 2.2)))

# Smooth edges a little, then find bounding box.
mask = mask.filter(ImageFilter.GaussianBlur(0.45))
bbox = mask.getbbox()
if not bbox:
    raise RuntimeError('Could not detect logo pixels')

# Add small crop margin around detected logo.
margin = 24
bbox = (
    max(0, bbox[0] - margin),
    max(0, bbox[1] - margin),
    min(w, bbox[2] + margin),
    min(h, bbox[3] + margin),
)
logo_mask = mask.crop(bbox)

# Scale logo to fit safely inside circle.
lw, lh = logo_mask.size
scale = min(SAFE_DIAMETER / lw, SAFE_DIAMETER / lh)
new_size = (int(lw * scale), int(lh * scale))
logo_mask = logo_mask.resize(new_size, Image.Resampling.LANCZOS)

# Slightly strengthen after resize for crisp profile icons.
logo_mask = ImageOps.autocontrast(logo_mask)


def compose(name, fg, bg, ring=None, transparent_outside_circle=False):
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0) if transparent_outside_circle else bg)
    draw = ImageDraw.Draw(img)

    circle_bbox = (56, 56, SIZE - 56, SIZE - 56)
    if transparent_outside_circle:
        draw.ellipse(circle_bbox, fill=bg)
    if ring:
        draw.ellipse(circle_bbox, outline=ring, width=34)

    # Put recolored logo in center.
    color_layer = Image.new('RGBA', logo_mask.size, fg)
    x = (SIZE - logo_mask.size[0]) // 2
    y = (SIZE - logo_mask.size[1]) // 2 + 8
    img.paste(color_layer, (x, y), logo_mask)

    # Save PNG and JPEG preview-friendly copy.
    png = OUT / f'{name}.png'
    jpg = OUT / f'{name}.jpg'
    img.save(png)
    img.convert('RGB').save(jpg, quality=95)
    return png, jpg

files = []
files.append(compose('midwest-profile-logo-black-on-white-circle', BLACK, WHITE, ring=RING_BLACK))
files.append(compose('midwest-profile-logo-red-on-black-circle', RED, BLACK, ring=RING_RED))
files.append(compose('midwest-profile-logo-black-on-white-transparent-outside', BLACK, WHITE, ring=RING_BLACK, transparent_outside_circle=True))
files.append(compose('midwest-profile-logo-red-on-black-transparent-outside', RED, BLACK, ring=RING_RED, transparent_outside_circle=True))

# Contact sheet for quick review.
thumbs = []
labels = []
for png, _ in files[:4]:
    im = Image.open(png).convert('RGBA').resize((520, 520), Image.Resampling.LANCZOS)
    thumbs.append(im)
    labels.append(png.stem.replace('midwest-profile-logo-', '').replace('-', ' '))

sheet = Image.new('RGB', (1100, 1160), 'white')
d = ImageDraw.Draw(sheet)
positions = [(20, 40), (560, 40), (20, 610), (560, 610)]
for im, label, pos in zip(thumbs, labels, positions):
    checker = Image.new('RGB', (520, 520), (238, 238, 238))
    checker.paste(im.convert('RGB'), (0, 0), im.split()[-1])
    sheet.paste(checker, pos)
    d.text((pos[0], pos[1] + 528), label, fill=(0, 0, 0))
sheet.save(OUT / 'profile-logo-preview-sheet.jpg', quality=95)

for p in sorted(OUT.iterdir()):
    print(p, p.stat().st_size)
