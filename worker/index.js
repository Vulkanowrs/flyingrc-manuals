/**
 * FlyingRC 说明书管理 API（Cloudflare Worker）
 *
 * 作用：管理员在 Cloudflare 里放一个 GitHub Token，
 * 文案/运营用「团队密码」登录本 Worker，不必各自申请 Token。
 *
 * 部署（一次性，约 10 分钟）：
 * 1. https://dash.cloudflare.com → Workers 和 Pages → 创建 Worker
 * 2. 粘贴本文件内容 → 部署
 * 3. 设置 → 变量：
 *      GITHUB_TOKEN   = 仅含本仓库 contents:write 的 Fine-grained PAT（机密）
 *      TEAM_PASSWORD  = 团队密码，例如 FlyingRC2026（机密）
 *      ALLOW_ORIGIN   = https://vulkanowrs.github.io
 * 4. 记下 Worker 地址，如 https://flyingrc-docs.xxxx.workers.dev
 * 5. 打开管理页，填 Worker 地址 + 团队密码即可
 */

const OWNER = "Vulkanowrs";
const REPO = "flyingrc-manuals";
const BRANCH = "main";
const API = "https://api.github.com";

function cors(env, req) {
  const origin = req.headers.get("Origin") || "*";
  const allow = env.ALLOW_ORIGIN || "*";
  const headers = {
    "Access-Control-Allow-Origin": allow === "*" ? origin : allow,
    "Access-Control-Allow-Methods": "GET,PUT,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
  };
  return headers;
}

function json(data, status, env, req) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: { "Content-Type": "application/json; charset=utf-8", ...cors(env, req) },
  });
}

function b64encode(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  bytes.forEach((b) => (bin += String.fromCharCode(b)));
  return btoa(bin);
}
function b64decode(b64) {
  const bin = atob(b64.replace(/\n/g, ""));
  const bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

async function gh(path, env, options = {}) {
  const res = await fetch(API + path, {
    ...options,
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: "Bearer " + env.GITHUB_TOKEN,
      "X-GitHub-Api-Version": "2022-11-28",
      ...(options.headers || {}),
    },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || res.statusText);
  return data;
}

function authOk(req, env) {
  const h = req.headers.get("Authorization") || "";
  const pass = h.replace(/^Bearer\s+/i, "");
  return env.TEAM_PASSWORD && pass === env.TEAM_PASSWORD;
}

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { headers: cors(env, req) });
    const url = new URL(req.url);
    const path = url.pathname;

    if (!authOk(req, env)) {
      return json({ error: "密码错误或未登录" }, 401, env, req);
    }

    try {
      // list markdown files
      if (path === "/api/files" && req.method === "GET") {
        const ref = await gh(`/repos/${OWNER}/${REPO}/git/ref/heads/${BRANCH}`, env);
        const commit = await gh(`/repos/${OWNER}/${REPO}/git/commits/${ref.object.sha}`, env);
        const tree = await gh(
          `/repos/${OWNER}/${REPO}/git/trees/${commit.tree.sha}?recursive=1`,
          env
        );
        const files = (tree.tree || [])
          .filter(
            (t) =>
              t.type === "blob" &&
              t.path.startsWith("docs/") &&
              (t.path.endsWith(".md") || /\.(png|jpe?g|gif|webp|svg)$/i.test(t.path))
          )
          .map((t) => ({ path: t.path, size: t.size }));
        return json({ files }, 200, env, req);
      }

      // get file
      if (path.startsWith("/api/file/") && req.method === "GET") {
        const fp = decodeURIComponent(path.slice("/api/file/".length));
        const data = await gh(`/repos/${OWNER}/${REPO}/contents/${fp}?ref=${BRANCH}`, env);
        const content = data.content ? b64decode(data.content) : "";
        return json({ path: fp, sha: data.sha, content }, 200, env, req);
      }

      // save file
      if (path.startsWith("/api/file/") && req.method === "PUT") {
        const fp = decodeURIComponent(path.slice("/api/file/".length));
        const body = await req.json();
        const payload = {
          message: body.message || `docs: update ${fp}`,
          content: b64encode(body.content || ""),
          branch: BRANCH,
        };
        if (body.sha) payload.sha = body.sha;
        const result = await gh(`/repos/${OWNER}/${REPO}/contents/${fp}`, env, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        return json({ ok: true, sha: result.content && result.content.sha }, 200, env, req);
      }

      // upload binary image
      if (path === "/api/upload" && req.method === "POST") {
        const body = await req.json(); // {path, contentBase64, message}
        const payload = {
          message: body.message || `assets: upload ${body.path}`,
          content: body.contentBase64,
          branch: BRANCH,
        };
        // if exists, need sha
        try {
          const existing = await gh(
            `/repos/${OWNER}/${REPO}/contents/${body.path}?ref=${BRANCH}`,
            env
          );
          payload.sha = existing.sha;
        } catch (_) {}
        const result = await gh(`/repos/${OWNER}/${REPO}/contents/${body.path}`, env, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        return json({ ok: true, path: body.path, sha: result.content && result.content.sha }, 200, env, req);
      }

      return json({ error: "not found" }, 404, env, req);
    } catch (e) {
      return json({ error: e.message }, 500, env, req);
    }
  },
};
