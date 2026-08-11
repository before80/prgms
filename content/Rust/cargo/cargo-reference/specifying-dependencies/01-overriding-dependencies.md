+++
title = "01-覆盖依赖"
date = 2026-07-30T14:49:00+08:00
weight = 36
type = "docs"
description = "[patch] 与 [replace] 覆盖依赖"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 覆盖依赖 {#overriding-dependencies}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/overriding-dependencies.html](https://doc.rust-lang.org/cargo/reference/overriding-dependencies.html)


覆盖依赖的需求可能产生于多种场景。然而，其中大多数都归结为：在 crate 发布到 [crates.io] 之前就能使用它。例如：

* 你正在开发的 crate 也用在你正在开发的一个大得多的应用中，你希望在更大的应用内部测试对该库的 bug 修复。
* 你未参与开发的上游 crate 在其 git 仓库的 master 分支上有新特性或 bug 修复，你希望试用。
* 你即将发布 crate 的新主版本，但希望跨整个包做集成测试，以确保新主版本可用。
* 你已向上游 crate 提交了你发现的 bug 的修复，但希望让你的应用立即开始依赖该 crate 的已修复版本，以避免阻塞在 bug 修复被合并上。

这些场景可用 [`[patch]` 清单节](#the-patch-section)解决。

本章将介绍几种不同的用例，并包含关于覆盖依赖的不同方式的细节。

* 示例用例
    * [测试 bug 修复](#testing-a-bugfix)
    * [使用未发布的次版本](#working-with-an-unpublished-minor-version)
        * [覆盖仓库 URL](#overriding-repository-url)
    * [预发布破坏性变更](#prepublishing-a-breaking-change)
    * [对多个版本使用 `[patch]`](#using-patch-with-multiple-versions)
* 参考
    * [`[patch]` 节](#the-patch-section)
    * [`[replace]` 节](#the-replace-section)
    * [`paths` 覆盖](#paths-overrides)

> **注意**：另见用[多个位置][multiple locations]指定依赖，这可用于覆盖本地包中单条依赖声明的源。

## 测试 bug 修复 {#testing-a-bugfix}

假设你在使用 [`uuid` crate]，但在使用过程中发现了一个 bug。不过你很有进取心，于是决定也尝试修复该 bug！最初你的清单看起来像：

[`uuid` crate]: https://crates.io/crates/uuid

```toml
[package]
name = "my-library"
version = "0.1.0"

[dependencies]
uuid = "1.0"
```

我们要做的第一件事是通过以下方式在本地克隆 [`uuid` 仓库][uuid-repository]：

```console
$ git clone https://github.com/uuid-rs/uuid.git
```

接下来我们将编辑 `my-library` 的清单，使其包含：

```toml
[patch.crates-io]
uuid = { path = "../path/to/uuid" }
```

这里我们声明正在用一个新依赖*打补丁*源 `crates-io`。这将有效地把本地检出的 `uuid` 版本添加到我们本地包的 crates.io 注册表中。

接下来我们需要确保锁文件已更新为使用这个新版本的 `uuid`，以便我们的包使用本地检出的副本而非来自 crates.io 的副本。`[patch]` 的工作方式是：它会加载 `../path/to/uuid` 处的依赖，然后每当向 crates.io 查询 `uuid` 的版本时，它*也会*返回本地版本。

这意味着本地检出的版本号很重要，并将影响是否使用该补丁。我们的清单声明了 `uuid = "1.0"`，这意味着我们只会解析到 `>= 1.0.0, < 2.0.0`，而 Cargo 的贪婪解析算法也意味着我们会解析到该范围内的最大版本。通常这无关紧要，因为 git 仓库的版本已经大于或匹配 crates.io 上发布的最大版本，但记住这一点很重要！

无论如何，通常你现在只需要：

```console
$ cargo build
   Compiling uuid v1.0.0 (.../uuid)
   Compiling my-library v0.1.0 (.../my-library)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

就是这样！你现在正在用本地版本的 `uuid` 构建（注意构建输出中括号里的路径）。若你没有看到本地路径版本正在构建，则可能需要运行 `cargo update uuid --precise $version`，其中 `$version` 是本地检出的 `uuid` 副本的版本。

一旦你修复了最初发现的 bug，接下来你可能希望将其作为 pull request 提交给 `uuid` crate 本身。完成后，你也可以更新 `[patch]` 节。`[patch]` 内的列表就像 `[dependencies]` 节一样，因此一旦你的 pull request 被合并，你可以将 `path` 依赖改为：

```toml
[patch.crates-io]
uuid = { git = 'https://github.com/uuid-rs/uuid.git' }
```

[uuid-repository]: https://github.com/uuid-rs/uuid

## 使用未发布的次版本 {#working-with-an-unpublished-minor-version}

现在让我们从 bug 修复转向添加特性。在开发 `my-library` 时，你发现 `uuid` crate 中需要一个全新的特性。你已实现该特性，用上面的 `[patch]` 在本地测试过，并提交了 pull request。让我们看看在它实际发布之前，你如何继续使用并测试它。

我们还假设 crates.io 上 `uuid` 的当前版本是 `1.0.0`，但此后 git 仓库的 master 分支已更新到 `1.0.1`。该分支包含你之前提交的新特性。要使用此仓库，我们将编辑 `Cargo.toml`，使其看起来像：

```toml
[package]
name = "my-library"
version = "0.1.0"

[dependencies]
uuid = "1.0.1"

[patch.crates-io]
uuid = { git = 'https://github.com/uuid-rs/uuid.git' }
```

注意我们对 `uuid` 的本地依赖已更新为 `1.0.1`，因为一旦 crate 发布，这就是我们实际需要的版本。然而该版本在 crates.io 上尚不存在，因此我们通过清单的 `[patch]` 节提供它。

现在当我们的库构建时，它会从 git 仓库获取 `uuid`，并解析到仓库内的 1.0.1，而不是尝试从 crates.io 下载某个版本。一旦 1.0.1 发布到 crates.io，就可以删除 `[patch]` 节。

还值得注意的是，`[patch]` *传递*生效。假设你在更大的包中使用 `my-library`，例如：

```toml
[package]
name = "my-binary"
version = "0.1.0"

[dependencies]
my-library = { git = 'https://example.com/git/my-library' }
uuid = "1.0"

[patch.crates-io]
uuid = { git = 'https://github.com/uuid-rs/uuid.git' }
```

记住 `[patch]` *传递*适用，但只能在*顶层*定义，因此 `my-library` 的消费者在必要时必须重复 `[patch]` 节。不过这里，新的 `uuid` crate 同时适用于我们对 `uuid` 的依赖以及 `my-library -> uuid` 依赖。`uuid` crate 将为整个 crate 图解析为一个版本 1.0.1，并且会从 git 仓库拉取。

### 覆盖仓库 URL {#overriding-repository-url}

若你想覆盖的依赖不是从 `crates.io` 加载的，你需要稍微改变使用 `[patch]` 的方式。例如，若依赖是 git 依赖，你可以用本地路径覆盖它：

```toml
[patch."https://github.com/your/repository"]
my-library = { path = "../my-library/path" }
```

就是这样！

## 预发布破坏性变更 {#prepublishing-a-breaking-change}

让我们看看处理 crate 的新主版本（通常伴随破坏性变更）的情况。沿用之前的 crate，这意味着我们将创建 `uuid` crate 的版本 2.0.0。在我们向上游提交所有变更后，可以将 `my-library` 的清单更新为：

```toml
[dependencies]
uuid = "2.0"

[patch.crates-io]
uuid = { git = "https://github.com/uuid-rs/uuid.git", branch = "2.0.0" }
```

就是这样！与前面的示例一样，2.0.0 版本实际上并不存在于 crates.io 上，但我们仍可通过 `[patch]` 节用 git 依赖放入它。作为思考练习，让我们再看看上面的 `my-binary` 清单：

```toml
[package]
name = "my-binary"
version = "0.1.0"

[dependencies]
my-library = { git = 'https://example.com/git/my-library' }
uuid = "1.0"

[patch.crates-io]
uuid = { git = 'https://github.com/uuid-rs/uuid.git', branch = '2.0.0' }
```

注意这实际上会解析到 `uuid` crate 的两个版本。`my-binary` crate 将继续使用 `uuid` crate 的 1.x.y 系列，但 `my-library` crate 将使用 `uuid` 的 `2.0.0` 版本。这将允许你通过依赖图逐步推出对 crate 的破坏性变更，而不必被迫一次更新所有内容。

## 对多个版本使用 `[patch]` {#using-patch-with-multiple-versions}

你可以用用于重命名依赖的 `package` 键为同一 crate 的多个版本打补丁。例如，假设 `serde` crate 有一个我们希望用于其 `1.*` 系列的 bug 修复，但我们也希望原型使用我们 git 仓库中的 `2.0.0` 版本的 serde。要配置这一点，我们可以这样做：

```toml
[patch.crates-io]
serde = { git = 'https://github.com/serde-rs/serde.git' }
serde2 = { git = 'https://github.com/example/serde.git', package = 'serde', branch = 'v2' }
```

第一个 `serde = ...` 指令表示应从 git 仓库使用 serde `1.*`（拉取我们需要的 bug 修复），第二个 `serde2 = ...` 指令表示也应从 `https://github.com/example/serde` 的 `v2` 分支拉取 `serde` 包。我们在此假定该分支上的 `Cargo.toml` 提及版本 `2.0.0`。

注意使用 `package` 键时，这里的 `serde2` 标识符实际上会被忽略。我们只需要一个不与其他被打补丁的 crate 冲突的唯一名称。

## `[patch]` 节 {#the-patch-section}

`Cargo.toml` 的 `[patch]` 节可用于用其他副本覆盖依赖。语法与 [`[dependencies]`][dependencies] 节类似：

```toml
[patch.crates-io]
foo = { git = 'https://github.com/example/foo.git' }
bar = { path = 'my/local/bar' }

[dependencies.baz]
git = 'https://github.com/example/baz.git'

[patch.'https://github.com/example/baz']
baz = { git = 'https://github.com/example/patched-baz.git', branch = 'my-branch' }
```

> **注意**：`[patch]` 表也可以指定为[配置选项](../../06-configuration/)，例如在 `.cargo/config.toml` 文件中，或像 `--config 'patch.crates-io.rand.path="rand"'` 这样的 CLI 选项。这对于你不想提交的仅本地变更，或临时测试补丁，会很有用。

`[patch]` 表由类似依赖的子表组成。`[patch]` 之后的每个键是正在被打补丁的源的 URL，或注册表的名称。名称 `crates-io` 可用于覆盖默认注册表 [crates.io]。上例中的第一个 `[patch]` 演示了覆盖 [crates.io]，第二个 `[patch]` 演示了覆盖 git 源。

这些表中的每个条目都是普通的依赖规范，与清单 `[dependencies]` 节中的相同。`[patch]` 节中列出的依赖会被解析，并用于对指定 URL 处的源打补丁。上面的清单片段用 `foo` crate 与 `bar` crate 对 `crates-io` 源（例如 crates.io 本身）打补丁。它还用来自别处的 `my-branch` 对 `https://github.com/example/baz` 源打补丁。

可以用不存在的 crate 版本对源打补丁，也可以用已存在的 crate 版本打补丁。若源被已存在于该源中的 crate 版本打补丁，则源的原始 crate 会被替换。

Cargo 仅查看工作空间根处 `Cargo.toml` 清单中的补丁设置。在依赖中定义的补丁设置将被忽略。

## `[replace]` 节 {#the-replace-section}

> **注意**：`[replace]` 已弃用。你应改用 [`[patch]`](#the-patch-section) 表。

Cargo.toml 的这一节可用于用其他副本覆盖依赖。语法与 `[dependencies]` 节类似：

```toml
[replace]
"foo:0.1.0" = { git = 'https://github.com/example/foo.git' }
"bar:1.0.2" = { path = 'my/local/bar' }
```

`[replace]` 表中的每个键是[包 ID 规范](../../10-package-id-specifications/)，允许任意选择依赖图中的一个节点进行覆盖（需要 3 部分版本号）。每个键的值与指定依赖的 `[dependencies]` 语法相同，但你不能指定特性。注意当 crate 被覆盖时，用于覆盖的副本必须具有相同的名称与版本，但它可以来自不同的源（例如 git 或本地路径）。

Cargo 仅查看工作空间根处 `Cargo.toml` 清单中的 replace 设置。在依赖中定义的 replace 设置将被忽略。

## `paths` 覆盖 {#paths-overrides}

有时你只是临时在某个 crate 上工作，不想像上面的 `[patch]` 节那样修改 `Cargo.toml`。对于这种用例，Cargo 提供了一种限制得多的覆盖版本，称为 **path 覆盖**。

Path 覆盖通过 [`.cargo/config.toml`](../../06-configuration/) 而非 `Cargo.toml` 指定。在 `.cargo/config.toml` 内，你会指定一个名为 `paths` 的键：

```toml
paths = ["/path/to/uuid"]
```

此数组应填入包含 `Cargo.toml` 的目录。在本例中，我们只是添加 `uuid`，因此它将是唯一被覆盖的那个。此路径可以是绝对路径，或相对于包含 `.cargo` 文件夹的目录。

然而，path 覆盖比 `[patch]` 节限制更多，因为它们不能更改依赖图的结构。使用 path 替换时，先前的依赖集必须与新的 `Cargo.toml` 规范完全匹配。例如，这意味着不能用 path 覆盖来测试向 crate 添加依赖。在那种情况下必须改用 `[patch]`。因此，path 覆盖的使用通常仅限于快速 bug 修复，而非较大的变更。

> **注意**：使用本地配置覆盖路径仅对已发布到 [crates.io] 的 crate 有效。你不能用此特性告诉 Cargo 如何查找本地未发布的 crate。


[crates.io]: https://crates.io/
[multiple locations]: ../../#multiple-locations
[dependencies]: ../../
