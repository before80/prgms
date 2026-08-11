+++
title = "3.2 别名"
date = 2026-08-06T17:08:00+08:00
weight = 12
type = "docs"
description = "别名为何重要"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 别名


> 原文链接: [https://doc.rust-lang.org/nomicon/aliasing.html](https://doc.rust-lang.org/nomicon/aliasing.html)


　　首先，先把几个重要前提说清楚：

* 为便于讨论，我们采用 alias（别名）最宽泛的定义。Rust 的定义可能会更受限，以纳入 mutation（变更）与 liveness（存活期）。

* 我们假定单线程、无中断的执行，并忽略内存映射硬件等。Rust 假定这些情况不会发生，除非你另有说明。更多细节见[并发一章](concurrency.html)。

　　在此前提下，工作定义如下：若变量与指针指向重叠的内存区域，则它们*互为别名*。

## 别名为何重要

　　那我们为何要在意 alias？

　　考虑这个简单函数：

```rust
fn compute(input: &u32, output: &mut u32) {
    if *input > 10 {
        *output = 1;
    }
    if *input > 5 {
        *output *= 2;
    }
    // 记住：若 `input > 10`，`output` 将为 `2`
}
```

　　我们*希望*能把它优化成：

```rust
fn compute(input: &u32, output: &mut u32) {
    let cached_input = *input; // 把 `*input` 缓存在寄存器中
    if cached_input > 10 {
        // 若输入大于 10，原代码会先把 output 设为 1 再翻倍，
        // 结果为 2（因为 `>10` 蕴含 `>5`）。
        // 这里避免两次赋值，直接设为 2。
        *output = 2;
    } else if cached_input > 5 {
        *output *= 2;
    }
}
```

　　在 Rust 中，此优化应是健全（sound）的。对几乎所有其他语言则不然（除非做全局分析）。因为优化依赖知道不存在 alias，而多数语言对此相当宽松。具体地，我们须担心使 `input` 与 `output` 重叠的实参，例如 `compute(&x, &mut x)`。

　　对该输入，可能出现如下执行：

```rust,ignore
                    //  input ==  output == 0xabad1dea
                    // *input == *output == 20
if *input > 10 {    // true  (*input == 20)
    *output = 1;    // 也覆盖 *input，因为二者相同
}
if *input > 5 {     // false (*input == 1)
    *output *= 2;
}
                    // *input == *output == 1
```

　　我们的优化函数对该输入会产生 `*output == 2`，故优化正确性依赖该输入不可能出现。

　　在 Rust 中我们知道该输入应不可能，因为 `&mut` 不允许 alias。故可安全排除其可能性并做此优化。在多数其他语言中，该输入完全可能，必须考虑。

　　这就是 alias 分析重要的原因：它让编译器做有用优化！例如：

* 通过证明无指针访问某值内存，把值保留在寄存器中
* 通过证明自上次读取后某内存未被写入，消除读取
* 通过证明某内存在下次写入前从未被读，消除写入
* 通过证明读写互不依赖，移动或重排读写

　　这些优化也往往会证明更大优化的健全性，如循环向量化、常量传播、死代码消除。

　　上一例中，我们利用 `&mut u32` 不能 alias 证明对 `*output` 的写入不可能影响 `*input`，从而把 `*input` 缓存在寄存器、消除一次读取。

　　通过缓存该读取，我们知道 `> 10` 分支的写入不会影响是否走 `> 5` 分支，从而在 `*input > 10` 时也可消除读-改-写（把 `*output` 翻倍）。

　　alias 分析要记住的关键是：写入是优化的主要隐患。即，阻止我们把读取移到程序任意其他部分的唯一可能是：可能与同一位置的写入重排。

　　例如，下面修改版函数我们不必担心 alias，因为把对 `*output` 的唯一写入移到了函数末尾。这允许我们自由重排它之前的 `*input` 读取：

```rust
fn compute(input: &u32, output: &mut u32) {
    let mut temp = *output;
    if *input > 10 {
        temp = 1;
    }
    if *input > 5 {
        temp *= 2;
    }
    *output = temp;
}
```

　　我们仍依赖 alias 分析假定 `input` 不 alias `temp`，但证明简单得多：局部变量的值不能被声明它之前已存在的东西 alias。这是每种语言都自由做出的假设，故该版本函数可在任何语言中按我们期望优化。

　　这就是 Rust 将使用的「alias」定义很可能涉及 liveness 与 mutation 的原因：若没有实际内存写入，我们实际上并不在意是否发生 alias。

　　当然，Rust 的完整 alias 模型还须考虑函数调用（可能修改我们看不见的东西）、裸指针（自身无 alias 要求）与 `UnsafeCell`（允许通过 `&` 修改 referent）。
