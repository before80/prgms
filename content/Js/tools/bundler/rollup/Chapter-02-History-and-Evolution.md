+++
title = "第2章 历史与演进"
weight = 20
date = "2026-03-28T11:38:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 2 章　历史沿革与版本演进

---

## 2.1 诞生背景

2008 年，Chrome V8 引擎的诞生让 JavaScript 第一次有了"快"的可能；2015 年，ES6（ES2015）正式落地，JavaScript 有了官方的模块系统。就在这样的时代背景下，一个叫 **Rich Harris** 的开发者开始尝试一种新的打包方式，并于 2015 年创建了 **Rollup**。

当时的打包工具市场，要么是笨重的 Webpack，要么是面向 Node.js 的 Browserify。Rich Harris 想要更直接地利用 ES Module 的静态结构，生成干净、小巧的 bundle，并尽可能剔除未使用的代码。这个思路后来成为 Rollup 的核心卖点，也让 Rollup 成为 Svelte 生态的重要基础设施。

于是他一不做二不休，自己动手写了一个。2015 年，Rollup 诞生了。

### 2.1.1 首次发布：一个人写出的打包工具

Rich Harris 不是一般人——他是那种"现有的工具不好用我就自己造一个"的典型代表。他后来创造的 Svelte 框架也是同样的思路：现有的框架太重了，我不如自己写一个更优雅的。

Rollup 的第一个版本发布在 GitHub 上，虽然粗糙，但核心思想非常超前：基于 ES Module 做 Tree-Shaking。

> 🎵 **冷知识**：Rollup 名字的灵感来自音乐制作中的 "roll up"——把所有音轨合并成一条。打包工具嘛，不就是把各种模块"卷"（roll up）在一起吗？起名简单直白，但回看历史，这个名字起得还挺有预见性的：它后来确实成了把 JavaScript 模块"卷"成最优 bundle 的利器。

GitHub 上那个最早的提交信息写的是：*"first commit"*- 是的，就是这么朴实无华且枯燥。但正是这个"first commit"，埋下了后世最优雅打包工具的种子。

### 2.1.2 初衷：更好地打包 ES Module

Rollup 的目标是直接以 ES Module 为输入和输出，充分利用静态 import/export 信息做 Tree Shaking。Svelte 在 2016 年发布后，也采用了 Rollup 作为推荐的打包工具，因此很多人会把 Rollup 与 Svelte 联系在一起；但 Rollup 并不是专门为 Svelte 而生的。

Rollup 的定位可以概括为：**以 ES Module 为核心输入，把 Tree Shaking 做到极致**。

### 2.1.3 灵感来源：Google Closure Compiler 的死代码消除思想

说到 Tree-Shaking 的灵感，Rich Harris 本人提到过 Google 的 **Closure Compiler** 是重要的灵感来源之一。Closure Compiler 是 Google 用 Java 写的一个 JavaScript 优化工具，它可以分析 JavaScript 代码并移除未使用的代码——这其实就是 Tree-Shaking 的雏形。

不过 Closure Compiler 太重量级了——它基于 Java，需要 JVM 环境，对 JavaScript 开发者来说门槛不低。Rich Harris 想的是：**能不能用更轻量的方式做到同样的事？** 结果他一不小心就造出了一个被全世界开发者喜爱的打包工具。

---

## 2.2 0.x 时代（2015—2017）：概念验证阶段

Rollup 的 0.x 时代就像一颗刚发芽的种子——充满潜力，但还不够成熟。

### 2.2.1 API 不稳定，插件生态几乎为零

最早的 Rollup API 和现在完全不一样。那时候插件系统还不存在，Rollup 的命令行接口（CLI）功能也比较简陋，能做的事情非常有限——不过它其实一直都有 JavaScript API，只是那个 API 设计得比较原始，用来用去基本就是打个包，没啥扩展性可言。

这就好比你买了一台功能机，预装了电话和短信，但应用商店？别想了，没有。你想加个微信？自己改源码去。

### 2.2.2 虽支持多种输出格式，但 Tree-Shaking 几乎无用武之地

早期的 Rollup（0.x）仅支持 ES Module 作为输入格式（所以彼时的输入源基本只有 Svelte 编译器），输出则支持 `cjs`（CommonJS）、`es`（ES Module）、`iife`（立即执行函数）和 `umd`（通用模块定义）四种格式。那个年代最主流的用法还是打 `cjs` 包——毕竟 ES Module 在浏览器里跑不起来，在 Node.js 里支持也相当有限。

回头看这段历史，你会发现一个有趣的反转：**Rollup 最早其实是用来打 CJS 包的**，而它的核心优势——Tree-Shaking——反而在当时没什么用武之地。不过这里有个常见的误解：很多人以为 CJS 完全无法 Tree-Shaking，其实不对。CJS 的 require 是动态的，但只要你导出的内容是静态可分析的，Rollup 依然能帮你剪掉从未被 import 的那一半。只是相比 ES Module 的原生静态分析，CJS 下的 Tree-Shaking 效果确实大打折扣——这大概就是"基因好但生不逢时"的典型代表。

---

## 2.3 1.x 时代（2017—2019）：插件 API 奠基

2017 年，Rollup 发布了 1.0 版本，这是 Rollup 历史上的重要转折点。值得注意的是，1.0 是一次"壮士断腕"式的升级——大量 0.x 时代的 API 在 1.0 中不再兼容，从 0.x 升级上来的用户不得不重写配置。不过这次 break 也换来了更干净的插件架构，为后来插件生态的蓬勃发展打下了基础。

### 2.3.1 build / generateBundle 两阶段插件钩子系统确立

这是 Rollup 历史上最重大的架构升级之一。Rollup 团队定义了插件的两大执行阶段：

> **build 阶段**（也叫 buildStart、resolve、load、transform）：在这个阶段，Rollup 读取源码、解析依赖、转换代码。插件可以拦截这个过程中的任何一步，比如把 TypeScript 转成 JavaScript，把 SCSS 转成 CSS——只要你愿意，甚至可以把图片转成 Base64 塞进代码里（虽然我们不太推荐这么做）。

> **generateBundle 阶段**：在所有模块都被处理完毕、准备生成最终打包文件时触发。插件可以在这个阶段生成或修改 chunk、asset、Source Map 等最终输出。Rollup 1.0 还废弃了更早的 `ongenerate`、`onwrite` 等旧钩子，插件 API 从此逐渐稳定下来。

这种两阶段设计让插件可以精确地控制打包过程中的每一个环节——你可以把 Rollup 的插件系统想象成一个**流水线**，每一步都有检查点，插件想在哪儿插队就在哪儿插队，想改什么就改什么，相当自由。这也是后来 Rollup 插件生态蓬勃发展的技术基础。

### 2.3.2 官方插件陆续发布（node-resolve / commonjs / babel）

1.x 时代，Rollup 官方推出了第一批插件：

- `@rollup/plugin-node-resolve`：让 Rollup 能找到 `node_modules` 里的模块（没有这个插件，Rollup 根本不知道去哪里找第三方依赖）
- `@rollup/plugin-commonjs`：把 CommonJS 格式的模块转成 ES Module（因为 npm 上大量的包还是 CJS 格式）
- `@rollup/plugin-babel`：用 Babel 转译代码，支持 JSX、TypeScript 等语法

这三剑客直到今天依然是大多数 Rollup 配置中的标配。

### 2.3.3 Vue 生态率先采纳（npm 生态跟进）

Vue 生态是第一个大规模采用 Rollup 的阵营。Vue 3 的源码从一开始就用 Rollup 打包，Vue 生态中的众多官方周边库（如 Vite、Vitest、svelte-preprocess 等）也都纷纷跟进——这给 Rollup 带来了巨大的曝光度和社区信任。可以说 Rollup 早期能活下来，很大程度上靠的是 Vue 生态的背书。

---

## 2.4 2.x 时代（2019—2022）：全面拥抱 ES Module

2019 年，Rollup 2.x 发布，这是 Rollup 走向成熟的标志性版本。

### 2.4.1 ES Module 输出支持大幅完善

2.x 版本对 ES Module 的输出支持更加完善——实际上 Rollup 从 0.x 起就支持 ES Module 输入，但 2.x 才真正完善了 ES 格式的输出能力。这为 Tree-Shaking 的效果提供了最大保障——因为全程没有中间格式的转换，信息零损失。

### 2.4.2 Tree-Shaking 大幅改进（基于 ES Module 静态分析）

2.x 版本对 Tree-Shaking 算法做了大量优化。在这个版本中，Tree-Shaking 不再是简单的"移除未使用的 export"，而是进化成了真正的"静态代码分析"——可以分析函数调用链、判断变量是否真的被使用，甚至可以处理 `if (false)` 这种不可达代码分支，以及**纯函数**（pure function）的内联优化。

值得一提的是，2.x 还引入了**作用域提升（Scope Hoisting）**——Rollup 会把模块的代码"提升"到同一个作用域里，把原本分散的函数包装合并掉。这让输出代码不仅体积更小，运行时的作用域查找开销也更低。可以理解为：Tree-Shaking 负责剪枝，Scope Hoisting 负责把剪完的枝干拼成更简洁的形状——两者配合，产物质量才能达到最优。

说到纯函数，这里有个很实用的技巧：**`/* @__PURE__ */` 注释**。如果你有一个函数调用本身没有副作用，但 Rollup 无法自动判断（比如调用了一个外部库函数），你可以在调用前加上 `/* @__PURE__ */` 注释，告诉 Rollup："这个调用是纯的，可以放心地当死代码删掉"。比如：

```js
/* @__PURE__ */ someHelper()
```

这在优化第三方库依赖时特别有用——一个被 tree-shake 掉的无用模块，如果它的顶层代码有副作用，Rollup 可能就不敢删它。加上 `/* @__PURE__ */` 就相当于给 Rollup 吃了颗定心丸。

> 💡 **配套技巧**：`/* @__PURE__ */` 是标注**某个调用表达式**是纯的，而 `/* @__NO_SIDE_EFFECTS__ */` 则是标注**函数声明**本身没有副作用。比如 `/* @__NO_SIDE_EFFECTS__ */ function helper() { ... }`，Rollup 就会知道：调用这个函数本身不会产生副作用，如果它的返回值没被用到，整个函数调用都可以安全地删除。两者配合使用，优化效果更佳。

> 🔮 **趣闻**：虽然 Rich Harris 最早将 Tree-Shaking 实践落地，但"Tree-Shaking"这个名字在 JavaScript 社区的流行，更多是 Rollup 和 webpack 共同推广的结果——两边的团队都在用这个词来形容死代码消除。更有意思的是，这个术语其实借鉴自造纸工业的术语"tree shaking"，指的是在造纸前把树枝上的枯叶摇下来——没用的一律不要，跟我们打包时剔除死代码是一个道理。

> 📊 **对比**：Rollup 的 Tree-Shaking 和 webpack 的 Tree-Shaking 有一个本质区别：**Rollup 是完整地分析整个模块图后再打成一个 bundle，webpack 是分成多个 chunk 独立分析**。这意味着 Rollup 的 Tree-Shaking 通常更彻底——因为它能看到完整的依赖链，知道哪些 export 真的没被用过。而 webpack 在代码分割场景下，每个 chunk 独立分析，可能会漏掉一些跨 chunk 的优化机会。不过 webpack 也在不断追赶，两者的差距已经越来越小了。

### 2.4.3 性能显著提升，构建速度成倍优化

2.x 版本对打包性能做了大量重构，构建速度有了显著提升。对于习惯了 Webpack 漫长构建等待的开发者来说，这简直是一种解放——从"等一杯咖啡泡好还没构建完"进化到了"喝口水的功夫就打好了"，虽然夸张了点，但意思就是这么个意思。

### 2.4.4 watch 模式稳定可用

**watch 模式**是什么？简单说就是让 Rollup 监听文件变化，当你的源代码发生变化时，自动重新打包。这个功能在开发插件和库的时候特别有用——你改一行代码，不用手动去敲打包命令了。watch 模式的加入，让 Rollup 在开发阶段的体验上了一个台阶，终于不是一个每次改完代码还得手动敲命令的"一次性"工具了。

---

## 2.5 3.x 时代（2023—2024）：功能完善期

2023 年，Rollup 3.x 发布。这一时期的 Rollup 已经是一个非常成熟的工具了，3.x 更多是在修补完善和适配新的生态需求。

### 2.5.1 代码分割能力增强

代码分割（Code Splitting）是什么意思？简单说就是把一个大包拆成多个小包，按需加载。比如你写了一个日历组件和一个图表组件，把它们打成一个巨大无比的 bundle 实在没必要——用户可能只用到日历，用不到图表，为什么要下载图表的代码？代码分割就是解决这个问题的。

3.x 版本对动态导入（`import()`）的处理更加智能，可以更好地处理跨 chunk 的模块共享问题——简单来说就是：同一个模块被多个 chunk 引用时，不会傻傻地复制 N 份，而是抽取出来做成共享模块，按需加载。这在大型应用里能显著减小产物体积。

### 2.5.2 import.meta 完整支持

`import.meta` 是 ES2020 引入的一个元属性，它提供关于当前模块的上下文信息。最常见的用法是 `import.meta.url`——拿到当前模块文件的 URL，这在处理静态资源路径时特别有用（比如在 Node.js 里，你知道模块在哪个文件，就能反推出同级目录下其他资源的路径）。3.x 版本完整支持了这个特性，让 Rollup 能更好地处理现代 JavaScript 的各种特性。

### 2.5.3 export conditions 支持（exports 字段多条件导出）

`package.json` 中的 `exports` 字段是 Node.js 12+ 支持的一种**条件导出**机制，它允许你根据不同的条件（是 `import` 还是 `require`？是浏览器还是 Node？）提供不同的入口文件。比如你写了一个库，可以做到：**浏览器环境用 ESM 版本（体积小、支持 Tree-Shaking），Node.js 环境用 CJS 版本（直接 require 就行）**，不用自己手动维护两套包。3.x 版本对这个机制的支持让 Rollup 能更准确地解析 npm 包的导出路径。

### 2.5.4 与 Vite 深度绑定（Vite 1–7 使用 Rollup 做生产构建）

这里要特别提一下 **Vite**。Vite 是 2020 年出现的构建工具，Vite 1–7 的经典架构是开发时用 esbuild（极快）、生产时用 Rollup（产物质量高）。这大幅扩大了 Rollup 的用户群，因为大量 Vite 开发者在生产构建阶段实际上都在使用 Rollup。到 **Vite 8（2026 年 3 月）**，生产与开发构建统一改为 **Rolldown**，因此“所有 Vite 项目都在用 Rollup”只适用于 Vite 7 及之前。

---

## 2.6 4.x 时代（2024—）：持续进化

2024 年，Rollup 4.x 正式发布。这一版本的 Rollup 在性能和功能上都有显著提升。

### 2.6.1 更快的解析与打包速度

Rollup 4 使用 **SWC** 作为解析器（不再使用 Acorn），解析速度相比 3.x 有明显提升。与此同时，Rollup 4 开始通过可选的原生依赖提供 Rust 实现，并移除了 `acorn`、`acornInjectPlugins` 等旧配置入口。对大型项目来说，这些改动能实实在在减少构建时间。

### 2.6.2 改进的 TypeScript 支持

4.x 对 TypeScript 的处理更加智能，类型擦除（TypeScript 编译时删除类型信息）的过程更加干净，不会产生干扰 Tree-Shaking 的冗余代码。以前有些 TypeScript 代码在编译后会产生一些"看起来有用但实际没用"的中间代码，Rollup 会误以为这些代码有副作用（side effect）而不敢删除——4.x 改善了这一点，让 Tree-Shaking 更加激进（激进是好事，越少冗余代码越好）。

### 2.6.3 更完善的 Source Map

4.x 版本的 Source Map 生成更加精确，调试体验更好。

### 2.6.4 output.generatedCode 选项（控制 Rollup 自己生成的辅助代码语法）

`output.generatedCode` 允许你指定 Rollup 在生成包装代码、helper 等**自己产生的代码**时可以使用哪些 JavaScript 特性。例如设置成 `es2015`，Rollup 会在自己的辅助代码中放心使用 ES2015 语法。注意它**不会转译你的业务代码**，只影响 Rollup 生成的胶水代码。

```js
export default {
  output: {
    generatedCode: {
      preset: 'es2015',
      // 或者精细化控制
      constBindings: false,
      objectShorthand: true
    }
  }
};
```

### 2.6.5 使用 perf 选项查看构建耗时

Rollup 没有名为 `compiletime` 的配置项；官方提供的性能分析开关是 `perf`。开启后，Rollup 会在构建结束时输出各阶段耗时，帮助你定位瓶颈：

```js
export default {
  perf: true
};
```

输出大致长这样：

```
build start      12.34ms
parse modules    45.67ms
generate chunks 23.45ms
✓ built in 81.46ms
```

哪个阶段最慢，就重点优化哪个阶段。有种"性能分析报告"的感觉，妈妈再也不用担心我不知道时间去哪儿了。

### 2.6.6 generateBundle 是稳定的输出阶段钩子

`generateBundle` 用于在打包文件写入磁盘前修改或生成最终输出。它在 Rollup 1.0 时代就已经成为稳定的核心钩子；Rollup 1.0 同时废弃了更早的 `ongenerate`、`onwrite` 等旧写法。它并不是在 4.x 才从 `renderBundle` 改名的。

### 2.6.7 output.inlineDynamicImports 是输出选项

`inlineDynamicImports` 一直是**输出选项**，应写在 `output` 中，用于把动态导入内联到单个 bundle。它并不是 Rollup 4.x 才从顶层移入 `output` 的。它要求只有一个入口，并且会改变动态导入模块的执行时机。

---

## 2.7 Rolldown：Vite 生态的新打包器

Rollup 生态的下一个重要项目是 **Rolldown**——由 VoidZero 团队用 Rust 开发的打包器。

### 2.7.1 Rust 重写，预计带来数量级性能提升

Rolldown 用 Rust 语言实现了兼容 Rollup 的插件 API，并基于 Oxc 等 Rust 工具链进行解析、转换和打包。Rust 带来的并行能力和原生执行效率，使它在大型项目中有机会显著缩短构建时间。

按照 Vite 8 官方公布的数据，Rolldown 路径在部分真实项目中带来了 10–30 倍的构建速度提升；具体收益取决于项目规模、依赖结构和插件复杂度。

> 💡 **背景补充**：Rolldown 由 Evan You 创立的 VoidZero 团队推进，目标是为 Vite 生态提供统一、快速、兼容 Rollup 插件 API 的底层打包器。

### 2.7.2 与 Vite 的深度整合计划

Rolldown 的目标是**成为 Vite 的默认打包器**。Vite 7 通过 `rolldown-vite` 提供了技术预览；Vite 8 已正式把 Rolldown 作为默认且统一的打包器，开发和生产不再需要维护 esbuild、Rollup 两套独立管线。

### 2.7.3 Rolldown 的现状与展望

Rolldown 已在 **Vite 8（2026 年 3 月）** 中成为默认且统一的打包器。它与 Rollup 插件 API 高度兼容，大量插件可以相对平滑地迁移；但底层运行时不同（JavaScript vs Rust），依赖 Rollup 内部实现或特殊行为的插件仍需要验证。Vite 8 提供配置兼容层，复杂项目应参考官方迁移指南逐步升级。

对于 Rollup 用户来说，Rolldown 的到来既是挑战也是机遇——Rolldown 会继承 Rollup 所有的优秀特性，同时带来性能上的质变。**Rollup.js 本身仍会持续维护，不会突然消失**，它仍然是学习 bundler 原理的最佳范本，毕竟底层原理不会因为语言改变而改变。

---

> 📦 **冷知识**：npm 上包名叫 `rollup`，但官方文档和官网都叫 **Rollup.js**。所以当你看到 `rollup` 包和 `rollup.js` 两个称呼时，知道它们是同一个东西就好了。另外，Rollup 的配置文件默认叫 `rollup.config.js`，不过在 3.x 之后也支持 `rollup.config.mjs`、`rollup.config.cjs` 等多种格式——这种"配置文件后缀自由"的设计，后来也被 Vite 学了过去。

## 本章小结

这一章我们回顾了 Rollup 从诞生到现在的完整历程：

1. **诞生背景**：2015 年由 Rich Harris 创建，核心目标是直接利用 ES Module 的静态结构做 Tree Shaking；后来 Svelte 等框架采用了 Rollup，但 Rollup 并非专为 Svelte 而生。

2. **0.x 时代**：概念验证期，功能简陋，插件生态为零，但已有原始的 JavaScript API。

3. **1.x 时代**：插件 API 奠基，推出 node-resolve/commonjs/babel 三剑客，Vue 生态率先采纳。

4. **2.x 时代**：全面拥抱 ES Module，Tree-Shaking 大幅改进，构建速度成倍优化，watch 模式稳定可用。

5. **3.x 时代**：功能完善期，代码分割增强，import.meta 完整支持，export conditions 支持，与 Vite 深度绑定。

6. **4.x 时代**：性能持续提升，改用 SWC 解析器并引入原生依赖；`output.generatedCode` 控制 Rollup 辅助代码语法，`perf` 用于分析构建耗时。

7. **未来**：Rolldown 由 VoidZero 团队开发，并在 Vite 8 中成为默认的统一打包器；Rollup 本身仍会继续维护。
