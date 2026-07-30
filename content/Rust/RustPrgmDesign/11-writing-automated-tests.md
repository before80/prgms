+++
title = "11-编写自动化测试"
date = 2026-07-28T14:49:00+08:00
weight = 110
type = "docs"
description = "单元测试与集成测试的写法、cargo test 选项与组织方式"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第11章

# 编写自动化测试

类型系统捕获很多错误；**测试**验证行为是否符合意图。Rust 支持单元测试与集成测试。

## 如何编写测试

测试三步：**设置** → **执行** → **断言**。

### 精心组织测试函数

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
```

- `#[test]`：标记测试函数；`cargo test` 运行。
- 测试在**独立线程**；panic → 该测试失败。
- `cargo new adder --lib` 自动生成测试模板。

```console
cargo test
# running 1 test ... ok
# test result: ok. 1 passed; 0 failed
```

### 使用 `assert!` 宏来检查结果

```rust
#[test]
fn larger_can_hold_smaller() {
    assert!(larger.can_hold(&smaller));
}
```

### 使用 `assert_eq!` 和 `assert_ne!` 宏测试相等

```rust
assert_eq!(add_two(2), 4);
assert_ne!(result, 0);
```

- 失败时打印 `left` / `right`；需 `PartialEq + Debug`（可 `#[derive(PartialEq, Debug)]`）。

### 自定义失败信息

```rust
assert!(result.contains("Carol"), "Greeting was: {}", result);
```

### 使用 `should_panic` 检查 panic

```rust
#[test]
#[should_panic(expected = "less than or equal to 100")]
fn greater_than_100() {
    Guess::new(200);
}
```

- panic 则通过；无 panic 则失败。`expected` 匹配 panic 信息子串。

### 在测试中使用 `Result<T, E>`

```rust
#[test]
fn it_works() -> Result<(), String> {
    if 2 + 2 == 4 { Ok(()) } else { Err(String::from("two plus two")) }
}
```

- 不能用 `#[should_panic]`；断言 `Err` 用 `assert!(value.is_err())`，勿对 `Result` 用 `?`。

## 控制测试如何运行

```console
cargo test -- [传给测试二进制体的参数]
cargo test --help
cargo test -- --help
```

### 并行或顺序运行测试

```console
cargo test -- --test-threads=1
```

- 默认并行；共享状态/文件时用单线程。

### 显示函数输出

```console
cargo test -- --show-output
```

- 默认通过时截获 `println!`；失败时显示输出。

### 通过名称运行部分测试

```console
cargo test one_hundred      # 过滤名称（含模块名）
cargo test add              # 匹配子串
```

### 除非特别指定否则忽略测试

```rust
#[test]
#[ignore]
fn expensive_test() { }
```

```console
cargo test -- --ignored           # 只跑 ignored
cargo test -- --include-ignored   # 全部
```

## 测试的组织结构

| | 单元测试 | 集成测试 |
|---|----------|----------|
| 位置 | `src/*.rs` 内 `#[cfg(test)] mod tests` | 项目根 `tests/*.rs` |
| 可见性 | 可测私有（`use super::*`） | 仅 public API |
| 编译 | 与源码同 crate | **每文件独立 crate** |

### 单元测试

```rust
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn internal() {
        assert_eq!(internal_adder(2, 2), 4);
    }
}
```

- `#[cfg(test)]`：`cargo build` 不包含；`cargo test` 才编译。

### 集成测试

```text
adder/
├── src/lib.rs
└── tests/integration_test.rs
```

```rust
// tests/integration_test.rs
use adder::add_two;

#[test]
fn it_adds_two() {
    assert_eq!(add_two(2), 4);
}
```

```console
cargo test --test integration_test   # 只跑该文件
```

#### 集成测试中的子模块

- 共享代码：`tests/common/mod.rs` + `mod common;`（**不要** `tests/common.rs`，会被当独立测试 crate）。
- 二进制-only 项目：用 `main` 调 `lib`，集成测试测 `lib`。

- 输出顺序：单元测试 → 集成测试 → 文档测试；任一部分失败则后续不跑。
