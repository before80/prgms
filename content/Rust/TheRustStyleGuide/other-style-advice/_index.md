+++
title = "第5章 其他风格建议"
date = 2026-08-18T22:00:00+08:00
weight = 60
type = "docs"
description = "其他风格建议 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/advice.html](https://doc.rust-lang.org/nightly/style-guide/advice.html)

# 其他风格建议

## 表达式 {#expressions}

尽量利用 Rust 以表达式为中心的特性；

```rust
// 使用
let x = if y { 1 } else { 0 };
// 而不是
let x;
if y {
    x = 1;
} else {
    x = 0;
}
```

## 名称 {#names}

- 类型应为 `UpperCamelCase`，
- 枚举变体应为 `UpperCamelCase`，
- 结构体字段应为 `snake_case`，
- 函数与方法名应为 `snake_case`，
- 局部变量应为 `snake_case`，
- 宏名称应为 `snake_case`，
- 常量（`const` 以及不可变 `static`）应为 `SCREAMING_SNAKE_CASE`。
- 若名称因是保留字而被禁止（例如 `crate`），
  要么使用原始标识符（`r#crate`），要么使用尾随下划线
  （`crate_`）。不要故意拼错该词（`krate`）。

### 模块 {#modules}

尽量避免使用 `#[path]` 注解。
