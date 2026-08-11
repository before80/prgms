+++
title = "5.4.2 推论"
date = 2026-08-11T11:30:00+08:00
weight = 536
type = "docs"
description = "02-推论 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/soundness-proof/corollary.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/soundness-proof/corollary.html)

# 5.4.2 推论

健全函数是指：在其安全前置条件得到满足时，不会触发未定义行为（UB）的函数。

推论：所有完全用 Safe Rust 实现的函数都是健全的。

证明：

- Safe Rust 代码没有安全前置条件。

- 因此，调用纯 Safe Rust 实现函数的调用方，总是平凡地满足空集前置条件。

- Safe Rust 代码不会触发 UB。

证毕。

> - 朗读推论。
>
> - 解释证明过程。
>
> - 用通俗语言解释：所有 Safe Rust 代码都『守规矩』。程序员无需考虑安全前置条件，它始终遵守规则，且永远不会触发 UB。

