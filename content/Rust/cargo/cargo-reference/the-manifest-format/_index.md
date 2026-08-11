+++
title = "01-Manifest 格式"
date = 2026-07-30T14:49:00+08:00
weight = 31
type = "docs"
description = "Cargo.toml 清单格式与 [package] 等表"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Manifest 格式


> 原文链接: [https://doc.rust-lang.org/cargo/reference/manifest.html](https://doc.rust-lang.org/cargo/reference/manifest.html)


每个包的 `Cargo.toml` 文件称为其 *manifest*（清单）。它以 [TOML] 格式编写，包含编译该包所需的元数据。关于 Cargo 如何查找清单文件的更多细节，请参阅 `cargo locate-project` 一节。

每个清单文件由以下部分组成：

* [`cargo-features`](../17-unstable-features/) —— 不稳定、仅 nightly 可用的特性。
* [`[package]`](#the-package-section) —— 定义一个包。
  * [`name`](#the-name-field) —— 包名。
  * [`version`](#the-version-field) —— 包版本。
  * [`authors`](#the-authors-field) —— 包作者。
  * [`edition`](#the-edition-field) —— Rust edition。
  * [`rust-version`](02-rust-version/) —— 最低支持的 Rust 版本。
  * [`description`](#the-description-field) —— 包描述。
  * [`documentation`](#the-documentation-field) —— 包文档的 URL。
  * [`readme`](#the-readme-field) —— 包 README 文件的路径。
  * [`homepage`](#the-homepage-field) —— 包主页 URL。
  * [`repository`](#the-repository-field) —— 包源码仓库 URL。
  * [`license`](#the-license-and-license-file-fields) —— 包许可证。
  * [`license-file`](#the-license-and-license-file-fields) —— 许可证文本的路径。
  * [`keywords`](#the-keywords-field) —— 包关键字。
  * [`categories`](#the-categories-field) —— 包分类。
  * [`workspace`](#the-workspace-field) —— 包所属工作空间的路径。
  * [`build`](#the-build-field) —— 包构建脚本的路径。
  * [`links`](#the-links-field) —— 包所链接的本地库名称。
  * [`exclude`](#the-exclude-and-include-fields) —— 发布时排除的文件。
  * [`include`](#the-exclude-and-include-fields) —— 发布时包含的文件。
  * [`publish`](#the-publish-field) —— 可用于阻止发布该包。
  * [`metadata`](#the-metadata-table) —— 供外部工具使用的额外设置。
  * [`default-run`](#the-default-run-field) —— [`cargo run`] 默认运行的二进制。
  * [`autolib`](01-cargo-targets/#target-auto-discovery) —— 禁用库自动发现。
  * [`autobins`](01-cargo-targets/#target-auto-discovery) —— 禁用二进制自动发现。
  * [`autoexamples`](01-cargo-targets/#target-auto-discovery) —— 禁用示例自动发现。
  * [`autotests`](01-cargo-targets/#target-auto-discovery) —— 禁用测试自动发现。
  * [`autobenches`](01-cargo-targets/#target-auto-discovery) —— 禁用基准测试自动发现。
  * [`resolver`](../specifying-dependencies/03-dependency-resolution/#resolver-versions) —— 设置要使用的依赖解析器。
* 目标表：（设置见[配置](01-cargo-targets/#configuring-a-target)）
  * [`[lib]`](01-cargo-targets/#library) —— 库目标设置。
  * [`[[bin]]`](01-cargo-targets/#binaries) —— 二进制目标设置。
  * [`[[example]]`](01-cargo-targets/#examples) —— 示例目标设置。
  * [`[[test]]`](01-cargo-targets/#tests) —— 测试目标设置。
  * [`[[bench]]`](01-cargo-targets/#benchmarks) —— 基准测试目标设置。
* 依赖表：
  * [`[dependencies]`](../specifying-dependencies/) —— 包的库依赖。
  * [`[dev-dependencies]`](../specifying-dependencies/#development-dependencies) —— 示例、测试与基准测试的依赖。
  * [`[build-dependencies]`](../specifying-dependencies/#build-dependencies) —— 构建脚本的依赖。
  * [`[target]`](../specifying-dependencies/#platform-specific-dependencies) —— 平台特定依赖。
* [`[badges]`](#the-badges-section) —— 在注册表上显示的徽章。
* [`[features]`](../features/) —— 条件编译特性。
* [`[lints]`](#the-lints-section) —— 为本包配置 linter。
* [`[hints]`](#the-hints-section) —— 为本包编译提供提示。
* [`[patch]`](../specifying-dependencies/01-overriding-dependencies/#the-patch-section) —— 覆盖依赖。
* [`[replace]`](../specifying-dependencies/01-overriding-dependencies/#the-replace-section) —— 覆盖依赖（已弃用）。
* [`[profile]`](../05-profiles/) —— 编译器设置与优化。
* [`[workspace]`](../02-workspaces/) —— 工作空间定义。

## `[package]` 节 {#the-package-section}

`Cargo.toml` 中的第一节是 `[package]`。

```toml
[package]
name = "hello_world" # 包名
version = "0.1.0"    # 当前版本，遵循 semver
```

Cargo 唯一必需的字段是 [`name`](#the-name-field)。若发布到注册表，注册表可能要求额外字段。关于发布到 [crates.io] 的要求，见下文说明以及[发布章节][publishing]。

### `name` 字段 {#the-name-field}

包名是用于引用该包的标识符。在另一个包中列为依赖时会用到它，也是推断出的 lib 与 bin 目标的默认名称。

名称只能使用[字母数字][alphanumeric]字符或 `-` 或 `_`，且不能为空。

注意 [`cargo new`] 与 [`cargo init`] 会对包名施加额外限制，例如强制其为有效的 Rust 标识符且不是关键字。[crates.io] 还会施加更多限制，例如：

- 仅允许 ASCII 字符。
- 不要使用保留名称。
- 不要使用特殊的 Windows 名称，例如 "nul"。
- 长度最多 64 个字符。

[alphanumeric]: https://doc.rust-lang.org/std/primitive.char.html#method.is_alphanumeric

### `version` 字段 {#the-version-field}

`version` 字段按 [SemVer] 规范格式化：

版本必须有三个数字部分：
主版本、次版本与补丁版本。

可在破折号后添加预发布部分，例如 `1.0.0-alpha`。
预发布部分可用句点分隔以区分独立组成部分。数字组成部分使用数值比较，
其他一切按字典序比较。
例如，`1.0.0-alpha.11` 高于 `1.0.0-alpha.4`。

可在加号后添加元数据部分，例如 `1.0.0+21AF26D3`。
这仅用于信息目的，Cargo 通常会忽略它。

Cargo 内建了[语义化版本](https://semver.org/)的概念，
因此若最左侧非零的主/次/补丁组成部分相同，则版本被视为[兼容](../13-semver-compatibility/)。
关于 Cargo 如何使用版本解析依赖，见[解析器][Resolver]章节。

该字段可选，默认为 `0.0.0`。发布包时该字段为必需。

> **MSRV：** 在 1.75 之前，该字段为必需

[SemVer]: https://semver.org
[Resolver]: ../specifying-dependencies/03-dependency-resolution/
[SemVer compatibility]: ../13-semver-compatibility/

### `authors` 字段 {#the-authors-field}

> **警告**：该字段已弃用

可选的 `authors` 字段以数组形式列出被视为包「作者」的个人或组织。可在每个作者条目末尾的尖括号中包含可选的电子邮件地址。

```toml
[package]
# ...
authors = ["Graydon Hoare", "Fnu Lnu <no-reply@rust-lang.org>"]
```

该字段会出现在包元数据中，以及 `build.rs` 内的 `CARGO_PKG_AUTHORS` 环境变量中，以保持向后兼容。

### `edition` 字段 {#the-edition-field}

`edition` 键是可选键，影响你的包使用哪个 [Rust Edition] 编译。在 `[package]` 中设置 `edition` 键会影响包中的所有目标/crate，包括测试套件、基准测试、二进制、示例等。

```toml
[package]
# ...
edition = '2024'
```

大多数清单的 `edition` 字段由 [`cargo new`] 自动填入最新稳定 edition。默认情况下，`cargo new` 目前会创建带有 2024 edition 的清单。

若 `Cargo.toml` 中不存在 `edition` 字段，则会为向后兼容假定为 2015 edition。注意所有用 [`cargo new`] 创建的清单都不会使用这一历史回退，因为它们会显式将 `edition` 指定为较新的值。

### `rust-version` 字段 {#the-rust-version-field}
`rust-version` 字段告诉 Cargo 你的包所支持的 Rust 工具链版本。
详见 [Rust 版本章节](02-rust-version/)。

### `description` 字段 {#the-description-field}

描述是关于该包的简短介绍。[crates.io] 会与你的包一起显示它。应为纯文本（非 Markdown）。

```toml
[package]
# ...
description = "A short description of my package"
```

> **注意**：[crates.io] 要求设置 `description`。

### `documentation` 字段 {#the-documentation-field}

`documentation` 字段指定托管该 crate 文档的网站 URL。若清单文件中未指定 URL，当文档已构建并可用时，[crates.io] 会自动将你的 crate 链接到对应的 [docs.rs] 页面（见 [docs.rs 队列][docs.rs queue]）。

```toml
[package]
# ...
documentation = "https://docs.rs/bitflags"
```

[docs.rs queue]: https://docs.rs/releases/queue

### `readme` 字段 {#the-readme-field}

`readme` 字段应为包根目录中某个文件的路径（相对于本 `Cargo.toml`），该文件包含关于该包的一般信息。
发布时该文件会传输到注册表。[crates.io]
会将其解释为 Markdown，并在 crate 页面上渲染。

```toml
[package]
# ...
readme = "README.md"
```

若未为此字段指定值，且包根目录中存在名为 `README.md`、
`README.txt` 或 `README` 的文件，则将使用该文件名。可通过将此字段设为
`false` 来抑制该行为。若字段设为 `true`，则假定默认值为 `README.md`。

### `homepage` 字段 {#the-homepage-field}

`homepage` 字段应为你的包主页站点的 URL。

```toml
[package]
# ...
homepage = "https://serde.rs"
```

仅当存在除源码仓库或 API 文档之外的专用网站时，才应为 `homepage` 设置值。不要让 `homepage` 与 `documentation` 或 `repository` 的值冗余。

### `repository` 字段 {#the-repository-field}

`repository` 字段应为你的包源码仓库的 URL。

```toml
[package]
# ...
repository = "https://github.com/rust-lang/cargo"
```

### `license` 与 `license-file` 字段 {#the-license-and-license-file-fields}

`license` 字段包含该包所发布软件许可证的名称。`license-file` 字段包含含有许可证文本的文件路径（相对于本 `Cargo.toml`）。

[crates.io] 将 `license` 字段解释为 [SPDX 2.3 许可证表达式][spdx-2.3-license-expressions]。名称必须是 [SPDX 许可证列表 3.20][spdx-license-list-3.20] 中的已知许可证。更多信息见 [SPDX 站点]。

SPDX 许可证表达式支持 AND 与 OR 运算符以组合多个许可证。[^slash]

```toml
[package]
# ...
license = "MIT OR Apache-2.0"
```

使用 `OR` 表示用户可选择任一许可证。使用 `AND` 表示用户必须同时遵守两个许可证。`WITH` 运算符表示带有特殊例外的许可证。一些示例：

* `MIT OR Apache-2.0`
* `LGPL-2.1-only AND MIT AND BSD-2-Clause`
* `GPL-2.0-or-later WITH Bison-exception-2.2`

若包使用非标准许可证，则可指定 `license-file` 字段以代替 `license` 字段。

```toml
[package]
# ...
license-file = "LICENSE.txt"
```

> **注意**：[crates.io] 要求设置 `license` 或 `license-file` 之一。

[^slash]: 以前可用 `/` 分隔多个许可证，但该用法已弃用。

### `keywords` 字段 {#the-keywords-field}

`keywords` 字段是描述该包的字符串数组。这有助于在注册表上搜索该包，你可以选择任何有助于他人找到该 crate 的词。

```toml
[package]
# ...
keywords = ["gamedev", "graphics"]
```

> **注意**：[crates.io] 最多允许 5 个关键字。每个关键字必须是
> ASCII 文本，最多 20 个字符，以字母数字字符开头，
> 且仅包含字母、数字、`_`、`-` 或 `+`。

### `categories` 字段 {#the-categories-field}

`categories` 字段是该包所属分类的字符串数组。

```toml
categories = ["command-line-utilities", "development-tools::cargo-plugins"]
```

> **注意**：[crates.io] 最多有 5 个分类。每个分类应
> 与 <https://crates.io/category_slugs> 上可用的字符串之一匹配，且
> 必须完全匹配。

### `workspace` 字段 {#the-workspace-field}

`workspace` 字段可用于配置该包将作为其成员的工作空间。若未指定，将推断为文件系统向上第一个带有 `[workspace]` 的 Cargo.toml。若成员不在工作空间根的子目录内，设置此项很有用。

```toml
[package]
# ...
workspace = "path/to/workspace/root"
```

若清单已定义 `[workspace]` 表，则不能指定该字段。也就是说，一个 crate 不能既是工作空间中的根 crate（包含 `[workspace]`），同时又是另一个工作空间的成员 crate（包含 `package.workspace`）。

更多信息见[工作空间章节](../02-workspaces/)。

### `build` 字段 {#the-build-field}

`build` 字段指定包根目录中用于构建本地代码的[构建脚本]文件。更多信息见[构建脚本指南][build script]。

[build script]: ../build-scripts/

```toml
[package]
# ...
build = "build.rs"
```

默认值为 `"build.rs"`，即从包根目录中名为 `build.rs` 的文件加载脚本。使用 `build = "custom_build_name.rs"` 可指定不同文件的路径，或使用 `build = false` 禁用构建脚本的自动检测。

### `links` 字段 {#the-links-field}

`links` 字段指定正在链接到的本地库名称。更多信息见构建脚本指南的 [`links`][links] 一节。

[links]: ../build-scripts/#the-links-manifest-key

例如，链接名为 "git2" 的本地库的 crate（例如 Linux 上的 `libgit2.a`）可以指定：

```toml
[package]
# ...
links = "git2"
```

### `exclude` 与 `include` 字段 {#the-exclude-and-include-fields}

`exclude` 与 `include` 字段可用于显式指定在打包项目以便[发布][publishing]时包含哪些文件，以及某些变更跟踪（见下文）。
`exclude` 字段中指定的模式标识一组不包含的文件，而 `include` 中的模式指定显式包含的文件。

```toml
[package]
# ...
exclude = ["/ci", "images/", ".*"]
```

```toml
[package]
# ...
include = ["/src", "COPYRIGHT", "/examples", "!/examples/big_example"]
```

> **注意：** 运行 [`cargo package --list`][`cargo package`]
> 可验证包中将包含哪些文件。

若两个字段都未指定，默认包含包根目录下的所有文件，但下文列出的排除项除外。

若未指定 `include`，则将排除以下文件：

* 若包不在 git 仓库中，所有以点开头的「隐藏」文件将被跳过。
* 若包在 git 仓库中，任何被仓库与全局 git 配置的 [gitignore] 规则忽略的文件将被跳过。

若指定了 `include`，
则不会应用仓库与全局 git 配置的 gitignore 规则。

无论是否指定了 `exclude` 或 `include`，以下文件始终被排除：

* 任何子包将被跳过（任何包含 `Cargo.toml` 文件的子目录）。
* 包根目录中名为 `target` 的目录将被跳过。

以下文件始终被包含：

* 包自身的 `Cargo.toml` 文件始终包含，无需在 `include` 中列出。
* 会自动包含一份精简的 `Cargo.lock`。
  详见 [`cargo package`]。
* 若指定了 [`license-file`](#the-license-and-license-file-fields)，它始终被包含。

这两个选项互斥；设置 `include` 会覆盖 `exclude`。若需要对一组 `include` 文件进行排除，请使用下文描述的 `!` 运算符。

模式应为 [gitignore] 风格的模式。简要说明：

- `foo` 匹配包中任何位置名为 `foo` 的文件或目录。这等价于模式 `**/foo`。
- `/foo` 仅匹配包根目录中名为 `foo` 的文件或目录。
- `foo/` 匹配包中任何位置名为 `foo` 的*目录*。
- 支持常见的 glob 模式如 `*`、`?` 与 `[]`：
  - `*` 匹配除 `/` 外的零个或多个字符。例如，`*.html`
    匹配包中任何位置带有 `.html` 扩展名的文件或目录。
  - `?` 匹配除 `/` 外的任意一个字符。例如，`foo?` 匹配 `food`，
    但不匹配 `foo`。
  - `[]` 允许匹配一段字符。例如，`[ab]`
    匹配 `a` 或 `b`。`[a-z]` 匹配字母 a 到 z。
- `**/` 前缀匹配任意目录。例如，`**/foo/bar` 匹配直接位于目录 `foo` 下任意位置的文件或目录 `bar`。
- `/**` 后缀匹配内部的一切。例如，`foo/**` 匹配目录 `foo` 内的所有文件，包括 `foo` 下子目录中的所有文件。
- `/**/` 匹配零个或多个目录。例如，`a/**/b` 匹配
  `a/b`、`a/x/b`、`a/x/y/b` 等。
- `!` 前缀否定一个模式。例如，模式 `src/*.rs` 与
  `!foo.rs` 会匹配 `src` 目录内所有带有 `.rs` 扩展名的文件，
  但名为 `foo.rs` 的文件除外。

在某些情况下，include/exclude 列表也用于变更跟踪。
对于用 `rustdoc` 构建的目标，它用于确定要跟踪的文件列表，以决定是否应重建该目标。若包有[构建脚本]且未发出任何 `rerun-if-*` 指令，则 include/exclude 列表用于跟踪：若这些文件中有任何变化，是否应重新运行构建脚本。

[gitignore]: https://git-scm.com/docs/gitignore

### `publish` 字段 {#the-publish-field}

`publish` 字段可用于控制该包可以发布到哪些注册表名称：
```toml
[package]
# ...
publish = ["some-registry-name"]
```

为防止包被误发布到注册表（如 crates.io），
例如为了在公司中保持包私有，
你可以省略 [`version`](#the-version-field) 字段。
若想更明确，可以禁用发布：
```toml
[package]
# ...
publish = false
```

若 publish 数组包含单个注册表，当未指定 `--registry` 标志时，`cargo publish` 命令将使用它。

### `metadata` 表 {#the-metadata-table}

默认情况下，Cargo 会对 `Cargo.toml` 中未使用的键发出警告，以帮助检测拼写错误等。然而，`package.metadata` 表会被 Cargo 完全忽略，且不会发出警告。本节可供希望在 `Cargo.toml` 中存储包配置的工具使用。例如：

```toml
[package]
name = "..."
# ...
# 例如生成 Android APK 时使用的元数据。
[package.metadata.android]
package-name = "my-awesome-android-app"
assets = "path/to/static"
```

你需要查看所用工具的文档以了解如何使用该字段。
对于使用 `package.metadata` 表的 Rust 项目，见：
- [docs.rs](https://docs.rs/about/metadata)

工作空间级别也有类似的表：
[`workspace.metadata`][workspace-metadata]。虽然 Cargo 并未规定这两个表内容的格式，但建议外部工具以一致的方式使用它们，例如在 `package.metadata` 缺少数据时引用 `workspace.metadata` 中的数据（若对该工具合理）。

[workspace-metadata]: ../02-workspaces/#the-metadata-table

### `default-run` 字段 {#the-default-run-field}

清单 `[package]` 节中的 `default-run` 字段可用于指定 [`cargo run`] 选择的默认二进制。例如，当同时存在 `src/bin/a.rs` 与 `src/bin/b.rs` 时：

```toml
[package]
default-run = "a"
```

## `[lints]` 节 {#the-lints-section}

通过在表中为不同工具的 lint 分配新级别，可覆盖其默认级别，例如：
```toml
[lints.rust]
unsafe_code = "forbid"
```

这是以下写法的简写：
```toml
[lints.rust]
unsafe_code = { level = "forbid", priority = 0 }
```

`level` 对应 `rustc` 中的 [lint 级别](https://doc.rust-lang.org/rustc/lints/levels.html)：
- `forbid`
- `deny`
- `warn`
- `allow`

`priority` 是一个有符号整数，控制哪些 lint 或 lint 组覆盖其他 lint 组：
- 较低（特别是负数）的数字优先级较低，会被较高数字覆盖，并且在传给 `rustc` 等工具的命令行上靠前出现

要知道某个特定 lint 属于 `[lints]` 下的哪张表，取 lint 名称中 `::` 之前的部分。若没有 `::`，则工具为 `rust`。例如关于 `unsafe_code` 的警告会是 `lints.rust.unsafe_code`，而关于 `clippy::enum_glob_use` 的 lint 会是 `lints.clippy.enum_glob_use`。

例如：
```toml
[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
enum_glob_use = "deny"
```

一般而言，这些只影响当前包的本地开发。
Cargo 仅将这些应用到当前包，而不应用到依赖。
至于依赖方，Cargo 会通过类似 [`--cap-lints`](https://doc.rust-lang.org/rustc/lints/levels.html#capping-lints) 的特性抑制非 path 依赖的 lint。

> **MSRV：** 自 1.74 起生效

## `[hints]` 节 {#the-hints-section}

`[hints]` 节允许为编译本包指定提示。Cargo 在编译本包时默认会尊重这些提示，不过正在构建的顶层包可通过 `[profile]` 机制覆盖这些值。按设计，提示始终可被 Cargo 安全忽略；若 Cargo 遇到不理解的提示，或理解提示但不理解其值，会发出警告但不会报错。因此，在 crate 中指定提示不会影响该 crate 的 MSRV。

个别提示可能关联不稳定的特性门控，你需要传入该门控才能应用它们所指定的配置；但若你未指定该不稳定特性门控，同样只会得到警告，而不是错误。

目前尚无稳定的提示。关于不稳定提示的信息，见 [hint-mostly-unused 文档](../17-unstable-features/#profile-hint-mostly-unused-option)。

> **MSRV：** 自 1.90 起生效。

## `[badges]` 节 {#the-badges-section}

`[badges]` 节用于指定状态徽章，可在包发布后于注册表网站上显示。

> 注意：[crates.io] 以前会在其网站上的 crate 旁显示徽章，但该功能已移除。包应将徽章放在其 README 文件中，该文件会在 [crates.io] 上显示（见 [`readme` 字段](#the-readme-field)）。

```toml
[badges]
# `maintenance` 表表示该 crate 的维护状态。注册表可能会使用它，
# 但 crates.io 目前未使用。更多细节见
# https://github.com/rust-lang/crates.io/issues/2437
# 与 https://github.com/rust-lang/crates.io/issues/2438。
# `status` 字段为必需。可用选项为：
# - `actively-developed`：正在添加新特性并修复 bug。
# - `passively-maintained`：没有新特性的计划，但维护者打算响应提交的 issue。
# - `as-is`：crate 功能已完整，维护者不打算继续开发或提供支持，
# 但对其设计用途仍然可用。
# - `experimental`：作者希望与社区分享，但不打算满足任何人的特定用例。
# - `looking-for-maintainer`：当前维护者希望将 crate 转让给他人。
# - `deprecated`：维护者不建议使用此 crate（crate 描述中可说明原因，
# 可能有更好的解决方案，或 crate 存在作者不想修复的问题）。
# - `none`：在 crates.io 上不显示徽章，因为维护者未选择说明其意图，
# 潜在用户需要自行调查。
maintenance = { status = "..." }
```

## 依赖节 {#dependency-sections}
关于 `[dependencies]`、`[dev-dependencies]`、
`[build-dependencies]` 以及目标特定的 `[target.*.dependencies]` 节的信息，见[指定依赖页面](../specifying-dependencies/)。

## `[profile.*]` 节 {#the-profile-sections}
`[profile]` 表提供了一种自定义编译器设置（如优化与调试设置）的方式。更多细节见[配置文件（Profiles）章节](../05-profiles/)。



[`cargo init`]: ../../cargo-commands/package-commands/01-cargo-init/
[`cargo new`]: ../../cargo-commands/package-commands/03-cargo-new/
[`cargo package`]: ../../cargo-commands/publishing-commands/04-cargo-package/
[`cargo run`]: ../../cargo-commands/build-commands/11-cargo-run/
[crates.io]: https://crates.io/
[docs.rs]: https://docs.rs/
[publishing]: ../../cargo-guide/09-publishing-on-crates-io/
[Rust Edition]: https://doc.rust-lang.org/edition-guide/index.html
[spdx-2.3-license-expressions]: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
[spdx-license-list-3.20]: https://github.com/spdx/license-list-data/tree/v3.20
[SPDX site]: https://spdx.org
[TOML]: https://toml.io/
