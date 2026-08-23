+++
title = "07-类型检查"
date = 2026-08-22T18:00:00+08:00
weight = 77
type = "docs"
description = "类型检查相关 lint"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 类型检查 {#type-checking}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/type_checking.html](https://doc.rust-lang.org/nightly/clippy/development/type_checking.html)


开发新 lint 或改进现有 lint 时，我们可能出于多种原因需要获取表达式 `Expr` 的类型 `Ty`。这可以通过 [`LateLintPass`][LateLintPass] 可用的 [`LateContext`][LateContext] 实现。

## `LateContext` 与 `TypeckResults`

lint 上下文 [`LateContext`][LateContext] 与 [`TypeckResults`][TypeckResults]（由 `LateContext::typeck_results` 返回）是 `LateLintPass` 中最有用的两个数据结构。它们让我们能跳转到类型定义及其他编译阶段（如 HIR）。

> 注意：`LateContext.typeck_results` 的返回类型是 [`TypeckResults`][TypeckResults]，在类型检查步骤中创建，包含表达式类型、方法解析方式等有用信息。

`TypeckResults` 包含 [`expr_ty`][expr_ty] 等有用方法，可访问给定表达式底层的 [`Ty`][Ty] 结构。

```rust
pub fn expr_ty(&self, expr: &Expr<'_>) -> Ty<'tcx>
```

顺带说明，除 `expr_ty` 外，[`TypeckResults`][TypeckResults] 还有 [`pat_ty()`][pat_ty] 方法，用于从模式获取类型。

## `Ty`

`Ty` 结构体包含表达式的类型信息。
让我们查看 `rustc_middle` 的 [`Ty`][Ty] 结构体：

```rust
pub struct Ty<'tcx>(Interned<'tcx, WithStableHash<TyS<'tcx>>>);
```

乍一看该结构体颇为晦涩，但细看会发现它包含许多对类型检查有用的方法。

例如 [`is_char`][is_char] 检查给定 `Ty` 是否对应原生字符类型。

### `is_*` 用法

某些场景下，我们只需检查表达式的 `Ty` 是否为特定类型（如 `char`），可写：

```rust
impl LateLintPass<'_> for MyStructLint {
    fn check_expr(&mut self, cx: &LateContext<'_>, expr: &Expr<'_>) {
        // 获取 `expr` 的类型
        let ty = cx.typeck_results().expr_ty(expr);

        // 检查该表达式的 `Ty` 是否为字符类型
        if ty.is_char() {
            println!("Our expression is a char!");
        }
    }
}
```

此外，若查看 `is_char` 的[源码][is_char_source]，会发现：

```rust
#[inline]
pub fn is_char(self) -> bool {
    matches!(self.kind(), Char)
}
```

我们发现了 `Ty` 的 [`kind()` 方法][kind]，它提供 `Ty` 的 [`TyKind`][TyKind]。

## `TyKind`

`TyKind` 定义 Rust 类型系统中的类型种类。
查看 [`TyKind` 文档][TyKind]，可见它是包含 `Bool`、`Int`、`Ref` 等 25 个以上变体的枚举。

### `kind` 用法

`Ty` 的 `TyKind` 可通过 [`Ty.kind()` 方法][kind] 获取。
在 Clippy 中，我们常用该方法进行模式匹配。

例如要检查是否为 `struct`，可判断 `ty.kind` 是否为 [`Adt`][Adt]（代数数据类型）且其 [`AdtDef`][AdtDef] 为 struct：

```rust
impl LateLintPass<'_> for MyStructLint {
    fn check_expr(&mut self, cx: &LateContext<'_>, expr: &Expr<'_>) {
        // 获取 `expr` 的类型
        let ty = cx.typeck_results().expr_ty(expr);
        // 匹配其 kind 以进入类型
        match ty.kind() {
            ty::Adt(adt_def, _) if adt_def.is_struct() => println!("Our `expr` is a struct!"),
            _ => ()
        }
    }
}
```

## `hir::Ty` 与 `ty::Ty`

本文一直在讨论 [`ty::Ty`][middle_ty]，但 [`hir::Ty`][hir_ty] 同样重要。

`hir::Ty` 表示*用户所写*的内容，而 `ty::Ty` 是编译器如何看待该类型，包含更多信息。示例：

```rust
fn foo(x: u32) -> u32 { x }
```

此处 HIR 看到的类型未经「深思」：函数接受 `u32` 并返回 `u32`。对 `hir::Ty` 而言，它们可能是不同类型。但在 `ty::Ty` 层面，编译器理解它们是同一类型，包括生命周期等细节……

要从 `hir::Ty` 得到 `ty::Ty`，在函数体外可用 [`lower_ty`][lower_ty]，
在函数体内可用 [`TypeckResults::node_type()`][node_type]。

> **警告**：不要在函数体内使用 `lower_ty`，否则可能导致 ICE。

## 以编程方式创建类型

以编程方式创建类型的常见用例是检查某类型是否实现某 trait（见 [Trait 检查](trait_checking.md)）。

以下示例创建 `u8` 切片类型 `Ty`，即 `[u8]`：

```rust
use rustc_middle::ty::Ty;
// 假设可访问 LateContext
let ty = Ty::new_slice(cx.tcx, Ty::new_u8());
```

一般而言，我们依赖 `Ty::new_*` 方法。这些方法定义类型系统与 trait 系统用来定义和理解所写代码的基本构建块。

## 有用链接

以下是进一步探索本章概念的链接：

- [编译阶段](https://rustc-dev-guide.rust-lang.org/compiler-src.html#the-main-stages-of-compilation)
- [诊断项（Diagnostic items）](https://rustc-dev-guide.rust-lang.org/diagnostics/diagnostic-items.html)
- [类型检查](https://rustc-dev-guide.rust-lang.org/hir-typeck/summary.html)
- [Ty 模块](https://rustc-dev-guide.rust-lang.org/ty.html)

[Adt]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_type_ir/ty_kind/enum.TyKind.html#variant.Adt
[AdtDef]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/adt/struct.AdtDef.html
[expr_ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.TypeckResults.html#method.expr_ty
[node_type]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.TypeckResults.html#method.node_type
[is_char]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.Ty.html#method.is_char
[is_char_source]: https://github.com/rust-lang/rust/blob/d34f1f931489618efffc4007e6b6bdb9e10f6467/compiler/rustc_middle/src/ty/sty.rs#L1429-L1432
[kind]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.Ty.html#method.kind
[LateContext]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/struct.LateContext.html
[LateLintPass]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.LateLintPass.html
[pat_ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/typeck_results/struct.TypeckResults.html#method.pat_ty
[Ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.Ty.html
[TyKind]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_type_ir/ty_kind/enum.TyKind.html
[TypeckResults]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.TypeckResults.html
[middle_ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.Ty.html
[hir_ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_hir/hir/struct.Ty.html
[lower_ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_hir_analysis/fn.lower_ty.html
