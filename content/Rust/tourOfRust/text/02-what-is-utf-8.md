+++
title = "02-什么是 utf-8"
date = 2026-08-17T22:00:00+08:00
weight = 62
type = "docs"
description = "什么是 utf-8 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/60_zh-cn.html](https://tourofrust.com/60_zh-cn.html)

# 什么是 utf-8

随着在计算机上使用的语言增加，需要一个能比 ASCII 编码（1 字节表示 1 个字符，总共可表示 256 个字符）表示更多字符的编码来容纳其它语言的字符。

**utf-8** 编码这时被引入来解决这个问题，它用 1-4 个字节来表示 1 个字符，这使得可以表示的字符数大大增加。

使用可变长度的字节来表示字符有一个优点，就是常见的 ASCII 编码字符在 **utf-8** 编码中无需使用更多的字节（也是 1 字节表示 1 个字符）。

但是这样做也有缺点，在 **utf-8** 文本中通过索引来匹配字符（例：`my_text[3]` 获取 my_text 的第 4 个字符）将不能像以前的编码标准那么快（以前编码标准花费 **O(1)** 常数时间）。 这是因为前面的字符具有可变的对应字节，从而无法直接确定第 4 个字符在字节序列中的起始字节。

我们需要遍历 **utf-8** 的字节序列才可以得到对应 Unicode 字符的起始位置（这将花费 **O(n)** 线性时间）。

Ferris：“我只是为 **utf-8** 编码有表示我水中好友的表情符号感到高兴。“

🐠🐙🐟🐬🐋
