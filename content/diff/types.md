+++
title = "types"
date = 2026-09-18T22:24:56+08:00
weight = 1
type = "docs"
description = "18 种语言的数据类型横向对照：整型、浮点、复合、自定义与其他类型，每个主题用标签页切换语言"
isCJKLanguage = true
draft = false

+++

# 数据类型对照：18 种语言

同一件东西——"一个整数"——在 18 种语言里有 18 种说法：有的语言默认只有 32 位，有的干脆没有上限；有的溢出就崩溃，有的溢出悄悄给你一个负数，有的语言**根本没有整型**。本页按数据类型分类，每一类用标签页切换语言，每个标签里给出：**类型清单 → 定义与字面量 → 最值 → 计算与溢出 → 比较 → 常见陷阱**。没有这个类型的语言，会直接说明"没有"以及通常的替代做法。

读法约定：

| 记号 | 含义 |
| --- | --- |
| `// prints:` | 该行注释是真实跑出来的输出 |
| ⚠️ | 易错点，踩过一次就该记住 |
| 🛑 | 错误示例或会崩溃/报错/未定义的行为 |
| 📘 | 官方文档或权威资料链接 |

> 版本基线（写作时 2026-09，均为各语言当前稳定版）：Rust 1.98、Swift 6.4、Go 1.27、Python 3.14、Kotlin 2.4、Java 26（LTS 25）、C++23、C23、Julia 1.13、C# 14 / .NET 10、Dart 3.13、R 4.6、Zig 0.15、Lua 5.5、TypeScript 7、Node 26、PHP 8.5、Ruby 4.0。

---

## 整型

整型是所有语言里分歧最大的地方，可以用四个问题把 18 种语言分开：

1. **有没有固定宽度类型**——是 `int` 一种走天下，还是 `i8/i16/i32/i64` 全家桶？
2. **默认类型是什么**——写 `42` 得到的到底是 32 位、64 位还是任意精度？
3. **溢出怎么办**——崩溃（trap）、回绕、变浮点、未定义行为，还是根本不溢出？
4. **有符号和无符号怎么相遇**——混算时谁转成谁？

**一页速览**

| 语言 | 默认/常用类型 | 位宽 | 溢出时 | 任意精度 |
| --- | --- | --- | --- | --- |
| Rust | `i32` | 8/16/32/64/128 + `isize` | debug 崩溃、release 回绕；`wrapping_*`/`checked_*`/`saturating_*` 可选 | ✗ |
| Swift | `Int` | 平台字长 + 8/16/32/64/128 | 默认 trap（崩溃）；`&+` 才回绕 | ✗ |
| Go | `int` | 平台字长 + 8/16/32/64 | 静默回绕 | ✗ |
| Python | `int` | 无限 | 不存在 | ✓ |
| Kotlin | `Int` | 8/16/32/64（含无符号） | 静默回绕；`Math.addExact` 可检查 | ✗ |
| Java | `int` | 8/16/32/64（无无符号） | 静默回绕；`Math.addExact` 可检查 | `BigInteger` |
| C++ | `int` | 实现定义 + `<cstdint>` 固定宽度 | 有符号 UB、无符号回绕 | ✗ |
| C | `int` | 实现定义 + `<stdint.h>` 固定宽度 | 有符号 UB、无符号回绕；C23 `ckd_*` 可检查 | ✗ |
| Julia | `Int`（= `Int64`） | 8/16/32/64/128 + 无符号 | 静默回绕；`Base.Checked` 可检查 | `BigInt` |
| C# | `int` | 8/16/32/64/128 + `nint` | 默认回绕；`checked` 抛异常 | `BigInteger` |
| Dart | `int` | VM 64 位；Web ±2⁵³ | VM 回绕；Web 丢精度 | `BigInt` |
| R | `integer`（`1L`） | 32 位；默认数字是 double | 变 `NA` + 警告 | `bit64` / `gmp` |
| Zig | `comptime_int` → 目标类型 | 任意位宽 `iN`/`uN` | 安全模式崩溃；`+%` 回绕、`+\|` 饱和 | `std.math.big` |
| Lua | `integer` | 64 位有符号 | 回绕 | ✗ |
| TypeScript | `number` | 双精度，±2^⁵³ 安全 | 丢精度且不报错 | `bigint` |
| JavaScript | `number` | 同上 | 同上 | `bigint` |
| PHP | `int` | 平台字长 | **静默变 float** | `gmp` / `bcmath` |
| Ruby | `Integer` | 无限 | 不存在 | ✓ |

**逐语言详解**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的整数是固定宽度、二进制补码表示的值类型，共 12 种：`i8`/`i16`/`i32`/`i64`/`i128`/`isize` 与对应的无符号版本；字面量默认推断为 `i32`，溢出行为由编译模式决定。

**类型清单**

| 类型 | 宽度 | 说明 |
| --- | --- | --- |
| `i8` `i16` `i32` `i64` `i128` | 8/16/32/64/128 位 | 有符号，补码 |
| `u8` `u16` `u32` `u64` `u128` | 同上 | 无符号 |
| `isize` / `usize` | 指针宽度（本机 64） | 索引、长度、指针差值专用 |

**定义与字面量**

```rust
let a = 42;            // 默认 i32
let b: i64 = -9_000_000_000;
let c = 42u8;          // 后缀决定类型
let d = 0xFF_u32;      // 十六进制
let e = 0b1010_1010;   // 二进制
let f = 0o755;         // 八进制
let g = 1_000_000;     // 下划线纯属人类友好

let h: i32 = "42".parse().unwrap();
let i = i32::from_str_radix("ff", 16).unwrap();   // 255
let j = 'A' as u32;                               // char → u32
```

**最值**

```rust
i32::MIN    // -2147483648
i32::MAX    // 2147483647
u8::MAX     // 255
i64::BITS   // 64
usize::BITS // 64（本机）
```

**计算：溢出是"编译模式"决定的**

```rust
let x: u8 = 250;
x + 10                  // 🛑 debug：panic（attempt to add with overflow）；release：4
x.wrapping_add(10)      // 4       显式回绕
x.checked_add(10)       // None    显式检查，返回 Option
x.overflowing_add(10)   // (4, true)            结果 + 溢出标志
x.saturating_add(10)    // 255     饱和到边界
```

`profile` 决定默认行为：debug 打开 `overflow-checks`，release 关闭。想要 release 也检查，在 `Cargo.toml` 里写 `[profile.release] overflow-checks = true`。

除法向零截断，`%` 的符号跟被除数；除零和 `i32::MIN / -1` **在任何模式都 panic**（这是仅剩的两种"永远检查"的算术）。想要可控版本用 `checked_div` / `wrapping_div`；想要地板语义用 `div_euclid` / `rem_euclid`。

```rust
println!("{} {} {}", -7 / 2, -7 % 2, (-7).div_euclid(2));
// prints: -3 -1 -4
println!("{}", (-7i32).rem_euclid(2));
// prints: 1
```

**比较：不同类型连 `==` 都不给**

```rust
let a: u8 = 255;
let b: i32 = 256;
// a < b                     // 🛑 mismatched types
(a as i32) < b               // true：as 只截断/重解释，不做检查
i32::try_from(a).unwrap() < b // true：转换带检查
```

上面这段代码演示了三种定义方式（默认 `i32`、显式类型/后缀、`parse` 解析）以及 `MIN`/`MAX` 与四种溢出 API 的用法。要点是：溢出行为由编译 profile 决定（debug 崩溃、release 回绕），但"除零"和 `i32::MIN / -1` 在任何模式下都会 panic，所以生产代码要么用 `checked_*` 显式检查，要么明确选 `wrapping_*`/`saturating_*` 表达意图。

📘 [Rust Reference · Numeric types](https://doc.rust-lang.org/reference/types/numeric.html)、[Operator expressions · overflow](https://doc.rust-lang.org/reference/expressions/operator-expr.html#overflow)、[std::num](https://doc.rust-lang.org/std/num/)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的整数是值类型：`Int`/`UInt` 跟随平台字长（Apple 平台 64 位），另有 `Int8`~`Int64`、`UInt8`~`UInt64` 与 `Int128`/`UInt128`；字面量默认是 `Int`，溢出默认直接崩溃（trap）。

**类型清单**

| 类型 | 宽度 | 说明 |
| --- | --- | --- |
| `Int` / `UInt` | 平台字长（Apple 平台 64 位） | 默认整数类型就是 `Int` |
| `Int8` `Int16` `Int32` `Int64` / `UInt8` `UInt16` `UInt32` `UInt64` | 8/16/32/64 位 | 与 C 的定宽类型一一对应 |
| `Int128` / `UInt128` | 128 位 | Swift 6 起，64 位平台可用 |

**定义与字面量**

```swift
let a = 42                 // Int
let b: Int64 = -9_000_000_000
let c: UInt8 = 0xFF
let d = 0b1010_1010
let e = 0o755
let f = 1_000_000
let g = Int("42")          // Int?，解析失败给 nil（不是崩溃）
let h = Int("4x")          // nil
```

**最值**

```swift
Int.max      // 9223372036854775807
Int.min      // -9223372036854775808
UInt8.max    // 255
Int64.min    // -9223372036854775808
Int128.max   // 170141183460469231731687303715884105727
```

**计算：默认就是"崩溃派"**

```swift
var a = Int.max
a += 1        // 🛑 Fatal error: arithmetic overflow（debug 和 release 都崩）

Int8(127) &+ 1   // -128   回绕
Int8(-128) &- 1  // 127    回绕
Int8(127) &* 2   // -2     回绕
```

Swift 只有 `&+` `&-` `&*` 三个回绕运算符（**没有** `&/`、`&%`）。需要"溢出时怎么办"的选择权，就用带上报版本：

```swift
let o = Int8(120).addingReportingOverflow(10)
// (partialValue: -126, overflow: true)
let m = Int8(12).multipliedReportingOverflow(by: 10)
// (partialValue: 120, overflow: false)
```

除法向零截断，`%` 符号跟被除数，除零与 `Int.min / -1` 都 trap；配套 API 是 `quotientAndRemainder(dividingBy:)`、`isMultiple(of:)`。

```swift
print(-7 / 2, -7 % 2)              // -3 -1
print((17).quotientAndRemainder(dividingBy: 5))  // (3, 2)
print((9).isMultiple(of: 3))       // true
print(Double(7) / 2)               // 3.5（想要小数就得先转 Double）
```

**比较：必须显式转换**

```swift
let big: UInt8 = 255
// big < 256            // 🛑 Binary operator '<' cannot be applied to 'UInt8' and 'Int'
Int(big) < 256          // true
UInt8(exactly: 300)     // nil：可失败转换
UInt8(clamping: 300)    // 255：饱和转换
```

代码先展示 `Int`/`Int64`/`UInt8` 的写法与最值，再用 `a += 1` 演示默认 trap、用 `&+` 演示回绕。Swift 与 C 系最大的区别就在这：溢出默认直接崩溃（安全性优先），想要回绕必须显式写 `&+`/`&-`/`&*`，想要"带溢出标志"用 `addingReportingOverflow` 这类 API。

📘 Swift 标准库：`FixedWidthInteger`、`BinaryInteger`、`Numeric`

{{% /tab %}}

{{% tab header="Go" %}}

Go 的整数分两类：平台相关的 `int`/`uint`（本机 64 位）和定宽的 `int8`~`int64`、`uint8`~`uint64`；`byte` 是 `uint8` 的别名，`rune` 是 `int32` 的别名，溢出静默回绕。

**类型清单**

| 类型 | 宽度 | 说明 |
| --- | --- | --- |
| `int` / `uint` | 平台字长（本机 64 位） | 别拿它当"固定 64 位"用 |
| `int8/16/32/64`、`uint8/16/32/64` | 定宽 | 协议、文件格式里用这些 |
| `byte` | = `uint8` | 别名，不是新类型 |
| `rune` | = `int32` | 存 Unicode 码点 |
| `uintptr` | 指针宽度 | 无符号，专给 unsafe 用 |

**定义与字面量**

```go
var a int = 42
var b int32 = -2_000_000_000
var c uint8 = 0xFF
var d byte = 'A'          // byte 就是 uint8
r := '中'                  // rune（int32），值是 20013
n := int64(42)            // 显式转换：Go 没有隐式数值转换

v, err := strconv.ParseInt("ff", 16, 64)   // 255, nil
u := 0b1010_1010          // 二进制字面量
```

**最值（`math` 包，Go 1.17+）**

```go
math.MaxInt8    // 127
math.MaxUint8   // 255
math.MaxInt64   // 9223372036854775807
math.MaxInt     // 9223372036854775807（随平台）
math.MinInt     // -9223372036854775808
```

**计算：静默回绕，没有任何提示**

```go
var i int8 = 127
i++                 // -128    静默回绕，不 panic、不告警
var u uint8 = 255
u++                 // 0
```

Go 没有 `checked_add` 之类的标准 API：要么自己写边界判断（`if a > math.MaxInt64-b`），要么用 `math/bits` 做位级运算。`//` 不是注释以外的运算：除法向零截断，除零 panic（`runtime error: integer divide by zero`），但 `math.MinInt64 / -1` 按语言规范**等于** `math.MinInt64`（回绕，不 panic）。

```go
fmt.Println(8/2, -7/2, -7%2)   // 4 -3 -1
```

**比较：类型必须一致**

```go
var a int32 = 1
// a == int64(1)        // 🛑 invalid operation: mismatched types
a == 1                  // ok：1 是无类型常量，自动适配
a == int32(int64Val)    // 显式转换
```

⚠️ 经典死循环：`uint` 永远 `>= 0`。

```go
var n uint = 3
for i := n - 1; i >= 0; i-- { }   // 🛑 i 是 uint，条件恒真
for i := int(n) - 1; i >= 0; i-- { }  // ✅ 用有符号 int
```

代码给出定宽类型、`rune`/`byte` 别名、显式 `int64()` 转换与 `math` 里的最值常量。要点是"没有隐式转换 + 溢出静默回绕"：无符号变量做递减会死循环，跨平台协议里别用 `int`，而 `math.MinInt64 / -1` 也不会 panic（按规范回绕）。

📘 [Go spec · Arithmetic operators](https://go.dev/ref/spec#Arithmetic_operators)、[math 常量](https://pkg.go.dev/math#pkg-constants)

{{% /tab %}}

{{% tab header="Python" %}}

Python 只有一种整数类型 `int`，而且是任意精度的——没有上限、不会溢出；`bool` 是 `int` 的子类。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `int` | 任意精度整数，没有上限 |
| `bool` | `int` 的子类（`True == 1`，`isinstance(True, int)` 为真） |
| `float` | C double；`int` 与它混算会提升为 `float` |
| `decimal.Decimal` / `fractions.Fraction` | 需要十进制精度或精确分数时用 |

**定义与字面量**

```python
a = 42                 # int
b = 10 ** 100          # 1267650600228229401496703205376
c = 0xFF               # 255
d = 0b1010_1010        # 170
e = 0o755              # 493
f = 1_000_000
g = int("42")          # 42
h = int("ff", 16)      # 255
i = int("2A", 36)      # 106
j = int(3.9)           # 3（向零截断）
k = int(-3.9)          # -3
l = int.from_bytes(b"\x01\x00", "little")   # 1
m = (255).to_bytes(2, "big")                # b'\x00\xff'
```

**最值：没有这回事**

Python 的 `int` 是任意精度，**不存在 `INT_MAX`**。`sys.maxsize` 是"容器的长度上限"（64 位平台上是 2⁶³−1），不是 `int` 的上限——`sys.maxsize + 1` 照样算得好好的。

```python
import sys
sys.maxsize          # 9223372036854775807
sys.maxsize + 1      # 9223372036854775808
```

**计算：整数永不溢出，混入 float 才丢精度**

```python
float(2**53 + 1)        # 9007199254740992.0 ← 精度丢了
(2**53 + 1) == float(2**53)   # False（int 与 float 的比较是精确的）
0.1 + 0.2 == 0.3        # False（浮点问题，不是整数问题）
```

除法语义和 C 系相反，这是 Python 最常被踩的地方：

```python
7 / 2       # 3.5   真除法，永远给 float
7 // 2      # 3     地板除法（向 -∞）
-7 // 2    # -4    ← 不是 -3！
-7 % 2     # 1     % 的符号跟除数
divmod(-7, 2)   # (-4, 1)
1 // 0      # 🛑 ZeroDivisionError
```

`//` 与 `%` 满足 `a == (a // b) * b + a % b`，所以负数取模的结果总是非负（当 `b > 0`）。此外 `math.isqrt(10**40 + 1)` 给整数平方根，`divmod` 一次拿商余，`x.bit_length()` 给位数。

**比较：`==` 是值，`is` 是身份**

```python
2**53 == float(2**53)           # True
2**53 + 1 == float(2**53 + 1)   # False ← 比较是精确的，是 float() 转换丢了那一位
1 == True                       # True
eval("1000") is eval("1000")   # False：两个不同对象
1000 == 1000                   # True
```

CPython 缓存 −5 到 256 的小整数，所以小整数上的 `is` 可能"碰巧"为真——**绝不要用 `is` 比较数值**，它只用来和 `None`/`True`/`False` 这类单例比较。字典键也遵循值语义：

```python
{True: "a", 1: "b"}    # {True: 'b'}：True 和 1 是同一个键
```

代码演示任意精度整数（`10 ** 100`）、`int()` 的解析与截断，以及 `//`、`%` 在负数上的行为。要点是：Python 整数不会溢出，但 `//` 是地板除（`-7 // 2 == -4`），`int()` 对浮点是向零截断，而 3.11+ 还限制 `int`↔`str` 的默认位数。

📘 [Python docs · Numeric types](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)、[PEP 237](https://peps.python.org/pep-0237/)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的整数是 JVM 上的定宽值类型 `Byte`/`Short`/`Int`/`Long`，以及 Kotlin 1.5 起稳定的无符号版本 `UByte`/`UShort`/`UInt`/`ULong`；字面量默认是 `Int`。

**类型清单**

| 类型 | 宽度 | 说明 |
| --- | --- | --- |
| `Byte` / `Short` / `Int` / `Long` | 8/16/32/64 位 | 有符号，`Int` 是默认 |
| `UByte` / `UShort` / `UInt` / `ULong` | 同上 | 无符号，Kotlin 1.5 起稳定 |

**定义与字面量**

```kotlin
val a = 42                 // Int
val b: Long = 9_000_000_000L
val c: Byte = 0x7F
val d = 0b1010_1010        // 二进制可以；Kotlin 没有八进制字面量
val e = 0xFF_EC_DE_5E
val f = 42u                // UInt
val g = 42uL               // ULong
val h = 0x7F                // 127

val i = "42".toInt()             // NumberFormatException 风险
val j = "42".toIntOrNull()       // Int?
val k = "ff".toInt(16)           // 255
```

**最值**

```kotlin
Int.MAX_VALUE    // 2147483647
Int.MIN_VALUE    // -2147483648
Byte.MAX_VALUE   // 127
Long.MAX_VALUE   // 9223372036854775807
UInt.MAX_VALUE   // 4294967295
Int.SIZE_BITS    // 32
```

**计算：回绕由 JVM 负责，编译器不吭声**

```kotlin
val intNumber: Int = Int.MAX_VALUE
println(intNumber + 1)   // -2147483648
println(-Int.MIN_VALUE)  // -2147483648  ← 取负也会"溢出"

Math.addExact(Int.MAX_VALUE, 1)      // 🛑 ArithmeticException
Math.multiplyExact(Int.MAX_VALUE, 2) // 🛑 ArithmeticException
val narrowed: Byte = 130.toByte()    // -126：窄化就是截断
```

除法向零截断；除零抛 `ArithmeticException`；`Int.MIN_VALUE / -1` 在 JVM 上**回绕成 `Int.MIN_VALUE`**（不抛异常）。想要地板语义用 Kotlin 1.5 起自带的 `floorDiv` / `mod`：

```kotlin
println(-7 / 2)          // -3   向零截断
println(-7 % 2)          // -1   符号跟被除数
println(-7.floorDiv(2))  // -4   地板除法
println(-7.mod(2))       // 1    符号跟除数
1 / 0                    // 🛑 ArithmeticException: / by zero
```

**比较：赋值不隐式拓宽，但算术表达式可以混类型**

```kotlin
val intNumber = 1
val longNumber = 1000L
val result = intNumber + longNumber   // Long：运算符重载自动定结果类型
// val bad: Long = intNumber          // 🛑 type mismatch：赋值必须显式
val good: Long = intNumber.toLong()
```

无符号与有符号之间**不能**混算，必须 `toUInt()` / `toInt()` 显式转换。另外 Kotlin 的 `==` 编译成 `equals`，装箱也按值比较，这一点和 Java 相反：

```kotlin
val p: Int? = 1000
val q: Int? = 1000
p == q      // true
p === q     // false（两个不同的装箱对象）
```

代码给出 `Int`/`Long`/`Byte`/`UInt` 的写法与最值，并用 `Math.addExact` 演示检查算术、用 `floorDiv`/`mod` 演示地板语义。要点是：Kotlin 整数静默回绕（`Int.MAX_VALUE + 1` 变成 `MIN_VALUE`），`Int.MIN_VALUE / -1` 也回绕；混合类型算术合法，但赋值给更宽类型必须显式转换。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的整数是定宽的基本类型 `byte`/`short`/`int`/`long`，全部有符号；`char` 是唯一的无符号 16 位整数类型，溢出静默回绕。

**类型清单**

| 类型 | 宽度 | 说明 |
| --- | --- | --- |
| `byte` / `short` / `int` / `long` | 8/16/32/64 位 | 全部有符号，**没有无符号整型** |
| `char` | 16 位无符号 | 唯一的无符号整型，用来存 UTF-16 码元 |
| 包装类 `Byte`/`Short`/`Integer`/`Long` | — | 装箱后有缓存和 `==` 陷阱 |

**定义与字面量**

```java
int a = 42;
long b = 9_000_000_000L;      // L 后缀别忘了
short c = 32_000;
byte d = 127;
char e = 'A';                 // 65
int f = 0b1010_1010;          // 二进制（Java 7+）
int g = 0xFF_EC_DE_5E;
int h = 010;                  // 八进制！值是 8

int i = Integer.parseInt("42");
int j = Integer.parseInt("ff", 16);              // 255
int k = Integer.parseUnsignedInt("4294967295");  // -1（按无符号语义解析）
long l = Integer.toUnsignedLong(-1);             // 4294967295
```

**最值**

```java
Integer.MAX_VALUE   // 2147483647
Integer.MIN_VALUE   // -2147483648
Integer.SIZE        // 32
Byte.MAX_VALUE      // 127
Long.MAX_VALUE      // 9223372036854775807
Long.SIZE           // 64
Character.MAX_VALUE // 65535
```

**计算：回绕静默，检查要靠 `Math.*Exact`**

```java
int m = Integer.MAX_VALUE + 1;              // -2147483648，静默
Math.addExact(Integer.MAX_VALUE, 1);        // 🛑 ArithmeticException
Math.multiplyExact(Integer.MAX_VALUE, 2);   // 🛑 ArithmeticException
Math.toIntExact(9_000_000_000L);            // 🛑 ArithmeticException
```

除法向零截断；除零抛 `ArithmeticException: / by zero`；**`Integer.MIN_VALUE / -1` 静默回绕成 `Integer.MIN_VALUE`**，这是 JDK 规范明确定义的行为，也是非常经典的坑。地板语义用 `Math.floorDiv` / `Math.floorMod`：

```java
System.out.println(-7 / 2);                    // -3
System.out.println(-7 % 2);                    // -1
System.out.println(Math.floorDiv(-7, 2));      // -4
System.out.println(Math.floorMod(-7, 2));      // 1
```

**比较：装箱 `==` 是引用比较**

```java
Integer x = 127, y = 127;
System.out.println(x == y);      // true  ← 命中 -128..127 的缓存
Integer p = 128, q = 128;
System.out.println(p == q);      // 🛑 false！不同对象
System.out.println(p.equals(q)); // true
```

代码演示字面量（二进制/十六进制/下划线）、`parseInt` 与 `parseUnsignedInt` 的差别，以及 `Math.addExact`、`toUnsignedLong` 的用法。要点是：Java 没有无符号整型（只有 `char`），溢出静默回绕；无符号操作"靠方法而不是靠类型"，包装类的 `==` 还有缓存陷阱。

无符号运算靠静态方法：`Integer.compareUnsigned(a, b)`、`divideUnsigned`、`remainderUnsigned`、`toUnsignedString`。真正的任意精度用 `BigInteger`（不可变、无溢出、但慢）。

📘 JLS §15.17（除法与取模）、`java.lang.Math`、`java.lang.Integer`

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的整数有两套：宽度由实现决定的 `short`/`int`/`long`/`long long`，以及 `<cstdint>` 里保证精确宽度的 `int8_t`~`int64_t`、`uint8_t`~`uint64_t`；有符号溢出是未定义行为。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `short` / `int` / `long` / `long long` | 至少 16/16/32/64 位，实际宽度由实现决定 |
| `<cstdint>`：`int8_t` `int16_t` `int32_t` `int64_t`、`uint8_t` `uint16_t` `uint32_t` `uint64_t` | 固定宽度（存在则保证精确） |
| `int_leastN_t` / `int_fastN_t` / `intmax_t` / `intptr_t` | 至少 N 位 / 最快 / 最大 / 能装指针 |
| `char` / `signed char` / `unsigned char` | `char` 的符号性由实现决定 |
| `char16_t` / `char32_t` / `char8_t`（C++20） | 字符类型，不是数值类型 |

**定义与字面量**

```cpp
#include <cstdint>
#include <limits>

int a = 42;
long long b = 9'000'000'000LL;      // C++14 数字分隔符
std::int8_t c = -128;
std::uint64_t d = 0xFFFF'FFFF'FFFF'FFFFULL;
auto e = 0b1010'1010;               // C++14
auto f = 010;                       // 八进制！值是 8
```

**最值：只有 `numeric_limits` 是权威**

```cpp
std::numeric_limits<int>::max();       // 2147483647
std::numeric_limits<int>::min();       // -2147483648（整型是"最小"，不是最低）
std::numeric_limits<int>::lowest();    // -2147483648
std::numeric_limits<unsigned>::max();  // 4294967295
```

**计算：有符号溢出是未定义行为**

```cpp
unsigned u = std::numeric_limits<unsigned>::max();
u + 1;                                  // 0，良定义（模 2^N）

int i = std::numeric_limits<int>::max();
i + 1;                                  // 🛑 UB：可能回绕，也可能被优化掉
int r;
bool over = __builtin_add_overflow(i, 1, &r);   // GCC/Clang：over == true
```

要检查溢出有几条路：编译器内建 `__builtin_add/sub/mul_overflow`、UBSan（`-fsanitize=signed-integer-overflow`）、`-ftrapv`；C++26 会带来 `std::add_sat` / `sub_sat` / `mul_sat` / `saturate_cast`。**不要**指望 `-fwrapv` 之外的行为是可移植的。

除法向零截断（C++11 起保证）；除零是 UB；`INT_MIN / -1` 也是 UB。`%` 的符号跟被除数；`std::div` 一次拿商余。

**比较：有符号/无符号混比是祖传陷阱**

```cpp
int i = -1;
unsigned u = 1;
if (i < u) { /* 🛑 条件不成立：i 被转成 4294967295 */ }
if (std::cmp_less(i, u)) { /* ✅ C++20：true，安全比较 */ }
```

`<utility>` 里的 `std::cmp_equal` / `cmp_not_equal` / `cmp_less` / `cmp_greater` 系列专治这个。另外 C++20 的 `std::ssize(x)` 返回 `ptrdiff_t`，不用再和 `size_t` 的无符号较劲；`<=>` 提供三路比较。

窄化转换不会报错但会截断，列表初始化会拦住一部分：

```cpp
int x{2.5};                              // 🛑 编译错误：窄化
std::uint8_t y = static_cast<std::uint8_t>(300);   // 44
```

代码给出 `std::numeric_limits` 的最值写法、`__builtin_add_overflow` 与 `std::cmp_less`。混合有符号/无符号比较要用 `std::cmp_*` 系列，`char` 的符号性由实现决定。

{{% /tab %}}

{{% tab header="C" %}}

C 的整数同样分"实现定义宽度"（`char`/`short`/`int`/`long`/`long long`）与 `<stdint.h>` 的定宽类型；有符号溢出是未定义行为，无符号溢出按模 2^N 回绕。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `char` / `short` / `int` / `long` / `long long` | 宽度的下限是 8/16/16/32/64 位，实际由实现决定 |
| `unsigned` 前缀 | 只有"无符号"这一种修饰，没有真正的定宽保证 |
| `<stdint.h>`：`int8_t` `int16_t` `int32_t` `int64_t`、`uint8_t` `uint16_t` `uint32_t` `uint64_t` | 定宽（存在则精确），`intmax_t`、`intptr_t`、`size_t` 各有用途 |
| `_Bool` / `bool`（C23 起是关键字） | 布尔，参与整型提升 |

**定义与字面量**

```c
#include <limits.h>
#include <stdint.h>
#include <inttypes.h>

int a = 42;
long long b = 9000000000LL;
uint8_t c = 0xFF;
int64_t d = -9223372036854775807LL - 1;
size_t e = sizeof(int);
printf("%" PRId64 "\n", d);      // 可移植格式串在 <inttypes.h>
int v = 0b1010;                  // C23 标准；老编译器当扩展
int w = 1'000'000;               // C23 数字分隔符
```

**最值：全部在头文件里**

```c
INT_MAX       // 2147483647
INT_MIN       // -2147483648
UINT_MAX      // 4294967295
LLONG_MAX     // 9223372036854775807
CHAR_BIT      // 8
SIZE_MAX      // 18446744073709551615
INT64_MAX     // <stdint.h>
```

**计算：有符号 UB，无符号回绕**

```c
unsigned u = UINT_MAX;
u + 1;                       // 0，良定义
int i = INT_MAX;
i + 1;                       // 🛑 UB：编译器可以假设它不会发生

int r;
bool over = ckd_add(&r, INT_MAX, 1);   // C23 <stdckdint.h>：over == 1, r == INT_MIN
```

C23 的 `<stdckdint.h>` 提供 `ckd_add` / `ckd_sub` / `ckd_mul`，返回"是否溢出"的布尔值，是标准库层面第一次正经解决这个问题。旧标准下只能靠 `__builtin_*_overflow`（GCC/Clang）、`-fwrapv`（把有符号溢出错就成回绕）、`-ftrapv`、或者 UBSan。

除法：C99 起向零截断；除零是 UB；`INT_MIN / -1` 是 UB；`%` 符号跟被除数；`div()` / `ldiv()` / `lldiv()` 一次拿商余。

**比较：整型提升 + 有符号/无符号相遇**

```c
int a = -1;
unsigned b = 1;
if (a < b) { }               // 🛑 不成立：a 被转成 UINT_MAX
if (a < (int)b) { }          // 显式转换（前提是 b 能被 int 表示）
```

`sizeof` 返回 `size_t`（无符号），于是 `for (int i = 0; i < sizeof(x); i++)` 这类写法会触发 `-Wsign-compare`（**一定要开 `-Wall -Wextra`**）。C23 还带来 `_BitInt(N)` 任意位宽整数、二进制字面量、`nullptr`。

```c
unsigned _BitInt(8) x = 200;   // C23：8 位无符号，任意位宽
```

代码展示 `<limits.h>` 的宏、无符号回绕以及 C23 的 `ckd_add`。要点是：C 只有"无符号回绕"与"有符号 UB"两种命运，C23 的 `<stdckdint.h>` 才给了标准化的检查算术；比较时 `int` 与 `unsigned` 相遇会按无符号比较，这是最经典的坑。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的整数是机器整数类型：`Int8`~`Int128`、`UInt8`~`UInt128`，`Int`/`UInt` 是平台字长别名（64 位平台上即 `Int64`/`UInt64`）；`BigInt` 提供任意精度。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `Int8` `Int16` `Int32` `Int64` `Int128` / `UInt8` `UInt16` `UInt32` `UInt64` `UInt128` | 定宽，补码 |
| `Int` / `UInt` | 平台字长别名（64 位平台上就是 `Int64`） |
| `Bool` | 8 位，`Bool <: Integer` |
| `BigInt` | 任意精度（`Base.GMP`） |
| `Rational` | 精确分数，另算一类 |

**定义与字面量**

```julia
a = 42                # Int（64 位平台上即 Int64）
b = Int8(42)
c = Int128(42)
d = big"123456789012345678901234567890"   # BigInt
e = 0x1F              # UInt8
f = 0b1010_1010       # UInt8
g = 1_000_000
h = parse(Int, "42")
i = parse(Int, "ff", base=16)   # 255
j = Int8(200)         # 🛑 InexactError：超出范围
```

**最值**

```julia
typemax(Int64)    # 9223372036854775807
typemin(Int64)    # -9223372036854775808
typemax(UInt8)    # 0xff
typemax(Int128)   # 170141183460469231731687303715884105727
```

**计算：定宽回绕，需要检查用 `Base.Checked`**

```julia
typemax(Int8) + Int8(1)                            # -128，静默回绕
Base.Checked.checked_add(typemax(Int8), Int8(1))   # 🛑 OverflowError
Base.Checked.add_with_overflow(typemax(Int8), Int8(1))  # (结果, 溢出标志)
abs(typemin(Int8))                                 # -128 ← abs 也会溢出
```

Julia 的除法家族比别的语言都齐全，而且各有明确含义：

```julia
7 / 2        # 3.5    / 永远给 Float64
7 ÷ 2        # 3      div：向零截断
-7 ÷ 2       # -3
div(-7, 2)   # -3
fld(-7, 2)   # -4     向 -∞
cld(-7, 2)   # -3     向 +∞
rem(-7, 2)   # -1     符号跟被除数
mod(-7, 2)   # 1      符号跟除数
divrem(-7, 2)   # (-3, -1)
fldmod(-7, 2)   # (-4, 1)
div(1, 0)    # 🛑 DivideError
1 / 0        # Inf（浮点除零不报错）
```

**比较：跨类型也按数学值来，安全**

```julia
-1 < UInt(1)       # true   ← 有符号/无符号混比在 Julia 里不会翻车
Int8(1) == UInt8(1) # true
1 == 1.0           # true
1 === 1.0          # false（=== 还要求类型一致）
```

代码给出 `typemax`/`typemin`、`Base.Checked` 系列与 `div`/`fld`/`rem`/`mod` 的差异。要点是：定宽整数静默回绕（连 `abs(typemin(Int8))` 都还是负数），检查算术要显式用 `Base.Checked`，而"向零、向 -∞、符号跟除数还是被除数"在 Julia 里有四个不同的函数。

📘 [Julia · Integers and Floating-Point Numbers](https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/)、[`Base.Checked`](https://docs.julialang.org/en/v1/base/math/#Base.Checked)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的整数是值类型 `sbyte`/`byte`/`short`/`ushort`/`int`/`uint`/`long`/`ulong`，另有原生字长的 `nint`/`nuint` 与 128 位的 `Int128`/`UInt128`（.NET 7+）；默认 unchecked，溢出静默回绕。

**类型清单**

| 类型 | 宽度 | 说明 |
| --- | --- | --- |
| `sbyte` / `short` / `int` / `long` | 8/16/32/64 位 | 有符号 |
| `byte` / `ushort` / `uint` / `ulong` | 同上 | 无符号 |
| `nint` / `nuint` | 原生字长 | C# 9 起，是真数值类型 |
| `Int128` / `UInt128` | 128 位 | .NET 7 / C# 11 起 |
| `char` | 16 位无符号 | UTF-16 码元 |

**定义与字面量**

```csharp
int a = 42;
long b = 9_000_000_000L;
byte c = 0xFF;
sbyte d = -128;
nuint e = 42;
Int128 f = Int128.MaxValue;      // .NET 7+
int g = 0b1010_1010;             // C# 7 起
int h = 0x1F;

int i = int.Parse("42");
bool ok = int.TryParse("42", out int j);
int k = Convert.ToInt32("ff", 16);       // 255
```

**最值**

```csharp
int.MaxValue      // 2147483647
int.MinValue      // -2147483648
byte.MaxValue     // 255
long.MaxValue     // 9223372036854775807
Int128.MaxValue   // 170141183460469231731687303715884105727
```

**计算：默认 unchecked（静默回绕），要检查得开口**

```csharp
int m = int.MaxValue + 1;                     // -2147483648，静默
int n = unchecked(int.MaxValue + 1);          // 同上，明确表达"我就要回绕"
checked { int o = int.MaxValue + 1; }         // 🛑 OverflowException
int p = checked(int.MaxValue + 1);            // 🛑 OverflowException
Convert.ToInt32(9_000_000_000L);              // 🛑 OverflowException
```

可以整个项目打开溢出检查（`<CheckForOverflowUnderflow>true</CheckForOverflowUnderflow>`），也可以只包住关键代码块。除法向零截断；除零**永远**抛 `DivideByZeroException`；`int.MinValue / -1` 在 unchecked 下回绕成 `int.MinValue`，在 checked 下抛 `OverflowException`——同一个表达式，行为取决于上下文。

```csharp
int q = -7 / 2;              // -3
int r = -7 % 2;              // -1
int s = int.MinValue / -1;   // -2147483648（unchecked）
```

**比较：值类型没问题，装箱后要小心**

```csharp
object x = 128, y = 128;
Console.WriteLine(x == y);            // false（object 的 == 是引用比较）
Console.WriteLine((int)x == (int)y);  // true
```

代码演示 `int`/`uint`/`Int128` 的写法，以及 `checked`、`unchecked`、`Convert.ToInt32` 三者的区别。要点是：默认 unchecked（静默回绕），只有 `checked`/`checked{}` 才抛 `OverflowException`；`int.MinValue / -1` 在 unchecked 下回绕、checked 下抛异常，行为取决于上下文。

📘 C# 语言规范：integer types、`checked`/`unchecked`、`System.Int128`

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 只有一种整数类型 `int`：在 VM 上是 64 位二进制补码，编译到 Web 时退化成 JS number（精确范围约 ±2⁵³，位运算被截断到 32 位）。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `int` | VM 上是 64 位补码；Web 上是 JS number（±2⁵³ 精确） |
| `BigInt` | 任意精度，`dart:core` |
| `Int8List` `Uint8List` `Uint8ClampedList` `Int16List` `Uint16List` `Int32List` `Uint32List` `Int64List` `Uint64List` | `dart:typed_data`，固定宽度缓冲区 |

**定义与字面量**

```dart
var a = 42;
var b = 0xFF;              // 255
var c = 0b1010_1010;       // 170
var d = 1_000_000;

var e = int.parse("42");
var f = int.parse("ff", radix: 16);   // 255
var g = int.tryParse("4x");           // null
var h = BigInt.parse("123456789012345678901234567890");
var i = 42.toRadixString(16);         // "2a"
var j = 0.5.truncate();               // 0
```

**最值：没有现成常量**

Dart 的 `int` 没有 `MAX_VALUE` 之类的常量，需要边界就自己写：

```dart
const maxInt = 0x7FFFFFFFFFFFFFFF;   // 2^63 - 1（VM）
const minInt = -0x7FFFFFFFFFFFFFFF - 1;   // -2^63（VM）
maxInt.bitLength;                    // 63
```

**计算：VM 回绕，Web 丢精度**

```dart
var m = 0x7FFFFFFFFFFFFFFF;
m + 1;                    // -9223372036854775808（VM：补码回绕）
m * 2;                    // -2（VM）
```

⚠️ 同一段代码在 Web 上完全不是这个行为：编译成 JS 后 `int` 就是 double，`m + 1` 变成 `9.223372036854776e+18`，位运算还会被截断到 32 位。**需要跨 Web 的位运算或超过 2⁵³ 的整数，请用 `BigInt` 或 `Int32List`/`Uint8List` 这类 typed data。**

除法语义两套并存：

```dart
7 / 2       // 3.5   / 永远返回 double
7 ~/ 2      // 3     向零截断的整除
-7 ~/ 2     // -3
-7 % 3      // 2     % 是欧几里得模，结果永远非负
(-7).remainder(3)   // -1  余数跟被除数
1 ~/ 0      // 🛑 UnsupportedError
1 % 0       // 🛑 UnsupportedError
1 / 0       // Infinity（浮点除零不报错）
```

`>>` 是算术右移，`>>>`（Dart 2.14+）是无符号右移。

**比较**

```dart
1 == 1.0            // true（按数值比较，int 与 double 可以相等）
identical(1, 1)     // true
1.compareTo(2)      // -1
```

代码给出 `int`/`BigInt`/`Int32List` 三种形态与手写的最值常量。要点是：Dart 的 `int` 在 VM 上是 64 位（回绕），编译到 Web 后退化成 JS number（超过 2⁵³ 丢精度、位运算截到 32 位），所以跨平台数据要用 `BigInt` 或字符串承载。

📘 [dart:core · int](https://api.dart.dev/stable/latest/dart-core/int-class.html)

{{% /tab %}}

{{% tab header="R" %}}

R 的"整数"是 32 位的 `integer` 类型，字面量必须带 `L`（如 `42L`）；而 R 里默认的数字是双精度 `double`，两者不能混为一谈。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `integer` | 32 位有符号，写法必须带 `L`（`1L`） |
| `double` | **默认数字类型**，`1` 是 double，不是 int |
| `bit64::integer64` | 扩展包的 64 位整数（底层仍是 double，另加类） |
| `numeric` | `integer` 与 `double` 的通称 |

**定义与字面量**

```r
a <- 42L                      # integer
b <- 42                       # double！R 里默认数字是双精度
c <- 0x1F                     # 31（double）
d <- as.integer("42")         # 42
e <- strtoi("0x1f", 16L)      # 31
f <- as.integer(3.9)          # 3（向零截断）

typeof(a); typeof(b)          # "integer" "double"
is.integer(a); is.double(b)   # TRUE TRUE
```

**最值：32 位，只有约 21 亿**

```r
.Machine$integer.max          # 2147483647
-2147483647L - 1L             # -2147483648（唯一的 integer 写法：结果刚好落在边界内）
2147483648L                   # 🛑 NA + 警告：字面量本身就超出 integer 范围
-2147483648L                  # 🛑 同样是 NA：负号在外，先解析 2147483648L
```

**计算：溢出给 NA，不报错**

```r
.Machine$integer.max + 1L
# [1] NA
# Warning message: NAs produced by integer overflow
as.integer(2147483648)        # NA + 警告
as.integer(3.9)               # 3
```

官方文档的原话是：两个整数做 `/` 和 `^` 结果类型是 `numeric`，其他运算符结果仍是 integer；"integer 溢出发生在 ±(2³¹−1)，返回 `NA_integer_` 并给出警告"。

除法与取模是**地板**语义，而且整数除整数仍是整数：

```r
7 / 2        # 3.5    / 总是给 double
7L %/% 2L    # 3
-7L %/% 2L   # -4     地板整除
-7L %% 2L    # 1      余数符号跟除数（sign(r) == sign(y)）
7L %% -2L    # -1
as.integer(7) %% 0L      # NA_integer_（除零不报错，得到特殊值）
```

**比较：类型不同也按数值比，`NA` 要单独判**

```r
1L == 1          # TRUE   按数值
identical(1L, 1) # FALSE  类型不同
1L < 2.0         # TRUE
NA_integer_ == 1 # NA     ← 任何和 NA 的比较都是 NA
is.na(NA_integer_)
```

代码演示 `42L` 与 `42` 的区别、`.Machine$integer.max` 与整数溢出成 `NA` 的现象。要点是：R 的"整数"必须带 `L` 否则是 double；整数溢出给 `NA_integer_` 加警告；`%/%`/`%%` 是地板语义，且两个整数运算的结果仍是整数。

📘 [`?Arithmetic`](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Arithmetic.html)、`?integer`、`?as.integer`

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的整数是任意位宽的类型：写成 `iN`/`uN`（`N` 由你指定，如 `u7`、`i33`），常用宽度有 `i8`~`i128`、`u8`~`u128`，指针宽度用 `isize`/`usize`。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `i8` `i16` `i32` `i64` `i128` / `u8` `u16` `u32` `u64` `u128` | 定宽 |
| `iN` / `uN` | **任意位宽**：`i7`、`u33`、`u0`、`u1` 都合法 |
| `isize` / `usize` | 指针宽度 |
| `comptime_int` | 编译期任意精度，字面量的默认类型 |

**定义与字面量**

```zig
const std = @import("std");

pub fn main() void {
    const a: u8 = 250;
    const b: i32 = -7;
    const c: u7 = 100;         // 任意位宽
    const d = 42;              // comptime_int，按使用场景落到具体类型
    const e = 0b1010_1010;
    const f = 0o755;
    const g = 0xFF;
    const h: u8 = @intCast(256 - 44);        // 显式转换，安全模式带检查
    const i = std.fmt.parseInt(i32, "42", 10) catch 0;
    _ = .{ a, b, c, d, e, f, g, h, i };
}
```

**最值**

```zig
std.math.maxInt(u8)    // 255
std.math.minInt(i32)   // -2147483648
std.math.maxInt(u7)    // 127
@bitSizeOf(u7)         // 7
```

**计算：默认检查，回绕和饱和都要显式写**

```zig
const x: u8 = 250;
x + 10;                  // Debug/ReleaseSafe：panic「integer overflow」；ReleaseFast：UB
x +% 10;                 // 4     回绕
x +| 10;                 // 255   饱和（还有 -|、*|、<<|）
@addWithOverflow(x, 10); // .{ 4, 1 }   结果 + 溢出位
-% @as(i8, -128);        // -128  回绕取负
```

除法与取模在**有符号**操作数上不能直接用 `/` 和 `%`（语言参考要求它们 comptime-known 且为正），运行时一律走内置函数，各自语义写得明明白白：

```zig
@divTrunc(-7, 2);   // -3   向零
@divFloor(-7, 2);   // -4   向 -∞
@divExact(10, 5);   // 2    除不尽就是错误
@rem(-7, 2);        // -1   符号跟被除数
@mod(-7, 2);        // 1    符号跟除数
```

**比较：跨类型靠 peer type resolution，不匹配就编译失败**

```zig
const a: i8 = 12;
const b: i16 = 34;
if (a < b) {}                        // ✅ peer type resolution 提升为 i16

const big: u64 = 1;
const small: i32 = 2;
// if (big < small) {}               // 🛑 编译错误：u64 与 i32 没有共同类型
if (@as(i64, @intCast(big)) < small) {}          // 显式转换后才能比
if (std.math.cast(i32, big)) |v| { _ = v < small; }   // 可失败转换，越界给 null
```

代码展示 `std.math.maxInt`、`+%`（回绕）、`+|`（饱和）与 `@addWithOverflow`。要点是：Zig 默认检查溢出（安全模式 panic），但 `ReleaseFast` 会变成 UB，所以"回绕/饱和"必须显式写出来；有符号除法不能用 `/`，要用 `@divTrunc`/`@divFloor`。

📘 [Zig Language Reference · Operators](https://ziglang.org/documentation/master/#Operators)、[`@divTrunc` / `@divFloor` / `@divExact` / `@rem` / `@mod`](https://ziglang.org/documentation/master/#divTrunc)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 5.3 起数值有 `integer`（64 位有符号）与 `float`（双精度）两个子类型，但都属于 `number` 类型，用 `math.type()` 区分。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `integer` | Lua 5.3 起的子类型，64 位有符号，补码 |
| `float` | 双精度，`type()` 都是 `"number"`，`math.type()` 才区分 |
| 无符号 | **不存在**，最高位就是符号位 |

**定义与字面量**

```lua
local a = 42          -- integer
local b = 3.0         -- float
local c = 0x2A        -- 42
local d = 0x1p4       -- 16.0，十六进制浮点

print(math.type(a), math.type(b))   -- integer  float
print(math.tointeger(3.0))          -- 3
print(math.tointeger(3.5))          -- nil
print(tonumber("42"), math.type(tonumber("42")))    -- 42  integer
print(tonumber("42.0"), math.type(tonumber("42.0"))) -- 42.0  float
print(tonumber("ff", 16))           -- 255
```

**最值**

```lua
math.maxinteger   -- 9223372036854775807
math.mininteger   -- -9223372036854775808
math.maxinteger + 1 == math.mininteger   -- true（回绕）
math.abs(math.mininteger) == math.mininteger  -- true ← 经典陷阱
```

**计算：溢出回绕，除法分两套**

```lua
print(7 / 2)     -- 3.5   / 永远是 float 除法
print(7 // 2)    -- 3     地板除法（向 -∞）
print(-7 // 2)   -- -4
print(-7 % 2)    -- 1     % 的符号跟除数（a - floor(a/b)*b）
print(1 // 0)    -- 🛑 运行时错误：尝试对整数做零除
print(1 % 0)     -- 🛑 同上
print(1 / 0)     -- inf（浮点除零不报错）
print(0 / 0)     -- nan（符号位因平台而异）
```

位运算 `&` `|` `~` `<<` `>>` 全部在 64 位整数上做；位移量超过 64 位直接得 0（定义良好，不是 UB）。

**比较：整数与浮点按数学值精确比较**

```lua
print(1 == 1.0)          -- true
print(1 < 1.5)           -- true
print(math.maxinteger < 2.0^63)   -- true（比较是精确的）

local t = {}
t[1] = "a"
print(t[1.0])            -- a：整值的 float 键会被归一化成整数键
```

代码演示 `math.type`、`//` 与 `%` 的地板语义，以及整数回绕。要点是：Lua 的 `integer` 是 64 位有符号、溢出回绕（`math.abs(math.mininteger)` 仍是负数），`/` 永远给浮点，只有 `//` 和 `%` 才是整数语义。

📘 [Lua 5.5 Reference · Arithmetic Operators](https://www.lua.org/manual/5.5/manual.html#3.4.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有整型：数值就是 `number`（IEEE 754 双精度，安全整数上限 2⁵³−1），需要任意精度整数时用 ES2020 引入的 `bigint`。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `number` | 唯一的"小数/整数"类型，IEEE 754 双精度 |
| `bigint` | 任意精度整数，需要 target ≥ ES2020 |
| 字面量类型 | `42`、`0xFF`、`123n` 可以当类型用 |
| `Int8Array` `Uint8Array` `Uint8ClampedArray` `Int16Array` `Uint16Array` `Int32Array` `Uint32Array` `BigInt64Array` `BigUint64Array` | 固定宽度缓冲区，运行时才有 |

**定义与字面量**

```ts
const a = 42;              // number
const b = 0xFF;            // 255
const c = 0b1010_1010;
const d = 0o755;
const e = 1_000_000;
const f: number = Number("42");
const g = Number.parseInt("ff", 16);     // 255
const h = 123n;                          // bigint（target ≥ ES2020）
const i = BigInt("123456789012345678901234567890");
const j: 42 = 42;                        // 字面量类型
```

**最值：只有"安全范围"这个概念**

```ts
Number.MAX_SAFE_INTEGER;   // 9007199254740991（2^53 - 1）
Number.MIN_SAFE_INTEGER;   // -9007199254740991
Number.MAX_VALUE;          // 1.7976931348623157e+308
Number.EPSILON;            // 2.220446049250313e-16
Number.isSafeInteger(2 ** 53);      // false
```

**计算：类型系统不会替你挡住精度丢失**

```ts
Number.MAX_SAFE_INTEGER + 1 === Number.MAX_SAFE_INTEGER + 2;  // true！
9007199254740993;         // 实际是 9007199254740992
1 << 31;                  // -2147483648  位运算先转 32 位有符号整数
2 ** 31 | 0;              // -2147483648
1n + 1;                   // 🛑 TypeError：Cannot mix BigInt and other types
1n + BigInt(1);           // 2n
```

`bigint` 与 `number` 不能混算，必须显式 `BigInt(x)` / `Number(x)`；除法永远是浮点，整除自己写 `Math.trunc(a / b)`；`%` 的符号跟被除数（`-7 % 3 === -1`），没有 Python/Ruby 的地板语义；除零得 `Infinity`/`NaN` 而不抛错。

**比较**

```ts
1n == 1;      // true   宽松相等会做转换
1n === 1;     // false  类型不同
0.1 + 0.2 === 0.3;   // false
NaN === NaN;  // false，判 NaN 用 Number.isNaN(x)
Object.is(-0, 0);    // false，而 -0 === 0 是 true
```

代码演示 `number`、`bigint`、`Number.MAX_SAFE_INTEGER` 与 32 位位运算的边界。要点是：TS 没有整型，`number` 超过 2⁵³ 会静默丢精度，位运算自动转成 32 位有符号整数；需要精确大整数就用 `bigint`，而且它不能与 `number` 混算。

📘 [TS Handbook · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)、[MDN · BigInt](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/BigInt)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 同样只有 `number`（双精度）与 `bigint` 两种数值类型：`number` 不区分整数与浮点，`bigint` 能表示任意精度整数但不能与 `number` 混算。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `number` | 唯一数值类型，双精度浮点 |
| `bigint` | 任意精度整数（ES2020） |
| `Int8Array` `Uint8Array` `Uint8ClampedArray` `Int16Array` `Uint16Array` `Int32Array` `Uint32Array` `BigInt64Array` `BigUint64Array` | TypedArray，固定宽度缓冲区 |

**定义与字面量**

```js
const a = 42;              // number
const b = 0xFF;            // 255
const c = 0b1010_1010;     // 数字分隔符 ES2021
const d = 0o755;
const e = 1_000_000;
Number("42");              // 42
Number("1_000");           // NaN（Number 不认分隔符）
Number.parseInt("1_000");  // 1
Number.parseInt("ff", 16); // 255
Number.parseInt("08");     // 8（不要依赖隐式八进制）
123n;                      // bigint
BigInt("123456789012345678901234567890");
```

**最值**

```js
Number.MAX_SAFE_INTEGER;   // 9007199254740991
Number.MIN_SAFE_INTEGER;   // -9007199254740991
Number.MAX_VALUE;          // 1.7976931348623157e+308
Number.isInteger(1.0);     // true（1.0 就是 1）
Number.isSafeInteger(2 ** 53);   // false
```

**计算：该丢精度就丢精度，该截断就截断**

```js
9007199254740993;          // 9007199254740992
0.1 + 0.2;                 // 0.30000000000000004
7 / 2;                     // 3.5
Math.trunc(-7 / 2);        // -3   想要整除
Math.floor(-7 / 2);        // -4   想要地板
-7 % 3;                    // -1   % 符号跟被除数
1 / 0;                     // Infinity
0 / 0;                     // NaN
1 << 31;                   // -2147483648
2 ** 31 | 0;               // -2147483648
(-1) >>> 0;                // 4294967295（无符号右移，32 位）
```

⚠️ JSON 不支持 `bigint`：`JSON.stringify(1n)` 直接抛 `TypeError`，`Math.*` 也不接受 `bigint`。传输大整数只能自己约定字符串/分片格式。

**比较**

```js
1n == 1;         // true
1n === 1;        // false
NaN === NaN;     // false
Object.is(NaN, NaN);   // true（Object.is 才是"同值"比较）
```

代码给出 `Number.isSafeInteger`、`Math.trunc`、`Math.round(-0)` 与 `Number.isNaN` 的对比。要点是：JS 只有一种数值类型，`0.1 + 0.2 !== 0.3`、`1 << 31` 溢出、NaN 不等于自身都要靠 API 处理，`BigInt` 也不能直接 JSON 序列化。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 只有一种整型 `int`，宽度等于平台字长（64 位平台上是 64 位）；最特别的一点是整数溢出不会报错，而是静默变成 `float`。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `int` | 平台字长（64 位平台上是 64 位），是唯一整型 |
| `float` | 双精度；整数一旦溢出就**变成它** |
| `gmp` / `bcmath` | 扩展，提供任意精度 |

**定义与字面量**

```php
$a = 42;
$b = 0x1F;          // 31
$c = 0b1010;        // 10
$d = 0o17;          // 15（PHP 8.1+；老写法 017）
$e = 1_000_000;     // PHP 7.4+ 数字分隔符

var_dump(PHP_INT_MAX);   // int(9223372036854775807)
var_dump(PHP_INT_SIZE);  // int(8)：字节数

$f = intdiv(7, 2);       // 3
$g = 7 / 2;              // 3.5
$h = (int) "42";         // 42
$i = intval("ff", 16);   // 255
$j = intval("42abc");    // 42（宽松）
```

**最值**

```php
PHP_INT_MAX     // 9223372036854775807
PHP_INT_MIN     // -9223372036854775808
PHP_INT_SIZE    // 8（字节数；32 位平台上是 4）
```

**计算：溢出变成 float，这是 PHP 最特别的一点**

```php
var_dump(PHP_INT_MAX + 1);      // float(9.2233720368547758E+18)
is_int(PHP_INT_MAX + 1);        // false
var_dump(PHP_INT_MAX);          // int(9223372036854775807)
```

它既不回绕也不报错，而是**悄悄换了个类型**继续算下去——之后的 `intdiv()`、数组下标、`is_int()` 判断都会跟着出问题。

```php
7 / 2;          // 3.5
6 / 3;          // 2（两个整数整除时返回 int）
intdiv(7, 2);   // 3
-7 % 2;         // -1   符号跟被除数
1 / 0;          // 🛑 DivisionByZeroError
intdiv(1, 0);   // 🛑 DivisionByZeroError
intdiv(PHP_INT_MIN, -1);   // 🛑 ArithmeticError
```

**比较：`==` 是雷区，`===` 才是日常**

```php
0 == "abc";      // false（PHP 8 起；PHP 7 及以前是 true，经典坑）
0 == "";         // false（PHP 8 起）
1 == "1";        // true
1 === "1";       // false
"10" == "1e1";   // true：两个数字字符串按数值比
```

代码演示 `intdiv`、`/` 与"整数溢出变 float"这一 PHP 特有的行为。要点是：溢出既不回绕也不报错，而是换成 `float` 继续算（之后 `is_int` 为 false）；除零在 PHP 8 抛 `DivisionByZeroError`，`intdiv(PHP_INT_MIN, -1)` 抛 `ArithmeticError`。

⚠️ 处理金额、ID、雪花算法这种不能丢精度的整数，请用 `bcmath`（字符串运算）或 `gmp`，别用 `int`。

📘 [PHP Manual · Integers](https://www.php.net/manual/en/language.types.integer.php)、[`intdiv`](https://www.php.net/manual/en/function.intdiv.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 只有一种整数类型 `Integer`，它是任意精度的：小整数是"立即数"（比较与哈希很快），超出范围后自动变成大整数，不会溢出。

**类型清单**

| 类型 | 说明 |
| --- | --- |
| `Integer` | 任意精度；小整数是"立即数"优化，Ruby 2.4 起 `Fixnum`/`Bignum` 统一 |
| `Float` | 双精度；与 `Integer` 混算会提升 |
| `Rational` / `BigDecimal` | 精确分数 / 十进制，另算一类 |

**定义与字面量**

```ruby
a = 42                       # Integer
b = 0x2A                     # 42
c = 0b101010                 # 42
d = 0o52                     # 42（八进制）
e = 1_000_000
f = 2**100                   # 1267650600228229401496703205376，没有上限
g = Integer("42")            # 严格解析，失败抛 ArgumentError
h = Integer("ff", 16)        # 255
i = Integer("0x1f")          # 31
j = "ff".to_i(16)            # 255（宽松：碰到非法字符就停）
k = "12abc".to_i             # 12  ← 宽松解析的坑
```

**最值：不存在**

`Integer` 是任意精度，**没有 `Integer::MAX`**。小整数（约 2⁶² 以内）在 MRI 里是"立即数"，`object_id` 稳定、比较极快；超过就自动变成堆上的大整数。

```ruby
2**100                    # 1267650600228229401496703205376
1.equal?(1)               # true（小整数是立即数）
(2**70).equal?(2**70)     # false（大整数是对象）
```

**计算：整数不溢出，浮点才丢精度**

```ruby
(2**53 + 1).to_f          # 9.007199254740992e+15
2**53 + 1 == (2**53 + 1).to_f   # false
```

除法与取模是**地板**语义，和 C 系相反：

```ruby
7 / 2        # 3
-7 / 2       # -4    ← 不是 -3！
-7 % 3       # 2     % 的符号跟除数
-7.divmod(3) # [-3, 2]   divmod 底层就是地板除法：商 -3，余 2
-7.div(3)    # -3         div 同样是地板（不像 C 的向零截断）
-7.fdiv(3)   # -2.3333333333333335
7.ceildiv(2) # 4     向上取整
1 / 0        # 🛑 ZeroDivisionError
1.0 / 0      # Infinity
```

**比较：`==` 按值，`eql?` 还看类型，Hash 用后者**

```ruby
1 == 1.0        # true
1.eql?(1.0)     # false
1 === 1.0       # true（Integer#=== 就是值比较，不是类型检查）
{1 => :a}[1.0]  # nil   ← Hash 用 eql?/hash，整型和浮点不是同一个键
```

代码演示任意精度整数、`/` 的地板语义以及 `divmod`/`fdiv` 的区别。要点是：Ruby 整数不会溢出，`-7 / 2 == -4`（地板），`%` 的符号跟除数；`to_i` 宽松而 `Integer()` 严格，`Integer` 与 `Float` 在 Hash 里是两个不同的键。

⚠️ 严格解析用 `Integer(str, base)`（抛异常），宽松解析用 `to_i`（`"12abc".to_i == 12`）——读用户输入别用后者。

📘 [Ruby · Integer](https://docs.ruby-lang.org/en/master/Integer.html)、[Numeric#divmod](https://docs.ruby-lang.org/en/master/Numeric.html#method-i-divmod)

{{% /tab %}}

{{< /tabpane >}}

---

## 浮点型

浮点型的分歧点比整型更隐蔽：大家几乎都实现 IEEE 754，但**默认类型不同、精度不同、舍入规则不同、有没有十进制类型不同**。这一节的重点不是"怎么写一个字面量"，而是"哪些相等是假的、哪些转换会崩、哪些场合根本不该用浮点"。

**一页速览**

| 语言 | 浮点类型 | 默认 | 十进制 / 定点 | NaN 相关注意 |
| --- | --- | --- | --- | --- |
| Rust | `f32` `f64`（`f16`/`f128` 仍是 nightly） | `f64` | 无，用 `rust_decimal` 等库 | `partial_cmp` 返回 `None`，排序要 `total_cmp` |
| Swift | `Float16` `Float` `Double` | `Double` | `Decimal`（Foundation） | `Int(Double.nan)` 直接崩溃，用 `Int(exactly:)` |
| Go | `float32` `float64` | `float64` | 无，用 `shopspring/decimal` 等库 | 常量表达式精确、变量不精确 —— 同一行代码两种结果 |
| Python | `float` | `float`（双精度） | `decimal.Decimal`、`fractions.Fraction` | `round(2.5) == 2`（银行家舍入） |
| Kotlin | `Float` `Double` | `Double` | `java.math.BigDecimal` | 静态类型是 `Any` 时 NaN 反而"等于自己" |
| Java | `float` `double` | `double` | `BigDecimal` | `Math.round(-2.5) == -2` |
| C++ | `float` `double` `long double`；C++23 `std::float16_t` `std::float32_t` `std::float64_t` `std::float128_t` `std::bfloat16_t` | `double` | 无，用库 | `-ffast-math` 会让 NaN/Inf 假设失效 |
| C | `float` `double` `long double`；C23 `_FloatN`（可选） | `double` | 无，用库 | `==` 对 NaN 恒假，打印要 `%.17g` 或 `%a` |
| Julia | `Float16` `Float32` `Float64` `BigFloat` | `Float64` | `BigFloat`、`Rational` | `Int(3.9)` 抛 `InexactError`（不许悄悄截断） |
| C# | `Half` `float` `double` `decimal` | `double` | `decimal`（base-10，28~29 位） | `double.Epsilon` 不是机器 epsilon |
| Dart | `double`（`Float32List` 拿单精度） | `double` | 无 | 没有 epsilon 常量，`toInt()` 遇 NaN 抛错 |
| R | `double` | `double` | `Rmpfr`、`gmp` | `NA_real_` 与 `NaN` 是两种值，`is.na(NaN)` 为真 |
| Zig | `f16` `f32` `f64` `f80` `f128` `c_longdouble` | 看目标类型 | 无 | 字面量是 `comptime_float`（≥f128 精度） |
| Lua | `float`（双精度） | — | 无 | 只有双精度，没有单精度/长双精度 |
| TypeScript | `number` | `number` | 库（decimal.js 等） | `Math.round(-0.5)` 是 `-0` |
| JavaScript | `number` | `number` | 库 | `JSON.stringify(NaN)` 是 `"null"` |
| PHP | `float` | `float`（双精度） | `bcmath` / `gmp` | `round()` 默认是 half away from zero，不是 IEEE |
| Ruby | `Float` | `Float`（双精度） | `BigDecimal`、`Rational` | `0.0.eql?(-0.0)` 竟然是 `true` |

**逐语言详解**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的浮点遵循 IEEE 754，有 `f32`（单精度）与 `f64`（双精度，字面量默认）两种；`f16`/`f128` 目前仍是 nightly 特性，稳定版用不了。

**类型**：`f32`、`f64`（默认）。`f16`、`f128` 在 1.98 仍是 nightly feature（`#![feature(f16)]`），稳定代码别指望。

```rust
let a = 1.5;            // f64
let b: f32 = 1.5;
let c = 1e-3_f64;
let d = 0x1.8p3_f64;    // 十六进制浮点：1.5 × 2³ = 12
let e = f64::from(1u8); // 整型→浮点只能显式转换
```

| 常量 | 值 |
| --- | --- |
| `f64::MAX` | 1.7976931348623157e308 |
| `f64::MIN_POSITIVE` | 2.2250738585072014e-308（最小正规数） |
| `f64::EPSILON` | 2.220446049250313e-16 |
| `f32::EPSILON` | 1.1920929e-7 |
| `f64::NAN` / `f64::INFINITY` | NaN / ∞ |

```rust
0.1_f64 + 0.2 == 0.3      // false
f64::NAN == f64::NAN      // false
f64::NAN.partial_cmp(&1.0)  // None（要排序用 total_cmp）
(-0.0_f64).is_sign_negative()   // true
```

代码给出 `f32`/`f64` 的写法、`MIN_POSITIVE`/`EPSILON` 等常量和 `as` 转换的结果。要点是：`NaN` 与任何值比较都为假，排序要用 `total_cmp`；Rust 没有隐式数值转换，而浮点转整数是"截断 + 饱和"（`NaN` 变 0、超大值变 `MAX`），不会像 C 那样 UB。

⚠️ 排序浮点切片用 `sort_by(|a, b| a.total_cmp(b))`，直接用 `sort_by(partial_cmp)` 会因为 NaN 里的 `None` 而 panic 或乱序。

📘 [`std::f64`](https://doc.rust-lang.org/std/primitive.f64.html)、[`total_cmp`](https://doc.rust-lang.org/std/primitive.f64.html#method.total_cmp)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的浮点是 IEEE 754 的值类型：`Float16`（Apple 芯片）、`Float`、`Double`（默认），以及 Foundation 提供的十进制 `Decimal`；`NaN` 与任何值比较都为假。

**类型**：`Float16`（Apple 芯片）、`Float`、`Double`（默认）、`Decimal`（Foundation，十进制）。

```swift
let a = 1.5            // Double
let b: Float = 1.5
let c: Float16 = 1.5
let d = Decimal(string: "0.1")!     // 十进制，钱用它
```

| 常量 | 值 |
| --- | --- |
| `Double.greatestFiniteMagnitude` | 1.7976931348623157e308 |
| `Double.leastNonzeroMagnitude` | 5e-324 |
| `Double.ulpOfOne` | 2.220446049250313e-16 |
| `.nan` / `.infinity` / `.signalingNaN` | 特殊值 |

```swift
0.1 + 0.2 == 0.3            // false
Double.nan == Double.nan    // false
Int(3.9)                    // 3（向零截断）
Int(exactly: 3.9)           // nil —— 需要"不丢信息"时用这个
// Int(Double.nan)          // 🛑 运行时崩溃
(2.5).rounded()             // 3.0（默认：四舍五入、远离零）
(2.5).rounded(.toNearestOrEven)   // 2.0（银行家舍入）
```

代码展示 `Float16`/`Float`/`Double`/`Decimal` 与两种舍入模式。要点是：`Double` 是默认类型、`Decimal` 用来表示十进制；`Int(Double.nan)` 会直接崩溃，安全转换要用 `Int(exactly:)`；判 NaN 用 `.isNaN`，需要全序用 `.isTotallyOrdered`。

📘 Swift 标准库：`FloatingPoint`、`BinaryFloatingPoint`、`Decimal`

{{% /tab %}}

{{% tab header="Go" %}}

Go 有 `float32` 与 `float64`（默认）两种 IEEE 754 浮点，还有 `complex64`/`complex128` 复数；`NaN` 只能用 `math.IsNaN` 判断。

**类型**：`float32`、`float64`（默认）。

```go
var a float64 = 1.5
b := 0.1
c := float32(1.5)
d := math.Inf(1)
e := math.NaN()
```

**常量**：`math.MaxFloat64`（1.797e308）、`math.SmallestNonzeroFloat64`（5e-324）、`math.MaxFloat32`（3.4e38）、`math.Inf(±1)`、`math.NaN()`。Go 没有 epsilon 常量，自己写 `math.Nextafter(1, 2) - 1`。

⚠️ **Go 最反直觉的一点：常量表达式与变量结果不同。**

```go
const x = 0.1 + 0.2
fmt.Println(x == 0.3)      // true  ← 无类型常量按任意精度计算

a, b := 0.1, 0.2
fmt.Println(a+b == 0.3)    // false ← 变量走 IEEE float64
```

代码演示 `math` 里的最值、`Round`/`RoundToEven`，以及"常量精确、变量不精确"这组关键对比。要点是：Go 的无类型常量按任意精度计算（所以 `const x = 0.1 + 0.2; x == 0.3` 为真），变量才走 IEEE（为假）；这和其他所有语言都不一样。

📘 [`math` 包](https://pkg.go.dev/math)、[Go spec · Constants](https://go.dev/ref/spec#Constants)

{{% /tab %}}

{{% tab header="Python" %}}

Python 只有一种内建浮点 `float`（C 的 double）；需要十进制精度用标准库 `decimal.Decimal`，需要精确分数用 `fractions.Fraction`。

**类型**：只有 `float`（C double）。需要十进制用 `decimal.Decimal`，需要精确分数用 `fractions.Fraction`。

```python
a = 1.5
b = 1e-3
c = float("inf"); d = float("nan")
e = float.fromhex("0x1.8p3")     # 12.0
from decimal import Decimal
f = Decimal("0.1")               # 十进制，钱用它
```

`sys.float_info` 给出全部边界：`.max`（1.797e308）、`.min`（2.225e-308）、`.epsilon`（2.22e-16）、`.mant_dig`（53）、`.max_exp`。

```python
0.1 + 0.2 == 0.3            # false
math.isclose(0.1 + 0.2, 0.3)        # true（默认 rel_tol=1e-9）
math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-16)   # false
round(2.5), round(3.5), round(-2.5)  # (2, 4, -2) ← 银行家舍入
int(3.9), math.floor(3.9), math.ceil(3.9)     # 3, 3, 4（floor/ceil 返回 int）
math.fsum([0.1] * 10)       # 1.0（精确求和，比 sum 稳）
```

代码给出 `sys.float_info`、`isclose`、`round` 与 `fsum` 的用法。要点是：`round()` 是银行家舍入（`round(2.5) == 2`），`int(float)` 向零截断，NaN 不能比较；

📘 [`decimal`](https://docs.python.org/3/library/decimal.html)、[`math`](https://docs.python.org/3/library/math.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的浮点是 JVM 的 `Float` 与 `Double`（默认）；比较语义取决于静态类型——静态是浮点时按 IEEE 754，装进 `Any`/集合后走 `equals`。

**类型**：`Float`、`Double`（默认）；`java.math.BigDecimal` 负责十进制。

```kotlin
val a = 1.5              // Double
val b: Float = 1.5f
val d = Double.NaN
val e = Double.POSITIVE_INFINITY
val f = 2.5.roundToInt() // 3（四舍五入、远离零）
val g = 0.1.toBigDecimal() + 0.2.toBigDecimal()   // 0.3（十进制精确）
```

常量：`Double.MAX_VALUE`、`Double.MIN_VALUE`（**最小正非零**，不是最负！）、`Double.EPSILON`（2.22e-16）、`Float.EPSILON`（1.19e-7）、`Double.NaN`、`Double.POSITIVE_INFINITY`。

⚠️ **Kotlin 独有的坑：比较结果取决于静态类型。**

```kotlin
Double.NaN == Double.NaN        // false（静态类型是浮点，走 IEEE 754）
0.0 == -0.0                     // true

fun generalizedEquals(a: Any, b: Any) = a == b
generalizedEquals(Double.NaN, Double.NaN)   // true（走 equals()）
generalizedEquals(0.0, -0.0)                // false
listOf(Double.NaN).contains(Double.NaN)     // true（集合里也是 equals 语义）
```

代码演示最值常量、`roundToInt`、`toBigDecimal`，并对比"静态浮点类型"与"`Any`"两种比较结果。金额用 `BigDecimal`。

📘 [Kotlin · Numbers / Floating-point number comparison](https://kotlinlang.org/docs/numbers.html#floating-point-number-comparison)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的浮点是 `float` 与 `double`（默认），十进制计算用 `BigDecimal`；Java 17 起所有浮点运算都是 strict（JEP 306），不再有 x87 扩展精度差异。

**类型**：`float`、`double`（默认）；`BigDecimal` 负责十进制。

```java
double a = 1.5;
float b = 1.5f;
double c = Double.NaN;
double d = Double.POSITIVE_INFINITY;
BigDecimal m = new BigDecimal("0.1");     // ✅ 用字符串构造
```

常量：`Double.MAX_VALUE`、`Double.MIN_VALUE`（最小正非零）、`Double.MIN_NORMAL`（最小正规数）、`Double.NaN`、`Double.POSITIVE_INFINITY`；机器 epsilon 是 `Math.ulp(1.0)`，Java **没有** `EPSILON` 常量。

```java
System.out.println(0.1 + 0.2 == 0.3);   // false
System.out.println(Double.NaN == Double.NaN);   // false
System.out.println(Double.compare(Double.NaN, 1.0));  // 1（NaN 最大）
System.out.println(Double.compare(-0.0, 0.0));        // -1（-0.0 更小）
System.out.println(Double.valueOf(Double.NaN).equals(Double.NaN)); // true（equals 把 NaN 当相等）
```

代码给出 `Double.compare`/`Double.equals`/`==` 三种比较的差异，以及 `Math.round(-2.5)` 的结果。要点是：`==` 遵循 IEEE、`compare` 提供全序、`equals` 把 NaN 当相等；`Math.round` 是"半值向 +∞"，要银行家舍入用 `Math.rint`，Java 17 起浮点运算一律 strict。

转换：`(int) 3.9 == 3`、`(int) Double.NaN == 0`、`(int) 1e300 == Integer.MAX_VALUE`（JLS 明确定义的饱和，不是 UB）；要检查用 `Math.toIntExact` 或先判范围。

⚠️ 金额不要用 `double`，也不要用 `new BigDecimal(0.1)`（那是二进制误差的十进制展开），要用 `new BigDecimal("0.1")` 并指定 `RoundingMode`。

📘 JLS §5.1.3（窄化转换）、`java.lang.Math`、`java.math.BigDecimal`

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有 `float`、`double`、`long double` 三种浮点，C++23 的 `<stdfloat>` 又定义了 `std::float16_t`~`std::float128_t` 与 `std::bfloat16_t`（该头文件的支持是可选的）。

**类型**：`float`、`double`、`long double`；C++23 `<stdfloat>` 的 `std::float16_t`、`std::float32_t`、`std::float64_t`、`std::float128_t`、`std::bfloat16_t`（实现可选支持）。

```cpp
float f = 1.5f;
double d = 1.5;
long double ld = 1.5L;
auto h = 1.5f16;      // C++23 <stdfloat>（有则支持）
```

```cpp
std::numeric_limits<double>::max();        // 1.7976931348623157e+308
std::numeric_limits<double>::min();        // 2.2250738585072014e-308（最小正规正数）
std::numeric_limits<double>::lowest();     // -1.7976931348623157e+308（最负）
std::numeric_limits<double>::epsilon();    // 2.220446049250313e-16
std::numeric_limits<double>::denorm_min(); // 4.9406564584124654e-324
std::numeric_limits<double>::infinity();
std::numeric_limits<double>::quiet_NaN();
```

代码展示 `numeric_limits` 的 `min`/`lowest`/`epsilon`/`denorm_min` 与 `std::bit_cast`。要点是：`min()` 是"最小正规正数"而不是最负值（要最负用 `lowest()`）；NaN 参与比较要显式处理（`std::strong_order` 可给全序）；`-ffast-math` 会让这些保证失效。

**计算**：`0.1 + 0.2 == 0.3` 为 false；`std::isnan` / `isinf` / `isfinite` / `signbit` / `copysign` / `fpclassify`；`std::nextafter`（相邻可表示值）、`std::fma`（融合乘加）、`std::lerp` 与 `std::midpoint`（C++20）、`std::bit_cast<std::uint64_t>(d)`（C++20 看位模式）。排序要把 NaN 也排进去，用 `std::strong_order`（C++20）而不是 `<`。

⚠️ `-ffast-math` 允许编译器假设"没有 NaN/Inf、加法可结合"，会静默破坏 `isnan`、`x != x` 这些判断；`long double` 在 x86 上是 80 位、在 ARM 上常是 128 位、在 MSVC 上就等于 `double`——**别用它做序列化格式**。

📘 cppreference：[`std::numeric_limits`](https://en.cppreference.com/w/cpp/types/numeric_limits)、[`<stdfloat>`](https://en.cppreference.com/w/cpp/header/stdfloat)

{{% /tab %}}

{{% tab header="C" %}}

C 有 `float`、`double`、`long double` 三种浮点（边界值在 `<float.h>`），C23 增加了可选的 `_Float16`/`_Float32`/`_Float64`/`_Float128` 类型。

**类型**：`float`、`double`、`long double`；C23 新增可选的 `_Float16`/`_Float32`/`_Float64`/`_Float128`（本机 Apple clang 只支持 `_Float16`）。

```c
float f = 1.5f;
double d = 1.5;
long double ld = 1.5L;
_Float16 h = 1.5;      // C23 可选类型
```

`<float.h>` 里的边界：

```c
FLT_MAX          // 3.4028235e38
FLT_MIN          // 1.1754944e-38（最小正规正数）
FLT_EPSILON      // 1.1920929e-7
FLT_TRUE_MIN     // 1.4e-45（C11：含非正规数的最小正值）
DBL_MAX          // 1.7976931348623157e308
DBL_MIN          // 2.2250738585072014e-308
DBL_EPSILON      // 2.220446049250313e-16
FLT_MANT_DIG     // 24；DBL_MANT_DIG 是 53
```

```c
printf("%.17g\n", 0.1);      // 0.10000000000000001
printf("%a\n", 0.1);         // 0x1.999999999999ap-4（十六进制，精确）
printf("%d %d\n", 0.1 + 0.2 == 0.3, NAN == NAN);   // 0 0
printf("%d\n", -0.0 == 0.0); // 1（相等，但 signbit(-0.0) 为真）
```

代码给出 `<float.h>` 的边界、`%.17g`/`%a` 打印与 `signbit` 的用法。要点是：默认 `%f` 只显示 6 位小数，比较与调试都用 `%.17g`；`float` 参与运算会被提升为 `double`；`-0.0 == 0.0` 成立，但 `signbit` 能把两者区分开。

⚠️ 默认 `%.f`/`%f` 只打印 6 位小数，**看起来相等不代表真的相等**；比较和调试都用 `%.17g`，存二进制用 `%a`。

📘 C 标准 §5.2.4.2.2（浮点特性）、[`<float.h>`](https://en.cppreference.com/w/c/types/limits)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的浮点是 `Float16`、`Float32`、`Float64`（默认）以及任意精度的 `BigFloat`（基于 MPFR）；`Int(3.9)` 会抛 `InexactError`，必须显式选择取整方式。

**类型**：`Float16`、`Float32`、`Float64`（默认）、`BigFloat`（MPFR，任意精度十进制可调）；另有 `Rational` 精确分数。

```julia
a = 1.5                 # Float64
b = Float32(1.5)
c = Float16(1.5)
d = big"0.1"            # BigFloat
e = 1//3                # Rational{Int64}

floatmax(Float64)       # 1.7976931348623157e308
floatmin(Float64)       # 2.2250738585072014e-308
eps(Float64)            # 2.220446049250313e-16
eps(Float32)            # 1.1920929f-7
Inf, -Inf, NaN, -0.0
```

```julia
0.1 + 0.2 == 0.3            # false
isapprox(0.1 + 0.2, 0.3)    # true（≈ 默认 rtol = √eps）
NaN == NaN                  # false
isequal(NaN, NaN)           # true
round(2.5)                  # 2.0（银行家/IEEE）
round(Int, 2.5)             # 2
```

代码演示 `floatmax`/`eps`、`isapprox` 以及"整数转浮点必须显式"这一点。要点是：`Int(3.9)` 会抛 `InexactError`（Julia 拒绝静默截断），近似比较用 `isapprox`/`≈`，需要更高精度还有 `BigFloat` 与 `Rational`。

其他实用项：`nextfloat`/`prevfloat` 取相邻值、`setprecision(256)` 调 `BigFloat` 位数、`Rational` 运算全程精确（`1//3 + 1//6 == 1//2`）、`sum` 对浮点用成对求和更稳。

📘 [Julia · Integers and Floating-Point Numbers](https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/)、[`Base.eps`](https://docs.julialang.org/en/v1/base/math/#Base.eps)

{{% /tab %}}

{{% tab header="C#" %}}

C# 有 `Half`（.NET 5+）、`float`、`double`（默认）与十进制的 `decimal`（128 位、28~29 位有效数字）；注意 `double.Epsilon` 是最小非零非正规数，不是机器 epsilon。

**类型**：`Half`（.NET 5+）、`float`(Single)、`double`（默认）、`decimal`（base-10，128 位）。

```csharp
double d = 1.5;
float f = 1.5f;
Half h = (Half)1.5;
decimal m = 0.1m;            // 十进制字面量
decimal n = 0.1m + 0.2m;     // 0.3，精确
```

```csharp
double.MaxValue          // 1.7976931348623157E+308
double.MinValue          // -1.7976931348623157E+308（最负）
double.Epsilon           // 4.9406564584124654E-324 ← 最小非零非正规数，不是机器 epsilon！
double.NaN / double.PositiveInfinity / double.NegativeInfinity
Math.BitIncrement(1.0) - 1.0    // 才是机器 epsilon ≈ 2.22e-16
```

⚠️ `double.Epsilon` 的名字是历史包袱，绝大多数人以为它是"比较容差"，实际上它小到没有实用意义。要容差就自己定义 `1e-9`，或用 `Math.BitIncrement`/`Math.BitDecrement`。

```csharp
0.1 + 0.2 == 0.3                       // false
double.NaN == double.NaN               // false（运算符遵循 IEEE）
double.NaN.Equals(double.NaN)          // true（Equals 把 NaN 当相等）
Math.Round(2.5)                        // 2（默认银行家舍入）
Math.Round(2.5, MidpointRounding.AwayFromZero)   // 3
(int)3.9                               // 3
Convert.ToInt32(double.NaN)            // 🛑 OverflowException
```

代码演示 `double`/`float`/`Half`/`decimal` 与 `Math.Round` 的两种模式。要点是：默认 `Math.Round` 是银行家舍入、`double.Epsilon` 不是机器 epsilon（要 `Math.BitIncrement(1.0) - 1.0`）；金额一律用 `decimal`，`Convert.ToInt32(NaN)` 会抛异常。

📘 [`double`](https://learn.microsoft.com/dotnet/api/system.double)、[`decimal`](https://learn.microsoft.com/dotnet/api/system.decimal)、[`MidpointRounding`](https://learn.microsoft.com/dotnet/api/system.midpointrounding)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 只有 `double`（IEEE 754 双精度）一种浮点类型；需要单精度时用 `Float32List`/`Float32x4` 这类定宽缓冲区，`double` 没有 epsilon 常量。

**类型**：只有 `double`（IEEE 754 双精度）；单精度要用 `Float32List`，位级操作可以用 `ByteData`。

```dart
var a = 1.5;
var b = double.nan;
var c = double.infinity;
var d = double.negativeInfinity;
var e = double.parse("1.5");
var f = 1 / 3;                 // 0.3333333333333333
var g = Float32List.fromList([0.1])[0];   // 0.10000000149011612
```

常量：`double.nan`、`double.infinity`、`double.negativeInfinity`、`double.maxFinite`（1.7976931348623157e308）、`double.minPositive`（5e-324）。**没有 epsilon 常量**，机器 epsilon 要自己写 `2.220446049250313e-16`。

```dart
0.1 + 0.2 == 0.3      // false
double.nan == double.nan   // false
double.nan.isNaN      // true
(-0.0) == 0.0         // true
2.5.round()           // 3（远离零）
-2.5.round()          // -3
3.9.truncate()        // 3
(1.0 / 0).isInfinite  // true
double.nan.toInt()    // 🛑 UnsupportedError
```

代码给出 `double.nan`/`maxFinite`/`minPositive` 与 `Float32List` 的单精度舍入。要点是：Dart 只有 `double`，没有 epsilon 常量；`toInt()` 遇 NaN/Inf 抛错，`round()` 远离零；编译到 Web 后就是 JS number。

📘 [`double` 类](https://api.dart.dev/stable/latest/dart-core/double-class.html)

{{% /tab %}}

{{% tab header="R" %}}

R 只有一种浮点类型 `double`（双精度），没有 `float`；单精度可用 `float` 包，任意精度用 `Rmpfr`，整数用 `bit64`。

**类型**：只有 `double`（`float` 在 R 里不存在）。`Rmpfr` 提供任意精度，`gmp` 提供大整数与有理数。

```r
a <- 1.5
b <- 1.5e-3
c <- Inf; d <- -Inf; e <- NaN; f <- NA_real_
is.double(a)      # TRUE
```

```r
.Machine$double.xmax    # 1.797693e+308
.Machine$double.xmin    # 2.225074e-308
.Machine$double.eps     # 2.220446e-16
.Machine$double.digits  # 53
```

⚠️ **R 里 `NA` 和 `NaN` 是两种值**：`is.na(NaN)` 为 `TRUE`，但 `is.nan(NA_real_)` 为 `FALSE`；`NA` 表示"缺失"，`NaN` 表示"算不出来"，`NA` 参与任何比较都得 `NA`。

```r
0.1 + 0.2 == 0.3     # FALSE
round(2.5)           # 2    ← IEC 60559 银行家舍入
round(-2.5)          # -2
1/0                  # Inf
0/0                  # NaN
Inf - Inf            # NaN
sqrt(-1)             # NaN + 警告
all.equal(1, 1 + 1e-9)   # TRUE：默认 tolerance ≈ 1.5e-8
```

代码演示 `.Machine$double.*`、`round(2.5)` 的结果与 `all.equal` 的默认容差。要点是：R 只有 double、`round` 是银行家舍入、`all.equal` 自带容差；R 打印默认只有 7 位有效数字，想看真相用 `sprintf("%.17g", x)`。

📘 [`?Machine`](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Machine.html)、[`?round`](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Round.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 有 `f16`、`f32`、`f64`、`f80`、`f128` 与 `c_longdouble`；字面量类型是 `comptime_float`（精度至少等同 f128），且没有 NaN/Inf 字面量，要用 `std.math`。

**类型**：`f16`、`f32`、`f64`、`f80`、`f128`、`c_longdouble`；字面量类型是 `comptime_float`，保证有 `f128` 的精度与运算。

```zig
const a: f64 = 1.5;
const b: f32 = 1.5;
const c: f80 = 1.5;
const d = 1.5;                    // comptime_float
const inf = std.math.inf(f32);
const nan = std.math.nan(f64);
const eps = std.math.floatEps(f64);     // 2.220446049250313e-16
const max = std.math.floatMax(f32);     // 3.4028235e38
```

Zig **没有 NaN/Inf 字面量**，必须走 `std.math`；十六进制浮点写作 `0x103.70p-5`。

```zig
0.1 + 0.2 == 0.3            // false（运行时 f64）
std.math.isNan(nan)         // true
@intFromFloat(3.9)          // 3（截断）
@intFromFloat(nan)          // 🛑 安全模式 panic（ReleaseFast 下是 UB）
```

代码展示 `std.math.inf/nan/floatEps` 与"没有 NaN 字面量"这一点。要点是：Zig 的浮点默认 `.strict` 模式（不重排、保留 NaN 语义），`@intFromFloat` 在安全模式下对 NaN/越界会 panic，字面量类型 `comptime_float` 至少有 f128 精度。

⚠️ `comptime_float` 是编译期高精度（≥f128），所以 `const x = 0.1 + 0.2;` 与运行时 `var y: f64 = 0.1; y += 0.2;` 的结果可能不同——这跟 Go 的常量/变量差异是同一类现象。

📘 [Zig Language Reference · Floats](https://ziglang.org/documentation/master/#Floats)、[`std.math`](https://ziglang.org/documentation/master/std/#std.math)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的浮点就是双精度 `float`，与 `integer` 同属 `number`；`/` 永远返回浮点，`//` 才是地板除，负数取模与 C 的 `fmod` 结果不同。

**类型**：只有一种浮点——`float`（双精度）；Lua 5.3 起与 `integer` 共用 `number` 类型，用 `math.type()` 区分。

```lua
local a = 1.5
local b = 1e-3
local c = 0x1p4            -- 16.0（十六进制浮点）
local d = math.huge        -- inf
local e = -math.huge
local f = 0/0              -- nan
print(math.type(a), math.type(2))   -- float  integer
```

常量与函数：`math.huge`、`math.pi`、`math.maxinteger`、`math.mininteger`；没有 epsilon 常量。`math.fmod(x, y)` 用 C 语义（余数符号跟被除数），而 `x % y` 是地板语义（符号跟除数）——两者在负数上结果不同。

```lua
print(0.1 + 0.2 == 0.3)              -- false
print(math.nan ~= math.nan)          -- true（NaN 不等于自己）
print(-0.0 == 0.0)                   -- true
print(string.format("%.17g", 0.1+0.2))   -- 0.30000000000000004
print(string.format("%d", 3.0))      -- 3（整值浮点可以按 %d 打印）
print(math.tointeger(3.5))           -- nil（不是截断，是不转换）
print(math.floor(2.7), math.ceil(2.1))    -- 2 3（5.3+ 返回 integer）
print(math.fmod(-7, 2), -7 % 2)      -- -1 1
```

代码演示 `math.huge`、`%.17g` 打印，以及 `math.fmod` 与 `%` 在负数上的差别。要点是：Lua 只有双精度，整数与浮点的比较是精确的；`%` 是地板语义（符号跟除数），`math.fmod` 是 C 语义（符号跟被除数）。

📘 [Lua 5.4 · Arithmetic Operators](https://www.lua.org/manual/5.5/manual.html#3.4.1)、[`math` 库](https://www.lua.org/manual/5.5/manual.html#6.7)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 只有 `number`（双精度）这一种浮点；单精度用 `Float32Array` 或 `Math.fround`，十进制与货币用 decimal.js 之类的库。

**类型**：只有 `number`（IEEE 754 双精度）和 `bigint`；十进制要靠库（decimal.js、big.js），单精度靠 `Float32Array`。

```ts
const a = 1.5;                    // number
const b = 0.1 + 0.2;              // 0.30000000000000004
const c = Number.EPSILON;         // 2.220446049250313e-16
const d = Number.MAX_VALUE;       // 1.7976931348623157e+308
const e = Number.MIN_VALUE;       // 5e-324（最小正非零，不是最负）
const f = Number.NaN;
const g = new Float32Array([0.1])[0];   // 0.10000000149011612
```

```ts
Number.isNaN(NaN);          // true
Number.isFinite(Infinity);  // false
Number.isSafeInteger(2 ** 53);  // false
Math.round(2.5);            // 3
Math.round(-2.5);           // -2   ← 半值一律向 +∞ 取
Math.round(-0.5);           // -0
Object.is(Math.round(-0.5), 0);   // false（因为它是 -0）
Math.trunc(3.9);            // 3
Math.fround(0.1);           // 0.10000000149011612（转 float32）
(1.005).toFixed(2);         // "1.00" ← 经典陷阱
```

代码展示 `Number.*` 常量、`Math.round(-0.5)` 得到 `-0` 以及 `toFixed` 的经典陷阱。要点是：`(1.005).toFixed(2)` 得到 `"1.00"`，因为 1.005 的二进制表示不精确；金额用整数分/`bigint`/decimal 库，判 NaN 一律用 `Number.isNaN`。

📘 [MDN · Number](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number)、[TS Handbook · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `number` 就是双精度浮点，`Math.fround` 能做单精度舍入；`NaN`/`Infinity` 是合法值，但 `JSON.stringify` 会把它们变成 `null`。

**类型**：只有 `number`；`Float32Array` / `Float64Array` / `DataView` 用于二进制；十进制用库。

```js
0.1 + 0.2 === 0.3            // false
(0.1 + 0.2).toFixed(17)      // "0.30000000000000004"
Number.EPSILON               // 2.220446049250313e-16
Number.MIN_VALUE             // 5e-324
Number.isNaN(NaN)            // true
Number.isNaN("abc")          // false
isNaN("abc")                 // true ← 全局 isNaN 会强制转换，别用
Number.isFinite(1 / 0)       // false
Math.round(-2.5)             // -2
Math.round(-0.5)             // -0
Math.fround(0.1)             // 0.10000000149011612
JSON.stringify(NaN)          // "null"  ← 陷阱
JSON.stringify(Infinity)     // "null"  ← 陷阱
JSON.stringify(-0)           // "0"
99.99 * 100                  // 9998.999999999998
```

代码给出 `Number.isNaN` 与全局 `isNaN` 的区别，以及 `JSON.stringify` 对 NaN/Infinity 的处理。要点是：全局 `isNaN` 会做类型转换（`isNaN("abc")` 为真），判 NaN 必须用 `Number.isNaN`；

`-0` 只在 `Object.is`、`1/x`（`-Infinity`）和 `JSON.stringify` 之外几乎不可见，但排序、除法、`Intl` 格式化时可能出现；判 NaN 一律用 `Number.isNaN`。

📘 [MDN · Number](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number)、[MDN · Math](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Math)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 只有双精度 `float`，常量在 `PHP_FLOAT_*`；`round()` 默认是 half away from zero（不是 IEEE 银行家舍入），十进制/任意精度要装 `bcmath` 或 `gmp`。

**类型**：只有 `float`（双精度）；`bcmath` / `gmp` 扩展给十进制与任意精度。

```php
$a = 1.5;
$b = 1e-3;
$c = NAN; $d = INF; $e = -INF;

var_dump(PHP_FLOAT_EPSILON);   // float(2.220446049250313E-16)
var_dump(PHP_FLOAT_MAX);       // float(1.7976931348623157E+308)
var_dump(PHP_FLOAT_MIN);       // float(2.2250738585072014E-308)
var_dump(PHP_FLOAT_DIG);       // int(15)：能往返的十进制位数
```

```php
0.1 + 0.2 == 0.3;            // false
is_nan(NAN);                 // true
is_finite(INF);              // false
round(2.5);                  // 3.0 ← PHP 默认是 half away from zero
round(2.5, 0, PHP_ROUND_HALF_EVEN);   // 2.0 ← 显式要银行家舍入
number_format(1234.5678, 2); // "1,234.57"（千分位、字符串）
sprintf("%.17g", 0.1 + 0.2); // 0.30000000000000004
(int) 3.9;                   // 3（向零截断）
(int) NAN;                   // 结果无可移植保证
fmod(-7, 2);                 // -1：C 语义
-7 % 2;                      // -1：% 只对整数，操作数会先转 int
```

代码展示 `PHP_FLOAT_*` 常量、`round` 的默认模式与 `fmod`。

📘 [PHP Manual · Floating point numbers](https://www.php.net/manual/en/language.types.float.php)、[`round`](https://www.php.net/manual/en/function.round.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的 `Float` 是双精度（含 `Float::INFINITY`/`Float::NAN`）；十进制用标准库 `BigDecimal`，精确分数用 `Rational`。

**类型**：`Float`（双精度）；精确十进制用 `BigDecimal`，精确分数用 `Rational`。

```ruby
a = 1.5
b = 1.5e-3
c = Float::INFINITY
d = -Float::INFINITY
e = Float::NAN
f = Rational(1, 3)          # 1/3，精确
g = BigDecimal("0.1")       # 十进制

Float::MAX       # 1.7976931348623157e+308
Float::MIN       # 2.2250738585072014e-308（最小正规正数）
Float::EPSILON   # 2.220446049250313e-16
Float::DIG       # 15
Float::MANT_DIG  # 53
Float::RADIX     # 2
```

```ruby
0.1 + 0.2 == 0.3        # false
Float::NAN == Float::NAN    # false
(1.0/0).infinite?       # 1（正 1、负 -1、有限 nil）
Float::NAN.nan?         # true
2.5.round               # 3（远离零）
-2.5.round              # -3
2.5.round(half: :even)  # 2（银行家，可选）
3.9.to_i                # 3
Float("1.5")            # 1.5（严格解析，失败抛异常）
"abc".to_f              # 0.0（宽松解析，别用在用户输入上）
"%.17g" % (0.1 + 0.2)   # 0.30000000000000004
```

代码给出 `Float::*` 常量、`infinite?`/`nan?` 与三种取整方式。要点是：`0.0 == -0.0` 且 `eql?` 也为真（Hash 键相同），`Float("1.5")` 严格而 `"1.5".to_f` 宽松，金额用 `BigDecimal` 或整数分。

📘 [Ruby · Float](https://docs.ruby-lang.org/en/master/Float.html)、[`BigDecimal`](https://docs.ruby-lang.org/en/master/BigDecimal.html)

{{% /tab %}}

{{< /tabpane >}}

---

## 布尔、字符与字符串

这一节回答三个问题：**什么值算"假"**、**字符到底是不是一种类型**、**字符串的"长度"数的是什么**。最后一条是跨语言搬代码时最容易出事的地方——字节、码点、字素簇是三套不同的计数方式，同一个 `"👍🏽"` 在不同语言里的 `length` 可以是 2、4 或 1。

**一页速览**

| 语言 | 布尔与真值 | 字符类型 | 字符串（编码 / 可变性） | 字节串 |
| --- | --- | --- | --- | --- |
| Rust | `bool`，无真值转换 | `char`=4 字节 Unicode 标量 | `String` / `&str`，UTF-8，不可变（`String` 可增长） | `Vec<u8>` / `&[u8]` |
| Swift | `Bool`，无真值转换 | `Character`=扩展字素簇 | `String`，UTF-8 存储，值语义 | `Data` / `[UInt8]` |
| Go | `bool`，`if` 只收 bool | `byte`(=`uint8`)、`rune`(=`int32`) | `string`，UTF-8 约定，不可变 | `[]byte` |
| Python | `bool` 是 `int` 子类，有一整套真值规则 | 无（长度 1 的 `str`） | `str`，Unicode，不可变 | `bytes` / `bytearray` |
| Kotlin | `Boolean`，无真值转换 | `Char`=UTF-16 码元 | `String`，UTF-16，不可变 | `ByteArray` |
| Java | `boolean`，无真值转换 | `char`=UTF-16 码元，还是数字 | `String`，UTF-16，不可变 | `byte[]`（有符号！） |
| C++ | `bool`，有隐式数值转换 | `char` `char8_t` `char16_t` `char32_t` `wchar_t` | `std::string`（字节，可变）、`std::u8string` | `std::vector<std::byte>` |
| C | `bool`（C23 关键字），非 0 即真 | `char`（1 字节，符号性由实现定） | **没有字符串类型**：`char[]` + `\0` | `unsigned char[]` |
| Julia | `Bool`，`if` 只收 Bool | `Char`=32 位码点 | `String`，UTF-8，不可变，**按字节索引** | `Vector{UInt8}` |
| C# | `bool`，无真值转换 | `char`=UTF-16 码元 | `string`，UTF-16，不可变、按值相等 | `byte[]` / `ReadOnlySpan<byte>` |
| Dart | `bool`，无真值转换 | 无（长度 1 的 `String`） | `String`，UTF-16 码元，不可变 | `Uint8List` + `utf8` |
| R | `logical`（含 `NA`），`if` 只收长度 1 的 logical | 无（长度 1 的 `character`） | `character` 向量 | `raw` |
| Zig | `bool`，无真值转换 | 无（`u8` 或码点整数） | `[]const u8`，UTF-8 约定，无字符串类型 | `[]u8` / `std.ArrayList(u8)` |
| Lua | `boolean`，只有 `false`/`nil` 为假 | 无（长度 1 的 string） | `string`，**字节序列**，不可变 | 同上（string 就是字节串） |
| TypeScript | `boolean`，有 JS 真值规则 | 无 | `string`，UTF-16，不可变 | `Uint8Array` + `TextEncoder` |
| JavaScript | 同上 | 无 | 同上 | 同上 + `Buffer`（Node） |
| PHP | `bool`，falsy 规则里有 `"0"`，而 `NAN` 是真 | 无（**单字节**字符串） | `string`，字节序列，写时复制 | `string` 本身就是字节串 |
| Ruby | 只有 `false` 和 `nil` 为假 | 无（长度 1 的 String） | `String`，**可变**，每个字符串自带 encoding | `String#b` / `Array#pack` |

**逐语言详解**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

**布尔**：`bool`，1 字节，只有 `true`/`false`，没有真值转换——`if 1 {}` 编译不过。

**字符**：`char`，4 字节，一个 Unicode 标量值（不含代理对）：`'A'`、`'中'`、`'😀'`、`'\u{1F600}'`，是独立类型而不是整数。

**字符串**：`String`（拥有、可增长）与 `&str`（借用切片），内容一律 UTF-8。

```rust
let s = "héllo";                  // &str
let mut t = String::from(s);      // String
t.push_str("!");

s.len()                           // 6：字节数（é 占 2 字节）
s.chars().count()                 // 5：码点数
// &s[1..2]                       // 🛑 panic：不是字符边界
&s[0..2]                          // "hé"：按字节切
s.to_uppercase()                  // "HÉLLO"
s.contains('é')                   // true
let bytes: &[u8] = s.as_bytes();  // 字节视图，零成本
```

代码演示 `String`/`&str` 的拼接、`len()`（字节）与 `chars().count()`（码点）的差别，以及按字节切片可能 panic。要点是：Rust 的 `char` 是 4 字节的 Unicode 标量值，字符串一律 UTF-8，切片下标必须落在字符边界上；字节视图用 `as_bytes()`。

⚠️ `len()` 是字节、`chars().count()` 是码点，两者都不是"人眼字符"（`"👍🏽"` 是 4 个码点、1 个字素簇）。Rust 的 `char` 也不是字素簇，要按字素簇切分用 `unicode-segmentation` 这类库。

{{% /tab %}}

{{% tab header="Swift" %}}

**布尔**：`Bool`，只有 `true`/`false`，没有真值转换。

**字符**：`Character` 是一个**扩展字素簇**——`"é"`、`"👍🏽"`、`"🇨🇳"` 都是单个 `Character`。

**字符串**：`String`，值语义（赋值即复制语义），UTF-8 存储，Unicode 正确是它的卖点。

```swift
let flag = "🇨🇳"
flag.count                  // 1：字素簇
flag.unicodeScalars.count   // 2：码点
flag.utf8.count             // 8：字节

var s = "héllo"
s += "!"
s.append("?")
let i = s.index(s.startIndex, offsetBy: 1)
s[i]                        // "é"

let n = "42"
Int(n)                      // Optional(42)
String(42)                  // "42"
```

代码用同一个 `"🇨🇳"` 演示了三种"长度"：`count`（字素簇）为 1、`unicodeScalars.count`（码点）为 2、`utf8.count`（字节）为 8。要点是：`Character` 是扩展字素簇，`String.Index` 不能和整数互换，所以 `s[1]` 根本编译不过。

⚠️ `String.Index` 不能和整数互换，`s[1]` 编译不过——Swift 逼你面对"字符不是定长单元"。`"é"` 的 `count` 是 1、`utf8.count` 是 2，两个数都对，取决于你问的是什么。

{{% /tab %}}

{{% tab header="Go" %}}

**布尔**：`bool`，只有 `true`/`false`；`if 1 == 1` 可以，`if 1` 编译不过。

**字符串**：`string` 是只读的字节序列，UTF-8 是约定而非强制。

```go
s := "héllo"
len(s)                        // 6：字节数
utf8.RuneCountInString(s)     // 5：码点数
s[0]                          // 104：是 byte，不是字符
for i, r := range s {         // i 是字节下标，r 是 rune
    _, _ = i, r
}
[]rune(s)                     // 码点切片
strings.ToUpper(s)            // Unicode 感知的大写
strings.Contains(s, "é")
```

代码演示 `len(s)`（字节）与 `utf8.RuneCountInString`（码点）的差别，以及 `range` 遍历字符串时拿到的是 rune 而不是字节。要点是：`string` 是只读字节序列，`s[0]` 是 `byte`，拼接大量字符串要用 `strings.Builder`。

**字节串**：`[]byte`；`[]byte(s)` 与 `string(b)` 都会**复制**内容。

⚠️ `s[0]` 是字节不是字符，`len(s)` 也不是字符数；要把字符串当字符序列处理，先 `[]rune(s)` 或走 `unicode/utf8`。

{{% /tab %}}

{{% tab header="Python" %}}

**布尔**：`bool` 是 `int` 的子类，`True == 1`；假值有 `None`、`False`、`0`、`0.0`、`""`、`[]`、`{}`、`()`、`set()`，对象可以用 `__bool__`/`__len__` 自定义。

**字符串**：`str` 是不可变的 Unicode 码点序列；CPython 内部按内容选最紧凑编码（latin-1 / UCS-2 / UCS-4）。

```python
s = "héllo"
len(s)                  # 5：码点数（不是字节）
s[1]                    # 'é'
s.encode("utf-8")       # b'h\xc3\xa9llo'：6 字节
len(s.encode("utf-8"))  # 6

b = b"h\xc3\xa9llo"
b.decode("utf-8")       # 'héllo'
bytearray(b)            # 可变版本
memoryview(b)           # 零拷贝视图

f"{s!r} 的长度是 {len(s)}"      # f-string
rf"C:\path\{s}"                # raw + f 组合
",".join(["a", "b"])           # 拼接首选 join
```

代码演示 `len(s)`（码点）、`encode`/`decode`、`bytearray`/`memoryview` 与 f-string。要点是：`str` 与 `bytes` 不能隐式互转，`len` 数的是码点而不是字素簇（`"👍🏽"` 是 2），拼接用 `join` 而不是循环 `+=`。

{{% /tab %}}

{{% tab header="Kotlin" %}}

**布尔**：`Boolean`，没有真值转换。

**字符**：`Char`，16 位 UTF-16 码元，单引号：`'A'`、`'中'`；辅助平面字符（`'😀'`）无法用一个 `Char` 表示。

**字符串**：`String` 不可变，JVM 上内部是 UTF-16。

```kotlin
val s = "héllo"
s.length                     // 5：UTF-16 码元数
s.codePoints().count()       // 5：码点数
s.toByteArray()              // ByteArray（默认 UTF-8）
s.uppercase()                // Locale 无关的大写
s[1]                         // 'é'

val name = "World"
println("Hello, $name! ${name.length}")   // 字符串模板
val raw = """C:\path\file"""               // 原始字符串
```

代码演示 `length`（UTF-16 码元）、`codePoints().count()`（码点）与 `toByteArray` 的转码。要点是：emoji 的 `length` 是 2；大小写转换用 Locale 无关的 `uppercase()`；跨进程传输要显式指定 `Charsets.UTF_8`。

{{% /tab %}}

{{% tab header="Java" %}}

**布尔**：`boolean`，没有真值转换（`if (1)` 编译不过）。

**字符**：`char` 是 16 位 UTF-16 码元，**并且是数值类型**：`'A' + 1 == 66`。

**字符串**：`String` 不可变，UTF-16；`StringBuilder` 用于可变拼接。

```java
String s = "héllo";
s.length();                       // 5：UTF-16 码元数
s.codePointCount(0, s.length());  // 5：码点数
s.charAt(1);                      // 'é'
s.getBytes(StandardCharsets.UTF_8);
new String(bytes, StandardCharsets.UTF_8);

String t = """
        多行文本块（Java 15+）
        """;
String joined = String.join(",", "a", "b");
```

代码演示 `length()`/`codePointCount`/`getBytes` 与文本块。要点是：`char` 是 UTF-16 码元，所以 `"😀".length()` 是 2；`byte` 有符号（协议处理要 `b & 0xFF`）；字符串比较永远用 `equals` 而不是 `==`。

⚠️ `"😀".length()` 是 2，`charAt()` 会给你半个代理对，按码点遍历用 `codePoints()`；做二进制协议时 `byte` 要 `b & 0xFF`；

{{% /tab %}}

{{% tab header="C++" %}}

**布尔**：`bool`，有隐式数值转换（`int` → `bool` 是 `!= 0`），这点和 Swift/Kotlin/Java 不同。

**字符**：`char`（1 字节，符号性由实现定）、`signed char`、`unsigned char`、`wchar_t`、`char16_t`、`char32_t`，C++20 起还有 `char8_t`。

**字符串**：`std::string` 是**可变**的字节容器（不保证 UTF-8）；`std::string_view`（C++17）是非拥有视图。

```cpp
#include <string>
#include <string_view>

std::string s = "héllo";
s.size();                     // 6：字节数
s += "!";                     // 可变，原地追加
std::string_view v = s;       // 不拷贝，注意生命周期

std::u8string u8 = u8"中文";   // char8_t（C++20）
std::u16string u16 = u"中文";
std::string hex = std::format("{:x}", 255);   // C++20
```

代码演示 `std::string` 的字节语义、`string_view` 的非拥有视图与 C++20 的 `u8string`。要点是：`size()` 是字节数、字符串没有编码概念，`c_str()` 在含 `\0` 的二进制数据上会截断，Unicode 处理要靠 ICU 之类的库。

⚠️ `size()` 是字节且没有编码概念，`std::toupper` 也不认 Unicode；C 风格接口 `c_str()` 在含 `\0` 的二进制数据上会截断。要 Unicode 处理就用 ICU 或第三方库。

{{% /tab %}}

{{% tab header="C" %}}

**布尔**：C99 `<stdbool.h>` 提供 `bool`/`true`/`false`；C23 起它们是关键字。真值规则是"非 0 即真"。

**字符**：`char` 是 1 字节，符号性由实现决定（要明确就用 `signed char`/`unsigned char`）；`'A'` 的类型是 `int`。

**字符串**：**没有字符串类型**，只有"以 `\0` 结尾的 `char` 数组"这一约定。

```c
#include <string.h>
#include <stdio.h>

char s[] = "héllo";      // 6 个可见字节 + 1 个 \0
sizeof(s);                // 7
strlen(s);                // 6：字节数，O(n)
strcmp(s, "héllo");       // 0

char buf[16];
snprintf(buf, sizeof buf, "%s-%d", s, 42);   // 唯一安全的拼接方式
```

代码演示 `char[]` + `strlen`/`strcmp` 与 `snprintf` 的拼接写法。要点是：C 没有字符串类型，`strlen` 是 O(n) 且遇到 `\0` 就停；`strcpy`/`sprintf` 是缓冲区溢出的主要来源，一律改用 `snprintf` 并检查返回值。

`wchar_t` 宽度跨平台不同（Windows 16 位、Linux 32 位），要用宽字符就选 C11 的 `char16_t`/`char32_t`/`u16"..."`/`u32"..."`；C23 补上了 `char8_t` 与 `u8"..."`。

{{% /tab %}}

{{% tab header="Julia" %}}

**布尔**：`Bool`（8 位），`if` 只接受 `Bool`，`if 1` 是 `TypeError`。

**字符**：`Char`，32 位 Unicode 码点，单引号：`'A'`、`'中'`、`'😀'`；`Int('A') == 65`。

**字符串**：`String` 不可变、UTF-8，**按字节索引**——这是 Julia 最独特的地方。

```julia
s = "héllo"
length(s)             # 5：码点数
sizeof(s)             # 6：字节数
s[1]                  # 'h'：返回 Char
nextind(s, 1)         # 下一个字符的字节下标
# s[2]                # 🛑 StringIndexError：é 的第二字节不是字符起点
collect(s)            # ['h','é','l','l','o']
eachindex(s)          # 按字符边界前进的索引

SubString(s, 1, 1)    # 零拷贝子串
codeunits(s)          # 字节视图
Vector{UInt8}(s)      # 复制成字节数组
string(1, "a", 'b')   # 拼接
join(["a", "b"], ",")
"$s 的长度 $(length(s))"   # 插值
raw"C:\path"               # 原始字符串
```

代码演示 `length`（字符）与 `sizeof`（字节）的差别、`s[1]` 返回 `Char`，以及按字节索引会抛 `StringIndexError`。要点是：`String` 不可变且按**字节**索引，遍历要用 `for c in s` 或 `eachindex(s)`；字节视图用 `codeunits`。

{{% /tab %}}

{{% tab header="C#" %}}

**布尔**：`bool`，没有真值转换（`if (1)` 编译不过，这点和 C++ 相反）。

**字符**：`char` 是 16 位 UTF-16 码元，可以当数字用（`(int)'A' == 65`）。

**字符串**：`string` 不可变、UTF-16，引用类型但 `==` 按值比较内容；`StringBuilder` 用于可变拼接。

```csharp
string s = "héllo";
s.Length;                     // 5：UTF-16 码元数
s[1];                         // 'é'
System.Text.Encoding.UTF8.GetBytes(s);
string.Join(",", new[] { "a", "b" });

$"Hello, {name}! {name.Length}";     // 插值
@"C:\path\file";                     // 逐字字符串
ReadOnlySpan<byte> utf8 = "héllo"u8; // C# 11：UTF-8 字面量
```

代码演示 `Length`（UTF-16 码元）、`Encoding.UTF8.GetBytes` 与 C# 11 的 UTF-8 字面量 `u8`。要点是：`"😀".Length` 是 2，按码点遍历用 `Rune`；字符串比较用 `string.Equals(a, b, StringComparison.Ordinal)` 把语义写清楚。

循环拼接用 `StringBuilder`；

{{% /tab %}}

{{% tab header="Dart" %}}

**布尔**：`bool`，只有 `true`/`false`，`if (1)` 是编译错误。

**字符串**：`String` 不可变，UTF-16 码元；单双引号等价，支持插值与多行。

```dart
var s = 'héllo';
s.length;                  // 5：UTF-16 码元数
s.runes.length;            // 5：码点数
s.codeUnits;               // 码元列表
s[1];                      // 'é'（String，不是 char）

var t = 'Hello, $name! ${name.length}';
var raw = r'C:\path\n';    // 原始字符串

import 'dart:convert';
utf8.encode(s);            // Uint8List
utf8.decode(bytes);        // String

'👍🏽'.length;              // 4：UTF-16 码元
'👍🏽'.runes.length;        // 2：码点
```

代码演示 `length`/`runes`/`codeUnits` 三个层次与 `utf8.encode` 的转码。要点是：`length` 是 UTF-16 码元（emoji 算 2），要按字素簇处理得加 `characters` 包；字节数据用 `Uint8List`。

⚠️ `length` 是 UTF-16 码元数（`"😀".length == 2`）；按"人眼字符"处理要加 `characters` 包（`s.characters.length`）；`String.fromCharCodes` 不校验代理对。

{{% /tab %}}

{{% tab header="R" %}}

**布尔**：`logical`，取值 `TRUE`/`FALSE`/`NA`；`T` 和 `F` 只是可以被覆盖的变量，别在代码里用。`if` 只接受长度 1 的非 NA logical。

```r
s <- "héllo"
nchar(s)                     # 5：字符数
nchar(s, type = "bytes")     # 6：字节数
Encoding(s)                  # "UTF-8" 之类
substr(s, 1, 2)              # "hé"
toupper(s)
paste0(s, "!", 42)
sprintf("%s-%d", s, 42)
strsplit("a,b", ",")[[1]]    # c("a", "b")
gsub("l", "L", s)
```

代码演示 `nchar` 的三种 type、`substr`/`gsub` 与 `charToRaw`。要点是：`length("abc")` 是 1（向量元素个数），字符数要用 `nchar()`；排序受 locale 影响，要稳定结果用 `sort(method = "radix")`。

`==` 遇到 `NA` 返回 `NA`，判空用 `is.na()`。

{{% /tab %}}

{{% tab header="Zig" %}}

**布尔**：`bool`，只有 `true`/`false`，没有真值转换（`u1` 与 `bool` 是不同类型）。

**字符串**：没有字符串类型；双引号字面量是 `*const [N:0]u8`（带哨兵 0 的数组指针），通常当 `[]const u8` 用。

```zig
const std = @import("std");

pub fn main() !void {
    const s: []const u8 = "héllo";
    std.debug.print("{} bytes\n", .{s.len});                 // 6
    std.debug.print("{}\n", .{try std.unicode.utf8CountCodepoints(s)});  // 5

    var out: std.ArrayList(u8) = .empty;        // 0.15 起 ArrayList 是非托管版本
    defer out.deinit(std.heap.page_allocator);
    try out.appendSlice(std.heap.page_allocator, s);
    try out.append(std.heap.page_allocator, '!');
    std.debug.print("{s}\n", .{out.items});
}
```

代码演示 `[]const u8` 字符串、`utf8CountCodepoints` 与用 `std.ArrayList(u8)` 拼接。要点是：`[]const u8` 是只读切片，比较用 `std.mem.eql`（切片上的 `==` 编译不过）；0.15 起 `ArrayList` 的每个操作都要传 allocator。

⚠️ 字符串字面量不可变，`s[0] = 'H'` 编译失败；`[]const u8` 可能真的指向只读内存，别 `@constCast`。UTF-8 校验用 `std.unicode.utf8ValidateSlice`，按码点迭代用 `std.unicode.Utf8View`。

{{% /tab %}}

{{% tab header="Lua" %}}

**布尔**：`boolean`，只有 `false` 和 `nil` 为假——`0`、`""`、空表都是**真**。

**字符串**：不可变的字节序列（8 位安全），不自带编码信息；`#s` 是字节数、`string.sub` 按字节切。

```lua
local s = "héllo"            -- 5 个字符，6 个字节
print(#s)                     -- 6
print(utf8.len(s))            -- 5（Lua 5.3+ 的 utf8 库）
print(s:sub(1, 2))            -- 按字节切，中文会被切坏
print(string.byte("A"))       -- 65
print(string.char(65))        -- "A"
print(s .. "!")               -- .. 拼接
print(string.format("%s-%d", s, 42))
print(utf8.char(0x4E2D))      -- "中"
for pos, cp in utf8.codes(s) do end   -- 按码点迭代
```

代码演示 `#s`（字节数）、`utf8.len`（字符数）、`string.sub` 的字节切分与 `table.concat` 批量拼接。要点是：Lua 里 `0` 与 `""` 都是真值，`#s` 与 `string.sub` 都是字节语义，处理中文要显式用 `utf8` 库。

**字节串**：Lua 的 `string` 本身就是字节串，二进制数据直接存（`\0` 合法，`#s` 仍然准确）。

⚠️ `0` 和 `""` 是**真值**（不像 Python/JS/PHP），`if 0 then` 会执行；`#s`、`string.sub`、`string.find` 都是字节语义，处理中文要显式用 `utf8` 库；`string.format("%s", nil)` 会报错，先 `tostring`。

{{% /tab %}}

{{% tab header="TypeScript" %}}

**布尔**：`boolean`，类型层面还有字面量类型 `true`/`false`（常用于判别联合）。

**字符串**：`string` 不可变、UTF-16；类型层面可以用模板字面量类型表达格式约束。

```ts
const s = "héllo";
s.length;                        // 5：UTF-16 码元数
[...s].length;                   // 5：码点数
s.codePointAt(0);                // 104
String.fromCodePoint(0x1f600);   // "😀"

const name = "World";
const greet = `Hello, ${name}! ${name.length}`;
const raw = String.raw`C:\path\n`;     // 反斜杠不解释
type Id = `user-${number}`;            // 模板字面量类型（编译期）
```

**字节串**：`TextEncoder` / `TextDecoder`（UTF-8）、`Uint8Array`、Node 的 `Buffer`。

```ts
const bytes = new TextEncoder().encode(s);          // Uint8Array
const back = new TextDecoder("utf-8").decode(bytes);
```

代码演示 `length`（UTF-16 码元）与 `[...s]`（按码点展开）的差别，以及 `TextEncoder` 的 UTF-8 编码。要点是：`string` 不可变、类型系统不追踪编码，字符串与字节之间必须显式转换，按码点遍历用 `for...of` 或展开。

{{% /tab %}}

{{% tab header="JavaScript" %}}

**布尔**：falsy 值只有 `false`、`0`、`-0`、`0n`、`""`、`null`、`undefined`、`NaN`；其余都是真值——包括 `[]`、`{}`、`"0"`、`"false"`。

**字符串**：`string` 不可变、UTF-16。

```js
!!""               // false
!![]               // true ← 空数组是真值
Boolean("false")   // true ← 非空字符串都是真
new Boolean(false) // 🛑 对象，永远是真值，别这么写

const s = "héllo";
s.length;                    // 5：UTF-16 码元
[...s].length;               // 5：码点
s.at(-1);                    // 'o'（ES2022）
s.normalize("NFC");          // Unicode 规范化
"👍🏽".length;                // 4
Array.from("👍🏽").length;    // 2
```

代码演示 falsy 列表、`new Boolean(false)` 的陷阱与 `Array.from`/`[...s]` 按码点切分。要点是：`new Boolean(false)` 是真值、`[] == false` 为真，布尔判断一律 `!!x`；`for...of` 遍历字符串时按码点而不是码元。

字符串不可变，`s[0] = "H"` 静默失败（严格模式下抛错）。

{{% /tab %}}

{{% tab header="PHP" %}}

**布尔**：falsy 值有 `false`、`0`、`0.0`、`-0.0`、`""`、`"0"`、`[]`、`null`；`"0"` 为假是 PHP 独有的坑，而 **`NAN` 是真值**。

**字符串**：`string` 是不可变的字节序列（二进制安全），写时复制；PHP 8 起有 `str_contains` / `str_starts_with` / `str_ends_with`。

```php
$s = "héllo";
strlen($s);                   // 6：字节数
mb_strlen($s, "UTF-8");       // 5：字符数（需要 mbstring）
substr($s, 0, 2);             // 按字节切，会切断字符
mb_substr($s, 0, 2, "UTF-8"); // "hé"：按字符切
str_contains($s, "é");        // true（PHP 8）
implode(",", ["a", "b"]);
sprintf("%s-%d", $s, 42);
```

代码演示 `strlen` 与 `mb_strlen` 的差别、`mb_substr` 与 heredoc。要点是：PHP 默认字符串函数都是字节语义，处理中文必须用 `mb_*` 并显式传 `"UTF-8"`；`"0"` 是 falsy，正则要加 `/u` 修饰符。

正则要加 `/u` 修饰符才有 Unicode 语义。

{{% /tab %}}

{{% tab header="Ruby" %}}

**布尔**：只有 `false` 和 `nil` 为假——`0`、`""`、`[]` 都是**真**（与 PHP、Python、JS 都不同）。

**字符串**：`String` 是**可变**的，而且每个字符串自带 `Encoding`（默认 `UTF-8`）。

```ruby
s = "héllo"
s.length          # 5：字符数
s.bytesize        # 6：字节数
s.encoding        # #<Encoding:UTF-8>
s.chars           # ["h", "é", "l", "l", "o"]
s.codepoints
s[1]              # "é"
s.upcase!         # 原地修改（! 结尾是危险版本）
s << "!"          # 原地追加

bin = s.b         # 复制成 ASCII-8BIT（二进制）字符串
bin.bytesize      # 6
bin.force_encoding("UTF-8")   # 只改标签，不转码
s.encode("UTF-16LE")          # 真正转码
format("%s-%d", s, 42)
```

代码演示 `length`（字符）与 `bytesize`（字节）的差别、`chars`、`String#b` 与 `force_encoding`。要点是：`String` 可变且自带 encoding，`force_encoding` 只换标签不转码（转码用 `encode`），只有 `false`/`nil` 是假值。

⚠️ Ruby 字符串默认可变，常量也可能被调用方改掉——文件顶部加 `# frozen_string_literal: true` 更安全；`bytesize` 与 `length` 在非 ASCII 上不同；`force_encoding` 只换标签、`encode` 才转码；`if 0` 会执行（因为 0 是真值）。

{{% /tab %}}

{{< /tabpane >}}

---

## 复合类型

复合类型是差异最大的一节：有的语言把它做成语法（Go 的切片、Lua 的 table），有的语言只有标准库（C++ 的 `std::vector`），有的语言根本就没有（C 只有数组和指针）。下面按四类分开写，每类一套 18 语言标签页，方便横向对照。

### 数组与切片

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的数组是 `[T; N]`（长度属于类型、存在栈上），动态数组是 `Vec<T>`（堆分配、可增长），切片 `&[T]` 是指向连续元素的"胖指针"（指针 + 长度）。

```rust
let a = [1, 2, 3];             // [i32; 3]，栈上
let mut v = vec![0; 3];        // Vec<i32>
v.push(4);
let s: &[i32] = &v[1..];       // 借用切片，零拷贝
v.get(10)                      // None（安全）
// v[10]                       // 🛑 panic：越界
let arr: [i32; 3] = v[0..3].try_into().unwrap();
```

代码演示 `[T; N]`、`Vec<T>`、`&[T]` 三种形态，以及 `get()`（返回 `Option`）与下标（越界 panic）的区别。要点是：数组长度是类型的一部分，切片是借用视图——借用未结束就不能改 `Vec`；把切片转成定长数组用 `try_into()`。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `Array<T>` 是值语义的动态数组（写时复制）；`ArraySlice` 是共享底层存储的切片，但它的索引继承自原数组，`slice[0]` 常常会崩。

```swift
var a = [1, 2, 3]
a.append(4)
let slice = a[1...2]        // ArraySlice：共享存储
slice.startIndex            // 1 ← 不是 0！切片保留原索引
Array(slice)                // 复制成新数组，索引从 0 开始
a.first                     // Optional(1)
a[10]                       // 🛑 运行时崩溃
```

代码演示 `Array` 的增删、`ArraySlice` 的索引继承与 `first`/尾元素的可选返回。要点是：`Array` 是值语义（写时复制），`ArraySlice` 的索引来自原数组（所以 `slice[0]` 常崩），Swift 6.2 起还可以用 `InlineArray` 表达真正的定长数组。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的数组 `[N]T` 是值类型（赋值即复制），切片 `[]T` 是"指针 + 长度 + 容量"的三元组；`append` 是否扩容决定切片之间是否还共享底层数组。

```go
var a [3]int = [3]int{1, 2, 3}
b := a                 // 复制整个数组
s := []int{1, 2, 3}    // 切片
s = append(s, 4)       // 可能扩容（新底层数组）
sub := s[1:3]          // 共享底层数组
len(sub), cap(sub)     // 2, 2
slices.Contains(s, 4)  // Go 1.21+ 的 slices 包
```

代码演示数组赋值复制、切片共享底层数组、`append` 可能扩容，以及 `slices` 包的用法。要点是：数组是值类型、切片是"指针 + 长度 + 容量"；`append` 之后原切片可能看到新值也可能看不到，需要切断关系就 `slices.Clone`。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `list` 是动态、可变、异构的引用容器（切片会复制）；`array.array` 是紧凑的同质数组，数值计算通常用 NumPy 的 `ndarray`。

```python
a = [1, 2, 3]
a.append(4)
b = a[1:3]        # 新列表（复制）
a[::-1]           # 反转副本
del a[0]
[x * 2 for x in a]            # 列表推导
import array
c = array.array("i", [1, 2, 3])   # 紧凑 int 数组
```

代码演示 `list` 的增删、切片复制与 `array.array` 的紧凑存储。要点是：`list` 是引用容器、切片产生新列表（不是视图，要视图用 `memoryview`/NumPy），元素类型可以不同，性能敏感场景用 `array` 或 NumPy。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `Array<T>` 是对象数组，`IntArray`/`LongArray`/`DoubleArray` 等是免装箱的基本类型数组；动态列表用 `MutableList`，`subList` 返回的是视图而不是拷贝。

```kotlin
val a = intArrayOf(1, 2, 3)             // IntArray
val b = Array(3) { it * 2 }             // Array<Int>
val list = mutableListOf(1, 2, 3)
list.add(4)
list.getOrNull(10)                      // null（不抛）
val view = list.subList(1, 3)           // 视图，底层修改后会失效
```

代码演示 `IntArray`、`Array(n) { }`、`MutableList` 与 `subList` 视图。要点是：`IntArray` 等免装箱，`subList` 是视图（原列表结构性修改后失效），只读接口不代表底层不可变，需要真不可变先 `toList()`。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 `T[]` 是定长数组（长度不可变、元素可变），`ArrayList` 是动态数组（扩容约 1.5 倍），`List.of` 提供不可变列表。

```java
int[] a = new int[3];
int[] b = {1, 2, 3};
List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
list.add(4);
int[] c = Arrays.copyOf(b, 5);          // 复制 + 补零
List<Integer> view = Arrays.asList(1, 2, 3);   // 定长视图
// List<Integer>[] bad = new List<Integer>[3];  // 🛑 泛型数组不允许
```

代码演示数组创建、`Arrays.copyOf`、`List.of` 与 `Arrays.asList` 的定长视图。要点是：数组长度固定，`Arrays.asList` 不支持 `add`，泛型数组不能 `new List<String>[3]`（要用 `List<List<String>>`）。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的原生数组 `T arr[N]` 会退化成指针，`std::array<T,N>` 是值语义的定长数组，`std::vector<T>` 是动态数组，`std::span<T>`（C++20）是非拥有视图。

```cpp
int raw[3] = {1, 2, 3};
std::array<int, 3> a = {1, 2, 3};
std::vector<int> v = {1, 2, 3};
v.push_back(4);
v.reserve(100);                 // 预分配，避免反复扩容
std::span<int> s{v.data() + 1, 2};   // 视图，不拥有
v.at(10);                       // 抛 std::out_of_range
// v[10];                       // 🛑 未定义行为
```

代码演示原生数组、`std::array`、`std::vector`、`std::span`，以及 `at()` 与 `[]` 的区别。要点是：`vector` 扩容会让所有迭代器/指针/引用失效，`[]` 不做边界检查（越界是 UB），原生数组传参会退化成指针。

{{% /tab %}}

{{% tab header="C" %}}

C 只有 `T arr[N]`：数组名在表达式里几乎总会退化成指针，长度信息不会跟着传递，越界是未定义行为。

```c
int a[3] = {1, 2, 3};
size_t n = sizeof a / sizeof a[0];   // 只在同一作用域有效
int *p = a;                          // 退化成指针
p[1];                                // 2
int *heap = malloc(3 * sizeof(int)); // 动态数组
free(heap);
```

代码演示 `sizeof a / sizeof a[0]` 求长度、数组退化成指针与 `malloc` 动态数组。要点是：数组没有长度信息（传参后 `sizeof` 只能得到指针大小），越界是 UB 而不是异常，动态内存要配对 `free`。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `Vector{T}` 是动态一维数组（索引从 1 开始），`Array{T,N}` 支持多维；`a[2:3]` 会复制，`view(a, 2:3)` 才是视图。

```julia
a = [1, 2, 3]              # Vector{Int64}
push!(a, 4)
b = a[2:3]                 # 复制
v = view(a, 2:3)           # 视图，不复制
zeros(3), fill(0, 3), Vector{Int}(undef, 3)
A = [1 2; 3 4]             # 2×2 Matrix（列主序）
size(A), length(A)
```

代码演示 1 起始索引、切片复制与 `view` 视图的差别，以及多维数组与 `size`。要点是：索引从 1 开始，`a[2:3]` 复制而 `view(a, 2:3)` 不复制，`Vector{Any}` 会装箱——性能敏感处要标注具体元素类型或用 `StaticArrays`。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `T[]` 是定长数组，`List<T>` 是动态列表；`Span<T>`/`ReadOnlySpan<T>` 是安全视图（可指向栈内存），`Array.Resize` 其实是新建加复制。

```csharp
int[] a = new int[3];
var list = new List<int> { 1, 2, 3 };
list.Add(4);
Span<int> span = a.AsSpan(1, 2);        // 视图
ReadOnlySpan<char> ro = "abc";
Array.Resize(ref a, 10);                // 其实是新建 + 复制
a[^1];                                  // 最后一个元素（Index 语法）
```

代码演示数组、`List<T>`、`Span<T>` 视图与 `Array.Resize` 的真实行为。要点是：`Array.Resize` 其实是新建 + 复制（旧引用失效），`Span<T>` 不能跨 `await`，`arr[^1]` 是 C# 8 的尾部索引语法。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `List<T>` 是动态列表（`[]` 默认可增长，`List.filled(n, x, growable: false)` 定长）；紧凑的数值数组用 `Uint8List`/`Int32List` 等 TypedData。

```dart
var a = [1, 2, 3];
a.add(4);
var fixed = List.filled(3, 0, growable: false);
fixed[0] = 5;
var range = a.getRange(1, 3);        // Iterable（惰性视图）
a.sublist(1, 3);                     // 复制
a[10];                               // 🛑 RangeError
Uint8List(4);                        // 紧凑字节数组
```

代码演示 `List` 的增删、`List.filled(..., growable: false)` 定长、`getRange` 与 `sublist` 的差别以及越界异常。要点是：`getRange` 返回的是惰性 `Iterable`（原列表变了它也变），`sublist` 才是复制；真只读用 `List.unmodifiable`。

{{% /tab %}}

{{% tab header="R" %}}

R 的"数组"是向量：`c(1, 2, 3)` 创建同类型向量，`matrix()`/`array()` 是多维版本；异构数据用 `list`，索引从 1 开始，负索引表示排除。

```r
x <- c(1, 2, 3)        # double 向量
typeof(x)              # "double"
x + 1                  # [1] 2 3 4 ← 向量化，无循环
x[x > 1]               # [1] 2 3   逻辑索引
x[-1]                  # [1] 2 3   负索引 = 排除
m <- matrix(1:6, nrow = 2)
length(x); dim(m)
y <- vector("integer", 3)   # 预分配
```

代码演示向量化运算、逻辑索引、负索引与 `matrix`、`vector()` 预分配。要点是：索引从 1 开始，`x[-1]` 表示"排除第一个"而不是取尾部，循环里 `c(x, v)` 会反复复制整个向量（应预分配或向量化）。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `[N]T` 是值类型数组（可带哨兵 `[N:0]T`），`[]T` 是切片（指针 + 长度），动态增长用标准库的 `std.ArrayList`（0.15 起是非托管版本）。

```zig
const a = [3]u8{ 1, 2, 3 };
const b = [_]u8{ 1, 2, 3 };        // 长度自动推断
var v: std.ArrayList(u8) = .empty;      // 0.15 起非托管，操作时传 allocator
defer v.deinit(allocator);
try v.append(allocator, 4);
const slice: []u8 = v.items;
slice[10];                          // 🛑 安全模式 panic
```

代码演示 `[N]T`、`[_]T{...}` 自动推断长度与 `std.ArrayList`（0.15 起是非托管版本）。要点是：数组赋值是值拷贝、切片是"指针 + 长度"的胖指针，`ArrayList` 的每个操作都要传 allocator 并 `defer deinit`。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有数组类型：数组就是"键为 1..n 的 table"，用 `#t` 取边界长度、`ipairs` 遍历数组部分、`table.insert/sort/concat` 操作它。

```lua
local a = {1, 2, 3}
table.insert(a, 4)
print(#a)                -- 4：边界长度
print(a[1], a[#a])       -- 1  4
for i, v in ipairs(a) do end   -- 只遍历 1..n
table.sort(a)
table.concat(a, ",")
local packed = table.pack(1, nil, 3)   -- 记录 n
```

代码演示 `{}`、`table.insert`、`#t`、`ipairs` 与 `table.pack`。要点是：索引从 1 开始，`#t` 在稀疏表上结果未定义，越界读得到 `nil` 而不是报错；批量拼接用 `table.concat`。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 在类型层面提供 `T[]`/`Array<T>`/`readonly T[]`/`ReadonlyArray<T>` 与元组；运行时还是 JS 数组，只读只是编译期约束。

```ts
const a: number[] = [1, 2, 3];
const ro: readonly number[] = a;     // 只读视图（编译期约束）
const t: [number, string] = [1, "a"];
a.at(-1);
const copy = a.slice(1);             // 复制
a.splice(0, 1);                      // 原地删除
```

代码演示 `readonly number[]`、元组、`slice`（复制）与 `splice`（原地修改）。要点是：`readonly` 只在编译期有效，`Array(3)` 是"长度 3 但没有元素"的空槽数组（`Array.from({length: 3})` 才有元素），运行时仍然是 JS 数组。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `Array` 是动态、可稀疏、异构的；`new Array(3)` 是"长度为 3 但没有元素"的空槽数组，数值密集场景应改用 TypedArray。

```js
const a = [1, 2, 3];
a.push(4);
new Array(3).length;          // 3，但没有元素（空槽）
Array.from({ length: 3 });    // [undefined, undefined, undefined]
[10, 9, 100].sort();          // [10, 100, 9] ← 默认按字符串排序！
[10, 9, 100].sort((x, y) => x - y);   // [9, 10, 100]
a.slice(1);                   // 复制
a.splice(0, 1);               // 原地删除
new Float64Array(3);          // 紧凑数值数组
```

代码演示 `sort()` 默认按字符串排序、`splice` 原地删除与 `Float64Array` 的紧凑存储。要点是：数字排序必须传比较函数，`length` 可写（会截断数组），`slice` 复制而 `splice` 原地改，数值密集场景用 TypedArray。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `array` 是有序映射：键可以是 int 或 string，因此同一个类型同时充当列表、字典与集合；需要定长数组用 `SplFixedArray`。

```php
$a = [1, 2, 3];
$a[] = 4;                      // 追加
array_push($a, 5);
array_pop($a);
count($a);
array_slice($a, 1, 2);
array_map(fn($x) => $x * 2, $a);
in_array(3, $a, true);         // 第三个参数严格比较，务必传
$m = ["a" => 1, "b" => 2];     // 同一个类型当映射用
```

代码演示 `$a[]` 追加、`array_slice`、`in_array` 的严格参数与关联数组。要点是：`array` 是值类型（写时复制），`in_array` 默认松散比较（一律传 `true`），`$a[5]` 与 `$a["5"]` 其实是同一个键。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的 `Array` 是动态、异构、可变的序列，支持负索引与切片；注意 `Array.new(n, obj)` 会用同一个对象填充所有位置。

```ruby
a = [1, 2, 3]
a << 4                 # 追加
a.push(5); a.pop
a[1..2]                # [2, 3]
a[-1]                  # 5：最后一个
a.first(2)             # [1, 2]
Array.new(3, 0)        # [0, 0, 0]
Array.new(3, [])       # 🛑 三个元素是同一个数组对象！
Array.new(3) { [] }    # ✅ 各自独立
a.map { |x| x * 2 }
a.sum
```

代码演示 `<<` 追加、切片、`Array.new(3, [])` 的共享陷阱与 `map`/`sum`。要点是：`Array.new(n, obj)` 会让所有位置指向同一个对象（要用块形式 `Array.new(n) { [] }`），负索引从尾部数，`map` 返回新数组。

{{% /tab %}}

{{< /tabpane >}}

### 元组

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 有真正的元组类型：定长、异构、可以解构，元素用 `.0`/`.1` 访问；函数返回多个值其实就是返回一个元组。

```rust
let t = (1, "a", 3.0);
let (a, b, c) = t;         // 解构
t.0; t.1;                  // 按下标访问
let single = (1,);         // 单元素元组必须带逗号
let unit = ();             // 空元组 = unit
fn min_max(v: &[i32]) -> (i32, i32) { (v[0], v[1]) }   // 多返回值
```

代码演示元组定义、解构、`.0`/`.1` 访问、单元素元组必须写 `(1,)`，以及用元组实现多返回值。要点是：元组是定长、异构的值类型，字段没有名字（要名字就用 struct），`()` 是 unit 类型；常用 trait 只对不超过 12 个元素的元组自动实现。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的元组是值类型，可以带标签（`(x: 1, y: 2)`），最常见的用途是多返回值；但它不能带方法、不能遵循协议。

```swift
let t = (1, "a")
t.0; t.1
let (a, b) = t

let point = (x: 1, y: 2)   // 带标签的元组
point.x; point.y

func minMax(_ v: [Int]) -> (min: Int, max: Int) { (v.min()!, v.max()!) }
let r = minMax([3, 1, 2])
r.min
```

代码演示普通元组、带标签元组与"函数返回多个值"的写法。`let (a, b) = t` 解构之后可读性最好，字段超过两三个就该换成 struct。

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有元组类型**，只是函数可以返回多个值，所以语言里有 `a, b := f()` 和 `v, ok := m[k]` 这种多值赋值/逗号-ok 惯用法。

```go
func minMax(v []int) (int, int) { return v[0], v[1] }

a, b := minMax([]int{1, 2})     // 只是两个值，不是元组
v, ok := m["key"]               // 惯用的 comma-ok
_, err := os.ReadFile("x")      // 忽略第一个返回值
```

代码演示 `a, b := f()`、`v, ok := m[k]` 与用 `_` 忽略返回值。要点是：Go 只有"多返回值"，没有元组类型，所以多值不能赋给变量、不能放进容器；要传递就定义一个 struct。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `tuple` 是不可变、异构、可嵌套的序列，可以作为字典的键；支持解包、命名元组（`NamedTuple`）与"元组比列表更省内存"的用法。

```python
t = (1, "a", 3.0)        # 不可变、异构、可哈希
single = (1,)            # 逗号不能省，(1) 是整数
a, b, c = t              # 解包
first, *rest = t
x, y = y, x              # 交换

from typing import NamedTuple
class Point(NamedTuple):
    x: int
    y: int
```

代码演示元组创建、单元素必须带逗号、解包（含 `*rest`）与 `NamedTuple`。要点是：`tuple` 不可变、元素可哈希时本身也可作字典键；但不可变只是浅层——元组里装 list 照样能改。

⚠️ 元组不可变但不深不可变——里面装 `list` 照样能改；`t = ([],)` 之后 `t[0].append(1)` 是合法的。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 标准库只提供 `Pair` 与 `Triple` 两个元组式容器，都支持解构；字段超过三个就定义 `data class`（自动获得解构与 `copy`）。

```kotlin
val p = Pair("a", 1)
val t = Triple("a", 1, true)
val (name, count) = p          // 解构
p.first; p.second
val q = "key" to 42            // 中缀创建 Pair

data class Point(val x: Int, val y: Int)
val (x, y) = Point(1, 2)       // data class 也支持解构
```

代码演示 `Pair`/`Triple`、`to` 中缀创建与解构。要点是：标准库只有这两个元组容器，字段再多就定义 `data class`（它自动生成 `componentN()`，所以解构照样能用）。

{{% /tab %}}

{{% tab header="Java" %}}

Java 没有元组类型；Java 16 起用 `record` 作为官方推荐的多值载体，`Map.Entry` 偶尔被当作二元组使用。

```java
record Point(int x, int y) { }     // Java 16+ 的标准做法
Point p = new Point(1, 2);
p.x(); p.y();

Map.Entry<String, Integer> e = Map.entry("a", 1);   // 偶尔当二元组
var pair = new AbstractMap.SimpleEntry<>("a", 1);
```

代码演示 `record` 作为多值载体，以及 `Map.entry` 这种临时二元组。要点是：Java 没有元组，`record`（Java 16+）是官方推荐替代：不可变、按值相等，比第三方 Tuple 类库更符合语言习惯。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 用 `std::pair`（两个值）与 `std::tuple`（任意个数）表示异构定长组合，取值用 `std::get` 或 C++17 的结构化绑定。

```cpp
std::pair<int, std::string> p{1, "a"};
p.first; p.second;

std::tuple<int, std::string, double> t{1, "a", 3.0};
std::get<0>(t);
auto [a, b, c] = t;              // C++17 结构化绑定
auto m = std::make_tuple(1, 2);
std::apply([](auto... xs) { return (xs + ...); }, m);   // C++17
```

代码演示 `std::pair`（`.first`/`.second`）、`std::tuple` 的 `std::get`、结构化绑定与 `std::apply`。要点是：`pair` 有字段名、`tuple` 只能按序号取；`std::tie` 可以把已有变量打包，字段多了结构体通常比 tuple 更可读。

{{% /tab %}}

{{% tab header="C" %}}

C 没有元组：多值返回要么返回 struct（值拷贝），要么用输出参数（指针）。

```c
struct point { int x, y; };

struct point make(void) { return (struct point){1, 2}; }   // 复合字面量
void split(int v, int *a, int *b) { *a = v; *b = v + 1; }  // 输出参数

struct point p = make();
```

代码演示用 struct 返回多值，以及用输出参数（指针）返回多个结果。要点是：C 没有元组，struct 返回是值拷贝（安全），输出参数则要求调用方先把变量准备好并传地址。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的元组 `(a, b, c)` 不可变、异构，而且类型是精确的 `Tuple{...}`；`NamedTuple` 给字段起名，多返回值也是元组。

```julia
t = (1, "a", 3.0)        # Tuple{Int64, String, Float64}
t[1]                     # 1（1-based）
a, b, c = t              # 解构
nt = (x = 1, y = 2)      # NamedTuple
nt.x

values(nt)               # (1, 2)：NamedTuple 是具名字段的 Tuple
f() = (1, "a")           # 多返回值就是元组
```

代码演示元组创建、`t[1]`（1 起始）、解构与 `NamedTuple`。要点是：元组不可变、异构且类型精确（`Tuple{Int64,String}`），小元组性能极好；需要字段名用 `NamedTuple`，要返回多值直接 `return a, b`。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `(int, string)` 语法编译成值类型 `ValueTuple`，元素可以命名、可以解构；老的 `Tuple<...>` 是引用类型，现在基本不用了。

```csharp
(int, string) t = (1, "a");        // C# 7 元组语法
var (a, b) = t;                    // 解构
t.Item1; t.Item2;

(int x, int y) p = (1, 2);         // 命名元素
p.x;

// 老写法（引用类型，别用）
Tuple<int, string> old = Tuple.Create(1, "a");
```

要点是：C# 7 起元组是值类型 `ValueTuple`，可命名、可解构、按字段相等；

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 3 引入 record：`(1, 'a')` 是位置记录、`(x: 1, y: 2)` 是命名记录，它们不可变、结构相等、支持解构与类型注解。

```dart
var t = (1, 'a');                  // 位置记录
var p = (x: 1, y: 2);              // 命名记录
print(t.$1); print(p.x);
var (a, b) = t;                    // 解构
(int, String) typed = (1, 'a');    // 类型注解
```

代码演示 record 的位置与命名两种形式、`$1`/`.x` 访问与解构。要点是：record 不可变、结构相等（`(1, 'a') == (1, 'a')` 为真）、类型精确；Dart 3 之前只能退化成 List 或自定义类。

{{% /tab %}}

{{% tab header="R" %}}

R 没有元组类型；`c()` 装同质数据、`list()` 装异构数据，函数返回多个值就是返回一个 list。

```r
pair <- list(1, "a")        # 异构：用 list
v <- c(1, 2, 3)             # 同质的才是向量
unlist(list("1", "2"))

f <- function() list(min = 1, max = 2)   # 多返回值用 list
r <- f(); r$min
```

代码演示用 `list` 装异构数据、`c()` 强制同质、`unlist` 与函数返回 list。要点是：`c(1, "a")` 会把所有元素强制成字符串，要保住类型必须用 `list`；命名 list 常被当作"记录"使用。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的元组就是"字段名是下标的匿名 struct"：`.{ 1, "a" }`，用 `t[0]` 访问、可以解构，没有单独的 tuple 类型。

```zig
const t = .{ 1, "a", 3.0 };      // 匿名 struct，字段是 0、1、2
t[0]; t[1]; t.len;
const a, const b, const c = t;   // 解构

const p = .{ .x = 1, .y = 2 };   // 具名匿名 struct
p.x;
const Tuple = std.meta.Tuple(&.{ i32, []const u8 });   // 显式类型
```

代码演示 `.{}` 匿名 struct 当元组、`t[0]`、`t.len` 与解构。要点是：Zig 的"元组"和"记录"是同一个东西（字段名是下标的匿名 struct），所以不需要两套概念。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有元组类型，但函数可以返回多个值；要在数据结构里传递就 `table.pack(...)` 打包、`table.unpack(...)` 解包。

```lua
local function minmax(t) return t[1], t[2] end

local a, b = minmax({1, 2})       -- 多值赋值
print(select("#", minmax({1, 2})))  -- 2：返回值个数

local packed = table.pack(minmax({1, 2}))   -- 打包成表
print(packed.n)                              -- 2（table.pack 记录 n）
local x, y = table.unpack(packed)             -- 解包
```

代码演示多返回值、`select("#", ...)` 计数与 `table.pack`/`table.unpack` 打包解包。要点是：多返回值只在表达式最后位置展开（放在中间会被截断成第一个值），要跨调用传递就先 `table.pack`。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的元组类型 `[number, string]` 能精确描述"定长、每个位置类型不同"的数组（还可具名、可选、rest），但运行时仍是普通数组。

```ts
const t: [number, string] = [1, "a"];
const named: [x: number, y: string] = [1, "a"];   // TS 4.0 具名元组
const opt: [number, string?] = [1];
const rest: [number, ...string[]] = [1, "a", "b"];
const ro: readonly [number, string] = [1, "a"];
const lit = [1, "a"] as const;      // 字面量元组 readonly [1, "a"]
const [a, b] = t;
```

代码演示元组类型、具名/可选/rest 元素与 `as const`。要点是：元组类型只在编译期描述"定长 + 每位置类型不同"，运行时仍是普通数组——越界读是 `undefined`，长度也能被改。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有元组类型，惯例是用数组加解构：`const [a, b] = pair;`。

```js
const pair = [1, "a"];
const [a, b] = pair;
const [x, ...rest] = [1, 2, 3];
[a, b] = [b, a];               // 交换，注意分号

function minMax(v) { return [Math.min(...v), Math.max(...v)]; }
const [lo, hi] = minMax([3, 1, 2]);
```

代码演示数组解构、rest 解构与用数组返回多值。要点是：没有元组类型，解构只是语法糖；需要不可变就 `Object.freeze`（浅冻结），需要类型约束就上 TypeScript。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有元组，用数组加解构：`[$a, $b] = $pair;`（PHP 7.1+），老的写法是 `list($a, $b)`。

```php
$pair = [1, "a"];
[$a, $b] = $pair;              // PHP 7.1+ 解构
list($a, $b) = $pair;          // 老写法，等价
[$a, , $c] = [1, 2, 3];        // 跳过元素

function minMax(array $v): array { return [min($v), max($v)]; }
[$lo, $hi] = minMax([3, 1, 2]);
```

代码演示 `[$a, $b] = $pair`、`list()` 与跳过元素。要点是：PHP 用数组 + 解构模拟元组，数组是值类型（赋值复制），`...` 展开运算符可以把数组摊成参数列表。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有元组类型，多重赋值 `a, b = 1, 2` 只是语法糖；要"记录"就用 `Struct` 或 Ruby 3.2 的 `Data.define`。

```ruby
a, b = 1, 2
a, b = b, a                    # 交换
x, *rest = [1, 2, 3]           # x=1, rest=[2,3]
first, = [1, 2]                # 只取第一个

h = { name: "a", age: 1 }
h in { name: String => n }     # Ruby 3 的模式匹配（deconstruct_keys）

Point = Data.define(:x, :y)    # Ruby 3.2+：不可变的值对象
p1 = Point.new(x: 1, y: 2)
```

代码演示多重赋值、splat 解构与 `Data.define`。要点是：多重赋值只是语法糖（底层还是数组），要"记录"用 `Data`（不可变、结构相等）或 `Struct`（可变）。

{{% /tab %}}

{{< /tabpane >}}

### 映射与集合

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的映射与集合都在 `std::collections`：`HashMap`/`HashSet` 基于哈希（默认 SipHash，抗 HashDoS 但偏慢），`BTreeMap`/`BTreeSet` 基于 B 树保持有序。

```rust
use std::collections::{HashMap, HashSet, BTreeMap};

let mut m = HashMap::new();
m.insert("a", 1);
m.get("a");                      // Option<&i32>
*m.entry("b").or_insert(0) += 1; // 缺失时插入再自增
m.contains_key("a");

let mut s: HashSet<i32> = HashSet::from([1, 2, 3]);
s.insert(4);
s.contains(&4);
```

代码演示 `HashMap` 的增改查、`entry().or_insert()` 与 `HashSet` 的插入/包含。要点是：`get` 返回 `Option`，`entry` 是"缺失则插入"的惯用法；`HashMap` 无序（默认 SipHash 抗 HashDoS），要顺序用 `BTreeMap`，要插入序用 `IndexMap`。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `Dictionary<K, V>` 与 `Set<T>` 都是值类型（写时复制），元素必须遵循 `Hashable`；字典本身无序，需要顺序要自己排序。

```swift
var m: [String: Int] = ["a": 1]
m["b"] = 2
m["a"]                  // Optional(1) —— 没有就 nil
m["a", default: 0]      // 有默认值的读取（不插入）
m.updateValue(9, forKey: "a")
for (k, v) in m { }

var s: Set<Int> = [1, 2, 3]
s.insert(4)
s.contains(4)
s.union([5, 6]); s.intersection([1, 2])
```

代码演示字典赋值、可空取值、`default:` 下标与 `Set` 的并/交运算。`m[k, default:]` 读取时不会插入键。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的内建 `map[K]V` 是哈希表（引用类型、键必须可比较、遍历顺序随机），并发读写会 panic；**没有内建集合**，通常用 `map[T]struct{}` 模拟。

```go
m := map[string]int{"a": 1}
m["b"] = 2
v, ok := m["a"]          // comma-ok：区分 0 与"不存在"
delete(m, "a")
len(m)

for k, v := range m { }   // 顺序随机

set := map[string]struct{}{}   // 模拟集合
set["a"] = struct{}{}
_, exists := set["a"]
```

代码演示 `map` 的增删查、comma-ok 与"用 `map[T]struct{}` 当集合"。Go 没有内建 set，`maps`/`slices` 包（1.21+）提供了常用算法。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `dict` 从 3.7 起保证插入顺序，键必须可哈希；`set`/`frozenset` 是去重集合，`collections.Counter` 是多重集，`defaultdict` 处理缺失键。

```python
d = {"a": 1}                  # 3.7+ 保留插入顺序
d["b"] = 2
d.get("c", 0)                 # 不存在给默认值
d.setdefault("c", [])
d | {"d": 4}                  # 3.9+ 合并
for k, v in d.items(): ...

s = {1, 2, 3}                 # set（无序、去重）
s | {4}; s & {1, 2}; s - {1}  # 并、交、差
fs = frozenset([1, 2])        # 可哈希，能当字典键
from collections import Counter   # 多重集
```

代码演示 `dict` 的增改、`get`/`setdefault`、`|` 合并与 `set` 的集合运算。`d[k]` 缺失抛 `KeyError`（日常用 `.get()`），`Counter` 是"元素 → 计数"的多重集。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `Map`/`Set` 是只读接口，`MutableMap`/`MutableSet` 才提供修改方法；默认实现是 `LinkedHashMap`/`LinkedHashSet`，保留插入顺序。

```kotlin
val m = mutableMapOf("a" to 1)      // LinkedHashMap：保留插入顺序
m["b"] = 2
m["a"]                              // Int? 可空
m.getOrDefault("c", 0)
m.getOrPut("d") { 0 }
m.getOrElse("e") { 0 }

val s = mutableSetOf(1, 2, 3)       // LinkedHashSet
s.add(4)
```

代码演示 `mutableMapOf`、`getOrDefault`/`getOrPut` 与 `mutableSetOf`。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 `HashMap` 无序、`LinkedHashMap` 保插入序、`TreeMap` 按键排序，对应的 `HashSet`/`LinkedHashSet`/`TreeSet` 同理；作为键的类型必须正确实现 `equals` 与 `hashCode`。

```java
Map<String, Integer> m = new HashMap<>();        // 无序
Map<String, Integer> lm = new LinkedHashMap<>();  // 保插入序
Map<String, Integer> tm = new TreeMap<>();        // 按键排序
m.put("a", 1);
m.getOrDefault("b", 0);
m.computeIfAbsent("c", k -> 0);
m.merge("a", 1, Integer::sum);
m.forEach((k, v) -> { });

Set<String> s = new HashSet<>();
Map<String, Integer> immut = Map.of("a", 1, "b", 2);   // Java 9+
```

代码演示 `HashMap`/`LinkedHashMap`/`TreeMap`、`computeIfAbsent`/`merge` 与 `Set`。并发场景用 `ConcurrentHashMap`。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的 `std::map`/`std::set` 是红黑树（有序、比较用 `operator<`），`std::unordered_map`/`unordered_set` 是哈希表；注意 `m[k]` 会插入默认值。

```cpp
std::map<std::string, int> m;             // 红黑树，有序
std::unordered_map<std::string, int> um;  // 哈希，无序
m["a"] = 1;                                // ⚠️ 不存在就默认构造并插入
m.find("b"); m.contains("b");              // C++20 起有 contains
m.try_emplace("c", 3);                     // C++17：已存在就不动

std::set<int> s{1, 2, 3};
std::unordered_set<int> us{1, 2, 3};
```

代码演示 `std::map`/`unordered_map` 的插入、`find`/`contains` 与 `try_emplace`。要点是：`m[k]` 会插入默认值（读操作有副作用），只查不改要用 `find`/`contains`/`at`；`map` 需要 `operator<`，哈希表需要哈希与相等。

{{% /tab %}}

{{% tab header="C" %}}

C 没有映射与集合类型，标准库也不提供；实际项目用 uthash（宏实现）、GLib 的 `GHashTable`/`GTree`，或小规模用数组线性查找。

```c
/* 常见做法：开放寻址或链地址法自己写，或用库 */
/* POSIX 的 hsearch 很弱，通常用第三方：*/
/* - uthash（宏实现的哈希表，头文件即用）      */
/* - GLib 的 GHashTable / GTree               */
/* - 或者小规模就用数组线性查找               */
```

要点是：没有哈希函数、迭代器与自动扩容，键的内存（如 `strdup` 出来的）与释放都要自己管。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `Dict{K,V}` 与 `Set{T}` 在标准库；键按 `isequal`/`hash` 语义比较，迭代顺序不应依赖（需要顺序用 `OrderedDict` 或排序后再遍历）。

```julia
d = Dict("a" => 1, "b" => 2)
d["c"] = 3
get(d, "x", 0)            # 不存在给默认值
get!(d, "y") do; 0 end
haskey(d, "a")
keys(d); values(d)
for (k, v) in d ... end

s = Set([1, 2, 3])
push!(s, 4)
intersect(s, Set([2, 3]))   # 集合运算：union/intersect/setdiff
```

代码演示 `Dict` 的增改查、`get`/`get!` 与 `Set` 的集合运算。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `Dictionary<K,V>` 是哈希表、`SortedDictionary<K,V>` 是树实现，集合有 `HashSet<T>`/`SortedSet<T>`；读取优先用 `TryGetValue`（索引器找不到会抛异常）。

```csharp
var m = new Dictionary<string, int> { ["a"] = 1 };
m["b"] = 2;
m.TryGetValue("a", out var v);      // 首选的读取方式
m.GetValueOrDefault("c");
m.TryAdd("d", 4);
// m["zzz"]                          // 🛑 KeyNotFoundException

var s = new HashSet<int> { 1, 2, 3 };
s.Add(4); s.Contains(4);
var sd = new SortedSet<int>();       // 有序
```

代码演示 `Dictionary` 的索引器、`TryGetValue`/`GetValueOrDefault`/`TryAdd` 与 `HashSet`。要点是：索引器读不存在的键会抛 `KeyNotFoundException`，读取优先 `TryGetValue`；自定义类型做键要同时重写 `Equals` 与 `GetHashCode`。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `Map<K,V>` 与 `Set<T>` 都是内建容器，默认实现是保插入顺序的 `LinkedHashMap`/`LinkedHashSet`；注意空 `{}` 是 Map，`<int>{}` 才是 Set。

```dart
var m = {'a': 1};                  // Map<String, int>，默认 LinkedHashMap
m['b'] = 2;
m['a'];                            // int? 可空
m.putIfAbsent('c', () => 0);
m.update('a', (v) => v + 1, ifAbsent: () => 0);
m.containsKey('a');

var s = <int>{1, 2, 3};            // ⚠️ Set 字面量必须带类型或类型上下文
s.add(4);
s.union({5}); s.intersection({1});
```

代码演示 `Map` 的索引器（返回可空）、`putIfAbsent`/`update` 与 `<int>{}` 的 Set 字面量。Map 默认是保插入序的 `LinkedHashMap`，自定义键要重写 `==`/`hashCode`。

{{% /tab %}}

{{% tab header="R" %}}

R 没有内建哈希表：命名 `list` 常被当作映射用（名字查找是线性扫描），真正的哈希表是 `environment`；集合运算靠向量化的 `unique`/`intersect`/`union`/`setdiff`/`%in%`。

```r
l <- list(a = 1, b = 2)      # 命名 list：最常用的"映射"
l$a; l[["a"]]
names(l)

e <- new.env(hash = TRUE)    # 环境（environment）才是真正的哈希表
assign("a", 1, envir = e)
get("a", envir = e)
exists("a", envir = e)

# 集合运算（向量）
unique(c(1, 1, 2))
intersect(c(1, 2), c(2, 3))
union(1:2, 2:3)
setdiff(1:3, 2)
%in%                          # 成员测试
```

代码演示命名 list、`environment` 的 `assign`/`get` 与 `unique`/`intersect`/`%in%` 这些集合运算。R 里的"集合"就是去重后的向量，运算是向量化的。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的哈希表在标准库：`std.AutoHashMap(K,V)`、`std.StringHashMap`、保序的 `std.AutoArrayHashMap`；"集合"就是 value 为 `void` 的 map，所有表都必须显式 `init(allocator)` 与 `deinit()`。

```zig
var m = std.AutoHashMap(u32, []const u8).init(allocator);
defer m.deinit();
try m.put(1, "a");
m.get(1);                     // ?[]const u8
const gop = try m.getOrPut(2);
if (!gop.found_existing) gop.value_ptr.* = "b";

var sm = std.StringHashMap(u32).init(allocator);   // []const u8 做键
var om = std.AutoArrayHashMap(u32, u32).init(allocator);  // 保插入序

var set = std.AutoHashMap(u32, void).init(allocator);     // 集合 = value 为 void
```

要点是：哈希表必须 `init(allocator)` 并 `deinit()`，`StringHashMap` 已经按内容比较字符串，需要保插入序就用 `AutoArrayHashMap`。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的 table 同时是字典、集合、数组与对象；键可以是任何非 nil 值（表、函数也能当键），给键赋 nil 就是删除它，迭代顺序未定义。

```lua
local t = { a = 1, b = 2 }      -- 一切皆 table
t.c = 3
print(t.a, t["a"])
t.d = nil                        -- nil 表示"删除这个键"
for k, v in pairs(t) do end      -- 顺序未定义

local set = {}
set["apple"] = true
if set["apple"] then end

-- 用元表模拟默认值
setmetatable(t, { __index = function(_, k) return 0 end })
```

代码演示 table 当字典与集合、`nil` 删除键、以及元表 `__index` 提供默认值。要点是：键可以是任何非 nil 值，`t.k == nil` 既表示"不存在"也表示"值是 nil"，遍历用 `pairs`（顺序未定义）。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 在运行时用 `Map`/`Set`（保插入顺序、键可以是任意类型、用 SameValueZero 语义），对象字面量只能当 string/symbol 键的映射。

```ts
const m = new Map<string, number>([["a", 1]]);   // 保插入序，键任意
m.set("b", 2);
m.get("a");                  // number | undefined
m.has("a"); m.size;

const s = new Set<number>([1, 2, 3]);
s.add(4); s.has(4); s.size;

const rec: Record<string, number> = { a: 1 };     // 对象当映射（键只能是 string/symbol）
const wm = new WeakMap<object, number>();         // 键是弱引用
```

代码演示 `Map`/`Set` 的用法、`Record<string, number>` 与 `WeakMap`。要点是：`Map` 保插入序、键可以是任意类型、按 SameValueZero 比较；普通对象当字典会继承原型链，纯映射请用 `Map` 或 `Object.create(null)`。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `Map`/`Set` 是 ES2015 内建容器，`WeakMap`/`WeakSet` 持有弱引用；把普通对象当字典要注意原型链污染，用 `Object.create(null)` 或 `Map`。

```js
const m = new Map([["a", 1]]);
m.set("b", 2); m.get("a"); m.has("a"); m.size;
[...m.entries()];

const s = new Set([1, 1, 2]);       // Set(2) {1, 2}
s.add(3); s.has(3); s.size;
[...new Set([1, 1, 2])];            // 去重惯用法

const obj = Object.create(null);    // 纯字典，无原型污染
Object.hasOwn(obj, "a");           // ES2022
```

代码演示 `Map`/`Set`、`[...new Set(arr)]` 去重与 `Object.hasOwn`。要点是：`Map` 的键按引用比较（对象键要拿同一个引用才能取回），`Set` 按插入顺序迭代；`WeakMap`/`WeakSet` 的键必须是对象且不阻止回收。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `array` 就是映射：键可以是 int 或 string、保留插入顺序，同一个类型同时当列表/字典/集合用；`isset` 对 null 值返回 false，判"键存在"要用 `array_key_exists`。

```php
$m = ["a" => 1, "b" => 2];      // array 就是映射（保插入顺序）
$m["c"] = 3;
isset($m["a"]);                  // false 也返回 false！
array_key_exists("a", $m);       // 更严格：键存在（值可为 null）
unset($m["a"]);

$set = ["a" => true, "b" => true];       // 用键当集合
in_array("a", array_keys($set), true);
array_unique([1, 1, 2]);
array_flip($arr);                        // 值变键，快速做"集合存在性"
```

代码演示 `array` 当映射、`isset` 与 `array_key_exists` 的差别，以及 `array_flip` 做集合存在性判断。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的 `Hash` 保留插入顺序，键按 `eql?`/`hash` 比较（所以 `1` 与 `1.0` 是两个键）；`Set` 在标准库（Ruby 3.2 起自动加载），`Hash.new(obj)` 会让所有缺失键共享同一个对象。

```ruby
h = { a: 1, b: 2 }          # 保插入顺序
h[:c] = 3
h[:a]
h.fetch(:x, 0)              # 不存在给默认值；catch 版的 :x 会抛
h.fetch(:x) { 0 }
h.dig(:a, :b)
h.key?(:a)
h.merge(d: 4)

require "set"               # Ruby 3.2+ 默认已加载
s = Set.new([1, 2, 3])
s << 4
s | Set[5]                  # 并集；& 交集、- 差集、^ 对称差
```

代码演示 `Hash` 的增改查、`fetch`/`dig`/`merge` 与 `Set` 的集合运算。`Hash.new([])` 会让所有缺失键共享同一个数组（要用块形式 `Hash.new { |h,k| h[k] = [] }`）。

{{% /tab %}}

{{< /tabpane >}}

### 范围与迭代

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的范围是普通的枚举值（`0..5` 半开、`1..=5` 闭区间），迭代器是惰性的适配器链；`for x in v` 等价于 `into_iter()`，会移动 `v`。

```rust
for i in 0..5 { }              // 左闭右开
for i in 1..=5 { }             // 闭区间
(0..5).rev(); (0..10).step_by(2)
for (i, x) in v.iter().enumerate() { }

v.iter().map(|x| x * 2).filter(|x| x > &2).collect::<Vec<_>>();
```

代码演示 `0..5`/`1..=5`、`rev`/`step_by`、`enumerate` 与 `collect`。要点是：迭代器是惰性的（适配器不产生计算，直到 `collect`/`sum`/`for` 才真正执行）；

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 有 `0..<5`（半开）与 `1...5`（闭区间）两种 `Range`，步长用 `stride(from:to:by:)`；序列由 `Sequence`/`IteratorProtocol` 抽象，`Collection` 额外提供下标与多次遍历。

```swift
for i in 0..<5 { }             // 半开
for i in 1...5 { }             // 闭区间
for i in stride(from: 0, to: 10, by: 2) { }
for (i, c) in "abc".enumerated() { }

let doubled = (1...5).map { $0 * 2 }
let sum = (1...5).reduce(0, +)
Array(0..<5)                   // Range → Array 要显式转换
```

代码演示半开/闭区间、`stride`、`enumerated()` 与 `map`/`reduce`。要点是：`Range` 是独立类型（要 `Array(0..<5)` 才能当数组用），`Sequence` 允许单次遍历而 `Collection` 支持多次遍历与下标访问。

{{% /tab %}}

{{% tab header="Go" %}}

Go 只有 `for` 一种循环（`while` 写作 `for cond {}`）；Go 1.22 起可以 `range` 整数，Go 1.23 起可以 `range` 函数（`iter.Seq` 自定义迭代器）。

```go
for i := 0; i < 5; i++ { }
for i := range 5 { }            // Go 1.22+：range over int
for i, v := range slice { }
for k, v := range m { }
for i, r := range "héllo" { }   // i 是字节下标，r 是 rune

// Go 1.23+：range over func（自定义迭代器）
func seq(yield func(int) bool) { for i := 0; i < 5; i++ { if !yield(i) { return } } }
for v := range seq { }
```

代码演示三种 `for`、`range` 遍历切片/map/字符串，以及 Go 1.22 起可 `range` 整数。要点是：`range` 字符串给的是"字节下标 + rune"，Go 1.22 起循环变量每轮新建（闭包捕获不再是坑），Go 1.23 起还能 `range` 函数做自定义迭代器。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `range` 是惰性、不可变的序列对象，迭代协议是 `__iter__` + `__next__`；生成器表达式与 `itertools` 提供惰性管道，`zip` 默认在最短处停止。

```python
for i in range(5): ...          # 0..4，惰性、不可变
for i in range(10, 0, -2): ...
for i, x in enumerate(seq): ...
for a, b in zip(xs, ys): ...
for k, v in d.items(): ...

[x * 2 for x in xs]             # 列表推导
(x * 2 for x in xs)             # 生成器表达式（惰性）
from itertools import chain, islice, groupby, product
```

代码演示 `range`、`enumerate`/`zip`、字典 `.items()` 与列表推导/生成器表达式。要点是：`range` 惰性且 `in` 判断是 O(1)，`zip` 默认在最短处停止；

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 用 `1..5`、`until`、`downTo`、`step` 构造区间（一次性对象，可重复遍历）；`Sequence` 才是惰性管道，集合上的 `map`/`filter` 会立即生成中间列表。

```kotlin
for (i in 1..5) { }              // 闭区间
for (i in 1 until 5) { }         // 半开
for (i in 5 downTo 1 step 2) { }
for ((i, c) in "abc".withIndex()) { }
for (i in list.indices) { }

list.asSequence().map { it * 2 }.filter { it > 2 }.toList()   // 惰性
list.map { it * 2 }                                            // 立即返回新 List
```

代码演示 `1..5`、`until`、`downTo step`、`withIndex` 与集合和 `Sequence` 的差别。要点是：区间是普通对象、可重复遍历；

{{% /tab %}}

{{% tab header="Java" %}}

Java 有传统 `for`、增强 `for`（基于 `Iterable`）、`Iterator`/`ListIterator` 与惰性但只能消费一次的 `Stream`；Java 21 的 `SequencedCollection` 统一了首尾访问。

```java
for (int i = 0; i < 5; i++) { }
for (var x : list) { }
for (var e : map.entrySet()) { }

IntStream.range(0, 5).forEach(i -> { });        // 半开
IntStream.rangeClosed(1, 5).sum();
list.stream().filter(x -> x > 2).map(x -> x * 2).toList();   // Java 16+

Iterator<String> it = list.iterator();
while (it.hasNext()) { if (bad(it.next())) it.remove(); }
```

代码演示传统 `for`、增强 `for`、`IntStream.range` 与 `Iterator.remove()`。要点是：`Stream` 只能消费一次，遍历中安全删除元素要用 `Iterator.remove()`（直接 `list.remove` 会抛 `ConcurrentModificationException`）。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的范围 `for` 基于 `begin`/`end`，C++20 的 `std::ranges`/`views` 提供惰性管道；最大的坑是迭代器失效（`vector` 扩容或 `erase` 之后旧迭代器不能再用）。

```cpp
for (auto& x : v) { x *= 2; }        // 范围 for
for (const auto& x : v) { }

for (auto it = v.begin(); it != v.end(); ++it) { }

auto seq = std::views::iota(0, 5) | std::views::filter([](int x) { return x % 2 == 0; });
std::ranges::sort(v);                 // C++20 ranges 算法
```

代码演示范围 `for`、显式迭代器与 C++20 的 ranges/views。

{{% /tab %}}

{{% tab header="C" %}}

C 没有迭代器与范围类型，只有 `for` 和指针；想跳出多层循环只能用 `goto` 或标志变量。

```c
for (size_t i = 0; i < n; i++) { a[i]; }

for (int *p = a; p < a + n; p++) { *p; }

qsort(a, n, sizeof a[0], cmp);        // 回调式遍历
```

代码演示 `for` 下标遍历、指针遍历与 `qsort` 回调。指针越界、野指针、释放后使用全是未定义行为。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `1:5` 是具体的 `UnitRange` 对象（零分配、可重复遍历），`Iterators.filter/take/drop` 才是惰性；自定义迭代要实现 `Base.iterate`，返回 `nothing` 表示结束。

```julia
for i in 1:5 end                 # UnitRange
for i in 1:2:9 end               # StepRange
for (i, x) in enumerate(v) end
for (k, v) in pairs(d) end
for x in Iterators.filter(iseven, 1:10) end

range(0, 1, length = 11)         # 等分
eachindex(v)                     # 通用索引遍历
[i^2 for i in 1:5]               # 推导式
```

代码演示 `1:5`/`1:2:9`/`range`、`enumerate`/`pairs` 与 `Iterators.filter`。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `foreach` 基于 `IEnumerable<T>`/`IEnumerator<T>`（`yield return` 编译成状态机），LINQ 的 `Where`/`Select` 是惰性的；C# 8 起有 `Range`/`Index` 语法（`arr[1..3]`、`arr[^1]`）。

```csharp
for (int i = 0; i < 5; i++) { }
foreach (var x in list) { }
await foreach (var x in asyncSeq) { }        // IAsyncEnumerable<T>

IEnumerable<int> Squares() { for (int i = 0; i < 5; i++) yield return i * i; }
Enumerable.Range(0, 5).Where(x => x % 2 == 0).Select(x => x * 2);

var slice = arr[1..3];        // C# 8 范围语法
var last = arr[^1];           // 从尾部索引
```

代码演示 `for`/`foreach`、`yield return` 迭代器方法与 LINQ。`Span<T>` 之类的 ref struct 不能配 LINQ。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 用 `for (final x in iterable)` 遍历惰性的 `Iterable`，生成器有 `sync*`/`async*`；**没有内建 range 类型**，常用 `Iterable.generate(n)` 或普通 `for`。

```dart
for (var i = 0; i < 5; i++) { }
for (final x in list) { }
for (var i = 0; i < 5; i++) { }

Iterable.generate(5);                    // 0,1,2,3,4
list.map((x) => x * 2).where((x) => x > 2);   // 惰性 Iterable

Iterable<int> squares() sync* { for (var i = 0; i < 5; i++) yield i * i; }
Stream<int> ticks() async* { yield 1; }
```

代码演示三种 `for`、`Iterable.generate` 与 `sync*`/`async*` 生成器。要点是：Dart 没有内建 range 类型；`Iterable` 是惰性的（每次遍历重新计算），需要固定结果就先 `toList()`。

{{% /tab %}}

{{% tab header="R" %}}

R 的 `1:5` 是整数向量（闭区间、索引从 1 开始），`seq()`/`seq_len()`/`seq_along()` 生成序列；R 的哲学是向量化，循环应该尽量换成 `lapply`/`vapply`/`purrr::map`。

```r
1:5                       # integer 向量（闭区间）
seq(1, 10, by = 2)
seq_len(5)
seq_along(x)              # 比 1:length(x) 安全（长度为 0 时不产生 1:0）

for (x in v) { }          # 慢，且不会"返回"结果
sapply(v, function(x) x * 2)     # 向量化替代循环
lapply(v, function(x) x * 2)     # 返回 list
purrr::map_dbl(v, ~ .x * 2)
```

代码演示 `1:5`、`seq`/`seq_len`/`seq_along`、`sapply`/`lapply` 与 for 循环。要点是：`1:length(x)` 在 `x` 为空时会产生 `c(1, 0)`（要用 `seq_along`），循环里增长向量会反复复制整个对象（应预分配或用 map 家族）。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `for (xs) |x, i|` 同时给出元素与下标，`while (i < n) : (i += 1)` 是另一种写法，`inline for` 会在编译期展开；字符串切分用 `std.mem.splitScalar`/`tokenize`。

```zig
for (items) |x, i| { _ = x; _ = i; }        // 同时给元素与下标
for (0..5) |i| { _ = i; }

var i: usize = 0;
while (i < items.len) : (i += 1) { _ = items[i]; }

var it = std.mem.splitScalar(u8, "a,b,c", ',');
while (it.next()) |part| { _ = part; }

inline for (0..3) |i| { }        // 编译期展开
```

代码演示 `for (xs) |x, i|`、带 continuation 的 `while` 与 `std.mem.splitScalar`。要点是：`for` 直接同时给元素与下标（不需要 enumerate），`inline for` 在编译期展开；

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 有数值 `for`（闭区间、可带步长）与泛型 `for`（`pairs`/`ipairs`/自定义迭代函数）；`repeat ... until` 至少执行一次，`goto` 可以模拟 `continue`。

```lua
for i = 1, 10, 2 do end            -- 数值 for（闭区间）
for i = 10, 1, -1 do end
for k, v in pairs(t) do end        -- 全部键值
for i, v in ipairs(t) do end       -- 数组部分 1..n

local function range(n)            -- 自定义迭代器
  local i = 0
  return function() i = i + 1; if i <= n then return i end end
end
for i in range(5) do end

repeat ... until cond              -- 至少执行一次
for i = 1, 10 do if x then break end end
```

要点是：泛型 for 的本质是"迭代函数 + 状态 + 初值"；`ipairs` 只走 1..n 且遇到 nil 就停，`pairs` 走全部键但顺序未定义。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的 `for..of` 走迭代协议（`Iterable<T>`/`Iterator<T>`/`Generator<T>`），`for..in` 遍历键名；没有内建 range，常用 `[...Array(n).keys()]` 或生成器。

```ts
for (let i = 0; i < 5; i++) { }
for (const x of list) { }          // 可迭代对象的值
for (const k in obj) { }           // ⚠️ 键名（含原型链）

function* squares(n: number): Generator<number> { for (let i = 0; i < n; i++) yield i * i; }
[...squares(5)];

for await (const x of asyncIterable) { }
```

代码演示 `for..of`/`for..in`、生成器函数与 `for await`。要点是：`for..in` 遍历的是键名（并且会走原型链），遍历可迭代对象要用 `for..of`；

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `for..of` 遍历可迭代对象（字符串按码点、`Map`/`Set` 原生支持），`for..in` 遍历可枚举属性并会走原型链；自定义迭代靠 `Symbol.iterator`。

```js
for (let i = 0; i < 5; i++) { }
for (const x of [1, 2, 3]) { }
for (const [i, x] of arr.entries()) { }
for (const k in obj) { if (Object.hasOwn(obj, k)) { } }

function* gen() { yield 1; yield 2; }
const it = gen();
it.next();                    // { value: 1, done: false }

const obj = { *[Symbol.iterator]() { yield 1; } };   // 自定义迭代协议
```

要点是：`for..in` 会枚举原型链上的属性（要用 `Object.hasOwn` 过滤），`forEach` 不能 `break`，而 `for..of` 遍历字符串时按码点而不是码元。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `foreach` 支持键值遍历与引用遍历（引用遍历后必须 `unset($v)`）；`range()` 会一次性分配整个数组，惰性遍历要用 `Generator`（`yield`/`yield from`）。

```php
for ($i = 0; $i < 5; $i++) { }
foreach ($arr as $k => $v) { }
foreach ($arr as &$v) { $v *= 2; }   // 引用修改
unset($v);                            // ⚠️ 循环后必须 unset 引用

for ($i = 1; $i <= 5; $i++) { }
foreach (range(1, 5) as $i) { }       // range() 是数组，不是惰性

function gen() { yield 1; yield from [2, 3]; }
foreach (gen() as $v) { }             // Generator 是惰性的
```

代码演示 `for`/`foreach`、引用遍历与 `Generator`。要点是：引用遍历结束后必须 `unset($v)`，否则后续写 `$v` 会改到数组最后一个元素；

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的遍历核心是 `each`（不传块会返回 `Enumerator`，可以继续链式调用）；`Range` 支持 `each`/`cover?`，无限序列要配 `lazy` 或 `first(n)`。

```ruby
(1..5).each { |i| }
(1...5).each { |i| }          # 三个点：排除右端
1.step(10, 2) { |i| }
5.times { |i| }
arr.each_with_index { |x, i| }
arr.each_slice(2) { |pair| }

enum = arr.each                # 不传块 → Enumerator
enum.with_index.first(3)
(1..Float::INFINITY).lazy.map { |x| x * 2 }.first(5)   # 惰性无限序列
```

代码演示 `each`、`times`/`step`、`each_slice` 与 `lazy` 无限序列。无限序列必须配 `lazy` 或 `first(n)`，而 `for ... in` 会让循环变量泄漏到外层作用域。

{{% /tab %}}

{{< /tabpane >}}

## 自定义类型

自定义类型由三件事组成：**给数据起名字**（结构体/类）、**把行为绑上去**（方法/接口）、**限制谁能进来**（可见性/泛型约束）。不同语言的"零件"数量差别极大，所以下面拆成 7 个子类型，每个子类型一张"有没有 / 叫什么"总表 + 18 个语言标签页；某门语言没有这个构造时，会直接写"没有"以及常规替代做法。

### 结构体与记录

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `struct Point { x: i32, y: i32 }` | 值类型；另有元组结构体、单元结构体 |
| Swift | ✓ | `struct Point { var x: Int }` | 值类型；可遵循协议，但不能被继承 |
| Go | ✓ | `type Point struct { X, Y int }` | 值类型；用嵌入（embedding）替代继承 |
| Python | ✓（记录） | `@dataclass class P:` / `NamedTuple` | 由类实现；`frozen=True` 得到不可变记录 |
| Kotlin | ✓（记录） | `data class Point(val x: Int)` | 自动 `equals`/`copy`/解构 |
| Java | ✓（记录） | `record Point(int x, int y) { }` | Java 16+；不可变、值相等 |
| C++ | ✓ | `struct Point { int x, y; };` | 聚合初始化；与 `class` 只差默认可见性 |
| C | ✓ | `struct point { int x, y; };` | 只有数据没有方法；赋值是逐成员拷贝 |
| Julia | ✓ | `struct Point; x::Int; end` | 默认不可变；字段类型必须声明 |
| C# | ✓ | `struct V { }` / `record struct P(int X)` | 值类型；`record struct` 额外有值相等与解构 |
| Dart | ✓（记录） | `var p = (x: 1, y: 2);` | Dart 3.0+ 的 record：不可变、结构相等；**没有 struct** |
| R | ✗ | `list(x = 1, y = 2)` + `class` 属性 | 没有结构体类型，用 list/S3 对象代替 |
| Zig | ✓ | `const Point = struct { x: i32 };` | 值类型；可以在 struct 里定义方法 |
| Lua | ✗ | `local p = { x = 1 }` | 没有结构体，表（table）就是记录 |
| TypeScript | ✓（编译期） | `interface Point { x: number }` | 只存在于编译期，运行时是普通对象 |
| JavaScript | ✓（对象字面量） | `const p = { x: 1 }` | 没有类型声明，对象字面量即记录 |
| PHP | ✗ | `class Point {}` 或数组 | 没有结构体，用类或关联数组代替 |
| Ruby | ✓ | `Point = Data.define(:x, :y)` | Ruby 3.2+ 的不可变值对象；`Struct` 是可变版本 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 用 `struct` 定义结构体，它是**值类型**，共有三种形态：具名结构体、元组结构体（newtype）与单元结构体；字段默认私有，行为写在 `impl` 里。

```rust
struct Point { x: i32, y: i32 }     // 具名
struct Meters(f64);                  // 元组结构体（newtype）
struct Marker;                       // 单元结构体（零大小）

#[derive(Debug, Clone, PartialEq)]   // 常用派生
struct Id(u64);

let p = Point { x: 1, y: 2 };
let Point { x, y } = p;              // 解构
```

代码演示具名结构体、元组结构体（newtype）、单元结构体、`#[derive]` 与解构。要点是：结构体是值类型、字段默认私有、没有继承；newtype 用来做零开销的强类型包装，`#[derive]` 自动实现 `Debug`/`Clone`/`PartialEq` 这些常用 trait。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `struct` 是值类型，适合"纯数据 + 行为"的载体：赋值与传参都会复制（大容器有写时复制优化），但不能被继承。

```swift
struct Point {                       // 值类型
    var x: Int
    var y: Int
}
let p = Point(x: 1, y: 2)            // 逐成员初始化器（自动生成）
var q = p; q.x = 9                   // 复制语义：p 不受影响

struct Meters: Equatable { let v: Double }   // 可遵循协议
```

代码演示结构体的逐成员初始化、值语义（赋值后互不影响）与协议遵循。要点是：赋值和传参都会产生独立副本（大容器有写时复制优化），初始化器自动生成；结构体不能被继承，要继承只能用 class。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `struct` 是字段的集合，属于值类型；没有继承，复用靠**嵌入**（把另一个类型放进字段位置，其字段与方法会被提升）。

```go
type Point struct { X, Y int }       // 字段首字母大写才导出

p := Point{X: 1, Y: 2}
p.X = 9

type Circle struct {
    Point                            // 嵌入：字段与方法被"提升"
    R float64
}
c := Circle{Point: Point{X: 1}, R: 2}
c.X                                  // 直接访问嵌入字段
```

代码演示结构体字面量、字段导出规则与嵌入字段的"提升"访问。要点是：字段首字母大写才能导出到包外，嵌入是组合而不是继承（`c.X` 能直接访问嵌入字段），Go 没有构造函数（`NewXxx` 只是约定）。

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有编译期的结构体类型（`struct` 模块是二进制打包、`ctypes.Structure` 是 C 互操作，都不是普通记录），记录用 `@dataclass` 表达：自动生成 `__init__`/`__eq__`/`__repr__`，`frozen=True` 得到不可变版本；`NamedTuple` 是元组式的轻量替代。

```python
from dataclasses import dataclass, field
from typing import NamedTuple

@dataclass(frozen=True)              # 不可变记录：自动 __init__/__eq__/__repr__
class Point:
    x: int
    y: int
    tags: list[str] = field(default_factory=list)   # 可变默认值必须用 factory

class P(NamedTuple):                 # 元组式记录：可解包、可当字典键
    x: int
    y: int

p = Point(1, 2)
```

代码演示 `@dataclass(frozen=True)`、`field(default_factory=...)` 与 `NamedTuple`。要点是：`frozen=True` 才有不可变与 `__hash__`，可变默认值必须用 `default_factory`（写成 `= []` 会让所有实例共享同一个列表），要当元组用就选 `NamedTuple`。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 用 `data class` 作为记录：自动生成 `equals`/`hashCode`/`copy`/`toString` 与解构；需要"包装一个已有类型又想要类型安全"时用 `@JvmInline value class`。

```kotlin
data class Point(val x: Int, val y: Int)     // 记录：自动 equals/hashCode/copy/解构
val p = Point(1, 2)
val q = p.copy(x = 9)                         // 复制并改字段
val (x, y) = p                                // 解构

@JvmInline value class Meters(val v: Double)  // 值类：多数场合零装箱
```

要点是：`data class` 的 `equals`/`hashCode` 只按主构造参数计算，`copy` 是浅拷贝；`value class` 在多数场景零装箱，但可空、泛型、数组位置可能装箱。

{{% /tab %}}

{{% tab header="Java" %}}

Java 16 起用 `record` 表达不可变记录：字段是 final、自动生成访问器/`equals`/`hashCode`/`toString`，还可以写紧凑构造函数做参数校验。

```java
record Point(int x, int y) {          // Java 16+
    Point {                           // 紧凑构造函数（可校验参数）
        if (x < 0) throw new IllegalArgumentException();
    }
}

Point p = new Point(1, 2);
p.x();                                // 访问器：x() 而不是 getX()
```

代码演示 `record` 的紧凑构造函数与访问器（是 `x()` 不是 `getX()`）。要点是：record 字段 final、按值相等、隐式 final 不能继承，但可以实现接口、可以加方法；只读的小数据结构一律优先用它。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的 `struct` 是最基础的聚合类型，和 `class` 只差默认访问权限；它同时是 C 兼容布局与"值语义数据载体"的默认选择。

```cpp
struct Point { int x = 0, y = 0; };   // 聚合类型：可以逐个初始化
Point p{1, 2};
auto [x, y] = p;                       // C++17 结构化绑定

struct Meters { double v; };           // 强类型包装（newtype 模式）
```

代码演示聚合初始化、C++17 结构化绑定与强类型包装 struct。带指针成员的 struct 要自己定义拷贝/移动/析构（三/五法则）。

{{% /tab %}}

{{% tab header="C" %}}

C 的 `struct` 是"只有数据"的聚合类型：不能有方法、没有可见性，赋值时逐成员复制（含内嵌数组），含指针成员时只做浅拷贝。

```c
struct point { int x, y; };            // 只有数据
struct point p = { .x = 1, .y = 2 };   // 指定初始化器（C99）
struct point q = p;                    // 逐成员拷贝（含数组）

typedef struct point point;            // 省略每次写 struct
```

代码演示指定初始化器（C99）、逐成员拷贝与 `typedef` 省去 `struct` 关键字。要点是：结构体只有数据没有方法，赋值是逐成员拷贝（包含内嵌数组），含指针时只是浅拷贝；结构体大小受对齐影响，可能大于字段之和。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用 `struct`（默认不可变）与 `mutable struct` 定义复合类型，字段类型必须显式声明；这既约束了语义，也让编译器能生成高效的内存布局。

```julia
struct Point                # 不可变（Julia 的默认）
    x::Int
    y::Int
end

mutable struct Node         # 需要改字段才用 mutable
    next::Union{Node, Nothing}
end

p = Point(1, 2)             # 位置参数构造
```

代码演示 `struct`（不可变）与 `mutable struct` 的差别以及位置参数构造。要点是：字段类型必须显式声明（这让编译器能做类型化的内存布局），不可变结构体在并发下天然安全；确实要改字段才用 `mutable`。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `struct` 是值类型（赋值复制），`record struct`/`record` 额外提供值相等、`with` 表达式与解构；引用语义的对象用 `class`。

```csharp
public struct Vector { public double X, Y; }          // 值类型结构体
public readonly struct Point { public readonly int X; }

public record Point2(int X, int Y);                   // 引用类型记录（值相等）
public readonly record struct Point3(int X, int Y);   // 值类型记录（C# 10+）

var p = new Point3(1, 2);
var q = p with { X = 9 };                             // with：复制并改
```

代码演示 `struct`、`readonly struct`、`record`、`record struct` 与 `with` 表达式。要点是：`struct` 是值语义，`record struct` 在值语义之外还有值相等，`record`（引用类型）也按值相等；结构体不能继承。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 没有 struct：轻量记录用 Dart 3 的 record（不可变、结构相等），需要方法与可变状态就用 class。

```dart
var p = (1, 'a');                  // 位置记录
var q = (x: 1, y: 2);              // 命名记录
print(q.x);
var (a, b) = p;                    // 解构

class Point {                      // 普通类承担"对象"角色
  final double x, y;
  const Point(this.x, this.y);
}
```

代码演示 record 的位置/命名形式、解构与 class 的 `const` 构造。要点是：Dart 没有 struct，record 是不可变、值语义的轻量记录；需要方法与可变状态就用 class，而 class 想要值相等必须自己重写 `==`/`hashCode`。

{{% /tab %}}

{{% tab header="R" %}}

R 没有结构体类型：记录习惯用命名 `list` 加 `class` 属性（S3 对象），表格数据用 `data.frame` 的每一行，需要"带方法的对象"用 `R6::R6Class`。

```r
p <- list(x = 1, y = 2)                       # 命名 list：最像"记录"
class(p) <- "point"                           # 加上 class 变成 S3 对象

df <- data.frame(x = 1, y = 2)                 # 表格：每行是一条记录
df[1, ]                                        # 取一行（仍然返回 data.frame）

Point <- R6::R6Class("Point", public = list(   # 需要"结构体 + 方法"就用 R6
  x = NULL, y = NULL,
  initialize = function(x, y) { self$x <- x; self$y <- y }
))
```

代码演示命名 list + `class` 属性、`data.frame` 的一行与 `R6::R6Class`。要点是：S3 的"记录"就是 list 加 class 属性，没有任何字段类型约束；表格数据用 `data.frame`，需要引用语义对象才上 R6。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `struct` 是值类型，可以在里面定义方法（第一个参数是 `self`），还能声明 `packed`/`extern` 来指定位精确布局或 C ABI 布局。

```zig
const Point = struct {            // 值类型
    x: i32,
    y: i32,

    pub fn sum(self: Point) i32 { return self.x + self.y; }   // 方法：第一个参数是 self
};

const p = Point{ .x = 1, .y = 2 };
const q = p;                       // 值拷贝
const Packed = packed struct { a: u1, b: u7 };   // 紧凑布局
const Ext = extern struct { a: i32 };            // C ABI 布局
```

代码演示 struct 定义 + 方法、`packed`/`extern` 布局与值拷贝。要点是：方法就是"第一个参数是 `self`"的函数；`packed`/`extern` 用于位精确或 C ABI 场景，普通 struct 的字段顺序可能被编译器重排。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有结构体：表（table）就是记录，字段随时可增删，读不存在的字段得到 `nil` 而不是报错。

```lua
local p = { x = 1, y = 2 }        -- 记录
p.z = 3                            -- 随时加字段
print(p.x, p["x"])                 -- 两种取值方式等价

local Point = {}
Point.__index = Point
function Point.new(x, y) return setmetatable({ x = x, y = y }, Point) end
Point.origin = { x = 0, y = 0 }
```

代码演示用表当记录、动态添加字段与元表 `__index`。要点是：表是唯一的复合结构，字段随时可增删，读不存在的字段得到 `nil`——拼错字段名不会有任何报错。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的"结构体/记录"是 `interface` 或 `type` 声明的对象形状，只存在于编译期；编译后是完全消失的普通对象。

```ts
interface Point { x: number; y: number }       // 编译期结构
type PointT = { x: number; y: number };         // 等价别名写法
const p: Point = { x: 1, y: 2 };

interface Point3 extends Point { z: number }    // 组合/扩展
const p3: Point3 = { x: 1, y: 2, z: 3 };

type ReadonlyPoint = Readonly<Point>;           // 只读视图（编译期）
```

代码演示 `interface`/`type` 声明对象形状、接口继承与 `Readonly<T>`。要点是：这些声明编译后完全消失，运行时就是普通对象；字面量赋值会触发超额属性检查，但变量赋值只看结构兼容。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 用对象字面量表示记录，没有类型声明；需要只读就用 `Object.freeze`（浅冻结）或 `structuredClone` 配合约束。

```js
const p = { x: 1, y: 2 };             // 对象字面量就是记录
const frozen = Object.freeze({ x: 1 });// 浅冻结，防止加/改顶层字段

const { x, y } = p;                    // 解构
const q = { ...p, y: 9 };              // 展开复制并改字段

class Point { constructor(x) { this.x = x; } }   // 需要方法就用 class
```

代码演示对象字面量、`Object.freeze` 与 class。要点是：对象没有字段约束，`Object.freeze` 只是浅冻结；把对象当记录用要注意原型链（`"toString" in p` 恒为 true，判断自有属性用 `Object.hasOwn`）。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有结构体：要类型和方法就用类（构造函数属性提升 + `readonly`），要快速临时数据用关联数组。

```php
class Point {                          // 1) 类：有类型、有方法
    public function __construct(
        public readonly int $x = 0,
        public readonly int $y = 0,
    ) {}
}

$p = ['x' => 1, 'y' => 2];             // 2) 关联数组：快速、但无类型

readonly class Vec { }                 // PHP 8.2+：整个类只读
```

代码演示构造函数属性提升 + `readonly`、关联数组与 `readonly class`。要点是：需要类型约束、方法、IDE 补全就用类，临时数据用关联数组；PHP 8.4 起还能用属性钩子写计算属性与惰性初始化。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用 `Struct`（可变）与 `Data.define`（Ruby 3.2+，不可变）定义记录，两者都会自动生成访问器、相等性与解构支持。

```ruby
Point = Data.define(:x, :y)          # Ruby 3.2+：不可变值对象、结构相等
p = Point.new(x: 1, y: 2)
p.x
p.with(x: 9)                          # 复制并改（3.2+）

Record = Struct.new(:x, :y)           # 可变的结构体
r = Record.new(1, 2)
r.x = 9
```

代码演示 `Data.define`（不可变、`with`）与 `Struct`（可变）。要点是：两者都会自动生成访问器、相等语义与解构支持；`Data` 不可变、`Struct` 可改，普通 class 也能当记录但没有自动相等性。

{{% /tab %}}

{{< /tabpane >}}
### 类

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✗ | `struct` + `impl` + `trait` | 没有类、没有继承；行为靠 trait 与组合 |
| Swift | ✓ | `class Node { var next: Node? }` | 引用类型、ARC 管理、可继承、有 `deinit` |
| Go | ✗ | `struct` + 方法 + 嵌入 | 没有类、没有继承；方法挂在类型上 |
| Python | ✓ | `class Point:` | 多继承 + MRO；属性可运行时增删 |
| Kotlin | ✓ | `class A`（默认 final） | 继承要 `open`；有 `data`/`sealed`/`value` 等变体 |
| Java | ✓ | `class Node { }` | 单继承 + 多接口；有内部类/匿名类 |
| C++ | ✓ | `class Node { public: ... };` | 多继承、虚函数、RAII、访问控制齐全 |
| C | ✗ | 手写函数指针表（vtable） | 没有类、方法、继承 |
| Julia | ✗ | 多分派 + 抽象类型 | 方法不绑定在类型上，按参数类型选择 |
| C# | ✓ | `class Node { }` | 单继承、`sealed`、`partial`、可空引用类型 |
| Dart | ✓ | `class Point { }` | 单继承 + mixin；3.0 起有类修饰符 |
| R | ✓ | S3 / S4 / R6 三套 | 统计代码用 S3；要可变对象用 R6 |
| Zig | ✗ | `struct` + 方法 + 手写 vtable | 没有类、没有继承 |
| Lua | ✗（可模拟） | `table` + metatable | 没有类语法，用元表模拟对象与继承 |
| TypeScript | ✓ | `class Node { }` | 会生成真实 JS 类；可实现 interface |
| JavaScript | ✓ | `class Node { #secret = 1; }` | 原型继承；`#` 私有字段（ES2022） |
| PHP | ✓ | `class Point { }` | 单继承；trait 复用；8.4 起有属性钩子 |
| Ruby | ✓ | `class Point; end` | 开放类（可随时加方法）、单继承、module mixin |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust **没有类**：它用 `struct` 装数据、用 `impl` 挂行为、用 `trait` 表达接口，三件套组合出其他语言的"类 + 继承"能做的事。

```rust
struct Counter { n: u32 }

impl Counter {
    fn new() -> Self { Self { n: 0 } }
    fn inc(&mut self) { self.n += 1; }
}

trait Reset { fn reset(&mut self); }
impl Reset for Counter { fn reset(&mut self) { self.n = 0; } }
```

代码演示"`struct` 装数据 + `impl` 挂行为 + `trait` 定接口"这三件套。要点是：Rust 没有继承也没有虚表继承链，多态要靠 `dyn Trait`（动态派发）或泛型（静态单态化）；共享可变状态必须显式写成 `Rc<RefCell<_>>` 或 `Arc<Mutex<_>>`，语言不会替你决定。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `class` 是引用类型，由 ARC 管理生命周期，支持继承、重写与 `deinit`；需要值语义时应该优先用 struct。

```swift
class Node {
    var next: Node?
    init(next: Node? = nil) { self.next = next }
    deinit { }                                   // 只有 class 有析构
    func describe() -> String { "node" }
}

final class Leaf: Node {                          // 继承；final 禁止再继承
    override func describe() -> String { "leaf" }
}

weak var parent: Node?                            // 弱引用，打破循环引用
```

代码演示类定义、`init`/`deinit`、继承与 `override`，以及用 `weak` 打破循环引用。能用 struct 表达的就别用 class。

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有类**：方法可以挂在任何具名类型上，复用靠嵌入（组合），多态靠接口隐式实现。

```go
type Animal struct{ Name string }
func (a Animal) Speak() string { return "..." }

type Dog struct {
    Animal                    // 嵌入：字段与方法被提升
    Breed string
}
func (d Dog) Speak() string { return "woof" }   // 覆盖（不是 override）

type Speaker interface{ Speak() string }        // 多态靠接口
```

代码演示方法挂在类型上、通过嵌入复用字段与方法，以及用接口获得多态。要点是：Go 没有类与继承，"嵌入"是组合；方法集决定接口能否被满足，值接收者与指针接收者要前后一致。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的类是对象的模板：支持多继承与 MRO、属性和方法可以在运行时增删，几乎所有自定义行为都通过类表达。

```python
class Point:
    count = 0                        # 类属性（共享）
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

class Point3(Point):                 # 继承（可以多继承）
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z
```

代码演示类属性与实例属性、`__init__`/`__repr__` 与继承 + `super()`。要点是：多继承按 MRO 解析，属性可以随时增删；方法默认都是"虚方法"，`super()` 是协作式调用——多继承场景下必须用它。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的类默认是 `final` 的，要允许继承必须声明 `open`/`abstract`；主构造函数写在类头，属性可以直接写在参数列表里。

```kotlin
class Node(var next: Node? = null)          // 默认 final

open class Base(val id: Int) {              // 要 open 才能被继承
    open fun describe() = "base"
}
class Derived(id: Int) : Base(id) {
    override fun describe() = "derived"
}

abstract class Shape { abstract fun area(): Double }
data class Point(val x: Int, val y: Int)
```

代码演示默认 final 的类、`open`/`override`、`abstract class` 与 `data class`。`==` 调用的是 `equals`（与 Java 的 `==` 完全不同），一个类可以实现多个接口但只能继承一个类。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的类是引用类型，单继承 + 多接口；抽象类可以有状态，内部类/匿名类在老代码里很常见。

```java
public class Node {
    private int value;
    Node next;

    public Node(int value) { this.value = value; }
    @Override public String toString() { return "Node(" + value + ")"; }
}

public final class Leaf extends Node { }        // 单继承；final 禁止继承
public abstract class Shape { public abstract double area(); }
```

代码演示字段/构造/重写、`final class` 与 `abstract class`。要点是：单继承 + 多接口，抽象类可以有状态；Java 25 起构造函数体更灵活（`super(...)` 之前可以先写校验）；新代码用 record/lambda 取代大量样板。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的类支持多继承、虚函数、访问控制与 RAII（构造/析构），但没有垃圾回收；多态必须通过指针或引用。

```cpp
class Node {
public:
    explicit Node(int v) : value_{v} {}
    virtual ~Node() = default;                   // 多态基类必须有虚析构
    virtual std::string name() const { return "node"; }
private:
    int value_;
};

class Leaf final : public Node {                 // 继承；final 禁止再继承
public:
    std::string name() const override { return "leaf"; }
};
```

代码演示构造函数、虚析构、`virtual`/`override` 与 `final`。要点是：多态必须通过指针或引用（按值传递会对象切片），多态基类必须有虚析构；拷贝/移动语义要么显式定义，要么 `= delete` 明确禁用。

{{% /tab %}}

{{% tab header="C" %}}

C **没有类**：要"面向对象"只能手写结构体 + 函数指针表（vtable），并把 `this` 作为第一个参数传递。

```c
struct shape_vtable {
    double (*area)(const struct shape *);
    void   (*destroy)(struct shape *);
};

struct shape {
    const struct shape_vtable *vtable;   /* 模拟虚表 */
    void *data;
};

double shape_area(const struct shape *s) { return s->vtable->area(s); }
```

代码演示"结构体 + 函数指针表"模拟虚表，并把 `this` 当第一个参数传递。要点是：没有方法、继承与可见性，生命周期靠 `malloc`/`free`，这正是内核等 C 代码里的"对象"写法。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia **没有类**：数据是 `struct`，行为是按参数类型定义的方法，类型层级用抽象类型表达——也就是"多分派"替代了"继承 + 虚函数"。

```julia
abstract type Animal end            # 抽象类型：只能当分派节点

struct Dog <: Animal
    name::String
end

speak(a::Animal) = "..."
speak(d::Dog) = "woof"              # 更具体的方法自动优先
```

代码演示抽象类型、具体子类型与按参数类型选择方法（多分派）。要点是：方法不属于类型，而属于"函数 + 参数类型组合"，所以没有 `virtual`/`override`；`methods(f)` 能列出某个函数的全部实现。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的类是引用类型，单继承 + 多接口，惯例是用属性（`get`/`set`/`init`）而不是公共字段，资源释放用 `IDisposable` + `using`。

```csharp
public class Node {
    public int Value { get; init; }     // 属性（init 只能初始化时赋值）
    public Node? Next;
    public virtual string Name() => "node";
}

public sealed class Leaf : Node {        // sealed：禁止继承
    public override string Name() => "leaf";
}

public abstract class Shape { public abstract double Area(); }
```

代码演示属性（`get; init;`）、`virtual`/`override`、`sealed`/`partial` 与抽象类。要点是：单继承 + 多接口，公共成员用属性而不是字段；资源释放靠 `IDisposable` + `using`，而不是析构函数。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 只有类（没有结构体/值类型）：3.0 起的类修饰符（`base`/`final`/`interface`/`sealed`/`mixin`）决定谁能继承、谁能实现。

```dart
class Point {
  final double x, y;
  const Point(this.x, this.y);
}

sealed class Shape { }                   // Dart 3.0：密封，可配合 switch 穷尽
final class Circle extends Shape { }     // 类修饰符：base/final/interface/sealed/mixin

mixin Drawable { void draw() {} }        // mixin：横向复用
class Art with Drawable { }
```

代码演示类、`const` 构造、`==`/`hashCode` 重写与类修饰符（`sealed`/`final`/`mixin`）。要点是：Dart 只有类，修饰符决定谁能继承/实现；重写 `==` 时必须同时重写 `hashCode`。

{{% /tab %}}

{{% tab header="R" %}}

R 有三套面向对象系统：S3（`class` 属性 + `UseMethod` 分派，最常用）、S4（`setClass`/`setMethod`，正式类）、R6（引用语义的可变对象）。

```r
# S3：class 属性 + 泛型函数分派（最常用）
p <- structure(list(x = 1, y = 2), class = "point")
print.point <- function(x, ...) cat("point\n")
area <- function(x, ...) UseMethod("area")
area.point <- function(x, ...) x$x * x$y

# S4：正式类（有字段校验与继承）
setClass("Point", representation(x = "numeric", y = "numeric"))

# R6：引用语义的"真类"
Counter <- R6::R6Class("Counter",
  public = list(count = 0, inc = function() self$count <- self$count + 1))
```

要点是：S3 最轻量（靠命名约定），S4 有正式定义与继承，只有 R6/RC 提供引用语义。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig **没有类**：方法是"第一个参数是 `self`"的函数，多态要么用 `anytype` 编译期泛型，要么手写 vtable 结构体。

```zig
const Counter = struct {                 // 数据 + 方法
    n: u32 = 0,
    pub fn inc(self: *Counter) void { self.n += 1; }
};

const Drawable = struct {                // "接口"：数据指针 + 函数指针
    ptr: *anyopaque,
    drawFn: *const fn (*anyopaque) void,
    pub fn draw(self: Drawable) void { self.drawFn(self.ptr); }
};
```

代码演示 struct + 方法（`self` 显式）以及手写 vtable 做运行时多态。要点是：Zig 没有类与继承；资源靠 `defer` 手动配对释放。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有类语法**：对象就是 table，方法是表里的函数，`:` 是 `obj.m(obj, ...)` 的语法糖，继承靠元表 `__index` 链。

```lua
local Point = {}
Point.__index = Point                    -- 实例查不到的字段去 Point 里找

function Point.new(x, y)
  return setmetatable({ x = x, y = y }, Point)
end
function Point:len() return self.x + self.y end   -- 冒号 = 自动传 self

local Base = {}; Base.__index = Base     -- "继承" = 元表链
local Derived = setmetatable({}, { __index = Base })
```

代码演示用 `metatable` + `__index` 实现对象与继承链，以及冒号方法调用。要点是：`:` 只是 `obj.m(obj, ...)` 的语法糖，继承、私有、"父类调用"全靠约定，语言不做任何检查。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的 `class` 是少数会生成真实运行时代码的类型声明，支持 `implements`、访问修饰符与抽象类；`private` 编译后被擦除，真私有要用 `#field`。

```ts
class Node {
  #secret = 1;                 // 真私有（ES2022）
  private value: number;       // 仅编译期私有
  readonly id: string;
  static count = 0;

  constructor(id: string, value: number) { this.id = id; this.value = value; }
  get doubled() { return this.value * 2; }
}

class Leaf extends Node implements Drawable { }
abstract class Shape { abstract area(): number; }
```

代码演示 `class` 的字段/构造/getter/静态成员、`extends` 与 `implements`、抽象类。要点是：class 会生成真实运行时代码；参数属性简写能省掉字段声明。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `class` 是原型继承的语法糖（方法在 `prototype` 上），`#field` 提供真正的私有字段；`this` 由调用方式决定。

```js
class Node {
  #secret = 1;                       // 私有字段（ES2022）
  static count = 0;
  constructor(value) { this.value = value; }
  get doubled() { return this.value * 2; }
}

class Leaf extends Node { constructor(v) { super(v); } }
Object.getPrototypeOf(Leaf.prototype) === Node.prototype;   // 原型链
```

代码演示 class、私有字段 `#`、静态成员与原型链的关系。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的类支持单继承、多接口与 trait 复用；PHP 8.4 起还能用属性钩子写计算属性，8.2 起支持 `readonly` 类。

```php
class Point {
    public function __construct(
        public readonly int $x = 0,     // 属性提升 + 只读
        public readonly int $y = 0,
    ) {}
    public function length(): float { return sqrt($this->x ** 2 + $this->y ** 2); }
}

readonly class Vec { }                  // PHP 8.2+：整个类只读
final class Sealed { }
abstract class Shape { abstract public function area(): float; }
class Circle extends Shape { use Loggable; }
```

代码演示构造函数属性提升 + `readonly`、`readonly class`、抽象类与 `trait`。要点是：单继承 + 多接口 + trait 复用（trait 不是类型），PHP 8.4 起有属性钩子；属性必须显式声明，动态属性已弃用。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的类是**开放**的（随时可以重新打开加方法），单继承，横向复用靠 `module` + `include`，一切访问控制都只是约定。

```ruby
class Point
  attr_reader :x, :y
  def initialize(x, y) = (@x, @y = x, y)     # 3.0+ 无尽方法
end

class Point3 < Point                          # 单继承
  def initialize(x, y, z)
    super(x, y)
    @z = z
  end
end

module Drawable
  def draw = "circle"
end
class Point3; include Drawable; end           # mixin 代替接口
```

代码演示 `attr_reader`、无尽方法、继承与 `module` include。要点是：类是**开放**的（任何地方都能加方法），单继承、横向复用靠 module；访问控制只是约定，`send` 依然能调用"私有"方法。

{{% /tab %}}

{{< /tabpane >}}
### 枚举

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `enum Direction { North, South }` | 普通枚举与带数据的 ADT 用的是同一个 `enum` |
| Swift | ✓ | `enum Direction { case north, south }` | 可以只有 case，也可以带原始值或关联值 |
| Go | ✗ | `const ( A = iota; B )` | 没有 enum 类型；用常量 + `iota` 模拟，无类型安全 |
| Python | ✓ | `class Color(Enum): RED = auto()` | 成员不是整数；另有 `IntEnum`/`StrEnum`/`Flag` |
| Kotlin | ✓ | `enum class Direction { NORTH, SOUTH }` | 可带构造参数、属性、方法，可实现接口 |
| Java | ✓ | `enum Direction { NORTH, SOUTH }` | 本质是类：有 `values()`/`valueOf()`，可有字段与方法 |
| C++ | ✓ | `enum class Color { Red, Green };` | C++11 强类型枚举；可指定底层类型 |
| C | ✓ | `enum color { RED, GREEN };` | 本质是 `int` 常量集合，不做取值检查 |
| Julia | ✓ | `@enum Color RED GREEN` | 本质是不可变原始类型；可指定底层类型 |
| C# | ✓ | `enum Direction { North, South }` | 底层整数；`[Flags]` 做位标志 |
| Dart | ✓ | `enum Direction { north, south }` | 2.17+ 增强枚举：可以有字段、方法、构造参数 |
| R | ✗ | `factor(c("a", "b"))` | 没有枚举；`factor` 是带水平的分类变量 |
| Zig | ✓ | `const Color = enum { red, green };` | 可指定整数 tag 类型，也可声明 non-exhaustive |
| Lua | ✗ | `local D = { NORTH = "north" }` | 没有枚举；用常量表或字符串约定 |
| TypeScript | ✓ | `enum Direction { North, South }` | 会生成运行时代码；很多团队改用联合字面量 |
| JavaScript | ✗ | `Object.freeze({ North: "north" })` | 没有 enum；用冻结对象或字符串常量 |
| PHP | ✓ | `enum Direction { case North; }` | 8.1+；纯枚举与 backed enum（string/int），可实现接口 |
| Ruby | ✗ | `Color = %w[red green].freeze` | 没有枚举；用常量、Symbol 或冻结数组 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `enum` 是"带数据的和类型"：每个变体可以有不同字段，`match` 会强制穷尽；普通的"常量枚举"也只是它的一个特例。

```rust
enum Direction { North, South }              // 只能取这几个值
let d = Direction::North;

enum Shape {                                  // 带数据（ADT）
    Circle(f64),
    Rect { w: f64, h: f64 },
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum Level { Low, Mid, High }

let n = Level::Mid as u8;                     // 有判别值（从 0 开始）
```

代码演示只有名字的枚举、带判别值的枚举与 `as u8` 转换。要点是：枚举变体可以携带数据（见"联合与变体"一节），`match` 会强制穷尽；需要"枚举 ↔ 字符串"映射就手写 `Display` 或用 `strum`。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的枚举是值类型，可以只有 case（并可选原始值），也可以给每个 case 附加数据（关联值），`switch` 覆盖全部 case 时不需要 `default`。

```swift
enum Direction { case north, south }          // 纯 case
let d = Direction.north

enum Status: String {                          // 原始值（RawRepresentable）
    case ok = "ok"
    case failed = "failed"
}
Status(rawValue: "ok")                          // 可选：解析失败给 nil

enum Shape {                                    // 关联值（ADT）
    case circle(Double)
    case rect(w: Double, h: Double)
}

enum Direction: CaseIterable { case north, south }   // 可遍历
Direction.allCases
```

代码演示纯 case 枚举、原始值枚举（`RawRepresentable`）与 `CaseIterable`。要点是：原始值与关联值不能混用，`Status(rawValue:)` 返回可选；加了 `CaseIterable` 才能用 `allCases` 遍历。

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有枚举类型**：只有 `const` + `iota` 组成的常量组，既没有类型安全也没有取值检查，需要时自己定义具名类型和 `String()` 方法。

```go
type Direction int
const (
    North Direction = iota   // 0
    South                    // 1
)

func (d Direction) String() string { return [...]string{"North", "South"}[d] }

var d Direction = 99          // 合法！Go 不检查取值
```

代码演示 `type Direction int` + `iota` 常量组以及 `String()` 方法。要点是：`iota` 只是常量计数器（`North == 0` 为真），Go 不校验取值（`(Direction)99` 合法）；类型安全要靠自己写 `Valid()`，`String()` 常用 `go:generate stringer` 生成。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的枚举由标准库 `enum` 提供：`Enum` 的成员不是整数（`IntEnum` 才是）、`StrEnum` 成员是字符串、`Flag`/`IntFlag` 支持位组合，成员都是单例。

```python
from enum import Enum, IntEnum, StrEnum, Flag, auto

class Color(Enum):
    RED = auto()
    BLUE = 2

Color.RED.name, Color.RED.value      # ("RED", 1)
Color(2)                              # Color.BLUE

class Status(IntEnum):                # 同时是 int，可以比较/运算
    OK = 200

class Perm(Flag):                     # 位标志，可组合
    R = auto(); W = auto()
Perm.R | Perm.W

class Kind(StrEnum):                  # 3.11+：成员是字符串
    A = "a"
```

代码演示 `Enum`/`IntEnum`/`StrEnum`/`Flag` 与 `auto()`。要点是：`Enum` 成员**不是**整数（`Color.RED == 1` 为 false），要整数语义用 `IntEnum`；成员是单例，可以安全地当字典键。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `enum class` 是真正的类：可以带构造参数、属性、方法与接口实现，还有 `entries`（1.9+）拿到全部成员。

```kotlin
enum class Direction { NORTH, SOUTH }

enum class Planet(val mass: Double) {          // 带构造参数
    EARTH(5.97e24),
    MARS(6.42e23);

    fun label() = name.lowercase()              // 可以有方法
}

Direction.valueOf("NORTH")                      // 解析（不存在抛异常）
Direction.entries                               // 2.0+ 的枚举列表
Direction.NORTH.ordinal                         // 序号
```

代码演示带构造参数/方法的 `enum class` 与 `valueOf`/`entries`/`ordinal`。要点是：枚举可以有属性、方法、接口实现；`valueOf` 失败会抛异常（安全解析用 `enumValueOf` 或 `entries.find`），`entries` 是 1.9 起的推荐写法。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的枚举本质是一个 `final class`：可以带字段、构造函数和方法，天生单例且序列化安全，`EnumMap`/`EnumSet` 是配套的高效集合。

```java
enum Direction { NORTH, SOUTH }

enum Planet {
    EARTH(5.97e24), MARS(6.42e23);       // 枚举可以有字段与构造函数
    private final double mass;
    Planet(double mass) { this.mass = mass; }
    double mass() { return mass; }
}

Direction d = Direction.valueOf("NORTH");     // 解析
Direction.values();                            // 全部成员（每次调用会复制数组）
d.ordinal(); d.name();

enum Perm implements Flag { R, W }             // 枚举可以实现接口
```

代码演示带字段与构造函数的枚举、`valueOf`/`values()` 以及 `EnumMap`/`EnumSet`。要点是：枚举本质是 `final class`、天生单例且序列化安全；`values()` 每次调用都会复制数组，热路径里应缓存。

{{% /tab %}}

{{% tab header="C++" %}}

C++11 的 `enum class` 是作用域化、强类型的枚举（不隐式转 int），还可以指定底层类型（`enum class Small : std::uint8_t`）；老式 `enum` 会污染作用域。

```cpp
enum class Color { Red, Green };            // C++11 强类型（推荐）
Color c = Color::Red;
// int n = c;                               // 🛑 不隐式转 int
int n = static_cast<int>(c);                 // 必须显式转换

enum class Small : std::uint8_t { A = 1, B };   // 指定底层类型

enum Legacy { X, Y };                        // 老式枚举：污染作用域、可隐式转 int
```

要点是：`enum class` 不污染作用域、不会隐式转换；老式 `enum` 能和 int 混用，新代码基本不该再用。

{{% /tab %}}

{{% tab header="C" %}}

C 的 `enum` 只是 `int` 常量的集合：没有类型安全、没有名字空间、不做取值检查，`enum color c = 999;` 也是合法的。

```c
enum color { RED, GREEN = 5, BLUE };   /* BLUE 是 6 */
enum color c = RED;

int n = c;                              /* 枚举常量就是 int */
enum color bad = 999;                   /* 合法！编译器不检查 */

typedef enum { OK, ERR } status_t;      /* 常见写法：typedef 起别名 */
```

代码演示枚举常量、显式指定值（`GREEN = 5`）以及"越界赋值仍然合法"这一事实。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用 `@enum` 定义枚举，它生成的是一个不可变的原始类型（本质是整数），成员可以比较、排序、做字典键，越界转换会抛错。

```julia
@enum Color RED GREEN BLUE                 # 值从 0 开始
@enum Fruit apple=1 banana=2               # 指定值

instances(Color)                            # 所有成员
Integer(RED)                                # 0
Color(1)                                    # GREEN

enum Color32::UInt8 RED32 GREEN32           # 指定底层类型
```

代码演示 `@enum`、`instances()`、与整数的互转以及指定底层类型。要点是：`@enum` 生成的是原始类型（本质是整数），性能与整数相同，越界转换会抛错。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的枚举是底层整数值类型（可以指定 `byte`/`int` 等底层类型），值不校验（`(Direction)99` 合法）；加 `[Flags]` 就能表示位组合。

```csharp
public enum Direction { North, South }

public enum Status : byte { Ok = 1, Failed = 2 }   // 指定底层类型

[Flags]                                            // 位标志
public enum Perm { None = 0, Read = 1, Write = 2, All = Read | Write }

Direction.North.ToString();
(Direction)99                                       // 合法：不校验
Enum.TryParse("North", out Direction d);
Enum.GetValues<Direction>();
```

代码演示枚举定义、指定底层类型、`[Flags]` 与 `Enum.TryParse`/`GetValues`。要点是：枚举值是整数、不校验取值（要校验用 `Enum.IsDefined` 或自己写方法）；`[Flags]` 让 `ToString()` 输出组合名。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的枚举是编译期常量集合：简单枚举只有名字，2.17 起的增强枚举还能有字段、构造函数、方法与接口实现。

```dart
enum Direction { north, south }             // 简单枚举

enum Planet {                               // 2.17+ 增强枚举
  earth(mass: 5.97e24),
  mars(mass: 6.42e23);

  const Planet({required this.mass});
  final double mass;
  bool get isBig => mass > 1e24;
}

Direction.values;                            // 全部成员
Direction.values.byName("north");             // 按名字取
Direction.north.name;                         // "north"
Direction.north.index;                        // 0
```

代码演示简单枚举与带字段/构造/方法的增强枚举、`byName` 与 `index`。要点是：枚举值是编译期常量，可用于 `const` 与 `switch`；`byName` 找不到会抛异常（安全解析用 `firstWhereOrNull`）。

{{% /tab %}}

{{% tab header="R" %}}

R **没有枚举类型**：最接近的是 `factor`（带 levels 的分类变量，底层是整数），或者用常量字符串向量 + `match()`/`switch()`。

```r
f <- factor(c("a", "b", "a"), levels = c("a", "b"))   # 分类变量
levels(f)            # "a" "b"
as.integer(f)        # 1 2 1（底层是整数）
table(f)             # 计数

treatment <- c("control", "drug")                      # 常量向量
match("drug", treatment)                               # 2：把字符串映射成整数

state <- new.env()                                     # 常量集合
state$idle <- 1; state$running <- 2
```

代码演示 `factor` 的 levels、`as.integer` 与用 `match` 做字符串→整数映射。要点是：factor 本质是"整数 + levels 属性"，水平可以被修改；常量集合用字符串向量 + `match()`/`switch()`，取值校验要自己写。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `enum` 是整数 tag 的封装：可以指定 tag 类型（`enum(u8)`）、可以声明 non-exhaustive（用 `_` 占位以便扩展或 C 互操作）。

```zig
const Color = enum { red, green, blue };
const c: Color = .red;

const Small = enum(u8) { a = 1, b = 2 };        // 指定整数 tag 类型
@intFromEnum(c)                                   // 0
@enumFromInt(1)                                   // .green

const Status = enum(u8) {                          // 非穷尽枚举
    ok = 1,
    _,
};

switch (c) { .red => {}, else => {} }
```

代码演示 `enum`、`enum(u8)`、`@intFromEnum`/`@enumFromInt` 与 non-exhaustive 的 `_`。要点是：枚举是整数 tag 的封装（可指定 tag 类型），`union(enum)` 让每个 tag 携带数据，`_` 给 C 互操作或未来扩展留空间。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有枚举**：惯例是常量表（`{ NORTH = "north" }`）、字符串常量或唯一表值，拼错只会得到 `nil`，需要自己 `assert`。

```lua
local Direction = { NORTH = "north", SOUTH = "south" }
print(Direction.NORTH)

local DIRECTION = {}         -- 另一种：用唯一表值做哨兵
DIRECTION.north = {}
DIRECTION.south = {}
assert(DIRECTION.north ~= DIRECTION.south)

local DAY = { "mon", "tue" }   -- 数组 + 下标当枚举
print(DAY[1])
```

代码演示常量表、用唯一表值当哨兵、以及数组下标当枚举。要点是：没有枚举类型，拼错只会得到 `nil`（需要就 `assert`）；想要编译期检查就用 LuaLS 注解或 Teal。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的 `enum` 会生成运行时代码（有反向映射）；很多团队改用 `as const` 对象 + 字面量联合，因为它可擦除、配合类型收窄更好用。

```ts
enum Direction { North, South }              // 数值枚举（会生成代码）
enum Status { Ok = "ok", Failed = "failed" } // 字符串枚举
const enum Fast { A, B }                      // 编译期常量（会被内联）

// 更常见的替代写法：字面量联合 + as const 对象
const Directions = { North: "north", South: "south" } as const;
type Direction2 = (typeof Directions)[keyof typeof Directions];
```

代码演示数值/字符串枚举、`const enum` 与 `as const` 对象 + 字面量联合。要点是：`enum` 会生成运行时代码（含反向映射），很多团队改用可擦除的 `as const` 对象；`const enum` 在 `isolatedModules` 下受限。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有枚举**：常用 `Object.freeze({ North: "north" })` 或字符串常量表示，拼错不会被编译器拦住。

```js
const Direction = Object.freeze({ North: "north", South: "south" });

const DAYS = ["mon", "tue", "wed"];        // 数组当枚举

// 用 Symbol 做唯一哨兵
const NORTH = Symbol("north");
```

代码演示冻结对象、数组与 Symbol 三种"枚举"写法。要点是：没有枚举类型，字符串常量最容易调试；冻结只防改不防拼错，需要检查就上 TypeScript。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 8.1 起有枚举：纯枚举只有 case 名，backed enum 带 string/int 标量值（`from`/`tryFrom` 解析），枚举可以实现接口、带方法，成员是单例。

```php
enum Direction {                     // 纯枚举（PHP 8.1+）
    case North;
    case South;
}
Direction::North->name;              // "North"

enum Status: string {                // backed enum：有标量值
    case Ok = 'ok';
    case Failed = 'failed';
}
Status::from('ok');                  // 找不到抛 ValueError
Status::tryFrom('nope');             // null

enum Suit: string implements HasColor {   // 枚举可以实现接口、带方法
    case Hearts = 'H';
    public function color(): string { return 'red'; }
}
```

代码演示纯枚举、backed enum 的 `from`/`tryFrom`，以及枚举实现接口。要点是：枚举成员是单例（不要在枚举里存可变状态），backed enum 适合入库与序列化，纯枚举没有标量值。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby **没有枚举**：用常量、Symbol 或冻结数组表示；Rails 的 `enum` 是 ActiveRecord 的功能，不是语言特性。

```ruby
Color = %w[red green blue].freeze          # 字符串常量数组
Color.include?("red")

Direction = { north: 0, south: 1 }.freeze   # 散列映射

class Direction                            # 用类常量模拟
  NORTH = "north"
  SOUTH = "south"
end
```

代码演示冻结数组、散列映射与类常量三种写法。要点是：没有枚举类型，拼错只会得到 `nil`/`false`；

{{% /tab %}}

{{< /tabpane >}}
### 联合与变体

这一节说的是"**和类型**"（sum type）：一个值可能是 A、也可能是 B，而且每种子情况可以带自己的数据。它和"枚举只有名字"不同，也和 C 的 `union`（共享内存）不同。

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `enum Shape { Circle(f64), Rect { .. } }` | 每个变体可带不同数据；`match` 穷尽检查 |
| Swift | ✓ | `enum Shape { case circle(Double) }` | 关联值枚举，`switch` 穷尽 |
| Go | ✗（值层面） | `any` + `type switch`；约束里可写 `~int \| ~float64` | 泛型约束有 union 类型集，但不能当变量类型 |
| Python | ✓（类型层面） | `A \| B` 注解 + `match`（3.10+） | 联合类型注解 + 结构模式匹配，运行时不强制 |
| Kotlin | ✓ | `sealed interface Shape` | 密封层级，`when` 可穷尽 |
| Java | ✓ | `sealed interface Shape permits ...` | 17+ 密封类型 + 21+ `switch` 模式匹配 |
| C++ | ✓ | `std::variant<A, B>` | 类型安全联合；用 `std::visit`/`std::get` |
| C | ✓（不安全） | `union U { int i; float f; };` | 共享内存，没有"当前是哪个成员"的记录 |
| Julia | ✓ | `Union{Int, String}` | 类型联合 + 多分派 |
| C# | ✓ | `record` 继承层级 + 模式匹配 | `switch` 表达式 + 类型模式（C# 9+） |
| Dart | ✓ | `sealed class Shape` | 3.0 密封类 + `switch` 模式穷尽 |
| R | ✗（无静态类型） | `list` + `class` 属性；`UseMethod` / `switch(class(x))` | 动态语言：没有类型层面的和类型，但 `class` 属性 + 分派就是运行时的标签分派 |
| Zig | ✓ | `union(enum) { circle: f64 }` | 标签联合，`switch` 穷尽 |
| Lua | ✗（无静态类型） | 带 `tag`/`kind` 字段的表 | 动态语言：用约定字段做运行时标签分派 |
| TypeScript | ✓ | 判别联合（discriminated union） | 字面量 `kind` 字段 + 穷尽检查 |
| JavaScript | ✗（无静态类型） | `{ kind: "circle" }` + `switch` | 动态语言：运行时约定；TS 用判别联合 |
| PHP | 部分（union 类型） | `int\|string`（PHP 8.0+）、DNF 类型（8.2+）；标签联合靠接口 + 多态 | union 类型只是"几种类型之一"，不是"每种情况带数据"的和类型 |
| Ruby | ✗（近似） | 类层级 + `case/in`（3.0+） | 有模式匹配，但没有静态穷尽检查 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 里"带数据的枚举"本身就是和类型（ADT）：一个值只可能是某个变体，`match` 保证穷尽，`Option`/`Result` 就是标准库的例子。

```rust
enum Shape {
    Circle(f64),
    Rect { w: f64, h: f64 },
    Empty,
}

fn area(s: &Shape) -> f64 {
    match s {                                  // 必须覆盖所有变体
        Shape::Circle(r) => 3.14159 * r * r,
        Shape::Rect { w, h } => w * h,
        Shape::Empty => 0.0,
    }
}
```

代码演示带数据的 `enum` 与穷尽 `match`。要点是：这就是 Rust 的和类型，`Option`/`Result` 也是同一机制；`match` 漏掉变体会编译失败，只关心一种变体时用 `if let`。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 用"关联值枚举"表达和类型，`switch` 覆盖所有 case 时不需要 `default`，`if case` 可以只关心一种情况。

```swift
enum Shape {
    case circle(Double)
    case rect(w: Double, h: Double)
}

func area(_ s: Shape) -> Double {
    switch s {
    case .circle(let r): return .pi * r * r
    case .rect(let w, let h): return w * h
    }
}

if case .circle(let r) = shape { }        // 只关心一种 case
```

代码演示关联值枚举、穷尽 `switch` 与 `if case`。要点是：`switch` 覆盖全部 case 时不需要 `default`，这正是穷尽检查；关联值让枚举表达"每种状态带自己的数据"。

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有值层面的和类型**：你不能声明一个"要么是 A、要么是 B"的变量；泛型约束里虽然能写 union 类型集（`interface{ ~int | ~string }`），但它只描述类型参数的可选范围。运行时表达"多种情况之一"要靠接口 + 类型开关（`switch v := x.(type)`），而新增实现时编译器不会提醒你补分支。

```go
type Shape interface{ isShape() }        // 封闭接口（未导出方法）
type Circle struct{ R float64 }
func (Circle) isShape() {}
type Rect struct{ W, H float64 }
func (Rect) isShape() {}

func Area(s Shape) float64 {
    switch v := s.(type) {               // 运行时类型开关
    case Circle: return 3.14159 * v.R * v.R
    case Rect: return v.W * v.H
    }
    return 0
}
```

代码演示用封闭接口 + 类型开关表达"多种情况之一"。要点是：类型开关是**运行时**的，新增实现时编译器不会提醒你补分支；用未导出方法的接口可以把实现限制在本包内。

{{% /tab %}}

{{% tab header="Python" %}}

Python 用 `Union` 类型注解 + `match`（3.10+ 结构模式匹配）近似和类型；注解运行时不强制，`match` 也没有穷尽检查。

```python
from dataclasses import dataclass
from typing import Union, Literal

@dataclass class Circle: r: float
@dataclass class Rect:   w: float; h: float
Shape = Union[Circle, Rect]

def area(s: Shape) -> float:
    match s:                       # 3.10+ 结构模式匹配
        case Circle(r): return 3.14159 * r * r
        case Rect(w, h): return w * h

# 用字面量标签做"判别联合"
@dataclass class Tagged:
    kind: Literal["circle", "rect"]
```

代码演示 `Union` 注解 + `match`/`case` 结构模式匹配。要运行时分支就用类层级 + `isinstance`，要静态检查就靠 mypy/pyright。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 用 `sealed` 类/接口把子类型封闭在编译期，`when` 因此可以穷尽，`data object` 表示"没有数据的那个分支"。

```kotlin
sealed interface Shape                 // 子类型只能在同一模块内定义
data class Circle(val r: Double) : Shape
data class Rect(val w: Double, val h: Double) : Shape
data object Empty : Shape

fun area(s: Shape) = when (s) {        // when 用于表达式时必须有 else 或穷尽
    is Circle -> 3.14159 * s.r * s.r
    is Rect -> s.w * s.h
    Empty -> 0.0
}
```

代码演示 `sealed interface` + 数据类 + `when` 穷尽。要点是：密封把可能的子类型封闭在编译期，`when` 作为表达式时会检查穷尽；

{{% /tab %}}

{{% tab header="Java" %}}

Java 17+ 的 `sealed interface` + `record` + `switch` 模式匹配（21+）是表达和类型的主流组合，编译器会检查穷尽性。

```java
sealed interface Shape permits Circle, Rect { }     // Java 17+
record Circle(double r) implements Shape { }
record Rect(double w, double h) implements Shape { }

double area(Shape s) {
    return switch (s) {                              // Java 21+：模式匹配 + 穷尽
        case Circle c -> Math.PI * c.r() * c.r();
        case Rect r -> r.w() * r.h();
    };
}
```

要点是：编译器会检查穷尽性（加 `default` 反而掩盖遗漏），record 模式（`case Circle(double r)`）还能直接解构。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 用 `std::variant<A, B>` 表示"几种类型之一"（类型安全联合），访问用 `std::visit` 或 `std::get`，取错类型会抛异常；`std::monostate` 用来表示空状态。

```cpp
#include <variant>

struct Circle { double r; };
struct Rect   { double w, h; };
using Shape = std::variant<Circle, Rect, std::monostate>;   // monostate = 空状态

double area(const Shape& s) {
    return std::visit([](auto&& v) -> double {
        using T = std::decay_t<decltype(v)>;
        if constexpr (std::is_same_v<T, Circle>) return 3.14159 * v.r * v.r;
        else if constexpr (std::is_same_v<T, Rect>) return v.w * v.h;
        else return 0.0;
    }, s);
}
```

代码演示 `std::variant` + `std::visit` + `if constexpr`。要点是：`variant` 会记录当前是哪个备选类型，取错类型抛 `std::bad_variant_access`；

{{% /tab %}}

{{% tab header="C" %}}

C 只有不安全的 `union`：它共享内存、不记录当前是哪个成员；要"带标签的联合"必须自己加 `tag` 字段并保证一致性。

```c
struct shape {
    enum { CIRCLE, RECT } tag;      /* 自己维护标签 */
    union {
        struct { double r; } circle;
        struct { double w, h; } rect;
    } u;
};

double area(const struct shape *s) {
    switch (s->tag) {               /* 靠约定保证 tag 与 union 一致 */
    case CIRCLE: return 3.14 * s->u.circle.r * s->u.circle.r;
    case RECT:   return s->u.rect.w * s->u.rect.h;
    }
    return 0;
}
```

代码演示"tag + union"的手写标签联合。要点是：`union` 不记录当前有效成员，读错成员是 UB 或实现定义；tag 与 union 的一致性完全靠程序员维护。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用 `Union{Circle, Rect}` 表达"几种类型之一"，行为由多分派按实际类型自动选择，不需要 switch/模式匹配。

```julia
struct Circle; r::Float64; end
struct Rect;   w::Float64; h::Float64; end

const Shape = Union{Circle, Rect}          # 类型联合

area(c::Circle) = π * c.r^2
area(r::Rect) = r.w * r.h
area(s::Shape) = error("unknown shape")    # 兜底方法

shapes = Shape[Circle(1.0), Rect(2.0, 3.0)]
area.(shapes)                               # 广播：逐个按类型分派
```

代码演示用 `Union{Circle, Rect}` + 多分派代替 switch。要点是：多分派按实际类型自动选方法、在编译期特化，所以不需要模式匹配；要"封闭集合"可以把子类型限制在自己的包里。

{{% /tab %}}

{{% tab header="C#" %}}

C# 用 `record` 继承层级 + `switch` 表达式/模式匹配（C# 9+）表达"封闭的多种情况"，位置模式与属性模式都能直接写在 `case` 里。

```csharp
public abstract record Shape;
public sealed record Circle(double R) : Shape;
public sealed record Rect(double W, double H) : Shape;

double Area(Shape s) => s switch {
    Circle c => Math.PI * c.R * c.R,
    Rect r => r.W * r.H,
    _ => throw new ArgumentOutOfRangeException(nameof(s)),
};
```

代码演示 `abstract record` 基类 + 派生 `record` + `switch` 表达式。要点是：这是 C# 里最接近 ADT 的写法；编译器只做模式可达性警告，封闭集合要自己用 `abstract`/`sealed` 表达。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 3 的 `sealed` 类 + `switch` 表达式是表达和类型的标准做法：漏掉分支会编译报错。

```dart
sealed class Shape {}                       // 3.0+：同库内才能继承
final class Circle extends Shape { final double r; const Circle(this.r); }
final class Rect extends Shape { final double w, h; const Rect(this.w, this.h); }

double area(Shape s) => switch (s) {         // 穷尽 switch
  Circle(r: var r) => 3.14159 * r * r,
  Rect(w: var w, h: var h) => w * h,
};
```

代码演示 `sealed class` + `switch` 表达式的模式匹配。要点是：漏分支会直接编译报错（穷尽检查）；record 也能配合模式匹配写更轻量的变体。

{{% /tab %}}

{{% tab header="R" %}}

R 是动态类型语言，没有静态类型系统层面的"和类型"声明——但每个对象都带 `class` 属性，配合 `UseMethod` 或 `switch(class(x))` 就是运行时的**标签分派**，实际承担了其他语言里"标签联合"的角色，只是没有编译期穷尽检查。

```r
Circle <- function(r) structure(list(r = r), class = c("circle", "shape"))
Rect   <- function(w, h) structure(list(w = w, h = h), class = c("rect", "shape"))

area <- function(x, ...) UseMethod("area")
area.circle <- function(x, ...) pi * x$r^2
area.rect   <- function(x, ...) x$w * x$h

area(Circle(1))   # 3.141593
```

代码演示 S3 的 `class` 分派（`UseMethod` + `area.circle`）模拟和类型。要点是：分派发生在运行时、没有编译期穷尽检查；新增一种类型只是加一个 `area.xxx` 方法。

{{% /tab %}}

{{% tab header="Zig" %}}

`union(enum)` 是 Zig 的标签联合：tag 和数据放在一起，`switch` 保证只访问当前有效的字段；裸 `union` 是不安全版本。

```zig
const Shape = union(enum) {            // 标签联合：tag + 数据
    circle: f64,
    rect: struct { w: f64, h: f64 },
    empty,
};

fn area(s: Shape) f64 {
    return switch (s) {                 // 穷尽
        .circle => |r| 3.14159 * r * r,
        .rect => |r| r.w * r.h,
        .empty => 0,
    };
}
```

代码演示 `union(enum)` 与穷尽 `switch`。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有静态类型系统，也就没有类型层面的"和类型"；运行时用带 `kind`（或任何标签字段）的表表达"多种情况之一"，拼错字段名或忘记加分支只会在运行时暴露。

```lua
local function circle(r) return { kind = "circle", r = r } end
local function rect(w, h) return { kind = "rect", w = w, h = h } end

local function area(s)
  if s.kind == "circle" then return 3.14 * s.r * s.r
  elseif s.kind == "rect" then return s.w * s.h
  else error("unknown kind: " .. tostring(s.kind)) end
end
```

代码演示带 `kind` 字段的表 + if/elseif 分派。要点是：完全是运行时约定，新增 kind 时旧代码不会报错；要更强约束就用类型注解或换语言。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 用判别联合（一个公共字面量字段 + 联合类型）表达和类型，`switch`/`if` 会自动收窄类型，配 `never` 还能做穷尽检查。

```ts
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "rect"; w: number; h: number };

function area(s: Shape): number {
  switch (s.kind) {                       // 判别字段收窄类型
    case "circle": return Math.PI * s.r ** 2;
    case "rect":   return s.w * s.h;
  }
}
```

代码演示判别联合 + `switch` 收窄 + `never` 穷尽检查。要点是：`default: const _: never = s;` 能在漏分支时编译报错；类型只在编译期存在，运行时校验要另做。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有类型系统，因此没有类型层面的"和类型"；运行时靠 `{ kind: "circle", ... }` 这种标签字段 + `switch` 手动分派——同样的事情在 TypeScript 里可以用判别联合精确表达。

```js
const circle = (r) => ({ kind: "circle", r });
const rect = (w, h) => ({ kind: "rect", w, h });

function area(s) {
  switch (s.kind) {
    case "circle": return Math.PI * s.r ** 2;
    case "rect":   return s.w * s.h;
    default: throw new Error(`unknown kind: ${s.kind}`);
  }
}
```

代码演示 `kind` 字段 + `switch` + `default: throw`。要点是：没有编译期检查，`default: throw` 至少能让问题尽早暴露；需要静态检查就上 TypeScript。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 8.0 起类型系统里有 **union 类型**（`int|string`、`A|B|null`，8.2 起还支持 DNF 形式 `(A&B)|C`），但它表达的是"几种类型之一"，不是"每种情况带自己的数据"的标签联合；后者惯用接口 + 多态（把分支藏进具体类），简单多状态用枚举 + `match`。

```php
interface Shape { public function area(): float; }
final class Circle implements Shape {
    public function __construct(public readonly float $r) {}
    public function area(): float { return M_PI * $this->r ** 2; }
}
final class Rect implements Shape {
    public function __construct(public readonly float $w, public readonly float $h) {}
    public function area(): float { return $this->w * $this->h; }
}

function area(Shape $s): float { return $s->area(); }   // 多态，不做分支
```

代码演示"接口 + 多态"而不是在调用处写 `instanceof` 分支。要点是：PHP 的惯用法是把分支藏进具体类（多态）；枚举 + `match` 只能处理简单的多状态。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 有 `case/in` 模式匹配（3.0+），能按类/数组/哈希模式分派，但没有静态穷尽检查，必须自己写 `else`。

```ruby
Circle = Data.define(:r)
Rect   = Data.define(:w, :h)

def area(shape)
  case shape                      # Ruby 3.0+ 的模式匹配
  in Circle(r:) then Math::PI * r ** 2
  in Rect(w:, h:) then w * h
  else raise ArgumentError, "unknown shape"
  end
end
```

代码演示 `case/in` 的类模式、哈希模式与 `else` 分支。要点是：Ruby 3 有模式匹配但没有穷尽检查（必须写 `else`），也可以直接用多态替代 `case`。

{{% /tab %}}

{{< /tabpane >}}
### 接口、协议与 trait

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `trait Area { fn area(&self) -> f64; }` | 可以为别人的类型实现自己的 trait；有默认方法 |
| Swift | ✓ | `protocol Drawable { func draw() }` | 可写默认实现（extension）；`associatedtype` 支持泛型协议 |
| Go | ✓ | `type Shape interface { Area() float64 }` | **隐式实现**：方法集匹配就满足 |
| Python | ✓ | `class D(Protocol):` / `ABC` | Protocol 是结构化子类型，ABC 是名义子类 |
| Kotlin | ✓ | `interface Drawable { fun draw() }` | 可有默认实现与属性；一个类可实现多个 |
| Java | ✓ | `interface Drawable { void draw(); }` | 多实现；默认方法（8+）、私有方法（9+） |
| C++ | ✓ | 抽象基类（纯虚函数） | 运行时多态靠虚函数；C++20 的 concept 是编译期约束 |
| C | ✗ | 手写 vtable | 没有接口，用函数指针表模拟 |
| Julia | ✗（约定式） | 抽象类型 + 一组方法 | 没有接口关键字，"协议"就是方法约定 |
| C# | ✓ | `interface IDrawable { void Draw(); }` | 默认实现（8+）、静态抽象成员（11+） |
| Dart | ✓ | `abstract class` / `mixin` / `interface class` | mixin 做横向复用；类修饰符控制谁能实现 |
| R | ✗ | S3 泛型函数（`UseMethod`） | 没有接口，用命名约定的方法分派 |
| Zig | ✗ | `anytype` + vtable 结构体 | 没有接口语法，编译期或手写 vtable |
| Lua | ✗ | 鸭子类型 | 有这个方法就能用，没有声明 |
| TypeScript | ✓ | `interface Drawable { draw(): void }` | 结构类型：形状一样就兼容；编译期擦除 |
| JavaScript | ✗ | 鸭子类型 | 没有接口，运行时看方法是否存在 |
| PHP | ✓ | `interface Drawable { }` / `trait` | interface 是契约；trait 是代码复用 |
| Ruby | ✓（近似） | `module Drawable` + `include` | module 做 mixin；本质是鸭子类型 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `trait` 定义"共享行为的契约"：可以有默认方法、关联类型与泛型参数，而且可以为别人的类型实现自己的 trait（孤儿规则允许时）。

```rust
trait Area {
    fn area(&self) -> f64;
    fn describe(&self) -> String { "shape".into() }   // 默认方法
}

impl Area for Circle { fn area(&self) -> f64 { 3.14159 * self.r * self.r } }

fn print_area<T: Area>(x: &T) { }                     // 静态派发（单态化）
fn print_dyn(x: &dyn Area) { }                        // 动态派发（虚表）
```

代码演示 trait 定义、默认方法、泛型约束与 `dyn Trait`。要点是：孤儿规则限制"为谁实现"；泛型约束是静态派发（快但代码更大），`dyn` 是动态派发（小、可放异构集合）。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `protocol` 是接口，`extension` 提供默认实现与给已有类型补遵循；带 `associatedtype`/`Self` 的泛型协议不能再直接当类型用，要写 `any` 或用泛型参数。

```swift
protocol Drawable {
    func draw()
    var name: String { get }              // 可以要求属性
}

extension Drawable {                       // 默认实现
    func draw() { print("default") }
}

struct Circle: Drawable { var name = "circle" }   // 自动满足

protocol Container { associatedtype Item; func get() -> Item }   // 泛型协议
func show<T: Drawable>(_ x: T) { }         // 泛型约束
func showAny(_ x: any Drawable) { }        // 存在类型（Swift 5.7+ 要求写 any）
```

代码演示 protocol + extension 默认实现、`associatedtype` 与 `any`/`some`。`some` 保留静态特化。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `interface` 是方法集：实现是**隐式**的（方法匹配即满足），小接口是惯例，空接口 `any` 不提供任何保证。

```go
type Shape interface {
    Area() float64
}

type Rect struct{ W, H float64 }
func (r Rect) Area() float64 { return r.W * r.H }    // 隐式满足 Shape

var _ Shape = Rect{}                                   // 编译期断言

type Stringer interface{ String() string }             // 标准库也是这么做的
```

代码演示接口定义、隐式实现与编译期断言 `var _ Shape = Rect{}`。要点是：接口是隐式实现的（方法集匹配即满足），小接口是惯例；空接口 `any` 不提供任何保证。

{{% /tab %}}

{{% tab header="Python" %}}

Python 用 `typing.Protocol` 表达结构化子类型（鸭子类型的类型化版本），用 `abc.ABC` 表达名义继承；两者都只在类型检查器里生效。

```python
from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

class Drawable(Protocol):              # 结构化子类型：签名对就满足
    def draw(self) -> None: ...

@runtime_checkable                     # 才允许 isinstance 检查
class Named(Protocol):
    name: str

class Shape(ABC):                      # 名义子类：必须显式继承
    @abstractmethod
    def area(self) -> float: ...
```

代码演示 `Protocol`（结构化子类型）与 `ABC`（名义继承）。`Protocol` 不能有实例状态，需要状态就用 ABC 或普通类。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `interface` 可以有默认实现和属性访问器，一个类能实现多个接口；接口没有状态（不能有 backing field）。

```kotlin
interface Drawable {
    fun draw()
    fun log() { println("drawing") }        // 默认实现
    val name: String get() = "shape"         // 可以要求/提供属性
}

class Circle : Drawable {
    override fun draw() { }
}

interface Repo<T> { fun get(id: String): T } // 泛型接口
```

代码演示接口默认实现、接口属性与泛型接口。要点是：一个类可以实现多个接口；与 Java 互操作时注意 JVM 默认方法的历史差异。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 `interface` 支持多实现、默认方法（8+）、私有方法（9+）与静态方法；不能有实例字段，`sealed` 接口还能表达封闭集合。

```java
interface Drawable {
    void draw();                              // 抽象方法
    default void log() { System.out.println("draw"); }   // 默认方法（8+）
    private void helper() { }                  // 私有方法（9+）
    static Drawable empty() { return () -> { }; }         // 静态方法
}

sealed interface Shape permits Circle, Rect { }           // 封闭集合（17+）
```

代码演示 `interface` 的抽象方法、默认方法、私有方法与 `sealed` 接口。要点是：接口不能有实例字段，默认方法冲突时必须显式覆写；

{{% /tab %}}

{{% tab header="C++" %}}

C++ 没有 `interface` 关键字：接口就是"只有纯虚函数 + 虚析构"的抽象基类；C++20 的 `concept` 是编译期约束，和运行时接口是两回事。

```cpp
struct Drawable {                        // 抽象基类 ≈ 接口
    virtual void draw() const = 0;       // 纯虚函数
    virtual ~Drawable() = default;       // 必须虚析构
};

struct Circle : Drawable {
    void draw() const override { }
};

void render(const Drawable& d) { d.draw(); }   // 通过引用多态
```

代码演示抽象基类（纯虚函数 + 虚析构）与通过引用多态。要点是：C++ 的"接口"就是抽象基类，多态必须用指针/引用；

{{% /tab %}}

{{% tab header="C" %}}

C **没有接口**：只能手写"函数指针表 + 数据指针"的 vtable 结构，是否"实现了接口"完全靠约定与文档。

```c
struct drawable_ops {
    void (*draw)(void *self);
    void (*destroy)(void *self);
};

struct drawable {
    const struct drawable_ops *ops;
    void *self;
};

void draw(struct drawable d) { d.ops->draw(d.self); }
```

代码演示"函数指针表 + 数据指针"的 vtable 接口写法。要点是：接口=结构体里的函数指针，"实现了接口"完全靠约定与文档，没有任何类型检查。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia **没有接口语法**：所谓"协议"就是一组约定方法（如 `iterate`、`show`、`length`），用 `hasmethod` 能在运行时检查方法是否存在。

```julia
abstract type AbstractShape end

struct Circle <: AbstractShape; r::Float64; end

# 约定：任何 AbstractShape 都应实现 area
area(c::Circle) = π * c.r^2
area(x::AbstractShape) = error("area not implemented for $(typeof(x))")

function describe(x::AbstractShape)
    println("area = ", area(x))     # 依赖约定的方法存在
end
```

代码演示抽象类型 + 约定方法 + 兜底方法。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `interface` 支持默认实现（C# 8+）和静态抽象成员（C# 11+），一个类可以实现多个接口，显式实现用于解决同名冲突。

```csharp
public interface IDrawable {
    void Draw();
    void Log() => Console.WriteLine("draw");     // 默认实现（C# 8+）
    static abstract int Version { get; }          // 静态抽象成员（C# 11+）
}

public class Circle : IDrawable {
    public void Draw() { }
}

public class Box<T> where T : IDrawable { }       // 泛型约束
```

代码演示接口默认实现、静态抽象成员、泛型约束与显式接口实现。要点是：默认实现（C# 8+）与静态抽象成员（C# 11+）让接口能力更强；同名冲突用显式接口实现解决。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的"接口"由 `abstract class`、`interface class` 与 `mixin` 分工实现：`implements` 只借契约，`extends` 继承实现，`with` 混入实现。

```dart
abstract class Drawable {
  void draw();
  void log() => print("draw");       // 具体方法
}

class Circle implements Drawable {    // implements：只借接口，不继承实现
  @override void draw() { }
  @override void log() { }
}

mixin Named { String get name => "x"; }   // mixin：横向复用实现
class Art with Named { }

interface class Api { }               // 3.0 修饰符：只能被 implements
```

类修饰符决定谁能继承、谁能实现。

{{% /tab %}}

{{% tab header="R" %}}

R **没有接口**：最接近的是 S3 泛型函数——为 `area` 定义 `area.circle`/`area.rect` 等约定命名的方法，靠 `UseMethod` 在运行时分派。

```r
# 约定：任何有 class "shape" 的对象都应能响应 area()
area <- function(x, ...) UseMethod("area")

area.circle <- function(x, ...) pi * x$r^2
area.rect   <- function(x, ...) x$w * x$h
area.default <- function(x, ...) stop("area() not implemented")

is_shape <- function(x) inherits(x, "shape")     # 运行时能力检查
```

代码演示 S3 泛型函数（`UseMethod` + `area.circle` 命名约定）。要点是：方法名必须遵守约定，拼错只会在运行时报错（走到 `default`）；S4 的 `setGeneric`/`setMethod` 更正式。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig **没有接口关键字**：要么用 `anytype` 做编译期鸭子类型（零开销、单态化），要么手写 `*anyopaque` + 函数指针的 vtable 做运行时多态。

```zig
// 编译期"鸭子类型"：不声明接口，能调用就行
fn draw(it: anytype) void { it.draw(); }

// 运行时接口 = 手写 vtable
const Drawable = struct {
    ptr: *anyopaque,
    drawFn: *const fn (ptr: *anyopaque) void,
    pub fn draw(self: Drawable) void { self.drawFn(self.ptr); }
};

fn asDrawable(x: anytype) Drawable {
    return .{ .ptr = x, .drawFn = @ptrCast(&@TypeOf(x.*).draw) };
}
```

代码演示 `anytype` 编译期鸭子类型与手写 vtable 两种"接口"。要点是：`anytype` 会被单态化（零运行时开销），vtable 用于运行时多态；Zig 没有接口关键字。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 只有鸭子类型：只要对象在运行时存在同名方法就能调用，没有声明、没有检查。

```lua
local function draw(x)
  if type(x.draw) ~= "function" then
    error("object does not implement draw")
  end
  x:draw()
end

local circle = { r = 1 }
function circle:draw() print("circle") end
draw(circle)
```

代码演示运行时检查方法是否存在（鸭子类型）。要点是：只要同名方法存在就能调用，没有声明与检查；契约只能写在文档、断言或 LuaLS 注解里。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的 `interface` 是**结构类型**：形状匹配即兼容，不需要显式 `implements`；它在编译后完全擦除，运行时只有普通对象。

```ts
interface Drawable { draw(): void }              // 结构类型
interface Named extends Drawable { name: string }// 接口继承

class Circle implements Drawable { draw() {} }

function render(d: Drawable) { d.draw(); }        // 结构兼容即可传入

type Handler = { (e: Event): void };              // 可调用签名
```

要点是：接口编译后完全擦除，`instanceof` 只对 class 有意义；声明合并只对 `interface` 生效。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有接口**：靠鸭子类型与运行时检查（`typeof obj.draw === "function"`），需要契约就用 TypeScript 或 JSDoc。

```js
function render(obj) {
  if (typeof obj.draw !== "function") {
    throw new TypeError("draw() is required");
  }
  obj.draw();
}

// 或使用 Symbol 作为"接口"契约
const DRAW = Symbol("draw");
class Circle { [DRAW]() { } }
```

代码演示运行时 `typeof` 检查与用 Symbol 当契约。要点是：没有接口，Symbol 只是避免命名冲突、不提供类型安全；需要契约就上 TypeScript 或 JSDoc 类型。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `interface` 是契约（只声明），`trait` 是可复用的实现（不是类型，`instanceof` 对 trait 无效）；一个类可以 implements 多个接口、use 多个 trait。

```php
interface Drawable {
    public function draw(): void;
}

abstract class Shape implements Drawable {
    abstract public function area(): float;
}

trait Loggable {                       // trait：复用实现（不是类型）
    public function log(string $m): void { echo $m; }
}

final class Circle implements Drawable {
    use Loggable;
    public function draw(): void { }
}
```

代码演示 `interface` 与 `trait` 的分工、多实现与 `use`。trait 冲突用 `insteadof`/`as` 解决。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用 `module` + `include`（mixin）代替接口，还能 `prepend`/`extend`；本质仍是鸭子类型，静态契约交给 RBS/Sorbet。

```ruby
module Drawable                       # module 当"接口 + 默认实现"
  def draw = "shape"
end

class Circle
  include Drawable                    # 实例方法（mixin）
end

class Square
  extend Drawable                     # 变成类方法
end

Circle.new.respond_to?(:draw)          # 运行时能力检查（鸭子类型）
```

代码演示 `module` + `include`/`extend` 与 `respond_to?`。要点是：mixin 提供"带默认实现的接口"，本质仍是鸭子类型；

{{% /tab %}}

{{< /tabpane >}}
### 泛型

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `fn max<T: Ord>(xs: &[T]) -> &T` | 编译期单态化；约束用 trait bound |
| Swift | ✓ | `func f<T: Comparable>(_ a: T)` | 编译期特化；`some`/`any` 控制派发方式 |
| Go | ✓（1.18+） | `func Map[T, U any](...)` | 类型参数 + 约束接口；`~int` 表示底层类型 |
| Python | ✓（类型层面） | `class Box[T]:`（3.12+）/ `TypeVar` | 运行时擦除，只有类型检查器在意 |
| Kotlin | ✓ | `class Box<T>` | 型变 `in`/`out`；`reified` 需 `inline` |
| Java | ✓ | `class Box<T extends Comparable<T>>` | **类型擦除**；通配符与 PECS |
| C++ | ✓ | `template <class T> T max(T a, T b)` | 编译期实例化；C++20 `concept` 约束 |
| C | ✗ | `void*` / 宏 | 没有泛型 |
| Julia | ✓ | `struct Box{T}`、`f(x::T) where T` | 类型参数是一等公民，运行时可见 |
| C# | ✓ | `class Box<T> where T : IComparable<T>` | 运行时保留泛型；值类型专用代码 |
| Dart | ✓ | `class Box<T extends num>` | reified：可以 `is List<int>` |
| R | ✗ | 无 | S3 分派不是泛型；没有参数化类型 |
| Zig | ✓ | `fn f(comptime T: type, x: T)` | comptime 泛型，单态化 |
| Lua | ✗ | 无 | 没有类型系统 |
| TypeScript | ✓ | `function f<T>(x: T): T` | 编译期擦除；条件/映射类型很强 |
| JavaScript | ✗ | 无 | 没有泛型 |
| PHP | ✗ | `@template` 注解 | 语言没有；PHPStan/Psalm 支持 |
| Ruby | ✗ | 无（RBS 有泛型签名） | 语言没有泛型 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的泛型是编译期单态化（每个具体类型生成一份代码，零运行时开销），约束用 trait bound 表达，关联类型用来避免额外的类型参数。

```rust
fn largest<T: PartialOrd>(xs: &[T]) -> &T { &xs[0] }

struct Wrapper<T> { value: T }
impl<T: std::fmt::Display> Wrapper<T> { fn show(&self) { println!("{}", self.value); } }

trait Store { type Item; fn get(&self) -> Self::Item; }   // 关联类型
fn sum<I: Iterator<Item = i32>>(it: I) -> i32 { it.sum() }
```

代码演示泛型函数、泛型结构体、trait bound 与关联类型。要点是：单态化让泛型零运行时开销，但每个具体类型都会生成一份代码（二进制变大）；约束太长可以放到 `where` 子句，关联类型用来表达"每个实现自己的那种类型"。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的泛型支持协议约束、关联类型与 `where` 子句；`some` 保留静态类型信息，`any` 走运行时装箱与动态派发。

```swift
func largest<T: Comparable>(_ xs: [T]) -> T? { xs.max() }

struct Box<T> { var value: T }

protocol Container {
    associatedtype Item
    func get() -> Item
}

func show(_ x: some Drawable) { }   // 不透明类型（编译期知道具体类型）
func showAny(_ x: any Drawable) { } // 存在类型（运行时装箱）
```

代码演示泛型函数、泛型结构体、`associatedtype` 以及 `some` 与 `any` 的区别。要点是：`some` 保留静态类型信息（编译期特化、无装箱），`any` 会装箱并走动态派发；带关联类型的协议不能直接当类型用。

{{% /tab %}}

{{% tab header="Go" %}}

Go 1.18 起支持类型参数：约束用接口表达（`~int` 表示"底层类型是 int"），泛型在编译期实例化，但方法不能有自己的类型参数。

```go
func Map[T, U any](xs []T, f func(T) U) []U {
    out := make([]U, 0, len(xs))
    for _, x := range xs { out = append(out, f(x)) }
    return out
}

type Number interface{ ~int | ~float64 }   // ~ 表示"底层类型是"
func Sum[T Number](xs []T) T { var s T; for _, x := range xs { s += x }; return s }
```

代码演示类型参数、约束接口与 `~` 近似类型。要点是：约束用接口表达，`~int` 表示"底层类型是 int 的具名类型也满足"；

{{% /tab %}}

{{% tab header="Python" %}}

Python 的类型参数只对类型检查器有效，运行时会被擦除；3.12 起可以用 PEP 695 语法（`class Box[T]`、`def f[T]`、`type X[T] = ...`）。

```python
# 3.12+ 的新语法（PEP 695）
class Box[T]:
    def __init__(self, value: T) -> None: self.value = value

def first[T](xs: list[T]) -> T: return xs[0]

type Pair[T] = tuple[T, T]          # 泛型别名

# 旧写法（3.11 及以前）
from typing import TypeVar, Generic
T = TypeVar("T")
class Box2(Generic[T]): ...
```

代码演示 PEP 695 的 `class Box[T]`/`def first[T]`/`type Pair[T]` 与旧的 `TypeVar`+`Generic` 写法。要点是：泛型只对类型检查器有效（运行时被擦除），3.12+ 的新语法更简洁、也更适合写泛型别名。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的泛型支持声明处型变（`out` 协变 / `in` 逆变）与 `where` 约束；需要运行时类型信息时用 `inline` + `reified`。

```kotlin
class Box<T>(val value: T)

fun <T : Comparable<T>> max(a: T, b: T): T = if (a > b) a else b

interface Producer<out T> { fun get(): T }   // 协变：只产出
interface Consumer<in T> { fun put(v: T) }   // 逆变：只消费

inline fun <reified T> isType(x: Any) = x is T   // reified：运行时可见类型
```

代码演示泛型类/函数、声明处型变 `out`/`in` 与 `inline` + `reified`。要点是：型变写在声明处（Java 写在使用处）；`reified` 必须配合 `inline` 才能做 `is T`、`T::class` 这类运行时检查。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的泛型在运行时被**类型擦除**：`List<String>` 与 `List<Integer>` 是同一个类，通配符遵循 PECS（生产者 extends、消费者 super）。

```java
class Box<T extends Comparable<T>> {
    private final T value;
    Box(T value) { this.value = value; }
    T get() { return value; }
}

static double sum(List<? extends Number> xs) { }   // PECS：生产者用 extends
static void add(List<? super Integer> xs) { }      // 消费者用 super
<T> T pick(List<T> xs) { return xs.get(0); }
```

代码演示泛型类、上界 `T extends Comparable<T>`、通配符与 PECS。要点是：类型擦除导致不能 `new T[]`、不能 `instanceof List<String>`；需要运行时类型就传 `Class<T>` 参数。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 用模板做泛型，编译期实例化（错误信息长是主要代价）；C++20 的 `concept`/`requires` 让约束可读性大幅提升，可变参数模板表达任意个数参数。

```cpp
template <class T>
T maxOf(T a, T b) { return a > b ? a : b; }

template <typename T> concept Addable = requires(T a, T b) { a + b; };  // C++20
template <Addable T> T add(T a, T b) { return a + b; }

template <typename... Ts> void print(const Ts&... xs) { }   // 可变参数模板
```

代码演示函数模板、C++20 的 `concept` 约束与可变参数模板。要点是：模板在编译期实例化（每类型一份代码）且必须写在头文件里；

{{% /tab %}}

{{% tab header="C" %}}

C **没有泛型**：只有 `void*` + 回调、宏（无类型安全）或代码生成；C11 的 `_Generic` 能做编译期类型分派。

```c
qsort(arr, n, sizeof arr[0], cmp);     /* void* + 回调：最泛型的写法 */

#define MAX(a, b) ((a) > (b) ? (a) : (b))   /* 宏：无类型检查、可能重复求值 */

#define DEFINE_VECTOR(T, Name) struct Name { T *data; size_t len, cap; }
DEFINE_VECTOR(int, IntVec)                 /* 用宏生成"泛型"容器 */
```

代码演示 `qsort` 的 `void*` + 回调，以及用宏生成容器。要点是：`void*` 丢掉类型信息，宏没有类型安全（还要小心重复求值）；

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的参数化类型是"真泛型"：`Vector{Int}` 与 `Vector{Float64}` 在运行时是不同的类型，类型参数参与多分派与编译期特化。

```julia
struct Box{T}
    value::T
end

f(x::T) where {T<:Number} = x * 2

Box{Int}(1)            # 显式参数
Box(1)                 # 由参数推断 T

const IntVec = Vector{Int}        # 别名
```

代码演示参数化类型 `Box{T}`、`where` 约束与类型推断构造。要点是：类型参数在运行时可见（`Vector{Int}` 与 `Vector{Float64}` 是不同类型），抽象参数 `Vector{<:Number}` 与具体参数语义不同。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的泛型在运行时保留（`typeof(List<int>)` 能拿到真实类型），值类型会生成专用代码（无装箱），约束用 `where` 表达。

```csharp
public class Box<T> where T : IComparable<T> {
    public T Value { get; }
    public Box(T value) => Value = value;
}

public static T Max<T>(T a, T b) where T : IComparable<T> => a.CompareTo(b) > 0 ? a : b;

Span<T> AsSpan<T>(T[] array) => array;      // 泛型 + ref struct
```

代码演示泛型类、`where` 约束与 `Span<T>`。`ref struct` 默认不能当泛型参数（C# 13 起可用 `allows ref struct` 放宽）。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的泛型是 reified 的：`is List<int>` 能工作，`List<int>` 是 `List<num>` 的子类型（协变），但写入时会做运行时类型检查。

```dart
class Box<T extends num> {
  final T value;
  Box(this.value);
}

T first<T>(List<T> xs) => xs.first;

var b = Box<int>(1);
print(b is Box<int>);          // true：泛型是 reified 的
print(<int>[1] is List<num>);  // true：协变
```

代码演示泛型类/函数、`extends` 约束与 `is Box<int>` 检查。要点是：Dart 泛型是 reified 的（运行时可见）；

{{% /tab %}}

{{% tab header="R" %}}

R **没有泛型**（没有参数化类型）：S3 的"泛型函数"指的是 `print`/`summary` 这类按 `class` 分派的方法族。

```r
# S3 的"泛型函数"是方法分派，不是参数化类型
area <- function(x, ...) UseMethod("area")
area.circle <- function(x, ...) pi * x$r^2

# 通用容器靠 list（元素类型不限）或 attr 上的元数据
v <- vector("list", 3)          # 任意元素类型
attr(v, "element_type") <- "numeric"   # 类型只能"记录"，不能强制
```

代码演示 S3 泛型函数（`UseMethod`）与 `vector("list", n)`、属性记录类型。要严格类型化的容器用 vctrs。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的泛型就是"接受 `type` 的 `comptime` 函数"：每个实参组合生成一份代码（单态化），`anytype` 让参数类型自动推断。

```zig
fn maxOf(comptime T: type, a: T, b: T) T { return if (a > b) a else b; }

fn Box(comptime T: type) type {          // 返回类型的函数 = 泛型容器
    return struct {
        value: T,
        pub fn get(self: @This()) T { return self.value; }
    };
}

const IntBox = Box(i32);
fn print(anytype: anytype) void { }       // anytype：自动泛型参数
```

代码演示"接受 `type` 的函数"、`Box(i32)` 返回类型与 `anytype`。没有运行时泛型。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有泛型**：函数接受任意类型，运行时没有任何类型约束，"元素类型"只能写进文档或用 LuaLS 注解。

```lua
local function map(xs, f)          -- 类型完全靠约定
  local out = {}
  for i, x in ipairs(xs) do out[i] = f(x) end
  return out
end

print(map({1, 2, 3}, function(x) return x * 2 end))
```

代码演示把函数作为参数、对任意类型工作。要点是：没有泛型，运行时没有任何类型约束；要表达"元素类型"只能写文档或用 LuaLS 注解。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的泛型只存在于编译期（运行时擦除），但类型层面非常强：条件类型、映射类型、模板字面量类型、`infer` 都能用。

```ts
function first<T>(xs: T[]): T | undefined { return xs[0]; }

class Box<T> { constructor(readonly value: T) {} }

type Keys<T> = keyof T;                       // 键联合
type Pick2<T, K extends keyof T> = { [P in K]: T[P] };   // 映射类型
type Unwrap<T> = T extends Promise<infer U> ? U : T;     // 条件类型 + infer
```

代码演示泛型函数/类、`keyof`、映射类型与条件类型。要点是：编译后完全擦除（运行时拿不到 `T`），但类型层面非常强——映射类型、条件类型与 `infer` 能做类型级编程。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有泛型**：需要静态泛型就上 TypeScript，或用 JSDoc 的 `@template`（只在编辑器里有效）。

```js
function first(xs) { return xs[0]; }        // 参数与返回值都没有类型

class Box {
  constructor(value) { this.value = value; }
}
```

代码演示一个不做任何类型假设的函数。要点是：没有泛型，运行时靠 `typeof`/`Array.isArray` 自己判断；

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 语言层面**没有泛型**：`@template` 是给 PHPStan/Psalm 的注解，运行时不生效；"类型化容器"只能靠运行时校验或专门的集合类。

```php
/**
 * @template T
 * @param T[] $items
 * @return T
 */
function first(array $items) { return $items[0]; }

class Box {                     // 只能靠约定与文档
    public function __construct(public readonly mixed $value) {}
}
```

代码演示 `@template` 注解与 `mixed`。运行时想类型安全只能自己写校验或专门的集合类。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby **没有泛型**：容器接受任意对象；泛型类型签名写在 RBS/Sorbet 里，只在静态分析时生效。

```ruby
def first(xs) = xs.first          # 类型不限

class Box
  def initialize(value) = @value = value
end

# RBS 可以声明泛型签名（类型检查器用，运行时不生效）
# class Box[T]
#   def initialize: (T) -> void
# end
```

代码演示不做类型假设的方法与 RBS 泛型签名注释。泛型签名只存在于 RBS/Sorbet 里。

{{% /tab %}}

{{< /tabpane >}}

### 类型别名与新类型

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `type Id = u64`；新类型用 `struct Id(u64)` | 别名不产生新类型，newtype 才有类型安全 |
| Swift | ✓ | `typealias ID = Int` | 只是别名；新类型要包装 struct |
| Go | ✓ | `type ID = int64`（别名）/ `type ID int64`（新类型） | 有没有 `=` 决定一切 |
| Python | ✓ | `type Alias = int`（3.12+）/ `NewType` | NewType 只被静态检查器区分 |
| Kotlin | ✓ | `typealias ID = Long` / `@JvmInline value class` | 值类得到零开销新类型 |
| Java | ✗ | 无 | 需要新类型就写包装 `record` |
| C++ | ✓ | `using Id = std::uint64_t;` / 包装 struct | 别名 / 强类型包装 |
| C | ✓ | `typedef uint64_t id_t;` | 只是别名，不产生新类型 |
| Julia | ✗ | `const Id = UInt64` | 只是绑定，不是类型 |
| C# | ✓ | `using Id = int;`（C# 12+） | 别名；新类型用 `readonly record struct` |
| Dart | ✓ | `typedef F = int Function(int)` / `extension type Id(int)` | 3.3+ 的 extension type 是零开销包装 |
| R | ✗ | 无 | 没有别名机制 |
| Zig | ✗ | `const Id = u64;` | 只是常量绑定 |
| Lua | ✗ | 无 | 没有类型系统 |
| TypeScript | ✓ | `type Id = string` / branding | 类型别名可模拟名义类型 |
| JavaScript | ✗ | 无 | 没有类型 |
| PHP | ✗ | 无 | 用类包装 |
| Ruby | ✗ | 无 | 用类或 RBS 别名 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `type` 是类型别名（与原名完全等价、不产生新类型）；想要"同样的底层类型但是不同类型"必须用元组结构体写 newtype。

```rust
type Id = u64;                  // 别名：与 u64 完全等价
struct UserId(u64);             // newtype：不同类型，零开销

let a: Id = 1;
let b: UserId = UserId(1);
// let c: Id = b.0;             // 需要显式 .0 取内部值
```

代码演示 `type Id = u64`（完全等价）与 `struct UserId(u64)`（不同类型）。要点是：别名不提供任何类型安全，newtype 才有；newtype 还能绕过孤儿规则（为外部类型实现外部 trait）。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `typealias` 只是给类型起别名（编译器和 IDE 的可读性工具），要类型安全就得包装 struct。

```swift
typealias ID = Int                // 别名
typealias Handler = (Int) -> Void

struct UserId: Equatable, Hashable { let raw: Int }   // 新类型：要自己包装
```

代码演示 `typealias` 与包装 struct。要点是：`typealias` 只是可读性工具（与原名完全等价），要类型安全必须写包装结构体。

{{% /tab %}}

{{% tab header="Go" %}}

Go 里 `type A = B` 是**别名**（完全同一个类型），`type A B` 是**定义新类型**（有独立的方法集，不能隐式互转）；关键就是有没有那个 `=`。

```go
type ID = int64          // 别名：ID 和 int64 是同一个类型
type UserID int64        // 新类型：有自己的方法集，不能隐式互转

func (u UserID) Valid() bool { return u > 0 }

var a ID = 1
var b UserID = UserID(a)   // 必须显式转换
```

代码演示 `type ID = int64`（别名）与 `type UserID int64`（新类型）的差别。新类型有自己的方法集，并且不能隐式互转（必须显式转换）。

{{% /tab %}}

{{% tab header="Python" %}}

Python 3.12 起用 `type X = ...` 声明类型别名（PEP 695），`typing.NewType` 则在静态检查层面制造"新类型"；两者运行时都只是普通对象。

```python
type UserId = int                        # 3.12+：类型别名（PEP 695）
UserId2 = int                            # 老写法：普通赋值别名

from typing import NewType
OrderId = NewType("OrderId", int)        # 新类型（静态检查器区分）

def f(x: OrderId) -> None: ...
# f(1)   # 类型检查器报错；f(OrderId(1)) 才对
```

代码演示 PEP 695 的 `type UserId = int`、普通赋值别名与 `NewType`。要点是：`type` 与赋值别名在运行时都只是普通对象，"新类型"要靠 `NewType`（也只对静态检查器有效）。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `typealias` 只是可读性别名；要零开销的类型安全包装用 `@JvmInline value class`（旧名 inline class）。

```kotlin
typealias ID = Long                       // 别名（不产生新类型）
typealias Handler = (Int) -> Unit

@JvmInline
value class UserId(val raw: Long)          // 值类：新类型 + 基本零开销

val a: UserId = UserId(1)
// val b: Long = a                        // 🛑 类型不匹配
```

要点是：别名只是可读性，值类才是零开销的类型安全包装；但值类在可空、泛型、数组等位置仍可能装箱。

{{% /tab %}}

{{% tab header="Java" %}}

Java **没有类型别名**（`import` 只是导入名字）；需要"同一底层类型但语义不同"就写单字段 `record`。

```java
record UserId(long value) { }        // 用包装 record 造"新类型"
record OrderId(long value) { }

void f(UserId id) { }
// f(new OrderId(1));                // 🛑 类型不匹配：编译期就拦住
```

代码演示用单字段 `record` 造新类型。包装 record 能在编译期就拦住"把 `OrderId` 当 `UserId` 用"，而且几乎没有运行时开销。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的 `using`/`typedef` 是别名（不产生新类型），强类型包装要写 struct；C++20 起可以给包装加 `operator<=>` 自动生成比较。

```cpp
using Id = std::uint64_t;            // C++11 起的别名（比 typedef 可读）
typedef std::uint64_t LegacyId;      // 老写法

struct UserId { std::uint64_t v; };  // 强类型包装
// UserId u = 1;                     // 🛑 不允许隐式转换
UserId u{1};
```

要点是：别名不产生新类型；

{{% /tab %}}

{{% tab header="C" %}}

C 的 `typedef` 只是别名：`id_t` 与 `uint64_t` 完全等价；唯一的"新类型"手段是结构体包装。

```c
typedef uint64_t id_t;               /* 只是别名 */
typedef struct user_id { uint64_t v; } user_id_t;   /* 想要强类型就得包一层 */

id_t a = 1;
user_id_t u = { .v = 1 };            /* 不能直接和 id_t 混用（会编译错误） */
```

代码演示 `typedef` 与结构体包装。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `const Id = UInt64` 只是把类型绑定到一个名字（`Id === UInt64`），不是新类型；要类型安全就写 `struct` 包装。

```julia
const Id = UInt64                 # 只是绑定一个名字，不是新类型

struct UserId                     # 想要新类型就包装
    v::UInt64
end

UserId(1) == UserId(1)            # 结构体按字段比较（默认 === 语义见注意）
```

代码演示 `const Id = UInt64`（只是绑定）与 `struct UserId`（包装）。要点是：`Id === UInt64` 为真，不是新类型；包装结构体通常会在编译期被优化掉，代价很低。

{{% /tab %}}

{{% tab header="C#" %}}

C# 12 起支持 `using Id = int;` 这样的类型别名；想要名义类型与值语义就用 `readonly record struct`。

```csharp
using Id = System.Int64;                  // C# 12+ 的 using 别名

public readonly record struct UserId(long Value);   // 新类型（值语义）
public readonly record struct OrderId(long Value);

void F(UserId id) { }
// F(new OrderId(1));                     // 🛑 编译错误
```

代码演示 C# 12 的 `using Id = long;` 与 `readonly record struct UserId(long Value)`。要点是：别名没有类型安全，record struct 才同时提供值语义、名义类型与 `with` 表达式。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `typedef` 用于函数/记录类型别名；3.3 起的 `extension type` 是**编译期零开销**的包装，适合给已有类型加语义（ID、单位、金额）。

```dart
typedef Mapper = int Function(int);        // 函数类型别名

extension type UserId(int raw) {            // Dart 3.3+：零开销包装
  bool get isValid => raw > 0;
}

UserId id = UserId(42);
int raw = id.raw;                           // 访问表示类型
// int x = id;                              // 🛑 不会隐式转换
```

代码演示 `typedef Mapper = ...` 与 `extension type UserId(int raw)`（Dart 3.3+）。

{{% /tab %}}

{{% tab header="R" %}}

R **没有别名机制**：类型是运行时属性；要表达"用途"只能加 `class` 属性，或使用 vctrs 的 `new_vctr()` 建立带校验的类型。

```r
Id <- "numeric"          # 只是把字符串存到变量里，和类型无关
x <- 1:3                 # 类型由值决定

# 想要"语义化类型"只能靠 class 属性
user_id <- structure(1L, class = "user_id")
```

代码演示 `Id <- "numeric"`（只是字符串变量）与给对象加 `class` 属性。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `const Id = u64;` 只是常量绑定（不是别名类型），要新类型就定义包装 struct，通常没有任何运行时开销。

```zig
const Id = u64;                  // 只是常量绑定：Id 和 u64 完全一样

const UserId = struct {           // 新类型
    v: u64,
};

const a: Id = 1;
const b = UserId{ .v = 1 };
```

代码演示 `const Id = u64;`（常量绑定）与包装 struct。要点是：Zig 没有类型别名语法，`const X = T` 只是给类型起个名字；新类型用 struct 包装，通常零开销。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有类型别名**（也没有类型系统）：语义区分只能靠表里的标记字段或 Symbol 约定。

```lua
local Id = "number"        -- 只是字符串，和类型无关
local UserId = {}
UserId.__index = UserId     -- 用表当"类型标记"
```

代码演示用表当"类型标记"。要点是：没有类型系统也就没有别名；

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的 `type` 别名编译后完全消失；用 branding 技巧（`string & { [brand]: "UserId" }`）可以模拟名义类型。

```ts
type Id = string;                     // 类型别名（编译期）
type Handler = (e: Event) => void;

declare const brand: unique symbol;   // 名义类型模拟
type UserId = string & { [brand]: "UserId" };

function f(id: UserId) { }
// f("x" as string);                  // 🛑 类型不匹配
```

要点是：别名编译后消失，branding 是 TS 里模拟名义类型的主流做法。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有类型别名**：需要区分语义就用 `Symbol`、标签字段或运行时校验。

```js
const ID = Symbol("id");        // 想区分语义就用 Symbol 或标签字段

function makeUserId(n) { return { kind: "UserId", value: n }; }
```

代码演示用 Symbol 或标签字段区分语义。要点是：没有类型别名，语义区分靠运行时约定；需要静态检查就上 TypeScript。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP **没有类型别名**（`use` 只是导入命名空间）：用 `final class`/`readonly class` 包装当新类型，`@phpstan-type` 只对静态分析器有效。

```php
final class UserId {                      // 用类包装 = 新类型
    public function __construct(public readonly int $value) {}
}

function f(UserId $id): void { }

// 或用 PHPDoc 的 @phpstan-type（只对静态分析器有效）
/**
 * @phpstan-type Id int
 */
```

代码演示 `final class UserId` 包装与 `@phpstan-type` 注解。要点是：语言没有类型别名（`use` 只是导入命名空间），静态别名只对分析器有效。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby **没有类型别名**：用类/`Struct`/`Data` 表达新类型，类型别名只在 RBS 里存在。

```ruby
UserId = Struct.new(:value)         # 用类/Struct 表达"新类型"

# RBS 里可以写类型别名（运行时不生效）：
# type user_id = Integer
```

代码演示 `UserId = Struct.new(:value)` 与 RBS 的 `type user_id = Integer`。要点是：语言没有类型别名，语义区分靠类包装或运行时校验。

{{% /tab %}}

{{< /tabpane >}}

## 空值与可选

"没有值"是各家分歧最大的语义之一：C 只有指针能是 `NULL`，Rust/Swift/Kotlin 把它做进类型系统，Go 用零值 + comma-ok 绕开它，Python/Lua/Ruby 只有一个 `nil`/`None`，而 R 有 **三种**"没有"（`NULL`、`NA`、`NaN`）。这一节按"怎么写、怎么判、怎么取值、有什么坑"来对照。

**一页速览**

| 语言 | "没有值"叫什么 | 谁在管 | 一句话提醒 |
| --- | --- | --- | --- |
| Rust | `None`（`Option<T>`） | 类型系统 | 没有 null；用 `?`/`unwrap_or`/`match` |
| Swift | `nil`（`T?`） | 类型系统 | `if let`/`guard let`/`??`；`!` 会崩 |
| Go | `nil`（指针/切片/map/接口/error） | 运行时约定 | nil map 写入 panic；"typed nil" 接口不为 nil |
| Python | `None` | 运行时 | 判 None 用 `is`；`x or d` 会误伤 `0`/`""` |
| Kotlin | `null`（`T?`） | 类型系统 | `?.`/`?:`/`!!`；Java 来的平台类型 `T!` 不检查 |
| Java | `null` / `Optional<T>` | 注解与库 | Optional 建议只当返回值 |
| C++ | `std::nullopt` / `std::optional<T>` | 库类型 | 引用不能为空；`*o` 不检查 |
| C | `NULL` / `nullptr` | 只有指针 | 没有可空值类型，用哨兵或输出参数 |
| Julia | `nothing` / `missing` | 类型系统（`Union`） | `coalesce` 只跳 missing，`something` 只跳 nothing |
| C# | `null`（`int?` / `string?`） | 类型系统（可空引用是警告） | `?.`/`??`；`a.Value` 不检查会抛 |
| Dart | `null`（`T?`） | 类型系统（健全） | `?.`/`??`/`!`；`late` 是运行时检查 |
| R | `NULL` / `NA` / `NaN` | 运行时 | `is.na(NaN)` 为真；`NULL` 在向量里会消失 |
| Zig | `null`（`?T`） | 类型系统 | `orelse`/`if (...) |v|`/`.?`；`undefined` 不是 null |
| Lua | `nil` | 运行时 | 赋 nil 会删表键；`or` 会把 `false` 也替换 |
| TypeScript | `null` / `undefined` | 编译期（`strictNullChecks`） | `??` 与 `||` 不同；`!` 只是让编译器闭嘴 |
| JavaScript | `null` / `undefined` | 无 | `x == null` 同时判两者；默认参数只认 undefined |
| PHP | `null` | 类型系统（`?T`） | `isset` 对 null 为 false；`?->` 空安全调用 |
| Ruby | `nil` | 运行时 | 只有 nil/false 为假；`&.` 安全导航，`||` 会吞掉 false |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust **没有 null**：用 `Option<T>`（`Some(v)` / `None`）把"可能没有值"写进类型，用 `match`、`if let`、`?`、`unwrap_or` 处理它。

```rust
let a: Option<i32> = Some(1);
let b: Option<i32> = None;         // 没有 null

match a { Some(x) => x, None => 0 }
if let Some(x) = a { }
let c = a.unwrap_or(0);            // 有默认值
let d = a?;                        // ? 在 Option/Result 上提前返回
a.map(|x| x + 1).and_then(|x| Some(x * 2));
a.filter(|x| *x > 0);
a.unwrap();                        // 🛑 None 时 panic，生产代码少用
a.expect("a 必须存在");             // 同上，但带信息
```

要点是：`unwrap`/`expect` 表示"我确定不是 None"（写错就 panic），`?` 在返回 `Option`/`Result` 的函数里做提前返回，是最优雅的传播方式。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 用 `Optional<T>`（写作 `T?`）表示"有值或无值"，`nil` 就是它的空值；解包方式有 `if let`/`guard let`/`??`，`!` 会在 nil 时崩溃。

```swift
var a: Int? = 1                    // Optional<Int>
var b: Int? = nil

if let a { print(a) }              // 简写（Swift 5.7+）
guard let a else { return }        // 提前退出
let c = a ?? 0                     // 默认值
let d = a.map { $0 + 1 }
a?.description                     // 可选链
// a!                             // 🛑 nil 时崩溃
let e = try? risky()               // 失败变 nil
let f: Int! = 1                    // 隐式解包（危险，尽量别用）
["1", "x"].compactMap(Int.init)    // 过滤掉 nil
```

代码演示 `if let`/`guard let`/`??`、可选链、`try?` 与 `compactMap`。Optional 可以嵌套（`Int??`），`if let` 只解一层。

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有 Option 类型**：指针/切片/map/接口/函数/error 的零值是 `nil`，存在性用 comma-ok（`v, ok := m[k]`）表示，失败用 `error` 接口表示。

```go
var p *int                 // nil 指针
var s []int                // nil 切片（len 为 0，可直接 append）
var m map[string]int       // nil map：读可以，写会 panic
var e error                // nil 接口

v, ok := m["k"]            // comma-ok：判断"存在"
if err != nil { return err }

if v, ok := x.(string); ok { }   // 类型断言
```

代码演示 nil 指针、nil map、comma-ok 与 `err != nil`。要点是：nil map 写入会 panic（要先 `make`）；"typed nil"赋给接口后 `err != nil` 仍为 true，这是 Go 最隐蔽的坑之一。

{{% /tab %}}

{{% tab header="Python" %}}

Python 用单例 `None` 表示"没有值"：判等要用 `is None`（`== None` 可能被 `__eq__` 干扰），`None` 也是假值。

```python
a = None
def f(x: int | None = None) -> None: ...     # 3.10+ 的写法（旧写法 Optional[int]）

if a is None: ...            # ✅ 判 None 永远用 is
if a == None: ...            # 🛑 可能被 __eq__ 干扰

b = a or 0                   # ⚠️ 0、""、[] 也会走默认值
c = 0 if a is None else a    # ✅ 精确判 None

d = data.get("k", None)
e = getattr(obj, "attr", None)
f = (items or [])[0] if items else None
```

代码演示 `is None` 判断、`or` 默认值与 `getattr(obj, "x", None)`。要点是：`x or default` 会把 `0`/`""`/`[]` 也替换掉（要精确判断就写条件表达式），而 `== None` 可能被自定义 `__eq__` 干扰。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 把可空性写进类型系统：`T?` 与 `T` 是不同类型，编译器强制你用 `?.`、`?:`、`!!` 或 `requireNotNull` 处理。

```kotlin
var a: String? = null         // 可空类型
var b: String = "x"           // 不可空

a?.length                     // 安全调用，返回 Int?
a?.length ?: 0                // Elvis：为 null 时给默认值
a!!.length                    // 🛑 强解包：null 时抛 NPE
a?.let { println(it) }        // 只在实际非空时执行

val c = listOfNotNull(a, b)   // 过滤掉 null
requireNotNull(a)             // 不满足就抛 IllegalArgumentException
val d = a ?: error("缺失")     // 抛 IllegalStateException
```

代码演示 `?.`/`?:`/`!!`/`let` 与 `requireNotNull`。要点是：可空性是类型系统的一部分（编译器强制处理）；来自 Java 的"平台类型"不做检查，`!!` 会抛 NPE，安全写法是 `?.` 加 Elvis。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的引用类型都可以是 `null`（基本类型不行）；`Optional<T>` 主要用于返回值，字段与参数更多用 `@Nullable` 注解 + 静态分析。

```java
String a = null;                     // 任何引用类型都可以是 null
int b = 0;                           // 基本类型不能是 null

Optional<String> o = Optional.ofNullable(a);
o.orElse("default");
o.orElseGet(() -> compute());
o.map(String::length);
o.orElseThrow(() -> new IllegalStateException("缺失"));
o.ifPresent(System.out::println);

Objects.requireNonNull(a, "a 不能为空");
int n = a == null ? 0 : a.length();
```

代码演示 `Optional.ofNullable`/`orElse`/`map`/`orElseThrow` 与 `Objects.requireNonNull`。要点是：`Optional.of(null)` 抛 NPE（要用 `ofNullable`）；

{{% /tab %}}

{{% tab header="C++" %}}

C++17 的 `std::optional<T>` 表示"可能有值"，空状态是 `std::nullopt`；裸指针用 `nullptr`，而引用永远必须绑定对象。

```cpp
int* p = nullptr;                      // C++11 起的空指针字面量
std::optional<int> o = std::nullopt;   // C++17：可能有值
o = 42;
o.has_value(); o.value();              // value() 为空时抛 std::bad_optional_access
o.value_or(0);
*o;                                    // 不检查，空则 UB
if (o) { }

std::optional<std::optional<int>> nested;   // 区分"没有"与"空值"
```

代码演示 `std::optional`、`value()`/`value_or` 与嵌套 optional。要点是：`*o` 不检查（空则 UB），`value()` 才抛异常；引用不能为空、`optional<T&>` 非法，要"可空引用"就用指针。

{{% /tab %}}

{{% tab header="C" %}}

C 里只有指针可以为空（`NULL`/C23 的 `nullptr`），值层面的"缺失"要靠哨兵值（`-1`、`NAN`）或输出参数表示。

```c
int *p = NULL;                  // 只有指针可以为空
if (p != NULL) { *p = 1; }
p = nullptr;                    // C23 起的关键字（更安全，类型正确）

/* 值层面的"缺失"只能用哨兵或输出参数 */
int find(const char *s, int *out);     // 返回 0/1 表示成功/失败
double v = NAN;                        // 用 NAN 当哨兵（要 isnan 检查）
errno = 0;                             // 标准库的错误约定
```

代码演示 `NULL`/`nullptr` 检查与"哨兵值 + 输出参数"两种缺失表达。要点是：只有指针能为空，值层面的缺失只能用哨兵（如 `NAN`）或额外返回成功标志；解引用空指针是 UB 而不是异常。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 严格区分 `nothing`（没有值）与 `missing`（数据缺失，遵循三值逻辑）：`coalesce` 只跳 `missing`，`something` 只跳 `nothing`。

```julia
x = nothing            # Nothing 单例："没有值"
y = missing            # Missing 单例："缺失数据"（三值逻辑）

z::Union{Int, Nothing} = nothing
w::Union{Int, Missing} = missing

isnothing(x); ismissing(y)
coalesce(y, 0)         # 跳过 missing：y 是 missing 时得 0
something(x, 0)        # 跳过 nothing：x 是 nothing 时得 0
x === nothing          # 判 nothing 用 ===
skipmissing([1, missing, 3]) |> collect   # [1, 3]
y + 1                  # missing：缺失会传染
y == 1                 # missing（不是 false）
isequal(y, missing)    # true
```

代码演示 `nothing`/`missing`、`isnothing`/`ismissing`、`coalesce`/`something` 与 `skipmissing`。`missing` 参与运算会传染（结果仍是 `missing`）。

{{% /tab %}}

{{% tab header="C#" %}}

C# 用 `int?`（`Nullable<T>`）表示可空值类型，用 `string?`（可空引用类型，C# 8+）表示可空引用；后者默认只是编译期警告。

```csharp
int? a = null;                  // Nullable<int>，值类型的可空版本
a.HasValue; a.Value;            // 直接取 Value 而 a 是 null → 抛异常
a.GetValueOrDefault();          // 安全

string? s = null;               // C# 8 可空引用类型（编译期警告，不是错误）
s?.Length;                      // 空安全调用
s ?? "default";                 // 空合并
s ??= "default";                // 空合并赋值
s!.Length;                      // 空宽容运算符：我保证不是 null

ArgumentNullException.ThrowIfNull(s);      // .NET 6+
```

代码演示 `int?`/`HasValue`/`GetValueOrDefault`、`?.`/`??`/`??=` 与可空引用类型。要点是：可空引用类型默认只是编译期警告（要开 `<Nullable>`），`a.Value` 不检查会抛 `InvalidOperationException`。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 有健全的空安全：`T?` 可空、`T` 不可空，编译器在流分析里收窄类型；`late` 是"我保证会赋值"的运行时检查。

```dart
String? a;                 // 可空（null safety，Dart 2.12+）
String b = "x";            // 不可空

print(a?.length);          // null 时返回 null（不做后续调用）
print(a ?? "default");     // 空合并
a ??= "default";           // 空合并赋值
print(a!.length);          // 🛑 null 时抛异常（TypeError/Null check operator）

late String c;             // 延迟初始化；用之前赋值，否则抛 LateInitializationError
late final String d;
```

代码演示 `String?` 与 `String` 的区分、`?.`/`??`/`!` 与 `late`。要点是：空安全是健全的（流分析能把 `String?` 收窄成 `String`），但 `!` 在 null 时抛异常，`late` 是运行时的"我保证会赋值"。

{{% /tab %}}

{{% tab header="R" %}}

R 有**三种**"没有"：`NULL`（空对象、length 为 0）、`NA`（缺失值，有类型）、`NaN`（非数字）；`is.na(NaN)` 为真，所以判 NA 与判 NaN 是两件事。

```r
NULL          # 空对象：length 为 0
NA            # 缺失值（有类型：NA_integer_ / NA_real_ / NA_character_）
NaN           # 不是数字（0/0、sqrt(-1)）

is.null(NULL)      # TRUE
is.na(NaN)         # TRUE ← NaN 也算 NA
is.nan(NaN)        # TRUE
is.na(NULL)        # logical(0) ← 不是 TRUE！

c(1, NULL, 2)      # c(1, 2)：NULL 在向量里会消失
c(1, NA, 2)        # c(1, NA, 2)：NA 会保留并传染
mean(c(1, NA, 3))                  # NA
mean(c(1, NA, 3), na.rm = TRUE)    # 2
```

代码演示 `NULL`/`NA`/`NaN` 的判别、`na.rm` 与 `is.na(NULL)` 的特殊结果。要点是：`is.na(NaN)` 为真（要区分 NA 与 NaN 得用 `is.nan`），`c(1, NULL, 2)` 会得到 `c(1, 2)`（NULL 在向量里消失），任何与 NA 的比较结果都是 NA。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `?T` 是可选类型（值为 `null` 或具体值），处理方式有 `orelse`、`if (x) |v|`、`.?`；注意 `undefined` 表示"未初始化"，读它是 UB，不是 null。

```zig
var a: ?i32 = null;            // 可选类型：?T
a = 42;
const b = a orelse 0;          // 空则给默认值
if (a) |v| { _ = v; }          // 有值才进入
const c = a.?;                 // 断言非空；为空时安全模式 panic

while (it.next()) |item| { }   // 迭代器惯用法

var u: u32 = undefined;        // ⚠️ undefined ≠ null：读它是 UB
fn f() !void { }               // 错误联合 !T 表达"失败"，与 null 是两回事
```

代码演示 `?T`、`orelse`、`if (a) |v|`、`.?` 与 `undefined` 的区别。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 只有 `nil` 表示"没有值"：读不存在的表键得到 `nil`，给键赋 `nil` 等于删除该键，`or` 默认值会把 `false` 也一起替换。

```lua
local a = nil                  -- nil 是唯一的"空"
print(type(nil))                -- "nil"

local t = {}
t.x = 1
t.x = nil                       -- 赋 nil = 删除这个键
print(t.x)                      -- nil（读不存在的键也给 nil，不报错）

local v = t.y or 0              -- ⚠️ false 也会走默认值
if t.y ~= nil then v = t.y end  -- ✅ 精确判断
assert(a ~= nil, "a 不能为空")
```

代码演示 `nil`、赋 nil 删键与 `assert`。要点是：读不存在的键得到 `nil` 而不是报错，`or` 默认值会把 `false` 一起替换（要精确判断就写 `if x ~= nil`）。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 区分 `null` 与 `undefined` 两种值，`strictNullChecks` 打开后它们才进入类型系统；`??` 只对 null/undefined 生效，`!` 只是让编译器闭嘴。

```ts
let a: string | null = null;
let b: string | undefined = undefined;
let c: { x?: number } = {};          // 可选属性：可能是 undefined

a?.length;                            // 可选链
a ?? "default";                       // null/undefined 才走默认值
a ??= "default";
a!.length;                            // 非空断言：只影响类型，不做运行检查

type T = NonNullable<string | null>;  // string
function f(x: string | null): string { if (x === null) return ""; return x; }  // 收窄
```

代码演示 `string | null`、可选属性、`?.`/`??`/`!` 与类型收窄。要点是：`strictNullChecks` 必须开；`??` 与 `||` 语义不同（`||` 会替换 `0`/`""`）；`!` 只是让编译器闭嘴，运行时该空还是空。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 同时有 `null`（显式置空）与 `undefined`（未定义/未赋值），`x == null` 能同时判断两者，函数默认参数只对 `undefined` 生效。

```js
let a;                     // undefined：声明了没赋值
const b = null;            // null：显式置空
typeof null;               // "object" ← 历史遗留 bug

a?.length;                 // 可选链（ES2020）
a ?? "default";            // 空值合并（ES2020）
a ??= "default";           // 空值合并赋值（ES2021）

if (x == null) { }         // 同时判 null 与 undefined（== 的白名单用法）
function f(x = 1) { }      // 默认参数只对 undefined 生效，null 不触发
Object.hasOwn(o, "k");     // 判断属性存在（ES2022）
```

代码演示 `undefined`/`null`、`x == null` 与默认参数。要点是：`f(undefined)` 会用默认值而 `f(null)` 不会；可选链只在 null/undefined 处短路；`delete obj.k` 之后属性是 undefined 而不是 null。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 用 `null` 表示空值，`?T` 声明可空类型；注意 `isset()` 对值为 null 的键返回 false，判断"键存在"要用 `array_key_exists`。

```php
$a = null;

function f(?string $s = null): void { }   // 可空类型（PHP 7.1+）
class C { public ?int $n = null; }

$x = $a ?? "default";          // 空合并：未定义变量也不报警
$a ??= "default";
$obj?->method();               // 空安全调用（PHP 8.0+）

isset($a);                      // false（null 也返回 false）
array_key_exists("k", $arr);    // 更严格：键存在，值为 null 也算存在
is_null($a);
```

代码演示 `?string`、`??`、`?->` 与 `isset`/`array_key_exists`。PHP 8.1 起给内部函数传 null 到不可空参数会告警。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的 `nil` 是 `NilClass` 的单例对象（不是"什么都没有"，它也响应 `to_s`/`to_a`）；`&.` 做安全导航，`||` 会把合法的 `false` 一起替换掉。

```ruby
a = nil                     # nil 是 NilClass 的单例对象
nil.nil?                    # true
nil.to_s                    # ""（Ruby 里几乎什么都有方法）
nil.to_a                    # []
nil.inspect                 # "nil"

a&.length                   # 安全导航（2.3+）：nil 就返回 nil
a || "default"              # ⚠️ false 也会走默认值
b = h.fetch(:k, nil)        # 明确取默认值
h.dig(:a, :b)               # 逐层安全取值，任一层缺失返回 nil

defined?(a)
Object.new&.then { |x| x }
```

代码演示 `nil`、`&.`、`||` 与 `fetch`/`dig`。要点是：只有 `nil` 和 `false` 是假值，所以 `value || default` 会吞掉合法的 `false`；`dig` 用于嵌套 Hash/Array 的安全取值。

{{% /tab %}}

{{< /tabpane >}}

## 其他类型

这一节收拢"不属于上面任何一类、但每个语言都有、而且差异很大"的 5 个子类型：**函数与闭包、指针与引用、动态与顶层类型、日期与时间、大数与定点数**。结构和前面一样：每个子类型一张"有没有 / 叫什么"总表 + 18 个语言标签页。

### 函数与闭包

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `fn(i32) -> i32`、`|x| x + 1` | 闭包实现 `Fn`/`FnMut`/`FnOnce`；与函数指针是不同类型 |
| Swift | ✓ | `(Int) -> Int` | 函数是值；`@escaping` 逃逸、`@Sendable` 跨并发域 |
| Go | ✓ | `func(int) int` | 一等值；按引用捕获变量（1.22 起循环变量每轮新建） |
| Python | ✓ | `def`、`lambda x: x + 1` | 闭包用 cell 变量；改外层要 `nonlocal` |
| Kotlin | ✓ | `(Int) -> Int` | 高阶函数 + `inline`/`reified`；`suspend` 是另一类 |
| Java | ✓ | `Function<T,R>`、`x -> x + 1` | 函数式接口 + lambda + 方法引用 |
| C++ | ✓ | `std::function`、lambda | 捕获列表 `[&]`/`[=]`；泛型 lambda（C++14） |
| C | ✓（有限） | `int (*f)(int)` | 只有函数指针，**没有闭包**，状态要传 `void*` |
| Julia | ✓ | `f(x) = x + 1`、`x -> x + 1` | 一等值；`do` 块把函数当首参 |
| C# | ✓ | `Func<int,int>`、`x => x + 1` | lambda、方法组、表达式树、委托与事件 |
| Dart | ✓ | `int Function(int)`、`(x) => x + 1` | 闭包；`async`/`async*` 返回 `Future`/`Stream` |
| R | ✓ | `function(x) x + 1`、`\(x) x + 1` | 一等值；闭包捕获环境（`<<-` 改外层） |
| Zig | ✓（无闭包） | `*const fn (i32) i32` | 函数指针与 comptime 生成，但**没有捕获** |
| Lua | ✓ | `function(x) return x + 1 end` | 闭包捕获 upvalue；函数可返回多值 |
| TypeScript | ✓ | `(x: number) => number` | 泛型函数、重载签名、`Parameters`/`ReturnType` |
| JavaScript | ✓ | `(x) => x + 1` | 闭包 + `this` 绑定；生成器 `function*` |
| PHP | ✓ | `fn($x) => $x + 1`、`function () use ($x)` | 箭头函数自动按值捕获；`Closure::bind` |
| Ruby | ✓ | `->(x) { x + 1 }`、`proc { }` | block / proc / lambda 语义不同 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的函数是 `fn` 类型（函数指针），闭包是实现了 `Fn`/`FnMut`/`FnOnce` 的匿名类型；泛型约束 `F: Fn(..)` 是零成本，`Box<dyn Fn>` 才有动态开销。

```rust
fn add(a: i32, b: i32) -> i32 { a + b }

let fp: fn(i32, i32) -> i32 = add;        // 函数指针
let c = |x: i32| x + 1;                    // 闭包（实现 Fn）
let mut sum = 0;
let mut acc = |x: i32| { sum += x; };      // 可变闭包（FnMut）
let boxed: Box<dyn Fn(i32) -> i32> = Box::new(|x| x * 2);

fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(x) }
```

代码演示函数指针、闭包（`Fn`/`FnMut`/`FnOnce`）与 `Box<dyn Fn>`。要点是：闭包按捕获方式自动实现对应 trait；泛型参数零成本，`Box<dyn Fn>` 有分配与虚调用开销，返回闭包常需要 `move`。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的函数是一等值，闭包用 `{ }` 定义并支持 `$0` 简写；`@escaping` 表示闭包会活过函数调用，`@Sendable` 表示可跨并发域。

```swift
func add(_ a: Int, _ b: Int) -> Int { a + b }
let f: (Int, Int) -> Int = add             // 函数是值
let g = { (x: Int) -> Int in x + 1 }        // 闭包
let h = { $0 + 1 }                          // 简写参数

func run(_ body: @escaping () -> Void) { }   // 逃逸闭包要标注
let sum = [1, 2, 3].reduce(0, +)
```

代码演示函数值、闭包简写、`@escaping` 与 `reduce`。要点是：逃逸闭包必须显式标注（ARC 下要小心循环引用，用 `[weak self]`）；`@Sendable` 表示可以跨并发域传递。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的函数是一等值，可以传参、返回、放进 map；闭包按引用捕获变量（Go 1.22 起循环变量每轮新建），没有"方法引用"语法糖。

```go
var f func(int) int = func(x int) int { return x + 1 }

func apply(xs []int, fn func(int) int) []int { return nil }

func counter() func() int {           // 闭包捕获 n
    n := 0
    return func() int { n++; return n }
}

defer func() { }()                     // defer + 闭包
```

代码演示函数变量、闭包计数器与 `defer` 里的闭包。Go 没有方法引用语法糖，`http.HandlerFunc(f)` 这类转换很常见。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的函数是一等对象，支持闭包、装饰器与 `functools.partial`；闭包捕获的是变量（cell），修改外层变量要声明 `nonlocal`。

```python
def add(a, b): return a + b
f = lambda x: x + 1

def counter():                # 闭包
    n = 0
    def inc():
        nonlocal n            # 修改外层变量必须声明
        n += 1
        return n
    return inc

from functools import partial, wraps
```

代码演示 `lambda`、带 `nonlocal` 的闭包与 `functools.partial`。要点是：闭包捕获的是变量（cell）而不是值，循环里创建闭包要用默认参数固定当前值；`lambda` 只能写表达式。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的函数类型写作 `(A) -> B`，高阶函数非常常用；`inline` 能消除 lambda 的对象与调用开销，`reified` 让泛型参数在运行时可见。

```kotlin
val f: (Int) -> Int = { it + 1 }
fun apply(xs: List<Int>, fn: (Int) -> Int) = xs.map(fn)

inline fun <T> measure(block: () -> T): T = block()   // inline：省 lambda 对象
inline fun <reified T> check(x: Any) = x is T          // reified 需配合 inline

val mem = ::add                                          // 函数引用
suspend fun load(): String = ""                          // 挂起函数（协程）
```

代码演示函数类型、`inline`/`reified` 与函数引用。带接收者的函数类型是 DSL 风格的基础。

{{% /tab %}}

{{% tab header="Java" %}}

Java 用函数式接口（`Function`/`Supplier`/`Consumer`/`Predicate`）+ lambda + 方法引用表达函数值；lambda 只能捕获事实 final 的局部变量。

```java
Function<Integer, Integer> f = x -> x + 1;
BiFunction<Integer, Integer, Integer> add = Integer::sum;   // 方法引用
Supplier<String> s = () -> "x";
Consumer<String> log = System.out::println;

int base = 10;                                // 事实 final 才能捕获
Function<Integer, Integer> plus = x -> x + base;

Expression<Func<Integer, Integer>> tree = x -> x + 1;       // 表达式树
```

代码演示 `Function`/`BiFunction`/`Supplier`/`Consumer`、方法引用与"事实 final"捕获。要点是：lambda 只能捕获事实 final 的局部变量，要改状态就得用字段或 `AtomicInteger` 之类的容器。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 同时有函数指针、`std::function`（类型擦除、有开销）与带捕获列表的 lambda；`[&]` 捕获引用，逃出作用域就会悬垂。

```cpp
int (*fp)(int, int) = nullptr;                            // 函数指针
std::function<int(int)> f = [](int x) { return x + 1; };   // 类型擦除的可调用体

int n = 0;
auto g = [&](int x) { return x + n; };                     // 按引用捕获
auto h = [=]() mutable { };                                // 按值捕获
auto gen = [](auto x) { return x + x; };                    // C++14 泛型 lambda
```

`std::function` 有类型擦除开销，性能敏感处直接用模板参数或 `auto`。

{{% /tab %}}

{{% tab header="C" %}}

C 只有函数指针，**没有闭包**：需要捕获状态时必须把上下文（`void*` 或结构体指针）显式传给回调。

```c
int add(int a, int b) { return a + b; }
int (*fp)(int, int) = add;                 /* 函数指针 */

void each(int *xs, size_t n, void (*fn)(int, void *), void *ctx) {
    for (size_t i = 0; i < n; i++) fn(xs[i], ctx);   /* ctx 代替闭包 */
}

qsort(arr, n, sizeof arr[0], cmp);         /* 标准库回调 */
```

代码演示函数指针、带 `void*` 上下文的回调与 `qsort`。要点是：C 没有闭包，捕获的状态必须显式传进去；这是 C 里所有回调式 API 的标准写法。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的函数是一等值，命名函数、匿名函数（`x -> x + 1`）与 `do` 块都很常用；闭包捕获变量，要可变捕获就用 `Ref`。

```julia
f(x) = x + 1                  # 命名函数
g = x -> x + 2                 # 匿名函数

map([1, 2, 3]) do x            # do 块：函数作为第一个参数
    x * 2
end

function counter()             # 闭包
    n = Ref(0)
    () -> (n[] += 1; n[])
end
```

代码演示命名/匿名函数、`do` 块与用 `Ref` 的可变闭包。要点是：函数是一等值，闭包捕获变量；需要可变捕获就用 `Ref`（否则多个闭包共享变量会带来意外）。

{{% /tab %}}

{{% tab header="C#" %}}

C# 用委托（`Func`/`Action`/自定义 `delegate`）表示函数值，lambda 与方法组都能赋给它；表达式树能把 lambda 变成可解析的数据结构（ORM 靠它生成 SQL）。

```csharp
Func<int, int> f = x => x + 1;
Action<string> log = Console.WriteLine;

public delegate int Op(int a, int b);
Op add = (a, b) => a + b;

Expression<Func<int, int>> tree = x => x + 1;   // 表达式树（可解析）
static int Apply(Func<int, int> fn, int v) => fn(v);   // 局部函数
```

代码演示 `Func`/`Action`、自定义委托、多播委托与表达式树。要点是：委托是类型安全的函数指针；闭包捕获变量，循环变量在 C# 5 之后每轮新建。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的函数是对象，可以赋值、传参、返回；`async` 函数返回 `Future`，`async*` 函数返回 `Stream`，实现了 `call` 的对象也能像函数一样调用。

```dart
int add(int a, int b) => a + b;
var f = (int x) => x + 1;
int Function(int) g = (x) => x * 2;          // 函数类型

Future<int> load() async => 42;               // async → Future
Stream<int> ticks() async* { yield 1; }        // async* → Stream

class Adder { int call(int x) => x + 1; }      // 可调用对象
```

代码演示函数类型、闭包与 `async`/`async*`。

{{% /tab %}}

{{% tab header="R" %}}

R 的函数是一等值，闭包捕获的是环境（`<<-` 会去外层赋值）；`\(x)` 是 R 4.1+ 的匿名函数简写，公式（`~ .x`）常被当作 lambda 传给 purrr。

```r
f <- function(x) x + 1
g <- \(x) x + 2                    # R 4.1+ 简写

purrr::map(1:3, ~ .x * 2)           # 公式当 lambda

make_counter <- function() {        # 闭包捕获环境
  n <- 0
  function() { n <<- n + 1; n }
}
```

代码演示 `function`/`\(x)`、公式 lambda 与闭包环境。要点是：闭包捕获环境（`<<-` 会在外层环境里赋值）；R 还有惰性求值与非标准求值，元编程靠 `substitute`/rlang。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 只有函数指针（`*const fn (...) T`）与编译期生成的函数，**没有闭包捕获**：状态要么当参数传，要么放进结构体。

```zig
fn add(a: i32, b: i32) i32 { return a + b; }
const fp: *const fn (i32, i32) i32 = add;

const Ctx = struct { base: i32 };              // 没有闭包：显式传上下文
fn addWith(ctx: Ctx, x: i32) i32 { return ctx.base + x; }

fn makeAdder(comptime n: i32) fn (i32) i32 {    // comptime 生成特化函数
    return struct { fn f(x: i32) i32 { return x + n; } }.f;
}
```

代码演示函数指针、comptime 生成的特化函数，以及"没有闭包"时的显式上下文传递。要点是：状态必须显式传参或放进结构体，`comptime` 可以把编译期已知的值固化进生成的函数里。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的函数是一等值，闭包捕获 upvalue（多个闭包可以共享同一份状态），函数还能返回多个值。

```lua
local function add(a, b) return a + b end
local f = function(x) return x + 1 end

local function counter()          -- 闭包捕获 upvalue
  local n = 0
  return function() n = n + 1; return n end
end

local function variadic(...) return select("#", ...) end
table.sort(t, function(a, b) return a < b end)
```

代码演示函数值、upvalue 闭包与多返回值。要点是：闭包捕获的是变量本身（多个闭包可以共享状态）；`pcall`/`xpcall` 做错误处理，`coroutine` 提供协作式并发。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的函数类型包含参数、返回值与 `this`，支持泛型、重载签名与 `Parameters`/`ReturnType` 这类工具类型；箭头函数没有自己的 `this`。

```ts
function add(a: number, b: number): number { return a + b; }
const f = (x: number): number => x + 1;

type Mapper<T, U> = (x: T) => U;
function apply<T, U>(xs: T[], fn: Mapper<T, U>): U[] { return xs.map(fn); }

function overloaded(x: string): number;      // 重载签名
function overloaded(x: number): string;
function overloaded(x: any): any { return x; }
```

要点是：函数类型包含参数、返回值与 `this`；重载是"多个签名 + 一个实现"，实现签名不对外暴露；

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的函数是一等值，闭包捕获变量引用；`this` 由调用方式决定（`obj.m()`、`call`、`new`、箭头函数各不相同），生成器用 `function*`。

```js
function add(a, b) { return a + b; }
const f = (x) => x + 1;

const obj = {
  n: 1,
  inc() { this.n++; },      // this 由调用方式决定
  arrow: () => this,         // 箭头函数捕获外层 this
};

function* gen() { yield 1; }        // 生成器
async function load() { }            // async 函数返回 Promise
```

代码演示函数声明、箭头函数、`this` 绑定与生成器。要点是：`this` 由调用方式决定（箭头函数捕获外层 this），生成器函数是迭代协议的语法支持，异步函数返回 Promise。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 用 `Closure` 与箭头函数 `fn()` 表示函数值：箭头函数自动按值捕获，普通闭包要写 `use`，改外层变量用 `use (&$x)`。

```php
$f = fn($x) => $x + 1;                       // 箭头函数：按值自动捕获
$base = 10;
$g = function ($x) use ($base) { return $x + $base; };
$h = function ($x) use (&$base) { $base += $x; };   // 按引用捕获

class Adder { public function __invoke(int $x): int { return $x + 1; } }
$a = new Adder(); $a(1);                      // 可调用对象
```

代码演示箭头函数、`use` 闭包、按引用捕获与 `__invoke`。要点是：箭头函数自动按值捕获，要修改外层变量必须写 `use (&$x)`；`callable` 接受闭包、函数名字符串、`[对象, 方法]` 数组等多种形式。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的可调用对象分三种：block（隐式块）、`proc`（参数宽松、`return` 会从外层方法返回）与 `lambda`（参数严格、`return` 只返回自身）。

```ruby
def add(a, b) = a + b                  # 3.0+ 无尽方法

square = ->(x) { x * x }                # lambda：参数严格
pr = proc { |x| x + 1 }                  # proc：参数宽松

def apply(x, &block) = block.call(x)     # 捕获块
apply(3) { |v| v * 2 }

[1, 2, 3].map(&:to_s)                    # Symbol#to_proc
```

代码演示 lambda、proc、块与 `&:sym`。`proc` 参数宽松、`return` 会从外层方法返回——这是两者最容易踩的差异。

{{% /tab %}}

{{< /tabpane >}}
### 指针与引用

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓ | `&T`、`&mut T`、`*const T`、`Box`/`Rc`/`Arc` | 所有权 + 借用检查；裸指针要 `unsafe` |
| Swift | ✓（受控） | `class` + `weak`/`unowned`；`UnsafePointer` | 引用语义由 ARC 管；裸指针只在互操作里 |
| Go | ✓ | `*T`、`&v`、`new(T)` | 没有指针运算；跨类型要 `unsafe.Pointer` |
| Python | ✓（引用语义） | 一切皆引用；`id()`、`weakref`、`ctypes` | 没有指针类型 |
| Kotlin | ✗ | JVM 引用；`WeakReference` | 没有指针 |
| Java | ✗ | 引用类型 + `WeakReference`；FFM API | 没有指针运算；堆外内存用 `java.lang.foreign` |
| C++ | ✓ | `T*`、`T&`、`unique_ptr`/`shared_ptr`/`weak_ptr` | 引用必须绑定对象；智能指针管生命周期 |
| C | ✓ | `T*`、指针运算、`restrict` | 空指针/野指针/越界都是 UB |
| Julia | ✓ | `Ref{T}`、`Ptr{T}`、`GC.@preserve` | 用 `Ref`；`Ptr` 主要给 C 互操作 |
| C# | ✓（受控） | `ref`/`out`/`in`；`unsafe` + `fixed` | 托管引用 + 可选的不安全指针 |
| Dart | ✗ | GC；`dart:ffi` 的 `Pointer<T>` | 纯 Dart 没有指针 |
| R | ✓（受限） | `externalptr`、environment 引用语义 | 用户层没有指针 |
| Zig | ✓ | `*T`、`[*]T`、`[]T`、`*anyopaque` | 显式分配器；没有隐式堆分配 |
| Lua | ✗ | 表是引用；`lightuserdata` | 没有指针类型 |
| TypeScript | ✗ | 对象引用；`WeakRef` | 没有指针 |
| JavaScript | ✗ | 对象引用；`WeakRef`/`WeakMap` | 没有指针 |
| PHP | ✓（引用） | `&$x`、对象句柄 | "引用"是别名，不是指针 |
| Ruby | ✗ | 对象引用；`object_id` | 没有指针；`ObjectSpace` 可做诊断 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的引用（`&T` 共享、`&mut T` 可变）由借用检查器保证"永远有效且不冲突"，裸指针 `*const T`/`*mut T` 只能在 `unsafe` 里解引用；堆共享用 `Box`/`Rc`/`Arc`。

```rust
let mut v = 1;
let r: &i32 = &v;                // 共享引用（可同时多个）
let m: &mut i32 = &mut v;         // 可变引用（同一时刻只能一个）

let raw: *const i32 = &v;         // 裸指针：解引用要 unsafe
unsafe { println!("{}", *raw); }

let boxed = Box::new(1);                    // 堆分配、单一所有者
let rc = std::rc::Rc::new(1);               // 单线程共享
let arc = std::sync::Arc::new(1);            // 跨线程共享
let cell = std::cell::RefCell::new(1);        // 内部可变性（运行时借用检查）
```

代码演示共享引用与可变引用的规则、裸指针必须放进 `unsafe`，以及 `Box`/`Rc`/`Arc`/`RefCell` 的定位。要点是：引用由借用检查器保证有效且非空；`Rc`/`Arc` 是共享所有权（要可变就配 `RefCell`/`Mutex`），循环引用要用 `Weak` 打破。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的类实例是引用（由 ARC 管理生命周期），`weak`/`unowned` 用来表达不持有或弱持有；裸指针（`Unsafe*Pointer`）只在 C 互操作与底层优化里出现。

```swift
class Node { var next: Node? }
let a = Node()
let b = a                       // 同一个对象（引用语义）

weak var w = a                  // 弱引用：对象释放后自动变 nil
unowned let u = a               // 非持有引用：对象释放后访问会崩

let buf = UnsafeMutablePointer<Int>.allocate(capacity: 3)
buf.deallocate()
```

代码演示类的引用语义、`weak`/`unowned` 的区别与裸指针的分配/释放。要点是：ARC 管生命周期，`weak` 在对象释放后自动变 nil；值类型没有引用，`inout` 参数只是临时的可变引用。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `*T` 可以取地址（`&v`）与解引用（`*p`），指针是普通值、可以为 nil，但**没有指针运算**，跨类型转换必须走 `unsafe.Pointer`。

```go
v := 1
p := &v                  // *int
*p = 2

type Node struct{ Next *Node }
head := &Node{}
head.Next = &Node{}

// 没有指针运算；跨类型必须走 unsafe.Pointer
```

代码演示取地址、解引用、指针字段，以及"没有指针运算"这一事实。要点是：指针是普通值、可以为 nil、可以比较地址；跨类型转换必须走 `unsafe.Pointer`，方法接收者用 `*T` 才能修改结构体。

{{% /tab %}}

{{% tab header="Python" %}}

Python 里变量是"名字 → 对象"的绑定，赋值不会复制对象（引用语义）；没有指针类型，弱引用用 `weakref`，真指针要 `ctypes`/`cffi`。

```python
a = [1, 2]
b = a                  # 同一个 list
b.append(3)
print(a)               # [1, 2, 3]

import copy
c = copy.deepcopy(a)     # 深拷贝

import weakref
wr = weakref.ref(a)      # 弱引用：不阻止回收
id(a)                    # 对象标识（CPython 里是地址）
```

代码演示赋值共享对象、`copy.deepcopy`、`weakref` 与 `id()`。不可变对象（int/str/tuple）看起来像值语义，本质上仍是共享引用。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin（JVM）上没有指针，对象变量就是引用：`===` 比身份、`==` 比值；缓存场景用 `WeakReference`/`SoftReference`。

```kotlin
class Node(var next: Node?)
val a = Node(null)
val b = a                     // 同一个对象
a === b                       // true：身份比较

val weak = java.lang.ref.WeakReference(a)
val soft = java.lang.ref.SoftReference(a)
```

缓存里不阻止回收的对象要用弱引用。

{{% /tab %}}

{{% tab header="Java" %}}

Java 只有引用类型（可以为 null），没有指针运算；`==` 比身份、`equals` 比值，弱引用/软引用/虚引用用于缓存与资源清理，堆外内存用 FFM API（Java 22+ 正式）。

```java
Object a = new Object();
Object b = a;                          // 同一个对象
System.identityHashCode(a);

WeakReference<Object> w = new WeakReference<>(a);
PhantomReference<Object> p = new PhantomReference<>(a, new ReferenceQueue<>());

// 堆外内存（Java 22+ 正式）：java.lang.foreign
```

代码演示 `==` 与 `equals` 的差别、`identityHashCode` 与弱引用/虚引用。堆外内存与 C 互操作用 FFM API（Java 22+ 正式）而不是 `Unsafe`。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 同时有可空可重绑定的指针 `T*` 与必须绑定对象、不可重绑定的引用 `T&`；生命周期由智能指针（`unique_ptr`/`shared_ptr`/`weak_ptr`）或作用域管理。

```cpp
int v = 1;
int* p = &v;                  // 指针：可为空、可重新指向
int& r = v;                   // 引用：必须绑定对象、不可重绑定

auto up = std::make_unique<int>(1);    // 独占所有权
auto sp = std::make_shared<int>(1);    // 共享所有权（引用计数）
std::weak_ptr<int> wp = sp;            // 弱引用：不增加计数

std::span<int> s{p, 1};                // C++20 视图（指针 + 长度）
```

要点是：引用不能为空但可以悬垂；`span`/`string_view` 是非拥有视图，同样会悬垂。

{{% /tab %}}

{{% tab header="C" %}}

C 的指针是核心工具：可以取地址、做算术、多级间接，但空指针、野指针、释放后使用、越界全是未定义行为，所有权完全靠程序员。

```c
int v = 1;
int *p = &v;
int **pp = &p;                /* 多级指针 */

int arr[3] = {1, 2, 3};
int *q = arr;                 /* 数组退化成指针 */
*(q + 2);                     /* 指针运算 = arr[2] */

char *s = malloc(16);
free(s);
s = NULL;                     /* 释放后置空，防野指针 */
```

代码演示多级指针、指针运算与"free 之后置 NULL"。要点是：空指针、野指针、释放后使用、越界全是 UB；`restrict` 帮编译器优化，并发用 `_Atomic`/`stdatomic.h`。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 有 GC，用户层用 `Ref{T}` 表达"可变的单值引用"；`Ptr{T}`/`unsafe_load` 主要给 C 互操作，`GC.@preserve` 保证对象在调用期间不被回收。

```julia
r = Ref(1)                 # 可变引用容器
r[] = 2
r[]                        # 2

p = Ptr{Int}(C_NULL)        # C 指针（主要给互操作）
GC.@preserve obj begin      # 保证期间对象不被回收
    # 使用 pointer(obj)
end
```

代码演示 `Ref` 的读写、`Ptr` 与 `GC.@preserve`。要点是：用户层用 `Ref` 表达可变引用（闭包里也常用）；

{{% /tab %}}

{{% tab header="C#" %}}

C# 默认是托管引用（`ref`/`out`/`in` 是参数传递语义，`Span<T>` 是安全视图）；真正的指针只在 `unsafe` 块里可用，且需要显式开启。

```csharp
int v = 1;
ref int r = ref v;                        // 托管引用（ref 局部变量）

void Fill(out int x) { x = 5; }            // out：必须赋值
void Log(in Span<byte> data) { }            // in：只读引用

unsafe {
    int* p = stackalloc int[4];            // 不安全代码：指针
    fixed (byte* q = bytes) { }
}
```

代码演示 `ref` 局部变量、`out`/`in` 参数与 `unsafe` 指针。原生互操作推荐 `LibraryImport`（源生成）而不是老的 `DllImport` + 手工封送。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 没有指针：对象引用由 GC 管理，身份用 `identical` 比较；只有 `dart:ffi` 的 `Pointer<T>` 用于原生互操作。

```dart
class Node { Node? next; }
var a = Node();
var b = a;                  // 同一个对象
identical(a, b);             // true

import 'dart:ffi';           // 原生互操作：Pointer<T>
```

代码演示对象共享与 `identical`，以及 FFI 的 `Pointer`。要点是：纯 Dart 没有指针、GC 管生命周期；

{{% /tab %}}

{{% tab header="R" %}}

R 用户层没有指针；`environment` 是唯一的引用语义容器，`externalptr` 用于 C 互操作，向量/列表则遵循写时复制。

```r
e <- new.env()             # environment：引用语义
f <- e
assign("x", 1, envir = f)
get("x", envir = e)        # 1：两个名字指向同一环境

p <- new("externalptr")    # 外部指针（C 互操作）
tracemem(x)                # 观察向量是否被复制
```

向量/列表是写时复制——看起来像传值，实际只在修改时复制。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的指针类型区分单值 `*T`、多值 `[*]T` 与切片 `[]T`（指针 + 长度），类型擦除用 `*anyopaque`；所有堆分配都必须显式传 allocator 并用 `defer` 释放。

```zig
var v: i32 = 1;
const p: *i32 = &v;
p.* = 2;                          // 解引用

const many: [*]i32 = undefined;    // 多指针（可做指针运算）
const slice: []i32 = undefined;     // 切片：指针 + 长度
const any: *anyopaque = p;           // 类型擦除指针

var gpa = std.heap.GeneralPurposeAllocator(.{}){};
defer _ = gpa.deinit();
const buf = try gpa.allocator().alloc(u8, 16);
defer gpa.allocator().free(buf);
```

代码演示单值/多值/切片指针的区别与显式 allocator 的分配释放。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 里表、函数、线程是引用语义，数值/布尔/字符串是值语义；没有指针类型，与 C 交互才用 `lightuserdata`/`userdata`。

```lua
local a = {}
local b = a           -- 表是引用语义
b.x = 1
print(a.x)            -- 1

local n = 1
local m = n           -- 数值是值语义
m = 2
print(n)              -- 1
```

代码演示表/函数的引用语义与数值/字符串的值语义。弱表（`__mode = "k"`/`"v"`）是 Lua 的弱引用手段。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的对象/数组/函数是引用，原始值是值；没有指针，不阻止回收的引用用 `WeakRef`/`WeakMap`/`WeakSet`。

```ts
const a = { x: 1 };
const b = a;                   // 同一个对象
const c = { ...a };             // 浅拷贝
const d = structuredClone(a);    // 深拷贝（ES2022）

const ref = new WeakRef(a);      // 弱引用（ES2021）
const wm = new WeakMap<object, number>();
```

代码演示对象引用、浅拷贝/深拷贝与 `WeakRef`。要点是：对象是引用、原始值是值；`structuredClone` 不能克隆函数/DOM 节点/`WeakMap`，浅拷贝只复制第一层。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的引用语义只适用于对象，`===` 比较引用身份；弱引用有 `WeakRef` 与 `WeakMap`，深拷贝用 `structuredClone`（ES2022）。

```js
const a = { x: 1 };
const b = a;                    // 同一个对象
const c = { ...a };              // 浅拷贝
const d = structuredClone(a);     // 深拷贝（Node 17+/现代浏览器）

const ref = new WeakRef(a);
const wm = new WeakMap();         // 键必须是对象
```

要点是：`===` 比较引用身份；GC 时机不可控，`FinalizationRegistry` 不能用来做关键资源清理。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `&` 创建的是"别名"（引用）而不是指针，没有地址与指针运算；对象变量保存句柄（赋值共享同一对象），数组是值类型（写时复制）。

```php
$a = 1;
$b = &$a;                // 引用：同一份数据的两个名字
$b = 2;
echo $a;                  // 2

function inc(int &$n): void { $n++; }

$o1 = new stdClass();
$o2 = $o1;                // 对象按句柄共享
$o3 = clone $o1;           // 浅拷贝
```

代码演示 `&` 别名、引用参数与对象句柄共享。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 里一切皆对象、变量都是引用；`equal?` 比身份、`==` 比值、`eql?` 用于 Hash 键，`object_id` 与 `ObjectSpace` 可做诊断。

```ruby
a = [1, 2]
b = a                  # 同一个对象
b << 3
p a                     # [1, 2, 3]

a.object_id
a.equal?(b)             # true：身份比较
a == b                  # true：值比较

require "weakref"
WeakRef.new(a)
```

代码演示数组共享、`object_id`/`equal?`/`==` 的区别与 `WeakRef`。

{{% /tab %}}

{{< /tabpane >}}
### 动态与顶层类型

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓（受限） | `dyn Trait`、`Any`、泛型 | 以静态为主；`dyn`/`Any` 是受控的逃生舱 |
| Swift | ✓ | `Any`、`AnyObject`、`as?`/`is` | 编译期类型为主，运行时转换有开销 |
| Go | ✓ | `any`（=`interface{}`）、类型断言、`reflect` | 空接口是"万物类型"；反射能查类型与字段 |
| Python | ✓ | 一切动态：`Any`、`getattr`/`hasattr`、`__dict__` | 运行时决定一切 |
| Kotlin | ✓ | `Any`、`Any?`、`is`/`as?`、反射 | `Any` 是顶层类型，`Any?` 表示可空 |
| Java | ✓ | `Object`、`Class<T>`、反射 API | `Object` 是顶层类型；反射有性能与模块限制 |
| C++ | ✓ | `std::any`、`std::variant`、RTTI（`typeid`/`dynamic_cast`） | 类型擦除要显式选一种机制 |
| C | ✓ | `void*`、`_Generic` | 类型信息全靠程序员维护 |
| Julia | ✓ | 类型是一等值：`typeof`、`isa`、`Any` | 动态 + 多分派共存 |
| C# | ✓ | `object`、`dynamic`、反射 | `dynamic` 走 DLR，运行时绑定 |
| Dart | ✓ | `dynamic`、`Object?`、`is`/`as` | `dynamic` 关闭静态检查 |
| R | ✓ | 一切动态：`class()`、`attributes()`、`eval()` | 行为由运行时属性决定 |
| Zig | ✓（编译期） | `anytype`、`*anyopaque`、`@typeInfo` | 没有运行时反射式动态类型 |
| Lua | ✓ | 值自带类型：`type()`、元表 | 完全动态 |
| TypeScript | ✓ | `any`/`unknown`/`never`/`object` | 编译期类型；`unknown` 是安全的顶层类型 |
| JavaScript | ✓ | 一切动态：`typeof`、`instanceof` | 完全动态 |
| PHP | ✓ | `mixed`、`gettype`、反射 | 变量本身没有类型声明 |
| Ruby | ✓ | 一切动态：`class`、`respond_to?`、`send` | 完全动态 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 以静态类型为主，动态能力是受控的：`dyn Trait` 提供虚表派发，`Any` + `downcast_ref` 提供类型擦除与还原，没有运行时反射。

```rust
let x: Box<dyn std::fmt::Debug> = Box::new(1);      // 动态派发
let y = &1 as &dyn std::any::Any;                    // 类型擦除
y.downcast_ref::<i32>();                             // 还原具体类型

fn dump<T: std::fmt::Debug>(v: T) { }                // 泛型（静态）
```

代码演示 `dyn Trait`、`Any` + `downcast_ref` 与泛型的对比。要点是：动态派发是受控的（虚表 + 类型擦除），没有运行时反射；需要"看类型结构"的场景通常用过程宏在编译期生成代码。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的顶层类型是 `Any`（任何值，会装箱）与 `AnyObject`（任何类实例），运行时检查用 `as?`/`is`，只读反射用 `Mirror`。

```swift
let any: Any = 1
if let n = any as? Int { print(n) }        // 可选转换
any is Int                                  // 类型检查

let obj: AnyObject = NSString(string: "x")

Mirror(reflecting: any).children            // 反射（只读）
type(of: any)                                // 运行时类型
```

代码演示 `Any` 装箱、`as?`/`is` 检查与 `Mirror` 反射。要点是：`Any` 会装箱、`AnyObject` 只能装类实例；`Mirror` 是只读反射，真正的元编程靠宏（Swift 5.9+）。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的顶层类型是空接口 `any`（=`interface{}`），任何值都能装进去；运行时手段是类型断言、`type switch` 与 `reflect`（灵活但有性能与安全代价）。

```go
var v any = 42                 // any = interface{}
n, ok := v.(int)               // 类型断言
switch x := v.(type) {         // 类型开关
case int: _ = x
case string: _ = x
}

t := reflect.TypeOf(v)          // 反射
val := reflect.ValueOf(v)
t.Kind(); t.Name()
```

要点是：`any` 会有接口装箱开销；断言的安全形式是 `v, ok := x.(T)`；反射能读写字段、调用方法，但慢且会破坏类型安全。

{{% /tab %}}

{{% tab header="Python" %}}

Python 完全动态：变量的类型由运行时对象决定，属性/方法/类都可以在运行时查询与修改，`Any` 只是给类型检查器的"放弃检查"标记。

```python
x = 42
type(x)                     # int（运行时类型）
isinstance(x, int)

getattr(obj, "name", None)   # 动态属性访问
hasattr(obj, "name")
obj.__dict__                 # 实例属性字典（普通对象）

from typing import Any, cast
def f(v: Any) -> int: return cast(int, v)   # 注解不强制
```

代码演示 `type()`/`isinstance`、`getattr`/`hasattr` 与 `__dict__`。要点是：一切都在运行时决定；`Any` 只是"放弃检查"标记；反射与元编程靠 `getattr`/`inspect`/`type()` 动态建类。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的根类型是 `Any`（`Any?` 才可空），`is` 检查后编译器会做智能转换，反射通过 `KClass`/`KFunction`（JVM 上需要 `kotlin-reflect`）。

```kotlin
val x: Any = 42                 // Any 是顶层类型
val y: Any? = null               // Any? 可空

if (x is Int) println(x + 1)     // 智能转换：这里 x 变成 Int
val n = x as? Int                 // 安全转换（失败给 null）

x::class                          // KClass：反射入口
x::class.members
```

代码演示 `Any`/`Any?`、`is` 智能转换、`as?` 与 `KClass` 反射。要点是：`is` 检查后编译器自动收窄类型；反射在 JVM 上需要 `kotlin-reflect` 依赖，能用静态手段就别上反射。

{{% /tab %}}

{{% tab header="Java" %}}

Java 的根类型是 `Object`，任何引用类型都能装进去（值类型需要装箱）；反射（`Class`/`Method`）能在运行时查类型、调方法、读字段。

```java
Object o = 42;                     // Object 是顶层类型
if (o instanceof Integer i) { }     // 模式匹配（16+）
Integer n = (Integer) o;            // 强转（失败抛 ClassCastException）

Class<?> c = o.getClass();
c.getMethods();
c.getDeclaredFields();

var boxed = Integer.valueOf(42);    // 装箱
```

代码演示 `Object`、`instanceof` 模式、强转与反射入口。要点是：`Object` 能装任何引用类型（基本类型要装箱）；反射可以查类型、调方法，但绕过编译期检查，模块系统下还可能被拒绝访问。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 没有统一的动态类型，要按场景选：`std::any`（任意单值）、`std::variant`（已知备选集合）、多态基类 + RTTI（`typeid`/`dynamic_cast`）。

```cpp
#include <any>
#include <variant>

std::any a = 42;                              // 任意类型（类型擦除）
std::any_cast<int>(a);                         // 取回（失败抛 bad_any_cast）
a.type() == typeid(int);

std::variant<int, std::string> v = "x";         // 已知备选集合
std::holds_alternative<std::string>(v);

if (auto* p = dynamic_cast<Derived*>(base)) { }  // RTTI 向下转换
```

`-fno-rtti` 会禁用后两种。

{{% /tab %}}

{{% tab header="C" %}}

C 的"动态"就是 `void*`：类型信息完全由程序员维护；`_Generic`（C11）能在编译期做类型分派，但运行时没有任何反射。

```c
void *any = &value;              /* 万物皆可指 */

_Generic(x, int: 1, double: 2, default: 0)   /* C11：编译期类型分派 */

/* 运行时没有类型信息，只能自己带 tag */
struct tagged { enum { I, D } tag; union { int i; double d; } u; };
```

代码演示 `void*` 与 `_Generic`。要点是：`void*` 丢掉类型信息，解引用前必须自己知道正确类型；

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 里类型是一等值：`typeof`、`isa`、`fieldnames` 在运行时可用，"动态"与"多分派 + 编译期特化"共存。

```julia
x = 42
typeof(x)            # Int64
x isa Integer        # true

f(x) = x + 1          # 参数类型不限
f(x::Int) = x + 1      # 更具体的方法优先

fieldnames(typeof(x))
```

要点是：类型可以查询、比较、当参数传；动态与多分派共存，`Any` 容器会装箱（能标注具体类型就别写 `Any`）。

{{% /tab %}}

{{% tab header="C#" %}}

C# 的根类型是 `object`，`dynamic` 关键字走 DLR 在运行时绑定成员（编译期不检查）；反射 + 源生成器是更可控的替代方案。

```csharp
object o = 42;                       // object 是顶层类型
if (o is int n) { }                   // 模式匹配

dynamic d = 42;                       // dynamic：运行时绑定（DLR）
d.Foo();                              // 编译通过，运行时可能抛异常

Type t = o.GetType();
t.GetMethods();

var s = (string)o;                    // 显式转换（失败抛 InvalidCastException）
```

代码演示 `object`、`is` 模式、`dynamic` 与反射。要点是：`dynamic` 走 DLR 运行时绑定（编译期不检查、性能更差）；

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `dynamic` 会关闭静态检查（成员缺失变成运行时 `NoSuchMethodError`），`Object?` 才是安全的顶层类型，用之前必须收窄。

```dart
dynamic d = 42;                // 关闭静态检查
d.foo();                        // 编译通过，运行时可能抛 NoSuchMethodError

Object? o = 42;                 // 更安全：用之前要检查
if (o is int) print(o + 1);      // 智能转换

var list = <dynamic>[];          // 混杂类型容器
```

代码演示 `dynamic` 的运行时行为与 `Object?` + `is` 的安全写法。`Object?` 才是安全的顶层类型，用前必须收窄。

{{% /tab %}}

{{% tab header="R" %}}

R 里一切类型都是运行时属性（`class()`/`attributes()`/`typeof()`），`eval`/`quote`/`substitute` 支持非标准求值，S3/S4 的分派就建立在 `class` 上。

```r
x <- 42
class(x)              # "numeric"
typeof(x)             # "double"
attributes(x)

get("x")               # 按名字取值
eval(quote(1 + 1))      # 求值表达式
do.call("sum", list(1, 2))

structure(1, class = "my_type")   # 运行时加 class 属性
```

代码演示 `class`/`typeof`/`attributes`、`eval(quote(...))` 与 `structure()`。要点是：类型与行为都是运行时属性；

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的动态能力分两层：`anytype` + `@typeInfo` 是编译期反射（零开销、单态化），运行时只有手写的 `*anyopaque` + vtable。

```zig
fn dump(x: anytype) void {              // comptime 泛型
    const T = @TypeOf(x);
    const info = @typeInfo(T);          // 编译期反射
    _ = info;
}

const ptr: *anyopaque = &value;          // 运行时类型擦除
const vtable = struct {                    // 手写动态派发
    print: *const fn (*anyopaque) void,
};
```

代码演示 `anytype` + `@typeInfo` 的编译期反射与 `*anyopaque` 的运行时时类型擦除。要点是：编译期反射零开销、每个组合单态化；运行时的"动态类型"只有手写 vtable 这一种形式。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 里每个值自带类型标签（`type()` 可查），变量没有类型；元表能拦截索引、赋值、调用与运算，是"动态行为"的核心机制。

```lua
print(type(42))          -- number
print(type("x"))         -- string
print(type({}))          -- table
print(type(print))       -- function

local mt = { __index = function(_, k) return "?" end }
setmetatable(t, mt)       -- 元表可以模拟"动态行为"

debug.getinfo(1)
```

代码演示 `type()`、元表拦截与 `debug.getinfo`。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的类型层面有 `any`（放弃检查）、`unknown`（安全顶层类型，用前必须收窄）、`never`（不可能值）与 `object`；运行时全部擦除。

```ts
let a: any;             // 放弃检查（危险）
let b: unknown;         // 安全顶层类型：必须先收窄
let c: never;           // 不可能出现的值（穷尽检查）
let d: object;          // 任意非原始值

if (typeof b === "string") b.toUpperCase();

type T = Extract<string | number, string>;   // 类型层面的"运算"
```

代码演示 `any`/`unknown`/`never`/`object` 与 `typeof` 收窄。要点是：`any` 会污染整个表达式，`unknown` 才是安全的"暂时不知道"；类型编译后全部擦除，运行时校验要另写或用 schema 库。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 完全动态：`typeof`/`instanceof`/`constructor` 是运行时检查手段（注意 `typeof null === "object"` 这个历史遗留）。

```js
typeof 42;         // "number"
typeof "x";        // "string"
typeof {};         // "object"
typeof null;       // "object" ← 历史遗留
typeof undefined;  // "undefined"
typeof (() => {}); // "function"

[] instanceof Array;
"x".constructor === String;
```

代码演示 `typeof`/`instanceof`/`constructor` 与 `Array.isArray`。要点是：`typeof null === "object"` 是历史遗留；判数组必须用 `Array.isArray`，其他形状检查要自己在运行时写。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的变量没有类型声明，类型由值决定；`mixed`（8.0+）是显式的"任意类型"，反射与 `__get`/`__call` 提供元编程能力。

```php
$x = 42;                     // 变量无类型
gettype($x);                  // "integer"
is_int($x);

$o = new stdClass();
$o->any = 1;                  // 动态属性

(new ReflectionClass($o))->getProperties();   // 反射

function f(mixed $v): mixed { return $v; }     // PHP 8.0 的 mixed
```

代码演示 `gettype`/`is_int`、动态属性、反射与 `mixed`。要点是：变量本身没有类型，参数/返回值注解是可选约束；反射能查类结构、改属性、调用方法。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 完全动态：`class` 给出类型，`respond_to?` 做能力检查，`send`/`method_missing`/`define_method` 是元编程的核心。

```ruby
1.class              # Integer
"x".is_a?(String)
obj.respond_to?(:name)      # 鸭子类型检查

obj.send(:private_method)    # 绕过访问控制调用
obj.define_singleton_method(:foo) { 1 }   # 运行时加方法

Object.const_get(:String)
```

代码演示 `class`/`is_a?`/`respond_to?`、`send` 与 `define_singleton_method`。要点是：一切动态——类型由 `class` 回答、能力由 `respond_to?` 回答；

{{% /tab %}}

{{< /tabpane >}}
### 日期与时间

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓（仅时间点） | `SystemTime`、`Instant`；日历用 chrono/time | 标准库只有时间点与单调时钟 |
| Swift | ✓ | `Date`、`Calendar`、`DateComponents`、`Duration` | Foundation 提供日历与时区 |
| Go | ✓ | `time.Time`、`time.Duration`、`time.LoadLocation` | 时间点带时区；格式模板是参考时间 |
| Python | ✓ | `datetime`、`zoneinfo`、`timedelta` | 注意 naive 与 aware 的区别 |
| Kotlin | ✓ | `java.time`；多平台用 kotlinx-datetime | `Instant`/`LocalDate`/`Duration`/`ZoneId` |
| Java | ✓ | `java.time`（`Instant`/`LocalDate`/`ZonedDateTime`） | Java 8 起取代 `Date`/`Calendar` |
| C++ | ✓ | `<chrono>`；C++20 有日历（`year_month_day`） | `system_clock` 与 `steady_clock` 分工明确 |
| C | ✓ | `time_t`、`struct tm`、`clock_gettime` | 无日历库；`localtime_r` 才是线程安全版 |
| Julia | ✓ | `Dates` 标准库（`Date`/`DateTime`/`Period`） | 与语言一起发布的 stdlib |
| C# | ✓ | `DateTime`、`DateTimeOffset`、`TimeSpan`、`DateOnly`、`TimeOnly` | 推荐 `DateTimeOffset` |
| Dart | ✓ | `DateTime`（UTC/本地）、`Duration`、`Stopwatch` | 无时区数据库；格式化用 intl |
| R | ✓ | `Date`、`POSIXct`/`POSIXlt`、`difftime` | 时区参数容易漏；常用 lubridate |
| Zig | ✓ | `std.time.Instant`、`nanoTimestamp`、`epoch` | 标准库无日历格式化 |
| Lua | ✓ | `os.time`、`os.date`、`os.clock` | 无时区库 |
| TypeScript | ✓ | `Date`、`Intl.DateTimeFormat`；`Temporal` 新标准 | `Date` 可变、月份从 0 开始 |
| JavaScript | ✓ | 同上 | 同上 |
| PHP | ✓ | `DateTimeImmutable`、`DateTimeZone`、`DateInterval` | 推荐不可变版本；业务常用 Carbon |
| Ruby | ✓ | `Time`、`Date`/`DateTime`（date 库） | `Time` 带时区信息 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 标准库只提供时间点：`SystemTime`（墙钟，可能被系统调时影响）与 `Instant`（单调，用于计时）；日历、时区、格式化要引 chrono 或 time。

```rust
use std::time::{Duration, Instant, SystemTime};

let now = SystemTime::now();               // 墙钟时间（可回拨）
let t0 = Instant::now();                    // 单调时钟（计时用）
let d = Duration::from_millis(1500);
t0.elapsed();

// 日历/时区不在标准库：用 chrono 或 time
// chrono::Local::now().format("%Y-%m-%d %H:%M:%S")
```

代码演示 `SystemTime`（墙钟）与 `Instant`（单调）以及 `Duration`。要点是：测量耗时一律用 `Instant`（系统调时不会影响它）；

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 用 `Date` 表示时间点，`Calendar`/`DateComponents` 做日历运算，`Duration`（5.7+）表示时长，格式化和解析用 `DateFormatter`/`ISO8601DateFormatter`。

```swift
let now = Date()                                  // 时间点
let cal = Calendar.current
let comps = cal.dateComponents([.year, .month, .day], from: now)
let tomorrow = cal.date(byAdding: .day, value: 1, to: now)
let d = Duration.seconds(90)                       // 5.7+

let f = ISO8601DateFormatter()
f.string(from: now)
```

要点是：`Date` 只是时间点，日期加减必须经过 `Calendar`（否则夏令时/闰月会算错）；`DateFormatter` 创建昂贵，应该缓存复用。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `time.Time` 同时带时区与（可选的）单调时钟读数，`time.Duration` 是纳秒整数；格式化/解析用的是固定的参考时间 `2006-01-02 15:04:05`。

```go
now := time.Now()                          // 带时区 + 单调时钟读数
t, err := time.Parse(time.RFC3339, "2026-09-18T10:00:00+08:00")
loc, _ := time.LoadLocation("Asia/Shanghai")
local := now.In(loc)
d := 90 * time.Minute
elapsed := time.Since(now)                  // 单调时钟

now.Format("2006-01-02 15:04:05")            // 参考时间模板
```

代码演示 `time.Now`（带时区与单调读数）、`time.Parse` 与参考时间格式化模板。`time.Time` 携带时区，计时用 `time.Since` 比手算更稳。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `datetime` 分 naive（无时区）与 aware（带时区）两种，跨系统传输必须用 aware + ISO 8601；时区用 `zoneinfo`，时长用 `timedelta`。

```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

naive = datetime.now()                                  # 无时区（危险）
aware = datetime.now(timezone.utc)                       # 有时区
sh = datetime.now(ZoneInfo("Asia/Shanghai"))
later = aware + timedelta(hours=1)

aware.isoformat()                                        # 序列化首选
datetime.fromisoformat("2026-09-18T10:00:00+08:00")
```

naive 与 aware 不能安全混算；时区用 `zoneinfo`（而不是老的 `pytz` 用法），`datetime` 本身是不可变的。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 在 JVM 上直接使用 `java.time`（`Instant`/`LocalDate`/`ZonedDateTime`/`Duration`），Kotlin 多平台项目用 `kotlinx-datetime`。

```kotlin
import java.time.*

val now = Instant.now()
val date = LocalDate.now(ZoneId.of("Asia/Shanghai"))
val d = Duration.ofMinutes(90)
val zoned = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"))
val period = Period.ofDays(7)
```

要点是：JVM 上直接用 `java.time`（不可变、线程安全）；

{{% /tab %}}

{{% tab header="Java" %}}

Java 8 起统一用 `java.time`：`Instant`（时间点）、`LocalDate`（无时区日期）、`ZonedDateTime`（带时区）、`Duration`/`Period`（时长），新代码不要再用 `Date`/`Calendar`。

```java
Instant now = Instant.now();
LocalDate today = LocalDate.now(ZoneId.of("Asia/Shanghai"));
ZonedDateTime z = ZonedDateTime.now();
Duration d = Duration.ofMinutes(90);
Period p = Period.ofDays(7);

DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").format(z);
```

要点是：新代码一律用 `java.time`，`Date`/`Calendar` 已过时且可变；时间点用 `Instant`、无时区日期用 `LocalDate`、带时区用 `ZonedDateTime`。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 用 `<chrono>` 表示时间点与时长，`system_clock` 是墙钟、`steady_clock` 是单调时钟；C++20 起标准库还有日历类型（`year_month_day`）。

```cpp
#include <chrono>
using namespace std::chrono;

auto now = system_clock::now();                     // 墙钟
auto t0 = steady_clock::now();                       // 单调（计时）

auto today = floor<days>(now);
year_month_day ymd{today};                            // C++20 日历

std::println("{:%Y-%m-%d}", ymd);
```

代码演示 `system_clock` 与 `steady_clock`，以及 C++20 的 `year_month_day`。要点是：墙钟与单调时钟用途不同、千万别混用；C++20 才把日历放进标准库，更早的项目用 `std::tm` 或第三方库。

{{% /tab %}}

{{% tab header="C" %}}

C 用 `time_t`（时间点）与 `struct tm`（拆开的日历字段）配合 `strftime`；计时要用 `clock_gettime(CLOCK_MONOTONIC)`，`localtime_r` 才是线程安全版本。

```c
#include <time.h>

time_t now = time(NULL);
struct tm tmv;
localtime_r(&now, &tmv);                    /* 线程安全版本 */
strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S", &tmv);

struct timespec ts;
clock_gettime(CLOCK_MONOTONIC, &ts);         /* 计时用单调时钟 */
```

要点是：`localtime`/`gmtime` 返回静态缓冲区（线程里要用 `_r` 版本）；计时用单调时钟，格式化用 `strftime`。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的标准库 `Dates` 提供 `Date`、`DateTime`、`Period` 与格式化；时区支持有限，复杂时区用 `TimeZones.jl`。

```julia
using Dates

now()                                       # DateTime（本地）
Date(2026, 9, 18)
DateTime(2026, 9, 18, 10, 0)
Dates.format(now(), "yyyy-mm-dd HH:MM:SS")
today() + Day(1) - Hour(3)                   # Period 运算

DateTime("2026-09-18T10:00:00", dateformat"yyyy-mm-ddTHH:MM:SS")
```

要点是：`Date` 只有日期、`DateTime` 精确到毫秒；

{{% /tab %}}

{{% tab header="C#" %}}

C# 用 `DateTimeOffset`（带 UTC 偏移，推荐）或 `DateTime` 表示时间点，`TimeSpan` 表示时长，.NET 6+ 还有 `DateOnly`/`TimeOnly`，计时用 `Stopwatch`。

```csharp
DateTimeOffset now = DateTimeOffset.UtcNow;          // 推荐：带偏移
DateTime local = DateTime.Now;
TimeSpan d = TimeSpan.FromMinutes(90);
DateOnly day = DateOnly.FromDateTime(DateTime.Today);   // .NET 6+
TimeOnly time = TimeOnly.FromDateTime(DateTime.Now);

var tz = TimeZoneInfo.FindSystemTimeZoneById("Asia/Shanghai");
var sw = Stopwatch.StartNew();                        // 单调计时
```

`DateTime.Kind` 处理不当会引入时区 bug。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `DateTime` 分本地与 UTC 两种（`isUtc`），`difference` 得到 `Duration`，`Stopwatch` 做单调计时；没有内建时区数据库，格式化用 `intl`。

```dart
var now = DateTime.now();                  // 本地时区
var utc = DateTime.now().toUtc();
var d = DateTime.utc(2026, 9, 18, 10, 0);
var diff = d.difference(now);               // Duration
var sw = Stopwatch()..start();               // 单调计时

// 格式化用 intl 包的 DateFormat
```

要点是：`DateTime` 分本地与 UTC（`isUtc`），没有内建时区数据库；跨时区显示用 `intl` 或交给服务端转换。

{{% /tab %}}

{{% tab header="R" %}}

R 的时间分两套：`Date`（天）与 `POSIXct`/`POSIXlt`（秒），`difftime` 算时间差；`tz` 参数非常容易漏，业务代码常用 `lubridate`。

```r
as.Date("2026-09-18")
Sys.time()                                          # POSIXct（时间点）
as.POSIXct("2026-09-18 10:00:00", tz = "Asia/Shanghai")
format(Sys.time(), "%Y-%m-%d %H:%M:%S")
difftime(Sys.time(), Sys.time() - 3600, units = "mins")

lubridate::ymd_hms("2026-09-18 10:00:00", tz = "Asia/Shanghai")
```

代码演示 `as.Date`、带 `tz` 的 `POSIXct` 与 `difftime`。要点是：`tz` 参数漏了就会落到系统时区；`Date` 与 `POSIXct` 是两套类型、混用容易出错；`lubridate` 能让解析与算术更直观。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 标准库给的是纳秒时间戳、单调计时器与纪元换算（`std.time`），**没有**日历、时区与格式化，需要就自己写或引第三方。

```zig
const ns = std.time.nanoTimestamp();               // i128 纳秒
var timer = try std.time.Timer.start();             // 单调计时
const elapsed = timer.read();

const epoch = std.time.epoch.EpochSeconds{ .secs = 0 };
const day = epoch.getEpochDay();
const yd = day.calculateYearDay();
```

代码演示纳秒时间戳、`std.time.Timer` 与 `std.time.epoch` 的纪元换算。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 用 `os.time`/`os.date` 做基础日期处理（`!` 前缀表示 UTC），`os.clock` 是 CPU 时间而不是墙钟；没有时区数据库。

```lua
print(os.time())                     -- Unix 秒
print(os.date("%Y-%m-%d %H:%M:%S"))   -- 本地时间
print(os.date("!%Y-%m-%d"))           -- UTC（! 前缀）
print(os.clock())                     -- CPU 时间（不是墙钟）
print(os.difftime(t2, t1))
```

Lua 没有时区数据库，高精度计时要靠第三方库（如 LuaSocket 的 `gettime`）。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 运行时的日期仍然是 `Date`（可变、月份从 0 开始），本地化显示用 `Intl.DateTimeFormat`，日期运算常用 dayjs/date-fns，新标准 `Temporal` 正在落地。

```ts
const now = new Date();                       // 可变；月份从 0 开始
now.getMonth();                                // 0 = 一月
now.toISOString();                             // UTC ISO 字符串
Date.now();                                    // 毫秒时间戳

new Intl.DateTimeFormat("zh-CN", { timeZone: "Asia/Shanghai" }).format(now);

// Temporal（新标准，逐步落地）：不可变、语义清晰
```

代码演示 `Date` 的月份从 0 开始、`toISOString` 与 `Intl.DateTimeFormat`。要点是：`Date` 可变且解析行为有历史差异；显示用 `Intl`、传输用 ISO 字符串，复杂日期运算用 dayjs/date-fns。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `Date` 是可变对象（月份从 0 开始），传输用 `toISOString()`，显示用 `Intl.DateTimeFormat`，测耗时用 `performance.now()`。

```js
const now = new Date();
Date.now();
new Date("2026-09-18T10:00:00+08:00");        // 带时区的 ISO 最稳
now.getTime();
now.toLocaleString("zh-CN", { timeZone: "Asia/Shanghai" });

performance.now();                             // 高精度单调计时（毫秒）
```

代码演示 `Date.now`/`getTime`/`toLocaleString` 与 `performance.now()`。要点是：测量耗时用 `performance.now()`（单调时钟），`Date.now()` 会被系统调时影响。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 用 `DateTimeImmutable`（推荐）/`DateTime`、`DateInterval` 与 `DateTimeZone` 处理日期，业务代码常用 Carbon；耗时用单调的 `hrtime(true)`。

```php
$now = new DateTimeImmutable();                  // 推荐不可变版本
$sh = new DateTimeImmutable("2026-09-18 10:00:00", new DateTimeZone("Asia/Shanghai"));
$sh->format("Y-m-d H:i:s");
$sh->add(new DateInterval("P1D"));

hrtime(true);                                    // 单调纳秒（计时）
time();                                          // Unix 秒
```

要点是：优先用不可变版本（每次修改返回新对象），计时用单调的 `hrtime`，业务代码常用 Carbon 补足便利方法。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用 `Time`（带时区/偏移）表示时间点，`date` 标准库提供 `Date`/`DateTime`；Rails 项目用 `ActiveSupport::TimeWithZone` 统一时区。

```ruby
Time.now                       # 带时区的时间点
Time.now.utc
Time.at(0)
Time.new(2026, 9, 18, 10, 0, 0, "+08:00")
Time.now.strftime("%Y-%m-%d %H:%M:%S")

require "date"
Date.today                      # 只有日期
DateTime.now                     # 带日历（date 库）
```

代码演示 `Time.now`/`utc`/`Time.new` 与 `strftime`，以及 `date` 库的 `Date`/`DateTime`。要点是：`Time` 带时区/偏移、`Date` 只有日期；

{{% /tab %}}

{{< /tabpane >}}

### 大数与定点数

**一页速览**

| 语言 | 有没有 | 关键字 / 写法 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | ✓（部分） | `i128`/`u128`；`num-bigint`；`rust_decimal` | 没有内建任意精度整数 |
| Swift | ✓（部分） | `Decimal`（十进制定点）、`Int128`（Swift 6）；BigInt 靠包 | `Decimal` 适合金额 |
| Go | ✓ | `math/big`（`Int`/`Rat`/`Float`）；金额用 shopspring/decimal | 标准库自带任意精度 |
| Python | ✓ | `int` 任意精度、`decimal.Decimal`、`fractions.Fraction` | 三种都是内建/标准库 |
| Kotlin | ✓（JVM） | `java.math.BigInteger`/`BigDecimal` | JVM 上可用 |
| Java | ✓ | `BigInteger`/`BigDecimal` | 标准库自带 |
| C++ | ✓（部分） | `__int128`（GCC/Clang 扩展）、Boost.Multiprecision | 标准库没有大数 |
| C | ✗（内建） | GMP 等库；`__int128` 是扩展 | 需要第三方库 |
| Julia | ✓ | `BigInt`、`BigFloat`、`Rational` | 内建且好用 |
| C# | ✓ | `BigInteger`（System.Numerics）、`decimal` | `decimal` 是 128 位十进制 |
| Dart | ✓（部分） | `BigInt`（dart:core）；decimal 靠包 | BigInt 内建 |
| R | ✓（靠包） | `bit64`、`Rmpfr`、`gmp`；默认只有 double | 没有内建大整数 |
| Zig | ✓（部分） | 任意位宽 `uN`/`iN`；`std.math.big.int` | 大整数运算在标准库 |
| Lua | ✗ | 64 位整数；没有 BigInt | 需要自己实现或第三方 |
| TypeScript | ✓（部分） | `bigint`；decimal 靠库 | `bigint` 是语言内建 |
| JavaScript | ✓（部分） | `BigInt`；decimal 靠库 | ES2020 起内建 |
| PHP | ✓（扩展） | `bcmath`、`gmp` | 需要扩展支持 |
| Ruby | ✓ | `Integer` 任意精度、`BigDecimal`、`Rational` | 内建 + 标准库 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 内建的最大固定宽度整数是 `i128`/`u128`；任意精度整数用 `num-bigint`，十进制定点（金额）用 `rust_decimal`，标准库没有大数类型。

```rust
let a: i128 = 170_141_183_460_469_231_731_687_303_715_884_105_727;

// 更大的整数用 num-bigint
// let b = num_bigint::BigInt::from(1) << 200;

// 十进制定点用 rust_decimal
// let m = rust_decimal::Decimal::new(1, 1); // 0.1
```

代码演示 `i128` 的上限，以及注释里的 `num-bigint`/`rust_decimal` 方案。要点是：标准库最大就是 128 位；

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `Decimal` 是十进制定点（适合金额），`Int128`/`UInt128`（Swift 6）是最大的内建整数；任意精度整数需要第三方包。

```swift
let d = Decimal(string: "0.1")!        // 十进制定点
let sum = d + Decimal(string: "0.2")!   // 精确 0.3

let big = Int128.max                    // Swift 6 起（64 位平台）
// 更大的整数用 swift-numerics / BigInt 包
```

代码演示 `Decimal` 的十进制加法与 `Int128.max`。BigInt 需要第三方包。

{{% /tab %}}

{{% tab header="Go" %}}

Go 的标准库 `math/big` 提供任意精度整数、有理数与浮点（`Int`/`Rat`/`Float`）；金额场景常用 `shopspring/decimal`。

```go
import "math/big"

a := big.NewInt(1)
a.Lsh(a, 200)                     // 1 << 200（任意精度）
r := big.NewRat(1, 3)              // 精确有理数
f := new(big.Float).SetPrec(256)    // 任意精度浮点

// 金额：github.com/shopspring/decimal
```

代码演示 `big.Int` 的位移与 `big.Rat`/`big.Float` 的创建。

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `int` 天生任意精度，`decimal.Decimal` 提供十进制浮点，`fractions.Fraction` 提供精确分数——三种都在标准库里。

```python
2 ** 200                     # int：任意精度
from decimal import Decimal
Decimal("0.1") + Decimal("0.2")   # Decimal('0.3')，精确
from fractions import Fraction
Fraction(1, 3) + Fraction(1, 6)    # Fraction(1, 2)

import sys
sys.set_int_max_str_digits(10_000)   # 3.11+ 调整 int↔str 位数上限
```

代码演示任意精度 `int`、`Decimal` 与 `Fraction`。要点是：三者都在标准库里；`Decimal` 要用字符串构造（`Decimal("0.1")`），3.11+ 还有 `int`↔`str` 的默认位数上限。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 在 JVM 上直接用 `java.math.BigInteger` 与 `BigDecimal`（BigDecimal 的除法必须显式给舍入模式）。

```kotlin
val a = java.math.BigInteger("123456789012345678901234567890")
a.multiply(a)

val m = java.math.BigDecimal("0.1") + java.math.BigDecimal("0.2")
m.setScale(2, java.math.RoundingMode.HALF_UP)
```

代码演示 `BigInteger` 的乘法与 `BigDecimal` 的 `setScale`。要点是：直接用 JVM 的这两个类；`BigDecimal` 的除法必须显式指定舍入模式，否则除不尽会抛异常。

{{% /tab %}}

{{% tab header="Java" %}}

Java 标准库提供不可变的 `BigInteger`（任意精度整数）与 `BigDecimal`（任意精度十进制），构造要用字符串而不是 double。

```java
BigInteger a = new BigInteger("123456789012345678901234567890");
BigInteger b = a.multiply(a);

BigDecimal m = new BigDecimal("0.1").add(new BigDecimal("0.2"));
m.setScale(2, RoundingMode.HALF_UP);
m.divide(new BigDecimal("3"), 10, RoundingMode.HALF_UP);   // 除法必须给精度
```

代码演示 `BigInteger`/`BigDecimal` 的加法与 `divide` 的精度参数。要点是：两者都不可变（每次运算返回新对象），构造要用字符串，除法必须给精度与舍入模式。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 标准库没有大数：`__int128` 是 GCC/Clang 扩展（MSVC 不支持），任意精度用 Boost.Multiprecision 或 GMP。

```cpp
__int128 big = (__int128)1 << 100;          // GCC/Clang 扩展

// 任意精度：Boost.Multiprecision
// #include <boost/multiprecision/cpp_int.hpp>
// boost::multiprecision::cpp_int x = 1; x <<= 200;

// 十进制：boost::multiprecision::cpp_dec_float_50
```

代码演示 `__int128` 的位移，以及注释里的 Boost.Multiprecision 方案。

{{% /tab %}}

{{% tab header="C" %}}

C 没有内建大数，最大就是 `long long`；需要任意精度就用 GMP、OpenSSL BN 这类库（注意手动初始化与释放）。

```c
/* 没有内建大数：用 GMP 之类的库 */
#include <gmp.h>
mpz_t a;
mpz_init_set_str(a, "123456789012345678901234567890", 10);
mpz_mul(a, a, a);
mpz_clear(a);

/* __int128 是 GCC/Clang 扩展，不是标准 */
```

代码演示 GMP 的 `mpz_init_set_str`/`mpz_mul`/`mpz_clear` 三步。要点是：标准 C 最大只有 `long long`，大数必须用库，而且这类库都要手动初始化与释放。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 标准库内建 `BigInt`（任意精度整数）、`BigFloat`（基于 MPFR 的任意精度浮点）与 `Rational`（精确分数）。

```julia
big"123456789012345678901234567890"    # BigInt
BigFloat("0.1")                         # 任意精度浮点（MPFR）
1//3 + 1//6                             # Rational：精确分数

setprecision(256) do
    BigFloat(1) / 3
end
```

代码演示 `big"..."`、`BigFloat`、`Rational` 与 `setprecision` 块。要点是：`BigInt`/`BigFloat`/`Rational` 都在标准库；`BigFloat` 默认 256 位精度，可以临时调高。

{{% /tab %}}

{{% tab header="C#" %}}

C# 用 `System.Numerics.BigInteger` 表示任意精度整数，用 `decimal` 表示 128 位十进制定点（28~29 位有效数字，适合金额）。

```csharp
var a = System.Numerics.BigInteger.Parse("123456789012345678901234567890");
var b = a * a;

decimal m = 0.1m + 0.2m;            // 0.3（十进制，精确）
Math.Round(m, 2, MidpointRounding.AwayFromZero);
```

代码演示 `BigInteger.Parse`、`decimal` 运算与 `Math.Round` 的舍入模式。要点是：`BigInteger` 任意精度、`decimal` 是 128 位十进制（28~29 位有效数字），两者与 `double` 之间都没有隐式转换。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `BigInt` 在 `dart:core`，可做任意精度整数运算；十进制/货币要引第三方包（如 decimal）。

```dart
var a = BigInt.parse("123456789012345678901234567890");
var b = a * a;
a.isEven;

// 十进制：用 decimal 包（pub.dev）
// final m = Decimal.parse('0.1') + Decimal.parse('0.2');
```

代码演示 `BigInt.parse` 的乘法与 `isEven`。

{{% /tab %}}

{{% tab header="R" %}}

R 的默认数字是 double（53 位有效位），超出就会丢精度；64 位整数用 `bit64`，任意精度用 `Rmpfr`（浮点）与 `gmp`（整数/有理数）。

```r
.Machine$double.xmax             # 1.797693e+308（double 上限）
bit64::as.integer64("9007199254740993")   # 64 位整数
Rmpfr::mpfr(1, 256)              # 256 位浮点
gmp::as.bigz("123456789012345678901234567890")

2^53 + 1 == 2^53                  # TRUE ← double 只有 53 位有效位
```

代码演示 `.Machine$double.xmax`、`2^53 + 1 == 2^53` 与 `bit64`/`Rmpfr`/`gmp` 的用法。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的任意位宽整数（`uN`/`iN`）是语言级特性，编译期就能算；运行时的大整数运算用标准库 `std.math.big.int`（需要 allocator）。

```zig
const a: u256 = 1;                 // 任意位宽整数（编译期类型）
const b = @as(u1024, 1) << 1000;

const std = @import("std");
var big = try std.math.big.int.Managed.init(allocator);
defer big.deinit();
try big.setString(10, "123456789012345678901234567890");
```

代码演示任意位宽 `u256`/`u1024` 与 `std.math.big.int.Managed`。运行时大整数要用 `Managed`（需要 allocator），0.15 的接口是 `Managed.init(allocator)` + `setString(base, value)`。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的整数固定是 64 位、溢出会回绕，没有任意精度整数；需要大数只能自己实现字符串运算或引第三方库。

```lua
print(math.maxinteger)          -- 9223372036854775807
print(math.maxinteger + 1)      -- 回绕成 mininteger

-- 没有 BigInt：用字符串运算或第三方库
```

代码演示 `math.maxinteger` 与溢出回绕。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 用 ES2020 的 `bigint` 表示任意精度整数（不能与 `number` 混算、不能直接 JSON 序列化），十进制用 decimal.js 之类的库。

```ts
const a = 123456789012345678901234567890n;    // bigint（target ≥ ES2020）
const b = a * a;

// 十进制：decimal.js / big.js
// const m = new Decimal("0.1").plus("0.2");
```

代码演示 `bigint` 乘法与注释里的 Decimal 方案。十进制用 decimal.js 之类的库。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `BigInt` 是内建任意精度整数，但 `JSON.stringify(1n)` 会抛 TypeError，传输时要转成字符串。

```js
const a = 123456789012345678901234567890n;
const b = a * a;

Number.MAX_SAFE_INTEGER;      // 9007199254740991
JSON.stringify(1n);            // 🛑 TypeError：BigInt 不能直接序列化
```

代码演示 `BigInt` 乘法、`Number.MAX_SAFE_INTEGER` 与 `JSON.stringify(1n)` 抛错。要点是：`BigInt` 与 `number` 不能混算，序列化要转字符串；金额用整数分或 decimal 库。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `int` 只有平台字长，溢出会变 float；任意精度要用 `bcmath`（十进制字符串）或 `gmp`（大整数）扩展。

```php
bcadd("0.1", "0.2", 2);                     // "0.30"：十进制字符串运算
bcscale(2);
bcmul("1.5", "2.5");

$a = gmp_init("123456789012345678901234567890");
gmp_mul($a, $a);
```

代码演示 `bcadd`/`bcscale` 与 `gmp_*` 的用法。十进制用 `bcmath`（字符串运算），任意精度整数用 `gmp`，两者都需要相应扩展。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的 `Integer` 任意精度，标准库还提供 `BigDecimal`（十进制）与 `Rational`（精确分数），金额用后两者或整数分。

```ruby
2 ** 200                             # Integer：任意精度
require "bigdecimal"
BigDecimal("0.1") + BigDecimal("0.2")  # 0.3e0（精确）

Rational(1, 3) + Rational(1, 6)       # (1/2)
```

代码演示 `2 ** 200`、`BigDecimal` 与 `Rational`。金额用后两者或整数分。

{{% /tab %}}

{{< /tabpane >}}

---

> 本页覆盖 7 个大类：**整型、浮点型、布尔·字符·字符串、复合类型（数组与切片 / 元组 / 映射与集合 / 范围与迭代）、自定义类型（结构体与记录 / 类 / 枚举 / 联合与变体 / 接口·协议·trait / 泛型 / 类型别名与新类型）、空值与可选、其他类型（函数与闭包 / 指针与引用 / 动态与顶层类型 / 日期与时间 / 大数与定点数）**。每个标签页给出该语言的写法、边界、语义与陷阱；没有对应构造的语言会直接说明并给出替代做法。

> 版本基线（写作时 2026-09，均为各语言当前稳定版）：Rust 1.98、Swift 6.4、Go 1.27、Python 3.14、Kotlin 2.4、Java 26（LTS 25）、C++23、C23、Julia 1.13、C# 14 / .NET 10、Dart 3.13、R 4.6、Zig 0.15、Lua 5.5、TypeScript 7、Node 26、PHP 8.5、Ruby 4.0。
