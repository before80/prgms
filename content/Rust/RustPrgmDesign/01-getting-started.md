+++
title = "01-入门指南"
date = 2026-07-28T14:49:00+08:00
weight = 10
type = "docs"
description = "安装 Rust、Hello World 与 Cargo 构建系统的入门精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第1章

# 入门指南

本章目标：安装 Rust → 手写 Hello World → 用 Cargo 管理项目。

## 安装

- 推荐用 **rustup** 安装稳定版 Rust（Linux/macOS：`curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh`；Windows 见 [rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)）。
- 需要 **链接器**：macOS 用 `xcode-select --install`；Linux 装 GCC/Clang；Windows 安装 Visual Studio（MSVC）。
- 验证：`rustc --version`；Cargo 随 rustup 一并安装，`cargo --version`。
- 常用命令：`rustup update`（更新）、`rustup self uninstall`（卸载）、`rustup doc`（本地文档）。

### 故障排除（Troubleshooting）

`rustc --version` 失败时，检查 `%PATH%` / `$env:Path` / `$PATH` 是否包含 Rust 工具链目录。

### 本地文档

`rustup doc` 打开标准库 API 文档，离线可查类型与函数。

### 文本编辑器和集成开发环境（Integrated Development Environments, IDE）

任意编辑器均可；推荐支持 **rust-analyzer** 的 IDE，列表见 [rust-lang.org/tools](https://www.rust-lang.org/tools)。

### 离线使用本书

预下载依赖示例：

```console
cargo new get-dependencies
cd get-dependencies
cargo add rand@0.8.5 trpl@0.2.0
```

之后可用 `cargo ... --offline` 使用缓存。

## Hello, World!

### 创建项目目录

```console
mkdir ~/projects && cd ~/projects
mkdir hello_world && cd hello_world
```

### Rust 程序基础

- 源文件以 `.rs` 结尾；多词文件名用下划线（`hello_world.rs`）。
- 最小程序：

```rust
fn main() {
    println!("Hello, world!");
}
```

- 编译运行：`rustc main.rs` → `./main`（Windows：`.\main.exe`）。

### Rust 程序的结构

- `fn main()`：可执行程序入口，无参无返回值。
- `println!`：宏（带 `!`），不是普通函数。
- 语句以 `;` 结尾。

### 编译与运行

- Rust 是 **预先编译**（ahead-of-time compiled）语言：先 `rustc` 编译，再运行二进制；可分发可执行文件给未安装 Rust 的用户。

## Hello, Cargo!

**Cargo**：Rust 的构建系统 + 包管理器，处理编译、依赖下载与构建。

### 使用 Cargo 创建项目

```console
cargo new hello_cargo
cd hello_cargo
```

生成结构：

- `Cargo.toml`：项目配置（TOML）
- `src/main.rs`：源码
- 默认初始化 Git 仓库

`Cargo.toml` 要点：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

- `[package]`：包元数据；`edition` 指定 Rust 版本特性。
- `[dependencies]`：外部 crate 依赖；代码包叫 **crate**。

### 构建并运行 Cargo 项目

| 命令 | 作用 |
|------|------|
| `cargo build` | 编译，输出到 `target/debug/` |
| `cargo run` | 编译并运行（常用） |
| `cargo check` | 只检查能否编译，更快 |

- 首次 `cargo build` 生成 `Cargo.lock`，锁定依赖精确版本。
- 源码未改时 Cargo 会跳过重新编译。

### 发布（release）构建

```console
cargo build --release
```

- 输出在 `target/release/`，开启优化，运行更快、编译更慢。
- 做性能基准测试务必用 release 二进制。

### 把 Cargo 当作习惯

多文件、有依赖的项目用 Cargo 协调构建；克隆他人项目后 `cargo build` 即可。

## 总结

- `rustup` 安装 / 更新 Rust，本地文档 `rustup doc`
- `rustc` 直接编译单文件
- `cargo new` / `build` / `run` / `check` / `build --release` 管理真实项目
