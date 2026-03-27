+++
title = "第 17 章 原型与原型链"
weight = 170
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 17 章 原型与原型链

> 原型与原型链是 JavaScript 面向对象的基石。如果你理解了原型链，就能理解"为什么 a 对象有 sayHi 方法"，就能理解 JavaScript 的继承机制。这可能是 JavaScript 中最难理解的概念之一，但也是最强大的！

## 17.1 构造函数

### 工厂函数

在 ES6 class 出现之前，工厂函数是一种创建对象的常用方式：

```javascript
function createPerson(name, age) {
  return {
    name: name,
    age: age,
    greet: function() {
      console.log("你好，我是" + this.name);
    }
  };
}

const person1 = createPerson("小明", 18);
const person2 = createPerson("小红", 20);

person1.greet(); // "你好，我是小明"
person2.greet(); // "你好，我是小红"
```

**问题**：每个对象都有一份 `greet` 方法的副本，浪费内存！

```javascript
console.log(person1.greet === person2.greet); // false（方法不是共享的）
```

---

### 构造函数：首字母大写，用 new 调用

**构造函数**（Constructor）是专门用来创建对象的函数，配合 `new` 关键字使用：

```javascript
function Person(name, age) {
  this.name = name;
  this.age = age;
  this.greet = function() {
    console.log("你好，我是" + this.name);
  };
}

const person1 = new Person("小明", 18);
const person2 = new Person("小红", 20);

person1.greet(); // "你好，我是小明"
console.log(person1 instanceof Person); // true
```

**构造函数的特点**：
- 函数名首字母大写（约定）
- 使用 `new` 关键字调用
- `this` 指向新创建的对象
- 隐式返回 `this`（如果显式返回对象，会覆盖默认返回）

```javascript
// 构造函数
function Person(name) {
  this.name = name;
  this.greet = function() {
    console.log("你好，我是" + this.name);
  };
}

const p = new Person("小明");
console.log(p); // Person { name: "小明", greet: ƒ }
```

> 💡 构造函数是 JavaScript 实现"类"的基础，虽然 JavaScript 没有真正的类（ES6 之前），但构造函数让我们可以"模拟"面向对象编程。

---

### new 关键字做了什么

`new Person(...)` 实际上做了以下事情：

```javascript
// new Person("小明") 相当于执行：
// 1. 创建一个新对象
const obj = {};

// 2. 设置原型
obj.__proto__ = Person.prototype;

// 3. 调用构造函数（并绑定 this）
Person.call(obj, "小明"); // 或者 Person.apply(obj, arguments)

// 4. 返回对象
// return obj;
```

可以用一个函数来模拟这个过程：

```javascript
function myNew(constructor, ...args) {
  // 1. 创建新对象
  const obj = {};

  // 2. 设置原型
  Object.setPrototypeOf(obj, constructor.prototype);

  // 3. 调用构造函数
  const result = constructor.apply(obj, args);

  // 4. 如果构造函数显式返回对象，就返回那个对象
  // 否则返回新创建的对象
  return typeof result === "object" && result !== null ? result : obj;
}

// 使用
function Person(name) {
  this.name = name;
}

const p = myNew(Person, "小明");
console.log(p.name); // "小明"
console.log(p instanceof Person); // true
```

---

## 17.2 原型

### prototype 属性

每个函数都有一个 `prototype` 属性，它是一个对象。这个对象的用途是： **当用这个函数作为构造函数创建对象时，该对象会共享这个 prototype 上的属性和方法**。

```javascript
function Person(name) {
  this.name = name;
}

// 在 Person.prototype 上添加方法
Person.prototype.greet = function() {
  console.log("你好，我是" + this.name);
};

Person.prototype.species = "人类";

const person1 = new Person("小明");
const person2 = new Person("小红");

console.log(person1.greet()); // "你好，我是小明"
console.log(person2.greet()); // "你好，我是小红"

console.log(person1.species); // "人类"
console.log(person2.species); // "人类"

// 验证：方法共享（同一个引用）
console.log(person1.greet === person2.greet); // true（不像工厂函数那样每个对象都有自己的方法副本！）
```

> 💡 把方法放在 prototype 上而不是构造函数内部，可以大大节省内存！

---

### 原型对象

`prototype` 指向的那个对象叫做**原型对象**。原型对象上通常会有一个 `constructor` 属性，指回构造函数：

```javascript
function Person(name) {
  this.name = name;
}

console.log(Person.prototype.constructor === Person); // true

const p = new Person("小明");
console.log(p.__proto__ === Person.prototype); // true
```

**关系图**：

```
┌─────────────────────────────────────────────────────────┐
│  Person（构造函数）                                     │
│  - prototype ────────┐                                 │
└───────────────────────┼─────────────────────────────────┘
                        ↓
              ┌─────────────────┐
              │  Person.prototype │
              │  - constructor   │──→ Person
              │  - greet         │
              │  - species       │
              └────────┬─────────┘
                       │
         ┌─────────────┴─────────────┐
         ↓                           ↓
┌─────────────────┐        ┌─────────────────┐
│   person1 实例   │        │   person2 实例   │
│  - name          │        │  - name          │
│  __proto__ ──────┼────────┼─ __proto__       │
└─────────────────┘        └─────────────────┘
```

---

### constructor 属性

每个实例（通过 `new` 创建的对象）都有 `constructor` 属性，指向创建它的构造函数：

```javascript
function Person(name) {
  this.name = name;
}

const p = new Person("小明");
console.log(p.constructor === Person); // true
console.log(p.constructor === Person.prototype.constructor); // true

// 可以用 constructor 判断类型（但不完全可靠，因为 prototype 可以被替换）
console.log(p instanceof Person); // true
```

> ⚠️ 注意：不要随意修改 prototype，否则 constructor 会失准：
> ```javascript
> Person.prototype = {}; // 这样会丢失 constructor
> p.constructor === Person; // false！
> ```

---

## 17.3 原型链

### __proto__ 与 prototype

- `prototype`：构造函数上的属性，指向原型对象
- `__proto__`：对象的属性，指向其构造函数的 prototype（即该对象的原型）

```javascript
function Person(name) {
  this.name = name;
}

Person.prototype.greet = function() {
  console.log("你好，我是" + this.name);
};

const p = new Person("小明");

console.log(p.__proto__ === Person.prototype); // true
console.log(Person.prototype.__proto__ === Object.prototype); // true
console.log(Object.prototype.__proto__); // null（原型链的终点）
```

---

### 原型链的终点：Object.prototype.__proto__ === null

原型链是有尽头的，最终指向 `null`：

```javascript
console.log(Object.prototype.__proto__); // null
console.log(Object.prototype.__proto__ === null); // true
```

完整的原型链：

```
person 对象
  ↓ __proto__
Person.prototype
  ↓ __proto__
Object.prototype
  ↓ __proto__
null
```

---

### 属性查找机制：顺着原型链向上搜索

当你访问对象的属性时，JavaScript 会沿着原型链向上查找：

```javascript
function Person(name) {
  this.name = name;
}

Person.prototype.greet = function() {
  console.log("你好，我是" + this.name);
};

Person.prototype.species = "人类";

const p = new Person("小明");

// p.name 在 p 对象本身找到
console.log(p.name); // "小明"

// p.greet 在 Person.prototype 上找到
p.greet(); // "你好，我是小明"

// p.species 也在 Person.prototype 上找到
console.log(p.species); // "人类"

// p.toString 在 Object.prototype 上找到
console.log(p.toString); // ƒ toString() { [native code] }

// p.xxx 不存在，原型链上都没有，返回 undefined
console.log(p.xxx); // undefined
```

---

### Object.getPrototypeOf()：获取对象的原型

`Object.getPrototypeOf()` 是获取对象原型的标准方法（代替 `__proto__`）：

```javascript
function Person(name) {
  this.name = name;
}

const p = new Person("小明");

console.log(Object.getPrototypeOf(p) === Person.prototype); // true
console.log(Object.getPrototypeOf(p).constructor === Person); // true
```

> 💡 推荐使用 `Object.getPrototypeOf()` 而不是直接访问 `__proto__`，因为 `__proto__` 并不是所有环境都支持的标准属性。

---

### hasOwnProperty：区分自身属性与原型属性

`hasOwnProperty` 用于检查属性是对象自身的还是从原型链继承的：

```javascript
function Person(name) {
  this.name = name; // 自身属性
}

Person.prototype.greet = function() { // 原型属性
  console.log("你好");
};

const p = new Person("小明");

console.log(p.hasOwnProperty("name")); // true（构造函数中定义的）
console.log(p.hasOwnProperty("greet")); // false（在 prototype 上定义的）
console.log(p.hasOwnProperty("toString")); // false（Object.prototype 上的）

// 可以用 for...in 遍历所有可枚举属性
for (let key in p) {
  console.log(key, p.hasOwnProperty(key) ? "(自身)" : "(原型)");
}
// name (自身)
// greet (原型)
```

---

### instanceof：检查原型链

`instanceof` 运算符用于检查对象的原型链上是否存在某个构造函数的 prototype：

```javascript
function Person(name) {
  this.name = name;
}

function Student(name, grade) {
  Person.call(this, name);
  this.grade = grade;
}

// 设置原型链继承
Student.prototype = Object.create(Person.prototype);
Student.prototype.constructor = Student;

const s = new Student("小明", 3);

console.log(s instanceof Student); // true
console.log(s instanceof Person);  // true（因为 Student.prototype.__proto__ === Person.prototype）
console.log(s instanceof Object);  // true
```

---

### 原型链的引用共享问题

原型上的属性是被所有实例**共享**的！这意味着如果你在原型上定义了一个引用类型（数组、对象），所有实例都会共享这个引用：

```javascript
function Person(name) {
  this.name = name;
}

Person.prototype.hobbies = ["编程", "阅读"]; // 引用类型！

const p1 = new Person("小明");
const p2 = new Person("小红");

console.log(p1.hobbies); // ["编程", "阅读"]
console.log(p2.hobbies); // ["编程", "阅读"]

// 修改 p1 的 hobbies
p1.hobbies.push("游戏");

console.log(p1.hobbies); // ["编程", "阅读", "游戏"]
console.log(p2.hobbies); // ["编程", "阅读", "游戏"] ← p2 也被影响了！
```

> ⚠️ 这是一个经典的陷阱！解决方法是在构造函数中定义引用类型属性：
> ```javascript
> function Person(name) {
>   this.name = name;
>   this.hobbies = []; // 在构造函数中定义，每个实例都有独立的数组
> }
> ```

---

## 17.4 继承实现

### 原型链继承

原型链继承是最基本的继承方式：

```javascript
function Parent() {
  this.name = "Parent";
}

Parent.prototype.sayHi = function() {
  console.log("你好，我是" + this.name);
};

function Child() {
  this.name = "Child";
}

// 原型链继承
Child.prototype = new Parent();
Child.prototype.constructor = Child; // 修复 constructor

const child = new Child();
child.sayHi(); // "你好，我是Child"
console.log(child instanceof Child);  // true
console.log(child instanceof Parent); // true
```

**问题**：引用类型的属性被所有实例共享。

---

### 构造函数继承（借用构造函数 / call）

借用构造函数可以解决引用类型共享问题：

```javascript
function Parent(name, hobbies) {
  this.name = name;
  this.hobbies = hobbies; // 引用类型在构造函数中定义
}

function Child(name, hobbies, grade) {
  Parent.call(this, name, hobbies); // 借用 Parent 构造函数
  this.grade = grade;
}

const child1 = new Child("小明", ["阅读"], 3);
const child2 = new Child("小红", ["音乐"], 5);

child1.hobbies.push("游戏");

console.log(child1.hobbies); // ["阅读", "游戏"]
console.log(child2.hobbies); // ["音乐"] ← 没有被影响！
```

**问题**：方法无法复用（每个实例都有一份方法副本）。

---

### 组合继承

组合继承结合原型链和构造函数继承：

```javascript
function Parent(name) {
  this.name = name;
  this.colors = ["红", "绿"];
}

Parent.prototype.sayName = function() {
  console.log(this.name);
};

function Child(name, grade) {
  Parent.call(this, name); // 继承实例属性
  this.grade = grade;
}

Child.prototype = new Parent(); // 继承原型方法
Child.prototype.constructor = Child;
Child.prototype.sayGrade = function() {
  console.log(this.grade);
};

const c1 = new Child("小明", 3);
const c2 = new Child("小红", 5);

c1.colors.push("蓝");
console.log(c1.colors); // ["红", "绿", "蓝"]
console.log(c2.colors); // ["红", "绿"]
```

---

### 原型式继承：Object.create()

`Object.create()` 创建一个新对象，使用现有对象作为新对象的原型：

```javascript
const person = {
  name: "小明",
  hobbies: ["阅读", "音乐"]
};

const p1 = Object.create(person);
const p2 = Object.create(person);

p1.name = "小红";
console.log(p1.name); // "小红"
console.log(p2.name); // "小明"（不受影响）

p1.hobbies.push("游戏");
console.log(p1.hobbies); // ["阅读", "音乐", "游戏"]
console.log(p2.hobbies); // ["阅读", "音乐", "游戏"] ← 引用类型还是共享的！
```

---

### 寄生式继承

寄生式继承在原型式继承的基础上添加额外的方法：

```javascript
function createPerson(original) {
  const clone = Object.create(original);
  clone.greet = function() {
    console.log("你好，我是" + this.name);
  };
  return clone;
}

const person = {
  name: "小明",
  age: 18
};

const p = createPerson(person);
p.greet(); // "你好，我是小明"
```

---

### 寄生组合式继承（最佳方式）

寄生组合式继承是 JavaScript 最理想的继承方式，避免了其他方式的缺点：

```javascript
function Parent(name) {
  this.name = name;
  this.colors = ["红"];
}

Parent.prototype.sayName = function() {
  console.log(this.name);
};

function Child(name, grade) {
  Parent.call(this, name); // 继承实例属性
  this.grade = grade;
}

// 寄生组合继承的关键：用 Object.create 创建 Parent.prototype 的副本
Child.prototype = Object.create(Parent.prototype);
Child.prototype.constructor = Child;
Child.prototype.sayGrade = function() {
  console.log(this.grade);
};

const c = new Child("小明", 3);
c.sayName(); // "小明"
c.sayGrade(); // 3
console.log(c instanceof Child);  // true
console.log(c instanceof Parent); // true
```

> 💡 为什么寄生组合式继承是最佳方式？
> 1. 只调用一次 Parent 构造函数
> 2. 原型链完整（instanceof 正常工作）
> 3. 原型上的 constructor 正确

---

### 六种继承方式对比

| 方式 | 优点 | 缺点 |
|------|------|------|
| 原型链继承 | 简单 | 引用类型共享 |
| 构造函数继承 | 属性独立 | 方法不复用 |
| 组合继承 | 综合优点 | 调用两次构造函数 |
| 原型式继承 | 简单 | 引用类型共享 |
| 寄生式继承 | 可扩展 | 方法不复用 |
| 寄生组合式继承 | 完美继承 | 稍复杂 |

> 💡 **推荐使用寄生组合式继承**，或者直接使用 ES6 的 `class extends`。

---

## 本章小结

本章我们深入理解了原型与原型链：

1. **构造函数**：
   - 工厂函数：简单但方法不共享
   - 构造函数：配合 `new`，`this` 指向实例
   - `new` 的执行过程

2. **原型**：
   - `prototype` 是构造函数的属性
   - `__proto__` 是对象的属性，指向原型
   - 方法放 prototype 上可共享

3. **原型链**：
   - 沿着 `__proto__` 形成链
   - 终点是 `null`
   - 属性查找沿链向上

4. **继承方式**：
   - 原型链继承
   - 构造函数继承
   - 组合继承
   - 原型式继承（Object.create）
   - 寄生式继承
   - 寄生组合式继承（最佳）

> 📊 图示：原型链结构
>
> ```mermaid
> graph TD
>     A[实例<br/>obj] -->|__proto__| B[原型<br/>Constructor.prototype]
>     B -->|constructor| C[构造函数<br/>Constructor]
>     B -->|__proto__| D[Object.prototype]
>     D -->|__proto__| E[null]
>     D -->|constructor| F[Object]
> ```

---

**下章预告**：下一章我们将学习 **this 指向**——JavaScript 中最让人困惑的话题之一！ 🔮

