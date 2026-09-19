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

### 加减乘除取模：`+ - * / %`（外加幂运算 `**`）

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
console.log(Math.trunc(10 / 3)); // 3（直接砍掉小数部分）
console.log((10 / 3) | 0);       // 3（位运算截断，仅在 32 位整数范围内有效，可读性差，不推荐）
```

```javascript
// 幂运算 **（ES2016 引入，替代 Math.pow）
console.log(2 ** 10);      // 1024
console.log(2 ** -1);      // 0.5（负数次幂得到小数）
console.log((-2) ** 3);    // -8（负数底数必须加括号）
console.log(2 ** 3 ** 2);  // 512（右结合，等于 2 ** (3 ** 2)）
console.log(2 ** 53);      // 9007199254740992（再大就超出安全整数范围）

// 开方：用分数次幂，比 Math.sqrt 可读性差，一般还是写 Math.sqrt
console.log(9 ** 0.5);     // 3
console.log(Math.sqrt(9)); // 3（推荐）
```

```javascript
// 取模的结果符号跟随「被除数」，而不是数学意义上的「余数」
console.log(7 % 3);   // 1
console.log(-7 % 3);  // -1（不是 2！）
console.log(7 % -3);  // 1（符号只看左边）

// 想要始终为正的「模」，需要手动补一下
const mod = (n, m) => ((n % m) + m) % m;
console.log(mod(-7, 3)); // 2
```

```javascript
// 最经典的一课：+ 既能做加法，也能做字符串拼接
console.log(1 + 2);       // 3（都是数字，做加法）
console.log("1" + 2);     // "12"（只要有一边是字符串，就变成拼接）
console.log(1 + "2");     // "12"
console.log(1 + 2 + "3"); // "33"（从左往右：先 1+2=3，再 3+"3"="33"）
console.log("1" + 2 + 3); // "123"（先 "1"+2="12"，再 "12"+3="123"）

// 而 - * / % 没有「拼接」这个用法，遇到字符串会先转数字
console.log("5" - 1);   // 4
console.log("5" * "2"); // 10
console.log("abc" - 1); // NaN（转不成数字）

// 一元 + 是最短的「转数字」写法
console.log(+"5");      // 5
console.log(+"");       // 0
console.log(+"abc");    // NaN

// 实战建议：表单里的值都是字符串，做加法前先显式转换
const input = "10";
console.log(input + 5);          // "105"（踩坑）
console.log(Number(input) + 5);  // 15（正确）
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

// 字符串比较：逐位比较 UTF-16 编码单元（不是「按字典序」！）
console.log("a" > "b");    // false（a=97, b=98）
console.log("apple" < "banana"); // true（先比首字符就分出胜负）
console.log("Hello" > "hello"); // false（H=72, h=104）

// 中文、emoji 的排序结果往往反直觉
console.log("字母" > "数字"); // false（"字"=U+5B57，"数"=U+6570，"字" 反而更小）
console.log("a" > "A");       // true（小写字母编码值大于大写）
console.log("😀" > "\uFFFF");  // false！按码点 U+1F600 应更大，但 JS 逐位比的是
                              // 代理对的首单元 0xD83D，它小于 0xFFFF

// 想按人类语言习惯排序，别用 > <，用 localeCompare
console.log("apple".localeCompare("banana")); // -1（负数表示排在前面）
console.log("字".localeCompare("数", "zh"));   // 按中文拼音/笔画规则比较
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

// 比较数组内容：逐个比，或用 JSON.stringify
console.log(JSON.stringify(arr1) === JSON.stringify(arr2)); // true
console.log(arr1.length === arr2.length && arr1.every((item, i) => item === arr2[i])); // true

// 注意：JSON.stringify 比较法并不可靠
console.log(JSON.stringify({ a: 1, b: 2 }) === JSON.stringify({ b: 2, a: 1 })); // false（键顺序不同）
// 数组里的 undefined 会被序列化成 null，于是下面这个比较会「错误地」成立
console.log(JSON.stringify([undefined]) === JSON.stringify([null])); // true（实际两者并不相等）
// 对象里的 undefined / 函数 / Symbol 键则会被整个丢掉
console.log(JSON.stringify({ a: undefined, b() {} })); // "{}"
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

上表里 `[] == false` 的转换过程值得走一遍：`[]` 先转成字符串 `""`，再转成数字 `0`；`false` 转成数字 `0`；于是 `0 == 0` 成立。

```javascript
// === 也不是「万无一失」，它有两个著名的边缘情况
console.log(NaN === NaN);   // false（自己不等于自己）
console.log(0 === -0);      // true（但两者在多数场景下行为不同，比如 1/x）

// Object.is 能区分这些情况，可以理解为「更严格的 ===」
console.log(Object.is(NaN, NaN)); // true
console.log(Object.is(0, -0));    // false
// 除此之外，Object.is 和 === 的判定结果完全一致
```

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

```javascript
// 顺带记住：全局 isNaN 会把参数先转成数字，Number.isNaN 不会
console.log(isNaN("abc"));        // true（"abc" 转成 NaN，所以是 true —— 常被认为是个坑）
console.log(Number.isNaN("abc")); // false（参数压根不是数字类型）
console.log(isNaN(undefined));    // true（undefined 转成 NaN）
console.log(Number.isNaN(undefined)); // false

// 更现代的写法：Number.isNaN 配合 typeof
const isRealNaN = (v) => Number.isNaN(v);
console.log(isRealNaN(NaN)); // true
console.log(isRealNaN(0 / 0)); // true
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
// 注意：false、0、-0、0n、""、null、undefined、NaN 这八个值才是 falsy，其余全是 truthy
const values = [0, -0, 0n, "", null, undefined, NaN, false, "hello", 42];

for (const val of values) {
    const result = val && "truthy";
    console.log(`${val} && "truthy" =`, result);
}
// 0 && "truthy" = 0
// 0 && "truthy" = 0                （-0 用模板字符串打印出来也是 0）
// 0 && "truthy" = 0                （0n 同理）
// "" && "truthy" = ""
// null && "truthy" = null
// undefined && "truthy" = undefined
// NaN && "truthy" = NaN
// false && "truthy" = false
// "hello" && "truthy" = "truthy"
// 42 && "truthy" = "truthy"

// 空对象、空数组虽然是「空」的，但它们是对象，永远为 truthy
console.log([] ? "yes" : "no"); // "yes"
console.log({} ? "yes" : "no"); // "yes"
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
const gradeByTernary = score >= 90 ? "A" : score >= 80 ? "B" : score >= 60 ? "C" : "D";
console.log(gradeByTernary); // "B"

// 条件一多，推荐用 if...else
let grade;
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else if (score >= 60) {
    grade = "C";
} else {
    grade = "D";
}
console.log(grade); // "B"
```

```javascript
// 实际应用

// 1. 条件赋值
const isVip = true;
const discount = isVip ? 0.8 : 1.0;
console.log("原价100，折后", 100 * discount); // 原价100，折后 80

// 别忘了：三元也是「表达式」，可以直接嵌进模板字符串或 JSX
const price = 100;
console.log(`折后价：${price * (isVip ? 0.8 : 1)} 元`); // 折后价：80 元

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

// profile 存在时，这样写没有任何问题
const name = user.profile.name; // "张三"

// 但只要对象缺了这一层，就会直接抛错
const emptyUser = {};
// emptyUser.profile.name; // TypeError: Cannot read properties of undefined (reading 'name')

// 以前要这样写：
const safeName = (emptyUser.profile && emptyUser.profile.name) || "未知";
console.log(safeName); // "未知"
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
// 可选链的四种形态（下面 obj / arr / index 仅为示意）
// 1. 属性访问
obj?.prop
obj?.["prop"]        // 等价于 obj?.prop，用于键名是变量或含特殊字符时

// 2. 方法调用
obj.method?.()       // 方法名存在才调用
obj?.method()        // obj 存在才访问（注意两者保护的对象不同）

// 3. 数组 / 类数组下标
arr?.[0]
arr?.[index]

// 4. 与空值合并搭配，给「缺值」兜底
const user = {};
const name = user?.profile?.name ?? "匿名";
console.log(name); // "匿名"
```

```javascript
// 三个容易踩的坑

// 坑 1：?. 只保护「它自己那一层」，不会向后传染
const o = { a: {} };
console.log(o?.a?.b);  // undefined
// console.log(o?.x.b); // TypeError：o.x 是 undefined，后面的 .b 是普通访问
console.log(o?.x?.b);  // undefined（每一层都要写 ?.）

// 坑 2：?. 不能出现在赋值左侧
// document?.title = "Hi"; // SyntaxError：左侧不是合法赋值目标
if (document?.title !== undefined) {
    document.title = "Hi"; // 要赋值就老老实实写成这种形式
}

// 坑 3：new 不能直接和 ?. 连用
// const d = new Foo?.();      // SyntaxError
// 想用可选调用就得整体加括号，例如 new (Foo?.())()，但可读性很差，不如先判空再 new

// 附带一个好消息：?. 与 delete 可以安全组合
const target = { a: 1 };
delete target?.a; // 合法
console.log(target); // {}
```

```javascript
// 实际应用场景
// 注意：下面第 2 段用到了 document，需要在浏览器里运行

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

> 小贴士：`?.` 只对 `null` 和 `undefined` 短路。如果属性值是 `0`、`""` 或 `false`，可选链依旧会继续往后走，因为它检查的是「有没有值」而不是「值真假」。

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

const timeout = config.timeout || 3000; // 陷阱！0 被替换成 3000
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

```javascript
// 坑：?? 不能和 || / && 直接混用，必须加括号
const a = null, b = 0, c = "c";
// const x = a ?? b || c;   // SyntaxError: Unexpected token '||'
const x = a ?? (b || c);    // 合法：先算括号里的 ||
const y = (a ?? b) || c;    // 合法：先算 ??
console.log(x, y);          // "c" "c"

// ?? 同样有短路特性：左边不是 null/undefined 时，右边根本不会执行
function expensive() {
    console.log("计算了");
    return "结果";
}
console.log(0 ?? expensive());   // 0（不打印"计算了"）
console.log(null ?? expensive()); // 打印"计算了"，输出"结果"
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

```javascript
// 它们和「a = a || b」并不完全等价：条件不满足时，根本不会发生赋值
const box = {
    _v: 1,
    get v() {
        return this._v;
    },
    set v(val) {
        console.log("触发了 setter");
        this._v = val;
    }
};

box.v ||= 2;  // v 已经是 truthy，右侧不求值，赋值整个被跳过 —— 不打印"触发了 setter"
box.v = box.v || 2; // 这种写法永远会走一次赋值，会打印"触发了 setter"

// 所以 ||= / &&= / ??= 也叫「逻辑赋值」，只有在需要时才真正写回
let g = 0;
g ||= ++g;   // g 是 0（falsy），先算右边 ++g 得 1，再赋回 g
console.log(g); // 1
```

### 运算符优先级

运算符优先级决定了表达式的计算顺序。

```javascript
// 相当于加了隐含括号
console.log(2 + 3 * 4);       // 14（先算乘法）
console.log((2 + 3) * 4);     // 20（括号优先）

console.log(!true || true);   // true（!优先级最高）
console.log(!(true || true)); // false

console.log(2 + 3 === 5);     // true（+ 先算）
console.log(2 + 3 === 6);     // false

console.log(2 ** 3 ** 2);     // 512（幂运算是右结合：2 ** (3 ** 2)）
console.log(-2 ** 2);         // SyntaxError！一元负号和 ** 优先级的著名冲突
console.log((-2) ** 2);       // 4（必须加括号）
```

```javascript
// 建议：不确定优先级时，加括号
const result = ((a + b) * c) && (d || e);
const name = (user && user.profile && user.profile.name) || "匿名";
```

常见优先级（从高到低，只列常用的）：

| 级别 | 运算符 | 说明 |
|------|--------|------|
| 1 | `()` `[]` `.` `?.` | 分组、成员访问、可选链 |
| 2 | `new`（带参数） | 构造调用 |
| 3 | `++ --`（后置） | 后缀自增自减 |
| 4 | `! ~ + - ++ -- typeof void delete await` | 一元运算符（`+` 是取正，`-` 是取负） |
| 5 | `**` | 幂运算，右结合 |
| 6 | `* / %` | 乘除取模 |
| 7 | `+ -` | 加减 / 字符串拼接 |
| 8 | `<< >> >>>` | 移位 |
| 9 | `< <= > >= in instanceof` | 关系比较 |
| 10 | `== != === !==` | 相等比较 |
| 11 | `&` | 按位与 |
| 12 | `^` | 按位异或 |
| 13 | `\|` | 按位或 |
| 14 | `&&` | 逻辑与 |
| 15 | `\|\|` `??` | 逻辑或、空值合并（两者不能直接混用） |
| 16 | `? :` | 三元，右结合 |
| 17 | `= += -= *= /= %= **= <<= >>= &= ^= \|= &&= \|\|= ??=` | 赋值，右结合 |
| 18 | `,` | 逗号（最低） |

最需要记住的三条规则：

1. **一元运算符比二元运算符先算**，所以 `!a && b` 等价于 `(!a) && b`。
2. **`??` 不能与 `||`、`&&` 直接混用**（会报 `SyntaxError`），必须加括号。
3. **一旦读起来需要停顿，就加括号**。代码是写给人看的，编译器的优先级表不该由读者来背。
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
console.log(5 >> 1); // 2（右移一位，相当于除以 2 后向下取整）
// 5 = 0101
// 5 >> 1 = 0010 = 2

// >>> 无符号右移
console.log(-5 >>> 0); // 4294967291（把 -5 的补码当成无符号数读出来）

// 重要前提：所有位运算都会先把操作数转成「32 位有符号整数」，超出范围会被截断
console.log(2 ** 31 | 0);        // -2147483648（溢出成了负数！）
console.log(4294967296 & 1);     // 0（2^32 被截成 0）
console.log(1e20 | 0);           // 1661992960（一串毫无意义的残渣）
```

```javascript
// 位运算的实用技巧

// 1. 判断奇偶
const isOdd = (n) => (n & 1) === 1;
console.log(isOdd(5)); // true（奇数）
console.log(isOdd(4)); // false（偶数）
console.log(isOdd(-5)); // true（补码的低位同样是 1，负数也能正确判断）
console.log(isOdd(2 ** 32 + 3)); // true（虽然高位被截掉，但奇偶性不受影响）
// 注意：n & 1 本身返回的是数字 0 / 1，别直接当布尔值用
console.log(5 & 1); // 1（不是 true）

// 2. 快速乘除 2 —— 可读性和可控性都不如 * 2 / Math.floor，实战不推荐
const num = 8;
console.log(num << 1); // 16（左移一位 = 乘 2）
console.log(num >> 1); // 4（右移一位 = 除以 2 向下取整）

// 3. 取整：位运算做的是「截断」，不是「向下取整」，负数上两者不一样！
console.log((3.7 | 0));  // 3
console.log((-3.7 | 0)); // -3（截断），而 Math.floor(-3.7) 是 -4
console.log(Math.trunc(-3.7)); // -3 —— 语义上对等的其实是 Math.trunc
// 原理：位运算会先把操作数转成 32 位整数，小数部分被直接丢弃

// 4. 交换两个数（不用临时变量）
let x = 5, y = 3;
x = x ^ y;
y = x ^ y;
x = x ^ y;
console.log(x, y); // 3, 5
// 这只是一道智力题，真实代码里用 [x, y] = [y, x] 更好读
```

> 结论：位运算在当前 JavaScript 里主要用于**位标志（权限位、选项组合）**和**无符号数转换**，日常的乘除取整请用 `*` `/` `Math.trunc`，别为了「快」牺牲可读性——引擎对这两种写法的优化差距通常可以忽略。

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

```javascript
// in 的两个注意点
// 1. in 只能用于对象，对基本类型会直接抛错
// console.log("a" in "abc"); // TypeError: Cannot use 'in' operator to search for 'a' in abc

// 2. 数组上用 in，检查的是「下标是否存在」，而且稀疏数组的空洞也会被算成「不存在」
const sparse = ["a", , "c"]; // 中间有个空洞
console.log(1 in sparse);   // false（该下标从未被赋值）
console.log(sparse[1]);     // undefined
// 想判断数组里有没有某个「值」，用 includes / indexOf，而不是 in
console.log(sparse.includes(undefined)); // true（空洞读出来就是 undefined）
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

```javascript
// instanceof 的底层：它其实是在调用构造函数上的 Symbol.hasInstance
class Even {
    static [Symbol.hasInstance](n) {
        return typeof n === "number" && n % 2 === 0;
    }
}
console.log(4 instanceof Even); // true
console.log(5 instanceof Even); // false
// 这也解释了为什么 instanceof 可以「被伪造」——它只信这个方法，不做真正的类型判断

// 跨 iframe / 跨 realm 时，构造函数不是同一个对象，instanceof 会失效
// 判断数组请用 Array.isArray（它专门处理了跨 realm），判断基本类型请用 typeof
console.log(Array.isArray([]));        // true（无论数组来自哪个窗口）
console.log(typeof "hello");           // "string"
console.log(typeof new String("hi"));  // "object"（包装对象！）
```

### 一元运算符与其他：`typeof delete void` 和逗号运算符

这几个运算符出场频率不高，但都藏在细节里。

```javascript
// typeof：返回一个字符串，注意它的两个「历史遗留」
console.log(typeof 1);           // "number"
console.log(typeof "a");         // "string"
console.log(typeof true);        // "boolean"
console.log(typeof undefined);   // "undefined"
console.log(typeof Symbol());    // "symbol"
console.log(typeof 1n);          // "bigint"
console.log(typeof {});          // "object"
console.log(typeof []);          // "object"（数组也是 object，这正是要配 Array.isArray 的原因）
console.log(typeof null);        // "object"（著名历史 bug，永远不会修）
console.log(typeof function(){}); // "function"
console.log(typeof 未声明的变量); // "undefined"（typeof 对未声明变量不抛错，其它运算符会）

// 用 typeof 安全判断「函数是否存在」
if (typeof window !== "undefined" && typeof window.fetch === "function") {
    console.log("可以使用 fetch");
}
```

```javascript
// delete：删除对象属性，成功返回 true
const obj = { a: 1, b: 2 };
console.log(delete obj.a); // true
console.log(obj);          // { b: 2 }

// 注意 1：删不掉变量、函数声明和不可配置属性（严格模式下还会抛错）
const x = 1;
console.log(delete x); // false（非严格模式下静默失败）
console.log("a" in Object.prototype); // true
console.log(delete Object.prototype.toString); // false（不可配置）

// 注意 2：删数组元素不会改变长度，只会留下空洞
const arr = [1, 2, 3];
delete arr[1];
console.log(arr);        // [ 1, <1 empty item>, 3 ]
console.log(arr.length); // 3（不是 2）
// 要移除元素请用 splice
```

```javascript
// void：求值后返回 undefined，最常见的用途是把表达式变成「不产生返回值」
console.log(void 0);          // undefined
console.log(void "hello");    // undefined（表达式照样会求值，只是结果被丢掉）

// 经典用法：阻止 a 标签跳转（现在一般用 preventDefault，下面一行需在浏览器中运行）
// <a href="javascript:void(0)">点我</a>
document.querySelector("a")?.addEventListener("click", (e) => e.preventDefault());
// 另一个真实用途：配合箭头函数简写「只求值不返回」，比如 void somePromise()
```

```javascript
// 逗号运算符：从左到右依次求值，返回最后一个的结果（优先级最低）
let p = 1;
const q = (p++, p + 10, p * 2);
console.log(q); // 4（p 先自增到 2，最后算 2 * 2）

// 常用场景：for 循环里放多个表达式
for (let i = 0, j = 10; i < j; i++, j--) {
    // 每次循环 i 加 1、j 减 1
}
// 注意别和「数组/参数分隔符」的逗号弄混，那两种逗号不是运算符
const multi = [1, 2, 3];
console.log(multi.length); // 3
```

---

## 本章小结

本章我们全面学习了 JavaScript 的运算符与表达式：

1. **算术运算符**：`+ - * / %` 以及 `+= -= *= /= %= **=`。取模结果的符号跟着被除数走；自增自减 `++a` 和 `a++` 有区别——前者先加后用，后者先用后加。

2. **比较运算符**：`> < >= <=` 按 UTF-16 编码单元逐位比较，中文和 emoji 的排序结果常常反直觉，需要人类语言顺序时用 `localeCompare`。相等比较请**默认用 `===` 和 `!==`**，唯一值得破例的是 `x == null` 这种同时判断 `null`/`undefined` 的简写。

3. **逻辑运算符**：`&&`、`||`、`!`。逻辑运算符有「短路求值」特性，且返回的是值而非布尔（只有 8 个 falsy 值：`false 0 -0 0n "" null undefined NaN`）。

4. **三元运算符**：`condition ? expr1 : expr2`，是 `if...else` 的简写，适合简单条件。

5. **可选链 `?.`**：安全访问深层属性，避免「地狱般的嵌套检查」。它只保护自己那一层，只能读不能写在赋值左侧。

6. **空值合并 `??`**：只在值为 `null` 或 `undefined` 时才使用默认值，不误判 `0`、`""`、`false`。

7. **逻辑赋值运算符**：`||=`、`&&=`、`??=`，条件不满足时连赋值动作都会被跳过。`??` 与 `||`/`&&` 混用必须加括号。

8. **位运算符**：所有位运算都先把操作数截成 32 位有符号整数，大数会失真；用于位标志、无符号转换，不适合拿来做取整或性能优化。

9. **`in` 运算符**：检查对象属性是否存在（包含原型链），对基本类型会抛错。

10. **`instanceof`**：检查对象是否是某个类的实例（沿原型链向上查找，本质是 `Symbol.hasInstance`）；跨 iframe 会失效，判断数组优先用 `Array.isArray`。

11. **`typeof` / `delete` / `void` / 逗号运算符**：`typeof null` 是 `"object"` 这个历史 bug 要记住；`delete` 删不掉变量和不可配置属性，删数组元素只留空洞；逗号运算符返回最后一个表达式的值。

下一章，我们将学习控制流——程序的灵魂所在。准备好了吗？继续冲！
