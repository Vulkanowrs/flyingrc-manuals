# -*- coding: utf-8 -*-
"""Generate MkDocs product pages from extracted manuals."""
from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\说明书移植")
BATCH = Path(r"C:\Users\Administrator\XiaomiMiMoProjects\.mimo-sessions\2026-09-10\extract_out\batch")
SRC = Path(r"C:\Users\Administrator\Desktop\中转站")

# slug -> (category, display_name, short_code, status, extra_meta)
PRODUCTS = {
    "h7d-pro": ("flight-controller", "FlyingRC® H7D Pro", "h7dpro", "active"),
    "f4d-mk1": ("flight-controller", "FlyingRC® F4D MK1", "f4d", "active"),
    "f4wse-mk15": ("flight-controller", "FlyingRC® F4WSE MK1.5", "f4wsem", "active"),
    "f435wing-osd": ("flight-controller", "FlyingRC® F435Wing Mini OSD", "f435osd", "active"),
    "h7wlite-mk2": ("flight-controller", "FlyingRC® H7Wlite MK2", "h7wlite", "active"),
    "esc-4in1-45a": ("esc", "FlyingRC® 4IN1 45A ESC", "45a", "active"),
    "esc-4in1-75a": ("esc", "FlyingRC® 4IN1 75A ESC", "4in175", "active"),
    "esc-mini-40a": ("esc", "FlyingRC® AM32 Mini 40A", "mini40", "active"),
    "esc-dual-40a": ("esc", "FlyingRC® AM32 Dual 40A", "dual40", "active"),
    "esc-75a-can": ("esc", "FlyingRC® AM32 75A CAN", "75acan", "active"),
    "esc-control-board": ("esc", "FlyingRC® AM32 电调控制板", "escboard", "active"),
    "am32-programmer": ("accessory", "FlyingRC® AM32 调参器", "prog", "active"),
    "bec-10a-12s": ("bec", "FlyingRC® 10A 12S BEC", "bec1012", "active"),
    "bec-10a-8s": ("bec", "FlyingRC® 10A 8S BEC", "bec108", "active"),
    "bec-5a-12s": ("bec", "FlyingRC® 5A 12S BEC", "bec512", "active"),
    "bec-5a-6s": ("bec", "FlyingRC® 5A 6S BEC", "bec56", "active"),
    "bec-dji-o4": ("bec", "FlyingRC® Mini BEC For DJI O4", "becdji", "active"),
    "elrs-24g": ("receiver", "FlyingRC® ELRS 2.4G 真分集", "elrs", "active"),
    "gps-m10": ("gps", "FlyingRC® U-Blox M10 GPS", "m10", "active"),
    "airspeed-i2c": ("module", "FlyingRC® I2C 空速计（新款）", "asnew", "active"),
    "airspeed-old": ("module", "FlyingRC® 无空速管空速计", "asold", "discontinued"),
    "i2c-current": ("module", "FlyingRC® I2C 外置电流计", "i2ccur", "active"),
    "rm3100-spi": ("module", "FlyingRC® RM3100 SPI 罗盘", "rm3100", "active"),
    "rm3100-can": ("module", "FlyingRC® L4CAN RM3100", "rm3100can", "active"),
    "telemetry": ("module", "FlyingRC® 数传模块", "telem", "active"),
    "pdb-12s-440a": ("power", "FlyingRC® 12S 440A 分电板", "pdb", "active"),
    "l4-can-adapter": ("module", "FlyingRC® L4 CAN 扩展板", "l4can", "active"),
}

# Sections that should become shared snippets
SHARED_MARKERS = [
    (r"一、\s*FlyingRC", "shared/brand-intro.md"),
    (r"^FlyingRC介绍$", "shared/brand-intro.md"),
    (r"技术问题咨询", "shared/support.md"),
    (r"维修服务", "shared/warranty.md"),
    (r"其它产品介绍|其他产品介绍", "shared/other-products.md"),
    (r"免责声明", "shared/disclaimer.md"),
    (r"常见问题", "shared/faq.md"),
]

SKIP_HEADINGS = re.compile(
    r"目\s*录|FlyingRC介绍|产品概述|使用方法|技术问题咨询|维修服务|其它产品|其他产品"
)

CATEGORY_EXTRA_SNIPPETS = {
    "flight-controller": [
        ("USB 驱动与连接", "shared/flight-controller/usb-driver.md"),
        ("接收机连接", "shared/flight-controller/receiver-wiring.md"),
        ("安全须知", "shared/safety.md"),
        ("首次使用检查", "shared/first-use-check.md"),
    ],
    "esc": [
        ("AM32 固件与调参", "shared/esc/am32-setup.md"),
        ("电机转向与协议", "shared/esc/motor-direction.md"),
        ("安全须知", "shared/safety.md"),
        ("焊接注意", "shared/soldering.md"),
        ("首次使用检查", "shared/first-use-check.md"),
    ],
    "bec": [
        ("安全须知", "shared/safety.md"),
        ("焊接注意", "shared/soldering.md"),
        ("首次使用检查", "shared/first-use-check.md"),
    ],
    "module": [
        ("安全须知", "shared/safety.md"),
        ("首次使用检查", "shared/first-use-check.md"),
    ],
    "receiver": [
        ("接收机连接", "shared/flight-controller/receiver-wiring.md"),
        ("安全须知", "shared/safety.md"),
        ("首次使用检查", "shared/first-use-check.md"),
    ],
    "gps": [
        ("安全须知", "shared/safety.md"),
        ("首次使用检查", "shared/first-use-check.md"),
    ],
    "power": [
        ("安全须知", "shared/safety.md"),
        ("焊接注意", "shared/soldering.md"),
        ("首次使用检查", "shared/first-use-check.md"),
    ],
    "accessory": [
        ("安全须知", "shared/safety.md"),
    ],
}


def parse_extract(txt_path: Path):
    title = ""
    lines = []
    for raw in txt_path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("# SOURCE:"):
            continue
        if raw.startswith("# SLUG:"):
            continue
        if raw.startswith("# MEDIA:"):
            continue
        if not raw.strip():
            continue
        m = re.match(r"^\d{4}\|\s?(.*)$", raw)
        if not m:
            continue
        lines.append(m.group(1))
    if lines:
        # skip leading images for title
        for ln in lines:
            if ln.strip() and not ln.strip().startswith("[IMG:"):
                title = re.sub(r"\s+", " ", ln.strip())
                break
    return title, lines


def body_lines(lines):
    """Drop TOC-like early lines; keep content after first real heading."""
    out = []
    started = False
    for ln in lines:
        s = ln.strip()
        if not started:
            if re.match(r"^\[2\]", ln) or re.match(r"^[一二三四五六七八九十]+、", s):
                started = True
            elif "产品概述" in s or "使用方法" in s or "基础参数" in s:
                started = True
            else:
                continue
        # skip pure TOC leftovers
        if re.match(r"^\[\d+\]\s*[一二三四五六七八九十]+、", s) and len(s) < 40 and s[-1].isdigit():
            continue
        if s in ("目  录", "目录"):
            continue
        out.append(ln)
    return out


def strip_shared_text(lines):
    """Remove long shared boilerplate paragraphs; keep product-specific."""
    drop_substrings = [
        "上海玉涵航电智能科技有限公司",
        "累计销售各类电路产品",
        "技术总监刘玉涵",
        "官方QQ群是FlyingRC",
        "群内工程师工作时间",
        "质保期：自购买日起",
        "以旧换新服务",
        "付费维修服务",
        "上海市闵行区",
        "维修收费价格",
        "亲爱的飞友，衷心感谢",
        "别忘了关注FlyingRC",
        "FlyingRC®闲鱼店铺",
        "加入FlyingRC®官方QQ群",
        "公司的代理商遍及",
        "必读：鉴于网上销售平台",
        "几个相关链接贴心附在",
        "官方QQ群和官网是FlyingRC",
        "飞友收到产品后请务必",
        "独特设计和卓越品质",
        "FlyingRC® 产品寻求销售",
        "清华大学、上海交通",
        "2026年8月15日更新",
    ]
    out = []
    for ln in lines:
        s = ln.strip()
        plain = re.sub(r"^\[\d+\]\s*", "", s)
        if any(k in plain for k in drop_substrings):
            continue
        # skip catalog product list headings that are just numbers
        if re.match(r"^产品\d+\.", plain):
            continue
        out.append(ln)
    return out


def line_to_md(ln: str) -> str:
    s = ln.strip()
    if not s:
        return ""
    imgs = re.findall(r"\[IMG:([^\]]+)\]", s)
    text = re.sub(r"\[IMG:[^\]]+\]", "", s).strip()
    text = re.sub(r"^\[\d+\]\s*", "", text)
    parts = []
    if text:
        # headings
        if re.match(r"^[一二三四五六七八九十]+、", text) or text in (
            "产品概述", "使用方法", "基础参数", "技术参数", "产品特点"
        ):
            parts.append("## " + text)
        elif re.match(r"^\d+\.\s*布局|^布局|^LAYOUT", text, re.I):
            parts.append("### " + text)
        elif len(text) < 28 and not text.endswith("。") and not text.endswith("，") and imgs == [] and (
            text.endswith("参数") or text.endswith("方法") or "接线" in text or "布局" in text
            or text.startswith("1.") or text.startswith("2.") or text.startswith("3.")
        ):
            # short heading-ish
            if re.match(r"^\d+\.", text):
                parts.append("**" + text + "**")
            else:
                parts.append("### " + text)
        else:
            parts.append(text)
    for img in imgs:
        # media/imageN.ext -> will be rewritten later with slug prefix
        parts.append(f"![](ASSET::{img})")
    return "\n\n".join(parts) if parts else ""


def extract_assets(docx_path: Path, media_names: list[str], slug: str):
    assets_dir = ROOT / "docs" / "assets" / slug
    assets_dir.mkdir(parents=True, exist_ok=True)
    mapping = {}
    z = zipfile.ZipFile(docx_path)
    names_in_zip = set(z.namelist())
    kept = 0
    for name in media_names:
        candidates = [name]
        if not name.startswith("word/"):
            candidates.append("word/" + name)
        src = None
        for c in candidates:
            if c in names_in_zip:
                src = c
                break
        if not src:
            continue
        info = z.getinfo(src)
        if info.file_size < 8000:
            continue
        ext = Path(src).suffix.lower() or ".jpg"
        dest_name = f"img{kept:02d}{ext}"
        dest = assets_dir / dest_name
        with z.open(src) as f, open(dest, "wb") as o:
            shutil.copyfileobj(f, o)
        rel = f"assets/{slug}/{dest_name}"
        mapping[name] = rel
        if not name.startswith("word/"):
            mapping["word/" + name] = rel
        kept += 1
        if kept >= 80:
            break
    return mapping


def rewrite_assets(md: str, mapping: dict, page_rel: str) -> str:
    # page is docs/products/<slug>/index.md -> ../../assets/<slug>/imgXX
    def repl(m):
        src = m.group(1)
        if src.startswith("ASSET::"):
            key = src[7:]
            if key in mapping:
                return f"![](../../{mapping[key]})"
            return ""
        return m.group(0)

    md = re.sub(r"!\[\]\((ASSET::[^\)]+)\)", repl, md)
    md = re.sub(r"!\[\]\(\)", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md


def build_page(slug: str, category: str, title: str, body_md: str) -> str:
    extras = CATEGORY_EXTRA_SNIPPETS.get(category, [])
    lines = [
        f"# {title}",
        "",
        f"> 状态：在售 · 类别：{category} · 内容自原 WPS 说明书迁入",
        "",
        "---",
        "",
        body_md.strip(),
        "",
        "---",
        "",
    ]
    for h, path in extras:
        lines += [f"## {h}", "", f'--8<-- "{path}"', "", "---", ""]
    lines += [
        "## 技术支持", "",
        '--8<-- "shared/support.md"', "",
        "---", "",
        "## 售后与保修", "",
        '--8<-- "shared/warranty.md"', "",
        "---", "",
        "## FlyingRC® 其它产品", "",
        '--8<-- "shared/other-products.md"', "",
        "---", "",
        "## 免责声明", "",
        '--8<-- "shared/disclaimer.md"', "",
    ]
    return "\n".join(lines) + "\n"


def find_docx(slug: str) -> Path | None:
    # reverse map from SLUGS in batch_extract by re-scan
    for p in SRC.glob("*.docx"):
        if "英文" in p.name:
            continue
        # reuse slug logic roughly
        from scripts_slug import slug_for  # type: ignore
    return None


def main():
    # import slug map from batch_extract
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "batch_extract", ROOT / "scripts" / "batch_extract.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    slug_to_docx = {}
    for p in SRC.glob("*.docx"):
        if any(k in p.name for k in mod.SKIP_EN):
            continue
        slug_to_docx[mod.slug_for(p.name)] = p

    for slug, meta in PRODUCTS.items():
        cat, name, short, status = meta
        txt = BATCH / f"{slug}.txt"
        if not txt.exists():
            print("MISSING_TXT", slug)
            continue
        docx = slug_to_docx.get(slug)
        if not docx:
            print("MISSING_DOCX", slug)
            continue
        title, raw_lines = parse_extract(txt)
        if not title:
            title = name
        lines = body_lines(raw_lines)
        lines = strip_shared_text(lines)
        # collect media names in order
        media_names = []
        for ln in raw_lines:
            media_names += re.findall(r"\[IMG:([^\]]+)\]", ln)
        mapping = extract_assets(docx, media_names, slug)
        md_parts = []
        for ln in lines:
            part = line_to_md(ln)
            if part:
                md_parts.append(part)
        body = join_table_rows(md_parts)
        body = rewrite_assets(body, mapping, slug)
        page = build_page(slug, cat, title if title.startswith("FlyingRC") else (name + " 产品手册"), body)
        out = ROOT / "docs" / "products" / slug / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"PAGE {slug} assets={len(mapping)} md_len={len(page)}")


def join_table_rows(md_parts):
    """Join markdown fragments; keep consecutive table lines as one table (no blank lines)."""
    out = []
    for p in md_parts:
        p = (p or "").strip("\n")
        if not p:
            continue
        if p.startswith("|"):
            if out and out[-1].startswith("|"):
                out[-1] = out[-1] + "\n" + p
            else:
                out.append(p)
        else:
            out.append(p)
    return "\n\n".join(out) + "\n"


if __name__ == "__main__":
    main()
