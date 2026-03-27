+++
title = "第11章 模块系统与声明文件"
weight = 110
date = "2026-03-26T21:05:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 11 章 模块系统与声明文件

> 如果说 TypeScript 是一座繁华的城市，模块系统就是城市的交通网络——没有它，所有的代码都挤在同一条马路上，乱成一锅粥。模块系统让你把代码拆分成独立的小区，每个小区有自己的出入口（导入/导出），互不干扰，各司其职。

## 11.1 ES 模块导出

### 11.1.1 声明导出、命名导出、默认导出、导出 all 与重导出

ES 模块（ESM）是现代 JavaScript/TypeScript 的标准模块系统。它有两种导出方式：**命名导出**和**默认导出**。

**命名导出**：每个导出有名字，导入时必须用这个名字

```typescript
// math.ts
export const PI = 3.14159;
export function add(a: number, b: number): number {
    return a + b;
}
export class Calculator {
    multiply(a: number, b: number): number { return a * b; }
}

// 导入时必须用同样的名字
import { PI, add, Calculator } from "./math";
console.log(PI); // 3.14159
```

**声明导出**：直接在声明前面加 `export`

```typescript
// shapes.ts
export interface Point {
    x: number;
    y: number;
}

export type Shape = "circle" | "square" | "triangle";

export enum Direction {
    Up, Down, Left, Right,
}
```

**默认导出**：每个模块只能有一个默认导出，导入时名字可以随便起

```typescript
// greeter.ts
export default function greet(name: string): string {
    return `Hello, ${name}!`;
}

// 导入时可以随便起名字
import greet from "./greeter";
console.log(greet("World")); // Hello, World!
```

**混合导出**：一个模块可以同时有命名导出和默认导出

```typescript
// utils.ts
export default class Utils { /* ... */ }
export const VERSION = "1.0.0";
export function helper() { /* ... */ }

// 导入
import Utils, { VERSION, helper } from "./utils";
```

**重导出（Re-export）**：把其他模块的导出再导出去

```typescript
// index.ts
// 把 math 模块的所有导出再导出
export * from "./math";

// 只导出部分
export { add, Calculator } from "./math";

// 重导出并重命名
export { add as addNumbers } from "./math";
```

---

## 11.2 ES 模块导入

### 11.2.1 命名导入、默认导入、复合导入与整体导入

**命名导入**：精确导入想要的命名导出

```typescript
import { PI, add } from "./math";
import { add as sum } from "./math"; // 重命名导入
```

**默认导入**：导入默认导出

```typescript
import greet from "./greeter";
```

**复合导入**：同时导入默认导出和命名导出

```typescript
import greet, { PI, add } from "./greeter";
```

**整体导入**：把整个模块导入为一个对象，所有命名导出变成对象的属性

```typescript
import * as math from "./math";
console.log(math.PI);           // 3.14159
console.log(math.add(1, 2));    // 3
console.log(math.Calculator);    // [class Calculator]
```

### 11.2.2 import defer（TS 5.9 新增）

#### 11.2.2.1 语法：`import defer * as names from 'module'`

`import defer` 是 TypeScript 5.9 引入的新语法，允许你**延迟执行**模块的代码。

```typescript
// 定义一个延迟加载的模块
import defer * as analytics from "./analytics";

// 模块代码不会立即执行
console.log("页面加载完成");
// analytics 的代码在这里还没有执行

// 只有当你真正使用 analytics 时，模块才会执行
analytics.trackPageView("/home");
```

#### 11.2.2.2 语义：模块在当前作用域中延迟执行，仅当真正访问时才执行

`import defer` 的核心语义是"**延迟执行**"：

- 模块的**顶层代码**（变量声明等）在导入时不执行
- 模块的**顶层代码**在第一次**访问模块的任何导出**时才执行
- 执行后，模块状态被缓存，后续访问直接使用缓存结果

```typescript
// analytics.ts
console.log("analytics 模块开始加载..."); // 这行代码在第一次访问 analytics 之前不会执行

export function trackPageView(page: string) {
    console.log(`跟踪页面: ${page}`);
}

export const config = { apiKey: "xxx" };

// main.ts
import defer * as analytics from "./analytics";
console.log("模块加载完毕");

analytics.trackPageView("/home"); // 第一次访问，触发模块执行
// 输出: analytics 模块开始加载...
// 输出: 跟踪页面: /home

analytics.trackPageView("/about"); // 第二次访问，使用缓存，不重复执行模块代码
```

#### 11.2.2.3 设计动机：大型应用的按序加载管理，减少初始包体积；类似 HTML 的 `<script defer>`

这个语法的设计动机和 HTML 的 `<script defer>` 完全一样：

- **不使用 defer**：模块立即执行，阻塞后续代码
- **使用 defer**：模块延迟执行，不阻塞后续代码

典型应用场景：
- **日志/监控模块**：不影响主业务流程
- **大型库**：延迟加载减少初始 bundle 体积
- **按需初始化的配置**：如 i18n 配置、主题配置

### 11.2.3 Subpath Imports with #/（TS 6.0 新增）

#### 11.2.3.1 Node.js 20+ 支持 `#/` 开头的 subpath import

`#/subpath` 是 Node.js 20+ 引入的一种特殊导入路径，用于**简化内部模块导入**。

#### 11.2.3.2 语法：`import { something } from '#/utils'`

```typescript
// 从项目根目录的 src/utils/index.ts 导入
import { formatDate } from "#/utils";
// 相当于
import { formatDate } from "./src/utils/index.ts"; // 不用再写相对路径
```

#### 11.2.3.3 配置：package.json 的 `imports` 字段中使用 `"#": "./dist/index.js"` 和 `"#/*": "./dist/*"`

在 `package.json` 中配置路径映射：

```json
{
    "name": "my-package",
    "exports": {
        ".": "./dist/index.js"
    },
    "imports": {
        "#utils": "./dist/utils/index.js",
        "#utils/*": "./dist/utils/*.js",
        "#config": "./dist/config/index.js",
        "#config/*": "./dist/config/*.js"
    }
}
```

#### 11.2.3.4 支持范围：`--moduleResolution` 为 node20 / nodenext / bundler 时启用

这个功能需要正确的 `moduleResolution` 配置：

```json
{
    "compilerOptions": {
        "moduleResolution": "node20" // 或 "nodenext" 或 "bundler"
    }
}
```

### 11.2.4 类型导入与导出

TypeScript 扩展了 ES 模块，支持专门导入/导出**类型**。

#### 11.2.4.1 import type：`import type { SomeType } from 'module'`

```typescript
import type { User, Admin } from "./types";

// 编译后，这行 import 会被完全删除
// 因为类型信息在运行时不存在
```

#### 11.2.4.2 export type：`export type { SomeType }`

```typescript
// types.ts
export type User = { id: number; name: string };
export interface Admin extends User { permissions: string[]; }
export { type User, type Admin }; // 只导出类型
```

#### 11.2.4.3 为什么需要 import type：纯类型导入不产生运行时代码；解决循环导入问题

`import type` 的价值在于**编译时完全消除**——纯类型的导入在编译成 JavaScript 后会消失，不会产生任何运行时代码。

```typescript
// user.ts
import type { Config } from "./config"; // 编译后消失
import { fetchUser } from "./api";       // 编译后保留

export function getUser(id: number) {
    // ...
}
```

另外，`import type` 可以帮助解决某些循环导入问题——因为纯类型导入在编译后消失，不会在运行时造成问题。

### 11.2.5 import() 断言废弃（TS 6.0）

#### 11.2.5.1 旧语法：`import(obj, { assert: { type: 'json' } })` → 已废弃

旧版的动态 import 使用 `assert` 语法：

```typescript
const data = await import("./config.json", {
    assert: { type: "json" },
});
```

#### 11.2.5.2 新语法：`import(obj, { with: { type: 'json' } })`

TypeScript 6.0 将 `assert` 替换为 `with`：

```typescript
const data = await import("./config.json", {
    with: { type: "json" },
});
```

> **注意**：这是运行时行为的变化，不是 TypeScript 独有的。Node.js 和浏览器也在逐步切换到 `with` 语法。

---

## 11.3 模块的运行时行为

### 11.3.1 ES Module vs CommonJS 运行时差异

JavaScript 有两套模块系统：**ES Module（ESM）** 和 **CommonJS（CJS）**。它们在运行时行为上有显著差异。

#### 11.3.1.1 ESM：静态结构（import 在模块顶层，不能在条件语句中）、异步加载、import 绑定只读

ES Module 的核心特征是**静态结构**：

```javascript
// ESM - 静态导入，必须在模块顶层
import { foo } from "./module"; // 不能在 if 语句里
import.meta.url; // 访问模块元信息

export { foo };
export default bar;
```

#### 11.3.1.2 CJS：动态结构（require 可在任意位置）、同步加载、module.exports 可变

CommonJS 的核心特征是**动态结构**：

```javascript
// CJS - 动态导入，可以在任何地方
if (someCondition) {
    const foo = require("./module");
}
module.exports = { foo };
```

#### 11.3.1.3 混用限制：ESM 文件中不能使用 require；CJS 文件中不能使用动态 import（除非在 async 函数内）

```typescript
// ESM 文件中，动态 import() 是允许的（它是异步的）
const mod = await import("./module");

// 但 CJS 中，动态 import() 在顶层不能使用（需要 async 函数包装）
// const mod = await import("./module"); // 在 CJS 顶层会报错
```

### 11.3.2 esModuleInterop 配置的作用

`esModuleInterop` 是 TypeScript 编译选项中最重要的选项之一，它解决的是 **ESM 和 CJS 之间的互操作性问题**。

#### 11.3.2.1 让 `import 'module'` 在 default import 缺失时自动桥接（即使模块只有 CommonJS 导出）

在没有 `esModuleInterop` 的情况下，导入 CJS 模块时会有奇怪的行为：

```typescript
// 没有 esModuleInterop 时
import fs from "fs"; // fs 是 CJS 模块，只有 named exports，没有 default export
// TypeScript 报错或产生 undefined
```

有了 `esModuleInterop: true`：

```typescript
// tsconfig.json
{
    "compilerOptions": {
        "esModuleInterop": true
    }
}
```

```typescript
import fs from "fs"; // OK！现在 TypeScript 会自动处理 CJS 模块
fs.readFileSync("./file.txt", "utf-8");
```

#### 11.3.2.2 自动在输出的 bundle 中添加 ESM/CommonJS 兼容层（如 `__importStar`、`__importDefault`）

`esModuleInterop` 会在编译输出中注入辅助函数：

```javascript
// 编译前
import fs from "fs";

// 编译后（开启 esModuleInterop）
import __import fs from "fs";
```

### 11.3.3 Combining --moduleResolution bundler with --module commonjs（TS 6.0 新增）

#### 11.3.3.1 以前：`--moduleResolution bundler` 只能与 --module esnext 或 --module preserve 组合

在 TS 6.0 之前，`--moduleResolution bundler` 是一个"偏食"的选项——它只和 ESM 风格的 `--module` 配置搭配。

```json
// 旧配置（报错）
{
    "compilerOptions": {
        "moduleResolution": "bundler",
        "module": "commonjs" // 不兼容！
    }
}
```

#### 11.3.3.2 现在：允许与 --module commonjs 组合，为迁移提供更灵活的路径

TS 6.0 解除了这个限制：

```json
// 新配置（OK）
{
    "compilerOptions": {
        "moduleResolution": "bundler",
        "module": "commonjs"
    }
}
```

这为那些想用 `bundler` 的路径解析策略，但又需要输出 CommonJS 的项目提供了更大的灵活性。

---

## 11.4 声明文件（.d.ts）

### 11.4.1 声明文件的作用

`.d.ts` 文件是 TypeScript 的"**类型声明文件**"——它只描述类型，不包含任何运行时代码。

#### 11.4.1.1 为 JavaScript 代码补上类型信息，不包含实现

当你有一个纯 JavaScript 库时，可以用 `.d.ts` 文件给它加上类型信息：

```typescript
// my-lib.d.ts（类型声明文件）
declare module "my-lib" {
    export function greet(name: string): string;
    export const VERSION: string;
}
```

#### 11.4.1.2 为什么需要 .d.ts：JavaScript 代码没有类型信息，TypeScript 需要类型才能检查

JavaScript 是动态类型语言，没有类型信息。TypeScript 需要类型信息才能做类型检查。`.d.ts` 文件就是 TypeScript 的"眼睛"——让它在没有类型的 JavaScript 代码中也能做类型检查。

#### 11.4.1.3 .d.ts 只包含类型声明，不包含实现代码；编译时使用，运行时不加载

```typescript
// 声明文件
declare function add(a: number, b: number): number;
declare const PI: number;
declare class Calculator { /* ... */ }

// 这些声明在编译后完全消失，不产生任何 JavaScript 代码
```

### 11.4.2 全局声明：`declare var`、`declare function`、`declare namespace`

在 `.d.ts` 文件中，可以使用 `declare` 关键字来声明全局变量、函数和命名空间：

```typescript
// global.d.ts
declare var VERSION: string;
declare function log(message: string): void;
declare namespace MathUtils {
    export function add(a: number, b: number): number;
    export function multiply(a: number, b: number): number;
}
```

### 11.4.3 模块声明：`declare module 'module-name'`

为某个 npm 包或本地模块声明类型：

```typescript
// my-plugin.d.ts
declare module "my-plugin" {
    interface PluginOptions {
        debug?: boolean;
        timeout?: number;
    }

    export function init(options?: PluginOptions): void;
    export const version: string;
}
```

---

## 11.5 @types 与 DefinitelyTyped

### 11.5.1 @types/* 包的安装与使用

TypeScript 社区为几乎所有流行的 npm 包维护了类型声明——这就是 `@types/*` 包。

```bash
# 安装 React 的类型声明
npm install --save-dev @types/react

# 安装 Lodash 的类型声明
npm install --save-dev @types/lodash

# 安装 Node.js 的类型声明（用于 Node.js 环境）
npm install --save-dev @types/node
```

安装后，TypeScript 会自动找到并使用这些类型声明，不需要任何额外配置。

### 11.5.2 为什么有 @types

#### 11.5.2.1 JavaScript 生态在 TypeScript 出现前就存在大量库；DefinitelyTyped 社区为每个库编写并维护类型声明文件

JavaScript 生态有数十万个 npm 包，它们都是在 TypeScript 诞生前写的，没有类型信息。DefinitelyTyped（DefinitelyTyped.org）是一个社区项目，为这些库补上类型声明。

### 11.5.3 为无类型的 npm 包编写 declare module

如果你用的 npm 包没有类型声明，可以自己写一个声明文件：

```typescript
// 自定义声明文件 src/custom.d.ts
declare module "some-untyped-package" {
    export function doSomething(input: string): Promise<{ result: string }>;
    export const config: { debug: boolean };
}

// 使用
import { doSomething, config } from "some-untyped-package";
```

---

## 11.6 声明合并

TypeScript 允许**同名的 interface、namespace、enum 声明自动合并**——这是一个独特的特性，在其他静态类型语言中很少见。

### 11.6.1 同名 interface 合并

当两个同名的 interface 相遇时，它们的成员会自动合并：

```typescript
interface Animal {
    name: string;
}

interface Animal {
    age: number;
}

// 相当于
interface Animal {
    name: string;
    age: number;
}

const animal: Animal = {
    name: "小狗",
    age: 3,
};
```

#### 11.6.1.1 非函数成员：直接合并，类型不一致时报错

```typescript
interface A {
    id: number;
}

interface A {
    id: string; // 报错！类型不一致，无法合并
}
```

#### 11.6.1.2 函数成员：多个签名作为重载列表，依次排列（更具体的签名在前）

```typescript
interface Greeter {
    greet(name: string): string;
}

interface Greeter {
    greet(name: string, age: number): string;
}

// 相当于
interface Greeter {
    greet(name: string, age?: number): string;
    // 重载列表：先匹配无 age 的，再匹配有 age 的
}

const greeter: Greeter = {
    greet(name: string, age?: number) {
        if (age !== undefined) {
            return `你好 ${name}，你 ${age} 岁了`;
        }
        return `你好 ${name}`;
    },
};

console.log(greeter.greet("小明"));            // 你好 小明
console.log(greeter.greet("小红", 18));        // 你好 小红，你 18 岁了
```

### 11.6.2 同名 namespace 合并

```typescript
namespace Config {
    export const name = "App";
    export function init() { console.log("Config 初始化了"); }
}

namespace Config {
    export const version = "1.0.0";
    export function start() { console.log("Config 启动了"); }
}

// 相当于
namespace Config {
    export const name = "App";
    export const version = "1.0.0";
    export function init() { console.log("Config 初始化了"); }
    export function start() { console.log("Config 启动了"); }
}

Config.init();
// Config 初始化了
Config.start();
// Config 启动了
```

#### 11.6.2.1 namespace 内的导出成员会合并到同一命名空间

### 11.6.3 命名空间与类的合并

```typescript
class User {
    name: string = "张三";
}

// 在 User 类的命名空间中扩展静态属性
namespace User {
    export let count: number = 0;
    export function createGuest() {
        count++;
        return new User();
    }
}

// User 类本身是实例类型
// User 命名空间提供静态成员
console.log(User.count);      // 0
const guest = User.createGuest();
console.log(User.count);      // 1
```

#### 11.6.3.1 允许在 namespace 内扩展 class 的静态属性（在 .d.ts 中用于描述全局单例对象的扩展）

### 11.6.4 同名 type 不合并（别名冲突直接报错）

```typescript
type Id = number;
type Id = string; // 报错！Cannot redeclare type alias 'Id'
```

`type` 别名在 TypeScript 中不会合并——这是和 `interface` 的最大区别。

---

## 本章小结

本章系统地介绍了 TypeScript 的模块系统和声明文件。

### ES 模块

ES Module 是现代 JavaScript 的标准模块系统，核心特征是**静态结构**（import/export 在顶层，不能条件执行）。

- **命名导出/导入**：`export { foo }` / `import { foo }`
- **默认导出/导入**：`export default bar` / `import bar`
- **整体导入**：`import * as ns`
- **重导出**：`export { foo } from "./module"`

### 新特性

- **import defer（TS 5.9）**：延迟模块执行，类似 `<script defer>`
- **Subpath Imports #/（TS 6.0）**：简化内部模块导入路径
- **moduleResolution bundler + commonjs（TS 6.0）**：解除组合限制

### 类型导入

- `import type` / `export type`：纯类型导入，编译后消除
- `import()` 断言改用 `with` 语法

### 声明文件

`.d.ts` 文件为 JavaScript 库提供类型信息，`declare` 关键字用于声明全局变量、函数、命名空间、模块。社区维护的 `@types/*` 包为绝大多数 npm 库提供开箱即用的类型支持。

### 声明合并

同名的 `interface` 和 `namespace` 会自动合并（函数成员变成重载列表），但 `type` 别名不会合并。命名空间可以扩展同名类的静态成员——这是 `.d.ts` 文件中常见的模式。

> 模块系统是 TypeScript 项目的骨架。一个好的模块设计应该：高内聚（模块内部紧密相关）、低耦合（模块之间尽量少的依赖）、接口清晰（导出明确，隐藏内部细节）。
