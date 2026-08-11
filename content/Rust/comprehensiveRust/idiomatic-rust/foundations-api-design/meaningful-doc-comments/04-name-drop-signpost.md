+++
title = "2.1.4 点名与指路"
date = 2026-08-11T11:30:00+08:00
weight = 394
type = "docs"
description = "04-点名与指路 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/name-drop-signpost.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/name-drop-signpost.html)

# 2.1.4 点名与指路

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// A parsed representation of a [MARC 21 record leader][leader].
///
/// A MARC leader contains metadata that dictates how to interpret the rest  
/// of the record.
///
/// [leader]: https://www.loc.gov/marc/bibliographic/bdleader.html
pub struct Leader {
    /// Determines the schema and the set of valid subsequent data fields.  
    ///
    /// Encoded in byte 6 of the leader.  
    pub type_of_record: char,

    /// Indicates whether to parse relationship fields, such as a "773 Host  
    /// Item Entry" for an article within a larger work.  
    ///  
    /// Encoded in byte 7 of the leader.  
    pub bibliographic_level: char,
    // ... 其他字段
}

/// Parses the [leader of a MARC 21 record][leader].
///  
/// The leader is encoded as a fixed-length 24-byte field, containing metadata  
/// that determines the semantic interpretation of the rest of the record.  
/// 
/// [leader]: https://www.loc.gov/marc/bibliographic/bdleader.html
pub fn parse_leader(leader_bytes: &[u8; 24]) -> Result<Leader, MarcError> {
    todo!()
}

#[derive(Debug)]
pub enum MarcError {}
```

> - 动机：文档读者不会像读心爱小说里的对话那样仔细读你的大多数文档注释。
>
>   用户多半是在浏览与扫读，寻找与当下要解决的问题相关的那部分文档。
>
>   一旦用户找到与自己相关的关键词或潜在路标，他们才会开始搜索被文档化内容周围的上下文。
>
> - 问问学员：你在文档中找什么？聚焦于逐刻寻找信息的瞬间，而非文档的一般价值。
>
> - 把关键词点名（name-drop）放在段落开头附近。
>
>   这有助于浏览与扫读，因为段落前几个词最显眼。
>
>   浏览与扫读让用户快速导航文本；把关键词尽量靠近段首，能让用户更快判断是否找到了相关信息。
>
> - 指路，但不要过度解释。
>
>   用户未必具备与 API 设计者同等的领域专长。
>
>   若提到偏题的专业术语或缩写，尽量带上足够上下文，让新手能快速进一步研究。
>
> - 指路往往自然发生，例如网络库会提到各种协议。但当它不自然发生时，很难选择该提什么。
>
>   经验法则：API 开发者应自问——“若新手碰到正在文档化的内容，他们会查哪些资料，以及有没有可能误入歧途的红鲱鱼？”
>
>   应给用户足够信息，让他们能自行查阅主题。
>
> - 我们已讨论过的——包括命名约定在内的 API 可预测性——也是一种指路。

