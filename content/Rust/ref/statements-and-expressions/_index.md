+++
title = "第8章 语句与表达式"
date = 2026-08-18T08:45:00+08:00
weight = 41
type = "docs"
description = "语句与表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/statements-and-expressions.html](https://doc.rust-lang.org/reference/statements-and-expressions.html)

r[stmt-expr]
# 语句与表达式

Rust *主要*是一门表达式语言。这意味着大多数产生值或引起效果的求值，都由统一的语法范畴——_表达式_——来引导。每种表达式通常都可以*嵌套*在其他种类的表达式之内；表达式的求值规则既规定表达式产生的值，也规定其子表达式自身的求值顺序。

相比之下，语句*主要*用于包含并显式地顺序化表达式求值。
