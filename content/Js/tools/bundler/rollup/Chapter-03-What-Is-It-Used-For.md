+++
title = "第3章 有什么用"
weight = 30
date = "2026-03-28T11:38:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 3 章　有什么用

## 3.1 打包 JavaScript 库 / npm 包

这是 Rollup 最核心的使用场景，也是它的拿手好戏。如果你写了一个工具函数库、一个 UI 组件库，或者任何一个你想发布到 npm 上让其他开发者使用的项目，Rollup 几乎是你能找到的最佳打包方案。为什么这么说？

## 3.1.1 输出多格式（同时兼容 ESM / CJS / UMD 消费者）

想象一下：你的 npm 包只支持 CommonJS 格式，但一个使用 ES Module 的开发者试图 `import` 它，结果报错了——那场面有多尴尬。而用 Rollup 打包，你可以**一次性输出多种格式**：



```javascript
// rollup.config.js
export default [

  // 格式一：ES Module（给现代浏览器和 ESM bundler 用）
  {
    input: 'src/index.js',
    output: {
      file: 'dist/index.esm.js',
      format: 'es'
    }
  },
  // 格式二：CommonJS（给 Node.js 用）
  {
    input: 'src/index.js',
    output: {
      file: 'dist/index.cjs.js',
      format: 'cjs'
    }
  },
  // 格式三：UMD（同时支持浏览器和 Node）
  {
    input: 'src/index.js',
    output: {
      file: 'dist/index.umd.js',
      format: 'umd',
      name: 'MyLibrary'  // UMD 必须指定全局变量名
    }
  }
];
```



一份源码，三种格式（ES / CJS / UMD），其他开发者在他们的 `package.json` 中指定使用哪种格式就可以了。

## 3.1.2 Tree-Shaking 移除未使用代码，产物体积最小化

假设你的库里有很多工具函数，但用户只需要用其中一个 `debounce`，传统打包方案会把整个库打包进去；但 Rollup 的 Tree-Shaking 会只把 `debounce` 相关的代码提取出来，用户最终下载的代码量就是他们真正用到的那部分。这就是为什么 Vue 3、lodash-es 等知名项目都选择 Rollup 作为打包工具——它们对产物体积有着极致的追求。

## 3.1.3 配置 package.json 的 exports 字段

当你用 Rollup 输出了多格式之后，还需要在 `package.json` 里正确配置 `exports` 字段，告诉 npm 包的消费者"在什么情况下用哪个文件"：

```json
{
  "name": "my-awesome-library",
  "main": "dist/index.cjs.js",
  "module": "dist/index.esm.js",
  "exports": {
    ".": {
      "types": "dist/index.d.ts",
      "import": "dist/index.esm.js",
      "require": "dist/index.cjs.js"
    }
  }
}
```

这个配置的意思是：如果你用 `import` 语法，就用 ESM 文件；如果你用 `require`，就用 CJS 文件；如果你用 TypeScript，还能自动拿到类型定义。Rollup 帮你打包，配置告诉你怎么用，分工明确。

> 💡 敲黑板：`types` 字段必须放在 `exports` 条件的第一位！这是 npm 的规定——首个条件会被作为默认值。放错顺序可能导致 TypeScript "找不到类型定义"的报错，让人百思不得其解。

> 💡 补充：如果你的库使用 TypeScript 编写，`@rollup/plugin-typescript` 的 `declaration: true` 选项已经能生成 `.d.ts` 文件，无需额外插件。但如果想把类型定义单独打包（JS 和类型分开发布），才需要 `rollup-plugin-dts` 来做"二次加工"。

## 3.1.4 TypeScript 编译（生成 .d.ts 类型定义）

如果你用 TypeScript 编写库，Rollup 配合 `@rollup/plugin-typescript` 可以直接编译 TS 代码并输出 JavaScript：

```javascript
// rollup.config.js
import typescript from '@rollup/plugin-typescript';

export default {
  input: 'src/index.ts',
  output: {
    dir: 'dist',
    format: 'es'
  },
  plugins: [
    typescript({
      // 指向 tsconfig.json
      tsconfig: './tsconfig.json',
      // 输出 .d.ts 文件（由 TypeScript 编译器生成）
      declaration: true,
      declarationDir: 'dist'
    })
  ]
};
```

> ⚠️ 注意：`@rollup/plugin-typescript` 只会把 `.ts` 编译成 `.js` 并输出类型声明文件，**不会**额外做 Babel 的 JSX / TSX 转译。如果你写的是 React 组件库，还是需要 Babel 来处理 JSX——两者各司其职，并不冲突。

---

## 3.2 构建 UI 组件库

如果你要开发一个 React 组件库、Vue 组件库或者 Svelte 组件库，Rollup 同样是你最好的选择。

## 3.2.1 React 组件库打包（JSX 处理）

React 组件用的是 JSX 语法，这需要 Babel 或者 SWC 来转译。Rollup 配合 `@rollup/plugin-babel` 就可以处理 JSX：

```javascript
// rollup.config.js
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import babel from '@rollup/plugin-babel';
import terser from '@rollup/plugin-terser';

const production = process.env.NODE_ENV === 'production';

export default {
  input: 'src/index.js',
  output: {
    dir: 'dist',
    format: 'es',
    sourcemap: !production  // 生产环境关闭 sourcemap 减小体积
  },
  plugins: [
    resolve(),          // 解析 node_modules
    commonjs(),         // 处理 CJS 依赖
    babel({
      // babel 用于处理 JSX 的配置
      babelHelpers: 'bundled',  // 把 Babel helper 函数也打包进去
      extensions: ['.js', '.jsx'],
      exclude: 'node_modules/**',
      presets: [
        ['@babel/preset-react', { runtime: 'automatic' }]  // JSX 必须有 preset 才能转译！
      ]
    }),
    production && terser()  // 生产环境才压缩
  ].filter(Boolean)  // 过滤掉 falsy 值
};
```

## 3.2.2 Vue 组件库打包（Vue SFC 处理）

Vue 的单文件组件（`.vue` 后缀）需要专门的插件来处理。`rollup-plugin-vue` 由 vuejs-community 维护，支持 Vue 2 和 Vue 3（通过不同版本）：

- **Vue 3** 用 `rollup-plugin-vue@6`（最新版本，同时支持 Vue 3 的 SFC 格式）
- **Vue 2** 则用 `rollup-plugin-vue@5`（Vue 2 项目使用）

> ⚠️ 注意：rollup-plugin-vue 已于 2023 年年年底被官方归档（deprecated），不再维护。Vue 2 项目建议用 Vite 配合 vite-plugin-vue2，Vue 3 项目建议直接用 Vite + vite-plugin-vue，生态更活跃，打包速度也更快。当然，如果你还在维护老的 Vue 2 项目，老版本 rollup-plugin-vue@5 依然能跑，只是别指望再收到更新了——就像一台老打印机，能用但不保证哪天突然罢工。

```javascript
// rollup.config.js
import vue from 'rollup-plugin-vue';  // Rollup 打包 Vue SFC 的正确插件
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import css from 'rollup-plugin-css-only';  // 只提取 CSS，不打包进 JS

export default {
  input: 'src/index.js',
  output: {
    dir: 'dist',
    format: 'es'
  },
  plugins: [
    vue(),        // 编译 .vue 文件，提取出 <script> 和 <template>
    css(),        // 把 <style> 提取成独立的 .css 文件
    resolve(),
    commonjs()
  ]
};
```

## 3.2.3 Svelte 组件打包

Svelte 组件的后缀是 `.svelte`，打包方式和其他框架略有不同：

```javascript
// rollup.config.js
import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';

export default {
  input: 'src/index.js',  // 入口文件汇聚所有组件；如果只打包单个组件，可以直接写 'src/MyComponent.svelte'
  output: {
    file: 'dist/MyComponent.js',
    format: 'es',
    name: 'MyComponent'
  },
  plugins: [
    svelte(),
    // rollup-plugin-svelte 负责调用 Svelte 编译器处理 .svelte 文件
    resolve(),
    commonjs()
  ]
};
```

有趣的是，Svelte 官方后来选择 Rollup 作为其编译产物的打包工具（取代了早期的其他方案），两者可以说是相互成就——Svelte 的大量使用推动了 Rollup 早期插件生态的繁荣，Rollup 的出色打包能力也让 Svelte 的发布体验非常顺畅。

## 3.2.4 CSS 提取（组件样式独立打包）

组件库通常需要把 CSS 单独打包出来，而不是打包进 JavaScript 文件中。这样用户可以单独引入 CSS 文件，便于样式管理：

```javascript
// rollup.config.js
import css from 'rollup-plugin-css-only';  // 提取 CSS 到独立文件

export default {
  input: 'src/index.js',
  output: {
    dir: 'dist',
    format: 'es'
  },
  plugins: [
    // ... 其他插件
    css()  // 提取后的 CSS 文件会输出到 output.dir 指定目录下，默认为 'style.css'
  ]
};
```

> 💡 小贴士：`rollup-plugin-css-only` 会把所有组件的 `<style>` 标签提取合并成一个 CSS 文件。如果你想自定义输出文件名，可以结合 `@rollup/plugin-replace` 或者直接用输出文件名配置来实现。

## 3.3 Tree-Shaking（消除死代码）

Tree-Shaking 我们在第 1 章已经详细介绍过，这里再补充一些实用角度的内容。

## 3.3.1 原理：ES Module 静态结构 → 编译器安全删除未使用导出

Tree-Shaking 的工作原理可以拆解成两步：**标记（Mark）**和**清除（Sweep）**。

第一步"标记"：Rollup 从入口文件开始，沿着 import 链条遍历所有模块，把所有实际被用到的变量、函数、类都标记为"活的"（live）。

第二步"清除"：把没有被标记的导出（export）全部从打包产物中删除。

这就好比一个图书馆管理员整理书架：先在一本书的所有页面上盖章（标记），然后把没有盖章的书（死代码）全部下架。

## 3.3.2 效果：显著减少最终产物体积

举一个真实的数字：假设你使用了 lodash-es（lodash 的 ES Module 版本）的 100 个函数中的 5 个，完整引入 lodash-es 的体积是 ~70KB（minified），但通过 Tree-Shaking + 按需引入，最终打包体积可能只有 ~3KB。差了 20 多倍，这可不是闹着玩的。

> 🔔 敲黑板：必须是 **lodash-es** 才能 Tree-Shaking，原始的 `lodash` 包是 CommonJS 格式，Rollup 对它只能"望码兴叹"——根本没法分析 `require` 里的依赖。所以，用 lodash 之前记得加 `-es`，这是前端圈的"政治正确"。

> 反过来说，如果你要发自己的库，又想让它具备良好的 Tree-Shaking 能力，就不要用 CJS 格式闷头干——输出 ES Module 格式，让下游开发者享受"只吃一口"的快乐。

## 3.3.3 sideEffects 选项精确控制

`sideEffects` 选项是 Tree-Shaking 的精细化控制开关。

> **副作用（side effect）是什么？**
> 简单理解，副作用就是"这个代码除了返回值，还干了别的事"。比如修改全局变量、发起网络请求、往 console 打印东西……这些都是副作用。如果一个模块有副作用，Rollup 就不能随便删除它——因为你可能需要那些副作用。

你可以在 `package.json` 中声明哪些文件没有副作用：

```json
{
  "name": "my-library",
  "sideEffects": false  // 告诉所有 bundler：我的库没有任何文件有副作用，
                         // 放心大胆地做 Tree-Shaking 吧！
}
```

或者在 `rollup.config.js` 中精确控制：

```javascript
export default {
  input: 'src/index.js',
  output: { file: 'dist/index.js', format: 'es' },
  treeshake: {
    moduleSideEffects: false  // 假设所有模块都没有副作用
    // 或者传入一个函数：(id) => id.includes('node_modules')
  }
};
```

---

## 3.4 代码分割（Code Splitting）

代码分割是现代前端性能优化的重要手段，Rollup 对它的支持也相当成熟。

## 3.4.1 动态导入（dynamic import）按需分割

使用 `import()` 语法加载模块时，Rollup 会自动将这个模块放到一个独立的 chunk 中：

```javascript
// main.js
import { showHome } from './home.js';

showHome();

// 只有用户访问购物车页面时才加载这个文件
document.getElementById('cartBtn').addEventListener('click', async () => {
  const { showCart } = await import('./cart.js');
  // 独立 chunk
  showCart();
});
```

执行打包后，你会得到两个文件：`main.js` 和 `cart-[hash].js`（hash 是 Rollup 根据内容生成的唯一标识）。用户首次访问只加载 `main.js`，点击购物车按钮后才加载 `cart-[hash].js`。

## 3.4.2 manualChunks 手动分割策略

有时候自动分割不是你想要的结果，你可以用 `manualChunks` 手动指定分割策略。它有两种形式：

**对象形式**——适合把几个已知模块打包到一起：

```javascript
// rollup.config.js
export default {
  input: 'src/main.js',
  output: {
    dir: 'dist',
    format: 'es',
    manualChunks: {
      // 把 react 和 react-dom 打包到一起，叫 vendor chunk
      'vendor': ['react', 'react-dom']
    }
  }
};
```

**函数形式**——适合按路径规则自动分割大量模块：

```javascript
// rollup.config.js
export default {
  input: 'src/main.js',
  output: {
    dir: 'dist',
    format: 'es',
    manualChunks(id) {
      if (id.includes('node_modules')) return 'vendor';
      if (id.includes('src/utils')) return 'utils';
      if (id.includes('src/components')) return 'components';
    }
  }
};
```

> 💡 小技巧：函数形式非常适合大型项目，比如把 `node_modules` 全部打成 `vendor` chunk，把各个业务模块按目录各打一个 chunk，浏览器可以缓存久一些，更新代码时只影响业务 chunk，不影响 vendor。

> ⚠️ 注意：`manualChunks` 对象形式中，值是**模块 ID 数组**（通常就是 npm 包名，如 `'react'`），而不是文件路径。比如 `'utils': ['lodash']` 只会把 `lodash` 单独打包，传入 `'src/utils/index.js'` 反而不会命中 `node_modules` 里的实际模块。如果你想按目录分割，请用函数形式。

## 3.4.3 实现路由级懒加载（前端应用的核心场景）

路由懒加载是代码分割最典型的应用场景。以 React Router 为例：

```javascript
// App.jsx
import { Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';

// 路由组件用 lazy 包裹，实现懒加载
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Product = lazy(() => import('./pages/Product'));

function App() {
  return (
    <Suspense fallback={<div>加载中...</div>}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/product" element={<Product />} />
      </Routes>
    </Suspense>
  );
}
```

打包后，每个页面组件都会生成独立的 chunk，用户访问哪个路由才加载对应的文件，首屏加载时间大幅缩短。

## 3.5 多格式输出（进阶指南）

Rollup 的多格式输出是它区别于很多打包工具的核心竞争力。3.1.1 节我们已经讲过基础配置，这里再深入一些细节。

> 🎯 小知识：Rollup 为什么能输出这么多格式？因为它的核心设计就是"输出格式无关"——只要你告诉它用什么格式，它就能生成对应的产物。这可比有些打包工具"要么 CJS 要么自闭"强多了。

## 3.5.1 ES：现代浏览器 / 其他 bundler 消费者

ES 格式是 Rollup 的"原生格式"——Rollup 本身就是用 ES Module 写的，输出 ES 格式就好比"回家"，简直不要太自然。输出的文件使用 `import` 和 `export` 语法：

```javascript
// 输出的 ES 格式文件
export function add(a, b) { return a + b; }
export function multiply(a, b) { return a * b; }
```

这是目前前端生态最推荐的格式——它能被现代浏览器直接加载，也能被 Vite、Webpack 等工具进一步处理，最重要的是它完整支持 Tree-Shaking。没有 Tree-Shaking 的打包，就像点外卖只收到筷子——你啥也没吃到。

## 3.5.2 CJS：Node.js 环境

CommonJS 格式使用 `require()` 和 `module.exports` 语法，是 Node.js 的标准格式：

```javascript
// 输出的 CJS 格式文件
'use strict';

function add(a, b) { return a + b; }
function multiply(a, b) { return a * b; }

module.exports = { add, multiply };
```

如果你要发布一个 Node.js 工具包，CJS 格式是必须的。毕竟 Node.js 江湖地位摆在那，虽然 ESM 是大势所趋，但 CJS 还是那个"瘦死的骆驼比马大"的存在。

## 3.5.3 UMD：同时兼容浏览器和 Node

UMD（Universal Module Definition）是一种"万能格式"，它会先检测当前环境——如果是 Node.js 就用 `module.exports`，如果是浏览器就挂到全局变量上：

```javascript
// 输出的 UMD 格式文件（简化版）
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(factory) :
  (factory((global.MyLibrary = {})));
}(this, (function () {
  'use strict';
  // 这里是你的模块代码
  function add(a, b) { return a + b; }
  return { add };
})));
```

> ⚠️ 注意：UMD 的 `name` 字段（这里示例中是 `MyLibrary`）必须和你在 `rollup.config.js` 中配置的全局变量名一致，否则浏览器环境下会找不到你的库。

## 3.5.4 IIFE：浏览器 `<script>` 标签直接引用

IIFE（Immediately Invoked Function Expression）格式就像一个自我执行的函数，非常适合直接用 `<script>` 标签引入。配置方式和 ES/CJS 基本一样，只需要把 `format` 改成 `iife`：

```javascript
// rollup.config.js
export default {
  input: 'src/index.js',
  output: {
    file: 'dist/my-library.iife.js',
    format: 'iife',
    name: 'MyLibrary'  // 全局变量名，方便 <script> 标签直接引用
  }
};
```

然后在 HTML 里直接引用：

```html
<!-- 用户只需要在 HTML 里加一行 -->
<script src="my-library.iife.js"></script>
<script>
  // 库代码已经执行，MyLibrary 已经挂在全局变量上了
  console.log(MyLibrary.add(1, 2));  // 3
</script>
```

> 💡 一个小细节：IIFE 格式的产物会用一个匿名函数把整个库包起来然后立即执行，所以不需要 `name` 的情况下也可以工作（但有 `name` 的话就能在全局找到它）。和 UMD 的区别是，IIFE 只面向浏览器，不考虑 Node.js 环境，产物比 UMD 更简洁。

## 3.6 构建前端工具链

前端工具链的开发者是 Rollup 的另一个重要用户群体。

## 3.6.1 Babel 插件源码打包

Babel 插件本身就是 JavaScript 代码，用 Rollup 打包再合适不过。Babel 官方团队就使用 Rollup 来打包自己的插件：

```javascript
// rollup.config.js
export default {
  input: 'src/index.js',
  output: {
    file: 'lib/index.js',
    format: 'cjs',
    sourcemap: true
  },
  external: ['babel-core', '@babel/types']  // 依赖 Babel 核心库，不打包
};
```

## 3.6.2 Webpack Loader / Plugin 源码打包

Webpack 的 Loader 和 Plugin 本质上也是 JavaScript 模块，Rollup 可以把它们打包成干净、可分发的格式：

```javascript
// rollup.config.js
export default {
  input: 'src/my-webpack-plugin.js',
  output: {
    file: 'dist/my-webpack-plugin.js',
    format: 'cjs',
    // 这些是 Webpack 提供的运行时变量，不应该被打包
    external: ['webpack', 'schema-utils']
  }
};
```

## 3.6.3 Vite 插件源码打包

Vite 插件的写法本质上就是一个带有特定返回值的函数，Rollup 完全能胜任：

```javascript
// rollup.config.js
export default {
  input: 'src/vite-plugin-example.js',
  output: {
    file: 'dist/vite-plugin-example.js',
    format: 'es'  // Vite 插件推荐用 ES 格式
  }
};
```

## 3.6.4 CLI 工具打包（pkg / ncc 配合使用）

如果你用 Node.js 写了一个命令行工具，想把它打包成单个可执行文件发给用户，典型做法是：先用 Rollup 把源码打包成干净的 bundle（ESM 或 CJS），再用 `pkg` 把 bundle 转成真正的原生可执行文件。Rollup 负责"优化代码"，`pkg` 负责"打包成 exe"——各司其职：

```javascript
// rollup.config.js
export default {
  input: 'bin/cli.js',
  output: {
    file: 'dist/cli.js',
    format: 'cjs',
    banner: '#!/usr/bin/env node'  // Unix 系统执行入口标记
  }
};
```

> 💡 补充：如果只需要打包成单个 JS 文件（而不是原生可执行文件），可以用 `@vercel/ncc`。ncc 会把 Node.js 代码及其依赖全部打包进一个 JS 文件，非常适合发布到 npm 的 CLI 工具——用户安装后，ncc 打包的文件已经包含了所有依赖，无需用户手动安装。

## 3.6.5 banner 和 footer：给产物加点"签名"

`banner` 和 `footer` 可以在打包产物的头部或尾部插入自定义内容，常见的用途是添加许可证注释、版本信息、构建时间等：

```javascript
// rollup.config.js
export default {
  input: 'bin/cli.js',
  output: {
    file: 'dist/cli.js',
    format: 'cjs',
    banner: '#!/usr/bin/env node',
    footer: `// Built at: ${new Date().toISOString()}`
  }
};
```

> 💡 小技巧：`banner` 和 `footer` 都支持模板字符串，可以动态插入变量。如果你不希望某个模块被 `external`，又想在产物里标注它来自哪里，可以配合 `intro`（在每个 chunk 开头插入内容）使用。

## 3.7 处理静态资源

Rollup 本身只处理 JavaScript 模块，但通过插件可以优雅地处理各种静态资源。

## 3.7.1 图片、字体、SVG 等资源的引用与复制

使用 `@rollup/plugin-url` 可以把图片、字体等资源要么转为 Data URL（内嵌进 CSS/JS），要么复制到输出目录：

```javascript
// rollup.config.js
import url from '@rollup/plugin-url';

export default {
  plugins: [
    url({
      // 小于 4KB 的图片内嵌为 Data URL，大于 4KB 的复制到 dist/assets/
      limit: 4 * 1024,
      destDir: 'dist/assets',
      fileName: '[name]-[hash][ext]'
    })
  ]
};
```

## 3.7.2 JSON 直接导入

`@rollup/plugin-json` 让你可以直接在 JavaScript 中 `import` JSON 文件：

```javascript
import pkg from './package.json';

console.log(pkg.name);    // 直接用，不需要 JSON.parse()
console.log(pkg.version); // '1.0.0'
```

Rollup 会在打包时把 JSON 内容内联到代码中，不需要额外的运行时解析。

> ⚠️ 注意：Rollup 在打包时会将 JSON 解析为 JavaScript 对象字面量并直接内联。这意味着如果你的 JSON 文件很大，打包后的代码会包含所有键值对——即使你只用了其中一小部分。所以在发布 npm 包时，如果 JSON 体积较大，建议通过 `rollup.config.js` 的 `external` 选项把 JSON 文件排除掉，让消费者自行 `import` 读取（Node.js 原生支持 `import` JSON，无需额外处理）。

## 3.7.3 WebAssembly（.wasm）模块支持

WebAssembly 是一种可以运行在浏览器中的二进制指令集格式，某些对性能要求极高的场景会用到它。Rollup 通过 `@rollup/plugin-wasm` 支持 WebAssembly 模块：

```javascript
// rollup.config.js
import wasm from '@rollup/plugin-wasm';

export default {
  plugins: [
    wasm({
      // 指定哪些 .wasm 模块可以同步加载（必须是具体的模块 ID，不能是 glob）
      sync: ['node_modules/some-wasm-lib/pkg/module.wasm']
    })
  ]
};
```

```javascript
// 加载 WebAssembly 模块
import init from './my-module.wasm';

const instance = await init();
const result = instance.exports.add(1, 2);  // 调用 WASM 函数
console.log(result);  // 3
```
