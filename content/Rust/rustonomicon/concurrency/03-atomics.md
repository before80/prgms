+++
title = "8.3 原子操作"
date = 2026-08-06T17:08:00+08:00
weight = 41
type = "docs"
description = "原子操作与内存序"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 原子操作


> 原文链接: [https://doc.rust-lang.org/nomicon/atomics.html](https://doc.rust-lang.org/nomicon/atomics.html)


　　Rust 相当直白地从 C++20 继承 atomics 的内存模型。并非因为该模型特别优秀或易懂——事实上它相当复杂，且已知有[若干缺陷][C11-busted]。而是出于务实考虑，承认*每个人*在 atomics 建模上都不太行。至少我们可以受益于围绕 C/C++ 内存模型的现有工具与研究。（你常看到该模型被称为「C/C++11」或「C11」。C 只是复制 C++ 内存模型；C++11 是该模型首版，此后有过一些 bugfix。）

　　试图在本书中完整解释该模型相当无望。它用令人发狂的 causality 图定义，需要整本书才能从实践角度理解。若要所有细节，应查阅 [C++ 规范][C++-model]。我们仍会尝试覆盖基础以及 Rust 开发者面临的一些问题。

　　C++ 内存模型从根本上试图弥合我们想要的语义、编译器想要的优化，以及硬件所呈现的不一致混乱之间的鸿沟。*我们*希望只写程序并让它精确地做我们说的——还要快。岂不美哉？

## 编译器重排

　　编译器从根本上想做各种复杂变换以减少数据依赖、消除死代码。尤其可能大幅改变实际事件顺序，或让事件从不发生！若写：

```rust,ignore
x = 1;
y = 3;
x = 2;
```

　　编译器可能认为程序最好做：

```rust,ignore
x = 2;
y = 3;
```

　　这颠倒了事件顺序并完全消除一个事件。从单线程视角完全不可观察：所有语句执行后状态完全相同。但若程序是多线程的，我们可能依赖在 `y` 赋值前 `x` 确实被赋为 1。我们希望编译器能做这类优化，因为它们能显著提升性能。另一方面，我们也希望依赖程序*做我们说的*。

## 硬件重排

　　另一方面，即使编译器完全理解我们想要的并尊重我们的愿望，硬件也可能给我们找麻烦。麻烦来自 CPU 的 memory hierarchy。事实上硬件某处有 global 共享内存空间，但从每个 CPU 核心视角它*非常远*且*非常慢*。每个 CPU 宁愿用本地 cache，只有 cache 里没有该内存时才经历与共享内存通信的痛苦。

　　毕竟这就是 cache 的意义，对吧？若每次 cache 读都要回共享内存再次检查是否改变，有何意义？结果是硬件不保证在*一个*线程上某顺序发生的事件，在*另一*线程上以相同顺序发生。要保证这一点，必须向 CPU 发特殊指令让它不那么「聪明」。

　　例如，假设我们说服编译器生成以下逻辑：

```text
initial state: x = 0, y = 1

THREAD 1        THREAD 2
y = 3;          if x == 1 {
x = 1;              y *= 2;
                }
```

　　理想情况下程序有 2 种可能的最终状态：

* `y = 3`：（线程 2 在线程 1 完成前做检查）
* `y = 6`：（线程 2 在线程 1 完成后做检查）

　　然而硬件还允许第三种潜在状态：

* `y = 2`：（线程 2 看到 `x = 1`，但未看到 `y = 3`，然后覆盖 `y = 3`）

　　值得注意不同 CPU 提供不同保证。常见把硬件分为两类：strongly-ordered 和 weakly-ordered。最 notably x86/64 提供 strong ordering 保证，而 ARM 提供 weak ordering。这对并发编程有两条后果：

* 在 strongly-ordered 硬件上请求更强保证可能很便宜甚至免费，因为它们无条件已提供强保证。更弱保证可能只在 weakly-ordered 硬件上带来性能收益。

* 在 strongly-ordered 硬件上请求过弱保证更可能*碰巧*工作，尽管程序严格不正确。若可能，并发算法应在 weakly-ordered 硬件上测试。

## 数据访问

　　C++ 内存模型试图弥合这一鸿沟，让我们谈论程序的*因果性*（causality）。通常通过在程序部分与运行它们的线程之间建立 *happens before* 关系。这给硬件和编译器留出空间：在严格的 happens-before 未建立处更积极优化，但在已建立处强制它们更谨慎。我们通过*数据访问*和*原子访问*传达这些关系。

　　数据访问是编程世界的主食。它们从根本上未同步，编译器可积极优化。尤其编译器在假设程序单线程时可自由重排数据访问。硬件也可懒惰且不一致地把数据访问的变更传播到其他线程。关键是，数据访问是 data race 发生的方式。数据访问对硬件和编译器非常友好，但如我们所见，用它们写 synchronized 代码的语义*糟糕透顶*。实际上，这还太弱了。

　　**仅用数据访问，字面意义上不可能写出正确的 synchronized 代码。**

　　原子访问是我们告诉硬件和编译器程序是多线程的方式。每个原子访问可标记 *ordering*（内存序），指定它与其他访问建立何种关系。实践中这主要归结为告诉编译器和硬件某些它们*不能*做的事。对编译器，主要围绕指令重排；对硬件，主要围绕 write 如何传播到其他线程。Rust 暴露的 ordering 集合：

* Sequentially Consistent（SeqCst）
* Release
* Acquire
* Relaxed

　　（注：我们明确不暴露 C++ 的 *consume* ordering）

　　TODO: negative reasoning vs positive reasoning? TODO: 「不能忘记 synchronize」

## Sequentially Consistent

　　Sequentially Consistent 是最强的，蕴含所有其他 ordering 的限制。直观上，sequentially consistent 操作不能被重排：一个线程上在 SeqCst 访问前后发生的所有访问，都保持在其前后。仅使用 sequentially consistent atomics 和数据访问、且无 data race 的程序，有一个非常好的性质：存在单一 global 程序指令执行，所有线程一致认同。此执行也尤其便于推理：只是各线程各自执行的交错。若开始使用更弱 atomic ordering，这不再成立。

　　Sequential consistency 对开发者相对友好，但并非没有代价。即使在 strongly-ordered 平台上，sequential consistency 也涉及发出 memory fence。

　　实践中，sequential consistency 很少为程序正确性所必需。然而若对其他 memory order 没把握，sequential consistency 无疑是正确选择。程序稍慢当然好过不正确！之后可以机械地把 atomic 操作降级为更弱 consistency——把 `SeqCst` 改成 `Relaxed` 即可！当然，证明此变换*正确*是另一回事。

## Acquire-Release

　　Acquire 和 Release  largely  intended 成对使用。名字暗示其用例：非常适合获取和释放锁，并确保 critical section 不重叠。

　　直观上，acquire 访问确保其后的每个访问都保持在其后。然而 acquire 之前的操作可自由重排到其后。类似地，release 访问确保其前的每个访问都保持在其前。然而 release 之后的操作可自由重排到其前。

　　当线程 A release 某内存位置，随后线程 B acquire *同一*内存位置时，建立 causality。A 的 release 之前发生的每个 write（包括 non-atomic 和 relaxed atomic write）都会被 B 在 acquisition 之后观察到。然而与任何其他线程都不建立 causality。类似地，若 A 和 B 访问*不同*内存位置，也不建立 causality。

　　因此 release-acquire 的基本用法很简单：acquire 某内存位置开始 critical section，然后 release 该位置结束。例如简单 spinlock 可能如下：

```rust
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

fn main() {
    let lock = Arc::new(AtomicBool::new(false)); // 值表示「我是否已加锁？」

    // ... 以某种方式把 lock 分发给各线程 ...

    // 尝试通过设为 true 获取锁
    while lock.compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed).is_err() { }
    // 跳出循环，成功获取锁！

    // ... 可怕的数据访问 ...

    // 好了，释放锁
    lock.store(false, Ordering::Release);
}
```

　　在 strongly-ordered 平台上大多数访问有 release 或 acquire 语义，因此 release 和 acquire 往往完全免费。在 weakly-ordered 平台上则不然。

## Relaxed

　　Relaxed 访问是最弱的。可自由重排，不提供 happens-before 关系。不过 relaxed 操作仍是 atomic。即，它们不算数据访问，对它们的 read-modify-write 操作原子地发生。Relaxed 操作适合你肯定想发生、但并不特别在乎顺序的其他事。例如，若不用 counter 同步其他访问，多线程用 relaxed `fetch_add` 递增 counter 是安全的。

　　在 strongly-ordered 平台上把操作设为 relaxed 很少带来收益，因为它们通常已提供 release-acquire 语义。然而在 weakly-ordered 平台上 relaxed 操作可能更便宜。

[C11-busted]: http://plv.mpi-sws.org/c11comp/popl15.pdf
[C++-model]: https://en.cppreference.com/w/cpp/atomic/memory_order
