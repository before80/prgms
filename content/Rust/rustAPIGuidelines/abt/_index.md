+++
title = "关于"
date = 2026-08-18T21:50:00+08:00
weight = 10
type = "docs"
description = "关于 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/about.html](https://rust-lang.github.io/api-guidelines/about.html)

# 关于

这是一套关于如何设计与呈现 Rust 编程语言 API 的建议。主要由 Rust 库团队撰写，依据构建 Rust 标准库以及 Rust 生态系统中其他 crate 的经验。

这些只是指南，其中有些更为确定。有些情况下它们仍较模糊、尚在完善。Rust crate 作者应将其视为开发惯用、可互操作的 Rust 库时一组重要考量，按自身需要取用。这些指南绝不应被视为 crate 作者必须遵守的强制要求，不过他们可能会发现：较好遵循这些指南的 crate，与现有 crate 生态系统的集成会优于未遵循者。

本书分为两部分：一份简明的 [检查清单]，列出全部单项指南，适合在 crate 评审时快速浏览；以及按主题分章、详细解释各指南的正文。

若有意为本 API 指南做贡献，请参阅 [贡献指南] 并加入我们的 [Gitter 频道]。

[检查清单]: ../checklist/
[贡献指南]: https://github.com/rust-lang/api-guidelines/blob/master/CONTRIBUTING.md
[Gitter 频道]: https://gitter.im/rust-impl-period/WG-libs-guidelines
