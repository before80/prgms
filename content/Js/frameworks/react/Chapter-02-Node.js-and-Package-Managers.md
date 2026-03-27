+++
title = "第2章 Node.js与包管理器"
weight = 20
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-02 - Node.js 与包管理器

## 2.1 Node.js 简介

> 你有没有想过这样一个问题：JavaScript 这门语言，不是只能在浏览器里运行吗？它是怎么跑到服务器上去的？Node.js 就是这个"魔法"的化身——它把 Chrome 浏览器的 V8 引擎单独拎出来，放到一个没有浏览器的环境里运行，于是 JavaScript 第一次能够在服务器端大展拳脚。

### 2.1.1 Node.js 的安装：LTS 与 Current 版本的选择

Node.js 的安装有两种版本路线，像两条不同的登山道——一条稳定但风景一般，一条时髦但可能有坑。

- **LTS 版本**（Long Term Support，长期支持版）：适合绝大多数人，稳定、可靠、社区支持好，企业用这个。版本号比如 `20.x.x`、`22.x.x`
- **Current 版本**（当前最新版）：最新功能都在这儿，但可能有些不稳定，适合爱折腾的极客。版本号通常是 `21.x.x`、`23.x.x`

对于 React 开发来说，**直接选 LTS 版本**，稳如老狗，不翻车。

**安装方法（Windows / macOS / Linux 全覆盖）：**

**方法一：官网下载安装包（适合 Windows 用户）**

去 [nodejs.org](https://nodejs.org)，你会看到两个大按钮：
- **LTS**（推荐大多数用户使用）✅
- **Current**（最新功能，但可能不稳定）

点 LTS，下载 `.msi` 安装包，一路下一步-next-下一步-next，就装好了。

**方法二：命令行安装（适合所有平台，推荐开发者使用）**

```bash
# Windows (用管理员打开 PowerShell)
winget install OpenJS.NodeJS.LTS

# macOS (用 Homebrew)
brew install node@lts

# Linux (用 nvm 安装，最灵活，后面会讲)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

### 2.1.2 nvm（Node Version Manager）：多版本管理

**nvm** 是什么？它是 Node.js 的"时光机"和"分身术"——让你在同一台电脑上同时安装和切换多个 Node.js 版本。

> 场景模拟：你同时在维护两个项目：项目 A 用 Node 16，项目 B 用 Node 22。没有 nvm？你得每次手动卸载重装，烦死。有了 nvm？一个命令切换版本，丝滑流畅。

**安装 nvm（以 macOS/Linux 为例，Windows 用户用 nvm-windows）：**

```bash
# macOS / Linux 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 安装完成后，重新加载终端配置文件
source ~/.bashrc  # 如果你用的是 bash
source ~/.zshrc   # 如果你用的是 zsh（macOS 默认就是这个）
```

**nvm 常用命令：**

```bash
# 安装最新的 LTS 版本
nvm install --lts

# 安装指定版本
nvm install 20

# 查看已经安装的所有版本
nvm ls
# 输出示例：
#        v18.17.0
#        v20.14.0
# ->     v22.14.0
#         system
#    # -> 表示当前正在使用的版本

# 切换到指定版本（临时切换，关闭终端就恢复）
nvm use 20

# 设置默认版本（永久生效）
nvm alias default 20

# 卸载某个版本
nvm uninstall 16
```

> 💡 小技巧：Windows 用户请搜索 `nvm-windows` 下载安装，功能和 macOS 版的 nvm 类似。安装的时候记得用**管理员身份**运行安装程序，不然可能会遇到权限问题。

### 2.1.3 验证安装：node -v / npm -v

安装完 Node.js 之后，我们来验证一下是否安装成功！

**打开你的终端（Terminal）：**

- **Windows**：按 `Win + X`，选择"终端"或"PowerShell"
- **macOS**：按 `Command + Space`，搜索"终端"
- **Linux**：按 `Ctrl + Alt + T`

然后分别运行以下两条命令：

```bash
# 查看 Node.js 版本
node -v
# 打印结果示例：v20.14.0

# 查看 npm 版本（Node.js 自带的包管理器，后面会重点讲）
npm -v
# 打印结果示例：10.8.2
```

如果两条命令都输出了版本号（比如 `v20.14.0` 和 `10.8.2`），恭喜你！Node.js 安装成功！🎉

> 常见坑：如果提示"node 不是内部或外部命令"，说明安装没成功或者环境变量没配置好。解决方法：重启终端/电脑，或者手动把 Node.js 的路径加到系统 PATH 里。

---

## 2.2 npm 详解

npm 是 **Node Package Manager** 的缩写，中文名叫"节点包管理器"。你可以把它理解为 JavaScript 世界的"应用商店"——它托管了全世界开发者写的各种工具库，你只需要一个命令，就能把这些库下载到自己的项目里。

> 搞笑比喻：没有 npm 之前，JavaScript 开发者就像要去图书馆借书，得先自己去找、自己搬回来。有了 npm，就像有了外卖软件——你想吃什么，点一下，就给你送到家门口，还帮你拆好包装！

### 2.2.1 npm init：初始化项目

当你开始一个新项目时，第一步就是用 `npm init` 来"初始化"这个项目——相当于给它办一张身份证，告诉 npm："这个文件夹是我的地盘了。"

```bash
# 进入你的项目文件夹
cd my-react-project

# 初始化项目（会生成 package.json）
npm init

# 或者一步到位，自动填写默认值（不询问）
npm init -y
```

运行之后，你会在当前文件夹里发现一个 `package.json` 文件，它长这样：

```json
{
  "name": "my-react-project",   // 项目名称
  "version": "1.0.0",            // 版本号（遵循语义化版本 SemVer）
  "description": "我的第一个 React 项目",  // 项目描述
  "main": "index.js",            // 入口文件
  "scripts": {                   // 脚本命令（重点！）
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

> 📝 补充：如果你用 `npm init -y`，所有的选项都用默认值填充。后续你可以随时手动修改 `package.json` 文件，或者用 `npm config set` 命令来修改某个字段。

### 2.2.2 npm install / --save / --save-dev：安装依赖

这是 npm 最最最常用的命令！安装一个第三方包，就像在手机上点外卖一样简单。

```bash
# 安装一个包（例如：React）
npm install react
# 安装结果示例：added 1 package in 2s

# 安装并记录到 package.json 的 dependencies（生产依赖）
# 相当于 npm install react --save
npm install react
# dependencies 里的包是项目运行时需要的依赖

# 安装并记录到 package.json 的 devDependencies（开发依赖）
# 相当于 npm install react --save-dev
npm install --save-dev eslint
# devDependencies 里的包只在开发时需要，打包上线时不需要

# 一次性安装多个包
npm install react react-dom axios lodash

# 安装指定版本的包
npm install react@18.2.0  # 安装 React 18.2.0 版本
npm install react@^18.0.0  # 安装 React 18.x.x 中的最新版本（^表示可上浮）
npm install react@~18.2.0  # 安装 React 18.2.x 中的最新版本（~表示可小幅上浮）
```

**dependencies vs devDependencies 有什么区别？**

用一个生活中的例子来解释：
- **dependencies**（生产依赖）：就像盖房子用的砖头、水泥——房子盖好后，这些东西还留在房子里，是必需品。React、Vue、Axios 等属于这类。
- **devDependencies**（开发依赖）：就像盖房子用的脚手架、安全帽——房子盖好后，这些东西就拆掉了，不需要留在房子里。ESLint、Prettier、Webpack 等属于这类。

```json
// package.json 示例
{
  "dependencies": {
    "react": "^19.0.0",     // 项目运行时需要（React 19！）
    "react-dom": "^19.0.0", // React DOM 渲染库
    "axios": "^1.6.0"      // 网络请求库，运行时需要
  },
  "devDependencies": {
    "eslint": "^8.55.0",    // 代码检查，开发时需要
    "prettier": "^3.0.0",   // 代码格式化工具
    "vite": "^5.0.0"        // 构建工具，开发时需要
  }
}
```

### 2.2.3 npm scripts：package.json scripts 字段

`package.json` 里的 `scripts` 字段，是 npm 的"快捷命令"区域。你可以在这里定义一些常用的命令，给它们起简单的名字，之后运行 `npm run xxx` 就能执行对应的脚本。

```json
{
  "scripts": {
    "dev": "vite",                    // 启动开发服务器
    "build": "vite build",           // 构建生产版本
    "preview": "vite preview",       // 预览生产构建结果
    "lint": "eslint src/",           // 运行代码检查
    "test": "vitest",                // 运行测试
    "format": "prettier --write ."   // 格式化所有代码文件
  }
}
```

定义了之后，运行方式是：

```bash
# 运行 dev 脚本
npm run dev

# 运行 build 脚本
npm run build

# 运行自定义脚本
npm run lint
# 打印结果示例：> eslint src/
# ✖ 3 problems (2 errors, 1 warning)
```

> 💡 小技巧：npm 还内置了一些特殊脚本，不需要 `run` 这个前缀，可以直接用 `npm test`、`npm start`、`npm stop`。其中 `start` 通常用于启动生产服务器，`test` 用于运行测试。

### 2.2.4 npm install vs npm ci 的区别

这里有两个命令看起来差不多，实际上区别很大：

```bash
# npm install：根据 package.json 和 package-lock.json 安装依赖
npm install
# 特点：
# 1. 会自动添加/删除/更新依赖（根据 package.json 的变化）
# 2. 适合开发阶段使用
# 3. 速度相对较慢（因为要检查最新版本）

# npm ci：干净利落地安装依赖（"CI" = Continuous Integration，持续集成）
npm ci
# 特点：
# 1. 完全根据 package-lock.json 安装，忽略 package.json
# 2. 删除 node_modules 之后重新安装，确保一致性
# 3. 速度更快
# 4. 适合自动化环境（CI/CD）和生产部署
# 打印结果示例：
# Added 1247 packages in 45s
```

> 记住这个原则：**开发用 `npm install`，部署用 `npm ci`**！团队协作时，建议把 `package-lock.json` 也提交到 Git 仓库，这样大家的依赖版本完全一致，不会有"我本地能用，你本地不行"的尴尬。

### 2.2.5 package-lock.json 的作用

`package-lock.json` 是 npm 5.0 之后引入的文件，它的职责是**精确锁定依赖树的版本**。

你可能会问：package.json 里不是已经写了 `"react": "^18.2.0"` 吗？为什么还需要 `package-lock.json`？

好问题！区别在于：
- `package.json` 里写的是**范围**：`^18.2.0` 意味着"安装 18.2.0 到 18.x.x 之间最新的版本"
- `package-lock.json` 里写的是**精确版本**：`react: 18.2.0`，甚至每个依赖的依赖（传递依赖）的精确版本都有记录

```json
// package-lock.json 示例（简化版）
{
  "dependencies": {
    "react": {
      "version": "18.2.0",        // 精确版本
      "resolved": "https://registry.npmjs.org/react/-/react-18.2.0.tgz",
      "integrity": "sha512-b+Rs..."
    },
    "react-dom": {
      "version": "18.2.0",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-18.2.0.tgz",
      "integrity": "sha512-b+Rs..."
    }
  }
}
```

这样做的好处是：**每次 `npm install`，不管是谁、在哪台机器上安装，安装出来的依赖树是完全一致的**。不再有"在我这里好好的，在你那里就不行"的问题！

---

## 2.3 npx：无需全局安装即可运行命令

`npx` 是 npm 5.2.0 之后自带的工具，它解决了两个问题：

1. **不想全局安装某个工具，但又想运行它**——`npx` 来帮你临时运行
2. **想运行某个命令但不知道它在哪**——`npx` 会自动在本地找，找不到就去网上下载

### 2.3.1 npx create-vite / npx create-react-app

我们后面会学到，创建 React 项目最简单的方式就是用 Vite。而 `create-vite` 这个工具，用 `npx` 来运行就非常方便：

```bash
# 创建一个 React 项目（不需要全局安装 create-vite）
npx create-vite@latest my-react-app --template react

# 逐段解释这条命令：
# npx                      -> 用 npx 运行（自动下载并执行，用完不留痕迹）
# create-vite@latest       -> create-vite 工具名，@latest 表示最新版本
# my-react-app             -> 项目名称（会创建一个同名文件夹）
# --template react          -> 指定使用 React 模板
#   注意：不写 --template react，命令会进入交互式菜单，让你手动选择框架
# 打印结果示例：
# Scaffolding project in my-react-app...
# Done! Now run:
#   cd my-react-app
#   npm install
#   npm run dev
```

同理，如果你用 Create React App（Facebook 官方的老牌创建工具）：

```bash
# 创建 React 项目（老方法，现在不推荐了，太慢）
npx create-react-app my-react-app
```

### 2.3.2 npx vs 全局安装的优劣对比

| 对比项 | npx（临时运行） | 全局安装 |
|--------|------------|--------|
| **磁盘空间** | 不占全局空间（用完即删） | 一直占用空间 |
| **版本控制** | 每个项目可以用不同版本 | 全局只有一个版本 |
| **污染全局命名空间** | 不会 | 久了全局一堆不知道干啥的包 |
| **适合场景** | 一次性命令、创建项目脚手架 | 长期使用的 CLI 工具（如 eslint、prettier）|

> 小建议：
> - **脚手架工具**（create-vite、create-next-app 等）→ 用 `npx`，用完就走，不占地方
> - **长期工具**（eslint、prettier）→ 全局安装一次，之后随时用

---

## 2.4 pnpm 与 yarn：npm 的替代品

npm 虽然是 Node.js 官方的包管理器，但它有几个让人头疼的问题：
- 安装速度慢（有时慢到让人去泡杯咖啡）
- 磁盘占用大（同样的包被安装很多份）
- 依赖树管理有时候很混乱

于是，**pnpm** 和 **yarn** 这两位"挑战者"应运而生。

### 2.4.1 pnpm 的优势：快、省空间

**pnpm**（Performant npm，高性能 npm）是由 npm 的前员工开发的，它的核心创新是**硬链接（Hard Link）和符号链接（Symbolic Link）**。

简单说，pnpm 不会把你的依赖复制到每个项目的 `node_modules` 里，而是**共享同一份物理文件**。就像图书馆的书，所有人可以在不同楼层、不同房间"借阅"同一本书，而不需要每层楼都买一本。

```bash
# pnpm 的安装
npm install -g pnpm

# 之后，把所有的 npm install 换成 pnpm install
pnpm install
# 打印结果示例：Lockfile is up-to-date, node_modules is up to date
```

pnpm 的优势：
- **速度快**：因为它使用了并行的下载策略
- **省空间**：所有项目共享同一份依赖包，不重复存储
- **更安全**：pnpm 用了特殊的目录结构，防止幽灵依赖（Phantom Dependencies）——即项目里明明没装这个包，但 Node 却能找到它的问题

### 2.4.2 pnpm 的安装与基本使用

```bash
# 全局安装 pnpm
npm install -g pnpm

# 验证安装
pnpm --version
# 打印结果示例：9.0.0

# 使用 pnpm 的常用命令（几乎和 npm 命令一样）
pnpm install              # 安装依赖（对应 npm install）
pnpm add react            # 添加生产依赖（对应 npm install react）
pnpm add -D eslint        # 添加开发依赖（对应 npm install --save-dev eslint）
pnpm remove react         # 卸载包（对应 npm uninstall react）
pnpm update               # 更新所有包到最新兼容版本
pnpm run dev              # 运行 scripts 里的 dev 命令
```

### 2.4.3 workspaces：monorepo 管理

**pnpm workspaces**（工作区）是 pnpm 的一个超强大功能，它允许你在一个代码仓库里管理多个子项目（也叫 monorepo 单体仓库）。

场景是这样的：你有一个 React 项目，里面有一个组件库、一个工具库、一个文档站点——三个项目有共享的依赖，但又需要分开管理。传统的做法是建三个独立的 Git 仓库，三个 `node_modules`，三个 `package-lock.json`……光想想就头疼。

pnpm workspaces 帮你解决这个问题：

```json
// 根目录的 package.json
{
  "name": "my-monorepo",
  "version": "1.0.0",
  "private": true,
  // 启用 workspaces，指定子项目目录
  "pnpm": {
    "workspaces": [
      "packages/*"     // packages 目录下所有子项目
    ]
  }
}
```

目录结构变成这样：

```
my-monorepo/
├── package.json
├── pnpm-workspace.yaml     // pnpm 工作区配置文件
└── packages/
    ├── components/         // 组件库
    │   ├── package.json
    │   └── src/
    ├── utils/               // 工具库
    │   ├── package.json
    │   └── src/
    └── docs/                // 文档站点
        ├── package.json
        └── src/
```

`pnpm-workspace.yaml` 的内容非常简单，只需要声明工作区的路径即可：

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'   # 与 package.json 里的 workspaces 配置保持一致
```

根目录运行一次 `pnpm install`，所有子项目的依赖都会被安装，而且共享的依赖只会在磁盘上存一份！

> 🔥 React 官方（包括 Vite）从 2023 年开始官方支持 pnpm workspace，如果你的团队使用 monorepo 结构，强烈建议试试 pnpm！

---

## 本章小结

本章我们搞定了 React 开发的第一组"地基工具"：

- **Node.js**：JavaScript 的运行时环境，让 JS 能够跑在服务器端和本地命令行
- **npm**：Node.js 官方的包管理器，"JavaScript 世界的应用商店"，用 `npm install` 安装依赖，用 `npm init` 初始化项目
- **npx**：npm 内置的命令运行器，让你无需全局安装就能临时运行各种 CLI 工具
- **pnpm / yarn**：npm 的强力替代品，pnpm 以"硬链接共享"技术著称，yarn 以稳定和功能丰富著称

下一章，我们将配置开发工具——Visual Studio Code、插件、快捷键……让你的"武器库"武装到牙齿！💻🚀