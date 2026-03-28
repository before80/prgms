

+++
title = "第5章 如何使用esbuild"
weight = 50
date = "2026-03-28T11:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

## 5.1 环境安装

### 5.1.1 Node.js 环境要求（版本支持说明）

在安装 esbuild 之前，你需要确保系统里已经安装了 **Node.js**。

Node.js 是一个 JavaScript 运行时，简单理解就是：它让你能在服务器端、桌面端、命令行里运行 JavaScript 代码。esbuild 的 JavaScript 版本需要 Node.js 才能运行（也有不需要 Node.js 的原生二进制版本，后面会讲）。

你可以在命令行里输入以下命令来检查是否已经安装了 Node.js：

```bash
node --version
# 打印结果：v20.11.0
```

如果显示 `command not found` 或者错误信息，说明你还没装 Node.js。

安装 Node.js 很简单，去官网 nodejs.org 下载安装包，选 **LTS（长期支持版）** 就行——这是最稳定的版本，不容易踩坑。

### 5.1.2 全局安装（`npm install -g esbuild`）

全局安装的意思是：把 esbuild 安装到系统全局，所有项目都能用。

```bash
npm install -g esbuild
```

安装完成后，你可以直接在命令行里使用 `esbuild` 命令：

```bash
esbuild --version
# 打印结果：0.24.2
```

全局安装的好处是：一次性安装，到处使用。但缺点也很明显：每个项目的 esbuild 版本可能不一致，容易出现"在我电脑上能跑，在你电脑上挂了"的坑爹情况。

所以**推荐本地安装**，而不是全局安装。

### 5.1.3 本地安装（`npm install esbuild`）

本地安装的意思是：把 esbuild 安装到当前项目目录下，只有这个项目能用。

```bash
# 先初始化一个 npm 项目（如果还没有 package.json）
npm init -y

# 本地安装 esbuild
npm install esbuild
```

本地安装完成后，esbuild 的可执行文件会在 `./node_modules/.bin/esbuild`，你可以这样调用：

```bash
# Linux / macOS
./node_modules/.bin/esbuild --version

# Windows
.\node_modules\.bin\esbuild.cmd --version
```

但每次都敲这么长的路径很麻烦，所以更好的方式是：在 `package.json` 的 `scripts` 字段里配置快捷命令。

```json
{
  "name": "my-project",
  "scripts": {
    "build": "esbuild src/index.js --bundle --outfile=dist/index.js"
  },
  "dependencies": {
    "esbuild": "^0.20.0"
  }
}
```

然后你就可以用 `npm run build` 来执行构建了。

### 5.1.4 验证安装成功（`esbuild --version`）

不管你是全局安装还是本地安装，都可以用同样的命令验证安装是否成功：

```bash
esbuild --version
# 打印结果：0.24.2  （版本号可能不同，以你安装的为准）
```

如果打印出版本号，说明安装成功；如果报 `command not found`，说明安装可能出了问题。

### 5.1.5 原生平台二进制（无需 Node.js 也能运行）

这是 esbuild 的一大特色——它提供了**原生二进制版本**，不需要 Node.js 也能运行！

这个二进制文件是 esbuild 用 Go 语言编译出来的，它是独立运行的，不依赖任何运行时环境。

安装方式：

```bash
# 安装对应平台的原生二进制（选一个你系统对应的就行）
# macOS Apple Silicon（M1/M2/M3）
npm install -g @esbuild/darwin-arm64

# macOS Intel 芯片
npm install -g @esbuild/darwin-amd64

# Linux
npm install -g @esbuild/linux-x64

# Windows
npm install -g @esbuild/win32-x64
```

安装完成后，直接敲 `esbuild` 命令即可，不需要 Node.js：

```bash
esbuild --version
# 打印结果：0.24.2
```

这个特性特别适合：不想装 Node.js 只想体验一下 esbuild 速度的尝鲜用户、或者在某些受限环境里（比如只有 Go 运行时的 Docker 容器）使用。

---

## 5.2 命令行基础用法

### 5.2.1 基本语法结构

esbuild 的命令行语法非常简洁：

```bash
esbuild [入口文件] [选项]
```

最基本的用法，就是指定一个入口文件和输出路径：

```bash
esbuild src/index.js --bundle --outfile=dist/index.js
```

这条命令的意思是：把 `src/index.js` 作为入口文件，打包（`--bundle`），输出到 `dist/index.js`。

### 5.2.2 `--bundle` 开启打包模式

`--bundle` 是 esbuild 最重要的参数之一——没有之一。

说它是 esbuild 的灵魂都不为过，因为 esbuild 之所以快，很大程度上就是因为这个 bundler 做得足够极致。

不加 `--bundle`，esbuild 就只是简单地转译那个文件，`import` 统统当作不存在——你的代码会收到来自 Node.js 的灵魂拷问：`ReferenceError: require is not defined`。

所以，**大多数情况下都要加 `--bundle`**（除非你明确知道自己不需要）。这不是过度使用，这是 esbuild 的正确打开方式。

```bash
# 不加 --bundle：只转译当前文件，不管 import
esbuild src/index.js --outfile=dist/index.js

# 加 --bundle：打包所有依赖
esbuild src/index.js --bundle --outfile=dist/index.js
```

什么时候不加 `--bundle`？只有当你只是想转译单个文件、不需要打包的时候——这种情况非常少见。

### 5.2.3 `--outfile` / `--outdir` 输出路径

```bash
# 输出到单个文件
esbuild src/index.js --bundle --outfile=dist/bundle.js

# 输出到目录（会自动推断文件名）
esbuild src/index.js --bundle --outdir=dist/
```

当你有多个入口文件时，用 `--outdir` 更方便：

```bash
# 多个入口，打包到 dist 目录
esbuild src/home.js src/about.js --bundle --outdir=dist/

# 生成文件：dist/home.js 和 dist/about.js
```

### 5.2.4 `--format` 输出格式（esm / cjs / iife）

输出格式决定了打包产物的模块化风格：

```bash
# ES Modules（现代浏览器 / 打包工具）
esbuild src/index.js --bundle --format=esm --outfile=dist/index.mjs

# CommonJS（Node.js）
esbuild src/index.js --bundle --format=cjs --outfile=dist/index.js

# IIFE（直接 <script> 引用，全局变量）
esbuild src/index.js --bundle --format=iife --outfile=dist/index.global.js
```

`esm` 输出的代码长这样：

```javascript
// format=esm 输出
import { add } from './math.js';
export { add };
```

`cjs` 输出的代码长这样：

```javascript
// format=cjs 输出
const { add } = require('./math.js');
exports.add = add;
```

`iife` 输出的代码长这样：

```javascript
// format=iife 输出
(() => {
  "use strict";
  // ... 打包后的代码 ...
})();
```

### 5.2.5 `--platform` 目标平台（browser / node / neutral）

`--platform` 告诉 esbuild 你的代码要跑在什么环境里：

```bash
# 浏览器环境
esbuild src/index.js --bundle --platform=browser --outfile=dist/index.js

# Node.js 环境
esbuild src/index.js --bundle --platform=node --outfile=dist/index.js

# 中立环境（既不是浏览器也不是 Node.js）
esbuild src/index.js --bundle --platform=neutral --outfile=dist/index.js
```

不同的平台，esbuild 会做不同的默认处理：

- `browser`：把 `process`、`Buffer` 等 Node.js 特有内容标记为外部依赖；默认 `format=iife`
- `node`：把 `fs`、`path` 等内置模块标记为外部依赖；默认 `format=cjs`
- `neutral`：不包含任何平台特定的处理

### 5.2.6 `--minify` 压缩代码

生产环境必须用 `--minify` 来压缩代码：

```bash
esbuild src/index.js --bundle --minify --outfile=dist/index.min.js
```

压缩会做以下事情：

1. 缩短变量名（`userName` → `a`，`calculateTotalPrice` → `b`——是的，丧心病狂）
2. 删除空格和换行（你的代码从"排列整齐"变成"量子态"）
3. 删除注释（你的 `// TODO: 这里以后要重构` 也会消失，且用且珍惜）
4. 缩短字符串（可选，把 `"Hello, World!"` 变成 `"Hello, World!"` 的是语法优化，不是压缩）

压缩前：

```javascript
function greet(name) {
  // 打招呼函数
  console.log("Hello, " + name + "!");
}
greet("World");
```

压缩后：

```javascript
function n(n){console.log("Hello, "+n+"!")}n("World");
```

文件体积从 94 字节变成了 51 字节，缩小了将近一半。

### 5.2.7 `--sourcemap` 源码映射

```bash
# 生成外部 .map 文件
esbuild src/index.js --bundle --sourcemap --outfile=dist/index.js
# 同时生成：dist/index.js 和 dist/index.js.map

# 把 sourcemap 内联到 JS 文件里
esbuild src/index.js --bundle --sourcemap=inline --outfile=dist/index.js
```

`--sourcemap` 有几个可选值：

- `true` 或 `linked`：生成外部 `.map` 文件，并在 JS 文件末尾加上 `//# sourceMappingURL=index.js.map`
- `inline`：把 sourcemap 内容直接内联到 JS 文件底部（文件会变大）
- `external`：只生成外部 `.map` 文件，不内联（与 `true` 的区别是不加 sourceMappingURL 注释）

### 5.2.8 `--watch` 监听文件变化

```bash
esbuild src/index.js --bundle --watch --outfile=dist/index.js
```

加了 `--watch` 之后，esbuild 会一直运行，监听文件变化。一旦你修改了任何被依赖的文件，esbuild 会自动重新打包——这就是"热更新"背后的原理，虽然没有 HMR 那么高级，但足够用。

```bash
# 命令行输出
$ esbuild src/index.js --bundle --watch --outfile=dist/index.js

# 初次构建
[watch] build finished, watching for changes...

# 你改了 src/index.js 后
[watch] build finished (145ms)

# 又改了 src/utils.js
[watch] build finished (87ms)
```

按 `Ctrl + C` 可以停止 watch 模式。停止之后，esbuild 会优雅地和你说再见，不会赖着不走。

> 🎯 **小技巧**：watch 模式特别适合配合浏览器 Live Reload 使用——比如 `browser-sync` 或者 VS Code 的 Live Server 插件，改了代码浏览器自动刷新，一条龙服务。

### 5.2.9 `--target` 目标环境版本

```bash
# 支持到 ES2020 语法
esbuild src/index.js --bundle --target=es2020 --outfile=dist/index.js

# 支持到 Chrome 100+
esbuild src/index.js --bundle --target=chrome100 --outfile=dist/index.js

# 同时支持多个环境，esbuild 会自动取交集
esbuild src/index.js --bundle --target=chrome100,firefox100,safari15 --outfile=dist/index.js
```

`--target` 决定了代码转译的力度。如果目标环境支持 ES2020，那 ES2020 的语法就不会被降级；如果目标是 ES2015，那 ES2020 的新语法都会被转换成 ES2015 的等价写法。

### 5.2.10 `--jsx-factory` / `--jsx-fragment` / `--jsx-import-source` JSX 参数

如果你的项目用到了 JSX，这些参数能帮你配置 JSX 的转译行为：

```bash
# 使用自定义的 JSX 创建函数（Preact 用法）
esbuild src/app.jsx --bundle --jsx-factory=h --jsx-fragment=Fragment --outfile=dist/app.js

# 使用自动导入 JSX 运行时（React 17+ 用法）
esbuild src/app.jsx --bundle --jsx-import-source=react --outfile=dist/app.js
```

### 5.2.11 参数组合实战

来一个综合实战的例子，把刚才学到的参数组合起来：

```bash
# 一个典型的生产构建命令
esbuild src/index.js \
  --bundle \
  --format=esm \
  --platform=browser \
  --target=chrome100,firefox100,safari15 \
  --minify \
  --sourcemap \
  --outfile=dist/index.js
```

这条命令的意思是：

- 以 `src/index.js` 为入口，打包所有依赖
- 输出 ESM 格式
- 目标浏览器支持现代语法
- 压缩代码
- 生成 Source Map
- 输出到 `dist/index.js`

---

## 5.3 配置文件用法（build API）

### 5.3.1 创建配置文件（esbuild.config.js / esbuild.config.mjs）

命令行参数虽然方便，但参数多了就很繁琐——每次敲一长串，既费眼睛又容易敲错，debug 起来更是欲哭无泪。

比如你上周写的 `--external:node_modules/* --format=esm --platform=browser --target=chrome100,firefox100 --minify --sourcemap` 今天再看，你能说出每个参数的含义吗？我反正不能。

配置文件就是来解决这个问题的。

创建一个 `esbuild.config.js` 文件（或者 `.mjs` 后缀表示 ESM）：

```javascript
// esbuild.config.js
const esbuild = require('esbuild');

// 异步立即执行函数，因为 esbuild 的 API 是异步的
(async () => {
  try {
    await esbuild.build({
      // 入口文件
      entryPoints: ['src/index.js'],
      // 输出目录
      outdir: 'dist',
      // 开启打包
      bundle: true,
      // 输出格式
      format: 'esm',
      // 目标环境
      target: 'es2015',
      // 生产构建需要压缩
      minify: true,
      // 生成 Source Map
      sourcemap: true,
    });
    console.log('✅ 构建成功！');
  } catch (error) {
    console.error('❌ 构建失败:', error);
    process.exit(1);
  }
})();
```

然后运行：

```bash
node esbuild.config.js
# 打印结果：✅ 构建成功！
```

### 5.3.2 build() 方法基础

`build()` 是 esbuild 最核心的 API，用于执行一次性的构建：

```javascript
const result = await esbuild.build({
  entryPoints: ['src/index.js'],
  bundle: true,
  outfile: 'dist/index.js',
  metafile: true,  // 开启元数据输出
  minify: false,
});

console.log(result.metafile); // 打印：{ inputs: {...}, outputs: {...} }
```

`build()` 返回一个 Promise，resolve 时返回一个结果对象。设置了 `metafile: true` 后，结果对象中会包含一个 `metafile` 字段，其值是一个描述输入/输出文件依赖关系的 JSON 对象。

### 5.3.3 async / await 写法

esbuild 的 API 大部分是异步的，所以需要用 `async/await` 来处理：

```javascript
// 推荐写法：async/await
const esbuild = require('esbuild');

async function build() {
  await esbuild.build({
    entryPoints: ['src/index.js'],
    outfile: 'dist/index.js',
    bundle: true,
  });
  console.log('构建完成！');
}

build();
```

你也可以用 `.then()` 的写法，但 async/await 更直观：

```javascript
// .then() 写法（不推荐，可读性差）
esbuild.build({ entryPoints: ['src/index.js'], outfile: 'dist/index.js' })
  .then(() => console.log('构建完成！'))
  .catch(() => console.error('构建失败！'));
```

### 5.3.4 开发环境 vs 生产环境配置分离

实际项目中，我们通常需要两套配置：一套给开发用（不压缩、快速构建），一套给生产用（压缩、生成 Source Map）：

```javascript
// esbuild.config.js
const esbuild = require('esbuild');

// 判断当前环境：node build.js production
const isProduction = process.env.NODE_ENV === 'production';

async function build() {
  await esbuild.build({
    entryPoints: ['src/index.js'],
    bundle: true,
    outdir: 'dist',
    // 生产环境：压缩 + sourcemap（linked 生成独立 .map 文件，inline 内联到 JS 末尾）
    minify: isProduction,
    sourcemap: isProduction ? 'linked' : true,  // 开发: 外部 map；生产: 外部 map（linked）
    // 生产环境：目标浏览器更宽泛以获得更小体积
    target: isProduction
      ? ['chrome80', 'firefox80', 'safari13']
      : ['es2015'],
  });
  console.log(isProduction ? '🚀 生产构建完成' : '⚡ 开发构建完成');
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

## 5.4 context() 方法（精细化构建控制）

### 5.4.1 context() 与 build() 的区别

`build()` 每次调用都会创建一个新的构建上下文，构建完就结束。而 `context()` 创建一个**持久的构建上下文**，你可以反复用它来触发新的构建。

```javascript
// build()：一次性构建，不保留上下文
await esbuild.build({ entryPoints: ['src/index.js'], outfile: 'dist/index.js' });

// context()：创建上下文，保留构建状态，可以复用
const ctx = await esbuild.context({
  entryPoints: ['src/index.js'],
  outfile: 'dist/index.js',
});

// 之后可以用 ctx.rebuild() 重新构建
// 可以用 ctx.watch() 监听变化
// 可以用 ctx.serve() 启动服务器
```

简单理解：`build()` 是"点一次菜，吃完就走"，`context()` 是"办一张会员卡，可以反复来"。

> 🧧 会员卡福利：办了卡之后，你可以享受 `rebuild()`（增量构建，比从头来过快得多）、`watch()`（监听文件变化）和 `serve()`（启动本地服务器）三项增值服务。卡别丢，用完记得 `dispose()` 注销。

### 5.4.2 rebuild()（手动触发增量构建）

`rebuild()` 是 `context()` 返回对象上的一个方法，用于手动触发增量构建。增量构建比重新构建快，因为它只重新打包变化了的文件：

```javascript
const ctx = await esbuild.context({
  entryPoints: ['src/index.js'],
  bundle: true,
  outfile: 'dist/index.js',
});

// 第一次构建
await ctx.rebuild();
console.log('初次构建完成');

// 改了代码之后，再调用 rebuild() 只会重新构建变化的部分
await ctx.rebuild();
console.log('增量构建完成');

// 用完了记得 dispose() 释放资源
await ctx.dispose();
```

### 5.4.3 watch()（监听文件变化自动重构建）

```javascript
const ctx = await esbuild.context({
  entryPoints: ['src/index.js'],
  bundle: true,
  outdir: 'dist',
});

// 开启监听模式
await ctx.watch();

// 这行代码之后的逻辑会一直执行，直到你手动停止
console.log('esbuild 正在监听文件变化... 按 Ctrl+C 停止');

// 配合 serve 使用时，watch 会让服务器自动返回最新构建结果
```

### 5.4.4 serve()（启动本地开发服务器）

`context()` 创建的上下文也可以启动开发服务器：

```javascript
const ctx = await esbuild.context({
  entryPoints: ['src/index.js'],
  bundle: true,
  outdir: 'dist',
  minify: false,
  sourcemap: true,
});

await ctx.watch();

// 启动本地服务器
const server = await ctx.serve({
  port: 3000,
  servedir: 'dist',
});

console.log(`本地服务器已启动: http://${server.host}:${server.port}`);
// 打印结果：本地服务器已启动: http://127.0.0.1:3000
```

### 5.4.5 dispose()（释放构建上下文）

每次创建 `context()` 都会占用系统资源，当你不再需要它的时候，记得调用 `dispose()` 来释放：

```javascript
const ctx = await esbuild.context({
  entryPoints: ['src/index.js'],
  bundle: true,
  outfile: 'dist/index.js',
});

// ... 使用 ctx ...

// 用完了，释放资源
await ctx.dispose();
console.log('构建上下文已释放');
```

`dispose()` 会停止 watch 模式和 serve 模式，所以如果你开着 watch 或 serve，在 dispose 之后它们都会停止。

`ServeResult` 对象自身带有 `stop()` 方法，可以直接调用来关闭服务器：

```javascript
// esbuild.serve() 独立模式：用 serveResult.stop() 关闭服务器
const server = await esbuild.serve(
  { servedir: 'public', port: 3000 },
  { entryPoints: ['src/index.js'], bundle: true, outdir: 'public/dist' }
);

// ...

// 需要关闭时（stop() 是 ServeResult 对象上的方法）
await server.stop();
console.log('服务器已关闭');
```

> ⚠️ **注意**：如果你在 VS Code 终端里按 `Ctrl+C` 停止 watch/esbuild 进程，不需要再手动调用 `dispose()`——进程都没了，资源早就释放了。但如果你是在 Node.js 脚本里用 `ctx.watch()` 开了监听，那一定要记得在适当的时候调用 `ctx.dispose()`，否则 Node.js 进程会一直挂在那里，既不工作也不退出，像一个迷茫的灵魂。

---

## 5.5 开发服务器配置（serve 独立模式）

### 5.5.1 serve() 独立使用（非 context 模式）

除了通过 `context()` 调用 `serve()`，你也可以直接调用 `esbuild.serve()`——这是 `serve()` 的独立形式，不需要先创建 context：

```javascript
const server = await esbuild.serve(
  {
    servedir: 'dist',  // 要服务的目录
    port: 3000,
  },
  {}  // 第二个参数是 build 选项，和 build() 的参数一样
);

console.log(`服务器运行在 http://${server.host}:${server.port}`);
// 打印结果：服务器运行在 http://127.0.0.1:3000
```

`serve()` 的返回值是一个对象（`ServeResult`），包含以下字段：

- `host`：监听地址（string），格式为 `host:port`，例如 `"127.0.0.1:8000"`
- `port`：端口号（number）
- `stop()`：关闭服务器的方法（function），是 `ServeResult` 对象自身的方法，直接调用 `server.stop()` 即可

这个写法的特点是：**服务先启动，代码变化了自动重新构建并服务**——不需要手动 watch，构建是自动的。

### 5.5.2 本地服务器配置（port / host / servedir）

```javascript
await esbuild.serve(
  {
    port: 8080,      // 端口号，默认 8000
    host: '127.0.0.1', // 主机地址，默认 0.0.0.0（允许外部访问）
    servedir: 'public', // 服务目录，默认当前目录
  },
  {
    entryPoints: ['src/index.js'],
    bundle: true,
    outdir: 'public/dist',
  }
);
```

配置说明：

- `port`：服务端口，默认 `8000`。如果被占用会自动尝试下一个端口
- `host`：监听地址。`0.0.0.0` 允许所有机器访问，`127.0.0.1` 只有本机可以访问
- `servedir`：静态文件的服务目录

### 5.5.3 proxy 配置（esbuild 并不支持内置代理）

先泼一盆冷水：**esbuild 的 serve 并没有 proxy 功能。**

别急着骂娘，这其实是合理的——esbuild 的定位是"构建工具"，不是" Web 服务器"。它的 serve 功能本质上是个极简静态文件服务器，加代理这种功能有点越界了。

如果你需要代理，最常见的解决方案有两个：

**方案一：用 express + http-proxy-middleware 搭一个简单的代理层**

这是最常见的做法——esbuild serve 处理静态文件，前面架一层 express 做代理转发：

```javascript
// proxy-server.js
const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');
const esbuild = require('esbuild');

const app = express();

// 启动 esbuild serve（返回 ServeResult：{ host, port, stop }）
const server = await esbuild.serve(
  { servedir: 'public', port: 3000 },
  { entryPoints: ['src/index.js'], bundle: true, outdir: 'public/dist' }
);

// /api 开头的请求转发到后端服务
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:4000',
  changeOrigin: true,
}));

// 所有其他请求代理到 esbuild 开发服务器（支持 WebSocket，热更新需要）
// 注意：server.host 格式为 "host:port"，需要拼接 http:// 前缀
app.use(createProxyMiddleware({
  target: `http://${server.host}`,
  changeOrigin: true,
  ws: true,
}));

// 启动 express 代理服务器
app.listen(8080, () => {
  console.log(`代理服务器已启动: http://localhost:8080`);
  console.log(`esbuild 开发服务器: http://${server.host}`);
});
```

**方案二：换一个带代理的开发服务器**

最流行的方案是用 `vite` 或 `@web/dev-server`，它们都内置了代理支持，而且底层也用 esbuild 加速构建——体验最佳，一步到位。

> 💡 **总之**：esbuild 的 serve 追求的是"小而美"——只做静态文件服务，不搞大而全。如果你在项目中需要完整的开发服务器（含代理、热更新等），可以考虑在 esbuild 前面加一层 Express 代理，或者直接使用基于 esbuild 的上层方案（如 Vite）。

### 5.5.4 watch + serve 组合使用

把 watch 模式和 serve 模式组合起来，就是一个完整的本地开发服务器——代码变化了自动重新构建，浏览器刷新就能看到最新结果：

```javascript
// 组合使用：watch + serve
const ctx = await esbuild.context({
  entryPoints: ['src/index.js'],
  bundle: true,
  outdir: 'dist',
  minify: false,
  sourcemap: true,
});

// 先 watch
await ctx.watch();

// 再启动服务器
await ctx.serve({
  port: 3000,
  servedir: 'dist',
});

console.log('🎉 本地开发服务器已启动: http://localhost:3000');
console.log('📝 修改代码后，刷新浏览器即可看到最新效果');
```

---

## 本章小结

本章我们完成了 esbuild 的入门实战。

**环境安装**：需要 Node.js（或者用原生二进制），推荐本地安装以保证版本一致性。

**命令行用法**：esbuild 的核心参数有 `--bundle`、`--outfile`、`--format`、`--platform`、`--minify`、`--sourcemap`、`--watch`、`--target`。参数组合使用可以应对各种构建场景。

**配置文件**：`build()` API 是最常用的构建方式，`async/await` 是推荐的异步写法，开发和生产环境配置分离是最佳实践。

**context() 方法**：比 `build()` 更强大，可以做增量构建（`rebuild()`）、监听文件变化（`watch()`）、启动开发服务器（`serve()`），用完记得 `dispose()` 释放资源。

**开发服务器**：esbuild 自带 `serve` 功能，配合 `watch` 模式就是一个完整的本地开发服务器（极简静态文件服务器，不含代理，代理需另行搭建）。

学会了怎么用 esbuild，下一章我们来聊聊使用 esbuild 时需要注意的那些坑——知己知彼，方能少踩坑、多写码。

> 🔮 **彩蛋预告**：下一章（实战篇）会有一个完整的项目配置模板，拿去就能用，用了就能感受到 esbuild 的速度——那种"昨晚还在用的 Webpack，今天启动只需要 200ms"的速度。
