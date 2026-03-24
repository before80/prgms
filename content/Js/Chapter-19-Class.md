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

> ⚠️ class 声明不会被提升，这一点和函数表达式类似。如果你尝试在 class 定义之前使用它，会报错：`ReferenceError: Cannot access 'Person' before initialization`。

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
console.log(account.#balance);    // SyntaxError: Private field '#balance' must be declared
account.deposit(500);
console.log(account.getBalance()); // 1500
```

> 💡 私有属性是真正的私有，外部无法访问，即使是子类也无法访问！

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

#### 方式3：Symbol（真正私有）

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
console.log(p[nameSymbol]);      // "小明"（如果知道 Symbol，可以访问）
```

---

### 类字段：public / private / protected（ES2022+）

ES2022 正式支持在 class 字段声明时使用 `public` 或 `private` 关键字：

```javascript
class Person {
  publicName = "默认名字"; // 公有字段
  #privateName = "私有名字"; // 私有字段

  static publicSpecies = "人类"; // 公有静态字段
  static #privateSpecies = "智人"; // 私有静态字段
}
```

虽然语法上是类字段，但实际上相当于在 constructor 中 `this.publicName = "默认名字"`。

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

### 箭头函数不能作为类方法

```javascript
class Person {
  name = "小明";

  // ❌ 箭头函数作为类字段
  greet = () => {
    console.log("你好，我是" + this.name);
  };

  // ✅ 普通方法
  greet() {
    console.log("你好，我是" + this.name);
  }
}

const p = new Person();
p.greet(); // 普通方法：this 指向实例
```

箭头函数作为类字段时，它会在每次创建实例时创建一个新的函数，而不是放在 prototype 上。**这种写法虽然可以工作，但不推荐**。

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
   - 私有字段的实现方式（WeakMap、Symbol）
   - static 静态块（ES2022+）
   - 类的方法在 prototype 上
   - 子类构造函数必须先调用 super

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

**🎉 恭喜！你已经完成了 JavaScript 核心教程的全部章节！**

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

继续加油，JavaScript 大师之路就在脚下！ 🚀

