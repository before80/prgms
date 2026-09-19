+++
title = "第 19 章 class 语法"
weight = 190
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 19 章 class 语法

> ES6 引入了 class 语法，让 JavaScript 的面向对象编程更加直观。虽然 class 实际上是基于原型的语法糖，但它让代码更容易理解，也更容易被其他语言的程序员接受。

## 19.1 class 基础

### class 声明与 constructor

class 使用 `class` 关键字声明，`constructor` 是构造函数：

```javascript
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
    console.log("Person 实例创建：" + name);
  }

  greet() {
    console.log("你好，我是" + this.name);
  }
}

const p = new Person("小明", 18);
// 输出：Person 实例创建：小明

p.greet(); // "你好，我是小明"
console.log(p.name); // "小明"
console.log(p.age);  // 18
```

**class 声明 vs 函数声明**：

```javascript
// class 声明（不会被提升）
class Person {
  // ...
}

// 函数声明（会被提升）
function Person(name) {
  this.name = name;
}
```

> ⚠️ class 声明的「提升」和函数声明不同：它会被提升到当前作用域顶部，但**在求值前一直处于暂时性死区（TDZ）**，所以效果上等同于「不能提前使用」。在 class 定义之前访问它会报错：`ReferenceError: Cannot access 'Person' before initialization`。

还有几个和函数写法不同的硬性区别：

```javascript
class Person {}

console.log(typeof Person);   // "function"（class 本质还是函数）
// Person();                  // TypeError: Class constructor Person cannot be invoked without 'new'
// 类必须用 new 调用，不能用普通函数方式调用

// class 内部默认是严格模式，不需要写 'use strict'
```

---

### 实例方法与 static 静态方法

class 中定义的方法分为两种：

**实例方法**：需要通过实例调用，会被放到 prototype 上

```javascript
class Person {
  constructor(name) {
    this.name = name;
  }

  greet() {
    console.log("你好，我是" + this.name);
  }
}

const p = new Person("小明");
p.greet(); // 通过实例调用
console.log(p.greet === Person.prototype.greet); // true（方法在 prototype 上）
```

**static 静态方法**：通过类本身调用，不会被实例继承

```javascript
class Person {
  constructor(name) {
    this.name = name;
  }

  // 实例方法
  greet() {
    console.log("你好，我是" + this.name);
  }

  // 静态方法
  static create(name) {
    return new Person(name);
  }

  // 静态属性
  static species = "人类";
}

// 调用静态方法
const p = Person.create("小明"); // 不需要 new
console.log(Person.species); // "人类"

// 实例无法调用静态方法
console.log(p.create); // undefined
```

**静态方法的应用场景**：

```javascript
class MathUtils {
  static add(a, b) {
    return a + b;
  }

  static multiply(a, b) {
    return a * b;
  }

  static createRange(start, end) {
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  }
}

console.log(MathUtils.add(1, 2)); // 3
console.log(MathUtils.multiply(3, 4)); // 12
console.log(MathUtils.createRange(1, 5)); // [1, 2, 3, 4, 5]
```

---

### getter 与 setter

class 支持 getter 和 setter，可以像访问属性一样调用方法：

```javascript
class Rectangle {
  constructor(width, height) {
    this._width = width;
    this._height = height;
  }

  // getter
  get area() {
    return this._width * this._height;
  }

  // setter
  set width(value) {
    if (value <= 0) {
      throw new Error("宽度必须大于 0");
    }
    this._width = value;
  }

  get width() {
    return this._width;
  }
}

const rect = new Rectangle(10, 5);
console.log(rect.area); // 50（像访问属性一样，不需要 rect.area()）

rect.width = 20; // 调用 setter
console.log(rect.area); // 100

rect.width = -5; // 抛出错误：宽度必须大于 0
```

**实际应用：实现计算属性**：

```javascript
class Temperature {
  constructor(celsius) {
    this.celsius = celsius;
  }

  get fahrenheit() {
    return this.celsius * 9 / 5 + 32;
  }

  set fahrenheit(value) {
    this.celsius = (value - 32) * 5 / 9;
  }
}

const temp = new Temperature(25);
console.log(temp.celsius);    // 25
console.log(temp.fahrenheit); // 77

temp.fahrenheit = 86;
console.log(temp.celsius);    // 30
```

---

## 19.2 继承

### extends 关键字

使用 `extends` 关键字实现类继承：

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(this.name + " 发出了声音");
  }
}

class Dog extends Animal {
  // Dog 自动继承 Animal 的所有属性和方法
}

const dog = new Dog("旺财");
dog.speak(); // "旺财 发出了声音"（继承自 Animal）
```

---

### super()：调用父类构造函数

在子类的 constructor 中，必须先调用 `super()` 才能使用 `this`：

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(this.name + " 发出了声音");
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name); // 调用父类构造函数，必须在访问 this 之前
    this.breed = breed;
  }

  speak() {
    console.log(this.name + " 汪汪汪！");
  }
}

const dog = new Dog("旺财", "金毛");
dog.speak(); // "旺财 汪汪汪！"
console.log(dog.breed); // "金毛"
```

> ⚠️ 如果子类没有定义 constructor，会自动调用父类的 constructor。如果子类定义了 constructor，必须先调用 `super()`！

---

### super.xxx()：调用父类方法

可以用 `super` 调用父类的方法：

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(this.name + " 发出了声音");
  }
}

class Dog extends Animal {
  speak() {
    super.speak(); // 先调用父类的 speak
    console.log(this.name + " 然后汪汪汪！");
  }
}

const dog = new Dog("旺财");
dog.speak();
// 输出：
// 旺财 发出了声音
// 旺财 然后汪汪汪！
```

---

### 方法重写

子类可以重写父类的方法：

```javascript
class Animal {
  speak() {
    console.log("动物叫");
  }
}

class Cat extends Animal {
  speak() {
    console.log("喵喵喵！");
  }
}

class Dog extends Animal {
  speak() {
    console.log("汪汪汪！");
  }
}

new Cat().speak(); // "喵喵喵！"
new Dog().speak(); // "汪汪汪！"
new Animal().speak(); // "动物叫"
```

---

## 19.3 class 进阶

### static 静态属性（ES2022+）

ES2022 允许在 class 内部使用 `static` 关键字定义静态属性：

```javascript
class Config {
  static defaultTimeout = 3000;
  static apiUrl = "https://api.example.com";
}

console.log(Config.defaultTimeout); // 3000
console.log(Config.apiUrl); // "https://api.example.com"
```

之前的做法是在 class 定义外部添加：

```javascript
class Config {}
Config.defaultTimeout = 3000; // 在外部定义
```

---

### 私有属性：#xxx（ES2022+）

ES2022 引入了真正的私有字段，使用 `#` 开头：

```javascript
class BankAccount {
  #balance = 0; // 私有属性，外部无法访问

  constructor(initialBalance) {
    this.#balance = initialBalance;
  }

  deposit(amount) {
    if (amount <= 0) throw new Error("存款金额必须为正");
    this.#balance += amount;
  }

  withdraw(amount) {
    if (amount <= 0) throw new Error("取款金额必须为正");
    if (amount > this.#balance) throw new Error("余额不足");
    this.#balance -= amount;
  }

  getBalance() {
    return this.#balance;
  }
}

const account = new BankAccount(1000);
console.log(account.getBalance()); // 1000
account.deposit(500);
console.log(account.getBalance()); // 1500

// ❌ 外部访问私有字段会直接报语法错误（在解析阶段就被拦下，根本不会执行）
// console.log(account.#balance);
// SyntaxError: Private field '#balance' must be declared in an enclosing class

// 常见的「绕过不了」的尝试也都不成立
console.log(account["#balance"]); // undefined（不是字符串同名属性）
console.log("#balance" in account); // false
```

> 💡 私有字段是语言层面的真正私有：外部访问会报语法错误，子类也无法访问（子类里写 `this.#balance` 同样会报 `SyntaxError`）。需要子类访问时，改成 `protected` 风格的保护性方法或 Getter 暴露。

---

### 私有字段的其他实现方式

ES2022 之前，可以用一些变通方式实现私有效果：

#### 方式1：下划线约定（不真正私有）

```javascript
class Person {
  constructor(name) {
    this._name = name; // 下划线约定：外部不要直接访问
  }
}

const p = new Person("小明");
console.log(p._name); // "小明"（可以访问，但不推荐）
```

#### 方式2：WeakMap（真正私有）

```javascript
const privateData = new WeakMap();

class Person {
  constructor(name) {
    privateData.set(this, { name }); // 存储到 WeakMap
  }

  getName() {
    return privateData.get(this).name;
  }
}

const p = new Person("小明");
console.log(p.getName()); // "小明"
console.log(p.name);      // undefined（无法直接访问）
```

#### 方式3：Symbol（隐蔽但仍可被反射出来）

```javascript
const nameSymbol = Symbol("name");

class Person {
  constructor(name) {
    this[nameSymbol] = name;
  }

  getName() {
    return this[nameSymbol];
  }
}

const p = new Person("小明");
console.log(p.getName());        // "小明"
console.log(p.name);             // undefined
console.log(p[nameSymbol]);      // "小明"（只要拿到这个 Symbol 就能访问）
console.log(Object.getOwnPropertySymbols(p)); // [Symbol(name)]——能被列举出来
```

所以 Symbol 只是「不容易被误用」，不是真正的私有。除了 `#` 字段，WeakMap 是唯一能做到「外部完全拿不到」的经典方案（闭包也可以达到类似效果，但每个实例都会创建一份函数，内存开销更大）。

---

### 类字段：公有字段与私有字段（ES2022+）

> ⚠️ 先纠正一个常见混淆：**JavaScript 没有 `public`、`private`、`protected` 这三个关键字**（那是 TypeScript 的写法，编译后依然只是普通属性或约定）。JS 里只有两种：
>
> - **公有字段**：直接写名字，挂在实例上；
> - **私有字段**：名字以 `#` 开头，只能在类内部访问。

```javascript
class Person {
  // 公有字段：每个实例各有一份
  nickname = "默认名字";
  hobbies = [];          // 注意：默认值里的对象/数组会被每个实例各自创建，不会共享

  // 私有字段：只能在类内部访问
  #realName = "私有名字";

  // 静态字段：挂在类本身上
  static species = "人类";
  static #secretVersion = 3;

  get realName() {
    return this.#realName;
  }

  static describe() {
    return `${Person.species} v${Person.#secretVersion}`;
  }
}

console.log(Person.describe());  // "人类 v3"
console.log(new Person().nickname); // "默认名字"
```

字段初始化的时机可以这样记：**基类**里在构造函数体执行之前完成；**子类**里紧跟在 `super()` 返回之后、构造函数剩余代码之前完成。所有字段都是**每个实例独立求值**的，用 `[]` / `{}` 当默认值不会造成实例间共享。

---

### 静态块：static {}（ES2022+）

ES2022 支持静态初始化块，可以在 class 初始化时执行复杂逻辑：

```javascript
class MyClass {
  static config;
  static data;

  static {
    // 静态初始化块
    this.config = {
      apiUrl: "https://api.example.com",
      timeout: 5000
    };
    this.data = this.loadData();
  }

  static loadData() {
    return [1, 2, 3];
  }
}

console.log(MyClass.config); // { apiUrl: "...", timeout: 5000 }
console.log(MyClass.data);   // [1, 2, 3]
```

**应用场景**：当静态属性的初始化逻辑复杂时（需要多行代码、异常处理等），静态块比直接赋值更清晰。

---

### 类的方法放在原型上而非实例上

class 的方法定义是放在 prototype 上的，不是每个实例一份：

```javascript
class Person {
  constructor(name) {
    this.name = name;
  }

  greet() {
    console.log("你好，我是" + this.name);
  }
}

const p1 = new Person("小明");
const p2 = new Person("小红");

console.log(p1.greet === p2.greet); // true！方法是共享的
```

这与构造函数中直接定义方法的行为不同：

```javascript
function PersonOld(name) {
  this.name = name;
  this.greet = function() { // 每个实例都有自己的方法副本
    console.log("你好，我是" + this.name);
  };
}

const p1 = new PersonOld("小明");
const p2 = new PersonOld("小红");
console.log(p1.greet === p2.greet); // false！
```

> 💡 class 的方法定义方式节省内存，和原型链继承的效果一样！

---

### 子类构造函数必须先调用 super 再访问 this

```javascript
class Parent {
  constructor() {
    this.name = "Parent";
  }
}

class Child extends Parent {
  constructor() {
    // ❌ 错误：调用 super 之前访问 this
    console.log(this.name); // ReferenceError

    super();

    // ✅ 正确
    console.log(this.name); // "Parent"
  }
}
```

---

### 原型方法 vs 箭头函数字段：怎么选

类里的「普通方法」和「箭头函数字段」不是对错之分，而是两种取舍。注意下面两种写法**不能**写进同一个类里当同名成员——实例字段会遮蔽原型上的同名方法，调用时你拿到的是字段那一份：

```javascript
// 写法 A：原型方法（共享一份函数）
class PersonA {
  constructor(name) {
    this.name = name;
  }
  greet() {                      // 挂在 PersonA.prototype 上
    return "你好，我是" + this.name;
  }
}

const a1 = new PersonA("小明");
const a2 = new PersonA("小红");
console.log(a1.greet === a2.greet);   // true（同一份函数，省内存）

const lost = a1.greet;
// lost();                            // TypeError：脱离实例后 this 丢失

// 写法 B：箭头函数字段（每个实例一份，this 永远绑定实例）
class PersonB {
  constructor(name) {
    this.name = name;
  }
  greet = () => "你好，我是" + this.name;
}

const b1 = new PersonB("小明");
const b2 = new PersonB("小红");
console.log(b1.greet === b2.greet);   // false（每个实例各一份）

const safe = b1.greet;
console.log(safe());                   // "你好，我是小明"（可以直接传给别人用）
```

| | 原型方法 | 箭头函数字段 |
| --- | --- | --- |
| 函数份数 | 所有实例共享一份 | 每个实例一份 |
| 内存占用 | 小 | 实例多时更大 |
| `this` 是否会被剥离 | 会，传出去就丢 | 不会，永久绑实例 |
| 能否被 `super.method()` 调用 | 可以 | 不能（不是原型成员） |
| 适合场景 | 通用业务方法 | 事件回调、需要传出去的回调 |

实践建议：**默认用原型方法**；只有当这个函数会被当作回调传来传去（例如 `onClick={this.handleClick}`）时，才用箭头函数字段换取「不用手动 bind」的便利。

---

### instanceof 与继承链

`instanceof` 检查的是「构造函数的 `prototype` 是否出现在对象的原型链上」，所以子类实例对父类同样成立：

```javascript
class Animal {}
class Dog extends Animal {}

const dog = new Dog();

console.log(dog instanceof Dog);       // true
console.log(dog instanceof Animal);    // true（原型链上有 Animal.prototype）
console.log(dog instanceof Object);    // true（所有对象最终都到 Object.prototype）

// 真正判断「由哪个类直接创建」，看构造函数
console.log(dog.constructor === Dog);  // true

// 判断原型链关系的更精确方式
console.log(Object.getPrototypeOf(Dog.prototype) === Animal.prototype); // true

// 如果对象来自另一个 iframe / Realm，instanceof 会失效（原型不同），
// 这时改用 Array.isArray 这类自带判断，或检查 Symbol.toStringTag
```

### 继承内置类：Error 与 Array

内置类型也可以用 `extends` 继承，最常见的两个场景是自定义错误和自定义集合：

```javascript
// 1. 自定义错误类型（配合前面章节的错误处理一起用）
class ValidationError extends Error {
  constructor(message, field) {
    super(message);            // 一定要调用，否则 message / stack 不会正确设置
    this.name = "ValidationError";  // 不会自动变成类名，必须手写
    this.field = field;
  }
}

try {
  throw new ValidationError("年龄必须在 0-150 之间", "age");
} catch (err) {
  console.log(err instanceof ValidationError); // true
  console.log(err instanceof Error);           // true
  console.log(err.name, err.field);            // "ValidationError" "age"
  console.log(typeof err.stack);               // "string"
}

// 2. 继承 Array：可以给数组加上专属方法
class NumberList extends Array {
  sum() {
    return this.reduce((total, n) => total + n, 0);
  }
}

const list = NumberList.from([1, 2, 3]);
console.log(list.sum());            // 6
console.log(list instanceof NumberList); // true
console.log(Array.isArray(list));   // true
```

需要注意的是，`map`、`filter`、`slice` 这类方法会返回**子类实例**而不是普通数组，这由 `Symbol.species` 决定；如果你希望它们返回普通数组，可以显式定义：

```javascript
class NumberList2 extends Array {
  static get [Symbol.species]() {
    return Array;   // 让派生方法返回 Array 而不是 NumberList2
  }
}
console.log(NumberList2.from([1, 2]).map((n) => n).constructor === Array); // true
```

### new.target：判断函数是「被 new 调用」还是「被直接调用」

`new.target` 只在函数/构造函数内部可见：用 `new` 调用时它指向被调用的构造函数，普通调用时是 `undefined`。子类通过 `new` 调用父类时，`new.target` 是**子类**——这正是抽象基类的常用写法：

```javascript
class AbstractShape {
  constructor() {
    if (new.target === AbstractShape) {
      throw new TypeError("AbstractShape 是抽象类，不能直接实例化");
    }
    this.name = new.target.name;   // 记录实际被实例化的是哪个子类
  }
}

class Circle extends AbstractShape {}

console.log(new Circle().name);   // "Circle"
// new AbstractShape();           // TypeError: AbstractShape 是抽象类，不能直接实例化
```

`new.target` 也可以用在普通函数里，用来兼容「忘记写 `new`」的老代码：

```javascript
function Legacy(name) {
  if (!new.target) {
    return new Legacy(name);   // 忘了 new 就帮忙补上
  }
  this.name = name;
}
console.log(Legacy("小明").name);  // "小明"
```

---

## 本章小结

本章我们全面学习了 ES6+ 的 class 语法：

1. **class 基础**：
   - `class` 声明，`constructor` 构造函数
   - 实例方法 vs static 静态方法
   - getter / setter

2. **继承**：
   - `extends` 实现继承
   - `super()` 调用父类构造函数
   - `super.xxx()` 调用父类方法
   - 方法重写

3. **class 进阶**：
   - static 静态属性（ES2022+）
   - `#xxx` 私有字段（ES2022+）
   - 私有字段的实现方式（WeakMap、Symbol，以及它们的私有程度差异）
   - static 静态块（ES2022+）
   - 类的方法在 prototype 上
   - 子类构造函数必须先调用 super
   - 原型方法与箭头函数字段的取舍
   - `instanceof` 与继承链、继承内置类（Error / Array / `Symbol.species`）
   - `new.target` 判断调用方式、实现抽象基类

> 📊 图示：class 继承结构
>
> ```mermaid
> classDiagram
>     class Animal {
>       +String name
>       +speak()
>     }
>
>     class Dog {
>       +String breed
>       +speak()
>     }
>
>     class Cat {
>       +String color
>       +speak()
>     }
>
>     Animal <|-- Dog : extends
>     Animal <|-- Cat : extends
> ```

---

**🎉 到这里，JavaScript 的「核心语法」部分就告一段落了。**

从第9章到第19章，我们学习了：
- **字符串**：基础操作、查找替换、提取分割、转换格式化
- **数学与数值**：Math 对象、随机数、进制转换
- **函数**：定义、参数、返回值、箭头函数
- **作用域与闭包**：词法作用域、闭包、防抖节流
- **递归与函数式**：递归、纯函数、map/filter/reduce
- **事件循环**：同步异步、宏任务微任务
- **Promise**：状态、方法、进阶
- **async/await**：异步语法糖
- **Generator**：可暂停函数
- **原型与原型链**：继承机制
- **this 指向**：四种绑定规则
- **class 语法**：ES6 面向对象

接下来的章节会进入浏览器与服务端相关的世界：DOM 操作、事件机制、网络请求、客户端存储、正则与性能优化等。继续加油，JavaScript 大师之路就在脚下！ 🚀
