+++
title = "7 特殊生命周期"
date = 2026-08-23T16:26:00+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_7.html](https://tfpk.github.io/lifetimekata/chapter_7.html)

Rust 中有两个特殊的生命周期。值得把两者都讨论一下：

 - `'static`
 - `'_`（隐式生命周期）

# `static` 生命周期

程序中的某些东西保证会永远存在。最常见的原因是
它们的信息打包在你的二进制文件里。例如，当你写
这样的程序时：

```rust
fn main() {
    let my_text = "Hello World";
}
```

文本 `"Hello World"` 实际上在编译后的二进制文件中的某个位置。这意味着
对它的引用始终有效，因为只要程序
在运行，这段文本就一直在那里。

因此，如果我们要描述这段文本的类型，会说它是 `&'static str`。

同样，任何对常量的引用也可以是 `&'static`。例如：

```rust

const SOME_COORDINATE: (i32, i32) = (7, 4);

fn main() {
    let static_reference: &'static (i32, i32) = &SOME_COORDINATE;
}
```

# `'_` 生命周期（匿名生命周期、占位生命周期）

隐式生命周期告诉 Rust 自己推断生命周期。
这个生命周期在三个地方很有用：

 - 简化 `impl` 块
 - 消费/返回需要生命周期的类型时
 - 编写包含引用的 trait 对象时。

## 简化 Impl 块

假设你正在实现一个计数器结构体，看起来像这样：

```rust
struct Counter<'a> {
    counter: &'a mut i32
}

impl<'a> Counter<'a> {
    fn increment(&mut self) {
        *self.counter += 1;
    }
}

fn main() {
    let mut num = 0;
    
    let mut counter = Counter { counter: &mut num };
    counter.increment();
    
    println!("{num}"); // 打印 1
    
}
```

这没问题，但你会注意到 `impl` 块实际上并没有在任何地方使用 `'a` 生命周期。
因此，我们可以简化，改为写下面这样：

```rust
impl Counter<'_> {
    fn increment(&mut self) {
        self.counter += 1;
    }
}
```

上面两个 `impl` 块的含义相同，只是参数稍少一些。

## 返回结构体和枚举

建议在返回包含引用的
结构体/枚举时使用。你可以写这样的代码：

```rust

struct StrWrap<'a>(&'a str);

fn make_wrapper(string: &str) -> StrWrap {
    StrWrap(string)
}

# fn main() {}
```

但这种写法不再推荐，当你添加
`#![deny(rust_2018_idioms)]` 注解时就会看到错误：

```text
error: hidden lifetime parameters in types are deprecated
 --> src/main.rs:8:34
  |
_ | fn make_wrapper(string: &str) -> StrWrap {
  |                                  ^^^^^^^ expected lifetime parameter
  |
note: the lint level is defined here
 --> src/main.rs:1:9
  |
_ | #![deny(rust_2018_idioms)]
  |         ^^^^^^^^^^^^^^^^
  = note: `#[deny(elided_lifetimes_in_paths)]` implied by `#[deny(rust_2018_idioms)]`
help: indicate the anonymous lifetime
  |
_ | fn make_wrapper(string: &str) -> StrWrap<'_> {
  |                                         ++++
```

按照提示修改后，会更清楚地表明 `StrWrap` *确实*包含引用，
但编译器应该自己推断出来。

## Trait 对象上的生命周期

详见[第 10 章：trait 生命周期边界脚注](../10-footnote-trait-lifetime-bounds/)。

# 生命周期边界

生命周期边界并不常用，所以我们不会在练习中花大篇幅介绍。
除非你真的想了解细节，否则可以跳过本节。

简而言之，它们允许你指定一个生命周期应该比另一个活得更久。要指定边界，使用 where 子句，例如
`where 'a: 'b`。

引用 Rust 参考手册：

> 生命周期边界可以应用于类型或其他生命周期。
> 边界 `'a: 'b` 通常读作 `'a` *比* `'b` *活得更久*。
> `'a: 'b` 意味着 `'a` 至少与 `'b` 一样长，因此只要 `&'b ()` 有效，`&'a ()` 就有效。

> ```rust
> fn f<'a, 'b>(x: &'a i32, mut y: &'b i32) where 'a: 'b {
>     y = x;                      // 因为 'a: 'b，所以 &'a i32 是 &'b i32 的子类型
>     let r: &'b &'a i32 = &&0;   // 因为 'a: 'b，所以 &'b &'a i32 是良构的
> }
> ```

> `T: 'a` 意味着 `T` 的所有生命周期参数都比 `'a` 活得更久。
> 例如，如果 `'a` 是一个无约束的生命周期参数，那么 `i32: 'static` 和 `&'static str: 'a` 满足条件，但 `Vec<&'a ()>: 'static` 不满足。


# 练习

你得到了一段代码，其中多处使用了生命周期 `'a` 和 `'b`。
所有这些生命周期都可以替换为 `'_` 或 `'static`。

你的任务是把 `'a` 和 `'b` 的每一次出现替换为
`'_` 或 `'static`，去掉多余的生命周期声明，并确保
代码仍能编译。

### 关于过时信息的脚注
 
Rust 版本指南以前有一节
关于匿名生命周期的内容。现在 Google 上最热门的结果
是[这篇文章](https://yegeun542.github.io/rust-edition-guide-ko/rust-2018/ownership-and-lifetimes/the-anonymous-lifetime.html)，但我建议忽略它，因为其中的信息已经过时。
