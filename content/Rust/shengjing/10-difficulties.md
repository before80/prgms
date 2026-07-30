+++
title = "10-Rust难点攻关"
date = 2026-07-28T14:49:00+08:00
weight = 100
type = "docs"
description = "切片、字符串、Eq 等等价与比较概念精要辨析"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「Rust 难点攻关」

# Rust 难点攻关

学至此处，以下概念是否说得清、用得上？

- 切片 vs 切片引用
- `String` / `str` / `&str` 等字符串类型
- 裸指针 / 引用 / 智能指针（源码待补）
- move / Copy / Clone（源码待补）
- 作用域 / 生命周期 / NLL（源码待补）

本章整理已有解读；标注「待补」的小节见源码目录 `shengJing/_src/src/difficulties/`。

## 切片和切片引用

> 前置：[切片 slice](https://beatai.org/rust-course/basic/compound-type/string-slice#切片slice)

`str`、`[T]` 均为**切片**（DST，编译期大小未知），**不能**直接作为栈上变量使用：

```rust
let string: str = "banana"; // 编译错误：size not known at compile time
```

**结论**：切片只能通过**引用**使用；口语中的「字符串切片」通常指 `&str`。

| 切片（DST） | 常用引用 |
|-------------|----------|
| `str` | `&str` |
| `[T]` | `&[T]` |

要点：

- 切片长度运行时确定 → 类型为 DST
- 切片引用是**宽指针**（指针 + 长度），大小固定，可存栈上
- 固定长度用数组：`[i8; 4]`，类型含长度，非切片

```rust
let s1: &str = "banana";
let s2: &str = &String::from("banana");
let s3: &[i32] = &[1, 2, 3, 4, 5][1..3];
```

## Eq 和 PartialEq

`==` / `!=` 需实现 `PartialEq`；`Eq` 是标记 trait（无方法），表示**所有值**均可相等。

```rust
impl PartialEq for Book {
    fn eq(&self, other: &Self) -> bool { self.isbn == other.isbn }
}
impl Eq for Book {}  // 在 PartialEq 之上默认实现
```

**Partial = 部分相等**：浮点数实现 `PartialEq` 但未实现 `Eq`，因 `NaN != NaN`：

```rust
let f1 = f32::NAN;
let f2 = f32::NAN;
assert!(f1 != f2);  // 两者均为 NaN，但不相等
```

| trait | 含义 | 典型约束 |
|-------|------|----------|
| `PartialEq` | 可比较相等 | 一般类型 |
| `Eq` | 完全相等 | `HashMap` 的 K |
| `PartialOrd` | 可部分排序 | 浮点数 |
| `Ord` | 全序 | `BTreeMap` 的 K |

## 疯狂字符串

Rust 字符串类型易混，核心对照：

| 类型 | 所有权 | 可变性 | 常见场景 |
|------|--------|--------|----------|
| `str` | — | — | DST，不可直接使用 |
| `&str` | 借用 | 否 | 字符串字面量、函数参数 |
| `String` | 有 | 是 | 堆上可增长 UTF-8 字符串 |
| `&String` | 借用 | 视内部 | 少见，通常用 `&str` 即可 |
| `Box<str>` | 有 | 否 | 固定堆上字符串 |

- `str` 是语言内置的字符串切片；`String` / `&str` 是日常说的「字符串」
- 标准库还有 `OsStr`/`OsString`、`CStr`/`CString` 等，对应 OS/FFI 场景
- `str` 硬编码进二进制；`String` 可增长、可修改

## 待补专题（见源码）

以下章节在源仓库中为占位或 TODO，完整正文待后续补充：

- 作用域、生命周期和 NLL → `difficulties/lifetime.md`
- move、Copy 和 Clone → `difficulties/move-copy.md`
- 裸指针、引用和智能指针 → `difficulties/pointer.md`
