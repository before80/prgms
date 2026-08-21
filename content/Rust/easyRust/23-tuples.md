+++
title = "23-元组"
date = 2026-08-21T12:46:00+08:00
weight = 24
type = "docs"
description = "元组 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_22.html](https://dhghomon.github.io/easy_rust/Chapter_22.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 元组

Rust中的元组使用`()`。我们已经见过很多空元组了，因为函数中的*nothing*实际上意味着一个空元组。

```text
fn do_something() {}
```

其实是它的简写:

```text
fn do_something() -> () {}
```

这个函数什么也得不到(一个空元组)，也不返回什么(一个空元组)。所以我们已经经常使用元组了。当你在一个函数中不返回任何东西时，你实际上返回的是一个空元组。

```rust
fn just_prints() {
    println!("I am printing"); // 加上 ; 表示返回空元组
}

fn main() {}
```

但是元组可以容纳很多东西，也可以容纳不同的类型。元组里面的元素也是用数字0、1、2等来做索引的，但要访问它们，你要用`.`而不是`[]`。让我们把一大堆类型放到一个元组中。

```rust
fn main() {
    let random_tuple = ("Here is a name", 8, vec!['a'], 'b', [8, 9, 10], 7.7);
    println!(
        "Inside the tuple is: First item: {:?}
Second item: {:?}
Third item: {:?}
Fourth item: {:?}
Fifth item: {:?}
Sixth item: {:?}",
        random_tuple.0,
        random_tuple.1,
        random_tuple.2,
        random_tuple.3,
        random_tuple.4,
        random_tuple.5,
    )
}
```

这个打印:

```text
Inside the tuple is: First item: "Here is a name"
Second item: 8
Third item: ['a']
Fourth item: 'b'
Fifth item: [8, 9, 10]
Sixth item: 7.7
```

这个元组的类型是 `(&str, i32, Vec<char>, char, [i32; 3], f64)`。


你可以使用一个元组来创建多个变量。看看这段代码。

```rust
fn main() {
    let str_vec = vec!["one", "two", "three"];
}
```

`str_vec`里面有三个元素。如果我们想把它们拉出来呢？这时我们可以使用元组。

```rust
fn main() {
    let str_vec = vec!["one", "two", "three"];

    let (a, b, c) = (str_vec[0], str_vec[1], str_vec[2]); // 分别叫作 a、b 和 c
    println!("{:?}", b);
}
```

这就打印出`"two"`，也就是`b`。这就是所谓的*解构*。这是因为首先变量是在结构体里面的，但是我们又做了`a`、`b`、`c`这些不是在结构体里面的变量。

如果你需要解构，但又不想要所有的变量，你可以使用`_`。

```rust
fn main() {
    let str_vec = vec!["one", "two", "three"];

    let (_, _, variable) = (str_vec[0], str_vec[1], str_vec[2]);
}
```

现在它只创建了一个叫`variable`的变量，但没有为其他值做变量。

还有很多集合类型，还有很多使用数组、vec和tuple的方法。我们也将学习更多关于它们的知识，但首先我们将学习控制流。
