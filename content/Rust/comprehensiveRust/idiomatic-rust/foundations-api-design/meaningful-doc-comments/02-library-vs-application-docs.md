+++
title = "2.1.2 库文档 vs 应用文档"
date = 2026-08-11T11:30:00+08:00
weight = 392
type = "docs"
description = "02-库文档 vs 应用文档 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/library-vs-application-docs.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/library-vs-application-docs.html)

# 2.1.2 库文档 vs 应用文档

你可能见过基础 API 上详尽的文档——反复复述名称与类型签名。稳定且高度可复用的代码能负担得起这种投入，并获得正向投资回报（RoI）。

- 库代码：
  - 用户数量多，
  - 解决一整类相关问题，
  - 往往有稳定的 API。

- 应用代码则相反：
  - 用户少，
  - 解决特定问题，
  - 变更频繁。

> - 你可能见过详尽到重复代码、用大量示例与案例反复审视同一 API 的文档。语境是关键：谁写的、为谁写、覆盖什么材料、他们有什么资源。
>
> - 基础库代码往往有详尽文档，例如标准库、Serde 与 Tokio 这类高度可复用的框架。负责这类代码的团队通常有相应资源来编写并维护详尽文档。
>
> - 库代码往往稳定，因此社区能在文档需要重写之前，从详尽文档中获得显著收益。
>
> - 应用代码具有相反特质：用户少、解决特定问题、变更频繁。对应用代码而言，详尽文档很快就会过时并产生误导。即便文档仍是最新的，也很难从样板文档中榨取正向 RoI，因为用户本来就很少。

