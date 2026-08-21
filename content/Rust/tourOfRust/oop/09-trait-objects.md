+++
title = "09-Trait 对象"
date = 2026-08-17T22:00:00+08:00
weight = 84
type = "docs"
description = "Trait 对象 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/82_zh-cn.html](https://tourofrust.com/82_zh-cn.html)

# Trait 对象

当我们将一个对象的实例传递给类型为 `&dyn MyTrait` 的参数时，我们传递的是所谓的 *trait 对象*。

Trait 对象允许我们间接调用一个实例的正确方法。一个 trait 对象对应一个结构。 它保存着我们实例的指针，并保有一个指向我们实例方法的函数指针列表。

内存细节：
* 这个函数列表在 C++ 中被称为 *vtable*。
