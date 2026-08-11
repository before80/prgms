+++
title = "04-如何编写文档"
date = 2026-08-01T07:35:00+08:00
weight = 40
type = "docs"
description = "如何为 Rust 项目编写高质量文档"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 如何编写文档 {#how-to-write-documentation}


> 原文链接: [https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html)


写好文档并不自然。目标之间往往相互冲突，因此写好文档很难：既需要主题上的专长，又要站在新手视角来写。文档因此常常略过实现细节，或留下读者未解的疑问。

Rust 文档有几条原则，可以引导任何人完成库文档的编写，让大家都有充分机会使用这些代码。

本章不仅讲如何写文档，更具体地讲如何写出**好**文档。尽量写清楚、写完整非常重要。经验法则是：为 crate 写的文档越多越好。若某个项是公开的，就应当有文档。

## 入门 {#getting-started}

为 crate 写文档应从首页文档开始。例如，[`hashbrown`] 的 crate 级文档概括了该 crate 的作用，提供了解释技术细节的链接，并说明为何你会想使用它。

介绍完 crate 之后，首页应给出在实际场景中如何使用该 crate 的示例。示例要紧扣库的职责，但不要偷工减料，以便用户可以直接复制粘贴上手。

[`futures`] 用行内注释逐行解释使用 [`Future`] 的复杂之处，因为读者第一次接触 Rust 的 [`Future`] 可能就是这个示例。

[`backtrace`] 的文档走完整流程：说明对 `Cargo.toml` 的修改、向编译器传入的命令行参数，并给出一个真实场景中的简短 backtrace 示例。

最终，首页可以成为如何使用 crate 的全面参考，例如 [`regex`]。该首页列出全部要求、展示边界情况，并提供实用示例；接着说明如何使用正则表达式，最后以 crate 特性收尾。

不必担心拿刚起步的 crate 去和更成熟的 crate 比较。要把文档打磨得更好，就循序渐进：先写引言、示例和特性。罗马不是一天建成的！

`lib.rs` 开头的几行会构成首页，其约定与其余 rustdoc 不同：行应以 `//!` 开头，表示模块级或 crate 级文档。下面是一个快速对比示例：

```rust,no_run
//! 快速易用的队列抽象。
//!
//! 提供对队列的抽象。使用该抽象时有这些优点：
//! - 快速
//! - [`Easy`]
//!
//! [`Easy`]: http://thatwaseasy.example.com

/// 该模块让事情变得容易。
pub mod easy {

    /// 使用抽象函数来做这件具体的事。
    pub fn abstraction() {}

}
```

理想情况下，文档的第一行是一句不含高度技术细节的话，但能清楚说明该 crate 在 Rust 生态中的位置。用户读完这行后应能判断该 crate 是否符合自己的用例。

## 为组件编写文档 {#documenting-components}

无论是模块、结构体、函数还是宏：所有公开 API 都应有文档。很少有人会抱怨文档太多！

建议每个项的文档遵循如下基本结构：

```text
[简短一句说明它是什么]

[更详细的解释]

[至少一个用户可复制粘贴试用的代码示例]

[如有必要，再给出更高级的说明]
```

写文档时按这个基本结构即可；你或许觉得代码示例微不足道，但示例其实非常重要：它们能帮助用户理解某个项是什么、如何使用、以及为何存在。

来看出自[标准库][standard library]的例子，查看 [`std::env::args()`][env::args] 函数：

``````markdown
Returns the arguments which this program was started with (normally passed
via the command line).

The first element is traditionally the path of the executable, but it can be
set to arbitrary text, and may not even exist. This means this property should
not be relied upon for security purposes.

On Unix systems shell usually expands unquoted arguments with glob patterns
(such as `*` and `?`). On Windows this is not done, and such arguments are
passed as-is.

# Panics

The returned iterator will panic during iteration if any argument to the
process is not valid unicode. If this is not desired,
use the [`args_os`] function instead.

# Examples

```
use std::env;

// 将每个参数打印在单独一行
for argument in env::args() {
    println!("{argument}");
}
```

[`args_os`]: ./fn.args_os.html
``````

第一个空行之前的内容会在搜索结果与模块概览中复用，用于描述该组件。例如上面的 `std::env::args()` 会出现在 [`std::env`] 模块文档中。良好实践是把摘要控制在一行：简洁是好文档的目标之一。

类型系统已经很好地定义了函数传入和返回的类型，因此显式写进文档没有额外收益，尤其是 `rustdoc` 会为函数签名中的所有类型添加超链接。

在上面的例子中，「Panics」小节说明代码何时可能突然退出，有助于读者避免触发 panic。只要已知代码中可能触及边界情况，就建议写 panic 小节。

可以看到，它遵循上文结构：先用短句说明函数做什么，再提供更多信息，最后给出代码示例。

## Markdown {#markdown}

`rustdoc` 使用 [CommonMark Markdown 规范][CommonMark Markdown specification]。你或许想看看他们的网站了解能做什么：

 - [CommonMark 快速参考][CommonMark quick reference]
 - [当前规范][current spec]

除标准 CommonMark 语法外，`rustdoc` 还支持若干扩展：

### 删除线 {#strikethrough}

在文本两侧各包一层或两层波浪号，即可渲染穿过文字中心的横线：

```text
An example of ~~strikethrough text~~. You can also use ~single tildes~.
```

该示例会渲染为：

> An example of ~~strikethrough text~~. You can also use ~single tildes~.

这遵循 [GitHub 删除线扩展][strikethrough]。

### 脚注 {#footnotes}

脚注会在正文中生成带编号的小链接，点击后跳到该项底部的脚注文本。脚注标签的写法类似链接引用，但前面带脱字符。脚注正文的写法类似链接引用定义，文本跟在标签后面。示例：

```text
This is an example of a footnote[^note].

[^note]: This text is the contents of the footnote, which will be rendered
    towards the bottom.
```

该示例会渲染为：

> This is an example of a footnote[^note].
>
> [^note]: This text is the contents of the footnote, which will be rendered
>     towards the bottom.

脚注会按书写顺序自动编号。

### 表格 {#tables}

可用竖线和横线画出表格的行与列，它们会转成形状匹配的 HTML 表格。示例：

```text
| Header1 | Header2 |
|---------|---------|
| abc     | def     |
```

该示例渲染大致如下：

> | Header1 | Header2 |
> |---------|---------|
> | abc     | def     |

关于确切支持的语法，详见 [GitHub 表格扩展][tables] 规范。

### 任务列表 {#task-lists}

任务列表可用作已完成事项的清单。示例：

```md
- [x] Complete task
- [ ] Incomplete task
```

会渲染为：

> - [x] Complete task
> - [ ] Incomplete task

更多细节见 [任务列表扩展][task list extension] 规范。

### 智能标点 {#smart-punctuation}

一些 ASCII 标点序列会自动变成漂亮的 Unicode 字符：

| ASCII 序列 | Unicode |
|----------------|---------|
| `--`           | –       |
| `---`          | —       |
| `...`          | …       |
| `"`            | “ 或 ”，取决于上下文 |
| `'`            | ‘ 或 ’，取决于上下文 |

因此不必手动输入这些 Unicode 字符！

### 添加警告块 {#adding-a-warning-block}

若希望警告或类似说明在文档中更醒目，可以这样包裹：

```md
/// 文档
///
/// <div class="warning">重要警告！</div>
///
/// 更多文档
```

请注意：若要在 HTML 标签中放入 Markdown 并让其被解析，需要在 HTML 标签与 Markdown 内容之间留空行。例如要使用链接：

```md
/// 文档
///
/// <div class="warning">
///
/// 前往[此链接](https://rust-lang.org)！
///
/// </div>
///
/// 更多文档
```

[`backtrace`]: https://docs.rs/backtrace/0.3.50/backtrace/
[CommonMark Markdown specification]: https://commonmark.org/
[CommonMark quick reference]: https://commonmark.org/help/
[env::args]: https://doc.rust-lang.org/stable/std/env/fn.args.html
[`Future`]: https://doc.rust-lang.org/std/future/trait.Future.html
[`futures`]: https://docs.rs/futures/0.3.5/futures/
[`hashbrown`]: https://docs.rs/hashbrown/0.8.2/hashbrown/
[`regex`]: https://docs.rs/regex/1.3.9/regex/
[standard library]: https://doc.rust-lang.org/stable/std/index.html
[current spec]: https://spec.commonmark.org/current/
[`std::env`]: https://doc.rust-lang.org/stable/std/env/index.html#functions
[strikethrough]: https://github.github.com/gfm/#strikethrough-extension-
[tables]: https://github.github.com/gfm/#tables-extension-
[task list extension]: https://github.github.com/gfm/#task-list-items-extension-

## 本章其它页面 {#related-pages}

- [应包含（和排除）什么](01-what-to-include/)
- [`#[doc]` 属性](02-the-doc-attribute/)
- [重导出](03-re-exports/)
- [按名称链接到项](04-linking-to-items-by-name/)
- [文档测试](05-documentation-tests/)

