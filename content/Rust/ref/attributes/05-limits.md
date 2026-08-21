+++
title = "05-限制"
date = 2026-08-18T08:45:00+08:00
weight = 38
type = "docs"
description = "限制 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/attributes/limits.html](https://doc.rust-lang.org/reference/attributes/limits.html)

r[attributes.limits]
# 限制

下列[属性][attributes]影响编译期限制。

r[attributes.limits.recursion_limit]
## `recursion_limit` 属性

r[attributes.limits.recursion_limit.intro]
*`recursion_limit` 属性*可应用于 [crate] 级别，以设置可能无限递归的编译期操作（如宏展开或自动解引用）的最大深度。

r[attributes.limits.recursion_limit.syntax]
它使用 [MetaNameValueStr]
语法来指定递归深度。

> **注意**
> `rustc` 中的默认值为 128。

```rust
#![recursion_limit = "4"]

macro_rules! a {
    () => { a!(1); };
    (1) => { a!(2); };
    (2) => { a!(3); };
    (3) => { a!(4); };
    (4) => { };
}

// 展开失败，因为所需递归深度大于 4。
a!{}
```

```rust
#![recursion_limit = "1"]

// 失败，因为自动解引用需要两步递归。
(|_: &u8| {})(&&&1);
```

<!-- template:attributes -->
r[attributes.limits.type_length_limit]
## `type_length_limit` 属性

r[attributes.limits.type_length_limit.intro]
*`type_length_limit` [属性][attributes]*设置在单态化期间构造具体类型时允许的最大类型替换次数。

> **注意**
> 仅当启用 nightly 的 `-Zenforce-type-length-limit` 标志时，`rustc` 才会强制该限制。
>
> 更多信息见 [Rust PR #127670](https://github.com/rust-lang/rust/pull/127670)。

> [!EXAMPLE]
> <!-- ignore: not enforced without nightly flag -->
> ```rust
> #![type_length_limit = "4"]
>
> fn f<T>(x: T) {}
>
> // 编译失败，因为单态化为
> // `f::<((((i32,), i32), i32), i32)>` 所需的
> // 类型元素超过 4 个。
> f(((((1,), 2), 3), 4));
> ```

> **注意**
> `rustc` 中的默认值为 `1048576`。

r[attributes.limits.type_length_limit.syntax]
`type_length_limit` 属性使用 [MetaNameValueStr] 语法。字符串中的值必须是非负数字。

r[attributes.limits.type_length_limit.allowed-positions]
`type_length_limit` 属性只能应用于 crate 根。

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变成错误。

r[attributes.limits.type_length_limit.duplicates]
对同一项多次使用 `type_length_limit` 时，仅第一次生效。

> **注意**
> `rustc` 会对第一次之后的使用发出 lint。将来这可能变成错误。

[attributes]: ../attributes.md
[crate]: ../crates-and-source-files.md
