

+++
title = "第2章 环境准备与安装"
weight = 20
date = "2026-03-27T17:13:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter-02-Environment-Setup

# 第2章：环境准备与安装

> 古人云："工欲善其事，必先利其器。" 在正式开始写代码之前，我们得先把开发环境整利索了。
>
> 这一章，我们会解决几个灵魂拷问：
> - Node.js 是个啥？我电脑上要装几个 Node？
> - nvm、fnm、Volta...这些名字听起来像变形金刚的到底是什么？
> - pnpm、yarn、npm，三国鼎立，我该站哪边？
> - 创建一个 Vite 项目，到底要走哪几步？
>
> 准备好了吗？让我们开始这场"环境搭建马拉松"！🏃‍♂️

---

## 2.1 前置知识要求

在跳进 Vite 的深水区之前，我们得确保你对以下基础知识有足够的了解。这些知识就像游泳前的热身动作——做不做都能下水，但做了肯定游得更稳。

### 2.1.1 HTML/CSS/JavaScript 基础

这是前端开发的"三驾马车"，缺一不可。

**HTML（超文本标记语言）** 是网页的骨架。它定义了网页的结构——哪里是标题，哪里是段落，哪里是按钮。你可以把 HTML 想象成建造房屋时的钢筋骨架：

```html
<!-- 一个最简单的 HTML 结构 -->
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的第一个网页</title>
  </head>
  <body>
    <h1>你好，世界！</h1>
    <p>这是我的第一个网页，激动地搓手手~</p>
    <button onclick="sayHello()">点我</button>
  </body>
</html>
```

**CSS（层叠样式表）** 是网页的外衣。它负责"看起来怎么样"——颜色、字体、布局、动画，全靠 CSS。你可以把 CSS 想象成装修工人，把骨架装修成漂亮的房子：

```css
/* CSS 让网页从"毛坯房"变成"精装房" */
body {
  font-family: 'Microsoft YaHei', sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0;
}

h1 {
  color: white;
  font-size: 3rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

button {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 50px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #ee5a5a;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
}
```

**JavaScript** 是网页的灵魂。它让网页"活"起来——响应用户点击、处理数据、发送网络请求、动画效果，JavaScript 什么都能干。你可以把它想象成房子的智能家居系统，让静态的房子变成会"思考"的活物：

```javascript
// JavaScript 给网页注入灵魂
function sayHello() {
  alert('Hello！欢迎来到 JavaScript 的世界 🎉')
}

// 或者更现代一点的写法
const sayHello = () => {
  console.log('你好，JavaScript！')  // 你好，JavaScript！
}
```

> 💡 **小贴士**：如果你对这些基础知识还不太熟悉，建议先去 [MDN Web Docs](https://developer.mozilla.org/zh-CN/) 或者各大视频网站充充电。别担心，学基础不用太久——有基础的话，一两周足够了。

### 2.1.2 ES6+ 新特性

ES6（ECMAScript 2015）是 JavaScript 历史上最重要的一次更新，此后每年都有新特性加入。Vite 的开发体验之所以这么好，很大程度上是因为它充分利用了现代 JavaScript 的特性。所以，下面这些知识点，你最好都混个眼熟：

**箭头函数** —— 写起来更简洁，`this` 绑定更符合直觉：

```javascript
// 普通函数
function add(a, b) {
  return a + b
}

// 箭头函数
const add = (a, b) => a + b

// 箭头函数 + 对象返回（注意括号）
const getUser = (name, age) => ({ name, age })
console.log(getUser('小明', 18))  // { name: '小明', age: 18 }
```

**模板字符串** —— 再也不用 `+` 号拼接字符串了：

```javascript
const name = '小红'
const age = 20

// 老写法（累觉不爱）
const message = '我叫' + name + '，今年' + age + '岁'

// 新写法（真香警告）
const message = `我叫${name}，今年${age}岁`

// 还能写多行
const html = `
  <div>
    <h1>${name}</h1>
    <p>${age}岁</p>
  </div>
`
```

**解构赋值** —— 从数组或对象中提取值，只需一句话：

```javascript
// 对象解构
const { name, age } = { name: '小刚', age: 25 }
console.log(name, age)  // 小刚 25

// 数组解构
const [first, second, ...rest] = [1, 2, 3, 4, 5]
console.log(first, second, rest)  // 1 2 [3, 4, 5]

// 函数参数解构
const printUser = ({ name, age }) => {
  console.log(`${name} - ${age}`)
}
printUser({ name: '小芳', age: 22 })  // 小芳 - 22
```

**模块（import/export）** —— Vite 的根基，浏览器原生支持：

```javascript
// utils.js —— 导出
export const PI = 3.14159
export const add = (a, b) => a + b
export default class Calculator { }

// main.js —— 导入
import Calculator, { PI, add } from './utils.js'
console.log(PI)         // 3.14159
console.log(add(1, 2))   // 3
const calc = new Calculator()
```

**Promise 与 async/await** —— 异步编程的"人类可读版"：

```javascript
// Promise 版
fetch('/api/user')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err))

// async/await 版（更香）
const getUser = async () => {
  try {
    const res = await fetch('/api/user')
    const data = await res.json()
    console.log(data)
  } catch (err) {
    console.error(err)
  }
}
```

**其他常用新特性**：

| 特性 | 说明 | 示例 |
|------|------|------|
| `let/const` | 块级作用域声明 | `const API_URL = '...'` |
| `...` 展开符 | 数组/对象展开 | `[...arr1, ...arr2]` |
| `Map/Set` | 新的数据结构 | `new Map()`, `new Set()` |
| `for...of` | 遍历可迭代对象 | `for (const item of arr)` |
| `??` 空值合并 | 替代 `\|\|` 更合理 | `value ?? 'default'` |
| `?.` 可选链 | 安全访问深层属性 | `obj?.profile?.name` |

### 2.1.3 Node.js 与 npm 简介

**Node.js** 是什么？简单来说，Node.js 就是**用 JavaScript 写后端代码**的工具。

传统上，JavaScript 只能在浏览器里运行。但 Node.js 就像是给 JavaScript 装上了"腿"，让它可以在服务器、你的电脑、甚至树莓派上跑起来。

Node.js 基于 Chrome 的 V8 引擎（就是 Chrome 浏览器里运行 JavaScript 的那个引擎），经过优化后速度飞快。而且 Node.js 天生擅长处理 I/O 操作（读写文件、网络请求等），所以特别适合做：
- 前端构建工具（Webpack、Vite、esbuild 全是 Node.js 写的）
- 后端 API 服务
- 命令行工具
- 脚手架工具

你电脑上安装的 Node.js，其实包含了两样东西：
1. **Node.js 运行时** —— 执行 JavaScript 代码
2. **npm（Node Package Manager）** —— 管理 npm 上成千上万的"包"（别人写好的代码库）

你可以打开终端验证一下：

```bash
node -v    # 查看 Node.js 版本
npm -v     # 查看 npm 版本
```

> 📌 **版本号小知识**：目前 Node.js 的长期维护版本（LTS）是 Node.js 22.x 左右，Vite 6.x 要求 Node.js 18+。如果你的版本低于 18，建议升级。

**npm 的工作方式**其实很简单：
1. 你在项目里 `npm install` 一个包（比如 `lodash`）
2. npm 去 npm 仓库（registry.npmjs.org）下载这个包
3. npm 把包存到项目的 `node_modules` 文件夹里
4. npm 在 `package.json` 里记一笔："这个项目用了 lodash 版本 x.y.z"
5. 下次别人 `npm install` 时，npm 读到 `package.json`，自动把所有依赖都装好

---

## 2.2 安装 Node.js

### 2.2.1 下载与安装

安装 Node.js 有三种主流方式：

#### 方式一：官网直接下载安装包

这是最简单粗暴的方式，适合"不想折腾，只想快点用上"的同学。

1. 打开 [Node.js 官网](https://nodejs.org/)
2. 看到两个大按钮：**LTS（长期支持版）** 和 **Current（最新版）**
3. 点击 **LTS** 按钮下载（新手推荐，稳定第一）
4. 双击安装包，一路点"下一步"，搞定

> ⚠️ **Windows 用户注意**：安装时记得勾选 **"Add to PATH"**（添加到环境变量），否则终端里会找不到 `node` 命令。

#### 方式二：使用 nvm-windows（Node.js 版本管理神器）⭐强烈推荐

nvm（Node Version Manager）是什么？它是 Node.js 的"版本管理器"，可以让你的电脑同时安装**多个版本的 Node.js**，想用哪个用哪个，想换哪个换哪个。

为什么推荐这个？因为：

- **项目兼容性**：老项目可能需要 Node.js 14，新项目需要 Node.js 22，你不能把电脑重装成两个系统吧？
- **测试兼容性**：发布新包之前，你想在 Node.js 16、18、20、22 上都测试一遍
- **不怕搞坏**：装新版本出问题了？一行命令切回旧版本，原地满血复活

**nvm-windows** 是 nvm 的 Windows 版本，安装步骤如下：

**第一步：卸载已有的 Node.js**（重要！否则可能冲突）

去控制面板 → 程序和功能 → 找到 Node.js → 卸载

**第二步：安装 nvm-windows**

去 GitHub 下载：`https://github.com/coreybutler/nvm-windows/releases`

下载 `nvm-setup.exe` 或者 `nvm-setup.zip`，运行安装包即可。

**第三步：验证安装**

打开一个新的 PowerShell 或 CMD（**重新打开！不然环境变量不生效**），输入：

```bash
nvm version
# 输出类似：1.1.12
```

**第四步：安装 Node.js**

```bash
# 安装最新 LTS 版本
nvm install lts

# 或者安装指定版本
nvm install 20.12.0

# 查看已安装的版本
nvm list

# 切换使用某个版本
nvm use 20.12.0

# 验证
node -v  # 20.12.0
npm -v   # 10.x.x
```

> 💡 **nvm 常用命令速查**：
> ```bash
> nvm list                    # 查看已安装的版本
> nvm list available          # 查看可安装的版本
> nvm install <版本号>        # 安装指定版本
> nvm use <版本号>            # 切换到指定版本
> nvm uninstall <版本号>      # 卸载指定版本
> nvm alias default <版本号>  # 设置默认版本
> ```

#### 方式三：使用 fnm（更现代的选择）

fnm（Fast Node Manager）是另一个 Node.js 版本管理器，它的特点是：
- **速度更快**（用 Rust 写的）
- **跨平台**（Windows/macOS/Linux 通吃）
- **支持 `.nvmrc` 文件**（项目里放一个文件，自动切换版本）

安装 fnm：

```bash
# Windows 上用 PowerShell 安装
irm https://fnm.vercel.app/install | pwsh

# 或者用 npm 全局装
npm install -g fnm

# 配置 shell（把下面这行加到 ~/.bashrc 或 ~/.zshrc）
eval "$(fnm env --use-on-cd)"
```

fnm 使用示例：

```bash
fnm install 20
fnm use 20
fnm default 20

# 或者在项目里放一个 .nvmrc 文件，内容是：20
# 然后进入项目目录时，自动切换版本
fnm install 18
fnm use
```

### 2.2.2 版本管理工具对比

| 工具 | 编写语言 | 速度 | Windows 支持 | 特殊功能 |
|------|----------|------|--------------|----------|
| nvm | Shell | 中等 | 需单独安装 | 老牌稳定 |
| fnm | Rust | 极快 | 良好 | 自动版本切换 |
| Volta | Rust | 极快 | 良好 | 智能工具链管理 |

**我的建议**：
- 如果你只用 Windows，**nvm-windows** 最稳
- 如果你追求速度，且愿意折腾，**fnm** 是不错的选择
- **Volta** 比较特别，它不仅管理 Node.js，还管理 npm 包和命令行工具，适合"希望工具链完全版本化"的强迫症患者

### 2.2.3 验证安装成功

不管你用什么方式安装的，验证方法都一样。打开终端（PowerShell、CMD、Terminal 都可以），输入：

```bash
node -v
# 输出：v20.12.0（或者其他版本号）

npm -v
# 输出：10.x.x（或者更高版本号）
```

如果看到了版本号，恭喜你！Node.js 和 npm 已经成功安装。

你还可以顺便检查一下 npm 的镜像源是否是中国镜像（国内下载速度更快）：

```bash
npm config get registry
# 如果输出 https://registry.npmjs.org/ 就是官方源，速度一般
# 如果输出 https://registry.npmmirror.com/ 就是淘宝镜像，速度飞快
```

> 💡 **国内用户建议**：把 npm 镜像切换成淘宝镜像，速度能提升好几倍！
> ```bash
> npm config set registry https://registry.npmmirror.com/
> ```

### 2.2.4 Node.js 版本选择建议

Node.js 的版本号规则是：**主版本.次版本.补丁版本**

- **主版本（Major）**：有重大更新，可能有破坏性变更。Node.js 主版本号每年 4 月份递增一次。
- **次版本（Minor）**：添加新功能，向后兼容
- **补丁版本（Patch）**：修复 bug，向后兼容

**LTS vs Current 的区别**：
- **LTS（Long Term Support）**：长期维护版，稳定，bug 修复及时，适合生产环境
- **Current**：最新特性版，可能不稳定，适合尝鲜

**版本选择建议**：

| 场景 | 推荐版本 | 理由 |
|------|----------|------|
| 新手入门 | LTS（18+） | 稳定，文档多，社区支持好 |
| 企业项目 | LTS（20.x 或 22.x） | 稳定优先，生产环境首选 |
| 学习新技术 | Current（最新版） | 体验最新特性，但可能有坑 |
| Vue/React 开发 | 18+ | Vite 6.x 要求 18+ |

> ⚠️ **重要提醒**：如果你要用 Vite 6.x，**必须确保 Node.js 版本 >= 18**。低于这个版本的 Node.js 就像一辆老旧的汽车，可能无法启动最新的 Vite。

---

## 2.3 包管理器选择

Node.js 安装好了，现在我们要谈谈"包管理器"这件事。

包管理器是帮我们安装、更新、卸载"包"（别人写好的代码）的工具。npm、yarn、pnpm 是目前最主流的三个选择，它们各有特点。

### 2.3.1 npm 基础使用

npm（Node Package Manager）是 Node.js 自带的包管理器，装机即用，无需额外安装。它的仓库（registry）是世界上最大的开源代码仓库，目前有超过 200 万个包。

**npm 常用命令**：

```bash
# 初始化一个新项目（创建 package.json）
npm init

# 初始化并自动填默认值（项目名=文件夹名，版本=1.0.0）
npm init -y

# 安装依赖
npm install <包名>
npm install vue          # 安装特定包
npm install -D vite     # 安装开发依赖（-D 等价于 --save-dev）
npm install -g typescript  # 全局安装（-g 等价于 --global）

# 安装 package.json 里的所有依赖
npm install
npm install --legacy-peer-deps  # 忽略 peer dependencies 冲突

# 卸载依赖
npm uninstall <包名>
npm uninstall vue
npm uninstall -D vite

# 更新依赖
npm update              # 更新所有依赖到最新兼容版本
npm update vue          # 更新特定包

# 运行脚本
npm run dev             # 运行 package.json 里定义的 dev 脚本
npm run build           # 运行 build 脚本

# 查看信息
npm list                # 查看已安装的包
npm list vue            # 查看特定包版本
npm outdated           # 查看有哪些包可以更新
npm info vue           # 查看包的详细信息
```

**package.json 里的依赖字段**：

| 字段 | 说明 | 举例 |
|------|------|------|
| `dependencies` | 生产依赖，项目运行必须 | `vue`, `axios`, `react` |
| `devDependencies` | 开发依赖，只在开发时用到 | `vite`, `eslint`, `jest` |

```json
{
  "name": "my-vite-project",
  "version": "1.0.0",
  "dependencies": {
    "vue": "^3.4.0"  // ^表示"兼容更新"，可以更新到3.x.x
  },
  "devDependencies": {
    "vite": "^5.0.0"  // 开发时用，生产构建时需要
  }
}
```

### 2.3.2 yarn 简介与基本命令

yarn 是 Facebook 在 2016 年推出的包管理器，初始目的是解决 npm 的一些痛点（安装速度慢、没有锁文件等）。

yarn 的特点：
- **速度快**：并行安装，比 npm 早期版本快很多
- **离线安装**：依赖会被缓存到本地
- **命令简洁**：比 npm 简洁

**yarn 常用命令**：

```bash
# 安装（如果没用过 yarn，先 npm install -g yarn 全局安装）
yarn add vue              # 安装生产依赖
yarn add -D vite          # 安装开发依赖
yarn add -g typescript    # 全局安装

# 初始化
yarn init

# 安装所有依赖（根据 yarn.lock）
yarn install
yarn install --offline   # 离线模式，用本地缓存

# 卸载
yarn remove vue

# 运行脚本
yarn dev
yarn build

# 其他常用
yarn list                 # 查看已安装的包
yarn outdated             # 查看可更新的包
yarn upgrade              # 升级所有包
yarn info vue             # 查看包信息
```

> ⚠️ **注意**：yarn 和 npm 的 lock 文件不兼容！`yarn.lock` vs `package-lock.json`。团队项目里，大家最好用同一个包管理器，否则容易出现"我的电脑能跑，你的电脑不行"的诡异问题。

### 2.3.3 pnpm 推荐与安装（磁盘高效）⭐强烈推荐

**pnpm（performant npm）** 是目前我最推荐的包管理器，它解决了 npm 和 yarn 的两个核心痛点：

#### pnpm 的三大优势

**1. 磁盘空间节省 50%+**

npm 和 yarn 会把同一个包的同一个版本复制到每个项目的 `node_modules` 里。如果你有 10 个项目都用 Vue，每个项目里都有一份 Vue，磁盘空间就这么浪费了。

pnpm 使用**硬链接（hard link）**的方式：包只存储一份，各项目通过链接共享。这样，即使 100 个项目都用 Vue，磁盘上真的只有一份 Vue。

```
npm/yarn：10个项目 → 10份 Vue（每个约 200MB）= 2GB
pnpm：10个项目 → 1份 Vue = 200MB
```

**2. 安装速度更快**

pnpm 使用并行安装，比 yarn 的串行安装更快。

**3. 安全性更高**

pnpm **禁止幽灵依赖（phantom dependencies）**，采用严格结构管理模式，确保项目只能访问 `package.json` 里声明的依赖，防止"能访问但没声明"的混乱情况。

**pnpm 安装与使用**：

```bash
# 第一种方式：用 npm 全局安装
npm install -g pnpm

# 第二种方式：用 Corepack 启用（Node.js 16.10+）
corepack enable
corepack prepare pnpm@latest --activate

# 验证安装
pnpm -v
# 输出：9.x.x
```

**pnpm 常用命令**：

```bash
# 初始化项目
pnpm init

# 安装依赖
pnpm install              # 安装 package.json 里的依赖
pnpm add vue             # 安装生产依赖
pnpm add -D vite         # 安装开发依赖
pnpm add -g pnpm         # 全局安装

# 卸载
pnpm remove vue

# 更新
pnpm up                  # 更新所有依赖
pnpm up vue              # 更新特定包

# 运行脚本
pnpm dev                 # 开发模式
pnpm build               # 生产构建
pnpm preview             # 预览构建结果

# 其他
pnpm list                # 查看依赖树
pnpm outdated            # 查看可更新的包
pnpm store status        # 查看 pnpm store 状态
pnpm store prune         # 清理未使用的 store
```

### 2.3.4 包管理器对比与选择建议

| 特性 | npm | yarn | pnpm |
|------|-----|------|------|
| 安装速度 | 中等 | 快 | **最快** |
| 磁盘占用 | 高 | 高 | **最低** |
| node_modules 结构 | 扁平 | 扁平 | **严格结构** |
| lock 文件 | package-lock.json | yarn.lock | pnpm-lock.yaml |
| 幽灵依赖 | 允许（易出问题） | 允许 | **禁止（更安全）** |
| 生态兼容 | 最好 | 好 | 好 |
|  workspaces | 支持 | 支持 | **支持且更好** |
| 新项目推荐 | ⭐⭐ | ⭐⭐⭐ | **⭐⭐⭐⭐⭐** |

**选择建议**：
- 如果是个人小项目，随便选，差别不大
- 如果是团队项目，**强烈建议 pnpm**，磁盘占用省、速度快、依赖管理更严格
- 如果老项目已经在用 npm/yarn，不强制迁移，但新项目建议用 pnpm

> 💡 **小故事**：pnpm 的作者是来自俄罗斯的前端大佬 **Zoltan Kochan**。pnpm 的命名是因为"performant npm"（高性能 npm），但也有程序员调侃说是"pnpm = pretty npm"或者"pnpm = please npm performing much" 😂

**包管理器切换小技巧**：

如果你想在自己的项目里"禁止"使用某个包管理器，可以在 `package.json` 里加一个配置：

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "packageManager": "pnpm@9.0.0",
  "scripts": {
    "dev": "vite"
  }
}
```

这样，团队成员运行 `npm install` 或 `yarn install` 时，会收到错误提示，引导他们使用 pnpm。

---

## 2.4 安装 Vite

### 2.4.1 正确的创建命令

这是最重要的一步！创建一个 Vite 项目非常简单，只需要一行命令。但很多新手会在这里犯错——把 `npm create vite` 记成了 `npm install vite`。

**注意**：`create-vite` 是 Vite 官方提供的项目脚手架工具，专门用来**创建新项目**。而 `npm install vite` 是用来**在已有项目里安装 Vite 依赖**的。

**创建项目的正确命令**：

```bash
# npm
npm create vite@latest 项目名 -- --template 模板类型

# pnpm（推荐）
pnpm create vite@latest 项目名 -- --template 模板类型

# yarn
yarn create vite 项目名 --template 模板类型
```

> ⚠️ **重要**：这里的 `--` 不是打错了！它是一个分隔符，表示"后面的参数是传给模板的，不是传给 npm 的"。很多人忘了加 `--`，结果命令报错。

**语法解释**：
- `create vite@latest`：使用 create-vite 工具创建项目，@latest 表示使用最新版本
- `项目名`：你给项目起的名字，会作为文件夹名。如果想当前目录创建，用 `.` 代替项目名
- `--template 模板类型`：指定使用什么模板（vue/react/svelte/vanilla...）

### 2.4.2 全局安装 vs 本地安装

很多新手会问："Vite 能不能全局安装，这样我每次创建项目就不用下载了？"

**答案是不建议全局安装 Vite**。原因如下：

- **版本一致性**：每个项目应该锁定自己需要的 Vite 版本，而不是共用一个全局版本
- **插件兼容性**：Vite 插件和 Vite 版本有对应关系，全局安装会导致版本混乱
- **团队协作**：其他人克隆你的代码后，无法知道你用的是哪个全局版本

**正确做法**：通过 `create-vite` 脚手架创建项目时，脚手架会自动把 Vite 作为本地依赖安装到项目的 `node_modules` 里。`package.json` 里会记录确切的版本号，团队成员安装依赖时会安装完全相同的版本。

```json
{
  "devDependencies": {
    "vite": "^5.4.0"
  }
}
```

> 📌 **什么时候可以全局安装**？如果你只是临时尝鲜、写个 demo、或者自己写一些脚本，全局安装完全没问题：`npm install -g vite`

### 2.4.3 使用不同包管理器创建项目

这里分别展示用 npm、pnpm、yarn 创建项目的完整命令：

```bash
# 用 npm 创建（以 Vue 为例）
npm create vite@latest my-vue-app -- --template vue
cd my-vue-app
npm install
npm run dev

# 用 pnpm 创建（以 Vue 为例）⭐推荐
pnpm create vite@latest my-vue-app -- --template vue
cd my-vue-app
pnpm install
pnpm run dev

# 用 yarn 创建（以 Vue 为例）
yarn create vite my-vue-app --template vue
cd my-vue-app
yarn
yarn dev
```

### 2.4.4 交互式创建

如果你不想记那么多模板名，或者你想看看有哪些选项，可以直接运行不带模板的命令：

```bash
npm create vite@latest
# 或者
pnpm create vite@latest
# 或者
yarn create vite
```

这时，脚手架会问你几个问题：

```
? Project name: (my-vite-app)   # 项目名，直接回车用括号里的默认值
? Select a template:            # 选择模板
  > vanilla
    vanilla-ts
    vue
    vue-ts
    react
    react-ts
    preact
    preact-ts
    svelte
    svelte-ts
    solid
    solid-ts
    qwik
    qwik-city
    lit
    lit-ts
```

用键盘上下箭头选择，回车确认。

### 2.4.5 创建不同框架项目模板

Vite 支持非常多的框架模板，下面是完整的模板列表和使用方法：

| 模板名 | 说明 | 适用场景 |
|--------|------|----------|
| `vanilla` | 原生 HTML/JS/CSS | 纯静态页面，学习 JavaScript |
| `vanilla-ts` | 原生 + TypeScript | 想用 TS 的静态页面 |
| `vue` | Vue 3 + JavaScript | Vue 3 项目 |
| `vue-ts` | Vue 3 + TypeScript | Vue 3 + TS 项目 |
| `react` | React + JavaScript | React 项目 |
| `react-ts` | React + TypeScript | React + TS 项目 |
| `svelte` | Svelte | Svelte 框架项目 |
| `svelte-ts` | Svelte + TypeScript | Svelte + TS 项目 |
| `preact` | Preact | 轻量级 React 替代 |
| `preact-ts` | Preact + TypeScript | Preact + TS 项目 |
| `solid` | SolidJS | SolidJS 框架 |
| `solid-ts` | SolidJS + TypeScript | SolidJS + TS 项目 |
| `qwik` | Qwik | Qwik 框架项目 |
| `qwik-city` | Qwik + QwikCity | Qwik 全栈框架 |
| `lit` | Lit Web Components | Lit 组件库 |
| `lit-ts` | Lit + TypeScript | Lit + TS 项目 |

**创建示例**：

```bash
# 创建一个 Vue 项目
pnpm create vite@latest my-vue-app -- --template vue

# 创建一个 React 项目
pnpm create vite@latest my-react-app -- --template react

# 创建一个 Svelte 项目
pnpm create vite@latest my-svelte-app -- --template svelte

# 创建一个 TypeScript 项目（以 Vue 为例）
pnpm create vite@latest my-ts-app -- --template vue-ts

# 创建一个 Qwik 全栈项目
pnpm create vite@latest my-qwik-app -- --template qwik-city

# 创建一个 Lit Web Components 项目
pnpm create vite@latest my-lit-app -- --template lit
```

---

## 2.5 第一个 Vite 项目

### 2.5.1 使用命令行创建项目

好了，理论讲完了，是时候真刀真枪地创建一个项目了！让我们以创建一个 Vue 项目为例：

```bash
# 使用 pnpm 创建（假设你在桌面上操作）
cd ~/Desktop
pnpm create vite@latest hello-vite -- --template vue

# 安装依赖
cd hello-vite
pnpm install

# 启动开发服务器
pnpm dev
```

如果一切顺利，你会看到类似这样的输出：

```
  VITE v5.4.0  ready in 320 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

现在，打开浏览器，访问 `http://localhost:5173/`，你应该能看到一个漂亮的 Vite + Vue 页面！

> 🎉 **恭喜你！** 你的第一个 Vite 项目已经成功运行了！

### 2.5.2 项目目录结构解析

一个典型的 Vite 项目（以 Vue 为例），目录结构是这样的：

```
hello-vite/
├── public/                 # 公共静态资源目录
│   └── vite.svg           # Vite 的 logo（不会被处理，直接复制到 dist）
│
├── src/                    # 源代码目录（你的代码都在这里）
│   ├── assets/            # 资源目录（会被 Vite 处理）
│   │   └── vue.svg       # 图片资源
│   │
│   ├── components/        # 组件目录
│   │   └── HelloWorld.vue # 示例组件
│   │
│   ├── App.vue           # 根组件
│   ├── main.js           # 入口文件
│   └── style.css         # 全局样式
│
├── index.html             # 入口 HTML（浏览器访问的起点）
├── package.json           # 项目配置（依赖、脚本、名称）
├── vite.config.js         # Vite 配置文件（核心！）
├── tsconfig.json          # TypeScript 配置（如果用 TS 的话）
└── README.md              # 项目说明文档
```

**每个文件的职责**：

| 文件/目录 | 作用 |
|-----------|------|
| `index.html` | 浏览器访问的第一个页面，`<script type="module">` 引入入口 JS |
| `src/main.js` | Vue/React 应用的入口，创建应用实例 |
| `src/App.vue` | Vue 的根组件（React 里叫 App.jsx） |
| `public/` | 静态资源，不会被 Vite 处理，构建时原封不动复制到输出目录 |
| `src/assets/` | 动态资源，Vite 会处理（压缩、hash 命名等） |
| `vite.config.js` | Vite 配置文件，定义插件、服务器、构建选项等 |
| `package.json` | 项目元信息，记录依赖、脚本命令等 |

> 💡 **小技巧**：`public` 和 `src/assets` 的区别是什么？
> - `public/`：不需要打包处理的静态文件，直接复制。比如 `favicon.ico`、第三方 SDK 文件
> - `src/assets/`：需要打包处理的资源文件，Vite 会给它们加 hash、压缩等优化。比如图片、CSS

### 2.5.3 安装依赖并启动

如果你是从 GitHub 或者其他地方 clone 了一个 Vite 项目，第一件事就是安装依赖：

```bash
# npm
npm install

# pnpm（推荐）
pnpm install

# yarn
yarn
```

安装完成后，就可以启动开发服务器了：

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev
```

开发服务器启动后，Vite 会监听文件变化。当你修改代码时，它会自动重新加载（热更新），浏览器里几乎瞬间就能看到变化。

**npm scripts 里的常用命令**（定义在 `package.json` 里）：

| 命令 | 说明 |
|------|------|
| `vite` / `vite dev` / `vite serve` | 启动开发服务器 |
| `vite build` | 构建生产版本（生成 `dist` 目录） |
| `vite preview` | 预览生产构建（本地静态服务器） |
| `vite --help` | 查看 Vite 所有命令 |

### 2.5.4 浏览器中查看效果

开发服务器运行后，你会看到这样的输出：

```
  VITE v5.4.0  ready in 320 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**访问方式**：
- **本机访问**：直接在浏览器地址栏输入 `http://localhost:5173/`
- **局域网访问**：如果想用手机或其他设备访问，运行 `pnpm dev --host`，然后用电脑的 IP 地址访问（如 `http://192.168.1.100:5173/`）

**常见问题排查**：

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 浏览器显示空白 | 端口被占用 | 换一个端口：`pnpm dev --port 3000` |
| 页面一直转圈 | 服务器没启动成功 | 看终端有没有报错信息 |
| 样式不生效 | CSS 文件路径错误 | 检查 `import` 路径是否正确 |
| 页面报错 "import not found" | 模块导入错误 | 检查文件路径、大小写、扩展名 |

---

## 2.6 本章小结

### 🎉 本章总结

这一章我们搞定了 Vite 开发前的所有准备工作！让我们来回顾一下：

1. **前置知识**：复习了 HTML/CSS/JS 基础和 ES6+ 新特性，确认了 Node.js 和 npm 的基本概念

2. **Node.js 安装**：学会了三种安装方式，重点推荐使用 nvm-windows 或 fnm 进行版本管理，还学会了如何验证安装成功

3. **包管理器**：深入了解了 npm、yarn、pnpm 三种包管理器，重点推荐了磁盘高效且速度快的 **pnpm**

4. **Vite 安装**：掌握了正确的创建命令 `pnpm create vite@latest 项目名 -- --template xxx`，了解了全局安装 vs 本地安装的区别

5. **模板类型**：认识了所有可用的 Vite 模板（vanilla、vue、react、svelte 等）

6. **第一个项目**：成功创建、启动、访问了第一个 Vite 项目，并理解了项目目录结构

### 📝 本章练习

1. **安装 Node.js**：如果你还没安装，现在就去安装一个 LTS 版本（18+），然后用 `node -v` 验证

2. **安装 pnpm**：运行 `npm install -g pnpm`，然后 `pnpm -v` 验证

3. **创建你的第一个项目**：用 `pnpm create vite@latest my-first-vite -- --template vue` 创建一个 Vue 项目，然后 `cd my-first-vite && pnpm install && pnpm dev`，在浏览器里看看效果

4. **探索其他模板**：尝试用 `--template react` 创建一个 React 项目，感受一下 Vite 对不同框架的支持

5. **尝试修改代码**：打开 `src/App.vue`，修改一下文字，然后保存，看看浏览器是不是瞬间就更新了（这就是传说中的 HMR！）

---

> 📌 **预告**：下一章我们将深入 **Vite 基础使用**，详细讲解项目结构、命令行参数、入口文件、模块系统、静态资源处理、路径别名配置等。干货满满，敬请期待！
