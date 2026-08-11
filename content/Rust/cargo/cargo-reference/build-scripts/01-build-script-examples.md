+++
title = "01-构建脚本示例"
date = 2026-07-30T14:49:00+08:00
weight = 45
type = "docs"
description = "常见 build.rs 写法示例"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 构建脚本示例 {#build-script-examples}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/build-script-examples.html](https://doc.rust-lang.org/cargo/reference/build-script-examples.html)


以下各节展示编写构建脚本的一些示例。

部分常见构建脚本功能可通过 [crates.io] 上的 crate 实现。查看 [`build-dependencies` 关键词](https://crates.io/keywords/build-dependencies) 了解可用选项。以下是一些流行 crate 的示例[^†]：

* [`bindgen`](https://crates.io/crates/bindgen) --- 自动生成 C 库的 Rust FFI 绑定。
* [`cc`](https://crates.io/crates/cc) --- 编译 C/C++/汇编。
* [`pkg-config`](https://crates.io/crates/pkg-config) --- 使用 `pkg-config` 工具检测系统库。
* [`cmake`](https://crates.io/crates/cmake) --- 运行 `cmake` 构建工具以构建原生库。
* [`autocfg`](https://crates.io/crates/autocfg)、
  [`rustc_version`](https://crates.io/crates/rustc_version)、
  [`version_check`](https://crates.io/crates/version_check) --- 这些 crate 提供基于当前 `rustc`（如编译器版本）实现条件编译的方式。

[^†]: 此列表并非背书。请评估依赖以确定哪个适合你的项目。

## 代码生成 {#code-generation}
某些 Cargo 包出于各种原因需要在编译前生成代码。此处我们将通过一个简单示例，在构建脚本中生成库调用。

首先，看一下此包的目录结构：

```text
.
├── Cargo.toml
├── build.rs
└── src
    └── main.rs

1 directory, 3 files
```

可以看到，我们有 `build.rs` 构建脚本，二进制文件在 `main.rs`。此包有基本 manifest：

```toml
# Cargo.toml
[package]
name = "hello-from-generated-code"
version = "0.1.0"
edition = "2024"
```

看一下构建脚本内容：

```rust,no_run
// build.rs

use std::env;
use std::fs;
use std::path::Path;

fn main() {
    let out_dir = env::var_os("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("hello.rs");
    fs::write(
        &dest_path,
        "pub fn message() -> &'static str {
            \"Hello, World!\"
        }
        "
    ).unwrap();
    println!("cargo::rerun-if-changed=build.rs");
}
```

此处有几个要点：

* 脚本使用 `OUT_DIR` 环境变量确定输出文件位置。可用进程的当前工作目录查找输入文件位置，但此例没有输入文件。
* 通常，构建脚本不应修改 `OUT_DIR` 外的任何文件。初看似乎没问题，但将此类 crate 作为依赖使用时会有问题，因为 `.cargo/registry` 中的源码应不可变是*隐式*不变量。`cargo` 打包时不允许此类脚本。
  * 有时项目希望检入生成的文件并将其视为源码。但此时文件不应由 `build.rs` 生成。而应使用测试或类似机制，检查文件是否与生成版本完全一致*且不一致时失败*，并在 CI 中运行该测试。（测试可生成临时文件进行比较；若要更新生成文件，可用临时文件替换检入的文件。）
* 此脚本较简单，仅写出一个小生成文件。可以想象其他更复杂操作，例如从 C 头文件或其他语言定义生成 Rust 模块。
* [`rerun-if-changed` 指令](../../#rerun-if-changed) 告诉 Cargo，仅当构建脚本本身变化时才需重新运行。没有此行时，若包内任何文件变化，Cargo 会自动运行构建脚本。若代码生成使用某些输入文件，应在此处打印每个输入文件的列表。

接下来看库本身：

```rust,ignore
// src/main.rs

include!(concat!(env!("OUT_DIR"), "/hello.rs"));

fn main() {
    println!("{}", message());
}
```

这是关键所在。库使用 rustc 定义的 [`include!` 宏][include-macro]，结合 [`concat!`][concat-macro] 和 [`env!`][env-macro] 宏，将生成文件（`hello.rs`）包含进 crate 的编译。

使用此结构，crate 可从构建脚本包含任意数量的生成文件。

[include-macro]: https://doc.rust-lang.org/std/macro.include.html
[concat-macro]: https://doc.rust-lang.org/std/macro.concat.html
[env-macro]: https://doc.rust-lang.org/std/macro.env.html

## 构建原生库 {#building-a-native-library}
有时需要在包中构建一些原生 C 或 C++ 代码。这是利用构建脚本在 Rust crate 之前构建原生库的又一典型用例。作为示例，我们将创建一个调用 C 打印「Hello, World!」的 Rust 库。

与上面类似，先看包布局：

```text
.
├── Cargo.toml
├── build.rs
└── src
    ├── hello.c
    └── main.rs

1 directory, 4 files
```

与之前非常相似！接下来是 manifest：

```toml
# Cargo.toml
[package]
name = "hello-world-from-c"
version = "0.1.0"
edition = "2024"
```

目前不使用任何构建依赖，先看构建脚本：

```rust,no_run
// build.rs

use std::process::Command;
use std::env;
use std::path::Path;

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();

    // 注意，此方法有若干缺点，下方注释说明如何改进这些命令的可移植性。
    Command::new("gcc").args(&["src/hello.c", "-c", "-fPIC", "-o"])
                       .arg(&format!("{}/hello.o", out_dir))
                       .status().unwrap();
    Command::new("ar").args(&["crus", "libhello.a", "hello.o"])
                      .current_dir(&Path::new(&out_dir))
                      .status().unwrap();

    println!("cargo::rustc-link-search=native={}", out_dir);
    println!("cargo::rustc-link-lib=static=hello");
    println!("cargo::rerun-if-changed=src/hello.c");
}
```

此构建脚本首先将 C 文件编译为目标文件（调用 `gcc`），再将目标文件转换为静态库（调用 `ar`）。最后向 Cargo 反馈：输出在 `out_dir`，编译器应通过 `-l static=hello` 标志静态链接 crate 到 `libhello.a`。

注意，此硬编码方式有若干缺点：

* `gcc` 命令本身不可跨平台移植。例如 Windows 平台通常没有 `gcc`，并非所有 Unix 平台都有 `gcc`。`ar` 命令情况类似。
* 这些命令未考虑交叉编译。若交叉编译到 Android 等平台，`gcc` 不太可能生成 ARM 可执行文件。

不过不必担心，此处 `build-dependencies` 条目会有帮助！Cargo 生态中有若干包使此类任务更简单、可移植且标准化。我们试试 [crates.io] 上的 [`cc` crate](https://crates.io/crates/cc)。首先，在 `Cargo.toml` 的 `build-dependencies` 中添加：

```toml
[build-dependencies]
cc = "1.0"
```

并重写构建脚本以使用该 crate：

```rust,ignore
// build.rs

fn main() {
    cc::Build::new()
        .file("src/hello.c")
        .compile("hello");
    println!("cargo::rerun-if-changed=src/hello.c");
}
```

[`cc` crate] 抽象了 C 代码构建脚本的多种需求：

* 调用合适的编译器（Windows 用 MSVC，MinGW 用 `gcc`，Unix 平台用 `cc` 等）。
* 通过向所用编译器传递适当标志，考虑 `TARGET` 变量。
* 其他环境变量如 `OPT_LEVEL`、`DEBUG` 等都会自动处理。
* stdout 输出和 `OUT_DIR` 位置也由 `cc` 库处理。

此处可见，尽可能将功能委托给通用构建依赖，而不是在所有构建脚本中重复逻辑，带来的主要好处！

回到案例，快速看一下 `src` 目录内容：

```c
// src/hello.c

#include <stdio.h>

void hello() {
    printf("Hello, World!\n");
}
```

```rust,ignore
// src/main.rs

// 注意没有 `#[link]` 属性。我们将选择链接什么的责任委托给构建脚本，而不是在源文件中硬编码。
unsafe extern { fn hello(); }

fn main() {
    unsafe { hello(); }
}
```

完成！这应完成从 Cargo 包使用构建脚本构建 C 代码的示例。这也说明为何在许多情况下使用构建依赖至关重要，甚至更加简洁！

我们还简要看到构建脚本如何纯粹为构建过程使用 crate 作为依赖，而运行时 crate 本身不需要。

[`cc` crate]: https://crates.io/crates/cc

## 链接系统库 {#linking-to-system-libraries}
此示例演示如何链接系统库，以及构建脚本如何支持此用例。

Rust crate 经常希望链接系统提供的原生库以绑定其功能，或仅作为实现细节的一部分。以平台无关方式执行此操作是较微妙的问题。若可能，最好尽可能将此工作外包，使消费者尽可能简单。

此示例中，我们将创建与系统 zlib 库的绑定。zlib 是大多数类 Unix 系统上常见的数据压缩库。它已封装在 [`libz-sys` crate] 中，但此示例我们将做极度简化版本。完整示例见[源代码][libz-source]。

为便于查找库位置，我们将使用 [`pkg-config` crate]。该 crate 使用系统的 `pkg-config` 工具发现库信息，并自动告诉 Cargo 链接库所需的内容。这很可能仅在安装了 `pkg-config` 的类 Unix 系统上有效。先从设置 manifest 开始：

```toml
# Cargo.toml
[package]
name = "libz-sys"
version = "0.1.0"
edition = "2024"
links = "z"

[build-dependencies]
pkg-config = "0.3.16"
```

注意，我们在 `package` 表中包含了 `links` 键。这告诉 Cargo 我们链接到 `libz` 库。见[「使用另一个 sys crate」](#using-another-sys-crate) 了解将利用此设置的示例。

构建脚本相当简单：

```rust,ignore
// build.rs

fn main() {
    pkg_config::Config::new().probe("zlib").unwrap();
    println!("cargo::rerun-if-changed=build.rs");
}
```

用一个基本 FFI 绑定完善示例：

```rust,ignore
// src/lib.rs

use std::os::raw::{c_uint, c_ulong};

unsafe extern "C" {
    pub fn crc32(crc: c_ulong, buf: *const u8, len: c_uint) -> c_ulong;
}

#[test]
fn test_crc32() {
    let s = "hello";
    unsafe {
        assert_eq!(crc32(0, s.as_ptr(), s.len() as c_uint), 0x3610a686);
    }
}
```

运行 `cargo build -vv` 查看构建脚本输出。在已安装 `libz` 的系统上，可能类似：

```text
[libz-sys 0.1.0] cargo::rustc-link-search=native=/usr/lib
[libz-sys 0.1.0] cargo::rustc-link-lib=z
[libz-sys 0.1.0] cargo::rerun-if-changed=build.rs
```

很好！`pkg-config` 完成了查找库并告诉 Cargo 其位置的全部工作。

包包含库源码并在系统上找不到时静态构建，或设置了特性或环境变量时静态构建，这并不罕见。例如，真正的 [`libz-sys` crate] 检查环境变量 `LIBZ_SYS_STATIC` 或 `static` 特性，从源码构建而非使用系统库。更完整示例见[源代码][libz-source]。

[`libz-sys` crate]: https://crates.io/crates/libz-sys
[`pkg-config` crate]: https://crates.io/crates/pkg-config
[libz-source]: https://github.com/rust-lang/libz-sys

## 使用另一个 `sys` crate {#using-another-sys-crate}

使用 `links` 键时，crate 可设置其他依赖它的 crate 可读取的元数据。这提供了 crate 之间通信信息的机制。此示例中，我们将创建一个使用真正的 [`libz-sys` crate] 中 zlib 的 C 库。

若 C 库依赖 zlib，可利用 [`libz-sys` crate] 自动查找或构建它。这对跨平台支持（如通常未安装 zlib 的 Windows）很有帮助。`libz-sys` [设置 `include` 元数据](https://github.com/rust-lang/libz-sys/blob/3c594e677c79584500da673f918c4d2101ac97a1/build.rs#L156)，告诉其他包 zlib 头文件的位置。我们的构建脚本可通过 `DEP_Z_INCLUDE` 环境变量读取该元数据。示例如下：

```toml
# Cargo.toml
[package]
name = "z_user"
version = "0.1.0"
edition = "2024"

[dependencies]
libz-sys = "1.0.25"

[build-dependencies]
cc = "1.0.46"
```

此处包含了 `libz-sys`，确保最终库中只使用一个 `libz`，并从构建脚本访问它：

```rust,ignore
// build.rs

fn main() {
    let mut cfg = cc::Build::new();
    cfg.file("src/z_user.c");
    if let Some(include) = std::env::var_os("DEP_Z_INCLUDE") {
        cfg.include(include);
    }
    cfg.compile("z_user");
    println!("cargo::rerun-if-changed=src/z_user.c");
}
```

`libz-sys` 完成所有繁重工作后，C 源码现在可包含 zlib 头文件，即使系统上尚未安装也应能找到头文件。

```c
// src/z_user.c

#include "zlib.h"

// … 使用 zlib 的其余代码。
```

## 读取目标配置 {#reading-target-configuration}
当构建脚本需要根据目标平台做决策时，应读取 `CARGO_CFG_*` 环境变量，而不是使用 `cfg!` 或 `#[cfg]` 属性。这是因为构建脚本为*主机*机器编译并运行，而 `CARGO_CFG_*` 变量反映*目标*平台，交叉编译时这一区别很重要。

```rust,ignore
// build.rs

fn main() {
    // 读取 TARGET 配置
    let target_os = std::env::var("CARGO_CFG_TARGET_OS").unwrap();

    if target_os == "windows" {
        println!("cargo::rustc-link-lib=userenv");
    } else if target_os == "linux" {
        println!("cargo::rustc-link-lib=pthread");
    }
}
```

注意，某些配置值可能包含以逗号分隔的多个值（例如 `CARGO_CFG_TARGET_FAMILY` 可能是 `unix,wasm`）。检查这些值时，请适当处理。

若要更方便的类型化 API，考虑使用 [`build-rs`] crate，它会为你处理这些细节。

[`build-rs`]: https://crates.io/crates/build-rs

## 条件编译 {#conditional-compilation}

构建脚本可输出 [`rustc-cfg` 指令][`rustc-cfg` instructions]，启用可在编译时检查的条件。此示例中，我们看 [`openssl` crate] 如何用此支持 OpenSSL 库的多个版本。

[`openssl-sys` crate] 实现 OpenSSL 库的构建和链接。它支持多种不同实现（如 LibreSSL）和多个版本。它使用 `links` 键向其他构建脚本传递信息。传递的内容之一是 `version_number` 键，即检测到的 OpenSSL 版本。构建脚本中的代码大致[如下](https://github.com/sfackler/rust-openssl/blob/dc72a8e2c429e46c275e528b61a733a66e7877fc/openssl-sys/build/main.rs#L216)：

```rust,ignore
println!("cargo::metadata=version_number={openssl_version:x}");
```

此指令使直接依赖 `openssl-sys` 的任何 crate 中设置 `DEP_OPENSSL_VERSION_NUMBER` 环境变量。

提供高层接口的 `openssl` crate 将 `openssl-sys` 指定为依赖。`openssl` 构建脚本可通过 `DEP_OPENSSL_VERSION_NUMBER` 环境变量读取 `openssl-sys` 构建脚本生成的版本信息，并用此生成一些 [`cfg` 值](https://github.com/sfackler/rust-openssl/blob/dc72a8e2c429e46c275e528b61a733a66e7877fc/openssl/build.rs#L18-L36)：

```rust,ignore
// （build.rs 片段）

println!("cargo::rustc-check-cfg=cfg(ossl101,ossl102)");
println!("cargo::rustc-check-cfg=cfg(ossl110,ossl110g,ossl111)");

if let Ok(version) = env::var("DEP_OPENSSL_VERSION_NUMBER") {
    let version = u64::from_str_radix(&version, 16).unwrap();

    if version >= 0x1_00_01_00_0 {
        println!("cargo::rustc-cfg=ossl101");
    }
    if version >= 0x1_00_02_00_0 {
        println!("cargo::rustc-cfg=ossl102");
    }
    if version >= 0x1_01_00_00_0 {
        println!("cargo::rustc-cfg=ossl110");
    }
    if version >= 0x1_01_00_07_0 {
        println!("cargo::rustc-cfg=ossl110g");
    }
    if version >= 0x1_01_01_00_0 {
        println!("cargo::rustc-cfg=ossl111");
    }
}
```

这些 `cfg` 值可与 [`cfg` 属性][`cfg` attribute] 或 [`cfg` 宏][`cfg` macro] 配合使用，以条件包含代码。例如，SHA3 支持在 OpenSSL 1.1.1 中添加，因此对旧版本[条件排除](https://github.com/sfackler/rust-openssl/blob/dc72a8e2c429e46c275e528b61a733a66e7877fc/openssl/src/hash.rs#L67-L85)：

```rust,ignore
// （openssl crate 片段）

#[cfg(ossl111)]
pub fn sha3_224() -> MessageDigest {
    unsafe { MessageDigest(ffi::EVP_sha3_224()) }
}
```

当然，使用此方法时应谨慎，因为它使生成的二进制文件更依赖构建环境。此示例中，若二进制文件分发到其他系统，可能没有完全相同的共享库，可能导致问题。

[`cfg` attribute]: https://doc.rust-lang.org/reference/conditional-compilation.html#the-cfg-attribute
[`cfg` macro]: https://doc.rust-lang.org/std/macro.cfg.html
[`rustc-cfg` instructions]: ../../#rustc-cfg
[`openssl` crate]: https://crates.io/crates/openssl
[`openssl-sys` crate]: https://crates.io/crates/openssl-sys

[crates.io]: https://crates.io/
