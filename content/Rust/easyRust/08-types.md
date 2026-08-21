+++
title = "08-类型"
date = 2026-08-21T12:46:00+08:00
weight = 9
type = "docs"
description = "类型 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_7.html](https://dhghomon.github.io/easy_rust/Chapter_7.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 类型

Rust有很多类型，让你可以处理数字、字符等。有些类型很简单，有些类型比较复杂，你甚至可以创建自己的类型。

## 原始类型

Rust有简单的类型，这些类型被称为**原始类型**(原始=非常基本)。我们将从整数和`char`(字符)开始。整数是没有小数点的整数。整数有两种类型。

- 有符号的整数
- 无符号整数

符号是指`+`(加号)和`-`(减号)，所以有符号的整数可以是正数，也可以是负数(如+8，-8)。但无符号整数只能是正数，因为它们没有符号。

有符号的整数是 `i8`, `i16`, `i32`, `i64`, `i128`, 和 `isize`。

无符号的整数是 `u8`, `u16`, `u32`, `u64`, `u128`, 和 `usize`。

i或u后面的数字表示该数字的位数，所以位数多的数字可以大一些。8位=一个字节，所以`i8`是一个字节，`i64`是8个字节，以此类推。尺寸较大的数字类型可以容纳更大的数字。例如，`u8`最多可以容纳255，但`u16`最多可以容纳65535。而`u128`最多可以容纳340282366920938463463374607431768211455。

那么什么是`isize`和`usize`呢？这表示你电脑的位数。(你的电脑上的位数叫做你电脑的**架构**)。所以32位计算机上的`isize`和`usize`就像`i32`和`u32`，64位计算机上的`isize`和`usize`就像`i64`和`u64`。

整数类型不同的原因有很多。其中一个原因是计算机性能:较小的字节数处理速度更快。例如，数字-10作为`i8`是`11110110`，但作为`i128`是`11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110110`。但这里还有一些其他用法。

Rust中的字符叫做`char`. 每一个`char`都有一个数字:字母`A`是数字65，而字符`友`(中文的 "朋友")是数字21451。这个数字列表被称为 "Unicode"。Unicode对使用较多的字符使用较小的数字，如A到Z，或0到9的数字，或空格。

```rust
fn main() {
    let first_letter = 'A';
    let space = ' '; // ' ' 里的空格也是 char
    let other_language_char = 'Ꮔ'; // 多亏 Unicode，切罗基文等其他语言也能正常显示
    let cat_face = '😺'; // emoji 也是 char
}
```

使用最多的字符的数字小于256，它们可以装进`u8`。记住，`u8`是0加上255以内的所有数字，总共256个。这意味着 Rust 可以使用 `as` 将 `u8` 安全地 **cast**成 `char`。("把 `u8` cast成 `char`"意味着 "把 `u8` 假装成 `char`")

用 `as` cast是有用的，因为 Rust 是非常严格的。它总是需要知道类型。
 而不会让你同时使用两种不同的类型，即使它们都是整数。例如，这将无法工作:

```rust
fn main() { // main() 是 Rust 程序开始运行的地方。代码写在 {}（花括号）里

    let my_number = 100; // 我们没写整数类型，
                         // 所以 Rust 会选 i32。如果你不指定
                         // 其他类型，Rust 总是
                         // 把整数选成 i32

    println!("{}", my_number as char); // ⚠️
}
```

原因是这样的:

```text
error[E0604]: only `u8` can be cast as `char`, not `i32`
 --> src\main.rs:3:20
  |
3 |     println!("{}", my_number as char);
  |                    ^^^^^^^^^^^^^^^^^
```

幸运的是，我们可以用`as`轻松解决这个问题。我们不能把`i32`转成`char`，但我们可以把`i32`转成`u8`，然后把`u8`转换成`char`。所以在一行中，我们使用 `as` 将 my_number 变为 `u8`，再将其变为 `char`。现在可以编译了。

```rust
fn main() {
    let my_number = 100;
    println!("{}", my_number as u8 as char);
}
```

它打印的是`d`，因为那是100对应的`char`。

然而，更简单的方法是告诉 Rust `my_number` 是 `u8`。下面是你的做法。

```rust
fn main() {
    let my_number: u8 = 100; // 把 my_number 改成 my_number: u8
    println!("{}", my_number as char);
}
```

所以这就是Rust中所有不同数字类型的两个原因。这里还有一个原因:`usize`是Rust用于*索引*的大小。(索引的意思是 "哪项是第一"，"哪项是第二"等等)`usize`是索引的最佳大小，因为:

- 索引不能是负数，所以它需要是一个带u的数字
- 它应该是大的，因为有时你需要索引很多东西，但。
- 不可能是u64，因为32位电脑不能使用u64。

所以Rust使用了`usize`，这样你的计算机就可以得到它能读到的最大的数字进行索引。



我们再来了解一下`char`。你看到`char`总是一个字符，并且使用`''`而不是`""`。

所有的 `字符` 都使用4个字节的内存，因为4个字节足以容纳任何种类的字符:
- 基本字母和符号通常需要4个字节中的1个：`a b 1 2 + - = $ @`
- 其他字母，如德语的 Umlauts 或重音，需要4个字节中的2个： `ä ö ü ß è é à ñ`
- 韩文、日文或中文字符需要3或4个字节： `国 안 녕`

当使用字符作为字符串的一部分时，字符串被编码以使用每个字符所需的最小内存量。

我们可以用`.len()`来看一下。

```rust
fn main() {
    println!("Size of a char: {}", std::mem::size_of::<char>()); // 4 字节
    println!("Size of string containing 'a': {}", "a".len()); // .len() 给出字符串的字节大小
    println!("Size of string containing 'ß': {}", "ß".len());
    println!("Size of string containing '国': {}", "国".len());
    println!("Size of string containing '𓅱': {}", "𓅱".len());
}
```

这样打印出来。

```text
Size of a char: 4
Size of string containing 'a': 1
Size of string containing 'ß': 2
Size of string containing '国': 3
Size of string containing '𓅱': 4
```

可以看到，`a`是一个字节，德文的`ß`是两个字节，日文的`国`是三个字节，古埃及的`𓅱`是4个字节。

```rust
fn main() {
    let slice = "Hello!";
    println!("Slice is {} bytes.", slice.len());
    let slice2 = "안녕!"; // 韩语的「你好」
    println!("Slice2 is {} bytes.", slice2.len());
}
```

这个打印:

```text
Slice is 6 bytes.
Slice2 is 7 bytes.
```

`slice`的长度是6个字符，6个字节，但`slice2`的长度是3个字符，7个字节。

如果`.len()`给出的是以字节为单位的大小，那么以字符为单位的大小呢？这些方法我们后面会学习，但你只要记住`.chars().count()`就可以了。`.chars().count()` 将你写的东西变成字符，然后计算有多少个字符。


```rust
fn main() {
    let slice = "Hello!";
    println!("Slice is {} bytes and also {} characters.", slice.len(), slice.chars().count());
    let slice2 = "안녕!";
    println!("Slice2 is {} bytes but only {} characters.", slice2.len(), slice2.chars().count());
}
```

这就打印出来了。

```text
Slice is 6 bytes and also 6 characters.
Slice2 is 7 bytes but only 3 characters.
```
