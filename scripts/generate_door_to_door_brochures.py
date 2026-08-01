from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer, PageBreak
from reportlab.pdfgen import canvas
import qrcode

ROOT = Path('/opt/data/midwest-suppliers-site')
OUT = ROOT / 'door-to-door-brochures'
OUT.mkdir(exist_ok=True)
LOGO = ROOT / 'assets' / 'knife-logo.jpg'
BADGE = ROOT / 'assets' / 'profile-logos' / 'midwest-profile-logo-badge-red-black-gold-text-no-repeat.png'
FIRST_BACK_LOGO = ROOT / 'assets' / 'midwest-brochure-back-logo.jpg'
DISPLAY_DOMAIN = 'midwestsuppliersmeat.com'
QR = ROOT / 'assets' / 'site-qr.png'
URL = 'https://justicejuly.github.io/midwest-suppliers-site/'
PHONE = '605-675-9429'
IG = '@midwestsuppliersmeat'

if not QR.exists():
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(URL); qr.make(fit=True)
    qr.make_image(fill_color='black', back_color='white').save(str(QR))

red=colors.HexColor('#b5122a'); gold=colors.HexColor('#b8891f'); ink=colors.HexColor('#17110d')
muted=colors.HexColor('#5d5147'); line=colors.HexColor('#d8d0c5'); blue=colors.HexColor('#245f73')
cream=colors.HexColor('#fffdf8'); soft=colors.HexColor('#f7f2e9'); black=colors.HexColor('#090504')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='MSTitleBlue', fontName='Helvetica-Bold', fontSize=28, leading=27, textColor=blue, spaceAfter=4))
styles.add(ParagraphStyle(name='MSTitleRed', fontName='Helvetica-Bold', fontSize=34, leading=32, textColor=red, spaceAfter=4))
styles.add(ParagraphStyle(name='MSHead', fontName='Helvetica-Bold', fontSize=14, leading=15, textColor=ink, spaceAfter=5))
styles.add(ParagraphStyle(name='MSSmall', fontName='Helvetica', fontSize=7.7, leading=9.0, textColor=muted))
styles.add(ParagraphStyle(name='MSBody', fontName='Helvetica', fontSize=9.4, leading=11.0, textColor=ink))
styles.add(ParagraphStyle(name='MSLead', fontName='Helvetica-Bold', fontSize=11.8, leading=14, textColor=ink))
styles.add(ParagraphStyle(name='MSKicker', fontName='Helvetica-Bold', fontSize=7.8, leading=9, textColor=gold, uppercase=True))
styles.add(ParagraphStyle(name='MSPhone', fontName='Helvetica-Bold', fontSize=28, leading=29, textColor=red))
styles.add(ParagraphStyle(name='MSBackTitle', fontName='Helvetica-Bold', fontSize=30, leading=31, alignment=1, textColor=ink))
styles.add(ParagraphStyle(name='MSBackBody', fontName='Helvetica-Bold', fontSize=13, leading=16, alignment=1, textColor=muted))
styles.add(ParagraphStyle(name='MSCenterSmall', fontName='Helvetica', fontSize=9, leading=11, alignment=1, textColor=muted))

def P(txt, style='MSBody'):
    return Paragraph(txt, styles[style])

def box(flowables, border=line, top=None, bg=colors.white, width=3.0*inch):
    t=Table([[flowables]], colWidths=[width])
    cmds=[('BOX',(0,0),(-1,-1),.6,border),('BACKGROUND',(0,0),(-1,-1),bg),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    if top: cmds.append(('LINEABOVE',(0,0),(-1,0),2.5,top))
    t.setStyle(TableStyle(cmds)); return t

def mini_case(title, price, rows):
    data=[[P(f'<b>{title}</b>','MSSmall'),P(f'<b>{price}</b>','MSSmall')]]
    for n,p in rows:
        data.append([P(n,'MSSmall'),P(f'<b>{p}</b>','MSSmall')])
    t=Table(data,colWidths=[1.23*inch,.42*inch])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),soft),('TEXTCOLOR',(1,0),(1,0),red),('BOX',(0,0),(-1,-1),.45,line),('INNERGRID',(0,0),(-1,-1),.2,line),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2.3),('BOTTOMPADDING',(0,0),(-1,-1),2.3)]))
    return t

beef=[('Filet Mignon','$149'),('NY Strip','$89'),('Ranch Sirloin','$89'),('Rib Eye','$99'),('Porterhouse','$119'),('Sirloin Burgers','$79')]
pork=[('Center Cut Chops','$59'),('Porterhouse Chops','$69'),('Sirloin Roasts','$59'),('Bone-in Chops','$62'),('Italian Sausage','$57'),('Country Ribs','$55')]
sea=[('Jumbo Shrimp','$59'),('Un-peeled Shrimp','$55'),('Mahi Mahi','$84'),('Sockeye Salmon','$99'),('Red Snapper','$74'),('Sea Scallops','$78')]
chick=[('Plain Breasts','$59'),('Lemon Pepper','$64'),('Italian Breasts','$64'),('Mild BBQ','$64'),('Chicken Tenders','$54'),('Chicken Fritters','$56')]

def draw_border(c, doc, style='playful'):
    w,h=letter; c.saveState(); c.setFillColor(cream); c.rect(0,0,w,h,fill=1,stroke=0)
    c.setStrokeColor(line); c.rect(.22*inch,.22*inch,w-.44*inch,h-.44*inch,stroke=1,fill=0)
    if style=='playful':
        c.setStrokeColor(blue); c.setFillColor(blue); c.setFont('Helvetica-Bold',34); c.setFillAlpha(.12)
        c.drawString(6.7*inch,10.12*inch,'fish'); c.drawString(.35*inch,8.0*inch,'shrimp'); c.drawString(6.55*inch,1.1*inch,'crab')
        c.setFillAlpha(1)
    else:
        c.setFillColor(black); c.rect(0,h-.22*inch,w,.22*inch,fill=1,stroke=0)
        c.setFillColor(red); c.rect(2.8*inch,h-.22*inch,2.8*inch,.22*inch,fill=1,stroke=0)
        c.setFillColor(gold); c.rect(5.6*inch,h-.22*inch,2.9*inch,.22*inch,fill=1,stroke=0)
        c.setStrokeColor(colors.Color(red.red,red.green,red.blue,alpha=.25)); c.circle(7.1*inch,9.1*inch,.5*inch,stroke=1,fill=0); c.circle(7.1*inch,9.1*inch,.28*inch,stroke=1,fill=0)
    c.restoreState()

def front_story(kind):
    is_play=kind=='playful'
    logo=Image(str(FIRST_BACK_LOGO if is_play else LOGO),width=(.78*inch if is_play else 1.05*inch),height=(.78*inch if is_play else .66*inch))
    qr=Image(str(QR),width=.8*inch,height=.8*inch)
    title_style='MSTitleBlue' if is_play else 'MSTitleRed'
    title='Meats & seafood delivered' if is_play else 'Fill your freezer'
    kicker='Rapid City · Deadwood · The Black Hills' if is_play else 'Door-to-door delivery menu'
    lead='Stock your freezer without the grocery-store run. Midwest Suppliers delivers freezer-ready meats and seafood to homes, restaurants, and businesses.' if is_play else 'Restaurant-quality meats and seafood delivered across Rapid City, Deadwood, the Black Hills, and surrounding areas.'
    story=[]
    story.append(Table([[logo,[P(kicker,'MSKicker'),P(title,title_style),P(lead,'MSLead')]]],colWidths=[1.15*inch,6.15*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),5)]))
    story.append(Spacer(1,10))
    if is_play:
        story.append(box([P('Free home delivery  •  Ask about veteran discounts  •  Current deals  •  Freezer offers','MSLead')],border=blue,bg=colors.HexColor('#f4fbfb'),width=7.25*inch))
    else:
        offers=Table([[box([P('Free delivery','MSHead'),P('Home and business orders.','MSSmall')],top=red,width=2.25*inch),box([P('Veterans','MSHead'),P('Ask about veteran discounts.','MSSmall')],top=gold,width=2.25*inch),box([P('Freezer offer','MSHead'),P('Ask about select orders.','MSSmall')],width=2.25*inch)]],colWidths=[2.42*inch,2.42*inch,2.42*inch])
        offers.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),5)])); story.append(offers)
    story.append(Spacer(1,10))
    cases=Table([[mini_case('Big Beef','$624',beef),mini_case('Seafood' if is_play else 'Pork','$449' if is_play else '$361',sea if is_play else pork)],[mini_case('Pork' if is_play else 'Seafood','$361' if is_play else '$449',pork if is_play else sea),mini_case('Chicken','$361',chick)]],colWidths=[1.83*inch,1.83*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)])
    if is_play:
        right=[box([P('How it works','MSHead'),P('1. Call/text what you are interested in.<br/>2. We confirm current selections, prices, discounts, and delivery options.<br/>3. We deliver to your home or business.','MSBody')],border=blue,top=blue,width=3.0*inch),Spacer(1,6),box([P('Quality promise','MSHead'),P('USDA inspected · USDA Choice · restaurant quality · flash frozen · vacuum sealed · individually wrapped · no freezer burn.','MSSmall')],top=gold,width=3.0*inch),Spacer(1,6),box([P('One-year guarantee','MSHead'),P('Guaranteed for tenderness and quality. If dissatisfied, Midwest Suppliers will replace any unused portion.','MSSmall')],top=red,width=3.0*inch),Spacer(1,6),box([P('Freezer offer','MSHead'),P('Ask about a free chest freezer with select orders.','MSSmall')],width=3.0*inch)]
    else:
        right=[box([P('Why buy from us?','MSHead'),P('USDA inspected, restaurant quality, flash frozen, vacuum sealed, individually wrapped, and backed by a one-year tenderness and quality guarantee.','MSBody')],top=red,width=3.0*inch),Spacer(1,7),box([P('Preferred Customer Combo','MSHead'),P('Beef + Pork + Seafood + Chicken<br/><b>$999</b>','MSBody')],border=ink,width=3.0*inch),Spacer(1,7),box([P('Perfect for','MSHead'),P('Families · freezer fills · restaurants · bars · lodges · offices · recurring business orders.','MSSmall')],top=gold,width=3.0*inch),Spacer(1,7),box([P('Order steps','MSHead'),P('Call/text. Confirm current selections and pricing. Schedule delivery.','MSSmall')],width=3.0*inch)]
    grid=Table([[cases,right]],colWidths=[4.05*inch,3.15*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)])
    story.append(grid)
    story.append(Spacer(1,10))
    band = Table([[P('<b>Catch us in your neighborhood.</b>', 'MSHead'), P('Ask what is available today — cases, combos, delivery, rewards, veteran discounts, and freezer deals.', 'MSSmall')]], colWidths=[3.25*inch,3.75*inch])
    band.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.1,gold),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fff9e8')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('TEXTCOLOR',(0,0),(0,0),red)]))
    story.append(band)
    story.append(Spacer(1,8))
    cta=Table([[[P(PHONE,'MSPhone'),P('Selections, prices, and availability may vary. Ask about veteran discounts, current deals, delivery options, and freezer offers.','MSSmall')],qr]],colWidths=[6.25*inch,.85*inch],style=[('LINEABOVE',(0,0),(-1,0),1,line),('TOPPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'MIDDLE')])
    story.append(cta)
    return story

def back_story(kind='playful'):
    qr=Image(str(QR),width=1.05*inch,height=1.05*inch)
    if kind == 'playful':
        badge=Image(str(FIRST_BACK_LOGO),width=3.05*inch,height=3.05*inch)
        return [Spacer(1,.72*inch),Table([[badge]],colWidths=[7.2*inch],style=[('ALIGN',(0,0),(-1,-1),'CENTER')]),Spacer(1,.22*inch),P('Midwest Suppliers<br/>Meats & Seafood','MSBackTitle'),Spacer(1,.12*inch),P('Delivered to homes and businesses across Rapid City, Deadwood, the Black Hills, and surrounding areas.','MSBackBody'),Spacer(1,.14*inch),P(PHONE,'MSPhone'),Spacer(1,.10*inch),Table([[qr]],colWidths=[7.2*inch],style=[('ALIGN',(0,0),(-1,-1),'CENTER')]),Spacer(1,.05*inch),P(DISPLAY_DOMAIN,'MSBackBody'),Spacer(1,.14*inch),P('Scan the QR code to visit the website, or call/text to ask about current availability, delivery, rewards, veteran discounts, deals, and freezer offers.','MSCenterSmall')]
    badge=Image(str(BADGE),width=2.5*inch,height=2.5*inch)
    return [Spacer(1,1.15*inch),Table([[badge]],colWidths=[7.2*inch],style=[('ALIGN',(0,0),(-1,-1),'CENTER')]),Spacer(1,.25*inch),P('Midwest Suppliers<br/>Meats & Seafood','MSBackTitle'),Spacer(1,.12*inch),P('Delivered to homes and businesses across Rapid City, Deadwood, the Black Hills, and surrounding areas.','MSBackBody'),Spacer(1,.16*inch),P(PHONE,'MSPhone'),P(URL.replace('https://',''),'MSCenterSmall'),Spacer(1,.08*inch),P(f'Instagram {IG}','MSBackBody'),Spacer(1,.18*inch),P('Scan the front QR code or call/text to ask about current availability, delivery, rewards, veteran discounts, deals, and freezer offers.','MSCenterSmall')]

def build(kind, filename):
    path=OUT/filename
    doc=SimpleDocTemplate(str(path),pagesize=letter,leftMargin=.42*inch,rightMargin=.42*inch,topMargin=.42*inch,bottomMargin=.38*inch,title=filename)
    story=front_story(kind)+[PageBreak()]+back_story(kind)
    doc.build(story,onFirstPage=lambda c,d: draw_border(c,d,kind),onLaterPages=lambda c,d: draw_border(c,d,kind))
    print(path)

build('playful','midwest-door-to-door-playful-seafood-style.pdf')
build('bold','midwest-door-to-door-bold-meat-style.pdf')
