# -*- coding: utf-8 -*-
"""Batch-extract all manuals from 中转站 into extract_out/batch."""
import zipfile
import re
import sys
from pathlib import Path
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"

SRC = Path(r"C:\Users\Administrator\Desktop\中转站")
OUT = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\.mimo-sessions\2026-09-10\extract_out\batch")
OUT.mkdir(parents=True, exist_ok=True)

# slug map for known files
SLUGS = {
    "FlyingRC  AM32电调调参器产品手册.docx": "am32-programmer",
    "FlyingRC 12S 440A穿越机分电板 说明书.docx": "pdb-12s-440a",
    "FlyingRC 4IN1 45A ESC AM32四合一穿越机电调 说明书.docx": "esc-4in1-45a",
    "FlyingRC AM32 Dual ESC Mini说明书.docx": "esc-dual-40a",
    "FlyingRC ELRS 2.4G 分集接收机说明书.docx": "elrs-24g",
    "FlyingRC F435Wing Mini OSD版 说明书.docx": "f435wing-osd",
    "FlyingRC F4D MK1 F405主控 20,30.5孔距 穿越机飞控.docx": "f4d-mk1",
    "FlyingRC F4WSE MK1.5 说明书.docx": "f4wse-mk15",
    "FlyingRC FlyingRC  10A 12S BEC降压模块说明书.docx": "bec-10a-12s",
    "FlyingRC FlyingRC  10A 8S BEC降压模块说明书.docx": "bec-10a-8s",
    "FlyingRC FlyingRC  5A 12S BEC降压模块说明书.docx": "bec-5a-12s",
    "FlyingRC FlyingRC 5A BEC降压模块说明书.docx": "bec-5a-6s",
    "FlyingRC H7D Pro MK1 说明书.docx": "h7d-pro",
    "FlyingRC L4 CAN RC GPS Adapter CAN总线串口 PWM扩展板说明书.docx": "l4-can-adapter",
    "FlyingRC Mini BEC For DJI O4 降压模块说明书.docx": "bec-dji-o4",
    "FlyingRC U-Blox M10 GPS中文版说明书.docx": "gps-m10",
    "FlyingRC 无空速管数字空速计产品手册.docx": "airspeed-old",
    "FlyingRC® AM32  ESC单体电调控制板产品手册.docx": "esc-control-board",
    "FlyingRC® AM32 ESC 75A CAN总线单体金封电调 .docx": "esc-75a-can",
    "FlyingRC® I2C无空速管数字新款空速计产品手册.docx": "airspeed-i2c",
    "FlyingRC® L4CAN RM3100 CAN总线罗盘模块.docx": "rm3100-can",
    "FlyingRC® RM3100 SPI Module 罗盘模块.docx": "rm3100-spi",
    "FlyingRC® 数传模块.docx": "telemetry",
    "FlyingRC®I2C 外置电流计产品手册.docx": "i2c-current",
}

SKIP_EN = ("英文",)


def extract_docx(path):
    z = zipfile.ZipFile(path)
    doc = etree.fromstring(z.read("word/document.xml"))
    rels = etree.fromstring(z.read("word/_rels/document.xml.rels"))
    rid_to_target = {rel.get("Id"): rel.get("Target") for rel in rels}
    lines = []
    for el in doc.iter():
        if not isinstance(el.tag, str):
            continue
        if etree.QName(el).localname != "p":
            continue
        texts = [t.text or "" for t in el.findall(".//w:t", NS)]
        text = "".join(texts).strip()
        imgs = []
        for d in el.findall(".//a:blip", NS):
            rid = d.get(RID)
            imgs.append(f"[IMG:{rid_to_target.get(rid, '?')}]")
        style = ""
        pPr = el.find("w:pPr", NS)
        if pPr is not None:
            pStyle = pPr.find("w:pStyle", NS)
            if pStyle is not None:
                style = pStyle.get(
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"
                ) or ""
        if text or imgs:
            prefix = f"[{style}] " if style else ""
            lines.append(prefix + text + (" " + " ".join(imgs) if imgs else ""))
    media = [n for n in z.namelist() if n.startswith("word/media/")]
    return lines, media


def slug_for(name):
    if name in SLUGS:
        return SLUGS[name]
    base = name.rsplit(".", 1)[0]
    s = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return s[:40] or "unknown"


def main():
    files = sorted(SRC.glob("*.docx"))
    for p in files:
        if any(k in p.name for k in SKIP_EN):
            print("SKIP_EN", p.name)
            continue
        slug = slug_for(p.name)
        lines, media = extract_docx(p)
        out = OUT / f"{slug}.txt"
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"# SOURCE: {p.name}\n# SLUG: {slug}\n# MEDIA: {len(media)}\n\n")
            for i, line in enumerate(lines):
                f.write(f"{i:04d}| {line}\n")
        print(f"OK {slug} paras={len(lines)} media={len(media)}")


if __name__ == "__main__":
    main()
