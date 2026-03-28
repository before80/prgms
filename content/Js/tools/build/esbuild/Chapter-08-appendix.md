

+++
title = "第8章 附录"
weight = 80
date = "2026-03-28T11:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

## 8.1 官方资源链接（GitHub / 文档 / changelog）

学习任何工具，官方文档永远是最权威的资料。以下是 esbuild 的官方资源：

| 资源 | 链接 |
|------|------|
| GitHub 仓库 | [github.com/evanw/esbuild](https://github.com/evanw/esbuild) |
| 官方文档 | [esbuild.github.io](https://esbuild.github.io) |
| 官方博客 | [esbuild.github.io/news](https://esbuild.github.io/news) |
| Changelog | [github.com/evanw/esbuild/releases](https://github.com/evanw/esbuild/releases) |
| npm 页面 | [www.npmjs.com/package/esbuild](https://www.npmjs.com/package/esbuild) |

### GitHub 仓库

esbuild 的 GitHub 仓库（github.com/evanw/esbuild）是获取信息的第一站。

你可以在这个仓库里：

- 查看源代码，了解 esbuild 底层是怎么实现的
- 提 Issue 报告 bug 或者提功能请求
- 看别人提的 Issue，了解 esbuild 的已知问题和未来计划
- 参与社区讨论

一句话总结：这里才是 esbuild 的"源代码级真相"，所有文档的终点。

### 官方文档

esbuild 的官方文档（esbuild.github.io）简洁明了，涵盖了所有 API 和配置项的详细说明。如果你觉得这本书某个地方讲得不够清楚，可以去官方文档查证原文——万一哪天 esbuild 更新了，这本书还没来得及更新，官方文档永远是最新的。

### 官方博客

esbuild 的博客会不定期发布新版本说明、功能介绍、以及一些技术原理的深度解析。推荐关注，尤其是大版本更新时。

### Changelog

每次版本更新都会在 GitHub Releases 页面发布详细的变更日志。如果你的项目在使用某个版本时遇到了奇怪的问题，先看看 changelog 里有没有相关的修复记录。

> 💡 **小技巧**：订阅 GitHub Releases 的邮件通知，大版本更新时你会收到邮件，比刷社交网络靠谱多了。

---

## 8.2 命令行参数速查表

下面是 esbuild 命令行参数的速查表，按照功能分类，方便日常查阅。

> 记住这些参数就像记住前任的名字——用多了自然就记住了，用少了永远记不住。没关系，收藏这一页就行。反正你迟早会回来找它的。

### 基础参数

| 参数 | 说明 | 示例 |
|------|------|------|
| *(入口文件)* | 入口文件（位置参数，直接写路径） | `esbuild app.js` |
| `--bundle` | 开启打包 | `--bundle` |
| `--outfile=path` | 输出到文件 | `--outfile=dist/bundle.js` |
| `--outdir=path` | 输出到目录 | `--outdir=dist` |

### 格式与平台

| 参数 | 说明 | 示例 |
|------|------|------|
| `--format=esm` | 输出 ESM 格式 | `--format=esm` |
| `--format=cjs` | 输出 CJS 格式 | `--format=cjs` |
| `--format=iife` | 输出 IIFE 格式 | `--format=iife` |
| `--platform=browser` | 浏览器平台 | `--platform=browser` |
| `--platform=node` | Node.js 平台 | `--platform=node` |
| `--platform=neutral` | 中立平台 | `--platform=neutral` |

### 代码处理

| 参数 | 说明 | 示例 |
|------|------|------|
| `--minify` | 压缩代码 | `--minify` |
| `--sourcemap` | 生成 Source Map | `--sourcemap` |
| `--target=es2020` | 目标环境 | `--target=chrome100,firefox100,safari15` |
| `--jsx=automatic` | 自动 JSX 运行时 | `--jsx=automatic` |
| `--jsx-factory=h` | JSX 元素函数（classic 模式） | `--jsx-factory=h` |
| `--jsx-fragment=Fragment` | JSX 片段函数（classic 模式） | `--jsx-fragment=Fragment` |
| `--loader=.png=dataurl` | 文件加载器映射 | `--loader=.png=dataurl` |
| `--external:npm:pkg` | 外部化依赖 | `--external:npm:pkg` |
| `--alias=src=dist` | 路径别名 | `--alias=src=dist` |
| `--define:DEBUG=true` | 全局字符串替换 | `--define:DEBUG=true` |
| `--preserve-symlinks` | 保留符号链接原样 | `--preserve-symlinks` |
| `--banner=txt` | 文件头部注入内容 | `--banner="/* esbuild */"` |
| `--footer=txt` | 文件尾部注入内容 | `--footer="/* built */"` |
| `--splitting` | 开启代码分割（需配合 --format=esm） | `--splitting` |
| `--tree-shaking` | 开启摇树优化（默认开启） | `--tree-shaking` |
| `--legal-comments=mode` | 控制法律注释位置（none/inline/external） | `--legal-comments=none` |
| `--metafile=path` | 生成元数据文件（供分析工具使用） | `--metafile=dist/meta.json` |

### 文件监听与服务

| 参数 | 说明 | 示例 |
|------|------|------|
| `--watch` | 监听文件变化 | `--watch` |
| `--serve=port` | 启动开发服务器 | `--serve=3000` |

### 实战命令示例

> 如果你懒得配置又想看起来很专业，直接复制这些命令就行。反正 esbuild 快，配置错了重新跑也花不了多少时间（不是）。

```bash
# 最基础的单文件打包
esbuild app.js --bundle --outfile=dist/app.js

# 生产构建（压缩 + sourcemap）
esbuild app.js --bundle --minify --sourcemap --outfile=dist/app.js

# 浏览器应用，ESM 格式
esbuild app.js --bundle --format=esm --platform=browser --outfile=dist/app.mjs

# Node.js 类库，CJS 格式
esbuild app.js --bundle --format=cjs --platform=node --outfile=dist/app.js

# 带 watch 模式（改完代码自动重新打包，手都不用动）
esbuild app.js --bundle --watch --outfile=dist/app.js

# 带开发服务器（改完代码浏览器自动刷新，除非你手速比 V8  JIT 编译还快）
esbuild app.js --bundle --serve=3000 --outdir=dist
```

---

## 8.3 配置项速查表

下面是 `esbuild.build()` API 的配置项速查表。记不住所有配置？正常，没人能记住。这里就是你的"配置作弊小抄"——别害羞，开卷考试也是一种能力。

> 🔑 **背诵口诀**：entry 是亲爹，out 是亲妈，format 和 platform 定终身，剩下都是调味料。

### 入口与出口

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `entryPoints` | `string[]` | 入口文件列表（必填项，不填你就等着报错吧） |
| `outdir` | `string` | 输出目录 |
| `outfile` | `string` | 输出文件（单入口时用，多入口请用 outdir） |
| `outbase` | `string` | 输出基础目录 |
| `outExtension` | `Record<string,string>` | 输出扩展名映射 |
| `stdin` | `object` | 从标准输入读取（高级玩法） |
| `absWorkingDir` | `string` | 工作目录（绝对路径） |
| `allowOverwrite` | `boolean` | 允许覆盖已有文件 |
| `write` | `boolean` | 是否写入文件系统（设为 false 可用于内存分析） |

### 格式与平台

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `format` | `'esm' \| 'cjs' \| 'iife'` | 输出格式 |
| `platform` | `'browser' \| 'node' \| 'neutral'` | 目标平台 |
| `mainFields` | `string[]` | 模块主字段优先级 |
| `conditions` | `string[]` | exports 条件导出 |

### 代码处理

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `target` | `string \| string[]` | 目标环境 |
| `loader` | `Record<string,string>` | 文件加载器映射 |
| `jsx` | `'automatic' \| 'classic' \| 'transform'` | JSX 处理模式 |
| `jsxFactory` | `string` | JSX 元素函数 |
| `jsxFragment` | `string` | JSX 片段函数 |
| `jsxImportSource` | `string` | JSX 运行时来源 |
| `jsxDev` | `boolean` | 开发模式 JSX |
| `minify` | `boolean` | 压缩代码 |
| `mangleProps` | `string \| RegExp` | 属性名混淆 |
| `keepNames` | `boolean` | 保留函数名 |
| `drop` | `string[]` | 删除特定语句 |
| `pure` | `string[]` | 标记无副作用调用 |
| `legalComments` | `'none' \| 'inline' \| 'external' \| 'linked' \| 'eof'` | 法律注释位置（`none` 移除、`inline` 内联到输出中、`external` 输出到单独文件、`linked` 同 external 但以链接方式引用、`eof` 输出到文件末尾） |

### 路径解析

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `alias` | `Record<string,string>` | 路径别名 |
| `external` | `string[]` | 外部依赖 |
| `resolveExtensions` | `string[]` | 扩展名补全顺序 |
| `nodePaths` | `string[]` | 模块搜索路径 |

### 源码映射

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `sourcemap` | `boolean \| 'inline' \| 'external'` | Source Map 类型（true 或 'external' 生成外部 .map 文件，'inline' 内联到产物中，false 不生成） |
| `sourceRoot` | `string` | 源码根路径 |
| `sourcesContent` | `boolean` | 内联源码内容（设为 true 方便调试，设为 false 减小产物尺寸） |

### 全局变量

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `define` | `Record<string,string>` | 字符串替换 |
| `inject` | `string[]` | 注入文件列表 |

### 日志

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `logLevel` | `'debug' \| 'info' \| 'warning' \| 'error' \| 'silent'` | 日志级别（调成 silent 世界安静，调成 debug 控制台爆炸 💥） |
| `logLimit` | `number` | 错误信息行数限制 |
| `logOverride` | `Record<string,string>` | 按错误代码覆盖日志级别 |
| `banner` | `Record<string,string>` | 文件头部注入 |
| `footer` | `Record<string,string>` | 文件尾部注入 |

### 其他

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `bundle` | `boolean` | 是否打包 |
| `splitting` | `boolean` | 是否开启代码分割 |
| `treeShaking` | `boolean` | 是否开启 Tree Shaking |
| `metafile` | `boolean` | 生成元数据文件（供分析工具如 bundle-buddy 使用） |
| `tsconfig` | `string` | tsconfig.json 路径 |

---

## 8.4 常见错误代码速查

下面是 esbuild 常见错误的含义和解决方法。遇到问题时，先来这里找答案，省得到处搜索浪费时间——虽然直接 Google 报错信息也是一种选择，但万一你网络不好呢（不会吧）？

| 错误信息 | 含义 | 解决方法 |
|---------|------|---------|
| `Could not resolve "xxx"` | 找不到模块 "xxx" | 确认模块已安装，或检查路径是否正确 |
| `Cannot initialize worker when already initialized` | 重复初始化 | 确保没有同时调用多次 `context()` |
| `"xxx" is not compatible with "yyy"` | 平台和格式不兼容 | 检查 `platform` 和 `format` 的组合是否合理 |
| `"splitting" is only supported with "esm" format and "browser" platform` | 代码分割只能在 ESM 格式 + browser 平台下使用 | 确保 `format: 'esm'` 且 `platform: 'browser'`，CLI 下需同时加 `--format=esm --platform=browser` |
| `Expected "xxx" but got "yyy"` | 语法错误 | 检查源代码语法是否正确 |
| `Cannot import from "node:" protocol` | 旧版不支持 `node:` 协议 | 新版（≥0.14）已支持，直接用 `import 'node:fs'` 即可 |

> 📌 **防呆提示**：如果错误信息里提到了 "esm" 或 "format"，先检查你的 `format` 和 `platform` 配置组合是否合法。esbuild 的报错信息其实挺智能的，会告诉你问题出在哪，别光顾着骂娘，仔细读读。

---

## 8.5 术语表

下面是本书中出现的一些关键术语的解释。看完了还不懂？建议从头再看一遍（不是开玩笑，是真心建议，重复是学习他妈）。

### Bundler（打包工具）

把多个模块文件合并成一个或几个文件的工具。esbuild 就是一个 Bundler。

### Transpiling（转译）

把一种语言（或语言版本）转换成另一种等价形式，但不改变语言本身。比如 TypeScript 转成 JavaScript。

### Minifying（压缩）

把代码变"小"的过程——删除空格、注释、缩短变量名。压缩后的代码叫 minified code。

### Tree Shaking（摇树优化）

通过静态分析删除没有被用到的代码（死代码）的优化手段。只在 ESM 格式下完全生效。（名字很文艺对吧？想象一下用力摇晃一棵树，没用的果子（死代码）就会被抖落下来。）

### Source Map（源码映射）

记录压缩后代码与原始代码位置对应关系的文件，用于在调试时还原原始代码位置。

### HMR（热模块替换）

Hot Module Replacement，在页面不刷新的情况下替换已修改的模块，保留页面状态。

### Code Splitting（代码分割）

把打包产物拆成多个文件，浏览器按需加载的技术。

### Bundling（打包）

把多个模块及其依赖打包成少数文件的过程，目的是减少网络请求。

### Dependency Graph（依赖图）

描述模块之间导入导出关系的图结构。esbuild 通过分析依赖图来决定哪些文件需要打包。

### ESM（ES Modules）

ES6 引入的官方模块系统，使用 `import` 和 `export` 语法。

### CJS（CommonJS）

Node.js 传统的模块系统，使用 `require()` 和 `module.exports`。

### Side Effects（副作用）

当一个函数执行时，除了返回值之外还对外部环境产生了影响（如修改全局变量、发送网络请求）。

### sideEffects（package.json 字段）

`package.json` 的字段，用于告诉打包工具哪些文件有副作用、哪些没有，帮助 Tree Shaking。

### Pure Function（纯函数）

没有副作用、相同输入总是产生相同输出的函数。esbuild 可以对纯函数做更激进的优化。

### Plugin（插件）

扩展 esbuild 功能的机制。通过一系列生命周期钩子拦截文件解析和加载过程，自定义如何处理特定文件类型或路径。核心钩子包括：
- `onResolve` — 拦截模块解析请求，可修改路径或标记外部依赖
- `onLoad` — 拦截文件加载，可读取文件内容并返回自定义结果
- `onDispose` — 清理钩子，构建完成后释放资源

esbuild 的插件 API 和 Rollup 插件 API 高度相似，上手门槛低，社区插件生态丰富。（如果你用过 Rollup，写 esbuild 插件就是小菜一碟，API 几乎可以无缝迁移。）

### Build Context（构建上下文）

通过 `esbuild.context()` 创建的上下文对象，用于管理多次构建和增量构建。可以单独控制每个上下文的 watch、serve、rebuild 等行为，实现高级的构建编排。

### Serve（开发服务器）

esbuild 内置的轻量开发服务器，提供静态文件服务（**无 API 代理能力**，如需代理请配合 nginx 等反向代理工具）。启动后监控文件变化自动重新构建，请求直接透传到最新的构建产物，开发体验接近"即时生效"。

### IIFE

Immediately Invoked Function Expression，立即执行的函数表达式。代码被包在一个匿名函数中并立即执行，常用于浏览器中安全地隔离变量作用域，也是 `format: 'iife'` 输出的标准形式。


---

## 本章小结

第八章是本书的收尾附录部分。

我们给出了官方资源链接（GitHub 仓库、官方文档、博客、Changelog），方便你在需要深入学习时找到一手资料。

命令行参数速查表和配置项速查表是两份实用工具文档，日常开发时可以快速查阅，不用每次都翻正文。

常见错误代码速查表帮助你快速定位和解决问题。

术语表汇总了全书出现的所有关键概念，方便复习和巩固。

走到这里，esbuild 的知识体系已经全部覆盖——从"是什么"到"怎么用"，从核心能力到配置细节，从注意事项到生态集成。

如果看到这里你还有困惑，恭喜你——你是一个正常的初学者。建议：去跑步、去睡觉、去吃点好的，明天再看一遍，每一遍都会有新收获。（别打我，这是真的）

如果看到这里你已经觉得"就这？"，那说明你已经出师了。接下来你可以去读 esbuild 源码——大约一万行 Go 代码，写得干净利落，是学习 Go 和构建工具的绝佳素材。读完之后记得回来给我讲讲，让我知道你有多厉害（或者让我崇拜你一下）。

希望这本书能成为你学习 esbuild 路上的得力助手。如果还有什么不明白的地方，官方文档永远是最好的下一站。（我打赌你会忘了我，但没关系，我会在这里默默等你回来）。

祝打包愉快，构建飞速！🚀

> 🎉 **彩蛋**：感谢你坚持看到这里。如果你觉得这本书有用，请告诉你身边那个还在用 webpack 的朋友。也许你的转发能拯救他的头发。
