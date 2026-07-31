from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path('/opt/data/midwest-suppliers-site')
SRC = ROOT / 'assets' / 'knife-logo.jpg'
OUT = ROOT / 'assets' / 'profile-logos'
OUT.mkdir(parents=True, exist_ok=True)

SIZE = 2048
LOGO_SAFE_DIAMETER = 1060
PHONE = '605-675-9429'
AREA = 'RAPID CITY • BLACK HILLS, SD'
RED = (237, 20, 73, 255)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
GOLD = (244, 189, 61, 255)

FONT_BOLD = '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf'
if not Path(FONT_BOLD).exists():
    FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if not Path(FONT_REG).exists():
    FONT_REG = FONT_BOLD

src = Image.open(SRC).convert('RGBA')
w, h = src.size
mask = Image.new('L', src.size, 0)
spx = src.load(); mpx = mask.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = spx[x, y]
        if a and (r > 35 or g > 35 or b > 35) and r > max(g, b) + 8:
            mpx[x, y] = min(255, max(0, int((r - max(g, b)) * 2.2)))
mask = mask.filter(ImageFilter.GaussianBlur(0.45))
bbox = mask.getbbox()
if not bbox:
    raise RuntimeError('Could not detect logo pixels')
margin = 24
bbox = (max(0,bbox[0]-margin), max(0,bbox[1]-margin), min(w,bbox[2]+margin), min(h,bbox[3]+margin))
logo_mask = ImageOps.autocontrast(mask.crop(bbox))
lw, lh = logo_mask.size
scale = min(LOGO_SAFE_DIAMETER/lw, LOGO_SAFE_DIAMETER/lh)
logo_mask = logo_mask.resize((int(lw*scale), int(lh*scale)), Image.Resampling.LANCZOS)


def fit_font(text, path, max_width, start_size):
    size = start_size
    while size > 20:
        font = ImageFont.truetype(path, size)
        box = ImageDraw.Draw(Image.new('RGB',(10,10))).textbbox((0,0), text, font=font)
        if box[2] - box[0] <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(path, size)


def centered_text(draw, y, text, font, fill):
    box = draw.textbbox((0,0), text, font=font)
    x = (SIZE - (box[2]-box[0]))//2
    draw.text((x, y), text, font=font, fill=fill)


def compose(name, logo_color, bg, ring, text_color, accent=None):
    img = Image.new('RGBA', (SIZE, SIZE), bg)
    d = ImageDraw.Draw(img)
    circle = (58, 58, SIZE-58, SIZE-58)
    d.ellipse(circle, fill=bg, outline=ring, width=34)
    d.ellipse((142,142,SIZE-142,SIZE-142), outline=accent or ring, width=8)

    area_font = fit_font(AREA, FONT_BOLD, 1320, 94)
    phone_font = fit_font(PHONE, FONT_BOLD, 1160, 142)
    small_font = fit_font('MEATS & SEAFOOD', FONT_BOLD, 980, 62)

    centered_text(d, 300, AREA, area_font, text_color)
    centered_text(d, 1528, PHONE, phone_font, text_color)
    centered_text(d, 1685, 'MEATS & SEAFOOD', small_font, accent or text_color)

    # Small divider lines so the text looks intentional.
    d.line((455, 445, 1593, 445), fill=accent or ring, width=7)
    d.line((455, 1490, 1593, 1490), fill=accent or ring, width=7)

    logo_layer = Image.new('RGBA', logo_mask.size, logo_color)
    x = (SIZE-logo_mask.size[0])//2
    y = (SIZE-logo_mask.size[1])//2 + 8
    img.paste(logo_layer, (x,y), logo_mask)

    png = OUT / f'{name}.png'
    jpg = OUT / f'{name}.jpg'
    img.save(png)
    img.convert('RGB').save(jpg, quality=95)
    return png, jpg

files = []
files.append(compose('midwest-profile-logo-badge-black-white-phone-area', BLACK, WHITE, BLACK, BLACK, RED))
files.append(compose('midwest-profile-logo-badge-red-black-phone-area', RED, BLACK, RED, WHITE, GOLD))

# Preview sheet for the two new badge versions.
sheet = Image.new('RGB', (1120, 620), 'white')
d = ImageDraw.Draw(sheet)
for idx, (png, _) in enumerate(files):
    im = Image.open(png).convert('RGBA').resize((520,520), Image.Resampling.LANCZOS)
    x = 20 + idx*560
    y = 25
    sheet.paste(im.convert('RGB'), (x,y), im.split()[-1])
    d.text((x, y+535), png.stem.replace('midwest-profile-logo-','').replace('-',' '), fill=(0,0,0))
sheet.save(OUT / 'profile-logo-badge-preview-sheet.jpg', quality=95)

for p in sorted(files + [(OUT/'profile-logo-badge-preview-sheet.jpg', OUT/'profile-logo-badge-preview-sheet.jpg')]):
    print(p[0], p[0].stat().st_size)
