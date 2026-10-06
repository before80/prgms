+++
title = "重复借用"
date = 2026-10-06T16:45:00+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://beatai.org/rust-course/compiler/fight-with-compiler/borrowing/intro](https://beatai.org/rust-course/compiler/fight-with-compiler/borrowing/intro)

# 重复借用

　本章讲述如何解决类似`cannot borrow *self as mutable because it is also borrowed as immutable`这种重复借用的错误。
