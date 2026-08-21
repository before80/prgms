+++
title = "15-第五章 - 总结"
date = 2026-08-17T22:00:00+08:00
weight = 59
type = "docs"
description = "第五章 - 总结 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/57_zh-cn.html](https://tourofrust.com/57_zh-cn.html)

# 第五章 - 总结

哇，恭喜您成功走完了本章！我知道这下可能会有很多需要吸收的东西，但是您已经在成为一名 Rustacean 的路上走得很好了。希望您能愈发清晰地认识到 Rust 是如何致力于解决系统编程中的诸多常见挑战：
* 无意间对资源的修改
* 忘记及时地释放资源
* 资源意外地被释放两次
* 在资源被释放后使用了它
* 由于读取数据的同时有其他人正在向资源中写入数据而引起的数据争用
* 在编译器无法做担保时，清晰看到代码的作用域

在下一章中，我们会研究一些 Rust 如何处理文本的相关知识。
