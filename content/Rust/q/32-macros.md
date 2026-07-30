+++
title = "32-macros"
date = 2026-07-28T14:49:00+08:00
weight = 320
type = "docs"
description = "面向 Go 开发者讲清 Rust 宏、macro_rules!、过程宏、卫生性与常见误区"
isCJKLanguage = true
draft = false

+++

# 宏 (Macros)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你是否只知道 Rust 有 `println!`、`vec!`，但不知道宏和函数到底差在哪？
- 你是否想弄明白 `macro_rules!`、derive 宏、attribute 宏、function-like 过程宏各自干什么？
- 你是否被 `no rules expected this token`、`cannot find macro`、`unresolved module` 一类错误劝退过？
- 你是否想知道 Rust 宏和 Go 的 `go:generate`、代码生成、反射，分别适合解决什么问题？
- 你是否总听人说“卫生性（hygiene）”，但不知道这词落到代码里是什么意思？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| macro | — | 宏 | 编译前展开代码的工具 | `go:generate`/代码生成，部分近似 |
| `macro_rules!` | — | 声明宏 | 用模式匹配 token 写的宏 | 文本模板生成，部分近似 |
| procedural macro | — | 过程宏 | 用 Rust 代码处理 `TokenStream` 的宏 | AST 代码生成 |
| derive macro | — | 派生宏 | `#[derive(...)]` 这类宏 | `stringer` 之类生成器，部分近似 |
| attribute macro | — | 属性宏 | `#[route]` 这类贴在条目上的宏 | 注解生成器 |
| function-like macro | — | 函数式过程宏 | `sql!(...)` 这种像函数调用的宏 | 生成器 DSL |
| token | — | 词法记号 | 宏匹配和生成的最小单位 | token |
| `TokenStream` | — | 记号流 | 过程宏收到和吐出的 token 序列 | AST/token 流 |
| hygiene | — | 卫生性 | 宏展开后尽量避免和调用点局部变量意外冲突 | Go 无直接对应 |
| `$crate` | — | 定义处 crate 路径 | 让导出宏稳定引用自己 crate 内部路径 | 包内绝对导入路径，概念接近 |
| reflection | — | 反射 | 运行时看类型信息的机制 | Go `reflect` |
| DSL | Domain-Specific Language | 领域特定语言 | 为某类问题设计的小语法 | builder/生成器 DSL |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q8](#q8), [Q10](#q10) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q16](#q16), [Q17](#q17), [Q18](#q18) |
| `occasional` | [Q11](#q11) |
| `advanced` | [Q12](#q12) |

---

## Q1. 宏和函数到底差在哪？为什么 `println!` 不是函数？ {#q1}
**Tags:** `hot` `macro` `function`
**适用版本:** Rust 1.0+

**一句话答案：**

函数接收已经类型检查过的值；宏在编译期先接收 token 并展开成代码，再去编译展开结果，所以它能做到“可变参数、生成语句、生成类型或 impl”，这些普通函数做不到。

**解答：**

最直观的例子是 `println!`：

```rust
fn main() {
    let name = "Rust";
    println!("hello {name}");
}
```

函数没法接收这种“格式串 + 任意数量参数 + 生成一大段代码”的能力：

```rust
fn say(msg: &str) {
    println!("{msg}");
}

fn main() {
    say("hello");
}
```

```rust
macro_rules! answer {
    () => {
        42
    };
}

fn main() {
    assert_eq!(answer!(), 42);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	name := "Go"
	fmt.Printf("hello %s\n", name)
}
```

- **Go 怎么做**：很多可变参数需求直接靠普通函数加 `...any`。
- **Rust 为什么不同**：Rust 没有运行时反射式格式化作为默认路线，很多“语法层重复”问题交给宏在编译期解决。
- **Go 程序员易踩的坑**：把宏理解成“更怪的函数”；其实宏先展开、函数后调用，阶段完全不同。

**记忆点：**

- 宏处理 token，函数处理值。
- 宏能生成代码结构，函数不能。

---

## Q2. `macro_rules!` 的基本形状是什么？ {#q2}
**Tags:** `hot` `macro-rules`
**适用版本:** Rust 1.0+

**一句话答案：**

`macro_rules!` 是“左边匹配输入 token，右边生成展开结果”的规则系统；你可以把它想成一个带语法类别的模板匹配器。

**解答：**

最小例子：

```rust
macro_rules! say_hi {
    () => {
        println!("hi");
    };
}

fn main() {
    say_hi!();
}
```

带重复更像真实场景：

```rust
macro_rules! vec_strings {
( $( $x:expr ),* $(,)? ) => {{
    let mut v = Vec::new();
    $( v.push($x.to_string()); )*
    v
}};
}

fn main() {
    let v = vec_strings!["a", "b"];
    assert_eq!(v, vec!["a", "b"]);
}
```

```rust
macro_rules! one_plus_one {
    () => {
        1 + 1
    };
}

fn main() {
    assert_eq!(one_plus_one!(), 2);
}
```

**Go 对比：**

```go
package main

func main() {
	_ = []string{"a", "b"}
}
```

- **Go 怎么做**：类似代码通常直接手写、用生成器，或靠普通语法组合。
- **Rust 为什么不同**：声明宏擅长把“同一种语法模式反复出现”的样板代码收起来。
- **Go 程序员易踩的坑**：看不懂 `$( ... ),*` 时，先把它翻译成“逗号分隔的 0 个或多个表达式”。

**记忆点：**

- 左边是匹配器，右边是展开器。
- 常见元变量类别有 `expr`、`ident`、`ty`、`tt`。

---

## Q3. 声明宏和过程宏有什么本质区别？ {#q3}
**Tags:** `hot` `proc-macro`
**适用版本:** Rust 1.30+（过程宏稳定主线）

**一句话答案：**

声明宏 `macro_rules!` 靠模式匹配 token；过程宏则是“你写一个 Rust 函数去处理 `TokenStream`”。简单重复用声明宏，复杂 AST 改写和派生通常用过程宏。

**解答：**

声明宏：

```rust
macro_rules! answer {
    () => {
        42
    };
}

fn main() {
    assert_eq!(answer!(), 42);
}
```

过程宏常见的是 derive：

```rust
#[derive(Debug)]
struct User {
    id: u64,
}

fn main() {
    println!("{:?}", User { id: 1 });
}
```

```rust
macro_rules! pair {
    ($a:expr, $b:expr) => {
        ($a, $b)
    };
}

fn main() {
    assert_eq!(pair!(1, 2), (1, 2));
}
```

**Go 对比：**

```go
package main

type User struct {
	ID uint64
}

func main() {}
```

- **Go 怎么做**：更多依赖 `go:generate`、模板、反射或手写工具。
- **Rust 为什么不同**：过程宏把“读输入代码再生成代码”放进编译器流程里，用户使用体验更一体化。
- **Go 程序员易踩的坑**：把所有宏需求都往过程宏上靠；多数场景 `macro_rules!` 就够了。

**记忆点：**

- 简单重复用声明宏。
- 结构体/枚举派生代码常用过程宏。

---

## Q4. 什么是卫生性（hygiene）？ {#q4}
**Tags:** `hot` `hygiene`
**适用版本:** Rust 1.0+

**一句话答案：**

卫生性（**hygiene**）是 Rust 宏用来避免“宏里临时变量名字和调用处局部变量意外撞车”的机制；宏自己定义的局部名，默认不会偷偷污染调用者的同名变量。

**解答：**

看这个例子：

```rust
macro_rules! make_x {
    ($v:expr) => {{
        let x = $v;
        x + 1
    }};
}

fn main() {
    let x = 10;
    assert_eq!(make_x!(1), 2);
    assert_eq!(x, 10);
}
```

如果你想让调用者显式提供名字，就把名字作为 `ident` 传入：

```rust
macro_rules! declare_var {
    ($name:ident, $v:expr) => {
        let $name = $v;
    };
}

fn main() {
    declare_var!(answer, 42);
    assert_eq!(answer, 42);
}
```

```rust
macro_rules! keep_outer {
    () => {{
        let tmp = 1;
        tmp
    }};
}

fn main() {
    let tmp = 10;
    assert_eq!(keep_outer!(), 1);
    assert_eq!(tmp, 10);
}
```

**Go 对比：**

```go
package main

func main() {
	x := 10
	_ = x
}
```

- **Go 怎么做**：Go 没有语言内建的卫生宏，所以不存在这套编译期命名隔离规则。
- **Rust 为什么不同**：Rust 宏大量生成局部代码，若不做卫生隔离，变量名冲突会非常常见。
- **Go 程序员易踩的坑**：以为宏展开就是“纯文本替换”；Rust 宏不是 C 预处理器。

**记忆点：**

- Rust 宏不是简单文本替换。
- 宏内部局部名默认有卫生保护。

---

## Q5. `$crate` 是干什么的？ {#q5}
**Tags:** `common` `crate`
**适用版本:** Rust 1.30+

**一句话答案：**

`$crate` 让导出的宏能稳定引用“定义该宏的 crate 自己”的路径，而不是错误地按调用方的模块作用域去找名字。

**解答：**

坏例子：

```rust
fn main() {
    // #[macro_export]
    // macro_rules! bad {
    //     () => { helper::make() };
    // }
}
```

好例子：

```rust
fn main() {
    // #[macro_export]
    // macro_rules! good {
    //     () => { $crate::helper::make() };
    // }
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：包路径通常直接按导入路径解析，不存在导出宏在别人包里展开的同类问题。
- **Rust 为什么不同**：宏展开位置和名字解析位置可能跨 crate，所以需要 `$crate` 这种“回到定义处”的锚点。
- **Go 程序员易踩的坑**：在导出宏里写裸路径，结果一到别的 crate 用就炸。

**记忆点：**

- 只要宏要对外导出并引用本 crate 内部路径，就优先想 `$crate`。

---

## Q6. 为什么会报 `no rules expected this token`？ {#q6}
**Tags:** `common` `errors`
**适用版本:** Rust 1.0+

**一句话答案：**

因为传给 `macro_rules!` 的 token 形状和它的匹配规则对不上；这通常不是“类型错了”，而是“语法形状没匹配上”。

**解答：**

匹配正确：

```rust
macro_rules! only_one {
    ($x:expr) => {
        $x + 1
    };
}

fn main() {
    assert_eq!(only_one!(1), 2);
}
```

多传一个逗号就不匹配：

```rust
fn main() {
    // only_one!(1, 2);
    // error: no rules expected `,`
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：这类错误更像函数参数个数不对。
- **Rust 为什么不同**：声明宏先做语法模式匹配，压根还没走到类型检查阶段。
- **Go 程序员易踩的坑**：看到报错就去怀疑类型；很多宏错误其实要先看 token 形状。

**记忆点：**

- 先对照宏规则，再看调用点 token。
- 宏报错常常发生在类型检查之前。

---

## Q7. 过程宏有哪些种类？ derive / attribute / function-like 各适合什么？ {#q7}
**Tags:** `common` `derive`
**适用版本:** Rust 1.30+

**一句话答案：**

derive 宏最适合“给结构体/枚举补 impl”；attribute 宏适合“改写某个函数、模块或结构体”；function-like 过程宏适合 `sql!(...)`、`html!(...)` 这种 DSL。

**解答：**

derive：

```rust
#[derive(Debug, Clone)]
struct User {
    id: u64,
}

fn main() {}
```

function-like 的用法形状：

```rust
fn main() {
    // sql!(SELECT * FROM users);
}
```

**Go 对比：**

```go
package main

type User struct {
	ID uint64
}

func main() {}
```

- **Go 怎么做**：更多是外部生成器先改源码，再 `go build`。
- **Rust 为什么不同**：过程宏直接接进编译流程，用户只需写一个属性或调用一个宏。
- **Go 程序员易踩的坑**：把 derive 看成“反射”；它发生在编译期，不是运行时看类型。

**记忆点：**

- derive 补 impl。
- attribute 改条目。
- function-like 做 DSL。

---

## Q8. Rust 宏和 Go 的 `go:generate`、反射分别怎么类比？ {#q8}
**Tags:** `hot` `go-compare`
**适用版本:** Rust 1.0+

**一句话答案：**

最粗略地说：`macro_rules!` 更像编译期语法模板，过程宏更像内嵌编译流程的代码生成器，Go 的 `go:generate` 更像编译前外部脚本，反射则是运行时能力，不是一个层级。

**解答：**

Rust 宏示意：

```rust
macro_rules! make_pair {
    ($a:expr, $b:expr) => {
        ($a, $b)
    };
}

fn main() {
    let p = make_pair!(1, 2);
    assert_eq!(p, (1, 2));
}
```

Go `go:generate` 是另一条路线：

```go
package demo

//go:generate stringer -type=State
type State int
```

```rust
fn main() {
    let generated = ("compile-time", "runtime");
    assert_eq!(generated.0, "compile-time");
}
```

```rust
macro_rules! route {
    ($path:literal) => {
        $path
    };
}

fn main() {
    assert_eq!(route!("/users"), "/users");
}
```

**Go 对比：**

```go
package main

import "reflect"

func main() {
	_ = reflect.TypeOf(42)
}
```

- **Go 怎么做**：编译前用 `go:generate` 产文件，运行时用 `reflect` 看类型。
- **Rust 为什么不同**：Rust 宏主要走编译期扩展，不鼓励用运行时反射兜大部分元编程需求。
- **Go 程序员易踩的坑**：把过程宏和反射混成一类；它们一个在编译期，一个在运行时。

**记忆点：**

- `go:generate` 近似外部代码生成。
- 反射是运行时。
- Rust 宏的主战场是编译期。

---

## Q9. 什么时候该优先用函数 / trait / 泛型，而不是宏？ {#q9}
**Tags:** `common` `design`
**适用版本:** Rust 1.0+

**一句话答案：**

只要函数、trait、泛型能清楚表达，就不要先上宏；宏更适合“必须生成语法结构”或“必须做编译期 DSL/派生”的场景。

**解答：**

优先函数：

```rust
fn add_one(x: i32) -> i32 {
    x + 1
}

fn main() {
    assert_eq!(add_one(1), 2);
}
```

只有在你想隐藏重复语法时，宏才更有价值：

```rust
macro_rules! add_two {
    ($x:expr) => {
        $x + 2
    };
}

fn main() {
    assert_eq!(add_two!(1), 3);
}
```

**Go 对比：**

```go
package main

func addOne(x int) int { return x + 1 }

func main() {}
```

- **Go 怎么做**：工程里通常优先普通函数、接口和生成器。
- **Rust 为什么不同**：Rust 宏很强，但也会让错误信息和阅读成本上升。
- **Go 程序员易踩的坑**：看到宏很强就过度使用，结果 API 变难懂、报错也更绕。

**记忆点：**

- 能不用宏，就先不用。
- 宏是为了减少重复和扩语法，不是为了“显得高级”。

---

## Q10. 宏的稳定边界怎么理解？哪些是 stable，哪些别写成 stable？ {#q10}
**Tags:** `hot` `stability`
**适用版本:** Rust 1.97.1

**一句话答案：**

`macro_rules!`、derive/attribute/function-like 过程宏，都是 stable 主线；真正要小心的是某些实验性宏系统细节或新的 matcher 语法，不要把没稳定的扩展写成生产默认方案。

**解答：**

稳定主线：

```rust
macro_rules! ok {
    () => {
        1
    };
}

fn main() {
    assert_eq!(ok!(), 1);
}
```

过程宏主线也稳定，但创建过程宏 crate 需要专门配置：

```rust
fn main() {
    // Cargo.toml 里:
    // [lib]
    // proc-macro = true
}
```

```rust
macro_rules! stable_demo {
    () => {
        "stable"
    };
}

fn main() {
    assert_eq!(stable_demo!(), "stable");
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：代码生成链路更少和更外置。
- **Rust 为什么不同**：Rust 宏系统成熟且强大，但也有实验性边角。
- **Go 程序员易踩的坑**：看见博客里某个炫技 matcher 或实验特性，就误以为 stable 可直接上生产。

**记忆点：**

- `macro_rules!` 和主流过程宏是 stable。
- 写教程或文档时，要明确区分稳定主线和实验玩法。

---

## Q11. 宏报错时先怎么排查？ {#q11}
**Tags:** `occasional` `debug`
**适用版本:** Rust 1.0+

**一句话答案：**

先看“调用 token 是否匹配规则”，再看“展开后生成了什么代码”，最后才看类型检查；宏错误常常不是业务逻辑错，而是展开形状错。

**解答：**

一个简单宏：

```rust
macro_rules! wrap {
    ($x:expr) => {
        Some($x)
    };
}

fn main() {
    let _ = wrap!(1);
}
```

排查时常用工具是看展开结果。先安装 `cargo-expand`，再对目标 crate 展开：

```bash
cargo install cargo-expand
cargo expand
cargo expand --bin your_bin_name
cargo expand --lib
cargo expand path::to::module
```

上面几条分别表示：安装工具、展开当前包默认目标、按二进制名展开、按库目标展开、只展开某个模块路径。展开输出就是宏真正生成的代码，对照它再查匹配规则通常比盯调用点更快。

```rust
macro_rules! wrap {
    ($x:expr) => {
        Some($x)
    };
}

fn main() {
    // 对本文件跑 `cargo expand` 后，wrap!(1) 会展开成 Some(1)
    let _ = wrap!(1);
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：调代码生成器时更像看生成后的 `.go` 文件。
- **Rust 为什么不同**：过程宏和声明宏都嵌在编译流程里，所以“先看展开结果”尤其关键。
- **Go 程序员易踩的坑**：一直盯着调用点，不去看宏规则和展开结果。

**记忆点：**

- 先匹配，再展开，再类型检查。
- `cargo install cargo-expand`，再用 `cargo expand` 看真实展开。

---

## Q12. 过程宏 crate 为什么要单独建？ {#q12}
**Tags:** `advanced` `proc-macro-crate`
**适用版本:** Rust 1.30+

**一句话答案：**

因为过程宏本身要在编译器编译你的业务 crate 之前先被编译并加载，所以它必须作为 `proc-macro = true` 的独立 crate 存在，不能和普通业务库完全混在同一种角色里。

**解答：**

Cargo 配置：

```toml
[lib]
proc-macro = true
```

最小函数签名长这样：

```rust
fn main() {
    // #[proc_macro]
    // pub fn demo(input: TokenStream) -> TokenStream { ... }
}
```

```rust
fn main() {
    let proc_macro_crate_kind = "proc-macro";
    assert_eq!(proc_macro_crate_kind, "proc-macro");
}
```

**Go 对比：**

```go
package main

func main() {}
```

- **Go 怎么做**：生成器通常是独立命令行程序。
- **Rust 为什么不同**：过程宏本质上也是“编译期插件”，只不过通过 crate 形式装进编译链路。
- **Go 程序员易踩的坑**：期望在同一个普通库 crate 里顺手定义过程宏并直接用；Rust 的编译顺序不允许这么简单。

**记忆点：**

- 过程宏 crate 是编译期插件 crate。
- 它之所以独立，是由编译时机决定的。

---

## Q13. 我只是库用户，需要会写 `macro_rules!` 吗？ {#q13}
**Tags:** `common` `macro-rules` `user`
**适用版本:** Rust 1.0+

**一句话答案：**

多数应用/库用户会“调用宏”就够了；不必先学会写 `macro_rules!`。只有你要封装重复语法、写小 DSL，或维护导出宏时，才需要上手写。

**解答：**

日常你会用到 `println!`、`vec!`、`assert_eq!`、各类 `#[derive(...)]`，这些都是“当用户”。会读报错、会查文档比会写匹配器更重要。真正要自己写声明宏，往往是：项目里同一段样板反复出现、想做测试辅助宏、或库要对外提供宏 API。过程宏门槛更高，库用户更少直接写（见 [Q3](#q3)、[Q12](#q12)）。

```rust
fn main() {
    let v = vec![1, 2, 3];
    assert_eq!(v.len(), 3);
    println!("{v:?}");
}
```

```rust
#[derive(Debug, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 1, y: 2 };
    assert_eq!(format!("{p:?}"), "Point { x: 1, y: 2 }");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	fmt.Println([]int{1, 2, 3})
}
```

- **Go 怎么做**：普通用户几乎不写代码生成器；用标准库和手写代码即可。
- **Rust 为什么不同**：宏使用面更广，但“会用”和“会写”仍是两层技能。
- **Go 程序员易踩的坑**：以为学 Rust 必须先啃完整宏系统，结果卡在入门。

**记忆点：**

- 先会调用，再考虑编写。
- 写宏是为了消灭语法级重复，不是KPI。

---

## Q14. 宏里 `$()*` / `$()+` 重复匹配怎么读？ {#q14}
**Tags:** `common` `macro-rules` `repetition`
**适用版本:** Rust 1.0+

**一句话答案：**

`$( ... )*` 表示“这组模式重复 0 次或多次”；`$( ... )+` 是“至少 1 次”。中间的分隔符（如 `,`）写在重复器里，展开侧用同样的 `$( ... )*` 把捕获项逐个吐出。

**解答：**

把 `$( $x:expr ),*` 读成：“逗号分隔的 0 个或多个表达式，捕获到 `$x`”。右边写 `$( push($x); )*` 就是按匹配次数展开。`+` 与 `*` 的差别只在是否允许空输入；还有 `?` 表示 0 或 1 次。先对照 [Q2](#q2) 的基本形状，再看重复器，通常就能读懂 `vec!` 一类宏。

```rust
macro_rules! sum_all {
    ( $( $x:expr ),* $(,)? ) => {{
        let mut total = 0;
        $( total += $x; )*
        total
    }};
}

fn main() {
    assert_eq!(sum_all!(), 0);
    assert_eq!(sum_all!(1, 2, 3), 6);
}
```

```rust
macro_rules! at_least_one {
    ( $( $x:expr ),+ $(,)? ) => {{
        let mut v = Vec::new();
        $( v.push($x); )+
        v
    }};
}

fn main() {
    assert_eq!(at_least_one!(10), vec![10]);
    assert_eq!(at_least_one!(1, 2), vec![1, 2]);
}
```

**Go 对比：**

```go
package main

func main() {
	_ = []int{1, 2, 3}
}
```

- **Go 怎么做**：可变参数是函数层 `...T`，不是编译期 token 重复器。
- **Rust 为什么不同**：声明宏在 token 层描述“语法可以重复几次”。
- **Go 程序员易踩的坑**：把 `$*` 当成正则，忽略分隔符写在哪一层。

**记忆点：**

- `*` = 0+，`+` = 1+，常配分隔符。
- 匹配几次，展开侧就重复几次。

---

## Q15. `#[macro_export]` / 导入宏的现代写法是什么？ {#q15}
**Tags:** `common` `macro-export` `use`
**适用版本:** Rust 1.0+；`use` 导入宏为现代主线

**一句话答案：**

库要对外提供声明宏时加 `#[macro_export]`（宏会出现在 crate 根）；调用方用 `use your_crate::macro_name;` 导入后再 `macro_name!()`。老式 `#[macro_use] extern crate ...` 已不作为新代码默认写法。

**解答：**

导出宏里引用本 crate 路径时记得用 `$crate`（见 [Q5](#q5)）。2018 edition 之后，宏可以像普通路径一样 `use`；同一 crate 内，宏需先定义再使用，或放在合适模块并 `use` 进来。过程宏则是依赖对应 crate 后 `use` derive/属性/函数式宏名字，而不是 `macro_export`。

```rust
macro_rules! local_answer {
    () => {
        42
    };
}

fn main() {
    assert_eq!(local_answer!(), 42);
}
```

```rust
fn main() {
    // 库侧示意（签名示意，非完整程序）:
    // #[macro_export]
    // macro_rules! answer { () => { 42 }; }
    //
    // 用户侧:
    // use some_crate::answer;
    // assert_eq!(answer!(), 42);
    let imported_style = "use crate::macro_name;";
    assert!(imported_style.contains("use "));
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	fmt.Println("import path, then call")
}
```

- **Go 怎么做**：`import` 包路径，再调用导出符号。
- **Rust 为什么不同**：宏也曾靠 `#[macro_use]` 注入命名空间；现代写法对齐普通 `use`。
- **Go 程序员易踩的坑**：照抄旧教程的 `#[macro_use] extern crate`，和新 edition 项目风格打架。

**记忆点：**

- 导出：`#[macro_export]`。
- 导入：优先 `use path::macro_name;`。

---

## Q16. 能用函数/泛型解决时，为什么还要（或不该）上宏？derive 报错怎么定位？ {#q16}
**Tags:** `common` `design` `derive` `debug`
**适用版本:** Rust 1.0+

**一句话答案：**

函数/泛型能表达就优先它们（见 [Q9](#q9)）；宏留给“必须生成语法/impl/DSL”的缺口。derive 报错先看属性是否合法、字段是否满足 trait bound，再用 `cargo expand` 看展开后的 impl。

**解答：**

该上宏的信号：要在编译期根据 token 生成 `impl`、可变语法、或检查字面量形状。不该上宏的信号：只是少打几行样板、却把类型错误变成晦涩的宏匹配错误。derive 出错时，消息常指向生成代码：确认 `#[derive(Debug)]` 等依赖的字段类型也实现了对应 trait；复杂 derive（serde 等）先读属性文档。展开排查：

```bash
cargo install cargo-expand
cargo expand
```

对照展开后的 `impl` 再改原类型定义，通常比死盯调用点快（与 [Q11](#q11) 同一套路）。

```rust
#[derive(Debug, Clone, PartialEq)]
struct User {
    id: u64,
}

fn main() {
    let a = User { id: 1 };
    let b = a.clone();
    assert_eq!(a, b);
}
```

```rust
fn add_one(x: i32) -> i32 {
    x + 1
}

fn main() {
    assert_eq!(add_one(1), 2);
}
```

**Go 对比：**

```go
package main

type User struct {
	ID uint64
}

func main() {}
```

- **Go 怎么做**：优先普通函数/接口；特殊代码生成走 `go:generate`。
- **Rust 为什么不同**：derive 把“补 impl”变成一等体验，但也把部分错误推到生成代码里。
- **Go 程序员易踩的坑**：derive 一红就怀疑编译器，不看字段是否缺 `Debug`/`Clone` 等 bound。

**记忆点：**

- 能函数/泛型就别先上宏。
- derive 报错：查 bound → 必要时 `cargo expand`。

---

## Q17. `include_str!` / `include_bytes!` / `env!` / `concat!` 各干什么？ {#q17}
**Tags:** `common` `include_str` `env` `concat`
**适用版本:** Rust 1.0+

**一句话答案：** 它们都是**编译期**嵌入常量的内置宏：`include_str!`/`include_bytes!` 把源码旁文件嵌成 `&'static str` / `&'static [u8]`；`env!` 读编译期环境变量；`concat!` 把字面量拼接成一个字符串字面量。

**解答：**

| 宏 | 得到什么 | 典型用途 |
|---|---|---|
| `include_str!("path")` | `&'static str` | 嵌入 LICENSE、SQL、HTML 模板 |
| `include_bytes!("path")` | `&'static [u8]` | 嵌入图标、证书、二进制资源 |
| `env!("VAR")` | `&'static str` | 读 `PATH`，或 Cargo 注入的 `CARGO_PKG_VERSION` 等 |
| `concat!("a", "b")` | `&'static str` | 拼字面量、拼进其他宏参数 |

路径相对于**包含该宏调用的源文件**；文件不存在则编译失败。`env!` 变量缺失也会直接编不过；若允许缺失用 `option_env!`。

```rust
fn main() {
    let msg = concat!("hello", "-", "rust");
    assert_eq!(msg, "hello-rust");
    // 编译期读环境变量（本机通常都有 PATH）
    assert!(!env!("PATH").is_empty());
}
```

```rust
fn main() {
    // Cargo 构建时常见：env!("CARGO_PKG_NAME")、env!("CARGO_MANIFEST_DIR")
    // 资源文件则写：include_str!("../LICENSE")、include_bytes!("logo.png")
    const BANNER: &str = concat!("built-with-", "rustc");
    assert!(BANNER.starts_with("built-with-"));
}
```

和运行时 `std::fs::read_to_string` 的差别：`include_*` 把内容打进二进制，无该文件的机器也能跑，但改资源必须重新编译。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	// Go 1.16+ 可用 //go:embed 把文件打进二进制（构建时需要真实文件存在）
	// 这里用字面量示意“编译期嵌入”的结果形态：
	hello := "hello from embedded asset"
	fmt.Println(hello)
}
```

- **Go 怎么做**：`//go:embed` 嵌入文件；构建信息常用 `ldflags` 注入。
- **Rust 为什么不同**：用内置宏在表达式位置直接得到 `'static` 数据。
- **Go 程序员易踩的坑**：把 `include_str!` 当成运行时读文件；路径是编译期、相对源文件的。

**记忆点：**

- `include_*` = 编译期打进二进制；`env!` = 编译期环境变量；`concat!` = 字面量拼接。
- 缺文件/缺环境变量 → 编译失败，不是运行时 `Err`。

---

## Q18. `macro_rules!` 分隔符和尾随逗号为啥总匹配失败？ {#q18}
**Tags:** `common` `macro_rules` `trailing-comma`
**适用版本:** Rust 1.0+

**一句话答案：** 重复匹配里的分隔符（如 `,`）写在哪一层、是否允许尾随逗号，都是模式的一部分；调用处多一个逗号或少一个分隔符，就会变成 `no rules expected this token`（见 [Q6](#q6)、[Q14](#q14)）。

**解答：** 规则 `($($x:expr),+)` 表示“至少一个表达式，两两之间有逗号”，**默认不接受**末尾多余逗号。要支持 `foo!(1, 2,)`，得显式写可选尾随逗号，例如 `($($x:expr),+ $(,)?)`。

「❌ 错误写法」——规则不收尾随逗号，调用却写了：

```rust
macro_rules! pair {
    ($a:expr, $b:expr) => {
        ($a, $b)
    };
}

fn main() {
    // let _ = pair!(1, 2,);
    // error: no rules expected `,`
}
```

「✅ 正确写法」——要么调用别写尾逗号，要么规则允许：

```rust
macro_rules! sum {
    ($($x:expr),+ $(,)?) => {{
        let mut total = 0;
        $( total += $x; )*
        total
    }};
}

fn main() {
    assert_eq!(sum!(1, 2), 3);
    assert_eq!(sum!(1, 2, 3,), 6); // 尾随逗号 OK
}
```

分隔符也必须和规则一致：`($($x:expr);+)` 要用分号调用；把 `,` 写在 `)*` 外面还是里面，决定“重复体之间”还是“整段之后”的 token。匹配失败时先对照规则画 token，再改调用或改宏（见 [Q11](#q11)）。

**Go 对比：**

```go
package main

func sum(xs ...int) int {
	n := 0
	for _, x := range xs {
		n += x
	}
	return n
}

func main() {
	_ = sum(1, 2, 3)
}
```

- **Go 怎么做**：`...T` 是真正的可变参数，尾随逗号由语法统一允许。
- **Rust 为什么不同**：声明宏先做 token 模式匹配，逗号是模式的一部分，不是“参数列表糖”。
- **Go 程序员易踩的坑**：习惯函数调用随便加尾逗号，套到 `macro_rules!` 上就红。

**记忆点：**

- 尾随逗号要规则里写 `$(,)?`（或等价形式）才收。
- 分隔符写错层 = 形状不匹配，优先查宏定义不是查类型。

---
