#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: a one-page newspaper front page
summing up Saturday 21 November 2026. Pure Pillow; run once, writes
entry.png (1024x1024).

Stories (all reported 21 Nov 2026, verified against Reuters/AP/Le Monde/
BBC/NYT/ISW reporting and the OneTurn daily brief):
 1. Kyiv/Poland: Russia fired 400+ drones and 110+ missiles at Ukraine
    overnight (27 ballistic), killing eight and hitting three bridges
    across the Dnipro in Kyiv; two Russian Kh-101 cruise missiles and a
    jet-powered drone then came down in Poland. Warsaw calls it a
    deliberate provocation; NATO calls it a grave violation; Poland
    invoked NATO Article 4 and asked for AWACS and F-35s.
 2. Wall Street: the S&P 500 fell 3.7% to 6,910 on Friday, more than 10%
    below its peak -- a correction; the Nasdaq slid 5.3% to 22,617 and
    wiped out its gains for the year. Nvidia fell 14% in a day; Anthropic
    slipped 9% after its record IPO.
 3. Medicine: the pill daraxonrasib made pancreatic cancer undetectable
    on scans in one in 12 patients in a trial.
 4. Brussels: the UK and EU signed three agreements (food exports,
    carbon markets, youth mobility), their biggest step since Brexit;
    Gen Z protests spread across 25 European countries.
 5. Antalya: COP31 ran past its deadline as nearly 200 nations failed
    to agree on phasing out fossil fuels.
Ticker: Myanmar calls the ICJ's Rohingya genocide ruling 'unfair';
FBI and USDA hit by cyberattacks amid US outages; Trump weighs new
strikes on Iran as Israel presses; Bayer pays $7.25bn to settle
Roundup claims; magnitude 6.9 quake shakes the Peruvian Andes; gas
blast in Tbilisi kills six; South Korea court overturns ex-PM Han
Duck-soo's sentence; Bukele registers for a third term; US court lets
the Trump administration end protected status for 600,000
Venezuelans; man convicted of starting LA's deadly Palisades fire.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 228)
PANEL = (253, 251, 244)
INK = (26, 23, 18)
RED = (179, 39, 30)
NAVY = (29, 62, 110)
TEAL = (14, 74, 90)
GOLD = (176, 132, 38)
SKY = (198, 219, 228)
GREY = (96, 91, 80)
RULE = (196, 188, 164)
GREEN = (32, 110, 62)
NIGHT = (18, 28, 52)
RIVER = (90, 140, 165)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, fill=INK, leading=None):
    lh = leading or int(font.size * 1.32)
    for ln in wrap_text(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def headline(d, x, y, text, font, max_w, leading=None):
    lh = leading or int(font.size * 1.12)
    for ln in wrap_text(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=INK)
        y += lh
    return y


def kicker(d, x, y, text, color=RED):
    d.text((x, y), text, font=fnt(SANS_B, 15), fill=color)
    return y + 22


def hrule(d, y, x0=36, x1=988, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_strike(d, x, y, w, h):
    """Night sky over the Dnipro: three bridges, one broken, missile trails."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # stars
    for sx, sy in [(22, 18), (70, 34), (120, 14), (170, 30), (220, 16),
                   (270, 36), (300, 20), (48, 52), (150, 48), (250, 54)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    # missile trails: quadratic-bezier polylines, kept inside the panel
    def bez(p0, p1, p2, n=24):
        pts = []
        for i in range(n + 1):
            t = i / n
            bx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            by = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            pts.append((x + bx, y + by))
        return pts

    for (sx, sy, cx, cy, ex, ey) in [
            (12, 96, 70, 30, 150, 118),
            (90, 100, 170, 34, 250, 128),
            (200, 104, 260, 44, 310, 118)]:
        d.line(bez((sx, sy), (cx, cy), (ex, ey)), fill=(255, 120, 90),
               width=2)
        d.ellipse([x + ex - 4, y + ey - 4, x + ex + 4, y + ey + 4],
                  fill=RED)
    # river
    d.rectangle([x, y + h - 26, x + w, y + h], fill=RIVER)
    # three bridges: two hold, the middle one has dropped
    by = y + h - 78
    d.line([(x + 8, by), (x + 104, by)], fill=(230, 225, 200), width=5)
    d.line([(x + 220, by + 16), (x + w - 8, by + 16)], fill=(230, 225, 200),
           width=5)
    d.line([(x + 104, by), (x + 118, by + 12)], fill=(230, 225, 200), width=4)
    d.line([(x + 220, by + 16), (x + 206, by + 4)], fill=(230, 225, 200),
           width=4)
    for px in (x + 20, x + 90, x + 232, x + 300):
        d.line([(px, by), (px, y + h - 26)], fill=(230, 225, 200), width=3)
    # strike burst at the gap
    mx, my = x + 162, by + 8
    for ang in range(0, 360, 45):
        r = 13
        d.line([(mx, my),
                (mx + r * math.cos(math.radians(ang)),
                 my + r * math.sin(math.radians(ang)))], fill=RED, width=2)
    d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=RED)


def draw_chart_down(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=RULE, width=1)
    d.line([(x + 8, y + h - 26), (x + w - 8, y + h - 26)], fill=GREY, width=1)
    # one declining line (S&P); both numbers as text, clear of the line
    pts = [(x + 14, y + 24), (x + 60, y + 28), (x + 110, y + 26),
           (x + 160, y + 34), (x + 210, y + 36), (x + w - 14, y + h - 16)]
    d.line(pts, fill=RED, width=3)
    d.text((x + 10, y + 4), "S&P 500  \u22123.7%", font=fnt(SANS_B, 14), fill=RED)
    d.text((x + 10, y + h - 22), "Nasdaq  \u22125.3%",
           font=fnt(SANS_B, 14), fill=(120, 20, 20))


def draw_pill(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=RULE, width=1)
    # capsule: teal half + white half
    cx, cy, L, R = x + 30, y + h // 2, 150, 24
    d.rounded_rectangle([cx, cy - R, cx + L // 2, cy + R], radius=R,
                        fill=TEAL)
    d.rounded_rectangle([cx + L // 2, cy - R, cx + L, cy + R], radius=R,
                        fill=(255, 255, 255), outline=TEAL, width=2)
    d.line([(cx + L // 2, cy - R), (cx + L // 2, cy + R)], fill=TEAL, width=2)
    d.text((cx + L + 18, cy - 26), "1 in 12", font=fnt(SANS_B, 26), fill=TEAL)
    d.text((cx + L + 18, cy + 4), "saw tumours vanish",
           font=fnt(SANS, 14), fill=GREY)


def draw_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy, r = x + w / 2, y + h / 2, 42
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        # five-pointed star polygon (outer 8, inner 3.5)
        star = []
        for k in range(10):
            rr = 8 if k % 2 == 0 else 3.5
            a = math.radians(-90 + k * 36)
            star.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
        d.polygon(star, fill=(255, 209, 0))


def draw_thermo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=RULE, width=1)
    # thermometer: bulb + column, mercury near the top
    d.ellipse([x + w / 2 - 16, y + h - 34, x + w / 2 + 16, y + h - 2],
              fill=RED)
    d.rectangle([x + w / 2 - 8, y + 12, x + w / 2 + 8, y + h - 18], fill=RED)
    d.rectangle([x + w / 2 - 8, y + 12, x + w / 2 + 8, y + h - 18],
                outline=INK, width=2)
    d.ellipse([x + w / 2 - 16, y + h - 34, x + w / 2 + 16, y + h - 2],
              outline=INK, width=2)
    # tick marks
    for i in range(4):
        ty = y + 20 + i * 24
        d.line([(x + w / 2 + 10, ty), (x + w / 2 + 20, ty)], fill=INK, width=2)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, 10], fill=RED)

# ---- masthead ------------------------------------------------------------
d.text((W / 2, 22), "THE WORLD", font=fnt(SERIF_B, 88), fill=INK, anchor="mt")
d.text((W / 2, 116), "IN ONE PAGE", font=fnt(SANS_B, 17), fill=RED, anchor="mt")
hrule(d, 144)
d.text((36, 154), "SATURDAY, 21 NOVEMBER 2026", font=fnt(SANS_B, 20), fill=INK)
d.text((988, 154), "ONE DAY'S NEWS", font=fnt(SANS_B, 16), fill=GREY, anchor="rt")
hrule(d, 182, width=3)

# ---- lead: Russia strikes Ukraine, missiles land in Poland ---------------
y = 194
y = kicker(d, 36, y, "KYIV  \u00b7  WAR IN EUROPE")
y = headline(d, 36, y, "Russian missiles land in Poland as Kyiv\u2019s bridges burn",
             fnt(SERIF_B, 38), 600)
y = para(d, 36, y + 6,
         "Russia fired more than 400 drones and 110 missiles at Ukraine "
         "overnight \u2014 27 of them ballistic \u2014 killing eight "
         "people and hitting three bridges across the Dnipro in Kyiv. "
         "Two Russian cruise missiles and a jet-powered drone then came "
         "down in Poland.",
         fnt(SANS, 16), 600)
para(d, 36, y + 4,
     "Warsaw calls it a deliberate provocation; NATO calls it a grave "
     "violation. Poland has invoked the alliance\u2019s Article 4.",
     fnt(SERIF_I, 17), 600)
draw_strike(d, 664, 194, 324, 218)
d.text((664, 418), "Missiles and a drone came down in Poland; Kyiv\u2019s bridges hit.",
       font=fnt(SANS, 13), fill=GREY)

hrule(d, 452)

# ---- row 2: markets | cancer pill ----------------------------------------
y = 466
y1 = kicker(d, 36, y, "NEW YORK  \u00b7  MARKETS")
y1 = headline(d, 36, y1, "AI rout drags the S&P 500 into correction",
              fnt(SERIF_B, 25), 452)
y1 = para(d, 36, y1 + 4,
          "US stocks fell sharply on Friday as the AI sell-off spread: "
          "the S&P 500 dropped 3.7% to 6,910, more than 10% below its "
          "peak, and the Nasdaq slid 5.3%, wiping out its gains for the "
          "year. Nvidia fell 14% in a day.",
          fnt(SANS, 15), 452)
draw_chart_down(d, 36, 616, 452, 66)

y2 = kicker(d, 528, y, "HEALTH  \u00b7  CANCER TRIAL")
y2 = headline(d, 528, y2, "Cancer pill makes tumours vanish in one in 12",
              fnt(SERIF_B, 25), 460)
y2 = para(d, 528, y2 + 4,
          "A trial of the pill daraxonrasib made pancreatic cancer "
          "undetectable on scans in one in 12 patients \u2014 a rare "
          "advance against one of the hardest cancers to treat.",
          fnt(SANS, 15), 460)
draw_pill(d, 528, 616, 460, 66)

hrule(d, 700)
d.line([(512, 466), (512, 692)], fill=RULE, width=1)

# ---- row 3: Brussels | COP31 ---------------------------------------------
y = 714
y1 = kicker(d, 36, y, "BRUSSELS  \u00b7  EUROPE")
y1 = headline(d, 36, y1, "UK and EU sign biggest post-Brexit deals",
              fnt(SERIF_B, 24), 330)
y1 = para(d, 36, y1 + 4,
          "Britain and the EU signed three agreements in Brussels \u2014 "
          "on food exports, carbon markets and youth mobility \u2014 "
          "their biggest step since Brexit.",
          fnt(SANS, 15), 330)
para(d, 36, y1 + 4,
     "Gen Z protests spread across 25 European countries.",
     fnt(SANS, 15), 330)
draw_eu(d, 396, 730, 96, 140)

y2 = kicker(d, 528, y, "ANTALYA  \u00b7  CLIMATE")
y2 = headline(d, 528, y2, "COP31 runs past deadline over fossil fuels",
              fnt(SERIF_B, 24), 330)
y2 = para(d, 528, y2 + 4,
          "The UN climate summit in Antalya ran into overtime as nearly "
          "200 nations failed to agree on phasing out fossil fuels.",
          fnt(SANS, 15), 330)
para(d, 528, y2 + 4,
     "Iran says it downed a US MQ-9 drone over the Strait of Hormuz.",
     fnt(SANS, 15), 330)
draw_thermo(d, 888, 730, 100, 140)

hrule(d, 892)
d.line([(512, 714), (512, 884)], fill=RULE, width=1)

# ---- ticker ---------------------------------------------------------------
d.text((36, 904), "ALSO TODAY \u2014", font=fnt(SANS_B, 15), fill=RED)
para(d, 36, 926,
     "Myanmar calls the court\u2019s Rohingya genocide ruling \u2018unfair\u2019  "
     "\u2022  FBI and USDA hit by cyberattacks amid US outages  \u2022  "
     "Trump weighs new strikes on Iran as Israel presses  \u2022  Bayer "
     "pays $7.25bn to settle Roundup claims  \u2022  Magnitude 6.9 quake "
     "shakes the Peruvian Andes  \u2022  Gas blast in Tbilisi kills six, "
     "including a child  \u2022  South Korea court overturns ex-PM Han "
     "Duck-soo\u2019s sentence  \u2022  Bukele registers for a third term "
     "in El Salvador  \u2022  US court lets the Trump administration end "
     "protected status for 600,000 Venezuelans  \u2022  Man convicted of "
     "starting LA\u2019s deadly Palisades fire.",
     fnt(SANS, 14), 952, fill=INK, leading=19)

hrule(d, 994, width=1, fill=RULE)
d.text((W / 2, 1002), "Sources: Reuters \u00b7 AP \u00b7 Le Monde \u00b7 BBC \u00b7 NYT \u2014 Saturday 21 November 2026",
       font=fnt(SANS, 12), fill=GREY, anchor="mt")

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
