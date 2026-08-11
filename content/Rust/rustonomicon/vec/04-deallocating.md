+++
title = "9.4 释放"
date = 2026-08-06T17:08:00+08:00
weight = 46
type = "docs"
description = "释放 Vec 的内存"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 释放


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-dealloc.html](https://doc.rust-lang.org/nomicon/vec/vec-dealloc.html)


　　接下来应实现 `Drop`，以免大量泄漏资源。最简单是不断调用 `pop` 直到返回 `None`，然后 deallocate 缓冲区。注意若 `T: !Drop`，调用 `pop` 是不必要的。理论上可以问 Rust `T` 是否 `needs_drop` 并省略 `pop` 调用。但实践中 LLVM *非常*擅长去掉这类简单无副作用代码，除非发现没被 strip 否则我不 bother（此例会被 strip）。

　　当 `self.cap == 0` 时绝不能调用 `alloc::dealloc`，因为此时尚未真正分配内存。

```rust,ignore
impl<T> Drop for Vec<T> {
    fn drop(&mut self) {
        if self.cap != 0 {
            while let Some(_) = self.pop() { }
            let layout = Layout::array::<T>(self.cap).unwrap();
            unsafe {
                alloc::dealloc(self.ptr.as_ptr() as *mut u8, layout);
            }
        }
    }
}
```
