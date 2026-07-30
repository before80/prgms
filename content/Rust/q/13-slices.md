+++
title = "13-slices"
date = 2026-07-28T14:49:00+08:00
weight = 130
type = "docs"
description = "面向熟悉 Go 的读者讲清切片视图、胖指针、UTF-8 边界与参数选型"
isCJKLanguage = true
draft = false

+++

# 切片 (Slices)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你是否分不清 `&[T]`、`&str`、数组和 `Vec`，总把它们当成同一种“列表”？
- 你是否写过 `v[i]` 越界 panic，却不知道何时该改用 `get()`？
- 你是否想从 `Vec<String>` 里 `v[0]` 拿走一个 `String`，结果撞上 `error[E0507]`？
- 你是否疑惑：Go 的 `[]T` 和 Rust 的切片长得很像，为什么生命周期和可变规则差这么多？
- 你是否拿不准函数参数该写 `&[T]` 还是 `Vec<T>`？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| slice | — | 切片 | 对连续序列的借用视图，不拥有数据 | `[]T` / `string` 头 |
| fat pointer | — | 胖指针 | 指针 + 长度（有时再加元数据）的宽指针 | slice header（ptr+len，无 cap） |
| **DST** | Dynamically Sized Type | 动态大小类型 | 编译期大小未知，必须通过指针使用 | 无直接对应 |
| UTF-8 | UTF-8 | UTF-8 编码 | 一个字符可能占 1～4 字节 | Go 的 `string` 也是 UTF-8 字节序列 |
| borrow | — | 借用 | 临时看或改，但不接管所有权 | 传指针 / 传切片头 |
| lifetime | — | 生命周期 | 引用允许存活的作用域上限 | 无编译期对应物 |
| `Deref` | Dereference | 解引用转换 | 让 `String`/`Vec` 等“表现得像”切片 | 无直接对应 |
| owner | — | 所有者 | 负责这份值最终释放的人 | 无（Go 靠 GC） |
| **GC** | Garbage Collector | 垃圾回收器 | 运行时扫描并回收不用对象的机制 | Go 默认机制 |
| **RAII** | Resource Acquisition Is Initialization | 资源获取即初始化 | 资源跟着值的生命周期自动释放 | Go 里常要手写 `defer` |
| `Copy` | — | 按位复制 trait | 赋值后原变量仍可用的小值类型 | Go 的普通值拷贝 |
| `Clone` | — | 显式克隆 trait | 需要你手动调用的复制操作 | 手写深拷贝 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q15](#q15), [Q16](#q16) |
| `occasional` | [Q12](#q12), [Q13](#q13) |
| `advanced` | [Q14](#q14) |

---

## Q1. `&[T]` 和 `&str` 本质上是什么？ {#q1}
**Tags:** `hot` `beginner` `slice`
**适用版本:** Rust 1.0+（1.97.1 行为一致）

**一句话答案：**

`&[T]` 是对连续 `T` 序列的**借用视图**；`&str` 是对一段保证有效 **UTF-8**（UTF-8 编码：一个字符可能占 1～4 字节）文本的借用视图——二者都不拥有底层数据。

**解答：**

切片（slice）不是“另一份列表”，而是对着已有内存开的一扇窗口：窗口里有起点和长度，真正的数据仍归数组、`Vec` 或 `String` 所有。

```rust
fn main() {
    let a = [10, 20, 30, 40];
    let s: &[i32] = &a[1..3]; // 窗口 [20, 30]
    assert_eq!(s, &[20, 30]);
    println!("{s:?}");
}
```

同一套语法也能切 `Vec` / `String`——切的是借用，不是拷贝整份缓冲：

```rust
fn main() {
    let v = vec![1, 2, 3, 4];
    let owned = String::from("hello");
    let s1: &[i32] = &v[1..];
    let s2: &str = &owned[0..4];
    assert_eq!(s1, &[2, 3, 4]);
    assert_eq!(s2, "hell");
}
```

可变切片改的是原数据，进一步证明“窗口”语义：

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    let window: &mut [i32] = &mut v[1..3];
    window[0] = 99;
    assert_eq!(v, [1, 99, 3, 4]);
}
```

`&str` 的底层是字节，但类型契约比 `&[u8]` 更严：内容必须始终是有效 UTF-8。字符串细节见 [14-strings-and-text](../14-strings-and-text/#q1)。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := [4]int{10, 20, 30, 40}
	s := a[1:3] // []int，指向同一底层数组
	fmt.Println(s)
}
```

- **Go 怎么做**：`[]T` / `string` 也是对底层数组的窗口（再加 capacity 等字段）。
- **Rust 为什么不同**：Rust 把“窗口能活多久、能不能同时可变”交给借用检查器，而不是留给你和 GC。
- **Go 程序员易踩的坑**：别把切片当成“复制了一份元素”；两边改的都是同一块底层内存。

**记忆点：**

- `&[T]` / `&str` = 借用视图，不拥有数据。
- 改可变切片 = 改源数据。
- `&str` 额外保证 UTF-8 有效。

---

## Q2. 为什么切片不拥有数据？ {#q2}
**Tags:** `hot` `beginner` `slice` `ownership`
**适用版本:** Rust 1.0+

**一句话答案：**

因为切片的设计目标是“零成本偷看一段连续内存”；所有权仍在源数据上，切片离开作用域时只丢掉窗口，不会释放底层缓冲。

**解答：**

若 `&[T]` 也拥有数据，那每次取子区间都要拷贝或转移所有权，API 会又慢又难用。Rust 的选择是：所有者负责释放（**RAII**：Resource Acquisition Is Initialization，资源获取即初始化），切片只借用。

```rust
fn main() {
    let v = vec![1, 2, 3];
    {
        let s: &[i32] = &v[1..];
        assert_eq!(s, &[2, 3]);
    } // s 结束；v 仍拥有堆上数据
    assert_eq!(v, [1, 2, 3]);
}
```

正因为不拥有，切片不能独自“活过”源数据——源数据被 drop 后，窗口会变成悬垂引用，编译器直接禁止：

```rust
fn main() {
    let s: &[i32];
    {
        let v = vec![1, 2, 3];
        s = &v[..];
        // error[E0597]: `v` does not live long enough
    }
    // println!("{s:?}");
}
```

需要真正拥有一段切片数据时，用 `Vec<T>` / `String`，或 `Box<[T]>` / `Box<str>`（堆上拥有的切片），而不是指望 `&[T]` 自己保管内存。

```rust
fn main() {
    let owned: Box<[i32]> = vec![1, 2, 3].into_boxed_slice();
    let view: &[i32] = &owned; // 再借一层窗口
    assert_eq!(view, &[1, 2, 3]);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	s := v[1:]
	fmt.Println(s, v)
	// 底层数组由 GC 回收；没有“单一所有者必须 drop”的编译期规则
}
```

- **Go 怎么做**：slice 头也不拥有“独占释放权”，底层数组何时回收交给 **GC**（Garbage Collector，垃圾回收器）。
- **Rust 为什么不同**：没有 GC 时，必须把“谁释放”钉死在所有者上；切片只能借。
- **Go 程序员易踩的坑**：在 Rust 里返回指向局部 `Vec` 的切片，会直接编译失败——这是特性，不是刁难。

**记忆点：**

- 切片 = 窗口；所有者 = 负责释放的人。
- 窗口结束 ≠ 释放缓冲。
- 要拥有 → `Vec` / `String` / `Box<[T]>`。

---

## Q3. 索引和 `get()` 该怎么选？ {#q3}
**Tags:** `hot` `beginner` `indexing`
**适用版本:** Rust 1.0+

**一句话答案：**

`s[i]` / `s[a..b]` 在越界（或对 `&str` 切到非字符边界）时 **panic**；`get` / `get_mut` 返回 `Option`，失败是 `None`——库代码和不可信输入优先 `get`。

**解答：**

索引写法短，但契约是“调用者保证合法”。越界会直接崩：

```rust
fn main() {
    let v = vec![10, 20, 30];
    assert_eq!(v[1], 20);
    // let _ = v[100];
    // 运行时 panic: index out of bounds
    let y = v.get(1);   // Some(&20)
    let z = v.get(100); // None
    assert_eq!(y, Some(&20));
    assert!(z.is_none());
}
```

对 `&str` 还有 UTF-8 字符边界问题：索引按**字节**，切到多字节字符中间会 panic；`get(range)` 则返回 `None`：

```rust
fn main() {
    let s = "你好"; // “你”占 3 字节
    // let bad = &s[0..1];
    // 运行时 panic: byte index 1 is not a char boundary
    assert_eq!(s.get(0..1), None);
    assert_eq!(s.get(0..3), Some("你"));
}
```

确定合法、且在热路径上，才考虑索引；不确定时用 `get`，或先用 `is_char_boundary` / `char_indices` 找安全切点：

```rust
fn main() {
    let s = "你好a";
    assert!(s.is_char_boundary(3));
    assert!(!s.is_char_boundary(1));
    for (i, c) in s.char_indices() {
        println!("{i}: {c}");
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{10, 20, 30}
	fmt.Println(v[1])
	// v[100] 同样 panic
	s := "你好"
	fmt.Println(s[0:3]) // 按字节切；切错同样可能得到坏串或 panic
}
```

- **Go 怎么做**：下标越界同样 panic；字符串切片也是字节级。
- **Rust 为什么不同**：Rust 用类型系统保证 `&str` 永远是有效 UTF-8，所以非法字符边界直接拒绝。
- **Go 程序员易踩的坑**：把 `len(s)` 当“字符数”，再按字符数去切 `&str`，极易 panic。

**记忆点：**

- 越界索引 → panic；`get` → `None`。
- `&str` 必须切在字符边界，否则 panic；`get` 更安全。
- 不可信输入优先 `get` / `chars`。

---

## Q4. 为什么不能从切片索引里 move 出 `String`？ {#q4}
**Tags:** `hot` `beginner` `move` `E0507`
**适用版本:** Rust 1.0+

**一句话答案：**

`v[i]` 对非 `Copy` 元素只能给出借用；若允许 `let s = v[0]` 把 `String` move 走，会在 `Vec` 里留下“空洞”，破坏容器不变量——因此编译器报 `error[E0507]`。

**解答：**

`i32` 实现了 `Copy`，索引看起来像“取值”；`String` 没有 `Copy`，索引不能搬走：

```rust
fn main() {
    let mut v = vec![String::from("a"), String::from("b")];
    // let s = v[0];
    // error[E0507]: cannot move out of index of `Vec<String>`
    println!("{}", v[0]); // 只能借用打印
    let _ = &mut v;
}
```

「✅ 正确写法」——需要所有权时，用会真正取出元素的 API，或显式克隆：

```rust
fn main() {
    let mut v = vec![String::from("a"), String::from("b")];
    let cloned = v[0].clone();
    let removed = v.remove(0); // 取出并留下空位填补
    assert_eq!(cloned, "a");
    assert_eq!(removed, "a");
    assert_eq!(v, ["b"]);
}
```

切片本身也一样：`&[String]` 上的索引更不可能 move，因为你连容器所有权都没有：

```rust
fn first_owned(xs: &[String]) -> String {
    // xs[0] // 不能 move
    xs[0].clone()
}

fn main() {
    let v = vec![String::from("hi")];
    assert_eq!(first_owned(&v), "hi");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []string{"a", "b"}
	s := v[0] // 复制 string 头；底层字节由运行时共享/管理
	fmt.Println(s, v[0])
}
```

- **Go 怎么做**：赋值通常复制值头；没有“从切片 move 走所有权”的编译期概念。
- **Rust 为什么不同**：`String` 有唯一所有者；随意 move 出会让 `Vec` 无法安全 drop 剩余元素。
- **Go 程序员易踩的坑**：看到 `v[i]` 就以为能拿到所有权；在 Rust 里先想“借、clone，还是 `remove`/`swap_remove`/`pop`”。

**记忆点：**

- `E0507` = 不能从索引 move 出非 `Copy` 值。
- 借用 / `clone` / `remove`（等）三选一。
- 切片上更不可能 move——你只是访客。

---

## Q5. `String` / `Vec` 为什么能自动变成切片？ {#q5}
**Tags:** `common` `beginner` `deref`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 `String` 实现了 `Deref<Target = str>`，`Vec<T>` 实现了 `Deref<Target = [T]>`——在需要 `&str` / `&[T]` 的地方，编译器会自动做 **Deref**（Dereference，解引用转换）强制。

**解答：**

这就是为什么 API 参数写 `&str` / `&[T]` 最友好：调用方可以传字面量、`String`、`Vec`、数组引用：

```rust
fn take_str(s: &str) {
    assert!(!s.is_empty());
}

fn take_slice(s: &[u8]) {
    assert_eq!(s.len(), 3);
}

fn main() {
    let s = String::from("hi");
    take_str(&s);        // &String -> &str
    take_str(s.as_str());

    let v = vec![1u8, 2, 3];
    take_slice(&v);      // &Vec<u8> -> &[u8]
    take_slice(v.as_slice());
}
```

数组也一样，`&[T; N]` 可以强制成 `&[T]`：

```rust
fn sum(xs: &[i32]) -> i32 {
    xs.iter().sum()
}

fn main() {
    let a = [1, 2, 3];
    let v = vec![4, 5];
    assert_eq!(sum(&a), 6);
    assert_eq!(sum(&v), 9);
}
```

**Go 对比：**

```go
package main

import "fmt"

func take(s []int) {
	fmt.Println(s)
}

func main() {
	a := [3]int{1, 2, 3}
	take(a[:]) // 数组要显式切成 slice
	v := []int{4, 5}
	take(v)
}
```

- **Go 怎么做**：数组到 slice 通常要写 `a[:]`；`string` 与 `[]byte` 转换常显式拷贝或转换。
- **Rust 为什么不同**：`Deref` 让“拥有型容器”在只读 API 里表现得像切片，减少样板代码。
- **Go 程序员易踩的坑**：以为 `&String` 和 `&str` 是两种完全不能互通的类型——多数只读场景可以直接传 `&s`。

**记忆点：**

- 参数优先 `&str` / `&[T]`。
- `&String` / `&Vec<T>` 常自动变成切片引用。
- 需要所有权时再收 `String` / `Vec<T>`。

---

## Q6. 切片是不是 **DST**（动态大小类型）？ {#q6}
**Tags:** `common` `intermediate` `dst`
**适用版本:** Rust 1.0+

**一句话答案：**

是。`[T]` 与 `str` 都是 **DST**（Dynamically Sized Type，动态大小类型：编译期大小未知）；你日常写的 `&[T]` / `&str` 是指向它们的**胖指针**（fat pointer：数据指针 + 长度）。

**解答：**

普通引用 `&i32` 是一个指针宽；切片引用要额外记住“这段有多长”，所以通常是两个字宽：

```rust
use std::mem::size_of;

fn main() {
    assert_eq!(size_of::<&i32>(), size_of::<usize>());
    assert_eq!(size_of::<&[u8]>(), size_of::<usize>() * 2);
    assert_eq!(size_of::<&str>(), size_of::<usize>() * 2);
}
```

正因为 `[T]` / `str` 大小未知，不能按值放在变量里或直接作为函数返回类型（除非藏在指针后面）：

```rust
fn main() {
    let a = [1, 2, 3];
    let s: &[i32] = &a; // OK：胖指针大小已知
    // let unsized: [i32] = *s; // 不能：DST 不能按值存放
    assert_eq!(s.len(), 3);
}
```

`Box<[T]>`、`Box<str>` 同样是胖指针，但拥有堆上数据——这是“拥有的切片”，不是借用窗口。

**Go 对比：**

```go
package main

import (
	"fmt"
	"unsafe"
)

func main() {
	var p *int
	var s []int
	fmt.Println(unsafe.Sizeof(p)) // 通常 1 个字
	fmt.Println(unsafe.Sizeof(s)) // 通常 3 个字：ptr+len+cap
}
```

- **Go 怎么做**：`[]T` 头固定大小（含 cap）；没有“无大小的 `[T]` 类型”这种语言层 DST。
- **Rust 为什么不同**：把“变长序列本身”建模成 DST，再用胖指针引用，类型更精确。
- **Go 程序员易踩的坑**：把 `&[T]` 想成 Go 的三字段 slice；Rust 借用切片通常只有 ptr+len，cap 在 `Vec` 上。

**记忆点：**

- `[T]` / `str` = DST；`&[T]` / `&str` = 胖指针。
- 胖指针 ≈ 指针 + 长度。
- 不能把 DST 当普通栈变量“裸拿”。

---

## Q7. 范围语法 `a[..]` 到底有哪些变体？ {#q7}
**Tags:** `common` `beginner` `range`
**适用版本:** Rust 1.0+；`..=` 包容范围为稳定特性

**一句话答案：**

常用的是 `start..end`（不含 end）、`start..=end`（含 end），以及省略一端的 `..end`、`start..`、`..`（全切片）。

**解答：**

```rust
fn main() {
    let a = [0, 1, 2, 3, 4];
    assert_eq!(&a[1..3], &[1, 2]);
    assert_eq!(&a[1..=3], &[1, 2, 3]);
    assert_eq!(&a[..2], &[0, 1]);
    assert_eq!(&a[2..], &[2, 3, 4]);
    assert_eq!(&a[..], &[0, 1, 2, 3, 4]);
}
```

对 `str` 同样用范围，但边界必须是 UTF-8 字符边界，否则与 [Q3](#q3) 一样会 panic；不确定时用 `get`：

```rust
fn main() {
    let s = "hello";
    assert_eq!(&s[1..4], "ell");
    assert_eq!(s.get(1..4), Some("ell"));
    assert_eq!(s.get(10..), None); // 越界 → None，不 panic
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := []int{0, 1, 2, 3, 4}
	fmt.Println(a[1:3]) // 半开区间，同 Rust 的 1..3
	fmt.Println(a[:2])
	fmt.Println(a[2:])
	fmt.Println(a[:])
	// Go 没有 a[1:3] 的“含尾”语法；要含 3 就写 a[1:4]
}
```

- **Go 怎么做**：`low:high` 一律半开；靠调整 high 表达“含尾”。
- **Rust 为什么不同**：额外提供 `..=`，意图更直白。
- **Go 程序员易踩的坑**：把 Go 的 `a[1:3]` 写成 Rust `a[1..=3]`，会多切一个元素。

**记忆点：**

- `..` 半开；`..=` 含尾。
- 可省略 start / end / 两端。
- `&str` 范围仍受 UTF-8 边界约束。

---

## Q8. 为什么 `split_at_mut` 能安全拿两段可变切片？ {#q8}
**Tags:** `common` `intermediate` `split_at_mut`
**适用版本:** Rust 1.0+

**一句话答案：**

因为标准库保证两段**不重叠**；不重叠就没有别名可变借用，满足借用规则——这是 [12-references-and-borrowing](../12-references-and-borrowing/#q14) 里的经典解法。

**解答：**

「❌ 错误写法」——对同一数组直接取两个 `&mut`：

```rust
fn main() {
    let mut a = [0, 1, 2, 3, 4];
    let l = &mut a[0];
    let r = &mut a[2];
    // error[E0499]: cannot borrow `a` as mutable more than once at a time
    *l = 8;
    *r = 9;
}
```

「✅ 正确写法」——`split_at_mut` 一次切开：

```rust
fn main() {
    let mut a = [0, 1, 2, 3, 4];
    let (left, right) = a.split_at_mut(2);
    left[0] = 8;
    right[0] = 9;
    assert_eq!(a, [8, 1, 9, 3, 4]);
}
```

编译器自己推不出“这两个下标不重叠”，但 `split_at_mut` 的实现用 unsafe 证明了这一点，并把安全接口暴露给你。需要多个离散位置时，可用 `get_disjoint_mut`（1.86+）。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := []int{0, 1, 2, 3, 4}
	l, r := a[:2], a[2:]
	l[0], r[0] = 8, 9
	fmt.Println(a) // [8 1 9 3 4]
}
```

- **Go 怎么做**：本来就可以把一个 slice 切成两段再分别改；语言不静态检查重叠。
- **Rust 为什么不同**：默认禁止两个 `&mut`；只有证明不重叠的 API 才能放行。
- **Go 程序员易踩的坑**：下意识写两个 `&mut a[i]`，在 Rust 里会被硬拦。

**记忆点：**

- 两个 `&mut` 默认不行。
- `split_at_mut` = 安全的不重叠分割。
- 重叠别名可变 = 数据竞争温床。

---

## Q9. `&str` 为什么既像字符串又像切片？ {#q9}
**Tags:** `common` `beginner` `str` `utf8`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 `&str` 在形态上就是“字符串版的 `&[u8]`”：同样是胖指针窗口；但它额外承诺内容是有效 UTF-8，并提供文本向的方法。

**解答：**

字面量 `"hi"` 的类型是 `&'static str`；`String` 解引用后也能得到 `&str`：

```rust
fn show(s: &str) {
    println!("{s} (bytes={})", s.len());
}

fn main() {
    show("hi");
    let owned = String::from("hello");
    show(&owned);
}
```

你可以把它当成字节切片看，但要回到 `&str` 必须再次验证 UTF-8：

```rust
fn main() {
    let s = "Rust";
    let bytes: &[u8] = s.as_bytes();
    let back = std::str::from_utf8(bytes).unwrap();
    assert_eq!(s, back);
}
```

索引、范围、生命周期规则与普通切片一致，只是多了字符边界约束；更完整的字符串故事见 [14-strings-and-text](../14-strings-and-text/#q1)。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "Rust"
	b := []byte(s) // 通常复制
	fmt.Println(string(b))
}
```

- **Go 怎么做**：`string` 与 `[]byte` 是近亲，转换常见且语义偏“值头/字节序列”。
- **Rust 为什么不同**：`&str` 与 `&[u8]` 类型分开，用 UTF-8 不变量换取更安全的文本 API。
- **Go 程序员易踩的坑**：把 `&str` 当成可改的 `[]byte`；要改文本通常应使用 `String`。

**记忆点：**

- `&str` ≈ 保证 UTF-8 的字符串切片。
- 像切片一样借；像字符串一样用文本 API。
- 可变文本 → `String`，只读视图 → `&str`。

---

## Q10. 切片生命周期为什么总是跟源数据绑在一起？ {#q10}
**Tags:** `common` `lifetime` `borrow`
**适用版本:** Rust 1.0+

**一句话答案：**

因为切片是借用：它的 **lifetime**（生命周期：引用允许存活的作用域上限）不能超过源数据，否则会变成悬垂指针。

**解答：**

子切片的生命周期标注会跟输入走：

```rust
fn tail<'a>(s: &'a [u8]) -> &'a [u8] {
    &s[1..]
}

fn main() {
    let data = [1u8, 2, 3, 4];
    let t = tail(&data);
    assert_eq!(t, &[2, 3, 4]);
}
```

从 `Vec` 取出的切片，在可能触发重分配的 `&mut Vec` 操作面前会失效——借用检查器会挡住 use-after-realloc：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let s = &v[..];
    // v.push(4);
    // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    println!("{s:?}");
}
```

想让切片“独立活下去”，只能拷贝出拥有型数据（`to_vec` / `to_string`），不能延长借用。

**Go 对比：**

```go
package main

import "fmt"

func tail(s []byte) []byte {
	return s[1:]
}

func main() {
	data := []byte{1, 2, 3, 4}
	t := tail(data)
	fmt.Println(t)
	// 底层数组仍可能被别的别名修改；没有编译期生命周期
}
```

- **Go 怎么做**：slice 头可随便返回；悬垂问题靠 GC 与程序员纪律缓解。
- **Rust 为什么不同**：生命周期把“窗口不能长过房子”写成类型的一部分。
- **Go 程序员易踩的坑**：从函数返回指向局部数组的切片——在 Rust 里直接 `E0515` / 生命周期错误。

**记忆点：**

- 切片寿命 ≤ 源数据寿命。
- 持有切片时，别对源做可能失效借用的可变操作。
- 要独立副本 → `to_vec` / `to_string`。

---

## Q11. 什么时候参数应该写成 `&[T]` 而不是 `Vec<T>`？ {#q11}
**Tags:** `common` `api` `slice`
**适用版本:** Rust 1.0+

**一句话答案：**

只要函数只**读**（或通过 `&mut [T]` 就地改）元素、不需要拿走所有权或增长缓冲，就写 `&[T]` / `&mut [T]`；只有要拥有、要 `push`/`append` 时才收 `Vec<T>`。

**解答：**

`&[T]` 让数组、`Vec`、子切片都能传入，调用成本更低：

```rust
fn mean(xs: &[f64]) -> Option<f64> {
    if xs.is_empty() {
        return None;
    }
    Some(xs.iter().sum::<f64>() / xs.len() as f64)
}

fn main() {
    let a = [1.0, 2.0, 3.0];
    let v = vec![4.0, 5.0];
    assert_eq!(mean(&a), Some(2.0));
    assert_eq!(mean(&v), Some(4.5));
}
```

「❌ 不必要的所有权」——只求和却吃掉 `Vec`，调用方每次都要重建或 clone：

```rust
fn mean_owned(xs: Vec<f64>) -> Option<f64> {
    if xs.is_empty() {
        return None;
    }
    Some(xs.iter().sum::<f64>() / xs.len() as f64)
}

fn main() {
    let v = vec![1.0, 2.0];
    let m = mean_owned(v);
    // println!("{:?}", v);
    // error[E0382]: borrow of moved value: `v`
    assert_eq!(m, Some(1.5));
}
```

字符串同理：只读文本用 `&str`，要拥有再用 `String`。

**Go 对比：**

```go
package main

import "fmt"

func mean(xs []float64) (float64, bool) {
	if len(xs) == 0 {
		return 0, false
	}
	var sum float64
	for _, x := range xs {
		sum += x
	}
	return sum / float64(len(xs)), true
}

func main() {
	a := []float64{1, 2, 3}
	m, ok := mean(a)
	fmt.Println(m, ok)
}
```

- **Go 怎么做**：只读函数几乎总是收 `[]T`，很少有人传“拥有型容器类型”这种区分。
- **Rust 为什么不同**：`Vec<T>` 参数意味着可能 move；`&[T]` 明确“只借用不接管”。
- **Go 程序员易踩的坑**：照着自己的结构体字段类型把参数写成 `Vec<T>`，结果把调用方数据吃掉。

**记忆点：**

- 只看 / 就地改 → `&[T]` / `&mut [T]`。
- 要拥有或扩容 → `Vec<T>`。
- 文本同理：`&str` vs `String`。

---

## Q12. Go 的 slice 和 Rust 的 slice 最像，但差在哪？ {#q12}
**Tags:** `occasional` `beginner` `go`
**适用版本:** Rust 1.0+

**一句话答案：**

形态上都是“指向连续内存的窗口”；差别在于 Rust 切片通常无 cap、强绑定生命周期与借用规则，且 `&str` 有 UTF-8 不变量。

**解答：**

先看并排直觉：两边都能从已有序列切出子区间并共享底层存储：

```rust
fn main() {
    let mut v = vec![10, 20, 30, 40];
    let s = &mut v[1..3];
    s[0] = 99;
    assert_eq!(v, [10, 99, 30, 40]);
}
```

关键差异可以记三张卡片：

1. **头字段**：Go `[]T` 常有 ptr+len+cap；Rust `&[T]` 通常只有 ptr+len，cap 在 `Vec`。
2. **别名规则**：Go 允许多个 slice 同时改重叠区域（数据竞争靠你）；Rust 禁止重叠 `&mut`。
3. **寿命**：Go 靠 GC；Rust 切片不能活过源数据。

```rust
fn main() {
    let v = vec![1, 2, 3];
    let a = &v[..];
    let b = &v[1..];
    // 多个不可变切片没问题
    assert_eq!(a[0] + b[0], 3);
    // 但不能同时再拿 &mut v[..]
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{10, 20, 30, 40}
	s := v[1:3]
	s[0] = 99
	fmt.Println(v) // [10 99 30 40]，共享底层数组

	a := v[:2]
	b := v[1:3]
	a[1] = 7
	fmt.Println(b[0]) // 7：重叠区域互相可见，编译器不拦
}
```

- **Go 怎么做**：slice 是日常一等公民，append 可能换底层数组，别名问题运行时自行小心。
- **Rust 为什么不同**：把共享/可变/寿命前移到编译期，换取无数据竞争的默认安全。
- **Go 程序员易踩的坑**：把 Rust `&mut [T]` 当成可以随意重叠再切的 Go slice。

**记忆点：**

- 像：都是窗口，共享底层。
- 不像：cap、借用规则、生命周期、UTF-8。
- 迁移口诀：先借后改，别假设能乱别名。

---

## Q13. 数组、切片、`Vec` 到底怎么分工？ {#q13}
**Tags:** `occasional` `beginner` `array` `vec`
**适用版本:** Rust 1.0+

**一句话答案：**

`[T; N]` 固定长度、通常栈上拥有；`[T]` / `&[T]` 是动态长度视图；`Vec<T>` 是可增长的堆上所有者——三者常通过切片 API 互通。

**解答：**

```rust
fn main() {
    let arr: [i32; 3] = [1, 2, 3];      // 拥有，长度写进类型
    let slice: &[i32] = &arr[1..];      // 借用视图
    let mut v: Vec<i32> = vec![4, 5]; // 拥有，可 push
    v.push(6);
    assert_eq!(slice, &[2, 3]);
    assert_eq!(v, [4, 5, 6]);
}
```

选型和参数传递的经验法则：

```rust
fn only_three(xs: &[i32; 3]) -> i32 {
    xs.iter().sum()
}

fn any_len(xs: &[i32]) -> i32 {
    xs.iter().sum()
}

fn main() {
    let arr = [1, 2, 3];
    let v = vec![1, 2, 3, 4];
    assert_eq!(only_three(&arr), 6);
    assert_eq!(any_len(&arr), 6);
    assert_eq!(any_len(&v), 10);
}
```

| 类型 | 大小 | 拥有？ | 典型场景 |
|------|------|--------|----------|
| `[T; N]` | 固定 N | 是 | 小缓冲、长度是类型的一部分 |
| `&[T]` | 胖指针 | 否 | API 只读/就地改 |
| `Vec<T>` | 指针+len+cap | 是 | 运行期增长 |

**Go 对比：**

```go
package main

import "fmt"

func main() {
	arr := [3]int{1, 2, 3}
	s := arr[:]      // 数组 → slice
	v := []int{4, 5} // 动态 slice（常在堆上）
	v = append(v, 6)
	fmt.Println(s, v)
}
```

- **Go 怎么做**：数组少用，日常几乎都是 `[]T`。
- **Rust 为什么不同**：把“固定长 / 借用视图 / 可增长拥有”拆开，避免一个类型扛所有语义。
- **Go 程序员易踩的坑**：把 Rust 数组当成 Go 数组那样很少用——在 Rust 里 `[T; N]` 很常见且零成本。

**记忆点：**

- 固定长 → 数组；窗口 → 切片；可增长 → `Vec`。
- API 默认收 `&[T]`。
- 需要 cap/push 才上 `Vec`。

---

## Q14. 本章最值得背的切片规则是什么？ {#q14}
**Tags:** `advanced` `summary` `slice`
**适用版本:** Rust 1.0+

**一句话答案：**

切片是借用窗口：不拥有、寿命绑源数据、索引可能 panic、非 `Copy` 不能从索引 move，API 优先 `&[T]` / `&str`。

**解答：**

把前面各题收成一张可背清单，并配两个最小例子钉牢：

```rust
fn total(xs: &[i32]) -> i32 {
    xs.iter().sum()
}

fn main() {
    let arr = [1, 2, 3];
    let v = vec![4, 5];
    assert_eq!(total(&arr), 6);
    assert_eq!(total(&v), 9);
    assert_eq!(v.get(10), None); // 不确定就 get
}
```

```rust
fn main() {
    let mut v = vec![String::from("a"), String::from("b")];
    // let s = v[0];
    // error[E0507]: cannot move out of index of `Vec<String>`
    let s = v.remove(0);
    assert_eq!(s, "a");
}
```

背诵版：

1. `&[T]` / `&str` = 窗口，不是所有者。
2. 胖指针 = 指针 + 长度；`[T]` / `str` 是 DST。
3. 越界索引 / UTF-8 半字符切片 → panic；`get` → `None`。
4. 索引不能 move 出 `String` 等非 `Copy`（`E0507`）。
5. 参数优先 `&[T]` / `&str`；`split_at_mut` 解决两段可变。
6. 寿命 ≤ 源数据；要独立副本就 `to_vec` / `to_string`。

**Go 对比：**

```go
package main

import "fmt"

func total(xs []int) int {
	n := 0
	for _, x := range xs {
		n += x
	}
	return n
}

func main() {
	fmt.Println(total([]int{1, 2, 3}))
}
```

- **Go 怎么做**：`[]T` 几乎通吃；越界仍 panic，但没有 move/`E0507` 这套。
- **Rust 为什么不同**：切片规则是所有权与借用在“连续内存视图”上的具体化。
- **Go 程序员易踩的坑**：只记住“和 Go slice 很像”，却忘了生命周期与 move 规则。

**记忆点：**

- 窗口、不拥有、寿命绑定。
- panic vs `None`；`E0507` 不能索引 move。
- API 写 `&[T]` / `&str`，需要时再 `Vec` / `String`。

---

## Q15. 切片怎么用 `chunks` / `windows` 切块？ {#q15}
**Tags:** `common` `beginner` `chunks` `windows`
**适用版本:** Rust 1.0+

**一句话答案：**

`chunks(n)` / `chunks_mut(n)` 把切片切成**不重叠**的长度至多为 `n` 的块；`windows(n)` 给出长度恰好为 `n` 的**滑动窗口**（相邻窗口重叠）。

**解答：**

按固定大小分批处理时用 `chunks`：最后一块可以短于 `n`。只要完整块、剩余单独处理，用 `chunks_exact`：

```rust
fn main() {
    let data = [1, 2, 3, 4, 5];
    let parts: Vec<&[i32]> = data.chunks(2).collect();
    assert_eq!(parts, vec![&[1, 2][..], &[3, 4][..], &[5][..]]);

    let exact: Vec<&[i32]> = data.chunks_exact(2).collect();
    assert_eq!(exact, vec![&[1, 2][..], &[3, 4][..]]);
    assert_eq!(data.chunks_exact(2).remainder(), &[5]);
}
```

需要看“当前元素和邻居”时用 `windows`：每一步只前进 1，窗口互相重叠：

```rust
fn main() {
    let data = [10, 20, 30, 40];
    let w: Vec<&[i32]> = data.windows(3).collect();
    assert_eq!(w, vec![&[10, 20, 30][..], &[20, 30, 40][..]]);
}
```

可变分块用 `chunks_mut`（窗口没有通用的 `windows_mut`，因为重叠可变借用不安全）：

```rust
fn main() {
    let mut data = [1, 2, 3, 4];
    for chunk in data.chunks_mut(2) {
        chunk[0] *= 10;
    }
    assert_eq!(data, [10, 2, 30, 4]);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	data := []int{1, 2, 3, 4, 5}
	for i := 0; i < len(data); i += 2 {
		end := i + 2
		if end > len(data) {
			end = len(data)
		}
		fmt.Println(data[i:end]) // 手写 chunks
	}
}
```

- **Go 怎么做**：通常手写步长循环，或自己封装切块函数。
- **Rust 为什么不同**：标准库把“不重叠分块”和“滑动窗口”做成迭代器 API，少写边界算术。
- **Go 程序员易踩的坑**：把 `windows(n)` 当成 `chunks(n)`，结果块数变多且内容重叠。

**记忆点：**

- `chunks` = 不重叠切块；末块可能更短。
- `windows` = 滑动重叠窗口。
- 要改元素 → `chunks_mut`，别指望重叠的可变 `windows`。

---

## Q16. `copy_from_slice` 怎么安全拷贝？ {#q16}
**Tags:** `common` `beginner` `copy_from_slice`
**适用版本:** Rust 1.0+

**一句话答案：**

`dst.copy_from_slice(src)` 要求两边**长度相等**且元素实现 `Copy`，一次把 `src` 拷进 `dst`；长度不匹配会 **panic**——先比 `len`，或改用等长的子切片。

**解答：**

最常见用法：准备好同样长的目标缓冲，再拷：

```rust
fn main() {
    let src = [1, 2, 3, 4];
    let mut dst = [0; 4];
    dst.copy_from_slice(&src);
    assert_eq!(dst, [1, 2, 3, 4]);
}
```

只覆盖一部分时，先切出等长窗口再拷——这比“整片长度碰巧对上”更清晰：

```rust
fn main() {
    let src = [10, 20, 30];
    let mut dst = [0; 5];
    dst[1..4].copy_from_slice(&src);
    assert_eq!(dst, [0, 10, 20, 30, 0]);
}
```

「❌ 错误写法」——长度不等会直接 panic（不是返回 `Result`）：

```rust
fn main() {
    let src = [1, 2, 3];
    let mut dst = [0; 2];
    // dst.copy_from_slice(&src);
    // 运行时 panic: copy_from_slice: source slice length (3) does not match destination slice length (2)
    assert_eq!(src.len(), 3);
    assert_eq!(dst.len(), 2);
}
```

元素没有 `Copy` 时，用 `clone_from_slice`（需要 `Clone`），或逐个赋值 / `to_vec` 之类显式策略。不确定长度时，先 `assert_eq!(dst.len(), src.len())`，或只对 `dst.get_mut(..src.len())` 这类已核对过的窗口操作。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	src := []int{1, 2, 3, 4}
	dst := make([]int, 4)
	n := copy(dst, src) // 拷 min(len(dst), len(src)) 个，不因不等长而 panic
	fmt.Println(dst, n)
}
```

- **Go 怎么做**：内建 `copy` 按较短那边的长度拷，返回实际拷贝个数。
- **Rust 为什么不同**：`copy_from_slice` 契约更严——等长才拷，避免静默截断。
- **Go 程序员易踩的坑**：照 Go 习惯假定“多出来的自动丢掉”；在 Rust 里长度不对会直接崩。

**记忆点：**

- 等长 + `Copy` → `copy_from_slice`。
- 不等长 → panic；先切齐或先检查 `len`。
- 非 `Copy` → `clone_from_slice`（或别的显式拷贝）。

---
