+++
title = "29-并发与线程"
date = 2026-07-28T14:49:00+08:00
weight = 290
type = "docs"
description = "面向 Go 用户重写并发与线程：spawn、channel、锁、`Arc`、`Send`/`Sync` 与作用域线程"
isCJKLanguage = true
draft = false

+++

并发与线程 (Concurrency And Threads)

面向 **Rust 1.97.1** (stable, 2026-07)。这篇重点不是背 API，而是先分清“线程、消息传递、共享状态、所有权边界”这四件事。

**本篇能解决什么：**
- 你是否会把 Rust 线程直接等同于 Go goroutine，结果在成本和约束上产生误解？
- 你是否想知道为什么 `Arc<Mutex<T>>` 在 Rust 并发代码里这么常见？
- 你是否总在 `Send` / `Sync`、`spawn`、借用跨线程这些报错上绕圈？
- 你是否想比较“消息传递”和“共享状态”在 Rust 里的组织方式？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| thread | — | 线程 | 操作系统线程 | goroutine 不是同一层级 |
| channel | — | 通道 | 在线程间传值的消息通道 | channel |
| `Mutex<T>` | — | 互斥锁 | 同一时刻只允许一个写访问者 | `sync.Mutex` |
| `RwLock<T>` | — | 读写锁 | 允许多读单写 | `sync.RWMutex` |
| `Send` | — | 可发送 | 所有权可安全移动到其他线程 | 近似“线程可转移” |
| `Sync` | — | 可共享 | `&T` 可安全跨线程共享 | 近似“线程安全共享” |

**热度索引：**

| 热度 | 题目 |
|------|------|
| `common` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q17](#q17), [Q18](#q18), [Q19](#q19), [Q20](#q20), [Q21](#q21) |
| `occasional` | [Q16](#q16) |

## Q1. Rust 的 `thread::spawn` 和 Go 的 goroutine 最容易混淆的点是什么？ {#q1}
**Tags:** `common` `thread` `spawn`
**适用版本:** Rust 1.0+

**一句话答案：** Rust 标准库的 `thread::spawn` 启动的是操作系统线程，不是像 goroutine 那样由语言运行时调度的轻量任务。

**详细解答：** 这会直接影响你对创建成本、共享数据方式和生命周期要求的预期。Rust 当然也有更轻量的异步任务，但那属于 async runtime，而不是这篇的线程 API。

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| 1 + 2);
    assert_eq!(handle.join().unwrap(), 3);
}
```

```rust
use std::thread;

fn main() {
    let handles: Vec<_> = (0..3).map(|n| thread::spawn(move || n * 2)).collect();

    let results: Vec<_> = handles.into_iter().map(|h| h.join().unwrap()).collect();
    assert_eq!(results, vec![0, 2, 4]);
}
```

**🐹 Go 对比：** Go 的 goroutine 更轻，常成千上万；Rust `thread::spawn` 更适合明确的线程级工作单元。

**记忆点：** 线程和异步任务是两套并发工具，不要混成一个概念。

## Q2. 为什么 `spawn` 里的闭包总让我用 `move`？ {#q2}
**Tags:** `common` `move` `spawn`
**适用版本:** Rust 1.0+

**一句话答案：** 因为新线程可能活得比当前栈帧更久，`move` 能把需要的数据所有权转进线程，避免悬垂借用。

**详细解答：** 这不意味着“一律深拷贝”；很多类型只是移动其拥有权，堆上数据本体并不会复制。

```rust
use std::thread;

fn main() {
    let text = String::from("hello");
    let handle = thread::spawn(move || text.len());
    assert_eq!(handle.join().unwrap(), 5);
}
```

```rust
use std::thread;

fn main() {
    let numbers = vec![1, 2, 3];
    let handle = thread::spawn(move || numbers.into_iter().sum::<i32>());
    assert_eq!(handle.join().unwrap(), 6);
}
```

**🐹 Go 对比：** Go 闭包默认捕获外部变量，但这也容易踩循环变量和共享可变状态的坑；Rust 则更早逼你明确所有权转移。

**记忆点：** 看到线程闭包，先问“这个数据是借用过去，还是所有权搬过去”。

## Q3. 线程间传值时，channel 在 Rust 里是什么风格？ {#q3}
**Tags:** `common` `channel`
**适用版本:** Rust 1.0+

**一句话答案：** 标准库 `mpsc` 是“多生产者，单消费者”通道，发送的是值的所有权，不是隐式共享引用。

**详细解答：** 这与 Rust 的所有权模型非常契合：发送一个值通常就意味着把它交给接收方处理。

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        tx.send(String::from("hello")).unwrap();
    });
    assert_eq!(rx.recv().unwrap(), "hello");
}
```

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let tx2 = tx.clone();

    thread::spawn(move || tx.send(1).unwrap());
    thread::spawn(move || tx2.send(2).unwrap());

    let mut got = vec![rx.recv().unwrap(), rx.recv().unwrap()];
    got.sort();
    assert_eq!(got, vec![1, 2]);
}
```

**🐹 Go 对比：** 概念上很像 channel，但 Rust 更强调“发送的是拥有权转移后的值”。

**记忆点：** `mpsc` 读作 multi-producer, single-consumer。

## Q4. 什么时候该用 channel，什么时候该用 `Arc<Mutex<T>>`？ {#q4}
**Tags:** `common` `channel` `shared-state`
**适用版本:** Rust 1.0+

**一句话答案：** 如果更像“交任务 / 交结果”，优先 channel；如果更像“多线程共同维护同一份状态”，优先共享状态加锁。

**详细解答：** 两者都合法，但设计风格不同。channel 让数据在各线程之间流动；共享状态则让多个线程围着同一份数据协作。

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    for n in 0..3 {
        let tx = tx.clone();
        thread::spawn(move || tx.send(n * 2).unwrap());
    }
    drop(tx);
    let mut values: Vec<_> = rx.iter().collect();
    values.sort();
    assert_eq!(values, vec![0, 2, 4]);
}
```

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let sum = Arc::new(Mutex::new(0));
    let handles: Vec<_> = (0..3)
        .map(|n| {
            let sum = Arc::clone(&sum);
            thread::spawn(move || *sum.lock().unwrap() += n)
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }
    assert_eq!(*sum.lock().unwrap(), 3);
}
```

**🐹 Go 对比：** Go 社区也常强调 “share memory by communicating”；Rust 因为所有权模型，更容易把这句话落成类型上的硬约束。

**记忆点：** “传消息” 和 “守同一份状态” 是两种不同建模方式。

## Q5. `Mutex<T>` 的最小正确用法是什么？ {#q5}
**Tags:** `common` `Mutex`
**适用版本:** Rust 1.0+

**一句话答案：** 把临界区缩到最小，尽快拿锁、尽快释放锁，并通过作用域让 guard 尽早 drop。

**详细解答：** `lock()` 返回的是 guard，不是裸引用；guard 离开作用域时自动解锁，这也是 Rust RAII 风格在线程同步上的直接体现。

```rust
use std::sync::Mutex;

fn main() {
    let count = Mutex::new(0);
    {
        let mut guard = count.lock().unwrap();
        *guard += 1;
    }
    assert_eq!(*count.lock().unwrap(), 1);
}
```

```rust
use std::sync::Mutex;

fn main() {
    let values = Mutex::new(vec![1]);
    {
        let mut guard = values.lock().unwrap();
        guard.push(2);
        guard.push(3);
    }
    assert_eq!(values.lock().unwrap().as_slice(), &[1, 2, 3]);
}
```

**🐹 Go 对比：** Go 常见模式是 `mu.Lock(); ...; mu.Unlock()`；Rust 则更鼓励靠作用域自动解锁，减少忘记释放的风险。

**记忆点：** guard 活多久，锁就持有多久。

## Q6. `Mutex` 的 poisoning 是什么，为什么 `unwrap()` 很常见？ {#q6}
**Tags:** `common` `Mutex` `poisoning`
**适用版本:** Rust 1.0+

**一句话答案：** 如果持锁线程在临界区 panic，锁会被标记为 poisoned；这不是死锁，而是标准库在提醒你共享状态可能已经不一致。

**详细解答：** 在很多简单程序里，直接 `unwrap()` 是合理的，因为一旦状态可能损坏，整个程序继续跑下去也未必有意义。

```rust
use std::sync::Mutex;

fn main() {
    let value = Mutex::new(1);
    assert_eq!(*value.lock().unwrap(), 1);
}
```

```rust
use std::sync::Mutex;

fn main() {
    let value = Mutex::new(vec![1, 2]);
    let lock_result = value.lock();
    match lock_result {
        Ok(guard) => assert_eq!(guard.len(), 2),
        Err(poisoned) => assert_eq!(poisoned.into_inner().len(), 2),
    }
}
```

**🐹 Go 对比：** Go 的 `sync.Mutex` 没有 poisoning 语义；Rust 选择在标准库里把“状态可能不一致”这个风险显式化。

**记忆点：** poisoned lock 还能恢复，只是你要自己决定是否值得继续信任那份数据。

## Q7. `RwLock<T>` 和 `Mutex<T>` 什么时候该切换？ {#q7}
**Tags:** `common` `RwLock`
**适用版本:** Rust 1.0+

**一句话答案：** 当读远多于写，而且读操作彼此能并行时，`RwLock<T>` 才值得考虑；否则先用 `Mutex<T>` 保持简单。

**详细解答：** `RwLock` 看起来更强，但并不总是更快。它的状态管理更复杂，而且实际性能非常依赖读写比例与平台实现。

```rust
use std::sync::RwLock;

fn main() {
    let lock = RwLock::new(String::from("hello"));
    let first = lock.read().unwrap();
    let second = lock.read().unwrap();
    assert_eq!(first.len(), second.len());
}
```

```rust
use std::sync::RwLock;

fn main() {
    let lock = RwLock::new(vec![1]);
    {
        let mut writer = lock.write().unwrap();
        writer.push(2);
    }
    assert_eq!(lock.read().unwrap().as_slice(), &[1, 2]);
}
```

**🐹 Go 对比：** 这和 `sync.RWMutex` 的取舍非常像：别因为 API 看起来“更高级”就默认选它。

**记忆点：** 没有明确读多写少证据时，优先 `Mutex`。

## Q8. `thread::scope` 为什么这么重要？ {#q8}
**Tags:** `common` `thread-scope`
**适用版本:** `thread::scope` 自 Rust 1.63+

**一句话答案：** 因为它允许子线程安全借用外层栈数据，只要这些线程保证在作用域结束前全部 join 完成。

**详细解答：** 这很大程度上缓解了“普通 `spawn` 必须 `'static`”带来的心智门槛，尤其适合短生命周期并行工作。

```rust
use std::thread;

fn main() {
    let values = vec![1, 2, 3];
    thread::scope(|scope| {
        scope.spawn(|| assert_eq!(values[0], 1));
        scope.spawn(|| assert_eq!(values.len(), 3));
    });
}
```

```rust
use std::thread;

fn main() {
    let mut data = [1, 2, 3, 4];
    let (left, right) = data.split_at_mut(2);
    thread::scope(|scope| {
        scope.spawn(move || left.iter_mut().for_each(|x| *x *= 2));
        scope.spawn(move || right.iter_mut().for_each(|x| *x *= 3));
    });
    assert_eq!(data, [2, 4, 9, 12]);
}
```

**🐹 Go 对比：** Go 不需要单独的作用域线程 API 来借用栈数据，因为借用本身不是语言模型的一部分；Rust 则把这件事做得非常显式。

**记忆点：** 短生命周期并行任务，先想 `thread::scope`。

## Q9. `Send` 和 `Sync` 怎么用最少的话记住？ {#q9}
**Tags:** `common` `Send` `Sync`
**适用版本:** Rust 1.0+

**一句话答案：** `Send` 是“值能不能搬到别的线程”，`Sync` 是“`&T` 能不能安全给别的线程共享”。

**详细解答：** 它们通常由编译器自动推导，所以你更多是在报错里认识它们，而不是手写实现它们。

```rust
fn assert_send<T: Send>(value: T) -> T {
    value
}

fn main() {
    let text = String::from("hello");
    assert_eq!(assert_send(text), "hello");
}
```

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let value = Arc::new(vec![1, 2, 3]);
    let other = Arc::clone(&value);
    let handle = thread::spawn(move || other.len());
    assert_eq!(handle.join().unwrap(), 3);
    assert_eq!(value.len(), 3);
}
```

**🐹 Go 对比：** Go 依赖 race detector 和约定检查共享安全；Rust 用 `Send` / `Sync` 把大量错误提前成编译时问题。

**记忆点：** 迁移看 `Send`，共享看 `Sync`。

## Q10. 为什么 `Rc<T>` 不能在线程间传，而 `Arc<T>` 可以？ {#q10}
**Tags:** `common` `Rc` `Arc` `Send`
**适用版本:** Rust 1.0+

**一句话答案：** 因为 `Rc<T>` 的引用计数不是原子操作，多线程同时增减会数据竞争；`Arc<T>` 专门为此做了原子化。

**详细解答：** 这类报错经常是新手第一次在并发 Rust 里真正感受到“类型系统在拦线程安全 bug”。

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let value = Arc::new(10);
    let other = Arc::clone(&value);
    let handle = thread::spawn(move || *other + 1);
    assert_eq!(handle.join().unwrap(), 11);
}
```

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let shared = Arc::new(String::from("hello"));
    let a = Arc::clone(&shared);
    let b = Arc::clone(&shared);

    let ha = thread::spawn(move || a.len());
    let hb = thread::spawn(move || b.to_uppercase());

    assert_eq!(ha.join().unwrap(), 5);
    assert_eq!(hb.join().unwrap(), "HELLO");
}
```

**🐹 Go 对比：** Go 不会在类型层面区分“单线程引用计数对象”和“多线程引用计数对象”；Rust 这里做了显式拆分。

**记忆点：** 一看到线程边界，就检查自己手里是不是还拿着 `Rc`。

## Q11. 简单计数器应该用 `Mutex` 还是原子类型？ {#q11}
**Tags:** `common` `atomic` `Mutex`
**适用版本:** Rust 1.0+

**一句话答案：** 只有一个简单整数状态时，原子类型通常更直接；涉及多个字段一致性或复杂临界区时，还是该用锁。

**详细解答：** 原子类型不是“更高级的锁替代品”，它只适合有限的一类低层状态共享。

```rust
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let hits = Arc::new(AtomicUsize::new(0));
    let other = Arc::clone(&hits);
    let handle = thread::spawn(move || {
        other.fetch_add(1, Ordering::Relaxed);
    });
    handle.join().unwrap();
    assert_eq!(hits.load(Ordering::Relaxed), 1);
}
```

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let state = Arc::new(Mutex::new((0usize, vec![])));
    let other = Arc::clone(&state);
    let handle = thread::spawn(move || {
        let mut guard = other.lock().unwrap();
        guard.0 += 1;
        guard.1.push(42);
    });
    handle.join().unwrap();
    let guard = state.lock().unwrap();
    assert_eq!(guard.0, 1);
    assert_eq!(guard.1.as_slice(), &[42]);
}
```

**🐹 Go 对比：** Go 里也有 `sync/atomic` 与锁的区分；Rust 一样不建议拿原子操作硬拼复杂一致性逻辑。

**记忆点：** 单字段小状态才优先原子，多字段一致性直接上锁。

## Q12. Rust 并发入门时最值得先养成的习惯是什么？ {#q12}
**Tags:** `common` `mental-model`
**适用版本:** Rust 1.0+

**一句话答案：** 先决定数据如何流动，再决定用线程、channel 还是锁；不要一上来就选同步原语。

**详细解答：** 很多并发设计问题并不是“该用哪把锁”，而是“这份数据到底该被转移、复制还是共享”。Rust 的类型系统会逼你回答这个问题，而这通常是好事。

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || tx.send(21).unwrap());
    assert_eq!(rx.recv().unwrap() * 2, 42);
}
```

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let total = Arc::new(Mutex::new(0));
    let workers: Vec<_> = (1..=3)
        .map(|n| {
            let total = Arc::clone(&total);
            thread::spawn(move || *total.lock().unwrap() += n)
        })
        .collect();

    for worker in workers {
        worker.join().unwrap();
    }
    assert_eq!(*total.lock().unwrap(), 6);
}
```

**🐹 Go 对比：** 这条习惯在 Go 里也成立，但 Rust 会更强硬地把“数据流设计”变成编译期约束。

**记忆点：** 先画数据流，再挑并发原语。

## Q13. Go 的 `WaitGroup` 在 Rust 里怎么做？ {#q13}
**Tags:** `common` `WaitGroup` `join` `Barrier`
**适用版本:** Rust 1.0+；`thread::scope` 自 1.63+

**一句话答案：** 最常见是收集 `JoinHandle` 再逐个 `join`；短生命周期并行用 `thread::scope`；要“大家到齐再继续”用 `Barrier`。

**解答：** Go 的 `sync.WaitGroup` 是“等一组 goroutine 结束”。Rust 标准库没有同名类型，但模式一一对应：`spawn` 返回的 handle 就是你的等待句柄；`scope` 在离开作用域时自动等完子线程（见 [Q8](#q8)）。需要 N 个线程互相等齐，再用 `std::sync::Barrier`。

```rust
use std::thread;

fn main() {
    let handles: Vec<_> = (0..3).map(|n| thread::spawn(move || n * n)).collect();
    let sum: i32 = handles.into_iter().map(|h| h.join().unwrap()).sum();
    assert_eq!(sum, 0 + 1 + 4);
}
```

```rust
use std::sync::{Arc, Barrier};
use std::thread;

fn main() {
    let barrier = Arc::new(Barrier::new(3));
    let mut handles = vec![];
    for _ in 0..3 {
        let b = Arc::clone(&barrier);
        handles.push(thread::spawn(move || {
            b.wait();
            1
        }));
    }
    let total: i32 = handles.into_iter().map(|h| h.join().unwrap()).sum();
    assert_eq!(total, 3);
}
```

**Go 对比：**

```go
package main

import "sync"

func main() {
	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
		}()
	}
	wg.Wait()
}
```

- **Go 怎么做**：`Add`/`Done`/`Wait` 等一组结束。
- **Rust 为什么不同**：`join`/`scope`/`Barrier` 分工更细，和所有权、生命周期绑在一起。
- **Go 程序员易踩的坑**：到处找 `WaitGroup` crate，却忘了 `handles` + `join` 已经够用。

**记忆点：**
- 等结束 → `join` 或 `thread::scope`。
- 等齐步 → `Barrier`。

## Q14. 怎么判断自己可能写死锁了？怎么排查？ {#q14}
**Tags:** `common` `deadlock` `Mutex`
**适用版本:** Rust 1.0+

**一句话答案：** 线程卡住且 CPU 接近空闲、多把锁交叉持有、或“持锁再等 channel/再加锁”，都要怀疑死锁；用固定加锁顺序、缩小临界区、必要时超时/`try_lock` 排查。

**解答：** Rust 编译器防数据竞争，不防逻辑死锁。典型信号：进程挂死、`top` 里线程在睡、调试器里多个线程停在 `lock`/`recv`。常见成因：A 持锁 1 等锁 2，B 持锁 2 等锁 1；或持锁时又 `recv` 依赖对方先拿到同一把锁。排查：统一全局锁顺序、尽早 `drop(guard)`、用 `try_lock` 看谁在堵、必要时加日志打印“即将加锁/已解锁”。

```rust
use std::sync::Mutex;

fn main() {
    let a = Mutex::new(1);
    let b = Mutex::new(2);
    {
        let _ga = a.lock().unwrap();
        let _gb = b.lock().unwrap(); // 约定始终先 a 后 b
        assert_eq!(*_ga + *_gb, 3);
    }
}
```

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(0);
    {
        let mut g = m.lock().unwrap();
        *g += 1;
    } // guard drop，锁已释放，后面才能再锁
    assert_eq!(*m.lock().unwrap(), 1);
}
```

**Go 对比：**

```go
package main

import "sync"

func main() {
	var mu sync.Mutex
	mu.Lock()
	// 忘记 Unlock 或交叉 Lock 同样会死锁
	mu.Unlock()
}
```

- **Go 怎么做**：同样靠纪律与工具（race detector 不专查死锁）。
- **Rust 为什么不同**：RAII guard 少“忘 Unlock”，但交叉加锁照样死。
- **Go 程序员易踩的坑**：以为“能编译 = 不会卡死”。

**记忆点：**
- 编译通过 ≠ 不会死锁。
- 固定锁顺序 + 缩短持锁时间。

## Q15. channel 对端关闭后发送/接收会发生什么？ {#q15}
**Tags:** `common` `channel` `mpsc`
**适用版本:** Rust 1.0+

**一句话答案：** 所有 `Sender` 都 drop 后，`recv` 得到 `Err`（断开）；接收端已挂、再 `send` 也会得到 `Err`。不要对已关闭通道假设还能传值。

**解答：** `mpsc` 里“关闭”不是单独的 `close()` 调用，而是发送端全部被 drop。此时 `rx.recv()` 返回 `Err(RecvError)`，`rx.iter()` 结束；若接收端先没了，`tx.send(...)` 返回 `Err(SendError(_))` 并把值还你。多生产者时要等最后一个 `Sender` 也 drop，接收端才会看到“通道关了”。

```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel::<i32>();
    drop(tx);
    assert!(rx.recv().is_err());
}
```

```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    drop(rx);
    assert!(tx.send(1).is_err());
}
```

**Go 对比：**

```go
package main

func main() {
	ch := make(chan int)
	close(ch)
	_, ok := <-ch
	_ = ok // false，已关闭
}
```

- **Go 怎么做**：显式 `close`；向已关闭 channel 发送会 panic。
- **Rust 为什么不同**：靠 drop 发送端关闭；`send`/`recv` 用 `Result` 表达失败，而不是发送侧 panic。
- **Go 程序员易踩的坑**：找 `close(tx)`，或克隆了 `tx` 却忘 drop 克隆，接收端永远等。

**记忆点：**
- 发送端全 drop → 接收结束。
- 接收端没了 → `send` 返回 `Err`。

## Q16. CPU 密集要不要上 `rayon`？Rust 为啥没有 Go 那种 data race detector？ {#q16}
**Tags:** `occasional` `rayon` `data-race` `Send` `Sync`
**适用版本:** Rust 1.0+（`rayon` 为外部 crate）

**一句话答案：** CPU 密集的数据并行可优先考虑 `rayon`；Rust 靠类型系统（`Send`/`Sync`）在编译期挡数据竞争，所以没有 Go 那种默认的动态 race detector 作为主力工具。

**解答：** `rayon` 提供并行迭代器等工作窃取线程池，适合“同一算法劈开多核算”。先确认是 CPU 瓶颈且任务可独立分片，再引入依赖；I/O 等待型并发更常看线程/async/channel。引入方式用命令而不是在文档里假装已有依赖：

```text
cargo add rayon
```

随后可在业务代码里写 `use rayon::prelude::*;` 并把 `iter()` 换成 `par_iter()`（需已加入依赖后才能编译）。Rust 为什么少谈 race detector：不安全的共享可变在安全代码里往往根本编不过（见 [Q9](#q9)、[Q10](#q10)）；真正的数据竞争多出在 `unsafe` 或 FFI，那时用 MIRI、审代码、或专门工具，而不是日常默认开一个像 Go 的 `-race`。

```rust
fn main() {
    // CPU 密集但单线程也可先写清楚，再决定是否并行
    let sum: i64 = (1..=1_000).map(|x| x * x).sum();
    assert_eq!(sum, 1_000 * 1_001 * 2_001 / 6);
}
```

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| (1..=100).sum::<i32>());
    assert_eq!(handle.join().unwrap(), 5050);
}
```

**Go 对比：**

```go
package main

func main() {
	// go test -race / go run -race 查数据竞争
	_ = 1
}
```

- **Go 怎么做**：共享内存默认宽松，靠 `-race` 动态抓竞争。
- **Rust 为什么不同**：安全子集用类型系统前置拦截；race detector 不是入门标配。
- **Go 程序员易踩的坑**：找不到 `-race` 就以为 Rust“不管竞争”；其实大量问题在编译期已经被挡住。

**记忆点：**
- 数据并行 CPU 活 → 再考虑 `cargo add rayon`。
- 防数据竞争：类型系统为主，动态检测为辅。

## Q17. Atomic 的 `Ordering` 入门怎么选？ {#q17}
**Tags:** `common` `atomic` `Ordering`
**适用版本:** Rust 1.0+

**一句话答案：** 计数器、统计、纯“原子改一下、不靠它同步别的数据”用 `Relaxed`；要搭配“释放/获取”建立线程间可见性用 `Release`/`Acquire`（或读写一体的 `AcqRel`）；拿不准且性能不是瓶颈时用 `SeqCst`。

**解答：** [Q11](#q11) 讲了“简单计数器可走原子”；本题补 **Ordering**（内存序）：它约束这次原子操作相对其他内存访问的可见顺序，不是“换成更强的 Ordering 就不会写错逻辑”。常见档位：

- **`Relaxed`**：只保证这个原子变量本身的原子性，不额外同步别的读写。
- **`Release`（写侧）/ `Acquire`（读侧）**：配对后，Release 之前的写入对随后 Acquire 的读者可见。
- **`AcqRel`**：读改写（如 `fetch_add`）时同时带 Acquire + Release。
- **`SeqCst`**：最强、最好讲清“全局总序”，开销通常最大。

```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let ready = Arc::new(AtomicBool::new(false));
    let flag = Arc::clone(&ready);
    let h = thread::spawn(move || {
        // 生产者写完数据后再 Release
        flag.store(true, Ordering::Release);
    });
    while !ready.load(Ordering::Acquire) {
        // 消费者 Acquire：看到 true 后可安全读生产者此前写入
        thread::yield_now();
    }
    h.join().unwrap();
}
```

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

fn main() {
    let hits = AtomicUsize::new(0);
    hits.fetch_add(1, Ordering::Relaxed); // 纯计数，不靠它同步其他内存
    assert_eq!(hits.load(Ordering::Relaxed), 1);
}
```

「❌ 错误直觉」——以为随便写 `Relaxed` 就能当锁用：若线程 A 先写缓冲区再 `Relaxed` 置位，线程 B `Relaxed` 看到置位后读缓冲区，**不保证**看到完整写入。需要同步可见性时，至少用 Release/Acquire（或锁/channel）。

**Go 对比：**

```go
package main

import "sync/atomic"

func main() {
	var n atomic.Uint64
	n.Add(1)
	_ = n.Load()
}
```

- **Go 怎么做**：`sync/atomic` 的操作语义更接近“足够强的原子”，很少让你在每次调用上点选 Ordering。
- **Rust 为什么不同**：把内存序暴露出来，避免为所有原子操作默认付出 `SeqCst` 成本。
- **Go 程序员易踩的坑**：把 `Relaxed` 当成“原子版普通变量赋值”，却用它去发布复杂结构。

**记忆点：**
- 纯计数 → `Relaxed`；发布/订阅可见性 → `Release`/`Acquire`；不确定 → `SeqCst`。
- Ordering 管可见性，不替代锁对临界区的保护。

## Q18. `join` 的返回值是什么？`thread::Builder` 怎么命名和调栈？ {#q18}
**Tags:** `common` `join` `Builder` `stack`
**适用版本:** Rust 1.0+

**一句话答案：** `JoinHandle<T>::join()` 得到 `Result<T>`：`Ok` 是闭包返回值，`Err` 是子线程 panic 的载荷；要设线程名或栈大小，用 `thread::Builder`，不要只靠默认 `spawn`。

**解答：** `spawn` 返回 `JoinHandle<T>`，`T` 就是闭包的返回类型。`join()` 会等线程结束并取回结果；子线程若 panic，主线程这边拿到 `Err`，可用 `is_panic()` 等方法查看，而不是默默丢结果。

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| 21 * 2);
    assert_eq!(handle.join().unwrap(), 42);

    let panicked = thread::spawn(|| panic!("boom"));
    assert!(panicked.join().is_err()); // Err 载荷是 panic 值
}
```

`thread::Builder` 可在 spawn 前配置名字（调试/日志里好认）和栈大小（递归深、大数组在栈上时才需要加）：

```rust
use std::thread;

fn main() {
    let handle = thread::Builder::new()
        .name("worker".into())
        .stack_size(2 * 1024 * 1024) // 2 MiB，按需调整
        .spawn(|| {
            assert_eq!(thread::current().name(), Some("worker"));
            7
        })
        .expect("spawn failed");
    assert_eq!(handle.join().unwrap(), 7);
}
```

注意：`Builder::spawn` 返回 `io::Result<JoinHandle<_>>`（创建线程可能因系统限制失败）；默认 `thread::spawn` 失败时会直接 panic。栈大小是平台相关的“请求值”，不是可移植精确保证。

**Go 对比：**

```go
package main

func main() {
	done := make(chan int, 1)
	go func() { done <- 42 }()
	_ = <-done
}
```

- **Go 怎么做**：goroutine 没有 `join` 返回值；常用 channel/`WaitGroup` 收回结果。栈由运行时伸缩，一般不手调。
- **Rust 为什么不同**：OS 线程 + 所有权，结果和 panic 都经 `JoinHandle` 显式交回。
- **Go 程序员易踩的坑**：`join().unwrap()` 把子线程 panic 直接打成主线程 panic，却没意识到这是在传播失败。

**记忆点：**
- `join` → `Result<T>`：值或 panic。
- 要名字/栈大小 → `thread::Builder`；`spawn` 失败要处理 `io::Result`。

## Q19. `Condvar` 最小正确用法是什么？（对标 Go `sync.Cond`） {#q19}
**Tags:** `common` `Condvar` `Mutex`
**适用版本:** Rust 1.0+

**一句话答案：** 条件变量必须和 `Mutex` 配对：持锁检查条件，不满足就 `wait`（原子地放锁并等待），改条件后 `notify_one`/`notify_all`；用 **`while` 循环** 等条件，不要只用一次 `if`。

**解答：** `std::sync::Condvar` 对应 Go 的 `sync.Cond`：不是“睡一会”的定时器，而是“等某个被互斥保护的状态变真”。经典骨架是 `(Mutex<T>, Condvar)`，常放进 `Arc` 共享。

```rust
use std::sync::{Arc, Condvar, Mutex};
use std::thread;

fn main() {
    let pair = Arc::new((Mutex::new(false), Condvar::new()));
    let pair2 = Arc::clone(&pair);

    thread::spawn(move || {
        let (lock, cvar) = &*pair2;
        let mut ready = lock.lock().unwrap();
        *ready = true;
        cvar.notify_one();
    });

    let (lock, cvar) = &*pair;
    let mut ready = lock.lock().unwrap();
    while !*ready {
        ready = cvar.wait(ready).unwrap(); // wait 返回后重新持锁，必须再检查条件
    }
    assert!(*ready);
}
```

要点：`wait` 可能因虚假唤醒返回，或通知到达时条件又被别人改掉，所以必须 `while !predicate`。先改共享状态再 `notify_*`；通知时通常仍持有（或刚改完仍逻辑相关的）那把锁，具体习惯与 Go 类似——关键是状态更新与通知之间不要把条件弄丢。

**Go 对比：**

```go
package main

import "sync"

func main() {
	var mu sync.Mutex
	cond := sync.NewCond(&mu)
	ready := false

	go func() {
		mu.Lock()
		ready = true
		cond.Signal()
		mu.Unlock()
	}()

	mu.Lock()
	for !ready {
		cond.Wait()
	}
	mu.Unlock()
}
```

- **Go 怎么做**：`Cond` 绑在 `Locker` 上；`Wait`/`Signal`/`Broadcast`。
- **Rust 为什么不同**：`wait` 吃掉并归还 `MutexGuard`，所有权把“持锁等待”写进类型。
- **Go 程序员易踩的坑**：写成 `if !ready { wait }` 只等一次；或没用同一把 `Mutex` 保护条件。

**记忆点：**
- `Mutex` + `Condvar` + `while` 条件。
- `wait` 后必须重新检查谓词。
- 改状态再 `notify_one` / `notify_all`。

## Q20. 有界 `sync_channel` 和无限 `mpsc::channel` 怎么选？ {#q20}
**Tags:** `common` `channel` `sync_channel` `backpressure`
**适用版本:** Rust 1.0+

**一句话答案：** 默认 `mpsc::channel` 是**无界**队列，发送几乎总是立刻成功（内存撑不住另说）；`sync_channel(n)` 是**有界**，队列满时发送端阻塞，用来做背压。需要限制在途任务/内存时用有界，否则无界更简单。

**解答：** 两者都是多生产者、单消费者。差别在容量与阻塞语义：

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel(); // 无界
    thread::spawn(move || {
        tx.send(1).unwrap();
        tx.send(2).unwrap();
    });
    assert_eq!(rx.recv().unwrap() + rx.recv().unwrap(), 3);
}
```

```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::sync_channel(1); // 容量 1：再多就会阻塞发送
    let h = thread::spawn(move || {
        tx.send(10).unwrap();
        tx.send(20).unwrap(); // 等接收端腾出空位
    });
    thread::sleep(Duration::from_millis(10));
    assert_eq!(rx.recv().unwrap(), 10);
    assert_eq!(rx.recv().unwrap(), 20);
    h.join().unwrap();
}
```

`sync_channel(0)` 是会合信道（rendezvous）：发送与接收必须同时就绪才交接。无界 channel 在生产者远快于消费者时会堆内存；有界则把压力传回上游。异步运行时里还有各自的有界/无界通道，那是另一套 API；标准库线程场景先分清这两个。

**Go 对比：**

```go
package main

func main() {
	unbuffered := make(chan int)    // 容量 0，会合
	buffered := make(chan int, 8)   // 有界
	_ = unbuffered
	_ = buffered
}
```

- **Go 怎么做**：`make(chan T)` / `make(chan T, n)`；没有默认“无限缓冲”的 channel。
- **Rust 为什么不同**：`channel()` 默认无界，更像“先能发再说”；要背压显式 `sync_channel`。
- **Go 程序员易踩的坑**：按 Go 无缓冲直觉去用 `channel()`，结果生产者狂发也不堵。

**记忆点：**
- `channel()` ≈ 无界；`sync_channel(n)` ≈ 有界背压。
- 防内存涨、要限流 → 有界。
- `sync_channel(0)` ≈ Go 无缓冲会合。

## Q21. 多把锁怎么定顺序，才能少死锁？ {#q21}
**Tags:** `common` `deadlock` `Mutex` `lock-order`
**适用版本:** Rust 1.0+

**一句话答案：** 给锁排一个**全局固定顺序**（例如始终先 A 后 B），所有线程遵守同一顺序；拿不到完整集合时用 `try_lock` 失败回退，并尽量缩短持锁时间。编译器不防死锁（见 [Q14](#q14)）。

**解答：** 死锁经典形：线程 1 持锁 A 等锁 B，线程 2 持锁 B 等锁 A。破解法不是“少用锁”一句话，而是**顺序纪律**：

```rust
use std::sync::Mutex;

fn read_pair(a: &Mutex<i32>, b: &Mutex<i32>) -> (i32, i32) {
    // 约定：按地址排序后加锁，消除交叉顺序
    let (first, second) = if std::ptr::from_ref(a) < std::ptr::from_ref(b) {
        (a, b)
    } else {
        (b, a)
    };
    let g1 = first.lock().unwrap();
    let g2 = second.lock().unwrap();
    (*g1, *g2)
}

fn main() {
    let x = Mutex::new(10);
    let y = Mutex::new(3);
    let (u, v) = read_pair(&x, &y);
    assert_eq!(u + v, 13);
}
```

```rust
use std::sync::Mutex;

fn main() {
    let a = Mutex::new(1);
    let b = Mutex::new(2);
    {
        let _ga = a.lock().unwrap();
        let _gb = b.lock().unwrap(); // 全项目统一：先 a 后 b
        assert_eq!(*_ga + *_gb, 3);
    } // 按相反顺序 drop 也行，关键是加锁顺序一致
}
```

实践清单：文档化锁层级（L1/L2）；禁止持锁时再调可能加同层锁的代码；持锁不做 I/O、不 `recv` 依赖对方先拿你这把锁的事；能一把锁保护的结构别拆成两把“图方便”。`try_lock` 适合“锁不住就放弃/重试”，不是替代全局顺序的银弹。

**Go 对比：**

```go
package main

import "sync"

func main() {
	var a, b sync.Mutex
	a.Lock()
	b.Lock()
	b.Unlock()
	a.Unlock()
}
```

- **Go 怎么做**：同样靠约定顺序；`sync.Mutex` 无编译期顺序检查。
- **Rust 为什么不同**：RAII 少忘解锁，但交叉加锁照样死。
- **Go 程序员易踩的坑**：以为“能编译就不死锁”；多锁场景仍要顺序表。

**记忆点：**
- 全程序统一加锁顺序。
- 持锁要短，别嵌套未知锁。
- 排查手法见 [Q14](#q14)。
