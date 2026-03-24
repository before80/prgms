+++
title = "第 14 章 事件循环"
weight = 140
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 14 章 事件循环

> 事件循环是 JavaScript 的"大总管"，负责调度所有任务的执行顺序。理解了它，你就能解释为什么有些代码"明明后定义却先执行"，为什么 Promise 比 setTimeout 更有优先级。准备好了吗？让我们进入 JavaScript 的"调度室"！

## 14.1 单线程与异步

### JavaScript 单线程模型及原因

JavaScript 从诞生之日起就是**单线程**（Single Threaded）的语言。这意味着什么？

**单线程** = 一次只能做一件事。就像只有一个厨师的厨房，一次只能烹饪一道菜。

```javascript
console.log("第一步：洗菜");
console.log("第二步：切菜");
console.log("第三步：炒菜");
console.log("完成！");

// 输出顺序是固定的：
// 第一步：洗菜
// 第二步：切菜
// 第三步：炒菜
// 完成！
```

**为什么 JavaScript 是单线程的？**

1. **历史原因**：JavaScript 最初是为了在浏览器中处理简单的交互逻辑，不需要并发
2. **避免复杂性**：多线程需要处理锁、死锁、竞态条件等问题，单线程大大降低了复杂性
3. **DOM 限制**：浏览器中的 DOM 是非线程安全的，如果多个线程同时修改 DOM，会导致不可预测的结果

> 💡 虽然 JavaScript 主线程是单线程的，但浏览器提供了 **Web APIs**（如 setTimeout、fetch、DOM 事件等）来处理异步操作，这些是在后台线程中执行的。

---

### 同步 vs 异步执行模型

**同步（Synchronous）**：按顺序执行，一个任务完成后才开始下一个。

```javascript
console.log("1");
console.log("2");
console.log("3");
// 输出：1 2 3（按顺序，没有悬念）
```

**异步（Asynchronous）**：不等待前一个任务完成就继续执行下一个，任务结果在"将来"某个时刻才返回。

```javascript
console.log("1");

setTimeout(() => {
  console.log("3（异步任务完成了）");
}, 1000);

console.log("2");
// 输出：
// 1
// 2
// 3（异步任务完成了）（1秒后）
```

异步的"将来某时刻"可能是：
- 1秒后（setTimeout）
- 用户点击按钮时
- 网络请求返回时
- 文件读取完成时

---

### 调用栈（Call Stack）

**调用栈**（Call Stack）是 JavaScript 用来跟踪函数调用的"记账本"。它是一个 LIFO（Last In, First Out）结构——最后进入的函数最先出来。

```javascript
function a() {
  console.log("a 开始");
  b();
  console.log("a 结束");
}

function b() {
  console.log("b 开始");
  c();
  console.log("b 结束");
}

function c() {
  console.log("c 执行");
}

a();
// 输出：
// a 开始
// b 开始
// c 执行
// b 结束
// a 结束
```

调用栈的变化过程：

```
调用 a()
栈：[a]

在 a() 中调用 b()
栈：[a, b]

在 b() 中调用 c()
栈：[a, b, c]

c() 执行完毕，弹出
栈：[a, b]

b() 执行完毕，弹出
栈：[a]

a() 执行完毕，弹出
栈：[]（空）
```

当调用栈中的函数太多时，就会发生**栈溢出**（Stack Overflow）：

```javascript
// 无限递归导致栈溢出
function recursivelyCall() {
  recursivelyCall();
}

recursivelyCall();
// Uncaught RangeError: Maximum call stack size exceeded
```

---

### Web APIs：浏览器提供的能力（DOM / Timer / AJAX / FileReader 等）

JavaScript 本身只能执行同步代码，但浏览器提供了 **Web APIs** 来处理需要"等待"的操作。这些 Web APIs 是在浏览器内部的独立线程中运行的。

常见的 Web APIs：

| API | 用途 |
|-----|------|
| `setTimeout` / `setInterval` | 定时器 |
| `DOM Events` | DOM 事件监听 |
| `fetch` | 网络请求 |
| `FileReader` | 文件读取 |
| `IndexedDB` | 浏览器数据库 |
| `requestAnimationFrame` | 动画帧 |

```javascript
console.log("1");

setTimeout(() => {
  console.log("4（setTimeout 回调）");
}, 0); // 注意：延迟是 0！

console.log("2");
console.log("3");

// 输出：
// 1
// 2
// 3
// 4（setTimeout 回调）
```

即使 `setTimeout` 延迟是 0，它也不是立即执行的！因为 `setTimeout` 是 Web API，它的回调函数会先被放到任务队列中，等主线程空闲时才执行。

---

## 14.2 任务队列

### 宏任务（macrotask）：setTimeout / setInterval / UI Rendering / requestAnimationFrame

**宏任务**（MacroTask）代表要执行的整体任务，如 I/O 操作、解析 HTML、setTimeout 等。

常见的宏任务来源：

| 来源 | 说明 |
|------|------|
| `setTimeout` | 定时器任务 |
| `setInterval` | 间隔任务 |
| `setImmediate`（Node.js） | 立即执行任务 |
| I/O 操作 | 网络请求、文件读写等 |
| UI 渲染 | 浏览器重排、重绘 |
| `requestAnimationFrame` | 动画帧 |

---

### 微任务（microtask）：Promise.then / MutationObserver / queueMicrotask

**微任务**（MicroTask）是更小的任务，主要用于处理异步操作的结果。

常见的微任务来源：

| 来源 | 说明 |
|------|------|
| `Promise.then` / `catch` / `finally` | Promise 回调 |
| `queueMicrotask()` | 手动入队微任务 |
| `MutationObserver` | DOM 变化监听 |
| `process.nextTick`（Node.js） | Node.js 特有的微任务 |

> 💡 **重要区别**：
> - 宏任务：队列，每轮事件循环只执行一个
> - 微任务：队列，每轮事件循环中**所有微任务都会执行完**才结束

---

### 事件循环执行顺序：同步代码 → 微任务队列 → 渲染 → 宏任务队列

这是事件循环的核心执行顺序：

```
┌─────────────────────────────────────────┐
│ 1. 执行同步代码（调用栈）                │
│ 2. 执行所有微任务（清空微任务队列）       │
│ 3. 执行一个宏任务                        │
│ 4. （可能）渲染更新                      │
│ 5. 回到步骤 1，继续下一轮                │
└─────────────────────────────────────────┘
```

```javascript
console.log("1（同步）");

setTimeout(() => {
  console.log("4（宏任务 - setTimeout）");
}, 0);

Promise.resolve()
  .then(() => {
    console.log("3（微任务 - Promise.then）");
  });

console.log("2（同步）");

// 输出：
// 1（同步）
// 2（同步）
// 3（微任务 - Promise.then）← 微任务在同步代码后立即执行
// 4（宏任务 - setTimeout）← 宏任务在微任务后执行
```

解析执行过程：
1. `console.log("1")` 是同步代码，立即执行
2. `setTimeout` 是宏任务，放入宏任务队列
3. `Promise.resolve().then()` 是微任务，放入微任务队列
4. `console.log("2")` 是同步代码，立即执行
5. **同步代码执行完毕，开始执行微任务**
6. 执行 `Promise.then` 回调，打印 "3"
7. **微任务队列清空，执行一个宏任务**
8. 执行 `setTimeout` 回调，打印 "4"

---

### setTimeout(fn, 0) 不一定立即执行的原因

很多人以为 `setTimeout(fn, 0)` 会立即执行，但实际上它会等当前所有同步代码和微任务执行完毕。

```javascript
// 例子1
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("sync");

// 输出：
// sync
// promise
// timeout
```

```javascript
// 例子2
setTimeout(() => console.log("timeout1"), 0);

setTimeout(() => {
  console.log("timeout2 开始");
  Promise.resolve().then(() => {
    console.log("timeout2 内的 promise");
  });
  console.log("timeout2 结束");
}, 0);

console.log("sync");

// 输出：
// sync
// timeout2 开始
// timeout2 结束
// timeout2 内的 promise  ← 微任务在两个宏任务之间执行！
```

这个例子展示了事件循环的重要特性：**微任务在宏任务之间执行**。

---

### queueMicrotask：手动将回调放入微任务队列

`queueMicrotask` API 允许你手动将回调函数放入微任务队列：

```javascript
console.log("1（同步）");

queueMicrotask(() => {
  console.log("3（手动入队的微任务）");
});

Promise.resolve().then(() => {
  console.log("4（Promise 微任务）");
});

setTimeout(() => {
  console.log("5（宏任务）");
}, 0);

console.log("2（同步）");

// 输出：
// 1（同步）
// 2（同步）
// 3（手动入队的微任务）← 先注册的微任务先执行
// 4（Promise 微任务）
// 5（宏任务）
```

> 💡 什么时候用 `queueMicrotask`？当你需要在当前任务完成后、渲染前执行一些操作时，比如 React 的状态更新就使用了微任务队列。

---

## 14.3 浏览器 vs Node.js 事件循环

### 浏览器事件循环阶段

浏览器中的事件循环有明确的阶段划分：

```
   ┌─────────────────────────────┐
   │           阶段 1             │
   │   执行同步代码（调用栈）      │
   └─────────────┬───────────────┘
                 ↓
   ┌─────────────────────────────┐
   │           阶段 2             │
   │     执行所有微任务           │
   │  （Promise 回调等）         │
   └─────────────┬───────────────┘
                 ↓
   ┌─────────────────────────────┐
   │           阶段 3             │
   │       执行一个宏任务          │
   │   （setTimeout 回调等）      │
   └─────────────┬───────────────┘
                 ↓
   ┌─────────────────────────────┐
   │           阶段 4             │
   │       （可能）渲染更新        │
   └─────────────┬───────────────┘
                 ↓
        ← 返回阶段 1，继续循环 →
```

> 📊 简化版浏览器事件循环流程图：
>
> ```mermaid
> flowchart TD
>     A[开始] --> B[执行同步代码]
>     B --> C{微任务队列<br/>是否为空？}
>     C -->|否| D[执行所有微任务]
>     D --> C
>     C -->|是| E[执行一个宏任务]
>     E --> F{需要渲染？}
>     F -->|是| G[渲染更新]
>     F -->|否| H[下一轮循环]
>     G --> H
>     H --> B
> ```

---

### Node.js 事件循环：timers / pending callbacks / poll / check / close callbacks

Node.js 的事件循环与浏览器有所不同，主要体现在多了几个阶段：

| 阶段 | 说明 |
|------|------|
| `timers` | 执行 setTimeout / setInterval 回调 |
| `pending callbacks` | 执行上一轮延迟的 I/O 回调 |
| `idle, prepare` | 内部使用 |
| `poll` | 检索新的 I/O 事件，执行 I/O 回调 |
| `check` | 执行 setImmediate 回调 |
| `close callbacks` | 执行 close 事件回调 |

---

### process.nextTick / setImmediate

Node.js 有两个特殊的任务调度 API：

#### process.nextTick

`process.nextTick` 的回调会在**当前操作完成后、下一个事件循环阶段开始前**执行，比 `setImmediate` 更早：

```javascript
console.log("1（同步）");

setTimeout(() => console.log("3（setTimeout）"), 0);

setImmediate(() => console.log("4（setImmediate）"));

process.nextTick(() => console.log("2（nextTick）"));

console.log("5（同步）");

// 输出：
// 1（同步）
// 5（同步）
// 2（nextTick）← nextTick 在同步代码后立即执行
// 3（setTimeout）← setTimeout 在 timers 阶段
// 4（setImmediate）← setImmediate 在 check 阶段
```

> 💡 `process.nextTick` 不是事件循环的一部分，它是一个独立的微任务队列，会在每个阶段结束后立即执行所有 `nextTick` 回调。

#### setImmediate

`setImmediate` 的回调在 **check 阶段**执行，理论上在 I/O 回调之后、timers 之前：

```javascript
const fs = require("fs");

fs.readFile(__filename, () => {
  console.log("1（I/O 回调）");

  setTimeout(() => console.log("2（setTimeout in I/O）"), 0);
  setImmediate(() => console.log("3（setImmediate in I/O）"));

  process.nextTick(() => console.log("4（nextTick in I/O）"));
});

// 输出顺序：
// 4（nextTick in I/O）
// 1（I/O 回调）
// 2（setTimeout in I/O）← 不一定，看具体情况
// 3（setImmediate in I/O）
```

> 💡 总结：
> - `process.nextTick`：当前操作完成后立即执行，最快
> - `setImmediate`：在 check 阶段执行，下一轮事件循环
> - `setTimeout`：在 timers 阶段执行，下一轮事件循环

---

## 本章小结

本章我们深入理解了 JavaScript 的事件循环机制：

1. **单线程模型**：JavaScript 主线程一次只能执行一个任务
2. **同步 vs 异步**：同步阻塞执行，异步不等待结果
3. **调用栈**：跟踪函数调用，LIFO 结构
4. **Web APIs**：浏览器提供的异步能力（setTimeout、fetch 等）
5. **任务队列**：
   - 宏任务：setTimeout、setInterval、I/O、渲染等
   - 微任务：Promise.then、queueMicrotask、MutationObserver 等
6. **事件循环执行顺序**：同步代码 → 微任务队列 → 渲染 → 宏任务队列
7. **浏览器 vs Node.js**：Node.js 有更多阶段（timers、poll、check 等）和 `process.nextTick`、`setImmediate` 等特殊 API

> 📊 图示：事件循环流程图
>
> ```mermaid
> flowchart TD
>     A[开始] --> B[执行同步代码]
>     B --> C{微任务队列<br/>是否为空？}
>     C -->|否| D[执行所有微任务]
>     D --> C
>     C -->|是| E[执行一个宏任务]
>     E --> F{需要渲染？}
>     F -->|是| G[渲染更新]
>     F -->|否| H[下一轮循环]
>     G --> H
>     H --> B
> ```

---

**下章预告**：下一章我们将学习 **Promise**——处理异步操作的现代化解决方案！ 🚀

