+++
title = "10.1 泛型数据类型"
date = 2026-08-05T08:44:00+08:00
weight = 42
type = "docs"
description = "在函数、结构体、枚举与方法中定义和使用泛型"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 泛型数据类型


> 原文链接: [https://doc.rust-lang.org/stable/book/ch10-01-syntax.html](https://doc.rust-lang.org/stable/book/ch10-01-syntax.html)


## 泛型数据类型

　　我们用泛型为函数签名或结构体等条目创建定义，然后再把它们用于许多不同的具体数据类型。先看看如何用泛型定义函数、结构体、枚举与方法，再讨论泛型对代码性能的影响。

### 在函数定义中

　　定义使用泛型的函数时，把泛型放在函数签名里通常指定参数与返回值数据类型的位置。这样代码更灵活，在避免重复的同时为调用方提供更多功能。

　　继续我们的 `largest` 函数：示例 10-4 展示了两个都在切片中找最大值的函数。我们随后把它们合并成一个使用泛型的函数。

**文件名：`src/main.rs`**
```rust
fn largest_i32(list: &[i32]) -> &i32 {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn largest_char(list: &[char]) -> &char {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest_i32(&number_list);
    println!("The largest number is {result}");

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest_char(&char_list);
    println!("The largest char is {result}");

}
```

**示例 10-4：仅名称与签名中的类型不同的两个函数**

　　`largest_i32` 就是我们在示例 10-3 中提取的、在切片中找最大 `i32` 的函数。`largest_char` 在切片中找最大的 `char`。两个函数体代码相同，因此引入泛型类型参数，合并成单个函数以消除重复。

　　要使新的单一函数中的类型参数化，需要像为函数的值参数命名那样，为类型参数命名。任何标识符都可用作类型参数名，但我们使用 `T`：按惯例，Rust 中类型参数名很短，常常只有一个字母，且类型命名惯例是 UpperCamelCase。`T` 是 *type* 的缩写，也是多数 Rust 程序员的默认选择。

　　在函数体中使用参数时，必须在签名中声明参数名，编译器才知道该名字的含义。同样，在函数签名中使用类型参数名时，也必须先声明再使用。定义泛型 `largest` 时，我们把类型名声明放在函数名与参数列表之间的尖括号 `<>` 里，像这样：

```rust
fn largest<T>(list: &[T]) -> &T {
```

　　可读作：“函数 `largest` 对某种类型 `T` 是泛型的。”该函数有一个名为 `list` 的参数，它是类型为 `T` 的值的切片。`largest` 将返回对同一类型 `T` 的值的引用。

　　示例 10-5 展示了在签名中使用泛型数据类型的合并版 `largest` 定义，以及如何用 `i32` 或 `char` 值的切片调用它。注意这段代码目前还不能编译。

**文件名：`src/main.rs`**
```rust
fn largest<T>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest(&number_list);
    println!("The largest number is {result}");

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest(&char_list);
    println!("The largest char is {result}");
}
```

**示例 10-5：使用泛型类型参数的 `largest` 函数；目前尚不能编译**

　　若现在编译，会得到如下错误：

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> src/main.rs:5:17
  |
5 |         if item > largest {
  |            ---- ^ ------- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T` with trait `PartialOrd`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++

For more information about this error, try `rustc --explain E0369`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

　　帮助文本提到了 `std::cmp::PartialOrd`，这是一个 trait，下一节会讨论 trait。眼下要知道：该错误表明 `largest` 的函数体并不能适用于 `T` 可能是的所有类型。因为我们要在函数体中比较类型 `T` 的值，所以只能使用其值可排序的类型。为支持比较，标准库提供了可在类型上实现的 `std::cmp::PartialOrd` trait（更多内容见附录 C）。要修复示例 10-5，可按帮助文本的建议，把对 `T` 有效的类型限制为仅实现了 `PartialOrd` 的那些。之后示例就能编译，因为标准库已为 `i32` 和 `char` 实现了 `PartialOrd`。

### 在结构体定义中

　　我们也可以用 `<>` 语法定义在一个或多个字段中使用泛型类型参数的结构体。示例 10-6 定义了 `Point<T>` 结构体，用于保存任意类型的 `x` 与 `y` 坐标值。

**文件名：`src/main.rs`**

```rust
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let integer = Point { x: 5, y: 10 };
    let float = Point { x: 1.0, y: 4.0 };
}
```

**示例 10-6**


　　在结构体定义中使用泛型的语法与函数定义类似。先在结构体名后紧跟的尖括号中声明类型参数名，再在结构体定义中本应写具体数据类型的地方使用该泛型类型。

　　注意：因为我们只用一个泛型类型定义了 `Point<T>`，这表示 `Point<T>` 对某种类型 `T` 是泛型的，且字段 `x` 与 `y` *都是*同一类型（无论那是什么）。若像示例 10-7 那样创建 `x` 与 `y` 类型不同的 `Point<T>` 实例，代码将无法编译。

**文件名：`src/main.rs`**
```rust
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let wont_work = Point { x: 5, y: 4.0 };
}
```

**示例 10-7：字段 `x` 与 `y` 必须是同一类型，因为二者都使用同一泛型数据类型 `T`。**

　　本例中，当我们把整数值 `5` 赋给 `x` 时，就让编译器知道：对该 `Point<T>` 实例，泛型类型 `T` 将是整数。接着为 `y` 指定 `4.0`，而我们已定义 `y` 与 `x` 类型相同，于是会得到类型不匹配错误，如下：

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0308]: mismatched types
 --> src/main.rs:7:38
  |
7 |     let wont_work = Point { x: 5, y: 4.0 };
  |                                      ^^^ expected integer, found floating-point number

For more information about this error, try `rustc --explain E0308`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

　　若要定义 `x` 与 `y` 都是泛型、但可以是不同类型的 `Point`，可以使用多个泛型类型参数。例如在示例 10-8 中，我们把 `Point` 改成对类型 `T` 与 `U` 泛型，其中 `x` 是类型 `T`，`y` 是类型 `U`。

**文件名：`src/main.rs`**

```rust
struct Point<T, U> {
    x: T,
    y: U,
}

fn main() {
    let both_integer = Point { x: 5, y: 10 };
    let both_float = Point { x: 1.0, y: 4.0 };
    let integer_and_float = Point { x: 5, y: 4.0 };
}
```

**示例 10-8**


　　现在所示的全部 `Point` 实例都合法了！定义中想用多少泛型类型参数都可以，但用太多会让代码难读。若发现需要大量泛型类型，可能意味着代码应拆成更小的部分。

### 在枚举定义中

　　与结构体一样，我们也可以定义在变体中保存泛型数据类型的枚举。再看一下第 6 章用过的、标准库提供的 `Option<T>` 枚举：

```rust
enum Option<T> {
    Some(T),
    None,
}
```

　　现在这个定义应更容易理解了。可以看出，`Option<T>` 枚举对类型 `T` 是泛型的，并有两个变体：保存一个 `T` 类型值的 `Some`，以及不保存任何值的 `None`。通过 `Option<T>`，我们可以表达“可选值”这一抽象概念；又因为 `Option<T>` 是泛型的，无论可选值是什么类型，都能使用这一抽象。

　　枚举也可以使用多个泛型类型。第 9 章用过的 `Result` 枚举的定义就是一例：

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

　　`Result` 枚举对两种类型 `T` 与 `E` 是泛型的，并有两个变体：保存类型 `T` 值的 `Ok`，以及保存类型 `E` 值的 `Err`。这一定义让我们在任何“可能成功（返回某种类型 `T` 的值）或失败（返回某种类型 `E` 的错误）”的操作中都能方便地使用 `Result`。事实上，示例 9-3 打开文件时就是这样用的：成功打开时 `T` 填成 `std::fs::File`，打开出问题时 `E` 填成 `std::io::Error`。

　　当你发现代码中有多个结构体或枚举定义仅所保存值的类型不同时，可以用泛型类型避免重复。

### 在方法定义中

　　我们可以像第 5 章那样在结构体与枚举上实现方法，并在其定义中使用泛型类型。示例 10-9 展示了示例 10-6 中定义的 `Point<T>` 结构体，以及在其上实现的名为 `x` 的方法。

**文件名：`src/main.rs`**

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

fn main() {
    let p = Point { x: 5, y: 10 };

    println!("p.x = {}", p.x());
}
```

**示例 10-9**


　　这里我们在 `Point<T>` 上定义了名为 `x` 的方法，返回对字段 `x` 中数据的引用。

　　注意：必须在 `impl` 之后声明 `T`，才能用 `T` 指明我们是在类型 `Point<T>` 上实现方法。通过在 `impl` 后声明 `T` 为泛型类型，Rust 就能识别 `Point` 尖括号中的类型是泛型类型而非具体类型。我们本可以为该泛型参数选用与结构体定义中不同的名字，但使用相同名字是惯例。若在声明了泛型类型的 `impl` 中编写方法，该方法会定义在该类型的任何实例上，无论最终用什么具体类型替换泛型类型。

　　定义方法时也可以对泛型类型施加约束。例如，我们可以只在 `Point<f32>` 实例上实现方法，而不是在任意泛型类型的 `Point<T>` 上。示例 10-10 使用具体类型 `f32`，意味着我们不在 `impl` 后声明任何类型。

**文件名：`src/main.rs`**
```rust
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

**示例 10-10：仅适用于泛型类型参数 `T` 为某一具体类型的结构体的 `impl` 块**

　　这意味着类型 `Point<f32>` 会有 `distance_from_origin` 方法；其他 `T` 不是 `f32` 的 `Point<T>` 实例则不会定义该方法。该方法测量点到坐标 (0.0, 0.0) 的距离，并使用仅对浮点类型可用的数学运算。

　　结构体定义中的泛型类型参数未必总与同一结构体方法签名中使用的相同。示例 10-11 为 `Point` 结构体使用泛型类型 `X1` 与 `Y1`，为 `mixup` 方法签名使用 `X2` 与 `Y2`，以便示例更清晰。该方法用 `self` 这个 `Point`（类型 `X1`）的 `x` 值，以及传入的 `Point`（类型 `Y2`）的 `y` 值，创建一个新的 `Point` 实例。

**文件名：`src/main.rs`**
```rust
struct Point<X1, Y1> {
    x: X1,
    y: Y1,
}

impl<X1, Y1> Point<X1, Y1> {
    fn mixup<X2, Y2>(self, other: Point<X2, Y2>) -> Point<X1, Y2> {
        Point {
            x: self.x,
            y: other.y,
        }
    }
}

fn main() {
    let p1 = Point { x: 5, y: 10.4 };
    let p2 = Point { x: "Hello", y: 'c' };

    let p3 = p1.mixup(p2);

    println!("p3.x = {}, p3.y = {}", p3.x, p3.y);
}
```

**示例 10-11：使用与结构体定义不同的泛型类型的方法**

　　在 `main` 中，我们定义了一个 `x` 为 `i32`（值为 `5`）、`y` 为 `f64`（值为 `10.4`）的 `Point`。变量 `p2` 是一个 `x` 为字符串切片（值 `"Hello"`）、`y` 为 `char`（值 `c`）的 `Point`。对 `p1` 以参数 `p2` 调用 `mixup` 得到 `p3`：`p3` 的 `x` 是 `i32`，因为来自 `p1`；`y` 是 `char`，因为来自 `p2`。`println!` 宏会打印 `p3.x = 5, p3.y = c`。

　　本例的目的是演示：有些泛型参数在 `impl` 后声明，有些在方法定义中声明。这里 `X1` 与 `Y1` 在 `impl` 后声明，因为它们属于结构体定义；`X2` 与 `Y2` 在 `fn mixup` 后声明，因为它们只与该方法相关。

### 使用泛型的代码性能 {#performance-of-code-using-generics}

　　你可能想知道：使用泛型类型参数是否有运行时开销？好消息是：使用泛型类型不会让程序比使用具体类型跑得更慢。

　　Rust 通过在编译时对使用泛型的代码执行单态化（monomorphization）来做到这一点。*单态化*是把泛型代码变成具体代码的过程：在编译时填入实际使用的具体类型。在此过程中，编译器做的事与我们创建示例 10-5 中泛型函数时的步骤相反：它查看所有调用泛型代码的地方，并为所调用的具体类型生成代码。

　　我们用标准库的泛型 `Option<T>` 枚举看看这如何工作：

```rust
let integer = Some(5);
let float = Some(5.0);
```

　　Rust 编译这段代码时会执行单态化。过程中，编译器读取在 `Option<T>` 实例中用过的值，识别出两种 `Option<T>`：一种是 `i32`，另一种是 `f64`。于是它把 `Option<T>` 的泛型定义展开为分别特化于 `i32` 与 `f64` 的两个定义，从而用具体定义替换泛型定义。

　　单态化后的代码看起来类似下面这样（编译器实际使用的名字与这里为说明而用的不同）：

**文件名：`src/main.rs`**
```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

　　泛型的 `Option<T>` 被编译器创建的具体定义替换了。因为 Rust 把泛型代码编译成每个实例都指定了类型的代码，所以使用泛型没有运行时开销。代码运行时，表现就如同我们手工复制了每个定义一样。单态化过程使 Rust 的泛型在运行时极为高效。
