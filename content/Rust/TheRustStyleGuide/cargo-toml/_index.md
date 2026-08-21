+++
title = "第6章 Cargo.toml 约定"
date = 2026-08-18T22:00:00+08:00
weight = 70
type = "docs"
description = "Cargo.toml 约定 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/cargo.html](https://doc.rust-lang.org/nightly/style-guide/cargo.html)

# Cargo.toml 约定

## 格式约定 {#formatting-conventions}

使用与 Rust 代码相同的行宽和缩进。

在某一节的最后一个键值对与下一节的节标题之间空一行。不要在节标题与该节的键值对之间、或同一节内的键值对之间空行。

各节内的键名按版本排序（version-sort），`[package]` 节除外。将 `[package]` 节放在文件最上方；该节顶部按此顺序放置 `name` 和 `version` 键，随后按顺序放置除 `description` 以外的其余键，最后将 `description` 放在该节末尾。

标准键名不要加引号，使用裸键。仅当非标准键的名称需要引号时才使用带引号的键，并尽可能避免引入此类键名。详见 [TOML 规范](https://toml.io/en/v1.0.0#keys)。

键与值之间的 `=` 两侧各放一个空格。不要缩进任何键名；所有键名都从行首开始。

对包含多行的字符串值（例如 crate 描述）使用多行字符串，而不要使用换行转义序列。

对于数组值（例如 feature 列表），若能排下，则将整个列表与键放在同一行。否则使用块缩进：在左方括号后换行，每项缩进一级，每项（包括最后一项）后加逗号，并将右方括号单独放在最后一项之后的一行行首。

```rust
some_feature = [
    "another_feature",
    "yet_another_feature",
    "some_dependency?/some_feature",
]
```

对于表值（例如带 path 的 crate 依赖），若能排下，则用花括号和逗号将整个表写在与键同一行。若整个表无法与键放在同一行，则将其拆成带键值对的独立节：

```toml
[dependencies]
crate1 = { path = "crate1", version = "1.2.3" }

[dependencies.extremely_long_crate_name_goes_here]
path = "extremely_long_path_name_goes_right_here"
version = "4.5.6"
```

## 元数据约定 {#metadata-conventions}

若存在 `authors` 列表，其中每个字符串应包含作者姓名，后跟尖括号中的电子邮件地址：`Full Name <email@address>`。不应包含裸电子邮件地址，或没有电子邮件地址的姓名。（`authors` 列表也可以包含没有关联姓名的邮件列表地址。）

`license` 字段必须包含有效的 [SPDX 表达式](https://spdx.org/spdx-specification-21-web-version#h.jxpfx0ykyb60)，并使用有效的 [SPDX 许可证名称](https://spdx.org/licenses/)。（作为例外，按广泛惯例，`license` 字段可以用 `/` 代替 ` OR `；例如 `MIT/Apache-2.0`。）

若存在 `homepage` 字段，必须是单个 URL，并包含协议方案（例如 `https://example.org/`，而不能只是 `example.org`）。

在 `description` 字段中，文本按 80 列换行。不要以 crate 名称开头（例如「cratename 是一个……」）；直接描述 crate 本身。若提供多句描述，第一句应单独成行并概括该 crate，类似电子邮件或提交信息的主题；后续句子再更详细地描述该 crate。
