+++
title = "13 发布带类型的库"
weight = 113
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "package.json 的 exports 与 types 字段、双发布产物、声明生成、类型 API 的语义化版本"
isCJKLanguage = true
draft = false
+++

# 13 发布带类型的库

会写 `.d.ts` 不等于**别人能用上你的类型**。本页讲的是把类型**正确交付**给使用者的工程细节。

> 涉及解析行为的结论均在 TS 6.0.3 + `moduleResolution: nodenext` 实测。

---

## `package.json` 是类型交付的核心

{{< tabpane text=true persist=disabled >}}

{{% tab header="最小可用配置" %}}

```jsonc
{
  "name": "mylib",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "default": "./dist/index.js"
    }
  },
  "files": ["dist"]
}
```

| 字段 | 作用 | 还需要吗 |
| --- | --- | --- |
| `types`（顶层） | 老工具的类型入口 | ✅ 保留，兼容旧 `node10` 解析 |
| `main` | 老工具的 JS 入口 | ✅ 保留，兼容 CJS |
| `exports` | **现代解析的唯一事实来源** | ✅ 必须有 🔥 |
| `files` | 控制发布哪些文件 | ✅ 别忘了 `dist` |
| `type` | 决定 `.js` 被当作 ESM 还是 CJS | ✅ 明确写 |

> ⚠️ **`files` 忘了写 `dist`** 会导致发布了**没有产物**的包——本地测试正常，装到别的项目就报 `Cannot find module`。这是最常见的发布事故。

{{% /tab %}}

{{% tab header="types 条件的位置" %}}

社区普遍说法是「`types` 必须写在 `default` **之前**」。**实测结论要更细致**：

| 配置 | 实测结果（TS 6.0.3, `nodenext`） |
| --- | --- |
| `{"types": ..., "default": ...}` | ✅ 解析到类型 |
| `{"default": ..., "types": ...}` | ✅ **也解析到类型** |
| 只有顶层 `types` | ✅ 解析到类型 |
| `exports` 只有 `types` | ✅ 解析到类型 |
| `{"import": {"types": ...}, "require": {"types": ...}}` | ✅ 按条件分支正确解析 |

也就是说，**当前 TS 版本对顺序是宽容的**。但仍然建议 **`types` 写在最前**：

| 理由 | 说明 |
| --- | --- |
| 生态惯例 | Node 官方文档、`publint`、`arethetypeswrong` 都按此检查 |
| 其他工具 | 少数工具严格按顺序匹配第一个命中的条件 |
| 未来兼容 | 宽容行为不构成规范保证 💭 |
| 可读性 | 类型入口放最前，意图清楚 |

```jsonc
// ✅ 推荐写法：types 在最前
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    }
  }
}
```

> 🔥 **别只依赖「我本地能跑」**——用工具验证：
>
> ```bash
> npx publint                  # 检查 package.json 与产物的匹配
> npx @arethetypeswrong/cli --pack   # 检查类型在各解析模式下能否找到
> ```
>
> `attw` 会直接告诉你「在 `node16` ESM 下类型丢失」这类问题，比手工测试可靠得多。

**子路径导出**（`mylib/utils` 这种）：

```jsonc
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "default": "./dist/index.js"
    },
    "./utils": {
      "types": "./dist/utils/index.d.ts",
      "default": "./dist/utils/index.js"
    },
    "./package.json": "./package.json"    // ✅ 允许读取，很多工具需要
  }
}
```

⚠️ **一旦加了 `exports`，其它路径就全部封闭**。使用者不能再 `import "mylib/dist/internal/thing"`——这通常是你想要的（封装），但要**意识到这是破坏性变更**。

{{% /tab %}}

{{% tab header="双发布（ESM + CJS）" %}}

同时支持两种模块系统。**两种流派**：

**流派一：两次编译**（推荐，产物清晰）

```jsonc
// tsconfig.json（ESM）
{
  "compilerOptions": {
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "outDir": "./dist/esm",
    "declaration": true,
    "declarationDir": "./dist/types",
    "rootDir": "./src"
  },
  "include": ["src"]
}
```

```jsonc
// tsconfig.cjs.json（CJS）
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "module": "commonjs",
    "moduleResolution": "nodenext",
    "outDir": "./dist/cjs",
    "declaration": false          // 声明只产一份
  }
}
```

```jsonc
// package.json
{
  "type": "module",
  "main": "./dist/cjs/index.js",
  "types": "./dist/types/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/types/index.d.ts",
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  }
}
```

```
dist/
├── esm/          # ESM 产物
├── cjs/          # CJS 产物
└── types/        # 唯一一份 .d.ts
```

⚠️ **`dist/cjs` 目录需要自己的 `package.json`** 声明 CJS，否则 `"type": "module"` 会让 `.js` 被当成 ESM：

```jsonc
// dist/cjs/package.json ——构建脚本生成
{ "type": "commonjs" }
```

**流派二：打包器产双格式**（tsup / unbuild 等）

```jsonc
// tsup.config.ts
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm", "cjs"],
  dts: true,              // 生成声明
  clean: true,
  sourcemap: true,
});
```

| 流派 | 优点 | 缺点 |
| --- | --- | --- |
| 两次 `tsc` | 产物与源码一一对应，调试友好 | 配置略繁琐 |
| 打包器 | 一条命令，输出干净 | 声明由工具生成，偶有偏差 |

> ⚠️ **双发布的「双重身份」风险**：如果一个包同时被 ESM 和 CJS 引用，可能被**加载两次**，导致 `instanceof` 失败、单例状态不共享。缓解手段：
>
> | 手段 | 说明 |
> | --- | --- |
> | 尽量只发 ESM | 2026 年这是可行且推荐的 🔥 |
> | 用 `exports` 的 `import`/`require` 分支 | 现代打包器能正确处理 |
> | 避免跨模块边界的 `instanceof` | 用鸭子类型或品牌属性 |
>
> 💭 **新库建议只发 ESM**。Node 22+ 已原生支持 `require(esm)`，双发布的必要性大幅下降。

{{% /tab %}}

{{< /tabpane >}}

---

## 声明文件生成

{{< tabpane text=true persist=disabled >}}

{{% tab header="产物选项" %}}

| 选项 | 作用 | 建议 |
| --- | --- | --- |
| `declaration` | 生成 `.d.ts` | ✅ 必须 |
| `declarationMap` | 生成 `.d.ts.map` | ✅ **强烈建议** 🔥 |
| `declarationDir` | 声明单独目录 | 双发布时用 |
| `emitDeclarationOnly` | 只产声明 | 声明交给别的工具时用 |
| `stripInternal` | 删除 `@internal` 声明 | ✅ 隐藏内部 API |

```jsonc
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,     // 使用者 Ctrl+点击能跳到你的源码 🔥
    "sourceMap": true,
    "rootDir": "./src",
    "outDir": "./dist"
  }
}
```

**`declarationMap` 的价值**：没有它，使用者点进你的函数只能看到 `.d.ts` 的签名；有了它，能**直接跳到真实的 `.ts` 源码**。对调试体验影响很大，且成本极低。

**`stripInternal` 隐藏内部 API**（实测）：

```typescript
// src/index.ts
/** @internal */
export function internalHelper(): number { return 1; }

export function publicApi(x: number): number { return x * 2; }
```

```typescript
// 生成的 dist/index.d.ts —— internalHelper 完全消失 ✅
export declare function publicApi(x: number): number;
```

⚠️ **`stripInternal` 只删声明，不删实现**。`internalHelper` 在运行时**依然存在并可被导入**，只是没有类型。所以它**不是安全机制**，只是 API 面的收敛。

想真正不暴露，就不要 `export`，或拆成内部模块。

{{% /tab %}}

{{% tab header="isolatedDeclarations 🆕" %}}

TS 5.5 引入。要求**所有导出都有显式类型标注**，从而让声明生成**不依赖类型推断**。

```typescript
// 🛑 报错：没有显式返回类型
export function publicApi(x: number) { return x * 2; }
//                 ~~~~~~~~~ error TS9007: Function must have an explicit return
//                           type annotation with --isolatedDeclarations.

export const arrow = (x: number) => x + 1;
//           ~~~~~ error TS9007
```

```typescript
// ✅ 补上显式类型即可
export function publicApi(x: number): number { return x * 2; }
export const arrow = (x: number): number => x + 1;
```

（`TS9007` 已实测。）

| 好处 | 说明 |
| --- | --- |
| **并行生成声明** | 每次文件可独立处理，大项目构建显著加快 🔥 |
| 声明更稳定 | 不依赖推断，重构时声明不会意外变化 |
| 显式 API 契约 | 导出的类型一眼可见 |

| 代价 | 说明 |
| --- | --- |
| 要写很多返回类型 | 泛型函数的类型要手写，可能很长 |
| 类型体操受限 | 依赖推断的技巧可能写不出来 |
| 需要 `declaration` 或 `composite` | 否则 `TS5069` |

```jsonc
{
  "compilerOptions": {
    "declaration": true,
    "isolatedDeclarations": true
  }
}
```

> 💭 **给库作者的建议**：如果是**大型库**或用了项目引用/远程缓存，`isolatedDeclarations` 的构建收益很大，值得忍受手写返回类型。小型库可以先不开。

{{% /tab %}}

{{% tab header="声明文件的质量" %}}

**生成的声明会暴露内部类型**——这是常见问题：

```typescript
// src/index.ts
interface InternalOptions { retries: number; timeout: number }   // 没有 export

export function createClient(opts: InternalOptions): Client { /* ... */ }
```

```typescript
// 生成的 index.d.ts
interface InternalOptions {          // ⚠️ 被带出来了
  retries: number;
  timeout: number;
}
declare function createClient(opts: InternalOptions): Client;
export { createClient };
// ⚠️ InternalOptions 出现在公开 API 上，但使用者无法导入它
```

问题在于：使用者能看到 `createClient` 的参数类型叫 `InternalOptions`，却**无法 `import` 这个名字**，只能靠 `Parameters<typeof createClient>[0]` 迂回。

**修法**：

```typescript
// ✅ 显式导出，或给公开 API 用公开类型
export interface ClientOptions { retries: number; timeout: number }
export function createClient(opts: ClientOptions): Client { /* ... */ }
```

| 症状 | 修法 |
| --- | --- |
| 公开函数用了未导出类型 | 导出它，或改为公开类型 |
| 声明里出现匿名大对象 | 提取具名类型并导出 🔥 |
| 声明里出现 `any` | 补类型 |
| 声明里出现私有类 | 提取接口 |

> 🔥 **发布前检查生成的 `.d.ts`**。它才是使用者真正看到的 API，而不是你的源码。一个实用做法：打开 `dist/index.d.ts` 通读一遍，问「使用者能理解这个 API 吗」。

{{% /tab %}}

{{< /tabpane >}}

---

## 类型 API 的语义化版本

**类型也是 API**。改 `.d.ts` 就是改 API，可能构成破坏性变更。

{{< tabpane text=true persist=disabled >}}

{{% tab header="什么算 breaking change" %}}

| 变更 | 破坏性 | 为什么 |
| --- | --- | --- |
| 收窄参数类型 | 🔴 是 | 使用者的合法调用变得不合法 |
| 放宽参数类型 | 🟢 否 | 兼容 |
| 收窄返回类型 | 🟢 否 | 兼容（协变） |
| **放宽返回类型** | 🔴 是 | 使用者依赖窄类型会报错 |
| 给参数加可选属性 | 🔴 **是** ⚠️ | 使用者传入的对象字面量触发多余属性检查 |
| 给返回类型加属性 | 🟢 否 | 兼容 |
| 删除导出的类型 | 🔴 是 | 使用者 import 失败 |
| 重命名类型参数 | 🟡 可能 | 显式传类型实参时会失败 |
| 加 `readonly` | 🔴 是 | 使用者原本的赋值变非法 |
| 去 `readonly` | 🟢 否 | 兼容 |
| 把 `interface` 改成 `type` | 🔴 是 | 使用者无法再声明合并 🔥 |
| 加泛型默认值 | 🟢 否 | 兼容 |
| 收紧泛型约束 | 🔴 是 | 原有实参不再满足 |
| 放宽泛型约束 | 🟢 否 | 兼容 |
| 把具体类型改成泛型 | 🟡 可能 | 推断可能变化 |

⚠️ **最容易忽略的两条**：

**① 给接口加必需属性是 breaking**

```typescript
// v1
export interface Options { a: number }

// v2 —— 加一个可选属性，看起来安全
export interface Options { a: number; b?: string }
```

```typescript
// 使用者代码：对象字面量会触发多余属性检查 🛑
createClient({ a: 1, b: "x" });   // v1 报错，v2 才合法
// 反过来：使用者若要传给一个只接受 v1 Options 的地方...
```

实际上**加可选属性通常是安全的**，真正危险的是**加必需属性**：

```typescript
// v2 🛑
export interface Options { a: number; b: string }   // 加必需属性
// 使用者：createClient({ a: 1 })  → 编译失败
```

**② 把 `interface` 改成 `type` 会破坏声明合并**

```typescript
// v1 ✅ 使用者可以扩充
export interface Config { url: string }
// 使用者代码
declare module "mylib" { interface Config { token: string } }   // ✅ 合法

// v2 🛑 改成 type 后，上面的使用者代码直接报错
export type Config = { url: string };
```

> 💭 **给公开 API 用 `interface`** 的一个实际理由：它允许使用者通过声明合并扩充，也给未来的自己留了余地。

{{% /tab %}}

{{% tab header="用工具守住契约" %}}

**API Extractor**（微软出品）—— 生成 API 报告，把类型 API 纳入版本审查：

```jsonc
// api-extractor.json
{
  "$schema": "https://developer.microsoft.com/json-schemas/api-extractor/v7/api-extractor.schema.json",
  "mainEntryPointFilePath": "<projectFolder>/dist/types/index.d.ts",
  "apiReport": {
    "enabled": true,
    "reportFolder": "<projectFolder>/etc/"
  },
  "docModel": { "enabled": true },
  "dtsRollup": {
    "enabled": true,
    "untrimmedFilePath": "<projectFolder>/dist/index.d.ts"
  }
}
```

```bash
npx api-extractor run --local        # 生成/对比 API 报告
npx api-extractor run                # CI 中检查是否有未声明的变更
```

它会在 `etc/mylib.api.md` 里生成一份**人类可读的 API 摘要**，纳入 git。任何 API 变更都会在 PR diff 里显现——**review 时能直接看到类型 API 变了什么**。🔥

**`@public` / `@beta` / `@internal` 标记**：

```typescript
/**
 * 稳定 API，遵循语义化版本。
 * @public
 */
export function stableApi(): void {}

/**
 * 可能变更，不保证兼容。
 * @beta
 */
export function experimentalApi(): void {}

/** @internal */
export function privateHelper(): void {}
```

| 标记 | 语义 | API Extractor 行为 |
| --- | --- | --- |
| `@public` | 稳定 | 纳入 API 报告 |
| `@beta` | 实验性 | 纳入，但标记为 beta |
| `@alpha` | 内部预览 | 同上 |
| `@internal` | 私有 | **从 .d.ts 中移除** |

**其它验证工具**：

| 工具 | 检查什么 |
| --- | --- |
| `publint` | `package.json` 与产物是否匹配 |
| `@arethetypeswrong/cli` | 各解析模式下类型能否找到 🔥 |
| `tsd` | 类型行为是否符合预期（见 [12]({{< relref "12-Testing.md" >}})） |
| `api-extractor` | 类型 API 的变更追踪 |

```bash
# 发布前的标准检查流程
npm run build
npx tsc --noEmit
npx tsd
npx publint
npx @arethetypeswrong/cli --pack .
npm pack --dry-run          # 看看到底会发布哪些文件
```

> 🔥 **`npm pack --dry-run` 是最后一道防线**：它列出实际会被发布的文件。确认没有漏 `dist`、没有误带 `src`、没有带上测试文件。

{{% /tab %}}

{{% tab header="声明文件的测试" %}}

类型行为需要**专门的测试**，否则重构时悄悄退化。

```typescript
// test-d/index.test-d.ts
import { expectType, expectError, expectAssignable } from "tsd";
import { createClient, type Client } from "../src/index.js";

// ① 返回值类型精确
expectType<Client>(createClient({ retries: 3, timeout: 1000 }));

// ② 参数缺字段应当报错
expectError(createClient({ retries: 3 }));

// ③ 推断位置正确
const client = createClient({ retries: 3, timeout: 1000 });
expectType<Promise<string>>(client.get("/x"));

// ④ 泛型推断
expectType<{ a: number }>(pick({ a: 1, b: "x" }, ["a"] as const));
```

```bash
npx tsd          # CI 里跑
```

| 该测什么 | 例子 |
| --- | --- |
| 返回值类型 | `expectType<T>(fn())` |
| 错误用法被拒 | `expectError(fn(bad))` |
| 泛型推断位置 | 断言推断结果 |
| 可选性 | `expectType<{ a?: number }>(...)` |
| `readonly` 保留 | 断言只读 |

> 💭 **`tsd` 是库项目性价比最高的质量投入之一**。它把「类型 API」变成有测试保护的契约，防止重构时无意中改变使用者看到的类型。代价只是几十行断言。

{{% /tab %}}

{{< /tabpane >}}

---

## 发布检查清单

```jsonc
// 一个完整的库 package.json 模板
{
  "name": "mylib",
  "version": "1.0.0",
  "type": "module",
  "description": "带完整类型的示例库",
  "license": "MIT",

  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    },
    "./package.json": "./package.json"
  },

  "files": ["dist", "README.md", "LICENSE"],

  "sideEffects": false,

  "engines": { "node": ">=20" },

  "scripts": {
    "build": "tsc -p tsconfig.build.json",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:types": "tsd",
    "lint:pkg": "publint && attw --pack .",
    "prepublishOnly": "npm run build && npm run typecheck && npm run test && npm run test:types && npm run lint:pkg"
  },

  "devDependencies": {
    "typescript": "^6.0.3",
    "tsd": "^0.33.0",
    "vitest": "^5.0.1",
    "publint": "^0.3.0",
    "@arethetypeswrong/cli": "^0.18.0"
  }
}
```

| 检查项 | 命令 | 确认什么 |
| --- | --- | --- |
| 构建 | `npm run build` | 产物生成 |
| 类型检查 | `tsc --noEmit` | 源码类型正确 |
| 行为测试 | `vitest run` | 逻辑正确 |
| 类型测试 | `tsd` | 类型 API 未退化 🔥 |
| 包结构 | `publint` | `exports` 与产物匹配 |
| 解析验证 | `attw --pack .` | 各模式下类型可找到 🔥 |
| 发布内容 | `npm pack --dry-run` | 该发的都发了 |
| 声明可读性 | 人工读 `dist/index.d.ts` | API 面是否清晰 |

> 🔥 **`prepublishOnly` 把这些串起来**，保证不会把一个坏包推到 npm。注意 `npm publish` 触发它，而 `npm pack` **不触发**——所以本地验证用 `npm pack --dry-run` 看内容，用 `npm publish --dry-run` 触发完整检查。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| `files` 漏了 `dist` | 装了包找不到模块 | 加 `files: ["dist"]` |
| 只写顶层 `types` 没写 `exports` | 现代解析下丢类型 | 两者都写 |
| `exports` 漏了 `types` 条件 | 类型找不到 | 加 `types` 分支 |
| `exports` 忘了 `./package.json` | 某些工具读不到 | 显式导出 |
| 双发布的 CJS 目录缺 `package.json` | CJS 被当 ESM | 加 `{"type":"commonjs"}` |
| `stripInternal` 当安全机制 | 运行时仍可导入 | 不 export 才是真隐藏 |
| 公开 API 用了未导出类型 | 使用者无法引用 | 导出该类型 |
| 把 `interface` 改成 `type` | 使用者扩充报错 | 公开 API 用 `interface` |
| 加必需属性 | 使用者代码编译失败 | 加可选属性，或发大版本 |
| 加 `readonly` | 使用者赋值失败 | 发大版本 |
| 没有类型测试 | 类型悄悄退化 | 用 `tsd` 🔥 |
| 没验证包结构 | 发布后才发现问题 | `publint` + `attw` |
