+++
title = "10-控制流"
date = 2026-07-28T14:49:00+08:00
weight = 100
type = "docs"
description = "面向熟悉 Go 的开发者系统讲清 Rust 的 if、match、循环、标签与提前返回"
isCJKLanguage = true
draft = false

+++

# 控制流 (Control Flow)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会被 `if` 和 `match` 当表达式这一点绕晕，不知道什么时候需要 `else`？
- 你是否想知道：Go 里 `if`、`switch`、`for` 很直观，为什么 Rust 这里多了 `if let`、`let ... else`、`while let`？
- 你是否遇到过 `error[E0308]`、`error[E0004]`，却看不懂它其实是在提醒什么控制流问题？
- 你会不会写出"看起来像 Go，实际上把值 move 走了"的 `match` 或 `for`？
- 你是否想搞懂 `loop` 为什么能返回值、标签循环又该在什么场景下用？
- 你是否希望有一份"我该用 `if`、`match`、`if let`、`while let`、`?` 中哪个"的速查手册？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| control flow | — | 控制流 | 决定代码按什么路径执行、何时分支、循环或提前结束 | `if` / `switch` / `for` / `return` |
| expression | — | 表达式 | 会计算出一个值的语法单元 | Go 的表达式 |
| statement | — | 语句 | 执行动作但不直接产出值的语法单元 | Go 的语句 |
| branch | — | 分支 | `if` / `match` 中不同的执行路径 | `if` / `switch` 分支 |
| pattern | — | 模式 | 用来匹配值形状的语法，如 `Some(x)`、`0..=9` | `switch` case + 类型断言，近似但不等价 |
| pattern matching | — | 模式匹配 | 按值的结构而非只按真假做分支 | Go 无完整对应物 |
| destructuring | — | 解构 | 在匹配时把元组、结构体、枚举内部字段拆出来 | 多重赋值 / type switch，近似 |
| exhaustiveness | — | 穷尽性 | 编译器要求 `match` 覆盖所有可能情况 | Go `switch` 不强制 |
| wildcard pattern | — | 通配模式 | `_`，表示"别管具体值，只要兜底" | `default` |
| match guard | — | 匹配守卫 | `match` 分支后追加 `if 条件` 的过滤逻辑 | `switch` case 后手写条件，近似 |
| diverging expression | — | 发散表达式 | 不会回到当前位置的表达式，如 `return`、`panic!`、无限 `loop` | `return` / `panic` |
| never type | `!` | 永不返回类型 | 表示这段代码不会产出正常值 | Go 无对应类型 |
| enum | enumeration | 枚举 | 一种可列举变体的类型，常与 `match` 配合 | `const` + 接口模式，近似 |
| `Option<T>` | — | 可选值 | 不是 `Some(T)` 就是 `None`，显式表示"可能没有值" | `(T, ok)` 惯用法 |
| `Result<T, E>` | — | 结果类型 | 不是 `Ok(T)` 就是 `Err(E)`，显式表示"可能失败" | `(T, error)` |
| iterator | — | 迭代器 | 一个一个产出元素的对象，`for` 实际遍历的是它 | `range` 背后的迭代过程，近似 |
| `IntoIterator` | — | 可转迭代器 trait | 表示一个类型可以被 `for ... in ...` 遍历 | 可被 `range` 的对象，近似 |
| `if let` | — | 单分支匹配 | 只关心某一种模式时的简写 | `if x, ok := ...; ok {}`，近似 |
| `while let` | — | 条件匹配循环 | 只要某种模式持续匹配就一直循环 | `for { v, ok := ...; if !ok { break } }` |
| `let ... else` | — | 失败即退出绑定 | 模式不匹配时立刻走 `else` 并提前退出当前路径 | Go 无直接对应物 |
| label | — | 标签 | 给循环或块起名，便于跨层 `break`/`continue` | `break Outer` |
| move | — | 移动 / 转移 | 所有权从一个变量转给另一个，旧变量失效 | Go 赋值后原变量仍可用，不等价 |
| borrow | — | 借用 | 临时按引用访问一个值而不接管所有权 | 指针 / slice 头共享，近似 |
| **RAII** | Resource Acquisition Is Initialization | 资源获取即初始化 | 用作用域结束自动清理资源的模式 | `defer` 手动模拟 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q17](#q17) |
| `common` | [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q18](#q18) |
| `occasional` | [Q14](#q14), [Q15](#q15) |
| `advanced` | [Q16](#q16) |

---

## Q1. Rust 的 `if` 为什么能写在 `let` 右边？ {#q1}
**Tags:** `hot` `beginner` `if` `expression`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 的 `if` 是**表达式**（expression，会计算出一个值），不是只会执行动作的语句；所以它可以直接放进 `let` 右边，但所有分支必须产出兼容的类型。

**解答：**

Go 程序员最先不适应的一点，就是 Rust 把很多看起来像"语句"的东西设计成了**表达式**（expression，表达式，会计算出一个值）。最常见的就是 `if`：

```rust
fn main() {
    let n = 8;
    let label = if n % 2 == 0 { "even" } else { "odd" };
    println!("{label}");
}
```

因为 `if` 有值，所以你可以把它嵌到更大的表达式里：

```rust
fn main() {
    let debug = true;
    let port = 8000 + if debug { 1 } else { 0 };
    println!("{port}");
}
```

当你把 `if` 当表达式用时，两个分支要么类型一致，要么有一个分支是**发散表达式**（diverging expression，不会回到当前位置的表达式），比如 `return`、`panic!` 或无限 `loop`。这也是为什么下面这种写法能过：

```rust
fn positive_name(n: i32) -> &'static str {
    let name = if n > 0 {
        "positive"
    } else {
        return "non-positive"; // 发散：不会回到 let 的当前位置
    };
    name
}

fn main() {
    println!("{}", positive_name(3));
    println!("{}", positive_name(-1));
}
```

「❌ 错误写法」——条件不是 `bool`，Rust 不接受"非零即真"：

```rust
fn main() {
    let n = 1;
    if n {
        println!("yes");
    }
    // error[E0308]: mismatched types
    //   expected `bool`, found integer
}
```

编译器拒绝它，是因为 Rust 不想替你猜测条件判断的意图。`if n` 在 C 系语言里表示"非零即真"，但这很容易把数字和布尔语义混在一起。Rust 逼你写成显式判断：

```rust
fn main() {
    let n = 1;
    if n != 0 {
        println!("yes");
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 8

	// Go 的 if 不是表达式，不能直接写在赋值右侧。
	label := "odd"
	if n%2 == 0 {
		label = "even"
	}

	fmt.Println(label)
}
```

- **Go 怎么做**：先声明变量，再在 `if` 分支里给它赋值。
- **Rust 为什么不同**：Rust 倾向让分支直接产出值，减少"先声明、后补值"这种临时可变状态。
- **Go 程序员易踩的坑**：看见 `if` 能写在 `let` 右边就很兴奋，但别忘了分支类型必须统一；这个坑见 [Q2](#q2)。

**记忆点：**

- Rust 的 `if` 是表达式，所以能返回值。
- 条件必须是 `bool`，Rust 不做隐式真假转换。
- 当表达式用时，要么所有分支类型一致，要么某个分支发散。

---

## Q2. 为什么 `if` 少了 `else` 就会报错？ {#q2}
**Tags:** `hot` `beginner` `if` `E0317`
**适用版本:** Rust 1.0+

**一句话答案：**

把 `if` 当表达式用时，如果没有 `else`，那它的值就是 `()`；因此你把它赋给别的类型时，通常会得到 `error[E0317]` 或相关的类型不匹配报错。

**解答：**

Rust 里单独写一个 `if` 没问题，因为那时你只是把它当控制语句来执行：

```rust
fn main() {
    let debug = true;
    if debug {
        println!("verbose log");
    }
}
```

但只要你把它塞进 `let` 右边，它就必须给出一个值。没有 `else` 时，`if 条件为假` 那条路径没有值，于是整个 `if` 会被视为 `()`（unit，单元类型，表示"没有有意义的值"）：

```rust
fn main() {
    let debug = true;
    let result: () = if debug {
        println!("only side effect");
    };
    result
}
```

这就是为什么下面这段会出错：

```rust
fn main() {
    let debug = false;
    let level = if debug {
        1
    };
    println!("{level}");
    // error[E0317]: `if` may be missing an `else` clause
    //   expected integer, found `()`
}
```

编译器的意思不是"语法不合法"，而是"你想把一个可能产出 `()` 的表达式，当成 `i32` 来用"。修法通常有两种：补 `else`，或者别把它当表达式用。

```rust
fn main() {
    let debug = false;
    let level = if debug { 1 } else { 0 };
    println!("{level}");
}
```

```rust
fn main() {
    let debug = false;
    let mut level = 0;
    if debug {
        level = 1;
    }
    println!("{level}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	debug := false
	level := 0
	if debug {
		level = 1
	}
	fmt.Println(level)
}
```

- **Go 怎么做**：Go 的 `if` 根本不返回值，所以天然不存在"少了 `else`"这个表达式问题。
- **Rust 为什么不同**：Rust 允许 `if` 产值，但也因此需要你把所有路径补完整。
- **Go 程序员易踩的坑**：想用 Rust 的表达式风格减少可变变量，却忘了给假分支一个值。

**记忆点：**

- `if` 当语句用，可以没有 `else`。
- `if` 当表达式用，通常必须有 `else`。
- 报 `E0317` 时，先检查是否漏了 `else`。

---

## Q3. `if let` 和 `match` 到底怎么选？ {#q3}
**Tags:** `hot` `beginner` `if-let` `match`
**适用版本:** Rust 1.0+

**一句话答案：**

只关心一种模式时用 `if let`；需要覆盖所有情况、或要写多分支解构时用 `match`。`if let` 是"只挑一支看"的简写，不是另一套语义。

**解答：**

`if let` 适合处理 **模式**（pattern，用来匹配值形状的语法）里"我只在乎一种成功情况"的场景，比如 `Option<T>`（可选值，不是 `Some(T)` 就是 `None`）：

```rust
fn main() {
    let user = Some("alice");

    if let Some(name) = user {
        println!("hello, {name}");
    }
}
```

同一件事用 `match` 写，也完全正确，只是更啰嗦：

```rust
fn main() {
    let user = Some("alice");

    match user {
        Some(name) => println!("hello, {name}"),
        None => {}
    }
}
```

一旦你既关心成功，也关心失败，或者分支不止两个，`match` 往往更清楚：

```rust
fn main() {
    let code = Some(404);

    match code {
        Some(200) => println!("ok"),
        Some(n) => println!("other status: {n}"),
        None => println!("missing"),
    }
}
```

「❌ 错误写法」——以为 `if let` 会自动处理失败情况：

```rust
fn main() {
    let value: Option<i32> = None;

    let n = if let Some(x) = value {
        x
    };
    println!("{n}");
    // error[E0317]: `if` may be missing an `else` clause
    //   expected integer, found `()`
}
```

`if let` 本质上还是 `if`，只是条件位置换成了模式匹配。你把它当表达式用，就一样要考虑 `else` 这条路的值：

```rust
fn main() {
    let value: Option<i32> = None;

    let n = if let Some(x) = value { x } else { 0 };
    println!("{n}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	value, ok := map[string]int{"alice": 1}["alice"]
	if ok {
		fmt.Println(value)
	}
}
```

- **Go 怎么做**：常用 `v, ok := ...; if ok { ... }` 处理"只关心成功"。
- **Rust 为什么不同**：Rust 把"成功/失败"编码进 `Option` 或 `Result` 的形状里，所以 `if let` 是按模式拆值，不是看一个单独的 `ok` 布尔。
- **Go 程序员易踩的坑**：把 `if let` 误解成"带解包能力的 if"，从而忘记它在表达式位置同样需要 `else`。

**记忆点：**

- `if let` = 我只关心一个模式。
- `match` = 我要显式处理全部情况。
- `if let` 本质上还是 `if`，放在表达式位置就得考虑 `else`。

---

## Q4. `let ... else` 是干什么的？为什么 `else` 里必须退出？ {#q4}
**Tags:** `hot` `beginner` `let-else` `E0308`
**适用版本:** `let ... else` 需 Rust 1.65+

**一句话答案：**

`let ... else` 适合"模式不匹配就立刻退出当前路径"；它的 `else` 必须是**发散表达式**，否则变量就会处于"可能没绑定成功"的尴尬状态。

**解答：**

`let ... else` 很适合做输入校验、提早失败和早返回：

```rust
fn parse_port(s: &str) -> Option<u16> {
    let Ok(port) = s.parse::<u16>() else {
        return None;
    };
    Some(port)
}

fn main() {
    println!("{:?}", parse_port("8080"));
    println!("{:?}", parse_port("oops"));
}
```

如果你用 `if let` 也能写，但会多一层缩进：

```rust
fn parse_port(s: &str) -> Option<u16> {
    if let Ok(port) = s.parse::<u16>() {
        Some(port)
    } else {
        None
    }
}

fn main() {
    println!("{:?}", parse_port("8080"));
}
```

`let ... else` 的关键限制是：`else` 必须结束当前控制流，比如 `return`、`break`、`continue`、`panic!`。因为一旦模式失败，后面就不该继续假装变量已经绑定好了。

```rust
fn first_char(s: &str) -> char {
    let Some(ch) = s.chars().next() else {
        panic!("empty string");
    };
    ch
}

fn main() {
    println!("{}", first_char("rust"));
}
```

「❌ 错误写法」——`else` 不发散：

```rust
fn parse_port(s: &str) -> u16 {
    let Ok(port) = s.parse::<u16>() else {
        println!("bad port");
    };
    port
    // error[E0308]: `else` clause of `let...else` does not diverge
    // help: try adding a diverging expression, such as `return` or `panic!(..)`
}
```

修法就是让失败路径真正结束：

```rust
fn parse_port(s: &str) -> u16 {
    let Ok(port) = s.parse::<u16>() else {
        println!("bad port");
        return 0;
    };
    port
}

fn main() {
    println!("{}", parse_port("80"));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func parsePort(s string) int {
	port, err := strconv.Atoi(s)
	if err != nil {
		return 0
	}
	return port
}

func main() {
	fmt.Println(parsePort("80"))
}
```

- **Go 怎么做**：`x, err := ...; if err != nil { return ... }`。
- **Rust 为什么不同**：Rust 直接在模式里写出"我只接受 `Ok(port)`"，失败路径单独放进 `else`。
- **Go 程序员易踩的坑**：以为 `else` 里打印一句日志就够了；不行，因为 Rust 需要证明下面的 `port` 一定已经绑定成功。

**记忆点：**

- `let ... else` = 成功继续，失败立刻走人。
- `else` 必须发散，否则变量可能根本没值。
- 输入校验和早返回场景，用它往往比 `if let` 更平。

---

## Q5. `match` 为什么老逼我把所有分支写全？ {#q5}
**Tags:** `hot` `beginner` `match` `E0004`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 Rust 的 `match` 要求**穷尽性**（exhaustiveness，覆盖所有可能情况）；这是它帮你在编译期堵住漏分支 bug 的重要能力，不是啰嗦设计。

**解答：**

最基础的 `match` 写法如下：

```rust
fn classify(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1..=9 => "small",
        _ => "other",
    }
}

fn main() {
    println!("{}", classify(3));
}
```

它比 Go `switch` 更强的地方，是可以直接按**模式匹配**（pattern matching，按值的结构做匹配），而不是只按一个值做等号判断。比如枚举：

```rust
enum Light {
    Red,
    Yellow,
    Green,
}

fn action(light: Light) -> &'static str {
    match light {
        Light::Red => "stop",
        Light::Yellow => "wait",
        Light::Green => "go",
    }
}

fn main() {
    println!("{}", action(Light::Green));
}
```

如果你漏掉一种情况，编译器会立刻指出来：

```rust
enum Light {
    Red,
    Yellow,
    Green,
}

fn action(light: Light) -> &'static str {
    match light {
        Light::Red => "stop",
        Light::Green => "go",
    }
    // error[E0004]: non-exhaustive patterns: `Light::Yellow` not covered
}

fn main() {
    println!("{}", action(Light::Red));
}
```

修法通常有两种：真的把每种情况写出来，或者明确承认"其他情况我不在乎"，用 `_` 兜底：

```rust
enum Light {
    Red,
    Yellow,
    Green,
}

fn action(light: Light) -> &'static str {
    match light {
        Light::Red => "stop",
        _ => "go or wait",
    }
}

fn main() {
    println!("{}", action(Light::Yellow));
}
```

**Go 对比：**

```go
package main

import "fmt"

type Light int

const (
	Red Light = iota
	Yellow
	Green
)

func action(light Light) string {
	switch light {
	case Red:
		return "stop"
	case Green:
		return "go"
	default:
		return "go or wait"
	}
}

func main() {
	fmt.Println(action(Yellow))
}
```

- **Go 怎么做**：`switch` 默认不强制穷尽，漏掉分支通常靠测试才能发现。
- **Rust 为什么不同**：Rust 把"是否覆盖所有可能情况"当成类型安全的一部分，在编译期就检查。
- **Go 程序员易踩的坑**：一看到 Rust 要补 `None`、补枚举所有变体，就想用 `_` 一把梭；但这会失去编译器帮你兜底的价值。

**记忆点：**

- `match` 要求穷尽性，这是一种保护。
- 不想细分时可用 `_`，但会降低未来重构时的提醒能力。
- 枚举越常变动，越值得少用 `_`、多写具体分支。

---

## Q6. `match` 不只是 `switch` 吧？它到底能解构到什么程度？ {#q6}
**Tags:** `hot` `beginner` `match` `destructuring`
**适用版本:** Rust 1.0+

**一句话答案：**

对，`match` 的核心不是"多路分支"，而是**按结构解构值**；它能同时匹配字面量、范围、元组、结构体、枚举和嵌套组合。

**解答：**

先看元组解构：

```rust
fn main() {
    let point = (0, 7);

    match point {
        (0, y) => println!("on y-axis: {y}"),
        (x, 0) => println!("on x-axis: {x}"),
        (x, y) => println!("({x}, {y})"),
    }
}
```

结构体也能直接拆字段：

```rust
struct User {
    name: String,
    active: bool,
}

fn main() {
    let user = User {
        name: String::from("alice"),
        active: true,
    };

    match user {
        User { active: true, name } => println!("active: {name}"),
        User {
            active: false,
            name,
        } => println!("inactive: {name}"),
    }
}
```

带数据的枚举更是 `match` 的主战场：

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

fn main() {
    let msg = Message::Move { x: 3, y: 4 };

    match msg {
        Message::Quit => println!("quit"),
        Message::Move { x, y } => println!("move to ({x}, {y})"),
        Message::Write(text) => println!("text: {text}"),
    }
}
```

常见误区是：以为 `match` 只能像 Go `switch` 那样"看一个值等于啥"。其实它直接帮你完成了解包动作，所以很多原本要写多层 `if`、多次取字段的代码，在 Rust 里都能压进一个 `match`。

**Go 对比：**

```go
package main

import "fmt"

type Move struct {
	X int
	Y int
}

func main() {
	msg := Move{X: 3, Y: 4}

	switch {
	case msg.X == 0:
		fmt.Println("on y-axis")
	default:
		fmt.Printf("move to (%d, %d)\n", msg.X, msg.Y)
	}
}
```

- **Go 怎么做**：通常是 `switch` 配合字段访问、类型断言或手写条件。
- **Rust 为什么不同**：Rust 的枚举和模式系统是语言核心，所以分支和解构天然绑在一起。
- **Go 程序员易踩的坑**：把 `match` 当成"语法更重的 switch"，就会错过它最值钱的结构化解构能力。

**记忆点：**

- `match` 最强的地方是解构，不只是分支。
- 元组、结构体、枚举都能直接拆。
- 写控制流前先想：我要判断的只是值，还是值的形状？

---

## Q7. `loop`、`while`、`for` 我该怎么选？ {#q7}
**Tags:** `hot` `beginner` `loop` `for`
**适用版本:** Rust 1.0+

**一句话答案：**

遍历集合优先 `for`，按布尔条件反复执行用 `while`，需要"无限循环 + 手动决定何时返回值"时用 `loop`；大多数 Go 风格 `for` 在 Rust 里都能拆进这三类之一。

**解答：**

`for` 最常见，用来遍历 **iterator**（迭代器，一个一个产出元素的对象）：

```rust
fn main() {
    for x in [10, 20, 30] {
        println!("{x}");
    }
}
```

`while` 适合"只要条件为真就继续"：

```rust
fn main() {
    let mut n = 3;
    while n > 0 {
        println!("{n}");
        n -= 1;
    }
}
```

`loop` 则是最原始的无限循环，它的独特价值是可以 `break` 一个值出来：

```rust
fn main() {
    let mut n = 0;
    let found = loop {
        n += 1;
        if n == 3 {
            break n * 10;
        }
    };

    println!("{found}");
}
```

很多刚从 Go 过来的人会下意识想写 C/Go 风格三段式循环，但 Rust 没有 `for init; cond; post` 这个语法。你得换成 `while` 或迭代器风格：

```rust
fn main() {
    let mut i = 0;
    while i < 3 {
        println!("{i}");
        i += 1;
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	for i := 0; i < 3; i++ {
		fmt.Println(i)
	}

	n := 0
	for {
		n++
		if n == 3 {
			break
		}
	}
}
```

- **Go 怎么做**：Go 只有一个 `for`，语法上同时承担 `while`、无限循环和三段式循环三种角色。
- **Rust 为什么不同**：Rust 把三种意图分开写，读代码时更容易一眼看出"这是遍历、条件循环，还是显式控制退出点"。
- **Go 程序员易踩的坑**：一上来想找三段式 `for`；找不到不是遗漏，而是语言故意不用这种写法。

**记忆点：**

- 遍历集合：优先 `for`。
- 条件循环：用 `while`。
- 需要 `break value`：用 `loop`。

---

## Q8. `break`、`continue` 和标签循环该怎么用？ {#q8}
**Tags:** `common` `loop` `label`
**适用版本:** Rust 1.0+

**一句话答案：**

`break` 结束当前循环，`continue` 跳到下一轮；多层循环想跳出外层时，用标签（label）明确指出要操作哪一层。

**解答：**

最基础的 `break` / `continue`：

```rust
fn main() {
    for n in 0..5 {
        if n == 2 {
            continue;
        }
        if n == 4 {
            break;
        }
        println!("{n}");
    }
}
```

`loop` 还能 `break` 一个值：

```rust
fn main() {
    let mut n = 0;
    let answer = loop {
        n += 1;
        if n == 5 {
            break n * 2;
        }
    };
    println!("{answer}");
}
```

嵌套循环里，如果你想跳出外层，必须加标签：

```rust
fn main() {
    'outer: for row in 0..3 {
        for col in 0..3 {
            if row + col == 3 {
                break 'outer;
            }
            println!("{row}, {col}");
        }
    }
}
```

不写标签时，`break` 只会结束最内层循环。这通常不是编译错误，而是沉默的逻辑 bug，所以要靠你自己表达清楚意图。

**Go 对比：**

```go
package main

import "fmt"

func main() {
Outer:
	for row := 0; row < 3; row++ {
		for col := 0; col < 3; col++ {
			if row+col == 3 {
				break Outer
			}
			fmt.Println(row, col)
		}
	}
}
```

- **Go 怎么做**：Go 也支持标签 `break Outer` / `continue Outer`。
- **Rust 为什么不同**：Rust 的标签语法写成 `'outer:`，和生命周期的写法长得像，但这是两套不同概念。
- **Go 程序员易踩的坑**：看到前导单引号就误以为这里和生命周期有关；在循环标签场景，它只是控制流标签。

**记忆点：**

- `break` / `continue` 默认只作用于最内层循环。
- 跨层跳转就给循环起名字。
- `loop` 是唯一最常用的 `break value` 场景。

---

## Q9. `while let` 有什么用？为什么不用普通 `while`？ {#q9}
**Tags:** `common` `while-let` `Option`
**适用版本:** Rust 1.0+

**一句话答案：**

`while let` 适合"只要某个模式持续匹配就继续循环"；处理 `Option`、`Result`、迭代弹栈这类场景时，它比 `loop + match` 更短也更清楚。

**解答：**

最典型的例子就是不停 `pop()` 直到拿到 `None`：

```rust
fn main() {
    let mut stack = vec![1, 2, 3];

    while let Some(top) = stack.pop() {
        println!("{top}");
    }
}
```

同样的逻辑用 `loop + match` 也能写，只是更啰嗦：

```rust
fn main() {
    let mut stack = vec![1, 2, 3];

    loop {
        match stack.pop() {
            Some(top) => println!("{top}"),
            None => break,
        }
    }
}
```

它也适合不断读取成功值、失败就停：

```rust
fn main() {
    let mut words = ["1", "2", "oops"].into_iter();

    while let Some(Ok(n)) = words.next().map(|s| s.parse::<i32>()) {
        println!("{n}");
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	stack := []int{1, 2, 3}
	for len(stack) > 0 {
		top := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		fmt.Println(top)
	}
}
```

- **Go 怎么做**：Go 常用 `for len(stack) > 0 { ... }`，或者拿到 `(v, ok)` 后手动 `break`。
- **Rust 为什么不同**：Rust 常把"有值/没值"编码成 `Option` 的模式，所以 `while let` 可以直接把条件和解构绑在一起。
- **Go 程序员易踩的坑**：先写一层 `while condition`，再在循环体里 `match`；其实可以直接收缩成 `while let`。

**记忆点：**

- `while let` = 只要模式匹配成功就继续。
- `Option` / `Result` 连续消费场景优先考虑它。
- 它基本就是 `loop + match + break` 的语法糖。

---

## Q10. `for x in v`、`for x in &v`、`for x in &mut v` 差在哪？ {#q10}
**Tags:** `common` `for` `iterator` `move`
**适用版本:** Rust 1.0+

**一句话答案：**

`for x in v` 会消费集合，`for x in &v` 是只读借用，`for x in &mut v` 是可变借用；差别不在循环本身，而在 `for` 背后调用了哪个 `IntoIterator` 实现。

**解答：**

先看最容易理解的只读遍历：

```rust
fn main() {
    let v = vec![10, 20, 30];

    for x in &v {
        println!("{x}");
    }

    println!("{v:?}"); // v 还在
}
```

可变遍历时，循环变量是 `&mut T`，所以要解引用修改：

```rust
fn main() {
    let mut v = vec![1, 2, 3];

    for x in &mut v {
        *x *= 10;
    }

    println!("{v:?}");
}
```

按值遍历则会把元素所有权拿走。对 `Vec<T>` 来说，整个 `Vec` 也会被消费：

```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];

    for s in v {
        println!("{s}");
    }
}
```

「❌ 错误写法」——按值遍历后还想再用原集合：

```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];

    for s in v {
        println!("{s}");
    }

    println!("{v:?}");
    // error[E0382]: borrow of moved value: `v`
}
```

如果你只想读，不想把 `v` 搬走，改成借用版本即可：

```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];

    for s in &v {
        println!("{s}");
    }

    println!("{v:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []string{"a", "b"}

	for _, s := range v {
		fmt.Println(s)
	}

	fmt.Println(v) // range 后原 slice 仍然可用
}
```

- **Go 怎么做**：`range` 遍历 slice 时，不会把整个 slice "消费掉"。
- **Rust 为什么不同**：Rust 要同时表达"我要读、我要改、我要拿走所有权"这三种意图，所以 `for` 遍历方式被编码进了借用形式里。
- **Go 程序员易踩的坑**：看到 `for s in v` 就按 Go 习惯理解成"取元素副本"，结果把 `v` 整个 move 没了。

**记忆点：**

- `v`：消费。
- `&v`：只读借用。
- `&mut v`：可变借用。

---

## Q11. 为什么边遍历 `Vec` 边 `push` 会报借用错误？ {#q11}
**Tags:** `common` `for` `E0502` `borrow`
**适用版本:** Rust 1.0+

**一句话答案：**

因为迭代器已经借用了集合，再去 `push` 需要另一个可变借用；而且 `Vec` 扩容时还可能搬家，所以 Rust 用 `error[E0502]` 阻止你制造悬空引用或遍历失效。

**解答：**

先看错误场景：

```rust
fn main() {
    let mut values = vec![1, 2, 3];

    for x in &values {
        values.push(*x);
    }
    // error[E0502]: cannot borrow `values` as mutable because it is also borrowed as immutable
}
```

这里 `for x in &values` 已经创建了一个对 `values` 的不可变借用，整个循环期间都有效；而 `push` 需要可变借用。Rust 的规则是：同一时间要么多个只读借用，要么唯一一个可变借用，不能混用。

更深一层原因是 `Vec` 底层可能扩容。扩容时，原来的元素可能被搬到新的内存位置；如果迭代器还拿着旧位置，就会出问题。

正确做法通常是先收集，再修改：

```rust
fn main() {
    let mut values = vec![1, 2, 3];
    let additions: Vec<i32> = values.iter().copied().collect();

    values.extend(additions);
    println!("{values:?}");
}
```

如果你的目标是"原地修改每个元素"，那就用 `iter_mut()` 或 `for x in &mut values`，而不是结构性地增删元素：

```rust
fn main() {
    let mut values = vec![1, 2, 3];

    for x in &mut values {
        *x *= 2;
    }

    println!("{values:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	values := []int{1, 2, 3}
	for _, x := range values {
		values = append(values, x)
	}
	fmt.Println(values)
}
```

- **Go 怎么做**：Go 允许你 `range` 时 `append`，但行为细节容易依赖底层数组是否扩容，可读性和可预期性并不总是好。
- **Rust 为什么不同**：Rust 直接把这类"遍历视图可能失效"的问题挡在编译期，而不是让你靠经验记住边界行为。
- **Go 程序员易踩的坑**：把 Rust 里的借用错误当成"限制太多"；其实它是在防止你边走边拆地板。

**记忆点：**

- 遍历期间别结构性修改同一个 `Vec`。
- 要追加：先收集，再 `extend`。
- 要原地改值：用 `&mut`。

---

## Q12. `match` 里为什么一不小心就把值 move 走了？ {#q12}
**Tags:** `common` `match` `move` `E0382`
**适用版本:** Rust 1.0+

**一句话答案：**

`match value` 是按值匹配，分支里的绑定通常会把内部字段 move 出来；如果你只是想看，不想拿走所有权，就匹配 `&value` 或在模式里借用。

**解答：**

按值匹配 `Option<String>` 时，里面的 `String` 会被拿走：

```rust
fn main() {
    let name = Some(String::from("alice"));

    match name {
        Some(s) => println!("{s}"),
        None => {}
    }
}
```

如果后面还想用 `name`，这就会出问题：

```rust
fn main() {
    let name = Some(String::from("alice"));

    match name {
        Some(s) => println!("{s}"),
        None => {}
    }

    println!("{name:?}");
    // error[E0382]: borrow of partially moved value: `name`
    // note: partial move occurs because value has type `String`, which does not implement the `Copy` trait
}
```

只读场景下，最简单的修法是匹配引用：

```rust
fn main() {
    let name = Some(String::from("alice"));

    match &name {
        Some(s) => println!("{s}"),
        None => {}
    }

    println!("{name:?}");
}
```

或者更常见地直接用 `if let Some(s) = &name`：

```rust
fn main() {
    let name = Some(String::from("alice"));

    if let Some(s) = &name {
        println!("{s}");
    }

    println!("{name:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	name := "alice"
	copyOfHeader := name
	fmt.Println(copyOfHeader)
	fmt.Println(name) // 仍可用
}
```

- **Go 怎么做**：赋值或传参后原变量一般还在，尤其字符串、slice、map 这种头部复制的类型更容易让人形成这种习惯。
- **Rust 为什么不同**：Rust 要精确区分"读一眼"和"把里面那份值拿出来归我"，`match` 默认尊重按值语义。
- **Go 程序员易踩的坑**：把 `match name { Some(s) => ... }` 当成"只是解包看看"，但它其实是在转移所有权。

**记忆点：**

- `match value` 可能 move。
- 只读查看时，优先 `match &value`。
- 看到 `E0382`，先查自己是不是在模式里拿走了内部值。

---

## Q13. `return`、`break` 和 `?` 都是提前结束，它们分别结束哪一层？ {#q13}
**Tags:** `common` `return` `question-mark`
**适用版本:** Rust 1.0+

**一句话答案：**

`break` 结束循环，`return` 结束函数，`?` 在失败时等价于"提前 `return Err(...)` 或 `return None`"；它们不是同一级别的退出。

**解答：**

先看 `break` 和 `return` 的区别：

```rust
fn demo() {
    for n in 0..3 {
        if n == 1 {
            break; // 只退出 for
        }
        println!("{n}");
    }

    println!("after loop");
}

fn main() {
    demo();
}
```

`return` 则直接结束整个函数：

```rust
fn first_even(values: &[i32]) -> Option<i32> {
    for &n in values {
        if n % 2 == 0 {
            return Some(n);
        }
    }
    None
}

fn main() {
    println!("{:?}", first_even(&[1, 3, 4, 5]));
}
```

`?` 的层级和 `return` 一样，只不过它只在失败时触发提前返回：

```rust
fn double_number(s: &str) -> Result<i32, std::num::ParseIntError> {
    let n: i32 = s.parse()?;
    Ok(n * 2)
}

fn main() {
    println!("{:?}", double_number("21"));
}
```

它不能在返回 `()` 的函数里直接用：

```rust
fn main() {
    let n: i32 = "12".parse()?;
    println!("{n}");
    // error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option`
}
```

改法是让函数本身返回 `Result`，或者把可失败逻辑放进单独函数：

```rust
fn main() -> Result<(), std::num::ParseIntError> {
    let n: i32 = "12".parse()?;
    println!("{n}");
    Ok(())
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func doubleNumber(s string) (int, error) {
	n, err := strconv.Atoi(s)
	if err != nil {
		return 0, err
	}
	return n * 2, nil
}

func main() {
	fmt.Println(doubleNumber("21"))
}
```

- **Go 怎么做**：靠 `if err != nil { return ... }` 手动提早返回。
- **Rust 为什么不同**：Rust 把这种模式做成了 `?`，让错误传播成为控制流的一部分。
- **Go 程序员易踩的坑**：把 `?` 误以为只会"跳出当前代码块"；其实它结束的是整个函数（或闭包/`try` 边界）。

**记忆点：**

- `break` 管循环。
- `return` 管函数。
- `?` = 失败时提前 `return`。

---

## Q14. `match guard` 是什么？为什么不用再套一层 `if`？ {#q14}
**Tags:** `occasional` `match` `guard`
**适用版本:** Rust 1.0+

**一句话答案：**

`match guard` 就是在模式后面再加一个 `if 条件`；它适合"先按形状匹配，再按额外条件过滤"的场景，比把逻辑拆成外层 `match` + 内层 `if` 更紧凑。

**解答：**

基础写法：

```rust
fn main() {
    let value = Some(5);

    match value {
        Some(x) if x % 2 == 0 => println!("even {x}"),
        Some(x) => println!("odd {x}"),
        None => println!("none"),
    }
}
```

如果不用 guard，你通常会把条件塞到分支内部：

```rust
fn main() {
    let value = Some(5);

    match value {
        Some(x) => {
            if x % 2 == 0 {
                println!("even {x}");
            } else {
                println!("odd {x}");
            }
        }
        None => println!("none"),
    }
}
```

guard 的意思是：模式先匹配，再看 `if` 条件是否成立；如果不成立，继续往后试别的分支。它不是额外开启一个新的 `if` 作用域。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	value := 5

	switch {
	case value%2 == 0:
		fmt.Println("even", value)
	default:
		fmt.Println("odd", value)
	}
}
```

- **Go 怎么做**：常见是 `switch { case cond: ... }` 或 `if/else`。
- **Rust 为什么不同**：Rust 想把"形状匹配"和"额外条件"写在同一条分支声明上。
- **Go 程序员易踩的坑**：guard 看起来像附加条件，但不要忘了它依赖前面的模式变量，比如这里的 `x`。

**记忆点：**

- guard 写法：`pattern if condition => ...`。
- 先匹配模式，再判断守卫条件。
- 适合"结构条件 + 值条件"同时存在的分支。

---

## Q15. 标签不只能标循环？普通块也能 `break` 出值？ {#q15}
**Tags:** `occasional` `label` `block`
**适用版本:** 块标签 `break value` 需 Rust 1.65+

**一句话答案：**

能。Rust 可以给普通代码块加标签，再用 `break 'label value` 提前从块里退出；它很适合替代"只执行一轮的假循环"。

**解答：**

最常见的是给一段多分支初始化逻辑收口：

```rust
fn parse_flag(s: &str) -> i32 {
    'done: {
        if s.is_empty() {
            break 'done -1;
        }
        if s == "on" {
            break 'done 1;
        }
        0
    }
}

fn main() {
    println!("{}", parse_flag("on"));
}
```

有些人会用 `loop` 来模拟这个效果，其实没必要：

```rust
fn parse_flag(s: &str) -> i32 {
    loop {
        if s.is_empty() {
            break -1;
        }
        if s == "on" {
            break 1;
        }
        break 0;
    }
}

fn main() {
    println!("{}", parse_flag(""));
}
```

块标签的好处是语义更准确：这里根本不是循环，只是一段可以提前退出的计算块。

**Go 对比：**

```go
package main

import "fmt"

func parseFlag(s string) int {
	if s == "" {
		return -1
	}
	if s == "on" {
		return 1
	}
	return 0
}

func main() {
	fmt.Println(parseFlag("on"))
}
```

- **Go 怎么做**：通常直接 `return`，或者拆成额外函数。
- **Rust 为什么不同**：Rust 的块本身就是表达式，所以可以成为一块可提前结束、能返回值的局部计算区域。
- **Go 程序员易踩的坑**：把块标签和循环标签混为一谈；块标签只能 `break`，不能 `continue`，因为它没有下一轮。

**记忆点：**

- 普通块也能贴标签。
- 块标签适合局部提前返回一个值。
- 这比"假装自己是循环"的 `loop` 更清晰。

---

## Q16. 发散表达式和 `!`（never type）到底是什么？ {#q16}
**Tags:** `advanced` `never-type` `diverging`
**适用版本:** `!` 相关行为在稳定版可用；细节以 Rust 1.97.1 为准

**一句话答案：**

`!`（never type，永不返回类型）表示"这段代码不会正常产出值"；正因为它永不返回，所以它能出现在任何需要某种类型的位置，常见于 `panic!`、`return`、无限 `loop`。

**解答：**

最容易看到它效果的地方，就是 `if` 或 `match` 分支类型看起来不一致，但其实能过：

```rust
fn get_name(flag: bool) -> &'static str {
    let name = if flag {
        "rust"
    } else {
        panic!("no name");
    };
    name
}

fn main() {
    println!("{}", get_name(true));
}
```

为什么 `&'static str` 和 `panic!()` 能放在同一个 `if` 里？因为 `panic!()` 的类型是 `!`，而 `!` 可以被看作"永远不会真的交出一个值"，所以不需要和另一边对齐成相同具体类型。

`match` 里也一样：

```rust
fn first(xs: &[i32]) -> i32 {
    match xs.first() {
        Some(&n) => n,
        None => panic!("empty slice"),
    }
}

fn main() {
    println!("{}", first(&[10, 20]));
}
```

无限 `loop` 也是发散表达式：

```rust
fn spin_forever() -> ! {
    loop {
        std::hint::spin_loop();
    }
}

fn main() {
    let _f: fn() -> ! = spin_forever;
}
```

理解这一点后，你就能更自然地看懂 [Q1](#q1) 里为什么 `else { return ... }` 可以和普通值分支共存，也能看懂 [Q4](#q4) 里为什么 `let ... else` 要求 `else` 发散。

**Go 对比：**

```go
package main

import "fmt"

func getName(flag bool) string {
	if flag {
		return "rust"
	}
	panic("no name")
}

func main() {
	fmt.Println(getName(true))
}
```

- **Go 怎么做**：Go 也有 `panic` 和无限循环，但没有一个显式的 `!` 类型把"永不返回"编码进类型系统。
- **Rust 为什么不同**：Rust 会把控制流事实纳入类型检查，所以 `!` 是类型系统里真实存在的一员。
- **Go 程序员易踩的坑**：把 `panic!` 只看成运行时行为，而忽略它还会影响分支的类型推导。

**记忆点：**

- `!` 表示永不正常返回。
- `panic!`、`return`、无限 `loop` 都是发散表达式。
- 它解释了很多"分支类型看起来不一致却能编译"的现象。

---

## Q17. `0..n` 和 `0..=n` 差在哪？空区间会怎样？ {#q17}
**Tags:** `hot` `beginner` `range` `for`
**适用版本:** Rust 1.0+

**一句话答案：**

`0..n` 是**半开区间**（不含 `n`），等价于 `0, 1, …, n-1`；`0..=n` 是**闭区间**（含 `n`）。若起点大于终点（对半开）或起点大于终点（对闭区间的空情况），区间为空，`for` 一轮都不会进。

**解答：**

最常见写法：

```rust
fn main() {
    let half: Vec<_> = (0..3).collect(); // 0, 1, 2
    let closed: Vec<_> = (0..=3).collect(); // 0, 1, 2, 3
    assert_eq!(half, vec![0, 1, 2]);
    assert_eq!(closed, vec![0, 1, 2, 3]);
}
```

`n` 为 0 时，`0..0` 是空的；`0..=0` 则只产出一个 `0`：

```rust
fn main() {
    assert_eq!((0..0).count(), 0);
    assert_eq!((0..=0).count(), 1);
    assert_eq!((5..5).count(), 0);
    assert_eq!((5..=4).count(), 0); // 起点大于终点 → 空
}
```

「❌ 易混」——按 Go/`for i := 0; i <= n; i++` 的直觉写 `0..n`，少迭代最后一个：

```rust
fn main() {
    let n = 3;
    let mut sum = 0;
    for i in 0..n {
        // 只有 0,1,2；若你本意是包含 n，应写 0..=n
        sum += i;
    }
    assert_eq!(sum, 3); // 0+1+2，不是 0+1+2+3
}
```

空区间是合法值，不会 panic；`for` 体直接跳过。切片下标常用 `0..v.len()`（半开），刚好覆盖合法下标且不含 `len`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	n := 3
	for i := 0; i < n; i++ { // 半开：0..n
		fmt.Println(i)
	}
	for i := 0; i <= n; i++ { // 闭：约等于 0..=n
		fmt.Println(i)
	}
}
```

- **Go 怎么做**：用 `i < n` / `i <= n` 表达开闭。
- **Rust 为什么不同**：区间类型把开闭写进语法，还能当迭代器直接 `collect`。
- **Go 程序员易踩的坑**：把 `0..n` 当成“到 n 为止含 n”。

**记忆点：**

- `a..b` 不含 `b`；`a..=b` 含 `b`。
- 空区间合法，循环体不执行。
- 下标遍历优先 `0..len`（半开）。

---

## Q18. `for` 里改正在迭代的集合，还有哪些雷？ {#q18}
**Tags:** `common` `for` `iterator` `borrow`
**适用版本:** Rust 1.0+

**一句话答案：**

除了 [Q11](#q11) 那种“边借边 `push` 被编译器直接拦住”之外，用**下标循环**删元素会跳项/越界，对 `HashMap` 边遍历边结构性修改也不安全；正确做法是先收集、再改，或用 `retain` / `extract_if` / `drain` 等专用 API。

**解答：**

借用迭代时，结构性修改多半编译不过（见 [Q11](#q11)）。更阴的是“编译过了，逻辑错了”——按下标边删边走：

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4, 5];
    let mut i = 0;
    while i < v.len() {
        if v[i] % 2 == 0 {
            v.remove(i); // 后面元素前移，i 不能 +1
        } else {
            i += 1;
        }
    }
    assert_eq!(v, vec![1, 3, 5]);
}
```

「❌ 错误写法」——删完还 `i += 1`，会跳过紧随其后的元素：

```rust
fn main() {
    let mut v = vec![2, 4, 6];
    let mut i = 0;
    while i < v.len() {
        v.remove(i);
        i += 1; // 删掉下标 0 后，原 4 挪到 0，却被跳过
    }
    // 结果往往剩元素，而不是清空
    assert_ne!(v.len(), 0);
}
```

批量按条件留下，优先 `retain`（不必手搓下标）：

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4, 5];
    v.retain(|x| x % 2 == 1);
    assert_eq!(v, vec![1, 3, 5]);
}
```

`HashMap`：持有 `iter()` 时再 `insert`/`remove` 同样会借冲突；要改结构就先收集键，或用 `retain`。`for` 消费集合（`for x in v`）则根本没有“原集合”可改——那是所有权问题，见 [Q10](#q10)。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3, 4, 5}
	out := v[:0]
	for _, x := range v {
		if x%2 == 1 {
			out = append(out, x)
		}
	}
	fmt.Println(out)
}
```

- **Go 怎么做**：常新建切片，或小心处理 `range` 时 append 的语义。
- **Rust 为什么不同**：借用检查挡住一大类；剩下的下标手改仍要自己防跳项。
- **Go 程序员易踩的坑**：以为“没用迭代器、改用下标就自由了”，结果删元素逻辑 silently 错。

**记忆点：**

- 借着迭代 → 别结构性改（[Q11](#q11)）。
- 下标删除 → 删后不要无脑 `i++`，或改用 `retain`。
- Map 边遍历边改 → 先收集键，或用专用 API。

