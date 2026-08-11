+++
title = "3.3.2 方法解析冲突"
date = 2026-08-11T11:30:00+08:00
weight = 441
type = "docs"
description = "02-方法解析冲突 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/method-resolution-conflicts.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/method-resolution-conflicts.html)

# 3.3.2 方法解析冲突

固有方法与扩展方法发生命名冲突时会怎样？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod ext {
    pub trait CountOnesExt {
        fn count_ones(&self) -> u32;
    }

    impl CountOnesExt for i32 {
        fn count_ones(&self) -> u32 {
            let value = *self;
            (0..32).filter(|i| ((value >> i) & 1i32) == 1).count() as u32
        }
    }
}
fn main() {
    pub use ext::CountOnesExt;
    // 调用的是哪个 `count_ones` 方法？
    // 来自 `CountOnesExt` 的？还是 `i32` 的固有方法？
    assert_eq!((-1i32).count_ones(), 32);
}
```

> - 外来类型可能在较新版本中添加与我们扩展方法同名的新固有方法。
>
>   提问：上例会发生什么？会有编译错误吗？两个方法中哪一个优先级更高？
>
>   在 `CountOnesExt::count_ones` 方法体中加入 `panic!("Extension trait");`，以弄清实际调用的是哪个方法。
>
> - 为避免 Rust 使用者在所有情况下都手动指定要用哪个方法，方法「挑选」有优先级排序系统：
>   - 不可变（`&self`）优先
>     - 固有方法（在类型的 `impl` 块中定义）先于 Trait 方法（由 trait impl 添加）。
>   - 可变（`&mut self`）其次
>     - 固有方法先于 Trait 方法。
>
>   若同名方法的可变性各不相同，且分别定义为固有方法或 trait 方法、没有重叠，编译器的工作就很轻松。
>
>   这确实会给用户带来一些歧义：他们可能困惑为何依赖的方法没有产生预期行为。若可以，应避免命名冲突，而不是依赖这一机制。
>
>   演示：将 `CountOnesExt::count_ones` 的签名与实现改为 `fn count_ones(&mut self) -> u32`，并相应修改调用：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   assert_eq!((&mut -1i32).count_ones(), 32);
>   ```
>
>   会调用 `CountOnesExt::count_ones`，而不是固有方法，因为 `&mut self` 的优先级高于固有方法使用的 `&self`。
>
>   若同一类型既有不可变固有方法又有可变 trait 方法，可在调用处用
>   `(&<value>).count_ones()` 选择不可变（更高优先级）方法，或用
>   `(&mut <value>).count_ones()` 选择可变方法。
>
>   引导学生查阅 Rust 参考文档了解更多关于
>   [方法解析][2]
>   的信息。
>
> - 避免扩展 trait 方法与固有方法之间的命名冲突。Rust 的方法解析算法很复杂，可能让你的代码使用者感到意外。
>
> ## 深入探索
>
> - Rust 方法解析算法使用的优先级搜索与自动 `Deref` 之间的交互，可用于在稳定工具链上模拟 [特化（specialization）][4]，主要用于宏生成代码。具体细节见 [「Autoref Specialization」][5]。


[1]: https://doc.rust-lang.org/stable/reference/expressions/method-call-expr.html#r-expr.method.candidate-search
[2]: https://doc.rust-lang.org/stable/reference/expressions/method-call-expr.html
[3]: https://github.com/rust-lang/reference/pull/1725
[4]: https://github.com/rust-lang/rust/issues/31844
[5]: https://github.com/dtolnay/case-studies/blob/master/autoref-specialization/README.md
