# -*- coding: utf-8 -*-
"""Extract media from FlyingRC manuals into product asset folders."""
import zipfile
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\说明书移植")
ASSETS = ROOT / "docs" / "assets"

# Map: docx path -> (product_slug, useful images only or all)
JOBS = [
    (
        r"C:\Users\Administrator\Desktop\FlyingRC F4Wing Mini MK1 说明书.docx",
        "f4wing-mini",
        # product-relevant images (not the catalog section at the end)
        {
            "word/media/image12.png": "layout-front.png",
            "word/media/image13.png": "layout-back.png",
            "word/media/image14.png": "connector-functions.png",
            "word/media/image15.png": "battery-voltage-pins.png",
            "word/media/image16.png": "hd-vtx-pins.png",
            "word/media/image17.png": "wiring-external-bec-diagram.png",
            "word/media/image18.jpeg": "wiring-external-bec-photo.jpg",
            "word/media/image19.png": "wiring-esc-bec-diagram.png",
            "word/media/image20.jpeg": "wiring-esc-bec-photo.jpg",
            "word/media/image21.jpeg": "wiring-with-75a-esc.jpg",
            "word/media/image22.jpeg": "wiring-with-elrs.jpg",
            "word/media/image23.jpeg": "wiring-with-gps.jpg",
            "word/media/image24.jpeg": "wiring-with-hd-vtx.jpg",
            "word/media/image25.jpeg": "wiring-with-5a-bec.jpg",
            "word/media/image26.jpeg": "wiring-with-sbus.jpg",
            "word/media/image10.jpeg": "product-hero.jpg",
            "word/media/image11.jpeg": "solder-header.jpg",
            "word/media/image27.png": "qq-group-qr.png",
        },
    ),
    (
        r"C:\Users\Administrator\Desktop\FlyingRC AM32 ESC V2.5 说明书.docx",
        "am32-75a-v25",
        {
            "word/media/image12.png": "layout-control-board.png",
            "word/media/image13.png": "layout-power-board.png",
            "word/media/image14.png": "pad-definition.png",
            "word/media/image15.jpeg": "wiring-h7wlite.jpg",
            "word/media/image16.jpeg": "wiring-f4wse-pro.jpg",
            "word/media/image17.jpeg": "wiring-f4wing-mini.jpg",
            "word/media/image18.png": "wiring-am32-programmer.png",
            "word/media/image19.png": "heatsink-step1.png",
            "word/media/image20.png": "heatsink-step2.png",
            "word/media/image21.png": "heatsink-step3.png",
            "word/media/image22.png": "heatsink-step4.png",
            "word/media/image23.png": "heatsink-step5.png",
            "word/media/image24.png": "heatsink-done.png",
            "word/media/image25.png": "cap-bec.png",
            "word/media/image26.png": "cap-power.png",
            "word/media/image27.jpeg": "wiring-power.jpg",
            "word/media/image28.jpeg": "wiring-signal-with-bec.jpg",
            "word/media/image29.jpeg": "wiring-signal-no-bec.jpg",
            "word/media/image30.jpeg": "am32-tools-port.png",
            "word/media/image31.jpeg": "am32-tools-connect.jpg",
            "word/media/image32.png": "am32-flash-page.png",
            "word/media/image33.png": "am32-load-firmware.png",
            "word/media/image34.png": "am32-flash-firmware.png",
            "word/media/image35.png": "am32-crawler-default.png",
            "word/media/image36.jpeg": "am32-params.jpg",
            "word/media/image37.png": "qq-group-qr.png",
            "word/media/image9.png": "product-hero.png",
            "word/media/image10.png": "mos-detail.png",
            "word/media/image11.png": "wired-with-bec.png",
            "word/media/image38.jpeg": "repair-wechat.jpg",
        },
    ),
]


def main():
    for docx_path, slug, mapping in JOBS:
        out_dir = ASSETS / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        z = zipfile.ZipFile(docx_path)
        for src, dest_name in mapping.items():
            if src not in z.namelist():
                print(f"MISSING {src} in {slug}")
                continue
            dest = out_dir / dest_name
            with z.open(src) as f, open(dest, "wb") as o:
                shutil.copyfileobj(f, o)
            print(f"{slug}/{dest_name}  {dest.stat().st_size}")
        print(f"Done {slug}: {len(list(out_dir.iterdir()))} files")


if __name__ == "__main__":
    main()
