+++
title = "typeTrans"
date = 2026-09-19T10:00:00+08:00
weight = 8
type = "docs"
description = "18 种语言的类型转换对照：隐式提升、显式转换与截断、字符串与数字互转、优先级与求值顺序"
isCJKLanguage = true
draft = false
+++

# 类型转换：18 种语言对照

类型转换的分歧可以归结为四个问题：**会不会偷偷替你转**（隐式提升）、**怎么显式转**（`as`/`Int()`/`@intCast`/`T(x)`）、**转换失败会怎样**（截断、饱和、抛异常、变 `NA`）、**什么时候转**（运算符优先级与求值顺序）。本页按这四个主题组织，每个主题一套 18 语言标签页。

## 类型转换

**一页速览**

| 语言 | 隐式数值转换 | 显式转换写法 | 失败行为 |
| --- | --- | --- | --- |
| Rust | ✗ | `as`、`From`/`TryFrom` | `as` 截断且饱和；`TryFrom` 给 `Result` |
| Swift | ✗ | `Int(x)`、`Double(x)` | 溢出/NaN 崩溃；`Int(exactly:)` 给 `Optional` |
| Go | ✗（常量除外） | `T(x)` | 结果由实现决定（不 panic） |
| Python | ✓（int→float→complex） | `int()`、`float()`、`str()` | 不能转就抛 `ValueError`/`OverflowError` |
| Kotlin | ✗（字面量除外） | `toInt()`、`toDouble()` | 截断；NaN→0、超大值→极值 |
| Java | ✓（拓宽） | `(int)`、`Integer.parseInt` | 窄化截断；`parseInt` 抛异常 |
| C++ | ✓（数值提升/用户定义转换） | `static_cast<T>` | 越界是 UB/实现定义 |
| C | ✓（整型提升） | `(T)` | 越界实现定义 |
| Julia | ✗（赋值不隐式） | `T(x)`、`convert(T, x)` | 不能用就抛 `InexactError` |
| C# | ✓（拓宽） | `(int)`、`Convert.ToInt32` | `Convert` 抛 `OverflowException` |
| Dart | 部分（int/double 都是 `num`） | `toInt()`、`as`、`int.parse` | `as` 失败抛 `TypeError` |
| R | ✓（强制层级） | `as.numeric`、`as.integer` | 越界变 `NA` + 警告 |
| Zig | ✗ | `@intCast`、`@floatFromInt`、`@truncate` | 安全模式 panic |
| Lua | ✓（字符串↔数字） | `tonumber`、`tostring` | 失败给 `nil` |
| TypeScript | 类型层面（运行时同 JS） | `as`（仅编译期）、`Number()` | 运行时不做检查 |
| JavaScript | ✓（`+`/`==` 强制） | `Number()`、`String()`、`parseInt` | `NaN`；`parseInt` 静默截断 |
| PHP | ✓（松散） | `(int)`、`intval`、`intdiv` | 溢出变 float；转换可能告警 |
| Ruby | ✓（数值提升） | `to_i`、`Integer()`、`Float()` | `Integer()` 抛 `ArgumentError` |

### 隐式转换与类型提升

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
let x: i32 = 1;
// let y: i64 = x;          // 🛑 没有隐式转换
let y: i64 = x.into();       // From/Into：安全、无检查
let z: i32 = 300_i32;
// let w: u8 = z as u8;     // 44：as 直接截断
let s: &str = &String::from("x");   // Deref 强制转换
```

Rust 不隐式转换任何数值类型：`into()`/`try_into()` 走 trait，`as` 是"我知道我在干什么"的截断/饱和转换；`Deref` 是唯一的自动转换（`&String` → `&str`）。

📘 [Rust · 类型转换](https://doc.rust-lang.org/reference/expressions/operator-expr.html#type-cast-expressions)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
let i = 1
// let d: Double = i        // 🛑 没有隐式数值转换
let d = Double(i)             // 显式构造
let n = Int(3.9)               // 3（向零截断）
let m = Int(exactly: 3.9)       // nil
let any: Any = i
if let s = any as? String { }    // 类型转换（不是数值转换）
```

📘 [Swift · 类型转换](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/typecasting/)

{{% /tab %}}

{{% tab header="Go" %}}

```go
var i int32 = 1
// var j int64 = i          // 🛑 没有隐式转换
j := int64(i)
var f float64 = 1             // ✅ 无类型常量自动适配
var n int = 3
f2 := float64(n) / 2           // 3/2 会是 1，必须显式转
```

📘 [Go spec · 转换](https://go.dev/ref/spec#Conversions)

{{% /tab %}}

{{% tab header="Python" %}}

```python
1 + 1.5          # 2.5：int 自动提升为 float
True + 1          # 2：bool 是 int 子类
3 / 2              # 1.5：/ 永远给 float
3 // 2              # 1：地板除保持 int
"1" + 1              # 🛑 TypeError：字符串不会自动转数字
```

📘 [Python · 数值类型](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
val i = 1
// val l: Long = i           // 🛑 没有隐式拓宽
val l: Long = i.toLong()
val x: Long = 1                // ✅ 字面量常量可以
val sum = 1 + 2L                // Long（运算符重载自动提升）
val y: Int? = null
val z: Int = y ?: 0              // 可空性靠 ?: / !! 处理
```

📘 [Kotlin · 数字转换](https://kotlinlang.org/docs/numbers.html#explicit-number-conversions)

{{% /tab %}}

{{% tab header="Java" %}}

```java
byte b = 1;
int i = b;            // 拓宽：自动
long l = i;            // 自动
double d = l;           // 自动
// byte b2 = i;         // 🛑 窄化需要强制转换
byte b2 = (byte) i;
String s = "x" + 1;      // 字符串拼接（1 自动转字符串）
Integer boxed = 1;        // 自动装箱
```

📘 [JLS · 转换与提升](https://docs.oracle.com/javase/specs/jls/se25/html/jls-5.html)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
int i = 1;
long l = i;              // 标准转换：自动
double d = i;             // 自动
struct Meters { explicit Meters(double); };
// Meters m = 1.5;         // 🛑 explicit 阻止隐式构造
Meters m{1.5};
```

📘 [cppreference · 隐式转换](https://en.cppreference.com/w/cpp/language/implicit_conversion)

{{% /tab %}}

{{% tab header="C" %}}

```c
char c = 1;
int i = c;                 /* 整型提升 */
unsigned u = 1;
if (-1 < u) { }              /* 🛑 false：i 被转成 unsigned */
double d = 1 / 2;             /* 0.0！先做整数除法 */
double e = 1 / 2.0;            /* 0.5 */
```

📘 [cppreference · 隐式转换](https://en.cppreference.com/w/c/language/conversion)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
1 + 1.5            # 2.5：promote(Int, Float64) → Float64
typeof(1 + 1.5)     # Float64
x::Int = 1.0         # 🛑 InexactError：赋值不做隐式转换
convert(Float64, 1)   # 1.0（显式 convert）
Int(3.9)               # 🛑 InexactError
trunc(Int, 3.9)         # 3（显式取整）
```

📘 [Julia · 转换与提升](https://docs.julialang.org/en/v1/manual/conversion-and-promotion/)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
byte b = 1;
int i = b;                 // 拓宽：自动
long l = i;
double d = l;
// byte b2 = (byte)300;     // 44：显式窄化
checked { byte b3 = checked((byte)300); }   // 🛑 OverflowException
object o = i;               // 装箱
string s = "x" + i;          // 字符串拼接
```

📘 [MS Learn · 类型转换](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/casting-and-type-conversions)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
num a = 1;          // int 是 num 的子类型
num b = 1.5;
print(1 + 1.5);      // 2.5：int 与 double 混算自动提升
Object o = 42;
if (o is int) print(o + 1);    // 类型提升（智能转换）
var s = o as String;             // 🛑 类型不符抛 TypeError
```

📘 [Dart · 类型系统](https://dart.dev/language/type-system)

{{% /tab %}}

{{% tab header="R" %}}

```r
c(1, 2.5)        # double 向量（int 被提升）
c(1, "a")        # character 向量（全部变字符串）
TRUE + 1          # 2（logical 提升为 integer）
1 < "2"            # 用字符比较（强制层级：character 最高）
as.numeric("3.5")   # 3.5；as.numeric("a") → NA + 警告
```

强制层级是 logical < integer < double < complex < character：混合类型时向"更高"的一侧统一。

📘 [R · 强制转换](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Coercion)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const a: u8 = 250;
var b: i32 = a;          // ✅ u8 → i32 可隐式（i32 能装下 u8）
// var c: u8 = 300;      // 🛑 编译期越界
const d: i32 = @intCast(300);
const e: u8 = @truncate(d);        // 44（显式截断）
const f: u8 = std.math.cast(u8, 300) orelse 0;   // 可失败转换
```

Zig 的隐式转换只在"目标类型能完整表示源类型"时发生（peer type resolution）；其余一律显式。

📘 [Zig · 类型转换](https://ziglang.org/documentation/master/#Casting)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
print("10" + 1)      -- 11    字符串自动转数字
print("10" .. 1)      -- 101   数字自动转字符串（拼接）
print(1 + 1.0)         -- 2.0   整数提升为浮点
print(math.type(1 + 1.0))  -- float
print(tonumber("ff", 16))    -- 255
```

📘 [Lua 5.5 · 强制转换](https://www.lua.org/manual/5.5/manual.html#3.4.3)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
const x: number = 1;
const y: string = "1";
// const z: number = y;      // 🛑 编译错误
const z = Number(y);           // 运行时转换
const w = y as unknown as number;   // 断言：只骗编译器，不做转换
const lit = "a" as const;       // 字面量类型
```

类型层面的"隐式"包括结构子类型与字面量拓宽；运行时行为与 JS 完全一致——`as` 不产生任何代码。

📘 [TS · 类型断言](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
"1" + 1;         // "11"    + 触发字符串拼接
"1" - 1;          // 0       其它算术运算符触发数字转换
1 == "1";          // true
Number("42");       // 42
Number("");          // 0     ⚠️
Number(null);         // 0     ⚠️
Number(undefined);     // NaN
!!0;                    // false
```

📘 [MDN · 类型转换](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number#number_coercion)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
function f(int $x): int { return $x; }
declare(strict_types=1);         // 之后调用处不再自动转

"10" + 1;                         // 11（松散）
(int) "12abc";                     // 12
intval("ff", 16);                   // 255
1 == "1";                            // true（松散）
1 === "1";                            // false
```

PHP 的隐式转换只在"非严格模式"下发生；`declare(strict_types=1)` 只约束函数参数/返回值，运算符仍然松散。

📘 [PHP · 类型转换](https://www.php.net/manual/en/language.types.type-juggling.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
1 + 1.5        # 2.5：Integer 提升为 Float
1 + Rational(1, 2)   # (3/2)：提升为 Rational
1.to_s          # "1"
Integer("42")    # 42（严格，失败抛异常）
"12abc".to_i      # 12（宽松）
[1, 2] + [3]       # 数组拼接（+ 被重载）
```

Ruby 通过 `to_int`/`to_str` 这类隐式协议做转换，绝大多数转换仍需显式调用 `to_i`/`to_s`；严格解析用 `Integer()`/`Float()`。

📘 [Ruby · 隐式转换](https://docs.ruby-lang.org/en/master/language/implicit_conversion_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 显式转换与截断

显式转换要盯住三件事：**是否截断**（向零还是向下）、**失败怎么报**（抛异常、给 `nil`/`None`、还是静默给个数）、**有没有安全检查**（`checked`/`@intCast`/`TryFrom`）。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
let f = 3.9_f64;
f as i32;                     // 3（截断 + 饱和：NaN→0，超范围→边界）
let n: i32 = 300;
n as u8;                       // 44（直接截断低位）
i32::try_from(300_i64)?;        // 可失败转换（返回 Result）
let s = "42".parse::<i32>()?;    // 字符串解析
```

📘 [Rust · as 与 TryFrom](https://doc.rust-lang.org/reference/expressions/operator-expr.html#type-cast-expressions)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
Int(3.9)                // 3（向零截断）
Int(Double.nan)          // 🛑 崩溃
Int(exactly: 3.9)         // nil（可失败）
Int(clamping: 999)         // 255（UInt8 时饱和）
Int(truncatingIfNeeded: 300)   // 4400...（按位截断）
```

📘 [Swift · 数值转换](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/advancedoperators/)

{{% /tab %}}

{{% tab header="Go" %}}

```go
var f float64 = 3.9
int(f)                  // 3（向零截断）
int64(-1)               // -1
string(rune(65))         // "A"
string([]byte{65})        // "A"
strconv.Atoi("42")         // 42, nil
strconv.ParseInt("ff", 16, 64)   // 255
```

📘 [Go spec · 转换](https://go.dev/ref/spec#Conversions)

{{% /tab %}}

{{% tab header="Python" %}}

```python
int(3.9)        # 3（向零）
int(-3.9)        # -3
int("ff", 16)     # 255
float("1e3")       # 1000.0
str(42)             # "42"
int("4x")            # 🛑 ValueError
int(float("nan"))     # 🛑 ValueError
```

📘 [Python · 内置函数](https://docs.python.org/3/library/functions.html#int)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
3.9.toInt()              // 3（截断）
Double.NaN.toInt()        // 0
1e300.toInt()              // Int.MAX_VALUE
3.9.roundToInt()            // 4
"42".toInt()                 // 42（失败抛 NumberFormatException）
"42".toIntOrNull()            // Int?
java.math.BigDecimal(3.9).intValueExact()   // 抛 ArithmeticException
```

📘 [Kotlin · 显式转换](https://kotlinlang.org/docs/numbers.html#explicit-number-conversions)

{{% /tab %}}

{{% tab header="Java" %}}

```java
(int) 3.9;                 // 3（向零）
(int) Double.NaN;           // 0
(int) 1e300;                 // Integer.MAX_VALUE（JLS 定义的饱和）
Integer.parseInt("42");       // 抛 NumberFormatException 当输入非法
Integer.parseInt("ff", 16);    // 255
Math.toIntExact(9_000_000_000L);   // 🛑 ArithmeticException
```

📘 [JLS · 窄化转换](https://docs.oracle.com/javase/specs/jls/se25/html/jls-5.html#jls-5.1.3)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
static_cast<int>(3.9);          // 3
static_cast<unsigned char>(300); // 44
std::bit_cast<std::uint32_t>(1.0f);   // 位重解释（C++20）
std::stoi("42");                       // 抛 std::invalid_argument
std::from_chars(s.data(), s.data()+s.size(), n);   // 无异常、不分配
```

📘 [cppreference · static_cast](https://en.cppreference.com/w/cpp/language/static_cast)

{{% /tab %}}

{{% tab header="C" %}}

```c
(int) 3.9;                 /* 3 */
(unsigned char) 300;        /* 44 */
long v = strtol("42", &end, 10);   /* 带回错误检测 */
double d = strtod("3.14", NULL);
/* atoi("4x") 静默返回 4，没有错误检测——别用 */
```

📘 [`strtol`](https://en.cppreference.com/w/c/string/byte/strtol)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
Int(3.9)            # 🛑 InexactError
trunc(Int, 3.9)      # 3
round(Int, 3.5)       # 4（银行家舍入在 .5 时取偶）
parse(Int, "42")       # 42（失败抛 ArgumentError）
parse(Int, "ff", base=16)   # 255
reinterpret(UInt32, 1.0f0)   # 位重解释
```

📘 [Julia · 转换](https://docs.julialang.org/en/v1/manual/conversion-and-promotion/)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
(int) 3.9;                 // 3（unchecked）
checked((int) 1e300);        // 🛑 OverflowException
Convert.ToInt32(3.9);         // 4（四舍五入）
Convert.ToInt32(1e300);        // 🛑 OverflowException
int.Parse("42");                // 抛 FormatException 当非法
int.TryParse("4x", out int n);   // false
```

📘 [MS Learn · 转换表](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/numeric-conversions)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
3.9.toInt();            // 3
3.9.round();             // 4
double.nan.toInt();       // 🛑 UnsupportedError
int.parse("42");           // 42（失败抛 FormatException）
int.tryParse("4x");         // null
double.parse("1e3");         // 1000.0
```

📘 [Dart · num](https://api.dart.dev/stable/dart-core/num-class.html)

{{% /tab %}}

{{% tab header="R" %}}

```r
as.integer(3.9)        # 3（向零截断）
as.integer(-3.9)        # -3
as.integer(2147483648)   # NA + 警告（超出 32 位）
as.numeric("3.5")         # 3.5
as.numeric("a")            # NA + 警告
trunc(3.9); round(3.5)      # 3；4（银行家舍入：round(2.5)=2）
```

📘 [R · 转换](https://stat.ethz.ch/R-manual/R-devel/library/base/html/integer.html)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const f: f64 = 3.9;
const i: i32 = @intFromFloat(f);   // 3（安全模式：越界/NaN→panic）
const big: u16 = 300;
const small: u8 = @truncate(big);    // 44（显式截断）
const n = try std.fmt.parseInt(i32, "42", 10);
const bits: u64 = @bitCast(f);        // 位重解释
```

📘 [Zig · 内置转换函数](https://ziglang.org/documentation/master/#intCast)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
print(tonumber("42"))        -- 42（整数）
print(tonumber("42.5"))       -- 42.5（浮点）
print(tonumber("ff", 16))      -- 255
print(tonumber("x"))            -- nil（失败不抛错）
print(math.tointeger(3.0))       -- 3
print(math.tointeger(3.5))        -- nil
print(3.9 // 1)                    -- 3.0（截断技巧）
```

📘 [Lua 5.5 · tonumber](https://www.lua.org/manual/5.5/manual.html#pdf-tonumber)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
Number("42");            // 42
Number("");               // 0   ⚠️
Number.parseInt("42px");   // 42  ⚠️ 静默截断
Number.parseInt("ff", 16);  // 255
String(42);                  // "42"
BigInt("9007199254740993");   // 9007199254740993n
value as number;               // 仅编译期，不做转换
```

📘 [TS · 类型断言](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
Number("42");        // 42
parseInt("42px", 10);  // 42   ⚠️ 静默截断
parseFloat("3.14x");    // 3.14
String(null);             // "null"
Boolean("");               // false
~~3.9;                      // 3（32 位取整）
3.9 | 0;                     // 3
BigInt(42);                   // 42n
```

📘 [MDN · 类型转换](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
(int) 3.9;             // 3
(int) "12abc";          // 12
intval("ff", 16);        // 255
floatval("3.14");         // 3.14
strval(42);                // "42"
settype($x, "integer");     // 原地转换（返回 bool）
(int) NAN;                   // 结果无可移植保证
```

📘 [PHP · 类型转换](https://www.php.net/manual/en/language.types.type-juggling.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
3.9.to_i          # 3（向零）
3.9.round          # 4
Integer("42")       # 42（严格，失败抛 ArgumentError）
"ff".to_i(16)        # 255
"12abc".to_i          # 12（宽松）
Float("1.5")           # 1.5
[65].pack("C")          # "A"
```

📘 [Ruby · 转换](https://docs.ruby-lang.org/en/master/Kernel.html#method-i-Integer)

{{% /tab %}}

{{< /tabpane >}}

### 字符串与数字互转

这一类转换的关键是：**失败是给 `Optional`/`nil`/`bool` 还是抛异常**、**进制与格式化怎么写**、**地区（Locale）会不会影响结果**。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
let n: i32 = "42".parse()?;              // Result<i32, _>
let m = i32::from_str_radix("ff", 16)?;   // 255
let s = n.to_string();
let f = format!("{n:05} {:.2}", 3.14159);   // 00042 3.14
```

📘 [Rust · FromStr](https://doc.rust-lang.org/std/str/trait.FromStr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
Int("42")            // Optional(42)
Int("4x")             // nil（不抛异常）
Double("1.5")          // Optional(1.5)
String(42)              // "42"
String(format: "%05d", 42)   // "00042"
```

📘 [Swift · 字符串与数字](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/stringsandcharacters/)

{{% /tab %}}

{{% tab header="Go" %}}

```go
n, err := strconv.Atoi("42")            // 42, nil
m, err := strconv.ParseInt("ff", 16, 64)  // 255
s := strconv.Itoa(42)
f := fmt.Sprintf("%05d %.2f", 42, 3.14159)
// string(65) 是 "A"（rune → 字符串），不是 "65"
```

📘 [Go · strconv](https://pkg.go.dev/strconv)

{{% /tab %}}

{{% tab header="Python" %}}

```python
int("42"); int("ff", 16)      # 42；255
float("1.5"); float("nan")     # 1.5；nan
str(42); repr("a")              # "42"；"'a'"
f"{42:05d} {3.14159:.2f}"        # '00042 3.14'
int("4x")                         # 🛑 ValueError
```

📘 [Python · 格式化](https://docs.python.org/3/library/string.html#format-specification-mini-language)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
"42".toInt()             // 抛 NumberFormatException
"42".toIntOrNull()        // Int?
"ff".toInt(16)              // 255
42.toString(); 42.toString(2)   // "42"；"101010"
"%05d".format(42)                // "00042"
```

📘 [Kotlin · 字符串与数字](https://kotlinlang.org/docs/strings.html)

{{% /tab %}}

{{% tab header="Java" %}}

```java
Integer.parseInt("42");           // 抛 NumberFormatException 当非法
Integer.parseInt("ff", 16);         // 255
Integer.toString(42, 2);             // "101010"
String.format("%05d", 42);            // "00042"
Double.parseDouble("1.5");
```

📘 [JLS · 包装类](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Integer.html)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
std::stoi("42");                 // 抛 std::invalid_argument
std::stod("1.5");
int n; std::from_chars(s.data(), s.data()+s.size(), n);   // 无异常、无分配
std::string t = std::to_string(42);
std::string u = std::format("{:05d}", 42);   // C++20
```

📘 [cppreference · from_chars](https://en.cppreference.com/w/cpp/utility/from_chars)

{{% /tab %}}

{{% tab header="C" %}}

```c
long n = strtol("42", &end, 10);     /* 带错误检测 */
double d = strtod("1.5", NULL);
char buf[16];
snprintf(buf, sizeof buf, "%05d", 42);   /* "00042" */
/* atoi 没有错误检测，别用 */
```

📘 [`strtol`](https://en.cppreference.com/w/c/string/byte/strtol)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
parse(Int, "42")                 # 失败抛 ArgumentError
tryparse(Int, "4x")                # nothing（不抛）
parse(Int, "ff", base=16)           # 255
string(42); "$(42)"                  # "42"
using Printf; @sprintf("%05d", 42)    # "00042"
```

📘 [Julia · parse](https://docs.julialang.org/en/v1/base/numbers/#Base.parse)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
int.Parse("42");                  // 抛 FormatException 当非法
int.TryParse("4x", out int n);      // false（不抛）
Convert.ToInt32("42");
42.ToString("D5");                   // "00042"
$"{42:X}";                            // "2A"（十六进制）
// ⚠️ 默认按当前区域解析；跨系统用 CultureInfo.InvariantCulture
```

📘 [MS Learn · 分析数值字符串](https://learn.microsoft.com/en-us/dotnet/standard/base-types/parsing-numeric)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
int.parse("42");            // 抛 FormatException
int.tryParse("4x");          // null
int.parse("ff", radix: 16);   // 255
double.parse("1.5");
42.toString();                 // "42"
42.toRadixString(16);           // "2a"
```

📘 [Dart · int.parse](https://api.dart.dev/stable/dart-core/int/parse.html)

{{% /tab %}}

{{% tab header="R" %}}

```r
as.numeric("3.5")        # 3.5
as.numeric("a")           # NA + 警告（不抛错）
as.character(42)           # "42"
sprintf("%05d", 42)          # "00042"
format(3.14159, digits = 3)   # "3.14"
```

📘 [R · 转换函数](https://stat.ethz.ch/R-manual/R-devel/library/base/html/character.html)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const n = try std.fmt.parseInt(i32, "42", 10);
const f = try std.fmt.parseFloat(f64, "1.5");
var buf: [32]u8 = undefined;
const s = try std.fmt.bufPrint(&buf, "{d:0>5}", .{42});   // "00042"
```

📘 [Zig · std.fmt](https://ziglang.org/documentation/master/std/#std.fmt)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
print(tonumber("42"))        -- 42
print(tonumber("ff", 16))     -- 255
print(tonumber("x"))           -- nil（不抛错）
print(tostring(42))             -- "42"
print(string.format("%05d", 42)) -- "00042"
print("10" + 1)                  -- 11（自动转换）
```

📘 [Lua 5.5 · 字符串转换](https://www.lua.org/manual/5.5/manual.html#3.4.3)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
Number("42");                  // 42
Number.parseInt("ff", 16);      // 255
Number.parseFloat("3.14");
String(42);                      // "42"
(42).toString(2);                 // "101010"
(3.14159).toFixed(2);              // "3.14"
`${42}`;                            // "42"
```

📘 [TS · 字符串与数字](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
Number("42");               // 42
Number("");                  // 0     ⚠️
Number.parseInt("42px", 10);  // 42   ⚠️ 静默截断
String(42);                    // "42"
(42).toString(2);               // "101010"
(3.14159).toFixed(2);            // "3.14"
```

📘 [MDN · Number](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
intval("42");              // 42
intval("ff", 16);           // 255
floatval("3.14");
strval(42);                  // "42"
sprintf("%05d", 42);          // "00042"
number_format(1234.5678, 2);   // "1,234.57"
"10" + 1;                      // 11
```

📘 [PHP · 字符串转换](https://www.php.net/manual/en/language.types.string.php#language.types.string.conversion)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
Integer("42")          # 42（严格，失败抛 ArgumentError）
"ff".to_i(16)           # 255
Float("1.5")             # 1.5
42.to_s; 255.to_s(16)     # "42"；"ff"
"%05d" % 42                # "00042"
"%.2f" % 3.14159            # "3.14"
```

📘 [Ruby · Kernel#Integer](https://docs.ruby-lang.org/en/master/Kernel.html#method-i-Integer)

{{% /tab %}}

{{< /tabpane >}}

### 运算符优先级与求值顺序

优先级决定哪个运算符先结合，结合性决定同级运算符怎么分组，求值顺序决定子表达式按什么次序真正执行——这三件事在各语言里分道扬镳：C/C++ 有 15 到 17 级优先级却把求值顺序交给编译器（C 基本不指定，只有 `&&`、`||`、`?:`、`,` 与函数调用边界有定序；C++17 起才补上一部分定序规则），Rust、Python、JavaScript、Java、C# 把「从左到右」写进了规范，Swift 的实参顺序由 Swift Evolution 的 SE-0411、SE-0352 规定为从左到右，Go 只对函数调用、方法调用、接收操作与二元逻辑运算承诺词法次序，Ruby 只承诺实参值从左到右，Kotlin、Dart、Zig、Lua、PHP 在规范层面不承诺实参求值顺序。短路求值是另一条独立的分岔线：Rust、Swift、Go、Kotlin、Java、C#、Dart、Julia、Zig 要求两侧都是布尔值，Python、Lua、Ruby、JavaScript（以及运行时同源的 TypeScript）则让 `and`/`or`/`&&`/`||` 直接返回某个操作数，C 的 `&&`/`||` 返回 `int` 的 0 或 1、C++ 返回 `bool`、R 的 `&&`/`||` 返回单个逻辑值，PHP 又是另一类：它的 `&&`、`||`、`and`、`or`、`xor` 一律返回布尔值，惯用法靠的是短路与优先级而不是返回值。统计口径：按各语言官方优先级表的分组行数计，同一行内同级运算符算 1 组，表中若含 `clone`、`yield`、`lambda`、块、spread 等非算术条目也照官方原表计入（各表已注明）；18 门语言合计 **294** 个优先级分组，最少的是 Go（一元 + 5 个二元级 = 6 组），最多的是 PHP（30 组）。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的优先级与结合性由《The Rust Reference》的表达式章节给出，从最高的路径、方法调用一路排到赋值，最后是 `return`/`break`/闭包，共 19 组；比较运算符和区间运算符被规范强制要求加括号，`as` 与 `?` 又各自占一级，因此 `n as u8 + 1`、`x? as u8` 这类写法的读法常被搞错。它是静态编译期确定语法结构的语言，但求值顺序属于运行时语义：参考手册明确写了"多操作数表达式按源码从左到右求值"，所以 `f(a(), b(), c())` 的次序是有保证的。短路求值由 `&&`/`||` 提供，而 `?` 不是短路运算符，它是提前返回的语法糖。

| 优先级（高→低） | 运算符 / 表达式 | 结合性 |
| --- | --- | --- |
| 1 | 路径 `a::b` | 无 |
| 2 | 方法调用 `a.b()` | 无 |
| 3 | 字段访问 `a.b` | 左 |
| 4 | 函数调用、数组索引 `f()`, `a[i]` | 无 |
| 5 | `?`（错误/`None` 传播） | 无 |
| 6 | 一元 `-`, `!`, `*`, `&`, `&mut` | 无 |
| 7 | `as` | 左 |
| 8 | `*`, `/`, `%` | 左 |
| 9 | `+`, `-` | 左 |
| 10 | `<<`, `>>` | 左 |
| 11 | `&` | 左 |
| 12 | `^` | 左 |
| 13 | `\|` | 左 |
| 14 | `==`, `!=`, `<`, `>`, `<=`, `>=` | 必须加括号 |
| 15 | `&&` | 左 |
| 16 | `\|\|` | 左 |
| 17 | `..`, `..=` | 必须加括号 |
| 18 | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `\|=`, `^=`, `<<=`, `>>=` | 右 |
| 19 | `return`, `break`, 闭包（closure） | 无 |

```rust
fn side(tag: &str, v: bool) -> bool { println!("eval {tag}"); v }
fn arg(tag: &str, v: i32) -> i32 { println!("arg {tag}"); v }
fn f(a: i32, b: i32, c: i32) -> i32 { a + b + c }

fn main() {
    println!("{}", 2 + 3 * 4);              // 14
    println!("{}", 1 << 2 + 3);             // 32：+ 先于 <<
    println!("{}", (1 | 2) == 2);           // false：比较低于 |
    println!("{}", true || false && false); // true：&& 高于 ||
    println!("{}", 10 - 3 - 2);             // 5：减法左结合
    let (mut x, mut y) = ((), 0);
    x = y = 5;                              // 赋值右结合：y 得 5，x 得 ()
    println!("{:?} {}", x, y);              // () 5
    println!("{}", side("a", false) && side("b", true)); // eval a -> false
    println!("{}", f(arg("1", 1), arg("2", 2), arg("3", 3))); // arg 1/2/3 -> 6
}
```

`?` 的位置最容易看错：它排在函数调用与数组索引之下、一元运算符之上，所以 `f()?` 读作 `(f())?`，而 `x? as u8` 读作 `(x?) as u8`——`as` 比 `?` 低一级、比 `*` 高一级，于是 `n as u8 + 1` 其实是 `(n as u8) + 1`。比较运算符是 Rust 少见地禁止链写的地方：`a == b == c` 不合法，必须写成 `(a == b) == c`，编译器会在报错里直接要求括号；而 `0..10 == x` 之所以也要括起来，是因为比较的级别高于区间，不写括号就成了 `0..(10 == x)`。`&&` 与 `||` 短路且右侧按需求值，`?` 则按 `Try`/`FromResidual` 提前 `return`，所以 `a? + b?` 里的 `b?` 只在左侧成功时才执行；求值顺序上 Rust 是少数把"从左到右"写进规范的系统语言，二进制运算符 `a() + b()` 先算 `a()`，实参也按源码次序（唯一的例外是赋值：`a = b` 先算右侧的 `b`，再算左侧的 assignee），这一点与 C/C++ 的"未指定"形成鲜明对比。需要提醒的是，加括号只改变分组、不改变求值顺序，而 `as` 的截断/饱和与算术的调试期溢出检查都是运行时行为，与优先级无关。

📘 [Rust Reference · 表达式优先级与求值顺序](https://doc.rust-lang.org/reference/expressions.html#expression-precedence)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 不用"优先级数字"而用命名优先级组（precedence group），标准库一共声明了 13 组，从最高的 `BitwiseShiftPrecedence` 排到最低的 `AssignmentPrecedence`；没有声明结合性的组默认是 `none`，也就是不允许链写。它和 C 系最显眼的差别在移位：`<<`/`>>` 属于最高的 `BitwiseShiftPrecedence`，比 `*` 还高，所以 `1 << 2 + 3` 在 Swift 里是 7 而不是 32。类型层面的 `as`/`as?`/`is`、空合并 `??` 各有自己的组，属于编译期分组；运行时的短路则由 `&&`、`||` 与 `??` 的 `@autoclosure` 右侧共同完成。

| 优先级（高→低） | 优先级组与运算符 | 结合性 |
| --- | --- | --- |
| 1 | `BitwiseShiftPrecedence`：`<<`, `>>`, `&<<`, `&>>` | 无 |
| 2 | `MultiplicationPrecedence`：`*`, `/`, `%`, `&*`, `&` | 左 |
| 3 | `AdditionPrecedence`：`+`, `-`, `\|`, `^`, `&+`, `&-` | 左 |
| 4 | `RangeFormationPrecedence`：`..<`, `...` | 无 |
| 5 | `CastingPrecedence`：`is`, `as`, `as?`, `as!` | 无 |
| 6 | `NilCoalescingPrecedence`：`??` | 右 |
| 7 | `ComparisonPrecedence`：`==`, `!=`, `<`, `<=`, `>`, `>=`, `===`, `!==` | 无 |
| 8 | `LogicalConjunctionPrecedence`：`&&` | 左 |
| 9 | `LogicalDisjunctionPrecedence`：`\|\|` | 左 |
| 10 | `DefaultPrecedence`：自定义中缀运算符默认落点（与第 9 组之间无定序） | 无 |
| 11 | `TernaryPrecedence`：`? :` | 右 |
| 12 | `FunctionArrowPrecedence`：`->` | 右 |
| 13 | `AssignmentPrecedence`：`=`, `+=`, `-=`, `*=`, `/=`, `%=` | 右 |

```swift
func side(_ tag: String, _ v: Bool) -> Bool { print("eval \(tag)"); return v }
func arg(_ tag: String, _ v: Int) -> Int { print("arg \(tag)"); return v }
func f(_ a: Int, _ b: Int, _ c: Int) -> Int { a + b + c }

print(2 + 3 * 4)              // 14
print(1 << 2 + 3)             // 7：<< 高于 +
print((1 | 2) == 2)           // false
print(true || false && false) // true
print(10 - 3 - 2)             // 5
let a: Int? = nil
let b: Int? = 7
print(a ?? b ?? 0)            // 7：?? 右结合
print(side("a", false) && side("b", true))  // eval a -> false
print(f(arg("1", 1), arg("2", 2), arg("3", 3)))  // arg 1/2/3 -> 6
```

命名优先级组的好处是自定义运算符也能落进同一套关系里：用 `precedencegroup` 声明 `higherThan`/`lowerThan` 之后，`+-` 这样的新运算符能自动和 `+`、`*` 排好队，而文档特别提醒"优先级关系不必是线性的"——`DefaultPrecedence` 与 `LogicalDisjunctionPrecedence` 都只声明了"高于 `TernaryPrecedence`"，彼此之间没有定序，所以这两个组里的运算符相邻出现时必须加括号。`ComparisonPrecedence`、`CastingPrecedence`、`RangeFormationPrecedence` 都没有结合性，`a == b == c` 会直接编译报错，要写 `(a == b) == c`。`??` 是右结合，且右侧参数声明为 `@autoclosure`，只有左侧为 `nil` 时才求值，因此 `a ?? b ?? 0` 是 `a ?? (b ?? 0)` 并且天然短路；`?.` 属于后缀链式调用，`a?.b ?? 0` 中 `?.` 先结合。实参求值顺序在《The Swift Programming Language》里没有专门成段说明，但 Swift Evolution 的 SE-0411 把它规定为「显式实参从左到右，随后才是默认实参与 formal access 实参」，SE-0352 也称它是"Swift 长期以来的从左到右求值顺序"，本机 Swift 6.4 实测一致。

📘 [Swift 标准库 · 运算符声明与优先级组](https://developer.apple.com/documentation/swift/operator-declarations)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的优先级表只有 5 个二元级别加上"一元最高"，是 18 门语言里最扁的：5 级 `*` `/` `%` `<<` `>>` `&` `&^`，4 级 `+` `-` `|` `^`，3 级比较，2 级 `&&`，1 级 `||`。因为 `<<` 与 `*` 同级而不是像 C 那样低于 `+`，`1 << 2 + 3` 在 Go 里是 7 而不是 32。Go 没有三元运算符，`++`/`--` 是语句而不是表达式，这消掉了"同一表达式里两次自增"整类未定义行为。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | 一元 `+`, `-`, `!`, `^`, `*`, `&`, `<-` | 无 |
| 2 | 5 级 `*`, `/`, `%`, `<<`, `>>`, `&`, `&^` | 左 |
| 3 | 4 级 `+`, `-`, `\|`, `^` | 左 |
| 4 | 3 级 `==`, `!=`, `<`, `<=`, `>`, `>=` | 左 |
| 5 | 2 级 `&&` | 左 |
| 6 | 1 级 `\|\|` | 左 |

```go
func side(tag string, v bool) bool { fmt.Println("eval", tag); return v }
func arg(tag string, v int) int    { fmt.Println("arg", tag); return v }
func f(a, b, c int) int            { return a + b + c }

fmt.Println(2 + 3*4)                 // 14
fmt.Println(1<<2 + 3)                // 7：<< 与 * 同级，高于 +
fmt.Println((1 | 2) == 2)            // false：比较低于 |
fmt.Println(true || false && false)  // true：&& 高于 ||
fmt.Println(10 - 3 - 2)              // 5：左结合
fmt.Println(side("a", false) && side("b", true)) // eval a -> false
fmt.Println(f(arg("1", 1), arg("2", 2), arg("3", 3))) // arg 1/2/3 -> 6
```

Go spec 的"Order of evaluation"一节把承诺划得很清楚：函数调用、方法调用、接收操作与二元逻辑运算一律按词法从左到右求值，所以 `f(arg1, arg2, arg3)` 的打印次序有保证；但其余操作数与索引、映射赋值的顺序是未指定的，规范自己给了例子 `x := []int{a, f()}` 可能是 `[1, 2]` 也可能是 `[2, 2]`，`m := map[int]int{a: 1, a: 2}` 可能是 `{2: 1}` 也可能是 `{2: 2}`。因此不要在同一个表达式里让多个子表达式互相写同一个变量，需要确定的次序就拆成多条语句。`&&`/`||` 只接受 `bool`，没有真值转换，`if 1 {}` 不合法；没有三元运算符时用 `if`/`else` 或带返回值的立即执行函数代替。

📘 [Go spec · 求值顺序与运算符优先级](https://go.dev/ref/spec#Order_of_evaluation)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的优先级表在语言参考 6.17 节，从高到低共 18 行，最低的两行是 `lambda` 与 `:=`；`**` 是唯一的右结合算术运算符，并且"向左比一元负号紧、向右比一元负号松"，所以 `-2 ** 2` 是 -4 而 `2 ** -1` 是 0.5。`and`/`or`/`not` 返回操作数而不是布尔值，比较运算支持链式写法，三元运算用条件表达式 `a if c else b` 表达。整页的行为都是运行时的：语法结构在编译期定（`.pyc`），但求值与短路发生在执行期。

| 优先级（高→低） | 运算符 / 表达式 | 结合性 |
| --- | --- | --- |
| 1 | `(expr)`, `[expr]`, `{k: v}`, `{expr}` | 无 |
| 2 | `x[i]`, `x[i:j]`, `x(...)`, `x.attr` | 无 |
| 3 | `await x` | 无 |
| 4 | `**` | 右 |
| 5 | `+x`, `-x`, `~x` | 无 |
| 6 | `*`, `@`, `/`, `//`, `%` | 左 |
| 7 | `+`, `-` | 左 |
| 8 | `<<`, `>>` | 左 |
| 9 | `&` | 左 |
| 10 | `^` | 左 |
| 11 | `\|` | 左 |
| 12 | `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==` | 左（可链式） |
| 13 | `not x` | 无 |
| 14 | `and` | 左 |
| 15 | `or` | 左 |
| 16 | `a if c else b` | 右 |
| 17 | `lambda` | 无 |
| 18 | `:=` | 无 |

```python
def side(tag, v):
    print("eval", tag)
    return v

def arg(tag, v):
    print("arg", tag)
    return v

def f(a, b, c):
    return a + b + c

print(2 + 3 * 4)          # 14
print(2 ** 3 ** 2)        # 512：** 右结合
print(-2 ** 2)            # -4：** 高于一元负号
print(1 << 2 + 3)         # 32：+ 高于 <<
print(True or False and False)  # True：and 高于 or
print([] or "default")    # default：or 返回操作数
print(1 < 2 < 3)          # True：链式比较
print(side("a", False) and side("b", True))  # eval a -> False
print(f(arg("1", 1), arg("2", 2), arg("3", 3)))  # arg 1/2/3 -> 6
```

语言参考 6.16 节把求值顺序写得非常直白："Python evaluates expressions from left to right"，并且赋值语句"先算右边再算左边"；同一表格还注明同级运算符一般左结合，只有幂与条件表达式右结合。`and`/`or` 短路且返回操作数本身，这也是 `x or default` 这类写法的依据，但 `0 or 5` 得到 5、`[] or "default"` 得到字符串，判断"有没有值"时请用 `is None` 而不是真值判断。`not` 的优先级低于比较，所以 `not a == b` 是 `not (a == b)`；`and` 比 `or` 紧，`a and b or c` 会被读成 `(a and b) or c`，想表达"要么 a、要么 b 和 c"就必须写 `a or (b and c)`。链式比较 `0 < x < 10` 只对中间操作数求值一次，但如果中间是带副作用的调用，请改用显式的 `and` 避免误读。

📘 [Python 语言参考 · 求值顺序与运算符优先级](https://docs.python.org/3/reference/expressions.html#operator-precedence)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的运算符表在官方语法（kotlinlang.org/grammar）的 Expressions 一节，从高到低共 15 级（官方表把 spread `*` 也单列一行），从 Postfix（`++`, `--`, `.`, `?.`, `?`, `[]`, `()`）排到 Assignment。Kotlin 没有 `<<`/`>>` 这样的移位运算符，移位是中缀函数 `shl`/`shr`/`ushr`，而所有中缀函数共用同一级——它比 Range 低、比 Elvis `?:` 高，所以 `1 shl 2 + 3` 先算加法。空安全的两件套里 `?.` 属于 Postfix、`?:` 属于 Elvis，`?:` 是真短路；这属于编译期固定的语法分组，运行时只决定 `?:` 选哪边。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | Postfix：`++`, `--`, `.`, `?.`, `?`, `[]`, `()` | 无 |
| 2 | Prefix：`-`, `+`, `++`, `--`, `!`, label | 无 |
| 3 | Type RHS：`:`、`as`、`as?`（`asExpression`） | 无 |
| 4 | Multiplicative：`*`, `/`, `%` | 左 |
| 5 | Additive：`+`, `-` | 左 |
| 6 | Range：`..`, `..<` | 无 |
| 7 | Infix function：任意 `simpleIdentifier`（`shl`, `shr`, `and`, `or`, `xor`, `step`, `until`, `downTo`） | 无 |
| 8 | Elvis：`?:` | 左 |
| 9 | Named checks：`in`, `!in`, `is`, `!is` | 无 |
| 10 | Comparison：`<`, `>`, `<=`, `>=` | 无 |
| 11 | Equality：`==`, `!=`, `===`, `!==` | 无 |
| 12 | Conjunction：`&&` | 左 |
| 13 | Disjunction：`\|\|` | 左 |
| 14 | Spread operator：`*`（只出现在值实参位置的前缀写法） | 无 |
| 15 | Assignment：`=`, `+=`, `-=`, `*=`, `/=`, `%=` | 无 |

```kotlin
println(2 + 3 * 4)               // 14
println(1 shl 2 + 3)             // 32：shl 是 infix，优先级低于 +
println((1..5 step 2).toList())  // [1, 3, 5]：Range 先于 infix，读作 (1..5) step 2
println(true || false && false)  // true：&& 高于 ||
val a: String? = null
println(a?.length ?: 0)          // 0：?. 先结合，?: 兜底
val b: Int? = 7
println(b ?: 0)                  // 7：?: 短路，不取右边
```

说明：`1 shl 2 + 3` 是最容易踩的一脚——`shl` 与 `and`/`or`/`step` 一样落在 Infix function 这一级，低于 Additive，所以先算 `2 + 3` 再移位得到 32，想要 `(1 shl 2) + 3` 必须自己加括号。`?:` 只在左边为 `null` 时才求值右边，因此 `a?.length ?: 0` 既是空安全又是短路的，常写成 `val n = a?.length ?: return` 做提前返回。官方语法把 `?:` 写成 `infixFunctionCall (elvis infixFunctionCall)*` 这样的平铺产生式，所以它按左结合解析：`a ?: b ?: c` 读作 `(a ?: b) ?: c`（两种分组的结果相同）。Named checks（`in`, `is`）比 Elvis 还低，所以 `x ?: y in set` 读作 `x ?: (y in set)`；比较与相等分成两级，`a < b == c` 这种写法要靠括号表达真实意图。Kotlin 自定义中缀函数全在同一级、且没有结合性，链写 `a foo b bar c` 会编译报错，需要显式括号，这也是给 DSL 加中缀函数时最容易忽略的约束。求值顺序方面，Kotlin 文档只规定了优先级与结合性，没有对实参求值顺序给出明文承诺，JVM 与 ART 后端实际按从左到右依次求值，但把它当成语言保证并不安全。另外要澄清一处常见误读：官方表把 spread `*` 单列成一行，但它并不是二元运算符，而是值实参 `valueArgument` 产生式里的前缀写法，紧跟被展开的表达式，因此不参与二元结合性讨论，也不会与 `*` 乘法混淆。

📘 [Kotlin 官方语法 · 表达式与优先级](https://kotlinlang.org/grammar/#expressions)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的优先级由 JLS 的表达式语法隐式给出，Oracle 教程把它整理成 14 级，从 postfix 排到 assignment；`?:` 与赋值右结合，关系运算和相等运算分成两级。求值顺序则是 JLS 15.7 明确写下的：左操作数先算、参数列表从左到右，而且"求值顺序尊重括号与优先级"。需要特别区分的是，JLS 17.4.5 的 happens-before 讲的是多线程之间的内存可见性，与这里的单线程求值顺序是两套完全不同的概念。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | postfix：`expr++`, `expr--` | 无 |
| 2 | unary：`++expr`, `--expr`, `+expr`, `-expr`, `~`, `!` | 右 |
| 3 | multiplicative：`*`, `/`, `%` | 左 |
| 4 | additive：`+`, `-` | 左 |
| 5 | shift：`<<`, `>>`, `>>>` | 左 |
| 6 | relational：`<`, `>`, `<=`, `>=`, `instanceof` | 左 |
| 7 | equality：`==`, `!=` | 左 |
| 8 | bitwise AND：`&` | 左 |
| 9 | bitwise XOR：`^` | 左 |
| 10 | bitwise OR：`\|` | 左 |
| 11 | logical AND：`&&` | 左 |
| 12 | logical OR：`\|\|` | 左 |
| 13 | ternary：`? :` | 右 |
| 14 | assignment：`=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `^=`, `\|=`, `<<=`, `>>=`, `>>>=` | 右 |

```java
static int arg(String tag, int v) { System.out.println("arg " + tag); return v; }
static int f(int a, int b, int c) { return a + b + c; }

System.out.println(2 + 3 * 4);              // 14
System.out.println(1 << 2 + 3);             // 32：+ 高于 <<
System.out.println((1 | 2) == 2);           // false：== 高于 |
System.out.println(1 < 2 == true);          // true：关系先于相等
System.out.println(true || false && false); // true：&& 高于 ||
System.out.println(f(arg("1", 1), arg("2", 2), arg("3", 3))); // arg 1/2/3 -> 6
```

JLS 15.7 的组织方式本身就是一张排雷表：15.7.1 规定"先求左操作数"，15.7.2 规定"先算操作数再做运算"，15.7.3 规定"求值顺序尊重括号与优先级"，15.7.4 规定"参数列表从左到右求值"，15.7.5 覆盖其余表达式；因此 `f(arg1, arg2, arg3)` 与 `a() + b()` 的次序都有保证，这比 C/C++ 舒服得多。`&&` 与 `||` 短路且只接受 `boolean`，`?:` 只求值被选中的那一支，赋值右结合让 `a = b = c` 合法。最容易吃亏的是位运算与比较的搭配：`if ((flags & MASK) == 1)` 的括号不能省，因为 `==` 的优先级高于 `&`，漏掉括号会直接编译失败（`int & boolean` 类型不匹配）。另外要记住 `&&` 的短路不能被当成"顺序保证"来依赖副作用——需要确定的次序就拆成多条语句。

📘 [JLS 第 15 章 · 求值顺序](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.7)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的优先级表由 cppreference 整理为 17 级，从 `::` 一路到逗号运算符，`?:` 与赋值右结合、逗号左结合，C++20 的 `<=>` 单独占一级并排在移位与关系之间。C++ 最核心的一条原则是"优先级与结合性只决定分组，不决定求值顺序"：标准原文写明操作数与函数实参的求值顺序是未指定的，C++17 才补上若干条定序规则。这正是"编译期定分组、运行时由实现定顺序"的典型分工。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | `a::b` | 左 |
| 2 | 后缀 `a++`, `a--`, `type(a)`, `type{a}`, `a()`, `a[]`, `a.b`, `a->b` | 左 |
| 3 | 前缀 `++a`, `--a`, `+a`, `-a`, `!a`, `~a`, `(type)a`, `*a`, `&a`, `sizeof`, `co_await`, `new`, `new[]`, `delete`, `delete[]` | 右 |
| 4 | `a.*b`, `a->*b` | 左 |
| 5 | `*`, `/`, `%` | 左 |
| 6 | `+`, `-` | 左 |
| 7 | `<<`, `>>` | 左 |
| 8 | `<=>` | 左 |
| 9 | `<`, `<=`, `>`, `>=` | 左 |
| 10 | `==`, `!=` | 左 |
| 11 | `&` | 左 |
| 12 | `^` | 左 |
| 13 | `\|` | 左 |
| 14 | `&&` | 左 |
| 15 | `\|\|` | 左 |
| 16 | `a ? b : c`, `throw`, `co_yield`, `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`, `^=`, `\|=` | 右 |
| 17 | `,` | 左 |

```cpp
#include <cstdio>
#include <compare>
int arg(const char *t, int v) { std::printf("arg %s\n", t); return v; }
int f(int a, int b, int c) { return a + b + c; }

std::printf("%d\n", 2 + 3 * 4);      // 14
std::printf("%d\n", 1 << 2 + 3);     // 32：+ 高于 <<
std::printf("%d\n", (1 | 2) == 2);   // 0：== 高于 |
std::printf("%d\n", 1 || 0 && 0);    // 1：&& 高于 ||
std::printf("%d\n", (1 <=> 2) < 0);  // 1：C++20 三路比较
std::printf("%d\n", -1 < 1u);        // 0：有符号被转成无符号
std::printf("%d\n", f(arg("1", 1), arg("2", 2), arg("3", 3))); // 顺序未指定
```

cppreference 的原话是"操作数与函数实参的求值顺序是未指定的，编译器可以任意次序求值，甚至同一个表达式下次求值换一种次序"，并且强调"不要把结合性误当成求值顺序"：`a() + b() + c()` 因为 `+` 左结合而解析成 `(a() + b()) + c()`，但运行时 `c()` 可能最先算。C++17 起补上的定序规则包括：`E1[E2]` 中 `E1` 先于 `E2`；移位 `E1 << E2` 中 `E1` 先于 `E2`；赋值 `E1 = E2` 中 `E2` 先于 `E1`；`&&`、`||`、`,`、`?:` 的左操作数先于右侧；函数实参之间是 indeterminately sequenced——也就是说 `f(++i, ++i)` 在 C++17 之前是 UB、C++17 起变成"顺序未指定但不会交错"，而 `i = ++i + i++;` 仍然是 UB，这类写法永远不要写。日常规范是：涉及位运算与比较、移位与加法、三角与赋值时一律加括号，编译器的 `-Wparentheses` 系列警告（clang 的 `-Wshift-op-parentheses`、`-Wlogical-op-parentheses`）本来就是为这些陷阱准备的。

📘 [cppreference · 求值顺序](https://en.cppreference.com/w/cpp/language/eval_order)

{{% /tab %}}

{{% tab header="C" %}}

C 的优先级表在 cppreference 上整理为 15 级，从后缀 `++`/`--` 到逗号运算符，`?:` 与赋值右结合；C 的移位低于加法，`1 << 2 + 3` 是 32，这与 Go、Swift、Zig 正好相反。真正要小心的是求值顺序：C 标准规定运算符的操作数、函数实参、子表达式的求值顺序都是未指定的（只有 `&&`、`||`、`?:`、`,` 与函数调用边界这几处有定序），所以 `i++ + i++` 是未定义行为。C11 起规范引入 sequenced-before（定序于）的措辞来表述同一件事，"序列点"这个说法在 C11 里仍然保留，结论没有变。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | 后缀 `++`, `--`, `()`, `[]`, `.`, `->`, `(type){list}` | 左 |
| 2 | 前缀 `++`, `--`, `+`, `-`, `!`, `~`, `(type)`, `*`, `&`, `sizeof`, `_Alignof` | 右 |
| 3 | `*`, `/`, `%` | 左 |
| 4 | `+`, `-` | 左 |
| 5 | `<<`, `>>` | 左 |
| 6 | `<`, `<=`, `>`, `>=` | 左 |
| 7 | `==`, `!=` | 左 |
| 8 | `&` | 左 |
| 9 | `^` | 左 |
| 10 | `\|` | 左 |
| 11 | `&&` | 左 |
| 12 | `\|\|` | 左 |
| 13 | `?:` | 右 |
| 14 | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`, `^=`, `\|=` | 右 |
| 15 | `,` | 左 |

```c
#include <stdio.h>
static int arg(const char *t, int v) { printf("arg %s\n", t); return v; }
static int f(int a, int b, int c) { return a + b + c; }

printf("%d\n", 2 + 3 * 4);    /* 14 */
printf("%d\n", 1 << 2 + 3);   /* 32：+ 高于 << */
printf("%d\n", (1 | 2) == 2); /* 0：== 高于 | */
printf("%d\n", 1 || 0 && 0);  /* 1：&& 高于 || */
printf("%d\n", 1 ? 2 : 3);    /* 2：?: 右结合 */
printf("%d\n", (1, 2));       /* 2：逗号运算符最低 */
printf("%d\n", f(arg("1", 1), arg("2", 2), arg("3", 3))); /* 顺序未指定 */
```

C 的求值顺序在规范层面基本不指定：cppreference 写明"任何 C 运算符的操作数，包括函数调用表达式中的实参以及任意表达式中的子表达式，其求值顺序都是未指定的"（下文注明者除外），并且明确说 C 里没有"从左到右"或"从右到左"的求值概念——这与结合性完全是两件事。因此 `i++ + i++`、`a[i] = i++`、`f(++i, ++i)` 都是未定义行为；即便某个编译器这次从左到右求值，换个优化档位或换个编译器就可能变。位运算与比较的坑同样经典：`if (flags & MASK == 1)` 会先算 `MASK == 1`，位运算与移位混写 `1 << n + 1` 会先算加法，逗号运算符 `x = (a, b)` 只取最后一个值。实用建议是把编译警告开足：clang 会针对 `1 << 2 + 3` 报 `-Wshift-op-parentheses`、针对 `1 || 0 && 0` 报 `-Wlogical-op-parentheses`，把这些警告当错误处理，绝大多数优先级陷阱在编译期就会被拦下来。

📘 [cppreference · C 求值顺序](https://en.cppreference.com/w/c/language/eval_order)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的优先级表在手册的 Operator Precedence and Associativity 一节，从高到低共 14 行，比较运算显式标为 non-associative。与 C 系相反，Julia 的移位高于乘法与加法，`1 << 2 + 3` 是 7；`^` 高于一元负号，`-2 ^ 2` 是 -4。链式比较 `1 < 2 < 3` 是特例：中间项只求值一次，但手册明说链式比较内部的求值顺序是未定义的。Julia 是动态类型、运行时多重派发的语言，优先级在解析期固定，求值顺序则基本不做承诺。

| 优先级（高→低） | 运算符 / 语法 | 结合性 |
| --- | --- | --- |
| 1 | `.` 与 `::` | 左 |
| 2 | `^` | 右 |
| 3 | 一元 `+`, `-`, `!`, `~`, `¬`, `√`, `∛`, `∜`, `⋆`, `±`, `∓`, `<:`, `>:` | 右 |
| 4 | `<<`, `>>`, `>>>` | 左 |
| 5 | `//` | 左 |
| 6 | `*`, `/`, `%`, `&`, `\`, `÷` | 左 |
| 7 | `+`, `-`, `\|`, `⊻` | 左 |
| 8 | `:`, `..` | 左 |
| 9 | `\|>` | 左 |
| 10 | `<\|` | 右 |
| 11 | `>`, `<`, `>=`, `<=`, `==`, `===`, `!=`, `!==`, `<:` | 无结合 |
| 12 | `&&` 后接 `\|\|` 后接 `?` | 右 |
| 13 | `=>` | 右 |
| 14 | `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `\=`, `^=`, `÷=`, `%=`, `\|=`, `&=`, `⊻=`, `<<=`, `>>=`, `>>>=` | 右 |

```julia
2 + 3 * 4          # 14
2 ^ 3 ^ 2          # 512：^ 右结合
-2 ^ 2             # -4：^ 高于一元负号
1 << 2 + 3         # 7：移位高于加法
true || false && false   # true
1 < 2 < 3          # true：链式比较，中间项只求值一次
Base.operator_precedence(:+), Base.operator_precedence(:*), Base.operator_precedence(:.)
# (11, 12, 17)：手册给出的数值优先级查询
```

手册除了给出表，还提供了运行时查询工具：`Base.operator_precedence(op)` 返回数值优先级（数字越大越紧），`Base.operator_associativity(op)` 返回 `:left`、`:right` 或 `:none`，遇到自定义运算符时可以直接问解释器。`&&` 与 `||` 是短路运算符，并且两侧必须都是 `Bool`（Control Flow 一节的 Short-Circuit Evaluation），`false && error()` 不会触发错误。求值顺序方面 Julia 的手册只对少数构造明确表态：链式比较内部的顺序是未定义的、关键字参数默认值按从左到右求值；一般表达式的函数实参求值顺序并没有写进手册承诺（JuliaLang/julia#49067 一直在跟踪这个文档缺口），所以有副作用的实参不要互相依赖，需要确定次序就拆成多条语句或显式用 `begin`/`end` 包成块来固定。

📘 [Julia 手册 · 运算符优先级与结合性](https://docs.julialang.org/en/v1/manual/mathematical-operations/#Operator-Precedence-and-Associativity)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的优先级表在 MS Learn 的 C# 运算符页，共 17 行，从 Primary 排到 Assignment 与 lambda；`??`、`?:`、赋值三者都右结合，`is`/`as` 与关系运算同级。C# 的求值顺序是明确的：同一优先级的运算符按词法顺序求值，页面还专门给了一张"表达式 → 求值顺序"的对照表（`a + b * c` 对应 `a, b, c, *, +`）。它属于编译期固定分组、运行时严格从左到右的语言。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | Primary：`x.y`, `f(x)`, `a[i]`, `x?.y`, `x?[y]`, `x++`, `x--`, `x!`, `new`, `typeof`, `checked`, `unchecked`, `default`, `nameof`, `delegate`, `sizeof`, `stackalloc`, `x->y` | 左 |
| 2 | Unary：`+x`, `-x`, `!x`, `~x`, `++x`, `--x`, `^x`, `(T)x`, `await`, `&x`, `*x`, `true`, `false` | 右 |
| 3 | Range：`x..y` | 无 |
| 4 | `switch`, `with` 表达式 | 无 |
| 5 | Multiplicative：`*`, `/`, `%` | 左 |
| 6 | Additive：`+`, `-` | 左 |
| 7 | Shift：`<<`, `>>`, `>>>` | 左 |
| 8 | Relational and type-testing：`<`, `>`, `<=`, `>=`, `is`, `as` | 左 |
| 9 | Equality：`==`, `!=` | 左 |
| 10 | `&`（逻辑与按位） | 左 |
| 11 | `^`（逻辑异或按位） | 左 |
| 12 | `\|`（逻辑或按位） | 左 |
| 13 | Conditional AND：`&&` | 左 |
| 14 | Conditional OR：`\|\|` | 左 |
| 15 | Null-coalescing：`??` | 右 |
| 16 | Conditional：`c ? t : f` | 右 |
| 17 | Assignment and lambda declaration：`=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `\|=`, `^=`, `<<=`, `>>=`, `>>>=`, `??=`, `=>` | 右 |

```csharp
static int Arg(string t, int v) { Console.WriteLine("arg " + t); return v; }
static int F(int a, int b, int c) { return a + b + c; }

Console.WriteLine(2 + 3 * 4);      // 14
Console.WriteLine(1 << 2 + 3);     // 32：+ 高于 <<
Console.WriteLine((1 | 2) == 2);   // False：== 高于 |
Console.WriteLine(true || false && false);   // True：&& 高于 ||
int? n = null;
Console.WriteLine(n ?? 0);         // 0：?? 只在左侧为 null 时取右边
Console.WriteLine(F(Arg("1", 1), Arg("2", 2), Arg("3", 3)));  // arg 1/2/3 -> 6
```

MS Learn 的写法是"同一优先级的运算符按词法顺序求值"，并配了一张逐步展开的求值表，所以 `a + b * c` 的次序是 `a, b, c, *, +`，`a / (b + c) * d` 是 `a, b, c, +, /, d, *`——括号与优先级决定分组，分组再决定每一步何时算，两者在这里是一致且可预测的。`&&` 与 `||` 短路、只接受 `bool`；`??` 右结合并短路，只在左侧为 `null` 时求值右侧，因此 `a ?? b ?? c` 读作 `a ?? (b ?? c)`；`?.` 与 `?[]` 是 Primary 级的空安全链，`a?.b ?? 0` 中先做成员访问再兜底。最容易踩的仍是位运算与比较：`x & y == 0` 会先算 `y == 0`，因为 `==` 的级别高于 `&`，必须写成 `(x & y) == 0`；同理 `x | y != 0`、`flags & MASK == MASK` 都需要括号，否则是编译错误而不是悄悄算错——这一点比 C 幸运。

📘 [MS Learn · C# 运算符与优先级](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 官方运算符表（dart.dev/language/operators）给出 17 行，从 unary postfix 排到 spread；条件表达式 `? :` 右结合、赋值右结合，关系与相等两行都标为无结合。`??` 只对 `null` 生效，`&&`/`||` 短路，`?.`、`?[]`、`?..` 组成空安全链。文档自己声明这张表只是"近似值"，权威定义在 Dart 语言规范的语法部分。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | unary postfix：`expr++`, `expr--`, `()`, `[]`, `?[]`, `.`, `?.`, `!` | 无 |
| 2 | unary prefix：`-expr`, `!expr`, `~expr`, `++expr`, `--expr`, `await expr` | 无 |
| 3 | multiplicative：`*`, `/`, `%`, `~/` | 左 |
| 4 | additive：`+`, `-` | 左 |
| 5 | shift：`<<`, `>>`, `>>>` | 左 |
| 6 | bitwise AND：`&` | 左 |
| 7 | bitwise XOR：`^` | 左 |
| 8 | bitwise OR：`\|` | 左 |
| 9 | relational and type test：`>=`, `>`, `<=`, `<`, `as`, `is`, `is!` | 无 |
| 10 | equality：`==`, `!=` | 无 |
| 11 | logical AND：`&&` | 左 |
| 12 | logical OR：`\|\|` | 左 |
| 13 | if-null：`??` | 左 |
| 14 | conditional：`c ? a : b` | 右 |
| 15 | cascade：`..`, `?..` | 左 |
| 16 | assignment：`=`, `*=`, `/=`, `+=`, `-=`, `&=`, `^=`, `\|=`, `??=` | 右 |
| 17 | spread：`...`, `...?` | 无 |

```dart
int arg(String t, int v) { print('arg $t'); return v; }
int f(int a, int b, int c) => a + b + c;

print(2 + 3 * 4);              // 14
print(1 << 2 + 3);             // 32：+ 高于 <<
print((1 | 2) == 2);           // false：== 高于 |
print(true || false && false); // true：&& 高于 ||
String? name;
print(name ?? 'Guest');        // Guest：?? 只把 null 当作缺失
print(f(arg('1', 1), arg('2', 2), arg('3', 3)));  // arg 1/2/3 -> 6
```

文档给的教学例子很典型：`n % i == 0 && d % i == 0` 与 `(n % i == 0) && (d % i == 0)` 等价，因为乘法类运算符高于相等、相等高于 `&&`——但作者仍然建议写括号。要留意几处与 C 系不同的地方：`??` 在 Dart 表里是左结合，`a ?? b ?? c` 读作 `(a ?? b) ?? c`（结果一样，但与 C# 的右结合不同）；关系与类型测试同处一级且无结合，`a is int == true` 这种写法没有意义，必须先括号；`..` 与 `?..` 是 cascade，它的求值结果是被操作对象本身，所以只能出现在语句位置；`...`/`...?` 严格说不是运算符而是集合字面量语法，因此没有优先级，`[...a + b]` 里的 `a + b` 会整体先算。最后别忘了 Dart 编译到 Web 时 `int` 由 64 位 double 表示、算术在 2^53 以内精确（超过就丢精度），而位运算与移位会按 JavaScript 语义把操作数截断成 32 位无符号，优先级没变，但结果位宽会和 VM 不同。另外，Dart 官方运算符页只谈优先级与结合性，没有对实参求值顺序作明文承诺，需要确定次序时请先引入中间变量。

📘 [Dart · 运算符与优先级](https://dart.dev/language/operators)

{{% /tab %}}

{{% tab header="R" %}}

R 的优先级表在 base 包的 `?Syntax` 文档里，从高到低共 18 行，`^` 右结合、`<-`/`<<-`/`=` 右结合，`:` 高于 `*` 与 `+`，所以 `1:3 + 1` 是 `(1:3) + 1` 得到 2 3 4。文档同时写明"同一行内、优先级相同的运算符从左到右求值，除非另有说明"。R 又是惰性求值语言：函数实参是 promise，只有真正被用到时才求值，这让"求值顺序"在这里等同于"何时求值"。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | `::`, `:::` | 左 |
| 2 | `$`, `@` | 左 |
| 3 | `[`, `[[` | 左 |
| 4 | `^` | 右 |
| 5 | 一元 `-`, `+` | 右 |
| 6 | `:` | 左 |
| 7 | `%any%`, `\|>` | 左 |
| 8 | `*`, `/` | 左 |
| 9 | `+`, `-` | 左 |
| 10 | `<`, `>`, `<=`, `>=`, `==`, `!=` | 左 |
| 11 | `!` | 右 |
| 12 | `&`, `&&` | 左 |
| 13 | `\|`, `\|\|` | 左 |
| 14 | `~` | 无 |
| 15 | `->`, `->>` | 右 |
| 16 | `<-`, `<<-` | 右 |
| 17 | `=` | 右 |
| 18 | `?` | 无 |

```r
2 + 3 * 4          # 14
2 ^ 3 ^ 2          # 512：^ 右结合
-2 ^ 2             # -4：^ 高于一元负号
1:3 + 1            # 2 3 4：: 高于 +
TRUE || TRUE && FALSE   # TRUE：&& 高于 ||
f <- function(x) 42
f(stop("never"))   # 42：实参是 promise，没被用到就不求值
x <- 5; (x <- x + 1) * 2   # 12：括号强制赋值先发生
```

R Language Definition 的 Argument evaluation 一节原文说"R 对函数实参有一种惰性求值：参数在被需要之前不会被求值"，因此 `f(stop("never"))` 不会报错，而 `if (FALSE) stop()` 也不会——这是 R 里做条件式报错、写默认参数与 NSE 的基础。`?Syntax` 文档给出的经典例子是 `!1:10 %in% c(2, 3, 5, 7)`：特殊运算符 `%any%` 的优先级高于 `!`，所以它等价于 `!(1:10 %in% c(2, 3, 5, 7))`，文档仍然建议显式写括号。另一条硬性建议是不要混用 `<-` 与 `=`：`=` 的优先级低于 `<-`，`x <- y = 5` 会直接报错。`&&`/`||` 只看第一个元素并短路，`&`/`|` 是向量化的，这在条件里混用会造成 `the condition has length > 1` 警告；`:` 比 `+` 紧这一点也常让 `1:n + 1` 这类写法与直觉不符，写 `1:(n + 1)` 更清楚。

📘 [R · 运算符语法与优先级](https://search.r-project.org/R/refmans/base/html/Syntax.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 语言参考的 Precedence 一节只给出一张 12 行的裸表，从最高的 `x()`, `x[]`, `x.y`, `x.*`, `x.?` 一路到最低的赋值。`and`/`or` 是关键字逻辑运算符且要求两侧都是 `bool`；`orelse` 与 `catch` 和 `&`, `^`, `|` 同处一行，级别高于比较，因此 `a orelse b == c` 读作 `(a orelse b) == c`。语言参考在优先级之外非常克制：它没有对操作数与实参的求值顺序作任何规定。

| 优先级（高→低） | 运算符 / 语法 | 结合性 |
| --- | --- | --- |
| 1 | `x()`, `x[]`, `x.y`, `x.*`, `x.?` | 左 |
| 2 | `a!b`（错误联合表达式 `E!T`，语法产生式 `ErrorUnionExpr`） | 无 |
| 3 | `x{}`（初始化列表） | 无 |
| 4 | `!x`, `-x`, `-%x`, `~x`, `&x`, `?x` | 无 |
| 5 | `*`, `/`, `%`, `**`, `*%`, `*\|`, `\|\|` | 左 |
| 6 | `+`, `-`, `++`, `+%`, `-%`, `+\|`, `-\|` | 左 |
| 7 | `<<`, `>>`, `<<\|` | 左 |
| 8 | `&`, `^`, `\|`, `orelse`, `catch` | 左 |
| 9 | `==`, `!=`, `<`, `>`, `<=`, `>=` | 无 |
| 10 | `and` | 左 |
| 11 | `or` | 左 |
| 12 | `=`, `*=`, `*%=`, `*\|=`, `/=`, `%=`, `+=`, `+%=`, `+\|=`, `-=`, `-%=`, `-\|=`, `<<=`, `<<\|=`, `>>=`, `&=`, `^=`, `\|=` | 右 |

```zig
const std = @import("std");

2 + 3 * 4            // 14
1 << 2 + 3           // 32：+ 高于 <<
(1 | 2) == 2         // false：== 低于 |
true and false       // false：Zig 用 and / or，不是 && / ||
const maybe: ?u32 = null;
maybe orelse 0       // 0：orelse 与 & ^ | 同级，高于比较
var x: i32 = 1;
x += 2               // 赋值右结合
```

Zig 把"位运算与空值/错误兜底"放在同一级是它的特色：`&`, `^`, `|`, `orelse`, `catch` 共享一行，且整体高于 `==`、`<` 这些比较，所以 `value orelse 0 == 1` 会先做兜底再比较，想比较"兜底后的值是否等于 1"必须写 `(value orelse 0) == 1`。`?x` 是可选类型前缀，`x.?` 是解包（第 1 级后缀），`a!b` 是错误联合类型语法而不是普通中缀运算符，这三者写法相近、含义完全不同，读代码时要分清。`+%`, `-|`, `*%`, `<<|` 这类带 `%` 或 `|` 的运算符是回绕与饱和版本，它们与被检查版本同级、只是溢出行为不同，这不是优先级问题而是安全模式问题。求值顺序方面，语言参考只给出优先级与结合性，没有承诺实参与操作数的求值次序，因此 `f(g(), h())` 这种写法不要假设 `g()` 先执行，需要确定次序就引入中间变量。

📘 [Zig 语言参考 · 运算符优先级](https://ziglang.org/documentation/master/#Precedence)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 5.5 手册的 Precedence 一节给出 12 行优先级，从低到高是 `or`、`and`、比较、`|`、`~`、`&`、移位、`..`、`+ -`、`* / // %`、一元运算符、`^`；`..` 与 `^` 右结合，其余二元运算符左结合。`and`/`or` 短路并返回操作数，只有 `false` 与 `nil` 为假，所以 `nil or "default"` 得到字符串。手册对求值顺序很克制：只规定"所有实参在调用前求值完"，没有规定实参之间的先后。

| 优先级（低→高） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | `or` | 左 |
| 2 | `and` | 左 |
| 3 | `<`, `>`, `<=`, `>=`, `~=`, `==` | 左 |
| 4 | `\|` | 左 |
| 5 | `~` | 左 |
| 6 | `&` | 左 |
| 7 | `<<`, `>>` | 左 |
| 8 | `..` | 右 |
| 9 | `+`, `-` | 左 |
| 10 | `*`, `/`, `//`, `%` | 左 |
| 11 | 一元 `not`, `#`, `-`, `~` | 无 |
| 12 | `^` | 右 |

```lua
print(2 + 3 * 4)          -- 14
print(2 ^ 3 ^ 2)          -- 512.0：^ 右结合
print(-2 ^ 2)             -- -4.0：^ 高于一元负号
print(1 << 2 + 3)         -- 32：+ 高于 <<
print("a" .. 1 + 1)       -- a2：+ 高于 ..
print(1 < 2 and "yes")    -- yes：and 返回操作数
print(nil or "default")   -- default
print(10 or error("never"))  -- 10：or 短路，不触发错误
```

手册给出的短路例子很有教学价值：`10 or error()` 得到 10，`false and error()` 得到 false，`nil and 10` 得到 nil，`10 and 20` 得到 20——`and`/`or` 返回的是操作数本身而不是布尔值，这也是 Lua 里写默认值的惯用法。`^` 是唯一比一元运算符还紧的运算符，所以 `-2 ^ 2` 是 `-(2 ^ 2)`，而 `2 ^ -2` 合法；`..` 右结合，`"a" .. "b" .. "c"` 读作 `"a" .. ("b" .. "c")`，在拼接大量字符串时这会影响临时对象的产生次序。比较运算符在 Lua 里不能链写：`1 < 2 < 3` 会先算 `1 < 2` 得到 `true`，再拿 `true` 和 `3` 比较并抛错。求值顺序方面，手册只说"所有实参表达式在调用前被求值"以及"表构造器里赋值的顺序是未定义的"，所以 `f(i, i = i + 1)` 这类写法不要依赖任何次序。

📘 [Lua 5.5 参考手册 · 优先级](https://www.lua.org/manual/5.5/manual.html#3.4.8)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的运行时运算符与 JavaScript 完全一致，因此优先级表就是 MDN 的 18 级（18 级 grouping 到 1 级逗号）；TypeScript 只在类型层面追加 `as`、`satisfies`、非空断言 `!` 与类型注解，这些在编译成 JavaScript 后被完全擦除。`**` 右结合、赋值与三元右结合、`?.` 与 `??` 短路，而 `??` 不能与 `||`/`&&` 不加括号直接混写，那是语法错误而不是优先级问题。这套机制里"编译期存在、运行时消失"的部分与"运行时真正短路"的部分必须分清。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 18 | grouping：`(x)` | 无 |
| 17 | access and call：`x.y`, `x?.y`, `x[y]`, `new x(y)`, `x(y)`, `import(x)` | 左 |
| 16 | `new x`（无参列表） | 无 |
| 15 | postfix：`x++`, `x--` | 无 |
| 14 | prefix：`++x`, `--x`, `!x`, `~x`, `+x`, `-x`, `typeof x`, `void x`, `delete x`, `await x` | 无 |
| 13 | `x ** y` | 右 |
| 12 | `*`, `/`, `%` | 左 |
| 11 | `+`, `-` | 左 |
| 10 | `<<`, `>>`, `>>>` | 左 |
| 9 | `<`, `<=`, `>`, `>=`, `in`, `instanceof` | 左 |
| 8 | `==`, `!=`, `===`, `!==` | 左 |
| 7 | `&` | 左 |
| 6 | `^` | 左 |
| 5 | `\|` | 左 |
| 4 | `&&` | 左 |
| 3 | `\|\|`, `??` | 左 |
| 2 | 赋值 `=` 与全部复合赋值、`?:`、`=>`、`yield`、`yield*`、`...x` | 右 |
| 1 | `,` | 左 |

```typescript
const side = (tag: string, v: boolean): boolean => { console.log('eval', tag); return v; };
console.log(2 + 3 * 4);              // 14
console.log(2 ** 3 ** 2);            // 512：** 右结合
console.log(1 << 2 + 3);             // 32：+ 高于 <<
console.log(side('a', false) && side('b', true));  // 只打印 eval a，结果 false
const n: number | null = null;
console.log(n ?? 0);                 // 0
console.log((null ?? 'a') || 'b');   // a：?? 与 || 混用必须加括号
// console.log(null ?? 'a' || 'b');  // 🛑 SyntaxError
const x = '1' as unknown as number;  // as 只骗编译器，运行时不转换
```

运行时的每一条行为都与 JavaScript 相同（本机 Node 24.20.0 实测；文档口径按 Node 26）：`??` 只把 `null` 与 `undefined` 视为缺失，`||` 会把 `0`、`''`、`NaN` 也算作假，所以"给可能为 0 的配置项兜底"要用 `??` 而不是 `||`。`??` 与 `||`/`&&` 的混用限制是语法层面的：`null ?? 'a' || 'b'` 会抛 `SyntaxError: Unexpected token '||'`，必须写成 `(null ?? 'a') || 'b'`。`?.` 会短路整条链，`a?.b?.c` 中任何一环为 `null`/`undefined` 就整体得到 `undefined`。TypeScript 独有的 `as`、`satisfies`、`!` 全是编译期语法：`as` 不做任何转换也不产生代码，`!` 只是让类型检查器闭嘴，运行时该崩还是会崩，因此它们既不参与运行时的优先级计算，也不能当作类型转换使用（真要转换请用 `Number()`/`String()`）。

📘 [MDN · 运算符优先级](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_precedence)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的优先级表在 MDN 上按 18 个编号层级给出（18 级 grouping 到 1 级逗号），`**` 是唯一右结合的算术运算符，赋值与三元 `?:` 右结合。MDN 特别强调一条容易被忽视的结论：优先级与结合性只决定"分组"，操作数始终从左到右求值。`&&`、`||`、`??` 都短路，其中 `??` 只把 `null` 与 `undefined` 当作缺失，而且不能与 `||`/`&&` 不加括号混用，这是语法错误。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 18 | grouping：`(x)` | 无 |
| 17 | access and call：`x.y`, `x?.y`, `x[y]`, `new x(y)`, `x(y)`, `import(x)` | 左 |
| 16 | `new x`（无参列表） | 无 |
| 15 | postfix：`x++`, `x--` | 无 |
| 14 | prefix：`++x`, `--x`, `!x`, `~x`, `+x`, `-x`, `typeof x`, `void x`, `delete x`, `await x` | 无 |
| 13 | `x ** y` | 右 |
| 12 | `*`, `/`, `%` | 左 |
| 11 | `+`, `-` | 左 |
| 10 | `<<`, `>>`, `>>>` | 左 |
| 9 | `<`, `<=`, `>`, `>=`, `in`, `instanceof` | 左 |
| 8 | `==`, `!=`, `===`, `!==` | 左 |
| 7 | `&` | 左 |
| 6 | `^` | 左 |
| 5 | `\|` | 左 |
| 4 | `&&` | 左 |
| 3 | `\|\|`, `??` | 左 |
| 2 | 赋值 `=` 与全部复合赋值、`?:`、`=>`、`yield`, `yield*`, `...x` | 右 |
| 1 | `,` | 左 |

```javascript
const side = (tag, v) => { console.log('eval', tag); return v; };
const arg = (tag, v) => { console.log('arg', tag); return v; };
const f = (a, b, c) => a + b + c;

console.log(2 + 3 * 4);          // 14
console.log(2 ** 3 ** 2);        // 512：** 右结合
console.log(1 << 2 + 3);         // 32：+ 高于 <<
console.log(null ?? 'default');  // default
console.log(0 ?? 'x');           // 0：?? 只认 null/undefined
console.log(null || 'y');        // y：|| 把 0 与 "" 也当假
console.log(side('a', false) && side('b', true));  // eval a -> false
console.log(f(arg('1', 1), arg('2', 2), arg('3', 3)));  // arg 1/2/3 -> 6
// console.log(null ?? 'a' || 'b');  // 🛑 SyntaxError: Unexpected token '||'
```

MDN 的原文把两件事分得很清："运算符优先级与结合性只影响运算符的分组，不影响操作数的求值顺序；操作数永远从左到右求值"，所以 `4 ** 3 ** 2` 因为 `**` 右结合而是 `4 ** (3 ** 2)`，但 `echo('left', 4) * echo('right', 5)` 仍然先打印 left。`??` 与 `||` 的选择是实践中最常见的分岔：`||` 把 `false`、`0`、`''`、`NaN` 都当作假，`??` 只认 `null` 与 `undefined`，默认值语义要按需求挑；两者混写会直接抛 `SyntaxError`，必须用括号显式表明意图（`(a ?? b) || c` 或 `a ?? (b || c)`）。`?.` 会短路右侧整条链，`a?.b.c` 中 `a` 为 `null` 时 `c` 根本不会被访问。逗号运算符只在极少数压缩写法里出现，`x = (a, b)` 取最后一个值，可读性差，现代代码里通常直接拆成两条语句。

📘 [MDN · 运算符优先级与结合性](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_precedence)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的优先级表在 php.net 的 Operator Precedence 页，官方表共 30 行（含 `clone`、`new`、`yield`、`print`、`include`、`fn`、`throw` 等表内列出的语法条目）；`**` 右结合、`??` 右结合，三元 `? :` 自 PHP 8.0 起改为非结合，`.` 自 PHP 8.0 起低于 `+` 与 `-`。同一页还明确写了一句话：优先级只决定分组，PHP 一般不规定表达式的求值顺序。

| 优先级（高→低） | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | `clone`, `new` | 无 |
| 2 | `**` | 右 |
| 3 | `+`, `-`, `++`, `--`, `~`, `(int)`, `(float)`, `(string)`, `(array)`, `(object)`, `(bool)`, `@` | 无 |
| 4 | `instanceof` | 左 |
| 5 | `!` | 无 |
| 6 | `*`, `/`, `%` | 左 |
| 7 | `+`, `-` | 左 |
| 8 | `<<`, `>>` | 左 |
| 9 | `.` | 左 |
| 10 | `\|>` | 左 |
| 11 | `<`, `<=`, `>`, `>=` | 非结合 |
| 12 | `==`, `!=`, `===`, `!==`, `<>`, `<=>` | 非结合 |
| 13 | `&` | 左 |
| 14 | `^` | 左 |
| 15 | `\|` | 左 |
| 16 | `&&` | 左 |
| 17 | `\|\|` | 左 |
| 18 | `??` | 右 |
| 19 | `? :` | 非结合 |
| 20 | `=`, `+=`, `-=`, `*=`, `**=`, `/=`, `.=`, `%=`, `&=`, `\|=`, `^=`, `<<=`, `>>=`, `??=` | 右 |
| 21 | `yield from` | 无 |
| 22 | `=>` | 无 |
| 23 | `yield` | 无 |
| 24 | `print` | 无 |
| 25 | `and` | 左 |
| 26 | `xor` | 左 |
| 27 | `or` | 左 |
| 28 | `include`, `include_once`, `require`, `require_once` | 无 |
| 29 | `fn (...) =>` | 无 |
| 30 | `throw` | 无 |

```php
2 + 3 * 4;             // 14
2 ** 3 ** 2;           // 512：** 右结合
1 << 2 + 3;            // 32：+ 高于 <<
(1 & 2) == 2;          // false：== 高于 &
$flags = 1;
($flags & 4) == 1;     // false：漏掉括号会先算 4 == 1
$a = true and false;   // $a 得到 true：= 高于 and
$b = true && false;    // $b 得到 false：&& 高于 =
0 ?? 'x';              // 0：?? 只认 null
```

手册自己承认 PHP 不规定求值顺序，并给了两个著名例子：`echo $a + $a++;` 可能打印 2 也可能打印 3，`$array[$i] = $i++;` 可能写入下标 1 也可能写入下标 2——这类代码不要写。`and`/`or`/`xor` 排在赋值之下，所以 `$a = true and false` 得到 `true`（读作 `($a = true) and false`），而 `$b = true && false` 得到 `false`；`$ok = foo() or die('failed')` 这种惯用法正是靠这个优先级成立的。位运算与比较的组合是 PHP 里最容易出 bug 的地方：`==` 高于 `&`，因此 `$flags & MASK == 1` 实际是 `$flags & (MASK == 1)`，必须写 `($flags & MASK) == 1`。`.` 与 `+` 的优先级在 PHP 8.0 发生过变化（现在 `.` 更低），这也解释了为什么手册单独用两个例子演示 `"x minus one equals " . $x-1` 会先算 `-`；跨版本代码里把拼接与算术混写时务必加括号。`??` 的优先级低于 `.` 与 `||`，与它们混写同样需要括号。

📘 [PHP 手册 · 运算符优先级](https://www.php.net/manual/en/language.operators.precedence.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的优先级表在官方文档 doc/syntax/precedence.rdoc，从高到低共 21 行；`**` 右结合，`=` 及其复合形式右结合，`and`/`or`/`not` 排在赋值之下，比 `&&`/`||`/`!` 低得多。`&&` 与 `||` 短路，`and`/`or` 也短路但优先级完全不同，这是 Ruby 最著名的陷阱。它是动态类型语言，优先级在解析期固定，求值顺序在 doc/syntax/methods.rdoc 里明确写了"实参值总是从左到右求值"。

| 优先级（高→低） | 运算符 / 语法 | 结合性 |
| --- | --- | --- |
| 1 | `!`, `~`, 一元 `+` | 右 |
| 2 | `**` | 右 |
| 3 | 一元 `-` | 右 |
| 4 | `*`, `/`, `%` | 左 |
| 5 | `+`, `-` | 左 |
| 6 | `<<`, `>>` | 左 |
| 7 | `&` | 左 |
| 8 | `\|`, `^` | 左 |
| 9 | `>`, `>=`, `<`, `<=` | 左 |
| 10 | `<=>`, `==`, `===`, `!=`, `=~`, `!~` | 左 |
| 11 | `&&` | 左 |
| 12 | `\|\|` | 左 |
| 13 | `..`, `...` | 无 |
| 14 | `? :` | 右 |
| 15 | modifier-rescue（`expr rescue expr`） | 右 |
| 16 | `=`, `+=`, `-=`, `*=`, `/=`, `%=` 等赋值 | 右 |
| 17 | `defined?` | 无 |
| 18 | `not` | 右 |
| 19 | `or`, `and` | 左 |
| 20 | modifier-if, modifier-unless, modifier-while, modifier-until | 无 |
| 21 | `{ }` 块（`do`/`end` 形式更低） | 无 |

```ruby
2 + 3 * 4          # 14
2 ** 3 ** 2        # 512：** 右结合
-2 ** 2            # -4：** 高于一元负号
1 << 2 + 3         # 32：+ 高于 <<
true || false && false   # true：&& 高于 ||
x = false or true  # x 是 false：= 高于 or
y = (false or true) # y 是 true
a = true and false  # a 是 true
```

`-2 ** 2` 得到 -4 的原因正是表里 `**` 在第 2 行、一元 `-` 在第 3 行：幂先算，再取负。赋值与 `and`/`or` 的次序是 Ruby 代码风格的根源：`x = false or true` 先做赋值再做 `or`，所以 `x` 是 `false`；而 `x = (false or true)` 才是 `true`；`a = true and false` 里 `a` 得到 `true`。`and`/`or` 的低优先级是有意设计给流程控制用的，例如 `render or raise` 这类风格，而做布尔运算与返回布尔值时应当用 `&&`/`||`。`not` 也在赋值之下，所以 `x = not true` 是语法错误，必须写 `x = !true`。短路行为方面三者一致：`a && b`、`a and b`、`a || b`、`a or b` 都在结果已定时跳过右边。方法调用与块也有讲究：`foo bar { }` 里的块绑定到 `bar`，而 `foo bar do end` 里的块绑定到 `foo`，这就是表里"`{ }` 块高于 `do`/`end` 形式"的直接后果，写多行块时用 `do`/`end` 形式能避免这类歧义。

📘 [Ruby · 优先级](https://docs.ruby-lang.org/en/master/syntax/precedence_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}
