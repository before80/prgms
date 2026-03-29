+++
title = "第六章 需要注意哪些"
weight = 60
date = "2026-03-29T14:36:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第六章　需要注意哪些

> 🔔 **阅读警告**：Bun 虽然很香，但它不是万能药。在把它扔进生产环境之前，请先把这些坑看清楚——不然你会在凌晨两点哭着找 Node.js。
{: .info }

## 6.1 Node.js 兼容性

Bun 的目标是 100% 兼容 Node.js，但"仍在进行中"这句话翻译一下就是：**基本能用，但别指望它完美得像你理想中的另一半**。

### 哪些兼容，哪些不兼容？

**兼容良好**的部分（放心用）：
- 核心模块：`fs`、`path`、`crypto`、`stream`、`buffer`、`os`、`events`、`url`、`querystring`、`http`、`https`、`net`、`tls` 等——基本上你常用的那些都在
- Web 标准 API：`fetch`、`Response`、`Request`、`Headers`、`URL`、`URLSearchParams` 等——现代 Web API 全家桶
- npm 生态：大部分常用 npm 包能直接在 Bun 里跑起来，不用改一行代码

**仍有问题的**部分（踩坑预警 🚨）：
- Node.js 原生模块（`.node` 文件）——**不支持**，这是大坑，后文细说
- 部分 C++ 编写的原生 addon——编译好的二进制扩展，基本没戏
- 一些深度依赖 Node.js 内部实现的包——比如某些用了 `vm` 模块黑科技的

### 检测兼容性的方法

```bash
# 在项目目录运行这三连，基本能覆盖大部分问题
bun install
bun run  # 试试能不能正常跑起来
bun test  # 跑测试，看有没有报错
```

如果你遇到 `Module not found` 或者奇怪的运行时错误，先去 [Bun 的 GitHub Issues](https://github.com/oven-sh/bun/issues) 搜一下——大概率不是只有你一个人踩坑。如果没找到，恭喜你发现了一个新 bug，记得提个 issue 造福后人。

---

## 6.2 原生模块（Native Addons）

这是 Bun 和 Node.js 之间**最大的坑**，没有之一。

> 💡 **一个形象的比喻**：把 Bun 想象成一家新开的网红餐厅，菜品新鲜上菜快，但它不卖酒——因为它没有酒牌。`.node` 文件就是酒，而 Bun 还没拿到那张牌。

### 什么是 Native Addons？

Native Addons 是用 C/C++ 编写、编译成 `.node` 文件的 Node.js 扩展。一些追求极致性能或需要调用系统底层能力的库会用这种方式实现：

- 图像处理：`sharp`（高性能图片处理的扛把子）
- 数据库驱动：某些数据库的官方 Node.js 驱动
- 加密计算：`node-forge` 等用了原生加密库的

### Bun 不支持 .node 文件

**Bun 目前无法加载 `.node` 文件。**

这意味着如果你项目里用到了 `sharp` 这种 Native Addons 库，直接用 Bun 运行会爆炸。

### 解决方案

**1. 找替代品**：很多库有纯 JavaScript 或 WebAssembly 版本

| 原方案 | 替代方案 | 说明 |
|--------|----------|------|
| `sharp` | `jimp` 或 `squoosh` | 纯 JS/WASM 实现（jimp 仍在活跃维护） |
| `node-sass`（已废弃） | `sass`（Dart Sass） | 纯 Dart 实现，官方主推 |
| `better-sqlite3` | `bun:sqlite` | 内置，性能反而更强 |

**2. 用 Bun 的内置功能**：Bun 内置了很多常用功能，原生就能打：

```typescript
// 内置 SQLite，不用装任何包
import { Database } from "bun:sqlite";
const db = new Database("app.db");

// 内置 fetch，HTTP 客户端全省了
const res = await fetch("https://api.example.com/data");

// 内置压缩，一条语句搞定
new ReadableStream(data).pipeThrough(new CompressionStream("gzip"));
```

**3. FFI**：对于简单的 C 类库调用，可以用 Bun 的 FFI

> ⚠️ **注意**：`bun:ffi` 目前是实验性（experimental）功能，不建议在生产环境使用。
{: .warning }

```typescript
import { dlopen, FFIType, suffix } from "bun:ffi";

// 以调用 sqlite3 为例（示例代码，展示 FFI 调用语法）
// 注意：Linux/macOS 通常预装了 libsqlite3，但 Windows 需要自行安装 sqlite3.dll
const { symbols: { sqlite3_libversion } } = dlopen(
  `libsqlite3.${suffix}`,
  {
    sqlite3_libversion: {
      args: [],
      returns: FFIType.cstring,
    },
  },
);
console.log(`SQLite 版本：${sqlite3_libversion()}`);
```

**4. 继续用 Node.js**：如果这个包对你的业务至关重要，一时半会找不到替代，那——老实回去用 Node.js 吧。Bun 虽然快，但还没快到让你损失业务的地步。

---

## 6.3 npm 包兼容性

好消息：大部分 npm 包能直接在 Bun 里运行，不用魔改。

坏消息："大部分"不等于"全部"。

### 常见问题类型

1. **依赖 .node 文件的包**：上文提到的坑，绕不过去
2. **依赖特定 Node.js 内部 API 的包**：某些包用了 Node.js 内部实现，比如 `node:internal` 下面的黑科技
3. **Bun 和 Node.js 行为细微差异**：比如 `Buffer` vs `Uint8Array` 的处理差异、某些边界情况的行为不一致

### polyfill 策略

如果某个包用了 Bun 不支持的 API，可以尝试 polyfill 填补：

```typescript
// global.d.ts - 添加缺失的类型声明
declare module "some-node-api" {
  export const someAPI: any;
}
```

不过说实话，polyfill 是门玄学——能补上的类型声明只是表面功夫，真正运行时调用的 native 函数你是补不了的。所以最靠谱的还是：**换个包**。

### workspace 场景

在 monorepo（多包项目）里，Bun 对 workspace 的支持非常丝滑：

```json
// package.json
{
  "workspaces": ["packages/*"]
}
```

```bash
bun install  # 自动安装所有 workspace 包，比 npm/yarn 快好几个量级
```

---

## 6.4 生产环境成熟度

### Bun vs Node.js 生产验证

Node.js 是久经沙场的老将，十多年生产环境验证，Facebook、Google、Netflix、Uber 等顶级公司都在用。Bun 则是个意气风发的年轻人（2022 年发布），正在快速成长中。

目前已知的生产使用案例包括 Midjourney（AI 图像生成）、Shopify（电商平台后端服务）以及其他一些中小型项目。不过这些信息主要来自公开资料和社区讨论，**未全部获得官方确认**——建议以各公司官方技术博客或 Bun 官方披露为准，自行核实后再用于正式评估。

> 📝 **说明**：以上为公开资料整理，**无法完全保证准确性**——如有出入，欢迎指正。建议在评估时优先参考官方信源。
{: .info }

Bun 在生产环境的表现**已经相当稳定**，但如果你的项目极其关键（停了就是钱的损失），第一次迁移建议先在非核心业务上试点，稳了再全面铺开。

---

## 6.5 Windows 平台

Bun 对 Windows 的支持在稳步推进中，目前 v1.x 版本已经可以正常在 Windows 上跑。不过还是有几个注意点：

### Windows 10 版本要求

- **最低要求**：Windows 10 版本 **1809**（2018 年 10 月发布，也叫 Windows 10 October 2018 Update）
- 低于 1809 的 Windows 10 无法运行 Bun——系统会直接拒绝你，连报错的机会都不给
- Windows 11 当然也没问题，放心用

### 路径处理差异

```typescript
// Linux/macOS 风格路径（写法）
const path = "/tmp/file.txt";

// Windows 呢？Bun 会自动处理 POSIX 路径到 Windows 路径的转换
// 但如果你手动拼接路径在 Windows 上很容易出事，建议：
import { join } from "path";

const filePath = join(__dirname, "data.txt"); // 跨平台兼容，乖就用这个
```

### 行尾符差异（CRLF vs LF）

Windows 默认用 **CRLF**（`\r\n`），Linux/macOS 用 **LF**（`\n`）。这个差异会导致一些诡异的 bug，比如某行代码在本地跑得好好的，上了 CI 就炸了。

```bash
# 建议在项目根目录添加 .gitattributes 文件，让 Git 自动处理：
*.ts text eol=lf
*.tsx text eol=lf
*.js text eol=lf
*.json text eol=lf
*.md text eol=lf
```

### Shell 脚本跨平台

Bun 的 `$` 模板字符串语法是跨平台的：

```typescript
import { $ } from "bun";

// 这个在 Windows / Linux / macOS 都能正常工作
// 再也不用担心队友 Windows 环境跑不起来
await $`mkdir -p dist && cp src/* dist/`;
```

---

## 6.6 调试与错误排查

调试工具不给力，bug 能让你掉一把头发。还好 Bun 配套的工具链还算完整。

### 错误堆栈与 Node.js 的差异

Bun 的错误堆栈格式和 Node.js 略有不同。如果你习惯了 Node.js 的报错风格，刚转 Bun 可能需要适应一下：

```typescript
try {
  const data = JSON.parse("这根本不是 JSON{");
} catch (e) {
  console.error((e as Error).message);
  // Bun 的错误信息通常会包含更详细的上下文
}
```

### VS Code 调试配置

安装 VS Code 扩展 **"Bun"**（官方出品），会自动配置好调试环境：

```json
// .vscode/launch.json（扩展安装后通常会自动生成）
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "bun",
      "request": "launch",
      "name": "Debug Bun",
      "program": "${workspaceFolder}/src/index.ts",
      "breakpoints": ["**/*.ts"]
    }
  ]
}
```

有了这个，你就可以在 VS Code 里断点调试 Bun 代码了——单步执行、变量查看，该有的都有。

### bun --inspect 调试

如果你喜欢命令行风格，可以用 `--inspect` 启动 Bun 的调试模式：

```bash
# 启动调试模式，Bun 会在 localhost:9229 暴露调试端点
bun --inspect run server.ts
```

然后用 Chrome DevTools（或任何支持 Node.js 调试协议的 IDE）连接即可调试。

### bun doctor - 自检工具

`bun doctor` 是你的好帮手，能快速排查常见的环境问题：

```bash
bun doctor

# 输出示例：
# Checking Bun version...        ✓ v1.x.x
# Checking node_modules...       ✓ installed
# Checking registry...          ✓ https://registry.npmjs.org
# Checking cache dir...         ✓ ~/.bun/install/cache
# Checking platform...          ✓ Windows 10 (1809+)
```

如果你的环境有问题，`bun doctor` 通常能告诉你问题出在哪一行。

---

## 本章小结

本章介绍了 Bun 使用过程中需要注意的几个关键问题。

**Node.js 兼容性**：Bun 目标是 100% 兼容，目前大部分 API 和 npm 包兼容良好，但 `.node` 原生模块不支持。**Native Addons**：这是 Bun 和 Node.js 之间最大的坑——涉及 `.node` 文件的包需要找替代品（`bun:sqlite` 内置了 SQLite 支持）或暂时用 Node.js。**npm 包兼容性**：大部分正常，少数依赖 Node.js 内部实现的包可能有问题。**生产环境成熟度**：Bun 已经足够成熟，部分公司已有生产使用案例（具体以官方披露为准），但如果是核心业务建议先试点。**Windows 平台**：v1.x 相对稳定，最低要求 Windows 10 版本 1809，注意路径和行尾符差异。**调试**：VS Code + Bun 扩展、`bun --inspect`、`bun doctor` 是主要调试工具。

总的来说，Bun 的局限主要集中在 **Native Addons** 这一点上，其他方面的兼容性已经相当不错。了解这些局限，能帮助你在迁移项目时做出更明智的决策——而不是在凌晨两点发现 `sharp` 跑不起来之后，对着屏幕发出灵魂拷问。

---

> 📚 **相关资源**
> - [Bun 官方文档](https://bun.sh/docs)
> - [Bun GitHub Issues](https://github.com/oven-sh/bun/issues) —— 遇到 bug 先来这里搜
> - [Bun Discord 社区](https://discord.gg/bun) —— 活跃的社区，有问题可以提问
