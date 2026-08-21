+++
title = "02-变量"
date = 2026-08-18T08:45:00+08:00
weight = 104
type = "docs"
description = "变量 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/variables.html](https://doc.rust-lang.org/reference/variables.html)

r[variable]
# 变量

r[variable.intro]
*变量*是栈帧的组成部分，可以是具名函数参数、匿名[临时值][temporary]，或具名局部变量。

r[variable.local]
*局部变量*（或*栈局部*分配）直接持有一个值，分配在栈的内存中。该值是栈帧的一部分。

r[variable.local-mut]
除非另行声明，局部变量是不可变的。例如：`let mut x = ...`。

r[variable.param-mut]
除非用 `mut` 声明，函数参数是不可变的。`mut` 关键字仅作用于紧随其后的参数。例如：`|mut x, y|` 与 `fn f(mut x: Box<i32>, y: Box<i32>)` 声明一个可变变量 `x` 与一个不可变变量 `y`。

r[variable.init]
局部变量在分配时不会被初始化。相反，在进入栈帧时，该帧中的全部局部变量以未初始化状态分配。函数内后续语句可能初始化也可能不初始化这些局部变量。只有在所有可达控制流路径上都已初始化之后，局部变量才能被使用。

在下一个例子中，`init_after_if` 在 [`if` 表达式][`if` expression]之后已初始化，而 `uninit_after_if` 则未初始化，因为它在 `else` 分支中未被初始化。

```rust
## fn random_bool() -> bool { true }
fn initialization_example() {
    let init_after_if: ();
    let uninit_after_if: ();

    if random_bool() {
        init_after_if = ();
        uninit_after_if = ();
    } else {
        init_after_if = ();
    }

    init_after_if; // 可以
    // uninit_after_if; // 错误：使用可能未初始化的 `uninit_after_if`
}
```

[`if` expression]: expressions/if-expr.md#if-expressions
[temporary]: ../statements-and-expressions/02-expressions/#temporaries
