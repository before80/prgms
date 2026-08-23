+++
title = "02-用法"
date = 2026-08-22T18:00:00+08:00
weight = 20
type = "docs"
description = "cargo clippy 与 clippy-driver 用法"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 用法 {#usage}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/usage.html](https://doc.rust-lang.org/nightly/clippy/usage.html)


本章介绍如何充分利用 Clippy。Clippy 可以作为 `cargo` 子命令使用，也可以像 `rustc` 一样直接通过 `clippy-driver` 二进制文件运行。

> 注意：本章假定你已经安装了 Clippy。若不确定，请参阅[安装]一章。

## Cargo 子命令

运行 Clippy 最简单、最常见的方式是通过 `cargo`。只需运行：

```bash
cargo clippy
```

### Lint 配置

上述命令会运行默认的 lint 集合，它们包含在 lint 组 `clippy::all` 中。你可能希望启用更多 lint，或者并不认同每一个 Clippy lint，为此可以配置 lint 级别。

> 注意：Clippy 的设计意图是在代码中适度使用 `#[allow(..)]`。因此，若你不同意某个 lint，不必为在部分代码或整个项目中禁用它而感到不妥。

#### 命令行

你可以在命令行上通过添加 `-A/W/D clippy::lint_name` 来配置 lint 级别，例如：

```bash
cargo clippy -- -Aclippy::style -Wclippy::box_default -Dclippy::perf
```

#### 将警告提升为错误

在 [CI] 中，可以将所有警告提升为错误，从而使构建失败，并让 Clippy 以非 `0` 退出码退出。

自 Cargo 1.97 起，推荐通过 [`build.warnings`] 配置项来实现。

可以在命令行上通过环境变量启用：

```bash
CARGO_BUILD_WARNINGS=deny cargo clippy
```

……或在 `.cargo/config.toml` 中永久设置：

```toml
# .cargo/config.toml
[build]
warnings = "deny"
```

> 注意：使用 `CARGO_BUILD_WARNINGS=deny`（或 `-D warnings`）会在代码中发现**任何**警告时导致构建失败。这包括 rustc 发现的警告（例如 `dead_code` 等）。

若使用较旧版本的 Cargo，可以改用：

```bash
cargo clippy -- -Dwarnings
```

但请注意，这会破坏构建缓存，因此不推荐。

[`build.warnings`]: https://doc.rust-lang.org/cargo/reference/config.html#buildwarnings

有关配置 lint 级别的更多信息，请参阅 [rustc 文档]。

[rustc 文档]: https://doc.rust-lang.org/rustc/lints/levels.html#configuring-warning-levels

#### 更多 lint

Clippy 有一些默认允许的 lint 组。这意味着你必须手动启用这些组中的 lint。

所有 lint 的完整列表（含描述和示例）请参阅 [Clippy lint 列表]。下面介绍两个最重要的默认允许 lint 组：

[Clippy lint 列表]: https://rust-lang.github.io/rust-clippy/master/index.html

##### `clippy::pedantic`

第一个组是 `pedantic` 组。该组包含非常主观的 lint，可能会为了减少漏报而故意产生一些误报。因此，虽然该组可用于生产环境，但你可以预期需要在代码中多处添加 `#[allow(..)]`。若发现误报，仍欢迎向我们报告，以便后续改进。

> 补充说明：Clippy 使用整个组来 lint 自身。

##### `clippy::restriction`

第二个组是 `restriction` 组。该组包含以某种方式「限制」语言的 lint。例如，该组中的 `clippy::unwrap` lint 不允许在代码中使用 `.unwrap()`。你可能希望浏览该组中的 lint，并启用符合你需求的那些。

> 注意：你不应启用整个 lint 组，而应从该组中挑选 lint。该组中的某些 lint 甚至会与其他 Clippy lint 冲突！

#### 过多的 lint

Clippy 中最主观的默认警告 lint 组是 `clippy::style` 组。有些人倾向于完全禁用该组，然后从该组中挑选自己喜欢的 lint。当然，对 Clippy 的其他 lint 组也可以采用同样做法。

> 注意：我们努力使默认警告的 lint 组不含误报（FP）。若你发现某个 lint 错误触发，请在 issue 中报告（若尚无针对该 FP 的 issue）。

#### 源代码

你可以在源代码中配置 lint 级别，方式与配置 `rustc` lint 相同：

```rust,ignore
#![allow(clippy::style)]

#[warn(clippy::box_default)]
fn main() {
    let _ = Box::<String>::new(Default::default());
    // ^ 警告：`Box::new(_)` 使用了默认值
}
```

### 自动应用 Clippy 建议

与编译器一样，Clippy 可以自动应用部分 lint 建议。请注意，`--fix` 隐含 `--all-targets`，因此可以尽可能多地修复代码。

```terminal
cargo clippy --fix
```

### 工作区

所有常用的工作区选项都应适用于 Clippy。例如，以下命令会在工作区中的 `example` crate 上运行 Clippy：

```terminal
cargo clippy -p example
```

与 `cargo check` 一样，这会包含作为工作区成员的依赖，例如 path 依赖。若只想在指定的 crate 上运行 Clippy，请使用 `--no-deps` 选项：

```terminal
cargo clippy -p example -- --no-deps
```

## 不使用 `cargo` 运行 Clippy：`clippy-driver`

Clippy 也可用于不使用 cargo 的项目。为此，使用与 `rustc` 相同的参数运行 `clippy-driver`。例如：

```terminal
clippy-driver --edition 2018 -Cpanic=abort foo.rs
```

> 注意：`clippy-driver` 专为运行 Clippy 而设计，不应作为 `rustc` 的通用替代品。例如，`clippy-driver` 生成的产物可能未按预期优化。

[安装]: /clippy/installation/
[CI]: /clippy/continuous-integration/