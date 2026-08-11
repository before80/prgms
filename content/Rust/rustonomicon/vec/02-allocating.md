+++
title = "9.2 分配"
date = 2026-08-06T17:08:00+08:00
weight = 44
type = "docs"
description = "为 Vec 分配内存"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 分配


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-alloc.html](https://doc.rust-lang.org/nomicon/vec/vec-alloc.html)


　　使用 `NonNull` 会打乱 `Vec`（以及 indeed 所有 std 集合）的一个重要特性：创建空 `Vec` 实际上根本不分配。这与分配零大小内存块不同——全局分配器不允许后者（会导致未定义行为！）。因此若不能分配，也不能在 `ptr` 里放 null pointer，`Vec::new` 怎么办？我们在里面放点别的垃圾就行！

　　这完全没问题，因为我们已有 `cap == 0` 作为「未分配」的 sentinel。几乎任何代码里都不必特殊处理，因为我们通常本来就要检查 `cap > len` 或 `len > 0`。Rust 推荐放这里的值是 `mem::align_of::<T>()`。`NonNull` 提供了便利方法：`NonNull::dangling()`。很多地方会用到 `dangling`，因为没有真正的分配可谈，但 `null` 会让编译器做坏事。

　　于是：

```rust,ignore
use std::mem;

impl<T> Vec<T> {
    pub fn new() -> Self {
        assert!(mem::size_of::<T>() != 0, "我们尚未准备好处理 ZST");
        Vec {
            ptr: NonNull::dangling(),
            len: 0,
            cap: 0,
        }
    }
}
# fn main() {}
```

　　我在那里 slipped 了一个 assert，因为零大小类型会在整段代码中需要特殊处理，我想先 defer 这个问题。没有此 assert，早期草稿会做 Very Bad Things。

　　接下来要确定*确实*需要空间时做什么。为此使用稳定 Rust 中 [`std::alloc`][std_alloc] 提供的全局分配函数 [`alloc`][alloc]、[`realloc`][realloc] 和 [`dealloc`][dealloc]。该类型稳定后，这些函数预期会被 [`std::alloc::Global`][Global] 的方法取代而 deprecated。

　　还需要处理 OOM（内存耗尽）。标准库提供 [`alloc::handle_alloc_error`][handle_alloc_error]，会以平台相关方式 abort 程序。abort 而非 panic 的原因是展开可能导致分配，而分配器刚说「没内存了」时再做分配似乎很糟。

　　当然这有点 silly，因为大多数平台不会以常规方式真正耗尽内存。若你 legitimately 占满内存，操作系统可能用别的方式杀掉应用。最可能触发 OOM 的是一次要 ludicrous 数量的内存（例如理论地址空间的一半）。因此*可能* panic 也没事。但我们尽量像标准库，所以直接 kill 整个程序。

　　好，现在可以写 grow。大致逻辑：

```text
if cap == 0:
    allocate()
    cap = 1
else:
    reallocate()
    cap *= 2
```

　　但 Rust 唯一支持的分配器 API 层级很低，需要不少额外工作。还要防范超大分配或空分配的特殊情况。

　　尤其 `ptr::offset` 会给我们带来很多麻烦，因为它的语义与 LLVM 的 GEP inbounds 指令相同。若你有幸没接触过该指令，GEP 的基本故事是：alias analysis，alias analysis，alias analysis。优化编译器要能推理数据依赖和 aliasing，这 super 重要。

　　简单例子，考虑以下代码片段：

```rust,ignore
*x *= 7;
*y *= 3;
```

　　若编译器能证明 `x` 和 `y` 指向内存中不同位置，两个操作理论上可并行（例如加载到不同寄存器独立处理）。然而编译器 generally 不能，因为若 `x` 和 `y` 指向同一位置，操作必须作用在同一值上，不能事后简单合并。

　　使用 GEP inbounds 时，你明确告诉 LLVM 即将做的偏移在单个「已分配」实体的边界内。最终 payoff 是 LLVM 可以假设：若两个指针已知指向两个不相交对象，这些指针的所有偏移也*已知*不会 alias（因为你不会随机跳到内存某处）。LLVM heavily 优化 GEP 偏移，inbounds 偏移是 best of all，因此尽量多用很重要。

　　这就是 GEP 的要点，它如何给我们找麻烦？

　　第一个问题是我们用无符号整数索引数组，但 GEP（从而 `ptr::offset`）接受有符号整数。这意味着看似有效的一半数组索引会使 GEP 溢出并 actually 往错的方向走！因此必须把所有分配限制在 `isize::MAX` 个元素。实际上只需担心按字节计的对象，例如 `> isize::MAX` 个 `u16` 会 truly 耗尽系统内存。但为避免有人把 `< isize::MAX` 个对象的数组 reinterpret 为字节的 subtle 边角，std 把所有分配限制在 `isize::MAX` 字节。

　　在 Rust 当前支持的所有 64 位目标上，我们被人为限制在远小于 64 位地址空间（现代 x64 通常只暴露 48 位寻址），因此可以先指望先耗尽内存。但在 32 位目标上，尤其那些用扩展使用更多地址空间的（PAE x86 或 x32），理论上可能成功分配超过 `isize::MAX` 字节。

　　但作为教程，这里不会特别 optimal，会无条件检查，而不是用 clever 的平台特定 `cfg`。

　　另一个边角是空分配。有两种空分配要担心：对所有 `T` 的 `cap = 0`，以及对零大小类型的 `cap > 0`。

　　这些很 tricky，归结于 LLVM 所说的「已分配」是什么意思。LLVM 对分配的理解比我们通常用的抽象得多。因为 LLVM 要配合不同语言语义和自定义分配器，它不能 really  intimately 理解分配。相反，分配背后的 main idea 是「不与其他东西重叠」。即堆分配、栈分配和全局变量不会随机重叠。Yep，又是 alias analysis。因此 Rust  technically 可以对分配的概念 play a bit fast and loose，只要*一致*。

　　回到空分配，generic 代码会导致几处要对 0 做 offset。问题是：这样做一致吗？对零大小类型，我们 concluded 对任意数量元素做 GEP inbounds offset 确实一致。这是运行时 no-op，因为每个元素占零空间，可以 pretend 在 `0x01` 有无限零大小类型被分配。没有分配器会分配该地址，因为它们 generally 不分配 `0x00`，且通常按高于字节的 minimal alignment 分配。Also generally 内存第一页整页受保护不被分配（许多平台上整整 4k）。

　　但对 positive-sized 类型呢？更 tricky。原则上可以说 offset 0 不给 LLVM 信息：元素可能在地址前或后，它无法知道。但我们 chose 保守假设它可能做坏事。因此会显式 guard 此情况。

　　*Phew*

　　好，废话结束，actually 分配内存：

```rust,ignore
use std::alloc::{self, Layout};

impl<T> Vec<T> {
    fn grow(&mut self) {
        let (new_cap, new_layout) = if self.cap == 0 {
            (1, Layout::array::<T>(1))
        } else {
            // 不会溢出，因为 self.cap <= isize::MAX
            let new_cap = 2 * self.cap;
            (new_cap, Layout::array::<T>(new_cap))
        };

        // `Layout::array` 检查分配字节数在 1..=isize::MAX，
        // 否则 error。上面条件保证不可能分配 0 字节。
        let new_layout = new_layout.expect("Allocation too large");

        let new_ptr = if self.cap == 0 {
            unsafe { alloc::alloc(new_layout) }
        } else {
            let old_layout = Layout::array::<T>(self.cap).unwrap();
            let old_ptr = self.ptr.as_ptr() as *mut u8;
            unsafe { alloc::realloc(old_ptr, old_layout, new_layout.size()) }
        };

        // 若分配失败，`new_ptr` 为 null，此时 abort。
        self.ptr = match NonNull::new(new_ptr as *mut T) {
            Some(p) => p,
            None => alloc::handle_alloc_error(new_layout),
        };
        self.cap = new_cap;
    }
}
# fn main() {}
```

[Global]: ../../std/alloc/struct.Global.html
[handle_alloc_error]: ../../alloc/alloc/fn.handle_alloc_error.html
[alloc]: ../../alloc/alloc/fn.alloc.html
[realloc]: ../../alloc/alloc/fn.realloc.html
[dealloc]: ../../alloc/alloc/fn.dealloc.html
[std_alloc]: ../../alloc/alloc/index.html
