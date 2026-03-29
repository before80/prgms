+++
title = "第三章 有什么用"
weight = 30
date = "2026-03-29T14:36:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三章　有什么用

## 3.1 设计目标（官方五大设计原则）

Bun 团队在设计 Bun 时有五大核心原则，这些原则指导着 Bun 的每一次迭代。

> 💡 想象一下，如果厨房里只能有一把刀，这把刀要能切菜、切肉、削水果、开罐头——Bun 就是 JavaScript 世界的这把"瑞士军刀"。

### 速度压倒一切

Bun 的首要目标就是**快**。JavaScript 工具链的每一个环节——安装包、运行脚本、打包代码、跑测试——都要比现有工具快一个数量级。

JavaScriptCore 引擎 + Zig 语言优化的组合拳，让 Bun 在多个维度都显著快于 Node.js：**进程启动快 4 倍**，**HTTP 吞吐量高 2-3 倍**，**包安装快 30 倍**。这三个数字来自 Bun 官方 benchmark，不是我们拍脑袋编的。

### TypeScript & JSX 无需配置

在 Bun 之前，你运行 TypeScript 需要：装 ts-node 或 tsx、配置 tsconfig.json、可能还要装一堆类型声明包。好不容易配好了，ESLint 又报一堆奇奇怪怪的错。

**Bun 不需要**。你写一个 `.ts` 文件，直接 `bun run` 就跑起来了。JSX 也是，写 `.tsx`，直接运行，不需要 webpack 配 loader，不需要 babel 配插件，不需要对着报错信息怀疑人生。

```typescript
// index.tsx - 直接运行，不需要任何配置！
import React from "react";

const App = () => {
  return <h1>Hello, Bun!</h1>;
};

console.log(App);
```

### ESM & CommonJS 兼容

JavaScript 有两套模块系统：老的 CommonJS（`require()`）和新潮的 ES Modules（`import/export`）。在 Node.js 里这两者经常打架，各种奇怪问题让你头疼——比如明明有这个包，`require` 就是找不到；或者 `import` 了半天，报一个不知所云的循环引用错误。

Bun **两者都原生支持，而且支持得很好**。你可以混着用，Bun 会自动处理模块系统的转换。这对迁移项目特别友好——你不需要一次性把所有 `require` 改成 `import`，慢慢来就行。

### Web 标准 API 原生实现

Bun 基于 JavaScriptCore 实现了大量 Web 标准 API，比如 `fetch`、`Response`、`Request`、`Headers`、`WebSocket` 等。

这意味着你在浏览器里怎么写 HTTP 请求，在 Bun 里几乎一样的代码：

```typescript
// 浏览器里
const res = await fetch("https://api.example.com/data");

// Bun 里——完全一样的代码！
const res = await fetch("https://api.example.com/data");
```

写一次，到处跑（当然，跨平台还是要测一下的）。

### Node.js 兼容性

Bun 的终极目标是 **100% 兼容 Node.js**。这意味着你把 `node` 换成 `bun`，你的项目大概率能直接跑起来。

当然，"100%"是目标，目前还在路上。但对于大部分项目来说，兼容性已经非常好了——你不需要把所有依赖都检查一遍才知道能不能迁移。

---

## 3.2 Built-in Core Features（内置核心能力）

Bun 官网有一个对比表，列出了 Bun 内置的、而 Node.js 需要额外安装包才能有的功能。

### 数据库驱动

Bun **内置**了以下数据库驱动，不需要 npm install：

- **SQLite**：通过 `bun:sqlite`，高性能，比 better-sqlite3 快 3-6 倍
- **PostgreSQL / MySQL**：通过统一的 `sql` 标签模板 API（v1.3+），从 `bun` 导入

> ⚠️ 注意：MariaDB 暂时还不是 Bun 内置的，建议使用传统 `mysql2` 包。

```typescript
// SQLite - 直接导入，无需安装
import { Database } from "bun:sqlite";
const db = new Database("my.db");

// PostgreSQL / MySQL - 统一使用 sql 模板 API（v1.3+）
import { sql, SQL } from "bun";

// PostgreSQL（默认）
const pgUsers = await sql`SELECT * FROM users WHERE id = ${1}`;

// MySQL（显式指定连接字符串）
const mysql = new SQL("mysql://user:pass@localhost:3306/mydb");
const mysqlUsers = await mysql`SELECT * FROM users LIMIT 10`;
```

### 对象存储

Bun 内置了 **S3 客户端**（v1.2+），上传下载文件、生成预签名 URL、配置存储类（GLACIER_IR 等）全部搞定：

```typescript
import { s3, write } from "bun";

// 创建一个指向 S3 文件的"懒引用"（此时不发起网络请求）
const fileRef = s3.file("my-bucket/hello.txt");

// 上传文件
await write(fileRef, "Hello World");

// 下载文件（以文本形式）
const content = await fileRef.text();

// 生成预签名 URL，有效期 1 天
const url = fileRef.presign({ expiresIn: 60 * 60 * 24 });
```

### WebSocket 服务器

Bun 内置了 WebSocket 服务器，基于 **uWebSockets** 实现，性能比 Node.js + `ws` 库**快 7 倍**！

```typescript
Bun.serve({
  fetch(req, server) {
    server.upgrade(req); // 升级为 WebSocket
    return;
  },
  websocket: {
    open(ws) { console.log("连接来了！"); },
    message(ws, msg) { ws.send(msg); },
  },
});
```

### 单文件可执行文件

Bun 可以把应用打包成**单个二进制可执行文件**，直接拷贝到服务器上运行，不需要 Node.js，不需要任何运行时——Bun 本身就是运行时。

```bash
bun build --target=bun --outfile myapp myapp.ts
./myapp  # 直接运行！
```

### 加密密钥存储

Bun 内置了**加密密钥安全存储**（Encrypted Secrets Storage），再也不用把密钥硬编码在代码里了。

---

## 3.3 运行时：替代 Node.js

Bun 的运行时是它最核心的部分。

### 直接运行 TS/JS 文件

不需要编译，不需要配置，直接跑：

```bash
bun run index.ts
bun run index.tsx
bun index.js  # 裸命令，等价于 bun run
```

### 内置 Transpiler

Bun 自带了一个**超快的转译器**（Transpiler），在你运行代码之前，自动把 TypeScript 转成 JavaScript、把 JSX 转成 React.createElement。

你感知不到这个过程——它发生在后台，瞬间完成。

```typescript
// index.ts - TypeScript + JSX，Bun 直接运行
import React from "react";

interface Props {
  name: string;
}

const greet = (name: string): string => {
  return `Hello, ${name}!`;
};

const element = <h1>{greet("Bun")}</h1>;
console.log(element);
```

### 内置 .env 加载

Bun 自动加载 `.env` 文件，不需要额外安装 `dotenv`：

```bash
# .env 文件
DB_PASSWORD=secret123
API_KEY=hello-world

# 代码中直接用（无需任何 import！）
console.log(process.env.DB_PASSWORD); // secret123
```

### 内置 HTTP 服务器（Bun.serve）

Bun 内置了高性能 HTTP 服务器，直接使用 `Bun.serve()` 创建，无需任何第三方依赖：

```typescript
Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("Hello from Bun!");
  },
});
// 运行：bun run server.ts
// 访问：http://localhost:3000
```

### 内置 WebSocket 服务器

`Bun.serve` 的 `websocket` 配置项让你快速搭建 WebSocket 服务，支持 `open`、`message`、`close` 等生命周期钩子：

```typescript
Bun.serve({
  fetch(req, server) {
    // 如果是 WebSocket 请求，升级它
    if (server.upgrade(req)) return;
    return new Response("这不是 WebSocket");
  },
  websocket: {
    open(ws) { console.log("新连接:", ws.remoteAddress); },
    message(ws, msg) { ws.send(`你发了: ${msg}`); },
    close(ws) { console.log("连接断开"); },
  },
});
```

### 内置 Shell

Bun 的 `$` 语法让你在 JavaScript 里写 Shell 脚本：

```typescript
import { $ } from "bun";

const result = await $`ls -la`.text();
console.log(result);
```

### 内置 FFI

FFI（Foreign Function Interface）让你在 JavaScript 里直接调用 C 类库：

```typescript
import { dlopen } from "bun:ffi";

// 加载一个 C 库（Linux 示例，macOS 上是 libSystem.dylib，Windows 上是 libm.lib）
const lib = dlopen("libm.so.6", {
  abs: { returns: "int", args: ["int"] },
});

console.log(lib.symbols.abs(-42)); // 42
```

### 内置文件监听与热重载

`--watch` 模式让 Bun 自动监听文件变化，重启服务：

```bash
bun --watch run server.ts
# 修改 server.ts 后，Bun 自动重启
```

### 常用文件操作 API

Bun 的文件 API 比 Node.js 的 `fs` 模块更快：

```typescript
// 读取文件
const content = Bun.file("data.txt").text();
const json = Bun.file("data.json").json();

// 写入文件
await Bun.write("output.txt", "Hello Bun!");

// 高性能文件复制
await Bun.write("dest.txt", Bun.file("source.txt"));
```

---

## 3.4 打包器：替代 webpack / Vite / esbuild

Bun 的内置打包器适合轻量到中型打包场景。

### Bun.build() JavaScript API

```typescript
import { build } from "bun";

await build({
  entrypoints: ["./src/index.tsx"],
  outdir: "./dist",
  target: "browser",
  minify: true,
});
```

### CLI 方式

```bash
bun build ./src/index.tsx --outdir=dist --target=browser
```

### 代码分割（Code Splitting）

```bash
bun build ./src/index.tsx --outdir=dist --splitting
```

### Tree Shaking

Bun 自动删除没有用到的代码，减少包体积：

```bash
bun build ./src/index.tsx --outdir=dist --minify
```

### 多平台目标

```bash
# 浏览器
bun build ./src/app.ts --target=browser --outdir=dist

# Node.js
bun build ./src/app.ts --target=node --outdir=dist

# Bun 运行时
bun build ./src/app.ts --target=bun --outdir=dist
```

### HTML 入口打包

Bun 可以直接打包包含 HTML 的项目：

```bash
bun build ./public/index.html --outdir=dist
```

Bun 会自动处理 HTML 里引用的 JS/CSS/图片资源。

### 单文件可执行文件

```bash
bun build --target=bun --outfile myapp ./myapp.ts
./myapp  # 直接运行，不需要 Bun 运行时！
```

---

## 3.5 测试框架：替代 Jest / Vitest

Bun 的测试框架 `bun test` 完全兼容 Jest API：

```typescript
import { test, expect, describe } from "bun:test";

describe("数学运算", () => {
  test("加法", () => {
    expect(1 + 1).toBe(2);
  });

  test("乘法", () => {
    expect(3 * 4).toBe(12);
  });
});
```

运行测试：

```bash
bun test
```

### 并发测试

```typescript
test("并发测试", async () => {
  // 多个测试并行执行
}, { concurrent: true });
```

### Mock 函数

```typescript
import { mock } from "bun:test";

test("Mock 函数", () => {
  const fn = mock(() => 42);
  expect(fn()).toBe(42);
  expect(fn).toHaveBeenCalled();
});
```

### 覆盖率报告

```bash
bun test --coverage
```

---

## 3.6 内置 API 与工具

### bun init - 快速初始化项目

```bash
bun init              # 空白项目
bun init --react      # React 项目
bun init --library    # 类库项目
```

### bun fmt - 代码格式化

```bash
bun fmt              # 格式化当前目录
bun fmt ./src         # 格式化指定目录
```

### bun lint - 代码检查

```bash
bun lint
```

---

## 3.7 内置工具（Builtin Utilities）

### 密码与哈希 API

```typescript
import { hash, verify } from "bun:password";

const hash1 = await hash("my-secret-password");
// $argon2id$v=19...

const isValid = await verify(hash1, "my-secret-password");
console.log(isValid); // true
```

### String Width API

```typescript
import { stringWidth } from "bun";

console.log(stringWidth("Hello"));    // 5
console.log(stringWidth("你好"));      // 4（中文字符宽度为2）
console.log(stringWidth("🍌"));         // 2（emoji宽度为2）
```

### CSS 颜色转换 API

```typescript
import { cssColor } from "bun";

const colorObj = cssColor("#ff0000");
console.log(colorObj); // { r: 255, g: 0, b: 0, a: 1 }
```

---

## 3.8 脚本工具

### 跨平台 Shell 脚本

```typescript
import { $ } from "bun";

await $`mkdir -p dist && cp src/* dist/`;
await $`git status`;
```

---

## 3.9 运行时与打包器的内置 Loader

Bun 自动识别文件扩展名来决定用什么"加载器"处理文件。

| 扩展名 | Loader | 说明 |
|---|---|---|
| `.ts` / `.mts` / `.cts` | ts | TypeScript（转译 + 类型剥离） |
| `.tsx` | tsx | TypeScript + JSX |
| `.js` / `.mjs` | esm | JavaScript（作为 ES Module） |
| `.jsx` | jsx | JavaScript + JSX |
| `.cjs` | cjs | JavaScript（作为 CommonJS） |
| `.json` | json | JSON，导入时作为对象 |
| `.jsonc` | jsonc | JSON with Comments |
| `.toml` | toml | TOML |
| `.yaml` / `.yml` | yaml | YAML |
| `.css` | css | CSS |
| `.html` | html | HTML 及资产打包 |
| `.wasm` | wasm | WebAssembly |
| `.sh` | sh | Bun Shell 脚本 |

### 自定义 Loader

```bash
bun run --loader .myext:myLoader ./file.myext
```

---

## 本章小结

本章系统介绍了 Bun 的用途和核心内置能力。

**设计目标**上：Bun 追求速度、TypeScript 开箱即用、ESM/CommonJS 兼容、Web 标准 API 原生实现、Node.js 高度兼容。

**内置核心能力**上：Bun 内置了 SQLite（`bun:sqlite`）、PostgreSQL/MySQL（`sql` 统一 API，v1.3+）、S3（`s3.file` + `write`）、Redis（`redis` 全局单例，v1.3+）、WebSocket、单文件打包等重量级功能，全部不需要 npm install。MariaDB 暂时还没内置，老老实实用 `mysql2` 包吧。

**运行时**方面：Bun 可以直接运行 TS/JS 文件，内置 Transpiler、.env 加载、HTTP 服务器、WebSocket、Shell、FFI、文件操作等丰富能力。

**打包器**方面：`bun build` 适合轻量打包场景，支持代码分割、Tree Shaking、多平台目标、HTML 入口打包、单文件可执行文件。

**测试框架**：`bun test` 兼容 Jest API，支持并发测试、Mock、覆盖率报告。

> 🎯 总结一句话：**装一个 Bun，省一堆包。**
