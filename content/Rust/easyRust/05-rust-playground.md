+++
title = "05-Rust Playground"
date = 2026-08-21T12:46:00+08:00
weight = 6
type = "docs"
description = "Rust Playground — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_4.html](https://dhghomon.github.io/easy_rust/Chapter_4.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Rust Playground

也许你还不想安装Rust，这也没关系。你可以去[https://play.rust-lang.org/](https://play.rust-lang.org/)，在不离开浏览器的情况下开始写Rust。你可以在那里写下你的代码，然后点击Run来查看结果。你可以在浏览器的Playground里面运行本书中的大部分示例。只有在接近结尾的时候，你才会看到无法在Playground运行的示例(比如打开文件)。

以下是使用Rust Playground时的一些提示。

- 用"Run"来运行你的代码

- 如果你想让你的代码更快，就把Debug改为Release。Debug:编译速度更快，运行速度更慢，包含调试信息。Release:编译速度更慢，运行速度更快，删除调试信息。
- 点击Share，得到一个网址链接，你可以用它来分享你的代码。如果你需要帮助，可以用它来分享你的代码。点击分享后，你可以点击`Open a new thread in the Rust user forum`，马上向那里的人寻求帮助。
- Rustfmt工具: Rustfmt会很好地格式化你的代码。
- TOOLS: Rustfmt会很好地格式化你的代码。Clippy会给你额外的信息，告诉你如何让你的代码更好。
- CONFIG: 在这里你可以把你的主题改成黑暗模式，这样你就可以在晚上工作了，还有很多其他配置。

如果你想安装Rust，请到这里[https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)，然后按照说明操作。通常你会使用`rustup`来安装和更新Rust。
