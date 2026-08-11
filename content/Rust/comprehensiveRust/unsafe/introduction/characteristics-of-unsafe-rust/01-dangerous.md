+++
title = "3.5.1 危险"
date = 2026-08-11T11:30:00+08:00
weight = 510
type = "docs"
description = "01-危险 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/characteristics-of-unsafe-rust/dangerous.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/characteristics-of-unsafe-rust/dangerous.html)

# 3.5.1 危险

> 「Use-after-free（UAF，释放后使用）、整数溢出，以及 out of bounds（OOB，越界）读写
> 占漏洞的 90%，其中 OOB 最为常见。」
>
> --- **Jeff Vander Stoep and Chong Zang**，Google。
> "[Queue the Hardening Enhancements][blog]"

[blog]: https://security.googleblog.com/2019/05/queue-hardening-enhancements.html

> 「软件行业已收集大量证据表明，unsafe 代码难以正确编写，并会造成非常严重的问题。」
>
> 「这份清单中的问题已被 Rust 消除。`unsafe` 关键字又让它们回到了你的源代码中。」
>
> 「务必谨慎。」

