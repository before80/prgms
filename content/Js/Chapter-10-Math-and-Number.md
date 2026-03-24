+++
title = "第 10 章 数学与数值"
weight = 100
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 10 章 数学与数值

> 学好数学，走遍天下都不怕！——虽然大多数程序员只需要加减乘除，但 `Math` 对象告诉我们：JavaScript 的数学库比你想象的要强大得多。

## 10.1 Math 对象

JavaScript 有一个内置的数学宝库——`Math` 对象。它不是一个构造函数，你不能 `new Math()`，因为它只是一个**工具对象**，所有的方法都是静态方法，直接 `Math.xxx()` 调用就行。

---

### 取整：round / floor / ceil / trunc

取整是编程中最常见的数学操作之一。JavaScript 给了你四个取整高手，但它们各有性格：

#### Math.round — 四舍五入

```javascript
console.log(Math.round(1.4));   // 1
console.log(Math.round(1.5));   // 2
console.log(Math.round(-1.4));  // -1
console.log(Math.round(-1.5));  // -1（注意：负数的五舍六入）
console.log(Math.round(-1.6));  // -2
```

等等，`-1.5` 四舍五入变成 `-1`？没错！在 JavaScript（以及其他很多语言）中，`round` 对负数的处理是"五舍六入"，也就是：
- `-1.4` → `-1`
- `-1.5` → `-1`
- `-1.6` → `-2`

这是因为 round 采用的是"round half away from zero"（远离零取整）策略，而不是"round half to even"（银行家取整）。

#### Math.floor — 向下取整（地板）

```javascript
console.log(Math.floor(1.9));   // 1 — 永远向下，找地板
console.log(Math.floor(-1.9));  // -2 — 负数也一样，向下走更负的方向
console.log(Math.floor(5));     // 5 — 整数不变
console.log(Math.floor(0.1));   // 0
```

记住：`floor` 永远给你**小于或等于**原数的最大整数。就像坐电梯去地下室，不管你在1楼还是1.9楼，按下 `floor` 就直接到地下车库。

#### Math.ceil — 向上取整（天花板）

```javascript
console.log(Math.ceil(1.1));    // 2 — 永远向上，找天花板
console.log(Math.ceil(1.9));    // 2
console.log(Math.ceil(-1.1));   // -1 — 负数向上走（变得不那么负）
console.log(Math.ceil(-1.9));   // -1
console.log(Math.ceil(5));      // 5 — 整数不变
```

记住：`ceil` 永远给你**大于或等于**原数的最小整数。就像坐电梯去顶楼，不管你在5楼还是5.1楼，按下 `ceil` 就直接到最高层。

#### Math.trunc — 直接截断

```javascript
console.log(Math.trunc(1.9));   // 1 — 直接砍掉小数部分
console.log(Math.trunc(-1.9));  // -1 — 直接砍掉，不管正负
console.log(Math.trunc(0.123)); // 0
console.log(Math.trunc(-0.123)); // -0（注意返回 -0）
```

`trunc` 是 ES6 引入的，它只关心小数点左边的整数部分，小数部分直接"截断"，不管正负。

#### 四者对比

```javascript
const num = 3.7;

console.log(Math.round(num));   // 4 — 四舍五入
console.log(Math.floor(num));   // 3 — 向下取整
console.log(Math.ceil(num));    // 4 — 向上取整
console.log(Math.trunc(num));   // 3 — 直接截断

const negNum = -3.7;

console.log(Math.round(negNum));  // -4 — 四舍五入
console.log(Math.floor(negNum));  // -4 — 向下取整（更负）
console.log(Math.ceil(negNum));   // -3 — 向上取整（不那么负）
console.log(Math.trunc(negNum));  // -3 — 直接截断
```

> 💡 口诀：
> - `round` — 四舍五入
> - `floor` — 地板，向下
> - `ceil` — 天花板，向上
> - `trunc` — 截断，不要小数

---

### Math.random()：随机数生成

`Math.random()` 是 JavaScript 中生成随机数的唯一内置方法。它返回一个**[0, 1) 区间的浮点数**，也就是大于等于 0，小于 1。

```javascript
console.log(Math.random()); // 0.123456789（每次运行结果不同）
console.log(Math.random()); // 0.987654321
console.log(Math.random()); // 0.555555555
```

但是 `[0, 1)` 能干什么用？我们需要的是各种范围的随机数！

#### 生成 [0, n) 区间的随机整数

```javascript
// 生成 [0, 10) 的随机整数
const randomInt = Math.floor(Math.random() * 10);
console.log(randomInt); // 0, 1, 2, ..., 9
```

**原理**：`Math.random() * 10` 得到 `[0, 10)`，再 `floor` 取整得到 `[0, 9]`。

#### 生成 [min, max) 区间的随机整数

```javascript
// 生成 [5, 15) 的随机整数
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

console.log(randomInt(5, 15)); // 5, 6, 7, ..., 14
```

#### 生成 [min, max] 区间的随机整数（包含两端）

```javascript
// 生成 [1, 6] 的随机整数（骰子）
function rollDice() {
  return Math.floor(Math.random() * 6) + 1;
}

console.log(rollDice()); // 1, 2, 3, 4, 5, 或 6
```

#### 生成随机布尔值

```javascript
function randomBoolean() {
  return Math.random() < 0.5;
}

console.log(randomBoolean()); // true 或 false
```

#### 从数组中随机选一个元素

```javascript
const fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"];

function randomPick(array) {
  return array[Math.floor(Math.random() * array.length)];
}

console.log(randomPick(fruits)); // 随机选一个水果
```

#### 生成随机字符串（随机ID、验证码等）

```javascript
// 生成指定长度的随机字符串
function randomString(length) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return result;
}

console.log(randomString(8));  // 例如："aB3xZ9k2"
console.log(randomString(16)); // 例如："K9mP2nL4qR5sT7uV"
```

> 💡 重要提示：`Math.random()` 生成的随机数**不是真正的随机数**，而是**伪随机数**——它们是通过算法生成的，看起来随机但实际上是可预测的。如果你要做安全相关的应用（如生成密码、令牌等），请使用 `crypto.getRandomValues()` 而不是 `Math.random()`！

```javascript
// 安全随机数（适合密码、令牌等场景）
const array = new Uint32Array(1);
crypto.getRandomValues(array);
console.log(array[0]); // 一个密码学安全的随机整数
```

---

### 极值与比较：abs / max / min

#### Math.abs — 绝对值

```javascript
console.log(Math.abs(-5));      // 5
console.log(Math.abs(5));       // 5
console.log(Math.abs(-Infinity)); // Infinity
console.log(Math.abs(NaN));     // NaN
```

#### Math.max — 最大值

```javascript
console.log(Math.max(1, 5, 3, 9, 2)); // 9
console.log(Math.max());               // -Infinity（没有参数）
console.log(Math.max(1, 'hello'));     // NaN（遇到非数字就 NaN）
```

如果要求数组中的最大值，可以用展开运算符：

```javascript
const numbers = [1, 5, 3, 9, 2];

console.log(Math.max(...numbers)); // 9
// 或者
console.log(Math.max.apply(null, numbers)); // 9（apply 的传统写法）
```

#### Math.min — 最小值

```javascript
console.log(Math.min(1, 5, 3, 9, 2)); // 1
console.log(Math.min());               // Infinity（与 max 相反）
```

#### 综合应用：数值范围限制

```javascript
// 把一个值限制在 [min, max] 范围内
function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

console.log(clamp(15, 0, 10));  // 10 — 超过上限，限制为10
console.log(clamp(-5, 0, 10));  // 0  — 超过下限，限制为0
console.log(clamp(7, 0, 10));   // 7  — 在范围内，保持不变
```

---

### 指数与对数：pow / sqrt / log / exp

#### Math.pow — 幂运算

```javascript
console.log(Math.pow(2, 3));   // 8 — 2的3次方
console.log(Math.pow(4, 0.5));  // 2 — 4的0.5次方（开平方）
console.log(Math.pow(2, -2));  // 0.25 — 2的-2次方
console.log(Math.pow(27, 1/3)); // 3 — 立方根
```

当然，ES6 引入了更简洁的 **运算符：

```javascript
console.log(2 ** 3);   // 8 — 等同于 Math.pow(2, 3)
console.log(4 ** 0.5); // 2 — 开平方
console.log(2 ** -2);  // 0.25
```

#### Math.sqrt — 平方根

```javascript
console.log(Math.sqrt(16));  // 4
console.log(Math.sqrt(2));   // 1.4142135623730951
console.log(Math.sqrt(-1));  // NaN（负数开平方）
console.log(Math.sqrt(9));   // 3
```

#### Math.log / Math.log10 / Math.log2 — 对数

```javascript
console.log(Math.log(Math.E));     // 1 — 自然对数（底数为 e）
console.log(Math.log(1));         // 0
console.log(Math.log10(100));      // 2 — 底数为10的对数
console.log(Math.log10(1000));     // 3
console.log(Math.log2(8));         // 3 — 底数为2的对数
console.log(Math.log2(1024));      // 10
```

> 💡 小技巧：换底公式——如果你需要计算任意底数的对数：
> ```javascript
> function logBase(x, base) {
>   return Math.log(x) / Math.log(base);
> }
>
> console.log(logBase(8, 2)); // 3
> ```

#### Math.exp — e 的幂

```javascript
console.log(Math.exp(1));      // 2.718281828459045（e^1 ≈ e）
console.log(Math.exp(0));      // 1
console.log(Math.exp(-1));     // 0.36787944117144233（1/e）
```

---

### 三角函数：sin / cos / tan

JavaScript 提供了完整的三角函数家族，不过记住，它们的参数是**弧度**而不是角度！

```javascript
// 角度转弧度
function toRadians(degrees) {
  return degrees * (Math.PI / 180);
}

console.log(Math.sin(toRadians(90)));  // 1
console.log(Math.cos(toRadians(0)));   // 1
console.log(Math.tan(toRadians(45)));  // 0.9999999999999999（≈1）
```

反向三角函数（知道 sin/cos/tan 的值，反求角度）：

```javascript
console.log(Math.asin(1));   // π/2（弧度）
console.log(Math.acos(1));   // 0
console.log(Math.atan(1));   // π/4（弧度）
```

还有一个常用的 `atan2`：

```javascript
// atan2(y, x) — 比 atan(y/x) 更准确的反正切
console.log(Math.atan2(1, 1)); // π/4（45度）
```

> 🎯 小应用：计算坐标系中两点的角度
> ```javascript
> function angleBetweenPoints(x1, y1, x2, y2) {
>   return Math.atan2(y2 - y1, x2 - x1);
> }
>
> console.log(angleBetweenPoints(0, 0, 1, 1)); // π/4（45度）

---

## 10.2 数值处理

### toFixed：保留小数位

`toFixed` 方法可以让你把数字格式化成**固定小数位**的字符串。这在处理金额、百分比等场景中非常有用。

```javascript
const num = 3.1415926;

console.log(num.toFixed(2));   // "3.14" — 保留两位小数
console.log(num.toFixed(4));   // "3.1416" — 保留四位小数
console.log(num.toFixed(0));   // "3" — 保留0位小数
console.log((123).toFixed(2)); // "123.00" — 整数也可以格式化
```

> ⚠️ 注意：`toFixed` 返回的是**字符串**，不是数字！

```javascript
const price = 19.9;
const discountedPrice = price * 0.8;

console.log(discountedPrice);         // 15.919999999999999（浮点数精度问题！）
console.log(discountedPrice.toFixed(2)); // "15.92"（字符串）
console.log(parseFloat(discountedPrice.toFixed(2))); // 15.92（转回数字）
```

> 💡 小技巧：如果你需要精确的浮点数计算，可以使用一些库如 `decimal.js` 或 `big.js`，因为 JavaScript 的原生浮点数运算有时候会有精度问题！

---

### toPrecision：有效数字

`toPrecision` 方法按照**有效数字**（significant figures）的数量来格式化数字。如果你学的是理工科，应该对"有效数字"这个概念不陌生。

```javascript
const num = 123.456;

console.log(num.toPrecision(3));  // "123" — 3位有效数字
console.log(num.toPrecision(5));  // "123.46" — 5位有效数字
console.log(num.toPrecision(1));  // "1e+2" — 科学计数法
console.log(num.toPrecision(8));  // "123.45600" — 不足的补零
```

`toFixed` vs `toPrecision` 对比：

```javascript
const num = 1.23456;

// toFixed：固定小数位
console.log(num.toFixed(2));    // "1.23"
console.log(num.toFixed(4));    // "1.2346"

// toPrecision：有效数字
console.log(num.toPrecision(3)); // "1.23"
console.log(num.toPrecision(5)); // "1.2346"
```

对于 `1.23456` 来说，`toFixed(2)` 和 `toPrecision(3)` 都得到 "1.23"，但对于 `123.456`：

```javascript
const num = 123.456;

console.log(num.toFixed(2));    // "123.46" — 固定小数位
console.log(num.toPrecision(3)); // "123" — 3位有效数字
```

---

### toExponential：科学计数法

`toExponential` 把数字转换成**科学计数法**的形式：

```javascript
const num = 123456;

console.log(num.toExponential());     // "1.23456e+5"
console.log(num.toExponential(2));     // "1.23e+5" — 指定小数位数
console.log((0.000123).toExponential(2)); // "1.23e-4"
```

这个方法在处理非常大或非常小的数字时很有用：

```javascript
const huge = 602000000000000000000000n; // 阿伏伽德罗常数（近似）
console.log(huge.toExponential(2));     // "6.02e+23"
```

---

### toString(radix)：进制转换

`toString` 方法可以把数字转换成**字符串**，并且支持指定**进制**（radix）。

```javascript
const num = 255;

console.log(num.toString());      // "255"（默认十进制）
console.log(num.toString(2));     // "11111111"（二进制）
console.log(num.toString(8));     // "377"（八进制）
console.log(num.toString(16));    // "ff"（十六进制）
console.log(num.toString(36));    // "73"（36进制，最大支持36）
```

进制转换的常见应用：

```javascript
// 十进制转二进制（用于理解位运算）
console.log((42).toString(2));   // "101010"

// 十进制转十六进制（颜色代码）
console.log((255).toString(16)); // "ff"
console.log((168).toString(16)); // "a8"

// RGB 转十六进制颜色
function rgbToHex(r, g, b) {
  return "#" + [r, g, b]
    .map(x => x.toString(16).padStart(2, '0'))
    .join('');
}

console.log(rgbToHex(255, 128, 0)); // "#ff8000"
```

反过来（字符串转数字），可以用 `parseInt` 并指定进制：

```javascript
console.log(parseInt("11111111", 2));   // 255（二进制转十进制）
console.log(parseInt("ff", 16));         // 255（十六进制转十进制）
console.log(parseInt("377", 8));         // 255（八进制转十进制）
console.log(parseInt("73", 36));         // 255（36进制转十进制）
```

> 💡 小技巧：二进制、八进制、十六进制的字面量表示法：
> ```javascript
> // 二进制：0b 开头
> console.log(0b11111111); // 255
>
> // 八进制：0o 开头（注意是字母 o，不是数字0）
> console.log(0o377);      // 255
>
> // 十六进制：0x 开头
> console.log(0xff);       // 255
> ```

---

### isFinite vs Number.isFinite：全局函数 vs 方法的区别

这是一个很容易搞混的点！JavaScript 有两套判断"是否是有限数字"的函数：

```javascript
// 全局函数
console.log(isFinite(100));      // true
console.log(isFinite(Infinity));  // false
console.log(isFinite(NaN));       // false
console.log(isFinite("100"));     // true（会做类型转换，"100" → 100）

// Number 静态方法
console.log(Number.isFinite(100));      // true
console.log(Number.isFinite(Infinity));  // false
console.log(Number.isFinite(NaN));       // false
console.log(Number.isFinite("100"));     // false（不会类型转换！）
```

**关键区别**：
- `isFinite` 全局函数：**会进行类型转换**——如果参数不是数字，会先尝试转换成数字
- `Number.isFinite` 方法：**不做类型转换**——只有当参数本身是有限数字时才返回 true

所以如果你确定参数一定是数字，用哪个都行；但如果参数可能是字符串等类型，想要精确判断，用 `Number.isFinite` 更安全：

```javascript
function safeDivide(a, b) {
  if (!Number.isFinite(a) || !Number.isFinite(b)) {
    throw new Error("参数必须是有限数字");
  }
  return a / b;
}

console.log(safeDivide(10, 2));     // 5
console.log(safeDivide("10", 2));   // 抛出错误！（字符串不是数字）
```

---

### isNaN vs Number.isNaN：全局函数 vs 方法的区别

和 `isFinite` 的情况一模一样！

```javascript
// 全局函数
console.log(isNaN(NaN));       // true
console.log(isNaN(100));        // false
console.log(isNaN("hello"));   // true（强制转换，"hello" → NaN）
console.log(isNaN({}));        // true（{} → NaN）
console.log(isNaN("100"));     // false（"100" → 100，不是 NaN）

// Number 静态方法
console.log(Number.isNaN(NaN));      // true
console.log(Number.isNaN(100));       // false
console.log(Number.isNaN("hello"));   // false（不做类型转换！）
console.log(Number.isNaN({}));       // false（不做类型转换！）
console.log(Number.isNaN("100"));    // false
```

> ⚠️ `isNaN("hello")` 返回 true，这经常让人困惑！因为 `"hello"` 确实"不是一个数字"。但 `Number.isNaN("hello")` 返回 false，因为 `"hello"` 本身根本就不是 `NaN`，它只是"不是数字"而已——这两个概念是不同的！

**如何记住**：
- `isNaN(x)` = "x is Not-a-Number?" = "x 是NaN吗？"（但实际是"x 转换后是NaN吗？"）
- `Number.isNaN(x)` = "x 严格是 NaN 吗？"

推荐：**始终使用 `Number.isNaN`**，除非你有特殊需求。

---

### Number() / parseInt() / parseFloat() 对比

这三个函数都可以把字符串转换成数字，但它们各有特点：

```javascript
// Number() — 严格转换，整个字符串必须是有效的数字
console.log(Number("123"));       // 123
console.log(Number("123.45"));   // 123.45
console.log(Number("  123  "));  // 123（忽略前后空格）
console.log(Number("123abc"));   // NaN（包含非法字符）
console.log(Number("0xff"));     // 255（支持十六进制）
console.log(Number(""));         // 0（空字符串变成0）
console.log(Number(true));       // 1
console.log(Number(false));      // 0

// parseInt() — 从左到右解析，遇到非法字符停止
console.log(parseInt("123"));        // 123
console.log(parseInt("123.45"));     // 123（小数部分被截断）
console.log(parseInt("123abc"));     // 123（后面的被忽略）
console.log(parseInt("  42px"));     // 42（忽略空格和单位）
console.log(parseInt("0xff"));       // 255（支持十六进制）
console.log(parseInt("123", 16));    // 291（指定进制）

// parseFloat() — 从左到右解析，保留小数
console.log(parseFloat("123"));        // 123
console.log(parseFloat("123.45"));     // 123.45
console.log(parseFloat("123.45.67"));  // 123.45（第二个小数点后被忽略）
console.log(parseFloat("3.14m/s"));   // 3.14
console.log(parseFloat("0.00001"));    // 0.00001（不会变成科学计数法）
```

**使用场景对比**：

| 函数 | 适用场景 | 特点 |
|------|---------|------|
| `Number()` | 严格转换，需要整个字符串都是数字 | 最严格，空字符串变0 |
| `parseInt()` | 解析带单位的整数（如 "42px"、"16px"） | 从头解析，忽略末尾 |
| `parseFloat()` | 解析带单位的小数（如 "3.14rem"） | 保留第一个小数点 |

```javascript
// 实际应用示例
console.log(parseInt("100px", 10));   // 100（从样式值中提取数字）
console.log(parseFloat("3.5em"));      // 3.5
console.log(parseInt("Hello123"));      // NaN（完全没有数字）
console.log(Number("Hello123"));        // NaN

// 判断是否是有效数字（最安全的方式）
function isNumeric(value) {
  return !isNaN(value) && !isNaN(parseFloat(value));
}

console.log(isNumeric("123"));    // true
console.log(isNumeric("123.45")); // true
console.log(isNumeric("123abc")); // false
```

---

## 本章小结

本章我们探索了 JavaScript 的数学工具箱：

1. **Math 对象**：这个工具箱提供了大量数学函数，包括取整（`round`/`floor`/`ceil`/`trunc`）、随机数（`random`）、极值（`max`/`min`/`abs`）、指数对数（`pow`/`sqrt`/`log`）、三角函数（`sin`/`cos`/`tan`）等。

2. **数值处理**：`toFixed` 保留小数位，`toPrecision` 按有效数字格式化，`toExponential` 科学计数法，`toString(radix)` 进制转换。

3. **全局函数 vs Number 方法**：`isFinite` vs `Number.isFinite`、`isNaN` vs `Number.isNaN`——关键区别在于是否做类型转换。**推荐始终使用 Number 静态方法版本**。

4. **类型转换函数**：`Number()`、`parseInt()`、`parseFloat()` 三兄弟各有特点：`Number()` 最严格，`parseInt()` 适合带单位的整数，`parseFloat()` 适合带单位的小数。

> 📊 图示：Math 对象方法分类
>
> ```mermaid
> graph TD
>     A[Math 对象] --> B[取整函数]
>     A --> C[随机与极值]
>     A --> D[指数与对数]
>     A --> E[三角函数]
>     A --> F[其他常量]
>
>     B --> B1[round 四舍五入]
>     B --> B2[floor 向下]
>     B --> B3[ceil 向上]
>     B --> B4[trunc 截断]
>
>     C --> C1[random 随机数]
>     C --> C2[max 最大值]
>     C --> C3[min 最小值]
>     C --> C4[abs 绝对值]
>
>     D --> D1[pow 幂运算]
>     D --> D2[sqrt 平方根]
>     D --> D3[log 对数]
>     D --> D4[exp e的幂]
>
>     E --> E1[sin 正弦]
>     E --> E2[cos 余弦]
>     E --> E3[tan 正切]
>     E --> E4[atan 反切]
>
>     F --> F1[PI 圆周率]
>     F --> F2[E 自然常数]
>     F --> F3[SQRT2 √2]
>     F --> F4[LN2 ln2]
---

**下章预告**：下一章我们将进入**函数**的世界——函数声明、函数表达式、箭头函数、参数传递、返回值...准备好了吗？ 🔥
