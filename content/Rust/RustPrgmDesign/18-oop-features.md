+++
title = "18-面向对象编程特性"
date = 2026-07-28T14:49:00+08:00
weight = 180
type = "docs"
description = "封装、trait 对象、动态分发与状态模式精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第18章

# 面向对象编程特性

Rust 受 OOP 影响，但无继承。本章：OOP 三特征在 Rust 中的体现 + trait 对象 + 状态模式。

## 面向对象语言的特征

### 对象包含数据和行为

- GoF 定义：对象 = 数据 + 操作数据的方法。
- Rust：`struct`/`enum` 存数据 + `impl` 块提供方法 → 功能等价（只是不叫"对象"）。

### 封装隐藏了实现细节

```rust
pub struct AveragedCollection {
    list: Vec<i32>,      // 私有
    average: f64,        // 私有
}
impl AveragedCollection {
    pub fn add(&mut self, v: i32) { /* 更新 list + average */ }
    pub fn average(&self) -> f64 { self.average }
}
```

- `pub` 控制可见性；私有字段 + 公有方法 = 封装。
- 可改内部实现（如 `Vec` → `HashSet`）而不影响外部 API。

### 作为类型系统与代码共享的继承

- Rust **无继承**（不能用宏以外的方式继承字段/方法）。
- 代码复用 → **trait 默认实现**（类似但不等同继承）。
- 运行时多态 → **trait 对象**（非继承）。

## 使用 trait object 来抽象出共享行为

### 定义通用行为的 trait

```rust
pub trait Draw { fn draw(&self); }

pub struct Screen {
    components: Vec<Box<dyn Draw>>,
}

impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();  // 动态分发
        }
    }
}
```

- `dyn Trait` = trait 对象：运行时查找方法。
- 需用指针（`&`、`Box` 等）+ `dyn` 关键字。

### 实现 trait

```rust
pub struct Button { width: u32, height: u32, label: String }
impl Draw for Button { fn draw(&self) { /* ... */ } }
// 用户 crate 可扩展：impl Draw for SelectBox { ... }
```

### trait 对象执行动态分发

| | 泛型 + trait 约束 | trait 对象 |
|--|-------------------|-----------|
| 类型 | 编译时单态化 | 运行时多类型 |
| 分发 | **静态分发** | **动态分发** |
| 集合 | 同质（全 Button 或全 TextField） | 异质（Button + SelectBox 混合） |
| 性能 | 可内联优化 | 运行时查找开销 |
| 扩展 | 编译时已知类型 | 运行时添加新类型 |

- 未实现 trait 的类型不能放入 trait 对象 → **编译时**检查（优于鸭子类型的运行时错误）。
- trait 对象不能添加数据，只抽象行为。

## 实现一个面向对象设计模式

### 尝试采用传统的面向对象风格

**状态模式**：值内含状态对象，行为随状态改变。

博文工作流：Draft → PendingReview → Published

```rust
// 传统 OO 方式
pub struct Post {
    content: String,
    state: Option<Box<dyn State>>,
}
trait State {
    fn request_review(self: Box<Self>) -> Box<dyn State>;
    fn approve(self: Box<Self>) -> Box<dyn State>;
    fn content<'a>(&self, post: &'a Post) -> &'a str { "" }
}
```

- `self: Box<Self>` — 消费旧状态，返回新状态。
- `Option::take()` — 取出 state 所有权再转换。
- `Published` 重写 `content` 返回实际文本。

缺点：状态间耦合；重复逻辑；dyn 兼容性限制（trait 中无法返回 `Self`）。

#### 将状态和行为编码为类型

**Rust 惯用方式**：用不同类型编码状态，编译时防止非法操作。

```rust
pub struct Post { content: String }           // 仅已发布
pub struct DraftPost { content: String }      // 无 content 方法
pub struct PendingReviewPost { content: String }

impl DraftPost {
    pub fn new() -> Self { /* ... */ }
    pub fn add_text(&mut self, text: &str) { /* ... */ }
    pub fn request_review(self) -> PendingReviewPost { /* ... */ }
}
impl PendingReviewPost {
    pub fn approve(self) -> Post { /* ... */ }
}
impl Post {
    pub fn content(&self) -> &str { &self.content }
}
```

- 不可能创建未发布的 `Post`。
- 草稿/审核中博文**无 `content` 方法** → 编译错误，非运行时检查。
- 状态转移 = 类型转换（消费 `self`，返回新类型）。

| 传统 OO 状态模式 | Rust 类型编码 |
|-----------------|--------------|
| 运行时检查状态 | 编译时检查类型 |
| `match`/trait 对象分发 | 不同类型不同方法集 |
| 可扩展但耦合 | 类型安全但需更多类型 |

## 总结

- Rust 有 OOP 的封装、多态（trait 对象），但**无继承**。
- `Box<dyn Trait>` = 运行时多态；泛型 = 编译时多态。
- 状态模式可用 trait 对象实现，但**类型编码状态**更符合 Rust 优势。
- 面向对象模式可用，但不总是 Rust 最优解 — 善用所有权和类型系统。
