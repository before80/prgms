+++
title = "第 6 章 运算符与表达式（补充）"
weight = 60
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 6 章 运算符与表达式（补充）

## 6.1 自增自减详解

在第四章我们简单介绍了 `++` 和 `--`，但这一节我们要把它彻底讲透。这两个运算符虽然只有两个字符，但里面藏着的细节足以让无数面试者翻车。

### ++a 与 a++ 的区别与执行顺序

**前置 `++`（`++a`）**：先给变量加 1，然后返回新值。
**后置 `++`（`a++`）**：先返回当前值（副本），然后给变量加 1。

```javascript
// 前置++：先加后用
let a = 5;
console.log(++a); // 6（先加到6，再输出）
console.log(a);   // 6

// 后置++：先用后加
let b = 5;
console.log(b++); // 5（先输出5，b再变成6）
console.log(b);   // 6

// 内存中的变化
// ++a: a = a + 1; return a;
// a++: temp = a; a = a + 1; return temp;
```

```javascript
// 另一个角度理解
let a = 1;

console.log(++a); // a先+1变成2，返回2
console.log(a);   // 2

console.log(a++); // 返回a的值2，然后a变成3
console.log(a);   // 3
```

```javascript
// 三者对比
let x = 5;

// 表达式本身的值
let val1 = ++x; // 前置++：x变成6，表达式返回6
console.log("val1 =", val1, "x =", x); // val1 = 6, x = 6

let y = 5;
let val2 = y++; // 后置++：表达式返回5，然后y变成6
console.log("val2 =", val2, "y =", y); // val2 = 5, y = 6

let z = 5;
let val3 = z;   // 仅仅是赋值
console.log("val3 =", val3, "z =", z); // val3 = 5, z = 5
```

```javascript
// 常见陷阱：连续使用
let i = 1;
console.log(i++ + ++i); // 4
// 分析：
// 1. i++：返回1，i变成2
// 2. ++i：i变成3，返回3
// 3. 1 + 3 = 4
// 4. 最终 i = 3

console.log(i++ + i++); // 7
// 分析：
// 1. i++：返回3，i变成4
// 2. i++：返回4，i变成5
// 3. 3 + 4 = 7
// 4. 最终 i = 5

// 这种代码太混乱了！不要在同一个表达式中多次修改同一个变量！
```

### 循环中的 i++ 和 ++i

在循环中使用 `i++` 和 `++i`，哪个更好？

```javascript
// 答案：在大多数情况下，没有区别！
// 因为我们通常只关心循环变量本身，不关心表达式的返回值

for (let i = 0; i < 3; i++) {
    console.log(i); // 0, 1, 2
}

for (let i = 0; i < 3; ++i) {
    console.log(i); // 0, 1, 2（结果完全一样）
}
```

```javascript
// 唯一有区别的场景：表达式的返回值被使用
let arr = [1, 2, 3];
let i = 0;

// 使用后置++
console.log(arr[i++]); // arr[0] = 1，然后 i 变成 1
console.log(arr[i++]); // arr[1] = 2，然后 i 变成 2
```

```javascript
// 用 ++i 的话
let arr2 = [1, 2, 3];
let j = 0;

console.log(arr2[++j]); // j 先变成1，然后 arr[1] = 2
console.log(arr2[++j]); // j 先变成2，然后 arr[2] = 3
```

```javascript
// 性能方面：现代 JavaScript 引擎会优化，没有区别
// 但在某些极致的性能敏感场景下，V8 引擎对 ++i 的优化更好一点点

// 推荐：使用 ++i 而不是 i++（风格更一致，表达更清晰）
// 因为前置++先改变值再使用，逻辑更直观
```

```javascript
// 实用建议

// 1. 在 for 循环中，两者都可以，看个人习惯
for (let i = 0; i < 5; i++) {}  // 常见写法
for (let i = 0; i < 5; ++i) {}  // 也可以

// 2. 如果要使用表达式的值，小心选择
let k = 0;
while (k < 3) {
    // 用后置++：先使用当前值，再递增
    console.log(arr[k++]); // arr[0], arr[1], arr[2]

    // 用前置++：先递增，再使用
    // console.log(arr[++k]); // arr[1], arr[2], arr[3]（越界！）
}

// 3. 不确定的时候，用 i += 1 代替 ++i
for (let i = 0; i < 5; i += 1) {} // 最清晰，但有点啰嗦
```

```javascript
// 完整示例：遍历数组的两种方式
const fruits = ["苹果", "香蕉", "橙子", "葡萄"];

// 方式1：后置++（常用）
for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}

// 方式2：前置++（也可以）
for (let i = 0; i < fruits.length; ++i) {
    console.log(fruits[i]);
}

// 方式3：用 while + 后置++
let idx = 0;
while (idx < fruits.length) {
    console.log(fruits[idx++]); // 使用后置++，idx在访问后才递增
}

// 方式4：用 while + 前置++
idx = 0;
while (idx < fruits.length) {
    console.log(fruits[idx]); // 先打印当前
    ++idx;                     // 后置++写成单独一行
}
```

```javascript
// 特殊场景：对象属性的自增
const counter = { value: 0 };

// 前置++
console.log(++counter.value); // 1
console.log(counter.value);   // 1

// 后置++
console.log(counter.value++); // 1
console.log(counter.value);   // 2
```

```javascript
// 自减同理
let num = 5;
console.log(--num); // 4（先减后用）
console.log(num--); // 4（先用后减）
console.log(num);   // 3
```

---

## 本章小结

本章我们深入理解了自增自减运算符：

1. **`++a`（前置）**：先加 1，再返回新值。
2. **`a++`（后置）**：先返回当前值的副本，再加 1。
3. **循环中的选择**：在 for 循环中两者效果相同；在需要使用表达式值时，根据需求选择。
4. **实用建议**：大多数情况下用 `i++` 或 `++i` 都可以，但在表达式中使用时要格外小心。遇到复杂场景，拆成多行代码更清晰。

下一章，我们将学习 JavaScript 中最重要的数据结构——数组。准备好了吗？继续冲！
