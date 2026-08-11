+++
title = "9.3 Push 与 Pop"
date = 2026-08-06T17:08:00+08:00
weight = 45
type = "docs"
description = "实现 push 与 pop"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Push 与 Pop


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-push-pop.html](https://doc.rust-lang.org/nomicon/vec/vec-push-pop.html)


　　好。我们能初始化，能分配。来实现些功能吧！从 `push` 开始。它只需检查是否已满并在需要时 grow，无条件写入下一 index，然后递增 length。

　　写入时必须小心不要*求值*我们要写入的内存。最坏情况是分配器给出的 truly 未初始化内存；最好情况是某个被 pop 掉的旧值的比特。无论哪种，都不能直接索引并解引用，因为那会把内存求值为有效的 `T` 实例。更糟的是，`foo[idx] = x` 会尝试对 `foo[idx]` 的旧值调用 `drop`！

　　正确做法是用 `ptr::write`，它盲目用我们提供的值的比特覆盖目标地址，不涉及求值。

　　对 `push`，若旧 len（调用 push 前）为 0，我们要写入第 0 个 index。因此应按旧 len 偏移。

```rust,ignore
pub fn push(&mut self, elem: T) {
    if self.len == self.cap { self.grow(); }

    unsafe {
        ptr::write(self.ptr.as_ptr().add(self.len), elem);
    }

    // 不会失败，我们会先 OOM。
    self.len += 1;
}
```

　　简单！`pop` 呢？这次我们要访问的 index 已初始化，但 Rust 不会让我们解引用该内存位置把值移出，因为那会使内存未初始化！对此我们需要 `ptr::read`，它从目标地址复制比特并解释为 `T`。这会使该地址的内存逻辑上未初始化，尽管那里事实上仍有一个完好的 `T` 实例。

　　对 `pop`，若旧 len 为 1，我们要从第 0 个 index 读出。因此应按新 len 偏移。

```rust,ignore
pub fn pop(&mut self) -> Option<T> {
    if self.len == 0 {
        None
    } else {
        self.len -= 1;
        unsafe {
            Some(ptr::read(self.ptr.as_ptr().add(self.len)))
        }
    }
}
```
