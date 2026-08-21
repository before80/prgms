+++
title = "03-函数式光学"
date = 2026-08-18T22:10:00+08:00
weight = 49
type = "docs"
description = "函数式光学 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/functional/optics.html](https://rust-unofficial.github.io/patterns/functional/optics.html)

# 函数式光学

光学（Optics）是一种在函数式语言中常见的 API 设计。这是一个纯函数式概念，在 Rust 中并不常用。

尽管如此，探索这一概念可能有助于理解 Rust API 中的其他模式，例如[访问者](../design-patterns/01-behavioural/06-visitor/)。它们也有一些小众用例。

这是一个相当大的主题，要充分把握其能力需要真正关于语言设计的专著。然而它们在 Rust 中的适用性要简单得多。

为解释相关部分，将以 `Serde` API 为例——很多人仅从 API 文档很难理解它。

过程中会涵盖几种具体的模式，称为光学。它们是 *The Iso*、*The Poly Iso* 与 *The Prism*。

## 一个 API 示例：Serde {#an-api-example-serde}

仅靠阅读 API 来理解 *Serde* 的工作方式是一项挑战，尤其是第一次。考虑由任何解析新数据格式的库所实现的 `Deserializer` trait：

```rust,ignore
pub trait Deserializer<'de>: Sized {
    type Error: Error;

    fn deserialize_any<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    fn deserialize_bool<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    // 其余从略
}
```

下面是作为泛型传入的 `Visitor` trait 的定义：

```rust,ignore
pub trait Visitor<'de>: Sized {
    type Value;

    fn visit_bool<E>(self, v: bool) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_u64<E>(self, v: u64) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_str<E>(self, v: &str) -> Result<Self::Value, E>
    where
        E: Error;

    // 其余从略
}
```

这里有大量类型擦除，多层关联类型来回传递。

但大局是什么？为何不只让 `Visitor` 在流式 API 中返回调用方所需的片段就完事？为何要有这些额外部分？

一种理解方式是看函数式语言中称为 *optics*（光学）的概念。

这是一种行为与性质的组合方式，旨在便利 Rust 中常见的模式：失败、类型转换等。[^1]

Rust 语言对这些概念没有很好的直接支持。然而，它们出现在语言本身的设计中，其概念有助于理解 Rust 的一些 API。因此，本文尝试用 Rust 的做法来解释这些概念。

这或许能阐明那些 API 在达成什么：特定的可组合性性质。

## 基础光学 {#basic-optics}

### Iso（同构） {#the-iso}

Iso 是两种类型之间的值转换器。它极其简单，却是概念上重要的构建块。

举例来说，假设我们有一个自定义哈希表结构，用作文档的索引（concordance）。[^2] 它用字符串作键（单词），用索引列表作值（例如文件偏移）。

一个关键特性是能把这种格式序列化到磁盘。一种「快速脏写」的做法是实现与 JSON 格式字符串之间的双向转换。（暂时忽略错误，稍后处理。）

用函数式语言用户所期望的标准形式来写：

```text
case class ConcordanceSerDe {
  serialize: Concordance -> String
  deserialize: String -> Concordance
}
```

因此 Iso 是一对在不同类型的值之间转换的函数：`serialize` 与 `deserialize`。

一种直接的实现：

```rust
use std::collections::HashMap;

struct Concordance {
    keys: HashMap<String, usize>,
    value_table: Vec<(usize, usize)>,
}

struct ConcordanceSerde {}

impl ConcordanceSerde {
    fn serialize(value: Concordance) -> String {
        todo!()
    }
    // 无效的 concordance 为空
    fn deserialize(value: String) -> Concordance {
        todo!()
    }
}
```

这可能显得相当傻。在 Rust 中，这类行为通常用 trait 完成。毕竟标准库里已有 `FromStr` 和 `ToString`。

但那正是下一主题的切入点：Poly Isos。

### 多态 Iso {#poly-isos}

前一个例子只是在两个固定类型的值之间转换。下一块在其上用泛型构建，更有趣。

Poly Isos 允许某个操作对任意类型泛型化，同时返回单一类型。

这让我们更接近解析。考虑一个基本解析器在忽略错误情形时会做什么。同样，这是其标准形式：

```text
case class Serde[T] {
    deserialize(String) -> T
    serialize(T) -> String
}
```

这里我们有了第一个泛型：被转换的类型 `T`。

在 Rust 中，这可以用标准库中的一对 trait 实现：`FromStr` 与 `ToString`。Rust 版本甚至处理了错误：

```rust,ignore
pub trait FromStr: Sized {
    type Err;

    fn from_str(s: &str) -> Result<Self, Self::Err>;
}

pub trait ToString {
    fn to_string(&self) -> String;
}
```

与 Iso 不同，Poly Iso 允许多种类型的应用，并泛型地返回它们。这正是基本字符串解析器想要的。

乍一看，这似乎是写解析器的好选择。让我们看看实际效果：

```rust,ignore
use anyhow;

use std::str::FromStr;

struct TestStruct {
    a: usize,
    b: String,
}

impl FromStr for TestStruct {
    type Err = anyhow::Error;
    fn from_str(s: &str) -> Result<TestStruct, Self::Err> {
        todo!()
    }
}

impl ToString for TestStruct {
    fn to_string(&self) -> String {
        todo!()
    }
}

fn main() {
    let a = TestStruct {
        a: 5,
        b: "hello".to_string(),
    };
    println!("Our Test Struct as JSON: {}", a.to_string());
}
```

这看起来相当合乎逻辑。然而，有两个问题。

第一，`to_string` 并不会向 API 用户表明「这是 JSON」。每种类型都需要对 JSON 表示达成一致，而 Rust 标准库中的许多类型已经并不如此。用它并不合适。这很容易用我们自己的 trait 解决。

但还有第二个更微妙的问题：扩展性。

当每种类型都手写 `to_string` 时，这能工作。但如果每个想让自己的类型可序列化的人都必须自己写一大堆代码——还可能用不同的 JSON 库——很快就会变成一团糟！

答案是 Serde 的两项关键创新之一：一个独立的数据模型，用数据序列化语言中常见的结构来表示 Rust 数据。结果是它可以利用 Rust 的代码生成能力创建一个中间转换类型，称为 `Visitor`。

这意味着，用标准形式（同样为简洁起见跳过错误处理）：

```text
case class Serde[T] {
    deserialize: Visitor[T] -> T
    serialize: T -> Visitor[T]
}

case class Visitor[T] {
    toJson: Visitor[T] -> String
    fromJson: String -> Visitor[T]
}
```

结果是一个 Poly Iso 和一个 Iso（分别对应）。两者都可以用 trait 实现：

```rust
trait Serde {
    type V;
    fn deserialize(visitor: Self::V) -> Self;
    fn serialize(self) -> Self::V;
}

trait Visitor {
    fn to_json(self) -> String;
    fn from_json(json: String) -> Self;
}
```

因为把 Rust 结构转换到独立形式有一套统一规则，甚至可以用代码生成创建与类型 `T` 关联的 `Visitor`：

```rust,ignore
#[derive(Default, Serde)] // 「Serde」derive 会创建 trait impl 块
struct TestStruct {
    a: usize,
    b: String,
}

// 用户编写此宏以生成关联的 visitor 类型
generate_visitor!(TestStruct);
```

但让我们真正试一下这种方法。

```rust,ignore
fn main() {
    let a = TestStruct { a: 5, b: "hello".to_string() };
    let a_data = a.serialize().to_json();
    println!("Our Test Struct as JSON: {a_data}");
    let b = TestStruct::deserialize(
        generated_visitor_for!(TestStruct)::from_json(a_data));
}
```

结果是转换终究并不对称！理论上是对称的，但有了自动生成的代码，从 `String` 一路转换所需的实际类型名是隐藏的。我们需要某种 `generated_visitor_for!` 宏来获取类型名。

虽然别扭，但它能工作……直到我们碰到房间里的大象。

当前支持的唯一格式是 JSON。我们如何支持更多格式？

当前设计要求完全重写所有代码生成并创建新的 Serde trait。这相当糟糕，而且完全不可扩展！

为了解决这一点，我们需要更强大的东西。

## Prism（棱镜） {#prism}

要把格式纳入考虑，我们需要类似这样的标准形式：

```text
case class Serde[T, F] {
    serialize: T, F -> String
    deserialize: String, F -> Result[T, Error]
}
```

这种构造称为 Prism。它在泛型上比 Poly Isos「高一层」（在此例中，「相交」类型 F 是关键）。

不幸的是，因为 `Visitor` 是一个 trait（每种化身都需要自己的定制代码），这会要求一种 Rust 不支持的泛型类型边界。

幸运的是，我们仍有之前的 `Visitor` 类型。`Visitor` 在做什么？它试图让每个数据结构定义自身的解析方式。

那么，如果我们能为通用格式再加一个接口呢？那样 `Visitor` 就只是实现细节，它会「桥接」这两个 API。

用标准形式：

```text
case class Serde[T] {
    serialize: F -> String
    deserialize F, String -> Result[T, Error]
}

case class VisitorForT {
    build: F, String -> Result[T, Error]
    decompose: F, T -> String
}

case class SerdeFormat[T, V] {
    toString: T, V -> String
    fromString: V, String -> Result[T, Error]
}
```

你瞧，底部是一对可以作为 trait 实现的 Poly Isos！

于是我们有了 Serde API：

1. 每个要序列化的类型实现 `Deserialize` 或 `Serialize`，等价于 `Serde` 类
1. 它们获得一个（其实是两个，每个方向一个）实现 `Visitor` trait 的类型，通常（但不总是）通过 derive 宏生成的代码完成。其中包含在该数据类型与 Serde 数据模型格式之间构造或解构的逻辑。
1. 实现 `Deserializer` trait 的类型处理所有格式特有的细节，并由 `Visitor`「驱动」。

这种拆分与 Rust 的类型擦除，实质上是通过间接手段实现 Prism。

你可以在 `Deserializer` trait 上看到它

```rust,ignore
pub trait Deserializer<'de>: Sized {
    type Error: Error;

    fn deserialize_any<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    fn deserialize_bool<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    // 其余从略
}
```

以及 visitor：

```rust,ignore
pub trait Visitor<'de>: Sized {
    type Value;

    fn visit_bool<E>(self, v: bool) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_u64<E>(self, v: u64) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_str<E>(self, v: &str) -> Result<Self::Value, E>
    where
        E: Error;

    // 其余从略
}
```

以及由宏实现的 `Deserialize` trait：

```rust,ignore
pub trait Deserialize<'de>: Sized {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>;
}
```

以上较为抽象，让我们看一个具体例子。

实际的 Serde 如何把一段 JSON 反序列化成前面的 `struct Concordance`？

1. 用户会调用某个库函数来反序列化数据。这会基于 JSON 格式创建一个 `Deserializer`。
1. 基于结构体的字段，会创建一个 `Visitor`（稍后详述），它知道如何在表示该结构所需的通用数据模型中创建每种类型：`Vec`（列表）、`u64` 和 `String`。
1. 当解析器解析到各项时，会对 `Visitor` 发起调用。
1. `Visitor` 会指示找到的项是否符合预期；若不符合，则引发错误以表明反序列化失败。

对于上面非常简单的结构，预期模式会是：

1. 开始访问一个 map（*Serde* 中等价于 `HashMap` 或 JSON 的字典）。
1. 访问一个名为 "keys" 的字符串键。
1. 开始访问一个 map 值。
1. 对每一项，访问一个字符串键，然后是一个整数值。
1. 访问 map 的结束。
1. 把该 map 存入数据结构的 `keys` 字段。
1. 访问一个名为 "value_table" 的字符串键。
1. 开始访问一个列表值。
1. 对每一项，访问一个整数。
1. 访问列表的结束
1. 把该列表存入 `value_table` 字段。
1. 访问 map 的结束。

但什么决定了预期的「观察」模式？

函数式编程语言能够用柯里化基于类型本身创建每种类型的反射。Rust 不支持这一点，因此每种类型都需要根据其字段及其属性编写自己的代码。

*Serde* 用 derive 宏解决这一可用性挑战：

```rust,ignore
use serde::Deserialize;

#[derive(Deserialize)]
struct IdRecord {
    name: String,
    customer_id: String,
}
```

该宏只是生成一个 impl 块，使结构体实现名为 `Deserialize` 的 trait。

这就是决定如何创建结构体本身的函数。代码基于结构体的字段生成。当调用解析库时——在我们的例子中是 JSON 解析库——它创建一个 `Deserializer`，并以之为参数调用 `Type::deserialize`。

`deserialize` 代码随后会创建一个 `Visitor`，其调用会被 `Deserializer`「折射」。若一切顺利，最终该 `Visitor` 会构造出对应于正在解析之类型的值并返回它。

完整示例见
[*Serde* 文档](https://serde.rs/deserialize-struct.html)。

结果是：要反序列化的类型只需实现 API 的「顶层」，文件格式只需实现「底层」。每一部分都能与生态系统的其余部分「即插即用」，因为泛型类型会桥接它们。

总之，Rust 受泛型启发的类型系统可以接近这些概念并运用其能力，如本 API 设计所示。但它也可能需要过程宏来为其泛型创建桥梁。

若你有兴趣深入了解该主题，请查看下一节。

## 参见 {#see-also}

- [lens-rs crate](https://crates.io/crates/lens-rs)：预构建的 lenses
  实现，接口比这些示例更干净
- [Serde](https://serde.rs) 本身，使这些概念对最终用户（即定义结构体的人）直观，而无需理解细节
- [luminance](https://github.com/phaazon/luminance-rs) 是一个用于绘制
  计算机图形的 crate，使用类似的 API 设计，包括过程宏，
  为保持泛型的不同像素类型缓冲区创建完整的 prism
- [一篇关于 Scala 中 Lenses 的文章](https://web.archive.org/web/20221128185849/https://medium.com/zyseme-technology/functional-references-lens-and-other-optics-in-scala-e5f7e2fdafe)，
  即使没有 Scala 专长也很好读。
- [论文：Profunctor Optics: Modular Data Accessors](https://web.archive.org/web/20220701102832/https://arxiv.org/ftp/arxiv/papers/1703/1703.10857.pdf)（Profunctor 光学：模块化数据访问器）
- [Musli](https://github.com/udoprog/musli) 是一个尝试用
  类似结构但不同方法的库，例如去掉 visitor

[^1]: [School of Haskell: A Little Lens Starter Tutorial](https://web.archive.org/web/20221128190041/https://www.schoolofhaskell.com/school/to-infinity-and-beyond/pick-of-the-week/a-little-lens-starter-tutorial)（Haskell 学堂：Lens 入门教程）

[^2]: [维基百科上的 Concordance](https://en.wikipedia.org/wiki/Concordance_(publishing))
