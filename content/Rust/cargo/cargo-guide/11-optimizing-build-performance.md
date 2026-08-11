+++
title = "11-优化构建性能"
date = 2026-07-30T14:49:00+08:00
weight = 31
type = "docs"
description = "加快 Cargo 构建的实用建议"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 优化构建性能 {#optimizing-build-performance}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/build-performance.html](https://doc.rust-lang.org/cargo/guide/build-performance.html)


Cargo 配置选项与源码组织模式可以帮助提升构建性能，做法是优先考虑构建性能，而非在你的情境下可能不那么重要的其他方面。

与优化运行时性能一样，请务必针对你实际关心的工作流来衡量这些改动。我们提供的是一般性指南，而你的情况可能不同；其中一些方法实际上可能使你的用例的构建性能变差。

可考虑的示例工作流包括：
- 开发时的编译器反馈（修改代码后的 `cargo check`）
- 开发时的测试反馈（修改代码后的 `cargo test`）
- CI 构建

## Cargo 与编译器配置 {#cargo-and-compiler-configuration}
Cargo 使用的配置默认值试图在多个方面之间取得平衡，包括可调试性、运行时性能、构建性能、二进制大小等。本节描述若干改变这些默认值的方法，旨在最大化构建性能。

覆盖默认值的常见位置包括：
- [`Cargo.toml` 清单](../../cargo-reference/05-profiles/)
  - 对所有为你的项目做贡献的开发者可用
  - 支持的配置有限（扩展支持见 [#12738](https://github.com/rust-lang/cargo/issues/12738)）
- [`$WORKSPACE_ROOT/.cargo/config.toml` 配置文件](../../cargo-reference/06-configuration/)
  - 对所有为你的项目做贡献的开发者可用
  - 与 `Cargo.toml` 不同，它对你从哪个目录调用 `cargo` 敏感（见 [#2930](https://github.com/rust-lang/cargo/issues/2930)）
- [`$CARGO_HOME/.cargo/config.toml` 配置文件](../../cargo-reference/06-configuration/)
  - 供开发者控制其开发环境的默认值

### 减少生成的调试信息量 {#reduce-amount-of-generated-debug-information}
建议：添加到你的 `Cargo.toml` 或 `.cargo/config.toml`：

```toml
[profile.dev]
debug = "line-tables-only"

[profile.dev.package."*"]
debug = false

[profile.debugging]
inherits = "dev"
debug = true
```

这将：
- 更改 [`dev` 配置文件](../../cargo-reference/05-profiles/#dev)（开发命令的默认值）以：
  - 将工作空间成员的[调试信息](../../cargo-reference/05-profiles/#debug)限制为有用 panic 回溯所需的内容
  - 避免为依赖生成任何调试信息
- 在调试时通过 [`--profile debugging`](../../cargo-reference/05-profiles/#custom-profiles) 提供可选启用

> **注意：** 对 `dev` 配置文件的重新评估正在 [#15931](https://github.com/rust-lang/cargo/issues/15931) 中跟踪。

权衡：
- ✅ 更快的代码生成（`cargo build`）
- ✅ 更快的链接时间
- ✅ 更小的 `target` 目录磁盘占用
- ❌ 需要完整重建才能获得高质量的调试器体验

### 使用替代代码生成后端 {#use-an-alternative-codegen-backend}
建议：

- 安装 Cranelift 代码生成后端的 rustup 组件
    ```console
    $ rustup component add rustc-codegen-cranelift-preview --toolchain nightly
    ```
- 添加到你的 `Cargo.toml` 或 `.cargo/config.toml`：
    ```toml
    [profile.dev]
    codegen-backend = "cranelift"
    ```
- 使用 `-Z codegen-backend` 运行 Cargo，或在 `.cargo/config.toml` 中启用 [`codegen-backend`](../../cargo-reference/17-unstable-features/#codegen-backend) 特性。
  - 这是必需的，因为目前这是不稳定特性。

这会将 [`dev` 配置文件](../../cargo-reference/05-profiles/#dev)改为使用 [Cranelift 代码生成后端](https://github.com/rust-lang/rustc_codegen_cranelift)生成机器码，而不是默认的 LLVM 后端。Cranelift 后端应比 LLVM 更快地生成代码，从而改善构建性能。

权衡：
- ✅ 更快的代码生成（`cargo build`）
- ❌ **需要使用 nightly Rust 与[不稳定的 Cargo 特性][codegen-backend-feature]**
- ❌ 生成代码的运行时性能更差
  - 加快 `cargo test` 的构建部分，但可能增加其测试执行部分
- ❌ 仅适用于[特定目标](https://github.com/rust-lang/rustc_codegen_cranelift?tab=readme-ov-file#platform-support)
- ❌ 可能不支持所有 Rust 特性（例如 unwinding）

[codegen-backend-feature]: ../../cargo-reference/17-unstable-features/#codegen-backend

### 启用实验性并行前端 {#enable-the-experimental-parallel-frontend}
建议：添加到你的 `.cargo/config.toml`：

```toml
[build]
rustflags = "-Zthreads=8"
```

此 [`rustflags`][build.rustflags] 将启用 Rust 编译器的[并行前端][parallel-frontend-blog]，并告诉它使用 `n` 个线程。`n` 的值应根据系统上可用的核心数选择，尽管收益递减。我们建议最多使用 `8` 个线程。

权衡：
- ✅ 更快的构建时间（`cargo check` 与 `cargo build`）
- ❌ **需要使用 nightly Rust 与[不稳定的 Rust 特性][parallel-frontend-issue]**

[parallel-frontend-blog]: https://blog.rust-lang.org/2023/11/09/parallel-rustc/
[parallel-frontend-issue]: https://github.com/rust-lang/rust/issues/113349
[build.rustflags]: ../../cargo-reference/06-configuration/#buildrustflags

### 使用替代链接器 {#use-an-alternative-linker}
考虑：安装并配置替代链接器，如 [LLD](https://lld.llvm.org/)、[mold](https://github.com/rui314/mold) 或 [wild](https://github.com/davidlattimore/wild)。例如，要在 Linux 上配置 mold，可以添加到 `.cargo/config.toml`：

```toml
[target.'cfg(target_os = "linux")']
# mold，若你有 GCC 12+
rustflags = ["-C", "link-arg=-fuse-ld=mold"]

# mold，其他情况
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=/path/to/mold"]
```

虽然依赖可能并行构建，但链接所有依赖发生在构建结束时的一次性操作中，这可能使链接主导你的构建时间，尤其是增量重建时。通常，Rust 使用的链接器已经相当快，切换的收益可能不值得，但并非总是如此。例如，除 `x86_64-unknown-linux-gnu` 外的 Linux 目标仍使用相当慢的 Linux 系统链接器（更多细节见 [rust#39915](https://github.com/rust-lang/rust/issues/39915)）。

权衡：
- ✅ 更快的链接时间
- ❌ 可能不支持所有用例，尤其是当你依赖 C 或 C++ 依赖时

### 为整个工作空间解析特性 {#resolve-features-for-the-whole-workspace}
考虑：添加到项目的 `.cargo/config.toml`

```toml
[resolver]
feature-unification = "workspace"
```

调用 `cargo` 时，[特性会根据][resolver-features]你选择的工作空间成员被激活。然而，在为应用程序做贡献时，你可能需要构建并测试应用内的各个包，这可能因公共依赖激活不同的特性集而导致额外重建。使用 [`feature-unification`][feature-unification]，你可以通过确保激活相同的依赖特性集，在你当前构建与测试哪个包无关的情况下，复用更多依赖构建。

权衡：
- ✅ 在工作空间中构建不同包时更少重建
- ❌ **需要使用 nightly Rust 与[不稳定的 Cargo 特性][feature-unification]**
- ❌ 某个包激活特性可能掩盖其他本应激活却未激活该特性的包中的缺陷
- ❌ 若来自 `--workspace` 的特性统一对你不起作用，则此方案也不会起作用

[resolver-features]: ../../cargo-reference/specifying-dependencies/03-dependency-resolution/#features
[feature-unification]: ../../cargo-reference/17-unstable-features/#feature-unification

## 减少构建的代码 {#reducing-built-code}
### 移除未使用的依赖 {#removing-unused-dependencies}
建议：定期使用以下命令审查未使用的依赖以便移除：
```console
$ cargo +nightly check -Zcargo-lints --workspace --all-targets
```
这可能产生误报，来自：
- 依赖的使用由 `build.rs` 或 `RUSTFLAGS` 动态控制时

此外，定期审查隐藏的 [`cargo::unused_dependencies`] 结果：
```console
$ CARGO_LOG=cargo::diagnostics::rules::unused_dependencies=debug cargo +nightly check -Zcargo-lints --workspace --all-targets
```
这将显示潜在未使用的依赖，针对：
- 注册表与 git 依赖
- 当你的 [`package.rust-version`] 过旧而无法使用 `[lints.cargo]` 时
- 当你的依赖*可能*用于约束传递依赖的版本时（应改用 `[target."cfg(false)".dependencies]`）
- 当你的依赖*可能*用于激活传递依赖上的特性时
- 你的 `[dev-dependencies]`，因为尚无方法确保其所有消费者都被构建

修改代码时，很容易忽略某个依赖已不再使用、可以移除。

权衡：
- ✅ 更快的完整构建与链接时间
- ❌ **审查未使用依赖时需要使用 nightly Rust 与[不稳定的 Cargo 特性][cargo-lints]**
- ❌ 从误报中识别未使用依赖需要投入精力

[cargo-lints]: ../../cargo-reference/17-unstable-features/#lintscargo
[`cargo::unused_dependencies`]: ../../cargo-reference/16-lints/#unused_dependencies
[`package.rust-version`]: ../../cargo-reference/the-manifest-format/02-rust-version/

### 从依赖中移除未使用的特性 {#removing-unused-features-from-dependencies}
建议：定期使用第三方工具审查并移除依赖中未使用的特性，例如
[cargo-features-manager](https://crates.io/crates/cargo-features-manager)、
[cargo-unused-features](https://crates.io/crates/cargo-unused-features)。

修改代码时，很容易忽略某个依赖的特性已不再使用、可以移除。这可以减少被构建的传递依赖数量，或减少 crate 内被构建的代码量。移除特性时需格外谨慎，因为特性也可能用于期望的行为或性能变更，而这些变更从编译或测试中并不总是显而易见。

权衡：
- ✅ 更快的完整构建与链接时间
- ❌ 可能错误地将特性标记为未使用
