+++
title = "04-影响"
date = 2026-08-18T08:45:00+08:00
weight = 119
type = "docs"
description = "影响 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/influences.html](https://doc.rust-lang.org/reference/influences.html)

# 影响

Rust 并不是一门特别原创的语言，其设计元素来自广泛来源。其中一些列于下方（包括后来已移除的元素）：

* SML、OCaml：代数数据类型、模式匹配、类型推断、分号语句分隔
* C++：引用、RAII、智能指针、移动语义、单态化、内存模型
* ML Kit、Cyclone：基于区域的内存管理
* Haskell（GHC）：类型类、类型族
* Newsqueak、Alef、Limbo：通道、并发
* Erlang：消息传递、线程失败、~~链接的线程失败~~、~~轻量级并发~~
* Swift：可选绑定
* Scheme：卫生宏
* C#：属性
* Ruby：闭包语法、~~块语法~~
* NIL、Hermes：~~类型状态（typestate）~~
* [Unicode Annex #31](http://www.unicode.org/reports/tr31/)：标识符与模式语法
