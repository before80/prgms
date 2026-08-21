+++
title = "第1章 命名"
date = 2026-08-18T21:50:00+08:00
weight = 30
type = "docs"
description = "命名 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/naming.html](https://rust-lang.github.io/api-guidelines/naming.html)

# 命名

## 大小写遵循 RFC 430 (C-CASE) {#c-case}

基本的 Rust 命名约定在 [RFC 430] 中描述。

一般来说，Rust 倾向于对「类型级」构造（类型与 trait）使用 `UpperCamelCase`，对「值级」构造使用 `snake_case`。更精确地说：

| 项 | 约定 |
| ---- | ---------- |
| Crate | [尚不明确](https://github.com/rust-lang/api-guidelines/issues/29) |
| 模块 | `snake_case` |
| 类型 | `UpperCamelCase` |
| Trait | `UpperCamelCase` |
| 枚举变体 | `UpperCamelCase` |
| 函数 | `snake_case` |
| 方法 | `snake_case` |
| 一般构造器 | `new` 或 `with_more_details` |
| 转换构造器 | `from_some_other_type` |
| 宏 | `snake_case!` |
| 局部变量 | `snake_case` |
| 静态项 | `SCREAMING_SNAKE_CASE` |
| 常量 | `SCREAMING_SNAKE_CASE` |
| 类型参数 | 简洁的 `UpperCamelCase`，通常为单个大写字母：`T` |
| 生命周期 | 简短的 `lowercase`，通常为单个字母：`'a`、`'de`、`'src` |
| Feature | [尚不明确](https://github.com/rust-lang/api-guidelines/issues/101) 但参见 [C-FEATURE] |

在 `UpperCamelCase` 中，缩写词与复合词的缩略形式计为一个词：使用 `Uuid` 而非 `UUID`，使用 `Usize` 而非 `USize`，或使用 `Stdin` 而非 `StdIn`。在 `snake_case` 中，缩写词与缩略形式一律小写：`is_xid_start`。

在 `snake_case` 或 `SCREAMING_SNAKE_CASE` 中，「词」不应仅由单个字母构成，除非它是最后一个「词」。因此我们使用 `btree_map` 而非 `b_tree_map`，但使用 `PI_2` 而非 `PI2`。

Crate 名称不应使用 `-rs` 或 `-rust` 作为后缀或前缀。每个 crate 都是 Rust 的！反复提醒用户这一点毫无意义。

[RFC 430]: https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md
[C-FEATURE]: #c-feature

### 标准库中的示例

整个标准库。这条准则应当很容易遵守！

## 临时转换遵循 `as_`、`to_`、`into_` 约定 (C-CONV) {#c-conv}

转换应作为方法提供，名称前缀如下：

| 前缀 | 成本 | 所有权 |
| ------ | ---- | --------- |
| `as_` | 免费/无开销 | 借用 -\> 借用 |
| `to_` | 昂贵 | 借用 -\> 借用<br>借用 -\> 自有（非 Copy 类型）<br>自有 -\> 自有（Copy 类型） |
| `into_` | 不定 | 自有 -\> 自有（非 Copy 类型） |

例如：

- [`str::as_bytes()`] 将 `str` 视为 UTF-8 字节切片的视图，这是免费/无开销的。输入是借用的 `&str`，输出是借用的 `&[u8]`。
- [`Path::to_str`] 对操作系统路径的字节执行昂贵的 UTF-8 检查。输入与输出都是借用的。将其称为 `as_str` 并不正确，因为此方法在运行时有不可忽略的成本。
- [`str::to_lowercase()`] 产生 `str` 的 Unicode 正确小写等价形式，这需要遍历字符串中的字符，并可能需要内存分配。输入是借用的 `&str`，输出是自有的 `String`。
- [`f64::to_radians()`] 将浮点数量从度转换为弧度。输入是 `f64`。传入引用 `&f64` 并无必要，因为复制 `f64` 很廉价。将函数称为 `into_radians` 会有误导性，因为输入并未被消耗。
- [`String::into_bytes()`] 提取 `String` 底层的 `Vec<u8>`，这是免费/无开销的。它取得 `String` 的所有权，并返回自有的 `Vec<u8>`。
- [`BufReader::into_inner()`] 取得缓冲读取器的所有权并抽出底层读取器，这是免费/无开销的。缓冲区中的数据会被丢弃。
- [`BufWriter::into_inner()`] 取得缓冲写入器的所有权并抽出底层写入器，这可能需要对任何缓冲数据执行昂贵的 flush。

[`str::as_bytes()`]: https://doc.rust-lang.org/std/primitive.str.html#method.as_bytes
[`Path::to_str`]: https://doc.rust-lang.org/std/path/struct.Path.html#method.to_str
[`str::to_lowercase()`]: https://doc.rust-lang.org/std/primitive.str.html#method.to_lowercase
[`f64::to_radians()`]: https://doc.rust-lang.org/std/primitive.f64.html#method.to_radians
[`String::into_bytes()`]: https://doc.rust-lang.org/std/string/struct.String.html#method.into_bytes
[`BufReader::into_inner()`]: https://doc.rust-lang.org/std/io/struct.BufReader.html#method.into_inner
[`BufWriter::into_inner()`]: https://doc.rust-lang.org/std/io/struct.BufWriter.html#method.into_inner

以 `as_` 和 `into_` 为前缀的转换通常会 _降低抽象层次_，要么暴露底层表示的视图（`as`），要么将数据解构为其底层表示（`into`）。另一方面，以 `to_` 为前缀的转换通常停留在同一抽象层次，但会做一些工作以从一种表示变为另一种。

当某个类型包装单个值以将其与更高层语义关联时，应通过 `into_inner()` 方法提供对所包装值的访问。这适用于提供缓冲的包装器（如 [`BufReader`]）、编码或解码（如 [`GzDecoder`]）、原子访问（如 [`AtomicBool`]），或任何类似语义。

[`BufReader`]: https://doc.rust-lang.org/std/io/struct.BufReader.html#method.into_inner
[`GzDecoder`]: https://docs.rs/flate2/0.2.19/flate2/read/struct.GzDecoder.html#method.into_inner
[`AtomicBool`]: https://doc.rust-lang.org/std/sync/atomic/struct.AtomicBool.html#method.into_inner

如果转换方法名称中的 `mut` 限定符构成返回类型的一部分，它的出现位置应与其在类型中的位置一致。例如 [`Vec::as_mut_slice`] 返回 mut 切片；名副其实。此名称优于 `as_slice_mut`。

[`Vec::as_mut_slice`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.as_mut_slice

```rust
// 返回类型是 mut 切片。
fn as_mut_slice(&mut self) -> &mut [T];
```

##### 标准库中的更多示例

- [`Result::as_ref`](https://doc.rust-lang.org/std/result/enum.Result.html#method.as_ref)
- [`RefCell::as_ptr`](https://doc.rust-lang.org/std/cell/struct.RefCell.html#method.as_ptr)
- [`slice::to_vec`](https://doc.rust-lang.org/std/primitive.slice.html#method.to_vec)
- [`Option::into_iter`](https://doc.rust-lang.org/std/option/enum.Option.html#method.into_iter)

## Getter 名称遵循 Rust 约定 (C-GETTER) {#c-getter}

除少数例外，Rust 代码中的 getter 不使用 `get_` 前缀。

```rust
pub struct S {
    first: First,
    second: Second,
}

impl S {
    // 不是 get_first。
    pub fn first(&self) -> &First {
        &self.first
    }

    // 不是 get_first_mut、get_mut_first 或 mut_first。
    pub fn first_mut(&mut self) -> &mut First {
        &mut self.first
    }
}
```

仅当存在一个单一且显而易见、可以合理地由 getter 取得的对象时，才使用 `get` 命名。例如 [`Cell::get`] 访问 `Cell` 的内容。

[`Cell::get`]: https://doc.rust-lang.org/std/cell/struct.Cell.html#method.get

对于会做运行时校验（例如边界检查）的 getter，考虑添加 unsafe 的 `_unchecked` 变体。这些变体通常具有以下签名。

```rust
fn get(&self, index: K) -> Option<&V>;
fn get_mut(&mut self, index: K) -> Option<&mut V>;
unsafe fn get_unchecked(&self, index: K) -> &V;
unsafe fn get_unchecked_mut(&mut self, index: K) -> &mut V;
```

Getter 与转换（[C-CONV](#c-conv)）之间的区别可能很微妙，并非总是泾渭分明。例如 [`TempDir::path`] 可以理解为临时目录文件系统路径的 getter，而 [`TempDir::into_path`] 是一种转换，将删除临时目录的责任转移给调用者。由于 `path` 是 getter，将其称为 `get_path` 或 `as_path` 并不正确。

[`TempDir::path`]: https://docs.rs/tempdir/0.3.5/tempdir/struct.TempDir.html#method.path
[`TempDir::into_path`]: https://docs.rs/tempdir/0.3.5/tempdir/struct.TempDir.html#method.into_path

### 标准库中的示例

- [`std::io::Cursor::get_mut`](https://doc.rust-lang.org/std/io/struct.Cursor.html#method.get_mut)
- [`std::pin::Pin::get_mut`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.get_mut)
- [`std::sync::PoisonError::get_mut`](https://doc.rust-lang.org/std/sync/struct.PoisonError.html#method.get_mut)
- [`std::sync::atomic::AtomicBool::get_mut`](https://doc.rust-lang.org/std/sync/atomic/struct.AtomicBool.html#method.get_mut)
- [`std::collections::hash_map::OccupiedEntry::get_mut`](https://doc.rust-lang.org/std/collections/hash_map/struct.OccupiedEntry.html#method.get_mut)
- [`<[T]>::get_unchecked`](https://doc.rust-lang.org/std/primitive.slice.html#method.get_unchecked)

## 集合上产生迭代器的方法遵循 `iter`、`iter_mut`、`into_iter` (C-ITER) {#c-iter}

参见 [RFC 199]。

对于元素类型为 `U` 的容器，迭代器方法应命名为：

```rust
fn iter(&self) -> Iter             // Iter 实现 Iterator<Item = &U>
fn iter_mut(&mut self) -> IterMut  // IterMut 实现 Iterator<Item = &mut U>
fn into_iter(self) -> IntoIter     // IntoIter 实现 Iterator<Item = U>
```

本准则适用于概念上是同质集合的数据结构。作为反例，`str` 类型是保证为有效 UTF-8 的字节切片。这在概念上比同质集合更细致，因此它不提供 `iter`/`iter_mut`/`into_iter` 这一组迭代器方法，而是提供 [`str::bytes`] 按字节迭代，以及 [`str::chars`] 按字符迭代。

[`str::bytes`]: https://doc.rust-lang.org/std/primitive.str.html#method.bytes
[`str::chars`]: https://doc.rust-lang.org/std/primitive.str.html#method.chars

本准则仅适用于方法，不适用于函数。例如 `url` crate 中的 [`percent_encode`] 返回一个对百分号编码字符串片段的迭代器。使用 `iter`/`iter_mut`/`into_iter` 约定并不会带来更清晰的语义。

[`percent_encode`]: https://docs.rs/url/1.4.0/url/percent_encoding/fn.percent_encode.html
[RFC 199]: https://github.com/rust-lang/rfcs/blob/master/text/0199-ownership-variants.md

### 标准库中的示例

- [`Vec::iter`](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.iter)
- [`Vec::iter_mut`](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.iter_mut)
- [`Vec::into_iter`](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.into_iter)
- [`BTreeMap::iter`](https://doc.rust-lang.org/std/collections/struct.BTreeMap.html#method.iter)
- [`BTreeMap::iter_mut`](https://doc.rust-lang.org/std/collections/struct.BTreeMap.html#method.iter_mut)

## 迭代器类型名与产生它们的方法匹配 (C-ITER-TY) {#c-iter-ty}

名为 `into_iter()` 的方法应返回名为 `IntoIter` 的类型；所有其他返回迭代器的方法同理。

本准则主要适用于方法，但对函数往往也说得通。例如 `url` crate 中的 [`percent_encode`] 函数返回名为 [`PercentEncode`][PercentEncode-type] 的迭代器类型。

[PercentEncode-type]: https://docs.rs/url/1.4.0/url/percent_encoding/struct.PercentEncode.html

这些类型名在加上所属模块前缀时最有意义，例如 [`vec::IntoIter`]。

[`vec::IntoIter`]: https://doc.rust-lang.org/std/vec/struct.IntoIter.html

### 标准库中的示例

* [`Vec::iter`] 返回 [`Iter`][slice::Iter]
* [`Vec::iter_mut`] 返回 [`IterMut`][slice::IterMut]
* [`Vec::into_iter`] 返回 [`IntoIter`][vec::IntoIter]
* [`BTreeMap::keys`] 返回 [`Keys`][btree_map::Keys]
* [`BTreeMap::values`] 返回 [`Values`][btree_map::Values]

[`Vec::iter`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.iter
[slice::Iter]: https://doc.rust-lang.org/std/slice/struct.Iter.html
[`Vec::iter_mut`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.iter_mut
[slice::IterMut]: https://doc.rust-lang.org/std/slice/struct.IterMut.html
[`Vec::into_iter`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.into_iter
[vec::IntoIter]: https://doc.rust-lang.org/std/vec/struct.IntoIter.html
[`BTreeMap::keys`]: https://doc.rust-lang.org/std/collections/struct.BTreeMap.html#method.keys
[btree_map::Keys]: https://doc.rust-lang.org/std/collections/btree_map/struct.Keys.html
[`BTreeMap::values`]: https://doc.rust-lang.org/std/collections/struct.BTreeMap.html#method.values
[btree_map::Values]: https://doc.rust-lang.org/std/collections/btree_map/struct.Values.html

## Feature 名称不含占位词 (C-FEATURE) {#c-feature}

不要在 [Cargo feature] 的名称中包含毫无含义的词，例如 `use-abc` 或 `with-abc`。直接将 feature 命名为 `abc`。

[Cargo feature]: http://doc.crates.io/manifest.html#the-features-section

这种情况最常见于对 Rust 标准库有可选依赖的 crate。正确做法的标准方式是：

```toml
# 在 Cargo.toml 中

[features]
default = ["std"]
std = []
```

```rust
// 在 lib.rs 中
#![no_std]

#[cfg(feature = "std")]
extern crate std;
```

不要将 feature 称为 `use-std` 或 `with-std`，或任何并非 `std` 的创意名称。此命名约定与 Cargo 为可选依赖推断出的隐式 feature 命名一致。考虑 crate `x` 可选地依赖 Serde 以及 Rust 标准库：

```toml
[package]
name = "x"
version = "0.1.0"

[features]
std = ["serde/std"]

[dependencies]
serde = { version = "1.0", optional = true }
```

当我们依赖 `x` 时，可以用 `features = ["serde"]` 启用可选的 Serde 依赖。同样可以用 `features = ["std"]` 启用可选的标准库依赖。Cargo 为该可选依赖推断出的隐式 feature 称为 `serde`，而不是 `use-serde` 或 `with-serde`，因此我们希望显式 feature 的行为与此相同。

作为相关说明，Cargo 要求 feature 是可叠加的，因此像 `no-abc` 这样以否定方式命名的 feature 实际上几乎从不正确。

## 名称使用一致的词序 (C-WORD-ORDER) {#c-word-order}

以下是标准库中的一些错误类型：

- [`JoinPathsError`](https://doc.rust-lang.org/std/env/struct.JoinPathsError.html)
- [`ParseBoolError`](https://doc.rust-lang.org/std/str/struct.ParseBoolError.html)
- [`ParseCharError`](https://doc.rust-lang.org/std/char/struct.ParseCharError.html)
- [`ParseFloatError`](https://doc.rust-lang.org/std/num/struct.ParseFloatError.html)
- [`ParseIntError`](https://doc.rust-lang.org/std/num/struct.ParseIntError.html)
- [`RecvTimeoutError`](https://doc.rust-lang.org/std/sync/mpsc/enum.RecvTimeoutError.html)
- [`StripPrefixError`](https://doc.rust-lang.org/std/path/struct.StripPrefixError.html)

这些全部使用「动词-宾语-错误」词序。如果我们要添加一个表示地址解析失败的错误，为保持一致，应采用「动词-宾语-错误」词序将其命名为 `ParseAddrError`，而不是 `AddrParseError`。

具体选择哪种词序并不重要，但要注意 crate 内部的一致性，以及与标准库中类似功能的一致性。
