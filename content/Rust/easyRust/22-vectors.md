+++
title = "22-向量"
date = 2026-08-21T12:46:00+08:00
weight = 23
type = "docs"
description = "向量 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_21.html](https://dhghomon.github.io/easy_rust/Chapter_21.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 向量

就像我们有`&str`和`String`一样，我们有数组和向量。数组的功能少了就快，向量的功能多了就慢。(当然，Rust的速度一直都是非常快的，所以向量并不慢，只是比数组慢*一点*)。类型写成`Vec`，你也可以直接叫它 "vec"。

向量的声明主要有两种方式。一种是像`String`一样使用`new`:

```rust
fn main() {
    let name1 = String::from("Windy");
    let name2 = String::from("Gomesy");

    let mut my_vec = Vec::new();
    // 如果现在运行程序，编译器会报错。
    // 它还不知道 vec 的类型。

    my_vec.push(name1); // 现在它知道了：是 Vec<String>
    my_vec.push(name2);
}
```

你可以看到`Vec`里面总是有其他东西，这就是`<>`(角括号)的作用。`Vec<String>`是一个有一个或多个`String`的向量。你还可以在里面有更多的类型。比如说

- `Vec<(i32, i32)>` 这是一个 `Vec` 其中每个元素是一个元组。`(i32, i32)`.
- `Vec<Vec<String>>`这是一个`Vec`，其中有`Vec`的`Strings`。比如说你想把你喜欢的书保存为`Vec<String>`。然后你再用另一本书来做，就会得到另一个`Vec<String>`。为了保存这两本书，你会把它们放入另一个`Vec`中，这就是`Vec<Vec<String>>`。

与其使用 `.push()` 让 Rust 决定类型，不如直接声明类型。

```rust
fn main() {
    let mut my_vec: Vec<String> = Vec::new(); // 编译器已经知道类型
                                              // 所以不会报错。
}
```

你可以看到，向量中的元素必须具有相同的类型。

另一个创建向量的简单方法是使用 `vec!` 宏。它看起来像一个数组声明，但前面有 `vec!`。

```rust
fn main() {
    let mut my_vec = vec![8, 10, 10];
}
```

类型是`Vec<i32>`。你称它为 "i32的Vec"。而`Vec<String>`是 "String的Vec"。`Vec<Vec<String>>`是 "String的Vec的Vec"。

你也可以对一个向量进行分片，就像在数组中一样。

```rust
fn main() {
    let vec_of_ten = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    // 除了加了 vec!，其余与上面相同。
    let three_to_five = &vec_of_ten[2..5];
    let start_at_two = &vec_of_ten[1..];
    let end_at_five = &vec_of_ten[..5];
    let everything = &vec_of_ten[..];

    println!("Three to five: {:?},
start at two: {:?}
end at five: {:?}
everything: {:?}", three_to_five, start_at_two, end_at_five, everything);
}
```

因为Vector比数组慢，我们可以用一些方法让它更快。一个vec有一个**容量**，也就是给向量的空间。当你在向量上推送一个新的元素时，它会越来越接近容量。然后，如果你超过了容量，它将使其容量翻倍，并将元素复制到新的空间。这就是所谓的重新分配。我们将使用一种名为`.capacity()`的方法来查看向量的容量，在我们向它添加元素时。

例如，我们将使用名为`.capacity()`的方法来观察一个向量的容量。

```rust
fn main() {
    let mut num_vec = Vec::new();
    println!("{}", num_vec.capacity()); // 0 个元素：打印 0
    num_vec.push('a'); // 添加一个字符
    println!("{}", num_vec.capacity()); // 1 个元素：打印 4。只有 1 项的 Vec 容量总是从 4 开始
    num_vec.push('a'); // 再添加一个
    num_vec.push('a'); // 再添加一个
    num_vec.push('a'); // 再添加一个
    println!("{}", num_vec.capacity()); // 4 个元素：仍打印 4。
    num_vec.push('a'); // 再添加一个
    println!("{}", num_vec.capacity()); // 打印 8。我们有 5 个元素，但容量从 4 翻倍到 8 以腾出空间
}
```

这个打印:

```text
0
4
4
8
```

所以这个向量有两次重分配: 0到4，4到8。我们可以让它更快:

```rust
fn main() {
    let mut num_vec = Vec::with_capacity(8); // 给定容量 8
    num_vec.push('a'); // 添加一个字符
    println!("{}", num_vec.capacity()); // 打印 8
    num_vec.push('a'); // 再添加一个
    println!("{}", num_vec.capacity()); // 打印 8
    num_vec.push('a'); // 再添加一个
    println!("{}", num_vec.capacity()); // 打印 8。
    num_vec.push('a'); // 再添加一个
    num_vec.push('a'); // 再添加一个 // 现在有 5 个元素
    println!("{}", num_vec.capacity()); // 仍是 8
}
```

这个向量有0个重分配，这是比较好的。所以如果你认为你知道你需要多少元素，你可以使用`Vec::with_capacity()`来使它更快。

你记得你可以用`.into()`把`&str`变成`String`。你也可以用它把一个数组变成`Vec`。你必须告诉 `.into()` 你想要一个 `Vec`，但你不必选择 `Vec` 的类型。如果你不想选择，你可以写`Vec<_>`。

```rust
fn main() {
    let my_vec: Vec<u8> = [1, 2, 3].into();
    let my_vec2: Vec<_> = [9, 0, 10].into(); // Vec<_> 表示“由编译器帮我选 Vec 的类型”
                                             // Rust 会选择 Vec<i32>
}
```
