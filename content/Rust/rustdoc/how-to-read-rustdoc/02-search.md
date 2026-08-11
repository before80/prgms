+++
title = "02-搜索"
date = 2026-08-01T07:35:00+08:00
weight = 32
type = "docs"
description = "rustdoc 文档搜索功能说明"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 搜索 {#search}


> 原文链接: [https://doc.rust-lang.org/rustdoc/read-documentation/search.html](https://doc.rust-lang.org/rustdoc/read-documentation/search.html)


在搜索栏中输入会立即搜索可用文档，匹配项的名称与路径，或函数的近似类型签名。

## 按名称搜索 {#search-by-name}

要按项的名称搜索（项包括模块、类型、trait、函数和宏），写出其名称或路径。作为特例，路径中通常由 `::` 双冒号分隔的部分也可以用空格分隔。例如：

  * [`vec new`] 和 [`vec::new`] 都会把函数 `std::vec::Vec::new` 显示为结果。
  * [`vec`]、[`vec vec`]、[`std::vec`] 和 [`std::vec::Vec`] 都会在结果中包含结构体 `std::vec::Vec` 本身（除最后一个外，也都包含该模块）。

[`vec new`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=vec%20new&filter-crate=std
[`vec::new`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=vec::new&filter-crate=std
[`vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=vec&filter-crate=std
[`vec vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=vec%20vec&filter-crate=std
[`std::vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=std::vec&filter-crate=std
[`std::vec::Vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=std::vec::Vec&filter-crate=std

缩小结果列表的快捷方式是搜索输入框下方标有 “Results in \[std\]” 的下拉选择器。点击它可以更改正在搜索的 crate。

rustdoc 对此使用可容忍拼写错误的模糊匹配，其容错程度取决于输入名称的长度；[`HahsMap`] 就是很好的例子（会匹配到 `HashMap`）。若要禁用模糊匹配，用引号包裹该项，搜索 `"HahsMap"`（在本例中不会返回任何结果）。

[`HahsMap`]: https://doc.rust-lang.org/std/collections/struct.HashMap.html?search=HahsMap&filter-crate=std

### 按名称搜索界面中的标签页 {#tabs-in-the-search-by-name-interface}

实际上，再次以 [`HahsMap`] 为例，它会告诉你默认使用的是 “In Names”，但在 crate 下拉框下方还会列出另外两个标签页：“In Parameters” 和 “In Return Types”。

这两个标签页是函数列表，定义在与搜索最接近匹配的类型上（对于 `HahsMap`，它会明显地自动纠正为 `hashmap`）。仅当没有任何字面匹配时，才会启动这种自动纠正。

这些标签页不只是方法。例如，在 alloc crate 中搜索 [`Layout`] 也会列出接受 layout 的函数，即使它们是分配器上的方法或自由函数。

[`Layout`]: https://doc.rust-lang.org/alloc/index.html?search=Layout&filter-crate=alloc

## 按类型签名搜索 {#searching-by-type-signature}

如果你更具体地知道想查看的函数做什么，或者想知道如何从一个类型到达另一个类型，rustdoc 可以一次在参数和返回值中搜索不止一个类型。多个参数用 `,` 逗号分隔，返回值写在 `->` 箭头之后。

在更详细地描述语法之前，先看几个标准库的示例搜索以及结果列表中包含的函数：

| 查询 | 结果 |
|-------|---------|
| [`usize -> vec`][] | `slice::repeat` 和 `Vec::with_capacity` |
| [`vec, vec -> bool`][] | `Vec::eq` |
| [`option<T>, fnonce -> option<U>`][] | `Option::map` 和 `Option::and_then` |
| [`option<T>, (fnonce (T) -> bool) -> option<T>`][optionfilter] | `Option::filter` |
| [`option<T>, (T -> bool) -> option<T>`][optionfilter2] | `Option::filter` |
| [`option -> default`][] | `Option::unwrap_or_default` |
| [`stdout, [u8]`][stdoutu8] | `Stdout::write` |
| [`any -> !`][] | `panic::panic_any` |
| [`vec::intoiter<T> -> [T]`][iterasslice] | `IntoIter::as_slice` 和 `IntoIter::next_chunk` |
| [`iterator<T>, fnmut -> T`][iterreduce] | `Iterator::reduce` 和 `Iterator::find` |

[`usize -> vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=usize%20-%3E%20vec&filter-crate=std
[`vec, vec -> bool`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=vec,%20vec%20-%3E%20bool&filter-crate=std
[`option<T>, fnonce -> option<U>`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=option<T>%2C%20fnonce%20->%20option<U>&filter-crate=std
[optionfilter]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=option<T>%2C+(fnonce+(T)+->+bool)+->+option<T>&filter-crate=std
[optionfilter2]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=option<T>%2C+(T+->+bool)+->+option<T>&filter-crate=std
[`option -> default`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=option%20-%3E%20default&filter-crate=std
[`any -> !`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=any%20-%3E%20!&filter-crate=std
[stdoutu8]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=stdout%2C%20[u8]&filter-crate=std
[iterasslice]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=vec%3A%3Aintoiter<T>%20->%20[T]&filter-crate=std
[iterreduce]: https://doc.rust-lang.org/std/index.html?search=iterator<T>%2C%20fnmut%20->%20T&filter-crate=std

### 基于类型的搜索中的非函数项 {#non-functions-in-type-based-search}
某些不是函数的项会被当作语义上等价的函数来处理。

例如，结构体字段会被当作 getter 方法。这意味着搜索 `CpuidResult -> u32` 会在结果中显示 `CpuidResult::eax` 字段。

此外，`const` 和 `static` 项会被当作零元函数，因此 `-> u32` 会匹配 `u32::MAX`。

### 基于类型的搜索如何工作 {#how-type-based-search-works}

在复杂的基于类型的搜索中，rustdoc 始终将每个项的名称视为字面量。如果使用了某个名称，而文档中没有任何内容匹配该单独项，例如拼写错误的 [`uize -> vec`][] 搜索，则项 `uize` 会被当作泛型类型参数（从而得到 `vec::from` 以及其它泛型的 vec 构造函数）。

[`uize -> vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=uize%20-%3E%20vec&filter-crate=std

在决定哪些项是类型参数、哪些是实际类型之后，它通过匹配函数参数（写在 `->` 之前）和返回类型（写在 `->` 之后）来搜索。类型匹配与顺序无关，并允许查询中省略某些项，但查询中出现的项必须出现在函数中才能匹配。`self` 参数与其它任何参数同等对待，`Self` 会解析为底层类型的名称。

函数签名搜索可以查询泛型（用尖括号包裹），并且如果没有类型参数匹配它们，trait 会像搜索引擎中的类型一样被规范化。例如，签名为
`fn my_function<I: Iterator<Item=u32>>(input: I) -> usize`
的函数可以用以下查询匹配：

* `Iterator<Item=u32> -> usize`
* `Iterator<u32> -> usize`（可以省略 `Item=` 部分）
* `Iterator -> usize`（可以完全省略 iterator 的泛型）
* `T -> usize`（可以用泛型参数匹配）

上面的查询越来越宽松，但最后一个不会匹配 `dyn Iterator`，因为那不是类型参数。

如果一个 bound 有多个关联类型，指定名称可以让你选择匹配哪一个。如果未指定名称，则查询会匹配其中任意一个。例如，

```rust
pub trait MyTrait {
    type First;
    type Second;
}

/// 可以用以下搜索查询找到此函数：
///
///     MyTrait<First=u8, Second=u32> -> bool
///     MyTrait<Second=u32> -> bool
///
/// 然而，以下查询*不会*匹配它：
///
///     MyTrait<First=u32> -> bool
///     MyTrait<u32, u32> -> bool
///     MyTrait<u32, First=u8> -> bool
///     MyTrait<u32, u8> -> bool
pub fn my_fn(x: impl MyTrait<First=u8, Second=u32>) -> bool { true }
```

函数参数与顺序无关，但对嵌套和匹配数量敏感。例如，签名为
`fn read_all(&mut self: impl Read) -> Result<Vec<u8>, Error>`
的函数会匹配这些查询：

* `&mut Read -> Result<Vec<u8>, Error>`
* `Read -> Result<Vec<u8>, Error>`
* `Read -> Result<Vec<u8>>`
* `Read -> Vec<u8>`

但它*不会*匹配 `Result<Vec, u8>` 或 `Result<u8<Vec>>`，因为那些嵌套不正确；也不会匹配 `Result<Error, Vec<u8>>` 或 `Result<Error>`，因为那些顺序错误。它也不会匹配 `Read -> u8`，因为只有[某些泛型包装类型]可以省略，而 `Vec` 不在其中。

[某些泛型包装类型]: #wrappers-that-can-be-omitted

要搜索接受函数作为参数的函数，例如 `Iterator::all`，把嵌套签名用括号包起来，如 [`Iterator<T>, (T -> bool) -> bool`][iterator-all]。你也可以搜索特定的闭包 trait，例如 `Iterator<T>, (FnMut(T) -> bool) -> bool`，但你需要知道想要哪一个。

[iterator-all]: https://doc.rust-lang.org/std/vec/struct.Vec.html?search=Iterator<T>%2C+(T+->+bool)+->+bool&filter-crate=std

### 可以省略的包装类型 {#wrappers-that-can-be-omitted}

* References
* Box
* Rc
* Arc
* Option
* Result
* From
* Into
* Future

### 具有特殊语法的原语 {#primitives-with-special-syntax}

| 简写        | 显式名称                                    |
| ---------------- | ------------------------------------------------- |
| `&`              | `primitive:reference`                             |
| `&T`             | `primitive:reference<T>`                          |
| `&mut`           | `primitive:reference<keyword:mut>`                |
| `&mut T`         | `primitive:reference<keyword:mut, T>`             |
| `[]`             | `primitive:slice` 和/或 `primitive:array`        |
| `[T]`            | `primitive:slice<T>` 和/或 `primitive:array<T>`  |
| `()`             | `primitive:unit` 和/或 `primitive:tuple`         |
| `(T)`            | `T`                                               |
| `(T,)`           | `primitive:tuple<T>`                              |
| `!`              | `primitive:never`                                 |
| `(T, U -> V, W)` | `fn(T, U) -> (V, W)`、`Fn`、`FnMut` 和 `FnOnce` |

搜索 `[]` 时，rustdoc 会返回切片或数组的搜索结果。如果你知道想要哪一种，可以使用显式名称语法强制返回 `primitive:slice` 或 `primitive:array` 的结果。空方括号 `[]` 会匹配任何切片或数组，无论其包含什么；也可以提供项类型，例如 `[u8]` 或 `[T]`，以分别显式查找操作字节切片或泛型切片的函数。

包裹在括号中的单个类型表达式与该类型表达式相同，因为括号充当分组运算符。但如果它们为空，则会同时匹配 `unit` 和 `tuple`；如果有不止一个类型（或有尾随或前导逗号），则与 `primitive:tuple<...>` 相同。

然而，由于查询中可以省略项，`(T)` 仍会返回匹配元组的类型结果，即使它也匹配该类型本身。也就是说，`(u32)` 匹配 `(u32,)`，原因与它也匹配 `Result<u32, Error>` 完全相同。

`->` 运算符的优先级低于逗号。如果没有用括号包裹，它会分隔所搜索函数的返回值。要搜索接受函数作为参数的函数，请使用括号。

### 基于类型搜索的限制与怪癖 {#limitations-and-quirks-of-type-based-search}

基于类型的搜索仍然是一个有 bug、实验性、进行中的功能。这些限制中的大多数应在未来版本的 rustdoc 中得到解决。

  * 无法在泛型参数上书写 trait 约束。你可以直接命名 trait，如果有带该 bound 的类型参数，它会匹配，但无法精确搜索 `option<T> -> T where T: Default`（请使用 `option<Default> -> Default`）。

  * Supertraits、类型别名和 Deref 都会被忽略。搜索主要在*按书写形式*的类型签名上操作，而不是在编译器内部表示形式上操作。

  * 类型参数匹配类型参数，因此 `Option<A>` 匹配 `Option<T>`，但永远不会匹配函数签名中的具体类型。一个被当作类型命名的 trait，例如 `Option<Read>`，会匹配受该 trait 约束的类型参数，例如 `Option<T> where T: Read`，也会匹配 `dyn Trait` 和 `impl Trait`。

  * 参数位置的 `impl Trait` 被完全当作类型参数，但在返回位置它不会匹配类型参数。

  * 在复杂的基于类型的搜索中命名的任何类型，如果找不到完全匹配该名称的内容，都会被假定为类型参数。如果你想强制使用类型参数，写 `generic:T`，即使找到了匹配名称，它也会被用作类型参数。如果你知道不想要类型参数，可以通过给它不同的前缀（如 `struct:T`）强制它匹配其它内容。

  * 不支持搜索生命周期。

  * 无法基于数组长度进行搜索。

## 项过滤 {#item-filtering}

搜索界面中的名称可以加上项类型前缀，后跟冒号（例如 `mod:`），以将结果限制为仅该种类的项。另外，搜索 `println!` 会搜索名为 `println` 的宏，就像搜索 `macro:println` 一样。可用过滤器的完整列表在 <kbd>?</kbd> 帮助区域以及下方详细语法中给出。

项过滤器可用于基于名称和基于类型签名的搜索。

## 搜索查询语法 {#search-query-syntax}

```text
ident = *(ALPHA / DIGIT / "_")
path = ident *(DOUBLE-COLON ident) [BANG]
slice-like = OPEN-SQUARE-BRACKET [ nonempty-arg-list ] CLOSE-SQUARE-BRACKET
tuple-like = OPEN-PAREN [ nonempty-arg-list ] CLOSE-PAREN
borrow-ref = AMP *WS [MUT] *WS [arg]
arg = [type-filter *WS COLON *WS] (path [generics] / slice-like / tuple-like / borrow-ref)
type-sep = COMMA/WS *(COMMA/WS)
nonempty-arg-list = *(type-sep) arg *(type-sep arg) *(type-sep) [ return-args ]
generic-arg-list = *(type-sep) arg [ EQUAL arg ] *(type-sep arg [ EQUAL arg ]) *(type-sep)
normal-generics = OPEN-ANGLE-BRACKET [ generic-arg-list ] *(type-sep)
            CLOSE-ANGLE-BRACKET
fn-like-generics = OPEN-PAREN [ nonempty-arg-list ] CLOSE-PAREN [ RETURN-ARROW arg ]
generics = normal-generics / fn-like-generics
return-args = RETURN-ARROW *(type-sep) nonempty-arg-list

exact-search = [type-filter *WS COLON] [ RETURN-ARROW ] *WS QUOTE ident QUOTE [ generics ]
type-search = [ nonempty-arg-list ]

query = *WS (exact-search / type-search) *WS

type-filter = (
    "mod" /
    "externcrate" /
    "import" /
    "struct" /
    "enum" /
    "fn" /
    "type" /
    "static" /
    "trait" /
    "impl" /
    "tymethod" /
    "method" /
    "structfield" /
    "variant" /
    "macro" /
    "primitive" /
    "associatedtype" /
    "constant" /
    "associatedconstant" /
    "union" /
    "foreigntype" /
    "keyword" /
    "existential" /
    "attr" /
    "derive" /
    "traitalias" /
    "generic")

OPEN-ANGLE-BRACKET = "<"
CLOSE-ANGLE-BRACKET = ">"
OPEN-SQUARE-BRACKET = "["
CLOSE-SQUARE-BRACKET = "]"
OPEN-PAREN = "("
CLOSE-PAREN = ")"
COLON = ":"
DOUBLE-COLON = "::"
QUOTE = %x22
COMMA = ","
RETURN-ARROW = "->"
EQUAL = "="
BANG = "!"
AMP = "&"
MUT = "mut"

ALPHA = %x41-5A / %x61-7A ; A-Z / a-z
DIGIT = %x30-39
WS = %x09 / " "
```
