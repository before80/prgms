+++
title = "18-Rust性能优化todo"
date = 2026-07-28T14:49:00+08:00
weight = 180
type = "docs"
description = "move 优化、边界检查与过早优化等性能要点精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「Rust 性能优化」

# Rust 性能优化

本章仅提炼源码中**已有正文**（非 TODO 占位）。完整专题见 `shengJing/_src/src/profiling/`。

## Copy 与 move 基础

实现 `Copy` 的类型赋值时**复制值**；未实现 `Copy` 的类型则**转移所有权**：

```rust
let x = 1;
let y = x;           // Copy，x 仍可用
println!("{x}");

let s = "aaa".to_string();
let s1 = s;          // move，s 不可用
// println!("{s}");  // 编译错误
```

堆上数据 move 通常只复制指针；性能极高。

## move 时的「深拷贝」假象

大数组在**栈上**的结构体 move 时，若用 `println!` 打印内部地址，可能看到地址变化——看似深拷贝，实为**栈复制** + 观测阻止优化：

```rust
struct LargeArray { a: [i128; 10000] }

impl LargeArray {
    fn transfer(mut self) -> Self {
        println!("{:?}", &mut self.a[1] as *mut i128);
        self.a[1] += 23;
        self
    }
}
// 三次 println 可能输出三个不同地址
```

**原因链**：

1. `[i128; 10000]` 在栈上 → move = 整段栈复制
2. 无 `println` 时，编译器可**消除**多余 move 复制（见汇编对比）
3. `println!` 读取中间状态 → 优化失效 → 复制发生

**实践**：

- 优先 `&mut self`，避免不必要所有权转移
- 大结构用 `Box<[T; N]>` 放堆上，move 只复制指针
- 或信任编译器优化，避免在 hot path 观测中间地址

## 糟糕的提前优化

Rust + LLVM 会内联并消除多余函数调用。**合理分层 ≠ 性能损失**；先写清晰代码，再 profile 定位热点。

## Clone 与 Copy

- `Copy`：栈上浅拷贝，编译器自动复制
- `Clone`：可能堆分配与深拷贝；热点路径应减少 `clone()`

派生 `Copy` 要求所有字段均为 `Copy`；`Clone` 同理递归。

## 减少 runtime 检查

### 边界检查

```rust
// 索引循环 — 每次 bounds check
for i in 0..collection.len() {
    let item = collection[i];
}

// 迭代 — 编译期可证明合法，通常无 bounds check
for item in collection { /* ... */ }
```

优先 `for item in iter`、迭代器链式操作；必要时用 `get_unchecked`（需 `unsafe` 并自证安全）。

## 待补专题（源码 TODO）

以下小节在源仓库尚未成文，详见 `shengJing/_src/src/profiling/`：

- 内存布局、分配器、CPU 缓存、Enum 优化
- 计算性能、堆栈、profiling 工具链
- LLVM、编译速度优化
