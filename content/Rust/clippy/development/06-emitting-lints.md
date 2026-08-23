+++
title = "06-发出 Lint"
date = 2026-08-22T18:00:00+08:00
weight = 76
type = "docs"
description = "如何 emit lint"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 发出 Lint {#emitting-lints}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/emitting_lints.html](https://doc.rust-lang.org/nightly/clippy/development/emitting_lints.html)


在[定义 lint](defining_lints.md)、编写 [UI 测试](writing_tests.md)并[选择 lint pass](lint_passes.md)之后，
即可开始实现 lint 逻辑以发出 lint，逐步使 lint 行为符合预期。

注意本章不会深入具体 lint 逻辑的实现，细节将在后续章节及两个真实 Clippy lint 示例中讲解。

要发出 lint，必须为已声明的 lint 实现 pass（见 [Lint 遍历](lint_passes.md)）。本例实现 "late" lint，
请查看 [LateLintPass][late_lint_pass] 文档，其中提供大量可供实现的方法。

```rust
pub trait LateLintPass<'tcx>: LintPass {
    // Trait methods
}
```

Clippy lint 中最常用的方法是 [`check_expr` 方法][late_check_expr]，因为 Rust 是表达式语言，
我们要处理的 lint 多半需要检查表达式。

> _注意：_ 若不完全理解 Rust 中的表达式，请参阅官方[表达式][rust_expressions]文档。

其他常见方法包括 [`check_fn` 方法][late_check_fn] 与 [`check_item` 方法][late_check_item]。

### 发出 lint

在我们实现的方法内部，可编写 lint 逻辑并附带建议发出 lint。

Clippy 的 [diagnostics] 提供多种诊断函数。请查阅文档选择最适合你 lint 的。仓库中常见包括：

- [`span_lint`]：发出 lint，不提供其他信息
- [`span_lint_and_note`]：发出 lint 并添加 note
- [`span_lint_and_help`]：发出 lint 并提供帮助信息
- [`span_lint_and_sugg`]：发出 lint 并提供修复建议
- [`span_lint_and_then`]：类似 `span_lint`，但允许大量自定义输出

```rust
impl<'tcx> LateLintPass<'tcx> for LintName {
    fn check_expr(&mut self, cx: &LateContext<'tcx>, expr: &'tcx Expr<'_>)  {
        // 假设 `some_lint_expr_logic` 检查发出 lint 的条件
        if some_lint_expr_logic(expr) {
            span_lint_and_help(
                cx, // < 上下文
                LINT_NAME, // < 全大写的 lint 名称
                expr.span, // < 要 lint 的 span
                "message on why the lint is emitted",
                None, // < 可选的帮助 span（用于高亮 lint 中的某部分）
                "message that provides a helpful suggestion",
            );
        }
    }
}
```

> 注意：消息应客观陈述，避免大写与标点。若需要多句，通常应拆分为错误 + help / note / suggestion 消息。

## 建议：自动修复

部分 lint 知道如何修改代码以修复问题。例如 lint
[`range_plus_one`][range_plus_one] 对写成 `x..y + 1` 而非[闭区间][inclusive_range]（`x..=y`）的范围发出警告。修复方式是将 `x..y + 1` 改为 `x..=y`。**建议正在于此**。

建议是 lint 为修复所 lint 问题而提供的修改。输出大致如下（来自前文示例）：

```text
error: an inclusive range would be more readable
  --> tests/ui/range_plus_minus_one.rs:37:14
   |
LL |     for _ in 1..1 + 1 {}
   |              ^^^^^^^^ help: use: `1..=1`
```

### Applicability

**并非所有建议都始终正确**，部分需要人工确认，因此有 [Applicability][applicability]。

Applicability 表示对建议正确性的信心：有些始终正确（`Applicability::MachineApplicable`），对可能不正确的建议使用 `Applicability::MaybeIncorrect` 等。

### 示例

同样名为 `LINT_NAME` 但发出建议的 lint 大致如下：

```rust
impl<'tcx> LateLintPass<'tcx> for LintName {
    fn check_expr(&mut self, cx: &LateContext<'tcx>, expr: &'tcx Expr<'_>)  {
        // 假设 `some_lint_expr_logic` 检查发出 lint 的条件
        if some_lint_expr_logic(expr) {
            span_lint_and_then( // < 注意此变化
                cx,
                LINT_NAME,
                expr.span,
                "message on why the lint is emitted",
                |diag| {
                    // v 构建并发出建议
                    let mut app = Applicability::MachineApplicable;
                    let expr_snippet = snippet_with_applicability(cx, expr.span, "_", &mut app);
                    let sugg = format!("foo + {expr_snippet} * bar");
                    diag.span_suggestion(expr.span, "use", sugg, app);
                }
            );
        }
    }
}
```

建议通常使用 [`format!`][format_macro] 宏将旧值与新值插值。获取代码片段见 [代码片段](emitting_lints.md#代码片段)。

## 如何在 note、帮助消息与建议之间选择

Note 与主 lint 消息分开呈现，提供用户理解 lint 触发原因所需的信息。
附加到 span 时最有帮助。

示例：

### Note

```text
error: calls to `std::mem::forget` with a reference instead of an owned value. Forgetting a reference does nothing.
  --> tests/ui/drop_forget_ref.rs:10:5
   |
10 |     forget(&SomeStruct);
   |     ^^^^^^^^^^^^^^^^^^^
   |
   = note: `-D clippy::forget-ref` implied by `-D warnings`
note: argument has type &SomeStruct
  --> tests/ui/drop_forget_ref.rs:10:12
   |
10 |     forget(&SomeStruct);
   |            ^^^^^^^^^^^
```

### 帮助消息

帮助消息专门帮助用户，用于无法提供具体机器可应用建议的情况，也可附加到 span。

示例：

```text
error: constant division of 0.0 with 0.0 will always result in NaN
  --> tests/ui/zero_div_zero.rs:6:25
   |
6  |     let other_f64_nan = 0.0f64 / 0.0;
   |                         ^^^^^^^^^^^^
   |
   = help: consider using `f64::NAN` if you would like a constant representing NaN
```

### 建议

建议最有用，是对源码的修改以修复错误。建议的妙处在于 `rustfix` 等工具可检测并自动修复代码。

示例：

```text
error: This `.fold` can be more succinctly expressed as `.any`
--> tests/ui/methods.rs:390:13
    |
390 |     let _ = (0..3).fold(false, |acc, x| acc || x > 2);
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ help: try: `.any(|x| x > 2)`
    |
```

## 代码片段

代码片段是源码片段（字符串），通常通过 [`clippy_utils::source`][] 中的各种 `snippet_*` 函数提取。

若*不*用于构建建议，通常 [`snippet`][snippet_fn] 即可——接受项的 span 及回退字符串（见[回退字符串](emitting_lints.md#回退字符串)）。

例如若想知道某项的外观（且已知其 span），可用 `snippet(cx, span, "_")`。

若将片段用于建议，推荐使用 [`snippet_with_applicability`]，以便在无法「干净」提取片段时降低建议的 [applicability](emitting_lints.md#applicability)——详见该函数文档。

构建建议时常需多个片段，模式如下：

```rust
// 在 `span_lint_and_then` 内部

// 1. 创建初始 applicability
let mut app = Applicability::MachineApplicable;

// 2. 用它创建所有片段
let foo_snippet = snippet_with_applicability(cx, foo.span, "_", &mut app);
let bar_snippet = snippet_with_applicability(cx, bar.span, "_", &mut app);
let sugg = format!("{foo_snippet} + {bar_snippet}"); // 或其他

// 3. 用它发出最终建议
diag.span_suggestion(span, msg, sugg, app);
```

### 回退字符串
当 span 指向的源码不可用时，片段使用该字符串。这多半只在过程宏处理 span 不当时发生——见[过程宏相关章节][proc-macro-spans]。

建议中的片段多半来自（单个表达式的）span，因此 `"_"` 是合适的回退字符串。若建议插入多条语句或块等「较大」内容，可考虑使用 `".."`。

## 最后：运行 UI 测试以发出 Lint

现在运行 [UI 测试](writing_tests.md)，应能看到 Clippy 输出我们设计的 lint 消息。

下一步是正确实现逻辑，细节将在后续章节说明。

[diagnostics]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/diagnostics/index.html
[late_check_expr]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.LateLintPass.html#method.check_expr
[late_check_fn]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.LateLintPass.html#method.check_fn
[late_check_item]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.LateLintPass.html#method.check_item
[late_lint_pass]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.LateLintPass.html
[rust_expressions]: https://doc.rust-lang.org/reference/expressions.html
[`span_lint`]: https://doc.rust-lang.org/beta/nightly-rustc/clippy_utils/diagnostics/fn.span_lint.html
[`span_lint_and_note`]: https://doc.rust-lang.org/beta/nightly-rustc/clippy_utils/diagnostics/fn.span_lint_and_note.html
[`span_lint_and_help`]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/diagnostics/fn.span_lint_and_help.html
[`span_lint_and_sugg`]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/diagnostics/fn.span_lint_and_sugg.html
[`span_lint_and_then`]: https://doc.rust-lang.org/beta/nightly-rustc/clippy_utils/diagnostics/fn.span_lint_and_then.html
[`clippy_utils::source`]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/source/index.html
[range_plus_one]: https://rust-lang.github.io/rust-clippy/master/index.html#range_plus_one
[inclusive_range]: https://doc.rust-lang.org/std/ops/struct.RangeInclusive.html
[applicability]: https://doc.rust-lang.org/beta/nightly-rustc/rustc_errors/enum.Applicability.html
[snippet_fn]: https://doc.rust-lang.org/beta/nightly-rustc/clippy_utils/source/fn.snippet.html
[`snippet_with_applicability`]: https://doc.rust-lang.org/beta/nightly-rustc/clippy_utils/source/fn.snippet_with_applicability.html
[proc-macro-spans]: macro_expansions.html#is_from_proc_macro-函数
[format_macro]: https://doc.rust-lang.org/std/macro.format.html
