+++
title = "18-模式匹配"
date = 2026-07-28T14:49:00+08:00
weight = 180
type = "docs"
description = "围绕 `match`、`if let`、模式绑定与穷尽性，讲清 Rust 模式匹配的工程直觉"
isCJKLanguage = true
draft = false

+++

# 模式匹配 (Pattern Matching)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会把 `match` 当成加强版 `switch`，结果在 move、穷尽性、守卫上连环报错？
- 你是否分不清 `if let`、`let ... else`、`matches!` 各自适合什么场景？
- 你会不会被 `ref`、`@` 绑定、`_` 与 `_x`、slice 模式搞糊涂？
- 你是否想知道：为什么带 `if` 守卫的分支不能单独撑起穷尽性？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| pattern | — | 模式 | 描述值形状并可选绑定内部数据 | `switch` case / 解构近似 |
| `match` | — | 匹配表达式 | 按模式分支，要求穷尽 | `switch` |
| exhaustiveness | — | 穷尽性 | 所有可能都被覆盖 | 通常不强制 |
| `if let` | — | 单模式条件匹配 | 只关心一种成功模式时的语法糖 | `if v, ok := ...` |
| `let ... else` | — | 绑定否则早退 | 模式失败就走 else（常 return） | 早返回 if |
| guard | — | 匹配守卫 | 模式后的 `if expr` 额外条件 | case 里再 if |
| bindings | — | 绑定 | 模式里引入的变量名 | 短变量声明 |
| `ref` / `ref mut` | — | 引用绑定 | 在模式里按引用绑定字段 | 取地址 |
| `@` binding | — | at 绑定 | 既匹配子模式又抓住整个值 | 无直接对应 |
| `matches!` | — | 是否匹配宏 | 返回 bool，不取出载荷 | 条件判断 |
| move | — | 所有权移动 | 绑定可能把值拿走 | 无直接对应 |
| `GC` | Garbage Collector | 垃圾回收器 | 运行时回收 | Go 默认机制 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q17](#q17), [Q18](#q18), [Q19](#q19) |
| `occasional` | [Q12](#q12), [Q13](#q13), [Q14](#q14) |
| `advanced` | [Q15](#q15), [Q16](#q16) |

---

## Q1. 为什么 Rust 的 `match` 这么核心？ {#q1}
**Tags:** `hot` `beginner` `pattern`
**适用版本:** Rust 1.0+；`let ... else` 需 1.65+

**一句话答案：**

`match` 同时做控制流和数据解包，还能在编译期检查穷尽性与绑定方式，所以是处理 enum/Option/Result 的默认工具。

**解答：**

Go 的 `switch` 多半比较值；Rust 的 `match` 还能解构结构体、枚举变体、切片前缀。它是表达式，每个分支要能产出相容类型。

```rust
enum Dir {
    N,
    S,
}

fn main() {
    let d = Dir::S;
    let name = match d {
        Dir::N => "north",
        Dir::S => "south",
    };
    println!("{name}");
}
```

```rust
fn main() {
    let v = Some(3);
    let n = match v {
        Some(x) => x * 2,
        None => 0,
    };
    println!("{n}");
}
```

```rust
fn main() {
    let pair = (1, 2);
    match pair {
        (0, y) => println!("x=0 y={y}"),
        (x, 0) => println!("y=0 x={x}"),
        (x, y) => println!("{x},{y}"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	d := "S"
	switch d {
	case "N":
		fmt.Println("north")
	case "S":
		fmt.Println("south")
	}
}
```

- **Go 怎么做**：`switch` 分支比较。
- **Rust 为什么不同**：模式还能解包并绑定内部数据。
- **Go 程序员易踩的坑**：只把 `match` 当 `switch`，忘记它会 move/借用。

---

## Q2. 为什么 `match` 分支必须穷尽？ {#q2}
**Tags:** `hot` `beginner` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

防止漏掉一种可能；漏了就 `E0004`，把“忘了处理”提前到编译期。

**解答：**

对 enum 要覆盖每个变体，或写 `_`/`other` 通配。通配能过编译，但会吃掉未来新增变体的提醒。整数/字符等无限空间通常要靠通配收尾。

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

```rust
fn main() {
    let n = 3;
    let kind = match n {
        0 => "zero",
        1 => "one",
        _ => "other",
    };
    println!("{kind}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 3
	switch n {
	case 0:
		fmt.Println("zero")
	case 1:
		fmt.Println("one")
		// 无 default 也能编译
	}
}
```

- **Go 怎么做**：不必写满所有分支。
- **Rust 为什么不同**：穷尽性是类型安全的一部分。
- **Go 程序员易踩的坑**：漏变体还以为运行时走默认空操作。

---

## Q3. `if let` 和 `match` 该怎么选？ {#q3}
**Tags:** `hot` `beginner` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

只关心一种模式（常见 `Some`/`Ok`/`某一变体`）用 `if let`；要处理多种分支或需要穷尽提醒用 `match`。

**解答：**

`if let Pattern = expr { ... }` 失败时走 `else`（可省略）。它不会强迫你处理其它变体，所以不适合“必须覆盖全部”的场景。

```rust
fn main() {
    let v = Some(10);
    if let Some(n) = v {
        println!("{n}");
    }
}
```

```rust
enum Msg {
    Quit,
    Write(String),
}

fn main() {
    let m = Msg::Write(String::from("hi"));
    if let Msg::Write(s) = m {
        println!("{s}");
    } else {
        println!("not write");
    }
}
```

```rust
fn main() {
    let v: Option<i32> = None;
    if let Some(n) = v {
        println!("{n}");
    } else {
        println!("empty");
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var p *int
	if p != nil {
		fmt.Println(*p)
	} else {
		fmt.Println("empty")
	}
}
```

- **Go 怎么做**：`if ok` / `if p != nil`。
- **Rust 为什么不同**：`if let` 把解包和条件合成一步。
- **Go 程序员易踩的坑**：该穷尽时仍用一串 `if let`，漏分支无人提醒。

---

## Q4. `let ... else` 为什么特别适合早返回？ {#q4}
**Tags:** `hot` `beginner` `pattern`
**适用版本:** Rust 1.65+

**一句话答案：**

`let Pattern = expr else { /* 必须发散：return/break/panic */ };` 把“绑定成功才继续”写成直线代码，失败分支立刻退出。

**解答：**

写在函数体里，像 Go 的 `if err != nil { return }`。`else` 块必须 `!` 类型（不返回到后面）。适合 `Option`/`Result` 的卫语句风格。

```rust
fn first_even(xs: &[i32]) -> Option<i32> {
    let Some(&n) = xs.first() else {
        return None;
    };
    if n % 2 == 0 {
        Some(n)
    } else {
        None
    }
}

fn main() {
    println!("{:?}", first_even(&[2, 3]));
}
```

```rust
fn parse_positive(s: &str) -> Result<i32, &'static str> {
    let Ok(n) = s.parse::<i32>() else {
        return Err("parse");
    };
    if n <= 0 {
        return Err("not positive");
    }
    Ok(n)
}

fn main() {
    println!("{:?}", parse_positive("7"));
}
```

```rust
fn main() {
    let v = Some(1);
    let Some(n) = v else {
        panic!("need some");
    };
    println!("{n}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func parsePositive(s string) (int, error) {
	n, err := strconv.Atoi(s)
	if err != nil {
		return 0, err
	}
	if n <= 0 {
		return 0, fmt.Errorf("not positive")
	}
	return n, nil
}

func main() {
	fmt.Println(parsePositive("7"))
}
```

- **Go 怎么做**：卫语句 `if err != nil { return }`。
- **Rust 为什么不同**：`let else` 把模式失败和早退绑在一起。
- **Go 程序员易踩的坑**：`else` 里写完还能继续用后面的绑定（不允许）。

---

## Q5. 模式里绑定值时会不会 move？ {#q5}
**Tags:** `common` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

会。按值匹配非 `Copy` 数据会 move；只读请匹配引用或使用 `ref`。

**解答：**

`match m { Msg::Write(s) => ... }` 若 `m` 是值，`s: String` 被移出。`match &m { Msg::Write(s) => ... }` 则 `s` 是 `&String`。

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

```rust
enum Msg {
    Write(String),
}

fn main() {
    let m = Msg::Write(String::from("hi"));
    match m {
        Msg::Write(s) => println!("{s}"),
    }
    println!("{:?}", std::mem::size_of_val(&m));
    // error[E0382]: borrow of partially moved value: `m`
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

- **Go 怎么做**：赋值不破坏原变量。
- **Rust 为什么不同**：模式绑定遵循所有权。
- **Go 程序员易踩的坑**：按值 match 后还想用原 enum。

---

## Q6. `ref` / `ref mut` 还需要记吗？ {#q6}
**Tags:** `common` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

现代代码优先 `match &value` / `match &mut value`；在“按值匹配但字段要借”的场景仍可能看到 `ref`。

**解答：**

`Msg::Write(ref s)` 在按值 match 时得到 `&String`。新代码里更常见直接匹配引用。读旧代码时认识即可。

```rust
enum Msg {
    Write(String),
}

fn main() {
    let m = Msg::Write(String::from("hi"));
    match m {
        Msg::Write(ref s) => println!("{s}"),
    }
    match m {
        Msg::Write(ref s) => println!("still {s}"),
    }
}
```

```rust
fn main() {
    let mut s = String::from("hi");
    match &mut s {
        x => x.push('!'),
    }
    println!("{s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hi"
	p := &s
	fmt.Println(*p)
}
```

- **Go 怎么做**：显式取地址。
- **Rust 为什么不同**：可在模式层选择绑定方式。
- **Go 程序员易踩的坑**：新旧两种写法混用导致重复 move。

---

## Q7. `@` 绑定是什么？ {#q7}
**Tags:** `common` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

`name @ pattern` 表示：既要用子模式约束形状，又要把匹配到的整段值绑到 `name`。

**解答：**

常见于“匹配某个范围/变体，同时又要拿到整个值”。例如 `n @ 1..=5` 或 `e @ Err(_)`.

```rust
fn main() {
    let n = 3;
    match n {
        x @ 1..=5 => println!("small {x}"),
        x => println!("other {x}"),
    }
}
```

```rust
fn main() {
    let v = Some(7);
    match v {
        s @ Some(1..=10) => println!("{s:?}"),
        other => println!("{other:?}"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 3
	if n >= 1 && n <= 5 {
		fmt.Println("small", n)
	}
}
```

- **Go 怎么做**：条件判断后继续用原变量。
- **Rust 为什么不同**：`@` 把“约束”和“抓住值”写在一个模式里。
- **Go 程序员易踩的坑**：以为 `@` 是类型断言。

---

## Q8. `_` 和 `_x` 有什么区别？ {#q8}
**Tags:** `common` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

`_` 完全不绑定、也不触发未使用警告；`_x` 仍是一个绑定（会 move/借用），只是名字表示“故意不用”。

**解答：**

忽略字段用 `..` 或 `_`。若写 `_s` 去匹配 `String`，仍可能把值 move 走！真正只想忽略形状用 `_`。

```rust
fn main() {
    let pair = (1, String::from("x"));
    let (n, _) = pair;
    println!("{n}");
}
```

```rust
fn main() {
    let pair = (1, String::from("x"));
    let (n, _s) = pair;
    println!("{n}");
    // println!("{}", pair.1);
    // error[E0382]: borrow of moved value: `pair.1`
}
```

```rust
fn main() {
    let _unused = 1;
    println!("ok");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n, _ := 1, 2
	fmt.Println(n)
}
```

- **Go 怎么做**：`_` 丢弃多返回值。
- **Rust 为什么不同**：`_name` 仍是绑定；只有 `_` 是真正不绑定。
- **Go 程序员易踩的坑**：用 `_s` 以为没 move，结果字段没了。

---

## Q9. slice 模式什么时候很好用？ {#q9}
**Tags:** `common` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

要按长度/前缀拆 `&[T]` 或数组时，用 `[a, b, ..rest]` 这类模式比手写索引更清晰、更安全。

**解答：**

常匹配 `&xs[..]` 或数组。可变长度用 `..`、`[first, .., last]` 等。越界不会靠魔法索引，而是模式匹配失败走其它分支。

```rust
fn main() {
    let xs = [1, 2, 3, 4];
    match &xs[..] {
        [a, b, rest @ ..] => println!("a={a} b={b} rest={rest:?}"),
        [] => println!("empty"),
        [_] => println!("one"),
    }
}
```

```rust
fn head_sum(xs: &[i32]) -> i32 {
    match xs {
        [] => 0,
        [a] => *a,
        [a, b, ..] => a + b,
    }
}

fn main() {
    println!("{}", head_sum(&[3, 4, 5]));
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	xs := []int{1, 2, 3, 4}
	if len(xs) >= 2 {
		fmt.Println(xs[0], xs[1], xs[2:])
	}
}
```

- **Go 怎么做**：`len` + 切片表达式。
- **Rust 为什么不同**：模式把长度检查和解构合并。
- **Go 程序员易踩的坑**：继续到处 `xs[0]` 而不处理空切片。

---

## Q10. 守卫 `if guard` 有什么限制？ {#q10}
**Tags:** `common` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

守卫是模式后的额外布尔条件；它不能引入新绑定方式改变穷尽性结论，失败只是“本分支不中”，继续试下一分支。

**解答：**

写法：`Some(x) if x > 0 => ...`。守卫里不要做有副作用的重逻辑。注意 [Q11](#q11)：有守卫的分支对穷尽检查“不够格”。

```rust
fn main() {
    let v = Some(3);
    match v {
        Some(x) if x > 0 => println!("pos {x}"),
        Some(x) => println!("non-pos {x}"),
        None => println!("none"),
    }
}
```

```rust
fn main() {
    let n = 7;
    match n {
        x if x % 2 == 0 => println!("even {x}"),
        x => println!("odd {x}"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 7
	switch {
	case n%2 == 0:
		fmt.Println("even", n)
	default:
		fmt.Println("odd", n)
	}
}
```

- **Go 怎么做**：`switch` 无表达式 + case 条件。
- **Rust 为什么不同**：先模式，再守卫过滤。
- **Go 程序员易踩的坑**：以为 `Some(x) if ...` 已覆盖所有 `Some`。

---

## Q11. 为什么带守卫的分支不算穷尽？ {#q11}
**Tags:** `common` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

编译器把守卫当成运行期才知道的条件，静态上不能证明它覆盖该模式的所有值，所以仍要其它分支兜底。

**解答：**

例如只写 `Some(x) if x > 0` 和 `None`，仍漏了 `Some(x)` 且 `x <= 0` 的情况，报 `E0004`。补一个无守卫的 `Some(_)` 或 `_`。

```rust
fn main() {
    let v = Some(0);
    match v {
        Some(x) if x > 0 => println!("pos"),
        Some(_) => println!("other some"),
        None => println!("none"),
    }
}
```

```rust
fn main() {
    let v = Some(0);
    let _ = match v {
        Some(x) if x > 0 => "pos",
        None => "none",
    };
    // error[E0004]: non-exhaustive patterns: `Some(_)` not covered
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := 0
	switch {
	case v > 0:
		fmt.Println("pos")
	default:
		fmt.Println("other")
	}
}
```

- **Go 怎么做**：靠 `default` 兜底。
- **Rust 为什么不同**：无守卫模式与有守卫模式在穷尽分析里权重不同。
- **Go 程序员易踩的坑**：以为守卫已覆盖整个变体。

---

## Q12. 什么时候用 `matches!` 更合适？ {#q12}
**Tags:** `occasional` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

只想问“是不是这种形状”并得到 `bool`，不想绑定内部数据时，用 `matches!(expr, pattern)`。

**解答：**

适合条件表达式、断言、`assert!(matches!(...))`。需要载荷内容时仍用 `if let`/`match`。

```rust
enum Msg {
    Quit,
    Write(String),
}

fn main() {
    let m = Msg::Quit;
    if matches!(m, Msg::Quit) {
        println!("bye");
    }
}
```

```rust
fn main() {
    let v = Some(3);
    println!("{}", matches!(v, Some(1..=10)));
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	kind := "quit"
	fmt.Println(kind == "quit")
}
```

- **Go 怎么做**：直接比较。
- **Rust 为什么不同**：`matches!` 可测复杂模式且不取出值。
- **Go 程序员易踩的坑**：用 `matches!` 后又在别处重复 match 取数据。

---

## Q13. 为什么模式匹配也会触发借用问题？ {#q13}
**Tags:** `occasional` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

模式绑定会创建借用或 move；若绑定活得太久，后面就不能再可变借用同一数据。

**解答：**

典型坑：`match map.get(&k)` 得到的引用还在，又 `map.insert`。解决：缩短借用作用域、先拷贝/`cloned()`、或用 `entry` API。

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([(String::from("a"), 1)]);
    let got = map.get("a").copied();
    map.insert(String::from("b"), 2);
    println!("{:?} {}", got, map.len());
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([(String::from("a"), 1)]);
    let v = map.get("a");
    map.insert(String::from("b"), 2);
    // error[E0502]: cannot borrow `map` as mutable because it is also borrowed as immutable
    println!("{:?}", v);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{"a": 1}
	v := m["a"]
	m["b"] = 2
	fmt.Println(v, len(m))
}
```

- **Go 怎么做**：取出的是值拷贝（对 int），map 仍可改。
- **Rust 为什么不同**：`get` 返回的引用延长了对 map 的不可变借。
- **Go 程序员易踩的坑**：拿着 `get` 的引用去 `insert`。

---

## Q14. Go 的 type switch / if 链跟 Rust `match` 差在哪？ {#q14}
**Tags:** `occasional` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

Go type switch 针对接口动态类型；Rust `match` 针对静态已知的模式（尤其 enum），并能强制穷尽。

**解答：**

接口开放集合用 trait 对象 + downcast 才略像 type switch；封闭集合优先 enum。Rust 更少在运行期问“你到底是谁”。

```rust
enum Event {
    Click { x: i32, y: i32 },
    Key(char),
}

fn handle(e: Event) {
    match e {
        Event::Click { x, y } => println!("click {x},{y}"),
        Event::Key(c) => println!("key {c}"),
    }
}

fn main() {
    handle(Event::Key('a'));
}
```

```rust
fn main() {
    let any: &dyn std::fmt::Display = &1;
    println!("{any}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var v any = "hi"
	switch t := v.(type) {
	case string:
		fmt.Println("string", t)
	case int:
		fmt.Println("int", t)
	default:
		fmt.Println("other")
	}
}
```

- **Go 怎么做**：`any` + type switch。
- **Rust 为什么不同**：优先静态 enum/trait，少做动态类型分支。
- **Go 程序员易踩的坑**：把一切先擦成 `dyn Any` 再匹配。

---

## Q15. 哪些模式技巧初学者可以先跳过？ {#q15}
**Tags:** `advanced` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

先精通 `match`/`if let`/`let else`、引用匹配与穷尽性；`ref` 细节、复杂 `@`、高级 slice 模式、或模式里的盒子解引用可以后补。

**解答：**

优先清单：Option/Result 匹配、枚举变体、守卫 + 通配、避免长寿命借用。进阶清单：`box` 模式（稳定能力有限）、或-patterns 深层嵌套、宏生成模式等。

```rust
fn main() {
    let v = Some("hi");
    if let Some(s) = v {
        println!("{s}");
    }
}
```

```rust
fn main() {
    let n = 2;
    match n {
        1 | 2 | 3 => println!("small"),
        _ => println!("other"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 2
	switch n {
	case 1, 2, 3:
		fmt.Println("small")
	default:
		fmt.Println("other")
	}
}
```

- **Go 怎么做**：多 case 合并很常见。
- **Rust 为什么不同**：也有 `|` 或模式，但解包能力更强。
- **Go 程序员易踩的坑**：一上来钻冷门模式，基础穷尽性却不熟。

---

## Q16. 本章最值得背的匹配准则是什么？ {#q16}
**Tags:** `advanced` `pattern`
**适用版本:** Rust 1.0+

**一句话答案：**

先定匹配的是值还是引用；要穷尽就用 `match`；单模式用 `if let`/`let else`；守卫不能代替穷尽；绑定生命周期尽量短。

**解答：**

口诀：

1. 能 `&` 匹配就不按值掏 `String`。
2. 漏分支宁肯编译失败，也不要随手 `_ => todo!()` 吞掉。
3. `let else` 写卫语句。
4. `_` 才是不绑定；`_x` 仍可能 move。
5. 借用结束再改集合。

```rust
fn describe(v: Option<i32>) -> &'static str {
    match v {
        Some(x) if x < 0 => "neg",
        Some(0) => "zero",
        Some(_) => "pos",
        None => "none",
    }
}

fn main() {
    println!("{}", describe(Some(3)));
}
```

```rust
fn need(v: Option<i32>) -> i32 {
    let Some(n) = v else {
        return 0;
    };
    n
}

fn main() {
    println!("{}", need(Some(4)));
}
```

**Go 对比：**

```go
package main

import "fmt"

func need(ok bool, n int) int {
	if !ok {
		return 0
	}
	return n
}

func main() {
	fmt.Println(need(true, 4))
}
```

- **Go 怎么做**：if 早返回。
- **Rust 为什么不同**：模式系统把解包、分支、所有权绑在一起。
- **Go 程序员易踩的坑**：用 Go 的 switch 直觉硬套，忽略 move 与穷尽。

---

## Q17. or-pattern `A | B` 什么时候用？ {#q17}
**Tags:** `common` `pattern` `or-pattern`
**适用版本:** Rust 1.53+ 起 or-pattern 可在更多位置使用；`match` 臂里 `|` 从很早就有

**一句话答案：**

多个模式要跑**同一段逻辑**时，用 `A | B | C` 合并分支，避免复制粘贴；绑定的名字与类型在各或臂之间必须一致。

**解答：**

`match` 里最常见：

```rust
fn label(n: i32) -> &'static str {
    match n {
        1 | 2 | 3 => "small",
        4 | 5 => "mid",
        _ => "other",
    }
}

fn main() {
    println!("{}", label(2));
}
```

带绑定也行，但每个或支路要引入**同名**绑定：

```rust
enum Msg {
    Ping,
    Pong,
    Echo(i32),
    Note(i32),
}

fn num(m: &Msg) -> Option<i32> {
    match m {
        Msg::Echo(n) | Msg::Note(n) => Some(*n),
        Msg::Ping | Msg::Pong => None,
    }
}

fn main() {
    println!("{:?}", num(&Msg::Note(7)));
}
```

不要用 or-pattern「假装穷尽」却漏掉真正不同的处理；守卫仍要小心（见 [Q11](#q11)）。需要各分支不同逻辑时，老老实实分开写。

**Go 对比：**

```go
package main

import "fmt"

func label(n int) string {
	switch n {
	case 1, 2, 3:
		return "small"
	case 4, 5:
		return "mid"
	default:
		return "other"
	}
}

func main() {
	fmt.Println(label(2))
}
```

- **Go 怎么做**：`case 1, 2, 3:` 合并常量。
- **Rust 为什么不同**：`|` 还能合并带载荷的模式，并统一绑定。
- **Go 程序员易踩的坑**：以为只能合并常量，不敢在 enum 变体上写 `|`。

**记忆点：**

- 同逻辑多模式 → `A | B`。
- 绑定名要一致。
- 逻辑不同就别硬合并。

---

## Q18. 结构体模式 `Point { x, .. }` 怎么用？ {#q18}
**Tags:** `common` `pattern` `struct` `rest`
**适用版本:** Rust 1.0+

**一句话答案：**

在模式里按字段解包结构体；只关心部分字段时用 `..` 忽略其余，字段简写 `x` 等价于 `x: x`。

**解答：**

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn abs_x(p: Point) -> i32 {
    match p {
        Point { x, .. } => x.abs(), // 只要 x；y/z 丢掉（若非 Copy 则 move 掉）
    }
}

fn main() {
    let p = Point { x: -3, y: 1, z: 2 };
    println!("{}", abs_x(p));
}
```

按引用匹配，避免搬走：

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn sum_xy(p: &Point) -> i32 {
    let Point { x, y, .. } = p;
    x + y
}

fn main() {
    let p = Point { x: 1, y: 2, z: 9 };
    println!("{}", sum_xy(&p));
    println!("{}", p.z); // 仍可用
}
```

`..` 必须在模式里「吃掉」未写出的字段；字段都写全就不用 `..`。更新语法 `Point { x: 0, ..p }` 是**表达式**侧语法，和模式里的 `..` 别混。

**Go 对比：**

```go
package main

import "fmt"

type Point struct{ X, Y, Z int }

func absX(p Point) int {
	x := p.X
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	fmt.Println(absX(Point{X: -3, Y: 1, Z: 2}))
}
```

- **Go 怎么做**：字段选择用 `p.X`，没有结构体模式。
- **Rust 为什么不同**：模式里一次绑定多个字段，并可 `..` 忽略。
- **Go 程序员易踩的坑**：按值 `let Point { x, .. } = p` 后还以为整个 `p` 能用（非 `Copy` 时已部分/整体 move）。

**记忆点：**

- `Type { field, .. }` 只取关心的字段。
- 借用不想 move → 匹配 `&Type`。
- 模式 `..` ≠ 更新语法 `..base`。

---

## Q19. 函数参数里可以直接解构吗？ {#q19}
**Tags:** `common` `pattern` `function` `destructure`
**适用版本:** Rust 1.0+

**一句话答案：**

可以：参数位置也是模式，写 `fn f(Point { x, y }: Point)` 或 `fn g((a, b): (i32, i32))` 就能在入口拆开；要借用就解构引用。

**解答：**

```rust
struct Point {
    x: i32,
    y: i32,
}

fn dot(Point { x, y }: Point, Point { x: x2, y: y2 }: Point) -> i32 {
    x * x2 + y * y2
}

fn main() {
    let a = Point { x: 1, y: 2 };
    let b = Point { x: 3, y: 4 };
    println!("{}", dot(a, b));
}
```

只读借用、不 move：

```rust
struct Point {
    x: i32,
    y: i32,
}

fn mag2(&Point { x, y }: &Point) -> i32 {
    x * x + y * y
}

fn main() {
    let p = Point { x: 3, y: 4 };
    println!("{}", mag2(&p));
    println!("{} {}", p.x, p.y);
}
```

元组同样：`fn add((a, b): (i32, i32)) -> i32 { a + b }`。参数解构适合短函数；字段多、或还要整包 `p` 时，不如 `fn f(p: Point)` 再在体内取字段清晰。

**Go 对比：**

```go
package main

import "fmt"

type Point struct{ X, Y int }

func dot(a, b Point) int {
	return a.X*b.X + a.Y*b.Y
}

func main() {
	fmt.Println(dot(Point{1, 2}, Point{3, 4}))
}
```

- **Go 怎么做**：参数是完整值，字段在函数体内取。
- **Rust 为什么不同**：模式在 `let` / `match` / 参数处统一可用。
- **Go 程序员易踩的坑**：参数按值解构后还想用整结构体，或忘了写成 `&Point { .. }: &Point`。

**记忆点：**

- 参数 = 模式，可直接拆 struct/tuple。
- 要保留原值 → 解构引用。
- 字段一多就改回普通参数名。

---
