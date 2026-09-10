# -*- coding: utf-8 -*-
"""Extract F4WSE PRO product-relevant images."""
import zipfile
import shutil
from pathlib import Path

DOCX = r"C:\Users\Administrator\Desktop\FlyingRC® F4WSE PRO 飞控产品手册.docx"
OUT = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\说明书移植\docs\assets\f4wse-pro")
OUT.mkdir(parents=True, exist_ok=True)

MAPPING = {
    "word/media/image8.jpeg": "product-hero.jpg",
    "word/media/image9.jpeg": "layout-front.jpg",
    "word/media/image10.jpeg": "layout-back.jpg",
    "word/media/image11.jpeg": "connector-functions.jpg",
    "word/media/image12.jpeg": "usb-board-wiring.jpg",
    "word/media/image13.png": "usb-board-pinout.png",
    "word/media/image14.jpeg": "tf-board-wiring.jpg",
    "word/media/image15.jpeg": "tf-board-connection.jpg",
    "word/media/image16.png": "mission-planner-target.png",
    "word/media/image17.jpeg": "wiring-full-example.jpg",
    "word/media/image18.png": "esc-v32-v40-socket.png",
    "word/media/image19.jpeg": "esc-version-marks.jpg",
    "word/media/image20.jpeg": "wiring-full-alt.jpg",
    "word/media/image21.jpeg": "wiring-elrs.jpg",
    "word/media/image22.jpeg": "wiring-sbus.jpg",
    "word/media/image23.jpeg": "wiring-gps.jpg",
    "word/media/image24.png": "wiring-analog-camera.png",
    "word/media/image25.jpeg": "wiring-4in1-v32.jpg",
    "word/media/image26.jpeg": "wiring-4in1-v40.jpg",
    "word/media/image27.jpeg": "wiring-hd-vtx-sbus.jpg",
    "word/media/image28.png": "wiring-o4-bec.png",
    "word/media/image29.jpeg": "wiring-40a-esc.jpg",
    "word/media/image30.jpeg": "wiring-75a-esc.jpg",
    "word/media/image31.jpeg": "wiring-dual-esc.jpg",
    "word/media/image32.png": "packing-list.png",
    "word/media/image33.png": "qq-group-qr.png",
    "word/media/image34.jpeg": "repair-wechat.jpg",
}


def main():
    z = zipfile.ZipFile(DOCX)
    for src, dest in MAPPING.items():
        if src not in z.namelist():
            print("MISSING", src)
            continue
        with z.open(src) as f, open(OUT / dest, "wb") as o:
            shutil.copyfileobj(f, o)
        print(dest, (OUT / dest).stat().st_size)
    print("count", len(list(OUT.iterdir())))


if __name__ == "__main__":
    main()
