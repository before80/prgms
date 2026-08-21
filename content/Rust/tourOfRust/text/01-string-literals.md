+++
title = "01-字符串常量（String Literals）"
date = 2026-08-17T22:00:00+08:00
weight = 61
type = "docs"
description = "字符串常量（String Literals） — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/59_zh-cn.html](https://tourofrust.com/59_zh-cn.html)

# 字符串常量（String Literals）

字符串常量（String Literals）采用 Unicode 编码（注：下文提及的 **utf-8** 为 Unicode 的一部分）。

字符串常量的类型为 `&'static str`：

* `&` 意味着该变量为对内存中数据的引用，没有使用 `&mut` 代表编译器将不会允许对该变量的修改
* `'static` 意味着字符串数据将会一直保存到程序结束（它不会在程序运行期间被**释放（drop）**）
* `str` 意味着该变量总是指向一串合法的 **utf-8** 字节序列。


内存细节：
* Rust 编译器可能会将字符串储存在程序内存的数据段中。

## 示例代码

```rust
fn main() {
    let a: &'static str = "你好 🦀";
    println!("{} {}", a, a.len());
}
```
