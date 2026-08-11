+++
title = "35-Unsafe Rust"
date = 2026-07-28T14:49:00+08:00
weight = 350
type = "docs"
description = "面向 Go 开发者讲清 Unsafe Rust、UB、FFI、裸指针与安全抽象边界"
isCJKLanguage = true
draft = false

+++

# Unsafe Rust (Unsafe Rust)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你是否把 Rust `unsafe` 误解成“关掉所有检查，接下来靠信仰”？
- 你是否想知道 Go 的 `unsafe.Pointer` 和 Rust `unsafe` 到底像在哪里、又不像在哪里？
- 你是否分不清 `unsafe fn`、`unsafe {}`、裸指针、`UnsafeCell`、`extern "C"` 各自负责什么契约？
- 你是否总听人说 UB、ABI、FFI，却很难把这些词和具体代码风险对上？
- 你是否担心把 nightly、edition 差异和“只是概念示意”写混？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| unsafe | — | 不安全 | 允许做编译器无法静态保证安全的操作 | `unsafe` 包，部分近似 |
| UB | Undefined Behavior | 未定义行为 | 一旦触发，编译器不保证任何后果 | Go 中少得多 |
| raw pointer | — | 裸指针 | `*const T` / `*mut T`，不带借用与生命周期保证 | `unsafe.Pointer` |
| ABI | Application Binary Interface | 二进制调用约定 | 规定函数调用和数据布局如何在二进制层交互 | ABI |
| FFI | Foreign Function Interface | 外部函数接口 | 不同语言之间互调的边界 | cgo / syscall 边界 |
| `UnsafeCell` | — | 内部可变性原语 | 允许在共享引用后面安全封装可变状态的底层工具 | 无直接对应 |
| `transmute` | — | 位级重解释 | 把一种位模式直接当另一种类型看 | `unsafe.Pointer` 强转，部分近似 |
| `repr(C)` | — | C 布局表示 | 尽量按 C 兼容布局安排类型 | C 结构体布局兼容 |
| soundness | — | 健全性 | 安全 API 不应让用户触发 UB | 无直接对应 |
| `Pin` | — | 固定地址 | 禁止被安全移动的约束 | Go 无直接对应 |
| `MaybeUninit` | — | 可能未初始化 | 表示这块内存可能尚未初始化，避免假定已 init | 无直接对应 |
| `CString` / `CStr` | — | C 字符串（拥有 / 借用） | 与 C 的 `char*` 互操作时常用的 NUL 结尾字符串类型 | cgo 里的 C 字符串，部分近似 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q8](#q8), [Q10](#q10), [Q13](#q13) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q14](#q14), [Q15](#q15), [Q16](#q16), [Q17](#q17), [Q18](#q18) |
| `occasional` | [Q11](#q11) |
| `advanced` | [Q12](#q12) |

---

## Q1. `unsafe` 关键字到底打开了什么，不会打开什么？ {#q1}
**Tags:** `hot` `unsafe`
**适用版本:** Rust 1.0+

**一句话答案：**

`unsafe` 只允许你做少数几类编译器无法自动证明安全的操作，比如解引用裸指针、调用 `unsafe fn`；它**不会**关掉所有权、借用、生命周期这些安全 Rust 规则。

**解答：**

最小例子：

```rust
fn main() {
    let x = 5;
    let p = &x as *const i32;
    let y = unsafe { *p };
    assert_eq!(y, 5);
}
```

但借用检查并不会失效：

```rust
fn main() {
    let mut v = vec![1];
    let first = &v[0];
    // v.push(2);
    // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    let _ = first;
}
```

```rust
fn main() {
    let x = 1u32;
    let p = &x as *const u32;
    assert_eq!(unsafe { *p }, 1);
}
```

**Go 对比：**

```go
package main

import "unsafe"

func main() {
	x := 5
	p := unsafe.Pointer(&x)
	_ = p
}
```

- **Go 怎么做**：`unsafe` 包提供部分越权能力，但很多普通代码仍由 GC/runtime 保底。
- **Rust 为什么不同**：Rust 只是把“这几步我人工担保”单独圈出来，周围安全规则依然存在。
- **Go 程序员易踩的坑**：把 Rust `unsafe` 当成“完全自由模式”；其实只是把证明责任转给你。

**记忆点：**

- `unsafe` 不是全局关闸。
- 它只是允许某几类危险操作。

---

## Q2. `unsafe fn` 和 `unsafe {}` 有什么区别？ {#q2}
**Tags:** `hot` `unsafe-fn`
**适用版本:** Rust 1.0+；Edition 2024 语义更严格

**一句话答案：**

`unsafe fn` 表示“调用这个函数有额外前置条件”；`unsafe {}` 表示“这里正在执行危险操作”。前者声明调用契约，后者圈定危险代码块。

**解答：**

调用方要显式承诺：

```rust
unsafe fn read_ptr(p: *const i32) -> i32 {
    unsafe { *p }
}
```

调用时必须写 `unsafe`：

```rust
unsafe fn read_ptr(p: *const i32) -> i32 {
    unsafe { *p }
}

fn main() {
    let x = 5;
    let p = &x as *const i32;
    let y = unsafe { read_ptr(p) };
    assert_eq!(y, 5);
}
```

```rust
unsafe fn read_ptr(p: *const i32) -> i32 {
    unsafe { *p }
}

fn main() {
    let x = 7;
    let y = unsafe { read_ptr(&x) };
    assert_eq!(y, 7);
}
```

**Go 对比：**

```go
package main

import "unsafe"

func main() {
	x := 5
	_ = unsafe.Pointer(&x)
}
```

- **Go 怎么做**：Go 没有“函数本身是 unsafe 调用契约”的语法层区分。
- **Rust 为什么不同**：Rust 想把“危险发生在哪”和“谁要负责满足前置条件”分开记录。
- **Go 程序员易踩的坑**：只在函数体里看 `unsafe`，忽略了 `unsafe fn` 的文档契约才是更关键的部分。

**记忆点：**

- `unsafe fn` 说“怎么调我”。
- `unsafe {}` 说“哪几行危险”。

---

## Q3. 裸指针 `*const T` / `*mut T` 和引用有什么本质差别？ {#q3}
**Tags:** `hot` `raw-pointer`
**适用版本:** Rust 1.0+

**一句话答案：**

引用 `&T` / `&mut T` 自带“非空、对齐、有效、遵守借用规则”的承诺；裸指针没有这些保证，解引用时全靠你自己证明。

**解答：**

从引用转裸指针本身是安全的：

```rust
fn main() {
    let mut x = 10;
    let pc: *const i32 = &x;
    let pm: *mut i32 = &mut x;
    let _ = (pc, pm);
}
```

真正危险的是解引用：

```rust
fn main() {
    let x = 10;
    let p = &x as *const i32;
    let y = unsafe { *p };
    assert_eq!(y, 10);
}
```

```rust
fn main() {
    let mut x = 10;
    let p = &mut x as *mut i32;
    unsafe {
        *p = 11;
    }
    assert_eq!(x, 11);
}
```

**Go 对比：**

```go
package main

import "unsafe"

func main() {
	x := 10
	p := unsafe.Pointer(&x)
	_ = p
}
```

- **Go 怎么做**：`unsafe.Pointer` 也能绕开类型系统，但周围仍有 GC 和运行时语义。
- **Rust 为什么不同**：Rust 把“借用保证”与“裸地址”分得非常清楚。
- **Go 程序员易踩的坑**：把引用强转到裸指针后，就误以为借用规则失效；其实一旦重新解引用，UB 风险依旧存在。

**记忆点：**

- 裸指针是地址，不是借用。
- 真正危险点是解引用。

---

## Q4. UB 到底是什么，为什么比 panic 更可怕？ {#q4}
**Tags:** `hot` `ub`
**适用版本:** Rust 1.0+

**一句话答案：**

UB（**Undefined Behavior**，未定义行为）不是“会报错”或“会 panic”，而是“编译器从这一刻起可以做任何假设”；程序可能崩、可能静默错、也可能今天对明天错。

**解答：**

越界访问是常见 UB 来源之一：

```rust
fn main() {
    let v = [1, 2, 3];
    let p = v.as_ptr();
    // let _ = unsafe { *p.add(10) };
}
```

```rust
fn main() {
    let v = [1, 2, 3];
    assert_eq!(v[1], 2);
}
```

而普通 `panic!` 不是 UB：

```rust
fn main() {
    panic!("this is defined behavior");
}
```

**Go 对比：**

```go
package main

func main() {
	panic("boom")
}
```

- **Go 怎么做**：大多数越界、nil、类型错都会走已定义的 panic 路径。
- **Rust 为什么不同**：一旦进入 `unsafe` 违约区，编译器优化会假设“不可能发生坏事”，于是后果不再可预测。
- **Go 程序员易踩的坑**：把 UB 理解成“更严重的 panic”；它比 panic 更糟，因为后果不受语言定义约束。

**记忆点：**

- panic 是定义好的失败。
- UB 是失去语言保障。

---

## Q5. `UnsafeCell` 为什么是内部可变性的底层原语？ {#q5}
**Tags:** `common` `unsafecell`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 Rust 默认会假设共享引用 `&T` 指向的内容不会被偷偷改；`UnsafeCell<T>` 是标准库唯一允许你合法打破这条优化假设、再自己封装安全抽象的原语。

**解答：**

它的存在形状：

```rust
use std::cell::UnsafeCell;

struct MyCell<T> {
    inner: UnsafeCell<T>,
}
```

最小读写示意：

```rust
use std::cell::UnsafeCell;

fn main() {
    let c = UnsafeCell::new(1);
    unsafe {
        *c.get() = 2;
    }
    assert_eq!(unsafe { *c.get() }, 2);
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：Go 不会把“共享引用后面绝不偷偷改”做成同等级别的优化契约暴露给用户。
- **Rust 为什么不同**：Rust 的内部可变性必须通过一条明确受控的底层通道进入。
- **Go 程序员易踩的坑**：以为只要转成 `*mut T` 就能安全改共享借用背后的值；那正是 `UnsafeCell` 要避免的野路子。

**记忆点：**

- 内部可变性的根在 `UnsafeCell`。

---

## Q6. `transmute` 为什么名声这么差？ {#q6}
**Tags:** `common` `transmute`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 `transmute` 是“按位把一种类型直接当成另一种类型看”，几乎不帮你检查语义正确性；大小相同不代表就安全。

**解答：**

危险形状：

```rust
fn main() {
    // let b: bool = unsafe { std::mem::transmute(2u8) };
}
```

很多场景都有更安全替代：

```rust
fn main() {
    let bits = 1.0f32.to_bits();
    let v = f32::from_bits(bits);
    assert_eq!(v, 1.0);
}
```

**Go 对比：**

```go
package main

import "unsafe"

func main() {
	_ = unsafe.Sizeof(1)
}
```

- **Go 怎么做**：Go 的 `unsafe.Pointer` 强转也类似“越过静态语义”。
- **Rust 为什么不同**：Rust 更鼓励你先找专门 API，如 `from_bits`、`from_ne_bytes`，别上来就 `transmute`。
- **Go 程序员易踩的坑**：觉得“只要大小一样就行”；很多类型还有值域、对齐、生命周期等隐藏不变量。

**记忆点：**

- 能不用 `transmute` 就不用。

---

## Q7. `extern "C"`、ABI、FFI 三者怎么串起来理解？ {#q7}
**Tags:** `common` `ffi` `abi`
**适用版本:** Rust 1.0+

**一句话答案：**

FFI（**Foreign Function Interface**）是跨语言互调这件事；ABI（**Application Binary Interface**）是二进制层调用约定；`extern "C"` 是在 Rust 里说“这段函数调用按 C ABI 来”。

**解答：**

声明外部函数：

```rust
unsafe extern "C" {
    fn abs(input: i32) -> i32;
}
```

调用时：

```rust
fn main() {
    unsafe extern "C" {
        fn abs(input: i32) -> i32;
    }

    let n = unsafe { abs(-3) };
    assert_eq!(n, 3);
}
```

**Go 对比：**

```go
package main

// cgo 才是 Go 常见的跨语言互调入口
func main() {}
```

- **Go 怎么做**：常见跨 C 代码用 cgo。
- **Rust 为什么不同**：Rust 直接把 ABI 约定暴露在函数签名里。
- **Go 程序员易踩的坑**：只关心类型像不像，忽略 ABI 和所有权边界谁负责释放。

**记忆点：**

- FFI 是跨语言互调。
- ABI 是二进制约定。
- `extern "C"` 是 Rust 里说“按 C 规矩来”。

---

## Q8. `unsafe.Pointer` 和 Rust `unsafe` 最重要的差别是什么？ {#q8}
**Tags:** `hot` `go-compare`
**适用版本:** Rust 1.0+

**一句话答案：**

Go 的 `unsafe.Pointer` 更像一个局部越权工具，周围仍有 GC/runtime 帮你兜一部分；Rust 的 `unsafe` 则直接接入整个内存模型与优化契约，一旦违约就可能触发真正的 UB。

**解答：**

Rust：

```rust
fn main() {
    let x = 1u32;
    let p = &x as *const u32;
    let _ = unsafe { *p };
}
```

```rust
fn main() {
    let x = 1u32;
    let p = &x as *const u32;
    let addr = p as usize;
    assert!(addr > 0);
}
```

```rust
fn main() {
    let bytes = [1u8, 0, 0, 0];
    let ptr = bytes.as_ptr();
    assert_eq!(unsafe { *ptr }, 1);
}
```

Go：

```go
package main

import "unsafe"

func main() {
	x := uint32(1)
	p := unsafe.Pointer(&x)
	_ = p
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：`unsafe.Pointer` 主要绕类型系统，但 GC、栈扩容、写屏障等仍在运行时模型内工作。
- **Rust 为什么不同**：Rust 没有 GC 兜底，`unsafe` 直接碰到别名、生命周期、对齐、初始化等底层不变量。
- **Go 程序员易踩的坑**：用 Go 的直觉低估 Rust `unsafe` 的后果范围。

**记忆点：**

- Rust `unsafe` 的证明责任更重。

---

## Q9. 为什么 `repr(C)` 对 FFI 很重要？ {#q9}
**Tags:** `common` `repr-c`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 Rust 默认不承诺结构体字段布局；跨 C 边界传结构体时，通常要写 `#[repr(C)]`，告诉编译器按 C 兼容布局安排。

**解答：**

形状：

```rust
#[repr(C)]
struct Point {
    x: f64,
    y: f64,
}
```

如果不写，就别把它当 C 结构体直接共享：

```rust
fn main() {
    #[repr(C)]
    struct Point {
        x: f64,
        y: f64,
    }

    assert_eq!(std::mem::size_of::<Point>(), 16);
}
```

**Go 对比：**

```go
package main

type Point struct {
	X float64
	Y float64
}

func main() {}
```

- **Go 怎么做**：很多时候布局问题被 cgo 或运行时层封住了。
- **Rust 为什么不同**：Rust 更明确要求你在类型层表达布局意图。
- **Go 程序员易踩的坑**：以为“字段顺序看起来一样”就够了。

**记忆点：**

- FFI 里布局要显式，不要靠猜。

---

## Q10. soundness 是什么？为什么 unsafe 抽象一定要写不变量？ {#q10}
**Tags:** `hot` `soundness`
**适用版本:** Rust 1.0+

**一句话答案：**

soundness（健全性）指的是：你写出来的安全 API，不能让调用者仅靠安全 Rust 就触发 UB；因此每个 unsafe 抽象都必须有清楚的不变量和局部证明。

**解答：**

unsafe 抽象常见形状：

```rust
pub struct MyVec<T> {
    ptr: *mut T,
    len: usize,
    cap: usize,
}
```

你至少要能说清类似不变量：

```rust
fn main() {
    // 例如：len <= cap；ptr 指向一块能容纳 cap 个 T 的分配；
    // 0..len 内元素已初始化。
}
```

```rust
fn main() {
    let len = 3usize;
    let cap = 8usize;
    assert!(len <= cap);
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：Go 普通用户很少需要自己证明这类内存不变量。
- **Rust 为什么不同**：Rust 允许你造零成本安全抽象，但前提是你把危险藏好、把契约写清。
- **Go 程序员易踩的坑**：以为“代码跑过了”就算安全；unsafe 抽象的关键是长期可证明。

**记忆点：**

- unsafe 不是“能跑就行”。
- 安全抽象必须靠不变量站住。

---

## Q11. Miri 是什么？它和 nightly / stable 的关系要怎么说？ {#q11}
**Tags:** `occasional` `miri`
**适用版本:** 运行工具常依赖 nightly；Rust 1.97.1 下写业务代码仍可在 stable

**一句话答案：**

Miri 是 Rust 的解释执行工具，能帮你抓很多 UB 线索；它常通过 nightly 工具链运行，但这不代表你的业务代码本身必须写成 nightly。

**解答：**

Miri 是工具，不是语言特性。业务代码可以继续写 stable；用 nightly 工具链跑 Miri 检查即可。完整步骤：

```bash
rustup toolchain install nightly
rustup +nightly component add miri
cargo +nightly miri setup
cargo +nightly miri test
cargo +nightly miri run
```

含义分别是：安装 nightly、装 Miri 组件、初始化 Miri 依赖、用 Miri 跑测试、用 Miri 跑二进制。Windows 上若 shell 不认 `+nightly`，可写成 `cargo +nightly miri test` 前先确认 `rustup which --toolchain nightly rustc` 可用。

它常用于检查 unsafe 代码。下面这个测试在普通 `cargo test` 下可能“看起来没事”，但越界解引用属于 UB；用 `cargo +nightly miri test` 更容易把它抓出来：

```rust
#[test]
fn demo_ok_under_miri() {
    let v = vec![1, 2, 3];
    let p = v.as_ptr();
    let x = unsafe { *p };
    assert_eq!(x, 1);
}
```

```rust
#[test]
fn demo_ub_miri_should_catch() {
    let v = [1, 2, 3];
    let p = v.as_ptr();
    // 下面这行是故意越界：普通编译可能“碰巧能跑”，Miri 会报 UB
    // let _ = unsafe { *p.add(10) };
    let _ = p;
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：Go 更常见的是 `go test -race`、`vet` 等工具。
- **Rust 为什么不同**：Miri 专门盯的是 Rust 内存模型和 UB 相关问题。
- **Go 程序员易踩的坑**：把“用 nightly 跑工具”误解成“代码特性本身是 nightly”。

**记忆点：**

- Miri 是工具，不等于语言特性稳定级别。
- 安装：`rustup +nightly component add miri`；检查：`cargo +nightly miri test`。

---

## Q12. 这篇里哪些点必须明确标 stable / nightly / 概念示意？ {#q12}
**Tags:** `advanced` `stability`
**适用版本:** Rust 1.97.1

**一句话答案：**

`unsafe`、裸指针、`UnsafeCell`、`repr(C)`、FFI 主线都是 stable；Miri 常通过 nightly 跑；更底层的某些实现细节可当概念示意讲，但不能说成“生产默认写法”。

**解答：**

stable 主线：

```rust
fn main() {
    let x = 1;
    let p = &x as *const i32;
    let _ = unsafe { *p };
}
```

需要额外说明的边界：

```rust
fn main() {
    // - stable: unsafe 块、裸指针、FFI、UnsafeCell
    // - nightly tool usage: Miri 常用 +nightly
    // - 概念示意: 某些手写 poll / pin / 底层优化讨论
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：unsafe 区域较少、主线更收敛。
- **Rust 为什么不同**：Rust unsafe 话题直接连接类型系统、内存模型和 FFI，所以更需要精确标注边界。
- **Go 程序员易踩的坑**：把“能这样讲概念”误解成“就该这样写生产代码”。

**记忆点：**

- 讲 unsafe 时，稳定性和适用边界要写得比别的主题更明确。

---

## Q13. 什么情况下绝不该先写 `unsafe`？ {#q13}
**Tags:** `hot` `unsafe` `design`
**适用版本:** Rust 1.0+

**一句话答案：**

只要安全 Rust 或现有安全抽象就能表达，就绝不先写 `unsafe`：例如“绕过借用检查图省事”、未先读文档就 `transmute`、把性能猜测当成必须 unsafe 的理由。

**解答：**

先走安全路：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let (a, b) = v.split_at_mut(1); // 安全 API，不必手写裸指针
    a[0] = 9;
    b[0] = 8;
    assert_eq!(v, vec![9, 8, 3]);
}
```

这些信号出现时，停手：

```rust
fn main() {
    // 红灯：
    // - “编译器太烦，我先 unsafe 让它闭嘴”
    // - “我只是想把 &T 改成 &mut T”
    // - “大小一样，transmute 一下”
    // - 还说不清不变量，就开始解引用裸指针
}
```

正确顺序通常是：安全 API → 改设计（索引/拆借/Cell/锁）→ 实在需要再做**最小** unsafe，并写成有边界的安全封装（见 [Q10](#q10)、[Q15](#q15)）。

```rust
fn main() {
    let x = 1;
    let y = x; // 安全复制；别为此上裸指针
    assert_eq!(y, 1);
}
```

**Go 对比：**

```go
package main

func main() {
	// Go 里也不该一上来就 unsafe.Pointer；先用切片、拷贝、标准库
}
```

- **Go 怎么做**：`unsafe` 包同样是最后手段。
- **Rust 为什么不同**：违约成本是 UB，不只是“可能 panic”。
- **Go 程序员易踩的坑**：把借用错误当成“该用 unsafe 砸开”的提示。

**记忆点：**

- unsafe 是最后一公里，不是快捷键。
- 先问：标准库有没有安全写法？

---

## Q14. `MaybeUninit` 在解决什么问题？ {#q14}
**Tags:** `common` `maybeuninit`
**适用版本:** Rust 1.36+（`MaybeUninit` 稳定常用）

**一句话答案：**

**`MaybeUninit<T>`**（可能未初始化）用来表示“这块内存里可能还没有合法的 `T`”，避免把未初始化内存当成已初始化值读；常用于分步初始化数组、FFI 缓冲、性能敏感的延迟 init。

**解答：**

直接读未初始化是 UB；正确形状是先占位再写入：

```rust
use std::mem::MaybeUninit;

fn main() {
    let mut slot: MaybeUninit<i32> = MaybeUninit::uninit();
    slot.write(42);
    let v = unsafe { slot.assume_init() };
    assert_eq!(v, 42);
}
```

数组分步填充的常见模式：

```rust
use std::mem::MaybeUninit;

fn first_three() -> [i32; 3] {
    let mut buf = MaybeUninit::<[i32; 3]>::uninit();
    let p = buf.as_mut_ptr() as *mut i32;
    unsafe {
        for i in 0..3 {
            p.add(i).write(i as i32);
        }
        // SAFETY: 0..3 都已 write
        buf.assume_init()
    }
}

fn main() {
    assert_eq!(first_three(), [0, 1, 2]);
}
```

注意：`assume_init` / 把 `MaybeUninit` 当已初始化读，仍然是 unsafe 契约；它解决的是“类型层承认未初始化”，不是自动让你变安全。

**Go 对比：**

```go
package main

func main() {
	var buf [3]int // Go 会零值初始化；很少暴露“未初始化槽位”抽象
	_ = buf
}
```

- **Go 怎么做**：变量通常有零值，未初始化问题较少暴露给用户。
- **Rust 为什么不同**：Rust 默认禁止“看起来像 T、其实还没 init”。
- **Go 程序员易踩的坑**：以为 `MaybeUninit` 等于“随便读”；真正危险点仍在 `assume_init`。

**记忆点：**

- `MaybeUninit` = 合法表达“尚未 init”。
- 读之前必须证明已经写过。

---

## Q15. 给 unsafe 抽象写安全 API 的最小检查清单？ {#q15}
**Tags:** `common` `soundness` `api`
**适用版本:** Rust 1.0+

**一句话答案：**

先写清不变量，再把 `unsafe` 缩到模块内部，对外只暴露不会让用户轻松触发 UB 的安全 API；并用测试/Miri 守住边界。

**解答：**

最小清单：

1. **不变量**：用文字写清“什么时刻内存有效、别名如何、len/cap 关系”
2. **边界**：`unsafe` 块尽量小；`unsafe fn` 只留给真正有前置条件的入口
3. **安全封装**：公共方法是安全的，用户走安全路径完不成违约
4. **文档**：写 `# Safety`（对 `unsafe fn`）和模块级安全承诺
5. **检验**：单测 + 条件允许时用 Miri（见 [Q11](#q11)）

```rust
pub struct LockedFlag {
    // 不变量示例：value 只通过本类型方法读写
    value: bool,
}

impl LockedFlag {
    pub fn new(v: bool) -> Self {
        Self { value: v }
    }

    pub fn get(&self) -> bool {
        self.value
    }
}

fn main() {
    assert!(LockedFlag::new(true).get());
}
```

反面对照：

```rust
fn main() {
    // 坏清单：
    // - 公共 API 直接返回 *mut T 让用户自己保证
    // - 不变量只活在作者脑子里
    // - “先合并，以后再证明”
}
```

和 [Q10](#q10) 的关系：soundness 是目标；本清单是落地动作。

**Go 对比：**

```go
package main

func main() {
	// Go 封装更多靠“别导出字段 + 文档约定”；
	// Rust 还要求：安全用户不应仅靠安全代码触发 UB
}
```

- **Go 怎么做**：可见性与文档是主边界。
- **Rust 为什么不同**：安全抽象还要对接内存模型与优化假设。
- **Go 程序员易踩的坑**：以为“字段不导出”就等于 sound；若安全方法内部契约不成立，仍可能 UB。

**记忆点：**

- 不变量 → 最小 unsafe → 安全 API → 文档 → 检验。
- 让违约变得困难，而不是“靠用户自觉”。

---

## Q16. 从裸指针恢复引用前，必须守住哪些不变量？ {#q16}
**Tags:** `common` `raw-pointer` `reference` `UB`
**适用版本:** Rust 1.0+

**一句话答案：** 写成 `&T` / `&mut T` 前，你必须证明指针非空、对齐正确、指向已初始化的有效 `T`、借用规则成立（尤其 `&mut` 独占），且指向的对象在整个引用生命周期内都活着——任一破环都可能是 **UB**（未定义行为）。

**解答：** [Q3](#q3) 区分了裸指针和引用；本题给“恢复引用”检查清单（与 [Q10](#q10)、[Q15](#q15) 的不变量同一思路）：

1. **非空**：不能从空指针造引用（`null` 不是有效 `&T`）。
2. **对齐**：地址满足 `T` 的对齐要求。
3. **有效且已初始化**：指向真正的 `T` 对象，读之前已按类型规则初始化（未 init 见 [Q14](#q14)）。
4. **别名 / 借用规则**：已有 `&mut` 时不能再造别的引用去读写同一路径；多个 `&` 可共存但不能靠它们改内部（除非 `UnsafeCell`）。
5. **生命周期**：引用的 `'a` 期间，被指对象不能被释放、移走或复用这块内存。

合法的短例子：指针来自仍活着的对象，并立刻在同一作用域用完引用：

```rust
fn main() {
    let mut x = 10;
    let p: *mut i32 = &mut x;
    // SAFETY: p 来自有效 &mut x；此时无其它别名；x 仍存活
    let r: &mut i32 = unsafe { &mut *p };
    *r += 1;
    assert_eq!(x, 11);
}
```

「❌ 危险方向」——悬垂或空指针硬转引用（不要在生产里这样写）：

```rust
fn main() {
    let p: *const i32 = std::ptr::null();
    // let _r: &i32 = unsafe { &*p }; // UB：空指针不是有效引用
    assert!(p.is_null());
}
```

若你的目标是拼 `Vec`/`String` 一类容器：除上述外还要核对指针来源分配器、`len`/`cap` 关系、元素初始化与丢弃责任——那是更长的容器清单；本题先守住“引用”这一关。

**Go 对比：**

```go
package main

import "unsafe"

func main() {
	x := 10
	p := unsafe.Pointer(&x)
	_ = (*int)(p)
}
```

- **Go 怎么做**：`unsafe.Pointer` 转回 `*T` 也有规则，但周围有 GC，生命周期压力不同。
- **Rust 为什么不同**：引用会进入借用检查与优化假设，违约更易变成全程 UB。
- **Go 程序员易踩的坑**：觉得“地址非空就行”，忽略对齐、初始化和别名。

**记忆点：**

- 恢复引用：非空、对齐、已 init、别名合法、对象仍存活。
- 不确定就别造引用——先保持裸指针或走安全 API。

---

## Q17. `CString` / `CStr` 和 `#[no_mangle] pub extern "C"` 怎么对标 cgo 导出？ {#q17}
**Tags:** `common` `FFI` `CString` `no_mangle`
**适用版本:** Rust 1.0+

**一句话答案：**

对 C 导出函数用 `#[no_mangle] pub extern "C" fn ...`（按 C **ABI** 暴露符号）；字符串边界上，拥有权侧常用 `CString`（NUL 结尾、可交出 `*const c_char`），借用侧用 `CStr`。这和 cgo 导出/`C.CString` 同一类问题，但所有权与 `unsafe` 边界更显式（总览见 [Q7](#q7)）。

**解答：**

先把两个字符串角色分开：

- **`CString`**：拥有一块 NUL 结尾缓冲；适合“Rust 分配，交给 C 读一段时间，再由 Rust 负责释放（或按约定移交）”。
- **`CStr`**：不拥有，只是对已有 `*const c_char` 的借用视图；适合“C 传来的只读 C 字符串”。

可编译的字符串边界最小例子：

```rust
use std::ffi::{CStr, CString};

fn main() {
    let owned = CString::new("hello").expect("interior NUL");
    let ptr = owned.as_ptr(); // *const c_char，在 owned 活着期间有效

    // SAFETY: ptr 来自仍存活的 CString，且指向合法 NUL 结尾串
    let borrowed = unsafe { CStr::from_ptr(ptr) };
    assert_eq!(borrowed.to_bytes(), b"hello");
}
```

同一进程内可编译的最小导出形状（真实跨语言通常还要 `cdylib`/`staticlib`；完整工程注意见下方 text）：

```rust
#[no_mangle]
pub extern "C" fn add_c(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    // 在 Rust 侧也能当普通函数调用；对 C 暴露时关键符号名还要靠 no_mangle
    assert_eq!(add_c(1, 2), 3);
}
```

导出给 C 的工程形态（对标 cgo 的 `//export`）。下面用 **text**：crate-type、链接与 panic 边界要按项目配置，不要把“能写出来”当成“已经安全”。

```text
// Cargo.toml 概念：
// [lib]
// crate-type = ["cdylib"]
//
// use std::os::raw::{c_char, c_int};
//
// #[no_mangle]
// pub extern "C" fn add(a: c_int, b: c_int) -> c_int {
//     a + b
// }
//
// // 字符串参数常见模式（示意）：
// // #[no_mangle]
// // pub unsafe extern "C" fn use_name(name: *const c_char) { ... CStr::from_ptr ... }
```

清单（口语版）：

1. **`extern "C"`**：调用约定跟 C 走（见 [Q7](#q7)）。
2. **`#[no_mangle]`**：别让 Rust 把符号名搅乱，方便 C/`dlsym` 找到。
3. **字符串**：Rust → C 用 `CString`（注意内部不能有 `\0`）；C → Rust 用 `CStr`，并证明指针非空、生命周期覆盖整个使用期。
4. **panic**：不要让 panic 穿过 FFI 边界；边界函数里要接住或保证不 panic。
5. **布局**：结构体跨语言时再配 `repr(C)`（见 [Q9](#q9)）。

**Go 对比：**

```go
package main

/*
#include <stdint.h>
*/
import "C"

//export Add
func Add(a, b C.int) C.int { return a + b }

func main() {}
```

- **Go 怎么做**：cgo `//export` + `C.CString` / `C.GoString`。
- **Rust 为什么不同**：导出属性与 ABI 写在签名上；字符串用 `CString`/`CStr`，生命周期/释放责任必须说清。
- **Go 程序员易踩的坑**：把 `as_ptr()` 存出去却 drop 了 `CString`；或默认 Rust 字符串布局能直接当 `char*`。

**记忆点：**

- 导出：`#[no_mangle] pub extern "C"`。
- 字符串：`CString` 拥有，`CStr` 借用。
- FFI 边界默认 `unsafe` 契约，panic 别穿出去。

---

## Q18. 用 `cc` + `bindgen` 链一个最小 C 函数要几步？ {#q18}
**Tags:** `common` `FFI` `cc` `bindgen` `build.rs`
**适用版本:** `cc` / `bindgen` 生态；配合 [Q7](#q7)、[Q17](#q17)

**一句话答案：**
典型流水线：**C 源码 → `cc` 在 `build.rs` 里编成静态库 → `bindgen` 从头文件生成 Rust 声明 → `extern "C"` 调用**。另记两条边界铁律：回调也要 `extern "C"`；**panic 不得穿过 FFI**（见 [Q17](#q17)）。

**解答：**
最小步骤清单（text，工程级示意）：

```text
1. 放 C 代码，例如 c_src/add.c：
   int add(int a, int b) { return a + b; }

2. 放头文件 c_src/add.h：
   int add(int a, int b);

3. Cargo.toml：
   [build-dependencies]
   cc = "1"
   bindgen = "0.69"   # 版本随项目锁定

4. build.rs：
   // cc::Build::new().file("c_src/add.c").compile("add");
   // bindgen::Builder::default()
   //   .header("c_src/add.h")
   //   .generate()
   //   .expect("bindgen")
   //   .write_to_file(out_dir.join("bindings.rs"))
   //   .unwrap();

5. src/lib.rs 或 main.rs：
   // include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
   // unsafe { add(1, 2) }
```

同进程内可先体会导出侧形状（不依赖 C 工具链）：

```rust
#[no_mangle]
pub extern "C" fn rust_add(a: i32, b: i32) -> i32 {
    // FFI 边界：不要 panic；需要时 catch_unwind 并转成错误码
    a + b
}

fn main() {
    assert_eq!(rust_add(1, 2), 3);
}
```

```rust
fn main() {
    // 签名示意：bindgen 会生成类似 `extern "C" { fn add(...) -> ...; }`
    // 真正调用前必须由 cc 链上 C 实现，再写：unsafe { add(1, 2) }
    type AddFn = unsafe extern "C" fn(i32, i32) -> i32;
    assert_eq!(std::mem::size_of::<AddFn>(), std::mem::size_of::<usize>());
}
```

回调 / panic 边界（口语版）：

1. C 调 Rust 函数指针：Rust 侧必须是 `extern "C" fn(...)`，且约定空指针、生命周期。
2. Rust 调 C 回调：把回调当 `unsafe` 契约，假设它遵守 ABI。
3. **panic 穿过 FFI = 未定义行为倾向**：边界用 `catch_unwind` 转错误码，或保证内部不 panic。

**Go 对比：**

```go
package main

/*
int add(int a, int b) { return a + b; }
*/
import "C"
import "fmt"

func main() {
	fmt.Println(C.add(1, 2))
}
```

- **Go 怎么做**：cgo 把注释里的 C 和 `import "C"` 焊在一起。
- **Rust 为什么不同**：显式 `build.rs` + `cc` +（可选）`bindgen`，步骤更长但可控。
- **Go 程序员易踩的坑**：以为 `extern "C"` 写完就自动编译 `.c`；其实还要 `cc` 链接。

**记忆点：**
- `cc` 编译 C；`bindgen` 生成声明；`unsafe` 调用。
- 回调 + panic：守住 FFI 边界。

---
