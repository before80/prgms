+++
title = "第 31 章 客户端存储"
weight = 310
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 31 章 客户端存储

网页关闭后，数据还在吗？JavaScript 有几种方式可以把数据存在浏览器里，这就是"客户端存储"。

## 31.1 Cookie

### 特点：约 4KB / 自动发送 / 同源策略

Cookie 是最早期的客户端存储方案，有点像"便利店的小票"——每次你去（请求服务器），店员都会看看你手里的小票（Cookie），记住你之前买过什么。

```javascript
// Cookie 的限制
// 1. 大小限制：约 4KB
// 2. 自动发送：每个请求都会带上
// 3. 同源策略：只能访问同源的 Cookie
```

### document.cookie：读写同一属性（写入追加不覆盖）

```javascript
// 读取所有 Cookie
console.log(document.cookie);

// 写入 Cookie（注意：是追加，不是覆盖！）
document.cookie = 'name=小明';
document.cookie = 'age=18';
document.cookie = 'city=北京';
console.log(document.cookie);
// 打印结果: name=小明; age=18; city=北京
```

### 属性：expires / path / domain / secure / HttpOnly

```javascript
// 设置过期时间（UTC 时间格式）
document.cookie = 'session=abc123; expires=Wed, 31 Dec 2025 23:59:59 GMT';

// max-age 用「还能活多少秒」表示过期，写法比 expires 简单，优先级也更高
document.cookie = 'session=abc123; max-age=3600'; // 1 小时后过期

// 设置路径
document.cookie = 'name=小明; path=/';

// 设置域
document.cookie = 'name=小明; domain=example.com';

// 安全标志（只能通过 HTTPS 传输）
document.cookie = 'secure_cookie=value; secure';

// HttpOnly 标志（只能通过 HTTP 访问，JavaScript 无法访问）
// 这个只能通过服务器设置
```

现代浏览器还要求显式声明 **SameSite**，它决定跨站请求时要不要带上这个 Cookie，是防御 CSRF 的第一道门槛：

```javascript
// Lax（多数浏览器的默认值）：普通的跨站跳转带上，跨站的表单提交/子请求不带
document.cookie = 'a=1; SameSite=Lax';

// Strict：任何跨站请求都不带，最严格，也最容易导致「从外站点进来就掉登录态」
document.cookie = 'b=1; SameSite=Strict';

// None：跨站也带上，但必须同时加 Secure，否则浏览器直接忽略
document.cookie = 'c=1; SameSite=None; Secure';
```

还有两点务必记住：

- **`HttpOnly` 的 Cookie 在 `document.cookie` 里是看不到的**，这不是 bug，正是它的设计目的（防止 XSS 偷走会话）。
- 需要注意 Cookie 的总量限制：单个 Cookie 约 4KB，且同一个域名下的 Cookie 数量也有上限（各浏览器大约 50 个），超出的旧 Cookie 会被挤掉。

### 读取与删除 Cookie

```javascript
// 读取指定名称的 Cookie
function getCookie(name) {
    for (const cookie of document.cookie.split('; ')) {
        // 用 indexOf 切分，因为值本身可能包含 '='
        const index = cookie.indexOf('=');
        if (index === -1) continue;
        const key = cookie.slice(0, index);
        if (key === name) {
            return decodeURIComponent(cookie.slice(index + 1));
        }
    }
    return null;
}

console.log(getCookie('name')); // 打印结果: 小明

// 写入时记得编码，否则值里的分号、逗号、空格会把 Cookie 写坏
document.cookie = `nickname=${encodeURIComponent('小明; 北京')}; path=/`;

// 删除 Cookie：把过期时间设为过去
// 关键点：path 和 domain 必须与创建时完全一致，否则删不掉（只是又写了一个空 Cookie）
function deleteCookie(name, path = '/') {
    document.cookie = `${name}=; path=${path}; max-age=0`;
}

deleteCookie('name');
```

正因为读写 Cookie 如此繁琐、还会拖慢每个请求，**业务数据尽量别放 Cookie**。今天的常规做法是：Cookie 只留给需要自动带给服务器的少量凭据（并设置 `HttpOnly` + `Secure` + 合适的 `SameSite`），其余数据交给 Web Storage 或 IndexedDB。

下一节，我们来学习 Web Storage！

## 31.2 Web Storage

### localStorage：永不过期 / 约 5MB / 同源

localStorage 就像一个"永久仓库"——只要你不动它，数据就会一直保存着。

```javascript
// 设置数据
localStorage.setItem('name', '小明');
localStorage.setItem('age', '18');

// 读取数据
console.log(localStorage.getItem('name')); // 打印结果: 小明

// 删除数据
localStorage.removeItem('age');

// 清空所有数据
localStorage.clear();

// 获取所有 key
for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    const value = localStorage.getItem(key);
    console.log(key + ': ' + value);
}
```

### sessionStorage：会话结束自动清除

sessionStorage 就像一个"临时储物柜"——浏览器关了，数据就没了。

```javascript
// 设置数据（会话结束时自动清除）
sessionStorage.setItem('tempData', '临时数据');

// 读取数据
console.log(sessionStorage.getItem('tempData')); // 打印结果: 临时数据

// 删除数据
sessionStorage.removeItem('tempData');

// 关闭浏览器标签页后，数据就清除了
```

### setItem / getItem / removeItem / clear / key

```javascript
// setItem：设置
localStorage.setItem('key1', 'value1');

// getItem：获取
const value = localStorage.getItem('key1');

// removeItem：删除
localStorage.removeItem('key1');

// clear：清空
localStorage.clear();

// key：获取指定索引的 key
const firstKey = localStorage.key(0);
```

### localStorage 只能存字符串的坑

```javascript
// ❌ 直接存对象，会变成 [object Object]
const user = { name: '小明', age: 18 };
localStorage.setItem('user', user);
console.log(localStorage.getItem('user')); // 打印结果: [object Object]

// ✅ 正确做法：转成 JSON
localStorage.setItem('user', JSON.stringify(user));
const storedUser = JSON.parse(localStorage.getItem('user'));
console.log(storedUser.name); // 打印结果: 小明
```

### storage 事件：跨标签页通信

```javascript
// 标签页 A
localStorage.setItem('message', 'Hello from tab A!');

// 标签页 B（在同一个域下）
window.addEventListener('storage', function(event) {
    console.log('key:', event.key);
    console.log('newValue:', event.newValue);
    console.log('oldValue:', event.oldValue);
    console.log('storageArea:', event.storageArea); // 是 localStorage 还是 sessionStorage
    console.log('url:', event.url);                 // 触发变化的那一页地址
});
```

这个事件有几个必须知道的行为，否则很容易以为「它坏了」：

- **触发变化的那一页自己收不到事件**，只有同源的其他标签页/窗口/iframe 会收到。要在本页也更新界面，得在写入后手动再调一次渲染逻辑。
- 调用 `clear()` 时 `event.key` 为 `null`。
- 同一个 key 被反复赋相同的值不会触发事件。
- 事件是**异步**派发的，不保证顺序。
- `sessionStorage` 的变动只在同一标签页内的嵌套 iframe 之间通知，跨标签页收不到。

### 容量、同步阻塞与异常

localStorage 看着像普通对象，但它是**同步 API**：读写会直接在主线程上完成，数据量大时会造成卡顿。把几 MB 的 JSON 在滚动回调里反复读写，掉帧是可以预期的。

```javascript
// 1. 容量是有限且按源共享的，写满会抛 QuotaExceededError
try {
    localStorage.setItem('big', JSON.stringify(hugeObject));
} catch (e) {
    if (e.name === 'QuotaExceededError' || e.code === 22) {
        console.warn('存储空间不足，先清理旧数据');
        localStorage.removeItem('oldCache');
    } else {
        throw e;
    }
}

// 2. 隐私模式、禁用存储、被策略封锁时，访问 localStorage 本身就可能抛错
function canUseStorage() {
    try {
        const k = '__test__';
        localStorage.setItem(k, '1');
        localStorage.removeItem(k);
        return true;
    } catch {
        return false;
    }
}

// 3. 存进去的字符串可能不是合法 JSON（被用户改过、被旧版本代码写坏）
function readJSON(key, fallback = null) {
    const raw = localStorage.getItem(key);
    if (raw === null) return fallback;
    try {
        return JSON.parse(raw);
    } catch {
        localStorage.removeItem(key);   // 删掉坏数据，避免每次都解析失败
        return fallback;
    }
}

// 4. 存进去的永远是字符串：数字取出来还是字符串，布尔值也变成 'true'
localStorage.setItem('count', 1);
console.log(typeof localStorage.getItem('count')); // 'string'
```

关于容量还有一个常见误解：各浏览器给出的「5MB」通常是指**字符数量**而非字节数。由于 JavaScript 字符串以 UTF-16 存放，中文与 emoji 占用的空间更多，实际能存的内容会比英文少不少。

### sessionStorage 的边界

sessionStorage 的「会话」是按**标签页（浏览上下文）**划分的，不是按「浏览器是否关闭」划分：

- 同一域名的两个标签页各自独立，互不可见；
- 刷新页面、前进后退，数据保留；
- 用 `target="_blank"` 打开新标签页时，**新标签页会复制一份当前的 sessionStorage**，之后两者各走各的；
- 复制标签页也会复制；
- 关闭标签页即销毁；但浏览器「恢复上次会话」时可能把它一起恢复。

所以不要把「用户是否登录」这类判断只依赖 sessionStorage。

下一节，我们来学习 IndexedDB！

## 31.3 IndexedDB

### 概念：浏览器端 NoSQL 数据库

IndexedDB 是浏览器里的"数据库"，可以存储大量结构化数据，比 localStorage 强大得多。

```javascript
// IndexedDB 的特点
// 1. 容量大：可以存储几百 MB 甚至 GB 的数据
// 2. 支持索引：可以快速查询
// 3. 支持事务：保证数据一致性
// 4. 异步 API：不会阻塞主线程
```

### 核心概念：数据库 / 对象仓库 / 事务 / 索引

```javascript
// 数据库（Database）：最大的容器
// 对象仓库（Object Store）：类似数据库的"表"
// 事务（Transaction）：保证操作的原子性
// 索引（Index）：加速查询
```

### 打开数据库：indexedDB.open() / onupgradeneeded

```javascript
// 打开数据库
const request = indexedDB.open('myDatabase', 1);

request.onupgradeneeded = function(event) {
    const db = event.target.result;
    
    // 创建对象仓库
    const store = db.createObjectStore('users', { keyPath: 'id' });
    
    // 创建索引
    store.createIndex('name', 'name', { unique: false });
    store.createIndex('email', 'email', { unique: true });
};

request.onsuccess = function(event) {
    const db = event.target.result;
    console.log('数据库打开成功');
};

request.onerror = function(event) {
    console.log('数据库打开失败');
};
```

### 对象仓库主键：keyPath / autoIncrement

```javascript
// keyPath：使用对象的某个属性作为主键
db.createObjectStore('users', { keyPath: 'id' });

// autoIncrement：自动生成数字主键
db.createObjectStore('logs', { keyPath: 'id', autoIncrement: true });
```

### 增删改查：add / put / get / delete / getAll / clear

```javascript
// 在事务中进行操作
function addUser(db, user) {
    const transaction = db.transaction(['users'], 'readwrite');
    const store = transaction.objectStore('users');
    
    // 添加数据
    const request = store.add(user);
    request.onsuccess = function() {
        console.log('用户添加成功');
    };
}

// 读取数据
function getUser(db, id) {
    const transaction = db.transaction(['users'], 'readonly');
    const store = transaction.objectStore('users');
    
    const request = store.get(id);
    request.onsuccess = function() {
        console.log('用户信息：', request.result);
    };
}

// 更新数据（如果 key 已存在则更新）
function updateUser(db, user) {
    const transaction = db.transaction(['users'], 'readwrite');
    const store = transaction.objectStore('users');
    store.put(user);
}

// 删除数据
function deleteUser(db, id) {
    const transaction = db.transaction(['users'], 'readwrite');
    const store = transaction.objectStore('users');
    store.delete(id);
}

// 获取所有数据
function getAllUsers(db) {
    const transaction = db.transaction(['users'], 'readonly');
    const store = transaction.objectStore('users');
    
    const request = store.getAll();
    request.onsuccess = function() {
        console.log('所有用户：', request.result);
    };
}

// 清空仓库
function clearUsers(db) {
    const transaction = db.transaction(['users'], 'readwrite');
    const store = transaction.objectStore('users');
    store.clear();
}
```

### 版本升级：onupgradeneeded 只在版本号变化时触发

`indexedDB.open(name, version)` 的第二个参数是版本号。**只有传入的版本号大于已存在的版本时**，才会触发 `onupgradeneeded`。这意味着「加一个字段」「加一个索引」都必须把版本号 +1，否则代码根本不会执行：

```javascript
const request = indexedDB.open('myDatabase', 2); // 从 1 升到 2

request.onupgradeneeded = function (event) {
    const db = event.target.result;
    const tx = event.target.transaction; // 升级期间可以拿到这个事务

    // 注意：升级时不能删除仍被现存对象引用的对象仓库，也不能边遍历边改结构
    if (!db.objectStoreNames.contains('users')) {
        const store = db.createObjectStore('users', { keyPath: 'id' });
        store.createIndex('name', 'name', { unique: false });
    }
    if (!db.objectStoreNames.contains('logs')) {
        db.createObjectStore('logs', { keyPath: 'id', autoIncrement: true });
    }

    // 需要给已有数据补字段时，遍历游标在升级事务里完成
    if (tx) {
        tx.objectStore('users').openCursor().onsuccess = (e) => {
            const cursor = e.target.result;
            if (!cursor) return;
            const value = cursor.value;
            value.createdAt ??= Date.now();
            cursor.update(value);
            cursor.continue();
        };
    }
};

// 版本号比现有版本低时会直接报 VersionError，所以线上不要随意回滚版本号
```

### 事务的一个大坑：不要在中间 await

IndexedDB 的事务会在「事件循环空闲」时自动提交。一旦你在事务里 `await` 了一个跟这个事务无关的异步操作（比如 `fetch`、`setTimeout`），本轮微任务结束后事务就提交了，后续操作会抛 `TransactionInactiveError`：

```javascript
// ❌ 事务会因为中间的 await 提前提交
async function badAdd(db, user) {
    const tx = db.transaction(['users'], 'readwrite');
    const store = tx.objectStore('users');
    const extra = await fetch('/api/extra').then((r) => r.json()); // 事务在这里就废了
    store.add({ ...user, extra });                                 // TransactionInactiveError
}

// ✅ 先把异步数据准备好，再开启事务
async function goodAdd(db, user) {
    const extra = await fetch('/api/extra').then((r) => r.json());
    const tx = db.transaction(['users'], 'readwrite');
    tx.objectStore('users').add({ ...user, extra });
    // 事务会在本段同步代码结束后自动提交
}

// ✅ 确实需要等事务结束，就监听 oncomplete
function waitTx(tx) {
    return new Promise((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error ?? new Error('事务被中止'));
    });
}
```

### 用 Promise 包一层

原生 IndexedDB 全部靠事件回调，写起来冗长。实际项目中要么用 `idb` 这类小库，要么自己封装一层：

```javascript
function requestToPromise(request) {
    return new Promise((resolve, reject) => {
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function getUsersByName(db, name) {
    const tx = db.transaction(['users'], 'readonly');
    const index = tx.objectStore('users').index('name');
    return requestToPromise(index.getAll(IDBKeyRange.only(name)));
}

// 注意：包成 Promise 后仍然要遵守「事务内不要 await 无关操作」的规则

// 关闭连接与删除整个数据库
// db.close();
// const delReq = indexedDB.deleteDatabase('myDatabase');
// delReq.onsuccess = () => console.log('数据库已删除');
// delReq.onblocked  = () => console.warn('还有标签页占用这个数据库，先关掉它们');
```

### 常见错误与排查

| 现象 | 原因 |
| --- | --- |
| `onupgradeneeded` 里的代码不执行 | 版本号没加，或者数据库名拼错导致每次都新建 |
| `ConstraintError` | 向 `unique: true` 的索引写入了重复值 |
| `TransactionInactiveError` | 事务中途 `await` 了无关的异步操作 |
| `VersionError` | 请求的版本号低于当前数据库版本 |
| `onblocked` 一直不回调 | 其他标签页还开着旧版本连接，需要先 `db.close()` |
| 明明写入了却查不到 | 用了 `readonly` 事务，或者没等 `transaction.oncomplete` 就去读 |

## 31.4 该选哪种存储

| 方案 | 容量 | 是否随请求发送 | 生命周期 | 适合放什么 |
| --- | --- | --- | --- | --- |
| Cookie | 约 4KB | 是（同源请求自动带上） | 可设置，最长到指定日期 | 会话标识、需要服务端读取的少量信息 |
| sessionStorage | 约 5MB | 否 | 标签页关闭即销毁 | 表单向导中间状态、临时筛选条件、页面内一次性数据 |
| localStorage | 约 5MB | 否 | 永久，除非主动清除 | 主题偏好、语言设置、非敏感的轻量配置 |
| IndexedDB | 数百 MB 起，受配额限制 | 否 | 永久，除非主动清除 | 大量结构化数据、离线缓存、需要索引查询或事务的场景 |
| Cache Storage | 受配额限制 | 否 | 永久，除非主动清除 | Service Worker 缓存的静态资源与接口响应 |

一句话原则：**需要自动发给服务器的放 Cookie（并设好 HttpOnly/Secure/SameSite），其余数据按体积和查询需求选 Web Storage 或 IndexedDB**。任何存储方案都不要保存密码、完整身份证号、支付凭据这类敏感数据——前端存储对同源脚本完全开放，一旦出现 XSS 就等于全部泄露。

想知道当前站点用了多少空间、能不能申请「持久化」（避免浏览器在磁盘紧张时清掉你的数据），用 StorageManager：

```javascript
async function checkStorage() {
    if (navigator.storage?.estimate) {
        const { usage, quota } = await navigator.storage.estimate();
        console.log(`已用 ${(usage / 1024 / 1024).toFixed(2)} MB，配额约 ${(quota / 1024 / 1024).toFixed(0)} MB`);
    }

    // 申请持久化存储：通过后浏览器不会在空间紧张时自动清除本站数据
    if (navigator.storage?.persist) {
        const granted = await navigator.storage.persist();
        console.log('持久化存储是否获批：', granted);
    }
}

checkStorage();
```

另外，浏览器清理「可清除」存储的策略是：**磁盘空间紧张时优先清理长时间未访问的站点数据**。所以即使没写 `clear()`，localStorage 里的内容也不能视为绝对可靠，重要数据仍然要以服务端为准。

---

## 本章小结

本章我们学习了客户端存储：

1. **Cookie**：约 4KB、随请求自动发送，通过 `document.cookie` 读写；`expires`/`max-age` 控制有效期，`path`/`domain` 必须一致才能删除，`HttpOnly` 的 Cookie 前端看不到。
2. **SameSite**：`Lax`/`Strict`/`None` 决定跨站请求是否携带 Cookie，`None` 必须搭配 `Secure`。
3. **Web Storage**：只能存字符串（对象要 `JSON.stringify`）；localStorage 持久、sessionStorage 随标签页销毁；同步 API 会阻塞主线程，写满会抛 `QuotaExceededError`。
4. **storage 事件**：只通知同源的其他标签页，触发方自己收不到。
5. **IndexedDB**：支持大容量、索引与事务的浏览器数据库；升级结构要提升版本号，事务中不要 `await` 无关的异步操作。
6. **选型与配额**：按「是否要发往服务端、体积、查询需求」选择存储方案，用 `navigator.storage.estimate()` 查看用量、`persist()` 申请持久化；前端存储一律不放敏感数据。

下一章，我们要学习 Proxy 与 Reflect——JavaScript 的"拦截器"！
