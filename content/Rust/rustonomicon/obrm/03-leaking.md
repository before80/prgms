+++
title = "6.3 泄漏"
date = 2026-08-06T17:08:00+08:00
weight = 34
type = "docs"
description = "内存/资源泄漏与安全抽象"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 泄漏


> 原文链接: [https://doc.rust-lang.org/nomicon/leaking.html](https://doc.rust-lang.org/nomicon/leaking.html)


　　基于所有权的资源管理旨在简化组合。
　　创建对象时获取资源，销毁时释放资源。
　　由于析构自动处理，你不会忘记释放，且尽可能及时！看似完美，所有问题都解决了。

　　现实很残酷，我们又有了各种新问题要解决。

　　许多人相信 Rust 消除了资源泄漏。实践中大体如此。你很少会看到 Safe Rust 程序以失控方式泄漏资源。

　　但从理论角度，无论怎么看都绝非如此。在最严格意义上，「泄漏」抽象到无法阻止。例如，可以在程序开头初始化一个集合，填入大量带析构函数的对象，然后进入永不引用它的无限事件循环。集合会白白占着宝贵资源直到程序终止（届时 OS 反正会回收所有资源）。

　　可考虑更受限的泄漏形式：未能 drop 不可达的值。Rust 也不阻止这一点。事实上 Rust *有专门做这件事的函数*：`mem::forget`。它消费传入的值，*然后不运行其析构函数*。

　　过去 `mem::forget` 被标记为 unsafe，像 lint 一样反对使用，因为不调用析构函数通常不是良构行为（尽管对某些特殊 unsafe 代码有用）。但这最终被判定为不可持续的立场：Safe 代码中许多方式可以不调用析构函数。最著名的例子是用内部可变性创建引用计数指针环。

　　Safe 代码可以合理假设不会发生析构函数泄漏，泄漏析构函数的程序大概有问题。但 *unsafe* 代码不能依赖析构函数被运行以保证安全。对大多数类型这无关紧要：若泄漏析构函数，该类型按定义不可访问，对吧？例如泄漏 `Box<u8>` 只是浪费内存，几乎不会违反内存安全。

　　但须谨慎的是析构函数泄漏与*代理*类型。代理类型管理对独立对象的访问，但并不实际拥有它。代理对象相当罕见。你需要关心的更少。但我们将聚焦标准库中三个有趣的例子：

* `vec::Drain`
* `Rc`
* `thread::scoped::JoinGuard`

## Drain

　　`drain` 是集合 API，在不消费容器的情况下把数据移出容器。
　　这使我们在取得容器全部内容的所有权后可以复用 `Vec` 的分配。
　　它产生迭代器（Drain），按值返回 Vec 的内容。

　　考虑迭代中途的 Drain：一些值已移出，另一些还没有。这意味着 Vec 的一部分现在在逻辑上是未初始化数据！我们可在每次移除值时回移所有元素，但这有灾难性的性能后果。

　　相反，我们希望 Drain 在 drop 时修复 Vec 的底层存储。它应运行到完成，回移未移除的元素（drain 支持子范围），然后修复 Vec 的 `len`。甚至对 unwinding 也安全！听起来简单！

　　现在考虑：

```rust,ignore
let mut vec = vec![Box::new(0); 4];

{
    // 开始 drain，vec 不再可访问
    let mut drainer = vec.drain(..);

    // 取出两个元素并立即 drop
    drainer.next();
    drainer.next();

    // 丢掉 drainer，但不调用其析构函数
    mem::forget(drainer);
}

// 糟糕，`vec[0]` 已被 drop，我们在读指向已释放内存的指针！
println!("{}", vec[0]);
```

　　这显然不好。不幸的是，我们进退两难：每步保持一致状态成本巨大（会抵消 API 的任何收益）。不保持一致状态则在 safe 代码中给出未定义行为（使 API unsound）。

　　能做什么？可以选择一个表面上一致的状态：迭代开始时把 Vec 的 len 设为 0，必要时在析构函数中修复。这样一切正常执行时以最小开销得到期望行为。但若有人有*胆量*在迭代中途 `mem::forget` 我们，所做的就是*泄漏更多*（可能让 Vec 处于意外但在其他方面一致的状态）。既然我们接受 `mem::forget` 是 safe，这仍然是 safe 的。我们把泄漏导致更多泄漏称为*泄漏放大*（leak amplification）。

## Rc

　　Rc 是有趣案例，乍看似乎根本不是代理值。毕竟它管理所指向的数据，drop 所有 Rc 会 drop 该数据。泄漏 Rc 似乎并不特别危险。引用计数永久递增，阻止数据被释放或 drop，但似乎就像 Box，对吧？

　　并非如此。

　　考虑 Rc 的简化实现：

```rust,ignore
struct Rc<T> {
    ptr: *mut RcBox<T>,
}

struct RcBox<T> {
    data: T,
    ref_count: usize,
}

impl<T> Rc<T> {
    fn new(data: T) -> Self {
        unsafe {
            // heap::allocate 要是这样就好了
            let ptr = heap::allocate::<RcBox<T>>();
            ptr::write(ptr, RcBox {
                data,
                ref_count: 1,
            });
            Rc { ptr }
        }
    }

    fn clone(&self) -> Self {
        unsafe {
            (*self.ptr).ref_count += 1;
        }
        Rc { ptr: self.ptr }
    }
}

impl<T> Drop for Rc<T> {
    fn drop(&mut self) {
        unsafe {
            (*self.ptr).ref_count -= 1;
            if (*self.ptr).ref_count == 0 {
                // drop 数据然后释放
                ptr::read(self.ptr);
                heap::deallocate(self.ptr);
            }
        }
    }
}
```

　　此代码包含隐含的微妙假设：`ref_count` 能放进 `usize`，因为内存中不可能有超过 `usize::MAX` 个 Rc。但这本身假设 `ref_count` 准确反映内存中 Rc 数量，而我们知道用 `mem::forget` 这是错的。用 `mem::forget` 可使 `ref_count` 溢出，再降到 0 而仍有未 drop 的 Rc。然后可以对内部数据 use-after-free。非常糟糕。

　　可通过检查 `ref_count` 并做*某事*解决。标准库立场是直接 abort，因为程序已严重退化。而且*天哪*，这是如此荒谬的边角情况。

## thread::scoped::JoinGuard

> 注：此 API 已从 std 移除，更多信息见
> [issue #24292](https://github.com/rust-lang/rust/issues/24292)。
>
> 本节仍保留，因为我们认为此例仍然重要，
> 无论它是否属于 std。

　　`thread::scoped` API 旨在生成引用父栈数据的线程，无需对该数据的同步，方式是确保父线程在共享数据离开作用域前 join 子线程。

```rust,ignore
pub fn scoped<'a, F>(f: F) -> JoinGuard<'a>
    where F: FnOnce() + Send + 'a
```

　　这里 `f` 是另一线程执行的闭包。说 `F: Send + 'a` 表示它捕获存活 `'a` 的数据，且要么拥有该数据，要么数据是 Sync（蕴含 `&data` 是 Send）。

　　因为 JoinGuard 有生命周期，它保持父线程中它捕获的所有数据被借用。这意味着 JoinGuard 不能比另一线程正在处理的数据活得更久。JoinGuard *被* drop 时阻塞父线程，确保子线程在捕获的数据在父线程中离开作用域前终止。

　　用法大致如下：

```rust,ignore
let mut data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
{
    let mut guards = vec![];
    for x in &mut data {
        // 把可变引用 move 进闭包，在另一线程执行。
        // 闭包的生命周期由我们存入的可变引用 `x` 约束。
        // 返回的 guard 进而被赋予闭包的生命周期，
        // 因此也 mutably borrow `data`，就像 `x` 曾做的那样。
        // 这意味着 guard 消失前我们不能访问 `data`。
        let guard = thread::scoped(move || {
            *x *= 2;
        });
        // 稍后保存线程的 guard
        guards.push(guard);
    }
    // 所有 guard 在此 drop，强制线程 join
    // （此线程阻塞直到其他线程终止）。
    // 线程 join 后，借用失效，数据在此线程再次可访问。
}
// data 在此肯定已被修改。
```

　　原则上，这完全可行！Rust 所有权系统完美保证！
　　……但它依赖析构函数被调用才 safe。

```rust,ignore
let mut data = Box::new(0);
{
    let guard = thread::scoped(|| {
        // 这至少是数据竞争。最坏也是 use-after-free。
        *data += 1;
    });
    // 因为 guard 被 forget，借用失效而不阻塞此线程。
    mem::forget(guard);
}
// 因此 Box 在此 drop，而 scoped 线程可能正在尝试访问它。
```

　　糟糕。此处析构函数能否运行对 API 安全至关重要，该设计最终不得不废弃而采用完全不同的方案。
