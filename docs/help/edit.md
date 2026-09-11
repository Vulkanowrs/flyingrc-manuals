# 管理入口说明

说明书内容源在 GitHub，日常修改有三种方式：

## 1. 在线管理页（推荐给管理员）

打开：**[说明书管理页](../admin/index.html)**

1. 用 GitHub Token 登录（需 `repo` 权限）
2. 左侧选择 `docs/` 下的 Markdown
3. 编辑 → 预览 → **保存并发布**
4. 约 1–2 分钟后 GitHub Pages 自动更新

Token 只保存在本机浏览器，建议使用专用账号、用完可在 GitHub 吊销。

## 2. 每页「编辑此页」

在线说明书每个页面右上角铅笔图标，会跳到 GitHub 网页编辑器，改完 Commit 即可。

## 3. 本地 / Git

```powershell
git pull
# 修改 docs/**
python -m mkdocs serve   # 本地预览
git add -A && git commit -m "docs: ..." && git push
```

---

!!! warning "公共章节请改 shared/"

    改 `docs/shared/**` 会同步所有引用该模块的产品页。  
    产品专属内容只改 `docs/products/<型号>/index.md`。  
    参数数据库在仓库根目录 `data/products.yml`（管理页暂只编辑 docs/ 下 Markdown）。
