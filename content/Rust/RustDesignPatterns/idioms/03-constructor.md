+++
title = "03-构造器"
date = 2026-08-18T22:10:00+08:00
weight = 7
type = "docs"
description = "构造器 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/ctor.html](https://rust-unofficial.github.io/patterns/idioms/ctor.html)

# 构造器

## 描述 {#description}

Rust 没有作为语言构造的构造器。约定是使用[关联函数][associated function] `new` 来创建对象：

````rust
/// 以秒计的时间。
///
/// # 示例
///
/// ```
/// let s = Second::new(42);
/// assert_eq!(42, s.value());
/// ```
pub struct Second {
    value: u64,
}

impl Second {
    // 构造 [`Second`] 的新实例。
    // 注意这是关联函数——没有 self。
    pub fn new(value: u64) -> Self {
        Self { value }
    }

    /// 返回以秒为单位的值。
    pub fn value(&self) -> u64 {
        self.value
    }
}
````

## 默认构造器 {#default-constructors}

Rust 通过 [`Default`][std-default] trait 支持默认构造器：

````rust
/// 以秒计的时间。
///
/// # 示例
///
/// ```
/// let s = Second::default();
/// assert_eq!(0, s.value());
/// ```
pub struct Second {
    value: u64,
}

impl Second {
    /// 返回以秒为单位的值。
    pub fn value(&self) -> u64 {
        self.value
    }
}

impl Default for Second {
    fn default() -> Self {
        Self { value: 0 }
    }
}
````

若所有字段的类型都实现了 `Default`，也可以派生 `Default`，
`Second` 就是这种情况：

````rust
/// 以秒计的时间。
///
/// # 示例
///
/// ```
/// let s = Second::default();
/// assert_eq!(0, s.value());
/// ```
#[derive(Default)]
pub struct Second {
    value: u64,
}

impl Second {
    /// 返回以秒为单位的值。
    pub fn value(&self) -> u64 {
        self.value
    }
}
````

**注意：** 类型同时实现 `Default` 和无参 `new` 构造器是常见且符合预期的。
`new` 是 Rust 中的构造器约定，用户期望它存在，因此如果基本构造器不接受参数是合理的，
那就应当提供它，即便它在功能上与 default 完全相同。

**提示：** 实现或派生 `Default` 的好处是，你的类型现在可以用在需要 `Default` 实现的地方，
最突出的是[标准库中任何 `*or_default` 函数][std-or-default]。

## 参见 {#see-also}

- [Default 惯用法](04-the-default-trait/) 对 `Default` trait 有更深入的说明。

- [构建器模式](../design-patterns/02-creational/01-builder/) 用于在存在多种配置时构造对象。

- [Rust API 指南 / C-COMMON-TRAITS][API Guidelines/C-COMMON-TRAITS] 关于
  同时实现 `Default` 和 `new`。

[associated function]: https://doc.rust-lang.org/stable/book/ch05-03-method-syntax.html#associated-functions
[std-default]: https://doc.rust-lang.org/stable/std/default/trait.Default.html
[std-or-default]: https://doc.rust-lang.org/stable/std/?search=or_default
[API Guidelines/C-COMMON-TRAITS]: https://rust-lang.github.io/api-guidelines/interoperability.html#types-eagerly-implement-common-traits-c-common-traits
