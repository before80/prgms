+++
title = "06 类型层编程配方"
weight = 106
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "可直接抄用的自定义工具类型配方、递归技巧与类型体操的代价边界"
isCJKLanguage = true
draft = false
+++

# 06 类型层编程配方

[02]({{< relref "02-Type-System-Core.md" >}}) 讲的是**内置**工具类型，本页是**自己写**的常用配方——可以直接抄进项目。

> 本页所有配方均在 TS 6.0.3 实测编译通过，关键推断结果用 `Eq<A, B>` 断言验证。

---

## 一眼看懂写法

| 配方 | 类型 | 用在哪 |
| --- | --- | --- |
| `Mutable<T>` | 去只读 | 处理第三方 `readonly` 数据 |
| `DeepPartial<T>` | 深层可选 | 递归配置合并 |
| `DeepReadonly<T>` | 深层只读 | 冻结配置 |
| `StrictOmit<T, K>` | 会报错的 Omit | 重构时防拼写错误 🔥 |
| `KeysOfType<T, V>` | 按值类型取键 | 找出所有 `string` 属性 |
| `RequireAtLeastOne<T>` | 至少一个 | 查询条件参数 |
| `RequireExactlyOne<T>` | 恰好一个 | 互斥选项 |
| `Prettify<T>` | 展平交叉类型 | 让悬停提示可读 🔥 |
| `UnionToIntersection<U>` | 联合转交叉 | 高级组合 |
| `Brand<T, B>` | 品牌类型 | 区分同构 ID |
| `NonEmptyArray<T>` | 非空数组 | 避免空数组分支 |
| `Exact<T, Shape>` | 精确匹配 | 禁止多余属性 |
| `Equals<A, B>` | 类型相等判断 | 类型层条件判断 |

---

## 修饰符类配方

{{< tabpane text=true persist=disabled >}}

{{% tab header="Mutable / 深层层级" %}}

```typescript
// 去只读（浅层）
type Mutable<T> = { -readonly [K in keyof T]: T[K] };

// 深层可选
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

// 深层只读（正确保留数组语义）
type DeepReadonly<T> = T extends (infer U)[]
  ? readonly DeepReadonly<U>[]
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;
```

用法与效果：

```typescript
type Config = {
  readonly server: { readonly host: string; readonly port: number };
};

type P = DeepPartial<Config>;
// { server?: { host?: string; port?: number } } ✅ 每层都可选

type R = DeepReadonly<{ list: { id: number }[] }>;
// { readonly list: readonly { readonly id: number }[] } ✅ 数组也变只读
```

⚠️ **`DeepReadonly` 必须显式处理数组**。如果只写 `T extends object ? { readonly [K in keyof T]: ... }`，数组会走对象分支，得到一个「看起来像数组但不是」的怪类型：

```typescript
// 🛑 漏掉数组处理的后果：元组方法类型被破坏
type BadDeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: BadDeepReadonly<T[K]> }
  : T;

type Bad = BadDeepReadonly<{ list: number[] }>;
// { readonly list: { readonly [x: number]: number; ...一堆数组方法 } }
//                             ^^^^^^^^ 索引签名而不是 readonly number[]
```

{{% /tab %}}

{{% tab header="精确匹配类" %}}

```typescript
// 会检查键是否存在的 Omit 🔥
type StrictOmit<T, K extends keyof T> = Omit<T, K>;

// 精确形状：禁止多余属性
type Exact<T, Shape> = T extends Shape
  ? Exclude<keyof T, keyof Shape> extends never
    ? T
    : never
  : never;

// 类型相等判断（最可靠的实现）
type Equals<A, B> =
  (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2)
    ? true
    : false;
```

`StrictOmit` 的价值在重构时体现：

```typescript
interface User { id: number; name: string; email: string }

type A = Omit<User, "typo">;        // ✅ 不报错，静默什么都不排除 ⚠️
type B = StrictOmit<User, "typo">;
// ❌ TS2344: Type '"typo"' does not satisfy the constraint 'keyof User'.
```

> 💡 **重构时把 `Omit` 全换成 `StrictOmit`**，键改名后编译器会立刻告诉你哪里漏了。这是低成本高收益的一招。

`Equals` 的用途——在类型层做条件分支：

```typescript
type IsAny<T> = Equals<T, any>;
type IsNever<T> = Equals<T, never>;
type IsUnion<T> = T extends infer U
  ? [U] extends [T] ? ( [T] extends [U] ? false : true ) : false
  : false;

type A = IsAny<any>;        // true
type B = IsNever<never>;    // true
```

> ⚠️ **为什么不用 `T extends any ? true : false` 判 `any`**：`any` 与任何类型都「可赋」，那个写法永远返回 `true`。`Equals` 用的是编译器内部的类型同一性，才能正确区分。

{{% /tab %}}

{{% tab header="按条件筛选" %}}

```typescript
// 按值类型挑键
type KeysOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never
}[keyof T];

// 按值类型挑属性（保留类型）
type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};

// 按值类型排除属性
type OmitByValue<T, V> = {
  [K in keyof T as T[K] extends V ? never : K]: T[K];
};

// 只挑可选属性 / 只挑必需属性
type OptionalKeys<T> = {
  [K in keyof T as {} extends Pick<T, K> ? K : never]: T[K];
};
type RequiredKeys<T> = {
  [K in keyof T as {} extends Pick<T, K> ? never : K]: T[K];
};
```

```typescript
interface User { id: number; name: string; email: string; age?: number }

type S = KeysOfType<User, string>;      // "name" | "email"  ✅（实测）
type O = OptionalKeys<User>;            // { age?: number }
type R = RequiredKeys<User>;            // { id: number; name: string; email: string }
```

**筛掉函数属性**（序列化场景常用）：

```typescript
type DataOnly<T> = {
  [K in keyof T as T[K] extends (...args: any[]) => any ? never : K]: T[K];
};
```

> ⚠️ `{} extends Pick<T, K>` 检测可选属性是**社区惯用法**，不是语言保证的特性。它依赖 `{}` 可赋给「全可选对象」这一行为，实践中很稳定，但要知道它属于技巧而非规范。

{{% /tab %}}

{{% tab header="联合操作类" %}}

```typescript
// 联合转交叉 🔥
type UnionToIntersection<U> =
  (U extends any ? (k: U) => void : never) extends (k: infer I) => void
    ? I
    : never;

// 取联合的最后一个成员
type LastOf<T> = UnionToIntersection<
  T extends any ? () => T : never
> extends () => infer R ? R : never;

// 联合转元组（TS 4.x 常用，较复杂）
type UnionToTuple<T, L = LastOf<T>> = [T] extends [never]
  ? []
  : [...UnionToTuple<Exclude<T, L>>, L];

// 非空数组
type NonEmptyArray<T> = [T, ...T[]];

// 数组去重（类型层）
type Unique<T extends readonly unknown[], Acc extends unknown[] = []> =
  T extends readonly [infer H, ...infer R]
    ? H extends Acc ? Unique<R, Acc> : Unique<R, [...Acc, H]>
    : Acc;
```

```typescript
type I = UnionToIntersection<{ a: 1 } | { b: 2 }>;   // { a: 1 } & { b: 2 }  ✅（实测）
type N = NonEmptyArray<string>;                      // [string, ...string[]]
type U = Unique<[1, 2, 1, 3]>;                       // [1, 2, 3]
```

> ⚠️ `UnionToTuple` 这类配方**依赖联合成员的顺序**，而联合顺序在 TS 里**没有稳定保证**。所以它适合「做点什么」，不适合「依赖精确顺序」。💭

{{% /tab %}}

{{< /tabpane >}}

---

## 「至少一个 / 恰好一个」类配方

这类配方用于**互斥或必选**的参数建模，是表单、查询条件、选项对象的常见需求。

```typescript
// 至少一个键必填
type RequireAtLeastOne<T, K extends keyof T = keyof T> =
  Omit<T, K> & { [P in K]-?: Required<Pick<T, P>> & Partial<Pick<T, Exclude<K, P>>> }[K];

// 恰好一个键必填（互斥）
type RequireExactlyOne<T, K extends keyof T = keyof T> =
  Omit<T, K> & {
    [P in K]: Required<Pick<T, P>> & Partial<Record<Exclude<K, P>, never>>
  }[K];

// 全部必填或全部不填
type AllOrNone<T> = T | { [K in keyof T]?: never };
```

用法：

```typescript
type SearchParams = RequireAtLeastOne<{
  byId?: string;
  byName?: string;
  byEmail?: string;
}>;

const a: SearchParams = { byId: "1" };                    // ✅
const b: SearchParams = { byId: "1", byName: "x" };       // ✅ 可以多个
const c: SearchParams = {};                               // ❌ 一个都没有

type Shape = RequireExactlyOne<{ circle: number; square: number }>;

const s1: Shape = { circle: 1 };            // ✅
const s2: Shape = { circle: 1, square: 2 }; // ❌ 两个都给
const s3: Shape = {};                       // ❌ 都没给

type Opts = AllOrNone<{ timeout: number; retries: number }>;
const o1: Opts = {};                        // ✅
const o2: Opts = { timeout: 1, retries: 2 }; // ✅
const o3: Opts = { timeout: 1 };            // ❌ 只给一个
```

> ⚠️ 这类「互斥」类型有个已知限制：**赋值检查严格，但函数参数的位置推断有时会放宽**。它们的核心价值是**在编译期拦住明显错误**，不是数学意义上的完备保证。

---

## 品牌类型与名义化

```typescript
declare const brand: unique symbol;

// 通用品牌类型工厂
type Brand<T, B extends string> = T & { readonly [brand]: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
type Cents = Brand<number, "Cents">;
type Dollars = Brand<number, "Dollars">;

// 铸造函数（唯一允许断言的地方）
const UserId = (s: string): UserId => s as UserId;
const OrderId = (s: string): OrderId => s as OrderId;

// 内部算术保持品牌
const addCents = (a: Cents, b: Cents): Cents => (a + b) as Cents;

// 只在边界处解包
const toNumber = (c: Cents): number => c;
```

```typescript
declare const uid: UserId;
declare const oid: OrderId;
const a: OrderId = uid;      // ❌ TS2322: 无法互赋 ✅ 正是我们要的
const b: string = uid;       // ✅ 可以当 string 用（子类型）
```

**用私有成员实现「运行时有区分」的名义类型**（[04]({{< relref "04-Functions-Objects-and-Classes.md" >}}) 也提到）：

```typescript
class UserId {
  private readonly _brand!: void;   // 只存在于类型层
  constructor(readonly value: string) {}
}

class OrderId {
  private readonly _brand!: void;
  constructor(readonly value: string) {}
}

function findUser(id: UserId) { /* ... */ }
findUser(new OrderId("x"));
// ❌ TS2345: Types have separate declarations of a private property '_brand'.
```

| 方案 | 编译期区分 | 运行时区分 | 开销 | 适合 |
| --- | --- | --- | --- | --- |
| `Brand<T, B>` | ✅ | ❌ | 零 | 内部类型约束 🔥 |
| 私有成员类 | ✅ | ✅ | `new` 开销 | 跨模块边界、需运行时校验 |
| 包装对象 `{ value: T }` | ✅ | ✅ | 对象开销 | 需要携带元数据 |

> 💭 品牌类型最常见的批评是「到处 `as` 很烦」。经验做法：**只在系统边界（解析输入、构造实体）铸造，内部一律用品牌类型传递**。边界数量有限，`as` 也就集中在少数几个函数里。

---

## 展平与可读性

交叉类型在编辑器悬停提示里往往显示成一长串 `A & B & C & ...`，很难读。

```typescript
// 把交叉类型展平成单个对象类型 🔥
type Prettify<T> = { [K in keyof T]: T[K] } & {};

// 变体：只展平一层，保留嵌套结构
type Flatten<T> = T extends object
  ? { [K in keyof T]: T[K] }
  : T;
```

```typescript
type Raw = { a: 1 } & { b: 2 } & { c: 3 };
// 编辑器悬停显示：{ a: 1 } & { b: 2 } & { c: 3 }   😖

type Clean = Prettify<Raw>;
// 编辑器悬停显示：{ a: 1; b: 2; c: 3 }            😊
```

> 💡 **给公开 API 的返回类型套一层 `Prettify`**，能显著改善使用者的编辑器体验。代价是每次类型计算多一点点开销，但完全值得。

---

## 类型层字符串处理

```typescript
// 拆分路径
type Split<S extends string, D extends string = "/"> =
  S extends `${infer H}${D}${infer R}` ? [H, ...Split<R, D>] : [S];

// 提取路由参数
type RouteParams<T extends string> =
  T extends `${string}:${infer P}/${infer R}`
    ? P | RouteParams<`/${R}`>
    : T extends `${string}:${infer P}`
      ? P
      : never;

// 去掉前缀
type StripPrefix<S extends string, P extends string> =
  S extends `${P}${infer R}` ? R : S;

// 短横线转驼峰
type KebabToCamel<S extends string> =
  S extends `${infer H}-${infer T}`
    ? `${H}${Capitalize<KebabToCamel<T>>}`
    : S;
```

```typescript
type P1 = RouteParams<"/user/:id/post/:postId">;   // "id" | "postId"  ✅
type P2 = Split<"a/b/c">;                          // ["a", "b", "c"]
type P3 = StripPrefix<"onClick", "on">;            // "Click"
type P4 = KebabToCamel<"my-long-name">;            // "myLongName"
```

**实战：类型安全的路由**

```typescript
type Routes = "/" | "/users" | "/users/:id" | "/posts/:postId/comments";

// 把 :id 位置变成必需参数
type ExtractParams<T extends string> =
  T extends `${string}:${infer P}/${infer R}`
    ? Record<P, string> & ExtractParams<`/${R}`>
    : T extends `${string}:${infer P}`
      ? Record<P, string>
      : {};

type RouteArgs<R extends string> = ExtractParams<R> extends infer P
  ? keyof P extends never ? [] : [params: P]
  : [];

function navigate<R extends Routes>(route: R, ...args: RouteArgs<R>): void { /* ... */ }

navigate("/");                                       // ✅
navigate("/users");                                  // ✅
navigate("/users/:id", { id: "1" });                 // ✅
navigate("/users/:id");                              // ❌ 缺少参数
navigate("/users/:id", { wrong: "1" });              // ❌ 参数名不对
```

> ⚠️ 这类配方的**编译开销不可忽视**。上面这个 `navigate` 在路由很多的库里会明显拖慢类型检查。**路由数量超过几十条时，建议退回到「手写参数类型」**。

---

## 类型体操的代价边界 💭

这是本页最重要的一节。类型层编程**不是免费的**。

### 代价一：编译时间

每多一层条件类型/映射类型，`Instantiations` 就多一批。

```bash
npx tsc --noEmit --extendedDiagnostics
# Types:          1234567
# Instantiations: 9876543     ← 这个数爆炸就是类型体操过重的信号
# Check time:     45.67s
```

### 代价二：错误信息不可读

```typescript
type Result = DeepReadonly<DeepPartial<Prettify<UnionToIntersection<T>>>>;
// 一旦报错，错误信息里是一坨无法阅读的类型展开
```

### 代价三：编辑器变慢

悬停要算几秒、自动补全卡顿，都是类型计算过重的表现。

### 什么时候该收手

| 信号 | 处理 |
| --- | --- |
| `Instantiations` 超过百万 | 简化类型，或缓存中间结果 |
| 编辑器悬停明显卡顿 | 拆成多个具名类型别名 |
| 报错信息无法理解 | 加 `Prettify`，或退回手写类型 |
| 为「省一次断言」写了 20 行类型 | 🛑 不值 |
| 团队成员看不懂 | 🛑 维护成本大于收益 |
| 类型推导结果需要写注释才能解释 | ⚠️ 考虑简化 |

**核心判断标准** 🔥：

> **类型层代码是为了让「用错」变成编译错误。如果一段类型体操的收益只是「少写一个 `as`」，那它就不值得。**

真正值得的类型体操通常满足：**使用者很多、误用代价高、逻辑稳定不常改**。库的公开 API 符合；业务代码里的一个内部函数通常不符合。

### 中间结果缓存

避免重复计算同一类型：

```typescript
// 🛑 每次用都重新算
function f1<T>(x: T): DeepReadonly<DeepPartial<T>> { /* ... */ }
function f2<T>(x: T): DeepReadonly<DeepPartial<T>> { /* ... */ }

// ✅ 起个名字，通常也会被复用
type FrozenPatch<T> = DeepReadonly<DeepPartial<T>>;
function f3<T>(x: T): FrozenPatch<T> { /* ... */ }
function f4<T>(x: T): FrozenPatch<T> { /* ... */ }
```

> 💡 具名类型别名除了可读性，也有助于编译器复用已计算的结果。**给复杂类型起名字是好习惯**。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| `Omit` 拼错键 | 静默不排除 | 用 `StrictOmit` |
| `DeepReadonly` 漏数组 | 数组变成怪对象 | 显式 `T extends (infer U)[]` 分支 |
| 用 `T extends any` 判 `any` | 永远 `true` | 用 `Equals<T, any>` |
| 依赖联合顺序 | 结果不稳定 | 别依赖 `UnionToTuple` 的顺序 |
| 交叉类型不可读 | 悬停一长串 | 套 `Prettify` |
| 类型体操过重 | `TS2589` / 编译慢 | 加深度计数器，或简化 |
| 为省 `as` 写复杂类型 | 维护成本高 | 权衡后可能直接 `as` 更好 |
| 品牌类型到处 `as` | 断言泛滥 | 只在边界铸造 |
| 互斥类型当万能 | 某些位置推断放宽 | 当作「拦住常见错误」用 |
