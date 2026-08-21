+++
title = "第5章 可预测性"
date = 2026-08-18T21:50:00+08:00
weight = 70
type = "docs"
description = "可预测性 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/predictability.html](https://rust-lang.github.io/api-guidelines/predictability.html)

# 可预测性

## 智能指针不添加固有方法 (C-SMART-PTR) {#c-smart-ptr}

例如，这就是为何 [`Box::into_raw`] 函数如此定义。

[`Box::into_raw`]: https://doc.rust-lang.org/std/boxed/struct.Box.html#method.into_raw

```rust
impl<T> Box<T> where T: ?Sized {
    fn into_raw(b: Box<T>) -> *mut T { /* ... */ }
}

let boxed_str: Box<str> = /* ... */;
let ptr = Box::into_raw(boxed_str);
```

若改为定义为固有方法，则在调用处会令人困惑：被调用的究竟是 `Box<T>` 上的方法，还是 `T` 上的方法。

```rust
impl<T> Box<T> where T: ?Sized {
    // 不要这样做。
    fn into_raw(self) -> *mut T { /* ... */ }
}

let boxed_str: Box<str> = /* ... */;

// 这是通过智能指针的 Deref 实现访问的 str 上的方法。
boxed_str.chars()

// 这是 Box<str> 上的方法……？
boxed_str.into_raw()
```

## 转换位于所涉最具体的类型上 (C-CONV-SPECIFIC) {#c-conv-specific}

有疑问时，优先使用 `to_`/`as_`/`into_` 而非 `from_`，因为它们用起来更符合人体工程学（且可与其他方法链式调用）。

对于许多两种类型之间的转换，其中一种类型明显更“具体”：它提供了另一种类型所不具备的额外不变量或解释。例如，[`str`] 比 `&[u8]` 更具体，因为它是 UTF-8 编码的字节序列。

[`str`]: https://doc.rust-lang.org/std/primitive.str.html

转换应放在所涉及类型中更具体的那一侧。因此，`str` 既提供了 [`as_bytes`] 方法，也提供了 [`from_utf8`] 构造器，用于与 `&[u8]` 值之间的相互转换。这一约定不仅直观，还能避免用无穷无尽的转换方法污染像 `&[u8]` 这样的具体类型。

[`as_bytes`]: https://doc.rust-lang.org/std/primitive.str.html#method.as_bytes
[`from_utf8`]: https://doc.rust-lang.org/std/str/fn.from_utf8.html

## 有明确接收者的函数应是方法 (C-METHOD) {#c-method}

对于任何明显与某一特定类型相关联的操作，优先使用

```rust
impl Foo {
    pub fn frob(&self, w: widget) { /* ... */ }
}
```

而非

```rust
pub fn frob(foo: &Foo, w: widget) { /* ... */ }
```

方法相对函数有诸多优势：

* 使用时无需导入或限定：只需拥有适当类型的值。
* 调用时会执行自动借用（包括可变借用）。
* 便于回答“对类型 `T` 的值我能做什么”这一问题（尤其是在使用 rustdoc 时）。
* 提供 `self` 记法，更简洁，也往往更能清晰传达所有权上的区别。

## 函数不使用输出参数 (C-NO-OUT) {#c-no-out}

对于返回多个 `Bar` 值，优先使用

```rust
fn foo() -> (Bar, Bar)
```

而非

```rust
fn foo(output: &mut Bar) -> Bar
```

像元组和结构体这样的复合返回类型会被高效编译，且不需要堆分配。若函数需要返回多个值，应通过这类类型之一来完成。

主要例外：有时函数旨在修改调用方已经拥有的数据，例如复用缓冲区：

```rust
fn read(&mut self, buf: &mut [u8]) -> io::Result<usize>
```

## 运算符重载不令人意外 (C-OVERLOAD) {#c-overload}

带有内置语法的运算符（`*`、`|` 等）可通过实现 [`std::ops`] 中的 trait 为某一类型提供。这些运算符伴随强烈的期望：仅当某项运算与乘法有某种相似之处（并共享期望的性质，例如结合性）时才实现 `Mul`，其他 trait 同理。

[`std::ops`]: https://doc.rust-lang.org/std/ops/index.html#traits

## 只有智能指针实现 `Deref` 与 `DerefMut` (C-DEREF) {#c-deref}

`Deref` trait 在许多情形下会被编译器隐式使用，并与方法解析交互。相关规则专门为适配智能指针而设计，因此这些 trait 应仅用于该目的。

### 标准库中的示例

- [`Box<T>`](https://doc.rust-lang.org/std/boxed/struct.Box.html)
- [`String`](https://doc.rust-lang.org/std/string/struct.String.html) 是指向 [`str`](https://doc.rust-lang.org/std/primitive.str.html) 的智能指针
- [`Rc<T>`](https://doc.rust-lang.org/std/rc/struct.Rc.html)
- [`Arc<T>`](https://doc.rust-lang.org/std/sync/struct.Arc.html)
- [`Cow<'a, T>`](https://doc.rust-lang.org/std/borrow/enum.Cow.html)

## 构造器是静态固有方法 (C-CTOR) {#c-ctor}

在 Rust 中，“构造器”只是一种约定。围绕构造器命名有多种约定，其间的区分往往很微妙。

最基本的构造器形式是不带参数的 `new` 方法。

```rust
impl<T> Example<T> {
    pub fn new() -> Example<T> { /* ... */ }
}
```

构造器是它们所构造类型的静态（无 `self`）固有方法。再结合完全导入类型名的做法，这一约定会带来信息丰富而又简洁的构造：

```rust
use example::Example;

// 构造一个新的 Example。
let ex = Example::new();
```

名称 `new` 一般应用于实例化某一类型的主方法。有时它不带参数，如上面的示例。有时它确实接受参数，例如 [`Box::new`]，会传入要放入 `Box` 中的值。

某些类型的构造器——尤其是 I/O 资源类型——对其构造器使用不同的命名约定，如 [`File::open`]、[`Mmap::open`]、[`TcpStream::connect`] 和 [`UdpSocket::bind`]。在这些情况下，名称按领域需要选取。

同一类型往往有多种构造方式。此时常见做法是给次要构造器加上 `_with_foo` 后缀，如 [`Mmap::open_with_offset`]。不过若你的类型有大量构造选项，请考虑改用建造者模式（[C-BUILDER]）。

有些构造器是“转换构造器”，即从另一类型的已有值创建新类型的方法。它们的名称通常以 `from_` 开头，如 [`std::io::Error::from_raw_os_error`]。但也要注意十分类似的 `From` trait（[C-CONV-TRAITS]）。以 `from_` 为前缀的转换构造器与 `From<T>` 实现之间有三点区别。

- `from_` 构造器可以是 unsafe 的；`From` 实现则不行。一个例子是 [`Box::from_raw`]。
- `from_` 构造器可以接受额外参数，以消除源数据含义上的歧义，如 [`u64::from_str_radix`]。
- 仅当源数据类型足以确定输出数据类型的编码时，`From` 实现才合适。当输入只是一堆比特（如 [`u64::from_be`] 或 [`String::from_utf8`]）时，转换构造器的名称能够标明其含义。

[`Box::from_raw`]: https://doc.rust-lang.org/std/boxed/struct.Box.html#method.from_raw
[`u64::from_str_radix`]: https://doc.rust-lang.org/std/primitive.u64.html#method.from_str_radix
[`u64::from_be`]: https://doc.rust-lang.org/std/primitive.u64.html#method.from_be
[`String::from_utf8`]: https://doc.rust-lang.org/std/string/struct.String.html#method.from_utf8

请注意，类型同时实现 `Default` 与 `new` 构造器是常见且被期望的。对于两者都有的类型，它们的行为应当一致。任一方都可以用另一方来实现。

[C-BUILDER]: ../type-safety/#c-builder
[C-CONV-TRAITS]: ../interoperability/#c-conv-traits
### 标准库中的示例

- [`std::io::Error::new`] 是 IO 错误常用的构造器。
- [`std::io::Error::from_raw_os_error`] 是基于从操作系统收到的错误码的转换构造器。
- [`Box::new`] 创建新的容器类型，接受单个参数。
- [`File::open`] 打开文件资源。
- [`Mmap::open_with_offset`] 打开内存映射文件，并带有额外选项。

[`File::open`]: https://doc.rust-lang.org/stable/std/fs/struct.File.html#method.open
[`Mmap::open`]: https://docs.rs/memmap/0.5.2/memmap/struct.Mmap.html#method.open
[`Mmap::open_with_offset`]: https://docs.rs/memmap/0.5.2/memmap/struct.Mmap.html#method.open_with_offset
[`TcpStream::connect`]: https://doc.rust-lang.org/stable/std/net/struct.TcpStream.html#method.connect
[`UdpSocket::bind`]: https://doc.rust-lang.org/stable/std/net/struct.UdpSocket.html#method.bind
[`std::io::Error::new`]: https://doc.rust-lang.org/std/io/struct.Error.html#method.new
[`std::io::Error::from_raw_os_error`]: https://doc.rust-lang.org/std/io/struct.Error.html#method.from_raw_os_error
[`Box::new`]: https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.new
