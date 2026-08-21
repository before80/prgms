+++
title = "第4章 类型与约束"
date = 2026-08-18T22:00:00+08:00
weight = 50
type = "docs"
description = "类型与约束 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/types.html](https://doc.rust-lang.org/nightly/style-guide/types.html)

# 类型与约束

## 单行格式 {#single-line-formatting}

- `[T]` 无空格
- `[T; expr]`，例如 `[u32; 42]`、`[Vec<Foo>; 10 * 2 + foo()]`（冒号后有空格，方括号两侧无空格）
- `*const T`、`*mut T`（`*` 后无空格，类型前有空格）
- `&'a T`、`&T`、`&'a mut T`、`&mut T`（`&` 后无空格，其余词之间用单个空格分隔）
- `unsafe extern "C" fn<'a, 'b, 'c>(T, U, V) -> W` 或 `fn()`（关键字与符号两侧、以及逗号后使用单个空格，无尾随逗号，括号两侧无空格）
- `!` 按普通类型名处理，如同 `Name`
- `(A, B, C, D)`（逗号后有空格，圆括号两侧无空格；除非是一元组，否则无尾随逗号）
- `<Baz<T> as SomeTrait>::Foo::Bar` 或 `Foo::Bar` 或 `::Foo::Bar`（`::` 与尖括号两侧无空格，`as` 两侧各一个空格）
- `Foo::Bar<T, U, V>`（逗号后有空格，无尾随逗号，尖括号两侧无空格）
- `T + T + T`（类型与 `+` 之间各一个空格）。
- `impl T + T + T`（关键字、类型与 `+` 之间各一个空格）。

类型中使用的圆括号两侧不要加空格，例如 `(Foo)`

## 换行 {#line-breaks}

类型中尽量避免换行。优先在最外层作用域处换行，例如优先使用

```rust
Foo<
    Bar,
    Baz<Type1, Type2>,
>
```

而不是

```rust
Foo<Bar, Baz<
    Type1,
    Type2,
>>
```

若类型必须换行才能排下，本节说明必要时应在何处断开。

必要时在 `[T; expr]` 的 `;` 之后换行。

函数类型按函数声明的规则换行。

泛型类型按泛型的规则换行。

含 `+` 的类型在 `+` 之前换行，并对后续行使用块缩进。对此类类型换行时，在*每一个* `+` 之前都换行：

```rust
impl Clone
    + Copy
    + Debug

Box<
    Clone
    + Copy
    + Debug
>
```

## 精确捕获约束 {#precise-capturing-bounds}

`use<'a, T>` 精确捕获约束的格式，如同带有非 turbofish 尖括号参数的单个路径段，也如同标识符为 `use` 的 trait 约束。

```rust
fn foo() -> impl Sized + use<'a> {}

// 格式化方式类似于：

fn foo() -> impl Sized + Use<'a> {}
```
