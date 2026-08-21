+++
title = "06-类型系统"
date = 2026-08-18T08:45:00+08:00
weight = 39
type = "docs"
description = "类型系统 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/attributes/type_system.html](https://doc.rust-lang.org/reference/attributes/type_system.html)

r[attributes.type-system]
# 类型系统

下列[属性][attributes]用于改变类型的使用方式。

r[attributes.type-system.non_exhaustive]
## `non_exhaustive` 属性

r[attributes.type-system.non_exhaustive.intro]
*`non_exhaustive` 属性*表示某类型或变体将来可能添加更多字段或变体。

r[attributes.type-system.non_exhaustive.allowed-positions]
它可应用于 [`struct`][struct]、[`enum`][enum] 以及 `enum` 变体。

r[attributes.type-system.non_exhaustive.syntax]
`non_exhaustive` 属性使用 [MetaWord] 语法，因此不接受任何输入。

r[attributes.type-system.non_exhaustive.same-crate]
在定义它的 crate 内部，`non_exhaustive` 没有效果。

```rust
#[non_exhaustive]
pub struct Config {
    pub window_width: u16,
    pub window_height: u16,
}

#[non_exhaustive]
pub struct Token;

#[non_exhaustive]
pub struct Id(pub u64);

#[non_exhaustive]
pub enum Error {
    Message(String),
    Other,
}

pub enum Message {
    #[non_exhaustive] Send { from: u32, to: u32, contents: String },
    #[non_exhaustive] Reaction(u32),
    #[non_exhaustive] Quit,
}

// 在定义 crate 内，非穷尽结构体可以像往常一样构造。
let config = Config { window_width: 640, window_height: 480 };
let token = Token;
let id = Id(4);

// 在定义 crate 内，可以对非穷尽结构体进行穷尽匹配。
let Config { window_width, window_height } = config;
let Token = token;
let Id(id_number) = id;

let error = Error::Other;
let message = Message::Reaction(3);

// 在定义 crate 内，可以对非穷尽枚举进行穷尽匹配。
match error {
    Error::Message(ref s) => { },
    Error::Other => { },
}

match message {
    // 在定义 crate 内，可以对非穷尽变体进行穷尽匹配。
    Message::Send { from, to, contents } => { },
    Message::Reaction(id) => { },
    Message::Quit => { },
}
```

r[attributes.type-system.non_exhaustive.external-crate]
在定义 crate 之外，标注了 `non_exhaustive` 的类型有一些限制，以便在添加新字段或变体时保持向后兼容。

r[attributes.type-system.non_exhaustive.construction]
非穷尽类型不能在定义 crate 之外构造：

- 非穷尽变体（[`struct`][struct] 或 [`enum` 变体][enum]）不能用 [StructExpression]（包括[函数式更新语法][functional update syntax]）构造。
- [类单元结构体][struct]隐式定义的同名常量，或[元组结构体][struct]的同名构造函数，其[可见性][visibility]不高于 `pub(crate)`。
  也就是说，若结构体的可见性是 `pub`，则常量或构造函数的可见性是 `pub(crate)`；否则两者的可见性相同
  （与没有 `#[non_exhaustive]` 时一样）。
- [`enum`][enum] 实例可以构造。

以下构造示例在定义 crate 之外无法编译：

<!-- ignore: requires external crates -->
```rust
// 这些是上游 crate 中已标注为
// `#[non_exhaustive]` 的类型。
use upstream::{Config, Token, Id, Error, Message};

// 不能构造 `Config` 的实例；若 `upstream` 的新版本
// 添加了新字段，则此处将无法编译，因此被禁止。
let config = Config { window_width: 640, window_height: 480 };

// 不能构造 `Token` 的实例；若添加了新字段，
// 它将不再是类单元结构体，因此由其作为类单元结构体
// 而创建的同名常量在 crate 外不是公开的；
// 此代码无法编译。
let token = Token;

// 不能构造 `Id` 的实例；若添加了新字段，
// 其构造函数签名会改变，因此其构造函数
// 在 crate 外不是公开的；此代码无法编译。
let id = Id(5);

// 可以构造 `Error` 的实例；引入新变体
// 不会导致此处无法编译。
let error = Error::Message("foo".to_string());

// 不能构造 `Message::Send` 或 `Message::Reaction` 的实例；
// 若 `upstream` 的新版本添加了新字段，则此处将
// 无法编译，因此被禁止。
let message = Message::Send { from: 0, to: 1, contents: "foo".to_string(), };
let message = Message::Reaction(0);

// 不能构造 `Message::Quit` 的实例；若它在 `upstream` 中
// 被转换为元组枚举变体，则此处将无法编译。
let message = Message::Quit;
```

r[attributes.type-system.non_exhaustive.match]
在定义 crate 之外匹配非穷尽类型时存在限制：

- 对非穷尽变体（[`struct`][struct] 或 [`enum` 变体][enum]）进行模式匹配时，必须使用包含 `..` 的 [StructPattern]。元组枚举变体构造函数的[可见性][visibility]会被降低到不高于 `pub(crate)`。
- 对非穷尽 [`enum`][enum] 进行模式匹配时，匹配某个变体并不计入分支的穷尽性。以下匹配示例在定义 crate 之外无法编译：

<!-- ignore: requires external crates -->
```rust
// 这些是上游 crate 中已标注为
// `#[non_exhaustive]` 的类型。
use upstream::{Config, Token, Id, Error, Message};

// 匹配非穷尽枚举时必须包含通配分支。
match error {
  Error::Message(ref s) => { },
  Error::Other => { },
  // 加上 `_ => {},` 即可编译
}

// 匹配非穷尽结构体时必须包含通配符。
if let Ok(Config { window_width, window_height }) = config {
    // 加上 `..` 即可编译
}

// 不能匹配非穷尽的类单元或元组结构体，除非使用
// 带通配符的花括号结构体语法。
// 写成 `let Token { .. } = token;` 即可编译
let Token = token;
// 写成 `let Id { 0: id_number, .. } = id;` 即可编译
let Id(id_number) = id;

match message {
  // 匹配非穷尽结构体枚举变体时必须包含通配符。
  Message::Send { from, to, contents } => { },
  // 不能匹配非穷尽的元组或单元枚举变体。
  Message::Reaction(type) => { },
  Message::Quit => { },
}
```

也不允许对包含任何非穷尽变体的枚举使用数值转换（`as`）。

例如，下列枚举可以转换，因为它不包含任何非穷尽变体：

```rust
#[non_exhaustive]
pub enum Example {
    First,
    Second,
}
```

然而，若枚举即使只包含一个非穷尽变体，转换也会导致错误。考虑同一枚举的如下修改版本：

```rust
#[non_exhaustive]
pub enum EnumWithNonExhaustiveVariants {
    First,
    #[non_exhaustive]
    Second,
}
```

<!-- ignore: needs multiple crates -->
```rust
use othercrate::EnumWithNonExhaustiveVariants;

// 错误：不能对在另一 crate 中定义且含有非穷尽变体的枚举进行转换
let _ = EnumWithNonExhaustiveVariants::First as u8;
```

在下游 crate 中，非穷尽类型始终被视为有居住（inhabited）。

[`match`]: ../expressions/match-expr.md
[attributes]: ../attributes.md
[enum]: ../items/enumerations.md
[functional update syntax]: ../expressions/struct-expr.md#functional-update-syntax
[struct]: ../items/structs.md
[visibility]: ../visibility-and-privacy.md
