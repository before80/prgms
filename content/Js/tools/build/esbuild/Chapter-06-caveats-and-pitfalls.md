

+++
title = "第6章 注意事项与陷阱"
weight = 60
date = "2026-03-28T11:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

## 6.1 已知局限性

esbuild 很快，但这不意味着它什么都能干。在决定用 esbuild 之前，你需要了解它的局限性。

### 6.1.1 无内置 HMR（热模块替换），依赖上层工具实现

**HMR**（Hot Module Replacement，热模块替换）是前端开发中的"神器"——当你的代码发生变化时，不需要刷新整个页面，就能把变化的部分替换进去，页面的其他状态（比如输入框里的内容、滚动位置、API 请求的状态）都能保持不变。

esbuild **没有内置 HMR**。这不是 bug，是设计选择——HMR 需要和具体的框架（React、Vue、Svelte）深度集成，不同框架有不同的 HMR API，esbuild 作为底层打包工具，不应该承担这个职责。

**如果你的项目需要 HMR，有两个选择：**

第一个是使用 Vite。Vite 在 esbuild 基础上实现了完整的 HMR 协议，是目前最好用的带 HMR 的开发服务器。

第二个是自己实现。你可以用 `ctx.watch()` 监听文件变化，然后用浏览器的 HMR API 自己实现模块热替换。这个方案比较复杂，一般不推荐。

### 6.1.2 代码分割（Code Splitting）有条件限制（仅支持 esm + import.meta.url 场景）

代码分割（Code Splitting）是指把打包产物拆成多个文件，浏览器按需加载，而不是一次性下载整个 bundle。

esbuild **支持代码分割**，但有条件限制：

```javascript
// 开启代码分割（必须在 format=esm 且 platform=浏览器场景下）
await esbuild.build({
  entryPoints: ['src/index.js'],
  outdir: 'dist',
  bundle: true,
  format: 'esm',
  splitting: true,
  // 只能用 import.meta.url，不能用 __dirname
  platform: 'browser',
});
```

```javascript
// src/index.js
import('./moduleA.js'); // 动态导入，esbuild 会把它分割成单独的文件
```

**为什么限制这么多？**

因为 esbuild 的代码分割依赖于 ESM 的动态 `import()` 语法和浏览器原生的 `import.meta.url` 机制。如果你用 CommonJS 或者 Node.js 环境，这些机制都不存在，代码分割就无法工作。

所以：如果你的项目需要复杂的代码分割策略（比如根据路由分割、根据 vendors 分割），esbuild 可能不够用，建议用 Rollup。

### 6.1.3 插件生态不如 Webpack / Rollup 丰富

Webpack 有上万个插件，Rollup 的插件生态也很成熟。相比之下，esbuild 的插件数量还比较少——毕竟出道时间短，能理解。

这意味着：有些你用 Webpack 插件能做到的事情，在 esbuild 里可能找不到对应的插件，得自己造轮子。

不过好消息是，esbuild 的插件 API 设计得比较简洁，写起来不算太难。

### 6.1.4 部分高级 TypeScript 特性支持有限（仅做转译，不做类型检查）

这是 esbuild 一个很重要的特性：**它只转译 TypeScript，不做类型检查**。

```typescript
// app.ts
interface User {
  name: string;
  age: number;
}

function greet(user: User) {
  return `Hello, ${user.name}`;
}

const user: User = { name: '小明', age: '25' }; // 类型错误：age 应该是 number，这里给了 string
console.log(greet(user));
```

esbuild 会**直接无视这个类型错误**，一声不吭地打包成功——因为它只负责把 TypeScript 转成 JavaScript，类型对不对它才不管呢（又不是它的活儿）。

这既是优点也是缺点：

- **优点**：速度快，因为不需要做类型分析
- **缺点**：你可能会带着类型错误上线，运行时才发现问题

**最佳实践**：在开发流程里，用 `tsc --noEmit` 做类型检查，用 esbuild 做构建——两者各司其职。

### 6.1.5 不支持自定义模块解析逻辑

Webpack 允许你完全自定义模块解析逻辑——比如自定义路径别名规则、自定义模块查找顺序、甚至完全重写模块解析算法。

esbuild **不支持这种程度的自定义**。它的模块解析规则是固定的，只能通过 `alias`、`external`、`resolveExtensions` 这些配置项做有限调整。

如果你需要完全自定义模块解析逻辑（比如实现自己的 npm 包解析策略），esbuild 可能不满足需求。——这种情况极少，大多数项目用到的那点别名和 external 配置完全够用，别没事给自己加戏。

---

## 6.2 常见错误与解决方案

### 6.2.1 "Could not resolve" 依赖解析错误

这是 esbuild 最常见的错误之一：

```
[ERROR] Could not resolve "lodash" from "src/index.js"
```

**原因**：你 `import` 了一个模块，但 esbuild 在 `node_modules` 里找不到它。

**排查步骤**：

1. 确认这个包已经安装：`ls node_modules | grep lodash`
2. 确认 `node_modules` 目录存在
3. 如果包名写错了（比如大小写），修正它
4. 如果你确定这个包不存在，安装它：`npm install lodash`

```bash
# 常见场景：你 import 了一个还没装的包
import _ from 'lodash'; // esbuild 找不到，报错

# 解决方案：先安装
npm install lodash
```

### 6.2.2 TypeScript 类型错误被忽略（esbuild 不做类型检查）

```bash
# 你满怀信心地运行 esbuild
$ npx esbuild src/app.ts --bundle --outfile=dist/app.js

# 构建成功，零报错，零警告
# 但你的 TypeScript 代码里有严重的类型错误……
```

这是**正常的，不是 bug**。esbuild 有意忽略 TypeScript 类型错误——它就是个翻译官，只负责把 TypeScript 翻成 JavaScript，至于你写的类型对不对，它才不关心呢（又不是它写的）。

**解决方案**：单独运行 TypeScript 编译器来检查类型错误：

```bash
# 在项目里安装 typescript
npm install --save-dev typescript

# 运行类型检查（不生成任何文件，只检查错误）
npx tsc --noEmit

# 如果有类型错误，会显示：
# error TS2322: Type 'string' is not assignable to type 'number'.
```

建议在 CI/CD 流水线里加入 `tsc --noEmit` 步骤，确保代码类型安全。

### 6.2.3 CSS 被打包进 JS 文件

有时候你会发现，构建出来的 JS 文件里包含了 CSS 代码，或者你的 CSS 根本没有生成单独的文件。

```javascript
// index.js
import './styles.css';
console.log('Hello');
```

```bash
# 打包后，你期望得到 index.js 和 styles.css
# 但你只得到了 index.js，里面包含了 CSS 代码
```

**原因**：你没有配置正确的 CSS 加载器，或者 CSS 文件的加载器配置不正确。

**解决方案**：确保配置了 CSS loader：

```javascript
// esbuild.config.js
await esbuild.build({
  entryPoints: ['src/index.js'],
  outdir: 'dist',
  bundle: true,
  loader: {
    '.css': 'css',  // 关键：告诉 esbuild 如何处理 .css 文件
  },
});
```

如果你用的是 CSS Modules（一种 CSS 写法，让类名全局唯一），esbuild **没有内置** `css-modules` 加载器，需要借助插件：

```javascript
// 需要安装 esbuild-plugin-css-modules 或类似插件
import cssModulesPlugin from 'esbuild-plugin-css-modules';

await esbuild.build({
  entryPoints: ['src/index.js'],
  outdir: 'dist',
  bundle: true,
  plugins: [cssModulesPlugin()],
});
```

### 6.2.4 生产环境构建产物异常

有时候开发环境跑得好好的，但一打包到生产环境就出问题——代码报错、功能失效。

**常见原因和排查方法：**

1. **压缩把特殊代码炸了**：esbuild 压缩时会把 `with` 语句、`eval` 里的一些代码逻辑误判并删除，导致运行时行为异常（说白了：少侠慎用 `with` 和 `eval`，压缩它们纯属自找麻烦）。
   - 解决：给可疑的函数调用加 `/* @__PURE__ */` 注解，告诉压缩器"这个调用没副作用，别动它"

```javascript
// 压缩前
/* @__PURE__ */ getBuildVersion(); // 无副作用的函数调用，esbuild 会保留

// 或者标记一个工厂函数（它自己无副作用，但返回值可能有副作用）
/* @__PURE__ */ (() => createWidget())();
```

2. **环境变量问题**：`process.env.NODE_ENV` 在生产构建时变成了 `'production'`，有些库会根据这个值做不同的行为
   - 解决：用 `define` 配置替换环境变量

3. **路径问题**：生产环境路径和开发环境不一致
   - 解决：检查 `outdir`、`outbase` 配置

### 6.2.5 watch 模式不生效

有时候 `watch` 模式启动后，修改文件没有触发重新构建：

```bash
$ esbuild src/index.js --bundle --watch --outfile=dist/index.js

[watch] build finished, watching for changes...

# 修改了 src/index.js
# 没有输出……没有重新构建……
```

**可能的原因：**

1. **修改了错误的文件**：esbuild 只监听被 entryPoints 直接或间接引用的文件。如果你改了一个完全独立、不被引用的文件，esbuild 不会管它。

2. **文件系统问题**：某些网络文件系统（NFS、Docker 挂载卷）可能不支持文件监听。

3. **入口点配置有问题**：比如你写的是 `--outfile=dist/index.js`，但 entryPoints 路径配置不匹配实际文件结构。

**解决方案**：确认修改的文件确实被依赖图引用，然后重启 watch 模式。

### 6.2.6 路径别名不生效

你想用 `@/` 代替 `src/`，但配置了不生效：

```javascript
// index.js
import utils from '@/utils'; // 你期望这个 "@/" 指向 "src/utils"
```

```javascript
// esbuild.config.js
await esbuild.build({
  entryPoints: ['src/index.js'],
  outdir: 'dist',
  alias: {
    '@': 'src',  // 别名配置
  },
});
```

**检查以下几项：**

1. `alias` 配置的路径是否正确（是绝对路径还是相对路径）
2. 别名有没有被插件覆盖（有些插件会重置 esbuild 的配置）
3. 确认配置是在构建选项里，而不是在错误的地方

### 6.2.7 format 与 platform 组合不匹配

```javascript
// 你写了这样的配置
await esbuild.build({
  entryPoints: ['src/index.js'],
  outdir: 'dist',
  platform: 'node',    // 平台是 Node.js
  format: 'iife',      // 但格式是 IIFE（浏览器格式）
});
```

**原因**：指定的 format 和 platform 组合在语义上不兼容。例如 `iife` 格式是给浏览器用的，它的代码会被包在一个立即执行函数里，而 `node` 平台假设代码跑在 Node.js 环境。如果两者的语义矛盾，esbuild 会给出类似"不兼容"的错误提示。

**解决方案**：确保 platform 和 format 组合合理：

| platform | 推荐的 format |
|---------|-------------|
| browser | esm / iife |
| node | cjs / esm |
| neutral | esm / cjs |

### 6.2.8 splitting 模式报错（未使用 esm 格式）

```javascript
// 你配置了代码分割
await esbuild.build({
  entryPoints: ['src/index.js'],
  outdir: 'dist',
  bundle: true,
  splitting: true,  // 开启代码分割
  format: 'cjs',    // 但用的是 CommonJS 格式 —— 这是不支持的
});
```

```bash
X [ERROR] Splitting currently only works with the "esm" format
```

**原因**：esbuild 的代码分割依赖 ESM 的动态 `import()` 语法，CommonJS 的 `require()` 根本不支持动态加载，所以代码分割和 CommonJS 水火不容。

**解决方案**：把 `format` 改成 `esm`：

```javascript
format: 'esm',
```

---

## 6.3 开发环境与生产环境的差异

### 6.3.1 开发构建关注速度

开发环境的构建目标是：**快**。

页面加载慢 0.1 秒你可能感知不到，但如果改一行代码要等 10 秒才能看到效果，你会崩溃。所以开发构建的一切配置都围绕"快"字：

```javascript
const config = {
  minify: false,        // 不压缩，构建更快
  sourcemap: true,       // 要 sourcemap，方便调试
  target: 'es2015',     // 目标宽泛一些，减少转译工作
  treeShaking: false,   // 开发时关掉 Tree Shaking，减少分析时间
};
```

### 6.3.2 生产构建关注体积、安全性与性能

生产环境的构建目标是：**小**、**快**（网络加载快）。

```javascript
const config = {
  minify: true,                        // 压缩代码，减小体积
  sourcemap: process.env.SENTRY_DSN ? true : false,  // 如果接入了错误追踪就开启，否则关闭
  target: ['chrome80', 'firefox80'],    // 目标更精确，可以生成更小的代码
  treeShaking: true,                   // 必须开 Tree Shaking，删无用代码
  legalComments: 'none',               // 删除法律注释，进一步减小体积
};
```

### 6.3.3 配置分离最佳实践

把开发和生产配置写在一起，用一个变量来区分：

```javascript
// esbuild.config.js
const esbuild = require('esbuild');

const isProduction = process.env.NODE_ENV === 'production';

async function build() {
  await esbuild.build({
    entryPoints: ['src/index.js'],
    outdir: 'dist',
    bundle: true,
    // 根据环境动态配置
    minify: isProduction,
    sourcemap: !isProduction,
    target: isProduction ? ['chrome80'] : ['es2015'],
  });
}

build();
```

```bash
# 开发构建
NODE_ENV=development node esbuild.config.js

# 生产构建
NODE_ENV=production node esbuild.config.js
```

---

## 6.4 Tree Shaking 注意事项

### 6.4.1 ESM vs CommonJS 对 Tree Shaking 的影响（ESM 更彻底）

前面章节讲过，Tree Shaking 依赖 ESM 的静态结构来分析哪些代码是死代码。

用 CommonJS 格式时，Tree Shaking 的效果会大打折扣——因为 `require()` 可以在任何地方调用，编译器根本猜不到你什么时候会用到什么：

```javascript
// 用 ESM —— Tree Shaking 效果拉满，编译器一眼就知道谁没用
export function used() { return 1; }
export function unused() { return 2; }
```

```javascript
// 用 CommonJS —— Tree Shaking 基本瞎了
module.exports.used = function() { return 1; };
module.exports.unused = function() { return 2; };
// ↑ 编译器：我怎么知道你以后会不会 require 这两个？
```

**建议**：如果你要做代码分割和 Tree Shaking，入口文件用 ESM 格式。什么，还在用 CommonJS？——是时候升级了，老古董。

### 6.4.2 sideEffects 配置的作用

`package.json` 的 `sideEffects` 字段告诉打包工具："除了这些文件，其他文件都没有副作用，可以安全地 Tree Shaking。"

```json
{
  "name": "my-lib",
  "sideEffects": [
    "./src/polyfills.js",
    "./src/global.css"
  ]
}
```

这样 esbuild 会认为除了 `polyfills.js` 和 `global.css` 之外，其他文件都可以安全地删除没被引用的导出。

### 6.4.3 动态导入（import()）对 Tree Shaking 的限制

ESM 的动态 `import()` 是运行时的，只有代码真正执行了才会加载对应的模块。esbuild 无法在构建时预知哪些模块会被动态加载，所以这些模块不会被 Tree Shaking 优化。

```javascript
// 这段代码里的 someModule 会被排除在 Tree Shaking 之外
// 因为 esbuild 不知道 if 条件为 true 时到底会不会执行
if (someCondition) {
  import('./someModule.js');
}
```

### 6.4.4 副作用代码（side-effect）不能被 Tree Shaking

如果一个模块的执行有"副作用"（Side Effects），比如修改了全局变量、写了 `localStorage`、发送了网络请求——即使它没有被显式调用，Tree Shaking 也不敢删掉它。

```javascript
// 这个模块有副作用：执行时会修改 window.title
window.title = 'Hello, World!';
export const name = '小明';
```

```javascript
// 即使你 import 这个模块但不使用任何导出
import './hasSideEffect.js'; // esbuild 还是会把它打包进来，因为它是"有副作用"的
```

如果你的模块确实没有副作用，可以给打包工具一个提示：

```javascript
// 标记一个函数调用是无副作用的，告诉打包工具如果没用到可以安全删除
/* @__PURE__ */ getBuildVersion();

// 或者标记一个工厂函数调用本身无副作用（返回值可能有副作用）
/* @__PURE__ */ (() => createWidget())();
```

对于整个文件都没有副作用的情况，利用 `package.json` 的 `sideEffects: false` 配置比给每个导出加 `__PURE__` 更简洁。

---

## 6.5 浏览器兼容性注意事项

### 6.5.1 target 参数的合理设置

`target` 参数决定了代码需要兼容什么环境。如果设置得太宽泛（比如 `es2020`），生成的代码会很大（因为降级少）；如果设置得太窄（比如 `es5`），代码会更安全但体积可能更大。

**建议**：根据你的实际用户群体来设置 target。用 Chrome 的用户基本都是自动更新到最新版的，可以用较新的 target；用 Safari 的 iOS 用户更新较慢，可以设置较老的 target。

```javascript
// 保守策略：支持绝大多数浏览器
target: ['chrome74', 'firefox68', 'safari12', 'edge79'];

// 激进策略：只支持现代浏览器，代码更小
target: ['chrome100', 'firefox100', 'safari15'];
```

### 6.5.2 browserslist 格式支持与写法

esbuild 支持 `browserslist` 格式——这是一种行业标准的浏览器兼容性查询语法。

在 `package.json` 里配置：

```json
{
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead"
  ]
}
```

然后在 esbuild 里直接用：

```javascript
// esbuild 会自动读取 package.json 的 browserslist 配置
await esbuild.build({
  entryPoints: ['src/index.js'],
  outfile: 'dist/index.js',
  target: 'es2020', // 或者直接不写 target，让 esbuild 自己读 browserslist
});
```

常见的 browserslist 配置：

```json
{
  "browserslist": [
    "> 0.5%",       // 市场占有率超过 0.5% 的浏览器
    "last 2 versions", // 每个浏览器的最近两个版本
    "not dead",      // 不是已经停止更新的浏览器（如 IE）
    "not IE 11"      // 明确排除 IE 11
  ]
}
```

### 6.5.3 避免过度降级导致性能损失

有些 ES 新语法虽然能用旧语法替代，但替代后的代码运行效率反而更低——你本意是兼容老浏览器，结果反而让老浏览器跑得更慢，完美诠释了什么叫"好心办坏事"。

比如 `??`（空值合并运算符）：

```javascript
// 用新语法
const value = input ?? 'default';

// 降级后变成
const value = input !== null && input !== void 0 ? input : 'default';
```

降级后的代码更长、更复杂，在老浏览器里执行也更慢。所以 `target` 设置不要太低，只在必要时才降级。

### 6.5.4 platform=browser 下的默认行为差异

当你设置 `platform: 'browser'` 时，esbuild 会做一些浏览器特有的默认处理：

- `process.env.NODE_ENV` 会被替换成 `'production'`（在 minify 时）
- `__dirname` 和 `__filename` 会用 `import.meta.url` 模拟
- Node.js 内置模块（`fs`、`path` 等）会被标记为外部依赖

如果你在浏览器代码里不小心引用了 Node.js 模块，esbuild 会报错，而不是默默忽略：

```
[ERROR] Could not resolve "fs" from "src/index.js"
```

---

## 6.6 安全性注意事项

### 6.6.1 第三方插件安全性

esbuild 的插件可以访问和修改你的构建产物，所以**来源不明的插件有安全风险**。

打个比方：你写了一个计算器插件，正准备打包发到生产环境，结果插件里偷偷加了一行向第三方服务器发送你的代码——这就是供应链攻击（Supply Chain Attack）。所以 npm 上随便搜个插件就往项目里怼之前，先想想：你愿意让这个陌生人的代码在你眼皮底下对你的构建产物做任何事吗？

**建议**：

1. 只用官方或社区公认的插件
2. 在 `package.json` 里锁定插件版本
3. 定期审计依赖：`npm audit`

### 6.6.2 敏感信息不要写入构建产物

构建产物最终会发布到生产环境，可能被任何人访问。**不要在构建时把敏感信息硬编码进去**。

```javascript
// ❌ 危险：把密钥直接写进代码
const API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxx';
```

```javascript
// ✅ 安全：通过环境变量注入
const API_KEY = process.env.API_KEY;
```

```javascript
// ❌ 危险：把环境变量直接 define 替换进代码 —— 构建产物里会暴露真实密钥！
await esbuild.build({
  entryPoints: ['src/index.js'],
  outdir: 'dist',
  define: {
    // 注意：define 的 key 必须与源码中的表达式完全匹配
    // 源码里写的是 process.env.API_KEY，所以 key 必须是 'process.env.API_KEY'
    // 如果 env var 里有真实密钥，替换后真实密钥会被直接写进 bundle，任何人都能提取！
    'process.env.API_KEY': JSON.stringify(process.env.API_KEY ?? ''),
  },
});
```

`define` 适合替换**非敏感配置**（如 `process.env.NODE_ENV`），但**绝对不要**用它来处理真实密钥——构建产物是公开的，任何人都能从中提取字符串。

```javascript
// ✅ 安全：敏感信息走运行时注入，永远不进入 bundle
const API_KEY = process.env.API_KEY; // 运行时从环境读取，bundle 里只有变量名引用
```

### 6.6.3 版本依赖安全管理

锁定 esbuild 版本，避免不同环境里版本不一致导致奇怪的问题：

```json
{
  "devDependencies": {
    "esbuild": "0.20.0"  // 锁定到精确版本，不用 ^0.20.0
  }
}
```

```bash
# 提交 lock 文件
git add package-lock.json
git commit -m "chore: lock esbuild version to 0.20.0"
```

定期更新 esbuild 到最新稳定版可以获得性能提升和 bug 修复，但更新前最好先在测试环境验证。

---

## 本章小结

本章我们系统地梳理了使用 esbuild 时需要注意的那些坑。

**已知局限性**：esbuild 没有内置 HMR、代码分割有条件限制（仅 esm）、插件生态不如 Webpack 丰富、不做 TypeScript 类型检查、不支持自定义模块解析逻辑。

**常见错误**：`Could not resolve` 说明依赖没装好、TypeScript 类型错误被忽略是 esbuild 的正常操作（别怪它，它只管翻译不管纠错）、CSS 被打包进 JS 需要配置 loader、watch 不生效可能是改错了文件、splitting 必须配合 esm 格式使用。

**开发 vs 生产**：开发环境追求速度，生产环境追求体积和安全性。合理分离配置是最佳实践。

**Tree Shaking**：ESM 格式下效果最好，CommonJS 下效果大打折扣。副作用代码（Side Effects）不能被 Tree Shaking 删掉。

**浏览器兼容性**：`target` 设置要合理，不要过度降级。善用 browserslist 格式来管理兼容性列表。

**安全注意事项**：警惕来源不明的插件、不要把密钥硬编码进代码、锁定依赖版本。

了解了这些注意事项，下一章我们将进入最核心的部分：esbuild 的所有配置项详解——这是写 esbuild 配置文件的必备参考手册。
