+++
title = "4.2 引用与借用"
date = 2026-08-05T08:44:00+08:00
weight = 17
type = "docs"
description = "引用与借用：在不取得所有权的情况下使用值"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 引用与借用


> 原文链接: [https://doc.rust-lang.org/stable/book/ch04-02-references-and-borrowing.html](https://doc.rust-lang.org/stable/book/ch04-02-references-and-borrowing.html)


## 引用与借用

　　示例 4-5 中元组写法的问题在于：我们必须把 `String` 返回给调用方，才能在调用 `calculate_length` 之后继续使用它，因为 `String` 被移动进了 `calculate_length`。取而代之，我们可以提供指向该 `String` 值的引用。引用很像指针：它是一个地址，你可以跟着它去访问该地址上存放的数据；而数据本身由某个其他变量拥有。与指针不同的是，引用在其生命周期内保证指向某一特定类型的有效值。

　　下面演示如何定义并使用以值的引用为参数、而不取得值所有权的 `calculate_length` 函数：

**文件名：`src/main.rs`**
```rust
fn main() {
    let s1 = String::from("hello");

    let len = calculate_length(&s1);

    println!("The length of '{s1}' is {len}.");
}

fn calculate_length(s: &String) -> usize {
    s.len()
}
```

　　首先注意，变量声明和函数返回值里的元组相关代码都不见了。其次，我们把 `&s1` 传给 `calculate_length`，在函数定义里接收的是 `&String` 而不是 `String`。这些 `&` 表示引用，让你可以引用某个值而不取得其所有权。图 4-6 描绘了这一概念。

<img alt="三张表：表 s 只包含指向表 s1 的指针。表 s1 包含 s1 的栈数据，并指向堆上的字符串数据。" src="img/trpl04-06.svg" class="center" />

<span class="caption">图 4-6：`&String` 类型的 `s` 指向 `String` 类型的 `s1` 的示意图</span>

> 注意：用 `&` 引用的反面是*解引用*（dereferencing），通过解引用运算符 `*` 完成。第 8 章会看到一些解引用的用法，第 15 章会详细讨论解引用。

　　再仔细看看这里的函数调用：

```rust
    let s1 = String::from("hello");

    let len = calculate_length(&s1);
```

　　`&s1` 语法让我们创建一个*引用* `s1` 的值、但不拥有它的引用。因为引用并不拥有该值，所以当引用停止使用时，它所指向的值不会被丢弃。

　　同样，函数签名用 `&` 表明参数 `s` 的类型是引用。加上一些说明性注释：

```rust
fn calculate_length(s: &String) -> usize { // s is a reference to a String
    s.len()
} // Here, s goes out of scope. But because s does not have ownership of what
  // it refers to, the String is not dropped.
```

　　变量 `s` 的有效作用域与任何函数参数相同，但当 `s` 停止使用时，引用所指向的值不会被丢弃，因为 `s` 并不拥有所有权。函数以引用而非实际值作为参数时，我们就不必为了归还所有权而返回这些值——因为我们从未拥有过所有权。

　　创建引用的动作称为*借用*（borrowing）。就像现实生活中：别人拥有某物时，你可以从他那里借来用；用完要还回去，你并不拥有它。

　　那么，若试图修改我们正在借用的东西会怎样？试试示例 4-6 中的代码。提前说明：这样行不通！

**文件名：`src/main.rs`**
```rust
fn main() {
    let s = String::from("hello");

    change(&s);
}

fn change(some_string: &String) {
    some_string.push_str(", world");
}
```

**示例 4-6：尝试修改借用的值**

　　错误如下：

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0596]: cannot borrow `*some_string` as mutable, as it is behind a `&` reference
 --> src/main.rs:8:5
  |
8 |     some_string.push_str(", world");
  |     ^^^^^^^^^^^ `some_string` is a `&` reference, so it cannot be borrowed as mutable
  |
help: consider changing this to be a mutable reference
  |
7 | fn change(some_string: &mut String) {
  |                         +++

For more information about this error, try `rustc --explain E0596`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

　　正如变量默认不可变一样，引用也默认不可变。我们不被允许修改通过引用指向的内容。

### 可变引用

　　只需几处小改动，改用*可变引用*（mutable reference），就能修好示例 4-6 的代码，允许修改借用的值：

**文件名：`src/main.rs`**
```rust
fn main() {
    let mut s = String::from("hello");

    change(&mut s);
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

　　首先把 `s` 改为 `mut`。然后在调用 `change` 时用 `&mut s` 创建可变引用，并把函数签名更新为接受可变引用：`some_string: &mut String`。这样就清楚表明：`change` 函数会修改它所借用的值。

　　可变引用有一个很大的限制：若你对某个值有一个可变引用，就不能再有指向该值的其他引用。下面这段试图创建两个指向 `s` 的可变引用的代码会失败：

**文件名：`src/main.rs`**
```rust
    let mut s = String::from("hello");

    let r1 = &mut s;
    let r2 = &mut s;

    println!("{r1}, {r2}");
```

　　错误如下：

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0499]: cannot borrow `s` as mutable more than once at a time
 --> src/main.rs:5:14
  |
4 |     let r1 = &mut s;
  |              ------ first mutable borrow occurs here
5 |     let r2 = &mut s;
  |              ^^^^^^ second mutable borrow occurs here
6 |
7 |     println!("{r1}, {r2}");
  |                -- first borrow later used here

For more information about this error, try `rustc --explain E0499`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

　　错误指出这段代码无效，因为我们不能在同一时间对 `s` 进行超过一次的可变借用。第一次可变借用在 `r1` 中，必须持续到它在 `println!` 中被使用；但在创建该可变引用与使用它之间，我们又试图在 `r2` 中创建另一个可变引用，去借用与 `r1` 相同的数据。

　　禁止在同一时间对同一数据存在多个可变引用，使得修改得以进行，却又处于严格受控之中。Rust 新手常为此困扰，因为多数语言允许你随时修改。这一限制的好处是：Rust 能在编译期防止数据竞争。*数据竞争*（data race）类似于竞态条件，会在以下三种行为同时发生时出现：

- 两个或更多指针同时访问同一数据。
- 至少有一个指针在写入该数据。
- 没有用于同步该数据访问的机制。

　　数据竞争会导致未定义行为，若要在运行时追踪，往往很难诊断和修复；Rust 通过拒绝编译存在数据竞争的代码来防止这一问题！

　　一如既往，我们可以用花括号创建新作用域，从而允许有多个可变引用，只是不能*同时*存在：

```rust
    let mut s = String::from("hello");

    {
        let r1 = &mut s;
    } // r1 goes out of scope here, so we can make a new reference with no problems.

    let r2 = &mut s;
```

　　Rust 对可变引用与不可变引用的组合也有类似规则。下面的代码会报错：

```rust
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    let r3 = &mut s; // BIG PROBLEM

    println!("{r1}, {r2}, and {r3}");
```

　　错误如下：

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> src/main.rs:6:14
  |
4 |     let r1 = &s; // no problem
  |              -- immutable borrow occurs here
5 |     let r2 = &s; // no problem
6 |     let r3 = &mut s; // BIG PROBLEM
  |              ^^^^^^ mutable borrow occurs here
7 |
8 |     println!("{r1}, {r2}, and {r3}");
  |                -- immutable borrow later used here

For more information about this error, try `rustc --explain E0502`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

　　哎呀！在已有指向同一值的不可变引用时，我们*也不能*再有可变引用。

　　不可变引用的使用者并不期望所读数据在他们不知情时被修改！不过允许多个不可变引用，因为只读数据的人无法影响其他人对同一数据的读取。

　　注意：引用的作用域从引入之处开始，一直持续到该引用最后一次被使用。例如，下面的代码可以编译，因为不可变引用的最后一次使用发生在 `println!` 中，且在引入可变引用之前：

```rust
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    println!("{r1} and {r2}");
    // Variables r1 and r2 will not be used after this point.

    let r3 = &mut s; // no problem
    println!("{r3}");
```

　　不可变引用 `r1` 和 `r2` 的作用域在它们最后一次被使用的 `println!` 之后结束，而这发生在创建可变引用 `r3` 之前。这些作用域不重叠，因此代码被允许：编译器能判断在作用域真正结束之前，引用已不再被使用。

　　即便借用错误有时令人沮丧，也请记住：这是 Rust 编译器在早期（编译期而非运行时）指出潜在 bug，并精确告诉你问题所在。你就不必再去追查「为什么数据不是我想的那样」。

### 悬垂引用 {#dangling-references}

　　在带指针的语言里，很容易错误地创建*悬垂指针*（dangling pointer）——指针仍指向某块内存，但那块内存可能已被释放并交给别人使用——做法往往是释放内存却保留指向它的指针。相比之下，Rust 编译器保证引用永远不会是悬垂引用：若你有指向某数据的引用，编译器会确保该数据的作用域不会在引用之前结束。

　　试着创建一个悬垂引用，看看 Rust 如何用编译期错误阻止它：

**文件名：`src/main.rs`**
```rust
fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");

    &s
}
```

　　错误如下：

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0106]: missing lifetime specifier
 --> src/main.rs:5:16
  |
5 | fn dangle() -> &String {
  |                ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but there is no value for it to be borrowed from
help: consider using the `'static` lifetime, but this is uncommon unless you're returning a borrowed value from a `const` or a `static`
  |
5 | fn dangle() -> &'static String {
  |                 +++++++
help: instead, you are more likely to want to return an owned value
  |
5 - fn dangle() -> &String {
5 + fn dangle() -> String {
  |

For more information about this error, try `rustc --explain E0106`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

　　这条错误信息提到了我们尚未介绍的特性：生命周期（lifetime）。第 10 章会详细讨论生命周期。不过，若暂时忽略与生命周期有关的部分，信息里已经点出了这段代码出问题的关键：

```text
this function's return type contains a borrowed value, but there is no value
for it to be borrowed from
```

　　再仔细看看 `dangle` 代码每个阶段究竟发生了什么：

**文件名：`src/main.rs`**
```rust
fn dangle() -> &String { // dangle returns a reference to a String

    let s = String::from("hello"); // s is a new String

    &s // we return a reference to the String, s
} // Here, s goes out of scope and is dropped, so its memory goes away.
  // Danger!
```

　　因为 `s` 在 `dangle` 内部创建，当 `dangle` 的代码结束时，`s` 会被释放。但我们却试图返回指向它的引用。这意味着该引用会指向无效的 `String`。这可不行！Rust 不会让我们这样做。

　　这里的解决办法是直接返回 `String`：

```rust
fn no_dangle() -> String {
    let s = String::from("hello");

    s
}
```

　　这样完全没有问题。所有权被移出，没有任何东西被提前释放。

### 引用的规则

　　总结一下关于引用的讨论：

- 在任意给定时刻，你要么只能有*一个*可变引用，要么可以有任意数量的不可变引用。
- 引用必须始终有效。

　　接下来，我们看另一种引用：切片。
