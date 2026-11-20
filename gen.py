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
# 300x120 illustration: hazy, rain-wet Shenzhen skyline
ix,iy=lead_x,246
d.rectangle((ix,iy,ix+300,iy+120),fill="#8c9ba2")
d.ellipse((ix+231,iy+10,ix+259,iy+38),fill="#d8b98b")
# two soft cloud bands, assembled from opaque overlapping ellipses
for cx,cy,c in [(25,20,"#aab5b9"),(57,18,"#aab5b9"),(86,22,"#aab5b9"),
                (151,33,"#788b94"),(187,30,"#788b94"),(219,34,"#788b94")]:
    d.ellipse((ix+cx-24,iy+cy-5,ix+cx+28,iy+cy+7),fill=c)
# atmospheric separation, eight explicitly interpolated opaque bands
atmos=["#738892","#6d828d","#677d88","#617782","#5b717d","#556b77","#4f6572","#495f6d"]
for n,c in enumerate(atmos): d.rectangle((ix,iy+43+n*2,ix+300,iy+44+n*2),fill=c)
# varied middle skyline and individually lit 2x3 window grids
buildings=[(7,23,35),(34,28,48),(67,20,61),(91,35,42),(130,23,55),(157,34,46),(195,20,65),(219,31,51),(254,38,39)]
for bi,(bx,bw,bh) in enumerate(buildings):
    top=94-bh; d.rectangle((ix+bx,iy+top,ix+bx+bw,iy+94),fill="#2d414c")
    for wy in range(top+7,91,7):
        for wx in range(bx+5,bx+bw-3,7):
            lit=((wx//7)+(wy//7)+bi)%4 != 0
            d.rectangle((ix+wx,iy+wy,ix+wx+2,iy+wy+3),fill="#d7b875" if lit else "#263740")
# wet foreground and broken vertical reflection streaks
d.rectangle((ix,iy+94,ix+300,iy+120),fill="#1a252c")
for rx,rh in [(42,19),(49,12),(76,22),(83,15),(139,18),(146,10),(203,24),(210,16),(268,14)]:
    d.rectangle((ix+rx,iy+97,ix+rx+2,iy+97+rh),fill="#8d7658")
    d.rectangle((ix+rx+1,iy+101,ix+rx+3,iy+104),fill="#c5a76d")
# two darker near structures
d.rectangle((ix+4,iy+70,ix+35,iy+103),fill="#15242c")
poly([(ix+264,iy+103),(ix+264,iy+60),(ix+291,iy+49),(ix+296,iy+103)],"#12212a")
for wy in (68,77,86): d.rectangle((ix+271,iy+wy,ix+274,iy+wy+4),fill="#708994")
# subtle 12-step edge vignette, no alpha
vcols=["#26343b","#29383f","#2c3b42","#2f3e45","#324148","#35444b"]
for n in range(12):
    c=vcols[min(n//2,5)]
    d.line((ix+n,iy+n,ix+299-n,iy+n),fill=c)
    d.line((ix+n,iy+n,ix+n,iy+119-n),fill=c)
    d.line((ix+299-n,iy+n,ix+299-n,iy+119-n),fill=c)
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
    dark,mid,hi="#202830","#59616b","#d7dce1"
    d.rectangle((x,y,x+92,y+46),fill=dark)
    if k==0: # court gavel on a bench
        d.rectangle((x+8,y+35,x+84,y+41),fill=mid); d.rectangle((x+46,y+10,x+52,y+34),fill=c)
        poly([(x+34,y+9),(x+57,y+18),(x+53,y+27),(x+30,y+18)],c); d.line((x+35,y+11,x+54,y+18),fill=hi,width=2)
    elif k==1: # vial and chart
        d.rectangle((x+10,y+14,x+29,y+39),fill=c); d.rectangle((x+14,y+8,x+25,y+14),fill=mid)
        d.line((x+39,y+37,x+83,y+37),fill=mid,width=2); d.line((x+42,y+32,x+54,y+24,x+65,y+29,x+81,y+10),fill=c,width=3); d.ellipse((x+77,y+7,x+83,y+13),fill=hi)
    elif k==2: # wind turbine and wave
        d.line((x+31,y+15,x+31,y+40),fill=hi,width=2); d.ellipse((x+28,y+12,x+34,y+18),fill=c)
        for ex,ey in [(15,6),(45,7),(29,27)]: d.line((x+31,y+15,x+ex,y+ey),fill=c,width=3)
        d.arc((x+44,y+22,x+91,y+48),190,345,fill=c,width=4); d.arc((x+55,y+28,x+88,y+45),190,340,fill=hi,width=2)
    elif k==3: # ballot box with a queue
        d.rectangle((x+42,y+19,x+82,y+40),fill=c); d.line((x+49,y+23,x+73,y+23),fill=hi,width=2); poly([(x+55,y+7),(x+72,y+12),(x+67,y+25),(x+50,y+19)],hi)
        for px in (9,23,35): d.ellipse((x+px,y+16,x+px+7,y+23),fill=mid); d.line((x+px+3,y+23,x+px+3,y+38),fill=mid,width=3)
    elif k==4: # train entering a tunnel
        d.arc((x+4,y+6,x+60,y+55),180,360,fill=c,width=6); d.rectangle((x+25,y+20,x+56,y+41),fill=mid)
        d.rectangle((x+30,y+24,x+39,y+31),fill=hi); d.ellipse((x+29,y+37,x+35,y+43),fill=c); d.line((x+57,y+38,x+88,y+38),fill=hi,width=2)
    elif k==5: # satellite over a curve
        d.arc((x+2,y+22,x+90,y+70),180,360,fill=c,width=4); d.rectangle((x+39,y+13,x+53,y+27),fill=hi)
        poly([(x+36,y+15),(x+18,y+8),(x+15,y+18),(x+36,y+23)],mid); poly([(x+56,y+15),(x+75,y+8),(x+78,y+18),(x+56,y+23)],mid); d.line((x+46,y+13,x+51,y+5),fill=c,width=2)
    elif k==6: # flood wall with water
        d.rectangle((x+49,y+8,x+72,y+40),fill=mid); poly([(x+49,y+8),(x+77,y+8),(x+72,y+14),(x+49,y+14)],hi)
        for yy in (27,35,42): d.arc((x-8,y+yy-7,x+54,y+yy+8),190,345,fill=c,width=3)
    elif k==7: # container ship
        poly([(x+7,y+34),(x+82,y+34),(x+72,y+42),(x+18,y+42)],mid)
        for bx,by,bc in [(20,20,c),(36,20,hi),(52,20,c),(28,11,mid),(44,11,c)]: d.rectangle((x+bx,y+by,x+bx+14,y+by+8),fill=bc)
        d.line((x+8,y+44,x+87,y+44),fill=c,width=2)
    elif k==8: # power pylon and line
        poly([(x+43,y+5),(x+30,y+41),(x+56,y+41)],mid); d.line((x+35,y+25,x+52,y+25),fill=hi,width=2); d.line((x+32,y+15,x+55,y+15),fill=hi,width=2)
        d.line((x+4,y+13,x+32,y+15),fill=c,width=2); d.line((x+55,y+15,x+88,y+9),fill=c,width=2)
    else: # leaf over a chart
        d.line((x+8,y+39,x+85,y+39),fill=mid,width=2); d.line((x+15,y+34,x+31,y+28,x+48,y+31,x+73,y+12),fill=c,width=3)
        d.ellipse((x+44,y+7,x+73,y+26),fill=c); poly([(x+44,y+25),(x+50,y+8),(x+73,y+7),(x+66,y+22)],c); d.line((x+48,y+24,x+68,y+10),fill=hi,width=2)
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
