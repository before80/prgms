+++
title = "07-开发"
date = 2026-08-22T18:00:00+08:00
weight = 70
type = "docs"
description = "参与 Clippy 开发入门"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 开发 {#development}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/index.html](https://doc.rust-lang.org/nightly/clippy/development/index.html)


你好，Rustacean！如果你来到这里，多半是想通过贡献让 Clippy 变得更好。若是如此，欢迎加入本项目！

> _注意：_ 若你只是想使用 Clippy，从这里往后的内容对你没有帮助，请回到前面章节。

## 入门

若这是你第一次为 Clippy 做贡献，请先阅读[基础文档](basics.md)。其中会说明如何获取源码、如何编译与测试。

## 初学者延伸阅读

若读者从未上过编译器与解释器相关课程，可能会疑惑为何 AST 层面只处理语言的语法；也可能不理解词法分析、语法分析、AST 等术语的含义。

本文档绝非编译器或语言设计的速成课。与 Rust 相关的细节，[Rustc 开发指南][rustc_dev_guide] 是更好的阅读选择。

[语法与 AST][ast] 一章与 [高级 IR（HIR）][hir] 一章，是理解本章所提概念的良好入门。

部分读者也可能觉得 Robert Nystrom 的 _Crafting Interpreters_ 中[导论章节][map_of_territory]有助于在回到 Rustc 指南之前，对编译型与解释型语言建立概览。

## 编写代码

完成基础环境搭建后，就可以开始动手了。

[添加 lint](adding_lints.md) 一章会带你走完向 Clippy 添加新 lint 的全过程。即便你只是想修复某个 lint，这一章也值得一读，因为它还涵盖如何测试 lint，并概述整体图景。

若要添加新 lint 或修改现有 lint（除 bug 修复外），也建议快速阅读 [Clippy 1.0 RFC][clippy_rfc] 中的[稳定性保证][rfc_stability]与 [lint 类别][rfc_lint_cats] 部分。lint 类别在[本书前文](../lints.md)也有说明。

> _注意：_ 关于为 Clippy 做贡献的一些更高层事项，仍写在 [`CONTRIBUTING.md`] 中。其中部分内容会逐步迁入本书，例如：
> - 寻找可修复的问题
> - IDE 配置
> - Clippy 工作原理的高层概览
> - 分诊流程

[ast]: https://rustc-dev-guide.rust-lang.org/syntax-intro.html
[hir]: https://rustc-dev-guide.rust-lang.org/hir.html
[rustc_dev_guide]: https://rustc-dev-guide.rust-lang.org/
[map_of_territory]: https://craftinginterpreters.com/a-map-of-the-territory.html
[clippy_rfc]: https://github.com/rust-lang/rfcs/blob/master/text/2476-clippy-uno.md
[rfc_stability]: https://github.com/rust-lang/rfcs/blob/master/text/2476-clippy-uno.md#stability-guarantees
[rfc_lint_cats]: https://github.com/rust-lang/rfcs/blob/master/text/2476-clippy-uno.md#lint-audit-and-categories
[`CONTRIBUTING.md`]: https://github.com/rust-lang/rust-clippy/blob/master/CONTRIBUTING.md
