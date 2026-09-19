+++
title = "第 35 章 错误处理"
weight = 350
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 35 章 错误处理

程序不可能永远正确运行。错误处理就是让程序在出问题时能够优雅地"认错"，而不是直接崩溃。

## 35.1 错误处理基础

### try...catch / try...catch...finally

```javascript
try {
    // 尝试执行这段代码
    const result = riskyOperation();
    console.log('操作成功：', result);
} catch (error) {
    // 如果出错，执行这里
    console.error('出错了：', error.message);
} finally {
    // 不管成功还是失败，都会执行
    console.log('无论成功失败，我都会执行');
}
```

### Error 对象：message / name / stack

```javascript
try {
    throw new Error('出错了！');
} catch (error) {
    console.log('错误信息：', error.message); // 错误信息
    console.log('错误名称：', error.name);   // Error
    console.log('错误堆栈：', error.stack);   // 详细错误位置
}
```

### 内置错误类型：ReferenceError / TypeError / SyntaxError / RangeError / URIError

```javascript
// ReferenceError：引用错误
try {
    console.log(undefinedVariable); // 未定义的变量
} catch (e) {
    console.log(e.name); // 打印结果: ReferenceError
}

// TypeError：类型错误
try {
    null.method(); // null 没有方法
} catch (e) {
    console.log(e.name); // 打印结果: TypeError
}

// SyntaxError：语法错误
// 注意区分两种情况：
// 1. 脚本自身的语法错误在「解析阶段」就被发现，整个脚本都不会执行，
//    这时 try...catch 根本没有机会运行，自然也就捕获不到。
// 2. 运行时才去解析字符串的 API（eval、JSON.parse、new Function、
//    import() 等）抛出的 SyntaxError 是普通异常，可以被 try...catch 捕获。
try {
    JSON.parse('{ invalid }');
} catch (e) {
    console.log(e.name); // 打印结果: SyntaxError
}

try {
    eval('const = 1'); // eval 内部解析失败，抛出 SyntaxError 异常
} catch (e) {
    console.log(e.name); // 打印结果: SyntaxError
}

// RangeError：范围错误
try {
    const arr = new Array(-1); // 数组长度不能为负数
} catch (e) {
    console.log(e.name); // 打印结果: RangeError
}

// URIError：URI 错误
try {
    decodeURIComponent('%'); // 无效的 URI 编码
} catch (e) {
    console.log(e.name); // 打印结果: URIError
}
```

### throw：手动抛出

```javascript
// 抛出字符串
throw '出错了！';

// 抛出数字
throw 404;

// 抛出对象
throw {
    code: 'NOT_FOUND',
    message: '资源未找到'
};

// 抛出 Error 对象
throw new Error('出错了！');
```

语法上 `throw` 可以抛出任意值，但**实际开发中应当只抛出 Error（或其子类）对象**。原因很直接：

- 只有 Error 对象才带 `name`、`message`、`stack`，抛字符串会丢掉堆栈，排查问题时要靠猜。
- `e instanceof Error` 判断会失效，上层的统一错误处理逻辑只能写成一堆 `typeof` 分支。
- 一些工具链（错误上报、日志采集、Sentry 等）默认按 Error 结构解析，抛字符串会丢失上下文。

```javascript
// ❌ 不要这样写
throw '用户不存在';

// ✅ 推荐：需要额外信息就挂在对象上
const err = new Error('用户不存在');
err.code = 'USER_NOT_FOUND';
err.statusCode = 404;
throw err;
```

### 可选 catch 绑定（ES2019）

如果你确实不需要错误对象，可以省略 `catch` 后面的括号和变量名：

```javascript
// 只想在出错时走一条分支，不关心错误内容
try {
    JSON.parse(maybeBrokenJson);
} catch {
    console.log('这段 JSON 不合法，按空对象处理');
}
```

省略绑定时，`catch` 块内部无法引用错误对象，适合「有兜底逻辑、不需要上报」的场景。

### Error.cause（ES2022+）

```javascript
try {
    try {
        JSON.parse('invalid json');
    } catch (e) {
        // 在捕获错误时，附加 cause 信息
        throw new Error('解析失败', { cause: e });
    }
} catch (e) {
    console.log(e.message); // 打印结果: 解析失败
    console.log(e.cause); // 打印结果: SyntaxError: Unexpected token 'i'
}
```

### 自定义错误类型

```javascript
class ValidationError extends Error {
    constructor(message, field) {
        super(message);
        this.name = 'ValidationError';
        this.field = field;
    }
}

function validateAge(age) {
    if (typeof age !== 'number') {
        throw new ValidationError('年龄必须是数字', 'age');
    }
    if (age < 0 || age > 150) {
        throw new ValidationError('年龄必须在 0-150 之间', 'age');
    }
}

try {
    validateAge('abc');
} catch (e) {
    if (e instanceof ValidationError) {
        console.log('验证错误：', e.message, '字段：', e.field);
    } else {
        console.log('其他错误：', e.message);
    }
}
```

自定义错误有两个容易踩的坑：

1. **子类的 `name` 不会自动变成类名**，`Error` 的构造函数把 `name` 固定为 `'Error'`，所以必须手动赋值 `this.name = 'ValidationError'`，否则日志里全是 `Error`。
2. **`error.cause` 要在 `super()` 的第二个参数里传**，写成 `super(message, { cause })`。如果先 `super(message)` 再 `this.cause = cause`，在部分环境/序列化工具中 `cause` 不会被识别为标准字段。

```javascript
class HttpError extends Error {
    constructor(message, status, options) {
        super(message, options);      // options 里可以带 cause
        this.name = 'HttpError';      // 手动设置，否则 instanceof 对但 name 仍是 Error
        this.status = status;
    }
}

try {
    try {
        await fetch('https://example.invalid/api');
    } catch (e) {
        throw new HttpError('接口请求失败', 502, { cause: e });
    }
} catch (e) {
    console.log(e instanceof HttpError); // true
    console.log(e.name);                 // 'HttpError'
    console.log(e.cause);                // TypeError: Failed to fetch
}
```

下一节，我们来学习异步错误处理！

## 35.2 异步错误处理

### try...catch 对 Promise 无效（同步代码中捕获）

```javascript
// ❌ try...catch 不能捕获异步代码中的错误
try {
    setTimeout(function() {
        throw new Error('异步错误！');
    }, 1000);
} catch (e) {
    console.log('捕获到了？'); // 不会执行！
}
console.log('try...catch 之外的代码'); // 立即执行
```

### async/await 的错误处理：try...catch

```javascript
async function fetchData() {
    try {
        const response = await fetch('https://invalid-url');
        const data = await response.json();
        return data;
    } catch (error) {
        console.log('请求失败：', error.message);
        return null;
    }
}

fetchData();
```

还有一点必须记住：**`async` 函数永远不会「抛出」异常，它只会返回一个 rejected 的 Promise**。所以调用方如果只用同步的 `try...catch` 包住一个 async 函数调用，是捕获不到错误的。

```javascript
async function boom() {
    throw new Error('内部出错');
}

// ❌ 捕获不到：boom() 只是返回了一个 rejected 的 Promise
try {
    boom();
} catch (e) {
    console.log('不会执行');
}

// ✅ 三种正确写法
// 1. 调用方也是 async，直接 await + try...catch
async function caller() {
    try {
        await boom();
    } catch (e) {
        console.log('方式 1 捕获：', e.message);
    }
}
caller();

// 2. 不 await，用 .catch() 挂兜底
boom().catch((e) => console.log('方式 2 捕获：', e.message));

// 3. 交给全局 unhandledrejection（见 35.3，属于兜底而非方案）
```

如果只是想在成功、失败时都做同一件清理工作，用 `finally` 更清晰：

```javascript
async function loadUser(id) {
    showLoading();
    try {
        const res = await fetch(`/api/users/${id}`);
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);   // fetch 只在网络层失败时 reject
        }
        return await res.json();
    } finally {
        hideLoading();   // 成功、失败都会执行，不需要在 catch 里重复写一遍
    }
}
```

> 注意：`fetch()` 只有在**网络层出错**（断网、DNS 失败、跨域被拦截）时才 reject。服务器返回 404、500 都属于「请求成功」，`res.ok` 为 `false`，必须自己判断后抛错，否则会被当成正常数据继续处理。

### Promise 的 .catch()

```javascript
fetch('https://invalid-url')
    .then(function(response) {
        return response.json();
    })
    .catch(function(error) {
        console.log('请求失败：', error.message);
    })
    .finally(function() {
        console.log('无论成功失败都会执行');   // 收尾工作放这里
    });
```

### 并发 Promise 的错误聚合

一次并发发多个请求时，不同的组合方法对错误的处理方式完全不同，这是日常最容易写错的点之一。

| 方法 | 遇到一个失败时 | 适合场景 |
| --- | --- | --- |
| `Promise.all` | 立刻 reject，只拿到**第一个**错误，其余结果全部丢弃 | 少了任何一个就没法继续（如首屏必需数据） |
| `Promise.allSettled` | 永不 reject，返回每个任务的 `{status, value/reason}` | 允许部分失败（如仪表盘的多个卡片） |
| `Promise.any` | 全部失败才 reject，抛出 `AggregateError` | 有多个数据源，任何一个成功即可 |
| `Promise.race` | 第一个敲定（成功或失败）的结果直接决定整体 | 超时控制 |

```javascript
// allSettled：想拿到「哪些成功、哪些失败」，必须自己遍历判断
const results = await Promise.allSettled([
    fetch('/api/a').then((r) => r.json()),
    fetch('/api/b').then((r) => r.json()),
]);

for (const item of results) {
    if (item.status === 'fulfilled') {
        console.log('成功：', item.value);
    } else {
        console.log('失败：', item.reason.message);
    }
}

// any：全部失败时抛出 AggregateError，它的 errors 属性装着每一个失败原因
try {
    const data = await Promise.any([
        fetch('https://api-a.example.com/data').then((r) => r.json()),
        fetch('https://api-b.example.com/data').then((r) => r.json()),
    ]);
    console.log(data);
} catch (e) {
    console.log(e instanceof AggregateError); // true
    console.log(e.errors.map((err) => err.message));
}
```

### AggregateError（ES2021）

`AggregateError` 是内置的「多个错误打包」类型，`errors` 属性是一个数组，`cause`、`message` 用法与普通 `Error` 一致。除了 `Promise.any`，Node 的部分 API（如多地址连接失败）也会抛出它。自己实现批量任务时也可以主动用它，避免把错误信息拼成一行字符串：

```javascript
const errors = [];
for (const file of files) {
    try {
        parse(file);
    } catch (e) {
        errors.push(e);
    }
}
if (errors.length) {
    throw new AggregateError(errors, `${errors.length} 个文件解析失败`);
}
```

下一节，我们来学习全局错误处理！

## 35.3 全局错误处理

### window.onerror

```javascript
window.onerror = function(message, source, lineno, colno, error) {
    console.log('错误信息：', message);
    console.log('错误来源：', source);
    console.log('行号：', lineno);
    console.log('列号：', colno);
    console.log('错误对象：', error);
    
    // 返回 true 表示已处理，不再向上抛出
    return true;
};

// 触发错误
// window.onerror 会被调用
```

### unhandledrejection：未处理的 Promise rejection

```javascript
// 当 Promise 被 reject 但没有 .catch() 处理时触发
window.addEventListener('unhandledrejection', function(event) {
    console.log('未处理的 Promise 错误：');
    console.log('错误对象：', event.reason);
    
    // 阻止默认行为（浏览器控制台警告）
    event.preventDefault();
});

Promise.reject(new Error('未处理的错误！'));
```

`window.onerror` 虽然常用，但它有明确的覆盖范围，以下几点经常被误解：

| 错误类型 | 谁负责捕获 |
| --- | --- |
| 同步代码中未捕获的 `throw` | `window.onerror` |
| `setTimeout` / 事件回调里未捕获的 `throw` | `window.onerror`（回调里抛出的错误会作为未捕获错误上报） |
| Promise 未处理的 reject | 只有 `unhandledrejection`，`window.onerror` 收不到 |
| `<img>`、`<script>`、`<link>` 等资源加载失败 | `window.onerror` 收不到，要用 `addEventListener('error', handler, true)` 在捕获阶段监听 |
| 被 `try...catch` 正常捕获的错误 | 不会上报，这是预期行为 |

```javascript
// 资源加载失败：必须开启捕获阶段，否则事件不会冒泡到 window
window.addEventListener('error', function(event) {
    const target = event.target;
    if (target instanceof HTMLImageElement) {
        console.warn('图片加载失败：', target.src);
        target.src = '/images/placeholder.png';   // 兜底图
    } else if (target instanceof HTMLScriptElement) {
        console.warn('脚本加载失败：', target.src);
    }
}, true);

// 如果错误已经被捕获处理后又补挂了 catch，会触发 rejectionhandled
window.addEventListener('rejectionhandled', function(event) {
    console.log('迟到的处理：', event.reason);
});
```

另外两个细节：

- **开启 `preventDefault()` 会屏蔽控制台的默认警告**，方便你自己上报，但调试期建议先别关，否则容易漏掉问题。
- **跨域脚本报错会被脱敏**成 `Script error.`，拿不到堆栈。给跨域 `<script>` 加 `crossorigin="anonymous"`，并在响应头返回 `Access-Control-Allow-Origin`，才能拿到完整信息。

在 Node.js 中对应的两个兜底入口是 `process.on('uncaughtException')` 和 `process.on('unhandledRejection')`。它们只应该用来「记录日志后优雅退出」，不能指望程序从异常状态里继续正常运行。

## 35.4 错误处理的实践原则

### 只捕获你能处理的错误

`catch` 块要么能给出有意义的补救（重试、降级、提示用户），要么就应该继续往上抛，最忌讳的是「捕获后什么都不做」：

```javascript
// ❌ 错误被静默吞掉，出问题时毫无线索
try {
    await saveOrder(order);
} catch (e) {}

// ❌ 只打日志也不够：调用方会以为保存成功了，继续执行后续逻辑
try {
    await saveOrder(order);
} catch (e) {
    console.log(e);
}

// ✅ 要么处理，要么带上上下文重新抛出
try {
    await saveOrder(order);
} catch (e) {
    throw new Error(`订单 ${order.id} 保存失败`, { cause: e });
}
```

### 不要用异常做流程控制

异常的开销远高于普通分支，而且在异步代码里会让调用链难以追踪。像「查找可能不存在的元素」这种预期内的结果，应该用返回值表达，而不是抛异常。

```javascript
// ❌ 用异常表达「正常可能发生的情况」
function findUser(id) {
    const user = users.find((u) => u.id === id);
    if (!user) throw new Error('NOT_FOUND');
    return user;
}

// ✅ 预期内的结果用返回值，真正的异常才用 throw
function findUser(id) {
    return users.find((u) => u.id === id);   // 可能返回 undefined，调用方自己判断
}
```

### 给用户看的信息和给开发看的信息要分开

```javascript
class AppError extends Error {
    // userMessage：可以直接展示给用户
    // message / stack / cause：只进日志和错误上报
    constructor(userMessage, internalMessage, options) {
        super(internalMessage, options);
        this.name = 'AppError';
        this.userMessage = userMessage;
    }
}

try {
    await pay(order);
} catch (e) {
    reportToSentry(e);                     // 开发侧：完整堆栈
    toast(e.userMessage ?? '操作失败，请稍后重试');   // 用户侧：友好文案
}
```

### 关键操作要有超时和重试

只处理「失败」是不够的，长时间挂起的请求同样需要兜底：

```javascript
async function fetchWithTimeout(url, ms = 8000) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), ms);
    try {
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (e) {
        if (e.name === 'AbortError') {
            throw new Error(`请求超时（${ms}ms）`, { cause: e });
        }
        throw e;
    } finally {
        clearTimeout(timer);   // 成功也要清掉定时器，否则会留下悬挂的计时器
    }
}
```

### 常见误区速查

| 写法 | 问题 | 正确做法 |
| --- | --- | --- |
| `catch (e) {}` | 错误被吞掉，线上问题无从排查 | 至少重新抛出或上报 |
| `throw '错误信息'` | 丢堆栈、丢掉 `instanceof Error` | `throw new Error('错误信息')` |
| 用 `try...catch` 包住 `setTimeout` | 异步回调不在当前调用栈内 | 在回调内部再包一层 try...catch |
| 只判断 `res.json()` 成功 | `fetch` 对 4xx/5xx 不 reject | 先判断 `res.ok` |
| 自定义错误忘了设 `name` | 日志里全显示 `Error` | `this.name = 'XxxError'` |
| 在 `catch` 里 `return` 后忘了 `finally` 仍在执行 | 误以为已经跳出 | `finally` 里不要写会覆盖结果的 `return` |

---

## 本章小结

本章我们学习了错误处理：

1. **try...catch**：捕获同步代码中的错误。
2. **Error 对象**：包含 message、name、stack 信息。
3. **内置错误类型**：ReferenceError、TypeError、SyntaxError、RangeError、URIError。
4. **throw**：手动抛出错误，且应当只抛 Error 及其子类。
5. **自定义错误**：通过继承 Error 携带业务字段，记得设置 `name` 和 `cause`。
6. **异步错误处理**：Promise 用 `.catch()`/`.finally()`，async/await 用 `try...catch`；async 函数只会返回 rejected Promise。
7. **并发错误**：`all`/`allSettled`/`any`/`race` 的失败行为各不相同，`Promise.any` 全部失败时抛 `AggregateError`。
8. **全局错误处理**：`window.onerror`、`unhandledrejection`，以及需要捕获阶段的资源加载错误。
9. **实践原则**：只捕获能处理的错误、不用异常做流程控制、区分用户文案与技术细节、关键操作加超时与重试。

错误处理是写出健壮代码的关键。学会优雅地处理错误，你的程序就不会轻易崩溃了。

下一章，我们要学习调试——让 bug 无所遁形！
