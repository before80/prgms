+++
title = "关键字与保留字"
date = 2026-09-19T10:00:00+08:00
weight = 2
type = "docs"
description = "18 种语言的关键字与保留字对照：完整清单、硬关键字与软关键字、未来保留字、特殊值、标识符规避写法"
isCJKLanguage = true
draft = false
+++

# 关键字与保留字：18 种语言对照

## 关键字与保留字

关键字是语言"自己留着用"的词汇：它们不能（或不能随便）当作变量名、函数名、类型名。但"保留"这件事在不同语言里分好几层——**硬关键字**永远不能用，**软关键字/上下文关键字**只在特定语法位置才是关键字，**保留但未使用**是给未来留的位置，**特殊值**（`true`, `nil`, `None`, `this`）则是语言内建的常量与单例。本页按这五层组织，每个主题一套 18 语言标签页；每门语言都给出完整清单、可以实际运行的示例，以及"想用这个名字怎么办"的规避写法。

**一页速览**

| 语言 | 硬/保留关键字 | 软关键字、上下文关键字 | 一句话说明 |
| --- | --- | --- | --- |
| Rust | 39（严格）+ 14（保留）+ 5（弱） | 弱关键字 5 个：`union`, `macro_rules`, `raw`, `safe`, `'static` | 可以用 `r#type` 写"原始标识符" |
| Swift | 62（声明 27, 语句 19, 表达式 15, 模式 1） | 29 个上下文关键字 | 反引号 `` `class` `` 可强制当标识符 |
| Go | 25 | 0（预声明标识符不算关键字） | `bool`, `int`, `nil`, `len` 是预声明标识符，可以被遮蔽 |
| Python | 35 | 4 个软关键字：`_`, `case`, `match`, `type` | `match`, `case`, `type` 只在特定语句里才是关键字 |
| Kotlin | 31（硬） | 19 个软关键字 + 29 个修饰符关键字 | 反引号 `` `is` `` 可当标识符 |
| Java | 50（保留） | 17 个上下文关键字 | `var`, `record`, `sealed`, `permits`, `when` 都是上下文关键字 |
| C++ | 91（C++23，含 11 个替代记号） | 4 个上下文关键字：`final`, `override`, `import`, `module` | `and`, `or`, `not` 是 `&&`, `||`, `!` 的替代写法 |
| C | 59（C23，另有 2 个条件支持） | 0 | C23 把 `bool`, `true`, `nullptr`, `typeof` 等变成关键字 |
| Julia | 28（保留） | 6 个上下文关键字：`mutable`, `primitive`, `abstract`, `outer`, `public`, `where` | `in`, `isa` 是运算符而不是关键字 |
| C# | 77（保留） | 47 个上下文关键字 | `var`, `async`, `await`, `record`, `required` 都是上下文关键字 |
| Dart | 33（`reserved`，官方表 34 条） | 24（built-in identifier）+ 2（context）+ 8（unrestricted，官方表 9 条） | 关键字表分四档：reserved / built-in identifier / context / unrestricted |
| R | 20（保留字） | 0（`...`, `..1` 是特殊记号） | 反引号 `` `if` `` 可以当变量名 |
| Zig | 46 | 0 | `@"if"` 可以把关键字写成标识符 |
| Lua | 23（5.5 新增 `global`） | 0 | 没有软关键字，但字段名 `t.end` 合法 |
| TypeScript | 85（TS 7 词法器，含上下文） | 约 20 个上下文关键字：`type`, `declare`, `namespace`, `satisfies`, `readonly` 等 | 类型位置的关键字在运行时会被擦除 |
| JavaScript | 35（普通保留字） | 严格模式 9 + 模块/async 1 + 未来保留 1（`enum`） | 保留字可以做属性名：`obj.class` 合法 |
| PHP | 约 70（含 `yield from`）+ 9 个编译期常量 | 0（关键字可作方法名/属性名） | `readonly`, `enum`, `match`, `fn` 是新加入的关键字 |
| Ruby | 41（含 `BEGIN`, `END`, `__FILE__` 等） | 0 | 关键字可以做方法名，但不能当局部变量名 |

**合计**：18 种语言的硬/保留关键字约 **865** 条；再加上软关键字、上下文关键字与未来保留字约 **1,100 条**（不含预声明标识符、字面量与编译期常量）。

### 完整关键字清单

> 说明：每张表按类别分组，类别后的数字是**该类别下的条目数**，表尾的"本表合计"是各类别累加。同一个关键字如果同时属于两类（例如 Python 的 `match` 既在控制流、又在软关键字里），会在两边各计一次；因此"本表合计"与官方清单的"关键字个数"可能略有差异。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 把关键字分成三层：**严格关键字**（39 个，所有 edition 都有）、**保留关键字**（14 个，现在没用，但留给未来）、**弱关键字**（只在特定上下文里才是关键字）。下面按用途列出严格关键字。

| 类别 | 关键字 |
| --- | --- |
| 声明与定义（16 个） | `fn`, `struct`, `enum`, `trait`, `impl`, `type`, `mod`, `use`, `pub`, `const`, `static`, `let`, `crate`, `super`, `self`, `Self` |
| 控制流（9 个） | `if`, `else`, `match`, `loop`, `while`, `for`, `break`, `continue`, `return` |
| 类型与泛型（9 个） | `as`, `where`, `dyn`, `in`, `ref`, `mut`, `move`, `unsafe`, `extern` |
| 异步与其他（3 个） | `async`, `await`, `_` |
| 字面量（2 个） | `true`, `false` |
| 保留但未使用（14 个） | `abstract`, `become`, `box`, `do`, `final`, `gen`, `macro`, `override`, `priv`, `try`, `typeof`, `unsized`, `virtual`, `yield` |
| 弱关键字（5 个） | `union`, `macro_rules`, `raw`, `safe`, `'static` |

**本表合计：58 个条目。**

```rust
// 一行里塞进了 10 多个关键字，感受一下分布
pub struct Counter { n: u32 }

impl Counter {
    pub const fn new() -> Self { Self { n: 0 } }
    pub fn inc(&mut self) { self.n += 1; }
}

fn main() {
    let mut c = Counter::new();
    if c.n == 0 { c.inc(); }
    match c.n { 1 => println!("one"), _ => println!("other") }
}
```

关键字分布得很均匀：声明类（`fn`, `struct`, `impl`, `pub`, `const`）占一半，控制流（`if`, `match`, `loop`, `while`）占另一半。`async`, `await`, `dyn` 是 2018 edition 加入的，`gen` 在 2024 edition 被列为保留字（配合生成器语法），所以 **写 2024 edition 时不要用 `gen` 当变量名**。`union`, `raw`, `safe`, `macro_rules` 只在特定上下文有特殊含义，其他地方可以当标识符。

**几个特殊的关键字**：`unsafe` 表示"这段代码的安全性由我负责"；`dyn` 表示 trait 对象（动态派发）；`impl` 既用于实现块，也用于返回位置的 `impl Trait`；`_` 只作占位符；`union`, `macro_rules`, `raw`, `safe` 是弱关键字，只在特定语法位置才有特殊含义；保留字 `try` 在 2018 edition 之前只是普通标识符。

📘 [The Rust Reference · Keywords](https://doc.rust-lang.org/reference/keywords.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的关键字按"出现在语法的哪一部分"分组（这是官方文档的组织方式），另外还有一组"只在特定上下文里保留"的关键字。

| 类别 | 关键字 |
| --- | --- |
| 声明（27 个） | `associatedtype`, `borrowing`, `class`, `consuming`, `deinit`, `enum`, `extension`, `fileprivate`, `func`, `import`, `init`, `inout`, `internal`, `let`, `nonisolated`, `open`, `operator`, `precedencegroup`, `private`, `protocol`, `public`, `rethrows`, `static`, `struct`, `subscript`, `typealias`, `var` |
| 语句（19 个） | `break`, `case`, `catch`, `continue`, `default`, `defer`, `do`, `else`, `fallthrough`, `for`, `guard`, `if`, `in`, `repeat`, `return`, `switch`, `throw`, `where`, `while` |
| 表达式与类型（15 个） | `Any`, `as`, `await`, `catch`, `false`, `is`, `nil`, `rethrows`, `self`, `Self`, `super`, `throw`, `throws`, `true`, `try` |
| 模式（1 个） | `_` |
| `#` 开头（12 个） | `#available`, `#colorLiteral`, `#else`, `#elseif`, `#endif`, `#fileLiteral`, `#if`, `#imageLiteral`, `#keyPath`, `#selector`, `#sourceLocation`, `#unavailable` |
| 上下文关键字（29 个） | `associativity`, `async`, `convenience`, `didSet`, `dynamic`, `final`, `get`, `indirect`, `infix`, `lazy`, `left`, `mutating`, `none`, `nonmutating`, `optional`, `override`, `package`, `postfix`, `precedence`, `prefix`, `Protocol`, `required`, `right`, `set`, `some`, `Type`, `unowned`, `weak`, `willSet` |

**本表合计：103 个条目。**

```swift
protocol Drawable { func draw() }          // protocol / func

struct Circle: Drawable {
    let r: Double                           // let
    lazy var cached: Double = r * 2          // lazy 是上下文关键字
    func draw() { }
}

final class Shape {                        // final 是上下文关键字
    weak var parent: Shape?                 // weak 也是
    deinit { }
}

enum Result { case ok, failed }
for i in 0..<3 where i > 0 { print(i) }     // for / where / in
```

Swift 的"上下文关键字"（`final`, `lazy`, `weak`, `optional`, `override`…）在别的地方完全可以当标识符用；真要强行用关键字当名字，可以加反引号：`` let `class` = 1 ``。`#` 开头的一批（`#if`, `#available`, `#selector`…）是编译期指令或字面量，不算普通关键字；Swift 5.9 之后 `#file`, `#line`, `#function` 等已经改成标准库宏，不再是保留字。

**几个特殊的关键字**：`throws`, `rethrows`, `try` 构成错误处理体系；`some` 与 `any` 控制不透明类型与存在类型；`borrowing`, `consuming`（Swift 5.9+）标注参数所有权；`nonisolated`（Swift 5.10+）用于并发隔离；`#available`, `#if`, `#selector` 这些 `#` 开头的是编译期指令或字面量，不是普通关键字。

📘 [The Swift Programming Language · Lexical Structure](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/lexicalstructure/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的关键字只有 **25 个**，是这 18 种语言里最少的之一；真正的"陷阱"在于**预声明标识符**——它们不是关键字，可以随时被遮蔽。

| 类别 | 关键字 |
| --- | --- |
| 声明（6 个） | `const`, `func`, `import`, `package`, `type`, `var` |
| 复合类型（4 个） | `chan`, `interface`, `map`, `struct` |
| 控制流（15 个） | `break`, `case`, `continue`, `default`, `defer`, `else`, `fallthrough`, `for`, `go`, `goto`, `if`, `range`, `return`, `select`, `switch` |

**本表合计：25 个条目。**

```go
package main                                // package / import
import "fmt"

type Counter struct{ n int }                 // type / struct

func (c *Counter) Inc() { c.n++ }            // func

func main() {
    var c Counter                            // var
    const limit = 3                          // const
    for i := 0; i < limit; i++ {             // for
        switch {                             // switch
        case i == 0:
            continue                         // continue
        default:
            defer fmt.Println("done")        // defer
            go c.Inc()                       // go
            select {}                        // select
        }
        break                                // break
    }
}
```

25 个关键字里没有"类""枚举""异常"这类词，这正是 Go 的设计取向。真正容易踩的是**预声明标识符**：`bool`, `byte`, `int`, `rune`, `string`, `error`, `nil`, `true`, `iota`, `len`, `cap`, `make`, `new`, `append`, `copy`, `delete`, `panic`, `recover`, `print`, `println`（以及 Go 1.21 加入的 `min`, `max`, `clear`）都**不是关键字**，你可以写 `int := 3` 把类型名遮蔽掉——合法但极其危险。

**几个特殊的关键字**：`defer` 延迟到函数返回前执行；`go` 启动 goroutine；`select` 在多路 channel 上等待；`fallthrough` 强制贯穿到下一个 case（Go 的 `switch` 默认不贯穿）；`range` 是 `for` 的特殊形式；`chan`, `interface`, `map` 是类型构造关键字。

📘 [Go spec · Keywords](https://go.dev/ref/spec#Keywords)、[Predeclared identifiers](https://go.dev/ref/spec#Predeclared_identifiers)

{{% /tab %}}

{{% tab header="Python" %}}

Python 3.14 有 **35 个关键字**，另有 4 个"软关键字"（只在特定语法里才是关键字）。

| 类别 | 关键字 |
| --- | --- |
| 声明与定义（8 个） | `class`, `def`, `lambda`, `global`, `nonlocal`, `import`, `from`, `as` |
| 控制流（11 个） | `if`, `elif`, `else`, `for`, `while`, `break`, `continue`, `return`, `pass`, `match`* `case`* |
| 异常（5 个） | `try`, `except`, `finally`, `raise`, `assert` |
| 逻辑与成员（5 个） | `and`, `or`, `not`, `in`, `is` |
| 异步（2 个） | `async`, `await` |
| 上下文管理（3 个） | `with`, `yield`, `del` |
| 字面量（3 个） | `True`, `False`, `None` |
| 软关键字（4 个） | `_`, `case`, `match`, `type` |

**本表合计：41 个条目。**

```python
import asyncio
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

async def fetch(points):
    async with asyncio.TaskGroup() as tg:      # async / with
        for p in points:
            tg.create_task(handle(p))

def classify(value):
    match value:                               # match 是软关键字
        case int() as n if n > 0:              # case / as / if
            return "positive"
        case _:
            return "other"

try:
    assert classify(1) is not None
except AssertionError as e:
    raise RuntimeError from e
```

软关键字的好处是**向后兼容**：`match`, `case`, `_`, `type` 在别的上下文里仍然是合法标识符，比如 `match = 1`, `def type(): ...` 都能跑。另外注意 `print` 和 `exec` 早就不是关键字了（Python 3 起是普通函数），`None`, `True`, `False` 是关键字，而 `NotImplemented`, `Ellipsis` 只是名字。

**几个特殊的关键字**：`match`, `case`, `type`, `_` 是软关键字，只在对应语句里生效；`async`, `await` 自 3.7 起是正式关键字；`global`, `nonlocal` 声明作用域；`assert` 在 `-O` 优化模式下会被整个移除；`None`, `True`, `False` 是关键字而不是普通名字。

📘 [Python docs · `keyword`](https://docs.python.org/3/library/keyword.html)、[Lexical analysis · Keywords](https://docs.python.org/3/reference/lexical_analysis.html#keywords)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 把词法分成三档：**硬关键字**（31 个，永远不能当标识符）、**软关键字**（19 个，只在特定上下文生效）、**修饰符关键字**（31 个，只在修饰符位置生效）。这三档合起来才是官方"关键字参考"页的完整内容。

| 档位 | 关键字 |
| --- | --- |
| 硬关键字（31 个） | `as`, `as?`, `break`, `class`, `continue`, `do`, `else`, `false`, `for`, `fun`, `if`, `in`, `!in`, `interface`, `is`, `!is`, `null`, `object`, `package`, `return`, `super`, `this`, `throw`, `true`, `try`, `typealias`, `typeof`, `val`, `var`, `when`, `while` |
| 软关键字（19 个） | `by`, `catch`, `constructor`, `context`, `delegate`, `dynamic`, `field`, `file`, `finally`, `get`, `import`, `init`, `param`, `property`, `receiver`, `set`, `setparam`, `value`, `where` |
| 修饰符关键字（29 个） | `abstract`, `actual`, `annotation`, `companion`, `const`, `crossinline`, `data`, `enum`, `expect`, `external`, `final`, `infix`, `inline`, `inner`, `internal`, `lateinit`, `noinline`, `open`, `operator`, `out`, `override`, `private`, `protected`, `public`, `reified`, `sealed`, `suspend`, `tailrec`, `vararg` |

**本表合计：79 个条目。**

```kotlin
package demo                              // package

import kotlin.math.PI                     // import

sealed interface Shape                    // sealed / interface
data class Circle(val r: Double) : Shape  // data / class / val
data object Empty : Shape                 // object

inline fun <reified T> nameOf(x: T): String = T::class.simpleName ?: "?"

fun area(s: Shape): Double = when (s) {    // fun / when / is
    is Circle -> PI * s.r * s.r
    Empty -> 0.0
}

fun main() {
    val list = listOf(Circle(1.0), Empty)
    for (s in list) {                      // for / in
        if (s !is Empty) println(area(s))   // if / !is
    }
}
```

软关键字和修饰符关键字都能当普通标识符：`val by = 1`, `val get = 2`, `val data = 3` 都是合法的（只是可读性差）。真正被卡死的是 31 个硬关键字，比如你不能写 `val class = 1`；如果确实要用，可以加反引号：`` val `class` = 1 ``。`field`（2.2+ 显式 backing field）和 `context`（上下文参数）是较新加入的软关键字。

**几个特殊的关键字**：`!in`, `!is` 是"取反的成员/类型检查"；`typealias` 声明类型别名；`typeof` 被保留但尚未使用；`field`（2.2+）是访问属性 backing field 的软关键字；`context` 用于上下文参数；`object` 一词同时承担对象声明、伴生对象与匿名对象三种用途。

📘 [Kotlin · Keywords and operators](https://kotlinlang.org/docs/keyword-reference.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 JLS 把词法分成 **50 个保留关键字**（含 `_`）和 **17 个上下文关键字**；`true`, `false`, `null` 是字面量而不是关键字。

| 档位 | 词表 |
| --- | --- |
| 保留关键字（51 个） | `abstract`, `assert`, `boolean`, `break`, `byte`, `case`, `catch`, `char`, `class`, `const`, `continue`, `default`, `do`, `double`, `else`, `enum`, `extends`, `final`, `finally`, `float`, `for`, `goto`, `if`, `implements`, `import`, `instanceof`, `int`, `interface`, `long`, `native`, `new`, `package`, `private`, `protected`, `public`, `return`, `short`, `static`, `strictfp`, `super`, `switch`, `synchronized`, `this`, `throw`, `throws`, `transient`, `try`, `void`, `volatile`, `while`, `_` |
| 上下文关键字（17 个） | `exports`, `module`, `non-sealed`, `open`, `opens`, `permits`, `provides`, `record`, `requires`, `sealed`, `to`, `transitive`, `uses`, `var`, `when`, `with`, `yield` |
| 字面量（不是关键字）（3 个） | `true`, `false`, `null` |

**本表合计：71 个条目。**

```java
package demo;                                  // package
import java.util.List;                         // import

public sealed interface Shape permits Circle { }   // public / sealed / interface / permits
record Circle(double r) implements Shape { }        // record / implements

public class Demo {
    public static void main(String[] args) {
        var list = List.of(new Circle(1.0));        // var 是上下文关键字
        for (var s : list) {                       // for
            switch (s) {                           // switch
                case Circle c when c.r() > 0 ->    // case / when（21+）
                    System.out.println(Math.PI * c.r() * c.r());
                default -> System.out.println("?");
            }
        }
    }
}
```

`const` 和 `goto` 被保留但从不使用（方便编译器给出更好的报错），`strictfp` 已经过时，`_`（下划线）是关键字但只能用于"未命名变量"（Java 22 起也叫 unnamed variables）。上下文关键字在别的地方是合法标识符：`var var = 1;` 这类写法虽然能编译，但显然不该出现在真实代码里。

**几个特殊的关键字**：`const`, `goto` 被保留但从不使用；`_` 从 Java 22 起只能作未命名变量/模式；`strictfp` 已过时（Java 17 起浮点运算一律 strict）；`var`, `record`, `sealed`, `permits`, `when`, `yield` 都是上下文关键字；`assert` 需要以 `-ea` 启动才会执行。

📘 [JLS §3.9 Keywords](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.9)、[JLS §3.10 Literals](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.10)

{{% /tab %}}

{{% tab header="C++" %}}

C++23 有 **91 个关键字**（含 11 个替代记号；不含 C++26 的 `contract_assert` 与 TM/反射 TS 的关键字），另有若干"上下文关键字"（只有在特定语法位置才是关键字）。

| 类别 | 关键字 |
| --- | --- |
| 声明与类型（41 个） | `auto`, `bool`, `char`, `char8_t`, `char16_t`, `char32_t`, `class`, `const`, `constexpr`, `consteval`, `constinit`, `decltype`, `double`, `enum`, `explicit`, `extern`, `float`, `friend`, `inline`, `int`, `long`, `mutable`, `namespace`, `operator`, `short`, `signed`, `sizeof`, `static`, `struct`, `template`, `thread_local`, `typedef`, `typeid`, `typename`, `union`, `unsigned`, `using`, `virtual`, `void`, `volatile`, `wchar_t` |
| 控制流（15 个） | `break`, `case`, `catch`, `continue`, `default`, `do`, `else`, `for`, `goto`, `if`, `return`, `switch`, `throw`, `try`, `while` |
| 表达式与转换（22 个） | `and`, `and_eq`, `bitand`, `bitor`, `compl`, `delete`, `dynamic_cast`, `false`, `new`, `noexcept`, `not`, `not_eq`, `nullptr`, `or`, `or_eq`, `reinterpret_cast`, `static_assert`, `static_cast`, `this`, `true`, `xor`, `xor_eq` |
| 概念与协程（C++20）（5 个） | `concept`, `requires`, `co_await`, `co_return`, `co_yield` |
| 访问控制与其他（13 个） | `alignas`, `alignof`, `asm`, `const_cast`, `export`, `private`, `protected`, `public`, `register`, `synchronized`, `atomic_cancel`, `atomic_commit`, `atomic_noexcept` |

**本表合计：96 个条目。**

```cpp
#include <concepts>
#include <cstdint>
#include <string>

template <typename T> concept Addable = requires(T a, T b) { a + b; };   // template/concept/requires

class Counter {                                     // class
public:                                             // public
    explicit Counter(int start) noexcept : n_{start} {}   // explicit/noexcept
    virtual ~Counter() = default;                   // virtual
    constexpr int get() const { return n_; }        // constexpr/const
private:                                            // private
    int n_{};
};

static_assert(Addable<int>);                        // static_assert

int main() {
    auto c = Counter{1};                            // auto
    if (c.get() > 0) { c = Counter{2}; }            // if/else
    while (false) { break; }                        // while/break/false
    return 0;
}
```

C++ 的关键字里有一组**替代记号**：`and`, `or`, `not`, `bitand`, `bitor`, `xor`, `compl`, `and_eq`, `or_eq`, `not_eq`, `xor_eq` 分别是 `&&`, `||`, `!`, `&`, `|`, `^`, `~`, `&=`, `|=`, `!=`, `^=` 的另一种写法，在键盘缺符号的年代很有用。另外 `final` 和 `override`（C++11）以及 `import`, `module`（C++20）是**上下文关键字**：它们只在特定位置才是关键字，所以老代码里叫 `final` 的变量仍然能编译。C++26 又加了 `contract_assert`，本文按 C++23 列出。

**几个特殊的关键字**：`concept`, `requires` 是 C++20 的约束机制；`co_await`, `co_return`, `co_yield` 用于协程；`and`, `or`, `not`, `bitand` 等 11 个是替代记号；`final`, `override` 是上下文关键字；`export` 在 C++20 改用于模块；`thread_local`, `constinit`, `consteval` 分别控制存储期与求值时机。

📘 [cppreference · C++ keywords](https://en.cppreference.com/w/cpp/keyword)

{{% /tab %}}

{{% tab header="C" %}}

C23 把 C 的保留关键字扩到 **59 个**（另有 `asm`, `fortran` 两个条件支持）：旧的一批 `_Xxx` 拼写（`_Bool`, `_Static_assert` 等）仍然保留，同时新增了不带下划线的现代拼写。

| 类别 | 关键字 |
| --- | --- |
| 类型与声明（27 个） | `auto`, `char`, `const`, `constexpr`, `double`, `enum`, `extern`, `float`, `inline`, `int`, `long`, `register`, `restrict`, `short`, `signed`, `sizeof`, `static`, `struct`, `typedef`, `union`, `unsigned`, `void`, `volatile`, `_BitInt`, `bool`, `true`, `false` |
| 控制流（12 个） | `break`, `case`, `continue`, `default`, `do`, `else`, `for`, `goto`, `if`, `return`, `switch`, `while` |
| 类型工具（5 个） | `alignas`, `alignof`, `typeof`, `typeof_unqual`, `nullptr` |
| 断言与线程（2 个） | `static_assert`, `thread_local` |
| 旧拼写（仍保留）（13 个） | `_Alignas`, `_Alignof`, `_Atomic`, `_Bool`, `_Complex`, `_Decimal32`, `_Decimal64`, `_Decimal128`, `_Generic`, `_Imaginary`, `_Noreturn`, `_Static_assert`, `_Thread_local` |
| 条件支持（2 个） | `asm`, `fortran` |

**本表合计：61 个条目。**

```c
#include <stdbool.h>
#include <stddef.h>

typedef struct { int x, y; } point_t;      /* typedef / struct */

static inline int area(point_t p) {        /* static / inline */
    return p.x * p.y;
}

int main(void) {
    constexpr int limit = 3;                /* C23: constexpr */
    typeof(limit) i = 0;                    /* C23: typeof */
    for (i = 0; i < limit; i++) {           /* for */
        if (i == 0) continue;               /* if / continue */
        else break;                         /* else / break */
    }
    bool ok = true;                         /* C23: bool / true */
    void *p = nullptr;                      /* C23: nullptr */
    _Static_assert(sizeof(point_t) >= 8, "size");   /* 旧拼写仍然有效 */
    return ok && p == NULL ? 1 : 0;         /* return / && */
}
```

C23 的关键字变化值得记住：`bool`, `true`, `false`, `nullptr`, `constexpr`, `typeof`, `typeof_unqual`, `alignas`, `alignof`, `static_assert`, `thread_local`, `_BitInt` 成为关键字，过去要包含 `<stdbool.h>` 或写 `_Bool`。旧拼写（`_Bool`, `_Static_assert` 等）依然保留是为了兼容，写新代码时优先用新拼写。`asm` 和 `fortran` 是"条件支持"的（实现可以拒绝）。

**几个特殊的关键字**：`_Generic` 做编译期类型分派；`_BitInt(N)` 定义任意位宽整数；`static_assert`, `_Static_assert` 做编译期断言；`typeof`, `typeof_unqual` 取表达式类型；`restrict` 是给编译器的优化承诺；`_Noreturn` 自 C23 起弃用（改用 `[[noreturn]]`）；`asm`, `fortran` 是条件支持的关键字。

📘 [cppreference · C keywords](https://en.cppreference.com/w/c/keyword)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的保留字不多：解析器明确列出的有 **28 个**，另有几个"只在特定语法里才保留"的词（`mutable`, `primitive`, `abstract`, `outer`, `public`, `where`）。

| 类别 | 关键字 |
| --- | --- |
| 声明与模块（11 个） | `function`, `macro`, `struct`, `module`, `baremodule`, `using`, `import`, `export`, `local`, `global`, `const` |
| 控制流（16 个） | `begin`, `end`, `if`, `else`, `elseif`, `while`, `for`, `break`, `continue`, `return`, `try`, `catch`, `finally`, `do`, `let`, `quote` |
| 字面量（2 个） | `true`, `false` |
| 上下文关键字（7 个） | `mutable`（`mutable struct`）`primitive`, `abstract`, `outer`, `public`（1.11+）`where`（类型参数） |

**本表合计：36 个条目。**

```julia
module Demo                                  # module
export area                                  # export

abstract type Shape end                      # abstract / type

mutable struct Circle <: Shape               # mutable / struct
    r::Float64
end

area(c::Circle) = π * c.r^2                  # 函数定义（无 function 关键字）

function describe(s::Shape)                  # function
    if s isa Circle                          # if / isa（运算符）
        return "circle"
    elseif s isa Nothing
        return "none"
    else
        error("unknown")
    end
end

let c = Circle(1.0)                          # let
    try
        println(describe(c))
    catch err                                  # catch
        println(err)
    finally
        println("done")                        # finally
    end
end
```

Julia 的关键字有两个特殊之处：一是 **`in` 和 `isa` 不是关键字而是运算符**（`isa` 是二元运算符），所以你可以写 `in = 1`；二是 `mutable`, `primitive`, `abstract`, `outer`, `public`, `where` 只在特定位置才是保留字（`mutable struct`, `abstract type`, `for outer i = ...`, `f(x) where T`）。另外 `public` 是 Julia 1.11 新增的（配合 `export` 表达"公开但不导出"）。

**几个特殊的关键字**：`do` 把函数作为第一个参数传入（`map(xs) do x ... end`）；`where` 声明类型参数；`mutable`, `abstract`, `primitive` 只在类型定义处生效；`public`（1.11+）表示"公开但不导出"；`begin`, `end` 既是块界定符也能做索引（`v[begin]`, `v[end]`）；`in`, `isa` 其实是运算符而不是关键字。

📘 [Julia · Keywords](https://docs.julialang.org/en/v1/base/base/#Keywords)、[Julia parser 源码中的保留字表](https://github.com/JuliaLang/julia/blob/master/src/julia-parser.scm)

{{% /tab %}}

{{% tab header="C#" %}}

C# 有 **77 个保留关键字**，另有 40 个"上下文关键字"（在别处可以当普通标识符）。

| 类别 | 关键字 |
| --- | --- |
| 类型（18 个） | `bool`, `byte`, `char`, `decimal`, `double`, `enum`, `float`, `int`, `long`, `object`, `sbyte`, `short`, `string`, `struct`, `uint`, `ulong`, `ushort`, `void` |
| 声明与修饰（24 个） | `abstract`, `async`, `class`, `const`, `delegate`, `event`, `extern`, `fixed`, `internal`, `namespace`, `new`, `override`, `params`, `private`, `protected`, `public`, `readonly`, `ref`, `sealed`, `static`, `unsafe`, `using`, `virtual`, `volatile` |
| 控制流（17 个） | `break`, `case`, `catch`, `continue`, `default`, `do`, `else`, `finally`, `for`, `foreach`, `goto`, `if`, `return`, `switch`, `throw`, `try`, `while` |
| 表达式与转换（19 个） | `as`, `await`, `base`, `checked`, `explicit`, `false`, `implicit`, `in`, `is`, `lock`, `null`, `operator`, `out`, `sizeof`, `stackalloc`, `this`, `true`, `typeof`, `unchecked` |
| 上下文关键字（42 个） | `add`, `alias`, `and`, `ascending`, `args`, `by`, `descending`, `dynamic`, `equals`, `field`, `file`, `from`, `get`, `global`, `group`, `init`, `into`, `join`, `let`, `managed`, `nameof`, `nint`, `not`, `notnull`, `nuint`, `on`, `or`, `orderby`, `partial`, `record`, `remove`, `required`, `scoped`, `select`, `set`, `unmanaged`, `value`, `var`, `when`, `where`, `with`, `yield` |

**本表合计：120 个条目。**

```csharp
namespace Demo;                                  // namespace

public abstract record Shape;                    // public / abstract / record
public sealed record Circle(double R) : Shape;   // sealed

public class Demo
{
    public static string Describe(Shape s) => s switch   // switch
    {
        Circle { R: > 0 } c => $"circle {c.R}",      // when 也可以写在这里
        _ => "unknown",
    };

    public static void Main()
    {
        var shapes = new[] { new Circle(1.0) };      // var 是上下文关键字
        foreach (var s in shapes)                    // foreach / in
        {
            checked                                    // checked
            {
                if (s is Circle c) Console.WriteLine(Describe(c));   // if / is
            }
        }
    }
}
```

上下文关键字是 C# 的特色：`var`, `async`, `await`, `record`, `required`, `nameof`, `when`, `with`, `init`, `global` 等 40 个词都能当普通标识符（`int var = 1;` 合法）。真正被卡死的是 77 个保留关键字；如果非要用保留字当标识符（比如做 JSON 字段名），加 `@` 前缀即可：`var @class = 1;`。C# 14 新增的 `field` 是上下文关键字（用于属性 backing field）。

**几个特殊的关键字**：`partial`, `where` 在不同上下文有不同含义；`async`, `await` 是上下文关键字；`yield` 用于迭代器方法；`record`, `init`, `required` 用于不可变数据；`field`（C# 14）访问属性的 backing field；`scoped`, `file` 分别限制生命周期与可见性；`checked`, `unchecked` 控制溢出检查。

📘 [MS Learn · C# keywords](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的关键字表分四档（官方数据文件共 69 条，去重后 67 个词）：**reserved**（官方 34 条，去重后 33 个，完全不能用）、**built-in identifier**（24 个，不能当类型名/导入前缀，其他场合可以用）、**context**（2 个，只在特定上下文）、**unrestricted**（官方 9 条，去重后 8 个，基本随便用）。

| 档位 | 词表 |
| --- | --- |
| reserved（33 个） | `assert`, `break`, `case`, `catch`, `class`, `const`, `continue`, `default`, `do`, `else`, `enum`, `extends`, `false`, `final`, `finally`, `for`, `if`, `in`, `is`, `new`, `null`, `rethrow`, `return`, `super`, `switch`, `this`, `throw`, `true`, `try`, `var`, `void`, `while`, `with` |
| built-in identifier（24 个） | `abstract`, `as`, `covariant`, `deferred`, `dynamic`, `export`, `extension`, `external`, `factory`, `Function`, `get`, `implements`, `import`, `interface`, `late`, `library`, `mixin`, `operator`, `part`, `required`, `set`, `static`, `typedef`, `type` |
| context（2 个） | `await`, `yield` |
| unrestricted（8 个） | `async`, `hide`, `of`, `on`, `sealed`, `show`, `sync`, `when` |

**本表合计：67 个条目。**

```dart
import 'dart:async';                     // import

mixin Drawable {                         // mixin
  void draw() => print('draw');
}

sealed class Shape with Drawable { }     // sealed（unrestricted）/ with
final class Circle extends Shape {       // final / extends
  final double r;
  const Circle(this.r);                  // const
}

Future<void> main() async {              // async（unrestricted）
  var shapes = <Shape>[Circle(1.0)];     // var
  for (final s in shapes) {              // for / in
    if (s is Circle) {                   // if / is
      print(s.r);
    } else if (s case Circle(r: var r)) { // 模式匹配里的 case
      print(r);
    }
  }
  await Future<void>.delayed(Duration.zero);   // await（context）
}
```

Dart 的 `final` 和 `var` 是保留字（不能当变量名），但 `sealed`, `base`, `interface`, `when`, `sync` 这些"类修饰符/上下文词"其实属于 unrestricted 档，做标识符完全合法。`await` 和 `yield` 只在 `async` 函数体里才是关键字（context 档）。因为 Dart 有 `as`, `is`, `in` 这些关键字，写混合语言代码时最容易在这里手滑。

**几个特殊的关键字**：`covariant` 放宽参数的类型覆盖规则；`late` 做延迟初始化（有运行时检查）；`required` 标注命名参数必填；`factory` 声明工厂构造函数；`deferred` 延迟加载库；`await`, `yield` 只在 `async` 函数体里才是关键字；`show`, `hide` 控制导入哪些成员。

📘 [dart.dev · Keywords](https://dart.dev/language/keywords)

{{% /tab %}}

{{% tab header="R" %}}

R 的保留字只有 **20 个**，但 R 的类型系统靠"属性"而不是关键字，所以这份清单比别的语言短得多。

| 类别 | 保留字 |
| --- | --- |
| 控制流（8 个） | `if`, `else`, `repeat`, `while`, `for`, `in`, `next`, `break` |
| 定义（1 个） | `function` |
| 字面量常量（5 个） | `TRUE`, `FALSE`, `NULL`, `Inf`, `NaN` |
| 缺失值（5 个） | `NA`, `NA_integer_`, `NA_real_`, `NA_complex_`, `NA_character_` |
| 特殊记号（3 个） | `...`（以及 `..1`, `..2` 等，用于引用调用方传下来的参数） |

**本表合计：22 个条目。**

```r
add <- function(a, b = 1) a + b          # function

describe <- function(x) {
  if (is.na(x)) {                        # if / is.na
    "missing"
  } else if (is.infinite(x)) {           # else / Inf 判断
    "infinite"
  } else {
    repeat {                             # repeat
      break                              # break
    }
    "value"
  }
}

for (i in 1:3) next                      # for / in / next

vals <- c(1, NA_integer_, Inf, NaN)      # NA_integer_ / Inf / NaN
stopifnot(TRUE, !FALSE, is.null(NULL))   # TRUE / FALSE / NULL

f <- function(...) sum(...)              # 特殊记号 ...
f(1, 2, 3)
```

保留字按 R 的规则"即使不在引号里也总是被解析成内建对象"，所以不能直接当变量名；但用反引号可以绕开：`` `if` <- 1 `` 是合法的（虽然不建议）。注意 `NA_integer_`, `NA_real_`, `NA_character_` 是**带类型的缺失值**，和 `NA` 一样都在保留字清单里；`T`, `F` 不是保留字，很多人把它们当 `TRUE`, `FALSE` 用，但可以被覆盖，正式代码里不要这么写。

**几个特殊的关键字**：`...`, `..1`, `..2` 用于把参数转发给内层函数；`repeat` 是 R 里唯一的先循环结构（配合 `break` 退出）；`next` 相当于其他语言的 `continue`；`NA_integer_`, `NA_real_`, `NA_character_` 是带类型的缺失值；`Inf`, `NaN` 是保留常量；`T`, `F` **不是**保留字，可以被覆盖，正式代码不要用。

📘 [R · Reserved Words](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Reserved.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的关键字非常"直白"：**46 个**，而且没有软关键字这一层——因为 Zig 用 `@"..."` 语法给关键字"开了一个后门"。

| 类别 | 关键字 |
| --- | --- |
| 声明与类型（15 个） | `const`, `var`, `fn`, `struct`, `enum`, `union`, `opaque`, `error`, `comptime`, `anytype`, `anyframe`, `pub`, `export`, `extern`, `test` |
| 控制流（13 个） | `if`, `else`, `switch`, `while`, `for`, `break`, `continue`, `return`, `defer`, `errdefer`, `unreachable`, `suspend`, `resume` |
| 内存与属性（11 个） | `align`, `allowzero`, `addrspace`, `linksection`, `threadlocal`, `volatile`, `noalias`, `callconv`, `noinline`, `inline`, `packed` |
| 错误处理与逻辑（8 个） | `try`, `catch`, `orelse`, `and`, `or`, `asm`, `usingnamespace`, `nosuspend` |

**本表合计：47 个条目。**

```zig
const std = @import("std");                     // const

const Direction = enum { north, south };         // enum

const Shape = union(enum) {                      // union(enum)
    circle: f64,
    rect: struct { w: f64, h: f64 },             // struct
};

pub fn area(s: Shape) f64 {                      // pub / fn
    return switch (s) {                           // switch
        .circle => |r| std.math.pi * r * r,
        .rect => |r| r.w * r.h,
    };
}

pub fn main() !void {                             // !void
    var i: u8 = 0;                                // var
    while (i < 3) : (i += 1) {                    // while
        if (i == 1) continue;                     // if / continue
        defer std.debug.print("i={d}\n", .{i});    // defer
    }
    const s = Shape{ .circle = 1.0 };
    std.debug.print("{d}\n", .{area(s)});
}
```

Zig 里最值得记住的不是关键字本身，而是 **`@"..."` 转义写法**：当你想用关键字当标识符时（例如从 C 导入的结构体字段叫 `align`），写 `@""` 形式即可：`const @"if" = 1;`, `x.@"align"`。另外 Zig 的 `and`, `or`, `orelse`, `catch`, `try` 全是关键字，逻辑运算符没有 `&&`, `||` 这种符号写法。

**几个特殊的关键字**：`comptime` 控制编译期求值；`anytype` 让参数类型自动推断；`anyframe`, `suspend`, `resume`, `nosuspend` 属于异步机制的遗留关键字；`noalias` 是对编译器的别名承诺；`@"..."` 让关键字（甚至任意字符串）变成标识符；`usingnamespace`, `async`, `await` 已不在当前关键字表里。

📘 [Zig Language Reference · Keyword Reference](https://ziglang.org/documentation/master/#Keyword-Reference)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 5.5 的保留字只有 **23 个**；它们是大小写敏感的（`And` 是合法名字），并且 5.5 新增了一个 `global`（用于声明全局变量）。

| 类别 | 保留字 |
| --- | --- |
| 控制流（13 个） | `if`, `then`, `else`, `elseif`, `end`, `for`, `while`, `repeat`, `until`, `break`, `goto`, `do`, `return` |
| 声明与作用域（3 个） | `local`, `global`（5.5 新增）`function` |
| 逻辑与值（6 个） | `and`, `or`, `not`, `nil`, `true`, `false` |
| 其他（1 个） | `in` |

**本表合计：23 个条目。**

```lua
local function classify(v)              -- local / function
  if v == nil then                      -- if / nil
    return "nil"
  elseif v == false or v == 0 then      -- elseif / false / or
    return "falsey-ish"
  else
    return "other"
  end
end

global counter = 0                      -- Lua 5.5：显式声明全局变量

for i = 1, 3 do                         -- for / do
  if i == 2 then goto continue end      -- goto
  repeat                                -- repeat
    counter = counter + 1
  until counter % 2 == 0                -- until
  ::continue::                          -- 标签
end

while true do break end                 -- while / true / break
print(classify(counter), and)           -- 报错：and 不能当表达式
```

Lua 5.5 的两个变化要记住：`global` 成为保留字（以前可以当变量名），以及 `for` 循环的控制变量变成只读（想改就先 `local i = i`）。保留字不能当普通变量名，但**可以当表字段名**：`t.end = 1`, `t["function"] = 2` 都合法，因为字段名走的是另一套语法。

**几个特殊的关键字**：`goto`（5.2+）跳转到标签，常用来模拟 `continue`；`global`（5.5+）显式声明全局变量；`repeat ... until` 至少执行一次；Lua 没有 `continue` 关键字；`and`, `or`, `not` 是关键字，但用法与运算符无异。

📘 [Lua 5.5 Reference Manual · Lexical Conventions](https://www.lua.org/manual/5.5/manual.html#3.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 7 的词法器里定义了 **85 个关键字**：其中一部分是 JavaScript 保留字，另一部分是 TS 自己的（类型系统与声明相关），这些 TS 关键字在编译后会被完全擦除。

| 类别 | 关键字 |
| --- | --- |
| JS 保留字（运行时仍有意义）（39 个） | `break`, `case`, `catch`, `class`, `const`, `continue`, `debugger`, `default`, `delete`, `do`, `else`, `export`, `extends`, `false`, `finally`, `for`, `function`, `if`, `import`, `in`, `instanceof`, `new`, `null`, `return`, `super`, `switch`, `this`, `throw`, `true`, `try`, `typeof`, `var`, `void`, `while`, `with`, `yield`, `async`, `await`, `of` |
| 类型声明（编译期擦除）（11 个） | `any`, `bigint`, `boolean`, `never`, `number`, `object`, `string`, `symbol`, `undefined`, `unknown`, `void` |
| 类型操作（10 个） | `as`, `asserts`, `assert`, `infer`, `is`, `keyof`, `readonly`, `satisfies`, `type`, `unique` |
| 声明与模块（24 个） | `declare`, `enum`, `interface`, `module`, `namespace`, `abstract`, `implements`, `private`, `protected`, `public`, `override`, `static`, `get`, `set`, `accessor`, `constructor`, `intrinsic`, `package`, `global`, `require`, `from`, `let`, `immediate`, `defer` |

**本表合计：84 个条目。**

```ts
import type { Shape } from "./shapes";          // import / type / from

declare const VERSION: string;                   // declare / const

namespace Geometry {                              // namespace
  export type Point = { x: number; y: number };    // export / type
  export interface Named { name: string }          // interface
  export class Circle implements Named {            // class / implements
    constructor(public name: string, public r: number) {}   // constructor / public
    get area(): number {                            // get
      return Math.PI * this.r ** 2;
    }
  }
}

function describe(s: Shape): string {
  if (s.kind === "circle") return `${s.r}`;        // if / return
  switch (s.kind) {                                 // switch / case
    case "rect": return `${s.w * s.h}`;
    default: return "?";
  }
}

const p = { x: 1, y: 2 } satisfies Geometry.Point;  // satisfies
type Keys = keyof Geometry.Point;                   // keyof
```

TS 关键字的坑在于**语境不同、含义不同**：`as` 在类型断言里是关键字，在 JS 里只是普通标识符；`type` 在类型位置是关键字，但你可以写 `const type = 1`（TS 允许，因为 `type` 属于上下文关键字）；`declare`, `namespace`, `module` 只在声明位置生效。真正被 JS 保留、绝对不能当变量名的是第一组。

**几个特殊的关键字**：`satisfies` 做类型检查但不改变推断出的类型；`keyof`, `infer` 是类型运算；`asserts` 用于断言函数签名；`unique symbol` 产生唯一类型；`declare` 只声明类型、不生成代码；`readonly` 既能修饰属性也能修饰数组类型；`using`（5.2）是资源管理声明。

📘 [TypeScript 7 词法器源码（`textToKeyword`）](https://github.com/microsoft/typescript-go/blob/main/internal/scanner/scanner.go)、[MDN · JavaScript 保留字](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#reserved_words)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的保留字分三层：**普通保留字**（35 个，任何地方都不能当标识符）、**严格模式/模块下才保留**（`let`, `static`, `yield`, `await`）、以及**未来保留字**（目前只有 `enum` 是永久保留）。

| 档位 | 词表 |
| --- | --- |
| 普通保留字（35 个） | `break`, `case`, `catch`, `class`, `const`, `continue`, `debugger`, `default`, `delete`, `do`, `else`, `export`, `extends`, `false`, `finally`, `for`, `function`, `if`, `import`, `in`, `instanceof`, `new`, `null`, `return`, `super`, `switch`, `this`, `throw`, `true`, `try`, `typeof`, `var`, `void`, `while`, `with` |
| 严格模式额外保留（9 个） | `implements`, `interface`, `let`, `package`, `private`, `protected`, `public`, `static`, `yield` |
| 模块 / async 函数里保留（1 个） | `await` |
| 未来保留字（17 个） | `enum`（永久保留）；旧标准里还有 `abstract`, `boolean`, `byte`, `char`, `double`, `final`, `float`, `goto`, `int`, `long`, `native`, `short`, `synchronized`, `throws`, `transient`, `volatile` |

**本表合计：62 个条目。**

```js
import { readFile } from "node:fs/promises";     // import / from

class Counter {                                   // class
  static count = 0;                                // static（严格模式保留，但这里是合法用法）
  #value = 0;                                      // 私有字段
  constructor(start = 0) { this.#value = start; }   // constructor / this
  get value() { return this.#value; }               // get / return
  async load(path) {                                // async（不是保留字）
    const text = await readFile(path, "utf8");       // await（模块里保留字）/ const
    for (const line of text.split("\n")) {            // for / of
      if (line.trim()) this.#value += line.length;    // if / this
    }
    return this.#value;
  }
}

const obj = { class: "ok", if: 1, super: 2 };     // 保留字当属性名完全合法
console.log(obj.class, typeof obj.if);
```

JavaScript 的一个常见误解是"保留字哪儿都不能用"——实际上**保留字可以当属性名**：`obj.class`, `{ if: 1 }`, `x.delete()` 都没问题，因为属性名走的是标识符名而不是标识符文法。被限制的是变量名、函数名、类名、参数名。另外 `let`, `static`, `yield`, `await` 是否保留取决于代码是不是严格模式/模块/async 函数体。

**几个特殊的关键字**：`yield` 只在生成器函数里是关键字；`await` 只在模块或 `async` 函数体里保留；`with` 在严格模式下被禁用；`debugger` 是断点语句；`enum` 被永久保留但没有任何语义；`null` 是字面量，而 `undefined` 只是一个可以被遮蔽的全局属性。

📘 [MDN · Lexical grammar · Reserved words](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#reserved_words)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 有 **约 70 个关键字**（官方叫"保留字"，含 `yield from` 这种两词构造），另有 9 个编译期常量；PHP 的特点是**关键字可以做方法名、属性名和常量名**（只有 `class` 例外）。

| 类别 | 关键字 |
| --- | --- |
| 声明与类型（20 个） | `abstract`, `array`, `callable`, `class`, `const`, `enum`, `extends`, `final`, `fn`, `function`, `implements`, `interface`, `namespace`, `readonly`, `trait`, `var`, `static`, `public`, `protected`, `private` |
| 控制流（26 个） | `break`, `case`, `catch`, `continue`, `declare`, `default`, `do`, `echo`, `else`, `elseif`, `enddeclare`, `endfor`, `endforeach`, `endif`, `endswitch`, `endwhile`, `for`, `foreach`, `goto`, `if`, `match`, `return`, `switch`, `throw`, `try`, `while` |
| 逻辑与语言构造（11 个） | `and`, `or`, `xor`, `as`, `instanceof`, `insteadof`, `new`, `clone`, `print`, `yield`, `yield from` |
| 内建函数式构造（11 个） | `die`, `eval`, `exit`, `empty`, `include`, `include_once`, `isset`, `list`, `require`, `require_once`, `unset` |
| 特殊引用（3 个） | `self`, `parent`, `__halt_compiler` |
| 编译期常量（9 个） | `__CLASS__`, `__DIR__`, `__FILE__`, `__FUNCTION__`, `__LINE__`, `__METHOD__`, `__NAMESPACE__`, `__PROPERTY__`, `__TRAIT__` |

**本表合计：80 个条目。**

```php
<?php
declare(strict_types=1);                        // declare

namespace Demo;                                  // namespace

enum Status: string {                            // enum
    case Ok = 'ok';
    case Failed = 'failed';
}

readonly class Point {                           // readonly / class
    public function __construct(
        public readonly int $x = 0,
        public readonly int $y = 0,
    ) {}

    public function label(): string {             // public / function / return
        return match (true) {                      // match
            $this->x > 0 => 'right',
            default => 'other',
        };
    }
}

$p = new Point(1, 2);                            // new
foreach ([$p] as $item) {                        // foreach / as
    if ($item instanceof Point) {                 // if / instanceof
        echo $item->label();                      // echo
    }
}
```

PHP 的关键字限制比大多数语言宽松：`$obj->class` 不合法，但 `$obj->list()`, `Point::DEFAULT` 这类方法名/常量名里出现关键字是允许的（官方明确说明"关键字可以用作属性、常量和方法名"）。`match`（8.0）、`enum`（8.1）、`readonly`（8.1）、`fn`（7.4）都是较新加入的关键字，老代码里可能把它们当函数名使用——升级 PHP 版本时要检查。

**几个特殊的关键字**：`yield from` 是少数"两个词组成一个关键字"的例子；`match`（8.0）是表达式版 switch；`readonly`（8.1）既是关键字，又允许当函数名；`insteadof` 用来解决 trait 方法冲突；`__halt_compiler()` 停止编译；`clone` 会触发 `__clone`；`die` 与 `exit` 完全同义。

📘 [PHP Manual · List of Keywords](https://www.php.net/manual/en/reserved.keywords.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 4.0 有 **41 个关键字**（含 `BEGIN`, `END`, `__FILE__` 这类全大写/下划线开头的特殊记号）。

| 类别 | 关键字 |
| --- | --- |
| 定义与模块（7 个） | `class`, `module`, `def`, `alias`, `undef`, `BEGIN`, `END` |
| 控制流（17 个） | `if`, `unless`, `elsif`, `else`, `end`, `then`, `case`, `when`, `in`, `while`, `until`, `for`, `break`, `next`, `redo`, `retry`, `return` |
| 异常（4 个） | `begin`, `rescue`, `ensure`, `raise` |
| 逻辑与值（11 个） | `and`, `or`, `not`, `true`, `false`, `nil`, `self`, `super`, `yield`, `defined?`, `do` |
| 特殊记号（3 个） | `__FILE__`, `__LINE__`, `__ENCODING__` |

**本表合计：42 个条目。**

```ruby
module Drawable                              # module
  def draw = "shape"                          # def
end

class Circle                                 # class
  include Drawable
  attr_reader :r
  def initialize(r) = @r = r                 # 3.0+ 无尽方法
  def valid? = r.positive?
end

def classify(x)                              # def
  case x                                     # case
  when nil then "nil"                        # when / nil
  when Integer then "int"
  in [Integer => n, *rest] then "array #{n}"  # in（3.0+ 模式匹配）
  else "other"                               # else
  end
end

begin                                        # begin
  raise ArgumentError, "bad" unless true      # raise / unless / true
rescue ArgumentError => e                     # rescue
  puts e.message
ensure                                        # ensure
  puts __method__                             # 特殊记号
end

puts classify(1) if defined?(classify)        # if / defined?
```

Ruby 的关键字里 `defined?`, `__FILE__`, `__LINE__`, `__ENCODING__` 这几个带 `?` 或下划线的写法属于"特殊记号"，不属于普通标识符命名空间。Ruby 里关键字也不能当局部变量名（`if = 1` 报语法错误），但可以当**方法名**（`def class` 不行，`def if` 也不行；不过 `obj.class`, `obj.send(:if)` 这类反射调用可以）。

**几个特殊的关键字**：`BEGIN`, `END` 在解析阶段执行；`defined?` 检查名字是否已定义；`retry`, `redo` 分别用于异常重试与循环重做；`__FILE__`, `__LINE__`, `__ENCODING__` 是特殊记号而不是普通标识符；`yield` 调用传入的块；`then`, `do` 常常可以省略。

📘 [Ruby · Keywords](https://docs.ruby-lang.org/en/master/keywords_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 硬关键字与软关键字

**一页速览**

| 语言 | 硬关键字能不能当标识符 | 软/上下文关键字怎么判定 | 强行用关键字当名字的办法 |
| --- | --- | --- | --- |
| Rust | 不能 | 弱关键字只在 `union`, `macro_rules`, `'static` 这类位置生效 | `r#type` 原始标识符 |
| Swift | 不能 | 上下文关键字只在声明修饰/表达式里生效 | 反引号 `` `class` `` |
| Go | 不能 | 无软关键字；但预声明标识符可被遮蔽 | 改名字（没有转义语法） |
| Python | 不能 | `match`, `case`, `type`, `_` 只在对应语句里是关键字 | 改名字或加下划线 |
| Kotlin | 不能 | 软关键字与修饰符关键字只在对应上下文生效 | 反引号 `` `is` `` |
| Java | 不能 | `var`, `record`, `sealed`, `when` 等只在特定位置 | 改名字 |
| C++ | 不能 | `final`, `override`, `import`, `module` 只在特定位置 | 改名字 |
| C | 不能 | 无软关键字（C23 之后关键字只增不减） | 改名字 |
| Julia | 不能 | `mutable`, `abstract`, `public`, `where` 只在语法位置生效 | 改名字 |
| C# | 不能 | 47 个上下文关键字只在特定位置生效 | `@class` 前缀转义 |
| Dart | 不能 | 24 个 built-in identifier 只在类型名/前缀位置受限 | 改名字 |
| R | 不能 | 无软关键字 | 反引号 `` `if` `` |
| Zig | 不能 | 无软关键字 | `@"if"` |
| Lua | 不能 | 无软关键字（但字段名不受限） | 用字段名 `t["end"]` |
| TypeScript | 不能（JS 那批） | TS 自己的类型关键字只在类型位置生效 | 改名字；属性名不受限 |
| JavaScript | 不能 | `let`, `static`, `yield`, `await` 视模式而定 | 用属性名 `obj.class` |
| PHP | 不能 | 新关键字只在语法位置生效 | 改名字；方法名/属性名不受限 |
| Ruby | 不能 | 无软关键字 | 用方法名或符号 `:if` |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
let union = 1;          // union 是弱关键字，可以当变量名
let r#type = 2;         // r#type：用原始标识符绕开严格关键字
// let type = 3;        // 🛑 编译错误：type 是严格关键字

macro_rules! m { () => {} }   // macro_rules 只在定义宏时才是关键字
fn f(x: &'static str) {}       // 'static 是弱关键字（生命周期）
```

Rust 只有 39 个严格关键字是绝对禁区；`union`, `macro_rules`, `raw`, `safe`, `'static` 属于弱关键字，只在特定语法位置才有特殊含义，平时完全可以当变量名。真正需要"用关键字当名字"时（例如为 JSON 字段生成结构体），用 `r#` 前缀：`r#type`, `r#match`。

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
let `class` = 1          // 反引号：把关键字当标识符
print(`class`)

let final = 2            // final 是上下文关键字，本来就可以当名字
let lazy = 3
let some = 4

struct S { let `default` = 5 }   // 成员名也能这么写
```

Swift 的上下文关键字（`final`, `lazy`, `weak`, `some`, `Type`…）在语法上就是普通标识符，只在特定位置被解释成关键字。24 个硬关键字（如 `class`, `func`, `if`）想当名字必须加反引号，而且反引号在调用处也要写。

{{% /tab %}}

{{% tab header="Go" %}}

```go
// Go 没有软关键字，25 个关键字一律不能当标识符
// var if = 1        // 🛑 编译错误

func f() {
    int := 3         // ✅ 合法但危险：遮蔽了预声明类型名 int
    len := func() {} // ✅ 合法：len 不是关键字，只是内建函数
    _ = int
    _ = len
}
```

Go 没有"软关键字"这个概念：25 个关键字永远不能用。但要注意**预声明标识符**（`int`, `string`, `error`, `nil`, `len`, `cap`, `make`, `append`, `panic`…）不是关键字，可以被同名变量遮蔽——写 `int := 3` 能编译，但之后这个作用域里就没有 `int` 类型了。

{{% /tab %}}

{{% tab header="Python" %}}

```python
match = 1          # match 是软关键字，可以当变量
case = 2
type = 3           # type 也是软关键字
_ = 4

match match:       # 第一个 match 是语句，第二个是变量
    case 1:
        print("one")

type Alias = int   # 在语句开头，type 才被当成类型别名语法（3.12+）
```

Python 用"软关键字"实现向后兼容：`match`, `case`, `type`, `_` 只在对应语句的语法位置才被当作关键字，别的地方仍是普通名字。这也是为什么 3.10 引入 `match` 语句、3.12 引入 `type X = ...` 都没有破坏老代码。

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
val by = 1        // by 是软关键字
val get = 2
val data = 3      // data 是修饰符关键字，只在 class/data class 里生效
val `is` = 4      // 硬关键字要用反引号
println(`is`)

// val class = 5  // 🛑 class 是硬关键字
```

Kotlin 把关键字分成三档：31 个硬关键字（绝对不能用）、19 个软关键字（`by`, `catch`, `get`, `set`, `field`, `where`…）、29 个修饰符关键字（`data`, `sealed`, `inline`…）。软关键字和修饰符关键字在普通位置就是标识符；硬关键字想当名字只能加反引号。

{{% /tab %}}

{{% tab header="Java" %}}

```java
var var = 1;              // ✅ var 是上下文关键字，可以当变量名
int record = 2;           // ✅ record 也是
String sealed = "x";      // ✅ sealed 也是

// int class = 3;         // 🛑 class 是保留关键字
// int _ = 4;             // 🛑 _ 在 Java 22 之后不能当变量名
```

Java 的 17 个上下文关键字（`var`, `record`, `sealed`, `permits`, `yield`, `when`, `module`, `open`…）在别的地方都是合法标识符，所以 `var var = 1;` 这种写法能编译。真正的禁区是 50 个保留关键字，其中 `const` 和 `goto` 从未使用但一直保留，`_` 从 Java 22 起只能用于"未命名变量"。

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
int final = 1;        // ✅ final 是上下文关键字（只在类/虚函数声明里生效）
int override = 2;     // ✅ 老代码里很常见
int import = 3;       // ✅ C++20 的模块关键字也是上下文相关的

// int class = 4;     // 🛑 class 是关键字
auto and_ = true and false;   // and / or / not 是替代记号（关键字）
```

C++ 的关键字只增不减（从 C++98 的 63 个到 C++23 的 92 个），但 `final`, `override`, `import`, `module` 是**上下文关键字**，只在类声明/模块声明里才有意义，所以 2000 年代写的 `int final = 1;` 至今仍能编译。`and`, `or`, `not` 这一组是 `&&`, `||`, `!` 的替代写法，属于真关键字。

{{% /tab %}}

{{% tab header="C" %}}

```c
/* C 没有软关键字：C23 的 44 个关键字一律不能当标识符 */
// int class = 1;        /* 不可移植：GCC 把 class 当扩展关键字 */
int typeof_x = 1;        /* 避开 C23 新增的 typeof */

/* 实现保留的标识符也不能乱用 */
// int _Foo = 1;         /* 下划线 + 大写：实现保留 */
// int __bar = 2;        /* 双下划线开头：实现保留 */
```

C 没有软关键字，只有"关键字"和"实现保留标识符"两件事。后者常被忽视：以 `_` 加大写字母开头、或以 `__` 开头的名字保留给实现（标准库、编译器），自己定义会踩到冲突。另外 C23 把 `bool`, `true`, `nullptr`, `typeof`, `constexpr` 变成关键字，老代码里叫 `typeof` 的变量/函数在 C23 下需要改名。

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
public = 1          # ✅ public 是上下文关键字（1.11+），可以当变量
mutable = 2         # ✅ 只在 mutable struct 里才特殊
where = 3           # ✅ 只在类型参数位置才特殊

in = 4              # ✅ in 是运算符，不是关键字
isa = 5             # ✅ 同上

# if = 6            # 🛑 if 是保留字
```

Julia 的保留字表很短（28 个），其余"看起来像关键字"的东西分两种情况：`mutable`, `primitive`, `abstract`, `outer`, `public`, `where` 是上下文关键字（只在特定语法位置生效）；`in`, `isa` 干脆就是运算符，可以当变量名。保留字里最常撞的是 `end`, `do`, `global`, `local`。

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
int var = 1;                 // ✅ var 是上下文关键字
string record = "x";          // ✅ record 也是
int when = 2;                 // ✅ when 也是

int @class = 3;               // ✅ 用 @ 前缀把保留字当标识符
Console.WriteLine(@class);
// int class = 4;             // 🛑 class 是保留关键字
```

C# 的 77 个保留关键字绝对不能用（除非加 `@` 前缀），40 个上下文关键字（`var`, `async`, `await`, `record`, `required`, `nameof`, `when`, `with`, `init`, `field`…）在普通位置就是标识符。C# 14 的 `field` 也是上下文关键字，写属性 backing field 时才会被特殊解释。

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
var sealed = 1;      // ✅ sealed 属于 unrestricted 档
var when = 2;        // ✅ 同上
var late = 3;        // ✅ late 是 built-in identifier：不能当类型名，但能当变量名

// var class = 4;     // 🛑 reserved
// var await = 5;     // ⚠️ 在 async 函数体里，await 是 context 关键字
```

Dart 用四档来管理：34 个 `reserved` 真不能用；24 个 `built-in identifier`（`late`, `required`, `factory`, `mixin`, `operator`…）不能当类型名/扩展名/导入前缀，但其他场合可以当标识符；`await`, `yield` 是 `context` 档；`async`, `sealed`, `when`, `sync` 等是 `unrestricted`。

{{% /tab %}}

{{% tab header="R" %}}

```r
`if` <- 1            # 用反引号把保留字当变量名（合法但别这么写）
print(`if`)

for (i in 1:3) print(i)     # for / in 是保留字

x <- 1
x$if <- 2                    # 作为列表元素名（字段名）合法
names(x)
```

R 没有软关键字：20 个保留字一律按内建对象解析。但两个"后门"很有用：一是反引号 `` `if` `` 可以当变量名；二是**字段名不受限制**，`x$if`, `list(class = 1)` 这类写法在数据框/列表里非常常见（`data.frame` 的列名可以是任何东西）。

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const @"if" = 1;             // @"..." 把关键字变成标识符
const @"align" = 2;

const S = struct {
    @"type": u8 = 0,          // 字段名同样支持
};

const x: u8 = S{}.@"type";
```

Zig 没有软关键字，46 个关键字全都是硬的——但它给了 `@"..."` 这个统一的后门：任何关键字（甚至任何字符串）都能写成标识符。写 C 互操作代码时特别有用，因为 C 结构体字段可能叫 `align`, `type`, `linksection`。

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
-- Lua 没有软关键字；23 个保留字不能当变量名
-- local if = 1        -- 🛑 语法错误

local t = {}
t.end = 1                 -- ✅ 字段名不受限
t["function"] = 2
print(t.end, t["function"])

local End = 3             -- ✅ 大小写敏感：End 不是保留字
```

Lua 的保留字大小写敏感（`End`, `END` 都是合法名字），而且**只有变量名受限**：表字段名、字符串键随便用 `t.end`, `t["while"]`。这是配置文件式 Lua 代码里非常常见的写法。

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
const type = 1;        // ✅ type 是上下文关键字
const as = 2;          // ✅ as 只在断言/导入别名位置才特殊
const namespace = 3;   // ✅ 同上
const satisfies = 4;   // ✅ satisfies 只在类型位置特殊

// const enum = 5;     // 🛑 enum 是 JS 保留字
const obj = { class: 1, if: 2, delete: 3 };   // ✅ 属性名不受限
```

TS 的关键字分两类：从 JS 继承的保留字（`class`, `enum`, `delete`, `if`…）绝对不能当变量名；TS 自己加的类型关键字（`type`, `as`, `namespace`, `satisfies`, `readonly`, `out`, `override`…）属于上下文关键字，只在类型位置才特殊。属性名不受任何限制。

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
// 普通保留字不能当变量名
// const class = 1;          // 🛑

const obj = { class: 1, if: 2, delete: 3 };   // ✅ 属性名可以
obj.class;

// let / static / yield / await 视上下文而定
function f() { "use strict"; /* let x = 1; 合法 */ }
async function g() { /* await 在这里是关键字 */ }
```

JavaScript 的保留字只限制变量名、函数名、类名与参数名；**属性名完全不受限**。`let`, `static`, `yield` 只在严格模式（或特定声明里）保留，`await` 只在模块/async 函数体里保留。写老式代码时常见的坑是把 `class` 当变量名——在 ES5 之前它是合法的，现在不行了。

{{% /tab %}}

{{% tab header="PHP" %}}

```php
// 关键字不能当函数名/类名，但可以是方法名、属性名、常量名
class Demo {
    public const DEFAULT = 1;        // ✅ 常量名
    public function list(): array {  // ✅ 方法名用关键字
        return [];
    }
}

$d = new Demo();
echo $d->list()[0] ?? '';

// function class() {}             // 🛑 class 不能当函数名
// class if {}                     // 🛑
```

PHP 的限制比大多数语言宽松：官方明确说关键字"不能用作常量名、类名或函数名，但允许作为属性、常量、方法名（`class` 除外）"。所以 `$obj->list()`, `Foo::DEFAULT`, `$obj->for` 都是合法的，这也是为什么 PHP 代码里能看到很多"像关键字的"方法名。

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
# 关键字不能当局部变量名
# if = 1          # 🛑 语法错误

obj = Object.new
obj.class            # ✅ class 作为方法名（Object#class）完全合法
obj.send(:if) rescue nil   # ✅ 反射调用

h = { if: 1, class: 2 }     # ✅ 哈希键（符号）不受限
h[:if]
```

Ruby 没有软关键字：41 个关键字在词法层就确定了。但关键字可以当**方法名**和**符号**：`obj.class`, `{ if: 1 }`, `:class` 都合法（`obj.class` 是 Object 的内建方法）。局部变量和参数名才是禁区。

{{% /tab %}}

{{< /tabpane >}}

### 保留但未使用与未来保留字

"保留字"有两种含义：一种是**现在没人用、留给未来**的词（编译器一见到就报错，防止你占坑），另一种是**历史上用过、现在废弃**的词。这一节按语言列出这两种情况——没有这种情况的语言也会明确说明。

**一页速览**

| 语言 | 有没有未来保留字 | 关键内容 |
| --- | --- | --- |
| Rust | ✓ | 14 个保留字（`abstract`, `become`, `box`, `do`, `final`, `macro`, `override`, `priv`, `try`, `typeof`, `unsized`, `virtual`, `yield`）+ 2024 的 `gen` |
| Swift | ✗ | 新能力走上下文关键字或宏（`#file` 等已改为宏） |
| Go | ✗ | 新能力通过预声明标识符加入（`min`, `max`, `clear`） |
| Python | ✗（用软关键字） | `match`, `case`, `type`, `_` |
| Kotlin | ✓ | `typeof` 保留给未来使用 |
| Java | ✓ | `const`, `goto` 保留未用；`_` 从 22 起只作未命名变量；`strictfp` 过时 |
| C++ | ✗（关键字只增不减） | TS（`atomic_*`, `synchronized`, `reflexpr`）与 C++26 的 `contract_assert` 已在关键字表里 |
| C | ✓ | `_Decimal32/64/128`, `_Imaginary` 保留但极少实现；`_Noreturn` 自 C23 起弃用 |
| Julia | ✓（历史） | 旧的 `type` 已废弃，现在是普通标识符 |
| C# | ✗ | 新特性全部走上下文关键字（`var`, `async`, `record`, `required`, `field`） |
| Dart | ✗ | 用 reserved / built-in identifier / context / unrestricted 四档管理 |
| R | ✗ | 保留字表极小且稳定；`...`, `..1` 是特殊记号 |
| Zig | ✓（还会减少） | `usingnamespace` 已移除；`async`, `await` 不在关键字表中 |
| Lua | ✗（直接加词） | 5.5 把 `global` 变成保留字 |
| TypeScript | ✗ | 新关键字走上下文（`override`, `satisfies`, `using`, `accessor`） |
| JavaScript | ✓ | `enum` 永久保留；旧标准遗留 `abstract`, `boolean`, `byte`/… 一批 |
| PHP | ✗（按版本加词） | `fn`（7.4）、`match`（8.0）、`enum`, `readonly`（8.1） |
| Ruby | ✗ | `_1`…`_9` 是编号参数；`it` 是 3.4+ 的隐式块参数 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 类别 | 词表 |
| --- | --- |
| 保留关键字（未使用） | `abstract`, `become`, `box`, `do`, `final`, `macro`, `override`, `priv`, `try`, `typeof`, `unsized`, `virtual`, `yield` |
| 2024 edition 新增保留（1 个） | `gen`（配合生成器语法） |

```rust
// let abstract = 1;      // 🛑 保留关键字不能当标识符
// let try = 2;           // 🛑 同理（try 在 2018 起被保留）
let r#try = 2;             // ✅ r# 可以绕开大部分关键字（crate/self/super/Self 除外）
```

Rust 的保留表是"给未来留的坑"：`try` 曾经只是普通标识符（老代码里常见 `fn try()`），2018 edition 起变成保留字；`gen` 在 2024 edition 被保留。`r#` 原始标识符能绕开绝大多数关键字，但 `crate`, `self`, `super`, `Self` 不行。

{{% /tab %}}

{{% tab header="Swift" %}}

Swift **没有"留给未来"的保留字清单**，新增能力基本通过上下文关键字或宏实现（例如 `#file`, `#line`, `#function` 在 5.9 之后改成标准库宏，不再是保留记号）。

```swift
// Swift 5.9 之前 #file 是保留记号，现在它只是一个宏：
let file = #file          // 仍然能用，但实现方式变了
let path = #filePath       // 也是宏
```

所以写 Swift 时不需要背"未来保留字"，要记的是那 29 个上下文关键字——它们在特定位置才生效，所以新增它们几乎不会破坏老代码。

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有未来保留字**。语言设计上刻意不做"提前占词"，新能力通过**预声明标识符**加入（例如 1.21 加入 `min`, `max`, `clear`）——代价是老代码里如果定义了同名函数，升级后可能被遮蔽或冲突。

```go
func min(a, b int) int { return a }   // 仍然合法：遮蔽了内建 min
var x = min(1, 2)
```

Go 承诺兼容性，所以这种"名字占用"只会发生在预声明标识符层面，而不是关键字层面。

{{% /tab %}}

{{% tab header="Python" %}}

Python **没有未来保留字表**，靠"软关键字"避免占词：`match`, `case`, `type`, `_` 只在特定语句里才是关键字，所以新语法不会让老变量名失效。

```python
match = 1        # 老代码照常运行
type = 2
case = 3
_ = 4
print(match, type, case, _)
```

唯一的例外是历史遗留：Python 2 的 `print`, `exec` 是语句关键字，Python 3 改成了普通函数；`async`, `await` 在 3.5 引入、3.7 变成正式关键字（如果非要当变量名，用 `asyncio` 之类的替代命名）。

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 有一个明确的"保留但未使用"关键字：`typeof`。它在硬关键字清单里，但目前没有实际语义（官方说明是"保留给未来使用"）。

```kotlin
// val typeof = 1     // 🛑 编译错误：typeof 是硬关键字
val `typeof` = 1      // ✅ 反引号可以绕开
```

除此之外，Kotlin 没有成体系的未来保留字：新能力通过软关键字（`context`, `value`, `field`）加入，正是为了不破坏已有标识符。

{{% /tab %}}

{{% tab header="Java" %}}

| 类别 | 词表 | 说明 |
| --- | --- | --- |
| 保留但从未使用（2 个） | `const`, `goto` | 保留是为了让编译器对 C/C++ 关键字给出更好的报错 |
| 保留但语义特殊（1 个） | `_` | Java 22 起只能用于"未命名变量/模式" |
| 过时但仍保留（1 个） | `strictfp` | Java 17 起所有浮点运算都是 strict，关键字已无意义 |

```java
// int const = 1;        // 🛑 保留关键字
// int goto = 2;         // 🛑 保留关键字
int _ = 3;                // ⚠️ Java 21 及以前可以（有警告），Java 22+ 不行
```

Java 的策略是"保留字只增不减"：新特性一律走上下文关键字（`var`, `record`, `sealed`, `permits`, `when`），所以老代码几乎不会因为升级 Java 而炸掉。

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的关键字**只增不减**，没有"留给未来"的清单；但有几类需要知道：标准里包含的 TS（技术规范）关键字（`atomic_cancel`, `atomic_commit`, `atomic_noexcept`, `synchronized`, `reflexpr`）、C++26 新增的 `contract_assert`，以及历史上"基本没人实现"的 `export`（C++20 起改用于模块）。

```cpp
export module demo;        // C++20：export/module 成了真语法
// atomic_cancel { }       // TM TS：主流编译器不支持
```

写可移植代码时只应使用当前标准（C++23）里真正实现的关键字；TM TS 与反射 TS 的字不要用。

{{% /tab %}}

{{% tab header="C" %}}

| 类别 | 词表 | 说明 |
| --- | --- | --- |
| 保留但极少实现（4 个） | `_Decimal32`, `_Decimal64`, `_Decimal128`, `_Imaginary` | 十进制浮点与复数扩展，多数编译器不支持 |
| C23 起弃用（1 个） | `_Noreturn` | 推荐改用 `[[noreturn]]` |
| 实现保留标识符（2 个） | `_` + 大写字母开头、`__` 开头 | 保留给实现与标准库 |

```c
// _Decimal64 x = 0.1;      /* 大多数编译器不支持 */
[[noreturn]] void die(void);
// int _Foo;                /* 实现保留：自己别用 */
```

C 没有"未来保留字"，但要小心**实现保留标识符**：`_Foo`, `__bar`, `_Exit` 这类名字属于实现（编译器和标准库），自己定义会有冲突风险。

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的"废弃关键字"主要是 `type`：它在 0.7 之前用于定义类型，1.0 起被 `struct`, `mutable struct` 取代，现在 `type` 只是普通标识符（老代码升级时会报错，需要手动改名）。

```julia
# 0.6 的写法（现在会报错）
# type Point; x::Int; end

struct Point            # ✅ 现在的写法
    x::Int
end

type = 1                # ✅ type 现在是普通名字
```

除此之外 Julia 没有未来保留字；`abstract`, `mutable`, `primitive`, `outer`, `public`, `where` 都是上下文关键字，新增它们不会破坏既有名字。

{{% /tab %}}

{{% tab header="C#" %}}

C# **没有"留给未来"的保留关键字**：官方策略是保留字保持稳定，新能力一律用**上下文关键字**（C# 3 的 `var`、5 的 `async`, `await`、9 的 `record`, `init`、11 的 `required`, `file`, `scoped`、14 的 `field`）。

```csharp
int var = 1;          // var：上下文关键字，老代码里的变量名不受影响
int record = 2;
int field = 3;        // C# 14 的 field 同样是上下文关键字
```

因此升级到新版本 C# 时几乎不会遇到"名字突然变非法"，代价是关键字表越来越长、语义依赖上下文。

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 没有单独的"未来保留字"清单，它用四档划分（reserved / built-in identifier / context / unrestricted）来避免占词；例如 `sealed`, `base`, `interface`, `when`, `sync` 属于 unrestricted 档，做标识符完全合法。

```dart
var sealed = 1;       // ✅ unrestricted
var when = 2;
var late = 3;          // ✅ built-in identifier：不能当类型名，可当变量名
```

唯一"只增不减"的是 33 个 reserved 词，但它们都是核心语法词，很少与新特性相关。

{{% /tab %}}

{{% tab header="R" %}}

R 的保留字表**极小而且稳定**（20 个），没有未来保留字：R 核心团队几十年只加了 `NA_real_` 这类缺失值常量，从未预留过"将来可能用"的词。

```r
# R 里没有“保留给未来”的词
# 但 ... / ..1 / ..2 这类特殊记号保留给参数转发
f <- function(...) list(...)
f(1, 2)
```

需要注意的是 `...`, `..1`, `..2` 这些**特殊记号**：它们是保留的，不能当普通变量名，但可以在函数参数里做"参数转发"。

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的关键字表随版本**有增有减**，这在系统语言里比较少见：

| 词 | 现状 |
| --- | --- |
| `usingnamespace` | 0.14 起弃用，0.15 已不在关键字表中 |
| `async`, `await` | 已不在关键字表中（异步机制被移出语言、等待重新设计） |
| `suspend`, `resume`, `nosuspend`, `anyframe` | 仍在关键字表中（异步相关语法保留） |

```zig
const usingnamespace = 1;    // ✅ 0.15 里它只是普通标识符
const async = 2;              // ✅ 同上
```

写跨版本代码时，遇到这些词最好查一下目标 Zig 版本的语言参考——它们的含义真的会变。

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有未来保留字，但**新版本会直接新增关键字**：Lua 5.5 把 `global` 变成保留字（用于显式声明全局变量）。

| 版本 | 变化 |
| --- | --- |
| 5.2（1 个） | 新增 `goto` |
| 5.3 | 整数/浮点子类型、位运算符 |
| 5.4（2 个） | `<close>` 变量、`<const>` 属性（都不是关键字） |
| 5.5（2 个） | `global` 成为保留字；`for` 控制变量变成只读 |

```lua
-- Lua 5.5 之前这样写是合法的：
-- local global = 1
global counter = 0        -- 5.5：显式声明全局
```

编译 Lua 时可以用兼容开关（`LUA_COMPAT_GLOBAL`）把 `global` 还原成普通词，但官方建议尽早改代码。

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有"未来保留字"，但**关键字会随版本增加**，而且大多走上下文关键字（不破坏老代码）：

| 版本 | 新增 | 类型 |
| --- | --- | --- |
| 4.3（1 个） | `override` | 上下文关键字 |
| 4.9（2 个） | `satisfies`, `accessor` | 上下文关键字 |
| 5.2（1 个） | `using` | 上下文关键字（`using` 声明） |
| 7.0 | 模板字面量类型改为按码点处理（语言行为变化，不是关键字） | — |

```ts
const override = 1;      // ✅ 上下文关键字，可以当标识符
const satisfies = 2;
const using = 3;
```

真正不能用的只有从 JavaScript 继承的那批保留字（`class`, `enum`, `delete`…）。

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 是少数**真的有未来保留字**的语言：`enum` 被永久保留（ECMAScript 规范里没有给 `enum` 任何语义，但就是不让用），旧标准（ES1–ES3）还留了一批：

```js
// 永久保留：enum
// const enum = 1;      // 🛑 语法错误

// 旧标准的未来保留字（严格模式下才报错的那几个除外）
// abstract boolean byte char double final float goto int long
// native short synchronized throws transient volatile
```

这些词在现代运行时**大多已经不是保留字**（例如 `abstract`, `int` 现在可以当变量名），但 `enum` 依然被规范永久保留。写跨环境代码时，最好把这批词都当成禁区。

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有未来保留字：新关键字都是"随版本直接加入"的。

| 版本 | 新增关键字 |
| --- | --- |
| 7.4（1 个） | `fn` |
| 8.0（1 个） | `match` |
| 8.1（3 个） | `enum`, `readonly`, `never` |
| 8.5 | 无新增关键字（`|>` 是运算符，`clone(...)` 是语法） |

```php
// 升级 PHP 时最容易撞的：老代码里把 match / enum / readonly 当函数名
// function match($x) {}      // 🛑 PHP 8 起非法
// function enum() {}         // 🛑 PHP 8.1 起非法
```

升级到 PHP 8.x 时，检查一下函数名、类名里有没有 `match`, `enum`, `readonly`, `fn`——这是实际项目里最常见的兼容性问题。

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有未来保留字（41 个关键字几十年基本没变），但有几个**保留的编号参数**需要注意：`_1`…`_9` 是块里的编号参数，`it` 是 Ruby 3.4 起的隐式块参数（不是关键字，是语法糖）。

```ruby
[1, 2, 3].map { _1 * 2 }        # 编号参数（保留）
[1, 2, 3].map { it * 2 }         # Ruby 3.4+ 的 it（局部变量名 it 会被遮蔽）

it = 10                          # ✅ 仍然可以定义，但在块里可能被遮蔽
```

因为 `it` 是"隐式"的，Ruby 3.4+ 在块里引用 `it` 时可能拿到块参数而不是外层变量——升级时如果代码里大量用 `it` 当变量名，值得检查一遍。

{{% /tab %}}

{{< /tabpane >}}

### 特殊值与单例标识符

`true`, `false`, `null`, `nil`, `None`, `undefined`, `this`, `self`, `super` 这些词在词法上"像关键字"，但有的语言把它们当关键字（Python、Ruby、Lua），有的当字面量（Java、C#），有的干脆只是普通全局变量（JavaScript 的 `undefined`）。这一节逐语言说明。

**一页速览**

| 语言 | 真/假 | 空值 | 其他特殊值 |
| --- | --- | --- | --- |
| Rust | `true`, `false`（关键字） | `None`（`Option` 变体） | `()`, `_` |
| Swift | `true`, `false`（关键字） | `nil`（关键字） | `self`, `Self`, `super`, `_` |
| Go | `true`, `false`（预声明，可遮蔽） | `nil`（预声明） | `iota`, `_` |
| Python | `True`, `False`（关键字） | `None`（关键字） | `...`, `Ellipsis`, `NotImplemented`, `__debug__` |
| Kotlin | `true`, `false`（硬关键字） | `null`（硬关键字） | `this`, `super`, `it` |
| Java | `true`, `false`（字面量） | `null`（字面量） | `this`, `super`, `_` |
| C++ | `true`, `false`（关键字） | `nullptr`（关键字）/ `NULL`（宏） | `this`, `and`, `or`, `not` |
| C | `true`, `false`（C23 关键字） | `nullptr`（C23）/ `NULL`（宏） | 没有 `this`，用 `self` 参数 |
| Julia | `true`, `false`（关键字） | `nothing`（没有值）/ `missing`（缺失） | `Inf`, `NaN`, `_` |
| C# | `true`, `false`（字面量） | `null`（字面量） | `this`, `base`, `value` |
| Dart | `true`, `false`（reserved） | `null`（reserved） | `this`, `super` |
| R | `TRUE`, `FALSE`（保留字） | `NULL`, `NA`, `NaN`（保留字） | `Inf`；`T`, `F` 不是保留字 |
| Zig | `true`, `false`（字面量） | `null`, `undefined`（字面量） | `_` |
| Lua | `true`, `false`（保留字） | `nil`（保留字） | `0`, `""` 是真值 |
| TypeScript | `true`, `false`（关键字） | `null`, `undefined`（关键字） | `NaN`, `Infinity`, `void` |
| JavaScript | `true`, `false`（保留字） | `null`（保留字）/ `undefined`（全局属性，可遮蔽） | `NaN`, `Infinity`, `globalThis` |
| PHP | `true`, `false`（大小写不敏感） | `null`（大小写不敏感） | `$this`, `self`, `parent`, `static` |
| Ruby | `true`, `false`（关键字） | `nil`（关键字，NilClass 单例） | `self`, `__FILE__`, `__LINE__`, `__ENCODING__` |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false` | 关键字 | 类型是 `bool` |
| `None`, `Some(x)` | 枚举变体 | `Option<T>` 的两个变体，不是关键字 |
| `()` | unit 值 | 空元组，函数没有返回值时返回它 |
| `_` | 关键字 | 只用于模式匹配/丢弃（`let _ = f();`） |

```rust
let a: bool = true;               // 关键字
let b: Option<i32> = None;         // 枚举变体
fn f() -> () { }                    // unit
let _ = f();                        // 丢弃返回值
```

{{% /tab %}}

{{% tab header="Swift" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false` | 关键字 | `Bool` 的两个值 |
| `nil` | 关键字 | `Optional.none` 的写法 |
| `self`, `Self`, `super` | 关键字 | 实例自身 / 类型自身 / 父类 |
| `_` | 关键字 | 模式占位（`for _ in 0..<3`） |

```swift
let ok: Bool = true
let nothing: Int? = nil
class A { required init() {} }
class B: A { required init() { super.init() } }
for _ in 0..<2 { }
```

{{% /tab %}}

{{% tab header="Go" %}}

Go 的这些词**都不是关键字**，而是"预声明标识符"——可以被同名变量遮蔽：

| 词 | 说明 |
| --- | --- |
| `true`, `false` | 预声明常量 |
| `nil` | 预声明标识符（指针/切片/map/接口/函数/chan 的零值） |
| `iota` | 常量计数器 |
| `_` | 空白标识符：`_ = f()` 丢弃值 |

```go
true := false        // ✅ 合法但极其危险
nil := 1             // ✅ 合法
iota := 2            // ✅ 合法
_ = true             // 丢弃
```

{{% /tab %}}

{{% tab header="Python" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `True`, `False`, `None` | 关键字 | PEP 8 从 3.8 起要求大写 |
| `...`, `Ellipsis` | 单例 | 省略号对象，`numpy` 切片里常见 |
| `NotImplemented` | 单例 | 二元运算"未实现"的返回标记 |
| `__debug__` | 常量 | 解释器优化模式下为 False |

```python
ok = True
nothing = None
arr[...] = 0            # 省略号
type(NotImplemented)    # NotImplementedType
```

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `null` | 硬关键字 | `null` 只能赋给可空类型 |
| `this`, `super` | 硬关键字 | 当前接收者 / 父类实现 |
| `it` | 隐式参数 | 单参数 lambda 的默认名，可以被覆盖 |

```kotlin
val ok: Boolean = true
val nothing: String? = null
listOf(1, 2).map { it * 2 }        // it 是隐式参数
listOf(1, 2).map { it -> it * 3 }  // 显式命名
```

{{% /tab %}}

{{% tab header="Java" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `null` | 字面量（不是关键字） | JLS 把三者归为 Literals |
| `this`, `super` | 关键字 | 当前对象 / 父类 |
| `_` | 关键字 | Java 22 起只能用于未命名变量/模式 |

```java
boolean ok = true;
Object nothing = null;
int _ = 1;               // Java 22 起这是未命名变量，不能再用 _ 当名字
```

{{% /tab %}}

{{% tab header="C++" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false` | 关键字 | 类型是 `bool` |
| `nullptr` | 关键字（C++11） | 空指针字面量；`NULL` 是宏 |
| `this` | 关键字 | 指向当前对象 |
| `and`, `or`, `not` | 关键字 | 逻辑运算符的替代拼写 |

```cpp
bool ok = true;
int* p = nullptr;          // 推荐
int* q = NULL;             // 旧宏，来自 <cstddef>
if (ok and not p) { }
```

{{% /tab %}}

{{% tab header="C" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false` | C23 关键字（此前是宏） | 需要 `<stdbool.h>` 的旧代码仍能编译 |
| `nullptr` | C23 关键字 | 类型是 `nullptr_t`；`NULL` 仍是宏 |
| `_Generic` | 关键字 | 编译期类型分派，不是特殊值 |

```c
#include <stddef.h>
bool ok = true;             /* C23 */
void *p = nullptr;          /* C23 */
void *q = NULL;             /* 老写法，仍然可用 */
```

C 里没有 `this`；指向自身的指针要靠参数显式传递（`self`）。

{{% /tab %}}

{{% tab header="Julia" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false` | 关键字 | `Bool` 的两个值 |
| `nothing`, `Nothing()` | 单例类型 | "没有值" |
| `missing`, `Missing()` | 单例类型 | "缺失数据"（三值逻辑） |
| `Inf`, `NaN` | 常量（不是关键字） | 来自 `Base`，可以被遮蔽 |

```julia
ok = true
x = nothing          # 没有值
y = missing          # 缺失
Inf, -Inf, NaN
nothing === nothing  # true（单例）
```

{{% /tab %}}

{{% tab header="C#" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `null` | 字面量（不是关键字） | 官方文档把它们列在"字面量"下 |
| `this`, `base` | 关键字 | 当前实例 / 基类 |
| `value` | 上下文关键字 | 属性 `set` 访问器里的隐式参数 |

```csharp
bool ok = true;
object? nothing = null;
public int X { get; set { value += 1; } }   // value 是上下文关键字
```

{{% /tab %}}

{{% tab header="Dart" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `null` | reserved 关键字 | `null` 只在可空类型里合法 |
| `this`, `super` | reserved 关键字 | 当前对象 / 父类 |

```dart
var ok = true;
String? nothing = null;
class A { A(); }
class B extends A { B() : super(); }
```

Dart 里没有 `undefined`：未初始化的非空变量根本不允许存在（健全空安全）。

{{% /tab %}}

{{% tab header="R" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `TRUE`, `FALSE` | 保留字常量 | 逻辑值 |
| `NULL` | 保留字常量 | 空对象（length 为 0） |
| `NA`, `NA_integer_`, `NA_real_`, `NA_complex_`, `NA_character_` | 保留字常量 | 缺失值 |
| `Inf`, `-Inf`, `NaN` | 保留字常量 | 无穷与非数 |
| `T`, `F` | **不是保留字** | 只是普通的 `TRUE`, `FALSE` 绑定，可被覆盖 |

```r
x <- TRUE
y <- NA_real_
z <- NaN
T <- FALSE          # ⚠️ 合法！之后 T 就不再是 TRUE
is.null(NULL)       # TRUE
```

{{% /tab %}}

{{% tab header="Zig" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false` | 字面量 | `bool` 的两个值 |
| `null` | 字面量 | 只用于可选类型 `?T` |
| `undefined` | 字面量 | 未初始化；读它是 UB，不是 null |
| `_` | 丢弃 | `_ = f();`, `for (xs) |_| {}` |

```zig
const ok: bool = true;
const maybe: ?u8 = null;
var buf: [4]u8 = undefined;      // 未初始化，必须在读之前写
_ = buf;
```

{{% /tab %}}

{{% tab header="Lua" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `nil` | 保留字 | `nil` 是"没有值"；只有 `false` 与 `nil` 为假 |

```lua
print(true, false, nil)
if not nil then print("nil 为假") end
if 0 then print("0 是真值") end      -- ✅ 会打印
```

注意 `0` 和 `""` 在 Lua 里都是**真值**，这和其他动态语言不一样。

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `null`, `undefined` | 关键字 | `undefined` 在 TS 里是类型与值 |
| `NaN`, `Infinity` | `Number` 的常量 | 不是关键字，只是全局属性 |
| `void` | 关键字 | 类型层面的 `undefined`；运行时 `void 0` 是 `undefined` 的稳妥写法 |

```ts
const ok: boolean = true;
const nothing: null = null;
const missing: undefined = undefined;
Number.isNaN(NaN);           // ✅ 判 NaN 的正确方式
const u = void 0;             // 稳定拿到 undefined
```

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `null` | 保留字 | 三个字面量 |
| `undefined` | **普通全局属性** | 可以当变量名/参数名遮蔽（严格模式下赋值会报错） |
| `NaN`, `Infinity` | 全局属性 | 不是关键字，可被遮蔽（不推荐） |
| `globalThis` | 全局属性 | 标准化的全局对象入口 |

```js
true; false; null;
undefined;                    // 全局属性
function f(undefined) { }     // ✅ 合法：参数遮蔽了全局 undefined
Number.isNaN(NaN);            // 判 NaN 用这个
globalThis === globalThis;    // 跨环境拿全局对象
```

{{% /tab %}}

{{% tab header="PHP" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `null` | 保留的常量名（大小写不敏感） | 不是关键字，但不能当类名/常量名 |
| `$this` | 变量 | 指向当前对象（不能重新赋值） |
| `self`, `parent`, `static` | 关键字 | 类内引用：自身 / 父类 / 运行时类 |

```php
$ok = TRUE;                     // 大小写不敏感
$nothing = null;
class A {
    public function me(): string { return static::class; }   // 后期静态绑定
    public function parentName(): string { return parent::class; }
}
```

{{% /tab %}}

{{% tab header="Ruby" %}}

| 词 | 身份 | 说明 |
| --- | --- | --- |
| `true`, `false`, `nil` | 关键字 | 分别对应 TrueClass/FalseClass/NilClass 的单例 |
| `self` | 关键字 | 当前对象 |
| `__FILE__`, `__LINE__`, `__ENCODING__` | 特殊记号 | 当前文件 / 行号 / 编码 |

```ruby
true.class          # TrueClass
nil.class           # NilClass
nil.to_a            # []
self                # 当前对象
__FILE__; __LINE__; __ENCODING__
```

Ruby 里 `nil` 是真正的对象（不是"什么都没有"），所以 `nil.to_s` 返回 `""`, `nil.nil?` 返回 `true`。

{{% /tab %}}

{{< /tabpane >}}

### 标识符规则与关键字规避

关键字只有在"当名字"的时候才会挡路。下面按语言给出标识符的字符规则、官方命名约定，以及"确实想用这个名字"时的标准做法。

**一页速览**

| 语言 | 标识符字符集 | 关键字规避写法 |
| --- | --- | --- |
| Rust | ASCII + Unicode（XID） | `r#type` |
| Swift | Unicode（含 emoji） | 反引号 `` `class` `` |
| Go | Unicode 字母；首字母大写表示导出 | 只能改名（`typeName`） |
| Python | Unicode 字母/数字/下划线 | 加下划线 `class_` |
| Kotlin | Unicode 字母/数字/下划线 | 反引号 `` `is` `` |
| Java | Unicode 字母/数字/`$`, `_` | 只能改名（`class_`） |
| C++ | ASCII（Unicode 支持有限） | 只能改名（`class_`） |
| C | ASCII（C23 允许 Unicode，可移植性差） | 只能改名 |
| Julia | Unicode（支持希腊字母） | `var"if"` |
| C# | Unicode 字母/数字/`_` | `@class` 前缀 |
| Dart | 字母/数字/`_`, `$` | 只能改名；`_name` 表示库级私有 |
| R | 字母/数字/`.`, `_` | 反引号 `` `if` `` |
| Zig | ASCII 字母/数字/下划线 | `@"if"` |
| Lua | 字母/数字/下划线 | 字段名随便用（`t.end`） |
| TypeScript | Unicode 字母/数字/`_`, `$` | 属性名不受限；变量改名 |
| JavaScript | Unicode 字母/数字/`_`, `$` | 属性名不受限；变量改名 |
| PHP | 变量 `$` 开头；类名/函数名可用 Unicode | 方法名/属性名不受限 |
| Ruby | 字母/数字/下划线；方法名可带 `?`, `!`, `=` | 关键字可作方法名；变量要改名 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | ASCII 字母/数字/下划线，且支持 Unicode 标识符（XID） |
| 大小写 | 敏感 |
| 命名约定 | 变量/函数 `snake_case`、类型/枚举 `UpperCamelCase`、常量 `SCREAMING_SNAKE_CASE`、生命周期 `'a` |
| 关键字规避 | `r#type`（`crate`, `self`, `super`, `Self` 除外） |

```rust
let user_id = 1;                  // snake_case
struct UserProfile;                // UpperCamelCase
const MAX_LEN: usize = 10;         // SCREAMING_SNAKE_CASE
let r#type = "json";               // 关键字当字段名/变量名
struct S { r#match: i32 }          // 生成代码里很常见
```

{{% /tab %}}

{{% tab header="Swift" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode；可用表情符号（合法但不建议） |
| 大小写 | 敏感 |
| 命名约定 | 类型 `UpperCamelCase`、方法与属性 `lowerCamelCase`、常量同方法名 |
| 关键字规避 | 反引号 `` `default` `` |

```swift
let userName = "x"                 // lowerCamelCase
struct UserProfile { }             // UpperCamelCase
let `class` = 1                    // 反引号绕开关键字
enum E { case `default` }           // 枚举 case 也能这么写
```

{{% /tab %}}

{{% tab header="Go" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 字母 + 数字 + `_` |
| 大小写 | 敏感；**首字母大写 = 导出**（包外可见） |
| 命名约定 | `camelCase`（不是 snake_case）、缩写保持全大写（`userID`）、文件名 `snake_case` |
| 关键字规避 | 无转义语法，只能改名或加后缀（`type_`, `typeName`） |

```go
type User struct {           // 导出类型
    ID   int                  // 导出字段
    name string               // 未导出字段
}
var typeName = "x"            // 关键字不能直接用，只能改名
```

Go 用**大小写**表达可见性，所以命名不只是风格问题：`Name` 和 `name` 是"导出"与"不导出"的区别。

{{% /tab %}}

{{% tab header="Python" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 字母/数字/下划线，不能以数字开头 |
| 大小写 | 敏感 |
| 命名约定（PEP 8） | 变量/函数 `snake_case`、类 `CapWords`、常量 `SCREAMING_SNAKE_CASE`、内部用 `_x`、避免 `__x__` |
| 关键字规避 | 加下划线（`class_`, `type_`）是社区标准做法 |

```python
user_id = 1                 # snake_case
class UserProfile: ...      # CapWords
MAX_LEN = 10                # 常量
class_ = "demo"             # 关键字后加下划线（PEP 8 推荐）
```

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 字母/数字/下划线；`$` 只能在字符串模板里 |
| 大小写 | 敏感 |
| 命名约定 | 类型 `UpperCamelCase`、函数/属性 `lowerCamelCase`、常量 `SCREAMING_SNAKE_CASE` |
| 关键字规避 | 反引号 `` `is` ``（还能用空格等特殊字符） |

```kotlin
val userName = "x"
class UserProfile
const val MAX_LEN = 10
val `is` = true                  // 反引号
fun `test with spaces`() { }      // 反引号甚至允许空格（多用于测试名）
```

{{% /tab %}}

{{% tab header="Java" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 字母/数字/`$`, `_`，不能以数字开头 |
| 大小写 | 敏感 |
| 命名约定 | 类 `UpperCamelCase`、方法/变量 `lowerCamelCase`、常量 `SCREAMING_SNAKE_CASE`、包名全小写 |
| 关键字规避 | 无转义；改名或加下划线 |

```java
package com.example.demo;         // 包名全小写
public class UserProfile {         // 类 UpperCamelCase
    private static final int MAX_LEN = 10;   // 常量
    private String userName;                  // 变量
    int class_ = 1;                            // 改名规避关键字
}
```

`$` 在标识符里合法但约定只给编译器/生成代码使用（如内部类 `Outer$Inner`）。

{{% /tab %}}

{{% tab header="C++" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | ASCII 字母/数字/下划线（Unicode 支持有限，慎用） |
| 大小写 | 敏感 |
| 命名约定 | 标准库风格 `snake_case`；Google 风格：类型 `CamelCase`、函数 `CamelCase`、变量 `snake_case`、成员 `member_` |
| 保留标识符 | `__x`, `_X`（下划线+大写）保留给实现；全局作用域 `_x` 也保留 |
| 关键字规避 | 改名或加下划线（`class_`） |

```cpp
class UserProfile {            // 类型 CamelCase（Google 风格）
public:
    int user_id() const;        // 函数 snake_case 或 CamelCase，取决于项目
private:
    int user_id_;               // 成员加下划线后缀
};
```

{{% /tab %}}

{{% tab header="C" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | ASCII 字母/数字/下划线（C23 允许 Unicode 标识符，但可移植性差） |
| 大小写 | 敏感 |
| 命名约定 | `snake_case`；宏 `SCREAMING_SNAKE_CASE`；`_t` 后缀（POSIX 保留，自己项目慎用） |
| 保留标识符 | `__x`, `_X` 保留给实现 |
| 关键字规避 | 改名 |

```c
struct user_profile { int user_id; };   /* snake_case */
#define MAX_LEN 10                       /* 宏大写 */
typedef struct user_profile user_profile_t;   /* _t 后缀：POSIX 保留，慎用 */
```

{{% /tab %}}

{{% tab header="Julia" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 标识符（含希腊字母、上下标） |
| 大小写 | 敏感 |
| 命名约定 | 函数/变量 `snake_case`、类型 `UpperCamelCase`、常量 `SCREAMING_SNAKE_CASE`；`!` 结尾表示"会修改参数"、`?` 结尾表示返回布尔 |
| 关键字规避 | 改名（或用 `var"if"` 语法） |

```julia
sort!(v)            # 原地排序（! 约定）
isempty(v)           # 返回布尔（? 约定）
struct UserProfile   # 类型大写
    user_id::Int
end
var"if" = 1          # Julia 也支持 var"..." 写法
```

{{% /tab %}}

{{% tab header="C#" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 字母/数字/`_`；`@` 可以作为前缀 |
| 大小写 | 敏感 |
| 命名约定 | 类型/属性/方法 `PascalCase`、参数/局部变量 `camelCase`、私有字段 `_camelCase`、常量 `PascalCase` |
| 关键字规避 | `@class` 前缀（也可以把 `@` 用在普通名字上） |

```csharp
public class UserProfile {         // PascalCase
    private readonly int _maxLen;   // 私有字段
    public int UserId { get; }       // 属性
    public string @class = "x";      // @ 前缀绕开关键字
}
```

{{% /tab %}}

{{% tab header="Dart" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | 字母/数字/`_`, `$`，不能以数字开头 |
| 大小写 | 敏感 |
| 命名约定 | 类型 `UpperCamelCase`、变量/方法 `lowerCamelCase`、库与文件名 `lower_snake_case`、常量 `lowerCamelCase` |
| 私有 | `_name` 表示"库级私有"（Dart 的可见性单位是库/文件） |
| 关键字规避 | 改名 |

```dart
class UserProfile {          // UpperCamelCase
  final int userId;           // lowerCamelCase
  final String _secret;       // 库级私有
  const UserProfile(this.userId, this._secret);
}
```

{{% /tab %}}

{{% tab header="R" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | 字母/数字/`.`, `_`，不能以数字或 `_` 开头（`.` 开头可以，但会被 `ls()` 隐藏） |
| 大小写 | 敏感 |
| 命名约定 | 社区很混杂：`snake_case`（tidyverse 风格）、`camelCase`, `dot.case` 都有；函数常 `snake_case` |
| 关键字规避 | 反引号 `` `if` ``；或遵守 `make.names()` 规则 |

```r
user_id <- 1                    # snake_case（tidyverse）
.hidden <- 2                    # 点开头：ls() 默认不显示
`if` <- 3                       # 反引号绕开保留字
list(`class` = "a")              # 名字里也能用
```

{{% /tab %}}

{{% tab header="Zig" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | ASCII 字母/数字/下划线；关键字可用 `@"..."` 形式 |
| 大小写 | 敏感 |
| 命名约定 | 类型 `UpperCamelCase`、变量/函数 `snake_case`、常量同 snake_case |
| 关键字规避 | `@"if"`, `@"align"` |

```zig
const UserProfile = struct {      // 类型 UpperCamelCase
    user_id: u32,                  // 字段 snake_case
    @"type": u8 = 0,                // 关键字当字段名
};

fn maxLen() u32 { return 10; }      // 函数 snake_case（zls 也接受 camelCase）
```

{{% /tab %}}

{{% tab header="Lua" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | 字母/数字/下划线，不能以数字开头；大小写敏感 |
| 命名约定 | 常用 `snake_case`；`_G`, `_VERSION` 这类下划线大写是保留约定 |
| 关键字规避 | 变量名只能改；**字段名随便用**（`t.end`） |

```lua
local user_id = 1               -- snake_case
local _VERSION2 = "x"            -- 避免以 _ + 大写开头（Lua 内部保留）
local t = {}
t.end = 1                         -- ✅ 字段名可以用保留字
t["function"] = 2
```

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 字母/数字/`_`, `$` |
| 大小写 | 敏感 |
| 命名约定 | 类型/接口 `PascalCase`、变量/函数 `camelCase`、常量 `SCREAMING_SNAKE_CASE` 或 camelCase、私有 `#field` |
| 关键字规避 | 属性名不受限；变量名加下划线 |

```ts
interface UserProfile { userId: number }   // PascalCase
const userName = "x";                       // camelCase
const MAX_LEN = 10;                          // 常量
const obj = { class: 1, if: 2 };              // 属性名可用保留字
const type_ = "x";                            // 变量名规避
```

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | Unicode 字母/数字/`_`, `$` |
| 大小写 | 敏感 |
| 命名约定 | 类 `PascalCase`、变量/函数 `camelCase`、常量 `SCREAMING_SNAKE_CASE`、私有 `#field` |
| 关键字规避 | 属性名不受限；变量名加下划线或换名字 |

```js
class UserProfile {          // PascalCase
  #secret = 1;                // 私有字段
  constructor(userId) { this.userId = userId; }
}
const obj = { class: 1, delete: 2 };   // 属性名可用保留字
let class_ = 1;                        // 变量名规避
```

{{% /tab %}}

{{% tab header="PHP" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | 变量以 `$` 开头，后接字母/数字/下划线；类名/函数名可含 Unicode |
| 大小写 | 变量名敏感；函数名、类名、关键字**不敏感** |
| 命名约定（PSR-12） | 类 `PascalCase`、方法 `camelCase`、常量 `SCREAMING_SNAKE_CASE`、变量 `snake_case` 或 `camelCase` |
| 关键字规避 | 方法名/属性名不受限；变量名改掉即可 |

```php
namespace App;                       // 命名空间 PascalCase
final class UserProfile {             // 类 PascalCase
    public const MAX_LEN = 10;         // 常量大写
    public function getUserId(): int { return 1; }   // 方法 camelCase
}
$userId = 1;                          // 变量 $ + camelCase
echo StrToUpper("x");                  // 函数名大小写不敏感
```

{{% /tab %}}

{{% tab header="Ruby" %}}

| 规则 | 说明 |
| --- | --- |
| 字符集 | 字母/数字/下划线；方法名可含 `?`, `!`, `=`；常量以大写字母开头 |
| 前缀 | `@instance`, `@@class`, `$global` |
| 大小写 | 敏感 |
| 命名约定 | 变量/方法 `snake_case`、类/模块 `CamelCase`、常量 `SCREAMING_SNAKE_CASE`、布尔方法 `?` 结尾、危险方法 `!` 结尾 |
| 关键字规避 | 关键字可当方法名；变量名要改 |

```ruby
class UserProfile            # CamelCase
  MAX_LEN = 10                # 常量
  def user_id = @user_id       # snake_case
  def valid? = true            # 布尔方法
  def save! = nil              # 危险方法（带 !）
end

obj.class                     # 关键字可以当方法名
```

{{% /tab %}}

{{< /tabpane >}}

---

> 本页覆盖 18 种语言的关键字与保留字：**完整清单、硬关键字与软关键字、保留但未使用与未来保留字、特殊值与单例标识符、标识符规则与关键字规避**。所有清单均取自各语言的官方文档/规范或词法器源码（Python 用 `keyword` 模块、Go 用 `go/token`、Ruby 用 Ripper、TypeScript 7 用 typescript-go 的 `textToKeyword`、Lua 用 5.5 手册、Zig 用语言参考的 Keyword Reference 附录）。

> 版本基线（2026-09）：Rust 1.98、Swift 6.4、Go 1.27、Python 3.14、Kotlin 2.4、Java 26（LTS 25）、C++23、C23、Julia 1.13、C# 14 / .NET 10、Dart 3.13、R 4.6、Zig 0.15、Lua 5.5、TypeScript 7、Node 26、PHP 8.5、Ruby 4.0。
