+++
title = "9.7 IntoIter"
date = 2026-08-06T17:08:00+08:00
weight = 49
type = "docs"
description = "实现 IntoIter"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# IntoIter


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-into-iter.html](https://doc.rust-lang.org/nomicon/vec/vec-into-iter.html)


　　来写迭代器。`iter` 和 `iter_mut`  thanks to Deref 的 Magic 已经有了。然而 `Vec` 提供而 slice 不能提供的两个有趣迭代器是 `into_iter` 和 `drain`。

　　`IntoIter` 按值消费 `Vec`，因此可以按值 yield 元素。为此 `IntoIter` 需要取得 `Vec` 分配的控制权。

　　`IntoIter` 还需要是 `DoubleEnded`，以便从两端读取。从后端读可以直接调用 `pop`，但从前端读更难。可以调用 `remove(0)` 但代价极高。我们改用 `ptr::read` 从 `Vec` 任一端复制值，完全不修改缓冲区。

　　为此用非常常见的 C 风格数组迭代 idiom：两个指针，一个指向数组开头，一个指向末尾后一个元素。要从某端取元素，读出该端指向的值，指针移一位。两指针相等时结束。

　　注意 `next` 和 `next_back` 的 read 与 offset 顺序相反。
　　对 `next_back`，指针总在它要读的下一元素*之后*；对 `next`，指针总在它要读的下一元素*处*。
　　原因：考虑除一个外所有元素都已 yield 的情况。

　　数组如下：

```text
          S  E
[X, X, X, O, X, X, X]
```

　　若 `E` 直接指向它要 yield 的下一元素，就无法与「没有更多元素可 yield」区分。

　　迭代期间我们实际上并不关心，但也要持有 `Vec` 的分配信息，以便 `IntoIter` drop 时释放。

　　因此用以下 struct：

```rust,ignore
pub struct IntoIter<T> {
    buf: NonNull<T>,
    cap: usize,
    start: *const T,
    end: *const T,
}
```

　　初始化结果：

```rust,ignore
impl<T> IntoIterator for Vec<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;
    fn into_iter(self) -> IntoIter<T> {
        // 确保不 drop Vec，否则会释放缓冲区
        let vec = ManuallyDrop::new(self);

        // 不能解构 Vec，因为它实现了 Drop
        let ptr = vec.ptr;
        let cap = vec.cap;
        let len = vec.len;

        IntoIter {
            buf: ptr,
            cap,
            start: ptr.as_ptr(),
            end: if cap == 0 {
                // 不能对此指针 offset，它未分配！
                ptr.as_ptr()
            } else {
                unsafe { ptr.as_ptr().add(len) }
            },
        }
    }
}
```

　　向前迭代：

```rust,ignore
impl<T> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<T> {
        if self.start == self.end {
            None
        } else {
            unsafe {
                let result = ptr::read(self.start);
                self.start = self.start.offset(1);
                Some(result)
            }
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let len = (self.end as usize - self.start as usize)
                  / mem::size_of::<T>();
        (len, Some(len))
    }
}
```

　　向后迭代：

```rust,ignore
impl<T> DoubleEndedIterator for IntoIter<T> {
    fn next_back(&mut self) -> Option<T> {
        if self.start == self.end {
            None
        } else {
            unsafe {
                self.end = self.end.offset(-1);
                Some(ptr::read(self.end))
            }
        }
    }
}
```

　　因为 `IntoIter` 拥有其分配，需要实现 `Drop` 来释放。同时也想在 `Drop` 中 drop 未 yield 的元素。

```rust,ignore
impl<T> Drop for IntoIter<T> {
    fn drop(&mut self) {
        if self.cap != 0 {
            // drop 剩余元素
            for _ in &mut *self {}
            let layout = Layout::array::<T>(self.cap).unwrap();
            unsafe {
                alloc::dealloc(self.buf.as_ptr() as *mut u8, layout);
            }
        }
    }
}
```
