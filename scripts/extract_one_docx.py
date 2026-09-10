# -*- coding: utf-8 -*-
"""Extract paragraphs and media list from a single manual."""
import zipfile
import sys
from pathlib import Path
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"


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
    media = {n: z.getinfo(n).file_size for n in z.namelist() if n.startswith("word/media/")}
    return lines, media


def main():
    path = sys.argv[1]
    out = Path(sys.argv[2])
    lines, media = extract_docx(path)
    with open(out, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
            f.write(f"{i:04d}| {line}\n")
        f.write("\n--- MEDIA ---\n")
        for m, sz in media.items():
            f.write(f"{m}\t{sz}\n")
    print(f"Wrote {out} paragraphs={len(lines)} media={len(media)}")


if __name__ == "__main__":
    main()
