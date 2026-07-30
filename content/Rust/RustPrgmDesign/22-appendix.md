+++
title = "22-附录"
date = 2026-07-28T14:49:00+08:00
weight = 220
type = "docs"
description = "关键字、常用运算符、可派生 trait、开发工具、Edition 与 Nightly 速查"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 附录

# 附录

Rust 学习旅途中的参考资料速查。

## 附录 A：关键字

### 目前正在使用的关键字

| 关键字 | 用途 |
|--------|------|
| `as` | 类型转换、消除歧义、`use` 重命名 |
| `async` / `await` | 异步 Future |
| `break` / `continue` | 循环控制 |
| `const` | 常量、常量裸指针 |
| `crate` | 模块路径中的 crate 根 |
| `dyn` | trait 对象动态分发 |
| `else` | `if` / `if let` 分支 |
| `enum` / `struct` / `trait` | 类型定义 |
| `extern` | 外部函数/变量链接 |
| `fn` | 函数或函数指针类型 |
| `for` | 迭代、`impl Trait`、高阶生命周期 |
| `if` / `match` / `while` / `loop` | 控制流 |
| `impl` | 实现方法或 trait |
| `let` / `mut` / `ref` | 绑定、可变性、引用绑定 |
| `move` | 闭包获取捕获项所有权 |
| `pub` | 公有可见性 |
| `return` | 函数返回 |
| `Self` / `self` | 类型别名 / 方法接收者 / 当前模块 |
| `static` | 全局变量、`'static` 生命周期 |
| `super` | 父模块 |
| `type` | 类型别名、关联类型 |
| `union` | 联合体（仅声明处） |
| `unsafe` | 不安全代码/trait/impl |
| `use` | 引入作用域 |
| `where` | 泛型约束 |
| `true` / `false` | 布尔字面量 |
| `in` | `for` 循环语法 |

### 为将来使用保留的关键字

`abstract`、`become`、`box`、`do`、`final`、`gen`、`macro`、`override`、`priv`、`try`、`typeof`、`unsized`、`virtual`、`yield`

### 原始标识符

关键字作标识符时加前缀：`r#match`、`fn r#match(...)`。跨 edition 调用旧库时常见（如 `r#try`）。

## 附录 B：运算符与符号

### 运算符（常用）

| 运算符 | 含义 | 可重载 trait |
|--------|------|--------------|
| `+ - * / %` | 算术 | `Add` `Sub` `Mul` `Div` `Rem` |
| `+= -= ...` | 复合赋值 | 对应 `*Assign` |
| `== !=` | 相等 | `PartialEq` |
| `< <= > >=` | 比较 | `PartialOrd` |
| `&& \|\|` | 短路逻辑与/或 | — |
| `!` | 逻辑/按位非 | `Not` |
| `& \| ^` | 按位与/或/异或 | `BitAnd` `BitOr` `BitXor` |
| `<< >>` | 移位 | `Shl` `Shr` |
| `*` / `&` | 解引用 / 借用 | `Deref` / — |
| `..` / `..=` | 范围（开/闭） | `PartialOrd` |
| `\|` | 模式或 | — |
| `@` | 模式绑定 | — |
| `?` | 错误传播 | — |
| `!`（后缀） | 宏调用 | — |
| `->` | 函数/闭包返回类型 | — |
| `=>` | match 分支 | — |

### 非运算符符号（常用）

| 符号 | 含义 |
|------|------|
| `'a` | 生命周期 / 循环标签 |
| `"..."` / `'...'` | 字符串 / 字符字面量 |
| `r"..."` | 原始字符串 |
| `b"..."` / `b'...'` | 字节串 / 字节字面量 |
| `\|...\|` | 闭包 |
| `_` | 忽略模式 / 整型可读性 |
| `!`（类型） | never type |
| `::` | 路径（`crate::`、`self::`、`super::`） |
| `<T>` / `::<T>` | 泛型参数 / turbofish |
| `'a + Trait` | 生命周期 + trait 约束 |
| `T: Trait` / `where` | trait 约束 |
| `#[...]` / `#![...]` | 属性 / crate 级属性 |
| `//` / `///` / `//!` | 注释 / 文档 / crate 文档 |

## 附录 C：可派生的 trait

`#[derive(...)]` 自动生成 trait 实现（标准库）：

| Trait | 作用 | 要点 |
|-------|------|------|
| **`Debug`** | 调试输出 `{:?}` | `assert_eq!` 需要 |
| **`PartialEq`** | `==` / `!=` | 结构体全字段相等；枚举同变体相等 |
| **`Eq`** | 自反相等标记 | 须 `PartialEq`；浮点 NaN 不可 `Eq` |
| **`PartialOrd`** | `<` `>` `<=` `>=` | 须 `PartialEq`；NaN 无序 |
| **`Ord`** | 全序 `cmp` | 须 `PartialOrd` + `Eq`；`BTreeSet` 需要 |
| **`Clone`** | 显式深拷贝 `.clone()` | 所有字段须 `Clone` |
| **`Copy`** | 隐式位拷贝 | 须 `Clone`；仅栈上简单类型组合 |
| **`Hash`** | 哈希 | `HashMap` 键需要 |
| **`Default`** | `Default::default()` | 配合结构体更新语法 `..Default::default()` |

- **`Display`** 等不可 derive，须手动 impl。
- 库 crate 也可为自有 trait 提供 derive（过程宏）。

## 附录 D：实用开发工具

| 工具 | 命令 | 用途 |
|------|------|------|
| **rustfmt** | `cargo fmt` | 统一代码风格 |
| **rustfix** | `cargo fix` | 自动修复编译警告；edition 迁移 |
| **Clippy** | `cargo clippy` | 额外 lint，捕捉常见错误 |
| **rust-analyzer** | IDE 插件 | LSP：补全、跳转、内联错误 |

## 附录 E：版本

- Rust **每六周**稳定发布；约**每三年**一个 **Edition**（2015 / 2018 / 2021 / 2024）。
- `Cargo.toml` 中 `edition = "2024"`（缺省 2015）。
- 不同 edition 可混用依赖；新关键字等可能仅在新 edition 可用。
- 升级：`cargo fix --edition`；详见 [Edition Guide](https://doc.rust-lang.org/stable/edition-guide)。

## 附录 F：本书译本

- **简体中文**：[KaiserY/trpl-zh-cn](https://github.com/KaiserY/trpl-zh-cn)、[gnu4cn/rust-lang-Zh_CN](https://github.com/gnu4cn/rust-lang-Zh_CN)
- 另有日、韩、俄、西、法、德等多语言社区译本，见原书附录列表。

## 附录 G：Rust 是如何开发的与 “Nightly Rust”

### 无停滞稳定

升级稳定版应无痛：新功能 + 更少 bug + 更快编译；旧代码在升级编译器后仍应能编译。

### 发布通道（火车模型）

```text
nightly（每夜） → beta（六周切出） → stable（再六周发布）
```

- 大部分开发者用 **stable**；尝鲜用 nightly/beta。

### 不稳定功能

- 新功能先进 **nightly**，由 **feature flag** 门控；stable/beta **不可用**。
- 源码加 `#![feature(...)]` 并在 nightly 工具链下编译。

### Rustup 职责

```console
rustup toolchain install nightly
rustup override set nightly    # 当前目录用 nightly
rustup toolchain list
cargo +nightly build
```

### RFC 流程

功能提案 → 团队评审 → 实现 → feature gate → nightly 验证 → 稳定化移除 gate。

### 维护时间

仅支持**最新**稳定版；新版发布后旧版 EOL（约六周）。
