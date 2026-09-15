# -*- coding: utf-8 -*-
"""Update products.yml with all generated products."""
from pathlib import Path
import re

ROOT = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\说明书移植")
BATCH = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\.mimo-sessions\2026-09-10\extract_out\batch")

# slug, name, category, short, status
ROWS = [
    ("h7d-pro", "FlyingRC® H7D Pro", "flight-controller", "h7dpro", "active"),
    ("f4d-mk1", "FlyingRC® F4D MK1", "flight-controller", "f4d", "active"),
    ("f4wse-mk15", "FlyingRC® F4WSE MK1.5", "flight-controller", "f4wsem", "active"),
    ("f435wing-osd", "FlyingRC® F435Wing Mini OSD", "flight-controller", "f435osd", "active"),
    ("esc-4in1-45a", "FlyingRC® 4IN1 45A ESC", "esc", "45a", "active"),
    ("esc-dual-40a", "FlyingRC® AM32 Dual 40A", "esc", "dual40", "active"),
    ("esc-75a-can", "FlyingRC® AM32 75A CAN", "esc", "75acan", "active"),
    ("esc-control-board", "FlyingRC® AM32 电调控制板", "esc", "escboard", "active"),
    ("am32-programmer", "FlyingRC® AM32 调参器", "accessory", "prog", "active"),
    ("bec-10a-12s", "FlyingRC® 10A 12S BEC", "bec", "bec1012", "active"),
    ("bec-10a-8s", "FlyingRC® 10A 8S BEC", "bec", "bec108", "active"),
    ("bec-5a-12s", "FlyingRC® 5A 12S BEC", "bec", "bec512", "active"),
    ("bec-5a-6s", "FlyingRC® 5A 6S BEC", "bec", "bec56", "active"),
    ("bec-dji-o4", "FlyingRC® Mini BEC For DJI O4", "bec", "becdji", "active"),
    ("elrs-24g", "FlyingRC® ELRS 2.4G 真分集", "receiver", "elrs", "active"),
    ("gps-m10", "FlyingRC® U-Blox M10 GPS", "gps", "m10", "active"),
    ("airspeed-i2c", "FlyingRC® I2C 空速计（新款）", "module", "asnew", "active"),
    ("airspeed-old", "FlyingRC® 无空速管空速计", "module", "asold", "discontinued"),
    ("i2c-current", "FlyingRC® I2C 外置电流计", "module", "i2ccur", "active"),
    ("rm3100-spi", "FlyingRC® RM3100 SPI 罗盘", "module", "rm3100", "active"),
    ("rm3100-can", "FlyingRC® L4CAN RM3100", "module", "rm3100can", "active"),
    ("telemetry", "FlyingRC® 数传模块", "module", "telem", "active"),
    ("pdb-12s-440a", "FlyingRC® 12S 440A 分电板", "power", "pdb", "active"),
    ("l4-can-adapter", "FlyingRC® L4 CAN 扩展板", "module", "l4can", "active"),
]


def main():
    # keep existing 3 products, append new ones
    existing = (ROOT / "data" / "products.yml").read_text(encoding="utf-8")
    blocks = []
    for slug, name, cat, short, status in ROWS:
        if f"{slug}:" in existing:
            continue
        blocks.append(
            f"""
{slug}:
  name: "{name}"
  category: {cat}
  status: {status}
  short_code: {short}
  manual_url: /manual/{slug}/
  firmware_url: /downloads/{slug}/
  migrated_from: WPS docx
"""
        )
    if blocks:
        (ROOT / "data" / "products.yml").write_text(
            existing.rstrip() + "\n" + "".join(blocks), encoding="utf-8"
        )
    print("added", len(blocks), "products")

    # update mkdocs nav
    nav_path = ROOT / "mkdocs.yml"
    nav = nav_path.read_text(encoding="utf-8")
    # replace product nav section between "产品说明书:" and "公共说明:"
    start = nav.find("  - 产品说明书:")
    end = nav.find("  - 公共说明:")
    if start < 0 or end < 0:
        print("NAV_SECTION_NOT_FOUND")
        return
    fc = []
    esc = []
    other = []
    for slug, name, cat, short, status in ROWS:
        # include existing 3 too
        line = f"          - {name}: products/{slug}/index.md\n"
        if cat == "flight-controller":
            fc.append(line)
        elif cat == "esc":
            esc.append(line)
        else:
            other.append((cat, name, slug))
    # existing three
    fc.insert(0, "          - F4WSE PRO: products/f4wse-pro/index.md\n")
    fc.insert(1, "          - F4Wing Mini MK1: products/f4wing-mini/index.md\n")
    esc.insert(0, "          - AM32 75A ESC V2.5: products/am32-75a-v25/index.md\n")

    # group others
    groups = {}
    for cat, name, slug in other:
        groups.setdefault(cat, []).append(f"          - {name}: products/{slug}/index.md\n")
    cat_names = {
        "bec": "BEC",
        "module": "模块与外设",
        "gps": "GPS",
        "receiver": "接收机",
        "power": "分电板",
        "accessory": "工具配件",
    }
    other_block = []
    for cat in ["bec", "module", "gps", "receiver", "power", "accessory"]:
        if cat in groups:
            other_block.append(f"      - {cat_names.get(cat, cat)}:\n")
            other_block.extend(groups[cat])

    new_nav = (
        nav[:start]
        + "  - 产品说明书:\n"
        + "      - 飞控:\n"
        + "".join(fc)
        + "      - 电调:\n"
        + "".join(esc)
        + "".join(other_block)
        + nav[end:]
    )
    nav_path.write_text(new_nav, encoding="utf-8")
    print("nav updated")


if __name__ == "__main__":
    main()
