+++
title = "第 16 章 async/await 与 Generator"
weight = 160
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 16 章 async/await 与 Generator

> async/await 是 Promise 的"语法糖"，让异步代码看起来像同步代码。Generator 则是一种可以暂停和恢复的函数。它们都是 ES6+ 引入的强大特性。

## 16.1 async 函数

### async 关键字：函数返回 Promise

`async` 关键字用于声明一个异步函数。异步函数总是返回一个 **Promise**，即使你显式返回的是一个非 Promise 值：

```javascript
async function greet(name) {
  return "你好，" + name + "！";
}

console.log(greet("小明")); // Promise { "你好，小明！" }

greet("小明").then(console.log); // "你好，小明！"
```

如果 async 函数显式返回一个 Promise，那就直接返回那个 Promise：

```javascript
async function fetchData() {
  return fetch("/api/data").then(res => res.json());
}

console.log(fetchData()); // Promise（来自 fetch）
```

---

### await 关键字：等待 Promise 结果

`await` 关键字只能在 `async` 函数中使用，它会**暂停函数执行**，等待 Promise 结果，然后返回该结果：

```javascript
async function fetchUser() {
  const response = await fetch("/api/user/1");
  const user = await response.json();
  return user;
}
```

**对比 Promise 写法**：

```javascript
// Promise 写法
function fetchUser() {
  return fetch("/api/user/1")
    .then(response => response.json());
}

// async/await 写法（更直观）
async function fetchUser() {
  const response = await fetch("/api/user/1");
  const user = await response.json();
  return user;
}
```

> 💡 `await` 暂停的是 async 函数内部的执行，不会暂停外部代码！

```javascript
async function demo() {
  console.log("1");
  await Promise.resolve();
  console.log("3");
}

console.log("2");
demo();
console.log("4");

// 输出：
// 2
// 1
// 4
// 3
```

---

### async/await 处理错误：try...catch

错误处理是 async/await 的一大优势——可以用 `try...catch` 来捕获异步错误：

```javascript
async function fetchData() {
  try {
    const response = await fetch("/api/data");
    if (!response.ok) {
      throw new Error("HTTP 错误：" + response.status);
    }
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.log("获取数据失败：" + error.message);
  }
}
```

**对比 Promise 的 `.catch`**：

```javascript
// Promise 写法
fetch("/api/data")
  .then(response => {
    if (!response.ok) throw new Error("HTTP 错误");
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.log(error));

// async/await 写法
async function fetchData() {
  try {
    const response = await fetch("/api/data");
    if (!response.ok) throw new Error("HTTP 错误");
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.log(error);
  }
}
```

> 💡 `try...catch` 可以捕获同步和异步错误，比 `.catch()` 更统一。

---

## 16.2 async/await 进阶

### 并行执行：Promise.all + await

如果你有多个独立的异步操作想要**并行执行**，不要用 `await` 一个一个等待，要用 `Promise.all`：

```javascript
// ❌ 串行执行（慢）
async function fetchAllSlow() {
  const user = await fetchUser();    // 等 1 秒
  const posts = await fetchPosts();  // 再等 1 秒
  const comments = await fetchComments(); // 又等 1 秒
  // 总共 3 秒
}

// ✅ 并行执行（快）
async function fetchAllFast() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),      // 同时开始
    fetchPosts(),     // 同时开始
    fetchComments()   // 同时开始
  ]);
  // 总共 1 秒
}
```

> 💡 记住：`await` 会暂停函数执行，如果多个操作之间没有依赖，就用 `Promise.all` 并行执行！

---

### 循环中的 await：串行问题

在 `for` 循环中使用 `await` 是**串行执行**的：

```javascript
async function processItems(items) {
  const results = [];

  for (const item of items) {
    const result = await processItem(item); // 每次都要等待
    results.push(result);
  }

  return results;
}
```

如果你想**并行处理**，可以用 `map` + `Promise.all`：

```javascript
async function processItems(items) {
  const promises = items.map(item => processItem(item));
  const results = await Promise.all(promises);
  return results;
}
```

---

### forEach 中的 await：失效问题与解决方案

**`forEach` 中的 `await` 不起作用！** 这是因为 `forEach` 不会等待 Promise 完成：

```javascript
async function demo() {
  const items = [1, 2, 3];

  // ❌ 错误：不会等待
  items.forEach(async (item) => {
    await processItem(item);
    console.log("完成：" + item);
  });

  console.log("全部完成？"); // 这行会先执行！
}
```

`forEach` 不会处理 async 函数的返回值，所以 `await` 在这里毫无意义。

**正确做法：用 `for...of` 循环**：

```javascript
async function demo() {
  const items = [1, 2, 3];

  // ✅ 正确：用 for...of
  for (const item of items) {
    await processItem(item);
    console.log("完成：" + item);
  }

  console.log("全部完成！"); // 这行会在所有完成后执行
}
```

---

### async/await vs Promise.then 对比

两种写法都可以实现异步流程控制：

```javascript
// Promise 链式调用
function fetchUserPromise() {
  return fetch("/api/user")
    .then(response => response.json())
    .then(user => fetch(`/api/posts?userId=${user.id}`))
    .then(response => response.json())
    .then(posts => console.log(posts));
}

// async/await
async function fetchUserAsync() {
  const userResponse = await fetch("/api/user");
  const user = await userResponse.json();
  const postsResponse = await fetch(`/api/posts?userId=${user.id}`);
  const posts = await postsResponse.json();
  console.log(posts);
}
```

**选择建议**：
- 简单链式：Promise.then 更简洁
- 复杂逻辑：async/await 更易读
- 需要并行：Promise.all
- 错误处理：`try...catch` vs `.catch()`

---

## 16.3 Generator 函数

### function* 与 yield：函数可暂停可恢复

Generator（生成器）是一种可以**暂停和恢复**的函数。它不像普通函数那样一旦调用就必须执行到底。

```javascript
// 定义 Generator 函数
function* numberGenerator() {
  console.log("开始");
  yield 1;
  console.log("暂停后继续");
  yield 2;
  console.log("再次暂停后继续");
  yield 3;
  console.log("结束");
  return "完成";
}

// 创建 Generator 对象
const gen = numberGenerator();

console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { value: 3, done: false }
console.log(gen.next()); // { value: "完成", done: true }
```

**执行过程**：
1. 第一次调用 `gen.next()`，函数开始执行，遇到第一个 `yield` 暂停
2. 第二次调用 `gen.next()`，从暂停处继续执行
3. 直到遇到 `return` 或函数结束，`done` 变为 `true`

---

### next()：控制函数执行，返回 { value, done }

`next()` 是 Generator 的核心方法：
- 返回 `{ value, done }` 对象
- `value` 是 yield 后面表达式的值（或 `return` 的值）
- `done` 表示 Generator 是否已经结束

```javascript
function* simpleGenerator() {
  yield "第一";
  yield "第二";
  return "最后";
}

const gen = simpleGenerator();

console.log(gen.next()); // { value: "第一", done: false }
console.log(gen.next()); // { value: "第二", done: false }
console.log(gen.next()); // { value: "最后", done: true }
console.log(gen.next()); // { value: undefined, done: true }（已经结束）
```

---

### yield 传值：next(value)

`next()` 可以传递值给 Generator，这个值会作为**上一个 `yield` 表达式的结果**：

```javascript
function* calculator() {
  const first = yield "请输入第一个数";
  const second = yield "请输入第二个数";
  return Number(first) + Number(second);
}

const gen = calculator();
console.log(gen.next().value);    // "请输入第一个数"
console.log(gen.next("10").value); // "请输入第二个数"（10 作为第一个 yield 的结果）
console.log(gen.next("20").value); // 30（"10" + "20"）
```

**应用：实现简单的状态机**

```javascript
function* stateMachine() {
  let state = "idle";

  while (true) {
    const event = yield state;

    switch (state) {
      case "idle":
        if (event === "start") state = "running";
        break;
      case "running":
        if (event === "stop") state = "idle";
        if (event === "pause") state = "paused";
        break;
      case "paused":
        if (event === "resume") state = "running";
        if (event === "stop") state = "idle";
        break;
    }
  }
}

const machine = stateMachine();
console.log(machine.next().value);      // "idle"
console.log(machine.next("start").value);  // "running"
console.log(machine.next("pause").value); // "paused"
console.log(machine.next("resume").value); // "running"
```

---

### return() / throw()

- `return(value)`：提前结束 Generator，返回指定值
- `throw(error)`：在 Generator 暂停位置抛出错误

```javascript
function* gen() {
  yield 1;
  yield 2;
  yield 3;
}

const g = gen();

console.log(g.next());     // { value: 1, done: false }
console.log(g.return("结束")); // { value: "结束", done: true }
console.log(g.next());     // { value: undefined, done: true }
```

```javascript
function* gen() {
  try {
    yield 1;
    yield 2;
  } catch (e) {
    console.log("捕获错误：" + e);
  }
}

const g = gen();
console.log(g.next());          // { value: 1, done: false }
console.log(g.throw(new Error("出错了"))); // "捕获错误：出错了" { value: undefined, done: true }
```

---

### for...of 自动遍历 Generator

`for...of` 可以自动遍历 Generator，不需要手动调用 `next()`：

```javascript
function* numberGenerator() {
  yield 1;
  yield 2;
  yield 3;
}

for (const num of numberGenerator()) {
  console.log(num);
}
// 输出：1, 2, 3
```

> ⚠️ 注意：`for...of` 不会访问 `return` 的值！

```javascript
function* gen() {
  yield 1;
  yield 2;
  return "被跳过的值";
}

for (const value of gen()) {
  console.log(value); // 1, 2（不会打印 "被跳过的值"）
}
```

---

### Generator 与迭代器的关系

Generator 实现了**迭代器协议**（Iterator Protocol），所以它是可迭代的：

```javascript
function* gen() {
  yield 1;
  yield 2;
}

const iterator = gen()[Symbol.iterator]();
console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }
console.log(iterator.next()); // { value: undefined, done: true }
```

这意味着 Generator 可以使用展开运算符、数组方法等：

```javascript
function* range(start, end) {
  for (let i = start; i <= end; i++) {
    yield i;
  }
}

console.log([...range(1, 5)]);      // [1, 2, 3, 4, 5]
console.log(Array.from(range(1, 5))); // [1, 2, 3, 4, 5]
```

---

### Generator 的惰性求值

Generator 是**惰性求值**的——只在需要时才计算下一个值，非常适合处理大量数据或无限序列：

```javascript
// 无限序列
function* fibonacci() {
  let [a, b] = [0, 1];
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// 取前10个，不需要定义10个数的数组
const fib = fibonacci();
for (let i = 0; i < 10; i++) {
  console.log(fib.next().value); // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
}
```

> 💡 想象一下如果用普通数组来实现，需要先计算所有斐波那契数，会占用大量内存。而 Generator 按需计算，内存占用是 O(1)！

---

## 本章小结

本章我们学习了 async/await 和 Generator：

1. **async 函数**：
   - `async` 函数始终返回 Promise
   - `await` 等待 Promise 结果（只能在 async 函数中使用）
   - 错误处理用 `try...catch`

2. **async/await 进阶**：
   - 并行执行：用 `Promise.all` + `await`
   - 循环中的 await：串行执行
   - `forEach` 中的 await 不起作用（用 `for...of`）

3. **Generator 函数**：
   - `function*` 定义，`yield` 暂停
   - `next()` 控制执行，返回 `{ value, done }`
   - 可以传值给上一个 `yield`
   - `for...of` 自动遍历
   - 实现迭代器协议
   - 惰性求值，适合处理大数据

> 📊 图示：async/await vs Promise
>
> ```mermaid
> graph LR
>     A[Promise.then链式] --> B[优点：链式调用]
>     A --> C[缺点：复杂时难读]
>
>     D[async/await] --> E[优点：像同步代码]
>     D --> F[缺点：需要捕获错误]
>
>     G[两者可以互相转换] --> H[本质都是Promise]
> ```

---

**下章预告**：下一章我们将进入 **面向对象编程** 的世界——原型链、继承、class 语法！准备好了吗？ 🧩

