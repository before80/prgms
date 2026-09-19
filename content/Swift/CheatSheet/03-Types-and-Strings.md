+++
title = "03 类型与字符串"
linkTitle = "03 类型与字符串"
weight = 30
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "整数与浮点的边界、Character 与 String 的全部写法、正则、格式化"
isCJKLanguage = true
draft = false
+++

# 03 类型与字符串

## 数值类型全景

| 类型 | 位数 | 范围 / 精度 |
| --- | --- | --- |
| `Int` / `UInt` | 平台字长（64 位平台上 64 位） | `Int` 是默认整数类型，能用就用它 |
| `Int8` `Int16` `Int32` `Int64` | 8 / 16 / 32 / 64 | 有符号，与 C 的 `int8_t` 等一一对应 |
| `UInt8` `UInt16` `UInt32` `UInt64` | 同上 | 无符号，处理二进制协议时用 |
| `Float16` | 16 | 精度约 3 位十进制；只有 Apple 芯片（arm64）可用，Intel Mac 上是 unavailable 🆕 |
| `Float` | 32 | 精度约 6 位十进制 |
| `Double` | 64 | 精度约 15 位十进制，**浮点默认类型** |

```swift
print(Int8.max, Int8.min, UInt8.max)
// prints: 127 -128 255
print(Int.max)
// prints: 9223372036854775807
```

⚠️ `UInt` 并不是"更安全的 `Int`"。它只是不给你负数：`UInt(0) - 1` 不会变成 `-1`，而是当场崩溃。真要用环绕写法，`&-` 会送你一个看起来非常体面的巨大正数，bug 就从这里开始：

```swift
print(Int(0) - 1)
// prints: -1
print(UInt(0) &- 1)
// prints: 18446744073709551615
print(UInt(5) &- 7)
// prints: 18446744073709551614     本来想要 -2，拿到一个天文数字
// print(UInt(0) - 1)              // 🛑 运行时崩溃：下溢
```

再加上 `[1, 2, 3].count`、`index` 这类 API 一律返回 `Int`，全程用 `UInt` 只会换来满屏 `Int(...)` 转换。**除非在写二进制协议或与 C 交互，否则一律用 `Int`。**

## 整数

### 字面量

```swift
let decimal = 42
let binary = 0b1010_1010
let octal = 0o755
let hex = 0xFF_FF
let padded = 1_000_000     // 下划线只是给人看的
let negative = -17
```

### 常用操作

| 操作 | 写法 |
| --- | --- |
| 判整除 | `n.isMultiple(of: 3)` 🔥 比 `n % 3 == 0` 更能表达意图 |
| 同时取商和余 | `let (q, r) = 17.quotientAndRemainder(dividingBy: 5)` → `(3, 2)` |
| 随机数 | `Int.random(in: 1...100)`、`Bool.random()`、`array.randomElement()` |
| 转字符串 | `String(42)` |
| 从字符串解析 | `Int("42")` 返回 `Int?` |
| 取绝对值 | `abs(-3)` |
| 最小值 / 最大值 | `min(a, b)`、`max(a, b)`、`array.max()` |
| 整数转浮点 | `Double(7) / 2` → `3.5` |

```swift
print(7 / 2)
// prints: 3
print(Double(7) / 2)
// prints: 3.5
print(-7 / 2, -7 % 2)
// prints: -3 -1      除法向零截断，余数符号跟着被除数
```

⚠️ 两个整数相除得到整数，这不是 bug 是特性。算平均值时先转 `Double`，或者用 [11 标准库速查]({{< relref "11-Standard-Library.md" >}}) 里的格式化工具。

### 溢出报告：既不想崩，又想知道出了事

`+` 溢出会崩，`&+` 会静默环绕，第三条路是**让它把"溢出了"当返回值告诉你**。这一族方法返回一个元组 `(partialValue:overflow:)`，`partialValue` 是按环绕规则算出来的结果：

```swift
let over = Int.max.addingReportingOverflow(1)
print(over.overflow, over.partialValue)
// prints: true -9223372036854775808

print(Int.max.multipliedReportingOverflow(by: 2).overflow)
// prints: true

print(Int(17).dividedReportingOverflow(by: 5))
// prints: (partialValue: 3, overflow: false)

print(Int8(100).addingReportingOverflow(100).partialValue)
// prints: -56     128 放不进 Int8，环绕成了 -56
```

| 需求 | 写法 |
| --- | --- |
| 加法 / 减法 | `a.addingReportingOverflow(b)`、`a.subtractingReportingOverflow(b)` |
| 乘法 | `a.multipliedReportingOverflow(by: b)` |
| 除法 / 取余 | `a.dividedReportingOverflow(by: b)`、`a.remainderReportingOverflow(dividingBy: b)` |
| "装得下才给我" | `Int(exactly: someValue)` → `Int?`，装不下给 `nil` |

⚠️ 唯一一个**除法也会溢出**的组合是 `Int.min / -1`（结果比 `Int.max` 还大 1）。它同样有报告版本：`Int.min.dividedReportingOverflow(by: -1).overflow` 是 `true`。但直接写常量测不到——编译器会在编译期先报 `division '-9223372036854775808 / -1' results in an overflow`，得让除数经过一个变量或函数调用才测得到（实测）。

💭 这族 API 适合"用户输入的两个数相乘"这种既不想崩、又必须知道结果可不可信的场景：拿到 `overflow == true` 就返回一条友好的错误，而不是让进程消失。

### 二进制与位运算常用属性

写协议解析、权限位、哈希这些东西时，下面这几个属性比手写循环好用：

```swift
let mask: UInt8 = 0b1011_0000
print(mask.nonzeroBitCount, UInt8(1).leadingZeroBitCount, UInt8(0b1000_0000).trailingZeroBitCount)
// prints: 3 7 7     1011_0000 里有三个 1；后两个数是"高位 / 低位连续几个 0"

print(Int8(-5).signum(), Int8(-5).magnitude)
// prints: -1 5

print(UInt16(0x0102).byteSwapped == 0x0201)
// prints: true

print(Int8.bitWidth, Int16(1).bitWidth)
// prints: 8 16

print(String(0b1011_0000, radix: 2))
// prints: 10110000
```

| 属性 / 方法 | 含义 |
| --- | --- |
| `x.nonzeroBitCount` | 二进制里 1 的个数（popcount） |
| `x.leadingZeroBitCount` / `x.trailingZeroBitCount` | 高位 / 低位连续 0 的个数 🔥 求"最高位在哪"常用 |
| `x.bitWidth` | 类型一共多少位（是**类型属性**，写在类型上） |
| `x.signum()` | 符号：`-1` / `0` / `1` |
| `x.magnitude` | 丢掉符号的绝对值，类型变成对应的无符号类型 |
| `x.byteSwapped` | 字节序翻转，网络字节序转换用得上 |
| `x.littleEndian` / `x.bigEndian` | 按指定字节序取同一段位模式 |
| `x.words` | 拆成机器字数组（大整数实现才用得到）🝖 |

💭 这些能力都来自 `FixedWidthInteger` 协议，`Int`、`UInt8` 这些定长整数全都遵守它。泛型里想用这些 API，约束就写 `T: FixedWidthInteger`。

## 浮点

```swift
let a: Double = 1.0 / 3.0
print(a)
// prints: 0.3333333333333333
print(Double.pi, Double.infinity, -Double.infinity)
// prints: 3.141592653589793 inf -inf
print(1e3, 1.5e-3, 0x1p2)
// prints: 1000.0 0.0015 4.0
```

### 特殊值与安全判断

| 属性 / 方法 | 作用 |
| --- | --- |
| `x.isNaN` | 判断是不是 NaN 🔥 |
| `x.isFinite` | 既不是 NaN 也不是 ±inf |
| `x.isInfinite` | 是 ±inf |
| `x.rounded()` | 四舍五入到最接近的整数，`.5` 一律远离零（`2.5 → 3`） |
| `x.rounded(.toNearestOrEven)` | 银行家舍入法：`.5` 舍到偶数（`2.5 → 2`、`3.5 → 4`） |
| `x.rounded(.down)` / `.up` / `.towardZero` / `.toNearestOrAwayFromZero` | 指定其他舍入规则 |
| `x.ulp` | 相邻可表示浮点之间的距离 🝖 |
| 保留两位小数 | `(x * 100).rounded() / 100`，标准库没有 `scale:` 参数 |

```swift
print(Double.nan == Double.nan)
// prints: false    ⚠️ NaN 连自己都不等于自己
print(Double.nan.isNaN)
// prints: true

print(0.1 + 0.2 == 0.3)
// prints: false    浮点数永远的经典
print(0.1 + 0.2)
// prints: 0.30000000000000004

print((2.5).rounded(), (2.5).rounded(.toNearestOrEven))
// prints: 3.0 2.0      默认不是银行家舍入，要银行家那套得自己写
```

⚠️ **永远不要用 `==` 比较两个浮点数**，要比较就用误差范围：

```swift
func almostEqual(_ a: Double, _ b: Double, tolerance: Double = 1e-9) -> Bool {
    abs(a - b) < tolerance
}
print(almostEqual(0.1 + 0.2, 0.3))
// prints: true
```

💭 涉及金额的计算请用整数分单位，或者 Foundation 的 `Decimal`，别和二进制浮点讲道理。

### 浮点的邻居与余数

整数有 `+` `%`，浮点这边对应的两个工具叫法更长：

```swift
print(7.5.truncatingRemainder(dividingBy: 2))
// prints: 1.5
print((-7.5).truncatingRemainder(dividingBy: 2))
// prints: -1.5      符号跟被除数，和整数的 % 一个规矩

print(7.5.remainder(dividingBy: 2))
// prints: -0.5      IEEE 取余：商取"最近的整数"，所以 7.5 减去 8

print((1.0).nextUp > 1.0, (1.0).nextDown < 1.0)
// prints: true true
```

| 写法 | 含义 |
| --- | --- |
| `x.truncatingRemainder(dividingBy: y)` | 商向零截断取余，等价于 C 的 `fmod` 🔥 |
| `x.remainder(dividingBy: y)` | IEEE 取余，商取最近的整数，结果可能和被除数异号 🝖 |
| `x.nextUp` / `x.nextDown` | 相邻的下一个 / 上一个可表示浮点数 |
| `x.ulp` | 当前量级下"一格"有多大 |
| `x.exponent` / `x.significand` | 拆成指数与尾数，写数值分析才用得到 🝖 |

⚠️ **Swift 的 `%` 只给整数。** 写 `7.5 % 2` 会报 `'%' is unavailable: For floating point numbers use truncatingRemainder instead`（实测），照它说的改就行。

### 算钱请用 `Decimal`

`Double` 的 `0.1 + 0.2 != 0.3` 不是 bug，是二进制浮点的本性。要按人习惯的十进制算，就用 Foundation 的 `Decimal`：

```swift
import Foundation

let a = Decimal(string: "0.1")!
let b = Decimal(string: "0.2")!
print(a + b)
// prints: 0.3
print(a + b == Decimal(string: "0.3")!)
// prints: true          同样是十进制，这里就没有 0.30000000000000004

print(Decimal(1) / Decimal(3))
// prints: 0.33333333333333333333333333333333333333
```

⚠️ `Decimal` 也不是万能的：它是**十进制**浮点，有效数字大约 38 位，除法照样会除不尽；而且它和 `Double` 不能混算，得显式转。🝖

💭 金额三条路，按推荐顺序：**整数分单位 → `Decimal` → 先想清楚再碰 `Double`**。展示时再用 `formatted(.currency(code:))` 把整数分或 `Decimal` 变好看。

### 常用数学函数

这些来自标准库或 Foundation，多数需要 `import Foundation`：

| 函数 | 说明 |
| --- | --- |
| `x.squareRoot()` | 平方根，标准库 |
| `abs(x)` | 绝对值，标准库 |
| `min(a, b)` / `max(a, b)` | 取小 / 取大，标准库 |
| `pow(a, b)` | 幂，需要 Foundation |
| `round(x)` / `floor(x)` / `ceil(x)` | 取整（返回浮点），需要 Foundation |
| `sin` `cos` `tan` `log` `exp` | 三角与指数，需要 Foundation |

```swift
import Foundation

print((2.0).squareRoot())
// prints: 1.4142135623730951
print(pow(2, 10))
// prints: 1024        ⚠️ 两个整数字面量会选中 Foundation 的 Decimal 重载
print(pow(Double(2), 10))
// prints: 1024.0      要 Double 就得把类型说清楚
```

⚠️ `pow` 有 `(Double, Double)` 和 `(Decimal, Int)` 两个重载，而 `2`、`2.0` 这种字面量两边都能去，于是 `pow(2.0, 10)` 直接报 `ambiguous use of 'pow'`。老老实实写 `pow(Double(2), 10)`，或者先声明成 `let base: Double = 2.0`。

## 数值与字符串之间的转换

Swift **不做隐式转换**：`Int` 和 `Double` 之间、数字和字符串之间，都要显式说一句。规矩就一条——**凡是可能失败的，返回可选值；凡是可能丢信息的，名字里带 `exactly`**。

```swift
print(Double(7) / 2)
// prints: 3.5

print(Int(3.9), Int(-3.9))          // 直接截断，负数也朝零截
// prints: 3 -3
print(Int((3.9).rounded()))         // 要四舍五入就自己先 rounded
// prints: 4

print(Int(exactly: 3.0) ?? -1)
// prints: 3
print(Int(exactly: 3.5) as Any)     // 不精确就不给，绝不悄悄砍一刀
// prints: nil
print(Float(exactly: 16_777_217) as Any)   // Float 放不下这个整数
// prints: nil
print(Float(16_777_217))            // 普通转换只会悄悄取整
// prints: 16777216.0

print(Double(Int.max) == Double(Int.max - 1))
// prints: true
```

💭 最后那个 `true` 就是精度丢失的证据：`Int.max` 和 `Int.max - 1` 是两个不同的整数，塞进 53 位尾数的 `Double` 之后变成了同一个值。**整数运算永远不要借道 `Double`**，尤其是 ID、时间戳、金额这几种大数。

| 需求 | 写法 | 失败 / 丢精度时 |
| --- | --- | --- |
| 整数 → 浮点 | `Double(i)`、`Float(i)` | 大整数会丢精度，不报错 |
| 浮点 → 整数 | `Int(d)` | 小数被截断；NaN、±inf、超范围**直接崩** |
| 浮点 → 整数（安全版） | `Int(exactly: d)` | 给 `Int?`，不精确就是 `nil` |
| 浮点 → 浮点 | `Double(f)`、`Float(d)` | 可能有舍入，用 `exactly:` 问清楚 |
| 整数 → 字符串 | `String(i)`、`"\(i)"` | 不会失败 |
| 字符串 → 整数 | `Int("42")` | 返回 `Int?`，非法输入给 `nil` |
| 任意进制 → 整数 | `Int("ff", radix: 16)` | 同上 |
| 整数 → 任意进制字符串 | `String(255, radix: 16)` | 给 `"ff"` |
| 字符串 → 浮点 | `Double("1.5")` | 返回 `Double?` |
| 字符 → 数字 / ASCII | `c.wholeNumberValue`、`c.asciiValue` | 都是可选值 |
| 任意值 → 字符串 | `String(describing:)`、`String(reflecting:)` | 见 [15 章]({{< relref "15-Macros-and-Debugging.md" >}}) |

```swift
print(Int("42") ?? -1)
// prints: 42
print(Int(" 42 ") as Any)
// prints: nil       ⚠️ 前后空白不认，先 trimming 再转
print(Int("ff", radix: 16) ?? -1)
// prints: 255
print(String(255, radix: 16), Double("1.5") ?? -1)
// prints: ff 1.5
print("3.14".first!.wholeNumberValue ?? -1)
// prints: 3
```

⚠️ **`Int(d)` 和 `Int(exactly: d)` 的区别值得记一辈子**：前者"能转就转，转不了就崩"，后者"不精确就返回 `nil`"。处理外部数据用后者，处理自己刚算出来的、确定在范围内的值用前者。

## Bool

```swift
let ok = true
let done = !ok          // done == false

print(ok && !done || false)
// prints: true       && 比 || 紧，所以先算 (ok && !done)
print(ok && (done || false))
// prints: false      括号一加，结果就翻了
```

`Bool` 只有 `true` / `false` 两个值，**没有** 0/1 的隐式转换。要转数字自己写：`ok ? 1 : 0`。

## Character

`Character` 表示**一个扩展字形簇**，不是"一个字节"，也不是"一个 Unicode 标量"。

```swift
let letter: Character = "A"
let flag: Character = "🇨🇳"
let family: Character = "👨‍👩‍👧‍👦"
print(flag, family)
// prints: 🇨🇳 👨‍👩‍👧‍👦
```

常用判断：

| 属性 | 说明 |
| --- | --- |
| `isLetter` `isNumber` `isWhitespace` `isPunctuation` | 字符类别 |
| `isUppercase` `isLowercase` | 大小写 |
| `isASCII` | 是否落在 ASCII 范围内 |
| `isHexDigit` | 十六进制数字 |
| `wholeNumberValue` | 数字的数值，支持 `"Ⅷ"` 这类字符 |
| `asciiValue` | ASCII 码，非 ASCII 返回 `nil` |

```swift
print("7".first!.wholeNumberValue ?? -1)
// prints: 7
print("Ⅷ".first!.wholeNumberValue ?? -1)
// prints: 8
print("A".first!.isUppercase)
// prints: true
```

⚠️ `Character` 与 `String` 不能混用。`let c: Character = "ab"` 是编译错误，而 `"a" + "b"` 里两个都是 `String`。要给 `Character` 拼字符串，用 `String(c)` 或者 `"" + String(c)`。

## String

### 创建方式

| 写法 | 结果 |
| --- | --- |
| `"hello"` | 普通字符串 |
| `"""` 多行 `"""` | 多行字符串，自动去掉公共缩进 |
| `#"C:\path"#` | 原始字符串，反斜杠不转义 |
| `#"\#(value)"#` | 原始字符串里的插值要写成 `\#(...)` |
| `String(repeating: "ab", count: 3)` | `ababab` |
| `String(42)` / `String(describing:)` | 从其他值构造 |
| `String(decoding: bytes, as: UTF8.self)` | 从字节构造，非法序列会被替换 |
| `String(validating: bytes, as: UTF8.self)` | 同上，但非法序列返回 `nil` |

### 多行字符串

```swift
let poem = """
    第一行
    第二行
    """
print(poem)
// prints: 第一行
//         第二行
```

规则只有两条：**结束的 `"""` 决定缩进基准**，每行多出来的缩进会被剥掉；想保住前导空格就在结束符号左侧多留空格。

```swift
let indented = """
        前面有四个空格
    """
print("[\(indented)]")
// prints: [    前面有四个空格]
```

上面这段里，内容行缩进 8 格、结束符号缩进 4 格，于是每行剥掉 4 格，结果保留了 4 个空格。**缩进基准由结束符号决定**——这也是为什么结束的 `"""` 不能顶格写在左边。

### 原始字符串

处理正则、路径、JSON 时非常省事：

```swift
let path = #"C:\Users\dev\file.txt"#
print(path)
// prints: C:\Users\dev\file.txt

let name = "Swift"
let greeting = #"你好，\#(name)"#
print(greeting)
// prints: 你好，Swift

let pattern = #"\\d+\.\\d+"#
print(pattern)
// prints: \\d+\.\\d+
```

### 插值与转义

| 写进字符串 | 得到 |
| --- | --- |
| `\(表达式)` | 任意表达式的字符串形式 🔥 |
| `\n` `\t` `\r` `\"` `\\` | 换行、制表、回车、引号、反斜杠 |
| `\0` | 空字符 |
| `\u{1F600}` | 指定码位，`😀` |
| `\(a, b)` | ⚠️ **不是合法语法**，Swift 5 起已移除元组插值 |

```swift
let x = 3, y = 4
print("\(x) + \(y) = \(x + y)")
// prints: 3 + 4 = 7
print("坐标为 (\(x), \(y))")
// prints: 坐标为 (3, 4)
print("坐标为 \(String(describing: (x, y)))")
// prints: 坐标为 (3, 4)
print("\u{1F600}")
// prints: 😀
```

⚠️ 一次插多个值必须**并排写**：`"\(x), \(y)"`。老教程里的 `"\(x, y)"` 在 Swift 5 就被移除了，现在它不是"能跑但不推荐"，而是**编译失败**——编译器会把它解析成标准库里那个 `appendInterpolation(_:default:)`，于是报 `missing argument label 'default:'`（值不是 `String` 时报的是"要求遵守 `StringProtocol`"）。真想插一整个元组，就 `String(describing:)` 包一层。

⚠️ 插值会调用 `description`。可选值插进去会带上 `Optional(...)` 包装：

```swift
let maybe: Int? = 5
print("值是 \(maybe)")
// prints: 值是 Optional(5)
print("值是 \(maybe ?? 0)")
// prints: 值是 5
```

### 自定义插值：给自己的类型造语法

插值不是内建魔法，它只是 `String.StringInterpolation` 上的一组 `appendInterpolation` 方法。给这个类型写扩展，就能往 `\( )` 里塞任何你想得到的写法：

```swift
extension String.StringInterpolation {
    mutating func appendInterpolation(_ value: Int, repeated times: Int) {
        appendLiteral(String(repeating: String(value), count: times))
    }
    mutating func appendInterpolation(hex value: Int) {
        appendLiteral("0x" + String(value, radix: 16))
    }
}

print("\(7, repeated: 3)")
// prints: 777
print("\(hex: 255)")
// prints: 0xff
```

### 索引与切片（最容易踩的地方）

`String` 的索引**不是整数**。原因很简单：UTF-8 字节、Unicode 标量、扩展字形簇是三套不同的计数单位，没有一个整数能同时对上。所以 Swift 给你一个 `String.Index`。

```swift
let s = "Hello, Swift"

print(s[s.startIndex])
// prints: H
print(s[s.index(s.startIndex, offsetBy: 7)])
// prints: S
print(s[s.index(before: s.endIndex)])
// prints: t

print(s.prefix(5), s.suffix(5))
// prints: Hello Swift

let comma = s.firstIndex(of: ",")!
print(String(s[..<comma]))
// prints: Hello
print(String(s[s.index(after: comma)...]))   // 注意结果前面那个空格也是内容
// prints:  Swift
```

⚠️ 三条纪律：

1. `s[s.index(...)]` 返回的是 `Character`，要变回字符串得用 `String(...)`。
2. `s.index(_:offsetBy:)` 是 **O(n)** 的，在循环里按索引逐个取字符会变成 O(n²)。需要频繁按位取字符时先转 `Array(s)`。
3. `s[0]` 永远不合法，这不是 Swift 在为难你。

### Substring：切片的免费与代价

切片返回 `Substring` 而不是 `String`，它和原字符串**共享同一块内存**，所以切片本身不复制数据。

```swift
let original = "Hello, Swift"
let piece = original.prefix(5)
print(type(of: piece))
// prints: Substring
print(piece.uppercased())
// prints: HELLO
```

⚠️ 只要 `piece` 活着，整个 `original` 就不会被释放。如果切片要长期持有，记得 `String(piece)` 拷一份——这是内存泄漏的高发区。

### 索引的算术：distance 与 limitedBy

索引拿到手之后，常见的四种"算一算"：

```swift
let s = "Hello, 世界"
let i = s.index(s.startIndex, offsetBy: 7)
print(s[i], s.distance(from: s.startIndex, to: i))
// prints: 世 7

print(s.index(s.startIndex, offsetBy: 100, limitedBy: s.endIndex) as Any)
// prints: nil      越界时给 nil，而不是崩

print(s.indices.count, s[s.index(before: s.endIndex)])
// prints: 9 界
```

| 需求 | 写法 |
| --- | --- |
| 前后挪 n 位 | `s.index(i, offsetBy: n)` |
| 挪，但别越界 | `s.index(i, offsetBy: n, limitedBy: s.endIndex)` → `String.Index?` |
| 两个索引差多远 | `s.distance(from: a, to: b)` 🔥 数的是 `Character` 个数 |
| 上一个 / 下一个 | `s.index(before: i)`、`s.index(after: i)` |
| 走遍每个下标 | `for i in s.indices { }`、`s.indices.count` |

⚠️ 这些操作都是 **O(n)**，因为它们得按字形簇一个个数过去。`s.indices.count` 和 `s.count` 一样慢，别在循环条件里反复调。

### 三个视角：字形簇、UTF-8、Unicode 标量

同一个 `String`，按不同单位数出来的长度完全不一样。这不是 Swift 在找麻烦，而是"长度"这个词在 Unicode 世界里本来就有歧义：

```swift
let s = "Hello, 世界"
print(s.count, s.utf8.count, s.unicodeScalars.count, s.utf16.count)
// prints: 9 13 9 9      "世界"各占 3 个 UTF-8 字节

print(Array(s.utf8).prefix(5))
// prints: [72, 101, 108, 108, 111]
print(String(decoding: Array(s.utf8), as: UTF8.self))
// prints: Hello, 世界
print(s.unicodeScalars.filter { $0.value > 127 }.map(String.init).joined())
// prints: 世界
```

| 视角 | 拿到什么 | 单位 |
| --- | --- | --- |
| `s.count`、`for c in s` | 扩展字形簇，用户眼里的"一个字" | `Character` |
| `s.utf8` | 字节序列，写文件 / 算哈希 / 走网络用 | `UInt8` |
| `s.utf16` | UTF-16 码元，和 `NSString`、`NSRange` 打交道时用 | `UInt16` |
| `s.unicodeScalars` | Unicode 标量，处理编码细节时用 | `Unicode.Scalar` |
| `String(decoding:as:)` | 把字节按指定编码还原成字符串 | — |

⚠️ `s.utf8.count` 和 `s.count` 不一样，所以**不能用"字符数"去分配字节缓冲区**。要把字符串交给 C 或写进文件，先 `Array(s.utf8)`；反过来还原就用 `String(decoding:as:)`，它比 `String(bytes:encoding:)` 宽容（非法字节会变成替换字符，而不是给 `nil`）。

### 常用 API

| 需求 | 写法 |
| --- | --- |
| 长度 | `s.count`（数的是字形簇，O(n)） |
| 是否为空 | `s.isEmpty` |
| 拼接 | `"a" + "b"`、`var s = ""; s += "x"`、`["a","b"].joined()` |
| 查找子串 | `s.contains("abc")`（标准库）、`s.range(of: "abc")`（Foundation） |
| 前后缀 | `s.hasPrefix("He")`、`s.hasSuffix("ft")` |
| 位置 | `s.firstIndex(of: "l")`、`s.lastIndex(of: "l")` |
| 替换 | `s.replacingOccurrences(of: "l", with: "L")`（Foundation） |
| 替换区间 | `var t = s; t.replaceSubrange(t.startIndex...t.index(t.startIndex, offsetBy: 4), with: "Howdy")` |
| 分隔 | `s.split(separator: ",")` 返回 `[Substring]`（标准库）；`s.components(separatedBy: ",")` 返回 `[String]`（Foundation） |
| 去空白 | `s.trimmingCharacters(in: .whitespacesAndNewlines)`（Foundation） |
| 大小写 | `s.uppercased()`、`s.lowercased()`（标准库）、`s.capitalized`（Foundation） |
| 反转 | `String(s.reversed())` |
| 多次重复 | `String(repeating: s, count: 3)` |
| 逐字符处理 | `for c in s`、`s.map { ... }`、`s.filter(\.isNumber)` |
| 全角 / 半角 | `s.applyingTransform(.fullwidthToHalfwidth, reverse: false)`（Foundation）🝖 |

```swift
print("a,b,,c".split(separator: ",").count)
// prints: 3      默认丢弃空子串
print("a,b,,c".split(separator: ",", omittingEmptySubsequences: false).count)
// prints: 4
```

### 比较

```swift
let a = "café"              // é 是单个码位
let b = "cafe\u{301}"       // e + 组合重音
print(a == b)
// prints: true            Swift 按"规范化等价"比较，这点非常正确
print(a.count, a.unicodeScalars.count)
// prints: 4 4

print("Z" < "a")
// prints: true            大写字母排在前面
print("apple" < "banana")
// prints: true
```

需要更聪明的比较时用 `compare(_:options:)`：

```swift
import Foundation

print("file10".compare("file9", options: .numeric) == .orderedDescending)
// prints: true            按数字大小比，"file10" > "file9"
print("Hello".compare("hello", options: .caseInsensitive) == .orderedSame)
// prints: true
```

## 正则表达式

Swift 5.7 起正则成为语言的一部分，可以用 `/.../ ` 字面量写，并做编译期检查。

```swift
let log = "2026-09-16 ERROR disk full"
let pattern = /(\d{4})-(\d{2})-(\d{2})\s+(\w+)/

if let m = log.firstMatch(of: pattern) {
    print(m.0)
    // prints: 2026-09-16 ERROR
    print(m.1, m.2, m.3, m.4)
    // prints: 2026 09 16 ERROR
}

print(log.contains(/ERROR/))
// prints: true

let rewritten = log.replacing(pattern) { match in "\(match.4)@\(match.1)" }
print(rewritten)
// prints: ERROR@2026 disk full
```

⚠️ `/.../ ` 字面量在包含 `/` 的文本里会很难看，此时用原始字面量 `#/.../#`。另外，正则字面量需要运行时支持，部署目标低于 macOS 13 / iOS 16 时请改用 `NSRegularExpression`。

### 动态构造

```swift
let dynamic = try! Regex(#"(\d{4})"#)
print("year 2026".contains(dynamic))
// prints: true
```

### RegexBuilder：让复杂正则能读

```swift
import RegexBuilder

let word = OneOrMore(.word)
let digits = OneOrMore(.digit)

let rule = Regex {
    Capture { digits }
    "@"
    Capture { word }
}

if let m = "u42@example".firstMatch(of: rule) {
    print(m.1, m.2)
    // prints: 42 example
}
```

🔥 正则超过一行、或者需要嵌套分组时，RegexBuilder 的可维护性比一行"符号汤"高一个量级。它还能配合 `TryCapture` 直接产出强类型值 🝖。

## 格式化

Swift 5.7 引入的 `FormatStyle` 是现在推荐的做法，它按**当前区域设置**输出，还能在 SwiftUI 里以实时刷新的方式使用。

两代写法先摆在一起看：

{{< tabpane text=true persist=disabled >}}

{{% tab header="FormatStyle（推荐）" %}}

```swift
import Foundation

print(1234.5.formatted(.number.precision(.fractionLength(2))))
// prints: 1,234.50
print(0.256.formatted(.percent.precision(.fractionLength(1))))
// prints: 25.6%
print(1234.5.formatted(.currency(code: "CNY")))
// prints: ¥1,234.50
```

类型安全、可组合、可自定义，SwiftUI 里还能直接当参数用。

⚠️ `FormatStyle` 和 `.formatted(...)` 住在 **Foundation** 里，不是标准库。忘了 `import Foundation` 时的报错很有迷惑性：`value of type 'Double' has no member 'formatted'`——看上去像"这个方法不存在"，其实只是没导入。

{{% /tab %}}

{{% tab header="String(format:)（老写法）" %}}

```swift
import Foundation

print(String(format: "%.2f", 1234.5))
// prints: 1234.50
print(String(format: "%.1f%%", 25.6))
// prints: 25.6%
```

方便复制 C 的格式串，但**不做类型检查**，参数与占位符对不上会在运行时炸。

{{% /tab %}}

{{< /tabpane >}}

```swift
import Foundation

print(1234567.formatted())
// prints: 1,234,567

print(1234.5.formatted(.number.precision(.fractionLength(2))))
// prints: 1,234.50

print(0.256.formatted(.percent.precision(.fractionLength(1))))
// prints: 25.6%

print(1234.5.formatted(.currency(code: "CNY")))
// prints: ¥1,234.50
```

| 用途 | 写法 |
| --- | --- |
| 千分位 | `.formatted()` 或 `.formatted(.number)` |
| 固定小数位 | `.formatted(.number.precision(.fractionLength(2)))` |
| 百分比 | `.formatted(.percent)` |
| 货币 | `.formatted(.currency(code: "CNY"))` |
| 科学计数 | `.formatted(.number.notation(.scientific))` |
| 日期 | `date.formatted(date: .abbreviated, time: .shortened)` |
| 相对时间 | `date.formatted(.relative(presentation: .named))` |
| 时长 | `Duration.seconds(90).formatted(.units(allowed: [.minutes, .seconds]))` 🆕 |
| 列表 | `["a", "b", "c"].formatted(.list(type: .and))` |
| 字节数 | `123456.formatted(.byteCount(style: .file))` |

⚠️ **格式化结果依赖区域设置。** 上面所有输出都是在本机 `zh_CN` 环境下跑出来的；如果在别的区域跑，千分位和货币符号会变。写测试时要么固定 locale，要么别断言字符串。

### 老写法：String(format:)

需要 C 风格格式串时还能用，但要 `import Foundation`，而且**不做类型检查**——参数与占位符对不上会在运行时出问题。

```swift
import Foundation

print(String(format: "%.2f", 3.14159))
// prints: 3.14
print(String(format: "%05d", 42))
// prints: 00042
print(String(format: "%@", "hi"))
// prints: hi
```

## 陷阱速查

| 陷阱 | 正确做法 |
| --- | --- |
| 整数除法截断 | 先转 `Double`，`Double(a) / Double(b)` |
| 浮点用 `==` 比较 | 用容差函数，或者比较 `rounded()` 后的整数 |
| `NaN` 判等 | 用 `isNaN`，别用 `==` |
| `s[0]` 取字符 | 用 `s.first` 或 `s.startIndex` |
| 循环里按索引取字符 | 先 `Array(s)`，否则 O(n²) |
| 切片长期持有 | `String(slice)` 复制一份 |
| 可选值写进插值 | 用 `??` 兜底，否则会打印 `Optional(...)` |
| 靠 `count` 判断"字节长度" | `s.utf8.count` 才是字节数 |
| `split` 丢掉空段 | 加 `omittingEmptySubsequences: false` |
| 格式化结果写进断言 | 固定 locale，或者比较数值本身 |
