+++
title = "第15章 作用域规则"
date = 2026-08-20T21:20:00+08:00
weight = 101
type = "docs"
description = "作用域规则 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/scope.html](https://doc.rust-lang.org/stable/rust-by-example/scope.html)

# 作用域规则

作用域在所有权（ownership）、借用（borrow）和生命周期（lifetime）中起着重要作用。也就是说，作用域告诉编译器什么时候借用是合法的、什么时候资源可以释放、以及变量何时被创建或销毁。
