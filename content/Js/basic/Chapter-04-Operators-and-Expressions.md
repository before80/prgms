+++
title = "第 4 章 运算符与表达式"
weight = 40
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 4 章 运算符与表达式

如果说变量是程序的「名词」，那运算符就是程序的「动词」——它们让数据动起来。JavaScript 的运算符种类繁多，从最基础的加减乘除，到高大上的可选链和空值合并运算符，这一章统统给你安排上。

## 4.1 算术运算符

算术运算符是最基础的运算符，我们从小学数学就开始学了。

### 加减乘除取模：`+ - * / %`

```javascript
// 基本算术运算
console.log(10 + 5);  // 15（加法）
console.log(10 - 5);  // 5（减法）
console.log(10 * 5);  // 50（乘法）
console.log(10 / 5);  // 2（除法）
console.log(10 % 3);  // 1（取模/取余）
console.log(10 % 4);  // 2

// 除法有浮点精度问题
console.log(0.1 + 0.2); // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3); // false（别用 === 比较浮点数！）

// 整数除法（向下取整）
console.log(Math.floor(10 / 3)); // 3
console.log((10 / 3) | 0);       // 3（位运算取整，快但不直观）
```

```javascript
// 取模运算的应用
// 判断奇偶
console.log(7 % 2);  // 1（奇数）
console.log(8 % 2);  // 0（偶数）

// 循环计数
for (let i = 0; i < 10; i++) {
    if (i % 3 === 0) {
        console.log(i + "是3的倍数");
    }
}

// 获取数字的某位
const num = 12345;
// 获取个位
console.log(num % 10); // 5
// 获取十位
console.log(Math.floor(num / 10) % 10); // 4

// 数字范围限制（循环数组）
const arr = [1, 2, 3, 4, 5];
let index = 0;
function getNextIndex() {
    index = (index + 1) % arr.length; // 0,1,2,3,4,0,1,2...
    return index;
}
```

### 赋值运算符：`= += -= *= /= %=`

```javascript
// 基本赋值
let x = 10;
console.log(x); // 10

// 复合赋值运算符
let a = 10;
a += 5;  // a = a + 5
console.log(a); // 15

a -= 3;  // a = a - 3
console.log(a); // 12

a *= 2;  // a = a * 2
console.log(a); // 24

a /= 4;  // a = a / 4
console.log(a); // 6

a %= 4;  // a = a % 4
console.log(a); // 2
```

```javascript
// 字符串拼接赋值
let str = "Hello";
str += ", "; // str = str + ", "
str += "World!";
console.log(str); // Hello, World!

// 实际应用：构建长字符串
let html = "";
html += "<div>";
html += "<h1>标题</h1>";
html += "<p>内容</p>";
html += "</div>";
console.log(html); // <div><h1>标题</h1><p>内容</p></div>
```

### 自增自减：`++a` vs `a++`

`++` 和 `--` 是两个极端——看起来差不多，效果却不同。这是面试常考题，我们来彻底搞清楚。

```javascript
// 前置++（++a）：先加1，再返回值
let a = 5;
console.log(++a); // 6（先加到 6，再输出）
console.log(a);  // 6

// 后置++（a++）：先返回值，再加1
let b = 5;
console.log(b++); // 5（先输出 5，再加到 6）
console.log(b);  // 6

// 实际例子
let count = 0;
console.log(count++); // 0（输出0，count变成1）
console.log(count++); // 1（输出1，count变成2）
console.log(count);   // 2（最终是2）
```

```javascript
// 自减同理
let num = 10;
console.log(--num); // 9（先减到9，再输出）
console.log(num--); // 9（先输出9，再减到8）
console.log(num);   // 8
```

```javascript
// 实际应用：数组索引
const arr = ["a", "b", "c"];
let i = 0;
console.log(arr[i++]); // arr[0] -> "a"，然后 i 变成 1
console.log(arr[i++]); // arr[1] -> "b"，然后 i 变成 2
console.log(arr[i++]); // arr[2] -> "c"，然后 i 变成 3

// 另一种写法
let j = 0;
console.log(arr[++j]); // 先 j 变成 1，再 arr[1] -> "b"
```

```javascript
// 陷阱：不要在表达式中混用自增和其他操作
let i = 1;
let result = i++ + ++i + i++;
// i++: 返回1，i变成2
// ++i: i变成3，返回3
// i++: 返回3，i变成4
console.log(result); // 1 + 3 + 3 = 7
console.log(i);      // 4
// 这种代码太混乱了，不建议这么写！
```

## 4.2 比较运算符

比较运算符返回布尔值，是条件判断的基础。

### 大小比较：`> < >= <=`

```javascript
// 基本比较
console.log(5 > 3);   // true
console.log(5 < 3);   // false
console.log(5 >= 5);   // true
console.log(3 <= 2);  // false

// 字符串比较（按 Unicode 码点）
console.log("a" > "b");    // false（a=97, b=98）
console.log("apple" < "banana"); // true（按字母顺序）
console.log("Hello" > "hello"); // false（H=72, h=104）

// Unicode 排序问题
console.log("字母" > "数字"); // true（"字"的 Unicode 码点大于"数"）
console.log("a" > "A");       // true（小写字母 Unicode 值大于大写）
```

```javascript
// 数字字符串的比较（会自动转数字）
console.log("10" > "2");   // false！（字符串比较，"1" < "2"）
console.log(10 > 2);      // true（数字比较）

// 实际建议：比较数字字符串时先转数字
console.log(Number("10") > Number("2")); // true
```

### 相等比较：`== != === !==`

这是 JavaScript 最容易出错的地方。**记住：永远用 `===` 和 `!==`。**

```javascript
// ==（宽松相等）：会进行类型转换
console.log(1 == "1");         // true
console.log(true == 1);        // true
console.log(null == undefined); // true
console.log("" == 0);          // true
console.log(false == "");     // true

// ===（严格相等）：不进行类型转换
console.log(1 === "1");         // false
console.log(true === 1);       // false
console.log(null === undefined); // false
console.log("" === 0);         // false
console.log(false === "");    // false
```

```javascript
// != vs !==
console.log(1 != "1");   // false（宽松不相等）
console.log(1 !== "1"); // true（严格不相等）

// 建议：永远用 !== 而非 !=

// 特殊情况：NaN
console.log(NaN != NaN);   // true（NaN 和谁都不等）
console.log(NaN !== NaN); // true
// 判断 NaN 的正确方式：Number.isNaN() 或 Object.is()
// ES6 引入的 Number.isNaN() 不会进行类型转换，只有当参数本身是 NaN 且类型为 Number 时才返回 true。
Number.isNaN(NaN);       // true
Number.isNaN("abc");     // false
Number.isNaN(undefined); // false
Number.isNaN({});        // false
// Object.is() 是 ES6 新增的严格相等比较方法，它修复了 === 的一些特殊行为，
// 其中包括将 NaN 与 NaN 视为相等。
Object.is(NaN, NaN); // true
Object.is(NaN, 0/0); // true（0/0 也是 NaN）
```

```javascript
// 对象的比较
const obj1 = { a: 1 };
const obj2 = { a: 1 };
console.log(obj1 == obj2);  // false（两个不同对象，地址不同）
console.log(obj1 === obj2); // false

const obj3 = obj1;
console.log(obj1 == obj3);  // true（同一个引用）
console.log(obj1 === obj3); // true
```

```javascript
// 数组的比较
const arr1 = [1, 2, 3];
const arr2 = [1, 2, 3];
console.log(arr1 == arr2);  // false（不同数组）
console.log(arr1 === arr2); // false

// 比较数组内容：用 JSON.stringify 或 every
console.log(JSON.stringify(arr1) === JSON.stringify(arr2)); // true
console.log(arr1.every((item, i) => item === arr2[i]));   // true
```

### `==` 与 `===` 的区别

| 场景 | == | === |
|------|-----|-----|
| `1` vs `"1"` | true | false |
| `true` vs `1` | true | false |
| `null` vs `undefined` | true | false |
| `[]` vs `""` | true | false |
| `[]` vs `false` | true | false |
| `{}` vs `"[object Object]"` | true | false |

```javascript
// 安全建议
// 1. 永远用 === 和 !==
// 2. 只有在检查 null/undefined 时可以用 == null（简写形式）
//    if (value == null) 等价于 if (value === null || value === undefined)
function test(value) {
    if (value == null) {
        console.log("值是 null 或 undefined");
    }
}

test(null);      // 执行
test(undefined); // 执行
test(0);         // 不执行
test("");        // 不执行
test(false);     // 不执行
```

## 4.3 逻辑运算符

逻辑运算符用于组合多个条件，是程序逻辑的核心。

### &&（与） ||（或） !（非）

```javascript
// &&（与）：两边都为 true 才为 true
console.log(true && true);   // true
console.log(true && false); // false
console.log(false && true);  // false
console.log(false && false); // false

// ||（或）：任一边为 true 就为 true
console.log(true || true);   // true
console.log(true || false);  // true
console.log(false || true);  // true
console.log(false || false); // false

// !（非）：取反
console.log(!true);  // false
console.log(!false); // true
console.log(!!true); // true（双重取反变正）
```

```javascript
// 实际应用：条件组合
const age = 25;
const hasTicket = true;

// 必须同时满足
if (age >= 18 && hasTicket) {
    console.log("允许入场"); // 允许入场
}

// 满足任一即可
if (age < 18 || !hasTicket) {
    console.log("禁止入场");
} else {
    console.log("允许入场"); // 执行
}

// 取反
if (!hasTicket) {
    console.log("请购票");
}
```

### 短路求值

这是逻辑运算符最重要的特性：**只计算必要的部分**。

```javascript
// && 短路：如果左边是 false，不再计算右边
console.log(false && console.log("右边不会执行")); // false，不打印
console.log(true && console.log("右边会执行"));   // 打印"右边会执行"

const isLoggedIn = false;
isLoggedIn && console.log("欢迎回来"); // 不打印，因为 isLoggedIn 是 false
```

```javascript
// || 短路：如果左边是 true，不再计算右边
console.log(true || console.log("右边不会执行")); // true，不打印
console.log(false || console.log("右边会执行")); // 打印"右边会执行"

const defaultValue = null;
const value = defaultValue || "默认值";
console.log(value); // "默认值"
```

```javascript
// 短路求值的实用技巧

// 1. 设置默认值
const config = { timeout: 0 };
const timeout = config.timeout || 3000; // 0 被误判为 false！
console.log(timeout); // 3000（错误！timeout 应该是 0）

// 解决方案：用 ?? 空值合并运算符（ES2020）
const timeout2 = config.timeout ?? 3000;
console.log(timeout2); // 0（正确！）

// 2. 条件执行
isAdmin && showAdminPanel(); // isAdmin 为 true 时才执行
user || (user = defaultUser); // user 为 falsy 时才赋值

// 3. 链式调用
const user = {
    profile: {
        name: "张三"
    }
};
// 以前：if (user && user.profile && user.profile.name)
const name = user && user.profile && user.profile.name;
console.log(name); // "张三"

// 现在：可选链 ?.（ES2020）
const name2 = user?.profile?.name;
console.log(name2); // "张三"
```

### 返回值特性：返回的是值不是布尔

逻辑运算符返回的不一定是 `true` 或 `false`，而是**实际参与运算的值**。

```javascript
// && 返回最后一个求值的值，或第一个 falsy 值
console.log(true && "hello");     // "hello"
console.log(false && "hello");    // false
console.log("a" && "b" && "c");   // "c"（都是 truthy，返回最后一个）
console.log("a" && null && "c");  // null（遇到 falsy 就返回）

// || 返回第一个 truthy 值，或最后一个值
console.log(false || "hello");   // "hello"
console.log(true || "hello");     // true
console.log("a" || "b" || "c");  // "a"（第一个 truthy）
console.log(false || null || "c"); // "c"（都是 falsy，返回最后一个）
```

```javascript
// 实用技巧：提取值或默认值

// 1. 提取第一个 truthy 值
const options = {
    theme: null,
    language: "zh-CN",
    timeout: 0
};

// 提取第一个 truthy 的配置
const selectedTheme = options.theme || "dark";
const selectedLanguage = options.language || "en";
const selectedTimeout = options.timeout || 5000; // 0 会被误判！

// 2. 复杂的条件赋值
const user = {
    name: "张三",
    role: null
};

const displayName = user.name || user.role || "匿名用户";
console.log(displayName); // "张三"
```

```javascript
// 注意：0、""、null、undefined、NaN 都是 falsy
const values = [0, "", null, undefined, NaN, false, "hello", 42];

for (const val of values) {
    const result = val && "truthy";
    console.log(`${val} && "truthy" =`, result);
}
// 0 && "truthy" = 0
// "" && "truthy" = ""
// null && "truthy" = null
// undefined && "truthy" = undefined
// NaN && "truthy" = NaN
// false && "truthy" = false
// "hello" && "truthy" = "truthy"
// 42 && "truthy" = "truthy"
```

## 4.4 其他运算符

除了算术、比较、逻辑运算符，JavaScript 还有一些特殊而强大的运算符。

### 三元运算符：condition ? expr1 : expr2

三元运算符是 `if...else` 的简写形式。

```javascript
// 基本语法
const age = 20;
const status = age >= 18 ? "成年人" : "未成年";
console.log(status); // "成年人"

// 嵌套三元运算符（不推荐，太难读）
const score = 85;
const grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 60 ? "C" : "D";
console.log(grade); // "B"

// 推荐写法：用 if...else 或提前计算
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else if (score >= 60) {
    grade = "C";
} else {
    grade = "D";
}
```

```javascript
// 实际应用

// 1. 条件赋值
const isVip = true;
const discount = isVip ? 0.8 : 1.0;
console.log("原价100，折后", 100 * discount); // 折后 80

// 2. 条件返回值
function getWelcomeMessage(user) {
    return user.isLoggedIn
        ? `欢迎回来，${user.name}！`
        : "请先登录！";
}

console.log(getWelcomeMessage({ isLoggedIn: true, name: "张三" })); // 欢迎回来，张三！
console.log(getWelcomeMessage({ isLoggedIn: false })); // 请先登录！

// 3. 条件执行
const shouldShowButton = true;
shouldShowButton && console.log("显示按钮"); // 显示按钮
```

### 可选链操作符 ?.（ES2020+）：安全访问深层属性

这是 ES2020 最重要的新特性之一，终于告别了「地狱般的嵌套检查」。

```javascript
// 以前：层层检查
const user = {
    profile: {
        name: "张三"
    }
};

// 如果没有 profile，下面的代码会报错！
// const name = user.profile.name; // 安全

const emptyUser = {};
// const name = emptyUser.profile.name; // TypeError!

// 以前要这样写：
const name = (emptyUser.profile && emptyUser.profile.name) || "未知";
console.log(name); // "未知"
```

```javascript
// 现在：用可选链
const user1 = {
    profile: {
        name: "张三"
    }
};

const user2 = {};

console.log(user1?.profile?.name); // "张三"
console.log(user2?.profile?.name); // undefined（不报错！）

// 还可以用于方法调用
const obj = {
    fn: function() {
        return "Hello!";
    }
};

console.log(obj?.fn?.()); // "Hello!"
console.log(obj?.say?.()); // undefined（方法不存在，不报错）
```

```javascript
// 可选链的各种用法

// 属性访问
obj?.prop
obj?.["prop"]

// 方法调用
obj?.method()
obj?.method?.()

// 数组访问
arr?.[0]
arr?.[index]

// 结合空值合并
const user = {};
const name = user?.profile?.name ?? "匿名";
console.log(name); // "匿名"
```

```javascript
// 实际应用场景

// 1. API 响应数据
const apiResponse = {
    data: {
        user: {
            name: "张三",
            address: {
                city: "北京"
            }
        }
    }
};

const city = apiResponse?.data?.user?.address?.city ?? "未知";
console.log(city); // "北京"

// 2. DOM 操作
const title = document.querySelector(".title")?.textContent;
console.log(title); // 如果元素不存在，返回 undefined 而不是报错

// 3. 函数参数处理
function greet(user) {
    const name = user?.name ?? "陌生人";
    console.log("你好，" + name + "！");
}

greet({ name: "张三" }); // 你好，张三！
greet(null);             // 你好，陌生人！
greet(undefined);        // 你好，陌生人！
```

### 空值合并运算符 ??（ES2020+）：区分 undefined 和 null

`??` 是 ES2020 引入的，用于处理「值为 null 或 undefined」的情况，但不处理其他 falsy 值（如 `0`、`""`）。

```javascript
// || vs ??
const value1 = 0;
const value2 = "";
const value3 = false;

console.log(value1 || "默认值"); // "默认值"（0 被当作 falsy）
console.log(value1 ?? "默认值");  // 0（0 是有效值！）

console.log(value2 || "默认值"); // "默认值"（空字符串被当作 falsy）
console.log(value2 ?? "默认值");  // ""（空字符串是有效值！）

console.log(value3 || "默认值"); // "默认值"（false 被当作 falsy）
console.log(value3 ?? "默认值");  // false（false 是有效值！）
```

```javascript
// 实际应用：配置值

// 以前的做法：用 || 但有 bug
const config = {
    timeout: 0,
    retries: 5,
    apiUrl: "https://api.example.com"
};

const timeout = config.timeout || 3000; // 错误！0 被替换成 3000
const retries = config.retries || 3;    // 正确
const url = config.apiUrl || "default"; // 正确

// 现在：用 ?? 精确处理 null/undefined
const timeout2 = config.timeout ?? 3000; // 正确！0 保留
const retries2 = config.retries ?? 3;    // 正确
const url2 = config.apiUrl ?? "default"; // 正确
```

```javascript
// 结合可选链使用
const user = {
    settings: {
        theme: "dark"
    }
};

const theme = user?.settings?.theme ?? "light";
console.log(theme); // "dark"

const user2 = {};
const theme2 = user2?.settings?.theme ?? "light";
console.log(theme2); // "light"
```

### 逻辑赋值运算符：`||=  &&= ??=`（ES2021+）

ES2021 引入了逻辑赋值运算符，将逻辑运算和赋值合二为一。

```javascript
// ||= 或等于
let a = false;
a ||= "hello";
console.log(a); // "hello"

let b = "world";
b ||= "hello";
console.log(b); // "world"（保持原值）
```

```javascript
// &&= 且等于
let c = true;
c &&= "hello";
console.log(c); // "hello"

let d = false;
d &&= "hello";
console.log(d); // false（保持原值）
```

```javascript
// ??= 空值赋值
let e = null;
e ??= "default";
console.log(e); // "default"

let f = 0;
f ??= "default";
console.log(f); // 0（0 不是 null/undefined，保持原值）
```

```javascript
// 实际应用

// 1. 合并配置
const options = { timeout: null };
options.timeout ??= 3000;
console.log(options.timeout); // 3000

// 2. 初始化对象属性
const state = { count: 0 };
state.count ||= 10; // count 是 0，0 是 falsy，会被替换！注意！
console.log(state.count); // 10（可能不是你想要的）

state.count ??= 10; // count 是 0，0 不是 null/undefined，保持原值
console.log(state.count); // 0
```

### 运算符优先级

运算符优先级决定了表达式的计算顺序。

```javascript
// 优先级从高到低：括号 > 一元 > 乘除 > 加减 > 比较 > 相等 > 逻辑与 > 逻辑或

// 相当于加了隐含括号
console.log(2 + 3 * 4);       // 14（先算乘法）
console.log((2 + 3) * 4);     // 20（括号优先）

console.log(!true || true);   // true（!优先级最高）
console.log(!(true || true)); // false

console.log(2 + 3 === 5);     // true（+ 先算）
console.log(2 + 3 === 6);     // false
```

```javascript
// 建议：不确定优先级时，加括号
const result = ((a + b) * c) && (d || e);
const name = (user && user.profile && user.profile.name) || "匿名";

// 常见优先级（从高到低）
// 1. () 括号
// 2. 单目运算符 ! ++ -- typeof
// 3. 乘法除法 * / %
// 4. 加法减法 + -
// 5. 比较 > < >= <=
// 6. 相等 == != === !==
// 7. 逻辑与 &&
// 8. 逻辑或 ||
// 9. 三元 ? :
// 10. 赋值 = += -= *= /= %=
```

### 位运算符：`& | ^ ~ << >> >>>`（了解）

位运算符直接操作数字的二进制位。在现代 JavaScript 中，位运算符的实用场景不多，但了解它们能帮助你理解计算机底层。

```javascript
// & 按位与
console.log(5 & 3); // 1
// 5 = 0101
// 3 = 0011
// 5 & 3 = 0001 = 1

// | 按位或
console.log(5 | 3); // 7
// 5 = 0101
// 3 = 0011
// 5 | 3 = 0111 = 7

// ^ 按位异或（相同为0，不同为1）
console.log(5 ^ 3); // 6
// 5 = 0101
// 3 = 0011
// 5 ^ 3 = 0110 = 6

// ~ 按位取反
console.log(~5); // -6
// ~x = -(x + 1)

// << 左移
console.log(5 << 1); // 10（乘以2）
// 5 = 0101
// 5 << 1 = 1010 = 10

// >> 右移
console.log(5 >> 1); // 2（除以2，向下取整）
// 5 = 0101
// 5 >> 1 = 0010 = 2

// >>> 无符号右移
console.log(-5 >>> 0); // 巨大的正数（用于获取有符号整数的无符号值）
```

```javascript
// 位运算的实用技巧

// 1. 判断奇偶（比 % 快）
const isOdd = (num & 1) === 1;
console.log(isOdd); // true
console.log((5 & 1) === 1); // true（奇数）
console.log((4 & 1) === 1); // false（偶数）

// 2. 快速乘除2
const num = 8;
console.log(num << 1); // 16（乘以2）
console.log(num >> 1); // 4（除以2）

// 3. 取整（比 Math.floor 快）
console.log((3.7 | 0));  // 3
console.log((3.7 >> 0));  // 3
console.log((3.7 << 0));  // 3
// 原理：位运算会把浮点数转成整数

// 4. 交换两个数（不用临时变量）
let x = 5, y = 3;
x = x ^ y;
y = x ^ y;
x = x ^ y;
console.log(x, y); // 3, 5
```

### in 运算符：检查属性是否存在

`in` 运算符用于检查对象是否包含某个属性。

```javascript
// 基本用法
const person = {
    name: "张三",
    age: 25
};

console.log("name" in person);   // true
console.log("age" in person);   // true
console.log("email" in person); // false
console.log("toString" in person); // true（原型链上的属性也会返回 true）
```

```javascript
// in vs hasOwnProperty
const obj = { a: 1 };
console.log("a" in obj);                    // true
console.log("hasOwnProperty" in obj);        // true（在原型链上）
console.log(obj.hasOwnProperty("a"));       // true
console.log(obj.hasOwnProperty("hasOwnProperty")); // false

// ES2022+ 推荐用 Object.hasOwn()
console.log(Object.hasOwn(obj, "a"));       // true
console.log(Object.hasOwn(obj, "hasOwnProperty")); // false
```

```javascript
// 实际应用：检查数组索引
const arr = ["a", "b", "c"];
console.log(0 in arr);  // true
console.log(3 in arr);  // false（索引3不存在）
console.log("includes" in arr); // true（数组方法在原型链上）

// 检查方法是否存在
const obj = {
    greet: function() {
        console.log("你好！");
    }
};

if ("greet" in obj) {
    obj.greet(); // "你好！"
}
```

### instanceof：检查原型链

`instanceof` 用于检查对象是否是某个构造函数的实例。

```javascript
// 基本用法
const arr = [1, 2, 3];
console.log(arr instanceof Array);    // true
console.log(arr instanceof Object);   // true（Array 继承自 Object）
console.log(arr instanceof RegExp);   // false

const date = new Date();
console.log(date instanceof Date);     // true
console.log(date instanceof Object);   // true

const obj = {};
console.log(obj instanceof Object);    // true
console.log({} instanceof Object);     // true
```

```javascript
// 自定义类的实例检查
class Person {
    constructor(name) {
        this.name = name;
    }
}

class Student extends Person {
    constructor(name, grade) {
        super(name);
        this.grade = grade;
    }
}

const student = new Student("张三", "三年级");
console.log(student instanceof Student); // true
console.log(student instanceof Person);   // true（继承链）
console.log(student instanceof Object);   // true

const person = new Person("李四");
console.log(person instanceof Person);   // true
console.log(person instanceof Student);  // false
```

```javascript
// instanceof 的局限性
// 1. 跨 iframe 的对象（不同全局环境，构造函数不同）
// 2. 基本类型不是对象
console.log("hello" instanceof String); // false
console.log(42 instanceof Number);     // false
console.log(true instanceof Boolean);   // false

// 3. 解决方案：用 Object.prototype.toString
console.log(Object.prototype.toString.call("hello")); // "[object String]"
console.log(Object.prototype.toString.call(42));     // "[object Number]"
console.log(Object.prototype.toString.call(true));    // "[object Boolean]"
console.log(Object.prototype.toString.call([]));      // "[object Array]"
```

---

## 本章小结

本章我们全面学习了 JavaScript 的运算符与表达式：

1. **算术运算符**：`+ - * / %` 以及 `+= -= *= /= %=`。自增自减 `++a` 和 `a++` 有区别——前者先加后用，后者先用后加。

2. **比较运算符**：`> < >= <=` 用于大小比较，`== != === !==` 用于相等比较。**永远用 `===` 和 `!==`！**

3. **逻辑运算符**：`&&`、`||`、`!`。逻辑运算符有「短路求值」特性，且返回的是值而非布尔。

4. **三元运算符**：`condition ? expr1 : expr2`，是 `if...else` 的简写，适合简单条件。

5. **可选链 `?.`**：安全访问深层属性，避免「地狱般的嵌套检查」。

6. **空值合并 `??`**：只在值为 `null` 或 `undefined` 时才使用默认值，不误判 `0`、`""`、`false`。

7. **逻辑赋值运算符**：`||=`、`&&=`、`??=`。

8. **位运算符**：了解即可，现代 JavaScript 中使用场景不多。

9. **`in` 运算符**：检查对象属性是否存在（包含原型链）。

10. **`instanceof`**：检查对象是否是某个类的实例（沿原型链向上查找）。

下一章，我们将学习控制流——程序的灵魂所在。准备好了吗？继续冲！
