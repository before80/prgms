+++
title = "03-如何阅读 rustdoc 输出"
date = 2026-08-01T07:35:00+08:00
weight = 30
type = "docs"
description = "如何阅读与使用 rustdoc 生成的文档"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 如何阅读 rustdoc 输出 {#how-to-read-rustdoc}


> 原文链接: [https://doc.rust-lang.org/rustdoc/how-to-read-rustdoc.html](https://doc.rust-lang.org/rustdoc/how-to-read-rustdoc.html)


rustdoc 的 HTML 输出包含友好且实用的导航界面，便于用户浏览并理解你的代码。
本章介绍该界面的主要功能，对文档作者和读者都是很好的起点。

## 结构 {#structure}

`rustdoc` 的输出分为三个部分。
每个页面的左侧是快速导航栏，显示与当前条目相关的上下文信息。
页面其余部分由顶部的搜索界面，以及其下方当前项的文档占据。

## 项文档 {#the-item-documentation}

屏幕的大部分区域被当前查看项的文档正文占据。
顶部有一些一目了然的信息与控件：

- 项的类型和名称，例如 “Struct `std::time::Duration`”，
- 一个将项路径复制到剪贴板的按钮（剪贴板图标），
- 一个折叠或展开该项顶层文档的按钮（`[+]` 或 `[-]`），
- 指向源代码的链接（`[src]`），前提是已[配置](../how-to-write-documentation/02-the-doc-attribute/#html_no_source)，且源码存在（如果文档是用 `cargo doc --no-deps` 创建的，源码可能不可用），
- 以及该项变为稳定的版本（如果它是标准库中的稳定项）。

其下是该项的主要文档，在适当时包括定义或函数签名，然后是 Rust 类型的字段或变体列表。最后，页面列出关联函数与 trait 实现，包括 `rustdoc` 已知的自动实现和 blanket 实现。

### 各节 {#sections}

<!-- FIXME: Implementations -->
<!-- FIXME: Trait Implementations -->
<!-- FIXME: Implementors -->
<!-- FIXME: Auto Trait Implementations -->

#### 别名类型 {#aliased-type}

类型别名在编译时会展开为其[别名类型（aliased type）](https://doc.rust-lang.org/reference/items/type-aliases.html)。
这可能涉及用类型别名定义所提供的类型，替换目标类型中的部分或全部类型参数。别名类型一节会显示该展开的结果，包括可能依赖于这些替换的公有字段或变体的类型。

### 导航 {#navigation}

本文档中的小标题、变体、字段以及许多其它内容都是锚点，可以点击并深度链接，这是精确沟通你所谈论内容的好方法。排版字符 “§” 会在悬停或获得键盘焦点时出现在带有锚点的行旁边。

## 导航栏 {#the-navigation-bar}

例如，在查看 crate 根的文档时，它会显示文档包中所有已文档化的 crate，以及指向当前 crate 可用的模块、结构体、trait、函数和宏的快速链接。顶部会显示[可配置的 logo](../how-to-write-documentation/02-the-doc-attribute/#html_logo_url)，以及当前 crate 的名称和版本，或当前正在显示文档的项。

## 主题选择器与搜索界面 {#the-theme-picker-and-search-interface}

在启用了 JavaScript 的浏览器中查看 `rustdoc` 的输出时，页面顶部会出现一个动态界面，由[搜索]界面、帮助屏幕和[选项]组成。

[选项]: 01-in-doc-settings/
[搜索]: 02-search/

也支持路径：你可以查找 `Vec::new` 或 `Option::Some`，甚至 `module::module_child::another_child::struct::field`。空白字符被视为与 `::` 相同，因此如果你写 `Vec    new`，它会被视为与 `Vec::new` 相同。

### 快捷键 {#shortcuts}

在页面其它位置获得焦点时按 `S` 会把焦点移到搜索栏，按 `?` 会显示帮助屏幕，其中包含所有这些快捷键以及更多内容。

当搜索结果获得焦点时，左右箭头在标签页之间移动，上下箭头在结果之间移动。按 Enter 或 Return 键会打开高亮的结果。

在查看某个项的文档时，加号和减号键会展开和折叠文档中的所有章节。

## 本章其它页面 {#related-pages}

- [文档内设置](01-in-doc-settings/)
- [搜索](02-search/)
