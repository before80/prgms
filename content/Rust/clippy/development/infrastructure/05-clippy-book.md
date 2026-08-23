+++
title = "05-Clippy 手册"
date = 2026-08-22T18:00:00+08:00
weight = 825
type = "docs"
description = "维护 Clippy book"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Clippy 手册 {#clippy-book}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/infrastructure/book.html](https://doc.rust-lang.org/nightly/clippy/development/infrastructure/book.html)


本文说明如何向 Clippy 手册（你正在阅读的指南）添加与修改内容。Clippy 手册使用 [Markdown](https://www.markdownguide.org) 编写，由 [mdBook](https://github.com/rust-lang/mdBook) 生成。

- [获取 mdBook](#获取-mdbook)
- [进行修改](#进行修改)

## 获取 mdBook

虽然手册源码只是 Markdown 文本文件，不严格需要本地 mdBook，但本地安装后可在提交前构建、测试并提供手册服务以预览更改。你可能已安装 `cargo`，最简单的方式是：

```shell
cargo install mdbook
```

其他安装方式见 mdBook [安装说明](https://github.com/rust-lang/mdBook#installation)。

## 进行修改

手册的
[src](https://github.com/rust-lang/rust-clippy/tree/master/book/src)
目录包含生成手册所用的全部 markdown 文件。若要实时查看更改，可用 mdBook 的 `serve` 命令在本地启动 Web 服务器，修改会自动更新。在 `rust-clippy` 目录顶层运行：

```shell
mdbook serve book --open
```

然后访问 `http://localhost:3000` 查看生成的手册。服务器运行期间，你所做的更改会自动更新。

更多信息见 mdBook
[指南](https://rust-lang.github.io/mdBook/)。
