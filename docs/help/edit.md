# 如何修改说明书（给运营 / 文案）

不需要会 Git，也不用自己写代码。按下面做即可。

## 方式一：在线编辑页（推荐）

打开：**[说明书编辑](../admin/index.html)**

### 登录（二选一）

**A. 团队密码（推荐，同事都这么进）**

1. 管理员部署过一次 Cloudflare Worker 后，会得到：
   - 管理服务地址（类似 `https://xxx.workers.dev`）
   - 团队密码
2. 打开编辑页 → 选「团队密码」→ 填这两项 → 登录

**B. GitHub Token（仅技术同事）**

1. https://github.com/settings/tokens/new  
2. 勾选 **repo** → 生成 → 复制  
3. 编辑页选「GitHub Token」→ 粘贴 → 登录  

### 日常怎么改

| 步骤 | 操作 |
|------|------|
| 1 | 左侧找文件：`shared/` 是公共章节，`products/` 是某一款说明书 |
| 2 | 中间直接改文字；上方按钮可加粗、标题、表格、提示框 |
| 3 | 右侧可预览效果；图片会按仓库路径显示 |
| 4 | 要插图：点「上传图片」，选文件后自动写入 `docs/assets` |
| 5 | 点 **保存并发布** → 约 1–2 分钟后官网自动更新 |

!!! warning "改公共章节会影响所有产品"

    改 `shared/warranty.md`（售后）、`shared/support.md`（联系方式）等，所有引用它们的说明书会一起变。这是设计如此，改前请确认。

## 方式二：每页铅笔图标

在线说明书右上角「编辑此页」→ GitHub 网页编辑器 → Commit。适合只改一两句话。

## 方式三：技术同事本地改

```powershell
git pull
python -m mkdocs serve
# 修改 docs/**
git add -A && git commit -m "docs: ..." && git push
```

---

## 管理员：部署团队密码（只做一次）

仓库里有 `worker/index.js`（Cloudflare Worker）。

1. [Cloudflare Workers](https://dash.cloudflare.com/) 创建 Worker，粘贴该文件  
2. 机密变量：
   - `GITHUB_TOKEN`：仅本仓库、`contents: write` 的 Fine-grained PAT  
   - `TEAM_PASSWORD`：给同事的密码  
   - `ALLOW_ORIGIN`：`https://vulkanowrs.github.io`  
3. 把 Worker 地址 + 密码发给运营同事  

之后同事**不用**再申请 GitHub Token。
