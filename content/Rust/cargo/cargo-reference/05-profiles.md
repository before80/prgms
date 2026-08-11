+++
title = "05-配置文件（Profiles）"
date = 2026-07-30T14:49:00+08:00
weight = 41
type = "docs"
description = "dev/release 等编译配置文件"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 配置文件（Profiles）


> 原文链接: [https://doc.rust-lang.org/cargo/reference/profiles.html](https://doc.rust-lang.org/cargo/reference/profiles.html)


配置文件（Profiles）提供了一种改变编译器设置的方式，影响优化与调试符号等内容。

Cargo 有 4 个内置配置文件：`dev`、`release`、`test` 与 `bench`。若命令行上未指定配置文件，则根据正在运行的命令自动选择。除内置配置文件外，也可以指定自定义的用户定义配置文件。

配置文件设置可在 [`Cargo.toml`](../the-manifest-format/) 中用 `[profile]` 表更改。在每个命名配置文件内，可用如下键/值对更改个别设置：

```toml
[profile.dev]
opt-level = 1               # 使用稍好一些的优化。
overflow-checks = false     # 禁用整数溢出检查。
```

Cargo 仅查看工作空间根处 `Cargo.toml` 清单中的配置文件设置。在依赖中定义的配置文件设置将被忽略。

此外，配置文件可从[配置][config]定义中覆盖。在配置文件或环境变量中指定配置文件将覆盖 `Cargo.toml` 中的设置。

[config]: ../06-configuration/

## 配置文件设置 {#profile-settings}
以下是可在配置文件中控制的设置列表。

### opt-level {#opt-level}
`opt-level` 设置控制 [`-C opt-level` 标志][`-C opt-level` flag]，后者控制优化级别。更高的优化级别可能以更长的编译时间为代价产生更快的运行时代码。更高的级别也可能更改并重排已编译代码，这可能使其更难与调试器一起使用。

有效选项为：

* `0`：无优化
* `1`：基本优化
* `2`：一些优化
* `3`：全部优化
* `"s"`：为二进制大小优化
* `"z"`：为二进制大小优化，但也关闭循环向量化。

建议试验不同级别以为你的项目找到合适的平衡。可能有令人惊讶的结果，例如级别 `3` 比 `2` 更慢，或 `"s"` 与 `"z"` 级别不一定更小。随着较新版本的 `rustc` 改变优化行为，你可能还想随时间重新评估你的设置。

关于更高级的优化技术，另见 [Profile Guided Optimization]。

[`-C opt-level` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#opt-level
[Profile Guided Optimization]: https://doc.rust-lang.org/rustc/profile-guided-optimization.html

### debug {#debug}
`debug` 设置控制 [`-C debuginfo` 标志][`-C debuginfo` flag]，后者控制包含在已编译二进制中的调试信息量。

有效选项为：

* `0`、`false` 或 `"none"`：完全无调试信息，[`release`](#release) 的默认值
* `"line-directives-only"`：仅行信息指令。对于 nvptx* 目标，这启用[性能分析][profiling]。对于其他用例，`line-tables-only` 是更好、更兼容的选择。
* `"line-tables-only"`：仅行表。生成用于回溯的最少量调试信息（带文件名/行号信息），但不包含其他任何内容，即无变量或函数参数信息。
* `1` 或 `"limited"`：不含类型或变量级信息的调试信息。生成比 `line-tables-only` 更详细的模块级信息。
* `2`、`true` 或 `"full"`：完整调试信息，[`dev`](#dev) 的默认值

关于每个选项的作用的更多信息，见 `rustc` 关于 [debuginfo] 的文档。

你可能还希望根据需要配置 [`split-debuginfo`](#split-debuginfo) 选项。

> **MSRV：** `none`、`limited`、`full`、`line-directives-only` 与 `line-tables-only` 需要 1.71

[`-C debuginfo` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#debuginfo
[debuginfo]: https://doc.rust-lang.org/rustc/codegen-options/index.html#debuginfo
[profiling]: https://reviews.llvm.org/D46061

### split-debuginfo {#split-debuginfo}
`split-debuginfo` 设置控制 [`-C split-debuginfo` 标志][`-C split-debuginfo` flag]，后者控制若生成调试信息，是将其放在可执行文件本身中还是其旁边。

此选项是字符串，可接受的值与[编译器接受][`-C split-debuginfo` flag]的相同。对于已启用调试信息的配置文件，此选项在 macOS 上的默认值为 `unpacked`。否则此选项的默认值在 [rustc 文档中说明][`-C split-debuginfo` flag]，且是平台特定的。某些选项仅在 [nightly 通道][nightly channel]上可用。一旦完成更多测试且对 DWARF 的支持稳定后，Cargo 默认值将来可能会更改。

请注意 Cargo 与 rustc 对此选项有不同的默认值。此选项的存在是为了允许 Cargo 试验不同的标志组合，从而提供更好的调试与开发体验。

[nightly channel]: https://doc.rust-lang.org/book/appendix-07-nightly-rust.html
[`-C split-debuginfo` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#split-debuginfo

### strip {#strip}
`strip` 选项控制 [`-C strip` 标志][`-C strip` flag]，它指示 rustc 从二进制中剥离符号或 debuginfo。可以这样启用：

```toml
[package]
# ...
[profile.release]
strip = "debuginfo"
```

`strip` 可能的字符串值为 `"none"`、`"debuginfo"` 与 `"symbols"`。
默认值为 `"none"`。

你也可以用布尔值 `true` 或 `false` 配置此选项。
`strip = true` 等价于 `strip = "symbols"`。`strip = false` 等价于 `strip = "none"` 并完全禁用 `strip`。

[`-C strip` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#strip

### debug-assertions {#debug-assertions}
`debug-assertions` 设置控制 [`-C debug-assertions` 标志][`-C debug-assertions` flag]，它打开或关闭 `cfg(debug_assertions)` [条件编译][conditional compilation]。调试断言旨在包含仅在调试/开发构建中可用的运行时验证。这些可能是在发布构建中过于昂贵或不受欢迎的东西。调试断言启用标准库中的 [`debug_assert!` 宏][`debug_assert!` macro]。

有效选项为：

* `true`：启用
* `false`：禁用

[`-C debug-assertions` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#debug-assertions
[conditional compilation]: https://doc.rust-lang.org/reference/conditional-compilation.md#debug_assertions
[`debug_assert!` macro]: https://doc.rust-lang.org/std/macro.debug_assert.html

### overflow-checks {#overflow-checks}
`overflow-checks` 设置控制 [`-C overflow-checks` 标志][`-C overflow-checks` flag]，它控制[运行时整数溢出][runtime integer overflow]的行为。启用 overflow-checks 时，溢出将发生 panic。

有效选项为：

* `true`：启用
* `false`：禁用

[`-C overflow-checks` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#overflow-checks
[runtime integer overflow]: https://doc.rust-lang.org/reference/expressions/operator-expr.md#overflow

### lto {#lto}
`lto` 设置控制 `rustc` 的 [`-C lto`]、[`-C linker-plugin-lto`] 与 [`-C embed-bitcode`] 选项，它们控制 LLVM 的[链接时优化][link time optimizations]。LTO 可使用全程序分析产生更好优化的代码，代价是更长的链接时间。

有效选项为：

* `true` 或 `"fat"`：执行「fat」LTO，尝试跨依赖图中的所有 crate 执行优化。
* `"thin"`：执行 [「thin」LTO]["thin" LTO]。这与「fat」类似，但运行时间显著更短，同时仍能实现与「fat」类似的性能增益。
* `false`：执行「thin local LTO」，仅对本地 crate 跨其 [codegen units](#codegen-units) 执行「thin」LTO。若 codegen units 为 1 或 [opt-level](#opt-level) 为 0，则不执行 LTO。
* `"off"`：禁用 LTO。

若你对跨语言 LTO 感兴趣，见 [linker-plugin-lto 章节][linker-plugin-lto chapter]。
Cargo 尚未原生支持这一点，但可通过 `RUSTFLAGS` 执行。

[`-C lto`]: https://doc.rust-lang.org/rustc/codegen-options/index.html#lto
[link time optimizations]: https://llvm.org/docs/LinkTimeOptimization.html
[`-C linker-plugin-lto`]: https://doc.rust-lang.org/rustc/codegen-options/index.html#linker-plugin-lto
[`-C embed-bitcode`]: https://doc.rust-lang.org/rustc/codegen-options/index.html#embed-bitcode
[linker-plugin-lto chapter]: https://doc.rust-lang.org/rustc/linker-plugin-lto.html
["thin" LTO]: http://blog.llvm.org/2016/06/thinlto-scalable-and-incremental-lto.html

### panic {#panic}
`panic` 设置控制 [`-C panic` 标志][`-C panic` flag]，它控制使用哪种 panic 策略。

有效选项为：

* `"unwind"`：在 panic 时展开栈。
* `"abort"`：在 panic 时终止进程。

当设为 `"unwind"` 时，实际值取决于目标平台的默认值。例如，NVPTX 平台不支持展开，因此它始终使用 `"abort"`。

测试、基准测试、构建脚本与 proc macros 忽略 `panic` 设置。`rustc` 测试 harness 目前需要 `unwind` 行为。见启用 `abort` 行为的 [`panic-abort-tests`] 不稳定标志。

此外，当使用 `abort` 策略并构建测试时，所有依赖也将被迫以 `unwind` 策略构建。

[`-C panic` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#panic
[`panic-abort-tests`]: ../17-unstable-features/#panic-abort-tests

### incremental {#incremental}
`incremental` 设置控制 [`-C incremental` 标志][`-C incremental` flag]，它控制是否启用增量编译。增量编译使 `rustc` 将额外信息保存到磁盘，这些信息在重新编译 crate 时将被重用，从而改善重新编译时间。额外信息存储在 `target` 目录中。

有效选项为：

* `true`：启用
* `false`：禁用

增量编译仅用于工作空间成员与「path」依赖。

增量值可用 `CARGO_INCREMENTAL` [环境变量][environment variable]或 [`build.incremental`] 配置变量全局覆盖。

[`-C incremental` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#incremental
[environment variable]: ../07-environment-variables/
[`build.incremental`]: ../06-configuration/#buildincremental

### codegen-units {#codegen-units}
`codegen-units` 设置控制 [`-C codegen-units` 标志][`-C codegen-units` flag]，它控制一个 crate 将被拆分为多少个「代码生成单元」。更多的代码生成单元允许更多 crate 内容并行处理，可能缩短编译时间，但可能产生更慢的代码。

此选项接受大于 0 的整数。

对于[增量](#incremental)构建，默认值为 256；对于非增量构建，默认值为 16。

[`-C codegen-units` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#codegen-units

### rpath {#rpath}
`rpath` 设置控制 [`-C rpath` 标志][`-C rpath` flag]，它控制是否启用 [`rpath`]。

[`-C rpath` flag]: https://doc.rust-lang.org/rustc/codegen-options/index.html#rpath
[`rpath`]: https://en.wikipedia.org/wiki/Rpath

## 默认配置文件 {#default-profiles}
### dev {#dev}

`dev` 配置文件用于正常开发与调试。它是像 [`cargo build`] 这样的构建命令的默认值，并用于 `cargo install --debug`。

`dev` 配置文件的默认设置为：

```toml
[profile.dev]
opt-level = 0
debug = true
split-debuginfo = '...'  # 平台特定。
strip = "none"
debug-assertions = true
overflow-checks = true
lto = false
panic = 'unwind'
incremental = true
codegen-units = 256
rpath = false
```

### release {#release}

`release` 配置文件旨在用于发布与生产中的优化产物。使用 `--release` 标志时使用此配置文件，并且它是 [`cargo install`] 的默认值。

`release` 配置文件的默认设置为：

```toml
[profile.release]
opt-level = 3
debug = false
split-debuginfo = '...'  # 平台特定。
strip = "none"
debug-assertions = false
overflow-checks = false
lto = false
panic = 'unwind'
incremental = false
codegen-units = 16
rpath = false
```

### test {#test}
`test` 配置文件是 [`cargo test`] 使用的默认配置文件。

`test` 配置文件的默认设置为：

```toml
[profile.test]
inherits = "dev"
```

### bench {#bench}
`bench` 配置文件是 [`cargo bench`] 使用的默认配置文件。

`bench` 配置文件的默认设置为：

```toml
[profile.bench]
inherits = "release"
```

### 构建依赖 {#build-dependencies}
为了快速编译，默认情况下所有配置文件都不优化构建依赖（构建脚本、proc macros 及其依赖），并在构建依赖不用作运行时依赖时避免计算调试信息。构建覆盖的默认设置为：

```toml
[profile.dev.build-override]
opt-level = 0
codegen-units = 256
debug = false # 在可能时

[profile.release.build-override]
opt-level = 0
codegen-units = 256
```

然而，若运行构建依赖时发生错误，在需要时打开完整调试信息将改善回溯与可调试性：

```toml
debug = true
```

否则，构建依赖从正在使用的活动配置文件继承设置，如[配置文件选择](#profile-selection)中所述。

## 自定义配置文件 {#custom-profiles}
除内置配置文件外，还可以定义额外的自定义配置文件。这些对于设置多个工作流与构建模式可能很有用。定义自定义配置文件时，必须指定 `inherits` 键，以指定在未指定设置时自定义配置文件从哪个配置文件继承设置。

例如，假设你想比较正常的 release 构建与带有 [LTO](#lto) 优化的 release 构建，你可以在 `Cargo.toml` 中指定类似以下内容：

```toml
[profile.release-lto]
inherits = "release"
lto = true
```

然后可使用 `--profile` 标志选择此自定义配置文件：

```console
cargo build --profile release-lto
```

每个配置文件的输出将放在 [`target` 目录][`target` directory]中与配置文件同名的目录中。如上例所示，输出将进入 `target/release-lto` 目录。

[`target` directory]: ../09-build-cache/

## 配置文件选择 {#profile-selection}

使用的配置文件取决于命令、像 `--release` 或 `--profile` 这样的命令行标志，以及包（在[覆盖](#overrides)的情况下）。若未指定，默认配置文件为：

| 命令 | 默认配置文件 |
|---------|-----------------|
| [`cargo run`]、[`cargo build`]、<br>[`cargo check`]、[`cargo rustc`] | [`dev` 配置文件](#dev) |
| [`cargo test`] | [`test` 配置文件](#test)
| [`cargo bench`] | [`bench` 配置文件](#bench)
| [`cargo install`] | [`release` 配置文件](#release)

你可以使用 `--profile=NAME` 选项切换到不同的配置文件，它将使用给定的配置文件。`--release` 标志等价于 `--profile=release`。

所选配置文件适用于所有 Cargo 目标，包括[库](../the-manifest-format/01-cargo-targets/#library)、[二进制](../the-manifest-format/01-cargo-targets/#binaries)、[示例](../the-manifest-format/01-cargo-targets/#examples)、[测试](../the-manifest-format/01-cargo-targets/#tests)与[基准测试](../the-manifest-format/01-cargo-targets/#benchmarks)。

特定包的配置文件可用下文描述的[覆盖](#overrides)指定。

[`cargo bench`]: ../../cargo-commands/build-commands/01-cargo-bench/
[`cargo build`]: ../../cargo-commands/build-commands/02-cargo-build/
[`cargo check`]: ../../cargo-commands/build-commands/03-cargo-check/
[`cargo install`]: ../../cargo-commands/package-commands/02-cargo-install/
[`cargo run`]: ../../cargo-commands/build-commands/11-cargo-run/
[`cargo rustc`]: ../../cargo-commands/build-commands/12-cargo-rustc/
[`cargo test`]: ../../cargo-commands/build-commands/14-cargo-test/

## 覆盖 {#overrides}

可为特定包与构建时 crate 覆盖配置文件设置。要覆盖特定包的设置，使用 `package` 表更改命名包的设置：

```toml
# `foo` 包将使用 -Copt-level=3 标志。
[profile.dev.package.foo]
opt-level = 3
```

包名实际上是[包 ID 规范](../10-package-id-specifications/)，因此你可以用诸如 `[profile.dev.package."foo:2.1.0"]` 的语法针对包的个别版本。

要覆盖所有依赖（但不是任何工作空间成员）的设置，使用 `"*"` 包名：

```toml
# 为依赖设置默认值。
[profile.dev.package."*"]
opt-level = 2
```

要覆盖构建脚本、proc macros 及其依赖的设置，使用 `build-override` 表：

```toml
# 为构建脚本与 proc-macros 设置设置。
[profile.dev.build-override]
opt-level = 3
```

> 注意：当依赖既是普通依赖又是构建依赖时，在未指定 `--target` 时 Cargo 将尝试只构建它一次。使用 `build-override` 时，该依赖可能需要构建两次，一次作为普通依赖，一次使用覆盖的构建设置。这可能增加初始构建时间。

使用哪个值的优先级按以下顺序进行（第一个匹配获胜）：

1. `[profile.dev.package.name]` —— 命名包。
2. `[profile.dev.package."*"]` —— 对于任何非工作空间成员。
3. `[profile.dev.build-override]` —— 仅用于构建脚本、proc macros 及其依赖。
4. `[profile.dev]` —— `Cargo.toml` 中的设置。
5. Cargo 内置的默认值。

覆盖不能指定 `panic`、`lto` 或 `rpath` 设置。

### 覆盖与泛型 {#overrides-and-generics}
泛型代码实例化的位置将影响用于该泛型代码的优化设置。这会在使用配置文件覆盖更改特定 crate 的优化级别时导致微妙的交互。若你尝试提高定义泛型函数的依赖的优化级别，那些泛型函数在你的本地 crate 中使用时可能不会被优化。这是因为代码可能在其实例化的 crate 中生成，因此可能使用该 crate 的优化设置。

例如，[nalgebra] 是一个大量使用泛型参数定义向量与矩阵的库。若你的本地代码定义了具体的 nalgebra 类型如 `Vector4<f64>` 并使用其方法，对应的 nalgebra 代码将在你的 crate 内实例化并构建。因此，若你尝试使用配置文件覆盖提高 `nalgebra` 的优化级别，可能不会带来更快的性能。

进一步复杂化该问题的是，`rustc` 有一些优化会尝试在 crate 之间共享单态化的泛型。若 opt-level 为 2 或 3，则 crate 不会使用来自其他 crate 的单态化泛型，也不会导出本地定义的单态化项以与其他 crate 共享。在试验为开发优化依赖时，考虑尝试 opt-level 1，它会应用一些优化，同时仍允许共享单态化项。

[nalgebra]: https://crates.io/crates/nalgebra
