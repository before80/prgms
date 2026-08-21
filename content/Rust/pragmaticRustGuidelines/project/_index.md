+++
title = "第8章 项目"
date = 2026-08-18T18:10:00+08:00
weight = 100
type = "docs"
description = "项目指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/project/index.html](https://microsoft.github.io/rust-guidelines/guidelines/project/index.html)

# 项目

## 公共设置来自 workspace 的 Cargo.toml (M-CARGO-WORKSPACE) {#M-CARGO-WORKSPACE}

*本条守护：一致、可维护的项目配置。*

任何包含两个或更多彼此相关 crate 的仓库，都应当用 workspace 的 `Cargo.toml` 统一这些 crate。成员随后通过 `[workspace.dependencies]`、`[workspace.lints]` 等从 workspace 根继承共享元数据与依赖版本，而不是在每个 crate 中重复这些值。

若某依赖是 crate 特有的，仍应在 workspace 中定义。Workspace 定义一般不应启用依赖特性（`["std"]` 等基础特性除外），而应使用 `default-features = false`。

## workspace 列出并为所有 crate 指定版本 (M-CRATES-IN-WORKSPACE) {#M-CRATES-IN-WORKSPACE}

*本条守护：简洁的 crate 间依赖与调试。*

项目产出的每个 crate 都应列为 workspace 成员，并在 `[workspace.dependencies]` 中声明其版本，使 workspace 内依赖解析到单一规范版本。

```toml
# 不好：crate 直接链接兄弟 crate
[dependencies]
sibling.path = "../sibling"

# 好：通过 workspace
[dependencies]
sibling.workspace = true

[workspace.dependencies]
sibling = { path = "crates/sibling", version = "0.5.2" }
```

## 所有 crate 作为兄弟目录放在同一文件夹 (M-CRATES-FLAT-FOLDER) {#M-CRATES-FLAT-FOLDER}

*本条守护：简洁的项目导航与标准 Rust 布局。*

仓库应包含单一的 workspace `Cargo.toml`，所有 Rust crate 都应从属于它。所有 crate 随后应位于 workspace 下单一的直接子目录（例如 `crates/`）中（适用于大约一两打 crate）；超出此规模则应使用某种文件夹层级（例如 `common/`、`server/`、`client/`）来组织兄弟 crate。

```bash
# 大多数 workspace 的理想布局
Cargo.toml
crates/
  foo/Cargo.toml 
  foo_core/Cargo.toml 
  foo_proc/Cargo.toml 
  foo_tests/Cargo.toml 
  bar/Cargo.toml
  baz/Cargo.toml

# 大型 workspace 亦可接受
Cargo.toml
crates/
  server/
    main/Cargo.toml 
    routes/Cargo.toml 
  client/
    foo/Cargo.toml
    bar/Cargo.toml
  common/
    error/Cargo.toml
```

将 crate 放在其他 crate 内部（位于其 `Cargo.toml` 处或之下），甚至放在其 `src/` 文件夹中，绝不可接受。若需表达 crate 关系，应通过公共前缀（例如 `foo`、`foo_util`、`foo_build`）。

```bash
# 绝不可接受：crate 位于 `src/` 文件夹内
Cargo.toml
crates/
  foo/Cargo.toml 
    src/lib.rs
       deps/bar/Cargo.toml 
```

本规则的罕见例外可能出现在：你的 crate 业务就是处理 workspace，并依赖一批 UI 测试或类似内容；即便如此，这些通常本质上也是哑 crate。

## 新 crate 面向最新 edition (M-LATEST-EDITION) {#M-LATEST-EDITION}

*本条守护：使用最新 Rust 特性。*

创建新 crate 或 workspace 时，将 `edition` 设为最新稳定 edition（撰写时至少为 `2024`）；通常不需要 `resolver` 字段。

对新项目使用较旧 edition 通常没有好处，却会迫使你写「旧式 Rust」，更不惯用，且有更差的 UX 边界情况。值得注意的是，使用较旧 edition _不会_ 带来与生态其余部分的任何兼容性收益。基于 `2015` 的应用可以正常使用为 `2024` 编写的库。

## 保守地更新 MSRV (M-MSRV) {#M-MSRV}

*本条守护：现代特性与对用户的稳定性。*

首次创建库时应设置最低支持的 Rust 版本（MSRV）。随着需要新的 Rust 特性可以更新它，但应保持落后于最新编译器发布几个版本。

生态期望是：项目用 _合理现代_ 的 Rust 编译器编译。

因此提升 MSRV 不需要主版本发布，可通过次版本更新处理（例如 `1.3` 到 `1.4`）。事实上，任何依赖第三方 crate 的项目本来就受此约定约束；强制主版本提升不会带来任何好处，却可能造成下游依赖分裂。
