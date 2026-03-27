+++
title = "第10章 类与面向对象"
weight = 100
date = "2026-03-26T21:05:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 10 章 类与面向对象

> 如果说 TypeScript 是一门语言，那类就是这门语言的"贵族血统"——它把 JavaScript 从"草根函数联盟"一下子拉到了"面向对象殿堂"。但别被唬住了，TypeScript 的类其实就是一个**带类型注解的构造函数语法糖**，理解了这一点，就没什么好怕的。

## 10.1 类的基本结构

### 10.1.1 类声明、属性声明与类型注解、构造函数、方法

TypeScript 的类和 Java/C++ 的类非常相似，但多了类型注解的加持：

```typescript
class User {
    // 属性声明 + 类型注解
    id: number;
    name: string;
    email: string;
    private _age: number; // 私有属性（下划线约定，不是语法强制）

    // 构造函数
    constructor(id: number, name: string, email: string, age: number) {
        this.id = id;
        this.name = name;
        this.email = email;
        this._age = age;
    }

    // 方法
    greet(): string {
        return `Hello, I'm ${this.name}!`;
    }

    // getter
    get age(): number {
        return this._age;
    }
}

const user = new User(1, "张三", "zhangsan@example.com", 25);
console.log(user.greet()); // Hello, I'm 张三!
console.log(user.age);     // 25
```

### 10.1.2 类的实例化

类的实例化使用 `new` 关键字：

```typescript
class Point {
    constructor(public x: number, public y: number) {
        // 参数属性：public x 自动声明并赋值，等价于上面两行
    }

    distanceTo(other: Point): number {
        return Math.sqrt((this.x - other.x) ** 2 + (this.y - other.y) ** 2);
    }
}

const p1 = new Point(0, 0);
const p2 = new Point(3, 4);

console.log(p1.distanceTo(p2)); // 5
```

---

## 10.2 访问修饰符

TypeScript 提供了三个访问修饰符：`public`、`private`、`protected`。它们控制属性和方法的**可见性**。

### 10.2.1 public：默认修饰符，任意位置可访问

`public` 是默认修饰符，可以省略：

```typescript
class Animal {
    public name: string; // 等价于 name: string
    constructor(name: string) {
        this.name = name;
    }
}

const animal = new Animal("小狗");
console.log(animal.name); // 小狗 —— public 成员可以在任何地方访问
```

### 10.2.2 private

`private` 成员只能在**类的内部**访问，类的实例和子类都无法访问。

```typescript
class BankAccount {
    public accountName: string;
    private balance: number;

    constructor(accountName: string, initialBalance: number) {
        this.accountName = accountName;
        this.balance = initialBalance;
    }

    deposit(amount: number): void {
        if (amount > 0) {
            this.balance += amount;
            console.log(`存入 ${amount}，余额: ${this.balance}`);
        }
    }

    withdraw(amount: number): void {
        if (amount > 0 && amount <= this.balance) {
            this.balance -= amount;
            console.log(`取出 ${amount}，余额: ${this.balance}`);
        } else {
            console.log("余额不足！");
        }
    }

    getBalance(): number {
        return this.balance; // 类内部可以访问 private
    }
}

const account = new BankAccount("张三", 1000);
account.deposit(500);              // 存入 500，余额: 1500
console.log(account.getBalance()); // 1500
// account.balance;                // 报错！private 成员不能在类外部访问
```

#### 10.2.2.1 为什么 TypeScript 的 private 是「编译时检查」而非「运行时保护」：JavaScript 没有真正的私有字段语法（ES2022 之前）；真正的私有字段需要用 `#field`（ES2022+）或闭包/WeakMap 模式

这里有个重要的事实：**TypeScript 的 `private` 不是真正的私有**。

TypeScript 编译成 JavaScript 后，`private` 关键字会**消失**：

```typescript
// TypeScript 源码
class Secure {
    private secret = "12345";
}

// 编译成 JavaScript 后
class Secure {
    constructor() {
        this.secret = "12345";
    }
}

const s = new Secure();
console.log(s.secret); // 可以访问！private 已经被擦除了
```

如果需要真正的私有字段，有两种方案：

**方案一：JavaScript 的 `#field` 语法（ES2022+，推荐）**

```typescript
class Secure {
    #secret = "12345"; // 真正的私有字段，编译后仍然私有

    checkPassword(pwd: string): boolean {
        return this.#secret === pwd;
    }
}

const s = new Secure();
console.log(s.checkPassword("12345")); // true
// console.log(s.#secret); // 报错！真正的私有字段，语法层面就禁止访问
```

**方案二：TypeScript 的 `private` + 闭包模式**

```typescript
// 用闭包模拟私有变量（TypeScript 早期的方法）
function createCounter() {
    let count = 0; // 这个 count 只属于 createCounter 的作用域，外部无法访问
    return {
        increment() { count++; },
        getCount() { return count; },
    };
}

const counter = createCounter();
counter.increment();
counter.increment();
console.log(counter.getCount()); // 2
// counter.count; // 报错！count 不存在于 counter 对象上
```

### 10.2.3 protected：类内部及子类可访问

`protected` 成员可以被**类本身和子类**访问，但不能被类的实例直接访问：

```typescript
class Animal {
    protected name: string;

    constructor(name: string) {
        this.name = name;
    }

    protected speak(): void {
        console.log(`${this.name} 发出了声音`);
    }
}

class Dog extends Animal {
    private breed: string;

    constructor(name: string, breed: string) {
        super(name);
        this.breed = breed;
    }

    bark(): void {
        console.log(`${this.name}（${this.breed}）汪汪叫！`);
        this.speak(); // 子类可以访问 protected 方法
    }
}

const dog = new Dog("旺财", "金毛");
// dog.name;        // 报错！protected 成员不能通过实例访问
// dog.speak();    // 报错！protected 方法不能通过实例调用
dog.bark();         // 旺财（金毛）汪汪叫！ - protected speak() 在内部被调用了
```

#### 10.2.3.1 protected 的设计动机：面向对象中「子类可见，实例不可见」的需求；这是 TS 对 OO 设计的抽象，不对应任何 JavaScript 运行时语义

`protected` 对应的是面向对象设计中的"**受保护的成员**"概念——它允许子类访问，但不允许外部随意操作。这在设计**模板方法模式**时特别有用：

```typescript
class Base {
    protected log(message: string): void {
        console.log(`[BASE] ${message}`);
    }

    public execute(): void {
        this.log("开始执行");
        this.doWork();
        this.log("执行结束");
    }

    protected doWork(): void {
        // 子类必须实现这个方法
    }
}

class Specialized extends Base {
    protected doWork(): void {
        this.log("执行专用逻辑"); // 子类可以访问 protected 方法
    }
}

const s = new Specialized();
s.execute();
// [BASE] 开始执行
// [BASE] 执行专用逻辑
// [BASE] 执行结束
```

### 10.2.4 readonly 修饰符：初始化后不可修改

`readonly` 成员只能在**声明时**或**构造函数中**赋值，之后就不能改了：

```typescript
class Config {
    readonly id: string;
    readonly createdAt: Date;

    constructor(id: string, createdAt: Date) {
        this.id = id;
        this.createdAt = createdAt;
    }
}

const config = new Config("app-001", new Date());
// config.id = "app-002"; // 报错！Cannot assign to 'id' because it is a read-only property
// config.createdAt = new Date(); // 报错！Cannot assign to 'createdAt' because it is a read-only property
```

### 10.2.5 参数属性：`constructor(public name: string, private age: number)`

TypeScript 提供了"参数属性"语法，可以一步完成属性声明 + 构造函数参数赋值：

```typescript
// 普通写法
class Person {
    public name: string;
    private age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
}

// 参数属性写法（等价）
class PersonConcise {
    constructor(
        public name: string,     // 自动声明 public name，并赋值
        private age: number,    // 自动声明 private age，并赋值
        readonly id: string,   // 自动声明 readonly id，并赋值
    ) {}
}

const p = new PersonConcise("小明", 18, "P-001");
console.log(p.name); // 小明
// p.age; // 报错！private
console.log(p.id);  // P-001
// p.id = "P-002"; // 报错！readonly
```

---

## 10.3 继承与多态

### 10.3.1 extends 关键字（单继承）

TypeScript 类只支持**单继承**——一个类只能有一个直接父类：

```typescript
class Animal {
    constructor(public name: string) {}
    move(): void {
        console.log(`${this.name} 在移动`);
    }
}

class Dog extends Animal {
    constructor(name: string, private breed: string) {
        super(name); // 调用父类构造函数
    }

    bark(): void {
        console.log(`${this.name}（${this.breed}）汪汪叫！`);
    }
}

const dog = new Dog("旺财", "金毛");
dog.move();  // 继承自 Animal
dog.bark();  // Dog 自有的方法
```

### 10.3.2 super 调用：构造函数 super()、方法 super.method()

`super` 用于调用父类的构造函数或方法：

```typescript
class Base {
    constructor(public id: number) {}
    describe(): void {
        console.log(`Base: id = ${this.id}`);
    }
}

class Extended extends Base {
    constructor(id: number, public name: string) {
        super(id); // 必须先调用 super，才能使用 this
    }

    describe(): void {
        super.describe(); // 调用父类方法
        console.log(`Extended: name = ${this.name}`);
    }
}

const e = new Extended(1, "小明");
e.describe();
// Base: id = 1
// Extended: name = 小明
```

### 10.3.3 extends vs implements

这两个关键字长得像，但含义完全不同：

- `extends`：**继承**父类的实现（代码复用）
- `implements`：**约束**类的结构（接口契约）

```typescript
// extends：继承实现
class Animal {
    speak() { console.log("动物发出声音"); }
}
class Dog extends Animal {
    speak() { console.log("汪汪"); }
}

// implements：只约束结构，不继承实现
interface Speakable {
    speak(): void;
}

class Cat implements Speakable {
    speak() { console.log("喵喵"); } // 必须实现这个方法，但没有继承任何实现代码
}
```

### 10.3.4 为什么 TypeScript 区分 extends 和 implements

#### 10.3.4.1 这反映了「继承 vs 组合」的设计哲学——TS 鼓励组合而非继承

这是面向对象设计中的经典话题：**组合优先于继承**（Composition over Inheritance）。

**继承的问题**：
```typescript
class Animal { /* ... */ }
class FlyingAnimal extends Animal { fly() {} }
class Bird extends FlyingAnimal { /* 鸟 */ }
class Bat extends FlyingAnimal { /* 蝙蝠 */ }
class Ostrich extends FlyingAnimal { /* 鸵鸟 */ } // 鸵鸟不能飞！但被迫继承了 fly()
```

**组合的解法**：
```typescript
interface CanFly { fly(): void; }

class Bird implements CanFly { fly() { console.log("鸟儿飞翔"); } }
class Ostrich { fly() { throw new Error("鸵鸟不会飞！"); } } // 没有被迫继承
```

TypeScript 用 `extends` 和 `implements` 的区分，明确告诉你：**能用接口约束，就别用继承**。

### 10.3.5 方法重写（Override）

子类可以**重写**（override）父类的方法。

#### 10.3.5.1 子类方法签名兼容规则：返回值类型协变（子类型允许返回更具体的类型），参数类型逆变（子类允许接受更宽泛的参数）；这是里氏替换原则（Liskov Substitution Principle）在 TS 类型系统中的体现

里氏替换原则（LSP）是面向对象设计的基石之一。它的核心思想是：**子类对象可以替换父类对象，而不改变程序的正确性**。

```typescript
class Animal {
    speak(): Animal {
        console.log("动物叫");
        return this;
    }
}

class Dog extends Animal {
    // 协变：子类的返回类型可以是更具体的 Dog
    speak(): Dog {
        console.log("汪汪");
        return this;
    }
}

function makeSpeak(animal: Animal): void {
    animal.speak(); // 期望返回 Animal，实际可能返回 Dog —— 这是协变，OK
}

const dog = new Dog();
makeSpeak(dog); // 正常工作 —— Dog 可以替换 Animal
```

**协变**：子类方法的返回值类型可以是父类方法返回值类型的**子类型**（更具体）。

**逆变**：子类方法的参数类型可以是父类方法参数类型的**父类型**（更宽泛）。

```typescript
class Animal { name: string = "动物"; }
class Dog extends Animal { breed: string = "狗"; }

function handleAnimal(a: Animal): void {
    console.log(a.name);
}

function handleDog(d: Dog): void { // 逆变：参数可以是更宽泛的 Animal
    console.log(d.name, (d as Animal).name);
}

// 逆变：fn 的参数是 Dog（窄），handleAnimal 接受 Animal（宽）
// 我们把宽的赋值给窄的 —— 合法，因为调用 fn 时只会用到 Dog 的属性
const fn: (a: Dog) => void = handleAnimal; // OK！
// const fn2: (a: Animal) => void = handleDog; // 报错！fn2 的参数是 Animal（宽），handleDog 只认识 Dog（窄）
```

#### 10.3.5.2 noImplicitOverride

TypeScript 4.3 引入了 `noImplicitOverride` 选项。当你打开它时，如果子类要重写父类方法，**必须显式使用 `override` 关键字**：

```typescript
// tsconfig.json: { "noImplicitOverride": true }

class Base {
    method(): void { console.log("Base"); }
}

class Derived extends Base {
    override method(): void { // 不加 override 会报错
        super.method();
        console.log("Derived");
    }
}
```

这个选项的价值在于：**防止父类新增方法时，子类意外覆盖**。

#### 10.3.5.3 子类覆盖父类方法时必须使用 override 关键字（TS 4.3+），防止父类新增方法时子类意外覆盖

这是因为 TypeScript 的类方法默认是"开放"的——子类可以定义和父类同名的方法，不加任何关键字。

```typescript
// 不开 noImplicitOverride 的隐患
class Parent {
    method() { console.log("Parent"); }
}

class Child extends Parent {
    helper() { console.log("Child"); } // 本意是新增一个方法
    method() { console.log("Child"); } // 本意是新增一个方法 —— 但编译器认为这是 override
}
```

---

## 10.4 抽象类与抽象方法

### 10.4.1 abstract 修饰符：抽象类不可直接实例化，抽象方法子类必须实现

**抽象类**是"不完整的类"——它定义了接口规范，但自己不提供完整实现。抽象类**不能直接实例化**，只能被继承。

```typescript
// 抽象类
abstract class Shape {
    abstract getArea(): number; // 抽象方法：没有实现，只有签名
    abstract getPerimeter(): number;

    // 抽象类可以提供完整实现的方法
    describe(): void {
        console.log(`面积: ${this.getArea()}, 周长: ${this.getPerimeter()}`);
    }
}

// 抽象类的子类必须实现所有抽象方法
class Circle extends Shape {
    constructor(public radius: number) {
        super();
    }

    getArea(): number {
        return Math.PI * this.radius ** 2;
    }

    getPerimeter(): number {
        return 2 * Math.PI * this.radius;
    }
}

class Rectangle extends Shape {
    constructor(public width: number, public height: number) {
        super();
    }

    getArea(): number {
        return this.width * this.height;
    }

    getPerimeter(): number {
        return 2 * (this.width + this.height);
    }
}

const shapes: Shape[] = [new Circle(5), new Rectangle(4, 6)];
shapes.forEach((s) => s.describe());
// 面积: 78.53981633974483, 周长: 31.41592653589793
// 面积: 24, 周长: 20
```

### 10.4.2 抽象类的设计动机

#### 10.4.2.1 抽象类 = 「不能直接实例化，只能被继承」的限制；这是 TS 对 OO 设计中「模板方法模式」的类型层面支持

抽象类的核心价值是**模板方法模式**（Template Method Pattern）——父类定义算法的骨架（骨架中的某些步骤由子类实现）：

```typescript
abstract class DataProcessor {
    // 模板方法：定义处理数据的完整流程
    process(data: string[]): string[] {
        const validated = this.validate(data);
        const cleaned = this.clean(validated);
        return this.transform(cleaned);
    }

    abstract validate(data: string[]): string[]; // 子类实现
    abstract clean(data: string[]): string[];   // 子类实现
    abstract transform(data: string[]): string[]; // 子类实现
}

class NumberProcessor extends DataProcessor {
    validate(data: string[]): string[] {
        return data.filter((s) => !isNaN(Number(s)));
    }

    clean(data: string[]): string[] {
        return data.map((s) => s.trim());
    }

    transform(data: string[]): string[] {
        return data.map((s) => String(Number(s) * 2));
    }
}

const processor = new NumberProcessor();
console.log(processor.process(["  1  ", "2", "abc", "  4  "]));
// ["2", "4", "8"]
```

---

## 10.5 getter、setter 与静态成员

### 10.5.1 getter / setter 的声明与类型注解

Getter 和 Setter 让你用"属性访问"的语法，调用"方法执行"的逻辑：

```typescript
class BankAccount {
    private _balance: number = 0;

    // getter
    get balance(): number {
        return this._balance;
    }

    // setter
    set balance(value: number) {
        if (value < 0) {
            throw new Error("余额不能为负数！");
        }
        this._balance = value;
    }

    deposit(amount: number): void {
        this._balance += amount;
    }
}

const account = new BankAccount();
account.deposit(1000);
console.log(account.balance); // 1000（触发 getter）
account.balance = 500;        // 触发 setter
console.log(account.balance); // 500
// account.balance = -100;    // 报错！throw new Error("余额不能为负数！")
```

### 10.5.2 静态属性与静态方法

**静态成员**属于类本身，而不是类的实例：

```typescript
class MathUtils {
    static PI: number = 3.14159; // 静态属性：类本身的属性

    static circleArea(radius: number): number {
        // 静态方法：不需要实例化就能调用
        return this.PI * radius ** 2;
    }
}

console.log(MathUtils.PI);          // 3.14159 —— 通过类本身访问
console.log(MathUtils.circleArea(5)); // 78.53975 —— 不需要 new MathUtils()
```

---

## 10.6 结构化类型系统与类的兼容性

### 10.6.1 结构化类型 vs 名义类型

这是 TypeScript 类型系统的核心概念之一。

#### 10.6.1.1 TypeScript 使用结构化类型：只要结构相同即可兼容

**结构化类型**（Structural Typing）的含义是：**类型的兼容性由结构决定，而不是名字决定**。只要两个类型的"形状"相同，它们就是兼容的。

```typescript
interface Point2D {
    x: number;
    y: number;
}

class CreativePoint {
    constructor(public x: number, public y: number) {}
}

function render(point: Point2D): void {
    console.log(`(${point.x}, ${point.y})`);
}

const cp = new CreativePoint(10, 20);
render(cp); // OK！CreativePoint 有 x 和 y，结构兼容 Point2D
```

#### 10.6.1.2 为什么 TypeScript 用结构化类型：JavaScript 本身是结构化的，对象没有类声明，只有属性集合

JavaScript 是一门"鸭子类型"语言——"如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子"。TypeScript 继承了这个哲学。

在 JavaScript 中，对象就是"属性的集合"，没有"类型声明"这种东西。你可以把任意对象传给任意函数，只要它有需要的属性。

```javascript
// JavaScript 的"鸭子类型"
const point = { x: 1, y: 2, name: "origin" };
function render(p) { console.log(p.x, p.y); }
render(point); // 完全 OK，多余的 name 属性被忽略了
```

TypeScript 的结构化类型完美匹配了 JavaScript 的这种动态特性。

### 10.6.2 类的类型兼容性

#### 10.6.2.1 私有成员影响兼容性：若父类包含 private 或 protected 成员，子类必须是同一个类（或继承自同一个父类）才能兼容

```typescript
class A {
    private secret = "A的秘密";
    x: number = 1;
}

class B {
    private secret = "B的秘密"; // 和 A 的 secret 不同
    x: number = 1;
}

function useA(a: A): void {
    console.log(a.x);
}

const b = new B();
useA(b); // 报错！即使 B 也有 x: number，但 B 有 private secret，和 A 不兼容
```

#### 10.6.2.2 静态成员不参与实例类型兼容性检查（静态成员属于类本身，不属于实例）

```typescript
class Base {
    static count: number = 0;
    x: number = 1;
}

class Derived extends Base {
    static count: number = 100;
    y: number = 2;
}

function useBase(b: Base): void {
    console.log(b.x);
}

const derived = new Derived();
useBase(derived); // OK！Derived 实例兼容 Base 类型
// 静态成员 count 在这个检查中完全不参与 —— 它属于类，不属于实例
```

---

## 本章小结

本章涵盖了 TypeScript 类的所有核心概念。

### 访问修饰符

- `public`：默认修饰符，任意位置可访问
- `protected`：类内部及子类可访问
- `private`：仅类内部可访问（编译时检查，不是运行时保护）
- `readonly`：初始化后不可修改

### 继承与多态

- `extends`：单继承，复用父类实现
- `implements`：约束类结构，不复用实现
- `override`（TS 4.3+）：显式标记方法重写，配合 `noImplicitOverride` 使用
- 里氏替换原则：协变返回类型，逆变参数类型

### 抽象类

抽象类不能实例化，用于定义"模板方法模式"。子类必须实现所有抽象方法。

### 结构化类型系统

TypeScript 使用结构化类型——类型兼容性由结构决定。JavaScript 的鸭子类型哲学决定了这一点：对象只有属性，没有类型声明。

### 重要区分

- `extends`（继承实现）vs `implements`（约束结构）
- `private`（编译时检查）vs `#field`（运行时保护）
- 实例成员 vs 静态成员（静态成员不参与实例兼容性检查）

> 类是 TypeScript 面向对象编程的基石。但记住：组合优于继承，接口优于抽象类——别让"类"成为你代码的枷锁。
