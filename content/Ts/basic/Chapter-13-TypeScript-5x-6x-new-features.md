+++
title = "第13章 TypeScript 5.x ~ 6.x 新特性详解"
weight = 130
date = "2026-03-26T21:05:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 13 章 TypeScript 5.x ~ 6.x 新特性详解

> **本章说明**：TypeScript 从 5.0 到 6.x，引入了大量让人眼前一亮的新特性。本章按版本时间线，从实际应用角度讲解每个特性的设计动机、语法和典型使用场景，让你不仅「知道有这回事」，更能「知道什么时候用它」。

## 13.1 TypeScript 5.0 ~ 5.4 核心新特性

TypeScript 5.0 是一个非常重要的里程碑版本，它带来了多个从 TypeScript 用户社区投票中诞生的特性（之前 TS 团队会从 GitHub issues 里收集用户投票最高的特性请求，然后实现它们）。

### 13.1.1 const 类型参数（TS 5.0）

---

#### 13.1.1.1 语法：`<const T>`

这是 TypeScript 5.0 最受欢迎的特性之一！它的设计动机非常清晰：**解决泛型函数中字面量类型被过度推断的问题**。

先看一个没有 `const` 类型参数时的「痛苦」：

```typescript
// ❌ 没有 const 类型参数
function inferLiteral<T>(value: T) {
  return value;
}

const result = inferLiteral("hello");
// result 的类型是 string，而不是 "hello"！
// 因为 TypeScript 把字面量 "hello" 推断为宽泛的 string
```

```typescript
// ✅ 有 const 类型参数
function inferLiteral<const T>(value: T) {
  return value;
}

const result = inferLiteral("hello");
// result 的类型是 "hello"（字面量类型），而不是 string！
// ✅ const 类型参数让泛型精确推断为字面量类型
```

---

#### 13.1.1.2 设计动机：泛型函数中的字面量类型推断经常被扩大为宽泛类型；`<const T>` 让泛型参数精确推断为字面量类型

`const` 类型参数主要用于以下场景：

**场景一：路径字面量**

```typescript
// ❌ 没有 const：path 被推断为 string
function getConfig<const T>(path: T) {
  return path;
}

const path1 = getConfig("/api/users");
// path1 类型：string（不是 "/api/users"）

// ✅ 有 const：path 精确推断为 "/api/users"
function getConfig<const T>(path: T): T {
  return path;
}

const path2 = getConfig("/api/users");
// path2 类型："/api/users"（字面量类型！）
```

**场景二：对象字面量**

```typescript
// ✅ const 类型参数让对象属性的类型也保持精确
function createRoute<const T extends Record<string, string>>(config: T): T {
  return config;
}

const route = createRoute({
  path: "/home",
  name: "home-page"
});
// route 的类型精确为 { path: "/home", name: "home-page" }
// 而不是宽泛的 { path: string, name: string }
```

**场景三：数组字面量**

```typescript
function combine<const T extends string[]>(...parts: T): string {
  return parts.join("-");
}

const result = combine("a", "b", "c");
// result 的类型是 "a" | "b" | "c" 拼接成的联合类型？
// 不，是 "a-b-c" 这个精确的字面量！
```

> 💡 **什么时候用 const 类型参数**：当你的泛型函数期望接收字面量值，并且希望这些字面量类型被精确保留而不是被推断为宽泛的基础类型时，用它！

---

### 13.1.2 Using 声明（TS 5.2）

---

#### 13.1.2.1 语法：`using` 声明

`using` 是 TypeScript 5.2 引入的一个革命性特性 —— 它让 TypeScript 拥有了类似 Python `with` 语句、C# `using` 语句的资源管理能力。

```typescript
// 使用 using 声明来自动管理资源
function createResource() {
  const resource = acquireResource();
  return {
    get() { return resource; },
    [Symbol.dispose]() {
      releaseResource(resource);  // 离开作用域时自动调用
    }
  };
}

// 使用 using
function process() {
  using r = createResource();
  console.log(r.get());
  // 函数结束时，Symbol.dispose() 自动被调用！
  // 资源自动释放，不需要手动 try...finally
}
```

---

#### 13.1.2.2 `Symbol.dispose` 与 `Symbol.asyncDispose`

`using` 声明依赖于两个特殊的 Symbol：

```typescript
// 同步资源释放
Symbol.dispose

// 异步资源释放（用于 async 资源管理）
Symbol.asyncDispose
```

**示例：数据库连接池**

```typescript
class DBConnection {
  private connected = false;

  async connect() {
    this.connected = true;
    console.log("数据库连接已建立！");  // 输出: 数据库连接已建立！
  }

  async query(sql: string) {
    if (!this.connected) {
      throw new Error("Not connected!");
    }
    console.log(`执行 SQL: ${sql}`);  // 输出: 执行 SQL: SELECT * FROM users
  }

  [Symbol.asyncDispose]() {
    this.connected = false;
    console.log("数据库连接已关闭！");  // 输出: 数据库连接已关闭！
  }
}

async function processData() {
  using db = new DBConnection();
  await db.connect();
  await db.query("SELECT * FROM users");
  // 函数结束，Symbol.asyncDispose 自动调用
  // 不需要手动 await db.close()！
}

// 输出顺序：
// 数据库连接已建立！
// 执行 SQL: SELECT * FROM users
// 数据库连接已关闭！
```

---

#### 13.1.2.3 设计动机：资源管理需要「用完即释放」的语义；C# 的 `using`、Python 的 `with` 早已有此功能

在 TypeScript 5.2 之前，如果你想确保资源被正确释放，你需要写这样的代码：

```typescript
// ❌ 传统写法：手动 try...finally
function process() {
  const resource = acquireResource();
  try {
    // 使用 resource
    use(resource);
  } finally {
    releaseResource(resource);  // 忘记写 finally？资源泄漏！
  }
}
```

```typescript
// ✅ 现代写法：using 声明（TS 5.2+）
function process() {
  using resource = acquireResource();
  use(resource);
  // 函数结束，自动调用 Symbol.dispose()
}
```

`using` 声明的好处：

1. **更简洁**：不需要写 `try...finally`
2. **更安全**：资源一定会在作用域结束时释放，即使抛异常
3. **更直观**：代码意图一目了然

> 🔧 **谁需要这个特性**：任何涉及「获取资源 → 使用 → 释放」模式的开发者。比如数据库连接、文件句柄、锁、计时器、事件监听器等。

---

### 13.1.3 Isolated Declarations（TS 5.5）

---

#### 13.1.3.1 独立声明文件：解耦类型声明与实现

`Isolated Declarations` 是 TypeScript 5.5 引入的一个新特性，专门为大型代码库优化。

在大型项目里，TypeScript 做类型检查时有一个性能瓶颈：**类型文件之间有依赖关系，A 文件的类型检查可能需要等待 B 文件先完成**。这导致类型检查很难并行化。

`Isolated Declarations` 解决了这个问题 —— 它允许你写一个「独立的类型声明」，这个声明**不依赖于实现文件的类型信息**，可以单独进行类型检查。

```typescript
// ❌ 传统写法：类型推断依赖实现
// utils.ts
export function add(a: number, b: number) {
  return a + b;
}

// ❌ 如果你只想声明类型，不写实现，TypeScript 会报错
// 因为 TypeScript 通常需要通过实现来推断类型

// ✅ 独立声明：声明和实现完全分离
// 开启 isolatedDeclarations 后，TypeScript 要求每个导出都有显式类型注解
export function add(a: number, b: number): number;  // ← 显式类型注解
export function add(a: number, b: number) {
  return a + b;
}
```

开启 `isolatedDeclarations` 后，TypeScript 要求每个导出的函数/变量都必须有**显式的类型注解**（不能靠类型推断）：

```typescript
// ❌ 错误（isolatedDeclarations: true）：没有显式类型注解
export function add(a: number, b: number) {
  return a + b;
}
// Error: Under isolatedDeclarations, the return type of a publicly exported
// function must be an explicit type annotation.
```

---

#### 13.1.3.2 设计动机：大型项目中，类型检查必须按文件顺序等待依赖文件完成；独立声明让类型文件可以并行生成

```json
{
  "compilerOptions": {
    "isolatedDeclarations": true
  }
}
```

开启 `isolatedDeclarations` 后，TypeScript 要求每个导出的函数/变量都必须有**显式的类型注解**（不能靠类型推断）：

```typescript
// ✅ 正确：显式标注了返回类型
export function add(a: number, b: number): number {
  return a + b;
}

// ❌ 错误（isolatedDeclarations: true）：没有显式类型注解
export function add(a: number, b: number) {
  return a + b;
}
// Error: Under isolatedDeclarations, the return type of a publicly exported
// function must be an explicit type annotation.
```

这个限制的代价是：写代码时要多打几个字。但换来的是：**TypeScript 编译器可以并行处理每个文件的类型声明，显著提升大型 monorepo 的类型检查速度。**

> 🎯 **适合场景**：大型 monorepo 项目（几十上百个包），类型检查时间成为开发瓶颈的团队。

---

### 13.1.4 NoInfer（TS 5.4）

---

#### 13.1.4.1 语法：`NoInfer<T>`

`NoInfer` 是 TypeScript 5.4 引入的一个精密类型工具，它的语法超级简单，但用途非常精准。

```typescript
type NoInfer<T> = [T][T extends any ? 0 : never];
```

`NoInfer<T>` 的语义是：**「不要在这个位置推断 T。」**

---

#### 13.1.4.2 设计动机：某些场景下类型推断过于「激进」，导致泛型参数被扩大到不该有的范围；`NoInfer` 阻止在特定位置进行类型推断

看一个经典的「类型推断过度」问题：

```typescript
// ❌ 没有 NoInfer：defaultValue 被推断为 string | T
function processValue<T>(value: T, defaultValue: T | string) {
  return value ?? defaultValue;
}

// 当你传入 number 和 "default" 时：
const result = processValue(123, "default");
// result 被推断为 string | number，而不是 number！
// 因为 "default" 把 T 扩大成了 string | number
```

```typescript
// ✅ 使用 NoInfer：阻止 defaultValue 影响 T 的推断
function processValue<T>(value: T, defaultValue: NoInfer<T>) {
  return value ?? defaultValue;
}

// 现在：
const result = processValue(123, "default");
// Error: Argument of type 'string' is not assignable to parameter of type 'number'
// ✅ "default" 不能赋值给 number，因为 NoInfer<T> 阻止了推断被扩大
```

**实际应用场景：React 的 `useState`**

```typescript
// 假设一个自定义的 useState：
function useState<T>(initialValue: T | (() => T)): [T, (value: T) => void] {
  // ...
}

// ❌ 没有 NoInfer：setState 可以接受比 T 更宽泛的类型
// setState(string) 可能会被接受，即使 T 是 number

// ✅ 使用 NoInfer：
function useState<T>(
  initialValue: NoInfer<T> | (() => NoInfer<T>)
): [T, (value: NoInfer<T>) => void] {
  // ...
}
// setState 现在严格要求传入 T 类型，不能传入更宽泛的类型
```

> 💡 **什么时候用 NoInfer**：当你发现泛型参数被「意外扩大」，导致类型检查不严格时，用 `NoInfer<T>` 包裹那些不应该影响泛型推断的参数。

## 13.2 TypeScript 5.5 ~ 5.9 核心新特性

TypeScript 5.5 ~ 5.9 这一系列版本，引入了一些对「日常开发体验」有显著提升的特性。让我们逐一来看。

### 13.1.5 小结

本节我们学习了 TypeScript 5.0 ~ 5.4 的核心新特性：

- **`const` 类型参数**：让泛型精确推断为字面量类型，不再被扩大为基础类型
- **`using` 声明 + `Symbol.dispose`/`Symbol.asyncDispose`**：自动资源管理，类似 Python `with` 和 C# `using`，再也忘不了写 `finally`
- **`Isolated Declarations`**：解耦类型声明与实现，让大型 monorepo 可以并行进行类型检查
- **`NoInfer<T>`**：阻止特定位置的泛型推断，解决「类型被意外扩大」的问题

这些都是 TypeScript 团队基于用户反馈精心设计的特性，每一个都解决了真实的开发痛点。下一节我们将学习 TypeScript 5.5 ~ 5.9 的新特性！

### 13.2.1 Predicate 改进（TS 5.5）

---

#### 13.2.1.1 自定义类型守卫函数的返回类型可以更精确地收窄联合类型成员

在 TypeScript 5.5 之前，类型守卫函数有时候不能精确地收窄联合类型。看看这个例子：

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

// ❌ TS 5.5 之前：Predicate 不够精确
function isCircle(shape: Shape): shape is { kind: "circle"; radius: number } {
  return shape.kind === "circle";
}

// 使用
function process(shape: Shape) {
  if (isCircle(shape)) {
    // TS 5.4 及之前：shape 的类型可能还是整个 Shape 联合类型
    // 不够精确！
    console.log(shape.radius);  // 可能报错
  }
}
```

TypeScript 5.5 改进了 Predicate 的类型收窄机制，让自定义类型守卫能够更精确地工作：

```typescript
// ✅ TS 5.5：Predicate 改进，类型收窄更精确
function isCircle(shape: Shape): shape is { kind: "circle"; radius: number } {
  return shape.kind === "circle";
}

function process(shape: Shape) {
  if (isCircle(shape)) {
    // ✅ TS 5.5：shape 被精确收窄为 { kind: "circle"; radius: number }
    console.log(shape.radius);  // 完美通过！
  }
}
```

**更复杂的例子：过滤联合类型**

```typescript
type AllShapes =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

// ✅ TS 5.5：类型守卫可以精确地从联合类型中挑出特定成员
function is2DShapeWithArea(shape: AllShapes): shape is
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number } {
  return shape.kind === "circle" || shape.kind === "square";
}

const shapes: AllShapes[] = [
  { kind: "circle", radius: 5 },
  { kind: "square", side: 4 },
  { kind: "triangle", base: 3, height: 4 }
];

// ✅ TS 5.5：filter + 类型守卫的组合更精确了
const shapesWithArea = shapes.filter(is2DShapeWithArea);
// shapesWithArea 的类型被精确收窄了！
```

---

### 13.2.2 Iterator Helper Methods（TS 5.6）

---

#### 13.2.2.1 在迭代器上新增 `.filter()`、`.map()` 等链式方法

TypeScript 5.6 为迭代器引入了一组链式方法，类似于数组的 `filter`、`map` 等，但作用于迭代器！

> 📝 **前置说明**：Iterator Helper Methods 是 TC39 Stage 2 提案（目前已是 Stage 2 或更高），属于 JavaScript 语言本身的特性，TypeScript 5.6 为其提供了完整的类型支持。这些方法需要宿主环境（浏览器、Node.js）本身实现了该提案后才能使用，在还不支持的环境中需要 polyfill。

```typescript
// TS 5.6：Iterator helpers（需要宿主环境支持，或使用 polyfill）
function* generateNumbers() {
  yield* [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
}

// ✅ filter：过滤
const evens = generateNumbers().filter(x => x % 2 === 0);
// evens 是一个迭代器，只产出偶数：2, 4, 6, 8, 10

// ✅ map：转换
const doubled = evens.map(x => x * 2);
// doubled 产出：4, 8, 12, 16, 20

// ✅ take：取前 N 个
const first3 = doubled.take(3);
// first3 产出：4, 8, 12

// ✅ drop：跳过前 N 个
const rest = doubled.drop(2);
// rest 产出：12, 16, 20

// ✅ chain：串联多个迭代器
const chained = generateNumbers().chain([100, 200]);
// chained 产出：1, 2, 3, ..., 10, 100, 200

// ✅ reduce：聚合
const sum = generateNumbers().reduce((acc, x) => acc + x, 0);
// sum = 55

// ✅ toArray：转数组
const arr = generateNumbers().toArray();
// arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

**组合使用（链式调用）**

```typescript
const result = generateNumbers()
  .filter(x => x > 3)       // [4, 5, 6, 7, 8, 9, 10]
  .map(x => x * 2)           // [8, 10, 12, 14, 16, 18, 20]
  .take(3)                   // [8, 10, 12]
  .toArray();                // [8, 10, 12]
```

> 🚀 **性能优势**：迭代器是惰性的（lazy），不会一次性把数据加载到内存。而数组的 `filter`/`map` 是急性的（eager），会立即创建一个新数组。在处理大数据集时，迭代器的内存效率远高于数组。

> ⚠️ **兼容性问题**：Iterator Helper Methods 是相对较新的 JS 提案。如果你的代码需要跑在旧版浏览器或旧版 Node.js 上，使用前请确认目标环境是否支持，或者使用 `core-js` 等 polyfill 库。

---

### 13.2.3 import defer（TS 5.9）

---

#### 13.2.3.1 延迟导入的语法糖

`import defer` 是 TypeScript 5.9 引入的一个语法特性（参见第11章 11.2.2 节），它允许你「声明式地声明我要导入什么，但实际导入行为由 bundler 决定」。

```typescript
// TS 5.9+：使用 import defer
import defer { someFunction } from "./module";

// 这个导入的效果取决于 bundler 如何处理 defer：
// - bundler 可能决定现在就加载（preload）
// - 或者等到第一次使用时再加载（lazy load）
```

> 📖 详细的 `import defer` 语法和应用场景，请参考第 11 章 11.2.2 节。

---

### 13.2.4 tsc --init 精简（TS 5.9）

---

#### 13.2.4.1 详见第 12 章 12.1.2 节

`tsc --init` 命令在 TypeScript 5.9 中得到了大幅精简 —— 从 50+ 行注释化配置项变成了一个极简的推荐配置。详见第 12 章 12.1.2 节。

---

### 13.2.5 --module node20（TS 5.9）

---

#### 13.2.5.1 详见第 12 章 12.2.2 节

TypeScript 5.9 新增了 `--module Node20` 配置，专门用于 Node.js 20+ 的原生 ESM 模式。详见第 12 章 12.2.2 节。

### 13.2.6 小结

本节我们学习了 TypeScript 5.5 ~ 5.9 的新特性：

- **Predicate 改进**：自定义类型守卫的收窄更精确，filter + 类型守卫的组合更强大
- **Iterator Helper Methods**：在迭代器上实现链式 `filter`/`map`/`take`/`drop` 等操作，惰性求值，内存效率更高（需宿主环境支持）
- **import defer**：延迟导入的声明式语法，bundler 决定加载时机
- **tsc --init 精简** 和 **--module node20**：开发体验和 Node.js 支持的持续改进

下一节我们将进入 TypeScript 6.0 的新特性！

## 13.3 TypeScript 6.0 核心新特性

TypeScript 6.0 是 TypeScript 发展史上的一个重要转折点 —— 它不仅是功能上的更新，更是底层架构的一次重大改变。

### 13.3.1 无 this 使用的方法语法上下文推断优化

---

#### 13.3.1.1 详见第 8 章 8.4.5 节

TypeScript 6.0 对「无 `this` 使用的方法」进行了上下文推断优化。当 TypeScript 检测到一个方法内部没有使用 `this` 时，会采用更宽松的上下文类型推断，减少不必要的类型约束。

> 📖 详细内容请参考第 8 章 8.4.5 节。

---

### 13.3.2 Subpath Imports 以 #/ 开头

---

#### 13.3.2.1 详见第 11 章 11.2.3 节

TypeScript 6.0 引入了以 `#/` 开头的 Subpath Imports 语法，这是一种新的导入路径规范，允许更精确地导入包的子路径。

> 📖 详细内容请参考第 11 章 11.2.3 节。

---

### 13.3.3 Combining --moduleResolution bundler with --module commonjs

---

#### 13.3.3.1 详见第 11 章 11.3.3 节

TypeScript 6.0 解锁了一个之前不可能的组合：`module: "commonjs"` 配合 `moduleResolution: "bundler"`。这对于从 CommonJS 迁移到 ESM 的项目非常有价值。

> 📖 详细内容请参考第 11 章 11.3.3 节。

---

### 13.3.4 --stableTypeOrdering flag

---

#### 13.3.4.1 背景：TypeScript 内部用类型 ID（出现顺序）排序联合类型成员

在 TypeScript 的内部实现中，联合类型（Union Types）的成员是按「类型 ID」排序的，这个 ID 是类型在编译过程中首次出现的顺序。

这意味着：

```typescript
type Mixed = string | number | boolean | null;
// 顺序取决于它们在类型检查过程中「第一次出现」的顺序
```

这个顺序会影响到 `.d.ts` 输出文件的类型顺序，进而影响：

- **代码 diff 的可读性**：不同文件顺序导致的 diff 不稳定
- **库的发布**：每次发布的 `.d.ts` 可能顺序不一致
- **代码审查**：审查 `.d.ts` 变更时，顺序噪音会干扰真正重要的变化

---

#### 13.3.4.2 问题：不同文件顺序导致 .d.ts 输出顺序不确定，影响 diff 稳定性

在大型 monorepo 中，这个问题特别明显：

```
// 文件 A.ts
type MyUnion = string | number | boolean;

// 文件 B.ts
type MyUnion = boolean | string | number;
```

在 TypeScript 内部，这两个文件的 `MyUnion` 类型成员可能因为「文件检查顺序」不同而产生不同的 ID 排序。这导致在输出 `.d.ts` 时，同一个联合类型的成员顺序不确定。

---

#### 13.3.4.3 作用：开启后使用稳定的语义排序替代 ID 排序

TypeScript 6.0 引入了 `--stableTypeOrdering` 标志：

```bash
tsc --stableTypeOrdering
```

```json
{
  "compilerOptions": {
    "stableTypeOrdering": true
  }
}
```

开启后，TypeScript 会使用**稳定的语义排序**（按字母顺序或按类型优先级）来排列联合类型成员，而不是按内部 ID 排序：

```typescript
// 开启 stableTypeOrdering 后，顺序是稳定的：
type Mixed = boolean | null | number | string;
// 按字母顺序：boolean → null → number → string
```

---

#### 13.3.4.4 应用：多文件声明合并输出的稳定性，对库发布和代码审查有意义

```bash
# 不开启 stableTypeOrdering
# 每次构建 .d.ts 顺序可能不一样
tsc --build

# 开启 stableTypeOrdering
# 每次构建 .d.ts 顺序一致，diff 更干净
tsc --build --stableTypeOrdering
```

> 🎯 **适合场景**：
>
> - **npm 库发布者**：每次发版时 `.d.ts` 的 diff 更干净，用户能看到真正变化的类型
> - **大型 monorepo**：多包之间的类型合并输出更稳定
> - **代码审查自动化**：减少 `.d.ts` diff 的噪音

---

### 13.3.5 import() 断言废弃

---

#### 13.3.5.1 详见第 11 章 11.2.5 节

TypeScript 6.0 废弃了 `import()` 类型断言的旧语法（`import assertion`），改用新的 `import attributes` 语法。

> 📖 详细内容请参考第 11 章 11.2.5 节。

---

### 13.3.6 TypeScript 6.0 与 7.0 的关系

---

#### 13.3.6.1 TS 6.0 是最后一个基于当前 JS 代码库的版本

TypeScript 6.0 是最后一个基于 **TypeScript 团队用 TypeScript/C++ 写的编译器代码库**的版本。

从 6.0 开始，TypeScript 团队宣布将启动一个雄心勃勃的计划：**用 Go 语言重写 TypeScript 编译器**。

#### 13.3.6.2 TS 7.0 基于 Go 语言重写的编译器，带来原生多线程和性能提升

TypeScript 7.0 预计将带来：

| 改进点 | 当前编译器（TS 6.x）| 新编译器（TS 7.0 Go版）|
|---|---|---|
| 语言 | TypeScript/C++ | Go |
| 并行化 | 有限 | 原生多线程支持 |
| 编译速度 | 较快 | 预计 5-10 倍提升 |
| 内存占用 | 较高（Node.js 运行时）| 预计更低（原生二进制）|
| 跨平台 | 受限于 Node.js | 更好的跨平台支持 |

> 📅 **关于 TS 7.0 的 Go 重写**：这是 TypeScript 团队公布的长期路线图计划，将用 Go 语言重写编译器以获得原生多线程支持和巨大的性能提升。该计划一旦实现，将对**普通使用者完全透明** —— 你的 `.ts` 代码完全不需要改动，但编译速度和增量构建速度将会有质的飞跃，CI/CD 构建时间大幅缩短！不过请注意，TS 7.0 的具体发布时间和细节请以 TypeScript 官方公告为准。

---

### 13.3.7 小结

本节我们学习了 TypeScript 6.0 的新特性和未来展望：

- **无 this 方法的上下文推断优化**：让没有使用 `this` 的方法享受更宽松的类型检查
- **Subpath Imports `#/`**：新的子路径导入语法
- **moduleResolution bundler + module commonjs 组合**：解锁新的迁移路径
- **stableTypeOrdering**：让 `.d.ts` 输出的联合类型顺序稳定，减少代码审查噪音
- **import() 断言废弃**：向新的 import attributes 语法迁移
- **TS 7.0 展望**：Go 语言重写编译器，原生多线程，编译速度 5-10 倍提升

TypeScript 6.0 是一个「承上启下」的版本 —— 它在继续完善当前编译器的同时，也为即将到来的 Go 重写做好了铺垫。

---

## 本章小结

### TypeScript 5.x ~ 6.x 版本新特性总览

| 版本 | 特性 | 实用指数 |
|---|---|---|
| TS 5.0 | `const` 类型参数 | ⭐⭐⭐⭐⭐ |
| TS 5.2 | `using` 声明 + `Symbol.dispose` | ⭐⭐⭐⭐⭐ |
| TS 5.4 | `NoInfer<T>` | ⭐⭐⭐⭐ |
| TS 5.5 | Predicate 改进 | ⭐⭐⭐⭐ |
| TS 5.5 | `isolatedDeclarations` | ⭐⭐⭐⭐ |
| TS 5.6 | Iterator Helper Methods | ⭐⭐⭐⭐⭐ |
| TS 5.9 | `import defer` | ⭐⭐⭐ |
| TS 5.9 | `tsc --init` 精简 | ⭐⭐⭐⭐ |
| TS 5.9 | `--module Node20` | ⭐⭐⭐⭐ |
| TS 6.0 | `stableTypeOrdering` | ⭐⭐⭐⭐ |
| TS 6.0 | Subpath Imports `#/` | ⭐⭐⭐ |
| TS 6.0 | module bundler + commonjs 组合 | ⭐⭐⭐⭐ |
| TS 7.0 | Go 重写编译器（预计）| ⭐⭐⭐⭐⭐ |

### 重点推荐学习的特性

1. **`const` 类型参数**（TS 5.0）：日常开发中高频使用，让泛型精确推断为字面量
2. **`using` 声明**（TS 5.2）：资源管理的革命性改进，必学！
3. **Iterator Helper Methods**（TS 5.6）：惰性数据处理，性能优化利器
4. **`stableTypeOrdering`**（TS 6.0）：库开发者和大型 monorepo 必开

### 版本迁移建议

```
从 TS 4.x 迁移到 TS 5.x：
  ├── 检查是否有使用了被废弃的 API
  ├── 逐步开启 strict: true
  ├── 享受 const 类型参数带来的精确类型推断
  └── 对于使用装饰器的项目：保留 experimentalDecorators

从 TS 5.x 迁移到 TS 6.x：
  ├── 检查 import() 断言语法，改用 import attributes
  ├── 尝试开启 stableTypeOrdering（.d.ts 发布者推荐）
  ├── 体验 moduleResolution bundler + commonjs 的新组合
  └── 展望 TS 7.0：Go 编译器带来的性能革命
```

> 🎉 **恭喜你完成了第 13 章的学习！** TypeScript 的版本演进一直以「用户痛点」为驱动，每一个新特性都解决的是真实的开发问题。持续关注这些新特性，能让你的 TypeScript 技能栈始终保持最新状态！
