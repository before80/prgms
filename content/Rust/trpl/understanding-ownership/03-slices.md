+++
title = "4.3 切片类型"
date = 2026-08-05T08:44:00+08:00
weight = 18
type = "docs"
description = "切片类型：引用集合中一段连续元素而不取得所有权"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 切片类型


> 原文链接: [https://doc.rust-lang.org/stable/book/ch04-03-slices.html](https://doc.rust-lang.org/stable/book/ch04-03-slices.html)


## 切片类型 {#the-slice-type}

　　*切片*（slice）让你引用[集合](../../common-collections/)中一段连续的元素。切片是一种引用，因此不拥有所有权。

　　来看一个小编程问题：编写一个函数，接收由空格分隔的单词组成的字符串，并返回其中找到的第一个单词。若函数在字符串中找不到空格，整个字符串就是一个单词，应返回整个字符串。

> 注意：为引入切片，本节假定只处理 ASCII；关于 UTF-8 处理的更完整讨论见第 8 章[「用字符串存储 UTF-8 编码的文本」](../../common-collections/02-strings/#utf-8)一节。

　　先看看不用切片时如何写这个函数的签名，以便理解切片要解决的问题：

```rust
fn first_word(s: &String) -> ?
```

　　`first_word` 的参数类型是 `&String`。我们不需要所有权，这样没问题。（地道的 Rust 中，除非需要，函数不会取得参数的所有权；原因会随着学习逐渐清晰。）但应返回什么？我们其实没有办法谈论字符串的*一部分*。不过可以返回由空格标出的单词末尾索引。如示例 4-7 所示，试试看。

**文件名：`src/main.rs`**
```rust
fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }

    s.len()
}
```

**示例 4-7：返回指向 `String` 参数中字节索引的 `first_word` 函数**

　　因为需要逐元素检查 `String` 是否为空格，我们用 `as_bytes` 方法把 `String` 转成字节数组。

```rust
    let bytes = s.as_bytes();
```

　　接着用 `iter` 方法创建该字节数组的迭代器：

```rust
    for (i, &item) in bytes.iter().enumerate() {
```

　　第 13 章会更详细讨论迭代器。眼下只需知道：`iter` 会返回集合中的每个元素，而 `enumerate` 包装 `iter` 的结果，把每个元素作为元组的一部分返回。`enumerate` 返回的元组中，第一个元素是索引，第二个是对该元素的引用。这比自己算索引更方便一些。

　　因为 `enumerate` 返回元组，我们可以用模式来解构它。模式会在[第 6 章](../../enums/02-match/)详谈。在 `for` 循环里，我们指定的模式用 `i` 表示元组中的索引，用 `&item` 表示元组中的单个字节。由于从 `.iter().enumerate()` 得到的是对元素的引用，模式里要用 `&`。

　　在 `for` 循环内部，我们用字节字面量语法查找表示空格的字节。若找到空格，就返回该位置；否则用 `s.len()` 返回字符串长度。

```rust
        if item == b' ' {
            return i;
        }
    }

    s.len()
```

　　现在我们有办法找出字符串中第一个单词末尾的索引了，但有个问题。我们单独返回一个 `usize`，而它只在 `&String` 的上下文中才有意义。换言之，因为它是与 `String` 分离的值，无法保证将来仍然有效。考虑示例 4-8 中使用示例 4-7 的 `first_word` 的程序。

**文件名：`src/main.rs`**
```rust
fn main() {
    let mut s = String::from("hello world");

    let word = first_word(&s); // word will get the value 5

    s.clear(); // this empties the String, making it equal to ""

    // word still has the value 5 here, but s no longer has any content that we
    // could meaningfully use with the value 5, so word is now totally invalid!
}
```

**示例 4-8：保存调用 `first_word` 的结果，然后更改 `String` 的内容**

　　这个程序能无错误地编译；即便在调用 `s.clear()` 之后再使用 `word` 也一样。因为 `word` 与 `s` 的状态完全无关，`word` 仍含有值 `5`。我们可能拿着这个 `5` 和变量 `s` 去提取第一个单词，但这会是 bug，因为自从把 `5` 存进 `word` 之后，`s` 的内容已经变了。

　　还要操心 `word` 中的索引与 `s` 中的数据不同步，既繁琐又易错！若再写一个 `second_word` 函数，管理这些索引会更脆弱。它的签名大概得像这样：

```rust
fn second_word(s: &String) -> (usize, usize) {
```

　　现在我们既要跟踪起始索引又要跟踪结束索引，还有更多从某一状态下的数据算出、却又与该状态毫无绑定的值。三个本应同步、却彼此独立的变量，维护起来既繁琐又容易出错。

　　幸运的是，Rust 对此有解法：字符串切片。

### 字符串切片 {#string-slices}

　　*字符串切片*（string slice）是对 `String` 中一段连续元素的引用，长这样：

```rust
    let s = String::from("hello world");

    let hello = &s[0..5];
    let world = &s[6..11];
```

　　`hello` 不是对整个 `String` 的引用，而是对由额外的 `[0..5]` 指定的那一部分的引用。我们用方括号内的范围 `[starting_index..ending_index]` 创建切片，其中 *`starting_index`* 是切片中的第一个位置，*`ending_index`* 是切片中最后一个位置再加一。在内部，切片数据结构存储起始位置和切片长度，长度等于 *`ending_index`* 减去 *`starting_index`*。因此，对于 `let world = &s[6..11];`，`world` 会是一个切片：指针指向 `s` 中索引 6 处的字节，长度值为 `5`。

　　图 4-7 用图示说明这一点。

<img alt="三张表：一张表示 s 的栈数据，指向堆上字符串数据 &quot;hello world&quot; 中索引 0 处的字节。第三张表表示切片 world 的栈数据，长度为 5，指向堆数据表中的字节 6。" src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">图 4-7：引用 `String` 一部分的字符串切片</span>

　　借助 Rust 的 `..` 范围语法，若想从索引 0 开始，可以省略两点之前的值。换言之，下面两种写法等价：

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

　　同理，若切片包含 `String` 的最后一个字节，可以省略末尾的数字。也就是说，下面两种写法等价：

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

　　也可以两个值都省略，以取得整个字符串的切片。因此下面两种写法等价：

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> 注意：字符串切片的范围索引必须落在有效的 UTF-8 字符边界上。若试图在多字节字符中间创建字符串切片，程序会以错误退出。

　　有了这些信息，我们重写 `first_word`，让它返回切片。表示「字符串切片」的类型写作 `&str`：

**文件名：`src/main.rs`**
```rust
fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
```

　　我们用与示例 4-7 相同的方式得到单词末尾的索引：查找第一个空格。找到空格时，以字符串开头和空格索引作为起止索引返回字符串切片。

　　现在调用 `first_word` 会得到一个与底层数据绑定的单一值。该值由指向切片起点的引用以及切片中的元素个数组成。

　　返回切片对 `second_word` 函数同样适用：

```rust
fn second_word(s: &String) -> &str {
```

　　我们现在有了更直白、也更难用错的 API，因为编译器会确保指向 `String` 的引用保持有效。还记得示例 4-8 中的 bug 吗？我们拿到了第一个单词末尾的索引，随后清空了字符串，索引就失效了。那段代码在逻辑上不正确，却没有立即报错；若继续拿着已清空字符串的第一个单词索引去用，问题才会稍后出现。切片让这种 bug 不可能发生，并让我们更早发现代码有问题。使用返回切片的 `first_word` 会触发编译期错误：

**文件名：`src/main.rs`**
```rust
fn main() {
    let mut s = String::from("hello world");

    let word = first_word(&s);

    s.clear(); // error!

    println!("the first word is: {word}");
}
```

　　编译器错误如下：

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
  --> src/main.rs:18:5
   |
16 |     let word = first_word(&s);
   |                           -- immutable borrow occurs here
17 |
18 |     s.clear(); // error!
   |     ^^^^^^^^^ mutable borrow occurs here
19 |
20 |     println!("the first word is: {word}");
   |                                   ---- immutable borrow later used here

For more information about this error, try `rustc --explain E0502`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

　　回想借用规则：若对某物有不可变引用，就不能再取得可变引用。因为 `clear` 需要截断 `String`，它必须取得可变引用。`clear` 之后的 `println!` 使用了 `word` 中的引用，因此那时不可变引用必须仍然有效。Rust 不允许 `clear` 中的可变引用与 `word` 中的不可变引用同时存在，于是编译失败。Rust 不仅让我们的 API 更好用，还在编译期消除了整整一类错误！

#### 字符串字面量就是切片

　　还记得我们说过字符串字面量存放在二进制文件内部吗？现在了解了切片，就能正确理解字符串字面量了：

```rust
let s = "Hello, world!";
```

　　这里 `s` 的类型是 `&str`：它是一个指向二进制中那一特定位置的切片。这也是字符串字面量不可变的原因：`&str` 是不可变引用。

#### 字符串切片作为参数 {#string-slices-as-parameters}

　　知道可以对字面量和 `String` 值取切片之后，还能再改进一下 `first_word`，也就是它的签名：

```rust
fn first_word(s: &String) -> &str {
```

　　更有经验的 Rustacean 会写成示例 4-9 所示的签名，因为这样同一函数既可用于 `&String` 值，也可用于 `&str` 值。

```rust
fn first_word(s: &str) -> &str {
```

**示例 4-9：通过让参数 `s` 使用字符串切片类型来改进 `first_word`**

　　若已有字符串切片，可以直接传入；若有 `String`，可以传入该 `String` 的切片，或对 `String` 的引用。这种灵活性利用了解引用强制转换（deref coercion），我们会在第 15 章[「在函数与方法中使用 Deref 强制转换」](../../smart-pointers/02-deref/)一节介绍。

　　定义函数接受字符串切片而非对 `String` 的引用，能在不损失任何功能的情况下让 API 更通用、更有用：

**文件名：`src/main.rs`**
```rust
fn main() {
    let my_string = String::from("hello world");

    // `first_word` works on slices of `String`s, whether partial or whole.
    let word = first_word(&my_string[0..6]);
    let word = first_word(&my_string[..]);
    // `first_word` also works on references to `String`s, which are equivalent
    // to whole slices of `String`s.
    let word = first_word(&my_string);

    let my_string_literal = "hello world";

    // `first_word` works on slices of string literals, whether partial or
    // whole.
    let word = first_word(&my_string_literal[0..6]);
    let word = first_word(&my_string_literal[..]);

    // Because string literals *are* string slices already,
    // this works too, without the slice syntax!
    let word = first_word(my_string_literal);
}
```

### 其他切片

　　顾名思义，字符串切片专用于字符串。但还有更通用的切片类型。看这个数组：

```rust
let a = [1, 2, 3, 4, 5];
```

　　正如可能想引用字符串的一部分，我们也可能想引用数组的一部分。可以这样做：

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

　　这个切片的类型是 `&[i32]`。它与字符串切片工作方式相同：存储指向第一个元素的引用以及一个长度。你会在各种其他集合上使用这类切片。第 8 章讨论向量时会详细介绍这些集合。

## 总结

　　所有权、借用和切片这些概念，能在编译期保证 Rust 程序的内存安全。Rust 语言像其他系统编程语言一样，让你掌控内存使用。但数据所有者在离开作用域时自动清理数据，意味着你不必为获得这种控制而额外编写和调试代码。

　　所有权会影响 Rust 许多其他部分的工作方式，因此本书其余部分还会继续谈及这些概念。接下来进入第 5 章，看看如何用 `struct` 把多块数据组合在一起。

[ch13]: ../../functional-features/02-iterators/
[ch6]: ../../enums/02-match/
[strings]: ../../common-collections/02-strings/
[deref-coercions]: ../../smart-pointers/02-deref/
