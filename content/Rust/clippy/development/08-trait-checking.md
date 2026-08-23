+++
title = "08-Trait 检查"
date = 2026-08-22T18:00:00+08:00
weight = 78
type = "docs"
description = "trait 检查相关 lint"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Trait 检查 {#trait-checking}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/trait_checking.html](https://doc.rust-lang.org/nightly/clippy/development/trait_checking.html)


除[类型检查](type_checking.md)外，实现 lint 时我们可能还想检查特定类型 `Ty` 是否实现了某 trait。
有三种做法，取决于目标 trait 是否有[诊断项（diagnostic item）][diagnostic_items]、[语言项（lang item）][lang_items]，或两者皆无。

## 使用诊断项

如 [Rust 编译器开发指南][rustc_dev_guide] 所述，诊断项通过 [Symbol][symbol] 标识类型。

例如要检查表达式是否实现 `Iterator` trait，可写：

```rust
use clippy_utils::sym;
use clippy_utils::ty::implements_trait;
use rustc_hir::Expr;
use rustc_lint::{LateContext, LateLintPass};

impl LateLintPass<'_> for CheckIteratorTraitLint {
    fn check_expr(&mut self, cx: &LateContext<'_>, expr: &Expr<'_>) {
        let implements_iterator = (cx.tcx.get_diagnostic_item(sym::Iterator))
            .is_some_and(|id| implements_trait(cx, cx.typeck_results().expr_ty(expr), id, &[]));
        if implements_iterator {
            // [...]
        }

    }
}
```

> **注意**：所有已定义的 `Symbol` 见[此索引][symbol_index]。

## 使用语言项

除诊断项外，也可使用 [`lang_items`][lang_items]。
查看文档可知 `LanguageItems` 包含编译器中定义的所有语言项。

通过其 `*_trait` 方法，可获取任意特定项的 [DefId]，如 `Clone`、`Copy`、`Drop`、`Eq` 等 Rustacean 熟悉的 trait。

例如要检查表达式 `expr` 是否实现 `Drop` trait，可通过 `LateContext` 的
[TyCtxt] 访问 `LanguageItems`，其 `lang_items` 方法会返回 `Drop` trait 的 id。再调用 Clippy 工具函数 `implements_trait` 检查 `expr` 的 `Ty` 是否实现该 trait：

```rust
use clippy_utils::ty::implements_trait;
use rustc_hir::Expr;
use rustc_lint::{LateContext, LateLintPass};

impl LateLintPass<'_> for CheckDropTraitLint {
    fn check_expr(&mut self, cx: &LateContext<'_>, expr: &Expr<'_>) {
        let ty = cx.typeck_results().expr_ty(expr);
        if cx.tcx.lang_items()
            .drop_trait()
            .map_or(false, |id| implements_trait(cx, ty, id, &[])) {
                println!("`expr` implements `Drop` trait!");
            }
    }
}
```

## 使用类型路径

若既无诊断项也无语言项，可用 [`clippy_utils::paths`][paths] 获取 trait 的 `DefId`。

> **注意**：应尽量避免此法；最好向 [`rust-lang/rust`][rust] 提 PR 添加诊断项。

下面检查给定 `expr` 是否实现 [`core::iter::Step`](https://doc.rust-lang.org/std/iter/trait.Step.html)：

```rust
use clippy_utils::paths;
use clippy_utils::ty::implements_trait;
use rustc_hir::Expr;
use rustc_lint::{LateContext, LateLintPass};

impl LateLintPass<'_> for CheckIterStep {
    fn check_expr(&mut self, cx: &LateContext<'_>, expr: &Expr<'_>) {
        let ty = cx.typeck_results().expr_ty(expr);
        if let Some(trait_def_id) = paths::ITER_STEP.first(cx)
            && implements_trait(cx, ty, trait_def_id, &[])
        {
            println!("`expr` implements the `core::iter::Step` trait!");
        }
    }
}
```

## 以编程方式创建类型

Trait 常对类型参数泛化，例如 `Borrow<T>` 对 `T` 泛化。
Rust 允许为特定类型实现 trait。例如可为假设类型 `Foo` 实现 `Borrow<[u8]>`。
假设我们要判断该类型是否实际实现了 `Borrow<[u8]>`。

可使用与上文相同的 `implements_trait` 函数，传入表示 `[u8]` 的类型参数。由于 `[u8]` 是 `[T]` 的特化，可用 [`Ty::new_slice`][new_slice] 创建表示 `[T]` 的类型，并以 `u8` 为类型参数。
要以编程方式创建 `ty::Ty`，我们依赖 `Ty::new_*` 方法。这些方法创建 `TyKind` 再包装为 `Ty` 结构体，因此可访问所有原生类型，如 `Ty::new_char`、`Ty::new_bool`、`Ty::new_int` 等，也可由这些基本块构建切片、元组、引用等更复杂类型。

对于 trait 检查，仅创建类型不够，还需转换为 [GenericArg]。在 rustc 中，泛型是编译器理解的实体，有类型、常量与生命周期三种，对构造的 [Ty] 调用 `.into()` 即可包装为泛型，供查询系统判断是否实现了特化 trait。

以下代码演示做法：

```rust

use rustc_middle::ty::Ty;
use clippy_utils::sym;
use clippy_utils::ty::implements_trait;

let ty = todo!("Get the `Foo` type to check for a trait implementation");
let borrow_id = cx.tcx.get_diagnostic_item(sym::Borrow).unwrap(); // 实际代码中避免 unwrap
let slice_of_bytes_t = Ty::new_slice(cx.tcx, cx.tcx.types.u8);
let generic_param = slice_of_bytes_t.into();
if implements_trait(cx, ty, borrow_id, &[generic_param]) {
    todo!("Rest of lint implementation")
}
```

本质上，[Ty] 结构体让我们能以编译器与查询引擎可用的表示以编程方式创建类型。然后我们使用感兴趣类型的 `rustc_middle::Ty`，查询编译器是否确实实现了我们关心的 trait。


[DefId]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_hir/def_id/struct.DefId.html
[diagnostic_items]: https://rustc-dev-guide.rust-lang.org/diagnostics/diagnostic-items.html
[lang_items]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_hir/lang_items/struct.LanguageItems.html
[paths]: https://github.com/rust-lang/rust-clippy/blob/master/clippy_utils/src/paths.rs
[rustc_dev_guide]: https://rustc-dev-guide.rust-lang.org/
[symbol]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_span/symbol/struct.Symbol.html
[symbol_index]: https://doc.rust-lang.org/beta/nightly-rustc/rustc_span/symbol/sym/index.html
[TyCtxt]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/context/struct.TyCtxt.html
[Ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.Ty.html
[rust]: https://github.com/rust-lang/rust
[new_slice]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.Ty.html#method.new_slice
[GenericArg]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.GenericArg.html
