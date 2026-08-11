+++
title = "第5章 使用结构体组织相关联的数据"
date = 2026-08-05T08:44:00+08:00
weight = 19
type = "docs"
description = "使用结构体将相关联的数据组织在一起"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 使用结构体组织相关联的数据 {#using-structs-to-structure-related-data}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch05-00-structs.html](https://doc.rust-lang.org/stable/book/ch05-00-structs.html)


　　*结构体*（struct，或 structure）是一种自定义数据类型，能把多个相关值打包在一起并命名，形成一个有意义的组合。如果你熟悉面向对象语言，结构体有点像对象的数据属性。本章会在你已有知识的基础上，对比元组与结构体，并说明何时用结构体组织数据更合适。

　　我们会演示如何定义和实例化结构体，以及如何定义关联函数——尤其是称为*方法*（method）的那一类，用来描述与结构体类型相关的行为。结构体和枚举（第 6 章讨论）是在程序领域中创建新类型、充分发挥 Rust 编译期类型检查优势的基石。
