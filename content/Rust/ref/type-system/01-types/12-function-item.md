+++
title = "12-函数项类型"
date = 2026-08-18T08:45:00+08:00
weight = 77
type = "docs"
description = "函数项类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/function-item.html](https://doc.rust-lang.org/reference/types/function-item.html)

r[type.fn-item]
# 函数项类型

r[type.fn-item.intro]
当被引用时，函数项，或类元组结构体 / 枚举变体的构造函数，会产生一个[零大小][zero-sized]的*函数项类型*值。

r[type.fn-item.unique]
该类型显式标识该函数——其名称、其类型实参，以及其早绑定生命周期实参（但不包括晚绑定生命周期实参，后者仅在函数被调用时才赋值）——因此该值不必包含实际的函数指针，调用函数时也不需要间接。

r[type.fn-item.name]
没有直接引用函数项类型的语法，但编译器在错误消息中会把该类型显示为类似 `fn(u32) -> i32 {fn_name}` 的形式。

因为函数项类型显式标识函数，不同函数的项类型——不同的项，或同一项搭配不同泛型——是互不相同的，混用它们会产生类型错误：

```rust
fn foo<T>() { }
let x = &mut foo::<i32>;
*x = foo::<u32>; //~ ERROR mismatched types
```

r[type.fn-item.coercion]
不过，存在从函数项到具有相同签名的[函数指针][function pointers]的[强制转换][coercion]，它不仅在直接期望函数指针而使用函数项时触发，也在同一 `if` 或 `match` 的不同分支中遇到具有相同签名的不同函数项类型时触发：

```rust
## let want_i32 = false;
## fn foo<T>() { }

// 此处 `foo_ptr_1` 的类型为函数指针 `fn()`
let foo_ptr_1: fn() = foo::<i32>;

// ……`foo_ptr_2` 也是如此——此代码可通过类型检查。
let foo_ptr_2 = if want_i32 {
    foo::<i32>
} else {
    foo::<u32>
};
```

r[type.fn-item.traits]
所有函数项都实现 [`Copy`]、[`Clone`]、[`Send`] 和 [`Sync`]。

除非函数具有以下任一情况，否则会实现 [`Fn`]、[`FnMut`] 和 [`FnOnce`]：

- [`unsafe`][unsafe.fn] 限定符
- [`target_feature` 属性][attributes.codegen.target_feature]
- 除 `"Rust"` 以外的 [ABI][items.fn.extern]

[`Clone`]: ../special-types-and-traits.md#clone
[`Copy`]: ../special-types-and-traits.md#copy
[`Send`]: ../special-types-and-traits.md#send
[`Sync`]: ../special-types-and-traits.md#sync
[coercion]: ../type-coercions.md
[function pointers]: function-pointer.md
[zero-sized]: glossary.zst
