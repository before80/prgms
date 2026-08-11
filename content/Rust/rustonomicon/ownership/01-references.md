+++
title = "3.1 引用"
date = 2026-08-06T17:08:00+08:00
weight = 11
type = "docs"
description = "引用的语义与规则"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 引用


> 原文链接: [https://doc.rust-lang.org/nomicon/references.html](https://doc.rust-lang.org/nomicon/references.html)


　　引用有两种：

* 共享引用：`&`
* 可变引用：`&mut`

　　遵循下列规则：

* 引用不能比被引用对象活得更久
* 可变引用不能 alias（别名）

　　就这些。这就是引用遵循的完整模型。

　　当然，我们大概应定义*alias* 是什么意思。

```text
error[E0425]: cannot find value `aliased` in this scope
 --> <rust.rs>:2:20
  |
2 |     println!("{}", aliased);
  |                    ^^^^^^^ not found in this scope

error: aborting due to previous error
```

　　遗憾的是，Rust 实际上尚未定义其 alias 模型。🙀

　　在等 Rust 开发者明确语言语义时，下一节讨论 alias 一般是什么，以及为何重要。
