+++
title = "3.3 unsafe 关键字的两种角色"
date = 2026-08-11T11:30:00+08:00
weight = 503
type = "docs"
description = "03-unsafe 关键字的两种角色 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/two-roles.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/two-roles.html)

# 3.3 unsafe 关键字的两种角色

1. _创建_ 带有安全考量的 API

   - unsafe 函数：`unsafe fn get_unchecked(&self) { ... }`
   - unsafe trait：`unsafe trait Send {}`

2. _使用_ 带有安全考量的 API

   - 调用内置 unsafe 操作：`unsafe { *ptr }`
   - 调用 unsafe 函数：`unsafe { x.get_unchecked() }`
   - 实现 unsafe trait：`unsafe impl Send for Counter {}`

> 两种角色：
>
> 1. **创建** 带有安全考量的 API，并定义需要考虑什么
> 2. **使用** 带有安全考量的 API，并确认已满足相应考量
>
> ### 创建带有安全考量的 API
>
> 「首先，`unsafe` 关键字让你能够创建可能破坏 Rust 安全保证的 API。具体而言，定义 unsafe 函数和 unsafe trait 时需要使用 `unsafe` 关键字。」
>
> 「在这种角色下，你是在告知 API 用户需要谨慎。」
>
> 「API 的创建者应说明需要采取哪些谨慎措施。unsafe API 若缺少关于安全要求的文档，就是不完整的。调用者需要知道他们已满足所有要求，若要求未写下来，这是不可能的。」
>
> ### 使用带有安全考量的 API
>
> 「`unsafe` 关键字的另一种角色——使用 API——出现在花括号附近时。」
>
> 「在这种角色下，`unsafe` 关键字表示作者已谨慎行事。他们已验证代码是安全的，并向他人提供保证。」
>
> 「unsafe 块最为常见。它们允许你调用以第一种角色定义的 unsafe 函数。」
>
> 「unsafe 块还允许你执行编译器已知为 unsafe 的操作，例如解引用 raw pointer。」
>
> 「你也可能看到 `unsafe` 关键字用于实现 unsafe trait。」

