from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer, PageBreak
import qrcode

ROOT=Path('/opt/data/midwest-suppliers-site')
OUT=ROOT/'door-to-door-brochures'/'midwest-door-to-door-photo-menu-style.pdf'
LOGO=ROOT/'assets'/'knife-logo.jpg'
BADGE=ROOT/'assets'/'profile-logos'/'midwest-profile-logo-badge-red-black-gold-text-no-repeat.png'
QR=ROOT/'assets'/'site-qr.png'
PRIME=ROOT/'assets'/'door-to-door-prime-rib-plate.jpg'
MEATSEA=ROOT/'assets'/'door-to-door-meat-seafood-plate.jpg'
GRILL=ROOT/'assets'/'door-to-door-grill-steak.jpg'
URL='https://justicejuly.github.io/midwest-suppliers-site/'
PHONE='605-675-9429'
IG='@midwestsuppliersmeat'
if not QR.exists():
    qr=qrcode.QRCode(box_size=6,border=2); qr.add_data(URL); qr.make(fit=True); qr.make_image(fill_color='black',back_color='white').save(str(QR))
red=colors.HexColor('#b5122a'); gold=colors.HexColor('#b8891f'); ink=colors.HexColor('#17110d'); muted=colors.HexColor('#5d5147'); line=colors.HexColor('#d8d0c5'); soft=colors.HexColor('#f7f2e9'); cream=colors.HexColor('#fffdf8')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='PhotoTitle',fontName='Helvetica-Bold',fontSize=30,leading=29,textColor=red,spaceAfter=3))
styles.add(ParagraphStyle(name='PhotoHead',fontName='Helvetica-Bold',fontSize=13,leading=14,textColor=ink,spaceAfter=4))
styles.add(ParagraphStyle(name='PhotoLead',fontName='Helvetica-Bold',fontSize=11.5,leading=13.5,textColor=ink))
styles.add(ParagraphStyle(name='PhotoBody',fontName='Helvetica',fontSize=9.2,leading=10.7,textColor=ink))
styles.add(ParagraphStyle(name='PhotoSmall',fontName='Helvetica',fontSize=7.5,leading=8.7,textColor=muted))
styles.add(ParagraphStyle(name='PhotoKicker',fontName='Helvetica-Bold',fontSize=7.8,leading=9,textColor=gold,uppercase=True))
styles.add(ParagraphStyle(name='PhotoPhone',fontName='Helvetica-Bold',fontSize=27,leading=28,textColor=red))
styles.add(ParagraphStyle(name='BackTitlePhoto',fontName='Helvetica-Bold',fontSize=30,leading=31,alignment=1,textColor=ink))
styles.add(ParagraphStyle(name='BackBodyPhoto',fontName='Helvetica-Bold',fontSize=13,leading=16,alignment=1,textColor=muted))
styles.add(ParagraphStyle(name='CenterSmallPhoto',fontName='Helvetica',fontSize=9,leading=11,alignment=1,textColor=muted))

def P(t,s='PhotoBody'): return Paragraph(t,styles[s])
def box(flows,top=None,border=line,width=3.0*inch):
    t=Table([[flows]],colWidths=[width]); cmds=[('BOX',(0,0),(-1,-1),.6,border),('BACKGROUND',(0,0),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    if top: cmds.append(('LINEABOVE',(0,0),(-1,0),2.4,top))
    t.setStyle(TableStyle(cmds)); return t

def mini_case(title,price,rows):
    data=[[P(f'<b>{title}</b>','PhotoSmall'),P(f'<b>{price}</b>','PhotoSmall')]]
    for n,p in rows: data.append([P(n,'PhotoSmall'),P(f'<b>{p}</b>','PhotoSmall')])
    t=Table(data,colWidths=[1.22*inch,.42*inch])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),soft),('TEXTCOLOR',(1,0),(1,0),red),('BOX',(0,0),(-1,-1),.45,line),('INNERGRID',(0,0),(-1,-1),.2,line),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2.1),('BOTTOMPADDING',(0,0),(-1,-1),2.1)])); return t
beef=[('Filet Mignon','$149'),('NY Strip','$89'),('Ranch Sirloin','$89'),('Rib Eye','$99'),('Porterhouse','$119'),('Sirloin Burgers','$79')]
sea=[('Jumbo Shrimp','$59'),('Un-peeled Shrimp','$55'),('Mahi Mahi','$84'),('Sockeye Salmon','$99'),('Red Snapper','$74'),('Sea Scallops','$78')]
pork=[('Center Cut Chops','$59'),('Porterhouse Chops','$69'),('Sirloin Roasts','$59'),('Italian Sausage','$57'),('Country Ribs','$55')]
chick=[('Plain Breasts','$59'),('Lemon Pepper','$64'),('Italian Breasts','$64'),('Chicken Tenders','$54'),('Chicken Fritters','$56')]

def draw(c,doc):
    w,h=letter; c.saveState(); c.setFillColor(cream); c.rect(0,0,w,h,fill=1,stroke=0); c.setStrokeColor(line); c.rect(.22*inch,.22*inch,w-.44*inch,h-.44*inch,stroke=1,fill=0); c.restoreState()

def front():
    logo=Image(str(LOGO),1.05*inch,.66*inch); prime=Image(str(PRIME),4.75*inch,1.9*inch); meatsea=Image(str(MEATSEA),2.25*inch,.9*inch); grill=Image(str(GRILL),2.25*inch,.9*inch); qr=Image(str(QR),.8*inch,.8*inch)
    story=[Table([[logo,[P('Rapid City · Black Hills · Deadwood Area','PhotoKicker'),P('Restaurant-quality meats delivered','PhotoTitle'),P('Freezer-ready meats and seafood for homes, restaurants, and businesses.','PhotoLead')]]],colWidths=[1.15*inch,6.1*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),5)]),Spacer(1,8)]
    photos=Table([[prime,[meatsea,Spacer(1,4),grill]]],colWidths=[4.85*inch,2.35*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(0,0),1.2,red),('BOX',(1,0),(1,0),.6,line),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)])
    story += [photos,Spacer(1,8)]
    cases=Table([[mini_case('Big Beef','$624',beef),mini_case('Seafood','$449',sea)],[mini_case('Pork','$361',pork),mini_case('Chicken','$361',chick)]],colWidths=[1.82*inch,1.82*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),5)])
    combo=box([P('Preferred Customer Combo','PhotoHead'),P('Beef + Pork + Seafood + Chicken at $249.75 each<br/><b>$999</b>','PhotoBody')],border=ink,width=3.85*inch)
    left=[P('Case menu','PhotoHead'),cases,combo]
    right=[box([P('Why customers buy','PhotoHead'),P('USDA inspected, restaurant quality, flash frozen, vacuum sealed, individually wrapped, and backed by a one-year tenderness and quality guarantee.','PhotoBody')],top=red,width=3.05*inch),Spacer(1,5),box([P('Ask about','PhotoHead'),P('Free home delivery · veteran discounts · current deals · rewards · freezer offers · business orders.','PhotoSmall')],top=gold,width=3.05*inch),Spacer(1,5),box([P('How to order','PhotoHead'),P('Call/text what you are interested in. We confirm current selections, prices, discounts, and delivery options.','PhotoSmall')],width=3.05*inch)]
    story.append(Table([[left,right]],colWidths=[4.05*inch,3.15*inch],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
    story.append(Spacer(1,6))
    band=Table([[P('<b>Catch us in your neighborhood.</b>','PhotoHead'),P('Ask what is available today — cases, combos, delivery, rewards, veteran discounts, and freezer deals.','PhotoSmall')]],colWidths=[3.3*inch,3.7*inch])
    band.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,gold),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fff9e8')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)])); story.append(band)
    story.append(Spacer(1,6))
    story.append(Table([[[P(PHONE,'PhotoPhone'),P('Selections, prices, and availability may vary. Ask about veteran discounts, current deals, delivery options, and freezer offers.','PhotoSmall')],qr]],colWidths=[6.25*inch,.85*inch],style=[('LINEABOVE',(0,0),(-1,0),1,line),('TOPPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    return story

def back():
    badge=Image(str(BADGE),2.5*inch,2.5*inch)
    return [Spacer(1,1.15*inch),Table([[badge]],colWidths=[7.2*inch],style=[('ALIGN',(0,0),(-1,-1),'CENTER')]),Spacer(1,.25*inch),P('Midwest Suppliers<br/>Meats & Seafood','BackTitlePhoto'),Spacer(1,.12*inch),P('Meats · Seafood · Freezer cases · Home & business delivery','BackBodyPhoto'),Spacer(1,.16*inch),P(PHONE,'PhotoPhone'),P(URL.replace('https://',''),'CenterSmallPhoto'),Spacer(1,.08*inch),P(f'Instagram {IG}','BackBodyPhoto'),Spacer(1,.18*inch),P('Serving Rapid City, the Black Hills, Deadwood, and surrounding areas.','CenterSmallPhoto')]

doc=SimpleDocTemplate(str(OUT),pagesize=letter,leftMargin=.42*inch,rightMargin=.42*inch,topMargin=.38*inch,bottomMargin=.35*inch,title='Midwest Suppliers Photo Door-to-Door Brochure')
doc.build(front()+[PageBreak()]+back(),onFirstPage=draw,onLaterPages=draw)
print(OUT)
