+++
title = "07-常量与静态量"
date = 2026-07-28T14:49:00+08:00
weight = 70
type = "docs"
description = "讲清 Rust 的 const、static、const fn 与全局状态的基本边界。"
isCJKLanguage = true
draft = false

+++

# 常量与静态量 (Constants)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会分不清 `const` 和 `static`，不知道什么时候该用哪一个？
- 你是否想知道：为什么有些值能放进常量，有些却只能运行期初始化？
- 你会不会看到 `const fn`、`OnceLock`、`LazyLock`、`static mut` 后一头雾水？
- 你是否不清楚 `'static` 生命周期和 `static` 关键字是不是一回事？
- 你会不会在“全局可变状态”上照搬 Go 惯性，结果写出不安全或不可编译的 Rust？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| `const` | — | 常量 | 编译期可求值、可被内联到使用处的值 | `const` |
| `static` | — | 静态项 | 具有固定内存地址的全局值 | 包级变量 |
| `const fn` | — | 常量函数 | 既可运行期调用，也可在常量上下文调用的函数 | 无直接对应 |
| const evaluation | — | 常量求值 | 编译器在编译期执行某些表达式 | 编译期常量折叠 |
| `Sync` | — | 线程安全共享 trait | 表示类型可安全地被多个线程共享引用 | 无直接对应 |
| `Mutex` | mutual exclusion | 互斥锁 | 保证同一时刻只有一个线程可修改数据 | `sync.Mutex` |
| `OnceLock` | — | 一次初始化锁 | 全局值可延迟初始化一次 | `sync.Once` + 变量 |
| `LazyLock` | — | 惰性初始化锁 | 第一次访问时自动初始化的全局值 | `sync.OnceValue` 近亲 |
| `'static` | — | 静态生命周期 | 引用可活到整个程序结束 | 全局字面量近亲 |
| `ZST` | Zero-Sized Type | 零大小类型 | 编译后不占空间的类型 | Go 无直接对应 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q5](#q5), [Q8](#q8) |
| `common` | [Q4](#q4), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q13](#q13) |
| `occasional` | [Q11](#q11), [Q14](#q14) |
| `advanced` | [Q12](#q12) |

---

## Q1. `const` 和 `static` 到底差在哪？ {#q1}
**Tags:** `hot` `beginner` `const` `static`
**适用版本:** Rust 1.0+

**一句话答案：**
`const` 更像“编译期内联值”，`static` 更像“有固定地址的全局变量”；读配置常量常用 `const`，需要稳定地址或全局共享状态时才考虑 `static`。

**详细解答：**
```rust
const MAX: u32 = 100;
static GLOBAL: u32 = 200;

fn main() {
    println!("{MAX} {GLOBAL}");
}
```

```rust
const NAME: &str = "rust";

fn main() {
    let a = NAME;
    let b = NAME;
    println!("{a} {b}");
}
```

```rust
static PORT: u16 = 8080;

fn main() {
    let p = &PORT;
    println!("{p}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

const Max = 100

var Global = 200

func main() {
	fmt.Println(Max, Global)
}
```

- **Go 怎么做**：`const` 和包级 `var` 分工类似。
- **Rust 为什么不同**：Rust 还要区分“有无固定地址”“能否被编译期展开”这层语义。
- **Go 程序员易踩的坑**：看到 `static` 就以为只是“另一个 const”；它更接近包级全局存储。

**小结 / 记忆点：**
- 只读编译期值优先 `const`。
- 需要全局地址或共享存储时看 `static`。

---

## Q2. 为什么 `const` 里不能随便用运行期值？ {#q2}
**Tags:** `hot` `beginner` `const-eval`
**适用版本:** Rust 1.0+

**一句话答案：**
因为 `const` 要在编译期完成 **常量求值**（const evaluation）；运行期才能知道的值，编译器现在还拿不到。

**详细解答：**
```rust
const N: i32 = 10;

fn main() {
    println!("{N}");
}
```

```rust
fn main() {
    let n = 10;
    let m = n * 2;
    println!("{m}");
}
```

「❌ 错误写法」——用局部运行期变量初始化 `const`：

```rust
fn main() {
    let n = 10;
    const BAD: i32 = n * 2;
    // error[E0435]: attempt to use a non-constant value in a constant
    println!("{BAD}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	n := 10
	_ = n
	fmt.Println("Go 的 const 也只能来自编译期常量表达式")
}
```

- **Go 怎么做**：Go 的 `const` 也有限制，不能依赖运行期变量。
- **Rust 为什么不同**：Rust 这层限制更常和 `const fn`、类型系统、数组长度等能力连在一起。
- **Go 程序员易踩的坑**：把 `const` 当成“只要不改就行”；其实关键是“编译期能不能算出来”。

**小结 / 记忆点：**
- `const` 的核心不是“不变”，而是“编译期可求值”。

---

## Q3. `const fn` 是什么？跟普通函数什么关系？ {#q3}
**Tags:** `hot` `beginner` `const-fn`
**适用版本:** Rust 1.0+；支持能力逐步增加

**一句话答案：**
`const fn` 是“可在常量上下文里调用”的函数；它仍然也是普通函数，运行期同样能调用。

**详细解答：**
```rust
const fn square(x: i32) -> i32 {
    x * x
}

const N: i32 = square(4);

fn main() {
    println!("{N}");
}
```

```rust
const fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(1, 2));
}
```

const fn 既能编译期调用，也能运行期调用

**🐹 Go 对比：**
```go
package main

import "fmt"

func square(x int) int { return x * x }

func main() {
	fmt.Println(square(4))
}
```

- **Go 怎么做**：Go 没有 `const fn` 这一层，普通函数不会变成编译期常量表达式的一部分。
- **Rust 为什么不同**：Rust 希望把更多“本可提前算完”的逻辑移到编译期。
- **Go 程序员易踩的坑**：把 `const fn` 理解成“只能编译期调用”；其实它照样能运行期调用。

**小结 / 记忆点：**
- `const fn` = 普通函数 + 可进常量上下文。

---

## Q4. 关联常量（associated const）是什么？ {#q4}
**Tags:** `common` `associated-const`
**适用版本:** Rust 1.0+

**一句话答案：**
关联常量是“挂在类型或 trait 上的常量”，语义上更像“这个类型自带的固定配置”。

**详细解答：**
```rust
struct Circle;

impl Circle {
    const PI_TIMES_TWO: i32 = 6;
}

fn main() {
    println!("{}", Circle::PI_TIMES_TWO);
}
```

```rust
trait HasId {
    const ID: u32;
}

struct User;

impl HasId for User {
    const ID: u32 = 1;
}

fn main() {
    println!("{}", User::ID);
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

const UserID = 1

func main() {
	fmt.Println(UserID)
}
```

- **Go 怎么做**：更多靠包级常量命名约定。
- **Rust 为什么不同**：Rust 能把常量直接挂到类型和 trait 上，更利于抽象。
- **Go 程序员易踩的坑**：一股脑全丢成包级常量，忽略“常量也有归属语义”。

**小结 / 记忆点：**
- 与某个类型强绑定的常量，优先考虑关联常量。

---

## Q5. 为什么普通 `static` 里不能随便放 `RefCell` 这类可变状态？ {#q5}
**Tags:** `hot` `beginner` `Sync`
**适用版本:** Rust 1.0+

**一句话答案：**
因为普通 `static` 可能被多个线程同时看到，所以里面的类型通常必须满足 `Sync`；`RefCell<T>` 只适合单线程内部可变性，不满足这个要求。

**详细解答：**
```rust
use std::sync::Mutex;

static COUNTER: Mutex<u32> = Mutex::new(0);

fn main() {
    *COUNTER.lock().unwrap() += 1;
    println!("{}", *COUNTER.lock().unwrap());
}
```

全局可变状态优先用 Mutex / OnceLock / LazyLock

「❌ 错误写法」——把 `RefCell` 直接塞进普通 `static`：

```rust
use std::cell::RefCell;

static BAD: RefCell<u32> = RefCell::new(0);
// error[E0277]: `RefCell<u32>` cannot be shared between threads safely

fn main() {}
```

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"sync"
)

var (
	mu      sync.Mutex
	counter uint32
)

func main() {
	mu.Lock()
	counter++
	fmt.Println(counter)
	mu.Unlock()
}
```

- **Go 怎么做**：包级可变状态常配 `sync.Mutex`。
- **Rust 为什么不同**：Rust 在类型层面就要求你显式满足线程安全共享条件。
- **Go 程序员易踩的坑**：看到“全局变量”就先想着改值，而不是先想“它是否线程安全”。

**小结 / 记忆点：**
- 普通 `static` 的可变状态，优先配同步原语。

---

## Q6. `static mut` 为什么几乎总是不推荐？ {#q6}
**Tags:** `common` `unsafe`
**适用版本:** Rust 1.0+

**一句话答案：**
因为它把并发安全和别名规则全交给你自己兜底，很容易写出 **UB**（Undefined Behavior，未定义行为）。

**详细解答：**
```rust
static mut COUNT: u32 = 0;

fn main() {
    unsafe {
        COUNT += 1;
        println!("{COUNT}");
    }
}
```

多数场景请用 Mutex / Atomic* / OnceLock 代替 static mut

**🐹 Go 对比：**
```go
package main

import "fmt"

var count uint32

func main() {
	count++
	fmt.Println(count)
}
```

- **Go 怎么做**：语言本身不会阻止你写包级可变变量，但竞态得靠习惯和工具发现。
- **Rust 为什么不同**：Rust 直接把危险性标成 `unsafe`，逼你显式承担责任。
- **Go 程序员易踩的坑**：觉得 `static mut` 只是“麻烦一点的全局变量”；其实它是危险边界。

**小结 / 记忆点：**
- 能不用 `static mut`，就别用。

---

## Q7. `OnceLock` 和 `LazyLock` 怎么选？ {#q7}
**Tags:** `common` `lazy`
**适用版本:** `OnceLock` 稳定已久；`LazyLock` 自 Rust 1.80+ 稳定

**一句话答案：**
声明时就知道初始化逻辑，常用 `LazyLock`；需要稍后某处再 `set` 或 `get_or_init`，常用 `OnceLock`。

**详细解答：**
```rust
use std::sync::LazyLock;

static NAME: LazyLock<String> = LazyLock::new(|| "rust".to_string());

fn main() {
    println!("{}", *NAME);
}
```

```rust
use std::sync::OnceLock;

static PORT: OnceLock<u16> = OnceLock::new();

fn main() {
    let port = PORT.get_or_init(|| 8080);
    println!("{port}");
}
```

**🐹 Go 对比：**

- **Go 怎么做**：常用 `sync.Once` 或 `sync.OnceValue`。
- **Rust 为什么不同**：标准库直接给了两种常见初始化形态。
- **Go 程序员易踩的坑**：所有全局懒初始化都手写锁逻辑，忽略已有现成类型。

**小结 / 记忆点：**
- 自动惰性初始化：`LazyLock`
- 手动一次初始化：`OnceLock`

---

## Q8. const 里能不能用 `Vec`、`String`、堆分配？ {#q8}
**Tags:** `hot` `beginner` `alloc`
**适用版本:** Rust 1.97.1 stable

**一句话答案：**
空的 `Vec::new()` / `String::new()` 在稳定版可以，但“真正发生堆分配”的常量构造在 1.97.1 stable 里仍不能当成通用稳定能力依赖。

**详细解答：**
```rust
const EMPTY_VEC: Vec<i32> = Vec::new();
const EMPTY_STR: String = String::new();

fn main() {
    println!("{} {}", EMPTY_VEC.len(), EMPTY_STR.len());
}
```

在 **Rust 1.97.1 / 当前稳定通道** 上，边界可以记成：

- **可以**：空的 `Vec::new()` / `String::new()` 这类“无堆分配”的常量构造。
- **别当普适能力依赖**：`vec![1, 2, 3]`、`"hi".to_string()` 这类**真正发生堆分配**的常量构造；稳定通道对它们的支持仍有边界，很多场景仍编译失败，或只能在 nightly / 特殊条件下工作。
- **运行期照常可以**：把堆分配放到普通函数 / `main` 里做，例如 `let s = String::from("hi");`。

需要延迟初始化的全局堆数据时，优先 `OnceLock` / `LazyLock`，而不是硬塞进 `const`。

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	s := "hello"
	fmt.Println(s)
}
```

- **Go 怎么做**：字符串字面量和运行时字符串的边界对使用者不太显眼。
- **Rust 为什么不同**：Rust 更明确地区分“编译期构造”和“运行期分配”。
- **Go 程序员易踩的坑**：以为“既然不可变，就都能进 const”；Rust 看的还是编译期能否完成。

**小结 / 记忆点：**
- `const` 关注编译期能力，不只是不变性。

---

## Q9. `'static` 生命周期和 `static` 关键字是一回事吗？ {#q9}
**Tags:** `common` `lifetime`
**适用版本:** Rust 1.0+

**一句话答案：**
不是。`static` 是定义全局项的关键字；`'static` 是生命周期，表示一个引用能活到整个程序结束。

**详细解答：**
```rust
fn need_static(s: &'static str) {
    println!("{s}");
}

fn main() {
    need_static("hello");
}
```

```rust
static NAME: &str = "rust";

fn main() {
    println!("{NAME}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

var Name = "rust"

func main() {
	fmt.Println(Name)
}
```

- **Go 怎么做**：Go 没有显式生命周期语法。
- **Rust 为什么不同**：Rust 既要描述“值放在哪”，也要描述“引用能活多久”。
- **Go 程序员易踩的坑**：把 `'static` 看成“必须是全局变量”；其实字符串字面量这类引用也常满足 `'static`。

**小结 / 记忆点：**
- `static` 是存储位置概念。
- `'static` 是生命周期概念。

---

## Q10. 常量命名、位置和使用习惯有什么约定？ {#q10}
**Tags:** `common` `style`
**适用版本:** Rust 1.0+

**一句话答案：**
`const` / `static` 通常用 `SCREAMING_SNAKE_CASE`；与某类型强相关时可放进 `impl` 里做关联常量。

**详细解答：**
```rust
const MAX_RETRIES: u32 = 3;

fn main() {
    println!("{MAX_RETRIES}");
}
```

```rust
struct Config;

impl Config {
    const DEFAULT_PORT: u16 = 8080;
}

fn main() {
    println!("{}", Config::DEFAULT_PORT);
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

const MaxRetries = 3

func main() {
	fmt.Println(MaxRetries)
}
```

- **Go 怎么做**：常量命名更遵从导出与驼峰规则。
- **Rust 为什么不同**：Rust 社区约定全局常量和静态项多用大写蛇形。
- **Go 程序员易踩的坑**：沿用 Go 的导出命名风格，在 Rust 里显得别扭。

**小结 / 记忆点：**
- Rust 常量默认想成“大写蛇形”。

---

## Q11. 零大小类型（ZST）为什么会在常量话题里出现？ {#q11}
**Tags:** `occasional` `ZST`
**适用版本:** Rust 1.0+

**一句话答案：**
因为像 `()`、空结构体这类 **ZST**（Zero-Sized Type，零大小类型）经常和“编译期语义强、运行期开销低”联系在一起，能帮助你理解 Rust 类型和值并不总对应一块实际内存。

**详细解答：**
```rust
struct Marker;

fn main() {
    println!("{}", std::mem::size_of::<Marker>());
}
```

```rust
fn main() {
    let unit = ();
    println!("{}", std::mem::size_of_val(&unit));
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

type Marker struct{}

func main() {
	fmt.Println("Go 的空结构体也常被拿来表达占位或集合值")
}
```

- **Go 怎么做**：空结构体也常用来表达“占位、不存数据”。
- **Rust 为什么不同**：Rust 会更频繁把这种“零开销类型”概念和 trait、泛型、常量语义连起来。
- **Go 程序员易踩的坑**：忽略“类型本身可以有语义，但几乎没有运行时大小”这件事。

**小结 / 记忆点：**
- Rust 里“有类型”不等于“一定占内存”。

---

## Q12. const generics 里 `N + 1` 这种写法为什么还老是受限？ {#q12}
**Tags:** `advanced` `const-generics`
**适用版本:** Rust 1.97.1 stable；更复杂的 generic const expressions 仍未完全稳定

**一句话答案：**
因为“含泛型参数的更复杂常量表达式”在 stable 上仍有边界；简单 const generics 已稳定，但像 `N + 1` 这类类型级运算还不能随便到处用。

**详细解答：**
基础 const generics 已稳定，可以把长度写进类型：

```rust
struct Buf<const N: usize> {
    data: [u8; N],
}

fn main() {
    let b = Buf::<4> { data: [0; 4] };
    println!("{}", b.data.len());
}
```

「❌ 错误写法」——在 **Rust 1.97.1 stable** 上对 const 参数做 `N + 1` 这类运算（generic const expressions 仍未完全稳定）：

```rust
// 示意代码：下列在 stable 上会真实失败（尚无稳定的 error[EXXXX] 码）
struct Buf<const N: usize> {
    data: [u8; N],
}

fn widen<const N: usize>(_b: Buf<N>) -> Buf<{ N + 1 }> {
    Buf { data: [0; N + 1] }
}

fn main() {
    let b = Buf::<3> { data: [0; 3] };
    let _ = widen(b);
}
// error: generic parameters may not be used in const operations
//   = help: const parameters may only be used as standalone arguments here, i.e. `N`
```

需要“长度 + 1”这类能力时，通常改成运行期容器（如 `Vec`）、固定两个具体长度的重载，或等对应能力在稳定通道落地后再用。

**🐹 Go 对比：**

- **Go 怎么做**：Go 泛型目前不走“类型里直接带整数常量参数”这条路。
- **Rust 为什么不同**：Rust 希望把数组长度等编译期信息直接放进类型系统。
- **Go 程序员易踩的坑**：一看到 const generics 就默认所有整数运算都该可用；实际上 stable 仍有边界。

**小结 / 记忆点：**
- “基础稳定”不等于“复杂表达式全稳定”。

---

## Q13. Go 的包级全局变量，在 Rust 里对应 `const` / `static` 还是别的？ {#q13}
**Tags:** `common` `beginner` `static` `go`
**适用版本:** Rust 1.0+；`OnceLock` / `LazyLock` 见 [Q7](#q7)

**一句话答案：**
没有单一对应物：编译期只读常量用 `const`；需要固定地址的全局存储用 `static`；运行期才算出来或可变的全局状态，通常是 `static` 配 `OnceLock` / `LazyLock` / `Mutex` / 原子类型，而不是照搬 Go 的包级 `var`。

**详细解答：**
Go 里一个包级 `var` 往往同时承担“全局名字 + 可变 + 随便初始化”。Rust 把这些能力拆开了（也见 [Q1](#q1)、[Q5](#q5)、[Q7](#q7)）：

| Go 习惯 | Rust 更常见的落点 |
|---------|-------------------|
| `const Max = 100` | `const MAX: u32 = 100` |
| 永不改的配置字面量 | 优先 `const`；要取地址再考虑 `static` |
| `var x = compute()` | `OnceLock` / `LazyLock`（或启动时显式初始化） |
| `var mu sync.Mutex; var n int` | `static N: Mutex<i32> = Mutex::new(0)` 或 `Atomic*` |

```rust
const MAX_RETRIES: u32 = 3;
static DEFAULT_PORT: u16 = 8080;

fn main() {
    println!("{MAX_RETRIES} {DEFAULT_PORT}");
}
```

```rust
use std::sync::{LazyLock, Mutex};

static COUNTER: Mutex<u32> = Mutex::new(0);
static APP_NAME: LazyLock<String> = LazyLock::new(|| "demo".to_string());

fn main() {
    *COUNTER.lock().unwrap() += 1;
    println!("{} {}", *APP_NAME, *COUNTER.lock().unwrap());
}
```

「❌ 错误写法」——把 Go 的可变全局直接翻译成无同步的 `static mut`（也见 [Q6](#q6)）：

```rust
static mut COUNT: u32 = 0;

fn main() {
    unsafe {
        COUNT += 1;
        println!("{COUNT}");
    }
}
```

能写，但不该成为默认方案：并发与别名安全都甩给你自己。

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"sync"
)

const MaxRetries = 3

var (
	mu      sync.Mutex
	counter uint32
	port    = 8080
)

func main() {
	mu.Lock()
	counter++
	mu.Unlock()
	fmt.Println(MaxRetries, port, counter)
}
```

- **Go 怎么做**：包级 `const` / `var` 就是日常全局状态入口。
- **Rust 为什么不同**：要同时满足“编译期求值 / 固定地址 / 线程安全共享”，所以拆成 `const`、`static` 和同步/惰性初始化类型。
- **Go 程序员易踩的坑**：一上来满项目 `static mut`，或把所有全局都写成 `static`，连真正的编译期常量也浪费掉。

**小结 / 记忆点：**
- 只读编译期值 → `const`。
- 全局存储 → `static`（常配锁 / Once / Lazy）。
- 不要默认把 Go `var` 译成 `static mut`。

---

## Q14. `thread_local!` 和普通 `static` 怎么选？ {#q14}
**Tags:** `occasional` `thread_local` `static`
**适用版本:** Rust 1.0+

**一句话答案：**
需要**所有线程共享同一份**全局状态时用普通 `static`（类型通常还得 `Sync`）；每个线程要各自一份、互不影响时用 `thread_local!`。

**详细解答：**
普通 `static` 是进程里一份、大家都能看到的存储；跨线程共享可变状态时，常见搭配是 `Mutex` / 原子类型（见 [Q5](#q5)）。

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

static HITS: AtomicUsize = AtomicUsize::new(0);

fn main() {
    HITS.fetch_add(1, Ordering::Relaxed);
    assert_eq!(HITS.load(Ordering::Relaxed), 1);
}
```

`thread_local!` 则是“每个线程一份”。线程 A 改了自己的副本，线程 B 看不见。单线程内部可变性（如 `RefCell`）因此可以放进 TLS，而不必满足普通 `static` 对 `Sync` 的要求：

```rust
use std::cell::Cell;

thread_local! {
    static TL_COUNT: Cell<u32> = const { Cell::new(0) };
}

fn main() {
    TL_COUNT.with(|c| c.set(c.get() + 1));
    TL_COUNT.with(|c| assert_eq!(c.get(), 1));
}
```

选型口诀：

- 缓存、计数、配置要**全局一致** → 普通 `static`（再加同步）。
- 请求上下文、每线程缓冲、避免锁竞争的分片状态 → `thread_local!`。
- 需要“懒初始化且全进程共享一份” → 先看 [Q7](#q7) 的 `OnceLock` / `LazyLock`，别和 TLS 混为一谈。

**🐹 Go 对比：**

- **Go 怎么做**：没有语言级 `thread_local` 一等公民；常见是自己封装、或把状态放进 context / goroutine 局部变量。
- **Rust 为什么不同**：标准库直接提供 `thread_local!`，并和借用 / `Sync` 规则联动。
- **Go 程序员易踩的坑**：把 TLS 当成“更方便的全局变量”；跨线程汇总时会发现各线程各算各的。

**小结 / 记忆点：**
- 共享一份 → `static`。
- 每线程一份 → `thread_local!`。
- TLS ≠ 进程级单例。

---
