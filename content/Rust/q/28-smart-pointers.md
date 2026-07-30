+++
title = "28-smart-pointers"
date = 2026-07-28T14:49:00+08:00
weight = 280
type = "docs"
description = "面向 Go 用户重写智能指针：Box、Rc、Arc、RefCell、Weak、Pin 与常见组合"
isCJKLanguage = true
draft = false

+++

智能指针 (Smart Pointers)

面向 **Rust 1.97.1** (stable, 2026-07)。这篇不把智能指针讲成“更多星号”，而是把它们放回所有权、共享和内部可变性的语境里。

**本篇能解决什么：**
- 你是否总把 `Box`、`Rc`、`Arc`、`RefCell`、`Mutex` 混成“都是某种指针”？
- 你是否想搞懂为什么 `Rc<RefCell<T>>`、`Arc<Mutex<T>>` 会成为固定搭配？
- 你是否不清楚 `Weak`、`Cow`、`Pin` 解决的到底是哪类具体问题？
- 你是否需要一个按“所有权 / 共享 / 可变性 / 线程”拆分的记忆方式？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| `Box<T>` | — | 盒指针 | 最简单的拥有型堆指针 | 堆上对象 |
| `Rc<T>` | Reference Counted | 引用计数指针 | 单线程共享所有权 | GC 管理对象的部分感觉 |
| `Arc<T>` | Atomically Reference Counted | 原子引用计数指针 | 多线程共享所有权 | 线程安全共享对象 |
| `RefCell<T>` | — | 运行时借用容器 | 把借用检查推迟到运行时 | 单线程可变容器 |
| `Weak<T>` | — | 弱引用 | 不增加强引用计数，常用来打破环 | 弱引用 |
| `Pin` | — | 固定位置 | 保证值在被 pin 后不再被安全移动 | Go 无直接对应物 |

**热度索引：**

| 热度 | 题目 |
|------|------|
| `common` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q16](#q16), [Q17](#q17), [Q18](#q18), [Q19](#q19), [Q20](#q20) |

## Q1. 智能指针和普通引用最本质的区别是什么？ {#q1}
**Tags:** `common` `smart-pointer` `ownership`
**适用版本:** Rust 1.0+

**一句话答案：** 普通引用只是借用视图；智能指针通常还携带所有权、引用计数、运行时借用检查或析构逻辑。

**详细解答：** 把智能指针理解成“带行为的数据结构”更准确。它们不只是某个地址，而是围绕地址建立的一套规则。

```rust
fn main() {
    let text = String::from("hello");
    let borrowed = &text;
    assert_eq!(borrowed.len(), 5);
    assert_eq!(text, "hello");
}
```

```rust
fn main() {
    let boxed = Box::new(String::from("hello"));
    assert_eq!(boxed.len(), 5);
    assert_eq!(*boxed, "hello");
}
```

**🐹 Go 对比：** Go 指针主要表达“可间接访问”；Rust 智能指针更常在表达“谁拥有、能否共享、怎样释放”。

**记忆点：** 先问它管理的是什么规则，再问它像不像指针。

## Q2. `Box<T>` 最常见的两个用途是什么？ {#q2}
**Tags:** `common` `Box`
**适用版本:** Rust 1.0+

**一句话答案：** 最常见的是把值放到堆上，以及为递归类型提供一个固定大小的间接层。

**详细解答：** `Box<T>` 是学习智能指针的起点，因为它只解决“单一所有者 + 堆分配”这件事，语义最简单。

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

fn main() {
    let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Nil))));
    assert!(matches!(list, List::Cons(1, _)));
}
```

```rust
fn consume_large(data: Box<[u8; 1024]>) -> usize {
    data.len()
}

fn main() {
    let buffer = Box::new([0u8; 1024]);
    assert_eq!(consume_large(buffer), 1024);
}
```

**🐹 Go 对比：** Go 让编译器决定是否逃逸到堆；Rust 这里是显式选择堆分配。

**记忆点：** `Box` 解决“单所有者的堆上值”，不解决共享和可变借用冲突。

## Q3. `Rc<T>` 和 `Arc<T>` 该怎么区分？ {#q3}
**Tags:** `common` `Rc` `Arc`
**适用版本:** Rust 1.0+

**一句话答案：** 二者都是共享所有权；`Rc` 只给单线程用，`Arc` 才能安全跨线程。

**详细解答：** 区别不在 API 形状，而在引用计数是否原子化。多线程需要原子计数，因此 `Arc` 会有额外开销。

```rust
use std::rc::Rc;

fn main() {
    let data = Rc::new(String::from("hello"));
    let a = Rc::clone(&data);
    let b = Rc::clone(&data);
    assert_eq!(Rc::strong_count(&data), 3);
    assert_eq!(a.as_str(), "hello");
    assert_eq!(b.as_str(), "hello");
}
```

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let value = Arc::new(String::from("hello"));
    let other = Arc::clone(&value);
    let handle = thread::spawn(move || other.len());
    assert_eq!(handle.join().unwrap(), 5);
    assert_eq!(value.len(), 5);
}
```

**🐹 Go 对比：** Go 默认所有堆对象都能在多 goroutine 间共享，但正确同步要靠你自己；Rust 先从类型上把 `Rc` 和 `Arc` 分开。

**记忆点：** 单线程优先 `Rc`，跨线程才上 `Arc`。

## Q4. 为什么 `Weak<T>` 是图和树结构里的高频工具？ {#q4}
**Tags:** `common` `Weak`
**适用版本:** Rust 1.0+

**一句话答案：** 因为 `Rc` / `Arc` 的强引用环会泄漏，`Weak` 不增加强计数，能安全表达“我知道你可能存在，但我不拥有你”。

**详细解答：** 树结构里最典型的用法是：父节点强持有子节点，子节点弱引用父节点。这样父一释放，子里的父指针就自然失效成 `None`。

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Default)]
struct Node {
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

fn main() {
    let parent = Rc::new(Node::default());
    let child = Rc::new(Node::default());

    *child.parent.borrow_mut() = Rc::downgrade(&parent);
    parent.children.borrow_mut().push(Rc::clone(&child));

    assert!(child.parent.borrow().upgrade().is_some());
}
```

```rust
use std::rc::{Rc, Weak};

fn main() {
    let weak: Weak<i32>;
    {
        let strong = Rc::new(42);
        weak = Rc::downgrade(&strong);
        assert_eq!(weak.upgrade().as_deref(), Some(&42));
    }
    assert!(weak.upgrade().is_none());
}
```

**🐹 Go 对比：** Go 有 GC，因此环不会变成传统意义的内存泄漏；Rust 的引用计数不是 tracing GC，所以必须显式打破环。

**记忆点：** “反向边常用 `Weak`” 是很实用的工程口诀。

## Q5. `Cell<T>` 和 `RefCell<T>` 的区别该怎么记？ {#q5}
**Tags:** `common` `Cell` `RefCell`
**适用版本:** Rust 1.0+

**一句话答案：** `Cell<T>` 适合整值替换，`RefCell<T>` 适合借出引用；两者都属于单线程内部可变性工具。

**详细解答：** 内部可变性指的是“即使外部只有 `&self`，内部仍然能改”。代价是：`RefCell` 把部分借用检查延后到运行时。

```rust
use std::cell::Cell;

fn main() {
    let count = Cell::new(1);
    count.set(count.get() + 1);
    assert_eq!(count.get(), 2);
}
```

```rust
use std::cell::RefCell;

fn main() {
    let values = RefCell::new(vec![1, 2]);
    values.borrow_mut().push(3);
    assert_eq!(values.borrow().len(), 3);
}
```

**🐹 Go 对比：** Go 不需要专门的“内部可变性容器”，因为默认共享可变状态本就能随时修改；Rust 则要求你显式选择这条路。

**记忆点：** `Cell` 改整个值，`RefCell` 借出后再改内容。

## Q6. `RefCell<T>` 为什么会 panic，它到底换来了什么？ {#q6}
**Tags:** `common` `RefCell` `runtime-check`
**适用版本:** Rust 1.0+

**一句话答案：** 因为它把“同一时刻要么多读要么一写”的借用规则挪到了运行时检查，违规时就会 panic。

**详细解答：** 这不是弱化规则，而是换检查时机。你得到的是更灵活的单线程共享可变结构，付出的代价是可能在运行时炸掉。

```rust
use std::cell::RefCell;

fn main() {
    let value = RefCell::new(String::from("hi"));
    {
        let mut w = value.borrow_mut();
        w.push('!');
    }
    assert_eq!(value.borrow().as_str(), "hi!");
}
```

```rust
use std::cell::RefCell;

fn main() {
    let value = RefCell::new(vec![1, 2, 3]);
    let read = value.borrow();
    assert_eq!(read.len(), 3);
    drop(read);
    value.borrow_mut().push(4);
    assert_eq!(value.borrow().len(), 4);
}
```

**🐹 Go 对比：** Go 常靠约定和测试保证“这里不会乱改”；Rust 允许你显式把这部分约束变成运行时检查。

**记忆点：** `RefCell` 不是“更自由”，而是“规则不变、检查延后”。

## Q7. 为什么 `Rc<RefCell<T>>` 经常一起出现？ {#q7}
**Tags:** `common` `Rc` `RefCell`
**适用版本:** Rust 1.0+

**一句话答案：** 因为 `Rc` 解决共享所有权，`RefCell` 解决共享后的可变访问，两者刚好互补。

**详细解答：** 这通常用于单线程图结构、UI 树、观察者模式等需要“很多地方都能拿到同一份数据，而且有人要改”的场景。

```rust
use std::cell::RefCell;
use std::rc::Rc;

fn main() {
    let shared: Rc<RefCell<Vec<i32>>> = Rc::new(RefCell::new(vec![]));
    let other = Rc::clone(&shared);
    other.borrow_mut().push(1);
    assert_eq!(shared.borrow().as_slice(), &[1]);
}
```

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Default)]
struct Counter {
    value: RefCell<u32>,
}

fn main() {
    let counter = Rc::new(Counter::default());
    let a = Rc::clone(&counter);
    let b = Rc::clone(&counter);
    *a.value.borrow_mut() += 1;
    *b.value.borrow_mut() += 2;
    assert_eq!(*counter.value.borrow(), 3);
}
```

**🐹 Go 对比：** Go 里常直接共享一个指针并修改；Rust 需要你把“共享”和“可变”这两层显式拼起来。

**记忆点：** 单线程共享可变状态，优先想到 `Rc<RefCell<T>>`。

## Q8. 多线程里为什么又变成 `Arc<Mutex<T>>`？ {#q8}
**Tags:** `common` `Arc` `Mutex`
**适用版本:** Rust 1.0+

**一句话答案：** 因为跨线程共享需要 `Arc`，跨线程可变访问需要锁；`Mutex<T>` 是最基本的一把互斥锁。

**详细解答：** 这和 `Rc<RefCell<T>>` 的结构几乎平行，只是把单线程运行时借用检查换成了线程安全锁。

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let count = Arc::new(Mutex::new(0));
    let other = Arc::clone(&count);
    let handle = thread::spawn(move || {
        *other.lock().unwrap() += 1;
    });
    handle.join().unwrap();
    assert_eq!(*count.lock().unwrap(), 1);
}
```

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let values = Arc::new(Mutex::new(vec![1]));
    let other = Arc::clone(&values);
    let handle = thread::spawn(move || {
        other.lock().unwrap().push(2);
    });
    handle.join().unwrap();
    assert_eq!(values.lock().unwrap().as_slice(), &[1, 2]);
}
```

**🐹 Go 对比：** 这最像 `sync.Mutex` + 共享对象；不同点在于 Rust 会先从类型层面禁止你把 `Rc<RefCell<T>>` 直接搬到线程里。

**记忆点：** 多线程共享可变状态，先考虑 `Arc<Mutex<T>>`。

## Q9. `Deref` 为什么能让 `Box<String>` 看起来像 `String` 一样用？ {#q9}
**Tags:** `common` `Deref`
**适用版本:** Rust 1.0+

**一句话答案：** 因为智能指针实现了 `Deref` 后，编译器会在合适场景自动做解引用和解引用强制转换。

**详细解答：** 这也是为什么很多智能指针“用起来不像指针”：方法调用和参数传递时，编译器经常会帮你沿着 `Deref` 链走到目标类型。

```rust
fn main() {
    let boxed = Box::new(String::from("hello"));
    assert_eq!(boxed.len(), 5);
    assert_eq!(boxed.to_uppercase(), "HELLO");
}
```

```rust
fn takes_str(s: &str) -> usize {
    s.len()
}

fn main() {
    let boxed = Box::new(String::from("hello"));
    assert_eq!(takes_str(&boxed), 5);
}
```

**🐹 Go 对比：** Go 没有这套 trait 驱动的自动解引用链；Rust 把它建立在 `Deref` 抽象之上。

**记忆点：** “像原值一样用” 往往来自 `Deref`，不是语法特殊照顾。

## Q10. `Drop` 的实际意义是什么，为什么不能手动调用 `Drop::drop`？ {#q10}
**Tags:** `common` `Drop`
**适用版本:** Rust 1.0+

**一句话答案：** `Drop` 用来在值离开作用域时自动清理资源；你可以提前 `drop(value)`，但不能直接手动调析构方法本身。

**详细解答：** Rust 要保证析构只发生一次，所以不允许你随便直接调用 `Drop::drop`。标准做法是让作用域结束，或调用 `std::mem::drop` 提前释放。

```rust
use std::cell::RefCell;
use std::rc::Rc;

struct Loud(Rc<RefCell<Vec<&'static str>>>);

impl Drop for Loud {
    fn drop(&mut self) {
        self.0.borrow_mut().push("dropped");
    }
}

fn main() {
    let events = Rc::new(RefCell::new(vec![]));
    {
        let _value = Loud(Rc::clone(&events));
    }
    assert_eq!(events.borrow().as_slice(), &["dropped"]);
}
```

```rust
use std::cell::RefCell;
use std::mem;
use std::rc::Rc;

struct Loud(Rc<RefCell<Vec<&'static str>>>);

impl Drop for Loud {
    fn drop(&mut self) {
        self.0.borrow_mut().push("dropped");
    }
}

fn main() {
    let events = Rc::new(RefCell::new(vec![]));
    let value = Loud(Rc::clone(&events));
    mem::drop(value);
    assert_eq!(events.borrow().as_slice(), &["dropped"]);
}
```

**🐹 Go 对比：** Go 更依赖 GC 和 `defer`；Rust 的 `Drop` 更接近“离开作用域自动析构”。

**记忆点：** 想提前释放就用 `drop(value)`，不要碰 `Drop::drop`。

## Q11. `Cow<'a, T>` 真正适合哪类场景？ {#q11}
**Tags:** `common` `Cow`
**适用版本:** Rust 1.0+

**一句话答案：** 当“多数情况下只借用、少数情况下才需要拷贝并修改”时，`Cow` 非常合适。

**详细解答：** `Cow` 是 **Clone-on-Write** 的缩写。它避免了“永远分配新 `String`”和“永远只能借用”这两种极端。

```rust
use std::borrow::Cow;

fn normalize(s: &str) -> Cow<'_, str> {
    if s.contains(' ') {
        Cow::Owned(s.replace(' ', "_"))
    } else {
        Cow::Borrowed(s)
    }
}

fn main() {
    assert_eq!(normalize("a b"), "a_b");
    assert_eq!(normalize("ab"), "ab");
}
```

```rust
use std::borrow::Cow;

fn main() {
    let mut value: Cow<'_, str> = Cow::Borrowed("hi");
    value.to_mut().push('!');
    assert_eq!(value, "hi!");
}
```

**🐹 Go 对比：** Go 字符串不可变，很多 API 会直接返回新字符串；Rust 的 `Cow` 则能把“是否复制”延后到真正需要修改时。

**记忆点：** “大多数借用，少数拥有” 是 `Cow` 的主场。

## Q12. `Pin` 为什么常跟 async 和自引用类型一起出现？ {#q12}
**Tags:** `common` `Pin`
**适用版本:** `Pin` 自 Rust 1.33+

**一句话答案：** 因为某些值一旦内部形成“指向自身一部分”的关系，就不能再被安全移动，而 `Pin` 正是在表达这种限制。

**详细解答：** 应用代码不一定天天手写 `Pin`，但只要碰到自定义 future、异步底层实现或自引用抽象，迟早会见到它。

```rust
use std::pin::Pin;

fn pin_ref<T: Unpin>(value: &mut T) -> Pin<&mut T> {
    Pin::new(value)
}

fn main() {
    let mut n = 5;
    let pinned = pin_ref(&mut n);
    assert_eq!(*pinned.as_ref().get_ref(), 5);
}
```

```rust
use std::future::Future;
use std::pin::pin;
use std::task::{Context, Poll, Waker};

async fn ready_value() -> i32 {
    7
}

fn main() {
    let waker = Waker::noop();
    let mut cx = Context::from_waker(waker);
    let mut fut = pin!(ready_value());
    match Future::poll(fut.as_mut(), &mut cx) {
        Poll::Ready(value) => assert_eq!(value, 7),
        Poll::Pending => panic!("unexpected pending"),
    }
}
```

**🐹 Go 对比：** Go 不暴露这类“值是否还能移动”的类型级约束；Rust 为了支持自引用状态机，把这层细节显式化了。

**记忆点：** 看到 `Pin`，先想到“某些移动会破坏内部不变式”。

## Q13. 什么时候用 `Box`，什么时候 `Rc`/`Arc`？ {#q13}
**Tags:** `common` `Box` `Rc` `Arc`
**适用版本:** Rust 1.0+

**一句话答案：** 只有一个所有者时用 `Box`；单线程多所有者用 `Rc`；要跨线程共享再用 `Arc`。

**解答：** 选型先问两件事：要不要共享所有权，以及要不要跨线程。`Box` 最简单——独占堆上值，适合递归类型、大对象上堆、`Box<dyn Trait>`。一旦多个地方都要“拥有同一份”，才升级到引用计数；多线程再换成原子版 `Arc`（见 [Q3](#q3)）。

```rust
fn main() {
    let alone = Box::new(String::from("only-me"));
    let moved = alone;
    assert_eq!(*moved, "only-me");
}
```

```rust
use std::rc::Rc;

fn main() {
    let shared = Rc::new(vec![1, 2, 3]);
    let a = Rc::clone(&shared);
    let b = Rc::clone(&shared);
    assert_eq!(a.len() + b.len(), 6);
    assert_eq!(Rc::strong_count(&shared), 3);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	p := new(int)
	*p = 7
	q := p // 多别名，GC 管生命周期
	fmt.Println(*p, *q)
}
```

- **Go 怎么做**：堆对象天然可多指针共享，生命周期靠 GC。
- **Rust 为什么不同**：`Box`/`Rc`/`Arc` 把“独占 / 单线程共享 / 跨线程共享”写进类型。
- **Go 程序员易踩的坑**：一上来就 `Rc`/`Arc`，其实很多地方 `Box` 或普通拥有值就够。

**记忆点：**
- 独占 → `Box`；同线程共享 → `Rc`；跨线程 → `Arc`。
- 先问“几个所有者”，再问“几个线程”。

## Q14. `Rc` 成环会泄漏吗？`Weak` 怎么解？ {#q14}
**Tags:** `common` `Rc` `Weak` `leak`
**适用版本:** Rust 1.0+

**一句话答案：** 会：强引用环让强计数永远到不了 0，内存不会释放；把反向边改成 `Weak` 就能打破环。

**解答：** `Rc`/`Arc` 不是 tracing GC，只靠强引用计数。A 强持有 B、B 又强持有 A 时，双方计数都 ≥1，作用域结束也清不掉。树/图里常见做法：父→子用 `Rc`，子→父用 `Weak`（见 [Q4](#q4)）。`upgrade()` 得到 `Option<Rc<_>>`：父还在则 `Some`，已释放则 `None`。

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(1);
    let b = Rc::clone(&a);
    assert_eq!(Rc::strong_count(&a), 2);
    drop(b);
    assert_eq!(Rc::strong_count(&a), 1);
}
```

```rust
use std::rc::{Rc, Weak};

fn main() {
    let strong = Rc::new(String::from("alive"));
    let weak: Weak<String> = Rc::downgrade(&strong);
    assert_eq!(weak.upgrade().as_deref().map(String::as_str), Some("alive"));
    drop(strong);
    assert!(weak.upgrade().is_none());
}
```

**Go 对比：**

```go
package main

type Node struct {
	Parent   *Node
	Children []*Node
}

func main() {
	p := &Node{}
	c := &Node{Parent: p}
	p.Children = append(p.Children, c)
	_ = p
}
```

- **Go 怎么做**：环对 GC 通常不是泄漏；对象不可达才会收。
- **Rust 为什么不同**：引用计数环会真泄漏，必须显式 `Weak`。
- **Go 程序员易踩的坑**：以为“有 GC 的语言才有环问题”，反而在 Rust 里忽略环。

**记忆点：**
- 强环 = 泄漏；反向边优先 `Weak`。
- `upgrade` 失败说明强所有者已经没了。

## Q15. `RefCell` 和 `Mutex` 怎么区分（单线程内部可变 vs 多线程）？ {#q15}
**Tags:** `common` `RefCell` `Mutex`
**适用版本:** Rust 1.0+

**一句话答案：** `RefCell` 是单线程运行时借用检查；`Mutex` 是多线程互斥锁。固定搭配常是 `Rc<RefCell<T>>` 与 `Arc<Mutex<T>>`。

**解答：** 两者都解决“外部不可变、内部要改”，但线程模型不同。`RefCell` 违规会 panic，不能跨线程；`Mutex` 用锁串行化访问，可与 `Arc` 一起跨线程（见 [Q7](#q7)、[Q8](#q8)）。单线程图结构别无端上锁；多线程别拿 `RefCell` 硬闯。

```rust
use std::cell::RefCell;

fn main() {
    let n = RefCell::new(0);
    *n.borrow_mut() += 1;
    assert_eq!(*n.borrow(), 1);
}
```

```rust
use std::sync::Mutex;

fn main() {
    let n = Mutex::new(0);
    *n.lock().unwrap() += 1;
    assert_eq!(*n.lock().unwrap(), 1);
}
```

**Go 对比：**

```go
package main

import "sync"

func main() {
	var mu sync.Mutex
	x := 0
	mu.Lock()
	x++
	mu.Unlock()
	_ = x
}
```

- **Go 怎么做**：共享可变几乎总靠锁或 channel；没有 `RefCell` 这种单线程专用工具。
- **Rust 为什么不同**：先按线程边界选型，避免把锁开销带进单线程代码。
- **Go 程序员易踩的坑**：凡是“要改共享状态”就直接 `Mutex`，忽略单线程场景的 `RefCell`。

**记忆点：**
- 单线程内部可变 → `RefCell`；多线程 → `Mutex`。
- 口诀：`Rc+RefCell`，`Arc+Mutex`。

## Q16. Go 里的指针/堆对象，在 Rust 常映射成什么？ {#q16}
**Tags:** `common` `go-compare` `Box` `Rc` `Arc`
**适用版本:** Rust 1.0+

**一句话答案：** Go 的 `*T`/堆对象常对应 Rust 的拥有值、`Box`、或显式共享的 `Rc`/`Arc`（再加可变包装）；没有“默认多别名 + GC”的单一映射。

**解答：** Go 指针拷贝只是多一个别名；Rust 赋值经常是 move。堆上独占 → `Box`；只读共享可多 `Rc`/`Arc`；还要改则叠 `RefCell`/`Mutex`。很多时候甚至不必指针：`String`、`Vec`、结构体本身已是拥有型值。先问所有权与可变性，再选智能指针。

```rust
fn main() {
    let owned = String::from("heap-ish");
    let boxed = Box::new(owned);
    assert_eq!(boxed.as_str(), "heap-ish");
}
```

```rust
use std::sync::{Arc, Mutex};

fn main() {
    let shared = Arc::new(Mutex::new(0));
    let other = Arc::clone(&shared);
    *other.lock().unwrap() = 42;
    assert_eq!(*shared.lock().unwrap(), 42);
}
```

**Go 对比：**

```go
package main

import "fmt"

type Counter struct{ N int }

func main() {
	c := &Counter{N: 1}
	alias := c
	alias.N = 2
	fmt.Println(c.N) // 2，同一对象
}
```

- **Go 怎么做**：`new`/`&` 得到可共享堆对象，GC 回收。
- **Rust 为什么不同**：共享与可变都要显式选型，编译器拦不安全别名。
- **Go 程序员易踩的坑**：把每个 `*T` 都翻译成 `Box`，或反过来到处 `&` 却忘了生命周期。

**记忆点：**
- Go `*T` ≠ 固定等于 Rust 某一种指针。
- 映射轴是：独占 / 共享 / 可变 / 是否跨线程。

## Q17. `Deref` / `DerefMut` 和方法解析到底怎么配合？ {#q17}
**Tags:** `common` `Deref` `DerefMut` `method-resolution`
**适用版本:** Rust 1.0+

**一句话答案：** 方法调用时，编译器会沿 `Deref`（可变场景再沿 `DerefMut`）自动解引用，直到找到匹配方法；赋值、字段访问等场景不会无限制地帮你“像原类型一样处处等价”。

**解答：** **Deref**（解引用 trait）让智能指针在方法调用、部分参数强制转换时表现得像内部类型；**DerefMut** 则对应可变路径。`Box`/`Rc`/`String`/`Vec` 都靠这套机制。注意：方法解析会自动解引用，但 `*` 解引用、模式匹配、部分运算符重载仍要你自己写清楚。自写类型实现 `Deref` 时，目标应是“智能指针语义”，不要拿它当随意的隐式转换工具。

```rust
fn main() {
    let boxed = Box::new(String::from("hello"));
    assert_eq!(boxed.len(), 5);
    assert_eq!(boxed.chars().count(), 5);
}
```

```rust
use std::ops::{Deref, DerefMut};

struct Wrap(String);

impl Deref for Wrap {
    type Target = String;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Wrap {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

fn main() {
    let mut w = Wrap(String::from("hi"));
    w.push('!');
    assert_eq!(w.as_str(), "hi!");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	p := new(string)
	*p = "hello"
	fmt.Println(len(*p))
}
```

- **Go 怎么做**：方法集在 `T` 与 `*T` 之间有固定规则，没有 `Deref` 链。
- **Rust 为什么不同**：用 trait 表达“指针样类型如何露出内部值”。
- **Go 程序员易踩的坑**：以为实现了 `Deref` 就处处等于内部类型；赋值与所有权规则仍按外层类型走。

**记忆点：**
- 方法调用常自动 `Deref`；可变方法走 `DerefMut`。
- `Deref` 是智能指针协议，不是通用隐式转换。

## Q18. `Rc::make_mut` / `Arc::make_mut` 的写时克隆是什么？ {#q18}
**Tags:** `common` `Rc` `Arc` `make_mut`
**适用版本:** Rust 1.0+（`Rc`/`Arc`）；`make_mut` 为标准库长期稳定 API

**一句话答案：** `make_mut` 在强引用计数为 1 时直接给出可变借用；若还有其它强引用，则先克隆一份再可变——典型的写时克隆（clone-on-write）。

**解答：** 适合“多数只读共享，偶尔要改且改完只影响自己这份”的数据。它不会动弱引用计数逻辑以外的魔法：有别人还强持有同一块时，你改的是克隆后的新分配。需要“改一处、所有别名一起变”时，应改用 `RefCell`/`Mutex` 等内部可变性，而不是 `make_mut`。

```rust
use std::rc::Rc;

fn main() {
    let mut a = Rc::new(vec![1, 2]);
    let b = Rc::clone(&a);
    assert_eq!(Rc::strong_count(&a), 2);
    Rc::make_mut(&mut a).push(3);
    assert_eq!(a.as_slice(), &[1, 2, 3]);
    assert_eq!(b.as_slice(), &[1, 2]);
    assert_eq!(Rc::strong_count(&a), 1);
}
```

```rust
use std::sync::Arc;

fn main() {
    let mut a = Arc::new(String::from("hi"));
    assert_eq!(Arc::strong_count(&a), 1);
    Arc::make_mut(&mut a).push('!');
    assert_eq!(a.as_str(), "hi!");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := []int{1, 2}
	b := append([]int(nil), a...) // 显式拷一份再改
	b = append(b, 3)
	fmt.Println(a, b)
}
```

- **Go 怎么做**：共享切片/map 时靠约定拷贝；没有内建 `make_mut`。
- **Rust 为什么不同**：引用计数指针能在“唯一所有者”时原地改，多所有者时自动拆分。
- **Go 程序员易踩的坑**：以为 `make_mut` 会就地改所有 `Rc` 别名；有克隆时只改自己那份。

**记忆点：**
- 唯一强引用 → 原地可变；否则先克隆。
- 要共享可变状态，别用 `make_mut` 冒充。

## Q19. 什么时候别急着上 `Rc` / `Arc`？ {#q19}
**Tags:** `common` `Rc` `Arc` `api-design`
**适用版本:** Rust 1.0+

**一句话答案：** 单一所有者、能 `move`、能按值返回、或短期借用就够时，先用拥有值 / `Box` / 普通引用；只有真正出现“多个所有者同时活着”再上引用计数。

**解答：** 过早 `Rc` 会带来：计数开销、更难推理的生命周期、成环泄漏风险、以及“到处 `clone` 指针”的 API 味道。优先顺序常见是：拥有并转移 → 借用 → `Box` 独占堆 → 最后才 `Rc`/`Arc`（见 [Q13](#q13)）。树若只有父拥有子，子不必反向强持有父；需要回调时也可以先传 `&T`/`&mut T`。

```rust
fn consume(s: String) -> usize {
    s.len()
}

fn main() {
    let text = String::from("hello");
    assert_eq!(consume(text), 5);
}
```

```rust
fn total(nums: &[i32]) -> i32 {
    nums.iter().sum()
}

fn main() {
    let data = vec![1, 2, 3];
    assert_eq!(total(&data), 6);
    assert_eq!(data.len(), 3);
}
```

**Go 对比：**

```go
package main

func sum(xs []int) int {
	n := 0
	for _, v := range xs {
		n += v
	}
	return n
}

func main() {
	_ = sum([]int{1, 2, 3})
}
```

- **Go 怎么做**：切片/指针共享很廉价，GC 托底，较少“先证明唯一所有者”。
- **Rust 为什么不同**：默认所有权更简单可证明；共享是显式升级。
- **Go 程序员易踩的坑**：把每个“多处能看见”都翻译成 `Rc`，其实借用或 move 就够。

**记忆点：**
- 先问“能不能唯一拥有或只借一会儿”。
- `Rc`/`Arc` 是共享所有权工具，不是默认指针。

## Q20. `Box::leak`、`into_raw` / `from_raw` 有哪些坑？ {#q20}
**Tags:** `common` `Box` `leak` `raw-pointer`
**适用版本:** Rust 1.0+

**一句话答案：** `Box::leak` 故意永不回收；`into_raw` 交出所有权后必须且只能用 `from_raw` 接回一次——重复释放、忘记接回、或接回后继续用旧裸指针，都会变成内存错误。

**解答：** `Box::leak` 适合真正要 `'static` 且接受泄漏的场景（插件表、进程级缓存）；日常业务数据别用它“逃生命周期”。`into_raw` 把 `Box` 变成 `*mut T` 后，Rust 不再自动 `drop`；你要自己保证：要么 `from_raw` 重建 `Box` 再释放，要么交给明确约定的 C/FFI 释放方。切勿对同一地址 `from_raw` 两次，也别在 `from_raw` 之后继续解引用旧指针。

```rust
fn main() {
    let leaked: &'static mut i32 = Box::leak(Box::new(7));
    *leaked += 1;
    assert_eq!(*leaked, 8);
}
```

```rust
fn main() {
    let boxed = Box::new(String::from("raw"));
    let ptr = Box::into_raw(boxed);
    unsafe {
        let rebuilt = Box::from_raw(ptr);
        assert_eq!(*rebuilt, "raw");
    }
}
```

**Go 对比：**

```go
package main

func main() {
	// Go 很少手写“泄漏换 static”或成对 into_raw/from_raw；
	// 堆对象默认交给 GC。
}
```

- **Go 怎么做**：GC 管回收；逃逸分析可能把局部放到堆上。
- **Rust 为什么不同**：`Box` 的释放责任明确；泄漏与裸指针交接必须显式。
- **Go 程序员易踩的坑**：用 `leak` 假装解决了生命周期；或把 `into_raw` 当“随便拿个指针”却忘了配对释放。

**记忆点：**
- `leak` = 故意不释放；先确认真要 `'static`。
- `into_raw` / `from_raw` 必须一对一，禁止双释放。
