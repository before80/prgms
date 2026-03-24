+++
title = "第 36 章 调试"
weight = 360
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 36 章 调试

代码写错了怎么办？调试就是帮你找到并修复 bug 的过程。JavaScript 提供了多种调试工具，让 bug 无所遁形。

## 36.1 console

### log / warn / error / info

```javascript
// log：普通日志
console.log('这是一条普通日志');

// warn：警告
console.warn('这是一条警告');

// error：错误
console.error('这是一条错误');

// info：信息
console.info('这是一条信息');
```

### %s / %d / %o 格式化 / %c 自定义样式

```javascript
// %s：字符串
console.log('Hello, %s!', 'World'); // 打印结果: Hello, World!

// %d：数字
console.log('年龄：%d', 18); // 打印结果: 年龄：18

// %o：对象
const obj = { name: '小明', age: 18 };
console.log('对象：%o', obj);

// %c：自定义样式
console.log('%c红色文字', 'color: red; font-size: 20px');
console.log('%c蓝色%c红色', 'color: blue', 'color: red');
```

### assert / group / count / time / trace / table

```javascript
// assert：断言
console.assert(1 === 1, '这行不会打印');
console.assert(1 === 2, '这行会打印，因为条件不满足');

// group：分组
console.group('用户信息');
console.log('姓名：小明');
console.log('年龄：18');
console.groupEnd();

// count：计数
function test() {
    console.count('函数调用次数');
}
test(); // 打印结果: 函数调用次数: 1
test(); // 打印结果: 函数调用次数: 2

// time / timeEnd：计时
console.time('耗时操作');
for (let i = 0; i < 1000; i++) {}
console.timeEnd('耗时操作'); // 打印结果: 耗时操作: 1.23ms

// trace：堆栈跟踪
function a() { b(); }
function b() { c(); }
function c() { console.trace('调用栈'); }
a();

// table：表格显示
const users = [
    { name: '小明', age: 18 },
    { name: '小红', age: 20 }
];
console.table(users);
```

下一节，我们来学习断点调试！

## 36.2 断点调试

### debugger 语句

在代码中加入 `debugger` 语句，浏览器会在该位置自动暂停执行。

```javascript
function calculateSum(n) {
    let sum = 0;
    debugger; // 程序会在这里暂停
    for (let i = 1; i <= n; i++) {
        sum += i;
    }
    return sum;
}

console.log(calculateSum(10));
```

### Chrome DevTools Sources：普通断点 / 条件断点 / XHR 断点

```javascript
// 普通断点：在 Sources 面板点击行号
function buggyFunction() {
    let result = 0; // 在这行点击设置断点
    for (let i = 0; i < 10; i++) {
        result += i;
    }
    return result;
}

// 条件断点：右键点击行号，输入条件
// 当 i === 5 时暂停
function conditionalBreakpoint() {
    for (let i = 0; i < 10; i++) {
        console.log(i); // 在这里设置条件断点：i === 5
    }
}

// XHR 断点：在 Sources 面板的 XHR Breakpoints 中添加 URL 条件
// 当请求的 URL 包含特定字符串时暂停
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data));
```

### VS Code 断点调试：launch.json

```json
// launch.json 配置
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "启动调试",
            "skipFiles": ["<node_internals>/**"],
            "program": "${workspaceFolder}/app.js"
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome 调试",
            "url": "http://localhost:3000",
            "webRoot": "${workspaceFolder}"
        }
    ]
}
```

下一节，我们来学习面板工具！

## 36.3 面板工具

### Network：网络请求分析

Network 面板可以查看所有的网络请求，包括请求头、响应头、响应内容、耗时等。

```javascript
// 在 Network 面板可以看到这个请求的详细信息
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data));
```

### Performance：性能分析（帧率 / 函数耗时）

Performance 面板可以记录页面的性能数据，包括帧率、函数调用耗时、布局计算等。

### Memory：内存分析（堆快照 / 泄漏检测）

Memory 面板可以进行堆快照分析，检测内存泄漏。

```javascript
// 内存泄漏示例：闭包导致变量无法释放
function createLeak() {
    const largeData = new Array(100000).fill('data');
    
    return function() {
        console.log(largeData.length);
    };
}

const leaked = createLeak();
leaked(); // largeData 永远不会被释放
```

### source map：压缩代码调试

```javascript
// 生产环境使用压缩的 JavaScript
// <script src="bundle.min.js.map" />

// source map 可以让压缩代码的报错指向源代码
// 开发时启用 source map，生产时可以使用
```

---

## 本章小结

本章我们学习了调试工具：

1. **console**：log、warn、error、info、assert、group、count、time、trace、table。
2. **断点调试**：debugger 语句、Chrome DevTools、VS Code。
3. **面板工具**：Network、Performance、Memory、source map。

调试是每个程序员必备的技能。学会使用这些工具，你就能快速定位并修复 bug。

下一章，我们要学习工具函数——让代码更优雅！
