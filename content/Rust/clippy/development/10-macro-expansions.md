+++
title = "10-宏展开"
date = 2026-08-22T18:00:00+08:00
weight = 80
type = "docs"
description = "宏展开相关 lint"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 宏展开 {#macro-expansions}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/macro_expansions.html](https://doc.rust-lang.org/nightly/clippy/development/macro_expansions.html)


在 Clippy 中工作时，有时会遇到 Rust 宏展开。宏展开虽不如宇宙膨胀那般宏大，却可能为代码与逻辑的秩序世界带来混乱。

一般原则是：在 Clippy 中应忽略来自宏展开的代码，因为这类代码可能以难以或无法预见的方式动态变化。

## 误报

「难以预见地动态变化」具体指什么？

宏在 `EarlyLintPass` 层面[展开][expansion]，
因此宏的位置会生成抽象语法树（AST）。这意味着我们在 Clippy 中处理的代码已是展开后的代码。

若写了新 lint，可能在宏生成代码中触发。由于展开后的宏代码由宏作者而非宏用户编写，用户不应也无法负责修复触发 lint 的问题。

此外，宏中的 [Span] 可被宏作者修改。
因此应避免与行号或列号相关的 lint 检查，因为它们可能随时变化，成为不可靠或错误的信息。

由于这些不可预测或不稳定的特性，宏展开通常不应视为稳定 API 的一部分。
这也是大多数 lint 在向最终用户发出建议前，会检查是否位于宏内部，以避免误报。

## 如何处理宏

有多种函数可用于处理宏。

### `Span::from_expansion` 方法

可使用 `span` 的 [`from_expansion`] 方法，检测 `span` 是否来自宏展开或脱糖。
这是 lint 中非常常见的第一步：

```rust
if expr.span.from_expansion() {
    // 我们很可能应忽略它
    return;
}
```

### `Span::ctxt` 方法

`span` 的上下文由 [`ctxt`] 方法给出，返回 [SyntaxContext]，
表示 span 是否来自宏展开，若是，则由哪次宏调用展开。

有时比较两个 span 的上下文很有用。
例如以下代码会展开为 `1 + 0`：

```rust
// 以下代码对 `EarlyLintPass` 和 `LateLintPass` 均展开为 `1 + 0`
1 + mac!()
```

假设我们将 `1` 表达式收集为变量 `left`，`0`/`mac!()` 表达式为 `right`，
只需比较它们的上下文。若上下文不同，多半在处理宏展开，应忽略：

```rust
if left.span.ctxt() != right.span.ctxt() {
    // 代码作者很可能无法修改该表达式
    return;
}
```

> **注意**：非展开代码处于「根」上下文。
> 因此任何 `from_expansion` 返回 `false` 的 span 可假定具有相同上下文。正因如此，使用 `span.from_expansion()` 通常已足够。

再深入一点，在 `a == b` 这类简单表达式中，
`a` 与 `b` 上下文相同。
但在 `macro_rules!` 的 `a == $b` 中，`$b` 展开为与 `a` 上下文不同的表达式。

看以下宏 `m`：

```rust
macro_rules! m {
    ($a:expr, $b:expr) => {
        if $a.is_some() {
            $b;
        }
    }
}

let x: Option<u32> = Some(42);
m!(x, x.unwrap());
```

若 `m!(x, x.unwrap());` 行被展开，会得到两个展开表达式：

- `x.is_some()`（来自 `m` 宏中 `$a.is_some()` 行）
- `x.unwrap()`（对应 `m` 宏中的 `$b`）

假设 `x.is_some()` 表达式的 span 关联变量 `x_is_some_span`，
`x.unwrap()` 表达式的 span 关联 `x_unwrap_span`，
可假定这两个 span 不共享同一上下文：

```rust
// x.is_some() 来自宏内部
// x.unwrap() 来自宏外部
assert_ne!(x_is_some_span.ctxt(), x_unwrap_span.ctxt());
```

### `in_external_macro` 函数

`Span` 提供 [`in_external_macro`] 方法，可检测给定 span 是否来自外部 crate 中定义的宏。

因此，若确实希望新 lint 处理宏生成代码，
这是下一道防线，避免 lint 用户无法修改的外部 crate 宏。

例如假设 Clippy 检查以下代码：

```rust
#[macro_use]
extern crate a_foreign_crate_with_macros;

// `foo` 宏定义在 `a_foreign_crate_with_macros` 中
foo!("bar");
```

假设 `foo` 宏调用对应变量 `foo_span`，若 `in_external_macro`
结果为 `true`，可决定不进行 lint（注意 `cx` 可为 `EarlyContext` 或 `LateContext`）：

```rust
if foo_span.in_external_macro(cx.sess().source_map()) {
    // 应忽略来自外部 crate 的宏
    return;
}
```

### `is_from_proc_macro` 函数

[`is_from_proc_macro`] 的存在及其与 [`in_external_macro`]/[`from_expansion`] 的区别，常令人困惑。

[`in_external_macro`] 与 [`from_expansion`] 对*声明式*宏（即 `macro_rules!` 与宏 2.0）展开的代码检测良好，
但检测*过程宏*生成代码更棘手，因为过程宏可（且常）自由操纵返回 token 的 span。

实践中，这常通过 [`quote::quote_spanned!`] 使用输入 token 的 span 实现。

此时编译器（及 Clippy 等工具）*无法可靠*区分此类过程宏生成的代码与用户直接编写的代码，
[`in_external_macro`] 会返回 `false`。

对编译器这通常不是问题，实际上有助于过程宏作者生成更好的错误信息，因为可将展开部分与宏输入关联，在编译错误时指向用户相关代码。

但对 Clippy 不便，因为多数时候我们*不想* lint 过程宏生成的代码，这使得无法分辨哪些属于过程宏代码。

> 注意：这仅在过程宏**显式**将 span 设为**输入 span** 时才是问题。
>
> 例如，创建 `TokenStream` 的其他常见方式，如 `"fn foo() {...}".parse::<TokenStream>()`，
> 会将每个 token 的 span 设为 `Span::call_site()`，已标记为来自过程宏，
> 常规 span 方法可毫无问题地将其识别为宏 span。

因此 Clippy 有自己的 `is_from_proc_macro` 函数，通过检查给定 span 处的源码文本是否与给定 AST 节点一致，*近似*判断 span 是否来自过程宏。

该函数通常与其他宏 span 函数组合使用，但往往在条件链较后调用，因为它比其他条件更重，以便更便宜的条件先失败。例如 `borrow_deref_ref` lint：
```rs
impl<'tcx> LateLintPass<'tcx> for BorrowDerefRef {
    fn check_expr(&mut self, cx: &LateContext<'tcx>, e: &rustc_hir::Expr<'tcx>) {
        if let ... = ...
            && ...
            && !e.span.from_expansion()
            && ...
            && ...
            && !is_from_proc_macro(cx, e)
            && ...
        {
            ...
        }
    }
}
```

### 测试涉及宏展开的 lint
为测试 lint 是否正确处理所有这些情况，
我们有一个辅助 crate 暴露各种宏，测试用法如下：
```rust
//@aux-build:proc_macros.rs

extern crate proc_macros;

fn main() {
    proc_macros::external!{ code_that_should_trigger_your_lint }
    proc_macros::with_span!{ span code_that_should_trigger_your_lint }
}
```
这覆盖两种情况：
- `proc_macros::external!` 是简单过程宏，回显输入 token 但使用宏 span：
代表常见情况——外部宏展开为会触发 lint 的代码，由 `in_external_macro` 与 `Span::from_expansion` 正确处理。

- `proc_macros::with_span!` 从第二个 token 起回显输入 token，并使用第一个 token 的 span：此时其他函数会失效，需要 `is_from_proc_macro`


[`ctxt`]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_span/struct.Span.html#method.ctxt
[expansion]: https://rustc-dev-guide.rust-lang.org/macro-expansion.html#expansion-and-ast-integration
[`from_expansion`]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_span/struct.Span.html#method.from_expansion
[`in_external_macro`]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_span/struct.Span.html#method.in_external_macro
[Span]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_span/struct.Span.html
[SyntaxContext]: https://doc.rust-lang.org/stable/nightly-rustc/rustc_span/hygiene/struct.SyntaxContext.html
[`is_from_proc_macro`]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/fn.is_from_proc_macro.html
[`quote::quote_spanned!`]: https://docs.rs/quote/latest/quote/macro.quote_spanned.html
