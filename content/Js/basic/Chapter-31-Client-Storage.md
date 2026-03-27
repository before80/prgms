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
document.cookie = 'session=abc123; expires=Thu, 31 Dec 2024 23:59:59 GMT';

// 设置路径
document.cookie = 'name=小明; path=/;';

// 设置域
document.cookie = 'name=小明; domain=example.com';

// 安全标志（只能通过 HTTPS 传输）
document.cookie = 'secure_cookie=value; secure';

// HttpOnly 标志（只能通过 HTTP 访问，JavaScript 无法访问）
// 这个只能通过服务器设置
```

### 读取与删除 Cookie

```javascript
// 读取指定名称的 Cookie
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

console.log(getCookie('name')); // 打印结果: 小明

// 删除 Cookie（设置过期时间为过去的时间）
function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT';
}

deleteCookie('name');
```

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
});
```

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

---

## 本章小结

本章我们学习了客户端存储：

1. **Cookie**：约 4KB，自动发送，适合少量数据。
2. **Web Storage**：localStorage 永不过期，sessionStorage 会话结束清除，只能存字符串。
3. **IndexedDB**：浏览器端数据库，支持大量数据、索引、事务。

下一章，我们要学习 Proxy 与 Reflect——JavaScript 的"拦截器"！
