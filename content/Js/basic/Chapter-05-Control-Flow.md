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
// while 的注意事项：确保条件最终会变为 false
// 错误的例子：无限循环！
// while (true) {
//     console.log("这会一直执行，直到浏览器崩溃！");
// }

// 正确做法：确保有退出条件
let i = 0;
while (i < 10) {
    if (i === 5) {
        console.log("遇到5，提前退出");
        break; // 用 break 提前退出
    }
    i++;
}
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

---

## 本章小结

本章我们学习了 JavaScript 的控制流：

1. **条件语句**：`if` 基础单分支，`if...else` 二选一，`if...else if...else` 多条件分支，`switch` 多值匹配（注意 `break` 的穿透效应和 `default` 默认分支）。

2. **循环语句**：`for` 计数循环（已知次数），`while` 条件循环（未知次数），`do...while` 至少执行一次。

3. **循环控制**：`break` 立即退出循环，`continue` 跳过本次迭代。

4. **嵌套循环**：外层循环控制行，内层循环控制列，常用于处理二维数据（矩阵、表格等）。

5. **性能注意**：避免在循环内进行重复计算（把不变的值提到循环外），避免不必要的嵌套循环。

下一章我们将进入数据结构篇，学习 JavaScript 的数组。准备好了吗？继续冲！
