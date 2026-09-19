#!/usr/bin/env python3
"""Pack processed sheets into public/sprites plus palette variants and pixel props."""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path("/workspace")
SRC = ROOT / "assets/sprites"
OUT = ROOT / "public/sprites"
OUT.mkdir(parents=True, exist_ok=True)


def copy_sheet(src: Path, dest_name: str) -> None:
    im = Image.open(src).convert("RGBA")
    im.save(OUT / dest_name, "PNG")


def hue_shift(im: Image.Image, degrees: float, sat: float = 1.0, val: float = 1.0) -> Image.Image:
    rgba = im.convert("RGBA")
    hsv = rgba.convert("HSV")
    h, s, v = hsv.split()
    h = h.point(lambda p: int((p + degrees / 360 * 255) % 255))
    if sat != 1.0:
        s = s.point(lambda p: max(0, min(255, int(p * sat))))
    if val != 1.0:
        v = v.point(lambda p: max(0, min(255, int(p * val))))
    out = Image.merge("HSV", (h, s, v)).convert("RGBA")
    out.putalpha(rgba.getchannel("A"))
    return out


def recolor_mul(im: Image.Image, r: float, g: float, b: float) -> Image.Image:
    px = im.convert("RGBA")
    data = list(px.getdata())
    out = []
    for pr, pg, pb, pa in data:
        if pa < 8:
            out.append((pr, pg, pb, pa))
            continue
        out.append(
            (
                max(0, min(255, int(pr * r))),
                max(0, min(255, int(pg * g))),
                max(0, min(255, int(pb * b))),
                pa,
            )
        )
    px.putdata(out)
    return px


def portrait_from(frame: Path, dest: str) -> None:
    im = Image.open(frame).convert("RGBA")
    w, h = im.size
    crop = im.crop((0, 0, w, int(h * 0.62)))
    crop = crop.resize((96, 96), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    canvas.paste(crop, (0, 0), crop)
    canvas.save(OUT / dest, "PNG")


def px(draw: ImageDraw.ImageDraw, x: int, y: int, c: tuple, s: int = 1) -> None:
    draw.rectangle([x, y, x + s - 1, y + s - 1], fill=c)


def draw_barrel(size: int = 48) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # metal drum
    body = (70, 92, 78)
    dark = (32, 42, 36)
    light = (150, 168, 142)
    rust = (120, 72, 40)
    d.ellipse([10, 6, 38, 16], fill=light, outline=dark)
    d.rectangle([10, 12, 38, 40], fill=body)
    d.ellipse([10, 34, 38, 44], fill=dark)
    d.ellipse([12, 8, 36, 14], fill=(90, 110, 96))
    d.line([10, 20, 38, 20], fill=dark)
    d.line([10, 28, 38, 28], fill=dark)
    d.rectangle([14, 18, 16, 30], fill=rust)
    d.rectangle([30, 22, 33, 34], fill=light)
    return im


def draw_crate(size: int = 48) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    wood = (156, 110, 58)
    dark = (78, 48, 22)
    light = (198, 154, 88)
    d.rectangle([8, 14, 40, 44], fill=wood, outline=dark)
    d.rectangle([8, 14, 40, 20], fill=light)
    d.line([8, 28, 40, 28], fill=dark)
    d.line([24, 14, 24, 44], fill=dark)
    d.rectangle([12, 18, 16, 22], fill=dark)  # nail
    d.rectangle([32, 18, 36, 22], fill=dark)
    return im


def draw_dumpster(size: int = 56) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    green = (46, 110, 62)
    dark = (18, 48, 28)
    light = (90, 160, 100)
    d.rectangle([6, 16, 50, 50], fill=green, outline=dark)
    d.rectangle([6, 12, 50, 20], fill=light, outline=dark)
    d.rectangle([10, 8, 22, 14], fill=dark)
    d.rectangle([34, 8, 46, 14], fill=dark)
    d.rectangle([12, 24, 20, 44], fill=dark)
    d.rectangle([36, 26, 44, 46], fill=(30, 80, 44))
    return im


def draw_phone(size: int = 48) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    blue = (40, 70, 150)
    dark = (16, 28, 70)
    d.rectangle([14, 4, 34, 46], fill=blue, outline=dark)
    d.rectangle([16, 8, 32, 18], fill=(20, 20, 30))
    d.rectangle([18, 22, 30, 28], fill=(200, 180, 60))
    d.rectangle([18, 32, 22, 36], fill=(220, 220, 230))
    d.rectangle([26, 32, 30, 36], fill=(220, 220, 230))
    return im


def draw_sign(size: int = 48) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([22, 20, 26, 46], fill=(80, 80, 88), outline=(20, 20, 24))
    d.rectangle([8, 6, 40, 24], fill=(180, 40, 40), outline=(60, 10, 10))
    d.rectangle([12, 10, 36, 14], fill=(240, 220, 180))
    return im


def draw_vending(size: int = 56) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([12, 2, 44, 54], fill=(40, 48, 90), outline=(12, 14, 30))
    d.rectangle([16, 8, 40, 32], fill=(20, 160, 170))
    d.rectangle([16, 36, 24, 42], fill=(220, 50, 50))
    d.rectangle([28, 36, 40, 42], fill=(240, 200, 40))
    d.rectangle([18, 46, 38, 50], fill=(10, 10, 16))
    return im


def draw_table(size: int = 56) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 18, 50, 28], fill=(120, 78, 42), outline=(50, 28, 12))
    d.rectangle([10, 28, 14, 46], fill=(70, 44, 22))
    d.rectangle([42, 28, 46, 46], fill=(70, 44, 22))
    return im


def draw_hydrant(size: int = 40) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([14, 10, 26, 36], fill=(200, 40, 40), outline=(80, 10, 10))
    d.ellipse([12, 4, 28, 16], fill=(220, 70, 70), outline=(80, 10, 10))
    d.rectangle([8, 16, 14, 22], fill=(180, 30, 30))
    d.rectangle([26, 16, 32, 22], fill=(180, 30, 30))
    d.rectangle([12, 34, 28, 38], fill=(90, 20, 20))
    return im


def draw_weapon_pipe() -> Image.Image:
    im = Image.new("RGBA", (48, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 5, 44, 11], fill=(140, 148, 156), outline=(40, 44, 50))
    d.rectangle([2, 5, 8, 11], fill=(90, 94, 100))
    return im


def draw_weapon_bat() -> Image.Image:
    im = Image.new("RGBA", (52, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 6, 12, 10], fill=(90, 60, 30), outline=(40, 24, 10))
    d.polygon([(12, 5), (48, 3), (48, 13), (12, 11)], fill=(176, 128, 64), outline=(70, 42, 16))
    return im


def draw_weapon_knife() -> Image.Image:
    im = Image.new("RGBA", (36, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 4, 12, 10], fill=(90, 50, 30), outline=(40, 20, 10))
    d.polygon([(12, 3), (34, 6), (12, 11)], fill=(210, 220, 230), outline=(80, 90, 100))
    return im


def draw_weapon_bottle() -> Image.Image:
    im = Image.new("RGBA", (16, 28), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 2, 10, 8], fill=(40, 140, 90), outline=(10, 50, 30))
    d.rectangle([4, 8, 12, 26], fill=(30, 160, 100), outline=(10, 50, 30))
    d.rectangle([5, 10, 8, 18], fill=(180, 230, 200))
    return im


def draw_weapon_chain() -> Image.Image:
    im = Image.new("RGBA", (48, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(6):
        x = 3 + i * 7
        d.ellipse([x, 3, x + 8, 11], outline=(180, 180, 190), width=2)
    return im


def draw_weapon_hammer() -> Image.Image:
    im = Image.new("RGBA", (40, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([18, 4, 22, 22], fill=(120, 80, 40), outline=(50, 30, 12))
    d.rectangle([8, 2, 32, 10], fill=(90, 96, 110), outline=(30, 32, 40))
    return im


def draw_weapon_katana() -> Image.Image:
    im = Image.new("RGBA", (56, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 5, 14, 9], fill=(40, 30, 28), outline=(20, 12, 10))
    d.rectangle([12, 3, 16, 11], fill=(180, 150, 40))
    d.polygon([(16, 4), (54, 6), (16, 10)], fill=(230, 236, 242), outline=(80, 90, 100))
    return im


def draw_food(kind: str) -> Image.Image:
    im = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if kind == "chicken":
        d.ellipse([4, 8, 20, 20], fill=(210, 150, 60), outline=(90, 50, 10))
        d.rectangle([10, 2, 14, 10], fill=(230, 200, 140))
    elif kind == "soda":
        d.rectangle([8, 4, 16, 20], fill=(200, 30, 40), outline=(80, 10, 10))
        d.rectangle([8, 4, 16, 8], fill=(220, 220, 230))
    elif kind == "pizza":
        d.polygon([(12, 4), (22, 20), (2, 20)], fill=(230, 190, 70), outline=(140, 80, 20))
        d.ellipse([8, 12, 12, 16], fill=(180, 40, 30))
    else:
        d.ellipse([4, 6, 20, 20], fill=(80, 180, 70), outline=(20, 70, 30))
    return im


def draw_impact_sheet() -> Image.Image:
    im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cells = [(0, 0), (64, 0), (0, 64), (64, 64)]
    sizes = [6, 12, 18, 10]
    for (cx, cy), s in zip(cells, sizes):
        ox, oy = cx + 32, cy + 32
        d.ellipse([ox - s, oy - s, ox + s, oy + s], outline=(255, 240, 180, 230), width=2)
        d.ellipse([ox - s // 2, oy - s // 2, ox + s // 2, oy + s // 2], fill=(255, 255, 255, 180))
        for a in range(0, 360, 45):
            import math

            rad = math.radians(a)
            x2 = ox + int(math.cos(rad) * (s + 8))
            y2 = oy + int(math.sin(rad) * (s + 8))
            d.line([(ox, oy), (x2, y2)], fill=(255, 220, 80, 200), width=2)
    return im


def assemble_sheet(frames: list[Image.Image], cols: int, rows: int, cell: int) -> Image.Image:
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        r, c = divmod(i, cols) if False else (i // cols, i % cols)
        canvas = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
        fr = fr.convert("RGBA")
        scale = min(cell / fr.width, cell / fr.height) * 0.9
        nw, nh = max(1, int(fr.width * scale)), max(1, int(fr.height * scale))
        frs = fr.resize((nw, nh), Image.Resampling.NEAREST)
        canvas.paste(frs, ((cell - nw) // 2, cell - nh - 2), frs)
        sheet.paste(canvas, (c * cell, r * cell), canvas)
    return sheet


def main() -> None:
    mapping = {
        "kael-idle": SRC / "kael-idle/sheet-transparent.png",
        "kael-attack": SRC / "kael-attack/sheet-transparent.png",
        "vyra-idle": SRC / "vyra-idle/sheet-transparent.png",
        "vyra-attack": SRC / "vyra-attack/sheet-transparent.png",
        "rutger-idle": SRC / "rutger-idle/sheet-transparent.png",
        "rutger-attack": SRC / "rutger-attack/sheet-transparent.png",
        "sien-idle": SRC / "sien-idle/sheet-transparent.png",
        "thug": SRC / "thug/sheet-transparent.png",
        "runner": SRC / "runner/sheet-transparent.png",
        "brute": SRC / "brute/sheet-transparent.png",
    }
    for name, path in mapping.items():
        if path.exists():
            copy_sheet(path, f"{name}.png")

    # Sien has no attack sheet — reuse idle with a hue-locked copy labeled attack
    sien = SRC / "sien-idle/sheet-transparent.png"
    if sien.exists():
        copy_sheet(sien, "sien-attack.png")

    # Walk sheets reuse idle (weight-shift frames already exist)
    for hero in ("kael", "vyra", "rutger", "sien"):
        idle = SRC / f"{hero}-idle/sheet-transparent.png"
        if idle.exists():
            copy_sheet(idle, f"{hero}-walk.png")

    # Enemy palette variants
    thug = Image.open(SRC / "thug/sheet-transparent.png").convert("RGBA")
    runner = Image.open(SRC / "runner/sheet-transparent.png").convert("RGBA")
    brute = Image.open(SRC / "brute/sheet-transparent.png").convert("RGBA")

    hue_shift(thug, 40, 0.9, 0.85).save(OUT / "grabber.png")
    recolor_mul(thug, 0.75, 0.65, 0.5).save(OUT / "shooter.png")
    recolor_mul(thug, 0.9, 0.55, 0.45).save(OUT / "armed.png")
    hue_shift(runner, -20, 0.4, 1.15).save(OUT / "elite.png")
    recolor_mul(brute, 0.7, 0.75, 0.95).save(OUT / "shield.png")
    recolor_mul(brute, 1.1, 0.7, 0.4).save(OUT / "blocker.png")
    hue_shift(runner, 80, 1.2, 1.0).save(OUT / "jumper.png")
    recolor_mul(thug, 0.45, 0.45, 0.5).save(OUT / "dodger.png")

    # Mini-boss / boss tints
    recolor_mul(brute, 1.3, 0.5, 0.4).save(OUT / "miniboss-heavy.png")
    hue_shift(runner, 160, 1.1, 0.9).save(OUT / "miniboss-assassin.png")
    recolor_mul(brute, 0.4, 0.35, 0.55).save(OUT / "boss-warden.png")
    hue_shift(thug, -80, 1.3, 0.8).save(OUT / "boss-conductor.png")
    recolor_mul(runner, 1.4, 0.6, 0.3).save(OUT / "boss-cinder.png")
    recolor_mul(brute, 0.5, 0.7, 1.2).save(OUT / "boss-harbor.png")
    hue_shift(runner, 200, 0.8, 1.1).save(OUT / "boss-mannequin.png")
    recolor_mul(thug, 0.55, 0.8, 0.55).save(OUT / "boss-hollow.png")
    recolor_mul(brute, 1.2, 1.1, 0.4).save(OUT / "boss-crown.png")
    recolor_mul(brute, 0.35, 0.2, 0.45).save(OUT / "boss-helix.png")
    hue_shift(runner, 300, 1.4, 0.7).save(OUT / "boss-secret.png")

    # Portraits
    portrait_from(SRC / "kael-idle/idle-1.png", "portrait-kael.png")
    portrait_from(SRC / "vyra-idle/idle-1.png", "portrait-vyra.png")
    portrait_from(SRC / "rutger-idle/idle-1.png", "portrait-rutger.png")
    portrait_from(SRC / "sien-idle/idle-1.png", "portrait-sien.png")

    # Props
    props = [
        draw_barrel(),
        draw_crate(),
        draw_dumpster(),
        draw_phone(),
        draw_sign(),
        draw_vending(),
        draw_table(),
        draw_hydrant(),
    ]
    assemble_sheet(props, 4, 2, 64).save(OUT / "props.png")

    weapons = [
        draw_weapon_pipe(),
        draw_weapon_bat(),
        draw_weapon_knife(),
        draw_weapon_bottle(),
        draw_weapon_chain(),
        draw_weapon_hammer(),
        draw_weapon_katana(),
        draw_food("chicken"),
    ]
    assemble_sheet(weapons, 4, 2, 64).save(OUT / "weapons.png")

    draw_food("chicken").save(OUT / "item-chicken.png")
    draw_food("soda").save(OUT / "item-soda.png")
    draw_food("pizza").save(OUT / "item-pizza.png")
    draw_food("apple").save(OUT / "item-apple.png")
    draw_impact_sheet().save(OUT / "impact.png")

    print("packed", len(list(OUT.glob("*.png"))), "sprites")


if __name__ == "__main__":
    main()
