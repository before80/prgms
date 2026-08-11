+++
title = "5.1 受检的未初始化"
date = 2026-08-06T17:08:00+08:00
weight = 28
type = "docs"
description = "MaybeUninit 等受检方式"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 受检的未初始化


> 原文链接: [https://doc.rust-lang.org/nomicon/checked-uninit.html](https://doc.rust-lang.org/nomicon/checked-uninit.html)


　　与 C 类似，Rust 中所有栈变量在显式赋值之前都是未初始化的。与 C 不同，Rust 静态阻止你在赋值前读取它们：

```rust,compile_fail
fn main() {
    let x: i32;
    println!("{}", x);
}
```

```text
  |
3 |     println!("{}", x);
  |                    ^ use of possibly uninitialized `x`
```

　　这基于基本分支分析：每个分支在首次使用前必须为 `x` 赋值。简言之，也说「`x` 已初始化」或「`x` 未初始化」。

　　有趣的是，若每个分支恰好赋值一次，Rust 不要求变量可变 即可延迟初始化。但分析不利用常量分析等。因此下面能编译：

```rust
fn main() {
    let x: i32;

    if true {
        x = 1;
    } else {
        x = 2;
    }

    println!("{}", x);
}
```

　　但下面不能：

```rust,compile_fail
fn main() {
    let x: i32;
    if true {
        x = 1;
    }
    println!("{}", x);
}
```

```text
  |
6 |     println!("{}", x);
  |                    ^ use of possibly uninitialized `x`
```

　　而下面可以：

```rust
fn main() {
    let x: i32;
    if true {
        x = 1;
        println!("{}", x);
    }
    // 不关心未初始化分支，因为那些分支不用该值
}
```

　　当然，虽然分析不考虑实际值，但对依赖和控制流有相对深入的理解。例如下面可行：

```rust
let x: i32;

loop {
    // Rust 不理解此分支会无条件执行，因为它依赖实际值。
    if true {
        // 但它理解只会执行一次，因为我们无条件 break。
        // 因此 `x` 不必标记为 mutable。
        x = 0;
        break;
    }
}
// 它还知道没有 break 就不可能到这里。
// 因此这里 `x` 必已初始化！
println!("{}", x);
```

　　若从变量 move 出值，且值类型不是 `Copy`，该变量在逻辑上变为未初始化。即：

```rust
fn main() {
    let x = 0;
    let y = Box::new(0);
    let z1 = x; // x 仍有效，因为 i32 是 Copy
    let z2 = y; // y 在逻辑上未初始化，因为 Box 不是 Copy
}
```

　　但此例中重新赋值 `y` *会*要求 `y` 标记为 mutable，因为 Safe Rust 程序可观察到 `y` 的值变了：

```rust
fn main() {
    let mut y = Box::new(0);
    let z = y; // y 在逻辑上未初始化，因为 Box 不是 Copy
    y = Box::new(1); // 重新初始化 y
}
```

　　否则就像 `y` 是全新变量。
