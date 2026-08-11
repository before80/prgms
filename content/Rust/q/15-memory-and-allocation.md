+++
title = "15-内存与分配"
date = 2026-07-28T14:49:00+08:00
weight = 150
type = "docs"
description = "用 Go 对比讲清栈堆、分配、容量、Box 与泄漏"
isCJKLanguage = true
draft = false

+++

# 内存与分配 (Memory and Allocation)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你是否把 Rust 当成「没有 GC 的 Go」，结果分不清栈、堆、谁负责释放？
- 你会不会拿着 `Vec` / `String` 元素的引用再 `push`，撞上 `error[E0502]`？
- 你是否分不清 `len` / `capacity`、`Box`、`move`、循环引用泄漏各自在防什么？
- 你是否需要一套「数据放哪、谁拥有、会不会搬家、何时释放」的日常判断流程？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| stack | — | 栈 | 函数帧里放局部变量的快速内存，随返回自动回收 | goroutine 栈（可增长） |
| heap | — | 堆 | 运行时按需申请的动态内存，必须有人负责释放 | 堆对象 + GC |
| **GC** | Garbage Collector | 垃圾回收器 | 运行时扫描并回收不再使用的对象 | Go 默认机制 |
| **RAII** | Resource Acquisition Is Initialization | 资源获取即初始化 | 资源跟着值的生命周期自动获取/释放 | 常靠 `defer` 手写模拟 |
| ownership | — | 所有权 | 每个值同一时刻只有一个负责人 | 无（Go 靠 GC） |
| move | — | 移动 | 转移所有权，通常只搬栈上元数据 | 赋值后两边都能用，不等价 |
| `Drop` | — | 析构 | 离开作用域时自动跑的清理逻辑 | `defer` 的自动版 |
| `Box<T>` | — | 堆上独占指针 | 把 `T` 放到堆上，栈上只留指针 | `new(T)` + 单一所有者，近似 |
| capacity | — | 容量 | 缓冲区已分配、可容纳的元素上限 | `cap(slice)` |
| niche | — | 空位 / 非法位型 | 类型合法值用不到的位模式 | 无直接对应 |
| niche optimization | — | 空位优化 | 用 niche 表示 `None` 等，省掉额外判别字节 | 无 |
| **ABI** | Application Binary Interface | 应用二进制接口 | 类型布局、调用约定等二进制约定 | Go 与 C 互操作也有 ABI 问题 |
| **FFI** | Foreign Function Interface | 外部函数接口 | 与 C 等其他语言互通 | `cgo` |
| `repr(C)` | — | C 兼容布局 | 按 C 兼容方式排布字段 | `struct` 的 C 布局约定 |
| `Rc` / `Weak` | Reference Counted | 引用计数 / 弱引用 | 共享所有权；`Weak` 不增加强计数、可破环 | 多指针 + GC（环通常能收） |
| OOM | Out Of Memory | 内存耗尽 | 分配器拿不到足够内存 | Go 也可能 OOM，常直接崩 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5) |
| `common` | [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q17](#q17), [Q19](#q19) |
| `occasional` | [Q12](#q12), [Q13](#q13), [Q14](#q14) |
| `advanced` | [Q15](#q15), [Q16](#q16), [Q18](#q18) |

---

## Q1. 栈和堆在 Rust 里该怎么理解？ {#q1}
**Tags:** `hot` `beginner` `stack` `heap`
**适用版本:** Rust 1.0+（1.97.1 行为一致）

**一句话答案：**

**栈**（stack）放函数帧里大小已知的局部数据，返回即回收；**堆**（heap）按需申请、动态长大，必须由所有者在离开作用域时通过 **RAII**（Resource Acquisition Is Initialization，资源获取即初始化）释放——Rust 没有默认的 **GC**（Garbage Collector，垃圾回收器）。

**解答：**

先建立画面，再谈所有权。栈像一叠盘子：调用函数压一层，返回弹一层，速度极快，但每层大小最好在编译期就清楚。堆像仓库：你向分配器要一块地，地址可能任意远，用完必须有人归还。

小整数、函数参数、返回值、多数 `Copy` 小值通常落在栈上：

```rust
fn add(a: i32, b: i32) -> i32 {
    let sum = a + b; // sum 在当前栈帧
    sum
}

fn main() {
    let x = 10;
    let y = add(x, 32);
    println!("{y}");
}
```

需要可变长度或「活得比当前帧更久」的数据时，真正的字节往往在堆上；栈上只留指针、长度等元数据：

```rust
fn main() {
    let on_stack = 42; // 通常在栈
    let on_heap = String::from("hello"); // 元数据在栈，"hello" 字节在堆
    println!("{on_stack} {on_heap}");
} // on_heap 离开作用域 → Drop → 归还堆缓冲
```

Rust **不保证**每个绑定的绝对物理位置（优化可能改变），但所有权规则保证：堆资源一定有明确的释放路径。大对象不想撑栈时，可显式放堆：

```rust
fn main() {
    // 1MB 数组若直接放局部变量，容易撑爆默认栈
    let big = Box::new([0u8; 1024 * 1024]);
    println!("len={}", big.len());
} // Box drop 时释放堆上数组
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	x := 42          // 可能在栈；逃逸分析也可能把它弄到堆
	s := "hello"     // string 头很小；底层字节由运行时管理
	b := make([]byte, 1024*1024)
	fmt.Println(x, s, len(b))
	// 何时回收：GC 决定，程序员通常不点名「谁 drop」
}
```

- **Go 怎么做**：逃逸分析 + GC；你较少精确关心「这一帧结束是否立刻释放」。
- **Rust 为什么不同**：用所有权 / **RAII** 在编译期钉死释放责任，换取可预测的资源回收与无 GC 停顿。
- **Go 程序员易踩的坑**：以为「没有 GC = 要自己 free」；其实是「编译器按作用域帮你 drop」，不是手写 `free`。

**记忆点：**

- 栈：快、帧绑定、大小宜已知；堆：动态、要所有者。
- 释放靠 **RAII** / `Drop`，不是靠 GC 扫描。
- 位置可优化，责任不能糊。

---

## Q2. `String` / `Vec` 的数据到底放哪？ {#q2}
**Tags:** `hot` `beginner` `string` `vec` `heap`
**适用版本:** Rust 1.0+

**一句话答案：**

`String` / `Vec<T>` 在栈上只存「指针 + 长度 + 容量」三元组；真正的字节 / 元素缓冲在堆上。赋值默认 **move** 的是这份栈上元数据，不是整块堆拷贝（见 [11-ownership](../11-ownership/#q2)）。

**解答：**

把 `String` 想成「带头的缓冲区」：

| 放在哪 | 存什么 |
|--------|--------|
| 栈 | `ptr`、`len`、`capacity`（三字头） |
| 堆 | 实际 UTF-8 字节 |

`Vec<T>` 同理，只是堆上是 `T` 元素序列。

```rust
fn main() {
    let s = String::from("hi");
    // 栈上：ptr → 堆上 b'h','i'；len=2；capacity ≥ 2
    println!("len={} cap={}", s.len(), s.capacity());
    assert_eq!(std::mem::size_of_val(&s), 24); // 64 位上常见：3 × usize
}
```

`Vec` 也是同一张图：

```rust
fn main() {
    let mut v = Vec::new();
    v.push(10);
    v.push(20);
    // 栈：三字头；堆：[10, 20, ...]
    println!("len={} cap={} data={:?}", v.len(), v.capacity(), v);
}
```

move 只搬三字头，堆缓冲仍在原地，只是责任卡换人：

```rust
fn main() {
    let s1 = String::from("hello");
    let ptr_before = s1.as_ptr();
    let s2 = s1; // move：搬三字头，不拷贝 "hello"
    assert_eq!(s2.as_ptr(), ptr_before); // 同一块堆
    println!("{s2}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hello" // string：ptr+len；底层只读数据由运行时管
	v := []int{10, 20} // slice：ptr+len+cap；数组可能在堆
	fmt.Println(len(s), len(v), cap(v))
}
```

- **Go 怎么做**：`string` / slice 头也是小结构；底层数组何时回收靠 GC。
- **Rust 为什么不同**：头的所有者同时负责 `Drop` 归还堆缓冲；双所有者会 double-free，所以默认 move。
- **Go 程序员易踩的坑**：把 `let t = s;` 当成 Go 那样「两边都能用」——对 `String`/`Vec` 会吃掉左边。

**记忆点：**

- 栈三字头 + 堆缓冲。
- move 搬头，不搬整堆（除非你 `.clone()`）。
- 谁持有头，谁负责释放。

---

## Q3. `len` 和 `capacity` 为什么要分开？ {#q3}
**Tags:** `hot` `beginner` `vec` `capacity`
**适用版本:** Rust 1.0+

**一句话答案：**

`len` 是已初始化、对外可见的元素个数；`capacity` 是堆缓冲当前已分配、还能装多少的上限——分开才能「先多分配、后少次扩容」。

**解答：**

若缓冲永远刚好等于 `len`，每次 `push` 都可能重新分配并搬家，成本很高。所以 `Vec` / `String` 常预留空位：`len ≤ capacity`。

```rust
fn main() {
    let mut v = Vec::with_capacity(8);
    assert_eq!(v.len(), 0);
    assert!(v.capacity() >= 8);
    v.push(1);
    v.push(2);
    assert_eq!(v.len(), 2);
    assert!(v.capacity() >= 8); // 空位还在，push 通常不必再分配
    println!("len={} cap={}", v.len(), v.capacity());
}
```

`String` 同样有 `len`（字节数）与 `capacity`：

```rust
fn main() {
    let mut s = String::with_capacity(16);
    s.push_str("hi");
    assert_eq!(s.len(), 2);
    assert!(s.capacity() >= 16);
    println!("len={} cap={}", s.len(), s.capacity());
}
```

超容量时会扩容：申请更大缓冲、把旧元素 **move** 到新地址、释放旧块。这正是「持有元素引用时不能再 `push`」的物理原因（见 [Q5](#q5)）：

```rust
fn main() {
    let mut v = vec![1, 2];
    let cap0 = v.capacity();
    while v.len() <= cap0 {
        v.push(0); // 最终会触发至少一次扩容
    }
    assert!(v.capacity() > cap0);
    println!("grew: {} -> {}", cap0, v.capacity());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := make([]int, 0, 8) // len=0, cap=8
	v = append(v, 1, 2)
	fmt.Println(len(v), cap(v))
}
```

- **Go 怎么做**：`len` / `cap` 同一套直觉；`append` 可能返回新底层数组。
- **Rust 为什么不同**：语义几乎平行；差别在于 Rust 用借用规则在编译期挡住「旧引用指向已释放缓冲」。
- **Go 程序员易踩的坑**：在 Go 里忽略 `append` 返回值会踩坑；在 Rust 里则是持引用再 `push` 直接编译失败。

**记忆点：**

- `len` = 有几个；`capacity` = 还能装到哪。
- 预留 capacity = 少分配、少搬家。
- 扩容 = 新地址 → 旧引用作废。

---

## Q4. `Box<T>` 什么时候值得用？ {#q4}
**Tags:** `hot` `beginner` `box`
**适用版本:** Rust 1.0+

**一句话答案：**

当你需要「堆上独占一份 `T`、栈上只留指针」时用 `Box<T>`：递归类型、大对象避栈、`dyn Trait` 拥有型对象、只想 move 一个指针时。

**解答：**

`Box::new(value)` 把 `value` 放到堆上，返回拥有该堆块的智能指针。离开作用域时 `Drop` 先析构 `T`，再归还分配。

```rust
fn main() {
    let b = Box::new(5);
    assert_eq!(*b, 5);
    println!("{b}");
} // 释放堆上的 i32
```

递归类型没有 `Box`（或其它间接层）时，大小无法算完：

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

fn main() {
    let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Nil))));
    match list {
        List::Cons(n, _) => println!("head={n}"),
        List::Nil => {}
    }
}
```

大对象、trait 对象、只搬指针的转移，也是高频场景：

```rust
fn take(b: Box<[u8; 1024]>) {
    println!("got {} bytes on heap", b.len());
}

fn main() {
    let big = Box::new([0u8; 1024]);
    take(big); // move 的是指针大小，不是 1024 字节再拷一遍
    let err: Box<dyn std::error::Error> = "boom".into();
    println!("{err}");
}
```

**Go 对比：**

```go
package main

import "fmt"

type node struct {
	val  int
	next *node // 间接层，类似 Box 打破「无限大」
}

func main() {
	n := &node{val: 1, next: &node{val: 2}}
	fmt.Println(n.val, n.next.val)
	// 回收：GC；没有单一 Drop 所有者
}
```

- **Go 怎么做**：`new` / `&T` 把对象放到堆（或由逃逸分析决定）；GC 回收。
- **Rust 为什么不同**：`Box` 明确「独占 + 自动释放」；共享要用 `Rc`/`Arc`。
- **Go 程序员易踩的坑**：把所有堆指针都当成可随便共享——在 Rust 里 `Box` 是独占的。

**记忆点：**

- 递归、大对象、`dyn Trait`、轻量 move → 想 `Box`。
- `Box` = 堆上独占 + RAII 释放。
- 要共享，换 `Rc`/`Arc`（见 [Q9](#q9)）。

---

## Q5. 扩容为什么会让旧引用失效？ {#q5}
**Tags:** `hot` `intermediate` `vec` `borrowing`
**适用版本:** Rust 1.0+

**一句话答案：**

`push` / `reserve` 等可能触发重分配：元素搬到新堆块，旧地址释放——若仍握着指向旧缓冲的引用，就会悬垂；借用检查器用 `error[E0502]` 在编译期拦住（见 [12-references-and-borrowing](../12-references-and-borrowing/#q1)）。

**解答：**

物理过程：

1. 容量不够 → 申请更大缓冲  
2. 把旧元素 move 到新地址  
3. 释放旧缓冲  
4. 更新三字头里的 `ptr` / `capacity`

因此「先借元素，再可能扩容」是非法的：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let first = &v[0];
    v.push(4);
    // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    println!("{first}");
}
```

`String` 同样：

```rust
fn main() {
    let mut s = String::from("hi");
    let r = &s[0..1];
    s.push_str("!!!!"); // 可能重分配
    // error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
    println!("{r}");
}
```

安全写法：先结束借用（或先拷贝出需要的值），再改容器；需要边读边攒结果时，先 `collect` 再 `extend`：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let first = v[0]; // Copy：不持有对缓冲的引用
    v.push(first * 10);
    assert_eq!(v, [1, 2, 3, 10]);

    let extra: Vec<i32> = v.iter().map(|x| x * 2).collect();
    v.extend(extra);
    println!("{v:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	p := &v[0]
	v = append(v, 4) // 可能换底层数组；p 可能悬空——Go 编译器不管
	fmt.Println(v, *p) // 可能碰巧对，也可能读到垃圾
}
```

- **Go 怎么做**：`append` 可能换数组；持旧指针是程序员责任，语言层不挡。
- **Rust 为什么不同**：扩容与可变借用绑定，编译期消灭悬垂引用。
- **Go 程序员易踩的坑**：习惯「先取下标指针再 append」——在 Rust 里应先取值 / 先算完再改。

**记忆点：**

- 扩容 = 搬家 = 旧引用作废。
- 持引用期间禁止可能重分配的操作 → `E0502`。
- 先读完 / 先拷贝 / 先 `collect`，再 `push`。

---

## Q6. `Vec::with_capacity` 为什么能减少分配？ {#q6}
**Tags:** `common` `beginner` `vec` `performance`
**适用版本:** Rust 1.0+

**一句话答案：**

已知最终大概要多少元素时，先 `with_capacity` / `reserve` 一次分配到位，后续 `push` 多半只写内存、不再向分配器要新块，也就少了搬家。

**解答：**

对比「从空 `Vec` 一路 push」：每次容量满都会分配 + move。预分配则把成本摊成一次（或少数次）：

```rust
fn main() {
    let n = 1000;
    let mut v = Vec::with_capacity(n);
    for i in 0..n {
        v.push(i); // 在 capacity 内：通常无新分配
    }
    assert_eq!(v.len(), n);
    assert!(v.capacity() >= n);
    println!("cap={}", v.capacity());
}
```

`reserve` 是在已有 `Vec` 上「至少再保证能再 push 这么多」：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    v.reserve(100);
    let cap = v.capacity();
    for i in 0..100 {
        v.push(i);
    }
    assert_eq!(v.capacity(), cap); // 这 100 次 push 不应再扩容
    println!("len={} cap={}", v.len(), v.capacity());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := make([]int, 0, 1000) // 等价思路：先定 cap
	for i := 0; i < 1000; i++ {
		v = append(v, i)
	}
	fmt.Println(len(v), cap(v))
}
```

- **Go 怎么做**：`make([]T, 0, n)` 预留 cap，同款优化。
- **Rust 为什么不同**：API 名不同（`with_capacity`），动机完全一样。
- **Go 程序员易踩的坑**：两边都容易「懒得预分配」；热路径上日志级分配次数差很多。

**记忆点：**

- 知道长度 → `with_capacity` / `make(..., 0, n)`。
- 少分配 = 少搬家 = 少打满分配器。
- 不确定上界就用 `reserve` 按批次加。

---

## Q7. `Drop` 跟释放内存是什么关系？ {#q7}
**Tags:** `common` `intermediate` `drop` `raii`
**适用版本:** Rust 1.0+

**一句话答案：**

离开作用域时，编译器插入 **drop glue**：先跑你的 `Drop::drop`（若有），再按规则析构字段；对 `Box`/`Vec`/`String` 来说，这一步最终会把堆缓冲归还给分配器——这就是 **RAII** 的释放半边。

**解答：**

`Drop` 是「值要没了」时的钩子；堆内存释放通常发生在标准库类型的 `Drop` 实现里，而不是你手写 `free`。

```rust
struct Loud(&'static str);

impl Drop for Loud {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let _a = Loud("a");
    let _b = Loud("b");
} // 先 b 后 a（局部变量与声明相反顺序）
```

`String` 离开作用域时：先 drop 自身（释放堆上 UTF-8 缓冲），无需你干预：

```rust
fn main() {
    {
        let s = String::from("temp");
        println!("{s}");
    } // 此处释放 s 的堆缓冲
    println!("after");
}
```

结构体若实现了 `Drop`，会先执行 `Drop::drop`（字段此时仍完整），再按**声明顺序** drop 各字段：

```rust
struct Loud(&'static str);
impl Drop for Loud {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

struct Wrap {
    first: Loud,
    second: Loud,
}
impl Drop for Wrap {
    fn drop(&mut self) {
        println!("Wrap::drop");
    }
}

fn main() {
    let _w = Wrap {
        first: Loud("first"),
        second: Loud("second"),
    };
} // Wrap::drop → first → second
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "temp"
	fmt.Println(s)
	// 无 Drop；不可达后等 GC
	// 若持有文件等资源，通常要 defer f.Close()
}
```

- **Go 怎么做**：内存靠 GC；文件/锁等常靠 `defer`。
- **Rust 为什么不同**：内存与其它资源同一套作用域析构，减少「忘了 Close」。
- **Go 程序员易踩的坑**：在 `Drop` 里 panic、或假设别的全局状态还活着——析构顺序敏感。

**记忆点：**

- 作用域结束 → drop glue → 可能归还堆。
- 局部变量：反声明序；字段：声明序（自定义 `Drop` 先跑）。
- 想提前释放：`drop(value)`，不要手调 `Drop::drop`。

---

## Q8. 为什么说 move 不等于拷贝整块堆内存？ {#q8}
**Tags:** `common` `beginner` `move` `ownership`
**适用版本:** Rust 1.0+

**一句话答案：**

对 `String`/`Vec`/`Box` 等，move 只把栈上的指针头（或 `Box` 指针）按位搬到新绑定，并让旧绑定失效；堆上那一大块数据通常原地不动（见 [11-ownership](../11-ownership/#q2)）。

**解答：**

若每次赋值都深拷贝堆，代价会像 Go 里无脑 `append` 复制那样爆炸。Rust 默认选择转移所有权：

```rust
fn main() {
    let s = String::from("hello-world-........");
    let p1 = s.as_ptr();
    let t = s; // move 三字头
    let p2 = t.as_ptr();
    assert_eq!(p1, p2); // 堆缓冲未因 move 而复制
    println!("{t}");
}
```

`Box` 更直观：move 的是指针宽度：

```rust
fn main() {
    let b = Box::new([1u8; 4096]);
    let p1 = b.as_ptr();
    let b2 = b; // 只搬指针
    assert_eq!(p1, b2.as_ptr());
    println!("{}", b2.len());
}
```

真要两份独立堆数据，必须显式 `clone`（或自己分配再拷）：

```rust
fn main() {
    let s = String::from("hello");
    let t = s.clone(); // 新分配 + 拷贝字节
    assert_ne!(s.as_ptr(), t.as_ptr());
    println!("{s} {t}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := []byte("hello")
	b := a // 复制 slice 头；底层数组仍共享
	b[0] = 'H'
	fmt.Println(string(a), string(b)) // 两边都变
}
```

- **Go 怎么做**：赋值复制头；底层是否共享取决于类型；回收靠 GC。
- **Rust 为什么不同**：非 `Copy` 类型赋值后旧绑定失效，避免两头都去 `Drop` 同一块堆。
- **Go 程序员易踩的坑**：把 move 想成「很贵的深拷贝」——通常很便宜；贵的是 `.clone()`。

**记忆点：**

- move ≈ 搬指针头 + 作废旧名。
- 深拷贝要 `clone`（或等价 API）。
- `Copy` 类型才是「赋值后两边都能用」的按位复制。

---

## Q9. 循环引用为什么会泄漏？ {#q9}
**Tags:** `common` `intermediate` `rc` `leak`
**适用版本:** Rust 1.0+

**一句话答案：**

`Rc` 靠强引用计数归零才释放；两个节点互相 `Rc` 持有时，计数永远到不了 0，堆块安全但永不回收。用 `Weak`（弱引用，不增加强计数）打破环。

**解答：**

下面这段**可以编译运行**：`a`↔`b` 互相强引用，局部变量结束后计数仍 ≥ 1，形成泄漏（演示用，不要当正常设计）：

```rust
use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    next: RefCell<Option<Rc<Node>>>,
}

fn main() {
    let a = Rc::new(Node {
        next: RefCell::new(None),
    });
    let b = Rc::new(Node {
        next: RefCell::new(None),
    });
    *a.next.borrow_mut() = Some(Rc::clone(&b));
    *b.next.borrow_mut() = Some(Rc::clone(&a)); // 环
    assert_eq!(Rc::strong_count(&a), 2);
    assert_eq!(Rc::strong_count(&b), 2);
} // a、b 局部 drop 后，彼此仍各持有对方 → 永不释放
```

修法：反向边改成 `Weak`，需要时 `upgrade()`：

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    next: RefCell<Option<Rc<Node>>>,
    prev: RefCell<Weak<Node>>,
}

fn main() {
    let a = Rc::new(Node {
        next: RefCell::new(None),
        prev: RefCell::new(Weak::new()),
    });
    let b = Rc::new(Node {
        next: RefCell::new(None),
        prev: RefCell::new(Weak::new()),
    });
    *a.next.borrow_mut() = Some(Rc::clone(&b));
    *b.prev.borrow_mut() = Rc::downgrade(&a); // 弱引用，不增加 a 的强计数
    assert_eq!(Rc::strong_count(&a), 1);
    assert_eq!(Rc::strong_count(&b), 2); // 仅 a.next 多持一份
    assert!(b.prev.borrow().upgrade().is_some());
} // a drop → b 强计数降为 1 → 再随局部结束归零，无环泄漏
```

**Go 对比：**

```go
package main

type node struct {
	next *node
}

func main() {
	a, b := &node{}, &node{}
	a.next, b.next = b, a // 环
	_ = a
	// tracing GC 仍可回收互指但不可达的对象
}
```

- **Go 怎么做**：tracing GC 能处理环，只要对象整体不可达。
- **Rust 为什么不同**：`Rc` 不是 tracing GC，只看强计数；环 = 逻辑泄漏。
- **Go 程序员易踩的坑**：以为「Rust 也有 GC 所以环没事」——`Rc` 环会漏。

**记忆点：**

- 强引用环 → 计数不归零 → 泄漏。
- 树/图的反向边优先 `Weak`。
- 这是安全的泄漏，不是 UB。

---

## Q10. 什么是故意泄漏，比如 `Box::leak`？ {#q10}
**Tags:** `common` `intermediate` `leak`
**适用版本:** Rust 1.0+

**一句话答案：**

故意泄漏是主动放弃 `Drop` 释放路径，让内存活到进程结束（或交给别处管）；`Box::leak` 把 `Box<T>` 变成 `&'static mut T`，常见于全局表、插件、测试夹具。

**解答：**

```rust
fn main() {
    let b = Box::new(String::from("forever"));
    let leaked: &'static mut String = Box::leak(b);
    leaked.push_str("!");
    println!("{leaked}");
    // 无对应的 Box 再 drop：这块堆不会因作用域结束而释放
}
```

`mem::forget` 也会跳过 `Drop`（不交出 `'static` 引用，只是「忘记析构」）：

```rust
fn main() {
    let s = String::from("skip-drop");
    std::mem::forget(s); // 不运行 String 的 Drop → 堆缓冲泄漏
    println!("forgotten");
}
```

适用面很窄：真正需要进程级存活、或与手动/外部释放协议对接时。日常业务逻辑优先正常所有权，而不是泄漏。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "forever"
	fmt.Println(s)
	// 没有 Box::leak 这种「交出 'static 并放弃释放」的常用 API
	// 全局变量 / sync.Once 初始化更常见
}
```

- **Go 怎么做**：包级变量、`sync.Once`、进程级缓存；GC 仍可能扫到它们。
- **Rust 为什么不同**：`'static` 引用要求数据永不失效；`leak` 是显式换取静态生命周期的手段之一。
- **Go 程序员易踩的坑**：用 `leak` 逃避借用检查——能编译，但会真漏内存。

**记忆点：**

- `Box::leak` / `forget` = 故意不 Drop。
- 换来的是 `'static` 或「跳过析构」，不是免费午餐。
- 默认仍应让 RAII 收尾。

---

## Q11. 什么时候该担心栈太大？ {#q11}
**Tags:** `common` `beginner` `stack` `overflow`
**适用版本:** Rust 1.0+

**一句话答案：**

巨型局部数组、极深递归、或在默认栈很小的线程里塞大帧时，要担心栈溢出；大块数据优先 `Vec`/`Box` 放堆，深递归优先改迭代或加大**你自己创建的**线程栈。

**解答：**

栈溢出通常直接 abort / 崩溃，和堆 OOM 不是同一条路径。把大缓冲放到堆上是最常见修法：

```rust
fn main() {
    // let big = [0u8; 10_000_000]; // 约 10MB 局部数组：容易撑爆默认栈
    let big = vec![0u8; 10_000_000]; // 堆上
    println!("{}", big.len());
}
```

`Box` 同样把大数组挪出栈帧：

```rust
fn main() {
    let big = Box::new([0u8; 1_000_000]);
    println!("first={} len={}", big[0], big.len());
}
```

只有你用 `std::thread::Builder` 创建的线程才能直接指定栈大小（不是 Tokio runtime 的通用旋钮）：

```rust
use std::thread;

fn main() {
    let h = thread::Builder::new()
        .stack_size(8 * 1024 * 1024)
        .spawn(|| {
            let local = [0u8; 64];
            local.len()
        })
        .unwrap();
    println!("{}", h.join().unwrap());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	big := make([]byte, 10_000_000) // 通常在堆
	fmt.Println(len(big))
	// goroutine 栈可分段增长，但仍可能因极深递归出问题
}
```

- **Go 怎么做**：goroutine 栈可增长；大切片多在堆。
- **Rust 为什么不同**：默认线程栈固定量级，大数组局部变量更危险。
- **Go 程序员易踩的坑**：把 Go 里「随便 `var buf [1e7]byte`」的习惯搬到 Rust 主线程。

**记忆点：**

- 大块 → `Vec` / `Box`，别塞栈。
- 深递归 → 迭代，或自建线程并加大栈。
- 栈溢出 ≠ 堆 OOM。

---

## Q12. `repr(C)` 跟内存布局有什么关系？ {#q12}
**Tags:** `occasional` `intermediate` `repr` `ffi` `abi`
**适用版本:** Rust 1.0+；布局规则稳定

**一句话答案：**

默认 `repr(Rust)` 允许编译器重排字段；写 **`#[repr(C)]`**（就写在结构体定义上方的源码属性）要求按 C 兼容布局排布，以便 **FFI**（Foreign Function Interface，外部函数接口）与 **ABI**（Application Binary Interface，应用二进制接口）稳定对齐。

**解答：**

下面这份 Rust 源码里，`#[repr(C)]` **直接写在 `struct` 上**——不是运行时开关，而是类型布局契约：

```rust
#[repr(C)]
struct Pod {
    a: u8,
    b: u32,
}

fn main() {
    assert_eq!(std::mem::size_of::<Pod>(), 8); // 典型：1 + 3 padding + 4
    assert_eq!(std::mem::align_of::<Pod>(), 4);
    let p = Pod { a: 1, b: 2 };
    println!("a={} b={}", p.a, p.b);
}
```

没有 `repr(C)` 时，字段顺序与填充**不保证**与 C 一致，不能安全按 C 结构体解读：

```rust
struct Rusty {
    a: u8,
    b: u32,
}

#[repr(C)]
struct Compatible {
    a: u8,
    b: u32,
}

fn main() {
    println!(
        "Rusty={} Compatible={}",
        std::mem::size_of::<Rusty>(),
        std::mem::size_of::<Compatible>()
    );
    // 跨 C 边界传结构体时，用 Compatible 这种写法，而不是默认 Rusty
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"unsafe"
)

// 与 C 互通时同样要自己保证字段顺序与对齐；Go 没有 #[repr(C)] 这种一键契约
type Pod struct {
	A uint8
	_ [3]byte // 手工 padding，示意对齐问题
	B uint32
}

func main() {
	var p Pod
	fmt.Println(unsafe.Sizeof(p), unsafe.Alignof(p))
}
```

- **Go 怎么做**：`cgo` / 手工 padding / `encoding/binary`；字段对齐要自己盯。
- **Rust 为什么不同**：默认布局为语言优化服务；与 C 互通必须显式 `#[repr(C)]`。
- **Go 程序员易踩的坑**：以为「字段声明顺序 = 内存顺序」在默认 Rust struct 上永远成立。

**记忆点：**

- `#[repr(C)]` 写在源码的 `struct`/`enum` 上。
- FFI / 稳定 ABI → 要 `repr(C)`（或更具体的 `repr(transparent)` 等）。
- 默认 `repr(Rust)` 可重排，别拿去对 C 头文件。

---

## Q13. 为什么 `Option<&T>` 经常不额外占空间？ {#q13}
**Tags:** `occasional` `intermediate` `niche` `option`
**适用版本:** 长期存在；1.97.1 一致

**一句话答案：**

引用不能为空，全零位型是非法的——这是一个 **niche**（空位 / 非法位型）。**niche optimization**（空位优化）用该位型表示 `None`，于是 `Option<&T>` 常与 `&T` 同宽。

**解答：**

```rust
use std::mem::size_of;

fn main() {
    assert_eq!(size_of::<Option<&i32>>(), size_of::<&i32>());
    assert_eq!(size_of::<Option<Box<i32>>>(), size_of::<Box<i32>>());
    println!("Option<&i32> = {} bytes", size_of::<Option<&i32>>());
}
```

对比：普通 `u32` 没有可用 niche，`Option<u32>` 通常更宽；`NonZeroU32` 则把 0 留给 `None`：

```rust
use std::mem::{size_of, size_of_val};
use std::num::NonZeroU32;

fn main() {
    assert_eq!(size_of::<Option<NonZeroU32>>(), size_of::<u32>());
    assert!(size_of::<Option<u32>>() > size_of::<u32>());
    let n = NonZeroU32::new(7).unwrap();
    let opt = Some(n);
    println!("{:?} width={}", opt, size_of_val(&opt));
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var p *int
	fmt.Println(p == nil) // 指针本身可 nil；没有 Option 与 niche 这套类型编码
}
```

- **Go 怎么做**：`*T` 用 `nil` 表示空；没有与 `Option` 同构的零成本枚举编码保证。
- **Rust 为什么不同**：`Option` 是类型；对有 niche 的 `T` 可压缩判别。
- **Go 程序员易踩的坑**：以为所有 `Option<T>` 都比 `T` 多一个字——对 `&T`/`Box`/`NonZero*` 常常不是。

**记忆点：**

- 非法位型 = niche；可拿来编码 `None`。
- `Option<&T>` / `Option<Box<T>>` 常零额外空间。
- 不要依赖未 `repr` 保证的自定义布局细节。

---

## Q14. 分配失败时稳定版 Rust 一般怎么处理？ {#q14}
**Tags:** `occasional` `intermediate` `oom` `alloc`
**适用版本:** 默认 OOM abort；`Vec::try_reserve` 等 fallible API 在 1.97.1 stable 可用

**一句话答案：**

稳定版默认路径下，`Vec::push` / `Box::new` 等分配失败通常 **abort**（或走 `alloc_error_hook`）——进程直接终止；需要可恢复时用已稳定的 fallible API，例如 `Vec::try_reserve`。

**解答：**

日常代码把「内存够用」当前提：失败即终止，避免在半初始化状态继续跑。若你要在容量预留失败时自行降级（换算法、回传错误），用 `try_reserve`：

```rust
fn main() {
    let mut v: Vec<u8> = Vec::new();
    match v.try_reserve(1_000) {
        Ok(()) => {
            v.push(1);
            println!("reserved cap={}", v.capacity());
        }
        Err(e) => {
            eprintln!("try_reserve failed: {e}");
        }
    }
}
```

`try_reserve_exact` 同属稳定 fallible 预留；多数 `Box::try_new` 一类仍依赖 nightly `allocator_api`，**1.97.1 stable 不要当成已稳定全家桶**：

```rust
fn main() {
    let mut v: Vec<i32> = Vec::new();
    v.try_reserve_exact(32).expect("reserve");
    for i in 0..32 {
        v.push(i);
    }
    assert!(v.capacity() >= 32);
    println!("ok len={}", v.len());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := make([]byte, 0, 1000)
	fmt.Println(cap(v))
	// 极端 OOM 时进程也可能直接挂；少见「分配失败当普通 error 层层返回」
}
```

- **Go 怎么做**：多数分配失败同样致命；语言没有全面的 fallible alloc 习惯。
- **Rust 为什么不同**：默认也是 abort；但标准库提供部分 `try_*` 预留 API 给需要降级的场景。
- **Go 程序员易踩的坑**：以为 Rust 的 `Result` 文化意味着每次 `push` 都返回 `Result`——默认不是。

**记忆点：**

- 默认：分配失败 → abort / OOM 钩子。
- 可恢复预留：`try_reserve` / `try_reserve_exact`（stable）。
- 别把 nightly 的 `allocator_api` 全家桶写成 stable。

---

## Q15. Go 的 GC 直觉和 Rust 的 RAII 心智差在哪？ {#q15}
**Tags:** `advanced` `beginner` `gc` `raii`
**适用版本:** 概念贯穿各版本

**一句话答案：**

Go 靠 **GC** 在运行时找「谁还被引用」并回收；Rust 靠 **RAII** / 所有权在编译期确定「谁离开作用域就释放」——你换的是心智模型：从「可达性分析」转到「所有者与借用」。

**解答：**

同一份堆数据，两条时间线：

```rust
fn main() {
    let s = String::from("raii");
    println!("{s}");
} // 作用域结束立刻 drop，归还缓冲——不等待 GC 周期
```

借用让你在不转移所有权的情况下使用数据；借用一结束，所有者仍可释放（规则见 [12-references-and-borrowing](../12-references-and-borrowing/#q1)）：

```rust
fn print_len(s: &String) {
    println!("{}", s.len());
}

fn main() {
    let s = String::from("borrow");
    print_len(&s);
    println!("{s}"); // 仍由 s 拥有；函数返回后在此作用域末尾释放
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "gc"
	fmt.Println(s)
	// 不可达后，某个 GC 周期才可能回收；时刻不可精确预期
}
```

- **Go 怎么做**：写完逻辑即可；生命周期由 GC 兜底；代价是停顿与更少的确定性。
- **Rust 为什么不同**：确定性释放、无 GC 扫描；代价是 move / 借用规则要学。
- **Go 程序员易踩的坑**：用「反正 GC 会收」逃避结构设计——在 Rust 里环、泄漏、扩容失效都要正面处理。

**记忆点：**

- GC：运行时找垃圾；RAII：作用域到了就扔。
- Rust：谁拥有，谁释放；谁借用，谁不能让所有者提前消失。
- 性能与确定性换来的是编译期纪律。

---

## Q16. 本章最重要的内存判断题是什么？ {#q16}
**Tags:** `advanced` `beginner` `checklist`
**适用版本:** Rust 1.0+

**一句话答案：**

每次动手前先问四句：**数据放栈还是堆？谁拥有？会不会因扩容搬家？何时 Drop？**——答得清，绝大多数内存坑都能提前避开。

**解答：**

把判断题落到代码动作上：

```rust
fn main() {
    // 1) 放哪？小状态栈上；动态缓冲交给 Vec/String/Box
    let flag = true;
    let mut buf = Vec::with_capacity(64); // 2) 谁拥有？buf
    buf.push(1);
    // 3) 会搬家吗？再 push 可能；所以不要边持 &元素边 push（见 [Q5](#q5)）
    let snapshot = buf[0];
    buf.push(snapshot);
    // 4) 何时 Drop？离开 main 时 buf drop → 释放堆
    println!("flag={flag} buf={buf:?}");
}
```

遇到共享与环，把第四问展开成「强计数如何归零」：

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(1);
    let b = Rc::clone(&a);
    assert_eq!(Rc::strong_count(&a), 2);
    drop(b);
    assert_eq!(Rc::strong_count(&a), 1);
    // 无环：最后一次 drop 后归零释放；有环则要 Weak（见 [Q9](#q9)）
    println!("{a}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	buf := make([]int, 0, 64)
	buf = append(buf, 1)
	fmt.Println(buf)
	// 判断题更短：逃逸了吗？有没有并发写？——释放时刻通常不问
}
```

- **Go 怎么做**：更少问「谁 drop」；更多问并发与逃逸。
- **Rust 为什么不同**：释放责任是类型系统的一等公民。
- **Go 程序员易踩的坑**：跳过这四问直接抄 API，最容易在 `E0502`、泄漏、栈溢出上反复摔跤。

**记忆点：**

- 四问：放哪 / 谁有 / 搬家否 / 何时 Drop。
- 扩容 + 旧引用 → 禁止；环 → `Weak`；大块 → 堆。
- 默认为 abort 的 OOM，需要时再 `try_reserve`。

---

## Q17. `clear` / `truncate` 会不会降低 capacity？何时 `shrink_to_fit`？ {#q17}
**Tags:** `common` `vec` `capacity` `shrink`
**适用版本:** Rust 1.0+

**一句话答案：**

不会：`clear` / `truncate` 只改 `len`（丢掉尾部元素），**保留**已分配的 `capacity`；真要还内存给分配器，再显式 `shrink_to_fit`（或 `shrink_to`）。

**解答：**

清空后容量往往还在，这是刻意设计——后面再 `push` 时少分配：

```rust
fn main() {
    let mut v = Vec::with_capacity(64);
    v.extend([1, 2, 3, 4, 5]);
    let cap = v.capacity();
    v.clear(); // 或 truncate(0)
    assert!(v.is_empty());
    assert_eq!(v.capacity(), cap); // capacity 通常不变
    v.shrink_to_fit(); // 请求把缓冲收到贴近 len（这里是 0）
    assert!(v.capacity() <= cap);
    println!("after shrink cap={}", v.capacity());
}
```

`String` 同理：`clear` 不保证缩小缓冲。`shrink_to_fit` 是**请求**，实现可能略大于 `len`，不要当成精确字节协议。

什么时候该 shrink：峰值很大、之后长期很小，且进程会长期活着、内存压力可见。热路径里反复 shrink 再涨，反而多分配、多搬家。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := make([]int, 5, 64)
	v = v[:0] // 缩短 len，cap 仍在
	fmt.Println(len(v), cap(v))
	// 想“真正变小”常重建：v = append([]int(nil), v...) 或换新 slice
}
```

- **Go 怎么做**：`s = s[:0]` 也常保留 `cap`；缩小底层数组通常靠新分配再拷。
- **Rust 为什么不同**：API 把「逻辑清空」和「归还容量」拆开，避免默认付昂贵代价。
- **Go 程序员易踩的坑**：以为 `clear` 等于释放堆，看 RSS 不降就怀疑泄漏。

**记忆点：**

- `clear`/`truncate` → 改 `len`，不保证降 `capacity`。
- 要还内存 → `shrink_to_fit`。
- 热路径别为「好看」反复 shrink。

---

## Q18. `MaybeUninit` 什么时候才该碰？ {#q18}
**Tags:** `advanced` `maybeuninit` `unsafe`
**适用版本:** Rust 1.0+（API 随版本演进；日常业务代码多数用不到）

**一句话答案：**

只在你需要「先占位、后逐个写满、再声明已初始化」且普通 `Option`/`Vec` 表达不了或太贵时才用；读未初始化内存是未定义行为（undefined behavior, UB）。

**解答：**

安全 Rust 默认：值要么已初始化，要么不存在。`MaybeUninit<T>` 表示「这里可能还没写完」，把「初始化完成」变成你的责任。

常见动机（概念）：

```text
1) 手工填固定数组 / 缓冲，避免先 Dummy 再覆盖
2) FFI / 系统调用：对面写入一块你尚未视为有效的内存
3) 性能极致路径：推迟 drop、控制初始化次数（仍要 unsafe 收尾）
```

安全替代优先：`Vec::with_capacity` + `push`、`resize`、`array::from_fn`、`Option<T>`。能用它们就别上 `MaybeUninit`。

错误心智（示意，勿当模板抄）：

```text
// 伪步骤——缺少 assume_init 契约就会 UB：
// let mut slot = MaybeUninit::<u32>::uninit();
// let v = unsafe { slot.assume_init() }; // 还没写入就读 → UB
```

正确路径的要点：每个字节/字段都写过 → 再 `assume_init` / `assume_init_ref`；中途失败要按「已初始化部分」手动 drop 或忘掉。细节见标准库文档；本章只要求记住：**它是 unsafe 边界工具，不是日常容器**。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var buf [4]byte // 零值已定义；Go 没有 MaybeUninit 这套模型
	fmt.Println(buf)
}
```

- **Go 怎么做**：变量多有零值；未初始化直觉弱很多。
- **Rust 为什么不同**：禁止「随便读垃圾位」；要延迟初始化就显式 `MaybeUninit` + `unsafe`。
- **Go 程序员易踩的坑**：把 `uninit` 当 `var x T` 的零值等价物。

**记忆点：**

- 日常：`Vec` / `Option` / `from_fn`。
- `MaybeUninit` = 延迟初始化 + 你保证写满。
- 未写先读 = UB。

---

## Q19. 大结构体要不要 `Box` 来防栈溢出？ {#q19}
**Tags:** `common` `box` `stack` `overflow`
**适用版本:** Rust 1.0+

**一句话答案：**

大块、按值传来传去、或局部会撑爆帧时，**值得**把载荷放堆（`Box`/`Vec`）；小到中等结构体不必条件反射 `Box`——先看大小与调用方式（栈风险总览见 [Q11](#q11)，`Box` 动机见 [Q4](#q4)）。

**解答：**

结构体本身在栈上占 `size_of::<T>()`；按值参数/返回也会搬这一整块（或至少按 ABI 处理大对象）。把大 `T` 换成 `Box<T>` 后，栈上通常只剩一个指针大小：

```rust
struct Big {
    data: [u8; 64 * 1024], // 64 KiB：示意「偏大」；更大块优先 Vec
}

fn touch(b: &Big) -> u8 {
    b.data[0]
}

fn main() {
    // let on_stack = Big { data: [0; 64 * 1024] }; // 大局部：栈压力大
    let on_heap = Box::new(Big {
        data: [0; 64 * 1024],
    });
    println!("{}", touch(&on_heap));
}
```

选型口诀：

1. 真正的大缓冲 → 优先 `Vec`/`String`，别塞固定巨数组进 struct。
2. 必须是单个拥有的大 `T`（递归、异构、API 要 `T`）→ `Box<T>`。
3. 热路径上传小结构体 → 直接值或 `&`/`&mut`，不要为「感觉安全」层层 `Box`。

注意：`Box::new(expr)` 仍可能先在栈上构造 `expr` 再搬到堆；极端尺寸要配合堆上构建策略（如 `vec!`、分步写入）。日常「大数组/大帧」问题，用 `Vec` 往往比「巨型 `Box::new([..])`」更省心。

**Go 对比：**

```go
package main

import "fmt"

type Big struct {
	Data [64 * 1024]byte
}

func main() {
	b := &Big{} // 取地址常促使逃逸到堆
	fmt.Println(b.Data[0])
}
```

- **Go 怎么做**：编译器逃逸分析可能自动把大对象放到堆。
- **Rust 为什么不同**：放哪由类型与 API 显式决定，`Box` 是你写出来的堆所有权。
- **Go 程序员易踩的坑**：以为「Rust 会像 Go 一样自动逃逸」，结果大数组局部直接爆栈。

**记忆点：**

- 大载荷 → 堆（`Box`/`Vec`）；小值别乱箱。
- 按值传来传去放大栈压力。
- 巨缓冲优先 `Vec`，不必硬塞 `[T; N]`。

---
