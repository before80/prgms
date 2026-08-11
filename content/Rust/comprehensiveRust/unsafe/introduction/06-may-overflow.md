+++
title = "3.8 示例：may_overflow"
date = 2026-08-11T11:30:00+08:00
weight = 515
type = "docs"
description = "06-示例：may_overflow — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/may_overflow.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/may_overflow.html)

# 3.8 示例：may_overflow

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 对负数加上 2^31 - 1。
unsafe fn may_overflow(a: i32) -> i32 {
    a + i32::MAX
}

fn main() {
    let x = unsafe { may_overflow(123) };
    println!("{x}");
}
```

> 「`unsafe` 关键字的含义可能比某些人假设的更为微妙。」
>
> 「代码作者认为代码是正确的。原则上，这段代码是安全的。」
>
> 「在这个玩具示例中，`may_overflow` 函数只应被负数调用。」
>
> 请学员解释为什么 `may_overflow` 需要 `unsafe` 关键字。
>
> 「若你不确定问题出在哪里，我们稍作停顿说明一下。`i32` 只有 31 位可用于正数。当运算结果需要超过 31 位时，程序会进入无效状态。这不仅是数值问题。编译器基于无效状态不可能发生这一假设来优化代码，导致代码路径被删除，产生难以预测的 runtime 行为，并引入安全漏洞。」
>
> 编译并运行代码，产生 panic。然后在 playground 中以 `--release` 模式运行示例以触发 UB（undefined behavior，未定义行为）。
>
> 「这段代码可以被正确使用，但不当使用极其危险。」
>
> 「编译器无法验证用法是否正确。」
>
> 这就是我们所说的：`unsafe` 关键字标记了内存安全责任从编译器转移到程序员的位置。

