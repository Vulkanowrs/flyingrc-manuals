# FlyingRC 批量化说明书系统

统一 Markdown 内容源 → 自动生成在线说明书与 PDF。

## 内容口径源（重要）

**所有说明书公共内容不一致处，一律以《FlyingRC® F4WSE PRO 飞控产品手册》为准。**

- 本地源文件：`C:\Users\Administrator\Desktop\FlyingRC® F4WSE PRO 飞控产品手册.docx`
- 手册标注更新日期：**2026-08-15**
- 云文档（WPS）：https://www.kdocs.cn/l/cm7xI59wJgrf （请以你们团队当前最新云文档为准；本仓库公共章节已按上述 2026-08-15 导出稿对齐）

公共章节更新入口：`docs/shared/**`（售后、支持、品牌、固件下载、安全等）。

## 目录结构

```text
docs/
  shared/           公共章节（售后、安全、支持…）
  shared/<series>/  系列通用（飞控/电调/CAN…）
  products/<slug>/  产品专属说明
  assets/<slug>/    产品图片
data/products.yml   产品参数数据库
scripts/
  check_docs.py     完整性检查（CI 会跑）
  extract_*.py      从 WPS 说明书抽图
mkdocs.yml
```

## 本地运行

```powershell
pip install -r requirements.txt
python scripts/check_docs.py
python -m mkdocs serve
```

浏览器打开 <http://127.0.0.1:8000>。

## 构建发布

```powershell
python -m mkdocs build --strict
```

产物在 `site/`。GitHub Actions：`.github/workflows/check.yml`、`deploy.yml`。

## 发布目标（两阶段）

| 阶段 | 站点 | 说明 |
|------|------|------|
| 现在 | `https://vulkanowrs.github.io/flyingrc-manuals/` | 公开仓库 GitHub Pages，长期免费 |
| 以后 | `www.flyingrc.cn`（如 `manual.flyingrc.cn`） | 迁到自有服务器/官网，仓库与内容源不变 |

迁到官网时只需：

1. 改 `mkdocs.yml` 的 `site_url` 为正式域名  
2. 增加一条部署任务（推到你们 Nginx/OSS/静态目录，或自建 Runner）  
3. 包装短链仍用 `flyingrc.cn/m/<short_code>`，指向正式说明书路径  

`data/products.yml` 里的 `short_code`（`f4wse` / `f4wing` / `75a`）可直接作短链后缀。

## 新增产品

1. 在 `data/products.yml` 增加型号与参数（`name` / `category` / `status` / `short_code` 必填）。
2. 新建 `docs/products/<slug>/index.md`，图片放 `docs/assets/<slug>/`。
3. 公共章节用 snippets 引用，例如：

   ```markdown
   --8<-- "shared/warranty.md"
   --8<-- "shared/esc/am32-setup.md"
   ```

4. 更新 `mkdocs.yml` 的 `nav`。
5. 运行 `python scripts/check_docs.py`。

## 修改公共内容

只改 `docs/shared/**` 下对应文件，所有引用该章节的产品页会自动同步。  
**改之前请对照 F4WSE PRO 口径源；若口径源有更新，先同步公共章节再迁产品。**

## 当前已迁移

| 产品 | 页面 | 状态 |
|------|------|------|
| F4WSE PRO | `docs/products/f4wse-pro/` | 完成（口径源） |
| F4Wing Mini MK1 | `docs/products/f4wing-mini/` | 完成 |
| AM32 75A ESC V2.5 | `docs/products/am32-75a-v25/` | 完成 |

## 待确认

- 包装短链：`flyingrc.cn/m/f4wse`、`f4wing`、`75a` 是否采用  
- 云文档与本地导出稿是否一致（如云文档已再改，请导出最新 docx 再对齐一次）  
- 迁到 `www.flyingrc.cn` 的时间与服务器/域名绑定方式  
- PDF 导出工作流（暂不需要）  

