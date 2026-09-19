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

// table 的第二个参数可以只列感兴趣的列
console.table(users, ['name']);

// group + collapsed：折叠分组，日志多时很好用
console.groupCollapsed('详细信息');
console.dir(users);
console.groupEnd();

// timeLog：计时中途打点，不结束计时
console.time('循环');
for (let i = 0; i < 3; i++) {
    console.timeLog('循环', `第 ${i} 次`);
}
console.timeEnd('循环');

// countReset：把计数清零
console.countReset('函数调用次数');
```

几个容易混淆的点：

- `console.log` 打印对象时，浏览器控制台显示的是**引用**。你展开它时看到的是「展开那一刻」的值，不是打印那一刻的值。要冻结当时的值，用 `console.log(JSON.parse(JSON.stringify(obj)))` 或 `console.log(structuredClone(obj))`。
- `console.error` 和 `console.warn` 除了样式不同，还带有堆栈，可以直接点开看是哪一行调用的，排查时比 `log` 更有用。
- `%o` 与 `%O` 在浏览器里几乎等价，在 Node.js 中 `%o` 走简洁格式、`%O` 走完整格式（等同 `util.inspect` 的更多选项）。

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

除了上面三种，DevTools 还有几类在实战中非常好用的断点：

| 断点类型 | 位置 | 典型用途 |
| --- | --- | --- |
| 日志点（Logpoint） | 右键行号 → Add logpoint | 不暂停执行，只打印一段表达式，效果类似临时 `console.log` 但不改代码 |
| 异常断点 | Sources → 右侧「暂停在异常」图标 | 让调试器在抛异常处停下，可选「只暂停未捕获的异常」 |
| DOM 断点 | Elements 面板右键节点 → Break on | 元素被修改、被删除、属性变化时暂停，定位「谁偷偷改了 DOM」 |
| 事件监听断点 | Sources → Event Listener Breakpoints | 在 click、scroll、submit 等事件回调入口处暂停 |
| 代码中打标记 | 控制台执行 `debug(fn)` / `undebug(fn)` | 让某个函数每次被调用都自动暂停 |

> 常见的「断点打不上」有两种原因：一是该行代码已经被浏览器缓存或代码行号对不上，需要刷新并确认加载的是最新文件；二是断点被放在注释、空行或已经无用代码（unused code）上，压缩工具把这段代码删掉了。

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

配置时有两个常见报错：

- `type: "chrome"` 依赖已停止维护的 Debugger for Chrome 扩展。新版本的 VS Code 改用内置的 JS 调试器，把这个值换成 `"pwa-chrome"`（Edge 用 `"msedge"`）即可正常使用。
- 调试 TypeScript 时，如果断点位置和源码对不上，通常是因为缺少 source map。除了在 `tsconfig.json` 里打开 `"sourceMap": true`，还可以在配置里补上 `"sourceMaps": true` 和 `"resolveSourceMapLocations"`，把映射范围限制在源码目录内。

调试 Node.js 也可以不开编辑器，直接用命令行挂上调试器：

```bash
# 在代码第一行就暂停，适合调试启动阶段的问题
node --inspect-brk ./app.js

# 启动后不暂停，等你在 DevTools 里点继续
node --inspect ./app.js

# 然后在 Chrome 里打开 chrome://inspect 点击 inspect
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

Memory 面板的主要用法是**堆快照对比**：在操作前后各拍一张快照，切换到 Comparison 视图，看哪些对象「只增不减」。用 `Detached` 可以专门筛出已经脱离文档树的 DOM 节点，这是最典型的泄漏信号。

需要澄清一个常见误解：**闭包本身不是内存泄漏**。下面这段代码没有任何问题——只要 `leaked` 还被引用，`largeData` 就应该活着；一旦 `leaked = null`，两者都会被回收。

```javascript
function createClosure() {
    const largeData = new Array(100000).fill('data');
    return function() {
        console.log(largeData.length);   // 闭包持有 largeData，这是设计如此
    };
}

let leaked = createClosure();
leaked();
leaked = null;   // 引用断开后，闭包和 largeData 都可以被回收
```

真正会造成泄漏的是「本该断开的引用没有断开」：

```javascript
// 1. 忘记移除的定时器：回调持续引用组件数据，并使回调永远存活
const timer = setInterval(() => {
    renderFrom(this.data);
}, 1000);
// 组件卸载时必须 clearInterval(timer)

// 2. 忘记移除的事件监听：DOM 被移除但监听器还挂在 window 上
window.addEventListener('resize', onResize);
// 卸载时必须 window.removeEventListener('resize', onResize)

// 3. 全局缓存只增不减：这是最隐蔽的一类
const cache = new Map();
function getUser(id) {
    if (!cache.has(id)) cache.set(id, buildHugeObject(id));   // 永远不会淘汰
    return cache.get(id);
}
// 换成 WeakMap，或给 Map 加上容量上限与淘汰策略
```

排查顺序一般是：持续复现操作 → 拍快照 → 再复现一次 → 对比快照。如果同一类对象数量每次都稳步增加，而且 Retainers 面板里能一路走回到某个长久存活的全局对象，基本就能确定泄漏源了。

### source map：压缩代码调试

打包后的代码被压缩成一行、变量名变成 `a`、`b`、`c`，报错堆栈自然也对不上源码。source map 就是一张「压缩后位置 → 原始位置」的映射表，让浏览器和错误监控平台能还原出真实代码。

最常见的误解是把它当成一个 `<script>` 标签来引入——它不是脚本，而是**通过特殊注释或响应头关联**的：

```javascript
// bundle.min.js 文件的最后一行会自动生成这样的注释
//# sourceMappingURL=bundle.min.js.map

// 也可以用响应头关联，适合把 map 放到 CDN 或内部服务器上
// SourceMap: /maps/bundle.min.js.map
```

生产环境的推荐做法是 **hidden-source-map**：

| 模式 | 产出 .map 文件 | 文件里带 `sourceMappingURL` | 适用场景 |
| --- | --- | --- | --- |
| `source-map` | 是 | 是 | 开发、预发布 |
| `hidden-source-map` | 是 | **否** | 生产：把 map 上传到错误监控平台，但不随包对外公开 |
| `nosources-source-map` | 是 | 是 | 需要定位行列号，但不想暴露源码内容 |
| `false` / `none` | 否 | 否 | 对体积和源码保密要求极高的场景 |

```javascript
// Vite：vite.config.js
export default {
    build: {
        sourcemap: 'hidden',   // 生成 .map 但不在产物里写注释
    },
};
```

如果生产站点把 `.map` 一起部署到了公网，任何人都能还原出你的完整源码（含注释、接口路径、内部逻辑），这是很常见的安全疏漏。正确姿势是把 map 上传到监控平台后从发布产物中移除。

## 36.4 高效排查的通用手法

工具之外，一些「土办法」在定位问题时往往更快：

```javascript
// 1. 二分定位：先注释掉一半逻辑，看问题还在不在，快速缩小范围

// 2. 用 JSON.stringify 展开对象，避免控制台只显示 [object Object]
console.log(JSON.stringify(bigObject, null, 2));

// 3. console.trace 直接打印调用链，比打断点更轻量
function suspicious() {
    console.trace('谁调用了我');
}

// 4. 控制台里的快捷变量：$0 是当前选中元素，$1 是上一个选中元素
// $0.textContent
// 选中某个节点后执行 copy($0.outerHTML) 可以直接复制到剪贴板

// 5. 临时监听某个函数的调用
// monitor(someFunction, 'args');      // 每次调用打印参数
// monitorEvents(document.body, 'click');

// 6. 用断言把「不该发生的情况」变成显式错误，而不是让人猜
function divide(a, b) {
    console.assert(b !== 0, '除数不能为 0', { a, b });
    return a / b;
}
```

另外两个顺序上的建议：**先复现再动手改**，能稳定复现的问题才谈得上验证修复；**先看报错堆栈的第一行和你自己的代码**，大部分问题不需要从框架源码看起。

最后别忘了 `debugger` 语句和 `console.log` 都是临时工具，提交代码前应清理掉，可以在 ESLint 中打开 `no-debugger` 规则来兜底。

---

## 本章小结

本章我们学习了调试工具：

1. **console**：log、warn、error、info、assert、group、count、time、timeLog、trace、table、dir，以及「打印对象看到的是引用」这个坑。
2. **断点调试**：`debugger` 语句、普通/条件断点、日志点、异常/DOM/事件监听断点、XHR 断点，以及 VS Code 的 launch.json 与 Node 的 `--inspect`。
3. **面板工具**：Network、Performance、Memory（快照对比与真正的泄漏模式）、source map（hidden-source-map 与源码泄漏风险）。
4. **通用手法**：二分定位、`JSON.stringify` 展开对象、`console.trace` 打印调用链、控制台快捷变量与 `monitor`，以及提交前清理调试代码。

调试是每个程序员必备的技能。学会使用这些工具，你就能快速定位并修复 bug。

下一章，我们要学习工具函数——让代码更优雅！
