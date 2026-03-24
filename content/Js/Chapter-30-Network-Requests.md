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

// 设置请求头
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
    xhr.abort();
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
const validJson = '{
    "string": "你好",
    "number": 123,
    "boolean": true,
    "null": null,
    "array": [1, 2, 3],
    "object": { "key": "value" }
}';
```

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
//   "age": 18
// }
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

---

## 本章小结

本章我们学习了网络请求：

1. **XMLHttpRequest**：老式但兼容好的请求方式，需要手动管理状态。
2. **Fetch API**：现代浏览器的请求方式，返回 Promise，更简洁。
3. **JSON**：轻量级的数据交换格式，键必须双引号，不支持 undefined 和函数。
4. **注意事项**：fetch 不 reject HTTP 错误状态，需要手动检查 response.ok。

下一章，我们要学习客户端存储——让数据持久化保存在浏览器里！
