+++
title = "12-用私有性保证可扩展性"
date = 2026-08-18T22:10:00+08:00
weight = 19
type = "docs"
description = "用私有性保证可扩展性 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/priv-extend.html](https://rust-unofficial.github.io/patterns/idioms/priv-extend.html)

# 用私有性保证可扩展性

## 描述 {#description}

在少数场景中，库作者可能希望向公开结构体添加公开字段，或向枚举添加新变体，同时不破坏向后兼容性。

Rust 为这个问题提供了两种解决方案：

- 在 `struct`、`enum` 以及 `enum` 变体上使用 `#[non_exhaustive]`。关于 `#[non_exhaustive]` 可用于哪些位置的详尽文档，参见
  [文档](https://doc.rust-lang.org/reference/attributes/type_system.html#the-non_exhaustive-attribute)。

- 可以向结构体添加一个私有字段，以阻止它被直接实例化或匹配（见替代方案）

## 示例 {#example}

```rust
mod a {
    // 公开结构体。
    #[non_exhaustive]
    pub struct S {
        pub foo: i32,
    }

    #[non_exhaustive]
    pub enum AdmitMoreVariants {
        VariantA,
        VariantB,
        #[non_exhaustive]
        VariantC {
            a: String,
        },
    }
}

fn print_matched_variants(s: a::S) {
    // 因为 S 是 `#[non_exhaustive]` 的，此处不能写出全部字段，
    // 必须在模式中使用 `..`。
    let a::S { foo: _, .. } = s;

    let some_enum = a::AdmitMoreVariants::VariantA;
    match some_enum {
        a::AdmitMoreVariants::VariantA => println!("it's an A"),
        a::AdmitMoreVariants::VariantB => println!("it's a b"),

        // 需要 `..`，因为该变体同样是 non-exhaustive 的
        a::AdmitMoreVariants::VariantC { a, .. } => println!("it's a c"),

        // 需要通配匹配，因为将来可能
        // 添加更多变体
        _ => println!("it's a new variant"),
    }
}
```

## 替代方案：结构体的私有字段 {#alternative-private-fields-for-structs}

`#[non_exhaustive]` 只在 crate 边界之外生效。在同一个 crate 内，可以使用私有字段方法。

向结构体添加字段大体上是向后兼容的变更。然而，如果客户端用模式解构结构体实例，它们可能会写出结构体的全部字段，此时再添加一个新字段就会破坏该模式。客户端也可以只写出部分字段并在模式中使用 `..`，这种情况下再添加字段就是向后兼容的。让结构体至少有一个字段是私有的，会迫使客户端使用后一种模式，从而保证该结构体面向未来。

这种方法的缺点是，你可能需要给结构体添加一个本来并不需要的字段。可以使用 `()` 类型以免产生运行时开销，并在字段名前加 `_` 以避免未使用字段的警告。

```rust
pub struct S {
    pub a: i32,
    // 因为 `b` 是私有的，匹配 `S` 时必须使用 `..`，并且 `S`
    //  不能被直接实例化或完整匹配
    _b: (),
}
```

## 讨论 {#discussion}

在 `struct` 上，`#[non_exhaustive]` 允许以向后兼容的方式添加额外字段。即使所有字段都是公开的，它也会阻止客户端使用结构体构造器。这可能有帮助，但值得考虑的是：你是否*希望*客户端以编译错误的方式发现新增字段，而不是让它在无声中被忽略。

`#[non_exhaustive]` 也可以用在枚举变体上。`#[non_exhaustive]` 变体的行为与 `#[non_exhaustive]` 结构体相同。

请有意识地、谨慎地使用它：添加字段或变体时递增主版本号往往是更好的选择。当你在建模一个可能与库不同步变化的外部资源时，`#[non_exhaustive]` 可能合适，但它不是通用工具。

### 缺点 {#disadvantages}

`#[non_exhaustive]` 会让你的代码用起来不那么顺手，尤其是在被迫处理未知枚举变体时。只有在需要这类演进且**不**递增主版本号时，才应使用它。

当 `#[non_exhaustive]` 用在 `enum` 上时，它会迫使客户端处理通配变体。如果在这种情况下没有合理的处理方式，就可能导致别扭的代码，以及只在极其罕见情况下才会执行的代码路径。如果客户端在这种场景下选择 `panic!()`，那么在编译期暴露该错误可能更好。事实上，`#[non_exhaustive]` 迫使客户端处理“其他情况”；而在这种场景下很少有合理的应对办法。

## 参见 {#see-also}

- [为枚举和结构体引入 #[non_exhaustive] 属性的 RFC](https://github.com/rust-lang/rfcs/blob/master/text/2008-non-exhaustive.md)
