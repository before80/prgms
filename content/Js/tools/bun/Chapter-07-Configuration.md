+++
title = "第七章 相关配置"
weight = 70
date = "2026-03-29T14:36:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第七章　相关配置

> 🤓 本章聊聊 Bun 的各种"花式配置"——从配置文件到环境变量，从国内镜像加速到 IDE 配合，手把手把你打造成配置大师。

## 7.1 bunfig.toml（全局配置文件）

如果说 Bun 是一个狂飙的老司机，那 `bunfig.toml` 就是它的**外挂副驾驶**——全局配置，想怎么调就怎么调。

它长得有点像 `.npmrc` 和 `tsconfig.json` 的远房亲戚，但脾气比它们都好使。

### 文件位置

- **全局**：~/.bunfig.toml（推荐，大多数人装一次就够了）
- **项目级**：./bunfig.toml（项目专属，千人千面）
- **指定路径**：通过命令行 `-c myconfig.toml` 指定，或者配合环境变量（见后文）

### 常用配置项

```toml
# bunfig.toml

[install]
# npm 镜像源（解决国内下载慢的问题）
registry = "https://registry.npmmirror.com"

# 生产模式（跳过 devDependencies）
production = false

# 自动安装策略
# auto      → 找不到就自动安装（默认）
# fallback  → 优先用缓存，缓存没有再装
# force     → 强制重新安装，不管缓存
# none      → 离线模式，装不了就摆烂
auto = "fallback"

# 跳过 scripts（安装前后自动执行的脚本）
ignore-scripts = false

# 安装可选依赖（optionalDependencies）
optional = true

[install.cache]
# 缓存目录
dir = "~/.bun/cache"
```

### 国内镜像配置

```toml
# bunfig.toml（解决 npm 安装慢的问题）
[install]
registry = "https://registry.npmmirror.com"
```

配置后，所有 `bun install` 命令都会使用镜像源，速度飙升！🚀

### 离线模式

```toml
[install]
# 强制离线模式，找不到包也绝不联网
auto = "none"
```

### bunfig vs 环境变量优先级

环境变量优先级更高。如果同时配置了 `bunfig.toml` 和 `BUN_CONFIG_REGISTRY`，**环境变量会覆盖配置文件**。

```bash
# 环境变量覆盖 bunfig.toml
BUN_CONFIG_REGISTRY=https://registry.npmmirror.com bun install
```

### 日志级别

```toml
# 控制 bun 的输出详细程度
logLevel = "warning"  # debug | info | warning | error
```

---

## 7.2 bun.lockb（锁文件）

Bun 的锁文件叫 `bun.lockb`，是一个**二进制格式**的文件——对，你没看错，不是 JSON/YAML， Bun 就喜欢搞点不一样的。

### 为什么要用锁文件？

想象一下：团队五个人，同样的 `package.json`，结果装了五个不同版本的 `lodash`——那画面太美我不敢看。锁文件就是为了终结这种"玄学 bug"而生的。

### 锁文件格式说明

`bun.lockb` 是二进制格式，**不要手动编辑**！手贱改坏了怎么办？淡定，删掉重装就行：

```bash
rm bun.lockb
bun install  # 重新生成
```

### 与其他锁文件的区别

| 锁文件 | 格式 | 可读性 |
|---|---|---|
| bun.lockb | 二进制 | ❌ 别碰 |
| package-lock.json | JSON | ✅ 可读 |
| yarn.lock | YAML | ✅ 可读 |
| pnpm-lock.yaml | YAML | ✅ 可读 |

### 提交到 Git

**锁文件一定要提交到 Git**！否则团队其他成员拉了代码，`bun install` 装出来的包版本可能和你不一致，"在我电脑上是好的"这种经典剧情又要上演了。

---

## 7.3 package.json 中的 Bun 配置

### overrides（依赖覆盖）

强制统一依赖树中某个包的版本，解决传递依赖冲突的利器：

```json
{
  "dependencies": {
    "lodash": "^4.17.21"
  },
  "overrides": {
    "lodash": "^4.17.21"  // 所有依赖树里的 lodash 都用这个版本
  }
}
```

> 💡 `overrides` 在 Bun、pnpm 和 npm 7+ 中都支持。

### bun 特定字段

```json
{
  "scripts": {
    "install": "bun install",       // 安装时自动运行
    "prepack": "bun run build",     // npm pack 前自动运行
    "postpack": "bun run clean"     // npm pack 后自动运行
  }
}
```

### workspace / monorepo 配置

```json
{
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

```bash
# 工作区根目录运行，一键安装所有 workspace 包
bun install
```

---

## 7.4 环境变量配置

### 常用环境变量

| 变量 | 说明 | 示例 |
|---|---|---|
| `BUN_INSTALL` | Bun 安装路径 | `~/.bun` |
| `BUN_ENV` | 环境标识 | `development` / `production` |
| `BUN_CONFIG_REGISTRY` | 镜像源 | `https://registry.npmmirror.com` |
| `BUN_CACHE_DIR` | 缓存目录 | `~/.bun/cache` |
| `HTTP_PROXY` | HTTP 代理 | `http://localhost:7890` |
| `HTTPS_PROXY` | HTTPS 代理 | `http://localhost:7890` |

### BUN_ENV

这个变量决定了 Bun 运行时的心境——是"认真打工"还是"摸鱼划水"：

```typescript
// 根据环境加载不同配置
if (process.env.BUN_ENV === "production") {
  console.log("生产环境模式！");
} else {
  console.log("开发环境模式！");
}
```

```bash
BUN_ENV=production bun run server.ts
```

---

## 7.5 国内镜像加速 🇨🇳

好消息：配置很简单。坏消息：你得先知道配哪里。

### npmmirror（原淘宝镜像）

一行配置，告别龟速下载：

```toml
# ~/.bunfig.toml
[install]
registry = "https://registry.npmmirror.com"
```

或者直接写进 shell 配置：

```bash
echo 'export BUN_CONFIG_REGISTRY=https://registry.npmmirror.com' >> ~/.bashrc
source ~/.bashrc
```

### 临时指定镜像

不想改全局配置？一次性的，用命令行参数：

```bash
bun install --registry https://registry.npmmirror.com
```

### 不同包管理器共用镜像的坑

npm、pnpm、Bun 三兄弟的镜像配置是**各自独立的**：

- npm → `~/.npmrc`
- pnpm → `~/.config/pnpm/npmrc`（默认）
- Bun → `~/.bunfig.toml`

光给一个工具配了镜像其他工具还是原装的龟速，等于没配。

---

## 7.6 IDE 与编辑器支持

好马配好鞍，好代码配好 IDE。

### VS Code

VS Code 对 Bun 的支持非常贴心：

1. **Bun Language Features**：语法高亮、智能补全、类型提示全安排
2. **Bun Debugger**：断点调试，想停哪停哪

去 VS Code 扩展市场搜 "Bun"，安装官方插件就行。

### WebStorm

WebStorm **原生支持** Bun，2024.1+ 版本无需安装任何插件，开箱即用。

### Neovim

```lua
-- init.vim 或 init.lua
local lspconfig = require("lspconfig")

lspconfig.bun.setup({})
```

配合 `nvim-lspconfig` 使用，Bun 的 LSP 服务自动启动。

---

## 7.7 与 Node.js 共存配置

好消息：Bun 和 Node.js 可以**和平共处**，不需要二选一。

### PATH 优先级

谁先被找到，取决于 PATH 里的顺序：

```bash
# 查看当前 bun 的路径
which bun
# /home/user/.bun/bin/bun

# 查看 node 的路径
which node
# /usr/local/bin/node
```

想让 `bun` 优先于系统的 `node`？把 bun 的路径放 PATH 前面：

```bash
# ~/.bashrc 或 ~/.zshrc
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

> ⚠️ 顺手的事，但要注意——如果你有其他工具（如 fnm、nvm）也在管 node，别让它们的 PATH 配置互相打架。

### CI/CD 中切换

```yaml
# GitHub Actions 示例
- name: Install Bun
  uses: oven-sh/setup-bun@v1

- name: Install dependencies
  run: bun install

- name: Run tests
  run: bun test
```

官方 Action：[oven-sh/setup-bun](https://github.com/marketplace/actions/setup-bun)

---

## 7.8 诊断工具

Bun 自带了一套"体检套餐"，帮你快速定位环境问题。

### bun doctor - 环境自检

```bash
bun doctor

# 真实输出示例（来自 bun v1.x）：
# Checking for Bun...      ✓ Bun is installed
# Checking for node...     ✓ node is installed
# Checking for npm...      ✓ npm is installed
# Checking environment variables... ✓
# Bun can find "npm"       ✓
# Bun can find "node"      ✓
```

### bun --version - 查看版本

```bash
bun --version
# 1.3.11
```

### bun pm - 包管理器工具集

```bash
bun pm ls     # 列出已安装的包
bun pm bin    # 列出 bun 安装目录
bun pm cache dir  # 显示缓存目录路径
```

### bun info - 查看包信息

```bash
bun info react
# react@18.2.0
# Latest: 18.3.1
# Description: React is a JavaScript library for building user interfaces.
```

---

## 本章小结

本章介绍了 Bun 的配置体系，帮你从"会用"进化到"会配"。

**bunfig.toml** 是 Bun 的全局配置文件，可配置镜像源、缓存目录、自动安装行为、日志级别等。国内用户最重要的配置就是镜像——配完你就知道什么叫"飞一般的感觉"。**bun.lockb** 是二进制锁文件，必须提交到 Git，但不要手贱去编辑它。**package.json 中的 Bun 配置**：overrides 用于强制依赖版本，scripts 中可以指定 bun 命令，workspaces 配置 monorepo。**环境变量**：BUN_INSTALL、BUN_ENV、BUN_CONFIG_REGISTRY、BUN_CACHE_DIR 等都是高频使用的配置项。**国内镜像**：bunfig.toml 中配一行 registry 就够了。**IDE 支持**：VS Code 装插件、WebStorm 原生支持、Neovim 配 LSP，各取所需。**与 Node.js 共存**：两者可以同时装，通过 PATH 决定谁出场。**诊断工具**：`bun doctor` 跑一遍，环境有没有问题一目了然。

配置好的 Bun，配上国内镜像——这时候你再回头看 npm 的速度，就像在老式电脑上跑 VS Code。差距，就是这么残酷。
