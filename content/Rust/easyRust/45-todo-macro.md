+++
title = "45-todo! 宏"
date = 2026-08-21T12:46:00+08:00
weight = 46
type = "docs"
description = "todo! 宏 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_44.html](https://dhghomon.github.io/easy_rust/Chapter_44.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# todo! 宏

有时你想粗略写点写代码帮助你想象你的项目。例如，想象一个简单的项目，用书籍做一些事情。下面是你写的时候的想法:

```rust
struct Book {} // 好，首先需要一个 Book 结构体。
               // 里面还没有东西——以后再加

enum BookType { // 书可以是精装或平装，所以加一个枚举
    HardCover,
    SoftCover,
}

fn get_book(book: &Book) -> Option<String> {} // ⚠️ get_book 应接受 &Book 并返回 Option<String>

fn delete_book(book: Book) -> Result<(), String> {} // delete_book 应接受 Book 并返回 Result……
                                                    // TODO：写 impl 块，把这些函数做成方法……
fn check_book_type(book_type: &BookType) { // 确认一下 match 语句能工作
    match book_type {
        BookType::HardCover => println!("It's hardcover"),
        BookType::SoftCover => println!("It's softcover"),
    }
}

fn main() {
    let book_type = BookType::HardCover;
    check_book_type(&book_type); // 好，检查一下这个函数！
}
```

但Rust对`get_book`和`delete_book`不满意。它说

```text
error[E0308]: mismatched types
  --> src\main.rs:32:29
   |
32 | fn get_book(book: &Book) -> Option<String> {}
   |    --------                 ^^^^^^^^^^^^^^ expected enum `std::option::Option`, found `()`
   |    |
   |    implicitly returns `()` as its body has no tail or `return` expression
   |
   = note:   expected enum `std::option::Option<std::string::String>`
           found unit type `()`

error[E0308]: mismatched types
  --> src\main.rs:34:31
   |
34 | fn delete_book(book: Book) -> Result<(), String> {}
   |    -----------                ^^^^^^^^^^^^^^^^^^ expected enum `std::result::Result`, found `()`
   |    |
   |    implicitly returns `()` as its body has no tail or `return` expression
   |
   = note:   expected enum `std::result::Result<(), std::string::String>`
           found unit type `()`
```

但是你现在不关心`get_book`和`delete_book`。这时你可以使用`todo!()`。如果你把这个加到函数中，Rust不会抱怨，而且会编译。

```rust
struct Book {}

fn get_book(book: &Book) -> Option<String> {
    todo!() // todo 的意思是“我以后再做，请安静”
}

fn delete_book(book: Book) -> Result<(), String> {
    todo!()
}

fn main() {}
```

所以现在代码编译，你可以看到`check_book_type`的结果:`It's hardcover`。

但是要小心，因为它只是编译--你不能使用函数。如果你调用里面有`todo!()`的函数，它就会崩溃。

另外，`todo!()`函数仍然需要真实的输入和输出类型。如果你只写这个，它将无法编译。

```rust
struct Book {}

fn get_book(book: &Book) -> WorldsBestType { // ⚠️
    todo!()
}

fn main() {}
```

它会说

```text
error[E0412]: cannot find type `WorldsBestType` in this scope
  --> src\main.rs:32:29
   |
32 | fn get_book(book: &Book) -> WorldsBestType {
   |                             ^^^^^^^^^^^^^^ not found in this scope
```

`todo!()`其实和另一个宏一样：`unimplemented!()`。程序员们经常使用 `unimplemented!()`，但打字时太长了，所以他们创建了 `todo!()`，它比较短。
