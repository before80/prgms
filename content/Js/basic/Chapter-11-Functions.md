+++
title = "第 11 章 函数基础"
weight = 110
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 11 章 函数基础

> 函数是 JavaScript 的灵魂——没有函数的 JavaScript，就像没有调料的方便面，能吃，但总觉得少了点什么。

## 11.1 函数定义

### 函数声明：function 关键字，存在提升

函数声明是最传统的定义函数的方式，就像写简历一样正式——用 `function` 关键字，后面跟函数名（必须有）：

```javascript
// 函数声明
function greet(name) {
  return "你好，" + name + "！";
}

console.log(greet("小明")); // "你好，小明！"
```

**函数声明会被提升（hoisting）**——这意味着你可以先调用函数，再声明函数，程序依然能正常运行：

```javascript
// 可以在声明之前调用！
console.log(sayHello("world")); // "Hello, world!"

function sayHello(name) {
  return "Hello, " + name + "!";
}
```

这是因为 JavaScript 引擎在执行代码之前，会把所有函数声明"提升"到当前作用域的顶部。就像老师在你提问之前就知道答案一样，JavaScript 引擎在运行代码之前就已经"看到了"所有的函数声明。

> 💡 为什么需要提升？因为函数声明和变量声明一样，会被提升到顶部，这样我们就可以在代码中先使用后定义，符合人类"先想到要做什么，再实现"的思维方式。

---

### 函数表达式：赋值给变量，存在提升差异

函数表达式把函数当作一个**值**，赋值给变量。就像把一只猫放进盒子里，从此这只猫就叫"盒子里的猫"：

```javascript
// 函数表达式
const greet = function(name) {
  return "你好，" + name + "！";
};

console.log(greet("小红")); // "你好，小红！"
```

**关键区别：函数表达式不会被完全提升！**

```javascript
// ❌ 错误！
console.log(greet("小明")); // TypeError: greet is not a function

const greet = function(name) {
  return "你好，" + name + "！";
};
```

为什么？因为变量声明会被提升，但赋值不会！提升后的情况实际上是：

```javascript
// JavaScript 引擎看到的代码（提升后）
const greet;  // 变量声明被提升，值为 undefined
console.log(greet("小明")); // greet 还是 undefined，当然不能调用！

greet = function(name) {  // 赋值没有提升
  return "你好，" + name + "！";
};
```

**所以函数表达式必须先赋值再调用！**

```javascript
// ✅ 正确做法
const greet = function(name) {
  return "你好，" + name + "！";
};

console.log(greet("小明")); // "你好，小明！"
```

> ⚠️ 小心陷阱：函数表达式虽然变量声明会被提升，但初始值是 `undefined`，所以在赋值之前调用会报错。而函数声明是完全提升（声明和函数体都被提升），所以可以在任何位置调用。

---

### 匿名函数

顾名思义，匿名函数就是**没有名字的函数**。它通常出现在需要函数作为值的地方，比如回调函数：

```javascript
// 匿名函数作为回调
setTimeout(function() {
  console.log("三秒后打印这句话");
}, 3000);

// 匿名函数作为事件处理器
button.addEventListener("click", function(event) {
  console.log("按钮被点击了！");
});

// 匿名函数作为参数
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(function(n) {
  return n * 2;
});
console.log(doubled); // [2, 4, 6, 8, 10]
```

匿名函数的优点是简洁，缺点是调试时堆栈信息会显示为 "anonymous function"，不利于调试。所以如果一个函数需要复用，最好给它一个名字。

---

### 箭头函数：() => {}

ES6 引入了箭头函数，这是 JavaScript 函数定义的"简化版"，语法更加简洁：

```javascript
// 传统函数
const add1 = function(a, b) {
  return a + b;
};

// 箭头函数
const add2 = (a, b) => {
  return a + b;
};
```

**箭头函数的简写规则：**

1. 如果只有一个参数，可以省略括号（但参数为空时不能省略）：
```javascript
const double = x => x * 2;  // 只有一个参数，省略括号
const getRandom = () => Math.random();  // 没有参数，括号不能省
```

2. 如果函数体只有一条语句，可以省略大括号，并且隐式返回：
```javascript
const add = (a, b) => a + b;
console.log(add(1, 2)); // 3
```

3. 如果想直接返回一个对象，需要把对象用括号包起来，否则 `{}` 会被解释为函数体：
```javascript
// ❌ 错误
const createUser = (name, age) => { name: name, age: age };

// ✅ 正确
const createUser = (name, age) => ({ name: name, age: age });

// 或者更简洁
const createUser = (name, age) => ({ name, age }); // ES6 对象属性简写
```

箭头函数还有几个重要特性：
- 没有 `arguments` 对象
- `this` 词法绑定（继承外层作用域的 this）
- 不能用作构造函数（不能 new）
- 没有 `prototype` 属性

---

### 函数提升规则：函数声明完整提升，函数表达式只提升变量声明

| 类型 | 声明提升 | 赋值提升 | 调用时机 |
|------|---------|---------|---------|
| 函数声明 | ✅ 完全（函数体也提升） | N/A | 任意位置 |
| 函数表达式 | ✅ 变量声明 | ❌ 不提升 | 赋值之后 |

```javascript
// 函数声明
console.log(declared()); // "函数声明被调用" — 可以调用
function declared() {
  return "函数声明被调用";
}

// 函数表达式
console.log(expressed()); // TypeError: expressed is not a function
const expressed = function() {
  return "函数表达式被调用";
};
```

> 🎯 最佳实践：
> - 如果需要函数提升（先调用后定义），用函数声明
> - 如果想避免意外调用，用函数表达式
> - 如果用箭头函数或函数表达式给变量赋值，注意在赋值之后再调用

---

## 11.2 参数

### 形参与实参

这是两个非常重要的概念：

- **形参（Parameters）**：函数定义时的参数，就像留学中介告诉你"需要准备这些材料"——只是列出名字，并不实际占用东西。
- **实参（Arguments）**：函数调用时的参数，就像你真正去递交签证时带的那些文件——实际的材料。

```javascript
// name 和 age 是形参（参数列表）
function introduce(name, age) {
  console.log(`我是${name}，今年${age}岁`);
}

// "张三" 和 25 是实参（实际传递的值）
introduce("张三", 25); // "我是张三，今年25岁"
```

---

### 默认参数（ES6+）

ES6 之前，如果你想让参数有默认值，得这么写：

```javascript
// 传统写法：手动检查并赋值
function greet(name) {
  name = name || "陌生人";
  return "你好，" + name + "！";
}

console.log(greet());        // "你好，陌生人！"
console.log(greet("小明"));  // "你好，小明！"
```

这种写法有个问题——如果我传入 `0`、`""`、`false` 这些"假值"，默认值也会生效（因为 `0 || "陌生人"` 返回 `"陌生人"`），这可能不是我们想要的。

ES6 引入了**默认参数**：

```javascript
function greet(name = "陌生人") {
  return "你好，" + name + "！";
}

console.log(greet());        // "你好，陌生人！"
console.log(greet("小明"));  // "你好，小明！"
console.log(greet(""));      // "你好，！"（空字符串是合法的实参，不会触发默认值）
```

> 💡 默认参数只在实参为 `undefined` 时才会使用，`0`、`""`、`false` 这些假值都是合法的实参！

**多个默认参数：**

```javascript
function createUser(name, age = 18, city = "北京") {
  return { name, age, city };
}

console.log(createUser("小明"));           // { name: "小明", age: 18, city: "北京" }
console.log(createUser("小红", 20));      // { name: "小红", age: 20, city: "北京" }
console.log(createUser("小李", 25, "上海")); // { name: "小李", age: 25, city: "上海" }
```

**使用函数调用作为默认值：**

```javascript
function getDefaultName() {
  console.log("生成默认名字..."); // 只有在需要默认值时才执行
  return "匿名用户";
}

function greet(name = getDefaultName()) {
  return "你好，" + name + "！";
}

console.log(greet());        // 打印"生成默认名字..."，返回"你好，匿名用户！"
console.log(greet("小明"));   // "你好，小明！"（不触发默认函数）
```

---

### arguments 对象：类数组对象

在 ES6 之前，`arguments` 对象是访问函数参数的唯一方式。它是一个**类数组对象**（Array-like Object），长得像数组但不是数组：

```javascript
function sum() {
  console.log(arguments); // [Arguments] { '0': 1, '1': 2, '2': 3, '3': 4 }
  console.log(arguments.length); // 4
  console.log(arguments[0]); // 1
  console.log(arguments[1]); // 2
}

sum(1, 2, 3, 4);
```

**arguments 的特点：**

1. 它是类数组对象，有 `length` 属性，可以用下标访问
2. 它不是真正的数组，没有数组的方法（如 `forEach`、`map`）
3. 它只在普通函数中有效，箭头函数没有 `arguments`

```javascript
// 类数组转数组
function demo() {
  // 方法1：Array.from
  const args1 = Array.from(arguments);

  // 方法2：展开运算符
  const args2 = [...arguments];

  // 方法3：slice
  const args3 = Array.prototype.slice.call(arguments);

  console.log(args1, args2, args3); // 都是真正的数组
}
```

> ⚠️ 注意：`arguments` 已经被 ES6 的剩余参数取代了，尽量使用剩余参数 `...args` 代替！

---

### 剩余参数 ...args（ES6+）：真正的数组

ES6 引入了**剩余参数**（Rest Parameters），用 `...` 开头，可以接收不定数量的参数。它比 `arguments` 更好用，因为它是**真正的数组**：

```javascript
function sum(...numbers) {
  console.log(numbers); // [1, 2, 3, 4] — 是真正的数组！
  return numbers.reduce((a, b) => a + b, 0);
}

console.log(sum(1, 2, 3, 4)); // 10
console.log(sum(1, 2));        // 3
console.log(sum());            // 0
```

**剩余参数 vs arguments：**

| 特性 | 剩余参数 `...args` | arguments |
|------|-------------------|-----------|
| 类型 | 真正的数组 | 类数组对象 |
| 箭头函数 | 有效 | 无效 |
| 包含剩余参数之后的参数 | 是 | 否 |
| 可选参数之前的默认值 | 支持 | 不支持 |

```javascript
// 剩余参数可以和其他参数混用
function multiply(factor, ...numbers) {
  return numbers.map(n => n * factor);
}

console.log(multiply(2, 1, 2, 3, 4)); // [2, 4, 6, 8]
// factor = 2, ...numbers = [1, 2, 3, 4]
```

**解构剩余参数：**

```javascript
function parseCommand(action, ...options) {
  const [verb, target, value] = options;
  console.log(action, verb, target, value);
}

parseCommand("send", "email", "user@example.com", "Hello!");
// action = "send"
// options = ["email", "user@example.com", "Hello!"]
// verb = "email"
// target = "user@example.com"
// value = "Hello!"
```

---

## 11.3 返回值

### return 语句

`return` 语句用于指定函数的返回值。当函数遇到 `return` 时，会立即返回指定的值，并停止执行函数体内后面的代码：

```javascript
function add(a, b) {
  return a + b;
}

const result = add(1, 2);
console.log(result); // 3
```

**return 立即退出函数：**

```javascript
function process(value) {
  console.log("1. 开始处理");

  if (value < 0) {
    console.log("2. 负数处理");
    return; // 提前退出，不执行后面的代码
  }

  console.log("2. 正数处理");
  console.log("3. 结束处理");
}

process(-5);
// 输出:
// 1. 开始处理
// 2. 负数处理

process(10);
// 输出:
// 1. 开始处理
// 2. 正数处理
// 3. 结束处理
```

**return 可以返回任何值：**

```javascript
// 返回数字
function double(x) {
  return x * 2;
}

// 返回字符串
function greet(name) {
  return `Hello, ${name}!`;
}

// 返回布尔值
function isEven(n) {
  return n % 2 === 0;
}

// 返回数组
function range(start, end) {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

// 返回对象
function createPoint(x, y) {
  return { x, y };
}

// 返回函数（高阶函数）
function createMultiplier(factor) {
  return function(number) {
    return number * factor;
  };
}
```

---

### 未指定返回值时返回 undefined

如果函数没有 `return` 语句，或者 `return` 后面没有值，那么函数的返回值是 `undefined`：

```javascript
function sayHello(name) {
  console.log("你好，" + name + "！");
}

const result = sayHello("小明");
console.log(result); // undefined

// 显式返回 undefined
function sayBye(name) {
  console.log("再见，" + name + "！");
  return undefined;
}

console.log(sayBye("小红")); // undefined
```

> 💡 很多初学者会搞混 `console.log()` 和 `return`：
> - `console.log()` 只是**打印**值到控制台，不影响函数的返回值
> - `return` 是**返回**值给调用者，函数外部可以拿到这个值

```javascript
function getGreeting(name) {
  console.log("计算中..."); // 打印到控制台
  return "你好，" + name + "！"; // 返回值
}

const greeting = getGreeting("小明");
// 计算中...
// greeting 变量的值是 "你好，小明！"

console.log(greeting); // "你好，小明！"
```

---

## 11.4 箭头函数

### 简写语法：单参数省略括号 / 单行省略 return

箭头函数有几种简写形式：

```javascript
// 完整写法
const add = (a, b) => {
  return a + b;
};

// 省略括号（单参数）
const double = x => {
  return x * 2;
};

// 省略大括号和 return（单行函数体）
const add = (a, b) => a + b;
const double = x => x * 2;

// 没有任何参数
const getRandom = () => Math.random();

// 多行函数体不能省略大括号
const calculate = (a, b) => {
  const sum = a + b;
  const product = a * b;
  return sum + product;
};
```

---

### 返回对象需加括号

箭头函数返回对象时，必须用括号包起来，否则 `{}` 会被解释为函数体：

```javascript
// ❌ 错误：JS 引擎会认为 {} 是函数体
const createUser = (name, age) => { name: name, age: age };

// ✅ 正确：用括号包起来
const createUser = (name, age) => ({ name: name, age: age });

// 利用 ES6 对象属性简写
const createUser = (name, age) => ({ name, age });

console.log(createUser("小明", 18)); // { name: "小明", age: 18 }
```

---

### 无 arguments 对象

箭头函数没有 `arguments` 对象，如果你需要访问所有参数，应该使用剩余参数：

```javascript
// 普通函数：可以使用 arguments
function sum() {
  return Array.from(arguments).reduce((a, b) => a + b, 0);
}

console.log(sum(1, 2, 3)); // 6

// 箭头函数：使用剩余参数
const sumArrow = (...numbers) => {
  return numbers.reduce((a, b) => a + b, 0);
};

console.log(sumArrow(1, 2, 3)); // 6
```

---

### this 词法绑定：继承外层函数的 this

这是箭头函数最重要的特性之一！箭头函数没有自己的 `this`，它会**继承外层作用域的 `this`**：

```javascript
// 普通函数：this 指向调用者
const person = {
  name: "小明",
  sayHi: function() {
    console.log("你好，我是" + this.name);
  },
  waitAndSayHi: function() {
    setTimeout(function() {
      console.log("你好，我是" + this.name); // this 指向 window/undefined！
    }, 1000);
  }
};

person.sayHi();         // "你好，我是小明"
person.waitAndSayHi();  // "你好，我是undefined"（1秒后）
```

看看上面 `waitAndSayHi` 的问题——`setTimeout` 的回调函数是普通函数，`this` 指向 `window`（非严格模式），而 `window.name` 是空字符串！

```javascript
// 箭头函数：继承外层的 this
const person = {
  name: "小明",
  waitAndSayHi: function() {
    setTimeout(() => {
      console.log("你好，我是" + this.name); // this 指向 person！
    }, 1000);
  }
};

person.waitAndSayHi(); // "你好，我是小明"（1秒后）
```

---

### 不能用作构造函数

箭头函数没有 `prototype` 属性，也不能用 `new` 调用：

```javascript
const Person = (name, age) => {
  this.name = name;
  this.age = age;
};

// ❌ TypeError: Person is not a constructor
const p = new Person("小明", 18);

// ✅ 普通函数可以用 new
const PersonNormal = function(name, age) {
  this.name = name;
  this.age = age;
};
const p2 = new PersonNormal("小红", 20); // 正常工作
```

---

### 不能用作对象方法

虽然技术上可以在对象中定义箭头函数作为方法，但它的 `this` 不会绑定到对象：

```javascript
const calculator = {
  value: 10,
  // ❌ 箭头函数：this 不会指向 calculator
  add: (n) => this.value + n,
  // ✅ 普通函数：this 会指向 calculator
  subtract: function(n) {
    return this.value - n;
  }
};

console.log(calculator.subtract(3)); // 7
console.log(calculator.add(3));      // NaN（this.value 是 undefined）
```

---

### 普通函数 vs 箭头函数对比

| 特性 | 普通函数 | 箭头函数 |
|------|---------|---------|
| `this` | 动态绑定，取决于调用方式 | 词法绑定，继承外层 |
| `arguments` | 有 | 没有（可用 `...args`） |
| `prototype` | 有 | 没有 |
| `new` | 可以用作构造函数 | 不能 |
| 作为对象方法 | `this` 指向对象 | `this` 不指向对象 |
| 提升 | 函数声明完整提升 | 变量声明提升，赋值不提升 |
| 简写语法 | 无 | 单参数省略括号、单行省略 return |

```javascript
// 什么时候用箭头函数？
const numbers = [1, 2, 3, 4, 5];

// ✅ 适合：回调函数，不需要自己的 this
numbers.filter(n => n > 2);        // [3, 4, 5]
numbers.map(n => n * 2);           // [2, 4, 6, 8, 10]
numbers.reduce((a, b) => a + b);  // 15

// ❌ 不适合：需要动态 this 的场景
document.addEventListener("click", () => {
  // 这里的 this 不指向 document！
  console.log(this);
});

document.addEventListener("click", function() {
  // 这里的 this 指向 document
  console.log(this);
});
```

> 💡 总结：大多数情况下，箭头函数让代码更简洁。但要记住它的限制——没有自己的 `this`、`arguments`、`prototype`，不能用作构造函数。如果需要这些特性，就用普通函数。

---

## 本章小结

本章我们深入学习了 JavaScript 函数的定义和调用：

1. **函数定义方式**：函数声明（完整提升）、函数表达式（只提升变量声明）、箭头函数（简洁语法）

2. **参数**：形参与实参的区别、默认参数（ES6+）、`arguments` 对象（类数组）、剩余参数 `...args`（真正的数组）

3. **返回值**：`return` 语句、提前退出、未指定返回值时返回 `undefined`

4. **箭头函数特性**：
   - 简写语法：单参数省略括号、单行省略 return
   - 返回对象需加括号
   - 无 `arguments`（用剩余参数代替）
   - `this` 词法绑定（继承外层）
   - 不能用作构造函数
   - 不能用作对象方法

> 📊 图示：函数定义方式对比
>
> ```mermaid
> graph TD
>     A[函数定义] --> B[函数声明]
>     A --> C[函数表达式]
>     A --> D[箭头函数]
>
>     B --> B1[function 关键字]
>     B --> B2[完整提升]
>     B --> B3[有 arguments]
>
>     C --> C1[赋值给变量]
>     C --> C2[只提升变量声明]
>     C --> C3[可匿名]
>
>     D --> D1["() => {} 语法"]
>     D --> D2[this 词法绑定]
>     D --> D3[无 arguments]
>     D --> D4[不能 new]
> ```

---

**下章预告**：下一章我们将探索**作用域与闭包**——JavaScript 最神秘又最强大的特性之一！准备好了吗？ 🔮
