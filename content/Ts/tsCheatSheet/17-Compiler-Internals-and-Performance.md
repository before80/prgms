+++
title = "17 编译器与性能"
weight = 117
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "编译变慢怎么查、extendedDiagnostics 指标解读、项目引用、isolatedDeclarations 与 TS 7.0 迁移前瞻"
isCJKLanguage = true
draft = false
+++

# 17 编译器与性能

「`tsc` 好慢」是可以**量化定位**的，不用猜。本页讲清楚每个诊断指标的含义和对应的解法。

> 本页所有命令输出格式均在 TS 6.0.3 实测。

---

## 编译流水线

理解阶段划分，才能把「慢」定位到具体环节。

| 阶段 | 做什么 | 慢的典型原因 |
| --- | --- | --- |
| **Parse**（解析） | 源码 → AST | 文件过多、单文件过大 |
| **Bind**（绑定） | AST → 符号表 | 通常很快 |
| **Check**（检查） | 类型推导与比较 | **绝大多数性能问题的所在** 🔥 |
| **Emit**（产物） | 生成 JS / `.d.ts` | 只在 `tsc` 直接产物时相关 |
| **ResolveModule**（解析模块） | 定位 `import` 目标 | 解析策略配置不当、路径太深 |

关键认知：**`Check` 阶段是耗时主体**，而它的耗时几乎完全由**类型实例化次数**决定。

```text
源文件 ──Parse──> AST ──Bind──> 符号表 ──Check──> 类型图 ──Emit──> JS/.d.ts
                                ▲
                                └── 慢在这里，且主要由「类型体操」造成
```

---

## 诊断：先量化再优化

{{< tabpane text=true persist=disabled >}}

{{% tab header="extendedDiagnostics" %}}

```bash
npx tsc --noEmit --extendedDiagnostics
```

**实测输出**（TS 6.0.3，一个 61 文件的小项目）：

```text
Lines of TypeScript:           183
Lines of JavaScript:             0
Lines of JSON:                   0
Lines of Other:                  0
Identifiers:                 50264
Symbols:                     57593
Types:                       30622
Instantiations:              32819
Memory used:               117906K
Assignability cache size:    12684
Identity cache size:             0
Subtype cache size:              0
Strict subtype cache size:       4
I/O Read time:               0.01s
Parse time:                  0.09s
ResolveModule time:          0.00s
Program time:                0.12s
Bind time:                   0.04s
Check time:                  0.41s
printTime time:              0.00s
Emit time:                   0.00s
Total time:                  0.57s
```

**指标解读**：

| 指标 | 含义 | 关注点 |
| --- | --- | --- |
| `Lines of TypeScript` | 参与编译的 TS 行数 | 是否比预期多很多（幽灵文件） |
| `Identifiers` | 标识符总数 | 突然很大说明 `@types` 被全量加载 |
| `Symbols` | 符号数 | 同上 |
| `Types` | 创建的类型对象数 | 类型定义过多 |
| **`Instantiations`** | **类型实例化次数** | 🔥 **最重要**，爆炸就是类型体操过重 |
| `Memory used` | 内存峰值 | 过高会 OOM |
| `Assignability cache size` | 可赋值性缓存条目 | 大量类型比较 |
| `Parse time` | 解析耗时 | 大 → 文件多/大 |
| `Bind time` | 绑定耗时 | 通常很小 |
| **`Check time`** | **类型检查耗时** | 🔥 通常占总时间的大头 |
| `Emit time` | 产物生成耗时 | 只影响直接产物 |
| `Total time` | 总耗时 | — |

**判断标准**（经验值 💭）：

| 指标 | 健康范围 | 需要警惕 |
| --- | --- | --- |
| `Check time` 占比 | < 70% 总时间 | > 85% |
| `Instantiations` | 十万量级 | **百万以上** ⚠️ |
| `Types` | 几万 | 数十万 |
| `Bind time` | 远小于 Check | 与 Check 相当 |
| `Memory used` | < 1–2 GB | > 3 GB（易 OOM） |

> 🔥 **`Instantiations` 是核心指标**。它统计泛型被「填上具体类型」的次数。一个 `DeepReadonly<DeepPartial<UnionToIntersection<T>>>` 这种组合会在每个使用点产生大量实例化。**如果 `Instantiations` 到百万级，先简化类型，别急着调配置。**

{{% /tab %}}

{{% tab header="generateTrace" %}}

想知道**具体哪个文件、哪个类型**最耗时，用 trace。

```bash
npx tsc --noEmit --generateTrace ./trace
```

**实测产出**：

```text
trace/
├── trace.json     # 时间线（Chrome Trace 格式）
└── types.json     # 类型与实例化统计
```

打开方式：把 `trace.json` 拖进 `chrome://tracing`，或用 [Perfetto UI](https://ui.perfetto.dev/)。

**`types.json` 才是排查类型爆炸的关键**——它记录了哪些类型被实例化得最多。可以用脚本聚合：

```javascript
// analyze-types.mjs —— 找出实例化最多的类型
import { readFileSync } from "node:fs";

const data = JSON.parse(readFileSync("./trace/types.json", "utf8"));
const counts = new Map();

function walk(node) {
  if (!node || typeof node !== "object") return;
  if (node.name && node.count) {
    const key = `${node.name} (${node.kind ?? "?"})`;
    counts.set(key, (counts.get(key) ?? 0) + node.count);
  }
  for (const v of Object.values(node)) walk(v);
}
walk(data);

const top = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 30);
for (const [name, count] of top) {
  console.log(String(count).padStart(9), name.slice(0, 110));
}
```

```bash
node analyze-types.mjs
```

典型输出会指出某个类型名被实例化几十万次——**那就是要优化的目标**。

| 观察到的现象 | 可能原因 |
| --- | --- |
| 某个泛型工具类型实例化极多 | 在热点路径反复使用复杂条件类型 |
| 某个第三方类型的实例化占大头 | 该库的类型定义过重 |
| 大量实例化来自 `.d.ts` | 某个 `@types` 包的类型太复杂 |
| 检查时间集中在少数文件 | 这些文件的类型最复杂 |

> 💡 **`types.json` 比 `trace.json` 更有用**。时间线告诉你「哪慢」，`types.json` 告诉你「为什么慢」。

{{% /tab %}}

{{% tab header="其它诊断参数" %}}

| 参数 | 回答什么 |
| --- | --- |
| `--diagnostics` | 简版统计 |
| `--explainFiles` | 每个文件为什么被包含 🔥 |
| `--listFiles` | 实际参与编译的文件 |
| `--listFilesOnly` | 只列文件不编译 |
| `--traceResolution` | 模块解析全过程 |
| `--noErrorTruncation` | 完整类型错误 |

```bash
# 找出意外的文件（幽灵文件、多余 @types）
npx tsc --noEmit --explainFiles | head -60

# 找出编译了多少文件（对比预期）
npx tsc --noEmit --listFiles | wc -l
```

> 🔥 **编译慢的第一嫌疑人是「编译了不该编译的文件」**。常见来源：
>
> | 来源 | 表现 |
> | --- | --- |
> | `include` 太宽（含了 `dist`、`node_modules`） | 文件数远超预期 |
> | 6.0 之前 `types` 自动加载全部 `@types` | `Identifiers` / `Symbols` 巨大 |
> | 测试文件被纳入产物编译 | `dist` 里出现 `.test.js` |
> | `@types` 包版本重复 | 同名符号多份 |

{{% /tab %}}

{{< /tabpane >}}

---

## 性能优化手段

按**收益 / 成本比**排序，从最划算的开始。

{{< tabpane text=true persist=disabled >}}

{{% tab header="① 配置层（最高性价比）" %}}

```jsonc
{
  "compilerOptions": {
    "skipLibCheck": true,        // 🔥 收益最大，几乎必开
    "incremental": true,         // 增量编译
    "tsBuildInfoFile": "./node_modules/.cache/tsbuildinfo"
  },
  "include": ["src"],            // 🔥 精确限定
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

| 手段 | 收益 | 代价 |
| --- | --- | --- |
| `skipLibCheck: true` | 🔥🔥🔥 大 | 不检查 `.d.ts`（含自己写的） |
| 精确 `include` / `exclude` | 🔥🔥🔥 大 | 需要维护 |
| `incremental: true` | 🔥🔥 二次编译快 | 生成 `.tsbuildinfo` |
| `types: []` 显式列出 | 🔥🔥 大 | 需要显式 import 全局类型 |
| 减少 `lib` | 🔥 中 | 可能缺类型 |
| `noUnusedLocals: false` | 🔥 小 | 交给 lint |

**`types` 的影响常常被低估**：6.0 之前自动加载全部 `@types/*`，一个装了 40 个 `@types` 的项目，其中 38 个可能完全用不到，却全部参与类型检查。

```jsonc
// 🛑 隐式加载全部 @types（5.x 的行为）
{}

// ✅ 6.0 默认已是 []，显式列出真正需要的
{ "compilerOptions": { "types": ["node"] } }

// ⚠️ 不要为了省事写这个（会加载全部，拖慢编译）
{ "compilerOptions": { "types": ["*"] } }
```

**`--explainFiles` 找出多余文件**：

```bash
npx tsc --noEmit --explainFiles | grep -E "^node_modules|^\.\./" | head -30
```

{{% /tab %}}

{{% tab header="② 类型层（治本）" %}}

性能问题的根因通常在类型设计。

| 反模式 | 问题 | 改法 |
| --- | --- | --- |
| 深层递归类型 | 实例化爆炸 | 加深度计数器限制 |
| 在每个使用点展开复杂工具类型 | 重复实例化 | **起个具名别名缓存** 🔥 |
| 巨型联合（几百个成员） | 每次比较都遍历 | 分层，或用可辨识联合 |
| 交叉类型嵌套很深 | 展开成本高 | 用 `interface extends` |
| 条件类型套条件类型 | 组合爆炸 | 拆成多步，用具名中间类型 |
| `keyof` 巨型对象 | 生成巨大联合 | 缩小范围 |

```typescript
// 🛑 类型内联展开：每个使用点都重新计算
function a<T>(x: T): DeepReadonly<DeepPartial<Prettify<T>>> { /* ... */ }
function b<T>(x: T): DeepReadonly<DeepPartial<Prettify<T>>> { /* ... */ }
function c<T>(x: T): DeepReadonly<DeepPartial<Prettify<T>>> { /* ... */ }

// ✅ 具名别名：编译器可复用计算结果
type FrozenPatch<T> = DeepReadonly<DeepPartial<Prettify<T>>>;
function a2<T>(x: T): FrozenPatch<T> { /* ... */ }
function b2<T>(x: T): FrozenPatch<T> { /* ... */ }
function c2<T>(x: T): FrozenPatch<T> { /* ... */ }
```

```typescript
// 🛑 深递归无限制
type DeepReadonly<T> = { readonly [K in keyof T]: DeepReadonly<T[K]> };

// ✅ 加深度计数器
type Prev = [never, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
type SafeDeepReadonly<T, D extends number = 5> = D extends 0
  ? T
  : { readonly [K in keyof T]: SafeDeepReadonly<T[K], Prev[D]> };
```

```typescript
// 🛑 深交叉：展开成本随层数增长
type A = B & C & D & E & F & G & H & I & J;

// ✅ 用 interface 继承（编译器处理得更高效，错误信息也更清晰）
interface A2 extends B, C, D, E, F, G, H, I, J {}
```

> 🔥 **`interface extends` 优于 `type &`**：不仅是可读性，编译器对接口继承的处理路径更短，且错误信息会显示接口名而不是展开整个交叉类型。

{{% /tab %}}

{{% tab header="③ 工程结构（大项目）" %}}

```jsonc
// 根 tsconfig.json ——解决方案文件
{
  "files": [],
  "references": [
    { "path": "./packages/types" },
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
    "incremental": true,
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src"],
  "references": [{ "path": "../types" }]
}
```

```bash
npx tsc --build            # 按拓扑顺序增量构建 🔥
npx tsc --build --watch    # 监听
npx tsc --build --clean    # 清理
npx tsc --build --force    # 强制全量
```

| 项目引用带来的 | 说明 |
| --- | --- |
| 增量复用 | 未变化的包不重新检查 🔥 |
| 明确边界 | 不能 import 未声明的依赖 |
| 并行构建 | 无依赖关系的包可并行 |

⚠️ **项目引用的成本**：

| 成本 | 说明 |
| --- | --- |
| 配置复杂 | 每个包都要 `composite` + `declaration` |
| 必须用 `--build` | 直接 `tsc` 不走引用逻辑 |
| `.tsbuildinfo` 管理 | 陈旧会导致行为异常 |
| 循环引用不允许 | 需要重构依赖 |

> 💭 **什么时候值得上项目引用**：包数 > 5、或全量检查 > 30 秒、或团队规模大。小项目上它纯属负担。

**`isolatedDeclarations` 加速声明生成** 🆕：

```jsonc
{
  "compilerOptions": {
    "declaration": true,
    "isolatedDeclarations": true    // 声明生成不再依赖类型推断，可并行
  }
}
```

```typescript
// 代价：所有导出必须有显式返回类型
export function f(x: number): number { return x * 2; }
//                 ~~~~~~~~~~~~~~~ 必须写，否则 TS9007
```

| 收益 | 代价 |
| --- | --- |
| 声明生成可并行、可缓存 🔥 | 手写所有返回类型 |
| 声明与实现解耦 | 依赖推断的技巧写不出来 |
| 大库构建显著加快 | 需要 `declaration` 或 `composite` |

{{% /tab %}}

{{% tab header="④ CI 与缓存" %}}

```yaml
# .github/workflows/ci.yml
jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm

      # 🔥 缓存 .tsbuildinfo，让增量生效
      - uses: actions/cache@v4
        with:
          path: |
            **/*.tsbuildinfo
            node_modules/.cache
          key: tsbuildinfo-${{ hashFiles('**/*.ts', '**/tsconfig*.json') }}
          restore-keys: tsbuildinfo-

      - run: npm ci
      - run: npx tsc --noEmit --incremental
```

| 手段 | 效果 |
| --- | --- |
| 缓存 `.tsbuildinfo` | 二次 CI 显著变快 🔥 |
| 缓存 `node_modules` | 省安装时间 |
| `--incremental` | 必须与缓存配合才有意义 |
| 并行跑 lint / test | 墙钟时间下降 |

> ⚠️ **`--incremental` 与 `--noEmit` 一起用**需要注意：`--noEmit` 时 TS 仍会写 `.tsbuildinfo`（用于缓存检查结果），但**不会**写产物。确保缓存路径包含所有 `*.tsbuildinfo`。

**在 CI 里设性能门槛**（防止劣化）：

```bash
#!/bin/bash
# scripts/check-ts-perf.sh
OUTPUT=$(npx tsc --noEmit --extendedDiagnostics 2>&1)
INSTANTIATIONS=$(echo "$OUTPUT" | grep "Instantiations:" | grep -oE "[0-9]+")
MAX=500000

echo "Instantiations: $INSTANTIATIONS (门槛 $MAX)"
if [ "$INSTANTIATIONS" -gt "$MAX" ]; then
  echo "❌ 类型实例化数量超门槛，可能有类型体操过重"
  echo "$OUTPUT" | tail -20
  exit 1
fi
```

> 💭 这类门槛的价值在于**防劣化**——单次提交看不出问题，但类型复杂度是「温水煮青蛙」式增长的。

{{% /tab %}}

{{< /tabpane >}}

---

## 编译器内部：语言服务

除了 `tsc`，还有个常被忽略的组件。

| 组件 | 用途 | 使用者 |
| --- | --- | --- |
| `tsc` | 命令行编译器 | 构建、CI |
| `tsserver` | 语言服务（长驻进程） | VS Code 等编辑器 |

**两者共享类型系统，但可能用不同配置**：

| 差异点 | `tsc` | `tsserver` |
| --- | --- | --- |
| 配置来源 | 你指定的 `-p` | 文件所在目录最近的 `tsconfig.json` |
| TS 版本 | `node_modules` 里的 | 编辑器内置或工作区版本 |
| 缓存 | 进程级 | 长驻内存，状态会陈旧 |

```jsonc
// .vscode/settings.json —— 强制用工作区版本
{ "typescript.tsdk": "node_modules/typescript/lib" }
```

**排查「编辑器与 CI 不一致」**：

```bash
# 1. 看 tsc 实际用的配置
npx tsc --showConfig

# 2. 在编辑器里跑 "TypeScript: Select TypeScript Version"
#    确认版本与 node_modules 一致

# 3. 重启语言服务
#    命令面板 → "TypeScript: Restart TS Server"
```

| 症状 | 原因 |
| --- | --- |
| 编辑器红、CI 绿 | 语言服务状态陈旧，或用了不同配置 |
| CI 红、编辑器绿 | 编辑器用了不同的 TS 版本 |
| 类型提示与预期不符 | `lib` / `strict` 设置不同 |

**编辑器性能问题**（大项目常见）：

| 症状 | 处理 |
| --- | --- |
| 悬停卡顿 | 简化类型，加快 `Prettify` 具名化 |
| 自动补全慢 | 缩小 `include`，减少 `@types` |
| 打开文件慢 | 检查是否在编译范围内 |
| 内存占用高 | `disableSizeLimit` 谨慎使用 |

```jsonc
// .vscode/settings.json
{
  "typescript.tsserver.maxTsServerMemory": 4096,
  "typescript.disableAutomaticTypeAcquisition": true   // 禁掉自动下载 @types 🔥
}
```

> 🔥 `typescript.disableAutomaticTypeAcquisition` 值得加上：编辑器默认会**自动下载** `@types` 包，这在大型项目里会悄悄增加编译负担。

---

## TypeScript 7.0 前瞻

7.0 是**用 Go 重写的原生编译器**（代号 Corsa），与 6.0 的关系：

```text
5.9  ──>  6.0  ──>  7.0
         (桥接版本)   (Go 原生编译器)
          对齐行为      性能大幅提升
          清理废弃      移除全部废弃项
```

| 维度 | 6.0（JS 实现） | 7.0（Go 实现） |
| --- | --- | --- |
| 语言 | TypeScript/JavaScript | Go |
| 并发 | 单线程 + 部分并行 | **共享内存多线程** 🔥 |
| 类型系统 | 同一套 | 同一套（目标一致） |
| 废弃选项 | 报错但可 `ignoreDeprecations` | **彻底移除** |
| 语言服务 | `tsserver` | 原生语言服务 |

**6.0 已经为 7.0 做了哪些对齐**（本速查表覆盖到的）：

| 6.0 的变化 | 目的 |
| --- | --- |
| `strict` 默认 `true` | 与 7.0 默认一致 |
| `target` 默认 `ES2025` | 同上 |
| `types` 默认 `[]` | 行为可预测 |
| `rootDir` 不再推断 | 消除隐式行为 |
| 废弃 `baseUrl` / `outFile` / `node10` 等 | 7.0 将移除 |
| `import assertions` → `import attributes` | 对齐标准 |
| CLI 传文件 + tsconfig 报 `TS5112` | 消除歧义 |

**为 7.0 做准备的建议**：

| 建议 | 原因 |
| --- | --- |
| 现在就把 6.0 的废弃报错修掉 | 7.0 会直接失败 🔥 |
| 不要依赖 `ignoreDeprecations` 长期运行 | 它只是过渡 |
| 显式写 `strict` / `target` / `types` | 不依赖默认值变化 |
| 打开 `isolatedDeclarations` | 7.0 的并行声明生成受益 🔥 |
| 保持 `tsc --noEmit` 干净 | 直接反映 7.0 的就绪度 |

**验证 7.0 就绪度的实用方法**：

```bash
# 1. 确保没有废弃报错（不加 ignoreDeprecations 也能过）
npx tsc --noEmit

# 2. 试跑原生预览版（如果可用）
npx @typescript/native-preview --noEmit

# 3. 对比两者的诊断输出
```

> 💭 **迁移到 7.0 的心理准备**：类型系统本身**不会变**，所以你的类型代码不需要重写。要改的是**配置**（废弃选项）和**构建流程**（性能特征变化可能暴露新的瓶颈）。**现在保持 6.0 干净，7.0 就基本是换一个更快的 `tsc`。**

---

## 性能问题速查

| 症状 | 先查什么 | 常见解法 |
| --- | --- | --- |
| `tsc` 整体慢 | `--extendedDiagnostics` 看 `Check time` 占比 | `skipLibCheck`、缩小 `include` |
| `Instantiations` 百万+ | `--generateTrace` + 分析 `types.json` | 简化类型、具名别名 🔥 |
| 编译文件数远超预期 | `--explainFiles` | 收紧 `include`，检查 `@types` |
| 内存 OOM | `Memory used` 指标 | 减少类型复杂度，拆项目 |
| 增量不生效 | `.tsbuildinfo` 是否存在/被清 | 配置缓存目录 |
| 编辑器卡顿 | TS Server 日志 | 简化类型，加内存上限 |
| 某模块解析慢 | `--traceResolution` | 检查 `paths`、`exports` 配置 |
| 构建产物阶段慢 | `Emit time` | 用打包器替代 `tsc` 产物 |
| 二次构建没有变快 | 是否用了 `--build` / `--incremental` | 上项目引用 + 缓存 |

**优化优先级清单**（按性价比）🔥：

1. `skipLibCheck: true`
2. 精确 `include` / `exclude`（用 `--explainFiles` 验证）
3. `types` 只列必需项
4. 简化热点类型（用 `--generateTrace` 定位）
5. `incremental` + CI 缓存
6. `interface extends` 替代深交叉
7. 项目引用（包多时）
8. `isolatedDeclarations`（库项目）

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 只看 `Total time` 不看细分 | 不知道瓶颈在哪 | 看 `Check time` 占比 |
| 优化配置但不看类型 | 收益有限 | 先看 `Instantiations` 🔥 |
| `include` 太宽 | 编译了 `dist`、测试 | `--explainFiles` 验证 |
| 开了 `types: ["*"]` | 加载全部 `@types`，变慢 | 显式列出 |
| 类型内联不具名 | 重复实例化 | 起具名别名 |
| 深递归无限制 | `TS2589` / 极慢 | 加深度计数器 |
| 小项目上项目引用 | 配置复杂收益低 | 包多了再上 |
| 编辑器自动下载 `@types` | 悄悄增加负担 | `disableAutomaticTypeAcquisition` |
| 以为编辑器 = `tsc` | 两边报错不一致 | 对比 `--showConfig`，Restart TS Server |
| 长期依赖 `ignoreDeprecations` | 7.0 会失败 | 现在就修掉废弃项 🔥 |
