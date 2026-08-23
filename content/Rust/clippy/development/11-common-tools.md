+++
title = "11-常用工具"
date = 2026-08-22T18:00:00+08:00
weight = 81
type = "docs"
description = "编写 lint 的常用工具"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 常用工具 {#common-tools}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/common_tools_writing_lints.html](https://doc.rust-lang.org/nightly/clippy/development/common_tools_writing_lints.html)


编写 lint 时可能需要以下提示以掌握常见操作。

- [编写 lint 的常用工具](#编写-lint-的常用工具)
  - [获取表达式的类型](#获取表达式的类型)
  - [检查 expr 是否调用特定方法](#检查-expr-是否调用特定方法)
  - [检查特定类型](#检查特定类型)
  - [检查类型是否实现特定 trait](#检查类型是否实现特定-trait)
  - [检查类型是否定义特定方法](#检查类型是否定义特定方法)
  - [处理宏](#处理宏与展开)

有用的 Rustc 开发指南链接：
- [编译阶段](https://rustc-dev-guide.rust-lang.org/compiler-src.html#the-main-stages-of-compilation)
- [诊断项](https://rustc-dev-guide.rust-lang.org/diagnostics/diagnostic-items.html)
- [类型检查](https://rustc-dev-guide.rust-lang.org/type-checking.html)
- [Ty 模块](https://rustc-dev-guide.rust-lang.org/ty.html)

## 获取表达式的类型

有时需要获取表达式 `Expr` 的类型 `Ty`，例如回答：

- 该表达式对应哪种类型（通过其 [`TyKind`][TyKind]）？
- 是否为 sized 类型？
- 是否为原生类型？
- 是否实现某 trait？

该操作通过 [`TypeckResults`][TypeckResults] 结构体的 [`expr_ty()`][expr_ty] 方法完成，可访问底层 [`Ty`][Ty] 结构。

使用示例：
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

类似地，[`TypeckResults`][TypeckResults] 还有 [`pat_ty()`][pat_ty] 方法从模式获取类型。

此处两点值得注意：
- `cx` 是 lint 上下文 [`LateContext`][LateContext]。该上下文中最有用的数据结构是 `tcx` 与 `LateContext::typeck_results` 返回的 `TypeckResults`，可跳转到类型定义及其他编译阶段（如 HIR）。
- `typeck_results` 的返回类型是 [`TypeckResults`][TypeckResults]，在类型检查步骤创建，包含表达式类型、方法解析方式等。

## 检查 expr 是否调用特定方法

从 `expr` 出发，可检查是否调用特定方法 `some_method`：

```rust
impl<'tcx> LateLintPass<'tcx> for MyStructLint {
    fn check_expr(&mut self, cx: &LateContext<'tcx>, expr: &'tcx hir::Expr<'_>) {
        // 检查 expr 是否调用方法
        if let hir::ExprKind::MethodCall(path, _, _self_arg, ..) = &expr.kind
            // 检查方法名是否为 `some_method`
            && path.ident.name == sym::some_method
            // 可选：检查 self 参数的类型
            // - 见「检查特定类型」
        {
                // ...
        }
    }
}
```

## 检查特定类型

有三种方式检查表达式类型是否为我们要查的特定类型。这些方法只检查基础类型，泛型参数需单独检查。

```rust
use clippy_utils::{paths, sym};
use clippy_utils::res::MaybeDef;
use rustc_hir::LangItem;

impl LateLintPass<'_> for MyStructLint {
    fn check_expr(&mut self, cx: &LateContext<'_>, expr: &Expr<'_>) {
        // 获取表达式类型
        let ty = cx.typeck_results().expr_ty(expr);

        // 1. 使用诊断项
        // 最后一个参数是要检查的诊断项
        if ty.is_diag_item(cx, sym::Option) {
            // 类型是 `Option`
        }

        // 2. 使用语言项
        if ty.is_lang_item(cx, LangItem::RangeFull) {
            // 类型是完整范围，如 `.drain(..)`
        }

        // 3. 使用类型路径
        // 应尽量避免此法
        if paths::RESULT.matches_ty(cx, ty) {
            // 类型是 `core::result::Result`
        }
    }
}
```

优先使用诊断项与语言项。

## 检查类型是否实现特定 trait

有三种做法，取决于目标 trait 是否有诊断项、语言项或皆无。

```rust
use clippy_utils::sym;
use clippy_utils::ty::implements_trait;

impl LateLintPass<'_> for MyStructLint {
    fn check_expr(&mut self, cx: &LateContext<'_>, expr: &Expr<'_>) {

        // 1. 获取 trait 的 `DefId`
        // 通过语言项
        let trait_id = cx.tcx.lang_items().drop_trait();
        // 通过诊断项
        let trait_id = cx.tcx.get_diagnostic_item(sym::Eq);

        // 2. 通过 `implements_trait` 工具检查 trait 实现
        let ty = cx.typeck_results().expr_ty(expr);
        if trait_id.is_some_and(|id| implements_trait(cx, ty, id, &[])) {
            // `ty` 实现了该 trait
        }

        // 3. 若 trait 需要额外泛型参数
        let trait_id = cx.tcx.lang_items().eq_trait();
        if trait_id.is_some_and(|id| implements_trait(cx, ty, id, &[ty])) {
            // `ty` 实现了 `PartialEq<Self>`
        }
    }
}
```

> 若目标 trait 有诊断项或语言项，优先使用它们。

我们通过类型上下文 `tcx` 访问语言项。`tcx` 类型为 [`TyCtxt`][TyCtxt]，定义在 `rustc_middle` crate。Clippy 定义的路径列表见 [paths.rs][paths]

## 检查类型是否定义特定方法

检查类型是否定义名为 `some_method` 的方法：

```rust
use clippy_utils::ty::is_type_lang_item;
use clippy_utils::{sym, return_ty};

impl<'tcx> LateLintPass<'tcx> for MyTypeImpl {
    fn check_impl_item(&mut self, cx: &LateContext<'tcx>, impl_item: &'tcx ImplItem<'_>) {
        // 检查项是否为方法/函数
        if let ImplItemKind::Fn(ref signature, _) = impl_item.kind
            // 检查方法是否名为 `some_method`
            //
            // 若尚未存在，将 `some_method` 添加到 `clippy_utils::sym`
            && impl_item.ident.name == sym::some_method
            // 还可检查是否有 `self` 参数
            && signature.decl.implicit_self.has_implicit_self()
            // 甚至可检查返回类型是否为 `String`
            && return_ty(cx, impl_item.hir_id).is_lang_item(cx, LangItem::String)
        {
            // ...
        }
    }
}
```

## 处理宏与展开

请记住，宏已展开，脱糖已应用于你在 Clippy 中处理的代码表示。
这会导致大量误报，因为宏展开除非主动检查否则「不可见」。一般而言，含宏展开的代码应被 Clippy 忽略，因为这类代码可能以难以或无法预见的方式动态变化。使用以下函数处理宏：

- `span.from_expansion()`：检测 span 是否来自宏展开或脱糖。在 lint 中这是常见第一步。

   ```rust,ignore
   if expr.span.from_expansion() {
       // 直接忽略
       return;
   }
   ```

- `span.ctxt()`：span 的上下文表示是否来自展开，若是，由哪次宏调用展开。有时检查两个 span 的上下文是否相等很有用。

  ```rust,ignore
  // 展开为 `1 + 0`，但不要 lint
  1 + mac!()
  ```
  ```rust,ignore
  if left.span.ctxt() != right.span.ctxt() {
      // 编码者很可能无法修改该表达式
      return;
  }
  ```
  > 注意：非展开代码处于「根」上下文。因此 `from_expansion` 返回 `true` 的 span 可假定具有相同上下文，仅用 `span.from_expansion()` 通常已足够。


- `span.in_external_macro(sm)`：检测给定 span 是否来自外部 crate 定义的宏。若希望 lint 处理宏生成代码，这是下一道防线，避免 lint 当前 crate 未定义的宏。对编码者无法修改的代码进行 lint 没有意义。

  例如可避免对其他 crate 宏中的 `match` 开始 lint

  ```rust
  use a_crate_with_macros::foo;

  // `foo` 定义在 `a_crate_with_macros` 中
  foo!("bar");

  // 若我们对 `foo` 调用的 `match` 进行 lint 并测试其 span
  assert_eq!(match_span.in_external_macro(cx.sess().source_map()), true);
  ```

- `span.ctxt()`：span 的上下文表示是否来自展开，若是，由什么展开

  `SpanContext` 的一个用途是检查两个 span 是否在同一上下文。例如在 `a == b` 中，`a` 与 `b` 上下文相同。在 `macro_rules!` 的 `a == $b` 中，`$b` 展开为与 `a` 上下文不同的表达式。

   ```rust,ignore
   macro_rules! m {
       ($a:expr, $b:expr) => {
           if $a.is_some() {
               $b;
           }
       }
   }

   let x: Option<u32> = Some(42);
   m!(x, x.unwrap());

   // 这些 span 不在同一上下文
   // x.is_some() 来自宏内部
   // x.unwrap() 来自宏外部
   assert_eq!(x_is_some_span.ctxt(), x_unwrap_span.ctxt());
   ```

[Ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.Ty.html
[TyKind]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_type_ir/ty_kind/enum.TyKind.html
[TypeckResults]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.TypeckResults.html
[expr_ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.TypeckResults.html#method.expr_ty
[LateContext]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/struct.LateContext.html
[TyCtxt]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/context/struct.TyCtxt.html
[pat_ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/struct.TypeckResults.html#method.pat_ty
[paths]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/paths/index.html
