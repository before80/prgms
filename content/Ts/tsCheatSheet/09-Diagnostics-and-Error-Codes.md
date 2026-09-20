+++
title = "09 诊断与错误码"
weight = 109
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "高频 TSxxxx 错误码反查表、诊断参数、如何定位类型来源与读懂复杂类型错误"
isCJKLanguage = true
draft = false
+++

# 09 诊断与错误码

报错看不懂时翻这一页。**按错误码搜索**（`Ctrl+F` 搜 `TS2322`）或按**症状**查找。

> 本页所有错误码与其原文均在 **TypeScript 6.0.3** 真实触发并记录。

---

## 高频错误码反查表

{{< tabpane text=true persist=disabled >}}

{{% tab header="赋值与类型不符" %}}

| 错误码 | 原文要点 | 常见原因 | 修法 |
| --- | --- | --- | --- |
| `TS2322` | Type 'X' is not assignable to type 'Y' | 万能错误，见下 | 见下 |
| `TS2345` | Argument of type 'X' is not assignable to parameter of type 'Y' | 实参类型不对 | 检查参数类型，或用守卫收窄 |
| `TS2353` | Object literal may only specify known properties | 多余属性检查 | 删掉多余属性 / 经变量中转 / 改类型 |
| `TS2739` | Type 'X' is missing the following properties from type 'Y' | 缺属性 | 补齐，或改类型为 `Partial` |
| `TS2741` | Property 'x' is missing in type 'X' but required in type 'Y' | 缺一个必需属性 | 补上 🔥 穷举 `Record` 时常见 |
| `TS2375` | ...with 'exactOptionalPropertyTypes: true' | 给可选属性显式传了 `undefined` | 类型加 `\| undefined`，或不传该键 |
| `TS4104` | The type 'readonly T[]' is 'readonly' and cannot be assigned to the mutable type 'T[]' | 只读数组赋给可变数组 | 用 `[...ro]` 复制，或改目标为 `readonly` |
| `TS2540` | Cannot assign to 'x' because it is a read-only property | 改只读属性 | 去掉 `readonly`，或用副本 |

**`TS2322` 的系统排查法**——它只是「类型不符」，真正原因在**下面那几行**：

```text
error TS2322: Type '{ name: string; }' is not assignable to type 'User'.
  Property 'id' is missing in type '{ name: string; }' but required in type 'User'.
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ← 关键信息在这里！别只看第一行
```

| 附注信息 | 含义 |
| --- | --- |
| `Property 'x' is missing` | 少属性 |
| `Property 'x' is incompatible` | 属性类型不符 |
| `Types have separate declarations of a private property` | 私有成员不同源（结构类型不兼容） |
| `Property 'x' does not exist on type 'Y'` | 多了不该有的属性 |
| `Type 'X' is not assignable to type 'Y'. Did you mean 'Z'?` | 拼写建议 🔥 |

{{% /tab %}}

{{% tab header="属性与索引访问" %}}

| 错误码 | 原文要点 | 常见原因 | 修法 |
| --- | --- | --- | --- |
| `TS2339` | Property 'x' does not exist on type 'Y' | 拼错 / 联合上访问 / 类型没导入 | 见下 |
| `TS4111` | Property 'x' comes from an index signature | 开了 `noPropertyAccessFromIndexSignature` | 用 `obj["x"]` 而不是 `obj.x` |
| `TS7053` | Element implicitly has an 'any' type because expression of type 'string' can't be used to index | 用 `string` 索引没有索引签名的对象 | 用 `keyof`，或加索引签名 |
| `TS18048` | 'x' is possibly 'undefined' | 可能为 undefined | 判空收窄 |
| `TS18047` | 'x' is possibly 'null' | 可能为 null | 判空收窄 |
| `TS2532` | Object is possibly 'undefined' | 同上（表达式位置） | 同上 |
| `TS2531` | Object is possibly 'null' | 同上 | 同上 |
| `TS2564` | Property 'x' has no initializer and is not definitely assigned in the constructor | 类属性未初始化 | 给初值 / 构造函数赋值 / `?` |

**`TS2339` 的三种典型场景**：

```typescript
// 场景 1：拼写错误
const u = { name: "a" };
u.nmae;
// ❌ TS2339: Property 'nmae' does not exist on type '{ name: string; }'.
//    Did you mean 'name'?          ← TS 会给建议，注意看 🔥

// 场景 2：联合类型上访问成员
declare const v: string | number;
v.toUpperCase();
// ❌ TS2339: Property 'toUpperCase' does not exist on type 'string | number'.
//    Property 'toUpperCase' does not exist on type 'number'.    ← 指出哪个成员没有
// 修法：先收窄

// 场景 3：只读数组上调可变方法
declare const ro: readonly string[];
ro.push("x");
// ❌ TS2339: Property 'push' does not exist on type 'readonly string[]'.
```

{{% /tab %}}

{{% tab header="未知与隐式 any" %}}

| 错误码 | 原文要点 | 常见原因 | 修法 |
| --- | --- | --- | --- |
| `TS7006` | Parameter 'x' implicitly has an 'any' type | 参数没标注且无法推断 | 标注类型 |
| `TS7031` | Binding element 'x' implicitly has an 'any' type | 解构参数没类型 | 标注整个参数 |
| `TS18046` | 'x' is of type 'unknown' | 用了未收窄的 `unknown` | 守卫收窄 🔥 |
| `TS2571` | Object is of type 'unknown' | 同上（对象位置） | 同上 |
| `TS2304` | Cannot find name 'x' | 缺全局类型 / 拼错 / 缺导入 | 见下 |
| `TS2683` | 'this' implicitly has type 'any' | `function` 回调里的 `this` | 改箭头函数 |
| `TS7030` | Not all code paths return a value | 有分支没 return | 补 return，或用 `never` |

**`TS2304` 在 6.0 里的最大来源是 `types` 默认为 `[]`**：

```text
error TS2304: Cannot find name 'process'.
error TS2304: Cannot find name 'Buffer'.
error TS2304: Cannot find name 'describe'.
```

```jsonc
// 修法
{ "compilerOptions": { "types": ["node"] } }          // Node 全局
{ "compilerOptions": { "types": ["node", "vitest/globals"] } }  // 测试全局
```

**`TS18046` 的正确处理**：

```typescript
function f(u: unknown) {
  return u.name;
  //     ~ ❌ TS18046: 'u' is of type 'unknown'.
}

// ✅ 用守卫收窄
function g(u: unknown) {
  if (typeof u === "object" && u !== null && "name" in u) {
    return (u as { name: unknown }).name;
  }
  return undefined;
}
```

{{% /tab %}}

{{% tab header="函数与类" %}}

| 错误码 | 原文要点 | 常见原因 | 修法 |
| --- | --- | --- | --- |
| `TS2554` | Expected N arguments, but got M | 参数个数不符 | 补齐 / 改签名 |
| `TS2551` | Property 'x' does not exist... Did you mean 'y'? | 拼写 + 有建议 | 按建议改 |
| `TS2769` | No overload matches this call | 重载都不匹配 | 看下面列出的每个重载为何失败 |
| `TS2366` | Function lacks ending return statement | 有返回值声明但可能不返回 | 补 return 或 `default` |
| `TS2391` | Function implementation is missing or not immediately following the declaration | 只写了重载签名没写实现 | 补实现签名 |
| `TS2511` | Cannot create an instance of an abstract class | `new` 抽象类 | 用子类 |
| `TS2564` | 见「属性与索引」 | — | — |
| `TS4113` | This member cannot have an 'override' modifier | `override` 但基类没有 | 去掉 `override`，或基类补上 |
| `TS4114` | This member must have an 'override' modifier | 开了 `noImplicitOverride` | 加 `override` |
| `TS2411` | Property 'x' of type 'T' is not assignable to 'string' index type 'U' | 已知属性与索引签名冲突 | 统一类型 |
| `TS2341` | Property 'x' is private and only accessible within class | 访问私有成员 | 改 `public`/`protected`，或用方法 |

**`TS2769` 的读法**（信息量很大，别跳过）：

```text
error TS2769: No overload matches this call.
  Overload 1 of 2, '(input: string): string[]', gave the following error.
    Argument of type 'boolean' is not assignable to parameter of type 'string'.
  Overload 2 of 2, '(input: number): number[]', gave the following error.
    Argument of type 'boolean' is not assignable to parameter of type 'number'.
  ← TS 逐个重载告诉你为什么不行，直接看每个分支的原因
```

{{% /tab %}}

{{% tab header="模块与声明" %}}

| 错误码 | 原文要点 | 常见原因 | 修法 |
| --- | --- | --- | --- |
| `TS2307` | Cannot find module 'x' or its corresponding type declarations | 模块/类型找不到 | 见下 |
| `TS1484` | 'x' is a type and must be imported using a type-only import | 开了 `verbatimModuleSyntax` | `import type` |
| `TS1205` | Re-exporting a type when 'isolatedModules' is enabled requires using 'export type' | 再导出类型 | `export type` |
| `TS2835` | Relative import paths need explicit file extensions in ECMAScript imports | `nodenext` ESM 缺扩展名 | 写 `"./x.js"` |
| `TS5097` | An import path can only end with a '.ts' extension when 'allowImportingTsExtensions' is enabled | 导入了 `.ts` | 开该选项，或改 `.js` |
| `TS2664` | Invalid module name in augmentation | 在模块文件里写通配 `declare module` | 移到无 import 的脚本文件 |
| `TS2300` | Duplicate identifier 'x' | 重复声明（`type` 不能合并） | 改名，或改用 `interface` |
| `TS2344` | Type 'x' does not satisfy the constraint 'y' | 泛型约束不满足 | 看约束是什么 |

**`TS2307` 排查顺序** 🔥：

```bash
# 1. 模块解析到底试了哪些路径？
npx tsc --noEmit --traceResolution 2>&1 | grep -A10 "my-module"

# 2. 该文件为什么被/没被包含？
npx tsc --noEmit --explainFiles | head -50
```

| 症状 | 原因 |
| --- | --- |
| 装了包但仍报找不到 | 该包没有类型声明 → 装 `@types/xxx` 或手写 |
| 只有某些导入报错 | `moduleResolution` 与该包的 `exports` 不匹配 |
| 编辑器正常、CI 报错 | 依赖没装（CI 用 `npm ci` 重装后可能不同） |
| 相对路径导入报错 | 缺扩展名（`nodenext`）或路径写错 |

{{% /tab %}}

{{% tab header="泛型与类型运算" %}}

| 错误码 | 原文要点 | 常见原因 | 修法 |
| --- | --- | --- | --- |
| `TS2589` | Type instantiation is excessively deep and possibly infinite | 递归类型过深 | 加深度计数器，简化类型 |
| `TS2636` | Type 'X' is not assignable to type 'Y' as implied by variance annotation | 变型标注写错 | 改成 `in` / `out` / `in out` |
| `TS5052` | Option 'x' cannot be specified without specifying option 'y' | 选项有依赖 | 一起开（如 `strictNullChecks`） |
| `TS2314` | Generic type 'x' requires N type argument(s) | 泛型实参个数不对 | 补齐 |
| `TS2344` | 见「模块与声明」 | — | — |
| `TS2536` | Type 'K' cannot be used to index type 'T' | 用非法键索引 | 约束 `K extends keyof T` |

**`TS2589` 的处理**：

```typescript
// 🛑 无限递归（编译器无法判定终止）
type Infinite<T> = { [K in keyof T]: Infinite<T[K]> }[keyof T];

// ✅ 加深度限制
type Prev = [never, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
type SafeDeep<T, D extends number = 5> = D extends 0
  ? T
  : { [K in keyof T]: SafeDeep<T[K], Prev[D]> };
```

> ⚠️ `TS2589` 是**类型体操过重的信号**，不是「再加点技巧就能解决」的问题。见 [06 类型体操的代价边界]({{< relref "06-Type-Level-Programming-Recipes.md" >}})。

{{% /tab %}}

{{% tab header="TS 6.0 新增与废弃相关" %}}

这类错误是**升级 6.0 特有的**，看到就该想到「是不是 6.0 变了」。

| 错误码 | 原文要点 | 原因 | 修法 |
| --- | --- | --- | --- |
| `TS5101` | Option 'x' is deprecated and will stop functioning in TypeScript 7.0 | 用了废弃**选项** | 见下表替代 |
| `TS5107` | Option 'x=Y' is deprecated and will stop functioning in TypeScript 7.0 | 用了废弃**取值** | 见下表替代 |
| `TS5112` | tsconfig.json is present but will not be loaded if files are specified on commandline | 命令行传了文件 | 加 `--ignoreConfig` |
| `TS2880` | Import assertions have been replaced by import attributes. Use 'with' instead of 'assert' | 用了旧 `assert` 语法 | 改 `with` |
| `TS2882` | Cannot find module or type declarations for side-effect import of 'x' | `noUncheckedSideEffectImports`（6.0 默认开） | 修正路径或关掉该选项 |
| `TS1294` | This syntax is not allowed when 'erasableSyntaxOnly' is enabled | 用了非擦除语法 | 见 [08]({{< relref "08-tsconfig-Reference.md" >}}) |
| `TS5069` | Option 'isolatedDeclarations' cannot be specified without specifying option 'declaration' | 选项依赖 | 加 `declaration` 或 `composite` |

**废弃项的替代速查** 🔥：

| 报错涉及 | 改成 |
| --- | --- |
| `target=ES5` | `ES2015` 或更高 |
| `moduleResolution=node10` | `bundler` 或 `nodenext` |
| `module=AMD` / `UMD` / `System` | ESM（`esnext` / `nodenext`） |
| `baseUrl` | 前缀写进每条 `paths` |
| `outFile` | 用外部打包器 |
| `downlevelIteration` | 删掉 |
| `esModuleInterop=false` | 删掉该行 |
| `allowSyntheticDefaultImports=false` | 删掉该行 |
| `alwaysStrict=false` | 删掉该行 |
| `import ... assert` | `import ... with` |

临时压制（迁移期）：

```jsonc
{ "compilerOptions": { "ignoreDeprecations": "6.0" } }
```

> ⚠️ 这只是让报错消失，**代码并没有变正确**。7.0 会彻底移除这些选项。见 [08 tsconfig]({{< relref "08-tsconfig-Reference.md" >}})。

{{% /tab %}}

{{< /tabpane >}}

---

## 诊断手段

{{< tabpane text=true persist=disabled >}}

{{% tab header="看完整类型" %}}

类型太长时 TS 会截断成 `...`，此时**必须**关掉截断才能看懂。

```bash
npx tsc --noEmit --noErrorTruncation
```

或写进配置：

```jsonc
{ "compilerOptions": { "noErrorTruncation": true } }
```

**编辑器里看类型的最快方式**：

| 操作 | 效果 |
| --- | --- |
| 悬停标识符 | 看推断出的类型 🔥 |
| `Ctrl/Cmd + 悬停` | 看类型的完整展开 |
| 选中表达式后悬停 | 看该表达式类型 |
| 「转到类型定义」 | 跳到类型的声明处 🔥 |

💡 **最快的调试技巧**：写一行故意错误的赋值，让报错信息告诉你类型是什么：

```typescript
const config = buildConfig();
const _debug: null = config;
//    ~~~~~~ Type '{ host: string; port: number; ... }' is not assignable to type 'null'.
//            ^^^^^^^^ 完整类型直接打印出来了
```

{{% /tab %}}

{{% tab header="找模块与文件" %}}

```bash
# 每个文件为什么被包含进编译
npx tsc --noEmit --explainFiles

# 模块解析全过程（每个 import 试了哪些路径）
npx tsc --noEmit --traceResolution

# 实际参与编译的文件列表
npx tsc --noEmit --listFiles

# 只看文件列表，不编译
npx tsc --listFilesOnly
```

| 命令 | 回答的问题 |
| --- | --- |
| `--explainFiles` | 「这个文件为什么被编译进来？」 |
| `--traceResolution` | 「这个 import 为什么找不到 / 找错了？」 🔥 |
| `--listFiles` | 「一共编译了哪些文件？」 |

`--explainFiles` 输出里会标注包含原因：

```text
src/index.ts
  Matched by include pattern 'src/**/*.ts' in 'tsconfig.json'
node_modules/@types/node/index.d.ts
  Entry point for implicit type library 'node'
```

> 💡 **排查「幽灵文件」**：如果发现意料之外的文件被编译（比如某个测试文件、某个多余的 `@types`），`--explainFiles` 会直接告诉你原因——通常是 `include` 太宽，或 6.0 之前 `types` 自动加载全部。

{{% /tab %}}

{{% tab header="性能诊断" %}}

```bash
# 各阶段耗时 + 类型/实例化计数
npx tsc --noEmit --extendedDiagnostics

# 详细统计
npx tsc --noEmit --diagnostics

# 生成 Chrome Trace 剖析
npx tsc --noEmit --generateTrace ./trace
```

`--extendedDiagnostics` 输出解读：

| 指标 | 正常 | 偏高说明 |
| --- | --- | --- |
| `Parse time` | 小 | 文件过多/过大 |
| `Bind time` | 很小 | 通常正常 |
| `Check time` | 主要耗时 | 类型体操、复杂泛型 |
| `Total time` | — | — |
| `Types` | 几万以内 | 类型定义过多 |
| `Instantiations` | 十万量级 | **百万以上要警惕** ⚠️ |
| `Memory used` | — | 过高可能 OOM |

打开 `trace` 目录里的 `trace.json` 到 `chrome://tracing` 或 Perfetto 查看，能看到**具体哪个文件/哪个类型**最耗时。

> 🔥 `Instantiations` 是判断「类型体操是否过重」的核心指标。它爆炸通常意味着某个泛型被反复实例化。见 [17 性能]({{< relref "17-Compiler-Internals-and-Performance.md" >}})。

{{% /tab %}}

{{% tab header="编辑器与语言服务" %}}

| 现象 | 处理 |
| --- | --- |
| 编辑器报错但 `tsc` 不报 | `TypeScript: Restart TS Server` 🔥 |
| 类型显示陈旧 | 同上 |
| 用了错误的 TS 版本 | `TypeScript: Select TypeScript Version` |
| 想固定用项目内版本 | `.vscode/settings.json` 设 `typescript.tsdk` |

```jsonc
// .vscode/settings.json
{ "typescript.tsdk": "node_modules/typescript/lib" }
```

排查语言服务：

| 命令面板项 | 用途 |
| --- | --- |
| `TypeScript: Open TS Server log` | 看语言服务日志 |
| `TypeScript: Restart TS Server` | 重启（解决大部分怪问题） |
| `Developer: Reload Window` | 重启整个窗口 |

> ⚠️ **编辑器与 `tsc` 可能用不同配置**：编辑器按文件所在目录找最近的 `tsconfig.json`，而 `tsc` 用你指定的那个。这就是「编辑器红、CI 绿」（或反之）的常见原因。用 `tsc --showConfig` 对比确认。

{{% /tab %}}

{{< /tabpane >}}

---

## 读懂复杂类型错误

### 错误信息的结构

```text
error TS2322: Type 'A' is not assignable to type 'B'.
  Property 'x' is missing in type 'A' but required in type 'B'.
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ① 表面：A 不能赋给 B
  ② 真正原因：A 少了 x
```

**永远先读缩进最深的那些行**——那才是根因。

### 从内向外读

```text
error TS2345: Argument of type '{ id: number; name: string; }' is not assignable
              to parameter of type 'User'.
  Property 'email' is missing in type '{ id: number; name: string; }'
  but required in type 'User'.
```

读法：**最内层**（`{ id: number; name: string; }`）是实际类型，**中间**（`User`）是期望类型，**最外层**说明差异（缺 `email`）。

### 遇到「类型展开成一坨」时

```typescript
// 给复杂类型起个名字，错误信息立刻可读
type Config = Prettify<DeepPartial<UserConfig>>;
```

见 [06 Prettify]({{< relref "06-Type-Level-Programming-Recipes.md" >}})。

### 二分法定位

错误信息指向一行，但根因常在别处：

| 步骤 | 做法 |
| --- | --- |
| 1 | 把出错表达式**逐段拆成中间变量** |
| 2 | 给每个中间变量加类型标注，看哪一个先报错 🔥 |
| 3 | 或用「故意赋给 `null`」技巧打印类型 |

```typescript
// 🛑 一行里报错，不知道哪一段错了
const result = process(transform(parse(input)));

// ✅ 拆开，立刻定位
const a = parse(input);       // 看 a 的类型对不对
const b = transform(a);       // 错就在这
const c = process(b);
```

---

## 错误抑制的正确姿势

| 手段 | 强度 | 何时用 |
| --- | --- | --- |
| 修好它 | — | **永远首选** 🔥 |
| 类型守卫 / 收窄 | 强 | 外部数据 |
| `satisfies` | 强 | 校验字面量 |
| `as T` | 弱 | 你确实比编译器知道得多 |
| `// @ts-expect-error` | 无 | 测试负数场景、临时绕过 |
| `// @ts-ignore` | 无 | 🛑 不要用 |
| `// @ts-nocheck` | 无 | 🚧 迁移期整文件临时跳过 |

```typescript
// ✅ 好：@ts-expect-error 会「自我清理」——不再报错时会提示你删掉
// @ts-expect-error 上游类型定义有误，见 issue #123
legacyApi(badInput);

// 🛑 坏：写错了也发现不了，永远不会提醒你
// @ts-ignore
legacyApi(badInput);
```

**治理 `@ts-ignore` 的方法**（迁移项目必备）：

```bash
# 统计数量，纳入 CI 门槛
grep -rn "@ts-ignore" src --include="*.ts" --include="*.tsx" | wc -l

# 找出所有抑制点，逐个处理
grep -rn "@ts-ignore\|@ts-expect-error\|@ts-nocheck" src --include="*.ts"
```

| 策略 | 说明 |
| --- | --- |
| 全部改成 `@ts-expect-error` | 至少能在失效时被发现 🔥 |
| 每条都写原因 | `// @ts-expect-error: 原因 + issue 链接` |
| CI 里禁止新增 | lint 规则或计数门槛 |
| 定期清理 | 每次升级 TS 版本时重跑 |

---

## 常见「报错但代码没错」的情况

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 编辑器报错，`tsc` 不报 | 语言服务状态陈旧 / 配置不同 | Restart TS Server；对比 `--showConfig` |
| 升级后突然大量报错 | 6.0 的 `strict` 默认开启 | 先显式 `strict: false` 过渡，再逐项开 |
| 找不到 `process` / `describe` | 6.0 `types` 默认 `[]` | `types: ["node"]` |
| 别的项目正常，这个报错 | 缺 `@types/*` 依赖 | 检查 `package.json` |
| CI 报错，本地正常 | CI 用 `npm ci` 重装，`@types` 版本不同 | 锁定版本 |
| 只有某个文件报错 | 该文件不在 `include` 或用了不同 tsconfig | `--explainFiles` |
| 报错位置很奇怪 | 错误信息被截断 | `--noErrorTruncation` |
