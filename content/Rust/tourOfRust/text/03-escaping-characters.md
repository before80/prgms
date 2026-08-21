+++
title = "03-转义字符"
date = 2026-08-17T22:00:00+08:00
weight = 63
type = "docs"
description = "转义字符 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/61_zh-cn.html](https://tourofrust.com/61_zh-cn.html)

# 转义字符

有些字符难以使用可视字符表示，这时可通过**转义字符**来表示这些字符。

Rust 支持类 C 语言中的常见转义字符；

* `\n` - 换行符
* `\r` - 回车符（回到本行起始位置）
* `\t` - 水平制表符（即键盘 Tab 键）
* `\\` - 代表单个反斜杠 \
* `\0` - 空字符（null）
* `\'` - 代表单引号 '

完整的转义字符表[在这](https://doc.rust-lang.org/reference/tokens.html)。

## 示例代码

```rust
fn main() {
    let a: &'static str = "Ferris 说：\t\"你好\"";
    println!("{}",a);
}
```
