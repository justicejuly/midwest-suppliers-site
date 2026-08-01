from pathlib import Path
from html import escape
import shutil
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path('/opt/data/midwest-suppliers-site')
OUT = ROOT / 'adobe-editable' / 'midwest-door-to-door-favorite-editable'
ASSETS = OUT / 'assets'
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

asset_map = {
    'logo.jpg': ROOT / 'assets' / 'midwest-brochure-back-logo.jpg',
    'prime-rib-plate.jpg': ROOT / 'assets' / 'door-to-door-prime-rib-plate.jpg',
    'meat-seafood-plate.jpg': ROOT / 'assets' / 'door-to-door-meat-seafood-plate.jpg',
    'grill-steak.jpg': ROOT / 'assets' / 'door-to-door-grill-steak.jpg',
    'website-qr.png': ROOT / 'assets' / 'site-qr.png',
}
for name, src in asset_map.items():
    shutil.copy2(src, ASSETS / name)

W, H = 612, 792  # Letter size points, 8.5 x 11 in
COLORS = {
    'ink': '#17110d',
    'red': '#b5122a',
    'gold': '#b8891f',
    'muted': '#5d5147',
    'line': '#d8d0c5',
    'paper': '#fffdf8',
    'soft': '#f7f2e9',
    'black': '#090504',
}

def t(x, y, text, size=12, fill=None, weight='normal', anchor='start', family='Arial', transform=None):
    fill = fill or COLORS['ink']
    attrs = [f'x="{x}"', f'y="{y}"', f'font-family="{family}"', f'font-size="{size}"', f'fill="{fill}"', f'font-weight="{weight}"']
    if anchor != 'start': attrs.append(f'text-anchor="{anchor}"')
    if transform: attrs.append(f'transform="{transform}"')
    return f'<text {' '.join(attrs)}>{escape(text)}</text>'

def multiline(x, y, lines, size=10, fill=None, weight='normal', leading=None, anchor='start'):
    leading = leading or size * 1.25
    return '\n'.join(t(x, y + i * leading, line, size, fill, weight, anchor) for i, line in enumerate(lines))

def rect(x, y, w, h, fill='white', stroke=None, sw=1, rx=0):
    stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    rx_attr = f' rx="{rx}"' if rx else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{stroke_attr}{rx_attr}/>'

def image(x, y, w, h, href, clip_id=None):
    clip = f' clip-path="url(#{clip_id})"' if clip_id else ''
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{href}" preserveAspectRatio="xMidYMid slice"{clip}/>'

def contain_image(x, y, w, h, href):
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{href}" preserveAspectRatio="xMidYMid meet"/>'

def case_box(x, y, title, price, rows):
    out = [rect(x, y, 148, 92, 'white', COLORS['line'], 1, 8), rect(x, y, 148, 21, COLORS['soft'], None, rx=8)]
    out += [t(x+8, y+15, title.upper(), 10, COLORS['ink'], 'bold'), t(x+132, y+15, price, 10, COLORS['red'], 'bold', 'end')]
    yy = y + 34
    for name, val in rows:
        out.append(t(x+8, yy, name, 6.6, COLORS['ink']))
        out.append(t(x+136, yy, val, 6.6, COLORS['ink'], 'bold', 'end'))
        out.append(f'<line x1="{x+8}" y1="{yy+3}" x2="{x+140}" y2="{yy+3}" stroke="#cfc5b8" stroke-width=".5" stroke-dasharray="1 2"/>')
        yy += 10
    return '\n'.join(out)

def card(x, y, w, h, title, lines, top_color=None):
    out = [rect(x, y, w, h, 'white', COLORS['line'], 1, 8)]
    if top_color:
        out.append(rect(x, y, w, 5, top_color, None, rx=8))
    out.append(t(x+10, y+20, title.upper(), 10, COLORS['ink'], 'bold'))
    out.append(multiline(x+10, y+36, lines, 8.1, COLORS['muted'], leading=10))
    return '\n'.join(out)

beef = [('Filet Mignon','$149'),('NY Strip','$89'),('Ranch Sirloin','$89'),('Rib Eye','$99'),('Porterhouse','$119'),('Sirloin Burgers','$79')]
sea = [('Jumbo Shrimp','$59'),('Un-peeled Shrimp','$55'),('Mahi Mahi','$84'),('Sockeye Salmon','$99'),('Red Snapper','$74'),('Sea Scallops','$78')]
pork = [('Center Cut Chops','$59'),('Porterhouse Chops','$69'),('Sirloin Roasts','$59'),('Italian Sausage','$57'),('Country Ribs','$55')]
chick = [('Plain Breasts','$59'),('Lemon Pepper','$64'),('Italian Breasts','$64'),('Chicken Tenders','$54'),('Chicken Fritters','$56')]

common_defs = '''<defs>
  <clipPath id="heroClip"><rect x="28" y="130" width="355" height="140" rx="14"/></clipPath>
  <clipPath id="side1Clip"><rect x="397" y="130" width="168" height="65" rx="10"/></clipPath>
  <clipPath id="side2Clip"><rect x="397" y="205" width="168" height="65" rx="10"/></clipPath>
</defs>'''

front = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="8.5in" height="11in" viewBox="0 0 {W} {H}">
<title>Midwest Suppliers Door-to-Door Favorite Brochure - Front - Editable</title>
{common_defs}
{rect(0,0,W,H,COLORS['paper'])}
{rect(16,16,W-32,H-32,'none',COLORS['line'],1)}
<g id="header-logo-and-title">
  {contain_image(28,30,56,56,'assets/logo.jpg')}
  {t(96,43,'RAPID CITY · DEADWOOD · THE BLACK HILLS',7.6,COLORS['gold'],'bold')}
  {t(96,67,'RESTAURANT-QUALITY MEATS',27,COLORS['red'],'bold')}
  {t(96,94,'DELIVERED',27,COLORS['red'],'bold')}
  {t(96,116,'Freezer-ready meats and seafood for homes, restaurants, and businesses.',12,COLORS['ink'],'bold')}
</g>
<g id="food-photos">
  {image(28,130,355,140,'assets/prime-rib-plate.jpg','heroClip')}
  {rect(28,130,355,140,'none',COLORS['red'],3,14)}
  {rect(28,247,355,23,'rgba(0,0,0,.62)',None)}
  {t(36,263,'Premium beef cuts · freezer cases · home delivery',8,'white','bold')}
  {image(397,130,168,65,'assets/meat-seafood-plate.jpg','side1Clip')}
  {rect(397,130,168,65,'none',COLORS['line'],1,10)}
  {t(405,185,'Meat + seafood',8,'white','bold')}
  {image(397,205,168,65,'assets/grill-steak.jpg','side2Clip')}
  {rect(397,205,168,65,'none',COLORS['line'],1,10)}
  {t(405,260,'Grill-ready steaks',8,'white','bold')}
</g>
<g id="case-menu">
  {t(28,304,'CASE MENU',15,COLORS['ink'],'bold')}
  {case_box(28,320,'Big Beef','$624',beef)}
  {case_box(188,320,'Seafood','$449',sea)}
  {case_box(28,422,'Pork','$361',pork)}
  {case_box(188,422,'Chicken','$361',chick)}
  {rect(28,528,308,52,'white',COLORS['black'],2,10)}
  {t(40,550,'PREFERRED CUSTOMER COMBO',10,COLORS['ink'],'bold')}
  {t(40,564,'Beef + Pork + Seafood + Chicken at $249.75 each',8,COLORS['muted'])}
  {t(310,562,'$999',23,COLORS['red'],'bold','end')}
</g>
<g id="right-info-cards">
  {card(358,320,207,79,'Why customers buy',['USDA inspected, restaurant quality,','flash frozen, vacuum sealed, individually','wrapped, and backed by a one-year','tenderness and quality guarantee.'],COLORS['red'])}
  {card(358,411,207,64,'Ask about',['Free home delivery · veteran discounts','current deals · rewards · freezer offers','business orders.'],COLORS['gold'])}
  {card(358,487,207,66,'How to order',['Call/text what you are interested in.','We confirm current selections, prices,','discounts, and delivery options.'],None)}
</g>
<g id="neighborhood-cta">
  {rect(28,642,537,62,'#fff9e8',COLORS['gold'],2,12)}
  {multiline(42,671,['CATCH US IN YOUR','NEIGHBORHOOD.'],19,COLORS['red'],'bold',21)}
  {multiline(340,670,['Ask what is available today — cases, combos, delivery,','rewards, veteran discounts, and freezer deals.'],7.6,COLORS['muted'],'bold',10)}
</g>
<g id="phone-and-front-qr">
  <line x1="28" y1="718" x2="565" y2="718" stroke="{COLORS['line']}" stroke-width="2"/>
  {t(28,758,'605-675-9429',26,COLORS['red'],'bold')}
  {t(28,773,'Selections, prices, and availability may vary. Ask about veteran discounts, current deals, delivery options, and freezer offers.',6.6,COLORS['muted'])}
  {contain_image(506,730,56,56,'assets/website-qr.png')}
</g>
</svg>
'''

back = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="8.5in" height="11in" viewBox="0 0 {W} {H}">
<title>Midwest Suppliers Door-to-Door Favorite Brochure - Back - Editable</title>
{rect(0,0,W,H,COLORS['paper'])}
{rect(16,16,W-32,H-32,'none',COLORS['line'],1)}
<g id="centered-restaurant-menu-back">
  {contain_image(196,120,220,220,'assets/logo.jpg')}
  {multiline(306,386,['MIDWEST SUPPLIERS','MEATS & SEAFOOD'],31,COLORS['ink'],'bold',34,'middle')}
  {t(306,444,'Meats · Seafood · Freezer cases · Home & business delivery',13,COLORS['muted'],'bold','middle')}
  {t(306,507,'605-675-9429',32,COLORS['red'],'bold','middle')}
  {contain_image(266,540,80,80,'assets/website-qr.png')}
  {t(306,637,'midwestsuppliersmeat.com',10,COLORS['ink'],'bold','middle')}
  {multiline(306,670,['Serving Rapid City, Deadwood, the Black Hills, and surrounding areas.','Scan the QR code to visit the website, or call/text to ask about current','availability, delivery, rewards, veteran discounts, deals, and freezer offers.'],8,COLORS['muted'],'normal',10,'middle')}
</g>
</svg>
'''

(OUT / 'midwest-door-to-door-favorite-front-editable.svg').write_text(front)
(OUT / 'midwest-door-to-door-favorite-back-editable.svg').write_text(back)

readme = '''# Midwest Suppliers Favorite Brochure — Adobe Editable Package

These files are made for Adobe Illustrator editing.

## Open/edit in Illustrator
1. Unzip the package.
2. Open `midwest-door-to-door-favorite-front-editable.svg` in Adobe Illustrator.
3. Open `midwest-door-to-door-favorite-back-editable.svg` in Adobe Illustrator.
4. Text, boxes, colors, and most layout elements are editable.
5. Photos/logos/QR are linked from the `assets/` folder, so keep the SVG files and `assets/` folder together.

## InDesign option
InDesign can place these SVGs onto letter-size pages. For deeper editing, open them in Illustrator first, then place/export into InDesign.

## Size
- Letter portrait: 8.5 x 11 inches
- Front and back are separate files for two-sided printing.

## Notes
- The QR code currently goes to the working GitHub Pages website.
- The printed display domain says `midwestsuppliersmeat.com`, as requested, until Chuck confirms domain setup.
- Service area wording: “Rapid City, Deadwood, the Black Hills, and surrounding areas.”
'''
(OUT / 'README.txt').write_text(readme)

# Validate SVG XML
for svg in OUT.glob('*.svg'):
    ET.parse(svg)
    print('valid svg', svg)

zip_path = ROOT / 'adobe-editable' / 'midwest-door-to-door-favorite-editable-adobe-package.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for f in OUT.rglob('*'):
        z.write(f, f.relative_to(OUT.parent))
print('zip', zip_path, zip_path.stat().st_size)
