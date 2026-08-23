+++
title = "2.5 理解型变、引用与重借用"
date = 2026-08-23T10:16:00+08:00
weight = 14
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Learning Rust](https://quinedot.github.io/rust-learning/)

# 理解型变、引用与重借用 {#variance-references-reborrows}


> 原文链接: [https://quinedot.github.io/rust-learning/subtypes.html](https://quinedot.github.io/rust-learning/subtypes.html)


[这里有关于型变主题的官方文档，](https://doc.rust-lang.org/reference/subtyping.html) 但读起来可能让人眼花缭乱。作为替代，本节尝试通过几个层次，介绍引用与生命周期如何配合的一些基本规则。

如果仍然让你头晕，略读或跳过即可。
