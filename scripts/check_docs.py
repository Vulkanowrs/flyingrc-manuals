# -*- coding: utf-8 -*-
"""FlyingRC 说明书仓库完整性检查。

检查项：
1. snippets 引用文件是否存在
2. 相对路径图片是否存在
3. products.yml 必填字段
4. 停产/在售状态字段合法
5. 产品页是否存在
退出码非 0 表示有错误，可阻止发布。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data" / "products.yml"

REQUIRED_FIELDS = ["name", "category", "status", "short_code"]
VALID_STATUS = {"active", "eol", "discontinued"}

SNIPPET_RE = re.compile(r"--8<--\s+\"([^\"]+\.md)\"")
IMG_MD_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_HTML_RE = re.compile(r"src=\"([^\"]+)\"")


def load_yaml_simple(path: Path) -> dict:
    """Minimal YAML subset loader for products.yml (no nested custom tags)."""
    try:
        import yaml  # type: ignore
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # fallback: very small parser for our flat-ish structure
        data: dict = {}
        current = None
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            if not line.startswith(" ") and line.endswith(":"):
                current = line[:-1].strip()
                data[current] = {}
            elif current and line.startswith("  ") and ":" in line:
                k, _, v = line.strip().partition(":")
                v = v.strip().strip('"').strip("'")
                if v in ("true", "false"):
                    data[current][k] = v == "true"
                else:
                    data[current][k] = v
        return data


def check_snippets_and_images() -> list[str]:
    errors = []
    for md in DOCS.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(DOCS)
        for m in SNIPPET_RE.finditer(text):
            target = DOCS / m.group(1)
            if not target.is_file():
                errors.append(f"[snippet] {rel} -> missing {m.group(1)}")
        for m in IMG_MD_RE.finditer(text):
            src = m.group(1).split()[0].strip("\"'")
            if src.startswith(("http://", "https://", "data:")):
                continue
            # resolve relative to md file
            target = (md.parent / src).resolve()
            if not target.is_file():
                errors.append(f"[image] {rel} -> missing {src}")
        for m in IMG_HTML_RE.finditer(text):
            src = m.group(1)
            if src.startswith(("http://", "https://", "data:")):
                continue
            target = (md.parent / src).resolve()
            if not target.is_file():
                errors.append(f"[image-html] {rel} -> missing {src}")
    return errors


def check_products() -> list[str]:
    errors = []
    if not DATA.is_file():
        return [f"missing {DATA}"]
    products = load_yaml_simple(DATA)
    if not products:
        return ["products.yml is empty"]
    for slug, meta in products.items():
        if not isinstance(meta, dict):
            errors.append(f"[product] {slug} is not a mapping")
            continue
        for field in REQUIRED_FIELDS:
            if field not in meta or meta[field] in (None, ""):
                errors.append(f"[product] {slug} missing required field: {field}")
        status = meta.get("status")
        if status is not None and status not in VALID_STATUS:
            errors.append(
                f"[product] {slug} invalid status '{status}', expected one of {sorted(VALID_STATUS)}"
            )
        page = DOCS / "products" / slug / "index.md"
        if not page.is_file():
            errors.append(f"[product] {slug} missing page docs/products/{slug}/index.md")
        short = meta.get("short_code")
        if short:
            # short codes must be unique
            pass
    # unique short_code
    shorts = [p.get("short_code") for p in products.values() if isinstance(p, dict)]
    dup = [s for s in set(shorts) if shorts.count(s) > 1 and s]
    for s in dup:
        errors.append(f"[product] duplicate short_code: {s}")
    return errors


def main() -> int:
    errors = check_snippets_and_images() + check_products()
    if errors:
        print("CHECK FAILED")
        for e in errors:
            print(" -", e)
        print(f"\n{len(errors)} error(s)")
        return 1
    print("CHECK OK")
    print(f" - docs md: {len(list(DOCS.rglob('*.md')))}")
    print(f" - assets: {len(list((DOCS / 'assets').rglob('*')))} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
