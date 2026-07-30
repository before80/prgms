+++
title = "12-Cargo使用指南"
date = 2026-07-28T14:49:00+08:00
weight = 120
type = "docs"
description = "《Rust语言圣经》「Cargo使用指南」精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「Cargo 使用指南」

# Cargo 使用指南

Cargo = Rust 包管理 + 构建工具；`crates.io` 为社区注册中心。本章基于 [Cargo Book](https://doc.rust-lang.org/stable/cargo/index.html) 整理。

## 上手使用

**Package（项目）** ≠ Crate（包）。`cargo new hello_world` 默认 `--bin` 二进制项目。

```text
hello_world/
├── Cargo.toml    # 清单 manifest
└── src/main.rs
```

| 命令 | 说明 |
|------|------|
| `cargo build` | Debug 编译 → `target/debug/` |
| `cargo build --release` | Release（性能测试必用） |
| `cargo run` / `cargo run --release` | 编译并运行 |
| `cargo new --lib` | 库项目 |

## 基础指南

### 为何会有 Cargo

`rustc` 直接编译的问题：多文件、编译参数、依赖版本管理复杂。Cargo 四件事：

1. `Cargo.toml` + `Cargo.lock` 元数据
2. 拉取/构建依赖（crates.io 等）
3. 调用 `rustc` 并传正确参数
4. 约定目录结构，降低学习成本

### 下载并构建 Package

- `cargo build`：首次拉依赖并编译
- `cargo update`：更新 lock 中依赖（在允许范围内）
- 离线/缓存命中时跳过下载

### 添加依赖

`Cargo.toml`：

```toml
[dependencies]
serde = "1.0"
```

- `cargo add 包名`（新版 Cargo）自动写入
- 修改后 `cargo build` 自动解析

### Package 目录结构

标准布局：

```text
.
├── Cargo.toml
├── Cargo.lock          # 应用项目通常提交
├── src/
│   ├── main.rs         # bin 默认入口
│   └── lib.rs          # lib 默认入口
├── tests/              # 集成测试
├── benches/            # 基准测试
├── examples/           # 示例
└── build.rs            # 构建脚本（可选）
```

- 二进制：`src/bin/*.rs` 或 `[[bin]]` 指定
- 库：`src/lib.rs` 或 `[[lib]]`

### Cargo.toml vs Cargo.lock

| 文件 | 谁写 | 内容 |
|------|------|------|
| `Cargo.toml` | 用户 | 项目信息、依赖**范围** |
| `Cargo.lock` | Cargo | 依赖**精确**版本树 |

**是否提交 lock：**

- **库 crate**（被他人依赖）→ `.gitignore` lock
- **终端产品**（CLI/应用）→ 提交 lock，保证可复现构建

原因：下游引入库时不应被库的 lock 约束；应用需要确定性环境。

无 lock 时 Cargo 解析最新兼容版本；有 lock 则锁定直到 `cargo update`。

### 测试和 CI

- `cargo test` / `cargo check`（只检查不产出二进制，更快）
- CI 常用：`cargo test --all-features`、缓存 `~/.cargo` 与 `target/`
- 平台：GitHub Actions / Travis / GitLab CI

### Cargo 缓存

**Cargo Home**（默认 `~/.cargo`）：

- `registry/`：crate 源码缓存
- `git/`：git 依赖
- `bin/`：安装的 binary

CI 缓存 Cargo Home 可大幅加速。卡住 `Blocking waiting for file lock` → 并发构建争锁，稍等或杀残留进程。

### Build 缓存

**target/** 结构：

- `target/debug/` 或 `target/release/`：产物
- `target/<triple>/`：交叉编译
- `.fingerprint/`、`.d` 文件：增量编译依赖追踪

共享缓存：多项目可配置同一 `target` 目录（workspace 天然共享）。

## 进阶指南

### 指定依赖项

版本语法（semver）：

| 写法 | 含义 |
|------|------|
| `"1.2.3"` | `^1.2.3`（兼容升级） |
| `"~1.2.3"` | `>=1.2.3, <1.3.0` |
| `"=1.2.3"` | 精确 |
| `"*"` | 任意（不推荐） |
| `">=1.2.3, <2.0"` | 比较符组合 |

其他来源：

```toml
dep = { git = "https://...", rev = "abc123" }
dep = { path = "../local-crate" }
dep = { version = "1.0", registry = "..." }
```

- `[target.'cfg(windows)'.dependencies]` 平台依赖
- `[dev-dependencies]` 仅测试/示例
- `[build-dependencies]` 仅 build.rs
- `package = { ... }` 重命名依赖

### 依赖覆盖

`[patch]` 临时替换依赖源（测 bugfix、本地 fork）：

```toml
[patch.crates-io]
serde = { git = "..." }
```

- 可 patch 间接依赖
- `[replace]` 已不推荐

### Cargo.toml 清单详解

`[package]` 常用字段：

| 字段 | 说明 |
|------|------|
| `name` / `version` | 包名、semver |
| `edition` | 2021 等 |
| `authors` / `description` / `license` | 元信息 |
| `rust-version` | 最低 Rust 版本 |
| `readme` / `documentation` / `repository` | 文档链接 |
| `keywords` / `categories` | crates.io 分类 |
| `workspace` | 所属 workspace |
| `build` | 自定义 build 脚本路径 |
| `links` | 本地库链接 key（防重复） |
| `exclude` / `include` | 打包白/黑名单 |
| `publish` | 禁止发布到 crates.io |
| `default-run` | 多 bin 时默认运行哪个 |

`[badges]`：maintenance 状态等。

### Cargo Target

五类 target：**lib / bin / example / test / bench**

`Cargo.toml` 可显式配置：

```toml
[[bin]]
name = "my_tool"
path = "src/bin/tool.rs"
required-features = ["cli"]
```

- `crate-type`：`lib`、`cdylib`、`staticlib` 等
- `proc-macro = true`：过程宏 crate
- 自动发现：`src/bin/*.rs`、`examples/`、`benches/`、`tests/`

### 工作空间 Workspace

多 package 共享 `Cargo.lock` 与 `target/`。

两种：

1. **根 package**：根 `Cargo.toml` 含 `[package]` + `[workspace] members = [...]`
2. **虚拟 manifest**：仅 `[workspace]`，无根 package

常用命令：

```text
cargo build -p crate_name     # 指定 member
cargo test --workspace        # 全 workspace
```

`[workspace.metadata]` 供工具读取。

### 条件编译 Features

```toml
[features]
default = ["std"]
webp = ["dep:webp-decoder"]
full = ["webp", "async"]
```

要点：

- `default` 默认启用；`--no-default-features`
- 可选依赖：`optional = true` + feature 启用
- 命令行：`cargo build --features "a,b"`
- feature 统一化：同名 feature 合并启用
- `required-features`：bin/example 按需启用
- Resolver V2：避免 feature 意外传播

### 发布配置 Profile

| profile | 用途 |
|---------|------|
| `dev` | 默认 debug，编译快 |
| `release` | 优化，上线用 |
| `test` / `bench` | 测试/基准专用 |

常用设置：

| 键 | 说明 |
|----|------|
| `opt-level` | 0–3 / "s"/"z" |
| `debug` | 调试信息 |
| `lto` | 链接时优化 |
| `codegen-units` | 并行 codegen（1 更优优化） |
| `panic` | `unwind` / `abort` |
| `overflow-checks` | 算术溢出检查 |
| `incremental` | 增量编译 |

`[profile.release.package.foo] opt-level = 3` 可 per-crate 覆盖。

### 通过 config.toml 对 Cargo 进行配置

层级（后者覆盖前者）：

1. `$CARGO_HOME/config.toml`
2. 项目 `.cargo/config.toml`
3. 环境变量 `CARGO_*`

可配置：registry mirror、build target、`[patch]`、`[alias]`、`[env]` 等。

### 发布到 crates.io

流程：

1. [crates.io](https://crates.io) 注册 + `cargo login`
2. 完善 `Cargo.toml` 元数据、`README`、`license`
3. `cargo publish --dry-run` / `cargo package` 检查
4. `cargo publish`
5. 新版本 bump `version` 再 publish

管理：`cargo yank` 撤版本（不删）；`cargo owner` 管理协作者。

### 构建脚本 build.rs

- 项目根 `build.rs`，编译为独立程序，**先于**主 crate 运行
- 输出：`cargo:rustc-link-lib=...`、`cargo:rerun-if-changed=...` 等
- 用途：代码生成、编译 C 库、条件编译
- `[build-dependencies]` 引入 build 专用 crate
- `links` key 防止多 crate 重复链接同一本地库

---

**速查**

```text
cargo check / build / run / test
cargo add 包名
cargo update -p 包名
cargo tree                    # 依赖树
cargo publish --dry-run
```
