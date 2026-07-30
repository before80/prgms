+++
title = "06-入门实战：文件搜索工具"
date = 2026-07-28T14:49:00+08:00
weight = 60
type = "docs"
description = "minigrep 实战：CLI 参数、模块化、测试、环境变量与 stderr"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「入门实战：文件搜索工具」

# 入门实战：文件搜索工具

目标：简化版 `grep` — 从命令行读**查询词**和**文件路径**，打印含该词的行。项目名 `minigrep`。

## 基本功能

### 接收命令行参数

```bash
cargo run -- searchstring example-filename.txt
# `--` 后参数传给程序，不是 cargo
```

```rust
use std::env;
let args: Vec<String> = env::args().collect();
// args[0] = 程序路径；args[1] = query；args[2] = file_path
```

- `env::args()` → 迭代器，`collect()` → `Vec<String>`
- 非 Unicode 参数：`env::args_os()` → `OsString`

### 存储参数与读文件

```rust
let query = &args[1];
let file_path = &args[2];

use std::fs;
let contents = fs::read_to_string(file_path)
    .expect("Should have been able to read the file");
```

### 搜索并打印

```rust
for line in contents.lines() {
    if line.contains(query) {
        println!("{}", line);
    }
}
```

**最小 main 流程**：`args` → `query`/`file_path` → `read_to_string` → 逐行 `contains` → `println!`。

## 增加模块化和错误处理

**改进点**：

1. 拆分大 `main` → `lib.rs` 放逻辑
2. 配置聚合为 `Config` 结构体
3. 细化错误信息（非统一 expect）
4. 参数不足等返回 `Result`，勿 panic

**关注点分离**：

| 文件 | 职责 |
|------|------|
| `main.rs` | 解析参数、调 `run`、处理错误、进程退出 |
| `lib.rs` | `Config`、`run()`、`search()` |

```rust
// main.rs
fn main() {
    let config = Config::build(&env::args().collect())
        .unwrap_or_else(|err| { eprintln!("{err}"); process::exit(1); });
    if let Err(e) = minigrep::run(config) { ... }
}

// lib.rs
pub struct Config {
    pub query: String,
    pub file_path: String,
    pub ignore_case: bool,
}

impl Config {
    pub fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 { return Err("not enough arguments"); }
        Ok(Config {
            query: args[1].clone(),
            file_path: args[2].clone(),
            ignore_case: false,
        })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn std::error::Error>> {
    let contents = std::fs::read_to_string(config.file_path)?;
    for line in search(&config.query, &contents) {
        println!("{line}");
    }
    Ok(())
}

pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    contents.lines()
        .filter(|line| line.contains(query))
        .collect()
}
```

**错误类型演进**：`&'static str` → `Box<dyn Error>` → 自定义 `error` crate 枚举（见进阶章）。

**`?` 传播**：`read_to_string` 失败自动返回 `Err`。

## 测试驱动开发

TDD 循环：写失败测试 → 写通过测试 → 实现代码。

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_result() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.";
        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
}
```

```bash
cargo test
```

- 测试模块 `#[cfg(test)] mod tests`
- 先 stub `search` 返回 `vec![]` 确保测试**失败**
- 实现 `filter`/`contains` 后通过
- 集成测试：`tests/integration_test.rs`，仅测 public API

## 使用环境变量

**目标**：`IGNORE_CASE=1` 时大小写不敏感。

```rust
pub fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let query = query.to_lowercase();
    contents.lines()
        .filter(|line| line.to_lowercase().contains(&query))
        .collect()
}
```

```rust
// Config::build 内
let ignore_case = env::var("IGNORE_CASE").is_ok();
```

```rust
// run 内
let search_fn = if config.ignore_case {
    search_case_insensitive
} else {
    search
};
```

**测试**：

```rust
#[test]
fn case_insensitive() {
    assert_eq!(vec!["Rust:", "Trust me."],
        search_case_insensitive("rUsT", "Rust:\nTrust me."));
}
```

**运行**：`IGNORE_CASE=1 cargo run -- to poem.txt`（Windows PowerShell: `$env:IGNORE_CASE=1; cargo run -- ...`）。

## 重定向错误信息的输出

| 流 | 宏 | 用途 |
|----|-----|------|
| stdout | `println!` | 正常结果 |
| stderr | `eprintln!` | 错误、诊断 |

```rust
.unwrap_or_else(|err| {
    eprintln!("Problem parsing arguments: {err}");
    process::exit(1);
});
```

```bash
cargo run > output.txt          # 仅 stdout 进文件；stderr 仍终端
cargo run 2> errors.txt         # stderr 重定向
```

用户可将结果与错误分到不同文件。

## 使用迭代器来改进程序(可选)

**Config::build 拿迭代器所有权**，去掉 `clone`：

```rust
pub fn build(
    mut args: impl Iterator<Item = String>,
) -> Result<Config, &'static str> {
    args.next(); // 跳过程序名
    let query = args.next().ok_or("missing query")?;
    let file_path = args.next().ok_or("missing file")?;
    ...
}
```

```rust
// main
let config = Config::build(env::args())?;
```

**search 迭代器链**：

```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    contents.lines()
        .filter(|line| line.contains(query))
        .collect()
}
```

**case_insensitive** 同理；`to_lowercase()` 产生新 `String`，故 filter 内不能简单返回 `&line` 的子串 — 原书用 `contains` 整行匹配规避。

---

**项目结构总览**：

```
minigrep/
├── Cargo.toml
├── src/
│   ├── main.rs      # 入口、参数、错误 exit
│   └── lib.rs       # Config, run, search, tests
└── tests/           # 集成测试（可选）
```

**掌握点**：CLI → 模块拆分 → `Result`/`?` → 单元测试 → 环境变量 → stdout/stderr 分离 → 迭代器 idioms。
