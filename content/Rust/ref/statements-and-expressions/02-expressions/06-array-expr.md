+++
title = "06-数组与索引表达式"
date = 2026-08-18T08:45:00+08:00
weight = 49
type = "docs"
description = "数组与索引表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/array-expr.html](https://doc.rust-lang.org/reference/expressions/array-expr.html)

r[expr.array]
# 数组与索引表达式

## 数组表达式

r[expr.array.syntax]
```grammar,expressions
ArrayExpression -> `[` ArrayElements? `]`

ArrayElements ->
      Expression ( `,` Expression )* `,`?
    | Expression `;` Expression
```

r[expr.array.constructor]
*数组表达式*用于构造[数组][array]。数组表达式有两种形式。

r[expr.array.array]
第一种形式逐一列出数组中的每个值。

r[expr.array.array-syntax]
该形式的语法是：由方括号括起的、类型一致的、以逗号分隔的表达式列表。

r[expr.array.array-behavior]
这会生成一个数组，按书写顺序包含这些值。

r[expr.array.repeat]
第二种形式的语法是：由方括号括起的、以分号（`;`）分隔的两个表达式。

r[expr.array.repeat-operand]
`;` 之前的表达式称为*重复操作数*。

r[expr.array.length-operand]
`;` 之后的表达式称为*长度操作数*。

r[expr.array.length-restriction]
长度操作数必须是[推断常量][inferred const]，或类型为 `usize` 的[常量表达式][constant expression]（例如[字面量][literal]或[常量项][constant item]）。

```rust
const C: usize = 1;
let _: [u8; C] = [0; 1]; // 字面量。
let _: [u8; C] = [0; C]; // 常量项。
let _: [u8; C] = [0; _]; // 推断常量。
let _: [u8; C] = [0; (((_)))]; // 推断常量。
```

> **注意**
> 在数组表达式中，[推断常量][inferred const]按[表达式][Expression]解析，但在语义上被当作一种单独的[const 泛型实参][const generic argument]。

r[expr.array.repeat-behavior]
该形式的数组表达式会创建一个长度为长度操作数值的数组，每个元素都是重复操作数的副本。也就是说，`[a; b]` 会创建一个包含 `b` 个 `a` 的值的副本的数组。

r[expr.array.repeat-copy]
若长度操作数的值大于 1，则要求重复操作数的类型实现 [`Copy`]，或为 [const 块表达式][const block expression]，或为指向常量项的[路径][path]。

r[expr.array.repeat-const-item]
当重复操作数是 const 块或指向常量项的路径时，它会按长度操作数指定的次数求值。

r[expr.array.repeat-evaluation-zero]
若该值为 `0`，则完全不求值该 const 块或常量项。

r[expr.array.repeat-non-const]
对于既不是 const 块也不是指向常量项的路径的表达式，它只求值一次，然后将结果按长度操作数的值复制相应次数。

```rust
[1, 2, 3, 4];
["a", "b", "c", "d"];
[0; 128];              // 含 128 个零的数组
[0u8, 0u8, 0u8, 0u8,];
[[1, 0, 0], [0, 1, 0], [0, 0, 1]]; // 二维数组
const EMPTY: Vec<i32> = Vec::new();
[EMPTY; 2];
```

r[expr.array.index]
## 数组与切片索引表达式

r[expr.array.index.syntax]
```grammar,expressions
IndexExpression -> Expression `[` Expression `]`
```

r[expr.array.index.array]
[数组][Array]和[切片][slice]类型的值可以通过在其后书写一个由方括号括起、类型为 `usize` 的表达式（即索引）来进行索引。当数组可变时，得到的[内存位置][memory location]可以被赋值。

r[expr.array.index.trait]
对其它类型，索引表达式 `a[b]` 等价于 `*std::ops::Index::index(&a, b)`，或在可变位置表达式上下文中等价于 `*std::ops::IndexMut::index_mut(&mut a, b)`，但有一个例外：当索引表达式发生[临时值生命周期延长][temporary lifetime extension]时，被索引表达式 `a` 的[临时作用域][temporary scope]也会被延长。与方法一样，Rust 也会对 `a` 反复插入解引用操作以查找实现。

```rust
// 保存 `vec![()]` 结果的临时值会被延长
// 到块的末尾，因此 `x` 可在后续语句中使用。
let x = &vec![()][0];
## x;
```

```rust
// 保存 `vec![()]` 结果的临时值会在语句末尾被丢弃，
// 因此之后使用 `y` 是错误的。
let y = &*std::ops::Index::index(&vec![()], 0); // 错误
## y;
```

r[expr.array.index.zero-index]
数组和切片的索引从零开始。

r[expr.array.index.const]
数组访问是[常量表达式][constant expression]，因此在索引值为常量时可以在编译期检查边界。否则会在运行时执行检查，失败时会使线程进入 [_panic 状态_][panic]。

```rust
// 该 lint 默认是否认级别。
#![warn(unconditional_panic)]

([1, 2, 3, 4])[2];        // 求值为 3

let b = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
b[1][2];                  // 多维数组索引

let x = (["a", "b"])[10]; // 警告：索引越界

let n = 10;
let y = (["a", "b"])[n];  // 会 panic

let arr = ["a", "b"];
arr[10];                  // 警告：索引越界
```

r[expr.array.index.trait-impl]
通过实现 [Index] 和 [IndexMut] trait，也可以为数组和切片以外的类型实现数组索引表达式。

[`Copy`]: ../special-types-and-traits.md#copy
[IndexMut]: std::ops::IndexMut
[Index]: std::ops::Index
[array]: ../types/array.md
[const generic argument]: items.generics.const.argument
[const block expression]: expr.block.const
[constant expression]: ../const_eval.md#constant-expressions
[constant item]: ../items/constant-items.md
[inferred const]: items.generics.const.inferred
[literal]: ../tokens.md#literals
[memory location]: ../expressions.md#place-expressions-and-value-expressions
[panic]: ../panic.md
[path]: path-expr.md
[slice]: ../types/slice.md
[temporary lifetime extension]: destructors.scope.lifetime-extension
[temporary scope]: destructors.scope.temporary
