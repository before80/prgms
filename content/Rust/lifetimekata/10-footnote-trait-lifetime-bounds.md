+++
title = "10 trait 生命周期边界脚注"
date = 2026-08-23T16:26:00+08:00
weight = 12
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_10.html](https://tfpk.github.io/lifetimekata/chapter_10.html)

在第 7 章中，我们讨论了占位生命周期（`'_`）。我们说过
有三种使用方式：

 - 简化 `impl` 块
 - 在消费/返回需要生命周期的类型时
 - 编写包含引用的 trait 对象。

在第一种情况下，我们看到匿名生命周期只是简化了
我们需要写的内容。

在第二种情况下，我们看到 Rust 建议我们使用它，但
我们并*不必须*使用——生命周期省略会达到我们想要的效果。

看起来生命周期省略本应满足我们需求、
但实际上除非使用 `'_` 否则做不到的情况，就是 trait 对象。
本章将说明 trait 对象与生命周期如何协同工作。

我们先搭建一个简单的例子：

```rust
trait Bool {
    fn truthiness(&self) -> bool;
}

struct True();
impl Bool for True {
    fn truthiness(&self) -> bool {
        true
    }
}

struct False();
impl Bool for False {
    fn truthiness(&self) -> bool {
        false
    }
}

fn get_bool(b: bool) -> Box<dyn Bool> {
    if b == true {
        Box::new(True())
    } else {
        Box::new(False())
    }
}

fn main() {
    let my_bool = true;
    let my_dyn = get_bool(my_bool);

    println!("{}", my_dyn.truthiness());
}
```

明确一下，这里我们创建了两个结构体，分别表示
`true` 和 `false`。它们都实现了 `Bool` trait，该 trait 有
`truthiness` 函数，返回 `true` 或 `false`。

`get_bool` 函数根据传入的是
`true` 还是 `false`，返回一个装箱的 `Bool` trait 对象。

重要的是要意识到，由于 trait 对象可能包含引用（也可能不包含，或包含任意数量的引用），
所有 trait 对象都有生命周期。
即使该 trait 的所有实现者都不包含引用，这一点也成立。{{footnote:https://doc.rust-lang.org/reference/types/trait-object.html#trait-object-lifetime-bounds}}

因此，既然我们需要为 trait 对象关联一个生命周期，我们可能会
认为可以依赖生命周期省略。但生命周期省略
对我们的 `get_bool` 函数会怎么工作？没有输入引用，那么
应该给 trait 对象什么输出生命周期？生命周期省略在这里帮不上
我们。

于是，在 RFC 599 和 RFC 1156 中，trait 对象生命周期的规则被修改了。
这些规则很复杂，最好参考[参考文档中的说明](https://doc.rust-lang.org/reference/lifetime-elision.html#default-trait-object-lifetimes)，
但就 `get_bool` 而言，这意味着为 `dyn Bool` 推断出的生命周期是
`'static`。

现在我们稍微修改一下例子，让结构体包含一个
对 bool 的引用：

```rust
trait Bool {
    fn truthiness(&self) -> bool;
}

// 改动 1：在此处添加 &'a bool
struct True<'a>(&'a bool);
impl<'a> Bool for True<'a> {
    fn truthiness(&self) -> bool {
        true
    }
}

// 改动 2：在此处添加 &'a bool
struct False<'a>(&'a bool);
impl<'a> Bool for False<'a> {
    fn truthiness(&self) -> bool {
        false
    }
}

fn get_bool(b: &bool) -> Box<dyn Bool> {
    if *b == true {
        Box::new(True(b))
    } else {
        Box::new(False(b))
    }
}

// 改动 3：更新 main
fn main() {
    let my_dyn = {
        let my_bool = true;
        get_bool(&my_bool)
        // my_bool 在此处被 drop，因此我们返回的 trait 对象
        // 含有悬垂引用。
    };
    println!("{}", my_dyn.truthiness());
}
```

现在，我们会得到一个错误：

```text
error: lifetime may not live long enough
  --> src/main.rs:22:5
   |
21 |   fn get_bool(b: &bool) -> Box<dyn Bool> {
   |                  - let's call the lifetime of this reference `'1`
22 | /     if *b == true {
23 | |         Box::new(True(b))
24 | |     } else {
25 | |         Box::new(False(b))
26 | |     }
   | |_____^ returning this value requires that `'1` must outlive `'static`
   |
help: to declare that the trait object captures data from argument `b`, you can add an explicit `'_` lifetime bound
   |
21 | fn get_bool(b: &bool) -> Box<dyn Bool + '_> {
   |                                       ++++

error: could not compile __ due to previous error

```

尽管按照生命周期省略，`get_bool` 最终应得到类似
`fn get_bool<'elided>(b: &'elided bool) -> Box<dyn Bool +
'elided>` 的签名，但实际上并非如此。trait 对象的特殊规则意味着
实际签名是：`fn get_bool<'elided>(b: &'elided bool) -> Box<dyn Bool +
'static>`。那个 `'static` 边界是不正确的。

因此，我们需要 `'_` 边界（正如这条错误信息告诉我们的），以告知 Rust 应使用
正常的生命周期省略规则，而不是 trait 对象的
特殊规则。
