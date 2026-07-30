+++
title = "12-一个IO项目：构建命令行程序"
date = 2026-07-28T14:49:00+08:00
weight = 120
type = "docs"
description = "minigrep 项目：CLI 参数、文件 IO、重构、TDD 与环境变量"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第12章

# 一个 I/O 项目：构建命令行程序

综合第 7–11 章：实现简化版 **grep**（`minigrep`）— 在文件中搜索字符串并打印匹配行。

```console
cargo new minigrep
cargo run -- searchstring example-filename.txt
```

## 接受命令行参数

### 读取参数值

```rust
use std::env;

let args: Vec<String> = env::args().collect();
// args[0] = 程序名；args[1] = query；args[2] = file_path
```

- `env::args()`：无效 Unicode 会 panic；用 `args_os` + `OsString` 可接受。
- `collect` 需类型注解：`Vec<String>`。

### 将参数值保存进变量

```rust
let query = &args[1];
let file_path = &args[2];
```

## 读取文件

```rust
use std::fs;

let contents = fs::read_to_string(file_path)?;
// 返回 Result<String, io::Error>
```

## 重构改进模块性和错误处理

### 二进制项目的关注分离

| 文件 | 职责 |
|------|------|
| `main.rs` | 解析参数、配置、`run()`、错误退出 |
| `lib.rs` | 核心逻辑（可测试） |

流程：拆 `main` + `lib` → 参数解析可留 main 或移 lib → main 仅 orchestration。

### 组合配置值

```rust
struct Config {
    query: String,
    file_path: String,
}
```

- 配置与执行逻辑分离；`String` 所有权用 `.clone()` 从 `args` 取得（初版可接受）。

### 创建 `Config` 的构造函数

```rust
impl Config {
    fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }
        Ok(Config {
            query: args[1].clone(),
            file_path: args[2].clone(),
        })
    }
}
```

- `build` 而非 `new`：表示可能失败。

#### 返回 `Result` 而不是调用 `panic!`

- 用户错误 → `Result`；程序 bug → `panic!`。

#### 调用 `Config::build` 并处理错误

```rust
let config = Config::build(&args).unwrap_or_else(|err| {
    eprintln!("Problem parsing arguments: {err}");
    process::exit(1);
});
```

### 从 `main` 提取逻辑

```rust
fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;
    for line in search(&config.query, &contents) {
        println!("{line}");
    }
    Ok(())
}
```

- `Box<dyn Error>`：任意实现 `Error` 的错误类型。

#### 在 `main` 中处理 `run` 返回的错误

```rust
if let Err(e) = run(config) {
    eprintln!("Application error: {e}");
    process::exit(1);
}
```

### 将代码拆分到库 crate

```rust
// src/lib.rs
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> { /* ... */ }
```

```rust
// src/main.rs
use minigrep::search;
```

## 采用测试驱动开发增加功能

**TDD**：1. 写失败测试 → 2. 写最少代码通过 → 3. 重构 → 重复。

### 编写失败测试

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn case_sensitive() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Duct tape.";
        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
}
```

### 编写使测试通过的代码

```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let mut results = Vec::new();
    for line in contents.lines() {
        if line.contains(query) {
            results.push(line);
        }
    }
    results
}
```

- 生命周期 `'a`：返回 slice 引用 **`contents`**，不是 `query`。

#### 在 `run` 函数中使用 `search` 函数

```console
cargo run -- frog poem.txt
cargo run -- body poem.txt
```

## 处理环境变量

### 大小写不敏感搜索

```rust
pub fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let query = query.to_lowercase();
    let mut results = Vec::new();
    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            results.push(line);
        }
    }
    results
}
```

- `to_lowercase()` 产生新 `String`，故 `query` 为 owned；`contains` 需 `&query`。

### 读取环境变量

```rust
let ignore_case = env::var("IGNORE_CASE").is_ok();

struct Config {
    query: String,
    file_path: String,
    ignore_case: bool,
}
```

```rust
let results = if config.ignore_case {
    search_case_insensitive(&config.query, &contents)
} else {
    search(&config.query, &contents)
};
```

```console
# Linux/macOS
IGNORE_CASE=1 cargo run -- to poem.txt

# PowerShell
$Env:IGNORE_CASE=1; cargo run -- to poem.txt
Remove-Item Env:IGNORE_CASE
```

## 将错误重定向到标准错误

- **stdout**：一般输出；**stderr**：错误信息。
- `println!` → stdout；**`eprintln!`** → stderr。

```rust
eprintln!("Problem parsing arguments: {err}");
process::exit(1);
```

```console
cargo run > output.txt              # 错误仍显示在屏幕
cargo run -- to poem.txt > output.txt  # 结果进文件，错误在屏幕
```

- 命令行程序惯例：成功输出可重定向；错误走 stderr。
