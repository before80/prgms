+++
title = "05-子类型与可变性"
date = 2026-08-18T08:45:00+08:00
weight = 88
type = "docs"
description = "子类型与可变性 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/subtyping.html](https://doc.rust-lang.org/reference/subtyping.html)

r[subtype]
# 子类型与可变性

r[subtype.intro]
子类型是隐式的，可以发生在类型检查或推断的任何阶段。

r[subtype.kinds]
子类型仅限于两种情形：关于生命周期的型变，以及带有高阶生命周期的类型之间。若我们从类型中抹去生命周期，则唯一的子类型关系将来自类型相等。

考虑下面的例子：字符串字面量总是具有 `'static` 生命周期。尽管如此，我们仍可以将 `s` 赋给 `t`：

```rust
fn bar<'a>() {
    let s: &'static str = "hi";
    let t: &'a str = s;
}
```

由于 `'static` 长于生命周期参数 `'a`，`&'static str` 是 `&'a str` 的子类型。

r[subtype.higher-ranked]
[高阶][Higher-ranked][函数指针][function pointers]和 [trait 对象][trait objects]还有另一种子类型关系。它们是通过对高阶生命周期进行代换所得到类型的子类型。一些例子：

```rust
// 此处用 'static 代换 'a
let subtype: &(for<'a> fn(&'a i32) -> &'a i32) = &((|x| x) as fn(&_) -> &_);
let supertype: &(fn(&'static i32) -> &'static i32) = subtype;

// 这对 trait 对象同样适用
let subtype: &(dyn for<'a> Fn(&'a i32) -> &'a i32) = &|x| x;
let supertype: &(dyn Fn(&'static i32) -> &'static i32) = subtype;

// 我们也可以用一个高阶生命周期代换另一个
let subtype: &(for<'a, 'b> fn(&'a i32, &'b i32)) = &((|x, y| {}) as fn(&_, &_));
let supertype: &for<'c> fn(&'c i32, &'c i32) = subtype;
```

r[subtyping.variance]
## 型变

r[subtyping.variance.intro]
型变是泛型类型相对于其参数所具有的性质。泛型类型在某个参数上的 *型变* 描述了该参数的子类型关系如何影响该类型的子类型关系。

r[subtyping.variance.covariant]
* 若 `T` 是 `U` 的子类型蕴含 `F<T>` 是 `F<U>` 的子类型（子类型关系「穿透」），则 `F<T>` 在 `T` 上是 *协变* 的

r[subtyping.variance.contravariant]
* 若 `T` 是 `U` 的子类型蕴含 `F<U>` 是 `F<T>` 的子类型，则 `F<T>` 在 `T` 上是 *逆变* 的

r[subtyping.variance.invariant]
* 否则 `F<T>` 在 `T` 上是 *不变* 的（无法推导出子类型关系）

r[subtyping.variance.builtin-types]
类型的型变按如下方式自动确定

| 类型                          | 在 `'a` 上的型变  | 在 `T` 上的型变   |
|-------------------------------|-------------------|-------------------|
| `&'a T`                       | 协变              | 协变              |
| `&'a mut T`                   | 协变              | 不变              |
| `*const T`                    |                   | 协变              |
| `*mut T`                      |                   | 不变              |
| `[T]` 和 `[T; n]`             |                   | 协变              |
| `fn() -> T`                   |                   | 协变              |
| `fn(T) -> ()`                 |                   | 逆变              |
| `std::cell::UnsafeCell<T>`    |                   | 不变              |
| `std::marker::PhantomData<T>` |                   | 协变              |
| `dyn Trait<T> + 'a`           | 协变              | 不变              |

r[subtyping.variance.user-composite-types]
其他 `struct`、`enum` 和 `union` 类型的型变通过查看其字段类型的型变来决定。若该参数在具有不同型变的位置上被使用，则该参数是不变的。例如下面的结构体在 `'a` 和 `T` 上协变，在 `'b`、`'c` 和 `U` 上不变。

```rust
use std::cell::UnsafeCell;
struct Variance<'a, 'b, 'c, T, U: 'a> {
    x: &'a U,               // 这使 `Variance` 在 'a 上协变，并且会使它
                            // 在 U 上协变，但 U 稍后还会被使用
    y: *const T,            // 在 T 上协变
    z: UnsafeCell<&'b f64>, // 在 'b 上不变
    w: *mut U,              // 在 U 上不变，使整个结构体在 U 上不变

    f: fn(&'c ()) -> &'c () // 既协变又逆变，使 'c 在结构体中不变
}
```

r[subtyping.variance.builtin-composite-types]
当用在 `struct`、`enum` 或 `union` 之外时，参数的型变在每个位置分别检查。

```rust
## use std::cell::UnsafeCell;
fn generic_tuple<'short, 'long: 'short>(
    // 'long 在元组内部同时用于协变和不变位置。
    x: (&'long u32, UnsafeCell<&'long u32>),
) {
    // 由于这些位置的型变是分别计算的，
    // 我们可以在协变位置自由地缩短 'long。
    let _: (&'short u32, UnsafeCell<&'long u32>) = x;
}

fn takes_fn_ptr<'short, 'middle: 'short>(
    // 'middle 同时用于协变和逆变位置。
    f: fn(&'middle ()) -> &'middle (),
) {
    // 由于这些位置的型变是分别计算的，
    // 我们可以在协变位置自由地缩短 'middle，
    // 并在逆变位置延长它。
    let _: fn(&'static ()) -> &'short () = f;
}
```

[function pointers]: types/function-pointer.md
[Higher-ranked]: ../nomicon/hrtb.html
[trait objects]: types/trait-object.md
