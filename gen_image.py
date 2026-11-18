#!/usr/bin/env python3
"""Front page for Wednesday, 18 November 2026.

Draws a 1024x1024 newspaper front page with Pillow only: masthead,
dateline, one lead story, a drawn hero band, two mid stories and three
short stories, each with a small pictogram. No network, no external
images, no clock: identical input always yields an identical PNG.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 48
CONTENT_W = W - 2 * MARGIN  # 928

PAPER = (251, 247, 238)
INK = (20, 20, 20)
RED = (140, 29, 24)
NAVY = (30, 58, 92)
GOLD = (200, 162, 74)
SKY_TOP = (44, 84, 128)
SKY_BOTTOM = (214, 228, 238)
MUTED = (96, 96, 92)

NOTO = "/usr/share/fonts/truetype/noto"
DEJAVU = "/usr/share/fonts/truetype/dejavu"
LIBERATION = "/usr/share/fonts/truetype/liberation"

FONT_PATHS = {
    "black": [f"{NOTO}/NotoSerifDisplay-Black.ttf",
              f"{DEJAVU}/DejaVuSerif-Bold.ttf"],
    "bold": [f"{NOTO}/NotoSerifDisplay-Bold.ttf",
             f"{LIBERATION}/LiberationSerif-Bold.ttf",
             f"{DEJAVU}/DejaVuSerif-Bold.ttf"],
    "serif": [f"{NOTO}/NotoSerifDisplay-Regular.ttf",
              f"{LIBERATION}/LiberationSerif-Regular.ttf",
              f"{DEJAVU}/DejaVuSerif.ttf"],
    "sans_bold": [f"{DEJAVU}/DejaVuSans-Bold.ttf",
                  f"{DEJAVU}/DejaVuSans.ttf"],
    "sans": [f"{DEJAVU}/DejaVuSans.ttf"],
}


def load_font(kind, size):
    for path in FONT_PATHS[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, kind, size, max_width, max_lines):
    """Shrink the font until the text wraps into at most max_lines."""
    size = int(size)
    while size > 10:
        font = load_font(kind, size)
        lines = wrap_text(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 1
    font = load_font(kind, size)
    return font, wrap_text(draw, text, font, max_width)


def centred(draw, cx, y, lines, font, fill, leading):
    """Draw lines centred on cx, top edge at y; returns bottom y."""
    for line in lines:
        draw.text((cx, y), line, font=font, fill=fill, anchor="ma")
        y += leading
    return y


def rule(draw, y, weight=2, fill=INK, x0=None, x1=None):
    x0 = MARGIN if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


# ---------------------------------------------------------------- icons

def icon_scales(draw, cx, cy, s=1.0):
    """Balance scales: post, beam, two hanging pans."""
    top = cy - 24 * s
    draw.line([(cx, top), (cx, cy + 22 * s)], fill=NAVY, width=3)
    draw.line([(cx - 26 * s, top + 4 * s), (cx + 26 * s, top + 4 * s)],
              fill=NAVY, width=3)
    draw.ellipse([cx - 3 * s, top - 5 * s, cx + 3 * s, top + 1 * s], fill=RED)
    for side in (-1, 1):
        px = cx + side * 26 * s
        draw.line([(px, top + 4 * s), (px - 9 * s, cy + 8 * s)],
                  fill=NAVY, width=2)
        draw.line([(px, top + 4 * s), (px + 9 * s, cy + 8 * s)],
                  fill=NAVY, width=2)
        draw.arc([px - 11 * s, cy - 2 * s, px + 11 * s, cy + 18 * s],
                 start=0, end=180, fill=NAVY, width=2)
        draw.line([(px - 11 * s, cy + 8 * s), (px + 11 * s, cy + 8 * s)],
                  fill=NAVY, width=2)
    draw.line([(cx - 12 * s, cy + 22 * s), (cx + 12 * s, cy + 22 * s)],
              fill=NAVY, width=3)


def icon_bars(draw, cx, cy, s=1.0):
    """Bar chart: axis plus three rising bars."""
    base = cy + 20 * s
    draw.line([(cx - 26 * s, base), (cx + 28 * s, base)], fill=NAVY, width=3)
    draw.line([(cx - 26 * s, base), (cx - 26 * s, cy - 24 * s)],
              fill=NAVY, width=3)
    heights = [16, 28, 42]
    colours = [GOLD, NAVY, RED]
    for i, hgt in enumerate(heights):
        x0 = cx - 20 * s + i * 18 * s
        draw.rectangle([x0, base - hgt * s, x0 + 12 * s, base - 3],
                       fill=colours[i])


def icon_spiral(draw, cx, cy, s=1.0):
    """Cyclone spiral: an Archimedean coil with a calm eye."""
    pts = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps * 4.6 * math.pi
        r = 2.0 + 1.9 * t
        pts.append((cx + r * math.cos(t) * s, cy + r * math.sin(t) * s))
    draw.line(pts, fill=NAVY, width=3, joint="curve")
    draw.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s],
                 fill=RED)


def icon_cricket(draw, cx, cy, s=1.0):
    """Cricket bat leaning over a ball."""
    # Blade: thick diagonal stroke; handle: thin continuation.
    draw.line([(cx - 10 * s, cy + 20 * s), (cx + 4 * s, cy - 12 * s)],
              fill=NAVY, width=11)
    draw.line([(cx + 4 * s, cy - 12 * s), (cx + 10 * s, cy - 24 * s)],
              fill=RED, width=4)
    draw.ellipse([cx + 8 * s, cy + 8 * s, cx + 24 * s, cy + 24 * s],
                 fill=GOLD, outline=RED, width=2)
    draw.arc([cx + 11 * s, cy + 9 * s, cx + 21 * s, cy + 23 * s],
             start=200, end=340, fill=RED, width=2)


def icon_turbine(draw, cx, cy, s=1.0):
    """Wind turbine under a small sun."""
    hub_x, hub_y = cx - 8 * s, cy + 2 * s
    draw.line([(hub_x, hub_y), (hub_x - 3 * s, cy + 24 * s)],
              fill=NAVY, width=3)
    draw.line([(hub_x, hub_y), (hub_x + 3 * s, cy + 24 * s)],
              fill=NAVY, width=3)
    for k in range(3):
        ang = math.radians(-90 + k * 120)
        ex = hub_x + 19 * s * math.cos(ang)
        ey = hub_y + 19 * s * math.sin(ang)
        draw.line([(hub_x, hub_y), (ex, ey)], fill=NAVY, width=3)
    draw.ellipse([hub_x - 3 * s, hub_y - 3 * s, hub_x + 3 * s, hub_y + 3 * s],
                 fill=RED)
    # Sun with rays, top right of the turbine.
    sx, sy = cx + 16 * s, cy - 14 * s
    for k in range(8):
        ang = math.radians(k * 45)
        x0 = sx + 9 * s * math.cos(ang)
        y0 = sy + 9 * s * math.sin(ang)
        x1 = sx + 13 * s * math.cos(ang)
        y1 = sy + 13 * s * math.sin(ang)
        draw.line([(x0, y0), (x1, y1)], fill=GOLD, width=2)
    draw.ellipse([sx - 7 * s, sy - 7 * s, sx + 7 * s, sy + 7 * s], fill=GOLD)


# ---------------------------------------------------------------- hero band

def hero_band(draw, x0, y0, x1, y1):
    """Stylised skyline at dusk: gradient sky, sun, towers, birds."""
    band_h = y1 - y0
    strips = 10
    for i in range(strips):
        f = i / (strips - 1)
        col = tuple(int(SKY_TOP[c] + (SKY_BOTTOM[c] - SKY_TOP[c]) * f)
                    for c in range(3))
        sy = y0 + i * band_h // strips
        ey = y0 + (i + 1) * band_h // strips
        draw.rectangle([x0, sy, x1, ey], fill=col)
    # Sun, upper right.
    sx, sy = x1 - 110, y0 + 42
    draw.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=GOLD)
    # Birds.
    for bx, by in ((x0 + 150, y0 + 34), (x0 + 210, y0 + 52)):
        draw.line([(bx - 9, by), (bx, by - 6), (bx + 9, by)],
                  fill=INK, width=2)
    # Skyline silhouettes with a few lit windows.
    heights = [58, 86, 46, 98, 70, 112, 62, 90, 52, 80]
    bw = (x1 - x0) // len(heights)
    for i, bh in enumerate(heights):
        bx0 = x0 + i * bw + 4
        bx1 = x0 + (i + 1) * bw - 4
        draw.rectangle([bx0, y1 - bh, bx1, y1], fill=NAVY)
        for row in range((bh - 14) // 16):
            for col_i in range((bx1 - bx0 - 12) // 14):
                if (row + col_i + i) % 3 == 0:
                    wx = bx0 + 7 + col_i * 14
                    wy = y1 - bh + 8 + row * 16
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=GOLD)
    # Ground strip.
    draw.rectangle([x0, y1 - 6, x1, y1], fill=INK)


# ---------------------------------------------------------------- page

def story_cell(draw, x0, x1, y_top, headline, deck, icon, head_size,
               deck_size):
    """One story: pictogram strip, headline, deck. No overlaps by design:
    each element owns its own vertical band."""
    cx = (x0 + x1) // 2
    width = x1 - x0
    icon(draw, cx, y_top + 26)
    hy = y_top + 62
    font, lines = fit_lines(draw, headline, "bold", head_size, width, 2)
    leading = int(head_size * 1.12)
    hy = centred(draw, cx, hy, lines, font, INK, leading)
    dy = hy + 6
    dfont, dlines = fit_lines(draw, deck, "serif", deck_size, width, 2)
    dleading = int(deck_size * 1.25)
    centred(draw, cx, dy, dlines, dfont, INK, dleading)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    mast = load_font("black", 92)
    draw.text((W // 2, 22), "THE WORLD", font=mast, fill=INK, anchor="ma")
    rule(draw, 132, weight=3)
    rule(draw, 139, weight=1)

    # Dateline.
    date_font = load_font("sans_bold", 20)
    draw.text((W // 2, 152), "WEDNESDAY, 18 NOVEMBER 2026",
              font=date_font, fill=INK, anchor="ma")

    # Lead kicker + headline + deck.
    kick = load_font("sans_bold", 21)
    draw.text((W // 2, 188), "ASIA SUMMIT WEEK", font=kick, fill=RED,
              anchor="ma")
    lead_head = load_font("black", 62)
    draw.text((W // 2, 216), "QUAD MEETS IN MANILA", font=lead_head,
              fill=INK, anchor="ma")
    deck_font, deck_lines = fit_lines(
        draw,
        "Trump in Manila for Quad talks on a three-day Asia trip ending "
        "in China; APEC meets in Shenzhen 18\u201319 Nov; Xi, Trump and "
        "Putin talk Thursday.",
        "serif", 25, CONTENT_W, 2)
    centred(draw, W // 2, 292, deck_lines, deck_font, INK, 31)

    # Hero band.
    hero_band(draw, MARGIN, 362, W - MARGIN, 492)
    rule(draw, 510, weight=2)

    # Row 2: two stories.
    story_cell(draw, MARGIN, 492, 526,
               "BRITAIN SANCTIONS SETTLEMENT FIRMS",
               "Asset freezes and bans hit eight firms and Tzav 9, "
               "says Miliband.",
               icon_scales, 30, 20)
    story_cell(draw, 532, W - MARGIN, 526,
               "CANADA\u2013CHINA EXTEND TRADE DEALS",
               "Xi meets Carney; C$400m of tariff relief; steel "
               "extended 2 years.",
               icon_bars, 30, 20)
    draw.line([(512, 526), (512, 706)], fill=MUTED, width=1)

    rule(draw, 722, weight=2)

    # Row 3: three stories.
    col_w = 296
    gap = 20
    x = MARGIN
    story_cell(draw, x, x + col_w, 738,
               "CYCLONE AKVAN BEARS DOWN",
               "Severe storm, winds 120\u2013130 km/h; landfall due near "
               "noon on 20 Nov.",
               icon_spiral, 25, 18)
    x += col_w + gap
    story_cell(draw, x, x + col_w, 738,
               "DHONI CALLS TIME ON IPL",
               "Five-time champion retires; CSK mentor in 2027; "
               "5,439 runs.",
               icon_cricket, 25, 18)
    x += col_w + gap
    story_cell(draw, x, x + col_w, 738,
               "AMAZON BETS $7BN ON GREEN INDIA",
               "$7bn renewables by 2030, plus $4bn already contracted; "
               "934 MW new.",
               icon_turbine, 25, 18)

    # Footer.
    rule(draw, 946, weight=2)
    foot = load_font("sans_bold", 17)
    draw.text((W // 2, 958),
              "WEDNESDAY, 18 NOVEMBER 2026 \u2014 THE DAY IN SIX STORIES",
              font=foot, fill=INK, anchor="ma")

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, format="PNG")
    print(out)


if __name__ == "__main__":
    main()
