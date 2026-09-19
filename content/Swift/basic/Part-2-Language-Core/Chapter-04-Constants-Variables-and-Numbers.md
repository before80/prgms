+++
title = "第4章 常量、变量与数值：let 的哲学和一个没有隐式转换的世界"
weight = 40
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第四章：常量、变量与数值：let 的哲学和一个没有隐式转换的世界

> 别的语言先用一章教你怎么声明变量，Swift 想教你的第一件事却是"尽量别用变量"。这不是洁癖，`let` 用得多，代码能推理的地方就多、能被编译器优化的地方就多、将来跟并发打交道时被卡住的概率也小。这一章还会顺手讲清 Swift 最容易被骂、但也最省心的两个设计：**没有隐式转换**和**溢出就崩**。

## 4.1 let 与 var：默认选 `let`

两个关键字，一句话说清区别：`let` 一旦绑定就不许再指向别的值，`var` 可以。先看最普通的用法：

```swift
let pi = 3.14159      // 常量：绑定之后不能再指向别的值
var count = 0         // 变量：可以改

count += 1
print(pi, count)
// prints: 3.14159 1
```

试着改一个 `let`，编译器会拦住你，而且顺手告诉你怎么办：

```swift
let pi = 3.14159
pi = 3.0
```

```text
error: cannot assign to value: 'pi' is a 'let' constant
  | `- note: change 'let' to 'var' to make it mutable
```

注意那句提示：**编译器不是在骂你，是在问你"要不要改成 `var`"**。什么时候该改？只有当你确实需要重新赋值时。官方风格指南的建议是：默认写 `let`，需要时再改成 `var`——反过来（先 `var` 再回头收紧）常常会留下一些"其实从没被改过"的变量。

## 4.2 类型推断与类型标注

同一份数据，写不写类型标注都能跑，差别在于"类型由谁决定"：

```swift
let a = 42
let b = 3.14159
print(type(of: a), type(of: b))
// prints: Int Double
```

Swift 的推断相当可靠：整数默认 `Int`，浮点默认 `Double`。想指定别的类型，就在名字后面加标注：

```swift
let x: Int = 42
let y: Float = 42
let z: Double = 42
print(x, y, z)
// prints: 42 42.0 42.0
```

注意 `let y: Float = 42` 里的 `42`：字面量本身没有类型，标注说"要 `Float`"，它就变成 `42.0`。这也解释了为什么标注有时是**必须**的——比如

```swift
let nothing: Int? = nil      // 没有标注就不知道"空"的是什么类型
```

可以一行声明多个：

```swift
let a = 1, b = 2
print(a + b)
// prints: 3
```

## 4.3 整数家族：默认用 `Int`

整型有一大家子，名字里的数字就是位数：

| 类型 | 范围（大致） | 什么时候用 |
|------|--------------|------------|
| `Int` | 平台字长（64 位平台是 64 位） | **默认选择**，绝大多数场合都用它 |
| `Int8`、`Int16`、`Int32`、`Int64` | ±2^(n−1) | 要和外部二进制格式、网络协议、C API 精确对齐时 |
| `UInt`、`UInt8`…`UInt64` | 非负 | 确实需要"非负"语义，或和外部格式对齐时 |

```swift
print(Int.max, Int.min)
// prints: 9223372036854775807 -9223372036854775808
print(Int8.max, UInt8.max, Int32.max)
// prints: 127 255 2147483647
print(MemoryLayout<Int>.size)
// prints: 8
```

`MemoryLayout<Int>.size` 是 8 字节，说明这台机器的 `Int` 是 64 位。用 `Int` 而不是到处写 `Int64` 的好处就在这里：它在 32 位平台自动变 32 位，你的代码不用改。相反，**`UInt` 不要因为"这个数不可能为负"就随手用**——它会和 `Int` 混用时报一堆转换错，收益却通常为零。

### 4.3.1 整数除法会截断，求余会带符号

整数相除的规则和数学课上的除法不是一回事，`-7` 那些负数的结果尤其容易算错：

```swift
print(7 / 2, -7 / 2, 7 % 3, -7 % 3)
// prints: 3 -3 1 -1
```

整数除法**向零截断**：`7 / 2` 是 3 而不是 3.5，`-7 / 2` 是 -3。求余的符号跟着被除数走，所以 `-7 % 3` 是 -1。想要正常的数学除法，得先把至少一边转成浮点。

数字字面量本身还有一堆更顺手的写法——`1_000_000` 里的下划线、十六进制 `0x1F`、二进制 `0b1010`、科学计数法 `1e6`、十六进制浮点 `0x1p4`——第 15B.3 节把它们集中列了一遍。

## 4.4 浮点家族：默认用 `Double`

| 类型 | 位数 | 有意义的十进制位数 | 什么时候用 |
|------|------|--------------------|------------|
| `Double` | 64 | 约 15–17 位 | **默认选择** |
| `Float` | 32 | 约 6–7 位 | 内存敏感、或和图形/信号接口对齐时 |

浮点数有个所有人都要知道的事实：**它不能精确表示大多数小数**。

```swift
print(0.1 + 0.2)
// prints: 0.30000000000000004
print(0.1 + 0.2 == 0.3)
// prints: false
```

有意思的是，换成精度更低的 `Float`，这个比较反而成立了——因为误差太小，直接被舍掉了：

```swift
print(Float(0.1) + Float(0.2) == Float(0.3))
// prints: true
```

这不是"Float 更准"，而是"Float 更钝"。**别用 `==` 比较浮点数**，要比较就用差值范围；要是算钱，用整数的最小单位（比如"分"）或者 Foundation 的 `Decimal`。

浮点还有三个特殊值，它们是真正常见的，不是异常：

```swift
print(1.0 / 0.0, -1.0 / 0.0, 0.0 / 0.0)
// prints: inf -inf nan

let nan = 0.0 / 0.0
print(nan == nan)
// 编译器顺带提醒：'.nan' == '.nan' is always false
// prints: false
```

`nan`（Not a Number）连自己都不等于自己，所以判断它要用 `isNaN`。

### 4.4.1 `nan`、`isNaN`：三个特殊值里最特别的那个

先说结论：`nan` 不是"报错时返回的空值"，也不是 `nil` 的亲戚，它就是一个**货真价实的 `Double` 值**，只是这个值表示"这次运算的结果在数学上没有意义"。`0.0 / 0.0`、`(-1.0).squareRoot()`、`inf - inf` 都会得到它，Swift 还额外给了你一个现成的字面量 `Double.nan`。

它最反常的地方是：**和任何东西比较都不成立，包括和它自己**。

```swift
let bad = 0.0 / 0.0
print(bad == bad, bad != bad)          // 连自己都不等于自己
// prints: false true
print(bad.isNaN)
// prints: true
print(bad == Double.nan)
// prints: false

let normal = 1.5
print(normal.isNaN, normal.isFinite)
// prints: false true

let huge = 1.0 / 0.0                   // 这是 inf，另一个特殊值
print(huge.isNaN, huge.isInfinite, huge.isFinite)
// prints: false true false
```

所以"用 `==` 判断是不是 NaN"这条路上永远走不通——它和谁比都是 `false`。判断它要用 `.isNaN`，配套的还有 `.isInfinite`（是不是 ±∞）和 `.isFinite`（是不是正常可用的数）。这三个都是**属性的写法**，动词在点上，不在括号里：

```text
error: cannot find 'isNaN' in scope
```

写 `isNaN(x)` 会得到上面这条错误，正确写法是 `x.isNaN`。这是标准库给浮点数定义的计算属性，不是全局函数（计算属性见第 19.1 节）。

`nan` 还有两个会悄悄坑到你的行为。一是参与算术会被"传染"：加、减、乘、除，只要有一个 `nan` 参与，结果就是 `nan`。二是排序时它的位置不可靠——所有比较都返回 `false`，排序算法拿到的是一堆自相矛盾的答案，所以别指望它被排到某个固定位置。

```swift
let badValue = 0.0 / 0.0
print(badValue, badValue + 1, badValue * 0)
// prints: nan nan nan
```

实战中 `nan` 大多来自三处：除零（`0.0 / 0.0`）、对负数开平方、以及从外部数据里读进来的"坏数字"。它们不会让程序崩，只会让结果悄悄变成 `nan` 一路传下去——所以**在数据入口处判一次 `.isNaN`**，把它挡在计算之外，比在出问题的地方倒查要省事得多。

```swift
let fromSensor = 0.0 / 0.0
print(fromSensor.isNaN, (2.5).isNaN)
// prints: true false
```

## 4.5 没有隐式转换：Swift 最硬的一条规则

试着把 `Int` 和 `Double` 相加：

```swift
let i: Int = 1
let d: Double = 2.5
print(i + d)
```

```text
error: binary operator '+' cannot be applied to operands of type 'Int' and 'Double'
  | `- note: overloads for '+' exist with these partially matching parameter lists: (Double, Double), (Int, Int)
```

编译器把两种正确写法都指给你看了：要么把左边转成 `Double`，要么把右边转成 `Int`。**转换必须你亲手写**：

```swift
let i: Int = 1
let d: Double = 2.5
print(Double(i) + d)
// prints: 3.5
print(Int(d))
// prints: 2
```

`Int(d)` 是**截断**，不是四舍五入，而且是向零截断：

```swift
print(Int(2.9), Int(-2.9), Int(2.5), Int(-2.5))
// prints: 2 -2 2 -2
print((2.5).rounded(), (2.5).rounded(.down), (2.4).rounded())
// prints: 3.0 2.0 2.0
```

字符串转数字则可能失败，所以返回的是可选值（第 9 章）：

```swift
print(Int("42")!)
// prints: 42
print(Int("四十又二") == nil)
// prints: true
```

上面那个感叹号值得停下来讲清楚，因为它是新手代码里最常见的"定时炸弹"。

`Int("42")` 的类型**不是** `Int`，而是 `Int?`——读作"可选值"，意思是"这里可能有一个 `Int`，也可能什么都没有"。`!` 叫**强制解包**，它的意思是"我保证里面一定有值，直接拿出来给我"。于是它有两种结局：成功时你得到普通的 `Int`，失败时程序当场崩溃。

```swift
let ok = Int("42")!
print(ok + 1)
// prints: 43
```

```swift
let bad = Int("四十二")!
print("这一行永远不会执行")
// prints: （无输出，程序终止）
```

第二段的真实死法是：

```text
Fatal error: Unexpectedly found nil while unwrapping an Optional value
```

它在"我确信这里不会失败"的临时脚本里很好用，但在要交付的代码里基本属于禁品——一次输入不合法，整个 App 就没了。更稳的两条路是：**给个兜底值**，或者**先确认有值再动手**。

```swift
print(Int("42") ?? 0, Int("四十二") ?? 0)
// prints: 42 0
```

`??` 读作"空合运算符"：左边有值就用左边，左边是"没有值"就用右边（第 7.7 节）。要按条件分情况处理，则用第 9 章的 `if let` / `guard let`。这两个写法你在第 9 章会看到全貌，现在只要记住：**`!` 是"崩给我看"的开关，写它之前先想想有没有别的办法**。

这一条"没有隐式转换"的规则，短期内会让你多敲几次 `Double(...)`，长期会省下很多"这个精度是什么时候丢的"的排查时间。

## 4.6 溢出：Swift 选择崩掉，而不是回绕

如果一个整数运算的结果超出类型能表示的范围，Swift 的处理分两种。**编译期能算出来的**，直接报错：

```swift
var m: Int8 = 127
m += 1
```

```text
error: arithmetic operation '127 + 1' (on type 'Int8') results in an overflow
```

**编译期算不出来**（依赖运行时的数据）的，程序会在运行期直接崩溃，而不是给你一个悄悄回绕过的数字：

```swift
func next(_ x: Int8) -> Int8 { x + 1 }
print(next(127))     // 进程崩掉，退出码非 0，不会打印任何数字
// prints: （无输出，程序终止）
```

如果你**确实**要回绕语义（哈希、加密、位运算里很常见），必须显式写带 `&` 的版本：

```swift
var m: Int8 = 127
m = m &+ 1
print(m)
// prints: -128
```

| 写法 | 溢出时的行为 |
|------|--------------|
| `+` `-` `*` | 崩溃（这是刻意的） |
| `&+` `&-` `&*` | 回绕 |

为什么这么设计？因为整数溢出几乎总是 bug，而不是意图。让它在最接近现场的地方炸掉，比让一个错误的数字一路传播到数据库里要好得多。

## 4.7 几个天天要用的数字小工具

下面这几个是标准库自带的，比手写循环可靠得多：

```swift
print(10.isMultiple(of: 2), abs(-5), min(3, 7), max(3, 7))
// prints: true 5 3 7
```

四舍五入不是只有一个方向。`rounded()` 不带参数时是"四舍五入，遇到 .5 往绝对值大的方向走"，带上取整规则后含义就变了，尤其对负数——**`.down` 是朝负无穷，不是朝零**：

```swift
print((2.5).rounded(), (-2.5).rounded())                        // 默认：四舍五入
// prints: 3.0 -3.0
print((2.5).rounded(.down), (-2.5).rounded(.down))              // 朝负无穷
// prints: 2.0 -3.0
print((2.5).rounded(.up), (-2.5).rounded(.up))                  // 朝正无穷
// prints: 3.0 -2.0
print((2.5).rounded(.towardZero), (-2.5).rounded(.towardZero))  // 朝零
// prints: 2.0 -2.0
print((2.5).rounded(.toNearestOrEven))                          // 就近取整，.5 取偶数（银行家舍入）
// prints: 2.0
print((2.5).rounded(.toNearestOrEven), (2.5).rounded(.toNearestOrAwayFromZero))
// prints: 2.0 3.0
```

`.towardZero` 的行为和 `Int(x)` 的截断完全一致，区别只是它仍然返回 `Double`。要"先四舍五入再转整数"，就把两者串起来：

```swift
print(Int(2.9), Int(-2.9), Int((2.9).rounded()), Int((-2.9).rounded()))
// prints: 2 -2 3 -3
```

| 想做的事 | 写法 |
|----------|------|
| 判断能否整除 | `10.isMultiple(of: 2)`（比 `%` 更好读） |
| 取绝对值 | `abs(-5)` |
| 取小/取大 | `min(a, b)`、`max(a, b)` |
| 四舍五入 | `x.rounded()`；指定方向用 `x.rounded(.up)`、`.down`、`.towardZero`、`.toNearestOrEven` |
| 先取整再转整数 | `Int(x.rounded())`；只截断则直接 `Int(x)` |
| 判断坏数字 | `x.isNaN`、`x.isInfinite`、`x.isFinite` |

## 4.8 本章小结

| 你想做的事 | 写法 |
|------------|------|
| 声明不可变的值 | `let pi = 3.14159` |
| 声明可变的值 | `var count = 0` |
| 指定类型 | `let x: Int = 42` |
| 查类型 | `type(of: x)` |
| 整数转浮点 | `Double(i)`、`Float(i)` |
| 浮点转整数 | `Int(d)`（截断，不四舍五入） |
| 四舍五入 | `d.rounded()` |
| 字符串转数字 | `Int("42")`（可能为 `nil`） |
| 要回绕的运算 | `&+`、`&-`、`&*` |
| 平台字长 | `MemoryLayout<Int>.size` |

## 4.9 本章易错点速查

| 容易踩的地方 | 正确认识 |
|--------------|----------|
| 声明变量当然用 `var` | 官方风格反过来：默认 `let`，需要改再换 `var`。编译器会贴心提示你怎么改 |
| `let` 只是"不能重新赋值"，和可变性无关 | 对值类型成立；对类这类引用类型，`let` 约束的是"引用不能换"，对象内部仍可能变（第 17、18 章细讲） |
| `let x = 3.0` 是 `Float` | 浮点字面量的默认类型是 `Double`；要 `Float` 必须标注 |
| `Int(2.9)` 是 3 | 不是，是 2。`Int(...)` 向零截断；要四舍五入用 `rounded()` |
| `Int("42")` 直接能用 | 它返回的是可选值，因为字符串可能是别的；`Int("42")!` 或 `?? 0` 才能拿到数字 |
| `Int` 和 `Double` 会自动转换 | 不会，Swift 没有隐式数值转换。混用必须显式写 `Double(i)` 这类转换 |
| 整数除法 `7 / 2` 得 3.5 | 得 3。想得到小数，先把操作数转成 `Double` |
| 整数溢出会像某些语言一样回绕 | 不会，会崩。想要回绕必须写 `&+`、`&-`、`&*` |
| 用 `==` 比较浮点数是安全的 | 不安全。`0.1 + 0.2 == 0.3` 为 `false`；比较浮点要用误差范围，算钱用整数或 `Decimal` |
| `nan` 可以用 `==` 判断 | 不能，`nan == nan` 是 `false`；要用属性的写法 `x.isNaN`，写 `isNaN(x)` 会报 `cannot find 'isNaN' in scope` |
| `x.rounded(.down)` 是"舍去小数" | 它是**朝负无穷**：`(-2.5).rounded(.down)` 是 `-3.0`；要舍去小数用 `.towardZero` |
| 因为"这个数不会是负的"就用 `UInt` | 别随手用。`UInt` 与 `Int` 混用时转换麻烦，收益通常为零 |

## 4.10 下章预告

数字讲完了，下一章是 Swift 里最容易让人"以为自己懂了"的类型：`String`。为什么它的下标不能用整数？为什么 `"👨‍👩‍👧‍👦".count` 是 1 而它占二十几个字节？为什么 `Substring` 和 `String` 是两个类型？下一章把这些坑一次填平。
