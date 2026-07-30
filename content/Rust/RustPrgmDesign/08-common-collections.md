+++
title = "08-常见集合"
date = 2026-07-28T14:49:00+08:00
weight = 80
type = "docs"
description = "Vec、String 与 HashMap 的创建、访问、更新与所有权要点"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第8章

# 常见集合

集合数据在**堆**上，大小运行时可变。本章三种：**Vec**、**String**、**HashMap**。

## 使用 Vector 储存列表

`Vec<T>`：同类型、内存相邻、数量可变。

### 新建 vector

```rust
let v: Vec<i32> = Vec::new();
let v = vec![1, 2, 3];  // 宏推断类型
```

### 更新 vector

```rust
let mut v = Vec::new();
v.push(5);
v.push(6);
```

### 读取 vector 的元素

| 方式 | 越界行为 |
|------|----------|
| `&v[i]` | **panic** |
| `v.get(i)` | 返回 `Option<&T>` |

- 同一作用域不能同时持有元素引用又对 vector **push**（可能重新分配，引用失效）。

### 遍历 vector 中的元素

```rust
for i in &v { /* 不可变 */ }
for i in &mut v { *i += 50; }  // 可变需解引用
```

- 遍历中不可增删元素。

### 使用枚举来储存多种类型

```rust
enum SpreadsheetCell { Int(i32), Float(f64), Text(String) }
let row = vec![SpreadsheetCell::Int(3), ...];
```

- 运行时类型未知 → 用 trait 对象（第18章）。

### 丢弃 vector 时也会丢弃其所有元素

- vector 离开作用域，内部所有值一并 drop。

## 使用字符串储存 UTF-8 编码的文本

- **`&str`**：字符串 slice，UTF-8 引用（含字面值）。
- **`String`**：可增长、可变、可拥有、UTF-8；本质是带额外语义的 `Vec<u8>`。

### 新建字符串

```rust
let s = String::new();
let s = "initial".to_string();
let s = String::from("initial");
```

### 更新字符串

```rust
s.push_str("bar");   // 追加 &str
s.push('l');         // 追加 char
let s3 = s1 + &s2;   // s1 被 move；s2 用 &str
let s = format!("{}-{}-{}", t, u, v);  // 不取得所有权
```

- `+` 调用 `add(self, s: &str)`：`self` 被 move，第二参数为 `&str`（`&String` 可 deref  coercion）。

### 索引字符串

- **`String` 不支持 `s[i]`**（字节索引 ≠ Unicode 标量/字形簇；且无法 O(1) 保证）。

#### 内部表现

- UTF-8：拉丁字母常 1 字节/字符；西里尔、中文等可能多字节/字符。
- 三种视角：**字节**、**标量值**（`char`）、**字形簇**（最像“字母”）。

### 字符串 slice

```rust
let s = &hello[0..4];  // 字节范围；须在 char 边界，否则 panic
```

### 遍历字符串

```rust
for c in "Зд".chars() { }   // Unicode 标量
for b in "Зд".bytes() { }   // 原始字节
```

## 使用 Hash Map 储存键值对

`HashMap<K, V>`：键→值映射；需 `use std::collections::HashMap`（不在 prelude）。

### 新建一个哈希 map

```rust
let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);
```

- 键值类型各自同质。

### 访问哈希 map 中的值

```rust
let score = scores.get("Blue");           // Option<&V>
let v = scores.get("Blue").copied().unwrap_or(0);
for (k, v) in &scores { }
```

- 遍历顺序**任意**。

### 在哈希 map 中管理所有权

- `Copy` 类型（如 `i32`）拷贝进 map。
- 拥有权类型（如 `String`）**move** 进 map，原绑定失效。
- 存引用：引用所指值须比 map **活得久**（生命周期，第10章）。

### 更新哈希 map

- 同键 `insert` → **覆盖**旧值。
- `entry(key).or_insert(value)`：无键则插入，返回 `&mut V`（可用来计数）。

```rust
let count = map.entry(word).or_insert(0);
*count += 1;
```

### 哈希函数

- 默认 **SipHash**（抗 DoS）；可换 `BuildHasher` 实现（crates.io）。
