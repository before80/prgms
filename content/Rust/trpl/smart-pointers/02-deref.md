+++
title = "15.2 把智能指针当作常规引用"
date = 2026-08-05T08:44:00+08:00
weight = 69
type = "docs"
description = "实现 Deref 特征，让智能指针表现得像常规引用"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 把智能指针当作常规引用


> 原文链接: [https://doc.rust-lang.org/stable/book/ch15-02-deref.html](https://doc.rust-lang.org/stable/book/ch15-02-deref.html)


## 把智能指针当作常规引用 {#treating-smart-pointers-like-regular-references}

　　实现 `Deref` 特征可以自定义**解引用运算符** `*` 的行为（不要与乘法或 glob 运算符混淆）。若以“智能指针可当作常规引用对待”的方式实现 `Deref`，你就可以编写操作引用的代码，并让这些代码也能用于智能指针。

　　我们先看解引用运算符如何作用于常规引用。然后尝试定义一个行为类似 `Box<T>` 的自定义类型，并看看为何解引用运算符在我们新定义的类型上不像引用那样工作。接着会探索实现 `Deref` 如何让智能指针以类似引用的方式工作。最后会介绍 Rust 的解引用强制转换（deref coercion），以及它如何让我们同时方便地使用引用或智能指针。

### 沿着引用到达值 {#following-the-pointer-to-the-value-with-the-dereference-operator}

　　常规引用是一种指针；可以把指针想成指向别处所存值的箭头。示例 15-6 中，我们创建对一个 `i32` 值的引用，再用解引用运算符沿着引用到达该值。

**文件名：`src/main.rs`**
```rust
fn main() {
    let x = 5;
    let y = &x;

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

**示例 15-6：用解引用运算符沿着引用到达 `i32` 值**

　　变量 `x` 保存 `i32` 值 `5`。我们把 `y` 设为对 `x` 的引用。可以断言 `x` 等于 `5`。但若要对 `y` 中的值做断言，就必须用 `*y` 沿着引用到达它所指向的值（因此称为**解引用**），编译器才能比较实际的值。解引用 `y` 之后，就可以访问它指向的整数，并与 `5` 比较。

　　若写成 `assert_eq!(5, y);`，会得到如下编译错误：

```console
$ cargo run
   Compiling deref-example v0.1.0 (file:///projects/deref-example)
error[E0277]: can't compare `{integer}` with `&{integer}`
 --> src/main.rs:6:5
  |
6 |     assert_eq!(5, y);
  |     ^^^^^^^^^^^^^^^^ no implementation for `{integer} == &{integer}`
  |
  = help: the trait `PartialEq<&{integer}>` is not implemented for `{integer}`
  = help: the following other types implement trait `PartialEq<Rhs>`:
            f128
            f16
            f32
            f64
            i128
            i16
            i32
            i64
          and 8 others

For more information about this error, try `rustc --explain E0277`.
error: could not compile `deref-example` (bin "deref-example") due to 1 previous error
```

　　不允许比较数字与指向数字的引用，因为它们是不同类型。必须用解引用运算符沿着引用到达它所指向的值。

### 像引用一样使用 `Box<T>`

　　我们可以把示例 15-6 改写成使用 `Box<T>` 而不是引用；示例 15-7 中对 `Box<T>` 使用解引用运算符，其作用与示例 15-6 中对引用使用解引用运算符相同。

**文件名：`src/main.rs`**

```rust
fn main() {
    let x = 5;
    let y = Box::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

**示例 15-7**


　　示例 15-7 与示例 15-6 的主要区别是：这里把 `y` 设为指向 `x` 的副本的 box 实例，而不是指向 `x` 的值的引用。在最后的断言中，我们可以像 `y` 是引用时那样，用解引用运算符沿着 box 的指针前进。接下来，通过定义自己的 box 类型，看看 `Box<T>` 有何特殊之处，才使我们能使用解引用运算符。

### 定义自己的智能指针

　　我们来构建一个与标准库 `Box<T>` 类似的包装类型，体会智能指针类型默认时与引用有何不同。然后再看如何加入使用解引用运算符的能力。

> 说明：我们即将构建的 `MyBox<T>` 与真正的 `Box<T>` 有一个重大区别：我们的版本不会把数据存在堆上。本例重点在 `Deref`，因此数据实际存放在哪里，不如指针般的行为重要。

　　`Box<T>` 本质上定义为含一个元素的元组结构体，因此示例 15-8 以同样方式定义 `MyBox<T>`。我们还定义 `new` 函数，以匹配 `Box<T>` 上的 `new`。

**文件名：`src/main.rs`**

```rust
struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}
```

**示例 15-8**


　　我们定义名为 `MyBox` 的结构体，并声明泛型参数 `T`，因为希望该类型能保存任意类型的值。`MyBox` 是含一个 `T` 类型元素的元组结构体。`MyBox::new` 接受一个 `T` 参数，并返回持有该传入值的 `MyBox` 实例。

　　试着把示例 15-7 的 `main` 加到示例 15-8，并改用我们定义的 `MyBox<T>` 而不是 `Box<T>`。示例 15-9 的代码无法编译，因为 Rust 不知道如何解引用 `MyBox`。

**文件名：`src/main.rs`**

```rust
fn main() {
    let x = 5;
    let y = MyBox::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

**示例 15-9**


　　得到的编译错误如下：

```console
$ cargo run
   Compiling deref-example v0.1.0 (file:///projects/deref-example)
error[E0614]: type `MyBox<{integer}>` cannot be dereferenced
  --> src/main.rs:14:19
   |
14 |     assert_eq!(5, *y);
   |                   ^^ can't be dereferenced

For more information about this error, try `rustc --explain E0614`.
error: could not compile `deref-example` (bin "deref-example") due to 1 previous error
```

　　我们的 `MyBox<T>` 无法被解引用，因为尚未在该类型上实现这种能力。要启用 `*` 运算符解引用，需要实现 `Deref` 特征。

### 实现 `Deref` 特征

　　正如第 10 章 [「为类型实现 trait」](/trpl/generics/02-traits/#implementing-a-trait-on-a-type) 所述，实现特征需要为特征要求的方法提供实现。标准库提供的 `Deref` 特征要求实现一个名为 `deref` 的方法：它借用 `self`，并返回指向内部数据的引用。示例 15-10 给出了要加到 `MyBox<T>` 定义上的 `Deref` 实现。

**文件名：`src/main.rs`**

```rust
use std::ops::Deref;

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
```

**示例 15-10**


　　`type Target = T;` 语法为 `Deref` 特征定义了一个关联类型。关联类型是声明泛型参数的另一种略有不同的方式，目前不必深究；第 20 章会更详细介绍。

　　我们在 `deref` 方法体中填入 `&self.0`，使 `deref` 返回希望用 `*` 运算符访问的值的引用；回想第 5 章[「用元组结构体创建不同的类型」](/trpl/structs/01-defining-structs/#creating-different-types-with-tuple-structs)，`.0` 访问元组结构体中的第一个值。示例 15-9 中对 `MyBox<T>` 值调用 `*` 的 `main` 现在可以编译，断言也会通过！

　　没有 `Deref` 特征时，编译器只能解引用 `&` 引用。`deref` 方法让编译器能对任意实现了 `Deref` 的类型取值，调用 `deref` 得到它知道如何解引用的引用。

　　当我们在示例 15-9 中写下 `*y` 时，Rust 在幕后实际运行的是这段代码：

```rust
*(y.deref())
```

　　Rust 把 `*` 运算符替换为对 `deref` 方法的调用，再做一次普通解引用，这样我们就不必考虑是否需要调用 `deref`。这一特性让我们写出的代码在常规引用与实现了 `Deref` 的类型上都能同样工作。

　　`deref` 方法返回对值的引用、且 `*(y.deref())` 括号外仍需要普通解引用，原因与所有权系统有关。若 `deref` 直接返回值而不是引用，值就会从 `self` 中被移出。在这种情况下，以及多数使用解引用运算符的情况下，我们都不希望取得 `MyBox<T>` 内部值的所有权。

　　注意：每次在代码中使用 `*` 时，`*` 运算符只会被替换为一次对 `deref` 方法的调用，再加一次对 `*` 运算符的调用。由于这种替换不会无限递归，我们最终得到的是 `i32` 类型的数据，与示例 15-9 中 `assert_eq!` 里的 `5` 匹配。

### 在函数与方法中使用解引用强制转换

　　**解引用强制转换**（deref coercion）会把实现了 `Deref` 特征的类型的引用，转换为另一类型的引用。例如，解引用强制转换可以把 `&String` 转为 `&str`，因为 `String` 实现的 `Deref` 返回 `&str`。解引用强制转换是 Rust 在函数与方法参数上提供的便利，且只作用于实现了 `Deref` 的类型。当我们把某类型值的引用作为参数传给函数或方法，而该引用与定义中的参数类型不匹配时，它会自动发生。一系列对 `deref` 方法的调用会把我们提供的类型转换为参数所需的类型。

　　Rust 加入解引用强制转换，是为了让编写函数与方法调用的程序员不必加入那么多显式的 `&` 与 `*`。这一特性也让我们能写出更多既适用于引用、也适用于智能指针的代码。

　　为观察解引用强制转换，我们使用示例 15-8 中定义的 `MyBox<T>`，以及示例 15-10 中添加的 `Deref` 实现。示例 15-11 定义了一个参数为字符串切片的函数。

**文件名：`src/main.rs`**
```rust
fn hello(name: &str) {
    println!("Hello, {name}!");
}
```

**示例 15-11：参数 `name` 类型为 `&str` 的 `hello` 函数**

　　我们可以用字符串切片作为参数调用 `hello`，例如 `hello("Rust");`。借助解引用强制转换，也可以用指向 `MyBox<String>` 值的引用调用 `hello`，如示例 15-12 所示。

**文件名：`src/main.rs`**

```rust
fn main() {
    let m = MyBox::new(String::from("Rust"));
    hello(&m);
}
```

**示例 15-12**


　　这里用参数 `&m` 调用 `hello`，`&m` 是指向 `MyBox<String>` 值的引用。因为我们在示例 15-10 中为 `MyBox<T>` 实现了 `Deref`，Rust 可以通过调用 `deref` 把 `&MyBox<String>` 转为 `&String`。标准库为 `String` 提供了返回字符串切片的 `Deref` 实现（见 `Deref` 的 API 文档）。Rust 再次调用 `deref`，把 `&String` 转为 `&str`，从而匹配 `hello` 函数的定义。

　　若 Rust 没有实现解引用强制转换，我们就得写示例 15-13 那样的代码，而不是示例 15-12，才能用 `&MyBox<String>` 类型的值调用 `hello`。

**文件名：`src/main.rs`**
```rust
fn main() {
    let m = MyBox::new(String::from("Rust"));
    hello(&(*m)[..]);
}
```

**示例 15-13：若 Rust 没有解引用强制转换，我们将不得不这样写**

　　`(*m)` 把 `MyBox<String>` 解引用为 `String`。然后 `&` 与 `[..]` 取出等于整个字符串的字符串切片，以匹配 `hello` 的签名。没有解引用强制转换的这段代码，符号更多，更难读、写、理解。解引用强制转换让 Rust 自动处理这些转换。

　　当相关类型定义了 `Deref` 特征时，Rust 会分析类型，并根据需要多次使用 `Deref::deref`，以得到匹配参数类型的引用。需要插入多少次 `Deref::deref` 在编译期就已确定，因此利用解引用强制转换没有运行时惩罚！

### 处理可变引用上的解引用强制转换

　　类似于用 `Deref` 特征覆盖不可变引用上的 `*` 运算符，你可以用 `DerefMut` 特征覆盖可变引用上的 `*` 运算符。

　　Rust 在发现类型与特征实现满足以下三种情形时会做解引用强制转换：

1. 当 `T: Deref<Target=U>` 时，从 `&T` 到 `&U`
2. 当 `T: DerefMut<Target=U>` 时，从 `&mut T` 到 `&mut U`
3. 当 `T: Deref<Target=U>` 时，从 `&mut T` 到 `&U`

　　前两种情形相同，只是第二种涉及可变性。第一种说：若有 `&T`，且 `T` 实现了指向某类型 `U` 的 `Deref`，就可以透明地得到 `&U`。第二种说：对可变引用也会发生同样的解引用强制转换。

　　第三种更微妙：Rust 也会把可变引用强制转换为不可变引用。但反过来**不行**：不可变引用永远不会被强制转换为可变引用。由于借用规则，若你有可变引用，它必须是指向该数据的唯一引用（否则程序无法编译）。把一个可变引用转为一个不可变引用永远不会破坏借用规则。把不可变引用转为可变引用，则要求最初的那个不可变引用是指向该数据的唯一不可变引用，但借用规则并不保证这一点。因此，Rust 不能假定把不可变引用转为可变引用是可行的。

[impl-trait]: /trpl/generics/02-traits/#implementing-a-trait-on-a-type
[tuple-structs]: /trpl/structs/01-defining-structs/#creating-different-types-with-tuple-structs
