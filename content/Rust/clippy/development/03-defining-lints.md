+++
title = "03-定义 Lint"
date = 2026-08-22T18:00:00+08:00
weight = 73
type = "docs"
description = "lint 定义与元数据"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 定义 Lint {#defining-lints}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/defining_lints.html](https://doc.rust-lang.org/nightly/clippy/development/defining_lints.html)


新 lint 旅程的第一步，是在 Clippy 代码库中定义并注册该 lint。
由于涉及一些样板代码，可使用 Clippy 开发工具完成这一步。

#### Lint 类型

lint 类型指你的 lint 所关注的项与表达式的类别。

截至本文更新时，除 `clippy_lints/src/` 下众多独立 lint 外，还有 11 种 _类型_：

- `cargo`
- `casts`
- `functions`
- `loops`
- `matches`
- `methods`
- `misc_early`
- `operators`
- `transmute`
- `types`
- `unit_types`

这些类型将具有共同行为的 lint 分组。例如 `functions` 包含处理 Rust 函数某些方面的 lint，如定义、签名与属性。

更多信息可对比任一类别下的 lint 文件与[全部 Clippy lint][all_lints]，或询问维护者。

## Lint 名称

好的 lint 名称很重要，请务必查看 [lint 命名指南][lint_naming]。若名称不合适，Clippy 团队成员会在 PR 流程中提醒你。

---

我们的示例 lint 检测名为 "foo" 的函数，命名为 `foo_functions`。
可查看 [lint 命名指南][lint_naming] 了解该名称为何合理。

## 添加并注册 Lint

名称确定后，将 `foo_functions` 注册到代码库。有两种注册方式。

### 独立 lint

若你认为新 lint 是独立 lint（不属于 `functions`、`loops` 等特定[类型](#lint-类型)），可在 Clippy 项目中运行：

```sh
$ cargo dev new_lint --name=lint_name --pass=late --category=pedantic
```

注意两点：

1. `--pass`：本例使用 `--pass=late` 做 late lint pass。另一种是 `early` lint pass。区别见 [Lint 遍历] 一章。
2. `--category`：若未提供，新 lint 的 `category` 默认为 `nursery`。

`cargo dev new_lint` 会创建新文件 `clippy_lints/src/foo_functions.rs`，并[注册 lint](#lint-注册)。

总体上，你会看到以下文件被修改或创建：

```sh
$ git status
On branch foo_functions
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   CHANGELOG.md
	modified:   clippy_lints/src/lib.register_lints.rs
	modified:   clippy_lints/src/lib.register_pedantic.rs
	modified:   clippy_lints/src/lib.rs

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	clippy_lints/src/foo_functions.rs
	tests/ui/foo_functions.rs
```


### 特定类型

> **注意**：lint 类型列在 ["Lint 类型"](#lint-类型) 一节。

若你认为新 lint 属于某类 lint，可对 `cargo dev new_lint` 使用 `--type` 选项。

由于 `foo_functions` 与函数调用相关，可将其放入检测函数行为的 lint 组，例如 `functions` 组。

在 Clippy 项目中运行：

```sh
$ cargo dev new_lint --name=foo_functions --type=functions --category=pedantic
```

该命令会创建新文件 `clippy_lints/src/{type}/foo_functions.rs`。
本例路径为 `clippy_lints/src/functions/foo_functions.rs`。

注意该命令使用 `--type` 而非 `--pass`。与独立定义不同，该 lint 不会以传统方式注册，而需在类型对应的 lint pass 中调用，位于 `clippy_lints/src/{type}/mod.rs`。

_类型_ 就是 `clippy_lints/src` 下的目录名，如示例中的 `functions`。Clippy 将具有共同行为的 lint 分组，若你的 lint 属于某一类，最好加入该类型。

总体上，你会看到以下文件被修改或创建：

```sh
$ git status
On branch foo_functions
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   CHANGELOG.md
	modified:   clippy_lints/src/declared_lints.rs
	modified:   clippy_lints/src/functions/mod.rs

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	clippy_lints/src/functions/foo_functions.rs
	tests/ui/foo_functions.rs
```


## `declare_clippy_lint` 宏

运行 `cargo dev new_lint` 后，应能看到名为 `declare_clippy_lint` 的宏。若为独立 lint，宏在同一文件中；若为类型特定 lint，则在 `mod.rs` 中。

宏大致如下：

```rust
declare_clippy_lint! {
    /// ### What it does
    ///
    /// // 在此描述 lint 做什么。
    ///
    /// Triggers when detects...
    ///
    /// ### Why is this bad?
    ///
    /// // 描述该模式为何不好
    ///
    /// It can lead to...
    ///
    /// ### Example
    /// ```rust
    /// // Clippy 发出警告的示例代码
    /// ```
    /// Use instead:
    /// ```rust
    /// // 不会触发 Clippy 警告的示例代码
    /// ```
    #[clippy::version = "1.70.0"] // <- 实现版本，请保持更新！
    pub LINT_NAME, // <- 全大写的 lint 名称
    pedantic, // <- lint 分组
    "default lint description" // <- lint 描述，例如 "A function has an unit return type."
}
```

## Lint 注册

若为新 lint 运行 `cargo dev new_lint`，lint 会自动注册，无需额外操作。

但有时需要手动声明新 lint，此时应随后运行 `cargo dev update_lints`。

手动声明 lint 时，可能需在 `clippy_lints/src/lib.rs` 的 `late_lint_methods!` 宏调用中、`// add late passes here` 标记处手动注册 lint pass：

```rust
FooFunctions: foo_functions::FooFunctions = foo_functions::FooFunctions,
```

顾名思义，有 late 就有 early：Clippy 也有 `early_lint_methods!` 宏。early 与 late pass 的更多说明见 [Lint 遍历] 一章。

若未在 `early_lint_methods!` 或 `late_lint_methods!` 之一中登记，对应的 lint pass 不会运行。


[all_lints]: https://rust-lang.github.io/rust-clippy/master/
[lint_naming]: https://rust-lang.github.io/rfcs/0344-conventions-galore.html#lints
[Lint Passes]: lint_passes.md
