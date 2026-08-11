+++
title = "06-变量与可变性"
date = 2026-07-28T14:49:00+08:00
weight = 60
type = "docs"
description = "讲清 Rust 变量绑定、可变性、遮蔽、初始化与借用边界。"
isCJKLanguage = true
draft = false

+++

# 变量与可变性 (Variables)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会刚写 Rust 就被“变量默认不可变”绊住？
- 你是否分不清 `mut`、shadowing（遮蔽）和“里面的值能不能改”？
- 你会不会看到 `E0384`、`E0596`、`E0282`、`E0381` 这类错误码时不知道在说哪种变量问题？
- 你是否想知道：为什么 Rust 对“先声明、后赋值”“借用何时结束”这么较真？
- 你会不会把 Go 里对变量、切片、引用的习惯直接带进 Rust，结果处处撞墙？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| binding | — | 绑定 | 名字和某个值之间的绑定关系 | 变量绑定 |
| `mut` | — | 可变绑定标记 | 允许通过该绑定修改值或做可变借用 | 变量可变 |
| shadowing | — | 遮蔽 | 用同名新绑定遮住旧绑定 | 近似重新声明同名变量 |
| scope | — | 作用域 | 变量名字有效的代码区域 | 同概念 |
| `Copy` | — | 按位复制 trait | 赋值时复制而不是 move | 值类型复制近亲 |
| move | — | 所有权移动 | 把值的所有权交给新绑定 | Go 无直接对应 |
| `RefCell` | — | 运行期借用检查容器 | 允许内部可变性，但借用规则改为运行期检查 | 无直接对应 |
| `NLL` | Non-Lexical Lifetimes | 非词法生命周期 | 借用在最后一次使用后就可结束 | 无直接对应 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q5](#q5), [Q7](#q7), [Q9](#q9), [Q16](#q16), [Q17](#q17) |
| `common` | [Q4](#q4), [Q6](#q6), [Q8](#q8), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q15](#q15), [Q18](#q18) |
| `occasional` | [Q13](#q13), [Q14](#q14) |
| `advanced` | [Q4](#q4) |

---

## Q1. 为什么 Rust 变量默认不可变？ {#q1}
**Tags:** `hot` `beginner` `mut`
**适用版本:** Rust 1.0+

**一句话答案：**
Rust 默认让绑定不可变，是为了让代码更容易推理，也让编译器更早发现“你原本没打算改它，却改了”的问题。

**详细解答：**
默认不可变绑定让“会不会变”变成源码里的显式信息：

```rust
fn main() {
    let mut x = 5;
    x = 6;
    println!("{x}");
}
```

```rust
fn main() {
    let x = 5;
    x = 6;
    // error[E0384]: cannot assign twice to immutable variable `x`
    println!("{x}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	x := 5
	x = 6
	fmt.Println(x)
}
```

- **Go 怎么做**：普通变量默认就能改。
- **Rust 为什么不同**：Rust 想把“会不会变化”也变成显式信息。
- **Go 程序员易踩的坑**：忘记写 `mut`，却在心里默认“变量当然能改”。

**小结 / 记忆点：**
- Rust 先假设“不改”，需要改再显式 `mut`。

---

## Q2. `mut` 管的是变量名，还是里面的值？ {#q2}
**Tags:** `hot` `beginner` `mut`
**适用版本:** Rust 1.0+

**一句话答案：**
主要管“这个绑定是否允许被重新赋值，以及是否允许通过它做可变借用”；不是简单地说“里面的值会不会变”。

**详细解答：**
```rust
fn main() {
    let mut v = vec![1, 2];
    v.push(3);
    println!("{v:?}");
}
```

```rust
use std::cell::RefCell;

fn main() {
    let cell = RefCell::new(1);
    *cell.borrow_mut() += 1;
    println!("{}", cell.borrow());
}
```

```rust
fn main() {
    let v = vec![1, 2];
    v.push(3);
    // error[E0596]: cannot borrow `v` as mutable, as it is not declared as mutable
    println!("{v:?}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	v := []int{1, 2}
	v = append(v, 3)
	fmt.Println(v)
}
```

- **Go 怎么做**：切片修改时不会先声明“这个变量可不可变”。
- **Rust 为什么不同**：Rust 把“通过谁去改”变成了类型和借用规则的一部分。
- **Go 程序员易踩的坑**：看到 `let` 就以为“只是不让我重新赋值”，没想到连 `push` 这种需要 `&mut self` 的方法也会受影响。

**小结 / 记忆点：**
- `mut` 首先是绑定级别的信息。

---

## Q3. shadowing（遮蔽）和 `mut` 有什么根本区别？ {#q3}
**Tags:** `hot` `beginner` `shadowing`
**适用版本:** Rust 1.0+

**一句话答案：**
`mut` 是“同一个绑定变了值”；shadowing 是“新建了一个同名绑定”，因此它还能顺手改类型。

**详细解答：**
```rust
fn main() {
    let x = 5;
    let x = x + 1;
    let x = x.to_string();
    println!("{x}");
}
```

```rust
fn main() {
    let mut x = 5;
    x = 6;
    println!("{x}");
}
```

```rust
fn main() {
    let mut spaces = "   ";
    spaces = spaces.len();
    // error[E0308]: mismatched types
    println!("{spaces}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	x := 5
	x = x + 1
	fmt.Println(x)
}
```

- **Go 怎么做**：更多是同一变量反复赋值，少用“同名新绑定”的风格。
- **Rust 为什么不同**：遮蔽很适合表达“同一个概念经过了下一步处理”。
- **Go 程序员易踩的坑**：把 shadowing 当成“奇怪写法”，其实它在 Rust 中非常常见。

**小结 / 记忆点：**
- 改类型时，常优先考虑 shadowing。

---

## Q4. 变量什么时候会离开作用域并被 drop？ {#q4}
**Tags:** `common` `scope` `drop`
**适用版本:** Rust 1.0+

**一句话答案：**
当绑定离开它的作用域时，值就会被 drop；这让你可以用更小的代码块主动缩短借用或资源占用时间。

**详细解答：**
```rust
fn main() {
    let s = String::from("outer");
    {
        let t = String::from("inner");
        println!("{t}");
    }
    println!("{s}");
}
```

```rust
fn main() {
    let mut x = 1;
    {
        let r = &mut x;
        *r += 1;
    }
    let y = &x;
    println!("{y}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	{
		x := 1
		fmt.Println(x)
	}
}
```

- **Go 怎么做**：作用域也存在，但资源释放更多依赖 GC 或 `defer`。
- **Rust 为什么不同**：作用域边界直接影响资源何时释放与借用何时结束。
- **Go 程序员易踩的坑**：忽略“加一层块”在 Rust 里常能直接解决借用冲突。

**小结 / 记忆点：**
- 作用域不仅管名字可见性，也管资源释放时机。

---

## Q5. 解构赋值最常见的写法有哪些？ {#q5}
**Tags:** `hot` `beginner` `destructuring`
**适用版本:** Rust 1.0+

**一句话答案：**
元组、数组、结构体都能直接在 `let` 左边解构；这比先取字段再赋值更自然，也更符合 Rust 的模式匹配风格。

**详细解答：**
```rust
fn main() {
    let (a, b) = (1, 2);
    println!("{a} {b}");
}
```

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let Point { x, y } = Point { x: 1, y: 2 };
    println!("{x} {y}");
}
```

```rust
fn parse(s: &str) -> i32 {
    let Ok(n) = s.parse() else {
        return 0;
    };
    n
}

fn main() {
    println!("{}", parse("42"));
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func pair() (int, int) { return 1, 2 }

func main() {
	a, b := pair()
	fmt.Println(a, b)
}
```

- **Go 怎么做**：多返回值解构很常见。
- **Rust 为什么不同**：Rust 的解构覆盖范围更广，和 `match` / `let else` 连得更紧。
- **Go 程序员易踩的坑**：只把解构理解成“元组拆开”，忽略了结构体和模式解构能力。

**小结 / 记忆点：**
- Rust 的 `let` 左边，本质上是模式。

---

## Q6. 未使用变量警告该怎么优雅处理？ {#q6}
**Tags:** `common` `unused`
**适用版本:** Rust 1.0+

**一句话答案：**
完全不需要这个值时用 `_`；只是暂时不用但想保留它时，用前缀 `_name`。

**详细解答：**
```rust
fn ignore_completely() -> i32 {
    42
}

fn main() {
    // `_`：完全丢弃，不绑定名字
    let _ = ignore_completely();

    // `_name`：保留绑定，只是告诉编译器“我暂时故意不用”
    let _pending = String::from("later");

    println!("ok");
}
```

普通名字声明后完全不用只会触发 **warning**（不是硬错误）；要消警告就改成 `_` / `_name`，而不是无脑 `#[allow(unused_variables)]`。

**🐹 Go 对比：**
```go
package main

func main() {
	_ = 1
}
```

- **Go 怎么做**：同样常用 `_` 忽略值。
- **Rust 为什么不同**：Rust 还把“保留绑定但暂时不用”的 `_name` 当作常见约定。
- **Go 程序员易踩的坑**：无脑 `#[allow(unused_variables)]`，比起 `_` / `_name` 更不精确。

**小结 / 记忆点：**
- `_` = 完全忽略；`_name` = 保留但暂时不用。

---

## Q7. 为什么 `let y = x` 之后，有时 `x` 就不能用了？ {#q7}
**Tags:** `hot` `beginner` `move`
**适用版本:** Rust 1.0+

**一句话答案：**
因为对非 `Copy` 类型，这不是“再多一个引用”，而是发生了 move，所有权从 `x` 转到了 `y`。

**详细解答：**
```rust
fn main() {
    let s = String::from("hello");
    let t = s;
    println!("{t}");
}
```

```rust
fn main() {
    let a = 5;
    let b = a;
    println!("{a} {b}");
}
```

```rust
fn main() {
    let s = String::from("hello");
    let t = s;
    println!("{t}");
    println!("{s}");
    // error[E0382]: borrow of moved value: `s`
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	s := "hello"
	t := s
	fmt.Println(s, t)
}
```

- **Go 怎么做**：赋值后原变量照样能用。
- **Rust 为什么不同**：Rust 必须保证资源只有一个所有者负责释放。
- **Go 程序员易踩的坑**：把所有赋值都想成 Go 式“复制一份还能继续用”。

**小结 / 记忆点：**
- 非 `Copy` 类型的赋值，先怀疑 move。

---

## Q8. 什么类型是 `Copy`？和 `Clone` 怎么区分？ {#q8}
**Tags:** `common` `Copy` `Clone`
**适用版本:** Rust 1.0+

**一句话答案：**
小而简单、无需自定义清理的值类型常能 `Copy`；`Clone` 则是显式复制，可能有堆分配成本。

**详细解答：**
```rust
fn main() {
    let a = 5;
    let b = a;
    println!("{a} {b}");
}
```

```rust
fn main() {
    let s = String::from("x");
    let t = s.clone();
    println!("{t}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	a := 5
	b := a
	fmt.Println(a, b)
}
```

- **Go 怎么做**：值类型复制更自然，字符串和切片又是另一套头部复制语义。
- **Rust 为什么不同**：Rust 需要显式地区分“自动按位复制”和“显式克隆”。
- **Go 程序员易踩的坑**：一看到报错就 `.clone()`，却没想过是否只是该借用。

**小结 / 记忆点：**
- `Copy` 隐式，`Clone` 显式。

---

## Q9. 类型推断什么时候会不够？ {#q9}
**Tags:** `hot` `beginner` `inference`
**适用版本:** Rust 1.0+

**一句话答案：**
当编译器无法从上下文唯一确定类型时，你就得标注类型，最常见于空容器、`parse()`、`collect()`。

**详细解答：**
当编译器无法从上下文唯一确定类型时，你就得标注类型，最常见于空容器、`parse()`、`collect()`：

```rust
fn main() {
    let v: Vec<i32> = Vec::new();
    println!("{}", v.len());
}
```

```rust
fn main() {
    // let v = Vec::new();
    // error[E0282]: type annotations needed for `Vec<_>`
    let v = Vec::<i32>::new();
    println!("{}", v.len());
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	v := []int{}
	fmt.Println(len(v))
}
```

- **Go 怎么做**：类型推断也有，但空字面量场景通常语法更直接。
- **Rust 为什么不同**：同一个构造式常可落到多种目标类型，编译器需要你补一句话。
- **Go 程序员易踩的坑**：以为“编译器应该能猜到”，但事实上上下文根本不够。

**小结 / 记忆点：**
- 猜不到时就标注，别跟编译器赌气。

---

## Q10. `let` 左边还能写哪些模式？ {#q10}
**Tags:** `common` `patterns`
**适用版本:** Rust 1.0+

**一句话答案：**
除了简单名字，你还可以写数组模式、忽略模式、`ref`、`ref mut`、`..` 等。

**详细解答：**
除了简单名字，你还可以写数组模式、忽略模式、`ref`、`ref mut`、`..` 等。

```rust
fn main() {
    let [a, b, c] = [1, 2, 3];
    println!("{a} {b} {c}");
}
```

```rust
fn main() {
    let (first, ..) = (1, 2, 3);
    println!("{first}");
}
```

`ref` / `ref mut` 在模式里按引用绑定，而不是把值 move 出来：

```rust
fn main() {
    let s = String::from("hi");
    let ref r = s; // 等价于 let r = &s;
    println!("{r} {s}");
}
```

```rust
fn main() {
    let mut s = String::from("hi");
    let ref mut r = s; // 等价于 let r = &mut s;
    r.push('!');
    println!("{r}");
}
```

**🐹 Go 对比：**

- **Go 怎么做**：左值模式能力较少。
- **Rust 为什么不同**：Rust 把模式匹配当成语言主轴之一。
- **Go 程序员易踩的坑**：把 `let` 当成只能“放一个变量名”的地方。

**小结 / 记忆点：**
- `let` 左边不是名字列表，而是模式。
- 需要借用而不是 move 时，可用 `ref` / `ref mut`。

---

## Q11. 为什么可变借用和不可变借用不能同时乱来？ {#q11}
**Tags:** `common` `borrow`
**适用版本:** Rust 1.0+

**一句话答案：**
因为 Rust 要保证“要么很多人只读，要么只有一个人能改”，从源头避免数据竞争和悬空别名。

**详细解答：**
```rust
fn main() {
    let mut s = String::from("hi");
    let r1 = &s;
    println!("{r1}");
    let r2 = &mut s;
    r2.push('!');
    println!("{r2}");
}
```

NLL 让借用在最后一次使用后就能结束

```rust
fn main() {
    let mut s = String::from("hi");
    let r1 = &s;
    let r2 = &mut s;
    // error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
    println!("{r1} {r2}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	s := "hi"
	fmt.Println(s)
}
```

- **Go 怎么做**：语言层面对借用别名约束更少，更多依赖程序员习惯与并发工具。
- **Rust 为什么不同**：Rust 直接在编译期卡住危险组合。
- **Go 程序员易踩的坑**：觉得编译器“太严格”，但它其实是在替你挡住日后难排查的问题。

**小结 / 记忆点：**
- 多个只读可以；可写时要独占。

---

## Q12. 为什么循环累加通常写 `let mut sum = 0` 在外面？ {#q12}
**Tags:** `common` `loop`
**适用版本:** Rust 1.0+

**一句话答案：**
因为你想在每轮迭代之间保留同一个绑定的状态；这正是外层 `let mut` 的典型用途。

**详细解答：**
```rust
fn main() {
    let mut sum = 0;
    for i in 1..=3 {
        sum += i;
    }
    println!("{sum}");
}
```

跨迭代保留状态时，常是一个外层 mut 绑定

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	sum := 0
	for i := 1; i <= 3; i++ {
		sum += i
	}
	fmt.Println(sum)
}
```

- **Go 怎么做**：完全类似。
- **Rust 为什么不同**：只是多了 `mut` 这一层显式性。
- **Go 程序员易踩的坑**：忘记 `mut`，结果一边累加一边被编译器拦下。

**小结 / 记忆点：**
- 需要跨轮变化的状态，外层 `mut` 很常见。

---

## Q13. `const` 和 `let` 在函数里怎么选？ {#q13}
**Tags:** `occasional` `const`
**适用版本:** Rust 1.0+

**一句话答案：**
编译期已知且确实想表达“常量”的值可以用函数内 `const`；否则大多数时候普通 `let` 更直接。

**详细解答：**
```rust
fn main() {
    const N: i32 = 10;
    println!("{N}");
}
```

函数里的 `const` 仍然要编译期可求值；只是“这次不会改”的普通值，用 `let` 就够了。真正要跨调用共享、且有固定地址时，再考虑 `static`（见常量篇）。

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	const n = 10
	fmt.Println(n)
}
```

- **Go 怎么做**：函数内也能写 `const`。
- **Rust 为什么不同**：Rust 的 `const` 常跟“编译期可求值”语义绑定得更紧。
- **Go 程序员易踩的坑**：把“我不会改它”直接理解成“就该写 const”。

**小结 / 记忆点：**
- `const` 先问“能否编译期求值”，不是先问“会不会改”。

---

## Q14. 部分移动（partial move）是什么意思？ {#q14}
**Tags:** `occasional` `partial-move`
**适用版本:** Rust 1.0+

**一句话答案：**
当你把结构体里的某个非 `Copy` 字段按值取走后，整个原结构体往往就不能再按完整值使用了，这叫部分移动。

**详细解答：**
取出非 `Copy` 字段后，剩余字段往往还能单独用；但**整体**再当作完整值使用会失败：

```rust
struct Pair {
    a: String,
    b: String,
}

fn main() {
    let p = Pair {
        a: "x".into(),
        b: "y".into(),
    };
    let a = p.a; // 部分移动：拿走 a 的所有权
    println!("{a}");
    println!("{}", p.b); // OK：未移走的字段仍可用
}
```

「❌ 错误写法」——移动字段后还想整体再使用 `p`：

```rust
struct Pair {
    a: String,
    b: String,
}

fn main() {
    let p = Pair {
        a: "x".into(),
        b: "y".into(),
    };
    let a = p.a;
    println!("{a}");
    let _q = p;
    // error[E0382]: use of partially moved value: `p`
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

type Pair struct{ A, B string }

func main() {
	p := Pair{A: "x", B: "y"}
	fmt.Println(p.A, p.B)
}
```

- **Go 怎么做**：结构体字段取值后原结构体一般仍可继续用。
- **Rust 为什么不同**：Rust 需要继续跟踪字段级所有权是否还完整。
- **Go 程序员易踩的坑**：以为“只拿一个字段，整个结构体当然还在”，却忘了被拿走的是所有权。

**小结 / 记忆点：**
- 取走字段的所有权后，别急着再整体使用原值。

---

## Q15. 什么是静态提升和临时值生命周期？ {#q15}
**Tags:** `common` `temporary`
**适用版本:** Rust 1.0+；Edition 2024 对部分临时值规则更严格

**一句话答案：**
有些字面量引用可被提升成 `'static`；但一般临时值不会无条件“帮你活更久”，遇到生命周期不足时，常见修法是先绑到一个 `let` 变量上。

**详细解答：**
整数等字面量引用有时可被提升成 `'static`：

```rust
fn main() {
    let r: &'static i32 = &10;
    println!("{r}");
}
```

临时值生命周期不够时，先绑到 `let` 变量上，让所有者活得够久：

```rust
fn main() {
    let s = String::from("hi");
    let t = s.as_str();
    println!("{t}");
}
```

「❌ 错误写法」——引用仍指向临时值，临时值在语句结束就被丢弃（悬垂引用会被编译器拦住）：

```rust
fn main() {
    let x = String::from("hi").as_str();
    // error[E0716]: temporary value dropped while borrowed
    println!("{x}");
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	s := "x"
	fmt.Println(s)
}
```

- **Go 怎么做**：不会显式讨论 `'static` 这类生命周期语法。
- **Rust 为什么不同**：Rust 要明确区分“值在不在”和“引用能活多久”。
- **Go 程序员易踩的坑**：以为编译器会自动帮临时值延寿到你想要的时候。

**小结 / 记忆点：**
- 生命周期不够时，先试试 `let` 把临时值绑住。

---

## Q16. Rust 里怎么交换两个变量？ {#q16}
**Tags:** `hot` `beginner` `swap`
**适用版本:** Rust 1.0+

**一句话答案：**
优先用 `std::mem::swap(&mut a, &mut b)`；对简单 `Copy` 类型，也可用解构赋值 `(a, b) = (b, a)`。

**详细解答：**
```rust
fn main() {
    let mut a = 1;
    let mut b = 2;
    std::mem::swap(&mut a, &mut b);
    println!("{a} {b}");
}
```

```rust
fn main() {
    let mut x = 3;
    let mut y = 4;
    (x, y) = (y, x);
    println!("{x} {y}");
}
```

非 Copy 类型优先 std::mem::swap，更少踩 move 坑

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	a, b := 1, 2
	a, b = b, a
	fmt.Println(a, b)
}
```

- **Go 怎么做**：多重赋值交换非常自然。
- **Rust 为什么不同**：Rust 也支持，但对非 `Copy` 值更常推荐显式 `swap`。
- **Go 程序员易踩的坑**：对非 `Copy` 类型手写临时变量交换，结果碰上 move 规则。

**小结 / 记忆点：**
- 简单值可解构交换，复杂值优先 `std::mem::swap`。

---

## Q17. move 之后，为什么还能给同一个 `mut` 变量再赋值？ {#q17}
**Tags:** `hot` `beginner` `move` `mut`
**适用版本:** Rust 1.0+

**一句话答案：**
move 废掉的是**旧值**，不是变量名；`mut` 绑定在“值被搬走”之后仍可接收一个新值，相当于给这个名字重新装满合法内容。

**详细解答：**
[Q7](#q7) 说过：非 `Copy` 类型赋值会 move。很多人因此以为“`s` 整个人都死了”，其实死的是里面那个 `String`，绑定槽位还在：

```rust
fn main() {
    let mut s = String::from("hello");
    let t = s; // s 里的值被 move 走了
    s = String::from("world"); // 同一个 mut 绑定重新装入新值
    println!("{t} {s}");
}
```

这和“从未初始化就使用”不同：move 之后、再赋值之前，你不能**读** `s`，但可以**写**：

```rust
fn main() {
    let mut s = String::from("hello");
    let _t = s;
    s = String::from("ok");
    println!("{s}");
}
```

「❌ 错误写法」——move 后、再赋值前去读：

```rust
fn main() {
    let mut s = String::from("hello");
    let _t = s;
    println!("{s}");
    // error[E0382]: borrow of moved value: `s`
}
```

直觉：**`mut` 管的是“这个名字能不能被重新写入”**；move 只是把当前内容的所有权交出去，留下一个空槽，等你再塞新值。不可变绑定 `let s` 则不允许再赋值，move 后就只能换新名字（或 shadowing，见 [Q3](#q3)）。

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	s := "hello"
	t := s
	s = "world"
	fmt.Println(t, s)
}
```

- **Go 怎么做**：赋值后两边都还能用，也谈不上“空槽再填”。
- **Rust 为什么不同**：要保证同一时刻只有一个所有者负责释放；搬走后旧绑定在再赋值前不可读。
- **Go 程序员易踩的坑**：把 `E0382` 理解成“变量名作废”，其实常常只需 `s = 新值` 或改成借用。

**小结 / 记忆点：**
- move ≠ 删除变量名；`mut` 仍可再赋值。
- move 后、赋值前：能写，不能读。

---

## Q18. `if let` 里的临时值作用域有多长？和用 `{}` 提前 drop 怎么比？ {#q18}
**Tags:** `common` `temporary` `if-let` `scope`
**适用版本:** Rust 1.0+

**一句话答案：**
`if let` / `match` 的**审查对象**（scrutinee，被匹配的那个表达式）产生的临时值，会活到整段 `if`/`else`（或整个 `match`）结束；想提前释放，应先绑到 `let`，或像 [Q4](#q4) 那样用更小的 `{}` 包住。

**详细解答：**
临时值不一定在“分号处”就没。`if let` 会把审查对象的临时值延长到分支全部结束，方便你在分支里安全借用它的内部：

```rust
fn main() {
    let text = String::from("42");
    if let Ok(n) = text.parse::<i32>() {
        println!("{n}");
    } // parse 的 Result 临时值在这里才 drop
}
```

持有锁、文件句柄这类**RAII**（Resource Acquisition Is Initialization，资源获取即初始化）守卫时，作用域拉长意味着占用时间更久：

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(1);
    if let Ok(guard) = m.lock() {
        println!("{}", *guard);
    } // guard 在整段 if 结束时才 unlock
    // 这里才能再 lock
    *m.lock().unwrap() += 1;
}
```

想更早结束借用/守卫，先落到具名绑定，或用小块缩小作用域（[Q4](#q4) 的可靠做法）：

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(1);
    {
        let guard = m.lock().unwrap();
        println!("{}", *guard);
    } // 块结束立刻 unlock
    *m.lock().unwrap() += 1;
    println!("{}", *m.lock().unwrap());
}
```

「❌ 易混」——以为临时值在 `if let` 条件求值完就没了，结果后面还想用审查对象里的引用（生命周期不够时编译器会拦；锁场景则是逻辑上持有过久）。

小块 `{}` 提前 drop **靠谱**，而且是惯用法；`if let` 本身没错，只是审查对象的临时生命周期比“一行表达式”更长，资源敏感时优先具名 `let` + 小作用域。

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	if n, err := strconv.Atoi("42"); err == nil {
		fmt.Println(n)
	}
}
```

- **Go 怎么做**：`if` 短变量声明的作用域也覆盖整个 if/else。
- **Rust 为什么不同**：还要精确跟踪临时值何时 drop，直接影响借用与锁释放。
- **Go 程序员易踩的坑**：在 `if let Ok(g) = mutex.lock()` 里干太多事，把临界区无意拉长。

**小结 / 记忆点：**
- `if let` 临时值 ≈ 活到整个 if/else 结束。
- 要早释放：先 `let`，或加 `{}`（见 [Q4](#q4)）。

---
