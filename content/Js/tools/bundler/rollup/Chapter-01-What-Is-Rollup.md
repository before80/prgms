+++
title = "第1章 什么是 Rollup"
weight = 10
date = "2026-03-28T11:38:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 1 章　Rollup 是什么

## 1.1 官方定义：专注于 ES Module 的新一代打包工具

如果把前端世界的打包工具比作一家餐厅，那 **Rollup** 就是那个只做精品套餐、不卖自助餐的固执大厨。

它的官方定义是这样的：**Rollup 是一个 JavaScript 模块打包器（module bundler），专注于 ES Module 语法的打包工具**。听起来平平无奇对吧？就像说"这家餐厅是做菜的"一样敷衍。但魔鬼藏在细节里——它的核心卖点是"**专注于 ES Module**"这五个字。

这就好比说：别家餐厅啥菜都做，川菜粤菜西餐日料一应俱全，结果每道菜都是及格线水平；而 Rollup 跟你说，我们家只做一件事——把 ES Module 这种"食材"做成让你惊艳的"分子料理"，而且我们还顺带帮你把厨房里的垃圾（死代码）清理得一干二净。

> **ES Module 是什么？**
> ES Module 是 ECMAScript 2015（也就是 ES6）引入的官方模块系统。在那之前，JavaScript 这门语言其实是没有"模块"这个概念的——你只能通过各种民间方案（CommonJS、AMD、UMD）来模拟。ES Module 的出现，就像 JavaScript 终于拿到了大学文凭，终于可以光明正大地说自己是"科班出身"了。它长这样：

```javascript
// 导入
import { cloneDeep } from 'lodash-es';
import React from 'react';

// 导出
export function add(a, b) {
  return a + b;
}

export default function multiply(a, b) {
  return a * b;
}
```

这种语法在现代浏览器和 Node.js 中都是原生支持的。而 Rollup 的核心能力，就是**把一堆这样的 ES Module 文件，打包成一个（或多个）可以直接运行的文件**，同时顺便帮你把那些"导出了但根本没人用"的代码给剔除掉——这就是传说中的 **Tree-Shaking**（树摇），我们后面会详细介绍这个"大力出奇迹"的功能。

简单来说，Rollup 的定位就是：

- **专注于库和工具的打包**，追求极致的 Tree-Shaking 效果和最小的产物尺寸
- **也支持代码分割**，但不像 Webpack 那样以应用打包为设计核心
- **不提供**热更新、开发服务器这些"应用级"的开发体验功能
- **产物小、快、干净**，是它的核心竞争力

> 🤔 **等等，Rollup 不是说自己"不操心代码分割"吗？**
> 别急！Rollup 其实是支持代码分割的（见 1.3.3 节），只是这不是它的设计重心。它的核心招牌是 **Tree-Shaking 效果**——把这件事做到极致，其他都是顺带的。

如果 Webpack 是一个功能齐全的瑞士军刀，那 Rollup 就是一把磨得锋利无比的小刀——它只做一件事，但把这件事做到了极致。

---

## 1.2 核心设计理念

Rollup 能在打包工具的江湖中占有一席之地，靠的不是花拳绣腿，而是三招核心心法：**Tree-Shaking**、**Zero Runtime**、以及**原生 ES Module 支持**。这三招有多厉害？我们一个一个拆开来看。

### 1.2.1 "Tree-Shaking" — 消除死代码，产物最小化

先来玩个文字游戏：**Tree-Shaking 摇的是"死代码"，而不是你的头发**。所以不用担心发际线，它只是 JavaScript 打包领域里的一个专有名词。

> **Tree-Shaking（树摇）是什么？**
> Tree-Shaking 是 Rollup（以及现代打包工具）使用的一种优化技术。它的原理很简单：利用 ES Module 的静态结构（在代码运行之前就能确定导入和导出关系），找出那些"导出了但没有任何地方导入"的代码，然后把这些"死代码"从最终的打包产物中剔除出去。就像摇晃一棵树，把枯死的叶子摇掉，只留下活着的枝叶。

举一个让人会心一笑的例子：

```javascript
// utils.js
export function add(a, b) {
  return a + b; // 世界需要你！
}

export function deleteEverything() {
  // 这个函数没人用，但它会污染你的代码库
  console.log('我被导出了，但我永远不会被调用，哼');
}

// main.js
import { add } from './utils.js';

console.log(add(1, 2)); // 3
```

打包之后，`deleteEverything` 函数会被 Tree-Shaking 无情地剔除，就像你在收拾房间时把那些"说不定以后会用"的杂物直接扔进垃圾桶一样——痛快！

> ⚠️ **Tree-Shaking 的局限性：副作用问题**
> 上面例子里的 `deleteEverything` 函数之所以被删除，是因为它**没有任何副作用**——即它的执行不会影响到任何外部状态。但如果一个函数里有副作用（比如 `console.log`、修改全局变量、发起网络请求等），Rollup 会**保守地保留它**，因为它无法确定这个副作用是否真的"无用"。
> 
> 所以，如果你想让 Tree-Shaking 效果最大化，尽量使用**纯函数**的风格——把有副作用的代码和"只做计算"的代码分开。这样 Rollup 就能大展拳脚，把那些"只是算算算"的死代码全部剔除。

Tree-Shaking 之所以在 Rollup 中特别强大，是因为 **ES Module 的 import/export 语法是静态的**，编译器可以在不运行代码的情况下就分析出模块之间的依赖关系。这就像原版《哈利波特》直接看英文，和先翻译成中文再回译成英文的"二手货"对比——后者在来回翻译过程中难免丢失信息（比如注释、原始变量名、甚至语气），Tree-Shaking 就容易误判，把不该删的代码也一起"摇"掉了。

### 1.2.2 "Zero Runtime" — 极简运行时代码

"Runtime"（运行时）是什么概念呢？打个比方：

- **有 Runtime 的打包工具**（比如某些老版本打包方案）就像你去餐厅吃饭，服务员说"菜等会儿上，不过先送你一碗开胃小菜垫垫肚子"。问题是这碗小菜是强制赠送的，你可能根本不饿，而且它还要占你胃的空间。
- **Zero Runtime 的打包工具**（Rollup 走的就是这条路）则像是厨师直接把你要的主菜端上来，**不额外赠送任何东西**。你点了啥，就只给你做啥。

具体来说，Rollup 在打包时**极力避免**往最终产物里注入额外的"包装代码"。对于纯 ES Module 代码，Rollup 的产物几乎就是源代码的直接翻译——没有 `_interopRequireDefault` 这类 helper 函数，就是干干净净的 ES Module 代码。在现代浏览器原生支持 ES Module 的环境下，这就是最理想的"零包袱"产物。

不过，凡事都有例外——如果你的代码里用 `output.name` 导出了全局变量（通常用于 IIFE/UMD 格式），Rollup 会保留一个全局变量的赋值语句；又或者你混入了 CommonJS 模块，Rollup 也会加一点点"翻译层"来让两者和平共处。但这些都属于"迫不得已"的情况，能省则省。

不过说句实话，"Zero Runtime"这个说法略有营销成分——当你的代码有**多入口**、**动态导入**，或者需要**保留模块结构**时，Rollup 还是需要一小段 runtime 代码来协调模块加载。但相比某些老一代打包工具动辄几十 KB 的 runtime，Rollup 的 runtime 通常只有几百字节到几 KB，可以说是"轻如鸿毛"了。（悄悄告诉你：虽然名字叫"Zero Runtime"，但 Rollup 其实从来没有真正实现过零 runtime——它只是把 runtime 做得很小很小而已 🤫）

来看一个对比（简化版）：

```javascript
// 源代码
export const PI = 3.14159;
export function circleArea(r) {
  return PI * r * r;
}
```

Rollup 打包后（ES 格式）：

```javascript
const PI = 3.14159;
function circleArea(r) {
  return PI * r * r;
}

export { PI, circleArea };
```

干净利落，没有多余的运行时包袱。对比一下 Webpack 之类的老一代打包工具——它们往产物里塞 `__esModule` 标记、`_interopRequireDefault` 这样的 helper 函数，还要内置一整套模块系统的包装代码，产物膨胀得像个充了气的河豚。Rollup？不需要这些，因为浏览器原生就认识 ES Module。

### 1.2.3 原生 ES Module 支持，无需转换

这是 Rollup 区别于很多老一代打包工具的关键点。

早期的 JavaScript 打包工具（比如 Webpack 的早期版本）在处理模块时，需要先把 ES Module 语法转换成自己内部的模块表示形式，然后再处理。这个"翻译"过程有时候会造成信息丢失——比如某些语法特性在转换过程中变得面目全非，Tree-Shaking 就难以准确判断哪些代码是死代码了。

而 Rollup 从一开始就是**为 ES Module 而生的**，它直接理解 ES Module 的静态结构，不需要中间的"翻译层"。这意味着：Tree-Shaking 拿到的信息是完整的、原始的，没有被转换过程"污染"过，自然就能更精准地判断哪些代码该删、哪些该留。

还有一个顺便带来的好处：**Scope Hoisting（作用域提升）**🌳。因为 ES Module 之间的依赖关系在编译阶段就已确定，Rollup 可以大胆地把所有模块的代码"拍平"到同一个作用域里——原本分散在各个模块里的函数调用，直接变成顺序执行的代码，没有中间层、没有闭包的包袱。这不仅减少了函数调用开销，还为后续的压缩工具（如 Terser）创造了更大的优化空间。一个典型的例子是：

```javascript
// a.js
export const name = 'Alice';

// b.js
import { name } from './a.js';
export function greet() {
  return `Hello, ${name}!`;
}

// main.js
import { greet } from './b.js';
console.log(greet());
```

打包后，Rollup 会把它们合并成单一作用域，`name` 和 `greet` 都是顶层变量，`greet` 直接引用 `name`，不需要任何模块层的中间数据结构。这就是 Scope Hoisting 的魔力。

---

## 1.3 Rollup 的核心特性一览

Rollup 的特性列表不长，但每一条都精准地戳在开发者的痛点上。我们来一个一个品味。

### 1.3.1 Tree-Shaking（静态分析消除未使用代码）

这条特性我们在 1.2.1 节已经详细介绍过了，它是 Rollup 最招牌的能力。你可以把 Rollup 想成你代码的"健身教练"——专门负责把你代码里那些臃肿的肥肉（死代码）给甩掉。

### 1.3.2 多格式输出（ES / CJS / UMD / IIFE / AMD / System）

Rollup 支持一次性输出多种格式，就像同一家餐厅可以同时提供外卖盒饭、商务套餐和米其林三星料理，满足不同"消费者"的需求：

- **ES 格式**：给现代浏览器和其他打包工具用（Vite 生产构建用的就是这种格式）
- **CJS 格式**：给 Node.js 环境用（`require()` 语法）
- **IIFE 格式**：浏览器 `<script>` 标签直接引用，不需要任何模块系统（需要配合 `output.name` 设置全局变量名）
- **UMD 格式**：同时兼容浏览器、Node.js 和 AMD，一份代码走天下（也需要 `output.name`）
- **AMD 格式**：给 RequireJS 用户用（比较小众）
- **System 格式**：给 SystemJS 元编程加载器用（更小众）

这种灵活性对于要发布 npm 包的人来说简直是福音——你只需要写一份源码，Rollup 可以帮你同时打包出好几种格式，消费者根据他们的环境各取所需。

> **Tip：** 插件执行的顺序是**从上到下**，而每个插件内部处理文件的顺序则取决于它的 hook 类型（transform、load、resolve 等）。这个顺序有时候很重要——比如你得先 `resolve` 再 `commonjs`，顺序搞反了可能会原地爆炸 💥

### 1.3.3 代码分割（Code Splitting / Dynamic Import）

代码分割是什么？想象你网购了一个巨型家具，结果快递只发了一个巨大的木箱，里面凳子、桌子、椅子、螺丝钉全搅在一起，你得自己一件一件掏出来分类。而代码分割就像是快递公司帮你把货物分成了好几个箱子：凳子一箱、桌子一箱、椅子一箱，你需要什么的时候再拆对应的箱子。

> **Dynamic Import（动态导入）是什么？**
> Dynamic Import 是 ES2020 引入的一种按需加载语法，它允许你只在真正需要某个模块的时候才加载它，而不是一开始就把所有代码全部下载下来。语法就是 `import('./module.js')`，它返回一个 Promise。

**重要提示：** Rollup 的代码分割需要满足两个条件才生效：
> 1. 必须使用 `import()` 动态导入语法（普通 `import` 静态导入的代码会被打包进同一个 chunk）
> 2. 必须配置 `output.dir`（多入口输出目录）或 `output.manualChunks`（手动拆分策略）——只有配置了这些选项，Rollup 才会将动态导入的模块拆分成独立的 chunk 文件；如果同时有多个入口文件，Rollup 还会自动把共享的依赖抽离成独立的 shared chunk

在 Rollup 中，当你使用动态导入时，Rollup 会自动把被导入的模块打包成独立的 chunk（文件），实现代码分割。

```javascript
// main.js — 页面刚加载时只加载这个文件
import { showAlert } from './alert.js';
showAlert('欢迎来到我的网页！');

// router.js — 只有用户点击"购物车"按钮时才加载
document.getElementById('cartBtn').addEventListener('click', async () => {
  // 这一行代码执行时，才会去下载并执行 cart.js
  const { showCart } = await import('./cart.js');
  showCart();
});
```

这样一来，用户第一次访问网页时只需要下载 `main.js`，购物车相关的代码只有在用户真的点了购物车按钮之后才会加载，既节省流量又加快首屏速度。

### 1.3.4 高度可配置的插件系统

Rollup 的插件系统是它的灵魂所在。想象一下，Rollup 本身是一个没有感情的打包机器，而插件就是给它装上了各种各样的工具——有的插件让它能读取 TypeScript，有的让它能压缩代码，有的让它能处理 CSS……

> **插件（Plugin）是什么？**
> 插件本质上是一个带有特定生命周期钩子（hook）的函数或者对象。你可以把 Rollup 的打包过程想象成一条流水线，文件从一端进去，经过一个个插件的加工，最后从另一端出来变成打包好的文件。每个插件都可以在这条流水线上拦截、修改、转换文件内容。

```javascript
// rollup.config.js
import resolve from '@rollup/plugin-node-resolve'; // 解析 node_modules
import commonjs from '@rollup/plugin-commonjs';    // 把 CommonJS 转成 ESM
import terser from '@rollup/plugin-terser';         // 压缩代码

export default {
  input: 'src/main.js',      // 入口文件
  output: {
    file: 'dist/bundle.js',  // 输出文件
    format: 'es'              // 输出格式：ES Module
  },
  plugins: [
    resolve(),                // 让 Rollup 能找到 node_modules 里的模块
    commonjs(),               // 把 CJS 模块转成 ESM
    terser()                  // 把代码压缩混淆，减小体积
  ]
};
```

> **Rollup 原生不支持 TypeScript、JSX、CSS 和资源文件（图片、字体等）！** 这是新手最常踩的坑。Rollup 本身只处理 JavaScript 文件，任何 TypeScript、JSX、CSS 的转换都需要相应的插件（推荐 `@rollup/plugin-typescript`、`@rollup/plugin-babel` 处理 JSX、`rollup-plugin-postcss` 处理 CSS）。另外，从 **Rollup 3.0** 开始，内置的 CommonJS 支持被移除了，如果你要打包包含 `require()` 语法的 CJS 模块，必须使用 `@rollup/plugin-commonjs`。好消息是，Vite 在开发阶段帮你把这一切都配置好了，所以用 Vue/React+Svelte 开发时你感受不到这些繁琐的插件配置。

### 1.3.5 Source Map 生成 — 快速定位线上问题

Source Map 可以理解为代码的"导航地图"。上线后的 JavaScript 代码通常是被压缩混淆过的，如果浏览器控制台报错，你看到的就是一行乱码，根本无法定位问题。Source Map 就是那个能把你从压缩后的代码"导航"回原始源代码的神器。

```javascript
// rollup.config.js
export default {
  input: 'src/main.js',
  output: {
    file: 'dist/bundle.js',
    format: 'es',
    sourcemap: true  // 生成 .map 文件，浏览器用它来还原源代码
  }
};
```

开启后，Rollup 会同时输出 `bundle.js.map` 文件（或者内联到 bundle.js 末尾的 inline 模式），在 Chrome DevTools 中你就能像调试源代码一样自在地打断点、看变量值了。

> **小技巧：** `sourcemap` 可以是布尔值，也可以是 `'inline'`（内联到产物中）或 `object`（精细控制），比如 `{ exclude: ['node_modules/**'] }` 可以排除某些文件的 Source Map 生成。

---

## 1.4 Rollup 快速上手：安装与基础用法

光说不练假把式，让我们来看看如何用 Rollup 打包你的第一个项目。

> **小知识：** Rollup 本身是用 JavaScript 编写的，但它底层用到了 Node.js 的标准库。所以不管你用什么编辑器，只要装好了 Node.js，就能跑 Rollup。

### 1.4.1 安装 Rollup

Rollup 可以通过 npm 或 yarn 全局安装，也可以作为项目本地依赖：

```bash
# 全局安装（命令行使用）
npm install -g rollup

# 项目本地安装（推荐，配合 npm scripts）
npm install --save-dev rollup

# 或者用 yarn
yarn add -D rollup
```

### 1.4.2 最简单的打包命令

Rollup 的命令行使用方式非常直观：

```bash
# 打包单个入口文件，输出到控制台
rollup src/main.js

# 指定输出文件
rollup src/main.js --file dist/bundle.js

# 指定输出格式
rollup src/main.js --file dist/bundle.js --format es
```

常用的 CLI 参数：
- `--format`：输出格式（`es`、`cjs`、`umd`、`iife`、`amd`、`system`）
- `--file`：输出文件名
- `--watch`：监听文件变化，自动重新打包（开发时用）
- `--external`：指定外部依赖（如 `react`、`react-dom`），不打包进产物

### 1.4.3 配置文件：更强大的打包策略

对于稍微复杂一点的项目，推荐使用配置文件 `rollup.config.js`：

```javascript
// rollup.config.js
export default {
  input: 'src/main.js',      // 入口文件
  output: {
    file: 'dist/bundle.js',  // 输出文件
    format: 'es',            // 输出格式
    name: 'MyLibrary',       // IIFE/UMD 格式下，挂载到 window.MyLibrary
    sourcemap: true          // 生成 source map
  }
};
```

这里的 `name` 选项就是刚才说的——如果你打包成 IIFE 或 UMD 格式，就必须告诉 Rollup 把你的模块挂到哪个全局变量上。

然后运行：

```bash
rollup --config
```

**小贴士：** 如果你的项目使用 Node.js 16+ 且 `package.json` 中有 `"type": "module"`，Rollup 会自动读取 `rollup.config.js`，不需要加 `--config` 参数。当然，如果你配置文件的名字不是 `rollup.config.js`（比如 `rollup.config.mjs`），那就得显式指定了。

### 1.4.4 与 npm scripts 配合

在 `package.json` 中添加 scripts：

```json
{
  "scripts": {
    "build": "rollup --config",
    "build:watch": "rollup --config --watch"
  }
}
```

这样你就可以用 `npm run build` 来打包了。

---

## 1.5 Rollup vs Webpack：定位与适用场景对比

这是一个在社区里被讨论了无数次的话题。让我用一个生活化的比喻来把这个问题讲清楚。

### 1.5.1 Rollup：库 / 工具 / 组件打包，追求体积最小化

如果把你的项目比作一艘宇宙飞船：

- **Rollup** 就像是专门制造卫星的专业工厂，专注于把卫星造得又轻又结实，能省下宝贵的火箭燃料（网络流量）。每多一克重量都是罪过，所以 Rollup 会把卫星上的每一个螺丝钉都检查一遍，确保没有多余的零件被装上去。

用它来打包一个 npm 库？Rollup 几乎是目前社区公认的最佳选择。产物小、干净、Tree-Shaking 效果一流，最终用户的浏览器只需要下载真正有用的代码。

### 1.5.2 Webpack：应用打包，追求功能丰富与生态完整

继续上面的比喻：

- **Webpack** 就像一个综合性的航天飞机维修中心，里面有机械臂、检测仪、氧气管、导航系统……什么工具都有。它的目标是让你能建造一艘功能齐全的宇宙空间站，支持热更新、代码分割、样式处理、图片优化、服务端渲染……所有你能想到的功能它都有插件支持。

但代价是什么？系统复杂，配置繁多，学习曲线陡峭，而且"出厂"的飞船可能比 Rollup 造的要重一些（因为自带了很多工具）。当然，Webpack 5 引入了更好的 Tree-Shaking 支持和更高效的缓存机制，两者的差距已经比早年间缩小了不少——只是 Rollup 在库打包这个细分领域，依然是那个追求极致精简的偏执狂。

### 1.5.3 实际边界：大型应用也有用 Rollup 的场景

> 这里要打破一个常见的误解：大型应用只能用 Webpack，不能用 Rollup。

实际上，有一个你可能每天都在用的工具——**Vite**——它的生产构建就是用 Rollup 打包的。Vite 的开发服务器用的是 esbuild（另一个超快的打包工具），快是快，但压缩和 Tree-Shaking 效果不如 Rollup 精细。所以当你执行 `vite build` 的时候，它底层跑的就是 Rollup，为的就是产出更优质的生产代码。所以当你用 Vue3、React、SvelteKit 这些现代框架开发大型应用时，你其实已经在用 Rollup 了，只是你可能没意识到而已。

这就像你去一家餐厅吃饭，后厨是谁在炒菜你不需要知道，你只关心菜好不好吃。

> **简单记忆法：**
> - **你的代码要给别的开发者用（npm 包 / 组件库）** → 选 Rollup
> - **你的代码要给最终用户用（网站 / Web 应用）** → 用 Vite（底层 Rollup）或 Webpack

---

## 本章小结

这一章我们揭开了 Rollup 的神秘面纱：

1. **Rollup 是什么**：一个专注于 ES Module 的 JavaScript 打包工具，核心理念是 Tree-Shaking（消除死代码）、Zero Runtime（极简运行时代码）和原生 ES Module 支持。

2. **核心特性**：Tree-Shaking 死代码消除、Scope Hoisting 作用域提升、多格式输出（ES/CJS/UMD/IIFE/AMD/System）、代码分割（Dynamic Import，需要配置 `output.dir` 或 `manualChunks`，多入口时自动共享依赖）、插件系统、Source Map 生成。IIFE/UMD 格式还需要 `output.name` 来指定全局变量名。**注意**：Rollup 原生不支持 TypeScript、JSX、CSS 等，需要相应插件；Rollup 3.0 起移除了内置 CommonJS 支持，需使用 `@rollup/plugin-commonjs`。

3. **快速上手**：可以通过 CLI 直接打包，也可以使用 `rollup.config.js` 配置文件。推荐本地安装配合 npm scripts 使用。配置文件注意插件执行顺序是从上到下。

4. **与 Webpack 的关系**：两者定位不同——Rollup 擅长打包库和工具，追求产物体积最小化；Webpack 擅长打包应用，功能丰富但配置复杂。Vite 生产构建就是用 Rollup，所以 Rollup 其实离你很近。

下一章我们将穿越时空，聊聊 Rollup 的诞生史和版本演进——看看这个"固执的小厨子"是怎么一步步走到今天的。