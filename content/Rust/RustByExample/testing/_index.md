+++
title = "第21章 测试"
date = 2026-08-20T21:20:00+08:00
weight = 187
type = "docs"
description = "测试 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/testing.html](https://doc.rust-lang.org/stable/rust-by-example/testing.html)

# 测试

Rust 是一门非常重视正确性的语言，这门语言本身就提供了对编写软件测试的支持。

测试有三种风格：

* [单元][unit]测试。
* [文档][doc]测试。
* [集成][integration]测试。

Rust 也支持在测试中指定额外的依赖：

* [开发依赖][dev-dependencies]

## 参见 {#参见}

* [TRPL][doc-testing] 中关于测试的章节
* [API 指导原则][doc-nursery]中关于文档测试的部分

[unit]: 01-unit-testing/
[doc]: 02-doc-testing/
[integration]: 03-integration-testing/
[dev-dependencies]: 04-dev-dependencies/
[doc-testing]: https://rustwiki.org/zh-CN/book/second-edition/ch11-00-testing.html
[doc-nursery]: https://rust-lang-nursery.github.io/api-guidelines/documentation.html
