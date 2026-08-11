+++
title = "8.2 用字符串存储 UTF-8 编码的文本"
date = 2026-08-05T08:44:00+08:00
weight = 35
type = "docs"
description = "深入 String 与 UTF-8：创建、更新、切片与遍历"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用字符串存储 UTF-8 编码的文本 {#utf-8}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch08-02-strings.html](https://doc.rust-lang.org/stable/book/ch08-02-strings.html)


## 用字符串存储 UTF-8 编码的文本 {#storing-utf-8-encoded-text-with-strings}

　　我们在第 4 章谈过字符串，现在会看得更深入。Rust 新手常常在字符串上卡住，原因通常有三个叠加在一起：Rust 倾向于把可能的错误暴露出来；字符串比许多程序员以为的更复杂；还有 UTF-8。这些因素合在一起，对于从其他编程语言转来的人来说，有时会显得很难。

　　我们把字符串放在集合的语境下讨论，是因为字符串实现为字节的集合，再加上一些在把这些字节解释为文本时提供有用功能的方法。本节会讨论 `String` 上每种集合类型都有的操作，例如创建、更新和读取。我们也会讨论 `String` 与其他集合的不同之处，尤其是：由于人和计算机对 `String` 数据的解释不同，对 `String` 做索引会变得复杂。

### 定义字符串

　　我们先说明「字符串」这个词指什么。Rust 核心语言里只有一种字符串类型，即字符串切片 `str`，通常以借用形式 `&str` 出现。第 4 章我们谈过字符串切片，它们是对存放在别处的某些 UTF-8 编码字符串数据的引用。例如，字符串字面量存放在程序的二进制文件中，因此也是字符串切片。

　　`String` 类型由 Rust 标准库提供，而不是写进核心语言；它是可增长、可变、拥有所有权、UTF-8 编码的字符串类型。当 Rustacean 提到 Rust 中的「字符串」时，可能指的是 `String` 或字符串切片 `&str` 中的任意一种，而不是只指其中一种。虽然本节主要讲 `String`，但这两种类型在 Rust 标准库中都被大量使用，并且 `String` 与字符串切片都是 UTF-8 编码的。

### 创建新字符串

　　许多适用于 `Vec<T>` 的操作同样适用于 `String`，因为 `String` 实际上实现为对字节向量的包装，并附带一些额外的保证、限制和能力。一个对 `Vec<T>` 和 `String` 工作方式相同的函数例子，就是用来创建实例的 `new` 函数，如示例 8-11 所示。

```rust
    let mut s = String::new();
```

**示例 8-11：创建一个新的空 `String`**

　　这一行创建了一个名为 `s` 的新空字符串，之后我们可以向其中载入数据。通常我们会有一些想用来启动字符串的初始数据。这时可以使用 `to_string` 方法，任何实现了 `Display` 特征的类型都可用它，字符串字面量也是如此。示例 8-12 展示了两个例子。

```rust
    let data = "initial contents";

    let s = data.to_string();

    // The method also works on a literal directly:
    let s = "initial contents".to_string();
```

**示例 8-12：用 `to_string` 方法从字符串字面量创建 `String`**

　　这段代码创建了一个包含 `initial contents` 的字符串。

　　我们也可以用函数 `String::from` 从字符串字面量创建 `String`。示例 8-13 中的代码与示例 8-12 中使用 `to_string` 的代码等价。

```rust
    let s = String::from("initial contents");
```

**示例 8-13：用 `String::from` 函数从字符串字面量创建 `String`**

　　因为字符串用途极广，我们可以对字符串使用许多不同的通用 API，选项很多。有些看起来像是重复的，但各自都有用武之地！在这个例子里，`String::from` 和 `to_string` 做的是同一件事，选哪个取决于风格和可读性。

　　请记住字符串是 UTF-8 编码的，因此我们可以在其中包含任何正确编码的数据，如示例 8-14 所示。

```rust
    let hello = String::from("السلام عليكم");
    let hello = String::from("Dobrý den");
    let hello = String::from("Hello");
    let hello = String::from("שלום");
    let hello = String::from("नमस्ते");
    let hello = String::from("こんにちは");
    let hello = String::from("안녕하세요");
    let hello = String::from("你好");
    let hello = String::from("Olá");
    let hello = String::from("Здравствуйте");
    let hello = String::from("Hola");
```

**示例 8-14：在字符串中存放不同语言的问候语**

　　这些都是有效的 `String` 值。

### 更新字符串

　　与 `Vec<T>` 的内容一样，若向 `String` 中推入更多数据，它可以增长，内容也可以改变。此外，你可以方便地用 `+` 运算符或 `format!` 宏来拼接 `String` 值。

#### 用 `push_str` 或 `push` 追加

　　我们可以用 `push_str` 方法追加字符串切片来增长 `String`，如示例 8-15 所示。

```rust
    let mut s = String::from("foo");
    s.push_str("bar");
```

**示例 8-15：用 `push_str` 方法向 `String` 追加字符串切片**

　　这两行之后，`s` 将包含 `foobar`。`push_str` 方法接受字符串切片，因为我们不一定想取得参数的所有权。例如，在示例 8-16 的代码中，我们希望在把 `s2` 的内容追加到 `s1` 之后仍能使用 `s2`。

```rust
    let mut s1 = String::from("foo");
    let s2 = "bar";
    s1.push_str(s2);
    println!("s2 is {s2}");
```

**示例 8-16：在把字符串切片的内容追加到 `String` 之后继续使用该切片**

　　若 `push_str` 方法取得了 `s2` 的所有权，我们就无法在最后一行打印它的值。不过这段代码会如我们所期望的那样工作！

　　`push` 方法接受单个字符作为参数，并把它加到 `String` 上。示例 8-17 用 `push` 方法给一个 `String` 加上字母 *l*。

```rust
    let mut s = String::from("lo");
    s.push('l');
```

**示例 8-17：用 `push` 向 `String` 值添加一个字符**

　　结果是 `s` 将包含 `lol`。

#### 用 `+` 或 `format!` 拼接 {#concatenating-with--or-format}

　　常常你会想把两个已有的字符串合在一起。一种做法是使用 `+` 运算符，如示例 8-18 所示。

```rust
    let s1 = String::from("Hello, ");
    let s2 = String::from("world!");
    let s3 = s1 + &s2; // note s1 has been moved here and can no longer be used
```

**示例 8-18：用 `+` 运算符把两个 `String` 值合并成一个新的 `String` 值**

　　字符串 `s3` 将包含 `Hello, world!`。加法之后 `s1` 不再有效的原因，以及我们为何对 `s2` 使用引用，都与使用 `+` 运算符时调用的方法签名有关。`+` 运算符使用的是 `add` 方法，其签名大致如下：

```rust
fn add(self, s: &str) -> String {
```

　　在标准库中，你会看到 `add` 是用泛型和关联类型定义的。这里我们代入了具体类型，这正是用 `String` 值调用该方法时发生的事。我们将在第 10 章讨论泛型。这个签名给了我们理解 `+` 运算符棘手之处所需的线索。

　　首先，`s2` 带有 `&`，意味着我们是把第二个字符串的引用加到第一个字符串上。这是因为 `add` 函数中的 `s` 参数：我们只能把字符串切片加到 `String` 上；不能把两个 `String` 值直接相加。但是等等——`&s2` 的类型是 `&String`，而不是 `add` 第二个参数所要求的 `&str`。那示例 8-18 为什么能编译？

　　我们之所以能在调用 `add` 时使用 `&s2`，是因为编译器可以把 `&String` 参数强制转换成 `&str`。调用 `add` 方法时，Rust 使用解引用强制转换（deref coercion），在这里会把 `&s2` 变成 `&s2[..]`。我们会在第 15 章更深入地讨论解引用强制转换。因为 `add` 不会取得 `s` 参数的所有权，所以这次操作之后 `s2` 仍然是有效的 `String`。

　　其次，从签名可以看出 `add` 取得了 `self` 的所有权，因为 `self` *没有* `&`。这意味着示例 8-18 中的 `s1` 会被移动进 `add` 调用，之后不再有效。因此，虽然 `let s3 = s1 + &s2;` 看起来像是复制两个字符串并创建一个新字符串，这个语句实际上取得了 `s1` 的所有权，追加一份 `s2` 内容的副本，然后返回结果的所有权。换句话说，它看起来像在做大量复制，其实并没有；实现比复制更高效。

　　若需要拼接多个字符串，`+` 运算符的行为会变得笨拙：

```rust
    let s1 = String::from("tic");
    let s2 = String::from("tac");
    let s3 = String::from("toe");

    let s = s1 + "-" + &s2 + "-" + &s3;
```

　　此时 `s` 将是 `tic-tac-toe`。满眼的 `+` 和 `"` 字符让人很难看清发生了什么。要以更复杂的方式组合字符串时，可以改用 `format!` 宏：

```rust
    let s1 = String::from("tic");
    let s2 = String::from("tac");
    let s3 = String::from("toe");

    let s = format!("{s1}-{s2}-{s3}");
```

　　这段代码同样把 `s` 设为 `tic-tac-toe`。`format!` 宏的工作方式类似 `println!`，但不是把输出打印到屏幕，而是返回包含内容的 `String`。使用 `format!` 的版本可读性好得多，而且 `format!` 宏生成的代码使用引用，因此这次调用不会取得任何参数的所有权。

### 字符串索引

　　在许多其他编程语言中，通过索引引用字符串中的单个字符是合法且常见的操作。然而，若你在 Rust 中试图用索引语法访问 `String` 的部分内容，会得到错误。看看示例 8-19 中这段无效代码。

```rust
    let s1 = String::from("hi");
    let h = s1[0];
```

**示例 8-19：尝试对 `String` 使用索引语法**

　　这段代码会产生如下错误：

```console
$ cargo run
   Compiling collections v0.1.0 (file:///projects/collections)
error[E0277]: the type `str` cannot be indexed by `{integer}`
 --> src/main.rs:3:16
  |
3 |     let h = s1[0];
  |                ^ string indices are ranges of `usize`
  |
  = help: the trait `SliceIndex<str>` is not implemented for `{integer}`
  = note: you can use `.chars().nth()` or `.bytes().nth()`
          for more information, see chapter 8 in The Book: <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>
help: `usize` implements trait `SliceIndex<T>`
 --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/slice/index.rs:214:0
  |
  = note: `SliceIndex<[T]>`
 --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/bstr/traits.rs:197:0
  |
  = note: `SliceIndex<ByteStr>`
  = note: required for `String` to implement `Index<{integer}>`

For more information about this error, try `rustc --explain E0277`.
error: could not compile `collections` (bin "collections") due to 1 previous error
```

　　错误说明了一切：Rust 字符串不支持索引。但为什么不支持？要回答这个问题，我们需要讨论 Rust 如何在内存中存储字符串。

#### 内部表示

　　`String` 是对 `Vec<u8>` 的包装。让我们看看示例 8-14 中一些正确编码的 UTF-8 示例字符串。首先是这个：

```rust
    let hello = String::from("Hola");
```

　　此时 `len` 将是 `4`，意味着存放字符串 `"Hola"` 的向量长 4 字节。这些字母在 UTF-8 编码下各占 1 字节。然而下一行可能会让你吃惊（注意这个字符串以西里尔大写字母 *Ze* 开头，而不是数字 3）：

```rust
    let hello = String::from("Здравствуйте");
```

　　若有人问这个字符串有多长，你可能会说 12。事实上，Rust 的答案是 24：那是用 UTF-8 编码「Здравствуйте」所需的字节数，因为该字符串中的每个 Unicode 标量值都占 2 字节存储。因此，对字符串字节的索引并不总是对应有效的 Unicode 标量值。为了演示，看看这段无效的 Rust 代码：

```rust
let hello = "Здравствуйте";
let answer = &hello[0];
```

　　你已经知道 `answer` 不会是第一个字母 `З`。在 UTF-8 编码中，`З` 的第一个字节是 `208`，第二个是 `151`，因此看起来 `answer` 似乎应该是 `208`，但 `208` 本身并不是一个有效字符。若用户想要这个字符串的第一个字母，返回 `208` 多半不是他们想要的；然而那是 Rust 在字节索引 0 处仅有的数据。用户通常也不希望返回字节值，即便字符串只包含拉丁字母：若 `&"hi"[0]` 是合法代码并返回字节值，它会返回 `104`，而不是 `h`。

　　因此，为了避免返回出人意料的值并造成可能无法立即发现的 bug，Rust 根本不编译这段代码，从而在开发过程早期就防止误解。

#### 字节、标量值与字素簇

　　关于 UTF-8 的另一点是：从 Rust 的角度看，实际上有三种相关的方式来看待字符串：作为字节、作为标量值，以及作为字素簇（grapheme clusters，最接近我们所说的*字母*）。

　　若看用天城文（Devanagari）书写的印地语词「नमस्ते」，它作为 `u8` 值的向量存储时看起来是这样：

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

　　那是 18 个字节，也是计算机最终存储这些数据的方式。若把它们看作 Unicode 标量值（也就是 Rust 的 `char` 类型），这些字节看起来是这样：

```text
['न', 'म', 'स', '्', 'त', 'े']
```

　　这里有六个 `char` 值，但第四个和第六个不是字母：它们是单独看没有意义的变音符号。最后，若把它们看作字素簇，就会得到人们所说的构成这个印地语词的四个字母：

```text
["न", "म", "स्", "ते"]
```

　　Rust 提供了解释计算机所存原始字符串数据的不同方式，这样每个程序都可以选择自己需要的解释，无论数据使用的是哪种人类语言。

　　Rust 不允许我们对 `String` 做索引以得到一个字符，还有最后一个原因：索引操作被期望总是耗时恒定（O(1)）。但对 `String` 无法保证这种性能，因为 Rust 必须从开头遍历内容到该索引，才能确定有多少个有效字符。

### 字符串切片

　　对字符串做索引常常是个坏主意，因为不清楚字符串索引操作的返回类型应该是什么：字节值、字符、字素簇，还是字符串切片。因此，若你确实需要用索引来创建字符串切片，Rust 会要求你更加具体。

　　与其用带单个数字的 `[]` 做索引，你可以用带范围的 `[]` 来创建包含特定字节的字符串切片：

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

　　这里，`s` 将是包含该字符串前 4 个字节的 `&str`。前面我们提到这些字符各占 2 字节，这意味着 `s` 将是 `Зд`。

　　若我们试图只用某个字符字节的一部分做切片，例如 `&hello[0..1]`，Rust 会在运行时 panic，方式与访问向量中无效索引时相同：

```console
$ cargo run
   Compiling collections v0.1.0 (file:///projects/collections)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.43s
     Running `target/debug/collections`

thread 'main' (6017738) panicked at src/main.rs:4:19:
end byte index 1 is not a char boundary; it is inside 'З' (bytes 0..2 of string)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　用范围创建字符串切片时应当谨慎，因为这样做可能导致程序崩溃。

### 遍历字符串

　　操作字符串片段的最佳方式，是明确说明你想要的是字符还是字节。对于单个 Unicode 标量值，使用 `chars` 方法。对「Зд」调用 `chars` 会分离并返回两个 `char` 类型的值，你可以遍历结果来访问每个元素：

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

　　这段代码会打印：

```text
З
д
```

　　或者，`bytes` 方法返回每个原始字节，这在你的领域中可能更合适：

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

　　这段代码会打印构成该字符串的 4 个字节：

```text
208
151
208
180
```

　　但务必记住：有效的 Unicode 标量值可能由不止 1 个字节组成。

　　要从字符串中获取字素簇（例如天城文的情况）很复杂，因此标准库不提供这一功能。若你需要这种功能，[crates.io](https://crates.io/) 上有可用的 crate。

### 应对字符串的复杂性

　　总之，字符串很复杂。不同编程语言在如何向程序员呈现这种复杂性上做出了不同选择。Rust 选择让正确处理 `String` 数据成为所有 Rust 程序的默认行为，这意味着程序员必须从一开始就更多思考如何处理 UTF-8 数据。这种权衡使字符串的复杂性比在其他语言中更显眼，但它能防止你在开发生命周期的后期才去处理涉及非 ASCII 字符的错误。

　　好消息是，标准库在 `String` 和 `&str` 类型之上提供了大量功能，帮助你正确处理这些复杂情况。请务必查阅文档，了解像用于在字符串中搜索的 `contains`、以及用于替换字符串部分内容的 `replace` 这类有用方法。

　　让我们切换到稍微不那么复杂的东西：哈希映射！
