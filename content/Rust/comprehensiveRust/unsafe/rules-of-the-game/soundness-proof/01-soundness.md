+++
title = "5.4.1 健全性"
date = 2026-08-11T11:30:00+08:00
weight = 535
type = "docs"
description = "01-健全性 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/soundness-proof/soundness.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/soundness-proof/soundness.html)

# 5.4.1 健全性

健全函数是指：在其安全前置条件得到满足时，不会触发未定义行为（UB）的函数。

> - 朗读健全函数的定义。
>
> - 提醒学员：实现调用方的程序员负责满足安全前置条件；编译器不会帮忙。
>
> - 用通俗语言解释：健全性意味着函数『守规矩』——它记录了安全前置条件，调用方满足这些条件时，函数表现良好（不会 UB）。

