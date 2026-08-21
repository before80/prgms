+++
title = "15-函数指针类型"
date = 2026-08-18T08:45:00+08:00
weight = 80
type = "docs"
description = "函数指针类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/function-pointer.html](https://doc.rust-lang.org/reference/types/function-pointer.html)

r[type.fn-pointer]
# 函数指针类型

r[type.fn-pointer.syntax]
```grammar,types
BareFunctionType ->
    ForLifetimes? FunctionTypeQualifiers `fn`
       `(` FunctionParametersMaybeNamedVariadic? `)` BareFunctionReturnType?

FunctionTypeQualifiers -> `unsafe`? (`extern` Abi?)?

BareFunctionReturnType -> `->` TypeNoBounds

FunctionParametersMaybeNamedVariadic ->
    MaybeNamedFunctionParameters | MaybeNamedFunctionParametersVariadic

MaybeNamedFunctionParameters ->
    MaybeNamedParam ( `,` MaybeNamedParam )* `,`?

MaybeNamedParam ->
    OuterAttribute* ( ( IDENTIFIER | `_` ) `:` )? Type

MaybeNamedFunctionParametersVariadic ->
    ( MaybeNamedParam `,` )* MaybeNamedParam `,` OuterAttribute* `...`
```

r[type.fn-pointer.intro]
函数指针类型使用 `fn` 关键字书写，指的是其身份在编译时不一定已知的函数。

下面的例子中，`Binop` 被定义为函数指针类型：

```rust
fn add(x: i32, y: i32) -> i32 {
    x + y
}

let mut x = add(5,7);

type Binop = fn(i32, i32) -> i32;
let bo: Binop = add;
x = bo(5,7);
```

r[type.fn-pointer.coercion]
函数指针可以通过强制转换从[函数项][function items]以及不捕获、非 async 的[闭包][closures]创建。

r[type.fn-pointer.qualifiers]
`unsafe` 限定符表示该类型的值是一个 [unsafe 函数][unsafe function]，而 `extern` 限定符表示它是一个 [extern 函数][extern function]。

r[type.fn-pointer.constraint-variadic]
要使函数为可变参数函数，其 `extern` ABI 必须是 [items.extern.variadic.conventions] 中列出的 ABI 之一。

r[type.fn-pointer.extern-custom]
`extern "custom"` 函数指针必须遵循 [items.fn.extern.custom.signature] 中的规则。

r[type.fn-pointer.attributes]
## 函数指针参数上的属性

函数指针参数上的属性遵循与[普通函数参数][regular function parameters]相同的规则和限制。

[`extern`]: ../items/external-blocks.md
[closures]: closure.md
[extern function]: ../items/functions.md#extern-function-qualifier
[function items]: function-item.md
[unsafe function]: ../unsafe-keyword.md
[regular function parameters]: ../items/functions.md#attributes-on-function-parameters
