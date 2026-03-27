+++
title = "第 37 章 工具函数"
weight = 370
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 37 章 工具函数

所谓"工具函数"，就是那些可以反复使用的、封装好的函数。它们就像程序员工具箱里的"瑞士军刀"，让你写代码更高效、更优雅。

## 37.1 防抖与节流

### debounce：事件触发 n 毫秒后执行，n 毫秒内再次触发重新计时

防抖就像"等公交车"——每次有人上车（触发），司机就重新等一会儿。如果一直有人上车，司机就一直在等，直到没人上车了才发车。

```javascript
// 防抖函数
function debounce(func, delay) {
    let timer = null;
    
    return function(...args) {
        // 每次调用都清除之前的定时器
        if (timer) {
            clearTimeout(timer);
        }
        
        // 设置新的定时器
        timer = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// 使用防抖
const debouncedSearch = debounce(function(query) {
    console.log('搜索：' + query);
    // 实际发送搜索请求
}, 300);

// 快速输入时，只会在停止输入 300ms 后执行一次
debouncedSearch('a');
debouncedSearch('ab');
debouncedSearch('abc');
debouncedSearch('abcd');
// 300ms 后只打印一次：搜索：abcd
```

### throttle：n 毫秒内只执行一次，多次回触发只执行第一次

节流就像"射击"——扣一次扳机只能发射一颗子弹，即使你一直扣着不放，子弹也会按固定间隔发射。

```javascript
// 节流函数
function throttle(func, interval) {
    let lastTime = 0;
    
    return function(...args) {
        const now = Date.now();
        
        // 如果距离上次执行已经超过 interval，执行并更新时间
        if (now - lastTime >= interval) {
            lastTime = now;
            func.apply(this, args);
        }
    };
}

// 使用节流
const throttledScroll = throttle(function() {
    console.log('滚动位置：' + window.scrollY);
}, 100);

// 快速滚动时，每 100ms 最多执行一次
window.addEventListener('scroll', throttledScroll);
```

### 防抖 vs 节流对比与适用场景

| 场景 | 工具 | 说明 |
|------|------|------|
| 搜索框输入 | 防抖 | 用户停止输入后才搜索 |
| 窗口大小改变 | 节流 | 每隔一段时间检查一次 |
| 按钮点击 | 节流 | 防止重复提交 |
| 滚动加载 | 节流 | 滚动时每隔一定距离加载 |
| 表单验证 | 防抖 | 用户停止输入后验证 |

```javascript
// 防抖适用场景：搜索框
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', debounce(function() {
    console.log('发送搜索请求：' + this.value);
}, 500));

// 节流适用场景：滚动
window.addEventListener('scroll', throttle(function() {
    console.log('滚动位置：' + window.scrollY);
}, 200));
```

下一节，我们来学习深拷贝与浅拷贝！

## 37.2 深拷贝与浅拷贝

### JSON.parse(JSON.stringify())

```javascript
// 简单深拷贝
const original = {
    name: '小明',
    age: 18,
    hobbies: ['coding', 'gaming']
};

const copy = JSON.parse(JSON.stringify(original));
copy.hobbies.push('reading');

console.log(original.hobbies); // 打印结果: ['coding', 'gaming']
console.log(copy.hobbies);     // 打印结果: ['coding', 'gaming', 'reading']
```

### 递归深拷贝

```javascript
function deepClone(obj, hash = new WeakMap()) {
    // 基本类型直接返回
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
    
    // 防止循环引用
    if (hash.has(obj)) {
        return hash.get(obj);
    }
    
    // 处理 Date
    if (obj instanceof Date) {
        return new Date(obj.getTime());
    }
    
    // 处理 RegExp
    if (obj instanceof RegExp) {
        return new RegExp(obj.source, obj.flags);
    }
    
    // 处理数组或普通对象
    const cloned = Array.isArray(obj) ? [] : {};
    hash.set(obj, cloned);
    
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            cloned[key] = deepClone(obj[key], hash);
        }
    }
    
    return cloned;
}

// 测试
const original = { date: new Date(), regex: /test/g };
const copy = deepClone(original);
console.log(copy.date instanceof Date); // 打印结果: true
console.log(copy.regex.source); // 打印结果: test
```

### structuredClone（ES2021+）

```javascript
// 现代浏览器的原生深拷贝
const original = {
    name: '小明',
    hobbies: ['coding', 'gaming'],
    date: new Date()
};

const copy = structuredClone(original);
console.log(copy.name); // 打印结果: 小明
console.log(copy.hobbies); // 打印结果: ['coding', 'gaming']
console.log(copy.date instanceof Date); // 打印结果: true

// structuredClone 可以处理循环引用
const obj = { a: 1 };
obj.self = obj;
const copy2 = structuredClone(obj);
console.log(copy2 === obj); // 打印结果: false
```

下一节，我们来学习数组操作！

## 37.3 数组操作

### 扁平化：flat / reduce / 正则

```javascript
const nested = [1, [2, [3, [4, [5]]]];

// flat：ES2019+
console.log(nested.flat(Infinity)); // 打印结果: [1, 2, 3, 4, 5]

// reduce
function flattenDeep(arr) {
    return arr.reduce((acc, val) => 
        Array.isArray(val) ? acc.concat(flattenDeep(val)) : acc.concat(val)
    , []);
}
console.log(flattenDeep(nested)); // 打印结果: [1, 2, 3, 4, 5]
```

### 去重：Set / indexOf / filter / includes / reduce

```javascript
const nums = [1, 2, 2, 3, 3, 3, 4, 4, 5];

// Set（最简洁高效）
console.log([...new Set(nums)]); // 打印结果: [1, 2, 3, 4, 5]

// filter + indexOf
console.log(nums.filter((item, index) => nums.indexOf(item) === index)); // 打印结果: [1, 2, 3, 4, 5]

// reduce
console.log(nums.reduce((acc, cur) => 
    acc.includes(cur) ? acc : acc.concat(cur)
, [])); // 打印结果: [1, 2, 3, 4, 5]
```

### 洗牌：Fisher-Yates 算法

```javascript
function shuffle(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

console.log(shuffle([1, 2, 3, 4, 5])); // 打印结果: [随机顺序]
```

### 交集 / 并集 / 差集

```javascript
const a = [1, 2, 3, 4];
const b = [3, 4, 5, 6];

// 交集
console.log(a.filter(x => b.includes(x))); // 打印结果: [3, 4]

// 并集
console.log([...new Set([...a, ...b])]); // 打印结果: [1, 2, 3, 4, 5, 6]

// 差集（A 有 B 没有）
console.log(a.filter(x => !b.includes(x))); // 打印结果: [1, 2]
```

### 分组：groupBy

```javascript
function groupBy(array, key) {
    return array.reduce((groups, item) => {
        const group = typeof key === 'function' ? key(item) : item[key];
        groups[group] = groups[group] || [];
        groups[group].push(item);
        return groups;
    }, {});
}

const users = [
    { name: '小明', age: 18 },
    { name: '小红', age: 20 },
    { name: '小刚', age: 18 }
];

console.log(groupBy(users, 'age'));
// 打印结果: { '18': [用户1, 用户3], '20': [用户2] }
```

下一节，我们来学习字符串与数值！

## 37.4 字符串与数值

### UUID：crypto.randomUUID()（ES2022+）

```javascript
// 生成 UUID
const uuid = crypto.randomUUID();
console.log(uuid); // 打印结果: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
```

### 千分位：toLocaleString() / Intl.NumberFormat / 正则

```javascript
const num = 1234567;

// toLocaleString
console.log(num.toLocaleString()); // 打印结果: 1,234,567

// Intl.NumberFormat
console.log(new Intl.NumberFormat().format(num)); // 打印结果: 1,234,567

// 正则
console.log(num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')); // 打印结果: 1,234,567
```

### URL 参数：URLSearchParams

```javascript
const params = new URLSearchParams();
params.set('name', '小明');
params.set('age', '18');

console.log(params.toString()); // 打印结果: name=%E5%B0%8F%E6%98%8E&age=18

// 解析 URL 参数
const url = 'https://example.com?name=%E5%B0%8F%E6%98%8E&age=18';
const searchParams = new URLSearchParams(new URL(url).search);
console.log(searchParams.get('name')); // 打印结果: 小明
```

### Base64：btoa / atob（含中文处理）

```javascript
// 基础用法
const encoded = btoa('hello');
console.log(encoded); // 打印结果: aGVsbG8=
const decoded = atob(encoded);
console.log(decoded); // 打印结果: hello

// 处理中文
const str = '你好';
const encoded2 = btoa(encodeURIComponent(str));
console.log(encoded2); // 打印结果: JUU0JUJEJUEwJUU1
const decoded2 = decodeURIComponent(atob(encoded2));
console.log(decoded2); // 打印结果: 你好
```

下一节，我们来学习发布订阅！

## 37.5 发布订阅

### EventEmitter：on / off / emit / once

```javascript
class EventEmitter {
    constructor() {
        this.events = {};
    }
    
    on(event, listener) {
        this.events[event] = this.events[event] || [];
        this.events[event].push(listener);
        return this;
    }
    
    off(event, listenerToRemove) {
        if (!this.events[event]) return this;
        this.events[event] = this.events[event].filter(
            listener => listener !== listenerToRemove
        );
        return this;
    }
    
    emit(event, ...args) {
        if (!this.events[event]) return;
        this.events[event].forEach(listener => listener(...args));
        return this;
    }
    
    once(event, listener) {
        const wrapper = (...args) => {
            listener(...args);
            this.off(event, wrapper);
        };
        return this.on(event, wrapper);
    }
}

// 使用
const emitter = new EventEmitter();

emitter.on('message', (msg) => {
    console.log('收到消息：' + msg);
});

emitter.emit('message', 'Hello!'); // 打印结果: 收到消息：Hello!
emitter.emit('message', 'World!'); // 打印结果: 收到消息：World!

// once：只触发一次
emitter.once('oneTime', () => console.log('只触发一次'));
emitter.emit('oneTime'); // 触发
emitter.emit('oneTime'); // 不会触发
```

### Promise 队列：控制并发

```javascript
// 控制并发的 Promise 队列
async function controlledPromiseQueue(tasks, concurrency = 3) {
    const results = [];
    const executing = new Set();
    
    for (const task of tasks) {
        const promise = Promise.resolve().then(() => task());
        results.push(promise);
        
        const cleanup = () => executing.delete(promise);
        
        if (executing.size >= concurrency) {
            await Promise.race(executing);
        }
        
        executing.add(promise);
        promise.then(cleanup);
    }
    
    return Promise.all(results);
}

// 使用
const tasks = [() => fetch('/api/1'),
    () => fetch('/api/2'),
    () => fetch('/api/3')];

controlledPromiseQueue(tasks, 2).then(results => {
    console.log('所有请求完成');
});
```

---

## 本章小结

本章我们学习了一些实用的工具函数：

1. **防抖与节流**：控制函数执行频率，防止频繁触发。
2. **深拷贝与浅拷贝**：复制对象，JSON 方法、递归方法、structuredClone。
3. **数组操作**：扁平化、去重、洗牌、交集、并集、差集、分组。
4. **字符串与数值**：UUID、千分位格式化、URL 参数、Base64 编码。
5. **发布订阅**：EventEmitter 实现事件系统，Promise 队列控制并发。

这些工具函数在日常开发中非常实用。学会它们，你的代码会更加优雅、高效。

---

## 本章小结

从第28章到第37章，我们学习了 JavaScript 的进阶主题：

1. **事件基础**：事件绑定、事件对象、事件流、事件委托。
2. **事件类型**：鼠标事件、键盘事件、表单事件、资源事件、自定义事件、跨文档通信。
3. **网络请求**：XMLHttpRequest、Fetch API、JSON。
4. **客户端存储**：Cookie、Web Storage、IndexedDB。
5. **Proxy 与 Reflect**：代理器、拦截对象操作。
6. **Symbol**：独一无二的值、内置 Symbol。
7. **正则表达式**：字符类、量词、分组、字符串方法。
8. **错误处理**：try...catch、Error 对象、异步错误处理。
9. **调试**：console、断点调试、DevTools。
10. **工具函数**：防抖节流、深拷贝、数组操作、发布订阅。

JavaScript 的核心知识到这里就告一段落了！你已经掌握了 JavaScript 的基础知识、进阶主题和实用工具。继续深入学习吧！前端的世界还有很多精彩等着你！
