+++
title = "3.9 Drop 检查"
date = 2026-08-06T17:08:00+08:00
weight = 19
type = "docs"
description = "dropck 与逃逸舱口"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Drop 检查


> 原文链接: [https://doc.rust-lang.org/nomicon/dropck.html](https://doc.rust-lang.org/nomicon/dropck.html)


　　我们已经看到生命周期如何提供相当简单的规则，确保我们从不读取悬垂引用。但到目前为止，我们仅以包含方式与 _outlives_ 关系交互。也就是说，当谈到 `'a: 'b` 时，`'a` 与 `'b` *恰好*一样长是可以的。乍看之下，这似乎是毫无意义的区分——没有任何东西会与另一个同时被 drop，对吧？因此我们使用了 `let` 语句的如下脱糖：

```rust,ignore
let x;
let y;
```

　　脱糖为：

```rust,ignore
{
    let x;
    {
        let y;
    }
}
```

　　有些更复杂的情况无法用作用域脱糖，但顺序仍有定义——变量按定义顺序的逆序 drop，结构体和元组的字段按定义顺序 drop。关于 drop 顺序的更多细节见 [RFC 1857][rfc1857]。

　　我们做这个：

```rust,ignore
let tuple = (vec![], vec![]);
```

　　左侧 vector 先被 drop。但在借用检查器看来，右侧是否严格 outlive 左侧？答案是否。借用检查器本可以分别追踪元组各字段，但在 vector 元素等情形下仍无法决定 outlives 关系——元素通过纯库代码手动 drop，借用检查器不理解。

　　我们为何在意？因为若类型系统不够谨慎，可能意外制造悬垂指针。考虑下面简单程序：

```rust
struct Inspector<'a>(&'a u8);

struct World<'a> {
    inspector: Option<Inspector<'a>>,
    days: Box<u8>,
}

fn main() {
    let mut world = World {
        inspector: None,
        days: Box::new(1),
    };
    world.inspector = Some(Inspector(&world.days));
}
```

　　此程序完全 sound 且今天能编译。`days` 不严格 outlive `inspector` 无关紧要。只要 `inspector` 存活，`days` 就存活。

　　但若加上析构函数，程序就不再编译！

```rust,compile_fail
struct Inspector<'a>(&'a u8);

impl<'a> Drop for Inspector<'a> {
    fn drop(&mut self) {
        println!("I was only {} days from retirement!", self.0);
    }
}

struct World<'a> {
    inspector: Option<Inspector<'a>>,
    days: Box<u8>,
}

fn main() {
    let mut world = World {
        inspector: None,
        days: Box::new(1),
    };
    world.inspector = Some(Inspector(&world.days));
    // 假设 `days` 先被 drop。
    // 则 Inspector 被 drop 时会尝试读取已释放的内存！
}
```

```text
error[E0597]: `world.days` does not live long enough
  --> src/main.rs:19:38
   |
19 |     world.inspector = Some(Inspector(&world.days));
   |                                      ^^^^^^^^^^^ borrowed value does not live long enough
...
22 | }
   | -
   | |
   | `world.days` dropped here while still borrowed
   | borrow might be used here, when `world` is dropped and runs the destructor for type `World<'_>`
```

　　你可以尝试改变字段顺序或用元组代替结构体，仍然无法编译。

　　实现 `Drop` 让 `Inspector` 在销毁时执行任意代码。
　　这意味着它可能观察到本应与其同寿的类型实际上已被先销毁。

　　有趣的是，只有泛型类型需要担心这一点。若非泛型，它们能容纳的生命周期只有 `'static`，那才真正 _forever_ 存活。因此该问题称为 _sound generic drop_（健全的泛型 drop）。
　　健全的泛型 drop 由 _drop 检查器_（drop checker）强制执行。截至本文写作时，drop 检查器（亦称 dropck）如何验证类型的部分细节仍悬而未决。但**大规则**正是本节一直聚焦的微妙之处：

　　**泛型类型要 sound 地实现 drop，其泛型参数必须严格 outlive 它。**

　　遵守此规则（通常）是满足借用检查器的必要条件；遵守它是 sound 的充分但非必要条件。也就是说，若你的类型遵守此规则，则 drop 它肯定是 sound 的。

　　不总是必须满足上述规则的原因是：有些 `Drop` 实现不会访问借用数据，尽管类型赋予它这种能力；或者因为我们知道具体的 drop 顺序，借用数据仍然没问题，尽管借用检查器不知道。

　　例如，上面 `Inspector` 的如下变体永远不会访问借用数据：

```rust,compile_fail
struct Inspector<'a>(&'a u8, &'static str);

impl<'a> Drop for Inspector<'a> {
    fn drop(&mut self) {
        println!("Inspector(_, {}) knows when *not* to inspect.", self.1);
    }
}

struct World<'a> {
    inspector: Option<Inspector<'a>>,
    days: Box<u8>,
}

fn main() {
    let mut world = World {
        inspector: None,
        days: Box::new(1),
    };
    world.inspector = Some(Inspector(&world.days, "gadget"));
    // 假设 `days` 先被 drop。
    // 即使 Inspector 被 drop，其析构函数也不会访问借用的 `days`。
}
```

　　同样，此变体也永远不会访问借用数据：

```rust,compile_fail
struct Inspector<T>(T, &'static str);

impl<T> Drop for Inspector<T> {
    fn drop(&mut self) {
        println!("Inspector(_, {}) knows when *not* to inspect.", self.1);
    }
}

struct World<T> {
    inspector: Option<Inspector<T>>,
    days: Box<u8>,
}

fn main() {
    let mut world = World {
        inspector: None,
        days: Box::new(1),
    };
    world.inspector = Some(Inspector(&world.days, "gadget"));
    // 假设 `days` 先被 drop。
    // 即使 Inspector 被 drop，其析构函数也不会访问借用的 `days`。
}
```

　　然而，上述*两种*变体在分析 `fn main` 时都被借用检查器拒绝，说 `days` 不够长。

　　原因是 `main` 的借用检查分析不知道每个 `Inspector` 的 `Drop` 实现内部细节。就借用检查器分析 `main` 时所知，inspector 析构函数体可能访问那些借用数据。

　　因此，drop 检查器强制值中所有借用数据严格 outlive 该值。

## 逃逸舱口

　　支配 drop 检查的精确规则未来可能不那么严格。

　　当前分析故意保守：强制值中所有借用数据 outlive 该值，这无疑是 sound 的。

　　未来语言版本可能使分析更精确，
　　减少 sound 代码被误判为 unsafe 的情况。
　　这有助于处理上面两个在销毁时知道不检查的 `Inspector` 等情况。

　　与此同时，有一个 unstable 属性可（unsafely）断言泛型类型的析构函数*保证*不会访问任何已过期数据，即使类型赋予它这种能力。

　　该属性叫 `may_dangle`，在 [RFC 1327][rfc1327] 中引入。
　　在上面的 `Inspector` 上使用，可写成：

```rust
#![feature(dropck_eyepatch)]

struct Inspector<'a>(&'a u8, &'static str);

unsafe impl<#[may_dangle] 'a> Drop for Inspector<'a> {
    fn drop(&mut self) {
        println!("Inspector(_, {}) knows when *not* to inspect.", self.1);
    }
}

struct World<'a> {
    days: Box<u8>,
    inspector: Option<Inspector<'a>>,
}

fn main() {
    let mut world = World {
        inspector: None,
        days: Box::new(1),
    };
    world.inspector = Some(Inspector(&world.days, "gadget"));
}
```

　　使用此属性要求 `Drop` impl 标记为 `unsafe`，因为编译器不检查隐式断言：不访问可能已过期的数据（例如上面的 `self.0`）。

　　该属性可应用于任意数量的生命周期和类型参数。
　　下例中，我们断言不访问 `'b` 引用背后的数据，`T` 的用法只有 move 或 drop，但 `'a` 和 `U` 不加属性，因为确实访问了该生命周期和类型的数据：

```rust
#![feature(dropck_eyepatch)]
use std::fmt::Display;

struct Inspector<'a, 'b, T, U: Display>(&'a u8, &'b u8, T, U);

unsafe impl<'a, #[may_dangle] 'b, #[may_dangle] T, U: Display> Drop for Inspector<'a, 'b, T, U> {
    fn drop(&mut self) {
        println!("Inspector({}, _, _, {})", self.0, self.3);
    }
}
```

　　有时显然不会发生此类访问，如上面的情况。
　　但处理泛型类型参数时，可能间接发生。此类间接访问包括：

- 调用回调，
- 通过 trait 方法调用。

　　（语言的未来变更，如 impl specialization，可能增加其他间接访问途径。）

　　调用回调的例子：

```rust
struct Inspector<T>(T, &'static str, Box<for <'r> fn(&'r T) -> String>);

impl<T> Drop for Inspector<T> {
    fn drop(&mut self) {
        // `self.2` 调用可能访问借用，例如 `T` 为 `&'a _` 时
        println!("Inspector({}, {}) unwittingly inspects expired data.",
                 (self.2)(&self.0), self.1);
    }
}
```

　　trait 方法调用的例子：

```rust
use std::fmt;

struct Inspector<T: fmt::Display>(T, &'static str);

impl<T: fmt::Display> Drop for Inspector<T> {
    fn drop(&mut self) {
        // 下面有对 `<T as Display>::fmt` 的隐藏调用，
        // 可能访问借用，例如 `T` 为 `&'a _` 时
        println!("Inspector({}, {}) unwittingly inspects expired data.",
                 self.0, self.1);
    }
}
```

　　当然，所有这些访问也可能在析构函数调用的其他方法中进一步隐藏，而非直接写在析构函数里。

　　在上述析构函数访问 `&'a u8` 的所有情况中，添加 `#[may_dangle]`
　　属性会使类型易受借用检查器抓不住的误用，招致灾难。最好避免添加该属性。

## 关于 drop 顺序的相关旁注

　　虽然结构体内部字段的 drop 顺序有定义，依赖它脆弱且微妙。当顺序重要时，最好用 [`ManuallyDrop`] 包装器。

## 这就是 drop 检查器的全部吗？

　　事实证明，写 unsafe 代码时，我们一般完全不必为 drop 检查器操心。但有一个特殊情况需要注意，下一节会讲。

[rfc1327]: https://github.com/rust-lang/rfcs/blob/master/text/1327-dropck-param-eyepatch.md
[rfc1857]: https://github.com/rust-lang/rfcs/blob/master/text/1857-stabilize-drop-order.md
[`manuallydrop`]: ../std/mem/struct.ManuallyDrop.html
