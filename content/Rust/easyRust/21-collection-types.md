+++
title = "21-集合类型"
date = 2026-08-21T12:46:00+08:00
weight = 22
type = "docs"
description = "集合类型 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_20.html](https://dhghomon.github.io/easy_rust/Chapter_20.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 集合类型

Rust有很多类型用于创建集合。当你需要在一个地方有多个值时，就可以使用集合。例如，你可以在一个变量中包含你所在国家的所有城市的信息。我们先从数组开始，数组的速度最快，但功能也最少。它们在这方面有点像`&str`。

## 数组

数组是方括号内的数据。`[]`. 数组:

- 不能改变其大小。
- 必须只包含相同的类型。

但是，它们的速度非常快。

数组的类型是:`[type; number]`。例如，`["One", "Two"]`的类型是`[&str; 2]`。这意味着，即使这两个数组也有不同的类型。

```rust
fn main() {
    let array1 = ["One", "Two"]; // 这个类型是 [&str; 2]
    let array2 = ["One", "Two", "Five"]; // 而这个类型是 [&str; 3]。不同类型！
}
```

这里有一个很好的提示:要想知道一个变量的类型，你可以通过给编译器下坏指令来 "询问"它。比如说

```rust
fn main() {
    let seasons = ["Spring", "Summer", "Autumn", "Winter"];
    let seasons2 = ["Spring", "Summer", "Fall", "Autumn", "Winter"];
    seasons.ddd(); // ⚠️
    seasons2.thd(); // ⚠️ 同样
}
```

编译器说:"什么？seasons没有`.ddd()`的方法，seasons2也没有`.thd()`的方法！！"你可以看到:

```text
error[E0599]: no method named `ddd` found for array `[&str; 4]` in the current scope
 --> src\main.rs:4:13
  |
4 |     seasons.ddd(); // 
  |             ^^^ method not found in `[&str; 4]`

error[E0599]: no method named `thd` found for array `[&str; 5]` in the current scope
 --> src\main.rs:5:14
  |
5 |     seasons2.thd(); // 
  |              ^^^ method not found in `[&str; 5]`
```

所以它告诉你`` method not found in `[&str; 4]` ``，这就是类型。

如果你想要一个数值都一样的数组，你可以这样声明。

```rust
fn main() {
    let my_array = ["a"; 10];
    println!("{:?}", my_array);
}
```

这样就打印出了`["a", "a", "a", "a", "a", "a", "a", "a", "a", "a"]`。

这个方法经常用来创建缓冲区。例如，`let mut buffer = [0; 640]`创建一个640个零的数组。然后我们可以将零改为其他数字，以便添加数据。

你可以用[]来索引(获取)数组中的条目。第一个条目是[0]，第二个是[1]，以此类推。

```rust
fn main() {
    let my_numbers = [0, 10, -20];
    println!("{}", my_numbers[1]); // 打印 10
}
```

你可以得到一个数组的一个片断(一块)。首先你需要一个&，因为编译器不知道大小。然后你可以使用`..`来显示范围。

例如，让我们使用这个数组。`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`.

```rust
fn main() {
    let array_of_ten = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let three_to_five = &array_of_ten[2..5];
    let start_at_two = &array_of_ten[1..];
    let end_at_five = &array_of_ten[..5];
    let everything = &array_of_ten[..];

    println!("Three to five: {:?}, start at two: {:?}, end at five: {:?}, everything: {:?}", three_to_five, start_at_two, end_at_five, everything);
}
```

记住这一点。

- 索引号从0开始(不是1)
- 索引范围是**不包含的**(不包括最后一个数字)。

所以`[0..2]`是指第一个指数和第二个指数(0和1)。或者你也可以称它为 "零点和第一"指数。它没有第三项，也就是索引2。

你也可以有一个**包含的**范围，这意味着它也包括最后一个数字。要做到这一点。
 添加`=`，写成`..=`，而不是`..`。所以，如果你想要第一项、第二项和第三项，可以写成`[0..=2]`，而不是`[0..2]`。
