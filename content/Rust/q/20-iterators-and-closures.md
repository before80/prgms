+++
title = "20-iterators-and-closures"
date = 2026-07-28T14:49:00+08:00
weight = 200
type = "docs"
description = "讲清惰性迭代器、`collect()`、三种 iter、闭包捕获与 `Fn` 家族"
isCJKLanguage = true
draft = false

+++

# 迭代器与闭包 (Iterators and Closures)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会分不清 `iter` / `iter_mut` / `into_iter`，结果把容器吃掉或改不了元素？
- 你是否被 `Fn` / `FnMut` / `FnOnce`、`move` 闭包、`E0525` 搞到怀疑人生？
- 你会不会写了长长的 `map/filter` 却忘了 `collect`，以为已经执行？
- 你是否想知道：Go 的 `for range` / 闭包与 Rust 迭代器模型差在哪？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| iterator | — | 迭代器 | 惰性产出元素的对象，实现 `Iterator` | `for range` / `iter.Seq` |
| lazy | — | 惰性 | 适配器先组合、消费时才算 | 多数循环立即执行 |
| consumer | — | 消费器 | `collect`/`sum`/`for` 等真正拉动迭代的操作 | 循环体 |
| closure | — | 闭包 | 能捕获环境的匿名函数 | 函数字面量 |
| capture | — | 捕获 | 闭包使用外部变量的方式 | 闭包变量捕获 |
| `Fn` | — | 可反复不可变调用 | 闭包只不可变借用捕获 | 普通函数值近亲 |
| `FnMut` | — | 可反复可变调用 | 闭包会改捕获 | 改外部变量的闭包 |
| `FnOnce` | — | 最多调用一次 | 闭包会拿走捕获所有权 | 无直接对应 |
| `move` | — | 强制按值捕获 | 捕获时移交所有权进闭包 | 较少需要 |
| turbofish | `::<>` | 涡轮鱼 | 给函数/方法显式喂类型参数 | 少见 |
| `GC` | Garbage Collector | 垃圾回收器 | 运行时回收 | Go 默认机制 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q23](#q23), [Q25](#q25) |
| `common` | [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q21](#q21), [Q22](#q22), [Q24](#q24) |
| `occasional` | [Q16](#q16), [Q17](#q17), [Q18](#q18) |
| `advanced` | [Q19](#q19), [Q20](#q20) |

---

## Q1. 迭代器为什么说是惰性的？ {#q1}
**Tags:** `hot` `beginner` `iterator`
**适用版本:** Rust 1.0+；本篇不依赖 nightly

**一句话答案：**

`map`/`filter` 等适配器只是挂上加工步骤，不立刻算；直到 `collect`、`sum`、`for`、`count` 等消费器拉动时才执行。

**解答：**

Go 的 `for range` 立刻跑循环体。Rust 里 `v.iter().map(...).filter(...)` 本身几乎不做事——忘记 `collect` 会得到“什么也没发生”的错觉（有时还有 unused must_use 警告）。

```rust
fn main() {
    let it = (1..=5).map(|x| x * 2);
    let v: Vec<_> = it.collect();
    println!("{v:?}");
}
```

```rust
fn main() {
    let mut calls = 0;
    let v: Vec<_> = (1..=3)
        .map(|x| {
            calls += 1;
            x * 10
        })
        .collect();
    println!("{v:?} calls={calls}");
}
```

```rust
fn main() {
    let _lazy = (1..=1_000_000).map(|x| x * 2); // 尚未计算
    println!("not collected yet");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	out := []int{}
	for _, x := range []int{1, 2, 3} {
		out = append(out, x*2)
	}
	fmt.Println(out)
}
```

- **Go 怎么做**：循环立即执行。
- **Rust 为什么不同**：先描述流水线，再消费。
- **Go 程序员易踩的坑**：写完 `map` 就以为结果已经有了。

---

## Q2. `iter`、`iter_mut`、`into_iter` 三者到底差什么？ {#q2}
**Tags:** `hot` `beginner` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

`iter()` → 元素 `&T`，容器留下；`iter_mut()` → `&mut T`，可改元素；`into_iter()` → `T`，容器被消费。

**解答：**

这是本章最该背死的表。`for x in &v` / `for x in &mut v` / `for x in v` 分别对应三者。`IntoIterator` 对 `Vec` 的实现就是 `into_iter`。

```rust
fn main() {
    let v = vec![1, 2, 3];
    let sum: i32 = v.iter().sum();
    println!("{sum} len={}", v.len());
}
```

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    v.iter_mut().for_each(|x| *x += 1);
    println!("{v:?}");
}
```

```rust
fn main() {
    let v = vec![1, 2, 3];
    let owned: Vec<_> = v.into_iter().map(|x| x * 2).collect();
    println!("{owned:?}");
}
```

```rust
fn main() {
    let v = vec![1, 2, 3];
    let _s: i32 = v.into_iter().sum();
    println!("{}", v.len());
    // error[E0382]: borrow of moved value: `v`
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	for i := range v {
		v[i] *= 2
	}
	fmt.Println(v)
}
```

- **Go 怎么做**：`range` 下用索引改原切片。
- **Rust 为什么不同**：三种迭代把借用/消费写进类型。
- **Go 程序员易踩的坑**：`into_iter` 后还访问原 `Vec`。

---

## Q3. `collect()` 为什么总要你标注一下类型？ {#q3}
**Tags:** `hot` `beginner` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

同一个迭代器可以收成很多容器（`Vec`/`HashSet`/`String`…），编译器往往无法唯一定位目标类型，需要你标注或 turbofish。

**解答：**

常见写法：`let v: Vec<_> = iter.collect();` 或 `iter.collect::<Vec<_>>()`。`_` 让元素类型仍可推断。

```rust
fn main() {
    let v: Vec<i32> = (1..=3).collect();
    println!("{v:?}");
}
```

```rust
fn main() {
    let v = (1..=3).collect::<Vec<_>>();
    println!("{v:?}");
}
```

```rust
fn main() {
    let _v = (1..=3).collect();
    // error[E0283]: type annotations needed
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	out := make([]int, 0, 3)
	for i := 1; i <= 3; i++ {
		out = append(out, i)
	}
	fmt.Println(out)
}
```

- **Go 怎么做**：容器类型在 `make` 时已定。
- **Rust 为什么不同**：`collect` 是泛型目标。
- **Go 程序员易踩的坑**：看到 `E0283`/`E0282` 不知道加 `Vec<_>`。

---

## Q4. `map`、`filter`、`fold` 分别擅长什么？ {#q4}
**Tags:** `hot` `beginner` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

`map` 一对一变换；`filter` 按条件留下；`fold`（以及 `sum`/`product`）把序列收成一个累积值。

**解答：**

它们都是惰性适配器（`fold` 是立即消费的终端操作）。`filter_map`、`flat_map`、`try_fold` 是进阶组合。简单累积优先 `sum`。

```rust
fn main() {
    let v: Vec<_> = (1..=5).map(|x| x * x).collect();
    println!("{v:?}");
}
```

```rust
fn main() {
    let v: Vec<_> = (1..=8).filter(|x| x % 2 == 0).collect();
    println!("{v:?}");
}
```

```rust
fn main() {
    let s = (1..=5).fold(0, |acc, x| acc + x);
    println!("{s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	sum := 0
	for i := 1; i <= 5; i++ {
		sum += i
	}
	fmt.Println(sum)
}
```

- **Go 怎么做**：手写循环。
- **Rust 为什么不同**：用适配器表达意图。
- **Go 程序员易踩的坑**：把 `map` 当副作用循环（应优先 `for_each`/`for`）。

---

## Q5. 闭包为什么能访问外部变量？ {#q5}
**Tags:** `hot` `beginner` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

闭包会捕获环境：默认按需不可变借、可变借或 move；编译器根据你在闭包里怎么用外部变量来决定。

**解答：**

`|x| x + offset` 会捕获 `offset`。这和 Go 函数字面量类似，但 Rust 把捕获方式暴露到 `Fn` 家族（见 [Q6](#q6)）。

```rust
fn main() {
    let offset = 10;
    let add = |x| x + offset;
    println!("{}", add(3));
}
```

```rust
fn main() {
    let mut n = 0;
    let mut bump = || n += 1;
    bump();
    bump();
    println!("{n}");
}
```

```rust
fn main() {
    let name = String::from("Ada");
    let greet = || println!("hi {name}");
    greet();
    println!("{name}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	offset := 10
	add := func(x int) int { return x + offset }
	fmt.Println(add(3))
}
```

- **Go 怎么做**：闭包捕获变量（注意循环变量老坑）。
- **Rust 为什么不同**：捕获与调用次数约束进 trait。
- **Go 程序员易踩的坑**：以为捕获永远像引用，忽略 `move`/`FnOnce`。

---

## Q6. `Fn`、`FnMut`、`FnOnce` 应该怎么记？ {#q6}
**Tags:** `hot` `beginner` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

`FnOnce`：能调用至少一次（可能拿走捕获）；`FnMut`：可多次调用且可改捕获；`Fn`：可多次调用且只不可变用捕获。能力上 `Fn` ⊂ `FnMut` ⊂ `FnOnce`。

**解答：**

记法：看闭包体对捕获做了什么——只读 → 常实现 `Fn`；修改 → `FnMut`；把捕获 move 出去 → 只剩 `FnOnce`。API 若要求 `Fn`，你却改捕获，会报 `E0525`（见 [Q19](#q19)）。

```rust
fn call_fn<F: Fn(i32) -> i32>(f: F) {
    println!("{}", f(1));
    println!("{}", f(2));
}

fn main() {
    let add1 = |x| x + 1;
    call_fn(add1);
}
```

```rust
fn call_mut<F: FnMut()>(mut f: F) {
    f();
    f();
}

fn main() {
    let mut n = 0;
    call_mut(|| n += 1);
    println!("{n}");
}
```

```rust
fn call_once<F: FnOnce() -> String>(f: F) {
    println!("{}", f());
}

fn main() {
    let s = String::from("hi");
    call_once(|| s);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 0
	bump := func() { n++ }
	bump()
	bump()
	fmt.Println(n)
}
```

- **Go 怎么做**：一个函数值类型打天下。
- **Rust 为什么不同**：用三个 trait 编码“能调用几次、能否改捕获”。
- **Go 程序员易踩的坑**：把该 `FnMut` 的闭包传给只要 `Fn` 的 API。

---

## Q7. `move` 闭包到底改变了什么？ {#q7}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

`move || ...` 强制按值捕获：把捕获的所有权搬进闭包，常用于线程/`'static` 要求，或避免借用活得不够久。

**解答：**

写法：`thread::spawn(move || { ... })`。`Copy` 类型搬的是副本；`String` 搬的是所有权，外面不能再用。

```rust
fn main() {
    let s = String::from("hi");
    let f = move || println!("{s}");
    f();
}
```

```rust
fn main() {
    let s = String::from("hi");
    let f = move || println!("{s}");
    f();
    println!("{s}");
    // error[E0382]: borrow of moved value: `s`
}
```

```rust
fn main() {
    let n = 1;
    let f = move || n + 1; // i32 是 Copy，外面仍可用
    println!("{} {}", f(), n);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hi"
	f := func() { fmt.Println(s) }
	f()
	fmt.Println(s)
}
```

- **Go 怎么做**：捕获通常仍共享变量。
- **Rust 为什么不同**：`move` 明确移交/复制进闭包。
- **Go 程序员易踩的坑**：`move` 后还用原 `String`。

---

## Q8. 为什么 `Iterator::map` 接受 `FnMut`？ {#q8}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

`map` 会对每个元素调用闭包，可能多次；闭包也可能在多次调用间修改自己的捕获，所以界是 `FnMut`，而不是更严的 `Fn`。

**解答：**

只读闭包也实现 `FnMut`，所以 `|x| x+1` 没问题。若闭包是 `FnOnce` 且会吃掉捕获，就不能用于要多次调用的 `map`。

```rust
fn main() {
    let mut seen = 0;
    let v: Vec<_> = (1..=3)
        .map(|x| {
            seen += 1;
            x * 2
        })
        .collect();
    println!("{v:?} seen={seen}");
}
```

```rust
fn main() {
    let v: Vec<_> = (1..=3).map(|x| x + 1).collect();
    println!("{v:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	seen := 0
	out := []int{}
	for _, x := range []int{1, 2, 3} {
		seen++
		out = append(out, x*2)
	}
	fmt.Println(out, seen)
}
```

- **Go 怎么做**：循环里随便改外部变量。
- **Rust 为什么不同**：`FnMut` 允许闭包带可变状态。
- **Go 程序员易踩的坑**：把只能调用一次的 `FnOnce` 塞进 `map`。

---

## Q9. 什么时候闭包会变成 `FnOnce`？ {#q9}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

闭包体把捕获的值 move 出去（或调用只接受 `self` 的方法吃掉它）时，通常只实现 `FnOnce`。

**解答：**

典型：`|| s` 返回 `String`；`|| drop(s)`。这种闭包不能调用两次。需要多次时，改为借用、`clone`，或改 API。

```rust
fn main() {
    let s = String::from("hi");
    let f = || s;
    let owned = f();
    println!("{owned}");
}
```

```rust
fn main() {
    let s = String::from("hi");
    let f = || s;
    let _a = f();
    let _b = f();
    // error[E0382]: use of moved value: `f`
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hi"
	f := func() string { return s }
	fmt.Println(f(), f())
}
```

- **Go 怎么做**：多次返回 string 头通常无妨。
- **Rust 为什么不同**：返回拥有型捕获等于移出闭包环境。
- **Go 程序员易踩的坑**：把 `FnOnce` 闭包存起来调用两次。

---

## Q10. 为什么无捕获闭包能当函数指针？ {#q10}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

不捕获环境的闭包没有闭包状态，可强制转换成函数指针 `fn(...)`；有捕获则每个闭包是匿名独特类型，只能走泛型/`dyn Fn`。

**解答：**

`let f: fn(i32) -> i32 = |x| x + 1;` 合法。一旦捕获外部变量，就不能写成 `fn` 指针。

```rust
fn main() {
    let f: fn(i32) -> i32 = |x| x + 1;
    println!("{}", f(3));
}
```

```rust
fn main() {
    let n = 1;
    let f: fn(i32) -> i32 = |x| x + n;
    // error[E0308]: mismatched types
    println!("{}", f(3));
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var f func(int) int = func(x int) int { return x + 1 }
	fmt.Println(f(3))
}
```

- **Go 怎么做**：函数值类型统一。
- **Rust 为什么不同**：`fn` 指针与闭包类型分开。
- **Go 程序员易踩的坑**：有捕获还硬转 `fn`。

---

## Q11. 返回闭包为什么常写 `impl Fn(...)`？ {#q11}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

每个闭包都有独一无二的匿名类型，函数无法直接写出那个类型名，所以用 `impl Fn...`（或 `Box<dyn Fn...>`）作为返回类型。

**解答：**

写法：`fn make() -> impl Fn(i32) -> i32 { |x| x + 1 }`。若返回类型在分支间是两个不同闭包，通常不能写成同一个 `impl Fn`，要改用 `Box<dyn Fn...>`（见 [Q12](#q12)）。

```rust
fn make_adder(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x + n
}

fn main() {
    let add3 = make_adder(3);
    println!("{}", add3(4));
}
```

```rust
fn make_greeter(name: String) -> impl Fn() {
    move || println!("hi {name}")
}

fn main() {
    make_greeter(String::from("Ada"))();
}
```

**Go 对比：**

```go
package main

import "fmt"

func makeAdder(n int) func(int) int {
	return func(x int) int { return x + n }
}

func main() {
	fmt.Println(makeAdder(3)(4))
}
```

- **Go 怎么做**：返回 `func(...)` 即可。
- **Rust 为什么不同**：闭包类型匿名，需 `impl Trait` 或 trait 对象。
- **Go 程序员易踩的坑**：两个分支返回不同闭包却强行一个 `impl Fn`。

---

## Q12. 什么时候该用 `Box<dyn Fn()>`？ {#q12}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

需要在运行期统一多种闭包类型、存进结构体字段、或从分支返回不同闭包时，用堆上的 trait 对象 `Box<dyn Fn...>`。

**解答：**

代价：虚调用 + 堆分配。单形态热路径优先泛型 `impl Fn`/`F: Fn`。`FnMut`/`FnOnce` 同样可 `Box`。

```rust
fn pick(flag: bool) -> Box<dyn Fn(i32) -> i32> {
    if flag {
        Box::new(|x| x + 1)
    } else {
        Box::new(|x| x * 2)
    }
}

fn main() {
    println!("{}", pick(true)(3));
    println!("{}", pick(false)(3));
}
```

```rust
struct Hook {
    f: Box<dyn Fn()>,
}

fn main() {
    let h = Hook {
        f: Box::new(|| println!("hook")),
    };
    (h.f)();
}
```

**Go 对比：**

```go
package main

import "fmt"

func pick(flag bool) func(int) int {
	if flag {
		return func(x int) int { return x + 1 }
	}
	return func(x int) int { return x * 2 }
}

func main() {
	fmt.Println(pick(true)(3))
}
```

- **Go 怎么做**：函数值天然可互换。
- **Rust 为什么不同**：不同闭包类型不同，统一需 `dyn`。
- **Go 程序员易踩的坑**：到处 `Box<dyn Fn>`，热路径白白间接调用。

---

## Q13. 迭代器链会不会比手写循环慢？ {#q13}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

通常不会：闭包与迭代器适配器常被内联优化到和手写循环同级；先求清晰，真有热点再测。

**解答：**

Release 下 LLVM 常把 `map/filter/collect` 优化得很激进。调试构建更慢不代表发布慢。过长的链可读性差时，收中间 `Vec` 或改循环（见 [Q18](#q18)）。

```rust
fn main() {
    let s: i32 = (1..=100).filter(|x| x % 2 == 0).map(|x| x * x).sum();
    println!("{s}");
}
```

```rust
fn main() {
    let mut s = 0;
    for x in 1..=100 {
        if x % 2 == 0 {
            s += x * x;
        }
    }
    println!("{s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := 0
	for x := 1; x <= 100; x++ {
		if x%2 == 0 {
			s += x * x
		}
	}
	fmt.Println(s)
}
```

- **Go 怎么做**：循环是默认风格。
- **Rust 为什么不同**：迭代器是一等抽象且常零成本。
- **Go 程序员易踩的坑**：未测量就认定迭代器慢。

---

## Q14. 为什么 `collect::<Vec<_>>()` 这种 turbofish 写法这么常见？ {#q14}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

在表达式中间不能方便写 `let` 类型标注时，用 `::<>`（turbofish）直接告诉 `collect` 目标类型。

**解答：**

`foo().map(...).collect::<Vec<_>>()` 很常见。`_` 仍可推断元素。也可用 `FromIterator` 目标如 `HashMap<_,_>`。

```rust
fn main() {
    let n = (1..=3).map(|x| x * 2).collect::<Vec<_>>().len();
    println!("{n}");
}
```

```rust
use std::collections::HashSet;

fn main() {
    let s = [1, 2, 2, 3].into_iter().collect::<HashSet<_>>();
    println!("{}", s.len());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	fmt.Println(len([]int{2, 4, 6}))
}
```

- **Go 怎么做**：类型在复合字面量上可见。
- **Rust 为什么不同**：方法链中途需要喂类型参数。
- **Go 程序员易踩的坑**：看见 `::<>` 以为是魔咒，不理解是类型实参。

---

## Q15. `chars()` 和 `bytes()` 返回的其实也是迭代器，对吧？ {#q15}
**Tags:** `common` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

对。`str::chars` 产出 `char`（Unicode 标量值）迭代器；`bytes` 产出 `u8` 迭代器；都惰性，可继续 `map`/`collect`。

**解答：**

这和 Go `range` string 得 rune、或按字节遍历对应。别用 `len()` 当字符数。

```rust
fn main() {
    let s = "你好a";
    println!("bytes={} chars={}", s.len(), s.chars().count());
}
```

```rust
fn main() {
    let chars: Vec<char> = "hi".chars().collect();
    let bytes: Vec<u8> = "hi".bytes().collect();
    println!("{chars:?} {bytes:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "你好a"
	fmt.Println(len(s))
	for _, r := range s {
		fmt.Println(string(r))
	}
}
```

- **Go 怎么做**：`range` string 按 rune。
- **Rust 为什么不同**：显式选 `chars` 或 `bytes`。
- **Go 程序员易踩的坑**：`s.len()` 当字符数。

---

## Q16. Go 的 `for range` 和 Rust 迭代器最重要的区别是什么？ {#q16}
**Tags:** `occasional` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

`for range` 是立即执行的语言语法；Rust 迭代器是可组合的惰性值，消费方式（借/变/吃）由 `iter` 家族显式选择。

**解答：**

Rust 也能 `for x in v.iter()`，那只是消费器语法糖。真正差别是中间能插 `map/filter`，以及所有权模式清晰。

```rust
fn main() {
    let v = vec![1, 2, 3];
    for x in v.iter() {
        println!("{x}");
    }
    let doubled: Vec<_> = v.iter().map(|x| x * 2).collect();
    println!("{doubled:?}");
}
```

```rust
fn main() {
    let v = vec![1, 2, 3];
    for x in v {
        println!("{x}");
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	for _, x := range v {
		fmt.Println(x)
	}
}
```

- **Go 怎么做**：range 一把梭。
- **Rust 为什么不同**：迭代是库级抽象 + 所有权三态。
- **Go 程序员易踩的坑**：所有循环都 `for x in v` 把容器吃光。

---

## Q17. Go 1.23 的 range-over-func 跟 Rust 迭代器像吗？ {#q17}
**Tags:** `occasional` `iterator`
**适用版本:** Rust 1.0+；Go 1.23+ 的 `iter` 推送式迭代

**一句话答案：**

有点像：都把“可遍历序列”变成一等概念；但 Go 的 push 风格（回调 yield）与 Rust 的 pull 风格（`next`）模型不同。

**解答：**

Go 1.23+ 可用 `iter.Seq` 等与 `for range` 集成。Rust 标准是 `Iterator::next` 拉取。都能表达惰性序列，但组合子生态与所有权规则仍是 Rust 侧更重。

```rust
fn main() {
    let v: Vec<_> = (0..4).filter(|x| *x % 2 == 0).collect();
    println!("{v:?}");
}
```

```rust
fn odds() -> impl Iterator<Item = i32> {
    (1..).filter(|x| x % 2 == 1)
}

fn main() {
    let v: Vec<_> = odds().take(3).collect();
    println!("{v:?}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"iter"
)

func odds() iter.Seq[int] {
	return func(yield func(int) bool) {
		for i := 1; ; i += 2 {
			if !yield(i) {
				return
			}
		}
	}
}

func main() {
	n := 0
	for v := range odds() {
		fmt.Println(v)
		n++
		if n == 3 {
			break
		}
	}
}
```

- **Go 怎么做**：range-over-func 推送值。
- **Rust 为什么不同**：拉取式 `Iterator` + 适配器。
- **Go 程序员易踩的坑**：以为两者 API 可以一一对应翻译。

---

## Q18. 什么时候该为了看懂代码而收成中间 `Vec`？ {#q18}
**Tags:** `occasional` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

链太长难读、要多次复用中间结果、或下一步 API 只要切片/随机访问时，先 `collect::<Vec<_>>()` 更清晰。

**解答：**

可读性优先于微优化。中间 `Vec` 有分配成本，但调试和审查往往更省人时间。也可拆成具名函数返回 `impl Iterator`。

```rust
fn main() {
    let evens: Vec<_> = (1..=10).filter(|x| x % 2 == 0).collect();
    let squares: Vec<_> = evens.iter().map(|x| x * x).collect();
    println!("{squares:?}");
}
```

```rust
fn main() {
    let squares: Vec<_> = (1..=10)
        .filter(|x| x % 2 == 0)
        .map(|x| x * x)
        .collect();
    println!("{squares:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	evens := []int{}
	for i := 1; i <= 10; i++ {
		if i%2 == 0 {
			evens = append(evens, i)
		}
	}
	fmt.Println(evens)
}
```

- **Go 怎么做**：自然出现中间切片。
- **Rust 为什么不同**：可以一直惰性，但不必为炫技牺牲可读。
- **Go 程序员易踩的坑**：一条链式写 8 个适配器没人敢改。

---

## Q19. 闭包报 `E0525` 时通常意味着什么？ {#q19}
**Tags:** `advanced` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

API 要求 `Fn`（可共享、只读捕获），但你的闭包只实现了 `FnMut`/`FnOnce`（会改或拿走捕获）。

**解答：**

修法：别改捕获；把可变状态挪到外部用别的方式传；或把 API 改成 `FnMut`。典型是把 `|| n += 1` 传给只要 `Fn` 的参数。

```rust
fn need_fn<F: Fn()>(f: F) {
    f();
}

fn main() {
    let n = 0;
    need_fn(|| println!("{n}"));
}
```

```rust
fn need_fn<F: Fn()>(f: F) {
    f();
}

fn main() {
    let mut n = 0;
    let inc = || n += 1;
    need_fn(inc);
    // error[E0525]: expected a closure that implements the `Fn` trait, but this closure only implements `FnMut`
}
```

```rust
fn need_mut<F: FnMut()>(mut f: F) {
    f();
    f();
}

fn main() {
    let mut n = 0;
    need_mut(|| n += 1);
    println!("{n}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func need(f func()) { f() }

func main() {
	n := 0
	need(func() { n++ })
	fmt.Println(n)
}
```

- **Go 怎么做**：没有 Fn 分层。
- **Rust 为什么不同**：`Fn` 承诺可安全地多次只读调用（含共享场景）。
- **Go 程序员易踩的坑**：看见 `E0525` 却去乱 `move`/`clone` 整容器。

---

## Q20. 这一章最该带走的迭代器/闭包心智模型是什么？ {#q20}
**Tags:** `advanced` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

迭代器是惰性流水线，用三种 `iter` 选借用/消费；闭包按捕获方式落入 `Fn`/`FnMut`/`FnOnce`；`collect` 要给目标类型。

**解答：**

口诀：

1. 没消费器就没计算。
2. `iter` / `iter_mut` / `into_iter` 先选对。
3. 闭包：只读 / 可变 / 拿走 → `Fn` / `FnMut` / `FnOnce`。
4. 线程边界常要 `move`。
5. `E0283`/`E0282` 想 `Vec<_>`；`E0525` 想调用约定。

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let s: i32 = v.iter().sum();
    v.iter_mut().for_each(|x| *x += 1);
    let owned: Vec<_> = v.into_iter().map(|x| x * 2).collect();
    println!("{s} {owned:?}");
}
```

```rust
fn apply<F: FnMut(i32) -> i32>(mut f: F) {
    println!("{}", f(3));
}

fn main() {
    let mut n = 1;
    apply(|x| {
        n += 1;
        x + n
    });
    println!("{n}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	sum := 0
	for _, x := range v {
		sum += x
	}
	fmt.Println(sum, v)
}
```

- **Go 怎么做**：range + 闭包函数值。
- **Rust 为什么不同**：惰性、所有权、Fn 家族是显式技能。
- **Go 程序员易踩的坑**：用 Go 循环直觉硬写，忽略消费与捕获类别。

---

## Q21. `for` 循环和 `IntoIterator` 到底什么关系？ {#q21}
**Tags:** `common` `for` `IntoIterator` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

`for x in coll` 在语义上等价于对 `coll.into_iter()` 做循环（编译器会做这种展开）；因此传 `v`、`&v`、`&mut v` 会分别走到不同的 `IntoIterator` 实现，决定元素是拥有、共享借用还是可变借用（与 [Q2](#q2) 的三种 `iter` 同一套机制）。

**解答：**

三种写法对应三种 `IntoIterator`：

```rust
fn main() {
    let mut v = vec![1, 2, 3];

    for x in &v {
        // x: &i32
        println!("{x}");
    }

    for x in &mut v {
        // x: &mut i32
        *x += 10;
    }

    for x in v {
        // x: i32；v 被消费
        println!("{x}");
    }
}
```

自定义类型只要实现 `IntoIterator`，就能直接进 `for`：

```rust
struct Countdown(u8);

impl Iterator for Countdown {
    type Item = u8;
    fn next(&mut self) -> Option<u8> {
        if self.0 == 0 {
            None
        } else {
            self.0 -= 1;
            Some(self.0 + 1)
        }
    }
}

fn main() {
    let mut sum = 0;
    for n in Countdown(3) {
        // Iterator 类型自动实现 IntoIterator
        sum += n;
    }
    assert_eq!(sum, 6);
}
```

「❌ 易混」——以为 `for` 总是借用：

```rust
fn main() {
    let v = vec![String::from("a")];
    for _ in v {}
    // println!("{v:?}");
    // error[E0382]: borrow of moved value: `v`
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	for _, x := range v {
		fmt.Println(x)
	}
	fmt.Println(v) // 仍可用
}
```

- **Go 怎么做**：`range` 不吃掉切片变量；元素是拷贝或对底层的引用语义较松。
- **Rust 为什么不同**：`for` 统一走 `IntoIterator`，所有权规则一目了然。
- **Go 程序员易踩的坑**：`for x in v` 写完还用 `v`；应 `&v`。

**记忆点：**

- `for` = `into_iter()` + `loop`。
- `v` / `&v` / `&mut v` 三种进 `for` 含义不同。
- 实现 `IntoIterator`（或 `Iterator`）就能被 `for`。

---

## Q22. `copied` 和 `cloned` 该怎么选？ {#q22}
**Tags:** `common` `iterator` `copied` `cloned` `Copy` `Clone`
**适用版本:** Rust 1.0+

**一句话答案：**

迭代器元素是 `&T` 时：`T: Copy` 用 `.copied()` 得到 `T`（按位复制）；只有 `Clone` 时用 `.cloned()`（可能分配）。能 `copied` 就别 `cloned`，意图更清晰、成本也通常更低。

**解答：**

`Copy` 整数上用 `copied`：

```rust
fn main() {
    let v = vec![1, 2, 3];
    let doubled: Vec<i32> = v.iter().copied().map(|x| x * 2).collect();
    assert_eq!(doubled, [2, 4, 6]);
    assert_eq!(v, [1, 2, 3]); // v 仍在
}
```

`String` 不是 `Copy`，只能 `cloned`（或改 `into_iter` 搬所有权）：

```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];
    let upper: Vec<String> = v.iter().cloned().map(|s| s.to_uppercase()).collect();
    assert_eq!(upper, ["A", "B"]);
    assert_eq!(v, ["a", "b"]);
}
```

和 `find` / 选项组合时也很常见：`list.iter().copied().find(|&x| x > 2)` 得到 `Option<i32>`，而不是 `Option<&i32>`：

```rust
fn main() {
    let v = [10, 20, 30];
    let n = v.iter().copied().find(|&x| x > 15);
    assert_eq!(n, Some(20));
}
```

`cloned()` 对 `&T` 调 `Clone::clone`；对已经是 `T` 的迭代器不必再套。需要引用本身时保持 `iter()`，不要无脑 `cloned`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	out := make([]int, 0, len(v))
	for _, x := range v {
		out = append(out, x*2) // range 给出元素副本
	}
	fmt.Println(out, v)
}
```

- **Go 怎么做**：`range` 对元素基本是拷贝出来用。
- **Rust 为什么不同**：默认 `iter()` 给引用，避免隐式大拷贝；要值就显式 `copied`/`cloned`。
- **Go 程序员易踩的坑**：对 `String` 乱 `copied()`（编译不过），或反过来对 `i32` 写 `cloned()` 语义含糊。

**记忆点：**

- `&T` + `Copy` → `copied()`。
- `&T` + 仅 `Clone` → `cloned()`。
- 想搬走容器里的值 → `into_iter()`，不是 `cloned`。

---

## Q23. `filter_map` 和 `map` + `filter` 怎么选？ {#q23}
**Tags:** `hot` `beginner` `filter_map` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

闭包已经产出 `Option`（解析、查找、转换可能失败）时用 `filter_map`：一次完成“变换 + 丢掉 `None`”；先变成某种值再按布尔条件筛，用 `map` + `filter`（或反过来）更清晰。

**解答：**

`filter_map` 的闭包返回 `Option<U>`，`Some` 留下、`None` 跳过：

```rust
fn main() {
    let nums: Vec<i32> = ["1", "x", "3"]
        .into_iter()
        .filter_map(|s| s.parse().ok())
        .collect();
    assert_eq!(nums, [1, 3]);
}
```

等价但更啰嗦的 `map` + `filter` + `map`（或 `flatten`）：

```rust
fn main() {
    let nums: Vec<i32> = ["1", "x", "3"]
        .into_iter()
        .map(|s| s.parse::<i32>().ok())
        .filter(|opt| opt.is_some())
        .map(|opt| opt.unwrap())
        .collect();
    assert_eq!(nums, [1, 3]);
}
```

先改形状、再按条件留——用 `map` + `filter`：

```rust
fn main() {
    let doubled_evens: Vec<_> = (1..=6)
        .map(|x| x * 2)
        .filter(|x| x % 3 == 0)
        .collect();
    assert_eq!(doubled_evens, [6, 12]);
}
```

口令：闭包自然是 `Option`/`Result`（再 `.ok()`）→ `filter_map`；闭包是 `T` 而条件是 `bool` → `filter`（必要时前面加 `map`）。不要先 `map` 成 `Option` 再手写 `unwrap` 链。

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	out := []int{}
	for _, s := range []string{"1", "x", "3"} {
		if n, err := strconv.Atoi(s); err == nil {
			out = append(out, n)
		}
	}
	fmt.Println(out)
}
```

- **Go 怎么做**：循环里 `if err == nil` 手动筛。
- **Rust 为什么不同**：`filter_map` 把“可失败变换”收成一个适配器。
- **Go 程序员易踩的坑**：写成 `map(...).filter(|o| o.is_some()).map(|o| o.unwrap())` 却不知道有 `filter_map`。

**记忆点：**

- `Option` 变换 → `filter_map`。
- `bool` 条件 → `filter`（可配 `map`）。
- 少写 `unwrap` 链。

---

## Q24. `enumerate`、`zip`、`chain` 日常怎么拼？ {#q24}
**Tags:** `common` `enumerate` `zip` `chain` `iterator`
**适用版本:** Rust 1.0+

**一句话答案：**

要下标用 `enumerate`；两条迭代器并排配对用 `zip`（短的先结束）；首尾拼接用 `chain`。三者都是惰性适配器，最后仍要 `collect`/`for` 等消费器。

**解答：**

`enumerate` 给出 `(下标, 元素)`，下标从 0 起：

```rust
fn main() {
    let v = ["a", "b", "c"];
    let pairs: Vec<_> = v.iter().copied().enumerate().collect();
    assert_eq!(pairs, [(0, "a"), (1, "b"), (2, "c")]);
}
```

`zip` 两两配对；长度取较短者：

```rust
fn main() {
    let names = ["ada", "bob"];
    let scores = [90, 80, 70]; // 多出来的 70 被丢掉
    let report: Vec<_> = names.into_iter().zip(scores).collect();
    assert_eq!(report, [("ada", 90), ("bob", 80)]);
}
```

`chain` 先耗完左边再耗右边：

```rust
fn main() {
    let a = [1, 2];
    let b = [3, 4];
    let all: Vec<_> = a.into_iter().chain(b).collect();
    assert_eq!(all, [1, 2, 3, 4]);
}
```

常见拼法：`iter().enumerate().filter(...)`；`keys.iter().zip(vals.iter())`；`part1.iter().chain(part2.iter())`。`zip` 不会补齐较短边——需要等长时先自己检查 `len`，或改用 `itertools` 之类的 crate（本篇只谈标准库）。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	names := []string{"ada", "bob"}
	scores := []int{90, 80}
	for i, name := range names {
		fmt.Println(i, name, scores[i])
	}
}
```

- **Go 怎么做**：`range` 自带下标；并排靠同一索引；拼接靠第二次 `append`/`range`。
- **Rust 为什么不同**：用适配器显式组合，不必先物化中间切片。
- **Go 程序员易踩的坑**：以为 `zip` 像某些语言会按较长边补零；Rust 是截断到较短。

**记忆点：**

- 下标 → `enumerate`。
- 并排 → `zip`（就短）。
- 拼接 → `chain`。

---

## Q25. `collect::<Result<Vec<_>, _>>()` 怎么一口气收集可失败迭代？ {#q25}
**Tags:** `hot` `collect` `Result` `FromIterator`
**适用版本:** Rust 1.0+（`Result` 实现 `FromIterator`）

**一句话答案：**
对 `Iterator<Item = Result<T, E>>` 调用 **`collect::<Result<Vec<T>, E>>()`**（常写成 `collect::<Result<Vec<_>, _>>()`）：全部成功 → `Ok(Vec)`；**遇到第一个 `Err` 就短路返回该错误**。不必手写 `for` + `?` 推 `Vec`。

**解答：**
经典场景：`parse`、IO、校验——`map` 出一串 `Result`，一次收齐：

```rust
fn main() {
    let raw = ["1", "2", "3"];
    let nums: Result<Vec<i32>, _> = raw.iter().map(|s| s.parse::<i32>()).collect();
    assert_eq!(nums.unwrap(), vec![1, 2, 3]);
}
```

失败时短路（后面的元素不会再解析）：

```rust
fn main() {
    let raw = ["1", "x", "3"];
    let nums: Result<Vec<i32>, _> = raw.iter().map(|s| s.parse::<i32>()).collect();
    assert!(nums.is_err());
}
```

turbofish 写法在链上更常见（见 [Q14](#q14)）：

```rust
fn main() {
    let nums = ["10", "20"]
        .iter()
        .map(|s| s.parse::<i32>())
        .collect::<Result<Vec<_>, _>>()
        .unwrap();
    assert_eq!(nums, vec![10, 20]);
}
```

也可收集成 `Result<HashMap<_, _>, _>` 等任何 `FromIterator` 目标，不只是 `Vec`。若要「收集全部错误」而不是短路，需要别的模式（例如 `partition` / 自建），标准 `Result` 收集是 **fail-fast**。

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	raw := []string{"1", "2", "x"}
	out := make([]int, 0, len(raw))
	for _, s := range raw {
		n, err := strconv.Atoi(s)
		if err != nil {
			fmt.Println("fail:", err)
			return
		}
		out = append(out, n)
	}
	fmt.Println(out)
}
```

- **Go 怎么做**：循环里遇错 `return`。
- **Rust 为什么不同**：`Result` 的 `FromIterator` 把「短路收集」写成一等能力。
- **Go 程序员易踩的坑**：先 `collect::<Vec<Result<_,_>>>()` 再自己找 `Err`——多一次分配，也丢了短路语义。

**记忆点：**
- `Item=Result` → `collect::<Result<Vec<_>, _>>()`。
- 语义：全成或第一错。
- 要聚合全部错误时，别用这个捷径。

---
