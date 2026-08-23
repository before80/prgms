+++
title = "04-Clippy 的 Lint"
date = 2026-08-22T18:00:00+08:00
weight = 40
type = "docs"
description = "各 lint 分类说明"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Clippy 的 Lint {#lints}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/lints.html](https://doc.rust-lang.org/nightly/clippy/lints.html)


Clippy 提供大量额外 lint，帮助用户编写更正确、更符合惯用法的 Rust 代码。可按类别、lint 级别或关键词筛选的完整 lint 列表请参阅 [Clippy lint 文档]。

本章介绍不同 lint 类别的详情、各类别提供的 lint 类型，以及遇到该类 lint 时的建议处理方式。示例请参阅 [Clippy lint 文档] 并按类别筛选。类别概览请参阅[引言](/clippy/)。

不同 lint 组在 [Clippy 1.0 RFC] 中定义。

## Correctness

`clippy::correctness` 组是 Clippy 中唯一默认拒绝（deny-by-default）的 lint 组，触发时会中止编译。这是有充分理由的：若你看到 `correctness` lint，说明你的代码存在明显错误或无用，应尝试修复。

该类别中的 lint 经过精心挑选，应不含误报。因此不建议仅通过 `#[allow]` 来忽略这些 lint。

## Suspicious

`clippy::suspicious` 组与 correctness lint 类似，包含对真正可疑（_sus_）且应修复的代码触发的 lint。与 correctness lint 不同，被 lint 的代码有可能是故意这样写的。

仍建议修复该组 lint 所标记的代码，而不是 `#[allow]` 该 lint。若你故意写了触犯该 lint 的代码，应在局部显式 `#[allow]` 该 lint，并说明为何当前写法是正确的。

## Complexity

`clippy::complexity` 组提供简化代码的建议 lint。主要关注可在保持语义的同时以更短、更易读方式书写的代码。

若遇到 complexity lint，通常意味着可以删除或替换部分代码，建议这样做。但若出于表达需要必须使用更复杂的代码，建议按具体情况允许 complexity lint。

## Perf

`clippy::perf` 组提供提升代码性能的建议。这些 lint 主要针对编译器无法轻易优化、需要以略有不同的方式书写以便优化器工作的代码。

Perf lint 通常易于应用，建议采纳。

## Style

`clippy::style` 组主要关注编写符合惯用法的代码。由于风格具有主观性，该 lint 组是 Clippy 中最主观的默认警告组。

若看到 style lint，采纳建议通常会使代码更易读、更符合惯用法。但我们知道这具有主观性，因此可以在代码中适度使用 `#[allow]`，或在完全不同意建议风格时对整个 crate 使用 `#![allow]` 允许 style lint。

## Pedantic

`clippy::pedantic` 组使 Clippy 更加「较真」（_pedantic_）。可在 crate 的 `lib.rs`/`main.rs` 中使用 `#![warn(clippy::pedantic)]` 启用整个组。该 lint 组面向希望对代码进行深度检查的 Clippy 高级用户。

> 注意：与 Clippy 自身做法不同，你可能更希望从 pedantic 组中挑选 lint，而不是启用整个组。

若启用该组，请预期需要在代码中广泛使用 `#[allow]` 属性。该组中的 lint 设计为较真，有时会故意产生误报以避免漏报。

## Restriction

`clippy::restriction` 组包含会*限制*你使用 Rust 语言某些部分的 lint。**不建议**启用整个组，而应根据代码库和用例挑选有用的 lint。

> 注意：若 Clippy 在代码中发现 `#![warn(clippy::restriction)]` 属性，会发出警告！

该组的 lint 会在某种程度上限制你。若为 crate 启用 restriction lint，建议同时修复该 lint 触发的代码。不过这些 lint 设计上非常严格，在特殊情况下你可能需要 `#[allow]` 它们，并附上理由说明。

## Cargo

`clippy::cargo` 组提供改进 `Cargo.toml` 文件的建议。若你打算发布 crate 且不确定 `Cargo.toml` 是否包含所有有用信息，这可能尤其值得关注。

## Nursery

`clippy::nursery` 组包含存在缺陷或仍需完善的 lint。**不建议**启用整个组，而应根据代码库和用例挑选有用的 lint。

## Deprecated

`clippy::deprecated` 是空 lint，用于确保 lint 被弃用后 `#[allow(lintname)]` 仍能编译。弃用通过移除 lint 功能并将其标记为 deprecated 来「移除」lint，这可能引发进一步警告，但不会导致编译错误。

[Clippy lint 文档]: https://rust-lang.github.io/rust-clippy/
[Clippy 1.0 RFC]: https://github.com/rust-lang/rfcs/blob/master/text/2476-clippy-uno.md#lint-audit-and-categories
