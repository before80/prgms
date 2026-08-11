+++
title = "5.4.3 不健全性"
date = 2026-08-11T11:30:00+08:00
weight = 537
type = "docs"
description = "03-不健全性 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/soundness-proof/unsoundness.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/soundness-proof/unsoundness.html)

# 5.4.3 不健全性

健全函数是指：在其安全前置条件得到满足时，不会触发未定义行为（UB）的函数。

不健全函数即使满足已记录的安全前置条件，仍可能触发 UB。

不健全代码是 _坏的_。

> - 朗读不健全函数的定义。
>
> - 用通俗语言解释：不健全代码不『守规矩』。不，这样说还太轻了。不健全代码是 _坏的_。即使你遵守文档中的规则，不健全代码仍可能触发 UB！
>
> - 我们不希望代码库中出现任何不健全代码。
>
> - 发现不健全代码是代码审查的 **首要** 目标。

