+++
title = "第10章 AI"
date = 2026-08-18T18:10:00+08:00
weight = 120
type = "docs"
description = "AI 指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/ai/index.html](https://microsoft.github.io/rust-guidelines/guidelines/ai/index.html)

# AI

## 面向 AI 使用来设计 (M-DESIGN-FOR-AI) {#M-DESIGN-FOR-AI}

*本条守护：让在代码库中工作的智能体发挥最大效用。*

一般而言，让 API 对人类更易用，也会让 AI 更易用。
若你遵循本书中的指南，基础就应已经打好。

Rust 强大的类型系统对智能体是一大助力：它们缺乏真正的理解，但往往可由全面的编译器检查来弥补，而 Rust 在这方面极为丰富。

话虽如此，以下几条指南对提升 Rust 中的 AI 编码效果尤为重要：

* **创建惯用的 Rust API 模式**。无论公开还是内部，你的 API 越是看起来、用起来像世界上大多数 Rust 代码，对 AI 就越有利。请遵循 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html)
以及 [库 / 用户体验](../libraries/02-ux/) 中的指南。

* **提供详尽文档**。智能体喜爱详尽的文档。为 crate 中所有模块与公开条目编写文档。
假定读者对 Rust 有扎实但非专家级的理解，并且熟悉标准库。请遵循
[C-CRATE-DOC](https://rust-lang.github.io/api-guidelines/checklist.html#c-crate-doc)、
[C-FAILURE](https://rust-lang.github.io/api-guidelines/checklist.html#c-failure)、
[C-LINK](https://rust-lang.github.io/api-guidelines/checklist.html#c-link)，以及
[M-MODULE-DOCS](../documentation/#M-MODULE-DOCS)
[M-CANONICAL-DOCS](../documentation/#M-CANONICAL-DOCS)。

* **提供详尽示例**。文档应包含可直接使用的示例，仓库中还应包含更详尽的示例。请遵循
[C-EXAMPLE](https://rust-lang.github.io/api-guidelines/checklist.html#c-example)
[C-QUESTION-MARK](https://rust-lang.github.io/api-guidelines/checklist.html#c-question-mark)。

* **使用强类型**。通过使用语义严格且文档完备的强类型，避免 [原始类型迷恋](https://refactoring.guru/smells/primitive-obsession)。请遵循
[C-NEWTYPE](https://rust-lang.github.io/api-guidelines/checklist.html#c-newtype)。

* **让 API 可测试**。设计能让客户在单元测试中检验其用法的 API。这可能涉及引入 mock、fake
或 cargo feature。AI 智能体需要能够快速迭代，以证明它们正在编写的、调用你 API 的代码能正确工作。

* **确保测试覆盖**。你自己的代码应对可观察行为有良好的测试覆盖。
这使智能体在重构时能以基本无需人工干预的方式工作。

## 项只通过一条路径可见 (M-SINGLE-ITEM-PATH) {#M-SINGLE-ITEM-PATH}

*本条守护：通往每个类型的单一、整洁路径。*

crate 内的公开项应只通过一条路径可达。例如，某个 `crate::db::Connection` 不应同时作为 `crate::Connection` 可见：

```rust
// 不推荐
pub mod db {
    pub struct Connection;
}

pub use db::Connection;
```

智能体在多轮迭代中创建或重构大型代码库时，经常违反本规则。为了「简化」任务，它们会在多条路径下再导出同一项，往往是变更前的旧路径，而不是在合适时干净地重新设计结构。

注意，本规则仅针对面向用户的项的重复。在 crate 内部，随着导出树的构建，多次看到同一项是可以接受的（且往往不可避免）：

```rust
// 可以
pub(crate) mod db {
    pub struct Connection;
}

pub use db::Connection;
```

同理，外来项的再导出不受本规则约束，但它们应遵循 [M-FOREIGN-REEXPORTS](../libraries/01-interoperability/#M-FOREIGN-REEXPORTS)。

同样，本规则也不适用于宏所需的公开但隐藏的 `_private` 模块，参见 [M-MACRO-HELPERS](../macros/#M-MACRO-HELPERS)。

## 避免元设计文档 (M-NO-META-DESIGN-DOCUMENTATION) {#M-NO-META-DESIGN-DOCUMENTATION}

*本条守护：聚焦于用户相关内容的文档。*

Crate 与模块文档不得包含仅在创建 crate 期间才有意义的元设计叙述。换言之，应当文档化的是终态，而非设计历程。

智能体经常在面向用户的文档中生成描述某次变更如何设计的章节、「我们为何选 X 而非 Y」的长文，以及设计日志。这些产物在项目进行中或许是有趣的诊断材料，但对最终用户大多毫无意义。

例如，智能体可能附加一份如下的自述，总结它声称已遵循的指南：

```text
| 规则 | 已应用 | 位置 |
| --- | :---: | --- |
| M-SHORT-NAMES | ✅ | 缩短了数据访问层与 HTTP 处理层中的方法名。 |
| M-WEASEL-WORDS | ✅ | 从整个公开 API 的类型名与字段名中移除了含糊用词。 |
| M-PUBLIC-DISPLAY | ✅ | 为所有面向用户的标识符类型与错误类型添加了 `Display` 实现。 |
| M-ASYNC-FN | ✅ | 将面向 I/O 的 API 从返回 `impl Future` 迁移为 `async fn`。 |
```

这类内容描述的是过程而非行为，并且会随时间过时。话虽如此，在项目 README 中设置 _设计原则_ 或类似章节完全合理，用于在高层次描述与最终用户相关的持久架构目标（例如，某个 crate 无分配、采用 OSI 架构，或面向 `#[no_std]` 设计）。

## 测试不断言常识性事实 (M-TAUTOLOGICAL-TESTS) {#M-TAUTOLOGICAL-TESTS}

*本条守护：能增加价值而非噪音的测试。*

单元测试应验证有意义的行为，而不是重复基础定义。

智能体经常写出这样的测试：用被测代码相同的逻辑重述期望值，或只是镜像实现的各个分支。这类测试从构造上就会通过，几乎没有价值，却抬高了后续变更的噪音底线：

```rust
const CHECKPOINTS: [u32; 4] = [0, 90, 180, 270];

#[test]
fn checkpoints_are_correct() {
    assert_eq!(CHECKPOINTS, [0, 90, 180, 270]);
}
```

若这些测试是为了满足变异测试，则应改为跳过该变异测试。

有意义的测试应检查这些常量理应满足的性质，例如它们是否等距、是否单调递增，或是否在相关逻辑中施加了某种方向。

## Rust 代码解决 Rust 问题 (M-RUST-SHAPED) {#M-RUST-SHAPED}

*本条守护：惯用代码。*

在（自动）将 C#、Java、C++ 或类似代码移植到 Rust 时，不得一对一地复制技术构造。

明智的做法是将领域方面与语言方面分开。领域方面解决业务问题。计算质数的算法或处理客户表的逻辑，在语言之间翻译时可以（也应当）以相同方式工作。

然而，许多模式是为解决其源自的生态系统所特有的问题而存在的。Rust 生态系统有其自身的问题，需要用适合 Rust 的惯用法来应对。这些包括

- 错误处理，
- 任务与线程的管理，
- 组件抽象及其生命周期，
- 参数的所有权，
- 「面向对象」编程的缺席，
- 接口与 trait 之间的结构差异，
- 以及许多其他方面。

有些语言构造根本无法翻译（例如，与 C# 相比，Rust 没有任何有意义的反射），另一些则看似相似，可能数月后才出问题（例如 statics，参见 [M-AVOID-STATICS](../libraries/03-resilience/#M-AVOID-STATICS)）。

经验法则是：就业务功能而言，结构体及其方法可以有大致相似的名称、流程、输入与输出。然而，Rust 与 { C#、Java、Python、... } 实现之间任何显著的技术相似性，都表明存在更深的架构问题；`throw_if_null()` 永远说不通。
