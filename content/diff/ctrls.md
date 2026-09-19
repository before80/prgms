+++
title = "ctrls"
date = 2026-09-19T12:00:00+08:00
weight = 9
type = "docs"
description = "18 种语言的控制流对照：条件分支与模式匹配、循环、跳转与提前退出、迭代协议与生成器"
isCJKLanguage = true
draft = false
+++

# 控制流：18 种语言对照

条件、循环、跳转、迭代这四件事看着是编程语言的公分母，但每门语言对「控制流能不能有值」的回答截然不同：Rust、Swift、Kotlin 把 `if`、`switch`/`when`、`loop` 一律做成表达式，C、Go、Java 的传统形式则只是语句；Python、C#、Dart、Ruby 在各自的新版本里补上了结构化模式匹配，而 C、C++、Go、Lua、R 至今只有 `switch`/`case`/`if` 链。本页按 **条件分支与模式匹配 → 循环 → 跳转与提前退出 → 迭代协议与生成器** 四个主题组织，每个主题一套 18 语言标签页。前两个主题回答「怎么选、怎么重复」，后两个主题回答「怎么提前离开」与「怎么把遍历抽象成协议」。真正拉开差距的往往不是关键字拼写，而是穷尽性检查、作用域规则、标签跳转和迭代器协议这四件事。

## 控制流

**一页速览**

| 语言 | 条件分支与模式匹配 | 循环写法 | 跳转与陷阱 |
| --- | --- | --- | --- |
| Rust | `if`/`else`、`match`（穷尽、支持守卫）、`if let`、`let else` | `for` 走 `IntoIterator`、`while`、`while let`、`loop` 可带值 `break`；无 C 风格 `for` | 无 `goto`；标签写成生命周期 `'outer:`；`break`/`continue` 都能带标签 |
| Swift | `if` 与 `switch` 都是表达式，`switch` 穷尽、支持 `where` 与值绑定 | `for-in`、`while`、`repeat-while`、`stride`；无 C 风格 `for` | 标签 `outer:`；`switch` 分支不写 `break` 也不穿透，想穿透才写 `fallthrough` |
| Go | `if` 可带初始化语句；`switch` 默认不穿透、有类型 `switch`；无三元、无模式匹配 | 只有 `for` 一个关键字（三段式、条件式、无限式），配 `range` 迭代 | 有 `goto` 与标签；`fallthrough` 只能用在表达式 `switch`；1.22 起循环变量每次迭代新建 |
| Python | `if`/`elif`/`else`、条件表达式、`match`（3.10 起，软关键字） | `for` 遍历可迭代对象、`while`，以及 `for-else`/`while-else` | 无 `goto`、无标签跳转；`match` 是语句不是表达式；循环的 `else` 在没触发 `break` 时执行 |
| Kotlin | `if` 与 `when` 都是表达式；`when` 做穷尽检查，守卫条件 2.1 预览、2.2 起稳定 | `for (x in a..b)`、`while`、`do-while`、`repeat`；`for` 只遍历范围与集合 | 无 `goto`；标签 `foo@` 兼作 `return@foo`；`break`/`continue` 不能在非 inline lambda 里跨出 |
| Java | `if`、三元、`switch` 语句与 `switch` 表达式（14 起）、`switch` 模式匹配（21 起正式） | 经典 `for`、增强 `for`、`while`、`do-while` | 有标签 `outer:`、无 `goto`（保留字）；只有 `->` 形式才不穿透；原语类型模式到 Java 26 仍是 preview（JEP 530） |
| C++ | `if`/`switch` 可带初始化语句（17 起）、三元；没有模式匹配 | 经典 `for`、范围 `for`（11 起，20 起可带初始化语句）、`while`、`do-while` | 有 `goto`、无标签 `break`；穿透是默认行为；`case` 必须是常量表达式 |
| C | `if`/`else`、三元、`switch`（只能整数、穿透默认）；没有模式匹配 | `for`、`while`、`do-while` | 有 `goto`、无标签；悬垂 `else` 绑定最近的 `if`；C23 没有加 `switch` 表达式 |
| Julia | `if`/`elseif`/`else`、三元、短路布尔运算；没有 `switch`、没有模式匹配 | `for` 遍历集合、`while`，以及推导式与生成器表达式 | 语言没有 `goto`，Base 用宏 `@goto`/`@label` 模拟；`break`/`continue` 只能作用于最内层循环 |
| C# | `switch` 语句（不允许隐式穿透、每个 section 必须显式结束）、`switch` 表达式（8 起）、完整模式匹配（属性模式、列表模式、`when`） | `for`、`foreach`、`while`、`do-while` | 无标签 `break`（官方文档标注 C# 15 才加入），但有 `goto` 与 `goto case`；`switch` 表达式要穷尽；`yield break` 属于迭代器 |
| Dart | `if`、三元、`switch` 语句与 `switch` 表达式（3.0 起）加模式匹配 | `for`、`for-in`、`while`、`do-while` | 有标签 `outer:`；新式 `switch` 不穿透且要求穷尽；`for-in` 不能改集合结构 |
| R | `if`/`else`、向量化的 `ifelse()`、`switch()`；没有模式匹配 | `for`（遍历向量）、`while`、`repeat`，以及 `apply` 家族 | 无 `goto`、无标签；`if` 的 `else` 必须与 `if` 处在同一个表达式里；`break`/`next` 只在循环内有意义 |
| Zig | `if` 条件必须是 `bool`；`switch` 是表达式，支持范围与多值；无模式绑定 | `while` 可带 continue 表达式、`for`、`inline for`、`inline while`；无 C 风格 `for`、无 `do-while` | 标签 `blk:` 与 `outer:`，`break :blk value` 就是块的值；对 tagged union 的 `switch` 必须穷尽 |
| Lua | `if`/`elseif`/`else`；没有 `switch`，用 `if` 链或表分派替代 | 数值 `for`、泛型 `for`、`while`、`repeat-until` | 有 `goto` 与 `::label::`、没有 `continue`（用 `goto continue` 或 `if` 包裹）；5.5 起 `for` 控制变量只读 |
| TypeScript | `if`、三元、`switch`（用 `===` 比较、穿透默认）、`?.` 与 `??` 判空；无真模式匹配 | `for`、`for-in`（键）、`for-of`（值）、`while`、`do-while` | 有标签语句；`switch` 不穷尽也不报错；类型收窄只活在编译期 |
| JavaScript | 同 TypeScript，但没有类型收窄与 `satisfies` | `for`、`for-in`（键，含原型链）、`for-of`（值，走 `Symbol.iterator`） | 有标签语句；`for-in` 会枚举原型链上的可枚举属性；`function*` 生成器两用 |
| PHP | `if`/`elseif`/`else`、三元与 `?:`、`match` 表达式（8.0 起，严格比较）、`switch`（松散比较） | `for`、`foreach`、`while`、`do-while` | 有 `goto`（不能跳进循环或 `switch`、不能跨函数）；`break 2`/`continue 2` 按层数跳；`switch` 是松散比较 |
| Ruby | `if`/`unless`/`elsif`、三元、语句修饰符、`case/when`、`case/in` 模式匹配（3.0 起） | `while`、`until`、`for`（`each` 的语法糖）、`each`、`times`、`upto`、`step`、`loop` | 没有 `goto`、没有 `continue`（`next` 就是 continue）；`break` 可带值；`catch`/`throw` 做非局部退出 |

### 条件分支与模式匹配

`if`/`else` 与三元运算符是 18 门语言的公共起点，真正分道扬镳的是「分支能不能有值」和「匹配能不能解构」。这一节里，Rust、Swift、Kotlin、Zig、Ruby、Julia 的分支是表达式，C、Go、Java 的传统 `switch` 是语句；结构化模式匹配已经是主流：Rust、Swift、C#、Dart、Python、Ruby 在 `match`/`case`/`in` 里直接解构绑定，Java 21 起能用记录模式拆开 `record`，Kotlin 的 `when` 支持类型判断、区间与守卫但**不**做解构绑定；C、C++、Go、Lua、R 只能用 `if` 链、类型断言或表分派替代。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的分支全部是表达式：`if`/`else` 能求值，`match` 是最强的模式匹配工具，穷尽性由编译器在编译期强制检查。绑定按值还是按引用由模式与匹配对象的类型决定，`match` 臂可以带 `if` 守卫；只在意外一种形态时用 `if let`，需要在函数开头就退出时用 `let else`。Rust 没有三元运算符，也没有 `switch` 关键字。

```rust
enum Shape { Circle(f64), Square(f64) }

fn main() {
    let n = 7;
    let label = if n % 2 == 0 { "even" } else { "odd" };  // if 是表达式
    println!("{label}");                                  // odd

    let d = 3;
    let s = match d {
        1 => "one",
        2..=5 if d % 2 == 1 => "small odd",               // 范围模式 + 守卫
        _ => "other",                                     // 通配保证穷尽
    };
    println!("{s}");                                      // small odd

    let opt: Option<i32> = Some(5);
    if let Some(v) = opt { println!("{v}"); }             // 5
    let Some(w) = opt else { return };                    // let-else 必须发散
    println!("{w}");                                      // 5

    let area = match Shape::Circle(1.0) {                 // 枚举匹配必须穷尽
        Shape::Circle(r) => 3.14 * r * r,
        Shape::Square(a) => a * a,
    };
    println!("{area}");                                   // 3.14
}
```

`match` 与 `switch` 最本质的区别是：它按模式自上而下匹配，编译器会检查所有取值是否被覆盖，漏掉一个 `enum` 变体就编译不过；`_` 不是「default 分支」而是通配模式，写上它等于放弃穷尽性检查。`if let`/`let else` 是只匹配一个模式时的糖：前者在匹配失败时跳过块，后者在匹配失败时执行 `else` 块，而 `else` 块必须发散（`return`、`break`、`continue`、`panic!`）。⚠️ 注意 `match` 的臂按顺序求值，`_` 放在前面会让后面的臂变成不可达代码；守卫不参与穷尽性分析，所以 `2..=5 if cond` 之后仍需要 `_` 兜底。

📘 [Rust Reference · match 表达式](https://doc.rust-lang.org/reference/expressions/match-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 从 5.9 起把 `if` 和 `switch` 都提升为表达式，可以直接写在赋值或 `return` 右边。`switch` 不需要 `break`，一个 `case` 执行完自动结束，也不会穿透，只有显式写 `fallthrough` 才继续下一个分支；每个分支支持值绑定、区间模式、元组模式与 `where` 过滤，编译器检查穷尽性。没有模式匹配的语言里 `switch` 只能比常量，Swift 的 `case` 干的却是解构的活。

```swift
let n = 7
let label = if n % 2 == 0 { "even" } else { "odd" }   // if 是表达式
print(label)                                           // odd
let size = switch n {                                  // switch 也是表达式
case 1...5: "small"
case 6...10: "medium"
default: "large"
}
print(size)                                            // medium

enum Shape { case circle(Double), square(Double) }
func area(of shape: Shape) -> Double {
    switch shape {                                     // 穷尽性由编译器检查
    case .circle(let r): 3.14 * r * r
    case .square(let a): a * a
    }
}
print(area(of: .circle(1.0)))                          // 3.14

let opt: Int? = 5
if let v = opt { print(v) }                            // 5
guard let w = opt else { fatalError() }                // guard 提前退出
print(w)                                               // 5
```

`switch` 的每个分支至少要有一条语句，想什么都不做就写 `break`；`fallthrough` 会直接进入下一个 `case` 的代码而不重新匹配，所以它不适用于值绑定模式。`guard` 不是分支而是「不满足就离开当前作用域」的断言，它绑定出来的变量在 `guard` 之后仍然可用，这正是它比 `if let` 更适合做前置检查的原因。⚠️ `switch` 对 `enum` 必须覆盖全部 `case`，如果 `enum` 是 `@frozen` 之外的库类型，跨模块升级会导致编译失败，这时补一个 `@unknown default` 更稳妥。三元运算符 `?:` 仍然存在，但只有两个分支时用它、多分支用 `switch` 表达式是社区共识。

📘 [Swift · Control Flow](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/controlflow/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的条件分支只有 `if` 与 `switch` 两种语句，没有三元运算符、没有模式匹配，`if` 可以在条件前带一条初始化语句。`switch` 有两种形态：表达式 `switch` 与类型 `switch`；默认不穿透，想穿透要显式写 `fallthrough`，而不带标签的 `switch` 等价于 `switch true`，常被用来替代长 `if/else if` 链。类型 `switch` 是 Go 在缺少模式匹配时最接近「按类型分派」的写法。

```go
package main

import "fmt"

func main() {
	n := 7
	if r := n % 2; r == 0 {          // if 可以带初始化语句
		fmt.Println("even")
	} else {
		fmt.Println("odd")           // odd
	}
	label := "odd"                    // 没有三元，只能写 if
	if n%2 == 0 {
		label = "even"
	}
	fmt.Println(label)                // odd

	switch d := 3; d {                // 默认不穿透
	case 1:
		fmt.Println("one")
	case 2, 3:
		fmt.Println("two-or-three")   // two-or-three
	default:
		fmt.Println("other")
	}
	switch 1 {
	case 1:
		fmt.Println("one")
		fallthrough                   // 显式穿透
	case 2:
		fmt.Println("two")            // two
	}
	switch {                          // 无标签 switch == switch true
	case n > 5:
		fmt.Println("big")            // big
	}
	var x any = 42
	switch v := x.(type) {            // 类型 switch
	case int:
		fmt.Println("int", v)         // int 42
	case string:
		fmt.Println("string", v)
	}
}
```

`if` 的初始化语句把临时变量的作用域压缩到 `if/else` 内部，这是 Go 里 `if err := f(); err != nil {}` 惯用法的来源。`switch` 的 `case` 自上而下求值、命中第一个即停止，所以 `case` 的顺序就是优先级；`fallthrough` 只能出现在表达式 `switch` 里，而且它跳到的是下一个 `case` 的语句体，不重新判断条件。⚠️ 类型 `switch` 的 `v` 在每个 `case` 里类型不同（默认是原类型），且类型 `switch` 不支持 `fallthrough`。Go 没有模式匹配，解构结构体只能靠类型断言、`reflect` 或手写 getter。

📘 [Go spec · Switch statements](https://go.dev/ref/spec#Switch_statements)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的条件分支是语句式的 `if`/`elif`/`else`，三元写成条件表达式 `a if cond else b`；3.10 起增加了结构化模式匹配 `match`/`case`，它是一个语句而不是表达式，`match` 是「软关键字」，仍然可以继续当普通变量名用。`match` 支持字面量、捕获、序列、映射、类、或模式与守卫 `if`，并引入 `_` 通配与 `|` 或模式。没有 `switch` 关键字。

```python
# ---- 条件分支与模式匹配 ----
n = 7
label = "even" if n % 2 == 0 else "odd"      # 条件表达式
print(label)                                  # odd

def classify(command: str) -> str:
    match command.split():                    # 结构化模式匹配（3.10+）
        case ["go", direction]:               # 序列模式 + 捕获
            return f"go {direction}"
        case ["go", _]:                       # _ 是通配，不绑定
            return "go nowhere"
        case ["look"] if n > 5:               # 守卫
            return "look closely"
        case _:                               # 兜底，match 不检查穷尽
            return "unknown"

print(classify("go north"))                   # go north
print(classify("go"))                         # go nowhere
print(classify("look"))                       # look closely
print(classify("dance"))                      # unknown

point = (0, 3)
match point:                                  # 捕获与或模式
    case (0, 0):
        print("origin")
    case (0, y) | (y, 0):
        print(f"on axis at {y}")              # on axis at 3
    case _:
        print("elsewhere")
```

`case` 是模式不是表达式，同一分支里的多个模式用 `|` 连接，捕获在 `|` 两侧必须绑定同样的名字集合。`match` 不做穷尽性检查，漏掉的分支只在运行时静默落到下一个 `case`，如果都不想匹配就会什么都不做，所以工程上通常用 `case _:` 兜底再加 `raise`。⚠️ 网络上传的「`match` 比 `if` 快」是误解，它仍然逐条线性匹配，只是把解构与判类型写得更紧凑；`case` 里的裸名字是捕获模式而不是比较，想比较常量要用 `case 1:` 或加点号限定名（`case Color.RED:`）。

📘 [Python Reference · match 语句](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `if` 与 `when` 都是表达式，`when` 完全取代了 `switch`：分支条件可以是常量、逗号分隔的多个值、`in` 区间、`is` 类型判断甚至任意布尔表达式，对 `enum` 与 `sealed` 主语会做穷尽性检查。带主语的 `when` 分支支持守卫条件（在条件后加 `if`），该特性在 2.1 进入预览、2.2 起稳定。没有三元运算符，也没有 `switch` 关键字。

```kotlin
enum class Level { LOW, MID, HIGH }

fun label(n: Int): String = when (n) {            // when 是表达式
    0 -> "zero"
    in 1..5 -> "small"
    in 6..10 if n % 2 == 1 -> "odd medium"        // 守卫条件：2.1 预览、2.2 稳定
    else -> "big or even"                         // 有主语时需要兜底
}

fun describe(x: Any): String = when (x) {         // 类型分支
    is String -> "string of ${x.length}"
    is Int -> "int $x"
    else -> "other"
}

fun levelName(l: Level): String = when (l) {      // enum 穷尽，无需 else
    Level.LOW -> "low"
    Level.MID -> "mid"
    Level.HIGH -> "high"
}

fun main() {
    println(label(7))             // odd medium
    println(describe("abc"))      // string of 3
    println(levelName(Level.MID)) // mid
    val n = 7
    println(if (n % 2 == 0) "even" else "odd")   // Kotlin 没有三元运算符，用 if 表达式
}
```

`when` 有两种形态：带主语（`when (x)`）与不带主语（`when { cond -> ... }`，分支条件必须是布尔表达式）。带主语时，如果主语是 `enum`、`sealed` 或 `Boolean` 且所有取值都被覆盖，`else` 可以省略，编译器会替你证明穷尽；否则必须写 `else`，因为编译器无法枚举所有可能值。守卫条件让「同一个模式 + 额外判断」不必再嵌套 `if`，比在分支体里写 `if` 再 `return` 更清晰。⚠️ `when` 的分支如果用 `->` 就不穿透，用老式 `:` 才会继续往下执行；`is` 分支里的智能转换只在分支体、且变量是 `val` 或未被并发修改时才成立。

📘 [Kotlin · Control flow](https://kotlinlang.org/docs/control-flow.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 沿用 C 系的 `if`/`switch` 语句和三元运算符，但 14 起 `switch` 也能当表达式（用 `->` 与 `yield`），21 起 `switch` 支持模式匹配：`case` 后面可以跟类型模式、`null` 标签和 `when` 守卫，对 `sealed` 层次结构会做穷尽性检查。`goto` 是保留字但从未实现；多层循环只能靠带标签的 `break`/`continue` 离开。解构能力只覆盖 `record`：21 起可以用记录模式把 `Point(int x, int y)` 这类记录直接拆开，普通类没有通用的属性解构。

```java
sealed interface Shape permits Circle, Square {}
record Circle(double r) implements Shape {}
record Square(double a) implements Shape {}

public class Ctrl {
    static double area(Shape s) {
        return switch (s) {                            // switch 表达式，必须穷尽
            case Circle c -> 3.14 * c.r() * c.r();
            case Square q -> q.a() * q.a();
        };
    }

    static String kind(Object o) {
        return switch (o) {
            case null -> "null";                       // null 标签（21 起）
            case Integer i when i > 10 -> "big int";   // 守卫子句
            case Integer i -> "int " + i;
            case String s -> "string " + s.length();
            default -> "other";
        };
    }

    public static void main(String[] args) {
        System.out.println(area(new Circle(1.0)));     // 3.14
        System.out.println(kind(42));                  // big int
        System.out.println(kind("abc"));               // string 3
        int n = 7;
        String label = n % 2 == 0 ? "even" : "odd";    // 三元运算符
        System.out.println(label);                     // odd
        switch (n) {
            case 1: System.out.println("one"); break;
            default: System.out.println("other");      // other
        }
    }
}
```

`switch` 表达式的每一臂都要产出值：用 `->` 直接写表达式，或者用 `yield` 返回；语句形式用 `:` 标签时仍然默认穿透，直到遇到 `break`。21 起模式 `switch` 的两条重要规则是：`null` 不再一律抛 `NullPointerException`，而是可以被 `case null` 显式匹配；如果 `switch` 在编译期是穷尽的、运行时却遇到未覆盖的值，会抛 `MatchException`。⚠️ 类型模式按顺序判断，父类型模式写在子类型前面会让后面的分支不可达并直接编译报错；类型模式的类型不能带类型实参，泛型信息在运行时已经被 type erasure 抹掉，所以写不出 `case List<String> l`，只能用原始类型或带通配的形式再配守卫，类型参数也不是 reified 的，想按实参分派只能显式传入 `Class<T>` 之类的类型令牌；原语类型（`int`、`double` 等）作为模式尚未转正：Java 25 是 JEP 507 第三次预览、Java 26 是 JEP 530 第四次预览，写进生产代码前要确认目标 JDK 与 `--enable-preview`。

📘 [JLS · switch 语句（§14.11）](https://docs.oracle.com/javase/specs/jls/se25/html/jls-14.html#jls-14.11)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的条件分支是语句式的 `if`/`switch` 加三元运算符，没有模式匹配。C++17 给 `if` 和 `switch` 加了初始化语句（`if (init; cond)`），同年引入 `if constexpr` 做编译期分支；C++23 又补了 `if consteval`，用来判断当前是否在常量求值上下文中。`switch` 只能作用于整型与枚举，`case` 标签必须是常量表达式，穿透是默认行为。范围 `for` 的初始化语句是 C++20 才有的。

```cpp
#include <cstdio>
enum class Color { red, green, blue };

int main() {
    int n = 7;
    const char* label = (n % 2 == 0) ? "even" : "odd";        // 三元
    std::printf("%s\n", label);                               // odd
    if (int k = n * 2; k > 10) std::printf("big %d\n", k);    // big 14
    else std::printf("small %d\n", k);                        // k 的作用域在 if/else 内

    switch (n) {                                              // 只能整型/枚举
        case 1: std::printf("one\n"); break;
        case 2:
        case 3: std::printf("two-or-three\n"); break;          // 多标签共用
        default: std::printf("other\n"); break;                // other
    }

    if constexpr (sizeof(void*) == 8) std::printf("64-bit\n"); // 编译期分支
    else std::printf("32-bit\n");                              // 64-bit

    Color c = Color::green;
    switch (c) {
        case Color::red: std::printf("red\n"); break;
        case Color::green: std::printf("green\n"); break;      // green
        case Color::blue: std::printf("blue\n"); break;
    }
}
```

`if constexpr` 与普通 `if` 的区别在于：被丢弃的分支仍然要能通过语法检查，但不会实例化模板，也不要求在目标平台上合法，这是模板库里做条件编译的标准手段；C++23 的 `if consteval` 则用来在同一个函数里区分编译期与运行期实现（常量求值时不允许多数副作用）。`switch` 的穿透常被用错：连续几个没有语句的 `case` 标签是「多值共用一段代码」，而有语句却不写 `break` 才是 bug；C++17 起 `case` 标签还有 `[[fallthrough]]` 属性可以显式表达意图。⚠️ `switch` 的初始化语句与条件之间用分号分隔、不是逗号；`case` 标签必须是常量表达式，C++ 里不能用字符串或结构体做 `switch` 值。

📘 [cppreference · if 语句](https://en.cppreference.com/w/cpp/language/if)

{{% /tab %}}

{{% tab header="C" %}}

C 的条件分支只有语句式的 `if`/`else`、三元运算符和整型 `switch`；没有模式匹配，也没有 `switch` 表达式，C23 也没有加这两样。`switch` 的 `case` 必须是整数常量表达式，穿透是默认行为，`break` 才是出口；悬垂 `else` 永远绑定最近的、还没有 `else` 的 `if`。三元运算符的两个分支会做通常算术转换，得到一个公共类型。

```c
#include <stdio.h>

int main(void) {
    int n = 7;
    const char *label = (n % 2 == 0) ? "even" : "odd";   /* 三元运算符 */
    printf("%s\n", label);                               /* odd */

    switch (n) {                                         /* C 只有 switch 语句 */
    case 1: puts("one"); break;
    case 2:
    case 3: puts("two-or-three"); break;                 /* 多个标签共用一段代码 */
    default: puts("other"); break;                       /* other */
    }
    switch (1) {                                         /* 穿透是默认行为 */
    case 1: puts("one");                                 /* 故意不写 break */
    case 2: puts("two"); break;                          /* one 然后 two */
    }
    if (n > 5)
        if (n > 10) puts("gt10");
        else puts("5..10");                              /* 悬垂 else 绑定最近的 if */
    /* ✅ 想让 else 绑定外层 if 就加大括号 */
    if (n > 5) {
        if (n > 10) puts("gt10");
    } else {
        puts("5 or less");
    }
    return 0;
}
```

C 没有 `bool` 之外的「真值」概念：条件是标量表达式，`0`、空指针为假，其它为真。`case` 后面只能是整型常量表达式，所以 C 无法对字符串或结构体做 `switch`，这类需求只能用 `if`/`else if` 链或查表；`switch` 的表达式必须是整型，`long long` 与枚举都可以，浮点不行。⚠️ 悬垂 `else` 是 C 语法里的经典坑，编译器的 `-Wdangling-else` 就是为了提醒你这里有歧义，正确做法是无条件给内层 `if` 加花括号。`case` 标签下面的声明需要大括号包起来，否则会报「a label can only be part of a statement」。

📘 [cppreference · C switch 语句](https://en.cppreference.com/w/c/language/switch)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用 `if`/`elseif`/`else` 和三元 `cond ? a : b` 做条件分支，`if` 块的值就是块内最后一个表达式的值，所以它同时是表达式。Julia 没有 `switch`、没有模式匹配，多分支的惯用替代是多重派发（multiple dispatch）：按参数类型定义多个方法，由运行时的类型分派替你完成「选分支」。`&&` 与 `||` 是短路布尔运算，两边都必须是 `Bool`。

```julia
function classify(n)
    if n < 0
        "negative"
    elseif n == 0
        "zero"
    else
        "positive"
    end                       # if 块的值 = 最后一条语句的值
end
println(classify(7))           # positive
println(classify(-1))          # negative

n = 7
println(n % 2 == 0 ? "even" : "odd")   # odd（三元不是惰性语法糖，是表达式）

# 没有 switch/match：多重派发是惯用替代
describe(::Int) = "int"
describe(::AbstractString) = "string"
describe(::AbstractFloat) = "float"
println(describe(1.5))         # float
println(describe("x"))         # string

# ifelse 是普通函数，两个分支都会被求值
println(ifelse(n > 5, "big", "small"))   # big
```

三元运算符 `a ? b : c` 只在 `b`、`c` 类型相容时效率最好，因为 Julia 会做类型推断，返回类型不一致会导致装箱与性能下降；这也是社区更推荐 `if` 块而不是长三元链的原因。`ifelse(cond, a, b)` 是函数而不是语法，它的两个分支参数在调用前一定会被求值，所以不能用来做「除零保护」这类惰性判断，那种情况必须写 `if`。⚠️ `if` 的条件必须是 `Bool`：`if 1 end` 会直接报 `TypeError`，而 `missing` 也不是合法的条件；多重派发虽然能替代 `switch`，但它是按「方法表」分派而不是按值匹配，二者在编译期检查与可扩展性上并不等价。

📘 [Julia · Control Flow](https://docs.julialang.org/en/v1/manual/control-flow/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 同时有 `switch` 语句和 `switch` 表达式，配合 `is` 与递归模式（类型模式、属性模式、位置模式、关系模式、逻辑模式、列表模式）构成完整的模式匹配体系。`when` 提供守卫条件，`switch` 表达式要求穷尽，不穷尽时编译器给警告、运行时抛 `SwitchExpressionException`。与 C 系不同的是，`switch` 语句的每个 section 不允许隐式穿透，必须以 `break`、`goto`、`return` 或 `throw` 结束。

```csharp
using System;

record Point(int X, int Y);

class Ctrl {
    static string Describe(object o) => o switch {        // switch 表达式
        null => "null",
        int i when i > 10 => "big int",                   // 守卫
        int i => $"int {i}",
        Point { X: 0, Y: 0 } => "origin",                 // 属性模式
        Point (0, var y) => $"on y-axis at {y}",          // 位置模式
        string s => $"string of {s.Length}",
        _ => "other",                                     // 丢弃模式兜底
    };

    static void Main() {
        Console.WriteLine(Describe(42));                   // big int
        Console.WriteLine(Describe(new Point(0, 3)));        // on y-axis at 3
        Console.WriteLine(Describe("abc"));                 // string of 3
        int n = 7;
        string label = n % 2 == 0 ? "even" : "odd";
        Console.WriteLine(label);                           // odd
        switch (n) {
            case 1:
                Console.WriteLine("one");
                break;
            case 2:
                goto case 3;                                // 显式跳到别的 case
            case 3:
                Console.WriteLine("two-or-three");
                break;
            default:
                Console.WriteLine("other");                 // other
                break;
        }
    }
}
```

`switch` 表达式的每个臂都是「模式 `=>` 表达式」，编译器检查能否覆盖全部输入；`switch` 语句则更像 C 的 `switch`，但没有隐式穿透——想共用代码必须把多个 `case` 标签叠在一起写，想跳到别处要用 `goto case`/`goto default`。列表模式（C# 11）让数组与 `Span` 也能解构，例如 `[1, 2, .. var rest]`、`[_, .., last]`。⚠️ 常见坑是 `case string s` 之后又写 `case null` 的顺序：`null` 不会被任何类型模式匹配到，必须显式写 `case null` 或让兜底 `_` 处理；另外 `switch` 表达式里位置模式的参数个数必须与记录类型的解构函数一致。C# 14 没有给控制流加新语法，带标签的 `break`/`continue` 在官方文档里标注为 C# 15 才加入。

📘 [MS Learn · 模式匹配](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/patterns)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 3.0 引入模式匹配与 `switch` 表达式，`switch` 从此既能作语句也能作表达式，`case` 支持类型模式、解构（对象/列表/映射）、逻辑模式与关系模式，`when` 提供守卫。对 `sealed` 类型做穷尽性检查，新式 `->`/`=>` 分支不再需要 `break`。空安全在语言层面处理，`late`、`?`、`!`、`?.` 与 `??` 补足了判空能力。

```dart
sealed class Shape {}
class Circle extends Shape { final double r; Circle(this.r); }
class Square extends Shape { final double a; Square(this.a); }

double area(Shape s) => switch (s) {          // switch 表达式 + 穷尽检查
  Circle(r: var r) => 3.14 * r * r,           // 对象模式解构
  Square(a: var a) => a * a,
};

String classify(Object o) => switch (o) {
  int n when n > 10 => 'big int',             // 守卫
  int n => 'int $n',
  [int a, int b] => 'pair $a,$b',             // 列表模式
  String s => 'string ${s.length}',
  _ => 'other',
};

void main() {
  print(area(Circle(1.0)));                   // 3.14
  print(classify(42));                        // big int
  print(classify([1, 2]));                    // pair 1,2
  var n = 7;
  print(n % 2 == 0 ? 'even' : 'odd');         // odd
  if (n case > 5) print('big');               // if-case：模式直接写在条件里
}
```

`switch` 表达式要求穷尽：对 `sealed` 类型只要覆盖所有子类即可，对 `Object` 这种开放类型必须写 `_` 兜底，否则编译失败。`if-case` 把模式匹配带进了 `if`，适合「匹配成功就做一件事」的场景，比先 `switch` 再 `return` 更轻。⚠️ 对象模式里的 getter 名必须存在，`Circle(r: var r)` 要求 `Circle` 有无参 getter `r`，写错名字是编译错误而不是运行时错误；Dart 的 `switch` 语句里非空 `case` 执行完直接跳到 `switch` 末尾，**不需要** `break`，也不存在 C 那样的穿透（官方文档的措辞是「non-empty case clauses jump to the end of the switch after completion」），只有空分支才会落到下一个分支，因此想让两个分支共用一段代码，要么把空分支叠在一起，要么用 `continue` 加标签跳到指定分支。

📘 [Dart · Patterns](https://dart.dev/language/patterns)

{{% /tab %}}

{{% tab header="R" %}}

R 的 `if`/`else` 是表达式，可以直接赋值；`ifelse()` 是向量化版本，`switch()` 按位置或按名字选择分支。R 没有 `case`/`match` 这类的模式匹配，多分支靠 `if`/`else if` 链、`switch()` 或对数据框做子集操作。R 4.6 也没有给控制流加新语法。

```r
n <- 7
label <- if (n %% 2 == 0) "even" else "odd"    # if 是表达式
print(label)                                    # [1] "odd"

# ⚠️ else 必须和 if 处在同一个表达式里
# 下面这样写会报 "unexpected else"：
#   if (n > 0) { "pos" }
#   else { "neg" }
x <- 1
if (x > 0) {
  res <- "positive"
} else {
  res <- "non-positive"
}
print(res)                                      # [1] "positive"

ifelse(c(1, 2, 3) > 1, "big", "small")          # 向量化：[1] "small" "big" "big"

switch("b", a = 1, b = 2, c = 3)                # [1] 2（按名字）
switch(2, "one", "two", "three")                # [1] "two"（按位置）

# 没有模式匹配：用 if/else 链或 switch 模拟
grade <- function(score) {
  if (score >= 90) "A" else if (score >= 60) "pass" else "fail"
}
print(grade(75))                                # [1] "pass"
```

`ifelse()` 是普通的向量化函数而不是控制结构：三个参数都会被完整求值，所以 `ifelse(x > 0, log(x), 0)` 在 `x <= 0` 时仍然会算 `log(x)` 并产生警告，这类场景要用 `if`/`else` 或先做子集再赋值。`switch()` 的按名字形式在没有匹配时会返回 `NULL`（不是报错），按位置形式传入超出范围的位置也会返回 `NULL`，需要自己兜底。⚠️ `else` 换行是 R 新手最常见的语法错误，交互式环境里换行即执行，所以必须把 `} else {` 写在同一行；此外 `if` 的条件只取第一个元素，长度大于 1 的逻辑向量会警告并只用第一个。

📘 [R Language Definition · Control structures](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Control-structures)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的 `if` 与 `switch` 都是表达式，可以直接给变量赋值或 `return`。`if` 的条件必须是 `bool`，没有隐式真值转换；`switch` 支持多重值、范围与 `else`，对枚举与 tagged union 强制穷尽，是 Zig 里替代模式匹配的主力。可选类型用 `if (opt) |v| { ... }` 解包，错误联合用 `catch`/`try` 处理，这两种写法承担了别的语言里模式匹配的一部分职责。

```zig
const std = @import("std");
const Shape = union(enum) { circle: f64, square: f64 };

fn area(s: Shape) f64 {
    return switch (s) {                 // switch 表达式，必须覆盖所有 tag
        .circle => |r| 3.14 * r * r,    // 捕获负载
        .square => |a| a * a,
    };
}

fn classify(n: i32) []const u8 {
    return switch (n) {                 // 支持多重值与范围
        0 => "zero",
        1, 2, 3 => "small",
        4...10 => "medium",
        else => if (n < 0) "negative" else "big",   // if 也是表达式
    };
}

pub fn main() void {
    std.debug.print("{d}\n", .{area(.{ .circle = 1.0 })});   // 3.14
    std.debug.print("{s}\n", .{classify(7)});                // medium
    const maybe: ?i32 = 5;
    if (maybe) |v| {                                         // 解包 optional
        std.debug.print("{d}\n", .{v});                      // 5
    } else {
        std.debug.print("none\n", .{});
    }
}
```

`switch` 是 Zig 里最像模式匹配的构造：对象可以是整数、枚举、`bool`、可选类型、错误联合或元组，分支用 `.tag => |payload|` 同时完成判别与绑定；范围用三个点 `4...10`（含两端），多值用逗号，`else` 兜底。对 `enum` 或 `union(enum)`，只要不用 `else` 就必须列全所有成员，漏一个编译报错，这正是 Zig 抗忘记的机制。⚠️ Zig 没有 `do-while`、没有 C 风格 `for`、没有 `switch` 的穿透（一个分支结束就是结束）；`if` 的 `|v|` 解包语法只对 optional 与错误联合有效，`switch` 的 `|payload|` 只对带负载的类型有效，两者不能互换。C 的悬垂 `else` 在 Zig 里不存在，因为 `if` 是表达式、必须配 `else` 才能有值。

📘 [Zig · switch](https://ziglang.org/documentation/master/#switch)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的条件分支只有 `if`/`elseif`/`else`，没有 `switch`、也没有模式匹配；多分支的常规替代是 `if` 链、表分派或函数表。Lua 的真值规则极简：只有 `false` 与 `nil` 为假，`0` 和空字符串都是真。三元运算符也没有，惯用写法是 `cond and a or b`，它在 `a` 为 `false`/`nil` 时会出错。Lua 5.5 起 `global` 成了保留字。

```lua
local n = 7
print(n % 2 == 0 and "even" or "odd")     -- odd（三元模拟）
if 0 then print("0 是真值") end            -- 0 是真值（只有 false/nil 为假）

if n < 0 then
  print("negative")
elseif n == 0 then
  print("zero")
else
  print("positive")                        -- positive
end

-- 没有 switch：表分派是最接近的替代
local name = { [1] = "one", [2] = "two", [3] = "three" }
print(name[n] or "other")                  -- other

-- ⚠️ and/or 三元在候选值为 false/nil 时失效
local v = nil
print(true and v or "fallback")            -- fallback（不是 nil）
-- ✅ 用显式 if 或 (cond and {a} or {b})[1] 之类的包装
local r
if true then r = v else r = "fallback" end
print(r)                                   -- nil
```

表分派比 `if` 链更适合「值 → 动作」的映射：把处理函数放进表里，用 `handlers[key]` 取，既快又好扩展，取不到时用 `or` 给默认值。⚠️ `and`/`or` 返回的是操作数本身而不是布尔值，这既是三元模拟的基础，也是它失效的原因——`cond and a or b` 只在 `a` 不为假时等价于三元。5.5 把 `global` 列为保留字，老代码里用 `global` 当变量名会直接语法错误；另外 5.5 的 `for` 循环控制变量是只读的，循环体里给它赋值会报错，需要另起一个 `local` 变量。

📘 [Lua 5.5 · if 语句](https://www.lua.org/manual/5.5/manual.html#3.3.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有新增控制流语法，它继承 JavaScript 的 `if`、三元运算符与 `switch`，在这之上加了编译期的类型收窄：`typeof`、`instanceof`、`in`、判别联合（discriminated union）与自定义类型谓词都能让 `switch`/`if` 分支里的类型自动变窄。`switch` 仍然用 `===` 比较、默认穿透，编译器不强制穷尽，但可以用 `never` 赋值的技巧把穷尽性变成编译错误。

```typescript
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; a: number };

function area(s: Shape): number {
  switch (s.kind) {                     // 判别联合：按 kind 收窄
    case "circle": return 3.14 * s.r * s.r;
    case "square": return s.a * s.a;
    default: {
      const never: never = s;           // 穷尽检查：漏一个就编译报错
      throw new Error(`unhandled ${JSON.stringify(never)}`);
    }
  }
}
console.log(area({ kind: "circle", r: 1 }));   // 3.14

const n: number = 7;
console.log(n % 2 === 0 ? "even" : "odd");     // odd
const user: { address?: { city?: string } } = {};
console.log(user.address?.city ?? "unknown");  // unknown（?. 与 ??）
```

判别联合 + `switch` 是 TypeScript 里最常用的「模式匹配替代品」：每个变体带一个字面量类型的判别字段，`switch` 该字段之后每个分支里的对象类型自动收窄到对应变体，`default` 里把值赋给 `never` 就能在新增变体时立刻编译失败。⚠️ 类型收窄只存在于编译期，生成的 JavaScript 里没有任何检查代码；`switch` 里的 `case "circle"` 仍然是字符串比较，写错字面量只会落进 `default`；`as` 断言不会做运行时校验，判空请用 `?.`、`??` 或显式 `typeof`。

📘 [TypeScript Handbook · Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的条件分支只有 `if`、三元运算符和 `switch`，没有模式匹配；`switch` 用严格相等 (`===`) 比较、默认穿透，判空主要靠 `?.`（可选链）与 `??`（空值合并）以及 `||` 的假值兜底。`switch (true)` 是一个流传很广的惯用法，把布尔条件塞进 `case`，用来模拟多分支 `if` 链。所有值都有真假之分，假值只有 `false`、`0`、`-0`、`0n`、`""`、`null`、`undefined`、`NaN`。

```javascript
const n = 7;
console.log(n % 2 === 0 ? "even" : "odd");    // odd
switch (n) {                                   // 用 === 比较
  case 1: console.log("one"); break;
  case 2:
  case 3: console.log("two-or-three"); break;
  default: console.log("other");               // other
}
// switch (true)：把任意条件放进 case
switch (true) {
  case n > 10: console.log("big"); break;
  case n > 5: console.log("medium"); break;    // medium
  default: console.log("small");
}
const user = { address: null };
console.log(user.address?.city ?? "unknown");   // unknown
console.log(user.address && user.address.city); // null（旧写法）
console.log(0 || "fallback", 0 ?? "fallback");  // fallback 0（?? 只认 null/undefined）
```

`switch` 的比较是 `===`，所以 `case "1"` 永远不会匹配数字 `1`，类型不匹配时连隐式转换都不会发生；`case` 后面可以是任意表达式（包括变量与函数调用），但每个 `case` 都要求值，写在 `switch` 外部的表达式只会求值一次。⚠️ 忘了 `break` 会穿透到下一个分支，这是最经典的 JS bug；`switch (true)` 虽然好用，但 `case` 会从上到下求值，条件重叠时顺序就决定结果。`forEach`/`map` 的回调里 `break` 是语法错误，那种场景要用 `for...of` 或 `some`/`find`。

📘 [MDN · switch](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/switch)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 有 `if`/`elseif`/`else`、三元运算符、`?:` 与 `??`，并且从 8.0 起提供了 `match` 表达式：`match` 用严格比较 (`===`)，没有匹配时抛 `UnhandledMatchError`，每个分支只求值命中的那一个，且是表达式可以直接赋值。`switch` 仍然存在，但它用松散比较、默认穿透。PHP 没有模式匹配。

```php
<?php
$n = 7;
echo $n % 2 === 0 ? "even" : "odd", "\n";      // odd

switch ($n) {                                   // 松散比较 + 穿透
    case 1: echo "one\n"; break;
    case 2:
    case 3: echo "two-or-three\n"; break;
    default: echo "other\n";                     // other
}

echo match (true) {                              // match 是表达式，严格比较
    $n > 10 => "big\n",
    $n > 5 => "medium\n",                        // medium
    default => "small\n",
};

echo match (2) {
    1, 2 => "one-or-two\n",                      // 多值分支
    default => "other\n",                        // one-or-two
};

$v = null;
echo $v ?? "default", "\n";                       // default（?? 只判 null）
echo $v ?: "falsy", "\n";                         // falsy（?: 判所有假值）
echo 0 == "abc", "\n";                            // 空（PHP 8 起 0 == "abc" 为 false）
```

`match` 与 `switch` 的三点区别值得记牢：`match` 用 `===` 比较而 `switch` 用 `==`（PHP 8 起字符串与数字的比较规则收紧了，但松散比较仍然容易出意外）；`match` 没有匹配又没有 `default` 会抛 `UnhandledMatchError`，`switch` 则默默什么都不做；`match` 是表达式，可以直接嵌进赋值或函数调用，`switch` 是语句。`??` 只对 `null` 生效，`?:` 对所有假值生效，这是两个运算符最容易被混淆的地方。⚠️ `match` 的分支自上而下求值，第一个匹配的条件胜出，所以条件重叠时要按从特殊到一般排列。

📘 [PHP · match](https://www.php.net/manual/en/control-structures.match.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的分支工具是这一组里最丰富的：`if`/`unless`/`elsif`、语句修饰符（`puts "big" if n > 5`）、三元运算符、`case/when`，以及 3.0 起正式的结构化模式匹配 `case/in`。`case/when` 用 `===` 比较，所以区间、类、正则、Lambda 都能直接当分支条件；`case/in` 支持数组模式、哈希模式、查找模式与绑定，还能加守卫。Ruby 没有 `switch`。

```ruby
n = 7
puts n.even? ? "even" : "odd"            # odd
puts "big" if n > 5                       # big（语句修饰符）
puts "small" unless n > 5                 # 不输出（unless 是 if 的反面）

case n                                    # case/when 用 === 比较
when 1 then puts "one"
when 2, 3 then puts "two-or-three"
when 4..10 then puts "medium"             # medium（区间用 === 匹配）
when Integer then puts "int"
else puts "other"
end

case { name: "Ruby", year: 1995 }         # case/in 模式匹配
in { name: String => name, year: Integer => year } if year < 2000
  puts "#{name} is old"                   # Ruby is old
in [Integer => a, Integer => b]
  puts "pair #{a},#{b}"
else
  puts "unknown"
end
```

`case/when` 的 `===` 语义让它比大多数语言的 `switch` 强：`when 4..10` 匹配区间，`when String` 匹配类，`when /ab/` 匹配正则，`when ->(x) { x > 5 }` 还能匹配 Lambda。`case/in` 则是真正的解构匹配，哈希模式要求键存在（除非写 `**rest`），数组模式对长度敏感（`[*rest]` 才允许变长），`in` 失败会继续尝试下一个分支、全部失败且没有 `else` 就抛 `NoMatchingPatternError`；另外 `=>` 只做捕获不做检查，`in` 才做匹配。⚠️ 语句修饰符形式的 `if`/`unless` 优先级很低，`a = b if c` 里的赋值不受条件影响，写复合表达式时要加括号。

📘 [Ruby · Pattern matching](https://docs.ruby-lang.org/en/master/syntax/pattern_matching_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 循环

循环的分歧有三处：**有没有 C 风格三段式 `for`**（Rust、Swift、Kotlin、Python、Ruby、Zig 都取消了，Go、C、C++、Java、C#、Dart、TS/JS、PHP、Lua 保留）、**遍历是协议还是语法**（Rust 的 `IntoIterator`、Go 的 `range`、JS 的 `Symbol.iterator`、Python 的可迭代对象、Ruby 的 `each`+块），以及**循环变量的作用域**（Go 1.22 之前的所有迭代共用一个变量，R 的循环变量在循环结束后仍然存在，Lua 5.5 起循环变量是只读的）。有函数式传统的语言（Python、Julia、R、Ruby、TS/JS）还会告诉你：能用推导式、生成器或 `apply` 家族表达的，就别手写循环。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 只有 `for`、`while`、`while let` 和 `loop` 四种循环，没有 C 风格三段式 `for`。`for` 的右边必须是 `IntoIterator`：写 `for x in v` 会移动 `v`、`for x in &v` 借用、`for x in v.iter()` 明确借用；要索引就用 `enumerate()` 或 `(0..n)`。`loop` 是唯一能在 `break` 上带值的循环，也是「至少执行一次、最后统一返回」的惯用法。

```rust
fn main() {
    let v = vec![10, 20, 30];
    for (i, x) in v.iter().enumerate() { print!("{i}:{x} "); }   // 0:10 1:20 2:30
    println!();
    let mut stack = vec![1, 2, 3];
    while let Some(top) = stack.pop() { print!("{top} "); }      // 3 2 1
    println!();
    for i in (0..10).step_by(3) { print!("{i} "); }               // 0 3 6 9
    println!();
    let sum: i32 = v.iter().sum();
    println!("{sum}");                                            // 60
    let mut c = 0;                                                // 没有 C 风格 for
    while c < 3 { c += 1; }
    println!("{c}");                                              // 3
    let mut n = 0;
    let r = loop { n += 1; if n == 3 { break n * 7; } };          // loop 可带值 break
    println!("{r}");                                              // 21
}
```

`for` 循环的三种所有权形式决定了能否在循环里修改或再次使用集合：`for x in v` 消费集合，`for x in &v` 只借出不可变引用，`for x in &mut v` 借出可变引用因而可以原地修改元素。`while let` 是「只要模式还能匹配就继续」的循环，常用于消费 `Option`、迭代器或栈式结构，与 `if let` 的关系正如 `while` 与 `if`。⚠️ 没有 `Iterator` 的类型不能直接 `for`，但实现了 `IntoIterator` 的都可以；在 `for` 里修改被借用的集合会被借用检查器拦住，需要先收集要改的索引或用 `retain`/`iter_mut`；`loop` 里所有 `break` 的值的类型必须一致，否则编译器要求你补类型标注。

📘 [Rust By Example · Loops](https://doc.rust-lang.org/rust-by-example/flow_control/for.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的循环是 `for-in`、`while`、`repeat-while`，没有 C 风格三段式 `for`（Swift 3 就移除了）。`for-in` 遍历任何 `Sequence`，索引用 `enumerated()` 或 `indices`，等差数列用 `stride(from:to:by:)`（右开）与 `stride(from:through:by:)`（右闭）；`repeat-while` 是后测试循环，保证至少执行一次。Swift 6.4 起 `for-in` 还能遍历 `Span`、`InlineArray` 这类不可复制类型。

```swift
let xs = [10, 20, 30]
var sum = 0
for x in xs { sum += x }                        // for-in
print(sum)                                       // 60
for (i, x) in xs.enumerated() { print(i, x, terminator: " ") }
print()                                          // 0 10 1 20 2 30
for i in stride(from: 0, through: 10, by: 5) { print(i, terminator: " ") }
print()                                          // 0 5 10
for i in (1...3).reversed() { print(i, terminator: " ") }
print()                                          // 3 2 1
var n = 0
while n < 3 { n += 1 }
print(n)                                         // 3
repeat { n += 1 } while n < 5                    // repeat-while 至少一次
print(n)                                         // 5
```

`for-in` 的循环常量在每一轮都是新的绑定，所以闭包捕获它不会互相覆盖——这一点和 Go 1.22 之后的行为一致，而 Go 1.22 之前正好相反。`stride` 返回的是 `StrideTo`/`StrideThrough` 序列，仍然惰性，`by:` 的符号决定递增还是递减，写 `0` 会在运行时触发断言。⚠️ 想用 C 风格 `for (i = 0; i < n; i++)` 的写法在 Swift 里必须改成 `for i in 0..<n`（左闭右开）或 `0...n`（闭区间），而 `0...n` 在 `n` 为 `-1` 时会崩溃，所以数组下标一律用 `0..<xs.count` 或 `xs.indices`；`while` 里如果要修改被遍历的集合，请先用 `Array(xs)` 做快照。

📘 [Swift · Control Flow](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/controlflow/#For-In-Loops)

{{% /tab %}}

{{% tab header="Go" %}}

Go 只有 `for` 一个循环关键字，它承担了 `while`、`do-while`（用 `for` 加 `break` 模拟）与无限循环的全部职责：`for init; cond; post` 是三段式，`for cond` 是 while，`for {}` 是无限循环。`range` 用于数组、切片、字符串、map、channel，Go 1.22 起还能 `range` 整数，Go 1.23 起能 `range` 迭代器函数。1.22 起三条 `for` 形式里用 `:=` 声明的变量都是每次迭代新建。

```go
package main

import "fmt"

func main() {
	total := 0
	for i := 1; i <= 5; i++ {           // 三段式
		total += i
	}
	fmt.Println(total)                   // 15
	for total < 20 {                     // 只有条件 == while
		total += 5
	}
	fmt.Println(total)                   // 20
	sum, c := 0, 0
	for {                                // 无限循环
		c++
		if c == 3 {
			break
		}
		sum += c
	}
	fmt.Println(sum)                     // 3
	for i, v := range []int{10, 20} {     // range 给索引与值
		fmt.Println(i, v)                 // 0 10 / 1 20
	}
	for range 4 {                         // Go 1.22 起可以 range 整数
		fmt.Print("*")                    // ****
	}
	fmt.Println()
	fs := []func() int{}
	for _, v := range []int{1, 2, 3} {    // 1.22 起每次迭代新建 v
		fs = append(fs, func() int { return v })
	}
	fmt.Println(fs[0](), fs[1](), fs[2]()) // 1 2 3
}
```

Go 没有 `while`/`do-while` 关键字，`do { } while (cond)` 要写成 `for { ...; if !cond { break } }`，把判断挪到循环体末尾。`range` 的第二个返回值在只关心值时用 `_` 丢弃；`range` 一个 map 的顺序是随机的，需要稳定顺序就先取键排序。⚠️ Go 1.22 之前的代码里闭包捕获循环变量会共享同一个变量，所有闭包最后都读到最后一个值；如果你的 `go.mod` 里 `go` 指令低于 1.22，语义仍是旧的，升级需要显式改语言版本。另外 `range` 表达式只求值一次，循环中修改切片长度不会影响迭代次数。

📘 [Go spec · For 语句](https://go.dev/ref/spec#For_statements)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `for` 是纯粹的「对可迭代对象遍历」，没有 C 风格三段式，要计数就用 `range()`，要下标就 `enumerate()`，要多序列并行就 `zip()`。`while` 是唯一的条件循环，没有 `do-while`（惯用替代是 `while True:` 加 `break`）。列表、字典、集合、生成器推导式把「映射 + 过滤」压缩成一行，是 Python 里替代手写循环的首选。

```python
print([x * x for x in range(1, 6)])        # [1, 4, 9, 16, 25]
print([x for x in range(10) if x % 2])     # [1, 3, 5, 7, 9]
print({x: x * x for x in range(3)})        # {0: 0, 1: 1, 2: 4}
print(list(enumerate("abc")))              # [(0, 'a'), (1, 'b'), (2, 'c')]
print(list(zip([1, 2], [3, 4])))           # [(1, 3), (2, 4)]
for i, v in enumerate("ab"):
    print(i, v)                            # 0 a / 1 b
g = (x * x for x in range(3))              # 生成器表达式是惰性的
print(next(g), next(g), next(g))           # 0 1 4
print(sum(i for i in range(1, 101)))       # 5050
```

`range()` 返回的是惰性的 `range` 对象而不是列表，`range(10**9)` 不占内存；切片 `range(0, 10, 2)` 的第三个参数是步长，可以为负。推导式里的 `if` 是过滤、`for` 可以嵌套，但超过两层就该换成生成器函数，否则可读性急剧下降。⚠️ 遍历列表时删除元素会跳项，正确做法是遍历副本 `for x in list(xs)` 或反向索引；`for-else` 的 `else` 在循环正常结束（没有 `break`）时执行，命名容易误导但检查「没找到」很方便；`zip` 以最短序列为准，长度不等时会静默截断，`zip(..., strict=True)`（3.10 起）才会报错。

📘 [Python Tutorial · for 语句](https://docs.python.org/3/tutorial/controlflow.html#for-statements)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `for` 只能遍历「有迭代器的东西」：范围、数组、集合，没有 C 风格三段式。区间用 `a..b`，递减用 `downTo`，步长用 `step`，右开区间用 `until` 或 1.7.20 起预览、1.8.0 起稳定的 `..<`。`while` 与 `do-while` 保留，`repeat(n) { }` 是固定次数的简写，`indices`/`withIndex()`/`forEachIndexed` 负责索引。

```kotlin
fun main() {
    for (i in 1..5) print("$i ")                  // 1 2 3 4 5
    println()
    for (i in 5 downTo 1 step 2) print("$i ")      // 5 3 1
    println()
    for (i in 1 until 5) print("$i ")               // 1 2 3 4（不含 5）
    println()
    for (i in 1..<5) print("$i ")                   // 1 2 3 4（..< 等价写法）
    println()
    for ((i, c) in "abc".withIndex()) print("$i$c ")   // 0a 1b 2c
    println()
    val xs = listOf("a", "b")
    for (x in xs) print(x)                          // ab
    println()
    xs.forEachIndexed { i, x -> print("$i$x ") }     // 0a 1b
    println()
    var n = 0
    while (n < 3) n++                               // while
    do { n++ } while (n < 5)                        // do-while 至少一次
    println(n)                                      // 5
    repeat(3) { print("hi ") }                       // hi hi hi
    println()
}
```

`a..b` 是闭区间、`until` 与 `..<` 是右开区间，用错一个就会越界或漏掉最后一个元素，数组遍历推荐 `for (i in xs.indices)`；`downTo` 与 `step` 都返回 `Progression`，可以链式组合但 `step` 必须为正数。`forEach`/`forEachIndexed` 是 inline 函数，因此在其中使用 `return` 是「非局部返回」（直接返回外层函数），从 2.2 起 `break`/`continue` 在 inline lambda 中也已稳定可用。⚠️ 在非 inline lambda（例如自己写的回调、`crossinline` 参数）里 `break`/`continue` 依然非法，只能改用 `for` 循环或 `return@label`；`repeat` 里的 `it` 是当前次数（从 0 开始），别与 `forEach` 的 `it` 混淆。

📘 [Kotlin · Control flow](https://kotlinlang.org/docs/control-flow.html#for-loops)

{{% /tab %}}

{{% tab header="Java" %}}

Java 保留了完整的四种循环：经典 `for`、增强 `for`（for-each）、`while`、`do-while`。增强 `for` 的右边必须是数组或者 `Iterable` 子类型，编译器负责调用迭代器；想拿索引只能自己计数、用 `IntStream.range`，或者改用 `forEach` 系列方法。`Iterable.forEach`（Java 8）与 `Stream.forEach` 接收 lambda，是集合遍历的另一种写法。

```java
import java.util.List;
import java.util.stream.IntStream;

public class Loops {
    public static void main(String[] args) {
        int sum = 0;
        for (int i = 1; i <= 5; i++) sum += i;        // 经典 for
        System.out.println(sum);                       // 15
        List<String> xs = List.of("a", "b");
        for (String x : xs) System.out.print(x);       // ab（增强 for）
        System.out.println();
        xs.forEach(x -> System.out.print(x + " "));     // a b（Iterable.forEach）
        System.out.println();
        int n = 0;
        while (n < 3) n++;                              // while
        System.out.println(n);                          // 3
        do { n++; } while (n < 5);                      // do-while 至少一次
        System.out.println(n);                          // 5
        for (;;) { n++; if (n == 8) break; }             // 无限循环
        System.out.println(n);                          // 8
        IntStream.range(0, 3).forEach(i -> System.out.print(i));   // 012
        System.out.println();
    }
}
```

经典 `for` 的三个部分都可以为空（`for (;;)` 就是无限循环），初始化与更新部分可以用逗号写多条语句；增强 `for` 与迭代器版本在语义上等价，但增强 `for` 不能在遍历时安全地结构性修改集合（会抛 `ConcurrentModificationException`），要删除元素就用显式 `Iterator.remove()` 或 `removeIf`。⚠️ 增强 `for` 遍历数组时拿到的是副本，修改循环变量不会写回数组（遍历对象数组时改对象属性才会生效）；`forEach` 里的 `return` 只是跳过当前元素（相当于 `continue`），不能用它退出循环。

📘 [Java Tutorial · for 语句](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/for.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有经典 `for`、范围 `for`（C++11）、`while`、`do-while`。范围 `for` 能遍历任何提供 `begin()`/`end()` 的类型：原生数组、标准容器、初始化列表、C++20 的 `std::ranges` 视图；要修改元素就写 `auto&`，只读又不想拷贝就写 `const auto&`。C++20 起范围 `for` 还能带初始化语句。

```cpp
#include <cstdio>
#include <vector>
int main() {
    std::vector<int> v{1, 2, 3};
    int sum = 0;
    for (int x : v) sum += x;                        // 范围 for（C++11）
    std::printf("%d\n", sum);                        // 6
    for (auto& x : v) x *= 2;                        // 引用可修改元素
    std::printf("%d %d %d\n", v[0], v[1], v[2]);     // 2 4 6
    for (int i = 0; auto x : v) { (void)i; (void)x; } // C++20：范围 for 带初始化语句
    for (int i = 0; i < 3; i++) std::printf("%d ", i);
    std::printf("\n");                                // 0 1 2
    int n = 0;
    while (n < 3) n++;
    do { n++; } while (n < 5);                        // do-while 至少一次
    std::printf("%d\n", n);                           // 5
    for (;;) { if (n++ > 6) break; }                   // 无限循环
    std::printf("%d\n", n);                           // 8
}
```

范围 `for` 展开后是 `auto&& __range = range-init; auto __begin = begin(__range); auto __end = end(__range);`，所以临时容器会被延长生命周期、循环期间修改容器导致迭代器失效仍是未定义行为。写 `for (auto x : v)` 会逐元素拷贝，对大对象应当写成 `const auto&`；这也是 clang-tidy 的 `performance-for-range-copy` 检查盯的东西。⚠️ 范围 `for` 的初始值表达式只求值一次，因此 `for (auto x : makeVector())` 是安全的，但 `for (auto x : v) v.push_back(x)` 会因迭代器失效而崩溃；`do-while` 结尾的分号不能省，这是编译器最容易报出「expected ';'」的地方。

📘 [cppreference · 范围 for](https://en.cppreference.com/w/cpp/language/range-for)

{{% /tab %}}

{{% tab header="C" %}}

C 的循环只有三种：`for`、`while`、`do-while`。没有范围 `for`、没有 `foreach`、没有 `range`，遍历数组必须自己管索引或者用指针算术。`for` 的三个部分都可以省略，`for (;;)` 就是标准写法里的无限循环；`do-while` 是唯一的后测试循环，保证循环体至少执行一次。

```c
#include <stdio.h>
int main(void) {
    int total = 0;
    for (int i = 1; i <= 5; i++) total += i;      /* C 风格 for */
    printf("%d\n", total);                         /* 15 */
    int xs[] = {10, 20, 30};
    for (size_t i = 0; i < sizeof xs / sizeof xs[0]; i++)
        printf("%d ", xs[i]);
    printf("\n");                                  /* 10 20 30 */
    int *p = xs;                                   /* 指针版遍历 */
    for (int n = 3; n > 0; n--, p++) printf("%d ", *p);
    printf("\n");                                  /* 10 20 30 */
    int k = 0;
    while (k < 3) k++;                             /* while */
    printf("%d\n", k);                             /* 3 */
    do { k++; } while (k < 5);                     /* do-while 至少一次 */
    printf("%d\n", k);                             /* 5 */
    for (;;) { if (k++ > 6) break; }                /* 无限循环 */
    printf("%d\n", k);                             /* 8 */
    return 0;
}
```

`for` 的初始化部分在 C99 起允许声明变量（`for (int i = ...)`），该变量的作用域仅限于循环；`sizeof xs / sizeof xs[0]` 是只有数组可见时才能用的元素个数技巧，一旦数组退化成指针就失效，所以函数参数里必须额外传长度。⚠️ C 没有迭代器失效这层保护，`for (i = 0; i < n; i++)` 里改 `n` 会立即影响循环条件；`while ((c = getchar()) != EOF)` 这类赋值加比较必须加括号，否则优先级会让条件恒真；`for` 的第三个表达式里用逗号运算符可以更新多个变量，但可读性差，多数风格指南建议避免。

📘 [cppreference · C for 语句](https://en.cppreference.com/w/c/language/for)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `for` 遍历任何可迭代对象：`1:5` 这样的范围、数组、字典、生成器。索引遍历推荐 `eachindex(A)`（对任意维度和任意索引类型都正确），要值和下标用 `enumerate` 或 `pairs`，多序列并行用 `zip`。`while` 是条件循环，没有 `do-while`；推导式与生成器表达式是替代手写循环的首选，它们默认惰性且能自动做类型推断。

```julia
total = 0
for i in 1:5
    total += i
end
println(total)                        # 15

A = [10, 20, 30]
for i in eachindex(A)                 # 通用索引遍历
    print(A[i], " ")                  # 10 20 30
end
println()
for (i, v) in enumerate(A)            # 值与序号
    print("$i:$v ")                   # 1:10 2:20 3:30
end
println()
for (a, b) in zip([1, 2], [3, 4])     # 并行遍历
    print(a + b, " ")                 # 4 6
end
println()

println([x^2 for x in 1:5])            # [1, 4, 9, 16, 25]（推导式）
println(sum(x^2 for x in 1:100))       # 338350（生成器，不建数组）
g = (x^2 for x in 1:3)                 # 生成器是惰性的
println(collect(g))                    # [1, 4, 9]

n = 0
while n < 3
    global n += 1                      # 顶层作用域里需要 global
end
println(n)                             # 3
```

`for i in 1:3` 与 `for i = 1:3` 完全等价，`in`/`∈` 只是写法差异；`for i = 1:2, j = 3:4` 会按笛卡尔积展开，而且一个 `break` 会退出整个嵌套（不是只退出内层），需要只跳内层就得用 `continue` 或把内层包成函数。`eachindex` 比 `1:length(A)` 更正确，因为偏移数组与多维数组的下标并不从 1 开始或者不是线性区间。⚠️ 在脚本顶层写 `for` 时循环体有自己的作用域，想改外层变量要写 `global`（在函数里则直接可见）；推导式里的变量不会泄漏到外面，`for` 循环的变量也不会，但 `if` 块与 `begin` 块不引入新作用域（`while` 和 `try` 与 `for` 一样是 soft scope）。

📘 [Julia · Control Flow](https://docs.julialang.org/en/v1/manual/control-flow/#for-Loops-1)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的循环有 `for`、`foreach`、`while`、`do-while`。`foreach` 不是语法糖绑死接口：只要类型有公共无参 `GetEnumerator()`（C# 9 起可以是扩展方法），且返回类型有公共 `Current` 与返回 `bool` 的无参 `MoveNext()` 就能遍历，这让 `foreach` 也能作用于 `Span<T>`、`ReadOnlySpan<T>` 与自定义结构体，且不产生装箱。要索引就用 `for` 或 LINQ 的 `Select((x, i) => ...)`。

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Loops {
    static void Main() {
        int sum = 0;
        for (int i = 1; i <= 5; i++) sum += i;      // C 风格 for
        Console.WriteLine(sum);                      // 15
        var xs = new List<string> { "a", "b" };
        foreach (var x in xs) Console.Write(x);       // ab
        Console.WriteLine();
        foreach (var (x, i) in xs.Select((x, i) => (x, i)))
            Console.Write($"{i}{x} ");                // 0a 1b
        Console.WriteLine();
        int n = 0;
        while (n < 3) n++;                            // while
        do { n++; } while (n < 5);                    // do-while 至少一次
        Console.WriteLine(n);                         // 5
        foreach (var i in Enumerable.Range(0, 3)) Console.Write(i);  // 012
        Console.WriteLine();
        ReadOnlySpan<char> span = "hi";               // 结构体枚举器，零装箱
        foreach (var c in span) Console.Write(c);      // hi
        Console.WriteLine();
    }
}
```

`foreach` 的枚举器如果是结构体就完全不做堆分配，这是 `Span<T>` 与集合表达式在性能敏感代码里被推荐的原因；如果是引用类型的枚举器则每次循环可能产生一次分配（`List<T>` 的枚举器是结构体，代价只是一次拷贝）。⚠️ `foreach` 期间不能结构性修改被遍历的集合，`List<T>` 会抛 `InvalidOperationException`；`for` 与 `foreach` 的性能差异在现代 .NET 里通常可忽略，选可读性更好的那个；在 `foreach` 里用 `ref` 变量（`foreach (ref var x in span)`）才能真正原地修改元素。

📘 [MS Learn · 迭代语句](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/iteration-statements)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的循环有 `for`（C 风格）、`for-in`、`while`、`do-while`。`for-in` 遍历任何 `Iterable`，索引用 `.indexed`（3.0 起）、`.asMap()` 或经典计数；`Iterable.generate` 与 `List.generate` 负责造序列。`foreach` 不是关键字，对应的是集合的 `forEach` 方法，它接收回调。

```dart
void main() {
  var sum = 0;
  for (var i = 1; i <= 5; i++) sum += i;        // C 风格 for
  print(sum);                                    // 15
  var xs = ['a', 'b'];
  for (var x in xs) { print(x); }                // a / b
  for (var i = 0; i < xs.length; i++) print(xs[i]);   // a / b
  var n = 0;
  while (n < 3) n++;                             // while
  do { n++; } while (n < 5);                     // do-while 至少一次
  print(n);                                      // 5
  xs.forEach((x) => print(x));                    // a / b
  for (var i in Iterable.generate(3)) print(i);    // 0 / 1 / 2
  for (final (i, x) in xs.indexed) print('$i$x');  // 0a / 1b
}
```

`for-in` 的循环变量是元素的值绑定（元素对象本身可以修改，但遍历期间不能增删集合结构），`forEach` 的回调里 `return` 只结束当前回调、`break`/`continue` 是语法错误，要提前退出就用 `for-in` 加 `break`。`.indexed` 返回 `(int, T)` 记录，配合记录解构可以在循环头里一次拿到下标与值。⚠️ 遍历 `List` 时增删元素会抛 `ConcurrentModificationError`，需要过滤就先 `where(...).toList()`；`Iterable.generate` 默认无限，必须配 `.take(n)` 或显式给长度参数；Web 平台上 `int` 会退化成 JS 的 number，超大计数循环要注意精度。

📘 [Dart · Loops](https://dart.dev/language/loops)

{{% /tab %}}

{{% tab header="R" %}}

R 的循环只有 `for`、`while`、`repeat` 三种，`for` 遍历的是向量或列表的元素而不是索引序列；`break`/`next` 只能作用于最内层循环，没有标签。R 的循环慢是出了名的，惯用做法是用向量化运算或 `apply` 家族（`lapply`、`sapply`、`vapply`、`mapply`、`tapply`）替代显式循环——同一件事用向量化表达通常快一个数量级，代码也更短。

```r
total <- 0
for (i in 1:5) total <- total + i
print(total)                              # [1] 15

v <- c(1, 2, 3)
print(v * 2)                              # [1] 2 4 6（向量化替代循环）
print(sapply(v, function(x) x * x))        # [1] 1 4 9
print(vapply(v, function(x) x * x, numeric(1)))   # [1] 1 4 9（带类型检查）
print(Reduce(`+`, v))                      # [1] 6
print(sum(v))                              # [1] 6

i <- 0
while (i < 3) i <- i + 1                   # while
print(i)                                   # [1] 3
repeat { i <- i + 1; if (i >= 3) break }    # repeat 是后测试循环
print(i)                                   # [1] 4（i 已是 3，repeat 至少再加一次）

for (x in 1:3) NULL
print(x)                                   # [1] 3（循环变量在循环后仍存在）
print(for (y in 1:3) y)                    # NULL（for 返回 NULL，不可见）
```

`for` 的循环变量在循环结束后依然留在当前环境里，并且等于最后一个元素的值（空向量时是 `NULL`），这对交互式调试方便，对函数代码则是隐患。`sapply` 会尝试把结果简化成向量或矩阵，类型不确定时改用 `vapply` 并显式给出返回类型的模板，这样返回类型不对会直接报错而不是默默转成列表。⚠️ 用 `for` 累积结果时不要 `c()` 追加（每次复制整个向量，复杂度平方），要预分配 `vector("list", n)` 再按下标赋值；`1:length(v)` 在 `v` 为空时会得到 `c(1, 0)` 导致越界，必须写 `seq_along(v)`。

📘 [R Language Definition · for 循环](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#for-loops)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 只有 `while` 和 `for`，没有 C 风格三段式、也没有 `do-while`。`while` 可以带 continue 表达式（写在冒号后面），它在每一轮结束、包括 `continue` 之后执行，但 `break` 之后不执行；`for` 用来遍历数组、切片与范围，可以同时拿元素与索引，但不支持 continue 表达式。两者都支持 `inline` 版本，让循环在编译期完全展开。

```zig
const std = @import("std");
pub fn main() void {
    var i: usize = 0;
    while (i < 5) : (i += 1) {            // continue 表达式：每轮结束执行
        if (i == 2) continue;             // continue 会先执行 i += 1
        std.debug.print("{d} ", .{i});     // 0 1 3 4
    }
    std.debug.print("\n", .{});

    const xs = [_]i32{ 10, 20, 30 };
    var sum: i32 = 0;
    for (xs, 0..) |x, idx| {              // 同时拿值与索引
        _ = idx;
        sum += x;
    }
    std.debug.print("{d}\n", .{sum});      // 60

    for (0..3) |n| {                      // for 也能遍历范围
        std.debug.print("{d} ", .{n});     // 0 1 2
    }
    std.debug.print("\n", .{});

    var j: usize = 0;
    outer: while (true) : (j += 1) {       // 无 C 风格 for 的无限循环
        if (j == 3) break :outer;          // 带标签退出
    }
    std.debug.print("{d}\n", .{j});        // 3

    inline for (0..2) |n| {                // 编译期展开，n 必须是 comptime 可知
        _ = n;
    }
}
```

`while (cond) : (expr)` 的 continue 表达式让「索引自增」不必写在循环体末尾，也不会被 `continue` 跳过，这是 Zig 里最容易写错的语义之一：写成 `while (i < n)` 然后在体尾 `i += 1`，一旦 `continue` 就死循环。`for (slice, 0..) |item, idx|` 里的 `0..` 是索引来源，不写它就拿不到索引；对多参数容器 `for (a, b) |x, y|` 会按最短长度并行遍历。⚠️ Zig 的循环变量是不可变的，想修改元素要用指针解引用（`for (xs) |*p| p.* += 1`）；`inline while`/`inline for` 的循环次数必须编译期可知，否则报错；超过一层的嵌套循环要退出必须用标签 `break :outer`。

📘 [Zig · while 与 for](https://ziglang.org/documentation/master/#while)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 有四种循环：数值 `for`、泛型 `for`、`while`、`repeat-until`（后测试循环）。数值 `for` 是 `for i = 初值, 限值, 步长`，三个表达式只求值一次，步长为 0 会报错；泛型 `for` 是 `for k, v in 迭代函数, 状态, 初值`，实际求值出四个值，第四个是 to-be-closed 关闭值。Lua 5.5 起两种 `for` 的控制变量都是只读（`const`）的。

```lua
-- 数值 for：三个表达式只求值一次
for i = 1, 5 do io.write(i, " ") end
print()                                       -- 1 2 3 4 5
for i = 10, 1, -3 do io.write(i, " ") end
print()                                       -- 10 7 4 1

-- Lua 5.5 起控制变量只读
for i = 1, 3 do
  -- i = i + 1        -- 🛑 报错：控制变量是 read-only const
  local j = i + 1
  io.write(j, " ")                             -- 2 3 4
end
print()

-- 泛型 for：ipairs 依次给下标与值，pairs 给键
local t = { "a", "b", "c" }
for idx, v in ipairs(t) do io.write(idx, v, " ") end
print()                                        -- 1a 2b 3c
for k in pairs({ x = 1, y = 2 }) do io.write(k, " ") end
print()                                        -- x y 或 y x（pairs 顺序不保证）

-- while 与 repeat-until
local n = 0
while n < 3 do n = n + 1 end
print(n)                                       -- 3
repeat n = n + 1 until n >= 5                   -- 至少执行一次
print(n)                                       -- 5

-- 自定义迭代器：泛型 for 的协议就是"返回下一个值的函数"
local function upto(n)
  local i = 0
  return function() i = i + 1; if i <= n then return i end end
end
for v in upto(3) do io.write(v, " ") end
print()                                        -- 1 2 3
```

数值 `for` 的循环变量类型取决于初值与步长：两者都是整数时按整数循环，否则三个值都转成浮点，所以 `for i = 1, 3, 0.5` 的 `i` 是浮点。泛型 `for` 的第一个返回值是迭代函数，每次循环调用它并把上一个控制变量作为参数传回，返回 `nil` 时结束——这就是 Lua 的迭代协议，`ipairs`/`pairs` 只是预置实现。⚠️ 5.5 给控制变量加 `const` 之后，老代码里「在循环体里修改 `i` 来跳步」的写法直接报错，要在循环体里声明新 `local`；`pairs` 的顺序未定义，需要确定性顺序就先把键排好再遍历。

📘 [Lua 5.5 · for 语句](https://www.lua.org/manual/5.5/manual.html#3.3.5)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的循环就是 JavaScript 的那一套：`for`（三段式）、`for-in`（键）、`for-of`（值）、`while`、`do-while`，再加上数组的 `forEach`/`map`/`filter`/`reduce`。类型系统在这里能做的是给迭代结果加类型：`for-of` 的元素类型来自 `Iterable<T>`，`for-in` 的变量类型始终是 `string`，`.map` 的返回类型由回调推断。

```typescript
const arr: string[] = ["a", "b"];
for (const i in arr) console.log("in:", typeof i, i);  // in: string 0 / in: string 1
for (const v of arr) console.log("of:", typeof v, v);  // of: string a / of: string b
arr.forEach((v, i) => console.log(i, v));               // 0 a / 1 b
for (let i = 0; i < arr.length; i++) console.log(arr[i]);   // a / b

let n = 0;
while (n < 3) n++;
do { n++; } while (n < 5);                              // 至少一次
console.log(n);                                         // 5

const nums: number[] = [1, 2, 3];
const doubled = nums.map((x) => x * 2);                  // 映射优先于手写循环
console.log(doubled);                                    // [ 2, 4, 6 ]
console.log(nums.reduce((a, b) => a + b, 0));            // 6
```

`for-in` 与 `for-of` 的分工必须记清楚：`for-in` 枚举的是可枚举属性名（字符串），包括原型链上的，所以遍历数组得到的是 `"0"`、`"1"` 这样的字符串而不是值；`for-of` 走 `Symbol.iterator`，得到的是值，而且可以被 `break`/`continue` 正常打断。`forEach` 无法 `break`，也不能 `await` 后面的元素，需要提前退出就用 `for-of` 或者 `some`/`find`。⚠️ `for-in` 遍历数组时顺序不保证是数值序（对象属性顺序规则对整数键例外，但混入自定义属性后就乱了），一律不要用它遍历数组；`noUncheckedIndexedAccess` 未开启时 `arr[i]` 的类型不会带 `undefined`，开了才会，这会影响你写循环时的判空。

📘 [MDN · for...of](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/for...of)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的循环有 `for`、`for-in`、`for-of`、`while`、`do-while`，另有数组的 `forEach`/`map`/`filter`/`reduce`。`for-in` 枚举可枚举属性的**字符串键**（包含原型链上的），`for-of` 走 `Symbol.iterator` 拿**值**；两者名字只差一个字母，语义完全不同，是这门语言最常见的混淆点之一。

```javascript
const arr = ["a", "b"];
for (const i in arr) console.log("in:", typeof i, i);   // in: string 0 / in: string 1
for (const v of arr) console.log("of:", typeof v, v);   // of: string a / of: string b
const map = new Map([["k", 1]]);
for (const [k, v] of map) console.log(k, v);            // k 1
let n = 0;
while (n < 3) n++;                                      // while
console.log(n);                                         // 3
do { n++; } while (n < 5);                              // do-while 至少一次
console.log(n);                                         // 5
for (;;) { n++; if (n === 8) break; }                    // 无限循环
console.log(n);                                         // 8
arr.forEach((v, i) => console.log(i, v));                // 0 a / 1 b
```

`for-of` 适用于数组、字符串、`Map`、`Set`、`arguments`、`TypedArray` 以及任何实现了 `Symbol.iterator` 的对象，还能用 `for await...of` 消费异步可迭代对象；`for-in` 则主要用于遍历普通对象的键，而且会把原型链上可枚举的属性一起枚举出来，所以对象遍历更推荐 `Object.keys()`/`Object.entries()`。⚠️ `forEach` 里 `break` 或 `continue` 都是语法错误，`return` 只结束当前回调；遍历数组时新增元素不保证被访问到、删除元素可能跳项；`for-in` 遍历数组的下标是字符串，`arr[i]` 能用但 `i + 1` 会变成字符串拼接。

📘 [MDN · for...in](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/for...in)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的循环有 `for`、`foreach`、`while`、`do-while`。`foreach` 是遍历数组与任何 `Traversable` 对象的主力，语法 `foreach ($arr as $k => $v)` 同时拿键值；默认按值遍历，写 `as &$v` 才是引用遍历并且能原地修改数组——但循环后必须 `unset($v)`，否则残留的引用会污染后续同名赋值。

```php
<?php
$sum = 0;
for ($i = 1; $i <= 5; $i++) $sum += $i;       // C 风格 for
echo $sum, "\n";                                // 15

$xs = ['a' => 1, 'b' => 2];
foreach ($xs as $k => $v) echo "$k=$v ";        // a=1 b=2
echo "\n";

$nums = [1, 2, 3];
foreach ($nums as &$v) { $v *= 2; }             // 引用遍历可改原数组
unset($v);                                       // ⚠️ 必须断掉引用
echo implode(",", $nums), "\n";                  // 2,4,6

$n = 0;
while ($n < 3) $n++;                            // while
do { $n++; } while ($n < 5);                    // do-while 至少一次
echo $n, "\n";                                   // 5

foreach (range(1, 3) as $i) echo $i;             // 123
echo "\n";
```

`foreach` 操作的是数组的副本（写时复制），所以在循环里修改数组不会影响本轮遍历，这是 PHP 相对 C 系更安全的地方；要边遍历边改就必须用引用形式或按索引 `for`。`for` 的三个表达式都可以为空，`for (;;)` 是无限循环。⚠️ `foreach ($arr as $k => $v)` 里 `$k`、`$v` 在循环结束后仍然存在（作用域不限于循环）；不 `unset` 引用变量是 PHP 里最隐蔽的 bug 之一，第二次 `foreach ($arr as $v)` 会把值写到最后一次引用的位置上；`foreach` 对非数组非 `Traversable` 会告警并跳过，不会静默循环。

📘 [PHP · foreach](https://www.php.net/manual/en/control-structures.foreach.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的循环风格和其他语言差别最大：惯用写法是「集合 + 块」的迭代方法（`each`、`map`、`select`、`times`、`upto`、`downto`、`step`），`while`/`until` 用于条件循环，`for` 只是 `each` 的语法糖。`for` 与 `each` 的实质差别是作用域：`for` 不会创建新的作用域，循环变量会泄漏到外层；`each` 的块变量则不会。

```ruby
1.upto(3) { |i| print i }                       # 123
print "\n"
1.step(10, 3) { |i| print i, " " }               # 1 4 7 10
print "\n"
i = 0
loop do                                          # Kernel#loop 是无限循环
  i += 1
  break if i == 3
end
puts i                                           # 3
for x in [1, 2, 3] do print x end                # for 是 each 的语法糖
print "\n"
puts x.inspect                                   # 3（for 的变量泄漏到外层）
puts (1..4).map { |n| n * n }.inspect            # [1, 4, 9, 16]
acc = []
[10, 20].each_with_index { |v, idx| acc << [idx, v] }
puts acc.inspect                                 # [[0, 10], [1, 20]]
```

`each` 返回接收者本身、`map` 返回新数组、`select`/`reject` 过滤、`reduce`/`inject` 归约，这套组合基本覆盖了手写循环的全部用途。`while` 与 `until` 的返回值默认是 `nil`，但用 `break 值` 可以让循环整体求值为那个值。⚠️ `for` 的循环变量泄漏是真实的作用域差异（块变量不会），风格指南（RuboCop 的 `Style/For`）普遍建议禁用 `for`；在块里 `break` 退出的是「调用这个方法的那一层」而不是块本身，`next` 相当于 `continue`，`return` 从外层方法返回——三者在块与 lambda 里的语义还不一样（lambda 里 `return` 只退出 lambda）。

📘 [Ruby · Control expressions](https://docs.ruby-lang.org/en/master/syntax/control_expressions_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}


### 跳转与提前退出

`break`、`continue`、`return`、`throw` 这四件套人人都有，差异藏在三个地方：**能不能一次跳出多层循环**（C、C++、PHP、Go 靠 `goto`，Java、Kotlin、Swift、Rust、TypeScript/JavaScript、Dart、Zig 靠标签，Python、R 只能靠 `return` 或标志变量）、**`break` 能不能带回一个值**（Rust 的 `loop`、Ruby 的 `while` 与块可以，Java、C、Go 不行）、**非局部退出用什么机制**（Ruby 有 `catch`/`throw` 与 `redo`/`retry`，Lua 用 `error` 加 `pcall`，Go 用 `panic`/`recover`，R 用 `tryCatch`）。Python 的 `for-else`/`while-else` 是这一节里最独特的一个：它把「循环有没有被 `break` 打断」变成了可查询的状态。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的跳转是 `break`、`continue`、`return` 和 `?` 运算符，没有 `goto`。多层循环用生命周期风格的标签 `'outer:` 配合 `break 'outer` 与 `continue 'outer`；`loop` 是唯一能通过 `break 值` 产出值的循环；错误传播用 `?` 而不是异常，`panic!` 只用于「不该发生」的情况。

```rust
fn parse(s: &str) -> Result<i32, std::num::ParseIntError> {
    let n: i32 = s.parse()?;                 // ? 提前返回 Err
    Ok(n * 2)
}

fn main() {
    let mut n = 0;
    'outer: for _a in 1..=3 {
        for b in 1..=3 {
            if b == 2 { continue 'outer; }    // 跳过外层本轮剩余
            n += 1;
        }
    }
    println!("{n}");                          // 3
    println!("{:?}", parse("21"));             // Ok(42)
    println!("{}", parse("x").is_err());        // true
    let r = loop { break 7; };                 // loop 带值 break
    println!("{r}");                           // 7
}
```

标签写在循环前面并带一个单引号，用的是生命周期语法，所以标签不能与泛型参数重名。`break 'outer` 与 `continue 'outer` 都指向被标记的那层循环，这是 Rust 里唯一的多层退出手段；`break 值` 只在 `loop` 里合法，`for`/`while` 的 `break` 不能带值，需要返回值的条件循环要写成 `loop { ...; if cond { break v; } }`。⚠️ `?` 只能用在返回 `Result`/`Option` 的函数里，写进 `main` 要把返回类型改成 `Result<(), E>` 或就地 `match`；`panic!` 默认展开栈、可以用 `panic = "abort"` 改成直接中止，它能被 `catch_unwind` 拦住但不应作为常规控制流。

📘 [Rust Reference · loop 与 break](https://doc.rust-lang.org/reference/expressions/loop-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的跳转有 `break`、`continue`、`return`、`throw`、`fallthrough` 和 `guard`。带标签的语句写成 `outer: for ...`，可以 `break outer` 或 `continue outer`；`switch` 不需要 `break`，要穿透必须显式写 `fallthrough`；`guard` 是「条件不成立就离开当前作用域」的写法，比层层嵌套 `if` 更平坦。

```swift
import Foundation
var sum = 0
outer: for a in 1...3 {
    for b in 1...3 {
        if b == 2 { continue outer }      // 标签 + continue
        sum += a
    }
}
print(sum)                                 // 6
var m = 0
loop: for a in 0..<3 {
    for b in 0..<3 {
        if a == 1 && b == 1 { break loop }  // 标签 + break
        m += 1
    }
}
print(m)                                   // 4
switch 2 {
case 1: print("one")
case 2: print("two"); fallthrough          // 显式穿透
default: print("and more")                 // two / and more
}
func g(_ v: Int?) throws -> Int {
    guard let v else { throw NSError(domain: "x", code: 1) }
    return v * 2                           // guard 通过后 v 仍然可用
}
print(try g(3))                            // 6
defer { print("cleanup") }                 // 离开作用域时逆序执行
print("body")                              // body
```

`guard` 的 `else` 块必须离开当前作用域（`return`、`break`、`continue`、`throw` 或 `fatalError()`），它绑定出来的变量在 `guard` 之后继续可用，这正是它比 `if let` 更适合做前置校验的原因。`defer` 按后进先出顺序执行，即使函数因 `throw` 提前退出也会执行，因此常用来释放文件句柄、恢复状态；Swift 6.4 起 `defer` 块里也能写异步代码。⚠️ `fallthrough` 只能出现在 `case` 里而且不能是最后一个 `case`，它直接进入下一个分支的代码而不再匹配条件，所以不能与值绑定模式连用；`try` 必须写在调用点，忽略错误用 `try?`（得到 `Optional`）、确定不会错用 `try!`（出错即崩溃）。

📘 [Swift · Control Flow](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/controlflow/#Control-Transfer-Statements)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的跳转语句只有 `break`、`continue`、`goto`、`fallthrough` 和 `return`，没有异常；错误通过返回值传递，真正不可恢复的情况用 `panic` 加 `defer` 里的 `recover` 拦截。`break`/`continue` 可以带标签，标签必须写在某个外层 `for`/`switch`/`select` 之前，而且与跳转语句在同一函数内；`goto` 也能跳，但不允许跳过变量声明进入其作用域。

```go
package main

import "fmt"

func main() {
outer:
	for a := 1; a <= 3; a++ {
		for b := 1; b <= 3; b++ {
			if a*b == 4 {
				break outer // 带标签的 break
			}
		}
	}
	fmt.Println("done") // done
	i := 0
loop:
	if i < 2 {
		i++
		goto loop // 只能跳到同一函数内的标签
	}
	fmt.Println(i) // 2
	sum := 0
outer2:
	for a := 1; a <= 3; a++ {
		for b := 1; b <= 3; b++ {
			if b == 2 {
				continue outer2 // 跳到外层下一轮
			}
			sum++
		}
	}
	fmt.Println(sum) // 3
	func() {
		defer func() {
			if r := recover(); r != nil {
				fmt.Println("recovered:", r) // recovered: boom
			}
		}()
		panic("boom") // 没有 throw，panic 是最后手段
	}()
}
```

标签必须紧贴在要被标记的语句前，`break label` 的标签可以指向 `for`、`switch` 或 `select`，`continue label` 只能指向 `for`。`recover` 只在 `defer` 调用的函数里直接调用才有效，嵌套一层函数就失效；`panic` 会沿调用栈展开并执行所有 `defer`，未被 `recover` 时程序打印栈信息后以非零状态退出。⚠️ `fallthrough` 是唯一「不判断条件就进下一个 `case`」的语句，且只能用在表达式 `switch` 里、必须是该 `case` 的最后一条语句；`goto` 不能跳进 `for` 循环体或 `if` 块内部，也不能跳过一个变量声明，编译器会直接报错。

📘 [Go spec · Break/Continue/Goto](https://go.dev/ref/spec#Break_statements)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的跳转只有 `break`、`continue`、`return` 和 `raise`，没有 `goto`、没有标签跳转，多层循环要退出只能把循环装进函数再用 `return`，或者用标志变量。`raise` 是唯一的抛出机制，异常可以用 `try`/`except`/`else`/`finally` 完整处理；循环还额外带一个 `else` 子句：没有被 `break` 打断时执行。

```python
def classify(n):
    if n < 0:
        return "neg"           # return 提前退出
    if n == 0:
        return "zero"
    return "pos"

print(classify(-1), classify(0), classify(1))   # neg zero pos

for i in range(5):
    if i == 3:
        break
else:
    print("no break")          # 不输出：有 break

i = 0
while i < 3:
    i += 1
else:
    print("while-else")        # while-else

for i in range(6):
    if i % 2:
        continue                # continue 跳过本轮剩余
    print(i, end=" ")           # 0 2 4
print()

def load(x):
    try:
        if x < 0:
            raise ValueError("neg")
        return x * 2
    except ValueError as e:
        return f"err:{e}"
    finally:
        print("cleanup")        # 无论走哪条路径都输出
print(load(3))                  # cleanup / 6
print(load(-1))                 # cleanup / err:neg
```

`for-else` 的 `else` 属于循环而不是 `if`，它在循环正常耗尽时执行、被 `break` 打断时跳过；这个特性最常见的用法是「查找失败则报错」，避免额外设一个 `found` 标志。`try`/`except`/`else`/`finally` 中 `else` 在没抛异常时执行、`finally` 一定执行，连 `return` 也会先执行 `finally`。⚠️ `finally` 里再 `return` 会覆盖 `try` 里的返回值，这也是最容易被 lint 抓住的写法；`break`/`continue` 只能作用于最内层循环，需要跳出两层就把内层抽成函数或用异常（不推荐），进程级退出用 `sys.exit()`，它抛的是 `SystemExit` 而不是直接终止。

📘 [Python Tutorial · 循环中的 break/continue/else](https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 有 `break`、`continue`、`return`、`throw`，没有 `goto`，还多了一个 `return@label`：因为 lambda 的存在，「从哪里返回」需要显式说明。标签既可以标在循环上（`outer@ for`），也可以标在 lambda 上（`lit@{ }`）；2.2 起在 inline lambda 里直接 `break`/`continue` 已经稳定可用，而非 inline lambda 里仍然只能 `return@label`。

```kotlin
fun classify(n: Int): String {
    if (n < 0) return "neg"
    return if (n == 0) "zero" else "pos"
}

fun main() {
    println("${classify(-1)} ${classify(0)} ${classify(1)}")   // neg zero pos

    var n = 0
    outer@ for (a in 1..3) {                  // 循环标签
        for (b in 1..3) {
            if (b == 2) continue@outer         // 跳到外层下一轮
            n++
        }
    }
    println(n)                                 // 3

    listOf(1, 2, 3).forEach lit@{              // lambda 标签
        if (it == 2) return@lit                // 只结束本次 lambda
        print(it)                              // 13
    }
    println()

    run loop@{
        listOf(1, 2, 3).forEach {
            if (it == 2) return@loop            // 非局部返回：退出 run
            print(it)                           // 1
        }
    }
    println()

    for (i in 1..2) {
        run {
            if (i == 2) continue                // 2.2 起：inline lambda 里可 continue
            print(i)                            // 1
        }
    }
    println()
}
```

`return@forEach` 与 `return` 的区别是 Kotlin 里最容易踩的一处：前者只结束**当前这一次** lambda 调用（效果像 `continue`），后者是非局部返回、直接离开外层函数（效果像 `break` 加 `return`），而且只有 inline 函数支持非局部返回。`run`、`let`、`apply`、`also`、`with`、`forEach`、`repeat` 都是 inline 的，所以在它们里面 `return` 会穿透；自己写的普通 lambda 参数（或标了 `crossinline` 的）不能非局部返回，`break`/`continue` 也不行。⚠️ 循环标签与 lambda 标签同名时最近的那个生效，命名要避免重复；`throw` 在 Kotlin 里是表达式（类型 `Nothing`），可以写在 `?:` 右边，例如 `val x = v ?: throw IllegalArgumentException()`。

📘 [Kotlin · Returns and jumps](https://kotlinlang.org/docs/returns.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 有 `break`、`continue`、`return`、`throw`，`goto` 是保留字但从未实现；多层循环靠标签 `outer:` 加 `break outer`/`continue outer`。`break` 不能带值，`switch` 表达式的值用 `yield` 产出；`try`/`catch`/`finally` 与 try-with-resources 负责异常路径上的资源释放。

```java
public class Jumps {
    static String classify(int n) {
        if (n < 0) return "neg";
        if (n == 0) return "zero";
        return "pos";
    }

    static String label(int n) {
        return switch (n) {                  // switch 表达式
            case 1 -> "one";
            case 2 -> {
                yield "two";                  // 语句块里必须 yield
            }
            default -> "other";
        };
    }

    public static void main(String[] args) {
        System.out.println(classify(-1) + " " + classify(0) + " " + classify(1));  // neg zero pos
        int n = 0;
        outer:
        for (int a = 1; a <= 3; a++) {        // 标签单独一行
            for (int b = 1; b <= 3; b++) {
                if (b == 2) continue outer;    // 跳到外层下一轮
                n++;
            }
        }
        System.out.println(n);                 // 3
        int m = 0;
        search:
        for (int a = 0; a < 3; a++) {
            for (int b = 0; b < 3; b++) {
                if (a == 1 && b == 1) break search;
                m++;
            }
        }
        System.out.println(m);                  // 4
        System.out.println(label(2));            // two
        try {
            throw new IllegalStateException("boom");
        } catch (IllegalStateException e) {
            System.out.println("caught " + e.getMessage());   // caught boom
        } finally {
            System.out.println("finally");                    // finally
        }
    }
}
```

标签必须紧贴它要标记的语句，习惯上单独占一行；带标签的 `break`/`continue` 是 Java 里跳出多层循环的官方手段，比自己设标志位清晰得多。`finally` 总会在离开 `try` 时执行，包括 `return`、`break`、`continue` 与异常路径，但**不要**在 `finally` 里改返回值或再 `return`，那会静默覆盖结果。⚠️ `break` 与 `continue` 在 `switch` 里的含义不同：`break` 退出 `switch`，`continue` 作用于外层循环并跳过本轮剩余（在 `switch` 里写 `continue` 很容易看错）；`throw` 的参数必须是 `Throwable` 子类，`Error` 与 `RuntimeException` 是 unchecked、其它 checked 异常必须出现在方法签名里。

📘 [Java Tutorial · 分支语句](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/branch.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有 `break`、`continue`、`return`、`goto` 和 `throw`；没有带标签的 `break`，多层循环只能靠 `goto` 或把内层抽成函数。C++ 的独特之处在提前退出与资源释放的配合：栈展开（stack unwinding）会在 `throw` 或 `return` 时调用所有局部对象的析构函数，这就是 RAII 能替代 `finally` 的原因。

```cpp
#include <cstdio>
#include <stdexcept>
#include <vector>

int find(const std::vector<int>& xs, int target) {
    for (int i = 0; i < static_cast<int>(xs.size()); i++) {
        if (xs[i] == target) return i;      // return 提前退出
        if (xs[i] > target) break;           // break 只离开本层循环
    }
    return -1;
}

struct Guard {                               // RAII：提前退出也会执行析构
    ~Guard() { std::printf("cleanup\n"); }
};

int main() {
    std::vector<int> xs{1, 3, 5, 7};
    std::printf("%d %d\n", find(xs, 5), find(xs, 4));   // 2 -1
    int count = 0;
    for (int a = 1; a <= 3; a++) {
        for (int b = 1; b <= 3; b++) {
            if (a * b == 4) goto done;      // 没有标签 break，只能 goto
            count++;
        }
    }
done:
    std::printf("%d\n", count);              // 4
    try {
        Guard g;
        throw std::runtime_error("boom");    // 栈展开会调用析构
    } catch (const std::exception& e) {
        std::printf("caught %s\n", e.what()); // caught boom
    }
    return 0;
}
```

`goto` 的合法范围被严格限制：不能跳过初始化进入变量作用域（对带构造函数的类型尤其如此），但允许向后跳出循环与多重嵌套，并且会正确地调用离开作用域对象的析构函数。异常路径同样会展开栈，所以「提前 `return` 忘记释放」在 C++ 里基本不会发生——只要资源由对象持有；需要显式清理时用 `std::unique_ptr`、`std::lock_guard` 这类 RAII 包装，而不是在 `catch` 里手写 `delete`。⚠️ `break` 在 `switch` 里退出的是 `switch` 而不是外层循环，嵌套在循环里的 `switch` 想 `continue` 必须写在外层循环里或用 `goto`；`throw` 抛出的对象会被拷贝（除非抛的是指针或 `std::exception_ptr`），因此异常类型应当是可拷贝且构造简单的。

📘 [cppreference · goto 语句](https://en.cppreference.com/w/cpp/language/goto)

{{% /tab %}}

{{% tab header="C" %}}

C 的跳转只有 `break`、`continue`、`return`、`goto` 和 `setjmp`/`longjmp`，没有异常。`goto` 是 C 里唯一能一次跳出多层循环的手段，也是内核与库代码里做统一清理（`goto cleanup`）的标准写法；`break`/`continue` 只作用于最内层循环，`switch` 里的 `break` 退出的也是 `switch`。

```c
#include <stdio.h>

int find(const int *xs, int n, int target) {
    for (int i = 0; i < n; i++) {
        if (xs[i] == target) return i;    /* return 提前退出 */
        if (xs[i] > target) break;         /* break 只离开本层循环 */
    }
    return -1;
}

int main(void) {
    int xs[] = {1, 3, 5, 7};
    printf("%d\n", find(xs, 4, 5));         /* 2 */
    printf("%d\n", find(xs, 4, 4));         /* -1 */
    int count = 0;
    for (int a = 1; a <= 3; a++) {
        for (int b = 1; b <= 3; b++) {
            if (a * b == 4) goto done;      /* goto 是 C 里唯一的多层退出 */
            count++;
        }
    }
done:
    printf("%d\n", count);                  /* 4 */
    for (int i = 0; i < 5; i++) {
        if (i % 2 == 0) continue;           /* continue 跳过本轮剩余 */
        printf("%d ", i);                   /* 1 3 */
    }
    printf("\n");
    return 0;                               /* return 从 main 返回，即退出进程 */
}
```

`goto` 是标准的 C 语句，不是「坏味道」：在需要分配多份资源、失败时按相反顺序释放的场景里，`goto cleanup` 比层层嵌套 `if` 更不容易漏掉释放。C 的错误报告靠返回值或 `errno`，`setjmp`/`longjmp` 能做非局部跳转但会跳过栈上自动变量的清理与析构（C 里没有析构），几乎只用在解释器与协程这类特殊场合。⚠️ `goto` 不能跳进变长数组（VLA）的作用域，也不能跳进其它函数；`return` 从 `main` 返回等价于 `exit`，会刷新缓冲区并执行 `atexit` 注册的函数；`break` 在嵌套 `switch` 与循环里只退出一层，这是忘写 `break` 之外的另一个经典陷阱。

📘 [cppreference · C goto 语句](https://en.cppreference.com/w/c/language/goto)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 有 `break`、`continue`、`return`、`throw`，没有标签跳转；Base 额外提供宏 `@goto`/`@label` 作为 goto 的替代，但它们只能在同一顶层语句块内跳转（所以通常要把标签与跳转包进 `let` 或 `begin` 块）。异常用 `throw`/`error` 抛出，`try`/`catch`/`else`/`finally` 捕获，`return` 从函数返回，块的值是最后一条表达式的值。

```julia
function classify(n)
    n < 0 && return "neg"        # 短路 + return
    n == 0 && return "zero"
    "pos"                         # 最后一条表达式的值即返回值
end
println(classify(-1), " ", classify(0), " ", classify(1))   # neg zero pos

total = 0
for i in 1:10
    i > 5 && break                # break 只跳出最内层循环
    iseven(i) && continue          # continue
    total += i
end
println(total)                    # 9（1+3+5）

let                               # @goto 与 @label 必须同处一个块
    i = 0
    @label again
    i += 1
    i < 3 && @goto again
    println(i)                    # 3
end

try
    error("boom")                  # error() 抛 ErrorException
catch e
    println(typeof(e))             # ErrorException
finally
    println("finally")              # finally
end
```

`&&` 与 `||` 在 Julia 里是短路求值，所以 `cond && return x` 就是一行版的条件返回，比先写 `if` 再写 `return` 更紧凑；`for` 循环体引入的是 soft scope，在函数里对已存在的局部变量赋值会更新外层那个变量，脚本顶层则必须先 `global`（`while`、`try` 同样是 soft scope，只有 `if`/`begin` 块不引入新作用域）。`@goto`/`@label` 是宏而不是语法，官方文档明确说它们不能跨顶层语句跳转，需要时把两者包进同一个 `let`/`begin` 块。⚠️ `catch e` 捕获所有异常，只处理特定类型时要写 `catch e` 后用 `if e isa DomainError` 分支处理、否则 `rethrow()`，`rethrow()` 保留原始栈信息而 `throw(e)` 不会；`finally` 里的 `return` 会覆盖 `try` 的返回值，同样应避免。

📘 [Julia · Control Flow](https://docs.julialang.org/en/v1/manual/control-flow/#Exception-Handling-1)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的跳转有 `break`、`continue`、`return`、`throw`、`goto`、`goto case`/`goto default`，以及迭代器专用的 `yield break`。直到 C# 14 都没有带标签的 `break`/`continue`（官方文档把它标为 C# 15 的新增特性），所以跳出多层循环要么用 `goto`，要么把内层抽成方法用 `return`。

```csharp
using System;
using System.Collections.Generic;

class Jumps {
    static IEnumerable<int> Evens(int n) {
        for (int i = 0; i < n; i++) {
            if (i % 2 != 0) continue;      // continue
            if (i > 6) yield break;         // yield break 结束整个迭代器
            yield return i;                 // yield return 产出一个值
        }
    }

    static void Main() {
        foreach (var v in Evens(10)) Console.Write($"{v} ");   // 0 2 4 6
        Console.WriteLine();
        int n = 0;
        while (true) {
            n++;
            if (n > 5) break;               // break 退出 while
        }
        Console.WriteLine(n);               // 6
        for (int a = 0; a < 3; a++) {
            for (int b = 0; b < 3; b++) {
                if (a == 1 && b == 1) goto done;   // 无标签 break，只能 goto
                n++;
            }
        }
        done:
        Console.WriteLine(n);               // 10
        try {
            throw new InvalidOperationException("boom");
        } catch (InvalidOperationException e) {
            Console.WriteLine($"caught {e.Message}");   // caught boom
        } finally {
            Console.WriteLine("finally");               // finally
        }
    }
}
```

`yield return` 与 `yield break` 只能出现在返回 `IEnumerable<T>`/`IEnumerator<T>` 的迭代器方法里，前者把值交给调用方并暂停、后者结束迭代；编译器把它们编译成状态机，所以迭代器方法在第一次 `MoveNext()` 之前不会执行任何代码。`goto` 在 C# 里只允许在同一 `switch` 内部或同一方法内跳转，跳进 `try` 块或循环体是非法的。⚠️ `goto case`/`goto default` 是 C# `switch` 不能隐式穿透后的补偿手段；`throw` 是表达式（C# 7 起），可以写在 `??`、三元或 `=>` 右边；`finally` 里写 `return` 会编译报错（这点比 Java 安全）。

📘 [MS Learn · 跳转语句](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/jump-statements)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的跳转有 `break`、`continue`、`return`、`throw`、`rethrow`，循环与 `switch` 都支持标签（`outer: for ...`、`break outer`）。Dart 3.0 之后 `switch` 分支不再需要 `break`，只有空分支才会贯穿；生成器函数里用 `yield` 产出值，`return` 直接结束生成器。

```dart
String classify(int n) {
  if (n < 0) return 'neg';
  if (n == 0) return 'zero';
  return 'pos';
}

Iterable<int> evens(int n) sync* {          // sync* 是同步生成器
  for (var i = 0; i < n; i++) {
    if (i.isOdd) continue;                   // continue
    if (i > 6) return;                       // return 结束整个生成器
    yield i;                                  // yield 产出值
  }
}

void main() {
  print('${classify(-1)} ${classify(0)} ${classify(1)}');   // neg zero pos
  var n = 0;
  outer: for (var a = 0; a < 3; a++) {       // 循环标签
    for (var b = 0; b < 3; b++) {
      if (a == 1 && b == 1) break outer;      // 带标签 break
      n++;
    }
  }
  print(n);                                   // 4
  print(evens(10).toList());                  // [0, 2, 4, 6]
  try {
    throw const FormatException('bad');
  } on FormatException catch (e) {
    print('caught ${e.message}');              // caught bad
  } finally {
    print('finally');                          // finally
  }
}
```

生成器分两类：`sync*` 返回 `Iterable`、`async*` 返回 `Stream`，两者都用 `yield` 产出、用 `yield*` 委托给另一个可迭代对象；在生成器里 `return` 只是结束序列，不能带回值（`sync*` 的 `return` 不允许带表达式）。异常处理用 `on 类型 catch (e)` 只捕获指定类型，`rethrow` 原样重新抛出并保留栈信息，`finally` 一定执行。⚠️ 用错 `throw` 的对象类型会让 `on` 子句失效，`catch (e)` 不写 `on` 会捕获所有异常包括 `Error`；`break`/`continue` 的标签必须指向包含它的循环，标签只能出现在循环或 `switch` 之前。

📘 [Dart · Branches（含标签 break）](https://dart.dev/language/branches)

{{% /tab %}}

{{% tab header="R" %}}

R 的跳转只有 `break`、`next`（就是其它语言的 `continue`）和 `return`，没有 `goto`、没有标签，`break`/`next` 只作用于最内层循环。`return` 只在函数里有意义，返回的值是给定的对象，不给值就返回 `NULL`；`invisible()` 能把返回值标记为「不自动打印」，这是 R 里做副作用的函数常用的技巧。

```r
f <- function(x) {
  if (x < 0) return("neg")
  "non-neg"                       # 最后一条表达式的值即返回值
}
print(f(-1)); print(f(0))          # [1] "neg" / [1] "non-neg"

g <- function(x) invisible(x * 2)   # 计算但不自动打印
g(21)                               # 什么都不打印
print(g(21))                        # [1] 42

total <- 0
for (i in 1:10) {
  if (i > 5) break                  # break 只跳出最内层循环
  if (i %% 2 == 0) next             # next 就是 continue
  total <- total + i
}
print(total)                        # [1] 9（1+3+5）

safe <- function(expr) {
  tryCatch(expr, error = function(e) paste("error:", conditionMessage(e)))
}
print(safe(stop("boom")))            # [1] "error: boom"
print(safe(1 + 1))                   # [1] 2
```

`return` 求值并返回的是调用帧里的结果，如果没有给值就返回 `NULL`；在函数末尾省略 `return` 时，最后一个表达式的值自动成为返回值。`invisible()` 不改变值本身，只影响交互式环境是否打印，因此它适合「主要是副作用、顺手返回点东西」的函数，例如 `plot` 返回的绘图对象就是不可见的。⚠️ R 没有多层跳出机制，嵌套循环想一次退出就得用标志变量或者把内层写成函数；`break`/`next` 写在 `if` 里但不处于循环中会报错；错误处理用 `tryCatch`/`withCallingHandlers`，`stop()` 抛出错误、`warning()` 只提示，`on.exit()` 相当于 `finally`。

📘 [R · Control 与 break/next](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Control.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的跳转有 `break`、`continue`、`return`，以及带标签的 `break :label 值` 与 `continue :label`，没有 `goto`。因为 `if`、`switch`、块都是表达式，`break :blk expr` 就成了「从任意块里提前带值退出」的通用写法，它同时承担了其它语言里 `goto cleanup` 和 `return` 的部分职责；错误则通过 `try`/`catch`/`defer`/`errdefer` 在值层面传递。

```zig
const std = @import("std");

fn find(xs: []const i32, target: i32) !usize {
    for (xs, 0..) |x, i| {
        if (x == target) return i;        // 提前 return
        if (x > target) break;             // break 只退出本层
    }
    return error.NotFound;                 // 错误就是返回值
}

pub fn main() void {
    const xs = [_]i32{ 1, 3, 5, 7 };
    std.debug.print("{d}\n", .{find(&xs, 5) catch 0});        // 2
    std.debug.print("{}\n", .{find(&xs, 4)});                 // error.NotFound
    const v = blk: {                      // 带标签的块，break 就是块的值
        var acc: i32 = 0;
        for (xs) |x| {
            if (x > 3) break :blk acc;
            acc += x;
        }
        break :blk acc;
    };
    std.debug.print("{d}\n", .{v});        // 4
    var n: usize = 0;
    outer: while (n < 5) : (n += 1) {
        if (n == 2) continue :outer;        // 带标签 continue
    }
    std.debug.print("{d}\n", .{n});        // 5
}
```

`break :label 值` 让任何带标签的块都能当表达式用：循环里提前算出结果就 `break :blk acc`，不需要额外的标志变量，也不需要 `goto`。`defer` 在作用域退出时执行（包括 `return`、`break`、错误传播），`errdefer` 只在因为错误离开作用域时执行，这是 Zig 里释放资源的规范做法。⚠️ Zig 没有异常、没有 `goto`、没有标签 `break` 之外的跳转；`try` 只能用在返回错误联合的函数里，`catch` 必须处理错误或 `unreachable`；`continue :outer` 会先执行 `while` 的 continue 表达式再进入下一轮，而 `break :outer` 不会。

📘 [Zig · break 与标签块](https://ziglang.org/documentation/master/#Blocks)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的跳转有 `break`、`goto` 和 `return`；**没有 `continue`**，惯用替代是在循环体末尾放一个 `::continue::` 标签然后用 `goto continue` 跳过本轮剩余。`goto` 可以跳到同一函数内任何可见标签，只要不进入局部变量的作用域；`return` 必须是所在块的最后一条语句。

```lua
-- break 退出当前循环
local i = 0
while true do
  i = i + 1
  if i >= 3 then break end
end
print(i)                                   -- 3

-- 没有 continue：用 goto 跳到循环体末尾的标签
for n = 1, 5 do
  if n % 2 == 0 then goto continue end
  io.write(n, " ")                          -- 1 3 5
  ::continue::
end
print()

-- goto 不能跳进局部变量的作用域
-- 🛑 下面这段会报 "jumps into the scope of local 'x'"：
-- do
--   goto skip
--   local x = 1
--   ::skip::
-- end

-- return 必须是块的最后一条语句
local function classify(x)
  if x < 0 then return "neg" end
  return "non-neg"
end
print(classify(-1), classify(0))            -- neg	non-neg

-- 错误用 pcall/xpcall 捕获，而不是 try/catch
local ok, err = pcall(function() error("boom") end)
print(ok, err ~= nil)                        -- false	true
print(pcall(function() return 1 + 1 end))     -- true	2
```

`pcall` 以保护模式调用函数，返回 `true` 加所有返回值，或在出错时返回 `false` 加错误消息；`xpcall` 额外接收一个消息处理器，可以在栈展开前补充堆栈信息。`goto` 在 Lua 5.2 引入，官方定位是「结构化编程的补充」，最典型的用法就是模拟 `continue` 与跳出多层循环。⚠️ `return` 只能出现在块的最后（后面只能跟 `end`，不能跟标签或别的语句），需要提前返回就用 `do return end`；`error()` 抛出的值可以是任何类型（通常是字符串或表），`pcall` 原样返回它；`goto` 不能跳到函数外，也不能跨越局部变量的声明。

📘 [Lua 5.5 · goto 语句](https://www.lua.org/manual/5.5/manual.html#3.3.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的跳转就是 JavaScript 的那一套：`break`、`continue`、`return`、`throw`，加上标签语句 `outer: for ...`。类型系统在这里的贡献是 `never`：把 `function assertNever(x: never): never` 放在 `switch` 的 `default` 里，任何漏掉的分支都会在编译期让 `never` 赋值失败，从而把「不完整的穷尽」变成编译错误。

```typescript
function classify(n: number): string {
  if (n < 0) return "neg";                 // return 提前退出
  if (n === 0) return "zero";
  return "pos";
}
console.log(classify(-1), classify(0), classify(1));   // neg zero pos

let steps = 0;
outer: for (let a = 1; a <= 3; a++) {
  for (let b = 1; b <= 3; b++) {
    if (b === 2) continue outer;            // 标签 continue
    steps++;
  }
}
console.log(steps);                          // 3

function assertNever(x: never): never {
  throw new Error(`unexpected ${JSON.stringify(x)}`);   // never：函数不返回
}

try {
  throw new RangeError("bad");
} catch (e) {
  if (e instanceof RangeError) console.log(e.message);   // bad
} finally {
  console.log("done");                                    // done
}
```

标签写在任意语句之前，`break label` 可以跳出被标记的任意块（不只是循环），`continue label` 只能指向循环。`catch` 的异常参数在 TypeScript 4.0 起是 `unknown`，要按类型使用必须先收窄（`instanceof`、`typeof` 或自定义谓词），这是与 JavaScript 最大的差异之一。⚠️ 标签在编译产物里会保留，但压缩工具可能重命名它们，动态生成标签名不可靠；`never` 只表示「不会正常返回」，抛异常或死循环都算，但如果函数真的返回了值，编译期就会报错；类型谓词 `x is T` 不会做运行时检查，写错了只会骗过编译器。

📘 [TS Handbook · never 与穷尽检查](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#exhaustiveness-checking)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 有 `break`、`continue`、`return`、`throw`，以及可以给任意语句加标签的 `label:`——`break label` 甚至能跳出被标记的普通块，这在其它语言里很少见。异常用 `try`/`catch`/`finally` 处理，生成器对象还额外提供 `return()` 与 `throw()` 两个方法，能从外部让 `yield` 处产生一次返回或抛出。

```javascript
function classify(n) {
  if (n < 0) return "neg";                 // return 提前退出
  if (n === 0) return "zero";
  return "pos";
}
console.log(classify(-1), classify(0), classify(1));   // neg zero pos

let n = 0;
outer: for (let a = 1; a <= 3; a++) {
  for (let b = 1; b <= 3; b++) {
    if (b === 2) continue outer;            // 标签 continue
    n++;
  }
}
console.log(n);                              // 3

let m = 0;
loop1: for (let a = 0; a < 3; a++) {
  for (let b = 0; b < 3; b++) {
    if (a === 1 && b === 1) break loop1;     // 标签 break 跳出多层
    m++;
  }
}
console.log(m);                              // 4

try { null.x; } catch (e) { console.log(e.constructor.name); }   // TypeError

function* g() {
  try { yield 1; } finally { console.log("gen finally"); }
}
const it = g();
console.log(it.next().value);                 // 1
it.return();                                  // gen finally
```

`break label` 与不带标签的 `break` 的区别是前者能跨越任意层数，代价是可读性——多数场景用函数加 `return` 更清楚。`finally` 一定会执行，而且如果 `finally` 里有 `return`，它会覆盖 `try` 里的 `return` 甚至吞掉异常，这是 JS 里公认的坏味道。⚠️ 生成器的 `it.return(v)` 会让生成器在 `yield` 处结束并执行 `finally`，`it.throw(e)` 则在 `yield` 处抛出异常；`for...of` 提前 `break` 时会自动调用迭代器的 `return()`，手写 `while` + `next()` 则不会，忘掉这一点会导致资源清理逻辑不执行。

📘 [MDN · label 语句](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/label)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的跳转有 `break`、`continue`、`return`、`throw`、`goto` 和 `exit`/`die`。`break`/`continue` 可以带一个数字表示层数，`break 2` 就是一次跳出两层循环——这是少数语言提供的写法；`goto` 只能在同一文件、同一上下文内跳，不能跳进循环或 `switch`，也不能跨函数。

```php
<?php
function classify(int $n): string {
    if ($n < 0) return "neg";
    if ($n === 0) return "zero";
    return "pos";
}
echo classify(-1), " ", classify(0), " ", classify(1), "\n";   // neg zero pos

foreach ([[1, 2], [3, 4]] as $pair) {
    foreach ($pair as $v) {
        if ($v === 3) break 2;          // 一次跳出两层
        echo $v, " ";                    // 1 2
    }
}
echo "\n";

$i = 0;
while (true) {
    $i++;
    if ($i > 5) break;                   // 先判退出
    if ($i % 2 === 0) continue;           // 再判跳过
}
echo $i, "\n";                            // 6

for ($j = 0; $j < 3; $j++) {
    if ($j === 1) goto out;               // goto 跳出循环
}
out:
echo "out\n";                             // out

try {
    throw new RuntimeException("boom");
} catch (RuntimeException $e) {
    echo "caught ", $e->getMessage(), "\n";   // caught boom
} finally {
    echo "finally\n";                          // finally
}
```

`break 2`/`continue 2` 里的数字必须是一个大于等于 1 的字面量整数，超出嵌套层数会触发致命错误；这是 PHP 在缺少标签跳转时给出的折中方案，可读性不如标签，因此层数一大就该重构。`goto` 在 PHP 里主要用于跳出 `switch` 或多层循环，它的限制比 C 严格：目标标签必须在同一文件、同一函数内，且不能跳进循环或 `switch` 内部。⚠️ `exit`/`die` 会立刻终止脚本（`exit(1)` 设置退出码），`finally` 不会执行，所以只应在真正的终止点使用；`throw` 的对象必须是 `Throwable` 的实现，PHP 7 起内置的 `Error` 与 `Exception` 就是两条互不继承、但都实现 `Throwable` 的平行体系。

📘 [PHP · break 与 continue 的层数](https://www.php.net/manual/en/control-structures.break.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的跳转词汇表是这一组里最丰富的：`break`、`next`（相当于 `continue`）、`redo`（重做本轮）、`retry`（重试 `begin` 块）、`return`，以及用 `catch`/`throw` 做的非局部退出。同一个 `break`/`next`/`return` 在块、`Proc`、`lambda` 里的语义并不相同，这是 Ruby 里最需要记清的一组规则；Ruby 没有 `goto`、没有标签。

```ruby
attempts = 0
begin
  attempts += 1
  raise "boom" if attempts < 2
rescue
  retry                       # 重新执行整个 begin 块（仅 rescue 内合法）
end
puts attempts                 # 2

puts [1, 2, 3].map { |x| next 0 if x == 2; x }.inspect   # [1, 0, 3]

v = while true do break 42 end
puts v                        # 42（break 可以给循环一个值）

r = catch(:done) do
  10.times { |i| throw :done, i if i == 3 }   # 非局部退出
  :never
end
puts r                        # 3

def first_even(xs)
  xs.each { |x| return x if x.even? }   # return 从方法返回，不是从块
  nil
end
puts first_even([1, 3, 4, 5])           # 4

f = Fiber.new { Fiber.yield 1; Fiber.yield 2 }
puts f.resume                            # 1
```

三者的分界线是「谁拥有这个代码块」：在普通块（`each {}`）里 `break` 退出**提供块的那个方法**、`next` 结束本轮块调用、`return` 从**定义块的外层方法**返回；在 `lambda` 里三者都只作用于 lambda 自身；在非 lambda 的 `Proc` 里 `return` 会尝试从定义它的方法返回，方法已经不在了就抛 `LocalJumpError`。`redo` 重新执行同一轮块且不重新取值、`retry` 只能出现在 `rescue` 里并重跑 `begin` 块，两者都容易写出死循环。⚠️ `catch`/`throw` 与异常无关，它只是基于对象身份的成对跳转，跨方法使用时要保证 `throw` 的符号确实有对应的 `catch`，否则抛 `UncaughtThrowError`；`break` 只有用在循环或块里才合法。

📘 [Ruby · Control expressions](https://docs.ruby-lang.org/en/master/syntax/control_expressions_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 迭代协议与生成器

把「遍历」抽象成协议的语言，`for` 就不再需要知道容器的具体类型：Rust 用 `Iterator`/`IntoIterator`、Python 用 `__iter__`/`__next__`、JavaScript/TypeScript 用 `Symbol.iterator`、C# 用 `IEnumerable`/`IEnumerator`、Java 用 `Iterable`/`Iterator`、Kotlin 用 `Iterable`/`Sequence`、Swift 用 `Sequence`、C++ 用 `begin`/`end`、Julia 用 `iterate`、Ruby 用 `each` + `Enumerable`、Lua 用「迭代函数 + 状态 + 控制变量」、PHP 用 `Iterator`。C 和 R 没有原生协议：C 只能靠索引或函数指针，R 靠 `apply` 家族。生成器则是「把函数暂停在 `yield` 处」的语法糖，它天然是惰性与无限序列的来源，也和协程共用同一套挂起/恢复机制。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的迭代协议是 `Iterator` trait：只要实现 `next()` 返回 `Option<Self::Item>`，类型就能用在所有适配器上；`for` 循环认的是 `IntoIterator`，它由 `Iterator`、数组、`Vec`、`HashMap` 等实现。适配器（`map`、`filter`、`take`、`chain`）是惰性的，消费器（`collect`、`sum`、`fold`、`count`）才真正驱动迭代。Rust 至今**没有稳定的生成器语法**：`gen` 块与 `yield` 在 1.98 仍是 nightly 特性。

```rust
struct Countdown(i32);
impl Iterator for Countdown {                 // 实现 Iterator 就是"生成器"
    type Item = i32;
    fn next(&mut self) -> Option<i32> {
        if self.0 == 0 { None } else { self.0 -= 1; Some(self.0 + 1) }
    }
}

fn main() {
    let v: Vec<i32> = Countdown(3).collect();
    println!("{v:?}");                        // [3, 2, 1]

    let mut n = 0;
    let it = std::iter::from_fn(move || {      // 闭包版惰性序列：move 让闭包捕获 n
        n += 1;
        if n <= 3 { Some(n * n) } else { None }
    });
    let w: Vec<i32> = it.collect();
    println!("{w:?}");                         // [1, 4, 9]

    let squares: Vec<i32> = (1..=10).filter(|x| x % 2 == 0).map(|x| x * x).collect();
    println!("{squares:?}");                   // [4, 16, 36, 64, 100]
    let n7 = (1..).filter(|x| x % 7 == 0).take(3).count();   // 无限序列
    println!("{n7}");                          // 3
}
```

`Iterator` 的适配器都是零成本抽象：泛型参数经过 monomorphization 单态化之后，编译器把它们内联成与手写循环等价的机器码，所以链式写法不会带来运行时开销。惰性有两层含义——适配器不产生中间集合，且 `(1..)` 这样的无限范围只有配上 `take`/`find`/`take_while` 这类会提前结束的消费器才安全。⚠️ `gen` 块（`gen { yield 1; }`）和 `yield` 语法在 Rust 1.98 仍是 nightly，报错信息会指向 issue 117078 与 43122，生产代码里请用「手写 `Iterator` 实现」或 `std::iter::from_fn` 代替；协程方面 Rust 有稳定的 `async`/`await` 与 `Future`，但那是异步任务的挂起恢复，和同步生成器不是同一套 API。

📘 [Rust · Iterator trait](https://doc.rust-lang.org/std/iter/trait.Iterator.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的迭代协议是 `Sequence` 加 `IteratorProtocol`：`Sequence` 提供 `makeIterator()`，`IteratorProtocol` 只要求 `mutating func next() -> Element?`。`for-in` 认的是 `Sequence`，`AnyIterator` 把闭包包装成迭代器，`AsyncSequence` 则是它的异步版本，配合 `for await` 使用。Swift 没有生成器关键字：返回 `AnyIterator`、或遵守 `IteratorProtocol` 的类型就是「生成器」，6.4 起新增的 `Iterable`/`BorrowingIteratorProtocol` 则把 `for-in` 扩展到 `Span`、`InlineArray` 这类不可复制、不可逃逸的类型。

```swift
struct Countdown: Sequence, IteratorProtocol {   // 同时满足两个协议
    var n: Int
    mutating func next() -> Int? {
        if n == 0 { return nil }
        defer { n -= 1 }
        return n
    }
}
print(Array(Countdown(n: 3)))                    // [3, 2, 1]

let firstThree = (1...).lazy.filter { $0 % 7 == 0 }.prefix(3)   // 无限序列
print(Array(firstThree))                          // [7, 14, 21]

var it: AnyIterator<Int> = AnyIterator({          // 闭包式惰性序列
    var i = 0
    return { i += 1; return i <= 3 ? i * i : nil }
}())
print(Array(it))                                  // [1, 4, 9]

let stream = AsyncStream<Int> { cont in           // AsyncSequence
    for i in 1...3 { cont.yield(i) }
    cont.finish()
}
var got: [Int] = []
for await v in stream { got.append(v) }
print(got)                                        // [1, 2, 3]
```

`Sequence` 是「可以多次遍历」的语义，而 `IteratorProtocol` 的实现通常是一次性的，所以一个类型同时遵守两者时要注意 `makeIterator()` 是否返回独立的迭代器（这里 `Countdown` 是值类型，每次返回副本，因此可重复遍历）。`.lazy` 把 `filter`/`map` 变成惰性适配，`prefix`/`first`/`drop` 这类会提前结束的操作才让无限序列可用。Swift 6.4 起新增 `Iterable` 协议，让 `for-in` 也能遍历 `Span`、`InlineArray` 这类不可复制类型。⚠️ `for await` 只能在异步上下文里用，`AsyncStream` 必须调用 `finish()` 否则消费者永远挂起；`AnyIterator` 的闭包是可变的，写成 `let` 后不能再取第二个独立迭代器。

📘 [Swift · Sequence 与 IteratorProtocol](https://developer.apple.com/documentation/swift/sequence)

{{% /tab %}}

{{% tab header="Go" %}}

Go 在 1.23 之前没有迭代器协议：`range` 只认识数组、切片、字符串、map、channel 这几种内建类型，自定义序列只能写 `Next() (T, bool)` 这类方法然后手写 `for` 循环。Go 1.23 引入 range-over-func：`for x := range f` 中的 `f` 可以是 `func(func(K, V) bool)` 形式的迭代器函数，标准库用 `iter.Seq`/`iter.Seq2` 给出别名。生成器就写成一个接收 `yield` 回调的函数。

```go
package main

import (
	"fmt"
	"iter"
	"slices"
)

func Countdown(n int) iter.Seq[int] { // 迭代器函数：range-over-func
	return func(yield func(int) bool) {
		for i := n; i > 0; i-- {
			if !yield(i) { // yield 返回 false 表示消费方提前退出
				return
			}
		}
	}
}

func Naturals() iter.Seq[int] { // 无限序列
	return func(yield func(int) bool) {
		for i := 1; ; i++ {
			if !yield(i) {
				return
			}
		}
	}
}

func Take(seq iter.Seq[int], n int) iter.Seq[int] { // 惰性适配器
	return func(yield func(int) bool) {
		i := 0
		for v := range seq {
			if i >= n {
				return
			}
			i++
			if !yield(v) {
				return
			}
		}
	}
}

func main() {
	for v := range Countdown(3) { // 自定义序列
		fmt.Print(v, " ") // 3 2 1
	}
	fmt.Println()
	fmt.Println(slices.Collect(Countdown(3))) // [3 2 1]
	fmt.Println(slices.Collect(Take(Naturals(), 4))) // [1 2 3 4]
	fmt.Println(slices.Collect(slices.Values([]string{"a", "b"}))) // [a b]
}
```

迭代器函数的契约是：每次调用 `yield` 都可能返回 `false`，此时必须立刻 `return`，否则会破坏 `break`/`return` 的语义（`iter` 包把它描述为「push 迭代器」）。这套设计让任何 `iter.Seq` 都能被 `slices`/`maps` 包里的函数消费，也能链式组合适配器，代价是回调风格比通道更省内存（没有 goroutine 与缓冲）。⚠️ `iter.Seq2` 用于两值序列（键值对），`slices.Values` 只包装切片；range-over-func 是 Go 1.23 起的能力，`go.mod` 里语言版本低于 1.23 时编译不过；`yield` 之后不要再访问循环外的可变状态，因为消费方可能已经返回。

📘 [Go 1.23 Release Notes · range-over-func](https://go.dev/doc/go1.23)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的迭代协议只有两个方法：`__iter__()` 返回迭代器、`__next__()` 返回下一个值或抛 `StopIteration`。任何含 `yield` 的函数都是生成器函数，调用它得到的生成器对象自动实现了这两个方法，因此生成器与手写迭代器可以互换；`yield from` 把迭代委托给另一个可迭代对象，`itertools` 提供了无限序列与惰性组合子。

```python
def countdown(n):
    while n:
        yield n            # yield 让函数变成生成器函数
        n -= 1

g = countdown(3)
print(next(g), next(g), next(g))     # 3 2 1
print(list(countdown(3)))            # [3, 2, 1]

def chain():
    yield from countdown(2)          # 委托给另一个可迭代对象
    yield from "ab"
print(list(chain()))                 # [2, 1, 'a', 'b']

class Countdown:                     # 手写迭代器协议
    def __init__(self, n): self.n = n
    def __iter__(self): return self
    def __next__(self):
        if self.n == 0: raise StopIteration
        self.n -= 1
        return self.n + 1
print(list(Countdown(3)))            # [3, 2, 1]

import itertools
print(list(itertools.islice(itertools.count(7, 7), 3)))   # [7, 14, 21]
print(list(itertools.islice((x * x for x in itertools.count(1)), 3)))  # [1, 4, 9]
print(list(itertools.takewhile(lambda x: x < 4, itertools.count(1))))  # [1, 2, 3]
gen = countdown(2)
print(gen.send(None))                # 2
gen.close()
```

`__iter__` 与 `__next__` 的分工是：可迭代对象（list、dict、生成器）实现 `__iter__`，迭代器自身是「一次性」的、每次 `next` 前进一格；`for` 先调 `iter()` 再反复 `next()`，所以**迭代器不能重复遍历**，要重复遍历就得返回新的迭代器。`yield from` 不只是语法糖，它还负责把 `send()`/`throw()` 转发给子生成器，所以能让委托链完整透传。⚠️ 生成器被 `close()` 或垃圾回收时会在 `yield` 处抛 `GeneratorExit`，`finally` 会执行，但不要在 `finally` 里再 `yield`（会抛 `RuntimeError`）；生成器表达式与列表推导式的区别只在括号，前者惰性、后者立即建表；`itertools.count()` 默认无限，必须配 `islice`/`takewhile` 之类才能安全消费。

📘 [Python Reference · 生成器与迭代器](https://docs.python.org/3/reference/expressions.html#yield-expressions)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 有两套序列：`Iterable`（`List`、`Set`，以及 `Map` 的 `entries`/`keys`/`values` 视图）是**急切**的，每个 `map`/`filter` 都会建一个中间集合；`Sequence` 是**惰性**的，操作只是包装成新的序列，直到遇到 `toList`/`first`/`sum` 这类终止操作才逐个求值。`sequence { }` 是生成器构建器，里面的 `yield` 与 `yieldAll` 就是挂起点；`generateSequence` 适合造无限序列。

```kotlin
fun countdown(n: Int): Sequence<Int> = sequence {   // sequence builder
    var i = n
    while (i > 0) {
        yield(i)                                    // 惰性产出
        i--
    }
}

fun main() {
    println(countdown(3).toList())                   // [3, 2, 1]
    println(listOf(1, 2, 3).asSequence().map { it * it }.toList())   // [1, 4, 9]

    val naturals = generateSequence(1) { it + 1 }     // 无限序列
    println(naturals.filter { it % 7 == 0 }.take(3).toList())   // [7, 14, 21]

    var calls = 0
    val eager = listOf(1, 2, 3).map { calls++; it * 2 }          // 立刻算 3 次
    println("$calls $eager")                          // 3 [2, 4, 6]
    calls = 0
    val lazySeq = listOf(1, 2, 3).asSequence().map { calls++; it * 2 }
    println(calls)                                    // 0（还没算）
    println(lazySeq.first())                          // 2
    println(calls)                                    // 1（只算了一个）

    val once = sequence { yield(1); yield(2) }.constrainOnce()
    println(once.toList())                            // [1, 2]
    // once.toList()                                  // 🛑 IllegalStateException
}
```

`Sequence` 的价值在长链式操作与大数据量：`asSequence()` 之后 `map`/`filter` 不再产生中间集合，短路操作（`first`、`any`、`find`）也能提前停止，而 `Iterable` 的链式调用每一步都会遍历全量。元素类型在两者里都是协变的（`Iterable<out T>`、`Sequence<out T>`），所以 `List<String>` 可以直接当成 `Iterable<Any>` 传参。`sequence { }` 里的代码不是立刻执行的，它被包成一个挂起式构建器，只在被消费时推进；因此 `yield` 只能写在 `sequence`/`iterator` 这类构建器作用域里。⚠️ `constrainOnce()` 明确禁止二次遍历，忘了它会在第二次 `toList()` 时抛 `IllegalStateException`（普通 `sequence { }` 重复遍历会得到新的构建器，行为反而更宽松）；`generateSequence` 默认无限，必须用 `take`/`first` 截断；`Sequence` 不能并行，需要并行就转成 `Stream`（Java 互操作）或协程。

📘 [Kotlin · Sequences](https://kotlinlang.org/docs/sequences.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的迭代协议是 `Iterable` + `Iterator`：`Iterable.iterator()` 返回 `Iterator`，后者有 `hasNext()`、`next()`、`remove()`（默认抛 `UnsupportedOperationException`）以及 8 起的 `forEachRemaining()`。增强 `for` 认的就是 `Iterable` 或数组。`Stream` 是另一套惰性管道 API：中间操作（`map`、`filter`、`sorted`、`limit`）只是记录并返回新的 `Stream`，终止操作（`collect`、`forEach`、`count`、`reduce`、`toList`）才真正触发计算；Java 语言层面没有 `yield`，无限流要用 `Stream.iterate`/`Stream.generate` 加 `limit`。

```java
import java.util.Iterator;
import java.util.List;
import java.util.stream.Stream;

public class Iters {
    public static void main(String[] args) {
        List<Integer> xs = List.of(1, 2, 3);
        for (int x : xs) System.out.print(x);                 // 123（增强 for）
        System.out.println();
        Iterator<Integer> it = xs.iterator();                  // 手写 Iterator 协议
        while (it.hasNext()) System.out.print(it.next());      // 123
        System.out.println();
        xs.forEach(x -> System.out.print(x));                  // 123
        System.out.println();

        Stream<Integer> s = Stream.iterate(1, n -> n + 1)      // 无限流
                .filter(n -> n % 7 == 0)
                .limit(3);                                     // 惰性 + 短路
        s.forEach(n -> System.out.print(n + " "));             // 7 14 21
        System.out.println();
        System.out.println(Stream.of(1, 2, 3).map(n -> n * n).toList());   // [1, 4, 9]
    }
}
```

`Iterator` 与 `Stream` 的关键差别是复用性：`Iterator` 是一次性的，`Stream` 更严格——它只能被消费一次，再次使用会抛 `IllegalStateException`，想复用就得从数据源重新创建。`Stream.iterate(seed, f)` 是无限的，必须用 `limit`/`takeWhile` 截断，否则终止操作永不返回。⚠️ 在 `Iterator` 遍历过程中修改集合（除非通过 `Iterator.remove()`）会抛 `ConcurrentModificationException`，`Stream` 的管道里改源集合同理；`Stream` 的中间操作是惰性的，所以「忘了写终止操作」意味着整段代码根本不执行，这是新手最常见的困惑；并行流 `parallelStream()` 只在数据量大、操作无状态且可分解时才划算。

📘 [Java API · Iterator](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Iterator.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的迭代协议不是接口而是**约定**：`begin()`/`end()` 返回迭代器，迭代器提供 `*`、`++`、`!=` 等运算符，范围 `for` 与 `<algorithm>`、`<ranges>` 都按这套约定工作。C++20 的 range 库把「视图」做成惰性适配器，可以组合出无限序列；C++23 又加入了 `std::generator`，用协程实现同步生成器。自己写容器只要提供正确的迭代器就能直接用于范围 `for` 与算法。

```cpp
#include <cstdio>
#include <ranges>
#include <vector>

struct Countdown {                            // 自定义容器：提供 begin/end
    int n;
    struct It {
        int i;
        int operator*() const { return i; }
        It& operator++() { --i; return *this; }
        bool operator!=(const It& o) const { return i != o.i; }
    };
    It begin() const { return It{n}; }
    It end() const { return It{0}; }
};

int main() {
    for (int x : Countdown{3}) std::printf("%d ", x);   // 3 2 1
    std::printf("\n");
    std::vector<int> v{1, 2, 3, 4, 5, 6};
    auto even_sq = v | std::views::filter([](int x) { return x % 2 == 0; })
                     | std::views::transform([](int x) { return x * x; })
                     | std::views::take(2);              // C++20 惰性视图
    for (int x : even_sq) std::printf("%d ", x);         // 4 16
    std::printf("\n");
    auto inf = std::views::iota(1) | std::views::filter([](int x) { return x % 7 == 0; })
               | std::views::take(3);                     // 无限序列 + take
    for (int x : inf) std::printf("%d ", x);             // 7 14 21
    std::printf("\n");
}
```

迭代器的分类（输入、前向、双向、随机访问、连续）决定了它能用于哪些算法，自己实现时至少要让 `end()` 的哨兵比较可用；C++20 的 `std::ranges::range` 概念把这个约定形式化了，视图则是「轻量、惰性、可组合」的 range，`views::filter`/`transform`/`take`/`iota` 组合起来读起来与函数式语言接近。C++23 的 `std::generator` 基于协程实现，用 `co_yield` 产出值，是语言里第一个官方的生成器设施。⚠️ 视图不拥有数据，底层容器销毁后视图悬空；`views::filter` 返回的是 `bool` 而不是 `int`，`views::transform` 的 lambda 参数类型要与元素对齐；迭代器失效规则依然适用——在范围 `for` 里修改容器大小是未定义行为。

📘 [cppreference · ranges 视图](https://en.cppreference.com/w/cpp/ranges)

{{% /tab %}}

{{% tab header="C" %}}

C **没有迭代协议**：没有 `begin`/`end` 的约定，没有接口，也没有生成器（没有 `yield`、没有协程关键字）。遍历只能靠索引、指针算术，或者把「对每个元素做什么」写成回调函数传进去——这就是 C 里最接近 `foreach` 的写法。要模拟惰性序列，只能用一个带状态的结构体加 `next` 函数指针，或者用 `setjmp`/`longjmp` 这类非常规手段。

```c
#include <stdio.h>

/* 回调式遍历：C 里最接近 foreach 的抽象 */
static void each(const int *xs, int n, void (*fn)(int)) {
    for (int i = 0; i < n; i++) fn(xs[i]);
}
static void show(int v) { printf("%d ", v); }

/* 手写"迭代器"：结构体 + next 函数指针 */
typedef struct {
    const int *p;
    const int *end;
} Iter;
static int next(Iter *it, int *out) {
    if (it->p == it->end) return 0;           /* 0 表示结束 */
    *out = *it->p++;
    return 1;
}

int main(void) {
    int xs[] = {1, 2, 3};
    each(xs, 3, show);
    printf("\n");                              /* 1 2 3 */
    Iter it = {xs, xs + 3};
    int v;
    while (next(&it, &v)) printf("%d ", v);
    printf("\n");                              /* 1 2 3 */
    return 0;
}
```

回调式遍历把控制权交给被调函数，所以「提前退出」只能靠回调返回一个状态码（`int` 表示是否继续）或设置标志位，`break` 传不进去——这是 C 里做泛型遍历最别扭的地方。函数指针还会阻碍内联，`qsort`/`bsearch` 这类标准库函数在性能敏感场景下常被手写循环替代。⚠️ C 的数组在传参时退化为指针，元素个数必须额外传，`sizeof` 技巧在函数里失效；没有协议也就没有 `for-each` 语法，所有遍历都要自己写边界条件，`i <= n` 与 `i < n` 写错就是越界读写；`setjmp`/`longjmp` 能跨越栈帧跳转，但会跳过自动变量的清理，只有少数运行时实现才敢用。

📘 [cppreference · C 语句与迭代](https://en.cppreference.com/w/c/language/statements)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的迭代协议是 `iterate`：对可迭代对象调用 `iterate(iter)` 返回 `(第一个元素, 状态)` 或 `nothing`，之后调用 `iterate(iter, 状态)` 返回 `(下一个元素, 新状态)` 或 `nothing`。`for`、推导式、`collect`、`sum`、`map` 都建立在这个协议上，所以自定义类型只要实现两个 `iterate` 方法就能用于所有高阶函数。生成器表达式是惰性的，协程则用 `Task`/`Channel` 表达。

```julia
struct Countdown       # 自定义可迭代类型：实现 iterate 协议
    n::Int
end
Base.iterate(c::Countdown) = c.n == 0 ? nothing : (c.n, Countdown(c.n - 1))
Base.iterate(c::Countdown, state) = iterate(state)   # 有状态版本

println(collect(Countdown(3)))          # [3, 2, 1]
println(sum(Countdown(3)))              # 6

g = (x^2 for x in 1:3)                  # 生成器表达式，惰性
println(collect(g))                      # [1, 4, 9]
println(Iterators.take((i^2 for i in Iterators.countfrom(1)), 3) |> collect)  # [1, 4, 9]
println(first(Iterators.filter(iseven, Iterators.countfrom(1))))              # 2

ch = Channel{Int}(4) do c               # Channel + Task：协程化生产者
    for i in 1:3
        put!(c, i)
    end
end
for v in ch
    print(v, " ")                        # 1 2 3
end
println()
```

`iterate` 的两个方法分别负责「开始」与「继续」，状态可以是任何类型，这让迭代器可以是无状态的（重复调 `iterate(iter)` 总能重新开始）或有状态的。生成器表达式 `(f(x) for x in xs)` 返回 `Base.Generator`，它不分配数组、按需产出，`Iterators` 模块的 `take`/`filter`/`drop`/`countfrom` 提供了惰性组合子，`Iterators.Stateful` 则把一次性迭代器包装成可复用的。⚠️ 生成器表达式能不能重复遍历取决于底层可迭代对象：`(x^2 for x in 1:3)` 每次遍历都从头开始，可以反复 `collect`，而 `Iterators.Stateful` 包装的一次性迭代器（例如 `Channel`）一旦被消费就不能重来，想固化结果就先 `collect`；`Channel` 的默认容量为 0 表示会阻塞直到有消费者，这里写 4 是带缓冲；Julia 没有 `yield` 关键字，协程通过 `Task` 与 `Channel` 实现，`@task`/`schedule` 是底层入口。

📘 [Julia · Iteration interface](https://docs.julialang.org/en/v1/manual/interfaces/#Iteration-interface-1)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的迭代协议是 `IEnumerable<T>` + `IEnumerator<T>`：前者提供 `GetEnumerator()`，后者有 `MoveNext()`、`Current`、`Reset()`。只要方法返回 `IEnumerable<T>` 并在里面写 `yield return`，编译器就会生成一个状态机类，让你用线性代码写出惰性序列；`foreach` 还会优先使用结构体枚举器（如 `Span<T>`）以避免装箱。异步版本是 `IAsyncEnumerable<T>` + `await foreach`。

```csharp
using System;
using System.Collections.Generic;

class Iters {
    static IEnumerable<int> Countdown(int n) {   // 迭代器方法
        while (n > 0) {
            yield return n;                       // 每次 MoveNext 才继续
            n--;
        }
    }

    static IEnumerable<int> Naturals() {          // 无限序列
        for (int i = 1; ; i++) yield return i;
    }

    static IEnumerable<int> Take(IEnumerable<int> src, int n) {
        foreach (var v in src) {
            if (n-- <= 0) yield break;
            yield return v;
        }
    }

    static void Main() {
        foreach (var v in Countdown(3)) Console.Write($"{v} ");   // 3 2 1
        Console.WriteLine();
        foreach (var v in Take(Naturals(), 4)) Console.Write($"{v} ");  // 1 2 3 4
        Console.WriteLine();
        IEnumerator<int> e = Countdown(3).GetEnumerator();        // 手写协议
        while (e.MoveNext()) Console.Write($"{e.Current} ");       // 3 2 1
        Console.WriteLine();
    }
}
```

`yield return` 让编译器把方法体切成状态机：调用 `Countdown(3)` 只是创建状态机对象，真正的方法体要等到第一次 `MoveNext()` 才执行，之后每次都从上次 `yield` 处继续。适配器用 `yield` 嵌套 `foreach` 就能写成惰性的，`yield break` 相当于提前结束序列。⚠️ 迭代器方法里的 `try`/`finally` 会被状态机正确处理（`Dispose` 时执行 `finally`），但 `yield return` 不能出现在 `try` 的 `catch` 块或带 `catch` 的 `try` 块里（只能放在 `try`/`finally` 或 `try` 的 `try` 部分）；`IEnumerable<T>` 的枚举器默认是引用类型，每次 `foreach` 会分配一次，热点路径上考虑用 `struct` 枚举器或 `Span<T>`。

📘 [MS Learn · yield 语句](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/yield)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的迭代协议是 `Iterable<T>` + `Iterator<T>`：`Iterable` 提供 `iterator` getter，`Iterator` 只有 `moveNext()` 与 `current`。生成器用函数体标记区分：`sync*` 返回 `Iterable`、`async*` 返回 `Stream`，两者都用 `yield` 产出、用 `yield*` 委托。`Iterable` 的 `map`/`where`/`take` 都是惰性的，配合 `sync*` 能自然写出无限序列。

```dart
Iterable<int> countdown(int n) sync* {      // sync* 同步生成器
  while (n > 0) {
    yield n;                                 // 惰性产出
    n--;
  }
}

Stream<int> countdownAsync(int n) async* {   // async* 异步生成器
  for (var i = n; i > 0; i--) {
    yield i;
  }
}

Iterable<int> multiplesOf7() sync* {
  for (var i = 7; ; i += 7) yield i;         // 无限序列
}

void main() async {
  print(countdown(3).toList());              // [3, 2, 1]
  print(countdown(3).map((x) => x * x).toList());   // [9, 4, 1]（惰性适配）
  print(multiplesOf7().take(3).toList());    // [7, 14, 21]
  await for (final v in countdownAsync(3)) {
    print(v);                                 // 3 / 2 / 1
  }
}
```

`sync*` 生成的 `Iterable` 是惰性的：每次 `moveNext()` 才把函数推进到下一个 `yield`，所以 `take(3)` 之后剩余部分根本不会计算；`map`/`where`/`expand`/`followedBy` 返回的也都是惰性包装，只有 `toList`/`forEach`/`length`/`fold` 这类终止操作才驱动整个链。生成器可以被多次遍历（每次遍历从函数开头重新执行），这与一次性 `Iterator` 不同。⚠️ `async*` 里的 `yield` 必须在 `async` 上下文中，且 `await for` 只能消费 `Stream`；`yield*` 委托时，被委托的序列长度决定了当前位置；在生成器里 `return` 只是结束序列，`sync*` 的 `return` 不允许带值（想产出最后一个值请用 `yield`）。

📘 [Dart · Iterable 与生成器](https://dart.dev/language/functions#generators)

{{% /tab %}}

{{% tab header="R" %}}

R **没有原生的迭代器协议，也没有生成器**：没有 `yield`、没有 `Iterator` 接口、没有惰性序列语法。`for` 只认识向量与列表，遍历靠索引；需要「对每个元素做一件事」时用 `apply` 家族（`lapply`、`sapply`、`vapply`、`mapply`、`tapply`、`rapply`），需要惰性/流式处理则要装 `iterators`、`coro`、`generators` 这类第三方包。闭包是 base R 里唯一能携带状态的手段，可以用它手搓一个「下一个值」的函数。

```r
v <- c(1, 2, 3)
print(lapply(v, function(x) x * x))          # list(1, 4, 9)
print(vapply(v, function(x) x * x, numeric(1)))   # [1] 1 4 9
print(mapply(function(a, b) a + b, 1:3, 4:6))      # [1] 5 7 9

# 自定义"迭代器"：用闭包把状态藏在函数环境里
make_counter <- function(n) {
  i <- 0
  function() {
    i <<- i + 1
    if (i <= n) i else NULL
  }
}
next_val <- make_counter(3)
repeat {
  x <- next_val()
  if (is.null(x)) break
  cat(x, " ")                                 # 1 2 3
}
cat("\n")

# 向量化仍然是最快的"迭代"：没有中间集合，也没有 R 层循环开销
print(sum(v^2))                               # [1] 14
print(paste0("x", v))                          # [1] "x1" "x2" "x3"
```

`lapply` 返回列表、`sapply` 尝试简化（类型不确定时危险）、`vapply` 要求显式给出返回类型模板因而最安全、`mapply` 做多参数并行映射、`tapply` 按因子分组、`rapply` 递归处理嵌套列表。闭包模拟的状态机每次调用都要走一遍 R 函数调用，性能远不如向量化，因此只适合控制流复杂、没法向量化的场景。⚠️ base R 没有 `yield`，想要真正的生成器语义（暂停/恢复）必须依赖 `coro` 包或改用 C/C++ 扩展；`for` 循环体在 R 层解释执行且每轮都可能触发复制，长循环应当优先考虑 `vapply` 或矩阵化；`<<-` 是往父环境赋值，写错层级会静默创建全局变量。

📘 [R · apply 家族](https://stat.ethz.ch/R-manual/R-devel/library/base/html/lapply.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig **没有语言级的迭代器协议**：没有 Rust 那样的 `Iterator` trait，`for` 也不查询任何接口。`for` 是编译期展开的语法糖，只对数组、切片、范围、指向数组的指针等「长度可知」的对象生效；标准库里的迭代器是各 API 自带的具体类型（例如按分隔符切分的 `SplitIterator`），它们只是恰好叫这个名字的普通结构体。生成器与协程也没有：Zig 0.15 移除了 `async`/`await` 关键字，异步 I/O 由 `std.Io` 的 reader/writer 接口显式推进。

```zig
const std = @import("std");

const Countdown = struct {          // 手写"迭代器"：只是一个带 next 的结构体
    n: i32,
    pub fn next(self: *Countdown) ?i32 {
        if (self.n == 0) return null;
        self.n -= 1;
        return self.n + 1;
    }
};

pub fn main() void {
    const xs = [_]i32{ 1, 2, 3 };
    for (xs) |x| std.debug.print("{d} ", .{x});      // 1 2 3（编译期展开）
    std.debug.print("\n", .{});
    for (0..3) |i| std.debug.print("{d} ", .{i});     // 0 1 2
    std.debug.print("\n", .{});

    var it = Countdown{ .n = 3 };
    while (it.next()) |v| std.debug.print("{d} ", .{v});   // 3 2 1
    std.debug.print("\n", .{});

    var parts = std.mem.splitScalar(u8, "a,b,c", ',');      // 具体的迭代器类型
    while (parts.next()) |p| std.debug.print("{s} ", .{p});  // a b c
    std.debug.print("\n", .{});
}
```

`for` 的展开发生在编译期，所以它支持的容器长度必须编译期可知或由切片头提供，这也是为什么 `for` 能完全内联、没有虚函数调用开销。要抽象的场合，Zig 的惯例是让函数返回一个带 `next()` 的结构体，或者接受一个编译期已知类型（`anytype`）——用 `comptime` 泛型替代 trait 对象。惰性求值在 Zig 里表现为「你调一次 `next()` 才前进一格」，没有 `yield` 这样的语法。⚠️ 自定义类型不能直接放进 `for (x) |v|`，除非它有 `len` 与索引操作（或是一个切片/数组）；`while (it.next()) |v|` 的 `|v|` 只能解包 optional，错误要用 `try`/`catch` 另作处理；`std.mem.splitScalar` 这类迭代器持有对原切片的引用，原数据被释放后继续 `next()` 会产生悬空读取。

📘 [Zig · for 循环](https://ziglang.org/documentation/master/#for)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的迭代协议极简：泛型 `for k, v in explist do` 会把 `explist` 求值成四个值——迭代函数、状态、控制变量初值、关闭值，然后每轮用 `(状态, 控制变量)` 调用迭代函数，返回 `nil` 时结束。写一个闭包返回「下一个值」就是生成器；`coroutine.wrap` 把协程包成迭代函数，于是挂起/恢复天然就是惰性序列。Lua 没有独立的 `Iterator` 接口，协议就是「调用约定」。

```lua
-- 泛型 for 的协议：迭代函数、状态、控制变量初值、关闭值
local function range(n)
  local function step(_, i)
    i = i + 1
    if i <= n then return i end
  end
  return step, nil, 0
end
for v in range(3) do io.write(v, " ") end
print()                                       -- 1 2 3

-- 内建迭代器：ipairs 遍历数组部分，pairs 遍历所有键
for i, v in ipairs({ "a", "b" }) do io.write(i, v, " ") end
print()                                       -- 1a 2b

-- 协程包成迭代函数：yield 一次就是"产出"一个值
local function producer(n)
  return coroutine.wrap(function()
    for i = 1, n do coroutine.yield(i) end
  end)
end
for v in producer(3) do io.write(v, " ") end
print()                                       -- 1 2 3

-- 无限序列 + 提前退出
local function naturals()
  local i = 0
  return function() i = i + 1; return i end
end
local taken = 0
for v in naturals() do
  taken = taken + 1
  if taken > 3 then break end
  io.write(v, " ")                             -- 1 2 3
end
print()
```

迭代函数的两参数形式 `(state, control)` 支持把状态放在外面（例如 `ipairs` 用表与索引），闭包形式则把状态藏在 upvalue 里、只用第一个返回值，两种写法都合法。`coroutine.wrap` 返回的函数每次调用让协程运行到下一个 `yield`，因此它天生就是迭代器函数，这就是「生成器与协程同源」在 Lua 里最直接的体现。⚠️ `pairs` 的遍历顺序未定义，`ipairs` 只遍历连续整数键、遇到第一个 `nil` 就停；泛型 `for` 的第四个值（关闭值）在 5.4 起按 to-be-closed 语义处理，循环结束时调用它的 `__close`；`coroutine.wrap` 抛出的错误会传回调用方而不是静默失败，用 `pcall` 包住更安全。

📘 [Lua 5.5 · 泛型 for](https://www.lua.org/manual/5.5/manual.html#3.3.5)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 沿用 JavaScript 的迭代协议 `Symbol.iterator`，并在类型层面把它写成 `Iterable<T>`、`Iterator<T>`、`IterableIterator<T>` 与 `Generator<T, TReturn, TNext>`；`for-of` 要求操作数是 `Iterable<T>`，`[...x]`、解构、`Map`/`Set` 构造器也都走同一协议。`function*` 生成器的返回类型是 `Generator`，`yield` 的值类型由 `TNext` 决定。

```typescript
function* countdown(n: number): Generator<number> {   // Generator<T>
  while (n > 0) yield n--;                              // yield 的类型是 number
}
console.log([...countdown(3)]);                          // [ 3, 2, 1 ]

const iterable: Iterable<number> = {                     // 显式实现 Iterable<T>
  [Symbol.iterator](): Iterator<number> {
    let i = 0;
    return {
      next(): IteratorResult<number> {
        return i < 3 ? { value: ++i, done: false } : { value: undefined, done: true };
      },
    };
  },
};
console.log([...iterable]);                              // [ 1, 2, 3 ]

function* naturals(): Generator<number> {                // 无限序列
  let i = 0;
  while (true) yield ++i;
}
function* take<T>(n: number, src: Iterable<T>): Generator<T> {
  for (const v of src) { if (n-- <= 0) return; yield v; }
}
console.log([...take(3, naturals())]);                   // [ 1, 2, 3 ]

for await (const v of (async function* () { yield 1; yield 2; })()) {
  console.log(v);                                        // 1 / 2
}
```

类型层面最有用的一点是：`Iterable<T>` 只要求 `[Symbol.iterator]()`，所以数组、字符串、`Map`、`Set`、生成器都能互相替换，写泛型函数时用 `Iterable<T>` 而不是 `T[]` 能一次支持所有集合。生成器的三参数类型 `Generator<T, TReturn, TNext>` 分别描述产出值、`return` 的值与 `next(v)` 传入的值，`yield` 表达式本身的类型就是 `TNext`。⚠️ 手写 `[Symbol.iterator]` 时 `done: true` 的 `value` 类型由 `TReturn` 决定，声明成 `Iterator<number>` 时它就是 `any`，需要精确类型就写 `Iterator<number, void>`；`for await` 只能用于异步可迭代对象（`AsyncIterable`），普通迭代器套 `for await` 会报类型错误；类型只在编译期存在，运行时的协议仍然是 `Symbol.iterator` 方法查找。

📘 [TS · Iterators and Generators](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-6.html#stricter-generators)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的迭代协议是 `Symbol.iterator`：可迭代对象提供一个返回迭代器的方法，迭代器提供 `next()` 返回 `{ value, done }`。`for-of`、扩展运算符、解构、`Array.from`、`Map`/`Set` 构造器都走这个协议；`function*` 生成器函数返回的对象同时是可迭代对象与迭代器，`yield*` 负责委托，`async function*` 加 `for await` 处理异步序列。

```javascript
function* countdown(n) {          // function* 生成器函数
  while (n) yield n--;             // 每次 yield 暂停在这里
}
console.log([...countdown(3)]);    // [ 3, 2, 1 ]

function* chain() {
  yield* countdown(2);             // yield* 委托给另一个可迭代对象
  yield* "ab";
}
console.log([...chain()]);         // [ 2, 1, 'a', 'b' ]

const custom = {
  [Symbol.iterator]() {
    let i = 0;
    return { next: () => (i < 3 ? { value: ++i, done: false } : { value: undefined, done: true }) };
  },
};
console.log([...custom]);          // [ 1, 2, 3 ]

const it = countdown(3);           // 生成器对象本身就是迭代器
console.log(it.next().value, it.next().value);   // 3 2

function* naturals() { let i = 0; while (true) yield ++i; }   // 无限序列
function* take(n, iter) { for (const v of iter) { if (n-- <= 0) return; yield v; } }
console.log([...take(4, naturals())]);   // [ 1, 2, 3, 4 ]
```

生成器把「暂停函数」变成语言能力：`yield` 表达式的值就是下一次 `next(v)` 传入的参数，这让生成器既能产出也能接收，是手写状态机与惰性管道的常用工具（`redux-saga` 这类库就建立在它之上）。`yield*` 不只是拼接，它会把外部的 `next`/`throw`/`return` 转发给被委托的迭代器，所以清理逻辑能层层传递。⚠️ 生成器对象只能遍历一次，`[...g]` 之后再 `[...g]` 是空数组；`for-of` 提前 `break` 会自动调用迭代器的 `return()` 执行清理，手动 `while` + `next()` 不会；`async function*` 返回的是 `AsyncIterable`，只能用 `for await` 或 `for await` 支持的消费方式，`[...]` 会对它报错。

📘 [MDN · 迭代协议](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Iteration_protocols)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的迭代协议是 `Iterator` 接口：`current()`、`key()`、`next()`、`rewind()`、`valid()` 五个方法；任何实现了它的对象都能被 `foreach` 遍历。更常用的方式是用含 `yield` 的函数——它返回 `Generator`，而 `Generator` 本身就实现了 `Iterator`，还可以通过 `send()` 接收值、通过 `yield from` 委托；`foreach` 也支持普通数组与 `Traversable`。

```php
<?php
function countdown(int $n): Generator {        // 生成器函数返回 Generator
    while ($n > 0) {
        yield $n;                               // 每次 yield 暂停
        $n--;
    }
}
foreach (countdown(3) as $v) echo $v, " ";       // 3 2 1
echo "\n";

function chain(): Generator {
    yield from countdown(2);                     // yield from 委托
    yield from ['a', 'b'];
}
foreach (chain() as $v) echo $v, " ";            // 2 1 a b
echo "\n";

$g = countdown(3);
var_dump($g instanceof Iterator);                // bool(true)：生成器就是 Iterator
echo $g->current(), "\n";                         // 3
$g->next();
echo $g->current(), "\n";                         // 2

$gen = (function () { $x = yield 1; yield $x * 10; })();
echo $gen->current(), "\n";                       // 1
$gen->send(5);
echo $gen->current(), "\n";                       // 50

$inf = (function () { $i = 0; while (true) yield ++$i; })();   // 无限序列
$out = [];
foreach ($inf as $v) { $out[] = $v; if (count($out) === 3) break; }
echo implode(",", $out), "\n";                    // 1,2,3
```

`Generator` 的键默认是自增整数，需要自定义键就用 `yield $key => $value`；`yield from` 会把子生成器的键值一并委托出去，`foreach` 拿到的就是它们。生成器的双向通信靠 `send()`：`$gen->current()` 取当前产出值，`$gen->send($v)` 把值交给上一个 `yield` 表达式并推进到下一个产出。⚠️ 生成器只能遍历一次，`foreach` 完再 `foreach` 会抛 `Exception: Cannot traverse an already closed generator`；`rewind()` 在生成器已经推进后调用会抛异常，所以不要把同一个生成器交给两段代码；实现了 `Iterator` 的类必须让 `valid()` 与 `current()` 保持一致，否则 `foreach` 的结果会与手动调用不一致。

📘 [PHP · 生成器](https://www.php.net/manual/en/language.generators.overview.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的迭代协议是「方法 + 块」：定义一个接收块的方法，用 `yield` 把值交给块，就得到了遍历能力；只要类里定义了 `each` 并 `include Enumerable`，就免费获得 `map`、`select`、`reduce`、`sort_by`、`each_with_index` 等几十个方法。`Enumerator` 把任意方法包装成惰性序列对象，`Enumerator::Lazy` 支持无限序列，`Fiber` 则是底层的双向协程，也是 `Enumerator` 的实现基础。

```ruby
def countdown(n)                 # 方法 + yield = Ruby 的迭代协议
  while n > 0
    yield n                       # 把值交给块
    n -= 1
  end
end
acc = []
countdown(3) { |x| acc << x }
puts acc.inspect                       # [3, 2, 1]

e = Enumerator.new do |y|              # y 是 yielder
  i = 1
  loop { y << i; i += 1 }              # 无限序列
end
puts e.take(3).inspect                  # [1, 2, 3]
puts e.lazy.select(&:even?).first(3).inspect   # [2, 4, 6]

class Countdown                          # 只要定义 each 就获得整套 Enumerable
  include Enumerable
  def initialize(n) = @n = n
  def each
    n = @n
    while n > 0
      yield n
      n -= 1
    end
  end
end
puts Countdown.new(3).map { |x| x * x }.inspect   # [9, 4, 1]

f = Fiber.new do |x|                     # 双向协程
  y = Fiber.yield(x + 1)
  Fiber.yield(y * 2)
end
puts f.resume(1)                         # 2
puts f.resume(5)                         # 10
```

`Enumerable` 的方法都建立在 `each` 之上，所以自定义集合只需要写一个正确的 `each`，排序、分组、查找、聚合就全都有了。`Enumerator` 有三个来源：`enum_for`/`to_enum` 把已有方法包成枚举器、`Enumerator.new` 手写、以及不传块调用 `each` 时自动返回的枚举器——这也是为什么 `[1,2,3].each` 不带块不报错而是返回 `Enumerator`。⚠️ `Enumerator::Lazy` 必须用 `lazy` 显式开启，普通 `Enumerator` 上的 `select`/`map` 仍然会试图消费整个无限序列而挂死；`Fiber` 的 `resume` 传值会作为上一个 `Fiber.yield` 的返回值，第一次 `resume` 的参数则是块的参数；Ruby 没有 `yield` 之外的生成器关键字，`yield` 只能在方法体内使用，块内层再嵌套块时要用 `block_given?` 与显式 `&blk` 传参。

📘 [Ruby · Enumerable](https://docs.ruby-lang.org/en/master/Enumerable.html)

{{% /tab %}}

{{< /tabpane >}}
