+++
title = "04-别名"
date = 2026-08-20T21:20:00+08:00
weight = 30
type = "docs"
description = "别名 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/types/alias.html](https://doc.rust-lang.org/stable/rust-by-example/types/alias.html)

# 别名

​	可以用 `type` 语句给已有的类型取个新的名字。类型的名字必须遵循驼峰命名法（像是
 `CamelCase` 这样），否则编译器将给出警告。原生类型是例外，比如：
 `usize`、`f32`，等等。

```rust
// `NanoSecond` 是 `u64` 的新名字。
type NanoSecond = u64;
type Inch = u64;

// 通过这个属性屏蔽警告。
#[allow(non_camel_case_types)]
type u64_t = u64;
// 试一试 ^ 移除上面那个属性

fn main() {
    // `NanoSecond` = `Inch` = `u64_t` = `u64`.
    let nanoseconds: NanoSecond = 5 as u64_t;
    let inches: Inch = 2 as u64_t;

    // 注意类型别名*并不能*提供额外的类型安全，因为别名*并不是*新的类型。
    println!("{} nanoseconds + {} inches = {} unit?",
             nanoseconds,
             inches,
             nanoseconds + inches);//5 nanoseconds + 2 inches = 7 unit?
}
```
​	别名的主要用途是避免写出冗长的模板化代码（boilerplate code）。如 `IoResult<T>`
 是 `Result<T, IoError>` 类型的别名。

> `#[allow(non_camel_case_types)]` 是一个**给 lint（编译器静态检查）降级的属性**：它告诉编译器"这条命名规范检查，在这个 item 上跳过，不要警告"。和你之前见过的 `#[allow(dead_code)]`、`#[allow(unused_variables)]` 是同一套机制，只是针对的检查项不同。
>
> **这个 lint 在检查什么?**
>
> ​	`non_camel_case_types` 检查的是**类型名称的命名规范**。Rust 的命名约定（RFC 430 风格指南）：
>
> | 类别                                              | 约定                     | 例子                     |
> | ------------------------------------------------- | ------------------------ | ------------------------ |
> | 类型（结构体、枚举、trait、**类型别名**、联合体） | UpperCamelCase（大驼峰） | `Person`、`HttpResponse` |
> | 变量 / 函数                                       | snake_case（小写下划线） | `user_name`、`get_data`  |
>
> ​	代码里 `type u64_t = u64;` 是 **snake_case** 命名一个类型，违反了约定，所以默认会触发警告。
>
> **为什么教程故意这么写?**
>
> ​	`u64_t` 是 **C 语言风格**的命名（C 里 `typedef` 常用 `_t` 后缀，如 `size_t`、`uint64_t`），教程用它来演示"Rust 会检查命名规范"这件事。
>
> ​	如果移除上面那个属性，编译时会看到这样的警告（**只是警告，程序照常运行**）：
>
> ```bash
> warning: type `u64_t` should have an upper camel case name
>  --> src/main.rs:7:6
>   |
> 7 | type u64_t = u64;
>   |      ^^^^^ help: convert the identifier to upper camel case: `U64T`
>   |
>   = note: `#[warn(non_camel_case_types)]` (part of `#[warn(nonstandard_style)]`) on by default
> ```
>
> **属性本身的作用域细节**
>
> ​	这里用的是**外层属性 `#[...]`**，只对它**后面紧跟的那一个 item**（`type u64_t = u64;` 这一行）生效：
>
> ```rust
> #[allow(non_camel_case_types)]
> type u64_t = u64;    // ✓ 这条不警告
> 
> type another_t = u64; // ✗ 没有属性保护，照样警告
> ```
>
> ​	如果写成 `#![allow(non_camel_case_types)]` 放在文件顶部，则对整个 `crate` 生效（呼应你之前问的内层/外层属性区别）。
>
> **什么时候真的需要它?**
>
> ​	正常写 Rust 代码不该需要它——好代码应该遵守命名规范。真正合理的场景是：
>
> 1. **FFI / 对接 C 代码**：C 头文件里到处是 `u_int8_t`、`time_t` 这类 snake_case 类型，用 Rust 重写绑定想保持名字一致便于对照时，局部 allow 一下。
>
> 2. **绑定第三方库的既有 API**：不想改名的历史包袱。
>
>    这两种情况下，用**局部属性**（只压在出问题的 item 上）比全文件关闭更负责任——检查范围越小，越不容易漏掉真正的命名问题。
>
> **现代替代写法**
>
> ​	除了属性，还有两种等效的配置方式：
>
> ```toml
> # Cargo.toml（Rust 1.74+ 支持 [lints] 表）
> [lints.rust]
> non_camel_case_types = "allow"
> ```
>
> ​	或命令行编译时传 `-A non_camel_case_types`。
>
> **顺带把这段代码的上下文补全**
>
> ​	`type NanoSecond = u64;` 这类是**类型别名**，本质是**同义词，不是新类型**——所以 `nanoseconds + inches` 能直接相加（`NanoSecond` 和 `Inch` 底层都是 `u64`，编译器看不出区别）。这也正是教程注释说的"别名并不能提供额外的类型安全"：如果真想区分"纳秒"和"英寸"并禁止混加，需要的是**元组结构体**（`struct NanoSecond(u64);`），那就是另一个话题了。

### 参见: {#参见}

[属性](../attribute/)
