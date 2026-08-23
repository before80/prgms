+++
title = "5 内联"
date = 2026-08-23T13:57:00+08:00
weight = 6
type = "docs"
description = "内联与代码体积"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 内联 {#inlining}


> 原文链接: [https://nnethercote.github.io/perf-book/inlining.html](https://nnethercote.github.io/perf-book/inlining.html)


进入和退出未内联的热点函数，往往会占用相当一部分执行时间。内联这些函数可以消除这些进入和退出，并使编译器能够进行额外的底层优化。在最佳情况下，整体效果虽小，却是容易获得的性能提升。

Rust 函数上可以使用四种内联属性。
- **无**。编译器将自行决定是否内联该函数。这取决于优化级别、函数大小、函数是否为泛型以及内联是否跨 crate 边界等因素。
- **`#[inline]`**。建议内联该函数。
- **`#[inline(always)]`**。强烈建议内联该函数。
- **`#[inline(never)]`**。强烈建议不要内联该函数。

内联属性不保证函数一定会或一定不会内联，但在实践中，`#[inline(always)]` 在几乎所有情况下都会导致内联。

内联不具有传递性。如果函数 `f` 调用函数 `g`，而你希望在 `f` 的调用点将两个函数一起内联，则两个函数都应标记内联属性。

## 简单情况

最适合内联的候选是：(a) 非常小的函数，或 (b) 只有一个调用点的函数。即使没有内联属性，编译器也经常会自行内联这些函数。但编译器并不总能做出最佳选择，因此有时需要添加属性。
[**示例 1**](https://github.com/rust-lang/rust/pull/37083/commits/6a4bb35b70862f33ac2491ffe6c55fb210c8490d)，
[**示例 2**](https://github.com/rust-lang/rust/pull/50407/commits/e740b97be699c9445b8a1a7af6348ca2d4c460ce)，
[**示例 3**](https://github.com/rust-lang/rust/pull/50564/commits/77c40f8c6f8cc472f6438f7724d60bf3b7718a0c)，
[**示例 4**](https://github.com/rust-lang/rust/pull/57719/commits/92fd6f9d30d0b6b4ecbcf01534809fb66393f139)，
[**示例 5**](https://github.com/rust-lang/rust/pull/69256/commits/e761f3af904b3c275bdebc73bb29ffc45384945d)。

Cachegrind 是判断函数是否被内联的良好分析器。查看 Cachegrind 输出时，当且仅当函数的第一行和最后一行*未*标记事件计数时，可以判断该函数已被内联。例如：
```text
      .  #[inline(always)]
      .  fn inlined(x: u32, y: u32) -> u32 {
700,000      eprintln!("inlined: {} + {}", x, y);
200,000      x + y
      .  }
      .  
      .  #[inline(never)]
400,000  fn not_inlined(x: u32, y: u32) -> u32 {
700,000      eprintln!("not_inlined: {} + {}", x, y);
200,000      x + y
200,000  }
```
添加内联属性后应再次测量，因为效果可能难以预测。有时没有效果，因为附近之前被内联的函数不再被内联。有时会减慢代码速度。内联还可能影响编译时间，尤其是跨 crate 内联，涉及复制函数的内部表示。

## 较难的情况

有时你有一个较大且有多个调用点的函数，但只有一个调用点是热点。你希望对热点调用点进行内联以提高速度，但不对冷调用点内联以避免不必要的代码膨胀。处理方法是将该函数拆分为始终内联和从不内联两个变体，后者调用前者。

例如，这个函数：
```rust
# fn one() {};
# fn two() {};
# fn three() {};
fn my_function() {
    one();
    two();
    three();
}
```
将变为这两个函数：
```rust
# fn one() {};
# fn two() {};
# fn three() {};
// 在热点调用点使用此函数。
#[inline(always)]
fn inlined_my_function() {
    one();
    two();
    three();
}

// 在冷调用点使用此函数。
#[inline(never)]
fn uninlined_my_function() {
    inlined_my_function();
}
```
[**示例 1**](https://github.com/rust-lang/rust/pull/53513/commits/b73843f9422fb487b2d26ac2d65f79f73a4c9ae3)，
[**示例 2**](https://github.com/rust-lang/rust/pull/64420/commits/a2261ad66400c3145f96ebff0d9b75e910fa89dd)。

## 外联

内联的逆操作是*外联*：将很少执行的代码移入单独的函数。你可以对此类函数添加 `#[cold]` 属性，告诉编译器该函数很少被调用。这可以改善热路径的代码生成。
[**示例 1**](https://github.com/Lokathor/tinyvec/pull/127)，
[**示例 2**](https://crates.io/crates/fast_assert)。
