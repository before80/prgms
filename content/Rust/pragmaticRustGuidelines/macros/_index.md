+++
title = "第3章 宏"
date = 2026-08-18T18:10:00+08:00
weight = 50
type = "docs"
description = "宏指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/macros/index.html](https://microsoft.github.io/rust-guidelines/guidelines/macros/index.html)

# 宏

## 宏是最后手段 (M-MACRO-LAST-RESORT) {#M-MACRO-LAST-RESORT}

*本条守护：最小复杂度。*

只有在没有其他可行方案时才应使用宏，可对照这句箴言：

> 正如 @littlecalculist 一直对我说的：「宏是在你把语言用尽时才用的」。如果你还有语言可用——而 Rust 给了你很多语言——就先用语言。
>
> @pcwalton

宏很强大，但有若干缺点。它们

- 像魔法，往往无法预知它们做什么、或如何做到，
- 在本身不怎么依赖宏的项目里，会不成比例地增加编译时间，
- 可能在 edition 边界引发细微破坏，因为 Rust 的语法与语义可能发生变化。

反直觉的是，宏展开结果的结构越复杂，当初就越不该用宏来做这件事。理想的宏会让用户觉得：「_我完全知道这会生成什么，只是不想亲手写那么多_」。

## 优先示例宏而非过程宏 (M-EXAMPLE-OVER-PROC) {#M-EXAMPLE-OVER-PROC}

*本条守护：便于检查宏，并加快编译。*

当「示例宏」（macro by example）能胜任时，应优先于过程宏。

过程宏更强大，但其展开结果不易检查。在不需要这种灵活性时，简单的「示例宏」是更好的选择。

```rust
// 不好：属性宏需要过程宏机制，在某些 IDE 中
// 难以检查，且此处并不需要。
#[make_new_id]
struct MyId;

// 好：更易编写、维护与检查，编译更快。
make_new_id!(MyId);
```

## 宏不谎报签名 (M-MACROS-DONT-LIE) {#M-MACROS-DONT-LIE}

*本条守护：对用户与 LLM 清晰。*

宏不得（让用户）误报签名或项的形态。

宏可以任意改写 token 流。它们可以把结构体变成枚举、把 trait 变成函数，或做任何想象得到的变换。然而它们不该这么做，因为结果代码会极度令人困惑，几乎无法预测或推理。

此外，宏不得

- 明显改变数据类型的本质（例如结构体变枚举等），
- 改动函数签名，
- 改变项的 `async` 性，
- 做任何实质上让「_写下的内容_」与「_实际发生的事_」脱节的事。

```rust
// 不好：额外增加参数并把函数标为 `async`。从阅读代码
// 根本无法预测。
#[magic_transform]
fn foo() { }

foo(token).await
```

## 宏假定位于主 crate (M-MACRO-MAIN-CRATE) {#M-MACRO-MAIN-CRATE}

*本条守护：简单的宏逻辑。*

过程宏可以（也应）假定通过其主 crate 使用，并发出指向该主 crate 的路径。

对包含过程宏的 crate，出于技术原因，常见做法是拆成 3 个：

- `foo` — 主 crate，从 `foo_proc` 再导出宏，并附带额外 trait 或类型，
- `foo_proc` — 门面，以 `proc-macro = true` 从 `foo_proc_impl` 再导出宏，
- `foo_proc_impl` — 实际宏实现与单元测试。

有时还会牵涉更多 crate。作者可能想让 `foo`、`foo_proc` 及其兄弟都能单独工作，于是弄出复杂的再导出层级或依赖第三方辅助工具。实际上，鉴于生态先例大多本来就不支持这些用法，那点最小的 UX 收益通常不值得换来额外复杂度（或编译时间开销）。

这也意味着你不应试图支持把你的 crate 以不同名字导入的用例。

## 第三方项来自隐藏的 `_private` 模块 (M-MACRO-HELPERS) {#M-MACRO-HELPERS}

*本条守护：可预期的编译。*

当宏展开需要引用第三方项时，宿主 crate 应从隐藏模块再导出它们，宏应通过该模块发出完全限定路径，而不是指望用户的 crate 直接依赖那个第三方 crate。

例如，需要 `bar` trait 的 crate `foo` 会这样做：

```rust
#[doc(hidden)]
pub mod _private {
    pub use ::bar::Bar;
}

pub use foo_proc::my_macro;
```

然后 `my_macro!` 的实现在其发出的代码中依赖该存在：

```rust
impl ::foo::_private::Bar for MyType { ... }
```

## 过程宏应有独立的 impl crate（含测试） (M-PROC-IMPL) {#M-PROC-IMPL}

*本条守护：过程宏可充分测试。*

过程宏应是某个 `foo_proc` crate 里的薄垫片，委托给单独的普通库 crate（通常叫 `foo_proc_impl`），后者包含实际的 token 流变换逻辑及其测试。

由于过程宏 crate 比较特殊，从 `foo_proc` 测试它们通常需要为单元测试与快照测试做变通。相反，可考虑使用 `foo_proc_impl` crate：

```rust
use proc_macro2::TokenStream;

pub fn my_macro(attr: TokenStream, item: TokenStream) -> TokenStream { ... }
```

它们可以配备常规的 [insta](https://insta.rs/) 或类似快照测试，再通过 `foo_proc` crate 导出为真正的过程宏，例如：

```rust
#[proc_macro_attribute]
pub fn my_macro(attr: TokenStream, item: TokenStream) -> TokenStream {
    foo_proc_impl::my_macro(attr.into(), item.into()).into()
}
```

然后从核心 crate 再导出这些宏：

```rust
pub use foo_proc::my_macro;
```

在核心 crate 内部，我们也建议用 [trybuild](https://docs.rs/trybuild/latest/trybuild/) 增加带负面示例的 UI 测试，以确保错误消息一致。

## 过程宏不产生隐含或隐藏项 (M-PROC-IMPLIED-ITEMS) {#M-PROC-IMPLIED-ITEMS}

*本条守护：清晰的错误，以及正确的卫生与可见性。*

宏不应自行定义「魔法」类型，尤其不应定义公开类型，或那些不依赖命名空间技巧的类型。

有些宏想要定义类型，例如

```rust
#[my_macro]
struct UserType;

// 会展开为

struct UserType;
struct ExtraType; 
impl UserType {
    fn foo() -> ExtraType { ... };
}
```

这几乎总是坏主意，原因包括：

- 可能与同一模块中用户已定义的类型冲突，
- 若实现草率，可能与同宏的其他展开冲突，
- 可能与用户的命名约定冲突，
- 在源码层面不可见，容易忘记在需要处再导出。

虽然用户多少能绕过这些限制，但这些都是用户必须应付的「纸割伤」，可能在数月后重构本不相关的代码时才撞上。

注意本规则有一个例外，其 UX 通常可接受，即 [namespaces](https://doc.rust-lang.org/reference/names/namespaces.html)（命名空间）的重载用法，由 Rocket 等 crate 推广开来：

```rust
#[my_macro]
fn foo() { ... }

// 会展开为

fn foo() { ... }

struct foo;
impl SomeTrait for foo { ... }
```

这里引入了与函数 `foo` 同名的新类型 `foo`。由于 Rust 的命名空间规则，它们可以共存，并随父项自动再导出；又因 [Rust 的大小写规则 (C-CASE)](https://rust-lang.github.io/api-guidelines/naming.html#casing-conforms-to-rfc-430-c-case)，它们极不可能与用户定义的类型冲突。不过它们仍不宜作为漂亮的_公开_类型，因此主要用于根 crate 内定义请求处理器或 FFI 函数。

> ### 💡 命名空间 ≠ 模块
>
> Rust 中的命名空间与其他语言中的命名空间毫无关系。C# 中的命名空间大致相当于 Rust 中的模块。Rust 中的命名空间
是名字的一种冷门属性（例如 `fn foo`、`struct Bar {}`、`moo!`），决定它在模块内落在哪个「命名桶」里。
