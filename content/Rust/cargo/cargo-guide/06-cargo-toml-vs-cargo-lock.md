+++
title = "06-Cargo.toml 与 Cargo.lock"
date = 2026-07-30T14:49:00+08:00
weight = 26
type = "docs"
description = "清单文件与锁文件的职责区别"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Cargo.toml 与 Cargo.lock {#cargotoml-vs-cargolock}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html)


`Cargo.toml` 与 `Cargo.lock` 服务于两个不同的目的。在详细讨论之前，先做一个摘要：

* `Cargo.toml` 用于从较宽泛的意义上描述你的依赖，由你来编写。
* `Cargo.lock` 包含关于依赖的确切信息。它由 Cargo 维护，不应手工编辑。

拿不准时，请把 `Cargo.lock` 提交到版本控制系统（例如 Git）。要更好地理解原因以及可能的替代方案，参见[常见问题中的「为什么要把 Cargo.lock 纳入版本控制？」](../../05-faq/#why-have-cargolock-in-version-control)。我们建议将其与[验证最新依赖](../08-continuous-integration/#verifying-latest-dependencies)配合使用。

让我们再深入一点。

`Cargo.toml` 是一份[**清单（manifest）**][def-manifest]文件，你可以在其中指定关于包的各种元数据。例如，你可以声明依赖另一个包：

```toml
[package]
name = "hello_world"
version = "0.1.0"

[dependencies]
regex = { git = "https://github.com/rust-lang/regex.git" }
```

这个包只有一个依赖，即 `regex` 库。此处声明依赖位于 GitHub 上的特定 Git 仓库。由于你没有指定其他信息，Cargo 假定你打算用默认分支上的最新提交来构建包。

听起来不错？不过有个问题：若你今天构建这个包，然后把副本发给我，我明天再构建，就可能出问题。与此同时 `regex` 可能已有更多提交，我的构建会包含新提交，而你的不会。因此我们会得到不同的构建结果。这不好，因为我们希望构建可重复。

你可以通过在 `Cargo.toml` 中定义具体的 `rev` 值来修复该问题，这样 Cargo 在构建包时就能确切知道使用哪个修订：

```toml
[dependencies]
regex = { git = "https://github.com/rust-lang/regex.git", rev = "9f9f693" }
```

现在我们的构建会相同。但有一个很大的缺点：每次想更新库时，你都得手动考虑 SHA-1。这既繁琐又容易出错。

于是就有了 `Cargo.lock`。有了它，你不必手动跟踪确切修订：Cargo 会替你完成。当你有这样的清单时：

```toml
[package]
name = "hello_world"
version = "0.1.0"

[dependencies]
regex = { git = "https://github.com/rust-lang/regex.git" }
```

Cargo 会取最新提交，并在你首次构建时把该信息写入 `Cargo.lock`。该文件看起来会像这样：

```toml
[[package]]
name = "hello_world"
version = "0.1.0"
dependencies = [
 "regex 1.5.0 (git+https://github.com/rust-lang/regex.git#9f9f693768c584971a4d53bc3c586c33ed3a6831)",
]

[[package]]
name = "regex"
version = "1.5.0"
source = "git+https://github.com/rust-lang/regex.git#9f9f693768c584971a4d53bc3c586c33ed3a6831"
```

可以看到这里有多得多的信息，包括你用来构建的确切修订。现在当你把包交给别人时，即使你没有在 `Cargo.toml` 中指定，他们也会使用完全相同的 SHA。

当你准备采用该库的新版本时，Cargo 可以重新计算依赖并为你更新：

```console
$ cargo update         # 更新所有依赖
$ cargo update regex   # 仅更新 “regex”
```

这会写出带有新版本信息的新 `Cargo.lock`。注意，传给 `cargo update` 的参数实际上是[包 ID 规范](../../cargo-reference/10-package-id-specifications/)，而 `regex` 只是一个简短规范。

[def-manifest]:  ../../appendix/01-glossary/#manifest  '"manifest" (glossary entry)'
[def-package]:   ../../appendix/01-glossary/#package   '"package" (glossary entry)'
