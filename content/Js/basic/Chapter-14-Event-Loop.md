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

### 宏任务（macrotask）：setTimeout / setInterval / I/O

**宏任务**（MacroTask）代表要执行的整体任务，如 I/O 操作、解析 HTML、setTimeout 等。

常见的宏任务来源：

| 来源 | 说明 |
|------|------|
| `setTimeout` | 定时器任务 |
| `setInterval` | 间隔任务 |
| `setImmediate`（Node.js） | 立即执行任务 |
| I/O 操作 | 网络请求、文件读写等 |
| 用户交互 | 点击、滚动等事件的回调 |

> ⚠️ **两个常见的错误归类别**：
>
> - **渲染（重排、重绘）不是宏任务**。它是「更新渲染」这个独立步骤，发生在当前任务和它的微任务都执行完之后、浏览器决定绘制时；不会因为没有渲染任务就把渲染跳过，也不会被 `setTimeout(fn, 0)` 插到前面。
> - **`requestAnimationFrame` 也不是宏任务**。它的回调会在「更新渲染」这一步开始前统一执行（同一帧内只调用一次），和任务队列是两套机制。
>
> 另外还要注意，浏览器里并不是只有一个「宏任务队列」，而是按**任务源**分成多个队列（定时器、网络、用户交互等），浏览器可以在它们之间自行选择优先级，规范只保证「每个队列内部先进先出」。

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
> - 宏任务：每轮事件循环只取**一个**执行
> - 微任务：每轮事件循环中**所有微任务都会执行完**（包括执行过程中新产生的微任务）才结束
>
> 这个差别带来一个真实的坑：如果微任务里不断产生新的微任务，就会一直循环下去，宏任务和页面渲染都得不到执行，表现为页面卡死。

```javascript
// ❌ 无限微任务：页面会直接卡死（不要在控制台真跑这段）
// function loop() {
//   Promise.resolve().then(loop);
// }
// loop();

// ✅ 需要「让出主线程」时用宏任务
function loopByTask() {
  setTimeout(loopByTask, 0);   // 每次都会给渲染和用户操作留出机会
}
```

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

`process.nextTick` 的回调会在**当前操作（当前这段同步代码或当前这个回调）完成后立即执行**，它不在事件循环的任何阶段里。要特别注意两点：

1. 它是在**每个回调之后**就被清空，而不是「等一个阶段结束」才执行；
2. 在 Node 中它的优先级高于 Promise 微任务，也就是 `nextTick` 队列会先于 `then` 回调被清空。

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

> 💡 **注意**：`3（setTimeout）` 与 `4（setImmediate）` 的先后顺序在**主模块里是不确定的**，取决于进程启动时定时器的到期情况，实测每次运行都可能不同。只有在 I/O 回调内部，`setImmediate` 才稳定地早于 `setTimeout`。

#### setImmediate

`setImmediate` 的回调在 **check 阶段**执行。因为 poll 阶段结束后紧接着就是 check 阶段，所以在 I/O 回调里注册的 `setImmediate` 一定比 `setTimeout(fn, 0)` 更早执行：

```javascript
const fs = require("fs");

fs.readFile(__filename, () => {
  console.log("1（I/O 回调）");

  setTimeout(() => console.log("2（setTimeout in I/O）"), 0);
  setImmediate(() => console.log("3（setImmediate in I/O）"));

  process.nextTick(() => console.log("4（nextTick in I/O）"));
});

// 输出顺序：
// 1（I/O 回调）      ← 当前这个回调本身先执行完
// 4（nextTick in I/O）← 回调一结束，nextTick 队列立即清空
// 3（setImmediate in I/O）← 进入 check 阶段
// 2（setTimeout in I/O）  ← 下一轮 timers 阶段
```

> 💡 总结：
> - `process.nextTick`：当前操作完成后立即执行，优先级最高
> - `setImmediate`：在 check 阶段执行；在 I/O 回调里稳定早于 `setTimeout`
> - `setTimeout(fn, 0)`：在 timers 阶段执行，最小延迟会被钳到 1ms 左右
>
> 实践建议：日常写异步逻辑优先用 Promise / `async` / `await`，只有确实需要「在当前调用栈结束后插队」时才用 `process.nextTick`——它一旦递归就会饿死 I/O，官方也建议尽量改用 `queueMicrotask` 或 `setImmediate`。

## 14.4 常见误区与实战细节

### setTimeout(fn, 0) 并不等于「马上执行」，也不精确

- 它首先要排队，前面还有同步代码、微任务、其他宏任务；
- 浏览器里嵌套层级超过 5 层后，最小延迟会被强制提升到 **4ms**（这是规范写明的节流，防止脚本用定时器占满 CPU）；
- 如果前一任务耗时长，定时器回调只能等它结束，偏差可能是几百毫秒；
- 用 `setInterval` 做动画或精确节拍更是不可靠：回调的执行时间会被算进间隔，误差还会累积。

需要「下一帧再执行」用 `requestAnimationFrame`，需要「稳定节拍」用「递归 `setTimeout` + 记录误差补偿」，需要「尽快但让出主线程」用 `queueMicrotask` 或 `MessageChannel`。

### await 让出的次数是有意义的

`await` 的每一步都会产生一次微任务，所以「`await` 了几次」会直接体现在输出顺序里：

```javascript
async function f() {
  console.log('3 async 开始');
  await null;                 // 这里的 await 让出一次，后续代码进入微任务队列
  console.log('5 await 之后');
}

console.log('1 同步');
setTimeout(() => console.log('7 timer'), 0);
f();
Promise.resolve().then(() => console.log('6 promise.then'));
console.log('2 同步');

// 输出：
// 1 同步
// 3 async 开始      ← async 函数体在调用时同步执行到第一个 await
// 2 同步
// 5 await 之后      ← 微任务队列：先入队的先执行
// 6 promise.then
// 7 timer           ← 最后才是宏任务
```

这也解释了为什么「明明写了 `await`，某些状态却还没更新」——它只是把后续代码排进微任务，并不会等到渲染、也不会等到所有异步操作完成。

### 长任务与页面卡顿

页面卡顿几乎都源于「某一个宏任务执行太久」——事件循环被占住，渲染、用户输入、定时器全部排队等待。这类任务叫**长任务（Long Task）**，超过 50ms 就会被 Performance 面板标红。

处理方式是把大任务切成小片，每隔一小段让出一次主线程：

```javascript
// ❌ 十万条数据一次渲染完，期间页面完全没响应
// bigArray.forEach((item) => renderItem(item));

// ✅ 分片处理：每片只做一小部分，中间让浏览器有机会渲染和响应点击
async function renderInChunks(items, chunkSize = 200) {
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    chunk.forEach(renderItem);

    // 让出主线程：用宏任务而不是 Promise.resolve()，
    // 因为微任务不会给渲染留出时间
    await new Promise((resolve) => setTimeout(resolve, 0));
  }
}

// 更专业的做法：
// - requestIdleCallback：只在浏览器空闲时执行（兼容性一般，可用 MessageChannel 兜底）
// - scheduler.yield()：框架层提供的新 API，语义就是「让出主线程」
// - Web Worker：把纯计算搬离主线程，这才是根治长任务的方案
```

### 一张表记住「谁先谁后」

| 场景 | 顺序 |
| --- | --- |
| 同步代码 vs 任何异步回调 | 同步代码一定先执行完 |
| 微任务 vs 宏任务 | 微任务先；且当前任务产生的所有微任务都会被清空 |
| `Promise.then` vs `setTimeout(fn, 0)` | `then` 先 |
| `queueMicrotask` vs `Promise.then` | 先入队的先执行，两者优先级相同 |
| `process.nextTick` vs Promise 微任务 | Node 中 `nextTick` 优先 |
| `setImmediate` vs `setTimeout(fn, 0)` | 在 I/O 回调里 `setImmediate` 先；在主模块里不确定 |
| 渲染 vs 微任务 | 渲染在微任务清空之后 |
| `requestAnimationFrame` vs `setTimeout(fn, 0)` | 同一帧内 `rAF` 在渲染前统一执行，`setTimeout` 服从任务队列 |

---

## 本章小结

本章我们深入理解了 JavaScript 的事件循环机制：

1. **单线程模型**：JavaScript 主线程一次只能执行一个任务
2. **同步 vs 异步**：同步阻塞执行，异步不等待结果
3. **调用栈**：跟踪函数调用，LIFO 结构
4. **Web APIs**：浏览器提供的异步能力（setTimeout、fetch 等）
5. **任务队列**：
   - 宏任务：setTimeout、setInterval、I/O、用户交互等（渲染和 `requestAnimationFrame` **不属于**宏任务）
   - 微任务：Promise.then、queueMicrotask、MutationObserver 等
6. **事件循环执行顺序**：执行同步代码 → 清空微任务队列 →（可能）渲染更新 → 取出一个宏任务 → 回到第一步
7. **浏览器 vs Node.js**：Node.js 有更多阶段（timers、pending callbacks、poll、check、close）和 `process.nextTick`、`setImmediate` 等特殊 API
8. **常见误区**：`setTimeout(fn, 0)` 不精确、嵌套超过 5 层后最小延迟变成 4ms；`await` 只让出一个微任务；微任务无限递归会饿死渲染；长任务要切片处理或搬进 Web Worker

---

**下章预告**：下一章我们将学习 **Promise**——处理异步操作的现代化解决方案！ 🚀
