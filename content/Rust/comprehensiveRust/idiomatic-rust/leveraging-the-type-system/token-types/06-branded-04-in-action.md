+++
title = "3.6.6 Branded 之四：Branded 类型实战"
date = 2026-08-11T11:30:00+08:00
weight = 467
type = "docs"
description = "06-Branded 之四：Branded 类型实战 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-04-in-action.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-04-in-action.html)

# 3.6.6 Branded 之四：Branded 类型实战

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::marker::PhantomData;

#[derive(Default)]
struct InvariantLifetime<'id>(PhantomData<*mut &'id ()>);
struct ProvenIndex<'id>(usize, InvariantLifetime<'id>);

struct Bytes<'id>(Vec<u8>, InvariantLifetime<'id>);

impl<'id> Bytes<'id> {
    fn new<T>(
        // 我们想在此上下文中修改的数据。
        bytes: Vec<u8>,
        // 唯一地为 `Bytes` 的生命周期打品牌的函数
        f: impl for<'a> FnOnce(Bytes<'a>) -> T,
    ) -> T {
        f(Bytes(bytes, InvariantLifetime::default()))
    }

    fn get_index(&self, ix: usize) -> Option<ProvenIndex<'id>> {
        if ix < self.0.len() {
            Some(ProvenIndex(ix, InvariantLifetime::default()))
        } else {
            None
        }
    }

    fn get_proven(&self, ix: &ProvenIndex<'id>) -> u8 {
        self.0[ix.0]
    }
}

fn main() {
    let result = Bytes::new(vec![4, 5, 1], |mut bytes_1| {
        Bytes::new(vec![4, 2], |mut bytes_2| {
            let index_1 = bytes_1.get_index(2).unwrap();
            let index_2 = bytes_2.get_index(1).unwrap();
            bytes_1.get_proven(&index_1);
            bytes_2.get_proven(&index_2);
            // bytes_2.get_proven(&index_1); // ❌🔨
            "Computations done!"
        })
    });
    println!("{result}");
}
```

> - 实现现已就绪，我们可以编写这样一个程序：作为已存在索引之证明的令牌类型不能在变量之间共享。
>
> - 演示：取消注释 `bytes_2.get_proven(&index_1);` 行，展示当我们使用来自不同变量的索引时无法编译。
>
> - 提问：我们可以执行哪些能保证产生已证明索引的操作？
>
>   期望一个「push」实现，建议演示：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn push(&mut self, value: u8) -> ProvenIndex<'id> {
>       self.0.push(value);
>       ProvenIndex(self.0.len() - 1, InvariantLifetime::default())
>   }
>   ```
>
> - 提问：我们能否不只针对字节数组，而是做成 `Vec<T>` 的通用包装？
>
>   显然：可以！
>
>   或可演示：将 `Bytes<'id>` 泛化为 `BrandedVec<'id, T>`
>
> - 提问：还有哪些领域可以用类似的东西？
>
> - 最终的令牌 API **限制很强**，但它使能在 Rust 类型系统内证明为安全的事情是有意义的。
>
> ## 深入探索
>
> - [GhostCell](https://plv.mpi-sws.org/rustbelt/ghostcell/paper.pdf)
>   是一种允许在 Rust 中安全使用循环数据结构（以及其他此前难以表示的数据结构）的结构，它使用这类令牌类型，确保 cell 不能「逃出」我们知道类似本例中操作安全的上下文。
>
>   这组「Branded Types」幻灯片基于其论文中的 `BrandedVec` 实现，该实现更深入地覆盖了此用例的许多实现细节，作为对 `GhostCell` 本身如何实现及在实践中如何使用的温和介绍。
>
>   GhostCell 还使用 Rust 类型系统之外的形式化检查，证明它在这类上下文（生命周期 branding）中允许的事情是安全的。

