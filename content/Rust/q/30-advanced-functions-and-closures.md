+++
title = "30-高级函数与闭包"
date = 2026-07-28T14:49:00+08:00
weight = 300
type = "docs"
description = "面向 Go 初学 Rust 的高级函数与闭包入门，讲透 Fn 家族、返回闭包和回调设计"
isCJKLanguage = true
draft = false

+++

# 高级函数与闭包 (Advanced Functions and Closures)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你是否总分不清 `Fn`、`FnMut`、`FnOnce`，只知道“编译器又不让我传这个闭包”？
- 你是否想知道：Go 把函数当值传来传去很自然，为什么 Rust 这里突然要谈所有权和捕获方式？
- 你是否遇到过 `error[E0525]`、`error[E0373]`、`error[E0308]`，却看不懂闭包到底哪里“不够格”？
- 你是否想写“返回一个回调”的 API，却被匿名闭包类型、`impl Fn`、`Box<dyn Fn>` 搞晕？
- 你是否看到 HRTB、`for<'a>` 这类写法就头皮发麻，想先知道它到底在解决什么真实问题？
- 你是否想确认：哪些闭包、异步闭包、`Fn` trait 自定义实现是 stable，哪些仍是 nightly？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| closure | — | 闭包 | 带环境捕获的匿名函数值 | 闭包 |
| capture | — | 捕获 | 闭包把外部变量带进自己内部的方式 | 闭包捕获 |
| `FnOnce` | — | 调用一次 trait | 闭包可在调用时消耗捕获值，因此最多安全调用一次 | 无精确对应 |
| `FnMut` | — | 可变调用 trait | 闭包调用时可修改自己捕获的状态 | 带状态闭包 |
| `Fn` | — | 只读调用 trait | 闭包调用时只读捕获环境，可重复调用 | 纯读闭包 |
| function item | — | 函数项类型 | 每个 `fn foo` 都有自己的零大小具体类型 | 函数符号 |
| function pointer | — | 函数指针 | `fn(i32) -> i32` 这种只保存代码地址的类型 | 函数值 |
| HRTB | Higher-Ranked Trait Bound | 高阶 trait 约束 | `for<'a>` 这种“对任意生命周期都成立”的约束 | 无直接对应 |
| monomorphization | — | 单态化 | 泛型在编译期按具体类型展开成多份代码 | Go 泛型实例化，概念接近 |
| dynamic dispatch | — | 动态分发 | 通过 trait object 的虚表在运行时决定调哪个实现 | interface 调用 |
| trait object | — | trait 对象 | `dyn Trait`，保存数据指针和虚表指针 | interface 值 |
| `impl Trait` | — | 不透明返回类型 | 隐藏具体类型但仍走静态分发 | 无直接对应 |
| HOF | Higher-Order Function | 高阶函数 | 接收函数/闭包或返回函数/闭包的函数 | 高阶函数 |
| async closure | — | 异步闭包 | `async |x| ...`，真正的异步闭包（实现 `AsyncFn*`） | 返回 channel / future 的闭包 |
| `AsyncFn` / `AsyncFnMut` / `AsyncFnOnce` | — | 异步调用 trait 族 | 接受真正异步闭包时优先用的 bound（1.85+） | 无直接对应 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q8](#q8), [Q10](#q10), [Q13](#q13) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q14](#q14), [Q15](#q15), [Q16](#q16) |
| `occasional` | [Q11](#q11) |
| `advanced` | [Q12](#q12) |

---

## Q1. `Fn`、`FnMut`、`FnOnce` 到底怎么区分？ {#q1}
**Tags:** `hot` `closure` `fn-traits`
**适用版本:** Rust 1.0+

**一句话答案：**

看闭包体“怎么用捕获值”就行：只读是 `Fn`，会改状态是 `FnMut`，会把捕获值拿走就是 `FnOnce`；三者不是你手写选的，而是编译器推出来的。

**解答：**

这三个 trait 可以先理解成“回调最少需要什么权限”：

- **`Fn`**：只读调用，`call` 时只借用 `&self`。
- **`FnMut`**：可变调用，`call` 时借用 `&mut self`，允许改内部状态。
- **`FnOnce`**：一次性调用，`call` 时拿走 `self`，允许把捕获值移出闭包。

```rust
fn call_fn<F: Fn()>(f: F) {
    f();
    f();
}

fn call_fn_mut<F: FnMut()>(mut f: F) {
    f();
    f();
}

fn call_fn_once<F: FnOnce()>(f: F) {
    f();
}

fn main() {
    let name = String::from("rust");
    call_fn(|| println!("{name}")); // 只读捕获 -> Fn

    let mut n = 0;
    call_fn_mut(|| n += 1); // 修改捕获 -> FnMut

    let s = String::from("gone");
    call_fn_once(|| drop(s)); // 移出捕获 -> FnOnce
}
```

它们的包含关系是：`Fn` 也能当 `FnMut` 用，`FnMut` 也能当 `FnOnce` 用。反过来不行。

```rust
fn need_fn<F: Fn()>(f: F) {
    f();
}

fn main() {
    let mut count = 0;
    let bump = || count += 1;
    // need_fn(bump);
    // error[E0525]: expected a closure that implements the `Fn` trait,
    // but this closure only implements `FnMut`
    let _ = bump;
}
```

给 API 选约束时，用“能完成需求的最弱约束”：

```rust
fn run_twice<F: FnMut()>(mut f: F) {
    f();
    f();
}

fn main() {
    run_twice(|| println!("hello"));
}
```

**Go 对比：**

```go
package main

import "fmt"

func runTwice(f func()) {
	f()
	f()
}

func main() {
	n := 0
	runTwice(func() {
		n++
		fmt.Println(n)
	})
}
```

- **Go 怎么做**：Go 只有 `func()` 这一层签名，不区分“只读捕获”和“修改捕获”。
- **Rust 为什么不同**：Rust 要在编译期证明别名、可变性和所有权，所以把“调用时需要的权限”编码进 trait。
- **Go 程序员易踩的坑**：你在 Go 里写得通的带状态闭包，到了 Rust 可能要把参数类型从 `Fn` 放宽成 `FnMut` 才能传进去。

**记忆点：**

- 先看闭包体，再谈 `Fn*`。
- API 设计时尽量选最弱约束。
- `Fn`/`FnMut`/`FnOnce` 的差别，本质是“调用时拿 `self` 的方式不同”。

---

## Q2. `move` 闭包到底改变了什么？ {#q2}
**Tags:** `hot` `move` `ownership`
**适用版本:** Rust 1.0+

**一句话答案：**

`move` 只改变**捕获方式**，把外部变量按值搬进闭包；它不自动等于 `FnOnce`，闭包最终实现哪个 `Fn*` trait，仍要看闭包体有没有把捕获值消费掉。

**解答：**

不写 `move` 时，编译器会尽量按借用捕获；写了 `move`，编译器会优先把值带进闭包内部。

```rust
fn main() {
    let s = String::from("hi");
    let print = || println!("{s}");
    print();
    println!("{s}"); // 仍可用，因为只是借用捕获
}
```

`move` 最常见的场景是：闭包可能活得比外部变量更久，比如线程、任务、回调注册。

```rust
use std::thread;

fn main() {
    let data = vec![1, 2, 3];

    let handle = thread::spawn(move || {
        println!("{}", data.len());
    });

    handle.join().unwrap();
}
```

不加 `move` 时，会报经典生命周期错误：

```rust
use std::thread;

fn main() {
    let data = vec![1, 2, 3];
    // let handle = thread::spawn(|| println!("{}", data.len()));
    // error[E0373]: closure may outlive the current function, but it borrows `data`
    let _ = data;
}
```

注意：`move` 不等于“只能调用一次”。如果搬进去的是 `String`，但你只是读它长度，闭包依旧可能是 `Fn`。

```rust
fn need_fn<F: Fn()>(f: F) {
    f();
    f();
}

fn main() {
    let s = String::from("rust");
    let show_len = move || println!("{}", s.len());
    need_fn(show_len); // 可以，因为没有把 s 移出闭包体
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	data := []int{1, 2, 3}
	var wg sync.WaitGroup
	wg.Add(1)
	go func(v []int) {
		defer wg.Done()
		fmt.Println(len(v))
	}(data)
	wg.Wait()
}
```

- **Go 怎么做**：通常把变量作为参数传给 goroutine 闭包，达到“按值带进去”的效果。
- **Rust 为什么不同**：Rust 把这个动作明确写成 `move`，让所有权转移在语法层面可见。
- **Go 程序员易踩的坑**：别把 `move` 理解成“深拷贝”；它多数时候只是转移所有权，不一定复制底层数据。

**记忆点：**

- `move` 说的是怎么捕获，不是怎么调用。
- 线程、异步任务、长生命周期回调常常必须 `move`。
- `move` 后原变量可能失效，但闭包不一定降级成 `FnOnce`。

---

## Q3. 为什么“返回一个闭包”会这么别扭？ {#q3}
**Tags:** `hot` `return-closure` `impl-trait`
**适用版本:** Rust 1.26+（返回位置 `impl Trait` 稳定）

**一句话答案：**

因为每个闭包都有自己不可名的具体类型；返回时要么用 `impl Fn(...)` 隐藏它，要么用 `Box<dyn Fn(...)>` 做动态分发。

**解答：**

最简单的情况，用返回位置 `impl Trait`。

```rust
fn make_adder(x: i32) -> impl Fn(i32) -> i32 {
    move |y| x + y
}

fn main() {
    let add5 = make_adder(5);
    assert_eq!(add5(3), 8);
}
```

如果多个分支返回的是**不同闭包类型**，`impl Fn` 就不够了，因为 `if` 两边必须是同一个具体类型。

```rust
fn main() {
    let factor = 2;
    // let _choose = if true { |x| x + 1 } else { move |x| x * factor };
    // error[E0308]: `if` and `else` have incompatible types
}
```

这时就改用 trait object：

```rust
fn choose(flag: bool) -> Box<dyn Fn(i32) -> i32> {
    if flag {
        Box::new(|x| x + 1)
    } else {
        Box::new(|x| x * 2)
    }
}

fn main() {
    assert_eq!(choose(true)(3), 4);
    assert_eq!(choose(false)(3), 6);
}
```

若闭包借用了局部变量，也要记得 `move`，否则会返回悬垂借用：

```rust
fn build_len() -> impl Fn() -> usize {
    let s = String::from("abc");
    move || s.len()
}

fn main() {
    assert_eq!(build_len()(), 3);
}
```

**Go 对比：**

```go
package main

import "fmt"

func makeAdder(x int) func(int) int {
	return func(y int) int {
		return x + y
	}
}

func main() {
	fmt.Println(makeAdder(5)(3))
}
```

- **Go 怎么做**：直接返回 `func(int) int`，不需要区分静态分发还是动态分发。
- **Rust 为什么不同**：Rust 想尽量保留零成本抽象，所以先让你选 `impl Fn`，只有真需要异质返回时才付出 `Box<dyn Fn>` 的动态分发成本。
- **Go 程序员易踩的坑**：在 Rust 里“能返回闭包”不代表“任何分支的闭包都能混着返回”。

**记忆点：**

- 单一闭包类型用 `impl Fn`。
- 多种闭包类型混合返回用 `Box<dyn Fn>`。
- 只要返回的闭包带走了局部数据，通常就要 `move`。

---

## Q4. `fn` 指针和闭包到底差在哪？ {#q4}
**Tags:** `hot` `fn-pointer` `closure`
**适用版本:** Rust 1.0+

**一句话答案：**

`fn(i32) -> i32` 只是代码地址；闭包是“代码 + 捕获环境”的匿名结构体。无捕获闭包能自动退化成 `fn` 指针，有捕获闭包不行。

**解答：**

先看能转的情况：

```rust
fn add_one(x: i32) -> i32 {
    x + 1
}

fn main() {
    let f: fn(i32) -> i32 = add_one;
    let g: fn(i32) -> i32 = |x| x + 1; // 无捕获闭包可退化为 fn 指针
    assert_eq!(f(3), 4);
    assert_eq!(g(3), 4);
}
```

一旦闭包捕获了环境，它就不再只是代码地址。

```rust
fn main() {
    let offset = 10;
    // let f: fn(i32) -> i32 = |x| x + offset;
    // error[E0308]: mismatched types
    // note: closures can only be coerced to `fn` types if they do not capture any variables
    let _ = offset;
}
```

反过来，普通函数可以很自然地传给接收 `Fn` 的 API：

```rust
fn double(x: i32) -> i32 {
    x * 2
}

fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 {
    f(x)
}

fn main() {
    assert_eq!(apply(double, 3), 6);
}
```

**Go 对比：**

```go
package main

import "fmt"

func addOne(x int) int { return x + 1 }

func apply(f func(int) int, x int) int {
	return f(x)
}

func main() {
	offset := 10
	fmt.Println(apply(addOne, 3))
	fmt.Println(apply(func(x int) int { return x + offset }, 3))
}
```

- **Go 怎么做**：函数和闭包统一都看成 `func(...) ...`。
- **Rust 为什么不同**：Rust 区分“有没有环境数据”，这样无捕获情况能继续零开销。
- **Go 程序员易踩的坑**：Rust 的 `fn` 不等于“任意可调用东西”，它只是一类很窄的可调用值。

**记忆点：**

- 无捕获闭包可转 `fn`。
- 有捕获闭包必须走 `Fn*` 泛型或 `dyn Fn*`。
- API 若想同时接收函数和闭包，优先写 `impl Fn...`。

---

## Q5. 什么时候该用 `Box<dyn Fn>`？ {#q5}
**Tags:** `common` `dyn` `callback`
**适用版本:** Rust 1.0+

**一句话答案：**

当你要把“不同具体类型的回调”放进同一个容器、结构体字段或返回值里时，用 `Box<dyn Fn>`；如果只是参数传递，优先用泛型 `impl Fn`。

**解答：**

异质集合是最典型场景：

```rust
fn main() {
    let callbacks: Vec<Box<dyn Fn(i32) -> i32>> = vec![Box::new(|x| x + 1), Box::new(|x| x * 2)];

    assert_eq!(callbacks[0](3), 4);
    assert_eq!(callbacks[1](3), 6);
}
```

但如果只是普通参数，泛型更简单也更快：

```rust
fn run<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 {
    f(x)
}

fn main() {
    assert_eq!(run(|x| x + 1, 3), 4);
}
```

**Go 对比：**

```go
package main

func main() {
	callbacks := []func(int) int{
		func(x int) int { return x + 1 },
		func(x int) int { return x * 2 },
	}
	_, _ = callbacks[0](3), callbacks[1](3)
}
```

- **Go 怎么做**：直接把不同闭包放进 `[]func(...) ...`。
- **Rust 为什么不同**：不同闭包类型默认不同，必须通过 `dyn Fn` 做类型擦除。
- **Go 程序员易踩的坑**：不要为了“看起来统一”就到处 `Box<dyn Fn>`；很多时候泛型更自然。

**记忆点：**

- 容器/字段里装异质回调，用 `dyn Fn`。
- 参数位置优先 `impl Fn`。
- `dyn Fn` 的代价是堆分配和动态分发。

---

## Q6. 为什么 `Iterator::map` 用的是 `FnMut`？ {#q6}
**Tags:** `common` `iterator` `fnmut`
**适用版本:** Rust 1.0+

**一句话答案：**

因为映射闭包很常见地会带状态，比如计数、累加、缓存；`FnMut` 既覆盖纯函数，也覆盖带可变内部状态的闭包。

**解答：**

无状态当然可以：

```rust
fn main() {
    let out: Vec<_> = [1, 2, 3].into_iter().map(|x| x * 2).collect();
    assert_eq!(out, vec![2, 4, 6]);
}
```

但 `FnMut` 还能支持“每次调用都改点东西”的闭包：

```rust
fn main() {
    let mut i = 0;
    let out: Vec<_> = [10, 20]
        .into_iter()
        .map(|x| {
            i += 1;
            x + i
        })
        .collect();
    assert_eq!(out, vec![11, 22]);
}
```

**Go 对比：**

```go
package main

func main() {
	i := 0
	nums := []int{10, 20}
	out := make([]int, 0, len(nums))
	for _, x := range nums {
		i++
		out = append(out, x+i)
	}
	_ = out
}
```

- **Go 怎么做**：通常直接写 `for range`，状态变量顺手放外面。
- **Rust 为什么不同**：迭代器 API 把这类状态回调显式纳入 trait 约束。
- **Go 程序员易踩的坑**：以为 `map` 应该只接“纯函数”，其实 Rust 标准库故意留了状态空间。

**记忆点：**

- `FnMut` 是迭代器适配器里最常见的约束。
- 它比 `Fn` 更宽松，又比 `FnOnce` 更适合重复调用。

---

## Q7. 闭包的捕获规则是怎么决定的？ {#q7}
**Tags:** `common` `capture`
**适用版本:** Rust 1.0+

**一句话答案：**

不写 `move` 时，编译器会按“最小需要权限”捕获：能不可变借用就不多拿，能可变借用就不 move，只有必须移出时才捕获所有权。

**解答：**

先是只读借用：

```rust
fn main() {
    let s = String::from("hello");
    let show = || println!("{s}");
    show();
    println!("{s}");
}
```

再是可变借用：

```rust
fn main() {
    let mut v = vec![1];
    let mut push = || v.push(2);
    push();
    drop(push);
    assert_eq!(v, vec![1, 2]);
}
```

**Go 对比：**

```go
package main

func main() {
	v := []int{1}
	push := func() {
		v = append(v, 2)
	}
	push()
	_ = v
}
```

- **Go 怎么做**：闭包捕获规则较少暴露在类型层面。
- **Rust 为什么不同**：借用方式会直接影响后续能不能再借、能不能跨线程、能不能返回。
- **Go 程序员易踩的坑**：Rust 里“闭包还活着”这件事本身就可能占着借用。

**记忆点：**

- 编译器默认按最小权限捕获。
- `move` 是显式改写这个默认策略。

---

## Q8. `async |x| ...` 异步闭包现在是 stable 吗？和 `|x| async move { ... }` 有什么差别？ {#q8}
**Tags:** `hot` `async` `closure`
**适用版本:** `async`/`await` 自 Rust 1.39+；`async` 闭包与 `AsyncFn*` bound 自 Rust 1.85+ stable（1.97.1 可用）

**一句话答案：**

`async |x| ...` 在 1.85+ stable，是**真正的异步闭包**；接受它时 bound 应优先理解成 `AsyncFn` / `AsyncFnMut` / `AsyncFnOnce`。`|x| async move { ... }` 只是普通闭包返回一个 Future，bound 才是 `F: Fn(...) -> Fut`。俩长相像，别当成完整等价。

**解答：**

先把两句话钉死：

1. `async |x| ...` → 异步闭包 → 实现 `AsyncFn*`（1.85+）。
2. `|x| async move { ... }` → 普通 `Fn*` 闭包，调用后给你一个 Future → bound 用 `Fn(...) -> Fut`。

真正异步闭包 + 匹配的 bound（可编译示意，不依赖 Tokio；需 edition 2021+）：

```rust
fn takes_async_closure<F>(_f: F)
where
    F: AsyncFn(i32) -> i32,
{
}

fn main() {
    // 真正的异步闭包（1.85+）
    takes_async_closure(async |x: i32| x + 1);
}
```

老写法：普通闭包返回 Future（更老工具链也能写）：

```rust
fn takes_closure_returning_fut<F, Fut>(_f: F)
where
    F: Fn(i32) -> Fut,
    Fut: std::future::Future<Output = i32>,
{
}

fn main() {
    takes_closure_returning_fut(|x: i32| async move { x + 1 });
}
```

两种写法可以并存，但别混 bound：

```rust
fn main() {
    let _async_closure = async |x: i32| x + 1; // → AsyncFn*
    let _returns_fut = |x: i32| async move { x + 1 }; // → Fn -> Fut
}
```

口语对照：

| 写法 | 它是什么 | 接受它时常见 bound |
|------|----------|-------------------|
| `async \|x\| ...` | 真正异步闭包 | **`AsyncFn*`**（优先） |
| `\|x\| async move { ... }` | 普通闭包，返回 Future | `Fn(...) -> Fut` |

别用 `F: Fn(i32) -> Fut` 假装“完整覆盖了异步闭包”：异步闭包在借用捕获、多次调用、future 生命周期等方面和“返回一个独立 Future 的普通闭包”并不总是同一套故事；库作者 API 面对 `async |...|` 时应优先看 `AsyncFn*`。反过来，你若只收 `Fn -> Fut`，调用方用 `|x| async move { ... }` 通常就对上了。

要真正跑起来还得有 executor（Tokio / `block_on` 等）。下面只用 text 示意，避免把 `#[tokio::main]` 塞进可编译 `rust` 块误导：

```text
// 概念示意（需 runtime，勿当裸 rustc 片段）：
// let f = async |x: i32| x + 1;
// assert_eq!(f(3).await, 4);
//
// let g = |x: i32| async move { x + 1 };
// assert_eq!(g(3).await, 4);
```

稳定性边界（口语版）：

- **stable（1.85+）**：写 `async |...| ...`；用 `AsyncFn*` 作 bound。
- **仍常见**：`|x| async move { ... }` + `Fn -> Fut`（兼容旧代码、很多教程还在写）。
- **别混**：手搓实现 `AsyncFn*` 的底层细节、个别实验 API——那不是“写异步闭包”的日常门槛；日常就是语法 + bound。

**Go 对比：**

```go
package main

import "fmt"

func makeAdder() func(int) int {
	return func(x int) int {
		return x + 1
	}
}

func main() {
	fmt.Println(makeAdder()(3))
}
```

- **Go 怎么做**：Go 没有语言级 future，也没有异步闭包；通常直接开 goroutine，或返回一个会阻塞的函数。
- **Rust 为什么不同**：Rust 的 async 是 future 状态机；“闭包返回 future”与“异步闭包（`AsyncFn*`）”是两层相近但不同的类型故事。
- **Go 程序员易踩的坑**：别把 `async` 想成“自动并发”；也别把两种闭包写法当成同一种 bound。

**记忆点：**

- `async |x| ...` = 真异步闭包 → 想 `AsyncFn*`。
- `|x| async move { ... }` = 普通闭包返回 Future → 想 `Fn -> Fut`。
- `async` 不等于 goroutine，只是造 future。

---

## Q9. 闭包什么时候实现 `Copy` / `Clone`？ {#q9}
**Tags:** `common` `copy` `clone`
**适用版本:** Rust 1.0+

**一句话答案：**

看它捕获了什么：无捕获或只捕获 `Copy` 值时，闭包常常也 `Copy`；捕获 `String` 这类只 `Clone` 不 `Copy` 的值时，闭包通常只能 `Clone`。

**解答：**

无捕获闭包最简单：

```rust
fn main() {
    let f = |x: i32| x + 1;
    let g = f; // Copy
    assert_eq!(f(3), 4);
    assert_eq!(g(3), 4);
}
```

按值捕获 `String` 就不同了：

```rust
fn main() {
    let s = String::from("hi");
    let f = move || s.len();
    let g = f.clone();
    assert_eq!(f(), 2);
    assert_eq!(g(), 2);
}
```

**Go 对比：**

```go
package main

func main() {
	s := "hi"
	f := func() int { return len(s) }
	g := f
	_, _ = f(), g()
}
```

- **Go 怎么做**：函数值可以直接赋给另一个变量使用。
- **Rust 为什么不同**：闭包是具体结构体，复制能力由“内部字段”决定。
- **Go 程序员易踩的坑**：别默认以为“闭包值都能随便复制”；在 Rust 里它也是普通值。

**记忆点：**

- 把闭包当匿名结构体看，很多问题就通了。
- 闭包是否 `Copy` / `Clone`，由捕获字段决定。

---

## Q10. 为什么“我只是把这个闭包传进去”也会报 move 或借用错误？ {#q10}
**Tags:** `hot` `errors` `ownership`
**适用版本:** Rust 1.0+

**一句话答案：**

因为把闭包传给函数，本质上也是把一个值传进去；如果参数是 `FnOnce`，调用方可能就把这个闭包整体消费掉了，而闭包内部又可能持有别的值或借用。

**解答：**

`FnOnce` 参数会吃掉闭包：

```rust
fn consume<F: FnOnce()>(f: F) {
    f();
}

fn main() {
    let s = String::from("hello");
    let f = move || println!("{s}");
    consume(f);
}
```

如果你还想再用同一个闭包，就会报错：

```rust
fn consume<F: FnOnce()>(f: F) {
    f();
}

fn main() {
    let s = String::from("hello");
    let f = move || println!("{s}");
    consume(f);
    // consume(f);
    // error[E0382]: use of moved value: `f`
}
```

还有一类高频坑：闭包借用了外部变量，于是外部变量在闭包活着期间不能按冲突方式再借。

```rust
fn main() {
    let mut v = vec![1];
    let mut push = || v.push(2);
    // let first = &v[0];
    // error[E0502]: cannot borrow `v` as immutable because it is also borrowed as mutable
    push();
}
```

**Go 对比：**

```go
package main

func consume(f func()) {
	f()
}

func main() {
	s := "hello"
	f := func() { _ = s }
	consume(f)
	consume(f)
}
```

- **Go 怎么做**：函数值传参不暴露“消费一次还是多次”的类型差异。
- **Rust 为什么不同**：Rust 把“这个回调是否会被吃掉”也编码进类型系统，提前防止悬垂和重复消费。
- **Go 程序员易踩的坑**：不要把闭包当成“永远可复制、永远可重用”的轻量引用。

**记忆点：**

- 传闭包也是传值。
- `FnOnce` 最宽松，但也最容易“吃掉”调用方的闭包。
- 借用错误很多时候不是变量本身有问题，而是闭包仍持有它。

---

## Q11. Rust 能做柯里化吗？stable 和 nightly 的边界在哪？ {#q11}
**Tags:** `occasional` `currying`
**适用版本:** Rust 1.0+；某些更花哨的 `impl Trait` in `Fn` return 仍是 nightly

**一句话答案：**

能，但日常只建议做一层或两层的“部分应用”；更深层的“返回闭包再返回闭包”在 stable 上可以写，只是签名会很难看，某些更优雅的写法仍是 nightly。

**解答：**

稳定版最实用的是一层：

```rust
fn add(a: i32) -> impl Fn(i32) -> i32 {
    move |b| a + b
}

fn main() {
    assert_eq!(add(1)(2), 3);
}
```

更深层也能写，但常常要装箱：

```rust
fn add3(a: i32) -> impl Fn(i32) -> Box<dyn Fn(i32) -> i32> {
    move |b| Box::new(move |c| a + b + c)
}

fn main() {
    assert_eq!(add3(1)(2)(3), 6);
}
```

**Go 对比：**

```go
package main

func add(a int) func(int) int {
	return func(b int) int { return a + b }
}

func main() {
	_ = add(1)(2)
}
```

- **Go 怎么做**：直接嵌套返回 `func` 即可。
- **Rust 为什么不同**：Rust 优先保留具体类型和零开销，所以深层嵌套会很快暴露类型命名问题。
- **Go 程序员易踩的坑**：在 Rust 里为了“函数式优雅”过度柯里化，往往不如直接写结构体或普通函数清晰。

**记忆点：**

- stable 能写柯里化，但不一定值得。
- 工程里更常见的是部分应用，而不是深层函数式链条。

---

## Q12. `for<'a>` 这种 HRTB 到底在说什么人话？ {#q12}
**Tags:** `advanced` `hrtb` `lifetime`
**适用版本:** Rust 1.0+

**一句话答案：**

HRTB（**Higher-Ranked Trait Bound**，高阶 trait 约束）里的 `for<'a>`，意思是“这个回调对任意生命周期 `'a` 都得成立”，不是“挑一个刚好能用的生命周期”。

**解答：**

看一个最小例子：

```rust
fn call_any<F>(f: F)
where
    F: for<'a> Fn(&'a str) -> &'a str,
{
    let s = String::from("hello");
    assert_eq!(f(&s), "hello");
}

fn main() {
    call_any(|s| s);
}
```

如果没有 `for<'a>`，很多“输入借多久，输出也借多久”的签名就表达不清。

```rust
fn main() {
    // 这类问题的核心不是语法炫技，而是：
    // “我需要一个对任何输入借用长度都成立的函数”
}
```

**Go 对比：**

```go
package main

func echo(s string) string { return s }

func main() {
	_ = echo("hello")
}
```

- **Go 怎么做**：Go 没有显式生命周期参数，字符串和切片的借用关系不会被这样写进类型。
- **Rust 为什么不同**：Rust 需要把借用活多久也纳入类型契约，HRTB 就是表达“对所有生命周期都成立”的工具。
- **Go 程序员易踩的坑**：把 `for<'a>` 误解成“泛型语法糖”；它真正约束的是借用关系，不是普通类型参数。

**记忆点：**

- HRTB 的关键词是“任意生命周期都成立”。
- 看到 `for<'a>`，先把它翻译成人话，再看签名。

---

## Q13. 给库写回调时收 `Fn` 还是 `FnMut`/`FnOnce`？ {#q13}
**Tags:** `hot` `api` `fn-traits`
**适用版本:** Rust 1.0+

**一句话答案：**

选**能完成需求的最弱约束**：只调用一次用 `FnOnce`；要多次调用且可能改状态用 `FnMut`；明确只要只读、可重入再用 `Fn`。收太紧会把合法闭包拒之门外。

**解答：**

库 API 的默认经验：

```rust
// 最常见：只调用一次的回调（类似 “交给你就结束”）
fn with_setup<F: FnOnce()>(f: F) {
    f();
}

// 要循环/多次触发：FnMut
fn for_each<F: FnMut(i32)>(mut f: F) {
    for i in 0..3 {
        f(i);
    }
}

fn main() {
    with_setup(|| println!("once"));
    let mut sum = 0;
    for_each(|x| sum += x);
    assert_eq!(sum, 3);
}
```

太紧会把带状态闭包挡掉：

```rust
fn need_fn<F: Fn()>(f: F) {
    f();
}

fn main() {
    let mut n = 0;
    let bump = || n += 1;
    // need_fn(bump);
    // error[E0525]: expected a closure that implements the `Fn` trait,
    // but this closure only implements `FnMut`
    let _ = bump;
}
```

经验口诀：

- 事件处理器、迭代器适配器参数 → 常 `FnMut`
- `thread::spawn` / 一次性完成回调 → `FnOnce`
- 真正无状态、可并发重入 → 再升级到 `Fn`（必要时再加 `Send + Sync`）

**Go 对比：**

```go
package main

func withSetup(f func()) { f() }

func main() {
	n := 0
	withSetup(func() { n++ })
}
```

- **Go 怎么做**：只有 `func(...)`，不区分调用权限。
- **Rust 为什么不同**：要把“会不会改捕获、会不会吃掉闭包”编码进 API。
- **Go 程序员易踩的坑**：库一上来就写 `Fn`，结果用户带计数器的闭包传不进去。

**记忆点：**

- API 约束从弱到强：`FnOnce` → `FnMut` → `Fn`。
- 先问“我调用几次、要不要改状态”，再选 trait。

---

## Q14. 闭包借了 `self` 后为啥不能再调方法？ {#q14}
**Tags:** `common` `borrow` `closure`
**适用版本:** Rust 1.0+

**一句话答案：**

因为闭包一旦捕获了 `&self` / `&mut self`（或字段借用），这段借用会活到闭包结束；同一期间再调需要再借 `self` 的方法，就会和现有借用冲突。

**解答：**

典型冲突：

```rust
struct Counter {
    n: i32,
}

impl Counter {
    fn bump(&mut self) {
        self.n += 1;
    }

    fn demo(&mut self) {
        let mut add = || self.n += 1;
        // self.bump();
        // error[E0499]: cannot borrow `*self` as mutable more than once at a time
        add();
    }
}

fn main() {
    let mut c = Counter { n: 0 };
    c.demo();
    assert_eq!(c.n, 1);
}
```

修法：先算完闭包需要的数据，或缩短闭包作用域，或别让闭包抓住整个 `self`：

```rust
struct Counter {
    n: i32,
}

impl Counter {
    fn demo(&mut self) {
        {
            let mut add = || self.n += 1;
            add();
        } // 借用在这里结束
        self.n += 1; // 现在可以再借
    }
}

fn main() {
    let mut c = Counter { n: 0 };
    c.demo();
    assert_eq!(c.n, 2);
}
```

**Go 对比：**

```go
package main

type Counter struct{ N int }

func (c *Counter) Demo() {
	add := func() { c.N++ }
	add()
	c.N++ // Go 允许，靠程序员自己保证别竞态
}

func main() {
	c := &Counter{}
	c.Demo()
}
```

- **Go 怎么做**：方法接收者被闭包捕获很常见，冲突靠约定/竞态检测。
- **Rust 为什么不同**：借用检查把“闭包还活着”也算进别名冲突。
- **Go 程序员易踩的坑**：以为“我又没多线程，为啥不能再调方法”；问题是别名，不是线程。

**记忆点：**

- 闭包捕获 `self` = 占着借用。
- 先结束闭包，或只捕获需要的字段副本/局部。

---

## Q15. 返回 `impl Fn` 和 `Box<dyn Fn>` 怎么选？把闭包存进结构体为什么难？ {#q15}
**Tags:** `common` `impl-trait` `dyn`
**适用版本:** Rust 1.26+（返回位置 `impl Trait`）

**一句话答案：**

单一具体闭包类型、调用方不需要异质存储 → 优先 `impl Fn`；要放进字段/容器、或多个分支返回不同闭包 → `Box<dyn Fn...>`。难，是因为每个闭包类型匿名且不同，结构体字段必须写成可命名、可统一的类型。

**解答：**

返回单一闭包：

```rust
fn make_adder(x: i32) -> impl Fn(i32) -> i32 {
    move |y| x + y
}

fn main() {
    assert_eq!(make_adder(2)(3), 5);
}
```

结构体字段不能直接写“某个匿名闭包类型”，通常要类型擦除或泛型：

```rust
struct Hook {
    on_tick: Box<dyn FnMut() -> i32>,
}

fn main() {
    let mut n = 0;
    let mut h = Hook {
        on_tick: Box::new(move || {
            n += 1;
            n
        }),
    };
    assert_eq!((h.on_tick)(), 1);
    assert_eq!((h.on_tick)(), 2);
}
```

也可以把闭包类型做成结构体泛型参数 `struct Hook<F: FnMut()> { on_tick: F }`，零成本但类型会“传染”到所有使用方。

和 [Q3](#q3)、[Q5](#q5) 的关系：那两题讲返回/容器；本题补的是“存进自己的类型”时为何必须二选一。

**Go 对比：**

```go
package main

type Hook struct {
	OnTick func()
}

func main() {
	n := 0
	h := Hook{OnTick: func() { n++ }}
	h.OnTick()
}
```

- **Go 怎么做**：`func()` 本身就是统一的函数值类型。
- **Rust 为什么不同**：默认保留具体闭包类型以换取内联；要统一就必须显式 `dyn` 或泛型。
- **Go 程序员易踩的坑**：以为结构体字段写个闭包像 Go 一样自然；Rust 里要先决定静态还是动态。

**记忆点：**

- 能静态、同质 → `impl Fn` / 泛型字段。
- 要异质、可存可换 → `Box<dyn Fn*>`。

---

## Q16. `FnOnce` 调用后为啥不能再用？带借用的闭包塞进字段又卡在哪？ {#q16}
**Tags:** `common` `FnOnce` `lifetime` `struct`
**适用版本:** Rust 1.0+

**一句话答案：** `FnOnce` 调用会按值吃掉闭包（常因把捕获值移出），所以不能二次调用；把“借了局部数据的闭包”放进结构体字段时，字段的生命周期必须盖住那次借用，短命借用塞不进长命字段。

**解答：** 先看一次性消费。闭包体若把捕获的 `String` 等移出，它只实现 `FnOnce`；调用一次后闭包已被 move，再调就是 E0382（和 [Q1](#q1)、[Q10](#q10) 同一条线）：

```rust
fn main() {
    let s = String::from("hi");
    let once = || s; // 移出捕获 -> FnOnce
    assert_eq!(once(), "hi");
    // once();
    // error[E0382]: use of moved value: `once`
}
```

```rust
fn take_once<F: FnOnce() -> i32>(f: F) -> i32 {
    f()
}

fn main() {
    let f = || 1;
    assert_eq!(take_once(f), 1);
    // take_once(f); // f 已 move 进上次调用
}
```

再看字段生命周期。 [Q15](#q15) 说字段常要 `Box<dyn Fn*>`；若闭包还借用外部局部变量，类型会带上那段借用的生命周期。结构体若要活得更久（存到全局、返回给调用方），编译器会拒绝“短借用装进长字段”：

```rust
struct Hook {
    on_tick: Box<dyn Fn() -> usize>,
}

fn main() {
    let n = 3usize;
    let h = Hook {
        // move 把 n 搬进闭包，满足 dyn Fn 默认的 'static
        on_tick: Box::new(move || n),
    };
    assert_eq!((h.on_tick)(), 3);
}
```

若写成 `Box::new(|| n)` 只借用局部 `n`，`Box<dyn Fn() -> usize>` 默认还要求捕获满足 `'static`，就会生命周期报错。短借用要能进字段，得给 trait 对象加上生命周期（如 `Box<dyn Fn() -> usize + '_>`）并保证结构体不活过借用；更常见仍是 `move` 拥有数据，或字段改存 `String`/`Arc`。

**Go 对比：**

```go
package main

func main() {
	s := "hi"
	f := func() string { return s }
	_ = f()
	_ = f() // 可反复调用；捕获的是变量，不是“移走”
}
```

- **Go 怎么做**：函数值可反复调用；捕获不区分 FnOnce/Fn。
- **Rust 为什么不同**：要在类型里区分“调用是否消耗自身”和“借用能活多久”。
- **Go 程序员易踩的坑**：以为闭包字段像 Go 的 `func()` 字段一样随便塞局部变量；Rust 还要过生命周期关。

**记忆点：**

- `FnOnce`：调用即消费闭包；要多次调用就别移出捕获（或改 `Fn`/`FnMut`）。
- 闭包进字段：先解决类型（`dyn`/泛型），再解决借用是否活得过字段。

---
