+++
title = "03-依赖解析"
date = 2026-07-30T14:49:00+08:00
weight = 38
type = "docs"
description = "Cargo 依赖解析器算法与版本选择"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 依赖解析 {#dependency-resolution}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/resolver.html](https://doc.rust-lang.org/cargo/reference/resolver.html)


Cargo 的主要任务之一，是根据各包（package）中指定的版本需求，确定要使用的依赖版本。这一过程称为「依赖解析（dependency resolution）」，由「解析器（resolver）」执行。解析结果保存在 [`Cargo.lock` 文件]中，将依赖「锁定」到特定版本，并随时间保持不变。[`cargo tree`] 命令可用于可视化解析器的结果。

[`Cargo.lock` 文件]: ../../../cargo-guide/06-cargo-toml-vs-cargo-lock/
[dependency specifications]: ../../
[dependency specification]: ../../
[`cargo tree`]: ../../../cargo-commands/manifest-commands/08-cargo-tree/

## 约束与启发式 {#constraints-and-heuristics}
在许多情况下，并不存在唯一的「最佳」依赖解析结果。解析器在多种约束与启发式下工作，以找到普遍适用的解析方案。要理解这些要素如何相互作用，对依赖解析的工作方式有一个粗略了解会很有帮助。

以下伪代码近似描述了 Cargo 解析器的行为：

```rust
pub fn resolve(workspace: &[Package], policy: Policy) -> Option<ResolveGraph> {
    let dep_queue = Queue::new(workspace);
    let resolved = ResolveGraph::new();
    resolve_next(dep_queue, resolved, policy)
}

fn resolve_next(dep_queue: Queue, resolved: ResolveGraph, policy: Policy) -> Option<ResolveGraph> {
    let Some(dep_spec) = policy.pick_next_dep(&mut dep_queue) else {
        // 完成
        return Some(resolved);
    };

    if let Some(resolved) = policy.try_unify_version(dep_spec, resolved.clone()) {
        return Some(resolved);
    }

    let dep_versions = dep_spec.lookup_versions()?;
    let mut dep_versions = policy.filter_versions(dep_spec, dep_versions);
    while let Some(dep_version) = policy.pick_next_version(&mut dep_versions) {
        if policy.needs_version_unification(&dep_version, &resolved) {
            continue;
        }

        let mut dep_queue = dep_queue.clone();
        dep_queue.enqueue(&dep_version.dependencies);
        let mut resolved = resolved.clone();
        resolved.register(dep_version);
        if let Some(resolved) = resolve_next(dep_queue, resolved, policy) {
            return Some(resolved);
        }
    }

    // 未找到有效解，回溯并 `pick_next_version`
    None
}
```

关键步骤：

- 遍历依赖（`pick_next_dep`）：
  依赖的遍历顺序会影响
  同一依赖的相关版本需求如何被解析，参见版本统一，
  以及解析器回溯的程度，从而影响解析器性能。
- 统一版本（`try_unify_version`、`needs_version_unification`）：
  Cargo 在可能的情况下复用版本，以减少构建时间，并允许来自共同依赖的类型在 API 之间传递。
  若多个版本本可统一，但因[依赖规格（dependency specifications）][dependency specifications]冲突而无法统一，Cargo 将回溯，若找不到解则报错，而不是选择多个版本。
  [依赖规格（dependency specification）][dependency specification]或 Cargo 可能判定某版本不可取，
  宁愿回溯或报错也不使用它。
- 偏好版本（`pick_next_version`）：
  Cargo 可能决定应优先选择特定版本，
  回溯时再尝试下一个版本。

### 版本号 {#version-numbers}

一般而言，Cargo 偏好当前可用的最高版本。

例如，若解析图中某包包含：

```toml
[dependencies]
bitflags = "*"
```

若在生成 `Cargo.lock` 文件时，`bitflags` 的最高版本为 `1.2.1`，则该包将使用 `1.2.1`。

可能例外的说明，见 [Rust 版本](#rust-version)。

### 版本需求 {#version-requirements}

包通过[版本需求][version requirements]指定其支持的版本，并拒绝所有其他版本。

例如，若解析图中某包包含：

```toml
[dependencies]
bitflags = "1.0"  # 含义为 `>=1.0.0,<2.0.0`
```

若在生成 `Cargo.lock` 文件时，`bitflags` 的最高版本为 `1.2.1`，则该包将使用 `1.2.1`，因为它是兼容范围内的最高版本。若发布了 `2.0.0`，仍会使用 `1.2.1`，因为 `2.0.0` 被视为不兼容。

[version requirements]: ../../#version-requirement-syntax

### SemVer 兼容性 {#semver-compatibility}
Cargo 假定包遵循 [SemVer]，若依赖版本按 [插入符（Caret）版本需求][Caret version requirements]符合 [SemVer] 兼容，则会统一依赖版本。
若两个兼容版本因版本需求冲突而无法统一，
Cargo 将报错。

关于何种变更被视为「兼容」，请参阅 [SemVer 兼容性][SemVer Compatibility]章节。

示例：

以下两个包对 `bitflags` 的依赖将被统一，因为所选任意版本彼此兼容。

```toml
# 包 A
[dependencies]
bitflags = "1.0"  # 含义为 `>=1.0.0,<2.0.0`

# 包 B
[dependencies]
bitflags = "1.1"  # 含义为 `>=1.1.0,<2.0.0`
```

以下包将报错，因为版本需求冲突，会选中两个不同的兼容版本。

```toml
# 包 A
[dependencies]
log = "=0.4.11"

# 包 B
[dependencies]
log = "=0.4.8"
```

以下两个包对 `rand` 的依赖不会被统一，因为各自仅有不兼容版本可用。
相反，将解析并构建两个不同版本（例如 0.6.5 与 0.7.3）。
这可能引发潜在问题，详见[版本不兼容风险][Version-incompatibility hazards]一节。

```toml
# 包 A
[dependencies]
rand = "0.7"  # 含义为 `>=0.7.0,<0.8.0`

# 包 B
[dependencies]
rand = "0.6"  # 含义为 `>=0.6.0,<0.7.0`
```

一般而言，以下两个包不会统一其依赖，因为有满足版本需求的不兼容版本可用：
相反，将解析并构建两个不同版本（例如 0.6.5 与 0.7.3）。
其他约束或启发式的应用可能导致它们被统一，
并选中一个版本（例如 0.6.5）。

```toml
# 包 A
[dependencies]
rand = ">=0.6,<0.8.0"

# 包 B
[dependencies]
rand = "0.6"  # 含义为 `>=0.6.0,<0.7.0`
```

[SemVer]: https://semver.org/
[SemVer Compatibility]: ../../13-semver-compatibility/
[Caret version requirements]: ../../#default-requirements
[Version-incompatibility hazards]: #version-incompatibility-hazards

#### 版本不兼容风险 {#version-incompatibility-hazards}

当解析图中出现同一 crate 的多个版本时，若使用这些 crate 的上层 crate 暴露了其中的类型，就可能出现问题。
这是因为 Rust 编译器会将这些类型与项视为不同，即使名称相同。库在发布 SemVer 不兼容版本时（例如在使用 `1.0.0` 之后发布 `2.0.0`）应格外谨慎，尤其是被广泛使用的库。

「[semver trick]」是在发布破坏性变更的同时保持与旧版本兼容的变通方法。链接页面详细说明了问题所在及应对方式。简而言之，当库希望发布 SemVer 破坏性版本时，应发布新版本，同时发布旧版本的一个补丁版本，从新版本重新导出类型。

这些不兼容通常表现为编译期错误，但有时仅表现为运行时行为异常。例如，假设解析图中同时出现名为 `foo` 的常用库的版本 `1.0.0` 与 `2.0.0`。若对使用 `1.0.0` 版本的库创建的对象使用 [`downcast_ref`]，而调用 `downcast_ref` 的代码向下转型为 `2.0.0` 版本的类型，则向下转型会在运行时失败。

若你使用了某库的多个版本，务必确保正确使用它们，尤其当不同版本的类型可能被一起使用时。[`cargo tree -d`][`cargo tree`] 命令可用于识别重复版本及其来源。同样，若你要发布某流行库的 SemVer 不兼容版本，也应考虑对生态系统的影响。

[semver trick]: https://github.com/dtolnay/semver-trick
[`downcast_ref`]: https://doc.rust-lang.org/std/any/trait.Any.html#method.downcast_ref

### 锁文件 {#lock-file}
在使用时，Cargo 对 [`Cargo.lock` 文件]中包含的版本给予最高优先级。
这旨在在可重现构建与随清单变更而调整之间取得平衡。

例如，若解析图中某包包含：

```toml
[dependencies]
bitflags = "*"
```

若在生成 `Cargo.lock` 文件时，`bitflags` 的最高版本为 `1.2.1`，则该包将使用 `1.2.1`，并记录在 `Cargo.lock` 文件中。

当 Cargo 再次运行时，`bitflags` `1.3.5` 已发布。
在解析依赖时，
仍会使用 `1.2.1`，因为它存在于 `Cargo.lock` 文件中。

随后该包被编辑为：

```toml
[dependencies]
bitflags = "1.3.0"
```

`bitflags` `1.2.1` 不符合此版本需求，因此 `Cargo.lock` 中的该条目被忽略，现在将使用版本 `1.3.5`，并记录在 `Cargo.lock` 文件中。

### Rust 版本 {#rust-version}

为支持以最低支持的 [Rust 版本][Rust version]开发软件，
解析器可以考虑依赖版本与你 Rust 版本的兼容性。
这由配置字段 [`resolver.incompatible-rust-versions`] 控制。

在 `fallback` 设置下，解析器将偏好 Rust 版本小于或等于你当前 Rust 版本的包。
例如，你使用 Rust 1.85 开发以下包：

```toml
[package]
name = "my-cli"
rust-version = "1.62"

[dependencies]
clap = "4.0"  # 解析为 4.0.32
```

解析器会选择 4.0.32，因为其 Rust 版本为 1.60.0。

- 不会选择 4.0.0，尽管其 Rust 版本也是 1.60.0，但它是[较低版本号](#version-numbers)。
- 不会选择 4.5.20，尽管其[版本号更高](#version-numbers)，且其 Rust 版本 1.74.0 与你的 1.85 工具链兼容，但它与 `my-cli` 的 Rust 版本 1.62 不兼容。

若版本需求不包含与 Rust 版本兼容的依赖版本，
解析器不会报错，而是仍会选中一个版本，即使可能并非最优。
例如，你将 `clap` 的依赖改为：

```toml
[package]
name = "my-cli"
rust-version = "1.62"

[dependencies]
clap = "4.2"  # 解析为 4.5.20
```

没有 `clap` 版本既满足该[版本需求](#version-requirements)，又与 Rust 版本 1.62 兼容。
解析器随后会选中不兼容版本，例如 Rust 版本为 1.74 的 4.5.20。

当解析器为包选择依赖版本时，
它并不知道最终哪些工作空间成员会通过传递依赖用到该版本，
因此无法仅考虑与该依赖相关的 Rust 版本。
当工作空间成员具有不同 Rust 版本时，解析器会使用启发式方法寻找「足够好」的解。
这即使对工作空间中没有 Rust 版本的包也适用。

当工作空间成员具有不同 Rust 版本时，
解析器可能选中比必要更低的依赖版本。
例如，你有以下工作空间成员：

```toml
[package]
name = "a"
rust-version = "1.62"

[package]
name = "b"

[dependencies]
clap = "4.2"  # 解析为 4.5.20
```

尽管包 `b` 没有 Rust 版本，本可使用更高版本如 4.5.20，
但由于包 `a` 的 Rust 版本为 1.62，将选中 4.0.32。

或者解析器可能选中过高的版本。
例如，你有以下工作空间成员：

```toml
[package]
name = "a"
rust-version = "1.62"

[dependencies]
clap = "4.2"  # 解析为 4.5.20

[package]
name = "b"

[dependencies]
clap = "4.5"  # 解析为 4.5.20
```

尽管每个包对 `clap` 的版本需求都能满足各自的 Rust 版本，
但由于[版本统一](#version-numbers)，
解析器需要选中一个对两者都适用的版本，例如 4.5.20。

[Rust version]: ../../the-manifest-format/02-rust-version/
[`resolver.incompatible-rust-versions`]: ../../06-configuration/#resolverincompatible-rust-versions

### 特性 {#features}

为生成 `Cargo.lock`，解析器在构建依赖图时，假定所有[工作空间（workspace）][workspace]成员的[特性（feature）][features]均已启用。这确保在通过 [`--features` 命令行标志](../../features/#command-line-feature-options)添加或移除特性时，任何可选依赖都可用，并与图的其余部分正确解析。
解析器会第二次运行，以根据命令行所选特性确定*编译* crate 时实际使用的特性。

依赖以在其上启用的全部特性的并集进行解析。例如，若一个包依赖 [`im`] 包并启用了 [`serde` 依赖]，另一个包依赖它并启用了 [`rayon` 依赖]，则 `im` 将同时启用这两个特性构建，`serde` 与 `rayon` crate 将包含在解析图中。若没有包以这些特性依赖 `im`，则这些可选依赖会被忽略，不会影响解析。

在工作空间中构建多个包时（例如使用 `--workspace` 或多个 `-p` 标志），这些包依赖的特性会被统一。若你希望为不同工作空间成员避免这种统一，需要通过分别调用 `cargo` 来构建它们。

解析器会跳过缺少所需特性的包版本。例如，若某包依赖 [`regex`] 的 `^1` 版本并启用了 [`perf` 特性]，则它可选的最旧版本为 `1.3.0`，因为更早版本不包含 `perf` 特性。同样，若某特性在新版本中被移除，则需要该特性的包会停留在仍包含该特性的旧版本上。不建议在 SemVer 兼容版本发布中移除特性。请注意，可选依赖也会定义隐式特性，因此移除可选依赖或将其改为非可选可能引发问题，见[移除可选依赖][removing an optional dependency]。

[`im`]: https://crates.io/crates/im
[`perf` feature]: https://github.com/rust-lang/regex/blob/1.3.0/Cargo.toml#L56
[`rayon` dependency]: https://github.com/bodil/im-rs/blob/v15.0.0/Cargo.toml#L47
[`regex`]: https://crates.io/crates/regex
[`serde` dependency]: https://github.com/bodil/im-rs/blob/v15.0.0/Cargo.toml#L46
[features]: ../../features/
[removing an optional dependency]: ../../13-semver-compatibility/#cargo-remove-opt-dep
[workspace]: ../../02-workspaces/

#### 特性解析器版本 2 {#feature-resolver-version-2}

当在 `Cargo.toml` 中指定 `resolver = "2"` 时（见下文[解析器版本](#resolver-versions)），会使用不同的特性解析器，其统一特性时采用不同算法。版本 `"1"` 解析器无论包在何处被指定都会统一其特性。
版本 `"2"` 解析器在以下情况下会避免统一特性：

* 若当前未构建对应目标，则不会启用特定于目标的依赖的特性。例如：

  ```toml
  [dependencies.common]
  version = "1.0"
  features = ["f1"]

  [target.'cfg(windows)'.dependencies.common]
  version = "1.0"
  features = ["f2"]
  ```

  在非 Windows 平台上构建此示例时，`f2` 特性将*不会*被启用。

* 在[构建依赖][build-dependencies]或 proc-macro 上启用的特性，当相同依赖作为普通依赖使用时不会统一。例如：

  ```toml
  [dependencies]
  log = "0.4"

  [build-dependencies]
  log = {version = "0.4", features=['std']}
  ```

  构建构建脚本时，`log` crate 会启用 `std` 特性构建。构建你包的库时，不会启用该特性。

* 在[开发依赖][dev-dependencies]上启用的特性，当相同依赖作为普通依赖使用时不会统一，除非这些开发依赖当前正在被构建。例如：

  ```toml
  [dependencies]
  serde = {version = "1.0", default-features = false}

  [dev-dependencies]
  serde = {version = "1.0", features = ["std"]}
  ```

  在此示例中，库通常链接不带 `std` 特性的 `serde`。但作为测试或示例构建时，会包含 `std` 特性。例如，`cargo test` 或 `cargo build --all-targets` 会统一这些特性。请注意，依赖中的开发依赖始终被忽略，这仅与顶层包或工作空间成员相关。

[build-dependencies]: ../../#build-dependencies
[dev-dependencies]: ../../#development-dependencies
[resolver-field]: ../../features/#feature-resolver-version-2

### `links` {#links}
[`links` 字段][`links` field]用于确保二进制中只链接一份原生库副本。解析器会尝试找到每个 `links` 名称仅出现一次的图。若无法找到满足该约束的图，将返回错误。

例如，若一个包依赖 [`libgit2-sys`] 版本 `0.11`，另一个依赖 `0.12`，则为错误，因为 Cargo 无法统一它们，但它们都链接到 `git2` 原生库。由于此要求，若你的库被广泛使用，在使用 `links` 字段发布 SemVer 不兼容版本时应非常谨慎。

[`links` field]: ../../the-manifest-format/#the-links-field
[`libgit2-sys`]: https://crates.io/crates/libgit2-sys

### 被 yank 的版本 {#yanked-versions}
[被 yank 的发布][yank] 指标记为不应使用的版本。解析器构建图时会忽略所有被 yank 的发布，除非它们已存在于 `Cargo.lock` 文件中，或由 `cargo update` 的 [`--precise`] 标志显式请求。

[yank]: ../../../cargo-guide/09-publishing-on-crates-io/#cargo-yank
[`--precise`]: ../../../cargo-commands/manifest-commands/09-cargo-update/#option-cargo-update---precise

## 依赖更新 {#dependency-updates}
所有需要了解依赖图的 Cargo 命令都会自动执行依赖解析。例如，[`cargo build`] 会运行解析器以发现所有要构建的依赖。首次运行后，结果保存在 `Cargo.lock` 文件中。后续命令也会运行解析器，*在可能的情况下*将依赖锁定为 `Cargo.lock` 中的版本。

若 `Cargo.toml` 中的依赖列表已被修改，例如将某依赖版本从 `1.0` 改为 `2.0`，则解析器会为该依赖选中符合新需求的新版本。若该新依赖引入了新需求，这些新需求也可能触发额外更新。`Cargo.lock` 文件会更新为新结果。可使用 `--locked` 或 `--frozen` 标志改变此行为，在需求变更时阻止自动更新并改为返回错误。

[`cargo update`] 可在发布新版本时更新 `Cargo.lock` 中的条目。不带任何选项时，会尝试更新锁文件中的所有包。`-p` 标志可用于针对特定包进行更新，`--recursive` 或 `--precise` 等标志可控制如何选择版本。

[`cargo build`]: ../../../cargo-commands/build-commands/02-cargo-build/
[`cargo update`]: ../../../cargo-commands/manifest-commands/09-cargo-update/

## 覆盖 {#overrides}
Cargo 提供多种机制在图中覆盖依赖。[覆盖依赖][Overriding Dependencies]章节详细介绍了如何使用覆盖。
覆盖表现为对注册表的叠加层，用新条目替换被补丁的版本。除此之外，解析过程与正常情况相同。

[Overriding Dependencies]: ../01-overriding-dependencies/

## 依赖种类 {#dependency-kinds}
包中有三种依赖：普通、[构建][build]与[开发][dev-dependencies]依赖。从解析器角度看，它们大多被同等对待。一个区别是，非工作空间成员的开发依赖始终被忽略，不影响解析。

带有 `[target]` 表的[平台特定依赖][Platform-specific dependencies]在解析时假定所有平台均已启用。换言之，解析器会忽略平台或 `cfg` 表达式。

[build]: ../../#build-dependencies
[dev-dependencies]: ../../#development-dependencies
[Platform-specific dependencies]: ../../#platform-specific-dependencies

### 开发依赖环 {#dev-dependency-cycles}
通常解析器不允许图中出现环，但对[开发依赖][dev-dependencies]允许。例如，项目 "foo" 对 "bar" 有开发依赖，而 "bar" 对 "foo" 有普通依赖（通常是 "path" 依赖）。这是允许的，因为从构建产物角度看并不存在真正的环。在此示例中，"foo" 库被构建（不需要 "bar"，因为 "bar" 仅用于测试），然后可构建依赖 "foo" 的 "bar"，最后可构建链接到 "bar" 的 "foo" 测试。

请注意，这可能导致令人困惑的错误。在构建库单元测试时，最终测试二进制中实际上链接了两份库副本：与 "bar" 链接的那份，以及包含单元测试的那份。与[版本不兼容风险][Version-incompatibility hazards]一节中强调的问题类似，两份库之间的类型不兼容。在此情况下从 "bar" 暴露 "foo" 的类型时要谨慎，因为 "foo" 单元测试不会将其与本地类型同等对待。

若可能，请尝试将包拆分为多个包并重构，使其保持严格无环。

## 解析器版本 {#resolver-versions}

可通过 `Cargo.toml` 中的解析器版本指定不同的解析器行为，例如：

```toml
[package]
name = "my-package"
version = "1.0.0"
resolver = "2"
```

- `"1"`（默认）
- `"2"`（[`edition = "2021"`](../../the-manifest-format/#the-edition-field) 默认）：引入[特性统一](#features)方面的变更。详见[特性章节][features-2]。
- `"3"`（[`edition = "2024"`](../../the-manifest-format/#the-edition-field) 默认，需要 Rust 1.84+）：将 [`resolver.incompatible-rust-versions`] 的默认值从 `allow` 改为 `fallback`

解析器是全局选项，影响整个工作空间。依赖中的 `resolver` 版本会被忽略，仅使用顶层包中的值。若使用[虚拟工作空间][virtual workspace]，应在 `[workspace]` 表中指定版本，例如：

```toml
[workspace]
members = ["member1", "member2"]
resolver = "2"
```

> **MSRV：** 需要 1.51+

[virtual workspace]: ../../02-workspaces/#virtual-workspace
[features-2]: ../../features/#feature-resolver-version-2

## 建议 {#recommendations}
以下是在包内设置版本以及指定依赖需求的一些建议。这些是适用于常见情况的通用指南，当然某些情况可能需要指定不寻常的需求。

* 在决定如何更新版本号以及是否需要 SemVer 不兼容版本变更时，遵循 [SemVer 指南][SemVer guidelines]。
* 在大多数情况下，对依赖使用插入符需求，例如 `"1.2.3"`。这确保解析器在选择版本时尽可能灵活，同时保持构建兼容性。
  * 使用你当前所用版本并指定全部三个组件。这有助于设定将使用的最低版本，并确保其他用户不会得到缺少你的包所需内容的更旧依赖版本。
  * 避免 `*` 需求，因为 [crates.io] 不允许，且可能在普通 `cargo update` 中拉入 SemVer 破坏性变更。
  * 避免过于宽泛的版本需求。例如，`>=2.0.0` 可能拉入任意 SemVer 不兼容版本，如 `5.0.0`，导致未来构建失败。
  * 若可能，避免过于狭窄的版本需求。例如，若你指定 tilde 需求如 `bar="~1.3"`，而另一包指定 `bar="1.4"`，即使次版本发布本应兼容，也会解析失败。
* 尽量使依赖版本与实际所需的最低版本保持同步。例如，若你有 `bar="1.0.12"` 的需求，之后在新版本中使用 "bar" `1.1.0` 发布中新增的特性，应将依赖需求更新为 `bar="1.1.0"`。

  若未这样做，可能不会立即显现问题，因为不加区分地运行 `cargo update` 时 Cargo 可能伺机选择最新版本。然而，若其他用户依赖你的库并运行 `cargo update your-library`，在其 `Cargo.lock` 已锁定的情况下，*不会*自动更新 "bar"。仅当依赖声明也被更新时，该情况下才会更新 "bar"。未这样做可能导致使用 `cargo update your-library` 的用户遇到令人困惑的构建错误。
* 若两个包紧密耦合，则 `=` 依赖需求可能有助于保持同步。例如，带有配套 proc-macro 库的库有时会在两个库之间做出假设，若两者不同步则无法良好工作（且从不期望独立使用这两个库）。父库可对 proc-macro 使用 `=` 需求，并重新导出宏以便访问。
* `0.0.x` 版本可用于永久不稳定的包。

一般而言，依赖需求越严格，解析器失败的可能性越大。反之，若需求过于宽松，可能发布破坏构建的新版本。

[SemVer guidelines]: ../../13-semver-compatibility/
[crates.io]: https://crates.io/

## 故障排查 {#troubleshooting}
以下说明你可能遇到的一些问题及可能的解决方案。

### 为什么包含某依赖？ {#why-was-a-dependency-included}
假设你在 `cargo check` 输出中看到依赖 `rand`，但不认为需要它，想了解为何被拉入。

你可以运行

```console
$ cargo tree --workspace --target all --all-features --invert rand
rand v0.8.5
└── ...

rand v0.8.5
└── ...
```

### 为什么该依赖上启用了那个特性？ {#why-was-that-feature-on-this-dependency-enabled}
你可能发现是某已激活特性导致 `rand` 出现。**要找出哪个包激活了该特性，可添加 `--edges features`**

```console
$ cargo tree --workspace --target all --all-features --edges features --invert rand
rand v0.8.5
└── ...

rand v0.8.5
└── ...
```

### 意外的依赖重复 {#unexpected-dependency-duplication}
运行以下命令时看到 `rand` 的多个实例：

```console
$ cargo tree --workspace --target all --all-features --duplicates
rand v0.7.3
└── ...

rand v0.8.5
└── ...
```

解析器算法收敛到一个包含两份依赖的解，而一份即可满足。例如：

```toml
# 包 A
[dependencies]
rand = "0.7"

# 包 B
[dependencies]
rand = ">=0.6"  # 注意：不鼓励使用此类开放式需求
```

在此示例中，Cargo 可能构建两份 `rand` crate，尽管单一版本 `0.7.3` 即可满足所有需求。这是因为解析器算法倾向于为包 B 构建 `rand` 的最新可用版本，在撰写本文时为 `0.8.5`，这与包 A 的规格不兼容。解析器算法目前不会在此情况下尝试「去重」。

Cargo 不鼓励使用 `>=0.6` 这类开放式版本需求。
但若遇到此情况，可使用带 `--precise` 标志的 [`cargo update`] 命令手动消除此类重复。

[`cargo update`]: ../../../cargo-commands/manifest-commands/09-cargo-update/

### 为什么没有选中较新版本？ {#why-wasnt-a-newer-version-selected}
假设你注意到运行以下命令时未选中依赖的最新版本：

```console
$ cargo update
```

你可以启用额外日志查看原因：

```console
$ env CARGO_LOG=cargo::resolver=trace cargo update
```

**注意：** Cargo 日志目标与级别可能随时间变化。

### SemVer 破坏性补丁发布导致构建失败 {#semver-breaking-patch-release-breaks-the-build}
有时项目可能无意中发布了带有 SemVer 破坏性变更的补丁版本。用户通过 `cargo update` 更新时会获得该新版本，随后构建可能失败。此情况下，建议项目应 [yank] 该发布，并要么移除 SemVer 破坏性变更，要么将其作为新的 SemVer 主版本发布。

若变更发生在第三方项目中，若可能请尝试（礼貌地！）与项目协作解决问题。

在等待发布被 yank 期间，一些变通方法取决于具体情况：

* 若你的项目是最终产物（例如二进制可执行文件），只需避免在 `Cargo.lock` 中更新有问题的包。可通过 [`cargo update`] 的 `--precise` 标志实现。
* 若在 [crates.io] 上发布二进制，可临时添加 `=` 需求以强制依赖使用特定良好版本。
  * 二进制项目也可建议用户使用 [`cargo install`] 的 `--locked` 标志，以使用包含已知良好版本的原始 `Cargo.lock`。
* 库也可考虑发布临时新版本，使用更严格的需求以避开有问题的依赖。你可能希望考虑使用范围需求（而非 `=`），以避免与其他使用同一依赖的包产生过于严格的需求冲突。问题解决后，可再发布一个补丁版本，将依赖放宽回插入符需求。
* 若第三方项目似乎无法或不愿 yank 该发布，一个选项是更新代码以兼容变更，并将依赖需求的最低版本设为新发布。你还需要考虑这是否是你自身库的 SemVer 破坏性变更，例如若它暴露了依赖中的类型。

[`cargo install`]: ../../../cargo-commands/package-commands/02-cargo-install/
