+++
title = "第 12 章 作用域与闭包"
weight = 120
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 12 章 作用域与闭包

> 作用域和闭包是 JavaScript 最核心的概念之一。理解了它们，你就能理解为什么某些变量"莫名其妙"还存在，为什么某些函数能"记住"创建时的环境。这就像是 JavaScript 给函数施了魔法，让它们有了记忆。

## 12.1 作用域

**作用域**（Scope）决定了代码中变量和函数的可见性——换句话说，就是"谁能看见谁"的问题。

想象一下，你在一栋大楼里工作：
- 你在公司（全局作用域）能看到所有楼层
- 你在3楼（函数作用域）只能看到3楼的东西
- 你在会议室（块级作用域）出了会议室就看不见会议室里贴的便签

---

### 全局作用域

全局作用域是最外层的 scope，在浏览器环境中 `window` 对象就是全局作用域，在 Node.js 中是 `global`。

```javascript
// 全局变量
const globalVariable = "我在全局都能看到！";

function test() {
  // 函数内部可以访问全局变量
  console.log(globalVariable); // "我在全局都能看到！"
}

test();
console.log(globalVariable); // "我在全局都能看到！"
```

**尽量避免在全局作用域中定义过多变量！** 原因：
1. 命名冲突：两个文件都定义了 `count` 变量，后面的会覆盖前面的
2. 难以追踪：bug 不知道是哪个文件引入的
3. 内存泄漏：全局变量不会被垃圾回收

---

### 函数作用域

在函数内部定义的变量只在该函数内部可见，这就是**函数作用域**。

```javascript
function greet() {
  const message = "你好！";
  console.log(message); // "你好！"
}

greet();
console.log(message); // ReferenceError: message is not defined
```

函数内部可以访问外部变量：

```javascript
const name = "全局的小明";

function greet() {
  const greeting = "你好，" + name;
  console.log(greeting); // "你好，全局的小明"
}

greet();
```

但函数外部无法访问函数内部的变量：

```javascript
function createCounter() {
  let count = 0; // 这是函数内部的变量
  count++;
  console.log(count);
}

createCounter(); // 1
createCounter(); // 1（每次都是新的 count，重新从 0 开始）
console.log(count); // ReferenceError: count is not defined
```

---

### 块级作用域（let / const）

ES6 引入了 `let` 和 `const`，它们具有**块级作用域**（Block Scope）——大括号 `{}` 内的区域就是一个块。

```javascript
if (true) {
  let blockVar = "我在 if 块里面";
  const constBlockVar = "我也是块级作用域";
  console.log(blockVar); // "我在 if 块里面"
}

console.log(blockVar); // ReferenceError: blockVar is not defined
console.log(constBlockVar); // ReferenceError: constBlockVar is not defined
```

**`var` vs `let` vs `const`：**

| 特性 | `var` | `let` | `const` |
|------|-------|-------|---------|
| 作用域 | 函数作用域 | 块级作用域 | 块级作用域 |
| 提升 | 提升（undefined） | 提升（暂时性死区） | 提升（暂时性死区） |
| 重复声明 | 允许 | 不允许 | 不允许 |
| 重新赋值 | 可以 | 可以 | 不可以 |

```javascript
// var 的函数作用域问题
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 输出：3, 3, 3（因为 var 是函数作用域，i 是共享的）

// let 的块级作用域问题
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100);
}
// 输出：0, 1, 2（因为 let 是块级作用域，每次循环都是新的 j）
```

> 💡 强烈建议：**始终使用 `const` 或 `let`**，避免使用 `var`！块级作用域让代码更容易理解和预测。

---

### 词法作用域（静态作用域）：由定义位置决定

JavaScript 采用**词法作用域**（Lexical Scope），也叫静态作用域。这意味着变量的作用域是由**源代码中的位置**决定的，而不是由调用位置决定的。

```javascript
const a = 1;

function outer() {
  const b = 2;

  function inner() {
    const c = 3;
    console.log(a, b, c); // 1, 2, 3
  }

  inner();
  console.log(c); // ReferenceError: c is not defined
}

outer();
```

在上面的例子中：
- `inner` 函数定义在 `outer` 函数内部，所以 `inner` 可以访问 `outer` 中的变量 `b`
- `outer` 函数定义在全局环境中，所以 `outer` 可以访问全局变量 `a`
- `inner` 可以访问 `c`，但 `outer` 不能，因为 `c` 在 `inner` 内部

**词法作用域 vs 动态作用域：**

JavaScript 是词法作用域（静态作用域），而 Shell 脚本语言（如 Bash）是动态作用域。

```javascript
const a = 1;

function foo() {
  console.log(a);
}

function bar() {
  const a = 2;
  foo(); // 在 JavaScript 中，打印 1（词法作用域，看定义位置）
}

bar(); // JavaScript: 1
       // 动态作用域语言: 2（看调用位置）
```

> 📊 图示：词法作用域示例
>
> ```mermaid
> graph TD
>     A[全局作用域<br/>a = 1] --> B[outer 函数作用域<br/>b = 2]
>     B --> C[inner 函数作用域<br/>c = 3]
>
>     C -->|可以访问| A
>     C -->|可以访问| B
>     B -->|可以访问| A
>     B -->|不能访问| C
>     A -->|不能访问| B
>     A -->|不能访问| C
> ```

---

## 12.2 闭包

### 闭包的概念：函数能访问其创建时的词法环境

**闭包**（Closure）是 JavaScript 最强大又最神秘的概念之一。简单来说，**闭包 = 函数 + 函数创建时的词法环境**。

一个函数能够记住并访问它创建时所在的词法作用域，即使这个函数在别的地方被调用，这种现象就叫做闭包。

```javascript
function createGreeter() {
  const greeting = "你好";

  function greet(name) {
    console.log(greeting + "，" + name + "！");
  }

  return greet;
}

const greet = createGreeter();
greet("小明"); // "你好，小明！"
greet("小红"); // "你好，小红！"
```

在这个例子中：
1. `createGreeter` 创建了一个局部变量 `greeting`
2. `createGreeter` 返回了内部函数 `greet`
3. `greet` 函数"记住"了创建时的 `greeting` 变量
4. 即使 `createGreeter` 已经执行完毕，`greeting` 变量依然存在

这就是闭包的魔力——函数带着创建时的"行李"一起走了！

---

### 闭包的原理：作用域链

闭包的原理是 **JavaScript 的作用域链**（Scope Chain）。

当 JavaScript 引擎查找变量时，会沿着作用域链从内向外查找：

```javascript
const globalVar = "全局";

function outer() {
  const outerVar = "外层";

  function inner() {
    const innerVar = "内层";
    console.log(globalVar); // 通过作用域链找到
    console.log(outerVar); // 通过作用域链找到
    console.log(innerVar); // 直接找到
  }

  return inner;
}

const fn = outer();
fn();
// 输出:
// 全局
// 外层
// 内层
```

当 `fn` 被调用时，`inner` 函数需要访问 `outerVar`，但 `inner` 的作用域中没有 `outerVar`。JavaScript 引擎会沿着作用域链向上查找，最终在 `outer` 的作用域中找到 `outerVar`。

**即使 `outer` 已经返回了，只要 `inner` 还存在，`outer` 的作用域就不会被销毁**，因为 `inner` 还在引用它。这就是闭包！

---

### 闭包经典问题：循环中的 setTimeout

这是面试中经常出现的经典问题：

```javascript
// ❌ 错误示例
for (var i = 0; i < 3; i++) {
  setTimeout(function() {
    console.log(i);
  }, 100);
}
// 输出：3, 3, 3（不是你期望的 0, 1, 2）
```

为什么会这样？因为 `var` 是函数作用域，三个 setTimeout 回调共享同一个 `i`。当 setTimeout 执行时，循环已经结束，`i` 的值是 3。

**解决方案1：使用 let（最简单）**

```javascript
// ✅ 使用 let
for (let i = 0; i < 3; i++) {
  setTimeout(function() {
    console.log(i);
  }, 100);
}
// 输出：0, 1, 2
```

因为 `let` 是块级作用域，每次循环都会创建一个新的 `i`，每个 setTimeout 都有自己独立的 `i`。

**解决方案2：使用 IIFE（立即调用函数表达式）**

```javascript
// ✅ 使用 IIFE 创建新作用域
for (var i = 0; i < 3; i++) {
  (function(index) {
    setTimeout(function() {
      console.log(index);
    }, 100);
  })(i);
}
// 输出：0, 1, 2
```

IIFE 创建了一个新的函数作用域，`index` 是这个作用域中的变量，每次循环传入不同的 `i`。

**解决方案3：使用闭包返回函数**

```javascript
// ✅ 使用闭包工厂函数
function createLogger(index) {
  return function() {
    console.log(index);
  };
}

for (var i = 0; i < 3; i++) {
  setTimeout(createLogger(i), 100);
}
// 输出：0, 1, 2
```

---

### 闭包与内存泄漏

很多人说闭包会导致内存泄漏，其实这是对闭包的误解。**闭包本身不会导致内存泄漏**，问题在于你是否意外地保留了不必要的引用。

```javascript
// ❌ 可能导致内存泄漏的例子
function heavyModule() {
  const bigData = new Array(1000000).fill("x"); // 占用大量内存

  const process = function() {
    console.log(bigData.length);
  };

  // 暴露到全局
  window.processData = process;
}

heavyModule();
// 即使函数执行完毕，bigData 也不会被回收
// 因为 window.processData 还引用着它
```

**如何避免内存泄漏：**

```javascript
// ✅ 正确做法：在不需要时断开引用
function heavyModule() {
  const bigData = new Array(1000000).fill("x");

  const process = function() {
    console.log(bigData.length);
  };

  // 暴露到全局
  window.processData = process;

  // 主动清理
  return function cleanup() {
    window.processData = null;
    // 或者
    delete window.processData;
  };
}

const cleanup = heavyModule();
// 当需要清理时调用
cleanup();
```

> 💡 记住：闭包本身不会泄漏，泄漏的是那些你不想要但被意外保留的引用。现代浏览器的垃圾回收器很智能，只要你断开引用，它就能回收内存。

---

### 用闭包实现私有变量：计数器

闭包最经典的应用之一就是实现**私有变量**——那些不能在函数外部直接访问的变量。

```javascript
function createCounter() {
  let count = 0; // 私有变量，只有通过返回的方法才能访问和修改

  return {
    increment: function() {
      count++;
      return count;
    },
    decrement: function() {
      count--;
      return count;
    },
    getCount: function() {
      return count;
    },
    reset: function() {
      count = 0;
      return count;
    }
  };
}

const counter = createCounter();

console.log(counter.getCount()); // 0
console.log(counter.increment()); // 1
console.log(counter.increment()); // 2
console.log(counter.decrement()); // 1
console.log(counter.getCount()); // 1
console.log(counter.reset());    // 0
console.log(counter.count);      // undefined（外部无法直接访问）
```

如果用 `var`，你无法阻止外部直接访问：

```javascript
// ❌ 用 var 的问题
function createCounter() {
  var count = 0; // 仍然是私有的，但返回方式不同
}

const counter = createCounter();
console.log(counter.count); // undefined
```

闭包让我们有了真正的"私有变量"！

---

### 用闭包实现防抖（debounce）函数

防抖的原理是：当事件触发时，不立即执行函数，而是等待一段时间。如果在这段时间内事件再次触发，就重新计时。只有当事件停止触发一段时间后，才执行函数。

```javascript
function debounce(func, wait) {
  let timeout;

  return function(...args) {
    const context = this;

    // 每次调用都清除之前的定时器
    clearTimeout(timeout);

    // 设置新的定时器
    timeout = setTimeout(function() {
      func.apply(context, args);
    }, wait);
  };
}

// 使用示例
const handleSearch = debounce(function(query) {
  console.log("搜索：" + query);
}, 500);

// 模拟用户输入
handleSearch("a");
handleSearch("ab");
handleSearch("abc");
// 只有当用户停止输入 500ms 后，才会执行搜索
```

**应用场景**：搜索框输入（用户停止输入后才发送搜索请求）、窗口调整大小（用户停止调整后才计算）、按钮防重复点击。

---

### 用闭包实现节流（throttle）函数

节流的原理是：限制函数的执行频率。无论事件触发多频繁，函数都会按照固定的时间间隔执行。

```javascript
function throttle(func, interval) {
  let lastTime = 0; // 上次执行的时间

  return function(...args) {
    const context = this;
    const now = Date.now();

    // 如果距离上次执行已经超过间隔时间，就执行
    if (now - lastTime >= interval) {
      lastTime = now;
      func.apply(context, args);
    }
  };
}

// 使用示例
const handleScroll = throttle(function() {
  console.log("滚动位置：" + window.scrollY);
}, 200);

// 模拟滚动事件
window.addEventListener("scroll", handleScroll);
// 无论滚动多频繁，每 200ms 最多执行一次
```

**防抖 vs 节流**：
- **防抖**：事件停止触发一段时间后才执行（适合：搜索框输入）
- **节流**：固定时间间隔执行一次（适合：滚动事件、窗口调整）

---

### 模块模式（Module Pattern）：用闭包实现私有方法

模块模式是 JavaScript 中一种经典的设计模式，利用闭包实现私有成员：

```javascript
const Calculator = (function() {
  // 私有成员
  let result = 0;

  function validate(number) {
    if (typeof number !== "number" || isNaN(number)) {
      throw new Error("无效的数字");
    }
  }

  function updateResult(value) {
    result = value;
    return result;
  }

  // 公共 API
  return {
    add: function(num) {
      validate(num);
      return updateResult(result + num);
    },
    subtract: function(num) {
      validate(num);
      return updateResult(result - num);
    },
    multiply: function(num) {
      validate(num);
      return updateResult(result * num);
    },
    divide: function(num) {
      validate(num);
      if (num === 0) throw new Error("除数不能为零");
      return updateResult(result / num);
    },
    getResult: function() {
      return result;
    },
    reset: function() {
      result = 0;
      return result;
    }
  };
})();

// 使用
console.log(Calculator.add(10));     // 10
console.log(Calculator.multiply(2)); // 20
console.log(Calculator.getResult()); // 20
console.log(Calculator.result);      // undefined（私有，无法访问）
Calculator.validate(5);              // Error: 私有方法，无法访问
```

这个模式的好处：
1. 私有变量 `result` 和 `validate` 无法从外部直接访问
2. 公共方法只能通过返回的对象访问
3. 形成了一个完整的模块，有自己的命名空间

---

## 12.3 高阶函数

### 回调函数

**回调函数**（Callback）是作为参数传递给另一个函数的函数。接收方可以在适当的时机调用这个函数。

```javascript
// 简单的回调函数示例
function greet(name, callback) {
  console.log("你好，" + name + "！");
  callback(); // 调用回调函数
}

greet("小明", function() {
  console.log("回调函数执行了！");
});
// 输出:
// 你好，小明！
// 回调函数执行了！
```

回调函数在异步操作中特别常见：

```javascript
// 模拟异步操作
function fetchData(callback) {
  setTimeout(function() {
    const data = { name: "小明", age: 18 };
    callback(data);
  }, 1000);
}

fetchData(function(data) {
  console.log("获取到的数据：", data);
});
// 1秒后输出：获取到的数据：{ name: "小明", age: 18 }
```

**回调地狱**（Callback Hell）：当多个异步操作嵌套时，代码会变得难以阅读：

```javascript
// 回调地狱示例
fetchData(function(data1) {
  processData(data1, function(data2) {
    saveData(data2, function(data3) {
      notifyUser(data3, function() {
        console.log("完成！");
      });
    });
  });
});
```

这就是 Promise 和 async/await 出现的原因！

---

### 函数作为返回值

函数可以返回另一个函数，这种模式叫做**函数工厂**：

```javascript
// 函数工厂：创建特定行为的函数
function multiplier(factor) {
  return function(number) {
    return number * factor;
  };
}

const double = multiplier(2);
const triple = multiplier(3);
const tenTimes = multiplier(10);

console.log(double(5));    // 10
console.log(triple(5));     // 15
console.log(tenTimes(5));   // 50
```

每次调用 `multiplier` 都会创建一个新的函数，每个函数都有自己独立的 `factor` 值。

**典型应用：权限检查**

```javascript
function requirePermission(permission) {
  return function(user) {
    if (!user.permissions.includes(permission)) {
      throw new Error("没有 " + permission + " 权限");
    }
    return true;
  };
}

const canEdit = requirePermission("edit");
const canDelete = requirePermission("delete");

const user = { name: "小明", permissions: ["edit", "comment"] };

console.log(canEdit(user));    // true
console.log(canDelete(user));   // Error: 没有 delete 权限
```

---

### IIFE（立即调用函数表达式）

**IIFE**（Immediately Invoked Function Expression）是一种定义后立即执行的函数：

```javascript
// 基本语法
(function() {
  console.log("我立即执行了！");
})();

// 带参数
(function(name) {
  console.log("你好，" + name + "！");
})("小明");

// 箭头函数版本
(() => {
  console.log("箭头函数 IIFE");
})();
```

**IIFE 的作用：**

1. **创建独立作用域**：IIFE 内部定义的变量不会污染外部作用域

```javascript
const result = (function() {
  const temp = "我是临时变量";
  // 执行复杂计算
  return temp + "的结果";
})();

console.log(result); // "我是临时变量"
console.log(temp);   // ReferenceError: temp is not defined
```

2. **模拟块级作用域**（在 `let`/`const` 出现之前）

```javascript
// 用 IIFE 模拟块级作用域
for (var i = 0; i < 3; i++) {
  (function(index) {
    console.log(index);
  })(i);
}
// 输出：0, 1, 2
```

3. **模块模式**：IIFE 配合返回对象可以实现私有变量

```javascript
const myModule = (function() {
  let privateVar = "私有变量";

  function privateMethod() {
    console.log("私有方法");
  }

  return {
    publicMethod: function() {
      console.log("公共方法可以访问：" + privateVar);
      privateMethod();
    }
  };
})();

myModule.publicMethod();
// 公共方法可以访问：私有变量
// 私有方法
console.log(myModule.privateVar); // undefined
```

> 💡 注意：现代 JavaScript 中，`let` 和 `const` 提供了块级作用域，IIFE 的使用场景大大减少。但理解 IIFE 对于阅读旧代码和理解模块模式仍然很重要。

---

## 本章小结

本章我们深入探索了 JavaScript 的作用域和闭包：

1. **作用域类型**：
   - 全局作用域：程序最外层
   - 函数作用域：`function` 创建
   - 块级作用域：`let`/`const` 在 `{}` 中创建

2. **词法作用域**：由源代码位置决定，不是调用位置

3. **闭包**：函数能记住并访问创建时的词法环境
   - 原理：作用域链
   - 应用：私有变量、防抖、节流、模块模式

4. **高阶函数**：
   - 回调函数：作为参数传递的函数
   - 函数工厂：返回函数的函数
   - IIFE：立即执行的函数表达式

> 📊 图示：闭包原理
>
> ```mermaid
> graph LR
>     A[创建闭包] --> B[函数]
>     B --> C[词法环境]
>     C --> D[变量 a]
>     C --> E[变量 b]
>     C --> F[...其他变量]
>     G[调用闭包函数] --> H[访问词法环境中的变量]
> ```

---

**下章预告**：下一章我们将学习**递归与函数式编程**——如何用函数的思维来解决问题！ 🧠

