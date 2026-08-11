+++
title = "9.10 处理零大小类型"
date = 2026-08-06T17:08:00+08:00
weight = 52
type = "docs"
description = "Vec 对 ZST 的处理"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 处理零大小类型


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-zsts.html](https://doc.rust-lang.org/nomicon/vec/vec-zsts.html)


　　是时候了。我们要对付零大小类型（ZST，zero-sized type）这个幽灵。Safe Rust *从不需要*关心这件事，但 Vec 大量依赖裸指针和裸分配，而这两者恰恰最在意零大小类型。我们需要小心两件事：

* 原始分配器 API 在分配大小为 0 时行为未定义。
* 对零大小类型，裸指针 offset 是空操作，会破坏我们的 C 风格指针迭代器。

　　幸好我们把指针迭代器和分配处理分别抽象进了 `RawValIter` 和 `RawVec`。真是巧得可疑。

## 为零大小类型分配

　　若分配器 API 不支持零大小分配，那我们到底该存什么作为「分配」？当然是 `NonNull::dangling()`！几乎所有涉及 ZST 的操作都是空操作，因为 ZST 恰好只有一个值，存取时无需考虑任何状态。这甚至延伸到 `ptr::read` 和 `ptr::write`：它们根本不会查看指针。因此我们永远不必改指针。

　　但要注意，我们此前依赖「在溢出前先耗尽内存」的做法，对零大小类型不再成立。必须显式防止 ZST 的容量溢出。

　　按当前架构，这意味着在 `RawVec` 的每个方法里各写一道守卫，共三处。

```rust,ignore
impl<T> RawVec<T> {
    fn new() -> Self {
        // 这个分支应在编译期被剔除。
        let cap = if mem::size_of::<T>() == 0 { usize::MAX } else { 0 };

        // `NonNull::dangling()` 同时表示「未分配」和「零大小分配」
        RawVec {
            ptr: NonNull::dangling(),
            cap,
        }
    }

    fn grow(&mut self) {
        // 因为 T 大小为 0 时我们把容量设为 usize::MAX，
        // 能走到这里必然意味着 Vec 已满。
        assert!(mem::size_of::<T>() != 0, "capacity overflow");

        let (new_cap, new_layout) = if self.cap == 0 {
            (1, Layout::array::<T>(1).unwrap())
        } else {
            // 这不会溢出，因为我们保证 self.cap <= isize::MAX。
            let new_cap = 2 * self.cap;

            // `Layout::array` 会检查字节数 <= usize::MAX，
            // 但这是冗余的，因为 old_layout.size() <= isize::MAX，
            // 所以 `unwrap` 不应失败。
            let new_layout = Layout::array::<T>(new_cap).unwrap();
            (new_cap, new_layout)
        };

        // 确保新分配不超过 `isize::MAX` 字节。
        assert!(new_layout.size() <= isize::MAX as usize, "Allocation too large");

        let new_ptr = if self.cap == 0 {
            unsafe { alloc::alloc(new_layout) }
        } else {
            let old_layout = Layout::array::<T>(self.cap).unwrap();
            let old_ptr = self.ptr.as_ptr() as *mut u8;
            unsafe { alloc::realloc(old_ptr, old_layout, new_layout.size()) }
        };

        // 若分配失败，`new_ptr` 为 null，此时我们 abort。
        self.ptr = match NonNull::new(new_ptr as *mut T) {
            Some(p) => p,
            None => alloc::handle_alloc_error(new_layout),
        };
        self.cap = new_cap;
    }
}

impl<T> Drop for RawVec<T> {
    fn drop(&mut self) {
        let elem_size = mem::size_of::<T>();

        if self.cap != 0 && elem_size != 0 {
            unsafe {
                alloc::dealloc(
                    self.ptr.as_ptr() as *mut u8,
                    Layout::array::<T>(self.cap).unwrap(),
                );
            }
        }
    }
}
```

　　就这样。我们现在支持 push/pop 零大小类型了。我们的迭代器（不是 slice Deref 提供的那部分）仍然有问题。

## 迭代零大小类型

　　零大小 offset 是空操作。这意味着当前设计总会把 `start` 和 `end` 初始化为相同值，迭代器什么也产不出。当前做法是把指针转成整数、递增，再转回指针：

```rust,ignore
impl<T> RawValIter<T> {
    unsafe fn new(slice: &[T]) -> Self {
        RawValIter {
            start: slice.as_ptr(),
            end: if mem::size_of::<T>() == 0 {
                ((slice.as_ptr() as usize) + slice.len()) as *const _
            } else if slice.len() == 0 {
                slice.as_ptr()
            } else {
                slice.as_ptr().add(slice.len())
            },
        }
    }
}
```

　　现在我们有了另一种 bug：迭代器不是完全不跑，而是*永远*跑下去。迭代器实现里也要用同样技巧。另外，size_hint 对 ZST 会除以 0。既然我们基本上把两个指针当作指向字节，就把大小 0 映射为除以 1。`next` 如下：

```rust,ignore
fn next(&mut self) -> Option<T> {
    if self.start == self.end {
        None
    } else {
        unsafe {
            let result = ptr::read(self.start);
            self.start = if mem::size_of::<T>() == 0 {
                (self.start as usize + 1) as *const _
            } else {
                self.start.offset(1)
            };
            Some(result)
        }
    }
}
```

　　看到「bug」了吗？当时没人发现！原作者多年后在链到本页时才注意到。这段代码有点可疑，因为把迭代器指针滥用为*计数器*会让它们未对齐！使用 ZST 时我们*唯一*该做的就是保持指针对齐！*拍额头*

　　裸指针不必始终对齐，所以用指针当计数器这个基本技巧*没问题*，但传给 `ptr::read` 时*应该*对齐！对 ZST 来说 `ptr::read` 是空操作，这或许是无谓的迂腐，但让我们*稍微*负责一点，在 ZST 路径上从 `NonNull::dangling` 读取。

　　（也可以在 ZST 路径上调用 `read_unaligned`。两种都行，因为无论如何我们都是在凭空造值，编译后都是什么都不做。）

```rust,ignore
impl<T> Iterator for RawValIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<T> {
        if self.start == self.end {
            None
        } else {
            unsafe {
                if mem::size_of::<T>() == 0 {
                    self.start = (self.start as usize + 1) as *const _;
                    Some(ptr::read(NonNull::<T>::dangling().as_ptr()))
                } else {
                    let old_ptr = self.start;
                    self.start = self.start.offset(1);
                    Some(ptr::read(old_ptr))
                }
            }
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let elem_size = mem::size_of::<T>();
        let len = (self.end as usize - self.start as usize)
                  / if elem_size == 0 { 1 } else { elem_size };
        (len, Some(len))
    }
}

impl<T> DoubleEndedIterator for RawValIter<T> {
    fn next_back(&mut self) -> Option<T> {
        if self.start == self.end {
            None
        } else {
            unsafe {
                if mem::size_of::<T>() == 0 {
                    self.end = (self.end as usize - 1) as *const _;
                    Some(ptr::read(NonNull::<T>::dangling().as_ptr()))
                } else {
                    self.end = self.end.offset(-1);
                    Some(ptr::read(self.end))
                }
            }
        }
    }
}
```

　　迭代可以工作了。

　　最后一点：Vec 被 drop 时会释放存活期间分配的内存。对 ZST，我们从未分配内存；事实上永远不会。因此当前代码是不健全的：我们仍试图释放用于模拟 ZST 的 `NonNull::dangling()` 指针。若尝试释放从未分配的东西，会导致未定义行为（显然，且出于充分理由）。为修复，`RawVec` 的 `Drop` 要调整，确保只释放有大小的类型。

```rust,ignore
impl<T> Drop for RawVec<T> {
    fn drop(&mut self) {
        println!("RawVec<T> Drop called, deallocating memory");
        if self.cap != 0 && std::mem::size_of::<T>() > 0 {
            let layout = std::alloc::Layout::array::<T>(self.cap).unwrap();
            unsafe {
                std::alloc::dealloc(self.ptr.as_ptr() as *mut _, layout);
            }
        }
    }
}
```

