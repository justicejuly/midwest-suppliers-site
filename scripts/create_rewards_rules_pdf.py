
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
OUT=Path('/opt/data/midwest-suppliers-site/customer-tracking/midwest-rewards-program-rules.pdf')
PHONE='605-675-9429'
SITE='justicejuly.github.io/midwest-suppliers-site'
red=colors.HexColor('#b5122a'); gold=colors.HexColor('#b8891f'); ink=colors.HexColor('#17110d'); line=colors.HexColor('#d8d0c5'); muted=colors.HexColor('#5d5147')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleMS',fontName='Helvetica-Bold',fontSize=30,leading=31,textColor=ink))
styles.add(ParagraphStyle(name='HeadMS',fontName='Helvetica-Bold',fontSize=15,leading=17,textColor=red,spaceBefore=14,spaceAfter=6))
styles.add(ParagraphStyle(name='BodyMS',fontName='Helvetica',fontSize=12,leading=15,textColor=ink))
styles.add(ParagraphStyle(name='SmallMS',fontName='Helvetica',fontSize=9,leading=11,textColor=muted))
styles.add(ParagraphStyle(name='Phone',fontName='Helvetica-Bold',fontSize=26,leading=28,textColor=red))
styles.add(ParagraphStyle(name='Script',fontName='Helvetica-Bold',fontSize=15,leading=18,textColor=ink))
def P(txt,style='BodyMS'): return Paragraph(txt,styles[style])
def box(content):
    t=Table([[content]],colWidths=[7.1*inch]); t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.8,line),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fffdf8')),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),('VALIGN',(0,0),(-1,-1),'TOP') ])); return t
def draw(c,doc):
    w,h=letter; c.saveState(); c.setStrokeColor(red); c.setLineWidth(5); c.line(doc.leftMargin,h-.25*inch,w-doc.rightMargin,h-.25*inch); c.setStrokeColor(gold); c.setLineWidth(2); c.line(doc.leftMargin,h-.31*inch,w-doc.rightMargin,h-.31*inch); c.restoreState()
story=[P('Midwest Rewards Club','TitleMS'),P('A simple repeat-customer and referral program for Midwest Suppliers Meats & Seafood.','BodyMS'),P(PHONE,'Phone'),Spacer(1,8)]
story.append(Table([[box([P('<b>Earn points</b><br/><font color="#b5122a"><b>1 point</b></font> for every <b>$25 spent</b>.')]), box([P('<b>Redeem rewards</b><br/><b>5 points</b> = $10 off<br/><b>10 points</b> = $25 off<br/><b>20 points</b> = $60 off or free add-on when available.')])]], colWidths=[3.55*inch,3.55*inch], style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8)]))
story += [P('Referral offer','HeadMS'), box([P('<font color="#b5122a"><b>Give $25, get $25.</b></font><br/>When a current customer refers a new customer who places their first order, the current customer gets <b>$25 off</b> their next order and the new customer gets <b>$25 off</b> their first order.')]), P('VIP customers','HeadMS'), P('• VIP after <b>3 completed orders</b> or <b>$1,000 lifetime spend</b>.<br/>• VIP customers get first notice of specials and priority delivery when available.'), P('Door-to-door script','HeadMS'), box([P('“Can I put you down for our Midwest Rewards Club? It’s free. You earn rewards when you order, and if you refer someone who buys, you both get $25 off.”','Script')]), Spacer(1,12), P(f'Rewards should be confirmed before purchase. Offers may change. Do not issue referral reward until the new customer completes their first order. Midwest Suppliers Meats & Seafood · {SITE}','SmallMS')]
doc=SimpleDocTemplate(str(OUT),pagesize=letter,leftMargin=.55*inch,rightMargin=.55*inch,topMargin=.55*inch,bottomMargin=.45*inch,title='Midwest Rewards Program Rules')
doc.build(story,onFirstPage=draw,onLaterPages=draw)
print(OUT)
