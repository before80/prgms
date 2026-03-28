+++
title = "第7章 相关配置"
weight = 70
date = "2026-03-28T11:38:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 7 章　相关配置

---

## 7.1 输入配置（Input）

输入配置决定了"从哪里开始打包"，是整个 Rollup 配置的起点。

### 7.1.1 input：入口文件路径（字符串 / 对象多入口 / 数组）

`input` 是**必填项**（什么？你想不写？Rollup 会毫不客气地报错），它告诉 Rollup"从哪里开始找代码"。

```javascript
// 方式 1：字符串（单入口，最常见）
export default {
  input: 'src/main.js'
};

// 方式 2：对象（多入口，打包成多个独立的产物）
export default {
  input: {
    main: 'src/main.js',      // 产物：dist/main.js
    admin: 'src/admin.js',   // 产物：dist/admin.js
    vendor: 'src/vendor.js'  // 产物：dist/vendor.js
  },
  output: {
    dir: 'dist'  // 多入口时必须用 dir，不能用 file
  }
};

// 方式 3：数组（等价格式 2）
export default {
  input: ['src/main.js', 'src/admin.js', 'src/vendor.js'],
  output: { dir: 'dist' }
};
```

### 7.1.2 external：外部依赖列表（字符串 / 函数 / 正则）

`external` 配置告诉 Rollup 哪些模块不需要打包：

```javascript
export default {
  input: 'src/main.js',
  external: [
    // 精确包名
    'react',
    'react-dom',
    'lodash',

    // 正则匹配（所有以 @scope/ 开头的包，如 @scope/foo、@scope/bar）
    /^@[\w-]+\/[\w-]+/,

    // 函数（最灵活，根据路径判断）
    (id, parentId) => {
      // 不打包 node_modules 中的内容（但保留你自己包的代码）
      if (id.includes('node_modules') && !id.includes('my-local-package')) {
        return true;
      }
    }
  ]
};
```

### 7.1.3 cache：启用构建缓存（加快二次构建速度）

`cache` 选项可以让 Rollup 复用上一次构建的结果，加快二次构建速度：

```javascript
let bundle;

async function build() {
  if (bundle) {
    // 复用上一次的缓存
    const newBundle = await rollup({
      input: 'src/main.js',
      cache: bundle.cache  // 传入上次的 cache
    });
    bundle = newBundle;  // 构建成功后再更新引用
  } else {
    // 首次构建
    bundle = await rollup({ input: 'src/main.js' });
  }

  await bundle.write({ file: 'dist/bundle.js', format: 'es' });
}
```

> 🤔 **为什么要单独用 `newBundle` 接收？** 如果直接 `bundle = await rollup(...)`，万一构建过程中途出错，`bundle` 就会被覆盖成不完整的对象，下一次构建就丧失了缓存能力。用临时变量接住，成功后再赋值，更稳妥！

在 Vite 的 Rollup 配置中，这个选项是自动启用的，不需要手动配置。

### 7.1.4 preserveSymlinks：是否保留符号链接解析行为

当设置为 `true` 时，Rollup 不会解析符号链接（symlink），而是把符号链接当作真实的文件路径来处理。这个选项在 Monorepo 中特别有用，因为 Monorepo 中经常使用 npm workspace 的符号链接机制。

```javascript
export default {
  input: 'src/main.js',
  preserveSymlinks: true  // 保持符号链接，不解析真实路径
};
```

> 🤔 **为什么需要这个？** 假设你用 npm workspace，在 `node_modules/my-lib` 下有个指向源代码的符号链接。如果关闭 `preserveSymlinks`（默认值），Rollup 会顺着符号链接找到真实路径——也就是源代码目录！结果打包进去的不是编译好的 dist 文件，而是未经编译的源文件。这可不是你想要的结果！开启 `preserveSymlinks: true` 才能保持符号链接指向正确的编译产物。

---

## 7.2 输出配置（Output）

输出配置决定了打包产物"长什么样"，以及"放到哪里去"。

### 7.2.1 output.dir：输出目录（多入口时必须设置）

```javascript
// 多入口时必须指定 dir
export default {
  input: { main: 'src/main.js', admin: 'src/admin.js' },
  output: {
    dir: 'dist'  // 产物会输出到 dist/main.js 和 dist/admin.js
  }
};
```

### 7.2.2 output.file：输出文件名（单入口专用，与 dir 互斥）

```javascript
// 单入口时用 file
export default {
  input: 'src/main.js',
  output: {
    file: 'dist/bundle.js',  // 只能指定单个文件
    format: 'es'
  }
};
```

> **注意**：`file` 和 `dir` 只能二选一，不能同时使用。

### 7.2.3 output.format：输出格式（es / cjs / umd / iife / amd / system）

这是最常用的输出配置项，决定了打包产物的模块格式：

```javascript
export default {
  output: {
    format: 'es'   // 可选值：es | cjs | umd | iife | amd | system
  }
};
```

| 值 | 全称 | 适用场景 |
|---|---|---|
| `es` | ES Module | 现代浏览器 / 其他 bundler |
| `cjs` | CommonJS | Node.js |
| `umd` | Universal Module Definition | 浏览器 + Node 都支持 |
| `iife` | Immediately Invoked Function Expression | 浏览器 `<script>` 标签 |
| `amd` | Asynchronous Module Definition | RequireJS |
| `system` | SystemJS | SystemJS 加载器 |

### 7.2.4 output.name：UMD / IIFE 全局变量名

当输出格式为 `umd` 或 `iife` 时，Rollup 需要知道"把这个库挂到哪个全局变量上"：

```javascript
export default {
  output: {
    format: 'umd',
    name: 'MyLibrary'  // 在浏览器中可以通过 window.MyLibrary 访问
  }
};
```

生成的 UMD 代码会这样引用全局变量：

```javascript
root.MyLibrary = factory(root.React);
// 即 window.MyLibrary = factory(window.React)
```

### 7.2.5 output.extend：UMD / IIFE 全局对象为扩展还是覆盖（true 扩展 / false 覆盖）

```javascript
export default {
  output: {
    format: 'umd',
    name: 'MyLibrary',
    // true（默认）：把自己的属性合并到全局对象上（不删除已有的）
    // false：直接覆盖全局对象
    extend: true
  }
};
```

> ⚠️ **容易踩坑的地方**：`extend: true` 时，如果 `window.MyLibrary` 已经存在，Rollup 会把新属性**合并**进去；`extend: false` 时，会**整个替换** `window.MyLibrary`（可能造成其他库的数据丢失！）。大多数时候保持默认的 `true` 就好。

### 7.2.6 output.globals：external 模块对应的全局变量名（UMD / IIFE）

```javascript
export default {
  input: 'src/main.js',
  external: ['react', 'lodash'],
  output: {
    format: 'umd',
    name: 'MyLibrary',
    globals: {
      react: 'React',    // 提到 react 时，用 window.React
      lodash: '_'        // 提到 lodash 时，用 window._
    }
  }
};
```

### 7.2.7 output.banner：每个 chunk 文件顶部插入注释

```javascript
export default {
  output: {
    banner: '/*! MyLibrary v1.0.0 | (c) 2026 MIT */',
    // 生成: /*! MyLibrary v1.0.0 | (c) 2026 MIT */\n const ...
  }
};
```

### 7.2.8 output.footer：每个 chunk 文件底部插入注释

```javascript
export default {
  output: {
    footer: '/* Built with Rollup */',
    // 生成: ...\n/* Built with Rollup */
  }
};
```

### 7.2.9 output.intro：每个 chunk 顶部插入代码片段（如 import polyfills）

`intro` 和 `banner` 的区别是：`banner` 是字符串注释，`intro` 可以是任何 JavaScript 代码片段（比如 import 语句）：

> 🎯 **经典场景**：在产物顶部注入 polyfill（Promise、fetch 等）、环境变量初始化代码、或者全局错误捕获逻辑。比起在源码里到处 import，在 `intro` 里统一注入更省心！

```javascript
export default {
  output: {
    intro: `
      import 'promise-polyfill';
      if (!window.Promise) window.Promise = Promise;
    `
  }
};
```

> 🤔 **为什么用 `import 'promise-polyfill'` 而不是 `import Promise from 'promise-polyfill'`？** 因为 polyfill 只需要"执行"，不需要引用返回值。而且 `import` 放在 `intro` 里是直接拼到产物顶部的，如果用默认导入可能产生奇怪的变量引用，直接执行不依赖返回值，更省心！

### 7.2.10 output.outro：每个 chunk 底部插入代码片段

`outro` 和 `intro` 正好相反，插入到文件底部。和 `banner`/`footer` 的区别同上（一个是注释字符串，一个是任意代码片段）：

```javascript
export default {
  output: {
    outro: 'console.log("打包时间:", new Date().toISOString());'
  }
};
```

> 🎯 **经典用法**：在库中输出 `"MyLibrary loaded!"`、添加构建信息戳、或者注入统计代码（比如上报 CDN 版本等）。

### 7.2.11 output.sourcemap：Source Map 生成（true / false / 'inline'）

```javascript
export default {
  output: {
    sourcemap: true      // 生成独立的 .map 文件
    // sourcemap: false    // 不生成 Source Map（节省体积）
    // sourcemap: 'inline' // Source Map 内联到 JS 文件末尾（方便单文件传输）
  }
};
```

### 7.2.12 output.sourcemapIgnoreList：排除特定文件或 node_modules

```javascript
export default {
  output: {
    sourcemap: true,
    // 排除 node_modules，这样调试时不会跳到第三方库的源码
    sourcemapIgnoreList: (filePath) => filePath.includes('node_modules')
  }
};
```

### 7.2.13 output.assetFileNames：静态资源输出命名规则

```javascript
export default {
  output: {
    // [name] 原始文件名，[hash] 内容哈希，[extname] 扩展名
    assetFileNames: 'assets/[name]-[hash][extname]'
    // 输出: dist/assets/font-awesome-[hash].woff2
  }
};
```

> 💡 **可用的命名变量**：`[name]`（原始文件名）、`[hash]`（内容哈希）、`[extname]`（扩展名，含点如 `.woff2`）、`[ext]`（扩展名，不含点如 `woff2`）。这些变量同样适用于 `chunkFileNames` 和 `entryFileNames`。

### 7.2.14 output.chunkFileNames：代码分割后 chunk 的命名规则

```javascript
export default {
  output: {
    chunkFileNames: 'chunks/[name]-[hash].js'
    // 输出: dist/chunks/vendor~react-[hash].js
  }
};
```

> 💡 **命名规则中的特殊字符**：代码分割产生的 chunk 名称会自动带上 `~` 分隔符来标识来源入口。比如 `vendor~main~admin` 表示这个 chunk 同时被 `main` 和 `admin` 两个入口共享。`[name]` 替换为 chunk 的逻辑名称（由 `manualChunks` 返回的值）。

### 7.2.15 output.entryFileNames：入口文件的命名规则

```javascript
export default {
  output: {
    entryFileNames: '[name]-[hash].js'
    // 输出: dist/main-[hash].js
  }
};
```

> 💡 **命名变量说明**：`[name]` 是入口名称（如 `main`、`admin`），`[hash]` 是基于内容生成的内容哈希（内容不变则哈希不变，便于缓存）。如果不需要 hash 去掉这个变量即可。

### 7.2.16 output.inlineDynamicImports：内联动态导入（⚠️ Rollup 4.x 已废弃）

当设置为 `true` 时，Rollup 不会把动态 `import()` 的模块分割成独立文件，而是内联到主文件中。不过在 Rollup 4.x 中，这个选项已经被废弃了——现在你应该用 `output.manualChunks` 来精确控制代码分割策略。

```javascript
export default {
  output: {
    // true：禁用代码分割，所有代码打包进一个文件（⚠️ 已废弃）
    inlineDynamicImports: true
  }
};
```

> 💡 **推荐做法**：用 `manualChunks` 替代 `inlineDynamicImports`，可以更细粒度地控制哪些模块应该被分割成独立 chunk。

### 7.2.17 output.manualChunks：自定义代码分割策略（🔥 最重要！没有之一）

`manualChunks` 是 Rollup 最强大的代码分割配置项，允许你把打包产物拆成多个小块，按需加载：

```javascript
export default {
  input: 'src/main.js',
  output: {
    dir: 'dist',
    format: 'es',
    manualChunks(id) {
      // 把 node_modules 的代码单独打包成 vendor chunk
      if (id.includes('node_modules')) {
        return 'vendor';  // 所有第三方库打包到 vendor.js
      }
    }
  }
};
```

更细粒度的控制：

```javascript
manualChunks(id) {
  // React 生态单独打包
  if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
    return 'react-vendor';
  }
  
  // Lodash 单独打包
  if (id.includes('node_modules/lodash')) {
    return 'lodash-vendor';
  }
  
  // 其他 node_modules 打成一个大 vendor
  if (id.includes('node_modules')) {
    return 'vendor';
  }
}
```

> 🎯 **经典场景**：把不常变化的第三方库（vendor）和业务代码分开，这样用户只需下载一次 vendor，后续更新业务代码时可以享受缓存红利！

### 7.2.18 output.manualAsyncChunks：异步 chunk 的手动分割策略

```javascript
export default {
  output: {
    // 和 manualChunks 类似，但专门用于异步加载的 chunk
    manualAsyncChunks: (id) => {
      if (id.includes('node_modules/large-lib')) {
        return 'async-vendor';
      }
    }
  }
};
```

> 注意：这个选项在 Rollup 4.x 中同样是实验性的，API 可能会有变化。

### 7.2.19 output.externalLiveBindings：保留 CJS 风格的 live bindings

```javascript
export default {
  output: {
    // true（默认）：Rollup 会生成能在 CJS 中保持 live binding 的代码
    // false：代码更简洁，但某些 edge case 下行为可能不同
    externalLiveBindings: true
  }
};
```

### 7.2.20 output.esModule：是否添加 `__esModule` 标记（true / false）

```javascript
export default {
  output: {
    // true（默认）：给产物添加 __esModule: true 标记，方便 CJS 环境识别
    // false：不添加，适合纯 ESM 输出
    esModule: true
  }
};
```

> 💡 **为什么有这个选项？** `__esModule` 标记是 Rollup 为了兼容 CommonJS 默认导出而添加的元数据。当你用 `import React from 'react'` 这种默认导入方式消费一个 CJS 模块时，Rollup 会生成一个 interop helper 来处理。如果你的库只输出纯 ESM，可以设为 `false` 跳过这个开销。

### 7.2.21 output.hoistTransitiveImports：提升传递依赖的导入语句

这个选项控制"如果 A 导入了 B，B 导入了 C，最终产物要不要把 C 的导入提升到 A 里面"：

```javascript
export default {
  output: {
    // true（默认）：A 引入了 B，B 引入了 C？没关系，产物直接让 A 认识 C（跳过 B 这个"中间商"）
    // false：保持原始的依赖层级，该走 B 就走 B
    hoistTransitiveImports: true
  }
};
```

> 🤔 **什么时候需要关闭？** 大多数时候默认就行。但如果你的代码依赖精确的模块顺序（比如调试时），可以关掉让产物更接近源码结构。
>
> 💡 **典型场景**：假设 A.js 导入了 B，B 导入了 C。当你启用 `hoistTransitiveImports: true` 时，产物中的 A 会直接 `import { something } from 'C'`（跳过 B）；关闭时则保持 `A → B → C` 的原始链路。前者产物更扁平，后者调试更方便（断点能精准命中源码位置）。

### 7.2.22 output.generatedCode：输出 JS 语法特性（es2015 / esnext / preserved）

```javascript
export default {
  output: {
    // es2015：输出 ES2015 兼容的代码（适合较老的目标环境）
    generatedCode: 'es2015',

    // esnext：使用最新语法特性（产物更小，但需要目标环境支持）
    // generatedCode: 'esnext',

    // preserved：尽量保留源代码的语法特性
    // generatedCode: 'preserved'
  }
};
```

### 7.2.23 output.reexportHelpers：将 helper 函数内联而非 external（⚠️ Rollup 4.x 已废弃）

某些语法转换会产生 helper 函数（如 `_classCallCheck`、`_defineProperty` 等）。在 Rollup 4.x 中，此选项**已被废弃**，helper 函数现在**始终内联**到产物中，不再支持 external 化。以下是旧版本的行为描述（仅作参考）：

```javascript
export default {
  output: {
    // 在 Rollup 4.x 中，这个选项已无效，helper 函数始终内联
    // 之前的版本可以用它控制是否把 helper 函数抽取为独立 chunk
    reexportHelpers: true   // ⚠️ 已废弃，无效果
  }
};
```

> 🔥 **迁移提示**：如果你之前用 `reexportHelpers: false` 配合 `generatedCode: 'esnext'` 来external化 helper 函数，现在 Rollup 4.x 会直接忽略这个选项。所有 helper 都会内联到使用它们的 chunk 中。

### 7.2.24 output.experimentalMinChunkSize：合并小 chunk 的阈值

当一个 chunk 小于指定的字节数时，Rollup 会尝试把它合并到其他 chunk 中，以减少 HTTP 请求数：

```javascript
export default {
  output: {
    experimentalMinChunkSize: 5000  // 小于 5KB 的 chunk 尝试合并
  }
};
```

### 7.2.25 output.pure：自动为函数调用添加 `/*#__PURE__*/` 注释

`/*#__PURE__*/` 注释告诉 Rollup：这个函数调用没有副作用，可以放心删除（如果结果没被用到的话）：

```javascript
export default {
  output: {
    // 自动给 console.log、console.info 等调用加上 /*#__PURE__*/
    pure: ['console.log', 'console.info']
    // 注意：要写完整路径，如 console.log 而不是只写 console
  }
};
```

打包后的代码：

```javascript
/*#__PURE__*/ console.log('这条日志可以被删除吗？');
// 如果这个 console.log 的返回值没有被使用，且 dead code elimination 生效，它就可能被删除
```

> 📝 **为什么需要这个？** Tree-Shaking 只能删除"整个调用都没用"的代码，但 `console.log(...)` 这种语句本身（不管返回值是什么）Rollup 不好判断有没有副作用。加上 `/*#__PURE__*/` 就等于告诉 Rollup："放心删，这个真的没副作用！"

---

## 7.3 路径解析配置（Paths & Resolve）

### 7.3.1 output.paths：CDN 路径映射（如 react: 'https://cdn.example.com/react.js'）

`output.paths` 允许你为某些模块指定远程 URL，这样打包产物中会生成对应的 URL 引用，而不是打包进去：

```javascript
export default {
  input: 'src/main.js',
  external: ['react'],
  output: {
    format: 'iife',
    paths: {
      // react 这个 external 模块不打包，改为 CDN 引用
      react: 'https://unpkg.com/react@18/umd/react.production.min.js'
    }
  }
};
```

生成的 IIFE 代码中不会包含 react 的代码，而是从 CDN 加载：

```javascript
// 生成的代码（简化版）
(function() {
  'use strict';
  // react 不在这里，它从 CDN 加载
  var MyLibrary = factory(window.React);
  root.MyLibrary = MyLibrary;
}());
```

> 🔥 **注意**：生成的代码不会自己写 CDN 加载逻辑，你需要先在 HTML 中通过 `<script>` 标签加载 react，或者配合 `intro` 注入 import 语句。
>
> 💡 **异步 chunk 的 CDN 映射**：`output.paths` 同样支持动态导入的模块！当你在代码中使用 `import('react')` 时，如果配置了 `paths: { react: 'https://...' }`，Rollup 会生成 `import('https://...')` 而不是打包 react 到产物中。

### 7.3.2 @rollup/plugin-node-resolve 的配置项（root / extensions / preferBuiltins / browser）

```javascript
import resolve from '@rollup/plugin-node-resolve';

export default {
  plugins: [
    resolve({
      // 从哪个目录开始解析（默认是当前工作目录）
      root: '.',

      // 尝试的模块扩展名（按顺序）
      extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],

      // 是否把 Node.js 内置模块（fs、path 等）解析为内置模块
      // false：把它们当作普通的 npm 包处理
      preferBuiltins: true,  // 默认 true

      // 是否使用 browser 字段解析（用于打包前端库）
      // true 时会用 package.json 的 browser 字段替换 main 字段
      browser: false
    })
  ]
};
```

> ⚠️ **browser vs preferBuiltins**：如果你在打包前端库，`preferBuiltins: false` + `browser: true` 是常见的组合，这样 Rollup 会用 browser 字段解析模块（跳过 Node.js 内置模块的处理）。

### 7.3.3 plugins.resolveId：自定义模块解析逻辑

`resolveId` 是插件的核心钩子之一，它决定了"从哪里找这个模块"。你可以写一个自定义插件来拦截模块解析过程：

```javascript
// 自定义路径解析插件
function myAliasPlugin() {
  return {
    name: 'my-alias-plugin',
    resolveId(source, importer) {
      // 如果遇到 @utils，直接解析到 src/utils/index.js
      if (source === '@utils') {
        return { id: './src/utils/index.js', moduleSideEffects: false };
      }

      // 其他模块让 Rollup 自己处理
      return null;
    }
  };
}
```

### 7.3.4 别名配置（alias）的实现方式

别名通常用 `@rollup/plugin-alias` 来实现，它实际上就是在 `resolveId` 钩子中做了路径替换：

```javascript
import alias from '@rollup/plugin-alias';

export default {
  plugins: [
    alias({
      entries: [
        { find: '@', replacement: 'src' },
        { find: '~', replacement: '' }  // 替换波浪号为相对路径
      ]
    })
  ]
};
```

---

## 7.4 Tree-Shaking 配置

### 7.4.1 treeshake：是否启用 Tree-Shaking（true / false）

```javascript
export default {
  treeshake: true   // 启用 Tree-Shaking（默认）
  // treeshake: false  // 禁用 Tree-Shaking（用于调试）
};
```

### 7.4.2 treeshake.moduleSideEffects：模块副作用控制（false / 'no-external' / 'all'）

```javascript
export default {
  treeshake: {
    moduleSideEffects: false
    // 可选值：
    // false        - 声明所有模块都没有副作用，Tree-Shaking 最激进（大胆放心删）
    // 'all'        - 所有模块都可能有副作用（默认，保守策略，怕删了出问题）
    // 'no-external' - 仅非外部依赖（npm 包之外）的模块假设无副作用
  }
};
```

> 🎯 **实战建议**：如果你用到了 CSS-in-JS 库（如 styled-components），它会在运行时生成样式，这种"看不见的副作用"需要 `moduleSideEffects: true`；如果你的 CSS 都是独立的 CSS 文件（或者用了 `?inline` 查询参数），可以放心设为 `false`。

### 7.4.3 treeshake.propertyReadSideEffects：只读属性访问是否视为有副作用

```javascript
export default {
  treeshake: {
    // true：读取对象属性（如 obj.prop）可能触发 getter，被视为有副作用（保守策略）
    // false（Rollup 4.x 默认）：只读属性访问没有副作用，可以放心大胆地删除
    propertyReadSideEffects: false
  }
};
```

```javascript
// 当 propertyReadSideEffects: false 时
const obj = { prop: 123 };
obj.prop;  // 只读属性访问，被视为无副作用（Rollup 可以放心删除这行）
```

> 🤔 **什么情况下属性访问有副作用？** 比如某些全局配置对象会在首次访问时触发初始化，或者对象有自定义 getter 会在读取时产生副作用（访问数据库、发请求等）。如果你确定你的代码没有这种"骚操作"，放心大胆设为 `false`！

> ⚠️ **容易混淆的点**：`propertyReadSideEffects: false` 解决的是"读取对象属性有没有副作用"的问题，而 `console.log` 这种**函数调用**会不会被删除，取决于 Rollup 的 `output.pure` 配置（上面 7.2.24 讲过）。简单记：属性读取看 `propertyReadSideEffects`，函数调用看 `output.pure`。两者各管各的，别搞混了！

### 7.4.4 treeshake.annotations：是否尊重 pure 注解（/*#__PURE__*/）

```javascript
export default {
  treeshake: {
    // true（默认）：Rollup 会识别并尊重 /*#__PURE__*/ 注解，配合 output.pure 使用
    // false：忽略这些注解，相当于 tree-shaking 变弱
    annotations: true
  }
};
```

> 💡 **为什么要单独一个选项？** 因为有时候第三方库的代码可能带有很多 `/*#__PURE__*/` 注解，但你不一定信任它们（万一有副作用呢？）。关闭这个选项，Rollup 会更保守地保留代码。默认保持 `true` 就行。

### 7.4.5 treeshake.tryCatchDeoptimization：是否优化 try-catch

```javascript
export default {
  treeshake: {
    // true（默认）：Rollup 会对 try-catch 做特殊处理，保守地保留
    // false：更激进地优化 try-catch 中的代码
    tryCatchDeoptimization: true
  }
};
```

> 🤔 **为什么 try-catch 需要特殊照顾？** 因为 try-catch 中的代码执行时机不确定（可能抛出异常），Rollup 默认不敢优化它。如果你确定 catch 块不会影响主流程（比如只是记录错误），可以设为 `false` 来获得更好的 Tree-Shaking 效果。

### 7.4.6 treeshake.unknownGlobalSideEffects：未知全局变量的副作用控制

```javascript
export default {
  treeshake: {
    // true（默认）：访问未知的全局变量被视为有副作用（Rollup 小心翼翼，保留这行代码）
    // false：访问未知全局变量被视为无副作用（Rollup 大胆删除，但可能误删重要代码）
    unknownGlobalSideEffects: false
  }
};
```

```javascript
// 当 unknownGlobalSideEffects: false 时
console.log(unknownGlobalVar);  // unknownGlobalVar 的访问被忽略，但 console.log 调用本身还是有副作用的
```

> ⚠️ **风险提示**：设为 `false` 可能导致 Rollup 删掉一些看起来"没用"但实际上很重要的代码（比如访问全局配置对象）。除非你确定你的代码不依赖任何隐式的全局变量，否则建议保持默认的 `true`。

### 7.4.7 treeshake.templateObjects：模板字面量是否有副作用（true / false）

```javascript
export default {
  treeshake: {
    // true（默认）：模板字面量（如 `hello ${world}`）被认为可能有副作用
    // false：模板字面量没有副作用，可以放心优化
    templateObjects: false
  }
};
```

> 🤔 **什么情况下模板字面量有副作用？** 在 ES2016 之前，`String.prototype.toUpperCase()` 等可能会被修改，导致模板字面量求值产生副作用。不过这种情况极其罕见，现代代码放心设为 `false` 就行！

## 7.5 构建行为控制

### 7.5.1 watch：监听模式配置（clearScreen / include / exclude）

```javascript
export default {
  input: 'src/main.js',
  watch: {
    clearScreen: false,      // 重新构建时不清屏
    include: 'src/**',      // 只监听 src 目录
    exclude: 'node_modules/**'  // 忽略 node_modules
  }
};
```

### 7.5.2 context：顶层 this 的默认指向（默认 undefined）

在 ES Module 中，顶层 `this` 就是 `undefined`。但如果你需要兼容老代码，可以改变这个行为：

```javascript
export default {
  context: 'window'  // 把顶层 this 指向 window（相当于在每个模块顶部加了 "use strict";）
};
```

### 7.5.3 moduleContext：按模块覆盖 context

```javascript
export default {
  moduleContext: {
    // 指定模块的 context
    'src/legacy.js': 'window',   // 这个文件的顶层 this 指向 window
    'src/node.js': 'global'      // 这个文件的顶层 this 指向 Node.js 的 global
  }
};
```

### 7.5.4 makeAbsoluteExternalsRelative：是否将 external 路径转为相对路径

```javascript
export default {
  external: ['lodash'],
  output: {
    // true（默认）：external 模块路径转换为相对路径（如 ./lodash 或 ../lodash）
    // false：external 模块路径保持绝对路径（如 node_modules/lodash）
    makeAbsoluteExternalsRelative: false
  }
};
```

> ⚠️ 这个选项在 Rollup 4.x 中的默认值为 `true`（之前的版本是 `false`）。如果你在升级 Rollup 后发现行为变了，别慌，这很正常！
>
> 💡 **为什么会有这个选项？** 当 `external` 配置用了绝对路径（如 `/Users/name/project/node_modules/lodash/index.js`）时，这个选项决定产物里是保留绝对路径还是转成相对路径。相对路径更利于项目迁移，绝对路径在某些场景下更稳定（比如符号链接环境）。

### 7.5.5 compiletime：测量并输出本次构建耗时（⚠️ 实验性功能，API 不稳定）

```javascript
export default {
  input: 'src/main.js',
  // 开启构建耗时测量
  compiletime: true
};
```

执行打包后会输出类似：

```
Build performance:
  parse: 12ms
  resolve: 45ms
  transform: 234ms
  generate: 67ms
  total: 358ms
```

---

## 7.6 日志与警告

### 7.6.1 logLevel：日志级别（'warn' / 'info' / 'debug'）

```javascript
export default {
  logLevel: 'warn'
  // 'warn'   - 只显示警告（默认）
  // 'info'   - 显示警告和信息
  // 'debug'  - 显示详细调试信息
};
```

### 7.6.2 onwarn：自定义警告处理函数（可压制特定警告）

`onwarn` 钩子允许你拦截警告，甚至可以选择性地忽略某些警告：

```javascript
export default {
  onwarn(warning, warn) {
    // 忽略 "Circular dependency" 警告
    if (warning.code === 'CIRCULAR_DEPENDENCY') return;

    // 忽略特定模块的警告
    if (warning.message.includes('node_modules/lodash')) return;

    // 其他警告用默认方式处理
    warn(warning);
  }
};
```

### 7.6.3 onerror：自定义错误处理函数

```javascript
export default {
  onerror(error, handler) {
    // 自定义错误处理
    console.error('打包出错啦！', error.message);
    // 或者不调用 handler，自己处理错误（不会抛出异常）
  }
};
```

---

## 7.7 插件配置（Plugins）

### 7.7.1 plugins 数组：插件注册顺序（影响执行时机）

插件的执行顺序很重要，一般遵循以下原则：

1. **alias / resolve**：先解析路径（路径不对，后面都白搭）
2. **commonjs**：再转换 CJS（CJS 转 ESM 后才能被其他插件处理）
3. **typescript / babel**：转换代码（TS/JSX → 标准 JS）
4. **其他处理插件**（如 vue、svelte 处理 SFC）
5. **压缩 / 混淆**：最后压缩（压缩完就别动代码了）

> ⚠️ **一个经典坑**：如果你把 `terser()` 放在 `babel()` 前面，babel 生成的代码会被 terser 再次处理，可能导致一些 babel 的优化失效。正确的顺序是先生成目标代码，再压缩。

```javascript
export default {
  plugins: [
    // 第 1 步：别名（先处理路径，别名可能改变路径）
    alias({ entries: [...] }),

    // 第 2 步：node_resolve（解析到具体文件路径）
    resolve({
      extensions: ['.js', '.ts']
    }),

    // 第 3 步：commonjs（把 CJS 转成 ESM）
    commonjs(),

    // 第 4 步：typescript（转译 TS 代码）
    typescript(),

    // 第 5 步：terser（最后压缩）
    terser()
  ]
};
```

### 7.7.2 插件的执行阶段（Build 阶段 vs Output 阶段）

Rollup 的插件钩子分为两类：

> **Build 阶段钩子**（在打包过程中执行，每个模块都会触发）：`buildStart` → `resolveId` → `load` → `transform` → `moduleParsed` → `buildEnd`

> **Output 生成阶段钩子**（在生成最终文件时执行）：`renderStart` → `renderChunk` → `generateBundle` → `writeBundle` → `closeBundle`

> 💡 **小贴士**：如果你在 Watch 模式下，每次重新构建都会重新触发 build 阶段的钩子，但 `closeBundle` 只会在整个 watch 进程结束时调用（负责清理资源，比如关闭文件句柄、数据库连接等）。

```javascript
function myPlugin() {
  return {
    name: 'my-plugin',

    // Build 阶段
    buildStart() {
      console.log('开始构建！');
    },

    resolveId(source) {
      // 解析模块路径
      if (source === 'virtual-module') {
        return source;  // 返回模块 ID 表示这个模块由插件提供
      }
    },

    load(id) {
      // 加载模块内容
      if (id === 'virtual-module') {
        return 'export const answer = 42;';  // 返回模块内容
      }
    },

    transform(code, id) {
      // 转换代码
      if (!id.endsWith('.special')) return null;
      return { code: code.replace(/\$\{(\w+)\}/g, (_, k) => process.env[k]) };
    },

    // Output 阶段
    renderStart() {
      console.log('即将开始生成输出！');
    },

    generateBundle(options, bundle, isWrite) {
      console.log('准备写入文件！', Object.keys(bundle));
    },

    writeBundle(options, bundle) {
      console.log('文件写入完成！');
    },

    closeBundle() {
      console.log('构建结束，清理资源！');
    }
  };
}
```

### 7.7.3 插件的两种写法：同步工厂 vs 异步工厂

```javascript
// 方式 1：同步工厂（最简单，返回配置对象）
function myPlugin(options = {}) {
  // 在这里可以处理 options，返回插件对象
  return {
    name: 'my-plugin',
    resolveId(source) {
      // ...
    }
  };
}

// 方式 2：异步工厂（适合需要异步初始化的插件，比如读取文件、网络请求等）
function myAsyncPlugin(options) {
  return {
    name: 'my-async-plugin',
    async resolveId(source) {
      const resolved = await someAsyncOperation(source);
      return resolved;
    }
  };
}
```

> 🎯 **什么时候用异步工厂？** 比如你需要在插件初始化时读取配置文件、连接数据库、或者做一些网络请求来获取配置。同步工厂做不到这些，就得用异步工厂。
>
> ⚠️ **一个坑**：异步工厂返回的插件对象本身是同步的，只是初始化过程是异步的。Rollup 会在构建开始前等待你的异步初始化完成。

### 7.7.4 常用官方插件详解

#### @rollup/plugin-node-resolve（解析 node_modules）

告诉 Rollup 如何找到 `node_modules` 中的模块：

```javascript
import resolve from '@rollup/plugin-node-resolve';

export default {
  plugins: [
    resolve({
      // 从哪里开始找模块
      root: '.',
      // 尝试的扩展名（按顺序）
      extensions: ['.js', '.jsx', '.ts', '.tsx'],
      // 是否优先使用 Node.js 内置模块
      preferBuiltins: true
    })
  ]
};
```

#### @rollup/plugin-commonjs（CJS 转 ESM）

把 CommonJS 模块转成 ES Module：

```javascript
import commonjs from '@rollup/plugin-commonjs';

export default {
  plugins: [
    commonjs({
      // 要排除转换的模块
      exclude: ['node_modules/lodash/**'],
      // 忽略 CJS 中的全局变量引用（如 global、process、undefined）
      ignoreGlobal: true,
      // 支持混用 ESM 和 CJS 的模块（开启后 Rollup 能更好地处理 default 导入）
      transformMixedEsModules: true
    })
  ]
};
```

#### @rollup/plugin-terser（代码压缩 / 混淆）

生产环境必须用，用于压缩代码、混淆变量名、删除注释：

```javascript
import terser from '@rollup/plugin-terser';

export default {
  plugins: [
    terser({
      compress: {
        drop_console: true,     // 删除所有 console 调用（包括 console.log、console.error 等）
        pure_funcs: ['console.log', 'console.info'],  // 标记这些函数无副作用，配合 Tree-Shaking 删除未使用的调用
        passes: 2              // 多次压缩（更彻底）
      },
      mangle: {
        toplevel: true          // 压缩顶层变量名
      },
      format: {
        comments: false         // 删除所有注释
      }
    })
  ]
};
```

#### @rollup/plugin-babel（ES Next 转译，JSX / TS 支持）

```javascript
import babel from '@rollup/plugin-babel';

export default {
  plugins: [
    babel({
      // Babel helper 函数打包方式
      // 'runtime'（推荐）：helper 函数抽成独立模块，按需导入（产物更干净，避免重复）
      // 'bundled'：所有 helper 内联到每个用到它们的文件中（产物稍大，但完全自包含）
      babelHelpers: 'runtime',
      // 排除 node_modules
      exclude: 'node_modules/**',
      // Babel parser 选项（用于解析非标准语法或特殊语法特性）
      parserOpts: {
        plugins: ['decorators-legacy', 'classProperties']
      }
    })
  ]
};
```

> 💡 **为什么推荐 `runtime` 而不是 `bundled`？** 假设 10 个文件都用到了装饰器语法，`bundled` 模式会在每个文件里都塞一份 `_classCallCheck` 之类的 helper；`runtime` 模式则只生成一个 `helpers/runtime.js`，所有文件都从那里 import。产物更小，缓存更友好！

#### @rollup/plugin-typescript（TypeScript 类型检查与编译）

```javascript
import typescript from '@rollup/plugin-typescript';

export default {
  plugins: [
    typescript({
      // tsconfig.json 路径（默认查找项目根目录）
      tsconfig: './tsconfig.json',
      // 输出类型声明文件
      declaration: true,
      declarationDir: 'dist/types',
      // 是否输出 .map 文件
      sourceMap: true
    })
  ]
};
```

#### @rollup/plugin-json（JSON 直接 import 支持）

```javascript
import json from '@rollup/plugin-json';

export default {
  plugins: [
    json()  // 开启后就可以 import JSON 文件了
  ]
};
```

```javascript
// 这样用
import pkg from './package.json';
console.log(pkg.name);    // 'my-library'
```

#### @rollup/plugin-alias（路径别名）

```javascript
import alias from '@rollup/plugin-alias';

export default {
  plugins: [
    alias({
      entries: [
        { find: '@', replacement: 'src' },
        { find: 'react-dom', replacement: 'react-dom/profiling' }
      ]
    })
  ]
};
```

#### @rollup/plugin-replace（环境变量替换）

```javascript
import replace from '@rollup/plugin-replace';

export default {
  plugins: [
    replace({
      preventAssignment: true,  // 防止对未匹配的变量进行替换
      // 替换值
      __DEBUG__: JSON.stringify(false),
      // 条件替换
      'process.env.NODE_ENV': JSON.stringify('production')
    })
  ]
};
```

```javascript
// 源代码
if (__DEBUG__) {
  console.log('调试信息');
}
```

打包后（`__DEBUG__` 被替换成 `false`）：

```javascript
if (false) {
  console.log('调试信息');  // 整块代码被 terser 的死代码消除（Dead Code Elimination）删除，不是 Rollup Tree-Shaking 的功劳
}
```

#### rollup-plugin-postcss（CSS 处理 + PostCSS 生态）

```javascript
import postcss from 'rollup-plugin-postcss';

export default {
  plugins: [
    postcss({
      extract: 'styles.css',   // 提取成独立 CSS 文件
      minimize: true,           // 压缩 CSS
      sourceMap: true,         // Source Map
      use: [
        ['sass', { includePaths: ['node_modules'] }]  // SCSS 支持
      ]
    })
  ]
};
```

> 🔥 **注意**：`rollup-plugin-postcss` 是**社区插件**（非 Rollup 官方），需要单独安装：`npm install rollup-plugin-postcss -D`

#### @rollup/plugin-image（图片/字体等二进制资源导入）

```javascript
import image from '@rollup/plugin-image';

export default {
  plugins: [
    image()  // 开启后 import 图片会返回 Data URL
  ]
};
```

```javascript
import logo from './logo.png';

const img = new Image();
img.src = logo;  // logo 此时是一个 Data URL 字符串
console.log(img.src); // data:image/png;base64,.....
// 不需要担心单独 import 图片文件的问题，插件会自动处理
```

#### @rollup/plugin-url（资源转为 Data URL 或复制到输出目录）

```javascript
import url from '@rollup/plugin-url';

export default {
  plugins: [
    url({
      // 小于 limit 字节的资源转为 Data URL，大于的复制到 dist/assets/
      limit: 8 * 1024,
      // 资源文件的目标目录（相对于 output.dir）
      destDir: 'dist/assets',
      // 文件命名规则
      fileName: '[name]-[hash][extname]'
    })
  ]
};
```

#### @rollup/plugin-wasm（WebAssembly 模块支持）

```javascript
import wasm from '@rollup/plugin-wasm';

export default {
  plugins: [
    wasm({
      // 允许同步加载指定的 .wasm 文件
      sync: ['assets/*.wasm']
    })
  ]
};
```

### 7.7.5 常用社区插件

#### @vitejs/plugin-vue（Vue SFC 打包，配合 Vite 使用）

```javascript
import vue from '@vitejs/plugin-vue';

export default {
  plugins: [
    vue({
      // 是否提取 CSS 到独立文件
      css: true,
      // 自定义 Vue 编译器选项
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('ion-')
        }
      }
    })
  ]
};
```

#### rollup-plugin-visualizer（产物分析可视化，社区插件）

打包完成后，用浏览器打开一个可视化图表，查看每个模块的大小占比：

```javascript
import visualizer from 'rollup-plugin-visualizer';

export default {
  plugins: [
    // ... 其他插件
    visualizer({
      filename: 'stats.html',  // 生成的 HTML 分析报告
      open: true,              // 自动在浏览器中打开
      gzipSize: true           // 显示 gzip 后的体积
    })
  ]
};
```

---

## 本章小结

这一章我们完整梳理了 Rollup 的所有重要配置：

1. **输入配置（Input）**：`input`（入口）、`external`（外部依赖）、`cache`（构建缓存）、`preserveSymlinks`（符号链接）。

2. **输出配置（Output）**：25 个配置项（7.2.1 ~ 7.2.25），涵盖文件名、格式、全局变量、Source Map、代码注入、chunk 命名规则、`__esModule` 标记等方方面面。特别是 **`manualChunks`**（代码分割的核心配置），建议重点掌握！

3. **路径解析配置**：CDN 路径映射（`output.paths`）、node-resolve 配置、自定义 `resolveId` 钩子、别名配置。

4. **Tree-Shaking 配置**：`moduleSideEffects`、`propertyReadSideEffects`、`annotations`、`tryCatchDeoptimization`、`unknownGlobalSideEffects`、`templateObjects` 六个细粒度控制选项（Rollup 的 Tree-Shaking 比你想的精细得多！）。

5. **构建行为控制**：watch 监听配置、`context` 顶层 this、`moduleContext` 按模块覆盖、`makeAbsoluteExternalsRelative`、`compiletime` 耗时测量。

6. **日志与警告**：`logLevel`、`onwarn` 自定义警告处理、`onerror` 自定义错误处理。

7. **插件配置（Plugins）**：插件顺序原则、两阶段执行机制（build / generateBundle / closeBundle）、两种写法（同步工厂 / 异步工厂）、12 个常用插件详解（其中 11 个官方 + 1 个社区）+ 2 个常用社区插件补充。

Rollup 的配置看似繁杂，但核心逻辑非常清晰：**输入 → 处理（插件）→ 输出**。理解了这条主线，所有配置项的位置和作用就都一目了然了。