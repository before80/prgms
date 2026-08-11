+++
title = "08-构建脚本"
date = 2026-07-30T14:49:00+08:00
weight = 44
type = "docs"
description = "build.rs 生命周期、输入输出与指令"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 构建脚本


> 原文链接: [https://doc.rust-lang.org/cargo/reference/build-scripts.html](https://doc.rust-lang.org/cargo/reference/build-scripts.html)


某些包需要编译第三方非 Rust 代码，例如 C 库。其他包需要链接到 C 库，这些库可能位于系统上，也可能需要从源码构建。还有些包需要在构建前进行代码生成等功能（例如解析器生成器）。

Cargo 并不旨在取代其他针对这些任务优化良好的工具，但会通过自定义构建脚本与它们集成。在包根目录放置名为 `build.rs` 的文件，会使 Cargo 编译该脚本并在构建包之前执行它。

```rust,ignore
// 自定义构建脚本示例。
fn main() {
    // 告诉 Cargo：若给定文件发生变化，则重新运行此构建脚本。
    println!("cargo::rerun-if-changed=src/hello.c");
    // 使用 `cc` crate 编译 C 文件并静态链接。
    cc::Build::new()
        .file("src/hello.c")
        .compile("hello");
}
```

构建脚本的一些示例用例包括：

* 构建捆绑的 C 库。
* 在主机系统上查找 C 库。
* 从规范生成 Rust 模块。
* 执行 crate 所需的任何平台特定配置。

以下各节描述构建脚本的工作原理；[示例章节](01-build-script-examples/) 展示了多种编写脚本的方式。

> 注意：[`package.build` manifest 键](../the-manifest-format/#the-build-field) 可用于更改构建脚本名称，或完全禁用它。

## 构建脚本的生命周期 {#life-cycle-of-a-build-script}
在构建包之前，Cargo 会将构建脚本编译为可执行文件（若尚未构建）。然后运行脚本，脚本可执行任意数量的任务。脚本可通过向 stdout 打印以 `cargo::` 为前缀的特殊格式命令与 Cargo 通信。

若构建脚本的任何源文件或依赖发生变化，构建脚本会被重新构建。

默认情况下，若包内任何文件发生变化，Cargo 会重新运行构建脚本。通常最好使用下文[变更检测](#change-detection) 一节描述的 `rerun-if` 命令，缩小触发构建脚本再次运行的范围。

构建脚本成功执行完毕后，包的其余部分将被编译。若出现错误，脚本应以非零退出码退出以中止构建，此时构建脚本的输出会显示在终端上。

## 构建脚本的输入 {#inputs-to-the-build-script}
运行构建脚本时，有若干输入以[环境变量][build-env] 形式传入。

除环境变量外，构建脚本的当前目录是构建脚本所在包的根目录。

[build-env]: ../07-environment-variables/#environment-variables-cargo-sets-for-build-scripts

> **注意：** 在构建脚本中检查 `target_os` 或 `target_arch` 等[配置选项][configuration options] 时，不要使用 `cfg!` 宏或 `#[cfg]` 属性，它们检查的是**主机**机器（构建脚本运行的地方），而非你正在编译的**目标**平台。交叉编译时这一区别很重要。
>
> 应读取对应的 [`CARGO_CFG_*`][build-env] 环境变量，它们正确反映目标配置。若要类型化 API，考虑使用 [`build-rs`] crate。更多细节见[构建脚本示例][build script examples]。

[configuration options]: https://doc.rust-lang.org/reference/conditional-compilation.html
[`build-rs`]: https://crates.io/crates/build-rs
[build script examples]: 01-build-script-examples/#conditional-compilation

## 构建脚本的输出 {#outputs-of-the-build-script}
构建脚本可将任何输出文件或中间产物保存在 [`OUT_DIR` 环境变量][build-env] 指定的目录中。脚本不应修改该目录外的任何文件。

> **注意：** Cargo 在构建之间不会清理或重置 `OUT_DIR`。此目录的内容可能在重建之间保留，即使构建脚本被重新运行。此行为是有意为之，以支持增量构建（例如原生代码编译）。
>
> 构建脚本不应依赖 `OUT_DIR` 为空，因为其内容可能在重建之间保留。若脚本需要干净的目录，目前需自行管理或清理其创建的文件或子目录。此方面的未来改进正在讨论中（见 [#16427](https://github.com/rust-lang/cargo/issues/16427) 与 [#9661](https://github.com/rust-lang/cargo/issues/9661)）。

构建脚本通过向 stdout 打印与 Cargo 通信。Cargo 将每行以 `cargo::` 开头的行解释为影响包编译的指令。其他行会被忽略。

> 构建脚本打印的 `cargo::` 指令顺序*可能*影响 `cargo` 传给 `rustc` 的参数顺序。进而，传给 `rustc` 的参数顺序可能影响传给链接器的参数顺序。因此，应注意构建脚本指令的顺序。例如，若对象 `foo` 需要链接库 `bar`，你可能希望库 `bar` 的 [`cargo::rustc-link-lib`](#rustc-link-lib) 指令出现在链接对象 `foo` 的指令*之后*。

正常编译期间，脚本的输出在终端中隐藏。若要在终端直接查看输出，使用 `-vv` 标志以「非常详细」模式调用 Cargo。这仅在运行构建脚本时发生。若 Cargo 判断无变化，则不会重新运行脚本，更多见下文[变更检测](#change-detection)。

构建脚本打印到 stdout 的所有行会写入类似 `target/debug/build/<pkg>/output` 的文件（精确位置可能取决于配置）。stderr 输出也保存在同一目录。

以下是 Cargo 识别的指令摘要，每项在下文详述。

* [`cargo::rerun-if-changed=PATH`](#rerun-if-changed) --- 告诉 Cargo 何时重新运行脚本。
* [`cargo::rerun-if-env-changed=VAR`](#rerun-if-env-changed) --- 告诉 Cargo 何时重新运行脚本。
* [`cargo::rustc-link-arg=FLAG`](#rustc-link-arg) --- 向链接器传递自定义标志，用于 benchmark、二进制、`cdylib` crate、示例和测试。
* [`cargo::rustc-link-arg-cdylib=FLAG`](#rustc-cdylib-link-arg) --- 向链接器传递自定义标志，仅用于 cdylib crate。
* [`cargo::rustc-link-arg-bin=BIN=FLAG`](#rustc-link-arg-bin) --- 向链接器传递自定义标志，仅用于二进制 `BIN`。
* [`cargo::rustc-link-arg-bins=FLAG`](#rustc-link-arg-bins) --- 向链接器传递自定义标志，用于二进制。
* [`cargo::rustc-link-arg-tests=FLAG`](#rustc-link-arg-tests) --- 向链接器传递自定义标志，用于测试。
* [`cargo::rustc-link-arg-examples=FLAG`](#rustc-link-arg-examples) --- 向链接器传递自定义标志，用于示例。
* [`cargo::rustc-link-arg-benches=FLAG`](#rustc-link-arg-benches) --- 向链接器传递自定义标志，用于 benchmark。
* [`cargo::rustc-link-lib=LIB`](#rustc-link-lib) --- 添加要链接的库。
* [`cargo::rustc-link-search=[KIND=]PATH`](#rustc-link-search) --- 添加到库搜索路径。
* [`cargo::rustc-flags=FLAGS`](#rustc-flags) --- 向编译器传递特定标志。
* [`cargo::rustc-cfg=KEY[="VALUE"]`](#rustc-cfg) --- 启用编译时 `cfg` 设置。
* [`cargo::rustc-check-cfg=CHECK_CFG`](#rustc-check-cfg) --- 将自定义 `cfg` 注册为预期，用于编译时配置检查。
* [`cargo::rustc-env=VAR=VALUE`](#rustc-env) --- 设置环境变量。
- [`cargo::error=MESSAGE`](#cargo-error) --- 在终端显示错误。
* [`cargo::warning=MESSAGE`](#cargo-warning) --- 在终端显示警告。
* [`cargo::metadata=KEY=VALUE`](#the-links-manifest-key) --- 元数据，供 `links` 脚本使用。

> **MSRV：** `cargo::KEY=VALUE` 语法需要 1.77。
> 若要支持旧版本，使用 `cargo:KEY=VALUE` 语法。

### `cargo::rustc-link-arg=FLAG` {#rustc-link-arg}

`rustc-link-arg` 指令告诉 Cargo 向编译器传递 [`-C link-arg=FLAG` 选项][link-arg]，但仅在构建支持的目标（benchmark、二进制、`cdylib` crate、示例和测试）时。其用法高度依赖平台。可用于设置共享库版本或链接器脚本。

[link-arg]: https://doc.rust-lang.org/rustc/codegen-options/index.html#link-arg

### `cargo::rustc-link-arg-cdylib=FLAG` {#rustc-cdylib-link-arg}

`rustc-link-arg-cdylib` 指令告诉 Cargo 向编译器传递 [`-C link-arg=FLAG` 选项][link-arg]，但仅在构建 `cdylib` 库目标时。其用法高度依赖平台。可用于设置共享库版本或 runtime-path。

出于历史原因，`cargo::rustc-cdylib-link-arg` 形式是 `cargo::rustc-link-arg-cdylib` 的别名，含义相同。

### `cargo::rustc-link-arg-bin=BIN=FLAG` {#rustc-link-arg-bin}

`rustc-link-arg-bin` 指令告诉 Cargo 向编译器传递 [`-C link-arg=FLAG` 选项][link-arg]，但仅在构建名为 `BIN` 的二进制目标时。其用法高度依赖平台。可用于设置链接器脚本或其他链接器选项。

### `cargo::rustc-link-arg-bins=FLAG` {#rustc-link-arg-bins}

`rustc-link-arg-bins` 指令告诉 Cargo 向编译器传递 [`-C link-arg=FLAG` 选项][link-arg]，但仅在构建二进制目标时。其用法高度依赖平台。可用于设置链接器脚本或其他链接器选项。

### `cargo::rustc-link-arg-tests=FLAG` {#rustc-link-arg-tests}

`rustc-link-arg-tests` 指令告诉 Cargo 向编译器传递 [`-C link-arg=FLAG` 选项][link-arg]，但仅在构建测试目标时。

### `cargo::rustc-link-arg-examples=FLAG` {#rustc-link-arg-examples}

`rustc-link-arg-examples` 指令告诉 Cargo 向编译器传递 [`-C link-arg=FLAG` 选项][link-arg]，但仅在构建示例目标时。

### `cargo::rustc-link-arg-benches=FLAG` {#rustc-link-arg-benches}

`rustc-link-arg-benches` 指令告诉 Cargo 向编译器传递 [`-C link-arg=FLAG` 选项][link-arg]，但仅在构建 benchmark 目标时。

### `cargo::rustc-link-lib=LIB` {#rustc-link-lib}

`rustc-link-lib` 指令告诉 Cargo 使用编译器的 [`-l` 标志][option-link] 链接给定库。通常用于通过 [FFI] 链接原生库。

`LIB` 字符串直接传给 rustc，因此支持 `-l` 支持的任何语法。\
目前 `LIB` 的完整支持语法为 `[KIND[:MODIFIERS]=]NAME[:RENAME]`。

`-l` 标志仅传给包的库目标；若没有库目标，则传给所有目标。这是因为所有其他目标对库目标有隐式依赖，给定链接库应只包含一次。这意味着若包同时有库和二进制目标，*库*可访问给定 lib 的符号，二进制应通过库目标的公开 API 访问它们。

可选的 `KIND` 可以是 `dylib`、`static` 或 `framework` 之一。更多细节见 [rustc 书][option-link]。

[option-link]: https://doc.rust-lang.org/rustc/command-line-arguments.html#option-l-link-lib
[FFI]: https://doc.rust-lang.org/nomicon/ffi.html

### `cargo::rustc-link-search=[KIND=]PATH` {#rustc-link-search}

`rustc-link-search` 指令告诉 Cargo 向编译器传递 [`-L` 标志][option-search]，将目录添加到库搜索路径。

可选的 `KIND` 可以是 `dependency`、`crate`、`native`、`framework` 或 `all` 之一。更多细节见 [rustc 书][option-search]。

若这些路径位于 `OUT_DIR` 内，它们也会添加到[动态库搜索路径环境变量](../07-environment-variables/#dynamic-library-paths)。不建议依赖此行为，因为这会使生成的二进制文件难以使用。通常，最好避免在构建脚本中创建动态库（使用现有系统库则没问题）。

[option-search]: https://doc.rust-lang.org/rustc/command-line-arguments.html#option-l-search-path

### `cargo::rustc-flags=FLAGS` {#rustc-flags}

`rustc-flags` 指令告诉 Cargo 向编译器传递给定的空格分隔标志。这仅允许 `-l` 和 `-L` 标志，等价于使用 [`rustc-link-lib`](#rustc-link-lib) 和 [`rustc-link-search`](#rustc-link-search)。

### `cargo::rustc-cfg=KEY[="VALUE"]` {#rustc-cfg}

`rustc-cfg` 指令告诉 Cargo 向编译器传递给定值作为 [`--cfg` 标志][option-cfg]。可用于编译时检测特性以启用[条件编译][conditional compilation]。自定义 cfg 必须先用 [`cargo::rustc-check-cfg`](#rustc-check-cfg) 指令声明为预期，否则需要允许 [`unexpected_cfgs`][unexpected-cfgs] lint 以避免意外 cfg 警告。

注意，这*不会*影响 Cargo 的依赖解析。不能用于启用可选依赖或其他 Cargo 特性。

请注意 [Cargo 特性][cargo features] 使用 `feature="foo"` 形式。通过此标志传递的 `cfg` 值不受该形式限制，可提供单个标识符或任意键/值对。例如，输出 `cargo::rustc-cfg=abc` 后，代码可使用 `#[cfg(abc)]`（注意没有 `feature=`）。或使用 `=` 符号的任意键/值对，如 `cargo::rustc-cfg=my_component="foo"`。键应为 Rust 标识符，值应为字符串。

[cargo features]: ../features/
[conditional compilation]: https://doc.rust-lang.org/reference/conditional-compilation.html
[option-cfg]: https://doc.rust-lang.org/rustc/command-line-arguments.html#option-cfg
[unexpected-cfgs]: https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#unexpected-cfgs

### `cargo::rustc-check-cfg=CHECK_CFG` {#rustc-check-cfg}

添加到预期配置名称和值列表，用于使用 [`unexpected_cfgs`][unexpected-cfgs] lint 检查*可达* cfg 表达式。

`CHECK_CFG` 的语法与 `rustc` 的 [`--check-cfg` 标志][option-check-cfg] 一致，更多细节见[检查条件配置][checking-conditional-configurations]。

指令用法示例如下：

```rust,no_run
// build.rs
println!("cargo::rustc-check-cfg=cfg(foo, values(\"bar\"))");
if foo_bar_condition {
    println!("cargo::rustc-cfg=foo=\"bar\"");
}
```

注意，应定义所有可能的 cfg，而不仅是当前启用的 cfg。这包括给定 cfg 名称的所有可能值。

建议将 `cargo::rustc-check-cfg` 与 [`cargo::rustc-cfg`][option-cfg] 指令尽可能放在一起，以避免拼写错误、遗漏 check-cfg、过时的 cfg 等。

另见[条件编译][conditional-compilation-example] 示例。

> **MSRV：** 自 1.80 起生效

[checking-conditional-configurations]: https://doc.rust-lang.org/rustc/check-cfg.html
[option-check-cfg]: https://doc.rust-lang.org/rustc/command-line-arguments.html#option-check-cfg
[conditional-compilation-example]: 01-build-script-examples/#conditional-compilation

### `cargo::rustc-env=VAR=VALUE` {#rustc-env}

`rustc-env` 指令告诉 Cargo 在编译包时设置给定环境变量。编译后的 crate 可通过 [`env!` 宏][env-macro] 获取该值。这对于在 crate 代码中嵌入额外元数据很有用，例如 git HEAD 的哈希或持续集成服务器的唯一标识符。

另见 Cargo 自动包含的[环境变量][env-cargo]。

> **注意**：使用 `cargo run` 或 `cargo test` 运行可执行文件时，这些环境变量也会被设置。但不建议使用，因为这会将可执行文件绑定到 Cargo 的执行环境。通常，这些环境变量应仅在编译时通过 `env!` 宏检查。

[env-macro]: https://doc.rust-lang.org/std/macro.env.html
[env-cargo]: ../07-environment-variables/#environment-variables-cargo-sets-for-crates

### `cargo::error=MESSAGE` {#cargo-error}

`error` 指令告诉 Cargo 在构建脚本运行完毕后显示错误，然后使构建失败。

 > 注意：构建脚本库应仔细考虑是使用 `cargo::error` 还是返回 `Result`。返回 `Result` 可能更好，让调用者决定错误是否致命。调用者再决定是否使用 `cargo::error` 显示 `Err` 变体。

> **MSRV：** 自 1.84 起生效

### `cargo::warning=MESSAGE` {#cargo-warning}

`warning` 指令告诉 Cargo 在构建脚本运行完毕后显示警告。警告仅对 `path` 依赖（即你在本地正在处理的依赖）显示，因此例如 [crates.io] crate 中打印的警告默认不会输出，除非构建失败。可使用 `-vv`「非常详细」标志让 Cargo 显示所有 crate 的警告。

## 构建依赖 {#build-dependencies}
构建脚本也允许依赖其他基于 Cargo 的 crate。依赖通过 manifest 的 `build-dependencies` 节声明。

```toml
[build-dependencies]
cc = "1.0.46"
```

构建脚本**不能**访问 `dependencies` 或 `dev-dependencies` 节中列出的依赖（它们尚未构建！）。此外，构建依赖对包本身不可用，除非也在 `[dependencies]` 表中显式添加。

建议仔细考虑添加的每个依赖，权衡对编译时间、许可证、维护等的影响。若构建依赖与普通依赖共享，Cargo 会尝试复用依赖。然而，这并非总是可行，例如交叉编译时，因此需考虑对编译时间的影响。

## 变更检测 {#change-detection}

重建包时，Cargo 不一定知道是否需要再次运行构建脚本。默认采取保守策略：若包内任何文件发生变化（或 [`exclude` 与 `include` 字段][`exclude` and `include` fields] 控制的文件列表发生变化），总是重新运行构建脚本。对大多数情况这不是好选择，因此建议每个构建脚本至少输出一条 `rerun-if` 指令（见下文）。若输出了这些指令，Cargo 仅在给定值发生变化时重新运行脚本。若 Cargo 重新运行你自己 crate 或依赖的构建脚本而你不清楚原因，见 FAQ 中的[「为什么 Cargo 在重新编译我的代码？」](../../05-faq/#why-is-cargo-rebuilding-my-code)。

[`exclude` and `include` fields]: ../the-manifest-format/#the-exclude-and-include-fields

### `cargo::rerun-if-changed=PATH` {#rerun-if-changed}

`rerun-if-changed` 指令告诉 Cargo，若给定路径的文件发生变化，则重新运行构建脚本。目前 Cargo 仅使用文件系统最后修改时间戳「mtime」判断文件是否变化，并与构建脚本上次运行时的内部缓存时间戳比较。

若路径指向目录，会扫描整个目录以检测任何修改。

若构建脚本在任何情况下都无需重新运行，输出 `cargo::rerun-if-changed=build.rs` 是防止其被重新运行的简单方式（否则，若未输出任何 `rerun-if` 指令，默认会扫描整个包目录以检测变化）。Cargo 会自动处理脚本本身是否需要重新编译，脚本重新编译后当然会重新运行。否则，指定 `build.rs` 是冗余且不必要的。

### `cargo::rerun-if-env-changed=NAME` {#rerun-if-env-changed}

`rerun-if-env-changed` 指令告诉 Cargo，若给定名称的环境变量值发生变化，则重新运行构建脚本。

注意，此处的环境变量适用于 `CC` 等全局环境变量，不能用于 [Cargo 为构建脚本设置的][build-env] `TARGET` 等环境变量。使用的是 `cargo` 调用接收的环境变量，而非构建脚本可执行文件接收的环境变量。

自 1.46 起，在源代码中使用 [`env!`][env-macro] 和 [`option_env!`][option-env-macro] 会自动检测变化并触发重建。对于已被这些宏引用的变量，不再需要 `rerun-if-env-changed`。

[option-env-macro]: https://doc.rust-lang.org/std/macro.option_env.html

## `links` Manifest 键 {#the-links-manifest-key}

可在 `Cargo.toml` manifest 中设置 `package.links` 键，声明包与给定原生库链接。此 manifest 键的目的是让 Cargo 了解包的 native 依赖集合，并提供在包构建脚本之间传递元数据的规范机制。

```toml
[package]
# ...
links = "foo"
```

此 manifest 声明包链接到 `libfoo` 原生库。使用 `links` 键时，包必须有构建脚本，且构建脚本应使用 [`rustc-link-lib` 指令](#rustc-link-lib) 链接该库。

主要地，Cargo 要求每个 `links` 值最多对应一个包。换言之，禁止两个包链接同一原生库。这有助于防止 crate 之间的重复符号。但请注意，已有[约定](#-sys-packages)可缓解此问题。

构建脚本可以键值对形式生成任意元数据。此元数据通过 `cargo::metadata=KEY=VALUE` 指令设置。

元数据会传给**依赖**包的构建脚本。例如，若包 `foo` 依赖 `bar`，而 `bar` 链接 `baz`，若 `bar` 在其构建脚本元数据中生成 `key=value`，则 `foo` 的构建脚本会有环境变量 `DEP_BAZ_KEY=value`（注意使用的是 `links` 键的值，且 `key` 的大小写会变化）。见[「使用另一个 `sys` crate」][using-another-sys] 示例了解用法。

注意，元数据仅传给直接依赖，不传给传递依赖。

> **MSRV：** `cargo::metadata=KEY=VALUE` 需要 1.77。
> 若要支持旧版本，使用 `cargo:KEY=VALUE`（不支持的指令会被假定为元数据键）。

[using-another-sys]: 01-build-script-examples/#using-another-sys-crate

## `*-sys` 包 {#-sys-packages}
某些链接系统库的 Cargo 包遵循以 `-sys` 为后缀的命名约定。任何名为 `foo-sys` 的包应提供两大功能：

* 库 crate 应链接到原生库 `libfoo`。通常会先探测当前系统是否存在 `libfoo`，再回退到从源码构建。
* 库 crate 应提供 `libfoo` 中类型和函数的**声明**，但**不应**提供更高层抽象。

`*-sys` 包集合为链接原生库提供了通用依赖集。遵循此 native 库相关包约定有若干好处：

* 对 `foo-sys` 的通用依赖可缓解「每个 `links` 值仅一个包」的规则。
* 其他 `-sys` 包可利用 `DEP_LINKS_KEY=value` 环境变量更好地与其他包集成。见[「使用另一个 `sys` crate」][using-another-sys] 示例。
* 通用依赖可集中处理发现 `libfoo` 本身（或从源码构建）的逻辑。
* 这些依赖易于[覆盖](#overriding-build-scripts)。

通常会有不带 `-sys` 后缀的配套包，在 sys 包之上提供安全的高层抽象。例如，[`git2` crate] 为 [`libgit2-sys` crate] 提供高层接口。

[`git2` crate]: https://crates.io/crates/git2
[`libgit2-sys` crate]: https://crates.io/crates/libgit2-sys

## 覆盖构建脚本 {#overriding-build-scripts}

若 manifest 包含 `links` 键，Cargo 支持用自定义库覆盖指定的构建脚本。此功能的目的是完全避免运行相关构建脚本，而是预先提供元数据。

要覆盖构建脚本，在任何可接受的 [`config.toml`](../06-configuration/) 文件中放置以下配置。

```toml
[target.x86_64-unknown-linux-gnu.foo]
rustc-link-lib = ["foo"]
rustc-link-search = ["/path/to/foo"]
rustc-flags = "-L /some/path"
rustc-cfg = ['key="value"']
rustc-env = {key = "value"}
rustc-cdylib-link-arg = ["…"]
metadata_key1 = "value"
metadata_key2 = "value"
```

使用此配置时，若包声明链接到 `foo`，则构建脚本**不会**被编译或运行，而是使用指定的元数据。

不应使用 `warning`、`rerun-if-changed` 和 `rerun-if-env-changed` 键，它们会被忽略。

## Jobserver {#jobserver}
Cargo 和 `rustc` 使用为 GNU make 开发的 [jobserver 协议][jobserver protocol] 协调跨进程的并发。它本质上是控制并发运行任务数的信号量。并发可通过 `--jobs` 标志设置，默认为逻辑 CPU 数。

每个构建脚本从 Cargo 继承一个 job 槽，运行时应尽量只使用一个 CPU。若脚本希望并行使用更多 CPU，应使用 [`jobserver` crate] 与 Cargo 协调。

例如，[`cc` crate] 可启用可选的 `parallel` 特性，使用 jobserver 协议尝试同时构建多个 C 文件。

[`cc` crate]: https://crates.io/crates/cc
[`jobserver` crate]: https://crates.io/crates/jobserver
[jobserver protocol]: http://make.mad-scientist.net/papers/jobserver-implementation/
[crates.io]: https://crates.io/
