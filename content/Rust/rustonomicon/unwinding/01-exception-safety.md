+++
title = "7.1 异常安全"
date = 2026-08-06T17:08:00+08:00
weight = 36
type = "docs"
description = "异常安全等级与实践"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 异常安全


> 原文链接: [https://doc.rust-lang.org/nomicon/exception-safety.html](https://doc.rust-lang.org/nomicon/exception-safety.html)


　　尽管程序应谨慎使用展开，仍有大量代码*可能* panic。若你对 `None` 调用 `unwrap`、越界索引或除以 0，程序就会 panic。在 debug 构建中，每个算术运算在溢出时都可能 panic。除非你非常小心并严格控制运行的代码，否则几乎任何东西都可能展开，你需要做好准备。

　　为展开做好准备在更广泛的编程世界中常被称为*异常安全*（exception safety）。在 Rust 中，可以关注两个层次的异常安全：

* 在 unsafe 代码中，我们*必须*保证异常安全到不违反内存安全的程度。我们称之为*最低*异常安全。

* 在 safe 代码中，*最好*保证异常安全到程序仍能做正确之事的程度。我们称之为*最大*异常安全。

　　与 Rust 中许多地方一样，在展开方面，Unsafe 代码必须准备好应对糟糕的 Safe 代码。短暂创建 unsound 状态的代码必须小心 panic 不会导致该状态被使用。通常这意味着在这些状态存在期间只运行不会 panic 的代码，或制作在 panic 时清理状态的 guard。这并不一定意味着 panic 所目睹的状态是完全一致的——我们只需保证它是*安全*状态。

　　大多数 Unsafe 代码像叶子一样，因此相当容易做到异常安全。它控制所有运行的代码，且其中大部分不能 panic。然而 Unsafe 代码与临时未初始化数据的数组协作并反复调用调用方提供的代码并不罕见，此类代码需要谨慎考虑异常安全。

## Vec::push_all

　　`Vec::push_all` 是在没有 specialization 的情况下可靠高效地用 slice 扩展 `Vec` 的临时 hack。下面是一个简单实现：

```rust,ignore
impl<T: Clone> Vec<T> {
    fn push_all(&mut self, to_push: &[T]) {
        self.reserve(to_push.len());
        unsafe {
            let end_ptr = self.as_mut_ptr().add(self.len());

            // 不会溢出，因为我们刚刚 reserve 了
            self.set_len(self.len() + to_push.len());

            for (i, x) in to_push.iter().enumerate() {
                end_ptr.add(i).write(x.clone());
            }
        }
    }
}
```

　　我们绕过 `push`，以避免对我们确定已有容量的 `Vec` 做冗余的 capacity 和 `len` 检查。逻辑完全正确，但代码有一个 subtle 问题：它不具备异常安全！`set_len`、`add` 和 `write` 都没问题；`clone` 才是我们忽视的 panic 炸弹。

　　`Clone` 完全不受我们控制，完全可能 panic。若 panic，函数会提前退出，而 `Vec` 的 length 已被设得过大。若 `Vec` 被查看或 drop，就会读取未初始化内存！

　　此处的修复相当简单。若要保证我们*已* clone 的值被 drop，可以在每次循环迭代中设置 `len`。若只想保证未初始化内存不会被观察到，可以在循环后设置 `len`。

## BinaryHeap::sift_up

　　在堆中上浮元素比扩展 `Vec` 略复杂。伪代码如下：

```text
bubble_up(heap, index):
    while index != 0 && heap[index] < heap[parent(index)]:
        heap.swap(index, parent(index))
        index = parent(index)
```

　　将此代码字面翻译为 Rust 完全可行，但有一个恼人的性能特征：`self` 元素会被反复无用交换。我们更希望得到：

```text
bubble_up(heap, index):
    let elem = heap[index]
    while index != 0 && elem < heap[parent(index)]:
        heap[index] = heap[parent(index)]
        index = parent(index)
    heap[index] = elem
```

　　此代码确保每个元素尽可能少被复制（一般确实需要复制 `elem` 两次）。但它现在暴露了异常安全问题！在任何时候都存在同一值的两个副本。若在此函数中 panic，某物会被 double-drop。不幸的是，我们也不完全控制代码——那个比较是用户定义的！

　　与 `Vec` 不同，此处修复并不那么容易。一种做法是把用户定义代码与 unsafe 代码拆成两个阶段：

```text
bubble_up(heap, index):
    let end_index = index;
    while end_index != 0 && heap[index] < heap[parent(end_index)]:
        end_index = parent(end_index)

    let elem = heap[index]
    while index != end_index:
        heap[index] = heap[parent(index)]
        index = parent(index)
    heap[index] = elem
```

　　若用户定义代码爆炸，现在没问题了，因为我们尚未真正动堆的状态。一旦开始动堆，我们处理的只是我们信任的数据和函数，因此不必担心 panic。

　　也许你对这种设计不满意。这 surely 是作弊！而且复杂堆遍历要做*两遍*！好吧，我们硬着头皮来，*真正*地交织不可信与 unsafe 代码。

　　若 Rust 像 Java 那样有 `try` 和 `finally`，我们可以：

```text
bubble_up(heap, index):
    let elem = heap[index]
    try:
        while index != 0 && elem < heap[parent(index)]:
            heap[index] = heap[parent(index)]
            index = parent(index)
    finally:
        heap[index] = elem
```

　　基本思路很简单：若比较 panic，就把松散的元素扔进逻辑上未初始化的 index 然后 bail out。任何观察堆的人都会看到可能*不一致*的堆，但至少不会 double-drop！若算法正常结束，此操作恰好与无论如何的收尾方式一致。

　　遗憾的是 Rust 没有这种构造，我们需要自己实现！做法是把算法状态存进单独 struct，用析构函数实现「finally」逻辑。无论 panic 与否，该析构函数都会运行并为我们清理。

```rust,ignore
struct Hole<'a, T: 'a> {
    data: &'a mut [T],
    /// 从 new 到 drop，`elt` 始终为 `Some`。
    elt: Option<T>,
    pos: usize,
}

impl<'a, T> Hole<'a, T> {
    fn new(data: &'a mut [T], pos: usize) -> Self {
        unsafe {
            let elt = ptr::read(&data[pos]);
            Hole {
                data,
                elt: Some(elt),
                pos,
            }
        }
    }

    fn pos(&self) -> usize { self.pos }

    fn removed(&self) -> &T { self.elt.as_ref().unwrap() }

    fn get(&self, index: usize) -> &T { &self.data[index] }

    unsafe fn move_to(&mut self, index: usize) {
        let index_ptr: *const _ = &self.data[index];
        let hole_ptr = &mut self.data[self.pos];
        ptr::copy_nonoverlapping(index_ptr, hole_ptr, 1);
        self.pos = index;
    }
}

impl<'a, T> Drop for Hole<'a, T> {
    fn drop(&mut self) {
        // 再次填洞
        unsafe {
            let pos = self.pos;
            ptr::write(&mut self.data[pos], self.elt.take().unwrap());
        }
    }
}

impl<T: Ord> BinaryHeap<T> {
    fn sift_up(&mut self, pos: usize) {
        unsafe {
            // 取出 `pos` 处的值并创建洞
            let mut hole = Hole::new(&mut self.data, pos);

            while hole.pos() != 0 {
                let parent = parent(hole.pos());
                if hole.removed() <= hole.get(parent) { break }
                hole.move_to(parent);
            }
            // 洞会在此无条件被填上；panic 与否！
        }
    }
}
```
