#!/usr/bin/env python3
"""Copy Imagine outputs, chroma-process sprite sheets, pack props, emit runtime assets."""
from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path("/workspace")
IMG = ROOT / "artifacts/imagine_images"
SPR = ROOT / "assets/sprites"
MAP = ROOT / "assets/map"
PUB = ROOT / "public/sprites"
PUBMAP = ROOT / "public/maps"
PROC = ROOT / ".grok/skills/generate2dsprite/scripts/generate2dsprite.py"

SHEETS_2X2: dict[str, tuple[str, str, str]] = {
    # name: (uuid, target, mode)
    "kael-idle": ("987b154b-805e-4466-9346-d6ece00cd623", "player", "idle"),
    "kael-walk": ("c9fef290-4689-46f2-b287-d217fb500849", "player", "walk"),
    "kael-attack": ("df55017a-fbfb-499a-a406-10ee9f64de60", "player", "attack"),
    "kael-jump": ("27f91850-f367-4a2a-ba9b-4790f0c4170d", "player", "jump"),
    "kael-hurt": ("3ded3be0-9154-42fc-9ab0-4d5360880760", "player", "hurt"),
    "vyra-idle": ("8f1c1264-be02-45a9-a5f5-9ce2c7346adf", "player", "idle"),
    "vyra-walk": ("80efe265-6382-4735-854e-1346b869e568", "player", "walk"),
    "vyra-attack": ("dece8553-f9f7-41c6-9a70-7cb0bfae6f51", "player", "attack"),
    "vyra-jump": ("db119891-2a85-409e-9328-daaf5a569e63", "player", "jump"),
    "vyra-hurt": ("e0b44c2a-d561-4724-b916-82f7f91e3814", "player", "hurt"),
    "rutger-idle": ("ecaa0b5d-b308-4d5f-ad7d-e4427e35249d", "player", "idle"),
    "rutger-walk": ("7f1ba351-655e-4f2e-a088-9670097d56f5", "player", "walk"),
    "rutger-attack": ("4bda303b-8b04-4326-a40e-886e3757464a", "player", "attack"),
    "rutger-jump": ("63aec1ae-3ca1-4fe5-b4d5-02b3b35a2601", "player", "jump"),
    "rutger-hurt": ("02d06b83-5ed7-4a76-9e59-61031adb1564", "player", "hurt"),
    "sien-idle": ("cee59dd6-709b-4984-b964-94513a61cee1", "player", "idle"),
    "sien-walk": ("14a1d7de-cec9-4adf-b5b3-90ee2404519a", "player", "walk"),
    "sien-attack": ("cd591add-2403-41f2-a8e6-29d4a7a9a1a9", "player", "attack"),
    "sien-jump": ("71866798-8391-49fb-b173-88af4e8721e9", "player", "jump"),
    "sien-hurt": ("90078a6d-d401-41c2-b61c-db3e39912f2b", "player", "hurt"),
    "thug": ("31bfde06-00a3-4d67-a7e6-d89f2af716ec", "npc", "idle"),
    "brute": ("ed12f344-f2f2-4454-833f-7273d4cb76f3", "npc", "idle"),
    "runner": ("e8b56aaa-173c-4638-a465-fd6afa168949", "npc", "idle"),
    "grabber": ("4fd9ea58-12da-49bc-a52b-1ba61aa472a7", "npc", "idle"),
    "shooter": ("8718218f-1301-4cb0-b378-50219313c732", "npc", "idle"),
    "elite": ("cc30b488-5b75-4ad1-92e5-f6dffeac62a5", "npc", "idle"),
    "blocker": ("e8410c17-5728-4f0e-a57e-6e99449c2922", "npc", "idle"),
    "jumper": ("31fff29c-dbf9-4269-9b5b-cbe02b4d69e3", "npc", "idle"),
    "armed": ("7c618242-5d6c-40f8-9c37-9d7900495047", "npc", "idle"),
    "dodger": ("001ad986-8302-4a88-80a1-890d355e7e91", "npc", "idle"),
    "shield": ("be223f13-61c0-4d7e-a27e-af0ab92f9f82", "npc", "idle"),
    "miniboss-heavy": ("b1998cf6-d004-462a-a637-8d7b6a2d12eb", "npc", "idle"),
    "miniboss-assassin": ("7de2e57a-a489-40db-a0c6-1357b4c789ba", "npc", "idle"),
    "boss-warden": ("5b066e74-d833-467d-ab37-293e255adf8b", "creature", "idle"),
    "boss-conductor": ("2b4724ef-9d88-4fcb-bd1c-75c975e06c79", "creature", "idle"),
    "boss-cinder": ("78fb7aea-8983-40b6-99c7-e1c79873e762", "creature", "idle"),
    "boss-helix": ("ba057211-4dce-43af-91b9-684f0df7d51a", "creature", "idle"),
    "boss-harbor": ("1f4fa3ff-8c75-4853-9cea-207ac1d7d59b", "creature", "idle"),
    "boss-mannequin": ("ccdc5936-e1e2-43a8-a42f-a9a8e7a416fc", "creature", "idle"),
    "boss-hollow": ("493b1d75-f569-4d91-879e-20b8f4b96bc0", "creature", "idle"),
    "boss-secret": ("e96740f7-3330-4fb3-a094-ff27458bec4a", "creature", "idle"),
    "boss-crown": ("a28893b3-d394-426b-86d5-589f3d7b4330", "creature", "idle"),
    "impact": ("3d482ef4-c886-48a3-84f3-62a8ebd18fbb", "asset", "impact"),
}

PROPS = {
    "barrel": "2345d929-3245-4e58-834b-35b987caee30",
    "crate": "0d86cdc5-9ca4-4e45-9aae-650bb65f9d7d",
    "dumpster": "2c73e0fe-2539-41b5-89cc-cd899e707c48",
    "phone": "ef87282c-3ac2-4862-9c2e-94abb2fe737a",
    "sign": "0195fa25-3bf6-4f27-8323-275398af9daf",
    "vending": "5332da8f-d7eb-4fb9-aa37-bb2565b5ef16",
    "table": "e426cc7f-5149-4307-ba36-c814206d551e",
    "hydrant": "b3811659-4bbf-42cc-a4b4-a63dee6a9f9d",
}

BACKGROUNDS = {
    "bg-urban-far.jpg": "b0ef2842-2659-4efc-aa04-b36fedac3f00",
    "bg-metro-far.jpg": "1049edf9-68fe-4e43-8e6a-fdfb501efd5a",
    "bg-factory-far.jpg": "aa89da31-4de8-4c65-8754-a08e16a1d194",
    "bg-docks-far.jpg": "0b387a67-0e7a-4430-b5a1-f6d61b5c3df5",
    "bg-roofs-far.jpg": "7d2b1382-4c49-469f-84c1-3c66aa99785d",
    "bg-mall-far.jpg": "57f3f4e9-640b-456a-b8d0-ce497bd1b13d",
    "bg-hollow-far.jpg": "267012ca-b9a0-41d6-b219-57333974e34c",
    "bg-helix-far.jpg": "e5429e87-8c44-4559-b55f-ab498fbc9494",
    "bg-urban-mid.jpg": "e6d498d3-7f4b-41f7-968c-f2b139a1b2b0",
    "bg-metro-mid.jpg": "843cc097-82a5-4580-857f-4b51051c35c3",
    "bg-factory-mid.jpg": "200033a9-f4bc-4341-a8a3-21f66d075f69",
    "bg-docks-mid.jpg": "b5e23aa8-e0e5-4bc2-b478-5ac299c12fea",
}

FLOORS = {
    "floor-urban.png": "0121012b-fa97-4988-8370-afe7c322acd0",
    "floor-metro.png": "eeafd6e0-fe4e-4f9f-ac02-979f3a8c32b6",
    "floor-factory.png": "09647a44-bc90-480a-a524-591abd826ffc",
    "floor-docks.png": "518b2496-0ba5-4d94-947b-53da1e587dd9",
    "floor-roofs.png": "866fd13f-deb4-4c91-8ab4-10da47644faa",
    "floor-mall.png": "cfd58d8a-bcbf-4145-91c1-dc71cebaa07e",
}

PORTRAITS = {
    "portrait-kael.png": "ad9ec07e-8af2-4bbd-9d78-448b420eec95",
    "portrait-vyra.png": "122e9a13-e4bd-4e1f-ac82-2acea31f01d7",
    "portrait-rutger.png": "3b8eb37c-b52a-415a-9efe-d1970d44131b",
    "portrait-sien.png": "e1f93d44-ae07-4512-aedc-1e35a0110c5c",
}

ITEMS = "c1f40130-726d-47d5-bdf6-7363b865e013"
WEAPONS = "c30083ad-0d96-4a62-b2ef-77fb719f66f6"


def mag_key(im: Image.Image, t=55) -> Image.Image:
    arr = np.array(im.convert("RGBA"))
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mag = ((r > 180) & (b > 180) & (g < 90)) | ((np.abs(r.astype(int) - 255) < t) & (np.abs(b.astype(int) - 255) < t) & (g < 140))
    arr[mag, 3] = 0
    return Image.fromarray(arr)


def crop_subject(im: Image.Image, pad=8) -> Image.Image:
    im = mag_key(im)
    bbox = im.getbbox()
    if not bbox:
        return im
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad)
    y1 = min(im.height, y1 + pad)
    return im.crop((x0, y0, x1, y1))


def fit_cell(im: Image.Image, size: int, anchor="feet") -> Image.Image:
    cell = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    src = crop_subject(im)
    if src.width == 0 or src.height == 0:
        return cell
    scale = min((size * 0.82) / src.width, (size * 0.86) / src.height)
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    src = src.resize((nw, nh), Image.NEAREST)
    x = (size - nw) // 2
    y = size - nh - int(size * 0.06) if anchor == "feet" else (size - nh) // 2
    cell.paste(src, (x, y), src)
    return cell


def find_src(uuid: str) -> Path:
    p = IMG / f"{uuid}.jpg"
    if p.exists():
        return p
    p = IMG / f"{uuid}.png"
    if p.exists():
        return p
    raise FileNotFoundError(uuid)


def process_grid(name: str, uuid: str, target: str, mode: str) -> Path | None:
    out = SPR / name
    out.mkdir(parents=True, exist_ok=True)
    src = find_src(uuid)
    raw = out / "raw-sheet.png"
    Image.open(src).convert("RGB").save(raw)
    im = mag_key(Image.open(src))
    w, h = im.size
    cw, ch = w // 2, h // 2
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for i in range(4):
        col, row = i % 2, i // 2
        cell = im.crop((col * cw, row * ch, (col + 1) * cw, (row + 1) * ch))
        fitted = fit_cell(cell, 128)
        canvas.paste(fitted, (col * 128, row * 128), fitted)
    sheet = out / "sheet-transparent.png"
    canvas.save(sheet)
    dest = PUB / f"{name}.png"
    shutil.copy2(sheet, dest)
    print("OK", name, dest.stat().st_size)
    return dest


def process_prop(name: str, uuid: str) -> Image.Image:
    im = mag_key(Image.open(find_src(uuid)))
    return fit_cell(im, 128, "feet")


def pack_props():
    order = ["barrel", "crate", "dumpster", "phone", "sign", "vending", "table", "hydrant"]
    atlas = Image.new("RGBA", (512, 256), (0, 0, 0, 0))
    for i, name in enumerate(order):
        cell = process_prop(name, PROPS[name])
        cell.save(PUB / f"prop-{name}.png")
        col, row = i % 4, i // 4
        atlas.paste(cell, (col * 128, row * 128), cell)
    atlas_small = atlas.resize((256, 128), Image.NEAREST)
    atlas_small.save(PUB / "props.png")
    print("OK props atlas")


def pack_items():
    im = mag_key(Image.open(find_src(ITEMS)))
    w, h = im.size
    cw, ch = w // 2, h // 2
    names = ["item-soda", "item-chicken", "item-pizza", "item-apple"]
    for i, name in enumerate(names):
        col, row = i % 2, i // 2
        cell = fit_cell(im.crop((col * cw, row * ch, (col + 1) * cw, (row + 1) * ch)), 48, "center")
        cell.save(PUB / f"{name}.png")
    print("OK items")


def pack_weapons():
    im = mag_key(Image.open(find_src(WEAPONS)))
    w, h = im.size
    cols, rows = 4, 2
    cw, ch = w // cols, h // rows
    atlas = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
    for i in range(8):
        col, row = i % 4, i // 4
        cell = fit_cell(im.crop((col * cw, row * ch, (col + 1) * cw, (row + 1) * ch)), 64, "center")
        atlas.paste(cell, (col * 64, row * 64), cell)
    atlas.save(PUB / "weapons.png")
    print("OK weapons")


def make_portrait(name: str, uuid: str, idle_sheet: Path):
    # Prefer processed idle frame 0 bust crop; fall back to generated portrait.
    try:
        sheet = Image.open(idle_sheet).convert("RGBA")
        cell = sheet.crop((0, 0, sheet.width // 2, sheet.height // 2))
        cell = mag_key(cell)
        bbox = cell.getbbox()
        if bbox:
            x0, y0, x1, y1 = bbox
            h = y1 - y0
            bust = cell.crop((x0, y0, x1, y0 + int(h * 0.48)))
            bust = crop_subject(bust, 4)
            canvas = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
            scale = min(88 / bust.width, 88 / bust.height)
            nw, nh = max(1, int(bust.width * scale)), max(1, int(bust.height * scale))
            bust = bust.resize((nw, nh), Image.NEAREST)
            canvas.paste(bust, ((96 - nw) // 2, 96 - nh - 4), bust)
            canvas.save(PUB / name)
            print("OK", name, "from idle")
            return
    except Exception as e:
        print("portrait idle fail", name, e)
    im = mag_key(Image.open(find_src(uuid)))
    fit_cell(im, 96, "center").save(PUB / name)
    print("OK", name, "from gen")


def copy_bgs():
    PUBMAP.mkdir(parents=True, exist_ok=True)
    for name, uuid in BACKGROUNDS.items():
        src = find_src(uuid)
        dest = PUB / name
        shutil.copy2(src, dest)
        shutil.copy2(src, PUBMAP / name)
        print("OK bg", name)


def make_floors():
    for name, uuid in FLOORS.items():
        im = Image.open(find_src(uuid)).convert("RGB")
        w, h = im.size
        # take lower 38% as the walkable strip, then a 480x40 tile
        y0 = int(h * 0.62)
        strip = im.crop((0, y0, w, h))
        strip = strip.resize((480, 40), Image.NEAREST)
        strip.save(PUB / name)
        print("OK floor", name)


def main():
    PUB.mkdir(parents=True, exist_ok=True)
    SPR.mkdir(parents=True, exist_ok=True)
    fails = []
    for name, (uuid, target, mode) in SHEETS_2X2.items():
        try:
            process_grid(name, uuid, target, mode)
        except Exception as e:
            fails.append((name, str(e)))
            print("ERR", name, e)
    pack_props()
    pack_items()
    pack_weapons()
    copy_bgs()
    make_floors()
    make_portrait("portrait-kael.png", PORTRAITS["portrait-kael.png"], PUB / "kael-idle.png")
    make_portrait("portrait-vyra.png", PORTRAITS["portrait-vyra.png"], PUB / "vyra-idle.png")
    make_portrait("portrait-rutger.png", PORTRAITS["portrait-rutger.png"], PUB / "rutger-idle.png")
    make_portrait("portrait-sien.png", PORTRAITS["portrait-sien.png"], PUB / "sien-idle.png")
    print("FAILS", fails)


if __name__ == "__main__":
    main()
