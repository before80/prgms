+++
title = "第五章 怎么用"
weight = 50
date = "2026-03-29T14:36:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第五章 怎么用

欢迎来到 Bun 的"灵魂拷问"环节——前四章我们把 Bun 从头到脚介绍了一遍，现在终于要上手"干活"了。本章是 Bun 的**实战指南**，覆盖从安装到生产的完整流程，保证你学完就能跑。

> 如果你是从 Node.js 切换过来的，别担心——Bun 的口号是"零成本迁移"，我们会在每个环节证明这不是吹牛。

---

## 5.1 安装 Bun

安装 Bun 是你踏上 Bun 之旅的第一步，也是唯一需要"安装"的步骤——之后所有的工具都是 Bun 自带的！就像买了一把瑞士军刀，打开盒子那一刻，所有刀片都在里面了。

### Windows 安装

```powershell
# PowerShell 一行命令搞定（推荐）
irm bun.sh/install.ps1 | iex

# 或者手动下载安装
# 下载地址：https://github.com/oven-sh/bun/releases
```

> Windows 要求 Windows 10 版本 1809 或更高。如果安装后提示"command not found"，需要把 `C:\Users\你的用户名\.bun\bin` 添加到系统 PATH 环境变量里——这大概是整个安装过程中最"坑"的一步。

### macOS 安装

```bash
# Homebrew（推荐）
brew install oven-sh/bun/bun

# 或者官方脚本
curl -fsSL https://bun.com/install | bash
```

### Linux 安装

```bash
curl -fsSL https://bun.com/install | bash
```

> Linux 需要 unzip 包：`sudo apt install unzip`。内核建议 5.6+，最低 5.1。CentOS/RHEL 用户：`sudo yum install unzip`。

### npm 安装

```bash
npm install -g bun
```

Bun 官方说这是"你最后一个需要全局安装的 npm 包"——因为装完 Bun 之后，你再也不需要 npm install 全局包了。Bun 自己会帮你搞定一切。

### Docker 安装

```bash
# 标准镜像
docker pull oven/bun

# 运行
docker run --rm --init oven/bun bun --version

# 带项目的运行方式
docker run --rm -it -v $(pwd):/app -w /app oven/bun bun install
```

Docker 镜像变体：`oven/bun:debian`、`oven/bun:slim`、`oven/bun:alpine`、`oven/bun:distroless`。追求小体积？选 alpine；追求兼容性？选 debian。

### 升级 Bun

```bash
# 升级到最新稳定版
bun upgrade

# 升级到最新测试版（canary）
bun upgrade --canary

# 切回稳定版
bun upgrade --stable
```

> Homebrew 用户用 `brew upgrade bun`，Scoop 用户用 `scoop update bun`。

### 验证安装

```bash
bun --version     // 1.3.x（当前稳定版）
bun --revision    // 1.3.x+xxxxxxxxxxxx（精确 git commit hash）
```

> 版本号会随着发布更新，以上只是示例格式。如果看到版本号，说明一切正常——恭喜你，正式成为 Bun 用户！

### 卸载 Bun

```bash
# macOS / Linux
rm -rf ~/.bun

# Windows：运行卸载脚本
# 在文件管理器打开 %USERPROFILE%\.bun\ 目录，双击 uninstall.ps1
```

卸载前请三思——你确定要和一个启动速度比 Node 快 4 倍的运行时说再见吗？

---

## 5.2 包管理命令

Bun 的包管理命令和 npm 几乎一样，迁移成本为零。如果你用过 npm，看到下面的命令会有一种"这不就是换了个前缀"的快感。

### 安装依赖

```bash
# 安装所有依赖（等价于 npm install）
bun install

# 只安装生产依赖（跳过 devDependencies）
bun install --production

# CI 常用：锁定文件不允许变更（等价于 npm ci）
bun install --frozen-lockfile
```

### 添加包

```bash
# 安装并写入 package.json（等价于 npm install xxx）
bun add react react-dom

# 安装为开发依赖（等价于 npm install -D xxx）
bun add -d typescript @types/react
```

### 删除包

```bash
# 删除包并从 package.json 移除（等价于 npm uninstall xxx）
bun remove react
```

### 更新包

```bash
bun update              # 更新所有包（等价于 npm update）
bun update vite         # 更新特定包
```

### 查看包信息

```bash
# 查看依赖树（等价于 npm ls）
bun pm ls               # 查看已安装的包

# 查看包详情（等价于 npm info）
bun info react

# 安全审计（等价于 npm audit）
bun audit
```

> `bun list` 在某些旧版是别名，但新版推荐用 `bun pm ls`。

---

## 5.3 运行脚本

这一节是你最常用的部分——写完代码就要跑，跑了就要改，改完再跑。

### 运行 package.json 里的脚本

```bash
bun run dev        # 运行 dev 脚本
bun run build      # 运行 build 脚本
bun run test       # 运行 test 脚本
bun run            # 不带参数，列出所有可用脚本
```

### 直接运行文件

```bash
bun run index.ts        # 运行 TypeScript 文件
bun index.tsx           # 裸命令，等价于 bun run
bun index.js            # 直接运行 JS 文件
```

> 裸命令（如 `bun index.tsx`）和 `bun run index.tsx` 完全等效，只是少敲了几个字——懒人福利。

### 从模板创建项目

```bash
bun create react my-app       # React 项目模板
bun create library my-lib     # 类库项目模板
bun create blank my-project   # 空白项目
bun create https://example.com/template.zip  # 从 URL 创建
```

### 不安装直接运行包（bunx）

```bash
bunx cowsay "Hello from Bun!"  # 等价于 npx，但快很多（预热后基本无延迟）
```

> `bunx` 是 `bun execute` 的别名，第一次运行会缓存，不用每次都下载。

### 从 stdin 运行代码

```bash
# 相当于一个临时的小脚本执行器
echo "console.log('Hello!')" | bun run -
```

### Shebang 脚本

```bash
#!/usr/bin/env bun
console.log("这是一个独立运行的脚本！");
```

保存为 `script.ts`，赋予执行权限后直接运行：

```bash
chmod +x script.ts && ./script.ts
```

> Shebang 脚本在 Unix 系统下可以直接双击运行——比打开终端敲命令优雅多了。

---

## 5.4 TypeScript 支持

Bun 对 TypeScript 的支持是**内置的、零配置的**。你不需要装 ts-node、不需要配置 tsconfig、不需要任何额外步骤——把 `.js` 改成 `.ts`，然后直接跑。

### 无需配置

```typescript
// greeter.ts
interface User {
  name: string;
  age: number;
}

function greet(user: User): string {
  return `你好，${user.name}！今年${user.age}岁了。`;
}

const user: User = { name: "张三", age: 25 };
console.log(greet(user));
```

```bash
bun run greeter.ts
// 输出：你好，张三！今年25岁了。
```

tsconfig.json 会被自动读取，路径别名（paths）也自动生效。Bun 会尊重你已有的 tsconfig 配置，不需要额外适配。

### JSX 支持

```tsx
// app.tsx
import React from "react";

interface CardProps {
  title: string;
  children: React.ReactNode;
}

const Card = ({ title, children }: CardProps) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div>{children}</div>
    </div>
  );
};

const App = () => (
  <Card title="欢迎使用 Bun">
    <p>Bun 让 TypeScript 和 JSX 开发变得无比简单！</p>
  </Card>
);

export default App;
```

```bash
bun run app.tsx  # 直接运行，不需要任何配置！
```

> Bun 内置了 esbuild 来处理 JSX/TSX 编译，速度比 tsc 快 10-20 倍。当然了，最终上线前还是建议用 tsc 做完整类型检查。

---

## 5.5 环境变量

Bun 自动加载 `.env` 文件，不需要 `dotenv` 包——又一个"不需要安装额外依赖"的例子。

### .env 文件

```bash
# .env
DATABASE_URL=postgres://localhost:5432/myapp
API_KEY=hello-world-secret
NODE_ENV=development
```

### 代码中使用

```typescript
console.log(process.env.DATABASE_URL);
// postgres://localhost:5432/myapp
console.log(process.env.API_KEY);
// hello-world-secret
```

### 多环境配置

Bun 按以下顺序加载 `.env` 文件，后面的覆盖前面的：

```
.env                        # 所有环境共享的基础配置
.env.local                  # 本地覆盖（不提交到 Git，优先级最高）
.env.[BUN_ENV]              # 按环境加载，比如 .env.development 或 .env.production
```

> 如果设置了 `BUN_ENV=development`，会额外加载 `.env.development`。不设置时默认读取 `.env` 和 `.env.local`。

---

## 5.6 HTTP 服务开发

这是 Bun 最闪耀的部分之一——不用 Express，不用 Fastify，原生 API 写 HTTP 服务，性能比 Node 快 2-3 倍。

### Bun.serve 基础

```typescript
// server.ts
const server = Bun.serve({
  port: 3000,          // 端口号（也可以是字符串如 "3000"）
  hostname: "0.0.0.0", // 监听所有网卡，默认 localhost
  fetch(req) {
    return new Response("Hello from Bun HTTP server!");
  },
});

console.log(`🚀 服务启动啦：http://${server.hostname}:${server.port}`);
```

```bash
bun run server.ts
# 服务启动：bun serving on http://localhost:3000
```

> 注意：`port` 如果被占用，Bun 会自动选择下一个可用端口，并通过 `server.port` 获取实际端口号。写死端口时记得做好错误处理。

### JSON 响应

```typescript
async fetch(req) {
  const data = {
    message: "Hello JSON!",
    timestamp: new Date().toISOString(),
    count: 42,
  };
  // Bun 专用快捷方式，自动设置 Content-Type: application/json
  return Response.json(data);
}
```

> 注意：`Response.json()` 是 Bun/Fetch API 的标准方法，Node.js 12+ 也支持。放心用。

### 路由处理

```typescript
async fetch(req) {
  const url = new URL(req.url);
  const pathname = url.pathname;

  // GET /api/users - 返回用户列表
  if (pathname === "/api/users" && req.method === "GET") {
    return Response.json([
      { id: 1, name: "张三" },
      { id: 2, name: "李四" },
    ]);
  }

  // GET /api/users/:id - 返回单个用户
  if (pathname.startsWith("/api/users/") && req.method === "GET") {
    const id = pathname.split("/")[3];
    return Response.json({ id, name: `用户${id}` });
  }

  return new Response("Not Found", { status: 404 });
}
```

> 更复杂的路由（如 RESTful 风格参数解析）可以引入 `bun:router`，或使用社区路由库如 `@bunjs/router`。

### 静态文件服务

```typescript
// 注意：serve 是 Bun.serve，不是从 "bun" 导入的
const server = Bun.serve({
  port: 3000,
  async fetch(req) {
    const url = new URL(req.url);
    const filePath = url.pathname === "/"
      ? "./public/index.html"
      : `./public${url.pathname}`;

    const file = Bun.file(filePath);
    // BunFile 对象可以直接作为 Response 的 body
    return new Response(file);
  },
});
```

> `Bun.file()` 返回一个 `BunFile` 对象，Bun 会自动读取文件内容并确定 MIME 类型。BunFile 是惰性加载的，大文件也不会撑爆内存。

### WebSocket 服务

```typescript
const server = Bun.serve({
  port: 3000,
  fetch(req, server) {
    // 尝试升级为 WebSocket
    const success = server.upgrade(req);
    if (success) return;        // 升级成功，不返回 Response
    return new Response("Upgrade Required", { status: 426 });
  },
  websocket: {
    open(ws) {
      console.log("🟢 新连接:", ws.remoteAddress);
      ws.send("欢迎连接！");
    },
    message(ws, msg) {
      console.log("📨 收到消息:", msg);
      ws.send(`你说了: ${msg}`);  // echo 回去
    },
    close(ws, code, reason) {
      console.log("🔴 连接关闭:", code, reason);
    },
    // 可选：ping/pong 心跳
    ping(ws, data) {},
    pong(ws, data) {},
  },
});
```

### Cookie 处理

```typescript
async fetch(req) {
  // 读取 Cookie
  const cookie = req.headers.get("Cookie") || "";
  const sessionId = cookie
    .split("; ")
    .find(c => c.startsWith("session="))
    ?.split("=")[1];

  const body = JSON.stringify({ sessionId: sessionId ?? null });
  const response = new Response(body, {
    headers: { "Content-Type": "application/json" },
  });

  // 设置 Cookie
  response.headers.append(
    "Set-Cookie",
    "session=abc123; Path=/; HttpOnly; Max-Age=3600"
  );

  return response;
}
```

---

## 5.7 测试

Bun 内置的测试运行器速度极快（比 Jest 快 10-30 倍），而且**兼容 Jest 大部分 API**——你不需要重写现有的测试。

### 写一个测试

```typescript
// math.test.ts
import { test, expect, describe } from "bun:test";

describe("数学运算", () => {
  test("加法", () => {
    expect(1 + 1).toBe(2);
  });

  test("乘法", () => {
    expect(3 * 4).toBe(12);
  });

  test("异步操作", async () => {
    const result = await Promise.resolve(42);
    expect(result).toBe(42);
  });
});
```

```bash
bun test
# bun test v1.3.x
#   math.test.ts
#    数学运算
#      ✓ 加法 (1ms)
#      ✓ 乘法
#      ✓ 异步操作
#  3 pass 0 fail 3 tests
```

> 如果你写过 Jest 测试，上面的代码应该看起来非常眼熟——Bun 的目标就是让 Jest 用户无缝切换。

### Mock 函数

```typescript
import { test, expect, mock } from "bun:test";

test("Mock 函数演示", async () => {
  // 创建一个返回固定值的 mock 函数
  const fn = mock(() => 42);
  console.log(fn()); // 42

  // 创建一个异步 mock 函数
  const fetchUser = mock(async (id: number) => ({
    id,
    name: `User ${id}`,
  }));

  const user = await fetchUser(1);
  console.log(user); // { id: 1, name: "User 1" }
  expect(fetchUser).toHaveBeenCalledWith(1);
});
```

> `mock()` 是 Bun 自己的实现，不需要安装 `jest-mock` 或 `sinon`。

### 并发测试

```typescript
test("并发测试", async () => {
  // Bun 会尽可能并行运行标记了 concurrent: true 的测试
}, { concurrent: true });
```

> 并发测试要小心共享状态——多个测试同时修改全局变量会让你debug到怀疑人生。

### 覆盖率报告

```bash
bun test --coverage
# 会在终端显示详细的覆盖率统计
```

### 指定测试文件

```bash
bun test ./src/math.test.ts           # 只运行特定文件
bun test --test-name-pattern "加法"   # 只运行名字含"加法"的测试
```

---

## 5.8 构建与打包

Bun 的构建工具适合**轻量打包**场景，比如类库、工具脚本。如果你要构建复杂的大型应用，Vite/Webpack 仍然是更好的选择。

### 基本打包

```bash
bun build ./src/index.tsx \
  --outdir=dist \
  --target=browser \
  --minify
```

### 多平台目标

```bash
# 浏览器（生成 ESM/CJS 模块）
bun build ./src/app.ts --target=browser --outdir=dist

# Node.js（生成 CJS 或 ESM）
bun build ./src/app.ts --target=node --outdir=dist

# Bun 运行时（生成纯 Bun 可执行文件）
bun build ./src/app.ts --target=bun --outdir=dist
```

### 单文件可执行文件（独立运行时）

```bash
# 打包为单文件可执行文件（需要 target=bun）
bun build --target=bun --outfile=myapp ./myapp.ts
./myapp  # 直接运行，不需要安装 Bun！
```

> 生成的可执行文件是平台相关的——Linux 上打包只能在 Linux 上运行，macOS同理。跨平台构建需要 Docker 或 CI。

### 环境变量内联

```typescript
// app.ts
const dbUrl = process.env.DATABASE_URL ?? "localhost";

// build.ts
await Bun.build({
  entrypoints: ["./app.ts"],
  outdir: "./dist",
  env: "inline",  // process.env.* 在构建时被替换为实际值
});
```

> 注意：环境变量内联后，敏感信息（如 API Key）会直接写入产物，**不要**把包含密钥的代码提交到公开仓库。

---

## 5.9 代码质量工具

Bun 自带格式化工具，虽然生态不如 ESLint/Prettier 丰富，但对于中小项目已经够用。

### bun fmt - 代码格式化

```bash
bun fmt                # 格式化当前目录所有文件
bun fmt ./src          # 格式化指定目录
bun fmt --check        # 只检查，不修改（适合 CI）
```

### bun lint - 代码检查

```bash
bun lint               # 检查代码问题
```

> Bun 的 lint 目前还在积极开发中，规则集不如 ESLint 丰富。有复杂 lint 需求的项目建议继续使用 ESLint。

---

## 5.10 SQLite 专项（bun:sqlite）

SQLite 是世界上最流行的数据库，Bun **内置**了高性能 SQLite 驱动——比 `better-sqlite3` 快 3-6 倍，比 `sql.js` 快更多。而且不需要安装任何包，直接 `import` 就行。

### 基本操作

```typescript
import { Database } from "bun:sqlite";

const db = new Database("app.db");  // 文件数据库，:memory: 是内存数据库

// 创建表
db.run(`
  CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TEXT DEFAULT (datetime('now'))
  )
`);

// 插入数据（使用参数化查询，防 SQL 注入）
const insert = db.query(
  "INSERT INTO posts (title, content) VALUES ($title, $content)"
);
insert.run({ $title: "我的第一篇文章", $content: "Hello Bun!" });
insert.run({ $title: "第二篇", $content: "SQLite 真好用！" });

// 查询所有
const all = db.query("SELECT * FROM posts").all();
console.log(all);
// 输出：
// [
//   { id: 1, title: "我的第一篇文章", content: "Hello Bun!", created_at: "2024-01-01 12:00:00" },
//   { id: 2, title: "第二篇", content: "SQLite 真好用！", created_at: "2024-01-01 12:01:00" }
// ]

// 条件查询（只取一条）
const one = db.query("SELECT * FROM posts WHERE id = $id").get({ $id: 1 });
console.log(one);
// { id: 1, title: "我的第一篇文章", content: "Hello Bun!", created_at: "..." }

// 更新数据
db.run("UPDATE posts SET title = $title WHERE id = $id", {
  $title: "更新后的标题",
  $id: 1,
});

// 删除数据
db.run("DELETE FROM posts WHERE id = $id", { $id: 2 });
```

> `db.query()` 返回一个**预编译语句**对象，`.all()` 取所有行，`.get()` 取第一行，`.run()` 执行不返回结果集的操作。预编译语句可以复用，性能更好。

### 事务

```typescript
db.run("BEGIN TRANSACTION");
try {
  db.run("INSERT INTO posts (title) VALUES ($t)", { $t: "标题A" });
  db.run("INSERT INTO posts (title) VALUES ($t)", { $t: "标题B" });
  db.run("COMMIT");
} catch (err) {
  db.run("ROLLBACK");
  console.error("事务失败，已回滚:", err);
}
```

> Bun 的 SQLite 驱动也支持更便捷的 `db.transaction()` 包装：
> ```typescript
> const insertMany = db.transaction((titles: string[]) => {
>   for (const title of titles) {
>     db.run("INSERT INTO posts (title) VALUES ($t)", { $t: title });
>   }
> });
> insertMany(["标题A", "标题B"]); // 自动开启事务，成功自动 COMMIT，失败自动 ROLLBACK
> ```

### 严格模式

```typescript
// strict: true - 所有绑定参数必须带 $ 前缀，否则报错
const strictDb = new Database(":memory:", { strict: true });
try {
  // 注意：参数 key 是 "id"，但查询占位符是 $id —— 少了 $ 前缀会报错
  strictDb.query("SELECT * FROM users WHERE id = $id").get({ id: 1 });
} catch (e) {
  console.log("报错：", e.message);
  // 输出类似：Parameter "id" must have a $ prefix (got "id")
}
```

> 严格模式可以帮助你尽早发现参数绑定错误，建议在生产环境中开启。

---

## 5.11 WebSocket 专项

Bun 原生支持 WebSocket，不需要安装任何 ws 库。和 HTTP 服务一样，都是 `Bun.serve` 的一部分。

### Pub/Sub（发布/订阅）

```typescript
Bun.serve({
  port: 3000,
  fetch(req, server) {
    const url = new URL(req.url);
    if (url.pathname === "/ws") {
      // 升级到 WebSocket，并携带额外数据
      server.upgrade(req, { data: { pathname: url.pathname } });
      return;
    }
    return new Response("Only WebSocket at /ws");
  },
  websocket: {
    open(ws) {
      ws.subscribe("general");              // 加入 "general" 频道
      console.log("🟢 用户加入 general 频道，当前地址:", ws.remoteAddress);
    },
    message(ws, msg) {
      // 注意：server.publish(频道, 消息) - 频道在前，消息在后
      server.publish("general", `广播: ${msg}`);
    },
    close(ws, code, reason) {
      ws.unsubscribe("general");            // 离开频道
      console.log("🔴 用户离开 general 频道", code, reason);
    },
  },
});
```

> `server.publish()` 的参数顺序是 `publish(channel, message)`，不是 `publish(message, channel)`——很多人第一次用会搞反。

### 配置选项

```typescript
Bun.serve({
  port: 3000,
  fetch(req, server) { server.upgrade(req); return; },
  websocket: {
    // 每条消息最大 1MB（默认 16MB）
    maxPayloadLength: 1024 * 1024,
    // 空闲超时 60 秒后自动关闭（默认 120 秒）
    idleTimeout: 60,
    // 启用 per-message 压缩（默认 false）
    perMessageDeflate: true,
    // 每条 incoming 消息最大体积（默认 16MB）
    maxFragmentSize: 65536,
  },
});
```

---

## 本章小结

本章是 Bun 的"实战指南"，覆盖了从安装到使用的完整流程。总结一下核心知识点：

**安装**：Windows 一行命令、macOS 用 Homebrew、Linux 用 curl、Docker 多镜像可选。`bun upgrade` 一键升级。

**包管理**：`bun install/add/remove/update`，与 npm 用法完全一致，零迁移成本。

**运行脚本**：`bun run` 替代 `node` 和 `npx`，`bunx` 替代 `npx` 不安装运行。

**TypeScript 支持**：零配置，`.ts`/`.tsx` 直接跑，Bun 自动处理类型检查和编译（但上线前仍建议用 tsc 做完整检查）。

**HTTP 服务**：`Bun.serve` 写起来比 Express 简洁，性能高 2-3 倍（Express 场景可达 3 倍），原生支持 WebSocket。

**测试**：`bun test` 兼容 Jest API，速度快 10-30 倍，内置 Mock 和覆盖率报告。

**构建**：`bun build` 适合轻量打包，`--target=bun --outfile` 生成单文件可执行文件。

**SQLite**：`bun:sqlite` 内置驱动，参数化查询防注入，比 `better-sqlite3` 快 3-6 倍。

**WebSocket**：`server.upgrade()` 升级连接，`ws.subscribe/publish` 做 Pub/Sub 广播。

**代码质量**：`bun fmt` + `bun lint`，开箱即用，虽然生态不如 ESLint/Prettier 丰富，但对简单项目足够。

学完这一章，你应该已经可以：
- 用 Bun 跑 TypeScript 代码
- 写一个带路由和 JSON 接口的 HTTP 服务
- 用 Bun 原生测试框架写测试
- 用 SQLite 存储数据
- 打包一个可执行文件

下一章我们来聊聊 Bun 的**生态和插件系统**，以及如何参与贡献。🎉
