+++
title = "2.1.1 你在为谁写？"
date = 2026-08-11T11:30:00+08:00
weight = 391
type = "docs"
description = "01-你在为谁写？ — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/who-are-you-writing-for.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/who-are-you-writing-for.html)

# 2.1.1 你在为谁写？

同事、合作者、大多沉默的 API 用户，还是仅仅你自己？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 专家写给专家
/// Canonicalizes the MIR for the borrow checker.  
///  
/// This pass ensures that all borrows conform to the NLL-Polonius constraints  
/// before we proceed to MIR-to-LLVM-IR translation.  
pub fn canonicalize_mir(mir: &mut Mir) {
    // ...
}

// 专家写给新手
/// Prepares the Mid-level IR (MIR) for borrow checking.  
///  
/// The borrow checker operates on a simplified, "canonical" form of the MIR.  
/// This function performs that transformation. It is a prerequisite for the  
/// final stages of code generation.  
///  
/// For more about Rust's intermediate representations, see the  
/// [rustc-dev-guide](https://rustc-dev-guide.rust-lang.org/mir/index.html).  
pub fn canonicalize_mir(mir: &mut Mir) {
    // ...
}
```

> - 背景：[知识的诅咒](https://en.wikipedia.org/wiki/Curse_of_knowledge)（curse of knowledge）是一种认知偏差——专家会假定他人具备同等水平的专业知识与视角。
>
> - 动机：读者并不具备与你同等的专业水平和视角。不要写给和你一样的人，要写给他人。
>
> - 无意中只为自己写，会导致别人无法理解你想表达的要点或概念。
>
> - 想象一个正在文档中艰难寻找实用信息的你自己，或你认识的人。
>
>   在思考代码库哪些地方需要文档注释时，把这个人放在心里。
>
> - 你在为谁写？
>
> - 也想象一个在冗长、绕来绕去的文档注释中难以找到关键细节的你，或你认识的人。不要给太多信息。
>
> - 始终自问：这份文档是否让 API 用户更难用？他们能否快速抓住所需，或弄清该去哪里找？
>
> - 始终考虑：专家也会读 API 级文档。文档注释未必是向受众普及领域基础知识的合适场所。那种情况下，点名并指路（signpost and name-drop），把人导向长文文档。

