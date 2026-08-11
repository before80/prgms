+++
title = "4.1 强制转换（Coercion）"
date = 2026-08-06T17:08:00+08:00
weight = 23
type = "docs"
description = "Rust 的强制转换规则"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 强制转换（Coercion）


> 原文链接: [https://doc.rust-lang.org/nomicon/coercions.html](https://doc.rust-lang.org/nomicon/coercions.html)


　　类型可在特定上下文中隐式被强制转换而改变。
　　这些变化通常只是类型的*弱化*，主要围绕指针和生命周期。
　　它们主要存在是为了让 Rust 在更多情况下「开箱即用」，且大体无害。

　　强制转换类型的完整列表见 reference 的 [Coercion types] 章节。

　　注意，匹配 trait 时我们不执行强制转换（receiver 除外，见[下一页][dot-operator]）。
　　若某类型 `U` 有 `impl`，且 `T` 可强制转换为 `U`，这并不构成 `T` 的实现。
　　例如下面无法通过类型检查，尽管把 `t` 强制转换为 `&T` 没问题，且 `&T` 有 `impl`：

```rust,compile_fail
trait Trait {}

fn foo<X: Trait>(t: X) {}

impl<'a> Trait for &'a i32 {}

fn main() {
    let t: &mut i32 = &mut 0;
    foo(t);
}
```

　　失败信息如下：

```text
error[E0277]: the trait bound `&mut i32: Trait` is not satisfied
 --> src/main.rs:9:9
  |
3 | fn foo<X: Trait>(t: X) {}
  |           ----- required by this bound in `foo`
...
9 |     foo(t);
  |         ^ the trait `Trait` is not implemented for `&mut i32`
  |
  = help: the following implementations were found:
            <&'a i32 as Trait>
  = note: `Trait` is implemented for `&i32`, but not for `&mut i32`
```

[Coercion types]: ../reference/type-coercions.html#coercion-types
[dot-operator]: ./02-the-dot-operator.html
