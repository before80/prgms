+++
title = "01-编程范式"
date = 2026-08-18T22:10:00+08:00
weight = 47
type = "docs"
description = "编程范式 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/functional/paradigms.html](https://rust-unofficial.github.io/patterns/functional/paradigms.html)

# 编程范式

从命令式背景转向理解函数式程序时，最大的障碍之一是思维方式的转变。命令式程序描述的是**如何**做某事，而声明式程序描述的是**做什么**。我们用把 1 到 10 的数字求和来说明这一点。

## 命令式 {#imperative}

```rust
let mut sum = 0;
for i in 1..11 {
    sum += i;
}
println!("{sum}");
```

对于命令式程序，我们得自己当编译器才能看清发生了什么。这里，我们从 `sum` 为 `0` 开始。接着，我们遍历从 1 到 10 的范围。每次循环，我们把范围内对应的值加进去。然后把它打印出来。

| `i` | `sum` |
| :-: | :---: |
|  1  |   1   |
|  2  |   3   |
|  3  |   6   |
|  4  |  10   |
|  5  |  15   |
|  6  |  21   |
|  7  |  28   |
|  8  |  36   |
|  9  |  45   |
| 10  |  55   |

我们大多数人就是这样开始编程的。我们学到：程序是一组步骤。

## 声明式 {#declarative}

```rust
println!("{}", (1..11).fold(0, |a, b| a + b));
```

哇！这真的很不一样！这里发生了什么？请记住，声明式程序描述的是**做什么**，而不是**如何**做。`fold` 是一个
[组合](https://en.wikipedia.org/wiki/Function_composition)函数的函数。这个名字来自 Haskell 的惯例。

这里，我们把加法函数（这个闭包：`|a, b| a + b`）与从 1 到 10 的范围组合起来。`0` 是起点，因此一开始 `a` 是 `0`。`b` 是范围的第一个元素 `1`。`0 + 1 = 1` 是结果。于是我们再次 `fold`，此时 `a = 1`，`b = 2`，所以下一个结果是 `1 + 2 = 3`。这个过程持续到我们到达范围的最后一个元素 `10`。

| `a` | `b` | result |
| :-: | :-: | :----: |
|  0  |  1  |   1    |
|  1  |  2  |   3    |
|  3  |  3  |   6    |
|  6  |  4  |   10   |
| 10  |  5  |   15   |
| 15  |  6  |   21   |
| 21  |  7  |   28   |
| 28  |  8  |   36   |
| 36  |  9  |   45   |
| 45  | 10  |   55   |
