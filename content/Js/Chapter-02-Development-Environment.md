+++
title = "第 2 章 开发环境"
weight = 20
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 2 章 开发环境

工欲善其事，必先利其器。在开始写 JavaScript 代码之前，咱们得先准备好趁手的家伙事儿。这一章，我们来搭建 JavaScript 的开发环境，让你从「新手村」正式出道。

## 2.1 浏览器开发工具

浏览器是 JavaScript 最重要的运行环境。而浏览器的**开发者工具**（DevTools），则是调试 JavaScript 的神器。

打开 DevTools 的方法（以 Chrome 为例）：

| 操作 | 快捷键 |
|------|--------|
| Windows / Linux | `F12` 或 `Ctrl + Shift + I` |
| macOS | `Cmd + Option + I` |
| 快捷方式 | `Ctrl + Shift + J`（直接打开 Console） |
| 右键菜单 | 右键 → 检查 |

### Chrome DevTools Console 面板

Console（控制台）面板是 JavaScript 开发者的「主战场」。你可以在这里：

- 执行任意 JavaScript 代码
- 查看 `console.log` 的输出
- 调试程序逻辑

```javascript
// 在 Console 中输入以下代码，体验一下吧！

console.log("普通日志");
console.warn("警告信息");
console.error("错误信息");
console.info("提示信息");

// 输出结果会显示不同颜色，方便区分
// 黑色：普通日志
// 黄色：警告
// 红色：错误
// 蓝色：提示
```

```javascript
// Console 还支持变量和表达式
let name = "JavaScript 爱好者";
let version = "ES2024";
console.log("正在学习 " + name + "，版本：" + version); // 正在学习 JavaScript 爱好者，版本：ES2024

// 更现代的方式：模板字符串
console.log(`正在学习 ${name}，版本：${version}`); // 正在学习 JavaScript 爱好者，版本：ES2024

// 直接写表达式
console.log(`1 + 1 = ${1 + 1}`); // 1 + 1 = 2

// 调用函数
function greet(user) {
    return "你好，" + user + "！";
}
console.log(greet("张三")); // 你好，张三！
```

### console.log / warn / error / info 的用法

`console` 对象不仅仅只有 `log`，它还有一整套日志级别的「组合拳」：

```javascript
// console.log - 普通信息
console.log("这是一条普通日志"); // 这是一条普通日志

// console.warn - 警告
// 浏览器会显示黄色图标和警告文字
console.warn("这是一个警告！程序还能跑，但有问题需要注意！"); // 这是一个警告！程序还能跑，但有问题需要注意！

// console.error - 错误
// 浏览器会显示红色图标和错误信息
console.error("这是一个错误！程序可能出问题了！"); // 这是一个错误！程序可能出问题了！

// console.info - 提示信息
// 效果跟 log 差不多，但会有一个蓝色图标
console.info("这是一个提示信息！"); // 这是一个提示信息！

// console.debug - 调试信息
// 默认不显示，需要在 Console 面板过滤
console.debug("这是调试信息"); // (debug) 这是调试信息
```

```javascript
// 高级技巧：console.log 的格式化输出
// %s - 字符串
// %d - 数字
// %o - 对象
// %c - CSS 样式

console.log("我叫 %s，年龄 %d 岁", "张三", 25);
// 我叫 张三，年龄 25 岁

const person = { name: "李四", age: 30 };
console.log("用户信息：%o", person);
// 用户信息：{name: "李四", age: 30}

console.log("%c红色大字", "color: red; font-size: 20px; font-weight: bold;");
// 显示红色大字
```

```javascript
// 实用技巧：console.table 表格化显示数组和对象
const users = [
    { name: "张三", age: 25, city: "北京" },
    { name: "李四", age: 30, city: "上海" },
    { name: "王五", age: 28, city: "广州" }
];

console.table(users);
// 会在 Console 中显示一个美观的表格
```

### alert / confirm / prompt 浏览器对话框

在 Console 出现之前，这些是 JavaScript 与用户交互的主要方式。虽然现在基本被「复古化」了，但了解它们还是很有必要的——毕竟面试题里经常出现。

#### alert - 警告框

弹出一个只带「确定」按钮的警告框。通常用于提示用户某些信息。

```javascript
alert("欢迎来到 JavaScript 世界！");

// 典型场景：表单提交前确认
function submitForm() {
    alert("表单已提交，感谢您的填写！");
}

// 注意：alert 会阻塞代码执行，直到用户点击「确定」
// 在用户点击之前，后面的代码不会执行
console.log("这段代码在 alert 之前执行"); // 这段代码在 alert 之前执行

alert("点击确定后，下面的代码才会执行");

console.log("alert 的阻塞解除了！"); // alert 的阻塞解除了！
```

#### confirm - 确认框

弹出一个有「确定」和「取消」两个按钮的对话框。根据用户点击返回 `true`（确定）或 `false`（取消）。

```javascript
const isConfirmed = confirm("确定要删除这个文件吗？");

if (isConfirmed) {
    console.log("用户点击了确定，删除文件..."); // 用户点击了确定，删除文件...
} else {
    console.log("用户点击了取消，放弃删除。"); // 用户点击了取消，放弃删除。
}
```

```javascript
// 实用场景：离开页面时确认
window.addEventListener("beforeunload", function(event) {
    const hasUnsavedChanges = true; // 假设有未保存的更改

    if (hasUnsavedChanges) {
        event.preventDefault();
        // 现代浏览器需要返回字符串才会弹出确认框
        event.returnValue = "您有未保存的更改，确定要离开吗？";
    }
});
```

#### prompt - 输入框

弹出一个可以输入文本的对话框。返回用户输入的内容（字符串），如果用户点击「取消」则返回 `null`。

```javascript
const name = prompt("请输入您的名字：");

if (name !== null) {
    console.log("您好，" + name + "！"); // 您好，[输入的名字]！
} else {
    console.log("用户取消了输入"); // 用户取消了输入
}
```

```javascript
// 带默认值的 prompt
const nickname = prompt("请输入您的昵称：", "匿名用户");

if (nickname !== null) {
    console.log("昵称：" + nickname); // 昵称：[输入的值] 或 "匿名用户"
} else {
    console.log("用户取消了输入"); // 用户取消了输入
}
```

```javascript
// 完整示例：简单的交互程序
function askUserName() {
    const name = prompt("您好！我叫什么名字？");

    if (name === null) {
        console.log("用户没有输入，算了...");
        return;
    }

    if (name.trim() === "") {
        alert("喂，总得说个名字吧！");
        askUserName(); // 重新问
        return;
    }

    if (name === "JavaScript") {
        alert("没错！答对了！你很了解我嘛！");
    } else {
        alert("我叫 JavaScript，不是 " + name + " 啦！");
    }
}

// 调用函数开始交互
// askUserName();
```

## 2.2 VS Code 配置

如果说浏览器是 JavaScript 的「战场」，那么 **VS Code**（Visual Studio Code）就是程序员的「瑞士军刀」。

VS Code 是微软出品的免费代码编辑器，轻量、快速、插件丰富，是目前最流行的前端开发工具。没有之一。

### 下载与安装

**下载地址**：`https://code.visualstudio.com/`

支持 Windows、macOS、Linux 三大平台。安装过程跟装普通软件一样简单，一路「下一步」即可。

```powershell
# Windows 用户也可以用 winget 安装
winget install Microsoft.VisualStudioCode

# macOS 用户可以用 Homebrew 安装
brew install --cask visual-studio-code

# Linux 用户可以用 snap 安装
sudo snap install --classic code
```

> 第一次打开 VS Code 时，你会看到一个欢迎界面。建议勾选「打开时显示欢迎指南」，熟悉一下基本操作。

### 必装插件清单

VS Code 本身已经很强大了，但加上插件，它就是无敌的。以下是 JavaScript 开发者的**必装插件清单**：

#### Prettier：代码格式化

**作用**：自动格式化代码，让代码保持统一的风格。告别「这个缩进是 Tab 还是空格」的世纪争论。

**安装**：在扩展面板搜索 `Prettier - Code formatter`，点击安装。

```javascript
// 格式化前（乱七八糟的代码）
const  name ="JavaScript";const  age =  25;
function  greet(){console.log("你好！")}

// 格式化后（整整齐齐）
const name = "JavaScript";
const age = 25;

function greet() {
    console.log("你好！");
}
```

```javascript
// Prettier 的配置（在 .prettierrc 文件中）
// 常见的配置选项：
// - semi: true           // 语句末尾加分号
// - singleQuote: true    // 使用单引号
// - tabWidth: 4          // Tab 宽度
// - trailingComma: "es5" // 保留 ES5 的尾随逗号
// - printWidth: 80       // 每行最大字符数

// 快捷键：Shift + Alt + F（Windows）或 Shift + Option + F（macOS）
```

#### Live Server：本地开发服务器

**作用**：启动一个本地服务器，实时刷新浏览器。当你修改代码时，浏览器会自动刷新，不用手动按 F5。

**安装**：搜索 `Live Server`，点击安装。

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Live Server 测试</title>
</head>
<body>
    <h1 id="title">你好！</h1>
    <button onclick="changeTitle()">点我改标题</button>

    <script>
        function changeTitle() {
            document.getElementById("title").textContent = "标题被我改了！";
        }
    </script>

    <!-- 保存后，浏览器自动刷新 -->
</body>
</html>
```

> **使用技巧**：安装 Live Server 后，在 HTML 文件上右键，选择「Open with Live Server」，浏览器就会自动打开并实时预览。修改代码后，按 `Ctrl + S` 保存，浏览器就会自动刷新。

#### JavaScript ES6 snippets：代码片段补全

**作用**：输入简短的缩写，自动补全完整的代码片段。比如输入 `cl`，按 Tab，就能补全 `console.log()`。

**安装**：搜索 `ES6 String HTML Snippets`，点击安装。

```javascript
// 常用代码片段
// cl  -> console.log();
cl("Hello"); // Hello

// fn  -> function name() { }
// fne -> function name() { return }

// req -> require('');
// im  -> import '' from '';

// an  -> async function name() { }
// ac  -> await async function name() { }

// oo  -> console.log() 带对象格式化
// 常用片段（具体以插件实际提供的为准）
```

#### Auto Rename Tag：自动配对标签修改

**作用**：修改 HTML 标签的开始标签时，结束标签会自动跟着修改。修改 JSX 标签同样有效。

```html
<!-- 修改 <div> 标签时，</div> 会自动跟着变 -->
<div>
    <p>内容</p>
</div>

<!-- 当你把开始标签改成 <section> 时，结束标签自动变成 </section> -->
<section>
    <p>内容</p>
</section>
```

#### Bracket Pair Colorizer：括号高亮着色

**作用**：给配对的括号加上不同的颜色，再也不用担心括号对不上。

```javascript
// 不同层级的括号显示不同颜色
function example() {
    if ([1, 2, 3].includes(4)) {
        console.log("找到4了！");
    }
}

// 以前：括号全是黑色，分不清哪对哪
// 现在：每个层级都有不同颜色，一目了然
```

> **注意**：从 VS Code 1.60 开始，**括号着色功能已经内置**了，不需要额外安装插件！你可以通过设置 `editor.bracketPairColorization.enabled: true` 来开启。

### 保存自动格式化配置

让 VS Code 在保存文件时自动格式化代码：

1. 打开设置（`Ctrl + ,` 或 `Cmd + ,`）
2. 搜索 `Format On Save`
3. 勾选 `Editor: Format On Save`

```json
// 或者直接在 settings.json 中配置
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[javascriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[css]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
}
```

```javascript
// settings.json 常用配置项说明
// editor.formatOnSave: true       - 保存时自动格式化
// editor.defaultFormatter          - 默认格式化工具
// editor.tabSize: 4               - Tab 宽度
// editor.insertSpaces: true       - 用空格代替 Tab
// files.autoSave: "afterDelay"    - 自动保存（延迟后）
// editor.minimap.enabled: false    - 关闭代码缩略图（省屏幕空间）
```

## 2.3 常见错误类型

写代码嘛，出错是常态。重要的是——**知道什么错了，为什么错，怎么改**。这一节，我们来认识 JavaScript 中最常见的几种错误类型。

### SyntaxError：语法错误

**什么是 SyntaxError？**

SyntaxError 就是「语法错误」——你说的话 JavaScript 听不懂。这通常是因为代码写错了，比如括号没配对、少了分号、拼错了关键字等。

```javascript
// 错误示例 1：括号没配对
function greet() {
    console.log("你好");
// }  ← 少了右花括号！

// 运行结果：
// SyntaxError: Unexpected end of input
// 翻译：啥玩意儿？我还没说完呢，你怎么就停了？
```

```javascript
// 错误示例 2：关键字拼写错误
const message = "Hello";
conslo.log(message); // ← console 拼错了！

// 运行结果：
// ReferenceError: conslo is not defined
// 翻译：conslo 是谁？我不认识！
```

```javascript
// 错误示例 3：引号没配对
const str = '单引号没闭合;

// 运行结果：
// SyntaxError: Invalid or unexpected token
// 翻译：这是什么鬼符号？我看不懂！
```

```javascript
// 正确示例：括号配对
function greet(name) {
    if (name === undefined) {
        console.log("你好，陌生人！");
    } else {
        console.log("你好，" + name + "！");
    }
    return true; // 所有括号都乖乖闭上了
}

greet("张三"); // 你好，张三！
```

> **语法错误的特点**：代码根本跑不起来，JavaScript 在解析阶段就会报错。

### ReferenceError：引用错误

**什么是 ReferenceError？**

ReferenceError 就是「引用错误」——你引用了一个不存在的变量。就像你在通讯录里找人，结果发现这个人根本不在通讯录里。

```javascript
// 错误示例 1：变量未声明就使用
console.log(undeclaredVariable);

// 运行结果：
// ReferenceError: undeclaredVariable is not defined
// 翻译：这个变量我压根没见过，你从哪儿弄来的？
```

```javascript
// 错误示例 2：变量名拼写错误（大小写敏感）
let userName = "张三";
console.log(username); // ← u 和 n 的位置反了！

// 运行结果：
// ReferenceError: username is not defined
// 翻译：username 和 userName 是两个不同的人！
```

```javascript
// 错误示例 3：使用 let/const 声明前访问
console.log(age); // 在声明前访问
let age = 25;

// 运行结果：
// ReferenceError: Cannot access 'age' before initialization
// 翻译：我知道你要用 age，但你现在还不能用它，它还在准备中！
```

```javascript
// 正确示例：先声明后使用
let age = 25;
console.log(age); // 25

const PI = 3.14159;
console.log(PI); // 3.14159

// 在函数作用域内声明
function calculate() {
    let radius = 10;
    console.log("半径 =", radius); // 半径 = 10
}
calculate();
```

```javascript
// 实用技巧：使用 typeof 安全检查未声明的变量
// 注意：这招只对 var 有效，let/const 会抛出 ReferenceError
// typeof undeclaredVariable 的值是 "undefined"（不会报错）

// 推荐做法：用 try-catch 捕获
try {
    console.log(maybeExists);
} catch (error) {
    console.log("变量不存在:", error.message); // 变量不存在: maybeExists is not defined
}
```

### TypeError：类型错误

**什么是 TypeError？**

TypeError 就是「类型错误」——你对这个数据类型的操作，它不认。比如你想用数字调用 `split()` 方法，或者对 undefined 调用函数。

```javascript
// 错误示例 1：调用 undefined 的函数属性
const obj = {
    name: "张三",
    // greet 方法没有定义
};
obj.greet(); // 尝试调用 undefined 的 greet

// 运行结果：
// TypeError: obj.greet is not a function
// 翻译：obj 没有 greet 这个方法，你想调的是啥？
```

```javascript
// 错误示例 2：数字调用字符串方法
const num = 12345;
num.split(""); // 数字没有 split 方法！

// 运行结果：
// TypeError: num.split is not a function
// 翻译：数字是数字，字符串是字符串，别混为一谈！
```

```javascript
// 错误示例 3：null 调用属性
const person = null;
console.log(person.name);

// 运行结果：
// TypeError: Cannot read property 'name' of null
// 翻译：person 是 null（空），你还想让它有 name 属性？
```

```javascript
// 错误示例 4：给常量重新赋值
const PI = 3.14159;
PI = 3.14; // const 不能重新赋值！

// 运行结果：
// TypeError: Assignment to constant variable
// 翻译：PI 已经是 3.14159 了，你别想改它的值！
```

```javascript
// 正确示例：正确的类型操作
// 字符串操作字符串
const str = "Hello";
console.log(str.split("")); // ["H", "e", "l", "l", "o"]

// 数字先转字符串再操作
const num = 12345;
console.log(num.toString().split("")); // ["1", "2", "3", "4", "5"]

// 对象有方法才能调用
const person = {
    name: "张三",
    greet: function() {
        return "你好，我是 " + this.name;
    }
};
console.log(person.greet()); // 你好，我是 张三

// 用 let 而不是 const 声明可以重新赋值的变量
let counter = 0;
counter = counter + 1;
console.log(counter); // 1
```

```javascript
// 实用技巧：使用可选链避免 TypeError
const obj = {
    name: "张三"
    // 没有 age 属性
};

// 以前：这样会报错
// console.log(obj.age.toString()); // TypeError: Cannot read property 'toString' of undefined

// 现在：使用可选链 ?. 安全访问
console.log(obj.age?.toString()); // undefined（不会报错）
console.log(obj.name?.toString()); // 张三
```

### RangeError：范围错误

**什么是 RangeError？**

RangeError 就是「范围错误」——你给的值超出了允许的范围。比如数组长度为负数，或者递归调用太深导致栈溢出。

```javascript
// 错误示例 1：数组长度设为负数
const arr = new Array(-5);

// 运行结果：
// RangeError: Invalid array length
// 翻译：数组长度不能是负数啊，大兄弟！
```

```javascript
// 错误示例 2：toFixed/toPrecision 参数超出范围
const num = 123.456;
num.toFixed(101); // toFixed 参数范围是 0-100

// 运行结果：
// RangeError: toFixed() digits argument must be between 0 and 100
// 翻译：精度最多 100 位，你要求也太高了吧！
```

```javascript
// 错误示例 3：递归调用栈溢出
function recursive() {
    console.log("我还能跑！");
    recursive(); // 无限递归，栈会爆炸
}
// 调用
// recursive();

// 运行结果：
// RangeError: Maximum call stack size exceeded
// 翻译：递归太深了！栈都装不下了！你这是要把计算机累死吗？
```

```javascript
// 正确示例：合理的数组长度和递归
const arr = new Array(5);
console.log(arr.length); // 5

const num = 123.456;
console.log(num.toFixed(2)); // "123.46"
console.log(num.toPrecision(4)); // "123.5"

// 递归要有终止条件
function countdown(n) {
    if (n <= 0) {
        console.log("发射！");
        return;
    }
    console.log(n + "...");
    countdown(n - 1); // 每次减 1，总会到 0
}

countdown(5);
// 5...
// 4...
// 3...
// 2...
// 1...
// 发射！
```

```javascript
// 实用技巧：用递归实现阶乘（注意终止条件）
function factorial(n) {
    // 参数校验
    if (typeof n !== "number" || n < 0 || !Number.isInteger(n)) {
        throw new Error("请传入非负整数！");
    }

    // 终止条件
    if (n === 0 || n === 1) {
        return 1;
    }

    // 递归调用
    return n * factorial(n - 1);
}

console.log(factorial(5));  // 120
console.log(factorial(0)); // 1
// console.log(factorial(-1)); // Error: 请传入非负整数！
```

---

## 本章小结

本章我们完成了开发环境的搭建：

1. **浏览器 DevTools**：Chrome DevTools 是 JavaScript 调试的神器，Console 面板可以执行代码、查看日志。`console.log/warn/error/info` 分别用于不同级别的日志输出。`alert/confirm/prompt` 是老派的交互方式，了解一下就行，生产环境别用。

2. **VS Code 配置**：微软出品的免费编辑器，搭配 Prettier（代码格式化）、Live Server（本地热重载）、ES6 snippets（代码补全）、Auto Rename Tag（自动改标签）等插件，开发效率飞起。

3. **常见错误类型**：
   - **SyntaxError**：代码写错了，语法不对
   - **ReferenceError**：引用了不存在的变量
   - **TypeError**：对错误的数据类型做了操作
   - **RangeError**：值超出了允许的范围

遇到报错别慌！仔细看错误信息，它会告诉你哪里出了问题。善用搜索引擎和 AI 助手，没有解决不了的 bug——除非你遇到的是 IE6 的兼容性问题，那只能自求多福了。

下一章，我们将学习 JavaScript 的根基——变量与数据类型。这可是重头戏，准备好你的大脑，我们继续冲！


```

> **重要提醒：**
>
> 这三个对话框都是**同步阻塞**的——它们会暂停代码执行，直到用户做出响应。在现代 Web 开发中，**强烈不建议在生产环境使用它们**，因为：
>
> 1. 它们会阻塞浏览器主线程，影响用户体验
> 2. 样式无法自定义，丑
> 3. 在某些浏览器中，关掉对话框会直接抛出错误
>
> 现在的做法是：用 HTML/CSS/JavaScript 自定义模态框（Modal）。但作为学习工具和调试手段，了解这三个方法是很有必要的！
