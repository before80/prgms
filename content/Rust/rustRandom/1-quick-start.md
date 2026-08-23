+++
title = "1 快速入门"
date = 2026-08-23T16:44:00+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-random.github.io/book/quick-start.html](https://rust-random.github.io/book/quick-start.html)

下面列出一个简短示例。更多内容请参阅 [API 文档]或[指南]。

让我们从一个示例开始：

```rust
// 从 prelude 导入常用项：
use rand::prelude::*;

fn main() {
    // 我们可以立即使用 random()。它可以生成多种常见类型的值：
    let x: u8 = rand::random();
    println!("{}", x);

    if rand::random() { // 生成一个布尔值
        println!("Heads!");
    }

    // 如果我们想更明确一些（也更高效一点），可以
    // 获取线程局部生成器的句柄：
    let mut rng = rand::rng();
    if rng.random() { // 随机布尔值
        let x: f64 = rng.random(); // [0, 1) 范围内的随机数
        let y = rng.random_range(-10.0..10.0);
        println!("x is: {}", x);
        println!("y is: {}", y);
    }

    println!("Dice roll: {}", rng.random_range(1..=6));
    println!("Number from 0 to 9: {}", rng.random_range(0..10));
    
    // 有时直接使用分布会很有用：
    let distr = rand::distr::Uniform::new_inclusive(1, 100).unwrap();
    let mut nums = [0i32; 3];
    for x in &mut nums {
        *x = rng.sample(distr);
    }
    println!("Some numbers: {:?}", nums);

    // 我们也可以与迭代器和切片交互：
    let arrows_iter = "➡⬈⬆⬉⬅⬋⬇⬊".chars();
    println!("Lets go in this direction: {}", arrows_iter.choose(&mut rng).unwrap());
    let mut nums = [1, 2, 3, 4, 5];
    nums.shuffle(&mut rng);
    println!("I shuffled my {:?}", nums);
}
```

你可能注意到的第一件事是我们从 [prelude] 导入了所有内容。这是使用 rand 的简便方式，与[标准库的 prelude](https://doc.rust-lang.org/std/prelude/) 类似，只导入最常用的项。如果你不想使用 prelude，请记得导入 [`Rng`] trait！

Rand 库会在需要时自动初始化一个安全的、线程局部的生成器。可通过 [`rng()`] 和 [`random`] 函数访问。关于此主题的更多信息，请参阅[随机生成器](../guide/3.3-types-of-generators/)。

虽然 [`random`] 函数只能以 [`StandardUniform`]（类型相关）的方式采样值，但 [`rng()`] 会给你一个生成器句柄。所有生成器都实现了 [`Rng`] trait，它提供了上文使用的 [`random`]、[`random_range`] 和 [`sample`] 方法。

Rand 通过另外两个 trait——[`IteratorRandom`] 和 [`SliceRandom`]——为迭代器和切片提供功能。

## 固定种子的 RNG

你可能注意到了上文对 `rand::rng()` 的使用，并想知道如何指定固定种子。为此，你需要指定一个 RNG，然后使用 [`seed_from_u64`] 或 [`from_seed`] 等方法。

请注意，[`seed_from_u64`] **不适合用于加密用途**，因为单个 `u64` 无法提供足够的熵来安全地播种 RNG。所有加密 RNG 都通过 [`from_seed`] 接受更合适的种子。

下文使用 `ChaCha8Rng`，因为它快速、可移植且质量良好。更多 RNG 请参阅 [RNG] 一节，但如果你关心可重现的结果，请避免使用 `SmallRng` 和 `StdRng`。

```rust
use rand::{rngs::ChaCha8Rng, RngExt, SeedableRng};

fn main() {
    let mut rng = ChaCha8Rng::seed_from_u64(10);
    println!("Random f32: {}", rng.random::<f32>());
}
```

[API 文档]: https://docs.rs/rand/
[指南]: ../guide/
[RNG]: ../guide/3.4-our-rngs/
[prelude]: https://docs.rs/rand/latest/rand/prelude/
[`Rng`]: https://docs.rs/rand/latest/rand/trait.Rng.html
[`random`]: https://docs.rs/rand/latest/rand/trait.Rng.html#method.random
[`random_range`]: https://docs.rs/rand/latest/rand/trait.Rng.html#method.random_range
[`sample`]: https://docs.rs/rand/latest/rand/trait.Rng.html#method.sample
[`rng()`]: https://docs.rs/rand/latest/rand/fn.rng.html
[`random`]: https://docs.rs/rand/latest/rand/fn.random.html
[`StandardUniform`]: https://docs.rs/rand/latest/rand/distr/struct.StandardUniform.html
[`IteratorRandom`]: https://docs.rs/rand/latest/rand/seq/trait.IteratorRandom.html
[`SliceRandom`]: https://docs.rs/rand/latest/rand/seq/trait.SliceRandom.html
[`seed_from_u64`]: https://docs.rs/rand/latest/rand/trait.SeedableRng.html#method.seed_from_u64
[`from_seed`]: https://docs.rs/rand/latest/rand/trait.SeedableRng.html#tymethod.from_seed
