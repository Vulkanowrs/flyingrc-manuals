# -*- coding: utf-8 -*-
"""Extract product-catalog images from F4WSE PRO manual."""
import zipfile
import shutil
from pathlib import Path

DOCX = r"C:\Users\Administrator\Desktop\FlyingRC® F4WSE PRO 飞控产品手册.docx"
OUT = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\说明书移植\docs\assets\catalog")
OUT.mkdir(parents=True, exist_ok=True)

MAPPING = {
    # category banners / product thumbs from 其它产品介绍
    "word/media/image35.png": "fc-f4wse.png",
    "word/media/image36.png": "fc-f4wse-eol.png",
    "word/media/image37.png": "fc-h7wlite.png",
    "word/media/image38.png": "fc-f4wing-mini.png",
    "word/media/image39.png": "fc-f4wing-mini-pro.png",
    "word/media/image40.png": "fc-h7d-pro.png",
    "word/media/image41.png": "fc-h7d-mk1.png",
    "word/media/image42.png": "fc-f4d-mk1.png",
    "word/media/image44.png": "esc-4in1-75a.png",
    "word/media/image45.png": "esc-4in1-45a.png",
    "word/media/image46.png": "esc-am32-dual-40a.png",
    "word/media/image47.png": "esc-am32-75a.png",
    "word/media/image48.png": "esc-am32-75a-can.png",
    "word/media/image49.jpeg": "esc-am32-control.jpg",
    "word/media/image50.png": "esc-am32-mini-40a.png",
    "word/media/image52.png": "stack-premium.png",
    "word/media/image53.png": "stack-adv-f405-75a.png",
    "word/media/image54.jpeg": "stack-adv-h743-45a.jpg",
    "word/media/image55.jpeg": "stack-basic.jpg",
    "word/media/image56.png": "stack-fixed-wing.png",
    "word/media/image58.png": "bec-10a-12s.png",
    "word/media/image59.png": "bec-5a-12s.png",
    "word/media/image60.png": "bec-10a-8s.png",
    "word/media/image61.png": "bec-5a-6s.png",
    "word/media/image62.png": "bec-dji-o4.png",
    "word/media/image63.png": "mod-rm3100-spi.png",
    "word/media/image64.png": "mod-rm3100-can.png",
    "word/media/image65.png": "mod-telemetry.png",
    "word/media/image66.png": "mod-i2c-current.png",
    "word/media/image68.png": "other-pdb.png",
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
