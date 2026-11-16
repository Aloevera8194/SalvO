import sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
res = sys.argv[1]
YEL=(242,183,5,255); BLK=(22,25,24,255); WHITE=(255,255,255,255)

def font(px):
    for f in ('DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','LiberationSans-Bold.ttf','Arial Bold.ttf'):
        try: return ImageFont.truetype(f, px)
        except Exception: pass
    return None

def grad(size, top, bot):
    w, h = size
    g = Image.new('RGBA', (w, h))
    px = g.load()
    for y in range(h):
        t = y/max(1,h-1)
        c = tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3))+(255,)
        for x in range(w): px[x,y] = c
    return g

def backpack(S, scale=1.0, bg=None, shape='square'):
    im = Image.new('RGBA', (S, S), (0,0,0,0)); d = ImageDraw.Draw(im)
    if bg:
        if shape == 'round': d.ellipse([0,0,S-1,S-1], fill=bg)
        else: d.rounded_rectangle([0,0,S-1,S-1], radius=int(S*.22), fill=bg)
    u = lambda v: S*(0.5+(v-0.5)*scale)
    L = lambda v: S*v*scale
    def rr(x0,y0,x1,y1,rad,top,bot,outline=None):
        box = [int(u(x0)),int(u(y0)),int(u(x1)),int(u(y1))]
        w, h = box[2]-box[0], box[3]-box[1]
        g = grad((w,h), top, bot)
        m = Image.new('L',(w,h),0)
        ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1], radius=int(L(rad)), fill=255)
        im.paste(g, (box[0],box[1]), m)
        if outline: ImageDraw.Draw(im).rounded_rectangle(box, radius=int(L(rad)), outline=outline, width=max(1,int(L(.006))))
    def stitch(x0,y0,x1,y1,col=(150,150,140,200)):
        n = 28
        for i in range(n):
            if i%2: continue
            a=i/n; b=(i+.6)/n
            d.line([u(x0+(x1-x0)*a),u(y0+(y1-y0)*a),u(x0+(x1-x0)*b),u(y0+(y1-y0)*b)], fill=col, width=max(1,int(L(.005))))
    # sombra no chao
    sh = Image.new('RGBA',(S,S),(0,0,0,0)); sd = ImageDraw.Draw(sh)
    sd.ellipse([u(.22),u(.80),u(.78),u(.92)], fill=(0,0,0,110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(S*.02)))
    d = ImageDraw.Draw(im)
    # alca de mao
    d.rounded_rectangle([u(.40),u(.15),u(.60),u(.37)], radius=L(.09), outline=(30,33,32,255), width=max(2,int(L(.045))))
    d.rounded_rectangle([u(.41),u(.16),u(.59),u(.36)], radius=L(.08), outline=(70,75,72,255), width=max(1,int(L(.008))))
    # bolsos laterais (tela)
    rr(.17,.56,.31,.80,.03,(58,62,60),(30,33,32),outline=(15,17,16,255))
    rr(.69,.56,.83,.80,.03,(58,62,60),(30,33,32),outline=(15,17,16,255))
    # corpo
    rr(.25,.26,.75,.86,.12,(52,56,54),(16,18,17),outline=(10,11,11,255))
    # brilho
    hl = Image.new('RGBA',(S,S),(0,0,0,0)); ImageDraw.Draw(hl).rounded_rectangle([u(.28),u(.28),u(.50),u(.50)], radius=L(.08), fill=(255,255,255,26))
    im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(S*.025)))
    d = ImageDraw.Draw(im)
    # costura do compartimento de cima
    stitch(.30,.305,.70,.305)
    # painel frontal superior com ziper
    rr(.30,.32,.70,.50,.045,(60,64,62),(36,39,38),outline=(12,13,13,255))
    d.line([u(.33),u(.345),u(.67),u(.345)], fill=(120,125,120,255), width=max(1,int(L(.007))))
    stitch(.33,.36,.67,.36)
    for cx in (.335,.375):
        d.rounded_rectangle([u(cx-.012),u(.335),u(cx+.012),u(.385)], radius=L(.008), fill=(205,208,205,255), outline=(110,112,110,255))
    # plaquinha metalica
    rr(.455,.405,.545,.445,.008,(215,217,215),(140,142,140),outline=(90,92,90,255))
    # painel frontal inferior
    rr(.30,.52,.70,.80,.045,(44,48,46),(24,26,25),outline=(10,11,11,255))
    # texto EMERGENCIA
    txt='EMERGÊNCIA'; tw=L(.36); px=max(8,int(L(.07)))
    f=font(px)
    if f:
        for _ in range(40):
            bb=d.textbbox((0,0),txt,font=f)
            if bb[2]-bb[0] <= tw: break
            px=int(px*.94); f=font(px)
        bb=d.textbbox((0,0),txt,font=f)
        tx=u(.5)-(bb[2]-bb[0])/2-bb[0]; ty=u(.575)-(bb[3]-bb[1])/2-bb[1]
        d.text((tx,ty),txt,font=f,fill=YEL)
        d.rounded_rectangle([u(.32),u(.575)+(bb[3]-bb[1])/2+L(.018),u(.68),u(.575)+(bb[3]-bb[1])/2+L(.03)], radius=L(.006), fill=YEL)
    else:
        d.rounded_rectangle([u(.33),u(.55),u(.67),u(.60),], radius=L(.01), fill=YEL)
    # vivo amarelo na base do painel
    d.rounded_rectangle([u(.31),u(.76),u(.69),u(.775)], radius=L(.007), fill=YEL)
    return im

M = 1024
full = backpack(M, .94, YEL, 'square')
rnd = backpack(M, .88, YEL, 'round')
fg = backpack(M, .72, None)
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
if len(sys.argv) > 2: full.resize((512,512), Image.LANCZOS).save(sys.argv[2])
if len(sys.argv) > 3: full.resize((192,192), Image.LANCZOS).save(sys.argv[3])
