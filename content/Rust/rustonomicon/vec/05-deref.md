+++
title = "9.5 Deref"
date = 2026-08-06T17:08:00+08:00
weight = 47
type = "docs"
description = "为 Vec 实现 Deref"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Deref


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-deref.html](https://doc.rust-lang.org/nomicon/vec/vec-deref.html)


　　好！我们有了像样的最小栈实现。能 push、能 pop、能自我清理。然而还缺大量合理想要的功能。尤其我们有了真正的数组，却没有 slice 功能。这很好解决：实现 `Deref<Target=[T]>`。这会神奇地让 `Vec` 在各种情况下强制转换为 slice 并表现得像 slice。

　　我们只需 `slice::from_raw_parts`。它会正确处理空 slice。之后设置零大小类型支持时，对它们也会 Just Work。

```rust,ignore
use std::ops::Deref;

impl<T> Deref for Vec<T> {
    type Target = [T];
    fn deref(&self) -> &[T] {
        unsafe {
            std::slice::from_raw_parts(self.ptr.as_ptr(), self.len)
        }
    }
}
```

　　再来 `DerefMut`：

```rust,ignore
use std::ops::DerefMut;

impl<T> DerefMut for Vec<T> {
    fn deref_mut(&mut self) -> &mut [T] {
        unsafe {
            std::slice::from_raw_parts_mut(self.ptr.as_ptr(), self.len)
        }
    }
}
```

　　现在我们有 slice 提供的 `len`、`first`、`last`、索引、切片、排序、`iter`、`iter_mut` 等各种功能。妙极了！
