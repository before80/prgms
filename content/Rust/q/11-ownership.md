+++
title = "11-所有权"
date = 2026-07-28T14:49:00+08:00
weight = 110
type = "docs"
description = "面向 Go 初学者讲清 move、Copy、Clone、Drop 与所有权流转"
isCJKLanguage = true
draft = false

+++

# 所有权 (Ownership)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会把赋值当成“复制一份”，结果一用原变量就撞上 `error[E0382]`？
- 你是否分不清什么时候该 `move`、什么时候该借用、什么时候该 `.clone()`？
- 你是否想知道：Go 里赋值后两边都能用，为什么 Rust 对 `String` / `Vec` 要“吃掉”一边？
- 你是否需要一套能直接迁移到日常代码的判断规则：参数吃不吃值、返回交不交回、何时 `drop`？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| ownership | — | 所有权 | 每个值同一时刻只有一个负责人，负责最终释放 | 无直接对应（Go 靠 GC） |
| owner | — | 所有者 | 当前持有并负责释放该值的绑定 | 无 |
| move | — | 移动 / 转移 | 所有权从 A 交给 B，A 通常失效 | Go 赋值后原变量仍可用，不等价 |
| borrow | — | 借用 | 临时看或改，但不接管所有权 | 传指针 / 传切片头 |
| `Copy` | — | 按位复制 trait | 赋值后原变量仍可用的小值类型 | Go 的普通值拷贝 |
| `Clone` | — | 显式克隆 trait | 需要你手动调用的复制操作 | 手写深拷贝 / `append` 复制 |
| `Drop` | — | 析构 | 值离开作用域时自动清理资源 | `defer` 的自动版 |
| **GC** | Garbage Collector | 垃圾回收器 | 运行时扫描并回收不用对象的机制 | Go 默认机制 |
| **RAII** | Resource Acquisition Is Initialization | 资源获取即初始化 | 资源跟着值的生命周期自动释放 | Go 里常要手写 `defer` |
| partial move | — | 部分移动 | 只移走结构体/元组的部分字段 | 无直接对应 |
| `Box<T>` | — | 堆上独占指针 | 把 `T` 放到堆上，栈上只留指针 | `*T` + 手动 `new`，近似 |
| `Rc<T>` | Reference Counted | 单线程引用计数 | 多所有者共享只读数据（单线程） | 多指针指向同一对象 + GC |
| `Arc<T>` | Atomically Reference Counted | 原子引用计数 | 可跨线程共享只读数据 | 多 goroutine 共享指针 + GC |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5) |
| `common` | [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q21](#q21), [Q22](#q22) |
| `occasional` | [Q16](#q16), [Q17](#q17), [Q18](#q18) |
| `advanced` | [Q19](#q19), [Q20](#q20) |

---

## Q1. 什么是所有权，为什么 Rust 需要它？ {#q1}
**Tags:** `hot` `beginner` `ownership`
**适用版本:** Rust 1.0+（1.97.1 行为一致）

**一句话答案：**

所有权（ownership）是 Rust 的内存管理核心：每个值同一时刻只有一个**所有者**（owner），所有者离开作用域时自动释放资源——因此 Rust 不需要 **GC**（Garbage Collector，垃圾回收器）。

**解答：**

先补两个前置概念：**栈**是函数运行时存放局部变量的内存区，大小固定、随函数返回自动回收；**堆**是程序运行中按需申请的内存区，用完必须有人负责释放（详见 [15-memory-and-allocation](../15-memory-and-allocation/#q1)）。“谁来释放堆内存”正是所有权要回答的问题。

三条硬规则：

1. 每个值有且仅有一个 owner
2. 所有者离开作用域时，值被 **drop**（释放资源）
3. 所有权可以 **move**（转移）给另一个变量或函数

```rust
fn main() {
    let s = String::from("hello"); // s 拥有堆上字符串
    println!("{s}");
} // 离开 main 时自动 drop(s)，释放堆内存
```

Go 程序员最需要修正的直觉：赋值在 Rust 里首先是所有权问题，其次才是“复制了没有”。对 `String` 这种拥有堆缓冲区的类型，`let t = s;` 会把责任卡转给 `t`，而不是再复制一整份堆数据：

```rust
fn main() {
    let s = String::from("hello");
    let t = s; // move：责任卡从 s 转到 t
    // println!("{s}");
    // error[E0382]: borrow of moved value: `s`
    println!("{t}");
}
```

只读访问时用借用，原变量继续可用：

```rust
fn main() {
    let s = String::from("hello");
    let t = &s; // 借用，不接管所有权
    println!("{s} {t}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hello" // Go 的 string 头很小；真正的字节由运行时管理
	t := s       // 复制 string 头；两边都能用
	fmt.Println(s, t)
	// 堆对象何时释放由 GC 决定，不需要“单一所有者”
}
```

- **Go 怎么做**：靠 GC 在运行时回收；赋值/传参通常复制值头或指针头，原变量继续可用。
- **Rust 为什么不同**：Rust 希望在编译期就知道谁负责释放、谁还能继续访问，避免 double-free / use-after-free。
- **Go 程序员易踩的坑**：看到赋值先别想“复制”，先想“所有权有没有被转移”。

**记忆点：**

- 一个值，同一时刻一个 owner。
- 离开作用域 → 自动 drop（**RAII**：Resource Acquisition Is Initialization，资源获取即初始化）。
- 赋值/传参对非 `Copy` 类型默认是 move。

---

## Q2. 为什么赋值后原变量不能再用？ {#q2}
**Tags:** `hot` `beginner` `ownership` `move`
**适用版本:** Rust 1.0+

**一句话答案：**

对非 `Copy` 类型，赋值会 **move** 所有权；旧绑定立刻失效，再用就会 `error[E0382]`，从而避免两个人同时释放同一块堆内存。

**解答：**

`String` 在栈上只存指针 / 长度 / 容量，字节在堆上。若 `s1`、`s2` 赋值后两边都有效，离开作用域时会对同一块堆内存 drop 两次（double free）。Rust 的解法：赋值即转移所有权，旧绑定立即失效。

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // move
    // println!("{s1}");
    // error[E0382]: borrow of moved value: `s1`
    //  = note: move occurs because `s1` has type `String`,
    //          which does not implement the `Copy` trait
    println!("{s2}");
}
```

三种修复（按推荐顺序）：

```rust
fn main() {
    // 1) 借用：只需要读时最优，零成本
    let s1 = String::from("hello");
    let s2 = &s1;
    println!("{s1} {s2}");

    // 2) clone：确实需要两份独立堆数据
    let a = String::from("hello");
    let b = a.clone();
    println!("{a} {b}");

    // 3) Copy：字段全是 Copy 的小类型可 derive
    #[derive(Clone, Copy, Debug)]
    struct Point {
        x: i32,
        y: i32,
    }
    let p1 = Point { x: 1, y: 2 };
    let p2 = p1; // 按位复制，不是 move
    println!("{:?} {:?}", p1, p2);
}
```

选择依据：只读 → 借用；要独立副本 → `clone()`；字段全为 `Copy` 的小类型 → `#[derive(Copy, Clone)]`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s1 := []byte("hello")
	s2 := s1 // 复制 slice 头，共享底层数组
	s2[0] = 'H'
	fmt.Println(string(s1), string(s2)) // 两边都变
}
```

- **Go 怎么做**：赋值复制头；底层数组靠 GC，两边都能用（也可能共享底层）。
- **Rust 为什么不同**：Rust 用 move 保证“释放责任”唯一，而不是靠 GC 兜底。
- **Go 程序员易踩的坑**：把 Rust 的 `let t = s` 想成 Go 的 `t := s`，然后继续用 `s`。

**记忆点：**

- 非 `Copy` → 赋值后旧名作废。
- `E0382` = “你在用已经搬走的值”。
- 修复优先级：借 → clone → 改成 `Copy` 类型。

---

## Q3. `Copy` 和 `Clone` 到底差在哪？ {#q3}
**Tags:** `hot` `beginner` `copy` `clone`
**适用版本:** Rust 1.0+

**一句话答案：**

`Copy` 是隐式按位复制（赋值不 move）；`Clone` 是显式复制（必须 `.clone()`），对 `String`/`Vec` 会分配新堆内存。

**解答：**

| | `Copy` | `Clone` |
|---|---|---|
| 语义 | 隐式按位复制，赋值不 move | 显式复制，需调用 `.clone()` |
| 代价 | 通常廉价（小整数、指针大小） | 可能昂贵（`String`、`Vec`） |
| 约束 | 所有字段都是 `Copy`；不能实现 `Drop` | 可自定义逻辑 |

```rust
fn main() {
    let a = 5; // i32: Copy
    let b = a; // 复制，a 仍可用
    println!("{a} {b}");

    let s1 = String::from("hi");
    let s2 = s1.clone(); // 显式克隆堆数据
    println!("{s1} {s2}");
}
```

`Copy` 是 `Clone` 的子 trait：实现 `Copy` 必须实现 `Clone`（通常一起 `#[derive(Copy, Clone)]`）。

「❌ 错误写法」——想对拥有堆资源的类型 `derive(Copy)`：

```rust
#[derive(Clone, Copy)]
struct Name {
    // s: String, // 打开这行会无法 derive Copy
    n: i32,
}

fn main() {
    let a = Name { n: 1 };
    let b = a;
    println!("{} {}", a.n, b.n);
}
```

若字段含 `String`，编译器会拒绝 `Copy`（`String` 实现了 `Drop`，且拥有堆缓冲）。需要独立副本时用 `Clone`：

```rust
#[derive(Clone, Debug)]
struct Name {
    s: String,
}

fn main() {
    let a = Name {
        s: String::from("Ada"),
    };
    let b = a.clone();
    println!("{:?} {:?}", a, b);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := 5
	b := a // 整数：值拷贝
	s1 := "hi"
	s2 := s1 // string 头拷贝；字节共享且不可变
	fmt.Println(a, b, s1, s2)
}
```

- **Go 怎么做**：几乎一切赋值都是“拷贝头”；深拷贝要自己写或用库。
- **Rust 为什么不同**：把“便宜的隐式复制”和“可能很贵的显式克隆”拆成两个 trait，避免误伤性能与安全。
- **Go 程序员易踩的坑**：习惯性 `.clone()` 安抚编译器；先问能不能借用。

**记忆点：**

- `Copy` = 赋值仍可用；`Clone` = 必须显式调用。
- 有 `Drop` / 堆资源 → 通常不能 `Copy`。
- `#[derive(Copy, Clone)]` 只适合“小而纯”的类型。

---

## Q4. 函数参数为什么会“吃掉”值？ {#q4}
**Tags:** `hot` `beginner` `ownership` `functions`
**适用版本:** Rust 1.0+

**一句话答案：**

按值传 `T` 会把所有权移进函数；函数返回时参数被 drop，调用方原变量就不能再用了。只读应传 `&T` / `&str`。

**解答：**

```rust
fn consume(s: String) {
    println!("got {s}");
} // s 在这里 drop

fn borrow(s: &str) {
    println!("peek {s}");
}

fn main() {
    let owned = String::from("hi");
    borrow(&owned); // 借用，owned 仍有效
    consume(owned); // 转移所有权
    // 此后 owned 不可用
}
```

「❌ 错误写法」——吃掉后再用：

```rust
fn consume(s: String) {
    println!("{s}");
}

fn main() {
    let s = String::from("hi");
    consume(s);
    // println!("{s}");
    // error[E0382]: borrow of moved value: `s`
}
```

「✅ 正确写法」——改签名为借用，或调整使用顺序：

```rust
fn by_ref(s: &str) {
    println!("{s}");
}

fn by_val(s: String) {
    println!("{s}");
}

fn main() {
    let s = String::from("hi");
    by_ref(&s); // 1) 只读：改成借用（首选）
    by_val(s.clone()); // 2) 需要独立副本时再 clone
    by_val(s); // 3) 最后一次使用才 move
}
```

API 习惯：能读就收 `&str` / `&[T]`，调用方既可传 `&String` 也可传字面量。

**Go 对比：**

```go
package main

import "fmt"

func consume(s string) {
	fmt.Println("got", s)
}

func main() {
	s := "hi"
	consume(s)
	fmt.Println(s) // 仍然可用：传的是 string 头拷贝
}
```

- **Go 怎么做**：传 string/slice 头拷贝；原变量继续可用。
- **Rust 为什么不同**：按值传 `String` 表示“这个函数要拥有并最终释放它”。
- **Go 程序员易踩的坑**：把 `fn f(s: String)` 当成 Go 的 `func f(s string)`。

**记忆点：**

- `T` 进函数 = 可能被吃掉；`&T` / `&str` = 只看一眼。
- 只读 API 优先 `&str` / `&[T]`。
- 需要所有权才收 `String` / `Vec<T>`。

---

## Q5. 返回值如何把所有权交回来？ {#q5}
**Tags:** `hot` `beginner` `ownership` `return`
**适用版本:** Rust 1.0+

**一句话答案：**

返回 `T` 就把所有权交给调用方；也可以返回引用，但引用必须绑定到某个仍然活着的输入，不能指向函数里的局部变量。

**解答：**

```rust
fn make() -> String {
    String::from("owned") // 所有权交给调用方
}

fn first(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

fn main() {
    let a = make();
    let b = first("hello world");
    println!("{a} / {b}");
}
```

「❌ 错误写法」——返回指向局部变量的引用（悬垂引用）：

```rust
fn dangling() -> &'static String {
    let s = String::from("x");
    &s
    // error[E0515]: cannot return reference to local variable `s`
}

fn main() {
    let _ = dangling();
}
```

「✅ 正确写法」——返回所有权，或返回从输入借来的切片：

```rust
fn owned() -> String {
    String::from("x") // 只搬移指针/长度/容量，不拷贝堆字节
}

fn from_input(s: &str) -> &str {
    s.trim() // 生命周期跟输入走
}

fn main() {
    let a = owned();
    let b = from_input("  hi  ");
    println!("{a}/{b}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strings"
)

func makeOwned() string {
	return "owned"
}

func first(s string) string {
	parts := strings.Fields(s)
	if len(parts) == 0 {
		return ""
	}
	return parts[0]
}

func main() {
	fmt.Println(makeOwned(), first("hello world"))
}
```

- **Go 怎么做**：返回 string 很自然；逃逸分析可能把数据放到堆上，由 GC 管。
- **Rust 为什么不同**：返回引用必须证明“所指数据比引用活得更久”。
- **Go 程序员易踩的坑**：习惯返回局部变量地址；在 Rust 里应返回 `String` 或从参数切片。

**记忆点：**

- 交回所有权 → 返回 `T`。
- 返回 `&T` → 必须来自参数/更长生命周期的数据。
- `E0515` = 你想返回已经要死的局部变量的引用。

---

## Q6. 什么时候该借用，什么时候该移动？ {#q6}
**Tags:** `common` `ownership` `borrow`
**适用版本:** Rust 1.0+

**一句话答案：**

只读或短暂改一下 → 借用；函数要长期持有、存进结构体、或跨线程带走 → 移动（或 `clone` / `Rc`）。

**解答：**

决策树：

1. 函数只用一下就还 → `&T` / `&mut T`
2. 函数要拥有并在返回后继续持有 → `T`（move）
3. 两边都要独立继续用 → `.clone()`（或共享所有权 `Rc`/`Arc`，见 [Q15](#q15)）

```rust
fn summarize(s: &str) -> usize {
    s.len()
}

fn into_upper(mut s: String) -> String {
    s.make_ascii_uppercase();
    s // 所有权交回
}

fn main() {
    let name = String::from("rust");
    println!("{}", summarize(&name)); // 借：name 仍在
    let owned = into_upper(name); // move 进去再交回
    println!("{owned}");
}
```

「❌ 错误写法」——明明只读却按值收，导致调用方丢值：

```rust
fn only_len(s: String) -> usize {
    s.len()
}

fn main() {
    let s = String::from("hi");
    let n = only_len(s);
    // println!("{s}");
    // error[E0382]: borrow of moved value: `s`
    println!("{n}");
}
```

「✅ 正确写法」：

```rust
fn only_len(s: &str) -> usize {
    s.len()
}

fn main() {
    let s = String::from("hi");
    let n = only_len(&s);
    println!("{s} {n}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strings"
)

func summarize(s string) int { return len(s) }

func intoUpper(s string) string { return strings.ToUpper(s) }

func main() {
	name := "rust"
	fmt.Println(summarize(name))
	fmt.Println(intoUpper(name), name) // name 仍可用
}
```

- **Go 怎么做**：传 string 几乎总是拷贝头；“拥有/借用”不在类型系统里。
- **Rust 为什么不同**：签名本身就表达“吃不吃值”。
- **Go 程序员易踩的坑**：所有参数都写成 `String`，调用链上到处 `clone`。

**记忆点：**

- 默认先想借用。
- 签名里的 `T` vs `&T` 就是契约。
- 移动适合“移交责任”；借用适合“临时路过”。

---

## Q7. 为什么 `String` 不是 `Copy`？ {#q7}
**Tags:** `common` `ownership` `string`
**适用版本:** Rust 1.0+

**一句话答案：**

`String` 拥有堆缓冲区并实现了 `Drop`；若允许隐式 `Copy`，复制的只是指针，最终会 double-free。

**解答：**

常见 `Copy`：整数、浮点、`bool`、`char`、不可变引用 `&T`、仅含 `Copy` 字段的数组/元组。

```rust
fn main() {
    let a = 1;
    let b = a; // Copy
    println!("{a} {b}");

    let s = String::from("x");
    let t = s; // move，不是 Copy
    // println!("{s}"); // E0382
    println!("{t}");
}
```

`String` / `Vec<T>` 只能 `clone()`（复制堆数据）或 move。注意：`&T` 是 `Copy`，但 `&mut T` **不是** `Copy`（可变借用必须唯一，见 [12-references-and-borrowing](../12-references-and-borrowing/#q10)）。

```rust
fn main() {
    let s = String::from("hi");
    let r1 = &s;
    let r2 = r1; // &String 是 Copy
    println!("{r1} {r2} {s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "x"
	t := s // 拷贝 string 头；底层只读数据可共享
	fmt.Println(s, t)
}
```

- **Go 怎么做**：`string` 不可变 + GC，头拷贝很安全。
- **Rust 为什么不同**：`String` 可变、可释放；隐式复制指针不安全。
- **Go 程序员易踩的坑**：把 Rust `String` 当成 Go `string` 的直接等价物。

**记忆点：**

- 拥有堆资源 + 要释放 → 不能 `Copy`。
- 需要两份 → `.clone()`。
- `&T` 可 Copy；`&mut T` 不可。

---

## Q8. 部分移动是什么意思？ {#q8}
**Tags:** `common` `ownership` `partial-move`
**适用版本:** Rust 1.0+

**一句话答案：**

从结构体/元组取出非 `Copy` 字段叫**部分移动**（partial move）：整体值不能再完整使用，但未移走且为 `Copy` 的字段通常仍可单独读。

**解答：**

```rust
struct Person {
    name: String,
    age: u32,
}

fn main() {
    let p = Person {
        name: String::from("Ada"),
        age: 36,
    };
    let name = p.name; // partial move
    println!("{}", p.age); // OK：age 是 Copy
    // println!("{}", p.name);
    // error[E0382]: borrow of partially moved value: `p`
    println!("{name}");
}
```

需要整体再用：先 `clone` 字段，或解构时用引用，或改用引用访问：

```rust
struct Person {
    name: String,
    age: u32,
}

fn main() {
    let p = Person {
        name: String::from("Ada"),
        age: 36,
    };
    let Person { ref name, age } = p; // name 借用，不 move
    println!("{name} {age}");
    println!("{} {}", p.name, p.age); // p 仍完整
}
```

**Go 对比：**

```go
package main

import "fmt"

type Person struct {
	Name string
	Age  int
}

func main() {
	p := Person{Name: "Ada", Age: 36}
	name := p.Name
	fmt.Println(name, p.Age, p) // 结构体仍完整可用
}
```

- **Go 怎么做**：取字段是拷贝字段值；结构体本身不受影响。
- **Rust 为什么不同**：非 `Copy` 字段取出 = 所有权转走。
- **Go 程序员易踩的坑**：取出 `String` 字段后还想 `println!("{:?}", p)`。

**记忆点：**

- 移走一个非 `Copy` 字段 → 结构体“残缺”。
- `Copy` 字段仍可单独用。
- 想保留整体：用 `ref` / `&p.field` / `clone`。

---

## Q9. `Drop` 什么时候运行？ {#q9}
**Tags:** `common` `ownership` `drop`
**适用版本:** Rust 1.0+

**一句话答案：**

值离开作用域时，编译器插入 drop glue：若实现了 `Drop`，就调用 `Drop::drop`；局部变量按**声明的相反顺序**清理。

**解答：**

```rust
struct Guard(&'static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let _a = Guard("a");
    let _b = Guard("b");
    println!("end");
} // 先 drop b，再 drop a
```

结构体字段按**声明顺序** drop。若类型自身实现了 `Drop`，先跑你的 `Drop::drop`（字段仍完整可用），再按声明顺序 drop 各字段：

```rust
struct Guard(&'static str);
impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

struct Pair {
    first: Guard,
    second: Guard,
}
impl Drop for Pair {
    fn drop(&mut self) {
        println!("drop Pair");
    }
}

fn main() {
    let _p = Pair {
        first: Guard("first"),
        second: Guard("second"),
    };
} // drop Pair → drop first → drop second
```

提前释放用 `drop(x)`（即 `std::mem::drop`）。`Drop` 与 `Copy` 互斥。`std::mem::forget` 会跳过 drop（泄漏）。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	defer fmt.Println("drop b")
	defer fmt.Println("drop a")
	fmt.Println("end")
	// defer 也是 LIFO；但必须你自己写 defer
}
```

- **Go 怎么做**：资源清理常靠 `defer`；对象内存靠 GC。
- **Rust 为什么不同**：**RAII** 把清理绑在值的生命周期上，少写漏写 `defer`。
- **Go 程序员易踩的坑**：以为没写 `defer` 就不会清理；在 Rust 里离开作用域就会 drop。

**记忆点：**

- 离开 `{}` → drop。
- 局部变量：后声明的先 drop。
- 实现了 `Drop` 就不能 `Copy`。

---

## Q10. 为什么说 move 不是深拷贝？ {#q10}
**Tags:** `common` `ownership` `move`
**适用版本:** Rust 1.0+

**一句话答案：**

move 只转移“所有权凭证”（对 `String` 就是栈上的指针/长度/容量），堆上字节通常原地不动；深拷贝是 `.clone()` 的事。

**解答：**

```rust
fn main() {
    let s = String::from("hello"); // 堆上有 5 字节
    let t = s; // 只移动栈上的三元组；堆数据不复制
    println!("{t}");
}
```

对比 clone：

```rust
fn main() {
    let s = String::from("hello");
    let t = s.clone(); // 新分配堆缓冲并复制字节
    println!("{s} {t}");
}
```

这也解释了为什么 move 通常很便宜，而盲目 `clone` 可能很贵。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := []byte("hello")
	t := s              // 拷贝 slice 头，共享底层数组（不是深拷贝）
	u := append([]byte(nil), s...) // 才是复制底层
	fmt.Println(len(t), len(u))
}
```

- **Go 怎么做**：`t := s` 对 slice 是头拷贝；深拷贝要 `append`/`copy`。
- **Rust 为什么不同**：move 还附带“旧绑定失效”，防止双所有者。
- **Go 程序员易踩的坑**：把 move 想象成复制整块堆内存，从而害怕传 `String`。

**记忆点：**

- move ≈ 转交指针责任，不复制堆内容。
- 深拷贝 = `clone()`。
- 性能上 move 通常远便宜于 clone。

---

## Q11. 什么时候该用 `.clone()`？ {#q11}
**Tags:** `common` `ownership` `clone`
**适用版本:** Rust 1.0+；NLL 自 2018 edition 默认

**一句话答案：**

真的需要两份独立数据，或暂时用 clone 打断借用冲突时才用；优先缩小借用范围、换 API（如 `entry`），最后才 `.clone()`。

**解答：**

合理场景：要在多个所有者间各持一份、或要把值送进需要 `'static`/拥有数据的地方且无法再借用。

```rust
fn main() {
    let a = String::from("hi");
    let b = a.clone();
    println!("{a} {b}");
}
```

权宜场景——借用冲突时先 clone 打断：

```rust
use std::collections::HashMap;

fn main() {
    let mut map: HashMap<String, i32> = HashMap::from([("a".into(), 1)]);
    let v = map.get("a").cloned(); // Option<i32>，对 map 的借用结束
    map.insert("b".into(), 2);
    println!("{v:?}");
}
```

更好的做法：缩小作用域 / `entry` API：

```rust
use std::collections::HashMap;

fn main() {
    let mut map: HashMap<String, i32> = HashMap::from([("a".into(), 1)]);
    *map.entry("a".into()).or_insert(0) += 10;
    let doubled = map.get("a").copied().unwrap_or(0) * 2;
    map.insert("a2".into(), doubled);
    println!("{map:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := []byte("hi")
	b := append([]byte(nil), a...) // 明确深拷贝
	fmt.Println(string(a), string(b))
}
```

- **Go 怎么做**：深拷贝是显式的；共享很常见。
- **Rust 为什么不同**：clone 也是显式的，提醒你在付成本。
- **Go 程序员易踩的坑**：把 `.clone()` 当万能胶，掩盖本该借用的设计。

**记忆点：**

- clone = 我真的要第二份。
- 先借、再缩作用域、再换 API，最后 clone。
- `cloned()` / `copied()` 常比整容器 clone 更省。

---

## Q12. 结构体更新语法为什么会搬走字段？ {#q12}
**Tags:** `common` `ownership` `struct-update`
**适用版本:** Rust 1.0+

**一句话答案：**

`..old` 会把未写出的字段从 `old` **move**（或 `Copy`）过来；若含非 `Copy` 字段，`old` 之后通常不能再完整使用。

**解答：**

```rust
#[derive(Debug)]
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = User {
        active: false,
        ..u1 // name 从 u1 move 过来
    };
    // println!("{:?}", u1);
    // error[E0382]: borrow of partially moved value: `u1`
    println!("{:?}", u2);
}
```

若只改 `Copy` 字段且其余也想保留 `u1`，需要先 clone 非 `Copy` 字段：

```rust
#[derive(Debug, Clone)]
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = User {
        active: false,
        name: u1.name.clone(),
        // 或者：..u1.clone()
    };
    println!("{:?} {:?}", u1, u2);
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	u1 := User{Name: "Ada", Active: true}
	u2 := u1
	u2.Active = false
	fmt.Println(u1, u2) // 两个独立值拷贝
}
```

- **Go 怎么做**：结构体赋值是值拷贝（字段级）。
- **Rust 为什么不同**：`..u1` 是字段级 move/copy，不是“整包复制除非你 Clone”。
- **Go 程序员易踩的坑**：用完 `..u1` 还继续用 `u1`。

**记忆点：**

- `..old` 会搬走非 `Copy` 剩余字段。
- 两边都要留 → `old.clone()` 或逐字段 clone。
- 只读旧值 → 别用更新语法硬搬，改用引用字段设计。

---

## Q13. `println!` 会不会把值 move 走？ {#q13}
**Tags:** `common` `ownership` `println`
**适用版本:** Rust 1.0+

**一句话答案：**

一般不会：`println!` / `format_args!` 按引用格式化，不会拿走 `String` 的所有权；但你若先写成移动进函数的调用，那就另说。

**解答：**

```rust
fn main() {
    let s = String::from("hello");
    println!("{s}"); // 按引用使用
    println!("{s}"); // 仍可用
}
```

对比：自己写的按值函数会吃掉：

```rust
fn show(s: String) {
    println!("{s}");
}

fn main() {
    let s = String::from("hello");
    show(s);
    // println!("{s}");
    // error[E0382]: borrow of moved value: `s`
}
```

`dbg!(s)` 会移动（或复制）表达式的值并返回所有权；`dbg!(&s)` 只借用。`println!("{:?}", s)` 同样不 move。

```rust
fn main() {
    let s = String::from("hello");
    let s = dbg!(s); // 移入再移出
    println!("{s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hello"
	fmt.Println(s)
	fmt.Println(s) // 当然还能用
}
```

- **Go 怎么做**：打印从不“吃掉”变量。
- **Rust 为什么不同**：宏按引用格式化；普通函数的参数类型才决定吃不吃。
- **Go 程序员易踩的坑**：把“传给函数”和“传给 println!”当成一回事。

**记忆点：**

- `println!` / `eprintln!` 默认不 move。
- 自己的 `fn f(x: String)` 才会吃。
- 不确定时看参数类型，不看“有没有打印”。

---

## Q14. `Box<T>` move 时到底搬了什么？ {#q14}
**Tags:** `common` `ownership` `box`
**适用版本:** Rust 1.0+

**一句话答案：**

move `Box<T>` 只搬栈上那只堆指针（以及所有权），堆上的 `T` 通常不拷贝；旧 `Box` 失效，避免两次 `deallocate`。

**解答：**

```rust
fn main() {
    let b1 = Box::new(String::from("heap"));
    let b2 = b1; // 移动 Box 指针
    // println!("{b1}");
    // error[E0382]: borrow of moved value: `b1`
    println!("{b2}");
} // 只有 b2 drop 时释放堆上 String
```

`Box` 适合：递归类型、想把大对象放堆上减小栈帧、需要拥有的 trait 对象 `Box<dyn Trait>`。

```rust
fn take(b: Box<i32>) {
    println!("{b}");
}

fn main() {
    let b = Box::new(42);
    take(b); // 所有权进函数
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	p1 := new(int)
	*p1 = 42
	p2 := p1 // 复制指针值；两者指向同一块
	fmt.Println(*p1, *p2)
}
```

- **Go 怎么做**：复制指针后多别名共存，由 GC 回收。
- **Rust 为什么不同**：`Box` 是独占所有者；move 后旧名作废。
- **Go 程序员易踩的坑**：把 `Box` 当成普通 `*T`，以为赋值后两边都能 free。

**记忆点：**

- `Box` move = 转交堆指针所有权。
- 不复制堆上 `T`（除非你 `clone`）。
- 同一时刻只有一个 `Box` 拥有那块堆。

---

## Q15. `Rc` / `Arc` 为什么叫共享所有权？ {#q15}
**Tags:** `common` `ownership` `rc` `arc`
**适用版本:** Rust 1.0+

**一句话答案：**

`Rc`/`Arc` 用引用计数让多个人共同拥有同一份数据：`clone` 只加计数，最后一个 drop 时才真正释放。

**解答：**

**引用计数**记录“当前有几个持有者”。`Rc<T>`（Reference Counted）用普通整数，单线程；`Arc<T>`（Atomically Reference Counted）用原子计数，可跨线程。

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(vec![1, 2, 3]);
    let b = Rc::clone(&a); // 强引用 +1，不复制 Vec 元素
    println!("count={} len={}", Rc::strong_count(&a), b.len());
} // 最后一个 Rc drop 时释放 Vec
```

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let a = Arc::new(vec![1, 2, 3]);
    let b = Arc::clone(&a);
    let h = thread::spawn(move || println!("{}", b.len()));
    println!("{}", a.len());
    h.join().unwrap();
}
```

内部可变需搭配 `RefCell` / `Mutex`。循环引用会导致泄漏，需 `Weak` 打破（见 [15-memory-and-allocation](../15-memory-and-allocation/#q9)）。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := []int{1, 2, 3}
	b := a // 多个头指向同一底层数组；生命周期由 GC 管
	fmt.Println(a, b)
}
```

- **Go 怎么做**：多指针共享 + GC 自动收。
- **Rust 为什么不同**：默认单一所有权；要共享就显式选 `Rc`/`Arc`。
- **Go 程序员易踩的坑**：到处 `Rc` 回到“隐式共享”，丢失 Rust 的清晰所有权边界。

**记忆点：**

- `Rc` 单线程共享；`Arc` 跨线程共享。
- `Rc::clone` 加计数，不深拷贝 `T`。
- 有环用 `Weak`。

---

## Q16. 如何提前释放一个值？ {#q16}
**Tags:** `occasional` `ownership` `drop`
**适用版本:** Rust 1.0+

**一句话答案：**

用 `drop(x)`（`std::mem::drop`）把值 move 进函数并立刻结束其生命周期；或用更小的 `{}` 作用域让它自然离开。

**解答：**

```rust
fn main() {
    let s = String::from("temp");
    drop(s); // 立即释放堆缓冲
    // println!("{s}"); // E0382
    println!("after drop");
}
```

缩小作用域同样有效，且往往更清晰：

```rust
fn main() {
    {
        let s = String::from("temp");
        println!("{s}");
    } // s drop
    println!("after scope");
}
```

`mem::replace` / `Option::take` 可在不销毁外层容器的情况下抽出内部值：

```rust
fn main() {
    let mut slot: Option<String> = Some(String::from("data"));
    let taken = slot.take();
    assert!(slot.is_none());
    println!("{taken:?}");
}
```

**Go 对比：**

```go
package main

import "runtime"

func main() {
	s := []byte("temp")
	_ = s
	runtime.GC() // 只是请求，不保证立刻回收这块
}
```

- **Go 怎么做**：不能精确“立刻释放这个变量”；最多丢引用等 GC。
- **Rust 为什么不同**：`drop` 是确定性的。
- **Go 程序员易踩的坑**：寻找 `free(s)`；在 Rust 里就是 `drop(s)` 或离开作用域。

**记忆点：**

- `drop(x)` = 提前结束所有权。
- 更小的 `{}` 往往比手动 drop 更可读。
- `take`/`replace` 适合抽出内部所有权。

---

## Q17. 为什么实现了 `Drop` 的类型不能 `Copy`？ {#q17}
**Tags:** `occasional` `ownership` `drop` `copy`
**适用版本:** Rust 1.0+

**一句话答案：**

`Copy` 意味着赋值后新旧两个值都有效；若两者离开作用域都跑 `Drop`，同一资源会被释放两次。

**解答：**

```rust
struct FileLike(u32);

impl Drop for FileLike {
    fn drop(&mut self) {
        println!("close {}", self.0);
    }
}

fn main() {
    let a = FileLike(1);
    // let b = a; // 这是 move，不是 Copy
    let b = a;
    // println!("{}", a.0); // E0382
    println!("{}", b.0);
}
```

语言规则：`Copy` 与 `Drop` 互斥。标准库的 `String`、`Vec`、`Box`、`File` 都因此不能 `Copy`。

```rust
#[derive(Clone, Copy, Debug)]
struct Point {
    x: i32,
    y: i32,
} // 可以：没有 Drop，字段都是 Copy

fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = p1;
    println!("{:?} {:?}", p1, p2);
}
```

**Go 对比：**

- **Go 怎么做**：没有 `Copy`/`Drop` trait 这对组合；`Close()` 要自己调用或 `defer`。
- **Rust 为什么不同**：用类型系统禁止“可复制 + 有清理逻辑”的危险组合。
- **Go 程序员易踩的坑**：给带资源的结构体 `derive(Copy)`。

**记忆点：**

- 有自定义清理 → 不能 `Copy`。
- 需要多份 → `Clone`（并想清楚资源语义）。
- 互斥是为了防止 double-free。

---

## Q18. 错误 `E0382` 一般怎么排查？ {#q18}
**Tags:** `occasional` `ownership` `E0382`
**适用版本:** Rust 1.0+

**一句话答案：**

`E0382` 表示你使用了已 move 的值：先找到“谁搬走了它”，再决定改成借用、调整顺序、`clone`，或返回/交还所有权。

**解答：**

典型形态：

```rust
fn main() {
    let s = String::from("hello");
    let t = s; // 这里 move
    // println!("{s}");
    // error[E0382]: borrow of moved value: `s`
    println!("{t}");
}
```

排查步骤：

1. 看编译器指出的 move 发生点（赋值、按值传参、`for x in v`、结构体更新）。
2. 若只需读：把后面的使用改成在 move 前，或把接收方改成 `&T`。
3. 若两边都要拥有：`.clone()` 或 `Rc`。
4. 若是部分移动：用 `ref`、引用字段，或只使用未移走字段。

```rust
fn main() {
    let s = String::from("hello");
    let t = &s; // 修复：借而不是搬
    println!("{s} {t}");
}
```

**Go 对比：**

- **Go 怎么做**：几乎没有“用了已移动的值”这种编译错误。
- **Rust 为什么不同**：把 use-after-move 变成编译期错误。
- **Go 程序员易踩的坑**：忽略编译器 note 里的 “consider borrowing”。

**记忆点：**

- `E0382` = use after move。
- 先找 move 点，再选借 / 换序 / clone。
- 读懂 note，往往已经给出修法。

---

## Q19. 为什么 Go 的赋值直觉在 Rust 里经常失效？ {#q19}
**Tags:** `advanced` `ownership` `go`
**适用版本:** Rust 1.0+

**一句话答案：**

Go 的赋值默认“拷贝头 + GC 兜底”，Rust 的赋值默认“转移唯一所有权”；同一行 `t := s` / `let t = s` 语义完全不同。

**解答：**

```rust
fn main() {
    let s = String::from("hello");
    let t = s;
    // 在 Go 直觉下这里还想用 s——Rust 拒绝
    println!("{t}");
}
```

对照三种 Go 常见头：

| Go | 赋值后 | Rust 近亲 |
|---|---|---|
| `int` | 两边可用 | `i32`（`Copy`） |
| `string` | 两边可用 | `&str` 近似；`String` 是 move |
| `[]T` | 共享底层 | `&[T]` / `Vec` move / `clone` |

```rust
fn main() {
    let n = 1;
    let m = n; // 像 Go 的 int
    let s = String::from("x");
    let t = s.clone(); // 若要两边都像 Go string 那样继续用，需显式
    println!("{n} {m} {s} {t}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 1
	m := n
	s := "x"
	t := s
	fmt.Println(n, m, s, t) // 全部可用
}
```

- **Go 怎么做**：赋值便宜且不失效旧名；内存归 GC。
- **Rust 为什么不同**：用失效旧名换来无 GC 的安全释放。
- **Go 程序员易踩的坑**：用 Go 的“还能用”预期读 Rust 代码。

**记忆点：**

- Go 赋值 ≈ 拷贝头；Rust 非 Copy 赋值 ≈ move。
- `String`/`Vec` 最像 Go 里“带底层缓冲的头”，但多了唯一所有者。
- 迁移时先改直觉，再改代码。

---

## Q20. 这一章最该背下来的三条规则是什么？ {#q20}
**Tags:** `advanced` `ownership` `summary`
**适用版本:** Rust 1.0+

**一句话答案：**

① 每个值同一时刻一个 owner；② 非 `Copy` 赋值/按值传参是 move；③ 离开作用域自动 drop——需要共享时再显式选借用 / `clone` / `Rc`/`Arc`。

**解答：**

```rust
struct Guard(&'static str);
impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    // 规则 1+2：move
    let s = String::from("hello");
    let t = s;
    println!("{t}");

    // 规则 2 的例外：Copy
    let a = 1;
    let b = a;
    println!("{a} {b}");

    // 规则 3：作用域结束即 drop
    let _g = Guard("g");
}
```

日常决策口诀：

```rust
fn read(s: &str) {
    println!("{s}");
}

fn take(s: String) -> String {
    s
}

fn main() {
    let s = String::from("x");
    read(&s); // 能借就不搬
    let s = take(s); // 要拥有再搬，并可交回
    let _ = s.clone(); // 真要两份再 clone
    println!("{s}");
}
```

**Go 对比：**

- **Go 怎么做**：靠 GC + 约定；没有这三条编译期规则。
- **Rust 为什么不同**：把内存安全从运行时挪到类型系统。
- **Go 程序员易踩的坑**：背 API 不背规则，导致每个报错都像新坑。

**记忆点：**

- 一值一主。
- 非 Copy 赋值即 move。
- 离开作用域即 drop；共享要显式。

---

## Q21. 什么时候该用 `mem::take` / `replace` / `swap`，而不是 `.clone()`？ {#q21}
**Tags:** `common` `ownership` `mem` `take` `replace` `swap`
**适用版本:** Rust 1.0+；`mem::take` 稳定自 1.40

**一句话答案：**

当你需要**挪走**某个字段/槽位里的值、同时让原位置留下合法占位（默认值或另一个值），用 `take` / `replace` / `swap`；只有真的需要两份独立数据时才 `.clone()`。

**解答：**

三者都在 `std::mem` 里，都不做堆拷贝：

| API | 作用 |
|-----|------|
| `mem::take(&mut T)` | 取出原值，原地放入 `T::default()` |
| `mem::replace(&mut T, new)` | 放入 `new`，返回旧值 |
| `mem::swap(&mut a, &mut b)` | 交换两个可变位置 |

典型：结构体方法要交出字段所有权，但 `self` 还得保持可 drop 的完整状态：

```rust
use std::mem;

struct Buffer {
    data: Vec<u8>,
}

impl Buffer {
    fn into_bytes(&mut self) -> Vec<u8> {
        mem::take(&mut self.data) // 留下空 Vec，不 clone
    }
}

fn main() {
    let mut b = Buffer { data: vec![1, 2, 3] };
    let v = b.into_bytes();
    assert!(b.data.is_empty());
    assert_eq!(v, vec![1, 2, 3]);
}
```

`replace` 适合“换成新值并处理旧值”；`swap` 适合两处对调：

```rust
use std::mem;

fn main() {
    let mut a = String::from("left");
    let mut b = String::from("right");
    mem::swap(&mut a, &mut b);
    let old = mem::replace(&mut a, String::from("new"));
    println!("{a} {b} {old}"); // new left right
}
```

对比 clone：clone 分配并复制内容；`take` 只搬所有权。字段是 `String`/`Vec` 时，优先 `take`（也见 [Q16](#q16) 的 `Option::take`）。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a, b := []int{1, 2}, []int{3}
	a, b = b, a // 交换 slice 头，不拷贝底层数组
	fmt.Println(a, b)
}
```

- **Go 怎么做**：赋值/交换拷贝的是头；底层缓冲常共享，靠 GC。
- **Rust 为什么不同**：非 `Copy` 赋值是 move；`take`/`replace` 明确“挪走 + 留合法值”。
- **Go 程序员易踩的坑**：为通过编译乱 `.clone()` 字段；其实只要搬所有权。

**记忆点：**

- 要两份 → `clone`；要挪走 → `take`/`replace`/`swap`。
- `take` = `replace(..., Default::default())`。
- 保持外层结构完整时，这些 API 比拆 partial move 更干净。

---

## Q22. `for` / `into_iter` 把集合吃掉了怎么办？`Option::take` 怎么移出？ {#q22}
**Tags:** `common` `ownership` `into_iter` `Option` `take`
**适用版本:** Rust 1.0+

**一句话答案：**

`for x in collection` 默认走 `IntoIterator`，对 `Vec` 等会 **move 消费**整个集合；还要留着集合就写 `for x in &v` / `v.iter()`。要从 `Option`/`结构体字段` 里拿出所有权又不毁掉外壳，用 `Option::take` 或 `mem::take`。

**解答：**

「❌ 错误直觉」——按值 `for` 之后集合没了：

```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];
    for s in v {
        // v 被 into_iter 吃掉
        println!("{s}");
    }
    // println!("{v:?}");
    // error[E0382]: borrow of moved value: `v`
}
```

「✅ 正确写法」——只要借用：

```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];
    for s in &v {
        println!("{s}");
    }
    println!("still have {} items", v.len());
}
```

需要**移出**某个元素、其余留下：不要对整个 `Vec` `into_iter` 后再拼；用索引/`swap_remove`/`drain`，或对 `Option` 槽位 `take`：

```rust
fn main() {
    let mut slot = Some(String::from("payload"));
    let taken = slot.take(); // Some(...)，slot 变 None
    assert!(slot.is_none());
    println!("{taken:?}");

    let mut parts = vec![Some(1), Some(2), Some(3)];
    let mid = parts[1].take(); // 移出中间，位置留 None
    assert_eq!(mid, Some(2));
    assert_eq!(parts, vec![Some(1), None, Some(3)]);
}
```

`into_iter` 适合“我确实要消费并转换成别的东西”；`iter` 适合只读扫描。详见迭代器篇的三种 `iter`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []string{"a", "b"}
	for _, s := range v {
		fmt.Println(s)
	}
	fmt.Println(v) // 仍可用；range 不“吃掉”切片变量
}
```

- **Go 怎么做**：`range` 不转移切片变量所有权。
- **Rust 为什么不同**：按值迭代 = 移动集合所有权，避免用完后还以为缓冲区有效。
- **Go 程序员易踩的坑**：`for x in v` 写完还去用 `v`；应改成 `&v`。

**记忆点：**

- `for x in v` 常吃掉 `v`；`for x in &v` 不吃。
- 还要集合 → 借；要转换所有权 → `into_iter`。
- 从 `Option` 掏值留壳 → `take()`。

---
