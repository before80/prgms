+++
title = "04-特性（Features）"
date = 2026-07-30T14:49:00+08:00
weight = 39
type = "docs"
description = "可选依赖与条件编译 features"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 特性（Features） {#features}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/features.html](https://doc.rust-lang.org/cargo/reference/features.html)


Cargo「特性」（features）提供了一种表达[条件编译][conditional compilation]与[可选依赖](#optional-dependencies)的机制。包在 `Cargo.toml` 的 `[features]` 表中定义一组命名特性，每个特性可被启用或禁用。正在构建的包的特性可用 `--features` 等命令行标志启用。依赖的特性可在 `Cargo.toml` 的依赖声明中启用。

> **注意**：现在在 crates.io 上发布的新 crate 或版本最多限制为 300 个特性。例外按个案批准。详见此[博文][blog post]。鼓励通过 crates.io Zulip 流参与解决方案讨论。

[blog post]: https://blog.rust-lang.org/2023/10/26/broken-badges-and-23k-keywords.html

另见 [Features 示例][Features Examples]章节，了解特性如何使用的一些示例。

[conditional compilation]: https://doc.rust-lang.org/reference/conditional-compilation.md
[Features Examples]: 01-features-examples/

## `[features]` 节 {#the-features-section}
特性在 `Cargo.toml` 的 `[features]` 表中定义。每个特性指定它启用的其他特性或可选依赖的数组。以下示例说明特性如何用于一个可选包含不同图像格式支持的 2D 图像处理库：

```toml
[features]
# 定义名为 `webp` 的特性，它不启用任何其他特性。
webp = []
```

定义此特性后，可用 [`cfg` 表达式][`cfg` expressions]有条件地在编译时包含支持所请求特性的代码。例如，包的 `lib.rs` 内可包含：

```rust
// 有条件地包含实现 WEBP 支持的模块。
#[cfg(feature = "webp")]
pub mod webp;
```

Cargo 使用 `rustc` 的 [`--cfg` 标志][`--cfg` flag]在包中设置特性，代码可用 [`cfg` 属性][`cfg` attribute]或 [`cfg` 宏][`cfg` macro]测试其是否存在。

特性可以列出要启用的其他特性。例如，ICO 图像格式可包含 BMP 与 PNG 图像，因此启用它时应确保那些其他特性也被启用：

```toml
[features]
bmp = []
png = []
ico = ["bmp", "png"]
webp = []
```

特性名称可包含 [Unicode XID 标准][Unicode XID standard]中的字符（包括大多数字母），另外允许以 `_` 或数字 `0` 到 `9` 开头，且在第一个字符之后还可包含 `-`、`+` 或 `.`。

> **注意**：[crates.io] 对特性名称语法施加额外约束，它们只能是 [ASCII 字母数字][ASCII alphanumeric]字符或 `_`、`-` 或 `+`。

[crates.io]: https://crates.io/
[Unicode XID standard]: https://unicode.org/reports/tr31/
[ASCII alphanumeric]: https://doc.rust-lang.org/std/primitive.char.html#method.is_ascii_alphanumeric
[`--cfg` flag]: https://doc.rust-lang.org/rustc/command-line-arguments.md#option-cfg
[`cfg` expressions]: https://doc.rust-lang.org/reference/conditional-compilation.md
[`cfg` attribute]: https://doc.rust-lang.org/reference/conditional-compilation.md#the-cfg-attribute
[`cfg` macro]: https://doc.rust-lang.org/std/macro.cfg.html

## `default` 特性 {#the-default-feature}

默认情况下，除非显式启用，所有特性都是禁用的。可通过指定 `default` 特性来更改：

```toml
[features]
default = ["ico", "webp"]
bmp = []
png = []
ico = ["bmp", "png"]
webp = []
```

构建包时，`default` 特性被启用，进而启用所列特性。此行为可通过以下方式更改：

* `--no-default-features` [命令行标志](#command-line-feature-options)禁用包的默认特性。
* 可在[依赖声明](#dependency-features)中指定 `default-features = false` 选项。

> **注意**：选择默认特性集时要小心。默认特性是一种便利，使使用包更容易，而无需强迫用户为常见用途仔细选择要启用的特性，但也有一些缺点。除非指定 `default-features = false`，依赖会自动启用默认特性。这会使确保默认特性未被启用变得困难，尤其是对于在依赖图中出现多次的依赖。每个包都必须确保指定了 `default-features = false` 以避免启用它们。
>
> 另一个问题是，从默认集中移除特性可能是 [SemVer 不兼容的变更](#semver-compatibility)，因此你应确信会保留那些特性。

## 可选依赖 {#optional-dependencies}

依赖可标记为「可选」，这意味着默认不会编译它们。例如，假设我们的 2D 图像处理库使用外部包处理 GIF 图像。可以这样表达：

```toml
[dependencies]
gif = { version = "0.11.1", optional = true }
```

默认情况下，此可选依赖隐式定义一个如下所示的特性：

```toml
[features]
gif = ["dep:gif"]
```

这意味着仅当启用 `gif` 特性时才会包含此依赖。代码中可使用相同的 `cfg(feature = "gif")` 语法，并且依赖可像任何特性一样启用，例如 `--features gif`（见下文[命令行特性选项](#command-line-feature-options)）。

在某些情况下，你可能不希望公开与可选依赖同名的特性。例如，也许可选依赖是内部细节，或者你想将多个可选依赖组合在一起，或者你只是想使用更好的名称。若你在 `[features]` 表的任何位置用 `dep:` 前缀指定可选依赖，则会禁用隐式特性。

> **注意**：`dep:` 语法仅从 Rust 1.60 起可用。以前的版本只能使用隐式特性名称。

例如，假设为了支持 AVIF 图像格式，我们的库需要启用两个其他依赖：

```toml
[dependencies]
ravif = { version = "0.6.3", optional = true }
rgb = { version = "0.8.25", optional = true }

[features]
avif = ["dep:ravif", "dep:rgb"]
```

在本例中，`avif` 特性将启用所列的两个依赖。这也避免创建隐式的 `ravif` 与 `rgb` 特性，因为我们不希望用户单独启用它们，它们是我们 crate 的内部细节。

> **注意**：可选包含依赖的另一种方式是使用[平台特定依赖][platform-specific dependencies]。这些不使用特性，而是基于目标平台有条件。

[platform-specific dependencies]: ../specifying-dependencies/#platform-specific-dependencies

## 依赖特性 {#dependency-features}

可在依赖声明中启用依赖的特性。`features` 键指示要启用哪些特性：

```toml
[dependencies]
# 启用 serde 的 `derive` 特性。
serde = { version = "1.0.118", features = ["derive"] }
```

可使用 `default-features = false` 禁用 [`default` 特性](#the-default-feature)：

```toml
[dependencies]
flate2 = { version = "1.0.3", default-features = false, features = ["zlib-rs"] }
```

> **注意**：这可能无法确保默认特性被禁用。若另一个依赖包含 `flate2` 而未指定 `default-features = false`，则默认特性将被启用。详见下文[特性统一](#feature-unification)。

也可在 `[features]` 表中启用依赖的特性。语法是 `"package-name/feature-name"`。例如：

```toml
[dependencies]
jpeg-decoder = { version = "0.1.20", default-features = false }

[features]
# 通过启用 jpeg-decoder 的 "rayon" 特性来启用并行处理支持。
parallel = ["jpeg-decoder/rayon"]
```

`"package-name/feature-name"` 语法也会在 `package-name` 是可选依赖时启用它。这通常不是你想要的。你可以像 `"package-name?/feature-name"` 一样添加 `?`，它仅在其他东西启用该可选依赖时才启用给定特性。

> **注意**：`?` 语法仅从 Rust 1.60 起可用。

例如，假设我们已为我们的库添加了一些序列化支持，并且它需要在一些可选依赖中启用对应特性。可以这样做：

```toml
[dependencies]
serde = { version = "1.0.133", optional = true }
rgb = { version = "0.8.25", optional = true }

[features]
serde = ["dep:serde", "rgb?/serde"]
```

在本例中，启用 `serde` 特性将启用 serde 依赖。它也将为 `rgb` 依赖启用 `serde` 特性，但仅当其他东西已启用 `rgb` 依赖时。

## 命令行特性选项 {#command-line-feature-options}

以下命令行标志可用于控制启用哪些特性：

* `--features` _FEATURES_：启用所列特性。多个特性可用逗号或空格分隔。若使用空格，从 shell 运行 Cargo 时请务必用引号括起所有特性（例如 `--features "foo bar"`）。若在[工作空间][workspace]中构建多个包，可用 `package-name/feature-name` 语法为特定工作空间成员指定特性。
* `--all-features`：激活命令行上所选所有包的所有特性。
* `--no-default-features`：不激活所选包的 [`default` 特性](#the-default-feature)。

**注意**：有关细节请查看各个子命令文档。并非所有标志对所有子命令都可用。

[workspace]: ../02-workspaces/

## 特性统一 {#feature-unification}

特性对于定义它们的包是唯一的。在一个包上启用特性不会在其他包上启用同名特性。

当依赖被多个包使用时，Cargo 在构建它时将使用该依赖上启用的所有特性的并集。这有助于确保仅使用依赖的单个副本。详见解析器文档的[特性一节][features section]。

例如，让我们看看使用[大量][winapi-features]特性的 [`winapi`] 包。若你的包依赖启用了 `winapi` 的 "fileapi" 与 "handleapi" 特性的包 `foo`，以及启用了 `winapi` 的 "std" 与 "winnt" 特性的另一依赖 `bar`，则 `winapi` 将在启用所有这四个特性的情况下构建。

![winapi 特性示例](../../images/winapi-features.svg)

[`winapi`]: https://crates.io/crates/winapi
[winapi-features]: https://github.com/retep998/winapi-rs/blob/0.3.9/Cargo.toml#L25-L431

其结果是特性应当是*累加的*。也就是说，启用特性不应禁用功能，并且启用任意特性组合通常应当是安全的。特性不应引入 [SemVer 不兼容的变更](#semver-compatibility)。

例如，若你想可选支持 [`no_std`] 环境，**不要**使用 `no_std` 特性。相反，使用*启用* `std` 的 `std` 特性。例如：

```rust
#![no_std]

#[cfg(feature = "std")]
extern crate std;

#[cfg(feature = "std")]
pub fn function_that_requires_std() {
    // ...
}
```

[`no_std`]: https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute
[features section]: ../specifying-dependencies/03-dependency-resolution/#features

### 互斥特性 {#mutually-exclusive-features}
在罕见情况下，特性可能彼此互不兼容。应尽可能避免这种情况，因为它要求依赖图中该包的所有使用者协作以避免一起启用它们。若不可能，考虑添加编译错误来检测此场景。例如：

```rust,ignore
#[cfg(all(feature = "foo", feature = "bar"))]
compile_error!("feature \"foo\" and feature \"bar\" cannot be enabled at the same time");
```

不要使用互斥特性，考虑其他一些选项：

* 将功能拆分为单独的包。
* 当存在冲突时，[优先选择一个特性][feature-precedence]。[`cfg-if`] 包可帮助编写更复杂的 `cfg` 表达式。
* 将代码架构设计为允许同时启用特性，并用运行时选项控制使用哪一个。例如，使用配置文件、命令行参数或环境变量来选择启用哪种行为。

[`cfg-if`]: https://crates.io/crates/cfg-if
[feature-precedence]: 01-features-examples/#feature-precedence

### 检查已解析的特性 {#inspecting-resolved-features}

在复杂的依赖图中，有时很难理解不同特性如何在各个包上启用。[`cargo tree`] 命令提供若干选项以帮助检查与可视化启用了哪些特性。可尝试的一些选项：

* `cargo tree -e features`：这将在依赖图中显示特性。每个特性将显示是哪个包启用了它。
* `cargo tree -f "{p} {f}"`：这是更紧凑的视图，显示每个包上启用的逗号分隔特性列表。
* `cargo tree -e features -i foo`：这将反转树，显示特性如何流入给定包 "foo"。这可能很有用，因为查看整个图可能相当大且令人不知所措。当你试图弄清特定包上启用了哪些特性以及为什么时使用此选项。关于如何阅读，见 [`cargo tree`] 页面底部的示例。

[`cargo tree`]: ../../cargo-commands/manifest-commands/08-cargo-tree/

## 特性解析器版本 2 {#feature-resolver-version-2}

可用 `Cargo.toml` 中的 `resolver` 字段指定不同的特性解析器，像这样：

```toml
[package]
name = "my-package"
version = "1.0.0"
resolver = "2"
```

关于指定解析器版本的更多细节，见[解析器版本][resolver versions]一节。

版本 `"2"` 解析器在一些统一可能不受欢迎的情况下避免统一特性。确切情况在[解析器章节][resolver-v2]中描述，但简而言之，它在这些情况下避免统一：

* 为当前未构建的[目标架构][target]启用的[平台特定依赖][platform-specific dependencies]上的特性会被忽略。
* [构建依赖][Build-dependencies]与 proc-macros 不与普通依赖共享特性。
* [开发依赖][Dev-dependencies]不会激活特性，除非正在构建需要它们的 [Cargo 目标][target]（如测试或示例）。

在某些情况下必须避免统一。例如，若构建依赖启用 `std` 特性，且同一依赖在 `no_std` 环境中用作普通依赖，启用 `std` 会破坏构建。

然而，一个缺点是这可能增加构建时间，因为依赖被构建多次（每次带有不同特性）。使用版本 `"2"` 解析器时，建议检查被构建多次的依赖以减少总体构建时间。若*不需要*用单独特性构建那些重复的包，考虑将特性添加到[依赖声明](#dependency-features)的 `features` 列表中，使重复项最终具有相同特性（从而 Cargo 只构建它一次）。你可用 [`cargo tree --duplicates`][`cargo tree`] 命令检测这些重复依赖。它将显示哪些包被构建多次；查找以相同版本列出的任何条目。关于获取已解析特性信息的更多内容，见[检查已解析的特性](#inspecting-resolved-features)。对于构建依赖，若你使用 `--target` 标志进行交叉编译，则这不是必需的，因为在该场景中构建依赖始终与普通依赖分开构建。

[target]: ../../appendix/01-glossary/#target

### 解析器版本 2 命令行标志 {#resolver-version-2-command-line-flags}
`resolver = "2"` 设置也会更改 `--features` 与 `--no-default-features` [命令行选项](#command-line-feature-options)的行为。

对于版本 `"1"`，你只能为当前工作目录中的包启用特性。例如，在有包 `foo` 与 `bar` 的工作空间中，你在包 `foo` 的目录中，并运行命令 `cargo build -p bar --features bar-feat`，这将失败，因为 `--features` 标志只允许在 `foo` 上启用特性。

使用 `resolver = "2"` 时，特性标志允许为用 `-p` 与 `--workspace` 标志在命令行上选择的任何包启用特性。例如：

```sh
# 此命令在 resolver = "2" 时允许，无论你在哪个目录中。
cargo build -p foo -p bar --features foo-feat,bar-feat

# 此显式等价形式适用于任何解析器版本：
cargo build -p foo -p bar --features foo/foo-feat,bar/bar-feat
```

此外，对于 `resolver = "1"`，`--no-default-features` 标志仅禁用当前目录中包的默认特性。对于版本 "2"，它将禁用所有工作空间成员的默认特性。

[resolver versions]: ../specifying-dependencies/03-dependency-resolution/#resolver-versions
[build-dependencies]: ../specifying-dependencies/#build-dependencies
[Build-dependencies]: ../specifying-dependencies/#build-dependencies
[dev-dependencies]: ../specifying-dependencies/#development-dependencies
[Dev-dependencies]: ../specifying-dependencies/#development-dependencies
[resolver-v2]: ../specifying-dependencies/03-dependency-resolution/#feature-resolver-version-2

## 构建脚本 {#build-scripts}
[构建脚本][Build scripts]可通过检查 `CARGO_FEATURE_<name>` 环境变量来检测包上启用了哪些特性，其中 `<name>` 是转换为大写且 `-` 转换为 `_` 的特性名称。

[build scripts]: ../build-scripts/
[Build scripts]: ../build-scripts/

## 所需特性 {#required-features}
[`required-features` 字段][`required-features` field]可用于在特性未启用时禁用特定 [Cargo 目标][Cargo targets]。更多细节见链接的文档。

[`required-features` field]: ../the-manifest-format/01-cargo-targets/#the-required-features-field
[Cargo targets]: ../the-manifest-format/01-cargo-targets/

## SemVer 兼容性 {#semver-compatibility}

启用特性不应引入 SemVer 不兼容的变更。例如，特性不应以可能破坏现有用法的方式更改现有 API。关于什么变更是兼容的更多细节，见 [SemVer 兼容性章节](../13-semver-compatibility/)。

添加与移除特性定义和可选依赖时应谨慎，因为这些有时可能是向后不兼容的变更。更多细节见 SemVer 兼容性章节的 [Cargo 一节](../13-semver-compatibility/#cargo)。简而言之，遵循这些规则：

* 以下在次版本发布中通常是安全的：
  * 添加[新特性][cargo-feature-add]或[可选依赖][cargo-dep-add]。
  * [更改依赖上使用的特性][cargo-change-dep-feature]。
* 以下在次版本发布中通常**不应**做：
  * [移除特性][cargo-feature-remove]或[可选依赖][cargo-remove-opt-dep]。
  * [将现有公共代码移到特性后面][item-remove]。
  * [从特性列表中移除特性][cargo-feature-remove-another]。

见链接了解注意事项与示例。

[cargo-change-dep-feature]: ../13-semver-compatibility/#cargo-change-dep-feature
[cargo-dep-add]: ../13-semver-compatibility/#cargo-dep-add
[cargo-feature-add]: ../13-semver-compatibility/#cargo-feature-add
[item-remove]: ../13-semver-compatibility/#item-remove
[cargo-feature-remove]: ../13-semver-compatibility/#cargo-feature-remove
[cargo-remove-opt-dep]: ../13-semver-compatibility/#cargo-remove-opt-dep
[cargo-feature-remove-another]: ../13-semver-compatibility/#cargo-feature-remove-another

## 特性文档与发现 {#feature-documentation-and-discovery}
鼓励你记录包中有哪些可用特性。这可通过在 `lib.rs` 顶部添加[文档注释][doc comments]来完成。作为一个示例，见 [regex crate 源码][regex crate source]，渲染后可在 [docs.rs][regex-docs-rs] 上查看。若你有其他文档，如用户指南，考虑在那里添加文档（例如见 [serde.rs]）。若你有二进制项目，考虑在 README 或项目的其他文档中记录特性（例如见 [sccache]）。

清晰地记录特性可设定关于被视为「不稳定」或不应用的特性的期望。例如，若有可选依赖，但你不希望用户将该可选依赖显式列为特性，则将其排除在文档列表之外。

发布在 [docs.rs] 上的文档可在 `Cargo.toml` 中使用元数据来控制构建文档时启用哪些特性。详见 [docs.rs 元数据文档][docs.rs metadata documentation]。

> **注意**：Rustdoc 有实验性支持，可注解文档以指示使用某些 API 需要哪些特性。详见 `doc_cfg` 文档。一个示例是 [`syn` 文档][`syn` documentation]，你可以看到注明使用它需要哪些特性的彩色框。

[docs.rs metadata documentation]: https://docs.rs/about/metadata
[docs.rs]: https://docs.rs/
[serde.rs]: https://serde.rs/feature-flags.html
[doc comments]: https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html
[regex crate source]: https://github.com/rust-lang/regex/blob/1.4.2/src/lib.rs#L488-L583
[regex-docs-rs]: https://docs.rs/regex/1.4.2/regex/#crate-features
[sccache]: https://github.com/mozilla/sccache/blob/0.2.13/README.md#build-requirements
[`syn` documentation]: https://docs.rs/syn/1.0.54/syn/#modules

### 发现特性 {#discovering-features}
当特性在库 API 中有文档时，这可使你的用户更容易发现哪些特性可用以及它们做什么。若包的特性文档不易获得，你可以查看 `Cargo.toml` 文件，但有时可能很难找到。[crates.io] 上的 crate 页面有指向源码仓库的链接（若可用）。像 [`cargo vendor`] 或 [cargo-clone-crate] 这样的工具可用于下载源码并检查它。

[`cargo vendor`]: ../../cargo-commands/manifest-commands/10-cargo-vendor/
[cargo-clone-crate]: https://crates.io/crates/cargo-clone-crate

## 特性组合 {#feature-combinations}
因为特性是一种条件编译形式，要 100% 覆盖需要指数数量的配置与测试用例。默认情况下，测试、文档以及像 [Clippy](https://github.com/rust-lang/rust-clippy) 这样的其他工具将仅以默认特性集运行。

我们鼓励你考虑关于不同特性组合的策略与工具——每个项目在时间、资源以及覆盖特定场景的成本收益方面都会有不同要求。常见配置可能是带有/不带有默认特性、特定特性组合，或所有特性组合。
