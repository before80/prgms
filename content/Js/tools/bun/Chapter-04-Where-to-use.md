+++
title = "第四章 用在哪里"
weight = 40
date = "2026-03-29T14:36:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第四章　用在哪里

> 📌 **版本提示（2026-09 核对）**：Bun 当前稳定版为 1.4.x，底层已从 Zig 重写为 Rust，并继续以“接近 Node.js 兼容”为目标。具体生产迁移前请按本文场景逐项验证。

> 💡 如果你问"Bun 能干啥"，这章就是答案。它不是万能药，但在 JavaScript 开发的大部分高频场景里，Bun 都能让你少加班、早下班。

## 4.1 前端项目依赖管理

Bun 的包管理器 `bun install` 是 npm/yarn/pnpm 的直接替代品。官方给出的口径是**安装速度最多可提升约 25 倍**（相对 `npm install`，特定基准场景；实际差距取决于是首次安装还是缓存安装、依赖数量与磁盘速度）。

前端项目通常有大量的 npm 依赖，第一次 `npm install` 可能要等几分钟。用 Bun 的话，同样的项目几十秒搞定。依赖少的话？十秒以内收工，喝口水的时间都省了。

```bash
# 替换 npm install
bun install

# 安装特定包
bun add react react-dom

# 安装开发依赖
bun add -d typescript @types/react

# 卸载
bun remove react
```

### React / Vue / Svelte 项目的包安装

Bun 提供了开箱即用的官方项目模板，几秒钟拉起一个完整项目：

```bash
# 创建 React 项目（使用 Next.js 模板）
bun create next my-app
cd my-app
bun install

# 创建 Svelte 项目
bun create svelte my-svelte-app

# 创建空项目（自行搭建）
bun create bun my-app
```

### 前端工具库的安装与更新

```bash
# 更新所有依赖
bun update

# 更新特定包
bun update vite
```

> ⚡ 有意思的是，`bun update` 比 npm 的 `npm update` 快得多，但很多人不知道 Bun 还有这个命令——大概是 npm 的习惯太根深蒂固了。

---

## 4.2 TypeScript / JavaScript 项目开发

Bun 对 TypeScript 的支持是**原生级别**的——不需要任何配置，开箱即用。不用装 ts-node，不用配 tsx，不需要任何 loader。`.ts` 文件直接跑，就像 Node.js 运行 `.js` 一样自然。

### 纯 TS 后端服务开发

```typescript
// server.ts
import { Hono } from "hono";
import { cors } from "hono/cors";

const app = new Hono();

app.use("*", cors());

app.get("/", (c) => c.json({ message: "Hello from Bun!" }));

app.post("/api/users", async (c) => {
  const body = await c.req.json();
  return c.json({ ok: true, user: body });
});

export default app;
```

```bash
bun run server.ts
# 服务启动，访问 http://localhost:3000
```

### 全栈项目

Bun 的真正魅力在于前后端统一技术栈——写一份配置，前后端都能用：

- **前端**：React / Vue / Svelte + Bun 的打包器（自动处理 JSX/TSX、CSS、图片）
- **后端**：Bun 原生 HTTP 服务器，性能比 Node.js 高出一大截
- **数据**：内置 SQLite、PostgreSQL、Redis，不用装一堆驱动

```typescript
// api.ts - 后端 API 路由
export default {
  fetch(req) {
    return Response.json({ time: new Date().toISOString() });
  },
};
```

---

## 4.3 轻量级 HTTP 服务与 API 开发

Bun 的 HTTP 服务器性能极高，比 Node.js 快 **2-3 倍**（Express 框架场景可达 3 倍）。但光快没用，关键是写起来还简单。

### Bun.serve 基础用法

```typescript
// 最简单的 HTTP 服务
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/") {
      return new Response("Hello Bun!");
    }
    return new Response("Not Found", { status: 404 });
  },
});

console.log("服务启动在 http://localhost:3000");
```

### 与 Hono 框架结合

[Hono](https://hono.dev/) 是一个轻量、快速的 Web 框架，和 Bun 是绝配——它比 Express 轻，快比 Fastify，而且天然支持所有 Bun 的好东西：

```typescript
import { Hono } from "hono";
import { logger } from "hono/logger";

const app = new Hono();

app.use(logger());

app.get("/", (c) => c.text("Hello Hono + Bun!"));

app.get("/api/:name", (c) => {
  const name = c.req.param("name");
  return c.json({ greeting: `Hello, ${name}!` });
});

app.post("/data", async (c) => {
  const body = await c.req.json();
  return c.json({ received: body });
});

export default app;
```

### 与 Express / Fastify 兼容

Express 和 Fastify 的中间件在 Bun 里大部分可以正常工作，不用重写就能迁移：

```typescript
import express from "express";

const app = express();

app.get("/", (req, res) => {
  res.json({ message: "Hello from Express on Bun!" });
});

app.listen(3000, () => {
  console.log("Express 服务运行在 Bun 上！");
});
```

> 💡 虽然 Express 能在 Bun 上跑，但如果追求极致性能，还是推荐用 Bun 原生的 `Bun.serve` 或者 Hono/Fastify 等更现代的框架。毕竟用着 Bun 再套一层 Express，就像开着跑车去菜市场——有点憋屈。

---

## 4.4 前端构建与打包

Bun 的打包器是真正的多面手：处理 JSX/TSX、代码分割、CSS 加载、插件系统，统统在行。而且它比 Vite 快，比 Webpack 配置简单。

### 开发服务器

```bash
# 启动开发服务器（带 HMR）
bun --watch ./index.html

# 启动生产服务
bun ./index.html
```

Bun 的开发服务器有一个独特能力：**支持直接导入 HTML 文件作为入口**。它会自动扫描 `<script>` 和 `<link>` 标签，帮你打包所有前端资源，零配置。

```typescript
// app.ts
import homepage from "./index.html";

Bun.serve({
  routes: {
    "/": homepage,
  },
});
```

### HMR（热模块替换）

Bun 的 HMR 在开发时保留应用状态，修改代码后**不需要刷新页面**，页面内容直接更新——React 的 state 不会丢，表单内容不会清空，体验接近现代前端框架的 Hot Reload 水准。

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head><title>Bun HMR Demo</title></head>
<body>
  <h1 id="title">Hello</h1>
  <script type="module" src="./app.ts"></script>
</body>
</html>
```

```typescript
// app.ts - 修改这行文字，浏览器里直接看到变化，无需刷新
const title = document.getElementById("title")!;
title.textContent = "Hello, HMR!";
```

### 生产环境打包

```bash
# 生产构建（压缩 + 优化）
bun build ./src/index.tsx \
  --outdir=dist \
  --target=browser \
  --minify

# 代码分割（自动拆包）
bun build ./src/index.tsx \
  --outdir=dist \
  --target=browser \
  --splitting

# 生成单文件可执行包
bun build ./src/cli.ts \
  --outfile=my-app \
  --target=bun
```

### 插件系统

Bun 支持用插件扩展打包和运行时的行为，比如加载 `.scss`、`.yaml` 等非标准文件类型：

```typescript
import type { BunPlugin } from "bun";

const myPlugin: BunPlugin = {
  name: "Custom loader",
  setup(build) {
    build.onLoad({ filter: /\.yaml$/ }, (args) => {
      return { loader: "text", contents: "..." };
    });
  },
};

await Bun.build({
  entrypoints: ["./app.ts"],
  outdir: "./out",
  plugins: [myPlugin],
});
```

---

## 4.5 自动化脚本与 CLI 工具

### 跨平台 Shell 脚本

Bun 的 `$` 语法让你写脚本完全不需要 bash/powershell 的兼容性问题——写一次，哪都能跑：

```typescript
import { $ } from "bun";

async function buildProject() {
  console.log("开始构建...");

  // 并行执行多个任务
  await Promise.all([
    $`bun run build:css`,
    $`bun run build:js`,
    $`bun run build:html`,
  ]);

  console.log("构建完成！");
}

await buildProject();
```

### 数据处理脚本

```typescript
import { readFileSync, writeFileSync } from "fs";

// 读取 CSV
const csv = readFileSync("data.csv", "utf8");
const rows = csv.split("\n").slice(1); // 跳过表头

// 处理数据
const total = rows
  .filter(row => row.length > 0)
  .map(row => {
    const [name, age, city] = row.split(",");
    return { name, age: Number(age), city };
  })
  .filter(person => person.age > 30)
  .length;

writeFileSync("result.json", JSON.stringify({ count: total }));
console.log(`30岁以上人数：${total}`);
```

> 💡 `$` 模板字符串里的命令会通过 Bun 内置的 Shell 执行，在 Windows 上自动使用 bun shell（兼容 bash 语法），再也不用写两份脚本了。

---

## 4.6 Serverless 函数

### Cloudflare Workers

Cloudflare Workers 是 Bun 官方支持的 Serverless 平台，写好的 Bun 代码可以直接部署到全球 300+ 个边缘节点：

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/hello") {
      return Response.json({ message: "Hello from Cloudflare Workers!" });
    }

    return new Response("Not Found", { status: 404 });
  },
} satisfies ExportedHandler;
```

### Vercel Edge Functions

```typescript
export const config = { runtime: "edge" };

export default function handler(req: Request) {
  return Response.json({
    message: "Hello from Vercel Edge!",
    timestamp: Date.now(),
  });
}
```

> 🌍 Bun 的 Serverless 支持不只是"能跑"——它对启动速度的优化让冷启动时间大幅缩短，在讲究毫秒必争的边缘计算场景里，这可不是小事。

---

## 4.7 数据库与存储操作

### SQLite（bun:sqlite）

SQLite 是本地开发和小规模项目的神器，Bun **内置**了 SQLite 驱动，不需要安装任何包。插入就能用，快得像 in-memory 数据库：

```typescript
import { Database } from "bun:sqlite";

const db = new Database("myapp.db");

// 创建表
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
  )
`);

// 插入数据（参数化查询，防 SQL 注入）
const insert = db.query(
  "INSERT INTO users (name, email) VALUES ($name, $email)"
);
insert.run({ $name: "张三", $email: "zhangsan@example.com" });

// 查询
const users = db.query("SELECT * FROM users").all();
console.log(users);

// 事务
db.run("BEGIN TRANSACTION");
try {
  db.run("INSERT INTO users (name, email) VALUES ($n, $e)", {
    $n: "李四",
    $e: "lisi@example.com",
  });
  db.run("COMMIT");
} catch {
  db.run("ROLLBACK");
}
```

### PostgreSQL / MySQL

Bun 内置了统一 SQL 客户端（v1.3+），支持 PostgreSQL 和 MySQL，不需要额外的 npm 包：

```typescript
import { sql, SQL } from "bun";

// PostgreSQL（默认，或显式指定连接字符串）
const pgResult = await sql`SELECT * FROM products LIMIT 10`;
console.log(pgResult.rows);

// MySQL（显式指定）
const mysql = new SQL("mysql://admin:secret@localhost:3306/myapp");
const mysqlResult = await mysql`SELECT * FROM products WHERE id = ${42}`;
console.log(mysqlResult.rows);
```

> 💡 v1.2 引入 PostgreSQL 客户端（`Bun.sql` 模板 API），MySQL 在 v1.3 才加入。v1.3 进一步统一为 `sql`/`SQL` 导入接口，并同时支持 PostgreSQL 和 MySQL。

### Redis

Bun 内置了 Redis 客户端（v1.3+），不需要安装 `ioredis` 或其他第三方库：

```typescript
import { redis } from "bun";

// 字符串操作
await redis.set("token", "abc123", { EX: 3600 }); // 1小时过期
const token = await redis.get("token");
console.log(token); // abc123

// Hash 操作
await redis.hset("user:1", { name: "张三", age: "28" });
const user = await redis.hgetall("user:1");
console.log(user); // { name: "张三", age: "28" }

// 列表操作
await redis.lpush("queue", "任务1", "任务2", "任务3");
const first = await redis.lpop("queue");
console.log(first); // 任务3（最后 push 的）
```

> 💡 Bun 的 Redis 客户端使用环境变量 `REDIS_URL` 自动读取连接信息，部署到 Serverless 环境时完全不用改代码。

### S3 对象存储

Bun 内置了 S3 客户端（v1.2+），兼容 AWS S3、Cloudflare R2、DigitalOcean Spaces、MinIO 等所有 S3 协议存储：

```typescript
import { S3Client, s3, write } from "bun";

// s3 是全局单例，自动读取环境变量
// 也可以显式创建客户端
const client = new S3Client({
  region: "us-east-1",
  credentials: {
    accessKeyId: "YOUR_KEY",
    secretAccessKey: "YOUR_SECRET",
  },
});

// 上传文件：先获取 S3File 引用，再用 write() 写入
const s3file = client.file("my-bucket/hello.txt");
await write(s3file, "Hello World!");

// 下载文件：S3File 继承自 Blob，可用 .text()/.json() 等方法读取
const content = await s3file.text();
console.log(content); // Hello World!

// 生成预签名 URL（30分钟有效）
const signedUrl = await s3file.presign({
  expiresIn: 1800,
});
console.log(signedUrl);

// 删除文件
await s3file.delete();
```

### 键值存储与缓存：没有内置 KV，但有 Redis 客户端

> ⚠️ **澄清一个常见误传**：Bun **没有** `Bun.KV` 这类内置键值存储 API。截至 1.4.2，官方文档 "Data & Storage" 分类下只有 Cookies、File I/O、Streams、Binary Data、Archive、SQL、SQLite、S3、Redis；`Bun.KV.open(...)`、`kv.setMany(...)` 之类的写法并不存在，写了会直接报错。看到这类代码请以官方文档为准。

键值 / 缓存需求，按下面这张表选方案就不会错：

| 需求 | 推荐方案 |
|------|----------|
| 单机、随应用一起走的小数据 | `bun:sqlite`（建一张 key/value 表，事务、索引、查询都现成） |
| 分布式缓存、会话、限流计数、消息队列 | `Bun.redis`（1.3+，同时支持 Valkey） |
| 存文件、图片、备份、静态资源 | `Bun.s3`（1.2+，兼容 R2 / MinIO 等 S3 协议存储） |

`Bun.redis` 提供两种用法：全局单例（默认读环境变量 `REDIS_URL`）与自建连接：

```typescript
// 用法一：全局单例（适合大多数场景）
import { redis } from "bun";

await redis.set("name", "Bun Fan");
console.log(await redis.get("name"));   // "Bun Fan"

await redis.set("session:123", "active");
await redis.expire("session:123", 3600); // 1 小时后过期
console.log(await redis.ttl("session:123"));

await redis.incr("counter");            // 原子自增，适合计数器/限流
await redis.del("name");

// 用法二：自建连接，可以指定地址，也能用于发布/订阅
import { RedisClient } from "bun";

const client = new RedisClient("redis://localhost:6379");
await client.connect();
await client.set("name", "Bun Fan");
console.log(await client.get("name"));
client.close();
```

> 💡 官方把 Redis 的**发布/订阅**（1.2.23 加入）标注为实验性：订阅会独占连接，带订阅的客户端只能调用订阅相关方法，不能再执行普通命令，需要另外建一个客户端做读写。

---

## 本章小结

本章介绍了 Bun 的主要应用场景——从安装包到写后端，从打包前端到部署 Serverless，基本覆盖了 JavaScript 开发的全流程。

| 场景 | 核心能力 | 关键命令 |
|------|----------|----------|
| 前端依赖管理 | 包安装最多快约 25 倍（官方口径） | `bun install` / `bun add` |
| TS/JS 开发 | TypeScript 开箱即用 | `bun run` |
| HTTP 服务 | 比 Node.js 快 2-3 倍 | `Bun.serve` |
| 前端构建 | 极速打包 + HMR | `bun build` |
| 自动化脚本 | 跨平台 `$` 语法 | `$` 模板字符串 |
| Serverless | Cloudflare / Vercel 支持 | 零配置部署 |
| 数据库与存储 | SQLite/PostgreSQL/MySQL/MariaDB(v1.3)/Redis(v1.3)/S3(v1.2) | 内置驱动，无需安装 |
| 测试 | Jest 兼容，TypeScript 原生 | `bun test` |

总的来说，Bun 覆盖了 JavaScript 开发中**绝大多数高频场景**，而且每个场景都比传统工具更快、更简单。你不需要换掉所有工具，只需要在任何一个环节试试 Bun——大概率就回不去了。
