+++
title = "22-Appendix"
date = 2026-07-28T14:49:00+08:00
weight = 220
type = "docs"
description = "关键字、运算符、derive 与版本发布附录精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「Appendix」

# 附录

## A. 关键字

关键字不可作普通标识符（可用 `r#` 原生标识符绕过，如 `r#match`）。

### 当前使用中的关键字（按用途分类）

| 分类 | 关键字 |
|------|--------|
| 声明 | `let`, `const`, `static`, `fn`, `struct`, `enum`, `trait`, `impl`, `type`, `mod`, `use`, `pub`, `extern`, `crate`, `unsafe` |
| 控制流 | `if`, `else`, `match`, `loop`, `while`, `for`, `break`, `continue`, `return` |
| 类型/泛型 | `where`, `dyn`, `Self`, `self`, `super`, `as`, `in`, `ref`, `mut`, `move` |
| 字面量 | `true`, `false` |

### 保留关键字（暂无功能）

`abstract`, `async`, `await`, `become`, `box`, `do`, `final`, `macro`, `override`, `priv`, `try`, `typeof`, `unsized`, `virtual`, `yield`

> 注：`async`/`await` 在 modern Rust 中已可用；上表为语言规范分类。

### 原生标识符示例

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

源码：`shengJing/_src/src/appendix/keywords.md`

## B. 运算符与符号

### 常用运算符（节选）

| 运算符 | 含义 | 可重载 trait |
|--------|------|--------------|
| `+ - * / %` | 算术 | `Add`, `Sub`, `Mul`, `Div`, `Rem` |
| `+= -= …` | 复合赋值 | 对应 `*Assign` |
| `== !=` | 相等 | `PartialEq` |
| `< <= > >=` | 比较 | `PartialOrd` |
| `& \| ^` | 位运算 | `BitAnd`, `BitOr`, `BitXor` |
| `&&` / `||` | 逻辑与/或 | — |
| `!` | 逻辑/按位非 | `Not` |
| `*` | 解引用 | — |
| `& &mut` | 借用 | — |
| `.. ..=` | 区间 | `PartialOrd` |
| `?` | 错误传播 | — |
| `->` | 函数/闭包返回类型 | — |
| `::` | 路径 | — |
| `.` | 字段/方法 | — |
| `@` | 模式绑定 | — |
| `=>` | match 分支 | — |

### 符号语法（要点）

| 符号 | 用途 |
|------|------|
| `'a` | 生命周期 / 循环标签 |
| `r"..."` / `b"..."` | 原始字符串 / 字节串 |
| `'x'` / `b'x'` | char / ASCII 字节 |
| `\|...\|` | 闭包 |
| `!`（类型） | 发散类型 `!` |
| `_` | 忽略绑定 / 数字分隔 |
| `path<...>` / `path::<...>` | 泛型参数 / turbofish |
| `T: Trait` / `'a: 'b` | trait / 生命周期约束 |
| `#[attr]` / `#![attr]` | 外部/内部属性 |
| `$ident` / `$(...)*` | 宏捕获与重复 |
| `()` | 单元类型 |
| `[T; N]` / `[T]` | 数组 / 切片类型 |
| `{ ... }` | 块 / 结构体字面量 |

完整表格见源码：`shengJing/_src/src/appendix/operators.md`

## C. 表达式要点

Rust 中**多数控制结构是表达式**，可返回值。

| 表达式 | 说明 |
|--------|------|
| 基本 | `let n = 3;` |
| `if` | 分支各 arm 类型须一致 |
| `if let` | 模式匹配单分支 |
| `match` | 穷尽匹配 |
| `loop` | `break expr` 返回值 |
| `{ ... }` | 块表达式，末行无分号为返回值 |

```rust
let v = loop {
    if n == 10 { break n }
    n += 1;
};

let v = if let Some(x) = o { x } else { 0 };
```

源码：`shengJing/_src/src/appendix/expressions.md`

## D. 派生特征 `#[derive(...)]`

`derive` 为结构体/枚举自动生成 trait 实现。无法 derive 的 trait（如 `Display`）需手动实现。

| Trait | 作用 | 要点 |
|-------|------|------|
| `Debug` | `{:?}` 调试输出 | `assert_eq!` 失败时打印 |
| `PartialEq` / `Eq` | `==` / 完全相等 | 浮点仅 `PartialEq`（NaN） |
| `PartialOrd` / `Ord` | 比较 / 全序 | `BTreeMap` 需 `Ord` |
| `Clone` / `Copy` | 深拷贝 / 浅拷贝 | `Copy` 需所有字段 `Copy` |
| `Hash` | 哈希 | `HashMap` 的 K |
| `Default` | 默认值 | 配合结构体更新语法 `..Default::default()` |

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct User { id: u64, name: String }
```

源码：`shengJing/_src/src/appendix/derive.md`

## E. Prelude

标准库预导入模块，含 `Vec`、`String`、`Option`、`Result`、`Box` 等常用类型与 trait。详见 `shengJing/_src/src/appendix/prelude.md`。

## F. Rust 版本发布

### Edition 与 stable 节奏

- 每 **6 周** 发布 stable 小版本
- 每 **2–3 年** 一个 Edition（2015 / 2018 / 2021 / 2024）
- `Cargo.toml` 的 `edition` 字段指定编译版本；编译器向后兼容旧 edition

### 发布通道（火车模型）

```
nightly →（6 周）→ beta →（6 周）→ stable
```

- **Nightly**：每日构建，含不稳定特性
- **Beta**：候选稳定版
- **Stable**：生产推荐

```bash
rustup install nightly
rustup override set nightly   # 项目目录使用 nightly
```

不稳定特性需 `#![feature(...)]`，仅 nightly 可用。

源码：`shengJing/_src/src/appendix/rust-version.md`

## G. 新版解读索引（1.58 – 1.89）

以下版本在源仓库有**中文解读**；每版实际变更更多，完整内容见各文件开头官方 Release 链接。

| 版本 | 源码路径 |
|------|----------|
| 1.58 | `shengJing/_src/src/appendix/rust-versions/1.58.md` |
| 1.59 | `shengJing/_src/src/appendix/rust-versions/1.59.md` |
| 1.60 | `shengJing/_src/src/appendix/rust-versions/1.60.md` |
| 1.61 | `shengJing/_src/src/appendix/rust-versions/1.61.md` |
| 1.62 | `shengJing/_src/src/appendix/rust-versions/1.62.md` |
| 1.63 | `shengJing/_src/src/appendix/rust-versions/1.63.md` |
| 1.64 | `shengJing/_src/src/appendix/rust-versions/1.64.md` |
| 1.65 | `shengJing/_src/src/appendix/rust-versions/1.65.md` |
| 1.66 | `shengJing/_src/src/appendix/rust-versions/1.66.md` |
| 1.67 | `shengJing/_src/src/appendix/rust-versions/1.67.md` |
| 1.68 | `shengJing/_src/src/appendix/rust-versions/1.68.md` |
| 1.69 | `shengJing/_src/src/appendix/rust-versions/1.69.md` |
| 1.70 | `shengJing/_src/src/appendix/rust-versions/1.70.md` |
| 1.71 | `shengJing/_src/src/appendix/rust-versions/1.71.md` |
| 1.72 | `shengJing/_src/src/appendix/rust-versions/1.72.md` |
| 1.73 | `shengJing/_src/src/appendix/rust-versions/1.73.md` |
| 1.74 | `shengJing/_src/src/appendix/rust-versions/1.74.md` |
| 1.75 | `shengJing/_src/src/appendix/rust-versions/1.75.md` |
| 1.76 | `shengJing/_src/src/appendix/rust-versions/1.76.md` |
| 1.77 | `shengJing/_src/src/appendix/rust-versions/1.77.md` |
| 1.78 | `shengJing/_src/src/appendix/rust-versions/1.78.md` |
| 1.79 | `shengJing/_src/src/appendix/rust-versions/1.79.md` |
| 1.80 | `shengJing/_src/src/appendix/rust-versions/1.80.md` |
| 1.81 | `shengJing/_src/src/appendix/rust-versions/1.81.md` |
| 1.82 | `shengJing/_src/src/appendix/rust-versions/1.82.md` |
| 1.83 | `shengJing/_src/src/appendix/rust-versions/1.83.md` |
| 1.84 | `shengJing/_src/src/appendix/rust-versions/1.84.md` |
| 1.85 | `shengJing/_src/src/appendix/rust-versions/1.85.md` |
| 1.86 | `shengJing/_src/src/appendix/rust-versions/1.86.md` |
| 1.87 | `shengJing/_src/src/appendix/rust-versions/1.87.md` |
| 1.88 | `shengJing/_src/src/appendix/rust-versions/1.88.md` |
| 1.89 | `shengJing/_src/src/appendix/rust-versions/1.89.md` |

### 各版重点速览（一行摘要）

| 版本 | 重点 |
|------|------|
| 1.58 | 格式化字符串捕获变量；`unwrap_unchecked` |
| 1.59 | 内联汇编；解构赋值 |
| 1.60 | `cargo --timings`；Feature 新语法 |
| 1.61 | 自定义 `main` 返回 `ExitCode` |
| 1.62 | `cargo add`；`#[default]` 枚举 |
| 1.63 | Scoped threads |
| 1.64 | `IntoFuture`；Cargo workspace 继承 |
| 1.65 | GATs；`let-else` |
| 1.66 | 有字段枚举 `repr`；`black_box` |
| 1.67 | `async fn` 上 `#[must_use]` |
| 1.68 | Cargo sparse index；`pin!` |
| 1.69 | `cargo fix` 建议 |
| 1.70 | `OnceLock`；sparse 默认 |
| 1.71 | C-unwind；raw-dylib |
| 1.72 | cfg 特性提示；Clippy lint 升格 |
| 1.73 | panic 格式优化 |
| 1.74 | Cargo.toml 配置 lint |
| 1.75 | async trait / RPITIT |
| 1.76 | ABI 兼容；`type_name_of_val` |
| 1.77 | 递归 `async fn`；`offset_of!` |
| 1.78 | 诊断属性宏；unsafe 前提断言 |
| 1.79 | 内联 `const`；临时变量生命周期延长 |
| 1.80 | `LazyLock`；开区间 match 模式 |
| 1.81 | `#[expect(lint)]` |
| 1.82 | `use<..>`；`&raw const`；Rust 2024 铺垫 |
| 1.83–1.84 | const 能力扩展；MSRV 感知解析 |
| 1.85 | **Rust 2024** 稳定；`async` 闭包 |
| 1.86 | Trait upcasting |
| 1.87 | 匿名管道；`asm!` label |
| 1.88 | `let` chains；裸函数 |
| 1.89 | const 泛型 `_` 推断 |

索引说明见：`shengJing/_src/src/appendix/rust-versions/intro.md`
