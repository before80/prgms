+++
title = "9.8 RawVec"
date = 2026-08-06T17:08:00+08:00
weight = 50
type = "docs"
description = "抽取 RawVec 缓冲"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# RawVec


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-raw.html](https://doc.rust-lang.org/nomicon/vec/vec-raw.html)


　　我们 reached 一个有趣处境：在 `Vec` 和 `IntoIter` 中 duplicated 了指定缓冲区并释放其内存的逻辑。既然已经实现并识别出*真正的*逻辑重复，正是做逻辑压缩的好时机。

　　把 `(ptr, cap)` 对抽象出来，赋予分配、grow 和释放的逻辑：

```rust,ignore
struct RawVec<T> {
    ptr: NonNull<T>,
    cap: usize,
}

unsafe impl<T: Send> Send for RawVec<T> {}
unsafe impl<T: Sync> Sync for RawVec<T> {}

impl<T> RawVec<T> {
    fn new() -> Self {
        assert!(mem::size_of::<T>() != 0, "TODO: 实现 ZST 支持");
        RawVec {
            ptr: NonNull::dangling(),
            cap: 0,
        }
    }

    fn grow(&mut self) {
        // 不会溢出，因为我们保证 self.cap <= isize::MAX
        let new_cap = if self.cap == 0 { 1 } else { 2 * self.cap };

        // Layout::array 检查字节数 <= usize::MAX，
        // 但这是冗余的，因为 old_layout.size() <= isize::MAX，
        // 所以 `unwrap` 不应失败。
        let new_layout = Layout::array::<T>(new_cap).unwrap();

        // 确保新分配不超过 `isize::MAX` 字节
        assert!(new_layout.size() <= isize::MAX as usize, "Allocation too large");

        let new_ptr = if self.cap == 0 {
            unsafe { alloc::alloc(new_layout) }
        } else {
            let old_layout = Layout::array::<T>(self.cap).unwrap();
            let old_ptr = self.ptr.as_ptr() as *mut u8;
            unsafe { alloc::realloc(old_ptr, old_layout, new_layout.size()) }
        };

        // 若分配失败，`new_ptr` 为 null，此时 abort
        self.ptr = match NonNull::new(new_ptr as *mut T) {
            Some(p) => p,
            None => alloc::handle_alloc_error(new_layout),
        };
        self.cap = new_cap;
    }
}

impl<T> Drop for RawVec<T> {
    fn drop(&mut self) {
        if self.cap != 0 {
            let layout = Layout::array::<T>(self.cap).unwrap();
            unsafe {
                alloc::dealloc(self.ptr.as_ptr() as *mut u8, layout);
            }
        }
    }
}
```

　　`Vec` 相应修改：

```rust,ignore
pub struct Vec<T> {
    buf: RawVec<T>,
    len: usize,
}

impl<T> Vec<T> {
    fn ptr(&self) -> *mut T {
        self.buf.ptr.as_ptr()
    }

    fn cap(&self) -> usize {
        self.buf.cap
    }

    pub fn new() -> Self {
        Vec {
            buf: RawVec::new(),
            len: 0,
        }
    }

    // push/pop/insert/remove 大体不变：
    // * `self.ptr.as_ptr() -> self.ptr()`
    // * `self.cap -> self.cap()`
    // * `self.grow() -> self.buf.grow()`
}

impl<T> Drop for Vec<T> {
    fn drop(&mut self) {
        while let Some(_) = self.pop() {}
        // deallocation 由 RawVec 处理
    }
}
```

　　`IntoIter` 可以 really 简化：

```rust,ignore
pub struct IntoIter<T> {
    _buf: RawVec<T>, // 我们实际上并不关心它，只需要它活着
    start: *const T,
    end: *const T,
}

// next 和 next_back 字面不变，因为它们从未引用 buf

impl<T> Drop for IntoIter<T> {
    fn drop(&mut self) {
        // 只需确保所有元素被读出；
        // 缓冲区之后会自行清理
        for _ in &mut *self {}
    }
}

impl<T> IntoIterator for Vec<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;
    fn into_iter(self) -> IntoIter<T> {
        // 需要用 ptr::read unsafe 移出 buf，因为它不是 Copy，
        // 且 Vec 实现了 Drop（所以不能解构）
        let buf = unsafe { ptr::read(&self.buf) };
        let len = self.len;
        mem::forget(self);

        IntoIter {
            start: buf.ptr.as_ptr(),
            end: if buf.cap == 0 {
                // 不能对非分配一部分的指针 offset
                buf.ptr.as_ptr()
            } else {
                unsafe { buf.ptr.as_ptr().add(len) }
            },
            _buf: buf,
        }
    }
}
```

　　好多了。
