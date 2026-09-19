+++
title = "第 13 章 递归与函数式"
weight = 130
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 13 章 递归与函数式

> 递归是程序员的瑞士军刀，函数式编程是代码的诗歌。当两者结合，就像给程序员装上了翅膀——可以飞得很高，但也要小心别撞上"栈溢出"的天花板。

## 13.1 递归

### 递归函数：函数调用自身

**递归**（Recursion）就是函数调用自身。听起来简单，但它的威力巨大——可以解决很多看起来很复杂的问题。

```javascript
// 最简单的递归：倒计时
function countdown(n) {
  if (n <= 0) {
    console.log("发射！");
    return;
  }
  console.log(n);
  countdown(n - 1); // 调用自身
}

countdown(5);
// 输出：
// 5
// 4
// 3
// 2
// 1
// 发射！
```

递归就像俄罗斯套娃——打开一个娃娃，里面还有一个，打开那个，里面还有一个...直到找到最小的那个，然后从里往外一层层关上。

---

### 终止条件与栈溢出（Maximum call stack size exceeded）

递归必须有**终止条件**（Base Case），否则会无限递归下去，直到浏览器崩溃：

```javascript
// ❌ 错误示范：没有终止条件
function infiniteRecursion() {
  console.log("我停不下来...");
  infiniteRecursion(); // 调用自身，但没有退出条件
}

infiniteRecursion();
// Uncaught RangeError: Maximum call stack size exceeded
// 或者在 Node.js 中：RangeError: Maximum call stack size exceeded
```

**栈溢出**（Stack Overflow）是因为每次函数调用都会在调用栈中占用空间，无限递归会让栈溢出。

> 💡 记住：**每个递归函数都必须有终止条件！** 这是递归的第一原则。

```javascript
// ✅ 正确示例：计算阶乘
function factorial(n) {
  // 终止条件
  if (n <= 1) {
    return 1;
  }
  // 递归调用
  return n * factorial(n - 1);
}

console.log(factorial(5)); // 120 = 5 * 4 * 3 * 2 * 1
console.log(factorial(0)); // 1（0! = 1）
console.log(factorial(1)); // 1
```

---

### 递归实现阶乘 / 斐波那契数列 / 汉诺塔

#### 阶乘

阶乘的数学定义：n! = n × (n-1) × (n-2) × ... × 1

```javascript
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

// 迭代版本（对比）
function factorialIterative(n) {
  let result = 1;
  for (let i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}

console.log(factorial(5));        // 120
console.log(factorialIterative(5)); // 120
```

#### 斐波那契数列

斐波那契数列：1, 1, 2, 3, 5, 8, 13, 21, ...

```javascript
// 递归版本
function fibonacci(n) {
  if (n <= 2) return 1;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(1));  // 1
console.log(fibonacci(6));  // 8
console.log(fibonacci(10)); // 55

// 迭代版本（更高效）
function fibonacciIterative(n) {
  if (n <= 2) return 1;
  let prev = 1, curr = 1;
  for (let i = 3; i <= n; i++) {
    [prev, curr] = [curr, prev + curr];
  }
  return curr;
}

console.log(fibonacciIterative(10)); // 55
```

> ⚠️ 注意：递归版本的斐波那契有严重的性能问题——时间复杂度是 O(2^n)，因为有大量重复计算。可以用**记忆化**（Memoization）优化：

```javascript
// 记忆化递归版本
function fibonacciMemo(n, memo = {}) {
  if (n in memo) return memo[n];
  if (n <= 2) return 1;

  memo[n] = fibonacciMemo(n - 1, memo) + fibonacciMemo(n - 2, memo);
  return memo[n];
}

console.log(fibonacciMemo(100)); // 354224848179262000000（能正常计算）
// fibonacci(100) 会直接卡死
```

> 不过要注意精度：`fib(100)` 的真实值是 `354224848179261915075`，已经远超 `Number.MAX_SAFE_INTEGER`（2^53 - 1），所以上面打印出来的末几位是错的。需要精确结果时请用 `BigInt`：

```javascript
// 用 BigInt 写记忆化斐波那契，结果完全精确
function fibBig(n, memo = new Map()) {
  if (n <= 2n) return 1n;
  if (memo.has(n)) return memo.get(n);
  const value = fibBig(n - 1n, memo) + fibBig(n - 2n, memo);
  memo.set(n, value);
  return value;
}

console.log(fibBig(100n).toString()); // "354224848179261915075"（一位不差）
console.log(fibBig(100n) === 354224848179261915075n); // true
```

#### 汉诺塔

汉诺塔是经典的递归问题：有 A、B、C 三根柱子，A 柱子上有 n 个盘子（从上到下依次变大），需要把盘子全部移动到 C 柱子，每次只能移动一个盘子，且大盘子不能放在小盘子上面。

```javascript
function hanoi(n, from, to, auxiliary) {
  if (n === 1) {
    console.log(`把第 ${n} 个盘子从 ${from} 移动到 ${to}`);
    return;
  }

  // 把 n-1 个盘子从 A 移动到 B（借助 C）
  hanoi(n - 1, from, auxiliary, to);

  // 把最大的盘子从 A 移动到 C
  console.log(`把第 ${n} 个盘子从 ${from} 移动到 ${to}`);

  // 把 n-1 个盘子从 B 移动到 C（借助 A）
  hanoi(n - 1, auxiliary, to, from);
}

// 三层汉诺塔
hanoi(3, "A", "C", "B");

// 输出：
// 把第 1 个盘子从 A 移动到 C
// 把第 2 个盘子从 A 移动到 B
// 把第 1 个盘子从 C 移动到 B
// 把第 3 个盘子从 A 移动到 C
// 把第 1 个盘子从 B 移动到 A
// 把第 2 个盘子从 B 移动到 C
// 把第 1 个盘子从 A 移动到 C
```

汉诺塔的移动次数是 2^n - 1，所以三层汉诺塔需要 7 次移动。

---

### 尾递归优化：什么是尾递归

**尾递归**（Tail Recursion）是递归的一种特殊形式——在函数的最后一步直接返回递归调用的结果，不做任何其他操作。

```javascript
// ❌ 非尾递归：递归调用返回之后还要「再乘一次 n」，所以当前栈帧必须保留
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1); // 调用之后还有乘法要算
}

// ✅ 尾递归版本：把中间结果通过参数传下去，递归调用是最后一步动作
function factorialTail(n, result = 1) {
  if (n <= 1) return result;
  return factorialTail(n - 1, n * result); // 最后一步就是递归调用
}

console.log(factorial(5), factorialTail(5)); // 120 120
```

尾递归的好处是：如果引擎实现了**尾调用优化**（TCO），就可以复用当前栈帧、不新增栈空间，从而彻底避免栈溢出。

```javascript
// 普通递归：调用栈不断增长
function sumRecursive(n) {
  if (n <= 1) return n;
  return n + sumRecursive(n - 1);
}

// 尾递归：使用累加器
function sumTailRecursive(n, acc = 0) {
  if (n <= 0) return acc;
  return sumTailRecursive(n - 1, acc + n);
}
```

> ⚠️ 重要提示：ES2015 规范确实规定了「严格模式下必须实现尾调用优化」，但现实中只有 Safari 的 JavaScriptCore 落地了；**Chrome / Edge / Node 使用的 V8 至今没有实现**（官方态度是「不支持」，短期内也不会改变）。所以在实际部署时，别指望写成尾递归就能省下栈空间。

```javascript
// 无论是不是尾递归，V8 里递归深了都会栈溢出
function sumTail(n, acc = 0) {
  if (n <= 0) return acc;
  return sumTail(n - 1, acc + n);
}

// 10 万层左右就会崩（具体阈值和引擎、可用栈大小有关）
try {
  console.log(sumTail(100000));
} catch (e) {
  console.log(e.name, e.message); // RangeError Maximum call stack size exceeded
}

// 工程上的替代方案一：改成循环（最省心）
function sumLoop(n) {
  let acc = 0;
  for (let i = n; i > 0; i--) acc += i;
  return acc;
}
console.log(sumLoop(100000)); // 5000050000（超了 32 位但没超安全整数）

// 工程上的替代方案二：蹦床（trampoline）——用循环驱动「返回下一个函数」的写法
function trampoline(fn) {
  return function (...args) {
    let result = fn(...args);
    while (typeof result === "function") {
      result = result();
    }
    return result;
  };
}

const sumTrampolined = trampoline(function sumStep(n, acc = 0) {
  return n <= 0 ? acc : () => sumStep(n - 1, acc + n);
});
console.log(sumTrampolined(100000)); // 5000050000（不会栈溢出）
```

> 结论：写递归时把终止条件写对、控制递归深度（几万层以内），比纠结「尾递归能不能被优化」更实际。

---

## 13.2 函数式编程

### 纯函数：相同输入相同输出，无副作用

**纯函数**（Pure Function）是函数式编程的基石。它满足两个条件：
1. **相同输入，相同输出**：不管调用多少次，只要输入相同，结果永远一样
2. **无副作用**：不修改外部状态，不进行 I/O 操作，不抛出异常等

```javascript
// ✅ 纯函数
function add(a, b) {
  return a + b;
}

console.log(add(1, 2)); // 3
console.log(add(1, 2)); // 3（永远都是 3）
console.log(add(1, 2)); // 3

// ❌ 非纯函数（依赖外部状态）
let base = 10;
function addToBase(a) {
  return a + base;
}

console.log(addToBase(5)); // 15
base = 20;
console.log(addToBase(5)); // 25（输入相同，但结果不同！）

// ❌ 非纯函数（有副作用）
function greet(name) {
  console.log("你好，" + name + "！"); // console.log 是副作用
}
```

**副作用的例子**：
- 修改全局变量
- 修改传入的参数
- 进行 HTTP 请求
- 操作 DOM
- 打印到控制台
- 抛出异常
- 读取文件

---

### 纯函数的优势与原则

**纯函数的优势**：

1. **可测试**：给定输入就有确定的输出，不需要 mock 环境

```javascript
// 纯函数测试
test("add 纯函数", () => {
  expect(add(1, 2)).toBe(3);
  expect(add(1, 2)).toBe(3);
  expect(add(1, 2)).toBe(3);
  // 无论测试多少次，结果都一样！
});
```

2. **可缓存**：因为相同输入必定相同输出，可以缓存结果

```javascript
// 记忆化函数（自动缓存）
function memoize(fn) {
  const cache = new Map(); // 用 Map，才能安全地缓存 0、""、NaN 这类值

  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      console.log("命中缓存");
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const slowAdd = (a, b) => {
  // 模拟耗时操作
  return a + b;
};

const memoizedAdd = memoize(slowAdd);
console.log(memoizedAdd(1, 2)); // 第一次计算
console.log(memoizedAdd(1, 2)); // 命中缓存

// 如果用 `if (cache[key])` 判断，返回值是 0 / "" / false 时就会被误判成「没缓存」
const memoizedZero = memoize(() => 0);
console.log(memoizedZero()); // 第一次计算，返回 0
console.log(memoizedZero()); // 命中缓存（用 Map.has 判断才正确）
```

3. **易于并行**：不需要共享状态，可以安全并行执行

4. **易于推理**：没有隐藏的依赖，代码行为可预测

> 💡 实践建议：尽量编写纯函数，把副作用推到程序边界（如用户交互、网络请求等）处理。

---

### map / filter / reduce 的函数式组合

`map`、`filter`、`reduce` 是函数式编程的"三剑客"，它们的组合可以写出优雅的数据处理代码。

#### map — 转换

`map` 对数组中的每个元素执行操作，返回一个新数组：

```javascript
const numbers = [1, 2, 3, 4, 5];

// 传统写法
const doubled = [];
for (let n of numbers) {
  doubled.push(n * 2);
}

// map 写法
const doubledMap = numbers.map(n => n * 2);

console.log(doubledMap); // [2, 4, 6, 8, 10]
```

#### filter — 过滤

`filter` 根据条件筛选元素，返回一个新数组：

```javascript
const numbers = [1, 2, 3, 4, 5];

// 传统写法
const evens = [];
for (let n of numbers) {
  if (n % 2 === 0) {
    evens.push(n);
  }
}

// filter 写法
const evensFilter = numbers.filter(n => n % 2 === 0);

console.log(evensFilter); // [2, 4]
```

#### reduce — 聚合

`reduce` 将数组元素聚合成一个值：

```javascript
const numbers = [1, 2, 3, 4, 5];

// 传统写法
let sum = 0;
for (let n of numbers) {
  sum += n;
}

// reduce 写法
const sumReduce = numbers.reduce((acc, n) => acc + n, 0);

console.log(sumReduce); // 15
```

#### 链式调用

三个方法都可以返回数组，所以可以链式调用：

```javascript
const products = [
  { name: "iPhone", price: 800 },
  { name: "MacBook", price: 2000 },
  { name: "AirPods", price: 200 },
  { name: "iPad", price: 600 }
];

// 找出价格 > 500 的商品，把价格翻倍，计算总和
const result = products
  .filter(p => p.price > 500)  // [{ name: "iPhone", price: 800 }, { name: "MacBook", price: 2000 }, { name: "iPad", price: 600 }]
  .map(p => p.price * 2)       // [1600, 4000, 1200]
  .reduce((sum, price) => sum + price, 0); // 6800

console.log(result); // 6800
```

> 💡 对比传统写法：
> ```javascript
> let result = 0;
> for (let p of products) {
>       if (p.price > 500) {
>         result += p.price * 2;
>       }
> }
> console.log(result); // 6800
> ```
>
> 函数式写法更声明式，意图更清晰：先过滤，再转换，最后聚合。

---

## 本章小结

本章我们学习了递归和函数式编程的基础：

1. **递归**：
   - 函数调用自身
   - 必须有终止条件
   - 经典应用：阶乘、斐波那契数列、汉诺塔
   - 朴素递归的斐波那契是 O(2^n)，要用记忆化（缓存）或改成迭代；结果超出 2^53 时请用 `BigInt`
   - 尾递归：把中间结果放进参数、递归调用作为最后一步；但 **V8 没有实现尾调用优化**，深度太大照样栈溢出，实用替代是循环或蹦床
   - 递归深度受调用栈限制，几十万层这种需求应该改成循环

2. **函数式编程**：
   - 纯函数：相同输入相同输出、无副作用；副作用（改外部状态、I/O、DOM 操作、打印）尽量推到程序边界
   - 纯函数优势：可测试、可缓存（记忆化）、易并行、易推理
   - `map`（转换）/ `filter`（过滤）/ `reduce`（聚合）三剑客，链式调用写出声明式代码
   - 写缓存时用 `Map.has` 或 `Object.hasOwn` 判断，别用 `if (cache[key])`——返回值是 `0` / `""` / `false` 时会误判

> 📊 图示：map/filter/reduce 的数据流
>
> ```mermaid
> graph LR
>     A[数组] --> B[filter]
>     B --> C[map]
>     C --> D[reduce]
>     D --> E[最终结果]
>
>     B -.->|过滤| F[符合条件的元素]
>     C -.->|转换| G[转换后的元素]
> ```

---

**下章预告**：下一章我们将揭开 **JavaScript 事件循环** 的神秘面纱——为什么 setTimeout 不一定能准时执行？为什么 Promise 比 setTimeout 先执行？答案就在事件循环！ ⏰
