import sys, os
from PIL import Image, ImageDraw
res = sys.argv[1]
PINE=(31,74,61,255); YEL=(242,183,5,255); YEL2=(196,146,0,255); BLK=(24,28,26,255); RED=(214,60,44,255); WHITE=(255,255,255,255)

def pack(S, scale=1.0, badge=True, bg=None, shape='square'):
    im = Image.new('RGBA', (S, S), (0,0,0,0)); d = ImageDraw.Draw(im)
    if bg:
        if shape == 'round': d.ellipse([0,0,S-1,S-1], fill=bg)
        else: d.rounded_rectangle([0,0,S-1,S-1], radius=int(S*.22), fill=bg)
    u = lambda v: S*(0.5+(v-0.5)*scale)
    w = max(2, int(S*.035*scale))
    d.rounded_rectangle([u(.41),u(.17),u(.59),u(.36)], radius=u(.1)-u(0), outline=YEL, width=w)
    d.rounded_rectangle([u(.20),u(.56),u(.30),u(.78)], radius=S*.02*scale, fill=YEL2)
    d.rounded_rectangle([u(.70),u(.56),u(.80),u(.78)], radius=S*.02*scale, fill=YEL2)
    d.rounded_rectangle([u(.26),u(.27),u(.74),u(.84)], radius=S*.11*scale, fill=YEL)
    d.line([u(.30),u(.45),u(.70),u(.45)], fill=BLK, width=w)
    d.rounded_rectangle([u(.33),u(.54),u(.67),u(.78)], radius=S*.05*scale, fill=BLK)
    if badge:
        cx, cy, r = u(.75), u(.26), S*.13*scale
        d.ellipse([cx-r-w*.6, cy-r-w*.6, cx+r+w*.6, cy+r+w*.6], fill=PINE if bg else (31,74,61,255))
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=RED)
        bw = r*.22
        d.rounded_rectangle([cx-bw, cy-r*.55, cx+bw, cy+r*.15], radius=bw, fill=WHITE)
        d.ellipse([cx-bw*1.1, cy+r*.38, cx+bw*1.1, cy+r*.38+bw*2.2], fill=WHITE)
    return im

M = 1024
full = pack(M, .92, True, PINE, 'square')
rnd = pack(M, .86, True, PINE, 'round')
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
open(os.path.join(v,'ic_launcher_background.xml'),'w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#1F4A3D</color>\n</resources>\n')
if len(sys.argv) > 2: full.resize((512,512)).save(sys.argv[2])
