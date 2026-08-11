+++
title = "17-不稳定特性"
date = 2026-07-30T14:49:00+08:00
weight = 59
type = "docs"
description = "nightly 不稳定 Cargo 特性一览"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 不稳定特性


> 原文链接: [https://doc.rust-lang.org/cargo/reference/unstable.html](https://doc.rust-lang.org/cargo/reference/unstable.html)


实验性的 Cargo 特性只在 [nightly 渠道][nightly channel] 上可用。我们鼓励你试用这些特性，
看看它们是否满足你的需求，以及是否存在问题或缺陷。更多关于某个特性的信息，请查看下面列出的
跟踪 issue 链接；如果你希望获得后续更新，可以点击 GitHub 上的 subscribe 按钮。

经过一段时间之后，如果该特性没有重大问题，它就可能被[稳定化][stabilized]。一旦当前的 nightly
版本流转到 stable 渠道（大约需要 6 到 12 周），该特性就会在 stable 上可用。

根据特性的工作方式不同，共有三种启用不稳定特性的途径：

* `Cargo.toml` 中的新语法要求在 `Cargo.toml` 顶部、任何表（table）之前写上 `cargo-features`
  键。例如：

  ```toml
  # 这里指定启用了哪些新的 Cargo.toml 特性。
  cargo-features = ["test-dummy-unstable"]

  [package]
  name = "my-package"
  version = "0.1.0"
  im-a-teapot = true  # 这是由 test-dummy-unstable 启用的新选项。
  ```

* 新的命令行标志、选项和子命令要求同时带上 `-Z unstable-options` 这个 CLI 选项。例如，新的
  `--artifact-dir` 选项只在 nightly 上可用：

  ```cargo +nightly build --artifact-dir=out -Z unstable-options```

* `-Z` 命令行标志用于启用那些可能还没有界面、或者界面尚未设计好的新功能，也用于启用那些会影响
  Cargo 多个部分的复杂特性。例如，[mtime-on-use](#mtime-on-use) 特性可以这样启用：

  ```cargo +nightly build -Z mtime-on-use```

  运行 `cargo -Z help` 可以查看可用标志的列表。

  凡是能用 `-Z` 标志配置的东西，也都可以在 cargo 的[配置文件][config file]
  （`.cargo/config.toml`）的 `unstable` 表中设置。例如：

  ```toml
  [unstable]
  mtime-on-use = true
  build-std = ["core", "alloc"]
  ```

下面描述的每个新特性都会说明如何使用它。

*关于最新的 nightly，请参见本页的 [nightly 版本][nightly version]。*

[config file]: ../06-configuration/
[nightly channel]: https://doc.rust-lang.org/book/appendix-07-nightly-rust.html
[stabilized]: https://doc.crates.io/contrib/process/unstable.html#stabilization
[nightly version]: https://doc.rust-lang.org/nightly/cargo/reference/unstable.html

## 不稳定特性列表 {#list-of-unstable-features}
* 不稳定特性本身相关
    * [-Z allow-features](#allow-features) --- 提供一种限制可使用哪些不稳定特性的方式。
* 构建脚本与链接
    * [Metabuild](#metabuild) --- 提供声明式的构建脚本。
    * [Multiple Build Scripts](#multiple-build-scripts) --- 允许使用多个构建脚本。
    * [Any Build Script Metadata](#any-build-script-metadata) --- 允许任意构建脚本通过 `cargo::metadata=key=value` 指定环境变量。
* 解析器与特性（features）
    * [no-index-update](#no-index-update) --- 阻止 cargo 更新索引缓存。
    * [avoid-dev-deps](#avoid-dev-deps) --- 阻止解析器在解析过程中纳入 dev-dependencies。
    * [minimal-versions](#minimal-versions) --- 强制解析器使用最低的兼容版本，而不是最高版本。
    * [direct-minimal-versions](#direct-minimal-versions) — 强制解析器使用最低的兼容版本，而不是最高版本。
    * [public-dependency](#public-dependency) --- 允许把依赖归类为 public 或 private。
    * [msrv-policy](#msrv-policy) --- 感知 MSRV 的解析器与版本选择。
    * [precise-pre-release](#precise-pre-release) --- 允许通过 `update --precise` 选中预发布版本。
    * [sbom](#sbom) --- 为编译产物生成 SBOM 前置（pre-cursor）文件。
    * [update-breaking](#update-breaking) --- 允许用 `update --breaking` 升级到破坏性版本。
    * [feature-unification](#feature-unification) --- 在工作空间中启用新的特性统一（feature unification）模式。
    * [lockfile-publish-time](#lockfile-publish-time) --- 将解析器限制为早于指定时间的包。
    * [min-publish-age](#min-publish-age) --- 过滤掉发布时间比配置的最小年龄更晚的依赖版本。
* 输出行为
    * [artifact-dir](#artifact-dir) --- 增加一个用于拷贝构建产物的目录。
    * [build-dir-new-layout](#build-dir-new-layout) --- 启用新的 build-dir 文件系统布局。
    * [Different binary name](#different-binary-name) --- 为构建出的二进制指定一个与 crate 名称无关的名字。
    * [root-dir](#root-dir) --- 控制打印路径时所参照的根目录。
* 编译行为
    * [mtime-on-use](#mtime-on-use) --- 每次使用依赖时更新其最后修改时间戳，从而提供一种删除无用产物的机制。
    * [build-std](#build-std) --- 构建标准库，而不是使用预编译的二进制。
    * [build-std-features](#build-std-features) --- 设置构建标准库时使用的特性。
    * [binary-dep-depinfo](#binary-dep-depinfo) --- 让 dep-info 文件追踪二进制依赖。
    * [checksum-freshness](#checksum-freshness) --- 传入该标志后，判断某个 crate 是否需要重新构建将基于文件校验和而非文件 mtime。
    * [panic-abort-tests](#panic-abort-tests) --- 允许以 "abort" panic 策略运行测试。
    * [host-config](#host-config) --- 允许为宿主构建目标设置类似 `[target]` 的配置项。
    * [embed-metadata](#embed-metadata) --- 若设为 `no`，cargo 会向编译器传递 `-Zembed-metadata=no`，从而避免把元数据嵌入 rlib 和 dylib 产物，以节省磁盘空间。
    * [target-applies-to-host](#target-applies-to-host) --- 改变某些标志是否会传递给宿主构建目标。
    * [gc](#gc) --- 全局缓存垃圾回收。
    * [open-namespaces](#open-namespaces) --- 允许多个包参与同一个 API 命名空间。
    * [panic-immediate-abort](#panic-immediate-abort) --- 向编译器传递 `-Cpanic=immediate-abort`。
    * [compile-time-deps](#compile-time-deps) --- 为 rust-analyzer 准备的永久不稳定特性。
    * [fine-grain-locking](#fine-grain-locking) --- 使用细粒度锁，而不是锁住整个构建缓存。
    * [json-target-spec](#json-target-spec) --- 允许使用 `.json` 自定义目标规范。
    * [hint-msrv](#hint-msrv) --- 允许 Cargo 设置 `-Zhint-msrv`。
* rustdoc
    * [rustdoc-map](#rustdoc-map) --- 提供文档映射，使其能链接到 [docs.rs](https://docs.rs/) 等外部站点。
    * [scrape-examples](#scrape-examples) --- 在文档中展示示例。
    * [output-format](#output-format-for-rustdoc) --- 允许文档同时以实验性的 [JSON 格式](https://doc.rust-lang.org/nightly/nightly-rustc/rustdoc_json_types/) 输出。
    * [rustdoc-depinfo](#rustdoc-depinfo) --- 在 rustdoc 的重建检测中使用 dep-info 文件。
    * [rustdoc-mergeable-info](#rustdoc-mergeable-info) --- 使用 rustdoc 的可合并跨 crate 信息文件。
* `Cargo.toml` 扩展
    * [Profile `rustflags` option](#profile-rustflags-option) --- 直接传递给 rustc。
    * [Profile `hint-mostly-unused` option](#profile-hint-mostly-unused-option) --- 提示某个依赖大部分用不到，以优化编译时间。
    * [codegen-backend](#codegen-backend) --- 选择 rustc 使用的代码生成后端。
    * [per-package-target](#per-package-target) --- 为每个单独的包设置所用的 `--target`。
    * [artifact dependencies](#artifact-dependencies) --- 允许把构建产物包含进其他构建产物，并为不同目标构建它们。
    * [Profile `trim-paths` option](#profile-trim-paths-option) --- 控制构建输出中文件路径的净化（sanitization）。
    * [`[lints.cargo]`](#lintscargo) --- 允许为 Cargo 配置 lint。
    * [path bases](#path-bases) --- 为路径依赖提供具名的基准目录。
    * [`unstable-editions`](#unstable-editions) --- 允许使用尚未稳定的版次（edition）。
* 信息与元数据
    * [unit-graph](#unit-graph) --- 以 JSON 形式输出 Cargo 的内部图结构。
    * [`cargo rustc --print`](#rustc---print) --- 以 `--print` 调用 rustc，以显示来自 rustc 的信息。
    * [Build analysis](#build-analysis) --- 跨多次运行记录并持久化详细的构建指标，并提供查询过往构建的新命令。
    * [`rustc-unicode`](#rustc-unicode) --- 在 Cargo 的错误信息中启用 `rustc` 的 unicode 错误格式。
* 配置
    * [`cargo config`](#cargo-config) --- 新增一个用于查看配置文件的子命令。
* 注册表（Registries）
    * [publish-timeout](#publish-timeout) --- 控制从上传 crate 到它在索引中可用之间的超时时间。
    * [asymmetric-token](#asymmetric-token) --- 增加对使用非对称密码学的认证令牌的支持（`cargo:paseto` 提供者）。
* 其他
    * [gitoxide](#gitoxide) --- 对一组操作使用 `gitoxide` 而不是 `git2`。
    * [script](#script) --- 启用对单文件 `.rs` 包的支持。
    * [native-completions](#native-completions) --- 把 cargo 的 shell 补全迁移到原生补全。
    * [Package message format](#package-message-format) --- `cargo package` 的消息格式。
    * [`fix-edition`](#fix-edition) --- 一个永久不稳定的版次迁移辅助工具。
    * [Plumbing subcommands](https://github.com/crate-ci/cargo-plumbing) --- 底层命令，作为 Cargo 的 API 使用，类似 `cargo metadata`。

## allow-features {#allow-features}
这个永久不稳定的标志使得只有列出的那部分不稳定特性可以被使用。具体来说，如果你传入
`-Zallow-features=foo,bar`，你仍然可以向 `cargo` 传递 `-Zfoo` 和 `-Zbar`，但无法传递
`-Zbaz`。你可以传入空字符串（`-Zallow-features=`）来禁用所有不稳定特性。

`-Zallow-features` 同样限制了可以传给 `Cargo.toml` 中 `cargo-features` 条目的不稳定特性。
例如，如果你想允许

```toml
cargo-features = ["test-dummy-unstable"]
```

其中 `test-dummy-unstable` 是不稳定的，那么该特性同样会被 `-Zallow-features=` 禁止，而通过
`-Zallow-features=test-dummy-unstable` 才会被允许。

传给 cargo 的 `-Zallow-features` 特性列表也会被传递给 cargo 最终调用的所有 Rust 工具（例如
`rustc` 或 `rustdoc`）。因此，如果你运行 `cargo -Zallow-features=`，就不能使用任何不稳定的
Cargo _或_ Rust 特性。

## no-index-update {#no-index-update}
* 最初的 Issue：[#3479](https://github.com/rust-lang/cargo/issues/3479)
* 跟踪 Issue：[#7404](https://github.com/rust-lang/cargo/issues/7404)

`-Z no-index-update` 标志确保 Cargo 不会尝试更新注册表索引。它的目标用户是像 Crater 这样会
发出大量 Cargo 命令的工具——你希望避免每次都因更新索引而产生网络延迟。

## mtime-on-use {#mtime-on-use}
* 最初的 Issue：[#6477](https://github.com/rust-lang/cargo/pull/6477)
* 缓存使用情况元跟踪 Issue：[#7150](https://github.com/rust-lang/cargo/issues/7150)

`-Z mtime-on-use` 标志是一项实验：让 Cargo 更新所用文件的 mtime，以便 cargo-sweep 之类的
工具更容易检测出哪些文件已经过时。对许多工作流而言，这需要在 *所有* cargo 调用上都设置该标志。
为了让这更实用，在 `.cargo/config.toml` 中设置 `unstable.mtime_on_use` 标志或设置对应的环境
变量，就会把 `-Z mtime-on-use` 应用到所有 nightly cargo 的调用上。（该配置标志会被 stable 忽略。）

## avoid-dev-deps {#avoid-dev-deps}
* 最初的 Issue：[#4988](https://github.com/rust-lang/cargo/issues/4988)
* 跟踪 Issue：[#5133](https://github.com/rust-lang/cargo/issues/5133)

在运行诸如 `cargo install` 或 `cargo build` 之类的命令时，目前 Cargo 要求下载 dev-dependencies，
即使它们并未被使用。`-Z avoid-dev-deps` 标志允许 Cargo 在不需要时避免下载 dev-dependencies。
如果跳过了 dev-dependencies，就不会生成 `Cargo.lock` 文件。

## minimal-versions {#minimal-versions}
* 最初的 Issue：[#4100](https://github.com/rust-lang/cargo/issues/4100)
* 跟踪 Issue：[#5657](https://github.com/rust-lang/cargo/issues/5657)

> 注意：不推荐使用该特性。因为它会对所有传递依赖强制使用最小版本，而并非所有外部依赖都声明了
> 正确的版本下界，所以它的用处有限。未来计划将其改为只对直接依赖强制最小版本。

在生成 `Cargo.lock` 文件时，`-Z minimal-versions` 标志会把依赖解析到满足需求的最小 SemVer
版本（而不是最大版本）。

该标志的预期用途是在持续集成中检查：Cargo.toml 中指定的版本是否正确反映了你实际使用的最小版本。
也就是说，如果 Cargo.toml 写的是 `foo = "1.0.0"`，你不会不小心依赖了只在 `foo 1.5.0` 中才
加入的特性。

## direct-minimal-versions {#direct-minimal-versions}
* 最初的 Issue：[#4100](https://github.com/rust-lang/cargo/issues/4100)
* 跟踪 Issue：[#5657](https://github.com/rust-lang/cargo/issues/5657)

在生成 `Cargo.lock` 文件时，`-Z direct-minimal-versions` 标志会仅针对直接依赖，把依赖解析到
满足需求的最小 SemVer 版本（而不是最大版本）。

该标志的预期用途是在持续集成中检查：Cargo.toml 中指定的版本是否正确反映了你实际使用的最小版本。
也就是说，如果 Cargo.toml 写的是 `foo = "1.0.0"`，你不会不小心依赖了只在 `foo 1.5.0` 中才
加入的特性。

间接依赖仍按常规方式解析，以免被它们的最小版本校验所阻塞。

## artifact-dir {#artifact-dir}
* 最初的 Issue：[#4875](https://github.com/rust-lang/cargo/issues/4875)
* 跟踪 Issue：[#6790](https://github.com/rust-lang/cargo/issues/6790)

该特性允许你指定构建完成后产物被拷贝到哪个目录。通常产物只会写入 `target/release` 或
`target/debug` 目录，但要确定确切的文件名会比较麻烦，因为你需要解析 JSON 输出。
`--artifact-dir` 标志让访问产物变得更可预期。注意产物是被拷贝过去的，原件仍然留在 `target`
目录中。示例：

```sh
cargo +nightly build --artifact-dir=out -Z unstable-options
```

这也可以在 `.cargo/config.toml` 文件中指定。

```toml
[build]
artifact-dir = "out"
```

## root-dir {#root-dir}
* 最初的 Issue：[#9887](https://github.com/rust-lang/cargo/issues/9887)
* 跟踪 Issue：无（目前没有稳定化计划）

`-Zroot-dir` 标志设置打印路径时所参照的根目录。它同时影响诊断信息以及 `file!()` 宏输出的路径。

## Metabuild {#metabuild}
* 跟踪 Issue：[rust-lang/rust#49803](https://github.com/rust-lang/rust/issues/49803)
* RFC：[#2196](https://github.com/rust-lang/rfcs/blob/master/text/2196-metabuild.md)

Metabuild 是一项提供声明式构建脚本的特性。你不再需要编写 `build.rs` 脚本，而是在 `Cargo.toml`
的 `metabuild` 键中指定一组构建依赖。Cargo 会自动生成一个构建脚本，按顺序运行每个构建依赖。
Metabuild 包随后可以从 `Cargo.toml` 中读取元数据来决定自己的行为。

在 `Cargo.toml` 顶部加入 `cargo-features`，在 `package` 中加入 `metabuild` 键，在
`build-dependencies` 中列出依赖，并在 `package.metadata` 下添加 metabuild 包所需的任何元数据。
示例：

```toml
cargo-features = ["metabuild"]

[package]
name = "mypackage"
version = "0.0.1"
metabuild = ["foo", "bar"]

[build-dependencies]
foo = "1.0"
bar = "1.0"

[package.metadata.foo]
extra-info = "qwerty"
```

Metabuild 包应当提供一个名为 `metabuild` 的公开函数，执行常规 `build.rs` 脚本会执行的相同动作。

## Multiple Build Scripts {#multiple-build-scripts}
* 跟踪 Issue：[#14903](https://github.com/rust-lang/cargo/issues/14903)
* 最初的 Pull Request：[#15630](https://github.com/rust-lang/cargo/pull/15630)

多构建脚本特性允许你在包中拥有多个构建脚本。

在 `Cargo.toml` 顶部加入 `cargo-features` 并添加 `multiple-build-scripts` 以启用该特性。
把构建脚本的路径以数组形式写在 `package.build` 中。例如：

```toml
cargo-features = ["multiple-build-scripts"]

[package]
name = "mypackage"
version = "0.0.1"
build = ["foo.rs", "bar.rs"]
```

**访问输出目录**：每个构建脚本的输出目录可以通过 `<script-name>_OUT_DIR` 访问，其中
`<script-name>` 是该构建脚本文件名的主干部分（file stem），保持原样不变。
例如，位于 `foo/bar.rs` 的脚本对应 `bar_OUT_DIR`。（只在编译期间设置，可通过 `env!` 宏访问。）

## Any Build Script Metadata {#any-build-script-metadata}
* 跟踪 Issue：[#14903](https://github.com/rust-lang/cargo/issues/3544)

允许任意构建脚本通过 `cargo::metadata=key=value` 指定环境变量。

依赖方的构建脚本可以在运行时读取 `CARGO_DEP_<dep>_<key>` 环境变量来获取这些键值对。
对于带有 `links` 的 crate 的构建脚本，`DEP_<links>_<key>` 和 `CARGO_DEP_<dep>_<key>` 都会被设置。

注意，`CARGO_DEP_<dep>_<key>` 中的 `dep` 和 `key` 会被转为大写，并把连字符（`-`）替换为下划线（`_`）。

## public-dependency {#public-dependency}
* 跟踪 Issue：[#44663](https://github.com/rust-lang/rust/issues/44663)

'public-dependency' 特性允许把依赖标记为 'public' 或 'private'。启用该特性后，会向 rustc
传递额外信息，使得 [exported_private_dependencies](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#exported-private-dependencies)
lint 能够正常工作。

要启用该特性，你可以使用 `-Zpublic-dependency`

```sh
cargo +nightly run -Zpublic-dependency
```

或者使用 `[unstable]` 表，例如：

```toml
# .cargo/config.toml
[unstable]
public-dependency = true
```

`public-dependency` 也可以在 `cargo-features` 中启用，**不过这种方式已被弃用，并将很快移除**。

```toml
cargo-features = ["public-dependency"]

[dependencies]
my_dep = { version = "1.2.3", public = true }
private_dep = "2.0.0" # 默认为 'private'
```

文档更新：
- 在工作空间的「`dependencies` 表」一节中，把 `public` 列为 `workspace.dependencies` 不支持的字段
- 使用 `public` 所需的 MSRV 为 1.83（见 [#14507](https://github.com/rust-lang/cargo/pull/14507)）

## msrv-policy {#msrv-policy}
- [RFC：感知 MSRV 的解析器](https://rust-lang.github.io/rfcs/3537-msrv-resolver.html)
- [#9930](https://github.com/rust-lang/cargo/issues/9930)（感知 MSRV 的解析器）

这是 [RFC 2495](https://github.com/rust-lang/rfcs/pull/2495) 之下所有「感知 MSRV」的 cargo
特性的总括性不稳定特性。

### 感知 MSRV 的 cargo add {#msrv-aware-cargo-add}
该功能已在 1.79 中通过 [#13608](https://github.com/rust-lang/cargo/pull/13608) 稳定化。

### 感知 MSRV 的解析器 {#msrv-aware-resolver}
该功能已在 1.84 中通过 [#14639](https://github.com/rust-lang/cargo/pull/14639) 稳定化。

### 把 `incompatible_toolchain` 错误转换为 lint {#convert-incompatible_toolchain-error-into-a-lint}
尚未实现。

### 为 `cargo add`、`cargo update` 提供 `--update-rust-version` 标志 {#--update-rust-version-flag-for-cargo-add-cargo-update}
尚未实现。

### `package.rust-version = "toolchain"` {#packagerust-version-toolchain}
尚未实现。

### 更新 `cargo new` 模板以设置 `package.rust-version = "toolchain"` {#update-cargo-new-template-to-set-packagerust-version-toolchain}
尚未实现。

## precise-pre-release {#precise-pre-release}
* 跟踪 Issue：[#13290](https://github.com/rust-lang/cargo/issues/13290)
* RFC：[#3493](https://github.com/rust-lang/rfcs/pull/3493)

`precise-pre-release` 特性允许通过 `update --precise` 选中预发布版本，即使项目的 `Cargo.toml`
中并未指定预发布版本。

以这个 `Cargo.toml` 为例。

```toml
[dependencies]
my-dependency = "0.1.1"
```

可以用 `update -Zunstable-options my-dependency --precise 0.1.2-pre.0` 把 `my-dependency`
更新到某个预发布版本。这是因为 `0.1.2-pre.0` 被认为与 `0.1.1` 兼容。
但用同样的方式无法从 `0.1.1` 升级到 `0.2.0-pre.0`。

## sbom {#sbom}
* 跟踪 Issue：[#13709](https://github.com/rust-lang/cargo/pull/13709)
* RFC：[#3553](https://github.com/rust-lang/rfcs/pull/3553)

`sbom` 构建配置允许在每个编译产物旁边生成所谓的 SBOM 前置（pre-cursor）文件。软件物料清单
（SBOM）工具可以利用这些生成的文件，从 cargo 构建过程中收集那些难以或无法通过其他方式获取的
重要信息。

要启用该特性，可以在 `.cargo/config.toml` 中设置 `sbom` 字段

```toml
[unstable]
sbom = true

[build]
sbom = true
```

或者把 `CARGO_BUILD_SBOM` 环境变量设为 `true`。该功能位于 `-Z sbom` 标志之后。

生成的输出文件为 JSON 格式，遵循 `<artifact>.cargo-sbom.json` 的命名方案。该 JSON 文件包含
依赖、目标、特性以及所用 `rustc` 编译器的信息。

对于所有被提升（uplift）到 target 或 artifact 目录的可执行与可链接输出，都会生成 SBOM 前置文件。

### Cargo 为 crate 设置的环境变量 {#environment-variables-cargo-sets-for-crates}
* `CARGO_SBOM_PATH` -- 生成的 SBOM 前置文件列表，以平台的 PATH 分隔符分隔。该列表可用
  `std::env::split_paths` 拆分。

### SBOM 前置文件的 schema {#sbom-pre-cursor-schema}
```json5
{
  // Schema 版本。
  "version": 1,
  // 根 crate 在 crates 数组中的索引。
  "root": 0,
  // 所有 crate 的数组。如果同一个 crate 以不同方式编译（不同的 opt-level、
  // features 等），可能会出现重复项。
  "crates": [
    {
      // 完全限定的包 ID 规范
      "id": "path+file:///sample-package#0.1.0",
      // 目标种类列表：bin、lib、rlib、dylib、cdylib、staticlib、proc-macro、example、test、bench、custom-build
      "kind": ["bin"],
      // 已启用的特性标志。
      "features": [],
      // 该 crate 的依赖。
      "dependencies": [
        {
          // 在 crates 数组中的索引。
          "index": 1,
          // 依赖种类：
          // Normal：链接到该 crate 所生成产物的依赖。
          // Build：用于构建该 crate 的编译期依赖（构建脚本或过程宏）。
          "kind": "normal"
        },
        {
          // 一个 crate 可以同时通过 normal 边和 build 边依赖另一个 crate。
          "index": 1,
          "kind": "build"
        }
      ]
    },
    {
      "id": "registry+https://github.com/rust-lang/crates.io-index#zerocopy@0.8.16",
      "kind": ["bin"],
      "features": [],
      "dependencies": []
    }
  ],
  // 执行本次编译所用 rustc 的信息。
  "rustc": {
    // 编译器版本
    "version": "1.86.0-nightly",
    // 编译器包装器（wrapper）
    "wrapper": null,
    // 工作空间编译器包装器
    "workspace_wrapper": null,
    // rustc 的提交哈希
    "commit_hash": "bef3c3b01f690de16738b1c9f36470fbfc6ac623",
    // 宿主目标三元组
    "host": "x86_64-pc-windows-msvc",
    // 详细版本字符串：`rustc -vV`
    "verbose_version": "rustc 1.86.0-nightly (bef3c3b01 2025-02-04)\nbinary: rustc\ncommit-hash: bef3c3b01f690de16738b1c9f36470fbfc6ac623\ncommit-date: 2025-02-04\nhost: x86_64-pc-windows-msvc\nrelease: 1.86.0-nightly\nLLVM version: 19.1.7\n"
  }
}
```

## update-breaking {#update-breaking}
* 跟踪 Issue：[#12425](https://github.com/rust-lang/cargo/issues/12425)

允许使用 `--breaking` 标志把 `Cargo.toml` 中的依赖版本需求升级到 SemVer 不兼容的版本。

这只适用于满足以下条件的依赖：
- 该包是某个工作空间成员的依赖
- 该依赖没有被重命名
- 存在 SemVer 不兼容的可用版本
- 使用了「SemVer 运算符」（`^`，也就是默认行为）

用户还可以在命令行上指定包名，以进一步限制哪些包会被升级。

示例：
```console
$ cargo +nightly -Zunstable-options update --breaking
$ cargo +nightly -Zunstable-options update --breaking clap
```

*它的定位与 [cargo-upgrade](https://github.com/killercup/cargo-edit/) 类似。*

## build-std {#build-std}
* 跟踪仓库：<https://github.com/rust-lang/wg-cargo-std-aware>

`build-std` 特性让 Cargo 能够把标准库本身作为 crate 图编译的一部分来编译。该特性在历史上也
被称为「std-aware Cargo」。这项特性目前仍处于非常早期的开发阶段，同时也可能是 Cargo 的一次
大规模特性扩充。即便只按今天已有的最小形态来写，它也是一个非常庞大的待记录特性；因此，如果你
想持续了解最新进展，可以关注[跟踪仓库](https://github.com/rust-lang/wg-cargo-std-aware)及
其下的一系列 issue。

目前已实现的功能位于名为 `-Z build-std` 的标志之后。该标志表示 Cargo 应当使用与主构建相同的
profile，从源码编译标准库。注意，要让它工作，你需要有标准库的源码；目前唯一受支持的获取方式是
添加 `rust-src` 这个 rustup 组件：

```console
$ rustup component add rust-src --toolchain nightly
```

用法如下：

```console
$ cargo new foo
$ cd foo
$ cargo +nightly run -Z build-std --target x86_64-unknown-linux-gnu
   Compiling core v0.0.0 (...)
   ...
   Compiling foo v0.1.0 (...)
    Finished dev [unoptimized + debuginfo] target(s) in 21.00s
     Running `target/x86_64-unknown-linux-gnu/debug/foo`
Hello, world!
```

这里我们以 debug 模式并开启 debug assertions 重新编译了标准库（就像编译 `src/main.rs` 那样），
最后把所有东西链接在一起。

使用 `-Z build-std` 会隐式编译 `core`、`std`、`alloc` 和 `proc_macro` 这几个稳定的 crate。
如果你使用 `cargo test`，它还会编译 `test` crate。如果你所处的环境不支持其中某些 crate，
可以给 `-Zbuild-std` 传入参数：

```console
$ cargo +nightly build -Z build-std=core,alloc
```

这里的值是以逗号分隔的、要构建的标准库 crate 列表。

### 使用要求 {#requirements}
概括来说，今天使用 `-Z build-std` 的要求如下：

* 你必须通过 `rustup component add rust-src` 安装 libstd 的源码
* 你必须同时使用 nightly 的 Cargo 和 nightly 的 rustc
* 所有 `cargo` 调用都必须传入 `-Z build-std` 标志。

### 报告缺陷与参与贡献 {#reporting-bugs-and-helping-out}
`-Z build-std` 特性还处在非常早期的开发阶段！这项 Cargo 特性有着极其漫长的历史、涉及范围也
非常广，而现在只是个开始。如果你想报告缺陷，可以提交到：

* Cargo --- <https://github.com/rust-lang/cargo/issues/new> --- 用于实现层面的缺陷
* 跟踪仓库 ---
  <https://github.com/rust-lang/wg-cargo-std-aware/issues/new> --- 用于更宏观的设计问题。

另外，如果你希望看到某个尚未实现的功能，或者某些东西的行为不符合你的预期，欢迎查看跟踪仓库的
[issue 跟踪器](https://github.com/rust-lang/wg-cargo-std-aware/issues)；如果那里没有，
请提交一个新的 issue！

## build-std-features {#build-std-features}
* 跟踪仓库：<https://github.com/rust-lang/wg-cargo-std-aware>

这个标志是 `-Zbuild-std` 特性标志的姊妹项。它用于配置在构建标准库时，标准库自身启用哪些特性。
目前默认启用的特性是 `backtrace` 和 `panic-unwind`。该标志接受以逗号分隔的列表；一旦提供，
就会覆盖默认启用的特性列表。

## binary-dep-depinfo {#binary-dep-depinfo}
* rustc 跟踪 Issue：[#63012](https://github.com/rust-lang/rust/issues/63012)

`-Z binary-dep-depinfo` 标志会让 Cargo 把同样的标志转发给 `rustc`，从而让 `rustc` 在
「dep info」文件（扩展名为 `.d`）中包含所有二进制依赖的路径。Cargo 随后利用这些信息进行变更
检测（只要任何二进制依赖发生变化，该 crate 就会被重新构建）。主要用例是构建编译器本身，因为
它对标准库有隐式依赖，而这些依赖在其他情况下不会被变更检测追踪到。

## checksum-freshness {#checksum-freshness}
* 跟踪 Issue：[#14136](https://github.com/rust-lang/cargo/issues/14136)

`-Z checksum-freshness` 标志会用文件校验和取代 cargo 指纹（fingerprint）中对文件 mtime 的
使用。这在 mtime 实现较差的系统上，或者在 CI/CD 中最为有用。校验和算法可能在 cargo 各版本之间
无预告地变化。Cargo 使用指纹来判断某个 crate 何时需要重新构建。

目前，即便启用了 `checksum-freshness`，被构建脚本读取的文件仍会继续使用 mtime。这并不是一个
长期方案。

## panic-abort-tests {#panic-abort-tests}
* 跟踪 Issue：[#67650](https://github.com/rust-lang/rust/issues/67650)
* 最初的 Pull Request：[#7460](https://github.com/rust-lang/cargo/pull/7460)

`-Z panic-abort-tests` 标志会启用 nightly 上以 `-Cpanic=abort` 编译测试框架 crate 的支持。
若没有该标志，Cargo 会以 `-Cpanic=unwind` 编译测试及其所有依赖，因为这是 `test` 这个 crate
唯一知道如何工作的方式。不过，自 [rust-lang/rust#64158] 起，`test` crate 支持以「每个测试
一个进程」的方式使用 `-C panic=abort`，这有助于避免多次编译整个 crate 图。

目前尚不清楚该特性会以何种方式在 Cargo 中稳定化，但我们希望以某种方式把它稳定下来！

[rust-lang/rust#64158]: https://github.com/rust-lang/rust/pull/64158

## target-applies-to-host {#target-applies-to-host}
* 最初的 Pull Request：[#9322](https://github.com/rust-lang/cargo/pull/9322)
* 跟踪 Issue：[#9453](https://github.com/rust-lang/cargo/issues/9453)

历史上，对于构建脚本、插件以及其他 _始终_ 为宿主平台构建的产物，Cargo 是否遵循来自环境变量和
[`[target]`](../06-configuration/#target) 的 `linker` 与 `rustflags` 配置项，其行为一直
不太一致。
当 _没有_ 传入 `--target` 时，Cargo 对构建脚本使用与所有其他编译产物相同的 `linker` 和
`rustflags`。而当 _传入了_ `--target` 时，Cargo 会遵循
[`[target.<host triple>]`](../06-configuration/#targettriplelinker) 中的 `linker`，
并且不会采纳任何 `rustflags` 配置。
这种双重行为令人困惑，同时也让那些「宿主三元组与[目标三元组][target triple]恰好相同、但打算
在构建宿主上运行的产物仍需要不同配置」的构建难以正确配置。

`-Ztarget-applies-to-host` 启用 Cargo 配置文件中的顶层 `target-applies-to-host` 设置，
允许用户选择对这些属性采用不同（也更一致）的行为。当配置文件中未设置 `target-applies-to-host`
或将其设为 `true` 时，保留现有的 Cargo 行为（不过请参见 `-Zhost-config`，它会改变该默认值）。
当它被设为 `false` 时，无论是否向 Cargo 传入 `--target`，宿主产物都不会采纳来自
`[target.<host triple>]`、`RUSTFLAGS` 或 `[build]` 的任何选项。要定制打算在宿主上运行的
产物，请使用 `[host]`（见 [`host-config`](#host-config)）。

未来 `target-applies-to-host` 可能最终会默认为 `false`，以提供更合理、更一致的默认行为。

```toml
# config.toml
target-applies-to-host = false
```

```console
cargo +nightly -Ztarget-applies-to-host build --target x86_64-unknown-linux-gnu
```

## host-config {#host-config}
* 最初的 Pull Request：[#9322](https://github.com/rust-lang/cargo/pull/9322)
* 跟踪 Issue：[#9452](https://github.com/rust-lang/cargo/issues/9452)

配置文件中的 `host` 键可用于向宿主构建目标传递标志，例如那些在交叉编译时必须在宿主系统而非目标
系统上运行的构建脚本。它同时支持通用表和特定宿主架构的表。匹配的宿主架构表优先于通用的 host 表。

它要求设置 `-Zhost-config` 和 `-Ztarget-applies-to-host` 命令行选项，并且在 Cargo 配置文件中
设置 `target-applies-to-host = false`。

```toml
# config.toml
[host]
linker = "/path/to/host/linker"
runner = "host-runner"
[host.x86_64-unknown-linux-gnu]
linker = "/path/to/host/arch/linker"
runner = "host-arch-runner"
rustflags = ["-Clink-arg=--verbose"]
[target.x86_64-unknown-linux-gnu]
linker = "/path/to/target/linker"
```

`host.runner` 设置用于包裹宿主构建目标（如构建脚本）的执行过程，类似于
`target.<triple>.runner` 包裹 `cargo run`/`test`/`bench` 的方式。

在 `x86_64-unknown-linux-gnu` 宿主上构建时，上面通用的 `host` 表会被完全忽略，因为
`host.x86_64-unknown-linux-gnu` 表优先级更高。

设置 `-Zhost-config` 会把 `target-applies-to-host` 的默认值从 `true` 改为 `false`。

```console
cargo +nightly -Ztarget-applies-to-host -Zhost-config build --target x86_64-unknown-linux-gnu
```

## unit-graph {#unit-graph}
* 跟踪 Issue：[#8002](https://github.com/rust-lang/cargo/issues/8002)

`--unit-graph` 标志可以传给任意构建命令（`build`、`check`、`run`、`test`、`bench`、`doc` 等），
它会向 stdout 输出一个表示 Cargo 内部单元图（unit graph）的 JSON 对象。实际上不会构建任何东西，
命令在打印完之后立即返回。每个「单元（unit）」对应一次编译器的执行。这些对象还包含每个单元所依赖
的其他单元。

```
cargo +nightly build --unit-graph -Z unstable-options
```

这个结构能更完整地呈现 Cargo 所看到的依赖关系。特别地，"features" 字段支持新的特性解析器——在
新解析器下，同一个依赖可以以不同的特性集被构建多次。`cargo metadata` 从根本上无法表达不同依赖
种类之间的特性关系，而且特性现在还取决于运行的是哪个命令、选择了哪些包和目标。此外，它还能提供
包内部依赖（如构建脚本或测试）的细节。

以下是该 JSON 结构的说明：

```javascript
{
  /* JSON 输出结构的版本。如果做出任何向后不兼容的更改，
     该值都会递增。
  */
  "version": 1,
  /* 所有构建单元的数组。 */
  "units": [
    {
      /* 一个表示该包的不透明字符串。
         关于该包的信息可以通过 `cargo metadata` 获取。
      */
      "pkg_id": "my-package 0.1.0 (path+file:///path/to/my-package)",
      /* Cargo 目标。关于这些字段的更多信息，
         请参阅 `cargo metadata` 的文档。
         https://doc.rust-lang.org/cargo/commands/cargo-metadata.html
      */
      "target": {
        "kind": ["lib"],
        "crate_types": ["lib"],
        "name": "my_package",
        "src_path": "/path/to/my-package/src/lib.rs",
        "edition": "2018",
        "test": true,
        "doctest": true
      },
      /* 该单元的 profile 设置。
         这些值可能与清单中定义的 profile 不一致。
         单元可以使用被修改过的 profile 设置。例如，对测试而言
         "panic" 设置可能被覆盖为强制使用 "unwind"。
      */
      "profile": {
        /* 这些设置所派生自的 profile 名称。 */
        "name": "dev",
        /* 以字符串表示的优化级别。 */
        "opt_level": "0",
        /* 以字符串表示的 LTO 设置。 */
        "lto": "false",
        /* 以整数表示的 codegen units。
           若为 `null` 则表示应使用编译器的默认值。
        */
        "codegen_units": null,
        /* 以整数表示的调试信息级别。
           若为 `null` 则表示应使用编译器的默认值（0）。
        */
        "debuginfo": 2,
        /* 是否启用了 debug-assertions。 */
        "debug_assertions": true,
        /* 是否启用了 overflow-checks。 */
        "overflow_checks": true,
        /* 是否启用了 rpath。 */
        "rpath": false,
        /* 是否启用了增量编译。 */
        "incremental": true,
        /* panic 策略，"unwind" 或 "abort"。 */
        "panic": "unwind"
      },
      /* 该目标是为哪个平台构建的。
         值为 `null` 表示是为宿主构建的。
         否则是一个目标三元组字符串（例如
         "x86_64-unknown-linux-gnu"）。
      */
      "platform": null,
      /* 该单元的 "mode"。有效值：

         * "test" --- 使用 `rustc` 以测试方式构建。
         * "build" --- 使用 `rustc` 构建。
         * "check" --- 使用 `rustc` 以 "check" 模式构建。
         * "doc" --- 使用 `rustdoc` 构建。
         * "doctest" --- 使用 `rustdoc` 测试。
         * "run-custom-build" --- 表示执行一个构建脚本。
      */
      "mode": "build",
      /* 该单元上启用的特性（字符串）数组。 */
      "features": ["somefeat"],
      /* 该单元是否是标准库单元，
         属于不稳定的 build-std 特性的一部分。
         若未设置，按 `false` 处理。
      */
      "is_std": false,
      /* 该单元的依赖数组。 */
      "dependencies": [
        {
          /* 该依赖在 "units" 数组中的索引。 */
          "index": 1,
          /* 引用该依赖时所使用的名称。 */
          "extern_crate_name": "unicode_xid",
          /* 该依赖是否为 "public"，
             属于不稳定的 public-dependency 特性的一部分。
             若未设置，表示未启用 public-dependency 特性。
          */
          "public": false,
          /* 该依赖是否被注入到 prelude 中，
             目前由 build-std 特性使用。
             若未设置，按 `false` 处理。
          */
          "noprelude": false
        }
      ]
    },
    // ...
  ],
  /* "units" 数组中作为依赖图「根」的那些单元的索引数组。
  */
  "roots": [0],
}
```

## Profile `rustflags` option {#profile-rustflags-option}
* 最初的 Issue：[rust-lang/cargo#7878](https://github.com/rust-lang/cargo/issues/7878)
* 跟踪 Issue：[rust-lang/cargo#10271](https://github.com/rust-lang/cargo/issues/10271)

该特性在 `[profile]` 段中提供了一个新选项，用于指定直接传递给 rustc 的标志。
可以这样启用：

```toml
cargo-features = ["profile-rustflags"]

[package]
# ...
[profile.release]
rustflags = [ "-C", "..." ]
```

若要在 Cargo 配置中的 profile 里设置该选项，你需要使用 `-Z profile-rustflags` 或 `[unstable]`
表来启用它。例如：

```toml
# .cargo/config.toml
[unstable]
profile-rustflags = true

[profile.release]
rustflags = [ "-C", "..." ]
```

## Profile `hint-mostly-unused` option {#profile-hint-mostly-unused-option}
* 跟踪 Issue：[#15644](https://github.com/rust-lang/cargo/issues/15644)

该特性在 `[profile]` 段中提供了一个新选项，用于启用 rustc 的 `hint-mostly-unused` 选项。
它主要适用于为特定依赖启用：

```toml
[profile.dev.package.huge-mostly-unused-dependency]
hint-mostly-unused = true
```

要启用该特性，请传入 `-Zprofile-hint-mostly-unused`。不过，由于该选项只是一个提示（hint），
在不传 `-Zprofile-hint-mostly-unused` 的情况下使用它只会产生警告并忽略该 profile 选项。
在该特性引入之前的 Cargo 版本会给出「unused manifest key」警告，但除此之外仍能正常工作、
不会报错。这使得你可以在某个 crate 的 `Cargo.toml` 中使用该提示，而不必强制要求使用更新版本的
Cargo 来构建它。

一个 crate 也可以通过 `[hints]` 表自动为依赖它的 crate 提供该提示（同样会被较老的 Cargo 忽略）：

```toml
[hints]
mostly-unused = true
```

这会让该 crate 默认启用 hint-mostly-unused，除非通过 `profile` 覆盖——`profile` 优先级更高，
并且只能在被构建的顶层 crate 中指定。

## rustdoc-map {#rustdoc-map}
* 跟踪 Issue：[#8296](https://github.com/rust-lang/cargo/issues/8296)

该特性新增了一些会传递给 `rustdoc` 的配置项，使得当某个依赖没有被生成文档时，rustdoc 仍能生成
指向该依赖文档托管地址的链接。首先，把下面的内容加入 `.cargo/config`：

```toml
[doc.extern-map.registries]
crates-io = "https://docs.rs/"
```

然后，在构建文档时使用下面的标志，使依赖链接指向 [docs.rs](https://docs.rs/)：

```
cargo +nightly doc --no-deps -Zrustdoc-map
```

`registries` 表包含从注册表名称到目标链接 URL 的映射。该 URL 中可以带有 `{pkg_name}` 和
`{version}` 标记，它们会被替换为相应的值。如果两者都没有指定，Cargo 会默认在 URL 末尾追加
`{pkg_name}/{version}/`。

还有一个配置项可用于重定向标准库链接。默认情况下，rustdoc 会创建指向
<https://doc.rust-lang.org/nightly/> 的链接。要改变这一行为，请使用 `doc.extern-map.std`
设置：

```toml
[doc.extern-map]
std = "local"
```

值为 `"local"` 表示链接到 `rustc` sysroot 中的文档。如果你使用 rustup，可以通过
`rustup component add rust-docs` 安装这些文档。

默认值是 `"remote"`。

该值也可以是指向自定义位置的 URL。

## per-package-target {#per-package-target}
* 跟踪 Issue：[#9406](https://github.com/rust-lang/cargo/pull/9406)
* 最初的 Pull Request：[#9030](https://github.com/rust-lang/cargo/pull/9030)
* 最初的 Issue：[#7004](https://github.com/rust-lang/cargo/pull/7004)

`per-package-target` 特性为清单增加了两个键：`package.default-target` 和
`package.forced-target`。前者让该包默认（即没有传 `--target` 参数时）为某个目标编译；
后者让该包始终为该目标编译。

示例：

```toml
[package]
forced-target = "wasm32-unknown-unknown"
```

在这个例子中，该 crate 始终为 `wasm32-unknown-unknown` 构建，例如因为它将作为插件被某个运行在
宿主（或命令行指定）目标上的主程序使用。

## artifact-dependencies {#artifact-dependencies}
* 跟踪 Issue：[#9096](https://github.com/rust-lang/cargo/pull/9096)
* 最初的 Pull Request：[#9992](https://github.com/rust-lang/cargo/pull/9992)

产物依赖（artifact dependencies）允许 Cargo 包依赖 `bin`、`cdylib` 和 `staticlib` 类型的
crate，并在编译期使用这些 crate 构建出的产物。

运行 `cargo` 时带上 `-Z bindeps` 即可启用该功能。

### artifact-dependencies：依赖声明 {#artifact-dependencies-dependency-declarations}
产物依赖为 `Cargo.toml` 中的依赖声明增加了以下键：

- `artifact` --- 指定要构建的 [Cargo 目标](../the-manifest-format/01-cargo-targets/)。
  通常在没有该字段时，Cargo 只会构建依赖中的 `[lib]` 目标。
  该字段允许指定要构建哪个目标，并在构建时以二进制形式提供：

  * `"bin"` --- 编译出的可执行二进制，对应依赖清单中所有的 `[[bin]]` 段。
  * `"bin:<bin-name>"` --- 编译出的可执行二进制，对应由给定 `<bin-name>` 指定的某个特定二进制目标。
  * `"cdylib"` --- 与 C 兼容的动态库，对应依赖清单中带 `crate-type = ["cdylib"]` 的 `[lib]` 段。
  * `"staticlib"` --- 与 C 兼容的静态库，对应依赖清单中带 `crate-type = ["staticlib"]` 的 `[lib]` 段。

  `artifact` 的值可以是一个字符串，也可以是一个字符串数组，以指定多个目标。

  示例：

  ```toml
  [dependencies]
  bar = { version = "1.0", artifact = "staticlib" }
  zoo = { version = "1.0", artifact = ["bin:cat", "bin:dog"]}
  ```

- `lib` --- 这是一个布尔值，表示是否同时把该依赖的库作为普通的 Rust `lib` 依赖来构建。
  该字段只能在指定了 `artifact` 时使用。

  指定 `artifact` 时，该字段默认为 `false`。
  如果设为 `true`，那么该依赖的 `[lib]` 目标也会为声明方所构建的平台目标进行构建。
  这样一来，该包除了把它当作产物依赖之外，还能像普通依赖一样在 Rust 代码中使用它。

  示例：

  ```toml
  [dependencies]
  bar = { version = "1.0", artifact = "bin", lib = true }
  ```

- `target` --- 构建该依赖所针对的平台目标。
  该字段只能在指定了 `artifact` 时使用。

  未指定时的默认值取决于依赖种类。
  对于构建依赖，它会为宿主目标构建。
  对于其他所有依赖，它会为声明方所构建的相同目标构建。

  对于构建依赖，该字段还可以取特殊值 `"target"`，表示为该包正在构建的相同目标构建该依赖。

  ```toml
  [build-dependencies]
  bar = { version = "1.0", artifact = "cdylib", target = "wasm32-unknown-unknown"}
  same-target = { version = "1.0", artifact = "bin", target = "target" }
  ```

### artifact-dependencies：环境变量 {#artifact-dependencies-environment-variables}
构建完产物依赖之后，Cargo 会提供以下环境变量，供你访问这些产物：

- `CARGO_<ARTIFACT-TYPE>_DIR_<DEP>` --- 包含该依赖全部产物的目录。

  `<ARTIFACT-TYPE>` 是为该依赖指定的 `artifact`（转为大写，如 `CDYLIB`、`STATICLIB` 或 `BIN`），
  `<DEP>` 是该依赖的名称。
  与其他 Cargo 环境变量一样，依赖名会被转为大写，并把连字符替换为下划线。

  如果你的清单对该依赖做了重命名，`<DEP>` 对应你指定的名称，而不是原始包名。

- `CARGO_<ARTIFACT-TYPE>_FILE_<DEP>_<NAME>` --- 该产物的完整路径。

  `<ARTIFACT-TYPE>` 是为该依赖指定的 `artifact`（按上述规则转为大写），`<DEP>` 是该依赖的名称
  （按上述规则转换），`<NAME>` 则是来自该依赖的产物名称。

  注意 `<NAME>` 相对于提供该产物的 crate 中指定的 `name`（若未指定则为 crate 名）没有做任何
  修改；例如，它可能是小写的，或者包含连字符。

  为方便起见，如果产物名称与原始包名相同，cargo 还会额外提供一份省略了 `_<NAME>` 后缀的同名变量。
  例如，如果 `cmake` crate 提供了一个名为 `cmake` 的二进制，Cargo 会同时提供
  `CARGO_BIN_FILE_CMAKE` 和 `CARGO_BIN_FILE_CMAKE_cmake`。

对于每一种依赖，这些变量会被提供给构建过程中能够访问该类依赖的相应环节：

- 对于 build-dependencies，这些变量会提供给 `build.rs` 脚本，可通过
  [`std::env::var_os`](https://doc.rust-lang.org/std/env/fn.var_os.html) 访问。
  （与任何操作系统文件路径一样，它们不一定是合法的 UTF-8。）
- 对于普通依赖，这些变量在编译该 crate 期间提供，可通过 [`env!`] 宏访问。
- 对于 dev-dependencies，这些变量在编译示例、测试和基准测试期间提供，可通过 [`env!`] 宏访问。

[`env!`]: https://doc.rust-lang.org/std/macro.env.html

### artifact-dependencies：示例 {#artifact-dependencies-examples}
#### 示例：在构建脚本中使用二进制可执行文件 {#example-use-a-binary-executable-from-a-build-script}
在 `Cargo.toml` 文件中，你可以声明对某个二进制的依赖，使其可供构建脚本使用：

```toml
[build-dependencies]
some-build-tool = { version = "1.0", artifact = "bin" }
```

然后在构建脚本内部，就可以在构建时执行该二进制：

```rust
fn main() {
    let build_tool = std::env::var_os("CARGO_BIN_FILE_SOME_BUILD_TOOL").unwrap();
    let status = std::process::Command::new(build_tool)
        .arg("do-stuff")
        .status()
        .unwrap();
    if !status.success() {
        eprintln!("failed!");
        std::process::exit(1);
    }
}
```

#### 示例：在构建脚本中使用 _cdylib_ 产物 {#example-use-_cdylib_-artifact-in-build-script}
消费方包中的 `Cargo.toml`，把 `bar` 库作为 `cdylib` 为特定构建目标构建……

```toml
[build-dependencies]
bar = { artifact = "cdylib", version = "1.0", target = "wasm32-unknown-unknown" }
```

……以及 `build.rs` 中的构建脚本。

```rust
fn main() {
    wasm::run_file(std::env::var("CARGO_CDYLIB_FILE_BAR").unwrap());
}
```

#### 示例：在二进制中使用 _binary_ 产物及其库 {#example-use-_binary_-artifact-and-its-library-in-a-binary}
消费方包中的 `Cargo.toml`，构建 `bar` 二进制以作为产物引入，同时也把它作为库使用……

```toml
[dependencies]
bar = { artifact = "bin", version = "1.0", lib = true }
```

……以及使用 `main.rs` 的可执行文件。

```rust
fn main() {
    bar::init();
    command::run(env!("CARGO_BIN_FILE_BAR"));
}
```

## publish-timeout {#publish-timeout}
* 跟踪 Issue：[11222](https://github.com/rust-lang/cargo/issues/11222)

配置文件中的 `publish.timeout` 键可用于控制 `cargo publish` 在把包提交到注册表之后，等待它
在本地索引中变为可用的时长。

超时为 `0` 会阻止执行任何检查。当前默认值为 `60` 秒。

它要求设置 `-Zpublish-timeout` 命令行选项。

```toml
# config.toml
[publish]
timeout = 300  # 单位为秒
```

## asymmetric-token {#asymmetric-token}
* 跟踪 Issue：[10519](https://github.com/rust-lang/cargo/issues/10519)
* RFC：[#3231](https://github.com/rust-lang/rfcs/pull/3231)

`-Z asymmetric-token` 标志启用 `cargo:paseto` 凭证提供者，它允许 Cargo 在不通过网络发送密钥
的前提下向注册表进行认证。

在 [`config.toml`](../06-configuration/) 和 `credentials.toml` 文件中有一个名为 `private-key`
的字段，它是以 [`PASERK` 的 secret 子集](https://github.com/paseto-standard/paserk/blob/master/types/secret.md)
格式表示的私钥，用于签名非对称令牌。

可以用 `cargo login --generate-keypair` 生成密钥对，它会：
- 以当前推荐的方式生成一对公钥/私钥。
- 把私钥保存到 `credentials.toml` 中。
- 以 [PASERK public](https://github.com/paseto-standard/paserk/blob/master/types/public.md)
  格式打印公钥。

推荐把 `private-key` 保存在 `credentials.toml` 中。它在 `config.toml` 中也受支持，主要是为了
能通过对应的环境变量来设置——这也是在 CI 环境中提供它的推荐方式。这与我们为设置密钥令牌而提供的
`token` 字段是一致的做法。

还有一个可选字段 `private-key-subject`，它是由注册表选定的字符串。
该字符串会作为非对称令牌的一部分被包含进去，并且不应当是保密的。
它适用于诸如「用密码学方式证明中央 CA 服务器授权了此操作」这类罕见用例。Cargo 要求它是非空白的
可打印 ASCII。需要非 ASCII 数据的注册表应当对其进行 base64 编码。

这两个字段都可以通过 `cargo login --registry=name --private-key --private-key-subject="subject"`
设置，该命令会提示你输入密钥值。

一个注册表最多只能设置 `private-key` 或 `token` 之一。

所有 PASETO 都会包含 `iat`，即 ISO 8601 格式的当前时间。Cargo 会在适当的场合包含以下内容：
- `sub`：可选的、由注册表选定的非机密字符串，预期在每个请求中都会被声明。其值来自 `config.toml`
  文件中的 `private-key-subject`。
- `mutation`：若存在，表示该请求是一个变更操作（不存在则表示只读操作），其值必须是
  `publish`、`yank` 或 `unyank` 之一。
  - `name`：与该请求相关的 crate 名称。
  - `vers`：与该请求相关的 crate 版本字符串。
  - `cksum`：crate 内容的 SHA256 哈希，表示为 64 位小写十六进制数字字符串，仅当 `mutation`
    等于 `publish` 时才必须存在。
- `challenge`：本次会话中从该服务器收到的 401/403 响应里的挑战字符串。发放挑战的注册表必须记录
  哪些挑战已被发放/使用，并且在同一有效期内绝不接受同一个挑战超过一次（这样就不必记录曾经发放过的
  每一个挑战）。

「footer」（它是签名的一部分）将是一个 UTF-8 的 JSON 字符串，包含：
- `url`：cargo 获取 config.json 文件所用的、符合 RFC 3986 的 URL。
  - 如果这是一个使用 HTTP 索引的注册表，那么它就是所有索引查询相对参照的基准 URL。
  - 如果这是一个使用 GIT 索引的注册表，它就是 Cargo 用来克隆索引的 URL。
- `kid`：用于签名该请求的私钥标识符，采用
  [PASERK IDs](https://github.com/paseto-standard/paserk/blob/master/operations/ID.md) 标准。

PASETO 包含了被签名的消息，因此服务器不必为了校验签名而从请求中重建出确切的字符串。服务器需要做的
是检查签名对 PASETO 中的字符串是否有效，以及该字符串的内容是否与请求相符。
如果某个请求本应包含某个声明（claim），但 PASETO 中缺失，那么该请求必须被拒绝。

## `cargo config` {#cargo-config}
* 最初的 Issue：[#2362](https://github.com/rust-lang/cargo/issues/2362)
* 跟踪 Issue：[#9301](https://github.com/rust-lang/cargo/issues/9301)

`cargo config` 子命令提供了一种展示 cargo 所加载配置文件的方式。目前它包含 `get` 子命令，
可以接受一个可选的配置值来展示。

```console
cargo +nightly -Zunstable-options config get build.rustflags
```

如果没有给出配置值，它会展示所有配置值。更多可用选项请参见 `--help` 输出。

## rustc `--print` {#rustc---print}
* 跟踪 Issue：[#9357](https://github.com/rust-lang/cargo/issues/9357)

`cargo rustc --print=VAL` 会把 `--print` 标志转发给 `rustc`，以便从 `rustc` 中提取信息。
它会带上相应的
[`--print`](https://doc.rust-lang.org/rustc/command-line-arguments.html#--print-print-compiler-information)
标志运行 `rustc`，随后立即退出而不进行编译。把它暴露为一个 cargo 标志，可以让 cargo 依据当前
配置注入正确的 target 和 RUSTFLAGS。

主要用例是运行 `cargo rustc --print=cfg`，以获取相应目标的、且受其他 RUSTFLAGS 影响的配置值。


## Different binary name {#different-binary-name}
* 跟踪 Issue：[#9778](https://github.com/rust-lang/cargo/issues/9778)
* PR：[#9627](https://github.com/rust-lang/cargo/pull/9627)

`different-binary-name` 特性允许设置二进制文件的文件名，而不必遵守对 crate 名称的限制。
例如，crate 名称只能使用 `alphanumeric` 字符或 `-`、`_`，并且不能为空。

`filename` 参数**不应**包含二进制的扩展名，`cargo` 会自行推断合适的扩展名并用于该二进制。

`filename` 参数只能在清单的 `[[bin]]` 段中使用。

```toml
cargo-features = ["different-binary-name"]

[package]
name =  "foo"
version = "0.0.1"

[[bin]]
name = "foo"
filename = "007bar"
path = "src/main.rs"
```

## scrape-examples {#scrape-examples}
* RFC：[#3123](https://github.com/rust-lang/rfcs/pull/3123)
* 跟踪 Issue：[#9910](https://github.com/rust-lang/cargo/issues/9910)

`-Z rustdoc-scrape-examples` 标志告诉 Rustdoc 在当前工作空间的 crate 中搜索函数调用。
这些调用点随后会被包含进文档中。你可以这样使用该标志：

```
cargo doc -Z unstable-options -Z rustdoc-scrape-examples
```

默认情况下，Cargo 会从被生成文档的包的 example 目标中抓取示例。
你可以用 `doc-scrape-examples` 标志逐个启用或禁用某些目标被抓取，例如：

```toml
# 启用从库中抓取示例
[lib]
doc-scrape-examples = true

# 禁止从某个 example 目标中抓取示例
[[example]]
name = "my-example"
doc-scrape-examples = false
```

**关于测试的说明：** 在 test 目标上启用 `doc-scrape-examples` 目前不会有任何效果。从测试中抓取
示例的功能仍在开发中。

**关于 dev-dependencies 的说明：** 为库生成文档通常不需要该 crate 的 dev-dependencies。然而，
example 目标需要 dev-deps。为了向后兼容，`-Z rustdoc-scrape-examples` *不会* 为 `cargo doc`
引入 dev-deps 需求。因此，在满足以下条件时，示例 *不会* 从 example 目标中被抓取：

1. 没有任何被生成文档的目标需要 dev-deps，并且
2. 至少有一个含有被生成文档目标的 crate 拥有 dev-deps，并且
3. 所有 `[[example]]` 目标的 `doc-scrape-examples` 参数都未设置或为 false。

如果你希望从 example 目标中抓取示例，那么就必须打破上述条件之一。
例如，你可以把某个 example 目标的 `doc-scrape-examples` 设为 true，这就向 Cargo 表明你接受为
`cargo doc` 构建 dev-deps。

## output-format for rustdoc {#output-format-for-rustdoc}
* 跟踪 Issue：[#13283](https://github.com/rust-lang/cargo/issues/13283)

该标志决定 `cargo rustdoc` 的输出格式，接受 `html` 或 `json`，为工具提供了一种利用
[rustdoc 实验性 JSON 格式](https://doc.rust-lang.org/nightly/nightly-rustc/rustdoc_json_types/)
的方式。

你可以这样使用该标志：

```
cargo rustdoc -Z unstable-options --output-format json
```

## codegen-backend {#codegen-backend}
`codegen-backend` 特性使得可以通过 profile 选择 rustc 所使用的代码生成后端。

示例：

```toml
[package]
name = "foo"

[dependencies]
serde = "1.0.117"

[profile.dev.package.foo]
codegen-backend = "cranelift"
```

若要在 Cargo 配置中的 profile 里设置该选项，你需要使用 `-Z codegen-backend` 或 `[unstable]`
表来启用它。例如：

```toml
# .cargo/config.toml
[unstable]
codegen-backend = true

[profile.dev.package.foo]
codegen-backend = "cranelift"
```

## gitoxide {#gitoxide}
* 跟踪 Issue：[#11813](https://github.com/rust-lang/cargo/issues/11813)

启用 'gitoxide' 不稳定特性后，全部或指定的 git 操作将由 `gitoxide` crate 执行，而不是 `git2`。

`-Zgitoxide` 会启用当前已实现的全部功能，而通过 `-Zgitoxide=operation[,operationN]` 语法，
可以逐个选择哪些 git 操作使用 `gitoxide` 来运行。

有效的操作如下：

* `fetch` - 所有 fetch 都通过 `gitoxide` 完成，包括 git 依赖以及 crate 索引。
* `checkout` *（计划中）* - 检出工作树，支持过滤器和子模块。

## git {#git}
* 跟踪 Issue：[#13285](https://github.com/rust-lang/cargo/issues/13285)

启用 'git' 不稳定特性后，`gitoxide` 和 `git2` 都会对 crate 索引和 git 依赖执行浅克隆（shallow fetch）。

`-Zgit` 会启用当前已实现的全部功能，而通过 `-Zgit=operation[,operationN]` 语法，可以逐个选择
何时执行浅克隆。

有效的操作如下：

* `shallow-index` - 对索引执行浅克隆。
* `shallow-deps` - 对 git 依赖执行浅克隆。

**关于浅克隆的细节**

* 要启用浅克隆，抓取 git 依赖时加上 `-Zgit=shallow-deps`，抓取注册表索引时加上 `-Zgit=shallow-index`。
* 浅克隆和浅检出的 git 仓库会存放在各自带 `-shallow` 后缀的目录中，即：
  - `~/.cargo/registry/index/*-shallow`
  - `~/.cargo/git/db/*-shallow`
  - `~/.cargo/git/checkouts/*-shallow`
* 当该不稳定特性开启时，抓取/克隆 git 仓库始终是浅抓取。这大致相当于处处使用 `git fetch --depth 1`。
* 即使存在 `Cargo.lock` 或指定了某个提交 `{ rev = "…" }`，gitoxide 和 libgit2 依然足够智能，
  可以在不把已有仓库转为完整克隆（unshallow）的前提下执行浅抓取。

## script {#script}
* 跟踪 Issue：[#12207](https://github.com/rust-lang/cargo/issues/12207)

Cargo 可以直接运行 `.rs` 文件：
```console
$ cargo +nightly -Zscript file.rs
```
其中 `file.rs` 可以简单到只有：
```rust
fn main() {}
```

用户还可以在模块级注释中，通过一个 `cargo` 代码围栏（code fence）来指定清单，例如：
````rust
#!/usr/bin/env -S cargo +nightly -Zscript
---cargo
[dependencies]
clap = { version = "4.2", features = ["derive"] }
---

use clap::Parser;

#[derive(Parser, Debug)]
#[clap(version)]
struct Args {
    #[clap(short, long, help = "Path to config")]
    config: Option<std::path::PathBuf>,
}

fn main() {
    let args = Args::parse();
    println!("{:?}", args);
}
````

### 单文件包 {#single-file-packages}
除了今天已有的多文件包（`Cargo.toml` 文件加上其他 `.rs` 文件）之外，我们还引入了单文件包的概念，
它可以包含一个内嵌的清单。单文件 `.rs` 包与任何其他 `.rs` 文件之间没有必须的区分标志。

单文件包可以通过 `--manifest-path` 选择，例如 `cargo test --manifest-path foo.rs`。
与 `Cargo.toml` 不同，这类文件无法被自动发现。

单文件包可以包含一个内嵌清单。内嵌清单以 `TOML` 形式存放在 rust 的「frontmatter」中，也就是位于
文件顶部、infostring 以 `cargo` 开头的 markdown 代码围栏内。

推断/默认的清单字段：
- `package.name = <文件主干名的 slug 化结果>`
- `package.edition = <当前版次>`：避免总是必须添加内嵌清单，代价是脚本可能在 rust 升级时被破坏
  - 当 `edition` 未指定时会发出警告，以提醒用户注意这一点

不允许的清单字段：
- `[workspace]`、`[lib]`、`[[bin]]`、`[[example]]`、`[[test]]`、`[[bench]]`
- `package.workspace`、`package.build`、`package.links`、`package.autolib`、`package.autobins`、`package.autoexamples`、`package.autotests`、`package.autobenches`

单文件包默认的 `CARGO_TARGET_DIR` 位于 `$CARGO_HOME/target/<hash>`：
- 避免同一目录下的多个单文件包彼此冲突
- 避免单文件包的父目录只读所带来的问题
- 避免弄乱用户的目录

单文件包的锁文件会放在 `CARGO_TARGET_DIR` 中。未来在支持工作空间之后，用户将可以拥有一个持久化的
锁文件。

### 清单命令（Manifest-commands） {#manifest-commands}
你可以直接把清单传给 `cargo` 命令而不带子命令，比如 `foo/Cargo.toml`，或者像 `foo.rs` 这样的
单文件包。这主要是为了写在 `#!` 行里使用。

`cargo <subcommand>` 的解释优先级为：
1. 内置命令 与 单文件包（二者互斥）
2. 别名
3. 外部子命令

一个参数在满足以下任一条件时会被识别为清单命令：
- 含有路径分隔符
- 带有 `.rs` 扩展名
- 文件名为 `Cargo.toml`

`cargo run --manifest-path <path>` 与 `cargo <path>` 的区别：
- `cargo <path>` 使用 `<path>` 对应的配置而非当前目录的配置，更类似 `cargo install --path <path>`
- `cargo <path>` 的详细程度低于通常的默认级别。传入 `-v` 可以获得常规输出。

运行带有内嵌清单的包时，
[`arg0`](https://doc.rust-lang.org/std/os/unix/process/trait.CommandExt.html#tymethod.arg0)
将是脚本的路径。要获取可执行文件的路径，请参见
[`current_exe`](https://doc.rust-lang.org/std/env/fn.current_exe.html)。

### 文档更新 {#documentation-updates}
## Profile `trim-paths` option {#profile-trim-paths-option}
* 跟踪 Issue：[rust-lang/cargo#12137](https://github.com/rust-lang/cargo/issues/12137)
* rustc 跟踪 Issue：[rust-lang/rust#111540](https://github.com/rust-lang/rust/issues/111540)

它新增了一个 profile 设置，用于控制最终二进制中的路径如何被净化（sanitize）。
可以这样启用：

```toml
cargo-features = ["trim-paths"]

[package]
# ...
[profile.release]
trim-paths = ["diagnostics", "object"]
```

若要在 Cargo 配置中的 profile 里设置该选项，
你需要使用 `-Z trim-paths` 或 `[unstable]` 表来启用它。
例如：

```toml
# .cargo/config.toml
[unstable]
trim-paths = true

[profile.release]
trim-paths = ["diagnostics", "object"]
```

### 文档更新 {#documentation-updates}
#### trim-paths {#trim-paths}
*作为一个新的[「Profile 设置」条目](../05-profiles/#profile-settings)*

`trim-paths` 是一个 profile 设置，用于启用并控制构建输出中文件路径的净化。
它可以取以下值：

- `"none"` 和 `false` --- 禁用路径净化
- `"macro"` --- 净化 `std::file!()` 宏展开中的路径。
    内嵌的 panic 消息中的路径就来自这里
- `"diagnostics"` --- 净化打印出的编译器诊断信息中的路径
- `"object"` --- 净化编译出的可执行文件或库中的路径
- `"all"` 和 `true` --- 净化所有可能位置的路径

它也接受由 `"macro"`、`"diagnostics"` 和 `"object"` 组合而成的数组。

它在 `dev` profile 下默认为 `none`，在 `release` profile 下默认为 `object`。
你可以在 `Cargo.toml` 中指定该选项来手动覆盖：

```toml
[profile.dev]
trim-paths = "all"

[profile.release]
trim-paths = ["object", "diagnostics"]
```

`release` profile 的默认设置（`object`）只净化输出的可执行文件或库文件中的路径。
它总是会影响来自宏的路径（如 panic 消息），而对调试信息中的路径，只有当它们会与二进制一起被内嵌时
才会受影响（在使用 ELF 二进制的平台上是默认行为，如 Linux 和 windows-gnu）；
如果它们位于独立文件中（Windows MSVC 和 macOS 上的默认行为），则不会被触碰。
但指向这些独立文件的路径会被净化。

如果 `trim-paths` 不是 `none` 或 `false`，那么当以下路径出现在被选中的作用域中时会被净化：

1. 指向标准库与 core 库源文件（sysroot）的路径将以 `/rustc/[rustc commit hash]` 开头，
   例如 `/home/username/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu/lib/rustlib/src/rust/library/core/src/result.rs` ->
   `/rustc/fe72845f7bb6a77b9e671e6a4f32fe714962cec4/library/core/src/result.rs`
2. 指向当前包的路径会被剥离为相对于当前工作空间根目录的形式，例如 `/home/username/crate/src/lib.rs` -> `src/lib.rs`。
3. 指向依赖包的路径会被替换为 `[package name]-[version]`。例如 `/home/username/deps/foo/src/lib.rs` -> `foo-0.1.0/src/lib.rs`

当指向标准库与 core 库源文件的路径 *不在* 净化作用域内时，输出的路径取决于是否安装了 `rust-src`
组件。如果安装了，那么某些路径会指向你文件系统上那份源文件副本；
如果没有安装，它们会显示为 `/rustc/[rustc commit hash]/library/...`
（就像被选中净化时那样）。
指向所有其他源文件的路径不会受影响。

这不会影响源代码中任何硬编码的路径，例如字符串中的路径。

#### 环境变量 {#environment-variable}
*作为[「Cargo 为构建脚本设置的环境变量」](../07-environment-variables/#environment-variables-cargo-sets-for-crates)的新条目*

* `CARGO_TRIM_PATHS_SCOPE` --- `trim-paths` profile 选项的值。
    `false`、`"none"` 以及空数组会被转换为 `none`。
    `true` 和 `"all"` 会变成 `all`。
    非空数组中的值会被拼接成以逗号分隔的列表。
    如果构建脚本向构建产物中引入了绝对路径（例如通过调用某个编译器），
    用户可能会要求在不同类型的产物中对它们进行净化。
    常见需要净化的路径包括 `OUT_DIR`、`CARGO_MANIFEST_DIR` 和 `CARGO_MANIFEST_PATH`，
    以及构建脚本引入的其他路径，比如 include 目录。
* `CARGO_TRIM_PATHS_REMAP` --- Cargo 传给编译器的 `<from>=<to>` 路径重映射对，
    以平台的路径分隔符连接。
    仅在 `trim-paths` profile 生效时设置。
    构建脚本可以把这些映射转发给 C/C++ 编译器和其他工具，
    例如通过 `cc` 的 `-ffile-prefix-map`，
    从而与构建的其余部分保持一致地净化路径。

## gc {#gc}
* 跟踪 Issue：[#12633](https://github.com/rust-lang/cargo/issues/12633)

`-Zgc` 标志用于启用与 cargo 主目录中全局缓存垃圾回收相关的某些功能。

#### 自动 gc 配置 {#automatic-gc-configuration}
`-Zgc` 标志会让 Cargo 读取与垃圾回收相关的额外配置项。可用的设置有：

```toml
# config.toml 文件示例。
# 用于定义清理全局缓存具体设置的子表。
[cache.global-clean]
# 源码缓存中超过该时长的内容都将被删除。
max-src-age = "1 month"
# 压缩 crate 缓存中超过该时长的内容都将被删除。
max-crate-age = "3 months"
# 索引缓存中超过该时长的索引都将被删除。
max-index-age = "3 months"
# 检出缓存中超过该时长的 git 检出都将被删除。
max-git-co-age = "1 month"
# git 缓存中超过该时长的 git 克隆都将被删除。
max-git-db-age = "3 months"
```

注意，[`cache.auto-clean-frequency`] 选项已在 Rust 1.88 中稳定化。

[`cache.auto-clean-frequency`]: ../06-configuration/#cacheauto-clean-frequency

### 使用 `cargo clean` 手动进行垃圾回收 {#manual-garbage-collection-with-cargo-clean}
可以通过 `cargo clean gc -Zgc` 命令进行手动删除。
传入下列缓存选项之一即可执行缓存内容的删除：

- `--max-src-age=DURATION` --- 删除自给定时长以来未被使用的源码缓存文件。
- `--max-crate-age=DURATION` --- 删除自给定时长以来未被使用的 crate 缓存文件。
- `--max-index-age=DURATION` --- 删除自给定时长以来未被使用的注册表索引（包括其 `.crate` 与 `src` 文件）。
- `--max-git-co-age=DURATION` --- 删除自给定时长以来未被使用的 git 依赖检出。
- `--max-git-db-age=DURATION` --- 删除自给定时长以来未被使用的 git 依赖克隆。
- `--max-download-age=DURATION` --- 删除自给定时长以来未被使用的任何已下载缓存数据。
- `--max-src-size=SIZE` --- 从最旧的开始删除源码缓存文件，直到缓存小于给定大小。
- `--max-crate-size=SIZE` --- 从最旧的开始删除 crate 缓存文件，直到缓存小于给定大小。
- `--max-git-size=SIZE` --- 从最旧的开始删除 git 依赖缓存，直到缓存小于给定大小。
- `--max-download-size=SIZE` --- 从最旧的开始删除已下载的缓存数据，直到缓存小于给定大小。

DURATION 的形式为 "N seconds/minutes/days/weeks/months"，其中 N 是整数。

SIZE 的形式为 "N *后缀*"，其中 *后缀* 为 B、kB、MB、GB、kiB、MiB 或 GiB，N 为整数或浮点数。
如果没有指定后缀，该数字表示字节数。

```sh
cargo clean gc -Zgc
cargo clean gc -Zgc --max-download-age=1week
cargo clean gc -Zgc --max-git-size=0 --max-download-size=100MB
```

## open-namespaces {#open-namespaces}
* 跟踪 Issue：[#13576](https://github.com/rust-lang/cargo/issues/13576)

允许多个包参与同一个 API 命名空间。

可以这样启用：
```toml
cargo-features = ["open-namespaces"]

[package]
# ...
```

## panic-immediate-abort {#panic-immediate-abort}
* 跟踪 Issue：[#16042](https://github.com/rust-lang/cargo/issues/16042)
* 上游跟踪 Issue：[rust-lang/rust#147286](https://github.com/rust-lang/rust/issues/147286)

扩展 `panic` profile 设置，使其支持
[`immediate-abort`](https://doc.rust-lang.org/rustc/codegen-options/index.html#panic) panic 策略。
可以这样启用：

```toml
# Cargo.toml
cargo-features = ["panic-immediate-abort"]

[package]
# ...
[profile.release]
panic = "immediate-abort"
```

若要在 Cargo 配置中的 profile 里设置该选项，
你需要使用 `-Z panic-immediate-abort` CLI 标志
或 `[unstable]` 表来启用它。
例如：

```toml
# .cargo/config.toml
[unstable]
panic-immediate-abort = true

[profile.release]
panic = "immediate-abort"
```

## fine-grain-locking {#fine-grain-locking}
* 跟踪 Issue：[#4282](https://github.com/rust-lang/cargo/issues/4282)

使用细粒度锁，而不是锁住整个构建缓存。

注意：细粒度锁会隐式启用 [build-dir-new-layout](#build-dir-new-layout)，因为细粒度锁正是建立在
那套目录重组之上的。

## `[lints.cargo]` {#lintscargo}
* 跟踪 Issue：[#12235](https://github.com/rust-lang/cargo/issues/12235)

为 `cargo` 新增一个 `lints` 工具表，当使用 `-Zcargo-lints` 时，可用于配置由 `cargo` 自身发出的
lint。
```toml
[lints.cargo]
implicit-features = "warn"
```

它可以与
[RFC 2906 `workspace-deduplicate`](https://rust-lang.github.io/rfcs/2906-cargo-workspace-deduplicate.html)
配合使用：
```toml
[workspace.lints.cargo]
implicit-features = "warn"

[lints]
workspace = true
```

## Path Bases {#path-bases}
* 跟踪 Issue：[#14355](https://github.com/rust-lang/cargo/issues/14355)

`path` 依赖可以通过把 `base` 键设为某个路径基准（path base）的名称来可选地指定一个基准；
该路径基准来自[配置](../06-configuration/)中的 `[path-bases]` 表，或者是
[内置路径基准](#built-in-path-bases)之一。
该路径基准的值会被前置到 `path` 的值之前（必要时加上路径分隔符），从而得到 Cargo 实际查找该依赖
的位置。

例如，如果 `Cargo.toml` 中包含：

```toml
cargo-features = ["path-bases"]

[dependencies]
foo = { base = "dev", path = "foo" }
```

而配置中的 `[path-bases]` 表包含：

```toml
[path-bases]
dev = "/home/user/dev/rust/libraries/"
```

这就会得到一个位于 `/home/user/dev/rust/libraries/foo` 的 `path` 依赖 `foo`。

路径基准可以是绝对路径，也可以是相对路径。相对路径基准相对于声明该路径基准的配置文件所在的父目录。

路径基准的名称只能使用[字母数字](https://doc.rust-lang.org/std/primitive.char.html#method.is_alphanumeric)
字符或 `-`、`_`，必须以[字母](https://doc.rust-lang.org/std/primitive.char.html#method.is_alphabetic)
开头，并且不能为空。

如果依赖中使用的路径基准名称既不在配置中，也不是内置路径基准之一，Cargo 就会报错。

#### Built-in path bases {#built-in-path-bases}
Cargo 提供了一些隐式的路径基准，无需在 `[path-bases]` 表中指定即可使用。

* `workspace` - 如果一个项目是[工作空间或工作空间成员](../02-workspaces/)，
那么该路径基准被定义为该工作空间根 `Cargo.toml` 所在的父目录。

如果某个内置路径基准的名称同时也在配置中声明了，那么 Cargo 会优先使用配置中的值。这使得 Cargo
可以在不引起兼容性问题的前提下添加新的内置路径基准（因为已有的用法会遮蔽这个内置名称）。

## native-completions {#native-completions}
* 最初的 Issue：[#6645](https://github.com/rust-lang/cargo/issues/6645)
* 跟踪 Issue：[#14520](https://github.com/rust-lang/cargo/issues/14520)

该特性把手写的补全脚本迁移为 Rust 原生实现，使我们更容易添加、扩展和测试新的补全。该特性在
nightly 渠道上默认启用，不需要额外的 `-Z` 选项。

特别希望获得反馈的方面：
- 需要转义或加引号、但目前处理不正确的参数
- 信息中的不准确之处
- 命令行解析中的 bug
- 没有给出补全结果的参数
- 某个已知问题给你造成了困扰

反馈可以分为两类：
- 报告了哪些补全候选项
  - 已知问题：[#14520](https://github.com/rust-lang/cargo/issues/14520)、[`A-completions`](https://github.com/rust-lang/cargo/labels/A-completions)
  - [报告 issue](https://github.com/rust-lang/cargo/issues/new) 或[讨论其行为](https://github.com/rust-lang/cargo/issues/14520)
- Shell 集成、命令行解析与补全过滤
  - 已知问题：[clap#3166](https://github.com/clap-rs/clap/issues/3166)、[clap 的 `A-completions`](https://github.com/clap-rs/clap/labels/A-completion)
  - [报告 issue](https://github.com/clap-rs/clap/issues/new/choose) 或[讨论其行为](https://github.com/clap-rs/clap/discussions/new/choose)

如有疑问，你可以在 [#14520](https://github.com/rust-lang/cargo/issues/14520) 或
[zulip](https://rust-lang.zulipchat.com/#narrow/stream/246057-t-cargo) 上讨论。

### 如何使用 native-completions 特性： {#how-to-use-native-completions-feature}
- bash：
  把 `source <(CARGO_COMPLETE=bash cargo +nightly)` 加入 `~/.local/share/bash-completion/completions/cargo`。

- zsh：
  把 `source <(CARGO_COMPLETE=zsh cargo +nightly)` 加入你的 `.zshrc`。
  
- fish：
  把 `source (CARGO_COMPLETE=fish cargo +nightly | psub)` 加入 `$XDG_CONFIG_HOME/fish/completions/cargo.fish`

- elvish：
  把 `eval (E:CARGO_COMPLETE=elvish cargo +nightly | slurp)` 加入 `$XDG_CONFIG_HOME/elvish/rc.elv`

- powershell：
  把 `CARGO_COMPLETE=powershell cargo +nightly | Invoke-Expression` 加入 `$PROFILE`。

## feature unification {#feature-unification}
* RFC：[#3692](https://github.com/rust-lang/rfcs/blob/master/text/3692-feature-unification.md)
* 跟踪 Issue：[#14774](https://github.com/rust-lang/cargo/issues/14774)

`-Z feature-unification` 启用 `resolver.feature-unification` 配置项，用于控制特性在工作空间
范围内如何被统一。
如果没有启用 `-Z feature-unification` 这个不稳定标志，
`resolver.feature-unification` 配置就会被忽略。

### `resolver.feature-unification` {#resolverfeature-unification}
* 类型：字符串
* 默认值：`"selected"`
* 环境变量：`CARGO_RESOLVER_FEATURE_UNIFICATION`

指定哪些包参与[特性统一](../features/#feature-unification)。

* `selected`：合并当前构建所指定的全部包的依赖特性。
* `workspace`：跨所有工作空间成员合并依赖特性，无论当前构建指定了哪些包。
* `package`：逐包考虑依赖特性；当不同包激活了不同的特性集时，宁可对依赖进行多次重复构建。

## lockfile-publish-time {#lockfile-publish-time}
* 最初的 Issue：[#5221](https://github.com/rust-lang/cargo/issues/5221)
* 跟踪 Issue：[#16271](https://github.com/rust-lang/cargo/issues/16271)

使用 `cargo generate-lockfile -Zunstable-options --publish-time <time>` 时，
包解析将不会考虑任何比指定时间更新的包。

## Package message format {#package-message-format}
* 最初的 Issue：[#11666](https://github.com/rust-lang/cargo/issues/11666)
* 跟踪 Issue：[#15353](https://github.com/rust-lang/cargo/issues/15353)

`cargo package` 中的 `--message-format` 标志控制输出消息的格式。
目前它只能与 `--list` 标志一起使用，并影响文件列表的格式，需要 `-Zunstable-options`。
更多信息请参见
[`cargo package --message-format`](../../cargo-commands/publishing-commands/04-cargo-package/#option-cargo-package---message-format)。

## rustdoc depinfo {#rustdoc-depinfo}
* 最初的 Issue：[#12266](https://github.com/rust-lang/cargo/issues/12266)
* 跟踪 Issue：[#15370](https://github.com/rust-lang/cargo/issues/15370)

`-Z rustdoc-depinfo` 标志利用 rustdoc 的 dep-info 文件来判断文档是否需要重新生成。它可以与
`-Z checksum-freshness` 结合使用，从而检测校验和变化而非文件 mtime。

## embed-metadata {#embed-metadata}
* 最初的 Pull Request：[#15378](https://github.com/rust-lang/cargo/pull/15378)
* 跟踪 Issue：[#15495](https://github.com/rust-lang/cargo/issues/15495)

Rust 的默认行为是把 crate 元数据嵌入到 `rlib` 和 `dylib` 产物中。
由于 Cargo 还会为这些中间产物传递 `--emit=metadata` 以启用流水线式编译，这意味着大量元数据最终
在磁盘上被重复存储，从而浪费 target 目录的磁盘空间。

如果你向 Cargo 传入 `-Zembed-metadata=no`，它就会把 `-Zembed-metadata=no` 标志传给编译器，
指示编译器不要把元数据嵌入 rlib 和 dylib 产物中。这种情况下，元数据只会存储在 `.rmeta` 文件里。

```console
cargo +nightly -Zembed-metadata=no build
```

> 注意，该标志计划在未来被移除，因为 `no` 的行为应当成为默认行为。

## `unstable-editions` {#unstable-editions}
`cargo-features` 列表中的 `unstable-editions` 值允许 `Cargo.toml` 清单指定一个尚未稳定的版次
（edition）。

```toml
cargo-features = ["unstable-editions"]

[package]
name = "my-package"
edition = "future"
```

当引入新版次时，在该版次稳定化之前都需要 `unstable-editions` 特性。

特殊的 "future" 版次是尚在开发中的新特性的归宿，并且永久不稳定。"future" 版次本身也没有任何新行为。
其中的每一项变更都需要显式选择启用，例如通过 `#![feature(...)]` 属性。

## `fix-edition` {#fix-edition}
`-Zfix-edition` 是一个永久不稳定的标志，用于辅助测试版次迁移，尤其是配合 crater 使用。它只能与
`cargo fix` 子命令一起使用。它有两种形式：

- `-Zfix-edition=start=$INITIAL` --- 该形式检查当前版次是否等于给定的数值。如果不等，就以成功
  退出（因为我们希望忽略更旧的版次）。如果相等，则运行等价于 `cargo check` 的操作。它的用途是配合
  crater 的 "start" 工具链，为「之前」的工具链建立基线。
- `-Zfix-edition=end=$INITIAL,$NEXT` --- 该形式检查当前版次是否等于给定的 `$INITIAL` 值。
  如果不等，就以成功退出。如果相等，则执行到 `$NEXT` 所指定版次的版次迁移。之后，它会修改
  `Cargo.toml` 以加入相应的 `cargo-features = ["unstable-edition"]`、更新 `edition` 字段，
  并运行等价于 `cargo check` 的操作，以验证迁移在新版次下可以正常工作。

例如：

```console
cargo +nightly fix -Zfix-edition=end=2024,future
```

## section-timings {#section-timings}
* 最初的 Pull Request：[#15780](https://github.com/rust-lang/cargo/pull/15780)
* 跟踪 Issue：[#15817](https://github.com/rust-lang/cargo/issues/15817)

该特性可用于扩展 `cargo build --timings` 的输出。它会让 rustc 产出各个编译阶段（section）的
耗时数据，这些数据随后会显示在 timings 的 HTML/JSON 输出中。

```console
cargo +nightly -Zsection-timings build --timings
```

## Build analysis {#build-analysis}
* 最初的 Issue：[rust-lang/rust-project-goals#332](https://github.com/rust-lang/rust-project-goals/pull/332)
* 跟踪 Issue：[#15844](https://github.com/rust-lang/cargo/issues/15844)

`-Zbuild-analysis` 特性会把详细的构建指标记录并持久化到磁盘上，同时提供查询过往构建的新命令。

启用后，
Cargo 会以 JSONL 格式把构建日志写入 `$CARGO_HOME/log/` 目录。
每次 cargo 调用都会生成一个以唯一会话 ID 命名的日志文件。
这些日志包含耗时信息、重新构建的原因以及其他构建元数据，
可以用 `cargo report` 子命令进行分析。

要启用构建分析，请添加以下 [Cargo 配置](../06-configuration/)：

```toml
# config.toml 文件示例。
[unstable]
build-analysis = true

# 启用构建指标采集
[build.analysis]
enabled = true
```

在 stable 工具链上设置它只会产生一个未知配置的警告，
因此把它一直保留在 Cargo 配置中是安全的。

### `cargo report` 命令 {#cargo-report-commands}
`-Zbuild-analysis` 之下提供了以下命令：

- `cargo report sessions` --- 列出以往的构建会话。
  可以用它来查找供其他 report 命令使用的会话 ID。
- `cargo report timings` --- 根据以往的某次会话生成 HTML 耗时报告，
  类似 `cargo build --timings`，但无需重新构建。
- `cargo report rebuilds` --- 报告 crate 为何被重新构建，
  帮助诊断意料之外的重新编译。

## build-dir-new-layout {#build-dir-new-layout}
* 跟踪 Issue：[#15010](https://github.com/rust-lang/cargo/issues/15010)

启用新的 build-dir 文件系统布局。
这项布局变更为后续的缓存与加锁改进扫清了障碍。


## compile-time-deps {#compile-time-deps}
这是一个永久不稳定的标志，用于只构建过程宏和构建脚本（以及它们所需的依赖），并运行这些构建脚本。

它面向 rust-analyzer 这类工具，永远不会被稳定化。

示例：

```console
cargo +nightly build --compile-time-deps -Z unstable-options
cargo +nightly check --compile-time-deps --all-targets -Z unstable-options
```

## `rustc-unicode` {#rustc-unicode}
* 跟踪 Issue：[rust#148607](https://github.com/rust-lang/rust/issues/148607)

在 Cargo 的错误信息中启用 `rustc` 的 unicode 错误格式。

## rustdoc mergeable info {#rustdoc-mergeable-info}
* 最初的 Pull Request：[#16309](https://github.com/rust-lang/cargo/pull/16309)
* 跟踪 Issue：[#16306](https://github.com/rust-lang/cargo/issues/16306)
* rustc 跟踪 Issue：[rust-lang/rust#130676](https://github.com/rust-lang/rust/issues/130676)

`-Z rustdoc-mergeable-info` 利用 rustdoc 的可合并 crate 信息，
使 `cargo doc` 能够从各自独立的输出目录中合并跨 crate 的信息
（如搜索索引、源文件索引等），
并且并行地运行 `rustdoc`。

## json-target-spec {#json-target-spec}
* 跟踪 Issue：[rust-lang/rust#151528](https://github.com/rust-lang/rust/issues/151528)

`-Z json-target-spec` CLI 标志启用把
[自定义目标规范 JSON 文件](https://doc.rust-lang.org/nightly/rustc/targets/custom.html)
作为 target 使用的能力。

```console
cargo +nightly build --target my-target.json -Z json-target-spec
```

这通常必须与 [build-std](#build-std) 结合使用。

## hint-msrv {#hint-msrv}
* 跟踪 Issue：[rust-lang/rust#157574](https://github.com/rust-lang/rust/issues/157574)

`-Z hint-msrv` CLI 标志让 Cargo 把 `package.rust-version` 传给 rustc，这会影响哪些 lint 会被
发出。

你可以通过全局的 `~/.cargo/config.toml` 设置它：nightly 版 Cargo 会自动使用它，而 stable 版
Cargo 会静默忽略这个不稳定选项：

```toml
[unstable]
hint-msrv = true
```

## min-publish-age {#min-publish-age}
* 跟踪 Issue：[#17009](https://github.com/rust-lang/cargo/issues/17009)
* RFC：[#3923](https://github.com/rust-lang/rfcs/pull/3923)

`-Zmin-publish-age` 特性允许用户为依赖版本指定一个最小年龄。指定之后，Cargo 不会使用注册表中
比该最小年龄更新的 crate 版本，同时也提供了针对紧急安全修复等例外情况的覆盖方式。

例如，在你的 `<repo>/.cargo/config.toml` 中：

```toml
[registry]
global-min-publish-age = "14 days"
```

### 新增到配置中的内容 {#added-to-configuration}
以下内容将被加入 Cargo 的配置格式：

```toml
[resolver]
incompatible-publish-age = "deny" # 指定解析器如何应对这些版本

[registries.<name>]
min-publish-age = "..."  # 为该注册表覆盖 `registry.global-min-publish-age`

[registry]
min-publish-age = "..."  # 为 crates.io 覆盖 `registry.global-min-publish-age`
global-min-publish-age = "0"  # 允许来自该注册表的包所需的最小时间跨度
```

#### `resolver.incompatible-publish-age` {#resolverincompatible-publish-age}
* 类型：字符串
* 默认值：`"deny"`
* 环境变量：`CARGO_RESOLVER_INCOMPATIBLE_PUBLISH_AGE`

在解析依赖版本时，
指定对于 `pubtime`（若存在）与 `registry.min-publish-age` 不兼容的版本应采取何种行为。
可选值包括：

- `allow`：把 pubtime 不兼容的版本当作任何其他版本一样对待
- `deny`：忽略 pubtime 不兼容的版本，除非它们已经存在于锁文件中

#### `registries.<name>.min-publish-age` {#registriesnamemin-publish-age}
* 类型：字符串
* 默认值：无
* 环境变量：`CARGO_REGISTRIES_<name>_MIN_PUBLISH_AGE`

指定对于来自该注册表的包，自某个版本的 `pubtime` 起需经过多长时间，才可以被
`resolver.incompatible-publish-age` 纳入考虑。若未设置，则使用
`registry.global-min-publish-age`。

如果该注册表不支持此功能，该设置会被忽略。

它支持以下值：

- 一个整数，后跟 "seconds"、"minutes"、"hours"、"days"、"weeks" 或 "months"
- `"0"` 表示允许所有包

#### `registry.min-publish-age` {#registrymin-publish-age}
* 类型：字符串
* 默认值：无
* 环境变量：`CARGO_REGISTRY_MIN_PUBLISH_AGE`

指定对于来自 crates.io 的包，自某个版本的 `pubtime` 起需经过多长时间，才可以被
`resolver.incompatible-publish-age` 纳入考虑。若未设置，则使用
`registry.global-min-publish-age`。

它支持以下值：

- 一个整数，后跟 "seconds"、"minutes"、"hours"、"days"、"weeks" 或 "months"
- `"0"` 表示允许所有包

通常会使用 `"0"`、`"N days"` 和 `"N weeks"`。

#### `registry.global-min-publish-age` {#registryglobal-min-publish-age}
* 类型：字符串
* 默认值：`"0"`
* 环境变量：`CARGO_REGISTRY_GLOBAL_MIN_PUBLISH_AGE`

指定全局范围内，自某个版本的 `pubtime` 起需经过多长时间，才可以被
`resolver.incompatible-publish-age` 纳入考虑。
如果没有通过 `registries.<name>.min-publish-age` 为某个具体注册表设置 `min-publish-age`，
Cargo 就会使用这个最小发布年龄。

它支持以下值：

- 一个整数，后跟 "seconds"、"minutes"、"hours"、"days"、"weeks" 或 "months"
- `"0"` 表示允许所有包

### 新增到解析器中的内容 {#added-to-resolver}
以下内容将被加入[解析器章节][resolver chapter]，作为「Yanked versions」的兄弟小节：

> 「pubtime 不兼容的版本」
>
> 发布时间比配置的 `min-publish-age` 更新的版本被视为 pubtime 不兼容。
> 当 `resolver.incompatible-publish-age` 设为 `deny` 时，
> 解析器会忽略这些版本，
> 除非它们已经存在于 `Cargo.lock` 文件中。
> 把该配置设为 `allow` 会禁用这项检查；
> 若再与 `cargo update --precise` 结合，
> cargo 就会拉取某个特定版本及其传递依赖。

[resolver chapter]: ../specifying-dependencies/03-dependency-resolution/

# 已稳定化与已移除的特性 {#stabilized-and-removed-features}
## Compile progress {#compile-progress}
编译进度（compile-progress）特性已在 1.30 版本中稳定化。
现在进度条默认开启。
关于控制该特性的更多信息，请参见 [`term.progress`](../06-configuration/#termprogresswhen)。

## Edition {#edition}
在 `Cargo.toml` 中指定 `edition` 已在 1.31 版本中稳定化。
关于指定该字段的更多信息，请参见 [edition 字段](../the-manifest-format/#the-edition-field)。

## rename-dependency {#rename-dependency}
在 `Cargo.toml` 中指定重命名的依赖已在 1.31 版本中稳定化。
关于重命名依赖的更多信息，请参见
[重命名依赖](../specifying-dependencies/#renaming-dependencies-in-cargotoml)。

## Alternate Registries {#alternate-registries}
对备用注册表的支持已在 1.34 版本中稳定化。
关于备用注册表的更多信息，请参见[注册表章节](../registries/)。

## Offline Mode {#offline-mode}
离线（offline）特性已在 1.36 版本中稳定化。
关于使用离线模式的更多信息，请参见
[`--offline` 标志](../../cargo-commands/general-commands/01-cargo/#option-cargo---offline)。

## publish-lockfile {#publish-lockfile}
`publish-lockfile` 特性已在 1.37 版本中移除。
当被发布的包含有二进制目标时，`Cargo.lock` 文件总是会被包含进去。`cargo install` 需要
`--locked` 标志才会使用 `Cargo.lock` 文件。
更多信息请参见 [`cargo package`](../../cargo-commands/publishing-commands/04-cargo-package/) 与
[`cargo install`](../../cargo-commands/package-commands/02-cargo-install/)。

## default-run {#default-run}
`default-run` 特性已在 1.37 版本中稳定化。
关于指定默认运行目标的更多信息，请参见
[`default-run` 字段](../the-manifest-format/#the-default-run-field)。

## cache-messages {#cache-messages}
编译器消息缓存已在 1.40 版本中稳定化。
编译器警告现在默认会被缓存，并在重新运行 Cargo 时自动重放。

## install-upgrade {#install-upgrade}
`install-upgrade` 特性已在 1.41 版本中稳定化。
现在 [`cargo install`] 会在包看起来过时时自动升级它们。更多信息请参见 [`cargo install`] 文档。

[`cargo install`]: ../../cargo-commands/package-commands/02-cargo-install/

## Profile Overrides {#profile-overrides}
Profile 覆盖（overrides）已在 1.41 版本中稳定化。
关于使用覆盖的更多信息，请参见 [Profile 覆盖](../05-profiles/#overrides)。

## Config Profiles {#config-profiles}
在 Cargo 配置文件和环境变量中指定 profile 已在 1.43 版本中稳定化。
关于在配置文件中指定 [profile](../05-profiles/) 的更多信息，请参见
[配置中的 `[profile]` 表](../06-configuration/#profile)。

## crate-versions {#crate-versions}
`-Z crate-versions` 标志已在 1.47 版本中稳定化。
现在 crate 版本会自动包含在 [`cargo doc`](../../cargo-commands/build-commands/06-cargo-doc/)
生成的文档侧边栏中。

## Features {#features}
`-Z features` 标志已在 1.51 版本中稳定化。
关于使用新特性解析器的更多信息，请参见
[特性解析器版本 2](../features/#feature-resolver-version-2)。

## package-features {#package-features}
`-Z package-features` 标志已在 1.51 版本中稳定化。
关于使用 features CLI 选项的更多信息，请参见
[解析器版本 2 的命令行标志](../features/#resolver-version-2-command-line-flags)。

## Resolver {#resolver}
`Cargo.toml` 中的 `resolver` 特性已在 1.51 版本中稳定化。
关于指定解析器的更多信息，请参见
[解析器版本](../specifying-dependencies/03-dependency-resolution/#resolver-versions)。

## extra-link-arg {#extra-link-arg}
用于在构建脚本中指定额外链接器参数的 `extra-link-arg` 特性已在 1.56 版本中稳定化。
关于指定额外链接器参数的更多信息，请参见
[构建脚本文档](../build-scripts/#outputs-of-the-build-script)。

## configurable-env {#configurable-env}
用于在 Cargo 配置中指定环境变量的 `configurable-env` 特性已在 1.56 版本中稳定化。
关于配置环境变量的更多信息，请参见[配置文档](../06-configuration/#env)。

## rust-version {#rust-version}
`Cargo.toml` 中的 `rust-version` 字段已在 1.56 版本中稳定化。
关于使用 `rust-version` 字段和 `--ignore-rust-version` 选项的更多信息，请参见
[rust-version 字段](../the-manifest-format/#the-rust-version-field)。

## patch-in-config {#patch-in-config}
`-Z patch-in-config` 标志，以及对应的在 Cargo 配置文件中使用 `[patch]` 段的支持，已在 1.56
版本中稳定化。更多信息请参见 [patch 字段](../06-configuration/#patch)。

## edition 2021 {#edition-2021}
2021 版次已在 1.56 版本中稳定化。
关于设置版次的更多信息，请参见 [`edition` 字段](../the-manifest-format/#the-edition-field)。
关于迁移已有项目的更多信息，请参见
[`cargo fix --edition`](../../cargo-commands/build-commands/08-cargo-fix/) 与
[版次指南](https://doc.rust-lang.org/edition-guide/index.html)。


## Custom named profiles {#custom-named-profiles}
自定义命名 profile 已在 1.57 版本中稳定化。更多信息请参见
[profile 章节](../05-profiles/#custom-profiles)。

## Profile `strip` option {#profile-strip-option}
profile 的 `strip` 选项已在 1.59 版本中稳定化。更多信息请参见
[profile 章节](../05-profiles/#strip)。

## Future incompat report {#future-incompat-report}
生成未来不兼容报告的支持已在 1.59 版本中稳定化。更多信息请参见
[未来不兼容报告章节](../14-future-incompat-report/)。

## Namespaced features {#namespaced-features}
带命名空间的特性已在 1.60 版本中稳定化。
更多信息请参见[特性章节](../features/#optional-dependencies)。

## Weak dependency features {#weak-dependency-features}
弱依赖特性已在 1.60 版本中稳定化。
更多信息请参见[特性章节](../features/#dependency-features)。

## timings {#timings}
`-Ztimings` 选项已在 1.60 版本中以 `--timings` 的形式稳定化。
timings 的输出格式选项
（例如 `--timings=html` 以及机器可读的 `--timings=json` 输出）
已在 1.94.0-nightly 中移除。

## config-cli {#config-cli}
`--config` CLI 选项已在 1.63 版本中稳定化。更多信息请参见
[配置文档](../06-configuration/#command-line-overrides)。

## multitarget {#multitarget}
`-Z multitarget` 选项已在 1.64 版本中稳定化。
关于设置默认[目标平台三元组][target triple]的更多信息，请参见
[`build.target`](../06-configuration/#buildtarget)。

## crate-type {#crate-type}
`cargo rustc` 的 `--crate-type` 标志已在 1.64 版本中稳定化。更多信息请参见
[`cargo rustc` 文档](../../cargo-commands/build-commands/12-cargo-rustc/)。


## Workspace Inheritance {#workspace-inheritance}
工作空间继承已在 1.64 版本中稳定化。
更多信息请参见 [workspace.package](../02-workspaces/#the-package-table)、
[workspace.dependencies](../02-workspaces/#the-dependencies-table)
以及[从工作空间继承依赖](../specifying-dependencies/#inheriting-a-dependency-from-a-workspace)。

## terminal-width {#terminal-width}
`-Z terminal-width` 选项已在 1.68 版本中稳定化。
当从 Cargo 能够自动检测宽度的终端中运行时，终端宽度总是会被传给编译器。

## sparse-registry {#sparse-registry}
稀疏注册表（sparse registry）支持已在 1.68 版本中稳定化。
更多信息请参见[注册表协议](../registries/#registry-protocols)。

### `cargo logout` {#cargo-logout}
[`cargo logout`] 命令已在 1.70 版本中稳定化。

[target triple]: ../../appendix/01-glossary/#target '"target"（术语表）'
[`cargo logout`]: ../../cargo-commands/publishing-commands/02-cargo-logout/

## `doctest-in-workspace` {#doctest-in-workspace}
`cargo test` 的 `-Z doctest-in-workspace` 选项已在 1.72 版本中稳定化并默认启用。
关于编译和运行测试时工作目录的更多信息，请参见
[`cargo test` 文档](../../cargo-commands/build-commands/14-cargo-test/#working-directory-of-tests)。

## keep-going {#keep-going}
`--keep-going` 选项已在 1.74 版本中稳定化。更多细节可参考 `cargo build` 中的
[`--keep-going` 标志](../../cargo-commands/build-commands/02-cargo-build/#option-cargo-build---keep-going)
作为示例。

## `[lints]` {#lints}
[`[lints]`](../the-manifest-format/#the-lints-section)（通过 `-Zlints` 启用）已在
1.74 版本中稳定化。

## credential-process {#credential-process}
`-Z credential-process` 特性已在 1.74 版本中稳定化。

详情请参见[注册表认证](../registries/registry-authentication/)文档。

## registry-auth {#registry-auth}
`-Z registry-auth` 特性已在 1.74 版本中稳定化，并附加了必须配置凭证提供者这一要求。

详情请参见[注册表认证](../registries/registry-authentication/)文档。

## check-cfg {#check-cfg}
`-Z check-cfg` 特性已在 1.80 版本中通过将其设为默认行为而稳定化。

关于指定自定义 cfg 的信息，请参见
[构建脚本文档](../build-scripts/#rustc-check-cfg)。

## Edition 2024 {#edition-2024}
2024 版次已在 1.85 版本中稳定化。
关于设置版次的更多信息，请参见 [`edition` 字段](../the-manifest-format/#the-edition-field)。
关于迁移已有项目的更多信息，请参见
[`cargo fix --edition`](../../cargo-commands/build-commands/08-cargo-fix/) 与
[版次指南](https://doc.rust-lang.org/edition-guide/index.html)。

## Automatic garbage collection {#automatic-garbage-collection}
自动删除旧文件的支持已在 Rust 1.88 中稳定化。
更多信息可在[配置章节](../06-configuration/#cache)中找到。

## doctest-xcompile {#doctest-xcompile}
从 Rust 1.89 起，文档测试的交叉编译已无条件启用。用 `cargo test` 运行文档测试现在会遵循
`--target` 标志。

## package-workspace {#package-workspace}
多包发布已在 Rust 1.90.0 中稳定化。

## build-dir {#build-dir}
对 `build.build-dir` 的支持已在 1.91 版本中稳定化。
关于修改 build-dir 的信息，请参见[配置文档](../06-configuration/#buildbuild-dir)。

## Build-plan {#build-plan}
`build` 命令的 `--build-plan` 参数已在 1.93.0-nightly 中移除。
其移除原因请参见 <https://github.com/rust-lang/cargo/issues/7614>。

## config-include {#config-include}
通过 `include` 配置键包含额外配置文件的支持已在 1.93.0 中稳定化。
更多信息请参见 [`include` 配置文档](../06-configuration/#include)。

## pubtime {#pubtime}
`pubtime` 索引字段已在 Rust 1.94.0 中稳定化。

## lockfile-path {#lockfile-path}
对 `resolver.lockfile-path` 配置字段的支持已在 Rust 1.97.0 中稳定化。

## warnings {#warnings}
`build.warnings` 配置字段已在 Rust 1.97 中稳定化。






