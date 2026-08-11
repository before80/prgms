+++
title = "4.3 强制转型（Cast）"
date = 2026-08-06T17:08:00+08:00
weight = 25
type = "docs"
description = "as 强制转型的安全性与注意点"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 强制转型（Cast）


> 原文链接: [https://doc.rust-lang.org/nomicon/casts.html](https://doc.rust-lang.org/nomicon/casts.html)


　　强制转型（cast）是强制转换的超集：每次强制转换都可通过 cast 显式触发。
　　但有些转换必须用 cast。
　　强制转换无处不在且大体无害，而这些「真正的 cast」罕见且可能危险。
　　因此 cast 必须用 `as` 关键字显式触发：`expr as Type`。

　　[所有真正 cast 的完整列表][cast list]和[cast 语义][semantics list]见 reference。

## cast 的安全性

　　真正的 cast 主要围绕裸指针和原始数值类型。
　　尽管危险，这些 cast 在运行时通常不会失败。
　　若 cast 触发微妙的边角情况，不会有任何提示，cast 只会静默成功。
　　不过 cast 在类型层面必须合法，否则会被静态阻止。
　　例如 `7u8 as bool` 不会编译。

　　cast 不是 `unsafe`，因为它们通常无法*单独*违反内存安全。
　　例如把整数转为裸指针很容易酿成大祸。
　　但创建指针本身是 safe 的，因为使用裸指针已标记为 `unsafe`。

## 关于 cast 的若干说明

### 转换裸切片时的长度

　　注意转换裸切片时长度不会调整；`*const [u16] as *const [u8]` 创建的切片只包含原始内存的一半。

### 传递性

　　cast 没有传递性：即使 `e as U1 as U2` 是合法表达式，`e as U2` 也不一定合法。

[cast list]: ../reference/expressions/operator-expr.html#type-cast-expressions
[semantics list]: ../reference/expressions/operator-expr.html#semantics
