+++
title = "03-韧性"
date = 2026-08-18T18:10:00+08:00
weight = 30
type = "docs"
description = "韧性 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/libs/resilience/index.html](https://microsoft.github.io/rust-guidelines/guidelines/libs/resilience/index.html)

# 韧性

## I/O 与系统调用可被 mock (M-MOCKABLE-SYSCALLS) {#M-MOCKABLE-SYSCALLS}

*本条守护：否则难以触发的边界情况也可测试。*

任何面向用户、会做 I/O 或带副作用的系统调用的类型，都应能 mock 这些副作用。这包括文件和网络访问、时钟、熵源与种子，以及类似事物。更一般地说，任何满足以下条件的操作都应当可被 mock：

- 非确定性的，
- 依赖外部状态的，
- 依赖硬件或环境的，
- 本身脆弱或无法普遍复现的

> ### 💡  要 mock 分配吗？
>
> 除非你在写内核或类似代码，否则可以把分配视为确定性、与硬件无关、且实际上不会失败，因而本指南并不覆盖它。
>
> 不过，这*并不*意味着你应假定内存无限可用。若你的库内存复杂度*合理*，原样接受调用方提供的输入是可以的；但贪吃内存的库、以及处理外部输入的代码，应提供有界和/或分块操作。

本指南对库有若干含义，它们

- 不应做临时 I/O，例如调用 `read("foo.txt")`
- 不应依赖无法 mock 的 I/O 与系统调用
- 不应自己再造一套 I/O 或系统调用 *core*
- 不应提供 `MyIoLibrary::default()` 构造函数

相反，执行 I/O 与系统调用的库，要么应接受某个已经可 mock 的 I/O *core*，要么自己提供 mock 功能：

```rust
let lib = Library::new_runtime(runtime_io); // 传入已可 mock 的 I/O 功能
let (lib, mock) = Library::new_mocked(); // 支持内建 mock
```

支持内建 mock 的库应按如下方式实现：

```rust
pub struct Library {
    some_core: LibraryCore // 封装 syscall、I/O 等，见下文。
}

impl Library {
    pub fn new() -> Self { ... }
    pub fn new_mocked() -> (Self, MockCtrl) { ... }
}
```

在幕后，`LibraryCore` 是一个非公开 enum，类似于 [M-RUNTIME-ABSTRACTED]，要么把调用分派到相应系统调用，要么分派到 mock 控制器。

```rust
// 将调用分派到操作系统，或分派到 mock 控制器。
enum LibraryCore {
    Native,

    #[cfg(feature = "test-util")]
    Mocked(mock::MockCtrl)
}

impl LibraryCore {
    // 你会转发给操作系统的某个函数。
    fn random_u32(&self) {
        match self {
            Self::Native => unsafe { os_random_u32() }
            Self::Mocked(m) => m.random_u32()
        }
    }
}

#[cfg(feature = "test-util")]
mod mock {
    // 遵循 M-SERVICES-CLONE 模式，因此 `LibraryCore` 与
    // 用户都能持有同一 `MockCtrl` 实例。
    pub struct MockCtrl {
        inner: Arc<MockCtrlInner>
    }

    // 按需实现相应逻辑，通常转发给下面的
    // `MockCtrlInner`。
    impl MockCtrl {
        pub fn set_next_u32(&self, x: u32) { ... }
        pub fn random_u32(&self) { ... }
    }

    // 包含实际逻辑，例如下次应返回的随机数。
    struct MockCtrlInner {
        next_call: u32
    }
}
```

已经建立在 [M-RUNTIME-ABSTRACTED] 模式之上的运行时感知库，应扩展其运行时 enum：

```rust
enum Runtime {
    #[cfg(feature="tokio")]
    Tokio(tokio::Tokio),

    #[cfg(feature="smol")]
    Smol(smol::Smol)

    #[cfg(feature="test-util")]
    Mock(mock::MockCtrl)
}
```

如上所示，大多数支持 mock 的库不应接受 mock 控制器，而应通过参数元组返回它们：第一个参数是库实例，第二个是 mock 控制器。这是为了防止多个实例共享同一个控制器时出现状态歧义：

```rust
impl Library {
    pub fn new_mocked() -> (Self, MockCtrl) { ... } // 好
    pub fn new_mocked_bad(&mut MockCtrl) -> Self { ... } // 容易误用
}
```

[M-RUNTIME-ABSTRACTED]: 02-ux/#M-RUNTIME-ABSTRACTED

## 测试工具用 feature 门控 (M-TEST-UTIL) {#M-TEST-UTIL}

*本条守护：生产构建无法绕过安全检查。*

测试功能必须置于 feature 标志之后。这包括

- mock 功能（[M-MOCKABLE-SYSCALLS]），
- 检查敏感数据的能力，
- 安全检查覆盖，
- 假数据生成。

我们建议你只用一个标志，名为 `test-util`。无论怎样，该 feature（或多个 feature）必须清楚表明它们仅供测试使用。

```rust
impl HttpClient {
    pub fn get() { ... }

    #[cfg(feature = "test-util")]
    pub fn bypass_certificate_checks() { ... }
}
```

[M-MOCKABLE-SYSCALLS]: ./#M-MOCKABLE-SYSCALLS

## 集成测试放在 `tests/` 下 (M-INTEGRATION-TESTS) {#M-INTEGRATION-TESTS}

*本条守护：干净的代码文件。*

只触及公开 API 表面的测试是*集成测试*，应放在 `tests/` 下，而不是 `mod tests {}`。

在有覆盖率目标的项目中，`src/` 文件里的测试代码多于实际业务逻辑并不少见。这会让 IDE 和 PR 中浏览、理解代码更困难。同样，若某个测试目标既可通过集成测试也可通过单元测试达成，则始终优先前者。

## 使用合适的类型族 (M-STRONG-TYPES) {#M-STRONG-TYPES}

*本条守护：在恰当的时机使用正确的数据与安全不变量。*

为任务使用合适的 `std` 类型。一般来说应尽早使用可用的最强类型。常见问题包括

| 不要用…… | 而应使用…… | 说明 |
| --- | --- | --- |
| `String`* | `PathBuf`* | 凡与操作系统打交道的都应是 `Path` 一类 |

话虽如此，你也应遵循常见的 Rust `std` 惯例。公开 API 边界上的纯数值类型（例如 `window_size()`）预期是普通数字，而不是 `Saturating<usize>`、`NonZero<usize>` 或类似类型。

> <sup>*</sup> 包括它们的兄弟，例如 `&str`、`Path` 等。

## Newtype 守护不变量 (M-STRONG-TYPES-GUARD) {#M-STRONG-TYPES-GUARD}

*本条守护：集中的正确性不变量。*

当引入用于编码不变量的强类型或 newtype 时（非空字符串、百分比、端口号、已消毒路径……），该类型本身必须在适用处强制该不变量。

构造应当可失败：当无法维持不变量时返回恰当的错误，而不是把责任甩给每一个用户：

```rust
// 不好：创建了新类型却什么也不强制。每个调用方现在都得
// 再检查该值是否真是有效月份，专用类型的意义就没了。
pub struct Month(pub u8);

impl Month {
    pub fn new(value: u8) -> Self { ... }
}

// 好：不变量 (1..=12) 在边界处检查一次，
// 之后每次使用 `Month` 都可以依赖它。
pub struct Month(u8);

impl Month {
    pub fn from_u8(value: u8) -> Result<Self, DateError> { ... }
}
```

这意味着，对任何非全域的 newtype：

- 它必须至少有一个可失败的构造函数（例如 `fn from_foo(...) -> Result<Self, _>`）。
- 允许额外的会 panic 的构造函数（例如 `new`），且最好是 `const`。
- 从更弱类型转换到该 newtype 必须可失败（`TryFrom`/`FromStr`）。
- 不得提供永真的 `From` 实现。

> ### 💡  为什么用 `const`？
>
> 常量化构造函数使它们能用在 `const {}` 块中，从而将这些违规表现为错误。这让用户可以写 `let month_due = const { Month::new(14) }`，避免在运行时才撞上这些路径。

## Builder 在最终 `.build()` 中校验 (M-BUILD-RESULT) {#M-BUILD-RESULT}

*本条守护：干净的 Builder 错误处理。*

Builder 的逐字段 setter 应接受输入而不失败，最终校验应由 `.build()` 完成。

可失败的 setter 会增加噪音，而且仍无法防范相互依赖的错误条件。当 Builder 可失败时，应改为提供携带 `Result` 的 `.build()`。

```rust
// 不好：迫使反复做毫无价值的错误检查。
Foo::builder()
    .name("Foo")?
    .distance(42)?
    .build();

// 好：把合理性检查集中起来，并允许在属性之间交叉校验。
Foo::builder()
    .name("Foo")
    .distance(42)
    .build()?;
```

话虽如此，各个设置在适用时应优先使用自带校验的强类型，参见 M-STRONG-TYPES-GUARD。

## 不要 glob 再导出项 (M-NO-GLOB-REEXPORTS) {#M-NO-GLOB-REEXPORTS}

*本条守护：刻意设计的公开表面。*

不要从其他模块 `pub use foo::*`，尤其不要从其他 crate。你可能意外导出超出预期的内容，而且 glob 在 PR 中很难审查。应改为逐项再导出：

```rust
pub use foo::{A, B, C};
```

出于技术原因，glob 导出是允许的，例如从一组 HAL（硬件抽象层）模块做平台特定再导出：

```rust
#[cfg(target_os = "windows")]
mod windows { /* ... */ }

#[cfg(target_os = "linux")]
mod linux { /* ... */ }

// glob 再导出的可接受用法：这是常见模式，
// 而且很清楚一切只是从单一平台转发而来。

#[cfg(target_os = "windows")]
pub use windows::*;

#[cfg(target_os = "linux")]
pub use linux::*;
```

## 避免静态量 (M-AVOID-STATICS) {#M-AVOID-STATICS}

*本条守护：跨 crate 版本的一致性与正确性。*

若某项的一致视图对正确性很重要，库应避免 `static` 和线程局部项。本质上，任何在该静态量*魔术般*变成另一个值就会不正确的代码，都不得使用它们。仅用于性能优化的静态量可以。

Rust 中静态量的根本问题是状态的隐秘复制。

考虑 crate `core` 中的如下函数：

```rust
# use std::sync::atomic::AtomicUsize;
# use std::sync::atomic::Ordering;
static GLOBAL_COUNTER: AtomicUsize = AtomicUsize::new(0);

pub fn increase_counter() -> usize {
    GLOBAL_COUNTER.fetch_add(1, Ordering::Relaxed)
}
```

现在假设你有 crate `main`，调用两个库 `library_a` 和 `library_b`，它们各自调用该计数器：

```rust
// 将全局静态计数器增加 2 次
library_a::count_up();
library_a::count_up();

// 再将全局静态计数器增加 3 次
library_b::count_up();
library_b::count_up();
library_b::count_up();
```

它们最终报告结果：

```rust
library_a::print_counter();
library_b::print_counter();
main::print_counter();
```

此时，该计数器*到底*是多少：`0`、`2`、`3` 还是 `5`？

答案是，以上任意一个都有可能（甚至同时多个！），取决于 crate 的版本解析！

在底层，Rust 可能链接同一 crate 的多个版本，并独立实例化，以满足已声明的依赖。这在 crate 的 `0.x` 版本时间线中尤其明显，其中每个 `x` 都构成一个独立的*主*版本。

若 `main`、`library_a` 和 `library_b` 都声明了同一版本的 `core`，例如 `0.5`，则报告结果将是 `5`，因为所有 crate 实际*看到*的是同一个 `GLOBAL_COUNTER`。

然而，若 `library_a` 声明的是 `0.4`，它就会链接到另一个版本的 `core`；于是 `main` 和 `library_b` 会在值 `3` 上达成一致，而 `library_a` 报告 `2`。

尽管 `static` 项可能有用，但在库稳定化之前尤其危险；对任何*隐秘复制*会在静态量与非静态变量交互时造成一致性问题的状态也是如此。此外，静态量会干扰单元测试，并且是每核一线程设计中的争用点。

## 生产代码使用遥测而非 println (M-LOG-NOT-PRINT) {#M-LOG-NOT-PRINT}

*本条守护：诊断信息出现在需要它的地方。*

生产代码路径应通过项目的遥测框架发出诊断，而不是经由 `println!` 或 `dbg!`。控制台输出留给那些有意把 stdout 当作用户界面的 CLI。
