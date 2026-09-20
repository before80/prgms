+++
title = "04 函数、对象与类"
weight = 104
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "函数重载与 this、函数变型表、对象类型与索引签名、类的访问控制与 #私有字段"
isCJKLanguage = true
draft = false
+++

# 04 函数、对象与类

本页是日常编码里查得最频繁的一页：**函数类型怎么写、类成员怎么标、对象形状怎么约束**。

> 所有 `❌ TSxxxx` 均为 TS 6.0.3 实测。

---

## 函数类型

{{< tabpane text=true persist=disabled >}}

{{% tab header="基本写法" %}}

```typescript
// 函数声明
function add(a: number, b: number): number { return a + b; }

// 函数表达式（返回值可推断，通常省略）
const sub = (a: number, b: number) => a - b;

// 箭头函数的返回类型用括号包住参数列表
const mul = (a: number, b: number): number => a * b;

// 类型别名形式的函数类型
type BinOp = (a: number, b: number) => number;
const div: BinOp = (a, b) => a / b;      // ✅ 参数类型自动继承，无需重复标 🔥

// 对象里的方法
interface Calc { add(a: number, b: number): number }
```

| 参数形态 | 写法 | 说明 |
| --- | --- | --- |
| 必需 | `(a: number)` | — |
| 可选 | `(a?: number)` | 必须在必需参数之后 |
| 默认值 | `(a = 10)` | 类型从默认值推断；隐式可选 |
| 剩余 | `(...rest: number[])` | 永远是数组类型 |
| 元组剩余 | `(...args: [string, number])` | 参数个数固定 🔥 |
| `this` | `(this: Window)` | 假参数，不占实参位置 |

```typescript
// 用元组剩余参数约束参数个数
function log(...args: [level: string, msg: string]) { /* ... */ }
log("info", "ok");        // ✅
log("info");              // ❌ TS2554: Expected 2 arguments, but got 1.
log("info", "ok", "x");   // ❌ TS2554: Expected 2 arguments, but got 3.

// 默认值会自动变可选
function greet(name: string, greeting = "Hello") {
  return `${greeting}, ${name}`;
}
greet("A");               // ✅
```

> ⚠️ **可选参数与默认值在调用点上等价**，但在类型层面有细微差别：`a?: number` 表示「可以传 `undefined`」，`a = 10` 表示「有默认值」。开启 `exactOptionalPropertyTypes` 时这个区别才会显现（更多见 [08]({{< relref "08-tsconfig-Reference.md" >}})）。

{{% /tab %}}

{{% tab header="函数重载" %}}

TypeScript 的重载是**类型层面的**：写多个**签名**，最后一个**实现**。

```typescript
// 重载签名（对外可见）
function parse(input: string): string[];
function parse(input: number): number[];
// 实现签名（对外不可见）
function parse(input: string | number): string[] | number[] {
  return typeof input === "string" ? input.split("") : [input];
}

const a = parse("x");   // string[]
const b = parse(1);     // number[]
parse(true);            // ❌ TS2769: No overload matches this call.
```

⚠️ **顺序决定结果**——重载按**从上到下**匹配，宽的写前面会吞掉窄的：

```typescript
function bad(x: unknown): unknown;
function bad(x: string): string;
function bad(x: unknown): unknown { return x; }

const r = bad("a");     // 类型是 unknown 🛑 因为第一个签名先匹配上了

function good(x: string): string;
function good(x: unknown): unknown;
function good(x: unknown): unknown { return x; }

const r2 = good("a");   // ✅ string —— 窄的在前
```

**箭头函数不能重载**——只能用于 `function` 声明或对象/类方法：

```typescript
interface Fn {
  (x: string): string;    // 调用签名，可以多个 = 重载
  (x: number): number;
}
declare const f: Fn;
const s = f("a");         // string
```

| 限制 | 说明 |
| --- | --- |
| 实现签名必须兼容所有重载签名 | 否则报错 |
| 只有**最后一个**签名是实现的 | 实现签名不对外暴露 |
| 实现签名参数通常用联合或 `any` | 便于内部处理 |
| `Parameters` / `ReturnType` 只取**最后一个**签名 | ⚠️ 对重载函数有坑 |

> 💡 **能用联合类型就用联合，别急着上重载**。很多重载场景可以用「入参联合 + 返回值条件类型」表达得更清晰，而且对调用方更友好：
>
> ```typescript
> // 用重载
> function len(x: string): number;
> function len(x: unknown[]): number;
> function len(x: string | unknown[]): number { return x.length; }
>
> // 等价但更简洁
> function len2(x: string | unknown[]): number { return x.length; }
> ```

{{% /tab %}}

{{% tab header="this 参数" %}}

`this` 是**假参数**：写在参数列表最前面，占一个类型位置但不占实参位置，编译后消失。

```typescript
function handler(this: HTMLElement, e: Event) {
  this.classList.add("active");   // ✅ this 有类型
}

// 调用时必须保证 this 类型正确
button.addEventListener("click", handler);   // ✅ 事件系统会绑定正确的 this
handler.call(div, new Event("click"));       // ✅

// 🛑 单独调用会把 this 推断为 void，报错
const h = handler;
h(new Event("click"));   // ❌ TS2684: The 'this' context of type 'void' is not
                         //    assignable to method's 'this' of type 'HTMLElement'.
```

**显式标注 `this` 的两种位置**：

```typescript
// 1. 普通函数
function f(this: { count: number }) { this.count++; }

// 2. 对象/接口方法
interface Counter {
  count: number;
  inc(this: Counter): void;    // 显式 this 便于把方法拆出去复用
}
```

**在回调里保留 `this` 类型**：

```typescript
class Widget {
  name = "w";
  renderBad() {
    // 🛑 普通函数会丢 this
    return [1].map(function (n) { return this.name; });   // ❌ TS2683: 'this' implicitly has type 'any'
  }
  renderGood() {
    // ✅ 箭头函数继承外围 this
    return [1].map((n) => this.name);
  }
}
```

| 场景 | `this` 指向 | 处理 |
| --- | --- | --- |
| 箭头函数 | 定义处的 `this` | ✅ 首选 |
| `function` 回调 | `undefined`（严格模式） | 用箭头，或加 `this: T` 参数 |
| 对象方法拆出后单独调用 | 丢失 | 用 `bind`，或改成箭头属性 |
| 类的方法作为回调 | 丢失 | `this.method = this.method.bind(this)` 或箭头属性 |

{{% /tab %}}

{{% tab header="函数变型（逆变）" %}}

这是最容易搞错的一处。**`strictFunctionTypes` 下：参数逆变，返回值协变。**

```typescript
type Wide   = (x: string | number) => void;
type Narrow = (x: string) => void;

declare const wide: Wide;
declare const narrow: Narrow;

const a: Wide = narrow;   // ❌ TS2322: 参数不兼容
//    ~ Type '(x: string) => void' is not assignable to type '(x: string | number) => void'.
const b: Narrow = wide;   // ✅ 更宽的函数可以当更窄的用
```

**为什么参数是逆变**：`Narrow` 承诺「任何 `string` 都能处理」。如果把它当 `Wide` 用，调用方可能传 `number`，而它处理不了——所以不安全。反过来，`Wide` 什么都能处理，当 `Narrow` 用完全安全。

**方法语法是双变的**（历史遗留，`strictFunctionTypes` **不覆盖**方法）：

```typescript
type AsProp   = { f: (x: string | number) => void };   // 函数属性 -> 严格逆变
type AsMethod = { f(x: string | number): void };       // 方法语法 -> 双变

declare const narrowM: { f(x: string): void };

const p: AsProp   = { f: narrowM.f };   // ❌ TS2322
const m: AsMethod = narrowM;            // ✅ 放行 ⚠️
```

> ⚠️ 一个不健全的口子：**方法语法双变**意味着参数更窄的方法也能赋值。这是为了兼容大量既有 JS 代码而保留的。想强制严格检查，把方法写成**函数属性**形式。💭

**变型总表**（全部实测）：

| 位置 | 变型 | 方向 |
| --- | --- | --- |
| 函数参数 | **逆变** | 参数类型更**宽**才可赋值 |
| 函数返回值 | **协变** | 返回值类型更**窄**才可赋值 |
| 方法参数（方法语法） | **双变** ⚠️ | 双向都可 |
| `readonly` 属性 | 协变 | 可变 → 只读 ✅ |
| 可变属性 | 不变 | 只读 → 可变 ❌ |
| 数组元素 | 协变（不健全）⚠️ | 见 [02]({{< relref "02-Type-System-Core.md" >}}) |

{{% /tab %}}

{{% tab header="void 返回值的特例" %}}

回调位置的 `() => void` **接受任何返回值**：

```typescript
type Cb = () => void;

const returnsValue = () => 42;
const cb: Cb = returnsValue;      // ✅ 合法

[1, 2, 3].forEach((n) => n * 2);  // ✅ 返回了值也合法
[1, 2, 3].forEach((n) => { n * 2; });   // ✅ 返回 void 也合法
```

**为什么这样设计**：调用方声明「我不看返回值」，实现返回什么都不会造成问题。

⚠️ 但**显式声明返回类型**时不行：

```typescript
function f(): void { return 42; }   // ❌ TS2322: Type 'number' is not assignable to type 'void'.
```

| 写法 | 允许返回非 void |
| --- | --- |
| `type Cb = () => void`（当**值**赋给它） | ✅ |
| `function f(): void`（函数自己的返回类型） | ❌ |
| `function f(cb: () => void)`（参数位置） | ✅ |

> 💡 记住：**「`() => void` 作为类型标注」是宽松的，「`: void` 作为函数返回类型」是严格的。**

{{% /tab %}}

{{< /tabpane >}}

---

## 对象类型

{{< tabpane text=true persist=disabled >}}

{{% tab header="属性修饰符" %}}

```typescript
type Obj = {
  required: string;         // 必需
  optional?: number;        // 可选（可以不存在，或为 number）
  readonly frozen: boolean; // 只读（浅层）
  method(): void;           // 方法语法（双变）
  fnProp: () => void;       // 函数属性（严格逆变）
};
```

| 修饰符 | 效果 | 运行时有作用吗 |
| --- | --- | --- |
| `?` | 属性可缺省 | ❌ 编译期 |
| `readonly` | 禁止赋值 | ❌ 编译期（只是 `Object.freeze` 的注解） |
| `-?`（映射类型内） | 去掉可选 | ❌ |
| `-readonly`（映射类型内） | 去掉只读 | ❌ |

⚠️ **`readonly` 完全不影响运行时**，也不阻止深层修改：

```typescript
type R = { readonly a: { b: number } };
declare const r: R;
r.a = { b: 1 };   // ❌ TS2540: Cannot assign to 'a' because it is a read-only property.
r.a.b = 1;        // ✅ 合法！只保护第一层
```

> 💭 需要真正的运行时不可变，用 `Object.freeze`（注意它也**只是浅层**），或 `Immer`、`immutable.js` 这类库。`readonly` 的价值是**让编译器帮你避免误改**，不是安全边界。

{{% /tab %}}

{{% tab header="索引签名" %}}

表示「任意键都映射到某个类型」。

```typescript
type Dict = { [key: string]: number };
const d: Dict = { a: 1, b: 2 };
const v = d["anything"];        // number

// 也可以用 Record
type Dict2 = Record<string, number>;

// 数字索引
type Arr = { [index: number]: string };
type Arr2 = string[];           // 更常用

// 同时约束已知键与索引签名
type Mixed = { [k: string]: number; fixed: number };   // ✅ fixed 兼容索引类型
```

⚠️ **已知属性必须兼容索引签名**：

```typescript
type Bad = { [k: string]: number; fixed: string };
//                                     ~~~~~~ ❌ TS2411: Property 'fixed' of type 'string'
//                                            is not assignable to 'string' index type 'number'.
```

⚠️ **索引签名不带 `undefined`**——这是 `strictNullChecks` 下最大的坑之一：

```typescript
type Dict = { [k: string]: number };
const d: Dict = { a: 1 };
const v: number = d["missing"];   // ✅ 编译通过，运行时是 undefined 💥
```

防御手段是 `noUncheckedIndexedAccess`：

| 选项 | `d["missing"]` 类型 |
| --- | --- |
| 默认 | `number` ⚠️ 撒谎 |
| `noUncheckedIndexedAccess: true` | `number \| undefined` ✅ 诚实 |

```jsonc
// 强烈建议开启（注意：它不在 strict 里，需要单独写）
{ "compilerOptions": { "noUncheckedIndexedAccess": true } }
```

> 🔥 **`noUncheckedIndexedAccess` 是「不在 `strict` 内但极推荐」的选项**。它同样影响数组：`arr[0]` 变成 `T | undefined`。唯一的代价是要多写判空，但换来的正是真实情况。

**`keyof` 遇索引签名会包含 `number`**：

```typescript
type D = { [k: string]: number };
type K = keyof D;              // string | number ⚠️ 因为 obj[0] 等价于 obj["0"]
type K2 = string & keyof D;    // string —— 这样窄化
```

{{% /tab %}}

{{% tab header="多余属性检查" %}}

这是结构化类型的一个**特例**：只有**对象字面量**直接赋值时才会检查多余属性。

```typescript
type Opt = { a: number };

const lit: Opt = { a: 1, b: 2 };
//                        ~ ❌ TS2353: Object literal may only specify known properties,
//                                 and 'b' does not exist in type 'Opt'.

// 经过中间变量就不检查了
const viaVar = { a: 1, b: 2 };
const ok1: Opt = viaVar;                 // ✅ 不报错（结构化类型：多属性无害）

// 函数实参位置的字面量也会检查
function take(o: Opt) {}
take({ a: 1, b: 2 });                    // ❌ TS2353

// 展开运算符的结果不触发
const spread = { ...{ b: 2 }, a: 1 };
take(spread);                            // ✅
```

| 触发检查 | 不触发检查 |
| --- | --- |
| `const x: T = { ... }` | 经过变量中转 |
| `fn({ ... })` 实参 | 展开 `{ ...obj }` |
| 返回位置 `return { ... }` | `as T` 断言 |
| 嵌套字面量（也会查） | 索引签名目标类型 |

**为什么需要这个检查**：它是为了抓拼写错误。

```typescript
interface Config { timeout: number }
const c: Config = { timeOut: 5000 };   // ✅ 没有这个检查就抓不到拼写错误
```

**如何合法地「多带属性」**：

```typescript
// 1. 中间变量
const extra = { a: 1, b: 2 };
const o1: Opt = extra;

// 2. 用索引签名接收
const o2: Opt & Record<string, unknown> = { a: 1, b: 2 };

// 3. 明确断言为交叉类型
const o3 = { a: 1, b: 2 } as Opt & { b: number };
```

{{% /tab %}}

{{% tab header="接口 vs 类型别名" %}}

两者 90% 场景可互换，但有明确差异。

| 能力 | `interface` | `type` |
| --- | --- | --- |
| 描述对象形状 | ✅ | ✅ |
| 联合类型 | ❌ | ✅ |
| 交叉类型 | ❌（用 `extends` 多继承） | ✅ |
| 元组 / 原始类型别名 | ❌ | ✅ |
| 映射类型 / 条件类型 | ❌ | ✅ |
| **声明合并** | ✅ 可多次声明自动合并 🔥 | ❌ 重复声明报错 |
| 实现（`implements`） | ✅ | ✅（对象类型时） |
| 错误信息可读性 | ✅ 显示接口名 | ⚠️ 可能展开成大段结构 |
| 性能 | ✅ 通常更好 | ⚠️ 复杂交叉类型可能变慢 |

```typescript
// interface 可以声明合并（库的类型扩充靠这个）
interface Window { myGlobal: string }
interface Window { another: number }
// 结果：Window 同时有两个属性

// type 不能重复声明
type T = { a: number };
type T = { b: number };   // ❌ TS2300: Duplicate identifier 'T'.
```

**选择建议** 💭：

| 场景 | 用 |
| --- | --- |
| 对象形状、类契约、需要被扩充 | `interface` 🔥 |
| 联合、元组、映射类型、工具类型 | `type` 🔥 |
| 团队约定 | 任选其一保持一致即可 |
| 库的公开 API | `interface`（错误信息更友好，且允许使用者扩充） |

> ⚠️ `interface` 的声明合并是**双刃剑**：它让库能被扩充，也让「不小心重名」变成静默合并。全局接口名尤其要小心。

{{% /tab %}}

{{< /tabpane >}}

---

## 类

{{< tabpane text=true persist=disabled >}}

{{% tab header="访问控制：private vs #" %}}

**这是 TypeScript 里最重要的一个语义区别**。

| 特性 | `private`（TS 关键字） | `#field`（JS 原生） |
| --- | --- | --- |
| 检查时机 | **仅编译期** | **运行期真私有** |
| 编译产物 | 普通属性，运行时可见可改 | 真正的私有槽位 |
| `obj["privateProp"]` | ✅ 能访问 💥 | ❌ 拿不到 |
| 结构化类型 | 需要**同源声明** | 名义唯一，天然不兼容 |
| 目标要求 | 无 | `target` ≥ ES2022（或降级辅助） |
| 子类访问 | 不能（用 `protected`） | 不能 |

```typescript
class A { private x = 1; }
class B { private x = 1; }     // 形状相同但不同源
declare let a: A;
declare let b: B;
a = b;
// ❌ TS2322: Type 'B' is not assignable to type 'A'.
//    Types have separate declarations of a private property 'x'.
```

```typescript
class C { #x = 1; }
class D { #x = 1; }
declare let c: C;
declare let d: D;
c = d;
// ❌ TS2322: Type 'D' is not assignable to type 'C'.
//    Property '#x' in type 'D' refers to a different member that cannot be
//    accessed from within type 'C'.
```

> 🔥 **实用价值**：`private` 和 `#` 都能**阻止结构化类型的意外兼容**，这正是「品牌类型」想解决的问题，而且不需要手写 `unique symbol`。想让两个类型不能互赋，加一个私有成员就行。

```typescript
class UserId { private _brand!: void; constructor(readonly value: string) {} }
class OrderId { private _brand!: void; constructor(readonly value: string) {} }

declare const u: UserId;
declare const o: OrderId;
const x: OrderId = u;   // ❌ 无法互赋，且运行时有真实区分
```

**访问修饰符全表**：

| 修饰符 | 类内 | 子类 | 外部 | 编译期拦 | 运行时可绕过 |
| --- | --- | --- | --- | --- | --- |
| `public`（默认） | ✅ | ✅ | ✅ | — | — |
| `protected` | ✅ | ✅ | ❌ | ✅ | ✅ 能 |
| `private` | ✅ | ❌ | ❌ | ✅ | ✅ 能 |
| `#` | ✅ | ❌ | ❌ | ✅ | ❌ **不能** 🔥 |

```typescript
class P {
  constructor(
    public a: number,        // 参数属性：自动声明 + 赋值
    private b: string,
    protected c = true,
    readonly d = 1,
  ) {}
}
const p = new P(1, "x");
p.a;   // ✅
p.b;   // ❌ TS2341: Property 'b' is private and only accessible within class 'P'.
```

> ⚠️ **参数属性会生成运行时代码**，因此**不能**通过 `erasableSyntaxOnly`，也**不能**被 Node 直接运行。要兼容「Node 原生跑 TS」，得手写字段声明与赋值。

{{% /tab %}}

{{% tab header="初始化与明确赋值" %}}

`strictPropertyInitialization`（随 `strict` 默认开启）要求属性在构造函数里被赋值。

```typescript
class Bad {
  y: number;
  // ❌ TS2564: Property 'y' has no initializer and is not definitely assigned
  //    in the constructor.
}
```

**五种解法**：

```typescript
class A { x: number = 0; }                          // 1. 直接给初值
class B { x: number; constructor() { this.x = 1; } } // 2. 构造函数里赋值
class C { x?: number; }                             // 3. 声明为可选
class D { x!: number; }                             // 4. 明确赋值断言（你保证会赋值）⚠️
class E { x: number | undefined; }                  // 5. 允许 undefined
```

**明确赋值断言 `!`** 常用在框架注入的场景：

```typescript
class Service {
  // NestJS / DI 之类会注入，自己确实不赋值
  private readonly repo!: Repository;

  // 或者在生命周期钩子里赋值
  el!: HTMLElement;
  mounted() { this.el = document.createElement("div"); }
}
```

> ⚠️ `!` 是**你向编译器做的保证**，它不做任何检查。如果实际没赋值，运行时就是 `undefined`——而类型说有值。这是「类型撒谎」的常见来源。

**`readonly` 与 `as const` 在类里**：

```typescript
class Config {
  readonly host: string;
  constructor(host: string) {
    this.host = host;         // ✅ readonly 允许在构造函数里赋值
  }
  change() { this.host = "x"; }   // ❌ TS2540: Cannot assign to 'host'
}
```

{{% /tab %}}

{{% tab header="继承与 override" %}}

```typescript
class Base {
  greet() { return "base"; }
  protected secret() { return 1; }
}

class Sub extends Base {
  override greet() { return "sub"; }      // ✅ 显式声明覆盖
  override nope() { return 2; }
  //     ~~~~ ❌ TS4113: This member cannot have an 'override' modifier because
  //            it is not declared in the base class 'Base'.
}
```

**开启 `noImplicitOverride` 后必须写 `override`**：

| 选项 | 行为 |
| --- | --- |
| 默认 | `override` 可写可不写 |
| `noImplicitOverride: true` | 🚧 覆盖基类成员**必须**写 `override` |

> 🔥 `noImplicitOverride` 的价值：基类改名时，子类会**立刻报错**（因为 `override` 找不到目标），而不是静默变成「新增了一个无关方法」。**强烈建议开启**。

**`extends` vs `implements`**：

| | `extends` | `implements` |
| --- | --- | --- |
| 继承实现 | ✅ | ❌ 只检查形状 |
| 继承类型 | ✅ | ✅ |
| 多个 | ❌ 单继承（可 `extends` 一个类 + 多个接口） | ✅ 可多个 |
| 构造函数 | 必须 `super()` | 无要求 |
| 运行时代码 | ✅ 有原型链 | ❌ 完全擦除 |

```typescript
interface Serializable { serialize(): string }
interface Comparable { compareTo(o: unknown): number }

class Doc implements Serializable, Comparable {
  serialize() { return "{}"; }
  compareTo(o: unknown) { return 0; }
}
// implements 只做检查，编译产物里没有任何痕迹
```

**抽象类**：

```typescript
abstract class Shape {
  abstract area(): number;          // 抽象方法：子类必须实现
  describe(): string {              // 具体方法：可直接继承
    return `面积 ${this.area()}`;
  }
}

class Circle extends Shape {
  constructor(private r: number) { super(); }
  area() { return Math.PI * this.r ** 2; }
}

const s = new Shape();   // ❌ TS2511: Cannot create an instance of an abstract class.
```

**接口用 `abstract new` 约束构造函数**：

```typescript
type Ctor<T> = abstract new (...args: any[]) => T;
function create<T>(C: Ctor<T>): T { return new (C as any)(); }
```

{{% /tab %}}

{{% tab header="类的类型与静态成员" %}}

**「类的类型」有两个**——实例类型与构造函数类型：

```typescript
class User {
  constructor(public name: string) {}
  static create(n: string) { return new User(n); }
  greet() { return this.name; }
}

// 实例类型：直接用类名
const u: User = new User("a");
type Inst = User;                    // 实例类型

// 构造函数类型：用 typeof
type Ctor = typeof User;             // new (name: string) => User，含静态成员
const C: Ctor = User;

// 从构造函数取实例类型
type Inst2 = InstanceType<typeof User>;   // User
```

| 想要 | 写 |
| --- | --- |
| 实例类型 | `User` |
| 构造函数类型 | `typeof User` |
| 从值取实例类型 | `InstanceType<typeof User>` |
| 静态成员类型 | `typeof User.create` |

**静态成员与 `this`**：

```typescript
class Registry {
  static items: string[] = [];
  static add(item: string) { this.items.push(item); }   // this 指构造函数
}
Registry.add("a");   // ✅
```

> ⚠️ 静态成员**不参与**结构化类型的实例比较。`InstanceType<typeof A>` 不含静态成员。

**getter / setter**：

```typescript
class Temp {
  private _celsius = 0;
  get celsius(): number { return this._celsius; }
  set celsius(v: number) { this._celsius = v; }
}

// TS 5.1+ 允许 getter 和 setter 类型不同
class Box {
  private _v: string | undefined;
  get value(): string { return this._v ?? ""; }
  set value(v: string | undefined) { this._v = v; }   // ✅ 5.1+ 合法
}
```

> 💡 只写 `get` 不写 `set` 就等于 `readonly` 属性（TS 4.3+ 起赋值会报错）。

{{% /tab %}}

{{< /tabpane >}}

---

## 结构化类型的实战影响

因为 TS 看形状不看名字，有些事会「意外合法」：

```typescript
interface Point { x: number; y: number }
interface Vector2 { x: number; y: number }

declare const p: Point;
const v: Vector2 = p;    // ✅ 完全合法，尽管两者语义不同 ⚠️
```

**想让它们不兼容**，有三条路：

| 手段 | 写法 | 运行时区分 |
| --- | --- | --- |
| 私有成员 | `class Point { private _brand!: void }` | ✅ |
| 品牌类型 | `type Point = {x: number} & { readonly __b: unique symbol }` | ❌ |
| `#` 私有字段 | `class Point { #b = 1 }` | ✅ 🔥 |

```typescript
// 推荐：用私有成员做「名义类型」
class UserId {
  private readonly _brand!: void;      // 只为类型区分存在
  constructor(readonly value: string) {}
}
class OrderId {
  private readonly _brand!: void;
  constructor(readonly value: string) {}
}

function fetchUser(id: UserId) { /* ... */ }
fetchUser(new OrderId("x"));
// ❌ TS2345: Argument of type 'OrderId' is not assignable to parameter of type 'UserId'.
//    Types have separate declarations of a private property '_brand'.
```

> 💭 这个技巧在 ID 满天飞、金额与数量容易混淆的项目里价值极高。缺点是每次进入这个类型都要 `new` 一次（有轻微运行时开销），或者用 `as UserId` 断言。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 重载顺序反了 | 推断成 `unknown` | 窄签名写前面 |
| `Parameters` 对重载 | 只拿到最后一个签名 | 避免对重载用，或提供单一签名 |
| 回调里用 `function` | `this` 丢失（`TS2683`） | 用箭头函数 |
| 以为 `private` 是安全的 | 运行时能访问 | 用 `#` |
| 忘记初始化属性 | `TS2564` | 给初值或用 `?` |
| 滥用 `!` 明确赋值 | 运行时 `undefined` | 老老实实初始化 |
| 索引访问没 `undefined` | 运行时崩溃 | 开 `noUncheckedIndexedAccess` |
| 想用索引签名但已知键不兼容 | `TS2411` | 统一类型，或拆成联合 |
| 以为 `readonly` 是深层的 | 内层被改 | 深层用 `DeepReadonly`（见 [06]({{< relref "06-Type-Level-Programming-Recipes.md" >}})） |
| 对象字面量多带属性 | `TS2353` | 经变量中转，或改类型 |
| 以为 `implements` 生成代码 | 运行时没有 | 它纯擦除 |
| 参数属性 + Node 直跑 | `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` | 手写字段声明 |
