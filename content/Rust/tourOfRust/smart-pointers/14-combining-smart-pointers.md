+++
title = "14-组合智能指针"
date = 2026-08-17T22:00:00+08:00
weight = 105
type = "docs"
description = "组合智能指针 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/103_zh-cn.html](https://tourofrust.com/103_zh-cn.html)

# 组合智能指针

智能指针看起来可能会存在一些限制，但是我们可以做一些非常有用的结合。     

`Rc<Vec<Foo>>` - 允许克隆多个可以借用堆上不可变数据结构的相同向量的智能指针。    

`Rc<RefCell<Foo>>` - 允许多个智能指针可变/不可变地借用相同的结构`Foo`     

`Arc<Mutex<Foo>>` - 允许多个智能指针以 CPU 线程独占方式锁定临时可变/不可变借用的能力。     

内存细节：   
* 您会注意到一个包含许多这些组合的主题。  使用不可变数据类型（可能由多个智能指针拥有）来修改内部数据。
 这在 Rust 中被称为“内部可变性”模式。 这种模式让我们可以在运行时以与 Rust 的编译时检查相同的安全级别来改变内存使用规则。

## 示例代码

```rust
use std::cell::RefCell;
use std::rc::Rc;

struct Pie {
    slices: u8,
}

impl Pie {
    fn eat_slice(&mut self, name: &str) {
        println!("{} took a slice!", name);
        self.slices -= 1;
    }
}

struct SeaCreature {
    name: String,
    pie: Rc<RefCell<Pie>>,
}

impl SeaCreature {
    fn eat(&self) {
        // use smart pointer to pie for a mutable borrow
        let mut p = self.pie.borrow_mut();
        // take a bite!
        p.eat_slice(&self.name);
    }
}

fn main() {
    let pie = Rc::new(RefCell::new(Pie { slices: 8 }));
    // ferris and sarah are given clones of smart pointer to pie
    let ferris = SeaCreature {
        name: String::from("ferris"),
        pie: pie.clone(),
    };
    let sarah = SeaCreature {
        name: String::from("sarah"),
        pie: pie.clone(),
    };
    ferris.eat();
    sarah.eat();

    let p = pie.borrow();
    println!("{} slices left", p.slices);
}
```
