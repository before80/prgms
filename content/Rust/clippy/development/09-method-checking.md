+++
title = "09-方法检查"
date = 2026-08-22T18:00:00+08:00
weight = 79
type = "docs"
description = "方法检查相关 lint"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 方法检查 {#method-checking}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/method_checking.html](https://doc.rust-lang.org/nightly/clippy/development/method_checking.html)


开发 lint 时，某些场景下需要检查方法。我们可能关心两类问题：

-   调用：表达式是否调用了特定方法？
-   定义：`impl` 是否定义了某方法？

## 检查 `expr` 是否调用特定方法

假设有 `expr`，可通过匹配 `expr.kind` 中的 [`ExprKind`] 判断是否调用特定方法（如 `our_fancy_method`）：

```rust
use rustc_hir as hir;
use rustc_lint::{LateContext, LateLintPass};
use clippy_utils::res::{MaybeDef, MaybeTypeckRes};
use clippy_utils::sym;

impl<'tcx> LateLintPass<'tcx> for OurFancyMethodLint {
    fn check_expr(&mut self, cx: &LateContext<'tcx>, expr: &'tcx hir::Expr<'_>) {
        // 用模式匹配检查 expr 是否调用方法
        if let hir::ExprKind::MethodCall(path, _, _, _) = &expr.kind
            // 检查方法名是否为 `our_fancy_method`
            && path.ident.name == sym::our_fancy_method
            // 检查方法是否属于 `sym::OurFancyTrait` trait
            // （例如 `map` 可能属于用户自定义 trait 而非 `Iterator`）
            // 更多信息见下一节
            && cx.ty_based_def(expr).opt_parent(cx).is_diag_item(cx, sym::OurFancyTrait)
        {
            println!("`expr` is a method call for `our_fancy_method`");
        }
    }
}
```

请仔细查看 [`MethodCall`] 这一 `ExprKind` 枚举变体以了解模式匹配。如 [定义 Lint](defining_lints.md#lint-类型) 所述，`methods` lint 类型中大量使用 `MethodCall` 模式匹配，读者可进一步探索。

`our_fancy_method` 等新 symbol 需添加到 `clippy_utils::sym` 模块。
该模块扩展了 `rustc_span::sym` 中编译器 crate 已提供的 symbol 列表。

若 trait 只定义一个方法（如 `std::ops::Deref` 仅有 `deref()`），可能想省略方法名检查。这可行，但不总是可取，因为：
- 若 trait 新增方法（可能有默认实现），可能误匹配错误方法。
- 比较 symbol 成本很低，且可能避免更昂贵的查找。

## 检查 `impl` 块是否实现某方法

有时我们要检查方法是否被调用，有时则想知道 `Ty` 是否定义了某方法。

要检查 `impl` 块是否定义 `our_fancy_method`，可使用 beloved [`LateLintPass`] 中的 [`check_impl_item`] 方法（更多信息见 Clippy 手册中的 ["Lint 遍历"](lint_passes.md) 一章）。该方法提供 [`ImplItem`] 结构体，表示 `impl` 块内的任意项。

以下示例检查类型是否实现 `our_fancy_method`：

```rust
use clippy_utils::{return_ty, sym};
use clippy_utils::res::MaybeDef;
use rustc_hir::{ImplItem, ImplItemKind};
use rustc_lint::{LateContext, LateLintPass};

impl<'tcx> LateLintPass<'tcx> for MyTypeImpl {
    fn check_impl_item(&mut self, cx: &LateContext<'tcx>, impl_item: &'tcx ImplItem<'_>) {
        // 检查项是否为方法/函数
        if let ImplItemKind::Fn(ref signature, _) = impl_item.kind
            // 检查方法是否名为 `our_fancy_method`
            && impl_item.ident.name.as_str() == "our_fancy_method"
            // 还可检查是否有 `self` 参数
            && signature.decl.implicit_self.has_implicit_self()
            // 甚至可检查返回类型是否为 `String`
            && return_ty(cx, impl_item.hir_id).is_diag_item(cx, sym::String)
        {
            println!("`our_fancy_method` is implemented!");
        }
    }
}
```

[`check_impl_item`]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_lint/trait.LateLintPass.html#method.check_impl_item
[`ExprKind`]: https://doc.rust-lang.org/beta/nightly-rustc/rustc_hir/hir/enum.ExprKind.html
[`ImplItem`]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_hir/hir/struct.ImplItem.html
[`LateLintPass`]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_lint/trait.LateLintPass.html
[`MethodCall`]: https://doc.rust-lang.org/beta/nightly-rustc/rustc_hir/hir/enum.ExprKind.html#variant.MethodCall
