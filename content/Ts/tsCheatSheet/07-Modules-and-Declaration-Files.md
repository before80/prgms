+++
title = "07 模块系统与声明文件"
weight = 107
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "ESM 与 CJS 互操作、模块解析策略矩阵、.d.ts 编写、声明合并与模块扩充"
isCJKLanguage = true
draft = false
+++

# 07 模块系统与声明文件

TypeScript 的模块系统是**最容易出错**的一块：它同时要描述 ES 模块、CommonJS，还要适配各种打包器和 Node 的不同解析规则。

> 所有 `❌ TSxxxx` 均为 TS 6.0.3 实测。

---

## 模块语法

{{< tabpane text=true persist=disabled >}}

{{% tab header="导入" %}}

```typescript
// 命名导入
import { readFile, writeFile } from "node:fs/promises";

// 默认导入
import path from "node:path";

// 命名空间导入
import * as fs from "node:fs";

// 重命名
import { readFile as read } from "node:fs/promises";

// 副作用导入（只为执行）
import "./polyfills";

// 类型专用导入 🆕
import type { User } from "./types";
import { type User, createUser } from "./types";   // 混合写法

// 动态导入（返回 Promise）
const mod = await import("./lazy");
```

| 写法 | 编译产物 | 何时用 |
| --- | --- | --- |
| `import { X }` | 保留（若 X 是值） | 普通导入 |
| `import type { X }` | **完全删除** | 只当类型用时 🔥 |
| `import { type X, y }` | 只保留 `y` | 混用 |
| `import * as ns` | 保留 | 需要整体引用 |

⚠️ **`import type` 是纯粹的编译期构造**，运行时不产生任何代码：

```typescript
import type { User } from "./types";
// 编译后：这一行完全消失
```

> 🔥 开启 `verbatimModuleSyntax` 后，**类型必须显式用 `import type`**，否则报错——这条规则能让输出与源码一一对应，也能让打包器（esbuild/SWC）正确处理。

{{% /tab %}}

{{% tab header="导出" %}}

```typescript
// 命名导出（推荐）
export const VERSION = "1.0";
export function createUser() {}
export class Service {}

// 类型导出
export interface User { id: number }
export type ID = string;
export type { User as UserShape };            // 重命名后导出

// 默认导出（每个模块最多一个）
export default class Client {}

// 再导出
export { readFile } from "node:fs/promises";
export * from "./utils";
export * as utils from "./utils";             // 命名空间再导出

// 类型再导出（isolatedModules 下必须写 type）
export type { User } from "./types";
```

**命名导出 vs 默认导出**：

| | 命名导出 | 默认导出 |
| --- | --- | --- |
| 数量 | 多个 | 1 个 |
| 导入时重命名 | 需要 `as` | 随意命名 |
| 重构友好度 | ✅ 改名能被追踪 | ❌ 改名容易漏 |
| Tree-shaking | ✅ 好 | ⚠️ 较差 |
| CJS 互操作 | ✅ 干净 | ⚠️ 需 `esModuleInterop` |
| 建议 | ✅ **优先用** 🔥 | 框架约定需要时用 |

> 💭 在库的公开 API 上，**优先命名导出**。默认导出在 CJS/ESM 互操作、重命名重构、tree-shaking 三方面都更麻烦。

{{% /tab %}}

{{% tab header="isolatedModules 与 verbatimModuleSyntax" %}}

这两个选项约束的是「**单文件转译**」——esbuild、SWC、Babel 一次只看一个文件，无法知道某个导入是类型还是值。

```typescript
// 🛑 转译器无法判断 User 是不是类型，只能保守地保留这行导入
import { User } from "./types";
export type A = User;
```

开启 `verbatimModuleSyntax` 后：

```typescript
import { User } from "./types";
export type A = User;
// ❌ TS1484: 'User' is a type and must be imported using a type-only import
//    when 'verbatimModuleSyntax' is enabled.

// ✅ 正确写法
import type { User } from "./types";
export type A = User;
```

再导出类型同理：

```typescript
export { User } from "./types";
// ❌ TS1205: Re-exporting a type when 'isolatedModules' is enabled requires
//    using 'export type'.

// ✅
export type { User } from "./types";
```

| 选项 | 强制什么 | 推荐 |
| --- | --- | --- |
| `isolatedModules` | 禁止「无法单文件判断」的写法 | ✅ 打包器项目应开 |
| `verbatimModuleSyntax` | 类型必须显式 `import type` | ✅ 现代项目应开 🔥 |

**两个选项带来的额外约束**：

| 写法 | `isolatedModules` 下 |
| --- | --- |
| `export { SomeType }` | ❌ 必须 `export type` |
| `const enum` | ❌ 不允许（见 [16]({{< relref "16-Pitfalls-and-Gotchas.md" >}})） |
| 只有类型导出/导入的文件 | ⚠️ 需要加 `export {}` 才算模块 |

```typescript
// 只有类型声明的文件，想成为「模块」必须显式标记
export {};                      // 或 import type {} from "..."

interface Local { a: number }   // 没有 export 时，这是全局声明！⚠️
```

> ⚠️ **上面这条是高频坑**：一个 `.ts` 文件如果**没有任何顶层 `import`/`export`**，它是**脚本（script）**，其中所有声明都是**全局的**。加上 `export {}` 才会变成模块。这就是为什么有些 `.d.ts` 会意外污染全局命名空间。

{{% /tab %}}

{{< /tabpane >}}

---

## 模块解析

{{< tabpane text=true persist=disabled >}}

{{% tab header="解析策略矩阵" %}}

`moduleResolution` 决定「`import "x"` 去哪些地方找 x」。**它必须和 `module` 搭配**。

| `module` | 推荐的 `moduleResolution` | 场景 |
| --- | --- | --- |
| `nodenext` | `nodenext` | Node.js ESM/CJS 双支持 🔥 |
| `node16` | `node16` | 同上（旧名） |
| `esnext` | `bundler` | Vite / Rollup / esbuild 🔥 |
| `preserve` | `bundler` | 交给打包器，TS 只管检查 |
| `commonjs` | `node10` 🗑️ | 已废弃，改用 `nodenext` |
| `amd` / `umd` / `systemjs` | — | 🗑️ 6.0 全部废弃 |

**6.0 废弃警告**（实测）：

| 配置 | 报错 |
| --- | --- |
| `moduleResolution: "node"` 或 `"node10"` | `TS5107` |
| `module: "amd"` / `"umd"` / `"systemjs"` / `"none"` | `TS5107` |

**两种主流配置**：

```jsonc
// Node.js 项目
{
  "compilerOptions": {
    "module": "nodenext",
    "moduleResolution": "nodenext"
  }
}

// 打包器项目（Vite / Next.js / Rspack）
{
  "compilerOptions": {
    "module": "esnext",
    "moduleResolution": "bundler"
  }
}
```

**关键差异：要不要写扩展名** 🔥

| 解析策略 | `import "./x"` | `import "./x.js"` | `import "./x.ts"` |
| --- | --- | --- | --- |
| `bundler` | ✅ 允许 | ✅ 允许 | ⚠️ 需 `allowImportingTsExtensions` |
| `nodenext`（ESM） | ❌ **报错** | ✅ 必须 | ⚠️ 需 `allowImportingTsExtensions` |
| `node10` 🗑️ | ✅ | ✅ | ❌ |

```typescript
// nodenext 下，ESM 必须写扩展名（且写 .js，不是 .ts）
import { foo } from "./foo.js";   // ✅ 即使源文件是 foo.ts
import { foo } from "./foo";      // ❌ TS2835: Relative import paths need explicit
                                  //    file extensions in ECMAScript imports.
```

> ⚠️ **「源文件是 `.ts`，但导入要写 `.js`」是最反直觉的一条**。原因：`import` 语句会被原样保留到产物里，运行时它需要指向真实的 `.js` 文件。这不是 TS 的怪癖，而是 ESM 的规范要求。

**导入 `.ts` 扩展名**：需要显式开关——用于「Node 直接跑 TS」或打包器场景：

```jsonc
{ "compilerOptions": { "allowImportingTsExtensions": true, "noEmit": true } }
```

```typescript
import { v } from "./dep.ts";   // ✅ 开启后合法
```

相关选项 `rewriteRelativeImportExtensions`（TS 5.7+）：编译时把 `.ts` 改写成 `.js`，从而**既保留 `.ts` 源码写法，又产出正确的 JS**：

```jsonc
{
  "compilerOptions": {
    "allowImportingTsExtensions": true,
    "rewriteRelativeImportExtensions": true
  }
}
```

{{% /tab %}}

{{% tab header="CommonJS 互操作" %}}

在 ESM 文件里导入 CJS 模块，历史上问题很多。`esModuleInterop` 提供了统一的处理方式——**6.0 起它恒定开启，写 `false` 会报 `TS5107`**。

```typescript
// CJS 模块（module.exports = fn）
import express from "express";        // ✅ 默认导入，靠 interop
import { Router } from "express";     // ✅ 命名导入（TS 会分析 CJS 导出的属性）
```

| 老写法 | 现代等价 | 说明 |
| --- | --- | --- |
| `import x = require("m")` | `import x from "m"` | 仅 CJS 输出下可用 |
| `export = X` | `export default X` | 仅 CJS 输出下可用 |
| `import x = require()` | — | 🚧 `nodenext` 下仍可用于 CJS 文件 |

`export =` 与 `import = require()` 在声明文件里仍会遇到（很多老库这样写）：

```typescript
// CJS 风格声明
declare function foo(): void;
export = foo;

// 消费方
import foo = require("./cjs");   // ✅ 需在 CJS 模块（module: commonjs/node16 CJS）下
foo();
```

对应的 `@types` 包写法：

```typescript
// 一个典型的 CJS 库声明
declare namespace MyLib {
  interface Options { debug?: boolean }
  function init(o?: Options): void;
}
export = MyLib;

// 消费
import MyLib from "my-lib";              // ✅ 靠 esModuleInterop
import { init } from "my-lib";           // ✅ 命名导入也行
```

> 💡 **遇到底层库导入报错时的排查顺序**：① `moduleResolution` 是否是 `bundler`/`nodenext` → ② 该库的类型声明用的是 `export =` 还是 `export default` → ③ 是否需要 `allowSyntheticDefaultImports`（6.0 已恒开）→ ④ 最后才考虑手写 `declare module`。

{{% /tab %}}

{{% tab header="paths 与 node_modules" %}}

**`paths` 做路径别名**（`baseUrl` 已在 6.0 废弃，前缀要写进每条映射里）：

```jsonc
// 🗑️ 旧写法（6.0 报 TS5101）
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": { "@/*": ["*"] }
  }
}

// ✅ 6.0 写法：把前缀折叠进每条 paths
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"]
    }
  }
}
```

> ⚠️ **`paths` 只影响类型检查，不影响运行时！** TypeScript 不会重写导入路径。运行时还需要打包器或 `imports` 字段支持：
>
> ```jsonc
> // package.json：Node 原生的子路径导入
> {
>   "imports": {
>     "#utils/*": "./src/utils/*.js"
>   }
> }
> ```
>
> 或者用打包器的 `resolve.alias`。**这里最容易出现「编辑器不报错但运行时找不到模块」**。

**`types` / `typeRoots`**：

```jsonc
{
  "compilerOptions": {
    // 6.0 默认 []，不再自动加载全部 @types！
    "types": ["node", "vitest/globals"],

    // 自定义类型根目录（很少需要改）
    "typeRoots": ["./node_modules/@types", "./src/types"]
  }
}
```

| 选项 | 作用 | 6.0 变化 |
| --- | --- | --- |
| `types` | 只加载列出的 `@types` 包 | **默认 `[]`** ⚠️ 需显式声明 |
| `typeRoots` | 从哪些目录找 `@types` | 默认 `node_modules/@types` |
| `paths` | 路径别名 | `baseUrl` 已废弃 |
| `moduleSuffixes` | 按后缀优先解析 | 少见，React Native 用 |

{{% /tab %}}

{{< /tabpane >}}

---

## 声明文件 `.d.ts`

{{< tabpane text=true persist=disabled >}}

{{% tab header="declare 家族" %}}

`.d.ts` 文件描述**已存在的运行时代码**，因此所有声明都带 `declare`。

```typescript
// 变量
declare const VERSION: string;
declare let counter: number;

// 函数
declare function greet(name: string): string;

// 类
declare class Client {
  constructor(url: string);
  get(path: string): Promise<unknown>;
}

// 命名空间（对象）
declare namespace MathUtils {
  function clamp(n: number, min: number, max: number): number;
  const PI2: number;
}

// 模块
declare module "some-untyped-lib" {
  export function doThing(): void;
}

// 全局扩充
declare global {
  interface Window { myGlobal: string }
  var myGlobalVar: number;
}
```

| 声明 | 描述的东西 |
| --- | --- |
| `declare const/let/var` | 变量 |
| `declare function` | 函数 |
| `declare class` | 类 |
| `declare namespace` | 命名空间对象 |
| `declare module "x"` | 模块（含通配） |
| `declare global` | 全局作用域 |
| `declare enum` | 枚举 |
| `declare type/interface` | 类型（不需要 `declare`） |

> ⚠️ **`type` / `interface` 不需要也不能加 `declare`**——它们在 `.d.ts` 里天然就是「声明」。

{{% /tab %}}

{{% tab header="通配模块与资源导入" %}}

给非代码资源提供类型：

```css
/* styles.module.css */
.title { font-size: 14px; }
```

```typescript
// ✅ 在 globals.d.ts 里声明（必须是「不含顶层 import/export 的脚本文件」）
declare module "*.css" {
  const classes: Readonly<Record<string, string>>;
  export default classes;
}

declare module "*.svg" {
  const url: string;
  export default url;
}

declare module "*.png" {
  const url: string;
  export default url;
}

declare module "*.json" {
  const value: unknown;
  export default value;
}
```

⚠️ **通配模块声明必须写在「脚本」文件里**，否则报错：

```typescript
// globals2.ts —— 含顶层 import，所以这是「模块」不是「脚本」
import something from "./x";

declare module "*.foo" { const v: number; export default v; }
// ❌ TS2664: Invalid module name in augmentation, module '*.foo' cannot be found.
//    在模块文件里，declare module 被当作「模块扩充」，要求目标模块已存在。
```

| 文件类型 | 判定 | `declare module "*.css"` 的含义 |
| --- | --- | --- |
| **脚本**（无顶层 import/export） | ✅ 合法 | 环境声明，定义新模块 🔥 |
| **模块**（有顶层 import/export） | ❌ `TS2664` | 模块扩充，目标必须已存在 |

> 🔥 **记住这个判定**：`.d.ts` 里写通配模块时**不要有任何顶层 `import`/`export`**。需要引用其它类型就用 `import("...").Type` 这种内联形式：
>
> ```typescript
> declare module "*.css" {
>   const classes: Readonly<Record<string, string>>;
>   export default classes;
> }
>
> declare global {
>   // 需要类型时用内联 import
>   interface Window { store: import("./store").Store }
> }
> ```

{{% /tab %}}

{{% tab header="模块扩充" %}}

给**已有的**模块添加成员。这是给第三方库补类型的主要手段。

```typescript
// 给 express 的 Request 加自定义属性
import "express";

declare module "express" {
  interface Request {
    user?: { id: string; roles: string[] };
  }
}

// 给 vue 的组件实例加属性
import "vue";

declare module "vue" {
  interface ComponentCustomProperties {
    $format: (d: Date) => string;
  }
}
```

**扩充全局作用域**：

```typescript
export {};                        // 让本文件成为模块

declare global {
  interface Window {
    __APP_CONFIG__: { apiBase: string };
  }

  // 给 process.env 加类型
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: "development" | "production" | "test";
      API_BASE: string;
    }
  }
}
```

| 想扩充 | 写法 |
| --- | --- |
| 第三方模块的接口 | `declare module "包名" { interface X { ... } }` |
| 全局 `Window` | `declare global { interface Window { ... } }` |
| `process.env` | `declare global { namespace NodeJS { interface ProcessEnv { ... } } }` |
| 第三方库的命名空间 | `declare module "包名" { ... }` + `import "包名"` |

> ⚠️ **扩充是「加法」，不能覆盖**。同名同类型的成员会**声明合并**，但类型冲突会报错。想改已有成员的**类型**，只能靠 `Omit` 重新定义接口，或使用 `patch-package` 之类的手段。

{{% /tab %}}

{{% tab header="声明合并" %}}

同名声明会自动合并。这是 `interface` 相对 `type` 的独有能力。

| 合并组合 | 结果 | 例子 |
| --- | --- | --- |
| `interface` + `interface` | 成员累加 | 库扩充的主要机制 🔥 |
| `namespace` + `namespace` | 成员累加 | 分文件写同一命名空间 |
| `namespace` + `function` | 函数带属性 | jQuery 风格 |
| `namespace` + `class` | 类带静态成员 | — |
| `namespace` + `enum` | 枚举带方法 | — |
| `function` + `function` | ❌ 重载（不是合并） | 见 [04]({{< relref "04-Functions-Objects-and-Classes.md" >}}) |
| `class` + `class` | ❌ 报错 `TS2300` | — |
| `type` + `type` | ❌ 报错 `TS2300` | — |
| `var` + `var` | ❌ 报错 | 用 `interface` 代替 |

```typescript
// interface 合并
interface Box { a: number }
interface Box { b: string }
// 结果：{ a: number; b: string } ✅

// type 不能合并
type Box2 = { a: number };
type Box2 = { b: string };   // ❌ TS2300: Duplicate identifier 'Box2'.

// namespace + function（jQuery 风格）
declare function $(sel: string): void;
declare namespace $ {
  const version: string;
}
$.("div");        // ✅ 函数可调用
$.version;        // ✅ 也有属性

// namespace + class
class Album { constructor(public name: string) {} }
namespace Album {
  export const DEFAULT = "untitled";
}
Album.DEFAULT;    // ✅ 静态成员
```

> ⚠️ **合并顺序影响重载解析**：后面的声明在重载中**优先级更高**。跨文件合并时顺序由编译顺序决定，**不要依赖它**。💭

{{% /tab %}}

{{< /tabpane >}}

---

## 三斜线指令与引用

老式的文件级指令，现在多数场景已被 `import` 和 `types` 取代。

```typescript
/// <reference path="./other.d.ts" />        // 引用另一个文件
/// <reference types="node" />               // 引用 @types/node
/// <reference lib="es2022" />               // 引用内置 lib
```

| 指令 | 现代替代 |
| --- | --- |
| `/// <reference path="..." />` | 用 `import` 或 `include` |
| `/// <reference types="..." />` | `compilerOptions.types` |
| `/// <reference lib="..." />` | `compilerOptions.lib` |
| `/// <reference no-default-lib="true" />` | 🗑️ 6.0 废弃，改用 `noLib` / `libReplacement` |

> 💡 只有在**生成的 `.d.ts`** 里还能看到它们（`tsc` 产出的声明文件会用三斜线引用依赖）。手写代码里基本不需要。

---

## 实战：为一个无类型库写声明

假设有个 `legacy-analytics` 包，没有任何类型。

**第一步：先尝试官方类型**

```bash
npm install -D @types/legacy-analytics   # 有就别自己写
```

**第二步：没有就手写最小声明**

```typescript
// src/types/legacy-analytics.d.ts
declare module "legacy-analytics" {
  export interface TrackOptions {
    userId?: string;
    properties?: Record<string, string | number | boolean>;
  }

  export function track(event: string, options?: TrackOptions): void;
  export function identify(userId: string): void;
  export function flush(): Promise<void>;

  // 有的库这样导出
  const _default: {
    track: typeof track;
    identify: typeof identify;
  };
  export default _default;
}
```

**第三步：确保被包含**

```jsonc
// tsconfig.json
{
  "include": ["src/**/*.ts", "src/**/*.d.ts"]
}
```

> ⚠️ **手写声明的风险**：它是对运行时的**假设**。写错了编译器不会发现，只会在运行时炸。所以：
>
> | 原则 | 说明 |
> | --- | --- |
> | 先读源码/文档 | 别猜 API |
> | 用 `unknown` 而不是 `any` | 保留后续收窄的可能 |
> | 标注为最小必要 | 只声明你确实用到的 |
> | 加注释写明来源 | 便于日后核对 |
> | 考虑给 DefinitelyTyped 提 PR | 惠及他人，也获得 review |

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| `.d.ts` 缺 `export {}` | 意外污染全局 | 加 `export {}` |
| 在模块文件里写通配模块 | `TS2664` | 放到无 import 的脚本文件 |
| 类型没写 `import type` | `TS1484` | 开 `verbatimModuleSyntax` 并显式标注 |
| 再导出类型没写 `type` | `TS1205` | `export type { X }` |
| `nodenext` 下漏扩展名 | `TS2835` | 写 `"./x.js"`（不是 `.ts`） |
| 以为 `paths` 影响运行时 | 运行时找不到模块 | 同步配置打包器或 `imports` |
| 6.0 后找不到 `process` | `TS2304` | `types: ["node"]` |
| 用 `baseUrl` | `TS5101` | 前缀折叠进 `paths` |
| 想覆盖库的类型 | 合并只做加法 | 重新定义接口或 patch |
| 依赖合并顺序 | 行为不稳定 | 不要依赖 |
| 手写声明猜错 API | 运行时崩溃 | 读源码，用 `unknown` |
