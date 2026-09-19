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

> 💡 控制台里看到的 `Promise { '你好，小明！' }` 只是一份「预览」。Promise 刚创建时状态是 pending，值是在函数执行结束后才被记录的；你在控制台展开它看到的是展开那一刻的状态。想确认结果，永远用 `await` 或 `.then()`。

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

> 💡 `try...catch` 能同时接住同步抛出的错误和 `await` 表达式拒绝的 Promise，所以看起来比 `.catch()` 更统一。但它有一个必须记住的边界：**只有被 `await`（或 `return`）的 Promise 才会进入 `catch`**。

```javascript
async function wrong() {
  try {
    // ❌ 没有 await：这个失败不会进入下面的 catch
    Promise.reject(new Error("没人接住我"));
    return "看起来成功了";
  } catch (e) {
    console.log("不会执行");
  }
}
```

要并行发多个请求又想在失败时统一处理，应当先把它们放进 `Promise.all` / `Promise.allSettled` 再 `await`。

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
console.log(gen.next("20").value); // 30（Number("10") + Number("20")）
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

### yield*：委托给另一个可迭代对象

`yield*` 把控制权交给另一个 Generator 或任何可迭代对象，相当于把它产出的值「摊平」到当前 Generator 里：

```javascript
function* inner() {
  yield "a";
  yield "b";
  return "inner 的返回值";
}

function* outer() {
  const result = yield* inner();   // 逐个产出 a、b
  // yield* 的「返回值」是内层 Generator 的 return 值
  yield "内层结束：" + result;
}

console.log([...outer()]); // ["a", "b", "内层结束：inner 的返回值"]

// 也可以委托给数组、字符串等任何可迭代对象
function* spread() {
  yield* [1, 2];
  yield* "ab";
}
console.log([...spread()]); // [1, 2, "a", "b"]
```

递归遍历树结构就是它的经典用法：

```javascript
function* walk(node) {
  yield node.name;
  for (const child of node.children ?? []) {
    yield* walk(child);       // 递归委托，天然实现深度优先
  }
}

const tree = { name: "root", children: [{ name: "a" }, { name: "b", children: [{ name: "b1" }] }] };
console.log([...walk(tree)]); // ["root", "a", "b", "b1"]
```

### return() 与 finally：提前结束时的清理

提前 `return()` 或 `throw()` 会让 Generator 在暂停处「提前退出」，此时 `try...finally` 里的清理逻辑依然会执行——这是 Generator 管理资源的重要能力：

```javascript
function* withResource() {
  try {
    yield "占用中";
    yield "仍然占用中";
  } finally {
    console.log("释放资源");     // 正常结束、提前 return、抛错都会执行
  }
}

const g = withResource();
console.log(g.next().value);    // "占用中"
g.return();                     // 先打印 "释放资源"，再返回 { value: undefined, done: true }

// 典型用途：一段需要用完就关的逻辑，例如临时加锁、打开文件、切换 loading 状态
```

## 16.4 异步迭代与顶层 await

### async Generator 与 for await...of

把 `async` 和 `function*` 组合起来，就得到**异步生成器**：它产出的每个值都可以是异步等待的，用 `for await...of` 消费：

```javascript
async function* fetchPages(baseUrl) {
  let page = 1;
  while (true) {
    const res = await fetch(`${baseUrl}?page=${page}`);
    const data = await res.json();
    if (data.items.length === 0) return;   // 没有更多数据，结束
    yield data.items;
    page++;
  }
}

// 分页数据边取边用，不必先把所有页都加载到内存里
for await (const items of fetchPages("/api/list")) {
  console.log(`本页 ${items.length} 条`);
  if (items.length < 10) break;            // 也可以提前结束
}
```

异步生成器同样实现了 `Symbol.asyncIterator`，并且它是**惰性**的：`for await...of` 每次循环才会真正发起下一次请求。

### 顶层 await

在 ES 模块（`type="module"` / `.mjs` / 打包后的模块）里，可以直接在顶层使用 `await`，不必包一层 `async` 函数：

```javascript
// config.mjs
const res = await fetch("/api/config");
export const config = await res.json();
```

注意三点：

- 只有模块支持，普通 `<script>` 里会直接报语法错误；
- 顶层 `await` 会让**整个模块的加载变成异步**，依赖它的模块都会等它完成；
- 不要在顶层 `await` 一个永不结束的 Promise，那会让页面一直白屏。

## 16.5 常见错误与最佳实践

```javascript
// 1. 忘了 await：拿到的是 Promise 而不是值
async function bad() {
  const user = getUser();          // ❌ 是 Promise
  console.log(user.name);          // undefined
  const user2 = await getUser();   // ✅
}

// 2. await 一个非 Promise 值也没问题，但会白白多让出一个微任务
await 123;   // 等价于 await Promise.resolve(123)

// 3. 串行 vs 并发的选择要看业务约束
//    默认应该并发；但如果后端有速率限制、或者后面的请求依赖前面的结果，就必须串行
async function saveAll(records) {
  // 并发可能触发限流，这里的串行是刻意的
  for (const record of records) {
    await save(record);
  }
}

// 4. 并发数量需要控制时，用「分批」而不是一次性全部发出
async function runWithLimit(tasks, limit = 5) {
  const results = [];
  for (let i = 0; i < tasks.length; i += limit) {
    const batch = tasks.slice(i, i + limit);
    results.push(...(await Promise.all(batch.map((task) => task()))));
  }
  return results;
}

// 5. 不要用 async 函数当「立即执行的构造函数」或依赖它的返回值同步可用
//    async 函数永远返回 Promise，任何「马上就是结果」的期待都是错的
```

还有两个容易忽略的点：

- **`await` 会丢失一部分调用栈**。在 `try...catch` 里打印 `error.stack` 时，往往只能看到 `await` 之后的部分，排查时可以配合 `error.cause` 或自己记录日志。
- **不要在循环里做「并发量不受控」的 `Promise.all`**，几千个并发请求会把浏览器和后端一起拖垮，分批或使用并发上限更稳妥。

---

## 本章小结

本章我们学习了 async/await 和 Generator：

1. **async 函数**：
   - `async` 函数始终返回 Promise
   - `await` 等待 Promise 结果（只能在 async 函数中使用）
   - 错误处理用 `try...catch`，但只有被 `await` 的 Promise 才会进入 `catch`

2. **async/await 进阶**：
   - 并行执行：用 `Promise.all` + `await`
   - 循环中的 await：串行执行
   - `forEach` 中的 await 不起作用（用 `for...of`）
   - 需要限流时按批处理，不要一次并发上千个请求

3. **Generator 函数**：
   - `function*` 定义，`yield` 暂停
   - `next()` 控制执行，返回 `{ value, done }`
   - 可以传值给上一个 `yield`（作为 `yield` 表达式的结果）
   - `for...of` 自动遍历
   - 实现迭代器协议
   - 惰性求值，适合处理大数据
   - `yield*` 委托、`return()`/`throw()` 与 `finally` 清理

4. **异步迭代与顶层 await**：
   - `async function*` 产出异步序列，配合 `for await...of` 消费
   - ES 模块顶层可以直接 `await`

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
