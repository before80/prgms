+++
title = "01 起步与工具链"
weight = 101
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "TypeScript 6.0 的安装、五种运行方式、tsc 命令行全表与诊断参数"
isCJKLanguage = true
draft = false
+++

# 01 起步与工具链

本页回答两个问题：**这段 TypeScript 代码怎么跑起来**，以及**出了问题用什么命令查**。

> 基线：TypeScript **6.0.3**，Node.js **v24.20.0**。所有命令输出均为实测结果。

---

## 安装

```bash
npm install -D typescript        # 项目内（推荐，版本随项目锁定）
npm install -g typescript        # 全局（只为了有个 tsc 应急）
npx tsc --version                # 检查版本
```

| 包 | 作用 |
| --- | --- |
| `typescript` | 编译器本体，提供 `tsc` 与 `tsserver`（编辑器用的语言服务） |
| `@types/node` | Node 内置模块与全局变量的类型声明 🔥 **6.0 起必须显式配置** |
| `tsx` | 开发期直接运行 `.ts`，基于 esbuild |

> ⚠️ **6.0 重大变化**：`types` 默认值变为 **`[]`**。6.0 之前 `node_modules/@types` 下所有包会被自动加载，现在**不会**了。升级后如果突然报 `Cannot find name 'process'`，就是这个原因：
>
> ```jsonc
> { "compilerOptions": { "types": ["node"] } }
> ```

---

## 五种运行方式

TypeScript 不能直接被任何运行时执行。类型要么被**擦除**，要么被**转换**成 JS。「哪种方式」只影响开发体验，不影响语言语义。

{{< tabpane text=true persist=disabled >}}

{{% tab header="① tsc 编译后运行" %}}

最标准、产物最可控，生产环境最终都走这条路（或由打包器等价完成）。

```bash
npx tsc                      # 读 tsconfig.json 编译到 outDir
node dist/index.js           # 运行产物
```

常用变体：

| 命令 | 作用 |
| --- | --- |
| `npx tsc --noEmit` | **只类型检查，不产物**——CI 必备 🔥 |
| `npx tsc --watch` | 增量监听编译 |
| `npx tsc --build` | 按项目引用（`references`）拓扑顺序构建 |
| `npx tsc --init` | 生成 `tsconfig.json` |

{{% /tab %}}

{{% tab header="② Node 原生运行 🆕" %}}

Node.js 22.18+ / 24 可**直接执行 `.ts` 文件**，类型在加载时被擦除，不落盘生成 `.js`。

```bash
node index.ts
```

实测（Node v24.20.0）能跑与不能跑的语法：

| 语法 | 结果 | 说明 |
| --- | --- | --- |
| 类型注解、`interface`、`type` | ✅ | 纯擦除 |
| `as`、非空断言 `!`、`satisfies` | ✅ | 纯擦除 |
| `import type` / `export type` | ✅ | 纯擦除 |
| `declare` 声明 | ✅ | 纯擦除 |
| ESM 里 `import "./x.ts"`（带扩展名） | ✅ | Node 要求写全扩展名 |
| **`enum`** | ❌ `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` | 需要**转换** |
| 带运行时代码的 **`namespace`** | ❌ 同上 | 需要**转换** |
| 构造函数**参数属性** `constructor(public a)` | ❌ 同上 | 会生成赋值代码 |

要跑 `enum` 得换开关（会打印 `ExperimentalWarning`）：

```bash
node --experimental-transform-types index.ts
```

> 💡 想让代码**保证**能被 Node 直接跑，就打开 `erasableSyntaxOnly`。它让 `tsc` 主动禁止一切非擦除语法，报错码 `TS1294`。代价是**不能再用 `enum` 和参数属性**——这通常被认为是好事，因为 `enum` 本来就有坑（见 [16 血泪速查]({{< relref "16-Pitfalls-and-Gotchas.md" >}})）。

{{% /tab %}}

{{% tab header="③ tsx / ts-node" %}}

开发期不想手动编译，让工具即时转译。

```bash
npx tsx index.ts                 # 推荐：esbuild 驱动，快，ESM 友好 🔥
npx tsx watch index.ts           # 监听重启
npx ts-node index.ts             # 老牌，可做完整类型检查
```

| 工具 | 类型检查 | 速度 | 适合 |
| --- | --- | --- | --- |
| `tsx` | ❌ 不做 | 快 | 本地开发、脚本 |
| `ts-node` | ✅ 默认做（可关） | 慢 | 需要「检查通过才跑」 |
| `node --watch` | ❌ | 最快 | 配合任一使用做热重启 |

> ⚠️ `tsx` **不做类型检查**。类型错误只能靠编辑器或 `tsc --noEmit` 发现。

{{% /tab %}}

{{% tab header="④ 打包器 / 框架" %}}

Vite、Next.js、Rspack、Bun 等内部完成转译，你**从不手动执行 `tsc`**。

| 场景 | 谁转译 | 谁做类型检查 |
| --- | --- | --- |
| Vite + Vue | esbuild / Rollup | `vue-tsc --noEmit` |
| Vite + React | esbuild / Rollup | `tsc --noEmit` |
| Next.js | SWC | `next build` 内置 + 可加 `tsc --noEmit` |
| Bun | Bun 内置 | `tsc --noEmit` |
| esbuild / SWC 裸用 | 该工具 | **没人做，必须自己加** |

> 🛑 **最危险的误解**：以为「构建成功 = 类型正确」。
>
> esbuild、SWC、Bun 为了速度**只擦除类型，从不检查类型**。下面的代码能正常构建、正常打包，运行时报错：
>
> ```typescript
> const n: number = "这不是数字" as any;   // 打包器完全不管
> ```
>
> CI 里**必须**单独有一条 `tsc --noEmit`。

{{% /tab %}}

{{% tab header="⑤ 浏览器 / 在线" %}}

| 方式 | 用途 |
| --- | --- |
| [TypeScript Playground](https://www.typescriptlang.org/play) | 验证语法、查看 `.d.ts` 推导、分享复现 📘 |
| StackBlitz / CodeSandbox | 带完整工具链的在线项目 |
| `esm.sh` / `jsDelivr` | 直接引用已编译的第三方包 |

Playground 特别适合本速查表的用法：**把每个示例粘进去，鼠标悬停看推导出的类型**。

{{% /tab %}}

{{< /tabpane >}}

---

## `tsc` 命令行速查

### 文件与项目

| 命令 | 说明 |
| --- | --- |
| `tsc` | 读当前目录 `tsconfig.json` 编译 |
| `tsc -p ./tsconfig.build.json` | 指定配置文件 |
| `tsc --init` | 生成一份带注释的 `tsconfig.json` |
| `tsc --showConfig` | 打印**最终生效**的配置（含 `extends` 合并结果）🔥 |
| `tsc --ignoreConfig a.ts` | 忽略 `tsconfig.json`，只编译指定文件 🆕 |
| `tsc a.ts`（且存在 tsconfig） | 🛑 6.0 起报 `TS5112`，见下 |

> **6.0 新增 `TS5112`**：如果目录里有 `tsconfig.json`，同时又在命令行传了文件名，`tsc` 会**报错**而不是忽略配置：
>
> ```text
> error TS5112: tsconfig.json is present but will not be loaded if files are specified
> on commandline. Use '--ignoreConfig' to skip this error.
> ```
>
> 用意是消除「命令行参数悄悄绕过项目配置」这个长期困惑源。加 `--ignoreConfig` 即可恢复旧行为。

### 检查与产物

| 参数 | 作用 |
| --- | --- |
| `--noEmit` | 只检查不产物 🔥 |
| `--emitDeclarationOnly` | 只产 `.d.ts`，不产 `.js`（发库常用） |
| `--outDir dist` | 指定产物目录 |
| `--declaration` / `-d` | 生成 `.d.ts` |
| `--declarationMap` | 生成 `.d.ts.map`，能跳回源码 |
| `--sourceMap` | 生成 `.js.map` |
| `--removeComments` | 产物去掉注释 |
| `--watch` / `-w` | 监听模式 |
| `--build` / `-b` | 项目引用（`references`）增量构建 |
| `--clean` | 配合 `-b`，清理产物 |
| `--force` | 配合 `-b`，强制全量重建 |

### 目标与模块

| 参数 | 说明 |
| --- | --- |
| `--target es2022` | 产物语法级别；6.0 默认已是 `ES2025` |
| `--module nodenext` | 模块格式；Node 项目首选 |
| `--moduleResolution bundler` | 解析策略；打包器项目首选 |
| `--lib es2022,dom` | 可用的内置类型库 |
| `--jsx react-jsx` | JSX 转换方式 |

### 诊断（本页最有价值的部分）

| 参数 | 用来回答什么问题 |
| --- | --- |
| `--noEmit --pretty` | 彩色、带上下文的错误输出（默认开启） |
| `--extendedDiagnostics` | **时间都花哪了**：绑定、检查、emit 各阶段耗时 🔥 |
| `--diagnostics` | 编译统计：文件数、类型数、符号数、内存占用 |
| `--generateTrace ./trace` | 产出 Chrome Trace 格式的性能剖析 🔥 |
| `--explainFiles` | **每个文件为什么被包含进编译** 🔥 |
| `--traceResolution` | **模块解析全过程**：每个 `import` 试了哪些路径、为何失败 🔥 |
| `--listFiles` | 列出实际参与编译的所有文件 |
| `--listFilesOnly` | 只列文件，不编译（快） |
| `--noErrorTruncation` | 不截断超长类型错误信息（看完整类型时必开） |
| `--strict` / `--strict false` | 临时开关严格模式（6.0 已默认 true） |

**排查「类型为什么是这个」的标准动作**：

```bash
# 1. 报错信息被截断了，看不到完整类型
npx tsc --noEmit --noErrorTruncation

# 2. 不知道某个文件为什么被编译进来（幽灵文件、多余 @types）
npx tsc --noEmit --explainFiles | head -50

# 3. 某个 import 解析到了错误的位置
npx tsc --noEmit --traceResolution 2>&1 | grep -A5 "some-package"

# 4. 编译慢，想知道瓶颈
npx tsc --noEmit --extendedDiagnostics
```

`--extendedDiagnostics` 输出解读：

| 指标 | 含义 | 高了说明什么 |
| --- | --- | --- |
| `Parse time` | 解析源码 | 文件太多或太大 |
| `Bind time` | 建立符号表 | 正常应很小 |
| `Check time` | **类型检查** | 通常是主要耗时，复杂类型体操的代价 |
| `Emit time` | 生成产物 | 只影响 `tsc` 直接产物的场景 |
| `Total time` | 总计 | — |
| `Types` / `Instantiations` | 类型实例化次数 | **爆炸式增长说明类型体操过重** |
| `Memory used` | 内存峰值 | 过高会 OOM，需查 `skipLibCheck` / 巨型联合类型 |

> 💭 大多数「`tsc` 好慢」的根因是 **`Instantiations` 数量过大**，也就是泛型/条件类型被反复实例化。缓解手段见 [17 编译器与性能]({{< relref "17-Compiler-Internals-and-Performance.md" >}})。

---

## 错误抑制指令

三者的语义**完全不同**，选错的代价很大。

| 指令 | 作用 | 何时用 |
| --- | --- | --- |
| `// @ts-expect-error` | 断言**下一行一定报错**；不报错反而提示「未使用」 | ✅ 测试负数场景、临时绕过已知问题 🔥 |
| `// @ts-ignore` | 无条件忽略下一行；错不错都不管 | 🛑 几乎不要用，会掩盖问题 |
| `// @ts-nocheck` | 忽略**整个文件** | 🚧 迁移期的临时逃生舱 |
| `// @ts-check` | 在 `.js` 文件里开启检查 | 迁移期逐步试点 |

```typescript
// ✅ 推荐：不仅抑制，还保证「这里确实该报错」
// @ts-expect-error 故意传错类型，验证运行时兜底
doSomething("wrong type");

// 🛑 不推荐：写错了也发现不了
// @ts-ignore
doSomething("wrong type");
```

`@ts-expect-error` 的额外好处：**当上游修复后它会提示你删除**。因为不再报错时，它会变成「未使用的 expect-error」提示，形成自我清理。💭

**作用域**：这三个指令作用于**下一行**（`@ts-nocheck` / `@ts-check` 作用于整个文件，且必须写在文件顶部注释区）。

---

## 迁移期开关（渐进引入类型）

老 JS 项目不必一次性改完。按这个顺序推进，每一步都可运行：

| 阶段 | 配置 | 效果 |
| --- | --- | --- |
| 0 | 什么都不做 | JS 照跑 |
| 1 | `allowJs: true` | 允许 `.ts` 与 `.js` 共存 |
| 2 | `checkJs: true` + 文件头 `// @ts-check` | **逐文件**开始检查 JS |
| 3 | 把文件改名为 `.ts` | 该文件开始强制检查 |
| 4 | 打开 `strict` 相关项 | 收紧（6.0 已默认开） |
| 5 | 删掉 `@ts-ignore`、减少 `any` | 收尾 |

```jsonc
// 阶段 1~2 的典型配置
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,          // 配合 per-file 的 // @ts-check
    "noEmit": true             // 先只检查，产物仍交给原有工具链
  }
}
```

> ⚠️ **6.0 迁移注意**：由于 `strict` 默认变为 `true`，从旧版本升级的项目第一次跑 `tsc` 可能**一次性爆出大量错误**。务实做法是先显式固定：
>
> ```jsonc
> { "compilerOptions": { "strict": false } }   // 先恢复旧行为，再逐项开启
> ```
>
> 然后按 `noImplicitAny` → `strictNullChecks` → 其余 的顺序逐项打开。详见 [15 从 JS 迁移]({{< relref "15-Migrating-JS-to-TS-and-Ecosystem-Interop.md" >}})。

---

## 编辑器：`tsserver`

VS Code 等编辑器用的不是 `tsc`，而是 **`tsserver`**（语言服务）。二者共享同一套类型系统，但**可能使用不同的配置**。

| 现象 | 原因 |
| --- | --- |
| 编辑器报错但 `tsc` 不报 | 编辑器用了嵌套的另一个 `tsconfig.json`，或 TS 版本不同 |
| `tsc` 报错但编辑器不报 | 编辑器用了工作区自带的 TS 版本，或该文件不在任何 `tsconfig` 的 `include` 里 |
| 悬停类型与预期不符 | 大概率是 `strict` 设置或 `lib` 不同 |

排查命令（VS Code）：

| 命令面板项 | 作用 |
| --- | --- |
| `TypeScript: Select TypeScript Version` | 切换用工作区版本还是内置版本 🔥 |
| `TypeScript: Restart TS Server` | 重启语言服务，清掉陈旧状态 🔥 |
| `TypeScript: Open TS Server log` | 看语言服务日志 |

```jsonc
// .vscode/settings.json：强制使用项目内的 TS 版本
{ "typescript.tsdk": "node_modules/typescript/lib" }
```

> 💡 训练肌肉记忆：**编辑器红了先 Restart TS Server**，能解决相当一部分「明明没问题却报错」。

---

## 常见启动问题速查

| 症状 | 原因 | 处理 |
| --- | --- | --- |
| `Cannot find name 'process'` / `'Buffer'` | 6.0 `types` 默认为 `[]` | 加 `"types": ["node"]` |
| `Cannot find name 'describe'` | 同上，缺测试框架全局 | 加 `"types": ["vitest/globals"]` 或 `["jest"]` |
| `Cannot find module './x' or its corresponding type declarations` | 解析策略不匹配 | Node 用 `nodenext`，打包器用 `bundler` |
| `File 'x.ts' is not under 'rootDir'` | 6.0 **不再推断** `rootDir` | 显式设 `"rootDir": "./src"` |
| 产物跑到 `dist/src/...` | 同上 | 同上 |
| `error TS5112` | 命令行传了文件 + 存在 tsconfig | 加 `--ignoreConfig`，或用 `-p` |
| `error TS5101` / `TS5107` | 用了 6.0 废弃选项 | 见 [08 tsconfig]({{< relref "08-tsconfig-Reference.md" >}}) 的废弃清单 |
| `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` | Node 直跑遇到 `enum`/`namespace` | 换 `--experimental-transform-types`，或改用擦除式语法 |
| 改了代码编辑器不更新 | 语言服务状态陈旧 | Restart TS Server |

---

## 一句话总结

| 场景 | 记住这一条 |
| --- | --- |
| CI | 永远有 `tsc --noEmit`，因为它才做类型检查 |
| 本地开发 | `tsx watch` 跑得快，编辑器负责报错 |
| 找编译慢的原因 | `--extendedDiagnostics` 看 `Check time` 和 `Instantiations` |
| 找模块解析问题 | `--traceResolution` |
| 找幽灵文件 | `--explainFiles` |
| 临时绕过错误 | 用 `@ts-expect-error`，不用 `@ts-ignore` |
