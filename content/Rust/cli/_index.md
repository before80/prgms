+++
title = "Command Line Applications in Rust"
date = 2026-08-01T10:33:00+08:00
weight = 1
type = "docs"
description = "用 Rust 编写命令行应用的入门导读"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 入门 {#getting-started}


> 原文链接: [https://rust-cli.github.io/book/index.html](https://rust-cli.github.io/book/index.html)


Rust 是一门静态编译、运行速度快的语言，工具链出色，生态也在快速成长。
这使它非常适合编写命令行应用：
这类程序应当小巧、可移植，并且启动迅速。
命令行应用也是学习 Rust 的好途径；
或者把 Rust 介绍给你的团队！

为一个简单的命令行界面（CLI）编写程序，
对刚接触这门语言、想上手感受一下的初学者来说，
是很好的练习。
不过这个主题还有许多方面，
往往要到更后面才会显露出来。

本书的结构如下：
我们先从一份快速教程开始，
完成后你会得到一个能用的 CLI 工具。
你将接触到 Rust 的一些核心概念，
以及 CLI 应用的主要方面。
随后的章节会就其中若干方面
展开更细致的讨论。

在正式进入 CLI 应用之前还有一件事：
如果你在本书中发现了错误，
或者想帮我们补充更多内容，
可以在 [CLI book 仓库][book-src] 找到源码。
我们很乐意听到你的反馈！
谢谢！

[book-src]: https://github.com/rust-cli/book
