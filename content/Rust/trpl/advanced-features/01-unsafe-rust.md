+++
title = "20.1 不安全的 Rust"
date = 2026-08-05T08:44:00+08:00
weight = 95
type = "docs"
description = "目前为止讨论过的代码都有 Rust 在编译时会强制执行的内存安全保证。然而，Rust 还隐藏有第二种语言，它不会强制执行这类内存安全保证：这被称为不安全 Rust，它与常规 Rust 代码无异，但提供了额外的超能力。"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 不安全的 Rust {#rust}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch20-01-unsafe-rust.html](https://doc.rust-lang.org/stable/book/ch20-01-unsafe-rust.html)


## 不安全 Rust

　　目前为止讨论过的代码都有 Rust 在编译时会强制执行的内存安全保证。然而，Rust 还隐藏有第二种语言，它不会强制执行这类内存安全保证：这被称为 **不安全 Rust**（*unsafe Rust*）。它与常规 Rust 代码无异，但是会提供额外的超能力。

　　不安全 Rust 之所以存在，是因为静态分析本质上是保守的。当编译器尝试确定一段代码是否支持某个保证时，拒绝一些合法的程序比接受无效的程序要好一些。这必然意味着有时代码**可能**是合法的，但如果 Rust 编译器没有足够的信息来确定，它将拒绝该代码。在这种情况下，可以使用不安全代码告诉编译器，“相信我，我知道自己在干什么。” 不过千万注意，使用不安全 Rust 风险自担：如果不安全代码出错了，比如解引用空指针，可能会导致不安全的内存使用。

　　另一个 Rust 存在不安全一面的原因是底层计算机硬件固有的不安全性。如果 Rust 不允许进行不安全操作，那么有些任务则根本完成不了。Rust 需要能够进行像直接与操作系统交互甚至于编写你自己的操作系统这样的底层系统编程。底层系统编程也是 Rust 语言的目标之一。让我们看看不安全 Rust 能做什么，和怎么做。

### 执行不安全的超能力

　　要切换到不安全 Rust，使用 `unsafe` 关键字，然后开启一个包含不安全代码的新块。在不安全 Rust 中可以完成五类在安全 Rust 中做不到的操作，我们称之为**不安全超能力**（*unsafe superpowers*）。这些超能力包括：

1. 解引用裸指针
2. 调用不安全的函数或方法
3. 访问或修改可变静态变量
4. 实现不安全 trait
5. 访问 `union` 的字段

　　重要的是要明白：`unsafe` 并不会关闭借用检查器，也不会禁用 Rust 的其它安全检查——若在不安全代码中使用引用，引用仍会被检查。`unsafe` 关键字只是让你能使用这五类功能，而编译器不会再为它们检查内存安全。在不安全块内部，你仍然能得到一定程度的安全。

　　此外，`unsafe` 并不意味着块中的代码一定危险，或必然存在内存安全问题：其意图是由你作为程序员，确保 `unsafe` 块中的代码以有效的方式访问内存。

　　人难免会犯错，但要求这五类不安全操作必须放在标有 `unsafe` 的块中，就能知道任何与内存安全相关的错误都必定位于某个 `unsafe` 块内。请尽量把 `unsafe` 块写得小一些；日后排查内存 bug 时你会感谢自己。

　　为了尽可能隔离不安全代码，最好把它封装在安全抽象里并提供安全 API——本章稍后讨论不安全函数与方法时会谈到。标准库的一部分就是在经过审查的不安全代码之上实现的安全抽象。把不安全代码包在安全抽象里，可以避免 `unsafe` 泄漏到所有你或用户想使用该功能的地方，因为使用安全抽象本身是安全的。

　　让我们依次看看这五类不安全超能力，也会看到一些为不安全代码提供安全接口的抽象。

### 解引用裸指针

　　回到第四章的 [「悬垂引用」][dangling-references] 一节，那里提到了编译器会确保引用总是有效的。不安全 Rust 有两个被称为 **裸指针**（*raw pointers*）的类似于引用的新类型。和引用一样，裸指针是不可变或可变的，分别写作 `*const T` 和 `*mut T`。这里的星号不是解引用运算符；它是类型名称的一部分。在裸指针的上下文中，**不可变** 意味着指针解引用之后不能直接赋值。

　　裸指针与引用和智能指针的区别在于

* 允许忽略借用规则，可以同时拥有不可变和可变的指针，或多个指向相同位置的可变指针
* 不保证指向有效的内存
* 允许为空
* 不能实现任何自动清理功能

　　通过去掉 Rust 强加的保证，你可以放弃安全保证以换取性能或使用另一个语言或硬件接口的能力，此时 Rust 的保证并不适用。

　　示例 20-1 展示了如何创建一个不可变裸指针和一个可变裸指针。

```rust
    let mut num = 5;

    let r1 = &raw const num;
    let r2 = &raw mut num;
```

**示例 20-1：使用裸指针借用运算符创建裸指针**

　　注意这段代码中没有引入 `unsafe` 关键字。可以在安全代码中创建裸指针；只是不能在不安全块之外解引用裸指针，稍后便会看到。

　　我们通过使用裸指针借用操作符（*raw borrow operators*）创建裸指针：`&raw const num` 会创建一个 `*const i32` 的不可变裸指针。由于我们是直接从一个局部变量创建它们的，因此可以确定这些特定的裸指针是有效的，但是不能对任何裸指针都做出如此假设。

　　为了演示这一点，接下来我们将创建一个有效性无法确定的裸指针，使用 `as` 进行类型转换而不是使用裸指针借用操作符。示例 20-2 展示了如何创建一个指向任意内存地址的裸指针。尝试使用任意内存是未定义行为：此地址可能有数据也可能没有，编译器可能会优化掉这个内存访问，或者程序可能因段错误（segmentation fault）而终止。通常在有裸指针借用操作符可用的情况下，没有充分的理由编写这样的代码，但这确实是可行的。

```rust
    let address = 0x012345usize;
    let r = address as *const i32;
```

**示例 20-2：创建指向任意内存地址的裸指针**

　　记得我们说过可以在安全代码中创建裸指针，但不能 **解引用** 裸指针和读取其指向的数据。示例 20-3 中，我们在裸指针上使用了解引用运算符 `*`，该操作需要一个 `unsafe` 块：

```rust
    let mut num = 5;

    let r1 = &raw const num;
    let r2 = &raw mut num;

    unsafe {
        println!("r1 is: {}", *r1);
        println!("r2 is: {}", *r2);
    }
```

**示例 20-3：在 `unsafe` 块中解引用裸指针**

　　创建一个指针不会造成任何危害；只有当访问其指向的值时才有可能遇到无效的值。

　　还需注意示例 20-1 和 20-3 中创建了同时指向相同内存位置 `num` 的裸指针 `*const i32` 和 `*mut i32`。相反如果尝试同时创建 `num` 的不可变和可变引用，代码将无法通过编译，因为 Rust 的所有权规则不允许在拥有任何不可变引用的同时再创建可变引用。通过裸指针，就能够同时创建同一地址的可变指针和不可变指针，若通过可变指针修改数据，则可能造成潜在数据竞争。请多加小心！

　　既然存在这么多的危险，为何还要使用裸指针呢？一个主要的应用场景便是调用 C 代码接口，这在下一部分 [「调用不安全函数或方法」](#调用不安全函数或方法) 中会讲到。另一个场景是构建借用检查器无法理解的安全抽象。让我们先介绍不安全函数，接着看一看使用不安全代码的安全抽象的示例。

### 调用不安全函数或方法

　　第二类可以在不安全块中进行的操作是调用不安全函数。不安全函数和方法与常规函数方法十分类似，除了其开头有一个额外的 `unsafe`。在此上下文中，关键字 `unsafe` 表示该函数具有调用时需要满足的要求，而 Rust 不会保证满足这些要求。通过在 `unsafe` 块中调用不安全函数，表明我们已经阅读过此函数的文档并对其是否满足函数自身的契约负责。

　　如下是一个没有做任何操作的不安全函数 `dangerous` 的例子：

```rust
    unsafe fn dangerous() {}

    unsafe {
        dangerous();
    }
```

　　必须在一个单独的 `unsafe` 块中调用 `dangerous` 函数。如果尝试不使用 `unsafe` 块调用 `dangerous`，则会得到一个错误：

```console
$ cargo run
   Compiling unsafe-example v0.1.0 (file:///projects/unsafe-example)
error[E0133]: call to unsafe function `dangerous` is unsafe and requires unsafe block
 --> src/main.rs:4:5
  |
4 |     dangerous();
  |     ^^^^^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined behavior

For more information about this error, try `rustc --explain E0133`.
error: could not compile `unsafe-example` (bin "unsafe-example") due to 1 previous error
```

　　通过 `unsafe` 块，我们向 Rust 断言我们已经阅读过函数的文档，理解如何正确使用它，并核实我们履行了该函数的契约。

　　在不安全函数的函数体内部执行不安全操作时，同样需要使用 `unsafe` 块，就像在普通函数中一样，如果忘记了，编译器会发出警告。这有助于将 `unsafe` 块保持得尽可能小，因为不安全操作未必需要覆盖整个函数体。

#### 创建不安全代码的安全抽象

　　仅仅因为函数包含不安全代码并不意味着整个函数都需要标记为不安全的。事实上，将不安全代码封装进安全函数是一种常见的抽象方式。作为一个例子，了解一下标准库中的函数 `split_at_mut`，它需要一些不安全代码，让我们探索可以如何实现它。这个安全函数定义于可变切片之上：它获取一个切片并从给定的索引参数开始将其分割为两个切片。示例 20-4 展示了如何使用 `split_at_mut`。

```rust
    let mut v = vec![1, 2, 3, 4, 5, 6];

    let r = &mut v[..];

    let (a, b) = r.split_at_mut(3);

    assert_eq!(a, &mut [1, 2, 3]);
    assert_eq!(b, &mut [4, 5, 6]);
```

**示例 20-4：使用安全的 `split_at_mut` 函数**

　　这个函数无法只通过安全 Rust 实现。一个尝试可能看起来像示例 20-5，它不能编译。出于简单考虑，我们将 `split_at_mut` 实现为函数而不是方法，并只处理 `i32` 值而非泛型 `T` 的切片。

```rust
fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = values.len();

    assert!(mid <= len);

    (&mut values[..mid], &mut values[mid..])
}
```

**示例 20-5：尝试只使用安全 Rust 来实现 `split_at_mut`**

　　此函数首先获取切片的长度，然后通过检查参数是否小于或等于这个长度来断言参数所给定的索引位于切片当中。该断言意味着如果传入的索引比要分割的切片的索引更大，此函数在尝试使用这个索引前 panic。

　　之后我们在一个元组中返回两个可变的切片：一个从原始切片的开头直到 `mid` 索引，另一个从 `mid` 直到原切片的结尾。

　　如果尝试编译示例 20-5 的代码，会得到一个错误：

```console
$ cargo run
   Compiling unsafe-example v0.1.0 (file:///projects/unsafe-example)
error[E0499]: cannot borrow `*values` as mutable more than once at a time
 --> src/main.rs:6:31
  |
1 | fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
  |                         - let's call the lifetime of this reference `'1`
...
6 |     (&mut values[..mid], &mut values[mid..])
  |     --------------------------^^^^^^--------
  |     |     |                   |
  |     |     |                   second mutable borrow occurs here
  |     |     first mutable borrow occurs here
  |     returning this value requires that `*values` is borrowed for `'1`
  |
  = help: use `.split_at_mut(position)` to obtain two mutable non-overlapping sub-slices

For more information about this error, try `rustc --explain E0499`.
error: could not compile `unsafe-example` (bin "unsafe-example") due to 1 previous error
```

　　Rust 的借用检查器无法理解我们要借用这个切片的两个不同部分：它只知道我们借用了同一个切片两次。本质上借用切片的不同部分是可以的，因为这两段切片不会重叠，不过 Rust 还没有智能到能够理解这些。当我们知道某些事是可以的而 Rust 不知道时，就需要使用不安全代码了。

　　示例 20-6 展示了如何使用 `unsafe` 块，裸指针和一些不安全函数调用来实现 `split_at_mut`：

```rust
use std::slice;

fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = values.len();
    let ptr = values.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (
            slice::from_raw_parts_mut(ptr, mid),
            slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}
```

**示例 20-6：在 `split_at_mut` 函数的实现中使用不安全代码**

　　回忆第 4 章[「Slice 类型」][the-slice-type]一节：切片（slice）是一个指向一些数据的指针，并带有该切片的长度。可以使用 `len` 方法获取切片的长度，使用 `as_mut_ptr` 方法访问切片的裸指针。在这个例子中，因为有一个 `i32` 值的可变切片，`as_mut_ptr` 返回一个 `*mut i32` 类型的裸指针，并将其存储在 `ptr` 变量中。

　　我们保持索引 `mid` 位于切片中的断言。接着是不安全代码：`slice::from_raw_parts_mut` 函数获取一个裸指针和一个长度来创建一个切片。这里使用此函数从 `ptr` 中创建了一个有 `mid` 个项的切片。之后在 `ptr` 上调用 `add` 方法并使用 `mid` 作为参数来获取一个从 `mid` 开始的裸指针，使用这个裸指针并以 `mid` 之后项的数量为长度创建另一个切片。

　　`slice::from_raw_parts_mut` 函数是不安全的因为它获取一个裸指针，并必须确信这个指针是有效的。裸指针上的 `add` 方法也是不安全的，因为其必须确信此地址偏移量也是有效的指针。因此必须将 `slice::from_raw_parts_mut` 和 `add` 放入 `unsafe` 块中以便能调用它们。通过观察代码，和增加 `mid` 必然小于等于 `len` 的断言，我们可以说 `unsafe` 块中所有的裸指针将是有效的切片中数据的指针。这是一个可以接受的 `unsafe` 的恰当用法。

　　注意无需将 `split_at_mut` 函数的结果标记为 `unsafe`，并可以在安全 Rust 中调用此函数。我们创建了一个不安全代码的安全抽象，其代码以一种安全的方式使用了 `unsafe` 代码，因为其只从这个函数访问的数据中创建了有效的指针。

　　与此相对，示例 20-7 中的 `slice::from_raw_parts_mut` 在使用切片时很有可能会崩溃。这段代码获取任意内存地址并创建了一个长度为一万的切片：

```rust
    use std::slice;

    let address = 0x01234usize;
    let r = address as *mut i32;

    let values: &[i32] = unsafe { slice::from_raw_parts_mut(r, 10000) };
```

**示例 20-7：通过任意内存地址创建切片**

　　我们并不拥有这个任意地址的内存，也不能保证这段代码创建的切片包含有效的 `i32` 值。试图使用臆测为有效的 `values` 会导致未定义的行为。

#### 使用 `extern` 函数调用外部代码

　　有时你的 Rust 代码可能需要与其他语言编写的代码交互。为此 Rust 有一个关键字，`extern`，有助于创建和使用 **外部函数接口**（*Foreign Function Interface*，FFI）。外部函数接口是一个编程语言用以定义函数的方式，其允许不同（外部）编程语言调用这些函数。

　　示例 20-8 展示了如何集成 C 标准库中的 `abs` 函数。`extern` 块中声明的函数在 Rust 代码中通常是不安全的因此 `extern` 块本身也必须标注 `unsafe`。之所以如此，是因为其他语言不会强制执行 Rust 的规则，Rust 也无法检查这些约束，因此程序员有责任确保调用的安全性。

**文件名：`src/main.rs`**
```rust
unsafe extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
    }
}
```

**示例 20-8：声明并调用另一个语言中定义的 `extern` 函数**

　　在 `unsafe extern "C"` 块中，我们列出了希望能够调用的另一个语言中的外部函数的签名和名称。`"C"` 部分定义了外部函数所使用的 **应用二进制接口**（*application binary interface*，ABI） —— ABI 定义了如何在汇编语言层面调用此函数。`"C"` ABI 是最常见的，并遵循 C 编程语言的 ABI。有关 Rust 支持的所有 ABI 的信息请参见 [Rust 参考手册][ABI]。

　　`unsafe extern` 中声明的任何项都隐式地是 `unsafe` 的。然而，一些 FFI 函数**可以**安全地调用。例如，C 标准库中的 `abs` 函数没有任何内存安全方面的考量并且我们知道它可以使用任何 `i32` 调用。在类似这样的例子中，我们可以使用 `safe` 关键字来表明这个特定的函数即便是在 `unsafe extern` 块中也是可以安全调用的。一旦我们做出这个修改，调用它不再需要 `unsafe` 块，如示例 20-9 所示。

**文件名：`src/main.rs`**
```rust
unsafe extern "C" {
    safe fn abs(input: i32) -> i32;
}

fn main() {
    println!("Absolute value of -3 according to C: {}", abs(-3));
}
```

**示例 20-9：在 `unsafe extern` 块中显式地标记一个函数为 `safe` 并安全地调用它**

　　将一个函数标记为 `safe` 并不会固有地使其变得安全！相反，这像是一个对 Rust 的承诺表明它**是**安全的。确保履行这个承诺仍然是你的责任！

#### 从其它语言调用 Rust 函数

　　也可以使用 `extern` 来创建一个允许其它语言调用 Rust 函数的接口。不同于创建整个 `extern` 块，就在相关函数的 `fn` 关键字之前加上 `extern` 关键字并指定所用 ABI。还需增加 `#[unsafe(no_mangle)]` 注解，告诉 Rust 编译器不要对此函数名做名称修饰（*mangling*）。名称修饰是指编译器把我们起的函数名改成带有更多编译过程信息、但更不易读的名字。每种语言的编译器修饰方式略有不同，因此若要让其它语言能按名字找到这个 Rust 函数，就必须禁用 Rust 的名称修饰。这样做是不安全的，因为没有内置修饰时，跨库可能发生名字冲突，所以我们必须保证所选名称在不做修饰的情况下也能安全导出。

　　在如下的例子中，一旦其编译为动态库并从 C 语言中链接，`call_from_c` 函数就能够在 C 代码中访问：

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

　　这种 `extern` 用法只在属性中需要 `unsafe`，而不需要在 `extern` 块本身使用 `unsafe`。

### 访问或修改可变静态变量

　　在本书中，我们尚未讨论过 **全局变量**（*global variables*），Rust 确实支持它们，不过这对于 Rust 的所有权规则来说是有问题的。如果有两个线程访问相同的可变全局变量，则可能会造成数据竞争。

　　全局变量在 Rust 中被称为 **静态**（*static*）变量。示例 20-10 展示了一个拥有字符串切片值的静态变量的声明和使用：

**文件名：`src/main.rs`**
```rust
static HELLO_WORLD: &str = "Hello, world!";

fn main() {
    println!("value is: {HELLO_WORLD}");
}
```

**示例 20-10：定义和使用一个不可变静态变量**

　　静态（`static`）变量类似于第三章 [「常量」][constants] 一节讨论的常量。通常静态变量的名称采用 `SCREAMING_SNAKE_CASE` 写法。静态变量只能储存拥有 `'static` 生命周期的引用，这意味着 Rust 编译器可以自己计算出其生命周期而无需显式标注。访问不可变静态变量是安全的。

　　常量与不可变静态变量的一个微妙的区别是静态变量中的值有一个固定的内存地址。使用这个值总是会访问相同的地址。另一方面，常量则允许在任何被用到的时候复制其数据。另一个区别在于静态变量可以是可变的。访问和修改可变静态变量都是 **不安全** 的。示例 20-11 展示了如何声明、访问和修改名为 `COUNTER` 的可变静态变量：

**文件名：`src/main.rs`**
```rust
static mut COUNTER: u32 = 0;

/// SAFETY: Calling this from more than a single thread at a time is undefined
/// behavior, so you *must* guarantee you only call it from a single thread at
/// a time.
unsafe fn add_to_count(inc: u32) {
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    unsafe {
        // SAFETY: This is only called from a single thread in `main`.
        add_to_count(3);
        println!("COUNTER: {}", *(&raw const COUNTER));
    }
}
```

**示例 20-11：读取或修改一个可变静态变量是不安全的**

　　就像常规变量一样，我们使用 `mut` 关键字来指定可变性。任何读写 `COUNTER` 的代码都必须位于 `unsafe` 块中。这段代码可以编译并如期打印出 `COUNTER: 3`，因为这是单线程的。拥有多个线程访问 `COUNTER` 则可能导致数据竞争，所以这是未定义行为。因此，我们需要将整个函数标记为 `unsafe`，并在文档注释中说明其安全性限制，以便调用者明确哪些操作是安全的、哪些是不安全的。

　　每当我们编写一个不安全函数，惯常做法是编写一个以 `SAFETY` 开头的注释并解释调用者需要做什么才可以安全地调用该方法。同理，当我们进行不安全操作时，惯常做法是编写一个以 `SAFETY` 开头并解释安全性规则是如何维护的。

　　另外，编译器默认会通过一条 lint 拒绝任何创建可变静态变量引用的尝试。你要么显式添加 `#[allow(static_mut_refs)]` 来关闭该 lint 的保护，要么用裸指针借用运算符创建裸指针再访问可变静态变量。这也包括引用被隐式创建的情况，例如本示例中 `println!` 里用到的情形。要求通过裸指针来创建可变静态变量的引用，有助于让使用它们时的安全要求更加显眼。

　　拥有可以全局访问的可变数据，难以保证不存在数据竞争，这就是为何 Rust 认为可变静态变量是不安全的。在任何可能的情况下，请优先使用第十六章讨论的并发技术和线程安全智能指针，这样编译器就能检测不同线程间的数据访问是否是安全的。

### 实现不安全 trait

　　我们可以使用 `unsafe` 来实现一个不安全 trait。当 trait 中至少有一个方法中包含编译器无法验证的不变式（invariant）时该 trait 就是不安全的。可以在 `trait` 之前增加 `unsafe` 关键字将 trait 声明为 `unsafe`，同时 trait 的实现也必须标记为 `unsafe`，如示例 20-12 所示：

```rust
unsafe trait Foo {
    // methods go here
}

unsafe impl Foo for i32 {
    // method implementations go here
}
```

**示例 20-12：定义并实现不安全 trait**

　　通过 `unsafe impl`，我们承诺将保证编译器所不能验证的不变式。

　　作为一个例子，回忆第十六章 [「使用 `Sync` 和 `Send` trait 的可扩展并发」][send-and-sync] 一节中的 `Sync` 和 `Send` 标记 trait：如果我们的类型完全由实现了 `Send` 与 `Sync` 的其他类型组成，编译器会自动为其实现这些 trait。如果我们定义的类型包含某些未实现 `Send` 或 `Sync` 的类型，例如裸指针，但又想将该类型标记为 `Send` 或 `Sync`，就必须使用 `unsafe`。Rust 不能验证我们的类型保证可以安全地跨线程发送或在多线程间访问，所以需要我们自己进行检查，并通过 `unsafe` 表明这一点。

### 访问联合体中的字段

　　最后一个只能在 `unsafe` 块中执行的操作是访问（union）中的字段。`union` 和 `struct` 类似，但是在一个实例中同时只能使用一个已声明的字段。联合体主要用于和 C 代码中的联合体进行交互。访问联合体的字段是不安全的，因为 Rust 无法保证当前存储在联合体实例中数据的类型。可以查看 [Rust 参考手册][unions] 了解有关联合体的更多信息。

### 使用 Miri 检查不安全代码

　　当编写不安全代码时，你可能会想要检查编写的代码是否真的安全正确。最好的方式之一是使用 Miri，一个用来检测未定义行为的 Rust 官方工具。鉴于借用检查器是一个在编译时工作的**静态**工具，Miri 是一个在运行时工作的**动态**工具。它通过运行程序，或者测试集来检查代码，并检测你是否违反了它理解的 Rust 应该如何工作的规则。

　　使用 Miri 需要 nightly 版 Rust（我们在[附录 G：Rust 是如何开发的与 “Nightly Rust”][nightly]中有更多讨论）。可以输入 `rustup +nightly component add miri` 同时安装 nightly Rust 与 Miri。这不会改变项目当前使用的 Rust 版本；它只是把工具加到系统上，以便需要时使用。可以在项目中运行 `cargo +nightly miri run` 或 `cargo +nightly miri test`。

　　举个它能帮上大忙的例子：看看对示例 20-7 运行 Miri 会发生什么。

```console
$ cargo +nightly miri run
   Compiling unsafe-example v0.1.0 (file:///projects/unsafe-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.17s
     Running `file:///home/.rustup/toolchains/nightly/bin/cargo-miri runner target/miri/debug/unsafe-example`
warning: integer-to-pointer cast
 --> src/main.rs:5:13
  |
5 |     let r = address as *mut i32;
  |             ^^^^^^^^^^^^^^^^^^^ integer-to-pointer cast
  |
  = help: this program is using integer-to-pointer casts or (equivalently) `ptr::with_exposed_provenance`, which means that Miri might miss pointer bugs in this program
  = help: see https://doc.rust-lang.org/nightly/std/ptr/fn.with_exposed_provenance.html for more details on that operation
  = help: to ensure that Miri does not miss bugs in your program, use Strict Provenance APIs (https://doc.rust-lang.org/nightly/std/ptr/index.html#strict-provenance, https://crates.io/crates/sptr) instead
  = help: you can then set `MIRIFLAGS=-Zmiri-strict-provenance` to ensure you are not relying on `with_exposed_provenance` semantics
  = help: alternatively, `MIRIFLAGS=-Zmiri-permissive-provenance` disables this warning

error: Undefined Behavior: constructing invalid value of type &mut [i32]: encountered a dangling reference (0x1234[noalloc] has no provenance)
 --> src/main.rs:7:35
  |
7 |     let values: &[i32] = unsafe { slice::from_raw_parts_mut(r, 10000) };
  |                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Undefined Behavior occurred here
  |
  = help: this indicates a bug in the program: it performed an invalid operation, and caused Undefined Behavior
  = help: see https://doc.rust-lang.org/nightly/reference/behavior-considered-undefined.html for further information

note: some details are omitted, run with `MIRIFLAGS=-Zmiri-backtrace=full` for a verbose backtrace

error: aborting due to 1 previous error; 1 warning emitted
```

　　Miri 正确地警告我们：正在把整数转换成指针，这可能有问题；但 Miri 无法判定是否一定有问题，因为它不知道指针最初是如何产生的。随后，Miri 又在示例 20-7 存在未定义行为之处报错——因为这里有一个悬垂指针。多亏了 Miri，我们现在知道存在未定义行为的风险，就可以思考如何让代码变得安全。在某些情况下，Miri 甚至还能给出如何修复错误的建议。

　　Miri 并不能抓住编写不安全代码时可能犯的所有错误。它是动态分析工具，因此只抓实际会跑到的代码中的问题。这意味着需要把它和良好的测试手段结合起来，才能更有信心。Miri 也无法覆盖代码所有可能不健全的路径。

　　换句话说：如果 Miri **确实**抓到了问题，你就知道有 bug；但仅仅因为 Miri **没有**抓到，并不意味着没有问题。不过它确实能发现很多问题。不妨对本章其它不安全代码示例也跑一遍 Miri，看看它会说什么！

　　更多信息见 [Miri 的 GitHub 仓库][miri]。

### 正确使用不安全代码

　　使用 `unsafe` 来动用上述五类超能力之一并没有错，甚至也谈不上不受欢迎；但要写对 `unsafe` 代码更难，因为编译器帮不上内存安全的忙。当你有正当理由使用 `unsafe` 时就可以用，而显式的 `unsafe` 标注会让问题出现时更容易定位源头。每当编写不安全代码时，都可以借助 Miri，更有信心地确认代码遵循了 Rust 的规则。

　　若想更深入地了解如何高效使用不安全 Rust，请阅读 Rust 关于该主题的官方指南 [The Rustonomicon][nomicon]。

[dangling-references]: ../../understanding-ownership/02-references-and-borrowing/#dangling-references
[ABI]: https://doc.rust-lang.org/reference/items/external-blocks.html#abi
[constants]: ../../common-programming-concepts/01-variables-and-mutability/#declaring-constants
[send-and-sync]: ../../concurrency/04-extensible-concurrency-sync-and-send/
[the-slice-type]: ../../understanding-ownership/03-slices/#the-slice-type
[unions]: https://doc.rust-lang.org/reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: ../../appendix/05-e-editions/
[nightly]: ../../appendix/07-g-nightly-rust/
[nomicon]: https://doc.rust-lang.org/nomicon/
