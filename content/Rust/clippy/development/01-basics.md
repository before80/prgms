+++
title = "01-基础"
date = 2026-08-22T18:00:00+08:00
weight = 71
type = "docs"
description = "获取源码、编译与测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 基础 {#basics}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/basics.html](https://doc.rust-lang.org/nightly/clippy/development/basics.html)


本文说明参与 Clippy 开发所需的基础知识，包括如何构建与测试 Clippy 等。若要更深入地了解代码库，请参阅[添加 Lint] 或[常用工具]。

[添加 Lint]: adding_lints.md
[常用工具]: common_tools_writing_lints.md

- [参与 Clippy 开发的基础](#参与-clippy-开发的基础)
  - [获取代码](#获取代码)
  - [构建与测试](#构建与测试)
  - [`cargo dev`](#cargo-dev)
  - [lintcheck](#lintcheck)
  - [PR](#pr)
  - [常见缩写](#常见缩写)
  - [从源码安装](#从源码安装)

## 获取代码

首先确保已检出 Clippy 的最新版本。若这是你第一次参与 Clippy 开发，请先 fork 仓库，再用以下命令克隆：

```bash
git clone git@github.com:<your-username>/rust-clippy
```

若你之前已克隆过 Clippy，请更新到最新版本：

```bash
# 若尚未添加 upstream 远程
git remote add upstream https://github.com/rust-lang/rust-clippy
# upstream 必须是 rust-lang/rust-clippy 仓库的远程
git fetch upstream
# 确保当前在 master 分支
git checkout master
# 将本地 master 变基到 upstream master
git rebase upstream/master
# 推送到你 fork 的 master 分支
git push
```

## 构建与测试

可以像其他 Rust 项目一样构建和测试 Clippy：

```bash
cargo build  # 构建 Clippy
cargo test   # 测试 Clippy
```

由于 Clippy 测试套件很大，有一些命令只运行其中一部分测试：

```bash
# 仅运行 UI 测试
cargo uitest
# 仅运行以 `test_` 开头的 UI 测试
TESTNAME="test_" cargo uitest
# 仅运行 dogfood 测试
cargo dev dogfood
```

若 [UI 测试] 的输出与预期不符，可用以下命令更新参考文件：

```bash
cargo bless
```

例如，当你修复 lint 错误信息中的拼写错误，或修改测试文件以添加测试用例时，就需要这样做。

> _注意：_ 该命令可能更新超出你预期的文件。此时请只提交你打算更新的文件。

[UI 测试]: https://rustc-dev-guide.rust-lang.org/tests/adding.html#ui-test-walkthrough

## `cargo dev`

Clippy 提供一些开发工具，让开发更便捷。这些工具通过 `cargo dev` 访问。可用工具如下。要了解更多信息，可对各命令加上 `--help`。

```bash
# 格式化整个 Clippy 代码库及所有测试
cargo dev fmt
# 注册或更新 lint 名称/分组/...
cargo dev update_lints
# 创建新 lint 并注册
cargo dev new_lint
# 弃用 lint 并尝试删除相关代码
cargo dev deprecate
# 在每次提交前自动格式化所有代码
cargo dev setup git-hook
# （实验性）配置 Clippy 以配合 RustRover 使用
cargo dev setup intellij
# 运行 `dogfood` 测试
cargo dev dogfood
```

更多关于 [intellij] 命令的用法与原因。

[intellij]: https://github.com/rust-lang/rust-clippy/blob/master/CONTRIBUTING.md#rustrover

## lintcheck

`cargo lintcheck` 会在一组固定 crate 上构建并运行 Clippy，并生成结果日志。你可以用 `git diff` 将更新后的日志与先前版本对比，查看你的 lint 对少量 crate 的影响。若添加了新 lint，请审查产生的警告，确保没有误报且建议有效。

更多细节请参阅工具 [README]。

[README]: https://github.com/rust-lang/rust-clippy/blob/master/lintcheck/README.md

## PR

我们遵循 rustc 的无 merge commit 策略。参见
<https://rustc-dev-guide.rust-lang.org/contributing.html#opening-a-pr>。

## 常见缩写

| 缩写 | 含义 |
|--------------|----------------------------------------|
| UB           | 未定义行为（Undefined Behavior） |
| FP           | 误报（False Positive） |
| FN           | 漏报（False Negative） |
| ICE          | 编译器内部错误（Internal Compiler Error） |
| AST          | 抽象语法树（Abstract Syntax Tree） |
| MIR          | 中级中间表示（Mid-Level Intermediate Representation） |
| HIR          | 高级中间表示（High-Level Intermediate Representation） |
| TCX          | 类型上下文（Type context） |

这是 Clippy 开发中可能出现的缩写简明列表。更完整的通用列表见 [rustc-dev-guide 术语表][glossary]。若对某个缩写或含义不清楚，请随时提问。

## 从源码安装

若你正在开发 Clippy 并希望从源码安装，请按以下步骤操作：

在 Clippy 项目根目录运行以下命令，构建 Clippy 二进制并复制到工具链目录。默认会创建名为 `clippy` 的新工具链，其他选项见 `cargo dev setup toolchain --help`。

```terminal
cargo dev setup toolchain
```

之后即可在新工具链下于任意项目中运行 `cargo +clippy clippy`。

```terminal
cd my-project
cargo +clippy clippy
```

……或使用 `clippy-driver`：

```terminal
clippy-driver +clippy <filename>
```

若不再需要该工具链，可用 `rustup` 卸载：

```terminal
rustup toolchain uninstall clippy
```

> **请勿**使用 `cargo install --path . --force` 安装，因为这会覆盖 rustup
> [代理](https://rust-lang.github.io/rustup/concepts/proxies.html)。也就是说，
> `~/.cargo/bin/cargo-clippy` 与 `~/.cargo/bin/clippy-driver` 应是
> `~/.cargo/bin/rustup` 的硬链接或软链接。可运行 `rustup update` 修复。

[glossary]: https://rustc-dev-guide.rust-lang.org/appendix/glossary.html
