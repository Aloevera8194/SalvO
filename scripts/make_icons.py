import sys, os
from PIL import Image, ImageDraw
res = sys.argv[1]
PINE=(31,74,61,255); YEL=(242,183,5,255); BLK=(24,28,26,255); DK2=(52,57,54,255); DK3=(40,44,42,255); RED=(214,60,44,255); WHITE=(255,255,255,255)

def pack(S, scale=1.0, badge=True, bg=None, shape='square'):
    im = Image.new('RGBA', (S, S), (0,0,0,0)); d = ImageDraw.Draw(im)
    if bg:
        if shape == 'round': d.ellipse([0,0,S-1,S-1], fill=bg)
        else: d.rounded_rectangle([0,0,S-1,S-1], radius=int(S*.22), fill=bg)
    u = lambda v: S*(0.5+(v-0.5)*scale)
    w = max(2, int(S*.04*scale))
    r = lambda x0,y0,x1,y1,rad,fill: d.rounded_rectangle([u(x0),u(y0),u(x1),u(y1)], radius=S*rad*scale, fill=fill)
    d.rounded_rectangle([u(.41),u(.17),u(.59),u(.36)], radius=S*.09*scale, outline=BLK, width=w)
    r(.19,.56,.30,.78,.02,DK2); r(.70,.56,.81,.78,.02,DK2)
    r(.26,.27,.74,.84,.11,BLK)
    r(.31,.32,.69,.48,.04,DK3)
    r(.33,.545,.67,.595,.012,YEL)
    r(.33,.625,.67,.64,.007,YEL)
    r(.31,.765,.69,.78,.007,YEL)
    if badge:
        cx, cy, rr = u(.75), u(.26), S*.13*scale
        d.ellipse([cx-rr-w*.6, cy-rr-w*.6, cx+rr+w*.6, cy+rr+w*.6], fill=YEL)
        d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=RED)
        bw = rr*.22
        d.rounded_rectangle([cx-bw, cy-rr*.55, cx+bw, cy+rr*.15], radius=bw, fill=WHITE)
        d.ellipse([cx-bw*1.1, cy+rr*.38, cx+bw*1.1, cy+rr*.38+bw*2.2], fill=WHITE)
    return im

M = 1024
full = pack(M, .92, True, YEL, 'square')
rnd = pack(M, .86, True, YEL, 'round')
fg = pack(M, .70, True, None)
for dens, leg, ad in [('mdpi',48,108),('hdpi',72,162),('xhdpi',96,216),('xxhdpi',144,324),('xxxhdpi',192,432)]:
    p = os.path.join(res, 'mipmap-'+dens); os.makedirs(p, exist_ok=True)
    full.resize((leg,leg), Image.LANCZOS).save(os.path.join(p,'ic_launcher.png'))
    rnd.resize((leg,leg), Image.LANCZOS).save(os.path.join(p,'ic_launcher_round.png'))
    fg.resize((ad,ad), Image.LANCZOS).save(os.path.join(p,'ic_launcher_foreground.png'))

# icone da notificacao (silhueta branca)
S=192; m = Image.new('L',(S,S),0); d = ImageDraw.Draw(m)
d.rounded_rectangle([S*.36,S*.08,S*.64,S*.34], radius=S*.1, outline=255, width=int(S*.07))
d.rounded_rectangle([S*.12,S*.50,S*.24,S*.82], radius=S*.03, fill=255)
d.rounded_rectangle([S*.76,S*.50,S*.88,S*.82], radius=S*.03, fill=255)
d.rounded_rectangle([S*.20,S*.24,S*.80,S*.92], radius=S*.14, fill=255)
d.rounded_rectangle([S*.30,S*.58,S*.70,S*.82], radius=S*.06, fill=0)
d.line([S*.26,S*.46,S*.74,S*.46], fill=0, width=int(S*.04))
n = Image.new('RGBA',(S,S),(255,255,255,0)); n.putalpha(m)
p = os.path.join(res,'drawable'); os.makedirs(p, exist_ok=True)
n.resize((96,96), Image.LANCZOS).save(os.path.join(p,'ic_stat_icon_config_sample.png'))

v = os.path.join(res,'values'); os.makedirs(v, exist_ok=True)
open(os.path.join(v,'ic_launcher_background.xml'),'w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#F2B705</color>\n</resources>\n')
if len(sys.argv) > 2: full.resize((512,512)).save(sys.argv[2])
