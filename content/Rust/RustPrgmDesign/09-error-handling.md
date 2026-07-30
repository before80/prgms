+++
title = "09-错误处理"
date = 2026-07-28T14:49:00+08:00
weight = 90
type = "docs"
description = "panic 与 Result、? 传播及何时 panic 的决策要点"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第9章

# 错误处理

Rust 无异常；分两类：

| 类型 | 机制 | 场景 |
|------|------|------|
| **不可恢复** | `panic!` | bug、违反契约 |
| **可恢复** | `Result<T, E>` | 文件不存在等可处理失败 |

## 用 `panic!` 处理不可恢复的错误

- 触发方式：显式 `panic!`；或越界访问等。
- 默认：**展开**（unwind）栈并清理；可设 `panic = 'abort'` 直接终止（release 减小体积）。

```toml
[profile.release]
panic = 'abort'
```

```rust
panic!("crash and burn");
```

### 使用 `panic!` 的 backtrace

```console
RUST_BACKTRACE=1 cargo run
```

- 从 backtrace **最上往下**找**自己项目**的第一个帧。

## 用 `Result` 处理可恢复的错误

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

```rust
let f = File::open("hello.txt");  // Result<File, io::Error>
```

### 匹配不同的错误

```rust
let f = File::open("hello.txt").unwrap_or_else(|error| {
    if error.kind() == ErrorKind::NotFound {
        File::create("hello.txt").unwrap_or_else(|e| panic!("create: {e:?}"))
    } else {
        panic!("open: {error:?}")
    }
});
```

### 失败时 panic 的快捷方式

- **`unwrap()`**：`Ok` 取值，`Err` 则 panic。
- **`expect("msg")`**：同上，可自定义 panic 信息（生产更推荐）。

### 传播错误

- 函数返回 `Result`，用 `return Err(e)` 或 **`?`** 向上传播。

```rust
fn read_username_from_file() -> Result<String, io::Error> {
    let mut s = String::new();
    File::open("hello.txt")?.read_to_string(&mut s)?;
    Ok(s)
}

// 更简
fn read_username_from_file() -> Result<String, io::Error> {
    fs::read_to_string("hello.txt")
}
```

- `?`：`Ok` 解包继续；`Err` 经 `From` 转换后**提前 return**。
- **限制**：只能在返回 `Result` / `Option` / 实现 `FromResidual` 的函数中用。
- `main` 可返回 `Result<(), Box<dyn Error>>`，末尾 `Ok(())`；`Err` 退出码非 0。

### 哪里可以使用 `?` 运算符

- `Result` 上 `?` ↔ 返回 `Result` 的函数；`Option` 同理；**不可混用**（需 `ok` / `ok_or` 转换）。

## 要不要 `panic!`

| 用 `Result`（默认） | 用 `panic!` |
|---------------------|-------------|
| 调用者决定如何处理 | 不可恢复 / 有害状态 |
| 预期可能失败（解析、HTTP 限流） | 违反函数契约、无效前置条件 |
| 库 API 暴露错误 | 示例、原型、`unwrap` 占位 |

### 示例、代码原型和测试

- 原型/测试：`unwrap` / `expect` 可接受；测试失败即 panic。

### 当你比编译器知道更多时

- 逻辑上不可能 `Err` 时用 `expect("原因")`，并在消息中说明假设。

### 错误处理指导原则

- **有害状态**（不变量被破坏）且无法编码进类型 → panic。
- 用**类型系统**减少运行时检查（非 `Option` 即必有值；`u32` 非负等）。

### 为验证创建自定义类型

```rust
pub struct Guess { value: i32 }

impl Guess {
    pub fn new(value: i32) -> Self {
        if !(1..=100).contains(&value) {
            panic!("Guess must be 1..=100, got {value}");
        }
        Guess { value }
    }
    pub fn value(&self) -> i32 { self.value }
}
```

- 私有字段 + `new` 构造：保证有效范围；API 文档应说明 panic 条件。
