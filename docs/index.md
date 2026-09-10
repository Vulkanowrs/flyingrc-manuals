# FlyingRC® 产品说明书中心

统一内容源 · 模块化公共章节 · 产品参数数据化 · 在线阅读

## 快速入口

| 产品 | 类别 | 状态 | 说明书 |
|------|------|------|--------|
| F4WSE PRO | 固定翼飞控 | 在售 | [阅读](products/f4wse-pro/index.md) |
| F4Wing Mini MK1 | 固定翼飞控 | 在售 | [阅读](products/f4wing-mini/index.md) |
| AM32 75A ESC V2.5 | 单体电调 | 在售 | [阅读](products/am32-75a-v25/index.md) |

更多型号见 [产品总目录](catalog.md)（飞控 / 电调 / 飞塔 / BEC / 模块 / 外设）。

!!! info "公共内容口径"

    售后、支持、品牌等公共章节以 **F4WSE PRO 手册（2026-08-15）** 为唯一口径源。其它产品说明书与之不一致处，一律以该手册为准。

## 本系统如何工作

```text
公共说明模块 + 系列通用 + 产品专属 + 参数数据库
                ↓
        自动拼装与校验
                ↓
     官网在线说明书 + PDF
                ↓
        包装二维码永久访问
```

- **改一次公共章节**（如保修政策），所有引用该章节的产品说明书同步更新。
- **产品参数**集中在 `data/products.yml`，避免官网 / 说明书 / 下载页三处不一致。
- **硬件版本**按版本冻结传感器、接口、尺寸等内容；售后与联系方式可全局同步。

## 公共章节

- [安全注意事项](shared/safety.md)
- [首次使用检查](shared/first-use-check.md)
- [焊接注意事项](shared/soldering.md)
- [售后与保修](shared/warranty.md)
- [技术支持](shared/support.md)
- [固件下载说明](shared/firmware-download.md)
- [常见问题](shared/faq.md)

## 维护说明（内部）

1. 公共内容放在 `docs/shared/`，产品页用 snippets 语法引用相对路径下的 .md，不要复制粘贴正文。
2. 新增产品：在 `data/products.yml` 加参数 → 建 `docs/products/<slug>/index.md` → 放图片到 `docs/assets/<slug>/` → 更新 `mkdocs.yml` nav。
3. 提交前运行 `python scripts/check_docs.py`。
