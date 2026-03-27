+++
title = "第9章 泛型"
weight = 90
date = "2026-03-26T21:05:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 9 章 泛型

> 泛型——Generics，英文直译是"通用类型"。但这个名字起得有点误导，因为它不是"通用万能"，而是"模具通用"。就像一个月饼模具，你可以用它做莲蓉月饼、豆沙月饼、五仁月饼——模具本身没变，但产出的月饼馅料各不相同。泛型就是 TypeScript 世界里的"月饼模具"。

## 9.1 泛型基础

### 9.1.1 泛型的目的：代码复用 + 类型安全

在 TypeScript 的世界里，泛型的价值可以用一句话概括：**一份代码，多种类型，类型安全一个不少。**

想象没有泛型的日子：

```typescript
// 没有泛型，你要为每种类型写一个函数
function identityString(arg: string): string { return arg; }
function identityNumber(arg: number): number { return arg; }
function identityBoolean(arg: boolean): boolean { return arg; }
// ... 无穷无尽的重复
```

有了泛型：

```typescript
// 一份代码，所有类型通吃
function identity<T>(arg: T): T { return arg; }

const s = identity("hello"); // T = string
const n = identity(42);      // T = number
const b = identity(true);    // T = boolean
```

这就是泛型的魔力——**DRY 原则在类型系统中的完美实践**。

### 9.1.2 泛型函数、泛型接口、泛型类、泛型类型别名

泛型不只可以用在函数上，还可以用在接口、类、类型别名上。

**泛型函数**：

```typescript
function merge<T, U>(obj1: T, obj2: U): T & U {
    return { ...obj1, ...obj2 };
}

const merged = merge({ name: "张三" }, { age: 25 });
console.log(merged); // { name: '张三', age: 25 }
```

**泛型接口**：

```typescript
interface Container<T> {
    value: T;
    getValue(): T;
    setValue(newValue: T): void;
}

const stringContainer: Container<string> = {
    value: "Hello",
    getValue() { return this.value; },
    setValue(newValue: string) { this.value = newValue; },
};

console.log(stringContainer.getValue()); // Hello
```

**泛型类**：

```typescript
class Box<T> {
    private content: T;

    constructor(initial: T) {
        this.content = initial;
    }

    get(): T {
        return this.content;
    }

    set(value: T): void {
        this.content = value;
    }
}

const numberBox = new Box<number>(100);
const stringBox = new Box<string>("TypeScript");

console.log(numberBox.get()); // 100
console.log(stringBox.get());  // TypeScript
```

**泛型类型别名**：

```typescript
type Pair<T, U> = {
    first: T;
    second: U;
};

type StringNumberPair = Pair<string, number>;
// { first: string; second: number }
```

### 9.1.3 泛型参数的默认值：`<T = string>`

泛型参数可以有默认值，当调用时没有显式指定且 TypeScript 推断不出类型时，就用默认值：

```typescript
function wrap<T = string>(value: T): { data: T } {
    return { data: value };
}

const a = wrap("hello");     // T = string（推断）
const b = wrap(42);          // T = number（推断）
const c = wrap();             // T = string（默认值）
const d = wrap<number>();     // T = number（显式指定）

console.log(a); // { data: 'hello' }
console.log(c); // { data: 'hello' }
console.log(d); // { data: 0 }
```

---

## 9.2 泛型约束

### 9.2.1 extends 约束：`<T extends { length: number }>`

有时候，泛型参数 T 可以是任意类型，但我们需要在函数内部访问它的某些属性。这时候就需要用 `extends` 来**约束** T：

```typescript
function logLength<T extends { length: number }>(arg: T): T {
    console.log(`长度为: ${arg.length}`);
    return arg;
}

logLength("hello");    // 字符串有 length 属性: 5
logLength([1, 2, 3]); // 数组有 length 属性: 3
logLength({ length: 10 }); // 普通对象也可以: 10
// logLength(123); // 报错！number 没有 length 属性
```

### 9.2.2 为什么泛型约束用 `extends`（继承）关键字

#### 9.2.2.1 `extends` 在这里不是「继承」而是「约束上限」——「T 必须是可赋值给 U 的类型」；更接近数学中的「属于」符号

`extends` 在泛型约束中的含义容易让人混淆。让我们来解构一下：

```typescript
<T extends U>
```

这里的 `extends` 意思是："T **必须兼容于** U"——换句话说，"T 必须是 U 的子类型"。

这和类继承的 `extends` 不同：
- `class Dog extends Animal`：**Dog 继承 Animal 的实现**（代码复用）
- `<T extends Animal>`：**T 必须是 Animal 的子类型**（类型约束）

```typescript
// 类继承
class Animal { eat() {} }
class Dog extends Animal { bark() {} } // Dog 复用 Animal 的 eat()，还多了 bark()

// 泛型约束
interface Animal { eat(): void; }
function feed<T extends Animal>(animal: T) {
    animal.eat(); // T 可能是 Dog/Bird/Cat...，但它们都有 eat()
}
```

### 9.2.3 keyof 与泛型约束：`<K extends keyof T>`

这是最常见的泛型约束模式之一：

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user = { id: 1, name: "张三", email: "zhangsan@example.com" };

// K 被约束为 keyof T，即 "id" | "name" | "email"
// getProperty(user, "id") → T[K] = T["id"] = number
// getProperty(user, "name") → T[K] = T["name"] = string

console.log(getProperty(user, "id"));    // 1
console.log(getProperty(user, "name")); // 张三
// getProperty(user, "password"); // 报错！"password" 不是 user 的键
```

### 9.2.4 多重约束：`T extends A & B`

一个泛型参数可以同时满足多个约束，用 `&` 连接：

```typescript
interface Printable {
    print(): void;
}

interface Serializable {
    serialize(): string;
}

// T 必须同时满足 Printable 和 Serializable
function process<T extends Printable & Serializable>(obj: T): string {
    obj.print(); // T 有 print 方法
    return obj.serialize(); // T 有 serialize 方法
}
```

### 9.2.5 无约束泛型的行为

#### 9.2.5.1 无约束泛型参数未实例化时，其类型在类型检查期间保持为泛型参数；编译器根据调用参数推断具体类型，而非默认隐式 any

这是一个容易踩坑的地方：

```typescript
function identity<T>(arg: T): T {
    // 在这个函数内部，T 是一个"未知但具体"的类型
    // 不是 any！TypeScript 在这里知道 T 是某种类型，只是不确定是哪种
    return arg;
}

const x = identity(42); // T = number，不是 any
const y = identity("s"); // T = string，不是 any
```

#### 9.2.5.2 关闭 noImplicitAny 时若无法推断才会退化为 any

```typescript
// 如果 TypeScript 实在推断不出 T，且没有显式指定
// 那么在某些情况下会退化为 any（取决于配置）
function wrapper<T>(value: T = undefined) { // T 可能退化为 any
    return value;
}
```

**最佳实践**：始终给泛型函数足够的类型信息，让 TypeScript 推断出具体的 T，而不是依赖隐式 any。

---

## 9.3 泛型进阶

### 9.3.1 条件类型与泛型：`type IsArray<T> = T extends any[] ? true : false`

泛型和条件类型是天作之合——条件类型根据泛型参数的具体类型决定返回类型：

```typescript
type IsArray<T> = T extends any[] ? true : false;

type A = IsArray<string[]>; // true
type B = IsArray<string>;    // false
type C = IsArray<number[]>;  // true
```

### 9.3.2 映射类型与泛型组合

映射类型本身就是泛型的典型应用场景：

```typescript
// 深度只读：把 T 的所有嵌套属性都变成 readonly
type DeepReadonly<T> = T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

type Config = {
    server: {
        host: string;
        port: number;
    };
    db: {
        url: string;
    };
};

type ImmutableConfig = DeepReadonly<Config>;
// {
//   readonly server: {
//     readonly host: string;
//     readonly port: number;
//   };
//   readonly db: {
//     readonly url: string;
//   };
// }
```

### 9.3.3 递归泛型：树结构、JSON 类型的递归定义

递归泛型用于定义树结构、JSON 等嵌套数据类型：

```typescript
// 二叉树节点
type TreeNode<T> = {
    value: T;
    left?: TreeNode<T>;
    right?: TreeNode<T>;
};

// JSON 类型定义（参考自 type-fest）
type JSONScalar = string | number | boolean | null;
type JSONValue = JSONScalar | JSONValue[] | { [key: string]: JSONValue };
type JSONObject = { [key: string]: JSONValue };

const tree: TreeNode<number> = {
    value: 1,
    left: { value: 2, left: { value: 4 }, right: { value: 5 } },
    right: { value: 3 },
};

function sumTree(node: TreeNode<number>): number {
    let total = node.value;
    if (node.left) total += sumTree(node.left);
    if (node.right) total += sumTree(node.right);
    return total;
}

console.log(sumTree(tree)); // 15 (1+2+4+5+3)
```

### 9.3.4 泛型与设计模式

#### 9.3.4.1 Option/Maybe：`<T> = T | undefined | null`

Option/Maybe 模式用于表示"可能有值，也可能没有"的情况：

```typescript
type Option<T> = T | undefined | null;

// 或者更严格一点，用 undefined 表示"缺失"
type Maybe<T> = T | null;

function findUser(id: number): Maybe<User> {
    const users = new Map([[1, { id: 1, name: "张三" }]]);
    return users.get(id) ?? null; // 找不到返回 null
}

const user = findUser(1);
if (user !== null) {
    console.log(user.name); // OK! user 是 User，不是 null
}
```

#### 9.3.4.2 Result/Either：`Result<T, E> = { ok: true; value: T } | { ok: false; error: E }`

Result 模式用于表示"可能成功，也可能失败"的计算结果：

```typescript
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
    if (b === 0) {
        return { ok: false, error: "除数不能为0" };
    }
    return { ok: true, value: a / b };
}

const result = divide(10, 2);
if (result.ok) {
    console.log(`结果是 ${result.value}`); // 结果是 5
} else {
    console.log(`出错了: ${result.error}`); // 不执行
}

const badResult = divide(10, 0);
if (badResult.ok) {
    console.log(`结果是 ${badResult.value}`); // 不执行
} else {
    console.log(`出错了: ${badResult.error}`); // 出错了: 除数不能为0
}
```

### 9.3.5 为什么 Result 类型重要

#### 9.3.5.1 JavaScript 没有异常处理之外的错误传播机制；Result 类型让错误成为类型系统的第一等公民，强迫调用方处理错误

JavaScript 的错误处理有两种方式：
1. **异常**（throw/catch）
2. **返回值**（return 某个值）

但异常的问题是：**调用方可能忘记 catch**——TypeScript 不会强制你处理。

```typescript
// 用异常的代码
function risky() { throw new Error("炸了"); }
// 调用方可能忘记 try/catch，错误悄悄向上蔓延
risky(); // 如果不 catch，整个程序崩溃

// 用 Result 的代码
function safe(): Result<number, string> { /* ... */ }
// 调用方必须检查 result.ok，否则 TypeScript 会在使用 value 时报错
const r = safe();
console.log(r.value); // 报错！Object is possibly '{ ok: false; error: string; }'
```

Result 模式的本质是：**把"可能失败"变成类型系统的显式契约**——调用方必须处理失败分支，无法假装失败不存在。

---

## 本章小结

本章是 TypeScript 泛型的全面指南，从基础到进阶，层层递进。

### 泛型的本质

泛型不是"万能类型"，而是"类型参数化"——让函数/接口/类/类型别名在**定义时**使用占位符，在**调用时**才确定具体类型。这实现了**一份代码、多种类型、类型安全**的三角目标。

### 泛型约束

`<T extends U>` 是泛型约束的核心语法。`extends` 在这里是"约束"而非"继承"，意思是"T 必须是 U 的子类型"。常见的约束包括：
- `<T extends { length: number }>`：约束必须有 length 属性
- `<K extends keyof T>`：约束 K 必须是 T 的键
- `<T extends A & B>`：多重约束

### 泛型与类型运算

泛型可以和条件类型、映射类型组合出强大的类型操作：递归泛型可以处理树结构和 JSON 类型；映射类型本身就是一个泛型工具。

### 泛型设计模式

**Option/Maybe** 模式把"可能为空"变成显式类型；**Result/Either** 模式把"可能失败"变成显式契约。两者都是函数式编程的核心理念，让错误处理从"运行时惊喜"变成"编译期已知"。

> 泛型是 TypeScript 的"内功"——学会它，你就能写出既灵活又类型安全的代码；不会它，你永远只能在 any 的泥潭里打滚。
