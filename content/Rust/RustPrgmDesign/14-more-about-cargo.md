+++
title = "14-进一步认识Cargo和Crates.io"
date = 2026-07-28T14:49:00+08:00
weight = 140
type = "docs"
description = "发布配置、crates.io 发布、工作空间与 cargo 扩展精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第14章

# 进一步认识 Cargo 和 Crates.io

本章：发布配置 → 发布 crate → 工作空间 → 安装二进制 → 扩展 Cargo。

## 采用发布配置自定义构建

- **发布配置**（release profiles）：预定义的可定制编译选项集。
- 两个主要配置：
  - `dev` — `cargo build`（开发，编译快）
  - `release` — `cargo build --release`（发布，运行快）

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

- `opt-level` 0–3：越高优化越多，编译越慢。覆盖默认值只需在 `Cargo.toml` 添加 `[profile.*]` 段。

## 将 crate 发布到 Crates.io

### 编写有用的文档注释

- `///` — 为**后面**的项写文档（函数、结构体等）。
- `//!` — 为**包含它的项**写文档（crate 根、模块）。
- `cargo doc` / `cargo doc --open` 生成 HTML 文档。
- 常用章节：`# Examples`、`# Panics`、`# Errors`、`# Safety`。
- 文档中的示例代码会被 `cargo test` 作为**文档测试**运行。

### 导出实用的公有 API

- `pub use` **重导出**：内部结构不变，对外呈现扁平 API。

```rust
pub use self::kinds::PrimaryColor;
pub use self::utils::mix;
// 用户可 use art::PrimaryColor 而非 art::kinds::PrimaryColor
```

### 创建 Crates.io 账号

```console
cargo login
# 粘贴 API token（秘密，存 ~/.cargo/credentials）
```

### 向新 crate 添加元数据

```toml
[package]
name = "guessing_game"   # crates.io 先到先得
version = "0.1.0"
description = "A fun game..."
license = "MIT OR Apache-2.0"  # SPDX 标识符
```

- 必填：`description`、`license`（或 `license-file`）。

### 发布到 Crates.io

```console
cargo publish
```

- 发布**永久性**：版本不可覆盖/删除。遵循[语义化版本](https://semver.org/)。

### 发布现有 crate 的新版本

- 修改 `version`，再 `cargo publish`。

### 使用 `cargo yank` 从 Crates.io 撤回版本

```console
cargo yank --vers 1.0.1
cargo yank --vers 1.0.1 --undo
```

- yank 阻止**新**项目依赖该版本；已有 `Cargo.lock` 的项目不受影响。不删除代码。

## Cargo 工作空间

- **工作空间**：共享一个 `Cargo.lock` 和 `target/` 的多个包。

```toml
# 顶层 Cargo.toml
[workspace]
resolver = "3"
members = ["adder", "add_one"]
```

- 在工作空间内 `cargo new` 自动加入 `members`。
- 成员间依赖需**显式声明**路径依赖；Cargo 不自动假设成员互相依赖。
- 顶层唯一 `Cargo.lock` — 所有 crate 使用相同依赖版本。
- 某 crate 用了 `rand`，其他 crate 不能直接用，须各自声明依赖。
- 运行/测试/发布指定成员：`cargo run -p adder`、`cargo test -p add_one`。

## 使用 `cargo install` 安装二进制文件

```console
cargo install ripgrep
# 安装到 ~/.cargo/bin/（需加入 PATH）
```

- 仅安装含**二进制目标**（`src/main.rs`）的 crate，非库 crate。

## 使用自定义命令扩展 Cargo

- `$PATH` 中有 `cargo-something` 二进制 → 可用 `cargo something` 运行。
- `cargo --list` 显示所有可用子命令（含自定义）。
- 可用 `cargo install` 安装扩展命令。

## 总结

Cargo + crates.io 是 Rust 生态核心：分享代码、组织大项目、安装工具。
