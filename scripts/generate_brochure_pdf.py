from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.pdfbase.pdfmetrics import stringWidth
import qrcode

ROOT = Path('/opt/data/midwest-suppliers-site')
OUT = ROOT / 'midwest-suppliers-low-ink-brochure.pdf'
QR = ROOT / 'assets' / 'site-qr.png'
LOGO = ROOT / 'assets' / 'knife-logo.jpg'
PHOTO = ROOT / 'assets' / 'steak-seafood-plate.jpg'
URL = 'https://justicejuly.github.io/midwest-suppliers-site/'
PHONE = '605-675-9429'

qr = qrcode.QRCode(box_size=6, border=2)
qr.add_data(URL)
qr.make(fit=True)
qr.make_image(fill_color='black', back_color='white').save(QR)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleMS', fontName='Helvetica-Bold', fontSize=25, leading=25, textColor=colors.HexColor('#17110d'), spaceAfter=4))
styles.add(ParagraphStyle(name='RedHead', fontName='Helvetica-Bold', fontSize=15, leading=17, textColor=colors.HexColor('#b5122a'), spaceBefore=6, spaceAfter=5))
styles.add(ParagraphStyle(name='BodyMS', fontName='Helvetica', fontSize=10.5, leading=13, textColor=colors.HexColor('#17110d')))
styles.add(ParagraphStyle(name='SmallMS', fontName='Helvetica', fontSize=8.5, leading=10.5, textColor=colors.HexColor('#5f5349')))
styles.add(ParagraphStyle(name='Phone', fontName='Helvetica-Bold', fontSize=22, leading=24, textColor=colors.HexColor('#b5122a')))
styles.add(ParagraphStyle(name='BoxHead', fontName='Helvetica-Bold', fontSize=11.5, leading=13, textColor=colors.HexColor('#17110d')))

red = colors.HexColor('#b5122a')
gold = colors.HexColor('#b8891f')
line = colors.HexColor('#d8d0c5')
ink = colors.HexColor('#17110d')
muted = colors.HexColor('#5f5349')
cream = colors.HexColor('#fffdf8')
light = colors.HexColor('#f7f2e9')

def P(txt, style='BodyMS'):
    return Paragraph(txt, styles[style])

def case_table(title, price, rows):
    data = [[Paragraph(f'<b>{title}</b>', styles['BoxHead']), Paragraph(f'<b>{price}</b>', styles['BoxHead'])]]
    for name, p in rows:
        data.append([P(name, 'SmallMS'), P(f'<b>{p}</b>', 'SmallMS')])
    t = Table(data, colWidths=[2.45*inch, .65*inch], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), light), ('TEXTCOLOR',(1,0),(1,0), red),
        ('BOX',(0,0),(-1,-1),0.8,line), ('INNERGRID',(0,0),(-1,-1),0.35,line),
        ('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    return t

def boxed(items, widths=None):
    t = Table(items, colWidths=widths)
    t.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),0.8,line), ('INNERGRID',(0,0),(-1,-1),0.35,line),
        ('BACKGROUND',(0,0),(-1,-1),colors.white), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),8), ('BOTTOMPADDING',(0,0),(-1,-1),8),
    ]))
    return t

def draw_page(canvas, doc):
    canvas.saveState()
    w,h = letter
    canvas.setStrokeColor(red); canvas.setLineWidth(5); canvas.line(doc.leftMargin, h-0.18*inch, w-doc.rightMargin, h-0.18*inch)
    canvas.setStrokeColor(gold); canvas.setLineWidth(2); canvas.line(doc.leftMargin, h-0.23*inch, w-doc.rightMargin, h-0.23*inch)
    canvas.setFont('Helvetica', 8.5); canvas.setFillColor(muted)
    canvas.drawString(doc.leftMargin, 0.22*inch, 'Midwest Suppliers Meats & Seafood')
    canvas.drawRightString(w-doc.rightMargin, 0.22*inch, f'Call {PHONE}')
    canvas.restoreState()

story = []
# Page 1
logo = Image(str(LOGO), width=1.05*inch, height=.65*inch)
photo = Image(str(PHOTO), width=1.75*inch, height=1.18*inch)
head = Table([[logo, [P('Midwest Suppliers', 'TitleMS'), P('Meats & Seafood · Home & Business Delivery', 'BodyMS'), P('Serving Rapid City, the Black Hills, Deadwood, and surrounding areas since 2020.', 'SmallMS'), P(PHONE, 'Phone')], photo]], colWidths=[1.1*inch, 4.0*inch, 1.9*inch])
head.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [head, Spacer(1, 8)]
story.append(boxed([[P('<b>Restaurant-quality meats and seafood delivered to your door.</b><br/>USDA inspected · USDA Choice · flash frozen · vacuum sealed · individually wrapped · no freezer burn', 'BodyMS')]], [7.0*inch]))
story.append(Spacer(1, 10))
story.append(boxed([[
    [P('Free home delivery','BoxHead'), P('Stock the freezer without the grocery-store run.','SmallMS')],
    [P('Business accounts','BoxHead'), P('Restaurants, bars, lodges, offices, and recurring orders.','SmallMS')],
    [P('Freezer offer','BoxHead'), P('Ask about a <b>free chest freezer</b> with select orders.','SmallMS')]
]], [2.33*inch,2.33*inch,2.33*inch]))
story.append(Spacer(1, 10))
story.append(boxed([[
    [P('Popular orders','RedHead'), P('• Big Beef Case<br/>• Pork Case<br/>• Seafood Case<br/>• Chicken Case<br/>• Preferred Customer Combo<br/>• Custom home or business order','BodyMS')],
    [P('One-year guarantee','RedHead'), P('Products are guaranteed for one full year from date of purchase for tenderness and quality. If you are dissatisfied, Midwest Suppliers will replace any unused portion.<br/><br/><b>Payments:</b> Major credit cards, Venmo/Cash App, and checks accepted. Returned check fee: $35.','BodyMS')]
]], [3.45*inch,3.55*inch]))
story.append(Spacer(1, 10))
story.append(boxed([[[P('How to order','RedHead'), P(f'1. Call <b>{PHONE}</b> and tell us what case, combo, or products you need.<br/>2. We confirm current availability, pricing, and delivery timing.<br/>3. Your order is delivered to your home or business.', 'BodyMS')], Image(str(QR), width=1.0*inch, height=1.0*inch)]], [5.8*inch,1.2*inch]))
story.append(P(f'<br/><b>Website:</b> {URL}', 'SmallMS'))
story.append(PageBreak())

# Page 2
story += [P('Menu & Cases', 'TitleMS'), P('Call to confirm current availability, pricing, delivery timing, and freezer offers.', 'BodyMS'), P(PHONE, 'Phone'), Spacer(1, 8)]
beef=[('Filet Mignon','$149'),('New York Strip','$89'),('Ranch Sirloin','$89'),('Rib Eye','$99'),('Porterhouse','$119'),('Sirloin Burgers','$79')]
pork=[('Center Cut Pork Chops','$59'),('Porterhouse Pork Chops','$69'),('Sirloin Roasts','$59'),('Bone-in Pork Chops','$62'),('Italian Sausage','$57'),('Country Style Ribs','$55')]
sea=[('Jumbo Peeled Shrimp','$59'),('Un-peeled Shrimp','$55'),('Mahi Mahi Filet','$84'),('Sockeye Salmon','$99'),('Red Snapper Filets','$74'),('Sea Scallops','$78')]
chick=[('Plain Chicken Breasts','$59'),('Lemon Pepper Breasts','$64'),('Italian Breasts','$64'),('Mild BBQ Breasts','$64'),('Chicken Tenders','$54'),('Chicken Fritters','$56')]
story.append(Table([[case_table('Big Beef Case','$624',beef), case_table('Pork Case','$361',pork)], [case_table('Seafood Case','$449',sea), case_table('Chicken Case','$361',chick)]], colWidths=[3.4*inch,3.4*inch], style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
story.append(boxed([[[P('Preferred Customer Combo','RedHead'), P('Beef Case + Pork Case + Seafood Case + Chicken Case<br/>Four cases at $249.75 each.', 'BodyMS')], P('$999','Phone')]], [5.45*inch,1.55*inch]))
story.append(Spacer(1, 8))
story.append(boxed([[[P('Quality checklist','BoxHead'), P('• USDA inspected<br/>• USDA Choice<br/>• Restaurant quality<br/>• 30–40% less fat','SmallMS')], [P('Freezer-ready','BoxHead'), P('• Flash frozen<br/>• Vacuum sealed<br/>• Individually wrapped<br/>• No freezer burn','SmallMS')]]], [3.5*inch,3.5*inch]))
story.append(P('<br/>Prices and offers are based on the current brochure and may change. Call to confirm current inventory, exact package details, delivery availability, and free chest freezer eligibility before purchase.', 'SmallMS'))

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=.5*inch, leftMargin=.5*inch, topMargin=.35*inch, bottomMargin=.45*inch, title='Midwest Suppliers Low Ink Brochure')
doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
print(OUT)
