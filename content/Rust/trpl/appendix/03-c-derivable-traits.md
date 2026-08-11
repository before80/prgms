+++
title = "附录C 可派生的 Trait"
date = 2026-08-05T08:44:00+08:00
weight = 107
type = "docs"
description = "标准库中可用 derive 实现的特征参考"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# C - 可派生的 Trait {#c-trait}


> 原文链接: [https://doc.rust-lang.org/stable/book/appendix-03-derivable-traits.html](https://doc.rust-lang.org/stable/book/appendix-03-derivable-traits.html)


## 附录 C：可派生的特征（Trait）

　　本书多处讨论过 `derive` 属性，你可以把它用在结构体或枚举定义上。`derive` 属性会生成代码，为你用 `derive` 语法标注的类型实现某个带有默认实现的特征。

　　本附录提供标准库中所有可与 `derive` 一起使用的特征的参考。每一节都会说明：

- 派生该特征会启用哪些运算符与方法
- `derive` 提供的特征实现做了什么
- 实现该特征对类型意味着什么
- 在哪些条件下允许或不允许实现该特征
- 需要该特征的操作示例

　　若你想要的行为与 `derive` 属性提供的不同，请查阅各特征的[标准库文档](https://doc.rust-lang.org/stable/std/)，了解如何手动实现。

　　这里列出的特征，是标准库中唯一定义了、并能通过 `derive` 在你的类型上实现的那些。标准库中的其他特征没有合理的默认行为，因此要由你按目标以合理方式自行实现。

　　无法派生的特征的一个例子是 `Display`，它负责面向最终用户的格式化。你应始终考虑如何以合适方式向最终用户展示某个类型。类型的哪些部分应允许最终用户看到？哪些部分与他们相关？哪种数据格式对他们最有用？Rust 编译器没有这些洞察，因此无法为你提供合适的默认行为。

　　本附录提供的可派生特征列表并不完备：库可以为自己的特征实现 `derive`，因此你能用 `derive` 的特征列表实际上是开放的。实现 `derive` 涉及过程宏，见第 20 章[「自定义 `derive` 宏」][custom-derive-macros]一节。

### 面向程序员输出的 `Debug`

　　`Debug` 特征启用格式字符串中的调试格式化，做法是在 `{}` 占位符中加入 `:?`。

　　`Debug` 让你能为调试目的打印某个类型的实例，以便你和其他使用该类型的程序员能在程序执行的某个时间点检查实例。

　　例如，使用 `assert_eq!` 宏就需要 `Debug`。若相等断言失败，该宏会打印作为参数给出的实例的值，好让程序员看出两个实例为何不相等。

### 用于相等比较的 `PartialEq` 与 `Eq`

　　`PartialEq` 特征让你可以比较某个类型的实例以检查是否相等，并启用 `==` 与 `!=` 运算符。

　　派生 `PartialEq` 会实现 `eq` 方法。在结构体上派生时，仅当*所有*字段都相等时两个实例才相等；*任一*字段不相等则实例不相等。在枚举上派生时，每个变体与自身相等，与其他变体不相等。

　　例如，使用需要比较两个实例是否相等的 `assert_eq!` 宏时就需要 `PartialEq`。

　　`Eq` 特征没有方法。它的目的是表明：对被标注类型的每一个值，该值都与自身相等。`Eq` 只能用于同时也实现了 `PartialEq` 的类型，但并非所有实现了 `PartialEq` 的类型都能实现 `Eq`。一个例子是浮点数类型：浮点数的实现规定，两个非数（`NaN`）值彼此不相等。

　　需要 `Eq` 的一个例子是 `HashMap<K, V>` 中的键，以便 `HashMap<K, V>` 能判断两个键是否相同。

### 用于排序比较的 `PartialOrd` 与 `Ord`

　　`PartialOrd` 特征让你可以为排序目的比较某个类型的实例。实现了 `PartialOrd` 的类型可以与 `<`、`>`、`<=` 和 `>=` 运算符一起使用。你只能把 `PartialOrd` 用于同时也实现了 `PartialEq` 的类型。

　　派生 `PartialOrd` 会实现 `partial_cmp` 方法，它返回 `Option<Ordering>`；当给定值无法产生排序时为 `None`。即使该类型的大多数值可以比较，也可能有无法产生排序的值，例如浮点值 `NaN`。用任意浮点数与 `NaN` 浮点值调用 `partial_cmp` 都会返回 `None`。

　　在结构体上派生时，`PartialOrd` 按结构体定义中字段出现的顺序，逐字段比较两个实例的值。在枚举上派生时，枚举定义中声明得更靠前的变体被视为小于声明得更靠后的变体。

　　例如，`rand` crate 中根据区间表达式生成随机值的 `gen_range` 方法就需要 `PartialOrd`。

　　`Ord` 特征让你知道：对被标注类型的任意两个值，都存在有效的排序。`Ord` 实现 `cmp` 方法，它返回 `Ordering` 而不是 `Option<Ordering>`，因为始终可能得到有效排序。你只能把 `Ord` 用于同时也实现了 `PartialOrd` 和 `Eq` 的类型（而 `Eq` 又需要 `PartialEq`）。在结构体和枚举上派生时，`cmp` 的行为与为 `PartialOrd` 派生的 `partial_cmp` 实现相同。

　　需要 `Ord` 的一个例子是把值存入 `BTreeSet<T>`——一种按值的排序顺序存储数据的数据结构。

### 用于复制值的 `Clone` 与 `Copy`

　　`Clone` 特征让你可以显式创建值的深拷贝，复制过程可能涉及运行任意代码以及复制堆数据。关于 `Clone` 的更多信息，见第 4 章[「变量与数据交互：Clone」][variables-and-data-interacting-with-clone]一节。

　　派生 `Clone` 会实现 `clone` 方法；当为整个类型实现时，会对类型的每个部分调用 `clone`。这意味着类型中的所有字段或值也必须实现 `Clone`，才能派生 `Clone`。

　　需要 `Clone` 的一个例子是对切片调用 `to_vec` 方法。切片并不拥有它所包含的类型实例，但从 `to_vec` 返回的向量需要拥有自己的实例，因此 `to_vec` 会对每一项调用 `clone`。于是，切片中存储的类型必须实现 `Clone`。

　　`Copy` 特征让你只需复制存放在栈上的位就能复制一个值；不需要任意代码。关于 `Copy` 的更多信息，见第 4 章[「只在栈上的数据：Copy」][stack-only-data-copy]一节。

　　`Copy` 特征不定义任何方法，以防程序员重载这些方法并破坏「不会运行任意代码」的假定。这样，所有程序员都可以假定复制一个值会非常快。

　　只要类型的各个部分都实现了 `Copy`，就可以派生 `Copy`。实现了 `Copy` 的类型也必须实现 `Clone`，因为实现了 `Copy` 的类型有一个平凡的 `Clone` 实现，完成的任务与 `Copy` 相同。

　　很少有地方*硬性要求* `Copy`；实现了 `Copy` 的类型可以使用优化，意味着你不必调用 `clone`，代码也更简洁。

　　凡是用 `Copy` 能做的事，用 `Clone` 也能做，但代码可能更慢，或必须在各处使用 `clone`。

### 用于把值映射到固定大小值的 `Hash`

　　`Hash` 特征让你能取任意大小类型的一个实例，并用哈希函数把它映射为固定大小的值。派生 `Hash` 会实现 `hash` 方法。派生的 `hash` 实现会组合对类型各个部分调用 `hash` 的结果，这意味着所有字段或值也必须实现 `Hash`，才能派生 `Hash`。

　　需要 `Hash` 的一个例子是在 `HashMap<K, V>` 中存储键，以便高效地存储数据。

### 用于默认值的 `Default`

　　`Default` 特征让你能为类型创建默认值。派生 `Default` 会实现 `default` 函数。派生的 `default` 实现对类型的每个部分调用 `default`，这意味着类型中的所有字段或值也必须实现 `Default`，才能派生 `Default`。

　　`Default::default` 函数常与第 5 章[「用结构体更新语法从其他实例创建实例」][creating-instances-from-other-instances-with-struct-update-syntax]一节讨论的结构体更新语法一起使用。你可以自定义结构体的少数字段，然后用 `..Default::default()` 为其余字段设置并使用默认值。

　　例如，对 `Option<T>` 实例使用方法 `unwrap_or_default` 时就需要 `Default`。若 `Option<T>` 为 `None`，方法 `unwrap_or_default` 会返回存储在 `Option<T>` 中的类型 `T` 的 `Default::default` 结果。

[creating-instances-from-other-instances-with-struct-update-syntax]: ../../structs/01-defining-structs/#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ../../understanding-ownership/01-what-is-ownership/#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ../../understanding-ownership/01-what-is-ownership/#variables-and-data-interacting-with-clone
[custom-derive-macros]: ../../advanced-features/05-macros/#custom-derive-macros
