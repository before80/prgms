+++
title = "3.6 无界生命周期"
date = 2026-08-06T17:08:00+08:00
weight = 16
type = "docs"
description = "无界生命周期及其危险性"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 无界生命周期


> 原文链接: [https://doc.rust-lang.org/nomicon/unbounded-lifetimes.html](https://doc.rust-lang.org/nomicon/unbounded-lifetimes.html)


　　Unsafe 代码常常凭空产生引用或生命周期。
　　这类生命周期以*无界*（unbounded）的形式出现。最常见的来源是对解引用后的裸指针取引用，由此得到的引用具有无界生命周期。这种生命周期会随上下文需要而「撑大」。事实上它比单纯变成 `'static` 更强大——例如 `&'static &'a T` 会类型检查失败，而无界生命周期却能按需完美适配为 `&'a &'a T`。不过对大多数意图和目的而言，无界生命周期可以视为 `'static`。

　　几乎没有任何引用真的是 `'static`，因此这很可能是错误的。`transmute` 和 `transmute_copy` 是另外两大「惯犯」。应尽可能尽快为有界生命周期加上约束，尤其跨越函数边界时。

　　给定一个函数，任何不来自输入的输出生命周期都是无界的。例如：

```rust,no_run
fn get_str<'a>(s: *const String) -> &'a str {
    unsafe { &*s }
}

fn main() {
    let soon_dropped = String::from("hello");
    let dangling = get_str(&soon_dropped);
    drop(soon_dropped);
    println!("Invalid str: {}", dangling); // Invalid str: gӚ_`
}
```

　　避免无界生命周期最简便的方法是在函数边界使用生命周期省略。若输出生命周期被省略，则它*必须*由某个输入生命周期约束。当然，它可能被*错误*的生命周期约束，但这通常只会导致编译错误，而非轻易破坏内存安全。

　　在函数内部，为生命周期加上约束更容易出错。最安全、最简便的方式是从带有有界生命周期的函数返回它。若这不可接受，可将引用放入具有特定生命周期的位置。遗憾的是，无法为函数中涉及的所有生命周期都命名。
