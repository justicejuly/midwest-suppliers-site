from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path('/opt/data/midwest-suppliers-site')
OUT_DIR = ROOT / 'business-outreach'
OUT_DIR.mkdir(exist_ok=True)
OUT = OUT_DIR / 'midwest-suppliers-cold-call-script.pdf'

red = colors.HexColor('#b5122a')
gold = colors.HexColor('#b8891f')
ink = colors.HexColor('#17110d')
muted = colors.HexColor('#5d5147')
line = colors.HexColor('#d8d0c5')
cream = colors.HexColor('#fffdf8')
soft = colors.HexColor('#fff6df')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MSTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=22, leading=25, textColor=red, spaceAfter=6))
styles.add(ParagraphStyle(name='MSSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=muted, spaceAfter=10))
styles.add(ParagraphStyle(name='MSHead', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13.5, leading=15, textColor=ink, spaceBefore=6, spaceAfter=5))
styles.add(ParagraphStyle(name='MSBody', parent=styles['Normal'], fontName='Helvetica', fontSize=9.4, leading=12, textColor=ink, spaceAfter=5))
styles.add(ParagraphStyle(name='MSScript', parent=styles['Normal'], fontName='Helvetica', fontSize=9.2, leading=11.8, textColor=ink))
styles.add(ParagraphStyle(name='MSBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.4, leading=12, textColor=ink, spaceAfter=4))
styles.add(ParagraphStyle(name='MSNote', parent=styles['Normal'], fontName='Helvetica', fontSize=8.2, leading=10, textColor=muted))
styles.add(ParagraphStyle(name='MSPhone', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=17, textColor=red, alignment=1))

P = lambda text, style='MSBody': Paragraph(text, styles[style])

def box(title, body, accent=red):
    parts = [P(title, 'MSHead')]
    if isinstance(body, list):
        parts += [P(x, 'MSScript') for x in body]
    else:
        parts.append(P(body, 'MSScript'))
    t = Table([[parts]], colWidths=[7.15*inch])
    t.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),0.7,line),
        ('LINEABOVE',(0,0),(-1,0),3,accent),
        ('BACKGROUND',(0,0),(-1,-1),colors.white),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    return t

story = []
story.append(P('Midwest Suppliers Cold-Call Script', 'MSTitle'))
story.append(P('For restaurants, lodges, bars, casinos, and local kitchens without a public email address.', 'MSSub'))

story.append(box('Main opening script', [
    '“Hi, this is Chuck with Midwest Suppliers Meats & Seafood. We’re a local meat and seafood supplier serving Rapid City, Deadwood, the Black Hills, and surrounding areas. I was hoping to find out who handles food purchasing or vendor conversations for your kitchen.”',
    '<b>Pause and let them answer.</b>'
], red))
story.append(Spacer(1, 7))

story.append(box('If they ask what it is about', [
    '“We deliver meats and seafood for homes and businesses, and I’m reaching out to restaurants, lodges, and local kitchens to see if we can help with beef, pork, chicken, seafood, freezer-ready cases, or recurring orders.”',
    'Then ask: “Who would be the best person to talk to about that?”'
], gold))
story.append(Spacer(1, 7))

story.append(box('If the right person is not there', [
    '“No problem. What’s the best way to reach them — phone, email, or should I call back at a better time?”',
    'If they give an email: “Perfect, thank you. I’ll send over a short introduction and our contact info. Is there anything specific I should mention?”',
    'If they give a time: “Great, I’ll try back around then. Thank you.”'
], red))
story.append(Spacer(1, 7))

story.append(box('If you get the owner, chef, manager, or buyer', [
    '“Hi, this is Chuck with Midwest Suppliers Meats & Seafood. We deliver restaurant-quality meats and seafood around Rapid City, Deadwood, the Black Hills, and surrounding areas. I’m reaching out because we may be able to help with beef, pork, chicken, seafood, freezer-ready cases, or recurring restaurant orders.”',
    'Then ask: “Do you currently have someone you’re happy with for meat and seafood, or would it be worth sending you our information?”'
], gold))
story.append(Spacer(1, 7))

story.append(box('If they sound interested', [
    '“Great. I can send over a short menu/info sheet, or I can stop by with a brochure. What works better for you?”',
    '<b>Collect:</b> contact name, best email, best phone, best follow-up time, products they buy most, and who makes purchasing decisions.'
], red))
story.append(Spacer(1, 7))

story.append(box('If they already have a supplier', [
    '“That makes sense. Most places do. We’re not trying to replace anything overnight — we just like to be a backup option if pricing, availability, or delivery ever becomes an issue. Would it be okay if I sent our info so you have us on hand?”'
], gold))
story.append(Spacer(1, 7))

story.append(box('If they are not interested', [
    '“No problem at all. Thanks for taking the call. If anything changes or you ever need another option for meat or seafood delivery, Midwest Suppliers is local and easy to reach at 605-675-9429.”'
], red))
story.append(Spacer(1, 7))

# two columns for quick answers
left = [P('If they ask what you offer', 'MSHead'), P('“We can help with beef, pork, chicken, seafood, freezer cases, and larger restaurant or business orders. Selections, prices, and availability can vary, so we usually confirm current options directly before quoting.”', 'MSScript')]
right = [P('If they ask for pricing', 'MSHead'), P('“I can send over the current menu and then confirm what’s available. For restaurants or larger orders, it’s usually best to talk through what cuts and volume you use so we’re quoting the right thing.”', 'MSScript')]
t = Table([[left, right]], colWidths=[3.52*inch, 3.52*inch])
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),0.7,line),('INNERGRID',(0,0),(-1,-1),0.5,line),('BACKGROUND',(0,0),(-1,-1),colors.white),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story.append(t)
story.append(Spacer(1, 7))

story.append(box('Voicemail script', [
    '“Hi, this is Chuck with Midwest Suppliers Meats & Seafood. We deliver meats and seafood around Rapid City, Deadwood, the Black Hills, and surrounding areas. I’m calling to see who handles food purchasing or vendor conversations for your kitchen. You can call or text me back at 605-675-9429. Again, that’s Chuck with Midwest Suppliers, 605-675-9429. Thank you.”'
], gold))
story.append(Spacer(1, 7))

story.append(box('Text after voicemail', [
    '“Hi, this is Chuck with Midwest Suppliers Meats & Seafood. I left a quick voicemail about meat/seafood delivery for restaurants and businesses. Who would be the best person to talk with about food purchasing or vendor info? 605-675-9429”'
], red))
story.append(Spacer(1, 7))

statuses = ['Wrong number', 'No answer', 'Left voicemail', 'Call back later', 'Need buyer/manager name', 'Got email', 'Sent info', 'Interested', 'Not interested', 'Follow up in 1 week', 'Closed / not a fit']
status_text = ' · '.join(statuses)
story.append(box('What to write down after each call', [status_text], gold))
story.append(Spacer(1, 6))

story.append(P('Simple call goal', 'MSHead'))
goals = Table([
    [P('1. Buyer/manager name', 'MSBold'), P('2. Email address', 'MSBold'), P('3. Best callback time', 'MSBold')],
    [P('4. Permission to send info', 'MSBold'), P('5. Clear yes/no', 'MSBold'), P('A call is successful if you get any one of these.', 'MSNote')],
], colWidths=[2.35*inch, 2.35*inch, 2.35*inch])
goals.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.7,line),('INNERGRID',(0,0),(-1,-1),0.5,line),('BACKGROUND',(0,0),(-1,-1),soft),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.append(goals)
story.append(Spacer(1, 8))
story.append(P('Midwest Suppliers Meats & Seafood · Call/Text 605-675-9429 · midwestsuppliersmeat@gmail.com', 'MSPhone'))

doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.55*inch, rightMargin=0.55*inch, topMargin=0.45*inch, bottomMargin=0.45*inch, title='Midwest Suppliers Cold Call Script')
doc.build(story)
print(OUT)
