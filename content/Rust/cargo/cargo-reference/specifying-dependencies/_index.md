+++
title = "03-指定依赖"
date = 2026-07-30T14:49:00+08:00
weight = 35
type = "docs"
description = "版本需求、git/path/registry 依赖写法"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 指定依赖 {#specifying-dependencies}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)


你的 crate 可以依赖来自 [crates.io] 或其他注册表、`git` 仓库，或本地文件系统子目录的其他库。你也可以临时覆盖依赖的位置——例如，以便测试你在本地修复的依赖中的 bug。你可以为不同平台设置不同的依赖，以及仅在开发期间使用的依赖。让我们看看如何分别做到这些。

## 指定来自 crates.io 的依赖 {#specifying-dependencies-from-cratesio}
默认情况下，Cargo 配置为在 [crates.io] 上查找依赖。此时只需要名称与版本字符串。在 [Cargo 指南](../../cargo-guide/)中，我们指定了对 `time` crate 的依赖：

```toml
[dependencies]
time = "0.1.12"
```

版本字符串 `"0.1.12"` 称为[版本需求](#version-requirement-syntax)。
它指定了在[解析依赖](03-dependency-resolution/)时可从中选择的版本范围。
在本例中，`"0.1.12"` 表示版本范围 `>=0.1.12, <0.2.0`。
若更新落在该范围内则允许。
在本例中，若我们运行 `cargo update time`，cargo 应
在其为最新的 `0.1.z` 发布时将我们更新到 `0.1.13`，但不会
更新到 `0.2.0`。

## 版本需求语法 {#version-requirement-syntax}

### 默认需求 {#default-requirements}
**默认需求**指定一个最低版本，并允许更新到 [SemVer] 兼容的版本。
若最左侧非零的主/次/补丁组成部分相同，则版本被视为兼容。
这与 [SemVer] 不同：SemVer 认为所有 1.0.0 之前的包都不兼容。

`1.2.3` 是默认需求的一个示例。

```notrust
1.2.3  :=  >=1.2.3, <2.0.0
1.2    :=  >=1.2.0, <2.0.0
1      :=  >=1.0.0, <2.0.0
0.2.3  :=  >=0.2.3, <0.3.0
0.2    :=  >=0.2.0, <0.3.0
0.0.3  :=  >=0.0.3, <0.0.4
0.0    :=  >=0.0.0, <0.1.0
0      :=  >=0.0.0, <1.0.0
```

### Caret 需求 {#caret-requirements}
**Caret 需求**是默认的版本需求策略。
此版本策略允许 [SemVer] 兼容的更新。
它们指定为带有前导插入符（`^`）的版本需求。

`^1.2.3` 是 caret 需求的一个示例。

省略插入符是使用 caret 需求的简化等价语法。
虽然 caret 需求是默认的，但建议在可能时使用简化语法。

`log = "^1.2.3"` 与 `log = "1.2.3"` 完全等价。

### Tilde 需求 {#tilde-requirements}
**Tilde 需求**指定一个最低版本，并允许一定程度的更新。
若你指定了主、次与补丁版本，或仅指定了主与次版本，则仅允许补丁级变更。若你仅指定了主版本，则允许次与补丁级变更。

`~1.2.3` 是 tilde 需求的一个示例。

```notrust
~1.2.3  := >=1.2.3, <1.3.0
~1.2    := >=1.2.0, <1.3.0
~1      := >=1.0.0, <2.0.0
```

### 通配符需求 {#wildcard-requirements}
**通配符需求**允许通配符所在位置的任意版本。

`*`、`1.*` 与 `1.2.*` 是通配符需求的示例。

```notrust
*     := >=0.0.0
1.*   := >=1.0.0, <2.0.0
1.2.* := >=1.2.0, <1.3.0
```

> **注意**：[crates.io] 不允许裸 `*` 版本。

### 比较需求 {#comparison-requirements}
**比较需求**允许手动指定版本范围或精确版本。

以下是一些比较需求的示例：

```notrust
>= 1.2.0
> 1
< 2
= 1.2.3
```

<span id="multiple-requirements"></span>
### 多个版本需求 {#multiple-version-requirements}
如上例所示，多个版本需求可用逗号分隔，例如 `>= 1.2, < 1.5`。
所有需求都必须满足，
因此像 `<1.2, ^1.2.2` 这样不重叠的需求会导致没有匹配的版本。

### 预发布版 {#pre-releases}
除非特别要求，版本需求会排除[预发布版本](../the-manifest-format/#the-version-field)，例如 `1.0.0-alpha`。
例如，若包 `foo` 发布了 `1.0.0-alpha`，则需求 `foo = "1.0"` *不会*匹配，并将返回错误。必须指定预发布版，例如 `foo = "1.0.0-alpha"`。
类似地，除非显式要求安装预发布版，[`cargo install`] 也会避开预发布版。

Cargo 允许自动使用「更新」的预发布版。例如，若发布了 `1.0.0-beta`，则需求 `foo = "1.0.0-alpha"` 将允许更新到 `beta` 版本。注意这仅在同一发布版本上有效，`foo = "1.0.0-alpha"` 不允许更新到 `foo = "1.0.1-alpha"` 或 `foo = "1.0.1-beta"`。

Cargo 也会自动从预发布版升级到 semver 兼容的已发布版本。需求 `foo = "1.0.0-alpha"` 将允许更新到 `foo = "1.0.0"` 以及 `foo = "1.2.0"`。

请注意预发布版本可能不稳定，因此使用时应谨慎。某些项目可能选择在预发布版本之间发布破坏性变更。若你的库本身不是预发布版，建议不要在库中使用预发布依赖。更新 `Cargo.lock` 时也应谨慎，并准备好应对预发布更新导致的问题。

[`cargo install`]: ../../cargo-commands/package-commands/02-cargo-install/

### 版本元数据 {#version-metadata}
[版本元数据](../the-manifest-format/#the-version-field)，例如 `1.0.0+21AF26D3`，会被忽略，且不应在版本需求中使用。

> **建议：** 有疑问时，使用默认的版本需求运算符。
>
> 在罕见情况下，带有「公共依赖」
> （重新导出该依赖或在其公共 API 中与之互操作）
> 且与多个 semver 不兼容版本兼容的包
> （例如仅使用在发布之间未更改的简单类型，如 `Id`）
> 可能支持用户选择使用「公共依赖」的哪个版本。
> 在这种情况下，像 `">=0.4, <2"` 这样的版本需求可能值得关注。
> *然而*，该包的用户很可能会遇到错误，并需要
> 通过 `cargo update` 手动选择「公共依赖」的版本，若
> 他们也依赖它——因为 Cargo 在[解析依赖版本](03-dependency-resolution/)时可能为「公共依赖」挑选不同版本（见
> [#10599]）。
>
> 避免将版本上界约束为小于下一个 semver 不兼容版本的任何值
> （例如避免 `">=2.0, <2.4"`、`"2.0.*"` 或 `~2.0`），
> 因为依赖树中的其他包可能
> 需要更新的版本，从而导致无法解析的错误（见 [#9029]）。
> 考虑在你的 [`Cargo.lock`] 中控制版本是否更合适。
>
> 在某些情况下这无关紧要，或收益可能超过成本，包括：
> - 当没有其他人依赖你的包时；例如它只有一个 `[[bin]]`
> - 当依赖预发布包并希望避免破坏性变更时，则可能需要完全指定的 `"=1.2.3-alpha.3"`（见
>   [#2222]）
> - 当库重新导出 proc-macro，但该 proc-macro 生成的代码会
>   回调到重新导出库时，则可能需要完全指定的 `=1.2.3`，
>   以确保 proc-macro 不新于重新导出库，
>   且不会生成使用当前版本中不存在的 API 部分的代码

[`Cargo.lock`]: ../../cargo-guide/06-cargo-toml-vs-cargo-lock/
[#2222]: https://github.com/rust-lang/cargo/issues/2222
[#9029]: https://github.com/rust-lang/cargo/issues/9029
[#10599]: https://github.com/rust-lang/cargo/issues/10599

## 指定来自其他注册表的依赖 {#specifying-dependencies-from-other-registries}
要指定来自 [crates.io] 以外注册表的依赖，将 `registry` 键设为要使用的注册表名称：

```toml
[dependencies]
some-crate = { version = "1.0", registry = "my-registry" }
```

其中 `my-registry` 是在 `.cargo/config.toml` 文件中配置的注册表名称。
更多信息见[注册表文档][registries documentation]。

> **注意**：[crates.io] 不允许发布带有对发布在 [crates.io] 之外的代码之依赖的包。

[registries documentation]: ../registries/

## 指定来自 `git` 仓库的依赖 {#specifying-dependencies-from-git-repositories}

要依赖位于 `git` 仓库中的库，你需要指定的最少信息是带有 `git` 键的仓库位置：

```toml
[dependencies]
regex = { git = "https://github.com/rust-lang/regex.git" }
```

Cargo 会获取该位置的 `git` 仓库，并遍历文件树，在 `git` 仓库内的任意位置查找所请求 crate 的 `Cargo.toml` 文件。
例如，`regex-lite` 与 `regex-syntax` 是 `rust-lang/regex` 仓库的成员，
可通过仓库的根 URL（`https://github.com/rust-lang/regex.git`）引用，
无论它们在文件树中的位置如何。

```toml
regex-lite   = { git = "https://github.com/rust-lang/regex.git" }
regex-syntax = { git = "https://github.com/rust-lang/regex.git" }
```

上述规则不适用于 [`path` 依赖](#specifying-path-dependencies)。

### 选择提交 {#choice-of-commit}
若我们仅指定仓库 URL（如上例），Cargo 假定我们打算使用默认分支上的最新提交来构建我们的包。

你可以将 `git` 键与 `rev`、`tag` 或 `branch` 键组合，以更具体地说明使用哪个提交。以下是使用名为 `next` 的分支上最新提交的示例：

```toml
[dependencies]
regex = { git = "https://github.com/rust-lang/regex.git", branch = "next" }
```

不是分支或标签的任何内容都属于 `rev` 键。这可以是提交哈希，如 `rev = "4c59b707"`，或远程仓库公开的命名引用，如 `rev = "refs/pull/493/head"`。

`rev` 键可用的引用因仓库托管位置而异。
GitHub 会为每个 pull request 的最新提交公开一个引用，如上例所示。
其他 git 主机可能在不同的命名方案下提供等价内容。

**更多 `git` 依赖示例：**

```toml
# 若主机接受此类 URL，则可省略 .git 后缀——两个示例效果相同
regex = { git = "https://github.com/rust-lang/regex" }
regex = { git = "https://github.com/rust-lang/regex.git" }

# 带有特定标签的提交
regex = { git = "https://github.com/rust-lang/regex.git", tag = "1.10.3" }

# 按其 SHA1 哈希指定的提交
regex = { git = "https://github.com/rust-lang/regex.git", rev = "0c0990399270277832fbb5b91a1fa118e6f63dba" }

# PR 493 的 HEAD 提交
regex = { git = "https://github.com/rust-lang/regex.git", rev = "refs/pull/493/head" }

# 无效示例
# 在 # 后指定提交会忽略提交 ID 并生成警告
regex = { git = "https://github.com/rust-lang/regex.git#4c59b70" }

# git 与 path 不能同时使用
regex = { git = "https://github.com/rust-lang/regex.git#4c59b70", path = "../regex" }
```

Cargo 在添加 `git` 依赖时会将其提交锁定在 `Cargo.lock` 文件中，仅在你运行 `cargo update` 命令时检查更新。

### `version` 键的作用 {#the-role-of-the-version-key}
`version` 键始终意味着该包可在注册表中获得，无论是否存在 `git` 或 `path` 键。

`version` 键*不会*影响 Cargo 获取 `git` 依赖时使用哪个提交，但 Cargo 会对照 `version` 键检查依赖 `Cargo.toml` 文件中的版本信息，若检查失败则报错。

在本例中，Cargo 从 Git 获取名为 `next` 的分支的 HEAD 提交，并检查该 crate 的版本是否与 `version = "1.10.3"` 兼容：

```toml
[dependencies]
regex = { version = "1.10.3", git = "https://github.com/rust-lang/regex.git", branch = "next" }
```

`version`、`git` 与 `path` 键被视为解析依赖的独立位置。
详见下文[多个位置](#multiple-locations)一节。

> **注意**：[crates.io] 不允许发布带有对发布在 [crates.io] 本身之外的代码之依赖的包
> （[dev-dependencies] 会被忽略）。关于 `git` 与 `path` 依赖的回退替代方案，见[多个位置](#multiple-locations)一节。

### Git 子模块 {#git-submodules}
克隆 `git` 依赖时，
Cargo 会自动递归获取其子模块，
以便构建所需的所有代码都可用。

要跳过获取与构建无关的子模块，
可在依赖仓库的 `.gitmodules` 中设置 [`submodule.<name>.update = none`][submodule-update]。
这需要对仓库的写访问权限，并会更广泛地禁用子模块更新。

[submodule-update]: https://git-scm.com/docs/gitmodules#Documentation/gitmodules.txt-submodulenameupdate

### 访问私有 Git 仓库 {#accessing-private-git-repositories}
关于私有仓库的 Git 身份验证帮助，见 [Git 身份验证](../../appendix/02-git-authentication/)。

## 指定 path 依赖 {#specifying-path-dependencies}

随着时间推移，我们在[指南](../../cargo-guide/)中的 `hello_world` 包已经显著增大！已经到了我们可能希望拆分出一个单独的 crate 供他人使用的程度。为此，Cargo 支持 **path 依赖**，它们通常是同一仓库内的子 crate。让我们从在 `hello_world` 包内创建一个新 crate 开始：

```console
# 在 hello_world/ 内
$ cargo new hello_utils
```

这将创建一个新文件夹 `hello_utils`，其中 `Cargo.toml` 与 `src` 文件夹已准备好配置。要告诉 Cargo 这件事，打开 `hello_world/Cargo.toml` 并将 `hello_utils` 添加到你的依赖中：

```toml
[dependencies]
hello_utils = { path = "hello_utils" }
```

这告诉 Cargo 我们依赖一个名为 `hello_utils` 的 crate，它位于相对于写入该声明的 `Cargo.toml` 文件的 `hello_utils` 文件夹中。

下一次 `cargo build` 将自动构建 `hello_utils` 及其所有依赖。

### 无本地路径遍历 {#no-local-path-traversal}
本地路径必须指向带有依赖 `Cargo.toml` 的确切文件夹。
与 `git` 依赖不同，Cargo 不会遍历本地路径。
例如，若 `regex-lite` 与 `regex-syntax` 是本地克隆的 `rust-lang/regex` 仓库的成员，则必须用完整路径引用它们：

```toml
# git 键接受仓库根 URL，Cargo 会遍历树以查找 crate
[dependencies]
regex-lite   = { git = "https://github.com/rust-lang/regex.git" }
regex-syntax = { git = "https://github.com/rust-lang/regex.git" }

# path 键要求本地路径中包含成员名称
[dependencies]
regex-lite   = { path = "../regex/regex-lite" }
regex-syntax = { path = "../regex/regex-syntax" }
```

### 已发布 crate 中的本地路径 {#local-paths-in-published-crates}
仅用 path 指定依赖的 crate 不允许出现在 [crates.io] 上。

若我们想发布 `hello_world` crate，
我们需要将 `hello_utils` 的某个版本作为单独的 crate 发布到 [crates.io]，
并在 `hello_world` 的依赖行中指定其版本：

```toml
[dependencies]
hello_utils = { path = "hello_utils", version = "0.1.0" }
```

同时使用 `path` 与 `version` 键在[多个位置](#multiple-locations)一节中有说明。

> **注意**：[crates.io] 不允许发布带有对 [crates.io] 之外代码之依赖的包，[dev-dependencies] 除外。
> 关于 `git` 与 `path` 依赖的回退替代方案，见[多个位置](#multiple-locations)一节。

## 多个位置 {#multiple-locations}

可以同时指定注册表版本与 `git` 或 `path` 位置。本地将使用 `git` 或 `path` 依赖（此时会对照本地副本检查 `version`），而当发布到像 [crates.io] 这样的注册表时，将使用注册表版本。不允许其他组合。示例：

```toml
[dependencies]
# 本地使用时用 `my-bitflags`，发布时
# 使用 crates.io 上的版本 1.0。
bitflags = { path = "my-bitflags", version = "1.0" }

# 本地使用时用给定的 git 仓库，发布时
# 使用 crates.io 上的版本 1.0。
smallvec = { git = "https://github.com/servo/rust-smallvec.git", version = "1.0" }

# 注意：若版本不匹配，Cargo 将无法编译！
```

一个有用的例子是：你已将一个库拆分为同一工作空间内的多个包。然后你可以使用 `path` 依赖指向工作空间内的本地包，以便在开发期间使用本地版本，一旦发布则使用 [crates.io] 版本。这类似于指定[覆盖](01-overriding-dependencies/)，但仅适用于这一条依赖声明。

## 平台特定依赖 {#platform-specific-dependencies}

平台特定依赖采用相同格式，但列在 `target` 节下。通常会使用类似 Rust 的 [`#[cfg]` 语法](https://doc.rust-lang.org/reference/conditional-compilation.html)来定义这些节：

```toml
[target.'cfg(windows)'.dependencies]
winhttp = "0.4.0"

[target.'cfg(unix)'.dependencies]
openssl = "1.0.1"

[target.'cfg(target_arch = "x86")'.dependencies]
native-i686 = { path = "native/i686" }

[target.'cfg(target_arch = "x86_64")'.dependencies]
native-x86_64 = { path = "native/x86_64" }
```

与 Rust 一样，此处的语法支持 `not`、`any` 与 `all` 运算符以组合各种 cfg 名/值对。

若想知道你的平台上有哪些 cfg 目标可用，从命令行运行 `rustc --print=cfg`。若想知道另一平台（例如 64 位 Windows）有哪些 `cfg` 目标可用，运行 `rustc --print=cfg --target=x86_64-pc-windows-msvc`。

与 Rust 源码不同，你不能使用
`[target.'cfg(feature = "fancy-feature")'.dependencies]` 基于可选特性添加依赖。请改用 [`[features]` 节](../features/)：

```toml
[dependencies]
foo = { version = "1.0", optional = true }
bar = { version = "1.0", optional = true }

[features]
fancy-feature = ["foo", "bar"]
```

同样适用于 `cfg(debug_assertions)`、`cfg(test)` 与 `cfg(proc_macro)`。
这些值不会按预期工作，并将始终具有 `rustc --print=cfg` 返回的默认值。
目前无法基于这些配置值添加依赖。

除 `#[cfg]` 语法外，Cargo 还支持列出依赖将适用的完整目标：

```toml
[target.x86_64-pc-windows-gnu.dependencies]
winhttp = "0.4.0"

[target.i686-unknown-linux-gnu.dependencies]
openssl = "1.0.1"
```

### 自定义目标规格 {#custom-target-specifications}
若你正在使用自定义目标规格（例如 `--target foo/bar.json`），请使用不含 `.json` 扩展名的基本文件名：

```toml
[target.bar.dependencies]
winhttp = "0.4.0"

[target.my-special-i686-platform.dependencies]
openssl = "1.0.1"
native = { path = "native/i686" }
```

> **注意**：自定义目标规格在稳定通道上不可用。

## 开发依赖 {#development-dependencies}

你可以向 `Cargo.toml` 添加格式与 `[dependencies]` 等价的 `[dev-dependencies]` 节：

```toml
[dev-dependencies]
tempdir = "0.3"
```

Dev-dependencies 在为构建而编译包时不使用，但用于编译测试、示例与基准测试。

这些依赖*不会*传播到依赖本包的其他包。

你也可以通过在目标节标题中使用 `dev-dependencies` 而非 `dependencies` 来拥有目标特定的开发依赖。例如：

```toml
[target.'cfg(unix)'.dev-dependencies]
mio = "0.0.1"
```

> **注意**：发布包时，仅指定了 `version` 的 dev-dependencies 会包含在已发布的 crate 中。对于大多数用例，发布时不需要 dev-dependencies，不过某些用户（如操作系统打包者）可能希望在 crate 内运行测试，因此尽可能提供 `version` 仍可能有益。

## 构建依赖 {#build-dependencies}

你可以依赖其他基于 Cargo 的 crate 以在构建脚本中使用。
依赖通过清单的 `build-dependencies` 节声明：

```toml
[build-dependencies]
cc = "1.0.3"
```


你也可以通过在目标节标题中使用 `build-dependencies` 而非 `dependencies` 来拥有目标特定的构建依赖。例如：

```toml
[target.'cfg(unix)'.build-dependencies]
cc = "1.0.3"
```

在这种情况下，仅当宿主平台匹配指定目标时才会构建该依赖。

构建脚本**无法**访问列在 `dependencies` 或 `dev-dependencies` 节中的依赖。同样，构建依赖也不会对包本身可用，除非也列在 `dependencies` 节下。包本身与其构建脚本是分开构建的，因此它们的依赖不必一致。通过为独立目的使用独立依赖，Cargo 保持更简单、更干净。

## 选择特性 {#choosing-features}
若你依赖的包提供条件特性，你可以指定要使用哪些：

```toml
[dependencies.awesome]
version = "1.3.5"
default-features = false # 不包含默认特性，并可选择性地
                         # 挑选个别特性
features = ["secure-password", "civet"]
```

关于特性的更多信息见[特性章节](../features/#dependency-features)。

## 在 `Cargo.toml` 中重命名依赖 {#renaming-dependencies-in-cargotoml}
在 `Cargo.toml` 中编写 `[dependencies]` 节时，你为依赖写的键通常与代码中导入的 crate 名称匹配。但对某些项目，你可能希望在代码中用不同名称引用 crate，无论它在 crates.io 上如何发布。例如你可能希望：

* 避免在 Rust 源码中需要 `use foo as bar`。
* 依赖同一 crate 的多个版本。
* 依赖来自不同注册表的同名 crate。

为支持这一点，Cargo 在 `[dependencies]` 节中支持 `package` 键，用于指定应依赖哪个包：

```toml
[package]
name = "mypackage"
version = "0.0.1"

[dependencies]
foo = "0.1"
bar = { git = "https://github.com/example/project.git", package = "foo" }
baz = { version = "0.1", registry = "custom", package = "foo" }
```

在本例中，你的 Rust 代码中现在有三个 crate 可用：

```rust,ignore
extern crate foo; // crates.io
extern crate bar; // git 仓库
extern crate baz; // 注册表 `custom`
```

这三个 crate 在它们自己的 `Cargo.toml` 中的包名都是 `foo`，因此我们显式使用 `package` 键告知 Cargo：即使我们在本地用其他名称调用它，我们也想要 `foo` 包。若未指定，`package` 键默认为所请求依赖的名称。

注意若你有可选依赖，例如：

```toml
[dependencies]
bar = { version = "0.1", package = 'foo', optional = true }
```

你依赖的是 crates.io 上的 crate `foo`，但你的 crate 有一个 `bar` 特性而非 `foo` 特性。也就是说，重命名时，特性名称跟随依赖名称，而非包名。

启用传递依赖的方式类似，例如我们可以向上面的清单添加以下内容：

```toml
[features]
log-debug = ['bar/log-debug'] # 使用 'foo/log-debug' 会是错误！
```

## 从工作空间继承依赖 {#inheriting-a-dependency-from-a-workspace}

可通过在工作空间的 [`[workspace.dependencies]`][workspace.dependencies] 表中指定依赖来从工作空间继承依赖。之后，将其以 `workspace = true` 添加到 `[dependencies]` 表。

除 `workspace` 键外，依赖还可以包含这些键：
- [`optional`][optional]：注意 `[workspace.dependencies]` 表不允许指定 `optional`。
- [`features`][features]：这些与 `[workspace.dependencies]` 中声明的特性是累加的

除 `optional` 与 `features` 外，继承的依赖不能使用任何其他依赖键（例如 `version` 或 `default-features`）。

`[dependencies]`、`[dev-dependencies]`、`[build-dependencies]` 与 `[target."...".dependencies]` 节中的依赖都支持引用 `[workspace.dependencies]` 中的依赖定义。

```toml
[package]
name = "bar"
version = "0.2.0"

[dependencies]
regex = { workspace = true, features = ["unicode"] }

[build-dependencies]
cc.workspace = true

[dev-dependencies]
rand = { workspace = true, optional = true }
```


[SemVer]: https://semver.org
[crates.io]: https://crates.io/
[dev-dependencies]: #development-dependencies
[workspace.dependencies]: ../02-workspaces/#the-dependencies-table
[optional]: ../features/#optional-dependencies
[features]: ../features/
