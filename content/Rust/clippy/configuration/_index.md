+++
title = "03-配置"
date = 2026-08-22T18:00:00+08:00
weight = 30
type = "docs"
description = "clippy.toml 与 lint 级别配置"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 配置 {#configuration}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/configuration.html](https://doc.rust-lang.org/nightly/clippy/configuration.html)


> **注意：** 配置文件尚不稳定，未来可能会被弃用。

部分 lint 可在名为 `clippy.toml` 或 `.clippy.toml` 的 TOML 文件中配置。Clippy 会按以下优先级顺序，从第一个已定义的目录开始搜索：

1. `CLIPPY_CONF_DIR` 环境变量指定的目录，或
2. [CARGO_MANIFEST_DIR](https://doc.rust-lang.org/cargo/reference/environment-variables.html) 环境变量指定的目录，或
3. 当前目录。

若所选目录不包含配置文件，Clippy 会沿目录树向上遍历，在每个父目录中搜索，直到找到配置文件或到达文件系统根目录。

文件采用基本的 `variable = value` 映射，例如：

```toml
avoid-breaking-exported-api = false
disallowed-names = ["toto", "tata", "titi"]
```

[配置项表格](/clippy/configuration/01-lint-configuration/) 包含所有配置值、其默认值以及受影响的 lint 列表。每个[可配置 lint](https://rust-lang.github.io/rust-clippy/master/index.html#Configuration) 也包含这些值的相关信息。

对于具有默认值的列表类型配置（例如 [disallowed-names](https://rust-lang.github.io/rust-clippy/master/index.html#disallowed_names)），可使用特殊值 `".."` 来扩展默认值，而不是替换它们。

```toml
# disallowed-names 的默认值为 ["foo", "baz", "quux"]
disallowed-names = ["bar", ".."] # -> ["bar", "foo", "baz", "quux"]
```

若要禁用「for further information visit *lint-link*」消息，可定义 `CLIPPY_DISABLE_DOCS_LINKS` 环境变量。

### 允许/拒绝 Lint

#### 代码中的属性

你可以在代码中添加属性来 `allow`/`warn`/`deny` Clippy lint：

* 使用 `clippy` lint 组允许整个默认警告 lint 集合（`#![allow(clippy::all)]`）

* 使用 `clippy` 和 `clippy::pedantic` lint 组警告所有 lint（`#![warn(clippy::all, clippy::pedantic)]`。注意 `clippy::pedantic` 包含一些极易产生误报的激进 lint。

* 仅针对部分 lint（`#![deny(clippy::single_match, clippy::box_vec)]` 等）

* `allow`/`warn`/`deny` 可限定在单个函数或模块，使用 `#[allow(...)]` 等

注意：`allow` 表示为你的代码抑制该 lint。使用 `warn` 时，lint 仅发出警告；使用 `deny` 时，lint 会发出错误。错误会导致 Clippy 以错误码退出，因此在 CI/CD 脚本中最有用。

#### 命令行标志

若不想在代码中包含 lint 级别，可在运行 Clippy 时通过额外标志全局启用/禁用 lint：

要允许 `lint_name`，运行：

```terminal
cargo clippy -- -A clippy::lint_name
```

要针对 `lint_name` 发出警告，运行：

```terminal
cargo clippy -- -W clippy::lint_name
```

这也适用于 lint 组。例如，可以启用所有 pedantic lint 的警告来运行 Clippy：

```terminal
cargo clippy -- -W clippy::pedantic
```

若只关心某些 lint，可以允许所有其他 lint，然后显式警告你感兴趣的 lint：

```terminal
cargo clippy -- -A clippy::all -W clippy::useless_format -W clippy::...
```

#### `Cargo.toml` 中的 Lints 节

最后，可通过 `Cargo.toml` 文件中的 [lints 节](https://doc.rust-lang.org/nightly/cargo/reference/manifest.html#the-lints-section) 来允许/拒绝 lint：

要拒绝 `clippy::enum_glob_use`，在 `Cargo.toml` 中添加：

```toml
[lints.clippy]
enum_glob_use = "deny"
```

更多详情和选项请参阅 Cargo 文档。

### 指定最低支持的 Rust 版本

打算支持旧版 Rust 的项目，可在 Clippy 配置文件中指定最低支持的 Rust 版本（MSRV），以禁用与较新特性相关的 lint。

```toml
msrv = "1.30.0"
```

MSRV 也可通过属性指定，如下所示。

```rust,ignore
#![feature(custom_inner_attributes)]
#![clippy::msrv = "1.30.0"]

fn main() {
    ...
}
```

指定 MSRV 时也可省略补丁版本，因此 `msrv = 1.30` 等价于 `msrv = 1.30.0`。

> **注意：** 部分 lint 的行为取决于配置的 MSRV。
> 在某些情况下，Clippy 可能完全抑制某个 lint，以避免建议配置 MSRV 下不可用的 API 或语法。
> 在其他情况下，Clippy 可能仍会发出 lint，但会选择较旧、兼容的建议。

> **注意：** `custom_inner_attributes` 是不稳定特性，必须显式启用。

识别此配置选项的 lint 可在[此处](https://rust-lang.github.io/rust-clippy/master/index.html#msrv)找到。

### 禁用对特定代码的评估

> **注意：** 仅在其他方案（如 `#[allow(clippy::all)]`）不足时才应使用此方法。

极少数情况下，你可能希望完全阻止 Clippy 评估某些代码段。可通过[条件编译](https://doc.rust-lang.org/reference/conditional-compilation.html)实现，检查 `clippy` cfg 是否未设置。你可能需要提供桩代码以使代码能够编译：

```rust
#[cfg(not(clippy))]
include!(concat!(env!("OUT_DIR"), "/my_big_function-generated.rs"));

#[cfg(clippy)]
fn my_big_function(_input: &str) -> Option<MyStruct> {
    None
}
```
