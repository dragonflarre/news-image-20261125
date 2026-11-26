#!/usr/bin/env python3
"""The Daily Compass — Wednesday 25 November 2026.

Front page for the make.fun news-image-20261125 entry: Britain sanctions
five of Myanmar's generals after the world court's genocide verdict, Poland
urges NATO to shoot down Russian missiles over Ukraine, Libya vows revenge
after the Benghazi strike, and Huawei is found guilty in a US court. Drawn
with PIL only; writes entry.png next to itself.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 960, 1024
PAPER = (247, 243, 233)
INK = (26, 23, 18)
ACCENT = (140, 43, 29)
FAINT = (110, 102, 88)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, leading, fill=INK):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, y, text, fnt, fill=INK):
    draw.text(((W - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)
    return y


def rule(draw, y, weight=2):
    draw.line([(36, y), (W - 36, y)], fill=INK, width=weight)
    return y


def gavel(draw, cx, cy):
    """A simple gavel mark: head as a slanted block, handle below it."""
    draw.polygon([(cx - 52, cy - 74), (cx + 8, cy - 74), (cx + 8, cy - 34),
                  (cx - 52, cy - 34)], fill=INK)
    draw.line([(cx - 22, cy - 30), (cx - 58, cy + 74)], fill=INK, width=7)
    draw.line([(cx - 84, cy + 74), (cx - 32, cy + 74)], fill=INK, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top strip -------------------------------------------------------
    d.text((36, 14), "Vol. V — No. 329", font=font(SANS, 17), fill=FAINT)
    right = "LONDON • WARSAW • BENGHAZI"
    d.text((W - 36 - d.textlength(right, font=font(SANS, 17)), 14), right,
           font=font(SANS, 17), fill=FAINT)
    rule(d, 42, 1)

    # --- masthead --------------------------------------------------------
    size = 84
    while d.textlength("THE DAILY COMPASS", font=font(SERIF_B, size)) > W - 72:
        size -= 2
    centred(d, 52, "THE DAILY COMPASS", font(SERIF_B, size))
    rule(d, 146, 4)
    rule(d, 154, 1)
    centred(d, 162, "WEDNESDAY, 25 NOVEMBER 2026", font(SANS_B, 25))
    centred(d, 192, "The day's news, on one page", font(SERIF_I, 19), fill=FAINT)
    rule(d, 222, 2)

    # --- lead ------------------------------------------------------------
    d.text((36, 236), "LONDON  •  AFTER THE VERDICT", font=font(SANS_B, 19), fill=ACCENT)
    y = para(d, (36, 262), "BRITAIN SANCTIONS MYANMAR'S GENERALS",
             font(SERIF_B, 49), W - 72, 52)
    y = para(d, (36, y + 4),
             "London moves first after the world court's genocide verdict — five "
             "senior officers face asset freezes and travel bans",
             font(SERIF_I, 21), W - 72, 26, fill=(60, 54, 44))

    gavel(d, 140, y + 100)
    lead = ("LONDON — Britain has announced fresh sanctions against five senior "
            "Myanmar military leaders, the first concrete action after the "
            "International Court of Justice ruled that Myanmar committed genocide "
            "against the Rohingya. The measures freeze the officers' assets, bar "
            "them from travelling and restrict their company roles, and London will "
            "also curb the supply of aviation fuel the military uses for air strikes "
            "on civilians. The court's verdict — the first time it has held a state "
            "responsible for genocide — ordered Myanmar to investigate and punish "
            "those responsible and to pay compensation. Myanmar's junta called the "
            "decision “unfair”.")
    y = para(d, (248, y + 22), lead, font(SERIF, 17), W - 248 - 36, 22)
    rule(d, y + 14, 1)

    # --- three panels ------------------------------------------------------
    top = y + 28
    colw = (W - 72 - 2 * 24) // 3
    panels = [
        ("POLAND WANTS NATO TO SHOOT DOWN MISSILES",
         "WARSAW — Poland urged NATO to consider intercepting Russian missiles "
         "bound for Ukraine that stray toward alliance territory, in the sharpest "
         "call yet to widen the alliance's role in the war."),
        ("LIBYA VOWS REVENGE AFTER BENGHAZI STRIKE",
         "BENGHAZI — Libya vowed to retaliate after Ukraine's strike on a Russian "
         "warship in Benghazi port, as two Libyan naval officers died of wounds "
         "from the attack."),
        ("HUAWEI FOUND GUILTY IN US COURT",
         "NEW YORK — A US jury found Chinese tech giant Huawei guilty of bank "
         "fraud and conspiring to steal trade secrets, in a verdict that deepens "
         "the tech standoff between Washington and Beijing."),
    ]
    bottom = top
    for idx, (head, body) in enumerate(panels):
        x = 36 + idx * (colw + 24)
        hy = para(d, (x, top), head, font(SERIF_B, 18), colw, 22, fill=ACCENT)
        by = para(d, (x, hy + 6), body, font(SERIF, 14), colw, 19)
        bottom = max(bottom, by)
        if idx:
            d.line([(x - 12, top), (x - 12, bottom)], fill=FAINT, width=1)

    # --- briefs ------------------------------------------------------------
    by = bottom + 14
    rule(d, by, 2)
    d.text((36, by + 10), "THE DAY IN BRIEF", font=font(SANS_B, 19), fill=ACCENT)
    briefs = ("At least 30 killed as militants strike in Nigeria's Niger region  •  "
              "Six dead, 20 trapped after a flood hits an unauthorised gold mine in "
              "Indonesia  •  At least 30 die in a petroleum tanker fire in Egypt  •  "
              "Melania Trump helps reunite nine more Ukrainian and Russian children "
              "with their families")
    by = para(d, (36, by + 36), briefs, font(SERIF, 15), W - 72, 20)
    rule(d, by + 10, 1)
    centred(d, by + 18, "The Daily Compass — Wednesday 25 November 2026 — Page 1 of 1",
            font(SANS, 15), fill=FAINT)
    img.save("entry.png", optimize=True)
    print("final y:", by + 44)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
