+++
title = "15 从 JS 迁移与生态互操作"
weight = 115
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "渐进迁移路线、无类型依赖处理、any 治理、与 lint 和构建工具的边界"
isCJKLanguage = true
draft = false
+++

# 15 从 JS 迁移与生态互操作

把老 JS 项目搬上 TypeScript，难点不在语法，而在**如何在不停工的前提下逐步收紧**。

> ⚠️ **6.0 让迁移变难了一点**：`strict` 默认变为 `true`、`types` 默认变为 `[]`。所以从 5.x 升级或从零引入时，**第一步应该是显式固定这两个选项**，而不是直接吃默认值。详见 [08 tsconfig]({{< relref "08-tsconfig-Reference.md" >}})。

---

## 迁移路线

{{< tabpane text=true persist=disabled >}}

{{% tab header="阶段化推进" %}}

核心原则：**每一步都可运行、可发布、可回滚**。

| 阶段 | 配置 | 产出 |
| --- | --- | --- |
| 0 | 无 | JS 照跑 |
| 1 | `allowJs` + `noEmit` | TS 与 JS 共存，开始有编辑器提示 |
| 2 | `checkJs` + 逐文件 `// @ts-check` | 试点文件开始被检查 |
| 3 | 重命名 `.js` → `.ts`（从叶子文件开始） | 逐文件强制检查 |
| 4 | 打开严格性选项（逐个） | 逐步收紧 |
| 5 | 清理 `any` / `@ts-ignore` | 收尾 |

```jsonc
// 阶段 1~2 的配置：最小侵入
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,      // 先不检查 JS，只让 TS 文件共存
    "noEmit": true,        // 🔥 产物仍交给原有构建工具
    "strict": false,       // ⚠️ 6.0 默认 true，迁移期显式关掉
    "types": ["node"],
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

```jsonc
// 阶段 3：开始改名，此时开 checkJs 做过渡
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "noEmit": true,
    "strict": false
  }
}
```

**为什么 `noEmit: true` 很关键** 🔥：让 `tsc` **只做检查**，产物仍由现有的 Webpack/Vite/Babel 管线生成。这样迁移**不会改变运行时行为**，风险大幅降低。等全部迁完再考虑是否换成 `tsc` 产物。

**改名顺序：从叶子到根**

```text
✅ 正确顺序：
  utils/format.js          ← 无依赖的工具函数，先改
  services/api.js          ← 依赖 utils
  components/Button.jsx    ← 依赖 services
  pages/Home.jsx           ← 依赖 components
  index.js                 ← 最后改入口

🛑 反顺序（先改入口）会一次性暴露所有下游问题
```

| 优先迁移 | 理由 |
| --- | --- |
| 纯工具函数、常量表 | 无依赖，类型简单，收益立刻可见 |
| 数据模型 / API 类型 | 一次定义，全局受益 🔥 |
| 被引用最多的模块 | 改动一处，多处获得类型 |
| 新写的代码 | 从第一天就是 TS ✅ |

| 最后迁移 | 理由 |
| --- | --- |
| 入口文件 | 依赖最多 |
| 构建配置、脚本 | 收益低 |
| 第三方包装层 | 等库自己提供类型 |

{{% /tab %}}

{{% tab header="用 JSDoc 给 JS 加类型" %}}

**不改成 `.ts` 也能获得大部分类型能力**——这是被低估的选项。

```javascript
// @ts-check
/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} name
 * @property {"admin" | "user"} role
 */

/**
 * 按 ID 查找用户。
 * @param {string} id - 用户 ID
 * @param {{ timeout?: number }} [options] - 选项
 * @returns {Promise<User | null>}
 */
export async function findUser(id, options) {
  // id 和 options 都有类型了 ✅
  const res = await fetch(`/api/users/${id}`, { signal: AbortSignal.timeout(options?.timeout ?? 5000) });
  return res.json();
}

/** @type {User[]} */
const cache = [];

/**
 * @template T
 * @param {T[]} items
 * @param {(item: T) => boolean} pred
 * @returns {T | undefined}
 */
function find(items, pred) { return items.find(pred); }
```

| JSDoc 标签 | 对应 TS 语法 |
| --- | --- |
| `@param {string} x` | `x: string` |
| `@returns {number}` | `: number` |
| `@type {User[]}` | `const cache: User[]` |
| `@typedef {Object} X` | `interface X` |
| `@property {string} a` | `a: string` |
| `@template T` | `<T>` |
| `@satisfies {T}` | `satisfies T` |
| `@type {import("./x").Y}` | `import type { Y }` |
| `// @ts-check` | 开启该文件检查 |
| `// @ts-expect-error` | 同 TS |

**JSDoc 的适用场景**：

| 场景 | 适合 |
| --- | --- |
| 不能改文件扩展名（构建配置限制） | ✅ |
| 想边写边加类型，暂不改名 | ✅ |
| 遗留代码，只想修几个热点函数的类型 | ✅ |
| 新代码 | ❌ 直接写 `.ts` 更好 🔥 |
| 复杂泛型 / 条件类型 | ❌ JSDoc 表达力不足 |

> 💭 **JSDoc 是过渡工具，不是终点**。语法比 TS 啰嗦、表达力受限、工具支持也略弱。它的价值在于**零成本启动**——加一行 `// @ts-check` 就能开始受益。

{{% /tab %}}

{{% tab header="渐进式收紧严格性" %}}

**6.0 的 `strict` 默认 `true`**，所以迁移项目第一步要显式关掉，然后逐项打开：

```jsonc
// 迁移起点
{ "compilerOptions": { "strict": false } }
```

**推荐开启顺序**（按「修复成本 / 收益比」排序）：

| 顺序 | 选项 | 修复成本 | 收益 |
| --- | --- | --- | --- |
| 1 | `noImplicitAny` | 中 | 🔥🔥🔥 最高，抓住未标注的参数 |
| 2 | `strictNullChecks` | **高** | 🔥🔥🔥 抓 `null` 相关 bug，但改动最多 |
| 3 | `noImplicitThis` | 低 | 🔥🔥 |
| 4 | `alwaysStrict` | 无 | 🔥 |
| 5 | `strictFunctionTypes` | 低 | 🔥🔥 |
| 6 | `strictBindCallApply` | 低 | 🔥 |
| 7 | `useUnknownInCatchVariables` | 中 | 🔥🔥 |
| 8 | `strictPropertyInitialization` | 中 | 🔥🔥 |
| 9 | `noUncheckedIndexedAccess` | **高** | 🔥🔥🔥 但不在 strict 里，最后开 |
| 10 | `noImplicitOverride` | 低 | 🔥 |
| 11 | `exactOptionalPropertyTypes` | 高 | 🔥 语义变化大，最谨慎 |

```jsonc
// 逐项开启（每次只加一个，修完再加下一个）
{
  "compilerOptions": {
    "strict": false,
    "noImplicitAny": true      // ← 第一步只加这个
  }
}
```

**`strictNullChecks` 的务实策略**（它是最痛的一步）：

```jsonc
// 1. 先只在部分目录开（用额外 tsconfig）
// tsconfig.strict.json
{
  "extends": "./tsconfig.json",
  "compilerOptions": { "strictNullChecks": true },
  "include": ["src/new-feature/**/*"]
}
```

```jsonc
// 2. 或者按目录用 // @ts-strict 之类做不到，就用多配置 + CI 分步检查
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "typecheck:strict": "tsc --noEmit -p tsconfig.strict.json"
  }
}
```

> 🔥 **不要试图一次开完**。`strict: true` 一次性打开在成熟项目上通常意味着几千个错误，团队会直接放弃。**每次一个选项**，配合「新代码必须过、老代码登记 TODO」的策略更现实。

{{% /tab %}}

{{< /tabpane >}}

---

## 无类型依赖的处理

{{< tabpane text=true persist=disabled >}}

{{% tab header="类型来源的优先级" %}}

按这个顺序找，**能不自写就不自写**：

| 优先级 | 来源 | 检查方式 |
| --- | --- | --- |
| 1 | 库**自带**类型（`types` 字段 / `.d.ts`） | 看 `node_modules/包名/package.json` 的 `types` |
| 2 | `@types/包名` | `npm view @types/包名 version` 🔥 |
| 3 | 库作者提供的其它入口 | 查文档 |
| 4 | 自己写最小声明 | 最后手段 |
| 5 | 🛑 `declare module "x": any` 一刀切 | 等于放弃类型 |

```bash
# 快速判断有没有官方类型
npm view @types/express version        # 有输出 = 存在
npm view express types                 # 看库自己是否声明了 types 字段
ls node_modules/express/*.d.ts         # 看产物里有没有声明
```

**先检查是不是「假缺失」**：

| 症状 | 真实原因 |
| --- | --- |
| 报找不到模块，但 `@types` 装了 | `types` 数组没包含，或 `moduleResolution` 不匹配 |
| 报找不到模块，包在子路径 | 包的 `exports` 没暴露该子路径 |
| 只有某个文件报错 | 该文件不在 `include` 里 |

```bash
# 确认解析到底发生了什么
npx tsc --noEmit --traceResolution 2>&1 | grep -A10 "找不到的包名"
```

{{% /tab %}}

{{% tab header="手写最小声明" %}}

原则：**只声明你真正用到的，用 `unknown` 而不是 `any`**。

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
}
```

**写法要点**：

| 要点 | 说明 |
| --- | --- |
| 只写用到的 | 未用到的 API 不用声明 |
| 参数用 `unknown` 而非 `any` | 保留后续收窄的可能 🔥 |
| 返回值尽量具体 | 但不确定时用 `unknown` |
| 加注释写明来源 | 「依据 v2.1 文档」+ 链接 |
| 放在 `src/types/` 并在 `include` 内 | 通常自动包含 |

**逐步细化的策略**：

```typescript
// 第 1 步：先让它能编译（最小信息）
declare module "legacy-lib" {
  const lib: unknown;
  export default lib;
}

// 第 2 步：用到什么补什么
declare module "legacy-lib" {
  export function init(config: { key: string }): void;
  export function send(event: string, payload?: unknown): Promise<void>;
}

// 第 3 步：补充更精确的类型
declare module "legacy-lib" {
  export interface InitConfig {
    key: string;
    endpoint?: string;
    debug?: boolean;
  }
  export function init(config: InitConfig): void;
  export function send(event: string, payload?: Record<string, unknown>): Promise<void>;
}
```

> ⚠️ **手写声明是「对运行时的假设」**，写错了编译器不会发现。所以：
>
> | 做法 | 原因 |
> | --- | --- |
> | 读库的源码或文档 | 别猜 API |
> | 写个最小运行时测试验证 | 确认假设成立 🔥 |
> | 标注 `// 依据: <链接>` | 便于日后核对 |
> | 考虑给 DefinitelyTyped 提 PR | 惠及他人，也获得 review |

{{% /tab %}}

{{% tab header="给 DefinitelyTyped 提 PR" %}}

如果库没有类型，**最好的做法是给它加上**——自己用得上，社区也受益。

基本流程：

```bash
# 1. fork 并克隆 DefinitelyTyped
git clone https://github.com/<你的用户名>/DefinitelyTyped.git
cd DefinitelyTyped

# 2. 创建类型包目录（结构与 npm 包名一致）
mkdir -p types/my-library
```

```jsonc
// types/my-library/package.json
{
  "name": "@types/my-library",
  "version": "1.0.0",
  "projects": ["https://github.com/author/my-library"],
  "dependencies": {},
  "types": "index.d.ts",
  "typeScriptVersion": "5.0"
}
```

```typescript
// types/my-library/index.d.ts
export interface Options {
  key: string;
  debug?: boolean;
}

export function init(options: Options): void;
export function send(event: string, payload?: Record<string, unknown>): Promise<void>;
```

```bash
# 3. 测试（DT 提供工具）
npm test          # 或 npx dtslint types/my-library
npx tsc --noEmit  # 类型检查

# 4. 提交 PR
```

| 检查项 | 要求 |
| --- | --- |
| `index.d.ts` 无 `any`（除必要） | DT 有 lint 规则 |
| 写类型测试（`*.test-d.ts`） | 强烈建议 |
| `package.json` 元数据正确 | `projects`、`typeScriptVersion` |
| 头部注释格式 | DT 有固定模板 |
| 单一 PR 只改一个包 | 便于 review |

> 💭 提 PR 的隐性收益：**会被有经验的维护者 review**，是提升类型编写能力的好途径。如果嫌流程重，也可以先把声明放在自己项目里，稳定后再提交。

{{% /tab %}}

{{< /tabpane >}}

---

## `any` 治理

`any` 是迁移最大的技术债来源。**它不会自己消失，必须有策略。**

{{< tabpane text=true persist=disabled >}}

{{% tab header="先量化再治理" %}}

不知道有多少 `any`，就无法制定目标。

```bash
# 统计显式 any 出现次数
grep -rn ": any" src --include="*.ts" --include="*.tsx" | wc -l

# 分类查看
grep -rn "as any" src --include="*.ts" --include="*.tsx" | wc -l
grep -rn "@ts-ignore" src --include="*.ts" --include="*.tsx" | wc -l
grep -rn "@ts-expect-error" src --include="*.ts" --include="*.tsx" | wc -l
grep -rn "<any>" src --include="*.ts" --include="*.tsx" | wc -l

# 按文件排序，找出重灾区
grep -rc ": any" src --include="*.ts" | sort -t: -k2 -rn | head -20
```

**用 ESLint 规则量化并设门槛**：

```jsonc
// eslint.config.js（flat config，typescript-eslint）
export default [
  {
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      "@typescript-eslint/no-explicit-any": "error",      // 🔥 禁止显式 any
      "@typescript-eslint/no-unsafe-assignment": "error",  // 禁止 any 悄悄传播
      "@typescript-eslint/no-unsafe-member-access": "error",
      "@typescript-eslint/no-unsafe-call": "error",
      "@typescript-eslint/no-unsafe-return": "error",
      "@typescript-eslint/no-floating-promises": "error",  // 漏 await
      "@typescript-eslint/ban-ts-comment": ["error", {
        "ts-ignore": true,        // 🔥 禁止 @ts-ignore
        "ts-expect-error": "allow-with-description",
        "ts-nocheck": "allow-with-description"
      }]
    }
  }
];
```

> 🔥 **`no-unsafe-*` 系列规则需要类型信息**（要配 `parserOptions.project`），这正是 typescript-eslint 独有的能力——它能追踪 `any` 的**传播路径**，比单纯禁止 `: any` 有用得多。

**把 `any` 数量纳入 CI 门槛**：

```bash
#!/bin/bash
# scripts/check-any-budget.sh
MAX_ANY=50
CURRENT=$(grep -rc ": any" src --include="*.ts" | awk -F: '{sum+=$2} END {print sum}')
if [ "$CURRENT" -gt "$MAX_ANY" ]; then
  echo "❌ any 数量 $CURRENT 超过门槛 $MAX_ANY"
  exit 1
fi
echo "✅ any 数量 $CURRENT / $MAX_ANY"
```

```jsonc
// package.json
{ "scripts": { "check:any": "bash scripts/check-any-budget.sh" } }
```

> 💡 **门槛只降不升**：每次减少后就调低 `MAX_ANY`。这样 `any` 数量单调递减，不会因为「反正已经很多了」而继续恶化。

{{% /tab %}}

{{% tab header="替换 any 的决策树" %}}

```text
遇到 any，按顺序问：

1. 这个值的真实类型我确定吗？
   ├─ 确定 → 写上真实类型 ✅
   └─ 不确定 → 继续

2. 它是「外部来的」吗？（API / JSON / env / 用户输入）
   ├─ 是 → 改 unknown + 运行时校验（见 11）🔥
   └─ 否 → 继续

3. 它能用泛型表达吗？
   ├─ 能 → 用泛型 <T> ✅
   └─ 不能 → 继续

4. 它是「任意对象」吗？
   ├─ 是 → Record<string, unknown> ✅
   └─ 否 → 继续

5. 它是「任意值」吗？
   ├─ 是 → unknown ✅
   └─ 否 → 继续

6. 真的是无法表达 → 保留 any，但加注释说明原因 + TODO
```

| 原始写法 | 替换为 | 场景 |
| --- | --- | --- |
| `any` | `unknown` | 任意值，之后要收窄 🔥 |
| `any` | `Record<string, unknown>` | 任意对象 |
| `any[]` | `unknown[]` | 任意数组 |
| `any` | `<T>(x: T) => ...` | 通用函数 |
| `(x: any) => void` | `(x: unknown) => void` | 回调 |
| `Promise<any>` | `Promise<unknown>` | 异步结果 |
| `as any` | `as unknown as T`（仍不理想） | 最后手段 |
| `any` | 具体接口 | 最理想 ✅ |

**`unknown` 替换 `any` 后的连锁修改**：

```typescript
// 🛑 原代码
function process(data: any) {
  return data.items.map((i: any) => i.name).join(", ");
}

// ✅ 改成 unknown 后，编译器会逼你写清楚
function process(data: unknown): string {
  if (
    typeof data === "object" && data !== null &&
    "items" in data && Array.isArray((data as { items: unknown }).items)
  ) {
    const items = (data as { items: unknown[] }).items;
    return items
      .map((i) => (typeof i === "object" && i !== null && "name" in i
        ? String((i as { name: unknown }).name)
        : ""))
      .join(", ");
  }
  return "";
}

// ✅✅ 更好：用 schema 库，一次到位
import { z } from "zod";

const DataSchema = z.object({
  items: z.array(z.object({ name: z.string() })),
});

function process2(data: unknown): string {
  const parsed = DataSchema.safeParse(data);
  if (!parsed.success) return "";
  return parsed.data.items.map((i) => i.name).join(", ");
}
```

> 🔥 **注意 `unknown` 会带来一堆手写收窄代码**。这时应该停下来问：「我是不是在重造 schema 库？」——答案通常是「是」。见 [11 运行时校验]({{< relref "11-Runtime-Validation-and-Boundaries.md" >}})。

{{% /tab %}}

{{% tab header="抑制指令的治理" %}}

```bash
# 统计
grep -rn "@ts-ignore\|@ts-expect-error\|@ts-nocheck" src | wc -l
```

| 指令 | 治理策略 |
| --- | --- |
| `@ts-ignore` | 🛑 全部改成 `@ts-expect-error` 🔥 |
| `@ts-expect-error` | 每条必须写原因；定期清理 |
| `@ts-nocheck` | 登记为待迁移文件，设期限 |

```typescript
// ✅ @ts-expect-error 的正确用法：带原因
// @ts-expect-error 上游库类型定义缺失该重载，见 https://github.com/x/y/issues/123
legacyCall(x);

// 🛑 没有原因的抑制 = 定时炸弹
// @ts-expect-error
legacyCall(x);
```

**`@ts-expect-error` 的自我清理特性** 🔥：当上游修复后，该行不再报错，TS 会报：

```text
error TS2578: Unused '@ts-expect-error' directive.
```

于是 CI 会失败，提醒你删除这条已经没有用的抑制。**这是 `@ts-ignore` 完全没有的好处**。

```typescript
// 🛑 危险的 @ts-nocheck：整个文件不再检查
// @ts-nocheck
// TODO(2026-Q2): 迁移本文件，见 #1234
export function legacyStuff(x) { /* ... 全是隐式 any ... */ }
```

**`@ts-nocheck` 的登记表**（放在仓库里，避免遗忘）：

```markdown
<!-- docs/ts-migration-todo.md -->
| 文件 | 原因 | 负责人 | 期限 |
| --- | --- | --- | --- |
| `src/legacy/payment.ts` | 依赖已下线的 SDK | @alice | 2026-Q2 |
| `src/legacy/report.ts` | 复杂类型体操失败 | @bob | 2026-Q3 |
```

> 💭 **`@ts-nocheck` 比 `any` 更危险**，因为它让**整个文件**失去保护，包括新加的代码。如果必须用，一定要有登记和期限，否则会永久留存。

{{% /tab %}}

{{< /tabpane >}}

---

## 与生态工具的边界

{{< tabpane text=true persist=disabled >}}

{{% tab header="类型检查 vs lint" %}}

**两者互补，不能互相替代。**

| 问题 | 类型检查（tsc） | lint（ESLint） |
| --- | --- | --- |
| 拼错的属性名 | ✅ | ❌ |
| 类型不匹配 | ✅ | ❌ |
| 漏处理联合分支 | ✅ | ❌ |
| 未使用的变量 | ⚠️ 有选项但不推荐 | ✅ 🔥 |
| 漏 `await` | ❌ | ✅（需类型信息） |
| `any` 传播 | ❌ | ✅（需类型信息） |
| 代码风格 | ❌ | ✅ |
| 反模式（如 `==`） | ❌ | ✅ |
| Hook 依赖完整性 | ❌ | ✅（`react-hooks` 规则） |

```jsonc
// tsconfig 里不要开这些「风格类」检查
{
  "compilerOptions": {
    "noUnusedLocals": false,      // ← 交给 ESLint
    "noUnusedParameters": false   // ← 交给 ESLint
  }
}
```

> 💭 **建议的类型/lint 分工**：
>
> | 交给 `tsc` | 交给 ESLint |
> | --- | --- |
> | 类型正确性 | 代码风格 |
> | 未处理的分支 | 未使用变量 |
> | 结构不匹配 | 漏 `await`、`any` 传播 |
> | 严格性开关 | 框架特定规则 |
>
> 理由：`noUnusedLocals` 报错会**中断编译**，而「有个变量没用」通常不该阻止构建。

**typescript-eslint 的「类型感知」规则**（需要配置 project）：

```jsonc
// eslint.config.js
import tseslint from "typescript-eslint";

export default tseslint.config(
  ...tseslint.configs.recommendedTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,          // 🔥 自动发现 tsconfig
        tsconfigRootDir: import.meta.dirname
      }
    }
  }
);
```

| 规则 | 作用 |
| --- | --- |
| `no-floating-promises` | 漏 `await` 的 Promise 🔥 |
| `no-misused-promises` | 把 Promise 传给期望 `void` 的位置 |
| `await-thenable` | 对非 Promise `await` |
| `no-unsafe-*` 系列 | `any` 传播路径 🔥 |
| `require-await` | `async` 函数里没 `await` |
| `strict-boolean-expressions` | 隐式真值判断（可选，较严格） |
| `switch-exhaustiveness-check` | 穷尽性检查（比 `never` 技巧更早发现） |

> 🔥 **`switch-exhaustiveness-check` 值得单独提**：它在 `switch` 漏分支时直接报错，不需要你写 `default: never` 那套技巧。

{{% /tab %}}

{{% tab header="与打包器的分工" %}}

| 工具 | 转译 | 类型检查 |
| --- | --- | --- |
| `tsc` | ✅ | ✅ |
| esbuild | ✅ | ❌ |
| SWC | ✅ | ❌ |
| Vite（dev） | ✅ | ❌ |
| Babel | ✅ | ❌ |
| Bun | ✅ | ❌ |
| `tsx` | ✅ | ❌ |

> 🛑 **最重要的一条认知**：上表里除 `tsc` 外**都不做类型检查**。「构建成功」不代表「类型正确」。

```jsonc
// 典型的前端项目分工
{
  "scripts": {
    "dev": "vite",                        // 快速转译，类型错误不影响 HMR
    "build": "tsc --noEmit && vite build", // 🔥 构建前必须类型检查
    "typecheck": "tsc --noEmit --watch"   // 开发时单独跑
  }
}
```

**为什么打包器不做类型检查**：类型检查需要**跨文件分析**（整个程序的类型信息），而 esbuild/SWC 追求的是**单文件、可并行**的极致速度。这是刻意的设计取舍，不是缺陷。

**`isolatedModules` 为何必需**：单文件转译无法判断「这个 import 是类型还是值」，所以要开 `isolatedModules` + `verbatimModuleSyntax` 强制你写清楚。见 [07 模块系统]({{< relref "07-Modules-and-Declaration-Files.md" >}})。

{{% /tab %}}

{{% tab header="Monorepo 与项目引用" %}}

多包仓库的两种做法：

| 做法 | 说明 | 适合 |
| --- | --- | --- |
| **各自独立 tsconfig** | 每个包自己检查 | 简单，但重复检查公共依赖 |
| **项目引用（`references`）** | 声明包间依赖，增量构建 | monorepo 🔥 |

```jsonc
// 根 tsconfig.json ——solution 文件
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
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,          // 🔥 必需
    "declaration": true,        // 🔥 composite 隐含要求
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src"],
  "references": [
    { "path": "../types" }      // 声明依赖
  ]
}
```

```bash
npx tsc --build              # 按拓扑顺序构建所有包
npx tsc --build --watch      # 监听
npx tsc --build --clean      # 清理
```

| 项目引用带来的 | 说明 |
| --- | --- |
| 增量构建 | 只重建变化的包 🔥 |
| 强制边界 | 不能 import 未声明的依赖包 |
| 正确的检查顺序 | 依赖先检查 |
| 成本 | 配置复杂，需要 `composite` + `declaration` |

⚠️ **项目引用的常见坑**：

| 症状 | 原因 |
| --- | --- |
| `Referenced project must have composite: true` | 忘了 `composite` |
| `File is not listed within the file list of project` | 被引用的文件不在对方的 `include` 里 |
| 改了代码不重新检查 | 需要 `--build` 而不是 `tsc` |
| `.tsbuildinfo` 陈旧 | `--build --force` 或删掉它 |

> 💭 **小项目不要上项目引用**。配置复杂度和收益不成比例。**包数超过 5 个、或构建时间超过 30 秒**时再考虑。

{{% /tab %}}

{{< /tabpane >}}

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 一上来就 `strict: true` | 几千个错误，团队放弃 | 逐项开启 🔥 |
| 6.0 下没固定 `strict` | 吃了新默认值，错误暴增 | 显式 `strict: false` 起步 |
| 6.0 下没配 `types` | 找不到 `process` | `types: ["node"]` |
| 迁移时改了产物 | 运行时行为变化 | `noEmit: true`，产物交给原工具链 |
| 从入口文件开始改名 | 一次性暴露所有问题 | 从叶子文件开始 |
| 用 `declare module "x": any` | 等于没类型 | 写最小声明 |
| 手写声明靠猜 | 运行时崩溃 | 读源码 + 写测试验证 |
| `any` 没有量化 | 无法制定目标 | 统计 + CI 门槛 🔥 |
| 门槛只设不降 | 债越积越多 | 每次减少就调低门槛 |
| 保留 `@ts-ignore` | 上游修好也不知道 | 全改 `@ts-expect-error` |
| `@ts-nocheck` 无期限 | 永久留存 | 登记表 + 期限 |
| 以为打包器会检查类型 | 类型错误进主干 | CI 里加 `tsc --noEmit` 🔥 |
| 小项目上项目引用 | 配置复杂收益低 | 包多了再上 |
