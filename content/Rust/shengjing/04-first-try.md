+++
title = "04-寻找牛刀，以便小试"
date = 2026-07-28T14:49:00+08:00
weight = 40
type = "docs"
description = "安装 Rust、VSCode、Cargo 与首个程序，环境配置精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「寻找牛刀，以便小试」

# 寻找牛刀，以便小试

本章：安装 Rust → 配置 VSCode → 认识 Cargo → 写第一个程序 → 解决依赖下载慢。

## 安装 Rust 环境

**工具**：`rustup` = 安装器 + 版本管理器。推荐唯一安装方式。

| 平台 | 命令/步骤 |
|------|-----------|
| Linux/macOS | `curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf \| sh` |
| FreeBSD | `pkg install rustup-init` 或 Ports |
| Windows (msvc) | 先装 [C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)，再运行 `rustup-init.exe`，默认 `x86_64-pc-windows-msvc` |
| Windows (gnu) | MSYS2 + mingw64，安装时改 host 为 `x86_64-pc-windows-gnu` |

**链接器报错**：需 C 编译器 — macOS: `xcode-select --install`；Ubuntu: `build-essential`。

**常用命令**：

```bash
rustup update          # 更新
rustup self uninstall  # 卸载
rustc -V && cargo -V   # 验证
rustup doc               # 本地文档
```

**PATH**：Windows 确保 `%USERPROFILE%\.cargo\bin` 在 PATH 中。

## 墙推 VSCode!

**插件**：选 **rust-analyzer**（官方 `Rust` 插件已弃用）。优点：跳转三方库、类型标注、补全。

**注意**：保存时会触发 `cargo check`；勿与终端同时 `cargo build`，否则 `Blocking waiting for file lock`。

**推荐插件**：Even Better TOML、Error Lens、CodeLLDB。

## 认识 Cargo

Rust 包管理 + 构建工具，随 `rustup` 安装。

**创建项目**：

```bash
cargo new world_hello   # 默认 bin 项目，含 .git
cd world_hello
```

**目录**：

```
Cargo.toml
src/main.rs
```

**运行与编译**：

| 命令 | 作用 |
|------|------|
| `cargo run` | 编译 + 运行（debug） |
| `cargo build` | 仅编译 → `target/debug/` |
| `cargo run --release` | release 模式 → `target/release/` |
| `cargo check` | 只检查能否编译，最快 |

**debug vs release**：debug 编译快、运行慢；release 编译慢、运行快。

**Cargo.toml 核心**：

```toml
[package]
name = "world_hello"
version = "0.1.0"
edition = "2021"

[dependencies]
rand = "0.8"                    # crates.io 版本
# hammer = { version = "0.5" }
# color = { git = "https://..." }
# geometry = { path = "crates/geometry" }
```

**Cargo.lock**：由 Cargo 自动生成依赖锁定文件。

| 项目类型 | 是否提交 lock |
|----------|---------------|
| 可执行程序 (bin) | 提交 |
| 库 (lib) | 加入 `.gitignore` |

## 不仅仅是 Hello world

**多国语言问候**：

```rust
fn greet_world() {
    let regions = ["Grüß Gott!", "世界，你好", "World, hello"];
    for region in regions.iter() {
        println!("{}", region);
    }
}
```

**要点**：

- Rust 原生 UTF-8
- `println!` 中 `!` = 宏，非函数
- `{}` 自动识别类型，无需 `%s`
- 集合需 `.iter()` 才能 for 循环（2021+ 可写 `for region in regions`）

**初印象代码要点**（CSV 解析企鹅数据）：

| 特性 | 示例 |
|------|------|
| 控制流 | `for` + `continue` |
| 方法 | `record.trim()`, `.split(',')` |
| 闭包 | `.map(\|field\| field.trim())` |
| 类型标注 | `.parse::<f32>()` |
| if let | `if let Ok(length) = fields[1].parse::<f32>()` |
| 条件编译 | `if cfg!(debug_assertions) { eprintln!(...) }` |
| 隐式返回 | 块末尾表达式无分号 |

消除 debug 输出：`cargo run --release`。

## 下载依赖太慢了？

依赖源：[crates.io](https://crates.io)。国内慢 → 镜像或代理。

**方案 1：终端代理**（翻墙工具需开启终端/全局代理）：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890
```

**方案 2：覆盖默认镜像**（推荐，写 `$HOME/.cargo/config.toml`）：

```toml
[source.crates-io]
replace-with = 'ustc'

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
```

**字节跳动 rsproxy**：

```toml
[source.crates-io]
replace-with = 'rsproxy-sparse'

[source.rsproxy-sparse]
registry = "sparse+https://rsproxy.cn/index/"
```

**新增镜像**（需每个依赖指定 registry，不推荐大项目）：

```toml
[registries.ustc]
index = "https://mirrors.ustc.edu.cn/crates.io-index/"

[dependencies]
time = { registry = "ustc" }
```

**卡住排查**：

- 索引更新慢 → 用国内稀疏索引
- `Blocking waiting for file lock on package cache` → IDE 与终端同时构建；等待或杀 `rust-analyzer`，删 `~/.cargo/.package_cache`
