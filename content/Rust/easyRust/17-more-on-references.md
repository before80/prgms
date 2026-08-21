+++
title = "17-关于引用的更多信息"
date = 2026-08-21T12:46:00+08:00
weight = 18
type = "docs"
description = "关于引用的更多信息 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_16.html](https://dhghomon.github.io/easy_rust/Chapter_16.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 关于引用的更多信息

引用在Rust中非常重要。Rust使用引用来确保所有的内存访问是安全的。我们知道，我们使用`&`来创建一个引用。

```rust
fn main() {
    let country = String::from("Austria");
    let ref_one = &country;
    let ref_two = &country;

    println!("{}", ref_one);
}
```

这样就会打印出`Austria`。

在代码中，`country`是一个`String`。然后我们创建了两个`country`的引用。它们的类型是`&String`，你说这是一个 "字符串的引用"。我们可以创建三个引用或者一百个对 `country` 的引用，这都没有问题。

但这是一个问题。

```rust
fn return_str() -> &str {
    let country = String::from("Austria");
    let country_ref = &country;
    country_ref // ⚠️
}

fn main() {
    let country = return_str();
}
```

`return_str()`函数创建了一个String，然后它创建了一个对String的引用。然后它试图返回引用。但是`country`这个String只活在函数里面，然后它就死了。一旦一个变量消失了，计算机就会清理内存，并将其用于其他用途。所以在函数结束后，`country_ref`引用的是已经消失的内存，这是不对的。Rust防止我们在这里犯内存的错误。

这就是我们上面讲到的 "拥有"类型的重要部分。因为你拥有一个`String`，你可以把它传给别人。但是如果 `&String` 的 `String` 死了，那么 `&String` 就会死掉，所以你不能把它的 "所有权"传给别人。
