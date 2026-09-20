+++
title = "05 泛型与类型推断"
weight = 105
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "泛型约束与默认值、推断规则、条件类型与分配律、infer、映射类型、变型标注"
isCJKLanguage = true
draft = false
+++

# 05 泛型与类型推断

泛型是「类型的参数」。这一页从**怎么写**讲到**编译器怎么推**，最后是**条件类型与映射类型**——TypeScript 类型编程的两块基石。

> 本页的类型推断结论用 `Eq<A, B>` 断言**逐条实测**过（`tsc 6.0.3`），不是推测。

---

## 泛型基础

{{< tabpane text=true persist=disabled >}}

{{% tab header="函数 / 接口 / 类" %}}

```typescript
// 泛型函数
function identity<T>(x: T): T { return x; }
const a = identity("x");        // T 推断为 "x"
const b = identity<string>("x");// 显式指定，T = string

// 泛型接口
interface Box<T> { value: T }
const box: Box<number> = { value: 1 };

// 泛型类型别名
type Pair<A, B> = { first: A; second: B };

// 泛型类
class Stack<T> {
  private items: T[] = [];
  push(item: T) { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
}
const s = new Stack<number>();
s.push(1);
s.push("x");          // ❌ TS2345: Argument of type 'string' is not assignable to 'number'.

// 泛型箭头函数（.tsx 里需加逗号避免与 JSX 冲突）
const id = <T,>(x: T): T => x;
```

**多参数与默认值**：

```typescript
type Result<T, E = Error> = { ok: true; data: T } | { ok: false; error: E };

type R1 = Result<string>;              // E 用默认值 Error
type R2 = Result<string, TypeError>;   // 显式指定 E
```

⚠️ **默认值必须放在必需参数之后**，且**有默认值的参数可以省略**：

```typescript
type Box2<T extends object = {}> = { value: T };
type B1 = Box2;              // ✅ 合法，T = {}
type B2 = Box2<{ a: 1 }>;    // ✅
```

{{% /tab %}}

{{% tab header="约束 extends" %}}

`extends` 在泛型里表示**约束**（不是继承）。

```typescript
// 约束 T 必须有 length
function len<T extends { length: number }>(x: T): number {
  return x.length;
}
len("abc");        // ✅
len([1, 2]);       // ✅
len(123);          // ❌ TS2345: Argument of type 'number' is not assignable to
                   //    parameter of type '{ length: number; }'.
```

| 约束写法 | 含义 |
| --- | --- |
| `<T extends U>` | `T` 必须是 `U` 的子类型 |
| `<T extends keyof U>` | `T` 是 `U` 的键 |
| `<T extends object>` | `T` 是非原始类型 |
| `<T extends unknown[]>` | `T` 是数组/元组 |
| `<T extends abstract new (...a: any) => any>` | `T` 是构造函数 |
| `<T, K extends keyof T>` | 依赖前一个参数 🔥 |

**依赖型约束**（最实用的形态）：

```typescript
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];          // ✅ 返回类型精确到属性类型
}

const user = { name: "a", age: 1 };
const n = get(user, "name");   // string
const g = get(user, "age");    // number
get(user, "typo");             // ❌ TS2345: '"typo"' is not assignable to '"name" | "age"'.
```

⚠️ **约束里不能用 `T` 自己的成员做默认值以外的依赖**，且要注意「约束是上界、不是上转」：

```typescript
function bad<T extends { a: number }>(x: T) {
  return x.a;          // ✅ 可以读约束里声明的成员
  // return x.b;       // ❌ TS2339: Property 'b' does not exist on type 'T'.
}
```

**约束不会收窄实参类型**——`T` 保持精确：

```typescript
declare const lit: { a: 1; b: 2 };
const r = bad(lit);       // T 仍是 { a: 1; b: 2 }，不是 { a: number } ✅
```

{{% /tab %}}

{{% tab header="const 类型参数 🆕" %}}

TS 5.0 引入。默认情况下，对象/数组字面量传进泛型会被**拓宽**；加 `const` 修饰符可保持字面量。

```typescript
function withoutConst<T>(x: T) { return x; }
function withConst<const T>(x: T) { return x; }

const w1 = withoutConst({ a: 1 });   // { a: number }
const w2 = withConst({ a: 1 });      // { readonly a: 1 }        🔥
const w3 = withConst(["a", "b"]);    // readonly ["a", "b"]      🔥
const w4 = withoutConst(["a", "b"]); // string[]
```

（以上四条推断结果均以 `Eq<A, B>` 断言实测确认。）

**等价关系**：`withConst(x)` ≡ `withoutConst(x as const)`，但 `const` 类型参数**不要求调用方写 `as const`**，API 更友好。

**典型用途**：

```typescript
// 1. 路由/配置表：既要检查又要保留字面量
function defineRoutes<const T extends Record<string, `/${string}`>>(routes: T): T {
  return routes;
}
const routes = defineRoutes({
  home: "/",
  user: "/users/:id",
});
type RouteName = keyof typeof routes;      // "home" | "user"  ✅ 保留了

// 2. 元组保持长度
function tuple<const T extends readonly unknown[]>(...args: T): T { return args; }
const t = tuple(1, "a", true);             // readonly [1, "a", true]
```

⚠️ **`const` 类型参数会让属性变 `readonly`**——如果调用方需要可变，得显式去掉：

```typescript
function f<const T>(x: T): T { return x; }
const o = f({ a: 1 });      // { readonly a: 1 }
// o.a = 2;                 // ❌ TS2540
```

> 💭 `const` 类型参数最适合**「配置对象 / 常量表」类的 API**。普通数据转换函数加了它反而添麻烦（处处 `readonly`）。用在刀刃上。

{{% /tab %}}

{{% tab header="NoInfer 🆕" %}}

TS 5.4 引入。默认情况下，**所有**出现 `T` 的位置都会参与推断——有时这是错的。

```typescript
// 🛑 问题：期望 initial 被 states 约束，实际却反过来扩大了 T
function fsmBad<T extends string>(states: T[], initial: T) { return initial; }

const r1 = fsmBad(["idle", "done"], "idle");     // T = "idle" | "done" （恰好对）
const r2 = fsmBad(["idle", "done"], "typo");     // T = "idle" | "done" | "typo" ⚠️ 竟然通过！
```

```typescript
// ✅ 用 NoInfer 排除该位置的推断
function fsm<T extends string>(states: T[], initial: NoInfer<T>) { return initial; }

fsm(["idle", "done"], "idle");   // ✅ T = "idle" | "done"
fsm(["idle", "done"], "typo");
// ❌ TS2345: Argument of type '"typo"' is not assignable to parameter of type '"idle" | "done"'.
```

| 场景 | 是否该用 `NoInfer` |
| --- | --- |
| 参数是「默认值 / 回退值」，应从主参数推断 | ✅ 用 |
| 状态机的初始值 | ✅ 用 |
| 校验函数的目标类型 | ✅ 用 |
| 普通数据转换 | ❌ 不需要 |
| 想让每个参数都参与推断 | ❌ 不要用 |

**替代方案**（`NoInfer` 出现前的老写法）：

```typescript
// 用条件类型把候选排除
type NoInferOld<T> = [T][T extends any ? 0 : never];
```

> 💡 `NoInfer` 的核心作用：**让某个参数从「推断来源」降级为「检查对象」**。

{{% /tab %}}

{{< /tabpane >}}

---

## 推断规则

{{< tabpane text=true persist=disabled >}}

{{% tab header="推断从哪来" %}}

| 来源 | 例子 | 说明 |
| --- | --- | --- |
| 实参 | `identity("x")` → `T = "x"` | 最主要来源 |
| 上下文类型 | `[1].map(x => x + 1)` | 从目标类型反推参数类型 |
| 返回值 | — | **返回值不参与 `T` 的推断** ⚠️ |
| 显式类型参数 | `identity<string>("x")` | 优先级最高，直接指定 |
| 默认值 | `<T = string>` | 推断失败时兜底 |

⚠️ **返回值不能推断泛型参数**：

```typescript
// 🛑 期望通过返回值推断 T，实际 T 变成 unknown
function make<T>(): T { return {} as T; }
const x = make();          // T = unknown
const y = make<string>();  // ✅ 必须显式指定
```

⚠️ **推断失败会退化成约束或 `unknown`**：

```typescript
function first<T>(arr: T[]): T | undefined { return arr[0]; }
const f1 = first([1, 2]);       // T = number ✅
const f2 = first([]);           // T = never ⚠️ 空数组推不出来
const f3 = first(null as any);  // T = any
```

**推断顺序**：TS 会**跳过**「上下文敏感」的函数参数，先从其它实参推断，再回头检查回调。

```typescript
function map<T, U>(arr: T[], fn: (x: T) => U): U[] { return arr.map(fn); }

// T 从 arr 推断，U 从 fn 的返回值推断
const r = map([1, 2], (n) => n.toString());   // r: string[]
```

> ⚠️ 这个「跳过」行为导致方法语法与箭头函数在某些场景下有差异（TS 6.0 收窄了这个差异，见 [官方 6.0 公告](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/)）。实践中遇到推断意外失败时，**显式写类型参数**永远是最快的解法。

{{% /tab %}}

{{% tab header="手动控制推断" %}}

| 手段 | 写法 | 效果 |
| --- | --- | --- |
| 显式类型参数 | `f<number>(x)` | 跳过推断 |
| 显式标注参数 | `(x: number) => ...` | 提供上下文类型 |
| 上下文类型 | 目标类型已知时自动发生 | 回调参数自动有类型 |
| `NoInfer` | `NoInfer<T>` | 该位置不参与推断 |
| `const` 类型参数 | `<const T>` | 保持字面量 |
| 断言 | `x as T` | 🛑 最后手段 |

```typescript
// 上下文类型：参数自动获得类型，不用重复标注
const nums: number[] = [];
nums.map((n) => n.toFixed(2));    // n 自动是 number

// 显式类型参数解决推断失败
const empty = first<string>([]);   // T = string，而不是 never

// 显式标注回调参数（当上下文丢失时）
declare const cb: (f: (x: { id: number }) => void) => void;
cb((x: { id: number }) => x.id);
```

> 💡 **排查推断问题的顺序**：① 鼠标悬停看推出来的类型 → ② 显式写一个类型参数验证猜想 → ③ 用 `NoInfer` / `const` 修正。绝大多数「推断不对」都是因为某个位置**不该参与推断却参与了**，或**该参与却没参与**。

{{% /tab %}}

{{< /tabpane >}}

---

## 条件类型

条件类型的语法是 `T extends U ? X : Y`，读作「若 `T` 可赋给 `U`，则 `X`，否则 `Y`」。

{{< tabpane text=true persist=disabled >}}

{{% tab header="基础与分配律" %}}

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;   // true
type B = IsString<number>;   // false
```

⚠️ **分配律**（distributive conditional types）——这是条件类型最重要的行为，也是最大的坑：

**当 `T` 是「裸类型参数」时，条件类型会对联合的每个成员分别求值，再合并结果。**

```typescript
type ToArray<T> = T extends unknown ? T[] : never;

type A1 = ToArray<string | number>;   // string[] | number[]   ← 分配了！
```

**阻止分配**——用元组把它包起来：

```typescript
type NoDist<T> = [T] extends [unknown] ? T[] : never;

type A2 = NoDist<string | number>;    // (string | number)[]   ← 不分配
```

（以上两条均以 `Eq<A, B>` 断言实测确认。）

**实用推论**：`Exclude` / `Extract` 正是靠分配律实现的。

```typescript
type MyExclude<T, U> = T extends U ? never : T;
type R = MyExclude<"a" | "b" | "c", "a">;   // "b" | "c"
// 展开过程：
// ("a" extends "a" ? never : "a") | ("b" extends "a" ? never : "b") | ("c" ...)
// = never | "b" | "c" = "b" | "c"
```

🔑 **判定口诀**：

| 写法 | 是否分配 |
| --- | --- |
| `T extends U ? ...`（`T` 是裸参数） | ✅ 分配 |
| `[T] extends [U] ? ...` | ❌ 不分配 🔥 |
| `T & {} extends U ? ...` | ❌ 不分配 |
| 具体类型 `string extends U ? ...` | ❌ 不分配（不是参数） |

**`never` 在条件类型里的特殊行为** ⚠️：

```typescript
type A3 = IsString<never>;              // never ⚠️ 不是 false！
// 因为 never 是空联合，分配后没有任何成员，结果是 never

// 想正确判定 never 必须包元组
type IsNever<T> = [T] extends [never] ? true : false;
type A4 = IsNever<never>;               // true  ✅
type A5 = IsNever<string>;              // false ✅
```

（`A4`/`A5` 同样实测确认。）

{{% /tab %}}

{{% tab header="infer" %}}

`infer` 在条件类型里**声明一个待推断的类型变量**。

```typescript
// 解包 Promise
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type A = Unwrap<Promise<string>>;    // string
type B = Unwrap<number>;             // number

// 取数组元素类型
type El<T> = T extends (infer U)[] ? U : never;
type C = El<string[]>;               // string

// 取函数返回值
type Ret<T> = T extends (...args: never[]) => infer R ? R : never;
type D = Ret<() => number>;          // number

// 取函数参数（更简单的做法：内置 Parameters）
type Args<T> = T extends (...args: infer P) => unknown ? P : never;
type E = Args<(a: string, b: number) => void>;   // [a: string, b: number]
```

**多个 `infer` 与位置对应**：

```typescript
type Unpack2<T> =
  T extends Promise<infer U> ? Unpack2<U> :   // 递归解包
  T extends readonly (infer V)[] ? V :
  T;

type F = Unpack2<Promise<Promise<number[]>>>;   // number
```

**`infer ... extends`（TS 5.4+）**——在 `infer` 上直接加约束：

```typescript
// 只匹配第一个元素是 string 的元组
type FirstString<T> = T extends [infer S extends string, ...unknown[]] ? S : never;
type G = FirstString<["a", 1]>;      // "a"
type H = FirstString<[1, "a"]>;      // never

// 5.4 之前要写两层的写法
type FirstStringOld<T> =
  T extends [infer S, ...unknown[]] ? (S extends string ? S : never) : never;
```

**`infer` 在协变/逆变位置的差别** ⚠️：

```typescript
// 同一处 infer，位置决定推出来的类型
type Param<T> = T extends (x: infer P) => void ? P : never;   // 逆变位置
type RetOf<T> = T extends (x: never) => infer R ? R : never;  // 协变位置

type I = Param<(x: string) => void>;    // string
type J = RetOf<(x: string) => number>;  // number

// 同一函数类型，用在两个位置会得到不同的「最大公共」类型
type Both<T> = T extends (x: infer P) => infer R ? [P, R] : never;
type K = Both<(x: string | number) => boolean>;   // [string | number, boolean]
```

> 💭 记住：**逆变位置的 `infer` 会推出「最宽」的类型，协变位置推出「最窄」的**。

{{% /tab %}}

{{% tab header="递归与深度限制" %}}

递归条件类型可以处理嵌套结构，但有深度上限。

```typescript
// 递归解包 Promise（内置 Awaited 就是这么做的简化版）
type DeepUnwrap<T> = T extends Promise<infer U> ? DeepUnwrap<U> : T;
type A = DeepUnwrap<Promise<Promise<Promise<string>>>>;   // string

// 深层只读
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};
type DR = DeepReadonly<{ a: { b: { c: 1 } } }>;
// { readonly a: { readonly b: { readonly c: 1 } } }
```

⚠️ **深度限制**：TypeScript 对递归类型有实例化深度上限（约 50 层 / 5 百万次实例化），超出会报：

```text
error TS2589: Type instantiation is excessively deep and possibly infinite.
```

**处理递归过深的四种手段**：

| 手段 | 做法 |
| --- | --- |
| 加深度的计数器 | 用元组累加计数，到上限就停 |
| 改用尾递归形式 | TS 4.5+ 对特定形式的尾递归做了优化 |
| 降低递归范围 | 只在必要层级递归，别对所有键展开 |
| 直接放弃类型精度 | ⚠️ 有时返回 `any` 比报错好，但要注释说明 |

```typescript
// 用计数器限制递归深度
type Prev = [never, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

type DeepPartial<T, D extends number = 5> =
  D extends 0 ? T :
  { [K in keyof T]?: T[K] extends object ? DeepPartial<T[K], Prev[D]> : T[K] };
```

> ⚠️ **尾递归消除有条件**：必须是「直接返回自身」的特定形态，且 TS 对它有专门优化。写复杂的递归类型时，能写成尾递归就写，否则容易撞 `TS2589`。

{{% /tab %}}

{{< /tabpane >}}

---

## 映射类型

映射类型遍历键，构造新对象类型。它是 `Partial` / `Pick` / `Readonly` 等内置工具的实现基础。

{{< tabpane text=true persist=disabled >}}

{{% tab header="基本语法" %}}

```typescript
type MyPartial<T> = { [K in keyof T]?: T[K] };
type MyReadonly<T> = { readonly [K in keyof T]: T[K] };
type MyRequired<T> = { [K in keyof T]-?: T[K] };
type MyMutable<T>  = { -readonly [K in keyof T]: T[K] };
```

| 语法元素 | 含义 |
| --- | --- |
| `[K in keyof T]` | 遍历 `T` 的所有键 |
| `[K in "a" \| "b"]` | 遍历指定联合 |
| `?` / `+?` | 加可选 |
| `-?` | 去可选 |
| `readonly` / `+readonly` | 加只读 |
| `-readonly` | 去只读 |
| `as X` | **键重映射**（TS 4.1+）🆕 |

**同态 vs 非同态** 🔥：

| 类型 | 定义 | 特性 |
| --- | --- | --- |
| **同态** | `[K in keyof T]` | 保留原属性的修饰符（`?` / `readonly`） |
| **非同态** | `[K in SomeUnion]` | 不保留任何修饰符 |

```typescript
type Homomorphic<T> = { [K in keyof T]: T[K] };
type NonHomo<T> = { [K in keyof T & string]: T[K] };

type Src = { readonly a?: number; b: string };

type H = Homomorphic<Src>;   // { readonly a?: number; b: string }  ← 修饰符保留
type N = NonHomo<Src>;       // { a: number; b: string }             ← 修饰符丢失 ⚠️
```

> 💡 **这个区别非常实用**：`Partial<T>` 之所以能保留原有的 `readonly`，就是因为它是同态的。自己写映射类型时，**尽量用 `keyof T` 的裸形式**，修饰符行为才符合直觉。

{{% /tab %}}

{{% tab header="键重映射 as 🆕" %}}

用 `as` 子句**变换或过滤**键。

```typescript
// 加前缀生成 getter 类型
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
type G = Getters<{ name: string; age: number }>;
// { getName: () => string; getAge: () => number }

// 去掉特定前缀
type StripOn<T> = {
  [K in keyof T as K extends `on${infer E}` ? Uncapitalize<E> : never]: T[K];
};

// 按值类型筛选键（把值为函数的键挑出来）
type FunctionKeys<T> = {
  [K in keyof T as T[K] extends (...args: any[]) => any ? K : never]: T[K];
};

// 排除某些键
type OmitByKey<T, K extends PropertyKey> = {
  [P in keyof T as P extends K ? never : P]: T[P];
};
```

⚠️ **用 `never` 作为映射结果会把该键删掉**——这就是「过滤」的实现方式。

⚠️ `Capitalize<string & K>` 里的 `string &` 是必须的：`K` 的类型是 `string | number | symbol`，而 `Capitalize` 只接受 `string`。

```typescript
// 🛑 直接传 K 会报错
type Bad<T> = { [K in keyof T as `get${Capitalize<K>}`]: T[K] };
//                                          ~~~~~~~~~~~ error TS2345
// ✅ 加 string & 交叉
type Good<T> = { [K in keyof T as `get${Capitalize<string & K>}`]: T[K] };
```

{{% /tab %}}

{{% tab header="组合条件与映射" %}}

两者结合是类型编程的主力。

```typescript
// 把可选属性变必需，其余保持
type RequiredKeys<T> = {
  [K in keyof T as {} extends Pick<T, K> ? never : K]: T[K];
};
type OptionalKeys<T> = {
  [K in keyof T as {} extends Pick<T, K> ? K : never]: T[K];
};

// 按值类型分组
type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};
type StringsOnly = PickByValue<{ a: string; b: number; c: string }, string>;
// { a: string; c: string }

// 深层 Partial
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

// 深层只读（保留数组语义）
type DeepReadonly<T> = T extends (infer U)[]
  ? readonly DeepReadonly<U>[]
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;
```

> ⚠️ 注意 `{} extends Pick<T, K>` 这个惯用法：它用来**检测属性是否可选**。这是社区总结出的技巧，不是语言特性，但被广泛使用。

{{% /tab %}}

{{% tab header="变型标注 🆕" %}}

TS 4.7 引入，用于**显式声明泛型参数的变型**（variance annotation）。

```typescript
// out：T 只出现在输出位置（协变）
interface Producer<out T> {
  get(): T;
}

// in：T 只出现在输入位置（逆变）
interface Consumer<in T> {
  set(value: T): void;
}

// in out：双向（不变）
interface Both<in out T> {
  get(): T;
  set(value: T): void;
}
```

**作用**：

| 好处 | 说明 |
| --- | --- |
| 编译期校验 | 标错了会报错，而不是悄悄变得不健全 |
| **性能** | 让编译器跳过变型推断，**大项目编译更快** 🔥 |
| 可读性 | 让 API 作者的设计意图显式化 |

标错会被抓出来——但**只在函数属性位置上抓**（方法语法因双变而豁免，见下）：

```typescript
// ❌ 函数属性：T 在逆变位置，与 out 冲突
interface B<out T> {
  set: (value: T) => void;
  //   ~~~~~~~~~~~~~~~~~ error TS2636: Type 'B<sub-T>' is not assignable to type
  //                     'B<super-T>' as implied by variance annotation.
  //                     Types of property 'set' are incompatible.
}

// ❌ 返回值位置与 in 冲突
interface C<in T> {
  get(): T;
  //   ~ error TS2636: The types returned by 'get()' are incompatible
  //     between these types.
}
```

⚠️ **方法语法不参与变型检查**——这是必须知道的一个例外：

```typescript
interface Method<out T> { set(value: T): void }    // ✅ 不报错！
interface Prop<out T>   { set: (value: T) => void } // ❌ TS2636
```

原因和 [04 函数变型]({{< relref "04-Functions-Objects-and-Classes.md" >}}) 里讲的是同一件事：**方法参数是双变的**，双向都「可赋」，所以变型标注找不到矛盾。想让变型标注真正生效，把成员写成**函数属性**形式。

**各变型标注的正确性检查**：

| 标注 | `T` 允许出现的位置 |
| --- | --- |
| `out T` | 只读属性、返回值、`readonly T[]` 元素 |
| `in T` | 参数、只写属性 |
| `in out T` | 任意位置（默认行为） |
| 不标注 | 编译器自动推断 |

> 💭 **给库作者的建议**：公开的泛型接口上加变型标注值得做——既能在编译期自证设计正确，又能改善使用者的编译速度。业务代码里一般不需要。

{{% /tab %}}

{{< /tabpane >}}

---

## 泛型实战模式

### 类型安全的事件系统

```typescript
type EventMap = {
  click: { x: number; y: number };
  keydown: { key: string };
};

class Emitter<T extends Record<string, unknown>> {
  private handlers: Partial<{
    [K in keyof T]: Array<(payload: T[K]) => void>
  }> = {};

  on<K extends keyof T>(event: K, handler: (payload: T[K]) => void): void {
    (this.handlers[event] ??= []).push(handler);
  }

  emit<K extends keyof T>(event: K, payload: T[K]): void {
    this.handlers[event]?.forEach((h) => h(payload));
  }
}

const em = new Emitter<EventMap>();
em.on("click", (p) => p.x.toFixed(2));   // ✅ p 自动是 { x: number; y: number }
em.on("keydown", (p) => p.key.length);   // ✅ p 自动是 { key: string }
em.emit("click", { x: 1, y: 2 });        // ✅
em.emit("click", { key: "a" });          // ❌ TS2345: 缺少 x, y
```

### 类型安全的 `get` / `set`

```typescript
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

function set<T, K extends keyof T>(obj: T, key: K, value: T[K]): void {
  obj[key] = value;
}

const cfg = { host: "a", port: 80 };
get(cfg, "port");            // number
set(cfg, "port", 8080);      // ✅
set(cfg, "port", "8080");    // ❌ TS2345: 'string' is not assignable to 'number'
```

### 函数式管道

```typescript
function pipe<A, B>(f: (a: A) => B): (a: A) => B;
function pipe<A, B, C>(f: (a: A) => B, g: (b: B) => C): (a: A) => C;
function pipe<A, B, C, D>(f: (a: A) => B, g: (b: B) => C, h: (c: C) => D): (a: A) => D;
function pipe(...fns: Array<(x: unknown) => unknown>) {
  return (x: unknown) => fns.reduce((acc, fn) => fn(acc), x);
}

const f = pipe(
  (s: string) => s.length,          // string -> number
  (n: number) => n > 0,             // number -> boolean
  (b: boolean) => (b ? "yes" : "no"), // boolean -> string
);
const out = f("abc");               // string ✅
```

### 从常量表推导联合

```typescript
const STATUS = ["idle", "loading", "done"] as const;
type Status = (typeof STATUS)[number];   // "idle" | "loading" | "done" 🔥

// 反向：从联合生成可穷举的映射
const LABELS: Record<Status, string> = {
  idle: "空闲",
  loading: "加载中",
  done: "完成",
  // 漏一个就报错：❌ TS2741: Property 'done' is missing
};
```

> 🔥 这两个模式配合起来非常强：**联合类型 + `Record<联合, T>` 强制穷举**，新增成员时编译器会告诉你所有需要改的地方。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 期望从返回值推断泛型 | `T` 变成 `unknown` | 显式指定类型参数 |
| 空数组推断 | `T = never` | `f<string>([])` |
| 条件类型意外分配 | 得到联合而非单个类型 | 用 `[T] extends [U]` 包住 |
| `IsNever<T>` 判错 | `never` 结果仍是 `never` | `[T] extends [never]` |
| `infer` 加约束 | 5.4 前写法冗长 | 用 `infer S extends string` |
| 映射类型丢修饰符 | `?` / `readonly` 消失 | 用同态形式 `[K in keyof T]` |
| 键重映射报错 | `Capitalize<K>` 不合法 | `Capitalize<string & K>` |
| 递归过深 | `TS2589` | 加计数器限制深度 |
| 默认值参数参与推断 | 意外扩大联合 | 用 `NoInfer<T>` |
| `const` 类型参数处处只读 | 无法修改 | 只在常量表类 API 使用 |
| 变型标注写错 | `TS2636` | 按 `T` 出现的位置选 `in` / `out` |
