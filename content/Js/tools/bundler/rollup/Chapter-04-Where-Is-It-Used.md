+++
title = "第4章 用在哪里"
weight = 40
date = "2026-03-28T11:38:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 4 章　用在哪里

---

## 4.1 开源库 / npm 包发布

如果说 Rollup 是前端构建工具链中的瑞士军刀，那 npm 包发布就是它最闪耀的舞台。为啥？因为 Rollup 天生就是为了"精准投放"而生的——它只想把你写的代码打包成最小可用的形式，不会往包里塞一堆乱七八糟的东西。

### 4.1.1 Vue 生态（Vue 3 自身源码使用 Rollup 打包）

Vue 3 是最早大规模采用 Rollup 的知名项目之一。Vue 3 的 npm 发布包（`vue`、`@vue/runtime-core`、`@vue/runtime-dom`、`@vue/reactivity` 等）就是用 Rollup 打包的。当你 `npm install vue` 的时候，安装的包就是由 Rollup 打包生成的产物——这直接证明了 Rollup 在大型项目中的可靠性。

Vue 官方团队选择 Rollup 的理由很简单：**Tree-Shaking 做得好，产物小，Vue 用户只需要为他们真正用到的功能付费**。比如你没有用 `v-model`，就不会打包相关代码；没有用 Transition 组件，对应的运行时就不会打包进去。

### 4.1.2 React 生态（许多 React 库采用 Rollup 构建）

React 生态中有很多知名库使用 Rollup 打包：

- **react-router**：React 生态最流行的路由库
- **formik**：表单处理库
- **react-final-form**：高级表单状态管理库
- **date-fns**：一个"可 tree-shake" 的日期处理库（相比 moment.js 体积小得多）

这些库选择 Rollup 的共同原因是：**让消费者只加载他们用到的部分**。date-fns 如果不打包成支持 Tree-Shaking 的形式，用户引入整个库会是 ~100KB；但通过 Rollup 打包后，用户只引入 `format` 和 `parse` 两个函数，最终体积可能只有 ~10KB。

### 4.1.3 工具库（rxjs / express 等）

RxJS 是响应式编程领域最流行的库，它的体积极其庞大（完整引入 ~2MB）。通过 Rollup 打包成支持 Tree-Shaking 的 ESM 格式后，用户可以只引入自己用到的操作符：

```javascript
// 以前用 RxJS（完整引入，体积巨大）
import Rx from 'rxjs';  // 全部加载，~2MB，体积感人

// 现在用 RxJS 7+（按需引入，通过 Rollup Tree-Shaking 优化）
// 注意：from、map、filter 都可以直接从 'rxjs' 导入，一个 import 语句全搞定
import { from, map, filter } from 'rxjs';
from([1, 2, 3]).pipe(
  map(x => x * 2),
  filter(x => x > 2)
).subscribe(x => console.log(x));  // 最终可能只打包 ~5KB
```

> 💡 **RxJS 7+ 小贴士**：RxJS 7+ 统一了导入方式，大多数操作符都可以直接从 `rxjs` 导入（比如 `import { map, filter } from 'rxjs'`），不再强制要求从 `rxjs/operators` 导入。如果你看到老代码里 `import { map } from 'rxjs/operators'`，那是 RxJS 6 的写法——现在属于"活化石"级别的东西了，看到可以顺手升级一下。

Express 是 Node.js 生态最流行的 Web 框架之一，它中间件的注册机制让用户可以按需引入需要的部分——这和 Rollup 打包的思路有异曲同工之处。

### 4.1.4 UI 组件库（Ant Design / Element UI 构建工具链）

Ant Design 是 React 生态中最知名的 UI 组件库之一，它的构建工具链颇为复杂——Gulp 负责整体流程编排，Rollup 负责组件级别的打包和 Tree-Shaking，最终产物同时支持 ESM/CJS/UMD 多种格式。

Element Plus（Vue 3）也是类似，用 Rollup 打包出体积最小化的组件库，让用户按需引入。需要注意的是，老版的 Element UI（Vue 2）构建配置更为繁复（gulp + rollup + webpack 的混合配置），而新版的 Element Plus 则更加统一和简洁。

---

## 4.2 前端工具链开发

前端工具链的开发者是 Rollup 的重度用户群体——毕竟做工具的人自己也得用工具，而工具最大的追求就是：**快、小、稳**。Rollup 完美符合这三个要求，所以 Babel、ESLint、Vite 这些大名鼎鼎的工具都选择用它来打包自己的插件和核心代码。

### 4.2.1 Babel 插件

Babel 插件本质上是一些接收 Babel API 参数、返回转换器的函数。Babel 官方团队使用 Rollup 来打包所有 Babel 插件。

Babel 插件的结构通常是这样的：

```javascript
// 一个简单的 Babel 插件示例：禁止 console（生产环境统一日志规范）
export default function noConsolePlugin() {
  return {
    visitor: {
      // 访问所有函数调用表达式
      CallExpression(path) {
        const { callee } = path.node;

        // 检查是否是 console.xxx 的调用
        if (
          callee.type === 'MemberExpression' &&
          callee.object.type === 'Identifier' &&
          callee.object.name === 'console'
        ) {
          path.node.loc && console.warn(
            `⚠️ 发现 console.${callee.property.name || 'log'} 调用 (line ${path.node.loc.start.line})`
          );
          // 正确做法：用 context.report 上报 lint 错误（这里仅作演示）
          // context.report({ node: path.node, message: '生产代码禁止使用 console' });
        }
      }
    }
  };
}
```

这个插件演示了 Babel 插件的核心工作方式：通过 `visitor` 对象访问特定类型的 AST 节点，在节点上读取或修改信息。Babel 官方团队选择 Rollup 来打包这些插件，主要是因为 Rollup 输出干净、Tree-Shaking 效果好——毕竟插件本身可能很小巧，用户不希望因为装了一个插件而多打包一堆无关代码。

用 Rollup 打包后，这个插件就可以作为一个 npm 包被其他项目使用了。

### 4.2.2 Webpack Loader / Plugin

Webpack Loader 的作用是"翻译"特定类型的文件。比如 `babel-loader` 的工作就是把 ES6+ 代码转成 ES5，`sass-loader` 的工作是把 SCSS 转成 CSS。

Webpack Plugin 的作用则是在 Webpack 打包过程中的特定时机插入自定义逻辑。

这两者的打包同样适合用 Rollup：

```javascript
// 一个简单的 Webpack Plugin 示例
class MyWebpackPlugin {
  apply(compiler) {
    // 在打包完成时触发
    compiler.hooks.done.tap('MyWebpackPlugin', (stats) => {
      console.log('打包完成！');
      console.log('产物大小:', stats.toJson().assets);
    });
  }
}

export default MyWebpackPlugin;
```

### 4.2.3 ESLint 插件 / Rules

ESLint 插件就是 ESLint 规则的集合。ESLint 团队官方使用 Rollup 来打包所有官方插件：

```javascript
// 一个 ESLint 规则示例：禁止 console（统一日志规范）
export default {
  meta: {
    type: 'problem',
    docs: {
      description: '禁止使用 console，统一使用项目 logger',
      recommended: true
    }
    // 注意：没有 fixable 字段表示这个规则不支持自动修复
  },
  create(context) {
    return {
      CallExpression(node) {
        // 检查是否是 console.xxx 的调用（console.log / console.warn / console.error 等）
        if (
          node.callee.type === 'MemberExpression' &&
          node.callee.object.name === 'console'
        ) {
          context.report({
            node,
            message: '禁止使用 console，请使用项目统一的 logger'
          });
        }
      }
    };
  }
};
```

### 4.2.4 Vite 插件

Vite 插件本质上是一个返回特定生命周期钩子对象（或者函数）的工厂。Vite 官方使用的就是 Rollup 作为底层打包引擎，所以 Vite 插件实际上就是在 Rollup 的插件系统上封装了一层：

```javascript
// 一个简单的 Vite 插件示例：自动导入日志模块
export default function autoLoggerPlugin() {
  return {
    name: 'auto-logger',           // 插件名称（必须唯一）
    transform(code, id) {
      // 只处理业务代码，跳过 node_modules（最常用写法）
      if (id.includes('node_modules')) return null;

      // 检测是否有 console.log，没有则自动添加
      if (!code.includes('console.log') && !code.includes('logger.')) {
        return {
          code: `import { logger } from '../utils/logger.js';\n${code}`,
          map: null
        };
      }
      return null;
    }
  };
}
```

这个插件展示了 Vite 插件的典型模式：在 `transform` 钩子里对代码做转换处理。Vite 官方选择 Rollup 作为底层打包引擎，正是看中了 Rollup 插件系统的简洁和高效——Vite 插件本质上就是 Rollup 插件的超集（Vite 在 Rollup 插件接口基础上扩展了自己独有的钩子）。

### 4.2.5 微前端框架（qiankun 等子应用打包）

微前端是一种将大型前端应用拆分为多个独立子应用的架构模式。每个子应用都可以独立开发、独立部署，Rollup 打包出来的干净小产物在这种场景下简直是量身定做。

qiankun 是蚂蚁集团开源的微前端框架，它支持多种打包方式（Rollup、Vite、Webpack 均可）。使用 Rollup 打包子应用的优势在于：产物干净、体积小、加载快，非常适合微前端场景下对性能的严苛要求。如果子应用使用 Vite 开发，直接用 Vite 打包也是完全可行的——qiankun 官方对这两种方式都有良好支持。

> 💡 **qiankun + Rollup 的最佳实践**：子应用的入口文件建议使用 `format: 'iife'` 或 `format: 'system'`，因为 qiankun 的沙箱机制需要子应用导出为一个全局函数。Rollup 对这两种格式的支持非常好，配上 `name` 字段即可。

---

## 4.3 Vite 生产构建

这是 Rollup 被使用得最广泛的场景——尽管很多开发者可能没有意识到他们在"用 Rollup"。想象一下：全球几百万个项目用 Vite 构建生产代码，而这些项目的最终产物，都出自 Rollup 之手。Rollup 在幕后默默干活，却很少被人记起——这大概就是开源世界里的"幕后英雄"吧。

### 4.3.1 Vite 架构：开发用 esbuild，生产用 Rollup

Vite 是一个"开发时快如闪电，生产时质量过硬"的构建工具。它的架构设计非常聪明：

- **开发阶段**：使用 **esbuild** 做依赖预构建和即时转译。esbuild 是用 Go 语言写的，打包速度极快（比 Webpack 快 10-100 倍），Vite 启动时会先对项目依赖进行预构建（把 CJS 转成 ESM、合并 import 等），之后用户访问页面时请求的代码已经是预转译好的 ESM，用户几乎感觉不到等待。
- **生产阶段**：使用 **Rollup** 做最终打包。Rollup 的 Tree-Shaking 和多格式输出能力能确保最终产物既小又快。

```mermaid
graph LR
    A["开发阶段<br/>启动 Vite Dev Server"] --> B["esbuild 依赖预构建<br/>（CJS→ESM、合并 import）"]
    B --> C["用户访问页面"]
    C --> D["浏览器请求 ES Module<br/>（已预转译）"]
    D --> E["热更新 HMR<br/>仅重新加载变化的部分"]

graph LR
    F["生产阶段<br/>执行 vite build"] --> G["Rollup 打包"]
    G --> H["优化产物<br/>Tree-Shaking + 压缩"]
    H --> I["部署到服务器"]
```

> **esbuild 依赖预构建**：这是 Vite 开发阶段的第一步，会把项目依赖（如 `node_modules` 中的 CJS 库）提前转成 ESM，并处理 `import` 合并等。这不是"访问时"才发生，而是在你敲下 `vite` 命令后就悄悄完成了。

这种"开发用 esbuild，生产用 Rollup"的架构，既保证了开发体验，又保证了产物质量，是 Vite 成为现代前端主流工具的重要原因。

### 4.3.2 `vite build` 命令底层调用 Rollup

当你执行 `npm run build`（对应的命令就是 `vite build`）时，Vite 实际上就是在调用 Rollup：

```bash
$ vite build

# Vite 底层输出类似这样的日志：
# building for production...
# ✓ 42 modules transformed.
# dist/index.html    0.46 kB
# dist/assets/index.a1b2c3d4.js   142.35 kB │ gzip: 46.12 kB
# ✓ built in 1.23s
```

这个过程完全由 Rollup 完成，Vite 只是做了一个"包裹"和"配置传递"的工作。

### 4.3.3 通过 vite.config.js 的 rollupOptions 自定义配置

如果你需要在 Vite 的 Rollup 构建过程中做一些特殊配置，可以通过 `vite.config.js` 的 `rollupOptions` 来做：

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      // 多入口配置
      input: {
        main: './index.html',
        admin: './admin.html'
      },
      // 输出配置
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom']
        }
      },
      // 插件配置（会合并到 Rollup 插件列表中）
      plugins: [
        // 你的自定义 Rollup 插件
      ]
    }
  }
});
```

### 4.3.4 动态导入与代码分割（Code Splitting）

Rollup 的另一个杀手锏是**动态导入**（Dynamic Import）。配合 `input` 配置成对象（或在插件中返回 `Promise`），可以实现自动代码分割：

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // 按需分割：将 node_modules 里的包单独拆成 vendor chunk
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // 简单写法：所有 node_modules 打包成一个 vendor chunk
            // return 'vendor';
            // 进阶写法：每个 npm 包单独一个 vendor-chunk
            // 注意：scoped 包（如 @babel/runtime）需要特殊处理
            const match = id.match(/node_modules\/(@?[^/]+)/);
            if (match) return `vendor-${match[1].replace('/', '-')}`;
          }
        }
      }
    }
  }
});
```

在实际项目中，动态导入最典型的用法是配合 ES6 动态 `import()`：

```javascript
// 用户点击按钮时，才加载这个组件（不用一开始全量加载）
// 注意：await 只能在 async 函数中使用
button.addEventListener('click', async () => {
  const { default: HeavyChart } = await import('./components/HeavyChart.vue');
  new HeavyChart('#chart');
});
```

Rollup 会把这个动态 import 单独打包成一个 chunk，用户只有在触发这个 import 时才会请求对应的 JS 文件——这对于首屏加载优化极其重要。

---

## 4.4 Monorepo 项目

Monorepo（单体仓库）是一种将多个相关项目放在同一个代码仓库中管理的架构方式。Rollup 在 Monorepo 中有独特的价值。

### 4.4.1 子模块独立打包

在 Monorepo 中，一个仓库包含多个子包（比如 `packages/utils`、`packages/ui`）。每个子包通常需要独立打包发布。

Rollup 可以为每个子包配置独立的打包任务：

```javascript
// packages/utils/rollup.config.js
export default {
  input: 'src/index.js',
  output: {
    file: 'dist/index.js',
    format: 'es'
  }
};
```

### 4.4.2 共享包的构建与发布

在 Monorepo 中，共享包被多个子包依赖。Rollup 可以高效地处理这种场景——把共享包打包成支持 Tree-Shaking 的格式，让每个子包在打包时只引入自己真正用到的部分。

典型的共享包配置如下：

```javascript
// packages/shared/rollup.config.js
export default {
  input: 'src/index.js',
  output: [
    // ESM 格式：供支持 Tree-Shaking 的构建工具使用
    { file: 'dist/index.mjs', format: 'esm' },
    // CJS 格式：供 Node.js 环境或旧项目使用
    { file: 'dist/index.cjs.js', format: 'cjs' }
  ],
  // 外部化 peerDependencies，让消费者自己负责
  external: ['react', 'vue']
};
```

> ⚠️ **一个重要的坑**：Rollup 的 Tree-Shaking 对 **CommonJS 模块支持有限**。如果你写的库依赖了 CJS 格式的 npm 包，Rollup 可能无法正确分析其导出结构，导致 Tree-Shaking 失效。**最佳实践是**：始终把你的库打包成纯 ESM 格式，并确保依赖的 npm 包也优先使用 ESM 版本（很多现代库都提供了 `exports` 字段指向 ESM 构建）。

---

## 4.5 Electron / Web Extensions

### 4.5.1 Electron 主进程与渲染进程打包

Electron 应用同时包含"主进程"（运行在 Node.js 环境）和"渲染进程"（运行在浏览器环境）。这两种环境对代码格式的要求不同：主进程通常使用 CommonJS（因为 Electron 主进程默认是 CJS），而渲染进程因为要跑在浏览器里，需要 ESM 或 IIFE 格式。Rollup 可以分别为两种环境打包出合适的产物：

```javascript
// electron 主进程打包配置（Node.js 环境）
export default {
  input: 'src/main/index.js',
  output: {
    file: 'dist/main.js',
    format: 'cjs',  // Electron 主进程使用 CommonJS
    banner: "'use strict';"  // 确保严格模式
  },
  external: ['electron', 'node-fetch']  // 外部依赖不打包，由 Electron 运行时提供
};

// electron 渲染进程打包配置（浏览器环境）
export default {
  input: 'src/renderer/index.js',
  output: {
    file: 'dist/renderer.js',
    format: 'esm',  // 现代 Electron 渲染进程推荐 ESM
    sourcemap: true
  }
};
```

### 4.5.2 浏览器扩展（Chrome Extension）打包

Chrome 扩展（以及 Firefox、Edge 等浏览器的扩展）本质上是 HTML + CSS + JavaScript 的组合。Rollup 可以把多个脚本文件打包成一个（或几个），同时支持 `manifest.json` 配置中指定的 CSP（内容安全策略）。

```javascript
// Chrome 扩展的打包配置
export default {
  input: 'src/background.js',
  output: {
    file: 'dist/background.js',
    format: 'iife',  // Chrome 扩展 background 脚本用 IIFE
    name: 'background'
  }
};
```

---

## 4.6 Rollup 不适合的场景

说完 Rollup 能做什么，也要诚实地说说它不适合什么。

### 4.6.1 大型 Web 应用热更新开发（用 Vite / Webpack Dev Server）

Rollup 的设计初衷就不是"开发服务器"，它没有真正意义上的 HMR（热模块替换）能力。Rollup 的 watch 模式更像是"检测文件变化 → 重新打包"，而不是"只更新变化的模块，页面状态保持不变"。虽然可以通过插件实现简单的热更新，但和 Vite / Webpack 的开发服务器比起来，体验差距不是一星半点——简直是走路和坐火箭的区别。

> **HMR（Hot Module Replacement，热模块替换）是什么？**
> HMR 是一种开发时的高级功能：当你的代码发生变化时，不需要刷新整个页面，只需要替换（更新）变化的那部分模块，页面的其他部分保持不变。对于有复杂状态的前端应用（比如 Vue/React 应用），HMR 可以让你在修改代码后瞬间看到效果，而不需要重新操作一遍应用状态。想象一下：你花 10 分钟填好了一个表单，因为改了一行 CSS 要重新填——HMR 就是来拯救你的。

Rollup 的 watch 模式更偏向于"文件变了，重新打包"，而不是"局部更新"——这在大型应用里意味着你每次保存都要等完整的增量构建，虽然比全量快，但还是会打断思路。

### 4.6.2 需要强 HMR（热模块替换）实时重载的场景

如果你需要一个在保存代码后毫秒级看到效果的开发体验，Rollup 同样不是你的菜。这个场景应该用 **Vite**（开发服务器用 esbuild 即时转译）或 **Webpack**（内置成熟 HMR）——它们的 watch + 热更新链路是专门为"改一行代码等三秒"这种痛苦场景优化的。

### 4.6.3 watch 模式对大项目的性能瓶颈

Rollup 的 watch 模式在小型项目中表现良好，但当项目规模变大（几百个模块）时，每次文件变化触发的增量构建也会开始变慢。对于这种场景，建议直接使用 Vite 或 Webpack，它们有更完善的增量构建缓存机制。

### 4.6.4 需要 polyfill 的浏览器兼容场景

Rollup 本身不处理 polyfill。如果你需要兼容旧版浏览器（比如要支持 `Promise`、`Array.prototype.includes` 等），Rollup 不会像 Webpack 5 那样自动注入 polyfill。这种场景下，要么在源码中手动引入 polyfill（如 `core-js`），要么在构建链中额外加一层处理（比如 Rollup 打包后再用 esbuild 或 Babel 处理一遍）。

---

说了这么多"不适合"，你可能会想：Rollup 是不是很弱？恰恰相反——**知道自己不擅长什么，是它最强的优点**。Rollup 从来不试图做一个全能的构建工具，它只做自己擅长的事，并且做到极致。正是因为这种专注，Rollup 才能在"库打包"和"Vite 底层"这两个领域做到无可替代。

---

## 本章小结

这一章我们系统地梳理了 Rollup 的主要应用场景：

1. **开源库 / npm 包发布**：Vue 生态、React 生态、工具库、UI 组件库，Rollup 是这些场景的首选打包工具。它让用户"只为你用到的功能付费"。

2. **前端工具链开发**：Babel 插件、Webpack Loader/Plugin、ESLint 插件、Vite 插件、微前端子应用，都适合用 Rollup 打包。工具链追求快、小、稳，Rollup 完美契合。

3. **Vite 生产构建**：Vite 的生产构建底层就是 Rollup，所有使用 Vite 的开发者都在间接使用 Rollup。动态导入与代码分割（Code Splitting）也是通过 Rollup 的 `manualChunks` 和动态 `import()` 实现的。

4. **Monorepo 项目**：子模块独立打包、共享包的高效构建与发布——Rollup 让 monorepo 中的包既能独立发布，又能被其他包按需引用。

5. **Electron / Web Extensions**：主进程、渲染进程、浏览器扩展都可以用 Rollup 打包，按需生成不同格式的产物。

6. **不适用的场景**：大型 Web 应用的热更新开发、强 HMR 需求场景、watch 模式对大项目的性能瓶颈——这些场景应该选择 Vite 或 Webpack。

---

**一句话总结**：Rollup 是那种"知道自己擅长什么"的工具——它不是万能的，但在它擅长的领域（库打包、工具链、Vite 底层），它几乎是无可替代的存在。用好 Rollup，就是让它做它最擅长的事，而不是强迫它去干热更新开发服务器的活儿。