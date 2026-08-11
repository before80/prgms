+++
title = "01-Cargo 目标"
date = 2026-07-30T14:49:00+08:00
weight = 32
type = "docs"
description = "lib、bin、example、test、bench 等目标配置"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Cargo 目标


> 原文链接: [https://doc.rust-lang.org/cargo/reference/cargo-targets.html](https://doc.rust-lang.org/cargo/reference/cargo-targets.html)


Cargo 包由 *目标（targets）* 组成，它们对应可被编译为 crate 的源文件。包可以有[库](#library)、[二进制](#binaries)、[示例](#examples)、[测试](#tests)与[基准测试](#benchmarks)目标。目标列表可在 `Cargo.toml` 清单中配置，通常会根据源文件的[目录布局][package layout][自动推断](#target-auto-discovery)。

关于配置目标设置的细节，见下文[配置目标](#configuring-a-target)。

## 库 {#library}

库目标定义一个可被其他库与可执行文件使用和链接的「库」。文件名默认为 `src/lib.rs`，库名默认为包名（任何破折号替换为下划线）。一个包只能有一个库。库的设置可在 `Cargo.toml` 的 `[lib]` 表中[自定义][customized]。

```toml
# 在 Cargo.toml 中自定义库的示例。
[lib]
crate-type = ["cdylib"]
bench = false
```

## 二进制 {#binaries}

二进制目标是编译后可运行的可执行程序。
二进制的源可以是 `src/main.rs` 和/或存放在 [`src/bin/` 目录][package layout]中。对于 `src/main.rs`，默认二进制名是包名。每个二进制的设置可在 `Cargo.toml` 的 `[[bin]]` 表中[自定义][customized]。

二进制可以使用包库的公共 API。它们也会与 `Cargo.toml` 中定义的 [`[dependencies]`][dependencies] 链接。

你可以使用 [`cargo run`] 命令配合 `--bin <bin-name>` 选项运行单个二进制。[`cargo install`] 可用于将可执行文件复制到常用位置。

```toml
# 在 Cargo.toml 中自定义二进制的示例。
[[bin]]
name = "cool-tool"
test = false
bench = false

[[bin]]
name = "frobnicator"
required-features = ["frobnicate"]
```

## 示例 {#examples}

位于 [`examples` 目录][package layout]下的文件是库所提供功能的示例用法。编译后，它们会放在 [`target/debug/examples` 目录][build cache]中。

示例可以使用包库的公共 API。它们也会与 `Cargo.toml` 中定义的 [`[dependencies]`][dependencies] 与 [`[dev-dependencies]`][dev-dependencies] 链接。

默认情况下，示例是可执行二进制（带有 `main()` 函数）。你可以指定 [`crate-type` 字段](#the-crate-type-field)使示例编译为库：

```toml
[[example]]
name = "foo"
crate-type = ["staticlib"]
```

你可以使用 [`cargo run`] 命令配合 `--example <example-name>` 选项运行单个可执行示例。库示例可用 [`cargo build`] 配合 `--example <example-name>` 选项构建。[`cargo install`] 配合 `--example <example-name>` 选项可用于将可执行二进制复制到常用位置。默认情况下，示例会由 [`cargo test`] 编译，以防止它们腐化。若你在示例中有希望用 [`cargo test`] 运行的 `#[test]` 函数，请将 [`test` 字段](#the-test-field)设为 `true`。

## 测试 {#tests}

Cargo 项目中有两种风格的测试：

* *单元测试*，是位于库或二进制（或任何启用了 [`test` 字段](#the-test-field)的目标）中、带有 [`#[test]` 属性][test-attribute] 标记的函数。这些测试可以访问它们所定义目标内的私有 API。
* *集成测试*，是单独的可执行二进制，也包含 `#[test]` 函数，与项目的库链接，并可访问其*公共* API。

测试用 [`cargo test`] 命令运行。默认情况下，Cargo 与 `rustc` 使用 [libtest harness]，它负责收集带有 [`#[test]` 属性][test-attribute] 注解的函数并并行执行它们，报告每个测试的成功与失败。若想使用不同的 harness 或测试策略，见 [`harness` 字段](#the-harness-field)。

> **注意**：Cargo 中还有另一种特殊风格的测试：
> [文档测试][documentation examples]。
> 它们由 `rustdoc` 处理，执行模型略有不同。
> 更多信息请见 [`cargo test`][cargo-test-documentation-tests]。

[libtest harness]: https://doc.rust-lang.org/rustc/tests/index.html
[cargo-test-documentation-tests]: ../../../cargo-commands/build-commands/14-cargo-test/#documentation-tests

### 集成测试 {#integration-tests}
位于 [`tests` 目录][package layout]下的文件是集成测试。当你运行 [`cargo test`] 时，Cargo 会将这些文件各自编译为单独的 crate 并执行它们。

集成测试可以使用包库的公共 API。它们也会与 `Cargo.toml` 中定义的 [`[dependencies]`][dependencies] 与 [`[dev-dependencies]`][dev-dependencies] 链接。

若想在多个集成测试之间共享代码，可以将其放在单独的模块中，例如 `tests/common/mod.rs`，然后在每个测试中放上 `mod common;` 以导入它。

每个集成测试会产生单独的可执行二进制，且 [`cargo test`] 会串行运行它们。在某些情况下这可能效率不高，因为编译可能更久，运行测试时也可能无法充分利用多个 CPU。若你有很多集成测试，可能需要考虑创建一个单一集成测试，并将测试拆分为多个模块。libtest harness 会自动找到所有带有 `#[test]` 注解的函数并并行运行它们。你可以向 [`cargo test`] 传递模块名，以仅运行该模块内的测试。

若存在集成测试，二进制目标会自动构建。这允许集成测试执行该二进制以演练并测试其行为。构建并运行集成测试时会设置 `CARGO_BIN_EXE_<name>` [环境变量]，以便它可使用 [`env` 宏][`env` macro] 或 [`var` 函数][`var` function] 定位可执行文件。

[environment variable]: ../../07-environment-variables/#environment-variables-cargo-sets-for-crates
[`env` macro]: https://doc.rust-lang.org/std/macro.env.html
[`var` function]: https://doc.rust-lang.org/std/env/fn.var.html

## 基准测试 {#benchmarks}

基准测试提供了一种使用 [`cargo bench`] 命令测试代码性能的方式。它们遵循与[测试](#tests)相同的结构，每个基准测试函数用 `#[bench]` 属性注解。与测试类似：

* 基准测试放在 [`benches` 目录][package layout]中。
* 在库与二进制中定义的基准测试函数可以访问它们所定义目标内的*私有* API。`benches` 目录中的基准测试可以使用*公共* API。
* [`bench` 字段](#the-bench-field)可用于定义默认对哪些目标做基准测试。
* [`harness` 字段](#the-harness-field)可用于禁用内置 harness。

> **注意**：[`#[bench]` 属性](https://doc.rust-lang.org/unstable-book/library-features/test.html)目前不稳定，且仅在 [nightly 通道][nightly channel]上可用。[crates.io](https://crates.io/keywords/benchmark) 上有一些包可能有助于在稳定通道上运行基准测试，例如 [Criterion](https://crates.io/crates/criterion)。

## 配置目标 {#configuring-a-target}

`Cargo.toml` 中的所有 `[lib]`、`[[bin]]`、`[[example]]`、`[[test]]` 与 `[[bench]]` 节都支持类似的配置，用于指定目标应如何构建。像 `[[bin]]` 这样的双括号节是 [TOML 的表数组](https://toml.io/en/v1.0.0-rc.3#array-of-tables)，这意味着你可以写多个 `[[bin]]` 节以在 crate 中创建多个可执行文件。你只能指定一个库，因此 `[lib]` 是普通的 TOML 表。

以下是每个目标的 TOML 设置概览，每个字段在下文详细说明。

```toml
[lib]
name = "foo"           # 目标的名称。
path = "src/lib.rs"    # 目标的源文件。
test = true            # 默认是否被测试。
doctest = true         # 默认是否测试文档示例。
bench = true           # 默认是否被基准测试。
doc = true             # 默认是否生成文档。
proc-macro = false     # 对于 proc-macro 库设为 `true`。
harness = true         # 使用 libtest harness。
crate-type = ["lib"]   # 要生成的 crate 类型。
required-features = [] # 构建此目标所需的特性（对 lib 不适用）。
```

### `name` 字段 {#the-name-field}
`name` 字段指定目标的名称，对应于将生成的产物文件名。对于库，这是依赖用来引用它的 crate 名。

对于库目标，这默认为包名，任何破折号替换为下划线。对于默认二进制（`src/main.rs`），也默认为包名，破折号不做替换。对于[自动发现](#target-auto-discovery)的目标，默认为目录或文件名。

除 `[lib]` 外，所有目标都需要此字段。

### `path` 字段 {#the-path-field}
`path` 字段指定 crate 源码的位置，相对于 `Cargo.toml` 文件。

若未指定，则根据目标名称使用[推断路径](#target-auto-discovery)。

### `test` 字段 {#the-test-field}

`test` 字段指示目标默认是否由 [`cargo test`] 测试。对于 lib、bin 与 test，默认值为 `true`。

> **注意**：示例默认由 [`cargo test`] 构建以确保它们继续能编译，但默认不会被*测试*。将示例的 `test = true` 也会将其构建为测试，并运行示例中定义的任何 [`#[test]`][test-attribute] 函数。

### `doctest` 字段 {#the-doctest-field}
`doctest` 字段指示[文档示例][documentation examples]默认是否由 [`cargo test`] 测试。这仅与库相关，对其他节无影响。对于库，默认值为 `true`。

### `bench` 字段 {#the-bench-field}

`bench` 字段指示目标默认是否由 [`cargo bench`] 进行基准测试。对于 lib、bin 与基准测试，默认值为 `true`。

### `doc` 字段 {#the-doc-field}
`doc` 字段指示目标默认是否包含在 [`cargo doc`] 生成的文档中。对于库与二进制，默认值为 `true`。

> **注意**：若二进制的名称与 lib 目标相同，则该二进制将被跳过。

### `plugin` 字段 {#the-plugin-field}
此选项已弃用且未使用。

### `proc-macro` 字段 {#the-proc-macro-field}
`proc-macro` 字段指示该库是[过程宏][procedural macro]（[参考][proc-macro-reference]）。这仅对 `[lib]` 目标有效。

### `harness` 字段 {#the-harness-field}

`harness` 字段指示会向 `rustc` 传递 [`--test` 标志]，从而自动包含 libtest 库，后者是收集并运行带有 [`#[test]` 属性][test-attribute] 标记的测试或带有 `#[bench]` 属性的基准测试的驱动。对所有目标默认值为 `true`。

若设为 `false`，则你需要自行定义 `main()` 函数来运行测试与基准测试。

无论 harness 是否启用，测试都会启用 [`cfg(test)` 条件表达式][cfg-test]。

### `crate-type` 字段 {#the-crate-type-field}

`crate-type` 字段定义目标将生成的 [crate 类型][crate types]。它是字符串数组，允许你为单个目标指定多种 crate 类型。这只能为库与示例指定。二进制、测试与基准测试始终是 "bin" crate 类型。默认值为：

目标 | Crate 类型
|-------|-----------
普通库 | `"lib"`
Proc-macro 库 | `"proc-macro"`
示例 | `"bin"`

可用选项为 `bin`、`lib`、`rlib`、`dylib`、`cdylib`、`staticlib` 与 `proc-macro`。关于不同 crate 类型的更多信息，可读 [Rust 参考手册][crate types]。

### `required-features` 字段 {#the-required-features-field}
`required-features` 字段指定目标需要哪些[特性（features）][features]才能构建。若任何所需特性未启用，该目标将被跳过。这仅与 `[[bin]]`、`[[bench]]`、`[[test]]` 与 `[[example]]` 节相关，对 `[lib]` 无影响。

```toml
[features]
# ...
postgres = []
sqlite = []
tools = []

[[bin]]
name = "my-pg-tool"
required-features = ["postgres", "tools"]
```

### `edition` 字段 {#the-edition-field}
`edition` 字段定义目标将使用的 [Rust edition][Rust Edition]。若未指定，默认为 `[package]` 的 [`edition` 字段][package-edition]。

> **注意：** 此字段已弃用，并将在未来的 Edition 中移除

## 目标自动发现 {#target-auto-discovery}

默认情况下，Cargo 会根据文件系统上的[文件布局][package layout]自动确定要构建的目标。目标配置表，例如 `[lib]`、`[[bin]]`、`[[test]]`、`[[bench]]` 或 `[[example]]`，可用于添加不遵循标准目录布局的额外目标。

可以禁用自动目标发现，从而仅构建手动配置的目标。在 `[package]` 节中将键 `autolib`、`autobins`、`autoexamples`、`autotests` 或 `autobenches` 设为 `false`，将禁用对应目标类型的自动发现。

```toml
[package]
# ...
autolib = false
autobins = false
autoexamples = false
autotests = false
autobenches = false
```

仅在特殊情况下才应禁用自动发现。例如，若你有一个希望有一个名为 `bin` 的*模块*的库，这会带来问题，因为 Cargo 通常会尝试将 `bin` 目录中的任何内容编译为可执行文件。以下是此场景的示例布局：

```text
├── Cargo.toml
└── src
    ├── lib.rs
    └── bin
        └── mod.rs
```

为防止 Cargo 将 `src/bin/mod.rs` 推断为可执行文件，在 `Cargo.toml` 中设置 `autobins = false` 以禁用自动发现：

```toml
[package]
# …
autobins = false
```

> **注意**：对于 2015 edition 的包，若 `Cargo.toml` 中至少手动定义了一个目标，自动发现的默认值为 `false`。从 2018 edition 开始，默认值始终为 `true`。

> **MSRV：** 自 1.27 起对 `autobins`、`autoexamples`、`autotests` 与 `autobenches` 生效

> **MSRV：** 自 1.83 起对 `autolib` 生效

[Build cache]: ../../09-build-cache/
[build cache]: ../../09-build-cache/
[Rust Edition]: https://doc.rust-lang.org/edition-guide/index.html
[`--test` flag]: https://doc.rust-lang.org/rustc/command-line-arguments.html#option-test
[`cargo bench`]: ../../../cargo-commands/build-commands/01-cargo-bench/
[`cargo build`]: ../../../cargo-commands/build-commands/02-cargo-build/
[`cargo doc`]: ../../../cargo-commands/build-commands/06-cargo-doc/
[`cargo install`]: ../../../cargo-commands/package-commands/02-cargo-install/
[`cargo run`]: ../../../cargo-commands/build-commands/11-cargo-run/
[`cargo test`]: ../../../cargo-commands/build-commands/14-cargo-test/
[cfg-test]: https://doc.rust-lang.org/reference/conditional-compilation.html#test
[crate types]: https://doc.rust-lang.org/reference/linkage.html
[crates.io]: https://crates.io/
[customized]: #configuring-a-target
[dependencies]: ../../specifying-dependencies/
[dev-dependencies]: ../../specifying-dependencies/#development-dependencies
[documentation examples]: https://doc.rust-lang.org/rustdoc/documentation-tests.html
[features]: ../../features/
[nightly channel]: https://doc.rust-lang.org/book/appendix-07-nightly-rust.html
[package layout]: ../../../cargo-guide/05-package-layout/
[package-edition]: ../../#the-edition-field
[proc-macro-reference]: https://doc.rust-lang.org/reference/procedural-macros.html
[procedural macro]: https://doc.rust-lang.org/book/ch19-06-macros.html
[test-attribute]: https://doc.rust-lang.org/reference/attributes/testing.html#the-test-attribute
