+++
title = "第3章 所有权"
date = 2026-08-06T17:08:00+08:00
weight = 10
type = "docs"
description = "所有权与生命周期的深层规则"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 所有权


> 原文链接: [https://doc.rust-lang.org/nomicon/ownership.html](https://doc.rust-lang.org/nomicon/ownership.html)


　　所有权（ownership）是 Rust 的突破性特性。它使 Rust 完全内存安全且高效，又避免垃圾回收。在深入所有权系统前，我们先看这一设计的动机。

　　我们假定你接受垃圾回收（GC）并非总是最优解，在某些上下文手动管理内存是可取的。若不接受，要不要考虑别的语言？

　　无论你对 GC 看法如何，它显然对代码安全是*巨大*裨益。你不必再担心东西消失*太早*（尽管你是否仍想指向那东西是另一回事……）。这是 C 与 C++ 程序须应对的普遍问题。考虑这个我们都曾在非 GC 语言里犯过的简单错误：

```rust,compile_fail
fn as_str(data: &u32) -> &str {
    // 计算字符串
    let s = format!("{}", data);

    // 糟了！我们返回了只在本函数内
    // 存在之物的引用！
    // 悬垂指针！释放后使用！
    // （这在 Rust 中不能编译）
    &s
}
```

　　这正是 Rust 所有权系统要解决的。Rust 知道 `&s` 存活的作用域，因而可阻止其逃逸。但这是 C 编译器也许能抓到的简单情况。代码变大、指针经各函数传递时更复杂。最终 C 编译器会力有不逮，无法做足够逃逸分析证明代码不健全，因而被迫在假定正确的前提下接受程序。

　　这在 Rust 中不会发生。须由程序员向编译器证明一切健全。

　　当然，Rust 围绕所有权的故事远不只是验证引用不逃逸被引用对象的作用域。因为确保指针始终有效远比这复杂。例如在本代码中，

```rust,compile_fail
let mut data = vec![1, 2, 3];
// 取得内部引用
let x = &data[0];

// 糟了！`push` 导致 `data` 后备存储重新分配。
// 悬垂指针！释放后使用！
// （这在 Rust 中不能编译）
data.push(4);

println!("{}", x);
```

　　朴素的作用域分析不足以防止此 bug，因为 `data` 确实活得够久。但我们在持有其引用时*改变了*它。因此 Rust 要求任何引用冻结被引用对象及其 owner。
