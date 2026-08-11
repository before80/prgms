+++
title = "3.10 PhantomData"
date = 2026-08-06T17:08:00+08:00
weight = 20
type = "docs"
description = "PhantomData 与 drop 检查"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# PhantomData


> 原文链接: [https://doc.rust-lang.org/nomicon/phantom-data.html](https://doc.rust-lang.org/nomicon/phantom-data.html)


　　处理 unsafe 代码时，常会遇到类型或生命周期在逻辑上与结构体关联，却并非实际字段的情况。最常见的是生命周期。例如 `&'a [T]` 的 `Iter`（近似）定义如下：

```rust,compile_fail
struct Iter<'a, T: 'a> {
    ptr: *const T,
    end: *const T,
}
```

　　但由于 `'a` 在结构体体内未使用，它是*无界*的。
　　[因历史上由此引发的问题][unused-param]，
　　结构体定义中禁止无界生命周期和类型。
　　因此必须在体内以某种方式引用这些类型。
　　正确做法是获得正确的型变和 drop 检查。

[unused-param]: https://rust-lang.github.io/rfcs/0738-variance.html#the-corner-case-unused-parameters-and-parameters-that-are-only-used-unsafely

　　我们使用 `PhantomData`——一种特殊标记类型。`PhantomData`
　　不占空间，但在静态分析中模拟给定类型的字段。这比显式告诉类型系统期望的型变种类更不易出错，同时提供 auto trait 和 drop 检查所需信息等有用特性。

　　`Iter` 在逻辑上包含一堆 `&'a T`，因此正是我们让 `PhantomData` 模拟的：

```rust
use std::marker;

struct Iter<'a, T: 'a> {
    ptr: *const T,
    end: *const T,
    _marker: marker::PhantomData<&'a T>,
}
```

　　就这样。生命周期会有界，迭代器对 `'a` 和 `T` 协变。一切正常运行。

## 泛型参数与 drop 检查

　　过去还有另一点需要考虑。

　　本文档曾写道：

> 另一个重要例子是 Vec，（近似）定义如下：
>
> ```rust
> struct Vec<T> {
>     data: *const T, // *const 用于型变！
>     len: usize,
>     cap: usize,
> }
> ```
>
> 与上一例不同，*看似*一切正是我们想要的。Vec 的每个泛型参数都出现在至少一个字段中。
> 可以开始了！
>
> 并非如此。
>
> drop 检查器会宽松地判定 `Vec<T>` 不拥有任何 `T` 类型的值。进而认为不必在确定 drop 检查 soundness 时担心 Vec 在析构函数中 drop 任何 `T`。进而允许人们利用 Vec 的析构函数制造 unsoundness。
>
> 要告诉 drop 检查器我们*确实*拥有 `T` 类型的值，因此在*我们* drop 时可能 drop 一些 `T`，必须添加额外的 `PhantomData` 明确说明：
>
> ```rust
> use std::marker;
>
> struct Vec<T> {
>     data: *const T, // *const 用于型变！
>     len: usize,
>     cap: usize,
>     _owns_T: marker::PhantomData<T>,
> }
> ```

　　但自 [RFC 1238](https://rust-lang.github.io/rfcs/1238-nonparametric-dropck.html) 起，
　　**这已不再成立，也不再必要**。

　　若你写成：

```rust
struct Vec<T> {
    data: *const T, // `*const` 用于型变！
    len: usize,
    cap: usize,
}

# #[cfg(any())]
impl<T> Drop for Vec<T> { /* … */ }
```

　　则 `impl<T> Drop for Vec<T>` 的存在使 Rust 认为该 `Vec<T>` _拥有_ `T` 类型的值（更准确地说：可能在 `Drop` 实现中使用 `T` 类型的值），因此 drop `Vec<T>` 时不允许它们 _悬垂_（dangle）。

　　若类型已有 `Drop` impl，**再添加 `_owns_T: PhantomData<T>` 字段
　　对 dropck 而言是 _多余的_，毫无作用**（仍影响型变和 auto trait）。

  - （高级边角：若包含 `PhantomData` 的类型完全没有 `Drop` impl，
　　    但仍有 drop glue（因*另一个*字段有 drop glue），则本文提到的 dropck/`#[may_dangle]` 考虑同样适用：此时 `PhantomData<T>` 字段会在包含类型离开作用域时要求 `T` 可 drop。）

___

　　但这有时会导致过度严格的代码。因此标准库使用 unstable 且 `unsafe` 的属性，选择回到本文档曾警告的旧「未检查」drop 检查行为：`#[may_dangle]` 属性。

### 例外：标准库及其 unstable `#[may_dangle]` 的特殊情况

　　若你只写自己的库代码，可跳过本节；但若好奇标准库实际 `Vec` 定义，你会注意到它仍需要 `_owns_T: PhantomData<T>` 字段以保证 soundness。

<details><summary>点击了解原因</summary>

　　考虑以下例子：

```rust
fn main() {
    let mut v: Vec<&str> = Vec::new();
    let s: String = "Short-lived".into();
    v.push(&s);
    drop(s);
} // <- `v` 在此被 drop
```

　　在经典的 `impl<T> Drop for Vec<T> {` 定义下，上面代码[会被拒绝]。

[会被拒绝]: https://rust.godbolt.org/z/ans15Kqz3

　　此例中我们有 `Vec</* T = */ &'s str>`——存 `'s` 生命周期的 `str` 引用的 vector，但在 `let s: String` 中，`s` 在 `Vec` 之前被 drop，
　　因此 drop `Vec` 时 `'s` **已过期**，
　　会使用 `impl<'s> Drop for Vec<&'s str> {`。

　　若使用这样的 `Drop`，它将处理 _过期_ 或 _悬垂_ 的生命周期 `'s`。这与 Rust 原则相悖——默认情况下函数签名中涉及的所有 Rust 引用都是非悬垂、可解引用的。

　　因此 Rust 必须保守地拒绝此片段。

　　然而对真正的 `Vec`，`Drop` impl 并不关心 `&'s str`，
　　_因为它自身没有 drop glue_：它只想释放底层缓冲区。

　　换句话说，若能通过某种方式接受上面片段就好了——为 `Vec` 特判，或依赖 `Vec` 的某种特殊性质：`Vec` 可 _承诺在 drop 时不使用其持有的 `&'s str`_。

　　这类 `unsafe` 承诺可用 `#[may_dangle]` 表达：

```rust ,ignore
unsafe impl<#[may_dangle] 's> Drop for Vec<&'s str> { /* … */ }
```

　　或更一般地：

```rust ,ignore
unsafe impl<#[may_dangle] T> Drop for Vec<T> { /* … */ }
```

　　是以 `unsafe` 方式选择退出 Rust drop 检查器对被 drop 实例的类型参数不允许悬垂的保守假设。

　　标准库这样做时，在 `T` 自身有 drop glue 的情况下必须谨慎。此例中，把 `&'s str` 换成 `struct PrintOnDrop<'s> /* = */ (&'s str);`，其 `Drop` impl 会解引用并打印内部的 `&'s str`。

　　确实，在释放底层缓冲区之前，`Drop for Vec<T> {` 在 `T` 有 drop glue 时必须递归 drop 每个 `T` 项；对 `PrintOnDrop<'s>` 而言，意味着
　　`Drop for Vec<PrintOnDrop<'s>>` 在释放底层缓冲区前必须递归 drop `PrintOnDrop<'s>` 元素。

　　因此说 `'s` `#[may_dangle]` 是过于宽松的表述。我们更希望说：「`'s` 可悬垂，前提是不参与某种递归 drop glue」。或更一般：「`T` 可悬垂，前提是不参与某种递归 drop glue」。这种「例外的例外」在**我们拥有 `T`** 时普遍存在。因此 Rust 的 `#[may_dangle]` 足够智能，知道此退出机制，并在_泛型参数以 owned 方式被结构体字段持有_时禁用该退出机制。

　　因此标准库最终得到：

```rust
# #[cfg(any())]
// 我们郑重承诺 drop `Vec` 时不使用 `T`……
unsafe impl<#[may_dangle] T> Drop for Vec<T> {
    fn drop(&mut self) {
        unsafe {
            if mem::needs_drop::<T>() {
                /* … 除了这里，即…… */
                ptr::drop_in_place::<[T]>(/* … */);
            }
            // …
            dealloc(/* … */)
            // …
        }
    }
}

struct Vec<T> {
    // … 除了 `Vec` 拥有 `T` 项、
    // 因而 drop 时可能 drop `T` 项这一事实！
    _owns_T: core::marker::PhantomData<T>,

    ptr: *const T, // `*const` 用于型变（但这本身并不表达拥有 `T`）
    len: usize,
    cap: usize,
}
```

</details>

___

　　拥有内存分配的裸指针是如此普遍的模式，标准库为此提供了 `Unique<T>` 工具，它：

* 包装 `*const T` 以实现型变
* 包含 `PhantomData<T>`
* 自动 derive `Send`/`Sync`，仿佛包含 `T`
* 将指针标记为 `NonZero` 以实现空指针优化

## `PhantomData` 模式表

　　下面是 `PhantomData` 各种用法的表格：

| Phantom 类型                | `'a` 的型变 | `T` 的型变   | `Send`/`Sync`<br/>（或缺乏）       | drop glue 中悬垂的 `'a` 或 `T`<br/>（_例如_ `#[may_dangle] Drop`） |
|-----------------------------|:----------------:|:-----------------:|:-----------------------------------------:|:------------------------------------------------:|
| `PhantomData<T>`            | -                | **协**变     | 继承                                 | 禁止（「拥有 `T`」）                          |
| `PhantomData<&'a T>`        | **协**变    | **协**变     | `Send + Sync`<br/>要求<br/>`T : Sync` | 允许                                          |
| `PhantomData<&'a mut T>`    | **协**变    | **不**变     | 继承                                 | 允许                                          |
| `PhantomData<*const T>`     | -                | **协**变     | `!Send + !Sync`                           | 允许                                          |
| `PhantomData<*mut T>`       | -                | **不**变     | `!Send + !Sync`                           | 允许                                          |
| `PhantomData<fn(T)>`        | -                | **逆**变 | `Send + Sync`                             | 允许                                          |
| `PhantomData<fn() -> T>`    | -                | **协**变     | `Send + Sync`                             | 允许                                          |
| `PhantomData<fn(T) -> T>`   | -                | **不**变     | `Send + Sync`                             | 允许                                          |
| `PhantomData<Cell<&'a ()>>` | **不**变    | -                 | `Send + !Sync`                            | 允许                                          |

  - 注：要退出 `Unpin` auto trait，需使用专用的 [`PhantomPinned`] 类型。

[`PhantomPinned`]: ../core/marker/struct.PhantomPinned.html
