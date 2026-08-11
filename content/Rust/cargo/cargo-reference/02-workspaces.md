+++
title = "02-工作空间"
date = 2026-07-30T14:49:00+08:00
weight = 34
type = "docs"
description = "Cargo 工作空间成员、依赖与继承"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 工作空间


> 原文链接: [https://doc.rust-lang.org/cargo/reference/workspaces.html](https://doc.rust-lang.org/cargo/reference/workspaces.html)


*工作空间（workspace）* 是一个或多个包的集合，这些包称为 *工作空间成员（workspace members）*，被一起管理。

工作空间的要点是：

* 常用命令可跨所有工作空间成员运行，例如 `cargo check --workspace`。
* 所有包共享一份位于 *工作空间根* 的公共 [`Cargo.lock`] 文件。
* 所有包共享一个公共[输出目录]，默认是 *工作空间根* 下名为 `target` 的目录。
* 可共享包元数据，例如通过 [`workspace.package`](#the-package-table)。
* `Cargo.toml` 中的 [`[patch]`][patch]、[`[replace]`][replace] 与 [`[profile.*]`][profiles]
  节仅在 *根* 清单中被识别，成员 crate 清单中的会被忽略。

工作空间的根 `Cargo.toml` 支持以下节：

* [`[workspace]`](#the-workspace-section) —— 定义工作空间。
  * [`resolver`](../specifying-dependencies/03-dependency-resolution/#resolver-versions) —— 设置要使用的依赖解析器。
  * [`members`](#the-members-and-exclude-fields) —— 要包含在工作空间中的包。
  * [`exclude`](#the-members-and-exclude-fields) —— 要从工作空间中排除的包。
  * [`default-members`](#the-default-members-field) —— 未选择特定包时要操作的包。
  * [`package`](#the-package-table) —— 供包继承的键。
  * [`dependencies`](#the-dependencies-table) —— 供包依赖继承的键。
  * [`lints`](#the-lints-table) —— 供包 lint 继承的键。
  * [`metadata`](#the-metadata-table) —— 供外部工具使用的额外设置。
* [`[patch]`](../specifying-dependencies/01-overriding-dependencies/#the-patch-section) —— 覆盖依赖。
* [`[replace]`](../specifying-dependencies/01-overriding-dependencies/#the-replace-section) —— 覆盖依赖（已弃用）。
* [`[profile]`](../05-profiles/) —— 编译器设置与优化。

## `[workspace]` 节 {#the-workspace-section}

要创建工作空间，向 `Cargo.toml` 添加 `[workspace]` 表：
```toml
[workspace]
# ...
```

工作空间至少要有一个成员，可以是根包，也可以是虚拟清单。

### 根包 {#root-package}

若将 [`[workspace]` 节](#the-workspace-section) 添加到已定义 `[package]` 的 `Cargo.toml`，则该包是工作空间的 *根包*。*工作空间根* 是工作空间 `Cargo.toml` 所在的目录。

```toml
[workspace]

[package]
name = "hello_world" # 包名
version = "0.1.0"    # 当前版本，遵循 semver
```

### 虚拟工作空间 {#virtual-workspace}

或者，可以创建带有 `[workspace]` 节但不含 [`[package]` 节][package] 的 `Cargo.toml` 文件。这称为 *虚拟清单（virtual manifest）*。当没有「主」包，或你希望将所有包组织在独立目录中时，这通常很有用。

```toml
# [PROJECT_DIR]/Cargo.toml
[workspace]
members = ["hello_world"]
resolver = "3"
```

```toml
# [PROJECT_DIR]/hello_world/Cargo.toml
[package]
name = "hello_world" # 包名
version = "0.1.0"    # 当前版本，遵循 semver
edition = "2024"     # edition，不会影响工作空间中使用的解析器
```

通过使用没有根包的工作空间，

- 虚拟工作空间中必须显式设置 [`resolver`](../specifying-dependencies/03-dependency-resolution/#resolver-versions)，因为它们没有可用于推断[解析器版本](../specifying-dependencies/03-dependency-resolution/#resolver-versions)的 [`package.edition`][package-edition]。
- 在工作空间根运行的命令默认会对所有工作空间成员运行，见 [`default-members`](#the-default-members-field)。

## `members` 与 `exclude` 字段 {#the-members-and-exclude-fields}

`members` 与 `exclude` 字段定义哪些包是工作空间的成员：

```toml
[workspace]
members = ["member1", "path/to/member2", "crates/*"]
exclude = ["crates/foo", "path/to/other"]
```

位于工作空间目录中的所有 [`path` 依赖]会自动成为成员。可用 `members` 键列出额外成员，它应是包含带有 `Cargo.toml` 文件的目录的字符串数组。

`members` 列表还支持 [glob][globs] 以匹配多条路径，使用典型的文件名 glob 模式如 `*` 与 `?`。

**建议：** 将所有成员包放在扁平目录中（通常为 `crates/`），
并为 `members` 字段使用 glob 模式，例如
`members = ["crates/*"]`。这可最大限度地减少维护 `members` 列表的变动。

`exclude` 键可用于阻止路径被包含在工作空间中。若某些 path 依赖完全不希望加入工作空间，或在使用 glob 模式时想移除某个目录，这会很有用。

当位于工作空间内的子目录中时，Cargo 会自动向上搜索父目录中带有 `[workspace]` 定义的 `Cargo.toml` 文件，以确定使用哪个工作空间。成员 crate 中可使用 [`package.workspace`] 清单键指向工作空间根，以覆盖此自动搜索。若成员不在工作空间根的子目录内，手动设置会很有用。

### 包选择 {#package-selection}
在工作空间中，像 [`cargo build`] 这样与包相关的 Cargo 命令可使用 `-p` / `--package` 或 `--workspace` 命令行标志来确定要对哪些包操作。若未指定这些标志，Cargo 将使用当前工作目录中的包。然而，若当前目录是工作空间根，则将使用 [`default-members`](#the-default-members-field)。

## `default-members` 字段 {#the-default-members-field}

`default-members` 字段指定：当位于工作空间根且未使用包选择标志时，要操作的[成员](#the-members-and-exclude-fields)路径：

```toml
[workspace]
members = ["path/to/member1", "path/to/member2", "path/to/member3/*"]
default-members = ["path/to/member2", "path/to/member3/foo"]
```

> 注意：当存在[根包](#root-package)时，
> 只能使用 `--package` 与 `--workspace` 标志对其进行操作。

未指定时，将使用[根包](#root-package)。
对于[虚拟工作空间](#virtual-workspace)，将使用所有成员
（如同在命令行上指定了 `--workspace`）。

## `package` 表 {#the-package-table}

`workspace.package` 表用于定义可由工作空间成员继承的键。成员包可通过以 `{key}.workspace = true` 定义这些键来继承它们。

支持的键：

|                |                 |
|----------------|-----------------|
| `authors`      | `categories`    |
| `description`  | `documentation` |
| `edition`      | `exclude`       |
| `homepage`     | `include`       |
| `keywords`     | `license`       |
| `license-file` | `publish`       |
| `readme`       | `repository`    |
| `rust-version` | `version`       |

- `license-file` 与 `readme` 相对于工作空间根
- `include` 与 `exclude` 相对于你的包根

示例：
```toml
# [PROJECT_DIR]/Cargo.toml
[workspace]
members = ["bar"]

[workspace.package]
version = "1.2.3"
authors = ["Nice Folks"]
description = "A short description of my package"
documentation = "https://example.com/bar"
```

```toml
# [PROJECT_DIR]/bar/Cargo.toml
[package]
name = "bar"
version.workspace = true
authors.workspace = true
description.workspace = true
documentation.workspace = true
```

> **MSRV：** 需要 1.64+

## `dependencies` 表 {#the-dependencies-table}

`workspace.dependencies` 表用于定义可由工作空间成员继承的依赖。

指定工作空间依赖与[包依赖][specifying-dependencies]类似，但有以下区别：
- 此表中的依赖不能声明为 `optional`
- 此表中声明的 [`features`][features] 与 `[dependencies]` 中的 `features` 是累加的

然后你可以[将工作空间依赖继承为包依赖][inheriting-a-dependency-from-a-workspace]

示例：
```toml
# [PROJECT_DIR]/Cargo.toml
[workspace]
members = ["bar"]

[workspace.dependencies]
cc = "1.0.73"
rand = "0.8.5"
regex = { version = "1.6.0", default-features = false, features = ["std"] }
```

```toml
# [PROJECT_DIR]/bar/Cargo.toml
[package]
name = "bar"
version = "0.2.0"

[dependencies]
regex = { workspace = true, features = ["unicode"] }

[build-dependencies]
cc.workspace = true

[dev-dependencies]
rand.workspace = true
```

> **MSRV：** 需要 1.64+

## `lints` 表 {#the-lints-table}

`workspace.lints` 表用于定义可由工作空间成员继承的 lint 配置。

指定工作空间 lint 配置与[包 lint](../the-manifest-format/#the-lints-section) 类似。

示例：

```toml
# [PROJECT_DIR]/Cargo.toml
[workspace]
members = ["crates/*"]

[workspace.lints.rust]
unsafe_code = "forbid"
```

```toml
# [PROJECT_DIR]/crates/bar/Cargo.toml
[package]
name = "bar"
version = "0.1.0"

[lints]
workspace = true
```

> **MSRV：** 自 1.74 起生效

## `metadata` 表 {#the-metadata-table}

`workspace.metadata` 表会被 Cargo 忽略，且不会发出警告。本节可供希望在 `Cargo.toml` 中存储工作空间配置的工具使用。例如：

```toml
[workspace]
members = ["member1", "member2"]

[workspace.metadata.webcontents]
root = "path/to/webproject"
tool = ["npm", "run", "build"]
# ...
```

包级别也有类似的一组表：
[`package.metadata`][package-metadata]。虽然 Cargo 并未规定这两个表内容的格式，但建议外部工具以一致的方式使用它们，例如在 `package.metadata` 缺少数据时引用 `workspace.metadata` 中的数据（若对该工具合理）。

[package]: ../the-manifest-format/#the-package-section
[`Cargo.lock`]: ../../cargo-guide/06-cargo-toml-vs-cargo-lock/
[package-metadata]: ../the-manifest-format/#the-metadata-table
[package-edition]: ../the-manifest-format/#the-edition-field
[output directory]: ../09-build-cache/
[patch]: ../specifying-dependencies/01-overriding-dependencies/#the-patch-section
[replace]: ../specifying-dependencies/01-overriding-dependencies/#the-replace-section
[profiles]: ../05-profiles/
[`path` dependencies]: ../specifying-dependencies/#specifying-path-dependencies
[`package.workspace`]: ../the-manifest-format/#the-workspace-field
[globs]: https://docs.rs/glob/0.3.0/glob/struct.Pattern.html
[`cargo build`]: ../../cargo-commands/build-commands/02-cargo-build/
[specifying-dependencies]: ../specifying-dependencies/
[features]: ../features/
[inheriting-a-dependency-from-a-workspace]: ../specifying-dependencies/#inheriting-a-dependency-from-a-workspace
