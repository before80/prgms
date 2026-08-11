+++
title = "11-外部工具"
date = 2026-07-30T14:49:00+08:00
weight = 48
type = "docs"
description = "与 IDE、自定义工具集成 Cargo"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 外部工具 {#external-tools}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/external-tools.html](https://doc.rust-lang.org/cargo/reference/external-tools.html)


Cargo 的目标之一是与第三方工具（如 IDE 与其他构建系统）简单集成。为便于集成，Cargo 提供若干设施：

* [`cargo metadata`] 命令，以 JSON 输出包结构与依赖信息，

* `--message-format` 标志，输出特定构建的相关信息，以及

* 对自定义子命令的支持。


## 关于包结构的信息 {#information-about-package-structure}
你可以使用 [`cargo metadata`] 命令获取包结构与依赖信息。输出格式细节见 [`cargo metadata`] 文档。

该格式是稳定且带版本的。调用 `cargo metadata` 时应显式传递 `--format-version` 标志，以避免前向不兼容风险。

若你使用 Rust，可用 [cargo_metadata] crate 解析输出。

[cargo_metadata]: https://crates.io/crates/cargo_metadata
[`cargo metadata`]: ../../cargo-commands/manifest-commands/05-cargo-metadata/

## JSON 消息 {#json-messages}
传入 `--message-format=json` 时，Cargo 会在构建期间输出以下信息：

* 编译器错误与警告，

* 生成的产物，

* 构建脚本的结果（例如原生依赖）。

输出以每行一个 JSON 对象的格式发往 stdout。`reason` 字段区分不同类型的消息。
`package_id` 字段是引用该包的唯一标识符，也可用作许多命令的 `--package` 参数。语法文法见章节 [包 ID 规范][Package ID Specifications]。

> **注意：** `--message-format=json` 仅控制 Cargo 与 Rustc 的输出。
> 无法控制其他工具的输出，
> 例如 `cargo run --message-format=json`，
> 或过程宏的任意输出。
> 这些情况下一种可行的变通办法是：仅当一行以 `{` 开头时才将其解释为 JSON。

`--message-format` 选项还可接受额外的格式化值，以改变 JSON 消息的计算与呈现方式。更多细节见 [build 命令文档][build command documentation] 中对 `--message-format` 选项的说明。

若你使用 Rust，可用 [cargo_metadata] crate 解析这些消息。

> **MSRV：** `package_id` 成为包 ID 规范需要 1.77。在此之前，它是不透明的。

[build command documentation]: ../../cargo-commands/build-commands/02-cargo-build/
[cargo_metadata]: https://crates.io/crates/cargo_metadata
[Package ID Specifications]: ../10-package-id-specifications/

### 编译器消息 {#compiler-messages}
「compiler-message」消息包含来自编译器的输出，如警告与错误。`rustc` 的消息格式细节见 [rustc JSON 章节](https://doc.rust-lang.org/rustc/json.html)，其嵌入在以下结构中：

```javascript
{
    /* "reason" 表示消息种类。 */
    "reason": "compiler-message",
    /* 包 ID，用于引用该包的唯一标识符。 */
    "package_id": "file:///path/to/my-package#0.1.0",
    /* 包清单的绝对路径。 */
    "manifest_path": "/path/to/my-package/Cargo.toml",
    /* 生成该消息的 Cargo 目标（lib、bin、example 等）。 */
    "target": {
        /* 目标种类数组。
           - lib 目标列出清单中的 `crate-type` 值，
             如 "lib"、"rlib"、"dylib"、
             "proc-macro" 等。（默认 ["lib"]）
           - 二进制为 ["bin"]
           - 示例为 ["example"]
           - 集成测试为 ["test"]
           - 基准测试为 ["bench"]
           - 构建脚本为 ["custom-build"]
        */
        "kind": [
            "lib"
        ],
        /* crate 类型数组。
           - lib 与示例库列出清单中的 `crate-type` 值，
             如 "lib"、"rlib"、"dylib"、
             "proc-macro" 等。（默认 ["lib"]）
           - 所有其他目标种类为 ["bin"]
        */
        "crate_types": [
            "lib"
        ],
        /* 目标名称。
           对 lib 目标，短横线会替换为下划线。
        */
        "name": "my_package",
        /* 目标根源文件的绝对路径。 */
        "src_path": "/path/to/my-package/src/lib.rs",
        /* 目标的 Rust edition。
           默认为包的 edition。
        */
        "edition": "2018",
        /* 所需特性的数组。
           若未设置所需特性，则不包含此属性。
        */
        "required-features": ["feat1"],
        /* 目标是否应由 `cargo doc` 生成文档。 */
        "doc": true,
        /* 此目标是否启用了文档测试，以及
           该目标是否与文档测试兼容。
        */
        "doctest": true
        /* 此目标是否应使用 `--test` 构建并运行
        */
        "test": true
    },
    /* 编译器发出的消息。

    细节见 https://doc.rust-lang.org/rustc/json.html。
    */
    "message": {
        /* ... */
    }
}
```

### 产物消息 {#artifact-messages}
对每一个编译步骤，都会发出结构如下的「compiler-artifact」消息：

```javascript
{
    /* "reason" 表示消息种类。 */
    "reason": "compiler-artifact",
    /* 包 ID，用于引用该包的唯一标识符。 */
    "package_id": "file:///path/to/my-package#0.1.0",
    /* 包清单的绝对路径。 */
    "manifest_path": "/path/to/my-package/Cargo.toml",
    /* 生成产物的 Cargo 目标（lib、bin、example 等）。
       细节见上方 `compiler-message` 的定义。
    */
    "target": {
        "kind": [
            "lib"
        ],
        "crate_types": [
            "lib"
        ],
        "name": "my_package",
        "src_path": "/path/to/my-package/src/lib.rs",
        "edition": "2018",
        "doc": true,
        "doctest": true,
        "test": true
    },
    /* profile 表示使用了哪些编译器设置。 */
    "profile": {
        /* 优化级别。 */
        "opt_level": "0",
        /* 调试级别，整数 0、1 或 2，或字符串
           "line-directives-only" 或 "line-tables-only"。若为 `null`，
           则表示 rustc 的默认值 0。
        */
        "debuginfo": 2,
        /* 是否启用调试断言。 */
        "debug_assertions": true,
        /* 是否启用溢出检查。 */
        "overflow_checks": true,
        /* 是否使用了 `--test` 标志。 */
        "test": false
    },
    /* 已启用特性的数组。 */
    "features": ["feat1", "feat2"],
    /* 此步骤生成的文件数组。 */
    "filenames": [
        "/path/to/my-package/target/debug/libmy_package.rlib",
        "/path/to/my-package/target/debug/deps/libmy_package-be9f3faac0a26ef0.rmeta"
    ],
    /* 所创建可执行文件路径的字符串，若此步骤未生成可执行文件则为 null。
    */
    "executable": null,
    /* 此步骤是否实际被执行。
       为 `true` 表示已有产物是最新的，
       未执行 `rustc`。为 `false` 表示运行了
       `rustc` 来生成产物。
    */
    "fresh": true
}

```

### 构建脚本输出 {#build-script-output}
「build-script-executed」消息包含构建脚本的解析输出。注意即使未运行构建脚本也会发出此消息；它会显示先前缓存的值。构建脚本输出的更多细节见[构建脚本章节](../build-scripts/)。

```javascript
{
    /* "reason" 表示消息种类。 */
    "reason": "build-script-executed",
    /* 包 ID，用于引用该包的唯一标识符。 */
    "package_id": "file:///path/to/my-package#0.1.0",
    /* 要链接的库数组，由 `cargo::rustc-link-lib`
       指令指示。注意字符串中可能包含 "KIND=" 前缀，
       其中 KIND 是库种类。
    */
    "linked_libs": ["foo", "static=bar"],
    /* 要加入库搜索路径的路径数组，由
       `cargo::rustc-link-search` 指令指示。注意字符串中可能包含
       "KIND=" 前缀，其中 KIND 是库种类。
    */
    "linked_paths": ["/some/path", "native=/another/path"],
    /* 要启用的 cfg 值数组，由 `cargo::rustc-cfg`
       指令指示。
    */
    "cfgs": ["cfg1", "cfg2=\"string\""],
    /* 要设置的环境变量 [KEY, VALUE] 数组的数组，由
       `cargo::rustc-env` 指令指示。
    */
    "env": [
        ["SOME_KEY", "some value"],
        ["ANOTHER_KEY", "another value"]
    ],
    /* 编译当前包时用作 `OUT_DIR` 环境变量值的绝对路径。
    */
    "out_dir": "/some/path/in/target/dir"
}
```

### 构建完成 {#build-finished}
「build-finished」消息在构建结束时发出。

```javascript
{
    /* "reason" 表示消息种类。 */
    "reason": "build-finished",
    /* 构建是否成功完成。 */
    "success": true,
}
```

此消息有助于工具知道何时停止读取 JSON 消息。`cargo test` 或 `cargo run` 等命令可能在构建完成后产生额外输出。此消息让工具知道 Cargo 不会再产生额外的 JSON 消息，但之后仍可能有额外输出（例如 `cargo run` 所执行程序生成的输出）。

> 注意：测试的 JSON 输出有实验性的仅 nightly 支持，
> 若启用，在「build-finished」消息之后可能开始出现额外的测试专用 JSON 消息。

## 自定义子命令 {#custom-subcommands}
Cargo 设计为可扩展新子命令，而无需修改 Cargo 本身。这是通过将形如 cargo `(?<command>[^ ]+)` 的调用转换为外部工具 `cargo-${command}` 的调用来实现的。外部工具必须存在于用户的某个 `$PATH` 目录中。

> **注意**：Cargo 默认优先使用 `$CARGO_HOME/bin` 中的外部工具，
> 而非 `$PATH`。用户可通过将 `$CARGO_HOME/bin`
> 加入 `$PATH` 来覆盖此优先级。

当 Cargo 调用自定义子命令时，传给子命令的第一个参数照常是自定义子命令的文件名。第二个参数是子命令名称本身。例如，调用 `cargo-${command}` 时第二个参数为 `${command}`。命令行上的任何额外参数会原样转发。

Cargo 也可通过 `cargo help ${command}` 显示自定义子命令的帮助输出。Cargo 假定若子命令的第三个参数为 `--help`，它会打印帮助消息。因此，`cargo help ${command}` 会调用 `cargo-${command} ${command} --help`。

自定义子命令可使用 `CARGO` 环境变量回调 Cargo。或者，它可以链接 `cargo` crate 作为库，但这种方法有缺点：

* 作为库的 Cargo 不稳定：API 可能在无弃用的情况下变更
* 所链接的 Cargo 库版本可能与 Cargo 二进制文件不同

相反，鼓励使用 CLI 接口来驱动 Cargo。可用 [`cargo metadata`] 命令获取关于当前项目的信息（[`cargo_metadata`] crate 为此命令提供 Rust 接口）。

[`cargo metadata`]: ../../cargo-commands/manifest-commands/05-cargo-metadata/
[`cargo_metadata`]: https://crates.io/crates/cargo_metadata
