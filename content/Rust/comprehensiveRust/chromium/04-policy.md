+++
title = "4 策略"
date = 2026-08-11T11:30:00+08:00
weight = 259
type = "docs"
description = "04-策略 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/policy.html](https://google.github.io/comprehensive-rust/chromium/policy.html)

# 4 策略

Chromium 的 Rust 策略见
[此处](https://source.chromium.org/chromium/chromium/src/+/main:docs/rust.md;l=22)。
Rust 既可用于第一方代码，也可用于第三方代码。

纯第一方代码使用 Rust 的样子如下：

```bob
"C++"                           Rust
.- - - - - - - - - -.           .- - - - - - - - - - -.
:                   :           :                     :
: Existing Chromium :           :  Chromium Rust      :
: "C++"             :           :  code               :
: +---------------+ :           : +----------------+  :
: |               | :           : |                |  :
: |         o-----+-+-----------+-+->              |  :
: |               | : Language  : |                |  :
: +---------------+ : boundary  : +----------------+  :
:                   :           :                     :
`- - - - - - - - - -'           `- - - - - - - - - - -'
```

第三方情形也很常见。你通常还需要少量第一方胶水代码，因为极少有 Rust 库直接暴露 C/C++ API。

```bob
"C++"                           Rust
.- - - - - - - - - -.           .- - - - - - - - - - - - - - - - - - - - - - -.
:                   :           :                                             :
: Existing Chromium :           :  Chromium Rust              Existing Rust   :
: "C++"             :           :  "wrapper"                  crate           :
: +---------------+ :           : +----------------+          +-------------+ :
: |               | :           : |                |          |             | :
: |         o-----+-+-----------+-+->            o-+----------+-->          | :
: |               | : Language  : |                | Crate    |             | :
: +---------------+ : boundary  : +----------------+ API      +-------------+ :
:                   :           :                                             :
`- - - - - - - - - -'           `- - - - - - - - - - - - - - - - - - - - - - -'
```

使用第三方 crate 的场景更复杂，因此今天的课程将聚焦于：

- 引入第三方 Rust 库（“crates”）
- 编写胶水代码，以便能从 Chromium C++ 使用这些 crate。（处理第一方 Rust 代码时也使用相同技术。）
