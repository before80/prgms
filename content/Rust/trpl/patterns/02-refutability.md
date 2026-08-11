+++
title = "19.2 可反驳性：模式是否可能匹配失败"
date = 2026-08-05T08:44:00+08:00
weight = 92
type = "docs"
description = "模式分为两种形式：可反驳（refutable）和不可反驳（irrefutable）。对传入的任意可能值都能匹配的模式，称为不可反驳模式。比如语句 `let x = 5;` 中的 `x` 就是一个例子，因为 `x` 可以匹配任何值，因此不可能匹配失败。"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 可反驳性：模式是否可能匹配失败


> 原文链接: [https://doc.rust-lang.org/stable/book/ch19-02-refutability.html](https://doc.rust-lang.org/stable/book/ch19-02-refutability.html)


## 可反驳性：模式是否可能匹配失败

　　模式分为两种形式：可反驳（*refutable*）和不可反驳（*irrefutable*）。对传入的任意可能值都能匹配的模式，称为**不可反驳**模式。比如语句 `let x = 5;` 中的 `x` 就是一个例子，因为 `x` 可以匹配任何值，因此不可能匹配失败。对某些可能值会匹配失败的模式，称为**可反驳**模式。比如表达式 `if let Some(x) = a_value` 中的 `Some(x)`；如果变量 `a_value` 中的值是 `None` 而不是 `Some`，那么模式 `Some(x)` 就不会匹配。

　　函数参数、`let` 语句和 `for` 循环只能接受不可反驳模式，因为当值不匹配时，程序无法做出有意义的事情。`if let` 和 `while let` 表达式，以及 `let...else` 语句既接受可反驳模式，也接受不可反驳模式；不过编译器会对其中的不可反驳模式发出警告，因为根据定义，这些结构本来就是为处理可能失败的情况而设计的：条件判断的意义就在于它可以根据成功或失败执行不同的逻辑。

　　一般来说，你不必时刻担心可反驳模式和不可反驳模式的区别；不过你确实需要熟悉“可反驳性”这个概念，这样当你在错误信息里看到它时，就知道该如何应对。遇到这类情况时，你需要根据代码想要表达的行为，修改模式本身，或者修改与之搭配使用的语法结构。

　　让我们来看一个例子：当我们试图在 Rust 要求使用不可反驳模式的地方使用可反驳模式，以及反过来时，会发生什么。示例 19-8 展示了一个 `let` 语句，不过我们给它写了模式 `Some(x)`，这是一个可反驳模式。正如你可能已经猜到的，这段代码不会通过编译。

```rust
    let Some(x) = some_option_value;
```

**示例 19-8：尝试在 `let` 中使用可反驳模式**

　　如果 `some_option_value` 的值是 `None`，它就无法匹配模式 `Some(x)`，这说明该模式是可反驳的。然而，`let` 语句只能接受不可反驳模式，因为当值是 `None` 时，这段代码并没有什么合法的后续操作可做。在编译期，Rust 会抱怨我们试图在要求不可反驳模式的地方使用可反驳模式：

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
error[E0005]: refutable pattern in local binding
 --> src/main.rs:3:9
  |
3 |     let Some(x) = some_option_value;
  |         ^^^^^^^ pattern `None` not covered
  |
  = note: `let` bindings require an "irrefutable pattern", like a `struct` or an `enum` with only one variant
  = note: for more information, visit https://doc.rust-lang.org/book/ch19-02-refutability.html
  = note: the matched value is of type `Option<i32>`
help: you might want to use `let...else` to handle the variant that isn't matched
  |
3 |     let Some(x) = some_option_value else { todo!() };
  |                                     ++++++++++++++++

For more information about this error, try `rustc --explain E0005`.
error: could not compile `patterns` (bin "patterns") due to 1 previous error
```

　　因为我们没有覆盖模式 `Some(x)` 所对应的所有合法值（而且也不可能覆盖全部），所以 Rust 理所当然地给出了编译错误。

　　如果在某个需要不可反驳模式的地方却有一个可反驳模式，我们可以通过修改使用该模式的代码来修复这个问题：不用 `let`，而改用 `let...else`。这样一来，如果模式不匹配，大括号中的代码就会处理该值。示例 19-9 展示了如何修复示例 19-8 中的代码。

```rust
    let Some(x) = some_option_value else {
        return;
    };
```

**示例 19-9：用 `let...else` 和一个带可反驳模式的代码块来代替 `let`**

　　我们给这段代码留出了一条退路！现在这段代码是完全合法的。不过这也意味着，我们不能在这里使用不可反驳模式而不收到警告。如果我们给 `let...else` 一个总能匹配的模式，比如示例 19-10 中的 `x`，编译器就会发出警告。

```rust
    let x = 5 else {
        return;
    };
```

**示例 19-10：尝试在 `let...else` 中使用不可反驳模式**

　　Rust 会抱怨说，在 `let...else` 中使用不可反驳模式没有意义：

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
warning: unreachable `else` clause
 --> src/main.rs:2:15
  |
2 |     let x = 5 else {
  |     --------- ^^^^
  |     |
  |     assigning to binding pattern will always succeed
  |
  = note: this pattern always matches, so the else clause is unreachable
  = note: `#[warn(irrefutable_let_patterns)]` on by default

warning: `patterns` (bin "patterns") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.39s
     Running `target/debug/patterns`
```

　　基于这个原因，`match` 分支必须使用可反驳模式，只有最后一个分支例外，它应该用一个不可反驳模式来匹配所有剩余值。Rust 允许我们在一个只有单个分支的 `match` 中使用不可反驳模式，不过这种写法并没有太大用处，而且完全可以被更简单的 `let` 语句替代。

　　既然现在你已经知道模式该用在什么地方，以及可反驳模式和不可反驳模式之间的区别，接下来我们就来看看所有可以用来创建模式的语法。
