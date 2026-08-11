+++
title = "8.2 Send 与 Sync"
date = 2026-08-06T17:08:00+08:00
weight = 40
type = "docs"
description = "Send/Sync 的含义与实现"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Send 与 Sync


> 原文链接: [https://doc.rust-lang.org/nomicon/send-and-sync.html](https://doc.rust-lang.org/nomicon/send-and-sync.html)


　　并非一切都服从 inherited mutability。有些类型允许在 mutate 内存位置的同时拥有多个别名。除非这些类型用同步管理访问，它们绝对不安全。Rust 通过 `Send` 和 `Sync` trait 捕获这一点。

* 若类型可以安全地发送到另一线程，则它是 Send。
* 若类型可以在线程间安全共享，则它是 Sync（`T` 是 Sync 当且仅当 `&T` 是 Send）。

　　Send 和 Sync 是 Rust 并发故事的基础。因此存在大量特殊工具使其正确工作。首先，它们是 [unsafe trait]。这意味着实现它们是不安全的，其他 unsafe 代码可以假设它们被正确实现。由于它们是*标记 trait*（没有 methods 等关联项），正确实现即意味着具有实现者应有的内在性质。错误实现 Send 或 Sync 会导致未定义行为。

　　Send 和 Sync 也是自动 derived trait。这意味着与其他 trait 不同，若类型完全由 Send 或 Sync 类型组成，则它是 Send 或 Sync。几乎所有 primitive 都是 Send 和 Sync，因此你接触的几乎所有类型都是 Send 和 Sync。

　　主要例外包括：

* raw pointer 既不是 Send 也不是 Sync（因为没有安全护栏）。
* `UnsafeCell` 不是 Sync（因此 `Cell` 和 `RefCell` 也不是）。
* `Rc` 不是 Send 或 Sync（因为 refcount 是共享且未同步的）。

　　`Rc` 和 `UnsafeCell` 从根本上不是线程安全的：它们 enable 未同步的共享可变状态。然而 raw pointer 严格来说被标为 thread-unsafe 更像是一种* lint*。对 raw pointer 做任何有用的事都需要解引用，而解引用本身已是 unsafe。从这个意义上，可以认为标为 thread-safe 也「没问题」。

　　然而它们不是 thread-safe 很重要，以防止包含它们的类型被自动标为 thread-safe。这些类型有复杂的未跟踪所有权，作者未必认真考虑过 thread safety。对 `Rc`，我们有一个好例子：包含 definitely 不是 thread-safe 的 `*mut`。

　　不能自动 derived 的类型可以按需实现：

```rust
struct MyBox(*mut u8);

unsafe impl Send for MyBox {}
unsafe impl Sync for MyBox {}
```

　　在*极其罕见*的情况下，类型被不当地自动 derived 为 Send 或 Sync，也可以 unimplement Send 和 Sync：

```rust
#![feature(negative_impls)]

// 我为某种同步原语有一些 magic 语义！
struct SpecialThreadToken(u8);

impl !Send for SpecialThreadToken {}
impl !Sync for SpecialThreadToken {}
```

　　注意*就其本身而言*不可能错误 derive Send 和 Sync。只有被其他 unsafe 代码赋予特殊含义的类型，才可能因错误 Send 或 Sync 而惹麻烦。

　　大多数 raw pointer 用法应封装在足够抽象之后，以便 derive Send 和 Sync。例如 Rust 所有标准集合尽管 pervasive 使用 raw pointer 管理分配和复杂所有权，在包含 Send 和 Sync 类型时仍是 Send 和 Sync。类似地，这些集合的大多数 iterator 是 Send 和 Sync，因为它们 largely 表现得像对集合的 `&` 或 `&mut`。

## 示例

　　[`Box`][box-doc] 因[各种原因][box-is-special]由编译器实现为特殊 intrinsic 类型，但我们可以自己实现类似行为，以看何时 sound 地实现 Send 和 Sync。叫它 `Carton`。

　　先写把栈上分配的值转移到堆上的代码。

```rust
# pub mod libc {
#    pub use ::std::os::raw::{c_int, c_void};
#    #[allow(non_camel_case_types)]
#    pub type size_t = usize;
#    unsafe extern "C" { pub fn posix_memalign(memptr: *mut *mut c_void, align: size_t, size: size_t) -> c_int; }
# }
use std::{
    mem::{align_of, size_of},
    ptr,
    cmp::max,
};

struct Carton<T>(ptr::NonNull<T>);

impl<T> Carton<T> {
    pub fn new(value: T) -> Self {
        // 在堆上分配足够存储一个 T 的内存
        assert_ne!(size_of::<T>(), 0, "零大小类型超出本例范围");
        let mut memptr: *mut T = ptr::null_mut();
        unsafe {
            let ret = libc::posix_memalign(
                (&mut memptr as *mut *mut T).cast(),
                max(align_of::<T>(), size_of::<usize>()),
                size_of::<T>()
            );
            assert_eq!(ret, 0, "分配失败或对齐无效");
        };

        // NonNull 只是确保指针非 null 的包装
        let ptr = {
            // Safety: memptr 可解引用，因为我们从引用创建且拥有独占访问
            ptr::NonNull::new(memptr)
                .expect("若 posix_memalign 返回 0 则保证非 null")
        };

        // 把值从栈移到堆上分配的位置
        unsafe {
            // Safety: 若非 null，posix_memalign 给出可写且正确对齐的 ptr
            ptr.as_ptr().write(value);
        }

        Self(ptr)
    }
}
```

　　这不太有用，用户给出值后无法访问。[`Box`][box-doc] 实现 [`Deref`][deref-doc] 和 [`DerefMut`][deref-mut-doc] 以便访问内部值。我们也来。

```rust
use std::ops::{Deref, DerefMut};

# struct Carton<T>(std::ptr::NonNull<T>);
#
impl<T> Deref for Carton<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe {
            // Safety: 指针已对齐、已初始化且可解引用，
            //   由 [`Self::new`] 的逻辑保证。我们要求读者借用 Carton，
            //   返回值的 lifetime 被 elide 到输入的 lifetime。借用检查器会
            //   强制在返回的引用 drop 之前无人能 mutate Carton 内容
            self.0.as_ref()
        }
    }
}

impl<T> DerefMut for Carton<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        unsafe {
            // Safety: 指针已对齐、已初始化且可解引用，
            //   由 [`Self::new`] 的逻辑保证。我们要求写者 mutably 借用 Carton，
            //   返回值的 lifetime 被 elide 到输入的 lifetime。借用检查器会
            //   强制在返回的可变引用 drop 之前无人能访问 Carton 内容
            self.0.as_mut()
        }
    }
}
```

　　最后，思考 `Carton` 是否 Send 和 Sync。某物可以安全 Send，除非它在不强制独占访问的情况下与其他东西共享可变状态。每个 `Carton` 有唯一指针，我们没问题。

```rust
# struct Carton<T>(std::ptr::NonNull<T>);
// Safety: 除我们外无人持有 raw pointer，若 T 可安全转移，
// 我们可以安全地把 Carton 转移到另一线程
unsafe impl<T> Send for Carton<T> where T: Send {}
```

　　Sync 呢？`Carton` 要 Sync，必须强制不能在对 `&Carton` 中某物写入的同时，从另一 `&Carton` 读或写同一某物。由于需要 `&mut Carton` 才能写指针，且借用检查器强制可变引用必须独占，sound 地使 `Carton` sync 没有问题。

```rust
# struct Carton<T>(std::ptr::NonNull<T>);
// Safety: 由于存在从 `&Carton<T>` 到 `&T` 的公开、未同步路径（如 `Deref`），
// 若 `T` 不是 Sync，则 `Carton<T>` 不能是 `Sync`。
// 反之，`Carton` 本身完全不使用内部可变性：
// 所有 mutation 都通过独占引用（`&mut`）进行。因此只要 `T` 是 `Sync`，
// `Carton<T>` 就是 `Sync` 即可：
unsafe impl<T> Sync for Carton<T> where T: Sync  {}
```

　　断言类型 Send 和 Sync 时，通常需要强制每个 contained 类型是 Send 和 Sync。写 behave 像标准库类型的自定义类型时，可以断言有相同要求。例如以下代码断言 Carton 在同类 Box 是 Send 时 Send，此例即 T 是 Send。

```rust
# struct Carton<T>(std::ptr::NonNull<T>);
unsafe impl<T> Send for Carton<T> where Box<T>: Send {}
```

　　目前 `Carton<T>` 有内存泄漏，从不释放分配的内存。修复后 Send 有新要求：需知 `free` 可在另一线程分配产生的指针上调用。可在 [`libc::free`][libc-free-docs] 文档中确认。

```rust
# struct Carton<T>(std::ptr::NonNull<T>);
# mod libc {
#     pub use ::std::os::raw::c_void;
#     unsafe extern "C" { pub fn free(p: *mut c_void); }
# }
impl<T> Drop for Carton<T> {
    fn drop(&mut self) {
        unsafe {
            libc::free(self.0.as_ptr().cast());
        }
    }
}
```

　　一个 nice 的反例是 `MutexGuard`：注意[它不是 Send][mutex-guard-not-send-docs-rs]。`MutexGuard` 的实现[使用库][mutex-guard-not-send-comment]，要求确保不尝试释放你在不同线程获得的锁。若能把 `MutexGuard` Send 到另一线程，析构函数会在你发送到的线程运行，违反该要求。`MutexGuard` 仍可以是 Sync，因为发送到另一线程的只能是 `&MutexGuard`，而 drop 引用什么都不做。

　　TODO: 更好地解释什么能或不能 Send 或 Sync。仅诉诸数据竞争是否足够？

[unsafe traits]: safe-unsafe-meaning.html
[box-doc]: https://doc.rust-lang.org/std/boxed/struct.Box.html
[box-is-special]: https://manishearth.github.io/blog/2017/01/10/rust-tidbits-box-is-special/
[deref-doc]: https://doc.rust-lang.org/core/ops/trait.Deref.html
[deref-mut-doc]: https://doc.rust-lang.org/core/ops/trait.DerefMut.html
[mutex-guard-not-send-docs-rs]: https://doc.rust-lang.org/std/sync/struct.MutexGuard.html#impl-Send-for-MutexGuard%3C'_,+T%3E
[mutex-guard-not-send-comment]: https://github.com/rust-lang/rust/issues/23465#issuecomment-82730326
[libc-free-docs]: https://linux.die.net/man/3/free
