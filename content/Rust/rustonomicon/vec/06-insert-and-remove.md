+++
title = "9.6 Insert 与 Remove"
date = 2026-08-06T17:08:00+08:00
weight = 48
type = "docs"
description = "实现 insert 与 remove"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Insert 与 Remove


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-insert-remove.html](https://doc.rust-lang.org/nomicon/vec/vec-insert-remove.html)


　　slice *不*提供 `insert` 和 `remove`，我们来实现。

　　`insert` 需要把目标 index 处的所有元素右移一位。为此用 `ptr::copy`，即 C 的 `memmove` 的 Rust 版。它把一块内存从一处复制到另一处，正确处理源与目标重叠的情况（此处必然会发生）。

　　若在 index `i` 插入，要用旧 len 把 `[i .. len]` 移到 `[i+1 .. len+1]`。

```rust,ignore
pub fn insert(&mut self, index: usize, elem: T) {
    // 注意：用 `<=` 因为插入到末尾也合法，等价于 push。
    assert!(index <= self.len, "index out of bounds");
    if self.len == self.cap { self.grow(); }

    unsafe {
        // ptr::copy(src, dest, len)："从 src 复制 len 个元素到 dest"
        ptr::copy(
            self.ptr.as_ptr().add(index),
            self.ptr.as_ptr().add(index + 1),
            self.len - index,
        );
        ptr::write(self.ptr.as_ptr().add(index), elem);
    }

    self.len += 1;
}
```

　　`remove` 行为相反。需要用*新* len 把 `[i+1 .. len + 1]` 移到 `[i .. len]`。

```rust,ignore
pub fn remove(&mut self, index: usize) -> T {
    // 注意：用 `<` 因为*不能*删除末尾之后
    assert!(index < self.len, "index out of bounds");
    unsafe {
        self.len -= 1;
        let result = ptr::read(self.ptr.as_ptr().add(index));
        ptr::copy(
            self.ptr.as_ptr().add(index + 1),
            self.ptr.as_ptr().add(index),
            self.len - index,
        );
        result
    }
}
```
