+++
title = "02 类型系统主干"
weight = 102
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "原始类型全表、any/unknown/never 之辨、类型运算符、组合类型与内置工具类型"
isCJKLanguage = true
draft = false
+++

# 02 类型系统主干

本页是整套速查表的地基。`any` / `unknown` / `never` / `{}` / `object` 这几个概念如果没理清，后面每一页都会看不懂。

> 所有 `❌ TSxxxx` 标注均为 TS 6.0.3 实测错误码，可去 [09 错误码]({{< relref "09-Diagnostics-and-Error-Codes.md" >}}) 反查。

---

## 原始类型与字面量

{{< tabpane text=true persist=disabled >}}

{{% tab header="原始类型" %}}

| 类型 | 写法 | 说明 |
| --- | --- | --- |
| 字符串 | `string` | UTF-16 序列 |
| 数字 | `number` | 双精度浮点，**没有 `int`** |
| 布尔 | `boolean` | `true` / `false` |
| 大整数 | `bigint` | `123n`，需 `target` ≥ ES2020 |
| 符号 | `symbol` | `Symbol()` |
| 空 | `null` | 需 `strictNullChecks`（6.0 默认开）才与其它类型区分 |
| 未定义 | `undefined` | 同上 |
| 永不存在的值 | `never` | 空集，见下节 |

⚠️ **包装对象类型不是原始类型**，这是最高频的新手错误：

```typescript
const a: string = "x";        // ✅ 原始类型（永远用这个）
const b: String = "x";        // ⚠️ 合法但是包装对象，别用
const c: string = new String("x");  // ❌ TS2322: 'String' is not assignable to 'string'
```

| 🛑 别用 | ✅ 用 | 原因 |
| --- | --- | --- |
| `String` | `string` | 包装对象类型几乎总是写错了 |
| `Number` | `number` | 同上 |
| `Boolean` | `boolean` | 同上 |
| `Symbol` | `symbol` | 同上 |
| `BigInt` | `bigint` | 同上 |
| `Object` | `object` 或具体形状 | `Object` 几乎接受一切，等于没约束 |

> 💭 例外：极少数库的 API 确实要求包装对象类型（因为要挂方法），照文档写即可，但**自己定义类型时永远用小写**。

{{% /tab %}}

{{% tab header="字面量类型" %}}

字面量本身就是类型，表示「只能是这一个值」。

```typescript
type Direction = "up" | "down";   // 字符串字面量联合——最常用的建模手段 🔥
type Dice = 1 | 2 | 3 | 4 | 5 | 6;
type Yes = true;

const a: Direction = "up";        // ✅
const b: Direction = "left";      // ❌ TS2322: '"left"' is not assignable to '"up" | "down"'
```

**字面量何时会被「拓宽」**——这是最容易困惑的地方：

| 写法 | 推导出的类型 | 原因 |
| --- | --- | --- |
| `const x = "a"` | `"a"` | `const` 不能重新赋值，保持最窄 |
| `let x = "a"` | `string` | `let` 可能被改，拓宽为 `string` |
| `const o = { k: "a" }` | `{ k: string }` | **对象属性会被拓宽** ⚠️ |
| `const o = { k: "a" } as const` | `{ readonly k: "a" }` | `as const` 阻止拓宽 🔥 |
| `const arr = [1, 2]` | `number[]` | 数组元素被拓宽 |
| `const arr = [1, 2] as const` | `readonly [1, 2]` | 变成只读元组 |

```typescript
// as const 的典型用途：让配置对象保留精确字面量
const config = {
  host: "localhost",
  port: 8080,
  mode: "dev",
} as const;

type Mode = typeof config.mode;   // "dev"（而不是 string）
type Port = typeof config.port;   // 8080（而不是 number）
```

**模板字面量类型**（TS 4.1+）：在类型层面做字符串拼接。

```typescript
type Greeting = `hello ${string}`;
const g1: Greeting = "hello world";   // ✅
const g2: Greeting = "goodbye";       // ❌ TS2322

// 组合内置字符串工具类型
type EventName = "click" | "focus";
type Handler = `on${Capitalize<EventName>}`;   // "onClick" | "onFocus"

// 解析字符串结构（配合 infer，见 05）
type ExtractRouteParam<T> = T extends `${string}:${infer P}` ? P : never;
type P = ExtractRouteParam<"/user/:id">;   // "id"
```

{{% /tab %}}

{{% tab header="unique symbol" %}}

`symbol` 的类型层面细化，用于**保证唯一性**，是品牌类型（branded type）的基石之一。

```typescript
const KEY: unique symbol = Symbol("key");   // 必须 const + 直接初始化
type KEY = typeof KEY;                      // 类型是 typeof KEY，不是 symbol

const other: symbol = Symbol("key");
const bad: typeof KEY = other;   // ❌ TS2322: symbol 不能赋给 unique symbol
```

```typescript
// 用 unique symbol 做「名义类型」标记
declare const brand: unique symbol;
type UserId = string & { readonly [brand]: "UserId" };
type OrderId = string & { readonly [brand]: "OrderId" };

declare const uid: UserId;
declare const oid: OrderId;
const x: OrderId = uid;   // ❌ TS2322: 两者结构不同，无法互赋 🔥
```

{{% /tab %}}

{{% tab header="void / undefined / null" %}}

| 类型 | 含义 | 典型位置 |
| --- | --- | --- |
| `void` | 函数**没有有意义的返回值** | 回调返回值位置 |
| `undefined` | 值不存在 | 可选属性、未初始化变量 |
| `null` | 显式的空值 | API 返回、DOM 查询 |

⚠️ **`void` 的特例**：`() => void` 作为**回调类型**时，允许传入有返回值的函数。

```typescript
type Callback = () => void;

const returnsNumber = () => 42;
const cb: Callback = returnsNumber;   // ✅ 合法！

// 原因：调用方声明「我不关心返回值」，实现返回什么都无害
[1, 2, 3].forEach((n) => n * 2);      // ✅ 箭头函数返回了值，照样合法

// 但直接声明返回值时必须一致
function f(): void { return 42; }      // ❌ TS2322: Type 'number' is not assignable to type 'void'
```

> ⚠️ `void` 不等于 `undefined`。`void` 表示「不要使用这个值」，把它赋给变量再读取会被拦：
>
> ```typescript
> declare const v: void;
> const u: undefined = v;   // ✅ 允许
> const n: number = v;      // ❌ TS2322
> ```

{{% /tab %}}

{{< /tabpane >}}

---

## 特殊类型：`any` / `unknown` / `never` / `{}`

这一组是 TypeScript 里最需要「一次搞清楚」的东西。

{{< tabpane text=true persist=disabled >}}

{{% tab header="any（关掉检查）" %}}

`any` 的含义是「**放弃类型检查**」。它既是所有类型的父类型，也是所有类型的子类型。

```typescript
declare const an: any;
const s: string = an;        // ✅ 不报错
const n: number = an;        // ✅ 也不报错（同一个值赋给两种类型都行）
an.whatever.deeply.nested(); // ✅ 不报错
const r = an + 1;            // r 是 any
```

**`any` 会传染**——这是它真正的危险之处：

```typescript
declare const an: any;
const x = an.foo;            // x: any
const y = x.bar;             // y: any
function f(a: any) { return a.baz; }
const z = f(1);              // z: any
```

| 传染途径 | 例子 |
| --- | --- |
| 属性访问 | `anyValue.anything` |
| 函数调用返回值 | `anyFn()` |
| 数组元素 | `anyArr[0]` |
| 解构 | `const { a } = anyValue` |
| 泛型实参是 `any` | `Promise<any>` → `await` 后仍是 `any` |

**什么时候可以用 `any`**（克制使用）：

| 场景 | 是否可接受 |
| --- | --- |
| 迁移期临时的类型占位 | 🚧 可以，但必须有 TODO 和期限 |
| 与完全无类型的第三方 JS 互操作 | 🚧 可以，但优先 `unknown` + 守卫 |
| 写类型体操的内部实现 | 🚧 少见，通常能用泛型替代 |
| 日常业务代码 | 🛑 不要 |
| 想「先让它编译过」 | 🛑 这是在制造技术债 |

> 💡 打开 `noImplicitAny`（6.0 随 `strict` 默认开启）能拦住**隐式**的 `any`（如未标注参数），但拦不住你**显式**写下 `any`。后者只能靠 code review 和 lint 规则（`@typescript-eslint/no-explicit-any`）。

{{% /tab %}}

{{% tab header="unknown（安全的 any）" %}}

`unknown` 表示「**我不知道这是什么类型**」。它是 `any` 的安全替代品：可以接收任何值，但**不能直接使用**。

```typescript
function f(u: unknown) {
  return u.toFixed();     // ❌ TS18046: 'u' is of type 'unknown'.
}

function g(u: unknown) {
  if (typeof u === "number") {
    return u.toFixed(2);  // ✅ 收窄之后才能用
  }
  return "not a number";
}
```

`any` vs `unknown` 对照：

| 能力 | `any` | `unknown` |
| --- | --- | --- |
| 接收任意值 | ✅ | ✅ |
| 赋给任意类型 | ✅ | ❌ 需先收窄 |
| 读属性 / 调用方法 | ✅ 不检查 | ❌ `TS18046` |
| 会传染 | ✅ 会 | ❌ 不会 |
| 应该用在哪 | 尽量避免 | **外部输入的首选** 🔥 |

**使用 `unknown` 的标准姿势**：

```typescript
// 所有「外部来的」数据先声明成 unknown，再收窄
async function loadUser(id: string): Promise<User> {
  const raw: unknown = await (await fetch(`/api/users/${id}`)).json();
  if (!isUser(raw)) {                     // 自定义守卫，见 11
    throw new Error("响应格式不符合预期");
  }
  return raw;                             // ✅ 此时已收窄为 User
}

function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null
    && typeof (v as User).name === "string";
}
```

> 🔥 记住这条规则：**凡是从边界进来的数据，类型都是 `unknown` 而不是 `any`**。`any` 静默通过，`unknown` 强迫你处理。详见 [11 运行时校验与边界]({{< relref "11-Runtime-Validation-and-Boundaries.md" >}})。

{{% /tab %}}

{{% tab header="never（空集）" %}}

`never` 是**空类型**——没有任何值属于它。它是所有类型的子类型，可以赋给任何类型；但任何类型（除了 `never`）都不能赋给它。

```typescript
declare const nv: never;
const s: string = nv;      // ✅ never 可以赋给任何类型
const n: number = nv;      // ✅ 也可以

const bad: never = 1;      // ❌ TS2322: Type '1' is not assignable to type 'never'.
```

**`never` 从哪来**：

| 来源 | 例子 |
| --- | --- |
| 永远抛异常的函数 | `function fail(): never { throw new Error() }` |
| 无限循环 | `function loop(): never { while (true) {} }` |
| 不可能的类型运算 | `string & number` → `never` |
| 空联合 | 被 `Exclude` 过滤光的结果 |
| 穷尽检查的 `default` 分支 | 见 [03 收窄]({{< relref "03-Narrowing-and-Type-Guards.md" >}}) 🔥 |

**用法一：标记永不返回的函数**（比 `void` 更精确）

```typescript
function fail(msg: string): never {
  throw new Error(msg);
}

// 对控制流分析有意义：TS 知道这行之后不可达
function pick(v: string | undefined): string {
  if (v === undefined) fail("缺少 v");
  return v;      // ✅ TS 知道 v 已不是 undefined，无需再判断
}
```

**用法二：穷尽性检查**（`never` 最有价值的用途）

```typescript
type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };

function area(sh: Shape): number {
  switch (sh.kind) {
    case "circle": return Math.PI * sh.r ** 2;
    case "square": return sh.s ** 2;
    default:
      const _exhaustive: never = sh;   // ✅ 所有分支都覆盖了，sh 已收窄为 never
      return _exhaustive;
  }
}
```

将来给 `Shape` 加了新成员，这个 `default` 会**立刻报错**：

```typescript
type Shape = { kind: "circle"; r: number }
           | { kind: "square"; s: number }
           | { kind: "triangle"; b: number; h: number };   // 🆕 新增

// ❌ TS2322: Type '{ kind: "triangle"; ... }' is not assignable to type 'never'.
//    ← 编译器强迫你处理新情况，而不是运行时静默返回 undefined
```

> 🔥 这是 TypeScript 最实用的模式之一：**让编译器替你记住「加了新变体要改哪些地方」**。

{{% /tab %}}

{{% tab header="{} / object / Object" %}}

这三者名字像，含义差很远。

| 类型 | 接受 | 拒绝 | 说明 |
| --- | --- | --- | --- |
| `{}` | **除 `null` / `undefined` 外的一切** | `null`、`undefined` | 包括 `string`、`number`！ |
| `object` | 对象、数组、函数、类实例 | 所有**原始类型**、`null`、`undefined` | 想要「非原始」时用它 |
| `Object` | 几乎一切（含原始类型） | `null`、`undefined` | 🛑 基本等于没约束，别用 |

```typescript
const a: {} = "x";            // ✅ 字符串可以！{} 不是「空对象」
const b: object = "x";        // ❌ TS2322: Type 'string' is not assignable to type 'object'.
const c: object = null;       // ❌ TS2322: Type 'null' is not assignable to type 'object'.
const d: {} = null;           // ❌ TS2322: Type 'null' is not assignable to type '{}'.
const e: object = { x: 1 };   // ✅
const f: object = () => {};   // ✅ 函数也是 object
const g: object = [1, 2];     // ✅ 数组也是 object
```

**该用哪个**：

| 你想表达 | 写 |
| --- | --- |
| 任意非空值 | `{}`（少见，容易误解） |
| 任意对象（不要原始类型） | `object` ✅ |
| 任意值 | `unknown` ✅ |
| 具体形状 | `{ id: string }` 这种 ✅ 最常用 |

> ⚠️ 想表达「任意对象」时用 `Record<string, unknown>` 往往比 `object` 更有用——因为拿到之后还能索引访问。

{{% /tab %}}

{{% tab header="速查对照表" %}}

| 类型 | 能接收 | 能赋给谁 | 能读属性 | 会传染 | 一句话 |
| --- | --- | --- | --- | --- | --- |
| `any` | 一切 | 一切 | ✅ | ✅ | 关掉检查 |
| `unknown` | 一切 | 仅 `unknown`/`any` | ❌ | ❌ | 安全的 any 🔥 |
| `never` | 仅 `never` | 一切 | — | — | 空集，表示不可能 |
| `void` | `undefined`/`null` | 仅 `void`/`any` | ❌ | ❌ | 无返回值 |
| `{}` | 非空一切 | 仅 `{}`/`unknown`/`any` | ❌ | ❌ | 不是空对象 ⚠️ |
| `object` | 非原始 | 仅 `object`/`unknown`/`any` | ❌ | ❌ | 非原始值 |
| `null` / `undefined` | 自身 | 依赖 `strictNullChecks` | — | — | 空值 |

**赋值关系（谁是谁的子类型）**：

```text
never  ⊂  所有类型（never 可赋给一切）
一切   ⊂  unknown（一切可赋给 unknown）
any    ↔  一切（双向自由通行，但不安全）
```

{{% /tab %}}

{{< /tabpane >}}

---

## 组合类型：联合与交叉

{{< tabpane text=true persist=disabled >}}

{{% tab header="联合 `|`" %}}

「**或**」——值属于其中一个即可。

```typescript
type Status = "idle" | "loading" | "done";
type Id = string | number;
```

联合的运算律：

| 表达式 | 结果 | 说明 |
| --- | --- | --- |
| `string \| never` | `string` | `never` 是联合的单位元 |
| `string \| any` | `any` | `any` 吸收一切 |
| `string \| unknown` | `unknown` | `unknown` 也吸收一切 |
| `string \| "a"` | `string` | 字面量被父类型吸收 |
| `string \| number` | 保留 | — |

⚠️ **使用联合时必须先收窄**：

```typescript
function f(v: string | number) {
  return v.toUpperCase();   // ❌ TS2339: Property 'toUpperCase' does not exist on type
                            //    'string | number'. Property does not exist on type 'number'.
}

function g(v: string | number) {
  if (typeof v === "string") return v.toUpperCase();   // ✅ 已收窄
  return v.toFixed(2);
}
```

🔗 收窄的完整手段见 [03 收窄与类型守卫]({{< relref "03-Narrowing-and-Type-Guards.md" >}})。

**可辨识联合**（discriminated union）——联合最有价值的形态：

```typescript
type Result =
  | { ok: true;  value: string }
  | { ok: false; error: Error };
```

关键在于每个成员有一个**字面量类型的公共属性**（这里是 `ok`），它让 `switch` 能精确收窄。这是 TypeScript 里建模「互斥状态」的标准做法。🔥

{{% /tab %}}

{{% tab header="交叉 `&`" %}}

「**且**」——同时满足所有成员。

```typescript
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;   // { name: string; age: number }
```

| 表达式 | 结果 | 说明 |
| --- | --- | --- |
| `string & number` | **`never`** | 不可能同时满足 🔥 |
| `{ a: 1 } & { b: 2 }` | `{ a: 1; b: 2 }` | 属性合并 |
| `{ a: 1 } & { a: 2 }` | `{ a: never }` | **同名属性类型取交叉** ⚠️ |
| `T & unknown` | `T` | `unknown` 是交叉的单位元 |
| `T & any` | `any` | `any` 吸收一切 |

⚠️ **同名属性的坑**：

```typescript
type A = { v: string };
type B = { v: number };
type C = A & B;               // 类型上合法，但 v 变成 string & number = never
declare const c: C;
c.v;                          // 类型是 never —— 这个值不可能存在
const bad: C = { v: "x" };    // ❌ TS2322
```

**交叉的主要用途**：

| 用途 | 例子 |
| --- | --- |
| 组合多个「能力」接口 | `Loggable & Serializable` |
| **品牌类型**（模拟名义类型） | `string & { readonly __brand: unique symbol }` |
| 泛型约束叠加 | `<T extends A & B>` |
| 混合类的实例类型 | `Base & Mixin1 & Mixin2` |

```typescript
// 品牌类型：让「字符串」变成不可混淆的「用户 ID」
declare const brand: unique symbol;
type Brand<T, B> = T & { readonly [brand]: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function toUserId(s: string): UserId { return s as UserId; }

declare const uid: UserId;
declare const oid: OrderId;
const x: OrderId = uid;   // ❌ TS2322: 结构不同，无法互赋 🔥
```

> 💭 品牌类型的取舍：换来编译期的强区分，代价是每个入口都要 `as` 一次「铸造」。**在 ID 满天飞的项目里非常值得**，在只有一两种 ID 的项目里是过度设计。

{{% /tab %}}

{{% tab header="属性修饰符与变型" %}}

**`?` 可选属性的两种含义**（受 `exactOptionalPropertyTypes` 影响）：

```typescript
type Opt = { a?: number };   // a 可以「不存在」，或为 number

const x: Opt = {};           // ✅
const y: Opt = { a: 1 };     // ✅
const z: Opt = { a: undefined };   // 默认允许；开启 exactOptionalPropertyTypes 后 ❌
```

| 开关 | `{ a: undefined }` 能否赋给 `{ a?: number }` |
| --- | --- |
| `exactOptionalPropertyTypes: false`（默认） | ✅ 允许 |
| `exactOptionalPropertyTypes: true` | ❌ 报错，两者严格区分 |

**`readonly` 是浅层的** ⚠️：

```typescript
type R = { readonly a: { b: number } };
declare const r: R;
r.a = { b: 2 };      // ❌ TS2540: Cannot assign to 'a' because it is a read-only property.
r.a.b = 2;           // ✅ 合法！readonly 只保护第一层
```

**只读数组**：

```typescript
let mutable: string[] = ["a"];
let ro: readonly string[] = mutable;   // ✅ 可变 -> 只读，允许
let back: string[] = ro;               // ❌ TS4104: The type 'readonly string[]' is
                                       //    'readonly' and cannot be assigned to the mutable type 'string[]'.
ro.push("b");                          // ❌ TS2339: Property 'push' does not exist on type 'readonly string[]'.
```

**变型规则总表**（`strictFunctionTypes` 下实测）：

| 结构 | 变型 | 结论 |
| --- | --- | --- |
| `{ readonly a: T }` | 协变 | 可变 → 只读 ✅ |
| `{ a: T }` | 不变 | 只读 → 可变 ❌ |
| `readonly T[]` | 协变 | 可变数组 → 只读数组 ✅ |
| `T[]` | 不变 | 只读数组 → 可变数组 ❌ `TS4104` |
| 函数**参数** | **逆变** | 参数更宽的函数才能赋值 |
| 函数**返回值** | 协变 | 返回值更窄的函数才能赋值 |
| **方法语法** `f(x): void` | **双变** ⚠️ | 比函数属性宽松，是个历史遗留 |

```typescript
// 逆变：参数类型必须更宽
declare const wide: (x: string | number) => void;
declare const narrow: (x: string) => void;

const a: typeof wide = narrow;   // ❌ TS2322: 参数 'x' 类型不兼容
const b: typeof narrow = wide;   // ✅ 更宽可以赋给更窄

// 方法双变：同样的形状，写成方法就放行了 ⚠️
type FnProp   = { f: (x: string | number) => void };
type FnMethod = { f(x: string | number): void };

const p: FnProp = { f: narrow };     // ❌ TS2322
declare const narM: { f(x: string): void };
const m: FnMethod = narM;            // ✅ 方法双变，放行
```

> ⚠️ **数组是协变的，这是一个已知的不健全（unsound）设计**：
>
> ```typescript
> let strs: string[] = ["a"];
> let anys: (string | number)[] = strs;   // ✅ 编译器允许
> anys.push(123);                          // ✅ 也允许
> strs[1].toUpperCase();                   // 💥 运行时崩溃：123.toUpperCase is not a function
> ```
>
> 这是 TypeScript 团队**刻意保留**的：严格的数组不变性会让日常代码无法忍受。防御手段是**优先用 `readonly T[]` 作为函数参数类型**。

{{% /tab %}}

{{< /tabpane >}}

---

## 类型运算符

| 运算符 | 作用 | 例子 | 结果 |
| --- | --- | --- | --- |
| `keyof T` | 取所有键的联合 | `keyof { a: 1; b: 2 }` | `"a" \| "b"` |
| `typeof v` | 从**值**取类型 | `typeof { a: 1 }` | `{ a: number }` |
| `T[K]` | 索引访问 | `{ a: string }["a"]` | `string` |
| `T[number]` | 取数组元素类型 | `string[][number]` | `string` |
| `T[keyof T]` | 取所有值类型联合 | — | 值联合 |
| `as const` | 阻止拓宽 | `[1, 2] as const` | `readonly [1, 2]` |
| `as T` | 类型断言 | `v as string` | 强制视为 `T` |
| `satisfies T` | 检查但不改类型 | 见下 | 保留窄类型 🔥 |
| `!` | 非空断言 | `el!.id` | 去掉 `null`/`undefined` |

### `keyof` 与索引访问

```typescript
type Person = { name: string; age: number };

type K = keyof Person;              // "name" | "age"
type N = Person["name"];            // string
type V = Person[keyof Person];      // string | number

// 索引访问也能用于数组和元组
type Elem = string[][number];       // string
type First = [number, string][0];   // number

// keyof 也适用于索引签名
type Dict = { [k: string]: number };
type DK = keyof Dict;               // string | number ⚠️ 注意包含 number
```

> ⚠️ `keyof` 带索引签名的对象时结果含 `number`，因为 JS 中 `obj[0]` 与 `obj["0"]` 等价。这是常见困惑点。

**`keyof` + 泛型 = 类型安全的属性访问**：

```typescript
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];      // ✅ 返回类型精确到属性类型
}

const p = { name: "a", age: 1 };
const nm = get(p, "name");   // string
const ag = get(p, "age");    // number
get(p, "nope");              // ❌ TS2345: '"nope"' is not assignable to 'keyof typeof p'
```

### `typeof`：值 → 类型

```typescript
const config = { host: "localhost", port: 8080 };
type Config = typeof config;         // { host: string; port: number }

// 配合 as const 得到精确类型
const config2 = { host: "localhost", port: 8080 } as const;
type Config2 = typeof config2;       // { readonly host: "localhost"; readonly port: 8080 }

// 取函数类型、类类型
declare function fn(a: number): string;
type Fn = typeof fn;                 // (a: number) => string
class C { x = 1 }
type Ctor = typeof C;                // new () => C
```

**`typeof` 有两个身份** ⚠️：

| 写法 | 空间 | 结果 |
| --- | --- | --- |
| `typeof x === "string"` | 值/表达式 | 运行时判断，`boolean` |
| `type T = typeof x` | 类型 | 编译期取类型 |

### `satisfies`：检查但不拓宽 🔥

`satisfies` 是 TS 4.9 引入的运算符，解决了「既要检查、又要保留精确类型」的两难。

```typescript
type Config = Record<string, number | string>;

// 方案 A：类型注解 —— 类型信息丢失
const a: Config = { port: 8080, host: "x" };
a.port.toFixed();      // ❌ TS2339: a.port 是 string | number
const p1: number = a.port;   // ❌

// 方案 B：satisfies —— 检查通过，且保留字面量类型
const b = { port: 8080, host: "x" } satisfies Config;
b.port.toFixed();      // ✅ b.port 是 8080
const p2: 8080 = b.port;     // ✅
```

三者对照：

| 写法 | 做检查 | 拓宽类型 | 报错位置 |
| --- | --- | --- | --- |
| `const x: T = { ... }` | ✅ | ✅ 拓宽为 `T` | 赋值处 |
| `const x = { ... } as T` | ❌ **不检查** | ✅ 断言为 `T` | 基本不报错 🛑 |
| `const x = { ... } satisfies T` | ✅ | ❌ **保留窄类型** | 字面量处 🔥 |

```typescript
// satisfies 的典型用途一：校验配置对象但不丢字面量
const routes = {
  home: "/",
  user: "/users/:id",
} satisfies Record<string, `/${string}`>;

type RouteName = keyof typeof routes;    // "home" | "user"  ✅ 保留了

// 典型用途二：枚举式常量表的键值约束
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
} satisfies Record<string, string | [number, number, number]>;

palette.green.toUpperCase();   // ✅ 仍是 string，不是联合类型
```

> 🛑 **`as` 与 `satisfies` 的关键区别**：`as` 是**许愿**，编译器不检查你是否真的对得上；`satisfies` 是**检查**，对不上就报错。
>
> ```typescript
> const wrong = { port: "8080" } as Record<string, number>;   // ✅ 编译通过，运行时隐患
> const safe  = { port: "8080" } satisfies Record<string, number>;
> //            ❌ TS2322: Type 'string' is not assignable to type 'number'.
> ```
>
> 能用 `satisfies` 的地方不要用 `as`。💭

### 断言：`as` 与非空 `!`

```typescript
declare const v: string | number;

const s = v as string;        // 断言
const s2 = v as unknown as string;   // 双重断言（绕过「不够像」的检查）
const s3 = (v as any) as string;     // 🛑 别这样

declare const el: HTMLElement | null;
el!.id;                       // 非空断言：去掉 null
```

| 手段 | 检查强度 | 何时用 |
| --- | --- | --- |
| `as T` | 弱（只需类型「够像」） | 你比编译器知道得更多，且有依据 |
| `as unknown as T` | 无 | 🚧 极少，通常说明类型设计有问题 |
| `as any as T` | 无 | 🛑 不要 |
| `!` | 无 | 确定非空时（如刚判过、或框架保证） |
| `satisfies` | 强 | **优先选它** 🔥 |

> 💡 判断标准：**写下 `as` 的时候，你能不能说出「为什么这个断言一定成立」？** 说不出来就是在埋雷。

---

## 元组

元组是「长度和每个位置的类型都固定」的数组。

```typescript
type Pair = [number, string];

const a: Pair = [1, "x"];      // ✅
const b: Pair = ["x", 1];      // ❌ TS2322
const c: Pair = [1];           // ❌ TS2322: Source has 1 element(s), but target requires 2.
const d: Pair = [1, "x", 3];   // ❌ TS2322
```

**常用形态**：

```typescript
type Labeled   = [x: number, y: number];       // 带标签（纯文档作用）
type Optional  = [id: number, name?: string];  // 可选元素（必须在末尾）
type Variadic  = [first: string, ...rest: number[]];   // 剩余元素
type ReadonlyT = readonly [number, string];    // 只读元组
```

```typescript
// 变长元组：泛型拼接
type Concat<A extends unknown[], B extends unknown[]> = [...A, ...B];
type C = Concat<[1, 2], [3]>;      // [1, 2, 3]

// 元组 -> 数组
type Pair2 = [number, string];
let arr: (number | string)[] = null as unknown as Pair2;   // ✅ 元组可赋给数组
let back: Pair2 = null as unknown as (number | string)[];  // ❌ TS2322: 数组不能赋给元组
```

**元组的实战价值**——让「多返回值」有名字：

```typescript
function useState<T>(init: T): [T, (v: T) => void] {
  let v = init;
  return [v, (nv: T) => { v = nv; }];
}

const [count, setCount] = useState(0);   // count: number, setCount: (v: number) => void
```

> ⚠️ 元组的「长度」在运行时**不存在**。`[1, "x"]` 就是普通数组，`as const` / 元组类型都只是编译期约束。想验证长度必须自己写运行时检查。

---

## 内置工具类型全表

这些是 TypeScript 自带的类型层函数，定义在 `lib.es5.d.ts` 等文件里。**理解它们的实现**比记住名字更重要——下一节会逐个展开。

{{< tabpane text=true persist=disabled >}}

{{% tab header="属性变换" %}}

| 工具类型 | 作用 | 例子 → 结果 |
| --- | --- | --- |
| `Partial<T>` | 所有属性变可选 | `Partial<{a:1}>` → `{a?:1}` |
| `Required<T>` | 所有属性变必选 | `Required<{a?:1}>` → `{a:1}` |
| `Readonly<T>` | 所有属性变只读（浅层） | `Readonly<{a:1}>` → `{readonly a:1}` |
| `Record<K, V>` | 构造键值对象 | `Record<"a"\|"b", number>` → `{a:number;b:number}` |
| `Pick<T, K>` | 挑选若干属性 | `Pick<{a:1;b:2}, "a">` → `{a:1}` |
| `Omit<T, K>` | 排除若干属性 | `Omit<{a:1;b:2}, "a">` → `{b:2}` |

```typescript
interface User { id: number; name: string; email: string }

type UserPreview = Pick<User, "id" | "name">;      // 只要这两个
type UserDraft   = Omit<User, "id">;               // 除 id 外都要
type UserPatch   = Partial<User>;                  // PATCH 请求体
type UserMap     = Record<string, User>;           // 字典
```

> ⚠️ `Omit` **不检查键是否存在**：`Omit<User, "typo">` 不报错，只是什么都不排除。想要严格检查用 `Pick` 或自定义的 `StrictOmit`（见 [06]({{< relref "06-Type-Level-Programming-Recipes.md" >}})）。

{{% /tab %}}

{{% tab header="联合操作" %}}

| 工具类型 | 作用 | 例子 → 结果 |
| --- | --- | --- |
| `Exclude<T, U>` | 从 `T` 中**减去**可赋给 `U` 的成员 | `Exclude<"a"\|"b", "a">` → `"b"` |
| `Extract<T, U>` | 从 `T` 中**保留**可赋给 `U` 的成员 | `Extract<"a"\|1, string>` → `"a"` |
| `NonNullable<T>` | 去掉 `null` 和 `undefined` | `NonNullable<string\|null>` → `string` |

```typescript
type Status = "idle" | "loading" | "done" | "error";
type FinalStatus = Exclude<Status, "idle" | "loading">;   // "done" | "error"
type ErrStatus   = Extract<Status, "error">;              // "error"

// 可辨识联合的实用模式：按 kind 取出某个成员
type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };
type Circle = Extract<Shape, { kind: "circle" }>;         // { kind: "circle"; r: number } 🔥
```

> 💡 `Extract<Union, { kind: "x" }>` 是**从可辨识联合中精确取一个分支**的标准手法，配合 `Omit` 还能改写分支。

{{% /tab %}}

{{% tab header="函数与类" %}}

| 工具类型 | 作用 | 例子 → 结果 |
| --- | --- | --- |
| `Parameters<F>` | 取参数元组 | `Parameters<(a:1,b:2)=>void>` → `[a:1,b:2]` |
| `ReturnType<F>` | 取返回值类型 | `ReturnType<()=>string>` → `string` |
| `ConstructorParameters<C>` | 取构造函数参数 | `[string, number]` |
| `InstanceType<C>` | 取实例类型 | `InstanceType<typeof User>` → `User` |
| `ThisParameterType<F>` | 取 `this` 类型 | — |
| `OmitThisParameter<F>` | 去掉 `this` 参数 | — |
| `ThisType<T>` | 标记方法中的 `this` | 配合 `noImplicitThis` |
| `Awaited<T>` | 递归解包 Promise | `Awaited<Promise<Promise<number>>>` → `number` |

```typescript
declare function createUser(name: string, age: number): User;

type Args = Parameters<typeof createUser>;   // [name: string, age: number]
type Ret  = ReturnType<typeof createUser>;   // User

class Service { constructor(private url: string) {} }
type SvcArgs = ConstructorParameters<typeof Service>;   // [url: string]
type Svc     = InstanceType<typeof Service>;            // Service

// 从任意函数提取类型——避免重复定义
async function fetchUser() { return { id: 1, name: "a" }; }
type FetchedUser = Awaited<ReturnType<typeof fetchUser>>;   // { id: number; name: string } 🔥
```

> ⚠️ `ReturnType` / `Parameters` 对**重载函数**只取**最后一个**重载签名。重载函数要用 `Parameters` 得注意这一点。

{{% /tab %}}

{{% tab header="字符串（TS 4.1+）" %}}

| 工具类型 | 例子 → 结果 |
| --- | --- |
| `Uppercase<S>` | `Uppercase<"ab">` → `"AB"` |
| `Lowercase<S>` | `Lowercase<"AB">` → `"ab"` |
| `Capitalize<S>` | `Capitalize<"ab">` → `"Ab"` |
| `Uncapitalize<S>` | `Uncapitalize<"Ab">` → `"ab"` |

```typescript
// 最常用：从事件名生成 handler 名
type Event = "click" | "focus";
type HandlerName = `on${Capitalize<Event>}`;   // "onClick" | "onFocus"

// 生成 getter 类型（键重映射）
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
type PersonGetters = Getters<{ name: string; age: number }>;
// { getName: () => string; getAge: () => number }
```

> 注意 `Capitalize<string & K>` 里的 `string & K`：`K` 可能是 `string | number | symbol`，而 `Capitalize` 只接受 `string`，交叉一下做窄化。

{{% /tab %}}

{{% tab header="其它" %}}

| 工具类型 | 作用 |
| --- | --- |
| `NoInfer<T>` 🆕 | 阻止某个位置参与推断（TS 5.4+），见 [05]({{< relref "05-Generics-and-Inference.md" >}}) |
| `Uppercase` 家族 | 见「字符串」标签页 |
| `PropertyKey` | `string \| number \| symbol` |
| `Awaited<T>` | 见「函数与类」标签页 |

```typescript
// NoInfer：让第二个参数不参与 T 的推断
function createFSM<T extends string>(
  states: T[],
  initial: NoInfer<T>,      // 不参与推断，只能从 states 推
) { return { states, initial }; }

createFSM(["idle", "done"], "idle");   // ✅ T = "idle" | "done"
createFSM(["idle", "done"], "typo");   // ❌ TS2345: '"typo"' is not assignable to '"idle" | "done"'
```

{{% /tab %}}

{{< /tabpane >}}

---

## 从值到类型的四种手法

实际编码中最常用的「类型复用」技巧：

| 手法 | 写法 | 得到 |
| --- | --- | --- |
| 取整个对象类型 | `typeof obj` | 对象类型 |
| 取对象的某个属性类型 | `typeof obj[K]`（`K` 为字面量） | 属性类型 |
| 取数组元素类型 | `(typeof arr)[number]` | 元素类型 🔥 |
| 取函数返回类型 | `ReturnType<typeof fn>` | 返回值类型 |

```typescript
const ROLES = ["admin", "user", "guest"] as const;

type Role = (typeof ROLES)[number];      // "admin" | "user" | "guest"  🔥

const CONFIG = {
  api: { timeout: 5000, retries: 3 },
  ui: { theme: "dark" },
} as const;

type ApiConfig = typeof CONFIG.api;      // { readonly timeout: 5000; readonly retries: 3 }
type Theme = typeof CONFIG.ui.theme;     // "dark"
```

> 🔥 `(typeof ARRAY)[number]` 是**从常量数组推导联合类型**的标准写法，比手写联合更不容易漏。反过来，别忘了 `as const`——没有它 `ROLES` 会被推导为 `string[]`，`[number]` 就只是 `string`。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 用包装对象类型 | `String` / `Number` | 用小写 `string` / `number` |
| 以为 `{}` 是空对象 | `const x: {} = "a"` 竟然合法 | 用 `object` 或具体形状 |
| 用 `Object` 当约束 | 什么都没约束住 | 用 `object` / `unknown` |
| `as` 当转换用 | 运行时崩溃 | 用 `satisfies` 或守卫 |
| 联合上直接调方法 | `TS2339` | 先收窄 |
| `as const` 忘了写 | 推断成 `string` 而非字面量联合 | 常量表加 `as const` |
| 以为 `readonly` 是深层的 | 改内层属性竟然合法 | 深层只读要自己写 `DeepReadonly` |
| 数组协变 | 运行时类型污染 | 参数用 `readonly T[]` |
| 交叉同名属性 | 属性变 `never` | 避免同名交叉，或显式 Omit |
| 索引签名 `keyof` | 结果含 `number` | 用 `string & keyof T` 窄化 |
