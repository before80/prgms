+++
title = "3.6.3 Branded 之一：变量专用令牌"
date = 2026-08-11T11:30:00+08:00
weight = 464
type = "docs"
description = "03-Branded 之一：变量专用令牌 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-01-motivation.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-01-motivation.html)

# 3.6.3 Branded 之一：变量专用令牌

若想把令牌绑定到特定变量，该怎么办？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Bytes {
    bytes: Vec<u8>,
}
struct ProvenIndex(usize);

impl Bytes {
    fn get_index(&self, ix: usize) -> Option<ProvenIndex> {
        if ix < self.bytes.len() { Some(ProvenIndex(ix)) } else { None }
    }
    fn get_proven(&self, token: &ProvenIndex) -> u8 {
        unsafe { *self.bytes.get_unchecked(token.0) }
    }
}

fn main() {
    let data_1 = Bytes { bytes: vec![0, 1, 2] };
    if let Some(token_1) = data_1.get_index(2) {
        data_1.get_proven(&token_1); // 没问题！

        // let data_2 = Bytes { bytes: vec![0, 1] };
        // data_2.get_proven(&token_1); // 会 panic！我们能防止吗？
    }
}
```

> - 若想把令牌绑定到代码中的**特定变量**，该怎么办？我们能在 Rust 的类型系统中做到吗？
>
> - 动机：我们想要一种令牌类型，表示已知的、有效的字节数组索引。
>
>   一旦有了这些已证明的索引，我们就能完全避免边界检查，因为令牌会充当**存在该索引的证明**。
>
>   由于索引已知有效，`get_proven()` 可以跳过边界检查。
>
>   本例中没有什么能阻止一个数组的已证明索引被用在另一个数组上。若此时索引越界，则是未定义行为。
>
> - 演示：取消注释 `data_2.get_proven(&token_1);` 行。
>
>   这里的代码会 panic！我们想在编译期防止索引令牌类型的这种「交叉」使用。
>
> - 提问：我们可能如何尝试做到这一点？
>
>   期望学员不会从这里直接得出好的实现，但愿意实验并跟进建议。
>
> - 提问：有哪些替代方案，为什么不够好？
>
>   期望运行时检查索引边界，尤其是因为 `Vec::get` 与 `Bytes::get_index` 都已使用运行时检查。
>
>   运行时边界检查并不能从一开始防止错误的交叉使用，它只保证会 panic。
>
> - 我们将进行的这类令牌关联称为 Branding（打品牌）。这是一种进阶技术，将令牌类型的适用性扩展到更多 API 设计。
>
> - [`GhostCell`](https://plv.mpi-sws.org/rustbelt/ghostcell/paper.pdf)
>   是其显著用户，后续幻灯片会涉及。

