#!/usr/bin/env python3
"""Generate the DUNGEON ENGINE page icon / favicons with PIL.

Reuses the in-game pixel-art (the horned "brute" monster) on a dark, glowing
tile so the favicon matches the game's look. Outputs:
  icon-512.png, apple-touch-icon.png, favicon-32.png, favicon-16.png, favicon.ico
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.dirname(os.path.abspath(__file__))

# palette + the brute sprite, mirrored from index.html
PAL = {'K': (12, 14, 22), 'P': (196, 90, 255), 'E': (255, 243, 176), 'X': (26, 14, 20)}
BRUTE = [
    "...K........K...", "...KK......KK...", "..KPPK....KPPK..", "..KPPKKKKKKPPK..",
    ".KPPPPPPPPPPPPK.", ".KPPPPPPPPPPPPK.", ".KPPEEPPPPEEPPK.", ".KPPXXPPPPXXPPK.",
    ".KPPPPPPPPPPPPK.", ".KPKKKKKKKKKKPK.", ".KPPPPPPPPPPPPK.", "..KPPPPPPPPPPK..",
    "..KPPPPPPPPPPK..", "...KPPKKKKPPK...", "...KKK..KKK.....", "................",
]
N = 16


def sprite_img(body_only=False):
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    px = im.load()
    for r, row in enumerate(BRUTE):
        for c, ch in enumerate(row):
            if ch == '.':
                continue
            col = PAL['P'] if body_only else PAL.get(ch, (255, 0, 255))
            px[c, r] = (col[0], col[1], col[2], 255)
    return im


def radial_bg(size):
    g = Image.new("RGB", (64, 64))
    gp = g.load()
    cx, cy, maxd = 31.5, 31.5, math.hypot(31.5, 31.5)
    c0, c1 = (26, 31, 48), (9, 11, 18)
    for y in range(64):
        for x in range(64):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            gp[x, y] = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
    return g.resize((size, size), Image.BICUBIC)


def build(size=512):
    # rounded dark tile
    bg = radial_bg(size).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1],
                                           radius=int(size * 0.18), fill=255)
    res = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    res.paste(bg, (0, 0), mask)
    ImageDraw.Draw(res).rounded_rectangle([3, 3, size - 4, size - 4],
                                          radius=int(size * 0.17),
                                          outline=(90, 110, 140, 90), width=max(2, size // 170))

    sp = int(size * 0.62); sp -= sp % N
    sw = (sp // N) * N
    ox = (size - sw) // 2
    oy = (size - sw) // 2 - int(size * 0.015)

    # soft shadow under the monster
    sh = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([ox + sw * 0.16, oy + sw * 0.9,
                                ox + sw * 0.84, oy + sw * 1.04], fill=(0, 0, 0, 130))
    sh = sh.filter(ImageFilter.GaussianBlur(size * 0.02))
    res = Image.alpha_composite(res, sh)

    # colored glow (blurred silhouette)
    glow = sprite_img(body_only=True).resize((sw, sw), Image.NEAREST)
    gl = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gl.paste(glow, (ox, oy), glow)
    gl = gl.filter(ImageFilter.GaussianBlur(size * 0.045))
    r, g, b, a = gl.split()
    gl = Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v * 0.7))))
    res = Image.alpha_composite(res, gl)

    # crisp pixel monster on top
    res.alpha_composite(sprite_img().resize((sw, sw), Image.NEAREST), (ox, oy))
    return res


icon = build(512)
icon.save(os.path.join(OUT, "icon-512.png"))
for s in (32, 16):
    icon.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, f"favicon-{s}.png"))
icon.save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# opaque square for iOS home-screen
at = Image.alpha_composite(Image.new("RGBA", (512, 512), (11, 13, 21, 255)), icon)
at.convert("RGB").resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"))
print("icons written to", OUT)
