# -*- coding: utf-8 -*-
import zipfile
from pathlib import Path
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
BATCH = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\.mimo-sessions\2026-09-10\extract_out\batch")
BATCH.mkdir(parents=True, exist_ok=True)

FILES = [
    (
        r"C:\Users\Administrator\Desktop\中转站\FlyingRC® H7Wlite H743 MK2控固定翼飞控产品手册.docx",
        "h7wlite-mk2",
    ),
    (
        r"C:\Users\Administrator\Desktop\中转站\FlyingRC 4IN1 75A ESC 金封四合一电调产品说明书.docx",
        "esc-4in1-75a",
    ),
    (
        r"C:\Users\Administrator\Desktop\中转站\FlyingRC Mini ESC 40A V1.0 说明书.docx",
        "esc-mini-40a",
    ),
]


def extract(path):
    z = zipfile.ZipFile(path)
    doc = etree.fromstring(z.read("word/document.xml"))
    rels = etree.fromstring(z.read("word/_rels/document.xml.rels"))
    rid = {r.get("Id"): r.get("Target") for r in rels}
    lines = []
    for el in doc.iter():
        if not isinstance(el.tag, str) or etree.QName(el).localname != "p":
            continue
        text = "".join(t.text or "" for t in el.findall(".//w:t", NS)).strip()
        imgs = []
        for d in el.findall(".//a:blip", NS):
            target = rid.get(d.get(RID), "?")
            imgs.append("[IMG:%s]" % target)
        if text or imgs:
            suffix = (" " + " ".join(imgs)) if imgs else ""
            lines.append(text + suffix)
    media = [n for n in z.namelist() if n.startswith("word/media/")]
    return lines, media


def main():
    for path, slug in FILES:
        lines, media = extract(path)
        out = BATCH / ("%s.txt" % slug)
        with open(out, "w", encoding="utf-8") as f:
            f.write("# SOURCE: %s\n# SLUG: %s\n# MEDIA: %s\n\n" % (Path(path).name, slug, len(media)))
            for i, line in enumerate(lines):
                f.write("%04d| %s\n" % (i, line))
        print(slug, "paras", len(lines), "media", len(media))


if __name__ == "__main__":
    main()
