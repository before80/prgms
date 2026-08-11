+++
title = "06-并发"
date = 2026-08-01T10:38:00+08:00
weight = 92
type = "docs"
description = "并发（Concurrency）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 并发 {#concurrency}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/concurrency/](https://doc.rust-lang.org/stable/embedded-book/concurrency/)


当程序的不同部分可能在不同时间或乱序执行时，就发生了并发。在嵌入式语境中，这包括：

* 中断处理程序，每当相关中断发生时就会运行，
* 各种形式的多线程，微处理器会定期在程序的不同部分之间切换，
* 以及在某些系统中的多核微处理器，每个核可以同时独立运行程序的不同部分。

由于许多嵌入式程序需要处理中断，并发迟早会出现，而且许多微妙且难缠的 bug 也出在这里。幸好，Rust 提供了许多抽象与安全保证，帮助我们写出正确的代码。

## 无并发 {#no-concurrency}

嵌入式程序最简单的并发就是没有并发：你的软件由一个不断运行的主循环组成，完全没有中断。有时这恰恰适合手头的问题！通常你的循环会读取一些输入、做一些处理，再写出一些输出。

```rust,ignore
#[entry]
fn main() {
    let peripherals = setup_peripherals();
    loop {
        let inputs = read_inputs(&peripherals);
        let outputs = process(inputs);
        write_outputs(&peripherals, outputs);
    }
}
```

由于没有并发，就不必担心在程序各部分之间共享数据，或同步对外设的访问。若能采用如此简单的方案，这会是很好的解决方案。

## 全局可变数据 {#global-mutable-data}

与非嵌入式 Rust 不同，我们通常没有创建堆分配并把对该数据的引用传入新创建线程的奢侈条件。相反，我们的中断处理程序可能随时被调用，并且必须知道如何访问我们正在使用的任何共享内存。在最低层，这意味着我们必须有*静态分配*的可变内存，中断处理程序和主代码都能引用它。

在 Rust 中，这类 [`static mut`] 变量的读写总是不安全的，因为若不特别小心，你可能触发竞态条件：对变量的访问做到一半时被同样访问该变量的中断打断。

[`static mut`]: https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html#accessing-or-modifying-a-mutable-static-variable

作为这种行为如何在代码中造成微妙错误的例子，考虑一个在每秒周期内对某输入信号上升沿计数的嵌入式程序（频率计）：

```rust,ignore
static mut COUNTER: u32 = 0;

#[entry]
fn main() -> ! {
    set_timer_1hz();
    let mut last_state = false;
    loop {
        let state = read_signal_level();
        if state && !last_state {
            // 危险 —— 实际上并不安全！可能导致数据竞争。
            unsafe { COUNTER += 1 };
        }
        last_state = state;
    }
}

#[interrupt]
fn timer() {
    unsafe { COUNTER = 0; }
}
```

每秒，定时器中断把计数器重置为 0。与此同时，主循环持续测量信号，并在看到从低到高的变化时递增计数器。我们必须用 `unsafe` 访问 `COUNTER`，因为它是 `static mut`，这意味着我们向编译器承诺不会造成任何未定义行为。你能发现竞态条件吗？对 `COUNTER` 的递增*并不*保证是原子的 —— 事实上，在大多数嵌入式平台上，它会拆成一次加载、然后递增、再存储。若中断在加载之后、存储之前触发，重置为 0 会在中断返回后被忽略 —— 我们就会在该周期内多计一倍的跳变。

## 临界区 {#critical-sections}

那么，我们能对数据竞争做什么？一种简单做法是使用*临界区（critical sections）*，即禁用中断的上下文。通过把 `main` 中对 `COUNTER` 的访问包在临界区里，我们可以确保在完成递增 `COUNTER` 之前定时器中断不会触发：

```rust,ignore
static mut COUNTER: u32 = 0;

#[entry]
fn main() -> ! {
    set_timer_1hz();
    let mut last_state = false;
    loop {
        let state = read_signal_level();
        if state && !last_state {
            // 新的临界区确保对 COUNTER 的同步访问
            cortex_m::interrupt::free(|_| {
                unsafe { COUNTER += 1 };
            });
        }
        last_state = state;
    }
}

#[interrupt]
fn timer() {
    unsafe { COUNTER = 0; }
}
```

在本例中我们使用 `cortex_m::interrupt::free`，但其他平台也会有在临界区中执行代码的类似机制。这也等同于禁用中断、运行一些代码，再重新启用中断。

注意我们不需要在定时器中断内放临界区，原因有二：

  * 向 `COUNTER` 写入 0 不会受竞态影响，因为我们不读取它
  * 它反正永远不会被 `main` 线程打断

若 `COUNTER` 被可能*相互抢占*的多个中断处理程序共享，那么每一个可能也需要临界区。

这解决了眼前的问题，但我们仍然要写大量需要仔细推理的 unsafe 代码，而且可能不必要地使用临界区。由于每个临界区都会暂时暂停中断处理，会带来一些额外代码体积以及更高的中断延迟与抖动（中断可能需要更长时间才被处理，且被处理前的时间更不确定）的相关成本。这是否成问题取决于你的系统，但总的来说，我们希望避免它。

值得注意的是，虽然临界区保证不会有中断触发，但它并不在多核系统上提供排他性保证！另一个核可能正愉快地访问与你的核相同的内存，即使没有中断。若你使用多个核，将需要更强的同步原语。

## 原子访问 {#atomic-access}

在某些平台上，有特殊的原子指令可用，它们为读-改-写操作提供保证。具体到 Cortex-M：`thumbv6`（Cortex-M0、Cortex-M0+）只提供原子加载与存储指令，而 `thumbv7`（Cortex-M3 及以上）提供完整的比较并交换（CAS，Compare and Swap）指令。这些 CAS 指令是粗暴禁用所有中断之外的另一种选择：我们可以尝试递增，大多数时候会成功，但若被打断，它会自动重试整个递增操作。这些原子操作甚至跨多个核也是安全的。

```rust,ignore
use core::sync::atomic::{AtomicUsize, Ordering};

static COUNTER: AtomicUsize = AtomicUsize::new(0);

#[entry]
fn main() -> ! {
    set_timer_1hz();
    let mut last_state = false;
    loop {
        let state = read_signal_level();
        if state && !last_state {
            // 使用 `fetch_add` 原子地把 COUNTER 加 1
            COUNTER.fetch_add(1, Ordering::Relaxed);
        }
        last_state = state;
    }
}

#[interrupt]
fn timer() {
    // 使用 `store` 直接把 0 写入 COUNTER
    COUNTER.store(0, Ordering::Relaxed)
}
```

这次 `COUNTER` 是安全的 `static` 变量。得益于 `AtomicUsize` 类型，`COUNTER` 可以安全地从中断处理程序和主线程修改，而无需禁用中断。在可能的情况下，这是更好的方案 —— 但你的平台可能不支持它。

关于 [`Ordering`] 的说明：它影响编译器和硬件可能如何重排指令，也对缓存可见性有影响。假设目标是单核平台，在本例中 `Relaxed` 就足够了，也是最高效的选择。更严格的排序会让编译器在原子操作周围发出内存屏障；取决于你用原子做什么，你可能需要也可能不需要这个！原子模型的精确细节很复杂，最好在别处描述。

关于原子与排序的更多细节，参见 [nomicon]。

[`Ordering`]: https://doc.rust-lang.org/core/sync/atomic/enum.Ordering.html
[nomicon]: https://doc.rust-lang.org/nomicon/atomics.html


## 抽象、Send 与 Sync {#abstractions-send-and-sync}

上面的方案都不特别令人满意。它们需要必须非常仔细检查的 `unsafe` 块，而且不人体工学。我们在 Rust 里肯定能做得更好！

我们可以把计数器抽象成可在代码其他任何地方安全使用的安全接口。对本例，我们将使用临界区计数器，但你也可以用原子做非常类似的事。

```rust,ignore
use core::cell::UnsafeCell;
use cortex_m::interrupt;

// 我们的计数器只是 UnsafeCell<u32> 的包装，它是 Rust 中
// 内部可变性的核心。通过使用内部可变性，我们可以让
// COUNTER 是 `static` 而不是 `static mut`，但仍然能够
// 修改其计数值。
struct CSCounter(UnsafeCell<u32>);

const CS_COUNTER_INIT: CSCounter = CSCounter(UnsafeCell::new(0));

impl CSCounter {
    pub fn reset(&self, _cs: &interrupt::CriticalSection) {
        // 通过要求传入 CriticalSection，我们知道必须
        // 在临界区内操作，因此可以有信心使用这个
        // unsafe 块（调用 UnsafeCell::get 所必需）。
        unsafe { *self.0.get() = 0 };
    }

    pub fn increment(&self, _cs: &interrupt::CriticalSection) {
        unsafe { *self.0.get() += 1 };
    }
}

// 允许 static CSCounter 所必需。见下方解释。
unsafe impl Sync for CSCounter {}

// COUNTER 不再是 `mut`，因为它使用内部可变性；
// 因此访问它也不再需要 unsafe 块。
static COUNTER: CSCounter = CS_COUNTER_INIT;

#[entry]
fn main() -> ! {
    set_timer_1hz();
    let mut last_state = false;
    loop {
        let state = read_signal_level();
        if state && !last_state {
            // 这里没有 unsafe！
            interrupt::free(|cs| COUNTER.increment(cs));
        }
        last_state = state;
    }
}

#[interrupt]
fn timer() {
    // 我们确实需要进入临界区，只是为了获得有效的
    // cs token，即使我们知道没有其他中断能抢占这个。
    interrupt::free(|cs| COUNTER.reset(cs));

    // 如果我们真想避免开销，也可以用 unsafe 代码
    // 生成假的 CriticalSection：
    // let cs = unsafe { interrupt::CriticalSection::new() };
}
```

我们已经把 `unsafe` 代码移到精心规划的抽象内部，现在应用代码不再包含任何 `unsafe` 块。

这种设计要求应用传入 `CriticalSection` token：这些 token 只由 `interrupt::free` 安全生成，因此通过要求传入一个，我们确保在临界区内操作，而不必自己做锁定。该保证由编译器静态提供：与 `cs` 相关不会有任何运行时开销。若我们有多个计数器，它们都可以使用同一个 `cs`，而无需多个嵌套临界区。

这还引出了 Rust 并发中的一个重要主题：[`Send` 与 `Sync`] trait。概括 *The Rust Book*：当类型可以安全移动到另一线程时它是 Send，当它可以安全地在多个线程间共享时它是 Sync。在嵌入式语境中，我们认为中断在与应用代码不同的线程中执行，因此被中断和主代码都访问的变量必须是 Sync。

[`Send` 与 `Sync`]: https://doc.rust-lang.org/nomicon/send-and-sync.html

对 Rust 中的大多数类型，这两个 trait 都由编译器自动为你派生。然而，因为 `CSCounter` 包含 [`UnsafeCell`]，它不是 Sync，因此我们不能做 `static CSCounter`：`static` 变量*必须*是 Sync，因为它们可以被多个线程访问。

[`UnsafeCell`]: https://doc.rust-lang.org/core/cell/struct.UnsafeCell.html

为了告诉编译器我们已经确保 `CSCounter` 实际上可以在线程间安全共享，我们显式实现 Sync trait。与之前使用临界区一样，这只在单核平台上是安全的：有多个核时，你需要采取更进一步的措施来确保安全。

## 互斥锁 {#mutexes}

我们已经创建了针对计数器问题的有用抽象，但还有许多用于并发的常见抽象。

其中一种*同步原语*是互斥锁（mutex），mutual exclusion 的缩写。这些构造确保对变量（例如我们的计数器）的排他访问。线程可以尝试*锁定*（或*获取*）互斥锁，要么立即成功，要么阻塞等待获取锁，要么返回无法锁定互斥锁的错误。当该线程持有锁时，它被授予对受保护数据的访问权。当线程完成时，它*解锁*（或*释放*）互斥锁，允许另一线程锁定它。在 Rust 中，我们通常用 [`Drop`] trait 实现解锁，以确保互斥锁离开作用域时总是被释放。

[`Drop`]: https://doc.rust-lang.org/core/ops/trait.Drop.html

对中断处理程序使用互斥锁可能很棘手：中断处理程序通常不能接受阻塞，若它阻塞等待主线程释放锁会尤其灾难性，因为我们会*死锁*（主线程永远不会释放锁，因为执行停在中断处理程序中）。死锁不被认为是不安全：即使在安全 Rust 中也可能发生。

为完全避免这种行为，我们可以实现一个需要临界区才能锁定的互斥锁，就像我们的计数器例子一样。只要临界区必须持续到锁持有期间，我们就能确保对包装变量的排他访问，甚至不需要跟踪互斥锁的锁定/解锁状态。

事实上 `cortex_m` crate 已经为我们做了这件事！我们可以用它这样写计数器：

```rust,ignore
use core::cell::Cell;
use cortex_m::interrupt::Mutex;

static COUNTER: Mutex<Cell<u32>> = Mutex::new(Cell::new(0));

#[entry]
fn main() -> ! {
    set_timer_1hz();
    let mut last_state = false;
    loop {
        let state = read_signal_level();
        if state && !last_state {
            interrupt::free(|cs|
                COUNTER.borrow(cs).set(COUNTER.borrow(cs).get() + 1));
        }
        last_state = state;
    }
}

#[interrupt]
fn timer() {
    // 我们仍需进入临界区以满足 Mutex。
    interrupt::free(|cs| COUNTER.borrow(cs).set(0));
}
```

我们现在使用 [`Cell`]，它与其兄弟 `RefCell` 一起用于提供安全的内部可变性。我们已经见过 `UnsafeCell`，它是 Rust 内部可变性的底层：它允许你获得对其值的多个可变引用，但只能用 unsafe 代码。`Cell` 像 `UnsafeCell`，但它提供安全接口：它只允许取当前值的副本或替换它，不允许取引用，并且由于它不是 Sync，不能在线程间共享。这些约束意味着它可以安全使用，但我们不能直接在 `static` 变量中使用它，因为 `static` 必须是 Sync。

[`Cell`]: https://doc.rust-lang.org/core/cell/struct.Cell.html

那么上面的例子为什么能工作？`Mutex<T>` 对任何是 Send 的 `T` —— 例如 `Cell` —— 实现 Sync。它能安全地这样做，是因为它只在临界区期间给出对其内容的访问。因此我们能得到一个完全没有 unsafe 代码的安全计数器！

这对我们计数器的 `u32` 这类简单类型很棒，但更复杂、非 Copy 的类型呢？嵌入式语境中极其常见的例子是外设结构体，它一般不是 Copy。对此，我们可以求助于 `RefCell`。

## 共享外设 {#sharing-peripherals}

用 `svd2rust` 生成的设备 crate 以及类似抽象通过强制同一时间只能存在外设结构体的一个实例，来提供对外设的安全访问。这确保了安全，但使从主线程和中断处理程序两者访问外设变得困难。

要安全地共享外设访问，我们可以使用前面见过的 `Mutex`。我们还需要使用 [`RefCell`]，它用运行时检查确保同一时间只给出一个对外设的引用。这比普通的 `Cell` 开销更大，但既然我们给出的是引用而不是副本，就必须确保同一时间只存在一个。

[`RefCell`]: https://doc.rust-lang.org/core/cell/struct.RefCell.html

最后，我们还必须考虑如何在主代码中初始化外设之后，把它移入共享变量。为此我们可以使用 `Option` 类型，初始化为 `None`，稍后再设为外设实例。

```rust,ignore
use core::cell::RefCell;
use cortex_m::interrupt::{self, Mutex};
use stm32f4::stm32f405;

static MY_GPIO: Mutex<RefCell<Option<stm32f405::GPIOA>>> =
    Mutex::new(RefCell::new(None));

#[entry]
fn main() -> ! {
    // 获取外设单例并配置它。
    // 本例来自 svd2rust 生成的 crate，但
    // 大多数嵌入式设备 crate 会类似。
    let dp = stm32f405::Peripherals::take().unwrap();
    let gpioa = &dp.GPIOA;

    // 某种配置函数。
    // 假设它把 PA0 设为输入、PA1 设为输出。
    configure_gpio(gpioa);

    // 把 GPIOA 存入互斥锁，并移动它。
    interrupt::free(|cs| MY_GPIO.borrow(cs).replace(Some(dp.GPIOA)));
    // 我们不能再使用 `gpioa` 或 `dp.GPIOA`，而必须
    // 通过互斥锁访问它。

    // 注意只在设置 MY_GPIO 之后才启用中断：
    // 否则中断可能在它仍包含 None 时触发，
    // 而按目前的写法（使用 `unwrap()`），它会 panic。
    set_timer_1hz();
    let mut last_state = false;
    loop {
        // 我们现在通过互斥锁把状态作为数字输入读取
        let state = interrupt::free(|cs| {
            let gpioa = MY_GPIO.borrow(cs).borrow();
            gpioa.as_ref().unwrap().idr.read().idr0().bit_is_set()
        });

        if state && !last_state {
            // 若在 PA0 上看到上升沿，则把 PA1 置高。
            interrupt::free(|cs| {
                let gpioa = MY_GPIO.borrow(cs).borrow();
                gpioa.as_ref().unwrap().odr.modify(|_, w| w.odr1().set_bit());
            });
        }
        last_state = state;
    }
}

#[interrupt]
fn timer() {
    // 这次在中断中我们只是清除 PA0。
    interrupt::free(|cs| {
        // 我们可以用 `unwrap()`，因为我们知道中断在
        // MY_GPIO 设置之前不会启用；否则应处理
        // 可能为 None 的值。
        let gpioa = MY_GPIO.borrow(cs).borrow();
        gpioa.as_ref().unwrap().odr.modify(|_, w| w.odr1().clear_bit());
    });
}
```

内容不少，我们拆开重要的几行。

```rust,ignore
static MY_GPIO: Mutex<RefCell<Option<stm32f405::GPIOA>>> =
    Mutex::new(RefCell::new(None));
```

我们的共享变量现在是包着 `RefCell` 的 `Mutex`，而 `RefCell` 里包含 `Option`。`Mutex` 确保我们只在临界区期间有访问权，因此即使普通的 `RefCell` 不是 Sync，该变量也成为 Sync。`RefCell` 用引用为我们提供内部可变性，使用 `GPIOA` 时我们需要它。`Option` 让我们能把这个变量初始化为某种空值，稍后再真正移入变量。我们不能静态访问外设单例，只能在运行时访问，所以这是必需的。

```rust,ignore
interrupt::free(|cs| MY_GPIO.borrow(cs).replace(Some(dp.GPIOA)));
```

在临界区内我们可以对互斥锁调用 `borrow()`，这给我们一个对 `RefCell` 的引用。然后我们调用 `replace()` 把新值移入 `RefCell`。

```rust,ignore
interrupt::free(|cs| {
    let gpioa = MY_GPIO.borrow(cs).borrow();
    gpioa.as_ref().unwrap().odr.modify(|_, w| w.odr1().set_bit());
});
```

最后，我们以安全且并发的方式使用 `MY_GPIO`。临界区照常防止中断触发，并让我们借用互斥锁。然后 `RefCell` 给我们一个 `&Option<GPIOA>`，并跟踪它被借用多久 —— 一旦该引用离开作用域，`RefCell` 就会更新以表明它不再被借用。

由于我们不能把 `GPIOA` 移出 `&Option`，需要用 `as_ref()` 把它转成 `&Option<&GPIOA>`，最后再 `unwrap()` 得到让我们能修改外设的 `&GPIOA`。

若我们需要对共享资源的可变引用，则应改用 `borrow_mut` 和 `deref_mut`。下面的代码展示了使用 TIM2 定时器的例子。

```rust,ignore
use core::cell::RefCell;
use core::ops::DerefMut;
use cortex_m::interrupt::{self, Mutex};
use cortex_m::asm::wfi;
use stm32f4::stm32f405;

static G_TIM: Mutex<RefCell<Option<Timer<stm32::TIM2>>>> =
	Mutex::new(RefCell::new(None));

#[entry]
fn main() -> ! {
    let mut cp = cm::Peripherals::take().unwrap();
    let dp = stm32f405::Peripherals::take().unwrap();

    // 某种定时器配置函数。
    // 假设它配置 TIM2 定时器、其 NVIC 中断，
    // 最后启动定时器。
    let tim = configure_timer_interrupt(&mut cp, dp);

    interrupt::free(|cs| {
        G_TIM.borrow(cs).replace(Some(tim));
    });

    loop {
        wfi();
    }
}

#[interrupt]
fn timer() {
    interrupt::free(|cs| {
        if let Some(ref mut tim)) =  G_TIM.borrow(cs).borrow_mut().deref_mut() {
            tim.start(1.hz());
        }
    });
}

```

呼！这是安全的，但也有点笨拙。我们还能做什么吗？

## RTIC {#rtic}

一种替代方案是 [RTIC 框架]，全称 Real Time Interrupt-driven Concurrency。它强制静态优先级，并跟踪对 `static mut` 变量（「资源」）的访问，以静态确保共享资源总是被安全访问，而无需始终进入临界区并使用引用计数（如 `RefCell`）的开销。这有许多优点，例如保证无死锁，并给出极低的时间与内存开销。

[RTIC framework]: https://rtic.rs/2/book/en

RTIC 带有异步执行器，因此你的软件任务是 `async` 函数，你可以在其中使用 `async` API，以及常规的同步 API。

该框架还包括消息传递等其他功能，这减少了对显式共享状态的需求，以及在给定时间调度任务运行的能力，可用于实现周期性任务。更多信息请查阅[文档][the documentation]！

[the documentation]: https://rtic.rs

## Embassy {#embassy}

Embassy 是一组专注于使用 Rust 内置的 `async` / `await` 语法进行并发的库生态。Embassy 的核心是其[异步执行器](https://docs.rs/embassy-executor/latest/embassy_executor/)，支持大多数常见 MCU 架构。

Embassy 还采取开箱即用的方式，并提供许多其他组件，例如：

- [时间库](https://docs.rs/embassy-time/latest/embassy_time/)
- 各种同时提供时间库支持的 HAL 库。
- 用于同步原语的 [embassy-sync](https://docs.embassy.dev/embassy-sync/git/default/index.html)

你可以查看[网站](https://embassy.dev/)和[手册](https://embassy.dev/book/)获取更多信息。

## 实时操作系统 {#real-time-operating-systems}

嵌入式并发的另一种常见模型是实时操作系统（RTOS）。虽然目前在 Rust 中探索较少，但它们在传统嵌入式开发中被广泛使用。开源例子包括 [FreeRTOS] 和 [ChibiOS]。这些 RTOS 支持运行多个应用线程，CPU 在它们之间切换，要么在线程让出控制权时（称为协作式多任务），要么基于常规定时器或中断（抢占式多任务）。RTOS 通常提供互斥锁和其他同步原语，并经常与 DMA 引擎等硬件功能互操作。

[FreeRTOS]: https://freertos.org/
[ChibiOS]: http://chibios.org/

在撰写本文时，还没有很多可以指向的 Rust RTOS 例子，但这是一个有趣的领域，请持续关注！

## 多核 {#multiple-cores}

嵌入式处理器中拥有两个或更多核正变得越来越常见，这给并发增加了额外一层复杂性。所有使用临界区的例子（包括 `cortex_m::interrupt::Mutex`）都假设唯一的其他执行线程是中断线程，但在多核系统上这不再成立。相反，我们将需要为多核设计的同步原语（也称为 SMP，对称多处理）。

这些通常使用我们前面见过的原子指令，因为处理系统会确保原子性在所有核上得到保持。

详细覆盖这些主题目前超出本书范围，但一般模式与单核情况相同。
