from pathlib import Path
import base64, io, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

root=Path('.')
hero=base64.b64decode(root.joinpath('hero.b64').read_text().strip())
hero_b64=base64.b64encode(hero).decode()
tpl=root.joinpath('site-template.html').read_text()
root.joinpath('index.html').write_text(tpl.replace('__HERO_DATA__',hero_b64))

# OG card
im=Image.open(io.BytesIO(hero)).convert('RGB')
og=Image.new('RGB',(1200,630),'#15332A')
scale=max(660/im.width,630/im.height)
p=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)
left=max(0,(p.width-660)//2); top=max(0,(p.height-630)//2)
p=p.crop((left,top,left+660,top+630)); og.paste(p,(540,0))
ov=Image.new('RGBA',(1200,630),(0,0,0,0)); od=ImageDraw.Draw(ov)
for i in range(115):
    a=int(255*(1-i/114)); od.line((540+i,0,540+i,630),fill=(21,51,42,a),width=1)
og=Image.alpha_composite(og.convert('RGBA'),ov).convert('RGB')
d=ImageDraw.Draw(og)
serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
serifb='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
serifi='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'
sans='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fw=ImageFont.truetype(serifb,48); fi=ImageFont.truetype(serifi,48); fh=ImageFont.truetype(serif,63); fs=ImageFont.truetype(serifi,24); fu=ImageFont.truetype(sans,20)
x,y=50,48; part='Bick, Berry '; d.text((x,y),part,font=fw,fill='#F4EFE3'); xx=x+d.textlength(part,font=fw); d.text((xx,y),'&',font=fi,fill='#E0B04A'); xx+=d.textlength('&',font=fi); d.text((xx,y),' Ross',font=fw,fill='#F4EFE3')
d.text((50,158),'Life Cycle',font=fh,fill='#F4EFE3'); d.text((50,228),'Assessment',font=fh,fill='#F4EFE3')
d.text((52,322),'for wood, biomass & clean-energy projects',font=fs,fill='#E0B04A')
d.text((52,548),'bbr.northeastforests.com',font=fu,fill='#E0B04A')
og.save('og-card.jpg','JPEG',quality=86,optimize=True,progressive=True)

# Four-page landscape PDF companion brochure
W,H=landscape(letter)
forest=HexColor('#15332A'); green2=HexColor('#1F4538'); gold=HexColor('#E0B04A'); cream=HexColor('#F4EFE3'); paper=HexColor('#F8F6F1'); ink=HexColor('#1A2A24'); body=HexColor('#3A4842'); sage=HexColor('#B4C7A2'); tint=HexColor('#E8EDE3')
c=canvas.Canvas('brochure.pdf',pagesize=(W,H))

def wrap(txt,font,size,maxw):
    words=txt.split(); lines=[]; line=''
    for w in words:
        t=(line+' '+w).strip()
        if stringWidth(t,font,size)<=maxw: line=t
        else:
            if line: lines.append(line)
            line=w
    if line: lines.append(line)
    return lines
def draw_lines(txt,x,y,maxw,font='Helvetica',size=11,color=body,leading=14):
    c.setFillColor(color); c.setFont(font,size)
    for ln in wrap(txt,font,size,maxw):
        c.drawString(x,y,ln); y-=leading
    return y
def wordmark(x,y,size=28,dark=False):
    c.setFont('Times-Bold',size); c.setFillColor(ink if dark else cream); c.drawString(x,y,'Bick, Berry ')
    xx=x+stringWidth('Bick, Berry ','Times-Bold',size); c.setFillColor(HexColor('#8F6614') if dark else gold); c.setFont('Times-BoldItalic',size); c.drawString(xx,y,'&')
    xx+=stringWidth('&','Times-BoldItalic',size); c.setFillColor(ink if dark else cream); c.setFont('Times-Bold',size); c.drawString(xx,y,' Ross')

# p1
c.setFillColor(forest); c.rect(0,0,W,H,fill=1,stroke=0); wordmark(54,H-68,28)
c.setFillColor(sage); c.setFont('Helvetica-Bold',9); c.drawString(54,H-90,'FORESTRY  ·  ECONOMICS  ·  ENERGY  ·  POLICY')
c.setFillColor(cream); c.setFont('Times-Roman',48); c.drawString(54,H-190,'Life Cycle'); c.drawString(54,H-242,'Assessment')
c.setFillColor(gold); c.setFont('Times-Italic',17); c.drawString(54,H-282,'for wood, biomass & clean-energy projects')
c.setFillColor(cream); c.setFont('Helvetica',14); c.drawString(54,H-340,'Tax-credit readiness.'); c.drawString(54,H-363,'Defensible carbon accounting.'); c.drawString(54,H-386,'Better project decisions.')
c.setFillColor(sage); c.setFont('Helvetica-Oblique',10); c.drawString(54,95,'Independent analysis for projects that must withstand technical, financial and regulatory scrutiny.')
c.setFillColor(gold); c.setFont('Helvetica-Bold',10); c.drawString(54,60,'bbr.northeastforests.com')
# rings
cx,cy=650,300
for i,r in enumerate(range(32,250,15)):
    c.setStrokeColor(gold if i%2==0 else sage); c.setLineWidth(.7); c.ellipse(cx-r*1.25,cy-r,cx+r*1.25,cy+r,stroke=1,fill=0)
c.showPage()

# p2
c.setFillColor(paper); c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(HexColor('#8F6614')); c.setFont('Helvetica-Bold',10); c.drawString(50,H-55,'WHY AN LCA?')
c.setFillColor(ink); c.setFont('Times-Bold',29); c.drawString(50,H-93,'More than a'); c.drawString(50,H-126,'carbon number.')
c.setFillColor(body); c.setFont('Helvetica',11); c.drawString(470,H-100,'A strong LCA can create major tax, financing'); c.drawString(470,H-116,'and project-value benefits.')
c.setFillColor(forest); c.roundRect(50,255,300,150,10,fill=1,stroke=0); c.setFillColor(gold); c.setFont('Helvetica-Bold',9); c.drawString(68,382,'§45Y · CLEAN ELECTRICITY PRODUCTION'); c.setFont('Times-Bold',28); c.setFillColor(cream); c.drawString(68,337,'0.6¢'); c.setFillColor(gold); c.drawString(190,337,'3.1¢'); c.setFillColor(cream); c.setFont('Helvetica',9); c.drawString(68,317,'per kWh, base'); c.drawString(190,317,'2026 increased amount')
c.setFillColor(forest); c.roundRect(50,80,300,150,10,fill=1,stroke=0); c.setFillColor(gold); c.setFont('Helvetica-Bold',9); c.drawString(68,207,'§48E · CLEAN ELECTRICITY INVESTMENT'); c.setFont('Times-Bold',28); c.setFillColor(cream); c.drawString(68,162,'6%'); c.setFillColor(gold); c.drawString(190,162,'30%'); c.setFillColor(cream); c.setFont('Helvetica',9); c.drawString(68,142,'base credit'); c.drawString(190,142,'with qualifying labor rules')
titles=['Tax & financing readiness','Project strategy before filing','Operational insight','Reusable evidence base']; bodies=['Traceable emissions framework and evidence record.','Test assumptions before expensive commitments.','Identify emissions, cost and operational drivers.','Reuse the evidence base for grants, reporting and diligence.']
y=390
for i,(t,b) in enumerate(zip(titles,bodies),1):
    c.setFillColor(HexColor('#8F6614')); c.setFont('Times-Bold',20); c.drawString(400,y,f'{i:02d}')
    c.setFillColor(ink); c.setFont('Times-Bold',14); c.drawString(445,y+3,t); draw_lines(b,445,y-17,290,size=10); y-=75
c.showPage()

# p3
c.setFillColor(paper); c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(HexColor('#8F6614')); c.setFont('Helvetica-Bold',10); c.drawString(50,H-55,'OUR PROCESS')
c.setFillColor(ink); c.setFont('Times-Bold',28); c.drawString(50,H-95,'From messy project data to a defensible LCA.')
steps=[('01','Scope'),('02','Evidence'),('03','Model'),('04','Stress-test'),('05','Package')]
for idx,(n,t) in enumerate(steps):
    x=55+idx*145; c.setFillColor(gold); c.circle(x,H-175,20,fill=1,stroke=0); c.setFillColor(forest); c.setFont('Times-Bold',12); c.drawCentredString(x,H-180,n); c.setFillColor(ink); c.setFont('Times-Bold',12); c.drawString(x-20,H-215,t)
c.setFillColor(forest); c.roundRect(50,85,330,190,14,fill=1,stroke=0); c.setFillColor(gold); c.setFont('Helvetica-Bold',9); c.drawString(70,250,'THE BICK, BERRY & ROSS LCA WORKBENCH'); c.setFillColor(cream); c.setFont('Times-Bold',15); c.drawString(70,220,'A proprietary workflow for forest-products'); c.drawString(70,201,'and wood-energy projects.')
for j,t in enumerate(['Requirements mapped to required data','Source and provenance tracking','Deterministic calculations separated from judgment','Visible gaps, assumptions and review status']): c.setFont('Helvetica',9); c.drawString(78,170-j*22,'• '+t)
c.setFillColor(tint); c.roundRect(410,85,330,190,14,fill=1,stroke=0); c.setFillColor(HexColor('#8F6614')); c.setFont('Helvetica-Bold',9); c.drawString(430,250,'COMPILED REFERENCE LIBRARY'); c.setFillColor(ink); c.setFont('Times-Bold',15); c.drawString(430,220,'A curated library of third-party LCA studies,'); c.drawString(430,201,'methods and sector research.')
for j,t in enumerate(['Treasury / IRS / DOE guidance','General LCA methodology','CORRIM and wood-products / biomass literature','Forest carbon, feedstock and transport studies']): c.setFont('Helvetica',9); c.drawString(438,170-j*22,'• '+t)
c.showPage()

# p4
c.setFillColor(forest); c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(gold); c.setFont('Helvetica-Bold',10); c.drawString(50,H-55,'THE TEAM')
c.setFillColor(cream); c.setFont('Times-Bold',28); c.drawString(50,H-95,'Three disciplines. One integrated LCA team.')
people=[('Steven Bick, PhD','Certified Forester · forest economist · consultant',['38+ years of practice','Principal, Northeast Forests LLC','11 forestry / forest-products books']),('Alison H. Berry','Economist · forest-sector consultant',['20+ years consulting and research','Biomass markets, economics and policy','Project development and communication']),('Maura L. Ross','Energy engineer · wood-energy specialist',['Energy engineering + environmental science','20+ Forest Service grants · $2.5M+','GIS, guidance and stakeholder coordination'])]
for i,(name,role,bul) in enumerate(people):
    x=50+i*245; c.setFillColor(green2); c.roundRect(x,180,220,250,14,fill=1,stroke=0); c.setFillColor(cream); c.setFont('Times-Bold',14); c.drawString(x+16,395,name); c.setFillColor(sage); c.setFont('Helvetica-Oblique',9); draw_lines(role,x+16,375,185,size=9,color=sage,leading=12)
    c.setFillColor(cream); c.setFont('Helvetica',9)
    yy=320
    for b in bul: draw_lines('• '+b,x+16,yy,185,size=9,color=cream,leading=12); yy-=48
c.setFillColor(gold); c.roundRect(50,70,710,80,12,fill=1,stroke=0); c.setFillColor(forest); c.setFont('Times-Bold',16); c.drawString(70,120,'Start with the project question — not a generic template.'); c.setFont('Helvetica',10); c.drawString(70,95,'bbr.northeastforests.com · steve@northeastforests.com')
c.save()
