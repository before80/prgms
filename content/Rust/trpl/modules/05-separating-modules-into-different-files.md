+++
title = "7.5 将模块拆分到不同文件"
date = 2026-08-05T08:44:00+08:00
weight = 32
type = "docs"
description = "把模块定义拆到多个文件中以简化导航"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 将模块拆分到不同文件


> 原文链接: [https://doc.rust-lang.org/stable/book/ch07-05-separating-modules-into-different-files.html](https://doc.rust-lang.org/stable/book/ch07-05-separating-modules-into-different-files.html)


## 将模块拆分到不同文件

　　到目前为止，本章的例子都是在一个文件里定义多个模块。当模块变大时，你可能想把它们的定义挪到单独的文件里，好让代码更容易浏览。

　　例如，我们从示例 7-17 中有多个餐馆模块的代码开始。我们会把模块提取到文件中，而不是全部定义在 crate 根文件里。此例中 crate 根文件是 *src/lib.rs*，但对 crate 根为 *src/main.rs* 的二进制 crate，同样的步骤也适用。

　　首先，把 `front_of_house` 模块提取到它自己的文件。去掉 `front_of_house` 模块花括号里的代码，只留下 `mod front_of_house;` 声明，这样 *src/lib.rs* 就变成示例 7-21 所示的样子。注意，在创建示例 7-22 中的 *src/front_of_house.rs* 文件之前，这段代码无法编译。

**文件名：`src/lib.rs`**
```rust
mod front_of_house;

pub use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

**示例 7-21：声明主体将位于 *src/front_of_house.rs* 的 `front_of_house` 模块**

　　接下来，把原先花括号里的代码放到名为 *src/front_of_house.rs* 的新文件中，如示例 7-22 所示。编译器之所以知道去这个文件里找，是因为它在 crate 根遇到了名为 `front_of_house` 的模块声明。

**文件名：`src/front_of_house.rs`**
```rust
pub mod hosting {
    pub fn add_to_waitlist() {}
}
```

**示例 7-22：*src/front_of_house.rs* 中 `front_of_house` 模块内部的定义**

　　注意，你只需在模块树中用 `mod` 声明*加载一次*某个文件。一旦编译器知道该文件是项目的一部分（并根据你放置 `mod` 语句的位置知道代码在模块树中的位置），项目中的其他文件就应该用指向其声明位置的路径来引用已加载文件中的代码，正如[「路径：引用模块树中的项」][paths]一节所讲。换句话说，`mod` *不是*你在其他编程语言里可能见过的那种 “include” 操作。

　　接下来，我们把 `hosting` 模块也提取到自己的文件。过程略有不同，因为 `hosting` 是 `front_of_house` 的子模块，而不是根模块的子模块。我们会把 `hosting` 的文件放进一个按它在模块树中祖先命名的新目录里，此例中是 *src/front_of_house*。

　　开始移动 `hosting` 时，先把 *src/front_of_house.rs* 改成只包含 `hosting` 模块的声明：

**文件名：`src/front_of_house.rs`**
```rust
pub mod hosting;
```

　　然后创建 *src/front_of_house* 目录和 *hosting.rs* 文件，用来容纳 `hosting` 模块中的定义：

**文件名：`src/front_of_house/hosting.rs`**
```rust
pub fn add_to_waitlist() {}
```

　　若我们把 *hosting.rs* 放在 *src* 目录下，编译器就会期望 *hosting.rs* 的代码属于在 crate 根声明的 `hosting` 模块，而不是作为 `front_of_house` 的子模块。编译器关于「哪个模块的代码去哪个文件找」的规则，让目录与文件能更紧密地对应模块树。

> ### 备选文件路径 {#alternate-file-paths}
>
> 到目前为止我们讲的是 Rust 编译器最惯用的文件路径，但 Rust 也支持一种更旧的文件路径风格。对于在 crate 根声明的名为 `front_of_house` 的模块，编译器会在这些位置查找模块代码：
>
> - *src/front_of_house.rs*（我们已介绍的方式）
> - *src/front_of_house/mod.rs*（旧风格，仍然支持）
>
> 对于作为 `front_of_house` 子模块、名为 `hosting` 的模块，编译器会在这些位置查找：
>
> - *src/front_of_house/hosting.rs*（我们已介绍的方式）
> - *src/front_of_house/hosting/mod.rs*（旧风格，仍然支持）
>
> 若对同一模块同时使用两种风格，会得到编译错误。同一项目里对不同模块混用两种风格是允许的，但可能让浏览项目的人感到困惑。
>
> 使用名为 *mod.rs* 的文件那种风格的主要缺点是：项目里可能出现许多同名的 *mod.rs*，在编辑器里同时打开时容易搞混。

　　我们已经把每个模块的代码移到了单独的文件，模块树本身保持不变。即便定义位于不同文件中，`eat_at_restaurant` 里的函数调用也无需任何修改即可工作。这种技巧让你在模块变大时可以把它们挪到新文件里。

　　注意，*src/lib.rs* 中的 `pub use crate::front_of_house::hosting` 语句也没有改变，而且 `use` 也不会影响哪些文件会作为 crate 的一部分被编译。`mod` 关键字声明模块，Rust 会在与模块同名的文件中查找属于该模块的代码。

## 小结

　　Rust 允许你把一个包拆成多个 crate，再把一个 crate 拆成多个模块，从而可以从一个模块引用另一个模块中定义的项。你可以指定绝对路径或相对路径。这些路径可以用 `use` 语句引入作用域，以便在该作用域内多次使用该项时写更短的路径。模块代码默认是私有的，但可以在定义前加上 `pub` 关键字使其公有。

　　下一章，我们会看看标准库里一些你可以在整理好的代码中使用的集合数据结构。

[paths]: /trpl/modules/03-paths-for-referring-to-an-item-in-the-module-tree/
