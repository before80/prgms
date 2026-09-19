+++
title = "闭包"
date = 2026-09-19T12:00:00+08:00
weight = 11
type = "docs"
description = "18 种语言的闭包对照：捕获语义、生命周期与逃逸、与循环变量的经典陷阱、实际用途"
isCJKLanguage = true
draft = false
+++

# 闭包：18 种语言对照

闭包把函数和它引用的环境绑在一起，但"环境"在各语言里的含义完全不同。捕获语义要回答三件事：**按值捕获**（创建时拷一份快照）、**按引用捕获**（内外共享同一份存储）、**按移动捕获**（把所有权搬进闭包），以及由谁声明这件事。本页按四个主题组织：**捕获语义 → 生命周期与逃逸 → 闭包与循环变量 → 实际用途**，每个主题一套 18 语言标签页。最根本的分歧在两条轴上：一条是 Rust、C++、Swift 走"编译期规则 + 显式标注"，另一条是 Python、Ruby、JavaScript、PHP 走"运行时对象 + 隐式捕获"；Go、Java、C#、Kotlin、Dart 站在中间，用运行时对象实现、再用语言规则限定捕获的形态。C 与 Zig 干脆没有闭包，一律用"函数指针 + 显式上下文"手工模拟。

## 闭包

**一页速览**

| 语言 | 捕获写法 / 关键字 | 捕获语义 | 循环变量 |
| --- | --- | --- | --- |
| Rust | `move` 与 `Fn`/`FnMut`/`FnOnce` | 编译期按借用推断，`move` 强制按值 | `for` 变量每轮新建，逃逸必须 `move` |
| Swift | 捕获列表 `[x]`、`[weak self]`、`[unowned self]` | 捕获变量本身，捕获列表按值拷一份 | `for-in` 每轮新建，`while` 共享 |
| Go | 无关键字，直接引用外层变量 | 按变量捕获（引用语义），逃逸到堆 | 1.22 起每轮新建，之前共享 |
| Python | 无关键字，写入需 `nonlocal`/`global` | 按变量捕获（cell），重绑定要声明 | 延迟绑定，用 `lambda i=i` 或 `partial` 修 |
| Kotlin | 无关键字，直接引用 | `val`/`var` 都可捕获，`var` 改动外可见 | `for` 变量是每轮新建的 `val` |
| Java | 无关键字，lambda 直接引用 | 只捕获有效 final，可变状态要装箱 | 普通 `for` 共享，增强 `for` 每轮新建 |
| C++ | `[=]`、`[&]`、`[x]`、`[x = std::move(y)]`、`[=, this]` | 默认按值，`&` 按引用，初始化捕获可移动 | 按引用捕获循环变量必悬垂 |
| C | 没有闭包 | 函数指针 + `void *` 上下文 | 手动把当轮的值拷进结构体 |
| Julia | 无关键字，直接引用 | 按变量捕获，被改写的变量装箱到堆 | `for` 每轮新建，`while` 共享 |
| C# | 无关键字，`static` lambda 禁止捕获 | 捕获变量被提升为编译器生成类的字段 | C# 5 起 `foreach` 每轮新建，`for` 共享 |
| Dart | 无关键字，直接引用 | 按变量捕获（引用语义），由 GC 管理 | 规范规定每轮使用独立变量 |
| R | 无关键字，写外层用 `<<-` | 惰性求值 + 词法作用域 | `for` 共享，循环后变量仍存在 |
| Zig | 没有闭包 | 结构体 + 函数指针 + 上下文指针 | 没有闭包，回调靠显式上下文 |
| Lua | 无关键字，自动持有 upvalue | 按变量捕获（upvalue），`_ENV` 也是 upvalue | `for` 每轮独立，5.5 起控制变量只读 |
| TypeScript | 同 JavaScript | 同 JavaScript，另有闭包内类型收窄规则 | 同 JavaScript，类型层不阻止 `var` 陷阱 |
| JavaScript | 无关键字，直接引用 | 按变量捕获；`var` 函数级、`let` 块级 | `var` 共享（`let`/IIFE 修），`let` 每轮新建 |
| PHP | `use ($x)`、`use (&$x)`、`fn()` 自动按值 | `use` 按值，`use (&$x)` 按引用 | 箭头函数按值捕获，引用遍历要 `unset` |
| Ruby | 块、`Proc`、`lambda`/`->` | 捕获变量本身，块内赋值写回外层 | `for` 不建作用域（共享），块参数每轮新建 |

上表合计 18 行，统计口径为 18 种语言各占一行；「捕获语义」列由本页四个子主题的标签页正文归纳而来，按"有没有显式的捕获语法"分，三类合计 18 种：有显式捕获语法 4 种（Rust 的 `move`、Swift 的捕获列表、C++ 的方括号、PHP 的 `use`），无关键字、直接引用外层变量 12 种（Go、Python、Kotlin、Java、Julia、C#、Dart、R、Lua、TypeScript、JavaScript、Ruby），语言里没有闭包 2 种（C、Zig）。

### 捕获语义

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的捕获在编译期推断：编译器按"最少权限"原则，优先按共享引用借用，需要时升级为可变引用，再需要就按值移动。`Fn`、`FnMut`、`FnOnce` 三个 trait 正好对应这三种使用强度，而 `move` 关键字强制按值（拷贝或移动）捕获，用来让闭包摆脱对栈帧的借用。

```rust
fn main() {
    let s = String::from("hi");
    let show = || println!("Fn borrow: {s}");   // Fn：按共享引用捕获
    show();                                      // Fn borrow: hi
    show();                                      // 可重复调用

    let mut n = 0;
    let mut add = || { n += 1; n };              // FnMut：按可变引用捕获
    println!("FnMut: {} {}", add(), add());      // FnMut: 1 2

    let take = move || s.len();                  // move：s 被移进闭包
    println!("move: {}", take());                // move: 2
    // println!("{s}");                          // 🛑 s 已移动，编译报错

    let owned = String::from("bye");
    let consume = move || drop(owned);           // FnOnce：把捕获值移出闭包
    consume();
    // consume();                                // 🛑 FnOnce 只能调用一次
}
```

`show` 只读 `s`，所以是 `Fn`，可以反复调用；`add` 改写了 `n`，是 `FnMut`，因此绑定必须声明为 `mut`（否则连调用都编译不过）；`take` 与 `consume` 前面的 `move` 把 `s`、`owned` 的所有权搬进闭包，之后外层再用 `s` 就会报错，而 `consume` 还把捕获值移出了闭包体，所以只能调用一次。

选择哪种写法只看一个问题：闭包是否需要活过当前作用域。活不过就让它借用；活得久就用 `move`，或者用 `Box<dyn Fn>` 把类型擦掉（见"生命周期与逃逸"一节）。

📘 [Rust Reference · Closure expressions](https://doc.rust-lang.org/reference/expressions/closure-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的闭包默认按引用捕获变量本身，并且是"引用类型"：把同一个闭包赋给两个常量，它们指向同一个闭包。要控制捕获方式就得写捕获列表：`[x]` 在创建时按值拷一份，`[weak self]`、`[unowned self]` 用来打断引用环，捕获列表是 Swift 独有也是最重要的捕获工具。

```swift
var total = 0
let addTotal = { total += 1; return total }        // 捕获变量本身，共享同一份存储
print("shared:", addTotal(), addTotal(), total)    // shared: 1 2 2

var local = 10
let freeze = { [local] in local * 2 }              // 捕获列表：创建时按值拷贝
local = 99
print("list:", freeze(), "outer:", local)          // list: 20 outer: 99

final class Counter {
    var n = 0
    func makeGetter() -> () -> Int {
        { [weak self] in self?.n ?? -1 }           // [weak self] 打破循环引用
    }
}
let c = Counter()
c.n = 7
print("weak self:", c.makeGetter()())              // weak self: 7
```

`addTotal` 捕获的是 `total` 这个变量本身，所以两次调用能看到累加；`freeze` 用 `[local]` 在创建时把值 10 拷进闭包，之后外层把 `local` 改成 99 完全不影响它，这就是按值捕获的写法。

`[weak self]` 让闭包持有弱引用：对象被释放后 `self?` 求值为 `nil`，不会阻止析构；`[unowned self]` 既不增加引用计数也不置空，生命周期判断错了会直接崩溃。经验规则是：闭包存进属性、逃逸出函数用 `weak`/`unowned`，只作为参数在函数内同步调用就什么都不用写。

📘 [Swift · Closures](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的闭包按变量捕获，不按值：闭包和外层函数看到的是同一个变量，编译器通过逃逸分析决定该变量留在栈上还是分配到堆上。没有 `move`、没有捕获列表，想锁定"当时的值"只有一个办法——在闭包外复制一个局部变量。

```go
package main

import "fmt"

func main() {
	x := 1
	inc := func() int { x++; return x } // 闭包按变量捕获，共享同一份 x
	fmt.Println("ref:", inc(), inc(), x) // ref: 2 3 3

	mk := func() func() int {
		n := 0
		return func() int { n++; return n }
	}
	c := mk()
	fmt.Println("counter:", c(), c()) // counter: 1 2

	var fs []func() int
	for i := 0; i < 3; i++ { // Go 1.22 起每轮新建 i
		fs = append(fs, func() int { return i })
	}
	for _, f := range fs {
		fmt.Print(f(), " ") // 0 1 2
	}
	fmt.Println()
}
```

`x` 被 `inc` 捕获后逃逸到堆上，`inc()` 每次改写的是同一个 `x`，所以外层读到的也是 3；`mk` 里的 `n` 每个闭包各有一份，互不干扰。第三个例子说明 `for` 循环变量自 Go 1.22 起每轮新建，三个闭包分别捕获各自的 `i`，输出 `0 1 2`（1.22 之前的共享语义与 `GOEXPERIMENT=loopvar` 的历史见"闭包与循环变量"一节）。

要在旧语义下按轮取值，就在循环体第一行写 `i := i`，用一个新的局部变量承接当前值。

📘 [Go spec · For statements](https://go.dev/ref/spec#For_statements)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的闭包捕获变量所在的"格子"（cell），读写是共享的，但**重绑定**外层变量必须用 `nonlocal`（模块级用 `global`）声明，否则赋值只是在闭包内新建一个局部变量。捕获是运行时的、完全动态的，没有任何编译期所有权检查，闭包能活多久由引用计数和循环 GC 决定。

```python
def counter():
    n = 0
    def inc():
        nonlocal n          # 没有 nonlocal 就只能读、不能重绑定 n
        n += 1
        return n
    return inc

c = counter()
print("nonlocal:", c(), c())        # nonlocal: 1 2

g = 0
def bump():
    global g                        # 绑定模块级变量
    g += 1
    return g
print("global:", bump(), g)         # global: 1 1

fs = [lambda: i for i in range(3)]
print("late:", [f() for f in fs])   # late: [2, 2, 2]  延迟绑定
fs2 = [lambda i=i: i for i in range(3)]
print("default:", [f() for f in fs2])  # default: [0, 1, 2]
```

`inc` 里没有 `nonlocal` 时，`n += 1` 会因为"引用前赋值"直接抛 `UnboundLocalError`；加上 `nonlocal` 才会写回 `counter` 里的那个 `n`，`global` 是同一机制在模块层的形式。

最后两行是延迟绑定的最小复现：推导式里的 `lambda: i` 全部引用同一个 `i`，所以结果是 `[2, 2, 2]`；写成默认参数 `lambda i=i: i` 会在定义时求值，得到 `[0, 1, 2]`，`functools.partial` 是等价的另一种写法。

📘 [Python · The nonlocal statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 lambda 编译成 JVM 上的函数对象，捕获外层变量时不区分 `val` 和 `var`，而且与 Java 不同：闭包内可以直接修改被捕获的 `var`，改动在闭包外可见。编译器的做法是把被改写的变量包进一个 `Ref` 容器，所有引用它的闭包共享同一个实例。

```kotlin
fun counter(): () -> Int {
    var n = 0
    return { n += 1; n }        // 闭包捕获 var，改动对外可见
}

fun main() {
    val c = counter()
    println("var: ${c()} ${c()}")        // var: 1 2

    val k = 10
    val f: (Int) -> Int = { it + k }     // 捕获 val
    println("val: ${f(1)}")              // val: 11

    val outer = listOf(1, 2, 3)
    var sum = 0
    outer.filter { it > 0 }.forEach { sum += it }   // Java 里这样写不合法
    println("sum: $sum")                 // sum: 6
}
```

`counter()` 返回的 lambda 改写了 `n`，改动在闭包外可见，因为 `n` 被放进 `Ref` 对象，闭包持有容器而不是值的副本。这也意味着捕获有成本：只读的 `val` 通常能被直接内联，而会被改写的 `var` 一定多一层间接。

另一条实用规则是：`forEach`、`filter`、`map` 这些标准库高阶函数都是 `inline` 的，调用点不会真的生成闭包对象；自己写的高阶函数如果不加 `inline`，每次调用都会多一个对象。

📘 [Kotlin · Lambda expressions and anonymous functions](https://kotlinlang.org/docs/lambdas.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 lambda 只能捕获"有效 final"（effectively final）的局部变量，也就是初始化之后不再改动；捕获的是值的一份副本，所以从 lambda 或匿名内部类里都改不了外层局部变量。这是一条编译期规则，对应的运行时形态是编译器生成的方法加上一个委托实例。

```java
import java.util.function.IntSupplier;

public class Main {
    public static void main(String[] args) {
        int base = 10;                    // 有效 final：之后不再赋值
        IntSupplier add = () -> base + 1; // 只能捕获有效 final
        System.out.println("effectively final: " + add.getAsInt());   // 11

        int[] box = {0};                  // 需要可变状态就用单元素数组
        IntSupplier next = () -> ++box[0];
        System.out.println("box: " + next.getAsInt() + " " + next.getAsInt());  // 1 2

        // int n = 0; IntSupplier bad = () -> n++;   // 🛑 n 不是有效 final
    }
}
```

`base` 声明后再没被赋值，属于有效 final，可以捕获；只要在 lambda 之后再写一句 `base = 2`，第 5 行立刻编译报错。需要共享可变状态时用单元素数组、`AtomicInteger` 或对象字段，代码里的 `int[] box = {0}` 就是这个套路。

规则只覆盖局部变量、形参和异常参数，字段与数组元素不受限制。另外 JLS 特别说明：有效 final 的限制包括普通 `for` 的循环变量，但不包括增强 `for` 的循环变量，后者"在每次迭代中被视为不同的变量"。

📘 [JLS §15.27.2 · Lambda Body](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.27.2)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的捕获方式全部写在方括号里，编译期就定下来：`[=]` 默认按值拷贝、`[&]` 默认按引用、`[x]` 只拷一个、`[x = std::move(y)]`（初始化捕获）可以把移动的结果直接放进闭包成员。闭包类型是编译器为每个 lambda 生成的唯一类，被捕获的实体就是它的非静态数据成员。

```cpp
#include <iostream>
#include <string>
#include <utility>

struct S {
    int v = 7;
    auto f() {
        return [=, this] { return v; };   // C++20 起允许显式写 [=, this]
    }
};

int main() {
    int a = 1, b = 2;
    auto byValue = [=] { return a + b; };                  // 按值拷贝
    auto byRef = [&] { a += 10; return a; };               // 按引用
    auto one = [b] { return b * 2; };                      // 只捕获 b
    std::string s = "hello";
    auto moved = [s = std::move(s)] { return s.size(); };  // 初始化捕获 + 移动
    byRef();
    std::cout << byValue() << ' ' << a << ' ' << one() << ' ' << moved() << '\n';
    // 3 11 4 5
    std::cout << "this: " << S{}.f()() << '\n';            // this: 7
}
```

`byValue` 在创建时把 `a`、`b` 各拷一份，所以 `byRef` 把 `a` 改成 11 之后它仍然算出 3；`one` 只拷 `b`；`moved` 用初始化捕获把 `std::string` 移动进闭包，那之后外层的 `s` 已被掏空，不能再读。按值捕获的成员默认在 `const` 的 `operator()` 里，要在闭包体里修改得加 `mutable`。

成员函数里的 `[=]` 曾会隐式捕获 `*this`（按引用），cppreference 明确写着"隐式捕获 `*this` 在捕获默认值为 `=` 时自 C++20 起被弃用"，官方写法是显式写 `[=, this]`（直到 C++20 之前这样写都是错的，`[=, this]` 与 `[=]` 在成员函数里等价）；`[=, *this]` 自 C++17 起可以按值拷贝整个外围对象，适合闭包要活过对象本身的场景。

📘 [cppreference · Lambda expressions](https://en.cppreference.com/w/cpp/language/lambda)

{{% /tab %}}

{{% tab header="C" %}}

C 没有闭包：函数不是一等值，函数指针只能指向已有的函数，而且不携带环境。要模拟闭包，只能把状态放进结构体，调用时把上下文指针作为额外参数传进去；用全局变量也能凑合，代价是失去可重入性。

```c
#include <stdio.h>

/* C 没有闭包：把要“捕获”的状态放进结构体，函数通过 void* 上下文访问 */
typedef struct { int base; } Adder;

static int apply(void *ctx, int x) { return ((Adder *)ctx)->base + x; }

int main(void) {
    Adder a = {41};                     /* 状态由调用者显式持有 */
    printf("ctx: %d\n", apply(&a, 1));  /* ctx: 42 */
    return 0;
}
```

这段就是 C 里"捕获"的全部：`Adder` 是捕获的状态，`void *ctx` 是显式的 self 参数，类型还原由程序员负责，传错类型编译器不会拦。标准库的 `qsort` 更极端，它连上下文参数都没有，比较函数只能通过全局变量或元素自身取得额外信息，POSIX 的 `qsort_r` 才补上了上下文指针。

生命周期也要自己保证：上下文放在栈上、回调又活过了那个栈帧，就是悬垂指针；放在堆上就得记住谁负责 `free`。

📘 [cppreference · qsort](https://en.cppreference.com/w/c/algorithm/qsort)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的闭包是真正的匿名函数，按变量捕获外层局部变量；被捕获且可能被改写的变量会被"装箱"（box）到堆上，让内外看到同一个值。捕获发生在语法分析阶段，类型推断之后才介入，所以官方性能提示专门用一节讲捕获带来的装箱与动态派发开销。

```julia
function counter()
    n = 0
    () -> (n += 1)          # 闭包捕获 n，n 被装箱（box）到堆上
end
c = counter()
println("box: ", (c(), c()))    # box: (1, 2)

function make_adder(k)
    x -> x + k              # 只读捕获
end
println("adder: ", make_adder(10)(5))   # adder: 15
```

`counter` 里的 `n` 被闭包改写，于是被装进 `Core.Box`，`c()` 每次通过盒子读写。这是语义要求：外层和内层必须看到同一个变量，代价是一次间接访问加运行时类型分派。

若捕获的变量在闭包创建之后不再改写，可以用 `let r = r` 新建一个作用域内的只读变量，编译器就能取消装箱；`do` 块是同一个机制的语法糖（见"实际用途"一节）。

📘 [Julia · Performance of captured variables](https://docs.julialang.org/en/v1/manual/performance-tips/#Performance-of-captured-variables)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 lambda 直接引用外层局部变量就是捕获，捕获是运行时的：编译器把被捕获的局部变量"提升"（hoist）成编译器生成的类（closure class）的字段，匿名函数变成该类的一个实例方法，委托实例持有这个类实例。`static` lambda 则禁止任何捕获，用来避免意外的状态共享。

```csharp
using System;

class Program
{
    static Func<int> Counter()
    {
        int n = 0;                       // 被提升为编译器生成类的字段
        return () => ++n;
    }

    static void Main()
    {
        var c = Counter();
        Console.WriteLine($"closure: {c()} {c()}");   // closure: 1 2

        int outer = 10;
        Func<int, int> add = x => x + outer;          // 捕获变量（引用语义）
        outer = 99;
        Console.WriteLine($"later: {add(1)}");        // later: 100

        Func<int, int> sq = static x => x * x;        // static lambda：禁止捕获
        Console.WriteLine($"static: {sq(4)}");        // static: 16
    }
}
```

`Counter()` 返回的委托持有编译器生成的 `__Locals` 实例，`n` 成了它的字段，所以函数返回后 `n` 仍然活着，两次调用得到 1 和 2。`add` 捕获 `outer` 之后，外层把 `outer` 改成 99，闭包看到的是新值，因为共享的是同一个字段。C# 规范的原话是："为每个捕获了局部变量的块生成一个编译器生成的类，使不同块中的局部变量可以有独立的生命周期"，并把这个过程称为把局部变量"提升"为字段。

要明确表示"这个 lambda 不该捕获任何东西"就写 `static x => x * x`；一旦它需要引用外层变量，编译器会直接报错，这比事后排查意外的状态共享便宜得多。

📘 [MS Learn · C# 规范 · Expressions（捕获与编译器生成的类）](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/expressions)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的闭包是运行时的函数对象，捕获变量本身而不是值的快照，闭包与外层共享同一份存储；生命周期完全交给垃圾回收，语言不提供 `move`、捕获列表或引用限定符。`late` 只影响初始化时机：`late` 变量在被读取时才求值，闭包里的读取同样触发这一规则。

```dart
Function makeCounter() {
  var n = 0;
  return () => ++n;           // 闭包捕获变量本身（引用语义）
}

late String config;           // late：第一次读取时才算初始化完成

void main() {
  final c = makeCounter();
  print('closure: ${c()} ${c()}');   // closure: 1 2

  config = 'ready';                  // 若从不赋值，读它抛 LateInitializationError
  final read = () => config;         // 闭包里的 late 变量同样延迟初始化
  print('late: ${read()}');          // late: ready
}
```

`makeCounter` 返回的闭包和外层共享 `n`，所以得到 1 和 2；`late String config;` 是一个"稍后初始化"的非空变量，第一次读取才检查是否已赋值，没赋值就抛 `LateInitializationError`。

带初始化式的 `late` 则是惰性求值：`late String temperature = readThermometer();` 在第一次读取时才调用 `readThermometer()`，把它放进闭包也一样——闭包被调用时才触发初始化，所以 `late` 常被用来给闭包内的昂贵字段做懒加载。

📘 [Dart · Variables（Late variables）](https://dart.dev/language/variables#late-variables)

{{% /tab %}}

{{% tab header="R" %}}

R 的闭包由函数对象加上它的定义环境组成，查找自由变量遵守词法作用域；同时 R 是惰性求值语言，函数实参是 promise，在真正被使用之前不求值。写外层变量用 `<<-`，它会在父环境中查找并赋值，而不是在当前环境新建变量。

```r
counter <- function() {
  n <- 0
  function() { n <<- n + 1; n }   # <<- 修改外层环境的 n
}
ctr <- counter()
a <- ctr()
b <- ctr()
print(c(a, b))                     # [1] 1 2

make_adder <- function(k) function(x) x + k   # 词法作用域
print(make_adder(10)(5))           # [1] 15

f <- function(a) "a 从未被使用"
print(f(stop("永远不会执行")))      # [1] "a 从未被使用"
```

`counter` 里的 `n` 属于 `counter()` 的求值环境，`<<-` 让它被改写，所以两次调用是 1、2 而不是各返回 1；`make_adder` 演示词法作用域，`k` 在创建时就绑定在 `make_adder(10)` 的环境里。

`f(stop("永远不会执行"))` 说明惰性求值：实参 `stop(...)` 从未被使用，所以永远不会执行。反过来说，实参里的副作用不能当作控制流使用，官方语言定义明确提醒"用实参制造副作用是坏风格"。

📘 [R Language Definition · Promise objects](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Promise-objects)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有闭包，也没有捕获语法：函数只能声明在容器（文件、结构体）层级，没有 lambda 表达式，函数值退化为"函数指针 + 显式上下文"。官方标准库把这一点用成了惯用法——凡是需要携带状态的回调都手工打包上下文。

```zig
const std = @import("std");

// Zig 没有闭包：把“捕获”的状态放进结构体，连同函数一起传
const Adder = struct {
    base: i32,
    fn apply(ctx: *const Adder, x: i32) i32 {
        return ctx.base + x;      // 显式的上下文参数
    }
};

pub fn main() void {
    const a = Adder{ .base = 41 };
    std.debug.print("{d}\n", .{Adder.apply(&a, 1)});   // 42
    const add: *const fn (*const Adder, i32) i32 = Adder.apply;   // 函数指针
    std.debug.print("{d}\n", .{add(&a, 1)});           // 42
}
```

`Adder.apply` 的 `ctx: *const Adder` 就是被显式化的捕获环境：调用者负责提供它，也负责它的生命周期；函数指针 `*const fn (*const Adder, i32) i32` 加上具体的上下文类型就构成一个可传递的回调。

标准库里的 `std.mem.Allocator` 是同一模式的工业级版本，它就是一个带 `ptr: *anyopaque` 与 `vtable: *const VTable` 的结构体。Zig 里不存在"按值还是按引用捕获"的选择，因为根本没有隐式捕获，一切都在参数列表上写明。

📘 [Zig · std.mem.Allocator（ptr + vtable 模式）](https://ziglang.org/documentation/master/std/#std.mem.Allocator)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的函数都是闭包，外层局部变量被引用后就成为它的 upvalue，按变量共享；全局名字其实是 `_ENV.name` 的语法糖，`_ENV` 本身也是一个 upvalue，替换它就能替换整段代码的全局环境。Lua 5.5 起 `global` 变成声明语句用的关键字，`for` 的控制变量是只读的。

```lua
local function counter()
  local n = 0
  return function() n = n + 1; return n end   -- n 是 upvalue
end
local c = counter()
local first = c()
local second = c()
print(first, second)    -- 1  2

local x = 20
local t = {}
for i = 1, 3 do
  local y = 0
  t[i] = function() y = y + 1; return x + y end   -- 每个闭包有各自的 y
end
print(t[1](), t[2](), t[3]())    -- 21  21  21

local function with_env(env)
  local _ENV = env          -- 之后的自由名字都在 env 里查
  return function() return answer end
end
print(with_env({ answer = 42 })())   -- 42
```

`counter` 里的 `n` 被提升为 upvalue 存放在堆上，两次调用得到 1 和 2。第二个例子来自官方手册：手册明确写"每次执行 `local` 语句都会定义新的局部变量"，并给出同样的例子——循环里十个闭包各用各的 `y`，而外层的 `x` 被共享。第三个例子演示 `_ENV`：`local _ENV = env` 之后的自由名字都去 `env` 里查，于是返回 42。

判断两个闭包是否共享同一个 upvalue，可以用 `debug.upvalueid`；它返回相同的 id 就说明两者引用的是同一个变量。

📘 [Lua 5.5 · Visibility Rules（闭包与 upvalue）](https://www.lua.org/manual/5.5/manual.html#3.5)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的闭包在运行时和 JavaScript 完全一样，捕获变量本身；类型系统只多做两件事：给闭包标注参数与返回类型（泛型回调、显式的 `this` 参数），以及在闭包内决定类型收窄能不能沿用。TypeScript 7 换成了 Go 重写的原生编译器——官方公告的原话是 [a 10x faster native port of TypeScript](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)；编译速度变了，但捕获与作用域语义没有任何变化。

```typescript
function counter(): () => number {
  let n = 0;
  return () => ++n;              // 与 JS 一致：按变量（引用）捕获
}
const c = counter();
console.log("ref:", c(), c());   // ref: 1 2

const byVar: Array<() => number> = [];
for (var i = 0; i < 3; i++) byVar.push(() => i);
console.log("var:", byVar.map((f) => f()));   // var: [ 3, 3, 3 ]

const byLet: Array<() => number> = [];
for (let j = 0; j < 3; j++) byLet.push(() => j);
console.log("let:", byLet.map((f) => f()));   // let: [ 0, 1, 2 ]
```

`byVar` 与 `byLet` 的差别只来自 `var`/`let` 的作用域：`var i` 是函数级的一个变量，三个闭包共享它；`let j` 每次迭代创建新绑定，所以得到 `[0, 1, 2]`。类型系统不会阻止前者——它没有任何类型错误，只是语义如此。

闭包的类型写法是 `(x: number) => number`；如果闭包会改写被捕获的变量，TS 5.4 起"最后一次赋值之后的收窄"才能在闭包内沿用，而一旦该变量在任意嵌套函数里被再次赋值，收窄立即失效。

📘 [TypeScript 5.4 · Preserved Narrowing in Closures](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的闭包捕获变量所在的词法环境记录，不看值：`var` 是函数级作用域，`let`/`const` 是块级且每次 `for` 迭代新建绑定。闭包的存储由引擎的垃圾回收管理，V8 的 TurboFan 还会做逃逸分析，把不逃逸的闭包上下文直接优化掉。

```javascript
function counter() {
  let n = 0;
  return () => ++n;            // 捕获变量 n（引用），不是快照
}
const c = counter();
console.log("ref:", c(), c(), c());   // ref: 1 2 3

const byVar = [];
for (var i = 0; i < 3; i++) byVar.push(() => i);
console.log("var:", byVar.map((f) => f()));   // var: [ 3, 3, 3 ]

const byLet = [];
for (let j = 0; j < 3; j++) byLet.push(() => j);
console.log("let:", byLet.map((f) => f()));   // let: [ 0, 1, 2 ]
```

`counter` 返回的箭头函数改的是同一个 `n`，所以是 1、2、3。`var i` 在函数级只有一份，三个回调最后都读到 3；`let j` 每轮新建绑定，得到 `[0, 1, 2]`——MDN 把"在循环里创建闭包"单列为常见错误，根因就是所有闭包共享同一个词法环境记录。

闭包会延长被捕获变量的生命周期。V8 官方博客提到 TurboFan 的逃逸分析可以完全消除不逃逸的上下文分配（例如 `mapAdd` 里的自由变量 `x`），但这是实现优化；语言层面按"闭包持有整个环境"来推理才安全。

需要把一个闭包的生命周期钉在词法作用域上，可以用 `using` 声明（ES2026 起进入标准，Node 24 及以上支持；本文示例在 Node 24.20.0 上运行，Node 26 的语义相同）：

📘 [MDN · Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的闭包是 `Closure` 类的实例：匿名函数必须用 `use` 显式列出要捕获的变量，默认按值，写 `use (&$x)` 才是按引用；PHP 7.4 起的箭头函数 `fn($x) => expr` 自动按值捕获外层变量，不需要 `use`。捕获发生在闭包创建的那一刻。

```php
<?php
$y = 1;
$fn1 = fn($x) => $x + $y;              // 箭头函数：自动按值捕获
$fn2 = function ($x) use ($y) {         // 匿名函数：必须写 use
    return $x + $y;
};
$n = 0;
$bump = function () use (&$n) { return ++$n; };   // use (&$n)：按引用捕获
$y = 100;                                // 不影响已按值捕获的副本
$a = $fn1(3);
$b = $fn2(3);
$p = $bump();
$q = $bump();
echo $a, " ", $b, " ", $p, " ", $q, "\n";   // 4 4 1 2
```

`$fn1` 与 `$fn2` 行为完全相同，只是箭头函数省掉了 `use`；后面把 `$y` 改成 100 也不会改变 `$fn1(3)` 的结果，因为捕获的是创建时的值 1。`$bump` 用 `use (&$n)` 按引用捕获，两次调用返回 1 和 2，改动对外层可见。

按引用捕获本质上是"共享变量槽"：一个闭包改了，其他同样按引用捕获该变量的闭包都会看到；需要独立快照就按值捕获。PHP 8.5 起仍然没有捕获列表或 `move` 之类的语法，选择哪一种是代码里唯一能表达所有权的方式。

📘 [PHP · Arrow Functions](https://www.php.net/manual/en/functions.arrow.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的块、`Proc`、`lambda`/`->` 都是闭包：官方文档说 `Proc` 对象"记住并能使用创建它的整个上下文"。方法是严格的值传递，闭包是唯一的例外——块内对块外局部变量赋值会写回外层变量，除非块参数把名字遮蔽。

```ruby
def counter
  n = 0
  -> { n += 1 }              # lambda 捕获局部变量 n（引用）
end
c = counter
p [c.call, c.call, c.call]   # [1, 2, 3]

x = 0
[1, 2].each { x += 1 }       # 块内赋值写回外层局部变量
p x                          # 2

y = 0
[1, 2].each { |y| y += 1 }   # 块参数遮蔽外层 y
p y                          # 0

fs = []
for i in 1..3
  fs << -> { i }             # for 不引入新作用域，三个闭包共享同一个 i
end
p fs.map(&:call)             # [3, 3, 3]

fs2 = (1..3).map { |i| -> { i } }   # 块参数每轮新建
p fs2.map(&:call)                   # [1, 2, 3]
```

`counter` 返回的 lambda 与外层共享 `n`，得到 `[1, 2, 3]`。`[1, 2].each { x += 1 }` 把外层的 `x` 改成了 2；而 `{ |y| y += 1 }` 里的 `y` 是块参数，遮蔽了外层同名变量，所以外层仍是 0——这是块参数与普通赋值最需要分清的差别。

`for` 不创建新作用域，三个闭包共享同一个 `i`；换成 `map { |i| -> { i } }` 就每轮独立。官方文档在同一页写得很直白："块会创建新作用域"，而"`for` 循环不像块那样创建新作用域"。

📘 [Ruby · Proc](https://docs.ruby-lang.org/en/master/Proc.html)

{{% /tab %}}

{{< /tabpane >}}

### 生命周期与逃逸

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 把"闭包能不能活过当前作用域"变成编译期问题：按借用捕获的闭包类型带着生命周期参数，只要它引用了局部变量，就别想返回或离开作用域。想让闭包逃逸，要么用 `move` 把捕获的东西按值搬进去，要么用 trait object 擦除类型并存放在堆上。

```rust
fn make_adder(n: i32) -> impl Fn(i32) -> i32 {   // impl Fn：编译期单态化（monomorphization），无堆分配
    move |x| x + n
}

fn make_boxed(n: i32) -> Box<dyn Fn(i32) -> i32> {   // Box<dyn Fn>：类型擦除（type erasure）
    Box::new(move |x| x + n)
}

fn main() {
    let add2 = make_adder(2);
    println!("impl Fn: {}", add2(40));            // impl Fn: 42

    let fns: Vec<Box<dyn Fn(i32) -> i32>> = vec![make_boxed(1), make_boxed(10)];
    println!("boxed: {}", fns[1](5));             // boxed: 15

    let s = String::from("owned");
    let get = move || s.len();                    // 按值捕获才能逃逸出函数体
    println!("escaped: {}", get());               // escaped: 5
}
```

`make_adder` 返回 `impl Fn(i32) -> i32`，编译器为每个具体闭包生成一个类型，调用点单态化、零分配；`make_boxed` 返回 `Box<dyn Fn(i32) -> i32>`，用 vtable 做动态派发，可以塞进同一个 `Vec`，代价是一次堆分配加一次间接调用。

两者都必须写 `move`：如果写成 `|| x + n` 并试图返回，编译器会给出 E0373——"closure may outlive the current function, but it borrows n"。实用规则是：性能敏感、类型唯一的场合用 `impl Fn` 或泛型参数；要存进集合、跨线程或做回调表，就用 `Box<dyn Fn>` 或 `Arc<dyn Fn + Send + Sync>`。

📘 [Rust Reference · Closure expressions（捕获与 trait 实现）](https://doc.rust-lang.org/reference/expressions/closure-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 里闭包参数默认是 non-escaping：函数返回后就不允许再调用它，编译器因此能做更强优化，也不会产生引用环。要存进属性、数组或传给异步 API，必须显式标 `@escaping`；而被标记的闭包引用 `self` 时又要额外考虑循环引用。

```swift
var handlers: [() -> Int] = []

func store(_ h: @escaping () -> Int) { handlers.append(h) }  // 逃逸：必须 @escaping
func call(_ h: () -> Int) -> Int { h() }                     // 默认 non-escaping

func makeCounter() -> () -> Int {
    var n = 0
    return { n += 1; return n }   // 返回闭包 ⇒ 捕获的 n 被提升到堆
}

let c = makeCounter()
store(c)
print("escaping:", handlers[0](), call(c))    // escaping: 1 2

final class Node {
    var name: String
    var onChange: (() -> Void)?
    init(name: String) { self.name = name }
    deinit { print("deinit \(name)") }
}
do {
    let n = Node(name: "leaky")
    n.onChange = { print("changed", n.name) }   // 🛑 self → 闭包 → self 强引用环
    n.onChange?()
}                                                // 没有 deinit 输出：对象泄漏
print("end")                                     // end
```

`store` 的 `@escaping` 是必需的：去掉它，`handlers.append(h)` 立刻编译报错，提示"converting non-escaping parameter 'h' to generic parameter 'Element' may allow it to escape"。`makeCounter` 返回闭包，捕获的 `n` 被提升到堆上并随闭包存活。

最后那个 `Node` 演示闭包与对象互相强引用：`onChange` 持有闭包，闭包持有 `n`，两个引用计数都不会归零，`deinit` 永远不执行——上面这段程序的输出里只有 `changed leaky` 和 `end`。修法是写捕获列表 `[weak self]` 或 `[unowned self]`。

📘 [Swift · Automatic Reference Counting（闭包的强引用环与捕获列表）](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/automaticreferencecounting/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 不在类型系统里区分栈与堆，而是由编译器做逃逸分析：变量若在函数返回后仍被引用，就分配在堆上交给 GC。闭包是逃逸的主要来源之一，`go build -gcflags=-m` 会把每个决定打印出来。

```go
package main

import "fmt"

type Acc struct{ n int }

func makeCounter() func() int { // 返回的闭包逃逸，n 被分配到堆
	n := 0
	return func() int { n++; return n }
}

func newAcc() *Acc { // 返回局部变量的地址 ⇒ 逃逸到堆
	a := Acc{}
	return &a
}

func main() {
	c := makeCounter()
	fmt.Println("counter:", c(), c()) // counter: 1 2
	fmt.Println("acc:", newAcc().n)    // acc: 0
}
```

用 `go build -gcflags='-m' escape.go` 能看到编译器给出的三行结论：`./escape.go:8:2: moved to heap: n`、`./escape.go:9:9: func literal escapes to heap`、`./escape.go:13:2: moved to heap: a`。逃逸不是错误，只是成本：堆分配加 GC 压力。

反过来说，只要闭包本身不逃逸，捕获的变量就能留在栈上；性能敏感的内层循环里，把闭包存进长命 map 或传给 `go` 语句之前，值得先想一下是否真的需要逃逸。

📘 [Go FAQ · How do I know whether a variable is allocated on the heap or the stack?](https://go.dev/doc/faq#stack_or_heap)

{{% /tab %}}

{{% tab header="Python" %}}

Python 不区分栈与堆：闭包持有的 cell 和函数对象都由引用计数加循环 GC 管理，只要闭包可达，被捕获的对象就活着。这消灭了悬垂引用，代价是"看不见的持有"——一个长命闭包能让整片对象图无法回收。

```python
import gc
import weakref

class Big:
    pass

def make():
    b = Big()
    ref = weakref.ref(b)
    def get():
        return b            # 闭包持有 b：只要闭包活着，对象就不会被回收
    return get, ref

get, ref = make()
gc.collect()
print("alive:", ref() is not None)   # alive: True
del get                              # 闭包被回收
gc.collect()
print("alive:", ref() is not None)   # alive: False

def make_counter():
    n = 0
    return lambda: n + 1             # 闭包把 n 的 cell 挂到函数对象上
print("cell:", make_counter()(), make_counter()())   # cell: 1 1
```

`make()` 返回的闭包持有 `b`，所以手动 `gc.collect()` 之后弱引用仍然活着；`del get` 之后同一个弱引用立刻变成 `None`，可见对象是被闭包钉住的。`make_counter()` 每次调用创建独立的 cell，所以两个闭包各算各的，都返回 1。

常见的泄漏就是长命闭包意外持有大对象：注册后从不注销的回调、`functools.cache` 装饰过的函数、模块级字典里的 lambda。用 `weakref`、显式清空容器，或者干脆只捕获需要的字段，都能断开这种持有。

📘 [Python · weakref](https://docs.python.org/3/library/weakref.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin/JVM 的闭包与普通对象一样由 GC 管理：捕获的变量被装进 `Ref` 对象（只读时可被内联），闭包对象和它捕获的东西一起存活。Kotlin 没有 C++ 那种悬垂风险，但和 Java 一样有"闭包持有对象导致泄漏"的问题，尤其是长命回调。

```kotlin
fun make(): () -> Int {
    var n = 0
    return { n += 1; n }     // 逃逸：n 被放进 Ref 对象，分配到堆
}

fun main() {
    val c = make()
    println("escaped: ${c()} ${c()}")        // escaped: 1 2

    val big = StringBuilder("x".repeat(1000))
    val keep = { big.length }                // 闭包持有引用，big 无法被回收
    println("retained: ${keep()}")            // retained: 1000
}
```

`make()` 返回的 lambda 捕获了 `var n`，编译后会生成一个带 `element` 字段的 `Ref` 对象，闭包持有它，所以两次调用得到 1 和 2；只要这个闭包可达，`n` 就不可回收。`keep` 持有 `StringBuilder`，把这样的 lambda 存进单例的监听器列表就是最常见的一类泄漏。

Kotlin 的 `inline` 高阶函数（`forEach`、`filter`、`map` 都是 inline）在调用点展开，不会生成闭包对象，也没有额外的捕获分配；性能敏感的路径优先用这些内联版本，或者用 `Sequence` 把流水线串起来。

📘 [Kotlin · Lambda expressions（闭包与 inline）](https://kotlinlang.org/docs/lambdas.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 lambda 与匿名内部类在捕获局部变量时都只捕获"有效 final"的那份副本，这些副本成为闭包对象的字段：闭包对象活着它们就活着，闭包对象不可达就可以回收。此外 HotSpot 会在 JIT 阶段做逃逸分析，把不逃逸的对象直接在栈上分配甚至拆散。

```java
import java.util.function.IntSupplier;

public class Main {
    static IntSupplier make() {
        int[] n = {0};
        return () -> ++n[0];          // 委托持有捕获的副本，存活到委托被回收
    }

    public static void main(String[] args) {
        IntSupplier c = make();
        System.out.println("heap: " + c.getAsInt() + " " + c.getAsInt());   // heap: 1 2

        int sum = 0;
        for (int i = 0; i < 3; i++) {
            sum += new int[]{i}[0];   // 不逃逸的分配：JIT 可做标量替换
        }
        System.out.println("ea: " + sum);   // ea: 3
    }
}
```

`make()` 返回的 `IntSupplier` 持有被捕获的数组引用，所以两次调用是 1 和 2；在委托被回收之前，那个数组一直可达。这也是事件监听器泄漏的机制：长命组件持有委托，委托又持有它捕获的一切。

Oracle 官方文档对逃逸分析的表述是："HotSpot Server Compiler 可以分析一个新对象的使用范围，决定是否把它分配在 Java 堆上"，并说明"该特性自 Java SE 6u23 起默认支持并开启"。所以 `new int[]{i}[0]` 这类临时分配通常不会真的进堆，但这属于实现优化，不能当作语言保证。

📘 [Oracle · Java HotSpot VM Performance Enhancements（Escape Analysis）](https://docs.oracle.com/en/java/javase/25/vm/java-hotspot-virtual-machine-performance-enhancements.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的 lambda 是一个带 `operator()` 的闭包类对象，它的成员就是被捕获的实体：按值捕获的成员随闭包对象一起消亡，按引用捕获的成员只是一个引用。返回 lambda 本身没问题（闭包对象会被移动或拷贝出去），返回"按引用捕获了局部变量的 lambda"就是悬垂，语言不做任何检查。

```cpp
#include <functional>
#include <iostream>
#include <string>

std::function<int()> safe() {
    int local = 42;
    return [local] { return local; };   // ✅ 按值捕获，可以安全返回
}

std::function<int()> dangling() {
    int local = 42;
    return [&] { return local; };       // 🛑 悬垂：返回后 local 已销毁
}

int main() {
    std::cout << "safe: " << safe()() << '\n';   // safe: 42
    // std::cout << dangling()() << '\n';        // 🛑 未定义行为，不要运行
}
```

`safe()` 里的 `[local]` 让闭包对象自带一份副本，`f() == 42` 是可移植的；`dangling()` 里的 `[&]` 只保存引用，函数返回后 `local` 已被销毁，调用它就是未定义行为——可能打印 42，也可能崩溃，编译器未必警告。

C++ Core Guidelines 的 F.53 正是这条规则：不要在会用于非局部（返回、存堆、跨线程）的 lambda 里按引用捕获。需要把本地状态带出去时，用 `[p = std::move(p)]`、`[sp = std::make_shared<T>(...)]` 之类的初始化捕获明确转移所有权。

📘 [C++ Core Guidelines（F.53 避免在非局部使用的 lambda 中按引用捕获）](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

{{% /tab %}}

{{% tab header="C" %}}

C 没有对象也没有 GC，所谓"闭包的生命周期"就是"上下文那块内存的生命周期"，全部由程序员负责。上下文放在栈上，回调就不能活过那个栈帧；要跨界传递，必须放到堆上或静态存储区。

```c
#include <stdio.h>
#include <stdlib.h>

/* “闭包”= 函数指针 + 上下文指针；生命周期由程序员保证 */
typedef struct {
    int (*fn)(void *ctx);
    void *ctx;
} Closure;

typedef struct { int base; } Adder;

static int adder_apply(void *ctx) { return ((Adder *)ctx)->base + 1; }

/* 上下文在堆上分配，因此可以安全地“逃逸”出本函数 */
static Closure make_adder(int base) {
    Adder *a = malloc(sizeof *a);
    a->base = base;
    Closure c = { adder_apply, a };
    return c;
}

int main(void) {
    Closure c = make_adder(41);
    printf("heap ctx: %d\n", c.fn(c.ctx));   /* heap ctx: 42 */
    free(c.ctx);                             /* 谁分配谁释放，语言不帮忙 */
    return 0;
}
```

`make_adder` 在堆上分配 `Adder`，把函数指针和上下文打包成 `Closure` 返回，调用点只需要 `c.fn(c.ctx)`；用完 `free(c.ctx)`，漏掉就是泄漏，提前释放再调用就是解引用悬垂指针。

如果上下文放在栈上（`Closure c = { adder_apply, &stack_ctx };`），那它只能在本函数内同步用完；一旦存进全局表、交给线程或交给 `qsort` 这类会延后调用的 API，就必须确保那块内存在回调触发时仍然有效。

📘 [cppreference · Pointers（函数指针）](https://en.cppreference.com/w/c/language/pointer)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的闭包与捕获变量一起被 GC 管理，逃逸的闭包会把捕获变量装箱到堆上，由运行时负责回收；没有手动释放，也不会像 C 那样悬垂。需要关注的不是安全而是性能：装箱会导致类型不稳定，官方性能提示要求在意性能时用类型标注或 `let` 取消装箱。

```julia
function make_closure()
    n = 0
    () -> (n += 1)     # n 逃逸 ⇒ 装箱到堆，闭包与 n 一起被 GC 管理
end

f = make_closure()
println("escaped: ", (f(), f()))    # escaped: (1, 2)

function abmult(r0::Int)
    r = r0
    if r < 0
        r = -r
    end
    x -> x * r          # r 被改写 ⇒ 解析器为它生成 Core.Box
end
println("boxed: ", abmult(-3)(4))   # boxed: 12

function abmult2(r0::Int)
    r = abs(r0)
    let r = r
        x -> x * r      # let 新建只读变量 ⇒ 不装箱
    end
end
println("unboxed: ", abmult2(-3)(4))   # unboxed: 12
```

`make_closure` 返回的闭包让 `n` 装箱，箱子和闭包一起活着。`abmult` 返回 `x -> x * r`，只要 `r` 在闭包创建后还可能被改写，解析器就会生成 `Core.Box`；官方文档解释了原因：语言规定内层的 `r` 与外层的 `r` 必须是同一个变量，即使外层（或另一个内层函数）改写了它。

`abmult2` 用 `let r = r` 在闭包的作用域里新建一个不会再变的变量，装箱随之消失。可以用 `@code_warntype` 检查返回值里是否出现装箱后的抽象类型。

📘 [Julia · Performance Tips（Performance of captured variables）](https://docs.julialang.org/en/v1/manual/performance-tips/#Performance-of-captured-variables)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的闭包对象（编译器生成的类实例）和普通对象一样受 GC 管理：只要委托可达，被捕获的变量就不可回收。而 `ref struct`（例如 `Span<T>`）因为必须留在栈上，编译器直接禁止把它捕获进 lambda 或局部函数——这是少数几条编译期拦截的逃逸规则。

```csharp
using System;
using System.Collections.Generic;

class Program
{
    static Func<int> Make()
    {
        int n = 0;
        return () => ++n;      // 委托持有闭包对象 ⇒ n 存活到委托被回收
    }

    static void Main()
    {
        var c = Make();
        Console.WriteLine($"heap: {c()} {c()}");   // heap: 1 2

        Span<int> span = stackalloc int[2];
        // Action capture = () => Console.WriteLine(span.Length);
        // 🛑 编译错误：不能捕获 ref struct 变量

        var handlers = new List<Action>();
        for (int i = 0; i < 2; i++)
            handlers.Add(() => Console.WriteLine(i));   // for 共享 i
    }
}
```

`Make()` 返回的委托持有闭包对象，`n` 随之存活。官方文档对此的说明是："被捕获的变量在引用它的委托可被回收之前不会被垃圾回收"，所以长命委托（事件处理器、静态缓存里的回调）会拖住整片捕获图，这是 C# 里最常见的内存泄漏形式。

`ref struct` 的规则是硬性的：不能作为类字段、不能装箱、不能被 lambda 或局部函数捕获，因为任何一种都意味着栈上的东西逃到了堆上。要给事件解除引用，就在不再需要时把委托从事件或列表里移除。

📘 [MS Learn · ref struct types（不能捕获进 lambda）](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/ref-struct)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的闭包没有独立于 GC 的生命周期概念：闭包对象和被捕获的变量都由垃圾回收管理，语言不提供释放、引用计数或 `@escaping` 一类的标注。需要留意的只有"谁还引用着闭包"——监听器、定时器和全局列表是最常见的长期持有者。

```dart
Function makeCounter() {
  var n = 0;
  return () => ++n;      // Dart 的闭包由 GC 管理，没有手动生命周期
}

void main() {
  final c = makeCounter();
  print('gc: ${c()} ${c()}');   // gc: 1 2

  // Dart 没有“引用悬垂”：捕获的变量被提升到堆上的 context 对象
  final fns = <Function>[];
  for (var i = 0; i < 3; i++) {
    fns.add(() => i);            // 规范保证每轮是独立变量
  }
  print(fns.map((f) => f()).toList());   // [0, 1, 2]
}
```

`makeCounter()` 返回的闭包持有 `n`，两次调用得到 1 和 2；什么时候回收完全取决于闭包本身是否可达。`fns` 里三个闭包各捕获各自的 `i`，所以得到 `[0, 1, 2]`——Dart 规范明确写了传统 `for` 与 `for-in` 每次迭代都使用"独立的变量"，这一点见"闭包与循环变量"一节。

实践中最常见的泄漏在 Flutter 里：`State` 注册的回调没有在 `dispose` 里取消订阅，本质上是长命对象持有闭包；Dart 这一层没有任何编译期提示，只能靠代码纪律。

📘 [Dart · Functions（Lexical closures）](https://dart.dev/language/functions#lexical-closures)

{{% /tab %}}

{{% tab header="R" %}}

R 的闭包（函数加环境）由 GC 管理，不存在悬垂；但惰性求值会把"什么时候取值"推迟到第一次使用，promise 里保存的是表达式和它的环境，环境因此被持有。另一条 R 特有的性质是：`for` 的循环变量在循环结束后依然存在于当前环境。

```r
make <- function() {
  n <- 0
  function() { n <<- n + 1; n }   # 闭包环境由 GC 管理，不会悬垂
}
ctr <- make()
a <- ctr()
b <- ctr()
print(c(a, b))            # [1] 1 2

# R 的 for 循环变量活在当前环境里：循环结束后仍然存在
for (i in 1:3) {}
print(exists("i"))        # [1] TRUE
print(i)                  # [1] 3
```

`make()` 返回的函数环境里有 `n`，只要函数可达，`n` 就在，回收交给 GC。第二个例子是官方语言定义里的原话：循环结束后"变量名仍然存在，并且它的值是循环最后一次求值时的元素"，所以 `exists("i")` 返回 `TRUE`、`i` 等于 3。

这意味着循环里创建的闭包都会引用同一个 `i`（下一节展开），也意味着循环变量会意外泄漏到当前环境，覆盖同名变量。写函数时把循环体包进函数或 `local()`，可以让这些名字留在局部。

📘 [R Language Definition · for（循环变量在循环后仍存在）](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#for)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有 GC 也没有闭包，上下文生命周期完全手动：`defer`/`errdefer` 是唯一的自动化，语言不会替你判断某个指针是否还指向有效内存。与 C 的区别在于 Zig 的标准库把"谁拥有内存"写进类型（`Allocator`、切片、`*T` 与 `[]T` 的区分）。

```zig
const std = @import("std");

const Counter = struct {
    n: u32 = 0,
    fn bump(ctx: *Counter) u32 {
        ctx.n += 1;
        return ctx.n;
    }
};

pub fn main() !void {
    const a = std.heap.page_allocator;
    const c = try a.create(Counter);   // 上下文放堆上，生命周期由你控制
    defer a.destroy(c);                // 忘记这行就是泄漏，提前调用就是 use-after-free
    std.debug.print("{d} {d}\n", .{ Counter.bump(c), Counter.bump(c) });   // 1 2
}
```

`try a.create(Counter)` 在堆上创建上下文，`defer a.destroy(c);` 保证函数退出时释放；`Counter.bump(c)` 只是把上下文显式传进去，等价于 C 里的函数指针加 `void *`，但类型是安全的。忘记 `defer` 就是泄漏，在 `defer` 之后继续使用 `c` 就是 use-after-free。

凡是回调要活过创建者的场景，都要由调用者明确约定谁分配、谁释放；Zig 不提供闭包，也就不存在"捕获的东西被自动延长生命周期"这种隐式行为。

📘 [Zig · Memory（allocator 与手动生命周期）](https://ziglang.org/documentation/master/#Memory)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的闭包与 upvalue 都由 GC 管理，不存在悬垂：upvalue 打开时指向栈上的变量，一旦闭包存活到栈帧结束，Lua 会把它"关闭"并搬到堆上。能手动做的只有影响可达性——清空引用，必要时调用 `collectgarbage()`。

```lua
local function make()
  local n = 0
  return function() n = n + 1; return n end   -- upvalue 由 GC 管理
end
local c = make()
local first = c()
local second = c()
print(first, second)     -- 1  2

-- 断开引用后剩下的交给 GC
local f = make()
f = nil
collectgarbage("collect")
print("collected")   -- collected
```

`make()` 返回的闭包让 `n` 从栈转移到堆，`c()` 两次得到 1 和 2；Lua 的 upvalue 关闭机制保证了这一点，不需要程序员操心。把最后一个引用设为 `nil` 之后，闭包和它的 upvalue 一起变成垃圾，`collectgarbage("collect")` 会立刻回收。

真实项目里长期持有的闭包通常来自注册在表里的回调：从表中删掉条目就是"取消订阅"，否则闭包和它捕获的对象一直可达。弱表（`setmetatable(t, {__mode = "v"})`）可以让缓存不阻止回收，是 Lua 里处理这类问题的常用手段。

📘 [Lua 5.5 · Visibility Rules](https://www.lua.org/manual/5.5/manual.html#3.5)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的闭包生命周期与 JavaScript 完全相同：对象由 GC 管理，没有悬垂，也没有 `@escaping` 一类的逃逸标注。类型系统只补一条规则：TS 5.4 起，如果变量在闭包外有"最后一次赋值"，闭包内可以沿用那次赋值之后的类型收窄。但只要该变量在任意嵌套函数里被再赋值，收窄立刻失效。

```typescript
class Session {
  readonly id: string;
  constructor(id: string) { this.id = id; }
}

function keepSession(): () => string {
  const s = new Session("s1");
  return () => s.id;              // 闭包让 s 在函数返回后仍可达
}
const read = keepSession();
console.log("kept:", read());     // kept: s1

function getUrl(url: string | URL, names: string[]): string {
  if (typeof url === "string") url = new URL(url);
  return names
    .map((n) => {
      url.searchParams.set("name", n);   // TS 5.4：收窄在闭包内保留
      return url.toString();
    })
    .join("");
}
console.log("narrowed:", getUrl("https://x.test/", ["a"]));   // narrowed: https://x.test/?name=a
```

`keepSession()` 返回的闭包持有 `Session` 实例，函数返回后对象仍然可达，这是模块私有状态的基本形态。`getUrl` 演示收窄保持：`url = new URL(url)` 是最后一次赋值，所以 `map` 回调里的 `url` 被当作 `URL`，`searchParams` 可用。

官方文档同时提醒：一旦在嵌套函数里写了 `value = value` 这种赋值，闭包内的收窄就全部作废（示例会报 `'value' is possibly 'undefined'`）。需要跨闭包稳定的类型，就把它固定成局部 `const`。

📘 [TypeScript 5.4 · Preserved Narrowing in Closures](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的闭包由引擎的 GC 管理，被捕获的变量只要闭包可达就活着；V8 的 TurboFan 用逃逸分析把不逃逸的上下文分配直接消除。真正需要人工处理的是"注册与注销"：事件监听、定时器、观察者列表都必须配对释放。

```javascript
function makeReader() {
  const data = new Array(3).fill(7);   // 局部数组
  return () => data.length;            // 闭包让 data 在函数返回后继续存活
}
const read = makeReader();
console.log("kept alive:", read());    // kept alive: 3

// 事件监听不取消 ⇒ 闭包与它捕获的对象一直可达
const bus = new EventTarget();
const state = { hits: 0 };
const onPing = () => { state.hits += 1; };
bus.addEventListener("ping", onPing);
bus.dispatchEvent(new Event("ping"));
console.log("listener:", state.hits);  // listener: 1
bus.removeEventListener("ping", onPing);   // 必须配对移除，否则闭包泄漏
```

`makeReader` 返回的闭包让局部数组在函数返回后继续存活，这正是模块模式与私有状态的实现基础。第二个例子是浏览器与 Node 里最常见的泄漏：`addEventListener` 之后不 `removeEventListener`，监听器闭包和被它捕获的对象（往往是一整棵 DOM 或一个大对象）会一直可达；`AbortController` 的 `signal` 或 `{ once: true }` 是更省心的替代写法。

V8 官方博客说明了逃逸分析的边界：v7.1 起 TurboFan 的逃逸分析"能完全消除局部闭包上下文里的分配"（官方例子 `function mapAdd(a, x) { return a.map(y => y + x); }` 中的自由变量 `x`，某些场景提升约 40%），但前提是上下文不逃逸出优化单元，所以不要指望引擎帮你解决长期持有的引用。

需要把一个闭包持有的资源钉在词法作用域上，可以用 `using` 声明（TC39 的 Explicit Resource Management 提案，Node 24 及以上支持；上面的示例在 Node 24.20.0 与 Node 26 上语义相同）：

```javascript
class Conn {
  #closed = false;
  [Symbol.dispose]() { this.#closed = true; console.log("disposed"); }
  use() { return this.#closed ? "closed" : "open"; }
}

function makeReader() {
  using conn = new Conn();
  console.log("inside:", conn.use());   // inside: open
  return () => conn.use();              // 闭包逃逸，资源却已随作用域释放
}

const read2 = makeReader();             // disposed（作用域退出时同步释放）
console.log("after:", read2());         // after: closed
```

`conn` 在 `makeReader` 返回时被同步释放（打印 `disposed`），返回的闭包却仍然持有它，所以 `read2()` 拿到的是已释放的资源——`using` 只保证"按作用域释放"，它不会阻止闭包把引用带出去。MDN 把这个场景单列成"资源可能比声明活得更久"，要跟着调用释放就得在回调内部再写一层 `using` 别名。

📘 [MDN · Closures（含性能注意事项）](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的闭包是 `Closure` 对象，由引用计数加循环 GC 管理；按值捕获会在闭包对象里存一份 zval，按引用捕获（`use (&$x)`）则共享同一个变量槽。生命周期问题几乎都出在"谁还持有闭包"：事件表、静态数组、对象属性。

```php
<?php
function make() {
    $n = 0;
    return function () use (&$n) { return ++$n; };   // 闭包对象持有变量槽
}
$c = make();
$a = $c();
$b = $c();
echo $a, " ", $b, "\n";          // 1 2

class Bus {
    private array $listeners = [];
    public function on(callable $l): void { $this->listeners[] = $l; }
    public function off(callable $l): void {
        $this->listeners = array_filter($this->listeners, fn($x) => $x !== $l);
    }
    public function emit(): void { foreach ($this->listeners as $l) { $l(); } }
}

$bus = new Bus();
$state = new stdClass();
$state->hits = 0;
$on = function () use ($state) { $state->hits++; };   // 捕获对象句柄
$bus->on($on);
$bus->emit();
echo $state->hits, "\n";         // 1
$bus->off($on);                  // 取消订阅：否则闭包与 $state 一直可达
$bus->emit();
echo $state->hits, "\n";         // 1（已取消订阅）
```

`make()` 返回的闭包用 `use (&$n)` 持有变量槽，两次调用得到 1 和 2；按值捕获则会各存一份快照。第二个例子是典型的订阅泄漏：`Bus` 的 `$listeners` 持有闭包，闭包又捕获了 `$state` 对象，只要不调用 `off()`，`$state` 就无法回收；`off()` 摘掉同一个 `Closure` 实例后，`emit()` 不再触发它。

PHP 8.5 仍然没有弱引用监听器一类的设施，跨请求之外的长命场景要靠代码纪律：注册与注销成对出现，或者把监听器放在短命对象上。

📘 [PHP · Anonymous functions（Closure 与 use）](https://www.php.net/manual/en/functions.anonymous.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的闭包（块、`Proc`、`lambda`）由标记-清除 GC 管理，闭包与对象互相引用不会造成泄漏——这与 Swift 的强引用环正好相反。需要担心的只有"引用一直挂在某个长期对象上"这件事。

```ruby
def make
  n = 0
  -> { n += 1 }        # Proc 是闭包，n 由 GC 管理
end
c = make
p [c.call, c.call]     # [1, 2]

class Bus
  def initialize = @listeners = []
  def on(&blk) = @listeners << blk
  def off(&blk) = @listeners.delete(blk)
  def emit = @listeners.each(&:call)
end
bus = Bus.new
hits = 0
on = -> { hits += 1 }
bus.on(&on)
bus.emit
p hits            # 1
bus.off(&on)
bus.emit
p hits            # 1
```

`make` 返回的 lambda 持有 `n`，即使中间发生 GC 也依然可用；对象与回调互相引用同样能被回收，所以 Ruby 里不需要 `weak`/`unowned`。`Bus` 的例子演示真正要注意的一点：`off(&on)` 把同一个 `Proc` 从数组里删掉之后，`emit` 不再调用它，`hits` 保持 1；如果忘了 `off`，闭包和被它捕获的对象就会跟着 `Bus` 一起活着。

在长命结构（类变量、缓存、订阅表）里保存闭包时，删除条目的责任和注册的责任一样大。

📘 [Ruby · Proc（closures）](https://docs.ruby-lang.org/en/master/Proc.html)

{{% /tab %}}

{{< /tabpane >}}

### 闭包与循环变量

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `for` 循环变量每轮新建，本身不共享；陷阱出现在捕获方式上——闭包要活过循环就必须 `move`，否则借用检查器直接报错。换句话说，Rust 把这类问题变成了编译期错误，而不是运行时的意外结果。

```rust
fn main() {
    let mut fs: Vec<Box<dyn Fn() -> i32>> = Vec::new();
    for i in 0..3 {
        fs.push(Box::new(move || i));    // move：把当轮的 i 移进闭包
    }
    let got: Vec<i32> = fs.iter().map(|f| f()).collect();
    println!("move: {got:?}");           // move: [0, 1, 2]

    let mut total = 0;
    for i in 0..3 {
        let f = |x: i32| x + i;          // 只在循环体内使用：借用即可
        total += f(10);
    }
    println!("inline: {total}");         // inline: 33
}
```

`move || i` 把当轮的 `i`（`i32` 是 `Copy`）拷进闭包，三个闭包各持一份，输出 `[0, 1, 2]`。若写成 `|| i` 又试图把闭包塞进 `Vec<Box<dyn Fn() -> i32>>` 带出循环，编译器会报 E0597（"`i` does not live long enough"，借用活的没有 `Vec` 久）；把闭包改成直接返回、让它必须活过函数体，报的才是 E0373："closure may outlive the current function, but it borrows i"。

第二个例子说明借用捕获本身没问题：闭包只在循环体内立即使用，生命周期不超过一轮迭代，编译器和借用检查器都能证明它安全。所以判断标准只有一条——闭包是否逃出当前作用域。

📘 [Rust Reference · Closure expressions](https://doc.rust-lang.org/reference/expressions/closure-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的 `for-in` 循环变量每次迭代都是一个新的常量绑定，闭包捕获它天然安全；`while` 循环里手写的计数器是同一个变量，闭包就会共享最终值。Swift 没有 IIFE 惯用法，需要独立副本时一律在循环体内写 `let`。

```swift
var fs: [() -> Int] = []
for i in 0..<3 { fs.append { i } }        // for-in 每轮新建 i
print("for-in:", fs.map { $0() })          // for-in: [0, 1, 2]

var gs: [() -> Int] = []
var j = 0
while j < 3 { gs.append { j }; j += 1 }    // while 里 j 始终是同一个变量
print("while:", gs.map { $0() })           // while: [3, 3, 3]
```

`for i in 0..<3 { fs.append { i } }` 得到 `[0, 1, 2]`：每次迭代新建 `i`，闭包捕获各自的副本。`while j < 3 { gs.append { j }; j += 1 }` 得到 `[3, 3, 3]`：`j` 只有一份，三个闭包读到的都是循环结束后的值。

要在 `while` 里按轮捕获，就在循环体内写 `let copy = j` 再捕获 `copy`；这也适用于所有自管理的索引场景（例如用下标遍历数组并生成回调）。

📘 [Swift · Closures（捕获变量）](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的循环变量语义在 1.22 发生了不兼容变更：之前 `for` 声明的变量全循环只有一份，闭包与 goroutine 都会看到最终值；1.22 起每轮新建变量，闭包各拿各的。是否启用新语义由 `go.mod` 的语言版本决定，而不是工具链版本。

```go
package main

import "fmt"

func main() {
	var fs []func() int
	for i := 0; i < 3; i++ { // Go 1.22 起：每轮新建变量
		fs = append(fs, func() int { return i })
	}
	for _, f := range fs {
		fmt.Print(f(), " ") // 0 1 2
	}
	fmt.Println()

	var gs []func() int
	i := 0
	for i < 3 { // 循环外的 i 仍然只有一份
		gs = append(gs, func() int { return i })
		i++
	}
	for _, f := range gs {
		fmt.Print(f(), " ") // 3 3 3
	}
	fmt.Println()
}
```

官方规范现在明确写着"每次迭代都有自己的变量"：`for i := 0; i < 3; i++` 里第一个 `i` 由 init 语句声明，后续每个 `i` 在 post 语句之前隐式声明并拷入上一轮的值，`range` 变量同理。第二个例子里 `i` 声明在循环外，不在新语义的保护范围内，所以三个闭包输出 `3 3 3`。

版本分界要说清楚：新语义只对 `go.mod` 中 `go 1.22` 及以上的模块生效；Go 1.21 可以用 `GOEXPERIMENT=loopvar go build` 提前体验这套语义，1.22 起成为默认。为兼容旧代码，`go vet` 的"循环变量引用"警告也随语言版本调整。

📘 [Go Wiki · LoopvarExperiment](https://go.dev/wiki/LoopvarExperiment)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的闭包按变量捕获，`for` 循环变量在循环结束后依然存在，所有延迟调用的闭包最后都读到同一个终值——这就是"延迟绑定"。修复手段是在定义时把值固定下来：默认参数、`functools.partial`，或者干脆用工厂函数。

```python
from functools import partial

fs = [lambda: i for i in range(3)]
print("late:", [f() for f in fs])        # late: [2, 2, 2]

fs2 = [lambda i=i: i for i in range(3)]      # 默认参数在定义时求值
print("default:", [f() for f in fs2])        # default: [0, 1, 2]

fs3 = [partial(lambda i: i, i) for i in range(3)]
print("partial:", [f() for f in fs3])        # partial: [0, 1, 2]
```

`[lambda: i for i in range(3)]` 里三个 lambda 共享推导式作用域里的 `i`，调用时循环早已结束，所以是 `[2, 2, 2]`；`lambda i=i: i` 让 `i` 成为默认参数，默认值在函数定义时求值，得到 `[0, 1, 2]`；`functools.partial(lambda i: i, i)` 效果相同。

官方 FAQ 把这一条单列为"Why do lambdas defined in a loop with different values all return the same result?"，并推荐默认参数写法。注意 `while` 循环同理：循环变量始终是同一个变量，闭包不会自动快照。

📘 [Python FAQ · lambdas defined in a loop](https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 只有"增强 for"一种形式：规范给出的展开式里，循环体每次都声明一个新的 `val`，所以闭包捕获的是当轮的值，不存在共享陷阱。`while` 里手写的计数器仍然是同一个 `var`，需要自己拷一份。

```kotlin
fun main() {
    val fs = mutableListOf<() -> Int>()
    for (i in 1..3) fs.add { i }        // 展开为 val i = ...，每轮新建
    println("for: " + fs.map { it() })  // for: [1, 2, 3]

    val gs = mutableListOf<() -> Int>()
    var j = 0
    while (j < 3) { gs.add { j }; j++ } // while 里 j 是同一个 var
    println("while: " + gs.map { it() }) // while: [3, 3, 3]
}
```

官方规范把 `for (VarDecl in C) Body` 展开成 `while ($iterator.hasNext()) { val VarDecl = __iterator.next(); ... }`。`val` 位于循环体内，每次迭代重新声明，这一条同时解释了两件事：循环变量不可赋值（是 `val`），以及闭包天然每轮独立。

要在 `while` 里获得同样效果，就在体内写 `val copy = j`。Kotlin 没有 C 风格的三段 `for`，所以"普通 for 共享变量"这一整类问题在 Kotlin 里不存在。

📘 [Kotlin 规范 · For-loop statements](https://kotlinlang.org/spec/statements.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的两种 `for` 语义不同。JLS 明确写着："有效 final 的限制包括普通循环变量，但不包括增强 `for` 的循环变量，后者在每次迭代中被视为不同的变量。"所以 `for (int x : list)` 可以直接捕获，三段式 `for (int i = 0; ...)` 必须先拷一份。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.function.IntSupplier;

public class Main {
    public static void main(String[] args) {
        List<IntSupplier> fs = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            int copy = i;                 // 普通 for：必须手动拷一份
            fs.add(() -> copy);
        }
        int[] got = new int[fs.size()];
        for (int k = 0; k < fs.size(); k++) got[k] = fs.get(k).getAsInt();
        System.out.println("for: " + Arrays.toString(got));   // for: [0, 1, 2]

        List<IntSupplier> gs = new ArrayList<>();
        for (int x : new int[]{7, 8, 9}) {
            gs.add(() -> x);              // 增强 for：x 每轮新建，合法
        }
        System.out.println("for-each: " + gs.get(2).getAsInt());   // for-each: 9
    }
}
```

标准 `for` 里的 `i` 全循环只有一份，写 `() -> i` 既会因为共享而出错，也会因为 `i++` 改写而违反有效 final（编译直接报错），所以必须写 `int copy = i;` 再捕获。增强 `for` 的变量每次迭代新声明，可以直接捕获，上面的 `gs` 就拿到了 9。

需要按轮捕获索引而不是元素时，用 `IntStream.range(0, n).forEach(idx -> ...)` 的回调参数，或者显式拷一份 `i`。

📘 [JLS §15.27.2（有效 final 与增强 for）](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.27.2)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的 `for` 循环变量只有一份，而 lambda 又恰好能按引用捕获，两者相加就是最经典的悬垂：`[&i]` 把引用存进闭包，循环一结束引用就指向已销毁的对象。编译期不会有任何提示。

```cpp
#include <functional>
#include <iostream>
#include <vector>

int main() {
    std::vector<std::function<int()>> gs;
    for (int i = 0; i < 3; ++i) {
        gs.push_back([i] { return i; });      // ✅ 按值捕获：每轮一份
    }
    std::cout << "value: " << gs[0]() << gs[1]() << gs[2]() << '\n';   // value: 012

    std::vector<std::function<int()>> fs;
    for (int i = 0; i < 3; ++i) {
        fs.push_back([&i] { return i; });     // 🛑 按引用捕获：i 只有一份且循环后销毁
    }
    // std::cout << fs[0]() << '\n';          // 🛑 未定义行为，不要运行
    return 0;
}
```

`[i]` 按值捕获让每个闭包各持一份副本，输出 `012`。`[&i]` 能编译，问题出在调用时：循环结束后 `i` 已经离开作用域，`fs[0]()` 是未定义行为，可能打印 3，也可能崩溃，还可能因为寄存器复用打印出任意值。

如果确实需要多个闭包共享同一份可变计数器，就让它活得比所有闭包久，例如用 `auto counter = std::make_shared<int>(0);` 并按值捕获 `counter`（`shared_ptr` 的拷贝共享同一个对象）。这正是 Core Guidelines F.53 在循环里的具体表现。

📘 [cppreference · Lambda expressions（捕获）](https://en.cppreference.com/w/cpp/language/lambda)

{{% /tab %}}

{{% tab header="C" %}}

C 没有闭包，所以"循环变量被闭包捕获"这件事根本不存在，也没有任何隐式快照。取而代之的问题是"回调需要按轮不同的数据"：做法是把当轮的值显式拷进数组或结构体的字段，再让函数作用在指针上。手动管理这份拷贝，是 C 里唯一的"按轮捕获"。

```c
#include <stdio.h>

typedef struct { int captured; } Cell;

static int get(void *ctx) { return ((Cell *)ctx)->captured; }

int main(void) {
    Cell cells[3];
    for (int i = 0; i < 3; i++) {
        cells[i].captured = i;    /* 手动按轮复制：C 里“捕获”就是拷一份 */
    }
    for (int i = 0; i < 3; i++) {
        printf("%d ", get(&cells[i]));   /* 0 1 2 */
    }
    printf("\n");
    return 0;
}
```

`cells[i].captured = i;` 就是 C 版的按值捕获：循环变量 `i` 在下一轮会被改写，但每个 `cells[i]` 里存的是当时那份拷贝，所以输出 `0 1 2`。如果偷懒只保存 `&i`，或者让回调依赖全局的 `i`，所有回调都会读到最终值。

这在 C 里不会有任何警告，尤其在回调被延后调用（`qsort`、事件循环、线程）时极难排查。需要携带多个值时，就把它们一起打包进结构体，并把结构体数组的地址交给回调。

📘 [cppreference · Structures](https://en.cppreference.com/w/c/language/struct)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `for` 循环变量每轮新建，闭包捕获它天然安全；代价是可能触发装箱。`while` 循环里的计数器是同一个变量，闭包会共享最终值，这一点与 `for` 完全不同。

```julia
fs = Function[]
for i in 1:3
    push!(fs, () -> i)      # for 的迭代变量每轮新建
end
println("for: ", [f() for f in fs])    # for: [1, 2, 3]

function make_while()
    gs = Function[]
    i = 0
    while i < 3
        push!(gs, () -> i)  # while 里 i 是同一个局部变量
        i += 1
    end
    return gs
end
println("while: ", [f() for f in make_while()])   # while: [3, 3, 3]
```

官方手册的原话是："`for` 循环总是在循环体内引入新的迭代变量，无论外层作用域是否已有同名变量"，所以三个闭包分别捕获 1、2、3。`make_while` 里手写的 `i` 是同一个局部变量，闭包共享它，得到 `[3, 3, 3]`。

如果在全局作用域写 `while` 又想改外层变量，还必须显式写 `global`，否则赋值会新建局部变量；把循环包进函数（如上面的 `make_while`）是最省心的做法。性能上，循环里创建闭包常导致迭代变量装箱，能用生成器或 `let` 时优先用它们。

📘 [Julia · Control Flow（for 循环引入新的迭代变量）](https://docs.julialang.org/en/v1/manual/control-flow/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 有一条明确的时间分界线：C# 5 起 `foreach` 的循环变量"逻辑上位于循环内部"，闭包每轮捕获一份新副本；而 `for` 循环没有被改动，仍然只有一份变量。这条变更来自语言团队的官方公告。

```csharp
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        var fs = new List<Func<int>>();
        foreach (var i in new[] { 1, 2, 3 })
            fs.Add(() => i);            // C# 5 起 foreach 变量每轮新建
        Console.WriteLine(string.Join(",", fs.ConvertAll(f => f())));   // 1,2,3

        var gs = new List<Func<int>>();
        for (int i = 0; i < 3; i++)
            gs.Add(() => i);            // for 变量只有一份，仍然共享
        Console.WriteLine(string.Join(",", gs.ConvertAll(f => f())));   // 3,3,3
    }
}
```

`foreach (var i in new[] {1, 2, 3}) fs.Add(() => i);` 得到 1、2、3；`for (int i = 0; i < 3; i++) gs.Add(() => i);` 得到 3、3、3。官方公告的原话是："In C# 5, the loop variable of a foreach will be logically inside the loop, and therefore closures will close over a fresh copy of the variable each time. The 'for' loop will not be changed."

要在 `for` 里按轮捕获，就在循环体内写 `int copy = i;`（或把 `for` 换成 `foreach (var i in Enumerable.Range(0, 3))`）。

📘 [MS Learn（归档）· Closing over the loop variable, part two](https://learn.microsoft.com/en-us/archive/blogs/ericlippert/closing-over-the-loop-variable-part-two)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 规范直接把"循环里创建闭包"的陷阱堵死了：传统 `for` 的每一次迭代都使用"独立的变量"，`for-in` 也是。所以 Dart 里不存在 `var` 共享循环变量的问题，也不需要 IIFE、默认参数之类的技巧。

```dart
void main() {
  final fs = <Function>[];
  for (var i = 1; i <= 3; i++) {
    fs.add(() => i);      // 规范：每轮使用独立变量
  }
  print('for: ${fs.map((f) => f()).toList()}');    // for: [1, 2, 3]

  final gs = <Function>[];
  for (final v in [1, 2, 3]) {
    gs.add(() => v);      // for-in 同样每轮新建
  }
  print('for-in: ${gs.map((f) => f()).toList()}'); // for-in: [1, 2, 3]
}
```

Dart 规范对 `for (var v = e0; c; e)` 的执行过程写得很具体：第一轮使用初始声明创建的变量，之后每一轮都在执行 post 表达式之前新建一个变量 `v''` 并拷入当前值。规范的理由（rationale）里明确说，这是为了避免"所有闭包都捕获最后一个值"这个常见错误。

`for-in` 的展开式则在 `while` 体内写 `D id = id_2.current;`，同样是每轮新声明。两种 `for` 都能直接捕获，无需任何变通。

📘 [Dart 语言规范（For Loop / For-in 的每轮独立变量）](https://github.com/dart-lang/language/blob/main/specification/dartLangSpec.tex)

{{% /tab %}}

{{% tab header="R" %}}

R 的 `for` 不引入新作用域：循环变量就是当前环境里的一个普通变量，循环结束后还留着最后一个值。闭包直接引用它就会全部共享，按轮捕获要靠 `local()` 或工厂函数。

```r
gs <- list()
for (i in 1:3) {
  gs[[i]] <- function() i     # 直接引用 i：共享同一个 i
}
print(sapply(gs, function(f) f()))   # [1] 3 3 3
print(i)                             # [1] 3（循环变量在循环后仍然存在）

fs <- list()
for (i in 1:3) {
  fs[[i]] <- local({          # local() 里复制一份，按轮捕获
    j <- i
    function() j
  })
}
print(sapply(fs, function(f) f()))   # [1] 1 2 3
```

`gs[[i]] <- function() i` 看起来每轮都创建了函数，但函数体里的 `i` 是惰性求值、词法查找：等到调用时才去环境里找，那时 `i` 已经是 3，所以三个函数都返回 3。

修复方式是 `local({ j <- i; function() j })`：`local()` 新建一个环境并在里面复制一份 `j`，每轮一份，得到 1、2、3。R 里更惯用的写法是直接用 `lapply(1:3, function(i) function() i)`，因为函数调用本身带求值环境，每次调用都有独立的 `i`。

📘 [R Language Definition · for](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#for)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有闭包，因此也没有"闭包捕获循环变量"的问题；循环里要注册回调，就必须给每个回调准备独立的上下文，或者确认共用一份上下文正是想要的语义。语言不提供任何隐式快照。

```zig
const std = @import("std");

const Ctx = struct { value: u32 };

fn printCb(ctx: *Ctx) void {
    std.debug.print("{d} ", .{ctx.value});
}

pub fn main() void {
    var ctx = [_]Ctx{ .{ .value = 1 }, .{ .value = 2 }, .{ .value = 3 } };
    for (&ctx) |*c| {          // 每轮拿到指向不同元素的指针，天然按轮独立
        printCb(c);
    }
    std.debug.print("\n", .{});   // 1 2 3
}
```

`for (&ctx) |*c| printCb(c);` 里每轮拿到的是指向不同数组元素的指针，回调之间互不干扰，输出 `1 2 3`。如果把所有回调都指向同一个 `*Ctx`，那就是共享同一份状态——Zig 不会拦你，也不会给你隐式的"每轮快照"。

这正是 Zig 的取舍：没有闭包就没有隐式分配和隐式生命周期，代价是循环里的状态必须显式建模成数组、结构体或切片。

📘 [Zig · Documentation（for 循环与指针捕获）](https://ziglang.org/documentation/master/)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的数值与泛型 `for` 把控制变量声明为循环体的局部变量，每次迭代进入循环体都是新的局部变量，所以闭包按轮独立。Lua 5.5 起控制变量是只读的（`const`），想改只能在循环体里另建变量；`while` 里手写的计数器则完全共享。

```lua
local fns = {}
for i = 1, 3 do
  fns[i] = function() return i end   -- for 的控制变量每轮独立
end
print(fns[1](), fns[2](), fns[3]())  -- 1  2  3

local fns2 = {}
local i = 0
while i < 3 do
  i = i + 1
  fns2[i] = function() return i end   -- while 里的 i 是同一个变量
end
print(fns2[1](), fns2[2](), fns2[3]())  -- 3  3  3

-- Lua 5.5 起控制变量只读：
-- for k = 1, 3 do k = 10 end   -- 🛑 编译错误：不能给 const 控制变量赋值
```

`for i = 1, 3 do fns[i] = function() return i end end` 得到 1、2、3，因为每轮的 `i` 是新的局部变量（手册在讲闭包时给了 `local y = 0` 每轮新建的等价例子）。`while` 版本得到 3、3、3，因为 `i` 只有一份，闭包共享它。

5.5 的 `for k = 1, 3 do k = 10 end` 会直接报错：手册写明控制变量是"循环体局部的只读（`const`）变量"。需要可写副本就写 `local k = k`，这也顺带成为按轮捕获的显式写法。

📘 [Lua 5.5 · For Statement（控制变量只读）](https://www.lua.org/manual/5.5/manual.html#3.3.5)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的循环变量语义与 JavaScript 完全一致：`var` 共享、`let` 每轮新建，类型系统不会也不能阻止 `var` 的共享捕获。唯一的差别是 TS 可以在编译期标注闭包类型，配合 lint 规则能更早发现这类问题。所以这里的重点不是语义，而是"类型检查覆盖不到运行时作用域"这件事。

```typescript
const fs: Array<() => number> = [];
for (var i = 0; i < 3; i++) fs.push(() => i);
console.log("var:", fs.map((f) => f()));    // var: [ 3, 3, 3 ]

const gs: Array<() => number> = [];
for (let j = 0; j < 3; j++) gs.push(() => j);
console.log("let:", gs.map((f) => f()));    // let: [ 0, 1, 2 ]

// 两者都是合法且类型正确的 TS，区别纯粹在运行时的作用域语义
```

`for (var i = 0; i < 3; i++) fs.push(() => i);` 得到 `[3, 3, 3]`，`for (let j = 0; j < 3; j++) gs.push(() => j);` 得到 `[0, 1, 2]`。TypeScript 编译器对这两段代码都不会报错，因为类型完全一致——这正是 `var` 陷阱难查的原因。

想在编译期防住它，可以启用 `no-loop-func` 这类 ESLint 规则，或者干脆用 `forEach`/`map` 的回调参数，让每轮的值成为函数参数。TS 5.4 的闭包收窄规则在这里帮不上忙：循环变量在闭包外被 `i++` 改写，收窄本来就不会保留。

📘 [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

这是闭包最著名的坑：`var` 是函数级作用域，循环里只有一个变量，所有回调都拿到终值；`let` 在 `for` 语句的每次迭代创建一个新绑定，闭包各拿各的。IIFE 是 ES6 之前的修复手段，今天主要用于需要在一轮里锁定多个值的场景。

```javascript
const a = [];
for (var i = 0; i < 3; i++) a.push(() => i);
console.log("var:", a.map((f) => f()));        // var: [ 3, 3, 3 ]

const b = [];
for (var k = 0; k < 3; k++) b.push(((n) => () => n)(k));  // IIFE 每轮传参
console.log("iife:", b.map((f) => f()));       // iife: [ 0, 1, 2 ]

const c = [];
for (let j = 0; j < 3; j++) c.push(() => j);   // let 每轮新建绑定
console.log("let:", c.map((f) => f()));        // let: [ 0, 1, 2 ]
```

`var i` 在函数级只有一份，三个闭包共享同一个词法环境记录，所以输出 `[3, 3, 3]`；IIFE 把当轮的 `k` 作为参数传给新函数，参数是每次调用新建的绑定，得到 `[0, 1, 2]`；`let j` 靠规范直接得到 `[0, 1, 2]`。

MDN 的闭包指南把这一段单列成"Creating closures in loops: A common mistake"，并指出根因就是共享的词法环境记录。`let` 的每轮绑定对 `for`、`for-in`、`for-of` 都成立。

📘 [MDN · Closures（Creating closures in loops）](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `foreach` 默认按值遍历：每轮把元素拷进 `$v`，而箭头函数 `fn()` 又按值捕获创建时的值，所以整类陷阱基本消失。坑集中在两处：显式 `use (&$v)` 的按引用捕获，以及 `foreach ($a as &$v)` 之后忘了 `unset($v)`。

```php
<?php
$fns = [];
foreach ([1, 2, 3] as $v) {
    $fns[] = fn() => $v;      // 箭头函数按值捕获，每轮一份
}
echo implode(",", array_map(fn($f) => $f(), $fns)), "\n";   // 1,2,3

$gs = [];
foreach ([1, 2, 3] as $v) {
    $gs[] = function () use (&$v) { return $v; };   // ⚠️ use (&$v)：共享同一变量槽
}
echo implode(",", array_map(fn($f) => $f(), $gs)), "\n";    // 3,3,3

$arr = [1, 2, 3, 4];
foreach ($arr as &$v) { $v *= 2; }   // $arr 变成 [2, 4, 6, 8]，$v 仍指向 $arr[3]
foreach ($arr as $v) {}              // ⚠️ 引用还挂着：值会被逐个写回 $arr[3]
echo implode(",", $arr), "\n";       // 2,4,6,6
unset($v);                           // ✅ 官方建议：引用遍历后立刻 unset
```

第一个例子里箭头函数在每轮创建时按值捕获 `$v`，得到 `1,2,3`。第二个例子用 `use (&$v)` 按引用捕获，三个闭包共享同一个变量槽，循环结束后 `$v` 是 3，所以输出 `3,3,3`——要按轮固定就改成 `use ($v)`。

第三个例子是官方警告的复现：`foreach ($arr as &$v)` 结束后 `$v` 仍然是最后一个元素的引用，第二次 `foreach` 的每次赋值都会写回 `$arr[3]`，于是 `[2,4,6,8]` 变成 `[2,4,6,6]`，也就是手册所说的"倒数第二个值被复制到最后一个值上"。`unset($v)` 是官方推荐的收尾动作。

📘 [PHP · foreach（foreach and references）](https://www.php.net/manual/en/control-structures.foreach.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的块会创建新作用域，块参数又是每轮新建的局部变量，所以 `each`/`map` 里的闭包天然按轮捕获；而 `for` 关键字不创建新作用域，循环变量属于外层，闭包就共享最终值。官方文档明确写了"`for` 循环不像块那样创建新作用域"。

```ruby
fs = []
for i in 1..3
  fs << -> { i }          # for 不引入新作用域：三个闭包共享同一个 i
end
p fs.map(&:call)          # [3, 3, 3]

gs = []
i = 0
while i < 3
  gs << -> { i }          # while 同理
  i += 1
end
p gs.map(&:call)          # [3, 3, 3]

hs = (1..3).map { |i| -> { i } }   # 块参数是每轮新建的局部变量
p hs.map(&:call)                   # [1, 2, 3]
```

`for i in 1..3; fs << -> { i }; end` 得到 `[3, 3, 3]`：`i` 是外层局部变量，循环结束后是 3。`(1..3).map { |i| -> { i } }` 得到 `[1, 2, 3]`：块参数每轮新建，这也是官方建议用 `each`/`map` 替代 `for` 的原因之一。

要在块里避免污染外层同名变量，可以用块局部变量（参数列表里写 `|x; tmp|`）。官方文档对 `for` 的定位很明确："`for` 循环不像块那样创建新作用域"，所以在需要每轮独立绑定时，用 `each`/`map` 这类块方法比 `for` 更安全。

📘 [Ruby · Local Variable Scope（块作用域与 for）](https://docs.ruby-lang.org/en/master/syntax/assignment_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 实际用途

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 把闭包用在三处最典型：迭代器适配器、需要携带状态的缓存，以及把函数包一层的装饰器。所有迭代器适配器都是惰性的，只有遇到消费方法（`collect`、`sum`、`for_each`）才会真正执行。

```rust
use std::collections::HashMap;

fn logged<F: Fn(i32) -> i32>(f: F) -> impl Fn(i32) -> i32 {   // 装饰器：包一层
    move |x| {
        let y = f(x);
        println!("call({x}) = {y}");
        y
    }
}

fn main() {
    let v = vec![1, 2, 3, 4, 5];
    let out: Vec<i32> = v.iter().filter(|x| **x % 2 == 1).map(|x| x * 10).collect();
    println!("adapters: {out:?}");        // adapters: [10, 30, 50]

    let mut memo: HashMap<u64, u64> = HashMap::new();
    let mut sq = |x: u64| *memo.entry(x).or_insert(x * x);   // 记忆化：闭包持有缓存
    println!("memo: {} {}", sq(4), sq(4));                    // memo: 16 16

    let curried = |a: i32| move |b: i32| a + b;               // 柯里化
    let add10 = curried(10);
    println!("curried: {}", add10(5));                        // curried: 15

    let traced = logged(|x| x + 1);
    traced(41);                                               // call(41) = 42
}
```

`filter(...).map(...).collect()` 只遍历一次，也不创建中间集合，这是 Rust 里替代手写循环的默认写法；`memo` 用闭包持有 `HashMap`，同一个缓存被后续所有调用共享；`curried` 返回闭包实现柯里化；`logged` 是装饰器，泛型参数 `F: Fn(i32) -> i32` 让它在编译期单态化，没有动态派发开销。

回调与事件处理同理：把 `impl Fn` 或 `Box<dyn Fn>` 存进结构体即可；策略模式用泛型参数或 trait object 注入；延迟执行可以直接用迭代器，或者用 `Option::map`、`unwrap_or_else` 这类接受闭包的方法。

📘 [Rust Book · Closures](https://doc.rust-lang.org/book/ch13-01-closures.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的习惯是用尾随闭包把"最后一段逻辑"传进函数（`map`、`filter`、`sorted`、动画与异步 API 全是这个形状），`lazy` 视图提供惰性求值，需要缓存时再包一层返回闭包的函数。这些用法都建立在"闭包是引用类型、捕获是按变量"之上。

```swift
let nums = [1, 2, 3, 4, 5]
let odd = nums.filter { $0 % 2 == 1 }.map { $0 * 10 }
print("chain:", odd)                       // chain: [10, 30, 50]

func repeatTask(times: Int, task: () -> Void) {   // 尾随闭包
    for _ in 0..<times { task() }
}
var hits = 0
repeatTask(times: 3) { hits += 1 }
print("trailing:", hits)                   // trailing: 3

let lazySquares = nums.lazy.map { (n: Int) -> Int in
    print("compute \(n)")
    return n * n
}
print("first:", lazySquares.first!)        // compute 1
                                           // first: 1

func memoize(_ f: @escaping (Int) -> Int) -> (Int) -> Int {
    var cache: [Int: Int] = [:]
    return { x in
        if let v = cache[x] { return v }
        let v = f(x); cache[x] = v; return v
    }
}
var calls = 0
let sq = memoize { x in calls += 1; return x * x }
print("memo:", sq(4), sq(4), calls)        // memo: 16 16 1
```

`nums.filter { }.map { }` 是标准流水线，`repeatTask(times: 3) { }` 演示尾随闭包语法。`nums.lazy.map { }` 只在真正需要元素时求值，`first!` 只触发一次计算——输出里只有一行 `compute 1`。

`memoize` 用普通捕获持有 `cache` 字典，两次调用只计算一次（`calls` 是 1）。策略模式与依赖注入在 Swift 里通常是"协议 + 闭包参数"的组合：能用一个闭包表达的策略就不必先定义协议，需要多个方法时才升级成协议。

📘 [Swift · Closures（尾随闭包与 lazy）](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 里闭包的主要用途是回调（`sort.Slice`、`http.HandlerFunc`、`errgroup`）、带状态的缓存，以及用函数类型做依赖注入。标准库大量以 `func` 参数的形式要求回调，这是 Go 最"函数式"的一面。

```go
package main

import (
	"fmt"
	"sort"
)

type Handler func(string) string

func apply(h Handler, s string) string { return h(s) } // 回调

func main() {
	people := []string{"bob", "alice", "carol"}
	sort.Slice(people, func(i, j int) bool { return people[i] < people[j] })
	fmt.Println("sorted:", people) // sorted: [alice bob carol]

	fmt.Println("callback:", apply(func(s string) string { return s + "!" }, "hi")) // callback: hi!

	memo := map[int]int{}
	var fib func(int) int
	fib = func(n int) int { // 闭包 + 记忆化（递归前必须先声明变量）
		if n < 2 {
			return n
		}
		if v, ok := memo[n]; ok {
			return v
		}
		v := fib(n-1) + fib(n-2)
		memo[n] = v
		return v
	}
	fmt.Println("fib:", fib(30)) // fib: 832040
}
```

`sort.Slice(people, func(i, j int) bool { ... })` 是标准库要求传入比较闭包的典型例子，`Handler` 类型别名让回调可以像普通类型一样传递和存储。`fib` 用闭包加 `map` 做记忆化；递归引用自己时必须先写 `var fib func(int) int` 再赋值，否则闭包体里的 `fib` 还未定义。

延迟执行靠把闭包存进切片或交给 goroutine；依赖注入就是把 `func(...)` 作为构造参数传进去，Go 社区常见的"函数式选项"（`func(*Config)` 可变参数）也是这个套路。策略模式用接口或函数类型两种都能表达，只有一个方法时函数类型更轻。

📘 [Go · sort.Slice](https://pkg.go.dev/sort#Slice)

{{% /tab %}}

{{% tab header="Python" %}}

Python 里闭包最常见的四个落点是排序的 `key`、装饰器、缓存与部分应用；生成器表达式则提供不创建闭包的惰性求值。`functools` 把记忆化（`cache`）和部分应用（`partial`）都做成了标准工具。

```python
import functools

print("key:", sorted(["bb", "a", "ccc"], key=len))     # key: ['a', 'bb', 'ccc']

def trace(fn):                                          # 装饰器：闭包包住原函数
    @functools.wraps(fn)
    def wrapper(*args):
        print("call", fn.__name__)
        return fn(*args)
    return wrapper

@trace
def square(x):
    return x * x
print("decorated:", square(4))                          # call square
                                                        # decorated: 16

@functools.cache                                        # 记忆化由标准库提供
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print("fib:", fib(30))                                  # fib: 832040

add = lambda a: lambda b: a + b                         # 柯里化
print("curried:", add(1)(2))                            # curried: 3
print("gen:", sum(x * x for x in range(5)))             # gen: 30
```

`sorted(..., key=len)` 把函数当参数；`trace` 是典型装饰器，返回的 `wrapper` 闭包持有原函数 `fn`，`functools.wraps` 负责保留元数据；`@functools.cache` 用字典缓存结果，`fib(30)` 因此几乎是瞬时的；`partial` 与 `lambda a: lambda b:` 是部分应用与柯里化的两种写法。

`sum(x * x for x in range(5))` 是生成器表达式，惰性、不建中间列表——这是 Python 里"延迟执行"的默认手段，配合 `yield` 还能写成完整的生成器函数。策略模式在 Python 里就是传函数，依赖注入通常是构造参数或默认参数。

📘 [Python · functools.cache](https://docs.python.org/3/library/functools.html#functools.cache)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 把闭包包装成了两类语言设施：作用域函数（`let`、`run`、`with`、`apply`、`also`）和集合/序列的高阶函数。`Sequence` 是惰性版本，`List` 上的 `map`/`filter` 则立即求值并创建中间集合。

```kotlin
fun main() {
    val nums = listOf(1, 2, 3, 4, 5)
    println("chain: " + nums.filter { it % 2 == 1 }.map { it * 10 })   // chain: [10, 30, 50]

    val seq = nums.asSequence().map { println("compute $it"); it * it }
    println("lazy: " + seq.first())     // compute 1
                                        // lazy: 1

    val cache = mutableMapOf<Int, Int>()
    fun square(x: Int) = cache.getOrPut(x) { x * x }   // 记忆化：闭包持有缓存
    println("memo: ${square(4)} ${square(4)}")          // memo: 16 16

    fun sortBy(strategy: Comparator<String>) = listOf("bb", "a").sortedWith(strategy)
    println("strategy: " + sortBy(compareBy { it.length }))   // strategy: [a, bb]
}
```

`nums.filter { }.map { }` 是无处不在的集合处理；`nums.asSequence().map { }` 只在需要元素时求值，所以 `first()` 只打印一次 `compute 1`，这就是 Kotlin 的惰性流水线。`cache.getOrPut(x) { x * x }` 用闭包持有 `MutableMap` 做记忆化。

作用域函数的价值在于把"对某个对象的操作"写成一段闭包，并用 `this` 或 `it` 决定接收者的可见性；策略模式要么传函数、要么传 `Comparator`，依赖注入在 Kotlin 里常常就是主构造函数参数加默认值。

📘 [Kotlin · Scope functions](https://kotlinlang.org/docs/scope-functions.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的闭包主要活在 `Stream` 流水线、`Comparator`、`Runnable`/`Supplier` 等功能接口，以及事件监听器里。`Stream` 是惰性的：没有终止操作（`collect`、`forEach`、`toArray`）就不会执行。

```java
import java.util.*;
import java.util.function.*;

public class Main {
    static <T, R> Function<T, R> memoize(Function<T, R> f) {
        Map<T, R> cache = new HashMap<>();     // 闭包持有缓存
        return x -> cache.computeIfAbsent(x, f);
    }

    public static void main(String[] args) {
        List<Integer> nums = List.of(1, 2, 3, 4, 5);
        int[] out = nums.stream().filter(n -> n % 2 == 1).mapToInt(n -> n * 10).toArray();
        System.out.println("stream: " + Arrays.toString(out));    // stream: [10, 30, 50]

        Function<Integer, Integer> sq = memoize(x -> x * x);
        System.out.println("memo: " + sq.apply(4) + " " + sq.apply(4));   // memo: 16 16

        Supplier<String> lazy = () -> "computed";   // 延迟执行：需要时才求值
        System.out.println("lazy: " + lazy.get());  // lazy: computed
    }
}
```

`nums.stream().filter(...).mapToInt(...).toArray()` 是标准流水线，中间操作惰性、终止操作触发执行；`memoize` 用 `HashMap` 加 `computeIfAbsent` 让闭包持有缓存。

`Supplier` 是延迟执行的载体，`Optional.orElseGet`、日志占位、惰性初始化都靠它；策略模式在 Java 里就是"功能接口 + lambda"（`Comparator`、`Function`、`Predicate` 都是功能接口），依赖注入通常表现为构造器注入这些接口的实现。

📘 [Java · java.util.stream.Stream](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的闭包用在标准算法谓词、`std::function` 回调表，以及延迟执行（`std::async`、`std::ranges` 视图）中。STL 算法接受谓词而不是索引，这让"策略"可以直接以 lambda 传入，不必先写一个类。

```cpp
#include <algorithm>
#include <functional>
#include <iostream>
#include <iterator>
#include <map>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3, 4, 5};
    std::vector<int> out;
    std::copy_if(v.begin(), v.end(), std::back_inserter(out),
                 [](int x) { return x % 2 == 1; });              // 谓词
    std::transform(out.begin(), out.end(), out.begin(),
                   [](int x) { return x * 10; });                // 变换
    for (int x : out) std::cout << x << ' ';                     // 10 30 50
    std::cout << '\n';

    std::map<int, int> cache;
    auto sq = [&cache](int x) { return cache.try_emplace(x, x * x).first->second; };
    std::cout << "memo: " << sq(4) << ' ' << sq(4) << '\n';       // memo: 16 16

    std::function<int(int)> strategy = [](int x) { return x + 1; };   // 策略/注入
    std::cout << "strategy: " << strategy(41) << '\n';                // strategy: 42
}
```

`std::copy_if` 与 `std::transform` 分别接受一元谓词和变换函数；`sq` 用 `[&cache]` 捕获 `std::map` 做记忆化（引用捕获要求 `cache` 活得更久，这里在 `main` 里没问题）。

`std::function<int(int)>` 演示策略模式与依赖注入，代价是一次类型擦除加一次间接调用；性能敏感就把策略改成模板参数。柯里化用返回 lambda 的 lambda 表达（`auto add = [](int a) { return [a](int b) { return a + b; }; };`），比 `std::bind` 更直观。C++20 的 `std::ranges` 视图是惰性的，`views::filter`、`views::transform` 只在遍历时求值，等价于其他语言的生成器流水线。

📘 [cppreference · Algorithms（谓词）](https://en.cppreference.com/w/cpp/algorithm)

{{% /tab %}}

{{% tab header="C" %}}

C 里"闭包"只剩回调：标准库用函数指针表达回调（`qsort`、`bsearch`、`atexit`、pthread 入口），但大多数不带上下文参数，所以状态只能来自全局变量或元素自身。策略模式就是"传函数指针"，延迟执行则是把回调和参数存进结构体稍后调用。

```c
#include <stdio.h>
#include <stdlib.h>

/* C 的回调没有上下文参数：qsort 比较函数只能靠参数拿数据 */
static int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);          /* <0 / 0 / >0 三态 */
}

int main(void) {
    int v[] = {3, 1, 2};
    size_t n = sizeof v / sizeof v[0];
    qsort(v, n, sizeof v[0], cmp_int);
    for (size_t i = 0; i < n; i++) printf("%d ", v[i]);   /* 1 2 3 */
    printf("\n");
    return 0;
}
```

`qsort(v, n, sizeof v[0], cmp_int)` 是 C 最经典的高阶函数调用：比较函数必须满足"负数、零、正数"三态约定，返回 `x - y` 造成整型溢出、或者把方向写反，都是常见 bug。

要携带上下文，要么用 `qsort_r`（GNU/POSIX 扩展），要么把逻辑内联成一次性的 `static` 函数配一个全局变量（不可重入）。缓存、装饰器、柯里化在 C 里都没有语言支持，只能靠结构体手工模拟；惰性求值通常表现为"存函数指针加参数，需要时再调用"。

📘 [cppreference · qsort](https://en.cppreference.com/w/c/algorithm/qsort)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用 `do` 块把闭包写得像控制结构（`open` 的 `do` 块写法），`map`/`filter`/`reduce` 接受函数，生成器表达式提供惰性求值，点语法广播则是向量化版本。`do` 块本质上就是"把匿名函数作为第一个参数传入"。

```julia
function with_log(f)
    println("before")
    f()
end
with_log() do
    println("body")
end
# before
# body

println("map: ", map(x -> x^2, [1, 2, 3]))    # map: [1, 4, 9]
println("gen: ", sum(x^2 for x in 1:5))       # gen: 55

function memoize(f)
    cache = Dict{Any,Any}()
    x -> get!(cache, x) do
        f(x)
    end
end
sq = memoize(x -> x * x)
println("memo: ", (sq(4), sq(4)))    # memo: (16, 16)
```

`with_log() do` 块等价于把匿名函数直接传给 `with_log`，闭包捕获外层变量；官方文档提醒被捕获的变量可能带来性能问题。`map(x -> x^2, [1, 2, 3])` 与 `sum(x^2 for x in 1:5)` 是两种主流写法，后者是惰性生成器，不建中间数组。

`memoize` 用闭包持有 `Dict`，`get!(cache, x) do` 块把计算函数作为第一个参数传入。策略模式与依赖注入在 Julia 里通常表现为"把函数或类型作为参数"，多重派发让它比 OO 语言更直接；装饰器就是"接收函数、返回函数"的普通高阶函数。柯里化与部分应用没有专门语法，直接返回闭包即可（`add = a -> b -> a + b`），缓存则用上面 `memoize` 那样的闭包持有 `Dict`。

📘 [Julia · Functions（do 块语法与闭包捕获）](https://docs.julialang.org/en/v1/manual/functions/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 里闭包的主战场是 LINQ（查询语法最终编译成 lambda 与方法链）、事件处理器，以及 `Func`/`Action` 形式的策略与依赖注入。LINQ 的 `IEnumerable<T>` 版本是惰性的，`ToList()` 才立即求值。

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static Func<T, R> Memoize<T, R>(Func<T, R> f) where T : notnull
    {
        var cache = new Dictionary<T, R>();      // 闭包持有缓存
        return x => cache.TryGetValue(x, out var v) ? v : cache[x] = f(x);
    }

    static void Main()
    {
        var nums = new List<int> { 1, 2, 3, 4, 5 };
        var odd = nums.Where(n => n % 2 == 1).Select(n => n * 10);
        Console.WriteLine("linq: " + string.Join(",", odd));   // linq: 10,30,50

        var sq = Memoize((int x) => x * x);
        Console.WriteLine($"memo: {sq(4)} {sq(4)}");           // memo: 16 16

        Func<int, int> strategy = x => x + 1;                  // 策略/注入
        Console.WriteLine($"strategy: {strategy(41)}");        // strategy: 42
    }
}
```

`nums.Where(...).Select(...)` 是延迟执行的流水线：直到 `string.Join` 枚举它才真正遍历，所以把 `Where` 的结果重复枚举会重复计算。`Memoize` 返回的委托持有 `Dictionary`，实现缓存。`Func<int, int> strategy` 演示策略与依赖注入——把 `Func<T>` 注入构造器是 .NET 里很常见的做法。

柯里化用返回 lambda 的 lambda（`Func<int, Func<int, int>> add = a => b => a + b;`），延迟执行靠 `IEnumerable<T>` 的惰性与 `Func<T>`/`Lazy<T>`。事件处理要注意订阅与取消订阅配对：委托会持有订阅者（以及闭包捕获的一切），长命发布者加上短命订阅者而不注销，就是典型的泄漏。

📘 [MS Learn · LINQ（延迟执行）](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的集合方法（`map`、`where`、`fold`、`reduce`、`forEach`）都接受闭包，`Iterable` 版本是惰性的，只有 `toList()`、`first` 这类终结操作才求值。`Future`/`Stream` 的 `then`、`listen` 以及 Flutter 的 builder 回调是另一大用途。Dart 没有生成器之外的惰性语法，需要流式处理时通常靠 `Stream` 或自己返回闭包。

```dart
void main() {
  final nums = [1, 2, 3, 4, 5];
  final odd = nums.where((n) => n % 2 == 1).map((n) => n * 10).toList();
  print('chain: $odd');                        // chain: [10, 30, 50]

  final memo = <int, int>{};
  int square(int x) => memo.putIfAbsent(x, () => x * x);   // 闭包持有缓存
  print('memo: ${square(4)} ${square(4)}');     // memo: 16 16

  final strategy = (int x) => x + 1;            // 策略/注入：函数即值
  print('strategy: ${strategy(41)}');           // strategy: 42

  var total = 0;
  nums.fold<int>(0, (acc, n) => acc + n);       // reduce 家族
  total = nums.reduce((a, b) => a + b);
  print('total: $total');                       // total: 15
}
```

`nums.where(...).map(...).toList()` 是标准流水线，注意 `Iterable` 的惰性：不做 `toList()` 就不会执行。`memo.putIfAbsent(x, () => x * x)` 用闭包持有 `Map` 做记忆化，闭包只在未命中时调用。

策略模式在 Dart 里就是传函数（`Comparator`、`compareTo`）；延迟执行靠 `Future`、`Stream` 或 `late` 字段；Flutter 的 `Builder`、`ValueListenableBuilder` 都是"把构建逻辑作为闭包传入"的形态。装饰器与柯里化没有语法支持，统一用返回闭包的闭包表达（`Function curry(Function f) => (a) => (b) => f(a, b);`）。

📘 [Dart · Iterable collections](https://dart.dev/libraries/collections/iterables)

{{% /tab %}}

{{% tab header="R" %}}

R 的向量化让"迭代"通常不需要循环，`lapply`/`sapply`/`vapply`/`Map`/`Filter`/`Reduce` 构成 apply 家族；tidyverse 的 `purrr` 提供类型更稳定的版本。闭包在 R 里主要用于缓存与函数工厂。

```r
print(lapply(1:3, function(x) x^2))            # [[1]] 1 / [[2]] 4 / [[3]] 9
print(sapply(1:3, function(x) x^2))            # [1] 1 4 9
print(vapply(1:3, function(x) x^2, numeric(1)))  # [1] 1 4 9（写明返回类型）
print(Filter(function(x) x %% 2 == 1, 1:5))    # [1] 1 3 5

# purrr::map_dbl(1:3, ~ .x^2)                  # tidyverse 的等价版本

memo_square <- local({
  cache <- new.env()
  function(x) {
    key <- as.character(x)
    if (!exists(key, cache)) cache[[key]] <- x * x
    cache[[key]]
  }
})
print(c(memo_square(4), memo_square(4)))       # [1] 16 16

f <- function(a) "a 未被使用"
print(f(stop("never evaluated")))              # [1] "a 未被使用"
```

`lapply` 返回 list，`sapply` 会尝试简化结果，`vapply` 要求写明返回类型（最安全），`Filter` 与 `Reduce` 分别做筛选和折叠；`purrr::map_dbl(1:3, ~ .x^2)` 是同一思想的现代版本，公式 `~ .x` 会被转成函数。

`memo_square` 用 `local()` 把 `cache` 环境封进闭包，两次调用只算一次。柯里化与部分应用写成返回函数的函数即可（`add <- function(a) function(b) a + b`），`purrr::partial` 是现成工具；R 里也没有装饰器语法，装饰器通常写成"接收函数、返回函数"的工厂；延迟执行可以直接用惰性求值的实参，或者用 `delayedAssign` 显式创建 promise。

📘 [R · lapply](https://stat.ethz.ch/R-manual/R-devel/library/base/html/lapply.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有闭包，所以"回调"一律是"函数指针 + 上下文指针"，标准库把这种模式做成了 `std.mem.Allocator`（`ptr` 加 `vtable`）这样的显式接口。迭代用 `for`/`while` 与标准库的迭代器，没有生成器语法。

```zig
const std = @import("std");

const Ctx = struct {
    factor: i32,
    fn apply(ctx: *const Ctx, x: i32) i32 {
        return x * ctx.factor;
    }
};

fn applyAll(items: []const i32, ctx: *const Ctx,
            f: *const fn (*const Ctx, i32) i32, out: []i32) void {
    for (items, out) |x, *o| o.* = f(ctx, x);
}

pub fn main() void {
    const ctx = Ctx{ .factor = 3 };
    var items = [_]i32{ 1, 2, 3 };
    var out: [3]i32 = undefined;
    applyAll(&items, &ctx, Ctx.apply, &out);   // 回调结构体 + 函数指针
    std.debug.print("{d} {d} {d}\n", .{ out[0], out[1], out[2] });   // 3 6 9
}
```

`applyAll` 接收 `*const fn (*const Ctx, i32) i32` 加一个 `*const Ctx`，这就是 Zig 版的"带状态回调"，所有信息都在类型与参数里。策略模式同理：传不同的 `Ctx` 与函数即可，不需要语言特性；延迟执行可以先把 `Ctx` 和函数指针存进结构体，稍后再调用。

Zig 没有标准库级别的记忆化或装饰器工具，需要就自己写结构体。`std.mem.Allocator` 是"上下文加 vtable"这一模式最值得抄的范本：把一组函数指针放进 `VTable`，上下文放进 `ptr`，调用者拿到的就是一个可传递、可替换的实现。

📘 [Zig · std.mem.Allocator](https://ziglang.org/documentation/master/std/#std.mem.Allocator)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的闭包主要用于回调（事件、GUI、网络库）、自定义迭代器（泛型 `for` 的名字列表形式），以及用协程实现惰性与生成器。闭包持有 upvalue 的能力让"有状态的迭代器"写起来非常短。

```lua
-- 回调
local function each(t, f)
  for i, v in ipairs(t) do f(v, i) end
end
each({10, 20, 30}, function(v, i) print(i, v) end)   -- 1  10 / 2  20 / 3  30

-- 记忆化：闭包持有缓存表
local function memoize(f)
  local cache = {}
  return function(x)
    if cache[x] == nil then cache[x] = f(x) end
    return cache[x]
  end
end
local square = memoize(function(x) return x * x end)
print(square(4), square(4))    -- 16  16

-- 协程：惰性/延迟求值，可直接当泛型 for 的迭代器
local function gen(n)
  return coroutine.wrap(function()
    for i = 1, n do coroutine.yield(i * i) end
  end)
end
local g = gen(3)
local a = g()
local b = g()
local d = g()
print(a, b, d)    -- 1  4  9
```

`each(t, f)` 演示回调形状，表的键值对通过闭包参数传入；记忆化用闭包持有 `cache` 表，第一次调用后结果就留在表里；`coroutine.wrap` 把 `yield` 包装成可以逐个取值的函数，这是 Lua 里最常用的惰性求值手段，也可以直接把生成函数交给泛型 `for`。

策略模式就是把函数存进表里再调用（`obj.onClick`、`__index` 元方法、状态机的 `state.enter`）；延迟执行靠 `coroutine` 或把闭包排进队列。Lua 没有装饰器语法，装饰器就是"接收函数、返回新函数"的普通闭包，柯里化同理。

📘 [Lua 5.5 · Coroutines](https://www.lua.org/manual/5.5/manual.html#2.6)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的用途面与 JavaScript 相同，额外价值在于给回调、缓存和依赖注入标注类型：泛型回调能保证输入输出类型对应，装饰器有官方类型定义，函数类型的依赖注入可以在编译期抓错。下面的例子全部是可运行的标准 JavaScript，加上类型后由编译器做检查。

```typescript
function mapAll<T, R>(items: T[], f: (item: T, i: number) => R): R[] {
  return items.map(f);
}
console.log("generic:", mapAll([1, 2, 3], (n) => n * 2));   // generic: [2, 4, 6]

function memoize<T, R>(f: (x: T) => R): (x: T) => R {
  const cache = new Map<T, R>();          // 闭包持有缓存
  return (x) => {
    if (!cache.has(x)) cache.set(x, f(x));
    return cache.get(x)!;
  };
}
const sq = memoize((x: number) => x * x);
console.log("memo:", sq(4), sq(4));       // memo: 16 16

function logged<T extends unknown[], R>(fn: (...args: T) => R): (...args: T) => R {
  return (...args: T) => { console.log("call"); return fn(...args); };   // 装饰器/AOP
}
const square = logged((x: number) => x * x);
console.log("decorated:", square(4));     // call
                                          // decorated: 16
```

`mapAll<T, R>(items: T[], f: (item: T, i: number) => R)` 是泛型回调的骨架，`R` 由传入的函数推断出来；`memoize<T, R>` 让缓存键值类型跟着函数签名走，`cache.get(x)!` 的非空断言是因为前面刚 `set` 过。

装饰器（TypeScript 5.0 起的标准装饰器）本质是"接收类或方法再返回"的函数，适合做日志、计时这类 AOP；策略模式用函数类型或接口表达；惰性求值可以自己做 `thunk`（`() => T`），或者直接用生成器 `function*`。

📘 [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的闭包用法最杂：数组方法、事件处理、防抖节流、模块私有状态、记忆化、柯里化，以及函数式的依赖注入。数组方法里 `filter`/`map`/`reduce` 是即时求值，生成器 `function*` 才是惰性的。

```javascript
const nums = [1, 2, 3, 4, 5];
console.log("chain:", nums.filter((n) => n % 2).map((n) => n * 10));  // chain: [ 10, 30, 50 ]

function memoize(fn) {
  const cache = new Map();          // 闭包持有缓存：外部无法访问
  return (x) => (cache.has(x) ? cache.get(x) : (cache.set(x, fn(x)), cache.get(x)));
}
let calls = 0;
const slowSquare = memoize((x) => { calls += 1; return x * x; });
console.log("memo:", slowSquare(4), slowSquare(4), "calls:", calls);  // memo: 16 16 calls: 1

function debounce(fn, ms) {          // 延迟执行：闭包保存定时器句柄
  let timer = null;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}
console.log("debounced:", typeof debounce(() => {}, 100));  // debounced: function

const curry = (f) => (a) => (b) => f(a, b);                  // 柯里化
console.log("curried:", curry((a, b) => a + b)(1)(2));       // curried: 3
```

`nums.filter(...).map(...)` 每次都创建新数组，数据量大时要考虑改用一次 `reduce` 或生成器；`memoize` 用 `Map` 做缓存，闭包让缓存对外不可见，这就是模块私有状态；`debounce` 用闭包保存定时器句柄，是"延迟执行"在事件场景的典型形态。

装饰器在前端生态里通常表现为高阶函数（`withLogging(fn)` 返回新函数），策略模式就是把函数存进对象或参数，依赖注入在原生 JS 里就是传函数或对象——只有框架才会引入装饰器与 DI 容器。

📘 [MDN · Array.prototype.map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的闭包与箭头函数主要出现在数组函数（`array_map`、`array_filter`、`usort`、`array_reduce`）、事件与中间件回调，以及容器里的服务工厂。除了生成器，PHP 没有语言级惰性，数组函数一律立即求值。

```php
<?php
$out = array_map(fn($n) => $n * 10, array_filter([1, 2, 3, 4, 5], fn($n) => $n % 2 === 1));
echo implode(",", $out), "\n";     // 10,30,50

$words = ["bb", "a", "ccc"];
usort($words, fn($a, $b) => strlen($a) <=> strlen($b));   // 比较器
echo implode(",", $words), "\n";   // a,bb,ccc

$memo = [];
$square = function (int $x) use (&$memo): int {   // 闭包持有缓存
    return $memo[$x] ??= $x * $x;
};
echo $square(4), " ", $square(4), "\n";   // 16 16

class Sorter {                     // 策略模式 / 依赖注入
    public function __construct(private Closure $cmp) {}
    public function sort(array $a): array { usort($a, $this->cmp); return $a; }
}
echo implode(",", (new Sorter(fn($a, $b) => $b <=> $a))->sort([1, 3, 2])), "\n";   // 3,2,1
```

`array_map(fn(...), array_filter(...))` 是数组函数的常规组合；`usort` 的比较器必须返回负数、零或正数，用 `<=>` 最省事。`$square` 用 `use (&$memo)` 让闭包持有缓存，`??=` 在未命中时写入。

策略模式用 `callable` 参数或 `Closure` 属性注入（注意 `callable` 不能直接做属性类型，例子里用的是 `Closure`），中间件链是 PHP 里最常见的 AOP 形态；延迟执行可以用 `Closure` 数组，或者用生成器 `yield` 逐个产出。柯里化在 PHP 里没有语法支持，只能写成返回闭包的闭包。

📘 [PHP · array_map](https://www.php.net/manual/en/function.array-map.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的闭包以块的形式渗透进整个语言：`Enumerable` 的几十个方法、`File.open` 的资源管理、`each` 系列迭代器，以及用块实现的 DSL。`Enumerator::Lazy` 提供惰性管道，`Proc` 让块可以存下来以后再调用。

```ruby
p [1, 2, 3, 4].select(&:even?).map { |n| n * 10 }   # [20, 40]
p (1..5).each_slice(2).to_a                         # [[1, 2], [3, 4], [5]]
p (1..3).each_with_object([]) { |i, acc| acc << i * i }   # [1, 4, 9]

def memoize(fn)
  cache = {}
  ->(x) { cache.fetch(x) { cache[x] = fn.call(x) } }   # 闭包持有 cache
end
calls = 0
sq = memoize(->(x) { calls += 1; x * x })
p [sq.call(4), sq.call(4), calls]   # [16, 16, 1]

def around(fn)                      # 装饰器：接收函数、返回函数
  ->(*args) { puts "before"; fn.call(*args) }
end
p around(->(x) { x + 1 }).call(41)  # before
                                    # 42

class Sorter                        # 策略 / 依赖注入：块作为策略
  def initialize(&cmp) = @cmp = cmp
  def sort(a) = a.sort(&@cmp)
end
p Sorter.new { |a, b| b <=> a }.sort([1, 3, 2])   # [3, 2, 1]

p (1..Float::INFINITY).lazy.map { |x| x * x }.first(3)   # [1, 4, 9]
```

`select`/`map` 是 `Enumerable` 的基本用法，`each_slice`、`each_with_object` 处理分组与累积；`memoize` 返回的 lambda 持有 `cache` 哈希，两次调用只算一次；`around` 演示装饰器；`Sorter.new { |a, b| b <=> a }` 演示用块做策略注入，块被 `&` 捕获成 `Proc` 存进实例变量。

惰性求值用 `Enumerator::Lazy`：`(1..Float::INFINITY).lazy.map { }.first(3)` 在无限序列上也能工作，这是 Ruby 里处理流式数据的标准写法。柯里化用 `Proc#curry`，`add = ->(a, b) { a + b }.curry` 之后可以 `add.(1).(2)`。

📘 [Ruby · Enumerable](https://docs.ruby-lang.org/en/master/Enumerable.html)

{{% /tab %}}

{{< /tabpane >}}
