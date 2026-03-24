+++
title = "第 15 章 Promise"
weight = 150
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 15 章 Promise

> Promise 是 JavaScript 异步编程的里程碑——它解决了回调地狱问题，让异步代码看起来像同步代码。学了这一章，你就能优雅地处理"等会儿再告诉你"的场景了！

## 15.1 Promise 基础

### Promise 的三种状态：pending / fulfilled / rejected

Promise 是一个对象，它代表一个**异步操作的最终结果**。就像一个承诺——"我保证以后会告诉你结果"。

Promise 有**三种状态**：

| 状态 | 含义 | 能否转变 |
|------|------|---------|
| `pending` | 进行中（初始状态） | → fulfilled 或 rejected |
| `fulfilled` | 已成功 | → 不能再改变 |
| `rejected` | 已失败 | → 不能再改变 |

```
    pending
   /        \
  ↓          ↓
fulfilled  rejected
```

状态一旦改变，就不能再改变了。这叫做 **Promise 的不可逆性**。

---

### 状态不可逆

```javascript
const promise = new Promise((resolve, reject) => {
  resolve("第一次成功");
  reject("第二次失败"); // 这行无效，因为已经 resolved
});

promise.then(console.log); // "第一次成功"
```

---

### 创建 Promise：new Promise((resolve, reject) => {})

创建 Promise 使用 `new Promise` 构造函数，传入一个执行器函数（executor）：

```javascript
const promise = new Promise((resolve, reject) => {
  // 异步操作
  setTimeout(() => {
    const success = true;

    if (success) {
      resolve("操作成功！"); // 标记为 fulfilled
    } else {
      reject("操作失败了！"); // 标记为 rejected
    }
  }, 1000);
});

console.log("Promise 已创建（pending 状态）");

promise
  .then(result => {
    console.log("成功：" + result);
  })
  .catch(error => {
    console.log("失败：" + error);
  });

console.log("这段代码在 Promise 创建后立即执行");
```

**执行顺序**：
1. "Promise 已创建（pending 状态）"
2. "这段代码在 Promise 创建后立即执行"
3. （1秒后）"成功：操作成功！"

> 💡 因为 Promise 内部是异步执行的，Promise 构造器中的代码会立即执行，但 resolve/reject 会放到微任务队列中。

---

## 15.2 Promise 方法

### then：处理成功

`then` 方法用于处理 Promise 成功（fulfilled）的状态：

```javascript
const promise = Promise.resolve("成功了！");

promise.then(result => {
  console.log(result); // "成功了！"
});
```

`then` 接收一个回调函数，当 Promise 变为 fulfilled 状态时调用。

---

### catch：处理失败

`catch` 方法用于处理 Promise 失败（rejected）的状态：

```javascript
const promise = Promise.reject("出错了！");

promise.catch(error => {
  console.log(error); // "出错了！"
});
```

也可以用 `then` 的第二个参数处理失败：

```javascript
Promise.reject("出错了！")
  .then(
    result => console.log(result),
    error => console.log("失败：" + error)
  );
// "失败：出错了！"
```

---

### finally：无论如何都执行

`finally` 方法的回调无论 Promise 是成功还是失败都会执行，适合做清理工作：

```javascript
function fetchData() {
  return new Promise((resolve, reject) => {
    const success = Math.random() > 0.5;
    setTimeout(() => {
      if (success) {
        resolve("数据");
      } else {
        reject("网络错误");
      }
    }, 1000);
  });
}

fetchData()
  .then(data => console.log("成功：" + data))
  .catch(error => console.log("失败：" + error))
  .finally(() => {
    console.log("无论成功失败，都会执行这个清理操作");
    // 比如：关闭 loading 动画
  });
```

---

### 链式调用

Promise 的 `then`、`catch`、`finally` 都返回一个新的 Promise，支持链式调用：

```javascript
Promise.resolve(1)
  .then(x => x + 1)      // 2
  .then(x => x + 2)      // 4
  .then(x => {
    console.log(x);       // 4
    return x + 3;
  })
  .then(x => console.log(x)); // 7
```

---

### 返回值传递

每个 `then` 的返回值会传递给下一个 `then`：

```javascript
Promise.resolve(5)
  .then(x => x * 2)       // 10
  .then(x => x + 1)       // 11
  .then(x => ({ value: x })) // 返回对象
  .then(obj => console.log(obj.value)); // 11
```

---

### 忘记 return / return undefined 的坑

这是一个常见的坑！如果 `then` 的回调函数没有 `return`，会隐式返回 `undefined`，后续的 `then` 就会收到 `undefined`：

```javascript
// ❌ 错误示例
Promise.resolve(5)
  .then(x => {
    x * 2; // 没有 return！
  })
  .then(x => {
    console.log(x); // undefined！
  });

// ✅ 正确示例
Promise.resolve(5)
  .then(x => {
    return x * 2; // 有 return
  })
  .then(x => {
    console.log(x); // 10
  });
```

---

### catch 之后 return 的值进入下一个 then

如果你在 `catch` 中 `return` 一个值，它会进入下一个 `then`：

```javascript
Promise.reject("出错了")
  .catch(error => {
    console.log("捕获：" + error); // "捕获：出错了"
    return "恢复的值";
  })
  .then(value => {
    console.log("恢复后：" + value); // "恢复后：恢复的值"
  });
```

如果在 `catch` 中抛出错误，会进入下一个 `catch`：

```javascript
Promise.reject("出错了")
  .catch(error => {
    throw new Error("重新抛出");
  })
  .catch(error => {
    console.log("新的错误：" + error.message); // "新的错误：重新抛出"
  });
```

---

## 15.3 Promise 类方法

### Promise.resolve() / Promise.reject()

这两个静态方法用于创建已经 resolved 或 rejected 的 Promise：

```javascript
// 已经 resolved 的 Promise
const resolvedPromise = Promise.resolve("成功了");
resolvedPromise.then(console.log); // "成功了"

// 已经 rejected 的 Promise
const rejectedPromise = Promise.reject("失败了");
rejectedPromise.catch(console.log); // "失败了"
```

`Promise.resolve()` 还会**展开** thenable 对象（具有 `.then` 方法的对象）：

```javascript
const thenable = {
  then(resolve, reject) {
    resolve("从 thenable 来");
  }
};

Promise.resolve(thenable).then(console.log); // "从 thenable 来"
```

---

### Promise.all()：全部成功才成功，用于并发请求

`Promise.all` 接收一个 Promise 数组，只有当**所有** Promise 都成功时，整个 Promise 才成功；如果**任何一个**失败，整个 Promise 就失败。

```javascript
const promise1 = Promise.resolve("结果1");
const promise2 = Promise.resolve("结果2");
const promise3 = Promise.resolve("结果3");

Promise.all([promise1, promise2, promise3])
  .then(results => {
    console.log(results); // ["结果1", "结果2", "结果3"]
  });
```

**典型应用：并发请求并等待所有结果**

```javascript
function fetchUser(userId) {
  return fetch(`/api/user/${userId}`).then(res => res.json());
}

Promise.all([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
]).then(([user1, user2, user3]) => {
  console.log("所有用户加载完成");
  console.log(user1, user2, user3);
});
```

---

### Promise.all() 的错误处理：任一失败则整体失败

```javascript
const promises = [
  Promise.resolve("成功1"),
  Promise.reject("失败2"),
  Promise.resolve("成功3")
];

Promise.all(promises)
  .then(results => console.log(results))
  .catch(error => console.log("整体失败：" + error));
// "整体失败：失败2"
```

---

### Promise.allSettled()（ES2020+）：等待所有 Promise 结束

`Promise.allSettled` 无论成功还是失败都会等待所有 Promise 完成，返回每个 Promise 的**详细状态**：

```javascript
const promises = [
  Promise.resolve("成功1"),
  Promise.reject("失败2"),
  Promise.resolve("成功3")
];

Promise.allSettled(promises).then(results => {
  console.log(results);
  // [
  //   { status: "fulfilled", value: "成功1" },
  //   { status: "rejected", reason: "失败2" },
  //   { status: "fulfilled", value: "成功3" }
  // ]
});
```

> 💡 什么时候用？当你需要知道**所有请求的结果**（无论成功失败）时，用 `allSettled`；当你需要**任一失败就算整体失败**时，用 `all`。

---

### Promise.race()：返回最快的，用于超时处理

`Promise.race` 返回**最快完成**的那个 Promise（无论成功还是失败）：

```javascript
const slow = new Promise(resolve => setTimeout(() => resolve("慢"), 1000));
const fast = new Promise(resolve => setTimeout(() => resolve("快"), 500));

Promise.race([slow, fast])
  .then(result => console.log("获胜的是：" + result));
// "获胜的是：快"（1秒后）
```

**典型应用：请求超时**

```javascript
function fetchWithTimeout(url, timeout = 3000) {
  const fetchPromise = fetch(url);
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  return Promise.race([fetchPromise, timeoutPromise]);
}

fetchWithTimeout("/api/data", 1000)
  .then(data => console.log(data))
  .catch(error => console.log(error.message)); // "请求超时"（如果1秒内没响应）
```

---

### Promise.any()（ES2021+）：返回第一个成功的，忽略失败

`Promise.any` 与 `race` 类似，但返回**第一个成功**的 Promise，忽略失败：

```javascript
const promises = [
  Promise.reject("失败1"),
  Promise.resolve("成功2"),
  Promise.resolve("成功3")
];

Promise.any(promises)
  .then(result => console.log("第一个成功：" + result));
// "第一个成功：成功2"
```

如果**所有** Promise 都失败了，会抛出 `AggregateError`：

```javascript
Promise.any([
  Promise.reject("失败1"),
  Promise.reject("失败2")
])
  .then(result => console.log(result))
  .catch(error => {
    console.log(error.errors); // ["失败1", "失败2"]
  });
```

---

### all vs allSettled vs race vs any 选择指南

| 方法 | 成功条件 | 失败条件 | 返回值 |
|------|---------|---------|--------|
| `all` | 全部成功 | 任一失败 | 所有结果的数组 |
| `allSettled` | 总是等待所有完成 | 从不失败 | 每个 Promise 的状态对象 |
| `race` | 任意一个完成 | 任意一个失败 | 最快完成的结果 |
| `any` | 任意一个成功 | 全部失败 | 第一个成功的结果 |

---

## 15.4 Promise 进阶

### Promise 的微任务本质：then 是微任务

Promise 的 `.then`、`.catch`、`.finally` 的回调都是作为**微任务**执行的：

```javascript
console.log("1（同步）");

Promise.resolve()
  .then(() => console.log("3（微任务）"));

setTimeout(() => console.log("4（宏任务）"), 0);

console.log("2（同步）");

// 输出：
// 1（同步）
// 2（同步）
// 3（微任务）
// 4（宏任务）
```

---

### new Promise 构造函数是同步执行的

Promise 构造器中的代码是**同步执行**的：

```javascript
console.log("1");

new Promise((resolve, reject) => {
  console.log("2（Promise 内部同步执行）");
  resolve();
}).then(() => console.log("4（微任务）"));

console.log("3");

// 输出：
// 1
// 2（Promise 内部同步执行）
// 3
// 4（微任务）
```

---

### thenable 对象

thenable 是具有 `.then` 方法的对象，Promise.resolve() 会"展开"它：

```javascript
const thenable = {
  then(resolve, reject) {
    setTimeout(() => resolve("resolved!"), 1000);
  }
};

Promise.resolve(thenable)
  .then(value => console.log(value)); // "resolved!"（1秒后）
```

这意味着任何具有 `.then` 方法的对象都可以当作 Promise 使用，很多异步库就是利用这个特性实现的。

---

### 手写一个简易 Promise

理解了 Promise 的原理，我们可以自己实现一个简易版本：

```javascript
class SimplePromise {
  constructor(executor) {
    this.state = "pending";
    this.value = undefined;
    this.callbacks = [];

    const resolve = (value) => {
      if (this.state !== "pending") return;
      this.state = "fulfilled";
      this.value = value;
      this.callbacks.forEach(cb => cb.onFulfilled(value));
    };

    const reject = (reason) => {
      if (this.state !== "pending") return;
      this.state = "rejected";
      this.value = reason;
      this.callbacks.forEach(cb => cb.onRejected(reason));
    };

    try {
      executor(resolve, reject);
    } catch (error) {
      reject(error);
    }
  }

  then(onFulfilled, onRejected) {
    return new SimplePromise((resolve, reject) => {
      const handleCallback = (callback, fallback) => {
        try {
          const result = callback ? callback(this.value) : fallback(this.value);
          resolve(result);
        } catch (error) {
          reject(error);
        }
      };

      if (this.state === "fulfilled") {
        queueMicrotask(() => handleCallback(onFulfilled, v => v));
      } else if (this.state === "rejected") {
        queueMicrotask(() => handleCallback(onRejected, throw it => { throw it; }));
      } else {
        this.callbacks.push({
          onFulfilled: () => handleCallback(onFulfilled, v => v),
          onRejected: () => handleCallback(onRejected, throw it => { throw it; })
        });
      }
    });
  }

  catch(onRejected) {
    return this.then(null, onRejected);
  }

  finally(onFinally) {
    return this.then(
      value => { onFinally(); return value; },
      reason => { onFinally(); throw reason; }
    );
  }
}

// 测试
new SimplePromise(resolve => resolve("成功"))
  .then(value => console.log(value)); // "成功"
```

> 💡 这个简易 Promise 只实现了核心功能，真正完整的 Promise 实现（如 Promise/A+ 规范）要复杂得多。如果你想深入了解，可以去看 Promise/A+ 规范的实现。

---

### 手写 Promise.all

理解了 `Promise.all` 的原理，我们可以自己实现：

```javascript
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;

    if (promises.length === 0) {
      resolve([]);
      return;
    }

    promises.forEach((promise, index) => {
      Promise.resolve(promise)
        .then(value => {
          results[index] = value;
          completed++;

          if (completed === promises.length) {
            resolve(results);
          }
        })
        .catch(reason => {
          reject(reason);
        });
    });
  });
}

// 测试
promiseAll([
  Promise.resolve(1),
  Promise.resolve(2),
  Promise.resolve(3)
]).then(console.log); // [1, 2, 3]

promiseAll([
  Promise.resolve(1),
  Promise.reject("出错了"),
  Promise.resolve(3)
]).catch(console.log); // "出错了"
```

---

## 本章小结

本章我们深入学习了 Promise：

1. **Promise 基础**：
   - 三种状态：pending / fulfilled / rejected
   - 状态不可逆
   - `new Promise` 创建

2. **Promise 方法**：
   - `then`：处理成功
   - `catch`：处理失败
   - `finally`：无论如何都执行
   - 链式调用和返回值传递
   - 忘记 return 的坑

3. **Promise 类方法**：
   - `Promise.resolve/reject`
   - `Promise.all`：全部成功才成功
   - `Promise.allSettled`：等待所有完成
   - `Promise.race`：返回最快的
   - `Promise.any`：返回第一个成功的

4. **Promise 进阶**：
   - then 是微任务
   - thenable 对象
   - 手写简易 Promise
   - 手写 Promise.all

> 📊 图示：Promise 状态转换
>
> ```mermaid
> stateDiagram-v2
>     [*] --> Pending: new Promise
>     Pending --> Fulfilled: resolve()
>     Pending --> Rejected: reject()
>     Fulfilled --> [*]
>     Rejected --> [*]
>
>     note right of Fulfilled
>       状态不可逆
>     end note
> ```

---

**下章预告**：下一章我们将学习 **async/await 与 Generator**——让异步代码看起来像同步代码！ 🚀

