+++
title = "03 收窄与类型守卫"
weight = 103
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "控制流分析全表、typeof 返回值映射、自定义类型守卫、穷尽性检查与收窄失效的原因"
isCJKLanguage = true
draft = false
+++

# 03 收窄与类型守卫

**收窄**（narrowing）是 TypeScript 最强大的能力：你写普通的 `if` / `switch`，编译器自动把宽类型缩到窄类型。

```typescript
function f(v: string | number) {
  if (typeof v === "string") {
    return v.toUpperCase();   // v 已自动变成 string
  }
  return v.toFixed(2);        // v 已自动变成 number
}
```

这一页讲清楚：**什么情况下会收窄、什么情况下会失效**。后者才是真正花时间的地方。

> 所有 `❌ TSxxxx` 均为 TS 6.0.3 实测。

---

## 控制流分析：收窄手段全表

{{< tabpane text=true persist=disabled >}}

{{% tab header="typeof（原始类型）" %}}

`typeof` 能区分原始类型和函数，是收窄 `unknown` 的首选手段。

| `typeof v` 的结果 | 收窄为 | 备注 |
| --- | --- | --- |
| `"string"` | `string` | — |
| `"number"` | `number` | ⚠️ `NaN` 也是 `number` |
| `"bigint"` | `bigint` | — |
| `"boolean"` | `boolean` | — |
| `"symbol"` | `symbol` | — |
| `"undefined"` | `undefined` | — |
| `"object"` | `object \| null` | ⚠️ **`null` 也走这里！** |
| `"function"` | `Function` | — |

```typescript
function describe(v: unknown): string {
  switch (typeof v) {
    case "string":    return `字符串: ${v}`;
    case "number":    return `数字: ${v}`;
    case "bigint":    return `大整数: ${v}`;
    case "boolean":   return `布尔: ${v}`;
    case "symbol":    return `符号: ${v.toString()}`;
    case "undefined": return "未定义";
    case "object":    return v === null ? "null" : "对象";   // ⚠️ 必须再判 null
    case "function":  return `函数: ${v.name}`;
    default:          return "不可能到这里";
  }
}
```

> 🛑 **`typeof null === "object"` 是 JavaScript 的历史 bug**，TypeScript 忠实地保留了它。所以：
>
> ```typescript
> function f(v: string | null) {
>   if (typeof v === "object") {
>     return "这里能拿到 null";    // ⚠️ 编译器认为 v 可能是 null
>   }
>   return v;                      // 这里 v 是 string（null 被上面的分支拿走了）
> }
> ```
>
> `typeof v === "object"` **不会**排除 `null`。判定非空对象要写：
>
> ```typescript
> if (typeof v === "object" && v !== null) { /* 现在 v 是 object */ }
> ```

**`typeof` 判不出数组、Date、类实例**——它们的结果都是 `"object"`：

| 想判断 | 别用 `typeof` | 用 |
| --- | --- | --- |
| 数组 | `typeof v === "array"` 🛑 永远 false | `Array.isArray(v)` |
| Date | `typeof v === "Date"` 🛑 | `v instanceof Date` |
| 类实例 | `typeof v === "MyClass"` 🛑 | `v instanceof MyClass` |
| 普通对象 | `typeof v === "object"` ⚠️ 不够 | `v !== null && typeof v === "object" && !Array.isArray(v)` |

{{% /tab %}}

{{% tab header="instanceof / in" %}}

**`instanceof`**——收窄为某个类：

```typescript
function fmt(v: Date | string) {
  if (v instanceof Date) return v.toISOString();   // v: Date
  return v.toUpperCase();                          // v: string
}
```

> ⚠️ `instanceof` 用原型链判断，**跨 realm（如 iframe、Worker）会失效**——不同 realm 的同名类原型不同。跨 realm 数据用 `Object.prototype.toString.call(v)` 或鸭子类型判断。
>
> ⚠️ 接口（`interface`）在运行时不存在，所以 `x instanceof SomeInterface` **不能编译**。接口只能靠自定义守卫。

**`in`**——按属性存在性收窄：

```typescript
type A = { a: number };
type B = { b: string };

function f(v: A | B) {
  if ("a" in v) return v.a;   // v: A
  return v.b;                 // v: B
}
```

`in` 对**可选属性**的行为要小心：

```typescript
type P = { a?: number; b?: string };

function g(p: P) {
  if ("a" in p) {
    return p.a;    // 类型是 number | undefined ⚠️ 因为 a 本身可选
  }
  return p.b;
}
```

> 💡 `in` 判断的是「属性是否存在」，不是「值是否为 undefined」。`{ a: undefined }` 里 `"a" in p` 为 **true**。

{{% /tab %}}

{{% tab header="真值 / 相等 / 判别属性" %}}

**真值收窄**（truthiness）——最简洁，但覆盖面容易被误解：

```typescript
function f(v: string | null | undefined) {
  if (v) return v.length;   // 排除了 null / undefined / ""
  return 0;
}
```

| 表达式 | 排除掉的假值 |
| --- | --- |
| `if (v)` | `false`、`0`、`-0`、`0n`、`""`、`null`、`undefined`、`NaN` |
| `if (!v)` | 反向：保留上述假值 |

> ⚠️ **`if (v)` 会连空字符串和 `0` 一起排除**。如果 `0` 是合法值，必须写显式比较：
>
> ```typescript
> function bad(n: number | null) {
>   if (n) return n * 2;   // 🛑 n = 0 时会走 else！
>   return 0;
> }
>
> function good(n: number | null) {
>   if (n !== null) return n * 2;   // ✅ 只排除 null
>   return 0;
> }
> ```

**相等性收窄**：

```typescript
function f(a: string | number, b: string | boolean) {
  if (a === b) {
    return a.toUpperCase();   // a 和 b 都收窄为 string（唯一的公共成员）
  }
  return "";
}
```

**可辨识联合收窄**（`switch` 最常用的形态）🔥：

```typescript
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number }
  | { kind: "rect"; w: number; h: number };

function area(sh: Shape): number {
  switch (sh.kind) {
    case "circle": return Math.PI * sh.r ** 2;
    case "square": return sh.s ** 2;
    case "rect":   return sh.w * sh.h;
  }
}
```

注意这里**没写 `default`**。如果 `Shape` 新增了成员，函数会因「并非所有代码路径都返回值」而报错（`TS2366`）——这本身就是一种穷尽性保护。

配合 `never` 可以做得更明确：

```typescript
function area2(sh: Shape): number {
  switch (sh.kind) {
    case "circle": return Math.PI * sh.r ** 2;
    case "square": return sh.s ** 2;
    case "rect":   return sh.w * sh.h;
    default:
      const _exhaustive: never = sh;   // ✅ 所有分支覆盖后，sh 是 never
      return _exhaustive;
  }
}

// 新增成员后立刻报错：
// ❌ TS2322: Type '{ kind: "triangle"; ... }' is not assignable to type 'never'.
```

> 🔥 **两种穷尽性写法怎么选**：
>
> | 写法 | 加新成员时的表现 | 适合 |
> | --- | --- | --- |
> | 不写 `default` + 有返回值 | `TS2366` 函数缺少返回 | 简单函数 |
> | `default` + `never` 赋值 | `TS2322` 明确指向未处理的分支 | 复杂逻辑，**推荐** |

{{% /tab %}}

{{% tab header="自定义类型守卫" %}}

当内置手段不够时，用**类型谓词**（type predicate）自己声明收窄规则。

```typescript
function isString(v: unknown): v is string {
  return typeof v === "string";
}

function f(v: unknown) {
  if (isString(v)) {
    return v.toUpperCase();   // ✅ v 收窄为 string
  }
  return null;
}
```

**写法要点**：

| 要点 | 说明 |
| --- | --- |
| 返回类型写 `v is T` | 而不是 `boolean` 🔥 |
| `v` 必须是**参数名** | 不能是 `obj.prop is T` 这种表达式 |
| 参数通常是 `unknown` | 便于在任何地方使用 |
| 可以用于箭头函数 | `const isStr = (v: unknown): v is string => ...` |

```typescript
// ✅ 箭头函数也可以
const isNumber = (v: unknown): v is number => typeof v === "number";

// ❌ 不能对属性写谓词——语法直接不通过
function bad(o: { a: unknown }): o.a is string { return typeof o.a === "string"; }
//                              ~~~~~~~~~~~~~~~~~ error TS1144: '{' or ';' expected.
//                                                   （谓词位置只接受标识符，不接受属性访问）
```

**组合多个守卫**：

```typescript
type User = { id: number; name: string };

function isUser(v: unknown): v is User {
  return (
    typeof v === "object" && v !== null &&
    typeof (v as User).id === "number" &&
    typeof (v as User).name === "string"
  );
}

// 数组守卫
function isUserArray(v: unknown): v is User[] {
  return Array.isArray(v) && v.every(isUser);
}
```

> 🛑 **守卫是可以撒谎的，编译器不会检查**：
>
> ```typescript
> function isNum(v: unknown): v is number {
>   return typeof v === "string";   // ✅ 编译通过，但完全错误
> }
>
> function f(v: unknown) {
>   if (isNum(v)) {
>     return v.toFixed(2);   // 编译通过；v 若是字符串，运行时崩溃
>   }
> }
> ```
>
> 编译器**完全信任**你的谓词。所以守卫里必须真的做运行时检查。这也是为什么 [11 运行时校验]({{< relref "11-Runtime-Validation-and-Boundaries.md" >}}) 建议用 schema 库自动生成守卫，而不是手写。💭

{{% /tab %}}

{{% tab header="断言函数" %}}

**断言函数**（assertion function）用于「不满足就抛异常」的场景，比守卫更适合做前置条件检查。

```typescript
function assertIsString(v: unknown): asserts v is string {
  if (typeof v !== "string") {
    throw new Error("期望 string");
  }
}

function f(v: unknown) {
  assertIsString(v);
  return v.toUpperCase();   // ✅ 调用之后 v 就是 string
}
```

语法对比：

| 形式 | 返回类型写法 | 调用后的效果 |
| --- | --- | --- |
| 类型谓词 | `v is T` | 在 `if` 为真的分支里收窄 |
| 断言函数 | `asserts v is T` | **调用之后的代码**都收窄 🔥 |
| 无条件断言 | `asserts v` | 断言为真值（去假值） |

```typescript
// 无条件的真值断言
function assert(v: unknown): asserts v {
  if (!v) throw new Error("断言失败");
}

function g(s: string | null) {
  assert(s);
  return s.toUpperCase();   // ✅ 去掉了 null
}
```

**泛型断言函数**（很实用）：

```typescript
function assertDefined<T>(v: T | null | undefined): asserts v is T {
  if (v === null || v === undefined) {
    throw new Error("值不能为空");
  }
}

function h(v: string | undefined) {
  assertDefined(v);
  return v.toUpperCase();   // ✅ 去掉了 undefined
}
```

> ⚠️ **断言函数的两个限制**：
>
> 1. 必须**有显式类型标注**的声明（不能靠推断）——所以不能用箭头函数简写形式直接赋值给无标注的变量。
> 2. 它依赖「抛异常」来收窄，因此**在 try 块之外**调用才有效；跨函数边界（回调内）不保证收窄。

{{% /tab %}}

{{% tab header="推断的类型谓词 🆕" %}}

TS 5.5 起，简单的**内联**过滤函数能被**自动推断**出类型谓词，不需要手写 `x is T`。

```typescript
const arr = [1, "a", null, undefined, 2];

// 5.5 之前：结果是 (string | number | null | undefined)[]，null 没被去掉
// 5.5+：自动推断为 (x) => x is string | number
const filtered = arr.filter((x) => x !== null && x !== undefined);

const total = filtered.reduce<number>(
  (sum, x) => sum + (typeof x === "number" ? x : 0),
  0,
);
```

**能推断的条件**（必须足够简单）：

| 条件 | 说明 |
| --- | --- |
| 函数体是**单个 return 表达式** | 不能有复杂语句 |
| 参数**没有显式类型标注** | 有标注则按标注走 |
| 返回布尔表达式 | 且该表达式本身能产生收窄 |

```typescript
// ✅ 会被推断为 x is number
const a = arr.filter((x) => typeof x === "number");

// ❌ 有显式标注 -> 结果就是 boolean，不收窄
const b = arr.filter((x: unknown) => typeof x === "number");

// ❌ 多语句函数体 -> 不推断
const c = arr.filter((x) => {
  const ok = typeof x === "number";
  return ok;
});

// ✅ 想要收窄就手写谓词
const d = arr.filter((x): x is number => {
  const ok = typeof x === "number";
  return ok;
});
```

> 💡 判断口径很简单：**`.filter()` 之后类型没变窄，就手写 `: x is T`**。这比猜「能不能推断」快得多。

{{% /tab %}}

{{< /tabpane >}}

---

## 收窄为什么会失效

这是本页最有价值的部分。收窄只在**编译器能追踪的范围内**有效。

{{< tabpane text=true persist=disabled >}}

{{% tab header="闭包与回调" %}}

**核心规则**：收窄信息在**函数边界**处会丢失，因为编译器无法确定函数什么时候被调用、调用时变量变成了什么。

```typescript
function bad(v: string | null) {
  if (v !== null) {
    // 🛑 回调可能在任意时刻执行，编译器不敢保证 v 仍非空
    setTimeout(() => v.toUpperCase(), 0);
    //                ~ error TS18047: 'v' is possibly 'null'.
  }
}
```

**三种修复方式**：

```typescript
// 方案 1：提前取出到 const（推荐）🔥
function fix1(v: string | null) {
  if (v !== null) {
    const s = v;                        // s 是 string，且永不再变
    setTimeout(() => s.toUpperCase(), 0);   // ✅
  }
}

// 方案 2：用参数传入
function fix2(v: string | null) {
  if (v !== null) {
    const run = (s: string) => s.toUpperCase();
    setTimeout(() => run(v), 0);        // ✅ 实参位置已收窄
  }
}

// 方案 3：非空断言（下策）
function fix3(v: string | null) {
  if (v !== null) {
    setTimeout(() => v!.toUpperCase(), 0);   // ✅ 但绕过了检查
  }
}
```

> 💡 **方案 1 是几乎总是正确的选择**。把已收窄的值存进 `const`，语义立刻从「这个变量可能变」变成「这个值确定是 string」，编译器和你都轻松。

**TS 5.4+ 的改进**：对**未被重新赋值**的 `let` / 参数，收窄现在能保留到闭包内。

```typescript
function improved(v: string | null) {
  let s = v;
  if (s !== null) {
    return () => s.toUpperCase();   // ✅ 5.4+ 合法：s 之后从未被赋值
  }
  return () => "";
}

function stillBad(v: string | null) {
  let s = v;
  if (s !== null) {
    return () => {
      s = null;                     // ⚠️ 有赋值，收窄作废
      return s.toUpperCase();
      //     ~ error TS18047: 's' is possibly 'null'.
    };
  }
  return () => "";
}
```

判定标准：

| 变量在收窄后… | 闭包内是否保留收窄 |
| --- | --- |
| 从未再被赋值 | ✅ 保留（5.4+） |
| 在任意位置被赋值过 | ❌ 失效 |

{{% /tab %}}

{{% tab header="let 与别名" %}}

**`let` 会被重新赋值**，所以收窄更脆弱：

```typescript
function f(v: string | null | undefined) {
  if (!v) return;
  v = maybeGet();          // ⚠️ 重新赋值，之前的收窄作废
  return v.toUpperCase();  // ❌ TS18048: 'v' is possibly 'undefined'.
}
```

**别名（aliasing）也会破坏收窄**：

```typescript
type State = { value: string | null };

function bad(s: State) {
  if (s.value !== null) {
    mutate(s);                    // ⚠️ 编译器不知道这个函数做了什么
    return s.value.toUpperCase(); // ❌ TS18047: 's.value' is possibly 'null'.
  }
  return "";
}

function good(s: State) {
  const v = s.value;              // ✅ 先取出到局部 const
  if (v !== null) {
    mutate(s);
    return v.toUpperCase();       // ✅ v 不受 s 变化影响
  }
  return "";
}
```

> 💡 记住这个模式：**属性访问的收窄几乎总是不稳定的，先存到局部 `const`**。

{{% /tab %}}

{{% tab header="其它失效场景" %}}

| 场景 | 症状 | 处理 |
| --- | --- | --- |
| 复杂表达式被重复求值 | 收窄不适用于第二次求值 | 存到 `const` |
| 索引访问 | `obj[key]` 每次访问都重新判 | 存到 `const` |
| 解构后再判断 | 解构出的变量是独立的 | 直接判断解构后的变量 |
| 泛型参数 | 泛型 `T` 不收窄 | 用 `T & {}` 或收窄到具体类型 |
| `try`/`catch` 跨块 | 收窄不跨 catch | 块内重新判断 |
| 断言函数在回调外调用 | 回调内不收窄 | 把值作参数传入 |

```typescript
// 索引访问：每次 obj[key] 都是新求值
function f(obj: Record<string, string | null>, key: string) {
  if (obj[key] !== null) {
    return obj[key].toUpperCase();   // ❌ TS18047: 'obj[key]' is possibly 'null'.
  }
  return "";
}

function fixed(obj: Record<string, string | null>, key: string) {
  const v = obj[key];                // ✅ 一次求值，存起来
  if (v !== null) return v.toUpperCase();
  return "";
}
```

```typescript
// 泛型参数不收窄
function g<T>(v: T | null) {
  if (v !== null) {
    return v;      // 类型是 T & {} —— 不是 T ⚠️
  }
  return null;
}

// 需要精确类型时改用泛型约束
function h<T>(v: T | null): T | null {
  return v ?? null;
}
```

{{% /tab %}}

{{< /tabpane >}}

---

## `as` vs `satisfies` vs 守卫

三者都「告诉编译器信息」，但行为完全不同。

| 手段 | 运行时检查 | 编译器检查 | 适用场景 |
| --- | --- | --- | --- |
| `as T` | ❌ 无 | ❌ 无（只要够像） | 你确定、且无法用其它方式表达 |
| `satisfies T` | ❌ 无 | ✅ **有** | 校验字面量又保留窄类型 🔥 |
| `x is T` 守卫 | ✅ 有 | ❌ 不检查你写对没 | 外部数据的运行时校验 🔥 |
| `asserts x is T` | ✅ 有 | ❌ 同上 | 前置条件断言的场景 |
| 类型注解 `: T` | ❌ 无 | ✅ 有（但会拓宽） | 声明变量/参数类型 |

```typescript
declare const raw: unknown;

// ❌ 最危险：什么都不检查，运行时可能炸
const u1 = raw as User;

// ✅ 正确：运行时真的检查了
function isUser(v: unknown): v is User { /* 真实检查 */ }
let u2: User;
if (isUser(raw)) { u2 = raw; } else { throw new Error("bad data"); }

// ✅ 校验字面量：编译期检查，且不拓宽
const cfg = { retries: 3, timeout: 5000 } satisfies Record<string, number>;
```

**选择顺序**（从优到劣）🔥：

1. **能让编译器自己推断** → 什么都不写
2. **需要校验字面量** → `satisfies`
3. **外部数据** → 运行时 schema 校验（Zod 等）或手写守卫
4. **确定比编译器知道得多** → `as`（要能说出理由）
5. 🛑 `as any` / `as unknown as T` / `@ts-ignore`

---

## 实战模式

### 判别联合的状态机

```typescript
type FetchState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function render(state: FetchState<string>): string {
  switch (state.status) {
    case "idle":    return "等待中";
    case "loading": return "加载中";
    case "success": return state.data;      // ✅ data 只在 success 分支存在 🔥
    case "error":   return state.error.message;
    default: {
      const _exhaustive: never = state;
      return _exhaustive;
    }
  }
}
```

这个模式的威力：**`data` 只能在 `status === "success"` 时访问**，从根本上排除了「先访问 `data` 再判空」的整类 bug。

### 解析输入的边界函数

```typescript
type ParsedInput = { type: "text"; value: string } | { type: "number"; value: number };

function parseInput(raw: unknown): ParsedInput {
  if (typeof raw === "string") {
    return { type: "text", value: raw };
  }
  if (typeof raw === "number" && Number.isFinite(raw)) {
    return { type: "number", value: raw };
  }
  throw new TypeError(`无法解析输入: ${String(raw)}`);
}
```

### 带默认值的可选参数

```typescript
// 🛑 用真值判断会吞掉 0 和 ""
function bad(n?: number) {
  return n ? n * 2 : 100;   // n = 0 时返回 100！
}

// ✅ 显式判 undefined
function good(n?: number) {
  return n !== undefined ? n * 2 : 100;
}

// ✅ 或用 ?? （只对 null/undefined 生效）
function better(n?: number) {
  return (n ?? 100) * 2;
}
```

| 运算符 | 只对 `null` / `undefined` 生效 | 对 `0` / `""` / `false` 也生效 |
| --- | --- | --- |
| `??` | ✅ | ❌ 保留它们 🔥 |
| `\|\|` | ❌ | ✅ 会替换掉 |
| `?.` | ✅ | — |

### 判别联合的「更新一个分支」

```typescript
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number };

// 用 Extract 精确取分支，再改属性
type Circle = Extract<Shape, { kind: "circle" }>;

function scaleCircle(sh: Circle, k: number): Circle {
  return { ...sh, r: sh.r * k };   // ✅ kind 保留为 "circle"
}
```

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 用 `typeof` 判数组 | 永远 `false` | `Array.isArray(v)` |
| `typeof null` 是 `"object"` | `null` 混进对象分支 | 加 `v !== null` |
| `if (v)` 吞掉 `0` / `""` | 合法值走了错误分支 | 用 `v !== null` 或 `v !== undefined` |
| 回调里用收窄过的变量 | `TS18047` / `TS18048` | 先存 `const` |
| 收窄后重新赋值 | 收窄作废 | 别在收窄后改该变量 |
| 用 `in` 判可选属性 | 结果含 `undefined` | 判完再判 `!== undefined` |
| 期望 `.filter()` 自动收窄 | 类型没变 | 手写 `: x is T` |
| 以为守卫被检查 | 谓词撒谎也不报错 | 守卫里必须真实检查 |
| `instanceof` 判接口 | 编译不过 | 接口用自定义守卫 |
| 跨 realm 用 `instanceof` | 运行时判错 | 用 `Object.prototype.toString` |
