+++
title = "第5章 所有权和数据借用"
date = 2026-08-17T22:00:00+08:00
weight = 44
type = "docs"
description = "第五章 - 所有权和数据借用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/chapter_5_zh-cn.html](https://tourofrust.com/chapter_5_zh-cn.html)

# 第五章 - 所有权和数据借用

相较于其他编程语言，Rust 具有一套独特的内存管理范例。为了不让您被概念性的东西淹没，我们将一一展示这些编译器的行为和验证方式。 有一点很重要：所有这些规则的终极目的不是为了为难您，而是为了更好地降低代码的出错率！
