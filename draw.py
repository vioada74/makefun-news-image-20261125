#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024 PNG).

Layout: newspaper masthead + date ribbon, one large hero story, a grid of
eight photo blocks, and a markets ticker along the bottom. All text is drawn
with PIL using the DejaVu fonts; all photos are AI illustrations generated
for this entry (no text inside the photos, no recognisable real people).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "img")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN  # 976

PAPER = (251, 248, 241)
INK = (17, 17, 17)
RED = (176, 30, 30)
GREY = (96, 96, 96)
TICKER_BG = (17, 17, 17)
TICKER_FG = (245, 245, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 50)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_HERO_SUM = font("DejaVuSans.ttf", 19)
F_KICKER = font("DejaVuSans-Bold.ttf", 12)
F_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_SUM = font("DejaVuSans.ttf", 14)
F_TICKER = font("DejaVuSans-Bold.ttf", 14)


def text_width(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_width):
    """Word-wrap text to fit max_width, returning a list of lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_width(draw, trial, fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def cover(im, tw, th):
    """Center-crop image to the target aspect ratio, then resize to it."""
    iw, ih = im.size
    target = tw / th
    src = iw / ih
    if src > target:  # too wide: trim sides
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:  # too tall: trim top and bottom
        nh = int(iw / target)
        y0 = (ih - nh) // 2
        im = im.crop((0, y0, iw, y0 + nh))
    return im.resize((tw, th), Image.LANCZOS)


def photo(name):
    return Image.open(os.path.join(IMG_DIR, name + ".jpg")).convert("RGB")


HERO_HEADLINE = "TWO TANKERS HIT MINES IN STRAIT OF HORMUZ"
HERO_SUMMARY = "Oil tankers explode and burn after striking sea mines, Iran's IRGC says."

# (kicker, headline, summary, photo file)
BLOCKS = [
    ("YEMEN", "HOUTHIS STRIKE SAUDI OIL REFINERY",
     "Yemen's Houthis attack Ras Tanura refinery in Saudi Arabia.", "b1"),
    ("GAZA", "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "Mohammad Abuelouf killed in Gaza, Hamas says.", "b2"),
    ("SPACE", "PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG",
     "Muhammad Zeeshan Ali arrives at China's space station.", "b3"),
    ("TECH", "FCC CLEARS SPACEX'S MILLION-SATELLITE NETWORK",
     "Starmind would put one million data-centre satellites in orbit.", "b4"),
    ("TRADE", "TRUMP READIES NEW TARIFFS",
     "New duties planned for China, the EU and others.", "b5"),
    ("UKRAINE", "RUSSIAN STRIKE KILLS TWO IN ODESA",
     "Attack injures three, including a child, officials say.", "b6"),
    ("SUDAN", "RSF DRONE STRIKE KILLS 19 IN SUDAN",
     "Nineteen civilians killed, twenty wounded, medics report.", "b7"),
    ("PACIFIC", "AUSTRALIA-SOLOMONS PACT BANS FOREIGN BASES",
     "Deal bars foreign military bases in Solomon Islands.", "b8"),
]

TICKER_LINES = [
    "KOSPI 4,697.51 \u25bc 6.16%   \u00b7   TAIEX 38,195.43 \u25bc 4.80%   \u00b7   NIKKEI 57,011.62 \u25bc 2.78%   \u00b7   DOW 50,182.95 \u25b2 0.33%",
    "S&P 500 7,182.78 \u25bc 0.25%   \u00b7   NASDAQ 23,585.80 \u25bc 0.62%   \u00b7   US Q3 GDP 4.3%   \u00b7   HUAWEI GUILTY IN US COURT",
]


def draw_page():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # --- masthead ---
    d.line([(MARGIN, 12), (W - MARGIN, 12)], fill=INK, width=3)
    title = "WORLD NEWS ROUNDUP"
    tw = text_width(d, title, F_MASTHEAD)
    d.text(((W - tw) / 2, 16), title, font=F_MASTHEAD, fill=INK)
    d.line([(MARGIN, 76), (W - MARGIN, 76)], fill=INK, width=2)

    # --- date ribbon ---
    date_text = "WEDNESDAY, 25 NOVEMBER 2026"
    dw = text_width(d, date_text, F_DATE)
    cx = W / 2
    d.line([(MARGIN, 96), (cx - dw / 2 - 18, 96)], fill=RED, width=2)
    d.line([(cx + dw / 2 + 18, 96), (W - MARGIN, 96)], fill=RED, width=2)
    d.text((cx - dw / 2, 84), date_text, font=F_DATE, fill=RED)

    # --- hero photo ---
    hero = cover(photo("hero"), CONTENT_W, 250)
    page.paste(hero, (MARGIN, 112))

    # --- hero headline + summary ---
    hw = text_width(d, HERO_HEADLINE, F_HERO_HEAD)
    d.text(((W - hw) / 2, 370), HERO_HEADLINE, font=F_HERO_HEAD, fill=INK)
    sw = text_width(d, HERO_SUMMARY, F_HERO_SUM)
    d.text(((W - sw) / 2, 404), HERO_SUMMARY, font=F_HERO_SUM, fill=INK)

    d.line([(MARGIN, 442), (W - MARGIN, 442)], fill=INK, width=2)

    # --- grid of eight blocks: 4 columns x 2 rows ---
    gap = 12
    cell_w = (CONTENT_W - 3 * gap) // 4  # 235
    cell_h = 250
    grid_top = 452
    photo_h = 112
    for i, (kicker, headline, summary, img_name) in enumerate(BLOCKS):
        col = i % 4
        row = i // 4
        x = MARGIN + col * (cell_w + gap)
        y = grid_top + row * (cell_h + 8)
        page.paste(cover(photo(img_name), cell_w, photo_h), (x, y))
        ky = y + photo_h + 5
        d.text((x, ky), kicker, font=F_KICKER, fill=RED)
        hy = ky + 16
        head_lines = wrap(d, headline, F_HEAD, cell_w)
        for j, line in enumerate(head_lines):
            d.text((x, hy + j * 20), line, font=F_HEAD, fill=INK)
        # Summary starts below however many lines the headline took, so the
        # two can never collide.
        sy = hy + len(head_lines) * 20 + 4
        for j, line in enumerate(wrap(d, summary, F_SUM, cell_w)):
            d.text((x, sy + j * 17), line, font=F_SUM, fill=INK)

    # --- markets ticker ---
    d.rectangle([(MARGIN, 966), (W - MARGIN, 1012)], fill=TICKER_BG)
    for j, line in enumerate(TICKER_LINES):
        lw = text_width(d, line, F_TICKER)
        d.text(((W - lw) / 2, 972 + j * 20), line, font=F_TICKER, fill=TICKER_FG)

    return page


def main():
    page = draw_page()
    page.save(OUT, format="PNG", optimize=True, compress_level=9)
    size = os.path.getsize(OUT)
    print("wrote", OUT, page.size, size, "bytes")
    if size > 1048576:
        print("WARNING: over the 1 MiB limit")


if __name__ == "__main__":
    main()
