+++
title = "第 30 章 网络请求"
weight = 300
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 30 章 网络请求

JavaScript 本身只能运行在浏览器里，它需要和服务器"对话"才能获取数据、更新内容。网络请求就是 JavaScript 和服务器之间的"信使"。

## 30.1 XMLHttpRequest

### 创建对象

```javascript
// 创建 XMLHttpRequest 对象
const xhr = new XMLHttpRequest();
```

### open / send / setRequestHeader

```javascript
// 初始化请求
xhr.open('GET', 'https://api.example.com/data', true);
// 参数：请求方法、URL、是否异步
// 第三个参数省略时默认就是 true（异步）；传 false 表示同步请求，
// 它会阻塞主线程，已经被浏览器标记为不推荐，新代码不要使用

// 设置请求头
// 必须在 open() 之后、send() 之前调用，否则会抛 InvalidStateError
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.setRequestHeader('Authorization', 'Bearer token123');

// 发送请求
xhr.send(); // GET 请求
// xhr.send(JSON.stringify({ name: '小明' })); // POST 请求带数据
```

### onreadystatechange：监听状态变化

```javascript
xhr.onreadystatechange = function() {
    console.log('状态变化：', xhr.readyState);
};
```

### readyState 的 5 种状态

| 状态 | 值 | 说明 |
|------|---|------|
| UNSENT | 0 | 请求未初始化 |
| OPENED | 1 | open() 已调用 |
| HEADERS_RECEIVED | 2 | 接收到响应头 |
| LOADING | 3 | 正在下载响应体 |
| DONE | 4 | 请求完成 |

```javascript
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
        console.log('请求完成了');
    }
};
```

### HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 301/302 | 重定向 |
| 400 | 请求错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 未找到 |
| 500 | 服务器错误 |

```javascript
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
        if (xhr.status >= 200 && xhr.status < 300) {
            console.log('成功：', xhr.responseText);
        } else if (xhr.status === 404) {
            console.log('资源未找到');
        } else {
            console.log('请求失败：', xhr.status);
        }
    }
};
```

上面这段代码有一个容易忽略的漏洞：**网络层失败时 `xhr.status` 是 0**（例如断网、跨域被拦截、请求被中止），它既不是 2xx 也不是 404，会掉进 `else` 分支并显示一个毫无意义的「请求失败：0」。完整写法要加上错误回调：

```javascript
const xhrFull = new XMLHttpRequest();
xhrFull.open('GET', 'https://api.example.com/data', true);

xhrFull.onload = function() {
    // 只有请求正常走完（无论状态码是多少）才会进这里
    if (xhrFull.status >= 200 && xhrFull.status < 300) {
        console.log('成功：', xhrFull.responseText);
    } else {
        console.log('服务端返回了错误状态：', xhrFull.status);
    }
};

xhrFull.onerror = function() {
    console.log('网络错误，请求根本没发出去或连接被中断');
};

xhrFull.ontimeout = function() {
    console.log('请求超时');   // 超时后请求已经终止，不需要再调用 abort()
};

xhrFull.onabort = function() {
    console.log('请求被主动取消');
};

// 想要拿到实际的状态码文字（如 "Not Found"），用 statusText
xhrFull.timeout = 5000;
xhrFull.send();
```

用 `onload` / `onerror` / `ontimeout` 这套事件，比手写 `onreadystatechange` 再判断 `readyState === 4` 更清晰，也是现在的推荐做法。

### GET / POST 请求

```javascript
// GET 请求
const xhrGet = new XMLHttpRequest();
xhrGet.open('GET', 'https://api.example.com/users?id=1', true);
xhrGet.send();

// POST 请求
const xhrPost = new XMLHttpRequest();
xhrPost.open('POST', 'https://api.example.com/users', true);
xhrPost.setRequestHeader('Content-Type', 'application/json');
xhrPost.send(JSON.stringify({ name: '小明', age: 18 }));
```

### 文件上传：FormData + multipart/form-data

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('name', 'myFile');

const xhr = new XMLHttpRequest();
xhr.open('POST', 'https://api.example.com/upload', true);
xhr.send(formData);
```

### 超时处理：setTimeout + abort

```javascript
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://api.example.com/data', true);

// 设置超时（毫秒）
xhr.timeout = 5000;

xhr.ontimeout = function() {
    console.log('请求超时了！');
};

xhr.onload = function() {
    console.log('请求成功：', xhr.responseText);
};

xhr.send();
```

### 取消请求：abort()

```javascript
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://api.example.com/data', true);

xhr.send();

// 3秒后取消请求
setTimeout(function() {
    xhr.abort();
    console.log('请求已取消');
}, 3000);

xhr.onabort = function() {
    console.log('请求被中断了');
};
```

下一节，我们来学习 Fetch API！

## 30.2 Fetch API

### fetch() 基础：返回 Promise

```javascript
// 基本用法
fetch('https://api.example.com/data')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log('数据：', data);
    })
    .catch(function(error) {
        console.log('请求失败：', error);
    });
```

### Response 对象：status / ok / headers / body

```javascript
fetch('https://api.example.com/data')
    .then(function(response) {
        console.log('状态码：', response.status);
        console.log('是否成功：', response.ok);
        console.log('响应头：', response.headers);
        return response.json();
    })
    .then(function(data) {
        console.log('数据：', data);
    });
```

### response.json() / text() / blob()

```javascript
// JSON
fetch('https://api.example.com/data')
    .then(function(response) { return response.json(); })
    .then(function(data) { console.log(data); });

// 文本
fetch('https://api.example.com/text')
    .then(function(response) { return response.text(); })
    .then(function(text) { console.log(text); });

// 二进制数据（图片等）
fetch('https://api.example.com/image')
    .then(function(response) { return response.blob(); })
    .then(function(blob) {
        const url = URL.createObjectURL(blob);
        document.querySelector('img').src = url;
    });
```

### POST 请求配置：method / headers / body

```javascript
fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name: '小明', age: 18 })
})
    .then(function(response) { return response.json(); })
    .then(function(data) { console.log('创建成功：', data); });
```

### 发送 JSON / FormData / 文件

```javascript
// 发送 JSON
fetch('https://api.example.com/api', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: '小明' })
});

// 发送 FormData
const formData = new FormData();
formData.append('name', '小明');
formData.append('avatar', fileInput.files[0]);

fetch('https://api.example.com/upload', {
    method: 'POST',
    body: formData
});

// 注意：用 FormData 时千万不要手动设置 Content-Type
// 浏览器会自动生成带 boundary 分隔符的 multipart/form-data 头，
// 手动写死 Content-Type 会让服务端解析不出文件

// 发送文件
const fileInput = document.getElementById('file');
const file = fileInput.files[0];
const formDataFile = new FormData();
formDataFile.append('file', file);

fetch('https://api.example.com/upload', {
    method: 'POST',
    body: formDataFile
});
```

### AbortController：超时与取消

```javascript
const controller = new AbortController();
const signal = controller.signal;

// 带取消信号
fetch('https://api.example.com/data', { signal: signal })
    .then(function(response) { return response.json(); })
    .then(function(data) { console.log(data); })
    .catch(function(error) {
        if (error.name === 'AbortError') {
            console.log('请求被取消了');
        }
    });

// 取消请求
controller.abort();

// 超时取消
setTimeout(function() {
    controller.abort();
}, 5000);
```

### fetch 不 reject HTTP 错误状态的坑

```javascript
// ❌ fetch 不会 reject HTTP 错误状态（如 404、500）
fetch('https://api.example.com/notfound')
    .then(function(response) {
        // 404 也会进入这里，不会 reject
        if (!response.ok) {
            throw new Error('HTTP ' + response.status);
        }
        return response.json();
    })
    .catch(function(error) {
        console.log('请求失败：', error);
    });

// ✅ 正确做法：检查 response.ok
fetch('https://api.example.com/data')
    .then(function(response) {
        if (!response.ok) {
            throw new Error('请求失败：' + response.status);
        }
        return response.json();
    });
```

### 跨域（CORS）：为什么请求发出去了却拿不到数据

初学者最常见的困惑是「Network 面板里明明有响应（甚至状态码 200），控制台却报 CORS 错误」。原因在于：**跨域请求是被浏览器拦截的，被拦截的是「JavaScript 读取响应」这一步，而不是请求本身**。服务器收到了请求，也返回了数据，但响应头里没有允许你这个源读取，浏览器就把结果扣下了。

```text
浏览器地址：https://shop.example.com
请求目标：  https://api.other.com/users

如果 api.other.com 的响应里没有：
  Access-Control-Allow-Origin: https://shop.example.com
那么浏览器会阻止页面代码读取这份响应。
```

几件必须记住的事：

- **CORS 是服务端要解决的问题**，前端改代码、换请求库都没用。需要后端返回相应的 `Access-Control-Allow-*` 头。
- 携带 Cookie 的跨域请求用的是 `fetch(url, { credentials: 'include' })`，同时后端必须返回**具体域名**的 `Access-Control-Allow-Origin`，不能用 `*`；对应的 XHR 写法是 `xhr.withCredentials = true`。
- `POST` + `Content-Type: application/json`、自定义请求头（如 `Authorization`）会触发**预检请求**：浏览器先发一个 `OPTIONS`，服务器同意后才会发真正的请求。所以「多发了一次请求」是正常现象。
- **开发阶段的跨域用代理解决最干净**：Vite 的 `server.proxy`、Webpack 的 `devServer.proxy` 把 `/api` 转发到后端，浏览器看到的就是同源请求，彻底绕开 CORS。
- **CORS 不是安全边界**：它保护的是浏览器里的用户，不能替代服务端的鉴权。别人可以直接用 curl 调你的接口。

### AbortSignal.timeout：更简洁的超时写法

```javascript
// 一次性超时：现代浏览器支持，不需要自己管理 AbortController
try {
    const res = await fetch('/api/slow', { signal: AbortSignal.timeout(5000) });
    console.log(await res.json());
} catch (err) {
    // 超时抛的是 TimeoutError，主动取消抛的是 AbortError，两者要区分处理
    console.log(err.name); // 'TimeoutError'
}

// 需要在别处提前取消（例如用户点了「取消」按钮），才需要手动建 controller
```

### 封装 fetch 请求工具：拦截器 / 统一错误处理

```javascript
// 封装 fetch
function request(url, options) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    return fetch(url, { ...defaultOptions, ...options })
        .then(function(response) {
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            return response.json();
        })
        .catch(function(error) {
            console.error('请求错误：', error);
            throw error;
        });
}

// 使用
request('https://api.example.com/data')
    .then(function(data) { console.log(data); });
```

上面这段封装可以直接用，但有几个可以做得更好的地方：

1. **`headers` 会被整体覆盖**。`{ ...defaultOptions, ...options }` 是浅合并，只要调用方传了 `headers`，默认的 `Content-Type` 就消失了。正确做法是把 headers 单独合并。
2. **`.catch` 里 `console.error` 后原样抛出**这一步没有实质作用，只是多打一遍日志；真正需要的是在拦截器里统一处理「令牌过期跳登录」这类逻辑。
3. **`Content-Type: application/json` 不该无条件带上**，GET 请求带它没有意义，FormData 更不能带。
4. **204 等空响应体不能直接 `response.json()`**，会抛 `SyntaxError: Unexpected end of JSON input`。

```javascript
async function request(url, { method = 'GET', headers = {}, body, signal, ...rest } = {}) {
    const isFormData = body instanceof FormData;

    const finalHeaders = {
        Accept: 'application/json',
        ...headers,
    };
    if (body !== undefined && !isFormData && !finalHeaders['Content-Type']) {
        finalHeaders['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, {
        method,
        headers: finalHeaders,
        // 只有传了对象才自动序列化，字符串和 FormData 交给调用方
        body: body && !isFormData && typeof body !== 'string' ? JSON.stringify(body) : body,
        signal,
        ...rest,
    });

    // 约定：非 2xx 一律当作错误，并把响应体里的错误信息带出来
    if (!response.ok) {
        let detail = '';
        try {
            detail = (await response.text()).slice(0, 200);
        } catch {}
        throw new Error(`HTTP ${response.status} ${response.statusText} ${detail}`.trim());
    }

    // 204 / 205 表示没有响应体
    if (response.status === 204 || response.headers.get('content-length') === '0') {
        return null;
    }

    const type = response.headers.get('content-type') ?? '';
    return type.includes('application/json') ? response.json() : response.text();
}

const data = await request('/api/users');
await request('/api/users', { method: 'POST', body: { name: '小明' } });
```

### 实战中的四个常见需求

```javascript
// 1. 搜索框的竞态问题：旧请求可能后返回，把新结果覆盖掉
//    解法是在发新请求前取消旧请求
let currentController = null;
async function search(keyword) {
    currentController?.abort();                 // 取消上一次
    currentController = new AbortController();
    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(keyword)}`, {
            signal: currentController.signal,
        });
        render(await res.json());
    } catch (err) {
        if (err.name !== 'AbortError') throw err; // 被取消是预期行为，不算错误
    }
}

// 2. 并发请求：需要全部成功用 Promise.all，允许部分失败用 allSettled
const [user, orders] = await Promise.all([
    fetch('/api/user').then((r) => r.json()),
    fetch('/api/orders').then((r) => r.json()),
]);

// 3. 失败重试：只对网络错误和 5xx 重试，4xx 说明请求本身有问题，重试没意义
async function fetchWithRetry(url, { retries = 2, delay = 500 } = {}) {
    for (let i = 0; i <= retries; i++) {
        try {
            const res = await fetch(url);
            if (res.status >= 500 && i < retries) throw new Error('服务端错误');
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return await res.json();
        } catch (err) {
            if (i === retries) throw err;
            // 指数退避：500ms、1000ms、2000ms……
            await new Promise((r) => setTimeout(r, delay * 2 ** i));
        }
    }
}

// 4. 页面即将关闭时上报数据：普通 fetch 会被取消，要用 sendBeacon 或 keepalive
window.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
        const payload = JSON.stringify({ action: 'leave', at: Date.now() });
        // sendBeacon 不返回响应，但浏览器会保证发出
        navigator.sendBeacon('/api/telemetry', new Blob([payload], { type: 'application/json' }));
    }
});
```

下一节，我们来学习 JSON！

## 30.3 JSON

### JSON 格式规则：键必须双引号，不支持 undefined

```javascript
// ✅ 正确的 JSON
const json1 = '{"name": "小明", "age": 18}';

// ❌ 错误的 JSON（键没有双引号）
// const json2 = "{name: '小明', age: 18}"; // 这是无效的！

// ❌ JSON 不支持 undefined
// const json3 = '{"value": undefined}'; // 无效！

// JSON 支持的值
// 注意：JSON 文本跨行时必须用模板字符串或字符串拼接，
// 单引号字符串是不能直接换行的
const validJson = `{
    "string": "你好",
    "number": 123,
    "boolean": true,
    "null": null,
    "array": [1, 2, 3],
    "object": { "key": "value" }
}`;
```

几条容易记错的 JSON 规则：

| 规则 | 说明 |
| --- | --- |
| 键必须是双引号 | `{name: 1}`、`{'name': 1}` 都不是合法 JSON |
| 不允许尾随逗号 | `[1, 2, 3,]`、`{"a": 1,}` 非法 |
| 不允许注释 | `// 注释` 会让解析失败 |
| 数字有限制 | 不支持 `NaN`、`Infinity`、十六进制 `0x10`、前导零 `01` |
| 字符串必须双引号 | 单引号串 `'abc'` 非法 |
| 值类型有限 | 只有对象、数组、字符串、数字、布尔、`null` 六种 |

注意 JSON 的**类型系统是 JS 的子集**：JSON 里合法（`{"a":1}`）在 JS 里不一定能当对象字面量用，反过来 JS 的对象字面量写法（单引号、尾逗号、函数）也不是合法 JSON。这就是为什么 `JSON.parse("{'a':1}")` 会直接抛错。

### JSON.stringify：参数 replacer / space

```javascript
const obj = { name: '小明', age: 18, password: 'secret123' };

// 基本序列化
console.log(JSON.stringify(obj));
// 打印结果: {"name":"小明","age":18,"password":"secret123"}

// 过滤属性（排除 password）
const filtered = JSON.stringify(obj, ['name', 'age']);
console.log(filtered);
// 打印结果: {"name":"小明","age":18}

// 美化输出
const pretty = JSON.stringify(obj, null, 2);
console.log(pretty);
// 打印结果:
// {
//   "name": "小明",
//   "age": 18,
//   "password": "secret123"
// }
```

`replacer` 还有第二种形态——传函数，可以逐个字段决定怎么处理，这是脱敏的常用手段：

```javascript
// 把敏感字段替换掉
const safe = JSON.stringify(obj, (key, value) => {
    if (key === 'password' || key === 'token') return '[已隐藏]';
    return value;
}, 2);

// 空值统一转成 null
const normalized = JSON.stringify(obj2, (key, value) => value === undefined ? null : value);

// 也可以顺手做排序，让输出稳定（方便比对）
const sorted = JSON.stringify({ b: 1, a: 2 }, (key, value) =>
    value && typeof value === 'object' && !Array.isArray(value)
        ? Object.fromEntries(Object.entries(value).sort())
        : value
);
```

### JSON.parse：参数 reviver

```javascript
const jsonString = '{"timestamp":"2024-03-24T10:30:00Z"}';

// 基本解析
const obj = JSON.parse(jsonString);
console.log(obj.timestamp); // 打印结果: 2024-03-24T10:30:00Z

// 带 reviver 转换日期
const objWithDate = JSON.parse(jsonString, function(key, value) {
    if (key === 'timestamp') {
        return new Date(value);
    }
    return value;
});
console.log(objWithDate.timestamp instanceof Date); // 打印结果: true
```

### 序列化注意事项：函数/undefined/循环引用

```javascript
// ❌ 函数会被忽略
const obj1 = { name: '小明', greet: function() { return 'hi'; } };
console.log(JSON.stringify(obj1)); // 打印结果: {"name":"小明"}

// ❌ undefined 会被忽略
const obj2 = { name: '小明', value: undefined };
console.log(JSON.stringify(obj2)); // 打印结果: {"name":"小明"}

// ❌ 循环引用会报错
const obj3 = { name: '小明' };
obj3.self = obj3;
try {
    JSON.stringify(obj3); // 报错：Converting circular structure to JSON
} catch (e) {
    console.log('循环引用无法序列化');
}
```

### 序列化会损失什么：Date / Map / Set / 特殊数字

`JSON.stringify` 只认识那六种 JSON 类型，其他类型都会被「降级」处理，这一过程不可逆：

| 原始值 | `JSON.stringify` 之后 | 能否原样还原 |
| --- | --- | --- |
| `new Date()` | `"2024-03-24T10:30:00.000Z"`（字符串） | 否，`JSON.parse` 回来只是字符串 |
| `Map` / `Set` | `{}` | 否，内容全部丢失 |
| `undefined` / 函数 / `Symbol` | 对象里被跳过，数组里变成 `null` | 否 |
| `NaN` / `Infinity` | `null` | 否 |
| `BigInt` | 直接抛 `TypeError` | 否 |
| 类实例 | 只保留自有可枚举属性，原型丢失 | 否 |

```javascript
console.log(JSON.stringify(new Date('2024-03-24'))); // "2024-03-24T00:00:00.000Z"
console.log(JSON.stringify(new Map([['a', 1]])));    // {}
console.log(JSON.stringify(new Set([1, 2])));        // {}
console.log(JSON.stringify([undefined, function () {}])); // [null,null]
console.log(JSON.stringify(NaN));                    // null
// JSON.stringify(10n);                              // TypeError: Do not know how to serialize a BigInt
```

所以「用 JSON 深拷贝」有一个明确的能力边界：

```javascript
// ❌ 只在「纯数据、无循环引用、不含上述类型」时可用
const copy = JSON.parse(JSON.stringify(source));

// ✅ 现代环境里的标准深拷贝：能处理 Date、Map、Set、循环引用
const clone = structuredClone(source);

// 注意 structuredClone 也有边界：函数、Symbol、DOM 节点、原型上的类信息无法复制
```

如果的确需要自定义序列化行为，可以在类里实现 `toJSON()`，`JSON.stringify` 会自动调用它：

```javascript
class User {
    constructor(name, password) {
        this.name = name;
        this.password = password;
    }
    toJSON() {
        return { name: this.name };   // password 自动被排除
    }
}
console.log(JSON.stringify(new User('小明', 'secret'))); // {"name":"小明"}
```

### JSON.parse 的错误处理

`JSON.parse` 失败一定会抛 `SyntaxError`，凡是解析外部来源（接口返回、localStorage、用户输入）都应当兜住：

```javascript
function safeParse(text, fallback = null) {
    if (typeof text !== 'string' || text === '') return fallback;
    try {
        return JSON.parse(text);
    } catch (err) {
        console.warn('JSON 解析失败：', err.message, text.slice(0, 100));
        return fallback;
    }
}

// 常见报错语：
// Unexpected token 'x' in JSON at position 0   —— 多半是解析了 HTML 错误页
// Unexpected end of JSON input                 —— 空响应体
// Unexpected token '}'                         —— 多了尾随逗号

// 顺带一提：数字在 JSON 里是双精度浮点，超出安全范围的大整数会丢精度
console.log(JSON.parse('{"id": 9007199254740993}').id); // 9007199254740992
// 这类字段应该让服务端以字符串形式返回
```

---

## 本章小结

本章我们学习了网络请求：

1. **XMLHttpRequest**：老式但兼容好的请求方式，用 `onload`/`onerror`/`ontimeout` 管理状态；注意网络失败时 `status` 是 0。
2. **Fetch API**：基于 Promise 的现代请求方式，用 `response.ok` 判断业务成功，用 `response.json()/text()/blob()` 读取响应体。
3. **取消与超时**：`AbortController` 用于手动取消，`AbortSignal.timeout()` 用于一次性超时，两者抛出的错误名不同。
4. **CORS**：跨域限制的是「前端读取响应」，需要服务端返回允许头；开发环境用代理最省事。
5. **请求封装**：合并 headers、按需设置 Content-Type、统一处理非 2xx、兼容 204 空响应。
6. **实战模式**：搜索竞态取消、`Promise.all` 并发、只对网络错误和 5xx 重试、卸载时用 `sendBeacon` 上报。
7. **JSON**：六种值类型、键必须双引号；`stringify` 的 replacer/space、`parse` 的 reviver、循环引用与类型丢失、超过安全范围的整数会丢精度，深拷贝优先用 `structuredClone`。

下一章，我们要学习客户端存储——让数据持久化保存在浏览器里！
