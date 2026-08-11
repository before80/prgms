+++
title = "07-高级特性"
date = 2026-08-01T07:35:00+08:00
weight = 70
type = "docs"
description = "rustdoc 的高级功能"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 高级特性 {#advanced-features}


> 原文链接: [https://doc.rust-lang.org/rustdoc/advanced-features.html](https://doc.rust-lang.org/rustdoc/advanced-features.html)


本页列出的特性不属于其他主要分类。

## `#[cfg(doc)]`：文档化平台相关或特性相关信息 {#cfgdoc-documenting-platform-specific-or-feature-specific-information}

对于条件编译，Rustdoc 对你的 crate 的处理方式与编译器相同。只有宿主目标上的内容可用（或使用给定的 `--target` 时该目标上的内容），其余内容会从 crate 中被“过滤掉”。若你的 crate 在不同目标上提供不同内容，而你又希望文档反映所提供的全部项，这就会带来问题。

若希望无论以哪个平台为目标，某项都能被 Rustdoc 看到，可以对其应用 `#[cfg(doc)]`。Rustdoc 在构建文档时会设置该标志，因此使用该标志的内容会出现在生成的文档中。若该项还有其他 `#[cfg]` 过滤器，可以写成类似 `#[cfg(any(windows, doc))]`。这样在 Windows 上正常构建时会保留该项，在任意平台生成文档时也会保留。

请注意，此 `cfg` **不会**传给文档测试（doctest）。

示例：

```rust
/// 仅能在 Windows 上使用的 Token 结构体。
#[cfg(any(windows, doc))]
pub struct WindowsToken;
/// 仅能在 Unix 上使用的 Token 结构体。
#[cfg(any(unix, doc))]
pub struct UnixToken;
```

此处，各自的 token 只能由依赖 crate 在对应平台上使用，但两者都会出现在文档中。

### 平台特定文档之间的交互 {#interactions-between-platform-specific-docs}

Rustdoc 并没有魔法手段能“仿佛”为每个平台各跑一遍来编译文档（这种魔法棒曾被称为 [「rustdoc 的圣杯」][#1998]）。相反，它会*一次性*看到你的全部代码，就像你向 Rust 编译器传入 `--cfg doc` 时那样。主要区别在于 rustdoc 不会运行全部编译器 pass，因此某些无效代码不会报错。

[#1998]: https://github.com/rust-lang/rust/issues/1998

## 为文档搜索中的项添加别名 {#add-aliases-for-an-item-in-documentation-search}

此特性允许你通过 `doc(alias)` 属性，为项在 `rustdoc` 搜索中添加一个或多个别名。例如：

```rust,no_run
#[doc(alias = "x")]
#[doc(alias = "big")]
pub struct BigX;
```

之后在 `rustdoc` 搜索中查找时，若输入 “x” 或 “big”，搜索会优先显示 `BigX` 结构体。

文档别名名称有一些限制：不能包含引号（`'`、`"`）或大多数空白字符。若 ASCII 空格不出现在别名的首尾，则允许使用。

也可以用列表一次添加多个别名：

```rust,no_run
#[doc(alias("x", "big"))]
pub struct BigX;
```

## 自定义搜索引擎 {#custom-search-engines}

若你经常查阅在线 Rust 文档，可能会喜欢使用自定义搜索引擎。这样可以直接通过浏览器地址栏搜索某个 `rustdoc` 网站。
多数浏览器支持该功能：定义一个包含 `%s` 的 URL 模板，搜索词会替换 `%s`。例如，标准库可以使用如下模板：

```text
https://doc.rust-lang.org/stable/std/?search=%s
```

注意：这会跳转到列出所有匹配项的结果页。若希望立即跳转到第一个结果（通常也是最佳匹配），请改用：

```text
https://doc.rust-lang.org/stable/std/?search=%s&go_to_first=true
```

该 URL 增加了 `go_to_first=true` 查询参数，可追加到任意 `rustdoc` 搜索 URL，以自动跳转到第一个结果。

## `#[repr(...)]`：文档化类型的表示 {#repr-documenting-the-representation-of-a-type}

一般而言，仅当给定类型的所有变体都没有 `#[doc(hidden)]`，且所有字段都是公开的且没有 `#[doc(hidden)]` 时，rustdoc 才会显示该类型的表示（representation）——否则它很可能不应被视为公共 ABI 的一部分。

注意：没有办法覆盖该启发式规则、强制 rustdoc 无论如何都显示表示。

### `#[repr(transparent)]`

你可以在 [Rust 参考][repr-trans-ref] 和 [Rustonomicon][repr-trans-nomicon] 中阅读更多关于 `#[repr(transparent)]` 本身的内容。

由于仅当那个具有非平凡大小或对齐的单个字段是公开的、且文档未另行说明时，该表示才被视为公共 ABI 的一部分，rustdoc 会在且仅在以下情况显示该属性：非 1-ZST 字段公开且没有 `#[doc(hidden)]`；或者——若所有字段都是 1-ZST——至少一个字段公开且没有 `#[doc(hidden)]`。
术语 *1-ZST* 指对齐为 1 且大小为零的类型。

看上去可以用 `#[cfg_attr(not(doc), repr(transparent))]` 手动隐藏该属性，以便在非 1-ZST 字段公开时仍将表示声明为私有。
然而，由于[当前限制][cross-crate-cfg-doc]，该方法并不总是保证有效。
因此，若你希望这样做，应始终在正文中单独写明，无论是否使用 `cfg_attr`。

[repr-trans-ref]: https://doc.rust-lang.org/reference/type-layout.html#the-transparent-representation
[repr-trans-nomicon]: https://doc.rust-lang.org/nomicon/other-reprs.html#reprtransparent
[cross-crate-cfg-doc]: https://github.com/rust-lang/rust/issues/114952
