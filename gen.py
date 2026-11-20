#!/usr/bin/env python3
import os, sys
if sys.executable != "/usr/bin/python3" and os.path.exists("/usr/bin/python3"):
    os.execv("/usr/bin/python3", ["/usr/bin/python3", os.path.abspath(__file__), *sys.argv[1:]])
sys.path.insert(0, "/usr/lib/python3/dist-packages")
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28
BG, INK, BODY, RED = "#0d0f12", "#f2f3f5", "#b9bec7", "#c8102e"
RULE, PANEL = "#454a53", "#171a20"
REGIONS = [("EUROPE",5,"#31556b"),("MIDDLE EAST",5,"#7d493d"),("ASIA",12,"#9b3d4c"),
           ("AMERICAS",11,"#35645a"),("AFRICA",3,"#775e32"),("OCEANIA",5,"#4e527b"),("GLOBAL",4,"#595f68")]
assert sum(x[1] for x in REGIONS) == 45
LEAD_SIZE, RAIL_SIZE = 34, 17
assert LEAD_SIZE / RAIL_SIZE >= 1.8

img = Image.new("RGB", (W,H), BG)
d = ImageDraw.Draw(img)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT, size)
def tw(text, f):
    b=d.textbbox((0,0),text,font=f); return b[2]-b[0]
def text(x,y,s,size,color=INK,bold=False,maxw=None,anchor=None):
    assert not s.endswith("…") and not s.endswith("...")
    f=font(size,bold)
    if maxw is not None: assert tw(s,f) <= maxw, (s,tw(s,f),maxw)
    if anchor == "ra":
        assert x-tw(s,f) >= M
        d.text((x,y),s,font=f,fill=color,anchor="ra")
    else:
        assert x+tw(s,f) <= W-M, (s,x+tw(s,f))
        d.text((x,y),s,font=f,fill=color)
    return f
def rule(y,x1=M,x2=W-M): d.line((x1,y,x2,y),fill=RULE,width=1)
def poly(points, fill): d.polygon(points,fill=fill)

# Kicker and masthead
text(M,27,"THE WORLD'S NEWS IN ONE PICTURE",9,BODY,True,430)
text(W-M,27,"45 STORIES · 7 REGIONS · 13 ILLUSTRATED",9,BODY,True,anchor="ra")
rule(43)
text(M,51,"FRIDAY 20 NOVEMBER 2026",44,INK,True,900)
rule(104)

# Region strip
x=M; gap=3; stripw=W-2*M-gap*6; weights=[112,138,106,139,101,119,135]; scale=stripw/sum(weights)
for (name,count,c),raw in zip(REGIONS,weights):
    ww=round(raw*scale); d.rectangle((x,111,x+ww,136),fill=c)
    text(x+7,117,f"{name}  {count}",9,"#ffffff",True,ww-14); x += ww+gap

# Figures ticker
figs=[("+1.7°C","GLOBAL ANOMALY"),("112","SUMMIT DELEGATES"),("$84.20","BRENT / BARREL"),("46.8M","DISPLACED PEOPLE")]
x=M
for val,lab in figs:
    text(x,144,val,9,INK,True,70); text(x+58,144,lab,9,BODY,True,155); x+=242
rule(160)

# Lead band
lead_x, lead_y, lead_w = M,168,632
text(lead_x,166,"SHENZHEN SUMMIT FACES",34,INK,True,lead_w)
text(lead_x,204,"ITS FIRST TEST",34,INK,True,lead_w)
# 300x120 illustration: summit table, skyline, delegates
ix,iy=lead_x,246
d.rectangle((ix,iy,ix+300,iy+120),fill="#18252d")
d.rectangle((ix,iy+83,ix+300,iy+120),fill="#22272e")
for bx,bw,bh in [(12,29,52),(48,22,72),(78,40,45),(126,27,67),(161,48,56),(216,25,76),(249,38,48)]:
    d.rectangle((ix+bx,iy+83-bh,ix+bx+bw,iy+83),fill="#314452")
    for wx in range(ix+bx+5,ix+bx+bw-2,9): d.rectangle((wx,iy+73-bh,wx+2,iy+78-bh),fill="#75909d")
poly([(ix+42,iy+93),(ix+150,iy+68),(ix+258,iy+93),(ix+150,iy+114)],"#8b2638")
for cx in [76,105,134,166,195,224]:
    d.ellipse((ix+cx-5,iy+70,ix+cx+5,iy+80),fill="#d4b39a")
    d.rectangle((ix+cx-7,iy+80,ix+cx+7,iy+93),fill="#222831")
d.rectangle((ix,iy+103,ix+300,iy+120),fill=RED)
text(ix+7,iy+106,"SHENZHEN  ·  TRADE, CLIMATE AND SEA SECURITY",9,"#ffffff",True,286)
text(ix+314,248,"Leaders bring a carbon-market pledge, but a maritime",11,BODY,False,318)
text(ix+314,265,"standoff turns the staged gathering into a live test.",11,BODY,False,318)
text(ix+314,285,"Illustration: World Desk / figures as of 18:00 CST",9,"#7f8792",False,318)

# two rail stories
rx=684
d.rectangle((rx,168,W-M,257),fill=PANEL)
text(rx+10,177,"EUROPE'S WINTER",17,INK,True,302)
text(rx+10,198,"POWER PACT HOLDS",17,INK,True,302)
text(rx+10,225,"Grid sharing averts the first cold snap test.",9,BODY,False,302)
d.rectangle((rx,266,W-M,366),fill="#141b1d")
text(rx+10,275,"AMAZON STATES SET",17,INK,True,302)
text(rx+10,296,"A FOREST FLOOR",17,INK,True,302)
text(rx+10,323,"Nine governors agree a common carbon price.",9,BODY,False,302)
text(rx+10,344,"MANAUS · AMERICAS",8.5,"#58a48e",True,302)
rule(375)

# Ten illustrated cards
cards=[
 ("MIDEAST","GAZA TALKS ENTER","A SECOND WEEK","#b96b56",0),
 ("ASIA","TOKYO WAGES OUTRUN","PRICES AT LAST","#d55b70",1),
 ("AMERICAS","ANDES RAIL LINK","CLEARS LAST PASS","#58a48e",2),
 ("AFRICA","SAHEL SOLAR GRID","POWERS SIX CITIES","#c09a50",3),
 ("OCEANIA","REEF TREATY ADDS","A NO-TAKE ZONE","#858bd1",4),
 ("EUROPE","DANUBE FLOOD WALL","MEETS HIGH WATER","#65a5c9",5),
 ("ASIA","INDIA'S MOON RELAY","SENDS FIRST MAP","#d55b70",6),
 ("GLOBAL","VACCINE FUND WINS","FIVE-YEAR RENEWAL","#959da8",7),
 ("AMERICAS","CARIBBEAN CABLE","RETURNS ONLINE","#58a48e",8),
 ("OCEANIA","AUCKLAND VOTES","FOR DENSER HOMES","#858bd1",9)]
cw, cg = 184, 12
def vignette(x,y,k,c):
    d.rectangle((x,y,x+92,y+46),fill="#202830")
    if k%3==0:
        d.ellipse((x+10,y+8,x+42,y+40),fill=c); d.rectangle((x+50,y+13,x+82,y+36),fill="#59616b")
    elif k%3==1:
        poly([(x+4,y+39),(x+28,y+12),(x+49,y+32),(x+67,y+7),(x+90,y+39)],c)
        d.line((x+4,y+39,x+90,y+39),fill="#abb2bb",width=2)
    else:
        d.rectangle((x+9,y+11,x+83,y+38),fill=c); d.line((x+15,y+33,x+76,y+16),fill=INK,width=3)
for i,(slug,a,b,c,k) in enumerate(cards):
    row,col=divmod(i,5); x=M+col*(cw+cg); y=385+row*104
    vignette(x,y,k,c); text(x+99,y+1,slug,8.5,c,True,85)
    text(x,y+51,a,12,INK,True,cw); text(x,y+66,b,12,INK,True,cw)
rule(589)

# Footer feature: schematic map and date check
text(M,596,"THE DAY, MAPPED",9,INK,True,180)
mx,my=M,612
d.rectangle((mx,my,mx+240,my+150),fill="#11161b",outline=RULE)
land="#44545b"
poly([(mx+12,my+44),(mx+32,my+21),(mx+66,my+19),(mx+86,my+37),(mx+71,my+52),(mx+47,my+56),(mx+37,my+76),(mx+18,my+68)],land)
poly([(mx+72,my+76),(mx+93,my+86),(mx+98,my+116),(mx+86,my+139),(mx+76,my+105)],land)
poly([(mx+111,my+30),(mx+143,my+18),(mx+181,my+25),(mx+219,my+47),(mx+202,my+64),(mx+168,my+58),(mx+150,my+78),(mx+128,my+68)],land)
poly([(mx+130,my+72),(mx+159,my+74),(mx+169,my+112),(mx+151,my+137),(mx+134,my+105)],land)
poly([(mx+197,my+106),(mx+222,my+111),(mx+230,my+130),(mx+204,my+134)],land)
dots=[(207,51),(147,41),(131,54),(77,42),(55,52),(87,99),(149,91),(218,121),(173,46),(119,42),(37,40),(102,61)]
for n,(dx,dy) in enumerate(dots,1):
    d.ellipse((mx+dx-5,my+dy-5,mx+dx+5,my+dy+5),fill=RED)
    text(mx+dx,my+dy-5,str(n),8.5,"#ffffff",True,12,anchor="ra")
text(mx+250,my,"1–12  Illustrated stories above",9,BODY,True,230)
text(mx+250,my+18,"Dots locate the day's visual reports.",9,BODY,False,230)
d.rectangle((524,my,996,my+74),outline=RED,width=1)
text(536,my+8,"DATE CHECK",9,RED,True,130)
text(536,my+26,"Omitted: the 19 Nov Mars launch, the 21 Nov G20 ministerial,",9,BODY,False,445)
text(536,my+42,"and weekend election previews. This edition covers Friday only.",9,BODY,False,445)
text(536,my+87,"45 reports · numbered once · regional totals audited",9,INK,True,440)

# Briefs 14–45, 32 items in three columns
briefs=[
 ("BRUSSELS","AI audit rules clear parliament."),("WARSAW","Baltic patrols gain two ships."),("MADRID","Drought curbs ease after rain."),
 ("BEIRUT","Port insurers restore cover."),("AMMAN","Water accord opens a pipeline."),("DOHA","Mediators extend the truce draft."),
 ("SEOUL","Chip exports reach a yearly high."),("HANOI","Metro line opens ahead of plan."),("JAKARTA","Peatland fires fall by a third."),
 ("DHAKA","Garment wage panel sets a floor."),("KATHMANDU","Glacier sensors issue first alert."),("MANILA","Storm shelters pass a night drill."),
 ("BEIJING","Consumer spending edges higher."),("SINGAPORE","Port queues return to normal."),("NEW YORK","Markets digest a steady Fed."),
 ("OTTAWA","Arctic broadband reaches Nunavut."),("MEXICO CITY","Clean-bus tender draws six bids."),("SANTIAGO","Copper talks avert a strike."),
 ("LIMA","Anchovy quota rises cautiously."),("BRASÍLIA","Indigenous fund gains oversight."),("HAVANA","Solar imports clear the harbour."),
 ("NAIROBI","Regional rail freight restarts."),("ACCRA","Cocoa traceability goes live."),("CAPE TOWN","Reservoirs hold above target."),
 ("SYDNEY","Heat code protects outdoor crews."),("WELLINGTON","Farm methane vote advances."),("SUVA","Cyclone pool pays its first claim."),
 ("PORT MORESBY","Clinic drones double their range."),("APIA","Pacific archive opens online."),("GENEVA","Refugee appeal reaches two thirds."),
 ("OSLO","Ocean panel adopts noise limits."),("PARIS","Food index falls for a third month.")]
assert len(briefs)==32
text(M,772,"BRIEFS 14–45",9,RED,True,160); rule(787)
colw=312; starts=[M,356,684]
for sx in [344,672]: d.line((sx,795,sx,984),fill=RULE,width=1)
for i,(place,clause) in enumerate(briefs):
    col=i//11; row=i%11; x=starts[col]; y=794+row*17
    f=font(9,True); p=place+"  "; text(x,y,p,9,INK,True,colw)
    text(x+tw(p,f),y,clause,9,BODY,False,colw-tw(p,f))

rule(986)
text(M,993,"SOURCES  ·  WORLD DESK WIRES, PUBLIC AGENCIES, MARKET CLOSES  ·  ART AND EDITING: WORLD PICTURE DESK",8.5,"#7f8792",False,850)
text(W-M,993,"20 NOV 2026",8.5,"#7f8792",True,anchor="ra")

assert img.size == (1024,1024)
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),"entry.png")
img.save(out,"PNG",optimize=True,compress_level=9)
assert os.path.getsize(out) < 1024*1024
print(f"stories=45 lead_ratio={LEAD_SIZE/RAIL_SIZE:.2f} png_bytes={os.path.getsize(out)}")
