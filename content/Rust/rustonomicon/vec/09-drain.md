+++
title = "9.9 Drain"
date = 2026-08-06T17:08:00+08:00
weight = 51
type = "docs"
description = "实现 Drain"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Drain


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-drain.html](https://doc.rust-lang.org/nomicon/vec/vec-drain.html)


　　接下来实现 Drain。Drain 与 IntoIter 大体相同，区别在于它不消费 Vec，而是借用 Vec 并保留其分配不变。目前我们只实现「基础」的全范围版本。

```rust,ignore
use std::marker::PhantomData;

struct Drain<'a, T: 'a> {
    // 需要在这里约束生命周期，因此用 `&'a mut Vec<T>`，
    // 因为语义上我们包含的就是它。我们「只是」在调用
    // `pop()` 和 `remove(0)`。
    vec: PhantomData<&'a mut Vec<T>>,
    start: *const T,
    end: *const T,
}

impl<'a, T> Iterator for Drain<'a, T> {
    type Item = T;
    fn next(&mut self) -> Option<T> {
        if self.start == self.end {
            None
```

　　——等等，这看起来似曾相识。我们再做些压缩。IntoIter 和 Drain 结构完全相同，干脆抽出来。

```rust,ignore
struct RawValIter<T> {
    start: *const T,
    end: *const T,
}

impl<T> RawValIter<T> {
    // 构造是不安全的，因为它没有关联的生命周期。
    // 这是必要的，以便把 RawValIter 与实际分配放在同一结构体里。
    // 没问题，因为它是私有的实现细节。
    unsafe fn new(slice: &[T]) -> Self {
        RawValIter {
            start: slice.as_ptr(),
            end: if slice.len() == 0 {
                // 若 `len = 0`，则这并非真正已分配的内存。
                // 必须避免 offset，否则会通过 GEP 向 LLVM 传递错误信息。
                slice.as_ptr()
            } else {
                slice.as_ptr().add(slice.len())
            }
        }
    }
}

// Iterator 与 DoubleEndedIterator 的实现与 IntoIter 相同。
```

　　IntoIter 变成：

```rust,ignore
pub struct IntoIter<T> {
    _buf: RawVec<T>, // 我们并不真正关心它，只需要它活着。
    iter: RawValIter<T>,
}

impl<T> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<T> { self.iter.next() }
    fn size_hint(&self) -> (usize, Option<usize>) { self.iter.size_hint() }
}

impl<T> DoubleEndedIterator for IntoIter<T> {
    fn next_back(&mut self) -> Option<T> { self.iter.next_back() }
}

impl<T> Drop for IntoIter<T> {
    fn drop(&mut self) {
        for _ in &mut *self {}
    }
}

impl<T> IntoIterator for Vec<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;
    fn into_iter(self) -> IntoIter<T> {
        unsafe {
            let iter = RawValIter::new(&self);

            let buf = ptr::read(&self.buf);
            mem::forget(self);

            IntoIter {
                iter,
                _buf: buf,
            }
        }
    }
}
```

　　注意，我在设计里留了一些小瑕疵，以便日后把 Drain 升级为支持任意子范围时更容易。例如我们*可以*让 RawValIter 在 drop 时自行 drain，但对更复杂的 Drain 行不通。我们也接受 slice 以简化 Drain 的初始化。

　　好，现在 Drain 就很简单了：

```rust,ignore
use std::marker::PhantomData;

pub struct Drain<'a, T: 'a> {
    vec: PhantomData<&'a mut Vec<T>>,
    iter: RawValIter<T>,
}

impl<'a, T> Iterator for Drain<'a, T> {
    type Item = T;
    fn next(&mut self) -> Option<T> { self.iter.next() }
    fn size_hint(&self) -> (usize, Option<usize>) { self.iter.size_hint() }
}

impl<'a, T> DoubleEndedIterator for Drain<'a, T> {
    fn next_back(&mut self) -> Option<T> { self.iter.next_back() }
}

impl<'a, T> Drop for Drain<'a, T> {
    fn drop(&mut self) {
        for _ in &mut *self {}
    }
}

impl<T> Vec<T> {
    pub fn drain(&mut self) -> Drain<T> {
        let iter = unsafe { RawValIter::new(&self) };

        // 这是 mem::forget 相关的安全考量。若 Drain 被 forget，我们
        // 只会泄漏整个 Vec 的内容。而且我们*终究*要做这件事，
        // 何不现在就做？
        self.len = 0;

        Drain {
            iter,
            vec: PhantomData,
        }
    }
}
```

　　关于 `mem::forget` 问题的更多细节，见[泄漏一节][leaks]。

[leaks]: ../leaking.html
