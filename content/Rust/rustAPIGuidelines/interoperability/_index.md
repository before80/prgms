+++
title = "第2章 互操作性"
date = 2026-08-18T21:50:00+08:00
weight = 40
type = "docs"
description = "互操作性 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/interoperability.html](https://rust-lang.github.io/api-guidelines/interoperability.html)

# 互操作性

## 类型积极实现常用 trait (C-COMMON-TRAITS) {#c-common-traits}

Rust 的 trait 系统不允许 _orphan_（孤儿）实现：大致来说，每个 `impl` 必须位于定义该 trait 的 crate，或定义实现类型的 crate 中。
因此，定义新类型的 crate 应积极实现所有适用的常用 trait。

要理解原因，请考虑以下情形：

* Crate `std` 定义了 trait `Display`。
* Crate `url` 定义了类型 `Url`，但未实现 `Display`。
* Crate `webapp` 同时从 `std` 和 `url` 导入，

`webapp` 无法为 `Url` 添加 `Display`，因为它两者都未定义。（注：newtype 模式可以提供一种高效但不方便的变通办法。）

从 `std` 中最重要、应实现的常用 trait 包括：

- [`Copy`](https://doc.rust-lang.org/std/marker/trait.Copy.html)
- [`Clone`](https://doc.rust-lang.org/std/clone/trait.Clone.html)
- [`Eq`](https://doc.rust-lang.org/std/cmp/trait.Eq.html)
- [`PartialEq`](https://doc.rust-lang.org/std/cmp/trait.PartialEq.html)
- [`Ord`](https://doc.rust-lang.org/std/cmp/trait.Ord.html)
- [`PartialOrd`](https://doc.rust-lang.org/std/cmp/trait.PartialOrd.html)
- [`Hash`](https://doc.rust-lang.org/std/hash/trait.Hash.html)
- [`Debug`](https://doc.rust-lang.org/std/fmt/trait.Debug.html)
- [`Display`](https://doc.rust-lang.org/std/fmt/trait.Display.html)
- [`Default`](https://doc.rust-lang.org/std/default/trait.Default.html)

请注意，类型同时实现 `Default` 以及一个无参的 `new` 构造函数是常见且符合预期的。
`new` 是 Rust 中的构造函数约定，用户期望它存在，因此如果基本构造函数不需要参数是合理的，
那就应当提供，即使它在功能上与 `default` 完全相同。

## 转换使用标准 trait `From`、`AsRef`、`AsMut` (C-CONV-TRAITS) {#c-conv-traits}

在合理的地方，应实现以下转换 trait：

- [`From`](https://doc.rust-lang.org/std/convert/trait.From.html)
- [`TryFrom`](https://doc.rust-lang.org/std/convert/trait.TryFrom.html)
- [`AsRef`](https://doc.rust-lang.org/std/convert/trait.AsRef.html)
- [`AsMut`](https://doc.rust-lang.org/std/convert/trait.AsMut.html)

以下转换 trait 永远不应实现：

- [`Into`](https://doc.rust-lang.org/std/convert/trait.Into.html)
- [`TryInto`](https://doc.rust-lang.org/std/convert/trait.TryInto.html)

这些 trait 基于 `From` 和 `TryFrom` 有 blanket impl。应实现后者。

### 标准库中的示例

- `From<u16>` 为 `u32` 实现，因为较小的整数总是可以转换为较大的整数。
- `From<u32>` *不* 为 `u16` 实现，因为若整数过大，转换可能无法完成。
- `TryFrom<u32>` 为 `u16` 实现，若整数过大无法放入 `u16` 则返回错误。
- [`From<Ipv6Addr>`] 为 [`IpAddr`] 实现，后者是可同时表示 v4 与 v6 IP 地址的类型。

[`From<Ipv6Addr>`]: https://doc.rust-lang.org/std/net/struct.Ipv6Addr.html
[`IpAddr`]: https://doc.rust-lang.org/std/net/enum.IpAddr.html

## 集合实现 `FromIterator` 与 `Extend` (C-COLLECT) {#c-collect}

[`FromIterator`] 与 [`Extend`] 使集合能方便地与下列迭代器方法一起使用：

[`FromIterator`]: https://doc.rust-lang.org/std/iter/trait.FromIterator.html
[`Extend`]: https://doc.rust-lang.org/std/iter/trait.Extend.html

- [`Iterator::collect`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.collect)
- [`Iterator::partition`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.partition)
- [`Iterator::unzip`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.unzip)

`FromIterator` 用于从迭代器创建包含其元素的新集合，而 `Extend` 用于将迭代器中的元素追加到已有集合。

### 标准库中的示例

- [`Vec<T>`] 同时实现了 `FromIterator<T>` 与 `Extend<T>`。

[`Vec<T>`]: https://doc.rust-lang.org/std/vec/struct.Vec.html

## 数据结构实现 Serde 的 `Serialize`、`Deserialize` (C-SERDE) {#c-serde}

扮演数据结构角色的类型应实现 [`Serialize`] 与 [`Deserialize`]。

[`Serialize`]: https://docs.serde.rs/serde/trait.Serialize.html
[`Deserialize`]: https://docs.serde.rs/serde/trait.Deserialize.html

从明显是数据结构的东西，到明显不是的东西，中间存在连续谱与灰色地带。[`LinkedHashMap`]
与 [`IpAddr`] 是数据结构。有人想从 JSON 文件读入 `LinkedHashMap` 或 `IpAddr`，
或通过 IPC 发送到另一进程，这完全合理。[`LittleEndian`] 不是数据结构。
它是 `byteorder` crate 用来在编译期针对特定字节序做优化的标记，事实上 `LittleEndian`
的实例在运行时永远不会存在。这些是界限清晰的例子；更模糊的情形必要时可在 #rust 或 #serde
IRC 频道寻求评估帮助。

[`LinkedHashMap`]: https://docs.rs/linked-hash-map/0.4.2/linked_hash_map/struct.LinkedHashMap.html
[`IpAddr`]: https://doc.rust-lang.org/std/net/enum.IpAddr.html
[`LittleEndian`]: https://docs.rs/byteorder/1.0.0/byteorder/enum.LittleEndian.html

若 crate 并非因其他原因已依赖 Serde，可将 Serde 的 impl 放在 Cargo cfg 之后。这样下游库
仅在需要这些 impl 存在时才承担编译 Serde 的成本。

为与其他基于 Serde 的库保持一致，Cargo cfg 的名称应简单地为 `"serde"`。不要使用
`"serde_impls"` 或 `"serde_serialization"` 等不同的 cfg 名称。

不使用 derive 时，规范实现如下：

```toml
[dependencies]
serde = { version = "1.0", optional = true }
```

```rust
pub struct T { /* ... */ }

#[cfg(feature = "serde")]
impl Serialize for T { /* ... */ }

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for T { /* ... */ }
```

使用 derive 时：

```toml
[dependencies]
serde = { version = "1.0", optional = true, features = ["derive"] }
```

```rust
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub struct T { /* ... */ }
```

## 类型在可能时是 `Send` 和 `Sync` (C-SEND-SYNC) {#c-send-sync}

当编译器判定合适时，会自动实现 [`Send`] 与 [`Sync`]。

[`Send`]: https://doc.rust-lang.org/std/marker/trait.Send.html
[`Sync`]: https://doc.rust-lang.org/std/marker/trait.Sync.html

在操作原始指针的类型中，请警惕你的类型的 `Send` 与 `Sync` 状态是否准确反映其线程安全特性。
类似下面的测试有助于捕获类型是否实现 `Send` 或 `Sync` 的无意回退。

```rust
#[test]
fn test_send() {
    fn assert_send<T: Send>() {}
    assert_send::<MyStrangeType>();
}

#[test]
fn test_sync() {
    fn assert_sync<T: Sync>() {}
    assert_sync::<MyStrangeType>();
}
```

## 错误类型有意义且行为良好 (C-GOOD-ERR) {#c-good-err}

错误类型是指你的 crate 任一公开函数所返回的 `Result<T, E>` 中的类型 `E`。错误类型应始终实现
[`std::error::Error`] trait，这是像 [`error-chain`] 这样的错误处理库对不同错误类型进行抽象的机制，
也允许该错误被用作另一错误的 [`source()`]。

[`std::error::Error`]: https://doc.rust-lang.org/std/error/trait.Error.html
[`error-chain`]: https://docs.rs/error-chain
[`source()`]: https://doc.rust-lang.org/std/error/trait.Error.html#method.source

此外，错误类型应实现 [`Send`] 与 [`Sync`] trait。非 `Send` 的错误无法由 [`thread::spawn`]
启动的线程返回。非 `Sync` 的错误无法通过 [`Arc`] 跨线程传递。这些是多线程应用中基本错误处理的常见要求。

[`Send`]: https://doc.rust-lang.org/std/marker/trait.Send.html
[`Sync`]: https://doc.rust-lang.org/std/marker/trait.Sync.html
[`thread::spawn`]: https://doc.rust-lang.org/std/thread/fn.spawn.html
[`Arc`]: https://doc.rust-lang.org/std/sync/struct.Arc.html

`Send` 与 `Sync` 对于使用 [`std::io::Error::new`] 将自定义错误打包进 IO 错误也很重要，
该方法要求 trait bound 为 `Error + Send + Sync`。

[`std::io::Error::new`]: https://doc.rust-lang.org/std/io/struct.Error.html#method.new

需要特别留意本指南的一处是返回 Error trait 对象的函数，例如 [`reqwest::Error::get_ref`]。
通常对调用方最有用的是 `Error + Send + Sync + 'static`。加上 `'static` 可使该 trait 对象
与 [`Error::downcast_ref`] 一起使用。

[`reqwest::Error::get_ref`]: https://docs.rs/reqwest/0.7.2/reqwest/struct.Error.html#method.get_ref
[`Error::downcast_ref`]: https://doc.rust-lang.org/std/error/trait.Error.html#method.downcast_ref-2

永远不要用 `()` 作为错误类型，即使没有有用的额外信息可供错误携带。

- `()` 未实现 `Error`，因此无法与 `error-chain` 等错误处理库一起使用。
- `()` 未实现 `Display`，因此若用户想因该错误而失败，需要自行编写错误消息。
- 对决定 `unwrap()` 该错误的用户而言，`()` 的 `Debug` 表示毫无帮助。
- 下游库为其错误类型实现 `From<()>` 在语义上没有意义，因此不能将 `()` 作为错误类型与 `?` 运算符一起使用。

相反，应定义专属于你的 crate 或个别函数的有意义错误类型。提供适当的 `Error` 与 `Display` impl。
若没有有用的信息可供错误携带，可实现为单位结构体。

```rust
use std::error::Error;
use std::fmt::Display;

// 不要这样……
fn do_the_thing() -> Result<Wow, ()>

// 优先这样……
fn do_the_thing() -> Result<Wow, DoError>

#[derive(Debug)]
struct DoError;

impl Display for DoError { /* ... */ }
impl Error for DoError { /* ... */ }
```

错误类型的 `Display` 表示所给出的错误消息应为小写、无尾随标点，且通常简洁。

不应实现 [`Error::description()`]。它已被弃用，用户应始终使用 `Display` 而非 `description()` 来打印错误。

[`Error::description()`]: https://doc.rust-lang.org/std/error/trait.Error.html#tymethod.description

### 标准库中的示例

- 从字符串解析 bool 失败时返回 [`ParseBoolError`]。

[`ParseBoolError`]: https://doc.rust-lang.org/std/str/struct.ParseBoolError.html

### 错误消息示例

- "unexpected end of file"
- "provided string was not \`true\` or \`false\`"
- "invalid IP address syntax"
- "second time provided was later than self"
- "invalid UTF-8 sequence of {} bytes from index {}"
- "environment variable was not valid unicode: {:?}"

## 二进制数值类型提供 `Hex`、`Octal`、`Binary` 格式化 (C-NUM-FMT) {#c-num-fmt}

- [`std::fmt::UpperHex`](https://doc.rust-lang.org/std/fmt/trait.UpperHex.html)
- [`std::fmt::LowerHex`](https://doc.rust-lang.org/std/fmt/trait.LowerHex.html)
- [`std::fmt::Octal`](https://doc.rust-lang.org/std/fmt/trait.Octal.html)
- [`std::fmt::Binary`](https://doc.rust-lang.org/std/fmt/trait.Binary.html)

这些 trait 控制类型在 `{:X}`、`{:x}`、`{:o}` 与 `{:b}` 格式说明符下的表示。

对你会考虑进行 `|` 或 `&` 等位运算的任何数值类型实现这些 trait。这对 bitflag 类型尤其合适。
像 `struct Nanoseconds(u64)` 这样的数值量类型通常不需要这些。

## 泛型读写函数按值接受 `R: Read` 与 `W: Write` (C-RW-VALUE) {#c-rw-value}

标准库包含以下两个 impl：

```rust
impl<'a, R: Read + ?Sized> Read for &'a mut R { /* ... */ }

impl<'a, W: Write + ?Sized> Write for &'a mut W { /* ... */ }
```

这意味着任何按值接受 `R: Read` 或 `W: Write` 泛型参数的函数，必要时都可用可变引用调用。

在此类函数的文档中，简要提醒用户可以传入可变引用。Rust 新手常在此卡住。他们可能已经打开了文件，
想从中读取多段数据，但读取一段的函数按值消费了 reader，于是他们束手无策。解决办法是利用上述
impl 之一，将 `&mut f` 而非 `f` 作为 reader 参数传入。

### 示例

- [`flate2::read::GzDecoder::new`]
- [`flate2::write::GzEncoder::new`]
- [`serde_json::from_reader`]
- [`serde_json::to_writer`]

[`flate2::read::GzDecoder::new`]: https://docs.rs/flate2/0.2/flate2/read/struct.GzDecoder.html#method.new
[`flate2::write::GzEncoder::new`]: https://docs.rs/flate2/0.2/flate2/write/struct.GzEncoder.html#method.new
[`serde_json::from_reader`]: https://docs.serde.rs/serde_json/fn.from_reader.html
[`serde_json::to_writer`]: https://docs.serde.rs/serde_json/fn.to_writer.html
