+++
title = "05-Cell and RefCell"
date = 2026-08-12T20:00:00+08:00
weight = 64
type = "docs"
description = "Cell and RefCell — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/smart-pointers/cell-refcell.html](https://practice-rust.beatai.org/smart-pointers/cell-refcell.html)

# Cell and RefCell

`Cell<T>` 和 `RefCell<T>` 提供内部可变性：在不可变引用存在时也能修改数据。`RefCell` 在运行时检查借用规则。

1. 🌟
```rust
// 让代码工作
use std::cell::Cell;

fn main() {
    let c = Cell::new(5);
    c.set(10);
    assert_eq!(c.get(), 10);
    println!("Success!");
}
```

2. 🌟
```rust
// 让代码工作
use std::cell::RefCell;

fn main() {
    let data = RefCell::new(5);
    {
        let mut r = data.borrow_mut();
        *r += 1;
    }
    assert_eq!(*data.borrow(), 6);
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 让代码工作
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(i32, RefCell<Rc<List>>),
    Nil,
}

use List::{Cons, Nil};

fn main() {
    let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));
    let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));

    if let Some(link) = Rc::into_inner(a) {
        if let Cons(_, ref next) = link {
            *next.borrow_mut() = Rc::clone(&b);
        }
    }

    println!("Success!");
}
```

4. 🌟🌟
```rust
// 填空
use std::cell::RefCell;

fn main() {
    let s = RefCell::new(String::from("hello"));
    s.borrow_mut().push_str(", world");
    assert_eq!(s.borrow().as_str(), __);
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
