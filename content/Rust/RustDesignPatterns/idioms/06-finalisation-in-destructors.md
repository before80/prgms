+++
title = "06-析构器中的收尾"
date = 2026-08-18T22:10:00+08:00
weight = 10
type = "docs"
description = "析构器中的收尾 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/dtor-finally.html](https://rust-unofficial.github.io/patterns/idioms/dtor-finally.html)

# 析构器中的收尾

## 描述 {#description}

Rust 没有与 `finally` 块等价的机制——无论函数以何种方式退出都会执行的代码。
取而代之，可以使用对象的析构器来运行必须在退出前执行的代码。

## 示例 {#example}

```rust,ignore
fn baz() -> Result<(), ()> {
    // 一些代码
}

fn bar() -> Result<(), ()> {
    // 这些不必定义在函数内部。
    struct Foo;

    // 为 Foo 实现析构器。
    impl Drop for Foo {
        fn drop(&mut self) {
            println!("exit");
        }
    }

    // 无论函数 `bar` 以何种方式退出，_exit 的析构器都会运行。
    let _exit = Foo;
    // 使用 `?` 运算符的隐式返回。
    baz()?;
    // 正常返回。
    Ok(())
}
```

## 动机 {#motivation}

如果函数有多个返回点，那么在退出时执行代码就会变得困难且重复（因而容易出错）。
在由于宏而导致返回是隐式的情况下尤其如此。一个常见情形是 `?` 运算符：若结果是 `Err` 则返回，
若是 `Ok` 则继续。`?` 被用作异常处理机制，但与 Java（它有 `finally`）不同，
没有办法安排代码在正常情况和异常情况下都运行。发生 panic 也会使函数提前退出。

## 优点 {#advantages}

析构器中的代码（几乎）总会运行——能应对 panic、提前返回等情况。

## 缺点 {#disadvantages}

并不保证析构器一定会运行。例如，若函数中有无限循环，或函数在退出前崩溃。
若已在 panic 的线程中再次 panic，析构器也不会运行。因此，在必须绝对确保收尾发生的场合，
不能把析构器当作终结器来依赖。

这种模式会引入一些难以察觉的隐式代码。阅读函数时，看不出退出时会运行哪些析构器。
这会让调试变得棘手。

仅仅为了收尾就需要一个对象和 `Drop` 实现，样板代码很重。

## 讨论 {#discussion}

如何存储用作终结器的对象，有一些微妙之处。它必须保持存活直到函数结束，然后必须被销毁。
该对象必须始终是值或唯一拥有的指针（例如 `Box<Foo>`）。如果使用共享指针（如 `Rc`），
终结器就可能在函数生命周期之外继续存活。出于类似原因，终结器不应被移动或返回。

终结器必须赋给一个变量，否则它会立即被销毁，而不是在离开作用域时销毁。
如果该变量只用作终结器，变量名必须以 `_` 开头，否则编译器会警告终结器从未被使用。
但不要把变量叫作没有后缀的 `_`——那样它会立即被销毁。

在 Rust 中，对象离开作用域时会运行析构器。无论我们到达块的末尾、提前返回，还是程序 panic，都会如此。
panic 时，Rust 会展开栈，为每个栈帧中的每个对象运行析构器。因此，即便 panic 发生在被调用的函数中，
析构器也会被调用。

如果在展开过程中析构器发生 panic，就没有好的应对办法，因此 Rust 会立即中止该线程，不再运行后续析构器。
这意味着析构器并非绝对保证会运行。这也意味着你必须在析构器中格外小心不要 panic，
因为它可能使资源处于意外状态。

## 参见 {#see-also}

[RAII 守卫](../design-patterns/01-behavioural/04-raii-guards/)。
