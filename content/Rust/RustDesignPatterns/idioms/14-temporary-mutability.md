+++
title = "14-临时可变性"
date = 2026-08-18T22:10:00+08:00
weight = 21
type = "docs"
description = "临时可变性 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/temporary-mutability.html](https://rust-unofficial.github.io/patterns/idioms/temporary-mutability.html)

# 临时可变性

## 描述 {#description}

常常需要准备并处理一些数据，但之后这些数据只会被查看、不会再被修改。把可变变量重新定义为不可变，可以把这一意图表达清楚。

既可以在嵌套块中处理数据，也可以通过重新绑定变量来做到。

## 示例 {#example}

比方说，vector 在使用前必须先排序。

使用嵌套块：

```rust,ignore
let data = {
    let mut data = get_vec();
    data.sort();
    data
};

// 此处 `data` 是不可变的。
```

使用变量重新绑定：

```rust,ignore
let mut data = get_vec();
data.sort();
let data = data;

// 此处 `data` 是不可变的。
```

## 优点 {#advantages}

编译器确保你不会在某个时间点之后意外修改数据。

## 缺点 {#disadvantages}

嵌套块要求块体多一层缩进。还需要多一行从块中返回数据或重新定义变量。
