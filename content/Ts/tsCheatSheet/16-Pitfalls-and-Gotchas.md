+++
title = "16 血泪速查"
weight = 116
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "按症状索引的踩坑表：你这么写 / 实际发生什么 / 正确写法"
isCJKLanguage = true
draft = false
+++

# 16 血泪速查

这一页**按症状索引**，不是按语法索引。出问题时从「我看到的现象」出发查，比从「这是哪个语法」出发快得多。

> 本页所有「实际发生什么」都在 TS 6.0.3 实测过。

---

## 类型没报错，但运行时炸了

**这一类是最危险的**——编译器全程绿灯，生产环境报错。

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `const u: User = await res.json()` | `any` 静默赋给 `User`，**零校验** | schema 校验（见 [11]({{< relref "11-Runtime-Validation-and-Boundaries.md" >}})）🔥 |
| `const d = JSON.parse(s)` | 返回 `any`，之后全无检查 | `schema.parse(JSON.parse(s))` |
| `const x: User = raw as User` | 断言不检查，运行时可能缺字段 | 类型守卫 / schema |
| `localStorage.getItem(k)` | 返回 `string \| null`，`JSON.parse` 后是 `any` | 校验后再用 |
| `process.env.PORT` 声明成 `string` | 运行时可能是 `undefined` | 启动时 schema 校验 |
| `el!.focus()` | `!` 只去掉类型，不保证非空 | 判空或可选链 |
| `arr[0]` 当 `T` 用 | 越界/空数组时是 `undefined` | 开 `noUncheckedIndexedAccess` |
| `Object.keys(obj)` 当 `(keyof T)[]` | 实际是 `string[]` | 手写 `as (keyof T)[]` 或改数据结构 |

```typescript
// 🛑 三行全绿，运行时炸
async function loadUser(id: string) {
  const res = await fetch(`/api/users/${id}`);
  const user: User = await res.json();       // ✅ 编译通过
  return user.name.toUpperCase();            // 💥 若响应是 { username: ... }
}
```

```typescript
// ✅ 守住边界
import { z } from "zod";

const UserSchema = z.object({ id: z.number(), name: z.string() });
type User = z.infer<typeof UserSchema>;

async function loadUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  const raw: unknown = await res.json();
  return UserSchema.parse(raw);              // ✅ 真检查
}
```

> 🔥 **记住这一条**：**类型注解不是运行时保证**。凡是从边界进来的数据，编译器的绿灯毫无意义。

---

## `null` / `undefined` 相关

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `if (n)` 判断 `number \| null` | **`0` 也被排除**，走了错误分支 | `if (n !== null)` |
| `if (s)` 判断 `string \| undefined` | **空字符串也被排除** | `if (s !== undefined)` |
| `a \|\| b` 提供默认值 | `0` / `""` / `false` 被替换掉 | 用 `a ?? b` 🔥 |
| `obj.prop.toUpperCase()` | `TS18048` / `TS18047` | `obj.prop?.toUpperCase()` |
| 收窄后在回调里用 | 收窄失效，`TS18047` | 先存 `const` |
| 收窄后重新赋值 | 收窄作废 | 别在收窄后改该变量 |
| `ref.current.focus()` | `useRef` 初始为 `null` | `ref.current?.focus()` |
| 可选属性当必填用 | 可能是 `undefined` | 判空或改类型 |

```typescript
// 🛑 真值判断吞掉合法值
function retry(times: number | null) {
  if (times) return times * 2;    // times = 0 时走 else！
  return 0;
}

// ✅ 显式判断
function retry2(times: number | null) {
  return times !== null ? times * 2 : 0;
}
```

```typescript
// 🛑 回调里收窄失效
function bad(v: string | null) {
  if (v !== null) {
    setTimeout(() => v.toUpperCase(), 0);
    //                ~ TS18047: 'v' is possibly 'null'.
  }
}

// ✅ 先存 const
function good(v: string | null) {
  if (v !== null) {
    const s = v;
    setTimeout(() => s.toUpperCase(), 0);   // ✅
  }
}
```

| 运算符 | 只对 `null`/`undefined` 生效 |
| --- | --- |
| `??` | ✅ 保留 `0`、`""`、`false` 🔥 |
| `\|\|` | ❌ 会替换掉它们 |
| `?.` | ✅ 只在 `null`/`undefined` 时短路 |

---

## 类型不符合直觉

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `const x: {} = "a"` | **合法**！`{}` 不是「空对象」 | 用 `object` 或具体形状 |
| `const x: object = "a"` | `TS2322`，原始类型不符合 `object` | 明确要用哪个 |
| `typeof v === "object"` 判非空对象 | **`null` 也满足** | 加 `&& v !== null` 🔥 |
| `typeof arr === "array"` | 永远 `false` | `Array.isArray(arr)` |
| `x instanceof SomeInterface` | 编译失败（接口运行时不存在） | 自定义守卫 |
| `readonly obj.prop.deep` 改内层 | **合法**！`readonly` 是浅层的 | `DeepReadonly`（见 [06]({{< relref "06-Type-Level-Programming-Recipes.md" >}})） |
| `keyof Dict`（含索引签名） | 结果是 `string \| number` ⚠️ | `string & keyof Dict` |
| `Omit<T, "typo">` | **不报错**，静默不排除 | `StrictOmit` |
| 交叉同名属性 | 属性类型变 `never` | 避免同名，或显式 `Omit` |
| `readonly T[]` 赋给 `T[]` | `TS4104` | `[...ro]` 复制 |
| 用 `String` / `Number` | 包装对象类型，几乎总是写错 | 小写 `string` / `number` |

```typescript
// 🛑 三个都合法，但含义差很远
const a: {} = "字符串可以";        // ✅ 合法
const b: object = "字符串不行";    // ❌ TS2322
const c: object = () => {};        // ✅ 函数也是 object
```

```typescript
// 🛑 typeof null 是 "object"（JS 历史 bug）
function f(v: string | null) {
  if (typeof v === "object") {
    return "null 也会进来！";
  }
  return v;
}

// ✅ 正确判非空对象
if (typeof v === "object" && v !== null) { /* ... */ }
```

---

## 泛型与推断

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| 期望从返回值推断 `T` | `T` 变成 `unknown` | 显式 `f<string>()` |
| `first([])` | `T` 推断为 `never` | `first<string>([])` |
| 条件类型用在联合上 | **分配律**导致结果变联合 | `[T] extends [U] ? ...` 🔥 |
| `IsNever<T>` 判 `never` | 结果是 `never` 不是 `true` | `[T] extends [never]` |
| 映射类型丢修饰符 | `?` / `readonly` 消失 | 用同态形式 `[K in keyof T]` |
| `Capitalize<K>` 报错 | `K` 可能是 `number`/`symbol` | `Capitalize<string & K>` |
| 递归类型太深 | `TS2589` | 加深度计数器 |
| 默认值参数参与推断 | 联合被意外扩大 | `NoInfer<T>` 🆕 |
| `as const` 忘了写 | 推断成 `string` 而非字面量 | 常量表加 `as const` |
| 重载顺序反了 | 推断成宽类型 | 窄签名写前面 |
| `<T>` 在 `.tsx` 里 | `TS17008` | `<T,>` 或 `<T extends unknown>` |

```typescript
// 🛑 分配律：期望整体判断，结果逐成员判断
type IsString<T> = T extends string ? true : false;
type A = IsString<string | number>;   // boolean（不是 false！）

// ✅ 用元组阻止分配
type IsString2<T> = [T] extends [string] ? true : false;
type B = IsString2<string | number>;  // false
```

---

## 模块与导入

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `nodenext` 下 `import "./x"` | `TS2835` 缺扩展名 | 写 `"./x.js"`（不是 `.ts`）🔥 |
| 类型没写 `import type` | `TS1484` | `import type { X }` |
| `export { SomeType }` | `TS1205` | `export type { SomeType }` |
| `.d.ts` 无顶层 import/export | **成为脚本，污染全局** ⚠️ | 加 `export {}` |
| 在模块文件里写 `declare module "*.css"` | `TS2664` | 放到无 import 的脚本文件 🔥 |
| 以为 `paths` 影响运行时 | 打包器/Node 找不到模块 | 同步配 `resolve.alias` 或 `imports` |
| 6.0 下找不到 `process` | `types` 默认 `[]` | `types: ["node"]` |
| 用 `baseUrl` | `TS5101` 废弃 | 前缀写进 `paths` |
| 用 `moduleResolution: "node"` | `TS5107` 废弃 | `"bundler"` 或 `"nodenext"` |

```typescript
// 🛑 这个文件没有 import/export，是「脚本」
interface Config { url: string }
// ↑ 这是全局声明！会污染整个项目，且可能与其他文件冲突
```

```typescript
// ✅ 加一行让它成为模块
export {};                        // 或 import type {} from "x"

interface Config { url: string }  // 现在只在本文件内可见
```

---

## 类与对象

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `private` 当安全边界 | **运行时仍可访问** | 用 `#field` 🔥 |
| 类属性没初始化 | `TS2564` | 给初值 / 构造函数赋值 / `?` |
| 滥用 `!` 明确赋值断言 | 运行时是 `undefined` | 老实初始化 |
| `{ a: 1, b: 2 }` 赋给单属性类型 | `TS2353` 多余属性检查 | 经变量中转，或改类型 |
| 在 `function` 回调里用 `this` | `TS2683`，`this` 丢失 | 用箭头函数 |
| 忘了 `override` | 基类改名后静默失联 | 开 `noImplicitOverride` |
| 构造函数参数属性 | 生成运行时代码，Node 直跑报错 | 手写字段赋值（`erasableSyntaxOnly` 下必需） |
| 索引签名加已知属性 | `TS2411` 类型不兼容 | 统一类型 |

```typescript
// 🛑 private 只是编译期
class Secret {
  private key = "abc";
}
const s = new Secret();
(s as any).key;              // ✅ 运行时拿得到
s["key"];                    // ✅ 也拿得到

// ✅ # 是运行时真私有
class Secret2 {
  #key = "abc";
  getKey() { return this.#key; }
}
const s2 = new Secret2();
(s2 as any).#key;            // ❌ 语法错误
Object.keys(s2);             // [] —— 完全看不到
```

---

## 枚举与常量

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `enum` 做状态码 | 生成运行时代码，Node 直跑报错 | `as const` 对象 + 联合类型 🔥 |
| `const enum` 跨包使用 | 值被内联，`isolatedModules` 环境下可能取不到 | 用 `as const` 对象 |
| `enum` 当类型又当值 | 两个空间都有，容易混淆 | 明确分开类型与常量 |
| 手写联合类型 | 容易漏、容易过时 | `(typeof ARR)[number]` |

```typescript
// 🛑 enum：生成运行时代码，且不能通过 erasableSyntaxOnly
export enum Status { Idle = "idle", Done = "done" }

// ✅ 推荐：as const 对象
export const Status = {
  Idle: "idle",
  Done: "done",
} as const;
export type Status = (typeof Status)[keyof typeof Status];   // "idle" | "done" 🔥
```

| 方案 | 运行时代码 | Node 直跑 | 类型安全 |
| --- | --- | --- | --- |
| `enum` | ✅ 有 | ❌ | ✅ |
| `const enum` | ❌ 内联 | ⚠️ 视环境 | ✅ |
| `as const` 对象 | ✅ 有（普通对象） | ✅ | ✅ 🔥 |
| 字符串字面量联合 | ❌ 无 | ✅ | ✅ |

---

## 数组与集合

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `string[]` 赋给 `(string \| number)[]` | **合法但不健全**，写入后类型污染 | 参数用 `readonly T[]` |
| `readonly` 数组上 `.sort()` / `.reverse()` | `TS2339` | `[...arr].sort()` |
| `.sort()` 以为返回新数组 | **就地修改原数组** | 先复制 |
| `.filter()` 期望自动收窄 | 类型没变窄 | 手写 `(x): x is T =>` |
| `arr[0]` 当 `T` | 可能 `undefined` | 开 `noUncheckedIndexedAccess` |
| `.find()` 结果直接用 | 可能是 `undefined` | 判空 |

```typescript
// 🛑 数组协变的不健全漏洞
let strs: string[] = ["a"];
let anys: (string | number)[] = strs;   // ✅ 编译通过
anys.push(123);                          // ✅ 也通过
strs[1].toUpperCase();                   // 💥 运行时崩溃
```

```typescript
// ✅ 防御：函数参数用 readonly
function sum(xs: readonly number[]): number { /* ... */ }

// ✅ 或复制后再操作
const sorted = [...items].sort((a, b) => a - b);
```

---

## `any` 与抑制指令

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| `as any` 让编译通过 | `any` 会**传染**下游 | 用 `unknown` + 收窄 |
| `@ts-ignore` | 错了也不提示，永久留存 | `@ts-expect-error` 🔥 |
| `@ts-expect-error` 没用了 | `TS2578` 报错（**这是好事**） | 删掉它 |
| `@ts-nocheck` 整个文件 | 新代码也失去保护 | 登记 + 期限 |
| 无类型的 `declare module "x"` | 等于没有类型 | 最小声明，参数用 `unknown` |
| `catch (e)` 当 `Error` 用 | `TS18046` | `instanceof Error` 收窄 |

```typescript
// 🛑 any 传染
declare const data: any;
const a = data.foo;         // any
const b = a.bar;            // any
function f(x: any) { return x.baz; }
const c = f(1);             // any —— 三跳之后依然是 any
```

```typescript
// ✅ @ts-expect-error 会自我清理
// @ts-expect-error 上游库缺少该重载，见 issue #123
legacyCall(x);
// 上游修好后 → error TS2578: Unused '@ts-expect-error' directive.
// → CI 失败 → 你删掉它 ✅
```

---

## 异步

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| 忘了 `await` | Promise 浮空，错误丢失 | `@typescript-eslint/no-floating-promises` |
| 忘了 `Awaited` | 拿到 `Promise<T>` 而不是 `T` | `Awaited<ReturnType<typeof fn>>` |
| `setTimeout` 标 `number` | Node 下是 `NodeJS.Timeout` | `ReturnType<typeof setTimeout>` |
| 以为 `allSettled` 的 `reason` 是 `Error` | 实际是 `any` ⚠️ | 自己收窄 |
| `JSON.stringify(err)` | 得到 `{}`（属性不可枚举） | 手动提取 `message` / `stack` |
| `async` 函数标 `: number` | `TS1064` | 标 `: Promise<number>` |

```typescript
// 🛑 Error 序列化成空对象
JSON.stringify(new Error("出错了"));   // "{}"

// ✅ 手动序列化
const serialized = {
  name: err.name,
  message: err.message,
  stack: err.stack,
};
```

---

## tsconfig 与工程

| 你这么写 | 实际发生什么 | 正确写法 |
| --- | --- | --- |
| 6.0 下不写 `types` | `@types/node` 不加载 | `types: ["node"]` |
| 期望 `rootDir` 自动推断 | 产物多一层 `src/` | 显式 `rootDir` |
| `extends` 后期望 `lib` 合并 | 数组选项是**覆盖** | 子配置写完整 |
| 开了 `noUncheckedIndexedAccess` 但关了 `strictNullChecks` | **静默失效** | 必须开 `strictNullChecks` |
| 以为 `strict` 含所有检查 | 索引访问、exact optional 都不在内 | 单独开启 |
| 以为 `skipLibCheck` 万能 | 你自己的 `.d.ts` 也不检查了 | 手写声明要额外仔细 |
| 命令行传文件 + 有 tsconfig | `TS5112` | 加 `--ignoreConfig` |
| 以为打包器会检查类型 | 类型错误进主干 | CI 加 `tsc --noEmit` 🔥 |
| `dist` 里有测试文件 | 测试被编译进产物 | `exclude` 测试 |

```jsonc
// 🛑 数组选项不会合并
// tsconfig.base.json
{ "compilerOptions": { "lib": ["ES2023", "DOM", "DOM.Iterable"] } }

// tsconfig.json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": { "lib": ["ES2023"] }   // ⚠️ DOM 全丢了！
}
```

```jsonc
// ✅ 写完整
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": { "lib": ["ES2023", "DOM", "DOM.Iterable"] }
}
```

---

## 快速自查清单

把这份清单贴进 code review checklist：

| 检查项 | 为什么 |
| --- | --- |
| 所有外部数据都经过校验了吗？ | 类型在运行时不存在 🔥 |
| 有没有 `as any` / `@ts-ignore`？ | 新增的技术债 |
| 索引访问判空了没？ | `noUncheckedIndexedAccess` |
| 可选链 `?.` 和 `??` 用对了吗？ | 别用 `\|\|` 做默认值 |
| 新代码有没有加 `as const`？ | 常量表才能推出字面量联合 |
| 公开 API 用 `interface` 还是 `type`？ | 影响使用者能否扩充 |
| 有没有在收窄后重新赋值？ | 收窄会失效 |
| `readonly` 是浅的，深层改了吗？ | 可能需要 `DeepReadonly` |
| 异步函数漏 `await` 了吗？ | 用 lint 规则兜住 |
| CI 里有 `tsc --noEmit` 吗？ | 打包器不检查类型 🔥 |
