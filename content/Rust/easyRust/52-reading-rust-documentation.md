+++
title = "52-阅读 Rust 文档"
date = 2026-08-21T12:46:00+08:00
weight = 53
type = "docs"
description = "阅读 Rust 文档 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_51.html](https://dhghomon.github.io/easy_rust/Chapter_51.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 阅读 Rust 文档

知道如何阅读Rust中的文档是很重要的，这样你就可以理解其他人写的东西。这里有一些Rust文档中需要知道的事情。

## assert_eq!


你在做测试的时候看到`assert_eq!`是用的。你把两个元素放在函数里面，如果它们不相等，程序就会崩溃。下面是一个简单的例子，我们需要一个偶数。

```rust
fn main() {
    prints_number(56);
}

fn prints_number(input: i32) {
    assert_eq!(input % 2, 0); // 必须相等。
                              // 如果 number % 2 不是 0，就会 panic
    println!("The number is not odd. It is {}", input);
}
```

也许你没有任何计划在你的代码中使用`assert_eq!`，但它在Rust文档中随处可见。这是因为在一个文档中，你需要很大的空间来`println!`一切。另外，你会需要`Display`或`Debug`来打印你想打印的东西。这就是为什么文档中到处都有`assert_eq!`的原因。下面是这里的一个例子[https://doc.rust-lang.org/std/vec/struct.Vec.html](https://doc.rust-lang.org/std/vec/struct.Vec.html)，展示了如何使用Vec。

```rust
fn main() {
    let mut vec = Vec::new();
    vec.push(1);
    vec.push(2);

    assert_eq!(vec.len(), 2);
    assert_eq!(vec[0], 1);

    assert_eq!(vec.pop(), Some(2));
    assert_eq!(vec.len(), 1);

    vec[0] = 7;
    assert_eq!(vec[0], 7);

    vec.extend([1, 2, 3].iter().copied());

    for x in &vec {
        println!("{}", x);
    }
    assert_eq!(vec, [7, 1, 2, 3]);
}
```

在这些例子中，你可以只把`assert_eq!(a, b)`看成是在说 "a是b"。现在看看右边带有注释的同一个例子。注释显示了它的实际含义。

```rust
fn main() {
    let mut vec = Vec::new();
    vec.push(1);
    vec.push(2);

    assert_eq!(vec.len(), 2); // "vec 的长度是 2"
    assert_eq!(vec[0], 1); // "vec[0] 是 1"

    assert_eq!(vec.pop(), Some(2)); // "调用 .pop() 会得到 Some()"
    assert_eq!(vec.len(), 1); // "现在 vec 的长度是 1"

    vec[0] = 7;
    assert_eq!(vec[0], 7); // "Vec[0] 是 7"

    vec.extend([1, 2, 3].iter().copied());

    for x in &vec {
        println!("{}", x);
    }
    assert_eq!(vec, [7, 1, 2, 3]); // "现在 vec 是 [7, 1, 2, 3]"
}
```

## 搜索

Rust 文档的顶部栏是搜索栏。它在你输入时显示结果。当你往下翻时，你不能再看到搜索栏，但如果你按键盘上的**s**键，你可以再次搜索。所以在任何地方按**s**键可以让你马上搜索。

## [src] 按钮

通常一个方法、结构体等的代码不会是完整的。这是因为你通常不需要看到完整的源码就能知道它是如何工作的，而完整的代码可能会让人困惑。但如果你想知道更多，你可以点击[src]就可以看到所有的内容。例如，在`String`的页面上，你可以看到`.with_capacity()`的这个签名。

```rust
// 🚧
pub fn with_capacity(capacity: usize) -> String
```

好了，你输入一个数字，它给你一个`String`。这很简单，但也许我们很好奇，想看更多。如果你点击[src]你可以看到这个。

```rust
// 🚧
pub fn with_capacity(capacity: usize) -> String {
    String { vec: Vec::with_capacity(capacity) }
}
```

有趣的是，现在你可以看到，字符串是`Vec`的一种。而实际上一个`String`是一个`u8`字节的向量，这很有意思。你不需要知道，就可以使用`with_capacity`的方法，你只有点击[src]才能看到。所以如果文档没有太多细节，而你又想知道更多的话，点击[src]是个好主意。

## trait信息

trait文档的重要部分是左边的 "Required Methods"。如果你看到 "Required Methods"，可能意味着你必须自己编写方法。例如，对于 `Iterator`，你需要写 `.next()` 方法。而对于`From`，你需要写`.from()`方法。但是有些trait只需要一个**属性**就可以实现，比如我们在`#[derive(Debug)]`中看到的。`Debug`需要`.fmt()`方法，但通常你只需要使用`#[derive(Debug)]`，除非你想自己做。这就是为什么在`std::fmt::Debug`的页面上说 "一般来说，你应该直接派生出一个Debug实现"。
