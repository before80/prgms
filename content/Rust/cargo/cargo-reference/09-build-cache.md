+++
title = "09-构建缓存"
date = 2026-07-30T14:49:00+08:00
weight = 46
type = "docs"
description = "target 目录与共享构建缓存"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 构建缓存 {#build-cache}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/build-cache.html](https://doc.rust-lang.org/cargo/reference/build-cache.html)


Cargo 将构建输出存放到「target」与「build」目录中。默认情况下，这两个目录都指向你的 [*工作空间*][def-workspace] 根目录下名为 `target` 的目录。要更改 target-dir 的位置，可以设置 `CARGO_TARGET_DIR` [环境变量]、[`build.target-dir`] 配置值，或 `--target-dir` 命令行标志。要更改 build-dir 的位置，可以设置 `CARGO_BUILD_BUILD_DIR` [环境变量] 或 [`build.build-dir`] 配置值。

产物分为两类：
* 最终构建产物
  * 最终构建产物是面向 Cargo 终端用户的输出
  * 例如：bin crate 的二进制文件、`cargo doc` 的输出、Cargo `--timings` 报告
  * 存放在 target-dir 中
* 中间构建产物
  * 中间构建产物供 Cargo 与 Rust 编译器内部使用
  * 终端用户通常无需与中间构建产物交互
  * 存放在 Cargo 的 build-dir 中

目录布局取决于你是否使用 `--target` 标志为特定平台构建。若未指定 `--target`，Cargo 以面向宿主机架构的模式运行。输出进入目标目录根下，每个 [配置文件（profile）][profile] 存放在独立子目录中：

目录 | 说明
----------|------------
<code style="white-space: nowrap">target/debug/</code> | 包含 `dev` 配置文件的输出。
<code style="white-space: nowrap">target/release/</code> | 包含 `release` 配置文件的输出（使用 `--release` 选项时）。
<code style="white-space: nowrap">target/foo/</code> | 包含 `foo` 配置文件的构建输出（使用 `--profile=foo` 选项时）。

出于历史原因，`dev` 与 `test` 配置文件存放在 `debug` 目录中，`release` 与 `bench` 配置文件存放在 `release` 目录中。用户自定义配置文件存放在与配置文件同名的目录中。

使用 `--target` 为另一目标构建时，输出放在以 [目标][target] 命名的目录中：

目录 | 示例
----------|--------
<code style="white-space: nowrap">target/&lt;triple&gt;/debug/</code> | <code style="white-space: nowrap">target/thumbv7em-none-eabihf/debug/</code>
<code style="white-space: nowrap">target/&lt;triple&gt;/release/</code> | <code style="white-space: nowrap">target/thumbv7em-none-eabihf/release/</code>

> **注意**：不使用 `--target` 时，会产生一个后果：Cargo 会与构建脚本和过程宏共享你的依赖。[`RUSTFLAGS`] 会与每一次 `rustc` 调用共享。使用 `--target` 标志时，构建脚本和过程宏会单独构建（面向宿主机架构），并且不共享 `RUSTFLAGS`。

在配置文件目录内（例如 `debug` 或 `release`），产物放置在以下目录中：

目录 | 说明
----------|------------
<code style="white-space: nowrap">target/debug/</code> | 包含正在构建的包的输出（[二进制可执行文件][binary executables] 与 [库目标][library targets]）。
<code style="white-space: nowrap">target/debug/examples/</code> | 包含 [示例目标][example targets]。

部分命令会将输出放在 `target` 目录顶层的专用目录中：

目录 | 说明
----------|------------
<code style="white-space: nowrap">target/doc/</code> | 包含 rustdoc 文档（[`cargo doc`]）。
<code style="white-space: nowrap">target/package/</code> | 包含 [`cargo package`] 的输出。

Cargo 还会在 build-dir 中创建若干构建过程所需的其他目录与文件。build-dir 的布局被视为 Cargo 内部实现，可能变更。其中一些目录为：

目录 | 说明
----------|------------
<code style="white-space: nowrap">\<build-dir>/debug/deps/</code> | 依赖与其他产物。
<code style="white-space: nowrap">\<build-dir>/debug/incremental/</code> | `rustc` [增量输出][incremental output]，用于加速后续构建的缓存。
<code style="white-space: nowrap">\<build-dir>/debug/build/</code> | [构建脚本][build scripts] 的输出。

## Dep-info 文件 {#dep-info-files}
每个编译产物旁有一个后缀为 `.d` 的「dep info」文件。该文件采用类似 Makefile 的语法，标明重建该产物所需的全部文件依赖。它们旨在供外部构建系统使用，以便检测是否需要重新执行 Cargo。文件中的路径默认是绝对路径。参见 [`build.dep-info-basedir`] 配置选项以使用相对路径。

```Makefile
# 位于 target/debug/foo.d 的 dep-info 文件示例
/path/to/myproj/target/debug/foo: /path/to/myproj/src/lib.rs /path/to/myproj/src/main.rs
```

## 共享缓存 {#shared-cache}
第三方工具 [sccache] 可用于在不同工作空间之间共享已构建的依赖。

要设置 `sccache`，用 `cargo install sccache` 安装它，并在调用 Cargo 之前将 `RUSTC_WRAPPER` 环境变量设为 `sccache`。若使用 bash，可在 `.bashrc` 中添加 `export RUSTC_WRAPPER=sccache`。也可以在 [Cargo 配置][config] 中设置 [`build.rustc-wrapper`]。更多细节请参阅 sccache 文档。

[`RUSTFLAGS`]: ../06-configuration/#buildrustflags
[`build.dep-info-basedir`]: ../06-configuration/#builddep-info-basedir
[`build.rustc-wrapper`]: ../06-configuration/#buildrustc-wrapper
[`build.target-dir`]: ../06-configuration/#buildtarget-dir
[`build.build-dir`]: ../06-configuration/#buildbuild-dir
[`cargo doc`]: ../../cargo-commands/build-commands/06-cargo-doc/
[`cargo package`]: ../../cargo-commands/publishing-commands/04-cargo-package/
[`cargo publish`]: ../../cargo-commands/publishing-commands/05-cargo-publish/
[build scripts]: ../build-scripts/
[config]: ../06-configuration/
[def-workspace]: ../../appendix/01-glossary/#workspace
[target]: ../../appendix/01-glossary/#target
[environment variable]: ../07-environment-variables/
[incremental output]: ../05-profiles/#incremental
[sccache]: https://github.com/mozilla/sccache
[profile]: ../05-profiles/
[binary executables]: ../the-manifest-format/01-cargo-targets/#binaries
[library targets]: ../the-manifest-format/01-cargo-targets/#library
[example targets]: ../the-manifest-format/01-cargo-targets/#examples
