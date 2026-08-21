+++
title = "02-数值类型"
date = 2026-08-18T08:45:00+08:00
weight = 67
type = "docs"
description = "数值类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/numeric.html](https://doc.rust-lang.org/reference/types/numeric.html)

r[type.numeric]
# 数值类型

r[type.numeric.int]
## 整数类型

r[type.numeric.int.unsigned]
无符号整数类型包括：

类型   | 最小值 | 最大值
-------|---------|-------------------
`u8`   | 0       | 2<sup>8</sup>-1
`u16`  | 0       | 2<sup>16</sup>-1
`u32`  | 0       | 2<sup>32</sup>-1
`u64`  | 0       | 2<sup>64</sup>-1
`u128` | 0       | 2<sup>128</sup>-1

r[type.numeric.int.signed]
有符号二进制补码整数类型包括：

类型   | 最小值            | 最大值
-------|--------------------|-------------------
`i8`   | -(2<sup>7</sup>)   | 2<sup>7</sup>-1
`i16`  | -(2<sup>15</sup>)  | 2<sup>15</sup>-1
`i32`  | -(2<sup>31</sup>)  | 2<sup>31</sup>-1
`i64`  | -(2<sup>63</sup>)  | 2<sup>63</sup>-1
`i128` | -(2<sup>127</sup>) | 2<sup>127</sup>-1

r[type.numeric.float]
## 浮点类型

IEEE 754-2008 的 "binary32" 和 "binary64" 浮点类型分别是 `f32` 和 `f64`。

r[type.numeric.int.size]
## 机器相关的整数类型

r[type.numeric.int.size.usize]
`usize` 是无符号整数类型，位数与平台指针类型相同。它可以表示进程中的每一个内存地址。

> **注意**
> 虽然 `usize` 可以表示每一个*地址*，但将*指针*转换为 `usize` 不一定是可逆操作。更多信息见[类型转换表达式][type cast expressions]、[`std::ptr`] 以及特别是 [provenance][std::ptr#provenance] 的文档。

r[type.numeric.int.size.isize]
`isize` 是有符号二进制补码整数类型，位数与平台指针类型相同。对象和数组大小的理论上界是 `isize` 的最大值。这保证了 `isize` 可用于计算指向同一对象或数组的指针之间的差，并且可以寻址对象内的每一个字节以及末尾之后的一个字节。

r[type.numeric.int.size.minimum]
`usize` 和 `isize` 至少为 16 位宽。

> **注意**
> 许多 Rust 代码会假定指针、`usize` 和 `isize` 要么是 32 位要么是 64 位。因此，16 位指针支持有限，库若要支持可能需要显式处理并加以说明。

r[type.numeric.validity]
## 位有效性

对每一个数值类型 `T`，`T` 的位有效性等价于 `[u8; size_of::<T>()]` 的位有效性。未初始化的字节不是合法的 `u8`。

[type cast expressions]: ../expressions/operator-expr.md#type-cast-expressions
