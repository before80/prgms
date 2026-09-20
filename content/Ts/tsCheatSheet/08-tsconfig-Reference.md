+++
title = "08 tsconfig 全量参考"
weight = 108
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "按类别分表的编译选项参考、strict 逐项拆解、TypeScript 6.0 废弃清单与可直接抄的配置模板"
isCJKLanguage = true
draft = false
+++

# 08 tsconfig 全量参考

`tsconfig.json` 是 TypeScript 项目里**影响最大、又最容易抄错**的文件。本页按官方分类组织，重点是**6.0 的变化**。

> 本页所有「默认值」「报错码」「选项接受性」均在 **TypeScript 6.0.3** 用 `tsc --showConfig` 与真实编译实测确认。
>
> 官方完整选项列表：`typescriptlang.org/tsconfig` 📘

---

## TypeScript 6.0：先看这一段

6.0 是通往 7.0（Go 原生编译器）的桥梁，**主要目的就是对齐 7.0 行为**。升级时最容易踩的三类问题：

### 一、新默认值（会静默改变行为）

| 选项 | 5.x 默认 | **6.0 默认** | 后果 |
| --- | --- | --- | --- |
| `strict` | `false` | **`true`** 🔥 | 升级后可能一次爆出大量错误 |
| `target` | `ES5` / 浮动 | **`ES2025`**（`LatestStandard`） | 产物语法更现代 |
| `jsx` | — | `preserve` | 保留 JSX |
| `types` | 自动加载全部 `@types/*` | **`[]`** ⚠️ | **不再自动加载 `@types/node`** |
| `rootDir` | 从输入文件推断 | **不推断** | 产物路径可能多一层 |

### 二、两个高频「升级即报错」的症状

```text
error TS2304: Cannot find name 'process'.
```
→ `types` 默认为 `[]` 了。加：

```jsonc
{ "compilerOptions": { "types": ["node"] } }
```

```text
产物出现在 dist/src/index.js 而不是 dist/index.js
```
→ `rootDir` 不再推断。显式声明：

```jsonc
{ "compilerOptions": { "rootDir": "./src", "outDir": "./dist" } }
```

### 三、废弃选项（**报错**，不是警告）

| 🗑️ 废弃 | 报错码 | 替代方案 |
| --- | --- | --- |
| `target: "ES5"` | `TS5107` | 最低 `ES2015`；真要 ES5 得换编译器 |
| `moduleResolution: "node"` / `"node10"` | `TS5107` | `"bundler"`（打包器）或 `"nodenext"`（Node） |
| `module: "amd"` / `"umd"` / `"systemjs"` / `"none"` | `TS5107` | ESM + 打包器 |
| `baseUrl` | `TS5101` | 前缀折叠进每条 `paths` |
| `outFile` | `TS5101` | 外部打包器（esbuild / Rollup / Vite） |
| `downlevelIteration` | `TS5101` | 只在 ES5 产物下有意义，删掉 |
| `esModuleInterop: false` | `TS5107` | 互操作恒定开启，删掉该行 |
| `allowSyntheticDefaultImports: false` | `TS5107` | 同上 |
| `alwaysStrict: false` | `TS5107` | 所有代码恒为严格模式 |
| `import ... assert { }` | `TS2880` | 改用 `with { type: "json" }` |
| `/// <reference no-default-lib="true"/>` | 🗑️ | `noLib` / `libReplacement` |

**临时续命**（仅作迁移过渡，7.0 彻底移除）：

```jsonc
{ "compilerOptions": { "ignoreDeprecations": "6.0" } }
```

> ⚠️ `ignoreDeprecations` 是**临时止痛药**，不是解决方案。正确用法：① 先加上让项目能构建 → ② 修完新默认值问题 → ③ 逐个替换废弃选项 → ④ **删掉它**。删掉后能干净构建，就说明项目已为 7.0 做好准备。

---

## 严格性选项（Type Checking）

{{< tabpane text=true persist=disabled >}}

{{% tab header="strict 到底管哪些" %}}

`strict` 是一个**开关组**。它只包含下面这些（官方 `optionDeclarations` 分类实测）：

| 受 `strict` 控制的选项 | 检查什么 | 典型报错 |
| --- | --- | --- |
| `noImplicitAny` | 隐式 `any` | `TS7006` |
| `strictNullChecks` | `null` / `undefined` 可赋值性 | `TS2322` |
| `strictFunctionTypes` | 函数参数逆变 | `TS2322` |
| `strictBindCallApply` | `bind` / `call` / `apply` 参数 | `TS2345` |
| `strictPropertyInitialization` | 类属性必须初始化 | `TS2564` |
| `noImplicitThis` | 隐式 `any` 的 `this` | `TS2683` |
| `useUnknownInCatchVariables` | `catch` 变量为 `unknown` | `TS2322` |
| `alwaysStrict` | 输出 `"use strict"` | — |
| `strictBuiltinIteratorReturn` | 内建迭代器返回类型更严格 | 见 [16]({{< relref "16-Pitfalls-and-Gotchas.md" >}}) |

⚠️ **不在 `strict` 里但强烈建议开启的两个**（这是最常被误传的一点）：

| 选项 | 为什么不在 strict 里 | 建议 |
| --- | --- | --- |
| `noUncheckedIndexedAccess` | 会让大量现有代码报错 | ✅ **建议开** 🔥 |
| `exactOptionalPropertyTypes` | 语义变化较大 | ✅ 新项目建议开 |
| `noImplicitOverride` | 同上 | ✅ 建议开 |
| `noUnusedLocals` / `noUnusedParameters` | 属风格问题 | ⚠️ 交给 lint 更好 |
| `noImplicitReturns` | 同上 | ⚠️ 按团队口味 |
| `noFallthroughCasesInSwitch` | 同上 | ✅ 建议开 |

```jsonc
// 推荐的严格性配置（strict 之外再补几项）
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,   // 索引访问加 undefined 🔥
    "exactOptionalPropertyTypes": true, // 区分「缺省」与「值为 undefined」
    "noImplicitOverride": true,         // 覆盖基类必须写 override
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true // 副作用导入也检查（6.0 已默认开）
  }
}
```

> 🔥 **`noUncheckedIndexedAccess` 的正确理解**：它给**索引访问**的结果加上 `| undefined`。
>
> ```typescript
> declare const arr: string[];
> const a: string = arr[0];
> // ❌ TS2322: Type 'string | undefined' is not assignable to type 'string'.
>
> declare const d: Record<string, number>;
> const v: number = d["k"];
> // ❌ TS2322: Type 'number | undefined' is not assignable to type 'number'.
> ```
>
> ⚠️ **重要前提**：它**依赖 `strictNullChecks`**。如果 `strictNullChecks` 关闭，这个开关**静默失效**（因为类型系统里根本没有 `undefined` 类型可加）。这不是 bug，但会让你误以为开了就安全。

{{% /tab %}}

{{% tab header="受 strictNullChecks 约束的选项" %}}

有几个选项**不能脱离 `strictNullChecks` 单独使用**，否则报 `TS5052`：

```text
error TS5052: Option 'exactOptionalPropertyTypes' cannot be specified
              without specifying option 'strictNullChecks'.
error TS5052: Option 'strictPropertyInitialization' cannot be specified
              without specifying option 'strictNullChecks'.
```

| 选项 | 依赖 `strictNullChecks` |
| --- | --- |
| `exactOptionalPropertyTypes` | ✅ 必须 |
| `strictPropertyInitialization` | ✅ 必须 |
| `noUncheckedIndexedAccess` | ⚠️ 不报错，但静默失效 |

**`exactOptionalPropertyTypes` 到底改了什么**：

```typescript
type Opt = { a?: number };

// 默认（关闭时）：a?: number 等价于 number | undefined
const x: Opt = { a: undefined };   // ✅ 允许

// 开启后：a?: number 表示「可以没有 a」，但有了就必须是 number
const y: Opt = { a: undefined };
// ❌ TS2375: Type '{ a: undefined; }' is not assignable to type 'Opt'
//    with 'exactOptionalPropertyTypes: true'. Consider adding 'undefined'
//    to the types of the target's properties.
```

想同时允许「缺省」和「显式 undefined」：

```typescript
type Opt2 = { a?: number | undefined };   // ✅ 显式写出 undefined
const z: Opt2 = { a: undefined };         // ✅
```

{{% /tab %}}

{{% tab header="完整性检查" %}}

| 选项 | 作用 | 建议 |
| --- | --- | --- |
| `skipLibCheck` | **跳过 `.d.ts` 文件的类型检查** | ✅ **几乎总是开** 🔥 |
| `skipDefaultLibCheck` | 只跳过内置 `lib.*.d.ts` | 少见，已被 `skipLibCheck` 覆盖 |
| `noEmitOnError` | 有错就不产物 | ⚠️ 构建流水线里按需 |

```jsonc
{ "compilerOptions": { "skipLibCheck": true } }
```

> ⚠️ **关于 `skipLibCheck` 的正确认识**：
>
> | 常见误解 | 事实 |
> | --- | --- |
> | 「开了就不检查我的代码」 | ❌ 只跳过 `.d.ts`，**你的 `.ts` 照样全查** |
> | 「开了就失去类型安全」 | ⚠️ 只影响**依赖包声明文件之间**的冲突检查 |
> | 「不该开」 | ❌ 大型项目**不开会慢几倍**，且常被第三方 `.d.ts` 之间的冲突阻塞 |
>
> 它跳过的是「不同版本的 `@types` 互相不兼容」这类你**无法修复**的问题。**建议开**，但要知道它的边界：**你自己的 `.d.ts` 也不查了**。所以手写声明要额外仔细。

{{% /tab %}}

{{< /tabpane >}}

---

## 模块与解析（Modules）

| 选项 | 作用 | 6.0 状态 |
| --- | --- | --- |
| `module` | 产物模块格式 | `amd`/`umd`/`systemjs`/`none` 🗑️ 废弃 |
| `moduleResolution` | 解析策略 | `node`/`node10`/`classic` 🗑️ 废弃 |
| `rootDir` | 源码根目录 | ⚠️ **不再推断** |
| `outDir` | 产物目录 | — |
| `paths` | 路径别名 | ✅ `baseUrl` 废弃后前缀写这里 |
| `baseUrl` | 路径基准 | 🗑️ 废弃（`TS5101`） |
| `types` | 加载哪些 `@types` | ⚠️ **默认 `[]`** |
| `typeRoots` | `@types` 搜索根 | — |
| `resolveJsonModule` | 允许导入 `.json` | — |
| `allowImportingTsExtensions` | 允许 `import "./x.ts"` | 需配 `noEmit` 或用 `rewriteRelativeImportExtensions` |
| `rewriteRelativeImportExtensions` | 编译时把 `.ts` 改写成 `.js` | 🆕 5.7+ |
| `noUncheckedSideEffectImports` | 检查 `import "./x"` 是否存在 | 6.0 默认 **开** |
| `resolvePackageJsonExports` | 遵循 `exports` 字段 | `bundler`/`nodenext` 下默认开 |
| `customConditions` | 自定义 `exports` 条件 | 发库/多环境时用 |
| `allowUmdGlobalAccess` | 允许 UMD 全局访问 | 少见 |

**`module` 与 `moduleResolution` 的合法搭配** 🔥：

| 你写的是 | `module` | `moduleResolution` | 扩展名要求 |
| --- | --- | --- | --- |
| Node.js 库/服务 | `nodenext` | `nodenext` | ⚠️ ESM 下**必须写 `.js`** |
| Vite / Next / 打包器 | `esnext` | `bundler` | 不写扩展名 ✅ |
| 交给打包器、TS 只检查 | `preserve` | `bundler` | 不写扩展名 ✅ |
| 老 CJS 项目 | `commonjs` | `nodenext` | 不写扩展名 ✅ |

> ⚠️ `nodenext` 下写扩展名的规则最反直觉：**源文件是 `foo.ts`，导入要写 `"./foo.js"`**。原因是 `import` 语句原样保留到产物，运行时需要指向真实 `.js` 文件。见 [07 模块系统]({{< relref "07-Modules-and-Declaration-Files.md" >}})。

**`types` 的取舍**：

```jsonc
// 🛑 6.0 下不写 types，@types/node 不会被加载
{}

// ✅ 显式列出需要的全局类型包
{ "compilerOptions": { "types": ["node", "vitest/globals"] } }

// ⚠️ 恢复 5.x 的「全部加载」行为（不推荐，会拖慢编译）
{ "compilerOptions": { "types": ["*"] } }
```

| 场景 | `types` 怎么写 |
| --- | --- |
| Node 服务 | `["node"]` |
| Node + Vitest | `["node", "vitest/globals"]` |
| 浏览器 + Jest | `["jest"]` |
| 纯库（无全局依赖） | `[]`（默认即可）✅ 最好 |
| 不想管 | `["*"]`（性能代价） |

> 💭 **最佳实践是保持 `types: []`**，让每个文件显式 `import`。全局类型越少，编译越快，依赖关系越清晰。

---

## 目标与环境（Language and Environment）

| 选项 | 作用 | 说明 |
| --- | --- | --- |
| `target` | 产物 JS 版本 | 6.0 默认 `ES2025`；最低 `ES2015` |
| `lib` | 可用的内置类型库 | 不写则按 `target` 推导 |
| `jsx` | JSX 转换方式 | 6.0 默认 `preserve` |
| `jsxImportSource` | 新 JSX 运行时的导入源 | `react-jsx` 时用，如 `"react"` |
| `jsxFactory` | 经典 JSX 工厂函数 | `React.createElement` |
| `jsxFragmentFactory` | Fragment 工厂 | `React.Fragment` |
| `libReplacement` | 允许用自定义 lib 替换内置 | 6.0 默认 `false` |
| `noLib` | 不加载任何内置 lib | 极端场景 |
| `moduleDetection` | 如何判断文件是模块 | `force` 可避免「意外全局」 |
| `useDefineForClassFields` | 类字段用 `define` 语义 | `target` ≥ ES2022 时默认 `true` |
| `experimentalDecorators` | 旧版装饰器 | ⚠️ 与标准装饰器二选一 |
| `emitDecoratorMetadata` | 生成装饰器元数据 | 依赖 `experimentalDecorators` |

**`lib` 对照表**：

| `target` | 自动包含的 `lib` |
| --- | --- |
| `ES2025`（6.0 默认） | `lib.es2025.full.d.ts`（含 DOM） |
| `ES2022` | `lib.es2022.full.d.ts` |
| `ES2020` | `lib.es2020.full.d.ts` |
| `ES2015` | `lib.es2015.full.d.ts` |

```jsonc
// 手动指定 lib：想用 ES2023 的数组方法但要 DOM
{ "compilerOptions": { "target": "ES2020", "lib": ["ES2023", "DOM", "DOM.Iterable"] } }

// 后端项目：不要 DOM
{ "compilerOptions": { "lib": ["ES2023"] } }

// 前端项目：要 DOM + DOM.Iterable
{ "compilerOptions": { "lib": ["ES2023", "DOM", "DOM.Iterable"] } }
```

> ⚠️ **`lib` 决定「有哪些全局类型可用」，`target` 决定「产物语法」**，两者独立。常见错误是只改 `target` 却忘了 `lib`，导致新 API 的类型找不到（或反过来，类型有了但运行时环境不支持）。
>
> 💡 `DOM.Iterable` 让 `NodeList`、`HTMLCollection` 等支持 `for...of` 与展开。**前端项目建议总是带上**。

**关于装饰器**：TS 5.0 起支持**标准装饰器**（无需开关）。`experimentalDecorators` 是旧的实验版，两者语义不同，**不能混用**：

```jsonc
// 标准装饰器（新项目推荐）
{ "compilerOptions": {} }

// 旧版装饰器（Angular、TypeORM 等依赖元数据的框架需要）
{ "compilerOptions": { "experimentalDecorators": true, "emitDecoratorMetadata": true } }
```

---

## 产物（Emit）

| 选项 | 作用 |
| --- | --- |
| `noEmit` | 只检查不产物 🔥 |
| `outDir` | 产物目录 |
| `declaration` | 生成 `.d.ts` |
| `declarationMap` | 生成 `.d.ts.map`（能跳回源码） |
| `declarationDir` | `.d.ts` 单独目录 |
| `emitDeclarationOnly` | 只产 `.d.ts` |
| `sourceMap` | 生成 `.js.map` |
| `inlineSourceMap` | 内联 sourcemap |
| `inlineSources` | 把源码内联进 map |
| `removeComments` | 去掉注释 |
| `noEmitOnError` | 有错不产物 |
| `importHelpers` | 从 `tslib` 导入辅助函数 |
| `noEmitHelpers` | 不生成辅助函数 |
| `downlevelIteration` | 🗑️ 废弃 |
| `outFile` | 🗑️ 废弃，用打包器 |
| `preserveConstEnums` | 保留 `const enum` 的运行时对象 |
| `stripInternal` | 删除标了 `@internal` 的声明 |
| `newLine` | 换行符 `crlf` / `lf` |
| `emitBOM` | 输出 BOM |

```jsonc
// 库的典型产物配置
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,   // 使用者能跳回你的源码 🔥
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

> ⚠️ `stripInternal` 配合 `/** @internal */` 注释，可以把内部 API 从 `.d.ts` 里删掉。但**它只删声明，不删实现**——运行时那些 API 仍然存在，只是使用者没有类型。详见 [13 发布库]({{< relref "13-Publishing-Libraries-with-Types.md" >}})。

---

## 互操作约束（Interop Constraints）

| 选项 | 作用 | 6.0 状态 |
| --- | --- | --- |
| `isolatedModules` | 保证可单文件转译 | ✅ 建议开 |
| `verbatimModuleSyntax` | 类型必须用 `import type` | ✅ 建议开 🔥 |
| `erasableSyntaxOnly` | 禁止非擦除语法 | 🆕 5.8+，Node 直跑 TS 时开 |
| `isolatedDeclarations` | 要求显式返回类型，便于并行生成声明 | 🆕 5.5+，需 `declaration` 或 `composite` |
| `esModuleInterop` | CJS/ESM 互操作 | ⚠️ **恒为 true**，写 `false` 报 `TS5107` |
| `allowSyntheticDefaultImports` | 允许合成默认导入 | ⚠️ 恒为 true |
| `forceConsistentCasingInFileNames` | 大小写一致性 | ✅ 保持默认 `true` |
| `preserveSymlinks` | 保留符号链接 | 少见 |

```jsonc
// 现代项目的互操作配置
{
  "compilerOptions": {
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "erasableSyntaxOnly": true,       // 只在需要 Node 直跑时开
    "forceConsistentCasingInFileNames": true
  }
}
```

**`erasableSyntaxOnly` 会禁止这些语法**（实测报 `TS1294`）：

| 被禁语法 | 替代 |
| --- | --- |
| `enum` | 用 `as const` 对象 + 联合类型 🔥 |
| 带运行时代码的 `namespace` | 用 ES 模块 |
| 构造函数参数属性 `constructor(public a)` | 手写字段 + 赋值 |
| `import x = require()` | 用 `import` |

```typescript
// 🛑 erasableSyntaxOnly 下报 TS1294
export enum E { A }
export namespace N { export const x = 1; }
export class K { constructor(public a: number) {} }

// ✅ 替代写法
export const E = { A: "A" } as const;
export type E = (typeof E)[keyof typeof E];

export const N = { x: 1 };

export class K {
  a: number;
  constructor(a: number) { this.a = a; }
}
```

> 💭 打开 `erasableSyntaxOnly` 的一个附带好处：它**强迫你放弃 `enum`**，而 `enum` 本来就有不少坑（见 [16]({{< relref "16-Pitfalls-and-Gotchas.md" >}})）。用 `as const` 对象替代更符合 JS 习惯，且能被 Node 直接运行。

---

## 项目引用与增量（Projects）

| 选项 | 作用 |
| --- | --- |
| `composite` | 声明为可被引用的项目，强制 `declaration` |
| `incremental` | 增量编译，生成 `.tsbuildinfo` |
| `tsBuildInfoFile` | 指定 `.tsbuildinfo` 位置 |
| `references` | 引用其它项目（数组，含 `path`） |
| `disableSourceOfProjectReferenceRedirect` | 禁用源码重定向 |
| `disableReferencedProjectLoad` | 不自动加载被引用项目 |
| `disableSolutionSearching` | 减少 solution 搜索 |

```jsonc
// 根 tsconfig.json（solution 文件，只有引用不含源码）
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/web" }
  ]
}
```

```jsonc
// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src"]
}
```

```bash
npx tsc --build          # 按拓扑顺序增量构建
npx tsc --build --clean  # 清理
npx tsc --build --force  # 强制全量
```

> 💡 **项目引用适合 monorepo**：它让每个包独立检查、增量复用，大仓库能快很多。代价是配置变复杂，且必须开 `composite` + `declaration`。详见 [17 编译器与性能]({{< relref "17-Compiler-Internals-and-Performance.md" >}})。

---

## JavaScript 支持与迁移

| 选项 | 作用 |
| --- | --- |
| `allowJs` | 允许编译 `.js` |
| `checkJs` | 检查 `.js`（配合 `// @ts-check`） |
| `maxNodeModuleJsDepth` | 检查 `node_modules` 里 JS 的深度 |

```jsonc
// 迁移期配置
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "noEmit": true
  }
}
```

详见 [15 从 JS 迁移]({{< relref "15-Migrating-JS-to-TS-and-Ecosystem-Interop.md" >}})。

---

## 配置继承：extends

```jsonc
// tsconfig.base.json（团队共享）
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "target": "ES2022",
    "module": "esnext",
    "moduleResolution": "bundler",
    "skipLibCheck": true,
    "verbatimModuleSyntax": true
  }
}
```

```jsonc
// 各包继承
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": { "outDir": "./dist" },
  "include": ["src"]
}
```

| 规则 | 说明 |
| --- | --- |
| 相对路径 | 相对**配置文件自身**解析 |
| `compilerOptions` | 深合并，后者覆盖前者 |
| `files` / `include` / `exclude` | **整体覆盖**，不合并 ⚠️ |
| `references` | 覆盖 |
| 数组型选项 | 覆盖（如 `lib`、`types`） |
| 多重继承 | TS 5.0+ 支持 `extends: ["./a.json", "./b.json"]` 🆕 |

> ⚠️ **数组选项是覆盖不是合并**：父配置写了 `"lib": ["ES2023", "DOM"]`，子配置写 `"lib": ["ES2023"]`，结果是**只剩 `ES2023`**，DOM 类型全丢。

**从 npm 包继承**（团队共享配置的标准做法）：

```jsonc
{ "extends": "@tsconfig/strictest/tsconfig.json" }
{ "extends": "@tsconfig/node22/tsconfig.json" }
```

**查看最终生效配置**（排查继承问题必用）🔥：

```bash
npx tsc --showConfig
```

---

## 可直接抄的配置模板

{{< tabpane text=true persist=disabled >}}

{{% tab header="Node.js 服务（严格）" %}}

```jsonc
{
  "compilerOptions": {
    // 环境与目标
    "target": "ES2023",
    "lib": ["ES2023"],
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "types": ["node"],

    // 严格性
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,

    // 互操作
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,

    // 产物
    "rootDir": "./src",
    "outDir": "./dist",
    "sourceMap": true,
    "declaration": false,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

注意 `nodenext` 下导入要写 `.js` 扩展名：

```typescript
import { helper } from "./helper.js";   // ✅ 源文件是 helper.ts
```

{{% /tab %}}

{{% tab header="前端应用（Vite / React）" %}}

```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "types": ["vite/client"],

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,

    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "forceConsistentCasingInFileNames": true,

    "noEmit": true,          // Vite 负责产物，tsc 只做检查 🔥
    "skipLibCheck": true,

    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}
```

> ⚠️ `paths` **只影响类型检查**，运行时别名要在 `vite.config.ts` 里同步配置 `resolve.alias`。

{{% /tab %}}

{{% tab header="发布 npm 库" %}}

```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023"],
    "module": "nodenext",
    "moduleResolution": "nodenext",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "isolatedDeclarations": true,   // 让声明生成可以并行，加快构建 🆕

    // 产物：声明与 JS 都要
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "rootDir": "./src",
    "outDir": "./dist",

    "skipLibCheck": true
  },
  "include": ["src"]
}
```

> `isolatedDeclarations` 要求所有导出都有**显式返回类型**（否则报错），换来的是声明文件生成可以脱离类型推断、支持并行。库项目值得开。见 [13 发布库]({{< relref "13-Publishing-Libraries-with-Types.md" >}})。

{{% /tab %}}

{{% tab header="只要类型检查（CI）" %}}

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noUnusedLocals": false,       // CI 里交给 lint
    "noEmit": true,
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": ["src", "tests"]
}
```

```bash
npx tsc --noEmit
```

> 🔥 无论用什么打包器，CI 里都应该有这一步——打包器**不做类型检查**。

{{% /tab %}}

{{< /tabpane >}}

---

## 诊断类选项（放在 tsconfig 里）

这些也可以写进 `tsconfig.json`，省得每次敲命令行：

```jsonc
{
  "compilerOptions": {
    "noErrorTruncation": true   // 不截断超长类型错误，排查时必开 🔥
  }
}
```

| 选项 | 作用 |
| --- | --- |
| `noErrorTruncation` | 完整显示类型，不截断 |
| `pretty` | 彩色错误输出 |
| `listFiles` | 列出参与编译的文件 |
| `explainFiles` | 解释每个文件为何被包含 |
| `traceResolution` | 追踪模块解析 |
| `extendedDiagnostics` | 各阶段耗时 |
| `diagnostics` | 编译统计 |
| `generateTrace` | 生成性能剖析 |
| `noCheck` | 完全不检查，只产物（应急用） |

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 升级 6.0 后找不到 `process` | `TS2304` | `types: ["node"]` |
| 产物多了一层 `src/` | 路径不对 | 显式 `rootDir` |
| 用 `baseUrl` | `TS5101` | 前缀写进 `paths` |
| 用 `moduleResolution: "node"` | `TS5107` | `"bundler"` 或 `"nodenext"` |
| `nodenext` 下漏扩展名 | `TS2835` | 写 `"./x.js"` |
| 以为 `strict` 含全部检查 | 索引访问仍不安全 | 另开 `noUncheckedIndexedAccess` |
| `noUncheckedIndexedAccess` 无效果 | 静默失效 | 检查 `strictNullChecks` 是否开 |
| `extends` 后 `lib` 丢了 | 类型缺失 | 数组选项是**覆盖**不是合并 |
| 以为 `paths` 影响运行时 | 运行时找不到模块 | 同步配打包器别名 |
| `skipLibCheck` 当成万能 | 自己的 `.d.ts` 也没检查 | 手写声明要额外仔细 |
| `isolatedModules` 下 `const enum` | 报错 | 用 `as const` 对象 |
| 混用两种装饰器 | 行为怪异 | 只启用一种 |
