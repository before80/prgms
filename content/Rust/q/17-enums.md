+++
title = "17-枚举"
date = 2026-07-28T14:49:00+08:00
weight = 170
type = "docs"
description = "从 Go 的 tagged union 心智差异出发讲清 Rust 枚举、Option、Result 与变体数据"
isCJKLanguage = true
draft = false

+++

# 枚举 (Enums)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会把 Rust `enum` 想成 Go 的 `iota` 常量，结果完全低估它？
- 你是否还不清楚为什么 `Option`/`Result` 是日常基础类型而不是“高级语法糖”？
- 你会不会在 `match` 穷尽性、变体 move、递归 `Box`、`#[repr]`/`FFI` 上反复踩坑？
- 你是否想知道：什么时候该用 enum，什么时候该拆成多个 struct / trait？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| enum | enumeration | 枚举 | 一个值属于有限几种变体之一，可变体带数据 | `iota` / 接口+类型断言近亲 |
| variant | — | 变体 | enum 的一种可能形状 | 某具体实现类型 |
| discriminant | — | 判别式 | 标记当前是哪个变体的标签 | 手写 tag 字段 |
| `Option<T>` | — | 可选值 | `Some(T)` 或 `None` | 指针/`ok` 逗号布尔近亲 |
| `Result<T, E>` | — | 成功或失败 | `Ok(T)` 或 `Err(E)` | `(T, error)` |
| exhaustiveness | — | 穷尽性 | `match` 必须覆盖所有可能 | `switch` 通常不强制 |
| `Box<T>` | — | 堆分配智能指针 | 把 `T` 放到堆上并拥有它 | 近似 `*T` 但管释放 |
| niche optimization | — | 空位优化 | 用非法位模式表示 `None` 等，省空间 | 无直接对应 |
| `FFI` | Foreign Function Interface | 外部函数接口 | 与 C 等语言互操作 | `cgo` |
| `ABI` | Application Binary Interface | 应用二进制接口 | 二进制层面的调用/布局约定 | 同概念 |
| `#[non_exhaustive]` | — | 非穷尽标记 | 告诉下游：以后还可能加变体/字段 | 无直接对应 |
| `GC` | Garbage Collector | 垃圾回收器 | 运行时回收 | Go 默认机制 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q18](#q18) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q17](#q17), [Q19](#q19) |
| `occasional` | [Q12](#q12), [Q13](#q13), [Q14](#q14) |
| `advanced` | [Q15](#q15), [Q16](#q16) |

---

## Q1. Rust 的 enum 为什么比 Go 的 `iota` 强得多？ {#q1}
**Tags:** `hot` `beginner` `enum`
**适用版本:** Rust 1.0+；`#[non_exhaustive]` stable

**一句话答案：**

Rust enum 是带标签的联合体：每个变体可以携带不同类型的数据，并且 `match` 能做穷尽检查；`iota` 只是一组整数常量。

**解答：**

Go 常用 `const ( A = iota ...)` 表达枚举常量，多形态数据往往靠接口或 `struct { Kind; Payload }`。Rust 把“哪一种 + 带什么数据”写进同一个类型，编译器因此知道所有可能形状。

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

fn main() {
    let m = Message::Write(String::from("hi"));
    match m {
        Message::Quit => println!("quit"),
        Message::Move { x, y } => println!("{x},{y}"),
        Message::Write(s) => println!("{s}"),
    }
}
```

```rust
enum Dir {
    N,
    S,
}

fn main() {
    let d = Dir::N;
    let name = match d {
        Dir::N => "north",
        Dir::S => "south",
    };
    println!("{name}");
}
```

```rust
enum Dir {
    N,
    S,
}

fn main() {
    let d = Dir::N;
    let _name = match d {
        Dir::N => "north",
    };
    // error[E0004]: non-exhaustive patterns: `Dir::S` not covered
}
```

**Go 对比：**

```go
package main

import "fmt"

const (
	DirN = iota
	DirS
)

func main() {
	d := DirN
	switch d {
	case DirN:
		fmt.Println("north")
	case DirS:
		fmt.Println("south")
	}
}
```

- **Go 怎么做**：`iota` 给整数命名；复杂形态另用接口。
- **Rust 为什么不同**：变体、数据、穷尽性进同一类型系统。
- **Go 程序员易踩的坑**：把 enum 只当成常量列表。

---

## Q2. 为什么 `Option<T>` 到处都是？ {#q2}
**Tags:** `hot` `beginner` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 没有 null；“可能没有值”用 `Option<T>`（`Some(T)` / `None`）在类型里显式表达，强迫你处理缺失情况。

**解答：**

Go 用 `nil`、零值或 `(T, bool)`。Rust 把可空写进类型：返回 `Option<T>` 时，调用方必须 `match`/`if let`/`?`（在返回 `Option` 的函数里）等。标准库很多查找 API（如 `HashMap::get`）都返回 `Option`。

```rust
fn find_even(xs: &[i32]) -> Option<i32> {
    for &x in xs {
        if x % 2 == 0 {
            return Some(x);
        }
    }
    None
}

fn main() {
    match find_even(&[1, 3, 4]) {
        Some(v) => println!("{v}"),
        None => println!("none"),
    }
}
```

```rust
fn main() {
    let maybe = Some(String::from("hi"));
    if let Some(s) = maybe {
        println!("{s}");
    }
}
```

```rust
fn main() {
    let v = Some(1);
    println!("{}", v.unwrap_or(0));
}
```

**Go 对比：**

```go
package main

import "fmt"

func findEven(xs []int) (int, bool) {
	for _, x := range xs {
		if x%2 == 0 {
			return x, true
		}
	}
	return 0, false
}

func main() {
	if v, ok := findEven([]int{1, 3, 4}); ok {
		fmt.Println(v)
	}
}
```

- **Go 怎么做**：`nil` 或 `(value, ok)`。
- **Rust 为什么不同**：缺失是类型的一部分，不是约定。
- **Go 程序员易踩的坑**：到处 `unwrap()`，把 `Option` 又用成“可能 panic 的 null”。

---

## Q3. 为什么 `Result<T, E>` 是错误处理基础？ {#q3}
**Tags:** `hot` `beginner` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

可恢复错误用 `Result<T, E>`：`Ok(T)` 成功，`Err(E)` 失败；调用方必须处理或向上传递。

**解答：**

对应 Go 的 `(T, error)`，但 Rust 用枚举把互斥结果编码进一个值，并用 `?` 传播。`panic!` 留给真正的 bug，不替代日常错误。

```rust
fn parse_even(s: &str) -> Result<i32, String> {
    let n: i32 = s
        .parse()
        .map_err(|e: std::num::ParseIntError| e.to_string())?;
    if n % 2 == 0 {
        Ok(n)
    } else {
        Err(String::from("not even"))
    }
}

fn main() {
    match parse_even("4") {
        Ok(n) => println!("{n}"),
        Err(e) => println!("err={e}"),
    }
}
```

```rust
fn may_fail(ok: bool) -> Result<&'static str, &'static str> {
    if ok {
        Ok("yes")
    } else {
        Err("no")
    }
}

fn main() {
    let v = may_fail(true).unwrap_or("fallback");
    println!("{v}");
}
```

```rust
fn main() {
    let r: Result<i32, &str> = Err("boom");
    println!("{}", r.expect("must ok"));
    // 运行期 panic（不是编译错误）：展示 expect 会在 Err 时崩
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func parseEven(s string) (int, error) {
	n, err := strconv.Atoi(s)
	if err != nil {
		return 0, err
	}
	if n%2 != 0 {
		return 0, fmt.Errorf("not even")
	}
	return n, nil
}

func main() {
	if n, err := parseEven("4"); err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(n)
	}
}
```

- **Go 怎么做**：多返回值 `(T, error)`。
- **Rust 为什么不同**：单个 `Result` 值 + 穷尽匹配/`?`。
- **Go 程序员易踩的坑**：把 `unwrap`/`expect` 当默认错误处理。

---

## Q4. 带数据的枚举变体到底怎么用？ {#q4}
**Tags:** `hot` `beginner` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

变体可以是无数据单元变体、元组变体或结构体变体；构造用 `Enum::Variant(...)`，取出数据靠模式匹配。

**解答：**

像小型代数数据类型：不同分支携带不同载荷。匹配时把载荷绑到变量上；按值匹配非 `Copy` 载荷会 move，见 [Q6](#q6)。

```rust
enum Msg {
    Quit,
    Write(String),
    Move { x: i32, y: i32 },
}

fn main() {
    let msgs = [
        Msg::Quit,
        Msg::Write(String::from("hi")),
        Msg::Move { x: 1, y: 2 },
    ];
    for m in &msgs {
        match m {
            Msg::Quit => println!("quit"),
            Msg::Write(s) => println!("write {s}"),
            Msg::Move { x, y } => println!("move {x},{y}"),
        }
    }
}
```

```rust
enum Ip {
    V4(u8, u8, u8, u8),
    V6(String),
}

fn main() {
    let home = Ip::V4(127, 0, 0, 1);
    match home {
        Ip::V4(a, b, c, d) => println!("{a}.{b}.{c}.{d}"),
        Ip::V6(s) => println!("{s}"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

type Msg struct {
	Kind string
	Text string
	X, Y int
}

func main() {
	m := Msg{Kind: "write", Text: "hi"}
	switch m.Kind {
	case "write":
		fmt.Println(m.Text)
	default:
		fmt.Println("other")
	}
}
```

- **Go 怎么做**：常手写 kind + 可选字段。
- **Rust 为什么不同**：每种变体只带自己需要的数据。
- **Go 程序员易踩的坑**：做一个巨大 struct 让无关字段大量为零值。

---

## Q5. 为什么 `match` 会强迫你处理所有变体？ {#q5}
**Tags:** `common` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

为了在新增变体或漏写分支时，编译期就失败，而不是运行到某条路径才崩。

**解答：**

漏分支会报 `E0004`。可用 `_ => ...` 显式吞掉剩余情况，但那会削弱“加变体必改代码”的保护；库的公开 enum 还可能标 `#[non_exhaustive]`（见 [Q14](#q14)）。

```rust
enum Dir {
    N,
    E,
    S,
    W,
}

fn name(d: Dir) -> &'static str {
    match d {
        Dir::N => "north",
        Dir::E => "east",
        Dir::S => "south",
        Dir::W => "west",
    }
}

fn main() {
    println!("{}", name(Dir::E));
}
```

```rust
enum Dir {
    N,
    S,
}

fn main() {
    let d = Dir::N;
    let _ = match d {
        Dir::N => "north",
    };
    // error[E0004]: non-exhaustive patterns: `Dir::S` not covered
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	d := 1
	switch d {
	case 1:
		fmt.Println("north")
		// 漏掉其他 case 也能编译
	}
}
```

- **Go 怎么做**：`switch` 通常不强制穷尽。
- **Rust 为什么不同**：把“漏处理”变成编译错误。
- **Go 程序员易踩的坑**：习惯写部分 `case`，到 Rust 被 `E0004` 拦住。

---

## Q6. 变体里的数据会不会被 move 出来？ {#q6}
**Tags:** `common` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

会。按值 `match` 非 `Copy` 载荷会把数据 move 出来，之后原 enum 值通常不能再用。

**解答：**

只想看一眼：匹配引用 `match &m`，或用 `ref`/`ref mut`（现代代码更常直接匹配引用）。需要拿走所有权再按值匹配。

```rust
enum Msg {
    Write(String),
}

fn main() {
    let m = Msg::Write(String::from("hi"));
    match m {
        Msg::Write(s) => println!("{s}"),
    }
}
```

```rust
enum Msg {
    Write(String),
}

fn main() {
    let m = Msg::Write(String::from("hi"));
    match m {
        Msg::Write(s) => println!("{s}"),
    }
    match m {
        Msg::Write(s) => println!("{s}"),
    }
    // error[E0382]: use of partially moved value: `m`
}
```

```rust
enum Msg {
    Write(String),
}

fn main() {
    let m = Msg::Write(String::from("hi"));
    match &m {
        Msg::Write(s) => println!("{s}"),
    }
    match &m {
        Msg::Write(s) => println!("again {s}"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hi"
	t := s
	fmt.Println(s, t)
}
```

- **Go 怎么做**：字符串赋值复制头，原变量仍可用。
- **Rust 为什么不同**：从变体取出 `String` 是所有权转移。
- **Go 程序员易踩的坑**：`match m` 取出 `String` 后还想打印整个 `m`。

---

## Q7. 什么时候该给枚举写方法？ {#q7}
**Tags:** `common` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

当行为属于“这个枚举值本身该会的事”（查询、转换、显示）时，在 `impl Enum` 里写方法，避免外部到处复制 `match`。

**解答：**

`impl Message { fn describe(&self) -> ... }` 写在枚举定义附近。内部仍用 `match`，但调用方只看到方法。跨许多无关类型的行为更适合 trait。

```rust
enum Msg {
    Quit,
    Write(String),
}

impl Msg {
    fn describe(&self) -> String {
        match self {
            Msg::Quit => String::from("quit"),
            Msg::Write(s) => format!("write:{s}"),
        }
    }
}

fn main() {
    let m = Msg::Write(String::from("hi"));
    println!("{}", m.describe());
}
```

```rust
enum Traffic {
    Red,
    Green,
}

impl Traffic {
    fn can_go(&self) -> bool {
        matches!(self, Traffic::Green)
    }
}

fn main() {
    println!("{}", Traffic::Green.can_go());
}
```

**Go 对比：**

```go
package main

import "fmt"

type MsgKind int

const (
	Quit MsgKind = iota
	Write
)

func Describe(kind MsgKind, text string) string {
	switch kind {
	case Quit:
		return "quit"
	case Write:
		return "write:" + text
	default:
		return "?"
	}
}

func main() {
	fmt.Println(Describe(Write, "hi"))
}
```

- **Go 怎么做**：常写包级函数 + switch。
- **Rust 为什么不同**：方法挂在 enum 上，签名更清晰。
- **Go 程序员易踩的坑**：把所有 match 散落在业务代码各处。

---

## Q8. 判别式（discriminant）是什么？ {#q8}
**Tags:** `common` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

判别式是 enum 里标记“当前是哪个变体”的标签；有载荷时通常还有对应的数据区。

**解答：**

无载荷枚举的判别式有时可当整数用（`as`），但布局默认不保证稳定，跨语言别猜。需要稳定整数标签时用 `#[repr(u8)]` 等（见 [Q9](#q9)）。可用 `std::mem::discriminant` 比较“是不是同一变体”而不看载荷。

```rust
enum Color {
    Red = 1,
    Blue = 2,
}

fn main() {
    let c = Color::Blue;
    println!("{}", c as u8);
}
```

```rust
use std::mem::discriminant;

enum Msg {
    Quit,
    Write(String),
}

fn main() {
    let a = Msg::Quit;
    let b = Msg::Write(String::from("x"));
    println!("{}", discriminant(&a) == discriminant(&b));
}
```

**Go 对比：**

```go
package main

import "fmt"

const (
	ColorRed  = 1
	ColorBlue = 2
)

func main() {
	fmt.Println(ColorBlue)
}
```

- **Go 怎么做**：常量本身就是整数。
- **Rust 为什么不同**：默认 enum 布局由编译器决定，不一定是你想的 C 式布局。
- **Go 程序员易踩的坑**：把任意 enum `as` 成整数拿去持久化/FFI。

---

## Q9. 什么时候要 `#[repr(u8)]`？ {#q9}
**Tags:** `common` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

需要和 C/协议约定固定整数宽度、或明确判别式整数类型时，把属性写在 enum 定义正上方：`#[repr(u8)]`。

**解答：**

位置：紧挨着 `enum` 上一行。常用于无载荷或 C-like 枚举。带复杂载荷的 enum 还要另看 `#[repr(C)]` 等，且 **FFI**（Foreign Function Interface，外部函数接口）必须与对方头文件一致，不能凭感觉。

```rust
#[repr(u8)]
enum Opcode {
    Nop = 0,
    Add = 1,
    Ret = 2,
}

fn main() {
    let op = Opcode::Add;
    println!("{}", op as u8);
}
```

```rust
#[repr(u8)]
enum Flag {
    Off = 0,
    On = 1,
}

fn from_u8(v: u8) -> Option<Flag> {
    match v {
        0 => Some(Flag::Off),
        1 => Some(Flag::On),
        _ => None,
    }
}

fn main() {
    println!("{}", from_u8(1).is_some());
}
```

**Go 对比：**

```go
package main

import "fmt"

type Opcode uint8

const (
	Nop Opcode = 0
	Add Opcode = 1
)

func main() {
	fmt.Println(uint8(Add))
}
```

- **Go 怎么做**：自定义整数类型 + 常量。
- **Rust 为什么不同**：默认 enum 表示不承诺固定宽度，要用 `repr` 钉死。
- **Go 程序员易踩的坑**：没写 `repr` 就把 discriminant 当协议字节发到网上。

---

## Q10. 为什么递归枚举常要 `Box`？ {#q10}
**Tags:** `common` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

编译器要知道类型的固定大小；若变体里直接嵌套同一个 enum，大小无限，必须用 `Box` 把递归部分放到堆上。

**解答：**

写法：`enum List { Cons(i32, Box<List>), Nil }`。`Box<T>` 是堆分配拥有指针，大小固定。Go 用指针天然递归；Rust 要显式间接层。

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

fn main() {
    let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Nil))));
    match list {
        List::Cons(v, _) => println!("{v}"),
        List::Nil => println!("nil"),
    }
}
```

```rust
enum Bad {
    Cons(i32, Bad),
    Nil,
}
// error[E0072]: recursive type `Bad` has infinite size
```

**Go 对比：**

```go
package main

import "fmt"

type List struct {
	Val  int
	Next *List
}

func main() {
	l := &List{Val: 1, Next: &List{Val: 2}}
	fmt.Println(l.Val, l.Next.Val)
}
```

- **Go 怎么做**：结构体里放 `*List` 即可递归。
- **Rust 为什么不同**：值类型要有限大小，递归必须间接。
- **Go 程序员易踩的坑**：写成 `Cons(i32, List)` 触发 `E0072`。

---

## Q11. `Option<&T>` 为什么常常不额外占空间？ {#q11}
**Tags:** `common` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

引用不能是空；编译器做 **niche optimization**（空位优化）：用“不可能出现的全零引用”表示 `None`，于是 `Option<&T>` 常与 `&T` 同宽。

**解答：**

这是布局优化，不是语言魔法特例 alone：`Option<NonZeroU8>` 等也有类似性质。不要依赖所有 `Option<T>` 都同大小；对具体类型用 `size_of` 验证。

```rust
use std::mem::size_of;

fn main() {
    assert_eq!(size_of::<&i32>(), size_of::<Option<&i32>>());
    println!("{}", size_of::<Option<&i32>>());
}
```

```rust
fn main() {
    let x = 1;
    let a: Option<&i32> = Some(&x);
    let b: Option<&i32> = None;
    println!("{} {}", a.is_some(), b.is_none());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var p *int
	fmt.Println(p == nil)
}
```

- **Go 怎么做**：指针本身可以为 `nil`。
- **Rust 为什么不同**：引用非空，缺失交给 `Option`，再靠空位优化省空间。
- **Go 程序员易踩的坑**：以为所有 `Option` 都比 `T` 多一个字节标签。

---

## Q12. Go 里常用接口 + struct 模拟多形态，Rust enum 有什么优势？ {#q12}
**Tags:** `occasional` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

变体集合封闭且已知时，enum + `match` 更快、更易穷尽；开放扩展、多类型实现同一行为时才更像 Go 接口那样用 trait。

**解答：**

协议消息、状态机、AST 节点这类“就这几种”用 enum。插件式后端、第三方类型要实现同一能力用 trait 对象或泛型。两者可组合：enum 里再装 `Box<dyn Trait>`。

```rust
enum Shape {
    Circle(f64),
    Rect(f64, f64),
}

fn area(s: &Shape) -> f64 {
    match s {
        Shape::Circle(r) => std::f64::consts::PI * r * r,
        Shape::Rect(w, h) => w * h,
    }
}

fn main() {
    println!("{}", area(&Shape::Rect(3.0, 4.0)));
}
```

```rust
trait Area {
    fn area(&self) -> f64;
}

struct Circle(f64);
impl Area for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.0 * self.0
    }
}

fn main() {
    let c = Circle(2.0);
    println!("{}", c.area());
}
```

**Go 对比：**

```go
package main

import "fmt"

type Shape interface{ Area() float64 }

type Rect struct{ W, H float64 }

func (r Rect) Area() float64 { return r.W * r.H }

func main() {
	var s Shape = Rect{W: 3, H: 4}
	fmt.Println(s.Area())
}
```

- **Go 怎么做**：接口是默认多形态工具。
- **Rust 为什么不同**：封闭集合用 enum 更直接、可穷尽。
- **Go 程序员易踩的坑**：凡事先上 `dyn Trait`，丢掉穷尽匹配好处。

---

## Q13. 什么时候该拆成多个 struct，而不是一个大 enum？ {#q13}
**Tags:** `occasional` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

变体几乎无共享逻辑、或某些状态有大量独有字段/长生命周期流程时，拆成独立类型（再在边界用 enum/trait 汇总）。

**解答：**

信号：某个变体的方法与其它变体毫无关系；或 match 分支里出现巨大独立模块。相反，状态转换频繁且要统一处理时，留在一个 enum 更清晰。

```rust
struct Draft {
    body: String,
}
struct Published {
    body: String,
    views: u64,
}

enum Post {
    Draft(Draft),
    Published(Published),
}

fn main() {
    let p = Post::Draft(Draft {
        body: String::from("hi"),
    });
    match p {
        Post::Draft(d) => println!("draft {}", d.body),
        Post::Published(p) => println!("{} {}", p.body, p.views),
    }
}
```

```rust
enum TooBig {
    A { a1: i32, a2: i32, a3: i32 },
    B { b1: String, b2: String, b3: String, b4: String },
}

fn main() {
    let x = TooBig::A { a1: 1, a2: 2, a3: 3 };
    match x {
        TooBig::A { a1, .. } => println!("{a1}"),
        TooBig::B { b1, .. } => println!("{b1}"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

type Draft struct{ Body string }
type Published struct {
	Body  string
	Views uint64
}

func main() {
	d := Draft{Body: "hi"}
	fmt.Println(d.Body)
}
```

- **Go 怎么做**：不同状态常是不同 struct + 接口。
- **Rust 为什么不同**：可用 enum 统一，也可在变大后拆分。
- **Go 程序员易踩的坑**：一个 enum 塞进整个业务域的所有状态。

---

## Q14. `#[non_exhaustive]` 什么时候值得用？ {#q14}
**Tags:** `occasional` `enum`
**适用版本:** Rust 1.0+；`#[non_exhaustive]` stable

**一句话答案：**

写公共库、未来可能加变体（或结构体字段）又不想让下游 `match` 在小版本升级时突然非穷尽失败时，把属性标在类型定义上方。

**解答：**

写法：在 `pub enum` / `pub struct` 上一行写 `#[non_exhaustive]`。效果：外部 crate 必须写 `_` 分支（enum）或不能用全字段字面量构造（struct）。本 crate 内部仍可穷尽匹配。

```rust
#[non_exhaustive]
pub enum ErrorKind {
    NotFound,
    PermissionDenied,
}

fn main() {
    let e = ErrorKind::NotFound;
    match e {
        ErrorKind::NotFound => println!("404"),
        ErrorKind::PermissionDenied => println!("403"),
        // 同 crate 内仍可穷尽；跨 crate 时需要 `_ => ...`
    }
}
```

```rust
#[non_exhaustive]
pub struct Config {
    pub host: String,
}

fn main() {
    let c = Config {
        host: String::from("localhost"),
    };
    println!("{}", c.host);
}
```

**Go 对比：**

```go
package main

import "fmt"

// Go 无同名属性；库演进靠文档约定与新接口
func main() {
	fmt.Println("no non_exhaustive")
}
```

- **Go 怎么做**：靠版本与文档约束客户端。
- **Rust 为什么不同**：可用属性强制下游保留通配分支。
- **Go 程序员易踩的坑**：库 enum 不加该属性，加变体变成破坏性变更。

---

## Q15. FFI 场景下为什么不能乱猜 enum 布局？ {#q15}
**Tags:** `advanced` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

默认 Rust enum 的 **ABI**（Application Binary Interface，应用二进制接口）布局不保证与 C 一致；跨语言必须显式 `repr` 并与对方定义对齐。

**解答：**

与 C 互操作时：无载荷常用 `#[repr(u8)]`/`#[repr(C)]` 的 C-like enum；带数据的联合体要按 FFI 指南设计，而不是把日常 Rust enum 直接 `transmute`。不确定就在双方用整数标签 + 独立 payload。

```rust
#[repr(C)]
enum CLike {
    A = 1,
    B = 2,
}

fn main() {
    println!("{}", CLike::B as i32);
}
```

```rust
#[repr(u8)]
enum Wire {
    Ping = 1,
    Pong = 2,
}

fn main() {
    let tag = Wire::Ping as u8;
    println!("{tag}");
}
```

**Go 对比：**

```go
package main

import "fmt"

type Wire uint8

const (
	Ping Wire = 1
	Pong Wire = 2
)

func main() {
	fmt.Println(uint8(Ping))
}
```

- **Go 怎么做**：整数常量直接当协议标签。
- **Rust 为什么不同**：enum 默认是 Rust 自己的表示，不是 C enum。
- **Go 程序员易踩的坑**：把复杂 Rust enum 指针丢给 C 却不设 `repr`。

---

## Q16. 本章最重要的枚举设计建议是什么？ {#q16}
**Tags:** `advanced` `enum`
**适用版本:** Rust 1.0+

**一句话答案：**

封闭且已知的形状用 enum；可空/可失败用 `Option`/`Result`；匹配优先借用不乱 move；递归加 `Box`；对外稳定 API 考虑 `non_exhaustive`/`repr`。

**解答：**

检查清单：

1. 别用 `iota` 心智建模——先问变体要不要带数据。
2. 缺省值/错误不要用哨兵整数，用 `Option`/`Result`。
3. `match` 按引用，除非你真要拿走载荷。
4. 开放扩展用 trait；封闭协议用 enum。
5. FFI/协议整数标签才上 `repr`。

```rust
enum Cmd {
    Quit,
    Echo(String),
}

impl Cmd {
    fn run(&self) {
        match self {
            Cmd::Quit => println!("bye"),
            Cmd::Echo(s) => println!("{s}"),
        }
    }
}

fn main() {
    Cmd::Echo(String::from("hi")).run();
}
```

```rust
fn maybe_id(ok: bool) -> Option<u32> {
    if ok {
        Some(7)
    } else {
        None
    }
}

fn main() {
    println!("{:?}", maybe_id(true));
}
```

**Go 对比：**

```go
package main

import "fmt"

func maybeID(ok bool) (uint32, bool) {
	if ok {
		return 7, true
	}
	return 0, false
}

func main() {
	if id, ok := maybeID(true); ok {
		fmt.Println(id)
	}
}
```

- **Go 怎么做**：常量 + 接口 + `(T, error)/(T, bool)`。
- **Rust 为什么不同**：enum 把形状与穷尽性变成默认工具。
- **Go 程序员易踩的坑**：继续用魔法数字和可空指针表达状态。

---

## Q17. 为什么一个大变体会撑大整个 enum？ {#q17}
**Tags:** `common` `enum` `layout` `size`
**适用版本:** Rust 1.0+

**一句话答案：**

enum 的大小至少要装得下**最大那个变体**（外加判别式等），所以一个「胖」变体会抬高**所有**变体所占空间；大载荷请 `Box` 起来，或拆成多个类型。

**解答：**

布局直觉：同一时刻只存一个变体，但静态大小按最坏情况预留：

```rust
use std::mem::size_of;

enum Slim {
    A(u8),
    B(u16),
}

enum Fat {
    Small(u8),
    Huge([u8; 1024]),
}

enum Boxed {
    Small(u8),
    Huge(Box<[u8; 1024]>), // 变体里只多一个指针级大小
}

fn main() {
    println!("Slim={}", size_of::<Slim>());
    println!("Fat={}", size_of::<Fat>()); // 被 Huge 抬高
    println!("boxed={}", size_of::<Boxed>());
}
```

何时 `Box`：某个变体偶尔出现却极大，或你大量存放该 enum（`Vec<Enum>`）时。何时拆类型：变体集合并不总一起出现，用独立 struct + trait/`Result` 更清晰（见 [Q13](#q13)）。

```text
// 心智：size_of::<Enum>() ≈ discriminant + max(size_of 各变体载荷)（还有对齐）
// 一个 [u8; 1_000_000] 变体 → 整个 enum 都约莫那么「胖」
```

**Go 对比：**

```go
package main

import "fmt"

type Msg interface{} // 接口值：类型信息 + 数据指针，不按「最大变体」预留连续块

func main() {
	var m Msg = [1024]byte{}
	fmt.Printf("%T\n", m)
}
```

- **Go 怎么做**：接口/指针间接，大对象常在堆上，容器存的是小头。
- **Rust 为什么不同**：enum 默认内联最大变体，换来匹配快、少一层间接。
- **Go 程序员易踩的坑**：按「接口一样大」估 `Vec<Enum>` 内存，结果被一个胖变体拖垮。

**记忆点：**

- enum 大小 ≈ 标签 + 最大变体。
- 偶发巨载荷 → `Box` 该变体。
- 形状不闭合 → 考虑拆类型，而不是一个超级 enum。

---

## Q18. `Option` 的 `as_ref` / `as_mut` / `as_deref` 怎么用？ {#q18}
**Tags:** `hot` `option` `as_ref` `as_deref`
**适用版本:** Rust 1.0+；`as_deref` / `as_deref_mut` 需 1.40+

**一句话答案：**

要看清里面的值又不搬走：`as_ref` → `Option<&T>`，`as_mut` → `Option<&mut T>`；里面是 `String`/`Vec`/`Box` 等智能指针、想直接拿到 `&str`/`&[T]`/`&T` 时用 `as_deref`（或 `as_deref_mut`）。

**解答：**

按值 `match`/`unwrap` 会 move 出 `T`。先变成「可选的引用」更常见：

```rust
fn show(name: &Option<String>) {
    match name.as_ref() {
        Some(s) => println!("{s}"),
        None => println!("(none)"),
    }
}

fn main() {
    let mut name = Some(String::from("Ada"));
    show(&name);
    if let Some(s) = name.as_mut() {
        s.push('!');
    }
    show(&name);
}
```

`as_deref`：在 `as_ref` 之后再按 `Deref` 剥一层，适合 `Option<String>` → `Option<&str>`：

```rust
fn len(name: &Option<String>) -> usize {
    name.as_deref().map_or(0, str::len)
}

fn main() {
    let name = Some(String::from("Ada"));
    println!("{}", len(&name));
    // 等价直觉：name.as_ref().map(|s| s.as_str())
}
```

选型：只读借用内容 → `as_ref`；要改内容 → `as_mut`；要 `&str`/`&[T]` 这种已解引用视图 → `as_deref`。不要用 `clone` 灭火替代这三者。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var p *string
	s := "Ada"
	p = &s
	if p != nil {
		fmt.Println(*p) // 指针可空；没有 as_ref 这套转换
	}
}
```

- **Go 怎么做**：`*T` / 逗号 `ok` 表达可空，解引用靠 `*`。
- **Rust 为什么不同**：`Option<T>` 与引用组合要显式转换，避免误 move。
- **Go 程序员易踩的坑**：对 `Option<String>` 直接 `*o` 式思维，或疯狂 `clone`。

**记忆点：**

- `as_ref` / `as_mut`：可选引用，防 move。
- `as_deref`：再 `Deref` 一层（如 `String` → `str`）。
- 能借就不 `clone`。

---

## Q19. 怎么用 `FromStr` / `TryFrom` 把字符串转成 enum？ {#q19}
**Tags:** `common` `enum` `FromStr` `TryFrom` `parse`
**适用版本:** Rust 1.0+

**一句话答案：**

解析文本用 `FromStr`（配合 `"red".parse::<Color>()?`）；从已有类型（`u8`、别的 enum、`&str` 以外的输入）fallible 转换用 `TryFrom`——两者都返回 `Result`，比魔法 `unwrap` 映射表更合适。

**解答：**

`FromStr` 接 `parse`：

```rust
use std::str::FromStr;

#[derive(Debug, PartialEq)]
enum Color {
    Red,
    Green,
}

#[derive(Debug)]
struct ParseColorError;

impl FromStr for Color {
    type Err = ParseColorError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "red" => Ok(Color::Red),
            "green" => Ok(Color::Green),
            _ => Err(ParseColorError),
        }
    }
}

fn main() {
    let c: Color = "red".parse().unwrap();
    assert_eq!(c, Color::Red);
    assert!("blue".parse::<Color>().is_err());
}
```

`TryFrom` 适合「从别的类型试着转」：

```rust
use std::convert::TryFrom;

#[derive(Debug, PartialEq)]
enum Op {
    Add,
    Sub,
}

impl TryFrom<u8> for Op {
    type Error = ();

    fn try_from(v: u8) -> Result<Self, Self::Error> {
        match v {
            1 => Ok(Op::Add),
            2 => Ok(Op::Sub),
            _ => Err(()),
        }
    }
}

fn main() {
    assert_eq!(Op::try_from(1).unwrap(), Op::Add);
    assert!(Op::try_from(9).is_err());
}
```

`From`/`Into` 只用于**不会失败**的转换；会失败就留下 `TryFrom`/`FromStr`。错误类型在库代码里应比 `()` 更有信息量。

**Go 对比：**

```go
package main

import (
	"errors"
	"fmt"
)

type Color int

const (
	ColorRed Color = iota
	ColorGreen
)

func ParseColor(s string) (Color, error) {
	switch s {
	case "red":
		return ColorRed, nil
	case "green":
		return ColorGreen, nil
	default:
		return 0, errors.New("bad color")
	}
}

func main() {
	c, err := ParseColor("red")
	fmt.Println(c, err)
}
```

- **Go 怎么做**：手写 `ParseX(string) (T, error)`。
- **Rust 为什么不同**：标准 trait 让 `.parse()` / `TryFrom` 成为惯例，泛型边界也好写。
- **Go 程序员易踩的坑**：用 `iota` 整数乱转 enum，却不校验非法值。

**记忆点：**

- 文本 → enum：`FromStr` + `.parse()`。
- 其他类型 → enum：`TryFrom`。
- 可能失败 → 不要用 `From` 硬转。

---
