+++
title = "16-Lint"
date = 2026-07-30T14:49:00+08:00
weight = 58
type = "docs"
description = "[lints] 表与 Cargo/rustc/clippy lint 配置"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Lint {#lints}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/lints.html](https://doc.rust-lang.org/cargo/reference/lints.html)


> [!NOTE]
> 本章介绍由 `cargo` 自身发出的 lint。
>
> 关于为 `rustc` 或 `clippy` 等工具配置 lint 级别，见 [Manifest 格式章节中的 lints 小节](../the-manifest-format/#the-lints-section)。

> [!WARNING]
> [Cargo 的 lint 系统尚不稳定](../17-unstable-features/#lintscargo)，只能在 nightly 工具链上使用。



| 组                   | 说明                                                                                | 默认级别 |
|----------------------|-------------------------------------------------------------------------------------|---------------|
| `cargo::default`     | 默认开启的所有 lint（correctness、suspicious、style、complexity、perf） | warn/deny     |
| `cargo::correctness` | 明显错误或无用的代码                                              | deny          |
| `cargo::complexity`  | 以复杂方式做简单事情的代码                                | warn          |
| `cargo::perf`        | 可写得更快的代码                                              | warn          |
| `cargo::style`       | 应以更符合惯例的方式编写的代码                                 | warn          |
| `cargo::suspicious`  | 极可能错误或无用的代码                                           | warn          |
| `cargo::nursery`     | 仍在开发中的新 lint                                          | allow         |
| `cargo::pedantic`    | 相当严格或偶尔有误报的 lint                    | allow         |
| `cargo::restriction` | 阻止使用某些 Cargo 特性的 lint                                       | allow         |


## 默认允许（Allowed-by-default） {#allowed-by-default}
这些 lint 默认都设为 'allow' 级别。
- [`non_kebab_case_features`](#non_kebab_case_features)
- [`non_kebab_case_packages`](#non_kebab_case_packages)
- [`non_snake_case_features`](#non_snake_case_features)
- [`non_snake_case_packages`](#non_snake_case_packages)

## 默认警告（Warn-by-default） {#warn-by-default}
这些 lint 默认都设为 'warn' 级别。
- [`blanket_hint_mostly_unused`](#blanket_hint_mostly_unused)
- [`missing_lints_inheritance`](#missing_lints_inheritance)
- [`non_kebab_case_bins`](#non_kebab_case_bins)
- [`redundant_homepage`](#redundant_homepage)
- [`redundant_readme`](#redundant_readme)
- [`unknown_lints`](#unknown_lints)
- [`unused_dependencies`](#unused_dependencies)
- [`unused_workspace_dependencies`](#unused_workspace_dependencies)
- [`unused_workspace_package_fields`](#unused_workspace_package_fields)

## 默认拒绝（Deny-by-default） {#deny-by-default}
这些 lint 默认都设为 'deny' 级别。
- [`text_direction_codepoint_in_comment`](#text_direction_codepoint_in_comment)
- [`text_direction_codepoint_in_literal`](#text_direction_codepoint_in_literal)

## `blanket_hint_mostly_unused` {#blanket_hint_mostly_unused}
- 组：`suspicious`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查是否对所有依赖应用了 `hint-mostly-unused`。

### 为什么不好？ {#why-is-this-bad}
`hint-mostly-unused` 表示依赖它的任何代码大多不会使用该 crate 的 API 表面；此提示可通过尽量减少从未使用项的编译时间来加速构建。
对不符合该标准的 crate 误用会使构建变慢而非变快。应有选择地应用于符合这些标准的依赖。全局应用始终是误用，很可能会使构建变慢。

### 示例 {#example}
```toml
[profile.dev.package."*"]
hint-mostly-unused = true
```

应改为：
```toml
[profile.dev.package.huge-mostly-unused-dependency]
hint-mostly-unused = true
```


## `missing_lints_inheritance` {#missing_lints_inheritance}
- 组：`suspicious`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查在存在 `workspace.lints` 时包是否缺少 `lints` 表。

### 为什么不好？ {#why-is-this-bad}
许多人误以为 `workspace.lints` 会隐式继承，实际上并不会。

### 缺点 {#drawbacks}
### 示例 {#example}
```toml
[workspace.lints.cargo]
```

应写为：

```toml
[workspace.lints.cargo]

[lints]
workspace = true
```

或通过添加空的 `[lints]` 表明确表示你不打算继承：

```toml
[workspace.lints.cargo]

[lints]
```


## `non_kebab_case_bins` {#non_kebab_case_bins}
- 组：`style`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检测非 kebab-case 的二进制名称（显式与隐式）。

### 为什么不好？ {#why-is-this-bad}
kebab-case 二进制名称是命令行工具的常见约定。

### 缺点 {#drawbacks}
更改二进制名称会对现有用户造成干扰。

二进制可能需要符合外部控制的约定，其中可能包含不同的命名约定。

GUI 应用可能希望选择更面向用户的命名约定，如「Title Case」或「Sentence case」。

### 示例 {#example}
```toml
[[bin]]
name = "foo_bar"
```

应写为：

```toml
[[bin]]
name = "foo-bar"
```


## `non_kebab_case_features` {#non_kebab_case_features}
- 组：`restriction`
- 级别：`allow`


### 它做什么 {#what-it-does}
检测非 kebab-case 的特性名称。

### 为何限制此行为？ {#why-restrict-this}
工作空间内存在多种命名风格可能造成混淆。

### 缺点 {#drawbacks}
用户会期望与依赖紧密耦合的特性与依赖名称匹配。

### 示例 {#example}
```toml
[features]
foo_bar = []
```

应写为：

```toml
[features]
foo-bar = []
```


## `non_kebab_case_packages` {#non_kebab_case_packages}
- 组：`restriction`
- 级别：`allow`


### 它做什么 {#what-it-does}
检测非 kebab-case 的包名。

### 为何限制此行为？ {#why-restrict-this}
工作空间内存在多种命名风格可能造成混淆。

### 缺点 {#drawbacks}
用户必须在脑中将包名转换为 Rust 中的命名空间。

### 示例 {#example}
```toml
[package]
name = "foo_bar"
```

应写为：

```toml
[package]
name = "foo-bar"
```


## `non_snake_case_features` {#non_snake_case_features}
- 组：`restriction`
- 级别：`allow`


### 它做什么 {#what-it-does}
检测非 snake-case 的特性名称。

### 为何限制此行为？ {#why-restrict-this}
工作空间内存在多种命名风格可能造成混淆。

### 缺点 {#drawbacks}
用户会期望与依赖紧密耦合的特性与依赖名称匹配。

### 示例 {#example}
```toml
[features]
foo-bar = []
```

应写为：

```toml
[features]
foo_bar = []
```


## `non_snake_case_packages` {#non_snake_case_packages}
- 组：`restriction`
- 级别：`allow`


### 它做什么 {#what-it-does}
检测非 snake-case 的包名。

### 为何限制此行为？ {#why-restrict-this}
工作空间内存在多种命名风格可能造成混淆。

### 缺点 {#drawbacks}
用户必须在脑中将包名转换为 Rust 中的命名空间。

### 示例 {#example}
```toml
[package]
name = "foo_bar"
```

应写为：

```toml
[package]
name = "foo-bar"
```


## `redundant_homepage` {#redundant_homepage}
- 组：`style`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查 `package.homepage` 的值是否已被另一字段覆盖。

另见 [`package.homepage` 参考文档](../the-manifest-format/#the-homepage-field)。

### 为什么不好？ {#why-is-this-bad}
当包浏览器渲染每个链接时，冗余链接会增加视觉噪音。

### 缺点 {#drawbacks}
### 示例 {#example}
```toml
[package]
name = "foo"
homepage = "https://github.com/rust-lang/cargo/"
repository = "https://github.com/rust-lang/cargo/"
```

应写为：

```toml
[package]
name = "foo"
repository = "https://github.com/rust-lang/cargo/"
```


## `redundant_readme` {#redundant_readme}
- 组：`style`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查可被推断的 `package.readme` 字段。

另见 [`package.readme` 参考文档](../the-manifest-format/#the-readme-field)。

### 为什么不好？ {#why-is-this-bad}
增加样板代码。

### 缺点 {#drawbacks}
他们是否正确命名了文件可能并不明显。

### 示例 {#example}
```toml
[package]
name = "foo"
readme = "README.md"
```

应写为：

```toml
[package]
name = "foo"
```


## `text_direction_codepoint_in_comment` {#text_direction_codepoint_in_comment}
- 组：`correctness`
- 级别：`deny`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检测清单注释中会改变屏幕上文本视觉呈现、且与内存中表示不一致的 Unicode 码点。

### 为什么不好？ {#why-is-this-bad}
Unicode 允许改变屏幕上文本的视觉流向，以支持从右到左书写的文字，
但精心构造的注释可能使将被编译的代码看起来像是注释的一部分，
这取决于用于阅读代码的软件。
为避免潜在问题或混淆，
例如 CVE-2021-42574，
我们默认拒绝使用它们。


## `text_direction_codepoint_in_literal` {#text_direction_codepoint_in_literal}
- 组：`correctness`
- 级别：`deny`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检测清单字面量中会改变屏幕上文本视觉呈现、且与内存中表示不一致的 Unicode 码点。

### 为什么不好？ {#why-is-this-bad}
Unicode 允许改变屏幕上文本的视觉流向，以支持从右到左书写的文字，
但精心构造的字面量可能使将被编译的代码看起来像是字面量的一部分，
这取决于用于阅读代码的软件。
为避免潜在问题或混淆，
例如 CVE-2021-42574，
我们默认拒绝使用它们。


## `unknown_lints` {#unknown_lints}
- 组：`suspicious`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查 `[lints.cargo]` 表中的未知 lint

### 为什么不好？ {#why-is-this-bad}
- lint 名称可能拼写错误，导致对其为何未按预期工作产生困惑
- 若将来 `cargo` 决定添加同名 lint，未知 lint 最终可能导致错误

### 示例 {#example}
```toml
[lints.cargo]
this-lint-does-not-exist = "warn"
```


## `unused_dependencies` {#unused_dependencies}
- 组：`style`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查未被任何 cargo 目标使用的依赖。

### 为什么不好？ {#why-is-this-bad}
减慢编译时间。

### 缺点 {#drawbacks}
此 lint 仅在特定情况下发出，因为不同依赖表对应多个 cargo 目标，必须全部构建才能知道依赖是否未使用。
目前仅检查所选包，而不像大多数 lint 那样检查所有 `path` 依赖。
cargo 目标选择标志（与选择哪些包无关）决定检查哪些依赖表。
由于无法选择所有使用 `[dev-dependencies]` 的 cargo 目标，
它们不会被检查。

示例：
- `cargo check` 会检查 `[build-dependencies]` 与 `[dependencies]`
- `cargo check --all-targets` 仍只检查 `[build-dependencies]` 与 `[dependencies]`，而不检查 `[dev-dependencoes]`
- `cargo check --bin foo` 即使 `foo` 是唯一的 bin 也不会检查 `[dependencies]`，尽管会检查 `[build-dependencies]`
- `cargo check -p foo` 不会为 `path` 依赖 `bar` 检查任何依赖表，即使 `bar` 只有一个 `[lib]`

依赖传递依赖以激活特性时可能出现误报。

对于在 `Cargo.toml` 中固定传递依赖版本导致的误报，
可将该依赖移到 `target."cfg(false)".dependencies` 表中。

### 示例 {#example}
```toml
[package]
name = "foo"

[dependencies]
unused = "1"
```

应写为：

```toml
[package]
name = "foo"
```


## `unused_workspace_dependencies` {#unused_workspace_dependencies}
- 组：`suspicious`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查 `[workspace.dependencies]` 中尚未被继承的任何条目

### 为什么不好？ {#why-is-this-bad}
它们可能给人留下这些依赖正在被使用的错误印象

### 示例 {#example}
```toml
[workspace.dependencies]
regex = "1"

[dependencies]
```


## `unused_workspace_package_fields` {#unused_workspace_package_fields}
- 组：`suspicious`
- 级别：`warn`
- 最低 [`package.rust-version`]：`1.79.0`


### 它做什么 {#what-it-does}
检查 `[workspace.package]` 中尚未被继承的任何字段

### 为什么不好？ {#why-is-this-bad}
它们可能给人留下这些字段正在被使用的错误印象

### 示例 {#example}
```toml
[workspace.package]
edition = "2024"

[package]
name = "foo"
```



[`package.rust-version`]: ../the-manifest-format/02-rust-version/
