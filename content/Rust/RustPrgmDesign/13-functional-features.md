+++
title = "13-函数式语言特性：迭代器与闭包"
date = 2026-07-28T14:49:00+08:00
weight = 130
type = "docs"
description = "闭包捕获环境、Fn trait、惰性迭代器与零成本抽象精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第13章

# 函数式语言特性：迭代器与闭包

本章核心：**闭包**（存变量、捕获环境）+ **迭代器**（惰性序列处理）。

## 闭包

### 捕获环境

- 闭包 = 匿名函数，可捕获定义处作用域的值。
- 典型：`Option::unwrap_or_else(|| self.most_stocked())` — 闭包捕获 `self` 不可变引用，标准库无需了解你的类型。

### 推断和注解闭包类型

- 闭包通常**不需**显式参数/返回类型注解（编译器推断）。
- 首次调用后类型**锁定**；混用不同类型会编译错误。
- 语法对比：

```rust
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

- 单表达式可省略 `{}`；调用后才推断类型（类似 `Vec::new()` 需后续赋值推断）。

### 捕获引用或移动所有权

| 捕获方式 | 触发条件 | 示例 |
|---------|---------|------|
| 不可变借用 | 只读 | `\|list\| println!("{:?}", list)` |
| 可变借用 | 修改 | `\|list\| list.push(7)` |
| 移动所有权 | `move` 关键字 | 传给新线程时强制 move |

- `move` 闭包：即使只需不可变引用，也强制取得所有权（线程安全需要）。

### 将捕获的值移出闭包

三个 **Fn trait**（决定闭包可被如何使用）：

| Trait | 条件 | 调用次数 |
|-------|------|---------|
| `FnOnce` | 可能移出捕获值 | ≥1（所有闭包都实现） |
| `FnMut` | 可能修改捕获值，不移出 | 多次 |
| `Fn` | 不修改、不移出、不捕获 | 多次 |

- `unwrap_or_else` 约束 `FnOnce()` — 最多调用一次。
- `sort_by_key` 约束 `FnMut` — 对每个元素调用一次。
- 不需捕获环境时，可传函数名（如 `Vec::new`）代替闭包。

## 使用迭代器处理元素序列

### `Iterator` trait 和 `next` 方法

```rust
pub trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

- 迭代器**惰性**：创建时不执行，消费时才工作。
- 三种创建方式：`iter()`（`&T`）、`iter_mut()`（`&mut T`）、`into_iter()`（所有权）。
- 直接调用 `next` 需 `mut`；`for` 循环自动获取所有权并变 mut。

### 消费适配器

- **消费适配器**：获取迭代器所有权并耗尽它（如 `sum`、`collect`）。
- `sum` 后不能再使用迭代器。

### 产生其他迭代器的方法

- **迭代器适配器**：返回新迭代器，不消耗原迭代器（如 `map`、`filter`）。
- 适配器也是惰性的 — 必须调用消费适配器（如 `collect`）才执行。

```rust
let v1: Vec<i32> = vec![1, 2, 3];
let v2: Vec<_> = v1.iter().map(|x| x + 1).collect();
```

### 使用捕获其环境的闭包

- `filter(|s| s.size == shoe_size)` — 闭包捕获环境中的变量。

## 改进 I/O 项目

### 使用迭代器消除 `clone`

- `Config::build` 改为接收 `impl Iterator<Item = String>`，用 `next()` 取代索引 + `clone`。
- `env::args()` 直接传入，用 `move` 取得所有权。

### 使用迭代器适配器简化代码

```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    contents
        .lines()
        .filter(|line| line.contains(query))
        .collect()
}
```

- 无中间可变 `results` vector；更易并行化。

### 在循环和迭代器之间选择

- Rust 社区倾向迭代器风格 — 关注高层意图，抽象掉样板代码。
- 性能见下一节。

## 性能：循环 VS 迭代器

- 基准测试：`for` 循环 vs 迭代器版本性能**相近**。
- 迭代器是 Rust **零成本抽象**之一 — 编译结果与手写底层代码大致相同。
- 循环展开、边界检查消除等优化同样生效。

## 总结

闭包 + 迭代器 = 高层表达 + 低层性能。放心使用，无运行时开销。
