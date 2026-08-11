+++
title = "2.1.3 文档注释的结构"
date = 2026-08-11T11:30:00+08:00
weight = 393
type = "docs"
description = "03-文档注释的结构 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/anatomy-of-a-doc-comment.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/anatomy-of-a-doc-comment.html)

# 2.1.3 文档注释的结构

1. 简短的一句话摘要。
2. 更详细的说明。
3. 特殊小节：代码示例、panic、错误、安全前置条件。

````rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// Parses a key-value pair from a string.
///
/// The input string must be in the format `key=value`. Everything before the
/// first '=' is treated as the key, and everything after is the value.
///
/// # Examples
///
/// ```
/// use my_crate::parse_key_value;
/// let (key, value) = parse_key_value("lang=rust").unwrap();
/// assert_eq!(key, "lang");
/// assert_eq!(value, "rust");
/// ```
///
/// # Panics
///
/// Panics if the input is empty.
///
/// # Errors
///
/// Returns a `ParseError::Malformed` if the string does not contain `=`.
///
/// # Safety
///
/// Triggers undefined behavior if...
unsafe fn parse_key_value(s: &str) -> Result<(String, String), ParseError>

enum ParseError {
    Empty,
    Malformed,
}
````

> - 地道的 Rust 文档注释遵循约定结构，便于开发者阅读。
>
> - 文档注释的第一行是对该函数的单句摘要。保持简洁。`rustdoc` 及其他工具对此有强烈预期：它会用作模块级文档与搜索结果中的短摘要。
>
> - 接下来，你可以提供较长的、多段落的说明，解释函数的“为什么”与“做什么”。使用 Markdown。
>
> - 最后，可用顶层节标题组织内容。文档注释常用 `# Examples`、`# Panics`、`# Errors` 与 `# Safety` 作为节标题。Rust 社区期望在这些小节中看到 API 相关方面的文档。
>
> - Rust 高度重视安全性与正确性。记录错误情况下的行为，对编写可靠软件至关重要。
>
> - `# Panics`：若函数可能 panic，必须记录可能发生的具体条件。调用者需要知道该避免什么。
>
>   - **问题：** 问问学员，在更倾向返回 `Result` 的语言里，为何记录 panic 如此重要。
>
>   - **答案：** Panic 用于不可恢复的编程错误。除非调用者违反了契约，库不应 panic。记录这些契约至关重要。
>
> - `# Errors`：对返回 `Result` 的函数，本节说明可能发生哪些错误、在何种情况下。调用者需要这些信息才能写出稳健的错误处理逻辑。
>
> - `# Safety` 注释记录 unsafe 函数必须满足的安全前置条件，否则可能导致未定义行为。它们在 Unsafe Rust 深入部分有详细讨论。

