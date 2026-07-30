+++
title = "15-Rust最佳实践"
date = 2026-07-28T14:49:00+08:00
weight = 150
type = "docs"
description = "三方库精选、命名规范与日常开发流程精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「Rust 最佳实践」

# Rust 最佳实践

生产级项目重**稳定性与可维护性**。本章汇总库选型、命名惯例与开发习惯（节选自 [Cook Rust](https://cook.rs)）。

## 日常开发三方库精选

同一类别按推荐度降序；生产项目优先选**社区活跃、维护稳定**的 crate。

| 类别 | 首选 | 备选/说明 |
|------|------|-----------|
| HTTP 客户端 | [reqwest](https://github.com/seanmonstar/reqwest) | — |
| Web 框架 | [axum](https://github.com/tokio-rs/axum) | Rocket、actix-web |
| 异步运行时 | [tokio](https://github.com/tokio-rs/tokio) | async-std（学习/小项目） |
| 日志 | [tracing](https://github.com/tokio-rs/tracing) | log + 实现；不推荐 slog |
| 可观测 | [OpenTelemetry Rust](https://github.com/open-telemetry/opentelemetry-rust) | [vector](https://github.com/vectordotdev/vector) 采集 |
| SQL | [sqlx](https://github.com/launchbadge/sqlx) | diesel、rbatis |
| Redis | [redis-rs](https://github.com/mitsuhiko/redis-rs) | — |
| MongoDB | [官方驱动](https://github.com/mongodb/mongo-rust-driver) | — |
| gRPC | [tonic](https://github.com/hyperium/tonic) | grpc-rs |
| 序列化 | [serde](https://github.com/serde-rs/serde) + json/toml/yaml | — |
| 搜索（本地） | [tantivy](https://github.com/quickwit-inc/tantivy) | — |
| 基准测试 | [criterion](https://github.com/bheisler/criterion.rs) | hyperfine（CLI） |
| 火焰图 | [flame](https://github.com/llogiq/flame) | — |

完整清单见源码 `shengJing/_src/src/practice/third-party-libs.md`。

## 命名规范

**类型级**用驼峰（`UpperCamelCase`），**值级**用蛇形（`snake_case`）。

| 条目 | 惯例 |
|------|------|
| 模块 | `snake_case` |
| 类型/特征/枚举/结构体 | `UpperCamelCase` |
| 函数/方法/变量 | `snake_case` |
| 常量/静态 | `SCREAMING_SNAKE_CASE` |
| 生命周期 | `'a` |
| 包名 | 勿加 `-rs` / `-rust` 后缀 |

- 特征名用**动词**：`Print` 优于 `Printable`
- 复合词缩写作单词：`Uuid` 非 `UUID`

### 类型转换：`as_` / `to_` / `into_`

| 前缀 | 开销 | 所有权 |
|------|------|--------|
| `as_` | 零/极低 | 借 → 借 |
| `to_` | 可能分配 | 借 → 借/拥有 |
| `into_` | 视情况 | 拥有 → 拥有 |

### 迭代器命名

```rust
fn iter(&self) -> Iter<'_>       // Item = &T
fn iter_mut(&mut self) -> IterMut // Item = &mut T
fn into_iter(self) -> IntoIter    // Item = T
```

### Getter

优先 `fn first(&self)`，而非 `get_first`；仅当「通过索引/键取值」时用 `get` / `get_mut`。

## 开发流程要点

| 实践 | 说明 |
|------|------|
| `cargo watch` | 保存即编译，缩短反馈 |
| 测试组织 | 单元测试放 `mod tests`；集成测试放 `tests/` |
| `cargo clippy` | 静态检查，纳入 CI |
| 覆盖率 | codecov 等工具辅助 |
| 查类型 | rust-analyzer 跳转；或故意写错类型让编译器提示 |

```rust
let f: u32 = File::open("hello.txt");
// error: expected u32, found Result<File, Error>
```

## 面试资料（外链）

- [记一次 Rust 技术面试](https://zhuanlan.zhihu.com/p/411979704)
- [飞书 Rust 实习](https://blog.kuangjux.top/2021/10/22/飞书Rust实习面试/)
- [字节 Rust/C++ 实习](https://www.nowcoder.com/discuss/538078)

更多见源码 `shengJing/_src/src/practice/`。
