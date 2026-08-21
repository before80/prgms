+++
title = "第4章 应用"
date = 2026-08-18T18:10:00+08:00
weight = 60
type = "docs"
description = "应用指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/apps/index.html](https://microsoft.github.io/rust-guidelines/guidelines/apps/index.html)

# 应用

## 应用使用 mimalloc (M-MIMALLOC-APPS) {#M-MIMALLOC-APPS}

*本条守护：零成本下的显著性能提升。*

应用应当将 [mimalloc](https://crates.io/crates/mimalloc) 设为全局分配器。这通常会沿分配热点路径带来明显的性能提升；我们见过高达 25% 的基准改进。

更换分配器只需几行代码。像这样将 mimalloc 加入你的 `Cargo.toml`：

```toml
[dependencies]
mimalloc = { version = "0.1" } # 或可用的更新版本
```

然后在 `main.rs` 中使用：

```rust
use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;
```

## 应用可以使用 Anyhow 或其衍生库 (M-APP-ERROR) {#M-APP-ERROR}

*本条守护：简洁的应用级错误处理。*

> 注意，本指南主要是对 [M-ERRORS-CANONICAL-STRUCTS] 的放宽与澄清。

应用，以及仓库中仅由你的应用使用的 crate，可以使用 [ohno::AppError](https://docs.rs/crate/ohno/latest#structs)、[anyhow](https://github.com/dtolnay/anyhow)、
[eyre](https://github.com/eyre-rs/eyre) 或类似的应用级错误 crate，而不必自行实现类型。

例如，在你的应用 crate 中，你可以仅重新导出并使用 eyre 的通用 `Result` 类型，它应当能自动
处理所有第三方库错误，尤其是遵循
[M-ERRORS-CANONICAL-STRUCTS] 的那些。

```rust
use ohno::AppError;

fn start_application() -> Result<(), AppError> {
    start_server()?;
    Ok(())
}
```

一旦选定应用错误 crate，就应当将所有应用级错误切换为该类型，且不应混用多种
应用级错误类型。

库（被多个 crate 使用的 crate）则应始终遵循 [M-ERRORS-CANONICAL-STRUCTS]。

[M-ERRORS-CANONICAL-STRUCTS]: ../libraries/02-ux/#M-ERRORS-CANONICAL-STRUCTS

## 应用面向可行的最高 target-cpu (M-TARGET-CPU) {#M-TARGET-CPU}

*本条守护：机群性能。*

服务端应用应当针对部署环境保证支持的最高 `target-cpu` 编译，而不是默认使用通用基线。

例如，可通过在 `.cargo/config.toml` 中设置实现：

```toml
[target.x86_64-unknown-linux-gnu]
rustflags = ["-C", "target-cpu=x86-64-v3"]

[target.x86_64-pc-windows-msvc]
rustflags = ["-C", "target-cpu=x86-64-v3"]

# 按需在此添加其他平台 ...
```

注意本指南仅适用于应用，因为库会忽略目标设置。
