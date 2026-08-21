+++
title = "04-构建"
date = 2026-08-18T18:10:00+08:00
weight = 40
type = "docs"
description = "构建 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/libs/building/index.html](https://microsoft.github.io/rust-guidelines/guidelines/libs/building/index.html)

# 构建

## 库开箱即用 (M-OOBE) {#M-OOBE}

*本条守护：在整个 Rust 生态中易于采用。*

库必须在所有受支持平台上*开箱即用*，明确声明为平台或目标特定的库除外。

Rust crate 常常带有几十个依赖，应用则有上百个。用户期望 `cargo build` 和 `cargo install` *直接能用*。看看安装 `bat` 时拉入约 250 个依赖的情形：

```text
Compiling writeable v0.5.5
Compiling strsim v0.11.1
Compiling litemap v0.7.5
Compiling crossbeam-utils v0.8.21
Compiling icu_properties_data v1.5.1
Compiling ident_case v1.0.1
Compiling once_cell v1.21.3
Compiling icu_normalizer_data v1.5.1
Compiling fnv v1.0.7
Compiling regex-syntax v0.8.5
Compiling anstyle v1.0.10
Compiling vcpkg v0.2.15
Compiling utf8parse v0.2.2
Compiling aho-corasick v1.1.3
Compiling utf16_iter v1.0.5
Compiling hashbrown v0.15.2
Building [==>                       ] 29/251: icu_locid_transform_data, serde, winnow, indexma...
```

这次编译，与几乎所有其他应用和库一样，会*直接能用*。

虽然有面向特定功能的工具（例如 Wayland compositor）或像 `windows` 这样的平台 crate；除非一个 crate *明显*是平台特定的，否则人们期望它在其他方面*开箱即用*。

这意味着 crate 最终必须能构建于

- [ ] 所有 [Tier 1 platforms](https://doc.rust-lang.org/rustc/platform-support.html)，<sup>1</sup> 以及
- [ ] 除 `cargo` 和 `rust` 之外无需任何额外前提。<sup>2</sup>

> <sup>1</sup> 暂时不支持 [Tier 1 platforms](https://doc.rust-lang.org/rustc/platform-support.html) 可以接受，但必须已有抽象以便日后轻松扩展。通常通过引入内部 `HAL`（[Hardware Abstraction Layer](https://en.wikipedia.org/wiki/HAL_(software))）模块并配备 `dummy` 回退目标来完成。<br/>
> <sup>2</sup> 默认的 Rust 安装也会带有 `cc` 和链接器。

尤其是，非平台 crate 默认不得要求用户安装额外工具，或指望环境变量才能编译。若工具确实需要（例如从 `.proto` 文件生成 Rust），这些工具应作为发布工作流或更早步骤的一部分运行，生成的产物（例如 `.rs` 文件）应包含在已发布的 crate 内。

若某依赖已知是平台特定的，父级必须使用条件（平台）编译或可选的 feature 门控。

> **⚠️  库要为自己的依赖负责。**
>
> 设想你编写一个 `Copilot` crate，它又使用 `HttpClient`，而后者依赖一个 `perl` 脚本才能编译。
>
> 那么你的每一个用户、用户的用户、以及再往上的每一个人，都需要安装 Perl 才能编译*他们的* crate。在大型项目中，会有上百个既不了解也不关心你的库或 Perl 的人，碰到一条晦涩的编译错误，然后不得不搞清楚如何在自己的系统上安装它。
>
> 实际上，这种行为在开源领域很大程度上是自我判处的死刑，因为一旦有替代品可用，人们就会转向那些*开箱即用*的方案。

## 原生 `-sys` crate 无需额外依赖即可编译 (M-SYS-CRATES) {#M-SYS-CRATES}

*本条守护：在所有平台上开箱即用的库。*

若你编写一对 `foo` 与 `foo-sys` crate 来包装原生 `foo.lib`，你很可能会遇到 [M-OOBE] 中描述的问题。

按以下步骤制作一个跨平台*开箱即用*的 crate：

- [ ] 在 `foo-sys` 内部的 `build.rs` 中完全掌控 `foo.lib` 的构建。只通过 [cc](https://crates.io/crates/cc) crate 手写编译，*不要*运行 Makefile 或外部构建脚本，因为那会要求安装外部依赖，
- [ ] 让所有外部工具可选，例如 `nasm`，
- [ ] 把上游源码嵌入你的 crate，
- [ ] 使嵌入的源码可验证（例如包含 Git URL + hash），
- [ ] 若可能，预先生成 `bindgen` 胶水，
- [ ] 同时支持静态链接，以及经由 [libloading](https://crates.io/crates/libloading) 的动态链接。

偏离以上几点也可以行得通，可按个案考虑：

若原生构建系统本身作为*开箱即用* crate 可用，则可用它替代 `cc` 调用。外部工具同理。

若源码超出 crates.io 体积限制，可能必须下载。无论如何，只应使用可用性可与 crates.io 相比的服务器。此外，可接受下载的特定 hash 应存放在 crate 中并加以验证。

下载源码可能在隔离构建环境中失败，因此还应能指定备用源码根（例如通过环境变量）。

[M-OOBE]: ./#M-OOBE

## Feature 是可叠加的 (M-FEATURES-ADDITIVE) {#M-FEATURES-ADDITIVE}

*本条守护：大型复杂项目中可靠的编译。*

所有库 feature 必须可叠加，且任意组合都必须能工作，只要该 feature 本身能在当前平台上工作。这意味着：

- [ ] 不得引入 `no-std` feature，应改用 `std` feature
- [ ] 添加任何 feature `foo` 都不得禁用或修改任何公开项
  - 若这些 enum 是 `#[non_exhaustive]`，添加变体可以
- [ ] Feature 不得依赖其他 feature 被手动启用
- [ ] Feature 不得依赖其父级去 skip-enable 某个子依赖中的 feature

延伸阅读

- [Feature Unification](https://doc.rust-lang.org/cargo/reference/features.html#feature-unification)
- [Mutually Exclusive Features](https://doc.rust-lang.org/cargo/reference/features.html#mutually-exclusive-features)
