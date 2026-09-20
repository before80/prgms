+++
title = "11 运行时校验与边界"
weight = 111
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "类型在运行时不存在——JSON、环境变量、API 边界的运行时校验方案与 schema 库对照"
isCJKLanguage = true
draft = false
+++

# 11 运行时校验与边界

**这是整套速查表里最重要的一页。**

TypeScript 的类型在运行时**完全不存在**。所有「外部来的数据」——HTTP 响应、`JSON.parse`、`localStorage`、环境变量、表单、URL 参数、IPC 消息——**没有任何一个字节被校验过**。

```typescript
const user: User = await res.json();
// 这一行什么都没检查。类型注解只是你的许愿。
```

本页讲怎么把这条边界守住。

> 示例中的 zod 4.6.5 与 valibot 1.5.0 均在 TS 6.0.3 `strict` 下实测编译通过。

---

## 问题到底出在哪

{{< tabpane text=true persist=disabled >}}

{{% tab header="any 的静默穿透" %}}

`any` 可以赋给**任何**类型，所以类型注解在这里**完全不起作用**：

```typescript
interface User { id: number; name: string }

// res.json() 的返回类型是 any
const user: User = await res.json();   // ✅ 编译通过！没有任何检查

// 运行时真实数据是 { id: "1", username: "a" }
user.name.toUpperCase();   // 💥 TypeError: Cannot read properties of undefined
```

**关键认知**：把 `any` 赋给 `User` **不会触发任何检查**，因为 `any` 是所有类型的子类型。

| 写法 | 编译期检查 | 运行期检查 |
| --- | --- | --- |
| `const u: User = await res.json()` | ❌ 无 | ❌ 无 |
| `const u = await res.json() as User` | ❌ 无 | ❌ 无 |
| `const u = UserSchema.parse(await res.json())` | ✅ 有 | ✅ **有** 🔥 |

**更隐蔽的版本**：类型没写错，但**撒谎**了。

```typescript
// 声明说返回 User，实际服务端可能返回任何东西
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  return res.json();     // ⚠️ 返回值类型是 any，被静默当成了 User
}
```

这个函数**看起来完全类型安全**：有返回类型标注、有泛型、调用方拿到 `User`。但整个链路一次校验都没有。

{{% /tab %}}

{{% tab header="所有不可信的入口" %}}

凡是不由你的代码**构造**出来的值，都必须校验。

| 入口 | 类型 | 真实风险 |
| --- | --- | --- |
| `await res.json()` | `any` | 字段缺失、类型不符、结构变化 |
| `JSON.parse(s)` | `any` | 同上 |
| `localStorage.getItem(k)` | `string \| null` | 旧版本残留数据、被用户改过 |
| `process.env.X` | `string \| undefined` | 缺失、拼错、类型是字符串 |
| `new URLSearchParams(location.search)` | `string \| null` | 用户可以随便改 |
| `form.elements` / `FormData` | 各种 | 用户输入 |
| 文件内容 / `fs.readFile` | `string`/`Buffer` | 内容任意 |
| 数据库查询结果 | 取决于 ORM | 迁移不同步 |
| IPC / Worker 消息 | `unknown` | 跨进程不可信 |
| `postMessage` 收到的数据 | 事件对象 | 来源不可信 |
| 第三方 SDK 回调 | 库声明的类型 | 库的类型可能不准 |
| WebSocket 消息 | `string`/`Blob` | 同上 |
| Cookie | `string \| undefined` | 用户可改 |
| 命令行参数 | `string[]` | 用户输入 |

> 🔥 **一条实用规则**：**凡是跨越了「你的代码边界」的数据，都当作 `unknown` 处理**。边界的定义是：进程边界、网络边界、用户输入边界、持久化边界。

{{% /tab %}}

{{% tab header="三种应对策略" %}}

| 策略 | 做法 | 适合 |
| --- | --- | --- |
| **手写类型守卫** | 自己写 `v is T` 函数 | 结构简单、只校验几个字段 |
| **schema 库** | 用 Zod / Valibot 等声明 schema，自动得到类型 | 结构复杂、需要详细错误信息 🔥 |
| **从类型生成校验** | 用装饰器/元数据自动生成（如 `class-validator`） | 已有 DTO 类的中大型项目 |

**决策表**：

| 场景 | 推荐 |
| --- | --- |
| 1~2 个简单结构 | 手写守卫（零依赖）🔥 |
| 多个嵌套结构、需要错误信息 | schema 库 🔥 |
| 需要类型 ⇄ schema 双向一致 | schema 库 🔥 |
| 已经有大量 DTO 类 | `class-validator` + `class-transformer` |
| 只在构建期校验 | 不需要——那是编译器的活 |
| 前后端共享类型 | schema 库（前后端共用同一份 schema） |

{{% /tab %}}

{{< /tabpane >}}

---

## 手写类型守卫

零依赖方案，适合结构简单的场景。

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  tags?: string[];
}

function isUser(v: unknown): v is User {
  if (typeof v !== "object" || v === null) return false;
  const o = v as Record<string, unknown>;

  return (
    typeof o.id === "number" &&
    typeof o.name === "string" &&
    typeof o.email === "string" &&
    (o.tags === undefined ||
      (Array.isArray(o.tags) && o.tags.every((t) => typeof t === "string")))
  );
}
```

**手写守卫的检查清单**（漏一条就是 bug）：

| 检查 | 为什么必须 |
| --- | --- |
| `typeof v !== "object"` | 排除原始类型 |
| `v === null` | ⚠️ `typeof null === "object"`，必须单独判 |
| 每个必需字段 | 缺一个就漏了 |
| 可选字段的 `undefined` 分支 | 可选 ≠ 不存在 |
| 数组用 `Array.isArray` | `typeof []` 是 `"object"` |
| 嵌套对象递归调用 | 否则内层完全没校验 |
| 数字用 `Number.isFinite` | 排除 `NaN` / `Infinity` |

```typescript
// 可组合的小工具，减少重复
const isString = (v: unknown): v is string => typeof v === "string";
const isNumber = (v: unknown): v is number =>
  typeof v === "number" && Number.isFinite(v);
const isArrayOf = <T>(v: unknown, item: (x: unknown) => x is T): v is T[] =>
  Array.isArray(v) && v.every(item);

function isUser2(v: unknown): v is User {
  if (typeof v !== "object" || v === null) return false;
  const o = v as Record<string, unknown>;
  return (
    isNumber(o.id) &&
    isString(o.name) &&
    isString(o.email) &&
    (o.tags === undefined || isArrayOf(o.tags, isString))
  );
}
```

> ⚠️ **手写守卫的最大问题**：**编译器不检查守卫写得对不对**。守卫里少判一个字段，类型系统完全不知道，照样收窄成 `User`。结构一复杂，漏判几乎必然发生。
>
> 所以：**结构超过 5 个字段、或字段可能演进时，用 schema 库**。

---

## schema 库

{{< tabpane text=true persist=disabled >}}

{{% tab header="Zod 4" %}}

当前版本 **4.6.5**。核心优势：生态最广、类型推断最成熟。

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1),
  email: z.email(),                                  // ✅ v4 内置
  role: z.enum(["admin", "user"]).default("user"),
  tags: z.array(z.string()).optional(),
});

// 从 schema 推导类型 🔥
type User = z.infer<typeof UserSchema>;
// {
//   id: number;
//   name: string;
//   email: string;
//   role: "admin" | "user";
//   tags?: string[] | undefined;
// }
```

**解析的三种方式**：

| 方法 | 失败时 | 用途 |
| --- | --- | --- |
| `.parse(data)` | **抛异常** | 失败即中断 |
| `.safeParse(data)` | 返回结果对象 | 需要自己处理错误 🔥 |
| `.parseAsync(data)` | 抛异常（支持异步校验） | 含异步 refine |

```typescript
const raw: unknown = JSON.parse(responseText);

// ✅ 推荐：safeParse，不靠异常控制流
const result = UserSchema.safeParse(raw);
if (result.success) {
  const user: User = result.data;    // ✅ 收窄为 User
  console.log(user.name);
} else {
  // result.error.issues 是结构化错误列表
  for (const issue of result.error.issues) {
    console.error(`${issue.path.join(".")}: ${issue.message}`);
  }
}
```

**常用 schema 构造**：

| 需求 | 写法 |
| --- | --- |
| 字符串转数字 | `z.coerce.number()` |
| 判别联合 | `z.discriminatedUnion("kind", [...])` |
| 递归结构 | `z.lazy(() => Schema)` |
| 自定义校验 | `.refine(fn, msg)` / `.superRefine()` |
| 转换数据 | `.transform(fn)` |
| 部分可选 | `UserSchema.partial()` |
| 挑选字段 | `UserSchema.pick({ id: true })` |
| 排除字段 | `UserSchema.omit({ email: true })` |
| 合并 | `A.merge(B)` / `A.extend({...})` |
| ISO 日期字符串 | `z.iso.datetime()` |
| 不可信 URL | `z.url()` |

```typescript
// 判别联合（对应 TS 的可辨识联合）
const ShapeSchema = z.discriminatedUnion("kind", [
  z.object({ kind: z.literal("circle"), r: z.number() }),
  z.object({ kind: z.literal("square"), s: z.number() }),
]);
type Shape = z.infer<typeof ShapeSchema>;
// { kind: "circle"; r: number } | { kind: "square"; s: number }  ✅

// coerce：把 "42" 变成 42（处理 query/环境变量）
const Port = z.coerce.number().int().min(1).max(65535);
const port: number = Port.parse("8080");    // ✅ 42 号字符串也可以

// transform：校验后转换
const DateFromString = z.iso.datetime().transform((s) => new Date(s));
type D = z.infer<typeof DateFromString>;    // Date ✅
```

> 💡 **`z.coerce` 非常重要**：环境变量和 URL 参数**永远是字符串**，`z.coerce.number()` / `z.coerce.boolean()` 能省掉手写转换。

{{% /tab %}}

{{% tab header="Valibot 1.x" %}}

当前版本 **1.5.0**。核心优势：**体积极小**（可 tree-shake 到几百字节），API 是函数式管道。

```typescript
import * as v from "valibot";

const UserSchema = v.object({
  id: v.number(),
  name: v.pipe(v.string(), v.minLength(1)),
  email: v.pipe(v.string(), v.email()),
});
```

**与 Zod 的关键差异**：

| | Zod 4 | Valibot 1.x |
| --- | --- | --- |
| API 风格 | 方法链 `z.string().min(1)` | 管道 `v.pipe(v.string(), v.minLength(1))` |
| 体积 | 较大（全量引入） | **极小，可 tree-shake** 🔥 |
| 类型推断 | `z.infer<typeof S>` | `v.InferOutput<typeof S>` |
| 输入类型 | — | `v.InferInput<typeof S>` 🔥 |
| 解析 | `.parse` / `.safeParse` | `v.parse(S, d)` / `v.safeParse(S, d)` |
| 生态 | 最广 | 较小但增长快 |
| 错误信息 | `issue.path` 是数组 | 同样结构化 |

**Valibot 的输入/输出类型区分**（这是它的独特能力）：

```typescript
import * as v from "valibot";

// transform 会改变输出类型
const Schema = v.pipe(
  v.string(),
  v.transform((s) => s.length),
);

type In = v.InferInput<typeof Schema>;    // string  ← 接口收到的
type Out = v.InferOutput<typeof Schema>;  // number  ← 转换后的
```

| 类型 | 含义 |
| --- | --- |
| `v.InferInput<S>` | 校验**前**的类型（外部数据的形状） |
| `v.InferOutput<S>` | 校验**后**的类型（业务代码用的） |

> 🔥 这个区分在**前后端共享 schema** 时特别有价值：前端表单送出 `In`，后端处理后得到 `Out`，两者类型都精确。

```typescript
const result = v.safeParse(UserSchema, raw);
if (result.success) {
  const user: v.InferOutput<typeof UserSchema> = result.output;
  console.log(user.name);
} else {
  console.log(result.issues);
}
```

{{% /tab %}}

{{% tab header="其它方案对照" %}}

| 库 | 当前版本 | 特点 | 适合 |
| --- | --- | --- | --- |
| **Zod** | 4.6.5 | 生态最广，推断成熟 | 大多数项目 🔥 |
| **Valibot** | 1.5.0 | 体积极小，tree-shake 友好 | 前端包体积敏感 |
| **ArkType** | 2.2.3 | 语法接近 TS 类型定义，性能好 | 喜欢「写类型就是写 schema」 |
| **TypeBox** | 0.34.52 | 产出标准 JSON Schema | 需要 JSON Schema 互操作 |
| **AJV** | 8.20.0 | JSON Schema 校验（运行时） | 已有 JSON Schema 体系 |
| **class-validator** | — | 装饰器 + DTO 类 | NestJS 等既有 DTO 的项目 |
| **手写守卫** | — | 零依赖 | 结构简单 |

**ArkType 的写法**（语法几乎就是 TS 类型）：

```typescript
import { type } from "arktype";

const User = type({
  id: "number",
  name: "string",
  "role?": "'admin' | 'user'",
});

type U = typeof User.infer;    // 直接得到类型
const out = User(raw);          // 校验（返回错误或数据）
```

**从类型生成校验**（反方向）：

某些工具能从 TS 类型**生成 JSON Schema**，再用 AJV 校验：

```typescript
import type { Static, TSchema } from "@sinclair/typebox";
import { Type } from "@sinclair/typebox";
import Ajv from "ajv";

const UserSchema = Type.Object({
  id: Type.Number(),
  name: Type.String(),
});
type User = Static<typeof UserSchema>;   // ✅ 类型从 schema 来

const ajv = new Ajv();
const validate = ajv.compile(UserSchema);
if (validate(raw)) { /* raw 现在是 User */ }
```

| 方向 | 工具 | 优点 | 缺点 |
| --- | --- | --- | --- |
| schema → 类型 | Zod / Valibot / TypeBox | 单一事实来源 🔥 | 需要学库的 DSL |
| 类型 → schema | `ts-json-schema-generator` 等 | 不写两遍 | 构建步骤复杂，有表达能力损失 |

> 💭 **推荐方向是「schema → 类型」**。因为校验逻辑必须在运行时真实存在，让它成为唯一事实来源最不容易出现「类型和校验不一致」。反过来（类型 → schema）容易在类型用了高级特性时生成失败。

{{% /tab %}}

{{< /tabpane >}}

---

## 各类边界的实战写法

{{< tabpane text=true persist=disabled >}}

{{% tab header="HTTP 响应" %}}

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.email(),
});
const UsersSchema = z.array(UserSchema);

type User = z.infer<typeof UserSchema>;

// ✅ 把校验封在数据访问层，业务代码拿到的一定是可信类型
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const raw: unknown = await res.json();
  const parsed = UserSchema.safeParse(raw);

  if (!parsed.success) {
    // 带上上下文，便于定位是接口变了还是代码错了
    throw new Error(`响应格式不符合预期: ${parsed.error.message}`, {
      cause: parsed.error,
    });
  }
  return parsed.data;
}

// 列表
async function fetchUsers(): Promise<User[]> {
  const raw: unknown = await (await fetch("/api/users")).json();
  return UsersSchema.parse(raw);     // 抛异常版本，适合确定格式时
}
```

**统一封装的请求函数**：

```typescript
async function request<T extends z.ZodType>(
  url: string,
  schema: T,
  init?: RequestInit,
): Promise<z.infer<T>> {
  const res = await fetch(url, init);
  if (!res.ok) throw new HttpError(res.status, url);

  const raw: unknown = await res.json();
  const parsed = schema.safeParse(raw);
  if (!parsed.success) {
    throw new ValidationError(`响应校验失败: ${url}`, parsed.error);
  }
  return parsed.data;
}

// 使用：类型自动推导 ✅
const user = await request("/api/users/1", UserSchema);   // User
const users = await request("/api/users", z.array(UserSchema));  // User[]
```

> 🔥 **这个模式的价值**：`request` 是**唯一**接触 `any` 的地方，业务代码里再也不会出现未校验的数据。

{{% /tab %}}

{{% tab header="环境变量" %}}

环境变量**永远是字符串或 undefined**，且经常缺失。

```typescript
import { z } from "zod";

const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  DATABASE_URL: z.url(),
  API_KEY: z.string().min(1),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  FEATURE_X: z.coerce.boolean().default(false),
});

// ✅ 在进程启动时校验一次，失败立刻退出
function loadEnv() {
  const parsed = EnvSchema.safeParse(process.env);
  if (!parsed.success) {
    console.error("环境变量配置错误：");
    for (const issue of parsed.error.issues) {
      console.error(`  ${issue.path.join(".")}: ${issue.message}`);
    }
    process.exit(1);      // 🔥 启动即失败，好过运行时才炸
  }
  return parsed.data;
}

export const env = loadEnv();
// env.PORT 是 number ✅，env.NODE_ENV 是联合类型 ✅
```

| 要点 | 说明 |
| --- | --- |
| **启动时校验** | 早失败，不要等到用的时候才发现 🔥 |
| `z.coerce.number()` | 环境变量是字符串，必须转换 |
| `.default(...)` | 让可选配置有合理默认值 |
| 用 `z.enum` 而不是 `z.string` | 拼错立刻发现 |
| 不在代码里散落 `process.env.X` | 统一从 `env` 对象取 |

> ⚠️ **不要给 `process.env` 加类型声明就以为安全了**：
>
> ```typescript
> declare global {
>   namespace NodeJS {
>     interface ProcessEnv { PORT: string }   // ⚠️ 只是类型，运行时可能是 undefined
>   }
> }
> ```
>
> 这只是让编译器闭嘴，**没有任何校验**。变量不存在时类型说有，运行时是 `undefined`。

{{% /tab %}}

{{% tab header="localStorage 与持久化" %}}

持久化数据的特殊风险：**旧版本写入的数据还在**。

```typescript
import { z } from "zod";

const SettingsSchema = z.object({
  theme: z.enum(["light", "dark"]).default("light"),
  fontSize: z.number().min(8).max(72).default(14),
});
type Settings = z.infer<typeof SettingsSchema>;

const KEY = "app-settings";

function loadSettings(): Settings {
  const raw = localStorage.getItem(KEY);
  if (raw === null) return SettingsSchema.parse({});   // 用默认值

  try {
    const parsed = SettingsSchema.safeParse(JSON.parse(raw));
    if (parsed.success) return parsed.data;

    // ⚠️ 数据不符合当前 schema（很可能是旧版本写的）
    console.warn("设置格式已变化，使用默认值", parsed.error.issues);
    return SettingsSchema.parse({});
  } catch {
    // JSON 本身就坏了
    console.warn("设置数据损坏，使用默认值");
    return SettingsSchema.parse({});
  }
}

function saveSettings(s: Settings): void {
  localStorage.setItem(KEY, JSON.stringify(s));
}
```

| 风险 | 应对 |
| --- | --- |
| 旧版本数据格式不同 | schema 里给默认值 + 校验失败时回退 🔥 |
| 用户手动改过 | 校验拦住 |
| JSON 损坏 | `try/catch` 包住 `JSON.parse` |
| 数据被清空 | 处理 `null` 分支 |
| 需要迁移 | 加 `version` 字段，按版本走迁移函数 |

**带版本迁移的持久化**：

```typescript
const V2Schema = z.object({
  version: z.literal(2),
  settings: SettingsSchema,
});

type Stored = z.infer<typeof V2Schema>;

function load(): Settings {
  const raw = localStorage.getItem(KEY);
  if (!raw) return SettingsSchema.parse({});

  let data: unknown;
  try { data = JSON.parse(raw); } catch { return SettingsSchema.parse({}); }

  // 按 version 分派
  const v2 = V2Schema.safeParse(data);
  if (v2.success) return v2.data.settings;

  // 旧版本迁移
  const legacy = LegacySchema.safeParse(data);
  if (legacy.success) return migrateV1toV2(legacy.data);

  return SettingsSchema.parse({});
}
```

{{% /tab %}}

{{% tab header="表单与用户输入" %}}

```typescript
import { z } from "zod";

const SignupSchema = z.object({
  email: z.email("请输入有效邮箱"),
  password: z.string().min(8, "密码至少 8 位"),
  confirm: z.string(),
  age: z.coerce.number().int().min(18, "需年满 18 岁"),
}).refine((d) => d.password === d.confirm, {
  message: "两次密码不一致",
  path: ["confirm"],            // ✅ 把错误挂到具体字段
});

type Signup = z.infer<typeof SignupSchema>;

function handleSubmit(formData: FormData) {
  // FormData 的值都是 string | File | null，先转成普通对象
  const raw = Object.fromEntries(formData.entries());
  const parsed = SignupSchema.safeParse(raw);

  if (!parsed.success) {
    // 按字段聚合错误，方便渲染到表单项上
    const fieldErrors = z.flattenError(parsed.error);
    return { ok: false as const, errors: fieldErrors.fieldErrors };
  }
  return { ok: true as const, data: parsed.data };
}
```

| 要点 | 说明 |
| --- | --- |
| `Object.fromEntries(formData)` | `FormData` → 普通对象 |
| `z.coerce.number()` | 表单值永远是字符串 |
| `.refine(fn, { path })` | 跨字段校验并定位错误 |
| 聚合错误 | `z.flattenError()` 得到按字段分组的错误 |
| 错误挂在具体 `path` | 前端才能定位到输入框 |

> 💡 **前后端共享 schema**：把 schema 放在共享包里，前端做即时校验、后端做权威校验，**同一份定义**。这能消除「前端说合法、后端说非法」的整类问题。

{{% /tab %}}

{{< /tabpane >}}

---

## 输出侧也要校验

不只输入要校验，**输出**同样值得。

```typescript
// ✅ 用 satisfies 保证你返回的东西符合契约
const response = {
  id: user.id,
  name: user.name,
  // 漏了 email
} satisfies UserResponse;
// ❌ TS2741: Property 'email' is missing in type ... but required in type 'UserResponse'
```

| 手段 | 检查 | 运行时 |
| --- | --- | --- |
| `satisfies T` | ✅ 编译期 | ❌ |
| schema 的 `.parse()` | ✅ 编译期 | ✅ 运行时 🔥 |
| 返回类型标注 | ✅（但会拓宽） | ❌ |

**Schema 天然是双向契约**：

```typescript
// 一个 schema 同时用于校验输入和输出
const UserResponseSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.email(),
});

// 输出侧：确保我们没有返回不该返回的字段（如 passwordHash）
function toResponse(u: UserEntity) {
  return UserResponseSchema.parse({
    id: u.id,
    name: u.name,
    email: u.email,
    // passwordHash 忘了删？schema 会告诉你多了字段
  });
}
```

> 🔥 **`parse()` 对多余字段的默认行为**取决于库设置。Zod 默认**剥离**多余字段（strip），这正好能防止**意外泄露内部字段**——一个很实际的安全收益。

| 多余字段策略 | Zod 写法 | 效果 |
| --- | --- | --- |
| 剥离（默认） | `z.object({...})` | 多余字段被删除 🔥 防泄露 |
| 严格拒绝 | `z.strictObject({...})` | 有多余字段就报错 |
| 保留 | `z.looseObject({...})` | 原样保留 |

---

## 让「类型撒谎」无所遁形

### 验证库类型声明是否与现实一致

第三方库的 `.d.ts` 可能写错。校验一次能发现：

```typescript
// 拿真实返回值对照声明的类型
const raw: unknown = lib.getData();
const parsed = ExpectedSchema.safeParse(raw);
if (!parsed.success) {
  // 库的类型声明与真实行为不符！
  console.error("库返回的数据与类型声明不一致", parsed.error.issues);
}
```

### 用 `satisfies` 做编译期契约检查

```typescript
type ApiResponse = {
  users: { id: number; name: string }[];
  total: number;
};

// 编译期就能发现结构不符
const mock = {
  users: [{ id: 1, name: "a" }],
  total: 1,
} satisfies ApiResponse;
```

### 边界函数只做一件事

```typescript
// 🛑 混杂：校验、转换、业务逻辑在一处
async function processUser(id: string) {
  const res = await fetch(`/api/users/${id}`);
  const raw = await res.json() as User;       // ⚠️ 未校验
  const name = raw.name.toUpperCase();        // 可能炸
  await save({ name, id: raw.id });           // 可能存进脏数据
}

// ✅ 分层：校验在边界，业务逻辑只处理可信数据
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  const raw: unknown = await res.json();
  return UserSchema.parse(raw);               // 校验只在这一处
}

async function processUser(id: string) {
  const user = await fetchUser(id);           // ✅ 到这里一定是 User
  await save({ name: user.name.toUpperCase(), id: user.id });
}
```

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| `const u: User = await res.json()` | 无任何检查 | schema 校验 🔥 |
| 只加 `process.env` 类型声明 | 运行时仍是 undefined | 启动时用 schema 校验 |
| 守卫漏判 `null` | 运行时崩溃 | `typeof v === "object" && v !== null` |
| 手写守卫漏字段 | 编译器不报错 | 结构复杂就用 schema 库 |
| 忘了数组元素校验 | 内层没查 | `z.array(ItemSchema)` |
| 环境变量忘了 `coerce` | 类型是 string 不是 number | `z.coerce.number()` |
| 持久化数据没版本管理 | 升级后崩 | 加 `version` + 迁移 |
| 只在输入侧校验 | 输出泄露内部字段 | 输出也用 schema |
| 校验失败只抛「格式错误」 | 无法定位 | 带上 `error.issues` |
| 校验散落各处 | 难维护、易漏 | 统一封装在数据访问层 |
| 以为类型注解=运行时保证 | 生产事故 | 记住：类型在运行时不存在 |
