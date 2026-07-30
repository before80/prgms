+++
title = "07-包、Crates与模块"
date = 2026-07-28T14:49:00+08:00
weight = 70
type = "docs"
description = "包与 crate 划分、模块树、路径、use 与 pub 私有性规则精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第7章

# 包、Crates 与模块

大型项目需要组织代码：**包**（Cargo 构建单元）、**crate**（编译最小单位）、**模块**（分组 + 控制私有性）、**路径**（命名项）、**use**（引入作用域）。

## 包和 Crate

- **Crate**：编译器处理的最小单位；含模块，模块可拆到多文件。
- **二进制 crate**：有 `main`，产出可执行文件。
- **库 crate**：无 `main`，供复用；**crate root** 是起始源文件（`src/main.rs` 或 `src/lib.rs`）。
- **包**：一个或多个 crate + `Cargo.toml`。
  - 至多 **1 个库 crate**；任意多个二进制 crate；**至少 1 个 crate**。
- Cargo 约定：
  - `src/main.rs` → 与包同名的二进制 crate 根
  - `src/lib.rs` → 与包同名的库 crate 根
  - `src/bin/*.rs` → 每个文件一个独立二进制 crate

```console
cargo new my-project          # 默认二进制
cargo new restaurant --lib    # 库 crate
```

## 定义模块来控制作用域与私有性

### 模块小抄（Cheat Sheet）

| 规则 | 要点 |
|------|------|
| 从 crate 根开始 | 库：`src/lib.rs`；二进制：`src/main.rs` |
| 声明模块 | `mod garden;` → 内联 `{}` / `src/garden.rs` / `src/garden/mod.rs` |
| 声明子模块 | 父模块文件中 `mod vegetables;` → `src/garden/vegetables.rs` 等 |
| 路径引用 | 如 `crate::garden::vegetables::Asparagus` |
| 私有 vs 公用 | 默认私有；`pub mod` / `pub fn` 等暴露 |
| `use` | 创建快捷方式，减少长路径重复 |

```text
backyard/src/
├── main.rs          # pub mod garden;
├── garden.rs        # pub mod vegetables;
└── garden/vegetables.rs
```

### 在模块中对相关代码进行分组

- `mod` 定义模块；可嵌套模块、函数、结构体等。
- 模块树植根于隐式 `crate` 模块；父子/兄弟关系类比文件系统目录。

## 引用模块树中项的路径

- **绝对路径**：外部 crate 以 crate 名开头；当前 crate 以 `crate` 开头。
- **相对路径**：以 `self`、`super` 或当前模块标识符开头。
- 路径用 `::` 连接各段。

```rust
crate::front_of_house::hosting::add_to_waitlist()
front_of_house::hosting::add_to_waitlist()
super::deliver_order()  // 从父模块起，类似 ..
```

### 使用 `pub` 关键字暴露路径

- 默认：项对**父模块**私有；父不能用子模块私有项，子可用父模块项。
- `pub mod hosting`：模块公有，**内容仍默认私有**。
- 需逐级 `pub` 到实际要用的项（如 `pub fn add_to_waitlist`）。
- **最佳实践**：逻辑放 `src/lib.rs`；`main.rs` 只调用库的 public API。

### `super` 开始的相对路径

- `super::` 从父模块构建路径，便于模块树重组。

### 创建公有的结构体和枚举

- `pub struct`：结构体公有，**字段默认仍私有**；需 `pub` 字段或提供构造函数。
- `pub enum`：所有变体自动公有。

## 使用 `use` 关键字将路径引入作用域

- `use` 只在**当前作用域**有效；类似符号链接。
- **惯用法**：
  - 函数：引入**父模块**（`use crate::...::hosting`），调用时写 `hosting::add_to_waitlist`
  - 结构体/枚举：引入**完整路径**（`use std::collections::HashMap`）
- 同名冲突：用父模块限定（`std::fmt::Result`）或 `as` 别名（`use std::io::Result as IoResult`）。

### 使用 `pub use` 重导出名称

- `pub use`：重导出，外部可用更短路径（如 `restaurant::hosting::...`）。

### 使用外部包

```toml
# Cargo.toml
rand = "0.8.5"
```

```rust
use rand::Rng;
use std::collections::HashMap;  // std 也是外部 crate
```

### 使用嵌套路径来清理大量的 `use` 列表

```rust
use std::cmp::{max, min};
use std::io::{self, Write};  // self 引入 io 本身
```

### 通过 glob 运算符导入项

```rust
use std::collections::*;
```

- 测试模块常用；生产代码慎用（难追踪名称来源）。

## 将模块拆分成多个文件

- `mod front_of_house;` 只声明一次；编译器按模块树位置找文件。
- `mod` **不是** include；其他文件用路径引用，不再重复 `mod`。
- 子模块文件放父模块同名目录：`src/front_of_house/hosting.rs`。
- 旧风格 `mod.rs` 仍支持，但多个 `mod.rs` 不便浏览。

- **库 + 二进制**：`main.rs` 薄封装，调用 `lib.rs` 逻辑；便于测试与复用。
