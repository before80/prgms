+++
title = "13-你自己的 Prelude"
date = 2026-08-17T22:00:00+08:00
weight = 120
type = "docs"
description = "你自己的 Prelude — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/118_zh-cn.html](https://tourofrust.com/118_zh-cn.html)

# 你自己的 Prelude

你看，既然标准库里面有 prelude，那么你自己的库里面最好也要有一个 prelude 模块。 这个模块可以作为其他使用你的库的用户的起点：他们可以借此导入你的库里面所有常用的数据结构 (例如 `use my_library::prelude::*`)。
当然，这个模块就不会在用了你的库的程序或别的库里面自动启用了。不过使用这个惯例的话，大家会很轻松地知道从何开始的。

Ferris 说：“当个好 rustacean，帮助蟹友奏好序曲（prelude）！”
