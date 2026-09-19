#!/usr/bin/env python3
"""Resize, quantize and recompress Last Ward runtime images in public/."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

PUB = Path("/workspace/public")
SPR = PUB / "sprites"
ART = PUB / "art"

BG_SIZE = (960, 256)  # 2x the 480x128 plate draw
TITLE_SIZE = (960, 540)


def quantize_rgba(im: Image.Image, colors: int = 64) -> Image.Image:
    im = im.convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = Image.fromarray(arr[:, :, :3], "RGB")
    pal = rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    out = np.array(pal.convert("RGBA"))
    out[:, :, 3] = alpha
    out[alpha < 16] = (0, 0, 0, 0)
    return Image.fromarray(out)


def save_png(im: Image.Image, dest: Path, colors: int = 64) -> None:
    q = quantize_rgba(im, colors)
    q.save(dest, format="PNG", optimize=True, compress_level=9)


def save_jpg(im: Image.Image, dest: Path, quality: int = 76, size=None) -> None:
    rgb = im.convert("RGB")
    if size:
        rgb = rgb.resize(size, Image.Resampling.LANCZOS)
    rgb.save(dest, format="JPEG", quality=quality, optimize=True, progressive=True, subsampling=2)


def crop_horizon(im: Image.Image, top=0.18, bot=0.82) -> Image.Image:
    w, h = im.size
    y0, y1 = int(h * top), int(h * bot)
    return im.crop((0, y0, w, y1))


def optimize_backgrounds() -> None:
    for p in sorted(SPR.glob("bg-*.jpg")):
        im = Image.open(p)
        band = crop_horizon(im, 0.12, 0.88) if "far" in p.name else crop_horizon(im, 0.22, 0.92)
        save_jpg(band, p, quality=76, size=BG_SIZE)
        print(f"bg {p.name:24} {p.stat().st_size:7d}")


def optimize_title() -> None:
    p = ART / "title-street.jpg"
    if p.exists():
        save_jpg(Image.open(p), p, quality=78, size=TITLE_SIZE)
        print(f"title {p.stat().st_size}")


def optimize_floors() -> None:
    for p in sorted(SPR.glob("floor-*.png")):
        im = Image.open(p).convert("RGB").resize((480, 36), Image.Resampling.NEAREST)
        dest = p.with_suffix(".jpg")
        save_jpg(im, dest, quality=80, size=(480, 36))
        p.unlink()
        print(f"floor {dest.name:24} {dest.stat().st_size:7d}")


def optimize_sprites() -> None:
    skip_prefix = ("bg-",)
    for p in sorted(SPR.glob("*.png")):
        if p.name.startswith(skip_prefix):
            continue
        im = Image.open(p)
        colors = 96 if p.name.startswith("boss-") or p.name.startswith("rutger") else 64
        if p.name.startswith("item-") or p.name.startswith("prop-"):
            colors = 48
        if p.name in {"impact.png", "weapons.png", "props.png"}:
            colors = 80
        save_png(im, p, colors=colors)
        print(f"png {p.name:28} {p.stat().st_size:7d}")


def optimize_share() -> None:
    og = PUB / "og.jpg"
    if og.exists():
        im = Image.open(og)
        save_jpg(im, og, quality=82, size=im.size)
        print(f"og {og.stat().st_size}")


def main() -> None:
    optimize_backgrounds()
    optimize_title()
    optimize_floors()
    optimize_sprites()
    optimize_share()
    maps = PUB / "maps"
    if maps.exists():
        import shutil
        shutil.rmtree(maps)
        print("removed public/maps")


if __name__ == "__main__":
    main()
