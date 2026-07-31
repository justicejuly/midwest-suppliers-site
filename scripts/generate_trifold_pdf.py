from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import qrcode

ROOT = Path('/opt/data/midwest-suppliers-site')
OUT = ROOT / 'midwest-suppliers-one-page-trifold.pdf'
QR = ROOT / 'assets' / 'site-qr.png'
LOGO = ROOT / 'assets' / 'knife-logo.jpg'
PHOTO = ROOT / 'assets' / 'steak-seafood-plate.jpg'
URL = 'https://justicejuly.github.io/midwest-suppliers-site/'
PHONE = '605-675-9429'

if not QR.exists():
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(URL); qr.make(fit=True)
    qr.make_image(fill_color='black', back_color='white').save(QR)

red = colors.HexColor('#b5122a')
gold = colors.HexColor('#b8891f')
line = colors.HexColor('#d8d0c5')
ink = colors.HexColor('#17110d')
muted = colors.HexColor('#5d5147')
soft = colors.HexColor('#f7f2e9')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleMS', fontName='Helvetica-Bold', fontSize=24, leading=23, textColor=ink, spaceAfter=3))
styles.add(ParagraphStyle(name='HeadMS', fontName='Helvetica-Bold', fontSize=16, leading=17, textColor=ink, spaceAfter=6))
styles.add(ParagraphStyle(name='Tag', fontName='Helvetica-Bold', fontSize=8.8, leading=10, textColor=gold, uppercase=True, spaceAfter=8))
styles.add(ParagraphStyle(name='BodyMS', fontName='Helvetica', fontSize=9.5, leading=11.2, textColor=ink))
styles.add(ParagraphStyle(name='SmallMS', fontName='Helvetica', fontSize=8.2, leading=9.7, textColor=muted))
styles.add(ParagraphStyle(name='Phone', fontName='Helvetica-Bold', fontSize=25, leading=26, textColor=red))
styles.add(ParagraphStyle(name='BoxHead', fontName='Helvetica-Bold', fontSize=9.6, leading=10.4, textColor=ink))

def P(txt, style='BodyMS'):
    return Paragraph(txt, styles[style])

def box(content, border=line, top=None):
    t = Table([[content]], colWidths=[3.15*inch])
    cmds=[('BOX',(0,0),(-1,-1),0.65,border),('BACKGROUND',(0,0),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    if top: cmds.append(('LINEABOVE',(0,0),(-1,0),2.2,top))
    t.setStyle(TableStyle(cmds)); return t

def mini_case(title, price, rows):
    data=[[P(f'<b>{title}</b>','BoxHead'),P(f'<b>{price}</b>','BoxHead')]]
    for name, p in rows:
        data.append([P(name,'SmallMS'),P(f'<b>{p}</b>','SmallMS')])
    t=Table(data,colWidths=[1.13*inch,.36*inch])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),soft),('TEXTCOLOR',(1,0),(1,0),red),('BOX',(0,0),(-1,-1),.45,line),('INNERGRID',(0,0),(-1,-1),.25,line),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]))
    return t

def draw_page(canvas, doc):
    w,h=landscape(letter)
    canvas.saveState()
    canvas.setStrokeColor(red); canvas.setLineWidth(4); canvas.line(.25*inch,h-.15*inch,w-.25*inch,h-.15*inch)
    canvas.setStrokeColor(colors.HexColor('#aaa199')); canvas.setDash(3,3); canvas.setLineWidth(.7)
    canvas.line(w/3,.22*inch,w/3,h-.22*inch); canvas.line(2*w/3,.22*inch,2*w/3,h-.22*inch)
    canvas.restoreState()

# panel content
logo=Image(str(LOGO),width=1.02*inch,height=.64*inch)
photo=Image(str(PHOTO),width=3.15*inch,height=1.30*inch)
qr=Image(str(QR),width=.80*inch,height=.80*inch)

panel1=[Table([[logo,[P('Midwest Suppliers','TitleMS'),P('Meats & Seafood','BodyMS')]]],colWidths=[1.10*inch,2.00*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4)]),Spacer(1,16),photo,Spacer(1,16),box([P('<b>Restaurant-quality meats and seafood delivered to your door.</b>','BodyMS'),P('Home and business delivery across Rapid City, the Black Hills, Deadwood, and surrounding areas since 2020.','SmallMS')],border=red),Spacer(1,14),P(PHONE,'Phone'),Spacer(1,18),box([P('Free home delivery','BoxHead'),P('Stock the freezer without the grocery-store run.','SmallMS')],top=gold),Spacer(1,16),box([P('Free chest freezer','BoxHead'),P('Ask about a <b>free chest freezer</b> with select orders.','SmallMS')],top=red),Spacer(1,16),box([P('One-year guarantee','BoxHead'),P('Guaranteed for one full year from purchase for tenderness and quality. If dissatisfied, unused portions can be replaced.','SmallMS')])]

beef=[('Filet Mignon','$149'),('NY Strip','$89'),('Ranch Sirloin','$89'),('Rib Eye','$99'),('Porterhouse','$119'),('Sirloin Burgers','$79')]
pork=[('Center Cut Chops','$59'),('Porterhouse Chops','$69'),('Sirloin Roasts','$59'),('Bone-in Chops','$62'),('Italian Sausage','$57'),('Country Ribs','$55')]
sea=[('Jumbo Peeled Shrimp','$59'),('Un-peeled Shrimp','$55'),('Mahi Mahi Filet','$84'),('Sockeye Salmon','$99'),('Red Snapper','$74'),('Sea Scallops','$78')]
chick=[('Plain Breasts','$59'),('Lemon Pepper','$64'),('Italian Breasts','$64'),('Mild BBQ','$64'),('Chicken Tenders','$54'),('Chicken Fritters','$56')]
case_grid=Table([[mini_case('Big Beef','$624',beef),mini_case('Pork','$361',pork)],[mini_case('Seafood','$449',sea),mini_case('Chicken','$361',chick)]],colWidths=[1.56*inch,1.56*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),4)])
panel2=[P('MENU CASES','Tag'),case_grid,box([Table([[[P('Preferred Customer Combo','BoxHead'),P('Beef + Pork + Seafood + Chicken at $249.75 each','SmallMS')],P('$999','Phone')]],colWidths=[2.2*inch,.72*inch],style=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)])],border=ink),Spacer(1,3),P('Selections, prices, and availability may vary. Ask about veteran discounts, current deals, delivery options, and freezer offers.','SmallMS')]

qgrid=Table([[[P('Quality','BoxHead'),P('• USDA inspected<br/>• USDA Choice<br/>• Restaurant quality<br/>• 30–40% less fat','SmallMS')],[P('Freezer-ready','BoxHead'),P('• Flash frozen<br/>• Vacuum sealed<br/>• Individually wrapped<br/>• No freezer burn','SmallMS')]]],colWidths=[1.55*inch,1.55*inch],style=[('BOX',(0,0),(-1,-1),.45,line),('INNERGRID',(0,0),(-1,-1),.45,line),('BACKGROUND',(0,0),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)])
panel3=[P('WHY CUSTOMERS BUY','Tag'),P('Simple promise. Simple delivery.','HeadMS'),qgrid,Spacer(1,5),box([P('How to order','BoxHead'),P('1. Call and tell us what case, combo, or products you need.<br/>2. We confirm availability, pricing, and delivery timing.<br/>3. Your order is delivered to your home or business.','SmallMS')],top=red),box([P('Business accounts','BoxHead'),P('Restaurants, bars, lodges, offices, recurring orders, staff meals, and seasonal freezer fills.','SmallMS')],top=gold),box([Table([[qr,P(f'<b>Website:</b><br/>{URL}<br/><br/><b>Payments:</b> Major cards, Venmo/Cash App, checks. Returned check fee: $35.','SmallMS')]],colWidths=[.7*inch,2.25*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4)])])]

panel_table=Table([[panel1,panel2,panel3]],colWidths=[3.33*inch,3.33*inch,3.33*inch],rowHeights=[7.65*inch])
panel_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),16),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEAFTER',(0,0),(0,-1),.5,colors.HexColor('#aaa199')),('LINEAFTER',(1,0),(1,-1),.5,colors.HexColor('#aaa199'))]))

doc=SimpleDocTemplate(str(OUT),pagesize=landscape(letter),leftMargin=.25*inch,rightMargin=.25*inch,topMargin=.22*inch,bottomMargin=.2*inch,title='Midwest Suppliers One-Page Tri-Fold')
doc.build([panel_table],onFirstPage=draw_page,onLaterPages=draw_page)
print(OUT)
