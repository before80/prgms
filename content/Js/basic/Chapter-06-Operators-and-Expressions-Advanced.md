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
// 性能方面：完全没有区别
// 「前置++比后置++快」是 C++ 的经验（那里面涉及对象的拷贝构造），
// 在 JavaScript 里 ++i 与 i++ 都会被引擎编译成同样的自增指令，
// 区别只在于「表达式的返回值」不同，不存在可测量的性能差异。

// 所以这里的建议只有一条：
// ——当表达式的返回值会被使用时，一定要想清楚用前置还是后置；
//    如果返回值不被使用（例如 for 循环的更新表达式），写哪个纯粹是风格问题。
```

```javascript
// 实用建议

// 1. 在 for 循环中，两者都可以，看个人习惯
for (let i = 0; i < 5; i++) {}  // 常见写法
for (let i = 0; i < 5; ++i) {}  // 也可以

// 2. 如果要使用表达式的值，小心选择
const arr = ['a', 'b', 'c'];
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
    ++idx;                     // 但递增必须单独写成一行
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

## 6.2 自增自减的类型转换与边界

`++` 和 `--` 只对数字有意义，所以它们会对操作数做一次**隐式数字转换**，这一步经常带来意外结果：

```javascript
// 字符串会被转成数字
let s = '5';
console.log(++s);      // 6
console.log(typeof s); // 'number'（变量本身的类型也变了）

// 转不动就是 NaN，而且类型同样会变成 number
let t = 'abc';
console.log(++t);      // NaN
console.log(typeof t); // 'number'

// 布尔值：true 相当于 1
let b = true;
console.log(++b);      // 2

// 对象会先调用 valueOf / toString 尝试转成数字
let box = { valueOf: () => 41 };
console.log(++box);    // 42

// 注意目标必须可写：const 声明的变量不能自增
// const fixed = 1;
// ++fixed; // TypeError: Assignment to constant variable.

// BigInt 与 Number 不能混合运算
let big = 1n;
console.log(++big);    // 2n
// let mix = 1n; mix += 1; // TypeError: Cannot mix BigInt and other types
```

它还有两条硬性限制，都是初学者常踩的：

```javascript
// ❌ 不能作用于字面量：自增的前提是「有个可写的目标」
// ++5;
// SyntaxError: Invalid left-hand side expression in prefix operation

// ❌ 不能作用于常量
const c = 1;
// ++c;
// TypeError: Assignment to constant variable.
```

顺带回顾一个贯穿全书的点：`+` 既做加法又做字符串拼接，行为取决于两边类型，而 `-`、`*`、`/` 没有字符串语义，会强制转成数字。

```javascript
console.log('1' + 1); // '11'（拼接）
console.log('1' - 1); // 0（数字运算）
console.log(1 + true); // 2
console.log('1' + true); // '1true'
```

不想猜类型时，用 `Number()`、`String()` 显式转换，比依赖隐式规则可靠得多。

## 6.3 一元运算符补充

### typeof：查询类型

```javascript
console.log(typeof 1);            // 'number'
console.log(typeof 1n);           // 'bigint'
console.log(typeof 'a');          // 'string'
console.log(typeof true);         // 'boolean'
console.log(typeof undefined);    // 'undefined'
console.log(typeof Symbol());     // 'symbol'
console.log(typeof function () {}); // 'function'
console.log(typeof {});           // 'object'
console.log(typeof null);         // 'object'（著名的历史遗留问题）

// 判断 null 必须直接比较，不能靠 typeof
console.log(null === null);       // true

// typeof 是唯一可以安全探测「未声明变量」的运算符，不会抛错
console.log(typeof notDeclared);  // 'undefined'
// console.log(notDeclared);      // ReferenceError
```

### delete：删除属性

```javascript
const user = { name: 'A', age: 18 };
console.log(delete user.age); // true（删除成功）
console.log('age' in user);   // false
console.log(user);            // { name: 'A' }

// ❌ 不能删除变量、函数或参数
let x = 1;
console.log(delete x); // false（严格模式下会直接抛 SyntaxError）

// 删除数组元素不会缩短数组，只会留下「空槽」
const nums = [1, 2, 3];
delete nums[1];
console.log(nums);        // [1, <1 empty item>, 3]
console.log(nums.length); // 3
// 想真正移除元素要用 splice
nums.splice(1, 1);        // [1, 3]
```

### void：求值后返回 undefined

```javascript
console.log(void 0);        // undefined
console.log(void 'anything'); // undefined

// 典型用途：在箭头函数里表达「只执行、不返回」
const log = (msg) => void console.log(msg);
```

### !! 与一元 +：常见的类型转换写法

```javascript
// !!x 等价于 Boolean(x)
console.log(!!'');   // false
console.log(!!'0');  // true（非空字符串一律为 true，'0' 也不例外）
console.log(!!0);    // false
console.log(!![]);   // true（对象永远是 true）
console.log(!!{});   // true

// 一元 + 等价于 Number(x)
console.log(+'42');    // 42
console.log(+'');      // 0
console.log(+true);    // 1
console.log(+'42px');  // NaN（parseInt 才会得到 42）
```

`!!` 在 JavaScript 圈子里很常见，但在 TypeScript 或现代代码中 `Boolean(x)` 更直观。另外注意：判断「数组是否为空」不能写 `if (!arr)`，空数组是对象，永远为真；应该判断 `arr.length === 0`。

## 6.4 逗号运算符

```javascript
// 从左到右依次求值，返回最后一个表达式的值
const r = (1 + 1, 2 + 2, 3 + 3);
console.log(r); // 6

// 加括号才构成「逗号运算符」，否则逗号只是参数分隔符
function f(a) { return a; }
console.log(f((1, 2))); // 2

// 常见（但可读性一般）用法：for 循环里同时维护两个变量
for (let i = 0, j = 10; i < j; i++, j--) {
    console.log(i, j);
}

// 不推荐：把多个有副作用的操作塞进一个表达式
// const value = (doSomething(), doAnother(), finalValue);
```

大多数情况下，逗号运算符只会降低可读性，把它拆成多条语句即可。它的合法用途集中在压缩过的代码和少数 for 循环头部。

## 6.5 优先级与结合性

优先级决定「先算什么」，结合性决定「优先级相同时从左算还是从右算」：

```javascript
console.log(10 - 3 - 2);  // 5  减法左结合：(10 - 3) - 2
console.log(2 ** 3 ** 2); // 512 幂运算右结合：2 ** (3 ** 2)

// 赋值运算符右结合
let a, b;
a = b = 5;   // 等价于 a = (b = 5)
```

实战中最容易读错的几处：

| 表达式 | 结果 | 说明 |
| --- | --- | --- |
| `1 + 2 + '3'` | `'33'` | 先算 `1+2` 得到 3，再与 `'3'` 拼接 |
| `'3' + 1 + 2` | `'312'` | 先拼成 `'31'`，再拼 `'2'` |
| `'5' - 1` | `4` | 减号没有字符串语义，强制转数字 |
| `1 < 2 < 3` | `true` | 先算 `1 < 2` 得到 `true`，`true < 3` 又是 `true`（碰巧成立） |
| `3 > 2 > 1` | `false` | 先算 `3 > 2` 得到 `true`，`true > 1` 为 `false` |
| `-3 ** 2` | 语法错误 | 一元负号与 `**` 混用必须加括号：`(-3) ** 2` 或 `-(3 ** 2)` |
| `a ?? b` 未加括号地紧接着逻辑或 | 语法错误 | `??` 不能与逻辑或、逻辑与直接混用，必须显式加括号 |

```javascript
// 想表达「a 有值就用 a，否则用 b 或 c」时必须写清楚括号
const result = a ?? (b || c);

// 复杂表达式一律加括号，不要让别人（包括三个月后的自己）去查优先级表
const total = (price + tax) * quantity;
const isReady = (status === 'ready') && (retryCount < 3);
```

一条实用准则：**只要需要停下来想「这里谁先算」，就加括号**。括号的成本是零，读错优先级的成本可能是一次线上事故。

---

## 本章小结

本章我们深入理解了自增自减运算符：

1. **`++a`（前置）**：先加 1，再返回新值。
2. **`a++`（后置）**：先返回当前值的副本，再加 1。
3. **类型转换**：`++`/`--` 会隐式转数字，字符串 `'5'` 会变成 6，`'abc'` 会变成 `NaN`；不能作用于字面量和 `const`。
4. **一元运算符**：`typeof`、`delete`、`void`、`!!`、一元 `+` 各自的行为与边界。
5. **逗号运算符**：从左到右求值、返回最后一个值，多数情况下应该拆成多条语句。
6. **优先级与结合性**：结合性和优先级同样重要，容易读错的表达式要主动加括号。
7. **实用建议**：在 for 循环中 `i++` 与 `++i` 效果相同、性能也相同；真正需要小心的只有「表达式的返回值会被使用」的场合，此时拆成多行更清晰。

下一章，我们将学习 JavaScript 中最重要的数据结构——数组。准备好了吗？继续冲！
