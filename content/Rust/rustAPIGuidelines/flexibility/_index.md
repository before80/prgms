+++
title = "第6章 灵活性"
date = 2026-08-18T21:50:00+08:00
weight = 80
type = "docs"
description = "灵活性 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/flexibility.html](https://rust-lang.github.io/api-guidelines/flexibility.html)

# 灵活性

## 函数暴露中间结果以避免重复工作 (C-INTERMEDIATE) {#c-intermediate}

许多回答某个问题的函数同时会算出相关的有趣数据。若这些数据可能对客户端有价值，请考虑在 API 中暴露它们。

### 标准库中的示例

- [`Vec::binary_search`] 并不返回表示是否找到该值的 `bool`，也不返回可能找到该值处下标的 `Option<usize>`。相反，它在找到时返回关于下标的信息，并在未找到时返回若要插入该值应使用的下标。

- [`String::from_utf8`] 在输入字节不是 UTF-8 时可能失败。在错误情形下，它返回一个中间结果：暴露输入中直至何处仍为有效 UTF-8 的字节偏移，并把输入字节的所有权交还给调用方。

- [`HashMap::insert`] 返回 `Option<T>`，即给定键原先存在的值（若有）。在用户希望恢复该值的场景中，由插入操作直接返回可避免用户再做一次哈希表查找。

[`Vec::binary_search`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.binary_search
[`String::from_utf8`]: https://doc.rust-lang.org/std/string/struct.String.html#method.from_utf8
[`HashMap::insert`]: https://doc.rust-lang.org/stable/std/collections/struct.HashMap.html#method.insert

## 由调用方决定数据复制与存放位置 (C-CALLER-CONTROL) {#c-caller-control}

若函数需要参数的所有权，应取得参数的所有权，而不是借用后再克隆该参数。

```rust
// 优先这样：
fn foo(b: Bar) {
    /* 直接以拥有所有权的方式使用 b */
}

// 而非这样：
fn foo(b: &Bar) {
    let b = b.clone();
    /* 克隆后以拥有所有权的方式使用 b */
}
```

若函数*不*需要参数的所有权，应取得参数的共享或独占借用，而不是取得所有权再丢弃该参数。

```rust
// 优先这样：
fn foo(b: &Bar) {
    /* 以借用方式使用 b */
}

// 而非这样：
fn foo(b: Bar) {
    /* 以借用方式使用 b，在函数返回前会隐式丢弃 */
}
```

`Copy` trait 应仅在绝对必要时用作约束，而不应作为暗示“复制很便宜”的方式。

## 函数用泛型尽量减少对参数的假设 (C-GENERIC) {#c-generic}

函数对其输入所作的假设越少，其适用范围就越广。

若函数只需遍历数据，优先使用

```rust
fn foo<I: IntoIterator<Item = i64>>(iter: I) { /* ... */ }
```

而非以下任一形式

```rust
fn foo(c: &[i64]) { /* ... */ }
fn foo(c: &Vec<i64>) { /* ... */ }
fn foo(c: &SomeOtherCollection<i64>) { /* ... */ }
```

更一般地，考虑用泛型精确刻画函数对其参数需要作出的假设。

### 泛型的优点

* _可复用性_。泛型函数可应用于开放式的类型集合，同时清晰约定这些类型必须提供的功能。

* _静态分发与优化_。每次使用泛型函数都会针对实现了 trait 约束的具体类型进行特化（“单态化”），这意味着 (1) trait 方法的调用是对实现的静态、直接调用，且 (2) 编译器可以内联并进一步优化这些调用。

* _内联布局_。若 `struct` 与 `enum` 类型对某个类型参数 `T` 泛型，则类型 `T` 的值会以内联方式布局在 `struct`/`enum` 中，没有间接层。

* _推断_。由于泛型函数的类型参数通常可被推断，在原本需要显式转换或其他方法调用的代码中，泛型函数有助于减少冗长。

* _精确类型_。因为泛型为实现某一 trait 的具体类型给出了*名字*，就有可能精确说明何处需要或产生该确切类型。例如，函数

  ```rust
  fn binary<T: Trait>(x: T, y: T) -> T
  ```

  保证消费并产生完全相同类型 `T` 的元素；不能用两个都实现 `Trait` 但却不同类型的参数来调用它。

### 泛型的缺点

* _代码体积_。特化泛型函数意味着函数体被复制。必须在代码体积增长与静态分发带来的性能收益之间权衡。

* _同质类型_。这是“精确类型”硬币的另一面：若 `T` 是类型参数，它代表*单一*的实际类型。因此例如 `Vec<T>` 包含单一具体类型的元素（而且向量的表示确实特化为将这些元素内联布局）。有时异构集合很有用；参见 [trait objects][C-OBJECT]。

* _签名冗长_。大量使用泛型会使函数签名更难阅读与理解。

[C-OBJECT]: #c-object

### 标准库中的示例

- [`std::fs::File::open`] 接受泛型类型 `AsRef<Path>` 的参数。这使得可以从字符串字面量 `"f.txt"`、[`Path`]、[`OsString`] 以及另外几种类型方便地打开文件。

[`std::fs::File::open`]: https://doc.rust-lang.org/std/fs/struct.File.html#method.open
[`Path`]: https://doc.rust-lang.org/std/path/struct.Path.html
[`OsString`]: https://doc.rust-lang.org/std/ffi/struct.OsString.html

## 若可能作为 trait object 有用则保持对象安全 (C-OBJECT) {#c-object}

Trait object 有一些重要限制：通过 trait object 调用的方法不能使用泛型，也不能在接收者位置以外使用 `Self`。

设计 trait 时，应尽早决定该 trait 将作为 object 使用，还是作为泛型上的约束使用。

若 trait 旨在作为 object 使用，其方法应接受并返回 trait object，而不是使用泛型。

可用 `Self: Sized` 的 `where` 子句把特定方法排除在该 trait 的 object 之外。下面的 trait 因含有泛型方法而不是对象安全的。

```rust
trait MyTrait {
    fn object_safe(&self, i: i32);

    fn not_object_safe<T>(&self, t: T);
}
```

给泛型方法加上 `Self: Sized` 要求后，它会被排除在 trait object 之外，从而使该 trait 成为对象安全的。

```rust
trait MyTrait {
    fn object_safe(&self, i: i32);

    fn not_object_safe<T>(&self, t: T) where Self: Sized;
}
```

### Trait object 的优点

* _异构性_。当你需要它时，你真的需要它。
* _代码体积_。与泛型不同，trait object 不会生成特化的（单态化的）代码版本，这可以大幅减小代码体积。

### Trait object 的缺点

* _无泛型方法_。Trait object 目前不能提供泛型方法。
* _动态分发与胖指针_。Trait object 本质上涉及间接与虚表分发，可能带来性能代价。
* _无 Self_。除方法接收者参数外，trait object 上的方法不能使用 `Self` 类型。

### 标准库中的示例

- [`io::Read`] 与 [`io::Write`] trait 经常作为 object 使用。
- [`Iterator`] trait 有若干泛型方法标有 `where Self: Sized`，以保留将 `Iterator` 作为 object 使用的能力。

[`io::Read`]: https://doc.rust-lang.org/std/io/trait.Read.html
[`io::Write`]: https://doc.rust-lang.org/std/io/trait.Write.html
[`Iterator`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html
