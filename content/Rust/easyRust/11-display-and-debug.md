+++
title = "11-显示和调试"
date = 2026-08-21T12:46:00+08:00
weight = 12
type = "docs"
description = "显示和调试 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_10.html](https://dhghomon.github.io/easy_rust/Chapter_10.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 显示和调试

Rust中简单的变量可以用`{}`里面的`println!`打印。但是有些变量不能，你需要**debug print**。Debug打印是给程序员打印的，因为它通常会显示更多的信息。Debug有时看起来并不漂亮，因为它有额外的信息来帮助你。

你怎么知道你是否需要`{:?}`而不是`{}`？编译器会告诉你。比如说

```rust
fn main() {
    let doesnt_print = ();
    println!("This will not print: {}", doesnt_print); // ⚠️
}
```

当我们运行这个时，编译器会说:

```text
error[E0277]: `()` doesn't implement `std::fmt::Display`
 --> src\main.rs:3:41
  |
3 |     println!("This will not print: {}", doesnt_print);
  |                                         ^^^^^^^^^^^^ `()` cannot be formatted with the default formatter
  |
  = help: the trait `std::fmt::Display` is not implemented for `()`
  = note: in format strings you may be able to use `{:?}` (or {:#?} for pretty-print) instead
  = note: required by `std::fmt::Display::fmt`
  = note: this error originates in a macro (in Nightly builds, run with -Z macro-backtrace for more info)
```

信息比较多，但重要的部分是 `you may be able to use {:?} (or {:#?} for pretty-print) instead`. 这意味着你可以试试`{:?}`，也可以试试`{:#?}` `{:#?}`叫做 "漂亮打印"。它和`{:?}`一样，但是在更多的行上打印出不同的格式。

所以Display就是用`{}`打印，Debug就是用`{:?}`打印。

还有一点:如果你不想要新的一行，你也可以使用`print!`而不用`ln`。

```rust
fn main() {
    print!("This will not print a new line");
    println!(" so this will be on the same line");
}
```

这将打印`This will not print a new line so this will be on the same line`。

## 最小和最大的数

如果你想看最小和最大的数字，你可以用MIN和MAX。`std`的意思是 "标准库"，拥有Rust的所有主要函数等。我们将在以后学习标准库。但与此同时，你可以记住，这就是你如何获得一个类型的最小和最大的数字。

```rust
fn main() {
    println!("The smallest i8 is {} and the biggest i8 is {}.", std::i8::MIN, std::i8::MAX); // 提示：打印 std::i8::MIN 的意思是「打印标准库里 i8 部分中的 MIN」
    println!("The smallest u8 is {} and the biggest u8 is {}.", std::u8::MIN, std::u8::MAX);
    println!("The smallest i16 is {} and the biggest i16 is {}.", std::i16::MIN, std::i16::MAX);
    println!("The smallest u16 is {} and the biggest u16 is {}.", std::u16::MIN, std::u16::MAX);
    println!("The smallest i32 is {} and the biggest i32 is {}.", std::i32::MIN, std::i32::MAX);
    println!("The smallest u32 is {} and the biggest u32 is {}.", std::u32::MIN, std::u32::MAX);
    println!("The smallest i64 is {} and the biggest i64 is {}.", std::i64::MIN, std::i64::MAX);
    println!("The smallest u64 is {} and the biggest u64 is {}.", std::u64::MIN, std::u64::MAX);
    println!("The smallest i128 is {} and the biggest i128 is {}.", std::i128::MIN, std::i128::MAX);
    println!("The smallest u128 is {} and the biggest u128 is {}.", std::u128::MIN, std::u128::MAX);

}
```

将会打印:

```text
The smallest i8 is -128 and the biggest i8 is 127.
The smallest u8 is 0 and the biggest u8 is 255.
The smallest i16 is -32768 and the biggest i16 is 32767.
The smallest u16 is 0 and the biggest u16 is 65535.
The smallest i32 is -2147483648 and the biggest i32 is 2147483647.
The smallest u32 is 0 and the biggest u32 is 4294967295.
The smallest i64 is -9223372036854775808 and the biggest i64 is 9223372036854775807.
The smallest u64 is 0 and the biggest u64 is 18446744073709551615.
The smallest i128 is -170141183460469231731687303715884105728 and the biggest i128 is 170141183460469231731687303715884105727.
The smallest u128 is 0 and the biggest u128 is 340282366920938463463374607431768211455.
```
