+++
title = "09-函数"
date = 2026-07-28T14:49:00+08:00
weight = 90
type = "docs"
description = "面向熟悉 Go 的读者讲清 Rust 函数签名、返回值、所有权、泛型与可调用对象差异"
isCJKLanguage = true
draft = false

+++

# 函数 (Functions)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会总把 Rust 函数当成 Go 的 `func` 来看，结果一写就撞上类型、分号、返回值规则？
- 你是否想知道：Rust 为什么没有 Go 那样的“多返回值”语法，却照样能优雅返回多项结果？
- 你会不会在“参数传进去以后变量怎么没了”这个问题上，被所有权和借用搞糊涂？
- 你是否分不清“函数项、函数指针、闭包”到底是不是一回事，什么时候能互相替代？
- 你是否想搞懂泛型函数、`impl Trait`、turbofish 到底各自解决什么问题？
- 你会不会遇到 `E0308`、`E0382`、`E0277` 这类函数相关报错，却看不出编译器在阻止什么坑？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| function | — | 函数 | 一段可复用的可调用代码，有参数、返回值和函数体 | `func` |
| signature | — | 函数签名 | 函数名、参数类型、返回类型这一层“接口” | `func f(a int) string` 的声明头 |
| parameter | — | 形参 | 函数定义时写在括号里的名字和类型 | 形参 |
| argument | — | 实参 | 调用函数时传进去的具体值 | 实参 |
| return type | — | 返回类型 | `-> T` 指明函数调用结束后交出的值类型 | Go 返回列表 |
| expression | — | 表达式 | 会产生一个值的代码片段，如 `1 + 2`、`if`、`match` | Go 普通表达式；但 Go 的 `if` 不是表达式 |
| statement | — | 语句 | 执行动作但不产出可继续使用的值 | Go 语句 |
| unit | — | 单元类型 | `()`，表示“没有有意义的数据” | `void` / 空结构用途接近 |
| owner | — | 所有者 | 当前负责在作用域结束时释放该值的绑定 | Go 无对应物 |
| move | — | 移动 / 转移所有权 | 把值的所有权交给新变量或函数，旧绑定随即失效 | Go 没有这条规则 |
| borrow | — | 借用 | 临时把值“借出去看”或“借出去改”，不转移所有权 | 传指针最像，但规则更严格 |
| `Copy` | — | 按位复制 trait | 标记赋值/传参时直接复制的小类型 | Go 大多数值类型的默认行为 |
| `Clone` | — | 克隆 trait | 显式复制一份新值，可能有堆分配成本 | 手写深拷贝 |
| tuple | — | 元组 | 固定长度、可异构的数据包，可当“多返回值替身” | Go 没有直接等价物 |
| generic | — | 泛型 | 用类型参数把一份函数逻辑复用到多种类型 | Go 1.18+ 泛型 |
| monomorphization | /məˌnɒməfɪˈkeɪʃən/ | 单态化 | 编译器把泛型函数按实际类型展开成多份具体代码 | Go 编译器也会做类似专门化/字典混合实现，但细节不同 |
| turbofish | `::<...>` | turbofish 语法 | 显式写出类型参数，帮助编译器推断 | Go 没有专门叫法 |
| `impl Trait` | — | `impl Trait` 语法 | 用 trait 约束“某个实现了该能力的类型”，可出现在参数或返回位置 | Go 接口参数最像 |
| trait | — | trait / 特征 | 一组方法或能力约束 | interface |
| function item | — | 函数项 | 某个已命名函数本身的零大小唯一类型 | 命名函数值 |
| function pointer | `fn(...) -> ...` | 函数指针类型 | 只指向函数代码、不捕获环境的可调用值 | `func(int) int` 最像 |
| closure | — | 闭包 | 能捕获外部环境的匿名可调用对象 | Go 闭包 |
| associated function | — | 关联函数 | 写在 `impl` 里但没有 `self` 的函数，常作构造器 | 类型上的普通函数 |
| method | — | 方法 | 第一个参数是 `self` / `&self` / `&mut self` 的函数 | 方法 |
| diverging function | — | 发散函数 | 永远不会正常返回到调用点的函数 | `panic` / 无限循环函数 |
| never type | `!` | never 类型 | 表示“这个表达式永远没有值返回” | Go 无对应物 |
| `const fn` | — | 常量函数 | 既可像普通函数调用，也可在常量上下文求值 | Go 没有对应语法 |
| variadic | — | 可变参数 | 参数个数可变的函数形式 | Go `...T` |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q19](#q19) |
| `common` | [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q20](#q20) |
| `occasional` | [Q16](#q16), [Q17](#q17) |
| `advanced` | [Q18](#q18) |

---

## Q1. Rust 函数最基本的写法是什么？为什么参数类型一个都不能省？ {#q1}
**Tags:** `hot` `beginner` `fn`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 用 `fn 名字(参数: 类型, ...) -> 返回类型 { ... }` 定义函数；参数类型必须全部写明，因为函数签名是公开契约，Rust 不在这里做 Go 式的“从用法反推参数类型”。

**解答：**

先看最小可用写法。这里的**函数签名**（signature，函数名、参数类型、返回类型这一层接口）由 `fn add(a: i32, b: i32) -> i32` 构成：

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn greet(name: &str) {
    println!("hello, {name}");
}

fn main() {
    println!("{}", add(2, 3));
    greet("Rust");
}
```

无返回值函数的真实返回类型其实是 **单元类型**（unit）`()`，只是经常省略：

```rust
fn log_number(n: i32) -> () {
    println!("n = {n}");
}

fn main() {
    let value: () = log_number(7);
    assert_eq!(value, ());
}
```

「❌ 错误写法」——把 Go 的“同类型参数挤在一起写”带过来：

```rust
fn main() {
    // fn add(a, b: i32) -> i32 { a + b }
    // error: expected parameter name, found `:`
    // 在 Rust 里，每个参数都必须单独写成 `名字: 类型`
}
```

Rust 要你把类型写全，是因为函数定义点本身就要足够清晰，不能等调用点再猜。这样 IDE、文档、trait 实现匹配、错误提示都会更稳定。

「✅ 正确写法」——每个参数各写各的类型：

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    assert_eq!(add(10, 20), 30);
}
```

**Go 对比：**

```go
package main

import "fmt"

func add(a, b int) int {
	return a + b
}

func greet(name string) {
	fmt.Println("hello,", name)
}

func main() {
	fmt.Println(add(2, 3))
	greet("Go")
}
```

- **Go 怎么做**：同类型参数可合并写成 `a, b int`，无返回值直接省掉返回列表。
- **Rust 为什么不同**：Rust 把签名看成强约束接口，要求每个参数都显式写出类型，避免二义性并让类型系统工作更直接。
- **Go 程序员易踩的坑**：最容易把 `fn f(a, b: i32)` 当成合法写法；Rust 不接受。

**记忆点：**

- Rust 参数列表里没有“共享类型尾巴”写法。
- 无返回值函数本质上返回 `()`.
- 函数签名是 Rust 类型系统的重要边界，写全不是啰嗦，是规则。

---

## Q2. Rust 函数为什么常常“不写 return”？分号到底在控制什么？ {#q2}
**Tags:** `hot` `beginner` `expression`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 是**表达式语言**：函数体最后一个“没有分号的表达式”就是返回值；多写一个分号，它就从“有值”变成“只执行动作的语句”，返回值也就变成 `()` 了。

**解答：**

先区分两个词：**表达式**（expression，会产生值的代码）和**语句**（statement，只执行动作、不继续提供值的代码）。Rust 的 `if`、`match`、块 `{ ... }` 都可以是表达式。

```rust
fn square(n: i32) -> i32 {
    n * n // 最后一个无分号表达式，直接作为返回值
}

fn abs(n: i32) -> i32 {
    if n >= 0 {
        n
    } else {
        -n
    }
}

fn main() {
    assert_eq!(square(4), 16);
    assert_eq!(abs(-5), 5);
}
```

你当然也可以显式写 `return`，尤其在“提前退出”时很清楚：

```rust
fn classify(n: i32) -> &'static str {
    if n < 0 {
        return "negative";
    }
    "non-negative"
}

fn main() {
    assert_eq!(classify(-1), "negative");
    assert_eq!(classify(8), "non-negative");
}
```

「❌ 错误写法」——最后一行多写了分号，返回值从 `i32` 变成了 `()`：

```rust
fn main() {
    // let value: i32 = { 5; };
    // error[E0308]: mismatched types
    //  expected `i32`, found `()`
    let value: i32 = 5;
    let _ = value;
}
```

块表达式也遵守同一条规则：

```rust
fn main() {
    let x = {
        let base = 3;
        base + 1
    };
    assert_eq!(x, 4);
}
```

**Go 对比：**

```go
package main

import "fmt"

func square(n int) int {
	return n * n
}

func main() {
	x := func() int {
		base := 3
		return base + 1
	}()
	fmt.Println(square(4), x)
}
```

- **Go 怎么做**：普通函数必须显式 `return`；`if` 不是表达式，块也不会自然产出值。
- **Rust 为什么不同**：Rust 让控制流结构本身参与“产值”，这样很多逻辑可以更紧凑，而且编译器能直接检查各分支类型是否一致。
- **Go 程序员易踩的坑**：把分号当成无害结束符；在 Rust 里，它真的会改变类型和返回值。

**记忆点：**

- 最后一行想返回值，就别写分号。
- `return` 主要用于提前退出，不是每个函数结尾都必须写。
- `if`、`match`、块都可以产生值。

---

## Q3. Rust 能像 Go 那样返回多个值吗？该用元组还是结构体？ {#q3}
**Tags:** `hot` `beginner` `tuple`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 没有 Go 那种“返回值列表”语法，但可以返回**元组**（tuple，固定长度、可异构的数据包）来达到同样效果；当字段含义开始变多、变重要时，就该改用结构体。

**解答：**

最直接的写法就是返回元组，再在调用处解构：

```rust
fn div_rem(a: i32, b: i32) -> (i32, i32) {
    (a / b, a % b)
}

fn main() {
    let (q, r) = div_rem(17, 5);
    assert_eq!(q, 3);
    assert_eq!(r, 2);
}
```

不需要的部分可以用 `_` 忽略：

```rust
fn min_max(xs: &[i32]) -> (i32, i32) {
    let mut min = xs[0];
    let mut max = xs[0];
    for &x in xs {
        if x < min {
            min = x;
        }
        if x > max {
            max = x;
        }
    }
    (min, max)
}

fn main() {
    let (_, max) = min_max(&[3, 9, 1, 5]);
    assert_eq!(max, 9);
}
```

字段一多，元组就开始“靠位置猜含义”。这时结构体更稳：

```rust
#[derive(Debug, PartialEq)]
struct ParseStats {
    count: usize,
    sum: i32,
}

fn parse_stats() -> ParseStats {
    ParseStats { count: 3, sum: 60 }
}

fn main() {
    let stats = parse_stats();
    assert_eq!(stats, ParseStats { count: 3, sum: 60 });
}
```

如果还可能失败，就很常见地写成 `Result<(T, U), E>`：

```rust
fn parse_pair(a: &str, b: &str) -> Result<(i32, i32), std::num::ParseIntError> {
    Ok((a.parse()?, b.parse()?))
}

fn main() {
    assert_eq!(parse_pair("10", "20").unwrap(), (10, 20));
}
```

**Go 对比：**

```go
package main

import "fmt"

func divRem(a, b int) (int, int) {
	return a / b, a % b
}

type ParseStats struct {
	Count int
	Sum   int
}

func main() {
	q, r := divRem(17, 5)
	fmt.Println(q, r)

	stats := ParseStats{Count: 3, Sum: 60}
	fmt.Println(stats)
}
```

- **Go 怎么做**：语言原生支持多返回值，尤其常见于“值 + error”。
- **Rust 为什么不同**：Rust 把“一个函数调用的结果”统一看成一个值；这个值可以是元组、结构体、`Result`、`Option` 等。
- **Go 程序员易踩的坑**：总想找 `(x, y)` 以外的“多返回值语法糖”；其实 Rust 的惯用答案就是“返回一个复合值”。

**记忆点：**

- 少量结果：优先元组。
- 结果字段有名字或语义较强：优先结构体。
- “成功多值 / 失败报错”：常写 `Result<(T, U), E>`。

---

## Q4. Rust 的 `if` / `match` 为什么能直接当返回值？ {#q4}
**Tags:** `hot` `beginner` `if` `match`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 Rust 的 `if` 和 `match` 本身就是表达式；只要各分支类型一致，它们整个块就能产出一个值，直接作为函数返回值。

**解答：**

最常见的是把 `if` 当成返回值生成器：

```rust
fn sign(n: i32) -> &'static str {
    if n > 0 {
        "positive"
    } else if n < 0 {
        "negative"
    } else {
        "zero"
    }
}

fn main() {
    assert_eq!(sign(0), "zero");
}
```

`match` 更适合“枚举所有情况”：

```rust
fn grade(score: u8) -> &'static str {
    match score {
        90..=100 => "A",
        75..=89 => "B",
        60..=74 => "C",
        _ => "D",
    }
}

fn main() {
    assert_eq!(grade(88), "B");
}
```

「❌ 错误写法」——分支类型不一致：

```rust
fn main() {
    // let value: i32 = if true { 1 } else { "nope" };
    // error[E0308]: `if` and `else` have incompatible types
    let value: i32 = if true { 1 } else { 0 };
    let _ = value;
}
```

即使写成很多层判断，规则仍然一样：整个表达式只有一个统一类型。某个分支如果是 **never 类型**（`!`，表示永远不会返回到这里），也可以和别的类型统一，这会在 [Q18](#q18) 里讲。

**Go 对比：**

```go
package main

import "fmt"

func sign(n int) string {
	if n > 0 {
		return "positive"
	} else if n < 0 {
		return "negative"
	}
	return "zero"
}

func main() {
	fmt.Println(sign(0))
}
```

- **Go 怎么做**：`if` / `switch` 只负责控制流，不直接产出值，只能在分支里写 `return` 或给外部变量赋值。
- **Rust 为什么不同**：控制流就是表达式后，很多局部逻辑不必先声明可变变量再赋值，代码更贴近“把这个值算出来”。
- **Go 程序员易踩的坑**：会本能地先 `let mut x`，再在每个分支给它赋值；Rust 里很多时候不必这样写。

**记忆点：**

- `if` / `match` 在 Rust 里都是值。
- 各分支类型必须统一。
- 能直接返回时就直接返回，通常比“先声明再赋值”更自然。

---

## Q5. 函数参数传进去时，所有权到底会发生什么？ {#q5}
**Tags:** `hot` `beginner` `ownership` `E0382`
**适用版本:** Rust 1.0+

**一句话答案：**

参数传递默认也是“赋值”规则：对非 `Copy` 类型，传给 `fn f(x: T)` 会 **move**（转移所有权）；传给 `fn f(x: &T)` 则只是**借用**（borrow），调用方还能继续用原值。

**解答：**

先看“被吃掉”的版本。这里 `String` 没有实现 `Copy`，所以把它按值传入函数会把所有权交给函数：

```rust
fn consume(name: String) {
    println!("got {name}");
}

fn main() {
    let s = String::from("Rust");
    consume(s);
    // s 已经失效，不能再用
}
```

「❌ 错误写法」——传给按值参数后还想继续用原变量：

```rust
fn consume(name: String) {
    println!("{name}");
}

fn main() {
    let s = String::from("Rust");
    consume(s);
    // println!("{s}");
    // error[E0382]: borrow of moved value: `s`
}
```

如果你只是想读它，不想拿走所有权，就借用：

```rust
fn print_name(name: &str) {
    println!("name = {name}");
}

fn main() {
    let s = String::from("Rust");
    print_name(&s); // &String 会自动转成 &str
    print_name("Go"); // 字符串字面量本来就是 &str
    println!("{s}"); // 仍然可用
}
```

对于实现了 `Copy` 的小类型，如 `i32`、`bool`，按值传递只是复制一份，不会让原变量失效：

```rust
fn plus_one(n: i32) -> i32 {
    n + 1
}

fn main() {
    let x = 10;
    let y = plus_one(x);
    assert_eq!(x, 10);
    assert_eq!(y, 11);
}
```

**Go 对比：**

```go
package main

import "fmt"

func mutate(xs []int) {
	xs[0] = 99
}

func main() {
	s := "Rust"
	fmt.Println(s) // 字符串按值传，但原变量始终可继续用

	xs := []int{1, 2, 3}
	mutate(xs)      // slice 头按值复制，但底层数组共享
	fmt.Println(xs) // [99 2 3]
}
```

- **Go 怎么做**：参数永远是按值传，但很多值本身是“头部 + 指向底层数据”的结构，所以看起来像“函数里改了外面也变了”。
- **Rust 为什么不同**：Rust 把“谁负责释放资源”也纳入函数调用规则，因此按值参数会接管所有权，避免悬垂指针和二次释放。
- **Go 程序员易踩的坑**：以为“传参只是复制一个头”；在 Rust 里对 `String`、`Vec<T>` 不是这样，函数真的会把值吃掉。

**记忆点：**

- `fn f(x: T)`：函数拿走 `x` 的所有权（若 `T` 非 `Copy`）。
- `fn f(x: &T)`：函数只是借用。
- 遇到 `E0382`，先问自己“我是不是其实只想读它？”

---

## Q6. Rust 函数返回值时，所有权又是怎么交回来的？ {#q6}
**Tags:** `hot` `beginner` `return` `ownership`
**适用版本:** Rust 1.0+

**一句话答案：**

返回值本质上也是一次 move：函数把某个值的所有权交给调用方；因此“把参数吃进去再原样返回”是合法且常见的所有权转移模式。

**解答：**

最简单的例子：函数内部创建一个 `String` 并返回，调用者接管它：

```rust
fn make_name() -> String {
    String::from("Rust")
}

fn main() {
    let name = make_name();
    assert_eq!(name, "Rust");
}
```

你也可以把传进来的值吃进去、加工后再返回：

```rust
fn add_suffix(mut s: String) -> String {
    s.push_str(" language");
    s
}

fn main() {
    let s = String::from("Rust");
    let s = add_suffix(s);
    assert_eq!(s, "Rust language");
}
```

如果只是想“借进来算一圈，再返回结果”，很多时候根本不该接管所有权，而应返回借用计算的结果或新值：

```rust
fn first_len(s: &str) -> usize {
    s.len()
}

fn main() {
    let s = String::from("hello");
    assert_eq!(first_len(&s), 5);
    println!("{s}");
}
```

和“多返回值”结合时，Rust 很常用“把所有权一起带出来”：

```rust
fn trim_and_len(mut s: String) -> (String, usize) {
    s.truncate(s.trim_end().len());
    let len = s.len();
    (s, len)
}

fn main() {
    let (s, len) = trim_and_len(String::from("abc   "));
    assert_eq!(s, "abc");
    assert_eq!(len, 3);
}
```

**Go 对比：**

```go
package main

import "fmt"

func addSuffix(s string) string {
	return s + " language"
}

func main() {
	s := "Rust"
	s = addSuffix(s)
	fmt.Println(s)
}
```

- **Go 怎么做**：返回值不会影响调用方原变量的可用性，因为不存在所有权失效这层语义。
- **Rust 为什么不同**：Rust 把“谁拥有返回出来的资源”说清楚了，所以返回就是把所有权正式交给外层绑定。
- **Go 程序员易踩的坑**：会把“传入并返回”误解为多余；在 Rust 里，这往往是在显式交接资源的责任。

**记忆点：**

- 返回值通常意味着所有权转移给调用方。
- “按值接收，再按值返回”是合法且常见的所有权流动。
- 若函数不该拥有它，就别用按值参数。

---

## Q7. 参数到底该写 `String`、`&String` 还是 `&str`？ {#q7}
**Tags:** `hot` `beginner` `string`
**适用版本:** Rust 1.0+

**一句话答案：**

默认优先写 `&str`：它最通用，既能接收字符串字面量，也能接收 `String` 的借用；只有函数必须拿走所有权或要修改并保留内容时，才写 `String`。

**解答：**

先看推荐写法：只读文本参数几乎总是 `&str`。

```rust
fn shout(s: &str) -> String {
    format!("{}!", s.to_uppercase())
}

fn main() {
    let owned = String::from("rust");
    assert_eq!(shout(&owned), "RUST!");
    assert_eq!(shout("go"), "GO!");
}
```

如果你写成 `&String`，它就只能接收 `String` 的借用，反而更窄：

```rust
fn len_of_string(s: &String) -> usize {
    s.len()
}

fn main() {
    let owned = String::from("rust");
    assert_eq!(len_of_string(&owned), 4);
    // 字面量 "go" 不能直接传给 &String
}
```

「❌ 错误写法」——把只读函数写成按值接收 `String`，调用完原值就没了：

```rust
fn print_len(s: String) {
    println!("{}", s.len());
}

fn main() {
    let name = String::from("rust");
    print_len(name);
    // println!("{name}");
    // error[E0382]: borrow of moved value: `name`
}
```

只有在函数要**接管并保留**或**就地修改后返回**时，才该收 `String`：

```rust
fn append_world(mut s: String) -> String {
    s.push_str(" world");
    s
}

fn main() {
    let s = String::from("hello");
    let s = append_world(s);
    assert_eq!(s, "hello world");
}
```

**Go 对比：**

```go
package main

import "fmt"

func shout(s string) string {
	return s + "!"
}

func main() {
	fmt.Println(shout("rust"))
}
```

- **Go 怎么做**：字符串参数几乎总写 `string`，因为它本身就是只读字符串头，复制成本可控，也不涉及所有权失效。
- **Rust 为什么不同**：`String` 是拥有堆内存的可增长字符串，`&str` 是对 UTF-8 文本的借用视图；写 `&str` 能把接口做得更宽。
- **Go 程序员易踩的坑**：见到“读字符串”就写 `String`，结果把调用方值白白 move 走了。

**记忆点：**

- 只读文本参数：优先 `&str`。
- 很少需要 `&String`，它通常比 `&str` 更差。
- 需要拥有或改完再交回：才用 `String`。

---

## Q8. 泛型函数怎么写？`::<T>` 这个 turbofish 到底在干嘛？ {#q8}
**Tags:** `hot` `beginner` `generics`
**适用版本:** Rust 1.0+

**一句话答案：**

泛型函数用 `fn name<T>(...)` 定义，表示“这份逻辑可用于多种类型”；`::<T>` 叫 **turbofish**，是在编译器推断不出类型参数时，手动把类型写出来。

**解答：**

最基础的泛型函数长这样：

```rust
fn first<T>(xs: &[T]) -> Option<&T> {
    xs.first()
}

fn main() {
    assert_eq!(first(&[1, 2, 3]), Some(&1));
    assert_eq!(first(&["a", "b"]), Some(&"a"));
}
```

如果类型参数还需要满足某种能力，就加 trait 约束。这里的 **trait** 可以先理解成“接口 / 能力集合”：

```rust
fn show<T: std::fmt::Display>(value: T) {
    println!("{value}");
}

fn main() {
    show(42);
    show("rust");
}
```

当推断信息不足时，需要 turbofish：

```rust
fn parse_num<T: std::str::FromStr>(s: &str) -> Result<T, T::Err> {
    s.parse::<T>()
}

fn main() {
    let a: i32 = parse_num("42").unwrap();
    let b = parse_num::<u64>("99").unwrap();
    assert_eq!(a, 42);
    assert_eq!(b, 99);
}
```

「❌ 错误写法」——编译器不知道你想解析成什么：

```rust
fn main() {
    // let n = "42".parse().unwrap();
    // error[E0284]: type annotations needed
    //  cannot satisfy `<_ as FromStr>::Err == _`
}
```

泛型不是运行时“装箱成万能盒子”；Rust 常见做法是 **单态化**（monomorphization，编译器按实际类型生成多份具体代码），因此通常没有动态分发成本。

**Go 对比：**

```go
package main

import "fmt"

func first[T any](xs []T) T {
	return xs[0]
}

func main() {
	fmt.Println(first([]int{1, 2, 3}))
	fmt.Println(first([]string{"a", "b"}))
}
```

- **Go 怎么做**：Go 1.18+ 也有泛型，写法是 `func f[T any](...)`。
- **Rust 为什么不同**：Rust 的 trait 约束更深地嵌进类型系统，很多“这个类型会不会实现某个方法”在编译期就被展开并检查。
- **Go 程序员易踩的坑**：一看到 `::<T>` 就紧张；它只是“这里我来明确告诉编译器类型参数是什么”。

**记忆点：**

- 泛型函数的核心是 `fn f<T>(...)`.
- 有能力要求就写 `T: Trait`.
- 推断不出类型时，用 turbofish `::<T>` 补信息。

---

## Q9. `fn` 指针、函数项、闭包到底有什么差别？为什么有的闭包传不进去？ {#q9}
**Tags:** `hot` `beginner` `closure` `fn-pointer`
**适用版本:** Rust 1.0+

**一句话答案：**

命名函数本身先是**函数项**（function item，某个具体函数自己的唯一类型），可自动退化成 `fn(...) -> ...` **函数指针**；而**闭包**能捕获环境，只有“不捕获任何外部变量”的闭包才能转成 `fn` 指针，捕获了环境的闭包必须用 `Fn` / `FnMut` / `FnOnce` 这类 trait 约束接收。

**解答：**

先看函数指针：它只表示“去调用一段函数代码”，不携带环境状态。

```rust
fn double(x: i32) -> i32 {
    x * 2
}

fn apply(f: fn(i32) -> i32, x: i32) -> i32 {
    f(x)
}

fn main() {
    assert_eq!(apply(double, 3), 6);
}
```

不捕获环境的闭包，也能变成 `fn` 指针：

```rust
fn apply(f: fn(i32) -> i32, x: i32) -> i32 {
    f(x)
}

fn main() {
    let add_one: fn(i32) -> i32 = |x| x + 1;
    assert_eq!(apply(add_one, 5), 6);
}
```

但一旦闭包捕获了外部变量，它就不再只是“函数地址”，而是“代码 + 捕获到的环境”：

```rust
fn apply<F>(f: F, x: i32) -> i32
where
    F: Fn(i32) -> i32,
{
    f(x)
}

fn main() {
    let factor = 10;
    let times = |x| x * factor; // 捕获了 factor
    assert_eq!(apply(times, 3), 30);
}
```

「❌ 错误写法」——把捕获环境的闭包当成 `fn` 指针传：

```rust
fn apply(f: fn(i32) -> i32, x: i32) -> i32 {
    f(x)
}

fn main() {
    let factor = 10;
    let times = |x: i32| x * factor;
    // let _ = apply(times, 3);
    // error[E0308]: mismatched types
    //  expected fn pointer, found closure
    //  note: closures can only be coerced to `fn` types if they do not capture any variables
}
```

如果你只是要“能调用就行”，大多数时候写泛型 `F: Fn(...) -> ...` 比写 `fn(...) -> ...` 更灵活。

**Go 对比：**

```go
package main

import "fmt"

func double(x int) int {
	return x * 2
}

func apply(f func(int) int, x int) int {
	return f(x)
}

func main() {
	factor := 10
	times := func(x int) int { return x * factor }
	fmt.Println(apply(double, 3))
	fmt.Println(apply(times, 3))
}
```

- **Go 怎么做**：命名函数和闭包都统一落到 `func(...) ...` 这个函数类型里。
- **Rust 为什么不同**：Rust 区分“不带环境的函数代码”和“带捕获环境的匿名对象”，这样能更精确地表达零成本调用和捕获语义。
- **Go 程序员易踩的坑**：会以为 `fn(i32) -> i32` 就等于“任何可调用对象”；其实它只接真正的函数或不捕获环境的闭包。

**记忆点：**

- `fn(...) -> ...` 只适合不捕获环境的可调用值。
- 想接收闭包，优先写 `F: Fn(...) -> ...`。
- 命名函数可自动转成函数指针；捕获环境的闭包不行。

---

## Q10. `impl Trait` 放在参数和返回值位置，各代表什么？ {#q10}
**Tags:** `common` `impl-trait`
**适用版本:** 参数位置 `impl Trait`、返回位置 `impl Trait` 已稳定

**一句话答案：**

参数位置的 `impl Trait` 表示“来什么具体类型都行，只要实现了这个 trait”；返回位置的 `impl Trait` 表示“我返回某个具体类型，但我不想把它的真实名字暴露给调用者”。

**解答：**

参数位置常用于把签名写得更短：

```rust
fn print_twice(value: impl std::fmt::Display) {
    println!("{value}");
    println!("{value}");
}

fn main() {
    print_twice(42);
    print_twice("rust");
}
```

这和显式泛型本质相近：

```rust
fn print_twice<T: std::fmt::Display>(value: T) {
    println!("{value}");
    println!("{value}");
}

fn main() {
    print_twice(42);
}
```

返回位置的 `impl Trait` 则常用于隐藏很长、很丑或你不想公开承诺的具体类型：

```rust
fn make_iter() -> impl Iterator<Item = i32> {
    0..3
}

fn main() {
    let collected: Vec<_> = make_iter().collect();
    assert_eq!(collected, vec![0, 1, 2]);
}
```

一个重要限制：返回位置的 `impl Trait` 仍然只能对应“一个确定的具体类型”。根因和下面这个 `if` 表达式一样：分支若落成不同具体类型，编译器就会给出 `E0308`。

```rust
fn main() {
    // let value: i32 = if true { 1 } else { "x" };
    // error[E0308]: `if` and `else` have incompatible types
    let value: i32 = if true { 1 } else { 0 };
    let _ = value;
}
```

**Go 对比：**

```go
package main

import "fmt"

type shower interface {
	String() string
}

type word string

func (w word) String() string { return string(w) }

func printTwice(v fmt.Stringer) {
	fmt.Println(v.String())
	fmt.Println(v.String())
}

func main() {
	printTwice(word("rust"))
}
```

- **Go 怎么做**：参数最像“接收接口”；返回值若想隐藏具体类型，也常直接返回接口。
- **Rust 为什么不同**：参数位置 `impl Trait` 通常仍是静态分发；返回位置 `impl Trait` 则是在“不暴露具体类型”的同时保持静态分发。
- **Go 程序员易踩的坑**：把返回 `impl Trait` 误会成“可以随机返回任何实现了它的类型”；其实不行，底层必须是同一种具体类型。

**记忆点：**

- 参数位置 `impl Trait` 约等于“简写泛型”。
- 返回位置 `impl Trait` = 隐藏具体类型，但仍是一个确定类型。
- 多分支返回不同具体类型时，不能直接用返回位置 `impl Trait`。

---

## Q11. 什么时候该用关联函数，什么时候该用方法？`self` 三种写法又是什么意思？ {#q11}
**Tags:** `common` `method`
**适用版本:** Rust 1.0+

**一句话答案：**

写在 `impl` 里的无 `self` 函数叫**关联函数**（associated function），常用作构造器；带 `self` 的叫方法，`&self` 表示只读借用，`&mut self` 表示可变借用，`self` 表示把整个值吃掉。

**解答：**

先看三种最常见接收者：

```rust
struct Counter {
    value: i32,
}

impl Counter {
    fn new(value: i32) -> Self {
        Self { value }
    }

    fn get(&self) -> i32 {
        self.value
    }

    fn inc(&mut self) {
        self.value += 1;
    }

    fn into_inner(self) -> i32 {
        self.value
    }
}

fn main() {
    let mut c = Counter::new(1);
    assert_eq!(c.get(), 1);
    c.inc();
    assert_eq!(c.into_inner(), 2);
}
```

如果方法只需要读值，优先 `&self`；需要改值时用 `&mut self`；值在此调用后不该再存在时，用 `self`：

```rust
struct Buffer {
    data: String,
}

impl Buffer {
    fn len(&self) -> usize {
        self.data.len()
    }

    fn push_x(&mut self) {
        self.data.push('x');
    }
}

fn main() {
    let mut b = Buffer {
        data: String::from("ab"),
    };
    assert_eq!(b.len(), 2);
    b.push_x();
    assert_eq!(b.data, "abx");
}
```

**Go 对比：**

```go
package main

import "fmt"

type Counter struct {
	Value int
}

func NewCounter(v int) Counter {
	return Counter{Value: v}
}

func (c Counter) Get() int {
	return c.Value
}

func (c *Counter) Inc() {
	c.Value++
}

func main() {
	c := NewCounter(1)
	fmt.Println(c.Get())
	c.Inc()
	fmt.Println(c.Value)
}
```

- **Go 怎么做**：通过值接收者 / 指针接收者区分是否拷贝与是否可改。
- **Rust 为什么不同**：Rust 还要精确表达借用和所有权转移，所以 `self` / `&self` / `&mut self` 三者语义更强。
- **Go 程序员易踩的坑**：把 `self` 当成“只是值接收者”；在 Rust 里它意味着“这个方法会拿走整个对象”。

**记忆点：**

- `Type::new(...)` 常是关联函数。
- `&self` 读，`&mut self` 改，`self` 吃掉。
- 方法接收者不只是调用语法糖，还编码了借用/所有权规则。

---

## Q12. Rust 有函数重载、默认参数、命名参数吗？没有的话怎么替代？ {#q12}
**Tags:** `common` `api-design`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 没有 C++/Java 那种同名函数重载，也没有默认参数和命名参数；常见替代是不同函数名、配置结构体、`Option` 参数、Builder 模式或泛型 + trait。

**解答：**

同名重载在 Rust 里不成立：

```rust
fn greet(name: &str) {
    println!("hello, {name}");
}

fn main() {
    greet("Rust");
}
```

可选参数通常写 `Option<T>`：

```rust
fn connect(host: &str, port: Option<u16>) -> String {
    let port = port.unwrap_or(443);
    format!("{host}:{port}")
}

fn main() {
    assert_eq!(connect("example.com", None), "example.com:443");
    assert_eq!(connect("example.com", Some(8080)), "example.com:8080");
}
```

参数一多时，配置结构体更清楚：

```rust
struct OpenOptions {
    read: bool,
    write: bool,
}

fn open(path: &str, opt: OpenOptions) -> String {
    format!("{path} {} {}", opt.read, opt.write)
}

fn main() {
    let msg = open(
        "demo.txt",
        OpenOptions {
            read: true,
            write: false,
        },
    );
    assert_eq!(msg, "demo.txt true false");
}
```

**Go 对比：**

```go
package main

import "fmt"

type OpenOptions struct {
	Read  bool
	Write bool
}

func open(path string, opt OpenOptions) string {
	return fmt.Sprintf("%s %v %v", path, opt.Read, opt.Write)
}

func main() {
	fmt.Println(open("demo.txt", OpenOptions{Read: true, Write: false}))
}
```

- **Go 怎么做**：Go 也没有函数重载和默认参数，常用配置结构体与不同函数名。
- **Rust 为什么不同**：Rust 更倾向让 API 形状显式、类型驱动，而不是靠语法糖隐藏默认行为。
- **Go 程序员易踩的坑**：会下意识找“能不能多写一个同名版本”；Rust 不支持，直接换设计。

**记忆点：**

- Rust 没有函数重载、默认参数、命名参数。
- 可选参数：`Option<T>`。
- 参数复杂：配置结构体 / Builder。

---

## Q13. 可以在函数里面再定义函数吗？和闭包怎么选？ {#q13}
**Tags:** `common` `nested-fn`
**适用版本:** Rust 1.0+

**一句话答案：**

可以定义嵌套函数，但它**不能捕获外层局部变量**；想用到外层环境，就必须改用闭包。

**解答：**

嵌套函数适合“纯辅助逻辑，不依赖外层状态”：

```rust
fn outer(x: i32) -> i32 {
    fn double(y: i32) -> i32 {
        y * 2
    }

    double(x) + 1
}

fn main() {
    assert_eq!(outer(3), 7);
}
```

如果要捕获外层变量，闭包才行：

```rust
fn outer(x: i32) -> i32 {
    let add_x = |y: i32| y + x;
    add_x(10)
}

fn main() {
    assert_eq!(outer(5), 15);
}
```

「❌ 错误写法」——试图让嵌套 `fn` 直接用外层局部变量：

```rust
fn outer(x: i32) -> i32 {
    fn inner(y: i32) -> i32 {
        // 取消下一行注释会编译失败：嵌套 fn 不能捕获外层的 x
        // y + x
        y
    }
    inner(1) + x
}

fn main() {
    assert_eq!(outer(5), 6);
}
```

**Go 对比：**

```go
package main

import "fmt"

func outer(x int) int {
	inner := func(y int) int {
		return y + x
	}
	return inner(1)
}

func main() {
	fmt.Println(outer(5))
}
```

- **Go 怎么做**：Go 没有“命名嵌套函数”语法，但匿名函数天然可以捕获外层变量。
- **Rust 为什么不同**：Rust 的嵌套 `fn` 仍然是普通函数项，不带环境；只有闭包才是“代码 + 环境”。
- **Go 程序员易踩的坑**：看到嵌套 `fn` 就以为它和闭包一样能捕获 `x`；其实不能。

**记忆点：**

- 嵌套 `fn` 不捕获环境。
- 需要外层局部变量就用闭包。
- “嵌套函数”和“闭包”在 Rust 里不是一个东西。

---

## Q14. `main` 为什么可以返回 `Result`？这样和 `?` 怎么配合？ {#q14}
**Tags:** `common` `main` `question-mark`
**适用版本:** `main -> Result` 已稳定

**一句话答案：**

`main` 可以写成 `fn main() -> Result<(), E>`，这样函数体里就能直接用 `?`；一旦出错，程序会以非零退出码结束并打印错误。

**解答：**

最常见的 CLI 小程序写法如下：

```rust
use std::error::Error;
use std::fs;

fn main() -> Result<(), Box<dyn Error>> {
    let text = fs::read_to_string("Cargo.toml")?;
    println!("{}", text.len());
    Ok(())
}
```

如果你不想让 `main` 返回 `Result`，那就得自己 `match`：

```rust
use std::fs;

fn main() {
    match fs::read_to_string("Cargo.toml") {
        Ok(text) => println!("{}", text.len()),
        Err(err) => {
            eprintln!("read failed: {err}");
            std::process::exit(1);
        }
    }
}
```

「❌ 错误写法」——`main` 还是 `()`，却直接用 `?`：

```rust
fn main() {
    // let text = std::fs::read_to_string("Cargo.toml")?;
    // error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option`
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	data, err := os.ReadFile("go.mod")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(len(data))
}
```

- **Go 怎么做**：`main` 不能返回错误，只能手动 `if err != nil` 再 `os.Exit(1)`。
- **Rust 为什么不同**：Rust 把 `main` 也纳入统一的“返回一个结果值”模型，于是 `?` 可以一路用到程序入口。
- **Go 程序员易踩的坑**：忘记改 `main` 返回类型，结果一上来就撞 `E0277`。

**记忆点：**

- CLI/示例程序里，`main -> Result<(), E>` 很常见。
- 想用 `?`，返回类型必须支持它。
- 需要自定义错误展示和退出码时，再手写 `match`。

---

## Q15. `const fn` 是不是“只能在常量里用”的特殊函数？ {#q15}
**Tags:** `common` `const-fn`
**适用版本:** Rust 1.0+，可用能力随版本逐步扩展

**一句话答案：**

不是。`const fn` 在运行时就是普通函数；它只是额外承诺“这段函数在编译期常量上下文里也能求值”。

**解答：**

先看最基本用法：

```rust
const fn max(a: i32, b: i32) -> i32 {
    if a > b {
        a
    } else {
        b
    }
}

const LIMIT: i32 = max(10, 20);

fn main() {
    assert_eq!(LIMIT, 20);
}
```

同一个 `const fn` 也能在运行时当普通函数调用：

```rust
const fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    let x = add(3, 4);
    assert_eq!(x, 7);
}
```

如果函数体里用了当前稳定版还不允许出现在 const 上下文的操作，它就不能标成 `const fn`；这类限制是“编译期可求值能力”的限制，不是普通调用能力的限制。

**Go 对比：**

```go
package main

import "fmt"

const Limit = 20

func add(a, b int) int {
	return a + b
}

func main() {
	fmt.Println(Limit, add(3, 4))
}
```

- **Go 怎么做**：Go 有 `const`，但没有“可在编译期执行的函数”这层语法。
- **Rust 为什么不同**：Rust 把一部分可纯计算的函数扩展到编译期执行，既复用代码，又让常量定义更灵活。
- **Go 程序员易踩的坑**：把 `const fn` 误以为“特殊且只能给常量用”；其实运行时照样能调。

**记忆点：**

- `const fn` 也是普通函数。
- 它额外支持在常量上下文求值。
- 能不能标 `const`，取决于函数体是否满足当前 stable 的 const 限制。

---

## Q16. Rust 有可变参数函数吗？能不能写成 Go 那样的 `...T`？ {#q16}
**Tags:** `occasional` `variadic`
**适用版本:** 安全 Rust 无通用 variadic

**一句话答案：**

安全 Rust 没有 Go 那种 `...T` 形式的普通可变参数函数；常见替代是切片、迭代器、数组、元组或宏。

**解答：**

最常见的替代是切片：

```rust
fn sum(xs: &[i32]) -> i32 {
    xs.iter().sum()
}

fn main() {
    assert_eq!(sum(&[1, 2, 3]), 6);
}
```

或者更泛化地接收“任何可迭代输入”：

```rust
fn sum<I>(xs: I) -> i32
where
    I: IntoIterator<Item = i32>,
{
    xs.into_iter().sum()
}

fn main() {
    assert_eq!(sum(vec![1, 2, 3]), 6);
    assert_eq!(sum([4, 5]), 9);
}
```

要做“像 `println!` 那样参数个数不固定”的效果，Rust 更常见的武器其实是宏，而不是函数。

**Go 对比：**

```go
package main

import "fmt"

func sum(xs ...int) int {
	total := 0
	for _, x := range xs {
		total += x
	}
	return total
}

func main() {
	fmt.Println(sum(1, 2, 3))
}
```

- **Go 怎么做**：直接用 `...T` 定义 variadic 函数。
- **Rust 为什么不同**：Rust 更倾向把“变长输入”表示为集合/迭代器，把“语法可变形”留给宏系统。
- **Go 程序员易踩的坑**：会到处寻找 `fn f(xs: ...i32)`；稳定 Rust 没这个语法。

**记忆点：**

- 变长输入：优先 `&[T]` 或 `IntoIterator`.
- 想要 `println!` 那种调用体验，通常需要宏。
- 安全 Rust 日常业务代码里没有通用 variadic 函数。

---

## Q17. Rust 支持递归函数吗？需要特别担心什么？ {#q17}
**Tags:** `occasional` `recursion`
**适用版本:** Rust 1.0+

**一句话答案：**

支持递归，但要和 Go 一样警惕栈深；Rust 不保证尾递归优化，所以深递归更稳妥的做法通常还是改写成循环。

**解答：**

普通递归当然可以写：

```rust
fn fact(n: u64) -> u64 {
    if n <= 1 {
        1
    } else {
        n * fact(n - 1)
    }
}

fn main() {
    assert_eq!(fact(5), 120);
}
```

但深递归可能直接把栈打爆，更稳妥的常常是迭代：

```rust
fn fact_iter(n: u64) -> u64 {
    let mut acc = 1;
    for i in 2..=n {
        acc *= i;
    }
    acc
}

fn main() {
    assert_eq!(fact_iter(5), 120);
}
```

**Go 对比：**

```go
package main

import "fmt"

func fact(n uint64) uint64 {
	if n <= 1 {
		return 1
	}
	return n * fact(n-1)
}

func main() {
	fmt.Println(fact(5))
}
```

- **Go 怎么做**：也支持递归，也同样会受栈深影响。
- **Rust 为什么不同**：在函数语义上并无特别不同，但 Rust 社区对“显式控制资源和栈行为”通常更敏感。
- **Go 程序员易踩的坑**：以为编译器会自动把尾递归优化成循环；Rust 不保证。

**记忆点：**

- 递归合法，但深递归要小心栈溢出。
- Rust 不承诺尾递归优化。
- 能写循环时，通常更稳。

---

## Q18. `-> !` 是什么？为什么 `panic!()` 能塞进任何返回类型里？ {#q18}
**Tags:** `advanced` `never`
**适用版本:** `!` 在发散函数中的稳定用法已可依赖

**一句话答案：**

`!` 叫 **never 类型**，表示“这个函数永远不会正常返回”；因为它根本不会产出值，所以编译器允许把它放进任何“本来需要一个值”的位置。

**解答：**

最典型的发散函数是无限循环或直接 panic：

```rust
fn never_returns() -> ! {
    panic!("boom");
}

fn main() {
    let _f: fn() -> ! = never_returns;
}
```

这让 `match` 或 `if` 某个分支可以“没有正常值”，但整体仍然类型成立：

```rust
fn get_name(flag: bool) -> &'static str {
    if flag {
        "rust"
    } else {
        panic!("missing name")
    }
}

fn main() {
    assert_eq!(get_name(true), "rust");
}
```

也可以用于“失败就退出程序”的工具函数：

```rust
fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(1);
}

fn pick(opt: Option<i32>) -> i32 {
    match opt {
        Some(x) => x,
        None => die("missing number"),
    }
}

fn main() {
    assert_eq!(pick(Some(7)), 7);
}
```

**Go 对比：**

```go
package main

import "fmt"

func pick(ok bool) string {
	if ok {
		return "rust"
	}
	panic("missing name")
}

func main() {
	fmt.Println(pick(true))
}
```

- **Go 怎么做**：可以 `panic`，但没有 `!` 这种类型系统层面的“永不返回类型”。
- **Rust 为什么不同**：Rust 把“控制流不会回来”也编码进类型系统，因此很多分支类型检查能更精确。
- **Go 程序员易踩的坑**：看到 `!` 以为是“布尔取反”或什么宏语法；在函数返回位置里，它就是一个真正的类型。

**记忆点：**

- `-> !` = 这个函数永不正常返回。
- `panic!`、`loop {}`、`process::exit` 一类表达式都能体现 never 语义。
- never 类型能和别的返回类型在分支里统一。

---

## Q19. 返回参数里的引用时，生命周期该怎么写？ {#q19}
**Tags:** `hot` `lifetime` `reference` `E0106`
**适用版本:** Rust 1.0+

**一句话答案：**

返回的引用必须“借自某个输入参数（或 `'static` 数据）”，不能借自函数体内的局部变量；多个输入引用时，往往要显式标 `'a`，告诉编译器返回值到底跟谁活得一样久。

**解答：**

单个输入引用时，生命周期省略规则通常够用：

```rust
fn first_word(s: &str) -> &str {
    match s.find(' ') {
        Some(i) => &s[..i],
        None => s,
    }
}

fn main() {
    let s = String::from("hello rust");
    assert_eq!(first_word(&s), "hello");
}
```

两个输入都可能成为返回来源时，省略会失败，必须命名：

```text
// 这样写会报错（缺生命周期）：
// fn longest(x: &str, y: &str) -> &str {
//     if x.len() > y.len() { x } else { y }
// }
// error[E0106]: missing lifetime specifier
```

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let a = String::from("abcd");
    let b = String::from("xyz");
    assert_eq!(longest(&a, &b), "abcd");
}
```

「❌ 错误写法」——返回局部变量引用（悬垂）：

```text
// fn bad() -> &str {
//     let s = String::from("nope");
//     &s
// }
// error[E0515]: cannot return reference to local variable `s`
```

```rust
fn main() {
    let owned = String::from("ok");
    let r: &str = &owned; // 调用方拥有数据时才合法
    println!("{r}");
}
```

需要把“新造出来的数据”交出去时，返回 `String`（所有权），不要返回 `&str`。

**Go 对比：**

```go
package main

import "fmt"

func longest(x, y string) string {
	if len(x) > len(y) {
		return x
	}
	return y
}

func main() {
	fmt.Println(longest("abcd", "xyz"))
}
```

- **Go 怎么做**：`string` 头拷贝很便宜，返回局部 `string` 也安全（底层数据由 GC 管）。
- **Rust 为什么不同**：`&str` 不拥有缓冲，签名必须证明它不会比源数据活得更久。
- **Go 程序员易踩的坑**：按 Go 习惯返回“函数里临时拼的字符串的引用”；在 Rust 里应返回 `String`。

**记忆点：**

- 返回引用 = 必须挂在某个输入（或 `'static`）上。
- 多输入候选来源 → 写 `'a`。
- 新数据用拥有型返回值，别硬返回 `&`。

---

## Q20. `return`、`?` 和尾表达式混用时要注意什么？ {#q20}
**Tags:** `common` `return` `?` `Result` `expression`
**适用版本:** Rust 1.0+

**一句话答案：**

`?` 是“失败就提前返回”的表达式；成功路径常靠**最后一个无分号表达式**（或 `Ok(...)`）收尾。最常见的坑是：前面用了 `?`，最后却直接返回裸值而忘了包进 `Ok`，或尾表达式多写了分号变成 `()`。

**解答：**

标准混用：中间 `?`，末尾 `Ok`（也可写成 `Ok` 包住尾表达式）：

```rust
fn parse_pair(s: &str) -> Result<(i32, i32), std::num::ParseIntError> {
    let mut parts = s.split(',');
    let a = parts.next().unwrap_or("").parse()?;
    let b = parts.next().unwrap_or("").parse()?;
    Ok((a, b)) // 成功路径必须是 Result
}

fn main() {
    assert_eq!(parse_pair("3,4").unwrap(), (3, 4));
}
```

「❌ 错误写法」——`?` 之后尾表达式是元组，类型对不上：

```text
// fn parse_pair(s: &str) -> Result<(i32, i32), std::num::ParseIntError> {
//     let parts: Vec<_> = s.split(',').collect();
//     let a = parts[0].parse()?;
//     let b = parts[1].parse()?;
//     (a, b) // 少了 Ok(...)
// }
// error[E0308]: mismatched types
//   expected enum `Result<(i32, i32), ParseIntError>`
//     found tuple `(_, _)`
```

`return` 适合早退；与尾表达式并存时注意别写“死代码”：

```rust
fn pick(flag: bool) -> Result<&'static str, &'static str> {
    if !flag {
        return Err("no"); // 提前返回
    }
    Ok("yes") // 尾表达式
}

fn main() {
    assert_eq!(pick(true).unwrap(), "yes");
    assert!(pick(false).is_err());
}
```

分号规则（见 [Q2](#q2)）在 `Result` 函数里同样致命：最后一行 `Ok(x);` 会让函数实际返回 `()`。

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func parsePair(s string) (int, int, error) {
	parts := strings.Split(s, ",")
	a, err := strconv.Atoi(parts[0])
	if err != nil {
		return 0, 0, err
	}
	b, err := strconv.Atoi(parts[1])
	if err != nil {
		return 0, 0, err
	}
	return a, b, nil
}

func main() {
	a, b, err := parsePair("3,4")
	fmt.Println(a, b, err)
}
```

- **Go 怎么做**：每个错误分支手写 `if err != nil { return ... }`，成功也显式 `return`。
- **Rust 为什么不同**：`?` 压缩失败路径；成功路径常靠尾表达式/`Ok` 一次写清。
- **Go 程序员易踩的坑**：以为“解析完直接 `(a,b)` 就行”，忘了外层还是 `Result`。

**记忆点：**

- `?` 失败早退；成功路径要落到 `Ok(...)`（或兼容类型）。
- 尾表达式不要多余分号。
- `return` 管早退，别和“最后一行产值”打架。

---
