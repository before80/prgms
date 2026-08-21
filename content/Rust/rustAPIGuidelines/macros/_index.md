+++
title = "第3章 宏"
date = 2026-08-18T21:50:00+08:00
weight = 50
type = "docs"
description = "宏 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/macros.html](https://rust-lang.github.io/api-guidelines/macros.html)

# 宏

## 输入语法能让人联想到输出 (C-EVOCATIVE) {#c-evocative}

Rust 宏几乎允许你构想任意输入语法。目标是通过尽可能镜像已有的 Rust 语法，使输入语法对用户其余代码
保持熟悉且内聚。注意关键字与标点的选择和位置。

一个好的指导原则是：使用与宏输出中将要产生的内容相似的语法，尤其是关键字与标点。

例如，若你的宏用输入中给定的名称声明一个结构体，请在该名称前加上关键字 `struct`，以向读者表明
正在用给定名称声明一个结构体。

```rust
// 优先这样...
bitflags! {
    struct S: u32 { /* ... */ }
}

// ...而不是没有关键字...
bitflags! {
    S: u32 { /* ... */ }
}

// ...或某个临时词。
bitflags! {
    flags S: u32 { /* ... */ }
}
```

另一个例子是分号与逗号。Rust 中常量后跟分号，因此若你的宏声明一串常量，即便语法在其他方面与
Rust 略有不同，它们也很可能应后跟分号。

```rust
// 普通常量使用分号。
const A: u32 = 0b000001;
const B: u32 = 0b000010;

// 因此优先这样...
bitflags! {
    struct S: u32 {
        const C = 0b000100;
        const D = 0b001000;
    }
}

// ...而不是这样。
bitflags! {
    struct S: u32 {
        const E = 0b010000,
        const F = 0b100000,
    }
}
```

宏如此多样，这些具体例子未必相关，但请思考如何将相同原则应用到你的情形中。

## 项宏与属性良好组合 (C-MACRO-ATTR) {#c-macro-attr}

产生多个输出项的宏应支持向其中任一项添加属性。一个常见用例是将个别项放在 cfg 之后。

```rust
bitflags! {
    struct Flags: u8 {
        #[cfg(windows)]
        const ControlCenter = 0b001;
        #[cfg(unix)]
        const Terminal = 0b010;
    }
}
```

输出为结构体或枚举的宏应支持属性，以便输出能与 derive 一起使用。

```rust
bitflags! {
    #[derive(Default, Serialize)]
    struct Flags: u8 {
        const ControlCenter = 0b001;
        const Terminal = 0b010;
    }
}
```

## 项宏在任何允许项的地方都能工作 (C-ANYWHERE) {#c-anywhere}

Rust 允许将项放在模块级，或放在更紧的作用域（如函数）内。项宏应在所有这些地方与普通项同样良好工作。
测试套件应至少包含在模块作用域与函数作用域中对该宏的调用。

```rust
#[cfg(test)]
mod tests {
    test_your_macro_in_a!(module);

    #[test]
    fn anywhere() {
        test_your_macro_in_a!(function);
    }
}
```

作为一个简单例子说明可能出错之处：下面这个宏在模块作用域中工作得很好，但在函数作用域中会失败。

```rust
macro_rules! broken {
    ($m:ident :: $t:ident) => {
        pub struct $t;
        pub mod $m {
            pub use super::$t;
        }
    }
}

broken!(m::T); // 可以，展开为 T 与 m::T

fn g() {
    broken!(m::U); // 无法编译，super::U 指向包含模块而非 g
}
```

## 项宏支持可见性说明符 (C-MACRO-VIS) {#c-macro-vis}

遵循 Rust 关于宏所产生项可见性的语法。默认私有；若指定了 `pub` 则为公开。

```rust
bitflags! {
    struct PrivateFlags: u8 {
        const A = 0b0001;
        const B = 0b0010;
    }
}

bitflags! {
    pub struct PublicFlags: u8 {
        const C = 0b0100;
        const D = 0b1000;
    }
}
```

## 类型片段足够灵活 (C-MACRO-TY) {#c-macro-ty}

若你的宏在输入中接受像 `$t:ty` 这样的类型片段，它应能与下列全部一起使用：

- 原始类型：`u8`、`&str`
- 相对路径：`m::Data`
- 绝对路径：`::base::Data`
- 向上相对路径：`super::Data`
- 泛型：`Vec<String>`

作为一个简单例子说明可能出错之处：下面这个宏对原始类型与绝对路径工作得很好，但对相对路径会失败。

```rust
macro_rules! broken {
    ($m:ident => $t:ty) => {
        pub mod $m {
            pub struct Wrapper($t);
        }
    }
}

broken!(a => u8); // 可以

broken!(b => ::std::marker::PhantomData<()>); // 可以

struct S;
broken!(c => S); // 无法编译
```
