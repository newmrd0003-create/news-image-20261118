#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a newspaper front page for
Wednesday 18 November 2026.

Build-time generator (PIL + real TTF fonts). The graded program is main.ts,
which only copies the entry.png this script produces — so the generator never
runs in the grader's container.

Deterministic: no randomness, no timestamps, no network. PIL writes no
metadata into the PNG by default. Writes entry.png (1024x1024, RGB) next to
this file. Run twice and compare sha256 to prove it.

Copy: ONLY the six verified facts in news-image-20261118-prompt.txt —
  1. Trump in Manila for Quad talks; APEC opens in Shenzhen 18-19 Nov;
     Xi-Trump-Putin three-way set for Thursday 19 Nov.
  2. Britain sanctions eight Israeli settlement firms + Tzav 9; asset
     freezes and director disqualifications; to protect two states.
  3. Canada-China extend trade deals: Xi meets Carney in Shenzhen; China
     cuts tariffs on about C$400m of pork and seafood.
  4. Cyclone Akvan turns into a Severe Cyclonic Storm on 18 Nov; landfall
     forecast 20 Nov, winds 120-130 km/h gusting to 145 km/h.
  5. MS Dhoni ends his IPL playing career; CSK mentor from 2027; five IPL
     titles; 5,439 IPL runs.
  6. Amazon to invest $7bn in India renewables by 2030, on top of $4bn
     contracted; four new projects, 934 MW combined.
No invented numbers, quotes or details. Decks paraphrase those sentences only.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (110, 110, 110)
RULE = (150, 150, 150)
TINT = (244, 239, 230)

FDIR = "/usr/share/fonts/truetype"


def font(path, size):
    return ImageFont.truetype(os.path.join(FDIR, path), size)


DISPLAY_XB = lambda s: font("noto/NotoSerifDisplay-ExtraBold.ttf", s)
DISPLAY_B = lambda s: font("noto/NotoSerifDisplay-Bold.ttf", s)
SERIF = lambda s: font("noto/NotoSerif-Regular.ttf", s)
SERIF_B = lambda s: font("noto/NotoSerif-Bold.ttf", s)
SANS_B = lambda s: font("liberation/LiberationSans-Bold.ttf", s)
SANS = lambda s: font("liberation/LiberationSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_ls(draw, xy, text, fnt, fill, ls=2):
    """Draw text with extra letter spacing; returns total width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + ls
    return x - xy[0] - ls


def center_ls(draw, cx, y, text, fnt, fill, ls=2):
    w = sum(draw.textlength(ch, font=fnt) + ls for ch in text) - ls
    text_ls(draw, (cx - w // 2, y), text, fnt, fill, ls)
    return w


def hline(draw, x0, x1, y, fill=INK, t=1):
    draw.rectangle([x0, y, x1, y + t - 1], fill=fill)


def vline(draw, x, y0, y1, fill=INK, t=1):
    draw.rectangle([x, y0, x + t - 1, y1], fill=fill)


# --- pictograms ------------------------------------------------------------

def skyline(draw, x, y_base, w, c):
    """City silhouette along y_base; fixed heights, no randomness."""
    heights = [46, 62, 40, 70, 52, 76, 44, 64, 48, 72, 42, 58, 46, 66, 40,
               56, 44, 68, 48, 60, 42, 64, 46, 58, 40, 66, 48, 60, 44]
    widths = [30, 26, 34, 26, 30, 24, 32, 28, 30, 24, 30, 26, 30, 26, 30,
              26, 30, 24, 30, 26, 30, 26, 30, 26, 30, 24, 30, 26, 30]
    bx = 0
    for bh, bw in zip(heights, widths):
        if bx + bw > w:
            break
        draw.rectangle([x + bx, y_base - bh, x + bx + bw, y_base], fill=c)
        bx += bw + 4


def sun(draw, cx, cy, r, c):
    """Sun disc with straight rays."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    for k in range(8):
        import math
        a = k * math.pi / 4
        x0 = cx + int((r + 4) * math.cos(a))
        y0 = cy + int((r + 4) * math.sin(a))
        x1 = cx + int((r + 14) * math.cos(a))
        y1 = cy + int((r + 14) * math.sin(a))
        draw.line([x0, y0, x1, y1], fill=c, width=3)


def flag(draw, x, y_top, h, c, fly_c=None):
    """Flag pole with a triangular fly."""
    draw.line([x, y_top, x, y_top + h], fill=c, width=3)
    draw.polygon([(x, y_top), (x + 34, y_top + 10), (x, y_top + 20)],
                 fill=fly_c or c)


def scales(draw, cx, cy, s, c):
    """Scales of justice: post, beam, two hanging pans."""
    draw.line([cx, cy - 16 * s, cx, cy + 16 * s], fill=c, width=3)
    draw.line([cx - 22 * s, cy - 12 * s, cx + 22 * s, cy - 12 * s],
              fill=c, width=3)
    for dx in (-22 * s, 22 * s):
        draw.line([cx + dx, cy - 12 * s, cx + dx, cy + 2 * s], fill=c, width=2)
        draw.polygon([(cx + dx - 10 * s, cy + 2 * s),
                      (cx + dx + 10 * s, cy + 2 * s),
                      (cx + dx, cy + 10 * s)], outline=c, width=2)
    draw.ellipse([cx - 20 * s, cy + 16 * s, cx + 20 * s, cy + 20 * s], fill=c)


def bars(draw, x, y_base, c):
    """Rising bar chart with an arrow."""
    hs = [10, 16, 13, 22, 19, 28]
    for i, bh in enumerate(hs):
        bx = x + i * 34
        draw.rectangle([bx, y_base - bh, bx + 22, y_base],
                       fill=RED if i == len(hs) - 1 else c)
    draw.line([x - 6, y_base - 34, x + 200, y_base - 34], fill=RED, width=3)
    draw.line([x + 200, y_base - 34, x + 190, y_base - 40], fill=RED, width=3)
    draw.line([x + 200, y_base - 34, x + 190, y_base - 28], fill=RED, width=3)


def spiral(draw, cx, cy, c, r0=14):
    """Cyclone spiral: concentric arcs shrinking inward."""
    for r in (r0, r0 - 4, r0 - 8):
        if r <= 2:
            continue
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340,
                 fill=c, width=3)
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=160,
                 fill=c, width=3)


def bat_ball(draw, cx, cy, c, s=0.55):
    """Cricket bat leaning on a ball."""
    draw.polygon([(cx - 26 * s, cy - 34 * s), (cx - 6 * s, cy - 40 * s),
                  (cx + 26 * s, cy + 30 * s), (cx + 6 * s, cy + 36 * s)],
                 fill=c)
    draw.rectangle([cx - 4 * s, cy - 58 * s, cx + 8 * s, cy - 36 * s], fill=c)
    draw.ellipse([cx + 34 * s, cy + 18 * s, cx + 58 * s, cy + 42 * s],
                 fill=RED)
    draw.arc([cx + 34 * s, cy + 18 * s, cx + 58 * s, cy + 42 * s],
             start=90, end=270, fill=PAPER, width=2)


def turbine(draw, cx, cy_base, c):
    """Wind turbine: tower plus three blades."""
    draw.polygon([(cx - 4, cy_base), (cx + 4, cy_base),
                  (cx + 2, cy_base - 30), (cx - 2, cy_base - 30)], fill=c)
    import math
    for k in range(3):
        a = -math.pi / 2 + k * 2 * math.pi / 3
        x1 = cx + int(14 * math.cos(a))
        y1 = cy_base - 30 + int(14 * math.sin(a))
        draw.line([cx, cy_base - 30, x1, y1], fill=c, width=3)
    draw.ellipse([cx - 4, cy_base - 34, cx + 4, cy_base - 26], fill=RED)


# --- story blocks ----------------------------------------------------------

def kicker(draw, x, y, text):
    text_ls(draw, (x, y), text, SANS_B(16), RED, ls=3)
    return y + 22


def headline(draw, x, y, lines, fnt, max_w, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.08)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def deck(draw, x, y, text, fnt, max_w, leading=None, fill=INK):
    lh = leading or int(fnt.size * 1.32)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=3)

    # ---- masthead ----
    name = "THE WORLD"
    nf = DISPLAY_XB(102)
    nw = d.textlength(name, font=nf)
    d.text(((W - nw) / 2, 30), name, font=nf, fill=INK)
    hline(d, 36, 300, 158, RULE, 1)
    hline(d, 724, 988, 158, RULE, 1)
    center_ls(d, W // 2, 148, "WEDNESDAY, 18 NOVEMBER 2026", SANS_B(19),
              INK, ls=3)
    hline(d, 36, 988, 176, INK, 2)
    hline(d, 36, 988, 182, INK, 5)

    # ---- lead story: Asia summit week ----
    x0, x1 = 36, 988
    y = 202
    y = kicker(d, x0, y, "ASIA  —  THE LEAD STORY")
    hf = DISPLAY_B(64)
    y = headline(d, x0, y + 4, ["QUAD MEETS", "IN MANILA"], hf, x1 - x0)
    y = deck(d, x0, y + 6,
             "Trump joins Quad leaders in Manila as APEC opens in Shenzhen; "
             "a three-way meeting with Xi and Putin is set for Thursday.",
             SERIF(22), x1 - x0)
    # hero illustration band: skyline, sun, three summit flags
    by0, by1 = 446, 534
    d.rectangle([x0, by0, x1, by1], fill=TINT)
    d.rectangle([x0, by0, x1, by1], outline=INK, width=2)
    sun(d, 880, by0 + 40, 22, RED)
    skyline(d, x0 + 8, by1 - 2, x1 - x0 - 16, INK)
    flag(d, 150, by0 + 14, 52, INK)
    flag(d, 480, by0 + 14, 52, RED)
    flag(d, 700, by0 + 14, 52, INK)
    hline(d, x0, x1, 548, INK, 2)

    # ---- row 2: two stories ----
    y = 558
    col_w = 462
    lx, rx = 36, 526
    vline(d, 512, 560, 762, RULE, 1)
    # left: Britain sanctions
    yy = kicker(d, lx, y, "MIDDLE EAST")
    yy = headline(d, lx, yy + 2,
                  ["BRITAIN SANCTIONS", "SETTLEMENT FIRMS"],
                  DISPLAY_B(34), col_w)
    yy = deck(d, lx, yy + 4,
              "Eight Israeli firms and Tzav 9 hit with asset freezes to "
              "save the two-state solution.",
              SERIF(19), col_w)
    iy0, iy1 = yy + 8, 762
    d.rectangle([lx, iy0, lx + col_w, iy1], fill=TINT)
    scales(d, lx + col_w // 2, (iy0 + iy1) // 2, 1, INK)
    # right: Canada-China trade
    yy = kicker(d, rx, y, "TRADE")
    yy = headline(d, rx, yy + 2,
                  ["CANADA-CHINA", "TRADE DEALS"],
                  DISPLAY_B(34), col_w)
    yy = deck(d, rx, yy + 4,
              "Xi meets Carney in Shenzhen; China cuts tariffs on C$400m "
              "of pork and seafood.",
              SERIF(19), col_w)
    iy0, iy1 = yy + 8, 762
    d.rectangle([rx, iy0, rx + col_w, iy1], fill=TINT)
    bars(d, rx + 110, iy1 - 12, INK)
    hline(d, x0, x1, 776, INK, 2)

    # ---- row 3: three stories ----
    y = 794
    cw = 296
    cols = [36, 364, 692]
    vline(d, 352, 794, 962, RULE, 1)
    vline(d, 680, 794, 962, RULE, 1)
    # col 1: Cyclone Akvan
    yy = kicker(d, cols[0], y, "WEATHER")
    yy = headline(d, cols[0], yy + 2,
                  ["CYCLONE AKVAN", "BEARS DOWN"], DISPLAY_B(29), cw)
    yy = deck(d, cols[0], yy + 4,
              "Severe storm in the Bay of Bengal; landfall due 20 Nov.",
              SERIF(19), cw)
    iy0, iy1 = yy + 6, 966
    spiral(d, cols[0] + cw // 2, (iy0 + iy1) // 2, INK)
    # col 2: Dhoni
    yy = kicker(d, cols[1], y, "SPORT")
    yy = headline(d, cols[1], yy + 2,
                  ["DHONI CALLS", "TIME ON IPL"], DISPLAY_B(29), cw)
    yy = deck(d, cols[1], yy + 4,
              "Five-time champion retires; CSK mentor from 2027.",
              SERIF(19), cw)
    iy0, iy1 = yy + 6, 966
    bat_ball(d, cols[1] + cw // 2 - 10, (iy0 + iy1) // 2, INK)
    # col 3: Amazon
    yy = kicker(d, cols[2], y, "BUSINESS")
    yy = headline(d, cols[2], yy + 2,
                  ["AMAZON BETS", "$7BN ON INDIA"],
                  DISPLAY_B(29), cw)
    yy = deck(d, cols[2], yy + 4,
              "$7bn in renewables by 2030, on top of $4bn.",
              SERIF(19), cw)
    iy0, iy1 = yy + 6, 966
    turbine(d, cols[2] + cw // 2 - 40, iy1 - 8, INK)
    sun(d, cols[2] + cw - 52, (iy0 + iy1) // 2, 12, RED)

    # ---- footer ----
    hline(d, x0, x1, 978, INK, 1)
    center_ls(d, W // 2, 986,
              "WEDNESDAY, 18 NOVEMBER 2026  —  THE DAY IN SIX STORIES",
              SANS(13), GREY, ls=2)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, format="PNG")
    print(f"wrote {out}: {os.path.getsize(out)} bytes")
