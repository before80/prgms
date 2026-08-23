+++
title = "0 引用与生命周期回顾"
date = 2026-08-23T16:26:00+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_0.html](https://tfpk.github.io/lifetimekata/chapter_0.html)

*（本节为复习内容，部分读者可能已熟悉。
若你已了解引用的概念，可以跳过。）*

如果你使用 Rust 已有一段时间，想必已经接触过引用。对于任意类型 `T`，都有两种引用形式：

 - `&T`：`T` 的共享引用（常称为共享借用）。你可以同时拥有任意多个，但它们不允许修改所指向的数据。
 - `&mut T`：`T` 的可变引用（常称为独占借用）。同一时刻只能有一个，但允许修改所指向的数据。

引用让你可以在不复制数据的情况下，对数据调用函数。

Rust 引用的强大之处在于：它们保证始终指向仍然存在的对象（即尚未被 drop/释放/离开作用域）。指向已不存在对象的引用称为「悬垂引用」，Rust 保证你永远不会拥有这样的引用。因此，下面的例子无法通过编译：

```rust
fn main() {
    let x_ref = {
        let x = 3;
        &x
    };
    // 此时 x_ref 会指向 `x`，但 `x` 已离开作用域，因此 x_ref 是悬垂的。
   
    println!("{}", x_ref)
}
```

大多数现代语言（Python、Java 等）通过在运行时持续检查是否仍有引用指向某对象，并在没有任何引用时才释放它，来避免悬垂引用问题。这称为「垃圾回收」，其优点是无需考虑对象何时被释放——语言会替你处理。缺点是性能：垃圾回收需要程序偶尔暂停，让语言扫描你持有的每一个引用。

有些语言（尤其是 C 和汇编）提供「指针」类型。由于指针只是内存中的原始地址，编译器把避免悬垂引用的责任留给程序员。这使它们适用于内存受限或对性能要求极高的场景，但不幸的是，bug 可能在内存被销毁后仍去访问它，导致崩溃，甚至更糟——安全漏洞。

Rust 的强大之处在于：它让你在运行时确信永远不会访问已释放的内存；为此付出的代价是，你必须在编译时说服编译器：你正确使用了引用。

## 一个未能说服编译器的例子

你肯定遇到过下面这样的错误：

```rust
fn main() {
    let mut my_reference: Option<&String> = None;

    // 开始一个作用域
    {
        // my_variable 被创建                               // \ \
        let my_variable: String = "hello".to_string();       // | |
        my_reference = Some(&my_variable);                   // | |- my_variable 在此存在。（'variable）
        // 作用域结束时，`my_variable` 被 drop              // | |
        drop(my_variable);                                   // | |
        // my_variable 被销毁                                // | /
    }                                                        // | - my_reference 需要在此存在。（'reference）
                                                             // |
    if let Some(reference) = my_reference {                  // |
        println!("{}", reference);                           // |
    }                                                        // /

}
```

```
error[E0597]: `my_variable` does not live long enough
  --> bad_lifetimes.rs:7:29
   |
7  |         my_reference = Some(&my_variable);
   |                             ^^^^^^^^^^^^ borrowed value does not live long enough
8  |     }
   |     - `my_variable` dropped here while still borrowed
9  |
10 |     if let Some(reference) = my_reference {
   |                              ------------ borrow later used here

error: aborting due to previous error; 1 warning emitted

```

在这个例子中，由于 `my_variable` 在 `my_reference` 之前离开作用域，`if let` 有可能尝试访问 `my_reference`，却发现它指向的变量已不存在。

Rust 会说这个变量「存活得不够久」。它注意到「`my_variable` 有可能在存入 `my_reference` 的引用仍被使用之前就被 drop」。

形式上，我们可以通过观察这两样东西需要存在的代码区域来理解这一点。引用需要存在的代码区域，*大于*变量存在的代码区域。这表明在引用存在的某段时间里，变量可能已被 drop，因此可能出现悬垂引用。

我们把引用必须有效的代码区域称为「生命周期」。可以用 `'name` 语法为生命周期命名。设 `'variable` 为指向该变量的引用有效的代码区域，设 `'reference` 为引用可能被使用的代码区域。形式上可以说，`'variable` 必须大于 `'reference`。

这显然是成立的，它是「引用有效的代码区域必须大于引用实际可使用的代码区域」的简写。反过来想：若引用在某处可使用，而引用在该处却无效，你就会得到*无效*的东西——不安全的代码，换句话说，就是 bug。

## 那这本书讲什么？

有些情况下 Rust 编译器无法自行推断生命周期，需要程序员显式指定。本书旨在帮助你提高编写显式生命周期（如 `&'a str`）的能力。下一章就开始！

## 练习：完成 Rustlings 中关于生命周期的练习

若你不确定是否理解了上文，在继续阅读之前，
[请完成 rustlings 中关于生命周期的练习](https://github.com/rust-lang/rustlings/tree/main/exercises/16_lifetimes)。
