+++
title = "TypeScript 速查表"
linkTitle = "TS 速查表"
weight = 2
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "面向「已经会编程」的 TypeScript 6.0 速查表：一页一个主题，表格 + tabpane 标签页，专治『我记得 TS 里能干这个，但忘了怎么写』"
isCJKLanguage = true
draft = false
+++

# TypeScript 速查表

这不是教程，是**字典**。教程教你走路，字典只在你卡住时递上一根拐杖。所以本页写得密、写得短、写得没什么耐心——每一条都假设你已经会编程，只是记不清 TypeScript 里这个动作该怎么写。

风格上参考 [Rust Language Cheat Sheet](https://cheats.rs/)，但内容完全按 TypeScript 重写：TS 的类型系统是**图灵完备**的、类型在运行时**完全不存在**、结构化类型带来了一堆「看起来能过、其实错得离谱」的兼容，还有一整套只存在于类型层面的编程技巧。照搬没有意义，该不一样的地方就让它不一样。

> **版本基线**：**TypeScript 6.0.3**（本机 `tsc --version` 实测），示例默认按 TS 6.0 的**新默认值**编写——`strict` 已默认开启、`target` 已默认 `ES2025`。凡 TS 5.x 才引入的特性标 🆕，凡 6.0 中**已废弃**的写法标 🗑️ 并给出替代方案。

{{% alert title="为什么基线必须是 6.0" color="warning" %}}
TypeScript 6.0 是**最后一个基于 JavaScript 代码库的版本**，也是通往 7.0（Go 重写的原生编译器）的桥梁。它的主要目的就是**对齐 7.0 行为**，因此大量 5.x 时期的惯用配置在 6.0 里已经报废弃错误（`TS5101` / `TS5107`），到 7.0 会**彻底失效**。

本速查表所有涉及「默认值」和「废弃项」的断言，都在 TS 6.0.3 上**实际跑过**，不是抄来的。
{{% /alert %}}

---

## 图例说明

| 符号 | 含义 |
| --- | --- |
| 🔥 | 高频使用，值得先记住 |
| ⚠️ | 陷阱或易错点，踩过一次就该记住 |
| 🛑 | 错误示例，故意写错给你看 |
| 🆕 | TS 5.x 引入的特性，在 6.0 中可用 |
| 🗑️ | **在 6.0 中已废弃**，7.0 将移除；标了替代写法 |
| 🚧 | 有限制、仍在演进，或需要额外开关 |
| 🝖 | 偏深的内容，第一遍可以跳过 |
| 💭 | 笔者见解，不是官方定论 |
| ↪ | 等价写法或语法糖展开 |
| 📘 | 指向官方文档或权威资料 |

> **关于 `// ✅` / `// ❌` 注解**：它们标的是**编译器实际行为**。标 `// ❌ TS2322:` 的地方写的是真实错误码，可以在 [09 诊断与错误码]({{< relref "09-Diagnostics-and-Error-Codes.md" >}}) 里反查。注释使用中文，但**代码标识符与报错原文保持英文**，方便直接搜索。

---

## 目录导航

### 第一层：语法主干

| 主题 | 内容一句话 |
| --- | --- |
| [01 起步与工具链]({{< relref "01-Quickstart-and-Tooling.md" >}}) | 装什么、五种跑法、`tsc` 命令行全表、诊断参数 |
| [02 类型系统主干]({{< relref "02-Type-System-Core.md" >}}) | 原始类型全表、`any`/`unknown`/`never` 之辨、类型运算符、内置工具类型 |
| [03 收窄与类型守卫]({{< relref "03-Narrowing-and-Type-Guards.md" >}}) | 控制流分析全表、`typeof` 返回值映射、自定义守卫、穷尽性检查 |
| [04 函数、对象与类]({{< relref "04-Functions-Objects-and-Classes.md" >}}) | 重载、`this`、函数变型表、索引签名、`#私有字段` vs `private` |
| [05 泛型与类型推断]({{< relref "05-Generics-and-Inference.md" >}}) | 约束、条件类型、`infer`、映射类型、变型标注、`NoInfer` |
| [06 类型层编程配方]({{< relref "06-Type-Level-Programming-Recipes.md" >}}) | 手写工具类型配方、递归技巧，以及**什么时候该收手** |
| [07 模块系统与声明文件]({{< relref "07-Modules-and-Declaration-Files.md" >}}) | ESM/CJS 互操作、解析策略矩阵、`.d.ts` 编写、声明合并 |

### 第二层：工程与配置

| 主题 | 内容一句话 |
| --- | --- |
| [08 tsconfig 全量参考]({{< relref "08-tsconfig-Reference.md" >}}) | 按类别分表、`strict` 逐项拆解、**6.0 废弃清单**、可直接抄的配置模板 |
| [09 诊断与错误码]({{< relref "09-Diagnostics-and-Error-Codes.md" >}}) | 高频 `TSxxxx` 错误码反查表、诊断参数、如何定位类型来源 |
| [10 异步与错误处理]({{< relref "10-Async-and-Error-Handling.md" >}}) | `Promise` 组合子类型、`Awaited`、`using`、错误类型建模 |
| [11 运行时校验与边界]({{< relref "11-Runtime-Validation-and-Boundaries.md" >}}) | 类型在运行时不存在——JSON、环境变量、API 边界怎么守住 |
| [12 测试]({{< relref "12-Testing.md" >}}) | 类型断言测试、mock 类型安全、各测试运行器的类型接入 |

### 第三层：落地场景

| 主题 | 内容一句话 |
| --- | --- |
| [13 发布带类型的库]({{< relref "13-Publishing-Libraries-with-Types.md" >}}) | `exports` 与 `types` 字段、双发布、声明产物、类型 API 的语义化版本 |
| [14 JSX 与前端类型模式]({{< relref "14-JSX-and-Frontend-Type-Patterns.md" >}}) | 组件与事件类型、`useRef`/`useState` 推断陷阱、CSS 模块声明 |
| [15 从 JS 迁移与生态互操作]({{< relref "15-Migrating-JS-to-TS-and-Ecosystem-Interop.md" >}}) | 渐进迁移路线、无类型依赖处理、`any` 治理、lint 边界 |
| [16 血泪速查]({{< relref "16-Pitfalls-and-Gotchas.md" >}}) | 按**症状**索引的踩坑表：你这么写 / 实际发生什么 / 正确写法 |
| [17 编译器与性能]({{< relref "17-Compiler-Internals-and-Performance.md" >}}) | 编译变慢怎么查、项目引用、`isolatedDeclarations`、TS 7.0 迁移前瞻 |

---

## 心智模型：先建立这五条

TypeScript 的坑，九成来自没建立下面这几个模型。先把它们背下来，往后每一页都会轻松很多。

### 一、类型在运行时**不存在**

这是最重要的一条。`tsc` 做的所有事情——检查、推断、报错——都发生在**编译期**；它产出的 JavaScript 里**一个类型都不剩**。

```typescript
interface User { name: string; age: number }

function greet(u: User) {
  return `Hello, ${u.name.toUpperCase()}`;
}

// 编译产物（注意类型标注全部消失）
// function greet(u) {
//   return `Hello, ${u.name.toUpperCase()}`;
// }
```

推论（每一条都导致过生产事故）：

| 推论 | 后果 |
| --- | --- |
| 类型不能做运行时判断 | `if (typeof x === "User")` 永远不成立 🛑 |
| 类型不能校验外部数据 | `fetch()` 回来的 JSON 转成 `User` 只是**你说了算** |
| 类型不影响性能 | 泛型、交叉类型、条件类型都不产生运行时开销 |
| 类型不能保护 `any` 进来的东西 | 类型断言是**许愿**，不是转换 |

> 这就是为什么本速查表专门有 [11 运行时校验与边界]({{< relref "11-Runtime-Validation-and-Boundaries.md" >}})——**类型系统管不到数据入口**，那一层只能靠运行时校验。💭

### 二、结构化类型：看形状，不看名字

TS 用的是**结构化类型**（structural typing），也叫「鸭子类型」：只要形状对得上，就认为类型兼容，**类型叫什么名字、在哪定义的都不重要**。

```typescript
interface Point { x: number; y: number }
class Vec2 { constructor(public x: number, public y: number) {} }

const v: Point = new Vec2(1, 2);   // ✅ 合法！Vec2 从没声明 implements Point
```

这跟 Java/C#/Swift 的**名义类型**（nominal typing）截然相反，好处是灵活，代价是：

| 反直觉现象 | 说明 |
| --- | --- |
| 两个无关类型可以互相赋值 | 只要结构兼容 |
| 少几个属性也能赋值 | 目标类型只要求「至少有哪些属性」 |
| 多出来的属性有时却报错 | 这叫**多余属性检查**，只对**对象字面量**生效，见 [04]({{< relref "04-Functions-Objects-and-Classes.md" >}}) |
| 想把它们区分开很难 | 需要**品牌类型**（branded type）人为加一个私有标记 |

### 三、类型空间与值空间是两套东西

同一个名字 `Foo` 可以**同时**是类型和值，也可以只是其中之一。理解这个能解释大量「为什么这里写得那里写不得」：

```typescript
interface Foo { a: number }        // 只有类型空间有 Foo
const Foo = { a: 1 };              // 值空间也有 Foo（与上面同名，互不冲突）
type T = Foo;                      // ✅ 用类型
const v = Foo;                     // ✅ 用值

class Bar { a = 1 }                // Bar 同时在两个空间
type TB = Bar;                     // ✅ 类型
const b = new Bar();               // ✅ 值
type I = InstanceType<typeof Bar>; // ✅ 从值空间取回类型
```

最典型的踩坑是 **`typeof` 有两副面孔**：

| 写法 | 位置 | 含义 |
| --- | --- | --- |
| `typeof x === "string"` | 表达式（值空间） | 运行时判断，返回 `boolean` |
| `type T = typeof x` | 类型位置（类型空间） | 编译期取 `x` 的**类型** |

```typescript
const config = { host: "localhost", port: 8080 };

type Config = typeof config;   // { host: string; port: number }
type Wrong  = typeof config === "object";  // ❌ 类型位置不能写比较表达式
```

### 四、类型注解是**约束**，不是**保证**

```typescript
const data: User = await res.json();  // ⚠️ 这里没有任何检查发生
```

`res.json()` 返回 `any`，把 `any` 赋给 `User` **不会报错**，因为 `any` 可以赋给任何类型。运行时数据长什么样，TS 一无所知。

安全与不安全的入口对照：

| 入口 | 静态类型 | 真实安全 |
| --- | --- | --- |
| 你自己 new 出来的对象 | ✅ | ✅ |
| 类型化库的返回值 | ✅ | ✅（取决于库） |
| `JSON.parse` / `res.json()` | ❌ `any` | ❌ |
| `localStorage.getItem` | ❌ `string \| null` | ❌ |
| `process.env.X` | ❌ `string \| undefined` | ❌ |
| 表单输入、URL 参数 | ❌ | ❌ |

### 五、TS 是**不完备**的：有漏洞，也有误报

TS 的设计目标里明确写着「**不追求类型系统完备性**」，它优先考虑的是「能很好地描述 JavaScript 里真实存在的模式」。所以：

| 现象 | 例子 |
| --- | --- |
| 有安全漏洞（unsound） | 数组协变：`string[]` 可以赋给 `(string \| number)[]`，写进去就炸 |
| 有故意留的口子 | `any`、`as`、非空断言 `!`、`@ts-ignore` |
| 有时会误报 | 复杂泛型推断失败，需要手写类型参数 |
| 有时会漏报 | 索引访问、稀疏数组、可变性 |

对待漏洞的正确态度：**知道它们在哪，用在明确知道安全的边界上**，而不是当成日常工具。`as` 用多了，你就只是写了个带注解的 JavaScript。💭

---

## 你好，TypeScript

先让第一行代码跑起来。TS 本身**不能直接运行**——它要么被编译成 JS，要么由运行时/工具即时擦除类型。

{{< tabpane text=true persist=disabled >}}

{{% tab header="tsc 编译（最标准）" %}}

最原始也最可靠的路径：编译成 `.js` 再交给 Node 跑。

```bash
npm install -D typescript
npx tsc --init              # 生成 tsconfig.json
npx tsc                     # 按 tsconfig 编译
node dist/index.js          # 运行产物
```

只想类型检查、不要产物——这是**最常用的命令**，CI 里必加：

```bash
npx tsc --noEmit            # 只检查，不输出任何文件
```

好处是行为完全可控、产物可用于生产；坏处是多一步编译。

{{% /tab %}}

{{% tab header="Node 原生运行 🆕" %}}

**Node.js 22.18+ / 24** 可以直接跑 `.ts` 文件：类型标注在加载时被**擦除**（strip），不生成 `.js`。

```bash
node index.ts               # 直接运行，无需任何依赖
```

实测于 Node **v24.20.0**：

| 语法 | 能否直接跑 | 原因 |
| --- | --- | --- |
| 类型注解、`interface`、`type` | ✅ | 纯擦除 |
| `import type` / `export type` | ✅ | 纯擦除 |
| `as` 断言、非空断言 `!` | ✅ | 纯擦除 |
| `declare` 声明 | ✅ | 纯擦除 |
| **`enum`**、带运行时代码的 **`namespace`** | ❌ `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` | 需要**转换**而非擦除 |
| 构造函数参数属性 `constructor(public a)` | ❌ | 会生成运行时代码 |

要跑 `enum` 得换开关（会打 `ExperimentalWarning`）：

```bash
node --experimental-transform-types index.ts
```

> 想让代码**必然**能被 Node 直接跑，就打开 [`erasableSyntaxOnly`]({{< relref "08-tsconfig-Reference.md" >}})：它会让 `tsc` 主动报错禁止所有非擦除语法（错误码 `TS1294`）。这是 5.8 引入、为「Node 原生跑 TS」时代准备的开关。🚧

{{% /tab %}}

{{% tab header="tsx / ts-node（开发期）" %}}

不想每次手动编译时用它们，改完直接跑，内部即时转译。

```bash
npx tsx index.ts            # 推荐：基于 esbuild，快，ESM 支持好
npx ts-node index.ts        # 老牌，配置项多，ESM 支持历史上比较绕
npx ts-node --esm index.ts  # ESM 模式（新版可省略）
```

| 工具 | 特点 | 适合 |
| --- | --- | --- |
| `tsx` | 快、零配置、ESM/CJS 都能跑 | 本地开发、脚本 🔥 |
| `ts-node` | 走完整 `tsc` 类型检查，配置项多 | 需要类型检查后再跑 |
| `node --watch` | Node 自带热重启 | 配合上面任一使用 |

> ⚠️ 两者**都可能不做类型检查**（`tsx` 默认不检查）。类型错误要靠编辑器或 `tsc --noEmit` 兜住，别指望运行器。

{{% /tab %}}

{{% tab header="打包器 / 测试运行器" %}}

现代前端和全栈项目里，TS 通常由 Vite、Next.js、Vitest 等工具的转译管线处理，你**从不手动执行 `tsc`**。

| 场景 | 谁负责转译 | 类型检查由谁做 |
| --- | --- | --- |
| Vite / Vitest | esbuild / Rollup | 单独的 `tsc --noEmit` 或 `vue-tsc` |
| Next.js | SWC | `next build` 内置，或单独的 `tsc --noEmit` |
| Bun | Bun 内置转译 | `bun run --bun tsc --noEmit` |
| esbuild / SWC 单独使用 | 该工具 | 只能靠 `tsc` |

> ⚠️ **关键认知**：esbuild、SWC、Bun 这类工具**只擦除类型，不做类型检查**。它们追求的是速度，类型错误它们压根不看。所以「构建成功」不等于「类型正确」，CI 里必须单独有一个 `tsc --noEmit` 步骤。这是新手最常见的误解之一。

{{% /tab %}}

{{< /tabpane >}}

---

## 「零配置」下 TS 6.0 已经替你开了什么

6.0 最大的变化之一是**默认值大幅变严**。如果你不写 `tsconfig.json`（或写个空的 `{}`），实际生效的是这些——全部在 **TS 6.0.3 实测**：

| 选项 | 5.x 默认 | **6.0 默认** | 影响 |
| --- | --- | --- | --- |
| `strict` | `false` | **`true`** 🔥 | 隐式 `any`、`null` 检查全部开启 |
| `target` | `ES5`（早期）/ 随版本浮动 | **`ES2025`**（`LatestStandard`） | 产物直接用现代语法 |
| `jsx` | — | `preserve` | 保留 JSX 交给下游 |
| `types` | 自动加载全部 `@types/*` | **`[]` 空** ⚠️ | **不会自动加载 `@types/node` 了！** |

`types` 这一条最坑：6.0 起不再自动把 `node_modules/@types` 下**所有**包塞进全局，于是升级后常见「突然找不到 `process` / `Buffer` / `describe`」：

```jsonc
// ❌ 升级 6.0 后报：Cannot find name 'process'
{ }

// ✅ 显式声明要哪些全局类型包
{ "compilerOptions": { "types": ["node"] } }
```

> 完整的 6.0 废弃与默认值变更清单，连同可直接抄的配置模板，都在 [08 tsconfig 全量参考]({{< relref "08-tsconfig-Reference.md" >}})。

---

## TypeScript 6.0 废弃速览

这些在 6.0 里**已经报错**（不是警告），必须改。报错码：`TS5101`（选项废弃）、`TS5107`（取值废弃）。

| 🗑️ 废弃写法 | 报错 | 替代 |
| --- | --- | --- |
| `target: "ES5"` | `TS5107` | 最低 `ES2015`；真要 ES5 得用别的编译器 |
| `moduleResolution: "node"` / `"node10"` | `TS5107` | 打包器项目用 `"bundler"`，Node 项目用 `"nodenext"` |
| `module: "amd"` / `"umd"` / `"systemjs"` / `"none"` | `TS5107` | ESM + 打包器 |
| `baseUrl` | `TS5101` | 把前缀写进每条 `paths` 里 |
| `outFile` | `TS5101` | 用 esbuild / Rollup / Vite 等外部打包器 |
| `downlevelIteration` | `TS5101` | 只在 ES5 产物下有意义，直接删 |
| `esModuleInterop: false` / `allowSyntheticDefaultImports: false` | `TS5107` | 互操作恒定开启，删掉该行 |
| `alwaysStrict: false` | `TS5107` | 所有代码恒为严格模式，删掉该行 |
| `import ... assert { }`（含 `import()` 形式） | `TS2880` | 改用 `with { type: "json" }` |

临时续命（**仅作迁移过渡**，7.0 会彻底移除）：

```jsonc
{ "compilerOptions": { "ignoreDeprecations": "6.0" } }
```

> 官方迁移信息汇总：`tsc` 报错里会直接给出 `https://aka.ms/ts6` 📘

---

## 版本时间线速查

| 版本 | 关键特性 | 本表位置 |
| --- | --- | --- |
| **4.9** | `satisfies` 运算符 | [02]({{< relref "02-Type-System-Core.md" >}}) |
| **5.0** | `const` 类型参数、标准装饰器、`extends` 多配置继承 | [05]({{< relref "05-Generics-and-Inference.md" >}}) |
| **5.1** | 关联访问的推断改进、Getter/Setter 类型可不同 | [04]({{< relref "04-Functions-Objects-and-Classes.md" >}}) |
| **5.2** | `using` / `await using` 显式资源管理 | [10]({{< relref "10-Async-and-Error-Handling.md" >}}) |
| **5.3** | 类型收窄与 `switch` 的改进 | [03]({{< relref "03-Narrowing-and-Type-Guards.md" >}}) |
| **5.4** | `NoInfer<T>`、闭包收窄改进 | [05]({{< relref "05-Generics-and-Inference.md" >}}) |
| **5.5** | **推断的类型谓词**、`isolatedDeclarations` | [03]({{< relref "03-Narrowing-and-Type-Guards.md" >}}) |
| **5.6** | 禁止可疑的内建迭代、严格内建迭代器检查 | [16]({{< relref "16-Pitfalls-and-Gotchas.md" >}}) |
| **5.7** | 更长的相对路径不再被当作错误、`never` 初始化检查 | [09]({{< relref "09-Diagnostics-and-Error-Codes.md" >}}) |
| **5.8** | `erasableSyntaxOnly`、`require()` 的 ESM 支持 | [08]({{< relref "08-tsconfig-Reference.md" >}}) |
| **5.9** | 延迟导入、编辑器体验改进 | [07]({{< relref "07-Modules-and-Declaration-Files.md" >}}) |
| **6.0** | **`strict` 默认开启**、`target` 默认 ES2025、`types` 默认空、大面积废弃清理 | [08]({{< relref "08-tsconfig-Reference.md" >}}) |
| **7.0** | Go 重写的原生编译器（速度大幅提升），移除全部废弃项 | [17]({{< relref "17-Compiler-Internals-and-Performance.md" >}}) |

---

## 怎么用这份速查表

| 你的处境 | 从哪开始 |
| --- | --- |
| 刚接手一个 TS 项目 | [08 tsconfig]({{< relref "08-tsconfig-Reference.md" >}}) → [16 血泪速查]({{< relref "16-Pitfalls-and-Gotchas.md" >}}) |
| 报了个看不懂的错 | [09 错误码反查]({{< relref "09-Diagnostics-and-Error-Codes.md" >}}) |
| 要写复杂类型 | [05 泛型]({{< relref "05-Generics-and-Inference.md" >}}) → [06 配方]({{< relref "06-Type-Level-Programming-Recipes.md" >}}) |
| 接口报 `any` 相关警告 | [02 特殊类型]({{< relref "02-Type-System-Core.md" >}}) 的 `any`/`unknown` 一节 |
| 要处理接口返回的数据 | [11 运行时校验]({{< relref "11-Runtime-Validation-and-Boundaries.md" >}}) 🔥 |
| 要发一个 npm 包 | [13 发布带类型的库]({{< relref "13-Publishing-Libraries-with-Types.md" >}}) |
| 老 JS 项目要上 TS | [15 迁移]({{< relref "15-Migrating-JS-to-TS-and-Ecosystem-Interop.md" >}}) |
| 编译太慢 | [17 性能]({{< relref "17-Compiler-Internals-and-Performance.md" >}}) |


