+++
title = "第8章 函数类型系统"
weight = 80
date = "2026-03-26T21:05:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 8 章 函数类型系统

> 函数是 JavaScript/TypeScript 世界的一等公民——函数式编程、单体应用、事件驱动，统统离不开函数。TypeScript 的函数类型系统让你在定义函数时有"火眼金睛"，一眼看穿参数和返回值的类型猫腻。

## 8.1 函数声明的类型签名

### 8.1.1 返回值类型注解：显式声明 vs 隐式推断

在 TypeScript 中，函数的返回值可以**显式声明类型**，也可以让 TypeScript **自动推断**。

```typescript
// 显式声明返回值类型
function addExplicit(a: number, b: number): number {
    return a + b;
}

// 隐式推断（TypeScript 会自动推断返回值为 number）
function addImplicit(a: number, b: number) {
    return a + b;
}

console.log(addExplicit(1, 2)); // 3
console.log(addImplicit(3, 4));  // 7
```

**什么时候应该显式声明返回值？**

- **复杂类型**：当返回值类型不容易从代码中推断时
- **文档价值**：显式类型本身就是最好的文档
- **类型收窄**：在条件分支中，显式声明有助于类型检查

```typescript
// 复杂返回类型的典型场景
function parseJSON(json: string): { success: boolean; data?: object; error?: string } {
    try {
        return { success: true, data: JSON.parse(json) };
    } catch (e) {
        return { success: false, error: (e as Error).message };
    }
}
```

### 8.1.2 函数参数的注解：必选参数、可选参数（?）、默认参数、剩余参数（...）

TypeScript 的函数参数支持四种形式：

```typescript
// 必选参数：必须传，不传就报错
function required(name: string) {
    console.log(`Hello, ${name}!`);
}
required("张三"); // OK
// required(); // TS2554: Expected 1 argument, but got 0

// 可选参数：加了 ?，传不传都行
function optional(name: string, age?: number) {
    if (age !== undefined) {
        console.log(`${name} is ${age} years old.`);
    } else {
        console.log(`${name} doesn't want to reveal age.`);
    }
}
optional("小明");       // 小明 doesn't want to reveal age.
optional("小红", 25);   // 小红 is 25 years old.

// 默认参数：直接给默认值
function defaults(name: string, greeting: string = "Hello") {
    console.log(`${greeting}, ${name}!`);
}
defaults("张三");              // Hello, 张三!
defaults("李四", "Hi there"); // Hi there, 李四!

// 剩余参数：用 ... 收集剩余参数为数组
function sum(...numbers: number[]): number {
    return numbers.reduce((acc, n) => acc + n, 0);
}
console.log(sum(1, 2, 3, 4, 5)); // 15
```

### 8.1.3 为什么参数类型不匹配是编译错误

#### 8.1.3.1 函数是 JavaScript 中最常见的抽象单元；参数类型不匹配意味着调用方和实现方的契约不一致——这是最常见的 bug 来源

在 Java、C++ 等静态类型语言中，参数类型不匹配是理所当然的编译错误。但 JavaScript 诞生于"天下大同"的混沌年代，一个函数可以接受任意类型的参数，传什么算什么。

TypeScript 恢复了"契约精神"——**函数的参数类型是调用方和实现方之间的协议**。如果你签了"我要 number"的合同，却送来 string，TypeScript 就会毫不犹豫地报错。

```typescript
// 这份"合同"说：参数必须是 string
function greet(name: string) {
    console.log(`Hello, ${name.toUpperCase()}!`);
}

// 调用方送来一个 number —— 违反合同！
greet(123); // TS2345: Argument of type 'number' is not assignable to parameter of type 'string'
```

**为什么这是必要的？** 因为 `greet` 内部调用了 `.toUpperCase()`，这个方法只有 string 有。如果你传了 number，运行时就会爆炸：`TypeError: name.toUpperCase is not a function`。

TypeScript 在**编译期**就帮你捕捉到了这个 bug，而不是等到运行时才爆炸。这叫做"**防御性编程**"——TypeScript 是你的代码保安，把一切危险拦截在门外。

---

## 8.2 函数表达式与箭头函数

### 8.2.1 函数表达式的类型注解

在 TypeScript 中，函数表达式也可以有类型注解：

```typescript
// 方式一：给变量加类型注解，函数表达式符合这个类型
const add: (a: number, b: number) => number = function (a, b) {
    return a + b;
};

// 方式二：用 type 别名
type AddFn = (a: number, b: number) => number;
const add2: AddFn = function (a, b) {
    return a + b;
};

console.log(add(1, 2));   // 3
console.log(add2(3, 4));  // 7
```

### 8.2.2 箭头函数的类型签名

箭头函数在 TypeScript 中同样可以精确注解：

```typescript
// 完整的箭头函数类型注解
const double: (n: number) => number = (n) => n * 2;

// 多参数箭头函数
const add: (a: number, b: number) => number = (a, b) => a + b;

// 可选参数
const greet: (name?: string) => string = (name) =>
    name ? `Hello, ${name}!` : "Hello, stranger!";

console.log(double(5));    // 10
console.log(add(3, 4));    // 7
console.log(greet());       // Hello, stranger!
console.log(greet("小明")); // Hello, 小明!
```

**箭头函数 vs 普通函数的类型差异**：

- 普通函数有 `this`（执行期绑定）
- 箭头函数没有 `this`（永久词法绑定）

关于 `this`，我们后面有专门的小节来讲解。

---

## 8.3 函数重载（Overload）

### 8.3.1 函数重载的声明

函数重载让你为一个函数定义**多个类型签名**，TypeScript 会根据调用时传入的参数类型，选择最匹配的那个签名。

```typescript
// 函数重载签名
function process(value: string): string;
function process(value: number): number;
function process(value: boolean): string;

// 函数实现（实现签名）
function process(value: string | number | boolean): string | number {
    if (typeof value === "string") {
        return value.toUpperCase();
    } else if (typeof value === "number") {
        return value * 2;
    } else {
        return value ? "yes" : "no";
    }
}

console.log(process("hello"));   // HELLO（匹配第一个重载）
console.log(process(42));       // 84（匹配第二个重载）
console.log(process(true));     // yes（匹配第三个重载）
```

#### 8.3.1.1 多个重载签名 + 一个实现签名；每个重载签名之间参数数量或参数类型必须不同

注意：**重载签名没有函数体**，只有类型签名。实现签名要有函数体，它的参数类型必须**兼容**所有重载签名的参数类型。

```typescript
// 重载签名 1：参数为 string
function format(value: string): string;

// 重载签名 2：参数为 string + format style
function format(value: string, style: "upper" | "lower"): string;

// 实现签名：必须兼容所有重载
function format(value: string, style?: "upper" | "lower"): string {
    if (style === "upper") return value.toUpperCase();
    if (style === "lower") return value.toLowerCase();
    return value;
}

console.log(format("hello"));                    // hello
console.log(format("hello", "upper"));           // HELLO
console.log(format("hello", "lower"));           // hello
```

#### 8.3.1.2 所有重载签名的参数类型必须与实现签名的参数类型相互兼容（TS 按顺序匹配第一个兼容的重载）

TypeScript 按**从上到下**的顺序匹配重载签名，选择**第一个匹配的**。所以，把更具体的签名放在前面：

```typescript
// 正确的顺序：更具体的放前面
function fn(value: string): string;        // 匹配 string
function fn(value: unknown): string;        // 匹配其他
function fn(value: unknown): string {
    return String(value);
}

// 如果顺序错了……
function fnBad(value: unknown): string;        // 这个会先匹配！
function fnBad(value: string): string;         // 这个永远不会被用到
function fnBad(value: unknown): string {
    return String(value);
}
```

### 8.3.2 为什么 TypeScript 的函数重载是「静态的」

#### 8.3.2.1 Java/C++ 的重载在编译时直接生成多个函数实体（名字 mangling）；TypeScript 的重载只是类型层面的签名，编译后只保留一个函数实现

这是 TypeScript 和 Java/C++ 重载的本质区别。

Java 的重载：
```java
// 编译后，Java 会生成两个不同的 .class 文件
// add(int, int) 和 add(double, double) 是两个完全不同的方法
int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }
```

TypeScript 的重载：
```typescript
// 编译后，只有一个 JavaScript 函数实现
// 重载签名只是给 TypeScript 编译器看的"文档"
function add(a: number, b: number): number;
function add(a: string, b: string): string;
function add(a: number | string, b: number | string): number | string {
    // 只有一个函数体
}
```

编译成 JavaScript 后：

```javascript
function add(a, b) {
    // 只有一个实现，TypeScript 在编译期做类型检查，运行时就是这段代码
}
```

所以，TypeScript 的函数重载是"**纸老虎**"——看起来有多个函数，实际运行时只有一个。它只是 TypeScript 类型系统的语法糖，帮助你在编译期获得更好的类型检查。

### 8.3.3 构造函数重载

构造函数也可以重载：

```typescript
class Timer {
    private startTime: Date | number;

    // 重载签名 1：传入 Date
    constructor(time: Date);

    // 重载签名 2：传入毫秒时间戳
    constructor(time: number);

    // 重载签名 3：无参数，默认为现在
    constructor();

    // 实现
    constructor(time?: Date | number) {
        if (time === undefined) {
            this.startTime = Date.now();
        } else if (time instanceof Date) {
            this.startTime = time.getTime();
        } else {
            this.startTime = time;
        }
    }

    getStartTime(): number {
        return typeof this.startTime === "number" ? this.startTime : this.startTime.getTime();
    }
}

const t1 = new Timer();                          // 当前时间
const t2 = new Timer(new Date("2026-01-01"));    // 指定日期
const t3 = new Timer(1700000000000);             // 指定时间戳

console.log(t1.getStartTime()); // 1742976000000（当前时间戳示例）
```

---

## 8.4 this 的类型

### 8.4.1 JavaScript 中 this 的复杂性：执行期绑定

`this` 是 JavaScript 最让人头疼的特性之一。它的值不是由函数定义时决定，而是由**调用方式**决定。

```javascript
const person = {
    name: "张三",
    greet() {
        console.log(`Hello, I'm ${this.name}`);
    },
};

person.greet(); // "Hello, I'm 张三" —— this 是 person

const greetFn = person.greet;
greetFn(); // "Hello, I'm undefined" —— this 是 undefined（非严格模式）或 window（严格模式）
```

这就是 JavaScript 的"this 陷阱"——同一个函数，不同调用方式，this 完全不同。

### 8.4.2 TypeScript 中 this 的类型注解

#### 8.4.2.1 语法：函数第一个参数位置写 `this: Type`（编译时语法）

TypeScript 用一种巧妙的方式处理 `this` 类型——把它当作**函数的第一个参数**来写：

```typescript
function greet(this: { name: string }, message: string) {
    console.log(`${message}, I'm ${this.name}`);
}

const person = { name: "张三", greet };

// 显式绑定 this
greet.call({ name: "李四" }, "Hello"); // Hello, I'm 李四
person.greet("Hi");                     // Hi, I'm 张三
```

注意：`this: Type` 是**编译时语法**，编译成 JavaScript 后会**完全消失**，不影响运行时性能。

### 8.4.3 为什么 TypeScript 用参数位置写 this（而非关键字）

#### 8.4.3.1 JavaScript 语法中 `this` 是关键字，无法用作参数名；TS 的 `this: Type` 是编译时语法，编译后消除

JavaScript 的 `this` 是保留关键字，你不能写 `function(this, name)`。如果 TypeScript 直接支持 `function this(this: Type)`，会语法冲突。

所以 TypeScript 采用了折中方案：**把 this 当作一个隐式参数**，在类型注解位置用 `this: Type` 来表示。

```typescript
// TypeScript 源码
function myFunc(this: Window, name: string) {
    console.log(this.name); // this 的类型被标注为 Window
}

// 编译成 JavaScript 后
function myFunc(name) {
    // this 消失了！只剩 name 参数
    console.log(this.name);
}
```

这个设计非常聪明——既保持了 JavaScript 的语法兼容性，又让 TypeScript 获得了 this 类型检查的能力。

### 8.4.4 箭头函数中的 this：永久词法绑定，不需要类型注解

箭头函数没有自己的 `this`，它永远捕获**定义时**的外层 `this`，并且不可改变（call、apply、bind 都无法改变）。

```typescript
class Timer {
    name = "Timer";

    // 箭头函数，this 永久绑定为 Timer 实例
    tick = () => {
        console.log(`${this.name} ticked!`);
    };
}

const timer = new Timer();
const fn = timer.tick;
fn(); // Timer ticked! —— this 仍然是 Timer 实例
// 即使把函数单独取出来调用，this 也不会丢失

// 对比：普通函数会丢失 this
class Timer2 {
    name = "Timer2";
    tick() {
        console.log(`${this.name} ticked!`);
    }
}

const timer2 = new Timer2();
const fn2 = timer2.tick;
fn2(); // TypeError: Cannot read properties of undefined (reading 'name') —— 严格模式下 this 为 undefined，直接爆炸！
```

### 8.4.5 TypeScript 6.0 对无 this 方法的上下文推断优化

#### 8.4.5.1 背景：方法语法有隐式 this 参数，导致上下文推断优先级低于箭头函数；TS 6.0 改进：若方法内部未使用 this，则不视为上下文敏感函数，提升推断优先级

TypeScript 6.0 对方法 `this` 的推断做了重要优化：

```typescript
// 之前 TypeScript 的推断逻辑：
// 方法有隐式 this 参数 → 被视为"上下文敏感函数"
// → 推断优先级低于直接赋值的箭头函数

// TS 6.0 改进：
// 如果方法内部没有使用 this → 不视为上下文敏感函数
// → 推断优先级和箭头函数一样高

class Handler {
    // 方法内部没有用 this，TS 6.0 会优先推断
    handleClick = () => {
        console.log("clicked!");
    };

    // 这个方法用了 this，仍然是上下文敏感函数
    handleMouseDown(event: MouseEvent) {
        console.log(this.name); // this.name 用到了 this
    }
}
```

---

## 8.5 泛型函数

### 8.5.1 泛型函数的基本语法：`function identity<T>(arg: T): T`

泛型函数让函数可以"吃进任意类型，吐出对应类型"。`<T>` 是泛型参数，在调用时自动推断（或显式指定）。

```typescript
// identity 的意思是"原样返回"
function identity<T>(arg: T): T {
    return arg;
}

const num = identity(42);          // T 被推断为 number
const str = identity("hello");      // T 被推断为 string
const bool = identity<boolean>(true); // 显式指定 T = boolean

console.log(num);  // 42
console.log(str);  // hello
console.log(bool); // true
```

### 8.5.2 类型推断：编译器自动推断泛型参数

TypeScript 的类型推断能力非常强大，大多数情况下你不需要显式指定泛型参数：

```typescript
// TypeScript 自动推断 T = string[]
function firstElement<T>(arr: T[]): T | undefined {
    return arr[0];
}

const s = firstElement(["a", "b", "c"]); // T = string，s 的类型是 string | undefined
const n = firstElement([1, 2, 3]);      // T = number，n 的类型是 number | undefined
const empty = firstElement([]);          // T = unknown，empty 的类型是 unknown | undefined
```

### 8.5.3 多泛型参数：`function map<T, U>(arr: T[], fn: (item: T) => U): U[]`

一个函数可以有多个泛型参数：

```typescript
// map: 把 T[] 通过 fn 变换成 U[]
function map<T, U>(arr: T[], fn: (item: T) => U): U[] {
    return arr.map(fn);
}

const numbers = [1, 2, 3, 4, 5];
const doubled = map(numbers, (n) => n * 2); // number[]
const strings = map(numbers, (n) => `数字-${n}`); // string[]
const objects = map(numbers, (n) => ({ value: n })); // { value: number }[]

console.log(doubled);  // [2, 4, 6, 8, 10]
console.log(strings);  // ['数字-1', '数字-2', '数字-3', '数字-4', '数字-5']
console.log(objects);  // [{ value: 1 }, { value: 2 }, { value: 3 }, { value: 4 }, { value: 5 }]
```

---

## 8.6 异步函数与 Promise

### 8.6.1 Promise\<T\> 类型注解

`Promise<T>` 表示一个"将在未来产生 T 类型值"的操作。

```typescript
function fetchUser(): Promise<User> {
    return fetch("/api/user")
        .then((res) => res.json())
        .then((data) => data as User);
}

// 返回类型是 Promise<User>，调用方知道这是个异步操作
fetchUser().then((user) => {
    console.log(user.name); // user 的类型是 User
});
```

### 8.6.2 async 函数的返回类型推导：`async function getData(): Promise<string>`

`async` 函数**始终返回 Promise**。即使你写 `return "hello"`，实际返回值也是 `Promise<"hello">`。

```typescript
// async 函数会自动包装返回值为 Promise
async function getData(): Promise<string> {
    return "Hello, async world!";
}

// 等价于
function getDataEquiv(): Promise<string> {
    return Promise.resolve("Hello, async world!");
}

getData().then((value) => {
    console.log(value); // Hello, async world!
});
```

### 8.6.3 Promise 泛型方法：Promise.all、Promise.race、Promise.allSettled 的泛型类型

这三个是 Promise 的"聚合方法"，用来同时处理多个 Promise：

```typescript
// Promise.all<T>: 所有 Promise 都成功才成功，返回所有结果的数组
async function demoAll() {
    const [user, posts, comments] = await Promise.all([
        fetch("/api/user").then((r) => r.json()),
        fetch("/api/posts").then((r) => r.json()),
        fetch("/api/comments").then((r) => r.json()),
    ]);
    console.log(user, posts, comments);
}

// Promise.race<T>: 返回最先完成（无论成功或失败）的那个 Promise 的结果
async function demoRace() {
    const result = await Promise.race([
        fetch("/api/fast").then((r) => r.json()),
        fetch("/api/slow").then((r) => r.json()),
    ]);
    console.log(result); // 先返回的那个
}

// Promise.allSettled<T>: 所有 Promise 都结束后（无论成功失败），返回每个 Promise 的状态和结果
async function demoAllSettled() {
    const results = await Promise.allSettled([
        fetch("/api/user").then((r) => r.json()),
        fetch("/api/fail").then((r) => r.json()), // 这个会失败
    ]);

    for (const result of results) {
        if (result.status === "fulfilled") {
            console.log("成功:", result.value);
        } else {
            console.log("失败:", result.reason);
        }
    }
}
```

---

## 8.7 生成器函数

### 8.7.1 Generator 函数类型签名：`function*(): Generator<T, TReturn, TNext>`

生成器函数是 TypeScript 中最复杂的函数类型之一。它的签名有三个类型参数：

```typescript
// Generator<T, TReturn, TNext>
// T: yield 出来的值的类型
// TReturn: return 的值的类型
// TNext: next() 可以接收的参数类型

function* numberGenerator(): Generator<number, string, boolean> {
    console.log("生成器启动了");
    let count = 0;
    while (count < 3) {
        // yield 会暂停函数，返回 yield 右边的值
        const shouldContinue: boolean = yield count++; // yield 左边是 next() 传入的值，右边是 yield 出去的值
        console.log("收到外部消息:", shouldContinue);
    }
    return "Done!"; // 生成器结束时，返回这个值
}

const gen = numberGenerator();

console.log(gen.next());       // { value: 0, done: false } - 生成器启动了，收到外部消息: undefined
console.log(gen.next(true));   // { value: 1, done: false } - 收到外部消息: true
console.log(gen.next(false));  // { value: 2, done: false } - 收到外部消息: false
console.log(gen.next());       // { value: undefined, done: true } —— return 执行后生成器已结束，value 为 undefined（Generator 不保留 return 的值）
```

### 8.7.2 异步生成器函数类型

异步生成器是 `async function*`，返回 `AsyncGenerator`：

```typescript
type Page = { id: number; title: string; content: string };

async function* fetchPages(url: string): AsyncGenerator<Page, void, void> {
    let page = 1;
    let hasMore = true;

    while (hasMore) {
        const response = await fetch(`${url}?page=${page}`);
        const data = await response.json() as { items: Page[]; hasMore: boolean };

        for (const item of data.items) {
            yield item; // 每次 yield 一个页面数据
        }

        hasMore = data.hasMore;
        page++;
    }
}

async function demo() {
    for await (const page of fetchPages("/api/data")) {
        console.log("处理页面:", page);
    }
}
```

---

## 本章小结

本章深入探讨了 TypeScript 函数类型系统的方方面面。

### 函数类型基础

函数参数可以是**必选**、**可选（?）**、**默认参数**或**剩余参数（...）**。返回值可以显式声明，也可以让 TypeScript 隐式推断。参数类型不匹配是编译错误，因为这违反了调用方和实现方之间的"类型契约"。

### 函数重载

TypeScript 的函数重载是"静态的"——编译后只有一个函数实现，重载签名只是类型层面的语法糖。记住：把更具体的签名放在前面，TypeScript 按顺序匹配第一个兼容的重载。

### this 类型

TypeScript 用 `this: Type` 作为函数的第一个参数来处理 this 类型（编译时语法）。箭头函数没有自己的 this，永远是词法绑定。TS 6.0 改进了对"未使用 this 的方法"的推断优先级。

### 泛型函数

泛型函数 `<T>` 让一个函数可以操作多种类型，同时保持类型安全。TypeScript 自动推断泛型参数，你也可以显式指定。

### 异步函数

`async` 函数始终返回 `Promise`。`Promise.all`/`Promise.race`/`Promise.allSettled` 是三个聚合方法，分别处理"全成功才成功"、"谁先完成谁赢"和"全部结束再汇总"的场景。

### 生成器函数

生成器 `function*` 的类型签名是 `Generator<T, TReturn, TNext>`。异步生成器 `async function*` 返回 `AsyncGenerator`。

> 函数是 TypeScript 世界的"瑞士军刀"——小巧、灵活、功能强大。学会用好函数的类型签名，你就已经入门 TypeScript 了。
