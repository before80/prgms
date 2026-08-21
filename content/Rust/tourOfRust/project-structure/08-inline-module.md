+++
title = "08-内联模块"
date = 2026-08-17T22:00:00+08:00
weight = 115
type = "docs"
description = "内联模块 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/113_zh-cn.html](https://tourofrust.com/113_zh-cn.html)

# 内联模块

一个子模块可以直接内联在一个模块的代码中。

内联模块最常见的用途是创建单元测试。 下面我们创建一个只有在使用 Rust 进行测试时才会存在的内联模块！

```
// 当 Rust 不在测试模式时，这个宏会删除这个内联模块。
#[cfg(test)]
mod tests {
    // 请注意，我们并不能立即获得对父模块的访问。我们必须显式地导入它们。
    use super::*;

    ... 单元测试写在这里 ...
}
```
