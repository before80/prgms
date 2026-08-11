+++
title = "第18章 面向对象编程特性"
date = 2026-08-05T08:44:00+08:00
weight = 86
type = "docs"
description = "探讨 Rust 与面向对象特性的关系，以及如何用惯用 Rust 实现相关设计"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 面向对象编程特性 {#object-oriented-programming-features}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch18-00-oop.html](https://doc.rust-lang.org/stable/book/ch18-00-oop.html)


　　面向对象编程（object-oriented programming，OOP）是一种建模程序的方式。作为程序概念的“对象”出现在 1960 年代的 Simula 语言中。这些对象影响了 Alan Kay 的程序架构思想：对象之间互相传递消息。为描述这种架构，他在 1967 年创造了*面向对象编程*一词。关于什么是 OOP，存在许多相互竞争的定义；按其中一些定义，Rust 是面向对象的，按另一些则不是。本章将探讨通常被视为面向对象的若干特征，以及它们如何对应到惯用的 Rust。然后展示如何在 Rust 中实现一种面向对象设计模式，并讨论这样做与改用 Rust 自身优势来实现方案之间的取舍。
