+++
title = "01-Features 示例"
date = 2026-07-30T14:49:00+08:00
weight = 40
type = "docs"
description = "features 的常见用法示例"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Features 示例 {#features-examples}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/features-examples.html](https://doc.rust-lang.org/cargo/reference/features-examples.html)


以下展示一些实际使用中的特性示例。

## 最小化构建时间与文件大小 {#minimizing-build-times-and-file-sizes}
一些包使用特性，以便在特性未启用时减小 crate 大小并缩短编译时间。一些示例是：

* [`syn`] 是用于解析 Rust 代码的流行 crate。由于它如此流行，缩短编译时间很有帮助，因为它影响许多项目。它有一份[文档清晰的特性列表][syn-features]，可用于最小化其包含的代码量。
* [`regex`] 有[若干特性][regex-features]，且[文档完善][regex-docs]。去掉 Unicode 支持可以减小最终文件大小，因为它可以移除一些大型表。
* [`winapi`] 有[大量][winapi-features]特性，用于限制它所支持的 Windows API 绑定。
* [`web-sys`] 是另一个与 `winapi` 类似的示例，它提供由特性限制的[巨大 API 绑定表面积][web-sys-features]。

[`winapi`]: https://crates.io/crates/winapi
[winapi-features]: https://github.com/retep998/winapi-rs/blob/0.3.9/Cargo.toml#L25-L431
[`regex`]: https://crates.io/crates/regex
[`syn`]: https://crates.io/crates/syn
[syn-features]: https://docs.rs/syn/1.0.54/syn/#optional-features
[regex-features]: https://github.com/rust-lang/regex/blob/1.4.2/Cargo.toml#L33-L101
[regex-docs]: https://docs.rs/regex/1.4.2/regex/#crate-features
[`web-sys`]: https://crates.io/crates/web-sys
[web-sys-features]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/crates/web-sys/Cargo.toml#L32-L1395

## 扩展行为 {#extending-behavior}
[`serde_json`] 包有一个 [`preserve_order` 特性][serde_json-preserve_order]，它[改变][serde_json-code] JSON map 的行为以保留键的插入顺序。注意它启用可选依赖 [`indexmap`] 以实现新行为。

像这样改变行为时，务必确保变更是 [SemVer 兼容][SemVer compatible]的。也就是说，启用该特性不应破坏通常在关闭该特性时能构建的代码。

[`serde_json`]: https://crates.io/crates/serde_json
[serde_json-preserve_order]: https://github.com/serde-rs/json/blob/v1.0.60/Cargo.toml#L53-L56
[SemVer compatible]: ../../#semver-compatibility
[serde_json-code]: https://github.com/serde-rs/json/blob/v1.0.60/src/map.rs#L23-L26
[`indexmap`]: https://crates.io/crates/indexmap

## `no_std` 支持 {#no_std-support}
一些包希望同时支持 [`no_std`] 与 `std` 环境。这对于支持嵌入式与资源受限平台很有用，同时仍允许支持完整标准库的平台使用扩展能力。

[`wasm-bindgen`] 包定义了一个默认[启用][wasm-bindgen-default]的 [`std` 特性][wasm-bindgen-std]。在库的顶部，它[无条件启用 `no_std` 属性][wasm-bindgen-no_std]。这确保 `std` 与 [`std` prelude] 不会自动进入作用域。然后，在代码的各处（[示例1][wasm-bindgen-cfg1]、[示例2][wasm-bindgen-cfg2]），它使用 `#[cfg(feature = "std")]` 属性有条件地启用需要 `std` 的额外功能。

[`no_std`]: https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute
[`wasm-bindgen`]: https://crates.io/crates/wasm-bindgen
[`std` prelude]: https://doc.rust-lang.org/std/prelude/index.html
[wasm-bindgen-std]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/Cargo.toml#L25
[wasm-bindgen-default]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/Cargo.toml#L23
[wasm-bindgen-no_std]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/src/lib.rs#L8
[wasm-bindgen-cfg1]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/src/lib.rs#L270-L273
[wasm-bindgen-cfg2]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/src/lib.rs#L67-L75

## 重新导出依赖特性 {#re-exporting-dependency-features}
重新导出依赖的特性可能很方便。这允许依赖该 crate 的用户控制这些特性，而无需直接指定那些依赖。例如，[`regex`] [重新导出][regex-re-export]来自 [`regex_syntax`][regex_syntax-features] 包的特性。`regex` 的用户无需了解 `regex_syntax` 包，但他们仍可访问它所包含的特性。

[regex-re-export]: https://github.com/rust-lang/regex/blob/1.4.2/Cargo.toml#L65-L89
[regex_syntax-features]: https://github.com/rust-lang/regex/blob/1.4.2/regex-syntax/Cargo.toml#L17-L32

## 供应商化 C 库 {#vendoring-of-c-libraries}
一些包提供对常见 C 库的绑定（有时称为 ["sys" crate][sys]）。有时这些包让你选择使用系统上已安装的 C 库，或从源码构建它。例如，[`openssl`] 包有一个 [`vendored` 特性][openssl-vendored]，它启用 [`openssl-sys`] 的对应 `vendored` 特性。`openssl-sys` 构建脚本有一些[条件逻辑][openssl-sys-cfg]，使其从本地 OpenSSL 源码副本构建，而不是使用系统版本。

[`curl-sys`] 包是另一个示例，其中 [`static-curl` 特性][curl-sys-static]使其从源码构建 libcurl。注意它还有一个 [`force-system-lib-on-osx`][curl-sys-macos] 特性，强制它[使用系统 libcurl][curl-sys-macos-code]，覆盖 static-curl 设置。

[`openssl`]: https://crates.io/crates/openssl
[`openssl-sys`]: https://crates.io/crates/openssl-sys
[sys]: ../../build-scripts/#-sys-packages
[openssl-vendored]: https://github.com/sfackler/rust-openssl/blob/openssl-v0.10.31/openssl/Cargo.toml#L19
[build script]: ../../build-scripts/
[openssl-sys-cfg]: https://github.com/sfackler/rust-openssl/blob/openssl-v0.10.31/openssl-sys/build/main.rs#L47-L54
[`curl-sys`]: https://crates.io/crates/curl-sys
[curl-sys-static]: https://github.com/alexcrichton/curl-rust/blob/0.4.34/curl-sys/Cargo.toml#L49
[curl-sys-macos]: https://github.com/alexcrichton/curl-rust/blob/0.4.34/curl-sys/Cargo.toml#L52
[curl-sys-macos-code]: https://github.com/alexcrichton/curl-rust/blob/0.4.34/curl-sys/build.rs#L15-L20

## 特性优先级 {#feature-precedence}
一些包可能有互斥的特性。处理这一点的一种选项是优先使用某个特性而非另一个。[`log`] 包是一个示例。它有[若干特性][log-features]用于在编译时选择最大日志级别，在[此处][log-docs]有描述。它使用 [`cfg-if`] 来[选择优先级][log-cfg-if]。若启用多个特性，较高的「max」级别将优先于较低级别。

[`log`]: https://crates.io/crates/log
[log-features]: https://github.com/rust-lang/log/blob/0.4.11/Cargo.toml#L29-L42
[log-docs]: https://docs.rs/log/0.4.11/log/#compile-time-filters
[log-cfg-if]: https://github.com/rust-lang/log/blob/0.4.11/src/lib.rs#L1422-L1448
[`cfg-if`]: https://crates.io/crates/cfg-if

## Proc-macro 配套包 {#proc-macro-companion-package}
一些包有与之紧密关联的 proc-macro。然而，并非所有用户都需要使用该 proc-macro。通过将 proc-macro 设为可选依赖，你可以方便地选择是否包含它。这很有帮助，因为有时 proc-macro 版本必须与父包保持同步，而你不希望强迫用户必须指定两个依赖并保持它们同步。

一个示例是 [`serde`]，它有一个启用 [`serde_derive`] proc-macro 的 [`derive`][serde-derive] 特性。`serde_derive` crate 与 `serde` 非常紧密地绑定，因此它使用[等于版本需求][serde-equals]以确保它们保持同步。

[`serde`]: https://crates.io/crates/serde
[`serde_derive`]: https://crates.io/crates/serde_derive
[serde-derive]: https://github.com/serde-rs/serde/blob/v1.0.118/serde/Cargo.toml#L34-L35
[serde-equals]: https://github.com/serde-rs/serde/blob/v1.0.118/serde/Cargo.toml#L17

## 仅 Nightly 特性 {#nightly-only-features}
一些包希望试验仅在 Rust [nightly 通道][nightly channel]上可用的 API 或语言特性。然而，它们可能不希望也要求用户使用 nightly 通道。一个示例是 [`wasm-bindgen`]，它有一个 [`nightly` 特性][wasm-bindgen-nightly]，启用使用撰写本文时仅在 nightly 通道上可用的 [`Unsize`] 标记 trait 的[扩展 API][wasm-bindgen-unsize]。

注意在 crate 根处它使用 [`cfg_attr` 启用 nightly 特性][wasm-bindgen-cfg_attr]。请记住 [`feature` 属性][`feature` attribute] 与 Cargo 特性无关，用于选择加入实验性语言特性。

[`rand`] 包的 [`simd_support` 特性][rand-simd_support]是另一个示例，它依赖一个仅在 nightly 通道上构建的依赖。

[`wasm-bindgen`]: https://crates.io/crates/wasm-bindgen
[nightly channel]: https://doc.rust-lang.org/book/appendix-07-nightly-rust.html
[wasm-bindgen-nightly]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/Cargo.toml#L27
[wasm-bindgen-unsize]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/src/closure.rs#L257-L269
[`Unsize`]: https://doc.rust-lang.org/std/marker/trait.Unsize.html
[wasm-bindgen-cfg_attr]: https://github.com/rustwasm/wasm-bindgen/blob/0.2.69/src/lib.rs#L11
[`feature` attribute]: https://doc.rust-lang.org/unstable-book/index.html
[`rand`]: https://crates.io/crates/rand
[rand-simd_support]: https://github.com/rust-random/rand/blob/0.7.3/Cargo.toml#L40

## 实验性特性 {#experimental-features}
一些包有它们可能希望试验的新功能，而不必承诺这些 API 的稳定性。这些特性通常会文档说明它们是实验性的，因此即使在次版本发布中，将来也可能更改或破坏。一个示例是 [`async-std`] 包，它有一个 [`unstable` 特性][async-std-unstable]，它[门控新 API][async-std-gate]，人们可以选择加入使用，但可能尚未完全准备好被依赖。

[`async-std`]: https://crates.io/crates/async-std
[async-std-unstable]: https://github.com/async-rs/async-std/blob/v1.8.0/Cargo.toml#L38-L42
[async-std-gate]: https://github.com/async-rs/async-std/blob/v1.8.0/src/macros.rs#L46
