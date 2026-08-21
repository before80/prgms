+++
title = "第15章 链接"
date = 2026-08-18T08:45:00+08:00
weight = 106
type = "docs"
description = "链接 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/linkage.html](https://doc.rust-lang.org/reference/linkage.html)

r[link]
# 链接

> **注意**
> 本节更多是从编译器而非语言本身的角度来描述的。

r[link.intro]
编译器支持多种将 crate 静态或动态链接在一起的方法。本节将探讨这些将 crate 链接在一起的各种方法；关于原生库的更多信息，可见[本书的 FFI 章节][ffi]。

[ffi]: ../book/ch20-01-unsafe-rust.html#using-extern-functions-to-call-external-code

r[link.type]
在一次编译会话中，编译器可以通过命令行标志或 `crate_type` 属性生成多种产物。若指定了一个或多个命令行标志，则所有 `crate_type` 属性都会被忽略，仅按命令行指定的产物进行构建。

r[link.bin]
* `--crate-type=bin`，`#![crate_type = "bin"]` - 将生成可运行的可执行文件。这要求 crate 中存在 `main` 函数，程序开始执行时会运行该函数。这会链接进所有 Rust 与原生依赖，生成单个可分发的二进制文件。这是默认的 crate 类型。

r[link.lib]
* `--crate-type=lib`，`#![crate_type = "lib"]` - 将生成一个 Rust 库。至于具体生成什么，这是一个模糊的概念，因为库可以表现为多种形式。这个通用的 `lib` 选项旨在生成“编译器推荐”风格的库。输出库始终可被 rustc 使用，但实际库类型可能会随时间变化。其余输出类型都是库的不同变体，而 `lib` 类型可视为其中某一种的别名（但具体是哪一种由编译器定义）。

r[link.dylib]
* `--crate-type=dylib`，`#![crate_type = "dylib"]` - 将生成一个动态 Rust 库。这与 `lib` 输出类型不同，因为它强制生成动态库。生成的动态库可用作其他库和/或可执行文件的依赖。此输出类型在 Linux 上创建 `*.so` 文件，在 macOS 上创建 `*.dylib` 文件，在 Windows 上创建 `*.dll` 文件。

r[link.staticlib]
* `--crate-type=staticlib`，`#![crate_type = "staticlib"]` - 将生成一个静态系统库。这与其他库输出不同，因为编译器永远不会尝试链接到 `staticlib` 输出。此输出类型的目的是创建一个静态库，其中包含本地 crate 的全部代码以及所有上游依赖。此输出类型在 Linux、macOS 和 Windows（MinGW）上创建 `*.a` 文件，在 Windows（MSVC）上创建 `*.lib` 文件。推荐在例如将 Rust 代码链接进现有非 Rust 应用程序等场景中使用此格式，因为它不会对其他 Rust 代码产生动态依赖。

  请注意，静态库可能具有的任何动态依赖（例如对系统库的依赖，或对编译为动态库的 Rust 库的依赖）都必须在从别处链接该静态库时手动指定。`--print=native-static-libs` 标志可能对此有帮助。

  还请注意，由于生成的静态库包含所有依赖（包括标准库）的代码，并且也导出它们的所有公共符号，将静态库链接进可执行文件或共享库时可能需要特别小心。对于共享库，必须通过例如链接器或符号版本脚本、导出符号列表（macOS）或模块定义文件（Windows）等方式限制导出符号列表。此外，可以移除未使用的节，以去掉依赖中实际未使用的全部代码（例如 `--gc-sections`，或 macOS 上的 `-dead_strip`）。

r[link.cdylib]
* `--crate-type=cdylib`，`#![crate_type = "cdylib"]` - 将生成一个动态系统库。这用于编译一个将由另一种语言加载的动态库。此输出类型在 Linux 上创建 `*.so` 文件，在 macOS 上创建 `*.dylib` 文件，在 Windows 上创建 `*.dll` 文件。

r[link.rlib]
* `--crate-type=rlib`，`#![crate_type = "rlib"]` - 将生成一个“Rust 库”文件。这用作中间产物，可视为一种“静态 Rust 库”。与 `staticlib` 文件不同，这些 `rlib` 文件会在后续链接中由编译器解释。这本质上意味着 `rustc` 会像在动态库中查找元数据一样，在 `rlib` 文件中查找元数据。此输出形式用于生成静态链接的可执行文件以及 `staticlib` 输出。

r[link.proc-macro]
* `--crate-type=proc-macro`，`#![crate_type = "proc-macro"]` - 所生成的输出未予规定，但如果向其提供了 `-L` 路径，则编译器会将输出产物识别为宏，并可加载到程序中使用。以此 crate 类型编译的 crate 只能导出[过程宏][procedural macros]。编译器会自动设置 `proc_macro` [配置选项][configuration option]。这些 crate 始终以编译器自身构建时所用的相同目标进行编译。例如，如果你在带有 `x86_64` CPU 的 Linux 上执行编译器，则目标将是 `x86_64-unknown-linux-gnu`，即使该 crate 是另一个正在为不同目标构建的 crate 的依赖。

r[link.repetition]
请注意，这些输出在某种意义上是可叠加的：若指定了多种，则编译器会生成每种形式的输出而无需重新编译。不过，这仅适用于由同一方法指定的输出。若仅指定了 `crate_type` 属性，则它们都会被构建；但若指定了一个或多个 `--crate-type` 命令行标志，则只会构建那些输出。

r[link.dependency]
面对所有这些不同类型的输出，若 crate A 依赖于 crate B，则编译器可能在系统中以多种不同形式找到 B。然而，编译器只会查找 `rlib` 格式和动态库格式。对于依赖库的这两种选项，编译器必须在某个时刻在这两种格式之间做出选择。基于此，编译器在确定将使用何种格式的依赖时遵循以下规则：

r[link.dependency-staticlib]
1. 若正在生成静态库，则要求所有上游依赖都以 `rlib` 格式可用。这一要求源于动态库无法转换为静态格式。

   请注意，不可能将原生动态依赖链接进静态库；在这种情况下，会打印关于所有未链接的原生动态依赖的警告。

r[link.dependency-rlib]

2. 若正在生成 `rlib` 文件，则对上游依赖可用的格式没有限制。只要求所有上游依赖都可供读取元数据。

   其原因是 `rlib` 文件不包含其任何上游依赖。若所有 `rlib` 文件都包含一份 `libstd.rlib` 的副本，效率会很低！

r[link.dependency-prefer-dynamic]

3. 若正在生成可执行文件且未指定 `-C prefer-dynamic` 标志，则首先尝试以 `rlib` 格式查找依赖。若某些依赖不以 rlib 格式可用，则尝试动态链接（见下文）。

r[link.dependency-dynamic]

4. 若正在生成动态库，或正在生成动态链接的可执行文件，则编译器会尝试协调以 rlib 或 dylib 格式可用的依赖，以创建最终产物。

   编译器的一个主要目标是确保任何库在任何产物中都不会出现超过一次。例如，若动态库 B 和 C 各自静态链接到库 A，则一个 crate 不能同时链接到 B 和 C，因为会有两份 A 的副本。编译器允许混合 rlib 和 dylib 格式，但必须满足这一限制。

   编译器目前没有实现任何提示应以何种格式链接库的方法。在动态链接时，编译器会尝试最大化动态依赖，同时仍允许某些依赖通过 rlib 链接进来。

   对于大多数情况，若进行动态链接，建议将所有库都以 dylib 形式提供。对于其他情况，若编译器无法确定应以何种格式链接各个库，则会发出警告。

一般而言，`--crate-type=bin` 或 `--crate-type=lib` 应足以满足所有编译需求，其他选项仅在需要对 crate 的输出格式进行更细粒度控制时可用。

r[link.crt]
## 静态与动态 C 运行时

r[link.crt.intro]
标准库总体上力求在适当时为各目标同时支持静态链接与动态链接的 C 运行时。例如，`x86_64-pc-windows-msvc` 和 `x86_64-unknown-linux-musl` 目标通常同时提供两种运行时，由用户选择想要使用的那一种。编译器中的所有目标都有一种默认的 C 运行时链接模式。通常目标默认动态链接，但也有默认静态链接的例外，例如：

* `arm-unknown-linux-musleabi`
* `arm-unknown-linux-musleabihf`
* `armv7-unknown-linux-musleabihf`
* `i686-unknown-linux-musl`
* `x86_64-unknown-linux-musl`

r[link.crt.crt-static]
C 运行时的链接配置会遵循 `crt-static` 目标特性。这些目标特性通常通过传给编译器本身的命令行标志来配置。例如，要启用静态运行时，你可以执行：

```sh
rustc -C target-feature=+crt-static foo.rs
```

而要动态链接到 C 运行时，你可以执行：

```sh
rustc -C target-feature=-crt-static foo.rs
```

r[link.crt.ineffective]
不支持在 C 运行时链接方式之间切换的目标会忽略此标志。建议在编译器成功后检查生成的二进制文件，确保其按你的预期进行了链接。

r[link.crt.target_feature]
Crate 也可以获知 C 运行时是如何被链接的。例如，在 MSVC 上，代码需要根据所链接的运行时以不同方式编译（例如使用 `/MT` 或 `/MD`）。这目前通过 [`cfg` 属性的 `target_feature` 选项][`cfg` attribute `target_feature` option] 导出：

```rust
#[cfg(target_feature = "crt-static")]
fn foo() {
    println!("the C runtime should be statically linked");
}

#[cfg(not(target_feature = "crt-static"))]
fn foo() {
    println!("the C runtime should be dynamically linked");
}
```

还请注意，Cargo 构建脚本可以通过[环境变量][cargo]获知此特性。在构建脚本中，你可以通过以下方式检测链接方式：

```rust
use std::env;

fn main() {
    let linkage = env::var("CARGO_CFG_TARGET_FEATURE").unwrap_or(String::new());

    if linkage.contains("crt-static") {
        println!("the C runtime will be statically linked");
    } else {
        println!("the C runtime will be dynamically linked");
    }
}
```

[cargo]: ../cargo/reference/environment-variables.html#environment-variables-cargo-sets-for-build-scripts

要在本地使用此特性，通常会使用 `RUSTFLAGS` 环境变量，通过 Cargo 向编译器指定标志。例如，要在 MSVC 上编译静态链接的二进制文件，你可以执行：

```sh
RUSTFLAGS='-C target-feature=+crt-static' cargo build --target x86_64-pc-windows-msvc
```

r[link.foreign-code]
## 混合 Rust 与外来代码库

r[link.foreign-code.foreign-linkers]
若你将 Rust 与外来代码（例如 C、C++）混合，并希望制作一个同时包含这两类代码的单一二进制文件，最终二进制链接有两种方法：

* 使用 `rustc`。使用 `-L <directory>` 和 `-l<library>` 等 rustc 参数，和/或在 Rust 代码中使用 `#[link]` 指令，传入任何非 Rust 库。若需要链接 `.o` 文件，可以使用 `-Clink-arg=file.o`。
* 使用你的外来链接器。在这种情况下，你首先需要生成一个 Rust `staticlib` 目标，并将其传入外来链接器调用。若需要链接多个 Rust 子系统，你需要生成一个*单一*的 `staticlib`，或许使用大量 `extern crate` 语句来包含多个 Rust `rlib`。多个 Rust `staticlib` 文件很可能会冲突。

目前不支持将 `rlib` 直接传入外来链接器。

> **注意**
> 就本节而言，用不同实例的 Rust 运行时编译或链接的 Rust 代码算作“外来代码”。

r[link.unwinding]
### 禁止的链接与展开

r[link.unwinding.intro]
只有在按照以下规则一致地构建二进制文件时，才能使用 panic 展开。

r[link.unwinding.potential]
若满足以下任一条件，则称一个 Rust 产物为*潜在可展开*的：
- 该产物使用 [`unwind` panic 处理器][panic.panic_handler]。
- 该产物包含以 `unwind` [panic 策略][panic strategy]构建的 crate，且该 crate 使用 `-unwind` ABI 调用了某个函数。
- 该产物以 `"Rust"` ABI 调用了在另一个拥有独立 Rust 运行时副本的 Rust 产物中运行的代码，且该另一产物是潜在可展开的。

> **注意**
> 此定义刻画了 Rust 产物内部的 `"Rust"` ABI 调用是否可能发生展开。

r[link.unwinding.prohibited]
若一个 Rust 产物是潜在可展开的，则其所有 crate 都必须以 `unwind` [panic 策略][panic strategy]构建。否则，展开可能导致未定义行为。

> **注意**
> 若你使用 `rustc` 进行链接，这些规则会自动强制执行。若你*不*使用 `rustc` 进行链接，则必须小心确保在整个二进制文件中一致地处理展开。不使用 `rustc` 进行链接包括使用 `dlopen` 或类似设施的情况，此时由系统运行时完成链接，而 `rustc` 并不参与。这只可能在混合使用不同 [`-C panic`] 标志的代码时发生，因此大多数用户不必为此担心。

> **注意**
> 为了保证一个库无论在链接时使用何种 panic 运行时都是健全的（且可与 `rustc` 链接），可以使用 [`ffi_unwind_calls` lint]。该 lint 会标记对 `-unwind` 外来函数或函数指针的任何调用。

[`cfg` attribute `target_feature` option]: conditional-compilation.md#target_feature
[`ffi_unwind_calls` lint]: ../rustc/lints/listing/allowed-by-default.html#ffi-unwind-calls
[configuration option]: conditional-compilation.md
[procedural macros]: procedural-macros.md
[panic strategy]: panic.md#panic-strategy
[`-C panic`]: ../rustc/codegen-options/index.html#panic
