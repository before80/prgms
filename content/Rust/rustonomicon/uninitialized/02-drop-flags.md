+++
title = "5.2 Drop 标志"
date = 2026-08-06T17:08:00+08:00
weight = 29
type = "docs"
description = "Drop 标志如何跟踪初始化"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Drop 标志


> 原文链接: [https://doc.rust-lang.org/nomicon/drop-flags.html](https://doc.rust-lang.org/nomicon/drop-flags.html)


　　上一节的例子为 Rust 引入了一个有趣问题。
　　我们已经看到可以有条件地初始化、去初始化和重新初始化内存位置，且完全安全。对 `Copy` 类型这不特别值得注意，因为它们只是随机比特堆。但有析构函数的类型不同：Rust 需要知道变量被赋值或变量离开作用域时是否应调用析构函数。
　　在有条件初始化的情况下如何做到？

　　注意并非所有赋值都需要担心这一点。
　　特别是，通过解引用赋值会无条件 drop，在 `let` 中赋值则无条件不 drop：

```rust
let mut x = Box::new(0); // let 创建新变量，因此从不需要 drop
let y = &mut x;
*y = Box::new(1); // Deref 假设被引用对象已初始化，因此总是 drop
```

　　这只在覆盖先前已初始化的变量或其子字段时才是问题。

　　Rust 实际上在*运行时*追踪类型是否应被 drop。变量随初始化/未初始化切换，该变量的 *drop 标志*随之切换。当变量可能需要 drop 时，评估此标志决定是否 drop。

　　当然，值的初始化状态在程序每一点常可静态已知。若如此，编译器理论上可生成更高效代码！例如直线代码具有此类*静态 drop 语义*：

```rust
let mut x = Box::new(0); // x 未初始化；直接覆盖。
let mut y = x;           // y 未初始化；直接覆盖并使 x 未初始化。
x = Box::new(0);         // x 未初始化；直接覆盖。
y = x;                   // y 已初始化；Drop y，覆盖它，并使 x 未初始化！
                         // y 离开作用域；y 已初始化；Drop y！
                         // x 离开作用域；x 未初始化；什么都不做。
```

　　同样，所有分支对初始化行为一致的分支代码具有静态 drop 语义：

```rust
# let condition = true;
let mut x = Box::new(0);    // x 未初始化；直接覆盖。
if condition {
    drop(x)                 // x 被 move 出；使 x 未初始化。
} else {
    println!("{}", x);
    drop(x)                 // x 被 move 出；使 x 未初始化。
}
x = Box::new(0);            // x 未初始化；直接覆盖。
                            // x 离开作用域；x 已初始化；Drop x！
```

　　但如下代码*需要*运行时信息才能正确 Drop：

```rust
# let condition = true;
let x;
if condition {
    x = Box::new(0);        // x 未初始化；直接覆盖。
    println!("{}", x);
}
                            // x 离开作用域；x 可能未初始化；
                            // 检查标志！
```

　　当然，此例可轻易恢复静态 drop 语义：

```rust
# let condition = true;
if condition {
    let x = Box::new(0);
    println!("{}", x);
}
```

　　drop 标志在栈上追踪。
　　旧版 Rust 中，drop 标志藏在实现 `Drop` 的类型的隐藏字段里。
