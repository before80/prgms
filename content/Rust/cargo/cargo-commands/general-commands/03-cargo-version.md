+++
title = "03-cargo version"
date = 2026-07-30T14:49:00+08:00
weight = 44
type = "docs"
description = "cargo-version(1) 显示版本"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-version(1) {#cargo-version1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-version.html](https://doc.rust-lang.org/cargo/commands/cargo-version.html)


## 名称 {#name}
cargo-version --- 显示版本信息

## 大纲 {#synopsis}
`cargo version` [_options_]

## 描述 {#description}
显示 Cargo 的版本。

## 选项 {#options}
<dl>

<dt class="option-term" id="option-cargo-version--v"><a class="option-anchor" href="#option-cargo-version--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-version---verbose"><a class="option-anchor" href="#option-cargo-version---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>显示额外的版本信息。</p>
</dd>


</dl>

## 示例 {#examples}
1. 显示版本：

       cargo version

2. 也可通过标志查看版本：

       cargo --version
       cargo -V

3. 显示额外的版本信息：

       cargo -Vv

## 参见 {#see-also}
[cargo(1)](../01-cargo/)
