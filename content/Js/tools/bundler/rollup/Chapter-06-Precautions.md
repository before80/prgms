+++
title = "第6章 注意事项"
weight = 60
date = "2026-03-28T11:38:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 6 章　需要注意哪些

---

## 6.1 Tree-Shaking 的前提条件

Tree-Shaking 是 Rollup 最招牌的功能，但它的效果取决于你如何使用它。理解它的前提条件，可以让你避免踩坑。

### 6.1.1 必须使用 ES Module 语法（import / export）

Tree-Shaking 只能作用于 ES Module 语法的代码。如果你的代码用的是 CommonJS 语法（`require()` / `module.exports`），Tree-Shaking 基本上无法工作。

**正确的写法**（支持 Tree-Shaking）：

```javascript
// utils.js
export function add(a, b) { return a + b; }
export function multiply(a, b) { return a * b; }
```

**错误的写法**（不支持 Tree-Shaking）：

```javascript
// utils.js
module.exports = {
  add: function(a, b) { return a + b; },
  multiply: function(a, b) { return a * b; }
};
```

为什么 CommonJS 不支持 Tree-Shaking？因为 `require()` 语法是**动态**的——你可以在运行时根据条件决定加载哪个模块，编译器无法在构建时确定你到底用到了哪些模块。

### 6.1.2 CommonJS 模块需要 @rollup/plugin-commonjs 转换

如果你依赖的 npm 包是 CommonJS 格式（这在 npm 上非常常见），你需要使用 `@rollup/plugin-commonjs` 把它转换成 ES Module，这样 Tree-Shaking 才能工作：

```bash
npm install -D @rollup/plugin-commonjs
```

```javascript
// rollup.config.js
import commonjs from '@rollup/plugin-commonjs';

export default {
  plugins: [
    commonjs()  // 把 CJS 模块转成 ESM，之后才能 Tree-Shaking
  ]
};
```

### 6.1.3 混用 CJS 与 ESM 可能影响 Tree-Shaking 效果

这是一个常见的性能陷阱。假设你的代码和你的依赖都是 CJS 格式，Rollup 可以通过 `@rollup/plugin-commonjs` 做转换，但转换后的代码质量通常不如原生 ES Module，Tree-Shaking 效果会大打折扣。

**最佳实践**：优先选择提供 ES Module 版本的 npm 包（查看包的 `package.json` 是否有 `module` 或 `exports` 字段）。比如 `lodash-es` 就是 lodash 的 ES Module 版本。

---

## 6.2 CommonJS 相关坑

CommonJS 是 Node.js 传统的模块格式，本来在 Node.js 里老老实实用着挺好。但一旦你的代码要和其他生态（比如 Rollup、ES Module）打交道，就会遇到各种奇奇怪怪的问题——简直是模块界的"万恶之源"。

### 6.2.1 默认不处理 CJS，必须引入 @rollup/plugin-commonjs

Rollup 的默认行为是**完全不处理 CommonJS 模块**。如果你不安装 `@rollup/plugin-commonjs`，Rollup 遇到 `require()` 语法会直接报错：

```
Error: 'require' is not defined by an ES Module
```

这是因为 Rollup 认为 ES Module 规范中不应该出现 `require`——这是对的，只是 npm 上有太多 CJS 包了，我们不得不处理它们。

### 6.2.2 __esModule 标记的副作用

`@rollup/plugin-commonjs` 在转换 CJS 模块时，会给模块添加一个 `__esModule: true` 的标记。这个标记对 Rollup 内部判断模块类型和做 ESM/CJS 互操作有用，但有时候会带来意想不到的副作用。

**主要问题场景**：当一个 CJS 模块 `require()` 了一个被 Babel 转换过的 ES Module 时，由于 Babel 也在转换产物上加了 `__esModule: true`，两套 `__esModule` 机制叠加，会导致：

- 如果你用 `import React from 'react'`（ESM 语法），Rollup 的互操作层能正确处理，返回 React 核心对象
- 但如果你在另一个 CJS 文件里用 `const React = require('react')` 再传给 ESM 代码，可能会因为 interop 多次处理而拿到意外的值

**实战建议**：尽量不要在 CJS 模块中 `require()` ESM 模块（尤其是 Babel 转换过的）。如果你需要混用，保持全部用 ES Module 语法导入。

### 6.2.3 named export 与 default export 混用问题

这是 CJS 和 ESM 混用时最常见的问题之一。

假设你有一个被 Babel 转换过的 ES Module（ESM default export），然后你用 CJS 的方式 `require` 它：

```javascript
// 一个典型的 Babel ESM→CJS 转换产物（简化版）
// 这是 Babel 把 ESM 转成 CJS 后的结果
module.exports = React;
module.exports.__esModule = true;
Object.defineProperty(module.exports, 'default', {
  value: React  // 把 React 实例挂到 .default 上
});

// 你用 CJS 方式 require 后再被 ESM interop 处理
const React = require('react');
// React 是 { __esModule: true, default: <React 实例> } 这个对象
// React.default 才是真正的 React 核心对象
// 如果你写成 const { Component } = require('react')
// Component 是 undefined（因为顶层 exports 上没有 Component，只有 .default 上有）
// ——这就是混用 CJS/ESM 时常见的坑
```

正确的方式是**全部使用 ES Module 语法**，让 Babel 和 Rollup 各司其职：
- Babel 只做语法转译（`@babel/preset-env` 的 `modules: false`）
- 模块解析和打包交给 Rollup 处理

### 6.2.4 require / module.exports 语法不直接支持

ES Module 规范不允许在 ES Module 文件中使用 `require` 和 `module.exports` 语法。即使你把 Rollup 配置好了，如果你自己的源代码中写了 `require` 或 `module.exports`，Rollup 也会报错。

**如果你的 Rollup 配置文件必须使用 CommonJS**（比如你写的是一个 Node.js CLI 工具，需要兼容老版本 Node.js），你有两个选择：

1. 把配置文件名改成 `rollup.config.cjs`——Rollup 会自动识别 `.cjs` 扩展名并以 CommonJS 模式解析
2. 保持 `rollup.config.js` 不变（ESM 格式），在 Node.js 14+ 环境下直接使用 `import`/`export` 语法

> ⚠️ **注意**：有一种说法是"把配置文件改成 `.mjs` 来强制 ES Module"。其实大可不必——`.mjs` 文件在 Node.js 中**始终**被当作 ES Module 解析，不管 `package.json` 中 `type` 字段是什么。更重要的是，Rollup 的配置文件**默认就是 ESM 格式**，根本不需要"强制"什么。

---

## 6.3 external（外部依赖）处理

### 6.3.1 哪些模块应该 external（lodash / react 等）

`external` 配置告诉 Rollup："这个依赖不要打包，我会单独提供，你只管生成引用代码就行"。

典型的 external 场景：

- **运行时依赖**：比如 `react`、`react-dom`。如果你把这些打包进你的库里，使用你的库的人如果已经安装了 `react`，就会有两份 `react`——一份你的，一份他们的，既浪费空间又可能引发版本冲突。
- **Node.js 内置模块**：`fs`、`path`、`crypto` 等，在 Node.js 环境中天然存在，不需要打包。
- **太大的库**：比如 `moment.js`（~67KB 压缩后 / ~300KB 未压缩），如果你的库只是用它的一个函数，可以 external 掉让用户自行安装。

```javascript
// rollup.config.js
export default {
  input: 'src/index.js',
  external: [
    'react',          // React 库不打包
    'react-dom',
    'lodash',         // lodash 不打包
    'fs',             // Node.js 内置模块
    'path'
  ]
};
```

### 6.3.2 external 的三种配置方式（数组 / 函数 / 正则）

`external` 支持三种写法，灵活应对各种场景：

```javascript
export default {
  external: [
    // 方式 1：数组（精确匹配包名）
    'react',
    'lodash/debounce',

    // 方式 2：正则（匹配所有以 react 开头的包）
    /^react/,

    // 方式 3：函数（最灵活，根据模块 ID 动态判断）
    (id, parentId) => {
      // id: 模块 ID（如 'lodash' 或 '/path/to/file.js'）
      // parentId: 导入它的模块 ID
      if (id.includes('node_modules')) {
        // 所有 node_modules 中的模块都 external
        return true;
      }
      return false;
    }
  ]
};
```

### 6.3.3 UMD / IIFE 格式的 external 必须配合 globals

当你要输出 UMD 或 IIFE 格式时，`external` 配置必须配合 `output.globals` 一起使用，因为这两种格式需要知道"这个模块在全局环境下叫什么名字"：

```javascript
export default {
  input: 'src/index.js',
  external: ['react'],
  output: {
    file: 'dist/index.umd.js',
    format: 'umd',
    name: 'MyLibrary',
    // 必须指定 globals，否则 UMD 打包会失败
    globals: {
      react: 'React'  // react 这个模块在全局环境下叫 React
    }
  }
};
```

生成的 UMD 代码中会这样引用 React：

```javascript
// 生成的 UMD 代码（简化版）
(function (root, factory) {
  if (typeof exports === 'object' && typeof module === 'object')
    // Node.js
    module.exports = factory(require('react'));
  else if (typeof define === 'function' && define.amd)
    // AMD
    define(['react'], factory);
  else
    // 浏览器全局变量
    root.MyLibrary = factory(root.React);
}(this, function (React) {
  // 这里是你的库代码
}));
```

### 6.3.4 external 与依赖重复打包的矛盾

如果你的库依赖了 `lodash`（设为 external），但你的用户没有安装 `lodash`，那用户拿到你的库后运行时会报错 `"lodash" is not defined`。

解决方案：在库的 `package.json` 中使用 `peerDependencies` 声明依赖，并确保你的打包产物不对这些依赖做任何处理——让用户自行安装。

```json
{
  "name": "my-library",
  "peerDependencies": {
    "react": ">=17.0.0"
  }
}
```

> 💡 **提示**：如果你把 `react` 打包进去了，而用户的项目里也有 `react`，运行时就会有两份 React 实例——状态不共享，React Hooks 可能出现奇怪的行为。

---

## 6.4 循环依赖（Circular Dependencies）

### 6.4.1 ES Module 循环依赖的处理机制

循环依赖就是两个模块互相引用对方，比如 A 导入 B，B 又导入 A。这在 ES Module 中是允许的，但处理方式和你想象的可能不一样。

ES Module 的循环依赖机制是：**每个模块在被完全初始化之前，就可以被其他模块引用**。引用到的部分可能是 `undefined`（如果是 `import { something } from`），也可能是部分初始化的对象。

### 6.4.2 常见表现：undefined

```javascript
// a.js
import { b } from './b.js';
export const a = '我是 A';
console.log('b 的值:', b);  // undefined！此时 b 的赋值还没执行

// b.js
import { a } from './a.js';
export const b = '我是 B';
console.log('a 的值:', a);  // '我是 A'！a 在 B 之前已经初始化完成
```

打包后，你可能会发现 `b` 的值是 `undefined`——因为在 `a.js` 执行时，`b.js` 还没来得及执行 `export const b = '我是 B'`。这就是循环依赖的典型症状。相比之下，`a` 反而是正常的，因为 A 比 B 先初始化（先有鸡还是先有蛋的问题）。

### 6.4.3 设计层面的避免方式

循环依赖大多数时候是代码结构设计问题的信号。以下是几种推荐的避免方式：

1. **重新组织模块结构**：把公共部分提取到一个独立的第三模块 C，让 A 和 B 都依赖 C
2. **使用依赖注入**：把被循环引用的部分通过函数参数传入
3. **延迟访问**：把对另一个模块的访问放到函数中，而不是模块顶层

```javascript
// 方式 1：重构（推荐）
// a.js
import { c } from './c.js';  // A 和 B 都依赖 C，不再循环
export const a = '我是 A';
export function useC() { return c; }

// 方式 2：函数包装（临时方案）
// a.js
import { getB } from './b.js';
export const a = '我是 A';
export function getBValue() { return getB(); }
```

---

## 6.5 output.format 选择逻辑

### 6.5.1 ES：库 / 框架开发者首选

ES 格式（ES Module）是当前前端生态最推荐的格式。它的特点是：
- 代码最干净
- Tree-Shaking 效果最好
- 被现代浏览器和其他打包工具原生支持

如果你在开发一个供其他开发者使用的 npm 包，ES 格式几乎是必选的。

### 6.5.2 CJS：Node.js 工具

CommonJS 格式是 Node.js 的传统标准。如果你开发的是一个 Node.js 命令行工具（如 `eslint`、`prettier`），CJS 格式是首选。

### 6.5.3 UMD：需要同时支持浏览器和 Node 的库

UMD 的主要价值在于"一份代码同时支持浏览器和 Node"。

UMD 真正有价值的场景是：**你的库需要直接被 `<script src="">` 标签引入（浏览器），同时也要支持 npm 安装（Node）**。比如某些提供给第三方使用的 UI 组件库，或者是需要在各种环境复用的工具函数。

> 💡 **现代方案**：如果你只需要支持现代浏览器，越来越多的库选择**同时输出 ES + CJS 两种格式**，而不是用 UMD。用户通过 `import` 或 `require` 自行选择，不需要 UMD 来做"自动检测"。

### 6.5.4 IIFE：浏览器 `<script>` 标签直接引用（无需模块系统）

IIFE 格式适合：
- 你的库需要直接给用户复制粘贴到 HTML 里用
- 快速原型验证
- 不需要构建工具的简单场景

```html
<!-- 用户只需要这一行就能用你的库 -->
<script src="my-lib.iife.js"></script>
<script>
  console.log(MyLibrary.add(1, 2));  // 3
</script>
```

---

## 6.6 路径解析的常见错误

### 6.6.1 node_modules 模块找不到（缺少 @rollup/plugin-node-resolve）

最常见的错误之一：

```
Error: Could not resolve 'lodash' from src/index.js
```

这是因为 Rollup 默认只解析相对路径（`./` 或 `../`），不解析 `node_modules`。解决方法是安装 `@rollup/plugin-node-resolve`：

```bash
npm install -D @rollup/plugin-node-resolve
```

```javascript
import resolve from '@rollup/plugin-node-resolve';

export default {
  plugins: [resolve()]
};
```

### 6.6.2 相对路径 / 绝对路径混淆

Rollup 对路径的处理比较严格，混用相对路径和绝对路径会导致解析失败：

```javascript
// 正确
import { add } from './utils/math.js';
import { clone } from 'lodash-es';           // lodash-es 支持命名导入（named export）
import clone from 'lodash-es/clone.js';     // 也可以直接导入单个函数文件（更精确的按需导入）

// 错误（缺少 ./）
import { add } from 'utils/math.js';
```

### 6.6.3 配置 resolve.alias 别名简化路径

当项目变深时，`../../../utils/format.js` 这种长路径会让人崩溃。通过别名配置可以简化：

```javascript
import resolve from '@rollup/plugin-node-resolve';
import alias from '@rollup/plugin-alias';

export default {
  plugins: [
    alias({
      entries: [
        { find: '@', replacement: 'src' },        // @ → src
        { find: '@utils', replacement: 'src/utils' },
        { find: '@components', replacement: 'src/components' }
      ]
    }),
    resolve()  // resolve 要放在 alias 之后——因为 alias 先把 @/xxx 这种路径转成真实路径，resolve 才能接着去找真实路径对应的文件
  ]
};
```

现在可以这样写导入语句了：

```javascript
// src/page/Home.js
import { formatDate } from '@/utils/format.js';         // ✓ 别名生效
import MyButton from '@/components/MyButton.vue';       // ✓ 别名生效
```

---

## 6.7 sideEffects 与 Tree-Shaking

### 6.7.1 package.json 的 sideEffects 字段（告诉 bundler 哪些文件无副作用）

`sideEffects` 字段是给 bundler（包括 Rollup、Webpack 等）的一个提示，告诉它们"哪些文件是有副作用的，哪些文件是没有副作用的"：

```json
{
  "name": "my-library",
  "sideEffects": false
}
```

`"sideEffects": false` 的意思是：**这个库的所有文件都没有副作用，可以放心地做 Tree-Shaking**。这样 bundler 在分析时，如果发现某个 import 的模块最终没有被使用，可以直接删除，不需要担心删除后影响全局状态。

你也可以指定更精确的模式：

```json
{
  "sideEffects": [
    "src/styles.css",
    "src/polyfill.js"
  ]
}
```

意思是只有 `styles.css` 和 `polyfill.js` 是有副作用的，其他文件都可以放心删除。

### 6.7.2 rollup.config.js 的 treeshake.moduleSideEffects（false / 'no-external' / 'all'）

在 Rollup 配置中，你可以更细粒度地控制 Tree-Shaking 的副作用行为：

```javascript
export default {
  treeshake: {
    // false（等同于 'no-external'）：最激进的 Tree-Shaking，假设所有模块都没有副作用
    moduleSideEffects: false,

    // 'no-external'：仅对非外部依赖的模块假设无副作用（默认行为）
    // moduleSideEffects: 'no-external',

    // 'all'：所有模块都可能产生副作用，Tree-Shaking 基本不删除任何模块
    // moduleSideEffects: 'all',

    // 也可以传入函数
    moduleSideEffects: (id) => {
      if (id.includes('node_modules')) return true;  // 第三方库可能有副作用
      return false;                                  // 自己的代码假设无副作用
    }
  }
};
```

### 6.7.3 误配置导致正确代码被意外删除

这是 `sideEffects` 配置的阴暗面。假设你配置了 `sideEffects: false`，然后你的代码里有一个函数没有被任何地方使用，但这个函数实际上有"隐形的副作用"——比如它会修改全局变量、或者调用了 `console.log`：

```javascript
// polyfill.js
export function polyfill() {
  // 扩展 Array.prototype，副作用是修改全局对象
  Array.prototype.customMap = function(fn) { /* ... */ };
}

// math.js
export function add(a, b) {
  return a + b;
}

// main.js
import { add } from './math.js';
import { polyfill } from './polyfill.js';  // 你可能只是不小心导入了，但没用
console.log(add(1, 2));
```

由于 `polyfill.js` 虽然被导入但没有实际调用（`polyfill()` 没被执行），在 `sideEffects: false` 的情况下，bundler 会认为这段代码可以安全删除——结果你的 `Array.prototype.customMap` 根本没被扩展，线上就原地报错了。

> ⚠️ **教训**：`sideEffects: false` 是把双刃剑。用之前确保你真的理解了自己的代码哪些有副作用，哪些没有。

---

## 6.8 打包产物的兼容性问题

### 6.8.1 浏览器不支持 ES Module（需要 IIFE / UMD fallback）

IE 11 以及一些老版本浏览器不支持 ES Module。如果你需要兼容这些浏览器，你需要同时输出两份产物，然后用 `type="module"` 和 `nomodule` 属性分别引入：

```html
<!-- 老浏览器（IE 11 等）：IIFE 格式，nomodule 属性让现代浏览器忽略它 -->
<script src="my-lib.legacy.js" nomodule></script>
<!-- 现代浏览器：ES Module 格式，module 属性让老浏览器忽略它 -->
<script type="module" src="my-lib.esm.js"></script>
```

> 💡 `nomodule` 属性是 HTML5 标准属性，老浏览器不认识会直接忽略它；现代浏览器看到 `nomodule` 属性则不执行该脚本。两边互不干扰，完美共存。

注意：需要为两种格式分别准备打包产物——IIFE 格式给老浏览器用，ES Module 格式给现代浏览器用。

### 6.8.2 generatedCode 选项（控制模块包装语法，如 es2015 / esnext）

`generatedCode` 选项控制 Rollup 生成模块系统包装代码时使用的语法风格——比如是否使用 `Object.defineProperty` 包装 `export`，是否添加 `__esModule` 标记等。

> ⚠️ **注意**：这里控制的是**模块包装层**的语法，不是代码转译！`const` → `var`、箭头函数 → 普通函数这类语法降级是 Babel 的工作，不是 `generatedCode` 的职责范围。

```javascript
export default {
  output: {
    // 'es2015'：兼容更多环境的输出（如 exports.__esModule 标记）
    generatedCode: 'es2015',

    // 'esnext'（默认）：生成更简洁的现代模块语法
    // generatedCode: 'esnext',

    // 'preserved'：尽量保留源代码的语法特性（实验性）
    // generatedCode: 'preserved'
  }
};
```

这个选项主要影响 Rollup 如何生成 `import`/`export` 相关的包装代码，以及是否添加 ES Module 兼容性标记。如果你需要兼容老版本浏览器，**仍然需要 Babel**——`generatedCode` 只是控制模块层面的包装方式。

### 6.8.3 Source Map 路径偏移

Source Map 的作用是"把压缩后的代码映射回源代码"，但如果配置不当，Source Map 的路径可能和实际文件对不上，导致浏览器找不到源代码。

常见原因：
- 打包时用了 `output.dir` 把产物输出到某目录，但 Source Map 里的 `sources` 路径是相对于 map 文件本身的——如果 `dir` 和源文件目录结构不匹配，浏览器无法正确定位源文件
- 部署后 CDN 或反向代理路径与本地不一致，导致浏览器找不到 map 文件

```javascript
// 确保生成正确的 Source Map
export default {
  output: {
    sourcemap: true,
    // 或者手动指定 Source Map 的格式
    // sourcemap: 'inline'  // 内联到 JS 文件里
  }
};
```

---

## 6.9 模块解析优先级

### 6.9.1 exports vs main vs module 字段的优先级

`package.json` 中有多个可以指定入口文件的字段，它们有优先级顺序：

```
exports > module > main
```

- **`main`**：最早引入的字段，Node.js 和 bundler 最基本的入口
- **`module`**：专门给 ES Module 用的入口，通常指向 ESM 格式的文件
- **`exports`**：最灵活，支持条件导出，可以根据 import/require 等不同场景指定不同文件

### 6.9.2 export conditions（import / require / default / types）

`exports` 字段支持条件导出，可以根据不同的使用场景提供不同的入口：

```json
{
  "exports": {
    ".": {
      "import": "dist/index.mjs",   // import 语法用这个
      "require": "dist/index.cjs", // require 语法用这个
      "types": "dist/index.d.ts"   // TypeScript 类型用这个
    }
  }
}
```

Rollup 对 `exports` 字段的完整支持，使得打包产物能更准确地被消费者解析。

### 6.9.3 条件导出在 Rollup 中的处理方式

当 Rollup 解析一个 npm 包时，它会遵循 `exports` 字段的条件选择最合适的入口文件。如果你希望 Rollup 优先使用 ES Module 格式的入口，你可以在 `@rollup/plugin-node-resolve` 中配置：

```javascript
import resolve from '@rollup/plugin-node-resolve';

export default {
  plugins: [
    resolve({
      exportConditions: ['module', 'node'],  // 优先匹配 module 条件
      extensions: ['.js', '.mjs', '.cjs']
    })
  ]
};
```

---

## 6.10 Babel vs 原生 ESM

### 6.10.1 是否需要 Babel：取决于目标浏览器范围

Babel 的作用是把新版本 JavaScript 语法转译成旧版本语法。比如把 `const` 转成 `var`，把箭头函数转成普通函数，把 ES Class 转成构造函数……

**你需要 Babel 的场景**：
- 你的代码要运行在老版本浏览器（如 IE 11）上
- 你的代码要运行在老版本 Node.js 上

**你不需要 Babel 的场景**：
- 你只需要支持现代浏览器（Chrome 80+、Firefox 75+、Safari 13+）
- 你的代码只需要在 Node.js 14+ 上运行

### 6.10.2 Babel 的模块转换会破坏 Tree-Shaking

> ⚠️ **重要澄清**：Babel 的**语法转译**（如 `class` → 构造函数）**不会**破坏 Tree-Shaking。真正的问题是 **Babel 的模块格式转换**——当你启用 `@babel/plugin-transform-modules-*` 系列插件时，Babel 会把 ES `export` 转成 CJS `exports`，bundler 看到的就是 CommonJS 模块，而 CommonJS 的动态特性让 Tree-Shaking 基本失效。

> 💡 **另外需要注意**：如果你使用了 `@babel/plugin-transform-decorators`，确保它是最新版本——旧版本会把装饰器转译得非常复杂，产生大量隐藏函数引用，干扰 Tree-Shaking 的分析。

```javascript
// 源代码
class Calculator {
  add(a, b) { return a + b; }
}

export const calc = new Calculator();
```

如果 Babel 启用了模块转换插件（如 `@babel/plugin-transform-modules-commonjs`），会转译成：

```javascript
"use strict";

function _classCallCheck(instance, Constructor) { ... }

var Calculator = function () { ... }();

exports.calc = new Calculator();
```

问题是：**Babel 把 ES `export` 转成了 CJS `exports`，bundler 看到的就是 CommonJS 模块**——而 CommonJS 模块的动态特性（`require` 可以在条件分支里调用）让 Tree-Shaking 变得非常困难。

**结论**：如果你用 Babel + Rollup，**不要**让 Babel 处理模块转换。保持 Babel 只做语法转译，让 Rollup 自己处理 ES Module。

正确配置 Babel（`@babel/preset-env`）的姿势：

```javascript
// rollup.config.js（带 Babel 版本）
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';
import babel from '@rollup/plugin-babel';

export default {
  input: 'src/main.js',
  plugins: [
    resolve(),
    commonjs(),
    babel({
      babelHelpers: 'bundled',    // Babel 辅助函数直接打包进去
      presets: [
        ['@babel/preset-env', {
          targets: { chrome: '80' },  // 目标浏览器
          modules: false              // ★ 关键！禁止 Babel 转换模块格式
        }]
      ]
    }),
    terser()
  ]
};
```

### 6.10.3 现代浏览器环境下直接使用 Rollup 原生能力更优

如果你的项目只需要支持现代浏览器（这是现在大多数 Web 项目的现实情况），建议**尽量不使用 Babel**，直接用 Rollup 原生的 ES Module 处理能力。

```javascript
// rollup.config.js（无 Babel 版本）
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';

export default {
  input: 'src/main.js',
  plugins: [
    resolve(),
    commonjs(),
    terser()
  ]
};
```

这个配置比带 Babel 的配置简单得多，而且 Tree-Shaking 效果更好、打包速度更快。

---

## 6.11 Watch 模式的坑

### 6.11.1 初次构建慢，watch 增量构建也有瓶颈

Rollup 的 watch 模式在首次启动时仍然需要做完整构建（没有魔法能跳过这步），之后文件变化才会触发增量构建。对于大型项目（数百个模块），即使是增量构建也可能需要数秒——别指望改一行 CSS 就瞬间编译完成。

**优化建议**：使用 `output.compact: true` 可以压缩输出代码（对 bundle 内容做简化和混淆），减少写入文件的大小和写入时间；在 Node.js 环境中也可以开启 `fs.realpathCache` 减少重复的路径解析开销。

### 6.11.2 配置文件修改不会自动触发 reload

当你修改 `rollup.config.js` 时，watch 模式**不会自动重新加载配置**。你需要手动停止（`Ctrl+C`）再重新启动。

```bash
# 修改了 rollup.config.js 后
# 需要手动重启 watch
^C
npx rollup --config --watch
```

### 6.11.3 大项目 watch 内存占用高

长时间运行的 watch 进程会不断累积内存（因为 Rollup 会缓存每个版本的模块信息）。如果项目很大，长时间 watch 后可能会遇到内存溢出的问题。

**应对策略**：定期重启 watch 进程（比如配合 `nodemon` 监控配置文件变化并重启 Rollup）；或者将大型项目拆分，用 `rollup.watch()` API 在自定义脚本中控制缓存清理。

### 6.11.4 stdin 输入在 watch 模式下行为特殊

如果你通过管道向 Rollup 传入代码（如 `echo 'export const x = 1' | rollup --stdin`），watch 模式的 `--watch` 参数会**失效**——Rollup 无法监控 stdin 内容的文件变化。这种场景下建议直接使用文件输入。

---

## 6.12 多格式同时输出的常见问题

### 6.12.1 chunk 命名一致性（preserveModules 控制原始结构）

当同时输出多种格式时，Rollup 会尽量保证 chunk 命名的一致性。但某些情况下（比如使用了 `manualChunks`），不同格式之间的 chunk 命名可能不一致，给缓存策略带来困难。

如果你希望保持原始模块结构（方便调试和缓存），可以使用 `output.preserveModules: true`——Rollup 会保持每个源文件一个 chunk，文件名和原始路径对应：

```javascript
export default {
  output: {
    preserveModules: true,        // 保持原始模块结构
    preserveModulesRoot: 'src',   // chunk 路径相对于 src 目录
    chunkFileNames: '[name].js'
  }
};
```

> ⚠️ **注意**：`preserveModules: true` 会导致生成的 chunk 数量大幅增加（每个源文件一个），**不适合生产环境直接使用**（HTTP/2 下小文件多反而慢），更适合用于生成供其他打包工具消费的 ESM 产物。

### 6.12.2 external 模块在多格式间的一致性处理

同一个依赖在 ES 格式和 CJS 格式中都应该被 external 掉，而且引用方式要正确对应——这是多格式输出时最常见的坑。

一个常见的错误是：你在 `external` 数组中写了 `'lodash'`，但忘了在 `globals` 中声明它（UMD 格式需要），然后打包时报错一脸懵。或者 ES 格式下用了 `import { debounce } from 'lodash'`（命名导入），而 CJS 格式下用了 `const _ = require('lodash')`（默认导入）——运行时发现 debounce 是 `undefined`，然后开始漫长的 debug 之旅。**结论：多格式输出时，external 和 globals 要成双成对出现。**

### 6.12.3 UMD/IIFE 格式下 globals 与 external 的配合

UMD 和 IIFE 格式的 external 必须配合 `output.globals` 一起用，否则 Rollup 会报配置错误：

```
Error: You must supply options.output.globals for external UMD imports
```

这个错误的意思是：你在 UMD 输出中 external 了一些模块，但你没有告诉 Rollup 这些模块在全局环境下叫什么名字。

### 6.12.4 `inlineDynamicImports` 对多格式的影响

`output.inlineDynamicImports` 是一个容易被忽略的选项，但对多格式输出有重要影响：

- 设为 `true` 时，所有动态 `import()` 会被内联为同步的 `require()` 调用，所有代码打包进单个文件——**不兼容 ES 格式**（ES Module 原生就不支持 `require`，Rollup 会直接报错）
- 设为 `false`（默认）时，每个 `import()` 生成独立 chunk——ES/CJS/UMD/IIFE 全都兼容

> ⚠️ **实战教训**：如果你配了多格式输出（ES + CJS + IIFE），千万别手滑把 `inlineDynamicImports: true` 加上——ES 格式的产物会原地爆炸，找错都要找半天。

```javascript
export default {
  input: 'src/index.js',
  output: [
    { file: 'dist/index.mjs', format: 'es' },        // ES Module
    { file: 'dist/index.cjs', format: 'cjs' },        // CommonJS
    { file: 'dist/index.iife.js', format: 'iife', name: 'MyLib' }  // IIFE
  ]
  // Rollup 原生支持 output 数组输出多种格式，不需要任何额外插件！
  // inlineDynamicImports 默认为 false，多格式场景下保持默认即可
};
```

---

## 6.13 动态导入与代码分割

### 6.13.1 使用 `import()` 实现按需加载

Rollup 支持动态 `import()` 语法，可以实现按需加载和代码分割：

```javascript
// 源代码
async function loadUtility() {
  const { formatDate } = await import('./utils/date.js');
  return formatDate(new Date());
}
```

Rollup 会把 `date.js` 分割成独立的 chunk，只在需要时才加载：

```javascript
// 打包后的代码（简化版）
async function loadUtility() {
  return import(/* ./utils/date.js */ './chunk-A.js')
    .then(m => m.formatDate(new Date()));
}
```

### 6.13.2 动态导入的坑：external 处理不一致

动态 `import()` 的 external 处理和静态 `import` 有时会不一致。某些插件可能只处理了静态 import 的情况，导致动态 import 的模块被错误打包或解析失败。

如果遇到奇怪的问题，先检查你的 `@rollup/plugin-node-resolve` 是否配置正确，以及是否正确处理了 `node_modules` 中的模块。

**常见陷阱**：如果你在 `manualChunks` 中指定了某个模块为第三方库（放入 vendor chunk），同时又在代码里用动态 `import()` 加载它，`manualChunks` 可能不会生效——动态导入的模块会被放到自己的 chunk 里，导致你的缓存策略失效。

### 6.13.3 静态分析限制：条件执行的代码无法被 Tree-Shaking

如果 `import()` 在条件分支中，Rollup 无法静态分析你到底会加载哪个模块：

```javascript
// Rollup 不知道这个条件为 true 时会加载什么
if (Math.random() > 0.5) {
  const mod = await import('./heavy-module.js');
}
```

这种情况下，Rollup 无法静态分析会加载哪个模块，会**保守地将 `heavy-module.js` 作为独立 chunk 打包**——它不会帮你"智能删除"这段永远不知道会不会执行的代码。

> 💡 **提示**：这里的"打包"不是指打包进主 bundle，而是指 Rollup 会为它生成一个独立的 chunk 文件（代码分割），并在运行时根据条件动态加载。所以结论是：如果你的条件分支里搞了一个巨无霸模块，要么重构掉这个 `if`，要么就老老实实接受它会被打包的事实。
>
> **另外要注意**：条件分支中的动态 `import()` 虽然会被抽成独立 chunk，但静态 `import` 的模块仍然会照常打包进主 bundle。也就是说——如果你在顶层静态 import 了 `heavy-utils`，它早就已经在主 bundle 里了，和条件分支无关。

---

## 6.14 CSS 打包相关

### 6.14.1 CSS 文件需要专门的插件处理

Rollup 本身**只能处理 JavaScript**。如果你的代码中 `import` 了 CSS 文件（如 `import './style.css'`），Rollup 默认会报错。

解决方案是使用 `@rollup/plugin-postcss`：

```bash
npm install -D @rollup/plugin-postcss
```

```javascript
// rollup.config.js
import postcss from '@rollup/plugin-postcss';

export default {
  plugins: [
    postcss({
      // 把 CSS 抽离成单独文件
      extract: 'bundle.css',
      // 或者内联到 JS 中（适合 IIFE）
      // inject: true
    })
  ]
};
```

### 6.14.2 CSS 抽离后的路径问题

如果你用的是 `extract` 选项把 CSS 抽成单独文件，HTML 中需要手动引入这个 CSS 文件。另外，如果 CSS 中有 `url()` 引用图片等资源，路径是相对于 CSS 文件本身的——如果 CSS 被抽离到不同目录，路径可能会断裂。

解决方法是配置 `postcss` 的 `extract` 选项时指定输出路径，或者配合 `publicPath` 确保资源路径正确。

### 6.14.3 `output.assetFileNames` 控制静态资源命名

Rollup 输出的非 JS 文件（如 CSS、图片、字体等）可以通过 `output.assetFileNames` 来自定义命名规则：

```javascript
export default {
  output: {
    assetFileNames: 'assets/[name]-[hash][extname]'
  }
};
```

---

## 本章小结

这一章我们系统地梳理了 Rollup 使用过程中的各种坑和注意事项：

1. **Tree-Shaking 前提**：必须是 ES Module 语法，CJS 需要插件转换，混用会降低效果。

2. **CommonJS 坑**：不装 `@rollup/plugin-commonjs` 直接报错，`__esModule` 标记有副作用，named/default export 混用要小心。

3. **external 处理**：运行时依赖要 external，配合 UMD/IIFE 必须同时配置 globals。

4. **循环依赖**：表现为 undefined，设计层面尽量避免，用依赖注入或重构化解。

5. **format 选择**：ES 最优（库），CJS（Node.js），IIFE（直接 script 标签），UMD（需要同时支持浏览器和 Node）。

6. **路径解析**：必须装 `@rollup/plugin-node-resolve`，别名插件简化长路径。

7. **sideEffects 配置**：`false` 最激进，但可能误删有副作用的代码——特别是那些"被导入但未调用"的 polyfill 代码。

8. **兼容性问题**：老浏览器需要 IIFE/UMD fallback，`generatedCode` 只控制模块包装方式，不做语法转译。

9. **模块解析优先级**：`exports` > `module` > `main`，`exportConditions` 决定选哪个入口。

10. **Babel vs 原生 ESM**：Babel 的模块转换会破坏 Tree-Shaking，记得设置 `modules: false` 让 Rollup 处理模块。

11. **Watch 模式坑**：初次构建慢，配置文件修改不自动重载，大项目内存占用高，stdin watch 不生效。

12. **多格式输出坑**：`preserveModules` 保持原始结构但 chunk 过多，`inlineDynamicImports` 不兼容 ES 格式，external/globals 必须全套配置。

13. **动态导入**：`import()` 支持按需加载，但条件分支中的动态 import 无法被 Tree-Shaking。

14. **CSS 打包**：Rollup 不处理 CSS，需要 `@rollup/plugin-postcss` 配合，路径问题要注意。