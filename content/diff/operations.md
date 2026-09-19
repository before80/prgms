+++
title = "operations"
date = 2026-09-19T09:40:00+08:00
weight = 6
type = "docs"
description = "18 种语言的基本运算对照：算术运算、位运算与移位、比较与逻辑运算"
isCJKLanguage = true
draft = false
+++

# 基本运算：18 种语言对照

运算符看起来是全世界通用的符号，但每门语言都给它们塞进了不同的语义：`/` 在 Python 里永远给浮点、在 Ruby 里是地板除、在 C 里是截断除；`%` 的符号在 C 系跟被除数、在 Python/R 里跟除数；`==` 在 JavaScript 里会做类型转换，在 Kotlin 里等价于 `equals`。本页按三个主题组织：**算术运算 → 位运算与移位 → 比较与逻辑运算**，每个主题一套 18 语言标签页；类型转换与运算符优先级单独放在 [typeTrans]({{< relref "typeTrans.md" >}}) 一页。

## 基本运算

**一页速览**

| 语言 | 整数除法 | `%` 的符号 | 幂运算 | 溢出行为 |
| --- | --- | --- | --- | --- |
| Rust | 向零截断 | 跟被除数 | `pow`/`powi` | debug 崩溃、release 回绕 |
| Swift | 向零截断 | 跟被除数 | `pow`（浮点） | 崩溃（`&+` 回绕） |
| Go | 向零截断 | 跟被除数 | `math.Pow` | 静默回绕 |
| Python | `//` 向 −∞ | 跟除数 | `**` | 不溢出（任意精度） |
| Kotlin | 向零截断 | 跟被除数 | `Math.pow`/`pow` | 静默回绕 |
| Java | 向零截断 | 跟被除数 | `Math.pow` | 静默回绕 |
| C++ | 向零截断 | 跟被除数 | `std::pow` | 有符号 UB、无符号回绕 |
| C | 向零截断 | 跟被除数 | `pow` | 有符号 UB、无符号回绕 |
| Julia | `div` 向零、`fld` 向 −∞ | `rem` 跟被除数、`mod` 跟除数 | `^` | 回绕（`Base.Checked` 可检查） |
| C# | 向零截断 | 跟被除数 | `Math.Pow` | 默认回绕（`checked` 抛异常） |
| Dart | `~/` 向零 | `%` 恒非负 | `math.pow` | VM 回绕、Web 丢精度 |
| R | `%/%` 向 −∞ | 跟除数 | `^` | 变 `NA` + 警告 |
| Zig | `@divTrunc`/`@divFloor` | `@rem`/`@mod` | `std.math.pow` | 安全模式崩溃 |
| Lua | `//` 向 −∞ | 跟除数 | `^` | 回绕 |
| TypeScript | `Math.trunc` 模拟 | 跟被除数 | `**` | 丢精度（2⁵³ 以上） |
| JavaScript | `Math.trunc` 模拟 | 跟被除数 | `**` | 丢精度（2⁵³ 以上） |
| PHP | `intdiv` 向零 | 跟被除数 | `**` | 静默变 float |
| Ruby | `/` 向 −∞ | 跟除数 | `**` | 不溢出（任意精度） |

### 算术运算

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
let (a, b) = (7i32, 2i32);
a / b;                 // 3    向零截断
-7 % 2;                 // -1   % 的符号跟被除数
(-7i32).div_euclid(2);   // -4   地板除数
(-7i32).rem_euclid(2);   // 1    非负余数
2i32.pow(10);            // 1024（整数幂：powi/pow）
```

Rust 没有 `**` 运算符：整数用 `pow`/`powi`，浮点用 `powf`/`powi`。溢出在 debug 下 panic、release 下回绕，要确定性就用 `checked_*`/`wrapping_*`/`saturating_*`。

📘 [Rust · 运算符](https://doc.rust-lang.org/reference/expressions/operator-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
7 / 2          // 3
-7 % 2          // -1   符号跟被除数
7.0 / 2          // 3.5
pow(2.0, 10.0)    // 1024.0（浮点幂）
Int8(127) &+ 1     // -128  回绕
```

整数除法向零截断、`%` 支持整数与浮点（浮点用 `truncatingRemainder` 语义）；溢出默认 trap，只有 `&+`/`&-`/`&*` 才回绕。没有整数的 `**`。

📘 [Swift · 基本运算符](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/basicoperators/)

{{% /tab %}}

{{% tab header="Go" %}}

```go
7 / 2            // 3
-7 % 2            // -1   符号跟被除数
math.Pow(2, 10)    // 1024（浮点）
var u uint8 = 255
u++                // 0    回绕
```

Go 的整数除法向零截断、`%` 跟被除数；没有幂运算符（用 `math.Pow`，返回 `float64`）；溢出静默回绕，`math.MinInt64 / -1` 也回绕。

📘 [Go spec · 算术运算符](https://go.dev/ref/spec#Arithmetic_operators)

{{% /tab %}}

{{% tab header="Python" %}}

```python
7 / 2        # 3.5   真除法，永远 float
7 // 2       # 3     地板除（向 -∞）
-7 // 2      # -4
-7 % 2       # 1     % 的符号跟除数
7 % -2       # -1
2 ** 10      # 1024  任意精度
divmod(-7, 2)  # (-4, 1)
```

Python 的 `//` 与 `%` 满足 `a == (a // b) * b + a % b`，所以负数取模结果非负（当 `b > 0`）；整数是任意精度，不存在溢出。

📘 [Python · 算术运算](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
7 / 2              // 3
-7 % 2              // -1   符号跟被除数
(-7).floorDiv(2)     // -4   地板除（1.5+）
(-7).mod(2)          // 1    符号跟除数
2.0.pow(10)           // 1024.0
```

Kotlin 的 `/`/`%` 走 JVM 语义（向零、跟被除数），另有 `floorDiv`/`mod` 提供地板语义；整数没有 `**`，要用 `Math.pow` 或浮点的 `pow`。

📘 [Kotlin · 数字运算](https://kotlinlang.org/docs/numbers.html)

{{% /tab %}}

{{% tab header="Java" %}}

```java
7 / 2;                       // 3
-7 % 2;                       // -1   符号跟被除数
Math.floorDiv(-7, 2);          // -4
Math.floorMod(-7, 2);          // 1
Math.pow(2, 10);               // 1024.0
Math.addExact(Integer.MAX_VALUE, 1);   // 🛑 ArithmeticException
```

`/` 与 `%` 向零、跟被除数；`Math.floorDiv`/`floorMod` 给地板语义；没有 `**`，`Math.pow` 返回 `double`（大整数幂用 `BigInteger.pow`）。

📘 [JLS · 除法与取模](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.17)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
7 / 2;                 // 3
-7 % 2;                 // -1  符号跟被除数
std::pow(2.0, 10.0);      // 1024.0
std::midpoint(1, 2);       // 1    安全求平均（C++20）
1u << 31;                  // 无符号回绕（有符号溢出是 UB）
```

整数除法向零截断、`%` 跟被除数；有符号溢出是未定义行为，无符号才回绕；`std::pow` 返回浮点，整数幂要自己写或引库。

📘 [cppreference · 算术运算符](https://en.cppreference.com/w/cpp/language/operator_arithmetic)

{{% /tab %}}

{{% tab header="C" %}}

```c
7 / 2;             /* 3 */
-7 % 2;             /* -1  符号跟被除数 */
pow(2.0, 10.0);      /* 1024.0，需要 <math.h> 并链接 -lm */
INT_MIN / -1;        /* 🛑 UB */
```

C 的除法与取模同 C++：向零截断、`%` 跟被除数；`%` 只能用于整数（浮点取模用 `fmod`）；有符号溢出与 `INT_MIN / -1` 都是 UB。

📘 [cppreference · C 算术运算符](https://en.cppreference.com/w/c/language/operator_arithmetic)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
7 / 2        # 3.5   永远 Float64
7 ÷ 2        # 3     div：向零
div(-7, 2)   # -3
fld(-7, 2)   # -4    向 -∞
rem(-7, 2)   # -1    符号跟被除数
mod(-7, 2)   # 1     符号跟除数
2 ^ 10        # 1024
```

Julia 把"整除"拆成四个函数（`div`/`fld`/`cld` 与 `rem`/`mod`），语义一目了然；`^` 既能做整数幂也能做浮点幂，整数溢出静默回绕。

📘 [Julia · 数学运算](https://docs.julialang.org/en/v1/manual/mathematical-operations/)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
7 / 2;                       // 3
-7 % 2;                       // -1
Math.DivRem(7, 2, out int r);  // 商与余数一次拿到
Math.Pow(2, 10);               // 1024.0
decimal m = 0.1m + 0.2m;        // 0.3（十进制精确）
```

整数除法向零、`%` 跟被除数；没有 `**`（`Math.Pow` 返回 `double`）；`decimal` 是十进制运算，适合金额；整数溢出默认回绕，`checked` 才抛异常。

📘 [MS Learn · 算术运算符](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/arithmetic-operators)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
7 / 2       // 3.5   / 永远 double
7 ~/ 2      // 3     向零整除
-7 % 3      // 2     % 是欧几里得模，恒非负
(-7).remainder(3)   // -1   余数跟被除数
math.pow(2, 10)      // 1024（dart:math）
```

Dart 用 `~/` 表示整除、`%` 恒非负；没有 `**`，幂要用 `dart:math` 的 `pow`（返回 `num`）；Web 上整数退化为 JS number。

📘 [Dart · 运算符](https://dart.dev/language/operators)

{{% /tab %}}

{{% tab header="R" %}}

```r
7 / 2        # 3.5
7 %/% 2      # 3     地板整除
-7 %/% 2     # -4
-7 %% 2      # 1     符号跟除数
2 ^ 10       # 1024
c(1, 2) + 1   # 向量化：[1] 2 3
```

R 的 `/` 永远给 double、`%/%` 是地板整除、`%%` 的符号跟除数；**所有算术都是向量化的**，循环通常不需要；整数溢出得到 `NA` 加警告。

📘 [R · 算术运算符](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Arithmetic.html)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const a: i32 = -7;
@divTrunc(a, 2);   // -3   向零
@divFloor(a, 2);    // -4   向 -∞
@rem(a, 2);          // -1   符号跟被除数
@mod(a, 2);           // 1    符号跟除数
std.math.pow(f64, 2, 10);   // 1024
```

Zig 的 `+`/`-`/`*` 默认检查溢出（安全模式崩溃），`+%` 回绕、`+|` 饱和；有符号的 `/` 与 `%` 在运行时要用内置函数。

📘 [Zig · 运算符](https://ziglang.org/documentation/master/#Table-of-Operators)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
print(7 / 2)      -- 3.5   / 永远 float
print(7 // 2)     -- 3     地板除
print(-7 // 2)    -- -4
print(-7 % 2)     -- 1     % 跟除数
print(2 ^ 10)      -- 1024.0  ^ 返回 float
print("10" + 1)     -- 11    字符串自动转数字
```

Lua 的 `//`/`%` 是地板语义、`^` 永远返回浮点；整数溢出回绕（`math.maxinteger + 1 == math.mininteger`）。

📘 [Lua 5.5 · 算术运算符](https://www.lua.org/manual/5.5/manual.html#3.4.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
7 / 2;             // 3.5   / 永远浮点
Math.trunc(7 / 2);  // 3     模拟整除
-7 % 2;             // -1    符号跟被除数
2 ** 10;             // 1024
Number.MAX_SAFE_INTEGER + 1 === Number.MAX_SAFE_INTEGER + 2;   // true（丢精度）
```

`number` 是双精度浮点：没有整除运算符、超过 2⁵³ 静默丢精度；需要精确整数用 `bigint`（支持 `**` 但不能与 `number` 混算）。

📘 [MDN · 算术运算符](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators#arithmetic_operators)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
7 / 2;                 // 3.5
Math.trunc(7 / 2);      // 3
-7 % 2;                 // -1
2 ** 10;                 // 1024
"1" + 1;                 // "11"  ← + 会拼接字符串
10n ** 2n;                // 100n  bigint 幂
```

除了"永远浮点"之外，JS 最大的坑是 `+`：只要一边是字符串就变成拼接；判类型要显式用 `Number()`/`String()`。

📘 [MDN · 表达式与运算符](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
7 / 2;            // 3.5
intdiv(7, 2);      // 3     向零整除
-7 % 2;            // -1    符号跟被除数
2 ** 10;            // 1024
fmod(-7, 2);        // -1    浮点取模（C 语义）
PHP_INT_MAX + 1;     // float  ← 溢出变浮点
```

`/` 在整除时返回 int、否则 float；`%` 只对整数（会先转 int），浮点用 `fmod`；整数溢出静默变成 float。

📘 [PHP · 算术运算符](https://www.php.net/manual/en/language.operators.arithmetic.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
7 / 2        # 3
-7 / 2       # -4    地板除
-7 % 2       # 1     % 跟除数
2 ** 100      # 大整数，任意精度
7.fdiv(2)     # 3.5
(-7).divmod(2) # [-4, 1]
```

Ruby 的 `/` 对两个整数是地板除、`%` 跟除数，这点和 C 系相反；整数任意精度，不会溢出。

📘 [Ruby · 数值运算](https://docs.ruby-lang.org/en/master/Numeric.html)

{{% /tab %}}

{{< /tabpane >}}

### 位运算与移位

位运算的差异集中在三处：**移位计数怎么算**（超出位宽会怎样）、**有符号 vs 无符号**（逻辑移位还是算术移位）、以及**有没有饱和/回绕移位**。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
let (a, b) = (0b1010u8, 0b1100u8);
a & b; a | b; a ^ b; !a;
1u8 << 3;        // 8
1u8 << 8;         // 🛑 debug panic（移位溢出）；用 wrapping_shl 回绕
a.rotate_left(1); a.count_ones();
```

📘 [Rust · 运算符](https://doc.rust-lang.org/reference/expressions/operator-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
let a: UInt8 = 0b1010
a & 0b1100; a | 1; a ^ 1; ~a
a << 3
a &<< 9              // 回绕移位（&<< / &>>）
a.nonzeroBitCount     // 置位个数
a.leadingZeroBitCount
```

📘 [Swift · 位运算符](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/advancedoperators/)

{{% /tab %}}

{{% tab header="Go" %}}

```go
var a uint8 = 0b1010
a & 0b1100; a | 1; a ^ 1; a &^ 1   // &^ = AND NOT（位清除）
^a                                   // 取反（没有 ~ 运算符）
a << 3
a << 9                                // 移出位宽 → 0（不是 UB）
```

📘 [Go spec · 位运算符](https://go.dev/ref/spec#Arithmetic_operators)

{{% /tab %}}

{{% tab header="Python" %}}

```python
a = 0b1010
a & 0b1100; a | 1; a ^ 1; ~a        # ~x == -x-1（任意精度）
a << 3; a >> 1
a.bit_length(); a.bit_count()         # 3.10+
(255).to_bytes(2, "big")
```

📘 [Python · 位运算](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
val a = 0b1010
a and 0b1100    // 没有 & | ^ 运算符，用中缀函数
a or 1
a xor 1
a.inv()          // 按位取反
a shl 3          // 左移
a shr 1          // 算术右移（保留符号）
a ushr 1         // 逻辑右移
```

📘 [Kotlin · 位运算](https://kotlinlang.org/docs/numbers.html#bitwise-operations)

{{% /tab %}}

{{% tab header="Java" %}}

```java
int a = 0b1010;
a & 0b1100; a | 1; a ^ 1; ~a
a << 3; a >> 1; a >>> 1     // >>> 是无符号右移
a << 35                      // 计数按 32 取模 → 等价于 a << 3
Integer.toBinaryString(a)
```

📘 [JLS · 移位运算符](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.19)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
unsigned a = 0b1010u;
a & 0b1100u; a | 1u; a ^ 1u; ~a
a << 3; a >> 1
std::rotl(a, 1);              // C++20 循环移位
std::popcount(a);              // 置位个数
std::bit_width(a);              // 有效位数
```

📘 [cppreference · 位运算](https://en.cppreference.com/w/cpp/language/operator_arithmetic#Bitwise_operators)

{{% /tab %}}

{{% tab header="C" %}}

```c
unsigned a = 0b1010u;      /* C23 二进制字面量 */
a & 0b1100u; a | 1u; a ^ 1u; ~a
a << 3; a >> 1
/* 有符号左移溢出是 UB；右移是实现定义 */
```

📘 [cppreference · C 位运算](https://en.cppreference.com/w/c/language/operator_arithmetic#Bitwise_operators)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
a = 0b1010
a & 0b1100; a | 1; xor(a, 1); ~a
a << 3; a >> 1; a >>> 1      # >>> 是无符号右移
count_ones(a); bitstring(a)
leading_zeros(a)
```

📘 [Julia · 位运算](https://docs.julialang.org/en/v1/manual/mathematical-operations/#Bitwise-Operators)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
int a = 0b1010;
a & 0b1100; a | 1; a ^ 1; ~a
a << 3; a >> 1; a >>> 1     // >>> 从 C# 11 起
System.Numerics.BitOperations.PopCount((uint)a);
System.Numerics.BitOperations.LeadingZeroCount((uint)a);
```

📘 [MS Learn · 位运算符](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
var a = 0b1010;
a & 0b1100; a | 1; a ^ 1; ~a
a << 3; a >> 1; a >>> 1      // >>> 是逻辑右移（2.14+）
// ⚠️ 编译到 Web 时位运算被截断到 32 位
```

📘 [Dart · 运算符](https://dart.dev/language/operators)

{{% /tab %}}

{{% tab header="R" %}}

```r
bitwAnd(10L, 12L)      # 8
bitwOr(10L, 1L)         # 11
bitwXor(10L, 1L)         # 11
bitwNot(10L)              # -11
bitwShiftL(1L, 3)          # 8
bitwShiftR(8L, 1)           # 4
# ⚠️ 这些函数按 32 位整数运算；64 位用 bit64 包
```

📘 [R · 位运算](https://stat.ethz.ch/R-manual/R-devel/library/base/html/bitwAnd.html)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const a: u8 = 0b1010;
a & 0b1100; a | 1; a ^ 1; ~a
a << 3; a >> 1
a <<| 3;            // 饱和左移（<<|）
@popCount(a);        // 置位个数
@clz(a);             // 前导零
```

📘 [Zig · 运算符表](https://ziglang.org/documentation/master/#Table-of-Operators)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
local a = 0b1010        -- Lua 5.3+ 支持二进制字面量
print(a & 0b1100, a | 1, a ~ 1)   -- ~ 作为二元运算符是 XOR
print(~a)                          -- 一元 ~ 是按位取反
print(a << 3, a >> 1)
print(1 << 70)                      -- 超出位宽 → 0
```

📘 [Lua 5.5 · 位运算符](https://www.lua.org/manual/5.5/manual.html#3.4.2)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
const a = 0b1010;
a & 0b1100; a | 1; a ^ 1; ~a
a << 3; a >> 1; a >>> 1     // 32 位有符号 / 无符号右移
(2 ** 31) | 0;               // -2147483648（溢出到 32 位）
0b1010n << 3n;                // bigint 支持位运算，但没有 >>>
```

📘 [MDN · 位运算符](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators#bitwise_operators)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
const a = 0b1010;
a & 0b1100; a | 1; a ^ 1; ~~a   // ~~a 是常见的取整技巧
a << 3; a >> 1; a >>> 1          // >>> 返回无符号 32 位
(-1) >>> 0;                       // 4294967295
10n << 3n;                         // bigint
```

📘 [MDN · 位运算符](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators#bitwise_operators)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
$a = 0b1010;
$a & 0b1100; $a | 1; $a ^ 1; ~$a
$a << 3; $a >> 1                    // 算术右移
PHP_INT_MAX >> 1                     // 4611686018427387903
decbin($a);                          // 转二进制字符串
```

📘 [PHP · 位运算符](https://www.php.net/manual/en/language.operators.bitwise.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
a = 0b1010
a & 0b1100; a | 1; a ^ 1; ~a
a << 3; a >> 1          # >> 是算术右移（保留符号）
a.digits(2)              # 二进制各位
a.bit_length
(1 << 100).bit_length     # 101（任意精度）
```

📘 [Ruby · Integer](https://docs.ruby-lang.org/en/master/Integer.html)

{{% /tab %}}

{{< /tabpane >}}

### 比较与逻辑运算

比较运算的分歧在三处：**`==` 是值比较还是身份比较**、**逻辑运算符返回布尔还是返回操作数**、**`and`/`or` 是否短路以及优先级**。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
1 == 1; "a" < "b";              // 需要 PartialOrd
let x = 1; let y = &x;
x == *y;                         // 值比较；引用可比较
true && false; true || false;     // 短路
// if 1 {}                       // 🛑 没有隐式真值转换
```

📘 [Rust · 比较运算符](https://doc.rust-lang.org/std/cmp/index.html)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
1 == 1; "a" < "b"                 // Equatable / Comparable
let a = NSObject(); let b = a
a === b                            // 引用身份（AnyObject）
true && false; true || false        // 短路
```

📘 [Swift · 比较与身份](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/basicoperators/)

{{% /tab %}}

{{% tab header="Go" %}}

```go
1 == 1; "a" < "b"
a == b          // 结构体、数组可比较；切片/map 不可比较（除与 nil）
ok := x == nil
true && false; true || false   // 短路
// if 1 {}                     // 🛑 必须是 bool
```

📘 [Go spec · 比较运算符](https://go.dev/ref/spec#Comparison_operators)

{{% /tab %}}

{{% tab header="Python" %}}

```python
1 == 1.0        # True（按值）
a = [1]; b = [1]
a == b          # True
a is b          # False（身份）
0 < x < 10       # 链式比较
"" or "default"   # 'default'（and/or 返回操作数）
1 in [1, 2]        # 成员测试
```

📘 [Python · 比较](https://docs.python.org/3/reference/expressions.html#comparisons)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
val a = "x"; val b = "x"
a == b        // true：== 编译成 equals
a === b        // false：=== 是身份比较
1 < 2 && 2 < 3   // 短路
val x: Int? = null
x == null         // 判空用 ==
```

📘 [Kotlin · 相等性](https://kotlinlang.org/docs/equality.html)

{{% /tab %}}

{{% tab header="Java" %}}

```java
1 == 1;                        // 基本类型：值比较
Integer a = 128, b = 128;
a == b;                         // 🛑 false：引用身份（缓存只到 127）
a.equals(b);                     // true：值比较
Objects.equals(a, b);             // 空安全
true && false; true || false;
```

📘 [JLS · 相等性](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.21)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
1 == 1; "a" < "b"               // 可重载
auto c = (a <=> b);               // C++20 三路比较
std::cmp_less(-1, 1u);             // 混合符号的安全比较（C++20）
true && false; true || false;
```

📘 [cppreference · 比较运算符](https://en.cppreference.com/w/cpp/language/operator_comparison)

{{% /tab %}}

{{% tab header="C" %}}

```c
1 == 1; a < b;
(-1 < 1u)      /* 🛑 false：有符号被转成无符号 */
(x != 0) && (y != 0)   /* && / || 返回 0 或 1，且短路 */
```

📘 [cppreference · C 比较](https://en.cppreference.com/w/c/language/operator_comparison)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
1 == 1.0        # true（按值）
NaN == NaN       # false；isequal(NaN, NaN) 为 true
missing == 1      # missing（三值逻辑）
1 ≈ 1.0000001      # isapprox
true && false       # && / || 只接受 Bool
```

📘 [Julia · 比较](https://docs.julialang.org/en/v1/manual/mathematical-operations/#Comparison-Operators)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
1 == 1; string.Equals(a, b, StringComparison.Ordinal);
ReferenceEquals(a, b);          // 身份
a is string s;                   // 模式匹配
true && false; true || false;
Comparer<int>.Default.Compare(1, 2);
```

📘 [MS Learn · 相等性](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/statements-expressions-operators/equality-comparisons)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
1 == 1.0            // true（num 的 ==）
identical(a, b)      // 身份比较
a?.length ?? 0        // 空合并
true && false; true || false;
const listEquality = [1] == [1];   // 🛑 false（列表按身份比）
```

📘 [Dart · 运算符](https://dart.dev/language/operators)

{{% /tab %}}

{{% tab header="R" %}}

```r
c(1, 2) == 1        # [1] TRUE FALSE（向量化）
c(1, 2) > 0 & c(1,2) < 2   # & / | 是向量化的
TRUE && FALSE         # && / || 只看第一个元素且短路
identical(1L, 1)       # FALSE（类型不同）
all.equal(1, 1 + 1e-9)  # TRUE（带容差）
NA == 1                 # NA（缺失传染）
```

📘 [R · 逻辑运算符](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Logic.html)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
1 == 1; "a"[0] < "b"[0];
true and false; true or false;      // and / or（不是 && / ||）
const v = maybe orelse 0;            // 空合并
x != 0 and y != 0;
```

📘 [Zig · 运算符](https://ziglang.org/documentation/master/#Table-of-Operators)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
print(1 == 1.0)        -- true（按值）
print(1 ~= 2)           -- ~= 是不等
print(nil or "default")  -- and/or 返回操作数
if 0 then print("0 是真值") end   -- 只有 false/nil 为假
```

📘 [Lua 5.5 · 关系运算符](https://www.lua.org/manual/5.5/manual.html#3.4.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
1 === 1;            // 严格相等（用这个）
1 == "1";            // true（宽松，别用）
Object.is(NaN, NaN);   // true
Number.isNaN(NaN);      // true
null ?? "default";       // ?? 只对 null/undefined 生效
```

📘 [MDN · 相等比较](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Equality)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
1 === 1;                 // 严格
"1" == 1;                 // true（宽松）
null == undefined;         // true
Object.is(-0, 0);           // false
!!"" || "fallback";          // falsy 列表：false/0/-0/0n/""/null/undefined/NaN
```

📘 [MDN · 相等比较](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Equality)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
1 == "1";        // true（松散）
1 === "1";        // false（严格）
1 <=> 2;           // -1（太空船运算符）
0 == "abc";         // false（PHP 8 起；PHP 7 是 true）
$a = $b and false;   // ⚠️ = 优先级高于 and
```

📘 [PHP · 比较运算符](https://www.php.net/manual/en/language.operators.comparison.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
1 == 1.0        # true
1.eql?(1.0)      # false（类型也要一致，Hash 用这个）
1.equal?(1)       # true（身份）
1 <=> 2            # -1
a && b || c         # && 优先级高于 and/or
a and b or c         # ⚠️ 优先级更低
```

📘 [Ruby · 比较](https://docs.ruby-lang.org/en/master/Comparable.html)

{{% /tab %}}

{{< /tabpane >}}
