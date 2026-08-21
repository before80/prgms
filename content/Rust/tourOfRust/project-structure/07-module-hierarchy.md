+++
title = "07-模块层次结构"
date = 2026-08-17T22:00:00+08:00
weight = 114
type = "docs"
description = "模块层次结构 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/112_zh-cn.html](https://tourofrust.com/112_zh-cn.html)

# 模块层次结构

模块可以互相依赖。要建立一个模块和其子模块之间的关系，你需要在父模块中这样写：

```rust
mod foo;
```

上面的声明将使编译器寻找一个名为 `foo.rs `或 `foo/mod.rs` 的文件，并将其内容插入这个作用域内名为 `foo` 的模块中。
