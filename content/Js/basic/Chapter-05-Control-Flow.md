+++
title = "第 5 章 控制流"
weight = 50
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 5 章 控制流

程序就像一条河流，代码从上往下流。但有时候，我们需要让程序「拐弯」或者「原地打转」——这就是控制流的作用。没有控制流，程序只能从头跑到尾，一成不变。有了控制流，程序才能做出「决策」，才能「循环」起来。

## 5.1 条件语句

### if 语句

最基础的条件语句：如果满足条件，就执行代码。

```javascript
// 基本语法
let temperature = 30;

if (temperature > 35) {
    console.log("太热了！空调开到最大！");
}

// 单行写法（不推荐，可读性差）
if (temperature > 35) console.log("太热了！");

// 推荐写法：即使只有一行，也加花括号
if (temperature > 35) {
    console.log("太热了！");
}
```

```javascript
// 实用示例
function checkAge(age) {
    if (age >= 18) {
        console.log("成年人，可以买酒");
    }

    if (age < 0) {
        console.log("年龄不能为负数！");
    }
}

checkAge(20); // 成年人，可以买酒
checkAge(-5); // 年龄不能为负数！
```

```javascript
// if 的条件会被自动转成布尔值，下面是全部 8 个 falsy 值
if (false) {} // 不执行
if (0) {}     // 不执行
if (-0) {}    // 不执行
if (0n) {}    // 不执行
if ("") {}    // 不执行
if (null) {}  // 不执行
if (undefined) {} // 不执行
if (NaN) {}   // 不执行

// 除此之外一切都是真。注意这一条和 Python 等语言不同：
if ([]) {
    console.log("空数组是 truthy"); // 会打印
}
if ({}) {
    console.log("空对象是 truthy"); // 会打印
}
if ("0") {
    console.log("字符串 '0' 是 truthy"); // 会打印，别把字符串 "0" 当成假
}

// 想判断数组是否为空，要显式检查长度
const list = [];
if (list.length === 0) {
    console.log("空数组");
}
```

### if...else 语句

二选一：满足条件执行这个，不满足执行那个。

```javascript
// 基本语法
let score = 75;

if (score >= 60) {
    console.log("及格了！🎉");
} else {
    console.log("不及格，要加油哦！📚");
}
```

```javascript
// 实际应用：登录验证
function login(username, password) {
    if (password === "123456") {
        console.log(`欢迎，${username}！`);
    } else {
        console.log("密码错误！");
    }
}

login("admin", "123456"); // 欢迎，admin！
login("admin", "wrong");   // 密码错误！
```

> 这里只是演示分支写法。真实项目里密码绝不能这样明文比较或打印，必须交给服务端做哈希校验（见第 38 章安全专题）。

### if...else if...else：多条件分支

多个条件依次检查，找到第一个满足的。

```javascript
// 基本语法
let grade = 85;

if (grade >= 90) {
    console.log("优秀！A级");
} else if (grade >= 80) {
    console.log("良好！B级");
} else if (grade >= 70) {
    console.log("中等！C级");
} else if (grade >= 60) {
    console.log("及格！D级");
} else {
    console.log("不及格！F级");
}

// 输出：良好！B级
```

```javascript
// 实际应用：BMI 计算
function calculateBMI(weight, height) {
    const bmi = weight / (height * height);

    if (bmi < 18.5) {
        console.log("体重过轻");
    } else if (bmi < 24) {
        console.log("体重正常");
    } else if (bmi < 28) {
        console.log("体重过重");
    } else {
        console.log("肥胖");
    }

    return bmi;
}

console.log("BMI:", calculateBMI(70, 1.75)); // BMI: 22.857... 体重正常
```

### switch 语句：多值匹配

当需要匹配一个值的多个可能时，`switch` 比 `if...else if` 更清晰。

```javascript
// 基本语法
let day = 3;

switch (day) {
    case 1:
        console.log("今天是星期一");
        break;
    case 2:
        console.log("今天是星期二");
        break;
    case 3:
        console.log("今天是星期三");
        break;
    case 4:
        console.log("今天是星期四");
        break;
    case 5:
        console.log("今天是星期五");
        break;
    case 6:
    case 7:
        console.log("周末休息日");
        break;
    default:
        console.log("无效的日期");
}

// 输出：今天是星期三
```

```javascript
// 关键规则：switch 用「严格相等 ===」比较，不做任何类型转换
let code = "1"; // 注意是字符串

switch (code) {
    case 1:
        console.log("匹配到数字 1"); // 不执行（"1" !== 1）
        break;
    case "1":
        console.log("匹配到字符串 \"1\""); // 执行
        break;
    default:
        console.log("都没匹配上");
}

// 同理，NaN 永远匹配不到自己
// switch (NaN) { case NaN: /* 永远进不来 */ }

// case 后面的表达式是从上往下依次求值的，命中的第一个就停
// 所以 case 里最好只写常量，别塞函数调用或赋值
```

```javascript
// default 不一定非要写在最后，它只在「所有 case 都没命中」时执行
let animal = "dog";

switch (animal) {
    default:
        console.log("未知动物");
        break; // 即使 default 在开头，也建议加 break
    case "cat":
        console.log("猫");
        break;
    case "dog":
        console.log("狗"); // 命中这里，default 不会执行
        break;
}
// 输出：狗
```

```javascript
// 实际应用：计算器
function calculate(a, b, operator) {
    let result;

    switch (operator) {
        case "+":
            result = a + b;
            break;
        case "-":
            result = a - b;
            break;
        case "*":
            result = a * b;
            break;
        case "/":
            if (b === 0) {
                console.log("除数不能为零！");
                return;
            }
            result = a / b;
            break;
        case "%":
            result = a % b;
            break;
        default:
            console.log("不支持的运算符：" + operator);
            return;
    }

    console.log(`${a} ${operator} ${b} = ${result}`);
}

calculate(10, 5, "+"); // 10 + 5 = 15
calculate(10, 5, "/"); // 10 / 5 = 2
calculate(10, 0, "/"); // 除数不能为零！
```

### switch 的 break：穿透效应

如果 `switch` 语句中缺少 `break`，会发生「穿透」——执行完一个 case 后，继续执行下一个 case，直到遇到 `break` 或 `switch` 结束。

```javascript
// 没有 break：会发生穿透
let fruit = "apple";

switch (fruit) {
    case "apple":
        console.log("这是苹果"); // 会执行
        // 没有 break，继续往下
    case "banana":
        console.log("这是香蕉"); // 会执行（穿透过来的）
        break;
    case "orange":
        console.log("这是橙子");
        break;
    default:
        console.log("未知水果");
}

// 输出：
// 这是苹果
// 这是香蕉
```

```javascript
// 利用穿透：多个 case 执行相同逻辑
let month = 3;

switch (month) {
    case 1:
    case 2:
    case 3:
        console.log("第一季度（春）"); // 1月、2月、3月都执行这个
        break;
    case 4:
    case 5:
    case 6:
        console.log("第二季度（夏）");
        break;
    case 7:
    case 8:
    case 9:
        console.log("第三季度（秋）");
        break;
    case 10:
    case 11:
    case 12:
        console.log("第四季度（冬）");
        break;
}

// 输出：第一季度（春）
```

```javascript
// 实际应用：分数等级
function getGrade(score) {
    let grade;

    switch (true) { // 注意：这里用 true 作为判断值
        case score >= 90:
            grade = "A";
            break;
        case score >= 80:
            grade = "B";
            break;
        case score >= 70:
            grade = "C";
            break;
        case score >= 60:
            grade = "D";
            break;
        default:
            grade = "F";
    }

    return grade;
}

console.log(getGrade(95)); // A
console.log(getGrade(82)); // B
console.log(getGrade(45)); // F
```

> 关于 `switch (true)` 这个技巧：它确实能跑通，原理是每个 `case` 表达式求值后与 `true` 做严格比较。但绝大多数情况下，同样的逻辑用 `if...else if` 写出来更直观，也更符合阅读习惯，建议只在团队已有约定时使用。

### switch 的 default：默认分支

`default` 分支在没有任何 `case` 匹配时执行。

```javascript
// 基本语法
let color = "purple";

switch (color) {
    case "red":
        console.log("红色");
        break;
    case "blue":
        console.log("蓝色");
        break;
    case "green":
        console.log("绿色");
        break;
    default:
        console.log("未知颜色");
}

// 输出：未知颜色
```

```javascript
// 实际应用：处理 API 响应状态码
function handleStatusCode(code) {
    switch (code) {
        case 200:
            console.log("请求成功");
            break;
        case 201:
            console.log("资源创建成功");
            break;
        case 400:
            console.log("请求参数错误");
            break;
        case 401:
            console.log("未授权，请登录");
            break;
        case 404:
            console.log("资源不存在");
            break;
        case 500:
            console.log("服务器内部错误");
            break;
        default:
            console.log(`未知状态码：${code}`);
    }
}

handleStatusCode(200); // 请求成功
handleStatusCode(999); // 未知状态码：999
```

### switch vs if...else 的选择

| 场景 | 推荐使用 |
|------|---------|
| 匹配固定值（如星期几、月份） | `switch` |
| 匹配范围或条件（如 BMI > 30） | `if...else` |
| 需要比较复杂表达式 | `if...else` |
| 多个 case 共用逻辑 | `switch`（利用穿透） |
| 判断严格的相等性 | `switch` 或 `if...else` 都可以 |

```javascript
// switch 更适合的场景
let status = "pending";

switch (status) {
    case "pending":
        console.log("处理中...");
        break;
    case "approved":
        console.log("已批准");
        break;
    case "rejected":
        console.log("已拒绝");
        break;
    default:
        console.log("未知状态");
}

// if...else 更适合的场景
let temperature = 32;

if (temperature > 35) {
    console.log("高温预警");
} else if (temperature > 30) {
    console.log("天气炎热");
} else if (temperature > 20) {
    console.log("温度适宜");
} else if (temperature > 10) {
    console.log("天气凉爽");
} else {
    console.log("天气寒冷");
}
```

## 5.2 循环语句

### for 循环：计数循环

`for` 循环是最常用的循环语句，适合已知循环次数的场景。

```javascript
// 基本语法
for (let i = 0; i < 5; i++) {
    console.log("第" + (i + 1) + "次循环");
}

// 输出：
// 第1次循环
// 第2次循环
// 第3次循环
// 第4次循环
// 第5次循环
```

```javascript
// 遍历数组
const fruits = ["苹果", "香蕉", "橙子", "葡萄"];

for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}

// 输出：
// 苹果
// 香蕉
// 橙子
// 葡萄
```

```javascript
// 计算 1 到 100 的和
let sum = 0;
for (let i = 1; i <= 100; i++) {
    sum += i;
}
console.log("1+2+...+100 =", sum); // 5050

// 计算阶乘
function factorial(n) {
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

console.log("5! =", factorial(5)); // 120
console.log("10! =", factorial(10)); // 3628800
```

```javascript
// 嵌套循环：打印九九乘法表
for (let i = 1; i <= 9; i++) {
    let row = "";
    for (let j = 1; j <= i; j++) {
        row += `${j}×${i}=${i * j}\t`;
    }
    console.log(row);
}

// 输出：
// 1×1=1
// 1×2=2	2×2=4
// 1×3=3	2×3=6	3×3=9
// ...以此类推到 9×9=81
```

### for...of：直接遍历「值」（ES6）

普通 `for` 循环要自己管下标，写起来啰嗦还容易越界。`for...of` 直接给你每一个值，适用于所有可迭代对象（数组、字符串、Map、Set、NodeList、生成器……）。

```javascript
// 遍历数组：比下标循环清爽得多
const fruits = ["苹果", "香蕉", "橙子"];

for (const fruit of fruits) {
    console.log(fruit);
}
// 苹果
// 香蕉
// 橙子

// 遍历字符串：按「字符」切分（注意 emoji 等代理对的处理，见下）
for (const ch of "abc") {
    console.log(ch); // a b c
}

// 遍历 Set / Map
const uniqued = new Set([1, 2, 2, 3]);
for (const v of uniqued) {
    console.log(v); // 1 2 3
}

const scores = new Map([["语文", 90], ["数学", 95]]);
for (const [subject, score] of scores) {
    console.log(subject, score); // 语文 90 / 数学 95
}
```

```javascript
// 需要下标时，用 entries()，别退回去写下标循环
const letters = ["a", "b", "c"];

for (const [index, value] of letters.entries()) {
    console.log(index, value); // 0 "a" / 1 "b" / 2 "c"
}

// for...of 同样支持 break / continue
for (const n of [1, 2, 3, 4, 5]) {
    if (n === 2) continue;
    if (n === 4) break;
    console.log(n); // 1 3
}

// 想要「中途改数组」要格外小心：迭代过程中增删元素，行为不好预测
const mutable = [1, 2, 3];
for (const v of mutable) {
    if (v === 2) mutable.push(99); // 勉强能跑，但属于危险操作
}
```

```javascript
// for...of 的两个常见报错
// 1. 普通对象不是可迭代对象，直接用会抛错
const person = { name: "张三", age: 25 };
// for (const v of person) {} // TypeError: person is not iterable

// 想遍历对象，请显式选择要遍历什么
for (const key of Object.keys(person)) console.log(key);       // name age
for (const val of Object.values(person)) console.log(val);     // 张三 25
for (const [k, v] of Object.entries(person)) console.log(k, v); // name 张三 / age 25

// 2. 对 null / undefined 迭代也会抛错
// for (const v of null) {} // TypeError
// 需要容错时先兜底
for (const v of person.hobbies ?? []) {
    console.log(v); // 没有 hobbies 就什么都不做
}
```

### for...in：遍历「键名」（主要用于对象）

`for...in` 遍历的是对象的**可枚举属性名**（字符串），而且**会沿着原型链往上找**，这一点极易踩坑。

```javascript
// 遍历对象的键
const user = { name: "张三", age: 25, city: "北京" };

for (const key in user) {
    console.log(key, "=", user[key]); // name = 张三 / age = 25 / city = 北京
}

// 陷阱：原型链上被「可枚举」的属性也会被遍历到
Object.prototype.hacked = "我是原型上的属性"; // 教学演示，实际项目中绝不要这么写
for (const key in user) {
    console.log(key); // name age city hacked ← 多出来一个！
}
delete Object.prototype.hacked; // 用完清理掉

// 正确姿势：用 Object.hasOwn 过滤掉继承来的属性
for (const key in user) {
    if (!Object.hasOwn(user, key)) continue;
    console.log(key); // name age city
}
```

```javascript
// 千万别用 for...in 遍历数组
const arr = ["a", "b", "c"];
arr.extra = "我是挂上去的额外属性"; // 数组也是对象，可以挂属性

for (const key in arr) {
    console.log(key); // "0" "1" "2" "extra" —— 键是字符串，还混进了额外属性
}

// 也别指望顺序一定是你想象的那样；数组请用 for...of 或 forEach
for (const value of arr) {
    console.log(value); // "a" "b" "c"
}

// 如果只是想拿到下标和值，entries() 更明确
arr.forEach((value, index) => console.log(index, value));
```

什么时候用哪个，一张表说清楚：

| 需求 | 推荐写法 |
|------|----------|
| 遍历数组 / 字符串 / Set / Map 的**值** | `for...of` |
| 遍历对象自身的**键值对** | `Object.entries()` + `for...of`，或 `for...in` 配合 `Object.hasOwn` 过滤 |
| 需要下标 | `arr.entries()` 配 `for...of`，或直接 `forEach` |
| 需要 `break` / `continue` / `await` | 只能用 `for...of`（`forEach` 里做不到） |
| 遍历数组的**下标** | 不要用 `for...in`（键是字符串，还会带上额外属性） |

> 关于 emoji：`for...of` 按「码点」拆分，比下标循环更正确地处理了代理对，但组合字符（如带修饰符的 emoji）仍可能被拆散，需要按「字素簇」处理时要上 `Intl.Segmenter`。

### while 循环：条件循环

`while` 循环在条件为 `true` 时重复执行，适合不确定循环次数的场景。

```javascript
// 基本语法
let count = 0;

while (count < 3) {
    console.log("计数器：" + count);
    count++;
}

// 输出：
// 计数器：0
// 计数器：1
// 计数器：2
```

```javascript
// 实际应用：猜数字游戏
function guessNumber() {
    const target = Math.floor(Math.random() * 10) + 1;
    let attempts = 0;
    let guess = 0;

    console.log("猜一个 1-10 之间的数字：");

    while (guess !== target) {
        // 模拟用户输入（实际应该用 prompt）
        guess = Math.floor(Math.random() * 10) + 1;
        attempts++;
        console.log("尝试次数：" + attempts + "，猜的数字：" + guess);
    }

    console.log(`恭喜！猜对了！答案就是 ${target}，用了 ${attempts} 次`);
}

// guessNumber();
```

```javascript
// while 的注意事项：循环变量必须有机会让条件变成 false，否则就是死循环
// 下面这段忘了写 i++，条件永远是 true，页面会直接卡死
// let bad = 0;
// while (bad < 10) {
//     console.log(bad);
// }

// 正确做法：确保每一步都在靠近退出条件
let i = 0;
while (i < 10) {
    if (i === 5) {
        console.log("遇到5，提前退出");
        break; // 用 break 提前退出
    }
    i++;
}

// while (true) 本身没有错，只要循环体里有可靠的退出路径
let n = 0;
while (true) {
    n++;
    if (n >= 3) break; // 一定会到达
}
console.log(n); // 3
```

### do...while：保证至少执行一次

`do...while` 和 `while` 的区别：`do...while` 先执行一次，再判断条件。

```javascript
// 基本语法
let i = 0;

do {
    console.log("至少执行一次，i = " + i);
    i++;
} while (i < 0);

// 输出：至少执行一次，i = 0
// 即使条件不满足，也执行了一次！
```

```javascript
// 实际应用：菜单选择
function showMenu() {
    let choice;

    do {
        console.log("===== 菜单 =====");
        console.log("1. 开始游戏");
        console.log("2. 继续游戏");
        console.log("3. 退出游戏");
        console.log("================");

        // 模拟用户选择
        choice = Math.random() > 0.5 ? 3 : 1; // 随机选择1或3
        console.log("你选择了：" + choice);

    } while (choice !== 3);

    console.log("退出游戏，再见！");
}

// showMenu();
```

```javascript
// while vs do...while
// while：条件不满足，代码块一次都不执行
let a = 0;
while (a > 10) {
    console.log("不会执行"); // 不会打印
}

// do...while：代码块至少执行一次
let b = 0;
do {
    console.log("会执行一次"); // 会打印一次
} while (b > 10);
```

### break：提前退出循环

`break` 用于**立即退出**整个循环，不再执行后续迭代。

```javascript
// 在 for 循环中使用 break
for (let i = 1; i <= 10; i++) {
    if (i === 5) {
        console.log("遇到5，退出循环");
        break;
    }
    console.log("i = " + i);
}

// 输出：
// i = 1
// i = 2
// i = 3
// i = 4
// 遇到5，退出循环
// （不会继续执行 i = 5, 6, 7, 8, 9, 10）
```

```javascript
// 实际应用：查找数组中的元素
const numbers = [3, 7, 12, 5, 20, 15];
const target = 5;
let found = false;

for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] === target) {
        console.log(`找到了！索引是 ${i}`);
        found = true;
        break; // 找到就退出，不用继续找
    }
}

if (!found) {
    console.log("没找到");
}

// 输出：找到了！索引是 3
```

```javascript
// 在嵌套循环中使用 break（只退出内层循环）
for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 5; j++) {
        if (j === 2) {
            break; // 只退出内层循环
        }
        console.log(`i=${i}, j=${j}`);
    }
    console.log("--- 内层循环结束 ---");
}

// 输出：
// i=0, j=0
// i=0, j=1
// --- 内层循环结束 ---
// i=1, j=0
// i=1, j=1
// --- 内层循环结束 ---
// i=2, j=0
// i=2, j=1
// --- 内层循环结束 ---
```

### continue：跳过本次循环

`continue` 用于**跳过**当前迭代，继续执行下一次循环。

```javascript
// 在 for 循环中使用 continue
for (let i = 1; i <= 5; i++) {
    if (i === 3) {
        console.log("跳过3");
        continue; // 跳过 i=3 的剩余代码
    }
    console.log("i = " + i);
}

// 输出：
// i = 1
// i = 2
// 跳过3
// i = 4
// i = 5
```

```javascript
// 实际应用：打印奇数
console.log("1到10之间的奇数：");
for (let i = 1; i <= 10; i++) {
    if (i % 2 === 0) {
        continue; // 偶数跳过
    }
    console.log(i); // 1, 3, 5, 7, 9
}
```

```javascript
// 实际应用：计算总和，但跳过负数
const numbers = [5, -3, 10, -8, 20, -1, 15];
let sum = 0;

for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] < 0) {
        continue; // 负数跳过，不计入总和
    }
    sum += numbers[i];
}

console.log("正数总和：" + sum); // 5 + 10 + 20 + 15 = 50
```

```javascript
// continue 在 while 中的使用
let i = 0;
while (i < 5) {
    i++;
    if (i === 3) {
        continue; // 跳过 i=3 的打印
    }
    console.log("i = " + i);
}

// 输出：
// i = 1
// i = 2
// i = 4
// i = 5
// 注意：while 中使用 continue 要小心死循环！
```

### 嵌套循环

循环里面套循环，用于处理二维数据。

```javascript
// 打印矩形
function printRectangle(rows, cols) {
    let output = "";
    for (let i = 0; i < rows; i++) {
        let row = "";
        for (let j = 0; j < cols; j++) {
            row += "★ ";
        }
        output += row + "\n";
    }
    console.log(output);
}

printRectangle(3, 5);

// 输出：
// ★ ★ ★ ★ ★
// ★ ★ ★ ★ ★
// ★ ★ ★ ★ ★
```

```javascript
// 打印直角三角形
function printTriangle(n) {
    for (let i = 1; i <= n; i++) {
        let row = "";
        for (let j = 1; j <= i; j++) {
            row += "★ ";
        }
        console.log(row);
    }
}

printTriangle(5);

// 输出：
// ★
// ★ ★
// ★ ★ ★
// ★ ★ ★ ★
// ★ ★ ★ ★ ★
```

```javascript
// 打印倒直角三角形
function printInvertedTriangle(n) {
    for (let i = n; i >= 1; i--) {
        let row = "";
        for (let j = 1; j <= i; j++) {
            row += "★ ";
        }
        console.log(row);
    }
}

printInvertedTriangle(5);

// 输出：
// ★ ★ ★ ★ ★
// ★ ★ ★ ★
// ★ ★ ★
// ★ ★
// ★
```

```javascript
// 实际应用：矩阵相乘
function multiplyMatrices(a, b) {
    const rowsA = a.length;
    const colsA = a[0].length;
    const colsB = b[0].length;

    const result = [];

    for (let i = 0; i < rowsA; i++) {
        result[i] = [];
        for (let j = 0; j < colsB; j++) {
            let sum = 0;
            for (let k = 0; k < colsA; k++) {
                sum += a[i][k] * b[k][j];
            }
            result[i][j] = sum;
        }
    }

    return result;
}

const matrixA = [
    [1, 2],
    [3, 4]
];
const matrixB = [
    [5, 6],
    [7, 8]
];

const result = multiplyMatrices(matrixA, matrixB);
console.log(result);
// [[19, 22], [43, 50]]
// 验证：1*5+2*7=19, 1*6+2*8=22, 3*5+4*7=43, 3*6+4*8=50
```

### 标签语句：一次跳出多层循环

`break` 默认只跳出「离它最近的那一层」。如果想在内层循环里一次性跳出外层，可以给循环贴一个标签。

```javascript
// 给外层循环贴标签，break 时指到标签上
outer:
for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
        if (i === 1 && j === 1) {
            console.log(`在 i=${i}, j=${j} 处跳出外层`);
            break outer; // 直接结束外层循环
        }
        console.log(`i=${i}, j=${j}`);
    }
}
// 输出：
// i=0, j=0
// i=0, j=1
// i=0, j=2
// i=1, j=0
// 在 i=1, j=1 处跳出外层
```

```javascript
// continue + 标签：跳过外层循环的「本次迭代」，直接进入外层的下一轮
outer:
for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
        if (j === 1) {
            continue outer; // 内层剩下的 j 全部不跑了
        }
        console.log(`i=${i}, j=${j}`);
    }
    console.log("这行永远执行不到");
}
// 输出：
// i=0, j=0
// i=1, j=0
// i=2, j=0
```

> 标签语法属于「能用但不必常用」的特性。如果发现自己需要三层以上的标签跳转，通常说明这段逻辑该拆成函数了——在函数里直接 `return` 往往更清晰。

### 循环选择速查

| 场景 | 推荐写法 |
|------|----------|
| 次数已知，或需要下标控制步长 | `for (let i = 0; ...)` |
| 条件驱动、次数不确定 | `while` |
| 至少要执行一次（如菜单、输入校验） | `do...while` |
| 遍历数组 / Set / Map / 字符串的值 | `for...of` |
| 遍历对象的键值对 | `Object.entries()` / `Object.keys()` |
| 只想对每个元素做一件事、不需要中断 | `forEach`、`map` 等数组方法（见第 7 章） |

---

## 本章小结

本章我们学习了 JavaScript 的控制流：

1. **条件语句**：`if` 基础单分支，`if...else` 二选一，`if...else if...else` 多条件分支。`if` 的判断依据是「真值/假值」，只有 8 个 falsy 值（`false 0 -0 0n "" null undefined NaN`），空数组和空对象都是真。

2. **`switch`**：用**严格相等**比较，不做类型转换，所以 `"1"` 匹配不到 `case 1`；`break` 缺失会「穿透」到下一个 `case`（也可以刻意利用穿透让多个 `case` 共用逻辑）；`default` 可以写在任意位置。

3. **循环语句**：`for` 计数循环（已知次数），`while` 条件循环（未知次数），`do...while` 至少执行一次。写 `while` 时务必确保循环变量在靠近退出条件，否则就是死循环；`while (true)` 配合可靠的 `break` 是合法写法。

4. **遍历循环**：`for...of` 遍历「值」，适用于数组、字符串、Map、Set 等可迭代对象，支持 `break`/`continue`/`await`；普通对象不是可迭代对象，要用 `Object.keys/values/entries`。`for...in` 遍历「键名」，会带上原型链上的可枚举属性，需要 `Object.hasOwn` 过滤，尤其不要拿它遍历数组。

5. **循环控制**：`break` 立即退出，`continue` 跳过本次迭代；给循环贴标签（`outer:`）后，可以一次跳出多层循环，但真需要多层跳转时，通常拆成函数用 `return` 更清晰。

6. **嵌套循环**：外层控制行、内层控制列，常用于二维数据和矩阵运算；能提前满足条件就 `break`，别做无谓的遍历。

下一章我们会把运算符里那些容易忽略的细节再补一遍。准备好了吗？继续冲！
