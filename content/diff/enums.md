+++
title = "枚举"
date = 2026-09-19T12:00:00+08:00
weight = 12
type = "docs"
description = "18 种语言的枚举对照：定义与底层表示、取值转换与遍历、带数据的枚举与模式匹配"
isCJKLanguage = true
draft = false
+++

# 枚举：18 种语言对照

枚举在多数人印象里就是「给整数起名字」，可一旦跨语言看，它其实分裂成三种完全不同的东西：C/C++/Go/Java 路线把它当成**整数的别名或整数的包装**，Rust/Swift/Kotlin/Zig 路线把它当成**只能取有限几个构造子的类型**（Rust 的 `enum` 是代数数据类型，Zig 的 `enum` 可以带 payload），Lua/JavaScript/R/Ruby 路线则干脆**没有枚举**，用 table、`Object.freeze`、`factor`、`Symbol` 这些更基础的东西凑出等价效果。前一种路线的枚举值是数字，可以隐式转成整数、可以拿到不存在的值；后一种路线的枚举值只能来自声明过的构造子，编译器能替你检查穷尽性。本页按三个主题层层推进：**定义与底层表示**先确认每种语言的枚举到底是什么、占几个字节、序列化成什么；**取值、转换与遍历**看序号与底层值怎么互换、遍历顺序可不可靠、未知值怎么处理；**带数据的枚举与模式匹配**看哪些语言真的能做和类型（sum type），穷尽性检查是编译期保证还是运行时兜底。每一节都是一套 18 语言标签页，顺序固定，没有该机制的语言会明确写出「没有」并给出常规替代做法。

## 枚举

**一页速览**

| 语言 | 有没有 / 关键字写法 | 一句话说明 / 关键差异 | 关键陷阱 |
| --- | --- | --- | --- |
| Rust | 有，`enum`，是代数数据类型 | `#[repr(u8)]` 才能拿到稳定的判别值 | 默认布局不保证判别值，`as` 只对无字段枚举合法 |
| Swift | 有，`enum`，可带 raw value 或关联值 | raw value 与关联值互斥，`indirect` 支持递归 | `init?(rawValue:)` 给 Optional，未知值不崩溃 |
| Go | 没有，`type X int` + `iota` 常量 | 纯编译期常量，可被任意整数赋值替代 | `String()` 越界会 panic，零值常是合法枚举值 |
| Python | 有，`enum.Enum`/`IntEnum`/`StrEnum`/`Flag`/`IntFlag` | 成员是单例对象，`auto()` 自动配值 | `Enum` 不等价于其值，`IntEnum` 才等于 `int` |
| Kotlin | 有，`enum class`；和类型用 `sealed class`/`sealed interface` | `enum class` 可以有构造器、方法与接口 | `values()` 每次返回新数组，1.9 前 `entries` 不可用 |
| Java | 有，`enum` 就是 `final class` | 可以有字段、方法、构造器、实现接口 | `ordinal()` 不可持久化，重排常量会破坏旧数据 |
| C++ | 有，`enum` 与 `enum class` | `enum class` 强作用域、不隐式转 int，可指定底层类型 | `enum class` 默认没有位运算，要自己重载 |
| C | 有，`enum`；C23 起可指定底层类型 | 枚举常量就是 `int` 常量 | 底层类型由实现选择，越界值合法 |
| Julia | 有，`@enum Name::T v1 v2` | 基于 `Base.Enum` 的原始值类型 | `Int(x)` 给原始值而非序号，要用 `instances` 定位 |
| C# | 有，`enum`，可带底层类型与 `[Flags]` | 具名常量集，惯例把零值留给"无" | `Enum.Parse` 接受任意整数甚至不存在的名字 |
| Dart | 有，`enum`（2.17 起支持 enhanced enum） | 枚举可实现接口、带字段和方法 | `.index` 会随声明顺序变化，不要持久化 |
| R | 没有，用 `factor` 与常量 | `factor` 带 level 集合，天然支持序数 | level 默认按字典序排序，不是出现顺序 |
| Zig | 有，`enum` 与 `union(enum)` 标记联合 | 枚举可指定整数 tag，可声明非穷尽 `_` | 非穷尽枚举转整数再转回来要做范围检查 |
| Lua | 没有，用 table 常量 | `local C = { RED = 1 }` 加反查表 | 表默认可写，需要 `__newindex` 或只读约定 |
| TypeScript | 有，`enum`/`const enum`；也可用字面量联合类型 | 数值枚举自动双向映射，字符串枚举不反向 | Node 26 剥类型模式下 `enum` 直接报错 |
| JavaScript | 没有，用 `Object.freeze` 对象或 `Symbol` | 冻结是浅冻结，值仍是普通字符串/数字 | 没有类型约束，写错常量名要等运行时才发现 |
| PHP | 有，8.1 起纯枚举与 backed enum | 枚举可以有方法、常量、实现接口 | 枚举不能有属性，backed enum 只能是 `int`/`string` |
| Ruby | 没有，用 `Symbol`、常量与 `Data` | `Symbol` 内部化且不可变，天然适合做标签 | `case/in` 没有穷尽性检查，漏分支抛 `NoMatchingPatternError` |

### 定义与底层表示

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `enum` 不是「整数的别名」，而是一个真正的**代数数据类型（algebraic data type）**：每个变体（variant）可以不带数据、带匿名字段、带具名字段，甚至递归包含自身。它是值类型、编译期确定大小的静态类型，默认没有稳定的整数判别值——想要判别值必须显式写 `#[repr(u8)]` 之类的表示属性。

```rust
enum Color { Red, Green, Blue }              // 纯标签枚举
#[repr(u8)]                                   // 指定判别值底层类型
enum Code { Ok = 1, Fail = 2 }                // 判别值只有加了 repr 才保证
#[derive(Debug)]
enum Shape {                                  // 变体可以带数据
    Circle(f64),                              // 元组式字段
    Rect { w: f64, h: f64 },                  // 具名式字段
}
fn main() {
    println!("{}", std::mem::size_of::<Color>());        // 1（只有 3 个变体）
    println!("{}", std::mem::size_of::<Code>());          // 1（#[repr(u8)]）
    println!("{}", std::mem::size_of::<Option<Code>>());  // 1（niche 优化，实现细节）
    println!("{}", std::mem::size_of::<Shape>());         // 24（tag + 最大变体载荷 + 对齐）
    println!("{}", Code::Ok as u8);                        // 1
}
```

没有 `#[repr]` 时，判别值的次序「通常」跟声明顺序一致，但这是实现细节而不是语言保证，跨 `rustc` 版本或跨 crate 边界序列化后可能变形；只有 `#[repr(u8)]`、`#[repr(i32)]`、`#[repr(C)]` 这类显式表示才把布局固定下来。`Color` 这种无字段枚举占 1 字节是因为变体数少于 256，编译器会挑最小的判别类型；`Option<Code>` 也是 1 字节，因为 `#[repr(u8)]` 枚举有空闲判别值可以直接表示 `None`（这是 rustc 的 niche 优化，属实现细节而非语言保证）。⚠️ 另一个常见误解是 `as u8` 万能：只有当枚举所有变体都不带字段时 `Code::Ok as u8` 才合法，带字段的变体必须先 `match` 再取值。序列化方面，`serde` 默认把无字段变体写成名字符串 `"Ok"`，把带字段变体写成 `{"Rect":{"w":3.0,"h":4.0}}`，要写成整数得用 `#[serde(into = "u8")]` 之类的转换；`#[repr(u8)]` 本身不会改变 `serde` 的行为。

📘 [Rust Reference · Enumerations](https://doc.rust-lang.org/reference/items/enumerations.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `enum` 是值类型（`struct` 级别语义，赋值即拷贝）、编译期完整的静态类型，但它的两套机制必须二选一：要么给每个 case 配一个 **raw value**（`Int`、`String`、`Character`、浮点都行），要么让 case 带**关联值（associated value）**，不能同时用。这是 Swift 与 Rust 最根本的差别——Rust 的变体字段与判别值可以共存，Swift 不行。

```swift
enum Direction: Int, CaseIterable {          // raw value 型：底层是 Int
    case north = 1, south, east, west        // 之后的 case 自动递增
}
enum Suit: String { case hearts = "H", spades = "S" }   // raw value 也可以是 String
enum Barcode {                                // 关联值型：没有 rawValue
    case upc(Int, Int, Int, Int)
    case qrCode(String)
}
enum Tree {                                   // 递归枚举必须加 indirect
    indirect case node(Tree, Int, Tree)
    case leaf(Int)
}
print(Direction.north.rawValue)               // 1
print(Suit.hearts.rawValue)                   // H
print(MemoryLayout<Direction>.size)           // 1
print(MemoryLayout<Barcode>.size)             // 33（1 字节 tag + 32 字节最大载荷）
print(Direction.allCases.count)               // 4（CaseIterable 合成 allCases）
```

`rawValue` 型的底层表示由编译器按"能装下所有 raw value 的最小整数类型"选择，`Int` 声明的枚举通常占 1 字节（除非取值超过 255）；`rawValue` 的赋值必须互不重复，编译器会报错。关联值型的枚举在内存里是「标签 + 最大载荷的联合体」，`MemoryLayout` 会给对齐后的尺寸。`indirect` 会把该 case 的载荷装箱（heap 分配），这是解决递归枚举无法定大小的标准手段。序列化上，raw value 型可以直接 `rawValue` 写进 JSON，`Codable` 合成时也按 raw value 或 case 名编码；关联值型要自己实现 `Codable`，否则合成出来的形状不是你能控制的。⚠️ 常见陷阱：`enum` 与 `Int` 之间没有隐式转换，`let x: Int = Direction.north` 是编译错误。

📘 [The Swift Programming Language · Enumerations](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/enumerations/)

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有枚举类型**。语言规范里根本没有 `enum` 这个关键字或构造，社区的标准做法是「自定义整数类型 + `const` 块 + `iota`」：类型给出了名字与可读性，`iota` 给出从 0 递增的常量，但三样东西都不会阻止你把任意整数塞进去。

```go
package main

import "fmt"

type Weekday int                       // 自定义类型：枚举的"类型"部分

const (
	Sunday Weekday = iota              // 0
	Monday                             // 1（iota 自动递增）
	Tuesday                            // 2
	_                                  // 3 跳过保留值
	Thursday                           // 4
)

func (d Weekday) String() string {     // 常见配套：String() 实现 fmt.Stringer
	names := [...]string{"Sunday", "Monday", "Tuesday", "unknown", "Thursday"}
	if int(d) < 0 || int(d) >= len(names) {
		return fmt.Sprintf("Weekday(%d)", int(d))   // 越界时自保
	}
	return names[d]
}

func main() {
	fmt.Println(Sunday, Monday, int(Tuesday))       // Sunday Monday 2
	var d Weekday = 99                              // ⚠️ 合法：没有编译期约束
	fmt.Println(d)                                  // Weekday(99)
	var zero Weekday                                // 0 == Sunday，零值有含义
	fmt.Println(zero == Sunday)                     // true
}
```

`iota` 只在 `const` 块里有效，从 0 开始、每行递增 1；`_` 跳过某个值或让位给保留数字。类型与常量是分开的：`Weekday` 是 `int` 的具名类型，`Sunday` 是它的常量，但 `var d Weekday = 99` 完全合法，编译器不检查取值范围。这正是 Go 枚举方案的软肋——它给你名字，不给你封闭性。另一个软肋是零值：`var zero Weekday` 是 `0` 即 `Sunday`，如果 0 代表"未设置"，就必须把 0 留给一个显式的 `Unknown` 常量。序列化上 `encoding/json` 会把 `Weekday` 写成数字（因为它底层是 `int`），要写字符串得自己实现 `MarshalJSON`，或者用 `stringer` 工具生成的 `String()` 配合 `-tags` 类方案。⚠️ 注意 `String()` 方法里如果用固定数组下标而不做边界检查，越界调用会直接 panic（`%!v(PANIC=String method: runtime error: index out of range [99] with length 3)`），所以自产的 `String()` 一定要带兜底分支。

📘 [Go Spec · Constant declarations](https://go.dev/ref/spec#Constant_declarations)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的枚举来自标准库 `enum` 模块（不是语言关键字）：`Enum` 的每个成员都是一个**单例对象**，属于引用类型、运行时构造、动态语言里少见的强约束机制。3.11 起还有一个专门的 `StrEnum`，让成员既是枚举成员又能当字符串用。

```python
from enum import Enum, IntEnum, StrEnum, Flag, IntFlag, auto

class Color(Enum):          # 普通枚举：成员与值不等价
    RED = auto()            # auto() 自动编号 1、2、3
    GREEN = auto()
    BLUE = auto()

class Level(IntEnum):       # IntEnum：成员也是 int
    LOW = 1
    HIGH = 2

class Kind(StrEnum):        # StrEnum：3.11 起，成员也是 str
    A = "a"
    B = "b"

class Perm(Flag):           # Flag：可组合的位标志
    R = auto()              # 1
    W = auto()              # 2
    X = auto()              # 4

print(Color.RED, Color.RED.name, Color.RED.value)   # Color.RED RED 1
print(Color.RED == 1)                                # False（Enum 不等价于值）
print(Level.HIGH == 2, isinstance(Level.HIGH, int))  # True True
print(f"{Kind.A}", Kind.A == "a")                    # a True
print(Perm.R | Perm.W, (Perm.R | Perm.W).value)      # Perm.R|W 3
print(len(list(Color)))                              # 3
```

`Enum` 与 `IntEnum`/`StrEnum` 的区别是刻意设计的：`Enum` 成员故意不与底层值相等，逼你显式写 `Color.RED.value`，这样 `Color.RED == 1` 这种跨语言常见的 bug 在 Python 里直接是 `False`；要跟整数/字符串互操作才降级用 `IntEnum`/`StrEnum`（3.11 引入，替代 3.10 及以前的 `str, Enum` 多继承写法）。`Flag`/`IntFlag` 支持 `|`、`&`、`~` 做位组合，`IntFlag` 还额外允许与 `int` 混算。枚举成员默认不可变、`.value`/`.name` 只读，`Enum` 不允许重复值（重复值默认被当成别名 alias，`for x in Color` 不会遍历别名，要用 `Color.__members__` 才看得到）。⚠️ 常见陷阱是 `auto()` 的编号会随插入顺序变化，所以`Color.RED.value` 不该写进数据库或协议；要持久化就用显式字符串值或 `StrEnum`。

📘 [Python · enum — Support for enumerations](https://docs.python.org/3/library/enum.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `enum class` 是真正的类：可以有构造器参数、属性、方法、`companion object`、实现接口，但实例集合在编译期封闭。它是引用类型（JVM 上是 `java.lang.Enum` 的子类）、静态类型；而需要「每个分支带不同数据」时用的是另一个机制——`sealed class`/`sealed interface`，两者合起来才等价于 Rust 的 `enum`。

```kotlin
enum class Planet(val mass: Double, val radius: Double) {   // 带属性的枚举
    MERCURY(3.30e23, 2.44e6),                                // 每个成员调用构造器
    VENUS(4.87e24, 6.05e6),
    EARTH(5.97e24, 6.37e6);

    val surfaceGravity get() = 6.674e-11 * mass / (radius * radius)   // 方法/属性
    fun isHabitable() = this == EARTH                                  // 方法
}

interface Describable { fun describe(): String }
enum class Suit : Describable {                             // 枚举可以实现接口
    HEARTS { override fun describe() = "红桃" },             // 每个成员可覆写
    SPADES { override fun describe() = "黑桃" };
}

sealed interface Shape {                                     // 和类型：分支带数据
    data class Circle(val r: Double) : Shape
    data class Rect(val w: Double, val h: Double) : Shape
    data object Point : Shape                                // 无数据的单例分支
}

fun main() {
    println(Planet.EARTH.surfaceGravity)                     // 9.819325774024136
    println(Planet.EARTH.ordinal)                            // 2（从 0 起）
    println(Planet.EARTH.name)                               // EARTH
    println(Suit.HEARTS.describe())                          // 红桃
    println(Planet.entries.size)                             // 3
}
```

`enum class` 的每个成员都是单例，`Planet.EARTH` 就是唯一实例，所以可以用 `==` 比较（引用相等）；枚举成员可以匿名子类化并覆写方法，`Suit.HEARTS` 与 `Suit.SPADES` 其实类型不同。`sealed class`/`sealed interface` 的子类必须与密封类在同一个包、同一个模块（Kotlin 1.5 起放宽为同一模块 + 同一包），编译器因此知道全部子类，对 `when` 做**穷尽性检查**：漏分支是编译错误而不是警告。⚠️ `values()` 每次调用都新建一个数组，`Planet.entries`（Kotlin 1.9 起）返回缓存的 `EnumEntries`，新代码应该用 `entries`。序列化上，Kotlin 没有内建枚举序列化约定，`kotlinx.serialization` 默认按 `name` 写字符串，改名会破坏兼容；持久化时最好显式给 `@SerialName`。

📘 [Kotlin · Enum classes](https://kotlinlang.org/docs/enum-classes.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 `enum` 是 `java.lang.Enum` 的**最终子类**：它真的是类，可以声明字段、构造器（隐式 `private`）、方法、静态成员并实现接口，实例集合在类初始化时一次性建好。它是引用类型、运行时有对象身份，静态类型系统保证你只能拿到声明过的常量。

```java
enum Planet {                                       // 最简形式：0 起自动编号
    MERCURY, VENUS, EARTH
}

enum Suit implements Comparable<Suit> {             // 可以有字段/方法/构造器
    HEARTS("H", 1), SPADES("S", 4);                 // 成员列表，调用私有构造器
    private final String symbol;                     // 枚举字段惯例是 final
    private final int rank;
    Suit(String symbol, int rank) {                 // 构造器隐式 private
        this.symbol = symbol;
        this.rank = rank;
    }
    public String symbol() { return symbol; }        // 方法
    public boolean isRed() { return this == HEARTS; }
}

enum Flags {                                        // 位标志靠手动移位
    READ(1), WRITE(2), EXEC(4);
    private final int bit;
    Flags(int bit) { this.bit = bit; }
    public int bit() { return bit; }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(Planet.EARTH.ordinal());  // 2
        System.out.println(Suit.HEARTS.symbol());    // H
        System.out.println(Flags.READ.bit() | Flags.WRITE.bit());  // 3
        System.out.println(Suit.valueOf("SPADES")); // SPADES
    }
}
```

Java 没有 `[Flags]` 那种语言级位标志支持，惯例是用枚举 + 手写 `bit()` 或者 `EnumSet`（专门的位集实现，内部就是 `long` 位图，比手动位运算安全）。枚举的 `ordinal()` 是声明顺序，`name()` 是标识符原文，两个都由编译器固定，但只有 `name()` 适合持久化：`ordinal()` 一旦有人往中间插常量就会整体错位。⚠️ `values()` 每次调用都克隆一个新数组（这一点跟 Kotlin 的 `values()` 相同），在热路径里要缓存；此外枚举的 `equals` 就是引用相等，`==` 足够，别用 `equals` 之外的比较方式。序列化上，Java 原生序列化用 `name()` 而不是 `ordinal()`，所以给旧枚举改名会让反序列化失败；JSON 库（如 Jackson）默认也写 `name()`。枚举本身是可以被 `switch` 的，编译器会生成跳转表。

📘 [Java Language Specification · Enum Types](https://docs.oracle.com/javase/specs/jls/se26/html/jls-8.html#jls-8.9)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有两套枚举：从 C 继承来的**无作用域枚举（unscoped enum）**和 C++11 引入的**强作用域枚举（`enum class`）**。前者只是给整数起名字、名字泄漏到外层作用域、可以隐式转成 `int`；后者是独立类型、必须写 `Fruit::Apple`、不会隐式转 `int`，但可以有显式底层类型。两者都是值类型，布局由底层类型决定。

```cpp
#include <cstdio>
#include <cstdint>
enum Color { RED, GREEN, BLUE };                       // 无作用域：名字泄漏
enum class Fruit : std::uint8_t { Apple = 1, Pear };   // 强作用域 + 底层类型
enum class Perm : unsigned { R = 1, W = 2, X = 4 };

constexpr Perm operator|(Perm a, Perm b) {             // enum class 需要手动重载位运算
    return static_cast<Perm>(static_cast<unsigned>(a) | static_cast<unsigned>(b));
}

int main() {
    int n = GREEN;                                     // ✅ 无作用域可隐式转 int
    printf("%zu %d\n", sizeof(Color), n);              // 4 1
    printf("%d %zu\n", static_cast<int>(Fruit::Pear),  // 2 1
           sizeof(Fruit));
    // int x = Fruit::Apple;                           // 🛑 强作用域不会隐式转 int
    printf("%u\n", static_cast<unsigned>(Perm::R | Perm::W));  // 3
    auto bad = static_cast<Fruit>(77);                 // ⚠️ 合法但值是未命名的
    printf("%d\n", static_cast<int>(bad));             // 77
}
```

`sizeof(Color)` 是 4 是因为无作用域枚举的底层类型默认按实现选择（对本例三个值来说通常是 `int`），而 `enum class Fruit : std::uint8_t` 明确压到 1 字节——底层类型可以选 `std::int8_t`、`std::uint8_t`、`std::int16_t`、`std::int32_t`、`std::uint32_t`、`std::int64_t`、`std::uint64_t`（以及对应的内建整型）。C++17 起（CWG 1766）放宽了到枚举类型的 `static_cast` 的合法范围：有固定底层类型时，底层类型能表示的任意值都合法；没有固定底层类型时，合法范围是能容纳全部枚举器的最小位域范围。落在范围之外的转换**仍然是未定义行为**，所以「越界但合法」只对范围内、未具名的值成立，这种值适合做协议解析，但 `switch` 时一定要写 `default`，因为编译器对枚举的穷尽性只给警告不给错误。`enum class` 不会自动获得 `|`/`&`，要么像上面那样重载，要么用 `std::to_underlying`（C++23）转换后再运算。序列化上没有任何内建约定，写二进制时 `std::to_underlying` 才是拿到底层值的规范写法。

📘 [cppreference · Enumeration declaration](https://en.cppreference.com/w/cpp/language/enum)

{{% /tab %}}

{{% tab header="C" %}}

C 的 `enum` 是**纯整数常量集合**：C23 之前每个枚举器（enumerator）的类型是 `int`，C23 起则可能取 `int`、枚举类型本身或常量表达式的类型（有固定底层类型时就是枚举类型）；`enum` 类型本身与某个实现选择的整数类型兼容（称为兼容类型）。没有作用域、没有方法、没有封闭性，是彻头彻尾的编译期语法糖，值类型、无运行时表示。C23 补上了「显式指定底层类型」这个长期缺口。

```c
#include <stdio.h>
enum Color { RED, GREEN, BLUE };                  /* 枚举器是 int 常量 */
typedef enum { IDLE, RUN, DONE } State;            /* typedef enum 惯用法 */
enum Small : unsigned char { A = 1, B = 2 };      /* C23：固定底层类型 */
enum Flags { F_A = 1 << 0, F_B = 1 << 1, F_C = 1 << 2 };

int main(void) {
    printf("%zu %d %d\n", sizeof(enum Color), RED, BLUE);   /* 4 0 2 */
    printf("%zu\n", sizeof(enum Small));                     /* 1 */
    printf("%zu %s\n", sizeof(State), "run");                /* 4 run */
    enum Color c = (enum Color)99;                           /* ✅ 合法 */
    printf("%d\n", c);                                        /* 99 */
    int f = F_A | F_B;                                        /* 位标志靠整数运算 */
    printf("%d\n", f);                                        /* 3 */
    return 0;
}
```

`sizeof(enum Color)` 是实现定义的：标准只要求兼容类型能表示所有枚举器的值，所以三个值的枚举在主流编译器上就是 `int`（4 字节）；`enum Small : unsigned char` 是 C23 新增语法，把底层类型钉死成 1 字节——这在写二进制协议、寄存器映射、跨平台 ABI 时非常关键。⚠️ C 的枚举没有封闭性：`(enum Color)99` 合法，`switch` 里必须写 `default` 或者保证逻辑上不可能到达，否则漏掉的值会让函数走到末尾（`state_name` 里如果不写 `return`，非 `void` 函数会返回不确定值）。位标志惯例是把 `1 << n` 直接放进枚举器，但 `|` 的结果类型是 `int`，赋回枚举变量需要显式转换。C23 还允许在枚举器列表最后写逗号（C99 起就允许），`enum` 与 `int` 的隐式互转依旧双向放任。

📘 [cppreference · C enumeration declaration](https://en.cppreference.com/w/c/language/enum)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的枚举来自标准库 `@enum` 宏，生成的是一个 `<: Base.Enum` 的原始值类型（primitive type），成员是**编译期常量**、可以任意多分派。类型是值类型、静态，底层类型默认 `Int32`，可以在宏里指定。

```julia
using Printf

@enum Color::UInt8 RED GREEN BLUE          # 指定底层类型 UInt8
@enum Status begin                          # 块形式：可以写文档字符串
    OK = 0
    WARN = 10
    FAIL = 20
end

println(RED, " ", UInt8(RED))               # RED 0
println(Integer(BLUE), " ", BLUE)           # 2 BLUE
println(Status.WARN, " ", Int(Status.WARN)) # WARN 10
println(sizeof(Color))                      # 1（底层是 UInt8）
println(instances(Color))                   # (RED, GREEN, BLUE)
println(Symbol(RED))                        # :RED
println(RED isa Enum, RED isa Color)        # true true
println(Color(1))                           # GREEN（println 走 print，只给符号名）
println(repr(Color(1)))                     # GREEN（show 也只给符号名，REPL 才显示 GREEN::Color = 1）
for s in instances(Status)                  # 遍历：instances 返回元组
    @printf("%s=%d ", s, Integer(s))
end
println()
```

`@enum` 生成的类型有一个底层整型 `BaseType`（默认 `Int32`），文档明确说明成员值可以在枚举类型与该整数类型之间转换：`Integer(x)`/`Int(x)` 给原始值，`Color(1)` 按原始值反向构造，`instances(T)` 列出全部成员，`Symbol(x)` 从成员拿符号名，`read`/`write` 会自动做这种转换。⚠️ 第一个坑是 `Int(RED)` 拿的是**原始值**而不是声明位置：`Status` 的成员跳号成 0、10、20，只有 `instances` 的元组下标才是 0、1、2，把两者混为一谈是 Julia 枚举最常见的错误。第二个坑是 `Color(1)` 只按原始值匹配，越界值**会抛** `ArgumentError: invalid value for Enum Color: 99`（`@enum` 生成的构造器里带 membership 检查），并不会静默构造出非法成员；只有用 `reinterpret`/`bitcast` 硬造出来的值才会走到 `_symbol` 的 `<invalid #99>` 兜底分支。第三个坑是成员比较走 `isless(basetype(x), basetype(y))`，所以顺序由原始值而不是声明顺序决定。序列化方面没有内建约定，`JSON3`/`JSON.jl` 会把枚举写成数字（因为是 primitive type），要写字符串需自己加方法；这一点和 Go 很像。

📘 [Julia · Base.Enums](https://docs.julialang.org/en/v1/base/base/#Base.Enums.@enum)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `enum` 是**具名整数常量集**：它是值类型（`System.Enum` 的子类，但作为值类型直接内联），底层类型默认 `int`，可以是 `byte`、`sbyte`、`short`、`ushort`、`int`、`uint`、`long`、`ulong`。跟 C 一样不封闭——`(Color)99` 合法；跟 Java 不同，它不能有字段、方法或构造器（要附加数据只能用扩展方法或 `[Description]` 之类的特性）。

```csharp
using System;

enum Color { Red, Green, Blue }                       // 默认 int，Red = 0
enum Small : byte { A = 1, B = 2 }                    // 指定底层类型
[Flags] enum Perm { None = 0, R = 1, W = 2, X = 4 }   // [Flags] 影响 ToString
enum HttpStatus { Ok = 200, NotFound = 404 }          // 显式值（协议号）

class Program {
    static void Main() {
        Console.WriteLine($"{(int)Color.Blue} {sizeof(Color)}");    // 2 4
        Console.WriteLine($"{(byte)Small.B} {sizeof(Small)}");      // 2 1
        Console.WriteLine(Perm.R | Perm.W);                          // R, W
        Console.WriteLine(((Perm)7).ToString());                     // R, W, X
        Console.WriteLine((HttpStatus)404);                          // NotFound
        Console.WriteLine(default(Color));                           // Red（零值）
    }
}
```

这个例子把三个关键点串起来了：`sizeof` 直接反映底层类型（`Small : byte` 是 1）；`[Flags]` 只改变 `ToString()` 的格式化方式——没有 `[Flags]` 时 `(Perm)3` 会打印 `3`，加上之后才会拆成 `R, W`；零值总是合法值，所以 `default(Color)` 是 `Red`，把 0 留给 `None` 是 `[Flags]` 的设计惯例（Framework Design Guidelines 的建议，不是语言强制）。⚠️ `[Flags]` 不会阻止你写 `(Perm)8`，`Enum.IsDefined` 对组合值返回 `false`（它只认识单个常量），要判断标志位得用手动 `HasFlag` 或位运算。C# 对枚举的穷尽性只给分析器警告而不报错，`switch` 表达式漏分支会得到 `CS8509` 警告而不是编译失败。序列化上，`System.Text.Json` 默认把枚举写成数字，要写字符串得加 `JsonStringEnumConverter`；这也是跨版本兼容的坑——数字一旦换常量顺序就错位。

📘 [MS Learn · Enumeration types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `enum` 是引用类型、编译期常量集合，从 Dart 2.17 起支持 **enhanced enum**：成员可以带 final 字段、可以有构造器、方法和 `static` 成员，还能实现接口（该版本的发布说明把它列为 2.17 的语言特性）。没有 enhanced 之前的枚举只能当纯标签用。

```dart
enum Planet {                       // 最简形式：index 0 起
  mercury, venus, earth
}

enum Vehicle implements Comparable<Vehicle> {     // enhanced enum（2.17+）
  car(4, 'vroom'),                                  // 成员带构造器参数
  bike(2, 'ring');

  const Vehicle(this.wheels, this.sound);           // 构造器必须 const
  final int wheels;                                 // 字段必须 final
  final String sound;
  int get wheelCount => wheels;
  @override
  int compareTo(Vehicle other) => wheels.compareTo(other.wheels);  // 实现接口
  static Vehicle heaviest() => car;                  // 可以有 static 成员
}

void main() {
  print(Vehicle.car.wheels);          // 4
  print(Vehicle.bike.name);           // bike
  print(Vehicle.values.length);       // 2
  print(Planet.earth.index);          // 2
  print(Planet.mercury.name);         // mercury
  print(Vehicle.values.map((v) => v.name).toList());  // [car, bike]
}
```

enhanced enum 的限制是构造器必须是 `const`、所有实例字段必须是 `final`，因此成员在编译期就完全初始化好；`.index` 等于声明位置（0 起），`.name` 是标识符字符串，`values` 是全部成员的常量列表，`byName` 按名字查找。⚠️ 两个陷阱：第一，`.index` 随声明顺序变化，写进数据库或 JSON 后就不能重排成员；`name` 相对稳定但也别轻易改名。第二，`values.byName(s)` 在名字不存在时抛 `ArgumentError`，来自外部输入时要用 `firstWhere` 加 `orElse` 或 `try/catch`。序列化上，Dart 的 `json_serializable` 默认把枚举按 `name` 字符串编码（可用 `@JsonValue` 改），手写时通常是 `values.byName(json['kind'] as String)`。

📘 [Dart · Enumerated types](https://dart.dev/language/enum)

{{% /tab %}}

{{% tab header="R" %}}

R **没有枚举类型**。最接近的两个机制是 `factor`（带 `levels` 的分类变量，天然封闭且可有序）和「大写常量 + `switch()`」的手写方案。R 是向量化、动态类型的语言，`factor` 的成员在内存里是整数编码加一个 level 属性，比手写常量更接近其他语言的枚举。

```r
f <- factor(c("low", "high", "low"), levels = c("low", "mid", "high"))
print(f)                       # [1] low  high low    Levels: low mid high
print(as.integer(f))           # [1] 1 3 1（按 levels 的位置编码）
print(levels(f))               # [1] "low"  "mid"  "high"
print(nlevels(f))              # [1] 3
print(f[2] > f[1])             # [1] NA + 警告：'>' not meaningful for factors

g <- factor(c("b", "a"))       # 不给 levels：默认按去重后的字典序
print(levels(g))               # [1] "a" "b"

o <- ordered(c("mid", "low"), levels = c("low", "mid", "high"))
print(o[1] > o[2])             # [1] TRUE

# 手写常量方案：没有封闭性，只有命名约定
COLOR_RED <- 1L; COLOR_GREEN <- 2L
name_of <- function(x) switch(x, "red", "green", "unknown")
print(name_of(COLOR_GREEN))    # [1] "green"
print(match("high", levels(f)))  # [1] 3（按 level 反查位置）
```

⚠️ `factor` 最大的坑是 **levels 默认按排序结果而不是出现顺序**：`factor(c("b", "a"))` 的 levels 是 `"a" "b"`，`as.integer` 于是给 `2 1`，跟直觉相反；要给业务顺序必须显式传 `levels =`。第二个坑是赋值新值：`f[1] <- "mid"` 合法，但 `f[1] <- "ultra"` 会产生 `NA` 加警告（`invalid factor level`），因为 factor 是封闭的——这一点反而比整数常量更安全。第三个坑是 `as.integer(f)` 只给位置，任何重新排序 levels 的操作都会改变数值语义，跨会话持久化要存字符串。要遍历就用 `for (lv in levels(f))`，要判断合法值用 `lv %in% levels(f)`。

📘 [R · factor](https://stat.ethz.ch/R-manual/R-devel/library/base/html/factor.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `enum` 是编译期完整的整数标签类型，可以指定底层整数类型，也可以声明为**非穷尽（non-exhaustive）**——用一个 `_` 变体表示「还有其他值」。它还是值类型、静态类型；Zig 没有类，所以「带数据的枚举」由另一个构造 `union(enum)`（标记联合，tagged union）承担，两者配合才等价于 Rust 的 `enum`。

```zig
const std = @import("std");

const Color = enum { red, green, blue };            // 默认 tag 从 0 起
const Code = enum(u8) { ok = 1, fail = 2 };         // 指定底层类型与显式 tag
const Opcode = enum(u8) {                           // 非穷尽：允许表外值
    nop = 0,
    push = 1,                                       // _ 之外的具名变体
    _,                                              // 允许任意 u8
};

const Shape = union(enum) {                         // 标记联合 = 带数据的枚举
    circle: f64,
    rect: struct { w: f64, h: f64 },
    none,
};

pub fn main() void {
    std.debug.print("{d} {d}\n", .{ @intFromEnum(Color.green), @sizeOf(Color) }); // 1 1
    std.debug.print("{s} {d}\n", .{ @tagName(Code.fail), @intFromEnum(Code.fail) }); // fail 2
    const s = Shape{ .rect = .{ .w = 3, .h = 4 } };
    std.debug.print("{s}\n", .{@tagName(s)});       // rect
}
```

指定 `enum(u8)` 之后 `@sizeOf` 就是 1 字节；不给底层类型时编译器挑最小的整数。`@intFromEnum`/`@enumFromInt` 是标准的整数互转内建，`@tagName` 拿标识符字符串。⚠️ 非穷尽枚举的两个关键规则：第一，`@intFromEnum` 永远可用，但 `switch` 时**必须**有 `else` 分支（或 `_` 分支），否则编译错误；第二 `@enumFromInt` 把越界整数转成非穷尽枚举是安全的（值变成 `_`），但把它转成穷尽枚举在安全构建模式下会是**受检的非法行为**（checked illegal behavior，Debug/ReleaseSafe 下 panic）。序列化时通常用 `@intFromEnum` 写数字、`std.enums.fromInt`（返回 `?T`）或 `std.meta.intToEnum`（返回错误联合）做可失败的解析，不要直接 `@enumFromInt` 处理不可信输入。

📘 [Zig Language Reference · enum](https://ziglang.org/documentation/master/#enum)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有枚举**。标准做法是用 table 装一组命名常量，再加一张反查表；Lua 5.4 起还能用 `<const>` 属性把局部变量声明为常量，但这只是防重新赋值，不提供封闭性。Lua 是动态类型、值语义（table 是引用语义）、运行时构造，一切约束都得自己写。

```lua
-- 方案一：正向表 + 反向表
local Color = { RED = 1, GREEN = 2, BLUE = 3 }
local ColorName = {}                      -- 反查：值 -> 名字
for k, v in pairs(Color) do ColorName[v] = k end
print(Color.RED, ColorName[2])            -- 1  GREEN

-- 方案二：字符串常量（更适合可读的序列化）
local Suit = { HEARTS = "H", SPADES = "S" }
print(Suit.HEARTS)                        -- H

-- 方案三：Lua 5.4+ 的 <const> 局部常量
local MAX_LEVEL <const> = 10
-- MAX_LEVEL = 11                         -- 🛑 编译期报错：attempt to assign to const variable

-- 方案四：用 metatable 拒绝写入未知键（近似"封闭"）
local Status = setmetatable({ OK = 0, FAIL = 1 }, {
  __index = function(_, k) error("unknown status: " .. tostring(k), 2) end,
  __newindex = function() error("Status is read-only", 2) end,
})
print(Status.OK)                          -- 0
-- print(Status.BOGUS)                    -- 🛑 unknown status: BOGUS
local count = 0
for _ in pairs(Color) do count = count + 1 end
print(count)                              -- 3（成员个数要靠自己数）
```

这张表是普通 table，所以 `Color.RED = 99` 随时可以改；要真正只读得靠 `__newindex` 元方法（`table.freeze` 不是 Lua 标准库的一部分，别按 JS 习惯去找它）。方案四的 `__index` 兜底是个好习惯：读错常量名会立刻抛错，而不是得到 `nil` 然后在别处崩掉。⚠️ 用 `pairs` 遍历常量表的顺序是**未指定**的（手册只说 "The order in which the indices are enumerated is not specified"，实现上还可能因哈希随机化而在不同运行间变化），所以反查表不能用"遍历顺序"来推导，必须显式建表；需要稳定顺序就得用数组 `{ "RED", "GREEN" }` 配 `ipairs`。序列化时通常直接写字符串键，数字值虽然省空间但一旦有人插入常量就会错位。

📘 [Lua 5.5 Reference Manual · Table Manipulation](https://www.lua.org/manual/5.5/manual.html#6.7)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 有真正的 `enum` 关键字（这是它为 JS 添加的少数会生成运行时代码的语法糖之一），也有更新的替代路线：`as const` 对象加字面量联合类型。前者在编译期与运行时都存在，后者**只有类型层**、运行时就是一个普通对象——这个区别在 Node 26 的原生类型剥离模式下变成硬约束。

```typescript
enum Color { Red, Green, Blue }              // 数值枚举：编译出双向映射对象
enum Status { Ok = "OK", Fail = "FAIL" }     // 字符串枚举：只生成单向映射
const enum Tiny { A = 1, B = 2 }             // const enum：使用处内联，不生成对象

// 替代路线：as const + 字面量联合类型（运行时可被 Node 直接剥离）
const Dir = { Up: "UP", Down: "DOWN" } as const;
type Dir = (typeof Dir)[keyof typeof Dir];   // "UP" | "DOWN"

function move(d: Dir): string {
  return d === Dir.Up ? "向上" : "向下";      // 类型收窄到字面量
}

console.log(Color.Red, Color[1]);            // 0 Green（数值枚举双向映射）
console.log(Status.Ok);                      // OK
console.log(Dir.Up);                         // UP
console.log(move(Dir.Down));                 // 向下
// 运行时形状：enum 生成 { 0: "Red", 1: "Green", Red: 0, Green: 1 }
console.log(Object.keys(Color).length);      // 6（3 个名字 + 3 个数字键）
```

数值枚举会生成**双向映射**（`Color[0] === "Red"` 且 `Color.Red === 0`），字符串枚举只生成 `{ Ok: "OK" }`，所以 `Status["OK"]` 拿不到 `"Ok"`——这是最常见的困惑点。`const enum` 在使用处内联成字面量（编译产物里只剩字面量与 `/* Color.Red */` 注释），不生成运行时对象，因此拿不到任何运行时反查表，也不能把枚举对象传给外部库；`isolatedModules` 与 ambient `const enum` 本质上不兼容（跨项目引用会报错），`preserveConstEnums` 可以让它照常生成对象。⚠️ 关键版本约束：`--erasableSyntaxOnly`（TypeScript 5.8 引入）会把 `enum` 与 `const enum` 声明都判为 **TS1294 编译错误**（"This syntax is not allowed when 'erasableSyntaxOnly' is enabled."），因为 `enum` 有运行时语义、无法被单纯删除；例外是 `declare enum` 这种 ambient 声明，因为它整体会被擦除。这个开关只是 `tsc` 侧的护栏，Node 并不读 `tsconfig.json`；Node 24 LTS 的类型剥离遇到 `enum` 直接抛 `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`（可用 `--experimental-transform-types` 强制转换），而 Node 26.0.0 起该转换 flag 已被移除、只剩 `--no-strip-types`，所以想在 Node 里原生跑 TS 就必须改用 `as const` 对象方案。要写整数协议又不想放弃剥离，可以保留 `const Color = { Red: 0 } as const` 这种形状。

📘 [TypeScript · enums](https://www.typescriptlang.org/docs/handbook/enums.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有枚举**。最常用的替代是 `Object.freeze` 出来的普通对象：名字齐全、语义清楚，但冻结只是**浅冻结**，也没有任何类型层面的封闭性。另一条路是用 `Symbol` 做真正唯一的标签。

```javascript
// 方案一：Object.freeze 常量对象
const Color = Object.freeze({ RED: 0, GREEN: 1, BLUE: 2 });
console.log(Color.RED, Object.isFrozen(Color));   // 0 true
Color.RED = 99;                                    // 静默失败（非严格模式）
console.log(Color.RED);                            // 0（严格模式会抛 TypeError）

// 反向映射要自己建
const ColorName = Object.freeze(
  Object.fromEntries(Object.entries(Color).map(([k, v]) => [v, k])));
console.log(ColorName[2]);                         // BLUE

// 方案二：Symbol 做真正唯一的身份
const UNKNOWN = Symbol("unknown");
const OTHER = Symbol("unknown");                   // 同描述但不同身份
console.log(UNKNOWN === OTHER);                    // false（Symbol 保证唯一）
console.log(typeof UNKNOWN, UNKNOWN.toString());   // symbol Symbol(unknown)

// 方案三：类 + static readonly 字段
class Suit { static HEARTS = "H"; static SPADES = "S"; }
console.log(Suit.HEARTS);                          // H
console.log(Object.keys(Color).length);            // 3（成员数就是键数）
```

`Object.freeze` 只冻结对象自身属性，如果值本身是对象（`Object.freeze({ A: { x: 1 } })`）内部对象仍可改，这是它的浅冻结陷阱；对常量表这种「值为原始类型」的用法才安全。`Symbol` 适合做内部标签（Map 的键、事件名），它不会被字符串意外撞上，但 JSON 序列化会直接丢弃 Symbol 键，所以不适合做协议值。⚠️ JS 里最常见的枚举 bug 是拼错常量名：`Color.GREEM` 得到 `undefined` 而不是报错，一路传到序列化才炸；要兜底就在取值处显式检查 `if (!(name in Color)) throw new Error(...)`，或者干脆用 TypeScript 的 `as const` 让编译器替你查。另一个坑是 `for...in` 会遍历原型链上的可枚举属性，遍历常量表要用 `Object.keys` 或 `Object.entries`。

📘 [MDN · Object.freeze()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 从 **8.1** 起有了真正的枚举：`enum` 是独立的类型，成员是单例对象，可以有方法、常量、实现接口，但不能有实例属性。它分两种——**纯枚举（pure enum）**成员没有标量值，**backed enum** 成员带一个 `int` 或 `string` 标量值；这是 PHP 枚举最核心的分岔。

```php
<?php
enum Suit {                       // 纯枚举：成员只有名字
    case Hearts;
    case Spades;
    public function label(): string {          // 枚举可以有方法
        return match($this) {
            Suit::Hearts => '红桃',
            Suit::Spades => '黑桃',
        };                                     // match 对枚举穷尽时无 default
    }
}

enum Status: string {             // backed enum：底层是 string
    case Ok = 'OK';
    case Fail = 'FAIL';
    public function isError(): bool { return $this === Status::Fail; }
}

enum Code: int implements JsonSerializable {   // 可以带接口
    case NotFound = 404;
    public function jsonSerialize(): mixed { return $this->value; }
}

echo Suit::Hearts->name;                       // Hearts
echo Suit::Hearts->label();                    // 红桃
echo Status::Ok->value;                        // OK
echo Status::from('FAIL')->name;               // Fail
var_dump(Status::tryFrom('nope'));             // NULL
echo count(Suit::cases());                     // 2
echo Status::Ok instanceof Status ? 'yes' : 'no';   // yes
```

枚举成员用 `->name` 拿标识符、`->value` 拿标量值（纯枚举没有 `->value`，访问会报错）；`::cases()` 返回全部成员数组（声明顺序），`::from()`/`::tryFrom()` 按标量值反查（只有 backed enum 才有，`from` 失败抛 `ValueError`，`tryFrom` 返回 `null`）。接口方面 PHP 允许枚举实现任意多个接口，但它不能声明 `__toString` 之类的魔术方法（枚举只允许 `__call`、`__callStatic`、`__invoke`），因此实践中无法实现 `Stringable`；枚举也不能被继承或实例化——`enum` 隐含 `final`，`UnitEnum`/`BackedEnum` 由引擎自动附加、用户不能自己实现它们的 `cases()`/`from()`。⚠️ 三个硬限制：枚举**不能有属性**（"cases are forbidden from having state"，要附加数据只能靠方法、常量或 `match`）；backed enum 的标量值类型只能是 `int` 或 `string`（不能是 `float`/`bool`，也不能 `int|string` 混用）；每个 backed case 必须显式给出唯一标量值，引擎不会自动编号。序列化上 `json_encode(Status::Ok)` 直接输出 `"OK"`（backed enum 由引擎按 value 编码），纯枚举 `json_encode` 会报错，要覆盖默认行为就实现 `JsonSerializable`；`serialize()` 用的是专用格式（`E` 前缀加名字，如 `Status:Ok` 序列化成 `E:9:"Status:Ok";`），同样按名字而非标量值。PHP 8.5 没有新增枚举语言特性，只有行为层面的调整（例如枚举与布尔值的松散比较统一按 `(bool)$object`、`ArrayObject` 不再接受枚举）。

📘 [PHP · Enumerations](https://www.php.net/manual/en/language.enumerations.basics.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby **没有枚举类型**。惯用替代是 `Symbol`（内部化的不可变标识符）配常量，需要"带数据的枚举"时用 `Data.define`（Ruby 3.2 起）或普通类 + `case/in`。Ruby 是动态类型、一切皆对象、`Symbol` 是值语义的单例。

```ruby
module Color                     # 常量做枚举成员
  RED = :red
  GREEN = :green
  ALL = [RED, GREEN].freeze      # 显式成员列表
end
puts Color::RED                  # red
puts :red.to_s                   # "red"（Symbol 转字符串）
puts Color::ALL.include?(:red)   # true（自己写合法性检查）
puts :green.equal?(:green)       # true（Symbol 内部化，同值即同对象）

Shape = Data.define(:kind, :a, :b)          # Ruby 3.2+：不可变值对象
c = Shape.new(kind: :circle, a: 2.0, b: nil)
r = Shape.new(kind: :rect, a: 3.0, b: 4.0)
def area(s)
  case s
  in { kind: :circle, a: radius } then 3 * radius * radius
  in { kind: :rect, a: w, b: h } then w * h
  end                                       # ⚠️ 没有穷尽性检查
end
puts area(c), area(r)                       # 12.0  12.0
puts Shape.members.inspect                  # [:kind, :a, :b]
puts c.with(a: 5.0).a                       # 5.0（Data 提供 with）
```

`Symbol` 的关键性质是**内部化（interned）**：`:red` 在内存里只有一份，比较是 O(1) 的身份比较，而且不可变，所以特别适合做标签、哈希键和枚举成员。`Data.define` 生成不可变的值对象，自带 `members`、`with`、基于成员的值相等与 `deconstruct_keys`（所以能配合 `case/in` 做模式匹配）。⚠️ Ruby 的 `case/in` **没有穷尽性检查**：如果所有分支都不匹配且没有 `else`，会抛 `NoMatchingPatternError`（运行时才发现），漏掉一个分支编译器不会提醒；要主动兜底就写 `else raise ArgumentError`。另一个坑是常量没有封闭性：`Color::BLUE = :blue` 在别处照样能加，`Color.constants` 的顺序也不保证（源码里 `[:RED, :GREEN]` 可能打印成 `[:GREEN, :RED]`），要稳定顺序必须像 `ALL` 那样显式维护数组。

📘 [Ruby · Symbol](https://docs.ruby-lang.org/en/master/Symbol.html)

{{% /tab %}}

{{< /tabpane >}}

### 取值、转换与遍历

枚举的「值」有三个互不等价的含义：**声明位置**（序号）、**底层标量值**（原始值）、**标识符名字**。本节按这三个含义组织：序号与底层值怎么互转、字符串与枚举怎么互转、怎么遍历全部成员。分歧集中在三处：转换失败是抛异常、给 `Optional`/`nil` 还是静默得到一个非法值；遍历顺序是声明顺序还是哈希顺序；以及序列化的默认表示是数字还是字符串——这最后一点决定了你能不能安全地重排成员。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的转换全是显式的：无字段枚举用 `as` 拿判别值，反向要自己写或依赖 `TryFrom`；带字段的变体只能 `match` 取数据。语言不提供「把名字变成员」的内建函数——这是 `strum` 这类 crate 存在的理由。所有转换都是编译期类型检查的值操作，运行时不保留任何元数据。

```rust
#[derive(Debug, PartialEq)]
enum Code { Ok = 1, Fail = 2 }

impl Code {
    fn from_u8(v: u8) -> Option<Self> {          // 手写可失败反查
        match v { 1 => Some(Code::Ok), 2 => Some(Code::Fail), _ => None }
    }
    fn name(self) -> &'static str {               // 手写名字映射
        match self { Code::Ok => "Ok", Code::Fail => "Fail" }
    }
}

fn main() {
    println!("{}", Code::Ok as u8);                // 1（as 只在无字段枚举上合法）
    println!("{:?}", Code::from_u8(2));             // Some(Fail)
    println!("{:?}", Code::from_u8(9));             // None
    println!("{}", Code::Ok.name());                // Ok
    for c in [Code::Ok, Code::Fail] {              // 遍历：自己维护数组
        print!("{} ", c as u8);
    }
    println!();                                      // 1 2
}
```

`as` 是无检查的位级转换：`Code::Ok as u8` 拿判别值，但反向 `9 as Code` 只在判别值恰好合法时才有意义，Rust 不会替你校验，所以反向一律用 `TryFrom` 或手写 `match`。`#[derive(PartialOrd, Ord)]` 会按判别值比较，`#[derive(Hash)]` 让枚举能做 `HashMap` 键，`#[derive(Default)]` 可以给某个变体标 `#[default]`。⚠️ 序列化是最容易踩的地方：`serde` 默认把无字段变体写成名字字符串（`"Ok"`）、带字段变体写成外部标签对象（`{"Rect":{"w":3.0}}`），换句话说**默认表示是名字而不是数字**，改名即破坏兼容；要写数字得用 `serde_repr` crate 或 `#[serde(into = "u8")]`。遍历方面 Rust 没有反射式枚举遍历，标准做法是自己维护一个 `const ALL: [Code; 2]` 数组，`strum` 的 `EnumIter` 可以自动生成。

📘 [Rust std · `TryFrom`](https://doc.rust-lang.org/std/convert/trait.TryFrom.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 raw value 型枚举提供两条不对称的通道：`x.rawValue` 永远成功，`T(rawValue:)` 是可失败初始化器（返回 `Optional`），未知原始值给 `nil` 而不是崩溃。遍历要么实现 `CaseIterable` 拿 `allCases`，要么手写数组。这一切都是编译期生成的，没有反射参与。

```swift
enum Direction: Int, CaseIterable {
    case north = 1, south, east, west
}
enum Suit: String { case hearts = "H", spades = "S" }

print(Direction.east.rawValue)                  // 3
print(Direction(rawValue: 2)!)                  // south
print(Direction(rawValue: 99) as Any)           // nil（不崩溃）
print(Direction.allCases.map(\.rawValue))        // [1, 2, 3, 4]
print(Suit.spades.rawValue)                      // S
print(Suit(rawValue: "X") == nil)                // true
print(String(describing: Direction.south))       // south
print(Direction.allCases.count, Direction.allCases.first!)  // 4 north
// 序号：没有内建 ordinal，用 allCases.firstIndex(of:) 代替
print(Direction.allCases.firstIndex(of: .east)!) // 2（从 0 起的位置）
// 关联值型没有 rawValue：
enum Barcode { case qr(String) }
// Barcode.qr("x").rawValue                     // 🛑 编译错误
```

键的用法是记住「`rawValue` 出去容易、回来要解包」：`Direction(rawValue:)` 返回 `Optional`，所以必须 `if let`/`guard let` 或 `!`（外部输入绝不要 `!`）。序号没有内建方法，`allCases.firstIndex(of:)` 给的是 0 起的位置，而 `rawValue` 是从 1 起的原始值，两者只差 1 但含义完全不同——这是 Swift 枚举最容易混的一对概念。`CaseIterable` 是编译器合成的协议（只要没有关联值就能自动合成 `allCases`），关联值型枚举不能 `CaseIterable`、也没有 `rawValue`。序列化上 `Codable` 对 raw value 型枚举默认编码 raw value，对关联值型枚举会合成出嵌套结构（形如 `{"qr":{"_0":"x"}}`），通常要手写 `Codable`。

📘 [Swift · Raw Values](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/enumerations/#Raw-Values)

{{% /tab %}}

{{% tab header="Go" %}}

Go 没有枚举，所以「转换」就是普通整数转换：`int(d)` 拿底层值，`Weekday(2)` 反向构造，两者都不检查范围。名字与值的映射靠手写 `String()` 方法或 `stringer` 工具生成，反向解析要自己写表或 `switch`。全部是运行时代码，没有编译期元数据。

```go
package main

import "fmt"

type Weekday int

const (
	Sunday Weekday = iota
	Monday
	Tuesday
)

var weekdayName = map[Weekday]string{Sunday: "Sunday", Monday: "Monday", Tuesday: "Tuesday"}
var nameWeekday = map[string]Weekday{"Sunday": Sunday, "Monday": Monday, "Tuesday": Tuesday}

func (d Weekday) String() string {
	if s, ok := weekdayName[d]; ok {
		return s
	}
	return fmt.Sprintf("Weekday(%d)", int(d))   // 未知值兜底，不 panic
}

func ParseWeekday(s string) (Weekday, bool) {
	d, ok := nameWeekday[s]                       // 反查用 map，O(1)
	return d, ok
}

func main() {
	fmt.Println(int(Tuesday), Tuesday)            // 2 Tuesday
	d, ok := ParseWeekday("Monday")
	fmt.Println(d, ok)                            // Monday true
	_, ok = ParseWeekday("Funday")
	fmt.Println(ok)                               // false
	fmt.Println(Weekday(99))                      // Weekday(99)
	all := []Weekday{Sunday, Monday, Tuesday}     // 遍历要自己维护切片
	for _, v := range all {
		fmt.Print(int(v), " ")
	}
	fmt.Println()                                 // 0 1 2
}
```

`iota` 常量是编译期常量，可以用在数组长度、`switch case`、位运算里；`Weekday(2)` 这样的转换没有检查，越界值一样能存进变量。`String()` 方法要覆盖全部合法值并给未知值兜底，否则 `fmt` 打印越界值时会 panic（输出形如 `%!v(PANIC=String method: runtime error: index out of range)`），这是 Go 枚举方案里最容易线上翻车的一处。⚠️ 序列化默认走 `encoding/json`：因为 `Weekday` 的底层类型是 `int`，JSON 里是数字；想让 JSON 用字符串必须实现 `MarshalJSON`/`UnmarshalJSON`（`MarshalJSON` 里用 `String()`，`UnmarshalJSON` 里走反查表），这也是为什么很多人干脆把 `Weekday` 定义成 `string` 类型再加 `const`。遍历没有内建机制，要么手写切片，要么用 `go:generate stringer -type=Weekday` 生成一份 `_Weekday_name`/`_Weekday_index` 表。

📘 [Go · `fmt.Stringer`](https://pkg.go.dev/fmt#Stringer)

{{% /tab %}}

{{% tab header="Python" %}}

Python 三条通道都齐全，而且**失败行为按通道区分**：`Color(2)` 反查按值、失败抛 `ValueError`；`Color["RED"]` 反查按名、失败抛 `KeyError`；`getattr(Color, name, default)` 或 `Color.__members__.get(name)` 才给默认值。`.` 访问取成员，`.value`/`.name` 取两个属性，`list(ColorClass)` 遍历成员。

```python
from enum import Enum, IntEnum, StrEnum, auto

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

class Kind(StrEnum):          # 3.11+
    A = "a"
    B = "b"

print(Color.RED.name, Color.RED.value)        # RED 1
print(Color(2), Color["BLUE"])                 # Color.GREEN Color.BLUE
print([c.name for c in Color])                 # ['RED', 'GREEN', 'BLUE']
print(list(Color.__members__))                 # ['RED', 'GREEN', 'BLUE']
try:
    Color(99)
except ValueError as e:
    print(type(e).__name__)                    # ValueError
try:
    Color["NOPE"]
except KeyError as e:
    print(type(e).__name__)                    # KeyError
print(Color.__members__.get("NOPE", "fallback"))  # fallback
print(Kind.A.value, Kind.A == "a")             # a True
print(isinstance(Color.RED, Color), Color.RED is Color(1))  # True True
```

`Color(2)` 与 `Color["BLUE"]` 的区别是新手最常混的：前者按 **值** 反查、后者按 **名字** 反查，异常类型也不同（`ValueError` 对 `KeyError`）。`.` 取值不会 KeyError 是因为成员名在类定义时就绑定成了类属性，而 `Color(99)` 是运行时查表。遍历用 `list(Color)`（声明顺序），`Color.__members__` 是名字到成员的映射且包含别名；`Flag`/`IntFlag` 遍历时会跳过组合值与别名。⚠️ 序列化要显式：`json.dumps(Color.RED)` 会抛 `TypeError`（`Enum` 不是 JSON 原生类型），`IntEnum`/`StrEnum` 才能直接被序列化；惯用做法是继承 `str, Enum`（3.11 前）或直接用 `StrEnum`（3.11 起），或者给 `json.dumps(..., default=lambda o: o.value)`。枚举成员的 `value` 不该写进持久化协议，因为 `auto()` 编号会随插入顺序变。

📘 [Python · Enum HOWTO](https://docs.python.org/3/howto/enum.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的枚举转换接口很整齐：`ordinal` 是位置属性，`name` 是名字属性，`valueOf()` 按名字反查（失败抛 `IllegalArgumentException`），`entries`（1.9 起）给缓存的成员列表，`enumValues<T>()`/`enumEntries<T>()`/`enumValueOf<T>()` 是泛型内联版本。没有按序号反查的内建函数，也没有 raw value 概念。

```kotlin
enum class Direction(val degrees: Int) {
    NORTH(0), EAST(90), SOUTH(180), WEST(270);
    companion object {
        fun fromDegrees(d: Int): Direction? = entries.firstOrNull { it.degrees == d }
    }
}

fun main() {
    println(Direction.EAST.ordinal)                 // 1
    println(Direction.EAST.name)                    // EAST
    println(Direction.valueOf("SOUTH"))             // SOUTH
    println(Direction.entries.map { it.name })      // [NORTH, EAST, SOUTH, WEST]
    println(Direction.fromDegrees(270))             // WEST
    println(Direction.fromDegrees(45))              // null
    println(enumValues<Direction>().size)           // 4
    // Direction.entries[99]                        // 🛑 IndexOutOfBoundsException
    println(entries<Direction>())                   // [NORTH, EAST, SOUTH, WEST]
}
inline fun <reified T : Enum<T>> entries(): List<T> = enumEntries<T>().toList()

// 失败处理：没有 tryValueOf，要自己包
fun parse(s: String): Direction? =
    runCatching { Direction.valueOf(s) }.getOrNull()
```

`ordinal` 是 0 起的声明位置，`name` 是标识符原文；`valueOf` 对未知名字抛 `IllegalArgumentException`，需要"返回值"的版本就自己包 `runCatching` 或 `entries.firstOrNull { it.name == s }`。`entries` 返回的是 `EnumEntries`（一个只读视图，内部复用同一个数组），`values()` 每次调用都克隆一个新数组——Kotlin 1.9 起官方建议一律用 `entries`，`values()` 在 IDE 里被软弃用提示。⚠️ 按序号反查没有内建支持，要 `entries.getOrNull(i)`；`ordinal` 与任何持久化字段绑定的风险跟 Java 完全一样，插入常量就错位。序列化上 `kotlinx.serialization` 默认按 `name` 编码（可加 `@SerialName` 改名），Java 原生序列化则用 `name`；如果枚举带属性（如上面的 `degrees`），序列化仍然只输出名字，属性值不会进 JSON。

📘 [Kotlin · Enum classes](https://kotlinlang.org/docs/enum-classes.html#working-with-enum-constants)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的枚举接口最完整：`ordinal()` 给位置、`name()` 给名字、`values()` 给全部成员数组、`valueOf(String)` 按名字反查。但**没有按序号的公开反查**，也没有 raw value 概念（除非自己在字段里存）。核心 API 都在 `java.lang.Enum` 上，`values()`/`valueOf()` 是编译器为每个枚举合成的静态方法。

```java
enum Suit {
    HEARTS("H", 1), SPADES("S", 4);
    private final String symbol;
    private final int rank;
    Suit(String symbol, int rank) { this.symbol = symbol; this.rank = rank; }
    public String symbol() { return symbol; }
    public int rank() { return rank; }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(Suit.SPADES.ordinal());        // 1
        System.out.println(Suit.SPADES.name());           // SPADES
        System.out.println(Suit.valueOf("HEARTS"));       // HEARTS
        System.out.println(Suit.values().length);          // 2
        Suit.values()[0] = Suit.SPADES;                    // ⚠️ 改的是副本，不影响枚举
        System.out.println(Suit.values()[0]);              // HEARTS
        System.out.println(Suit.HEARTS.symbol());          // H
        // 序号反查：values()[i] 或自己建表
        int i = 1;
        System.out.println(Suit.values()[i]);              // SPADES
        // 字符串反查的失败行为
        try { Suit.valueOf("NOPE"); }
        catch (IllegalArgumentException e) { System.out.println("IAE"); }  // IAE
        // EnumSet / EnumMap：专为枚举优化
        var set = java.util.EnumSet.of(Suit.HEARTS);
        var map = new java.util.EnumMap<Suit, Integer>(Suit.class);
        map.put(Suit.SPADES, 4);
        System.out.println(set + " " + map.get(Suit.SPADES));  // [HEARTS] 4
    }
}
```

`ordinal()` 是 0 起的声明位置、`name()` 是标识符原文；`valueOf` 对未知名字抛 `IllegalArgumentException`，且它接受的字符串必须与 `name()` 完全一致（大小写敏感）。⚠️ `values()` 每次调用都克隆一个新数组，所以 `Suit.values()[0] = ...` 不会影响枚举本身——这也是为什么热路径里应该把 `values()` 缓存成 `private static final Suit[] VALUES = values();`。按序号反查只能 `values()[i]`，要 O(1) 反查就自己建 `EnumMap` 或用 `values()[i]`（本身就是 O(1)）。序列化上 Java 原生序列化与主流 JSON 库（Jackson、Gson）默认都用 `name()`，这一点比 `ordinal()` 安全得多；`ordinal()` 只适合做数组下标或 `EnumSet` 内部的位序。`EnumSet`/`EnumMap` 是枚举专属的高性能容器（前者是位图、后者是数组），能用就用，比 `HashSet`/`HashMap` 快且类型安全。

📘 [Java API · `java.lang.Enum`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Enum.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的取值分两套：无作用域枚举可以隐式转 `int`，强作用域枚举必须 `static_cast` 或 `std::to_underlying`（C++23）。反向转换用 `static_cast<T>(i)`，C++17 起（CWG 1766）只要 `i` 落在枚举的合法范围内（有固定底层类型时就是底层类型的范围）就合法，超出范围仍是未定义行为；转换结果不做枚举器校验。名字与值互查没有内建机制，要自己写表或用 `magic_enum` 这类库。

```cpp
#include <cstdio>
#include <string_view>
#include <utility>
enum Color { RED, GREEN, BLUE };
enum class Fruit : unsigned char { Apple = 1, Pear = 2 };

constexpr std::string_view name_of(Fruit f) {          // 手写名字映射
    switch (f) {
        case Fruit::Apple: return "Apple";
        case Fruit::Pear:  return "Pear";
    }
    return "?";
}
constexpr bool parse(std::string_view s, Fruit& out) {  // 手写可失败解析
    if (s == "Apple") { out = Fruit::Apple; return true; }
    if (s == "Pear")  { out = Fruit::Pear;  return true; }
    return false;
}

int main() {
    int n = GREEN;                                     // ✅ 隐式转 int
    printf("%d\n", n);                                  // 1
    printf("%u\n", static_cast<unsigned>(Fruit::Pear)); // 2
    printf("%u\n", std::to_underlying(Fruit::Apple));   // 1（C++23）
    Fruit f = static_cast<Fruit>(2);                    // 反向：无检查
    printf("%s\n", name_of(f).data());                  // Apple
    Fruit parsed{};
    printf("%d\n", parse("Pear", parsed));              // 1
    printf("%d\n", static_cast<int>(parsed));           // 2
    constexpr Fruit all[] = {Fruit::Apple, Fruit::Pear};  // 遍历：手写数组
    for (Fruit x : all) printf("%s ", name_of(x).data());
    printf("\n");                                        // Apple Pear
}
```

`std::to_underlying`（`<utility>`，C++23）等价于 `static_cast<std::underlying_type_t<T>>`，是拿底层值的规范写法，读写二进制协议时用它而不是 `static_cast<T>`（后者在枚举有底层类型时也正确，但语义不如前者清楚）。反向 `static_cast<Fruit>(2)` 不做校验，值不在枚举器列表里仍然合法，所以 `switch` 必须有 `default`；`-Wswitch` 只对**无** `default` 的 `switch` 报"未处理枚举值"的警告，一旦写了 `default` 就没有穷尽性检查。⚠️ 无作用域枚举的名字会泄漏到外层作用域，两个不同的无作用域枚举不能有同名枚举器；强作用域枚举则可以有同名成员（`Color::RED` 与 `Fruit::RED` 可以共存）。序列化上没有任何内建约定：写文本就用 `name_of`，写二进制就用 `std::to_underlying`，别用 `sizeof(enum)` 假定宽度而不用指定的底层类型。遍历没有内建机制，标准做法是维护一个 `constexpr T all[]` 数组。

📘 [cppreference · `std::to_underlying`](https://en.cppreference.com/w/cpp/types/underlying_type)

{{% /tab %}}

{{% tab header="C" %}}

C 的枚举值就是整数常量，转换是两个方向的自由互转，没有任何检查；名字与值的互查完全没有内建支持，必须自己维护字符串数组或 `switch`。所有操作都是编译期常量运算，运行时不保留枚举类型信息。

```c
#include <stdio.h>
#include <string.h>

enum Color { RED, GREEN, BLUE };
typedef enum { IDLE, RUN, DONE } State;

static const char *const color_names[] = { "RED", "GREEN", "BLUE" };

static const char *color_name(enum Color c) {           /* 按值取名字 */
    if (c < RED || c > BLUE) return "?";
    return color_names[c];
}
static int color_parse(const char *s, enum Color *out) { /* 按名字取值 */
    for (int i = RED; i <= BLUE; i++) {
        if (strcmp(s, color_names[i]) == 0) { *out = (enum Color)i; return 1; }
    }
    return 0;
}

int main(void) {
    enum Color c = GREEN;
    int n = c;                                            /* ✅ 隐式转 int */
    printf("%d %s\n", n, color_name(c));                  /* 1 GREEN */
    enum Color back = (enum Color)2;                      /* 反向：无检查 */
    printf("%s\n", color_name(back));                     /* BLUE */
    enum Color parsed;
    printf("%d %s\n", color_parse("BLUE", &parsed), color_name(parsed)); /* 1 BLUE */
    printf("%d\n", color_parse("PURPLE", &parsed));       /* 0（失败返回 0） */
    for (int i = RED; i <= BLUE; i++) {                   /* 遍历：整数递增 */
        printf("%s ", color_names[i]);
    }
    printf("\n");                                         /* RED GREEN BLUE */
    printf("%d\n", (int)sizeof(color_names) / (int)sizeof(color_names[0])); /* 3 */
}
```

遍历之所以能用 `for (int i = RED; i <= BLUE; i++)`，全靠枚举器默认从 0 连续递增；一旦有人写了 `enum E { A = 1, B = 5 }`，这种写法就会漏值或读到表外，所以生产代码要么保证连续，要么显式维护成员数组。`color_names` 用 `static const char *const` 是为了让表本身与指针都不可改；名字表与枚举声明必须人工保持同步，这是 C 枚举最大的维护负担。⚠️ 字符串反查的失败约定要自己定：上面返回 0/1 并把结果写进出参，也可以用哨兵值（但枚举没有天然的"无效值"，除非专门加一个 `COLOR_INVALID`）。序列化时写文本走名字表、写二进制直接写 `int`，但要记住 `enum` 的底层类型由实现选择，跨平台协议必须自己指定类型（C23 的 `enum E : uint8_t` 或干脆 `uint8_t` 加常量）。

📘 [cppreference · C enum](https://en.cppreference.com/w/c/language/enum)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的枚举转换全部走构造器与 `Integer`/`Symbol`：`Integer(x)` 或 `Int(x)` 给原始值，`T(v)` 按原始值反向构造，`Symbol(x)` 给名字，`instances(T)` 给全部成员。没有内建的"按名反查"函数（`namemap` 是未导出的内部实现），也没有序号概念——序号只能自己数 `instances` 的位置。

```julia
using Printf
@enum Color::UInt8 RED GREEN BLUE
@enum Status begin
    OK = 0
    WARN = 10
end

println(Integer(BLUE), " ", BLUE)             # 2 BLUE
println(Color(1))                             # GREEN
println(Symbol(RED), " ", String(Symbol(WARN)))  # :RED WARN
println(instances(Color))                     # (RED, GREEN, BLUE)
println(length(instances(Color)))             # 3
println(findfirst(==(BLUE), instances(Color)))  # 3（1 起的"序号"）
# 按名反查：没有内建函数，用 instances + Symbol 比对
lookup(s) = findfirst(x -> Symbol(x) === Symbol(s), instances(Color)) |> i -> i === nothing ? nothing : instances(Color)[i]
println(lookup("GREEN"))                      # GREEN
println(lookup("NOPE"))                       # nothing
# 从整数构造：合法原始值给成员，越界值抛 ArgumentError（构造器内有 membership 检查）
println(Color(2))                             # BLUE
println(try Color(9) catch e; sprint(showerror, e) end)
                                              # ArgumentError: invalid value for Enum Color: 9
# println(reinterpret(Color, UInt8(9)))       # 只有 reinterpret 造出的非法值才有 <invalid #9>
# 遍历
for c in instances(Status)
    @printf("%s=%d ", Symbol(c), Integer(c))
end
println()                                      # OK=0 WARN=10
```

`Int(x)`/`Integer(x)` 拿原始值这一点在官方 docstring 里就有示例（`f(x::Fruit) = "I'm a Fruit with value: $(Int(x))"`），所以不要指望它给序号；序号只能通过 `findfirst(==(x), instances(T))` 得到，而且返回的是 1 起的索引。⚠️ 字符串打印也要分清：`print`/`println` 只给符号名（`GREEN`），`GREEN::Color = 1` 这种形式只在 REPL 的 `text/plain` 显示里出现，两者都来自 `Base/Enums.jl` 的 `print`/`show` 定义。越界构造 `Color(9)` 直接抛 `ArgumentError`，所以 Julia 枚举的封闭性既体现在"不能赋别的类型"，也体现在"不能构造非法原始值"；真拿到非法值的唯一常规途径是从 C 侧读入或 `reinterpret`。⚠️ `Symbol(x)` 与 `String(Symbol(x))` 是拿名字的标准途径（对非法值 `Symbol` 会 `KeyError`，只有内部 `_symbol` 有兜底），`namemap` 是 `Base.Enums` 的未导出内部函数，跨版本不保证存在，不要依赖。序列化默认写原始值（primitive type 的数字），要写名字就自己定义 `JSON.lower` 或包装类型。

📘 [Julia · Base.Enums](https://docs.julialang.org/en/v1/base/base/#Base.Enums.@enum)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的枚举转换最丰富，因为 `System.Enum` 提供了一整套静态方法：`Enum.Parse`/`Enum.TryParse` 按名字（或数字字符串）解析、`Enum.GetValues`/`Enum.GetNames` 遍历、`Enum.IsDefined` 校验、`Enum.GetValuesAsUnderlyingType`（.NET 7 起）拿底层类型数组，加上 `(int)x`/`(Color)2` 的强制转换与 `ToString()` 格式化。

```csharp
using System;
using System.Linq;

enum Color { Red = 1, Green = 2, Blue = 4 }
[Flags] enum Perm { None = 0, R = 1, W = 2, X = 4 }

class Program {
    static void Main() {
        Console.WriteLine((int)Color.Green);                  // 2
        Console.WriteLine(((Color)4).ToString());             // Blue（已定义值打印名字）
        Console.WriteLine(((Color)99).ToString());            // 99
        Console.WriteLine(Enum.Parse(typeof(Color), "Green")); // Green（大写敏感）
        Console.WriteLine(Enum.Parse<Color>("green", true));   // Green（ignoreCase）
        Console.WriteLine(Enum.TryParse<Color>("Nope", out var bad)); // False
        Console.WriteLine(Enum.TryParse<Color>("99", out var num));   // True（数字也认）
        Console.WriteLine(num);                                       // 99
        Console.WriteLine(Enum.IsDefined(typeof(Color), "Blue"));     // True
        Console.WriteLine(Enum.IsDefined(typeof(Color), (Color)3));   // False（3 不是单个常量）
        Console.WriteLine(string.Join(",", Enum.GetNames<Color>()));  // Red,Green,Blue
        Console.WriteLine(Enum.GetValues<Color>().Sum(x => (int)x));  // 7
        foreach (int v in Enum.GetValuesAsUnderlyingType<Color>())
            Console.Write(v + " ");                                    // 1 2 4
        Console.WriteLine();
        Console.WriteLine(Perm.R | Perm.W);                            // R, W
        Console.WriteLine((Perm.R | Perm.W).HasFlag(Perm.W));          // True
        Console.WriteLine(Enum.Format(typeof(Color), 2, "X"));         // 00000002
    }
}
```

`Enum.Parse` 与 `Enum.TryParse` 都能解析**名字或十进制数字字符串**（`"99"` 会成功并给出未定义值），所以解析外部输入后必须再 `Enum.IsDefined` 才算真正校验；`IsDefined` 对组合标志值返回 `false`（它只认单个常量），判断位组合要用 `HasFlag` 或位运算。`GetValues<T>()` 泛型重载从 .NET 5 起返回 `T[]`，老版本返回 `Array` 需要强制转换；`GetValuesAsUnderlyingType<T>()` 是 .NET 7 新增，专门用于拿底层整型数组（遍历性能更好、不装箱）。⚠️ `[Flags]` 的 `ToString()` 会把多位置位拆成逗号列表，但只对齐到 2 的幂常量：`(Perm)9` 会打印成 `R, 8`，因为 8 没有具名常量。序列化上 `System.Text.Json` 默认写数字，要写字符串需注册 `JsonStringEnumConverter`；`Enum.Parse` 对纯数字字符串不做区域解析，跨系统文本解析则建议显式传 `CultureInfo.InvariantCulture`。

📘 [MS Learn · `System.Enum`](https://learn.microsoft.com/en-us/dotnet/api/system.enum)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的枚举三条通道都在：`.index` 给 0 起的位置、`.name` 给标识符字符串、`values` 给全部成员的常量列表、`byName` 按名字反查（失败抛 `ArgumentError`）。没有按位置反查的内建方法，也没有 raw value 概念——要附加标量就把值放成员字段里（enhanced enum）。

```dart
enum Suit {
  hearts('H', 1),
  spades('S', 4);

  const Suit(this.symbol, this.rank);      // enhanced enum（2.17+）
  final String symbol;
  final int rank;

  static Suit? fromSymbol(String s) {       // 按字段反查，返回可空
    for (final v in Suit.values) {
      if (v.symbol == s) return v;
    }
    return null;
  }
  static Suit? fromIndex(int i) =>          // 自行实现按位置反查
      (i >= 0 && i < Suit.values.length) ? Suit.values[i] : null;
}

void main() {
  print(Suit.spades.index);                  // 1
  print(Suit.spades.name);                   // spades
  print(Suit.spades.symbol);                 // S
  print(Suit.values.map((v) => v.name).toList());  // [hearts, spades]
  print(Suit.values.byName('hearts'));       // Suit.hearts
  print(Suit.fromSymbol('S'));               // Suit.spades
  print(Suit.fromSymbol('X'));               // null
  print(Suit.fromIndex(5));                  // null
  try {
    Suit.values.byName('nope');
  } on ArgumentError catch (e) {
    print('ArgumentError');                  // ArgumentError
  }
  print(Suit.values.length);                 // 2
  print(Suit.values.byName('hearts').rank);  // 1
}
```

`.index` 是 0 起的声明位置，`.name` 是标识符原文，`.values` 是常量列表；`byName` 在名字不存在时抛 `ArgumentError`，来自外部输入（JSON、URL 参数）时不要直接用，要先自己遍历并返回 `null`（如 `fromSymbol`），或用 `firstWhere(..., orElse: ...)` 给一个默认成员。按位置反查没有内建方法，要么 `values[i]` 自己做范围检查（如 `fromIndex`），要么改用 `.name` 做键。⚠️ `.index` 与 `.name` 的稳定性差别很大：重排成员会改变 `index` 但 `name` 不变，所以持久化一律存名字；反过来，改名字会破坏按名字持久化的数据，改名必须配数据迁移。序列化上 `json_serializable` 的枚举字段默认用 `name`（可用 `@JsonValue` 换成自定义字段），手写解析就是 `values.byName(json['suit'] as String)`，输入不可信时要先校验。

📘 [Dart · Enumerated types](https://dart.dev/language/enum#declaring-enhanced-enums)

{{% /tab %}}

{{% tab header="R" %}}

R 没有枚举，取值与遍历全围绕 `factor`：`levels()` 给层级集合、`as.integer()` 给整数编码、`nlevels()` 给数量、`match(x, levels(f))` 按名字反查位置、`for (lv in levels(f))` 遍历。有序 factor（`ordered()`）才允许 `<`/`>` 比较。

```r
f <- factor(c("low", "high", "low"), levels = c("low", "mid", "high"))
print(as.integer(f))            # [1] 1 3 1（level 位置）
print(levels(f))                # [1] "low"  "mid"  "high"
print(nlevels(f))               # [1] 3
print(as.character(f))          # [1] "low"  "high" "low"（回到名字）
print(f[2] == "high")           # [1] TRUE（factor 与字符串比较，按 level）
print(match("high", levels(f))) # [1] 3（按名字反查位置）
print(f[2] > f[1])              # [1] NA + 警告：'>' not meaningful for factors
o <- ordered(f, levels = c("low", "mid", "high"))
print(o[2] > o[1])              # [1] TRUE（ordered 才能比）
print(table(f))                 # low high → 2 1
f[1] <- "mid"                   # 合法：mid 是已有 level
print(f)                        # [1] mid  high low    Levels: low mid high
```

未排序的 `factor` 用 `>`/`<` 会得到警告 `'>' not meaningful for factors` 与 `NA`，要比较必须先 `ordered()`（或 `as.ordered(f)` 之后再定义 level 顺序）；`==` 是例外，它按 level 比较字符串，所以 `f[2] == "high"` 合法。`as.integer(f)` 给的是 level 位置，一旦有人改了 `levels` 的顺序（哪怕只是重排 `f` 的 `levels=` 参数），同一份数据的整数编码就全变了——所以持久化必须存 `as.character(f)`，不能存整数。⚠️ `factor(..., levels = c(...))` 里出现数据中没有的 level 是合法的（会产生计数为 0 的层级），反过来数据里有而 `levels` 没列的会变成 `NA` 并警告 `invalid factor level`；这种"封闭性"是 R 里最接近枚举检查的机制。遍历用 `for (lv in levels(f))` 保证层级顺序，`for (v in f)` 则是逐个元素。序列化时 `write.csv` 默认写字符串，`saveRDS` 保留 factor 的 levels 属性。

📘 [R · factor](https://stat.ethz.ch/R-manual/R-devel/library/base/html/factor.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的取值靠内建函数：`@intFromEnum` 拿 tag 值、`@enumFromInt` 反向构造、`@tagName` 拿名字，`std.enums.values` 按声明顺序列出全部具名成员，`std.meta.stringToEnum` 按名字反查。全部是编译期展开的内建，没有运行时反射。

```zig
const std = @import("std");

const Color = enum(u8) { red = 1, green = 2, blue = 3 };

pub fn main() !void {
    const g = Color.green;
    std.debug.print("{d} {s}\n", .{ @intFromEnum(g), @tagName(g) });  // 2 green
    const back = @enumFromInt(3);                                      // 反向：不检查
    std.debug.print("{s}\n", .{@tagName(back)});                       // blue
    // 遍历：std.enums.values 返回编译期数组
    const all = std.enums.values(Color);
    std.debug.print("{d}\n", .{all.len});                              // 3
    inline for (all) |c| std.debug.print("{s} ", .{@tagName(c)});      // red green blue
    std.debug.print("\n", .{});
    // 按名字反查：std.meta.stringToEnum 返回 Optional
    const parsed = std.meta.stringToEnum(Color, "green");
    std.debug.print("{any}\n", .{parsed});                             // .green
    const missing = std.meta.stringToEnum(Color, "purple");
    std.debug.print("{any}\n", .{missing});                            // null
    // 可失败解析（处理不可信输入）：intToEnum 返回错误联合
    const ok = try std.meta.intToEnum(Color, 1);
    std.debug.print("{any}\n", .{ok});                                 // .red
    std.debug.print("{any}\n", .{std.meta.intToEnum(Color, 99)});       // error.InvalidEnumTag
}
```

⚠️ 版本敏感：Zig 0.15 的 `std.enums` 提供了 `values`（声明顺序的全部具名成员数组）、`tagName`（对非穷尽枚举安全的名字查询，无匹配给 `null`）、`fromInt`（带校验的整数反查）；`std.meta.tags` 在 0.15 里仍然存在（返回指向数组的指针），而 `std.enums.values` 是等价的 slice 版本、用起来更顺手。按名字反查用 `std.meta.stringToEnum`（返回 `?T`），带错误的整数反查是 `std.meta.intToEnum`（返回 `error.InvalidEnumTag`），新代码更推荐等价的 `std.enums.fromInt`（返回 `?T`，无错误联合）。`@enumFromInt` 与 `@intFromEnum` 是无检查的双向转换，值只要落在底层类型范围内就合法（穷尽枚举越界在安全构建里是受检非法行为），所以处理外部输入一律走上面那几条可失败通道，不要直接 `@enumFromInt`。`inline for` 遍历 `values` 是编译期展开，每个成员都会单独实例化循环体，所以能配合 `inline switch` 做编译期分派。序列化写数字就 `@intFromEnum`、写名字就 `@tagName`，反向用可失败版本，这是 Zig 枚举方案里唯一可靠的校验路径。

📘 [Zig · `std.enums`](https://ziglang.org/documentation/master/std/#std.enums)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有枚举，取值与反查全靠自己建的 table：正向表给名字到值，反向表给值到名字，遍历用 `pairs`（顺序未定义）或自己维护的数组（顺序确定）。没有任何检查，写错键只会得到 `nil`。

```lua
local Color = { RED = 1, GREEN = 2, BLUE = 3 }
local ColorName = {}
local Order = { "RED", "GREEN", "BLUE" }      -- 显式顺序数组

for _, k in ipairs(Order) do ColorName[Color[k]] = k end

print(Color.RED, ColorName[2])                -- 1 GREEN
print(Color["BLUE"], Color["PURPLE"])          -- 3 nil（写错键给 nil）
print(#Order)                                  -- 3（成员个数）
for i, k in ipairs(Order) do                   -- 按固定顺序遍历
  io.write(Color[k], " ")
end
io.write("\n")                                 -- 1 2 3

-- 反查解析：名字 -> 值，失败给 nil
local function parse(name) return Color[name] end
print(parse("GREEN"), parse("NOPE"))            -- 2 nil

-- 用字符串做值可以直接序列化
local Suit = { HEARTS = "H", SPADES = "S" }
print(Suit.HEARTS, type(Suit.HEARTS))            -- H string

-- pairs 的顺序不保证：
local n = 0
for _ in pairs(Color) do n = n + 1 end
print(n)                                         -- 3（个数可靠，顺序不可靠）
```

`pairs` 的遍历顺序在 Lua 里是**未指定**的（手册原文 "The order in which the indices are enumerated is not specified, even for numeric indices"，实现上还可能因哈希随机化而在不同运行间不同），所以"按枚举顺序遍历"必须依赖一个显式的数组（上面的 `Order`）加 `ipairs`，不能依赖 `pairs`。写错键（`Color.PURPLE`）得到 `nil`，之后拿 `nil` 做算术才报 `attempt to perform arithmetic on a nil value`，错误位置离现场很远；想提前暴露就用 `__index` 元方法抛错（见上一节）。⚠️ 数值编码的问题跟其他语言一样：反查表是按当前值建的，一旦有人改了 `Color.RED = 10` 而忘了重建 `ColorName`，两边就不一致；所以要么把表建成后立刻冻结（`__newindex` 抛错），要么干脆用字符串值（`Suit.HEARTS = "H"`），省掉反查表且直接可序列化。序列化写数字走正向表、写字符串直接写值，读回来用 `Color[name]` 并检查 `nil`。

📘 [Lua 5.5 Reference Manual · Table Manipulation](https://www.lua.org/manual/5.5/manual.html#6.7)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的取值分两派：`enum` 派有运行时的双向映射对象，`as const` 派只有编译期类型、运行时是普通对象。数值枚举自动生成反查表，字符串枚举**没有**反查表，需要自己建。类型层面还能用 `keyof typeof` 与索引访问把值收窄成字面量联合。

```typescript
enum Num { Red, Green, Blue }              // 数值枚举：双向映射
enum Str { Ok = "OK", Fail = "FAIL" }      // 字符串枚举：单向映射

const Dir = { Up: "UP", Down: "DOWN" } as const;
type Dir = (typeof Dir)[keyof typeof Dir];       // "UP" | "DOWN"

function nameOf(d: Dir): string { return d === Dir.Up ? "上" : "下"; }

console.log(Num.Red, Num[1], Num[99]);      // 0 Green undefined
console.log(Str.Ok, (Str as any)["OK"]);    // OK undefined（字符串枚举无反向映射）
console.log(Object.keys(Num).length);       // 6（3 名字 + 3 数字键）
console.log(Object.keys(Str).length);       // 2（只有名字）
const names = Object.keys(Str).filter(k => Number.isNaN(Number(k)));
console.log(names);                          // [ 'Ok', 'Fail' ] 手动取名字
console.log(Dir.Up, nameOf(Dir.Down));       // UP 下
console.log(Object.values(Num).filter(v => typeof v === "number")); // [0,1,2]
// 校验外部输入
function isNum(v: number): v is Num { return v in Num && typeof Num[v] === "string"; }
console.log(isNum(1), isNum(99));            // true false
```

数值枚举的双向映射是编译产物：`Num[1] === "Green"` 且 `Num.Green === 1`，所以 `Object.keys(Num)` 会同时给出名字与数字字符串键（长度是成员数的两倍）；字符串枚举只生成 `{ Ok: "OK" }`，`(Str as any)["OK"]` 是 `undefined`，要反查必须 `Object.entries(Str).find(([, v]) => v === x)` 或自己建表。⚠️ 这个差异直接影响校验代码：`1 in Num` 对数值枚举是 `true`，所以必须像 `isNum` 那样同时检查"值存在且对应的是字符串键"，否则 `Num[99]` 的 `undefined` 会被漏过。`const enum` 更特殊：它不生成对象，使用处直接内联字面量，因此**不能**做任何运行时反查，也无法在 `isolatedModules` 下跨文件可靠使用。序列化上数值枚举写数字、字符串枚举写字符串，两者都随成员改名/重排而变；`as const` 对象写的字符串通常最稳，但要注意 `Object.values` 的顺序依赖对象插入顺序（字符串键例外，整数样式的键会被排到前面并升序）。

📘 [TypeScript · Enums at runtime](https://www.typescriptlang.org/docs/handbook/enums.html#enums-at-runtime)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有枚举**，所以"取值"就是访问对象属性：属性存在给值、不存在给 `undefined`（不抛错），反查表要自建，遍历用 `Object.values`/`Object.entries` 加 `Object.freeze`。用 `Symbol` 做成员时连名字都没有（`Symbol` 不进 JSON、不可枚举）。

```javascript
const Color = Object.freeze({ RED: 0, GREEN: 1, BLUE: 2 });
const ColorName = Object.freeze(
  Object.fromEntries(Object.entries(Color).map(([k, v]) => [v, k])));

console.log(Color.GREEN, Color.PURPLE);           // 1 undefined
console.log(ColorName[1]);                         // GREEN
console.log(Object.values(Color));                 // [0, 1, 2]
console.log(Object.keys(Color).length);            // 3
for (const [name, value] of Object.entries(Color)) {
  console.log(name, value);                        // RED 0 / GREEN 1 / BLUE 2
}
// 校验：属性名必须是自己拥有的键，而不是原型链上的
function isColor(name) { return Object.hasOwn(Color, name); }
console.log(isColor("RED"), isColor("toString"));  // true false
// Symbol 成员
const UNKNOWN = Symbol("unknown");
console.log(typeof UNKNOWN, JSON.stringify({ a: UNKNOWN }));  // symbol {}
```

`Color.PURPLE` 给 `undefined` 而不是报错，这是 JS 方案的最大风险：拼错常量名会一路静默传播，直到某个下游 `switch` 落到 `default` 或者 `Object.fromEntries` 里出现 `undefined` 键才暴露。校验必须用 `Object.hasOwn`（ES2022）而不是 `name in Color`——后者会命中原型链上的 `toString`、`constructor` 等属性，这是很典型的漏洞来源。用 `Symbol` 做成员的价值是身份唯一且不可伪造，代价是不能序列化、不能直接打印名字（`Symbol("unknown").toString()` 才给 `"Symbol(unknown)"`），所以协议字段别用 Symbol，内部状态机用起来很合适。⚠️ `Object.freeze` 是浅冻结，值为对象时要递归冻结。序列化直接 `JSON.stringify(Color)` 给 `{"RED":0,"GREEN":1}`，反序列化后就是普通对象，没有类型身份——这就是 TypeScript 的 `as const` 路线要补上的东西。

📘 [MDN · `Object.hasOwn()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 枚举的值通道分两种：纯枚举只有 `->name`，backed enum 有 `->name` 与 `->value`，并且**只有 backed enum** 才提供 `::from()`/`::tryFrom()` 按标量反查。遍历统一用 `::cases()`，没有任何"按序号"的 API。

```php
<?php
enum Suit {                          // 纯枚举：没有 value
    case Hearts;
    case Spades;
}

enum Status: string {                // backed enum：有 value 与 from/tryFrom
    case Ok = 'OK';
    case Fail = 'FAIL';
}

enum Code: int {                     // int 后备
    case NotFound = 404;
    case ServerError = 500;
}

echo Suit::Hearts->name;                        // Hearts
echo Status::Ok->value;                         // OK
echo Code::NotFound->value;                     // 404
echo Status::from('FAIL')->name;                // Fail
var_dump(Status::tryFrom('nope'));               // NULL（失败给 null）
print_r(array_map(fn($c) => $c->name, Suit::cases()));  // [Hearts, Spades]
print_r(array_map(fn($c) => $c->value, Status::cases())); // [OK, FAIL]
echo count(Suit::cases());                       // 2
echo Status::Ok === Status::from('OK') ? 'same' : 'diff'; // same（单例）
// 纯枚举按名字反查：只能自己写
$byName = array_column(Suit::cases(), null, 'name');
echo $byName['Spades']->name;                    // Spades
// 按整数拿成员：cases()[i]
echo Status::cases()[1]->name;                   // Fail
// from 失败是异常，tryFrom 是 null
try { Status::from('nope'); } catch (ValueError $e) { echo 'ValueError'; }  // ValueError
```

`::from()` 失败抛 `ValueError`，`::tryFrom()` 失败给 `null`——这是 PHP 里唯一成对出现的"抛异常/返回值"选择，处理外部输入一律用 `tryFrom`。纯枚举没有 `->value`（访问是致命错误），也没有 `::from()`/`::tryFrom()`（调用是 `Error`），所以需要标量反查就必须用 backed enum。⚠️ 枚举成员是单例，`===` 比较可靠（`==` 也一样），所以反查回来可以与常量做身份比较；`cases()` 返回声明顺序的数组，按序号拿成员就 `cases()[$i]`，这个序号没有专门的 API 名。序列化上 backed enum 默认 `json_encode` 输出 `value`（字符串或整数），纯枚举 `json_encode` 会抛错，必须实现 `JsonSerializable`；`serialize()`/`unserialize()` 对枚举按名字处理（`E:` 前缀的序列化格式），改名会让旧序列化数据失效。

📘 [PHP · Enumerations](https://www.php.net/manual/en/language.enumerations.backed.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有枚举，取值就是普通对象访问：`Symbol` 用 `==`/`equal?` 比较身份，常量用 `::` 取，名字用 `to_s`/`to_sym`。反查要么写 `match`/`index`，要么用 `Data` 的成员做字段查询；没有任何"序号"概念，需要序号就自己 `ALL.index(x)`。

```ruby
module Color
  RED = :red
  GREEN = :green
  BLUE = :blue
  ALL = [RED, GREEN, BLUE].freeze
  def self.valid?(sym) = ALL.include?(sym)          # 成员合法性检查
  def self.parse(str)
    sym = str.to_sym
    valid?(sym) ? sym : nil                          # 反查失败给 nil
  end
  def self.index_of(sym) = ALL.index(sym)            # 序号：0 起，失败给 nil
end

puts Color::RED, Color::RED.to_s, Color::RED.to_sym.inspect
puts Color.parse("green").inspect                     # :green
puts Color.parse("purple").inspect                    # nil
puts Color.valid?(:blue)                               # true
puts Color.index_of(:blue)                             # 2
puts Color::ALL.map(&:to_s).join(",")                  # red,green,blue
puts :red <=> :green                                   # 1（Symbol 按名字字典序比较）

# Symbol 内部化：同值同对象，比较是 O(1)
puts :red.equal?(:red)                                 # true
puts "red".to_sym.equal?(:red)                         # true（内部化）

# 按名字枚举：用常量列表而不是 Symbol 反射
Color.constants(false).sort.each { |c| puts c }        # ALL BLUE GREEN RED（常量名）
```

`Symbol` 的 `==`/`equal?` 可靠且快（内部化保证同值同对象）；`<=>` 按**名字字典序**比较（`:red <=> :green` 给 `1`，`:a <=> :b` 给 `-1`，只有与不同类型比较才给 `nil`），这跟成员声明顺序无关，所以按声明顺序排序仍必须借助 `ALL.index(x)`。⚠️ `Color.constants` 的**顺序不保证**（不同 Ruby 版本的常量表顺序不同），成员顺序必须靠显式的 `ALL` 数组维护，这也是 `index_of` 能工作的前提。反查失败用 `nil` 返回是 Ruby 惯例（对应 `Hash#[]`、`Array#index` 的行为），要抛错就自己 `raise ArgumentError`。`to_s`/`to_sym` 是 Symbol 与字符串互转的标准通道，序列化到 JSON 时 `:red.to_s` 给 `"red"`、读回来 `"red".to_sym`，注意 `to_sym` 对任意用户输入会创建动态符号（dynamic symbol）；现代 Ruby 的动态符号可被 GC，不再有永久性符号耗尽风险，但仍建议白名单校验。用 `Data.define` 做带数据的和类型时，取值是成员方法（`shape.kind`），没有序号也没有 raw value。

📘 [Ruby · Symbol](https://docs.ruby-lang.org/en/master/Symbol.html)

{{% /tab %}}

{{< /tabpane >}}

### 带数据的枚举与模式匹配

真正把枚举和普通常量区分开的能力是「每个分支可以携带不同的数据」。这一节看两件事：**语言有没有和类型（sum type）**，以及**解构时编译器能不能检查穷尽性**。Rust 的 `enum`、Swift 的关联值、Kotlin 的 `sealed`、Dart 的 `sealed`、TypeScript 的判别联合都能表达和类型，但只有一部分语言把穷尽性做成编译错误；Java 靠 record pattern 与 sealed 层次补上这一课，C#、Go、C、PHP 则只能靠继承、接口、标记联合或 tagged union 手工模拟。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `enum` 天生就是和类型：变体可以带匿名元组字段或具名结构体字段，字段类型互不相同，`match` 解构时编译器做**穷尽性检查**（漏一个变体是编译错误而不是警告）。所有变体共享同一个类型，因此函数签名里只需写 `Expr` 而不需要基类或接口。

```rust
#[derive(Debug)]
enum Shape {
    Circle { r: f64 },                         // 具名字段
    Rect(f64, f64),                            // 元组字段
    Point,                                     // 无载荷
}
#[derive(Debug)]
enum Expr {                                    // 递归和类型：必须用 Box 断开
    Num(i64),
    Add(Box<Expr>, Box<Expr>),
    Neg(Box<Expr>),
}
fn eval(e: &Expr) -> i64 {
    match e {                                   // 三个分支全部覆盖，编译器核对
        Expr::Num(n) => *n,
        Expr::Add(a, b) => eval(a) + eval(b),
        Expr::Neg(a) => -eval(a),
    }                                           // 漏一个变体会是 E0004 编译错误
}
fn area(s: &Shape) -> f64 {
    match s {
        Shape::Circle { r } => 3.14159 * r * r, // 字段解构
        Shape::Rect(w, h) => w * h,
        Shape::Point => 0.0,
    }
}
fn main() {
    println!("{}", eval(&Expr::Add(
        Box::new(Expr::Num(1)),
        Box::new(Expr::Neg(Box::new(Expr::Num(2)))))));   // -1
    println!("{}", area(&Shape::Rect(3.0, 4.0)));          // 12
    let s = Shape::Circle { r: 2.0 };
    if let Shape::Circle { r } = s {                       // 只关心一个变体
        println!("{r}");                                    // 2
    }
    let mut e = Expr::Num(5);
    match &mut e {                                          // 可变借用匹配
        Expr::Num(n) => *n += 1,
        _ => {}                                             // 其余用 _ 兜底
    }
    println!("{:?}", e);                                    // Num(6)
}
```

穷尽性检查是 Rust 枚举最值钱的地方：`match` 少写一个变体会直接编译失败（`non-exhaustive patterns`），加变体时所有匹配点都会报错，逼你同步更新代码。`if let`/`while let` 只匹配单个模式且**不做**穷尽性检查，适合"只关心一个变体"的场景，但要小心它静默忽略其他变体。⚠️ 递归变体必须装箱（`Box<Expr>`）否则类型大小无限；另一种做法是让子节点用 `Vec<Expr>` 或引用，都能打破递归。深度嵌套的模式还能配合守卫 `Expr::Num(n) if *n < 0 => ...`、`|` 多模式、`@` 绑定（`n @ 1..=9`），以及 `matches!` 宏做布尔判断。序列化时带字段的变体在 `serde` 里默认是外部标签（`{"Add":[{"Num":1},{"Num":2}]}`），也可以改成内部标签或相邻标签，跨语言协议最好显式指定。

📘 [Rust Reference · `match` expressions](https://doc.rust-lang.org/reference/expressions/match-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的关联值让枚举变成和类型：case 可以带任意类型、任意数量的载荷，`switch` 解构时编译器做穷尽性检查，`if case`/`guard case` 做单分支匹配。递归 case 要加 `indirect`。与 Rust 不同，Swift 的关联值型枚举没有 raw value，两者是互斥的设计。

```swift
enum Shape {
    case circle(radius: Double)                // 带标签的载荷
    case rect(width: Double, height: Double)
    case point
}
indirect enum Expr {                           // 递归枚举必须 indirect
    case num(Int)
    case add(Expr, Expr)
    case neg(Expr)
}
func area(_ s: Shape) -> Double {
    switch s {                                  // 穷尽：漏一个 case 是编译错误
    case .circle(let r): return 3.14159 * r * r
    case .rect(let w, let h): return w * h
    case .point: return 0
    }
}
func eval(_ e: Expr) -> Int {
    switch e {
    case .num(let n): return n
    case .add(let a, let b): return eval(a) + eval(b)
    case .neg(let a): return -eval(a)
    }
}
let s = Shape.rect(width: 3, height: 4)
print(area(s))                                  // 12.0
print(eval(.add(.num(1), .neg(.num(2)))))       // -1
if case .circle(let r) = s {                    // 只匹配一个 case
    print(r)
} else {
    print("not circle")                          // not circle
}
switch s {
case .rect(let w, let h) where w == h:           // where 守卫
    print("square \(w)")
case .rect: print("rect")                        // rect
default: print("other")
}
```

`switch` 对枚举的穷尽性是编译期强制的（`switch must be exhaustive` 会给出 fix-it 提示），加 case 时所有 `switch` 都会报错，这点和 Rust 一致。带标签的载荷（`radius:`、`width:`）让解构时可以按名字取：`case .rect(let w, let h)` 也可以写成 `case let .rect(width: w, height: h)`，标签还有 `case .rect(width: let w, height: let h)` 这种更精确的形式。⚠️ `if case`/`guard case` 与 `switch` 的区别是**不做穷尽性检查**，所以用它兜底时永远要写 `else` 分支处理意外变体；另外 `switch` 里一旦出现 `default`，新增 case 就不会再触发编译警告，所以能用穷尽枚举就别用 `default`。`indirect` 把递归 case 装箱（可写成 `indirect enum` 整体加，也可只给单个 case 加），代价是额外的堆分配。序列化上关联值型枚举的 `Codable` 合成结果是嵌套键（形如 `{"rect":{"width":3,"height":4}}`），跨语言协议通常要手写。

📘 [Swift · Associated Values](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/enumerations/#Associated-Values)

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有和类型**，也没有判别联合。表达"一个值可能是几种形状之一"只有三条路：接口加类型 switch、标记结构体加 `switch`、或者泛型约束（⚠️ 但类型集只能作约束，不能声明变量）。三者都没有编译器层面的穷尽性检查，`switch` 漏分支只在有 `default`/`panic` 时才在运行时暴露。

```go
package main

import "fmt"

type Shape interface{ isShape() }          // 路线一：接口 + 类型 switch
type Circle struct{ R float64 }
type Rect struct{ W, H float64 }
func (Circle) isShape() {}
func (Rect) isShape()   {}

func area(s Shape) float64 {
	switch v := s.(type) {                  // 类型 switch
	case Circle:
		return 3.14159 * v.R * v.R
	case Rect:
		return v.W * v.H
	default:
		panic(fmt.Sprintf("unhandled shape %T", s))   // 运行时兜底
	}
}

// 路线二：标记结构体（tagged struct），用零值区分，不需要接口
type Expr struct {
	Kind string   // "num" / "add" / "neg"
	Num  int
	L, R *Expr
}

// 路线三：泛型约束里的 union 类型集 —— ⚠️ 只能作约束，不能当类型用
type Number interface{ ~int | ~float64 }    // 类型集
func Sum[T Number](xs []T) T {              // 只能出现在类型参数约束位置
	var total T
	for _, x := range xs {
		total += x
	}
	return total
}
// var n Number                       // 🛑 编译错误：接口含类型项，不能声明变量
// var bad interface{ int | string }  // 🛑 同样不行

func main() {
	fmt.Println(area(Circle{2}), area(Rect{3, 4}))    // 12.56636 12
	fmt.Println(Sum([]int{1, 2, 3}))                   // 6
	e := Expr{Kind: "add", L: &Expr{Kind: "num", Num: 1}, R: &Expr{Kind: "num", Num: 2}}
	switch e.Kind {
	case "num":
		fmt.Println(e.Num)
	case "add":
		fmt.Println(e.L.Num + e.R.Num)                 // 3
	}
}
```

⚠️ 这是 Go 最容易搞错的一处：**含类型项（type term）的接口只能用作类型参数的约束**，不能作为变量的类型、不能作为返回值、不能用 `switch` 判别——`var n Number` 会得到 `cannot use type Number outside a type constraint` 之类的编译错误。所以「Go 的 union 类型」并不是其他语言的和类型，它只服务于泛型。接口 + 类型 switch 是 Go 里最接近和类型的写法，代价是：类型集合是开放的（任何包都能给 `Shape` 加实现），因此**没有穷尽性检查**，必须写 `default` 分支；`area` 里那个 `panic` 就是运行时兜底，忘写 `default` 的话未处理类型会静默返回零值 `0`，这是更糟的失败方式。标记结构体方案（`Kind` 字段 + 指针载荷）的好处是可比较、可序列化，坏处是字段常常是"部分有意义"的（`Num` 只在 `num` 时有效），非法组合可以在运行时构造出来。序列化时接口方案要自己处理类型标签（`json.Marshal` 只序列化具体类型），标记结构体方案则天然可序列化。

📘 [Go Spec · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations)

{{% /tab %}}

{{% tab header="Python" %}}

Python 3.10 起有结构化模式匹配（`match`/`case`），配合 `dataclass`、`Enum`、类模式可以表达和类型。⚠️ 关键限制是 `match` **没有编译期穷尽性检查**：漏分支不会报错，而且 `match` 是语句不是表达式，没有任何 case 匹配时整个语句被静默跳过（不抛异常），函数随即隐式返回 `None`——这比抛错更难查。

```python
from dataclasses import dataclass
from enum import Enum

class Kind(Enum):                     # 方式一：枚举 + 元组值携带数据
    CIRCLE = ("circle", 1)
    RECT = ("rect", 2)
    def __init__(self, tag, arity):
        self.tag = tag
        self.arity = arity

@dataclass(frozen=True)
class Circle:                         # 方式二：dataclass 做和类型的各变体
    r: float
@dataclass(frozen=True)
class Rect:
    w: float
    h: float
@dataclass(frozen=True)
class Point:
    pass

Shape = Circle | Rect | Point         # 3.10+ 联合类型做类型标注

def area(s: Shape) -> float:
    match s:                          # 结构化模式匹配（3.10+）
        case Circle(r=r):
            return 3.14159 * r * r
        case Rect(w=w, h=h):
            return w * h
        case Point():
            return 0.0
        case _:                        # ⚠️ 没有穷尽性检查，必须自己兜底
            raise TypeError(f"unknown shape: {s!r}")

print(area(Circle(2.0)), area(Rect(3.0, 4.0)))   # 12.56636 12.0
print(Kind.CIRCLE.tag, Kind.CIRCLE.arity)         # circle 1
print(Kind.CIRCLE.value)                          # ('circle', 1)

# 没有 _ 兜底时的行为：直接跳过 match，什么都不做
def silent(s):
    match s:
        case Circle(r=r):
            return r
    # 落到这里返回 None，不会报错
print(silent(Point()))                            # None
```

`match` 的匹配是按顺序尝试、第一个命中生效，所以**顺序有意义**：把 `case _` 放在前面会让后面的 case 全部失效。类模式（`case Circle(r=r)`）依赖 `__match_args__`，`@dataclass` 会自动生成，所以位置参数写法 `case Circle(r)` 也可用；`case Circle()` 只匹配类型不绑定字段。⚠️ 穷尽性问题在 Python 里没有任何编译期帮助：不加 `case _` 时，无法匹配的值会让整个 `match` 语句静默跳过（Python 的 `match` 是语句不是表达式，没有值可接），所以函数会隐式返回 `None`——这比抛异常难查得多，因此生产代码一定写 `case _: raise`。`Enum` 携带数据时用元组值 + `__init__` 解包的写法（如 `Kind.CIRCLE`）适合固定字段，而 `dataclass` + 联合类型适合不规则载荷。序列化上 `dataclass` 的 `asdict()` 给出嵌套字典，`Enum` 的 `value` 给元组，两者都要自己决定 wire format。

📘 [Python · `match` statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 用 `sealed class`/`sealed interface` 表达和类型：子类必须与密封类型在同一模块同一包，编译器因此知道全部子类，`when` 表达式（作为表达式使用时）**强制穷尽**，漏分支是编译错误。`enum class` 只能表达"每个分支数据相同"的情况（每个成员可以有自己的属性值，但形状一致），真正的和类型要靠 sealed 层次。

```kotlin
sealed interface Shape {                        // 密封层次 = 和类型
    data class Circle(val r: Double) : Shape
    data class Rect(val w: Double, val h: Double) : Shape
    data object Point : Shape                    // 无数据的单例分支
}
enum class Op(val symbol: String) {              // 枚举承载"每分支同形"的数据
    ADD("+"), SUB("-");
}

fun area(s: Shape): Double = when (s) {          // when 表达式：必须穷尽
    is Shape.Circle -> 3.14159 * s.r * s.r
    is Shape.Rect -> s.w * s.h
    Shape.Point -> 0.0                           // data object 用等值判断
}
fun apply(op: Op, a: Int, b: Int) = when (op) {  // 对 enum 的 when 也要穷尽
    Op.ADD -> a + b
    Op.SUB -> a - b
}

fun main() {
    println(area(Shape.Circle(2.0)))             // 12.56636
    println(area(Shape.Rect(3.0, 4.0)))          // 12.0
    println(apply(Op.ADD, 1, 2))                 // 3
    val s: Shape = Shape.Point
    if (s is Shape.Circle) println(s.r) else println("not circle")  // not circle
    when (s) {                                    // 作为语句：1.7 起 sealed 主题同样要求穷尽（这里用 else 兜底）
        is Shape.Point -> println("point")        // point
        else -> {}
    }
}
```

穷尽性检查在 `when` **表达式**上强制（结果被使用、或作为函数体返回时，漏分支是编译错误），Kotlin 1.7 起对 subject 是 `enum`、`sealed` 或 `Boolean` 的 `when` **语句**也报错而不是警告（1.6 只是警告），所以上面两种写法都安全。`is` 分支会智能转换（smart cast），在分支体内 `s` 自动变成 `Shape.Circle`，所以 `s.r` 直接可用；⚠️ Kotlin 的 `when` 只做智能转换、**不做解构绑定**，载荷字段必须在分支体里写成 `s.r`、`s.w`，这与 Rust/Swift 在模式里直接绑定字段是两种写法。`data object`（Kotlin 1.9 起）比 `object` 更适合做无数据分支，因为它自带 `toString`/`equals`。⚠️ sealed 的封闭性有边界：`sealed` 只约束**直接**子类的位置（Kotlin 1.5 起允许同一模块不同文件，但必须同包，此前必须同文件），间接子类可以在别处；`enum class` 完全封闭，并且只能实现接口、不能继承类。序列化上 `kotlinx.serialization` 对 sealed 层次用多态序列化，需要在基类加 `@Serializable` 并注册子类，JSON 里会带一个类型判别字段（默认 `"type"`）；`data object` 序列化只写判别字段。枚举成员带属性时 JSON 仍只写名字，属性不进 wire format。

📘 [Kotlin · Sealed classes and interfaces](https://kotlinlang.org/docs/sealed-classes.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 走的是「sealed 层次 + record pattern + switch 模式匹配」的组合路线：sealed interface 限定实现类，`record` 承载载荷，Java 21 起 `switch` 支持类型模式与 record 解构模式，对 sealed 层次做穷尽匹配时**不需要 `default`**（漏掉实现类是编译错误）。

```java
sealed interface Shape permits Circle, Rect, Point {}     // 密封层次
record Circle(double r) implements Shape {}
record Rect(double w, double h) implements Shape {}
record Point() implements Shape {}

public class Main {
    static double area(Shape s) {
        return switch (s) {                                // Java 21+ 模式匹配
            case Circle(double r) -> 3.14159 * r * r;      // record pattern 解构
            case Rect(double w, double h) -> w * h;
            case Point() -> 0.0;                           // 穷尽：无需 default
        };
    }
    static String describe(Shape s) {
        return switch (s) {
            case Circle(double r) when r > 5 -> "big circle";   // when 守卫
            case Circle(double r) -> "circle " + r;
            case Rect(double w, double h) -> "rect " + (w * h);
            case Point() -> "point";
        };
    }
    public static void main(String[] args) {
        System.out.println(area(new Circle(2)));            // 12.56636
        System.out.println(area(new Rect(3, 4)));            // 12.0
        System.out.println(describe(new Circle(9)));         // big circle
        Shape s = new Point();
        if (s instanceof Circle(double r)) {                 // instanceof 模式
            System.out.println(r);
        } else {
            System.out.println("not circle");                 // not circle
        }
        switch (s) {                                          // 语句形式的模式 switch 同样要求穷尽（这里靠 default 兜底）
            case Point() -> System.out.println("point");      // point
            default -> { }
        }
        record Pair<T>(T a, T b) {}                           // 嵌套 record pattern
        Object o = new Pair<>(new Circle(1), new Rect(2, 3));
        if (o instanceof Pair(Circle(double r), Rect(double w, double h))) {
            System.out.println(r + w + h);                     // 6.0
        }
    }
}
```

这套组合的关键是**密封 + record + switch 三者配合**：`sealed interface` 让编译器知道全部实现类（JEP 409，Java 17 正式），`record pattern`（JEP 440）把载荷直接解构成局部变量，`switch` 的模式匹配（JEP 441）对密封层次做穷尽检查——漏一个实现类是编译错误而不是警告，两者都在 Java 21 正式发布（此前的 JEP 405/432、406/420/427/433 都是预览）。⚠️ 穷尽性要求对**使用了模式标签或 `null` 标签的 `switch` 语句同样成立**：把一个漏掉实现类的模式 `switch` 写成语句也照样编译失败（Oracle 官方文档的 `notExhaustive(Pair<A> p)` 示例就是语句形式，报 "the switch statement does not cover all possible input values"）；只有不含模式标签的传统常量 `switch`（`int`、`String`、`enum`）才不要求穷尽，所以不能靠"写成语句"绕开检查。`case null` 从 Java 21 起也正式支持（可写 `case null` 或 `case null, default`），不处理时 null 会抛 `NullPointerException`。`when` 守卫允许在 case 标签里加布尔条件，但守卫不参与穷尽性判定，所以带守卫的 case 之后仍要有能覆盖全类型的分支。序列化上 record 与 sealed 层次没有内建 JSON 支持，Jackson 需要注册多态类型（`@JsonTypeInfo`）或自定义序列化器。Java 26 没有改动这套枚举与模式匹配机制，唯一相关的新内容是仍处预览的 JEP 530（primitive types in patterns）。

📘 [JLS · Pattern matching for switch](https://docs.oracle.com/javase/specs/jls/se26/html/jls-14.html#jls-14.30)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 没有语言级的和类型，标准库的 `std::variant`（C++17）是最接近的替代：它保存"若干类型之一"并记录当前是哪一个。访问用 `std::visit` 加泛型 lambda，`index()` 拿当前分支下标，`std::get` 按类型或下标取值，`std::get_if` 给指针。没有穷尽性检查——`visit` 重载集漏了类型会编译失败，但这是重载决议的副作用而不是语言特性。

```cpp
#include <cstdio>
#include <string>
#include <type_traits>
#include <variant>

struct Circle { double r; };
struct Rect { double w, h; };
struct Point {};
using Shape = std::variant<Circle, Rect, Point>;      // 和类型的替代品

double area(const Shape& s) {
    return std::visit([](auto&& v) -> double {         // 泛型 lambda 访问
        using T = std::decay_t<decltype(v)>;
        if constexpr (std::is_same_v<T, Circle>) return 3.14159 * v.r * v.r;
        else if constexpr (std::is_same_v<T, Rect>) return v.w * v.h;
        else return 0.0;                               // 兜底：不是穷尽检查
    }, s);
}
// 重载集写法：漏掉某个类型时编译失败（重载决议找不到匹配）
struct AreaVisitor {
    double operator()(const Circle& c) const { return 3.14159 * c.r * c.r; }
    double operator()(const Rect& r) const { return r.w * r.h; }
    double operator()(const Point&) const { return 0.0; }
};

int main() {
    Shape a = Circle{2.0};
    printf("%g %g\n", area(a), area(Rect{3, 4}));      // 12.5664 12
    printf("%zu %g\n", a.index(), std::visit(AreaVisitor{}, a));  // 0 12.5664
    printf("%g\n", std::get<Circle>(a).r);              // 2（按类型取值）
    printf("%g\n", std::get<0>(a).r);                   // 2（按下标取值）
    if (auto* p = std::get_if<Rect>(&a)) {              // get_if：不抛异常
        printf("%g\n", p->w);
    } else {
        printf("not rect\n");                            // not rect
    }
    try {
        std::get<Rect>(a);                               // 类型不匹配
    } catch (const std::bad_variant_access&) {
        printf("bad_variant_access\n");                  // bad_variant_access
    }
    Shape p = Point{};
    printf("%zu\n", p.index());                          // 2（按声明顺序）
    printf("%zu\n", sizeof(Shape));                      // 24（最大成员 + tag + 对齐）
}
```

`std::variant` 用 `index()` 记录分支（0 起，按模板参数顺序），`std::get<T>` 类型不符时抛 `std::bad_variant_access`，`std::get_if<T>` 返回 `nullptr` 而不抛——处理不可信数据要用后者。⚠️ 用 `if constexpr` 写 `visit` 时最后的 `else` 分支是**运行时兜底**而不是编译期保证：把 `Point` 分支删掉代码照样编译，只是返回 0.0；想拿到"漏类型就编译失败"的效果，要么用重载集 `AreaVisitor`（重载决议会报错），要么用 C++20 的 `std::visit` + `std::overloaded`。`std::variant` 可能是 valueless_by_exception 状态（构造过程中抛异常），正常情况下不会出现，但要写健壮代码就得考虑 `valueless_by_exception()`。`sizeof(Shape)` 是 24：variant 不省空间，它约为最大成员加上判别标记与对齐。序列化需要自己写 visitor 或引库（`std::variant` 没有任何内建序列化支持）。

📘 [cppreference · `std::variant`](https://en.cppreference.com/w/cpp/utility/variant)

{{% /tab %}}

{{% tab header="C" %}}

C 里的和类型是**手工构造的标记联合（tagged union）**：一个 `enum` 当标签、一个 `union` 装各分支载荷、一个 `struct` 把两者绑在一起。标签与联合的同步完全靠程序员自觉，`switch` 也没有穷尽性检查（`-Wswitch` 只在不写 `default` 时给出未处理枚举值的警告）。

```c
#include <stdio.h>
#include <string.h>

typedef struct Shape Shape;

enum ShapeTag { SHAPE_CIRCLE, SHAPE_RECT, SHAPE_POINT };   /* 判别标签 */

struct Shape {
    enum ShapeTag tag;                     /* 标签必须放在最前，便于比较 */
    union {                                /* 各分支载荷共享内存 */
        struct { double r; } circle;
        struct { double w, h; } rect;
    } as;                                  /* POINT 分支没有载荷 */
};

double area(const Shape *s) {
    switch (s->tag) {                       /* 按标签分派 */
        case SHAPE_CIRCLE: return 3.14159 * s->as.circle.r * s->as.circle.r;
        case SHAPE_RECT:   return s->as.rect.w * s->as.rect.h;
        case SHAPE_POINT:  return 0.0;
    }
    return -1.0;                            /* 兜底：编译器才会停止警告 */
}

int main(void) {
    Shape a = { .tag = SHAPE_CIRCLE, .as.circle = { .r = 2.0 } };   /* 指定初始化器 */
    Shape b = { .tag = SHAPE_RECT,   .as.rect   = { .w = 3.0, .h = 4.0 } };
    Shape c = { .tag = SHAPE_POINT };
    printf("%g %g %g\n", area(&a), area(&b), area(&c));   /* 12.5664 12 0 */
    printf("%zu\n", sizeof(Shape));                        /* 24（union 是最大分支） */
    /* ⚠️ 读错分支：编译能过，值是垃圾 */
    printf("%g\n", b.as.circle.r);                         /* 未定义值，别这么写 */
    /* 字符串化标签：没有内建支持，自己写 */
    const char *tags[] = { "circle", "rect", "point" };
    printf("%s\n", tags[b.tag]);                           /* rect */
    /* 用 memset 归零后只设 tag，载荷为 0 */
    Shape z;
    memset(&z, 0, sizeof z);
    z.tag = SHAPE_RECT;
    printf("%g\n", area(&z));                              /* 0 */
    char buf[32];
    snprintf(buf, sizeof buf, "%s", tags[c.tag]);
    printf("%s %zu\n", buf, strlen(buf));                   /* point 5 */
    return 0;
}
```

这个模式有三个必须自己守住的纪律：第一，**写的时候 tag 与 union 必须同时设对**，读的时候必须先用 `switch (s->tag)` 分派再访问 `s->as.xxx`，读错分支在 C 里是合法的（读到别的分支的位模式），值毫无意义；第二，`switch` 要有兜底 return 或 `default`，否则编译器报"控制到达非 void 函数末尾"，而一旦写了 `default`，将来加标签就不会再收到 `-Wswitch` 警告；第三，`union` 的内存是各分支共享的，`sizeof(Shape)` 由最大分支决定（这里是 24），所以给 `circle` 赋值会覆盖 `rect` 的字节。⚠️ 标签用 `enum` 而不用 `int` 是为了可读性，但 C 的 `enum` 与整数自由互转，所以非法标签值仍可能从外部数据进来，解析入口要校验。序列化要自己写编码（通常先写 tag 数字再按分支写载荷），跨平台还要固定字节序与整型宽度（用 `uint32_t` 而不是 `enum`）。C23 的 `enum : type` 可以让标签宽度确定。

📘 [cppreference · struct 与 union](https://en.cppreference.com/w/c/language/union)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用「抽象类型 + 结构体 + 多分派」表达和类型，而不是一个 `enum` 关键字：`abstract type Shape end` 定义封闭性的概念层级，具体 `struct` 继承它，函数用多分派自动分派到对应方法。⚠️ 与 sealed 不同，Julia 的抽象类型**不封闭**——任何模块都能加新子类型，所以没有穷尽性检查，`Union{Circle, Rect}` 才是显式列举的联合类型。

```julia
abstract type Shape end                    # 抽象类型：概念层级
struct Circle <: Shape; r::Float64; end
struct Rect   <: Shape; w::Float64; h::Float64; end
struct Point  <: Shape end

area(c::Circle) = 3.14159 * c.r^2          # 多分派：每个具体类型一个方法
area(r::Rect)   = r.w * r.h
area(::Point)   = 0.0

area2(s::Union{Circle,Rect,Point}) = area(s)   # 联合类型做类型标注

# 用 @enum 做"纯标签 + 外部数据表"的替代方案
@enum Kind CIRCLE RECT POINT
shape_of(k::Kind, dims::Vector{Float64}) = begin
    k === CIRCLE ? Circle(dims[1]) :
    k === RECT   ? Rect(dims[1], dims[2]) : Point()
end

println(area(Circle(2.0)), " ", area(Rect(3.0, 4.0)), " ", area(Point()))  # 12.56636 12.0 0.0
println(area2(Rect(3.0, 4.0)))                 # 12.0
println(shape_of(RECT, [3.0, 4.0]) |> area)     # 12.0

# 判别与解构：isa 与字段访问
s = Circle(2.0)
println(s isa Shape, s isa Circle)              # true true
if s isa Circle
    println(s.r)                                # 2.0
end

# 遍历一个类型的所有具体子类型（需要显式维护，没有反射穷尽）
const SHAPE_TYPES = (Circle, Rect, Point)
for T in SHAPE_TYPES
    inst = T === Point ? Point() : T === Circle ? Circle(1.0) : Rect(1.0, 1.0)
    println(T, " -> ", area(inst))
end
```

Julia 的分派是按参数的**运行时类型**选方法，编译器会做类型推断并在类型不稳定时插入动态分派，所以 `area(s::Shape)` 这种写法本身没有方法（抽象类型不能实例化，也没有为它定义 `area`），必须先定义 `area(s::Shape) = error("unknown shape")` 之类的兜底或者用 `Union` 标注。⚠️ 抽象类型不封闭意味着"漏掉一个子类型"在 Julia 里既不会编译报错也不会运行时自动报错，只会走 `MethodError`（如果没有兜底方法）或者走兜底方法的错误分支——所以和类型的穷尽性只能靠 `Union{...}` 显式列举加上测试。`@enum` 的标签适合做"种类"维度，数据放字段里（如 `shape_of` 演示）等价于把 tag 与载荷分开存，这与 C 的标记联合思路一致。序列化上 `StructTypes.jl`/`JSON3` 会按字段名输出（`{"r":2.0}`），类型判别字段要自己加，`@enum` 则输出数字。

📘 [Julia · Types](https://docs.julialang.org/en/v1/manual/types/)

{{% /tab %}}

{{% tab header="C#" %}}

C# **没有判别联合（discriminated union）**，也没有 `sealed` 那样的穷尽性强制。惯用替代是「抽象基类或接口 + record 子类型 + `switch` 表达式模式匹配」，穷尽性只由编译器分析器给警告（`CS8509`），漏分支不会编译失败。`OneOf` 这类第三方库提供泛型联合类型，但类型集合无法封闭。

```csharp
using System;

abstract record Shape;                                  // 抽象 record 做基类型
record Circle(double R) : Shape;                        // 位置 record：载荷即参数
record Rect(double W, double H) : Shape;
record Point : Shape;                                   // 无载荷分支

class Program {
    static double Area(Shape s) => s switch {            // switch 表达式 + 模式
        Circle { R: var r } => 3.14159 * r * r,           // 属性模式
        Rect(var w, var h) => w * h,                      // 位置模式
        Point => 0.0,
        _ => throw new ArgumentException($"unknown {s}")  // ⚠️ 必须写，否则 CS8509 警告
    };
    static string Describe(Shape s) => s switch {
        Circle c when c.R > 5 => "big circle",            // when 守卫
        Circle c => $"circle {c.R}",
        Rect => "rect",
        _ => "other"
    };
    static void Main() {
        Console.WriteLine(Area(new Circle(2)));           // 12.56636
        Console.WriteLine(Area(new Rect(3, 4)));          // 12
        Console.WriteLine(Describe(new Circle(9)));       // big circle
        Shape s = new Point();
        if (s is Circle { R: var rr }) Console.WriteLine(rr);
        else Console.WriteLine("not circle");              // not circle
        Console.WriteLine(s is Point ? "point" : "?");     // point
        // 记录的相等性与解构
        var c = new Circle(2);
        Console.WriteLine(c == new Circle(2));             // True（record 值相等）
        var (x, y) = (new Rect(3, 4)) switch {             // 解构到元组
            Rect(w, h) => (w, h),
            _ => (0.0, 0.0)
        };
        Console.WriteLine(x + y);                          // 7
    }
}
```

`switch` 表达式配合位置 record 模式（`Rect(var w, var h)`）与属性模式（`Circle { R: var r }`）让解构很简洁，`record` 还自带基于成员的值相等、`ToString` 与 `Deconstruct`，所以它比 class 层次更适合做和类型的变体。⚠️ 关键限制：C# 14 / .NET 10 里 `switch` 表达式**没有编译期穷尽性强制**——即使基类型是 `abstract record`，漏掉 `Point` 也只给 `CS8509`（"switch expression does not handle all possible values"）警告，代码照样跑，运行时落到 `_` 或抛 `SwitchExpressionException`；要把它升级为错误得在项目里开 `TreatWarningsAsErrors` 或 `<WarningsAsErrors>CS8509</WarningsAsErrors>`。另一个限制是 C# 的继承层次永远开放（除非 `sealed`），第三方程序集可以加子类，所以分析器也只能保守地给警告。社区库 `OneOf<T0, T1>` 提供泛型联合类型，代价是要写 `OneOf` 的泛型参数列表与 `Match` 调用，且不能携带自定义继承层次。前瞻一下：C# 15 已在公开预览中引入 `union` 类型（`public union Pet(Cat, Dog, Bird);`）与 `closed` 层次，官方说明里明确"编译器会保证 `switch` 表达式对所有 case 类型穷尽"，运行时的 `UnionAttribute`/`IUnion` 从 .NET 11 Preview 5 起提供；但它不在 C# 14 / .NET 10 基线上，本文按基线书写。序列化上 `System.Text.Json` 对多态层次需要 `[JsonDerivedType]` 标注（.NET 7 起）或自定义 converter，否则子类成员会丢失。

📘 [MS Learn · Pattern matching](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/functional/pattern-matching)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 3.0 起有 `sealed` 类修饰符 + 模式匹配 + `switch` 表达式，三者配合能得到编译期穷尽性检查：`sealed` 限制子类型必须与父类同库，编译器因此知道全部子类型，`switch` 作为表达式时对 sealed 层次强制穷尽。

```dart
sealed class Shape {}                      // sealed（Dart 3.0）：子类必须同库
final class Circle extends Shape {          // final：禁止在库外继承
  Circle(this.r);
  final double r;
}
final class Rect extends Shape {
  Rect(this.w, this.h);
  final double w, h;
}
final class Point extends Shape {}

double area(Shape s) => switch (s) {        // switch 表达式：必须穷尽
  Circle(r: var r) => 3.14159 * r * r,      // 对象模式 + 字段解构
  Rect(w: var w, h: var h) => w * h,
  Point() => 0.0,                            // 没有 default：靠 sealed 穷尽
};

String describe(Shape s) => switch (s) {
  Circle(r: var r) when r > 5 => 'big circle',   // when 守卫
  Circle() => 'circle',
  Rect() => 'rect',
  Point() => 'point',
};

void main() {
  print(area(Circle(2)));                  // 12.56636
  print(area(Rect(3, 4)));                 // 12.0
  print(describe(Circle(9)));              // big circle
  final Shape s = Point();
  if (s case Circle(r: var r)) {            // if-case 模式匹配
    print(r);
  } else {
    print('not circle');                     // not circle
  }
  switch (s) {                               // 语句形式：sealed 下同样必须穷尽
    case Circle():
      print('circle');
    case Rect():
      print('rect');
    case Point():
      print('point');                        // point
  }
  final list = [Circle(1), Rect(2, 3), Point()];
  final areas = [for (final x in list) area(x)];   // 集合 for + 模式
  print(areas);                              // [3.14159, 6.0, 0.0]
}
```

`sealed` 的语义是「子类型必须与它声明在同一个 library」，因此编译器掌握封闭集合：`switch` 表达式漏一个子类型是**编译错误**，语句形式的 `switch` 在 sealed 层次上同样要求穷尽（Kotlin 1.7 起对 `sealed`、`enum`、`Boolean` 主题的 `when` 语句也已从警告升级为编译错误）。类修饰符要配套用：`sealed` 允许继承但不能在库外继承，`final` 连库内继承也禁止，`base`/`interface` 各有用途，把它们写全能让 API 的封闭性更明确。⚠️ `sealed` 的穷尽性只对**直接**子类型有效：如果某个直接子类型不是 `final`/`sealed`，它的子类型可以无限扩展，编译器就不会认为 switch 已穷尽，所以和类型的分支通常都标 `final`。模式匹配还支持记录模式（`(var x, var y)`）、列表模式（`[var a, ...]`）与逻辑模式（`||`/`&&`），`if-case` 不做穷尽检查所以必须写 `else`。序列化上 Dart 没有内建多态 JSON，判别字段（Dart 里常叫 `type`）要自己在 `toJson`/`fromJson` 里写，`json_serializable` 对 sealed 层次需要 `@JsonKey` 或自定义 converter。

📘 [Dart · Pattern matching](https://dart.dev/language/patterns)

{{% /tab %}}

{{% tab header="R" %}}

R **没有和类型**，也没有模式匹配的等价物。表达"一个值可能是几种形状之一"要靠 `list` 加 `class` 属性（S3 对象系统）再配合 `switch`/`if`，或者用列表的"判别字段 + 载荷"结构手工模拟。`switch()` 只按一个标量分派，没有穷尽性检查。

```r
shape_area <- function(s) {
  switch(s$kind,                                  # 按判别字段分派
    circle = pi * s$r^2,
    rect   = s$w * s$h,
    point  = 0,
    stop("unknown shape: ", s$kind)                # 兜底：自己抛错
  )
}
circle <- function(r) structure(list(kind = "circle", r = r), class = "shape")
rect   <- function(w, h) structure(list(kind = "rect", w = w, h = h), class = "shape")
point  <- function() structure(list(kind = "point"), class = "shape")

print(shape_area(circle(2)))          # [1] 12.56637
print(shape_area(rect(3, 4)))         # [1] 12
print(shape_area(point()))            # [1] 0
# 用 class 属性做"类型判别"，再配 print/format 方法
print.shape <- function(x, ...) cat("shape:", x$kind, "\n")
print(circle(2))                       # shape: circle
# 尝试未知分支
tryCatch(shape_area(list(kind = "blob")),
         error = function(e) cat("Error:", conditionMessage(e), "\n"))  # Error: unknown shape: blob
# 列表没有封闭性：字段随便加，缺字段不报错
bad <- list(kind = "rect", w = 3)      # 少了 h
print(shape_area(bad))                  # numeric(0)：s$h 给 NULL，w * NULL 静默变成长度 0 的向量
```

`switch()` 按名字匹配第一个参数的值，命中第一个匹配的分支；给一个不存在的名字且没有默认分支时返回 `NULL`（不报错），所以上面的 `stop(...)` 是必须的兜底。⚠️ S3 的 `class` 属性只是字符串向量，任何对象都能被赋上任意 class，所以"类型判别"完全靠约定：写错 `kind` 字符串会在 `stop(...)` 兜底处报错，但**缺字段不会报错**——`s$h` 给 `NULL`，`w * NULL` 静默得到 `numeric(0)`，一路传播到下游才暴露，比抛错更难查。`list` 是引用语义的向量，字段可以随意增删（`s$extra <- 1` 合法），因此没有任何封闭性保证。更严格的方案是用 `vctrs`（`new_vctr`、`new_rcrd`，带类型检查与 `vec_ptype_abbr`）或者 R6/Reference Class 的正式类系统。`switch` 只接受一个标量判别值，真正的多路分派可以用 `UseMethod`（S3 泛型）：`area <- function(s) UseMethod("area")`，然后为每个 class 定义 `area.circle`、`area.rect`；这比手写 `switch` 更成体系，但 `UseMethod` 只按第一个参数分派、本质仍是单分派（要按多个参数联合分派必须上 S4 的 `setGeneric`/`setMethod`），而且同样没有穷尽性检查，未定义的方法会抛 `no applicable method`。

📘 [R · `switch`](https://stat.ethz.ch/R-manual/R-devel/library/base/html/switch.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的标记联合 `union(enum)` 就是带数据的枚举：变体各有自己的载荷类型，`switch` 解构时用 `|v|` 捕获载荷，**对穷尽枚举强制穷尽**（漏一个变体是编译错误），访问错误的字段在安全构建里是受检的非法行为。这是 Zig 里唯一真正封闭的和类型机制。

```zig
const std = @import("std");

const Shape = union(enum) {                 // 标记联合：tag 自动生成
    circle: f64,
    rect: struct { w: f64, h: f64 },
    point,
};

fn area(s: Shape) f64 {
    return switch (s) {                      // 穷尽：漏一个变体是编译错误
        .circle => |r| 3.14159 * r * r,       // |r| 捕获 payload
        .rect => |v| v.w * v.h,
        .point => 0.0,
    };
}

const Expr = union(enum) {                   // 递归：载荷用指针断开
    num: i64,
    add: struct { l: *const Expr, r: *const Expr },
};

fn eval(e: *const Expr) i64 {
    return switch (e.*) {
        .num => |n| n,
        .add => |v| eval(v.l) + eval(v.r),
    };
}

pub fn main() void {
    std.debug.print("{d} {d} {d}\n", .{ area(.{ .circle = 2 }), area(.{ .rect = .{ .w = 3, .h = 4 } }), area(.point) });
    // 12.56636 12 0
    const leaf = Expr{ .num = 1 };
    const leaf2 = Expr{ .num = 2 };
    const sum = Expr{ .add = .{ .l = &leaf, .r = &leaf2 } };
    std.debug.print("{d}\n", .{eval(&sum)});            // 3
    std.debug.print("{s}\n", .{@tagName(sum)});          // add（自动生成的 tag）
    // 非穷尽标记联合：需要 else 分支
    const Maybe = union(enum(u8)) { some: u8, none, _ };
    const m = Maybe{ .some = 7 };
    const label = switch (m) {
        .some => |v| if (v > 3) "big" else "small",
        .none => "none",
        else => "other",                                 // 非穷尽必须写 else
    };
    std.debug.print("{s}\n", .{label});                   // big
    // 用 std.meta.Tag 拿 tag 类型
    std.debug.print("{s}\n", .{@typeName(std.meta.Tag(Shape))});  // @typeInfo(...).@"enum"
}
```

穷尽性检查是标记联合最大的价值：对 `union(enum)` 的 `switch` 少写一个变体直接编译失败（`switch on union with no else prong`），加变体时所有 `switch` 都会报错；一旦联合是非穷尽的（末尾写 `_`），编译器就要求 `else`，检查随之失效。⚠️ 运行时安全：对标记联合访问"非当前变体"的字段在 Debug/ReleaseSafe 下是**受检的非法行为**（panic 并打印访问了哪个字段），在 ReleaseFast/ReleaseSmall 下是未定义行为，所以不要用 `s.rect` 这种直接访问，统一用 `switch` 解构或 `s == .rect` 判断。载荷捕获支持 `|v|`（整个载荷）、`|*v|`（指针，便于原地修改）、`|v| if (v > 3)`（带条件），也能用 `.rect => |v| ...` 直接命名。`std.meta.Tag(Shape)` 给自动生成的标签枚举类型，用于把 tag 单独存起来做协议字段。序列化上 `std.json` 会按变体名输出成外部标签（`{"circle":2}`），反向解析用 `std.json.parseFromSlice(Shape, ...)` 即可自动分派。

📘 [Zig Language Reference · Tagged union](https://ziglang.org/documentation/master/#Tagged-union)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有和类型**，惯用做法是「table 加 `tag` 字段」：一个普通 table 带 `tag`（或 `kind`）判别字段，载荷直接放在同一张表里，用 `if`/`elseif` 或分派表解构。没有任何封闭性与穷尽性检查，写错字段名只会得到 `nil`。

```lua
-- 用 tag 字段构造和类型
local function circle(r) return { tag = "circle", r = r } end
local function rect(w, h) return { tag = "rect", w = w, h = h } end
local point = { tag = "point" }

-- 分派表写法：tag -> 处理函数
local handlers = {
  circle = function(s) return 3.14159 * s.r * s.r end,
  rect   = function(s) return s.w * s.h end,
  point  = function() return 0 end,
}
local function area(s)
  local h = handlers[s.tag]
  if not h then error("unknown shape tag: " .. tostring(s.tag), 2) end  -- 必须兜底
  return h(s)
end

print(area(circle(2)), area(rect(3, 4)), area(point))   -- 12.56636 12 0

-- if/elseif 写法：可以做载荷校验
local function area2(s)
  if s.tag == "circle" then
    return 3.14159 * s.r * s.r
  elseif s.tag == "rect" then
    return s.w * s.h
  elseif s.tag == "point" then
    return 0
  else
    error("unknown shape: " .. tostring(s.tag), 2)        -- 兜底
  end
end
print(area2(circle(2)))                                   -- 12.56636

-- 嵌套和类型：载荷本身也是 tagged table
local function add(l, r) return { tag = "add", l = l, r = r } end
local function num(n) return { tag = "num", n = n } end
local function eval(e)
  if e.tag == "num" then return e.n
  elseif e.tag == "add" then return eval(e.l) + eval(e.r)
  else error("unknown expr: " .. tostring(e.tag), 2) end
end
print(eval(add(num(1), num(2))))                          -- 3

-- 缺字段的后果：静默 nil
print(rect(3, 4).h, rect(3, 4).z)                          -- 4 nil
local ok, err = pcall(area, { tag = "rect", w = 3 })       -- 缺 h：调用时抛错
print(ok, err)                                             -- false  attempt to perform arithmetic on a nil value (field 'h')
```

分派表写法的优点是分派 O(1) 且容易做插拔（把 `handlers.rect` 换成别的实现即可），缺点是漏写 tag 时只能在运行时靠 `if not h then error(...)` 兜住；`if/elseif` 写法便于在解构处顺带校验字段（比如检查 `type(s.r) == "number"`）。⚠️ Lua 的 table 是引用语义、完全开放：任何代码都能给 `s` 加字段、改 `tag`，甚至把 `tag` 设成 `nil`，所以"判别联合"的不变量只能靠构造函数（`circle`/`rect`）与入口校验维持，绝不能信任外部传入的 table 已经符合形状。多个和类型混用时，tag 字符串要加前缀（`"expr.add"`）避免撞名。序列化上 table 天然可以转 JSON（需要 `cjson`/`dkjson`），tag 字段就充当类型判别键，这也是 Lua 协议里最常见的形式。

📘 [Lua 5.5 · Metatables and metamethods](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有 `sealed` 关键字，和类型靠**判别联合（discriminated union）**表达：几个对象类型共享一个字面量类型的判别属性，`switch` 收窄后每个分支拿到具体类型，漏分支用 `never` 兜底检查（把剩余值赋给 `never` 变量，新增成员会报编译错误）。这套机制是纯类型层的，运行时什么也不做。

```typescript
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "rect"; w: number; h: number }
  | { kind: "point" };

function area(s: Shape): number {
  switch (s.kind) {                            // 按字面量判别属性收窄
    case "circle": return 3.14159 * s.r * s.r; // s 收窄为 circle 分支
    case "rect": return s.w * s.h;
    case "point": return 0;
    default: {
      const _exhaustive: never = s;            // 穷尽检查：漏分支报 TS2322
      return _exhaustive;
    }
  }
}
// 更简练的穷尽写法：不用 default，靠返回类型与 never 检查
function describe(s: Shape): string {
  switch (s.kind) {
    case "circle": return `circle ${s.r}`;
    case "rect": return `rect ${s.w}x${s.h}`;
    case "point": return "point";
    default: return assertNever(s);
  }
}
function assertNever(x: never): never { throw new Error(`unexpected: ${JSON.stringify(x)}`); }

const s: Shape = { kind: "rect", w: 3, h: 4 };
console.log(area(s), describe({ kind: "circle", r: 2 }));  // 12 circle 2
// 类型收窄也会发生在 if/三元里
if (s.kind === "rect") console.log(s.w * s.h);              // 12
// 结构化模式匹配（对象字面量类型）也能解构 JSON
const parsed = JSON.parse('{"kind":"point"}') as Shape;
console.log(area(parsed));                                  // 0
// satisfies 校验字面量而不拓宽类型（TS 4.9+）
const conf = { kind: "circle", r: 1 } satisfies Shape;
console.log(area(conf));                                     // 3.14159
```

判别属性的类型必须是**字面量类型**（`"circle"` 而不是 `string`），否则 TS 无法收窄；判别属性名通常叫 `kind`/`type`/`tag`，但没有语言强制。穷尽检查的两种写法里，`const _exhaustive: never = s` 最直接：所有分支都处理完后 `s` 的类型被收窄成 `never`，一旦新增联合成员，赋值立刻报 `TS2322: Type '...' is not assignable to type 'never'`；`assertNever` 版本把同样的检查装进函数，运行时有异常兜底。⚠️ 这套检查是编译期的，运行时 `JSON.parse` 出来的对象没有任何验证——`as Shape` 只是断言，非法数据照样能进去，所以外部输入要用 `zod`/`valibot` 之类的 schema 校验器做真正的运行时验证。序列化上判别联合天然映射到"带 `kind` 字段的 JSON"，这也是它比 `enum` 更适合 wire format 的原因：加分支时判别字段不变、旧数据仍可读，而数值枚举会随顺序漂移。

📘 [TS Handbook · Discriminated unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有和类型**，也没有模式匹配。惯用做法跟 Lua 类似：普通对象带 `tag`/`type` 判别字段，用 `switch (obj.type)` 解构；要保证分支穷尽只能靠 `default: throw`（或 TypeScript 的 `never`）。`instanceof` 也行，但只适用于类层次，且无法跨 realm 可靠判断。

```javascript
// 判别字段 + switch
const circle = (r) => ({ type: "circle", r });
const rect = (w, h) => ({ type: "rect", w, h });
const point = Object.freeze({ type: "point" });

function area(s) {
  switch (s.type) {
    case "circle": return 3.14159 * s.r * s.r;
    case "rect": return s.w * s.h;
    case "point": return 0;
    default: throw new Error(`unknown shape: ${JSON.stringify(s)}`);  // 穷尽靠它
  }
}
console.log(area(circle(2)), area(rect(3, 4)), area(point));  // 12.56636 12 0

// 分派表：tag -> 函数，便于扩展与测试
const handlers = {
  circle: (s) => 3.14159 * s.r * s.r,
  rect: (s) => s.w * s.h,
  point: () => 0,
};
const area2 = (s) => {
  const h = Object.hasOwn(handlers, s.type) ? handlers[s.type] : null;
  if (!h) throw new Error(`unknown shape: ${s.type}`);
  return h(s);
};
console.log(area2(rect(3, 4)));                                // 12

// 类层次 + instanceof（另一种思路）
class Shape { area() { throw new Error("abstract"); } }
class Circle extends Shape { constructor(r) { super(); this.r = r; } area() { return 3.14159 * this.r ** 2; } }
class Rect extends Shape { constructor(w, h) { super(); this.w = w; this.h = h; } area() { return this.w * this.h; } }
console.log(new Circle(2).area(), new Rect(3, 4).area());       // 12.56636 12
console.log(new Rect(3, 4) instanceof Shape);                   // true

// 解构取值（没有模式匹配，只有对象解构）
const { w, h } = rect(3, 4);
console.log(w * h);                                             // 12
try { area({ type: "blob" }); } catch (e) { console.log(e.message); }
// unknown shape: {"type":"blob"}
```

`switch` 用 `===` 比较字符串，所以判别字段写错大小写会直接落到 `default`；`default: throw` 是唯一的穷尽保障，忘写就会静默返回 `undefined`（进而污染下游）。分派表版本要用 `Object.hasOwn` 而不是 `in`，否则 `{ type: "toString" }` 会命中原型链上的方法。⚠️ 类层次的 `instanceof` 有跨 realm（iframe、worker、`vm` 模块）失效的问题，判别字段方案没有这个问题，所以跨边界的数据结构优先用判别字段。对象字面量是引用类型且完全开放，任何代码都能给结果加字段或改 `type`；要防意外修改就在构造时 `Object.freeze`（浅冻结）。序列化天然是带判别字段的 JSON，与 TypeScript 的判别联合、Lua 的 tagged table 形状一致，是跨语言协议里最通用的和类型编码。

📘 [MDN · `switch`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/switch)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP **没有带数据的枚举**：8.1 的枚举成员只能带一个 `int`/`string` 标量（backed enum），不能像 Rust 那样让不同成员携带不同形状的载荷。需要真正的和类型时要用类层次（抽象类 + 子类）或枚举加常量/静态映射；`match` 表达式可以在类层次上做分派，但**没有穷尽性检查**（漏分支抛 `UnhandledMatchError` 是运行时行为）。

```php
<?php
// 方案一：抽象类 + 子类（真正的和类型编码）
abstract class Shape {
    abstract public function area(): float;
}
final class Circle extends Shape {
    public function __construct(private float $r) {}
    public function area(): float { return 3.14159 * $this->r ** 2; }
}
final class Rect extends Shape {
    public function __construct(private float $w, private float $h) {}
    public function area(): float { return $this->w * $this->h; }
}
final class Point extends Shape {
    public function area(): float { return 0.0; }
}

echo (new Circle(2))->area(), ' ', (new Rect(3, 4))->area();   // 12.56636 12

// 方案二：枚举做标签 + match 分派（数据靠外部传入）
enum Kind { case Circle; case Rect; case Point; }
enum Op: string {                       // backed enum 只带一个标量
    case Add = '+';
    case Sub = '-';
}
function shapeArea(Kind $k, array $dims): float {
    return match($k) {                   // match 用 === 比较，穷尽时仍要 default 才安全
        Kind::Circle => 3.14159 * $dims['r'] ** 2,
        Kind::Rect   => $dims['w'] * $dims['h'],
        Kind::Point  => 0.0,
    };
}
echo shapeArea(Kind::Rect, ['w' => 3, 'h' => 4]);              // 12
echo Op::Add->value;                                            // +
try {
    // 枚举缺少某个 case 时的 match：抛 UnhandledMatchError
    $k = Kind::Point;
    echo match($k) { Kind::Circle => 1, Kind::Rect => 2 };      // 🛑 运行时抛错
} catch (\UnhandledMatchError $e) {
    echo 'UnhandledMatchError';                                 // UnhandledMatchError
}
// 方案三：用只读类携带数据（PHP 8.2 readonly class）
readonly class Vec2 { public function __construct(public float $x, public float $y) {} }
$v = new Vec2(1.0, 2.0);
echo $v->x + $v->y;                                             // 3
```

`match` 是表达式、用严格比较、**没有穷尽性检查**：所有 `case` 都不匹配时运行时抛 `UnhandledMatchError`（这是好事，比静默 `null` 强，但失败发生在运行时）；写成 `default => throw new \LogicException(...)` 也不能变成编译期检查。⚠️ 枚举不能有属性，所以"枚举 + 数据"只能把数据放在枚举的常量里（`const` 只能存标量或数组字面量）、或者放在外部数组里按 case 索引——前者要求数据在编译期已知，后者容易与枚举成员失同步。PHP 8.1 的枚举可以实现接口、可以有方法，所以一种实用折中是让枚举方法接受数据参数（`$kind->compute($dims)`），把每种形状的逻辑收进枚举；但数据本身仍不随成员走。`readonly class`（8.2 起）与 `final` 子类是 PHP 里最接近 record 的写法，配合 `match(true)` 或访问者模式做分派。序列化上类层次要自己定判别字段；backed enum 直接写 `value`，但纯枚举 `json_encode` 会失败。

📘 [PHP · `match`](https://www.php.net/manual/en/control-structures.match.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有和类型关键字，但结合 `Data.define`（3.2 起）与 `case/in` 模式匹配（3.0 起正式）能得到很接近的写法：`Data` 生成的不可变值对象自带 `deconstruct_keys`，`case/in` 用哈希模式解构并绑定变量。⚠️ **没有穷尽性检查**：所有分支都不匹配且没有 `else` 时抛 `NoMatchingPatternError`（运行时才发现）。

```ruby
Shape = Data.define(:kind, :a, :b)                 # 单一值对象承载和类型
def circle(r) = Shape.new(kind: :circle, a: r, b: nil)
def rect(w, h) = Shape.new(kind: :rect, a: w, b: h)
POINT = Shape.new(kind: :point, a: nil, b: nil)

def area(s)
  case s
  in { kind: :circle, a: r } then 3.14159 * r * r   # 哈希模式 + 变量绑定
  in { kind: :rect, a: w, b: h } then w * h
  in { kind: :point } then 0
  else raise ArgumentError, "unknown shape: #{s.kind}"   # 兜底（可选但强烈建议）
  end
end
puts area(circle(2.0)), area(rect(3.0, 4.0)), area(POINT)   # 12.56636 12.0 0

# 数组模式 + find 模式（deconstruct 由 Data 自动提供）
Case = Data.define(:tag, :value)
c = Case.new(tag: :num, value: 5)
case c
in [tag, value] then puts "#{tag}=#{value}"          # num=5（按 members 顺序解构）
end

# 独立的模式匹配运算符
puts(({ kind: :circle, a: 2.0, b: nil } in { kind: :circle }) ? "circle" : "other")  # circle

# 用类层次做真正的和类型
class Shape2; def area = raise NotImplementedError; end
class Circle2 < Shape2
  def initialize(r) = @r = r
  def area = 3.14159 * @r * @r
end
class Rect2 < Shape2
  def initialize(w, h) = (@w, @h = w, h)
  def area = @w * @h
end
puts Circle2.new(2.0).area, Rect2.new(3.0, 4.0).area  # 12.56636 12.0

# 没有 else 时的失败方式：运行时异常
begin
  area(Shape.new(kind: :blob, a: nil, b: nil))
rescue NoMatchingPatternError, ArgumentError => e
  puts e.class                                        # ArgumentError（命中上面的 raise）
end
```

`case/in` 的"exhaustive"在 Ruby 官方文档里的含义是**运行时失败**：不匹配任何 `in` 分支且没有 `else` 时抛 `NoMatchingPatternError`，`else` 是可选的，没有任何静态检查。⚠️ 因此想在编译期发现漏分支是做不到的，工程上的替代是给每个和类型写一个"分支清单"并加测试（例如遍历 `kind` 的所有取值都调一次 `area`），或者用 `dry-monads`/`sorbet` 的 `T::Enum` 配合 `case` 加 `T.absurd`（Sorbet 的 `T.absurd(x)` 在类型收窄不完整时**静态**报错，这是 Ruby 生态里唯一接近穷尽检查的机制，但需要静态类型检查器介入）。`Data` 的值相等、`with` 复制、`members`、`deconstruct`/`deconstruct_keys` 让它比散装 `Struct` 更适合做和类型载荷，但它不阻止 `kind` 取任意 Symbol——封闭性仍靠约定与测试。序列化上 `Data#to_h` 给 `{kind: :circle, a: 2.0, b: nil}`，Symbol 转 JSON 需要 `to_s` 或 `as_json` 自定义。

📘 [Ruby · Pattern matching](https://docs.ruby-lang.org/en/master/syntax/pattern_matching_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}
