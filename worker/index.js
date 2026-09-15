/**
 * FlyingRC 说明书管理 API（Cloudflare Worker）
 * 带 /health 诊断，便于排查 Token / 密钥问题。
 */
const OWNER = "Vulkanowrs";
const REPO = "flyingrc-manuals";
const BRANCH = "main";
const API = "https://api.github.com";

function cors(env) {
  const allow = env.ALLOW_ORIGIN || "*";
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "GET,PUT,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
  };
}

function json(data, status, env) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: { "Content-Type": "application/json; charset=utf-8", ...cors(env) },
  });
}

function b64encode(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
}

function b64decode(b64) {
  const clean = String(b64 || "").replace(/\n/g, "");
  const bin = atob(clean);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

async function gh(path, env, options = {}) {
  const token = env.GITHUB_TOKEN || "";
  if (!token) throw new Error("GITHUB_TOKEN is empty");
  const res = await fetch(API + path, {
    ...options,
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: "Bearer " + token,
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "flyingrc-docs-worker",
      ...(options.headers || {}),
    },
  });
  const text = await res.text();
  let data = {};
  try { data = text ? JSON.parse(text) : {}; } catch (_) { data = { raw: text.slice(0, 300) }; }
  if (!res.ok) {
    const msg = (data && data.message) || (data && data.raw) || res.statusText || "GitHub error";
    const doc = data && data.documentation_url ? " " + data.documentation_url : "";
    throw new Error("GitHub " + res.status + ": " + msg + doc);
  }
  return data;
}

function authOk(req, env) {
  const h = req.headers.get("Authorization") || "";
  const pass = h.replace(/^Bearer\s+/i, "").trim();
  const expect = (env.TEAM_PASSWORD || "").trim();
  return !!expect && pass === expect;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;

    if (req.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors(env) });
    }

    // 诊断：不需要密码
    if (path === "/health") {
      const hasToken = !!(env.GITHUB_TOKEN && String(env.GITHUB_TOKEN).length > 10);
      const hasPass = !!(env.TEAM_PASSWORD && String(env.TEAM_PASSWORD).length > 0);
      const hasOrigin = !!env.ALLOW_ORIGIN;
      let github = "skip";
      if (hasToken) {
        try {
          const res = await fetch(API + "/repos/" + OWNER + "/" + REPO, {
            headers: {
              Accept: "application/vnd.github+json",
              Authorization: "Bearer " + env.GITHUB_TOKEN,
              "X-GitHub-Api-Version": "2022-11-28",
              "User-Agent": "flyingrc-docs-worker",
            },
          });
          const bodyText = await res.text();
          let body = {};
          try { body = bodyText ? JSON.parse(bodyText) : {}; } catch (_) { body = { raw: bodyText.slice(0, 200) }; }
          github = res.status === 200
            ? "ok"
            : ("fail:" + res.status + ":" + (body.message || body.raw || res.statusText || ""));
        } catch (e) {
          github = "error:" + e.message;
        }
      }
      return json({
        ok: true,
        hasToken,
        hasPass,
        hasOrigin,
        github,
        tokenLen: hasToken ? String(env.GITHUB_TOKEN).length : 0,
        tokenPrefix: hasToken ? String(env.GITHUB_TOKEN).slice(0, 12) + "..." : null,
      }, 200, env);
    }

    if (!authOk(req, env)) {
      return json({ error: "密码错误或未登录" }, 401, env);
    }

    try {
      if (path === "/api/files" && req.method === "GET") {
        const ref = await gh("/repos/" + OWNER + "/" + REPO + "/git/ref/heads/" + BRANCH, env);
        const commit = await gh("/repos/" + OWNER + "/" + REPO + "/git/commits/" + ref.object.sha, env);
        const tree = await gh("/repos/" + OWNER + "/" + REPO + "/git/trees/" + commit.tree.sha + "?recursive=1", env);
        const files = (tree.tree || [])
          .filter(function (t) {
            return t.type === "blob" && t.path.indexOf("docs/") === 0 && t.path.slice(-3) === ".md";
          })
          .map(function (t) { return { path: t.path, size: t.size }; });
        return json({ files: files }, 200, env);
      }

      if (path.indexOf("/api/file/") === 0 && req.method === "GET") {
        const fp = decodeURIComponent(path.slice("/api/file/".length));
        const data = await gh("/repos/" + OWNER + "/" + REPO + "/contents/" + fp + "?ref=" + BRANCH, env);
        const content = data.content ? b64decode(data.content) : "";
        return json({ path: fp, sha: data.sha, content: content }, 200, env);
      }

      if (path.indexOf("/api/file/") === 0 && req.method === "PUT") {
        const fp = decodeURIComponent(path.slice("/api/file/".length));
        const body = await req.json();
        const payload = {
          message: body.message || ("docs: update " + fp),
          content: b64encode(body.content || ""),
          branch: BRANCH,
        };
        if (body.sha) payload.sha = body.sha;
        const result = await gh("/repos/" + OWNER + "/" + REPO + "/contents/" + fp, env, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        return json({ ok: true, sha: result.content && result.content.sha }, 200, env);
      }

      if (path === "/api/upload" && req.method === "POST") {
        const body = await req.json();
        const payload = {
          message: body.message || ("assets: upload " + body.path),
          content: body.contentBase64,
          branch: BRANCH,
        };
        try {
          const existing = await gh("/repos/" + OWNER + "/" + REPO + "/contents/" + body.path + "?ref=" + BRANCH, env);
          payload.sha = existing.sha;
        } catch (e) { /* new file */ }
        const result = await gh("/repos/" + OWNER + "/" + REPO + "/contents/" + body.path, env, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        return json({ ok: true, path: body.path, sha: result.content && result.content.sha }, 200, env);
      }

      return json({ error: "not found: " + path }, 404, env);
    } catch (e) {
      console.error("worker_error", path, e && e.message);
      return json({ error: e && e.message ? e.message : String(e) }, 500, env);
    }
  },
};
