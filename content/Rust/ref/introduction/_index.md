+++
title = "引言"
date = 2026-08-18T08:45:00+08:00
weight = 2
type = "docs"
description = "引言 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/introduction.html](https://doc.rust-lang.org/reference/introduction.html)

# 引言

本书是 Rust 编程语言的主要参考手册。

> **注意**
> 本书已知的缺陷与遗漏见我们的 [GitHub issues]。若发现编译器行为与此处文字不符，请提交 issue，以便我们判断哪一方是正确的。

## Rust 发行版

Rust 每六周发布一次语言版本。
该语言的第一个稳定版本是 Rust 1.0.0，随后是 Rust 1.1.0，依此类推。
工具（`rustc`、`cargo` 等）与文档（[标准库][standard library]、本书等）随语言版本一同发布。

本书与最新 Rust 版本对应的最新版始终位于 <https://doc.rust-lang.org/reference/>。
先前版本可在 “reference” 目录前加上 Rust 版本号来访问。
例如，Rust 1.49.0 的参考手册位于 <https://doc.rust-lang.org/1.49.0/reference/>。

## 《参考手册》不是什么

本书并非语言入门读物。
假定读者已具备该语言的背景知识。
另有一本 [书][book] 可用于获得这种背景知识。

本书也不是随语言发行版附带的 [标准库][standard library] 的参考。
那些库通过从其源代码中提取文档属性来单独生成文档。
许多人们可能以为是语言特性的功能，在 Rust 中其实是库特性，因此你要找的内容可能在那里，而不在这里。

同样，本书通常也不记录作为工具的 `rustc` 或 Cargo 的具体细节。
`rustc` 有自己的 [书][rustc book]。
Cargo 有一本 [书][cargo book]，其中包含一份 [参考][cargo reference]。
仍有少数页面（如 [链接][linkage]）描述 `rustc` 的工作方式。

本书也只作为稳定版 Rust 中可用内容的参考。
正在开发的不稳定特性见 [Unstable Book]。

Rust 编译器（包括 `rustc`）会执行优化。
参考手册并不规定哪些优化被允许或禁止。
相反，请把编译后的程序看作一个黑盒。
你只能通过运行它、向其输入并观察输出来探测。
以这种方式发生的一切都必须符合参考手册所述。

## 如何使用本书

本书并不假定你按顺序阅读。
各章通常可独立阅读，但会交叉链接到它们所涉及、却未展开讨论的语言其他章节。

阅读本文档主要有两种方式。

第一种是回答某个具体问题。
若你知道哪一章能回答该问题，可在目录中跳转到那一章。
否则，可以按 `s` 或点击顶栏上的放大镜，搜索与你的问题相关的关键字。
例如，假设你想知道在 let 语句中创建的临时值何时被丢弃。
若你并不已经知道 [临时值的生命周期][lifetime of temporaries] 定义在 [表达式一章][expressions chapter]，你可以搜索 “temporary let”，第一条搜索结果就会带你到那一节。

第二种是从总体上加深对语言某一侧面的了解。
此时只需浏览目录，直到看到你想进一步了解的内容，然后开始阅读。
若某个链接看起来有意思，点进去读那一节即可。

话虽如此，阅读本书并无对错之分。用你觉得最有帮助的方式去读即可。

### 体例

与所有技术书籍一样，本书在展示信息时有若干体例。
这些体例记录于此。

* 定义术语的语句将该术语标为 *斜体*。
  每当该术语在该章之外被使用时，通常会链接到给出此定义的小节。

  *示例术语* 是正在被定义的术语的一个例子。

* 正文描述最新的稳定 edition。与先前 edition 的差异单独放在 edition 块中：

  > [!EDITION-2018]
  > 在 2018 edition 之前，行为是这样。从 2018 edition 起，行为是那样。

* 包含关于本书状态的有用信息、或指出有用但大体超出范围的信息的注释，放在 note 块中。

  > [!NOTE]
  > 这是一条示例注释。

* 示例块展示演示某条规则或指出某种有趣侧面的例子。有些示例可能含有隐藏行，将鼠标悬停或点按示例时出现的眼睛图标可用来查看。

  > [!EXAMPLE]
  > 这是一个代码示例。
  > ```rust
  > println!("hello world");
  > ```

* 展示语言中不健全行为、或语言特性之间可能令人困惑的交互的警告，放在特殊的警告框中。

  > [!WARNING]
  > 这是一条示例警告。

* 正文中的行内代码片段放在 `<code>` 标签内。

  较长的代码示例放在语法高亮框中，右上角有用于复制、执行以及显示隐藏行的控件。

  ```rust
  # // 这是隐藏行。
  fn main() {
      println!("This is a code example");
  }
  ```

  除非另有说明，所有示例均按最新 edition 编写。

* 文法与词法产生式在 [记号][Notation] 一章中描述。

r[example.rule.label]
* 规则标识符出现在每条语言规则之前，并用方括号括起。这些标识符提供了一种引用并链接到语言中某条具体规则的方式（[例如][example rule]）。规则标识符用句点分隔各段，从最一般到最具体（例如 [destructors.scope.nesting.function-body]）。在窄屏幕上，规则名会折叠显示为 `[*]`。

  可以点击规则名以链接到该规则。

  > [!WARNING]
  > 规则的组织目前仍在变动。眼下这些标识符名称在各发行版之间并不稳定，若被更改，指向这些规则的链接可能失效。我们打算在组织稳定后将其固定下来，使指向规则名的链接不会在发行版之间断裂。

* 带有关联测试的规则会在其下方包含一个 `Tests` 链接（窄屏幕上该链接为 `[T]`）。点击该链接会弹出测试列表，可再点击以查看测试。例如见 [input.encoding.utf8]。

  将规则链接到测试是一项持续进行的工作。概览见 [测试摘要](../appendices/05-test-summary/) 一章。

## 贡献

我们欢迎各种形式的贡献。

你可以通过向 [Rust 参考手册仓库][the Rust Reference repository] 提交 issue 或发送 pull request 来为本手册做贡献。
若本书没有回答你的问题，而你认为答案属于本书范围，请不要犹豫，[提交 issue][file an issue]，或在 [Zulip] 的 `t-lang/doc` 流中询问。
了解人们最常把本书用于何处，有助于我们把注意力投向把那些章节做到最好。
当然，若你看到任何错误、或并非规范性却未明确如此标明的内容，也请 [提交 issue][file an issue]。

[book]: ../book/index.html
[github issues]: https://github.com/rust-lang/reference/issues
[standard library]: std
[the Rust Reference repository]: https://github.com/rust-lang/reference/
[Unstable Book]: https://doc.rust-lang.org/nightly/unstable-book/
[cargo book]: ../cargo/index.html
[cargo reference]: ../cargo/reference/index.html
[example rule]: example.rule.label
[expressions chapter]: expressions.html
[file an issue]: https://github.com/rust-lang/reference/issues
[lifetime of temporaries]: expressions.html#temporaries
[linkage]: linkage.html
[rustc book]: ../rustc/index.html
[Notation]: notation.md
[Zulip]: https://rust-lang.zulipchat.com/#narrow/stream/237824-t-lang.2Fdoc
