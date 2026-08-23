+++
title = "05-Lint 遍历"
date = 2026-08-22T18:00:00+08:00
weight = 75
type = "docs"
description = "lint pass 机制"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Lint 遍历 {#lint-passes}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/lint_passes.html](https://doc.rust-lang.org/nightly/clippy/development/lint_passes.html)


在实现新 lint 的逻辑之前，每位 Clippy 开发者都要做一个重要决定：使用
[`EarlyLintPass`][early_lint_pass] 还是 [`LateLintPass`][late_lint_pass]。

简而言之，`LateLintPass` 可访问类型与符号信息，而 `EarlyLintPass` 不能。若不需要类型信息，请使用 `EarlyLintPass`。

下面进一步说明这两个 trait。

## `EarlyLintPass`

若仔细查看 [`EarlyLintPass`][early_lint_pass] 文档，会发现该 trait 的每个方法都使用
[`EarlyContext`][early_context]。`EarlyContext` 文档中写道：

> 在宏展开之后、降级为 HIR 之前，对 AST 进行 lint 检查的上下文。

可见，`EarlyLintPass` 仅在抽象语法树（AST）层面工作。
AST 在编译的[词法分析与语法分析][lexing_and_parsing]阶段生成。因此它不知道符号含义或类型信息；若 lint 只涉及语法相关问题，就应选择该 trait。

虽然 Clippy 并不特别关心 lint 速度，
`EarlyLintPass` 更快；若确定 lint 不需要类型信息，应优先选择它。

提醒：要为使用 `EarlyLintPass` 的 lint 生成样板代码，可运行：

```sh
$ cargo dev new_lint --name=<your_new_lint> --pass=early --category=<your_category_choice>
```

### `EarlyLintPass` 示例

看以下代码：

```rust
let x = OurUndefinedType;
x.non_existing_method();
```

从 AST 角度看，两行在「语法」上都是正确的。
赋值用了 `let` 并以分号结尾；方法调用看起来也没问题。作为程序员我们可能已有疑问，但解析器可以接受。这就是我们所说的 `EarlyLintPass` 只处理 AST 层面语法。

另一种思路是[定义新 Lint](defining_lints.md) 一章提到的 `foo_functions` lint。

我们希望 `foo_functions` lint 检测名为 `foo` 的函数。
只检查函数名意味着只处理 AST，完全不必访问类型系统（类型系统正是 `LateLintPass` 的用武之地）。

## `LateLintPass`

与 `EarlyLintPass` 相反，`LateLintPass` 包含类型信息。

若仔细查看 [`LateLintPass`][late_lint_pass] 文档，会发现该 trait 的每个方法都使用
[`LateContext`][late_context]。

在 `LateContext` 文档中，可以找到处理类型检查的方法，而 `EarlyContext` 中没有，例如：

- [`maybe_typeck_results`](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/context/struct.LateContext.html#method.maybe_typeck_results)
- [`typeck_results`](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/context/struct.LateContext.html#method.typeck_results)

### `LateLintPass` 示例

看以下示例：

```rust
let x = OurUndefinedType;
x.non_existing_method();
```

从 AST 角度看，这两行语法正确：有赋值，并在某类型变量上调用方法。对解析器而言语法无误。

但若再深入类型信息层面，编译器会发现 `OurUndefinedType` 与 `non_existing_method()`
**均未定义**。

作为 Clippy 开发者，要访问这类类型信息，必须为我们的 lint 实现 `LateLintPass`。
浏览 Clippy 的 lint 时会发现，几乎所有 lint 都在 `LateLintPass` 中实现，因为我们常常不仅要检查语法问题，还要检查类型信息。

`EarlyLintPass` 的另一限制是：节点仅通过其在 AST 中的位置标识。这意味着不能简单地拿到某个 `id` 再请求对应节点。对大多数 lint 这没问题，但有些 lint 需要检查其他节点，在 HIR 层面更容易做到。此时 `LateLintPass` 是更好的选择。

提醒：要为使用 `LateLintPass` 的 lint 生成样板代码，可运行：

```sh
$ cargo dev new_lint --name=<your_new_lint> --pass=late --category=<your_category_choice>
```

[early_context]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/context/struct.EarlyContext.html
[early_lint_pass]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.EarlyLintPass.html
[late_context]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/context/struct.LateContext.html
[late_lint_pass]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.LateLintPass.html
[lexing_and_parsing]: https://rustc-dev-guide.rust-lang.org/overview.html#lexing-and-parsing
