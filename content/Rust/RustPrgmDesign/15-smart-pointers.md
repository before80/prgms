+++
title = "15-智能指针"
date = 2026-07-28T14:49:00+08:00
weight = 150
type = "docs"
description = "Box、Rc、RefCell、Deref/Drop 与引用循环精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第15章

# 智能指针

**指针** = 含内存地址的变量。**智能指针** = 类似指针 + 额外元数据/功能；通常**拥有**所指向的数据。

标准库常用：`Box<T>`、`Rc<T>`、`RefCell<T>`。智能指针实现 `Deref` 和 `Drop` trait。

## 使用 `Box<T>` 指向堆上的数据

```rust
let b = Box::new(5);
println!("b = {b}");  // 解引用同引用
```

使用场景：
1. **编译时未知大小**的类型（递归类型）
2. **大量数据**转移所有权时避免栈拷贝
3. **trait 对象**（第18章）

### Box 允许创建递归类型

- 递归类型编译时大小未知 → 用 `Box<T>` 打破无限大小（间接存储，指针大小固定）。

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

## 将智能指针视作常规引用

### 追踪引用的值

- `*y` 解引用运算符 — 追踪引用指向的值。

### 像引用一样使用 `Box<T>`

- `Box<T>` 实现了 `Deref`，可用 `*` 解引用。

### 定义我们自己的智能指针

```rust
struct MyBox<T>(T);
impl<T> Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target { &self.0 }
}
```

### 实现 `Deref` trait

- `*y` 底层 → `*(y.deref())` — 只展开一次，不会无限递归。
- `deref` 返回**引用**（不移动所有权）。

### 在函数和方法中使用 Deref 强制转换

- **Deref 强制转换**：`&T` → `&U`（当 `T: Deref<Target=U>`）。
- 例：`&MyBox<String>` → `&String` → `&str`，自动适配 `hello(name: &str)`。
- 编译时完成，无运行时开销。

### 处理可变引用的 Deref 强制转换

- `DerefMut` 重载可变引用的 `*`。
- 三种强制转换：
  1. `&T` → `&U`（`T: Deref<Target=U>`）
  2. `&mut T` → `&mut U`（`T: DerefMut<Target=U>`）
  3. `&mut T` → `&U`（`T: Deref<Target=U>`）— **不可逆**

## 使用 `Drop` Trait 运行清理代码

```rust
impl Drop for CustomSmartPointer {
    fn drop(&mut self) { println!("Dropping!"); }
}
// 变量按创建逆序自动 drop
```

- **不能**显式调用 `Drop::drop`（会 double free）。
- 提前释放：`drop(value)` — `std::mem::drop` 函数（prelude 中）。

## `Rc<T>` 引用计数智能指针

- **引用计数**：跟踪所有者数量，为 0 时清理。**仅单线程**。
- 解决多所有者共享数据（如图结构）。

```rust
enum List {
    Cons(i32, Rc<List>),
    Nil,
}
let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
let b = Cons(3, Rc::clone(&a));  // 惯例用 Rc::clone，非 a.clone()
```

- `Rc::strong_count(&a)` 查看引用计数。
- `Rc::clone` 只增计数，不深拷贝数据。

## `RefCell<T>` 和内部可变性模式

**内部可变性**：在不可变引用存在时也能修改数据（运行时借用检查）。

| 类型 | 所有者 | 借用检查 |
|------|--------|---------|
| `Box<T>` | 单一 | 编译时 |
| `Rc<T>` | 多个 | 编译时（仅不可变） |
| `RefCell<T>` | 单一 | **运行时** |

- `borrow()` → `Ref<T>`；`borrow_mut()` → `RefMut<T>`。
- 违反借用规则 → **panic**（非编译错误）。
- 典型：`Rc<RefCell<T>>` — 多所有者 + 可修改。

```rust
// Mock 测试：&self 方法内修改内部状态
sent_messages: RefCell<Vec<String>>
self.sent_messages.borrow_mut().push(String::from(msg));
```

## 引用循环与内存泄漏

- `Rc` + `RefCell` 可能形成**引用循环** → 引用计数永不为 0 → 内存泄漏（Rust 认为是内存安全的）。
- 预防：重新设计所有权关系。

### 使用 `Weak<T>` 防止引用循环

- `Rc::downgrade(&rc)` → `Weak<T>` — 不增加 strong_count，不影响清理。
- `weak.upgrade()` → `Option<Rc<T>>` — 值已丢弃则 `None`。
- 典型：树中子→父用 `Weak`，父→子用 `Rc`。

```rust
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}
```

## 总结

| 类型 | 用途 |
|------|------|
| `Box<T>` | 堆分配、递归类型、trait 对象 |
| `Rc<T>` | 单线程多所有者 |
| `RefCell<T>` | 内部可变性（运行时借用） |
| `Weak<T>` | 打破引用循环 |

`Deref`/`Drop` 是智能指针核心 trait。多线程用 `Arc<T>`/`Mutex<T>`（第16章）。
