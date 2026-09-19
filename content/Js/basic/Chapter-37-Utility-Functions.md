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

```javascript
// 实战中最好再给防抖函数补上 cancel()：组件卸载或切换页面时，
// 把还没到期的定时器清掉，避免"页面都走了还在发请求"。
function debounce(func, delay) {
  let timer = null;

  function debounced(...args) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      func.apply(this, args);   // ⭐ 箭头函数继承外层 this，调用者是谁就传给谁
    }, delay);
  }

  debounced.cancel = function () {
    if (timer) clearTimeout(timer);
    timer = null;
  };

  debounced.flush = function (...args) {   // 想立刻执行一次
    if (!timer) return;
    clearTimeout(timer);
    timer = null;
    func(...args);    // 注意：这里是"工具函数主动调用"，this 已不是原来的调用者
  };

  return debounced;
}

// 用法
const onResize = debounce(handleResize, 200);
window.addEventListener('resize', onResize);
// 组件卸载时
// onResize.cancel();
```

### throttle：n 毫秒内只执行一次

节流就像"机关枪"——不管你怎么疯狂扣扳机，子弹都按固定节奏往外射。
和防抖的区别在于：防抖是"等你停下来才执行一次"，节流是"过程中也按节奏执行"。

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

> ⚠️ **上面这个"朴素版"节流有两个可感知的缺陷**（面试和实际项目里都会被问到）：
>
> 1. **最后一帧会被丢掉**：滚动停止的那一刻如果还没到下一个 100ms，那次的最终位置就永远不会被处理。
>    比如拖拽结束时想记录最终坐标，用它就会差一点。
> 2. **用的是 `Date.now()`**：系统时间被改动（或遇到闰秒调整）会跳。做性能相关计时应该用
>    `performance.now()`（单调递增，不受系统时间影响）。
>
> 补上 `trailing`（记录并补发最后一次）的版本：
>
> ```javascript
> function throttle(func, interval) {
>   let lastTime = 0;
>   let timer = null;
>   let lastArgs = null;
>   let lastContext = null;
>
>   return function (...args) {
>     const now = performance.now();
>     lastArgs = args;
>     lastContext = this;
>
>     if (now - lastTime >= interval) {
>       lastTime = now;
>       func.apply(this, args);          // 立刻执行（leading）
>     } else if (!timer) {
>       // 安排一次"补发"，把这段时间里最后一次的参数用上
>       timer = setTimeout(() => {
>         timer = null;
>         lastTime = performance.now();
>         func.apply(lastContext, lastArgs);
>       }, interval - (now - lastTime));
>     }
>   };
> }
> ```

> 💡 顺便说一句：很多库（如 Lodash）的 `throttle` / `debounce` 都提供了
> `leading`（首次是否立即执行）和 `trailing`（结束后是否补发一次）两个开关。
> 自己写之前，先想清楚这两个语义，不然很容易出现"拖拽结束后位置没对上"这类 bug。

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
    
    // 处理 Map / Set（这两个不处理的话，会被当成空对象克隆）
    if (obj instanceof Map) {
        const cloned = new Map();
        hash.set(obj, cloned);
        obj.forEach((value, key) => cloned.set(deepClone(key, hash), deepClone(value, hash)));
        return cloned;
    }
    if (obj instanceof Set) {
        const cloned = new Set();
        hash.set(obj, cloned);
        obj.forEach((value) => cloned.add(deepClone(value, hash)));
        return cloned;
    }

    // 处理数组或普通对象
    const cloned = Array.isArray(obj) ? [] : {};
    hash.set(obj, cloned);
    
    for (const key in obj) {
        // ⭐ 用 Object.hasOwn 而不是 obj.hasOwnProperty：
        // 如果对象是用 Object.create(null) 创建的，它根本没有 hasOwnProperty 方法。
        if (Object.hasOwn(obj, key)) {
            cloned[key] = deepClone(obj[key], hash);
        }
    }

    // ⭐ 别忘了 Symbol 作为键的属性：for...in 是遍历不到的
    for (const sym of Object.getOwnPropertySymbols(obj)) {
        cloned[sym] = deepClone(obj[sym], hash);
    }
    
    return cloned;
}

// 测试
const original = { date: new Date(), regex: /test/g };
const copy = deepClone(original);
console.log(copy.date instanceof Date); // 打印结果: true
console.log(copy.regex.source); // 打印结果: test
```

> ⚠️ **手写深拷贝永远做不"全"**，这是它的固有局限：
>
> - 上面这份代码**不会保留原型**，`class` 实例克隆后会变成普通对象，方法全丢；
> - `Object.defineProperty` 定义的不可枚举属性、getter/setter 都会被拍平成普通属性；
> - `Promise`、`WeakMap`、`WeakSet`、DOM 节点、函数都没法真正克隆（函数通常直接返回原引用）；
> - 循环引用虽然用 `WeakMap` 处理了，但真正的难点在于各种内置类型的细节。
>
> 所以实际项目里：**能用 `structuredClone` 就用它**，需要保留原型或处理特殊类型时，
> 优先考虑成熟的库，或者干脆换成"不可变数据"的设计思路，从源头避免深拷贝。

### structuredClone（浏览器 2022 年起支持，Node.js 17+）

> 📌 先澄清一个常见误会：`structuredClone` **不是 ES6/ES2021 的语言特性**，
> 而是浏览器提供的一个全局函数（属于 HTML 结构化克隆算法），
> Chrome 98+、Firefox 94+、Safari 15.4+、Node.js 17+ 才可用。

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

```javascript
// structuredClone 的能力边界（这些是它比 JSON 方案强的地方）
const source = {
  date: new Date(),                 // ✅ Date 会被正确克隆（JSON 会变成字符串）
  map: new Map([['a', 1]]),         // ✅ Map / Set 支持
  set: new Set([1, 2]),
  buf: new Uint8Array([1, 2, 3]),   // ✅ 二进制数组支持，且是真正独立的内存
  inf: Infinity,                    // ✅ Infinity / NaN 保留（JSON 会变成 null）
  undef: undefined,                 // ✅ undefined 保留（JSON 会直接丢掉这个键）
  cyclic: null
};
source.cyclic = source;             // ✅ 循环引用也能处理

const clone = structuredClone(source);
console.log(clone.buf !== source.buf, clone.buf[0]);  // true 1

// ⚠️ 但它也有限制：
// 1. 不能克隆函数、DOM 节点、Promise、WeakMap —— 会抛 DataCloneError
// 2. 会丢掉对象的原型（class 实例会变成普通对象，方法没了）
// 3. Symbol 作为"键"的属性会被忽略，Symbol 作为值会抛错
// 4. getter 会被"求值"，得到的是当时的值，而不是保留 getter
// structuredClone({ fn: () => {} });  // ❌ DataCloneError

// 顺带一提：它还能转移"所有权"而不是复制，适合传大数据给 Worker
// const transferred = structuredClone(buffer, { transfer: [buffer] });
// 转移之后，原来的 buffer 会被清空（byteLength 变成 0）
```

下一节，我们来学习数组操作！

## 37.3 数组操作

### 扁平化：flat / reduce / 正则

```javascript
const nested = [1, [2, [3, [4, [5]]]]];   // ⚠️ 方括号必须一一配对

// flat：ES2019+
console.log(nested.flat(Infinity)); // 打印结果: [1, 2, 3, 4, 5]

// 也可以控制扁平化的层数
console.log(nested.flat(1));        // 打印结果: [1, 2, [3, [4, [5]]]]
console.log(nested.flat(2));        // 打印结果: [1, 2, 3, [4, [5]]]

// reduce
function flattenDeep(arr) {
    return arr.reduce((acc, val) => 
        Array.isArray(val) ? acc.concat(flattenDeep(val)) : acc.concat(val)
    , []);
}
console.log(flattenDeep(nested)); // 打印结果: [1, 2, 3, 4, 5]

// 还想更省事？flatMap 可以先映射再扁平一层：
console.log([[1], [2, 3]].flatMap(x => x)); // 打印结果: [1, 2, 3]
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

> ⚠️ **三种写法在"特殊值"上的行为并不一致**，这一点最容易被忽略：
>
> ```javascript
> const tricky = [NaN, NaN, 0, -0, null, undefined];
>
> console.log([...new Set(tricky)]);   // [ NaN, 0, null, undefined ]
> // Set 用 SameValueZero 比较：两个 NaN 合成 1 个，0 和 -0 视为同一个
>
> console.log(tricky.filter((v, i) => tricky.indexOf(v) === i)); // [ 0, null, undefined ]
> // indexOf 用的是严格相等：NaN !== NaN，它永远返回 -1，
> // 于是 NaN 被当成"重复项"整个丢掉了——这往往不是你想要的结果
> ```
>
> 所以"去重"要看你想要哪种语义：一般用 `Set` 就好；
> 如果你的数组里可能有 `NaN`，而你又希望它保留，那 `Set` 反而不符合预期。

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

> ⚠️ **这个手写版本有两个坑**：
>
> 1. **键会被强制转成字符串**：`groupBy(users, 'age')` 得到的键是 `'18'`、`'20'`，不是数字。
>    如果键是对象，所有东西都会被塞进 `'[object Object]'` 这一个分组里。
> 2. **危险键名会出问题**：`groups[group] || []` 遇到 `group === '__proto__'` 时，
>    `groups['__proto__']` 拿到的是 `Object.prototype`（真值），接着 `.push` 就会报
>    "not a function"；用 `constructor`、`toString` 也会踩到类似的坑。
>
> 想要更安全、更现代的写法，直接用内置的静态方法（ES2024）：
>
> ```javascript
> // 键是字符串或 symbol 时用 Object.groupBy，返回"无原型"的对象
> console.log(Object.groupBy(users, u => u.age));
>
> // 键可能是任意值（对象、数字）时用 Map.groupBy
> const byIsAdult = Map.groupBy(users, u => u.age >= 18 ? 'adult' : 'minor');
> console.log(byIsAdult.get('adult'));
> ```

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

// ⚠️ 直接对中文调用 btoa 会报错：
// btoa('你好');  // InvalidCharacterError: 只有 0~255 范围的字符才被接受

// 处理中文：先百分号编码，再 Base64
const str = '你好';
const encoded2 = btoa(encodeURIComponent(str));
console.log(encoded2); // 打印结果: JUU0JUJEJUEwJUU1JUE1JUJE
const decoded2 = decodeURIComponent(atob(encoded2));
console.log(decoded2); // 打印结果: 你好
```

> 💡 **上面那个"先 encodeURIComponent 再 Base64"的结果会变长**（中文变成 `%XX` 形式，体积暴涨）。
> 如果想要"真正的 UTF-8 字节 → Base64"，正确做法是先转字节再编码：
>
> ```javascript
> // 编码：字符串 → UTF-8 字节 → Base64
> function toBase64(str) {
>   const bytes = new TextEncoder().encode(str);
>   let binary = '';
>   for (const byte of bytes) binary += String.fromCharCode(byte);
>   return btoa(binary);
> }
>
> // 解码：Base64 → 字节 → 字符串
> function fromBase64(base64) {
>   const binary = atob(base64);
>   const bytes = Uint8Array.from(binary, (ch) => ch.charCodeAt(0));
>   return new TextDecoder().decode(bytes);
> }
>
> console.log(toBase64('你好'));      // 5L2g5aW9
> console.log(fromBase64('5L2g5aW9'));  // 你好
> ```
>
> 浏览器里更省事的写法是用 `FileReader.readAsDataURL()` 或 `Blob`；
> Node.js 里直接用 `Buffer.from(str, 'utf8').toString('base64')`。

下一节，我们来学习发布订阅！

## 37.5 发布订阅

### EventEmitter：on / off / emit / once

```javascript
class EventEmitter {
    constructor() {
        // ⭐ 用 Object.create(null) 而不是 {}：
        // 否则 on('toString', fn) 或 on('__proto__', fn) 会撞上 Object.prototype 上的属性，
        // 出现"events[event] 已经是真值，但 .push 不是函数"的诡异报错。
        this.events = Object.create(null);
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

        // ⭐ 先复制一份再遍历：
        // 如果某个监听器在回调里把自己 off 掉（或者再 on 新的监听器），
        // 直接遍历原数组会导致漏执行或行为不可预测。
        [...this.events[event]].forEach(listener => listener(...args));
        return this;
    }
    
    once(event, listener) {
        const wrapper = (...args) => {
            // ⭐ 用 try/finally 保证即使监听器抛错，也只触发一次
            try {
                listener(...args);
            } finally {
                this.off(event, wrapper);
            }
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

```javascript
// 如果只是想给"某个事件通知多个订阅者"，浏览器原生就有更省事的方案：
const bus = new EventTarget();

bus.addEventListener('message', (e) => console.log('A 收到：', e.detail));
bus.addEventListener('message', (e) => console.log('B 收到：', e.detail));

// 一次性监听
bus.addEventListener('ready', () => console.log('只执行一次'), { once: true });

// 派发（要带数据必须用 CustomEvent）
bus.dispatchEvent(new CustomEvent('message', { detail: 'Hello!' }));

// ⭐ 对比一下：
// - 自己写 EventEmitter：可控性强，能 `off`、能拦截、能实现优先级，但要自己维护
// - EventTarget：浏览器原生、零依赖，缺点是 event.type 只能是字符串、没有"通配符"监听
```

### Promise 队列：控制并发

```javascript
// 控制并发的 Promise 队列 —— "工人池"写法
//
// ⚠️ 先说说为什么不能这么写：
//   const promise = Promise.resolve().then(() => task());
// 这行代码在创建的瞬间就把 task() 排进了微任务队列。
// 结果就是任务"按顺序排好队，却全都抢跑了"，实际并发数会超过 limit
// （实测：limit 设成 2，峰值能到 3 甚至更多）。
// 想真正限流，必须做到一件事：任务要等到有空位才开始执行。

async function runWithConcurrency(tasks, limit = 3) {
  const results = new Array(tasks.length);
  let nextIndex = 0;

  // 每个 worker 就是一个"工人"：只要还有任务，就拿一个来做，做完再拿下一个
  async function worker() {
    while (nextIndex < tasks.length) {
      const index = nextIndex++;        // ⭐ 同步取出下标，天然不会重复
      results[index] = await tasks[index]();
    }
  }

  // 开 min(limit, 任务数) 个工人，一起把任务做完
  const workers = Array.from(
    { length: Math.min(limit, tasks.length) },
    () => worker()
  );

  await Promise.all(workers);
  return results;   // ⭐ 返回顺序和传入的 tasks 顺序一致
}

// 使用
const tasks = [
  () => fetch('/api/1').then(r => r.json()),
  () => fetch('/api/2').then(r => r.json()),
  () => fetch('/api/3').then(r => r.json()),
  () => fetch('/api/4').then(r => r.json())
];

runWithConcurrency(tasks, 2).then(results => {
  console.log('所有请求完成，最多同时只有 2 个在跑：', results);
});

// ⭐ 注意一个细节：某个任务 reject 时，Promise.all 会立刻抛出，
//    但其他已经在跑的任务不会自动中止。
//    想要"一个失败就全部取消"，用 AbortController 配合 Promise.allSettled。
```

---

## 本章小结

本章我们学习了一些实用的工具函数：

1. **防抖与节流**：控制函数执行频率，防止频繁触发。
2. **深拷贝**：`JSON.parse(JSON.stringify())` 简单但会丢 Date/undefined、遇循环引用报错；手写递归能处理 Map/Set/循环引用，但保留不了原型；`structuredClone` 是当下最省心的选择（注意它不是 ES2022 的语言特性，而是浏览器/Node 提供的全局函数）。
3. **数组操作**：扁平化（`flat(Infinity)`）、去重（`Set` 与 `indexOf` 在 `NaN` 上行为不同）、Fisher-Yates 洗牌、交集/并集/差集、分组（可用 `Object.groupBy`）。
4. **字符串与数值**：UUID（需要安全上下文）、千分位格式化、URL 参数、Base64（中文要先用 `TextEncoder` 转字节）。
5. **发布订阅**：自己实现 `EventEmitter` 时记得用 `Object.create(null)` 存事件表；浏览器原生有 `EventTarget` / `BroadcastChannel`；控制并发要用"工人池"，而不是"先把 Promise 全建好"。

这些工具函数在日常开发中非常实用。学会它们，你的代码会更加优雅、高效。

---

## 阶段小结（第 28 ～ 37 章）

从第 28 章到第 37 章，我们学习了 JavaScript 的进阶主题：

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
