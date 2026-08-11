+++
title = "1.3 使用 Unsafe"
date = 2026-08-06T17:08:00+08:00
weight = 5
type = "docs"
description = "编写与审阅 Unsafe 代码的实践要点"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 使用 Unsafe


> 原文链接: [https://doc.rust-lang.org/nomicon/working-with-unsafe.html](https://doc.rust-lang.org/nomicon/working-with-unsafe.html)


　　Rust 通常只给我们以有范围、二元的方式讨论 Unsafe Rust 的工具。遗憾的是，现实远比这复杂。例如看这个玩具函数：

```rust
fn index(idx: usize, arr: &[u8]) -> Option<u8> {
    if idx < arr.len() {
        unsafe {
            Some(*arr.get_unchecked(idx))
        }
    } else {
        None
    }
}
```

　　该函数安全且正确。我们检查索引在界内，若在界内则无检查地索引数组。这种正确但不安全实现的函数称为*健全（sound）*：Safe 代码不能通过它导致未定义行为（记住，这是 Safe Rust 的唯一基本性质）。

　　但在如此简单的函数里，unsafe 块的范围也值得质疑。把 `<` 改成 `<=`：

```rust
fn index(idx: usize, arr: &[u8]) -> Option<u8> {
    if idx <= arr.len() {
        unsafe {
            Some(*arr.get_unchecked(idx))
        }
    } else {
        None
    }
}
```

　　该程序现在*不健全*：Safe 代码可导致未定义行为，而我们*只改了 safe 代码*。这就是安全的根本问题：它是*非局部的*。我们 unsafe 操作的健全性必然依赖由 otherwise「safe」操作建立的状态。

　　安全在某种意义上是模块化的：选择 unsafety 不必考虑任意其他坏情况。例如无检查 slice 索引不意味着 suddenly 要担心 slice 为 null 或含未初始化内存——本质没变。但安全*并非*模块化：程序 inherently 有状态，unsafe 操作可能依赖任意其他状态。

　　当我们引入真正的持久状态时，这种非局部性更严重。看 `Vec` 的简单实现：

```rust
use std::ptr;

// 注意：此定义较 naive。见实现 Vec 一章。
pub struct Vec<T> {
    ptr: *mut T,
    len: usize,
    cap: usize,
}

// 注意：此实现未正确处理零大小类型。见实现 Vec 一章。
impl<T> Vec<T> {
    pub fn push(&mut self, elem: T) {
        if self.len == self.cap {
            // 对本例不重要
            self.reallocate();
        }
        unsafe {
            ptr::write(self.ptr.add(self.len), elem);
            self.len += 1;
        }
    }
    # fn reallocate(&mut self) { }
}

# fn main() {}
```

　　这段代码足够简单，可合理审计与非形式验证。现在加上：

```rust,ignore
fn make_room(&mut self) {
    // 增大容量
    self.cap += 1;
}
```

　　这段代码 100% 是 Safe Rust，但完全不健全。改 capacity 违反了 Vec 的不变式（`cap` 反映 Vec 中已分配空间）。Vec 其余部分无法防御。它*必须*信任 capacity 字段，因为无法验证。

　　由于它依赖结构体字段的不变式，这段 `unsafe` 代码污染的不只是一整个函数，而是整*个模块*。一般而言，限制 unsafe 代码范围唯一可靠的方式是在模块边界用 privacy。

　　然而这*完全可行*。`make_room` 的存在*不会*破坏 Vec 的健全性，因为我们未把它标为 public。只有定义该函数的模块能调用它。且 `make_room` 直接访问 Vec 的私有字段，只能写在定义 Vec 的同一模块。

　　因此我们可以写出完全 safe 的抽象，却依赖复杂不变式。这对 Safe 与 Unsafe Rust 的关系*至关重要*。

　　我们已看到 Unsafe 代码必须信任*某些* Safe 代码，但不应信任*泛型* Safe 代码。Privacy 对 unsafe 代码重要，原因类似：它避免我们必须信任宇宙中所有 safe 代码来破坏我们 trusted 的状态。

　　安全万岁！
