+++
title = "6.1 定义枚举"
date = 2026-08-05T08:44:00+08:00
weight = 24
type = "docs"
description = "定义枚举：变体、关联数据，以及 Option 相对空值的优势"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 定义枚举


> 原文链接: [https://doc.rust-lang.org/stable/book/ch06-01-defining-an-enum.html](https://doc.rust-lang.org/stable/book/ch06-01-defining-an-enum.html)


## 定义枚举

　　结构体提供了一种把相关字段和数据组合在一起的方式，例如带有 `width` 和 `height` 的 `Rectangle`；而枚举则让你表达：某个值是一组可能取值中的某一个。例如，我们可能想说 `Rectangle` 是一组可能形状中的一种，这组形状还包括 `Circle` 和 `Triangle`。为此，Rust 允许我们把这些可能性编码为枚举。

　　来看一个我们可能想在代码中表达的场景，并说明为何此时枚举有用、且比结构体更合适。假设我们需要处理 IP 地址。目前 IP 地址主要有两大标准：IPv4 和 IPv6。因为程序会遇到的 IP 地址只有这两种可能，我们可以*枚举*（enumerate）所有可能的变体——这也是 enumeration 一名的由来。

　　任何 IP 地址要么是 IPv4，要么是 IPv6，但不能同时是两者。IP 地址的这一性质使枚举数据结构很合适，因为枚举值只能是其变体之一。IPv4 和 IPv6 地址本质上仍都是 IP 地址，因此在处理适用于任何种类 IP 地址的场景时，应把它们视为同一类型。

　　可以在代码中通过定义 `IpAddrKind` 枚举并列出 IP 地址可能的种类 `V4` 和 `V6` 来表达这一概念。这些就是枚举的变体：

```rust
enum IpAddrKind {
    V4,
    V6,
}
```

　　`IpAddrKind` 现在是一个自定义数据类型，可以在代码的其他地方使用。

### 枚举值 {#enum-values}

　　可以像这样创建 `IpAddrKind` 两个变体各自的实例：

```rust
    let four = IpAddrKind::V4;
    let six = IpAddrKind::V6;
```

　　注意：枚举变体写在枚举名之后，用双冒号（`::`）分隔。这样很方便，因为 `IpAddrKind::V4` 和 `IpAddrKind::V6` 现在都是同一类型：`IpAddrKind`。于是我们可以定义接受任意 `IpAddrKind` 的函数：

```rust
fn route(ip_kind: IpAddrKind) {}
```

　　并且可以用任一变体调用该函数：

```rust
    route(IpAddrKind::V4);
    route(IpAddrKind::V6);
```

　　使用枚举还有更多优势。再想想我们的 IP 地址类型：目前还没有办法存储实际的 IP 地址*数据*，只知道它是哪种*类型*。既然你刚在第 5 章学过结构体，可能会想用结构体解决这个问题，如示例 6-1 所示。

```rust
    enum IpAddrKind {
        V4,
        V6,
    }

    struct IpAddr {
        kind: IpAddrKind,
        address: String,
    }

    let home = IpAddr {
        kind: IpAddrKind::V4,
        address: String::from("127.0.0.1"),
    };

    let loopback = IpAddr {
        kind: IpAddrKind::V6,
        address: String::from("::1"),
    };
```

**示例 6-1：用结构体存储 IP 地址的数据及其 `IpAddrKind` 变体**

　　这里我们定义了结构体 `IpAddr`，它有两个字段：类型为 `IpAddrKind`（先前定义的枚举）的 `kind` 字段，以及类型为 `String` 的 `address` 字段。我们有该结构体的两个实例。第一个是 `home`，其 `kind` 为 `IpAddrKind::V4`，关联地址数据为 `127.0.0.1`。第二个实例是 `loopback`，其 `kind` 为 `IpAddrKind` 的另一个变体 `V6`，关联地址为 `::1`。我们用结构体把 `kind` 和 `address` 捆在一起，于是变体就与值关联起来了。

　　不过，只用枚举表示同一概念更简洁：不必把枚举嵌在结构体里，可以直接把数据放进每个枚举变体。这个新的 `IpAddr` 枚举定义表明：`V4` 和 `V6` 变体都会带有关联的 `String` 值：

```rust
    enum IpAddr {
        V4(String),
        V6(String),
    }

    let home = IpAddr::V4(String::from("127.0.0.1"));

    let loopback = IpAddr::V6(String::from("::1"));
```

　　我们把数据直接附加到枚举的每个变体上，因此不需要额外的结构体。这里也更容易看出枚举工作方式的另一细节：我们定义的每个枚举变体名也会变成一个构造该枚举实例的函数。也就是说，`IpAddr::V4()` 是一个接受 `String` 参数并返回 `IpAddr` 类型实例的函数调用。定义枚举的结果就是自动得到这个构造函数。

　　使用枚举而非结构体还有另一个优势：每个变体可以有不同类型和数量的关联数据。IPv4 地址总是有四个数值分量，取值在 0 到 255 之间。若想把 `V4` 地址存为四个 `u8` 值，同时仍把 `V6` 地址表示为单个 `String`，用结构体就做不到。枚举轻松应对这种情况：

```rust
    enum IpAddr {
        V4(u8, u8, u8, u8),
        V6(String),
    }

    let home = IpAddr::V4(127, 0, 0, 1);

    let loopback = IpAddr::V6(String::from("::1"));
```

　　我们已经展示了几种定义数据结构以存储 IPv4 和 IPv6 地址的方式。不过，想存储 IP 地址并编码其种类其实非常常见，以至于[标准库就有我们可以使用的定义！][IpAddr]来看看标准库如何定义 `IpAddr`。它有我们定义并使用过的完全相同的枚举和变体，但把地址数据以两个不同结构体的形式嵌在变体中，且每个变体的结构体定义不同：

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

　　这段代码说明：你可以在枚举变体中放入任何种类的数据，例如字符串、数值类型或结构体。甚至还可以再包含另一个枚举！而且标准库类型往往并不比你自己可能想出的方案复杂多少。

　　注意：即便标准库包含 `IpAddr` 的定义，我们仍然可以创建并使用自己的定义而不会冲突，因为我们尚未 `use` 标准库中的那个定义。第 7 章会更多讨论如何把类型导入当前作用域。

　　再看示例 6-2 中的另一个枚举例子：它的变体中嵌入了各种各样的类型。

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

**示例 6-2：`Message` 枚举，其各变体存储不同数量和类型的值**

　　这个枚举有四个类型各异的变体：

- `Quit`：完全不关联任何数据
- `Move`：像结构体一样有命名字段
- `Write`：包含单个 `String`
- `ChangeColor`：包含三个 `i32` 值

　　定义像示例 6-2 这样带有变体的枚举，类似于定义多种不同的结构体，只是枚举不用 `struct` 关键字，且所有变体都属于 `Message` 这一种枚举类型。下面这些结构体能保存与前面枚举变体相同的数据：

```rust
struct QuitMessage; // unit struct
struct MoveMessage {
    x: i32,
    y: i32,
}
struct WriteMessage(String); // tuple struct
struct ChangeColorMessage(i32, i32, i32); // tuple struct
```

　　但若使用这些各自类型不同的结构体，就不像使用示例 6-2 中作为单一类型的 `Message` 枚举那样，容易定义接受任意这类消息的函数。

　　枚举与结构体还有一点相似：正如可以用 `impl` 在结构体上定义方法，也可以在枚举上定义方法。下面是可以在我们的 `Message` 枚举上定义的名为 `call` 的方法：

```rust
    impl Message {
        fn call(&self) {
            // method body would be defined here
        }
    }

    let m = Message::Write(String::from("hello"));
    m.call();
```

　　方法体会使用 `self` 来获取我们调用该方法时所用的值。在这个例子中，我们创建了变量 `m`，其值为 `Message::Write(String::from("hello"))`；当运行 `m.call()` 时，`call` 方法体中的 `self` 就是这个值。

　　再来看标准库中另一个非常常见且有用的枚举：`Option`。

### `Option` 枚举

　　本节以 `Option` 为案例研究——它是标准库定义的另一个枚举。`Option` 类型编码了一种非常常见的场景：某个值可能有内容，也可能什么都没有。

　　例如，若你请求非空列表的第一项，会得到一个值；若请求空列表的第一项，则什么也得不到。用类型系统表达这一概念，意味着编译器可以检查你是否处理了所有应处理的情况；这种功能能防止其他编程语言中非常常见的一类 bug。

　　人们讨论编程语言设计时常常关注包含哪些特性，但排除哪些特性同样重要。Rust 没有许多其他语言都有的空值（null）特性。*Null* 是一个表示「这里没有值」的值。在有 null 的语言中，变量总是可以处于两种状态之一：null 或非 null。

　　提出 null 引用概念的 Tony Hoare 在 2009 年的演讲「Null References: The Billion Dollar Mistake」中这样说：

> 我称之为十亿美元的错误。那时我在为面向对象语言中的引用设计第一套全面的类型系统。我的目标是确保所有对引用的使用都绝对安全，并由编译器自动完成检查。但我没能抵挡住加入空引用的诱惑，仅仅因为它太容易实现。这导致了无数错误、漏洞和系统崩溃，在过去四十年里大概造成了十亿美元的痛苦与损失。

　　空值的问题在于：若你试图把空值当非空值使用，就会得到某种错误。由于这种「空或非空」的性质无处不在，犯这类错误极其容易。

　　不过，null 试图表达的概念本身仍然有用：某个值由于某种原因当前无效或不存在。

　　问题不在于概念本身，而在于特定的实现方式。因此，Rust 没有 null，但有一个可以编码「值存在或不存在」这一概念的枚举。这个枚举就是 `Option<T>`，由[标准库定义][option]如下：

```rust
enum Option<T> {
    None,
    Some(T),
}
```

　　`Option<T>` 枚举非常有用，甚至被包含在 prelude 中；你不必显式 `use` 它。它的变体也包含在 prelude 中：可以直接使用 `Some` 和 `None`，而不必加 `Option::` 前缀。`Option<T>` 仍然只是普通枚举，`Some(T)` 和 `None` 仍然是类型 `Option<T>` 的变体。

　　`<T>` 语法是我们尚未讨论的 Rust 特性。它是泛型类型参数，第 10 章会更详细介绍泛型。眼下只需知道：`<T>` 表示 `Option` 枚举的 `Some` 变体可以保存任意类型的一块数据，并且每个用来替换 `T` 的具体类型都会使整体的 `Option<T>` 成为一个不同的类型。下面是一些用 `Option` 值保存数字类型和字符类型的例子：

```rust
    let some_number = Some(5);
    let some_char = Some('e');

    let absent_number: Option<i32> = None;
```

　　`some_number` 的类型是 `Option<i32>`。`some_char` 的类型是 `Option<char>`，这是不同的类型。Rust 能推断这些类型，因为我们在 `Some` 变体中指定了值。对于 `absent_number`，Rust 要求我们标注整体的 `Option` 类型：编译器无法仅凭一个 `None` 值推断对应的 `Some` 变体将保存什么类型。这里我们告诉 Rust，希望 `absent_number` 的类型是 `Option<i32>`。

　　当我们有 `Some` 值时，就知道存在一个值，并且该值保存在 `Some` 内部。当我们有 `None` 值时，在某种意义上它与 null 含义相同：我们没有有效值。那么，为什么有 `Option<T>` 比有 null 更好？

　　简而言之，因为 `Option<T>` 与 `T`（`T` 可以是任意类型）是不同的类型，编译器不会允许我们把 `Option<T>` 值当作一定有效的值来使用。例如，这段代码无法编译，因为它试图把 `i8` 与 `Option<i8>` 相加：

```rust
    let x: i8 = 5;
    let y: Option<i8> = Some(5);

    let sum = x + y;
```

　　若运行这段代码，会得到类似这样的错误信息：

```console
$ cargo run
   Compiling enums v0.1.0 (file:///projects/enums)
error[E0277]: cannot add `Option<i8>` to `i8`
 --> src/main.rs:5:17
  |
5 |     let sum = x + y;
  |                 ^ no implementation for `i8 + Option<i8>`
  |
  = help: the trait `Add<Option<i8>>` is not implemented for `i8`
help: the following other types implement trait `Add<Rhs>`
 --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/ops/arith.rs:98:8
  |
  = note: `i8` implements `Add`
 ::: /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/ops/arith.rs:113:0
  |
  = note: in this macro invocation
 --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/internal_macros.rs:22:8
  |
  = note: `&i8` implements `Add<i8>`
 ::: /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/internal_macros.rs:33:8
  |
  = note: `i8` implements `Add<&i8>`
 ::: /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/internal_macros.rs:44:8
  |
  = note: `&i8` implements `Add`
  = note: this error originates in the macro `add_impl` (in Nightly builds, run with -Z macro-backtrace for more info)

For more information about this error, try `rustc --explain E0277`.
error: could not compile `enums` (bin "enums") due to 1 previous error
```

　　错误信息可真长！实际上，这条错误信息意味着 Rust 不知道如何把 `i8` 和 `Option<i8>` 相加，因为它们是不同类型。当我们在 Rust 中拥有像 `i8` 这样的类型的值时，编译器会确保我们始终拥有有效值。我们可以放心继续，而不必在使用该值之前检查是否为 null。只有当我们拥有 `Option<i8>`（或我们正在处理的任意类型的 `Option`）时，才需要担心可能没有值，并且编译器会确保我们在使用该值之前处理这种情况。

　　换言之，你必须先把 `Option<T>` 转换成 `T`，才能对它执行 `T` 的操作。一般而言，这有助于抓住空值最常见的问题之一：假定某物不是 null，而实际上它是。

　　消除错误地假定非空值的风险，能让你对代码更有信心。为了拥有一个可能为空的值，你必须显式选择，把该值的类型设为 `Option<T>`。然后，在使用该值时，你被要求显式处理值为空的情况。凡是类型不是 `Option<T>` 的值，你都可以安全地假定它不是 null。这是 Rust 刻意做出的设计决策，用以限制 null 的普遍性并提高 Rust 代码的安全性。

　　那么，当你拥有类型为 `Option<T>` 的值时，如何从 `Some` 变体中取出 `T` 值以便使用呢？`Option<T>` 枚举有大量在各种情况下有用的方法；可以在[其文档][docs]中查看。熟悉 `Option<T>` 上的方法，对学习与使用 Rust 会非常有帮助。

　　一般而言，要使用 `Option<T>` 值，你会希望有分别处理每个变体的代码：希望有些代码只在拥有 `Some(T)` 值时运行，并且允许使用内部的 `T`；另一些代码只在拥有 `None` 值时运行，此时没有可用的 `T`。与枚举一起使用时，`match` 表达式正是这样一种控制流结构：它会根据枚举是哪个变体而运行不同的代码，并且这些代码可以使用匹配值内部的数据。

[IpAddr]: https://doc.rust-lang.org/std/net/enum.IpAddr.html
[option]: https://doc.rust-lang.org/std/option/enum.Option.html
[docs]: https://doc.rust-lang.org/std/option/enum.Option.html
