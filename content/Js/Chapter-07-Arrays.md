+++
title = "第 7 章 数组"
weight = 70
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 7 章 数组

如果说变量是一个「盒子」，那数组就是一条「走廊」——可以装下多个值，按顺序排列。数组是 JavaScript 中最重要的数据结构之一，也是你写代码时最常用到的工具。

## 7.1 数组基础

### 数组的概念与创建方式

数组（Array）是一组有序的元素集合。每个元素都有一个索引（从 0 开始），就像房间号一样。

```javascript
// 数组是什么？
// 普通变量：一个盒子装一个值
let name = "张三";

// 数组：一条走廊装多个值
let names = ["张三", "李四", "王五", "赵六"];
// 索引:        0       1       2       3

console.log(names); // ["张三", "李四", "王五", "赵六"]
console.log(names[0]); // "张三"（第一个元素）
console.log(names[1]); // "李四"（第二个元素）
console.log(names[3]); // "赵六"（第四个元素）
console.log(names.length); // 4（数组长度）
```

### 字面量[] vs new Array() vs Array.of() vs Array.from()

JavaScript 提供了多种创建数组的方式，每种都有其适用场景。

```javascript
// 方式1：数组字面量（最常用）
const arr1 = [1, 2, 3, 4, 5];
console.log(arr1); // [1, 2, 3, 4, 5]
console.log(typeof arr1); // "object"（数组的 typeof 是 "object"！）

// 方式2：new Array()（不推荐）
const arr2 = new Array(1, 2, 3, 4, 5);
console.log(arr2); // [1, 2, 3, 4, 5]

// new Array() 的坑：单个数字参数表示数组长度！
const arr3 = new Array(5); // 创建一个长度为5的空数组
console.log(arr3.length); // 5
console.log(arr3); // [empty × 5]（5个空位，不是5个0！）
```

```javascript
// 方式3：Array.of()（解决 new Array() 的参数歧义）
const arr4 = Array.of(5); // 创建一个只包含5的数组
console.log(arr4); // [5]
console.log(arr4.length); // 1

const arr5 = Array.of(1, 2, 3);
console.log(arr5); // [1, 2, 3]

// 对比
console.log(new Array(5));   // [empty × 5]（5个空位）
console.log(Array.of(5));    // [5]（一个元素，值是5）
console.log(new Array(5, 2)); // [5, 2]（两个元素）
console.log(Array.of(5, 2)); // [5, 2]（两个元素）
```

```javascript
// 方式4：Array.from()（将类数组对象或可迭代对象转成数组）
// 示例1：将 arguments 转成数组
function sum() {
    const args = Array.from(arguments);
    return args.reduce((a, b) => a + b, 0);
}
console.log(sum(1, 2, 3, 4, 5)); // 15

// 示例2：将 NodeList 转成数组
// const divs = document.querySelectorAll('div');
// const divArray = Array.from(divs);

// 示例3：将字符串转成数组
console.log(Array.from("hello")); // ["h", "e", "l", "l", "o"]

// 示例4：Array.from() 第二个参数（映射函数）
console.log(Array.from([1, 2, 3], x => x * 2)); // [2, 4, 6]
console.log(Array.from("123", Number)); // [1, 2, 3]
```

### Array.of vs new Array 的行为差异

| 特性 | `new Array(5)` | `Array.of(5)` |
|------|---------------|---------------|
| 参数 | 5 | 5 |
| 结果 | 长度为5的空数组 | 只包含5的数组 |
| 长度 | 5 | 1 |

```javascript
// 记忆技巧：
// new Array(n) - n 可能是长度，也可能是元素，容易混淆
// Array.of(n) - of 就是"包含"的意思，参数一定是元素

// 建议：始终用数组字面量 [] 或 Array.of()
const arr1 = [5];           // 推荐
const arr2 = Array.of(5);    // 推荐
const arr3 = new Array(5);   // 慎用！
```

### Array.from：类数组对象或可迭代对象转数组

```javascript
// 类数组对象：有 length 属性和索引访问，但没有数组方法
const arrayLike = {
    0: "a",
    1: "b",
    2: "c",
    length: 3
};

console.log(Array.from(arrayLike)); // ["a", "b", "c"]
```

```javascript
// 字符串也是可迭代对象
console.log(Array.from("hello")); // ["h", "e", "l", "l", "o"]

// Set 和 Map 也是可迭代对象
const set = new Set([1, 2, 3]);
console.log(Array.from(set)); // [1, 2, 3]

const map = new Map([[1, "one"], [2, "two"]]);
console.log(Array.from(map)); // [[1, "one"], [2, "two"]]
```

```javascript
// Array.from 的映射功能
console.log(Array.from([1, 2, 3], x => x * x)); // [1, 4, 9]
console.log(Array.from([1, 2, 3], x => x + "!")); // ["1!", "2!", "3!"]

// 实际应用：创建指定范围的数组
function range(start, end) {
    return Array.from({ length: end - start }, (_, i) => start + i);
}
console.log(range(1, 6)); // [1, 2, 3, 4, 5]
console.log(range(5, 10)); // [5, 6, 7, 8, 9]
```

### 访问与修改：arr[index]

```javascript
// 访问数组元素
const fruits = ["苹果", "香蕉", "橙子", "葡萄"];
console.log(fruits[0]); // "苹果"
console.log(fruits[1]); // "香蕉"
console.log(fruits[2]); // "橙子"
console.log(fruits[3]); // "葡萄"

// 访问越界：返回 undefined
console.log(fruits[10]); // undefined
console.log(fruits[-1]); // undefined（负数索引不支持）

// 修改数组元素
fruits[1] = "草莓";
console.log(fruits); // ["苹果", "草莓", "橙子", "葡萄"]

// 添加元素（超过当前长度）
fruits[10] = "西瓜";
console.log(fruits.length); // 11（数组自动扩展）
console.log(fruits[4]); // undefined（中间的空位）
console.log(fruits[10]); // "西瓜"
```

### 数组空位（稀疏数组）的处理

```javascript
// 创建稀疏数组
const sparse = [1, , 3, , 5];
console.log(sparse); // [1, empty, 3, empty, 5]
console.log(sparse.length); // 5
console.log(sparse[1]); // undefined（空位）
console.log(0 in sparse); // true（索引0存在，值为1）
console.log(1 in sparse); // false（索引1是空位）
console.log(2 in sparse); // true（索引2存在，值为3）
```

```javascript
// 稀疏数组的遍历
const sparseArr = [1, , 3];
for (let i = 0; i < sparseArr.length; i++) {
    console.log(`sparseArr[${i}] =`, sparseArr[i]);
}
// sparseArr[0] = 1
// sparseArr[1] = undefined
// sparseArr[2] = 3

// forEach 会跳过空位
sparseArr.forEach((val, idx) => {
    console.log(`forEach: sparseArr[${idx}] =`, val);
});
// forEach: sparseArr[0] = 1
// forEach: sparseArr[2] = 3

// map 会跳过空位，但保留结果
const mapped = sparseArr.map(x => x * 2);
console.log(mapped); // [2, empty, 6]

// filter 会跳过空位
console.log(sparseArr.filter(x => true)); // [1, 3]

// join 会将空位当作空字符串
console.log(sparseArr.join("-")); // "1--3"
```

```javascript
// 避免稀疏数组：用 Array.from() 或 fill()
const dense = Array.from({ length: 5 }); // [undefined, undefined, undefined, undefined, undefined]
console.log(dense.map((_, i) => i)); // [0, 1, 2, 3, 4]

// fill() 方法填充数组
const filled = new Array(5).fill(0);
console.log(filled); // [0, 0, 0, 0, 0]
```

### 伪数组（类数组对象）

类数组对象看起来像数组（有数字索引和 length），但不是真正的数组（没有数组方法）。

```javascript
// 常见的类数组对象：arguments
function printArgs() {
    console.log("类型:", typeof arguments); // "object"
    console.log("长度:", arguments.length); // 3
    console.log("第一个:", arguments[0]);   // "a"

    // arguments 不是数组，不能直接用数组方法
    // arguments.map(x => x); // TypeError!

    // 解决方案：转成数组
    const argsArray = Array.from(arguments);
    console.log(argsArray.map(x => x)); // ["a", "b", "c"]
}

printArgs("a", "b", "c");
```

```javascript
// 常见的类数组对象：NodeList（DOM查询结果）
// const divs = document.querySelectorAll('div');
// console.log(divs.length);
// console.log(divs[0]);
// divs.map(div => div.style); // TypeError!

// 解决方案
// const divsArray = Array.from(divs);
// const divsArray = [...divs]; // 展开运算符
```

```javascript
// 字符串也是类数组
const str = "hello";
console.log(str.length); // 5
console.log(str[0]); // "h"
console.log(Array.from(str)); // ["h", "e", "l", "l", "o"]
```

```javascript
// 数组方法的借用：让类数组使用数组方法
function sum() {
    // 方法1：Array.from()
    // return Array.from(arguments).reduce((a, b) => a + b, 0);

    // 方法2：展开运算符
    // return [...arguments].reduce((a, b) => a + b, 0);

    // 方法3：借用 slice + call
    // return Array.prototype.slice.call(arguments).reduce((a, b) => a + b, 0);

    // 方法4：借用 Array.prototype.reduce.call
    return Array.prototype.reduce.call(arguments, (a, b) => a + b, 0);
}

console.log(sum(1, 2, 3, 4, 5)); // 15
```


## 7.2 数组遍历

遍历是数组最常见的操作之一。JavaScript 提供了多种遍历方式，每种都有其特点和适用场景。

### for 循环遍历

最传统的方式，通过索引遍历。

```javascript
const fruits = ["苹果", "香蕉", "橙子", "葡萄"];

// 基本 for 循环
for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}

// 倒序遍历
for (let i = fruits.length - 1; i >= 0; i--) {
    console.log(fruits[i]);
}

// 步长遍历（每隔2个取一个）
for (let i = 0; i < fruits.length; i += 2) {
    console.log(fruits[i]);
}
```

### for...in：遍历对象可枚举属性

`for...in` 主要用于遍历对象的属性，但在数组上也能用——但**不推荐**！

```javascript
const fruits = ["苹果", "香蕉", "橙子"];

for (const index in fruits) {
    console.log(`索引 ${index}: ${fruits[index]}`);
}

// 输出：
// 索引 0: 苹果
// 索引 1: 香蕉
// 索引 2: 橙子
```

```javascript
// for...in 的问题：会遍历到自定义属性
const sparse = [1, , 3];
sparse.customProp = "自定义属性";

for (const key in sparse) {
    console.log(`${key}: ${sparse[key]}`);
}
// 输出：
// 0: 1
// 1: undefined
// 2: 3
// customProp: 自定义属性（这个不应该出现！）
```

```javascript
// for...in 的特点
// 1. 遍历的是键名（索引），不是值
// 2. 会遍历原型链上的属性
// 3. 遍历顺序不保证是数字顺序
// 4. 会遍历空位（返回 undefined）

// 结论：遍历数组不要用 for...in，用 for 或 for...of
```

### for...of（ES6+）：遍历可迭代对象，比 forEach 更灵活

`for...of` 是 ES6 引入的，专门用于遍历可迭代对象，是遍历数组的最佳选择之一。

```javascript
const fruits = ["苹果", "香蕉", "橙子", "葡萄"];

// 基本用法
for (const fruit of fruits) {
    console.log(fruit);
}

// 输出：
// 苹果
// 香蕉
// 橙子
// 葡萄
```

```javascript
// 同时获取索引和值：entries()
for (const [index, fruit] of fruits.entries()) {
    console.log(`第 ${index + 1} 个水果: ${fruit}`);
}

// 输出：
// 第 1 个水果: 苹果
// 第 2 个水果: 香蕉
// 第 3 个水果: 橙子
// 第 4 个水果: 葡萄
```

```javascript
// for...of 的优点
// 1. 直接遍历值，不需要通过索引
// 2. 可以用 break/continue 控制循环
// 3. 不会遍历到原型链上的属性
// 4. 语义清晰，不容易出错

// for...of vs for 循环
// for 循环：需要索引时用
for (let i = 0; i < fruits.length; i++) {
    console.log(`${i}: ${fruits[i]}`);
}

// for...of：只需要值时用
for (const fruit of fruits) {
    console.log(fruit);
}
```

```javascript
// for...of 可以用 break 和 continue
let found = false;
for (const fruit of fruits) {
    if (fruit === "橙子") {
        console.log("找到橙子了！");
        found = true;
        break; // 找到就退出，不用继续找
    }
}
if (!found) {
    console.log("没找到");
}

console.log("\n跳过某些元素：");
for (const fruit of fruits) {
    if (fruit === "香蕉") {
        continue; // 跳过香蕉
    }
    console.log(fruit);
}
```

### forEach：数组专用遍历，不支持 break

`forEach` 是数组方法，比 `for...of` 更简洁，但**不能用 break 中断**。

```javascript
const numbers = [1, 2, 3, 4, 5];

numbers.forEach(function(number, index, array) {
    console.log(`numbers[${index}] = ${number}`);
});

// 输出：
// numbers[0] = 1
// numbers[1] = 2
// numbers[2] = 3
// numbers[3] = 4
// numbers[4] = 5
```

```javascript
// 使用箭头函数更简洁
numbers.forEach((num, idx) => {
    console.log(`${idx}: ${num}`);
});

// 只有一个参数时可以省略括号
numbers.forEach(num => {
    console.log(num);
});
```

```javascript
// forEach 的特点
// 1. 回调函数有三个参数：当前值、索引、原数组
// 2. 不支持 break/continue
// 3. 不能用 return 提前退出（return 只是跳过本次回调）
// 4. 无法用 forEach 模拟 filter 的效果

// try-catch 模拟 break（不推荐）
try {
    numbers.forEach(num => {
        if (num === 3) throw new Error("找到3，退出");
        console.log(num);
    });
} catch (e) {
    if (e.message !== "找到3，退出") throw e;
}
```

```javascript
// forEach vs for...of vs for 循环
const arr = [1, 2, 3];

// for 循环
for (let i = 0; i < arr.length; i++) {
    // 可以用 break/continue
    // 需要索引时用
}

// for...of
for (const val of arr) {
    // 可以用 break/continue
    // 只需要值时用，更简洁
}

// forEach
arr.forEach((val, idx) => {
    // 简洁，但不能 break/continue
    // 适合不需要控制流程的场景
});
```

### for vs for...in vs for...of vs forEach 对比

| 特性 | for | for...in | for...of | forEach |
|------|-----|---------|---------|---------|
| 遍历内容 | 任意 | 键名 | 值 | 值 |
| 数组适用性 | ✅ | ⚠️ 不推荐 | ✅ 推荐 | ✅ |
| 支持 break/continue | ✅ | ✅ | ✅ | ❌ |
| 遍历顺序 | 按索引 | 不保证 | 按顺序 | 按顺序 |
| 遍历空位 | ✅ | undefined | 跳过 | 跳过 |
| 遍历原型属性 | ❌ | ✅（会遍历） | ❌ | ❌ |

```javascript
// 推荐选择
// 1. 只需要遍历值：for...of
for (const item of items) {
    console.log(item);
}

// 2. 需要索引：for 循环 或 for...of + entries()
for (let i = 0; i < items.length; i++) {
    console.log(i, items[i]);
}

// 或
for (const [i, item] of items.entries()) {
    console.log(i, item);
}

// 3. 需要执行副作用，不需要控制流程：forEach
items.forEach(item => {
    console.log(item);
});
```

### 用 let 替代 var 解决循环变量闭包问题

这是一个经典的 JavaScript 面试题，也是一个常见的 bug 来源。

```javascript
// 问题：用 var 声明循环变量，所有回调共享同一个变量
const funcs = [];

for (var i = 0; i < 3; i++) {
    funcs.push(function() {
        console.log(i); // 期望：0, 1, 2；实际：3, 3, 3
    });
}

funcs.forEach(f => f()); // 输出：3, 3, 3（而不是 0, 1, 2！）
```

```javascript
// 原因分析
// var i 是函数作用域，不是块级作用域
// 循环结束后，i 变成了 3
// 所有回调函数访问的都是同一个 i（值为 3）

// 图示：
// i = 0 -> funcs[0] 保存了函数，函数引用 i
// i = 1 -> funcs[1] 保存了函数，函数引用 i
// i = 2 -> funcs[2] 保存了函数，函数引用 i
// i = 3 -> 循环结束，i 变成 3
// 执行 funcs[0]()：打印 i，发现 i 是 3
// 执行 funcs[1]()：打印 i，发现 i 是 3
// 执行 funcs[2]()：打印 i，发现 i 是 3
```

```javascript
// 解决方案1：用 let 替代 var（ES6+）
const funcs1 = [];

for (let i = 0; i < 3; i++) {
    funcs1.push(function() {
        console.log(i); // 现在 i 是块级作用域，每次迭代都是新变量
    });
}

funcs1.forEach(f => f()); // 输出：0, 1, 2（正确！）

// 为什么 let 可以？
// let 是块级作用域
// 每次循环迭代都会创建新的 i
// 回调函数捕获的是各自迭代的 i
```

```javascript
// 解决方案2：用立即执行函数（IIFE）创建闭包（旧方法）
const funcs2 = [];

for (var i = 0; i < 3; i++) {
    funcs2.push((function(index) {
        return function() {
            console.log(index);
        };
    })(i)); // 立即执行，传入当前 i 的值
}

funcs2.forEach(f => f()); // 输出：0, 1, 2

// 图示：
// i = 0: IIFE 执行，index = 0，返回函数捕获 index = 0
// i = 1: IIFE 执行，index = 1，返回函数捕获 index = 1
// i = 2: IIFE 执行，index = 2，返回函数捕获 index = 2
```

```javascript
// 解决方案3：用 forEach（最简洁）
const funcs3 = [];

[0, 1, 2].forEach(function(i) {
    funcs3.push(function() {
        console.log(i);
    });
});

funcs3.forEach(f => f()); // 输出：0, 1, 2

// forEach 每次迭代都会创建新的 i，所以没问题
```

```javascript
// 解决方案4：用 bind（不常用）
const funcs4 = [];

for (var i = 0; i < 3; i++) {
    funcs4.push(console.log.bind(null, i));
}

funcs4.forEach(f => f()); // 输出：0, 1, 2

```

## 7.3 可迭代对象

可迭代对象是 ES6 引入的概念。如果你理解了可迭代对象，就能理解 `for...of`、展开运算符、`Array.from()` 等的工作原理。

### 内置可迭代对象：Array / String / Map / Set / NodeList / arguments

ES6 规定，只要对象实现了**迭代器协议**，就是可迭代对象。以下是常见的内置可迭代对象：

```javascript
// 数组
const arr = [1, 2, 3];
console.log(typeof arr[Symbol.iterator]); // "function"（数组有迭代器）
for (const item of arr) {
    console.log(item); // 1, 2, 3
}

// 字符串
const str = "hello";
for (const char of str) {
    console.log(char); // h, e, l, l, o
}

// Map
const map = new Map([["a", 1], ["b", 2]]);
for (const [key, value] of map) {
    console.log(`${key}: ${value}`); // a: 1, b: 2
}

// Set
const set = new Set([1, 2, 3]);
for (const item of set) {
    console.log(item); // 1, 2, 3
}

// NodeList（DOM）
// const divs = document.querySelectorAll('div');
// for (const div of divs) {
//     console.log(div); // 每个 div 元素
// }

// arguments
function printArgs() {
    for (const arg of arguments) {
        console.log(arg);
    }
}
printArgs("a", "b", "c"); // a, b, c
```

### Symbol.iterator：自定义迭代器

每个可迭代对象都有一个 `Symbol.iterator` 方法，调用它返回一个迭代器。

```javascript
// 获取数组的迭代器
const arr = [1, 2, 3];
const iterator = arr[Symbol.iterator]();

console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }
console.log(iterator.next()); // { value: 3, done: false }
console.log(iterator.next()); // { value: undefined, done: true }
```

### 迭代器协议与生成器

迭代器协议规定：对象有一个 `next()` 方法，返回 `{ value, done }` 形式的对象。

```javascript
// 自定义一个简易迭代器：返回一个范围
function makeRangeIterator(start = 0, end = Infinity, step = 1) {
    let nextStart = start;
    let iterationCount = 0;

    const rangeIterator = {
        next: function() {
            let result;
            if (nextStart < end) {
                result = { value: nextStart, done: false };
                nextStart += step;
                iterationCount++;
                return result;
            }
            return { value: iterationCount, done: true };
        }
    };
    return rangeIterator;
}

const it = makeRangeIterator(1, 5);
let result = it.next();
while (!result.done) {
    console.log(result.value); // 1, 2, 3, 4
    result = it.next();
}
console.log("迭代次数:", result.value); // 4
```

### for...of 遍历数组迭代器

```javascript
const arr = ["a", "b", "c"];

// 获取数组的默认迭代器
const iter = arr[Symbol.iterator]();
console.log(iter.next()); // { value: "a", done: false }
console.log(iter.next()); // { value: "b", done: false }
console.log(iter.next()); // { value: "c", done: false }
console.log(iter.next()); // { value: undefined, done: true }

// for...of 就是用迭代器遍历的语法糖
```

### entries / keys / values 迭代器

数组提供了三个方法返回不同的迭代器：

```javascript
const fruits = ["苹果", "香蕉", "橙子"];

// entries()：返回键值对的迭代器
for (const [index, fruit] of fruits.entries()) {
    console.log(`${index}: ${fruit}`);
}
// 0: 苹果
// 1: 香蕉
// 2: 橙子

// keys()：返回键的迭代器
for (const index of fruits.keys()) {
    console.log(index);
}
// 0, 1, 2

// values()：返回值的迭代器
for (const fruit of fruits.values()) {
    console.log(fruit);
}
// 苹果, 香蕉, 橙子
```

```javascript
// 迭代器转数组
const arr = [1, 2, 3];
const iter = arr.values();

// 方法1：Array.from
const arr1 = Array.from(iter);
console.log(arr1); // [1, 2, 3]

// 方法2：展开运算符
const arr2 = [...arr.values()];
console.log(arr2); // [1, 2, 3]

// 方法3：手动遍历
const arr3 = [];
let result;
while (!(result = arr.values().next()).done) {
    arr3.push(result.value);
}

console.log(arr3); // [1, 2, 3]

## 7.4 增删操作

数组的增删操作是日常开发中使用频率最高的操作之一。JavaScript 数组提供了丰富的增删方法。

### push / pop：末尾添加 / 删除

```javascript
const arr = [1, 2, 3];

// push：向数组末尾添加一个或多个元素，返回新长度
const newLength = arr.push(4, 5);
console.log(arr);        // [1, 2, 3, 4, 5]
console.log(newLength);  // 5

// pop：删除数组末尾最后一个元素，返回被删除的元素
const popped = arr.pop();
console.log(arr);   // [1, 2, 3, 4]
console.log(popped); // 5

// push 和 pop 结合使用：实现栈（后进先出）
const stack = [];
stack.push(1);  // 入栈
stack.push(2);
stack.push(3);
console.log(stack); // [1, 2, 3]

const top = stack.pop(); // 出栈
console.log(top);     // 3
console.log(stack);   // [1, 2]
```

### unshift / shift：开头添加 / 删除

```javascript
const arr = [3, 4, 5];

// unshift：向数组开头添加一个或多个元素，返回新长度
const newLength = arr.unshift(1, 2);
console.log(arr);        // [1, 2, 3, 4, 5]
console.log(newLength);   // 5

// shift：删除数组开头第一个元素，返回被删除的元素
const shifted = arr.shift();
console.log(arr);     // [2, 3, 4, 5]
console.log(shifted);  // 1

// unshift 和 shift 结合使用：实现队列（先进先出）
const queue = [];
queue.push(1);  // 入队
queue.push(2);
queue.push(3);
console.log(queue); // [1, 2, 3]

const front = queue.shift(); // 出队
console.log(front);    // 1
console.log(queue);    // [2, 3]
```

### splice：万能方法（添加 / 删除 / 替换）

`splice` 是数组最强大的方法，可以同时完成添加、删除和替换操作。

```javascript
const arr = ["a", "b", "c", "d", "e"];

// splice(start, deleteCount, ...items)
// start: 开始位置
// deleteCount: 删除数量（0 表示不删除）
// ...items: 要插入的项

// 删除：splice(起始位置, 删除数量)
const removed1 = arr.splice(1, 2); // 从索引1开始，删除2个
console.log(arr);      // ["a", "d", "e"]
console.log(removed1); // ["b", "c"]

// 插入：splice(起始位置, 0, 要插入的项)
const arr2 = ["a", "b", "c"];
arr2.splice(1, 0, "x", "y"); // 在索引1处插入，不删除
console.log(arr2); // ["a", "x", "y", "b", "c"]

// 替换：splice(起始位置, 删除数量, 要插入的项)
const arr3 = ["a", "b", "c", "d"];
arr3.splice(1, 2, "x", "y"); // 从索引1开始，删除2个，插入2个
console.log(arr3); // ["a", "x", "y", "d"]
```

```javascript
// 实用示例：移除数组中的某个元素
function removeItem(arr, item) {
    const index = arr.indexOf(item);
    if (index !== -1) {
        arr.splice(index, 1); // 找到就删除一个
        return true;
    }
    return false;
}

const nums = [1, 2, 3, 4, 3, 5];
removeItem(nums, 3);
console.log(nums); // [1, 2, 4, 3, 5]（只删除了第一个3）

// 移除所有出现的元素
function removeAllItems(arr, item) {
    return arr.filter(x => x !== item);
}

const nums2 = [1, 2, 3, 4, 3, 5];
const filtered = removeAllItems(nums2, 3);
console.log(filtered); // [1, 2, 4, 5]
```

```javascript
// 实用示例：在数组中间插入元素
function insertAt(arr, index, ...items) {
    arr.splice(index, 0, ...items);
}

const arr = ["a", "b", "c", "d"];
insertAt(arr, 2, "x", "y", "z");
console.log(arr); // ["a", "b", "x", "y", "z", "c", "d"]
```

```javascript
// splice 的注意事项：会修改原数组
// 如果不想修改原数组，先复制一份
const original = [1, 2, 3, 4, 5];
const modified = [...original];
modified.splice(1, 2);
console.log(original); // [1, 2, 3, 4, 5]（原数组不变）
console.log(modified); // [1, 4, 5]
```


## 7.5 查询与索引

数组的查询方法让你快速找到想要的数据。

### indexOf / lastIndexOf：查找元素

```javascript
const fruits = ["苹果", "香蕉", "橙子", "香蕉", "葡萄"];

// indexOf：返回元素第一次出现的索引，没找到返回 -1
console.log(fruits.indexOf("香蕉"));  // 1
console.log(fruits.indexOf("草莓"));  // -1（没找到）
console.log(fruits.indexOf("苹果"));  // 0

// lastIndexOf：返回元素最后一次出现的索引
console.log(fruits.lastIndexOf("香蕉"));  // 3（从后面数第1个）
console.log(fruits.lastIndexOf("苹果"));  // 0

// 第二个参数：从指定位置开始搜索
console.log(fruits.indexOf("香蕉", 2));  // 3（从索引2开始找香蕉）
```

### includes：判断是否包含

ES6 新增的 `includes` 方法，比 `indexOf` 更语义化，且能正确处理 `NaN`。

```javascript
const arr = [1, 2, 3, NaN, 5];

// indexOf 不能正确处理 NaN
console.log(arr.indexOf(NaN)); // -1（找不到！）

// includes 可以正确处理 NaN
console.log(arr.includes(NaN)); // true

// 基本用法
console.log(arr.includes(3)); // true
console.log(arr.includes(4)); // false

// 第二个参数：起始位置
console.log(arr.includes(2, 2)); // false（从索引2开始找2，找不到）
console.log(arr.includes(2, 1)); // true（从索引1开始找2，找得到）
```

### find / findIndex / findLast / findLastIndex：返回满足条件的元素

ES6 新增的查找方法，接受一个回调函数作为参数。

```javascript
const users = [
    { id: 1, name: "张三", age: 25 },
    { id: 2, name: "李四", age: 30 },
    { id: 3, name: "王五", age: 35 },
    { id: 4, name: "赵六", age: 30 }
];

// find：返回第一个满足条件的元素，没找到返回 undefined
const user1 = users.find(user => user.age === 30);
console.log(user1); // { id: 2, name: "李四", age: 30 }

const user2 = users.find(user => user.age === 20);
console.log(user2); // undefined（没找到）

// findIndex：返回第一个满足条件的元素索引，没找到返回 -1
const index1 = users.findIndex(user => user.age === 30);
console.log(index1); // 1

const index2 = users.findIndex(user => user.age === 20);
console.log(index2); // -1（没找到）
```

```javascript
// findLast / findLastIndex（ES2023）：从后往前找
const arr = [1, 2, 3, 2, 1];

const lastTwo = arr.findLast(x => x === 2);
console.log(lastTwo); // 2（从后往前第一个2）

const lastTwoIndex = arr.findLastIndex(x => x === 2);
console.log(lastTwoIndex); // 3（索引3的位置）
```

```javascript
// 实际应用：根据 ID 查找用户
function findUserById(users, id) {
    return users.find(user => user.id === id);
}

const users = [
    { id: 1, name: "张三" },
    { id: 2, name: "李四" },
    { id: 3, name: "王五" }
];

console.log(findUserById(users, 2)); // { id: 2, name: "李四" }
console.log(findUserById(users, 99)); // undefined
```


## 7.6 转换与聚合

数组的转换与聚合方法是函数式编程的精髓所在。掌握它们，你的代码会变得简洁而优雅。

### map：映射变换

`map` 对数组的每个元素执行回调，返回一个新数组（不改变原数组）。

```javascript
const numbers = [1, 2, 3, 4, 5];

// 基本用法：每个元素乘以2
const doubled = numbers.map(n => n * 2);
console.log(doubled); // [2, 4, 6, 8, 10]
console.log(numbers); // [1, 2, 3, 4, 5]（原数组不变！）

// 提取对象属性
const users = [
    { name: "张三", age: 25 },
    { name: "李四", age: 30 },
    { name: "王五", age: 35 }
];

const names = users.map(user => user.name);
console.log(names); // ["张三", "李四", "王五"]

const ages = users.map(user => user.age);
console.log(ages); // [25, 30, 35]
```

```javascript
// 实际应用：数据格式化
const products = [
    { name: "iPhone", price: 6999 },
    { name: "iPad", price: 4999 },
    { name: "MacBook", price: 12999 }
];

const formatted = products.map(p => ({
    ...p,
    priceTag: `¥${p.price}`
}));
console.log(formatted);
// [
//   { name: "iPhone", price: 6999, priceTag: "¥6999" },
//   { name: "iPad", price: 4999, priceTag: "¥4999" },
//   { name: "MacBook", price: 12999, priceTag: "¥12999" }
// ]
```

### filter：条件过滤

`filter` 返回满足条件的元素组成的新数组。

```javascript
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// 过滤偶数
const evens = numbers.filter(n => n % 2 === 0);
console.log(evens); // [2, 4, 6, 8, 10]

// 过滤大于5的数
const greaterThan5 = numbers.filter(n => n > 5);
console.log(greaterThan5); // [6, 7, 8, 9, 10]

// 过滤字符串
const names = ["张三", "李四", "王五", "赵六"];
const filteredNames = names.filter(name => name.length > 2);
console.log(filteredNames); // ["张三", "李四", "王五", "赵六"]（都大于2）
```

```javascript
// 实际应用：过滤有效数据
const users = [
    { name: "张三", email: "zhangsan@example.com" },
    { name: "李四", email: null },
    { name: "王五", email: "wangwu@example.com" },
    { name: "赵六", email: undefined }
];

const validUsers = users.filter(user => user.email);
console.log(validUsers);
// [{ name: "张三", ... }, { name: "王五", ... }]
```

### reduce：聚合计算，初始值

`reduce` 是最强大的数组方法，可以实现任何聚合逻辑。

```javascript
const numbers = [1, 2, 3, 4, 5];

// reduce(callback, initialValue)
// callback: (accumulator, currentValue) => newAccumulator

// 求和
const sum = numbers.reduce((acc, cur) => acc + cur, 0);
console.log(sum); // 15

// 求乘积
const product = numbers.reduce((acc, cur) => acc * cur, 1);
console.log(product); // 120

// 找最大值
const max = numbers.reduce((acc, cur) => acc > cur ? acc : cur, numbers[0]);
console.log(max); // 5

// 更简单的方法：Math.max + 展开运算符
console.log(Math.max(...numbers)); // 5
```

```javascript
// reduce 实现 sum / max / filter / map

// 实现 filter
function myFilter(arr, predicate) {
    return arr.reduce((acc, val) => {
        if (predicate(val)) {
            acc.push(val);
        }
        return acc;
    }, []);
}

const nums = [1, 2, 3, 4, 5];
console.log(myFilter(nums, n => n > 2)); // [3, 4, 5]

// 实现 map
function myMap(arr, transform) {
    return arr.reduce((acc, val) => {
        acc.push(transform(val));
        return acc;
    }, []);
}

console.log(myMap(nums, n => n * 2)); // [2, 4, 6, 8, 10]
```

```javascript
// reduce 实现 groupBy
function groupBy(arr, keyFn) {
    return arr.reduce((groups, item) => {
        const key = keyFn(item);
        if (!groups[key]) {
            groups[key] = [];
        }
        groups[key].push(item);
        return groups;
    }, {});
}

const users = [
    { name: "张三", role: "admin" },
    { name: "李四", role: "user" },
    { name: "王五", role: "admin" },
    { name: "赵六", role: "user" }
];

const grouped = groupBy(users, user => user.role);
console.log(grouped);
// {
//   admin: [{ name: "张三", ... }, { name: "王五", ... }],
//   user: [{ name: "李四", ... }, { name: "赵六", ... }]
// }
```

### flat / flatMap：扁平化（ES2019+）

```javascript
// flat：扁平化数组
const nested = [1, 2, [3, 4, [5, 6]]];
console.log(nested.flat()); // [1, 2, 3, 4, [5, 6]]（默认只扁平一层）
console.log(nested.flat(2)); // [1, 2, 3, 4, 5, 6]（扁平两层）
console.log(nested.flat(Infinity)); // [1, 2, 3, 4, 5, 6]（完全扁平）

// flatMap：先 map 再 flat
const arr = [1, 2, 3];
const result = arr.flatMap(x => [x, x * 2]);
console.log(result); // [1, 2, 2, 4, 3, 6]

// 等价于
const result2 = arr.map(x => [x, x * 2]).flat();
console.log(result2); // [1, 2, 2, 4, 3, 6]

// 实际应用：提取并扁平化
const sentences = ["Hello world", "How are you"];
const words = sentences.flatMap(sentence => sentence.split(" "));
console.log(words); // ["Hello", "world", "How", "are", "you"]
```

### some / every：条件判断

```javascript
const numbers = [1, 2, 3, 4, 5];

// some：是否有任一元素满足条件，返回布尔
const hasEven = numbers.some(n => n % 2 === 0);
console.log(hasEven); // true（有偶数）

const hasNegative = numbers.some(n => n < 0);
console.log(hasNegative); // false

// every：是否所有元素都满足条件，返回布尔
const allPositive = numbers.every(n => n > 0);
console.log(allPositive); // true（都是正数）

const allEven = numbers.every(n => n % 2 === 0);
console.log(allEven); // false（不是所有都是偶数）
```

### map vs filter vs reduce vs some vs every 选择指南

| 方法 | 返回值 | 用途 | 是否改变原数组 |
|------|--------|------|---------------|
| map | 新数组 | 转换/映射 | 否 |
| filter | 新数组 | 过滤 | 否 |
| reduce | 任意值 | 聚合/汇总 | 否 |
| some | 布尔 | 是否有满足条件的 | 否 |
| every | 布尔 | 是否都满足条件 | 否 |

```javascript
// 选择指南
const users = [
    { name: "张三", age: 25, scores: [80, 90, 85] },
    { name: "李四", age: 30, scores: [70, 95, 88] },
    { name: "王五", age: 35, scores: [60, 70, 75] }
];

// 1. 需要转换数组 -> map
const names = users.map(u => u.name); // ["张三", "李四", "王五"]

// 2. 需要过滤数组 -> filter
const adults = users.filter(u => u.age >= 30); // [李四, 王五]

// 3. 需要汇总计算 -> reduce
const totalAge = users.reduce((sum, u) => sum + u.age, 0); // 90
const maxAge = users.reduce((max, u) => Math.max(max, u.age), 0); // 35

// 4. 是否存在满足条件 -> some
const hasYoung = users.some(u => u.age < 28); // true（张三）

// 5. 是否都满足条件 -> every
const allAdults = users.every(u => u.age >= 25); // true
```


## 7.7 排序与拼接

### sort：排序（默认 Unicode 编码，数字排序需传比较函数）

```javascript
const fruits = ["banana", "apple", "orange", "grape"];

// 默认排序：按 Unicode 编码（不是按字母！）
console.log(fruits.sort()); // ["apple", "banana", "grape", "orange"]
// 注意：排序是原地排序，会修改原数组
```

```javascript
// 数字排序：必须传比较函数
const numbers = [10, 5, 8, 1, 3, 2];

// 升序排序
numbers.sort((a, b) => a - b);
console.log(numbers); // [1, 2, 3, 5, 8, 10]

// 降序排序
numbers.sort((a, b) => b - a);
console.log(numbers); // [10, 8, 5, 3, 2, 1]
```

```javascript
// 比较函数的原理
// 如果 a < b，返回负数 -> a 排在前面
// 如果 a === b，返回 0 -> 顺序不变
// 如果 a > b，返回正数 -> b 排在前面

// 简化写法
numbers.sort((a, b) => a - b); // 升序
numbers.sort((a, b) => b - a); // 降序

// 字母排序（localeCompare 更智能）
const strs = ["banana", "äpple", "orange"];
console.log(strs.sort()); // ["banana", "orange", "äpple"]（Unicode 顺序）
console.log(strs.sort((a, b) => a.localeCompare(b))); // ["äpple", "banana", "orange"]（locale 顺序）
```

### sort 实现升序 / 降序 / 随机排序

```javascript
// 升序
function ascending(arr) {
    return [...arr].sort((a, b) => a - b);
}

console.log(ascending([3, 1, 4, 1, 5, 9, 2, 6])); // [1, 1, 2, 3, 4, 5, 6, 9]

// 降序
function descending(arr) {
    return [...arr].sort((a, b) => b - a);
}

console.log(descending([3, 1, 4, 1, 5, 9, 2, 6])); // [9, 6, 5, 4, 3, 2, 1, 1]

// 随机排序（洗牌算法）
function shuffle(arr) {
    return [...arr].sort(() => Math.random() - 0.5);
}

console.log(shuffle([1, 2, 3, 4, 5])); // 随机顺序
```

### reverse：反转

```javascript
const arr = [1, 2, 3, 4, 5];
arr.reverse();
console.log(arr); // [5, 4, 3, 2, 1]

// 配合 sort 实现降序
const numbers = [3, 1, 4, 1, 5, 9, 2, 6];
const descending = [...numbers].sort((a, b) => a - b).reverse();
console.log(descending); // [9, 6, 5, 4, 3, 2, 1, 1]

// 更简洁：sort((a, b) => b - a) 就是降序
const descending2 = [...numbers].sort((a, b) => b - a);
console.log(descending2); // [9, 6, 5, 4, 3, 2, 1, 1]
```

### concat：合并

```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const arr3 = [7, 8, 9];

// concat：合并多个数组，返回新数组
const merged = arr1.concat(arr2, arr3);
console.log(merged); // [1, 2, 3, 4, 5, 6, 7, 8, 9]
console.log(arr1); // [1, 2, 3]（原数组不变）
```

```javascript
// 合并单个元素
console.log([1, 2, 3].concat(4)); // [1, 2, 3, 4]

// 合并数组和元素
console.log([1, 2].concat([3, 4], 5, 6)); // [1, 2, 3, 4, 5, 6]

// 展开运算符更简洁
const combined = [...arr1, ...arr2, ...arr3];
console.log(combined); // [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### slice：切片（不修改原数组）

```javascript
const arr = [1, 2, 3, 4, 5];

// slice(start, end)：返回从 start 到 end（不含）的元素
console.log(arr.slice(1, 3)); // [2, 3]（索引1到2，不含3）
console.log(arr.slice(1));    // [2, 3, 4, 5]（从索引1到末尾）
console.log(arr.slice(0, -1)); // [1, 2, 3, 4]（去掉最后一个）
console.log(arr.slice(-3));    // [3, 4, 5]（最后三个）
console.log(arr.slice());     // [1, 2, 3, 4, 5]（复制整个数组）

// slice 不修改原数组
console.log(arr); // [1, 2, 3, 4, 5]（原数组不变）
```

```javascript
// 实际应用：复制数组（浅拷贝）
const original = [1, 2, 3, 4, 5];
const copy = original.slice(); // 或 [...original] 或 Array.from(original)
copy.push(6);
console.log(original); // [1, 2, 3, 4, 5]（原数组不变）
console.log(copy);     // [1, 2, 3, 4, 5, 6]
```

### join：转字符串

```javascript
const fruits = ["苹果", "香蕉", "橙子"];

// join(separator)：用分隔符连接成字符串
console.log(fruits.join());    // "苹果,香蕉,橙子"（默认逗号）
console.log(fruits.join("-"));  // "苹果-香蕉-橙子"
console.log(fruits.join(""));  // "苹果香蕉橙子"（无分隔符）

// 空数组
console.log([].join("-")); // ""
```

```javascript
// 实际应用：数字数组变字符串
const numbers = [1, 2, 3, 4, 5];
console.log(numbers.join("")); // "12345"
console.log(numbers.join("+")); // "1+2+3+4+5"

// 配合 split 实现字符串和数组互转
const str = "hello";
const arr = str.split(""); // ["h", "e", "l", "l", "o"]
const back = arr.join("");  // "hello"
console.log(arr, back);    // ["h", "e", "l", "l", "o"] "hello"
```

### toString：转字符串

```javascript
const arr = [1, 2, 3, 4, 5];
console.log(arr.toString()); // "1,2,3,4,5"

// 和 join() 效果类似，但不接受分隔符参数
console.log([1, 2, 3].toString()); // "1,2,3"
console.log(["a", "b", "c"].toString()); // "a,b,c"
```

### fill：填充（ES6+）

```javascript
const arr = new Array(5); // [empty × 5]

// fill(value)：用指定值填充
console.log(arr.fill(0)); // [0, 0, 0, 0, 0]

// fill(value, start, end)：填充指定范围
const arr2 = [1, 2, 3, 4, 5];
console.log(arr2.fill(0, 1, 3)); // [1, 0, 0, 4, 5]（索引1到2）

// 典型应用：创建固定值的数组
const zeros = Array(10).fill(0);
console.log(zeros); // [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

### Array.isArray：判断是否是数组

```javascript
// Array.isArray() 是判断数组最可靠的方式
console.log(Array.isArray([1, 2, 3])); // true
console.log(Array.isArray([]));         // true
console.log(Array.isArray({}));         // false
console.log(Array.isArray("hello"));    // false
console.log(Array.isArray(null));       // false
console.log(Array.isArray(new Date())); // false

// typeof 的局限性（数组的 typeof 是 "object"）
console.log(typeof [1, 2, 3]); // "object"（不能区分对象和数组）
```


## 7.8 数组技巧

这一节汇总一些实用的数组技巧，让你的代码更优雅。

### 去重：Set / indexOf / filter / includes / reduce

```javascript
const arr = [1, 2, 2, 3, 3, 3, 4, 5, 5];

// 方法1：Set（最简洁，ES6+）
console.log([...new Set(arr)]); // [1, 2, 3, 4, 5]

// 方法2：filter + indexOf
console.log(arr.filter((item, index) => arr.indexOf(item) === index));

// 方法3：filter + includes
console.log(arr.filter((item, _, self) => self.includes(item)));

// 方法4：reduce
console.log(arr.reduce((unique, item) => {
    return unique.includes(item) ? unique : [...unique, item];
}, []));
```

### 合并：concat / 展开运算符 / flat

```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const arr3 = [7, 8, 9];

// concat
console.log(arr1.concat(arr2, arr3)); // [1, 2, 3, 4, 5, 6, 7, 8, 9]

// 展开运算符（更简洁）
console.log([...arr1, ...arr2, ...arr3]); // [1, 2, 3, 4, 5, 6, 7, 8, 9]

// flat：扁平化嵌套数组
const nested = [[1, 2], [3, 4], [5, 6]];
console.log(nested.flat()); // [1, 2, 3, 4, 5, 6]

// 多层嵌套
const deepNested = [[1, 2], [3, [4, 5]], [6]];
console.log(deepNested.flat(Infinity)); // [1, 2, 3, 4, 5, 6]
```

### 洗牌算法（Fisher-Yates）：数组随机打乱

```javascript
function shuffle(arr) {
    const result = [...arr];
    for (let i = result.length - 1; i > 0; i--) {
        // 从 0 到 i 之间随机选一个
        const j = Math.floor(Math.random() * (i + 1));
        // 交换
        [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
}

console.log(shuffle([1, 2, 3, 4, 5])); // 随机顺序
```

### 交集 / 并集 / 差集

```javascript
const a = [1, 2, 3, 4];
const b = [3, 4, 5, 6];

// 并集（去重）
console.log([...new Set([...a, ...b])]); // [1, 2, 3, 4, 5, 6]

// 交集
console.log(a.filter(x => b.includes(x))); // [3, 4]

// 差集（a 有 b 没有的）
console.log(a.filter(x => !b.includes(x))); // [1, 2]

// 对称差集
console.log([...a.filter(x => !b.includes(x)), ...b.filter(x => !a.includes(x))]); // [1, 2, 5, 6]
```

### 求和：for / forEach / reduce

```javascript
const numbers = [1, 2, 3, 4, 5];

// for 循环
let sum = 0;
for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i];
}
console.log(sum); // 15

// forEach
let sum2 = 0;
numbers.forEach(n => sum2 += n);
console.log(sum2); // 15

// reduce（最简洁）
console.log(numbers.reduce((a, b) => a + b, 0)); // 15

// 多维数组求和
const nested = [[1, 2], [3, 4], [5, 6]];
console.log(nested.flat().reduce((a, b) => a + b, 0)); // 21
```

### 删除假值：filter(Boolean)

```javascript
const mixed = [0, 1, false, 2, "", 3, null, undefined, NaN, "hello"];

// filter(Boolean)：删除所有假值
console.log(mixed.filter(Boolean)); // [1, 2, 3, "hello"]
```

### 随机获取数组元素

```javascript
const fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"];

const randomItem = arr => arr[Math.floor(Math.random() * arr.length)];
console.log(randomItem(fruits)); // 随机一个
```

### 分组：reduce 实现 groupBy

```javascript
function groupBy(arr, keyFn) {
    return arr.reduce((groups, item) => {
        const key = keyFn(item);
        (groups[key] = groups[key] || []).push(item);
        return groups;
    }, {});
}

const users = [
    { name: "张三", age: 25 },
    { name: "李四", age: 30 },
    { name: "王五", age: 25 }
];

console.log(groupBy(users, u => u.age));
// { "25": [张三, 王五], "30": [李四] }
```

### 数组扁平化多种实现对比

```javascript
const nested = [1, [2, [3, [4, [5]]]]];

// 方法1：flat(Infinity)
console.log(nested.flat(Infinity)); // [1, 2, 3, 4, 5]

// 方法2：reduce + concat（递归）
function flatten(arr) {
    return arr.reduce((acc, val) => {
        return Array.isArray(val) ? acc.concat(flatten(val)) : acc.concat(val);
    }, []);
}
console.log(flatten(nested)); // [1, 2, 3, 4, 5]

// 方法3：toString（只适合纯数字）
console.log(nested.toString().split(",").map(Number)); // [1, 2, 3, 4, 5]
```

---

## 本章小结

本章我们全面学习了 JavaScript 数组：

1. **数组基础**：`[]` vs `new Array()` vs `Array.of()` vs `Array.from()` 的区别；稀疏数组和类数组对象。

2. **数组遍历**：`for`（传统）、`for...of`（最推荐遍历值）、`for...in`（不推荐）、`forEach`（数组方法，不能 break）。

3. **可迭代对象**：`Symbol.iterator` 协议、`entries()`、`keys()`、`values()`。

4. **增删操作**：`push`/`pop`（末尾）、`unshift`/`shift`（开头）、`splice`（万能方法，可添加/删除/替换）。

5. **查询与索引**：`indexOf`/`lastIndexOf`、`includes`（支持 NaN）、`find`/`findIndex`/`findLast`。

6. **转换与聚合**：`map`（映射）、`filter`（过滤）、`reduce`（聚合）、`flat`/`flatMap`、`some`/`every`。

7. **排序与拼接**：`sort`（需比较函数）、`reverse`、`concat`/`slice`/`join`、`fill`、`Array.isArray`。

8. **数组技巧**：去重、合并、洗牌、交集、并集、差集、分组、扁平化。

数组是 JavaScript 最强大的数据结构之一。熟练掌握这些方法，你的代码会更简洁、更高效！

下一章，我们将学习 JavaScript 的另一个核心概念——对象。准备好了吗？继续冲！
```



```

